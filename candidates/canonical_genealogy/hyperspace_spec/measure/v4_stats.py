#!/usr/bin/env python3
"""
V4 statistics — the ONE primary estimand and its inference, in one place so the
power simulation and the live harness use IDENTICAL math (no estimand drift).

PRIMARY: partial Spearman rho(effort, effective_ops | display_ops, prompt_words)
on SOLVED items only. Partial Spearman = Pearson correlation of the rank-residuals
of effort and effective_ops after linearly regressing each on the rank-transformed
controls. Inference = a permutation null (shuffle the effective_ops ranks) + a
nonparametric bootstrap CI (resample items). numpy only.
"""
import numpy as np


def _rank(a):
    a = np.asarray(a, float)
    order = a.argsort(kind="mergesort")
    r = np.empty(len(a), float)
    r[order] = np.arange(len(a), dtype=float)
    # average ties
    _, inv, counts = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts)); np.add.at(sums, inv, r)
    return (sums / counts)[inv]


def _residual(rank_y, rank_Z):
    # regress rank_y on [1, rank_Z...]; return residuals
    X = np.column_stack([np.ones(len(rank_y))] + [rank_Z[:, j] for j in range(rank_Z.shape[1])])
    beta, *_ = np.linalg.lstsq(X, rank_y, rcond=None)
    return rank_y - X @ beta


def partial_spearman(effort, eff_ops, controls):
    """controls: list of 1D arrays (display_ops, prompt_words). Returns rho in [-1,1]."""
    effort = np.asarray(effort, float); eff_ops = np.asarray(eff_ops, float)
    if len(effort) < 4:
        return float("nan")
    # degenerate-input guard up front on the RANKS (residual std carries ~1e-16 fp noise; testing it ==0 is unreliable)
    if _rank(effort).std() == 0 or _rank(eff_ops).std() == 0:
        return float("nan")
    rZ = np.column_stack([_rank(c) for c in controls]) if controls else np.zeros((len(effort), 0))
    rx = _residual(_rank(effort), rZ)
    ry = _residual(_rank(eff_ops), rZ)
    sx, sy = rx.std(), ry.std()
    if sx < 1e-9 or sy < 1e-9:
        return float("nan")
    return float(np.clip(np.corrcoef(rx, ry)[0, 1], -1, 1))


def perm_pvalue(effort, eff_ops, controls, rng, n=5000):
    """Two-sided permutation p: shuffle the effective_ops labels, recompute partial rho."""
    obs = partial_spearman(effort, eff_ops, controls)
    if np.isnan(obs):
        return float("nan"), obs
    eff_ops = np.asarray(eff_ops, float); cnt = 0
    for _ in range(n):
        perm = rng.permutation(eff_ops)
        v = partial_spearman(effort, perm, controls)
        if not np.isnan(v) and abs(v) >= abs(obs) - 1e-12:
            cnt += 1
    return (cnt + 1) / (n + 1), obs


def bootstrap_ci(effort, eff_ops, controls, rng, n=2000, lo=2.5, hi=97.5):
    effort = np.asarray(effort, float); eff_ops = np.asarray(eff_ops, float)
    ctrls = [np.asarray(c, float) for c in controls]
    m = len(effort); vals = []
    for _ in range(n):
        idx = rng.integers(0, m, m)
        v = partial_spearman(effort[idx], eff_ops[idx], [c[idx] for c in ctrls])
        if not np.isnan(v):
            vals.append(v)
    if not vals:
        return (float("nan"), float("nan"))
    return (float(np.percentile(vals, lo)), float(np.percentile(vals, hi)))


def raw_spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3:
        return float("nan")
    rx, ry = _rank(x), _rank(y)
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.clip(np.corrcoef(rx, ry)[0, 1], -1, 1))
