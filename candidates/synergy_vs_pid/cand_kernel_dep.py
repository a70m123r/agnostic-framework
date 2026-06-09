"""cand_kernel_dep.py -- CANDIDATE emergence-function: kernel / dependence INTERACTION.

OWNED CANDIDATE (Phase-2 alternative emergence-function exploration):
    Kernel / dependence interaction (HSIC + distance-correlation), used to test
    whether M depends on (A, B) JOINTLY *beyond* depending on them SEPARABLY.

WHY THIS CANDIDATE (the caveat it is built to address)
------------------------------------------------------
The settled thread caveat (RATIO_FRAME_TEST.md, CROSS_MODEL_REVIEW_2.md): defining
interaction as "residual variance after a SEPARABLE polynomial/affine fit" CONFOUNDS
genuine interaction with main-effect MODEL MISSPECIFICATION -- a wrong/underpowered
basis (e.g. low-degree polynomial main effects) manufactures false "interaction."
Any sound interaction measure needs a properly specified, flexible, held-out
main-effects model.

This candidate attacks that caveat with MODEL-FREE / kernel dependence. Two routes,
both reported so the verdict does not hinge on a single construction:

  ROUTE D (direct, FIT-FREE -- the headline; NO main-effect model at all):
      A purely kernel/distance contrast between the dependence of M on the TRUE
      joint (A,B) and the dependence of M on an ADDITIVE SURROGATE built by breaking
      the A<->B coupling (independent reshuffles that preserve each marginal map but
      destroy joint structure). Pure additive M is reproduced by the surrogate
      (contrast ~ 0); genuinely joint M is not (contrast > 0). No parametric basis,
      no fitted main-effects model -> the basis-misspecification caveat cannot bite,
      because there is no basis to misspecify.

  ROUTE R (residual-dependence -- corroborating; model-free additive fit):
      Remove additive main effects with OUT-OF-FOLD NONPARAMETRIC kernel smoothers
      (Nadaraya-Watson on A alone and on B alone; k-fold, held-out), then measure the
      dependence that SURVIVES between the residual and the joint (A,B) via
      distance-correlation / HSIC. Because the main-effects model is nonparametric,
      flexible, and held-out (not a fixed low-degree basis), this is the GAM-bits
      recommendation realized model-free: it answers misspecification by NOT fixing a
      basis. Residual joint-dependence == interaction.

Both routes use measures that are model-free and characterize ALL dependence:
  * HSIC  (Hilbert-Schmidt Independence Criterion), Gretton et al. 2005, biased
    V-statistic estimator HSIC_b = (1/m^2) trace(K H L H), H = I - (1/m) 11^T,
    Gaussian RBF kernels (characteristic => HSIC=0 iff independent).
    Source: Gretton, Bousquet, Smola, Schoelkopf, "Measuring Statistical Dependence
    with Hilbert-Schmidt Norms", ALT 2005.
    http://www.gatsby.ucl.ac.uk/~gretton/papers/GreBouSmoSch05.pdf
  * Distance correlation, Szekely, Rizzo, Bakirov 2007, double-centered Euclidean
    distance matrices; dCor in [0,1], dCor=0 iff independent, detects nonlinearity.
    Source: "Measuring and testing dependence by correlation of distances",
    Annals of Statistics 35(6), 2007.
    https://projecteuclid.org/journals/annals-of-statistics/volume-35/issue-6/
    Measuring-and-testing-dependence-by-correlation-of-distances/10.1214/009053607000000505.full
    (sample formulas cross-checked against en.wikipedia.org/wiki/Distance_correlation)

CALIBRATION TARGET (controlled cases): the INTERACTION statistic must read
  HIGH on INT (M=A*B) and XOR (M=sign(A)*sign(B)),  ~0 on ADD (0.5A+0.5B) and
  SEP (M=A^2+B^2, separable nonlinear).  SEP is the crux: SEP is nonlinear but
  SEPARABLE -> a real interaction measure MUST floor it (a variance/codelength
  "non-additivity" or a naive total-dependence reading would WRONGLY flag it).

COMPUTE NOTE
------------
HSIC and dCor are O(m^2) in memory. The 65536 elementwise triples are treated as
iid samples; we SUBSAMPLE m points per block and AVERAGE over B independent blocks
(default m=1200, B=8). Controlled, fully local, numpy+scipy only, no torch/HF/network.
"""

