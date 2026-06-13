# S1 SYNERGY GATE — gain_v2-disciplined joint-vs-proper-additive duel on real GRACE-FO density
# RESULTS RAN AND SAVED: synergy_gate_results.json (runtime 9.2 s)
# Register: exploratory instrument, 0.99-not-Boolean, NO fabrication (real fetched data only),
# model bits counted, held-out by time blocks, engine BANDS not headlines.
#
# Question: does the JOINT law density|(F10.7, Dst) compress held-out data more than a PROPER
# ADDITIVE baseline f(F107)+g(Dst) fit by JOINT least squares (= backfit for linear smoothers),
# beyond model-bit cost and a permutation noise floor?  Plus the FRAME FLIP: driver dominance
# (held-out bits each marginal buys) quiet flanks vs the Gannon storm week.
#
# Disclosed engine pins:
#   target        : log10(rho_orbit_kgm3)  (orbit-average channel, per DATA seat normalization)
#   base covariate: scaled mean altitude in EVERY model incl. null (confound control, disclosed)
#   F107 transform: log10(min(F107, 300 sfu))  (cap per scout: 412.9 sfu radio-burst outlier)
#   quantization  : Q = 1e-3 dex on log10-density residuals (q6 convention)
#   model bits    : 32 bits/parameter (coefs + intercept + sigma) x 2 parity fits
#   holdout       : alternate calendar weeks (week = floor(days since 2024-03-01 / 7)),
#                   CROSS-FITTED: each hour scored by the parity model that never saw its week
#   scoring       : (a) Gaussian NLL bits on held-out residuals (train-fit sigma) + quant offset
#                   (b) lzma-9 coding of the quantized cross-fitted residual stream
#   noise floor   : K circular shifts of the Dst series (preserves autocorr, kills alignment),
#                   full refit of additive+joint per shift -> spurious-synergy (DoF) floor
#   bands         : lag budget {S,M,L} x model family {lin, quad}  (quad = misspecification guard)
import numpy as np, pandas as pd, lzma, json, time

t0 = time.time()
rng = np.random.default_rng(0)
DATA = r"D:\PlatformOperator\research\pav\candidates\dial_engine\experiments\s1_drag_synergy\data\s1_aligned_hourly.csv"
OUT  = r"D:\PlatformOperator\research\pav\candidates\dial_engine\experiments\s1_drag_synergy\synergy_gate_results.json"

Q_DEX = 1e-3
BITS_PER_PARAM = 32.0
RIDGE = 1e-3
QUANT_OFFSET = np.log2(1.0 / Q_DEX)          # 9.9658 bits/h, constant across models
N_PERM = 30
N_BOOT = 1000
BOOT_BLOCK = 72                               # h, moving-block bootstrap

df = pd.read_csv(DATA)
n = len(df)
tt = pd.to_datetime(df["datetime_utc"], utc=True)
y_raw = df["rho_orbit_kgm3"].to_numpy(float)
y = np.where(y_raw > 0, np.log10(np.where(y_raw > 0, y_raw, 1.0)), np.nan)
alt_s = (df["alt_mean_m"].to_numpy(float) - 490e3) / 1e4
f107 = df["f107_sfu"].to_numpy(float)
f81  = df["f107_81d_sfu"].to_numpy(float)
dst  = df["dst_nt"].to_numpy(float)

f107c = np.log10(np.minimum(f107, 300.0))
f81c  = np.log10(f81)
FC0   = np.log10(180.0)                       # fixed disclosed center for cross/quad terms
fc_dev = f107c - FC0

hour_idx = np.arange(n)
day_idx = hour_idx // 24
week = day_idx // 7
parity = week % 2

def lag(x, h):
    out = np.full(n, np.nan)
    if h == 0:
        return x.astype(float).copy()
    out[h:] = x[:-h]
    return out

CFGS = {
    "L-small": {"f_days": [0, 1],       "d_hours": [0, 6, 24]},
    "L-med":   {"f_days": [0, 1, 2],    "d_hours": [0, 3, 6, 12, 24]},
    "L-large": {"f_days": [0, 1, 2, 3], "d_hours": [0, 3, 6, 9, 12, 18, 24, 48]},
}
MAX_LAG = 72                                  # common valid mask across all cells
valid = (hour_idx >= MAX_LAG) & np.isfinite(y)
n_valid = int(valid.sum())

