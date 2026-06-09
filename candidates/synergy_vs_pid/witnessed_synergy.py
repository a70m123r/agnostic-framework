"""witnessed_synergy.py -- clean R1-R4-fixed witnessed-synergy estimator.

A self-contained re-implementation of the witnessed (non-additivity) synergy gate
with the four fixes the frame-lock pilot proposed and the in-tree recalibration
CONFIRMED (frame_lock_calibration_finding.md, recalib_confirm.py). No torch / HF /
network. numpy + stdlib compressors only. Controlled ground-truth tensors.

WHAT "WITNESSED SYNERGY" MEASURES
---------------------------------
Two parents A, B can produce an emergent weld M only if M carries information
reachable from BOTH jointly and from NEITHER alone -- structure NOT expressible
as any affine (linear + intercept) combination of A, B. The witness is the
description length (in bits) of the part of M that survives removing its best
affine reconstruction from (A, B):

    R_float = M - (a*A + b*B + c)          [least squares on the FLOATS]
    Syn_wit*(b) = L_b( round(R_float / step_M(b)) )

where step_M(b) is M's b-bit LSB and L_b(.) is the compressed codelength of the
integer codes. An additive blend (M in the affine span) has R_float == 0 and so
scores the all-zeros floor L0 -> FAIL. A genuine nonlinear interaction leaves a
structured residual -> real bits above the floor -> PASS, until coarse
quantization drives a small interaction sub-LSB (the frame-relative annihilation).

THE FOUR FIXES (R1-R4)
----------------------
R1  Witnessed-residual, NOT min-minus-joint. The naive BES-4.4 / PID surrogate
    Syn_pid = min(L(R_A), L(R_B)) - L(R_AB) mis-flags a pure additive blend as
    strongly synergistic. The witness is just L_b(R_AB-analog) -- the codelength
    of M's non-affine remainder -- which is 0 (floor) for any affine-span M.
    [Implemented: syn_wit_star fits the FULL affine model A,B,intercept and codes
     only the leftover; there is no min() of single-parent residuals.]

R2  Affine-blend null + floor-relative contrast, NOT a copy-null. The threshold is
    anchored on the affine-span all-zeros floor L0 (what ADD/ROT actually score),
    tau* = L0 + margin, and verdicts read the EXCESS over L0. The degenerate COPY
    case is NOT the calibrator (it sits ~18x below the affine pedestal under the
    old metric and passes everything); COPY is NULL by the upstream parent-count
    gate, not by the synergy number.
    [Implemented: zeros_floor_bits, compute_tau_star, excess = Syn - L0.]

R3  Verdict readable ACROSS the resolution band at FINE resolution, not only at a
    single coarse child-anchored r_top. PASS requires excess >= tau* at EVERY b
    from r_floor (fine) down to and including r_top. The fine end is where genuine
    synergy must show up; r_top is where the should-FAIL alloy must have decayed.
    [Implemented: band_sweep_star + verdict_star_from_band over the whole band.]

R4  Code residuals on M's OWN b-bit grid, NOT renormalized over the residual's own
    range. A near-zero residual coded on its own [min,max] gets stretched into a
    max-entropy incompressible field (inverting the witness); coding it on M's LSB
    sends "residual ~ 0" to "~all zeros -> ~0 bits".
    [Implemented: step_M = _grid_step(M, b); codes = round(R_float / step_M).]

WHAT THE RECALIBRATION CONFIRMED / REVISED (read-only, in the frame_lock tree)
------------------------------------------------------------------------------
CONFIRMED all four. The single REVISION: the child-anchored ceiling r_top moved
3 -> 2 for the 0.1*A*B alloy. The pilot's pinned r_top=3 was too FINE -- the old
quantize-FIRST rounding pedestal had MASKED a surviving 0.1*A*B bump at b=3
(ALLOY@3 ~ ADD@3 under the raw witness). Once the float-fit removes the pedestal,
the alloy is seen NOT to annihilate until b=2. r_top is therefore set by a
reviewer-recomputable function of the committed child (coarsest b at which the
child's float-residual is driven sub-LSB on its own grid), which closes the alloy
exploit MORE tightly than the pinned b=3 did. The recalib also confirmed the lzma
verdict is invariant for margin in [2000, 10000], and flagged the one wobble:
zlib leaves a ~2104-bit near-floor residual for ALLOY at the annihilation edge
(borderline on zlib only; the verdict is taken on the pinned lzma coder).

THE SHARPENED-BAR FRAMING (why this is not just PID with extra steps)
--------------------------------------------------------------------
Plain PID returns one frame-free number on fixed variables. This witnessed gate
has two things PID has no parameter for:
  (i) FRAME-RELATIVITY -- the verdict changes with the coding frame (resolution b
      / coarse-graining). ALLOY is synergistic at fine b and additive at coarse b;
      PID cannot express "synergy at this grain, none at that grain." band_sweep_*
      exposes exactly this band.
  (ii) the AFFINE QUOTIENT -- the witness quotients out the entire affine span of
      (A, B), so a pure additive blend (ADD/ROT) scores the FLOOR (excess 0). A
      mutual-information / PID synergy term need not vanish on an additive blend;
      the witness is constructed to. Whether a PROPER PID also vanishes on ADD is
      the discriminating measurement (see the companion PID-estimator agent); the
      witnessed numbers for ADD here are the FAIL baseline that comparison needs.
"""

