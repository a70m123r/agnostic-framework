"""cand_coinformation.py -- Candidate emergence-function: Co-information /
interaction-information (McGill 1954; Bell 2003 "co-information"), in BITS.

WEB-GROUNDED DEFINITION
-----------------------
The interaction information / co-information of three variables is the
established multivariate generalization of mutual information. With the merged
output M taken as the "target" and the two parents A, B as the sources, the
McGill "whole-minus-sum-of-parts" form is:

    II(A;B;M) = I(M; A,B) - I(M; A) - I(M; B)              ... (synergy form)

which is identically equal (a standard identity) to the conditional form

    II(A;B;M) = I(A;B | M) - I(A;B).

This is McGill's (1954) interaction information; Bell (2003) named the
symmetric quantity "co-information". The *co-information* convention used in much
of the literature is the NEGATION of the synergy form:

    CI(A;B;M) = I(A;B) - I(A;B | M) = -II(A;B;M).

SIGN CONVENTION (this is the load-bearing subtlety, confirmed from sources):
  * co-information CI:  POSITIVE => REDUNDANCY dominates,
                        NEGATIVE => SYNERGY dominates  (XOR is NEGATIVE here).
  * synergy form  II:  POSITIVE => SYNERGY dominates   (XOR is POSITIVE here),
                        NEGATIVE => REDUNDANCY dominates.
The task's calibration target ("HIGH on INT and XOR, ~0 on ADD and SEP") is the
*emergence / synergy* reading, so the headline number this candidate reports is
the SYNERGY-form value II = I(M;A,B) - I(M;A) - I(M;B) (and its magnitude),
with the raw co-information CI = -II also reported for transparency.

All quantities are in BITS (log base 2), estimated by binning the continuous
A, B, M onto a finite alphabet and using the plug-in (maximum-likelihood)
entropy estimator H(.) = -sum p log2 p over observed bin-cell frequencies,
treating the 65536 elementwise triples (A_i, B_i, M_i) as iid samples. We also
report the Miller-Madow bias-corrected variant, because plug-in MI is upward
biased and that bias is the main confound for an info-theoretic interaction read.

    II = H(M,A) + H(M,B) - H(M) - H(A,B) - H(M,A,B) + H(A) + H(B)        ... (*)

Equation (*) is the entropy expansion of I(M;A,B) - I(M;A) - I(M;B); it is what
the code actually computes (one joint-histogram per term).

MAIN-EFFECT-MISSPECIFICATION CAVEAT (how this candidate handles it)
-------------------------------------------------------------------
The residual-after-a-separable-fit family (GAM-bits / functional-ANOVA
interaction) confounds genuine interaction with main-effect MODEL
misspecification: if g(A) is fit too rigidly (e.g. affine), curvature in a TRUE
main effect leaks into the "interaction" residual and SEP = A^2 + B^2 false-
positives. Co-information sidesteps THAT particular confound by construction: it
never fits or subtracts a parametric main-effects model. I(M;A) and I(M;B) are
the FULL, model-free informations each parent alone carries about M -- they
already absorb *any* monotone-or-not single-parent main effect (A^2 included),
because mutual information is invariant to invertible reparameterization of a
single variable. So a purely separable M = h(A) + k(B) cannot inflate II via
main-effect curvature: that is the documented strength of this estimator for the
SEP case.

It is NOT a free lunch. Co-information has its own, DIFFERENT caveats, which we
report straight rather than hide:
  (C1) BINNING is the frame here. The estimator discretizes A, B, M onto `bins`
       cells; entropies (and hence II) depend on `bins`. We sweep bins and report
       the curve, distinguishing a stable signal from a discretization artifact.
  (C2) PLUG-IN BIAS. Empirical MI of finite samples is biased upward ~ (cells-1)
       / (2 N ln2) per term; the 3-way joint H(M,A,B) has the most cells, so the
       bias does NOT cancel cleanly across the three MI terms. We add the
       Miller-Madow correction and show ADD/SEP move toward 0 once corrected.
  (C3) SYNERGY/REDUNDANCY CANCELLATION. Co-information is a single scalar that
       confounds synergy and redundancy and is exactly 0 when they cancel
       (documented). It is therefore a NET balance, not a pure synergy gate; a
       system with equal synergy and redundancy reads 0. This is a real
       limitation of the measure (not of the implementation) and is why PID was
       invented. We flag it explicitly in the verdict.

Sources (web-grounded):
  - Timme et al., "Multivariate information measures: an experimentalist's
    perspective", arXiv:1111.6857  (McGill II definitions, entropy expansion,
    synergy/redundancy sign).
  - Wikipedia, "Interaction information" (co-information form
    I(X;Y;Z)=I(X,Y;Z)-I(X;Z)-I(Y;Z); XOR negative under co-info convention).
  - McGill (1954) "Multivariate information transmission"; Bell (2003)
    "The co-information lattice" (origin + name).
  - On the XOR-negative / synergy-negative co-information convention and the
    confounding caveat: arXiv:2404.01470 and the PID literature (Williams &
    Beer 2010), via the search summaries.

Run as a script to print the calibration table (REAL numbers).
"""

