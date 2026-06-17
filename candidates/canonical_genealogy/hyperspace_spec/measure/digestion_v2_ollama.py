#!/usr/bin/env python3
"""V2 second athlete — qwen3.5:27b (local) on the discriminating subset, for the Latent Olympics
cross-provider check + the UNIVERSAL RESIDUE (does the random stone resist BOTH athletes?).
Slow (local 27B ~minutes/call) -> 3 targets only. Appends provider='qwen3.5' rows to v2_run.jsonl."""
import sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from digestion_v2 import BATTERY, ollama_solve, verify, last_int, HERE

SUBSET = {"g3_batball", "d1_seq", "s1_random"}
recs = []
for tid, diff, prompt, ans, kind in BATTERY:
    if tid not in SUBSET:
        continue
    p = prompt + " Think step by step, then end your reply with the final number."
    try:
        reply, toks, dt = ollama_solve(p, budget=900)
        ok = verify(ans, reply)
        print(f"[qwen3.5 {tid:11s}] {dt}s tokens={toks} correct={ok} ans={last_int(reply)}")
    except Exception as e:
        toks, ok = None, False
        print(f"[qwen3.5 {tid:11s}] FAILED: {type(e).__name__}: {str(e)[:120]}")
    recs.append({"provider": "qwen3.5", "target": tid, "difficulty": diff, "kind": kind,
                 "effort": "single", "reasoning_tokens": toks, "answer": last_int(reply) if 'reply' in dir() else None,
                 "correct": ok})
with open(HERE/"v2_run.jsonl", "a", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
solved = [r["target"] for r in recs if r["correct"]]
floor = [r["target"] for r in recs if not r["correct"]]
print(f"\nqwen3.5 dissolved: {solved}")
print(f"qwen3.5 resisted: {floor}")
print(f"appended {len(recs)} qwen3.5 records to v2_run.jsonl")
