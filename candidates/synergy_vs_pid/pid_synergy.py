"""
pid_synergy.py -- a tractable, correct Partial Information Decomposition (PID)
synergy estimator for the synergy of a merged tensor M with respect to two
parents (A, B), treating the 65536 elementwise triples (a_i, b_i, m_i) as iid
samples.

WHY THIS FILE EXISTS (the sharpened bar)
----------------------------------------
Cross-model review (GPT-5.5 + Gemini) judged the framework's "witnessed synergy
gate" as "mostly PID synergy reframed / redundant with PID." To answer that we
need a PROPER PID synergy number to compare the witnessed gate against. This file
provides exactly that -- an independent, literature-grounded PID estimator -- so
the companion experiment can ask: does the witnessed gate do anything plain PID
cannot? This module makes NO claim about the gate; it only supplies the PID
baseline and proves the baseline itself is correct (calibration below).

TWO ESTIMATORS (the comparison between them is itself informative)
-----------------------------------------------------------------
(1) GAUSSIAN MMI PID  --  Barrett (2015), "Exploration of synergistic and
    redundant information sharing in static and dynamical Gaussian systems,"
    Phys. Rev. E 91, 052802 (arXiv:1411.2832). For a UNIVARIATE Gaussian target
    and two predictors of arbitrary dimension, EVERY operationally-motivated PID
    collapses to the Minimum-Mutual-Information (MMI) PID:
        Redundancy R(M;A,B) = min( I(M;A), I(M;B) )
        Synergy    S(M;A,B) = I(M;A,B) - max( I(M;A), I(M;B) )
    with Gaussian mutual informations computed in CLOSED FORM from the sample
    covariance via residual variances:
        I(M;A)      = 0.5 * log2( Var(M) / Var(M | A) )
        I(M;A,B)    = 0.5 * log2( Var(M) / Var(M | A,B) )
    where Var(M | .) is the least-squares residual variance of regressing M on
    the conditioning set (an affine fit -- this is the exact Gaussian conditional
    variance). Units: BITS (log base 2).

    This is closed-form, O(N) in the samples, and has NO binning / no estimator
    hyperparameters. It is the headline because it is exact and tractable. Its
    KNOWN blind spot: it sees only the linear (second-order) dependence
    structure, so a purely nonlinear coupling that is second-order-uncorrelated
    with each parent (the XOR archetype: sign(A)*sign(B)) reads ~0 synergy under
    the Gaussian assumption. That blind spot is real and we report it honestly --
    which is exactly WHY we ALSO implement (2).

(2) BINNED WILLIAMS-BEER I_min PID  --  Williams & Beer (2010), "Nonnegative
    decomposition of multivariate information" (arXiv:1004.2515). The original
    PID. Discretize each of A, B, M into `bins` equal-frequency (quantile) bins,
    estimate the joint pmf p(a,b,m) by counting, then:
        specific information   I(m ; X) = sum_x p(x|m) [ log2 1/p(m) - log2 1/p(m|x) ]
        redundancy             I_min(M;{A,B}) = sum_m p(m) * min( I(m;A), I(m;B) )
        synergy                S = I(M;A,B) - I(M;A) - I(M;B) + I_min(M;{A,B})
    This makes NO Gaussian / linearity assumption, so it is the estimator that
    can SEE XOR-type purely-nonlinear synergy. Its cost: discretization bias
    (finite bins, finite samples) -> mutual informations are biased high; we
    therefore (a) use the same bin count everywhere so the bias is shared, and
    (b) report a Miller-Madow-style first-order bias correction on each MI as a
    sanity rail. The synergy is the headline of THIS estimator on XOR.

CALIBRATION (run `python pid_synergy.py`)
-----------------------------------------
A PID synergy estimator is only trustworthy if it passes the canonical checks:
  * XOR  (sign(A)*sign(B))  -> synergy MUST be HIGH (~1 bit; each parent alone
    carries ~0 bit about M, the pair determines M exactly). This is THE PID
    synergy archetype. Only the BINNED estimator can register it (the Gaussian
    estimator is blind to it by construction -- we show both, and that contrast
    is the honest finding about which PID notion is being invoked).
  * INDEPENDENT NOISE (M = fresh noise, unrelated to A,B) -> synergy ~ 0 under
    BOTH estimators (no information of any kind), modulo finite-sample/binning
    bias which we quantify.
Both checks are executed below on real numpy arrays with fixed seeds and the
REAL numbers are printed. Nothing here is hand-waved.

DISCIPLINE: controlled ground-truth numpy only. No torch / HF / network. The
real-substrate (model-merge) run is the explicitly-owed later step, not this.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# ============================================================================
# (1) GAUSSIAN MMI PID  (Barrett 2015, closed form)
# ============================================================================


def _residual_variance(y: np.ndarray, X: np.ndarray | None) -> float:
    """Var(y | X): least-squares residual variance of regressing y on X + intercept.

    For a jointly Gaussian system this is exactly the Gaussian conditional
    variance, so 0.5*log2(Var(y)/Var(y|X)) is the exact Gaussian mutual
    information I(y; X). If X is None, returns Var(y) (no conditioning).

    y : (N,) float ; X : (N, k) float or None.
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    n = y.size
    if X is None:
        return float(np.var(y))  # population variance (ddof=0)
    X = np.asarray(X, dtype=np.float64)
    if X.ndim == 1:
        X = X[:, None]
    # design with intercept
    design = np.concatenate([X, np.ones((n, 1))], axis=1)
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    resid = y - design @ coef
    return float(np.mean(resid * resid))  # mean squared residual = Var(y|X)


