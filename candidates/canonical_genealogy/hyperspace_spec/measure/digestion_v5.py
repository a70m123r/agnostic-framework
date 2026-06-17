#!/usr/bin/env python3
"""
V5 harness — runs the two CHEAP PRE-TESTS first, then (only if green-lit) the full WIDE-vs-DEEP grid.

Reuses V4 infra EXACTLY: openai_solve/verify/last_int (digestion_v2), partial_spearman/perm_pvalue/
bootstrap_ci/raw_spearman (v4_stats), and the sha256 label-lock pattern (v5_generator). gpt-5.5 only.

Subcommands (each gated behind a spend flag):
  --tier-sweep     PRE-TEST B: re-run a V4 subset at effort low/med/high. ~30 calls. Does the V4
                   work-slope SURVIVE a different token budget? (budget-gate vs need-driven probe.)
  --v5-lite        PRE-TEST A: matched DEEP(span=W) vs WIDE(span<<W) at FIXED work. ~24 calls.
                   Decisive DIRECTION: is there a depth cost beyond work/transcription?
  --run            FULL V5 grid (only after the lite slice points a direction). Spends ~Nx more.

Primary estimand (full grid, pre-registered in v5_labels.LOCK):
  partial-Spearman(reasoning_tokens, SPAN | work_ops, display_lines, ans_digits, prompt_words)
  on SOLVED items only. A positive partial = a genuine depth/critical-path cost net of work and
  transcription length. A null = effort was work/transcription all along (V4 demoted to volume).

For the matched-pair pre-tests the headline is the simpler, more robust PAIRED contrast:
  per seed, delta = tokens(DEEP) - tokens(WIDE) at the SAME work level. Wilcoxon-style sign test +
  median paired delta + bootstrap CI. (Identical work/lines/digits/mix -> the pairing removes the
  per-seed nuisance the partial has to model.) The partial-Spearman is reported as the secondary,
  estimand-consistent number so the full grid and the lite slice share one math path.
"""
import sys, json, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from digestion_v2 import openai_solve, verify, last_int            # exact reuse
from v4_generator import build_grid as build_v4_grid              # the V4 ladder, for the tier sweep
from v5_generator import build_grid, build_lite, canonical_labels, lock_digest, W_LEVELS
from v4_stats import partial_spearman, bootstrap_ci, perm_pvalue, raw_spearman
import numpy as np


# ---------------------------------------------------------------- call one item
def solve_item(prompt, ansvar_answer, tier):
    exhausted = False
    try:
        reply, rt, dt = openai_solve(prompt, tier)
    except Exception:
        reply, rt, dt, exhausted = "", None, 100.0, True
    ok = (False if exhausted else verify(ansvar_answer, reply))
    a = (None if exhausted else last_int(reply))
    return ok, a, rt, dt, exhausted


