#!/usr/bin/env python3
"""
NF-C1 FIX (both audits' #1 methodological note): re-score NF on a COMPUTE endpoint -- the count of
trial-division markers in the reasoning TEXT -- instead of reasoning_tokens, which conflate compute with
NARRATION LENGTH (the confound that sank the 'word shortcut'). No new API calls: the reasoning text is saved
in v_nf_run.*.jsonl.

Marker = a divisibility/trial-division event in the CoT (divisib*, remainder, mod, '/N', '÷N'). The bare chain
operator '% 1000' is deliberately NOT counted; and any common restatement cancels in the WITHIN-seed delta.

KEY TEST -- HARD_WORD vs HARD_PLAIN:
  if MARKER delta ~ 0 while RT delta is negative (WORD cheaper in tokens) -> the 'word shortcut' is pure
  narration length, NOT a compute/amortization saving -> NF-C1 DEMOTION CONFIRMED.
  if HARD_WORD has FEWER markers -> the cached word genuinely cuts trial-division work -> amortization rescued.
"""
import json, re, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import paired

CONDS = ["TRIV_PLAIN", "TRIV_NONCE", "HARD_PLAIN", "HARD_NONCE", "HARD_WORD"]
DIV = re.compile(r'(?:divisib\w*|divides|divided|\bremainder\b|\bmod(?:ulo)?\b|[/÷]\s*\d+|prime\s+factor|trial[- ]divi)', re.I)


def markers(t):
    return len(DIV.findall(t or ""))


def load(m):
    return [json.loads(l) for l in (HERE / f"v_nf_run.{m}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def seed_means(recs, fn):
    out = {}
    for r in recs:
        if not r.get("correct"):
            continue
        out.setdefault(r["cond"], {}).setdefault(r["seed"], []).append(fn(r))
    return {c: {s: float(np.mean(v)) for s, v in d.items()} for c, d in out.items()}


def delta(sm, a, b):
    seeds = sorted(set(sm.get(a, {})) & set(sm.get(b, {})))
    return paired([sm[a][s] - sm[b][s] for s in seeds])


for m in ["deepseek", "qwen", "gemini"]:
    recs = load(m)
    mk = seed_means(recs, lambda r: markers(r.get("reasoning")))
    rt = seed_means(recs, lambda r: r.get("reasoning_tokens") or 0)
    print(f"\n==== {m} ====")
    print("  cond           median_MARKERS   median_RT")
    for c in CONDS:
        mks = [markers(r.get("reasoning")) for r in recs if r["cond"] == c and r.get("correct")]
        rts = [r["reasoning_tokens"] for r in recs if r["cond"] == c and r.get("correct") and r.get("reasoning_tokens")]
        print(f"    {c:<12}   {np.median(mks):>8.1f}        {np.median(rts):>8.0f}")
    print("  contrast              MARKERS (compute)        RT (tokens)")
    for a, b, why in [("HARD_WORD", "HARD_PLAIN", "WORD shortcut"),
                      ("HARD_NONCE", "HARD_PLAIN", "NONCE @ hard"),
                      ("HARD_PLAIN", "TRIV_PLAIN", "compute (hard-triv)")]:
        rm, rr = delta(mk, a, b), delta(rt, a, b)
        print(f"    {a:>10}-{b:<10} [{why:<16}] MARK {rm[0]:+6.1f} p={rm[2]:.3f}  |  RT {rr[0]:+7.0f} p={rr[2]:.3f}")