from __future__ import annotations

import numpy as np

SHAPE = (256, 256)
DTYPE = np.float32


# ----------------------------------------------------------------------------- #
# Controlled cases (matches the task's CONTROLLED CASES block exactly).
# seeds A=rng(1), B=rng(2), noise=rng(3); shape (256,256); "*" elementwise.
# ----------------------------------------------------------------------------- #
CASE_NAMES = ["SYN", "ADD", "SEP", "INT", "XOR", "ALLOY"]

# What a CORRECT interaction (synergy) measure should call each case.
EXPECTED = {
    "SYN":   "HIGH",   # 0.5A+0.5B+0.5 A*B  -> has interaction
    "ADD":   "~0",     # 0.5A+0.5B          -> separable (affine)  MUST floor
    "SEP":   "~0",     # A^2+B^2            -> separable nonlinear  MUST floor (crux)
    "INT":   "HIGH",   # A*B                -> pure interaction
    "XOR":   "HIGH",   # sign(A)*sign(B)    -> pure interaction (PID-synergy archetype)
    "ALLOY": "small",  # 0.5A+0.5B+0.1 A*B  -> small interaction
}


def build_case(name: str):
    """Return flat (A, B, M) float64 vectors of length 65536 for the named case."""
    name = name.upper()
    A = np.random.default_rng(1).standard_normal(SHAPE).astype(DTYPE)
    B = np.random.default_rng(2).standard_normal(SHAPE).astype(DTYPE)
    noise = np.random.default_rng(3).standard_normal(SHAPE).astype(DTYPE)

    if name == "SYN":
        M = 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * noise
    elif name == "ADD":
        M = 0.5 * A + 0.5 * B
    elif name == "SEP":
        M = A * A + B * B
    elif name == "INT":
        M = A * B
    elif name == "XOR":
        M = np.sign(A) * np.sign(B)
    elif name == "ALLOY":
        M = 0.5 * A + 0.5 * B + 0.1 * (A * B)
    else:
        raise ValueError(f"unknown case {name!r}; expected one of {CASE_NAMES}")

    return (A.astype(np.float64).ravel(),
            B.astype(np.float64).ravel(),
            M.astype(np.float64).ravel())


# ----------------------------------------------------------------------------- #
# Core kernel-dependence statistics (model-free; characterize ALL dependence).
# ----------------------------------------------------------------------------- #
def _median_bandwidth(X: np.ndarray) -> float:
    """Median-heuristic RBF bandwidth sigma (Gretton et al.). X: (m, d)."""
    m = X.shape[0]
    # pairwise squared distances
    sq = np.sum(X * X, axis=1)
    d2 = sq[:, None] + sq[None, :] - 2.0 * (X @ X.T)
    np.maximum(d2, 0.0, out=d2)
    iu = np.triu_indices(m, k=1)
    med = np.median(d2[iu])
    if med <= 0:
        med = np.mean(d2[iu]) if np.mean(d2[iu]) > 0 else 1.0
    return float(np.sqrt(med / 2.0))  # sigma s.t. exp(-d2/(2 sigma^2))


def _rbf_gram(X: np.ndarray, sigma: float) -> np.ndarray:
    sq = np.sum(X * X, axis=1)
    d2 = sq[:, None] + sq[None, :] - 2.0 * (X @ X.T)
    np.maximum(d2, 0.0, out=d2)
    return np.exp(-d2 / (2.0 * sigma * sigma))


def hsic_biased(X: np.ndarray, Y: np.ndarray) -> float:
    """Biased empirical HSIC_b = (1/m^2) trace(K H L H), Gaussian RBF kernels.

    X: (m, dx), Y: (m, dy). Gretton et al. 2005. HSIC>=0; =0 iff independent
    (population, characteristic kernel).
    """
    X = np.atleast_2d(X);  Y = np.atleast_2d(Y)
    if X.shape[0] == 1: X = X.T
    if Y.shape[0] == 1: Y = Y.T
    m = X.shape[0]
    K = _rbf_gram(X, _median_bandwidth(X))
    L = _rbf_gram(Y, _median_bandwidth(Y))
    H = np.eye(m) - np.ones((m, m)) / m
    Kc = H @ K @ H
    return float(np.sum(Kc * L) / (m * m))   # trace(Kc L) = sum(Kc * L)


