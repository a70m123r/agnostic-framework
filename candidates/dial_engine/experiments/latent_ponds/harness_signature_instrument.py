# -*- coding: utf-8 -*-
"""
P-L4 HARNESS-SIGNATURE INSTRUMENT (latent_ponds, dial-protocol).

Reads the PHYSICAL HARNESS through the LATENT OCEAN: millions of bodies in
location/language/bandwidth wrappers, read via Wikimedia hourly pageview aggregates
(agent=user). NESTED_PONDS_SKETCH.md sec 6: every split below is a WRAPPER-LAYER
reading, not demographics. Register: exploratory instrument, 0.99-not-Boolean,
dimensionless observables only across ponds (E-units), model bits counted in the
Q6 half, read-only data, NO fabrication (all series fetched + cached by
fetch_latent_ponds.py; controls are seeded synthetics, labelled, never read as data).

PRE-REGISTERED PREDICTIONS (written before any number was computed):
  P1 location-wrapper smear: circadian phase-concentration R ordering
       ja > de > ar > es > en
     (speaker-base timezone span: ja ~1 zone; de ~1; ar ~3; es ~9; en ~18).
  P2 channel-wrapper (B9 straw bandwidth regimes, Piccardi&West design change):
     desktop carries the WORK harness -> weekly/daily line-power ratio
     (f168/f24) HIGHER on desktop than mobile-web, in every pond.
  P3 rung resonance: the pond is a LINE-SPECTRUM medium (B4 institutional lines),
     so the Q6 persistence comp-ratio across rungs 1h/6h/24h/168h is NON-MONOTONE
     (dip at 6h, partial recovery at 24h) -- unlike the flare's monotone collapse.
  P4 DST micro-probe (location wrapper, falsifiable within-window): de peak-hour
     in UTC shifts ~ -1h from pre-EU-DST (Mar 1-27) to post (Apr 6-May 30);
     ja shifts ~ 0h (no DST).
  P5 canon radius: residual (event) co-movement is strongest within the Western
     shared canon (en-de-es pairs) and weaker for pairs involving ja or ar.

Avalanche-census cautions from the fresh scan (Okamura 2026 log-scaling, exponent
definition-sensitivity) belong to P-L5 and are NOT exercised here: P-L4 fits no
power law and reads no criticality dial; it reads spectral LINES, PHASE, and the
committed Q6 rung observables only. Weekly periodicity is not a confound here --
it is the second measurand. Multi-year amplitude trend (Crokidakis check) reported.
"""
import json, lzma, zlib, bz2, math, pathlib, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
UA = {"User-Agent": "agnostic-framework-research/0.1 (research instrument)"}

PONDS = ["en", "ja", "de", "ar", "es"]
PROJ = {p: f"{p}.wikipedia.org" for p in PONDS}
MAIN = ("2026030100", "2026060100")
NWEEK = 13                  # whole weeks used -> exact DFT bins
NH = NWEEK * 168            # 2184 hourly samples (91 days, Mar 1 .. May 30)
W_MA = 168                  # detrend moving-average window (zeros AT 24h & 168h lines)
TREND_YEARS = ["2019", "2021", "2023", "2025", "2026"]

# ---------------------------------------------------------------- loading
def load_hourly(proj, access, s, e):
    f = DATA / f"hourly_{proj}_{access}_{s}_{e}.json"
    items = json.loads(f.read_text(encoding="utf-8"))["items"]
    ts2v = {it["timestamp"]: it["views"] for it in items}
    # full hourly grid from s, NH hours
    t0 = time.strptime(s, "%Y%m%d%H")
    import datetime as dt
    start = dt.datetime(*t0[:4])
    grid, missing = [], 0
    for k in range(NH):
        t = start + dt.timedelta(hours=k)
        key = t.strftime("%Y%m%d%H")
        v = ts2v.get(key)
        if v is None:
            missing += 1; grid.append(np.nan)
        else:
            grid.append(max(float(v), 1.0))
    x = np.array(grid)
    if missing:
        idx = np.arange(NH); good = np.isfinite(x)
        x = np.interp(idx, idx[good], x[good])
    return x, missing

# ---------------------------------------------------------------- core observables
def ma_centered(x, w=W_MA):
    half = w // 2
    xp = np.concatenate([x[:half][::-1], x, x[-(w - half - 1):][::-1]])
    return np.convolve(xp, np.ones(w) / w, mode="valid")  # len == len(x)