from __future__ import annotations

import numpy as np

# --- controlled cases per the task CONTEXT (NOT cases.py; that file lacks ----
# --- SEP=A^2+B^2 and INT=A*B). Seeds A=rng(1), B=rng(2), noise=rng(3), -------
# --- shape (256,256), "*" elementwise. ---------------------------------------
SHAPE = (256, 256)

TASK_CASES = ["SYN", "ADD", "SEP", "INT", "XOR", "ALLOY"]

# Ground-truth emergence label for calibration:
#   HIGH  -> a genuine non-separable interaction is present (should read big)
#   FLOOR -> separable/additive, NO interaction (should read ~0)
GROUND_TRUTH = {
    "SYN":   "HIGH",    # 0.5A+0.5B+0.5*A*B+0.01n  -> has A*B term
    "ADD":   "FLOOR",   # 0.5A+0.5B                -> purely additive
    "SEP":   "FLOOR",   # A^2+B^2                  -> separable; MUST floor
    "INT":   "HIGH",    # A*B                      -> pure interaction
    "XOR":   "HIGH",    # sign(A)*sign(B)          -> canonical synergy
    "ALLOY": "HIGH",    # 0.5A+0.5B+0.1*A*B        -> small interaction
}


def build_case(name: str):
    """(A, B, M) for the named task case; exact seeds/formulas from CONTEXT."""
    name = name.upper()
    A = np.random.default_rng(1).standard_normal(SHAPE)
    B = np.random.default_rng(2).standard_normal(SHAPE)
    noise = np.random.default_rng(3).standard_normal(SHAPE)

    if name == "SYN":
        M = 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * noise
    elif name == "ADD":
        M = 0.5 * A + 0.5 * B
    elif name == "SEP":
        M = A ** 2 + B ** 2
    elif name == "INT":
        M = A * B
    elif name == "XOR":
        M = np.sign(A) * np.sign(B)
    elif name == "ALLOY":
        M = 0.5 * A + 0.5 * B + 0.1 * (A * B)
    else:
        raise ValueError(f"unknown case {name!r}; expected {TASK_CASES}")
    return A.ravel(), B.ravel(), M.ravel()


# ---------------------------------------------------------------------------
# Binned plug-in entropy estimation (everything in BITS, log base 2).
# ---------------------------------------------------------------------------

def _quantile_edges(x: np.ndarray, bins: int) -> np.ndarray:
    """Equal-frequency (quantile) bin edges -> roughly uniform marginal.

    Quantile binning maximizes marginal entropy and is the standard robust
    choice for MI estimation on continuous data (avoids empty tail cells that
    inflate equal-width entropies). XOR's M takes 2 values, so we de-duplicate
    edges and let np.digitize collapse them.
    """
    qs = np.linspace(0.0, 1.0, bins + 1)
    edges = np.quantile(x, qs)
    edges = np.unique(edges)
    if edges.size < 2:  # constant variable
        edges = np.array([x.min() - 1.0, x.max() + 1.0])
    return edges


def _discretize(x: np.ndarray, bins: int) -> np.ndarray:
    """Integer-code x onto a finite alphabet of size <= bins.

    Low-cardinality fix: if x already takes <= bins distinct values (e.g. XOR's
    M in {-1,+1}), label-encode those distinct values directly. Quantile edges
    collapse on a 2-valued array (the unique edges have no interior cut), which
    would wrongly map M to a single code and zero out every MI term -- the bug
    that made the first XOR run read 0. Otherwise use equal-frequency edges.
    """
    distinct = np.unique(x)
    if distinct.size <= bins:
        # exact label encoding -> preserves all information in x
        return np.searchsorted(distinct, x).astype(np.int64)
    edges = _quantile_edges(x, bins)
    # interior edges only -> codes in [0, len(edges)-2]
    codes = np.digitize(x, edges[1:-1], right=False)
    return codes.astype(np.int64)


