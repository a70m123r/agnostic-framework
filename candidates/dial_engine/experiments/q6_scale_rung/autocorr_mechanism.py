# -*- coding: utf-8 -*-
"""Angle: autocorrelation-mechanism. Test whether comp-ratio (persistence law) tracks
lag-1 autocorrelation at each scale-rung, and whether the flare's autocorr-vs-rung
curve matches AR(1) rho^r decay. Reuses the instrument's own functions for fidelity."""
import json, lzma, math, pathlib
import numpy as np

HERE = pathlib.Path("D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/q6_scale_rung")
GOES = HERE / "../../../cosmic_coin_probe/probe_data/goes_xray_7day.json"
Q = 1e-3
RUNGS = [1, 2, 5, 10, 30, 60]

def clen_bits(x, coder="lzma"):
    b = np.ascontiguousarray(np.round(x / Q).astype(np.int64)).tobytes()
    return len(lzma.compress(b, preset=9)) * 8

def coarsen(x, r, method):
    if r == 1: return x.copy()
    n = (len(x)//r)*r; xx = x[:n]
    if method == "mean": return xx.reshape(-1, r).mean(axis=1)
    if method == "decimate": return xx[::r]
    raise ValueError(method)

def lag1_autocorr(x):
    x = np.asarray(x, float); x = x - x.mean()
    denom = np.dot(x, x)
    if denom == 0: return float("nan")
    return float(np.dot(x[:-1], x[1:]) / denom)

def measure(series, r, method):
    x = coarsen(series, r, method)
    if len(x) < 8: return None
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    raw_b = clen_bits(x); res_b = clen_bits(resid); model_b = 64
    sig_raw = float(np.std(x)); sig_res = float(np.std(resid))
    rho = lag1_autocorr(x)
    # theoretical sigma-shrink from lag-1 autocorr: Var(resid)=2 sig^2 (1-rho)
    theo_shrink = (-0.5*math.log2(2*(1-rho))) if (rho < 1) else float("nan")
    return dict(rung=r, method=method, n=len(x),
                comp_ratio=raw_b/(res_b+model_b),
                sigma_shrink_bits=(math.log2(sig_raw/sig_res) if sig_res>0 else None),
                lag1_autocorr=rho, theo_shrink_bits=theo_shrink,
                raw_bits=raw_b, resid_bits=res_b)

def load_flare():
    rows = json.loads(pathlib.Path(GOES).read_text(encoding="utf-8"))
    longb = [r for r in rows if r.get("energy")=="0.1-0.8nm" and r.get("flux") is not None]
    longb.sort(key=lambda r: r["time_tag"])
    flux = np.clip(np.array([r["flux"] for r in longb], float), 1e-9, None)
    return np.log10(flux[np.isfinite(flux)])

flare = load_flare(); nseries = len(flare)
rng = np.random.default_rng(0)
noise = rng.normal(0, flare.std(), size=nseries)
ar1 = np.empty(nseries); ar1[0] = 0.0; a = 0.9
for t in range(1, nseries): ar1[t] = a*ar1[t-1] + rng.normal(0, 1)
ar1 *= flare.std()/ar1.std()
series = {"flare_REAL": flare, "noise_CONTROL_iid": noise, "ar1_CONTROL_memory": ar1}

print("="*96)
print("REPRODUCE instrument comp_ratio + ADD lag-1 autocorr, per rung")
print("="*96)
allrows = []
for name, s in series.items():
    for method in ("mean","decimate"):
        for r in RUNGS:
            m = measure(s, r, method)
            if m: m["series"]=name; allrows.append(m)

hdr = f"{'series':20s} {'meth':9s} " + " ".join(f"r={r:<3d}" for r in RUNGS)
def fmt_row(name, method, key, fmt="{:6.3f}"):
    d = {r["rung"]: r[key] for r in allrows if r["series"]==name and r["method"]==method}
    return f"{name:20s} {method:9s} " + " ".join(fmt.format(d.get(r, float('nan'))) for r in RUNGS)

print("\n-- comp_ratio raw/resid (should match scale_rung_results.json) --")
for name in series:
    for method in ("mean","decimate"): print(fmt_row(name, method, "comp_ratio"))
print("\n-- lag-1 autocorrelation of the coarsened series --")
for name in series:
    for method in ("mean","decimate"): print(fmt_row(name, method, "lag1_autocorr"))
print("\n-- sigma_shrink_bits  (empirical) --")
for name in series:
    for method in ("mean","decimate"): print(fmt_row(name, method, "sigma_shrink_bits"))
print("\n-- theo_shrink_bits = -0.5*log2(2(1-rho))  (predicted from autocorr alone) --")
for name in series:
    for method in ("mean","decimate"): print(fmt_row(name, method, "theo_shrink_bits"))

json.dump(allrows, open(HERE/"autocorr_mechanism_rows.json","w"), indent=2)
print("\n(wrote autocorr_mechanism_rows.json)")
