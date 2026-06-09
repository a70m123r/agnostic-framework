"""interaction_synergy.py -- the BUG-FIXED interaction-emergence gate.

WHY THIS FILE EXISTS (the confirmed bug it fixes)
-------------------------------------------------
The witnessed gate in `witnessed_synergy.py` quotients out only the AFFINE span
(aA + bB + c) of the parents and codes the remainder. The 2026-06-09 cross-model
pass (Gemini) proved this FALSE-POSITIVES on SEPARABLE nonlinearity: M = A^2+B^2
-- each parent transformed *separately* then added, with ZERO parent-interaction
-- was flagged at 1,040,352 bits, HIGHER than a genuine A*B interaction
(1,009,536 bits). See `separable_falsification_test.py` (the reproduced bug) and
`CROSS_MODEL_REVIEW.md` (the confirmation). The affine-residual gate measures
NON-AFFINITY, not interaction-emergence: A^2 is outside the affine span of A, so
A^2+B^2 leaves a huge affine residual despite being purely separable.

THE FIX (this module)
---------------------
"Additive blend = no emergence" must mean SEPARABLE (f(A) + g(B) for arbitrary,
possibly NONLINEAR f, g), not merely AFFINE (aA + bB + c). The right residual is
the exact 2-way FUNCTIONAL-ANOVA INTERACTION term:

    interaction(M) = M  -  Ehat[M | A]  -  Ehat[M | B]  +  Ehat[M]

  * Ehat[M | A] : average of M within each A-bin (A binned into `bins` quantile
                  bins -- the SAME quantile binning and SAME default bin count
                  pid_synergy.py uses, bins=8), broadcast back to the elements;
                  the best piecewise-constant function of A alone.
  * Ehat[M | B] : symmetric, the best piecewise-constant function of B alone.
  * Ehat[M]     : the global mean of M.

For ANY separable M = f(A) + g(B):
    Ehat[M|A] = f(A-bin-mean) + mean(g(B)),  Ehat[M|B] = mean(f(A)) + g(B-bin-mean),
    Ehat[M]   = mean(f(A)) + mean(g(B)),
so interaction(M) = [f(A) - f(A-bin-mean)] + [g(B) - g(B-bin-mean)] = ONLY the
within-bin discretization wiggle of the separable parts -- which -> 0 as the bins
resolve f, g, and is driven to the floor on M's coding grid. The separable mains
(including A^2+B^2) are removed BY CONSTRUCTION. Only genuine JOINT structure
(A*B, XOR, max(A,B)) -- which no f(A)+g(B) can absorb -- survives.

CODING (IDENTICAL to the witnessed gate, so the two are directly comparable)
----------------------------------------------------------------------------
Exactly as witnessed_synergy.syn_wit_star, but with the interaction residual in
place of the affine residual:

    Syn_int*(b) = L_b( round( interaction(M) / step_M(b) ) )

  * step_M(b)   = M's OWN b-bit LSB (R4: code the residual on the CHILD's grid,
                  not the residual's own range) -- reused from witnessed_synergy.
  * L_b(.)      = pinned lzma p6 raw-stream codelength in bits -- reused from
                  witnessed_synergy.codelength_bits (same compressor, same config).
  * excess      = Syn_int*(b) - L0, the all-zeros affine-span floor -- reused
                  from witnessed_synergy.zeros_floor_bits (IDENTICAL floor).
  * band/r_top  = the SAME resolution band + child-anchored ceiling, so
                  frame-relativity is still read off the band (R3).

So the ONLY change from the buggy gate is residual = interaction(M) instead of
residual = M - affine_fit(M; A,B). Everything downstream (grid, compressor,
floor, band, verdict logic) is reused verbatim from witnessed_synergy.py and the
quantile binner is reused verbatim from pid_synergy.py. No reimplementation.

DISCIPLINE: controlled ground-truth numpy only. No torch / HF / network. The
real-substrate (model-merge) run remains the explicitly-owed later step.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Reuse the EXACT coding machinery of the witnessed gate so the two gates differ
# in ONE thing only (the residual), and the excess/floor/band are comparable.
from witnessed_synergy import (
    BAND,
    R_FLOOR,
    R_TOP,
    codelength_bits,
    compute_tau_star,
    grid_step,
    zeros_floor_bits,
)

# Reuse PID's quantile binner so Ehat[M|A] is conditioned on the SAME bins PID
# uses (no separate, divergent discretization).
from pid_synergy import _quantile_bin

PINNED = "lzma"
DEFAULT_BINS = 8  # SAME as pid_synergy.binned_williams_beer_pid default.


# ----------------------------------------------------------------------------
# The fix: 2-way functional-ANOVA interaction residual.
# ----------------------------------------------------------------------------

def _conditional_mean(M_flat: np.ndarray, labels: np.ndarray, n_lab: int) -> np.ndarray:
    """Ehat[M | X] as a piecewise-constant array: mean of M within each X-bin,
    broadcast back to every element by its bin label.

    M_flat : (N,) float ; labels : (N,) int in [0, n_lab) ; returns (N,) float.
    This is the best (L2) piecewise-constant predictor of M from the binned X --
    the discrete conditional expectation. Empty bins (no samples) contribute the
    global mean for their (nonexistent) members, which never get indexed.
    """
    sums = np.zeros(n_lab, dtype=np.float64)
    cnts = np.zeros(n_lab, dtype=np.float64)
    np.add.at(sums, labels, M_flat)
    np.add.at(cnts, labels, 1.0)
    means = np.divide(sums, cnts, out=np.full(n_lab, M_flat.mean()),
                      where=cnts > 0)
    return means[labels]


def interaction_residual(A, B, M, bins: int = DEFAULT_BINS) -> np.ndarray:
    """The 2-way functional-ANOVA interaction term of M w.r.t (A, B):

        interaction(M) = M - Ehat[M|A] - Ehat[M|B] + Ehat[M]

    A, B binned into `bins` quantile bins (the SAME binning PID uses). Returns the
    flattened 1-D float interaction residual.

    SEPARABLE M = f(A)+g(B)  => this is only the within-bin wiggle of f,g (-> 0 as
    bins resolve them; floored on M's grid). GENUINE joint M (A*B, XOR, max) =>
    large structured residual no separable model can remove.
    """
    Mf = np.asarray(M, dtype=np.float64).ravel()
    la = _quantile_bin(A, bins)
    lb = _quantile_bin(B, bins)
    na = int(la.max()) + 1
    nb = int(lb.max()) + 1
    E_M_given_A = _conditional_mean(Mf, la, na)
    E_M_given_B = _conditional_mean(Mf, lb, nb)
    E_M = float(Mf.mean())
    return Mf - E_M_given_A - E_M_given_B + E_M


def interaction_variance_fraction(A, B, M, bins: int = DEFAULT_BINS) -> float:
    """Var(interaction(M)) / Var(M): the RESOLUTION-INDEPENDENT discriminator.

    This is the fraction of M's variance that the functional-ANOVA interaction
    term carries -- the honest, grid-free read of "how much of M is genuine joint
    structure." Unlike the codelength excess (which is coded on M's fine grid and
    is corrupted by the piecewise-constant within-bin wiggle, see
    INTERACTION_RESULTS.md), this quantity SEPARATES the battery cleanly:
    separable cases -> small and FALLING toward 0 as bins rise; genuine
    interactions -> large and STABLE. Reported as the diagnostic that the ANOVA
    DECOMPOSITION is correct even though the codelength READOUT leaks.
    """
    Mf = np.asarray(M, dtype=np.float64).ravel()
    inter = interaction_residual(A, B, M, bins=bins)
    vm = float(Mf.var())
    if vm <= 0.0:
        return 0.0
    return float(inter.var() / vm)


# ----------------------------------------------------------------------------
# EXACT-SEPARABLE variant: remove the best SMOOTH separable additive model
# f(A)+g(B) via a per-parent polynomial main-effects basis (NO cross terms),
# fitted in the CONTINUOUS variable, so the separable mains are removed exactly
# (not piecewise-constant). This floors every separable case the basis can SPAN
# (affine, A^2+B^2, A^3+B^3, ADD, ROT, exp, sin/cos at high degree) to ~L0 -- but
# it still FALSE-POSITIVES on separable functions OUTSIDE the basis (|A|+|B|, a
# polynomial cannot represent the kink). So it does NOT fully fix the bug; it
# moves the affine bug ONE RUNG up (affine span -> polynomial span). Kept as the
# honest "best in-family repair" so the residual-leak finding is reproducible.
# ----------------------------------------------------------------------------

def _poly_basis(x: np.ndarray, deg: int) -> np.ndarray:
    """Per-parent polynomial main-effect basis 1, x, x^2, ..., x^deg (one parent)."""
    return np.column_stack([x ** k for k in range(deg + 1)])


def separable_residual_poly(A, B, M, deg: int = 8) -> np.ndarray:
    """M minus the best polynomial separable additive model poly_deg(A)+poly_deg(B).

    Exact (continuous-variable) main-effects removal: floors any separable M in
    the polynomial span; leaks on separable M outside it (e.g. |A|+|B|). Returns
    the flattened 1-D float residual.
    """
    Mf = np.asarray(M, dtype=np.float64).ravel()
    af = np.asarray(A, dtype=np.float64).ravel()
    bf = np.asarray(B, dtype=np.float64).ravel()
    # poly(A) full + poly(B) minus its duplicate intercept column = shared intercept
    X = np.column_stack([_poly_basis(af, deg), _poly_basis(bf, deg)[:, 1:]])
    coef, *_ = np.linalg.lstsq(X, Mf, rcond=None)
    return Mf - X @ coef


def syn_int_poly_star(A, B, M, b, deg: int = 8, compressor=PINNED):
    """EXACT-SEPARABLE (polynomial) interaction synergy at resolution b (bits).

    Same coding as syn_int_star, but the residual is separable_residual_poly
    (continuous polynomial main-effects removed) instead of the binned ANOVA term.
    """
    rfl = separable_residual_poly(A, B, M, deg=deg)
    step, _lo = grid_step(M, b)
    if step is None:
        return 0
    codes = np.rint(rfl / step).astype(np.int64)
    codes = codes - codes.min()
    return codelength_bits(codes.astype(np.int64), compressor=compressor)


# ----------------------------------------------------------------------------
# The gate value: residual codelength on M's own b-bit grid (IDENTICAL coding to
# witnessed_synergy.syn_wit_star, only the residual differs).
# ----------------------------------------------------------------------------

def syn_int_star(A, B, M, b, bins: int = DEFAULT_BINS, compressor=PINNED):
    """INTERACTION-emergence synergy at resolution b (bits):

        Syn_int*(b) = L_b( round( interaction(M) / step_M(b) ) )

    interaction(M) = the 2-way functional-ANOVA term (separable mains removed);
    step_M(b)      = M's b-bit LSB (code on the child's grid, R4);
    L_b(.)         = pinned lzma p6 codelength (reused).

    Separable M (incl. A^2+B^2) => interaction ~0 => all-zeros codes => L0 floor.
    Genuine joint interaction (A*B, XOR, max) => real bits above the floor,
    decaying as b coarsens (frame-relative annihilation -- the ALLOY behavior).
    """
    rfl = interaction_residual(A, B, M, bins=bins)
    step, _lo = grid_step(M, b)
    if step is None:
        return 0
    codes = np.rint(rfl / step).astype(np.int64)
    codes = codes - codes.min()  # nonneg, scale-preserving (same as the witness)
    return codelength_bits(codes.astype(np.int64), compressor=compressor)


# ----------------------------------------------------------------------------
# Band sweep + verdict -- reused logic from witnessed_synergy, retargeted to the
# interaction residual so frame-relativity stays readable off the band.
# ----------------------------------------------------------------------------

@dataclass
class IntBandRow:
    b: int
    syn_int: int           # Syn_int*(b) in bits
    n_elem: int
    L0: int
    excess: int = field(init=False)          # Syn_int* - L0 (true interaction content)
    syn_int_per_elem: float = field(init=False)
    excess_per_elem: float = field(init=False)

    def __post_init__(self):
        self.excess = self.syn_int - self.L0
        self.syn_int_per_elem = self.syn_int / self.n_elem
        self.excess_per_elem = self.excess / self.n_elem


def band_sweep_int(A, B, M, band=BAND, bins: int = DEFAULT_BINS, compressor=PINNED):
    """Interaction synergy across the whole resolution band (R3).

    Returns a list of IntBandRow (one per b, most-fine first), each carrying
    Syn_int*(b), the floor L0, and the excess over floor.
    """
    n = int(np.asarray(M).size)
    L0 = zeros_floor_bits(n, compressor=compressor)
    rows = []
    for b in band:
        sw = syn_int_star(A, B, M, b, bins=bins, compressor=compressor)
        rows.append(IntBandRow(b=b, syn_int=sw, n_elem=n, L0=L0))
    return rows


def verdict_int_from_band(rows, r_top=R_TOP, margin=2000, compressor=PINNED):
    """Verdict under the interaction gate, read across the band (R2 + R3).

    Identical verdict logic to witnessed_synergy.verdict_star_from_band:
    PASS iff excess >= margin at EVERY b from r_floor down to and including r_top.
        PASS         -- interaction survives the whole band through the ceiling
        FAIL@r_top   -- resolves at fine b but annihilated by r_top (frame-relative;
                        e.g. ALLOY): genuine interaction at fine grain, none at coarse
        FAIL         -- below floor even at fine b (separable / additive: ADD, ROT,
                        and now A^2+B^2 -- the bug fix)
    """
    n = rows[0].n_elem
    tau, L0 = compute_tau_star(n, margin=margin, compressor=compressor)
    grid = [r for r in rows if r.b >= r_top]
    per_b = [(r.b, r.syn_int, r.excess, r.excess >= margin) for r in grid]
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


def format_int_band_table(rows, title=""):
    lines = []
    if title:
        lines.append(title)
    lines.append(f"  {'b':>3}  {'Syn_int*':>10}  {'excess(-L0)':>12}  {'int/elem':>10}")
    for r in rows:
        lines.append(f"  {r.b:>3}  {r.syn_int:>10}  {r.excess:>12}  "
                     f"{r.syn_int_per_elem:>10.4f}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Self-test: the bug-fix headline (A^2+B^2 must now FLOOR) + the full battery,
# plus a bin-sensitivity sweep. REAL numbers only -- run `python interaction_synergy.py`.
# ----------------------------------------------------------------------------

def _battery():
    """The full re-benchmark battery as (label, group, M-builder) over shared A,B.

    group in {separable, genuine, original}. Parents A,B,noise use the EXACT
    cases.py seeds so this is on the same ground truth.
    """
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float32)
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float32)
    noise = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float32)

    cases = [
        # --- original 6 ---
        ("SYN  0.5A+0.5B+0.5AB", "original", 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * noise),
        ("ADD  0.5A+0.5B",       "original", 0.5 * A + 0.5 * B),
        ("ROT  cosA+sinB",       "original", np.cos(np.pi / 5) * A + np.sin(np.pi / 5) * B),
        ("COPY A+0.001n",        "original", A + 0.001 * noise),
        ("ALLOY 0.5A+0.5B+0.1AB", "original", 0.5 * A + 0.5 * B + 0.1 * (A * B)),
        ("XOR  sign(A)*sign(B)", "original", np.sign(A) * np.sign(B)),
        # --- separable falsification battery (MUST floor) ---
        ("A^2+B^2",   "separable", A * A + B * B),
        ("A^3+B^3",   "separable", A ** 3 + B ** 3),
        ("sin(A)+cos(B)", "separable", np.sin(A) + np.cos(B)),
        ("exp(.5A)+exp(.5B)", "separable", np.exp(0.5 * A) + np.exp(0.5 * B)),
        ("|A|+|B|",   "separable", np.abs(A) + np.abs(B)),
        # --- genuine-interaction controls (MUST flag) ---
        ("A*B",       "genuine", A * B),
        ("A*B^2",     "genuine", A * (B * B)),
        ("A^2*B^2",   "genuine", (A * A) * (B * B)),
        ("sign(A)*sign(B) XOR", "genuine", np.sign(A) * np.sign(B)),
        ("max(A,B)",  "genuine", np.maximum(A, B)),
    ]
    return A, B, [(lbl, grp, M.astype(np.float32)) for lbl, grp, M in cases]


if __name__ == "__main__":
    A, B, battery = _battery()
    NE = A.size
    MARGIN = 2000
    L0 = zeros_floor_bits(NE)
    tau, _ = compute_tau_star(NE, margin=MARGIN)

    print("=" * 92)
    print("INTERACTION-EMERGENCE GATE (bug-fixed: separable / functional-ANOVA quotient)")
    print("Syn_int*(b) = L_b( round( interaction(M)/step_M(b) ) ),  "
          "interaction(M) = M - E[M|A] - E[M|B] + E[M]")
    print(f"E[M|.] via {DEFAULT_BINS}-quantile bins (= PID bins); pinned coder = lzma p6")
    print(f"affine-span all-zeros floor L0 = {L0} bits ; band = {BAND} ; "
          f"r_top = {R_TOP} ; margin = {MARGIN}")
    print("=" * 92)

    rows_by_case = {}
    print("\n--- FULL BATTERY: interaction-gate excess over floor L0 (bits) ---")
    print(f"  {'case':22} {'group':9} {'excess@b16':>12} {'excess@r_top':>13} {'verdict':>11}")
    for lbl, grp, M in battery:
        rows = band_sweep_int(A, B, M)
        rows_by_case[lbl] = rows
        verdict, _ = verdict_int_from_band(rows, margin=MARGIN)
        fine = rows[0].excess
        rtop = [r for r in rows if r.b == R_TOP][0].excess
        if lbl.startswith("COPY"):
            verdict = "NULL"
        print(f"  {lbl:22} {grp:9} {fine:>12,} {rtop:>13,} {verdict:>11}")

    # --- the bug-fix headline: A^2+B^2 must now FLOOR (excess ~ 0) ---
    print("\n" + "=" * 92)
    print("BUG-FIX HEADLINE -- the case that broke the affine gate")
    print("=" * 92)
    sep = rows_by_case["A^2+B^2"]
    print(format_int_band_table(sep, title="  A^2+B^2 (separable, NO interaction):"))
    print(f"\n  affine-residual gate flagged A^2+B^2 at 1,040,352 bits (the BUG).")
    print(f"  interaction gate excess @ b16 = {sep[0].excess} bits "
          f"(floored: {sep[0].excess < MARGIN}).")

    # --- bin-sensitivity sweep on the bug case + a genuine control ---
    print("\n" + "=" * 92)
    print("BIN-COUNT SENSITIVITY (excess @ b=16, bits) -- E[M|.] bin count vs PID's 8")
    print("=" * 92)
    sens_cases = ["A^2+B^2", "|A|+|B|", "A*B", "sign(A)*sign(B) XOR", "ALLOY 0.5A+0.5B+0.1AB"]
    bin_grid = [4, 8, 16, 32]
    print(f"  {'case':22} " + " ".join(f"bins={k:<2}".rjust(12) for k in bin_grid))
    for lbl in sens_cases:
        M = next(m for (l, g, m) in battery if l == lbl)
        vals = []
        for k in bin_grid:
            e = syn_int_star(A, B, M, 16, bins=k) - L0
            vals.append(e)
        print(f"  {lbl:22} " + " ".join(f"{v:>12,}" for v in vals))
    print("\n  (separable cases should stay near floor across bin counts; genuine")
    print("   interactions stay large -- bin count trades within-bin wiggle vs noise.)")