from __future__ import annotations

import bz2
import lzma
import zlib
from dataclasses import dataclass, field

import numpy as np

# ----------------------------------------------------------------------------
# Pinned compressor configuration (raw LZMA2 stream so the byte count is
# reproducible to the bit -- no .xz container header/footer, no random check).
# ----------------------------------------------------------------------------

LZMA_PRESET = 6  # PINNED. The headline / verdict compressor.


def _c_lzma(b: bytes) -> bytes:
    filt = [{"id": lzma.FILTER_LZMA2, "preset": LZMA_PRESET}]
    return lzma.compress(b, format=lzma.FORMAT_RAW, filters=filt)


def _c_zlib(b: bytes) -> bytes:
    return zlib.compress(b, level=9)


def _c_bz2(b: bytes) -> bytes:
    return bz2.compress(b, compresslevel=9)


COMPRESSORS = {
    "lzma": _c_lzma,   # pinned / headline
    "zlib": _c_zlib,   # sibling error bar
    "bz2": _c_bz2,     # sibling error bar
}
PINNED = "lzma"


# ----------------------------------------------------------------------------
# Codelength + quantization grid
# ----------------------------------------------------------------------------

def codelength_bits(codes: np.ndarray, compressor: str = PINNED) -> int:
    """L = 8 * len(COMPRESSOR(codes.tobytes())) in bits."""
    raw = np.ascontiguousarray(codes).tobytes()
    comp = COMPRESSORS[compressor](raw)
    return 8 * len(comp)


def grid_step(ref: np.ndarray, b: int):
    """(LSB step, lo) of the b-bit uniform grid over ref's [min, max].

    Returns (None, lo) for a degenerate (constant) reference. This is the grid we
    code residuals on (R4): residuals are quantized in units of the CHILD M's LSB,
    not their own range.
    """
    ref = np.asarray(ref, dtype=np.float64)
    lo, hi = float(ref.min()), float(ref.max())
    levels = (1 << b) - 1
    if hi <= lo:
        return None, lo
    return (hi - lo) / levels, lo


# ----------------------------------------------------------------------------
# R1: witnessed residual via FLOAT-fit affine reconstruction
# ----------------------------------------------------------------------------

def affine_residual_float(M, *parents):
    """Float least-squares affine fit of M on the parents + intercept.

    Returns R = M - (sum_k a_k * P_k + c), flattened to 1-D float.

    Fitting on the FLOATS (not on quantized codes) is load-bearing: for any M
    genuinely in the affine span of the parents the residual is ~0 to float
    precision, carrying NO quantize-first rounding-commutator pedestal. (Fitting
    on integer codes leaves ~1.6 bits/elem of independent rounding noise that a
    bit-counter mistakes for novelty -- the defect the recalib diagnosed.)
    """
    Mf = np.asarray(M, dtype=np.float64).ravel()
    cols = [np.asarray(p, dtype=np.float64).ravel() for p in parents]
    cols.append(np.ones_like(Mf))  # intercept
    design = np.stack(cols, axis=1)
    coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
    return Mf - design @ coef


