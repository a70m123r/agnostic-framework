"""cand_gam_anova.py -- GAM / functional-ANOVA interaction, the misspecification-robust
candidate emergence-function (the cross-model recommended fix).

WHAT THIS MEASURES (and why it is the *robust* version of the residual approach)
--------------------------------------------------------------------------------
The "synergy gate" asks whether two parents A, B make an emergent third M that is
MORE than a SEPARABLE combination f(A) + g(B). The earliest gate quotiented out
only the AFFINE span (aA+bB+c) and false-positived on SEPARABLE nonlinearity
(M = A^2+B^2, zero interaction, flagged -- see separable_falsification_test.py).
The fix is functional-ANOVA: subtract the best SEPARABLE model and call the
remainder the 2-way interaction term. But the cross-model pass (GPT-5.5 + Gemini,
recorded in RATIO_FRAME_TEST.md) flagged the DEEP caveat:

    "defining interaction as residual-variance-after-a-separable-fit CONFOUNDS
     genuine interaction with main-effect model MISSPECIFICATION -- any
     underpowered or wrong-basis main-effects model manufactures false
     'interaction'. The measure is only as good as its separable model; it needs
     a flexible, HELD-OUT GAM."

ratio_frame_test.py already showed this failure mode directly: a fixed degree-3
separable polynomial fit IN-SAMPLE on coarsely-quantized data manufactured false
interaction (ADD -> 0.51, SEP A^2+B^2 -> 0.88 at b=2) purely because the
underpowered basis could not fit the (quantization-induced) step main-effects.

THIS MODULE is the misspecification-robust answer. Two ingredients, both load-bearing:

  (1) FLEXIBLE separable basis. Each parent gets a natural cubic regression-spline
      expansion (B-spline basis, knots at parent quantiles) -- a GAM main-effects
      model g_A(A) + g_B(B). Splines are a far richer separable class than a fixed
      low-degree polynomial, so they actually FIT smooth separable mains (incl.
      A^2, A^3, |A|, ...) instead of leaving a misspecification residual that a
      naive measure would misread as interaction.

  (2) HELD-OUT evaluation. The separable GAM is FIT on a TRAIN split and the
      interaction variance-fraction is scored on a disjoint HELD-OUT split. This
      is the actual guard against misspecification-as-interaction: an underpowered
      OR over-flexible main-effects model is penalised out of sample. If extra
      spline flexibility were merely overfitting separable structure (the coarse-b
      failure mode), the held-out main-effects R^2 would not improve and the
      held-out interaction fraction would not be inflated. Genuine joint structure
      (A*B, XOR), which NO separable g_A(A)+g_B(B) can absorb at any flexibility,
      is exactly what survives out of sample.

THE MEASURE
-----------
    gam_interaction_frac(M)  =  Var_test( M - [ ghat_A(A) + ghat_B(B) ] )  /  Var_test(M)

where ghat_A, ghat_B are the spline main-effects fit by least squares on the train
split (centered; intercept absorbs the grand mean), evaluated on the test split,
and Var_test is the variance over held-out elements. This is the held-out fraction
of M's variance NOT explained by the best flexible separable model -- the
functional-ANOVA 2-way interaction component, the GAM-bits analogue in variance units.

  ~0   => M is (within held-out noise) a separable function of A and B: NO emergent
          third. ADD, ROT, COPY, and SEP=A^2+B^2 all land here (A^2+B^2 BY
          CONSTRUCTION: it is exactly separable, so the per-parent splines absorb it).
  HIGH => M carries joint A,B structure no separable model explains: emergent third.
          INT=A*B and XOR land here.

HOW IT HANDLES THE MISSPECIFICATION CAVEAT (the whole point)
-----------------------------------------------------------
  * FLEXIBILITY: splines (not a fixed low-degree polynomial) make the separable
    class rich enough that a genuinely separable M leaves ~0 residual -- so residual
    != misspecification for the separable cases.
  * HELD-OUT: scoring out of sample means MORE knots cannot manufacture interaction
    by overfitting; the floor cases stay ~0 as flexibility grows and the flag cases
    stay high. The built-in `misspecification_sweep()` demonstrates exactly this:
    sweep the spline knot count and show ADD / SEP / ROT held-out fraction stays
    pinned near 0 while INT / XOR / SYN stay high and FLAT -- i.e. the verdict is
    NOT an artifact of how flexible the main-effects model is. That stability across
    the flexibility axis IS the misspecification-robustness evidence.
  * RESIDUAL CAVEAT NOT FULLY DISSOLVED (honest): held-out + flexible bounds the
    confound but does not erase it -- with finite knots a sufficiently wiggly TRUE
    separable main-effect could still leave a small held-out residual. The sweep is
    the diagnostic that tells you whether you are in that regime (fraction creeping
    up with knots on a "floor" case = under-resolved main-effect, not interaction).
    The measure is a DIAGNOSTIC read together with its sweep, not a standalone scalar.

DISCIPLINE: controlled ground-truth, numpy + scipy(interpolate) only. No sklearn,
no torch, no HF, no network. New file; existing committed files untouched.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import BSpline


# ----------------------------------------------------------------------------- #
# Flexible separable main-effects basis: natural-ish cubic B-spline per parent.  #
# ----------------------------------------------------------------------------- #
def _bspline_design(x: np.ndarray, knots_interior: np.ndarray, degree: int = 3) -> np.ndarray:
    """Cubic B-spline design matrix for a 1-D parent x.

    Interior knots at the given quantile locations; boundary knots clamped
    (repeated `degree+1` times) at the data range so the basis spans the whole
    support. Returns an (n, K) design block; the per-column basis functions sum
    to 1, so a separate intercept handles the level and we drop the basis mean
    later for identifiability with the cross-parent ANOVA centering.
    """
    lo, hi = float(x.min()), float(x.max())
    # Clamped knot vector: (degree+1) copies of each boundary + sorted interior.
    t = np.concatenate(
        [np.full(degree + 1, lo), np.sort(knots_interior), np.full(degree + 1, hi)]
    )
    n_basis = len(t) - degree - 1
    # Evaluate each B-spline basis function on x.
    cols = np.empty((x.shape[0], n_basis), dtype=np.float64)
    eye = np.eye(n_basis)
    for j in range(n_basis):
        cols[:, j] = BSpline(t, eye[j], degree, extrapolate=True)(x)
    return cols


def _interior_knots(x_train: np.ndarray, n_interior: int) -> np.ndarray:
    """Interior knots at interior quantiles of the TRAIN parent values."""
    if n_interior <= 0:
        return np.empty(0, dtype=np.float64)
    qs = np.linspace(0.0, 1.0, n_interior + 2)[1:-1]
    return np.quantile(x_train, qs)


@dataclass
class GamSplit:
    train_idx: np.ndarray
    test_idx: np.ndarray


def _split(n: int, frac_train: float = 0.5, seed: int = 1234) -> GamSplit:
    """Deterministic disjoint train/test split of element indices."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    cut = int(round(frac_train * n))
    return GamSplit(train_idx=perm[:cut], test_idx=perm[cut:])