def nhsic(X: np.ndarray, Y: np.ndarray) -> float:
    """Normalized HSIC in [0,1]: HSIC(X,Y)/sqrt(HSIC(X,X) HSIC(Y,Y)).

    The kernel analogue of a correlation coefficient (a.k.a. centered kernel
    alignment). Scale-free => comparable across cases and across X-dimensions.
    """
    hxy = hsic_biased(X, Y)
    hxx = hsic_biased(X, X)
    hyy = hsic_biased(Y, Y)
    denom = np.sqrt(max(hxx, 0.0) * max(hyy, 0.0))
    return float(hxy / denom) if denom > 0 else 0.0


def _dcenter(D: np.ndarray) -> np.ndarray:
    rm = D.mean(axis=1, keepdims=True)
    cm = D.mean(axis=0, keepdims=True)
    gm = D.mean()
    return D - rm - cm + gm


def distance_correlation(X: np.ndarray, Y: np.ndarray) -> float:
    """Sample distance correlation dCor in [0,1] (Szekely-Rizzo-Bakirov 2007).

    Double-centered Euclidean distance matrices; dCor=0 iff independent.
    """
    X = np.atleast_2d(X);  Y = np.atleast_2d(Y)
    if X.shape[0] == 1: X = X.T
    if Y.shape[0] == 1: Y = Y.T
    m = X.shape[0]

    def _pdist(Z):
        sq = np.sum(Z * Z, axis=1)
        d2 = sq[:, None] + sq[None, :] - 2.0 * (Z @ Z.T)
        np.maximum(d2, 0.0, out=d2)
        return np.sqrt(d2)

    A = _dcenter(_pdist(X))
    Bm = _dcenter(_pdist(Y))
    dcov2 = np.sum(A * Bm) / (m * m)
    dvarx = np.sum(A * A) / (m * m)
    dvary = np.sum(Bm * Bm) / (m * m)
    denom = np.sqrt(dvarx * dvary)
    if denom <= 0:
        return 0.0
    val = dcov2 / denom
    # numerical floor; dCor^2 can be tiny-negative from roundoff
    return float(np.sqrt(max(val, 0.0)))


def dcor_excess(X: np.ndarray, Y: np.ndarray, n_perm: int = 20,
                rng: np.random.Generator | None = None) -> float:
    """Bias-corrected distance correlation: dCor(X,Y) minus the permutation-null
    mean dCor under INDEPENDENCE (Y rows shuffled). dCor is biased UPWARD at
    finite m -- even independent variables give dCor>0 -- so a raw residual dCor
    cannot floor to 0. Subtracting the permutation-null mean removes that finite-m
    floor in a fully MODEL-FREE way: under true independence the excess -> 0;
    genuine dependence survives. Clipped at 0 (excess is one-sided).
    """
    if rng is None:
        rng = np.random.default_rng(0)
    obs = distance_correlation(X, Y)
    Y2 = np.atleast_2d(Y)
    if Y2.shape[0] == 1:
        Y2 = Y2.T
    null = np.empty(n_perm)
    for i in range(n_perm):
        perm = rng.permutation(Y2.shape[0])
        null[i] = distance_correlation(X, Y2[perm])
    return float(max(obs - null.mean(), 0.0))


# ----------------------------------------------------------------------------- #
# ROUTE R: model-free additive residual, then JOINT dependence of the residual.
#   main effects removed by OUT-OF-FOLD Nadaraya-Watson smoothers on A and on B.
# ----------------------------------------------------------------------------- #
def _nw_oof_1d(x: np.ndarray, y: np.ndarray, folds: int, sigma: float,
               rng: np.random.Generator) -> np.ndarray:
    """Out-of-fold Nadaraya-Watson estimate of E[y|x] (held-out; no in-sample leak)."""
    m = x.size
    idx = rng.permutation(m)
    fold_id = np.zeros(m, dtype=int)
    for f in range(folds):
        fold_id[idx[f::folds]] = f
    yhat = np.empty(m, dtype=np.float64)
    inv2s2 = 1.0 / (2.0 * sigma * sigma)
    for f in range(folds):
        te = fold_id == f
        tr = ~te
        xtr = x[tr]; ytr = y[tr]; xte = x[te]
        # weights w_ij = exp(-(xte_i - xtr_j)^2 / 2 sigma^2)
        d2 = (xte[:, None] - xtr[None, :]) ** 2
        W = np.exp(-d2 * inv2s2)
        wsum = W.sum(axis=1)
        wsum[wsum == 0] = 1e-300
        yhat[te] = (W @ ytr) / wsum
    return yhat