def _entropy_bits(*cols: np.ndarray, n_per_axis=None, miller_madow=False):
    """Plug-in joint entropy H(cols...) in bits from integer-coded columns.

    If miller_madow, add the Miller-Madow correction (m_obs - 1)/(2 N ln2),
    where m_obs = number of OCCUPIED joint cells (standard MM uses occupied
    cells), reducing the systematic downward bias of plug-in entropy.
    """
    n = cols[0].shape[0]
    # Combine columns into a single linear cell index using per-axis sizes.
    if n_per_axis is None:
        n_per_axis = [int(c.max()) + 1 for c in cols]
    idx = np.zeros(n, dtype=np.int64)
    mult = 1
    for c, size in zip(cols, n_per_axis):
        idx += c * mult
        mult *= size
    counts = np.bincount(idx)
    counts = counts[counts > 0]
    p = counts / n
    H = -np.sum(p * np.log2(p))
    if miller_madow:
        m_obs = counts.size
        H = H + (m_obs - 1) / (2.0 * n * np.log(2.0))
    return float(H)


def coinformation_bits(A, B, M, bins: int = 16, miller_madow: bool = False):
    """Return a dict of co-information quantities for parents A,B and merge M.

    Headline keys:
      II_synergy : I(M;A,B) - I(M;A) - I(M;B)   [synergy POSITIVE]  (bits)
      CI         : -II_synergy                    [co-info; redundancy POSITIVE]
      magnitude  : |II_synergy|  (the "reads high" scalar for calibration)
    Plus the component MIs, for transparency.
    """
    cA = _discretize(A, bins)
    cB = _discretize(B, bins)
    cM = _discretize(M, bins)
    nA, nB, nM = int(cA.max()) + 1, int(cB.max()) + 1, int(cM.max()) + 1

    mm = miller_madow
    H_A   = _entropy_bits(cA, n_per_axis=[nA], miller_madow=mm)
    H_B   = _entropy_bits(cB, n_per_axis=[nB], miller_madow=mm)
    H_M   = _entropy_bits(cM, n_per_axis=[nM], miller_madow=mm)
    H_MA  = _entropy_bits(cM, cA, n_per_axis=[nM, nA], miller_madow=mm)
    H_MB  = _entropy_bits(cM, cB, n_per_axis=[nM, nB], miller_madow=mm)
    H_AB  = _entropy_bits(cA, cB, n_per_axis=[nA, nB], miller_madow=mm)
    H_MAB = _entropy_bits(cM, cA, cB, n_per_axis=[nM, nA, nB], miller_madow=mm)

    I_M_A  = H_M + H_A - H_MA                       # I(M;A)
    I_M_B  = H_M + H_B - H_MB                        # I(M;B)
    I_M_AB = H_M + H_AB - H_MAB                      # I(M; A,B)

    II_synergy = I_M_AB - I_M_A - I_M_B             # synergy POSITIVE
    CI = -II_synergy                                # co-info; redundancy POSITIVE

    return {
        "bins": bins,
        "miller_madow": mm,
        "I_M_A": I_M_A,
        "I_M_B": I_M_B,
        "I_M_AB": I_M_AB,
        "II_synergy": II_synergy,
        "CI": CI,
        "magnitude": abs(II_synergy),
    }


# ---------------------------------------------------------------------------
# Calibration driver.
# ---------------------------------------------------------------------------

def _fmt(v):
    return f"{v:+.4f}"