def blocks(dst_series, cfg, family):
    """Raw (unstandardized) feature blocks F, G, X built from a given dst series."""
    F = [lag(f107c, 24 * d) for d in cfg["f_days"]] + [f81c.copy()]
    G = [lag(dst_series / 100.0, h) for h in cfg["d_hours"]]
    if family == "quad":
        F += [lag(fc_dev, 24 * d) ** 2 for d in cfg["f_days"]]
        G += [lag(dst_series / 100.0, h) ** 2 for h in cfg["d_hours"]]
    X = [fc_dev * lag(dst_series / 100.0, h) for h in cfg["d_hours"]]
    return (np.column_stack(F), np.column_stack(G), np.column_stack(X))

def ridge_fit_predict(Xtr, ytr, Xte):
    mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0); sd[sd == 0] = 1.0
    Xs, Xts = (Xtr - mu) / sd, (Xte - mu) / sd
    ym = ytr.mean(); yc = ytr - ym
    p = Xs.shape[1]
    beta = np.linalg.solve(Xs.T @ Xs + RIDGE * np.eye(p), Xs.T @ yc)
    rtr = yc - Xs @ beta
    sigma = max(float(np.sqrt(np.mean(rtr ** 2))), 1e-6)
    return ym + Xts @ beta, sigma

def crossfit(feature_cols):
    """feature_cols: list of column blocks (or None) appended to [alt]. Returns per-hour
    held-out NLL bits (on valid hours, time order), residuals, n_params."""
    cols = [alt_s.reshape(-1, 1)] + [c for c in feature_cols if c is not None]
    Xall = np.column_stack(cols)
    bits = np.full(n, np.nan); resid = np.full(n, np.nan)
    for p_test in (0, 1):
        tr = valid & (parity != p_test); te = valid & (parity == p_test)
        pred, sigma = ridge_fit_predict(Xall[tr], y[tr], Xall[te])
        r = y[te] - pred
        resid[te] = r
        bits[te] = 0.5 * np.log2(2 * np.pi * sigma ** 2) + (r ** 2) / (2 * sigma ** 2 * np.log(2)) + QUANT_OFFSET
    n_params = Xall.shape[1] + 1 + 1          # features + intercept + sigma
    return bits[valid], resid[valid], n_params

def lzma_bits(resid_valid):
    q = np.clip(np.round(resid_valid / Q_DEX), -32000, 32000).astype(np.int16)
    return 8.0 * len(lzma.compress(q.tobytes(), preset=9))

def model_bits(n_params):
    return BITS_PER_PARAM * n_params * 2      # two parity fits transmitted

def run_cell(cfg, family, dst_series=dst):
    F, G, X = blocks(dst_series, cfg, family)
    out = {}
    for name, cols in [("null", []), ("mF107", [F]), ("mDst", [G]),
                       ("additive", [F, G]), ("joint", [F, G, X])]:
        b, r, npar = crossfit(cols)
        mb = model_bits(npar)
        out[name] = {"nll_bits": float(b.sum() + mb), "nll_bits_data": float(b.sum()),
                     "lzma_bits": float(lzma_bits(r) + mb), "model_bits": float(mb),
                     "n_params_per_fit": int(npar), "bits_per_h": float(b.mean() + mb / n_valid),
                     "_b": b, "_r": r}
    return out

def perm_floor(cfg, family, K=N_PERM):
    """Circular-shift Dst, refit additive+joint, spurious synergy delta distribution."""
    d_nll, d_lz = [], []
    shifts = rng.integers(336, n - 336, size=K)
    for s in shifts:
        dsh = np.roll(dst, int(s))
        F, G, X = blocks(dsh, cfg, family)
        ba, ra, npa = crossfit([F, G]); bj, rj, npj = crossfit([F, G, X])
        d_nll.append((ba.sum() + model_bits(npa)) - (bj.sum() + model_bits(npj)))
        d_lz.append((lzma_bits(ra) + model_bits(npa)) - (lzma_bits(rj) + model_bits(npj)))
    d_nll, d_lz = np.array(d_nll), np.array(d_lz)
    return {"K": K,
            "nll": {"mean": float(d_nll.mean()), "p95": float(np.percentile(d_nll, 95)), "max": float(d_nll.max())},
            "lzma": {"mean": float(d_lz.mean()), "p95": float(np.percentile(d_lz, 95)), "max": float(d_lz.max())}}

