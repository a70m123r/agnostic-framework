#!/usr/bin/env python3
"""
V5-LITE runner — the confound-free WIDE-vs-DEEP paired test (uses v5_widedeep, gate-passed).

Loads the locked matched pairs (refuses if the generator moved), runs each member at the
pre-registered effort tier, and computes the PAIRED primary: per (m,k,seed),
delta = reasoning_tokens(DEEP) - reasoning_tokens(WIDE), over pairs where BOTH solve. Because the
pair is identical in words/lines/live-vars/work/digits (selftest-verified), delta isolates SPAN.

Primary = median(delta) + a one-sided exact sign test for the DIRECTIONAL depth prediction
(DEEP > WIDE) + a paired bootstrap CI. Null band |delta| < 6 tokens (~one scratchpad line; V4's
~6 tok/op). gpt-5.5 only. Requires --run. Synthetic data.
"""
import sys, json, argparse
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from digestion_v2 import openai_solve, verify, last_int
from v5_widedeep import build_lite, canonical_labels, lock_digest
from v4_stats import raw_spearman
import numpy as np


def load_locked():
    lk = json.loads((HERE / "v5wd_labels.LOCK").read_text(encoding="utf-8"))
    items = build_lite(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH: v5_widedeep changed after pre-registration (supersession, not a run).")
    return items, lk


def run(items, tier):
    stream = []
    print(f"=== V5-LITE: {len(items)} items ({len(items)//2} matched pairs) @ effort='{tier}' ===")
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = verify(it["answer"], reply); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({"item_id": it["item_id"], "structure": it["structure"], "m": it["m"], "k": it["k"],
                       "span": it["span"], "work_ops": it["work_ops"], "live_vars": it["live_vars"],
                       "display_lines": it["display_lines"], "prompt_words": it["prompt_words"],
                       "ans_digits": it["ans_digits"], "seed": it["seed"], "tier": tier,
                       "reasoning_tokens": rt, "answer": a, "expected": it["answer"], "correct": ok, "exhausted": ex})
    (HERE / "v5wd_lite.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    return stream


def analyze(stream):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n=== V5-LITE ANALYSIS ===  solved {len(solved)}/{len(stream)}")
    for st in ("DEEP", "WIDE"):
        tk = [s["reasoning_tokens"] for s in solved if s["structure"] == st]
        if tk:
            print(f"  {st:>4}: n={len(tk):>2}  median_tok={np.median(tk):>5.0f}  mean={np.mean(tk):>6.1f}")
    pairs = {}
    for s in solved:
        pairs.setdefault((s["m"], s["k"], s["seed"]), {})[s["structure"]] = s["reasoning_tokens"]
    deltas = np.array([p["DEEP"] - p["WIDE"] for p in pairs.values() if "DEEP" in p and "WIDE" in p], float)
    if len(deltas) < 4:
        print("  too few complete solved pairs for the paired test."); return
    rng = np.random.default_rng(7)
    boot = [np.median(rng.choice(deltas, len(deltas), replace=True)) for _ in range(4000)]
    ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
    pos = int((deltas > 0).sum()); neg = int((deltas < 0).sum()); nz = pos + neg
    p_one = sum(comb(nz, i) for i in range(pos, nz + 1)) / (2 ** nz) if nz else 1.0
    k = max(pos, neg)
    p_two = min(1.0, 2 * sum(comb(nz, i) for i in range(k, nz + 1)) / (2 ** nz)) if nz else 1.0
    med = float(np.median(deltas))
    NULL = 6.0
    print(f"\n  PRIMARY paired median(DEEP - WIDE) reasoning_tokens = {med:+.1f}")
    print(f"          one-sided sign p(DEEP>WIDE) = {p_one:.4f}   two-sided = {p_two:.4f}   boot 95% CI [{ci[0]:+.1f}, {ci[1]:+.1f}]")
    print(f"          {pos} deep>wide / {neg} wide>deep / n={len(deltas)} pairs   (null band |delta|<{NULL:.0f} tok)")
    print(f"  SECONDARY raw Spearman(reasoning_tokens, span) = {raw_spearman([s['reasoning_tokens'] for s in solved], [s['span'] for s in solved]):+.3f}")
    print("\n  VERDICT (depth vs work/transcription; pre-registered one-sided alpha=0.05):")
    if p_one <= 0.05 and med > NULL:
        print(f"    DEEP > WIDE at fixed work/words/lines/vars -> GENUINE serial-DEPTH cost beyond work+transcription.")
        print(f"    -> PROMOTE: effort tracks work PLUS a critical-path-depth surcharge (gpt-5.5@high, this task class).")
    elif p_two <= 0.05 and med < -NULL:
        print(f"    WIDE > DEEP (unexpected) -> width/branch bookkeeping dominates; reasoning_tokens not a clean depth meter.")
    elif abs(med) <= NULL:
        print(f"    DEEP ~= WIDE (within {NULL:.0f}-tok null band) -> NO depth signal beyond work; the V4 effect was")
        print(f"    arithmetic WORK / transcription, NOT depth. Confirms the demotion. (Escalate seeds only for a tight zero-CI.)")
    else:
        print(f"    DEEP>WIDE in direction (median {med:+.1f}) but p={p_one:.4f}>0.05 -> SUGGESTIVE, underpowered; escalate seeds.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--tier", default="high")
    a = ap.parse_args()
    if not a.run:
        sys.exit("pass --run: ~32 gpt-5.5 calls (16 matched pairs x 2), ~$0.80")
    items, lk = load_locked()
    if a.tier != lk.get("tier_preregistered", "high"):
        sys.exit(f"TIER MISMATCH: --tier={a.tier} vs locked {lk.get('tier_preregistered')}")
    print(f"locked: {lk['n_items']} items, seeds={lk['seeds']}, sha256={lk['sha256'][:16]}...")
    stream = run(items, a.tier)
    analyze(stream)
    print(f"\n  wrote v5wd_lite.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    main()
