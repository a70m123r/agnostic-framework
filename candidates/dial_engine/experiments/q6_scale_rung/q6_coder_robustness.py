# -*- coding: utf-8 -*-
"""
Q6 CODER-AND-SHRINK ROBUSTNESS CHECK (external-pass angle on scale_rung_instrument.py).

Recomputes the comp-ratio-vs-rung curves under zlib-9 and bz2-9 (not just lzma-9),
and adds the CODER-FREE dimensionless sigma-shrink view log2(sig_raw/sig_resid) vs
rung, plus the lag-1 autocorrelation each rung actually has (the quantity the
persistence law exploits: sigma_shrink = -0.5*log2(2*(1-rho1)) under stationarity).

Verifies, per coder:
  (a) flare fine-scale edge at rung 1 (committed lzma value: 1.27x) and decay to the
      iid-noise floor by rung 10-60, under BOTH mean and decimate coarsening;
  (b) the ORDERING flare > ar1 > noise at rung 1, and convergence of flare into the
      noise-floor band at coarse rungs.

Pins are identical to scale_rung_instrument.py: persistence law f_hat(t)=f(t-1) on the
log10 series, quant Q=1e-3, model_b=64, rungs [1,2,5,10,30,60], controls seeded
(default_rng(0), AR(1) a=0.9). flare is the real committed GOES week; noise/ar1 are
clearly-labelled synthetic CONTROLS. Also asserts my lzma run reproduces the committed
scale_rung_results.json bit-for-bit (raw_bits/resid_bits).
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
GOES = HERE / "../../../cosmic_coin_probe/probe_data/goes_xray_7day.json"
Q = 1e-3
RUNGS = [1, 2, 5, 10, 30, 60]
CODERS = ["lzma", "zlib", "bz2"]


def clen_bits(x, coder):
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


def measure(series, r, method, coder):
    x = coarsen(series, r, method)
    if len(x) < 8:
        return None
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    raw_b = clen_bits(x, coder); res_b = clen_bits(resid, coder)
    model_b = 64
    sig_raw = float(np.std(x)); sig_res = float(np.std(resid))
    rho1 = float(np.corrcoef(x[1:], x[:-1])[0, 1])  # coder-free memory at this rung
    return dict(rung=r, method=method, coder=coder, n=len(x),
                comp_ratio=raw_b / (res_b + model_b),
                sigma_shrink_bits=(math.log2(sig_raw / sig_res) if sig_res > 0 else None),
                rho1=rho1, raw_bits=raw_b, resid_bits=res_b)


def load_flare():
    rows = json.loads(pathlib.Path(GOES).read_text(encoding="utf-8"))
    longb = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    longb.sort(key=lambda r: r["time_tag"])
    flux = np.clip(np.array([r["flux"] for r in longb], float), 1e-9, None)
    return np.log10(flux[np.isfinite(flux)])


def main():
    flare = load_flare()
    n = len(flare)
    rng = np.random.default_rng(0)
    noise = rng.normal(0, flare.std(), size=n)
    ar1 = np.empty(n); ar1[0] = 0.0
    a = 0.9
    for t in range(1, n):
        ar1[t] = a * ar1[t - 1] + rng.normal(0, 1)
    ar1 *= flare.std() / ar1.std()
    series = {"flare_REAL": flare, "noise_CONTROL_iid": noise, "ar1_CONTROL_memory": ar1}

    out = {"probe": "q6_coder_robustness v0.1", "coders": [c + "-9" for c in CODERS],
           "quant": Q, "rungs": RUNGS, "n_base": n, "law": "persistence",
           "note": "external-pass robustness on q6_scale_rung: same pins, 3 coders + "
                   "coder-free sigma-shrink/rho1; controls seeded synthetic; flare real GOES.",
           "curves": {}}
    for name, s in series.items():
        out["curves"][name] = {}
        for method in ("mean", "decimate"):
            out["curves"][name][method] = {}
            for coder in CODERS:
                rows = [measure(s, r, method, coder) for r in RUNGS]
                out["curves"][name][method][coder] = [r for r in rows if r]

    # --- 0) reproduce committed lzma run bit-for-bit ---
    committed = json.loads((HERE / "scale_rung_results.json").read_text(encoding="utf-8"))
    mismatches = 0
    for name in series:
        for method in ("mean", "decimate"):
            for old, new in zip(committed["curves"][name][method],
                                out["curves"][name][method]["lzma"]):
                for k in ("raw_bits", "resid_bits", "n"):
                    if old[k] != new[k]:
                        mismatches += 1
                        print(f"MISMATCH {name}/{method}/r{old['rung']}/{k}: "
                              f"committed {old[k]} vs rerun {new[k]}")
    print(f"[repro] committed-lzma bit-for-bit mismatches: {mismatches} "
          f"({'OK — exact reproduction' if mismatches == 0 else 'DRIFT'})\n")

    # --- 1) comp-ratio vs rung per coder ---
    for coder in CODERS:
        print(f"=== comp_ratio raw/(resid+64b)  [{coder}-9] ===")
        print("rung(min):                      " + "  ".join(f"{r:>5}" for r in RUNGS))
        for name in series:
            for method in ("mean", "decimate"):
                cr = {row["rung"]: row["comp_ratio"] for row in out["curves"][name][method][coder]}
                print(f"  {name:20s} {method:8s}: " +
                      "  ".join(f"{cr.get(r, float('nan')):5.3f}" for r in RUNGS))
        print()

    # --- 2) coder-free sigma-shrink + rho1 vs rung ---
    print("=== CODER-FREE sigma_shrink_bits = log2(sig_raw/sig_resid)  (iid floor = -0.5) ===")
    print("rung(min):                      " + "  ".join(f"{r:>6}" for r in RUNGS))
    for name in series:
        for method in ("mean", "decimate"):
            ss = {row["rung"]: row["sigma_shrink_bits"] for row in out["curves"][name][method]["lzma"]}
            print(f"  {name:20s} {method:8s}: " +
                  "  ".join(f"{ss.get(r, float('nan')):6.3f}" for r in RUNGS))
    print()
    print("=== lag-1 autocorrelation rho1 at each rung (memory the law exploits; iid = 0) ===")
    print("rung(min):                      " + "  ".join(f"{r:>6}" for r in RUNGS))
    for name in series:
        for method in ("mean", "decimate"):
            rh = {row["rung"]: row["rho1"] for row in out["curves"][name][method]["lzma"]}
            print(f"  {name:20s} {method:8s}: " +
                  "  ".join(f"{rh.get(r, float('nan')):6.3f}" for r in RUNGS))
    print()

    # --- 3) ordering + floor-convergence verdicts per coder ---
    print("=== ORDERING / FLOOR CHECKS per coder (decimate = claim-bearing column) ===")
    for coder in CODERS:
        g = lambda name, method, r: next(row["comp_ratio"]
                                         for row in out["curves"][name][method][coder]
                                         if row["rung"] == r)
        f1 = g("flare_REAL", "decimate", 1)
        a1 = g("ar1_CONTROL_memory", "decimate", 1)
        n1 = g("noise_CONTROL_iid", "decimate", 1)
        noise_vals = [row["comp_ratio"] for m in ("mean", "decimate")
                      for row in out["curves"]["noise_CONTROL_iid"][m][coder]]
        lo, hi = min(noise_vals), max(noise_vals)
        coarse = {m: [g("flare_REAL", m, r) for r in (10, 30, 60)] for m in ("mean", "decimate")}
        in_band = {m: [lo - 0.02 <= v <= hi + 0.02 for v in coarse[m]] for m in coarse}
        print(f"[{coder}-9] rung1: flare {f1:.3f}  ar1 {a1:.3f}  noise {n1:.3f}  "
              f"-> ordering flare>ar1>noise: {f1 > a1 > n1}")
        print(f"          noise floor band (all rungs/methods): [{lo:.3f}, {hi:.3f}]")
        for m in ("mean", "decimate"):
            print(f"          flare {m:8s} @10/30/60min: "
                  + "  ".join(f"{v:.3f}" for v in coarse[m])
                  + f"   within band(+/-0.02): {all(in_band[m])}")
        print()

    (HERE / "q6_coder_robustness_results.json").write_text(json.dumps(out, indent=2),
                                                           encoding="utf-8")
    print("wrote q6_coder_robustness_results.json")


if __name__ == "__main__":
    main()