# ----------------------------------------------------------------------------
# R4: residual codelength on the CHILD's own b-bit grid
# ----------------------------------------------------------------------------

def syn_wit_star(A, B, M, b, compressor=PINNED):
    """WITNESSED synergy at resolution b (bits):

        Syn_wit*(b) = L_b( round( R_float / step_M(b) ) )

    R_float = M - (float-lstsq affine fit of M on A, B);
    step_M(b) = M's b-bit LSB (R4: code on the child's grid, not the residual's).

    Affine-span M  => R_float == 0 => all-zeros codes => L0 floor (FAIL side).
    Genuine non-affine structure => real bits above the floor, decaying as b
    coarsens and the interaction is driven sub-LSB on M's grid (frame-relative
    annihilation -- the ALLOY behavior).
    """
    rfl = affine_residual_float(M, A, B)
    step, _lo = grid_step(M, b)
    if step is None:
        return 0
    codes = np.rint(rfl / step).astype(np.int64)
    codes = codes - codes.min()  # nonneg, scale-preserving
    return codelength_bits(codes.astype(np.int64), compressor=compressor)


# ----------------------------------------------------------------------------
# R2: affine-blend null floor + floor-relative threshold
# ----------------------------------------------------------------------------

def zeros_floor_bits(n_elem, compressor=PINNED):
    """L0 = codelength (bits) of an all-zeros residual of n_elem codes.

    The corrected NULL (R2): what an EXACTLY affine-span M (ADD/ROT) scores under
    syn_wit_star at any b. Pure compressor overhead, no structure. Deterministic
    (identical bytes => identical codelength => bootstrap sigma == 0), which is
    why the old COPY-style "+3 sigma" band collapses to a flat margin here.
    """
    return codelength_bits(np.zeros(int(n_elem), dtype=np.int64),
                           compressor=compressor)


def compute_tau_star(n_elem, margin=2000, compressor=PINNED):
    """Floor-relative threshold tau* = L0 + margin (R2).

    The lzma verdict is invariant for margin in [2000, 10000] because the
    should-FAIL cases sit AT L0 by genuine annihilation, not merely near tau*.
    Returns (tau_star, L0).
    """
    L0 = zeros_floor_bits(n_elem, compressor=compressor)
    return L0 + float(margin), L0


# ----------------------------------------------------------------------------
# R3: band sweep + verdict readable across the resolution band
# ----------------------------------------------------------------------------

# Resolution band: r_floor = 16 (fine) ... r_top = 2 (coarse child-anchored
# ceiling -- REVISED 3->2 by the recalib; see module docstring).
BAND = [16, 12, 8, 6, 4, 3, 2]
R_FLOOR = 16
R_TOP = 2


@dataclass
class BandRow:
    b: int
    syn_wit: int           # Syn_wit*(b) in bits
    n_elem: int
    L0: int
    excess: int = field(init=False)        # Syn_wit* - L0 (true non-affine content)
    syn_wit_per_elem: float = field(init=False)
    excess_per_elem: float = field(init=False)

    def __post_init__(self):
        self.excess = self.syn_wit - self.L0
        self.syn_wit_per_elem = self.syn_wit / self.n_elem
        self.excess_per_elem = self.excess / self.n_elem


def band_sweep_star(A, B, M, band=BAND, compressor=PINNED):
    """Witnessed synergy across the whole resolution band (R3).

    Returns a list of BandRow (one per b in `band`, most-fine first), each
    carrying Syn_wit*(b), the floor L0, and the excess over floor.
    """
    n = int(np.asarray(M).size)
    L0 = zeros_floor_bits(n, compressor=compressor)
    rows = []
    for b in band:
        sw = syn_wit_star(A, B, M, b, compressor=compressor)
        rows.append(BandRow(b=b, syn_wit=sw, n_elem=n, L0=L0))
    return rows


