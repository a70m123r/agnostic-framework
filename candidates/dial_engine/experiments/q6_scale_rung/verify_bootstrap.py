# -*- coding: utf-8 -*-
"""
Q6 SCALE-RUNG -- SIGNIFICANCE / ERROR-BARS verification.

Block-bootstrap the 1-min log-flux, recompute the persistence-law comp-ratio per rung
per resample, report mean +/- 95% CI per rung. Tests:
  (1) Is 1-min comp-ratio (~1.27) significantly above 1.0?
  (2) Is the decay to ~0.95 significantly below the 1-min value? (paired diff rung1-rungK)
  (3) Does the coarse-rung flare fall INTO the iid-noise floor band? (overlap test)
  (4) Which adjacent-rung differences are REAL (CI excludes 0)?
Accounts for n-shrinkage (n: 10078 -> 167 at 60-min) -- the bootstrap CIs widen naturally.

Method pins identical to scale_rung_instrument.py: persistence law, lzma-9, Q=1e-3,
comp_ratio = raw_bits / (resid_bits + 64). Flare is REAL GOES; noise/ar1 are seeded
synthetic CONTROLS regenerated fresh per replicate for the floor band.
"""
import json, lzma, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
GOES = HERE / "../../../cosmic_coin_probe/probe_data/goes_xray_7day.json"
Q = 1e-3
RUNGS = [1, 2, 5, 10, 30, 60]
MODEL_B = 64

# ---- method pins (identical to instrument) ---------------------------------
def clen_bits(x):
    b = np.ascontiguousarray(np.round(x / Q).astype(np.int64)).tobytes()
    return len(lzma.compress(b, preset=9)) * 8

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

def comp_ratio(series, r, method):
    x = coarsen(series, r, method)
    if len(x) < 8:
        return np.nan
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    return clen_bits(x) / (clen_bits(resid) + MODEL_B)

def load_flare():
    rows = json.loads(pathlib.Path(GOES).read_text(encoding="utf-8"))
    longb = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    longb.sort(key=lambda r: r["time_tag"])
    flux = np.clip(np.array([r["flux"] for r in longb], float), 1e-9, None)
    return np.log10(flux[np.isfinite(flux)])

# ---- moving block bootstrap -------------------------------------------------
def mbb(x, L, rng):
    """moving block bootstrap WITH replacement to same length."""
    n = len(x)
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, n - L + 1, size=nb)
    return np.concatenate([x[s:s+L] for s in starts])[:n]

def pct(a, q):
    return float(np.nanpercentile(a, q))

def summarize(mat, rungs):
    """mat: (B, nrung). return per-rung dict."""
    out = {}
    for j, r in enumerate(rungs):
        col = mat[:, j]
        out[r] = dict(mean=float(np.nanmean(col)), sd=float(np.nanstd(col)),
                      lo=pct(col, 2.5), med=pct(col, 50), hi=pct(col, 97.5))
    return out