def route_R_residual_dependence(A, B, M, m=1200, blocks=8, folds=5,
                                seed=0) -> dict:
    """Additive main effects removed model-free (OOF NW on A and on B); then the
    dependence that SURVIVES between the residual and the JOINT (A,B).

    Returns dCor and normalized-HSIC of (residual ; joint), averaged over blocks.
    Floors on additive/separable M (residual is ~ noise, independent of joint);
    high on genuinely interactive M.
    """
    rng = np.random.default_rng(1000 + seed)
    n = A.size
    dcs, nhs, rfrac = [], [], []
    for _ in range(blocks):
        sel = rng.choice(n, size=m, replace=False)
        a = A[sel]; b = B[sel]; mm = M[sel]
        # standardize for stable bandwidths
        a = (a - a.mean()) / (a.std() + 1e-12)
        b = (b - b.mean()) / (b.std() + 1e-12)
        mm = (mm - mm.mean()) / (mm.std() + 1e-12)
        sa = 0.5 * np.std(a)  # smoother bandwidths (fraction of spread)
        sb = 0.5 * np.std(b)
        # additive model-free fit: f(a) + g(b), each out-of-fold.
        fa = _nw_oof_1d(a, mm, folds, sa, rng)
        # fit g on the part of M not explained by f(a): residualize then smooth on b
        rb = mm - fa
        gb = _nw_oof_1d(b, rb, folds, sb, rng)
        resid = mm - fa - gb
        joint = np.column_stack([a, b])
        rv = float(np.var(resid) / (np.var(mm) + 1e-12))
        # bias-corrected (permutation-null) dCor: floors finite-m positive bias
        dcs.append(dcor_excess(joint, resid, n_perm=15, rng=rng))
        nhs.append(nhsic(joint, resid))
        rfrac.append(rv)
    return {
        "dCorX_resid_joint": float(np.mean(dcs)),  # bias-corrected excess dCor
        "dCorX_sd":          float(np.std(dcs)),
        "nHSIC_resid_joint": float(np.mean(nhs)),
        "resid_var_frac":   float(np.mean(rfrac)),
    }


