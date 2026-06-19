#!/usr/bin/env python3
"""
3-WAY cross-experiment comparison at MATCHED frame/size conditions, on the SAME seeds:
  V10  prime   (v10fs_run.<m>.jsonl) = apply predicate          : APPLICATION + locate + read
  V10b lookup  (v10b_run.<m>.jsonl)  = different task            : locate-by-name + read
  SV   verdict (v_sv_run.<m>.jsonl)  = same task, no application : locate-by-PASS + read
All three share v10_framestrip._make(seed) -> identical 6 chains + needle per seed, so the per-seed paired
contrast is clean. Headline: D_application = rt(prime) - rt(verdict)  (cost of applying primality, TASK HELD
FIXED -- the clean subtraction V10b could not make). Secondary: verdict vs lookup (does same-task-no-apply
differ from different-task-no-apply?), and whether SV's frame/size deltas survive (application-independent cost).
"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import paired

MATCH = ["F3_FRAMED", "FP_POINTED", "F2_DEINDEXED", "F1_S", "F1_M", "F1_L"]
SRC = {"prime": "v10fs_run.{m}.jsonl", "lookup": "v10b_run.{m}.jsonl", "verdict": "v_sv_run.{m}.jsonl"}


def load(path):
    p = HERE / path
    if not p.exists():
        return None
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def seed_means(recs):
    """{cond: {seed: mean rt over correct reps}}"""
    out = {}
    for r in recs:
        if not r.get("correct") or r.get("reasoning_tokens") is None:
            continue
        out.setdefault(r["cond"], {}).setdefault(r["seed"], []).append(r["reasoning_tokens"])
    return {c: {s: float(np.mean(v)) for s, v in d.items()} for c, d in out.items()}


def med(recs, cond):
    tk = [r["reasoning_tokens"] for r in recs if r["cond"] == cond and r.get("correct") and r.get("reasoning_tokens") is not None]
    return np.median(tk) if tk else float("nan")


def paired_delta(a_sm, b_sm, cond):
    a, b = a_sm.get(cond, {}), b_sm.get(cond, {})
    seeds = sorted(set(a) & set(b))
    d = [a[s] - b[s] for s in seeds]
    return paired(d)


def main():
    for m in ["deepseek", "gemini", "qwen"]:
        data = {k: load(v.format(m=m)) for k, v in SRC.items()}
        missing = [k for k, v in data.items() if v is None]
        if missing:
            print(f"\n### {m}: MISSING {missing} -- skip until run"); continue
        sm = {k: seed_means(v) for k, v in data.items()}
        print(f"\n================= {m} =================")
        print(f"  {'cond':>13} {'prime':>8} {'lookup':>8} {'verdict':>8}   {'D_app(prime-verdict)':>22}  {'verdict-lookup':>16}")
        for c in MATCH:
            mp, ml, mv = med(data["prime"], c), med(data["lookup"], c), med(data["verdict"], c)
            da = paired_delta(sm["prime"], sm["verdict"], c)
            vl = paired_delta(sm["verdict"], sm["lookup"], c)
            da_s = f"{da[0]:+8.0f} p={da[2]:.3f}" if da else "n/a"
            vl_s = f"{vl[0]:+7.0f} p={vl[2]:.3f}" if vl else "n/a"
            print(f"  {c:>13} {mp:>8.0f} {ml:>8.0f} {mv:>8.0f}   {da_s:>22}  {vl_s:>16}")
        # SV's own frame/size deltas (does application-free cost survive, same task?)
        print("  SV (verdict) internal -- application-free, same task:")
        sv = sm["verdict"]
        for a, b, why in [("F1_S", "F2_DEINDEXED", "D_frame"), ("F1_M", "F1_S", "size 1x->2.5x"),
                          ("F1_L", "F1_M", "size 2.5x->5x")]:
            aa, bb = sv.get(a, {}), sv.get(b, {})
            seeds = sorted(set(aa) & set(bb)); d = [aa[s] - bb[s] for s in seeds]; rr = paired(d)
            print(f"     {a:>12} - {b:<12} {rr[0]:+8.1f} CI[{rr[1][0]:+.0f},{rr[1][1]:+.0f}] p={rr[2]:.3f} (n={rr[5]})  {why}" if rr else f"     {a}-{b} n/a {why}")


if __name__ == "__main__":
    main()