def _gauss_mi_bits(var_marg: float, var_cond: float) -> float:
    """I = 0.5 * log2( var_marg / var_cond ), clamped at >= 0.

    Gaussian mutual information from a marginal variance and a conditional
    (residual) variance. Negative values (only from numerical noise when the two
    variances are equal) are clamped to 0; MI is nonnegative.
    """
    if var_cond <= 0.0 or var_marg <= 0.0:
        # var_cond ~ 0 => M perfectly determined by the conditioner (affine) =>
        # infinite Gaussian MI in principle; cap at a large finite value so the
        # arithmetic stays well-defined. This only happens for exactly-affine M.
        if var_marg <= 0.0:
            return 0.0
        if var_cond <= 0.0:
            return float("inf")
    val = 0.5 * np.log2(var_marg / var_cond)
    return float(max(val, 0.0))


@dataclass
class GaussPID:
    I_MA: float        # I(M; A)            bits
    I_MB: float        # I(M; B)            bits
    I_MAB: float       # I(M; A, B)         bits
    redundancy: float  # min(I_MA, I_MB)    bits
    unique_A: float    # I_MA - redundancy  bits
    unique_B: float    # I_MB - redundancy  bits
    synergy: float     # I_MAB - max(I_MA, I_MB)  bits


def gaussian_mmi_pid(A: np.ndarray, B: np.ndarray, M: np.ndarray) -> GaussPID:
    """Closed-form Gaussian (MMI) PID of M w.r.t. (A, B), in BITS.

    Treats the flattened elementwise triples as iid Gaussian samples. Exact for
    jointly Gaussian (A,B,M); for non-Gaussian data it measures the
    SECOND-ORDER (linear) synergy only (its documented blind spot vs XOR).
    """
    a = np.asarray(A, dtype=np.float64).ravel()
    b = np.asarray(B, dtype=np.float64).ravel()
    m = np.asarray(M, dtype=np.float64).ravel()

    var_m = _residual_variance(m, None)
    var_m_given_a = _residual_variance(m, a)
    var_m_given_b = _residual_variance(m, b)
    var_m_given_ab = _residual_variance(m, np.stack([a, b], axis=1))

    I_MA = _gauss_mi_bits(var_m, var_m_given_a)
    I_MB = _gauss_mi_bits(var_m, var_m_given_b)
    I_MAB = _gauss_mi_bits(var_m, var_m_given_ab)

    red = min(I_MA, I_MB)
    syn = I_MAB - max(I_MA, I_MB)
    return GaussPID(
        I_MA=I_MA, I_MB=I_MB, I_MAB=I_MAB,
        redundancy=red,
        unique_A=I_MA - red,
        unique_B=I_MB - red,
        synergy=syn,
    )


