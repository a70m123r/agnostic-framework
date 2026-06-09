"""diag_rot.py — diagnose WHY the affine ROT case yields large Syn_wit.

ROT = cos(pi/5)*A + sin(pi/5)*B is exactly in the affine span of (A,B) on the
FLOATS. So R_AB on floats should be ~0. We check whether the large Syn_wit comes
from the quantize-FIRST ordering: A,B,M are each quantized over their OWN range
BEFORE the fit, so the affine relation M = wA*A + wB*B does NOT hold exactly
between the integer code tensors (each has a different scale/offset), and the
lstsq residual on codes is genuine quantization-rounding structure coded on M's
LSB grid. Compare to: fit on FLOATS (no quantization) -> residual ~0.
"""

from __future__ import annotations

import numpy as np

import mdl_synergy as mdl
from cases import build_case

np.set_printoptions(suppress=True)

A, B, M = build_case("ROT")
wA, wB = np.cos(np.pi / 5), np.sin(np.pi / 5)

# 1. float-domain affine residual (should be ~machine/round-trip zero)
Mf = M.astype(np.float64).ravel()
design = np.stack([A.astype(np.float64).ravel(),
                   B.astype(np.float64).ravel(),
                   np.ones_like(Mf)], axis=1)
coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
fit = design @ coef
rfloat = Mf - fit
print("[float domain] fitted coef (a_A, a_B, c) =", coef)
print(f"  true weights (cos pi/5, sin pi/5)      = ({wA:.6f}, {wB:.6f})")
print(f"  float R_AB: max|r|={np.abs(rfloat).max():.3e}  std={rfloat.std():.3e}")
print(f"  (M is float32, so this floor is the float32 storage of M, not 0)")

# 2. code-domain residual at a few b: this is what the pipeline actually codes
for b in (16, 8, 3):
    Aq = mdl.quantize(A, b).astype(np.float64)
    Bq = mdl.quantize(B, b).astype(np.float64)
    Mq = mdl.quantize(M, b).astype(np.float64)
    R_AB = mdl.affine_residual(mdl.quantize(M, b),
                               mdl.quantize(A, b), mdl.quantize(B, b))
    step, lo = mdl._grid_step(M, b)
    # residual expressed in LSB units of M's grid
    r_in_lsb = (R_AB.ravel()) / step
    levels = (1 << b) - 1
    print(f"\n[b={b}] M-grid LSB step={step:.4e}, levels={levels}")
    print(f"  code-domain R_AB: max|r|={np.abs(R_AB).max():.4f} "
          f"std={R_AB.std():.4f}  (these are in M-code units already)")
    print(f"  R_AB in M-LSB units: max|r|={np.abs(r_in_lsb).max():.3f} "
          f"std={r_in_lsb.std():.4f}")
    # how many distinct integer codes does the residual occupy?
    rc = np.rint((R_AB.ravel() - lo) / step).astype(np.int64)
    rc = rc - rc.min()
    print(f"  distinct residual codes={np.unique(rc).size}, "
          f"range=[{rc.min()},{rc.max()}], Syn_wit_bits={mdl.syn_wit(A,B,M,b)}")

# 3. SANITY: compare to ADD floor at same b (ADD is also affine).
print("\n[cross-check] Syn_wit per b: ROT vs ADD vs COPY (all 'should be' affine/floor)")
for nm in ("ROT", "ADD", "COPY"):
    a, bb, m = build_case(nm)
    vals = [mdl.syn_wit(a, bb, m, b) for b in mdl.BAND]
    print(f"  {nm:5s}: " + " ".join(f"{v:>7d}" for v in vals))
