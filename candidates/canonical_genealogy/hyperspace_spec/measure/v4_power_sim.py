#!/usr/bin/env python3
"""
V4 power simulation — runs BEFORE any model call (codex fix: "fix power before calling models").

Simulates reasoning_tokens under a generative model where effective_ops E has a TRUE monotone
effect, display_ops T is a nuisance with its own effect, plus lognormal call-noise calibrated to
the ~2x within-item spread seen in v2_run.jsonl. For each (true effect b_E, seed count) it runs
the EXACT primary estimand from v4_stats (partial-Spearman(effort, E | T, prompt_words) on SOLVED
items) with a permutation test, and reports POWER = P(detect at p<0.05).

b_E = 0 is the calibration row: power there is the false-positive rate (should sit near 0.05).
Solved-only is enforced (failures excluded), matching the live harness — so the sim also exposes
how the solve-rate drop at high E erodes power. numpy only, offline, deterministic (fixed seed).
"""
import numpy as np
from v4_stats import partial_spearman, perm_pvalue
from v4_generator import build_grid

SIGMA = 0.55          # lognormal noise sd (v2 within-item spread ~2x -> ln ~0.5-0.6)
B_T = 0.25            # nuisance: display length nudges hidden-token count
SOLVE_BASE = 0.97     # P(solve) at easiest E
SOLVE_SLOPE = 0.045   # P(solve) drops with E (so high-E items get censored out)


def simulate_once(items, b_E, rng):
    E = np.array([it["effective_ops"] for it in items], float)
    T = np.array([it["display_ops"] for it in items], float)
    W = np.array([it["prompt_words"] for it in items], float)
    En = (E - E.mean()) / E.std(); Tn = (T - T.mean()) / T.std()
    # true generative model for hidden reasoning tokens (log scale)
    log_tok = 4.0 + b_E * En + B_T * Tn + rng.normal(0, SIGMA, len(items))
    effort = np.exp(log_tok)
    # solve model: harder (high E) -> more likely censored out (NOT turned into fake effort)
    p_solve = np.clip(SOLVE_BASE - SOLVE_SLOPE * (E - E.min()), 0.25, 0.99)
    solved = rng.random(len(items)) < p_solve
    if solved.sum() < 10:
        return None
    return effort[solved], E[solved], T[solved], W[solved]


def power(items, b_E, n_sims, rng, perms=150):
    hits = 0; rhos = []; solved_frac = []
    for _ in range(n_sims):
        s = simulate_once(items, b_E, rng)
        if s is None:
            continue
        effort, E, T, W = s
        solved_frac.append(len(effort) / len(items))
        p, rho = perm_pvalue(effort, E, [T, W], rng, n=perms)
        if not np.isnan(p):
            rhos.append(rho)
            if p < 0.05:
                hits += 1
    return hits / max(1, n_sims), float(np.mean(rhos)) if rhos else float("nan"), float(np.mean(solved_frac)) if solved_frac else float("nan")


def main():
    rng = np.random.default_rng(7)
    print("=== V4 power simulation (primary estimand, solved-only) ===")
    print(f"grid: E={[2,4,6,8,10]} x T=[12,16,20]; noise sigma={SIGMA}, nuisance b_T={B_T}")
    print(f"{'seeds':>6} {'n_items':>8} {'b_E':>5} {'power':>7} {'mean_rho':>9} {'solved%':>8}")
    for seeds in (8, 12, 16):
        items = build_grid(seeds)
        for b_E in (0.0, 0.3, 0.6, 1.0):
            pw, mrho, sf = power(items, b_E, n_sims=120, rng=rng)
            tag = "  <- false-positive rate (want ~0.05)" if b_E == 0.0 else ("  <- powered" if pw >= 0.8 else "")
            print(f"{seeds:>6} {len(items):>8} {b_E:>5.1f} {pw:>7.2f} {mrho:>9.3f} {sf*100:>7.0f}%{tag}")
    print("\nread: pick the smallest seed count whose b_E>=0.6 row clears power>=0.80 while the")
    print("b_E=0.0 row stays near 0.05. That seed count is the pre-registered N for the live run.")


if __name__ == "__main__":
    main()