def verdict_star_from_band(rows, r_top=R_TOP, margin=2000, compressor=PINNED):
    """Verdict under the witnessed gate, read across the band (R2 + R3).

    PASS iff excess (Syn_wit* - L0) >= margin at EVERY b from r_floor down to and
    including r_top. Returns (verdict, detail) where verdict is one of
    {PASS, FAIL@r_top, FAIL}:
        PASS         -- synergy survives the whole band through the ceiling
        FAIL@r_top   -- resolves at fine b but annihilated by r_top (frame-relative;
                        e.g. ALLOY): genuine synergy at fine grain, none at coarse
        FAIL         -- below floor even at fine b (e.g. pure additive blend)
    detail carries per-b (b, syn_wit, excess, ok) and tau*/L0.
    """
    n = rows[0].n_elem
    tau, L0 = compute_tau_star(n, margin=margin, compressor=compressor)
    grid = [r for r in rows if r.b >= r_top]
    per_b = [(r.b, r.syn_wit, r.excess, r.excess >= margin) for r in grid]
    all_ok = all(ok for *_, ok in per_b)
    fine_ok = per_b[0][3]
    rtop_ok = per_b[-1][3]
    if all_ok:
        verdict = "PASS"
    elif fine_ok and not rtop_ok:
        verdict = "FAIL@r_top"
    else:
        verdict = "FAIL"
    return verdict, {"tau_star": tau, "L0": L0, "margin": margin,
                     "r_top": r_top, "per_b": per_b}


# ----------------------------------------------------------------------------
# Naive PID-form surrogate -- kept ONLY as the contrast the witness must beat.
# This is the min-minus-joint form R1 rejects; it mis-flags additive blends.
# (NOT the verdict estimator; included so the SYN-vs-ADD separation is visible.)
# ----------------------------------------------------------------------------

def quantize_own_range(X, b):
    """Uniform b-bit codes of X over X's OWN [min,max] (for the naive surrogate)."""
    X = np.asarray(X, dtype=np.float64)
    lo, hi = float(X.min()), float(X.max())
    levels = (1 << b) - 1
    if hi <= lo:
        return np.zeros(X.shape, dtype=np.int64)
    codes = np.rint((X - lo) / (hi - lo) * levels).astype(np.int64)
    return np.clip(codes, 0, levels)


def syn_pid_naive(A, B, M, b, compressor=PINNED):
    """NAIVE BES-Thm-4.4 / PID-form surrogate (the thing R1 rejects):
        Syn_pid(b) = min(L_b(R_A), L_b(R_B)) - L_b(R_AB)
    with the affine fit on quantized codes and residuals coded on M's grid.
    Provided only to exhibit that this form mis-orders additive blends; do NOT
    use it for the verdict.
    """
    Aq = quantize_own_range(A, b).astype(np.float64)
    Bq = quantize_own_range(B, b).astype(np.float64)
    Mq = quantize_own_range(M, b).astype(np.float64)

    def _resid(Mc, *cols):
        Mf = Mc.ravel()
        design = np.stack([c.ravel() for c in cols] + [np.ones_like(Mf)], axis=1)
        coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
        return Mf - design @ coef

    step, _ = grid_step(Mq, b)
    if step is None:
        return 0

    def _code(R):
        c = np.rint(R / step).astype(np.int64)
        return codelength_bits((c - c.min()).astype(np.int64), compressor=compressor)

    L_RA = _code(_resid(Mq, Aq))
    L_RB = _code(_resid(Mq, Bq))
    L_RAB = _code(_resid(Mq, Aq, Bq))
    return min(L_RA, L_RB) - L_RAB


# ----------------------------------------------------------------------------
# Pretty-print helper
# ----------------------------------------------------------------------------