def detrend_log(views):
    """log10 series minus centered MA(168). MA(168) transfer fn has zeros at
    periods 168/k h (incl. 168h and 24h): subtraction PRESERVES the lines exactly,
    removes trend/slow drift. Edge: reflect-pad (84 h each side), disclosed."""
    x = np.log10(views)
    return x - ma_centered(x)

def line_powers(d):
    """exact-bin DFT power fractions; n must be a multiple of 168."""
    n = len(d)
    assert n % 168 == 0
    F = np.fft.rfft(d - d.mean())
    P = np.abs(F) ** 2
    tot = P[1:].sum()
    b24, b168 = n // 24, n // 168
    comb24 = sum(P[k * b24] for k in (1, 2, 3, 4))     # 24h + 12/8/6h harmonics
    return dict(
        f24=float(P[b24] / tot), f168=float(P[b168] / tot),
        f24comb=float(comb24 / tot),
        weekly_over_daily=float(P[b168] / P[b24]),
        acf24=float(np.corrcoef(d[:-24], d[24:])[0, 1]),
        acf168=float(np.corrcoef(d[:-168], d[168:])[0, 1]))

def diurnal_profile(d):
    """multiplicative diurnal gain by UTC hour-of-day from detrended log series."""
    r = 10.0 ** d                       # ratio to MA baseline, ~1
    hours = np.arange(len(d)) % 24      # series starts at 00 UTC
    g = np.array([r[hours == h].mean() for h in range(24)])
    g = g / g.mean()
    z = np.sum(g * np.exp(2j * np.pi * np.arange(24) / 24.0))
    R = float(np.abs(z) / g.sum())                      # phase concentration 0..1
    peak_utc = float((np.angle(z) * 24.0 / (2 * np.pi)) % 24)
    return dict(R=R, peak_hour_utc=peak_utc,
                peak_to_trough=float(g.max() / g.min()),
                argmax_hour_utc=int(np.argmax(g)), g=[float(v) for v in g])

def pond_read(views):
    d = detrend_log(views)
    out = line_powers(d); out.update(diurnal_profile(d))
    out["mean_hourly_views"] = float(views.mean())
    return out

# ---------------------------------------------------------------- Q6 rung instrument
# EXACT committed logic from experiments/q6_scale_rung/scale_rung_instrument.py
Q = 1e-3
RUNGS_H = [1, 6, 24, 168]

def clen_bits(x, coder="lzma"):
    b = np.ascontiguousarray(np.round(x / Q).astype(np.int64)).tobytes()
    c = {"lzma": lambda: lzma.compress(b, preset=9),
         "zlib": lambda: zlib.compress(b, 9),
         "bz2":  lambda: bz2.compress(b, 9)}[coder]()
    return len(c) * 8