# ============================================================ PRE-TEST B: tier sweep
def tier_sweep(seeds_subset=2, tiers=("low", "medium", "high")):
    """Re-run a SMALL balanced V4 subset (every E band x one T) at low/med/high.
    Reports the V4 work-slope (raw Spearman(tokens,E)) per tier. ~ |E|*seeds*|tiers| calls."""
    v4 = build_v4_grid(12)
    # balanced subset: all 5 E bands, ONE T (=16, the middle), first `seeds_subset` seeds
    sub = [it for it in v4 if it["display_ops"] == 16 and it["seed"] < seeds_subset]
    n_calls = len(sub) * len(tiers)
    print(f"=== PRE-TEST B: TIER SWEEP ({len(sub)} V4 items x {len(tiers)} tiers = {n_calls} calls) ===")
    stream = []
    for tier in tiers:
        for it in sub:
            ok, a, rt, dt, ex = solve_item(it["prompt"], it["answer"], tier)
            stream.append({"phase": "tier_sweep", "tier": tier, "item_id": it["item_id"],
                           "effective_ops": it["effective_ops"], "display_ops": it["display_ops"],
                           "reasoning_tokens": rt, "correct": ok, "exhausted": ex, "seconds": dt})
    (HERE / "v5_tier_sweep.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    print("\n  V4 work-slope per tier  (raw Spearman(reasoning_tokens, effective_ops), solved-only):")
    print(f"  {'tier':>7} {'solved':>7} {'slope':>7} {'p':>8} {'med_tok':>8}")
    rng = np.random.default_rng(7)
    slopes = {}
    for tier in tiers:
        rows = [s for s in stream if s["tier"] == tier and s["correct"] and s["reasoning_tokens"] is not None]
        if len(rows) < 6:
            print(f"  {tier:>7} {len(rows):>7}  too few solved"); continue
        eff = [r["reasoning_tokens"] for r in rows]; E = [r["effective_ops"] for r in rows]
        slope = raw_spearman(eff, E)
        p, _ = perm_pvalue(eff, E, [], rng, n=3000)
        slopes[tier] = slope
        print(f"  {tier:>7} {len(rows):>7} {slope:>+7.3f} {p:>8.4f} {np.median(eff):>8.0f}")
    # DECISION RULE
    print("\n  DECISION (budget-gate vs need-driven):")
    if "low" in slopes and "high" in slopes:
        if slopes["low"] >= 0.5:
            print(f"    slope SURVIVES at low effort ({slopes['low']:+.3f}) -> NOT pure budget-gate; the")
            print(f"    work->tokens coupling is need-driven (allocates by required work even on a small budget).")
        elif slopes["low"] < 0.2:
            print(f"    slope COLLAPSES at low effort ({slopes['low']:+.3f} vs high {slopes['high']:+.3f}) -> the")
            print(f"    V4 +0.894 is BUDGET-GATED: high tier buys headroom the model spends ~linearly on work.")
        else:
            print(f"    slope ATTENUATES (low {slopes['low']:+.3f} < high {slopes['high']:+.3f}) -> partial budget")
            print(f"    sensitivity; report as mixed, lean need-driven if CI(low) excludes 0.")
    return stream, slopes


# ============================================================ PRE-TEST A: V5-LITE
def paired_delta_test(stream):
    """Per-seed paired contrast DEEP - WIDE at fixed work.
    PRE-REGISTERED PRIMARY TEST = one-sided exact sign test for the DIRECTIONAL depth prediction
    (DEEP costs MORE reasoning_tokens than WIDE at fixed work). One-sided is what the power analysis
    (v5_power_sim.py) is calibrated on; a WIDE>DEEP surprise is reported but is NOT 'depth support'.
    Returns (median_delta, ci, p_onesided_deepgtwide, p_twosided, n_pairs, pos, neg)."""
    from math import comb
    byseed = {}
    for s in stream:
        if s["correct"] and s["reasoning_tokens"] is not None:
            byseed.setdefault((s["work_ops"], s["seed"]), {})[s["structure"]] = s["reasoning_tokens"]
    deltas = [d["DEEP"] - d["WIDE"] for d in byseed.values() if "DEEP" in d and "WIDE" in d]
    if len(deltas) < 4:
        return None
    deltas = np.array(deltas, float)
    rng = np.random.default_rng(7)
    boot = [np.median(rng.choice(deltas, len(deltas), replace=True)) for _ in range(4000)]
    ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
    pos = int((deltas > 0).sum()); neg = int((deltas < 0).sum()); nz = pos + neg
    p_one = sum(comb(nz, i) for i in range(pos, nz + 1)) / (2 ** nz) if nz else 1.0   # P(>=pos | Bin(nz,.5))
    k = max(pos, neg)
    p_two = min(1.0, 2 * (sum(comb(nz, i) for i in range(k, nz + 1)) / (2 ** nz))) if nz else 1.0
    return float(np.median(deltas)), ci, float(p_one), float(p_two), len(deltas), pos, neg


def v5_lite(seeds=12, tier="high"):
    """Matched DEEP(m=1, span=W) vs WIDE(m=5, span<<W) at W=14. n = 2*seeds calls."""
    items = build_lite(seeds)
    print(f"=== PRE-TEST A: V5-LITE  ({len(items)} matched items @ effort='{tier}') ===")
    print(f"  W=14 fixed (op-count matched); DEEP span=14 vs WIDE m=5 span~6; lines/digits/op-mix matched.")
    stream = []
    for it in items:
        ok, a, rt, dt, ex = solve_item(it["prompt"], it["answer"], tier)
        stream.append({"phase": "v5_lite", "item_id": it["item_id"], "structure": it["structure"],
                       "work_ops": it["work_ops"], "span": it["span"], "width": it["width"],
                       "display_lines": it["display_lines"], "ans_digits": it["ans_digits"],
                       "prompt_words": it["prompt_words"], "seed": it["seed"], "tier": tier,
                       "reasoning_tokens": rt, "answer": a, "expected": it["answer"],
                       "correct": ok, "exhausted": ex, "seconds": dt})
    (HERE / "v5_lite.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze_lite(stream)
    return stream


def analyze_lite(stream):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n=== V5-LITE ANALYSIS ===  solved {len(solved)}/{len(stream)}")
    for st in ("DEEP", "WIDE"):
        toks = [s["reasoning_tokens"] for s in solved if s["structure"] == st]
        if toks:
            print(f"  {st:>4} (span {'14' if st=='DEEP' else '~6'}): n={len(toks):>2} median_tok={np.median(toks):>5.0f} mean={np.mean(toks):>6.1f}")
    res = paired_delta_test(solved)
    if res is None:
        print("  too few matched pairs for the paired test (need >=4)."); return
    med, ci, p_one, p_two, npair, pos, neg = res
    print(f"\n  PRIMARY (paired, one-sided sign test for DEEP>WIDE): median (DEEP - WIDE) tokens = {med:+.1f}")
    print(f"           one-sided p = {p_one:.4f}  (two-sided {p_two:.4f})   descriptive 95% CI [{ci[0]:+.1f}, {ci[1]:+.1f}]   ({pos} deep>wide / {neg} wide>deep / n={npair})")
    eff = [s["reasoning_tokens"] for s in solved]; S = [s["span"] for s in solved]
    rho = raw_spearman(eff, S)
    print(f"  SECONDARY raw Spearman(reasoning_tokens, span) = {rho:+.3f}  (at fixed W=14, lines/digits/work all constant)")
    NOISE_FLOOR = 6.0   # ~1 scratchpad-line of tokens; a |median| under this is a practical null (V4: 6 tok/op)
    print("\n  DECISION (depth vs work/transcription) — pre-registered one-sided alpha=0.05, null-band |delta|<6 tok:")
    if p_one <= 0.05 and med > NOISE_FLOOR:
        print(f"    DEEP > WIDE at fixed work (one-sided p={p_one:.4f}, median +{med:.0f} tok) -> a GENUINE depth/span")
        print(f"    cost beyond work+transcription. V4's +0.894 was NOT only volume: longer critical paths cost extra")
        print(f"    reasoning_tokens. -> ESCALATE to the full V5 grid to estimate the per-span slope.")
    elif p_two <= 0.05 and med < -NOISE_FLOOR:
        print(f"    WIDE > DEEP (two-sided p={p_two:.4f}, unexpected sign) -> width/branch-tracking dominates;")
        print(f"    reasoning_tokens is NOT a clean depth meter. Diagnose serialization/branch-bookkeeping first.")
    elif abs(med) <= NOISE_FLOOR:
        print(f"    DEEP ~= WIDE (median {med:+.1f} tok, within the {NOISE_FLOOR:.0f}-tok null band; p={p_one:.4f}) -> NO")
        print(f"    depth signal beyond work; lean to DEMOTING V4 to op-volume/transcription. (Run the full grid only")
        print(f"    if you need a tight zero CI; the lite null is already the cheaper verdict.)")
    else:
        print(f"    DEEP > WIDE in direction (median {med:+.1f} tok) but p={p_one:.4f} > 0.05 -> SUGGESTIVE,")
        print(f"    underpowered. ESCALATE seeds 12->16 (+16 calls) before any verdict; do NOT demote yet.")


# ============================================================ FULL GRID (gated)
def run_full(seeds, tier="high"):
    items = build_grid(seeds)
    print(f"=== V5 FULL GRID: {len(items)} items @ effort='{tier}' (gpt-5.5) ===")
    stream = []
    for i, it in enumerate(items):
        ok, a, rt, dt, ex = solve_item(it["prompt"], it["answer"], tier)
        stream.append({"phase": "v5_full", "item_id": it["item_id"], "structure": it["structure"],
                       "work_ops": it["work_ops"], "span": it["span"], "width": it["width"],
                       "display_lines": it["display_lines"], "ans_digits": it["ans_digits"],
                       "prompt_words": it["prompt_words"], "seed": it["seed"], "tier": tier,
                       "reasoning_tokens": rt, "answer": a, "expected": it["answer"],
                       "correct": ok, "exhausted": ex, "seconds": dt})
        if (i + 1) % 12 == 0 or i + 1 == len(items):
            ns = sum(1 for s in stream if s["correct"])
            print(f"  [{i+1:>3}/{len(items)}] solved={ns} last {it['structure']} W{it['work_ops']} span{it['span']} -> {'OK' if ok else 'x'} {rt}t")
    (HERE / "v5_run.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze_full(stream)
    return stream


def analyze_full(stream, label="V5"):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n=== {label} ANALYSIS ===  solved {len(solved)}/{len(stream)}")
    if len(solved) < 10:
        print("  too few solved for the primary estimand."); return
    eff = [s["reasoning_tokens"] for s in solved]; S = [s["span"] for s in solved]
    W = [s["work_ops"] for s in solved]; D = [s["display_lines"] for s in solved]
    G = [s["ans_digits"] for s in solved]; P = [s["prompt_words"] for s in solved]
    rng = np.random.default_rng(7)
    rho = partial_spearman(eff, S, [W, D, G, P])
    ci = bootstrap_ci(eff, S, [W, D, G, P], rng, n=2000)
    p, _ = perm_pvalue(eff, S, [W, D, G, P], rng, n=5000)
    print(f"  PRIMARY partial-Spearman(reasoning_tokens, SPAN | work_ops, display_lines, ans_digits, prompt_words) = {rho:+.3f}")
    print(f"          bootstrap 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]   permutation p = {p:.4f}")
    print(f"  SECONDARY raw(tokens, span)={raw_spearman(eff, S):+.3f}  raw(tokens, work)={raw_spearman(eff, W):+.3f}")
    # paired contrast per (W, seed)
    res = paired_delta_test(solved)
    if res:
        med, cci, p_one, p_two, npair, pos, neg = res
        print(f"  PAIRED median(DEEP-WIDE)={med:+.1f}  CI[{cci[0]:+.1f},{cci[1]:+.1f}]  one-sided p={p_one:.4f}  ({pos}/{neg}/{npair})")
    print("\n  READ: partial(tokens,span|work,...) >> 0 with CI excluding 0 -> genuine DEPTH cost net of work")
    print("        + transcription (V4 effect was not only volume). partial ~ 0 -> effort = work/transcription.")


# ---------------------------------------------------------------- lock guard
def load_locked(which):
    tag = "v5_lite" if which == "lite" else "v5"
    lockp = HERE / f"{tag}_labels.LOCK"
    if not lockp.exists():
        sys.exit(f"no {tag}_labels.LOCK -- run: python v5_generator.py --lock --which {which} --seeds N")
    lock = json.loads(lockp.read_text(encoding="utf-8"))
    items = build_lite(lock["seeds"]) if which == "lite" else build_grid(lock["seeds"])
    if lock_digest(canonical_labels(items)) != lock["sha256"]:
        sys.exit("LOCK MISMATCH: generator changed after pre-registration (supersession, not a run).")
    return lock


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier-sweep", action="store_true", help="PRE-TEST B (~30 calls)")
    ap.add_argument("--v5-lite", action="store_true", help="PRE-TEST A (~24 calls)")
    ap.add_argument("--run", action="store_true", help="FULL V5 grid (spends most)")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--tier", default="high")
    a = ap.parse_args()
    if a.tier_sweep:
        tier_sweep(seeds_subset=2)
    elif a.v5_lite:
        load_locked("lite")            # refuse unless pre-registered
        v5_lite(seeds=a.seeds, tier=a.tier)
    elif a.run:
        load_locked("full")
        run_full(seeds=a.seeds, tier=a.tier)
    else:
        sys.exit("pass --tier-sweep | --v5-lite | --run  (each spends OPENAI_API_KEY; gpt-5.5)")


if __name__ == "__main__":
    main()
