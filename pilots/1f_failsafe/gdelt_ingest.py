"""
GDELT v2 country-day ingest for Pilot #150 (1/f-as-L0-failsafe signature).

Downloads GDELT v2 *export* (events) 15-minute slices over the pre-registered
window and stream-aggregates them into daily per-country signals. No raw files
are stored on disk; only the running accumulator state (checkpoint pickle) and
the final per-signal CSVs are persisted.

Why client-side aggregation: this machine has no BigQuery / AWS credentials
(the pre-registration's canonical BigQuery path, §5.1). Direct slice download +
client-side GROUP BY SQLDATE reproduces exactly the daily aggregates BigQuery
`gdelt-bq.gdeltv2.events` GROUP BY SQLDATE would yield, modulo events ADDED to
GDELT after this download (only affects the final ~few SQLDATE days). Logged as
a confound in confounds.md.

Aggregation is keyed by SQLDATE (field 1) per pre-registration §5.1 step 2, NOT
by the slice timestamp (DATEADDED). Country is matched on ActionGeo_CountryCode
(field 53, FIPS 2-letter) per the locked operationalization (pilot.py
GDELT_INGEST_INSTRUCTIONS + candidate doc §3).

Signals per (country, day):
  event_count       -- number of events
  mean_tone         -- mean of AvgTone (field 34)  [secondary, tone caveat]
  category_entropy  -- Shannon entropy (bits) of EventRootCode (field 28)  [PRIMARY]

Run:
  python gdelt_ingest.py --mode ingest    # download + accumulate (resumable)
  python gdelt_ingest.py --mode finalize   # (re)write CSVs from checkpoint

Resumable: re-running --mode ingest resumes from the last checkpointed slice-day.
"""

from __future__ import annotations

import argparse
import io
import math
import pickle
import sys
import time
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import requests

# ----------------------------------------------------------------------------
# Locked configuration (pre-registration + confounds.md §1 N=6 amendment)
# ----------------------------------------------------------------------------

# FIPS 2-letter (ActionGeo_CountryCode) -> ISO3-style label used in pairs table.
FIPS_TO_LABEL = {
    "CH": "CHN", "US": "USA",   # pair 1
    "RS": "RUS", "UK": "GBR",   # pair 2
    "KN": "PRK", "GM": "DEU",   # pair 3
    "IR": "IRN", "FR": "FRA",   # pair 4
    "TU": "TUR", "NL": "NLD",   # pair 5
    "VE": "VEN", "CI": "CHL",   # pair 6
}
TARGET_FIPS = set(FIPS_TO_LABEL)

# Pre-registered window: 2015-01-01 .. 2026-01-01. GDELT v2 begins 2015-02-18,
# so the effective SQLDATE floor is data-limited to v2 availability.
SQLDATE_LO = "20150218"
SQLDATE_HI = "20260101"  # exclusive
SLICE_DAY_START = date(2015, 2, 18)
SLICE_DAY_END = date(2026, 1, 1)   # exclusive (last slice-day = 2025-12-31)

BASE_URL = "http://data.gdeltproject.org/gdeltv2/{}.export.CSV.zip"

# Field indices in the 61-column GDELT 2.0 Event (export) schema (0-indexed).
F_SQLDATE = 1
F_ROOTCODE = 28
F_TONE = 34
F_ACTIONGEO_CC = 53

HERE = Path(__file__).resolve().parent
STATE_PATH = HERE / "data" / "gdelt_state.pkl"
RAW_DIR = HERE / "data" / "raw"
LOG_PATH = HERE / "data" / "gdelt_ingest.log"

WORKERS = 20
CKPT_EVERY_DAYS = 15   # checkpoint cadence (slice-days)
RETRIES = 4


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def slice_stamps(d: date) -> list[str]:
    ymd = d.strftime("%Y%m%d")
    return [f"{ymd}{h:02d}{m:02d}00" for h in range(24) for m in (0, 15, 30, 45)]


