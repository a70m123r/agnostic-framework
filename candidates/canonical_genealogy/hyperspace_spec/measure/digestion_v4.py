#!/usr/bin/env python3
"""
V4 — the Parametric Difficulty Ladder, REVISED per the codex+gemini external pass.

ONE primary estimand (no estimand drift):
    partial-Spearman(reasoning_tokens @ FIXED 'high', effective_ops | display_ops, prompt_words)
    on SOLVED items only.
Failures are a SEPARATE binary outcome (solve-rate), NEVER converted into fake high effort
(the censoring-manufactures-monotonicity trap). Everything else (raw Spearman, low/med curves,
solve-rate by band) is explicitly SECONDARY.

Pre-registration: the grid + every answer are frozen in v4_labels.LOCK (sha256). This harness
REBUILDS the grid from the locked seed count and REFUSES to run unless the hash matches -> the
run is bound to the pre-registered labels. gpt-5.5 only (the sole runner emitting reasoning_tokens).
Synthetic data (authorized). Spends OPENAI_API_KEY. Requires an explicit --smoke or --run flag.
"""
import sys, json, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from digestion_v2 import openai_solve, verify, last_int          # exact reuse
from v4_generator import build_grid, canonical_labels, lock_digest
from v4_stats import partial_spearman, bootstrap_ci, perm_pvalue, raw_spearman
import numpy as np


def load_locked():
    lockp = HERE / "v4_labels.LOCK"
    if not lockp.exists():
        sys.exit("no v4_labels.LOCK -- run: python v4_generator.py --lock --seeds N  first.")
    lock = json.loads(lockp.read_text(encoding="utf-8"))
    items = build_grid(lock["seeds"])
    digest = lock_digest(canonical_labels(items))
    if digest != lock["sha256"]:
        sys.exit(f"LOCK MISMATCH: rebuilt {digest[:16]} != locked {lock['sha256'][:16]}. The generator "
                 f"changed after pre-registration; this is a supersession, not a run.")
    return items, lock


def run(items, tier="high", limit=None):
    stream = []
    todo = items[:limit] if limit else items
    print(f"=== V4 run: {len(todo)} items @ effort='{tier}' (gpt-5.5) ===")
    for i, it in enumerate(todo):
        exhausted = False
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier)
        except Exception as e:
            reply, rt, dt, exhausted = "", None, 100.0, True
        ok = (False if exhausted else verify(it["answer"], reply))
        a = (None if exhausted else last_int(reply))
        rec = {"target": it["item_id"], "family": it["family"],
               "effective_ops": it["effective_ops"], "display_ops": it["display_ops"],
               "prompt_words": it["prompt_words"], "seed": it["seed"], "tier": tier,
               "reasoning_tokens": rt, "answer": a, "expected": it["answer"],
               "correct": ok, "exhausted": exhausted, "seconds": dt}
        stream.append(rec)
        if (i + 1) % 10 == 0 or i + 1 == len(todo):
            ns = sum(1 for s in stream if s["correct"])
            print(f"  [{i+1:>3}/{len(todo)}] solved={ns} last: E{it['effective_ops']} T{it['display_ops']} -> {'OK' if ok else ('CEIL' if exhausted else 'x')}({a}/{it['answer']}) {rt}t")
    return stream


def analyze(stream, label="V4"):
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    n_all, n_solved = len(stream), len(solved)
    print(f"\n=== {label} ANALYSIS ===")
    print(f"  solved {n_solved}/{n_all} ({100*n_solved/max(1,n_all):.0f}%)")
    if n_solved < 10:
        print("  too few solved items for the primary estimand (need >=10). Report solve-rate only.")
    else:
        eff = [s["reasoning_tokens"] for s in solved]
        E   = [s["effective_ops"] for s in solved]
        T   = [s["display_ops"] for s in solved]
        W   = [s["prompt_words"] for s in solved]
        rng = np.random.default_rng(7)
        rho = partial_spearman(eff, E, [T, W])
        ci  = bootstrap_ci(eff, E, [T, W], rng, n=2000)
        p, _ = perm_pvalue(eff, E, [T, W], rng, n=5000)
        raw = raw_spearman(eff, E)
        rawT = raw_spearman(eff, T)
        print(f"  PRIMARY partial-Spearman(effort, effective_ops | display_ops, prompt_words) = {rho:+.3f}")
        print(f"          bootstrap 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]   permutation p = {p:.4f}")
        print(f"  SECONDARY raw Spearman(effort, effective_ops) = {raw:+.3f}   raw Spearman(effort, display_ops) = {rawT:+.3f}")
        print(f"          read: if PRIMARY >> 0 and CI excludes 0 -> effort tracks EFFECTIVE difficulty net of length.")
        print(f"                if raw(effort,display_ops) is large but PRIMARY ~ 0 -> effort tracked LENGTH (the tautology).")
    # solve-rate by effective_ops band (the separate binary outcome; failures NOT faked into effort)
    print("  solve-rate by effective_ops band:")
    for e in sorted({s["effective_ops"] for s in stream}):
        rows = [s for s in stream if s["effective_ops"] == e]
        sv = sum(1 for s in rows if s["correct"])
        toks = [s["reasoning_tokens"] for s in rows if s["correct"] and s["reasoning_tokens"] is not None]
        mt = f"{np.median(toks):.0f}" if toks else "-"
        print(f"     E={e:>2}: solved {sv}/{len(rows)}  median reasoning_tokens(solved)={mt}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", type=int, default=0, help="run only the first N items (cheap end-to-end check)")
    ap.add_argument("--run", action="store_true", help="run the FULL locked grid (spends API)")
    ap.add_argument("--tier", default="high")
    a = ap.parse_args()
    items, lock = load_locked()
    pre_tier = lock.get("tier_preregistered", "high")
    if a.tier != pre_tier:
        sys.exit(f"TIER MISMATCH: --tier={a.tier} but the lock pre-registered tier='{pre_tier}'. "
                 f"The effort tier is the central manipulation; running a different tier is a supersession, not the locked run.")
    print(f"locked: {lock['n_items']} items, seeds={lock['seeds']}, tier={pre_tier}, sha256={lock['sha256'][:16]}...")
    if a.smoke:
        step = max(1, len(items) // a.smoke)           # stride across E-bands, not first-N (which are all E=2)
        sub = items[::step][:a.smoke]
        stream = run(sub, tier=a.tier)
        out = HERE / "v4_smoke.jsonl"
    elif a.run:
        stream = run(items, tier=a.tier)
        out = HERE / "v4_run.jsonl"
    else:
        sys.exit("pass --smoke N (cheap) or --run (full grid, spends API).")
    out.write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream, label=("V4-SMOKE" if a.smoke else "V4"))
    print(f"\n  wrote {out.name} ({len(stream)} records)")


if __name__ == "__main__":
    main()