# ============================================================================
# (2) BINNED WILLIAMS-BEER I_min PID  (Williams & Beer 2010)
# ============================================================================


def _quantile_bin(x: np.ndarray, bins: int) -> np.ndarray:
    """Equal-frequency (quantile) discretization of x into `bins` integer labels.

    Quantile binning keeps each bin ~equally populated (good plug-in pmf
    behaviour) and is invariant to any monotone transform of x -- which matters
    for the XOR case where M = sign(A)*sign(B) is already discrete.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    # rank-based quantile edges; np.unique guards against duplicate edges when x
    # is already discrete (e.g. +/-1), collapsing to the natural categories.
    qs = np.linspace(0.0, 1.0, bins + 1)
    edges = np.quantile(x, qs)
    edges = np.unique(edges)
    if edges.size <= 2:
        # x takes <=1 effective value after binning -> single category, OR x is
        # 2-valued (XOR target): use the distinct values directly.
        uniq = np.unique(x)
        if uniq.size <= bins:
            lut = {v: i for i, v in enumerate(uniq)}
            return np.array([lut[v] for v in x], dtype=np.int64)
    # assign to interior bins; clip the right edge into the last bin
    labels = np.digitize(x, edges[1:-1], right=False)
    return labels.astype(np.int64)


def _entropy_bits(counts: np.ndarray) -> float:
    """Shannon entropy (bits) of a count vector."""
    counts = counts[counts > 0].astype(np.float64)
    total = counts.sum()
    p = counts / total
    return float(-np.sum(p * np.log2(p)))


def _mi_bits_from_labels(la: np.ndarray, lm: np.ndarray) -> float:
    """Plug-in mutual information I(X;M) in bits from integer label arrays."""
    # joint histogram
    na = int(la.max()) + 1
    nm = int(lm.max()) + 1
    joint = np.zeros((na, nm), dtype=np.int64)
    np.add.at(joint, (la, lm), 1)
    n = joint.sum()
    pj = joint.astype(np.float64) / n
    pa = pj.sum(axis=1, keepdims=True)
    pm = pj.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = pj / (pa * pm)
        terms = np.where(pj > 0, pj * np.log2(ratio), 0.0)
    return float(np.sum(terms))


def _miller_madow(mi_raw: float, n: int, na: int, nm: int, njoint: int) -> float:
    """Miller-Madow first-order bias correction for plug-in MI (bits).

    Bias(MI) ~ (#nonzero_joint - #nonzero_a - #nonzero_m + 1) / (2 N ln2).
    Subtracting it gives a debiased MI; reported as a sanity rail, not the
    headline (the headline synergy is taken on the matched-bin raw estimate).
    """
    corr = (njoint - na - nm + 1) / (2.0 * n * np.log(2.0))
    return mi_raw - corr


@dataclass
class BinnedPID:
    bins: int
    I_MA: float
    I_MB: float
    I_MAB: float
    redundancy: float    # I_min(M;{A,B})
    unique_A: float
    unique_B: float
    synergy: float
    # debiased (Miller-Madow) siblings for the pairwise MIs
    I_MA_mm: float
    I_MB_mm: float
    I_MAB_mm: float
    synergy_mm: float


def binned_williams_beer_pid(A: np.ndarray, B: np.ndarray, M: np.ndarray,
                             bins: int = 8) -> BinnedPID:
    """Williams-Beer I_min PID of M w.r.t. (A,B) via quantile binning, in BITS.

    Steps:
      1. discretize A, B, M into `bins` quantile bins (labels la, lb, lm).
      2. estimate the joint pmf p(a,b,m) by counting.
      3. specific information I(m; X) = sum_x p(x|m)[log2 1/p(m) - log2 1/p(m|x)].
      4. redundancy I_min = sum_m p(m) min( I(m;A), I(m;B) ).
      5. synergy = I(M;A,B) - I(M;A) - I(M;B) + I_min.

    No Gaussian assumption -> this is the estimator that registers XOR synergy.
    """
    la = _quantile_bin(A, bins)
    lb = _quantile_bin(B, bins)
    lm = _quantile_bin(M, bins)
    n = la.size

    na, nb, nm = int(la.max()) + 1, int(lb.max()) + 1, int(lm.max()) + 1

    # --- pairwise MIs (for the uniques/synergy arithmetic and debias rail) ---
    I_MA = _mi_bits_from_labels(la, lm)
    I_MB = _mi_bits_from_labels(lb, lm)

    # --- joint source (A,B) as a composite label, then I(M; (A,B)) ---
    lab = la * nb + lb  # composite joint-source label in [0, na*nb)
    I_MAB = _mi_bits_from_labels(lab, lm)

    # --- specific information I(m; A) and I(m; B), per target value m ---
    # p(m), p(m|a) etc. from joint counts.
    # joint counts for (A,M) and (B,M)
    jam = np.zeros((na, nm), dtype=np.int64)
    np.add.at(jam, (la, lm), 1)
    jbm = np.zeros((nb, nm), dtype=np.int64)
    np.add.at(jbm, (lb, lm), 1)

    pm = jam.sum(axis=0).astype(np.float64) / n        # p(m), shape (nm,)
    # p(m | a) = jam[a,m] / sum_m jam[a,m]
    pa = jam.sum(axis=1).astype(np.float64) / n        # p(a)
    pb = jbm.sum(axis=1).astype(np.float64) / n        # p(b)

    def specific_info_per_m(jxm, px):
        """Return array I(m; X) for each m: sum_x p(x|m)[ -log2 p(m) + log2 p(m|x) ].

        Uses p(x|m) = jxm[x,m]/colsum_m, p(m|x) = jxm[x,m]/rowsum_x.
        """
        nx = jxm.shape[0]
        colsum = jxm.sum(axis=0).astype(np.float64)    # counts per m -> N*p(m)
        rowsum = jxm.sum(axis=1).astype(np.float64)    # counts per x -> N*p(x)
        Ispec = np.zeros(nm, dtype=np.float64)
        for mi in range(nm):
            if colsum[mi] <= 0:
                continue
            pm_val = colsum[mi] / n
            acc = 0.0
            for xi in range(nx):
                cxm = jxm[xi, mi]
                if cxm <= 0:
                    continue
                p_x_given_m = cxm / colsum[mi]
                p_m_given_x = cxm / rowsum[xi]
                # specific info contribution: p(x|m) * [ log2 1/p(m) - log2 1/p(m|x) ]
                acc += p_x_given_m * (np.log2(1.0 / pm_val) - np.log2(1.0 / p_m_given_x))
            Ispec[mi] = acc
        return Ispec

    Ispec_A = specific_info_per_m(jam, pa)
    Ispec_B = specific_info_per_m(jbm, pb)

    # redundancy I_min = sum_m p(m) * min( I(m;A), I(m;B) )
    redundancy = float(np.sum(pm * np.minimum(Ispec_A, Ispec_B)))

    unique_A = I_MA - redundancy
    unique_B = I_MB - redundancy
    synergy = I_MAB - I_MA - I_MB + redundancy

    # --- Miller-Madow debias rail on the three MIs ---
    nz_am = int(np.count_nonzero(jam))
    nz_bm = int(np.count_nonzero(jbm))
    jabm = np.zeros((na * nb, nm), dtype=np.int64)
    np.add.at(jabm, (lab, lm), 1)
    nz_abm = int(np.count_nonzero(jabm))
    nz_a = int(np.count_nonzero(jam.sum(axis=1)))
    nz_b = int(np.count_nonzero(jbm.sum(axis=1)))
    nz_ab = int(np.count_nonzero(jabm.sum(axis=1)))
    nz_m = int(np.count_nonzero(pm))

    I_MA_mm = _miller_madow(I_MA, n, nz_a, nz_m, nz_am)
    I_MB_mm = _miller_madow(I_MB, n, nz_b, nz_m, nz_bm)
    I_MAB_mm = _miller_madow(I_MAB, n, nz_ab, nz_m, nz_abm)
    # debiased redundancy is bounded by min of debiased pairwise MIs as a proxy;
    # synergy_mm uses the debiased joint minus debiased uniques+redundancy floor.
    redundancy_mm = min(redundancy, I_MA_mm, I_MB_mm)
    synergy_mm = I_MAB_mm - I_MA_mm - I_MB_mm + redundancy_mm

    return BinnedPID(
        bins=bins,
        I_MA=I_MA, I_MB=I_MB, I_MAB=I_MAB,
        redundancy=redundancy, unique_A=unique_A, unique_B=unique_B,
        synergy=synergy,
        I_MA_mm=I_MA_mm, I_MB_mm=I_MB_mm, I_MAB_mm=I_MAB_mm,
        synergy_mm=synergy_mm,
    )


# ============================================================================
# Convenience: one call -> both PID synergies for a case
# ============================================================================


def pid_synergy_both(A, B, M, bins: int = 8):
    """Return (GaussPID, BinnedPID) for M w.r.t (A,B). The two synergy numbers
    are .synergy on each. Gaussian = linear/second-order synergy (closed form);
    Binned = full (model-free) synergy incl. nonlinear (the XOR-sensitive one)."""
    return gaussian_mmi_pid(A, B, M), binned_williams_beer_pid(A, B, M, bins=bins)


# ============================================================================
# CALIBRATION  (run as a script)
# ============================================================================

def _build_calibration_arrays():
    """The exact controlled-case parents + the two calibration targets.

    A = rng(1).standard_normal, B = rng(2).standard_normal, noise = rng(3),
    shape (256,256) f32 -- identical seeding to cases.py so the calibration is
    on the SAME ground truth the experiment uses.
    """
    SHAPE = (256, 256)
    A = np.random.default_rng(1).standard_normal(SHAPE).astype(np.float32)
    B = np.random.default_rng(2).standard_normal(SHAPE).astype(np.float32)
    noise = np.random.default_rng(3).standard_normal(SHAPE).astype(np.float32)

    # XOR archetype: each parent's SIGN, product as +/-1. Each parent alone is
    # (by symmetry of the standard normal about 0) ~independent of M; the PAIR
    # determines M exactly. THE canonical PID-synergy case.
    XOR = (np.sign(A) * np.sign(B)).astype(np.float32)

    # Independent-noise target: M unrelated to A,B (fresh seed). Synergy ~ 0.
    NOISE_M = np.random.default_rng(99).standard_normal(SHAPE).astype(np.float32)

    return A, B, XOR, NOISE_M


def _run_calibration():
    A, B, XOR, NOISE_M = _build_calibration_arrays()
    N = A.size

    print("=" * 78)
    print("PID SYNERGY ESTIMATOR -- CALIBRATION (real numbers, fixed seeds)")
    print(f"N = {N} iid elementwise samples; shape (256,256) f32")
    print("Gaussian MMI PID = Barrett 2015 (linear/2nd-order synergy, closed form)")
    print("Binned Williams-Beer I_min PID = model-free synergy (XOR-sensitive)")
    print("=" * 78)

    # ---- XOR: the synergy archetype. Sanity-check the marginals first. ----
    print("\n[XOR]  M = sign(A)*sign(B) as +/-1  (each parent ~0 info alone; pair => M)")
    gx, bx = pid_synergy_both(A, B, XOR, bins=8)
    print("  -- single-parent dependence (should be ~0 for EACH parent alone) --")
    print(f"     Gaussian  I(M;A)={gx.I_MA:.5f}  I(M;B)={gx.I_MB:.5f}  bits")
    print(f"     Binned    I(M;A)={bx.I_MA:.5f}  I(M;B)={bx.I_MB:.5f}  bits "
          f"(MillerMadow {bx.I_MA_mm:.5f} / {bx.I_MB_mm:.5f})")
    print("  -- joint (pair) information (should be ~1 bit: pair determines M) --")
    print(f"     Gaussian  I(M;A,B)={gx.I_MAB:.5f}  bits   <-- BLIND: linear corr only")
    print(f"     Binned    I(M;A,B)={bx.I_MAB:.5f}  bits   (MillerMadow {bx.I_MAB_mm:.5f})")
    print("  -- SYNERGY --")
    print(f"     Gaussian  synergy = {gx.synergy:.5f} bits   "
          f"(EXPECTED ~0: Gaussian PID cannot see sign-XOR -- documented blind spot)")
    print(f"     Binned    synergy = {bx.synergy:.5f} bits   "
          f"(MillerMadow {bx.synergy_mm:.5f})  <-- MUST BE HIGH (~1 bit)")

    # ---- independent noise: synergy must be ~0 under both ----
    print("\n[INDEP NOISE]  M = fresh independent normal (unrelated to A,B)")
    gn, bn = pid_synergy_both(A, B, NOISE_M, bins=8)
    print(f"     Gaussian  I(M;A)={gn.I_MA:.5f} I(M;B)={gn.I_MB:.5f} "
          f"I(M;A,B)={gn.I_MAB:.5f}  synergy={gn.synergy:.5f} bits")
    print(f"     Binned    I(M;A)={bn.I_MA:.5f} I(M;B)={bn.I_MB:.5f} "
          f"I(M;A,B)={bn.I_MAB:.5f}  synergy={bn.synergy:.5f} bits")
    print(f"     Binned (MillerMadow debiased) synergy = {bn.synergy_mm:.5f} bits  "
          f"(EXPECTED ~0 -- finite-bin bias quantified by the debias gap)")

    # ---- a continuous-Gaussian POSITIVE control so the Gaussian estimator is
    #      shown to register synergy when it IS linear/2nd-order ----
    # M = A*B (product of two independent normals): genuinely synergistic AND
    # carries 2nd-order structure via |.|; still partly nonlinear. Plus a clean
    # linear-synergy case where I(M;A,B) > max single: M = A + B (additive ->
    # synergy 0 under MMI by construction, a useful nonzero-MI/zero-syn check).
    print("\n[POS CONTROL  M=A+B]  additive: large pairwise MI but MMI synergy ~0")
    ADD = (A + B).astype(np.float32)
    ga, ba = pid_synergy_both(A, B, ADD, bins=8)
    print(f"     Gaussian  I(M;A)={ga.I_MA:.4f} I(M;B)={ga.I_MB:.4f} "
          f"I(M;A,B)={ga.I_MAB:.4f}  synergy={ga.synergy:.5f} bits")
    print(f"     Binned    synergy={ba.synergy:.5f} bits (MillerMadow {ba.synergy_mm:.5f})")
    print("     (additive M: each parent already carries half; knowing the pair adds")
    print("      the OTHER half as UNIQUE info, not synergy -> MMI synergy ~0. This is")
    print("      the key contrast the experiment will probe vs the witnessed gate.)")

    print("\n" + "=" * 78)
    print("CALIBRATION VERDICT")
    print("=" * 78)
    xor_ok = bx.synergy > 0.5  # XOR binned synergy must be high (~1 bit)
    noise_ok = abs(bn.synergy_mm) < 0.05 and abs(gn.synergy) < 0.02
    print(f"  XOR binned synergy HIGH (>0.5 bit):           {bx.synergy:.4f}  -> {xor_ok}")
    print(f"  INDEP-NOISE synergy ~0 (Gaussian & binned-MM): "
          f"G={gn.synergy:.4f}, B_mm={bn.synergy_mm:.4f}  -> {noise_ok}")
    print(f"  Gaussian XOR synergy ~0 (documented blind spot): {gx.synergy:.4f}")
    print(f"\n  ESTIMATOR CALIBRATED (XOR high AND noise ~0): {xor_ok and noise_ok}")
    return {
        "xor_binned_synergy": bx.synergy,
        "xor_binned_synergy_mm": bx.synergy_mm,
        "xor_gaussian_synergy": gx.synergy,
        "noise_gaussian_synergy": gn.synergy,
        "noise_binned_synergy": bn.synergy,
        "noise_binned_synergy_mm": bn.synergy_mm,
        "xor_ok": xor_ok,
        "noise_ok": noise_ok,
    }


if __name__ == "__main__":
    _run_calibration()