def format_band_table(rows, title=""):
    lines = []
    if title:
        lines.append(title)
    lines.append(f"  {'b':>3}  {'Syn_wit*':>10}  {'excess(-L0)':>12}  {'wit/elem':>10}")
    for r in rows:
        lines.append(f"  {r.b:>3}  {r.syn_wit:>10}  {r.excess:>12}  "
                     f"{r.syn_wit_per_elem:>10.4f}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Smoke test: the discriminating pair SYN (PASS) vs ADD (FAIL), plus the full
# 6-case band. REAL numbers only -- run `python witnessed_synergy.py`.
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    from cases import CASE_NAMES, PREDICTED, build_case

    NE = 256 * 256
    MARGIN = 2000
    L0 = zeros_floor_bits(NE)
    tau, _ = compute_tau_star(NE, margin=MARGIN)

    print("=" * 86)
    print("WITNESSED SYNERGY (R1-R4 fixed) -- clean re-implementation")
    print("Syn_wit*(b) = L_b( round(R_float / step_M(b)) ), "
          "R_float = M - float_affine_fit(M; A,B)")
    print(f"null = affine-span all-zeros floor L0 = {L0} bits ; "
          f"band = {BAND} ; r_top = {R_TOP}")
    print(f"pinned coder = lzma p6 ; tau* = L0 + margin({MARGIN}) = {tau:.0f} bits")
    print("=" * 86)

    # --- discriminating pair: SYN vs ADD (the headline) ---
    print("\n--- DISCRIMINATING PAIR: witnessed synergy on SYN (PASS) vs ADD (FAIL) ---")
    for nm in ("SYN", "ADD"):
        A, B, M = build_case(nm)
        rows = band_sweep_star(A, B, M)
        verdict, _ = verdict_star_from_band(rows, margin=MARGIN)
        print(f"\n  {nm}  (predicted {PREDICTED[nm]}, witnessed verdict {verdict})")
        print(format_band_table(rows))

    # --- full 6-case band ---
    print("\n" + "=" * 86)
    print("FULL 6-CASE BAND  --  Syn_wit*(b) in bits")
    print("=" * 86)
    star = {nm: band_sweep_star(*build_case(nm)) for nm in CASE_NAMES}
    print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES) + f" {'FLOOR':>9}")
    for k, b in enumerate(BAND):
        print(f"  {b:>3} " + " ".join(f"{star[nm][k].syn_wit:>9d}" for nm in CASE_NAMES)
              + f" {L0:>9d}")

    print("\n  EXCESS over affine-span floor L0 (true non-affine content) [bits]:")
    print(f"  {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES))
    for k, b in enumerate(BAND):
        print(f"  {b:>3} " + " ".join(f"{star[nm][k].excess:>9d}" for nm in CASE_NAMES))

    print("\n" + "=" * 86)
    print("VERDICTS vs PREDICTED (witnessed gate)")
    print("=" * 86)
    allmatch = True
    for nm in CASE_NAMES:
        verdict, _ = verdict_star_from_band(star[nm], margin=MARGIN)
        if nm == "COPY":
            verdict = "NULL (degenerate; upstream parent-count gate)"
            got = "NULL"
        else:
            got = verdict
        ok = (got == PREDICTED[nm]) or (nm == "COPY" and got == "NULL")
        allmatch &= ok
        print(f"  {nm:6s} predicted={PREDICTED[nm]:11s} got={got:11s} "
              f"{'MATCH' if ok else 'MISMATCH'}")
    print(f"\n  ALL CALLED SHOTS MATCH: {allmatch}")

    # --- naive PID-form surrogate at fine b: shows it does NOT cleanly separate
    #     ADD from SYN the way the witness does (R1 motivation). ---
    print("\n" + "=" * 86)
    print("NAIVE min-minus-joint surrogate (the form R1 REJECTS) at b=16, bits:")
    print("  -- shown only to motivate R1; not the verdict estimator --")
    print("=" * 86)
    for nm in CASE_NAMES:
        A, B, M = build_case(nm)
        v = syn_pid_naive(A, B, M, 16)
        print(f"  {nm:6s} syn_pid_naive(b16) = {v:>10d}")