def main():
    flare = load_flare()
    n = len(flare)
    sd_flare = flare.std()
    print(f"flare: n={n}  log10-flux std={sd_flare:.4f}  range[{flare.min():.3f},{flare.max():.3f}]")

    # ---- 0) reproduce instrument point estimates (sanity that pipeline matches JSON) ----
    print("\n[REPRODUCE point estimates -- must match scale_rung_results.json]")
    for method in ("mean", "decimate"):
        pe = [comp_ratio(flare, r, method) for r in RUNGS]
        print(f"  flare {method:8s}: " + "  ".join(f"{v:5.3f}" for v in pe))

    B = 400
    Lmain = 120
    rng = np.random.default_rng(12345)

    # ---- 1) MBB on the flare, full rung curve per replicate (both methods) ----
    print(f"\n[BOOTSTRAP] moving-block, L={Lmain} min, B={B} replicates, seed=12345")
    boot = {m: np.full((B, len(RUNGS)), np.nan) for m in ("mean", "decimate")}
    for bi in range(B):
        xb = mbb(flare, Lmain, rng)
        for m in ("mean", "decimate"):
            for j, r in enumerate(RUNGS):
                boot[m][bi, j] = comp_ratio(xb, r, m)

    # ---- 2) noise + ar1 floor bands: regenerate fresh per replicate ----
    rng2 = np.random.default_rng(777)
    noise_mat = {m: np.full((B, len(RUNGS)), np.nan) for m in ("mean", "decimate")}
    ar1_mat   = {m: np.full((B, len(RUNGS)), np.nan) for m in ("mean", "decimate")}
    a = 0.9
    for bi in range(B):
        noise = rng2.normal(0, sd_flare, size=n)
        ar1 = np.empty(n); ar1[0] = 0.0
        eps = rng2.normal(0, 1, size=n)
        for t in range(1, n):
            ar1[t] = a*ar1[t-1] + eps[t]
        ar1 *= sd_flare / ar1.std()
        for m in ("mean", "decimate"):
            for j, r in enumerate(RUNGS):
                noise_mat[m][bi, j] = comp_ratio(noise, r, m)
                ar1_mat[m][bi, j]   = comp_ratio(ar1, r, m)

    # ---- report ----
    for method in ("decimate", "mean"):
        S = summarize(boot[method], RUNGS)
        Snz = summarize(noise_mat[method], RUNGS)
        Sar = summarize(ar1_mat[method], RUNGS)
        tag = "  <== CLAIM-BEARING" if method == "decimate" else ""
        print(f"\n================ FLARE  method={method} {tag} ================")
        print("rung |  flare mean  [95% CI]        |  >1.0? | noise floor [95% CI]      | ar1 [95% CI]        | flare-vs-noise overlap?")
        for r in RUNGS:
            f, nz, ar = S[r], Snz[r], Sar[r]
            above1 = "YES" if f["lo"] > 1.0 else ("no " if f["hi"] < 1.0 else "~1 ")
            overlap = "OVERLAP" if (f["lo"] <= nz["hi"] and nz["lo"] <= f["hi"]) else "separate"
            print(f"{r:4d} |  {f['mean']:.3f} [{f['lo']:.3f},{f['hi']:.3f}]  "
                  f"| {above1}    | {nz['mean']:.3f} [{nz['lo']:.3f},{nz['hi']:.3f}] "
                  f"| {ar['mean']:.3f} [{ar['lo']:.3f},{ar['hi']:.3f}] | {overlap}")

        # paired differences rung1 - rungK (within-replicate, accounts for correlation)
        print(f"  -- paired decay  cr(rung1) - cr(rungK), within-replicate 95% CI (excludes 0 => REAL decay):")
        d1 = boot[method][:, 0]
        for j, r in enumerate(RUNGS[1:], start=1):
            diff = d1 - boot[method][:, j]
            lo, hi, md = pct(diff, 2.5), pct(diff, 97.5), pct(diff, 50)
            real = "REAL (excl 0)" if lo > 0 else ("REAL- (excl 0)" if hi < 0 else "n.s. (incl 0)")
            print(f"     rung1 - rung{r:<2d}: {md:+.3f} [{lo:+.3f},{hi:+.3f}]  {real}")

        # adjacent-rung differences
        print(f"  -- adjacent-rung diffs cr(prev)-cr(next), 95% CI (which single steps are real):")
        for j in range(1, len(RUNGS)):
            diff = boot[method][:, j-1] - boot[method][:, j]
            lo, hi, md = pct(diff, 2.5), pct(diff, 97.5), pct(diff, 50)
            real = "REAL" if (lo > 0 or hi < 0) else "n.s."
            print(f"     rung{RUNGS[j-1]:<2d}->rung{RUNGS[j]:<2d}: {md:+.3f} [{lo:+.3f},{hi:+.3f}]  {real}")

    # ---- 3) block-length sensitivity (decimate, rung1 & rung60 & key diffs) ----
    print("\n[BLOCK-LENGTH SENSITIVITY] decimate; rung1 CI, rung60 CI, (rung1-rung10) diff CI")
    for L in (60, 120, 300, 600):
        rngL = np.random.default_rng(999)
        m1 = np.full(B, np.nan); m60 = np.full(B, np.nan); d10 = np.full(B, np.nan)
        for bi in range(B):
            xb = mbb(flare, L, rngL)
            c1 = comp_ratio(xb, 1, "decimate")
            c10 = comp_ratio(xb, 10, "decimate")
            c60 = comp_ratio(xb, 60, "decimate")
            m1[bi], m60[bi], d10[bi] = c1, c60, c1 - c10
        print(f"  L={L:4d}: rung1={np.nanmean(m1):.3f}[{pct(m1,2.5):.3f},{pct(m1,97.5):.3f}]  "
              f"rung60={np.nanmean(m60):.3f}[{pct(m60,2.5):.3f},{pct(m60,97.5):.3f}]  "
              f"(r1-r10)={np.nanmean(d10):+.3f}[{pct(d10,2.5):+.3f},{pct(d10,97.5):+.3f}]")

    # ---- 4) robustness: block PERMUTATION (no replacement -> no duplicate-block lzma artifact) ----
    print("\n[ROBUSTNESS] block PERMUTATION (no-replacement) vs MBB, decimate rung1 (checks lzma duplicate-block artifact)")
    rngp = np.random.default_rng(2024)
    Lp = 120
    nb = n // Lp
    base = flare[:nb*Lp].reshape(nb, Lp)
    permvals = np.full(B, np.nan)
    for bi in range(B):
        order = rngp.permutation(nb)
        xb = base[order].reshape(-1)
        permvals[bi] = comp_ratio(xb, 1, "decimate")
    print(f"  permutation rung1 (decimate): {np.nanmean(permvals):.3f} [{pct(permvals,2.5):.3f},{pct(permvals,97.5):.3f}]")
    print(f"  (compare MBB rung1 decimate above; similar => duplicate-block artifact NOT driving the CI)")

if __name__ == "__main__":
    main()
