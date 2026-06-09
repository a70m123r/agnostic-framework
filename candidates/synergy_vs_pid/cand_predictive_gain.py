"""cand_predictive_gain.py -- candidate emergence-function: HELD-OUT PREDICTIVE GAIN.

WHAT THIS MEASURES
------------------
The "emergence" of a child M from parents A, B is operationalized as: how much
better can you PREDICT M on UNSEEN data with a model that is allowed to use the
JOINT (A,B) structure than with one restricted to a SEPARABLE additive form
f(A)+g(B)?  This is the GPT "out-of-sample-predictability" suggestion:

    gain_R2 = R2_oos(joint model)  -  R2_oos(additive/GAM model)

Both models are fit on TRAIN folds and scored on HELD-OUT TEST folds (K-fold CV
over the 65536 elementwise triples, treated as iid samples per the brief). The
interaction "earns its keep" only if it improves prediction on data the model
never saw -- a genuinely emergent joint structure does; a separable one (even a
highly nonlinear one) does not, because the additive model can already absorb it.

WHY THIS IS THE RIGHT SHAPE FOR THE MISSPECIFICATION CAVEAT
----------------------------------------------------------
The deep caveat (thread state #4): "interaction-as-residual-after-a-separable-fit
CONFOUNDS genuine interaction with main-effect MODEL MISSPECIFICATION." A residual
gate that subtracts a WEAK main-effects model (e.g. affine) reads the curvature of
A^2 as if it were interaction (the confirmed A^2+B^2 false-positive). Held-out
predictive gain defuses this in two independent ways:

  (1) The additive baseline is itself FLEXIBLE and PROPERLY SPECIFIED: its main
      effects E[M|A], E[M|B] are nonparametric bin-means with the SAME per-axis
      resolution the joint model gets. So any separable f(A)+g(B) the joint grid
      can represent, the additive model can ALSO represent -- the gain cancels by
      construction, not by luck. Misspecification of the mains lowers BOTH R2s
      together, leaving the gain ~ unchanged. (Resolution sweep below confirms
      SEP stays ~0 as bins -> fine.)

  (2) Scoring is OUT OF SAMPLE. A joint model flexible enough to chase separable
      curvature (or noise) as spurious "interaction" overfits the TRAIN fold and
      is PENALIZED on the TEST fold: its held-out R2 does not beat the additive
      model's, so the gain stays ~0. In-sample residual measures cannot do this --
      extra joint parameters always reduce in-sample residual. Held-out CV is the
      standard, principled cure for "did the extra structure earn its keep."

So the gain is positive iff there is joint structure that (a) no same-resolution
separable model can express AND (b) GENERALIZES to unseen samples. That is exactly
"genuine, non-separable, real (not overfit) interaction."

MODELS (pure numpy -- controlled ground-truth, NO torch / HF / sklearn / network)
--------------------------------------------------------------------------------
  * additive / GAM:  Hhat_add(a,b) = mu_A[bin(a)] + mu_B[bin(b)] - grand_mean,
                     where mu_A, mu_B, grand_mean are TRAIN-fold means over
                     `bins` equal-frequency (quantile) bins per axis. This is the
                     held-out backfit of a 2-term GAM with piecewise-constant
                     smoothers -- the best separable predictor at this resolution.
  * joint / 2D smoother:  Hhat_joint(a,b) = TRAIN-fold mean of M in the 2D cell
                     (bin(a), bin(b)). The nonparametric stand-in for a
                     gradient-boosted-tree / 2D smoother: it can fit ANY function
                     of (A,B) at the grid resolution, including pure interaction
                     (A*B, XOR) that no separable model can touch. TEST cells
                     unseen/empty in TRAIN BACK OFF to the additive prediction
                     (leak-free: a real GBT would do the analogous smoothing), so
                     the joint model is never WORSE than additive by construction
                     except for sampling noise -- which is the honest null.

R2_oos is pooled across folds: 1 - SS_res_test / SS_tot_test (SS_tot about the
TRAIN grand mean, so a model that ignores everything scores ~0, not by cheating
on the test mean). For the binary XOR target we ALSO report a log-loss gain.

CALIBRATION TARGET: gain HIGH on INT (A*B) and XOR; gain ~0 on ADD and SEP
(A^2+B^2). Run `python cand_predictive_gain.py` for the real numbers.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Reuse the EXACT quantile binner the PID / interaction gates use, so this
# candidate conditions on the SAME bins as its siblings (no divergent binning).
from pid_synergy import _quantile_bin

DEFAULT_BINS = 8          # per-axis bins, == PID / interaction-gate default.
DEFAULT_FOLDS = 5         # K-fold CV.
SEED_CV = 1234            # fold-assignment RNG (independent of the data seeds).


# ----------------------------------------------------------------------------
# Train-fold bin means (the building block of both models).
# ----------------------------------------------------------------------------

def _group_means(values: np.ndarray, labels: np.ndarray, n_lab: int,
                 fallback: float) -> np.ndarray:
    """Mean of `values` within each label in [0, n_lab); empty labels -> fallback.

    The plug-in conditional mean E[values | label], used for E[M|A], E[M|B], and
    the 2D-cell mean E[M|A,B]. Empty groups (a cell present in TEST but absent in
    TRAIN) take `fallback` so the predictor is always defined and leak-free.
    """
    sums = np.zeros(n_lab, dtype=np.float64)
    cnts = np.zeros(n_lab, dtype=np.float64)
    np.add.at(sums, labels, values)
    np.add.at(cnts, labels, 1.0)
    out = np.full(n_lab, fallback, dtype=np.float64)
    nz = cnts > 0
    out[nz] = sums[nz] / cnts[nz]
    return out


@dataclass
class GainResult:
    bins: int
    folds: int
    r2_add: float        # pooled out-of-sample R2 of the additive/GAM model
    r2_joint: float      # pooled out-of-sample R2 of the joint 2D model
    gain_r2: float       # r2_joint - r2_add  (THE measure)
    logloss_add: float   # binary log-loss of additive model (nan if M not binary)
    logloss_joint: float
    logloss_gain: float  # logloss_add - logloss_joint (>0 == joint better; nan if M not binary)
    is_binary: bool


def _is_binary(M: np.ndarray) -> bool:
    u = np.unique(M)
    return u.size <= 2


def predictive_gain(A, B, M, bins: int = DEFAULT_BINS, folds: int = DEFAULT_FOLDS,
                    seed: int = SEED_CV) -> GainResult:
    """Held-out predictive gain of a JOINT model over an ADDITIVE/GAM model.

    Returns a GainResult; the headline number is `.gain_r2` (pooled out-of-sample
    R2 of the 2D joint model minus that of the same-resolution additive model).
    For a 2-valued target (XOR) `.logloss_gain` is also populated.

    Both models use the SAME per-axis quantile bins. Bin EDGES are computed once
    on the full sample (a fixed, data-independent discretization of the feature
    space -- the analogue of fixing tree split candidates); only the CELL/BIN
    MEANS (the model parameters) are fit per TRAIN fold and scored on TEST. This
    is the standard CV protocol: the hypothesis space is fixed, the fitted values
    are held-out.
    """
    Af = np.asarray(A, dtype=np.float64).ravel()
    Bf = np.asarray(B, dtype=np.float64).ravel()
    Mf = np.asarray(M, dtype=np.float64).ravel()
    n = Mf.size

    # Fixed discretization of the feature space (edges from the full sample).
    la = _quantile_bin(Af, bins)
    lb = _quantile_bin(Bf, bins)
    na = int(la.max()) + 1
    nb = int(lb.max()) + 1
    cell = la * nb + lb            # flat 2D-cell index in [0, na*nb)
    ncell = na * nb

    binary = _is_binary(Mf)
    EPS = 1e-6                      # log-loss clip for probabilities

    rng = np.random.default_rng(seed)
    fold_id = rng.integers(0, folds, size=n)

    # Pooled out-of-sample accumulators.
    ss_res_add = ss_res_joint = ss_tot = 0.0
    ll_add = ll_joint = 0.0        # summed binary log-loss over test points
    n_test_total = 0

    for k in range(folds):
        test = fold_id == k
        train = ~test
        if not test.any() or not train.any():
            continue

        gm = float(Mf[train].mean())                       # TRAIN grand mean

        # --- additive / GAM main effects on TRAIN ---
        muA = _group_means(Mf[train], la[train], na, gm)   # E[M|A] (train)
        muB = _group_means(Mf[train], lb[train], nb, gm)   # E[M|B] (train)
        pred_add = muA[la[test]] + muB[lb[test]] - gm

        # --- joint 2D-cell means on TRAIN; empty test cells back off to additive ---
        muC = _group_means(Mf[train], cell[train], ncell, np.nan)
        pred_joint = muC[cell[test]]
        empty = np.isnan(pred_joint)
        pred_joint = np.where(empty, pred_add, pred_joint)  # leak-free backoff

        y = Mf[test]
        # SS_tot about the TRAIN grand mean (the no-skill baseline a model must beat).
        ss_tot += float(np.sum((y - gm) ** 2))
        ss_res_add += float(np.sum((y - pred_add) ** 2))
        ss_res_joint += float(np.sum((y - pred_joint) ** 2))
        n_test_total += int(test.sum())

        if binary:
            # Map M to {0,1}; predictions are conditional means already in [lo,hi]
            # -> rescale to a probability of the "high" class, clip, log-loss.
            lo, hi = float(Mf.min()), float(Mf.max())
            span = (hi - lo) if hi > lo else 1.0
            yb = (y - lo) / span
            pa = np.clip((pred_add - lo) / span, EPS, 1 - EPS)
            pj = np.clip((pred_joint - lo) / span, EPS, 1 - EPS)
            ll_add += float(-np.sum(yb * np.log(pa) + (1 - yb) * np.log(1 - pa)))
            ll_joint += float(-np.sum(yb * np.log(pj) + (1 - yb) * np.log(1 - pj)))

    r2_add = 1.0 - ss_res_add / ss_tot if ss_tot > 0 else 0.0
    r2_joint = 1.0 - ss_res_joint / ss_tot if ss_tot > 0 else 0.0
    if binary and n_test_total > 0:
        la_add = ll_add / n_test_total
        la_joint = ll_joint / n_test_total
        ll_gain = la_add - la_joint
    else:
        la_add = la_joint = ll_gain = float("nan")

    return GainResult(
        bins=bins, folds=folds,
        r2_add=r2_add, r2_joint=r2_joint, gain_r2=r2_joint - r2_add,
        logloss_add=la_add, logloss_joint=la_joint, logloss_gain=ll_gain,
        is_binary=binary,
    )


# ----------------------------------------------------------------------------
# Calibration battery -- REAL numbers only. Run `python cand_predictive_gain.py`.
# ----------------------------------------------------------------------------

def _battery():
    """Controlled cases on the EXACT cases.py seeds (A=rng1,B=rng2,noise=rng3)."""
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float32)
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float32)
    noise = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float32)
    cases = [
        # label, group, M, expected
        ("SYN  0.5A+0.5B+0.5AB",  "genuine",   0.5*A + 0.5*B + 0.5*(A*B) + 0.01*noise, "HIGH"),
        ("ADD  0.5A+0.5B",        "separable", 0.5*A + 0.5*B,                          "~0"),
        ("SEP  A^2+B^2",          "separable", A*A + B*B,                              "~0"),
        ("INT  A*B",              "genuine",   A*B,                                    "HIGH"),
        ("XOR  sign(A)*sign(B)",  "genuine",   np.sign(A)*np.sign(B),                  "HIGH"),
        ("ALLOY 0.5A+0.5B+0.1AB", "genuine",   0.5*A + 0.5*B + 0.1*(A*B),              "small+"),
        # extra separable falsifiers the measure MUST also floor (misspec stress)
        ("A^3+B^3",               "separable", A**3 + B**3,                            "~0"),
        ("|A|+|B|",               "separable", np.abs(A) + np.abs(B),                  "~0"),
        ("sin(A)+cos(B)",         "separable", np.sin(A) + np.cos(B),                  "~0"),
        # extra genuine interactions the measure SHOULD flag
        ("max(A,B)",              "genuine",   np.maximum(A, B),                       "HIGH"),
    ]
    return A, B, [(l, g, M.astype(np.float32), e) for (l, g, M, e) in cases]


if __name__ == "__main__":
    A, B, battery = _battery()

    print("=" * 100)
    print("CANDIDATE: HELD-OUT PREDICTIVE GAIN  (out-of-sample R2[joint] - R2[additive/GAM])")
    print(f"  {DEFAULT_FOLDS}-fold CV over 65536 elementwise triples; "
          f"per-axis bins={DEFAULT_BINS}; pure-numpy plug-in models (no sklearn).")
    print("  joint = 2D-cell conditional mean ; additive = E[M|A]+E[M|B]-E[M] ; "
          "both fit on TRAIN, scored on TEST.")
    print("=" * 100)
    print(f"  {'case':24} {'group':9} {'R2_add':>9} {'R2_joint':>9} "
          f"{'GAIN_R2':>10} {'ll_gain':>9}  expect")
    rows = {}
    for lbl, grp, M, exp in battery:
        r = predictive_gain(A, B, M)
        rows[lbl] = r
        llg = "" if (r.logloss_gain != r.logloss_gain) else f"{r.logloss_gain:>9.4f}"
        print(f"  {lbl:24} {grp:9} {r.r2_add:>9.4f} {r.r2_joint:>9.4f} "
              f"{r.gain_r2:>10.5f} {llg:>9}  {exp}")

    print("\n" + "=" * 100)
    print("CALIBRATION HEADLINE (the four required cases)")
    print("=" * 100)
    for lbl in ["INT  A*B", "XOR  sign(A)*sign(B)", "ADD  0.5A+0.5B", "SEP  A^2+B^2"]:
        r = rows[lbl]
        print(f"  {lbl:24} GAIN_R2 = {r.gain_r2:+.5f}   "
              f"(R2_add={r.r2_add:.4f}  R2_joint={r.r2_joint:.4f})")

    # --- MISSPECIFICATION CAVEAT: resolution sweep. The whole point is that a
    #     SEPARABLE case stays ~0 as the per-axis resolution rises (the additive
    #     model keeps pace with the joint model), while a GENUINE interaction
    #     stays large. If SEP A^2+B^2 climbed with bins, the measure would be
    #     re-importing the misspecification confound -- it must NOT. ---
    print("\n" + "=" * 100)
    print("MISSPECIFICATION STRESS: GAIN_R2 vs per-axis bin count")
    print("  (separable cases must stay ~0 as bins->fine; genuine interactions stay large.)")
    print("=" * 100)
    bin_grid = [4, 8, 12, 16, 24]
    sweep_cases = ["SEP  A^2+B^2", "|A|+|B|", "ADD  0.5A+0.5B",
                   "INT  A*B", "XOR  sign(A)*sign(B)", "SYN  0.5A+0.5B+0.5AB"]
    print(f"  {'case':24} " + " ".join(f"bins={k:<2}".rjust(11) for k in bin_grid))
    for lbl in sweep_cases:
        M = next(m for (l, g, m, e) in battery if l == lbl)
        vals = [predictive_gain(A, B, M, bins=k).gain_r2 for k in bin_grid]
        print(f"  {lbl:24} " + " ".join(f"{v:>11.5f}" for v in vals))
    print("\n  Read: SEP / |A|+|B| / ADD rows ~ 0 (and NOT growing) across resolution")
    print("  = the held-out gain is NOT fooled by main-effect curvature (the A^2+B^2 bug).")
