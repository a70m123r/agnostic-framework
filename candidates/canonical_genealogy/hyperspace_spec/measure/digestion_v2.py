#!/usr/bin/env python3
"""
V2 — the slow-digestion / reasoning-effort axis (the Latent Olympics).

V1 measured rho(PRIOR): dissolve as you hand over context. V2 measures rho(EFFORT):
dissolve as the observer THINKS HARDER. Athletes (providers) digest a graded battery;
we sweep reasoning effort, apply the VERIFIED-DISSOLVE gate (answer == ground truth,
exact), and record effort-to-dissolve. Outputs: rho(effort) per target, effort-tracks-
difficulty, the Olympics leaderboard, the UNIVERSAL RESIDUE (resists every athlete).

Athletes: openai gpt-5.5 (fast, reasoning_tokens reported) + ollama qwen3.5:27b (local,
slow -> subset). Synthetic targets. Spends Pav's OPENAI_API_KEY (authorized).
"""
import os, json, re, time, urllib.request, urllib.error, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = os.environ.get("OPENAI_API_KEY", "")
random.seed(11)
RAND_SEQ = [random.randint(10, 99) for _ in range(6)]   # no rule -> the floor

# battery: (id, difficulty 1..5, prompt, answer or None for the no-ground-truth stone, kind)
BATTERY = [
    ("g1_add",   1, "Compute 13 + 29. Reply with ONLY the final number.", 42, "easy"),
    ("g2_speed", 2, "A train travels 60 km in 1.5 hours. What is its average speed in km/h? Reply with ONLY the number.", 40, "medium"),
    ("g3_batball",4,"A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How many CENTS does the ball cost? Reply with ONLY the number.", 5, "hard-trap"),
    ("d1_seq",   3, "What is the next number in the sequence 2, 6, 12, 20, 30, ? Reply with ONLY the number.", 42, "deep-structured"),
    ("s1_random",5, f"What is the next number in the sequence {', '.join(map(str,RAND_SEQ))}, ? Reply with ONLY the number.", None, "random-floor"),
]

def last_int(s):
    m = re.findall(r"-?\d+", s or "")
    return int(m[-1]) if m else None

def verify(target_ans, reply):
    if target_ans is None:
        return None            # no ground truth (the random floor) -> never a verified dissolve
    return last_int(reply) == target_ans

def openai_solve(prompt, effort):
    payload = {"model": "gpt-5.5", "messages": [{"role": "user", "content": prompt}]}
    if effort: payload["reasoning_effort"] = effort
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, method="POST")
    t = time.time()
    with urllib.request.urlopen(req, timeout=100) as r:   # ceiling: hitting it = effort-exhausted (a floor signal)
        resp = json.loads(r.read().decode("utf-8"))
    u = resp.get("usage", {})
    rt = (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
    return resp["choices"][0]["message"]["content"], rt, round(time.time()-t, 1)

def ollama_solve(prompt, budget=512):
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=json.dumps({"model": "qwen3.5:27b-q4_K_M", "prompt": prompt, "stream": False,
                         "options": {"num_predict": budget}}).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    t = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return resp.get("response", ""), resp.get("eval_count") or 0, round(time.time()-t, 1)

def run_openai(stream):
    EFFORTS = ["low", "medium", "high"]
    print("=== GPT-5.5 — rho(effort) sweep ===")
    for tid, diff, prompt, ans, kind in BATTERY:
        row = []
        first_correct_tok = None
        for eff in EFFORTS:
            exhausted = False
            try:
                reply, rt, dt = openai_solve(prompt, eff)
            except urllib.error.HTTPError as e:
                try: reply, rt, dt = openai_solve(prompt, None)          # unsupported effort -> default once
                except Exception: reply, rt, exhausted = "", None, True
            except Exception:                                            # timeout = effort ceiling hit, no dissolve
                reply, rt, exhausted = "", None, True
            ok = (False if exhausted else verify(ans, reply))
            a  = (None if exhausted else last_int(reply))
            if ok and first_correct_tok is None: first_correct_tok = rt
            row.append((eff, rt, ok, a, exhausted))
            stream.append({"provider":"gpt-5.5","target":tid,"difficulty":diff,"kind":kind,
                           "effort":eff,"reasoning_tokens":rt,"answer":a,"correct":ok,"effort_exhausted":exhausted})
        marks = " ".join(f"{e}:{('CEIL' if ex else ('OK' if ok else ('x' if ok is False else 'NA')))}{'' if rt is None else str(rt)+'t'}" for e,rt,ok,a,ex in row)
        print(f"  [{tid:11s} d{diff} {kind:15s}] {marks}   first-correct@{first_correct_tok} reasoning-tokens")
    return stream

def main():
    if not KEY:
        print("OPENAI_API_KEY not set."); sys.exit(2)
    stream = []
    run_openai(stream)
    # effort-tracks-difficulty: reasoning tokens at first-correct vs difficulty
    fc = {}
    for tid, diff, prompt, ans, kind in BATTERY:
        toks = [s["reasoning_tokens"] for s in stream if s["target"]==tid and s["correct"]]
        fc[tid] = (diff, min(toks) if toks else None)
    print("\n  effort-tracks-difficulty (reasoning tokens to FIRST correct vs difficulty):")
    for tid,(d,t) in sorted(fc.items(), key=lambda x:x[1][0]):
        print(f"    d{d}  {tid:11s}  {'DID NOT DISSOLVE (floor/failed)' if t is None else str(t)+' tokens'}")
    solved = [t for t,(d,tok) in fc.items() if tok is not None]
    floor  = [t for t,(d,tok) in fc.items() if tok is None]
    print(f"\n  dissolved by GPT-5.5: {solved}")
    print(f"  UNIVERSAL-RESIDUE candidates (resisted GPT-5.5): {floor}  (qwen3.5 cross-check pending)")
    (HERE/"v2_run.jsonl").write_text("\n".join(json.dumps(s,ensure_ascii=False) for s in stream)+"\n", encoding="utf-8")
    print(f"  wrote v2_run.jsonl ({len(stream)} records)")

if __name__ == "__main__":
    main()