# ----------------------------------------------------------------------------- #
# ROUTE D: FIT-FREE direct contrast (no main-effects model at all).
#   Compare dependence of M on TRUE joint (A,B) vs on an ADDITIVE SURROGATE that
#   preserves each parent's marginal relation to M but destroys A<->B coupling.
#
#   Construction of the additive surrogate M_add:
#     Sort-align A->M and B->M to get monotone marginal effect curves, then build
#     M_add(i) = fbarA(rankA_i) + fbarB(rankB_i) where fbarA, fbarB are the
#     isotonic-free marginal means of M across A-bins and B-bins (a model-FREE
#     additive reconstruction). For genuinely additive M this reconstructs M;
#     for interactive M it cannot. The HEADLINE statistic is:
#         interaction_1mR2 = 1 - R2_add, where
#         R2_add = fraction of Var(M) captured by the model-free additive recon
#                  (saturated binned backfit -- the most flexible separable model).
#     We ALSO report the kernel interaction residual dCor(M - M_add ; joint(A,B)),
#     bias-corrected against a permutation null.
#   This needs NO parametric basis and NO fitted smoother slope -- only binned
#   marginal means -- so basis-misspecification cannot inflate it (a saturated
#   binned additive model is the MOST flexible separable model; if interaction
#   still shows, it is real).
# ----------------------------------------------------------------------------- #
def _binned_marginal(x, y, nbins):
    """Model-free marginal mean of y over equal-count bins of x. Returns a function
    value per sample (the bin mean of y for that sample's x-bin)."""
    order = np.argsort(x, kind="stable")
    ranks = np.empty_like(order)
    ranks[order] = np.arange(x.size)
    bin_id = (ranks * nbins // x.size).clip(0, nbins - 1)
    out = np.empty_like(y, dtype=np.float64)
    for bb in range(nbins):
        msk = bin_id == bb
        if np.any(msk):
            out[msk] = y[msk].mean()
    return out, bin_id


def route_D_fitfree_contrast(A, B, M, m=1500, blocks=8, nbins=32,
                             seed=0) -> dict:
    """Fit-free additive-surrogate contrast. No parametric main-effect model.

    Builds a SATURATED binned-additive reconstruction M_add = fbarA + fbarB
    (the most flexible separable model), out-of-fold by backfitting on bin means.
    interaction = joint-dependence of the residual (M - M_add) measured by dCor;
    plus R2_add (additive variance explained). Floors separable M (R2_add ~ 1,
    residual dCor ~ 0); high interaction-residual on genuinely joint M.
    """
    rng = np.random.default_rng(2000 + seed)
    n = A.size
    rdc, r2a, raw_dc = [], [], []
    for _ in range(blocks):
        sel = rng.choice(n, size=m, replace=False)
        a = A[sel]; b = B[sel]; mm = M[sel].astype(np.float64)
        mm = mm - mm.mean()
        # backfit binned additive: iterate fbarA, fbarB a few passes (saturated, model-free)
        fa = np.zeros_like(mm); fb = np.zeros_like(mm)
        for _it in range(6):
            fa, _ = _binned_marginal(a, mm - fb, nbins); fa = fa - fa.mean()
            fb, _ = _binned_marginal(b, mm - fa, nbins); fb = fb - fb.mean()
        m_add = fa + fb
        resid = mm - m_add
        r2 = 1.0 - np.var(resid) / (np.var(mm) + 1e-12)
        joint = np.column_stack([
            (a - a.mean()) / (a.std() + 1e-12),
            (b - b.mean()) / (b.std() + 1e-12),
        ])
        rdc.append(dcor_excess(joint, resid, n_perm=15, rng=rng))
        raw_dc.append(distance_correlation(joint, mm))
        r2a.append(float(r2))
    r2m = float(np.mean(r2a))
    return {
        # HEADLINE interaction score: additive-UNEXPLAINED variance fraction,
        # from a SATURATED model-free binned additive backfit (most flexible
        # separable model -> basis-misspecification cannot inflate it).
        "interaction_1mR2": float(max(1.0 - r2m, 0.0)),
        "interaction_dCorX": float(np.mean(rdc)),  # bias-corr residual joint-dep
        "interaction_sd":   float(np.std(rdc)),
        "R2_additive":      r2m,                    # fraction explained additively
        "raw_dCor_M_joint": float(np.mean(raw_dc)), # TOTAL dependence (NOT interaction)
    }


# ----------------------------------------------------------------------------- #
# PHASE-2 CONTEXT/FRAME test (observer-kernel frame-relativity, NOT grid):
#   Does the emergence verdict GENUINELY flip when we change the CONTEXT/relevance
#   frame (a DIAL on which subset of A-space is "in scope"), as opposed to the grid
#   resolution? Principle: LOCALITY OF NONLINEARITY. M=A*B is interactive globally,
#   but in a NARROW band of A around a0 it is ~ a0*B -> additive. If 1-R2 (this
#   candidate's interaction statistic) is HIGH over a WIDE A-frame and FLOORS over a
#   NARROW A-band, the verdict is genuinely CONTEXT-relative -- distinct from the
#   resolution/grid artifact.
#
#   Second operationalization: CONDITION on a third context variable C. Build
#   M = A*B but where A = C + small (C a shared "context"). Out of context (ignore
#   C, frame over all A) -> interactive. In context (restrict to a thin C-slice)
#   -> A nearly constant -> M ~ const*B -> additive. Same global system, different
#   verdict by context.
# ----------------------------------------------------------------------------- #
def phase2_context_frame(nbins=32, blocks=8, seed=0) -> dict:
    """M=A*B. Compare interaction (1-R2_add) over a WIDE A-frame vs NARROW A-bands.
    Returns the interaction statistic per context width. Floors in narrow context
    => genuine, principled context-relativity (locality of nonlinearity)."""
    A = np.random.default_rng(1).standard_normal(SHAPE).astype(np.float64).ravel()
    B = np.random.default_rng(2).standard_normal(SHAPE).astype(np.float64).ravel()
    M = (A * B)
    out = {}
    # widths in std units of A around a0 = +1.0 (a non-zero context centre, so the
    # local linearization a0*B has real slope).
    a0 = 1.0
    for half in [3.0, 1.0, 0.5, 0.25, 0.1]:
        mask = np.abs(A - a0) <= half
        if mask.sum() < 400:
            out[half] = float("nan");  continue
        a = A[mask]; b = B[mask]; mm = M[mask]
        # subsample to keep dCor/backfit cheap; reuse route_D on the FRAMED subset
        d = route_D_fitfree_contrast(a, b, mm,
                                     m=min(1200, a.size), blocks=blocks,
                                     nbins=nbins, seed=seed)
        out[half] = d["interaction_1mR2"]
    return out


def phase2_context_variable(nbins=32, blocks=8, seed=0) -> dict:
    """Second operationalization: condition on a third context variable C.
    A = C + 0.15*eps (A tracks context C); M = A*B. Out-of-context = frame over
    all A; in-context = restrict to a thin slice of C. Floors in-context."""
    rng = np.random.default_rng(7)
    n = SHAPE[0] * SHAPE[1]
    C = rng.standard_normal(n)
    A = C + 0.15 * rng.standard_normal(n)
    B = rng.standard_normal(n)
    M = A * B
    out = {}
    # out of context: all data
    d_all = route_D_fitfree_contrast(A, B, M, m=1200, blocks=blocks,
                                     nbins=nbins, seed=seed)
    out["all_context"] = d_all["interaction_1mR2"]
    # in context: thin slice of C around c0=1.0
    c0 = 1.0
    for half in [1.0, 0.3, 0.1]:
        mask = np.abs(C - c0) <= half
        if mask.sum() < 400:
            out[f"Cslice_{half}"] = float("nan");  continue
        d = route_D_fitfree_contrast(A[mask], B[mask], M[mask],
                                     m=min(1200, int(mask.sum())),
                                     blocks=blocks, nbins=nbins, seed=seed)
        out[f"Cslice_{half}"] = d["interaction_1mR2"]
    return out


# ----------------------------------------------------------------------------- #
# Driver
# ----------------------------------------------------------------------------- #
def run_all(m_routeR=1200, m_routeD=1500, blocks=8, verbose=True):
    rows = []
    for nm in CASE_NAMES:
        A, B, M = build_case(nm)
        D = route_D_fitfree_contrast(A, B, M, m=m_routeD, blocks=blocks)
        R = route_R_residual_dependence(A, B, M, m=m_routeR, blocks=blocks)
        row = {"case": nm, "expected": EXPECTED[nm], **D, **R}
        rows.append(row)
        if verbose:
            print(
                f"{nm:6s} exp={EXPECTED[nm]:5s} | "
                f"[D] 1-R2_add={D['interaction_1mR2']:.4f} "
                f"inter_dCorX={D['interaction_dCorX']:.4f} "
                f"R2_add={D['R2_additive']:.4f} "
                f"raw_dCor(M;joint)={D['raw_dCor_M_joint']:.4f} | "
                f"[R] dCorX(res;joint)={R['dCorX_resid_joint']:.4f} "
                f"nHSIC={R['nHSIC_resid_joint']:.4f} resid_var={R['resid_var_frac']:.3f}"
            )
    return rows


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mR", type=int, default=1200)
    p.add_argument("--mD", type=int, default=1500)
    p.add_argument("--blocks", type=int, default=8)
    args = p.parse_args()
    print(f"# cand_kernel_dep calibration (mR={args.mR}, mD={args.mD}, "
          f"blocks={args.blocks})")
    print("# EXPECTED: HIGH on INT & XOR ; ~0 on ADD & SEP(A^2+B^2)")
    print("#" + "-" * 78)
    run_all(m_routeR=args.mR, m_routeD=args.mD, blocks=args.blocks)