def block_bootstrap_ci(per_h_delta, const, B=N_BOOT, L=BOOT_BLOCK):
    m = len(per_h_delta); nb = int(np.ceil(m / L)); tot = []
    for _ in range(B):
        st = rng.integers(0, m - L, size=nb)
        idx = (st[:, None] + np.arange(L)[None, :]).ravel()[:m]
        tot.append(per_h_delta[idx].sum() + const)
    return [float(np.percentile(tot, 2.5)), float(np.percentile(tot, 97.5))]

# ---------------- windows (frame dial) ----------------
t_naive = tt.dt.tz_localize(None)
storm_w = ((t_naive >= "2024-05-10") & (t_naive < "2024-05-17")).to_numpy()
disturbed = np.zeros(n, bool)
hit = np.where(dst < -100)[0]
for i in hit:
    disturbed[max(0, i - 48):i + 49] = True
quiet = ~disturbed & ~storm_w
quiet_pre  = quiet & (t_naive < "2024-05-10").to_numpy()
quiet_post = quiet & (t_naive >= "2024-05-17").to_numpy()
disturbed_other = disturbed & ~storm_w

def window_table(cell, masks):
    """Cross-fitted held-out bits each model buys vs null, per window (per-hour means)."""
    v = np.where(valid)[0]; res = {}
    for wname, m in masks.items():
        mm = m[v]; nh = int(mm.sum())
        if nh == 0: res[wname] = None; continue
        e = {"n_hours": nh}
        for nm in ("mF107", "mDst", "additive", "joint"):
            saved = (cell["null"]["_b"][mm] - cell[nm]["_b"][mm])
            e[f"saved_bits_per_h_{nm}"] = float(saved.mean())
            e[f"saved_bits_total_{nm}"] = float(saved.sum())
        e["synergy_bits_per_h"] = float((cell["additive"]["_b"][mm] - cell["joint"]["_b"][mm]).mean())
        e["dominant_marginal"] = "Dst" if e["saved_bits_per_h_mDst"] > e["saved_bits_per_h_mF107"] else "F10.7"
        res[wname] = e
    return res