def coarsen(x, r, method):
    if r == 1:
        return x.copy()
    n = (len(x) // r) * r
    xx = x[:n]
    if method == "mean":
        return xx.reshape(-1, r).mean(axis=1)
    elif method == "decimate":
        return xx[::r]
    raise ValueError(method)

def rho1(x):
    return float(np.corrcoef(x[:-1], x[1:])[0, 1]) if len(x) > 2 else None

def measure(series, r, method, coder="lzma"):
    x = coarsen(series, r, method)
    if len(x) < 8:
        return None
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    raw_b = clen_bits(x, coder); res_b = clen_bits(resid, coder)
    model_b = 64
    sig_raw = float(np.std(x)); sig_res = float(np.std(resid))
    rr = rho1(x)
    return dict(rung_h=r, method=method, coder=coder, n=len(x),
                comp_ratio=raw_b / (res_b + model_b),
                sigma_shrink_bits=(math.log2(sig_raw / sig_res) if sig_res > 0 else None),
                rho1=rr,
                shrink_pred_identity=(-0.5 * math.log2(2 * (1 - rr))
                                      if rr is not None and rr < 1 else None),
                raw_bits=raw_b, resid_bits=res_b)

def q6_block(en_views):
    x = np.log10(en_views)                      # same convention as flare log10 flux
    rng = np.random.default_rng(0)              # committed control seed
    noise = rng.normal(0, x.std(), size=len(x))
    ar1 = np.empty(len(x)); ar1[0] = 0.0
    for t in range(1, len(x)):
        ar1[t] = 0.9 * ar1[t - 1] + rng.normal(0, 1)
    ar1 *= x.std() / ar1.std()
    series = {"en_pond_REAL": x, "noise_CONTROL_iid": noise, "ar1_CONTROL_memory": ar1}
    out = {}
    for name, s in series.items():
        out[name] = {}
        for method in ("mean", "decimate"):
            rows = []
            for r in RUNGS_H:
                row = measure(s, r, method, "lzma")
                if row:
                    for sib in ("zlib", "bz2"):
                        row[f"comp_{sib}"] = measure(s, r, method, sib)["comp_ratio"]
                    rows.append(row)
            out[name][method] = rows
    # full-series lag-rho estimates (better-sampled than decimated rho1)
    out["en_full_lag_rho"] = {f"{L}h": float(np.corrcoef(x[:-L], x[L:])[0, 1])
                              for L in RUNGS_H if L < len(x) // 3}
    return out

# ---------------------------------------------------------------- canon radius
def canon_block(daily):                          # daily: dict pond -> 91-vector
    import datetime as dt
    d0 = dt.date(2026, 3, 1)
    nd = len(next(iter(daily.values())))
    dow = np.array([(d0 + dt.timedelta(days=i)).weekday() for i in range(nd)])
    logs = {p: np.log10(v) for p, v in daily.items()}
    resid = {}
    for p, x in logs.items():
        t = np.arange(nd)
        # remove linear trend + day-of-week means (log domain)
        A = np.c_[np.ones(nd), t]
        x1 = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]
        for w in range(7):
            x1[dow == w] -= x1[dow == w].mean()
        resid[p] = x1 / x1.std()
    def cmat(dd):
        M = np.zeros((len(PONDS), len(PONDS)))
        for i, a in enumerate(PONDS):
            for j, b in enumerate(PONDS):
                M[i, j] = np.corrcoef(dd[a], dd[b])[0, 1]
        return M
    raw_m, res_m = cmat(logs), cmat(resid)
    # co-spike census
    Z = np.vstack([resid[p] for p in PONDS])     # 5 x nd
    events = []
    for i in range(nd):
        hot = [PONDS[k] for k in range(5) if Z[k, i] > 2.0]
        if hot:
            events.append(dict(date=str(d0 + dt.timedelta(days=i)), langs=hot,
                               z={PONDS[k]: round(float(Z[k, i]), 2) for k in range(5)
                                  if Z[k, i] > 1.0}))
    global_ev = [e for e in events if len(e["langs"]) >= 3]
    local_ev = [e for e in events if len(e["langs"]) == 1
                and max(e["z"].values()) > 2.5]
    return dict(raw_corr=raw_m.round(3).tolist(), resid_corr=res_m.round(3).tolist(),
                ponds=PONDS, global_events=global_ev, local_events=local_ev)

def fetch_top(proj, y, m, d):
    import requests
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
        time.sleep(25 * (attempt + 1))
    return None

def name_event(date_str):
    y, m, d = date_str.split("-")
    named = {}
    for p in PONDS:
        j = fetch_top(PROJ[p], y, m, d)
        if not j:
            named[p] = None; continue
        arts = j["items"][0]["articles"]
        skip = ("Main_Page", "メインページ", "Wikipedia:Hauptseite",
                "Wikipedia:Portada", "الصفحة_الرئيسية")
        top = [a["article"] for a in arts
               if a["article"] not in skip and ":" not in a["article"]][:3]
        named[p] = top
    return named

# ---------------------------------------------------------------- main
def main():
    results = {"probe": "P-L4 harness-signature v0.1",
               "window": "2026-03-01T00Z .. +2184h (13 whole weeks)",
               "detrend": f"log10 minus centered MA({W_MA}h), reflect-padded",
               "agent": "user", "n_hours": NH}

    # ---- per-pond, per-access wrapper readings (main window)
    per = {}
    missing_tot = {}
    for p in PONDS:
        per[p] = {}
        for access in ("all-access", "desktop", "mobile-web"):
            v, miss = load_hourly(PROJ[p], access, *MAIN)
            per[p][access] = pond_read(v)
            missing_tot[f"{p}/{access}"] = miss
    results["per_pond"] = per
    results["missing_hours"] = missing_tot

    # bandwidth wrapper: relative volume shares + straw composition
    tot = sum(per[p]["all-access"]["mean_hourly_views"] for p in PONDS)
    results["volume_share"] = {p: round(per[p]["all-access"]["mean_hourly_views"] / tot, 4)
                               for p in PONDS}
    results["mobile_share"] = {p: round(per[p]["mobile-web"]["mean_hourly_views"] /
                                        per[p]["all-access"]["mean_hourly_views"], 4)
                               for p in PONDS}

    # ---- P4 DST micro-probe (sub-window phases, all-access)
    dst = {}
    for p in ("de", "ja", "en"):
        v, _ = load_hourly(PROJ[p], "all-access", *MAIN)
        pre = diurnal_profile(detrend_log(v[:27 * 24]))           # Mar 1-27 (pre EU DST)
        post = diurnal_profile(detrend_log(v[36 * 24:91 * 24]))   # Apr 6 - May 30
        dphi = ((post["peak_hour_utc"] - pre["peak_hour_utc"] + 12) % 24) - 12
        dst[p] = dict(pre_peak_utc=round(pre["peak_hour_utc"], 2),
                      post_peak_utc=round(post["peak_hour_utc"], 2),
                      shift_h=round(dphi, 2))
    results["dst_micro_probe"] = dst

    # ---- canon radius (daily totals, all-access)
    daily = {}
    for p in PONDS:
        v, _ = load_hourly(PROJ[p], "all-access", *MAIN)
        daily[p] = v[:91 * 24].reshape(91, 24).sum(axis=1)
    results["canon"] = canon_block(daily)
    if results["canon"]["global_events"]:
        big = max(results["canon"]["global_events"],
                  key=lambda e: sum(e["z"].values()))
        results["canon"]["top_global_event_named"] = {
            "date": big["date"], "top_articles": name_event(big["date"])}

    # ---- Q6 rung instrument on en pond
    v_en, _ = load_hourly(PROJ["en"], "all-access", *MAIN)
    results["q6_rungs_en"] = q6_block(v_en)

    # ---- multi-year circadian amplitude trend (Crokidakis check), en + ja
    trend = {}
    for p in ("en", "ja"):
        trend[p] = {}
        for y in TREND_YEARS:
            try:
                v, miss = load_hourly(PROJ[p], "all-access", f"{y}030100", f"{y}060100")
            except FileNotFoundError:
                trend[p][y] = "NOT_FETCHED_YET"; continue
            r = pond_read(v)
            trend[p][y] = dict(R=round(r["R"], 4), f24=round(r["f24"], 4),
                               f168=round(r["f168"], 5),
                               peak_to_trough=round(r["peak_to_trough"], 3),
                               peak_hour_utc=round(r["peak_hour_utc"], 2),
                               missing_hours=miss)
    results["amplitude_trend"] = trend

    out = HERE / "latent_ponds_results.json"
    out.write_text(json.dumps(results, indent=1), encoding="utf-8")

    # ------------- console summary
    print("=== P-L4 HARNESS SIGNATURE (13 whole weeks from 2026-03-01, agent=user) ===")
    print(f"{'pond':4} {'R':>6} {'peakUTC':>8} {'p2t':>6} {'f24':>7} {'f168':>8} "
          f"{'acf24':>6} {'acf168':>7}  (all-access)")
    for p in PONDS:
        r = per[p]["all-access"]
        print(f"{p:4} {r['R']:6.3f} {r['peak_hour_utc']:8.2f} {r['peak_to_trough']:6.2f} "
              f"{r['f24']:7.4f} {r['f168']:8.5f} {r['acf24']:6.3f} {r['acf168']:7.3f}")
    print("\nP2 channel split  weekly/daily power ratio f168/f24:")
    for p in PONDS:
        dsk = per[p]["desktop"]; mob = per[p]["mobile-web"]
        print(f"{p:4} desktop {dsk['weekly_over_daily']:8.4f}  R={dsk['R']:.3f} "
              f"peak={dsk['peak_hour_utc']:5.2f} | mobile-web {mob['weekly_over_daily']:8.4f} "
              f" R={mob['R']:.3f} peak={mob['peak_hour_utc']:5.2f}")
    print("\nP4 DST:", json.dumps(dst))
    print("\ncanon raw corr:", results["canon"]["raw_corr"])
    print("canon resid corr:", results["canon"]["resid_corr"])
    print("global events:", len(results["canon"]["global_events"]),
          "| local events:", len(results["canon"]["local_events"]))
    print("\nQ6 rungs (en, lzma, decimate): ",
          [(r["rung_h"], round(r["comp_ratio"], 3), round(r["rho1"], 3))
           for r in results["q6_rungs_en"]["en_pond_REAL"]["decimate"]])
    print("Q6 rungs (en, lzma, mean):     ",
          [(r["rung_h"], round(r["comp_ratio"], 3), round(r["rho1"], 3))
           for r in results["q6_rungs_en"]["en_pond_REAL"]["mean"]])
    print("full-series lag rho:", results["q6_rungs_en"]["en_full_lag_rho"])
    print("\ntrend:", json.dumps(trend, indent=0))
    print("\nsaved ->", out)

if __name__ == "__main__":
    main()