def gam_interaction_frac(
    A: np.ndarray,
    B: np.ndarray,
    M: np.ndarray,
    n_interior: int = 8,
    degree: int = 3,
    frac_train: float = 0.5,
    seed: int = 1234,
    ridge: float = 1e-8,
) -> float:
    """Held-out functional-ANOVA interaction fraction of Var(M).

    Fit separable GAM main-effects ghat_A(A)+ghat_B(B) (cubic splines, `n_interior`
    interior quantile knots per parent) by ridge-stabilised least squares on the
    TRAIN split; return the fraction of held-out M variance left in the residual.

    ~0 for separable M (incl. A^2+B^2); HIGH for genuine joint structure (A*B, XOR).
    """
    a = np.asarray(A, dtype=np.float64).ravel()
    b = np.asarray(B, dtype=np.float64).ravel()
    m = np.asarray(M, dtype=np.float64).ravel()
    n = m.shape[0]
    sp = _split(n, frac_train=frac_train, seed=seed)
    tr, te = sp.train_idx, sp.test_idx

    # Knots from TRAIN parents only (no test leakage into the basis).
    ka = _interior_knots(a[tr], n_interior)
    kb = _interior_knots(b[tr], n_interior)

    # Separable design = [1 | spline(A) | spline(B)]. The two spline blocks are the
    # additive main-effects; the intercept carries the grand mean. NO cross terms,
    # so the column space is exactly { c + g_A(A) + g_B(B) } -- the separable class.
    def design(ai: np.ndarray, bi: np.ndarray) -> np.ndarray:
        XA = _bspline_design(ai, ka, degree)
        XB = _bspline_design(bi, kb, degree)
        ones = np.ones((ai.shape[0], 1))
        return np.column_stack([ones, XA, XB])

    Xtr = design(a[tr], b[tr])
    Xte = design(a[te], b[te])

    # Ridge-stabilised normal equations (B-spline blocks are collinear with the
    # intercept; a tiny ridge keeps the solve well-posed without materially
    # shrinking the fit). Fit on TRAIN, predict on TEST.
    G = Xtr.T @ Xtr
    G[np.diag_indices_from(G)] += ridge * np.trace(G) / G.shape[0]
    coef = np.linalg.solve(G, Xtr.T @ m[tr])

    pred_te = Xte @ coef
    resid_te = m[te] - pred_te
    v = m[te].var()
    return float(resid_te.var() / v) if v > 0 else 0.0