def window_refit(cfg, family, mask, block_h):
    """Secondary: refit marginals INSIDE one window, cross-fitted by alternate blocks."""
    idx = np.where(mask & valid)[0]
    if len(idx) < 4 * block_h: return None
    bpar = ((idx - idx[0]) // block_h) % 2
    F, G, _ = blocks(dst, cfg, family)
    out = {"n_hours": int(len(idx))}
    for nm, cols in [("null", []), ("mF107", [F]), ("mDst", [G])]:
        Xall = np.column_stack([alt_s.reshape(-1, 1)] + cols) if cols else alt_s.reshape(-1, 1)
        bits = np.empty(len(idx))
        for p_test in (0, 1):
            tr, te = idx[bpar != p_test], idx[bpar == p_test]
            pred, sigma = ridge_fit_predict(Xall[tr], y[tr], Xall[te])
            r = y[te] - pred
            bits[bpar == p_test] = 0.5 * np.log2(2 * np.pi * sigma ** 2) + (r ** 2) / (2 * sigma ** 2 * np.log(2)) + QUANT_OFFSET
        out[nm] = float(bits.mean())
    out["saved_per_h_mF107"] = out["null"] - out["mF107"]
    out["saved_per_h_mDst"]  = out["null"] - out["mDst"]
    out["dominant_marginal"] = "Dst" if out["saved_per_h_mDst"] > out["saved_per_h_mF107"] else "F10.7"
    return out

# ---------------- run the band grid ----------------
masks = {"quiet_all": quiet, "quiet_pre": quiet_pre, "quiet_post": quiet_post,
         "storm_week_2024-05-10..16": storm_w, "disturbed_other": disturbed_other}
results = {"meta": {
    "n_hours_total": int(n), "n_valid": n_valid, "max_lag_h": MAX_LAG,
    "quant_dex": Q_DEX, "bits_per_param": BITS_PER_PARAM, "ridge": RIDGE,
    "holdout": "alternate calendar weeks, cross-fitted (both parities)",
    "storm_week_parity": int(parity[(t_naive >= "2024-05-10").to_numpy() & (t_naive < "2024-05-11").to_numpy()][0]),
    "dst_min": float(np.nanmin(dst)), "dst_min_when": str(t_naive[int(np.nanargmin(dst))]),
    "f107_max": float(np.nanmax(f107)), "rho_peak": float(np.nanmax(y_raw)),
    "window_hours": {k: int(v.sum()) for k, v in masks.items()},
}, "cells": {}}

for cname, cfg in CFGS.items():
    for fam in ("lin", "quad"):
        key = f"{cname}|{fam}"
        cell = run_cell(cfg, fam)
        d_per_h = cell["additive"]["_b"] - cell["joint"]["_b"]
        const = cell["additive"]["model_bits"] - cell["joint"]["model_bits"]
        delta_nll = cell["additive"]["nll_bits"] - cell["joint"]["nll_bits"]
        delta_lz  = cell["additive"]["lzma_bits"] - cell["joint"]["lzma_bits"]
        floor = perm_floor(cfg, fam)
        ci = block_bootstrap_ci(d_per_h, const)
        # residual autocorr disclosure
        rj = cell["joint"]["_r"]; rho1 = float(np.corrcoef(rj[:-1], rj[1:])[0, 1])
        results["cells"][key] = {
            "models": {nm: {k2: v2 for k2, v2 in cell[nm].items() if not k2.startswith("_")} for nm in cell},
            "synergy": {"delta_nll_bits": float(delta_nll), "delta_nll_ci95_blockboot": ci,
                        "delta_lzma_bits": float(delta_lz), "perm_floor": floor,
                        "delta_nll_bits_per_h": float(delta_nll / n_valid),
                        "exceeds_floor_nll": bool(delta_nll > floor["nll"]["p95"]),
                        "exceeds_floor_lzma": bool(delta_lz > floor["lzma"]["p95"])},
            "joint_resid_rho1": rho1,
            "windows": window_table(cell, masks),
        }
        print(f"[{key}] add={cell['additive']['nll_bits']:.0f}b joint={cell['joint']['nll_bits']:.0f}b "
              f"dNLL={delta_nll:+.0f} (floor p95 {floor['nll']['p95']:+.0f}) "
              f"dLZ={delta_lz:+.0f} (floor p95 {floor['lzma']['p95']:+.0f}) rho1={rho1:.3f}", flush=True)

# per-window refits (secondary), default cfg M x lin and M x quad
for fam in ("lin", "quad"):
    results[f"window_refit_L-med_{fam}"] = {
        "quiet_pre":  window_refit(CFGS["L-med"], fam, quiet_pre, 48),
        "quiet_post": window_refit(CFGS["L-med"], fam, quiet_post, 48),
        "storm_week": window_refit(CFGS["L-med"], fam, storm_w, 24),
    }

# quiet-threshold sensitivity (frame-dial wiggle): -50 nT version, default cell
dist50 = np.zeros(n, bool)
for i in np.where(dst < -50)[0]:
    dist50[max(0, i - 48):i + 49] = True
quiet50 = ~dist50 & ~storm_w
cell_m = run_cell(CFGS["L-med"], "lin")
results["quiet_minus50_sensitivity"] = window_table(
    cell_m, {"quiet50_all": quiet50, "storm_week": storm_w})

results["meta"]["runtime_s"] = round(time.time() - t0, 1)
with open(OUT, "w") as f:
    json.dump(results, f, indent=1)
print("saved", OUT, "runtime", results["meta"]["runtime_s"], "s")