def new_state() -> dict:
    return {
        "counts": defaultdict(int),                      # (label, sqldate) -> int
        "tone_sum": defaultdict(float),                  # (label, sqldate) -> float
        "root_hist": defaultdict(lambda: defaultdict(int)),  # (label,sqldate)->{root:int}
        "done_days": set(),                              # slice-day "YYYYMMDD" completed
        "failed_stamps": [],                             # stamps that errored after retries
        "missing_stamps": 0,                             # count of 404 (expected outages)
        "events_kept": 0,
    }


def load_state() -> dict:
    # SAFETY: gdelt_state.pkl is written exclusively by save_state() in this same
    # script (local checkpoint for resume). It is never sourced from anywhere
    # untrusted, so pickle load is safe here. Tuple-keyed defaultdicts make pickle
    # the pragmatic serializer (JSON can't represent tuple keys without transform).
    if STATE_PATH.exists():
        with open(STATE_PATH, "rb") as fh:
            s = pickle.load(fh)
        # restore defaultdict behavior after unpickle
        s["counts"] = defaultdict(int, s["counts"])
        s["tone_sum"] = defaultdict(float, s["tone_sum"])
        rh = defaultdict(lambda: defaultdict(int))
        for k, v in s["root_hist"].items():
            rh[k] = defaultdict(int, v)
        s["root_hist"] = rh
        s["done_days"] = set(s["done_days"])
        return s
    return new_state()


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    # convert defaultdicts to plain dicts for stable pickling
    dump = {
        "counts": dict(state["counts"]),
        "tone_sum": dict(state["tone_sum"]),
        "root_hist": {k: dict(v) for k, v in state["root_hist"].items()},
        "done_days": list(state["done_days"]),
        "failed_stamps": state["failed_stamps"],
        "missing_stamps": state["missing_stamps"],
        "events_kept": state["events_kept"],
    }
    tmp = STATE_PATH.with_suffix(".pkl.tmp")
    with open(tmp, "wb") as fh:
        pickle.dump(dump, fh, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(STATE_PATH)


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "agnostic-framework-pilot150/1.0 (research; contact via repo)"})
    # size the connection pool to the worker count so threads get real concurrency
    adapter = requests.adapters.HTTPAdapter(pool_connections=4, pool_maxsize=WORKERS + 4)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def fetch(session: requests.Session, stamp: str) -> tuple[str, object]:
    """Return (status, payload). status in {'ok','missing','error'}."""
    for attempt in range(RETRIES):
        try:
            r = session.get(BASE_URL.format(stamp), timeout=90)
            if r.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                return "ok", z.read(z.namelist()[0]).decode("latin-1")
            if r.status_code == 404:
                return "missing", None
            time.sleep(1.5 * (attempt + 1))
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return "error", None


def accumulate(state: dict, data: str) -> None:
    counts = state["counts"]; tone_sum = state["tone_sum"]; root_hist = state["root_hist"]
    kept = 0
    for line in data.split("\n"):
        if not line:
            continue
        f = line.split("\t")
        if len(f) <= F_ACTIONGEO_CC:
            continue
        cc = f[F_ACTIONGEO_CC]
        if cc not in TARGET_FIPS:
            continue
        sqldate = f[F_SQLDATE]
        if not (SQLDATE_LO <= sqldate < SQLDATE_HI):
            continue
        label = FIPS_TO_LABEL[cc]
        key = (label, sqldate)
        counts[key] += 1
        try:
            tone_sum[key] += float(f[F_TONE])
        except (ValueError, IndexError):
            pass
        root = f[F_ROOTCODE]
        if root:
            root_hist[key][root] += 1
        kept += 1
    state["events_kept"] += kept


