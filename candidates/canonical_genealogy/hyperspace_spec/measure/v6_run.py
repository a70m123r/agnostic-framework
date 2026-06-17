#!/usr/bin/env python3
"""
V6 runner — the additive-factors interaction test on reasoning_tokens. Loads the locked 2x2 grid,
runs at the pre-registered tier, computes per-seed the INTERACTION contrast and tests additive vs
interactive. gpt-5.5 only. Requires --run. Synthetic data.
"""
import sys, json, argparse
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from digestion_v2 import openai_solve, verify, last_int
from v6_additive import build_grid, canonical_labels, lock_digest
import numpy as np


def load_locked():
    lk = json.loads((HERE / "v6_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH: v6_additive changed after pre-registration.")
    return items, lk


def run(items, tier):
    stream = []
    print(f"=== V6 additive-factors: {len(items)} items (2x2 x {len(items)//4} seeds) @ effort='{tier}' ===")
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = verify(it["answer"], reply); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({"item_id": it["item_id"], "encode": it["encode"], "depth": it["depth"],
                       "seed": it["seed"], "prompt_words": it["prompt_words"], "tier": tier,
                       "reasoning_tokens": rt, "answer": a, "expected": it["answer"], "correct": ok, "exhausted": ex})
    (HERE / "v6_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    return stream


def analyze(stream):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n=== V6 ANALYSIS ===  solved {len(solved)}/{len(stream)}")

    def cell(E, D):
        return [s["reasoning_tokens"] for s in solved if s["encode"] == E and s["depth"] == D]
    print(f"  cell medians (reasoning_tokens):")
    print(f"            D=4      D=12")
    for E in (0, 3):
        c4, c12 = cell(E, 4), cell(E, 12)
        m4 = np.median(c4) if c4 else float('nan'); m12 = np.median(c12) if c12 else float('nan')
        print(f"    E={E}:   {m4:>6.0f}   {m12:>6.0f}")

    # main effects + the per-seed paired INTERACTION contrast
    seeds = sorted({s["seed"] for s in solved})
    def tok(E, D, sd):
        v = [s["reasoning_tokens"] for s in solved if s["encode"] == E and s["depth"] == D and s["seed"] == sd]
        return v[0] if v else None
    inter, mainE, mainD = [], [], []
    for sd in seeds:
        q = {(E, D): tok(E, D, sd) for E in (0, 3) for D in (4, 12)}
        if any(v is None for v in q.values()):
            continue
        # interaction I = [tok(E3,D12)-tok(E0,D12)] - [tok(E3,D4)-tok(E0,D4)]
        inter.append((q[(3, 12)] - q[(0, 12)]) - (q[(3, 4)] - q[(0, 4)]))
        mainE.append(((q[(3, 4)] + q[(3, 12)]) - (q[(0, 4)] + q[(0, 12)])) / 2.0)   # encode main effect
        mainD.append(((q[(0, 12)] + q[(3, 12)]) - (q[(0, 4)] + q[(3, 4)])) / 2.0)   # depth main effect
    if len(inter) < 4:
        print("  too few complete seeds for the interaction test."); return
    inter = np.array(inter, float)
    rng = np.random.default_rng(7)
    boot = [np.median(rng.choice(inter, len(inter), replace=True)) for _ in range(4000)]
    ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
    pos = int((inter > 0).sum()); neg = int((inter < 0).sum()); nz = pos + neg
    p_two = min(1.0, 2 * sum(comb(nz, i) for i in range(max(pos, neg), nz + 1)) / (2 ** nz)) if nz else 1.0
    print(f"\n  MAIN EFFECT encode (E=3 vs E=0): median {np.median(mainE):+.1f} tok   |   MAIN EFFECT depth (D=12 vs D=4): median {np.median(mainD):+.1f} tok")
    print(f"  PRIMARY INTERACTION (encode x depth): median {np.median(inter):+.1f} tok   bootstrap 95% CI [{ci[0]:+.1f}, {ci[1]:+.1f}]   sign p(two-sided)={p_two:.4f}  ({pos}+/{neg}-/n={len(inter)})")
    NULL = 8.0   # interaction within +/-8 tok ~ a null (about one op's worth)
    print("\n  VERDICT (additive vs interactive serial stages):")
    if abs(np.median(inter)) <= NULL and ci[0] < 0 < ci[1]:
        print(f"    ADDITIVE (interaction ~ 0, CI spans 0): encode and depth load SEPARABLE serial stages.")
        print(f"    -> the cost-camera reads compositional cost as a SUM of stage-costs -- the Sternberg")
        print(f"       additive-factors signature, reproduced on reasoning_tokens. Rediscovery-as-validation, made load-bearing.")
    elif np.median(inter) > NULL and ci[0] > 0:
        print(f"    SUPER-ADDITIVE interaction (+{np.median(inter):.0f} tok, CI excludes 0): the decode is re-paid")
        print(f"       through the chain -> encode and depth share a stage; NOT cleanly staged. Demote the additive claim.")
    else:
        print(f"    INCONCLUSIVE (median {np.median(inter):+.1f}, CI [{ci[0]:+.1f},{ci[1]:+.1f}]): underpowered; escalate seeds.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--tier", default="high")
    a = ap.parse_args()
    if not a.run:
        sys.exit("pass --run: ~48 gpt-5.5 calls (2x2 x 12 seeds), ~$1.2")
    items, lk = load_locked()
    if a.tier != lk.get("tier_preregistered", "high"):
        sys.exit(f"TIER MISMATCH: {a.tier} vs locked {lk.get('tier_preregistered')}")
    print(f"locked: {lk['n_items']} items, seeds={lk['seeds']}, sha256={lk['sha256'][:16]}...")
    stream = run(items, a.tier)
    analyze(stream)
    print(f"\n  wrote v6_run.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    main()
