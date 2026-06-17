#!/usr/bin/env python3
"""
V6b runner -- decomposes V6's encode effect into text-cost vs compute-cost via the E3dead control.
Loads the locked 3x2 grid, runs at the pre-registered tier, computes per (D,seed) the two paired
contrasts. gpt-5.5. Requires --run. Synthetic data.
"""
import sys, json, argparse
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from digestion_v2 import openai_solve, verify, last_int
from v6b_control import build_grid, canonical_labels, lock_digest
import numpy as np


def load_locked():
    lk = json.loads((HERE / "v6b_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH: v6b_control changed after pre-registration.")
    return items, lk


def run(items, tier):
    stream = []
    print(f"=== V6b control: {len(items)} items (3x2 x {len(items)//6} seeds) @ effort='{tier}' ===")
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = verify(it["answer"], reply); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({"item_id": it["item_id"], "encode": it["encode"], "depth": it["depth"],
                       "seed": it["seed"], "prompt_words": it["prompt_words"], "tier": tier,
                       "reasoning_tokens": rt, "answer": a, "expected": it["answer"], "correct": ok, "exhausted": ex})
    (HERE / "v6b_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    return stream


def paired(deltas):
    deltas = np.array([d for d in deltas if d is not None], float)
    if len(deltas) < 4:
        return None
    rng = np.random.default_rng(7)
    boot = [np.median(rng.choice(deltas, len(deltas), replace=True)) for _ in range(4000)]
    ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
    pos = int((deltas > 0).sum()); neg = int((deltas < 0).sum()); nz = pos + neg
    p = min(1.0, 2 * sum(comb(nz, i) for i in range(max(pos, neg), nz + 1)) / (2 ** nz)) if nz else 1.0
    return float(np.median(deltas)), ci, p, pos, neg, len(deltas)


def analyze(stream):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n=== V6b ANALYSIS ===  solved {len(solved)}/{len(stream)}")
    def cell(E, D):
        return [s["reasoning_tokens"] for s in solved if s["encode"] == E and s["depth"] == D]
    print(f"  cell medians (reasoning_tokens):       D=4     D=12")
    for E in ("E0", "E3dead", "E3live"):
        c4, c12 = cell(E, 4), cell(E, 12)
        m4 = np.median(c4) if c4 else float('nan'); m12 = np.median(c12) if c12 else float('nan')
        print(f"    {E:>7}:                          {m4:>6.0f}  {m12:>6.0f}")
    seeds = sorted({s["seed"] for s in solved})
    def tok(E, D, sd):
        v = [s["reasoning_tokens"] for s in solved if s["encode"] == E and s["depth"] == D and s["seed"] == sd]
        return v[0] if v else None
    text, comp, total = [], [], []
    for sd in seeds:
        for D in (4, 12):
            e0, ed, el = tok("E0", D, sd), tok("E3dead", D, sd), tok("E3live", D, sd)
            if None not in (e0, ed, el):
                text.append(ed - e0); comp.append(el - ed); total.append(el - e0)
    print("\n  DECOMPOSITION of the encode effect (paired, pooled over depth):")
    for name, arr in [("text-cost  (E3dead - E0)   = expr TEXT present, ignored", text),
                      ("compute-cost (E3live - E3dead) = same text, must EVALUATE", comp),
                      ("total encode (E3live - E0)", total)]:
        r = paired(arr)
        if r:
            med, ci, p, pos, neg, n = r
            print(f"    {name:<55} median {med:+6.1f} tok  CI[{ci[0]:+.1f},{ci[1]:+.1f}]  p={p:.3f}  ({pos}+/{neg}-/n={n})")
    rt = paired(text); rc = paired(comp)
    print("\n  VERDICT (is V6's encode load transcription or compute?):")
    if rt and rc:
        tmed, cmed = rt[0], rc[0]
        if cmed > tmed + 4 and rc[2] < 0.1:
            print(f"    COMPUTE-DRIVEN: compute-cost {cmed:+.0f} > text-cost {tmed:+.0f} -> evaluating the expression costs reasoning_tokens")
            print(f"    beyond merely carrying its text. The encode load is genuinely COMPUTATIONAL, not transcription. (Supports the camera.)")
        elif tmed > cmed + 4:
            print(f"    TEXT/TRANSCRIPTION-DRIVEN: text-cost {tmed:+.0f} > compute-cost {cmed:+.0f} -> V6's encode effect was mostly the")
            print(f"    expression TEXT being present, not computing it. reasoning_tokens here index transcription/attention. (Demote.)")
        else:
            print(f"    MIXED: text {tmed:+.0f} ~ compute {cmed:+.0f} -- both contribute; report the split, escalate seeds.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--tier", default="high")
    a = ap.parse_args()
    if not a.run:
        sys.exit("pass --run: ~96 gpt-5.5 calls (3x2 x 16 seeds), ~$2.4")
    items, lk = load_locked()
    if a.tier != lk.get("tier_preregistered", "high"):
        sys.exit(f"TIER MISMATCH: {a.tier} vs locked {lk.get('tier_preregistered')}")
    print(f"locked: {lk['n_items']} items, seeds={lk['seeds']}, sha256={lk['sha256'][:16]}...")
    stream = run(items, a.tier)
    analyze(stream)
    print(f"\n  wrote v6b_run.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    main()
