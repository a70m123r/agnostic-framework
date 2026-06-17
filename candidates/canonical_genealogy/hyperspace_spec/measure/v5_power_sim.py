#!/usr/bin/env python3
"""
V5 power/discrimination simulation — runs BEFORE any model call (power-before-spend).

Simulates reasoning_tokens under THREE generative hypotheses and checks the V5-LITE paired test +
the full-grid partial-Spearman recover the right verdict, with what power, at the proposed n.

Hypotheses (token model; calibrated to the REAL V4 run: ~6 tok/op, intercept ~27, lognormal spread):
  H_work  : tokens ~ f(work_ops)           only          -> DEEP == WIDE at fixed work (NULL paired delta)
  H_trans : tokens ~ f(display_lines)      only (== work) -> DEEP == WIDE                (NULL)
  H_depth : tokens ~ f(work) + beta*span                  -> DEEP  >  WIDE  (positive paired delta)

H_work and H_trans are indistinguishable here BY DESIGN (work==lines==const within a W tier) — that's
the V4 confound. Only H_depth moves the paired delta. So: paired-delta power under H_depth, and the
false-positive rate under H_work/H_trans (must sit ~0.05), is the decision-quality the lite slice buys.
numpy only, offline, deterministic.
"""
import numpy as np
from math import comb
from v5_generator import build_grid, build_lite
from v4_stats import partial_spearman, perm_pvalue, raw_spearman

TOK_PER_OP = 6.0      # real V4 median slope
INTERCEPT = 27.0      # real V4 intercept
SIGMA_LN = 0.13       # lognormal token noise — MEASURED: real V4 within-(E,T)-cell median ln-sd = 0.131


def gen_tokens(items, hyp, beta_span, rng):
    work = np.array([it["work_ops"] for it in items], float)
    span = np.array([it["span"] for it in items], float)
    lines = np.array([it["display_lines"] for it in items], float)
    if hyp == "work":
        mu = INTERCEPT + TOK_PER_OP * work
    elif hyp == "trans":
        mu = INTERCEPT + TOK_PER_OP * lines          # lines == work within a tier -> same as H_work
    elif hyp == "depth":
        # base on work, PLUS a per-span-step surcharge: longer critical path costs extra tokens
        mu = INTERCEPT + TOK_PER_OP * work + beta_span * span
    else:
        raise ValueError(hyp)
    return mu * np.exp(rng.normal(0, SIGMA_LN, len(items)))


def paired_delta(items, tokens):
    by = {}
    for it, t in zip(items, tokens):
        by.setdefault((it["work_ops"], it["seed"]), {})[it["structure"]] = t
    d = [v["DEEP"] - v["WIDE"] for v in by.values() if "DEEP" in v and "WIDE" in v]
    return np.array(d, float)


def sign_p(deltas):
    pos = int((deltas > 0).sum()); neg = int((deltas < 0).sum()); nz = pos + neg
    if nz == 0:
        return 1.0
    k = max(pos, neg)
    return min(1.0, 2 * sum(comb(nz, i) for i in range(k, nz + 1)) / (2 ** nz))


def lite_power(seeds, hyp, beta_span, n_sims=2000, one_sided=True):
    """Decision rule: directional one-sided sign-test (DEEP>=WIDE is the depth prediction) at alpha=.05.
    One-sided is legitimate because H_depth makes a SIGNED prediction (DEEP costs MORE); a WIDE>DEEP
    surprise is reported separately, not as 'support'. Reports power = P(reject toward DEEP>WIDE)."""
    items = build_lite(seeds)
    rng = np.random.default_rng(11)
    hits = 0; meds = []
    for _ in range(n_sims):
        tok = gen_tokens(items, hyp, beta_span, rng)
        d = paired_delta(items, tok)
        meds.append(np.median(d))
        pos = int((d > 0).sum()); neg = int((d < 0).sum()); nz = pos + neg
        if nz == 0:
            continue
        if one_sided:
            # one-sided binomial: P(>= pos successes | Bin(nz, .5)); reject if small AND median>0
            p_os = sum(comb(nz, i) for i in range(pos, nz + 1)) / (2 ** nz)
            if p_os <= 0.05 and np.median(d) > 0:
                hits += 1
        else:
            if sign_p(d) <= 0.05:
                hits += 1
    return hits / n_sims, float(np.mean(meds))


def full_power(seeds, hyp, beta_span, n_sims=300):
    items = build_grid(seeds)
    rng = np.random.default_rng(13)
    hits = 0; rhos = []
    W = [it["work_ops"] for it in items]; D = [it["display_lines"] for it in items]
    G = [it["ans_digits"] for it in items]; P = [it["prompt_words"] for it in items]
    S = [it["span"] for it in items]
    for _ in range(n_sims):
        tok = gen_tokens(items, hyp, beta_span, rng)
        p, rho = perm_pvalue(tok, S, [W, D, G, P], rng, n=200)
        if not np.isnan(p):
            rhos.append(rho)
            if p < 0.05:
                hits += 1
    return hits / n_sims, float(np.mean(rhos))


def main():
    print("=== V5 DISCRIMINATION + POWER (calibrated to real V4: 6 tok/op, sigma_ln=0.18) ===\n")
    print("V5-LITE paired sign-test (DEEP-WIDE), ONE-SIDED alpha=0.05, sigma_ln=0.13 (measured):")
    print(f"  {'hyp':>6} {'beta_span':>10} {'seeds':>6} {'pairs':>6} {'reject%':>8} {'mean_med_delta':>15}")
    for seeds in (12, 16, 24):
        npairs = seeds  # one DEEP & one WIDE per seed at W=14
        for hyp, b in [("work", 0.0), ("trans", 0.0), ("depth", 1.0), ("depth", 2.0), ("depth", 4.0)]:
            pw, md = lite_power(seeds, hyp, b)
            tag = "  <- FALSE POS (want <=0.05)" if hyp in ("work", "trans") else ("  <- powered" if pw >= 0.8 else "")
            print(f"  {hyp:>6} {b:>10.1f} {seeds:>6} {npairs:>6} {pw*100:>7.0f}% {md:>15.1f}{tag}")
    print("\n  (beta_span = extra reasoning_tokens per unit of critical-path length. At W=14 the DEEP-WIDE")
    print("   span gap is ~8, so a delta of 8*beta_span tokens must clear the ~5-15 token noise floor.)")

    print("\nFull-grid partial-Spearman(tokens, span | work, lines, digits, words), perm p<0.05:")
    print(f"  {'hyp':>6} {'beta_span':>10} {'seeds':>6} {'n':>5} {'power%':>8} {'mean_rho':>9}")
    for seeds in (12,):
        items = build_grid(seeds)
        for hyp, b in [("work", 0.0), ("depth", 1.0), ("depth", 2.0)]:
            pw, mr = full_power(seeds, hyp, b)
            tag = "  <- FALSE POS (want ~0.05)" if hyp == "work" else ("  <- powered" if pw >= 0.8 else "")
            print(f"  {hyp:>6} {b:>10.1f} {seeds:>6} {len(items):>5} {pw*100:>7.0f}% {mr:>9.3f}{tag}")
    print("\nread: pick the smallest seeds whose H_depth row clears reject>=0.80 while H_work/H_trans stay ~0.05.")
    print("      If even beta_span=1 is powered at seeds=12 (n_lite=24), the lite slice is decisive & cheap.")


if __name__ == "__main__":
    main()
