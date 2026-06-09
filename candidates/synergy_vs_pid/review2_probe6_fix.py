"""review2_probe6_fix.py -- SECOND-PASS reviewer probe P6 (Fable pass).

P4 in review2_probes.py showed cand_predictive_gain's additive baseline
(E[M|A]+E[M|B]-E[M], sum of MARGINAL bin-means, no backfit) FALSE-FLAGS pure
additive M when parents are correlated (r=0.9 -> gain=0.733), because the sum
of marginal conditional means is not the best additive model under dependence
(it double-counts the shared component). The GAM candidate's JOINT least-squares
separable fit floors the same case at 0.002.

P6 verifies the fix: keep the held-out joint-vs-additive protocol of
cand_predictive_gain UNCHANGED, but fit the additive model PROPERLY -- joint
ridge-stabilised least squares on [intercept | one-hot(A-bins) | one-hot(B-bins)]
(the piecewise-constant GAM, equivalent to backfitting to convergence). Same
folds, same bins, same backoff. If gain_v2 floors ADDc/SEPc under r=0.9 while
still reproducing the independent-parent calibration (INT/XOR HIGH, ADD/SEP ~0),
the hole is in the BASELINE FITTER, not in the measure's design.
"""
from __future__ import annotations

import numpy as np

from pid_synergy import _quantile_bin
from cand_predictive_gain import predictive_gain


def predictive_gain_v2(A, B, M, bins=8, folds=5, seed=1234, ridge=1e-8):
    """Held-out R2[joint 2D cell-mean] - R2[additive fit by JOINT least squares]."""
    Af = np.asarray(A, float).ravel()
    Bf = np.asarray(B, float).ravel()
    Mf = np.asarray(M, float).ravel()
    n = Mf.size
    la = _quantile_bin(Af, bins)
    lb = _quantile_bin(Bf, bins)
    na = int(la.max()) + 1
    nb = int(lb.max()) + 1
    cell = la * nb + lb
    ncell = na * nb

    # one-hot additive design: [1 | I(A-bin) | I(B-bin)]
    def design(ia, ib):
        m = ia.size
        X = np.zeros((m, 1 + na + nb))
        X[:, 0] = 1.0
        X[np.arange(m), 1 + ia] = 1.0
        X[np.arange(m), 1 + na + ib] = 1.0
        return X

    rng = np.random.default_rng(seed)
    fold_id = rng.integers(0, folds, size=n)
    ss_res_add = ss_res_joint = ss_tot = 0.0
    for k in range(folds):
        te = fold_id == k
        tr = ~te
        if not te.any() or not tr.any():
            continue
        gm = float(Mf[tr].mean())
        Xtr = design(la[tr], lb[tr])
        G = Xtr.T @ Xtr
        G[np.diag_indices_from(G)] += ridge * np.trace(G) / G.shape[0]
        coef = np.linalg.solve(G, Xtr.T @ Mf[tr])
        pred_add = design(la[te], lb[te]) @ coef
        # joint cell means on TRAIN, backoff to additive prediction
        sums = np.zeros(ncell); cnts = np.zeros(ncell)
        np.add.at(sums, cell[tr], Mf[tr])
        np.add.at(cnts, cell[tr], 1.0)
        muC = np.where(cnts > 0, sums / np.maximum(cnts, 1.0), np.nan)
        pj = muC[cell[te]]
        pj = np.where(np.isnan(pj), pred_add, pj)
        y = Mf[te]
        ss_tot += float(np.sum((y - gm) ** 2))
        ss_res_add += float(np.sum((y - pred_add) ** 2))
        ss_res_joint += float(np.sum((y - pj) ** 2))
    r2a = 1 - ss_res_add / ss_tot
    r2j = 1 - ss_res_joint / ss_tot
    return r2a, r2j, r2j - r2a


if __name__ == "__main__":
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float64).ravel()
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float64).ravel()
    n = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float64).ravel()

    print("P6  gain_v2 = held-out R2[joint] - R2[additive fit by JOINT LS] (backfit-correct baseline)")
    print("=" * 96)
    print("A) independent-parent calibration must REPRODUCE:")
    for lbl, Bx, M, exp in [
        ("INT  A*B", B, A * B, "HIGH"),
        ("XOR  sign*sign", B, np.sign(A) * np.sign(B), "HIGH"),
        ("ADD  0.5A+0.5B", B, 0.5 * A + 0.5 * B, "~0"),
        ("SEP  A^2+B^2", B, A * A + B * B, "~0"),
        ("ALLOY", B, 0.5 * A + 0.5 * B + 0.1 * A * B, "small+"),
        ("NOISY-ADD 0.5A+0.5B+0.5n", B, 0.5 * A + 0.5 * B + 0.5 * n, "~0"),
    ]:
        r2a, r2j, g = predictive_gain_v2(A, Bx, M)
        print(f"  {lbl:26} gain_v2={g:+.5f}  (R2_add={r2a:.4f} R2_joint={r2j:.4f})  expect {exp}")

    print()
    print("B) correlated parents (the P4 hole) -- v1 vs v2:")
    for rho in (0.9, 0.99):
        Bc = rho * A + np.sqrt(1 - rho * rho) * B
        for lbl, M, exp in [
            (f"ADDc r={rho}", 0.5 * A + 0.5 * Bc, "~0  (v1 FALSE-FLAGGED)"),
            (f"SEPc r={rho}", A * A + Bc * Bc, "~0  (v1 false-flagged)"),
            (f"INTc r={rho}", A * Bc, "small+ (true cross share shrinks)"),
        ]:
            g1 = predictive_gain(A, Bc, M, bins=8).gain_r2
            r2a, r2j, g2 = predictive_gain_v2(A, Bc, M)
            print(f"  {lbl:14} v1={g1:+.5f}   v2={g2:+.5f}  (R2_add={r2a:.4f})   expect {exp}")
