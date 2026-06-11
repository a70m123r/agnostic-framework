"""recalib_robustness.py -- confirm the corrected witness + affine-span null +
annihilation-grain r_top recover the 5 called shots ROBUSTLY across the three
pinned/sibling compressors (lzma p6 headline, zlib-9, bz2).
"""
from __future__ import annotations

import numpy as np

import mdl_synergy as mdl
from cases import CASE_NAMES, build_case

NE = 256 * 256
EBAND = [16, 12, 8, 6, 4, 3, 2]


def float_affine_resid(M, *parents):
    Mf = np.asarray(M, np.float64).ravel()
    cols = [np.asarray(p, np.float64).ravel() for p in parents]
    cols.append(np.ones_like(Mf))
    design = np.stack(cols, axis=1)
    coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
    return Mf - design @ coef


def syn_wit_star(A, B, M, b, compressor):
    rfl = float_affine_resid(M, A, B)
    step, lo = mdl._grid_step(M, b)
    if step is None:
        return 0
    codes = np.rint(rfl / step).astype(np.int64)
    codes = codes - codes.min()
    return mdl.codelength_bits(codes.astype(np.int64), compressor=compressor)


def L0(b, compressor):
    return mdl.codelength_bits(np.zeros(NE, dtype=np.int64), compressor=compressor)


for comp in ("lzma", "zlib", "bz2"):
    print(f"\n=== compressor = {comp} ===  excess over all-zeros floor (bits), r_top=2")
    print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES))
    star = {}
    for nm in CASE_NAMES:
        star[nm] = [syn_wit_star(*build_case(nm), b, comp) for b in EBAND]
    fl = [L0(b, comp) for b in EBAND]
    for k, b in enumerate(EBAND):
        print(f"  {b:>3} " + " ".join(f"{star[nm][k]-fl[k]:>9d}" for nm in CASE_NAMES))
    # verdict at r_top=2 with a floor-relative margin (require excess >= 1000 bits)
    TAU = 1000
    rtop_idx = EBAND.index(2)
    print(f"  verdict (excess>=TAU={TAU} for all b in [16..2]):")
    res = {}
    for nm in CASE_NAMES:
        ex = [star[nm][k] - fl[k] for k in range(rtop_idx + 1)]
        allok = all(e >= TAU for e in ex)
        fine_ok = ex[0] >= TAU
        rtop_ok = ex[rtop_idx] >= TAU
        if nm == "COPY":
            v = "NULL (degenerate; upstream parent-count gate)"
        elif allok:
            v = "PASS"
        elif fine_ok and not rtop_ok:
            v = "FAIL@r_top (would-pass@fine)"
        else:
            v = "FAIL"
        res[nm] = v
        print(f"     {nm:6s} -> {v}")
