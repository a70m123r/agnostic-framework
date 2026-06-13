# -*- coding: utf-8 -*-
"""
P-L4 follow-up: NAME the local-canon spike events (canon-radius 'when' half).
Fetches the Wikimedia top-articles endpoint for the 4 strongest single-pond
spike dates found by harness_signature_instrument.py, cached to disk.
Also computes pair-level co-movement days (both ponds z>1.5) from the saved
residual z-scores to answer 'which pairs co-move and when'.
"""
import json, pathlib, time, datetime as dt
import numpy as np
import requests

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
UA = {"User-Agent": "agnostic-framework-research/0.1 (research instrument)"}
PONDS = ["en", "ja", "de", "ar", "es"]
PROJ = {p: f"{p}.wikipedia.org" for p in PONDS}
MAIN = ("2026030100", "2026060100")

EVENTS = [("en", "2026-04-02"), ("ja", "2026-05-06"),
          ("de", "2026-05-14"), ("es", "2026-04-12")]

def fetch_top(proj, y, m, d):
    f = DATA / f"top_{proj}_{y}{m}{d}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
           f"{proj}/all-access/{y}/{m}/{d}")
    for attempt in range(6):
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code == 200:
            f.write_text(json.dumps(r.json()), encoding="utf-8")
            time.sleep(12.0)
            return r.json()
        print("retry", proj, r.status_code, flush=True)
        time.sleep(25 * (attempt + 1))
    return None

# ---- name the spikes
named = {}
for p, date in EVENTS:
    y, m, d = date.split("-")
    j = fetch_top(PROJ[p], y, m, d)
    arts = j["items"][0]["articles"]
    skip = ("Main_Page", "メインページ", "Wikipedia:Hauptseite",
            "Wikipedia:Portada", "الصفحة_الرئيسية")
    top = [(a["article"], a["views"]) for a in arts
           if a["article"] not in skip and ":" not in a["article"]][:5]
    named[f"{p}@{date}"] = top
    print(f"{p}@{date}:")
    for a, v in top:
        print(f"    {v:>9,}  {a}")

# ---- pair co-movement days (recompute z from cached hourly, same pipeline)
def load(proj):
    f = DATA / f"hourly_{proj}_all-access_{MAIN[0]}_{MAIN[1]}.json"
    items = json.loads(f.read_text(encoding="utf-8"))["items"]
    v = np.array([max(float(it["views"]), 1.0) for it in items[:91 * 24]])
    return v.reshape(91, 24).sum(axis=1)

d0 = dt.date(2026, 3, 1)
dow = np.array([(d0 + dt.timedelta(days=i)).weekday() for i in range(91)])
Z = {}
for p in PONDS:
    x = np.log10(load(PROJ[p]))
    t = np.arange(91); A = np.c_[np.ones(91), t]
    x = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]
    for w in range(7):
        x[dow == w] -= x[dow == w].mean()
    Z[p] = x / x.std()

print("\npair co-move days (both z>1.5):")
pair_days = {}
for i, a in enumerate(PONDS):
    for b in PONDS[i + 1:]:
        days = [str(d0 + dt.timedelta(days=int(k)))
                for k in np.where((Z[a] > 1.5) & (Z[b] > 1.5))[0]]
        pair_days[f"{a}-{b}"] = days
        print(f"  {a}-{b}: {len(days):d}  {days}")

out = dict(named_events=named, pair_comove_days=pair_days)
(HERE / "named_events.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
print("\nsaved -> named_events.json")