def ingest(workers: int = WORKERS) -> None:
    state = load_state()
    session = make_session()

    all_days = []
    d = SLICE_DAY_START
    while d < SLICE_DAY_END:
        all_days.append(d)
        d += timedelta(days=1)
    todo = [d for d in all_days if d.strftime("%Y%m%d") not in state["done_days"]]

    total = len(all_days)
    done0 = len(state["done_days"])
    log(f"INGEST start: {total} slice-days total, {done0} already done, {len(todo)} to go. "
        f"workers={workers}")

    t_run = time.time()
    processed = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for d in todo:
            ymd = d.strftime("%Y%m%d")
            stamps = slice_stamps(d)
            results = list(ex.map(lambda s: fetch(session, s), stamps))
            for stamp, (status, payload) in zip(stamps, results):
                if status == "ok":
                    accumulate(state, payload)
                elif status == "missing":
                    state["missing_stamps"] += 1
                else:
                    state["failed_stamps"].append(stamp)
            state["done_days"].add(ymd)
            processed += 1

            if processed % CKPT_EVERY_DAYS == 0 or d == todo[-1]:
                save_state(state)
                done_now = done0 + processed
                elapsed = time.time() - t_run
                rate = processed / elapsed if elapsed > 0 else 0
                remaining = (len(todo) - processed) / rate if rate > 0 else float("nan")
                log(f"  {ymd}  days={done_now}/{total} ({100*done_now/total:4.1f}%)  "
                    f"events_kept={state['events_kept']:,}  "
                    f"fail={len(state['failed_stamps'])} miss={state['missing_stamps']}  "
                    f"rate={rate*86400/86400:.2f} d/s  ETA={remaining/60:.0f} min")

    save_state(state)
    log(f"INGEST complete: events_kept={state['events_kept']:,}  "
        f"failed_stamps={len(state['failed_stamps'])}  missing={state['missing_stamps']}")
    finalize(state)


def shannon_entropy_bits(hist: dict) -> float:
    tot = sum(hist.values())
    if tot == 0:
        return float("nan")
    h = 0.0
    for v in hist.values():
        if v > 0:
            p = v / tot
            h -= p * math.log2(p)
    return h


def finalize(state: dict | None = None) -> None:
    if state is None:
        state = load_state()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    counts = state["counts"]; tone_sum = state["tone_sum"]; root_hist = state["root_hist"]

    # full daily date index across the window (continuous; gap handling in pilot.py)
    lo = date(int(SQLDATE_LO[:4]), int(SQLDATE_LO[4:6]), int(SQLDATE_LO[6:8]))
    hi = date(int(SQLDATE_HI[:4]), int(SQLDATE_HI[4:6]), int(SQLDATE_HI[6:8]))
    all_dates = []
    d = lo
    while d < hi:
        all_dates.append(d.strftime("%Y%m%d"))
        d += timedelta(days=1)

    labels = sorted(set(FIPS_TO_LABEL.values()))
    written = []
    for label in labels:
        for signal in ("event_count", "mean_tone", "category_entropy"):
            rows = []
            for ds in all_dates:
                key = (label, ds)
                c = counts.get(key, 0)
                if signal == "event_count":
                    val = c  # 0 means no events that SQLDATE (or pre-data); pilot.py handles
                    present = key in counts
                elif signal == "mean_tone":
                    val = (tone_sum.get(key, 0.0) / c) if c > 0 else ""
                    present = c > 0
                else:  # category_entropy
                    val = shannon_entropy_bits(root_hist[key]) if c > 0 else ""
                    present = c > 0
                iso = f"{ds[:4]}-{ds[4:6]}-{ds[6:8]}"
                rows.append(f"{iso},{val}")
            out = RAW_DIR / f"{label}_{signal}.csv"
            with open(out, "w", encoding="utf-8") as fh:
                fh.write("date,value\n")
                fh.write("\n".join(rows) + "\n")
            written.append(out.name)
    log(f"FINALIZE wrote {len(written)} CSVs to {RAW_DIR} over {len(all_dates)} daily rows each")

    # coverage summary
    log("Coverage (non-empty days per country, category_entropy signal):")
    for label in labels:
        nonempty = sum(1 for ds in all_dates if counts.get((label, ds), 0) > 0)
        total_events = sum(counts.get((label, ds), 0) for ds in all_dates)
        log(f"  {label}: {nonempty}/{len(all_dates)} days with events, {total_events:,} total events")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["ingest", "finalize"], default="ingest")
    ap.add_argument("--workers", type=int, default=WORKERS)
    args = ap.parse_args()
    if args.mode == "ingest":
        ingest(workers=args.workers)
    else:
        finalize()


if __name__ == "__main__":
    main()
