# -*- coding: utf-8 -*-
"""
Q6 SCALE-RUNG INSTRUMENT (dial-protocol sweep-1 candidate).

Question: is HARDNESS scale-relative? As you coarsen the GOES flare's time cadence
(zoom out the scale-rung FRAME dial), does its compressibility rise -- i.e. does the
phenomenon that is FUZZY minute-to-minute become LAWFUL when viewed coarse? If yes,
the hardness dial and the contextual-zoom dial move together (the FINDINGS Q6 / "same
dial seen twice" conjecture).

The confound the external pass would (rightly) raise, built into the design:
coarsening by MEAN-AGGREGATION averages, which reduces variance MECHANICALLY -- so
"compression improves" could be a trivial smoothing artifact, not new lawfulness.
CONTROL: also coarsen by DECIMATION (take every r-th raw sample, NO averaging). If
compressibility still rises under decimation, the scale-relativity is REAL (not a
variance-reduction artifact). A pure-iid NOISE series is the structureless floor
(should stay ~incompressible at every rung under decimation); an AR(1) series with
known memory is the has-structure reference.

Instrument (same pins as the cosmic-coin harness): law = persistence f_hat(t)=f(t-1)
on the (log-)series; coder = lzma-9 (zlib/bz2 siblings); quant disclosed; model bits
counted; compression ratio raw/resid and per-dim sigma-shrink log2(sig_raw/sig_resid),
both DIMENSIONLESS (E-units law). NO fabrication: flare is the real committed GOES
week; noise/AR1 are clearly-labelled synthetic CONTROLS, seeded, never read as data.
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
GOES = HERE / "../../../cosmic_coin_probe/probe_data/goes_xray_7day.json"
Q = 1e-3                      # log-series quantization (dex / unit), disclosed
LOG2E = 1.0 / math.log(2.0)
RUNGS = [1, 2, 5, 10, 30, 60]   # coarsening factor (x base 1-min cadence)

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
        return xx.reshape(-1, r).mean(axis=1)       # averages -> variance-reduction confound
    elif method == "decimate":
        return xx[::r]                               # every r-th sample -> NO averaging
    raise ValueError(method)

def measure(series, r, method, coder="lzma"):
    """persistence-law compression of a 1-D series at coarsening rung r."""
    x = coarsen(series, r, method)
    if len(x) < 8:
        return None
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    raw_b = clen_bits(x, coder); res_b = clen_bits(resid, coder)
    model_b = 64
    sig_raw = float(np.std(x)); sig_res = float(np.std(resid))
    return dict(rung=r, method=method, coder=coder, n=len(x),
                comp_ratio=raw_b / (res_b + model_b),
                sigma_shrink_bits=(math.log2(sig_raw / sig_res) if sig_res > 0 else None),
                raw_bits=raw_b, resid_bits=res_b)

def load_flare():
    rows = json.loads(pathlib.Path(GOES).read_text(encoding="utf-8"))
    longb = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    longb.sort(key=lambda r: r["time_tag"])
    flux = np.clip(np.array([r["flux"] for r in longb], float), 1e-9, None)
    return np.log10(flux[np.isfinite(flux)])

def main():
    flare = load_flare()
    nseries = len(flare)
    rng = np.random.default_rng(0)
    # CONTROLS, clearly synthetic, matched length:
    noise = rng.normal(0, flare.std(), size=nseries)                 # iid: structureless floor
    ar1 = np.empty(nseries); ar1[0] = 0.0                            # known temporal memory
    a = 0.9
    for t in range(1, nseries):
        ar1[t] = a * ar1[t-1] + rng.normal(0, 1)
    ar1 *= flare.std() / ar1.std()

    series = {"flare_REAL": flare, "noise_CONTROL_iid": noise, "ar1_CONTROL_memory": ar1}
    out = {"probe": "q6_scale_rung v0.1", "coder_primary": "lzma-9", "quant": Q,
           "rungs": RUNGS, "n_base": nseries, "law": "persistence",
           "design_note": "MEAN coarsening averages (variance-reduction confound); DECIMATE does not. "
                          "Real scale-relativity = compressibility rises under DECIMATE too, and the flare "
                          "rises more than the iid-noise floor. flare is real GOES; noise/ar1 are seeded synthetic controls.",
           "curves": {}}
    for name, s in series.items():
        out["curves"][name] = {}
        for method in ("mean", "decimate"):
            rows = [measure(s, r, method) for r in RUNGS]
            out["curves"][name][method] = [r for r in rows if r]
    (HERE / "scale_rung_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # headline: compression ratio vs rung, the decimate column is the claim-bearing one
    print("Q6 SCALE-RUNG  (persistence law, lzma-9; comp-ratio raw/resid)")
    print("rung(min):        " + "  ".join(f"{r:>5}" for r in RUNGS))
    for name in series:
        for method in ("mean", "decimate"):
            cr = {row["rung"]: row["comp_ratio"] for row in out["curves"][name][method]}
            line = "  ".join(f"{cr.get(r, float('nan')):5.2f}" for r in RUNGS)
            tag = "<- claim-bearing" if (name == "flare_REAL" and method == "decimate") else ""
            print(f"  {name:20s} {method:8s}: {line}  {tag}")
    print("\nREAD: does flare_REAL/decimate RISE with rung (real scale-relativity) and beat noise/decimate (above the structureless floor)?")

if __name__ == "__main__":
    main()