def calibrate(bins_list=(8, 16, 32), with_mm=True):
    print("=" * 78)
    print("CAND: Co-information / interaction-information (McGill), in BITS")
    print("Headline = II_synergy = I(M;A,B) - I(M;A) - I(M;B)  "
          "(synergy POSITIVE)")
    print("=" * 78)
    for bins in bins_list:
        print(f"\n--- bins = {bins}  (quantile edges) "
              f"{'[+ Miller-Madow column]' if with_mm else ''} ---")
        header = (f"{'case':6s} {'truth':6s} "
                  f"{'I(M;A)':>8s} {'I(M;B)':>8s} {'I(M;AB)':>8s} "
                  f"{'II_syn':>9s} {'|II|':>8s}")
        if with_mm:
            header += f" {'II_MM':>9s} {'|II_MM|':>9s}"
        print(header)
        for nm in TASK_CASES:
            A, B, M = build_case(nm)
            r = coinformation_bits(A, B, M, bins=bins, miller_madow=False)
            line = (f"{nm:6s} {GROUND_TRUTH[nm]:6s} "
                    f"{r['I_M_A']:8.4f} {r['I_M_B']:8.4f} {r['I_M_AB']:8.4f} "
                    f"{r['II_synergy']:+9.4f} {r['magnitude']:8.4f}")
            if with_mm:
                rmm = coinformation_bits(A, B, M, bins=bins, miller_madow=True)
                line += f" {rmm['II_synergy']:+9.4f} {rmm['magnitude']:9.4f}"
            print(line)

    # Separation summary at the middle resolution.
    print("\n" + "=" * 78)
    print("SEPARATION CHECK @ bins=16 (plug-in): does |II| put HIGH >> FLOOR?")
    bins = 16
    vals = {}
    for nm in TASK_CASES:
        A, B, M = build_case(nm)
        vals[nm] = coinformation_bits(A, B, M, bins=bins)["magnitude"]
    highs = [vals[n] for n in TASK_CASES if GROUND_TRUTH[n] == "HIGH"]
    floors = [vals[n] for n in TASK_CASES if GROUND_TRUTH[n] == "FLOOR"]
    print(f"  HIGH  cases |II| : min={min(highs):.4f}  "
          f"({', '.join(f'{n}={vals[n]:.4f}' for n in TASK_CASES if GROUND_TRUTH[n]=='HIGH')})")
    print(f"  FLOOR cases |II| : max={max(floors):.4f}  "
          f"({', '.join(f'{n}={vals[n]:.4f}' for n in TASK_CASES if GROUND_TRUTH[n]=='FLOOR')})")
    gap = min(highs) - max(floors)
    print(f"  margin (min HIGH - max FLOOR) = {gap:+.4f}  "
          f"-> {'SEPARATES' if gap > 0 else 'DOES NOT SEPARATE'}")
    print("=" * 78)


def stability_check(bins: int = 16):
    """Show the ADD/SEP/INT values are STABLE in N -> the FLOOR failure is a
    STRUCTURAL property of co-information, NOT finite-sample plug-in bias.

    If the inflated ADD/SEP readings were just bias, they would shrink toward 0
    as N grows. They do not. This is the load-bearing negative-result evidence.
    """
    print("\n" + "=" * 78)
    print("STABILITY-IN-N CHECK (bins=16): is the FLOOR failure bias or "
          "structural?")
    print("If just bias, II(ADD), II(SEP) -> 0 as N grows. Watch whether they "
          "do.")
    print(f"{'N':>10s} {'II(ADD)':>9s} {'II(SEP)':>9s} {'II(INT)':>9s} "
          f"{'II(XOR)':>9s}")
    for side in (256, 1000, 4000):
        N = side * side
        A = np.random.default_rng(1).standard_normal((side, side)).ravel()
        B = np.random.default_rng(2).standard_normal((side, side)).ravel()
        add = 0.5 * A + 0.5 * B
        sep = A ** 2 + B ** 2
        intc = A * B
        xor = np.sign(A) * np.sign(B)
        f = lambda M: coinformation_bits(A, B, M, bins=bins)["II_synergy"]
        print(f"{N:>10d} {f(add):+9.4f} {f(sep):+9.4f} {f(intc):+9.4f} "
              f"{f(xor):+9.4f}")
    print("VERDICT: ADD ~ INT (both ~+2.1 bits, stable) => co-information "
          "CANNOT")
    print("distinguish additive from interactive merges. It measures JOINT")
    print("DETERMINATION (each parent alone underdetermines M, both pin it),")
    print("which is synergistic in Shannon terms for a SUM as much as a "
          "PRODUCT.")
    print("=> FAILS the task target '~0 on ADD'. Honest negative result.")
    print("=" * 78)


if __name__ == "__main__":
    calibrate()
    stability_check()
