"""recalib_crossover.py -- find the child-anchored ceiling where the corrected
witness separates SYN (PASS-through) from ALLOY (FAIL-at-ceiling).

Extends the band to coarser grains (b=2,1) to locate the grain at which the
small 0.1*A*B interaction is genuinely sub-LSB (annihilated to the all-zeros
floor) while the large 0.5*A*B interaction still resolves. This tests whether
the pilot's pinned r_top=3 was simply too FINE to annihilate 0.1*A*B (the old
pedestal had masked the surviving bump).
"""
from __future__ import annotations

import numpy as np

import mdl_synergy as mdl
from cases import CASE_NAMES, PREDICTED, build_case

NE = 256 * 256
EBAND = [16, 12, 8, 6, 4, 3, 2, 1]


def float_affine_resid(M, *parents):
    Mf = np.asarray(M, np.float64).ravel()
    cols = [np.asarray(p, np.float64).ravel() for p in parents]
    cols.append(np.ones_like(Mf))
    design = np.stack(cols, axis=1)
    coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
    return Mf - design @ coef


def syn_wit_star(A, B, M, b, compressor=mdl.PINNED):
    rfl = float_affine_resid(M, A, B)
    step, lo = mdl._grid_step(M, b)
    if step is None:
        return 0
    codes = np.rint(rfl / step).astype(np.int64)
    codes = codes - codes.min()
    return mdl.codelength_bits(codes.astype(np.int64), compressor=compressor)


# all-zeros floor L0(b): codelength of a residual that is exactly affine-span
def L0(b):
    codes = np.zeros(NE, dtype=np.int64)
    return mdl.codelength_bits(codes)


print("=" * 92)
print("CORRECTED WITNESS Syn_wit* over EXTENDED band (incl coarse b=2,1)  [bits]")
print("=" * 92)
star = {nm: [syn_wit_star(*build_case(nm), b) for b in EBAND] for nm in CASE_NAMES}
floor = [L0(b) for b in EBAND]
print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES) + f" {'FLOOR':>9}")
for k, b in enumerate(EBAND):
    print(f"  {b:>3} " + " ".join(f"{star[nm][k]:>9d}" for nm in CASE_NAMES)
          + f" {floor[k]:>9d}")

print(f"\n  bits/elem:")
print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES) + f" {'FLOOR':>9}")
for k, b in enumerate(EBAND):
    print(f"  {b:>3} " + " ".join(f"{star[nm][k]/NE:>9.4f}" for nm in CASE_NAMES)
          + f" {floor[k]/NE:>9.4f}")

# excess over the all-zeros floor (true non-affine content)
print(f"\n  EXCESS over all-zeros floor  (Syn_wit* - L0)  [bits]:")
print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES))
for k, b in enumerate(EBAND):
    print(f"  {b:>3} " + " ".join(f"{star[nm][k]-floor[k]:>9d}" for nm in CASE_NAMES))

# For each candidate single committed ceiling, does SYN pass-through and ALLOY
# fail-at-ceiling under a threshold tau = floor + margin? Test a range of margins
# expressed as a multiple of the floor and as bits/elem, and report the verdict.
print("\n" + "=" * 92)
print("VERDICT SEARCH: for committed band [16..r_top], PASS iff excess>=TAU at all b")
print("  (excess = Syn_wit* - L0). Find (r_top, TAU) giving the 5 called shots.")
print("=" * 92)

called = {"SYN": "PASS", "ADD": "FAIL", "ROT": "FAIL", "COPY": "NULL", "ALLOY": "FAILrtop"}


def verdict(nm, rtop_idx, tau):
    """Return PASS / FAILrtop / FAIL using excess-over-floor >= tau across band[:rtop_idx+1]."""
    ex = [star[nm][k] - floor[k] for k in range(rtop_idx + 1)]
    allok = all(e >= tau for e in ex)
    fine_ok = ex[0] >= tau
    rtop_ok = ex[rtop_idx] >= tau
    if allok:
        return "PASS"
    if fine_ok and not rtop_ok:
        return "FAILrtop"
    return "FAIL"


for rtop in (3, 2, 1):
    rtop_idx = EBAND.index(rtop)
    for tau in (2000, 5000, 10000, 20000, 30000):
        got = {}
        for nm in CASE_NAMES:
            if nm == "COPY":
                got[nm] = "NULL"  # degenerate, upstream gate
                continue
            got[nm] = verdict(nm, rtop_idx, tau)
        ok = (got["SYN"] == "PASS" and got["ADD"] == "FAIL" and got["ROT"] == "FAIL"
              and got["ALLOY"] == "FAILrtop")
        flag = "  <<< ALL 5 MATCH" if ok else ""
        print(f"  r_top={rtop}  tau={tau:>6}: "
              + " ".join(f"{nm}={got[nm]}" for nm in CASE_NAMES) + flag)

# crossover grains: coarsest b at which each case's excess still exceeds, say,
# 5% of its own r_floor(b=16) excess -- a scale-free "still resolved" mark.
print("\n" + "=" * 92)
print("Per-case retention: excess(b) / excess(b=16), and coarsest b with >5% and >1%")
print("=" * 92)
for nm in ("SYN", "ALLOY"):
    e16 = star[nm][0] - floor[0]
    ratios = [(star[nm][k] - floor[k]) / e16 for k in range(len(EBAND))]
    print(f"  {nm:6s} " + " ".join(f"b{b}:{r:5.3f}" for b, r in zip(EBAND, ratios)))