def main_effects_r2_heldout(
    A: np.ndarray, B: np.ndarray, M: np.ndarray, **kw
) -> float:
    """Held-out R^2 of the separable GAM main-effects model (companion diagnostic).

    1 - gam_interaction_frac. High => M well-explained by separable mains (no
    emergent third). Reported alongside the interaction fraction so a low number
    flags 'separable model fits poorly here' rather than silently inflating the
    interaction reading.
    """
    return 1.0 - gam_interaction_frac(A, B, M, **kw)


# ----------------------------------------------------------------------------- #
# Misspecification sweep: the robustness DEMONSTRATION.                          #
#   Vary spline flexibility (knot count). A genuine separable case must stay     #
#   pinned ~0 across the whole axis (more flexibility does NOT manufacture        #
#   held-out interaction); a genuine interaction must stay HIGH and FLAT.        #
#   Creep-up on a floor case = under-resolved main-effect, the caveat made       #
#   visible.                                                                     #
# ----------------------------------------------------------------------------- #
def misspecification_sweep(cases: dict, knot_grid=(0, 2, 4, 8, 16, 24)) -> dict:
    """Return {case_name: [frac at each knot count]} for the given {name:(A,B,M)}."""
    out = {}
    for name, (A, B, M) in cases.items():
        out[name] = [
            gam_interaction_frac(A, B, M, n_interior=k) for k in knot_grid
        ]
    return out


# ----------------------------------------------------------------------------- #
# Calibration harness over the controlled ground-truth cases.                   #
# ----------------------------------------------------------------------------- #
def _controlled_cases() -> dict:
    """The exact controlled cases: seeds A=rng(1), B=rng(2), noise=rng(3), (256,256)."""
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float64)
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float64)
    n = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float64)
    return {
        # name: (A, B, M, expected_verdict)
        "SYN   0.5A+0.5B+0.5*A*B+0.01n (large interaction)": (A, B, 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * n, "HIGH"),
        "ADD   0.5A+0.5B               (separable/affine)": (A, B, 0.5 * A + 0.5 * B, "~0"),
        "SEP   A^2+B^2                 (separable nonlin -> MUST floor)": (A, B, A * A + B * B, "~0"),
        "INT   A*B                     (pure interaction)": (A, B, A * B, "HIGH"),
        "XOR   sign(A)*sign(B)         (canonical PID synergy)": (A, B, np.sign(A) * np.sign(B), "HIGH"),
        "ALLOY 0.5A+0.5B+0.1*A*B       (small interaction)": (A, B, 0.5 * A + 0.5 * B + 0.1 * (A * B), "small>0"),
        "ROT   cos(pi/5)A+sin(pi/5)B   (affine, control)": (A, B, np.cos(np.pi / 5) * A + np.sin(np.pi / 5) * B, "~0"),
        "COPY  A+0.001n                (single-parent null)": (A, B, A + 0.001 * n, "~0"),
    }


if __name__ == "__main__":
    cases = _controlled_cases()

    print("=" * 84)
    print("CALIBRATION -- held-out GAM functional-ANOVA interaction fraction  Var(resid_test)/Var(M_test)")
    print("flexible cubic-spline separable mains (8 interior quantile knots/parent), 50/50 held-out")
    print("=" * 84)
    print(f"{'case':<58s} {'frac':>8s}  {'mainR2':>7s}   expected")
    for name, (A, B, M, exp) in cases.items():
        f = gam_interaction_frac(A, B, M)
        r2 = 1.0 - f
        print(f"{name:<58s} {f:8.4f}  {r2:7.4f}   {exp}")

    print()
    print("=" * 84)
    print("MISSPECIFICATION SWEEP -- held-out interaction fraction vs spline flexibility (knot count)")
    print("robustness claim: separable/affine cases stay PINNED ~0 as flexibility grows;")
    print("genuine-interaction cases stay HIGH and FLAT. Creep-up on a floor case = under-resolved main.")
    print("=" * 84)
    knot_grid = (0, 2, 4, 8, 16, 24)
    sweep_cases = {name: (A, B, M) for name, (A, B, M, _) in cases.items()}
    sweep = misspecification_sweep(sweep_cases, knot_grid)
    print(f"{'case':<58s} " + " ".join(f"k={k:>2}" for k in knot_grid))
    for name in sweep_cases:
        print(f"{name:<58s} " + " ".join(f"{v:5.3f}" for v in sweep[name]))

    print()
    print("Note: k=0 has no interior knots (cubic spline with clamped boundary knots only =")
    print("a single global cubic per parent). Watch ADD/ROT/SEP stay ~0 and INT/XOR/SYN")
    print("stay high across k -- flatness on the floor cases IS the misspecification-robustness.")
