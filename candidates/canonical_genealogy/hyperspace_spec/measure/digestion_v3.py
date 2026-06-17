#!/usr/bin/env python3
"""
V3 — the multi-runner Latent Olympics (3 fast frontier athletes that actually terminate).

Fixes the qwen confound (it truncated) with: gpt-5.5 (OpenAI API, == codex model),
Claude (claude -p --output-format json, subscription, NO api key, ToS-compliant headless),
gemini (CLI). Same graded battery + the random stone. Verified-dissolve gate
(answer == ground truth). Per-call timeout = effort ceiling (hitting it = floor signal).

Clean outputs: the UNIVERSAL RESIDUE (resists ALL 3), the universal-solve set (all dissolve),
the split set (provider-dependent difficulty), the leaderboard, and where comparable, the
cross-provider difficulty signal (the pinned relational bit). Synthetic targets.
"""
import sys, json, subprocess, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from digestion_v2 import BATTERY, last_int, verify, openai_solve, HERE

TIMEOUT = 90

def run_openai(prompt):
    try:
        reply, rt, dt = openai_solve(prompt, "medium")
        return reply, rt, dt, False
    except Exception:
        return "", None, float(TIMEOUT), True       # timeout = effort-exhausted (floor)

def run_claude(prompt):
    t = time.time()
    try:
        r = subprocess.run(["claude", "-p", prompt, "--output-format", "json"],
                           capture_output=True, text=True, timeout=TIMEOUT, stdin=subprocess.DEVNULL)
        j = json.loads(r.stdout)
        ans = j.get("result", "")
        toks = (j.get("usage") or {}).get("output_tokens")
        return ans, toks, round(time.time()-t, 1), False
    except subprocess.TimeoutExpired:
        return "", None, float(TIMEOUT), True
    except Exception as e:
        return f"ERR:{type(e).__name__}", None, round(time.time()-t, 1), False

def run_gemini(prompt):
    t = time.time()
    try:
        # cmd /c resolves the gemini.cmd npm shim; LIST form (no shell=True) -> the prompt is a quoted
        # arg, never shell-interpreted (no injection). run from hyperspace_spec, not D:\ root (trust/root-scan).
        r = subprocess.run(["cmd", "/c", "gemini", "--skip-trust", "-p", prompt],
                           capture_output=True, text=True, timeout=TIMEOUT,
                           stdin=subprocess.DEVNULL, cwd=str(HERE.parent))
        return r.stdout.strip(), None, round(time.time()-t, 1), False
    except subprocess.TimeoutExpired:
        return "", None, float(TIMEOUT), True
    except Exception as e:
        return f"ERR:{type(e).__name__}", None, round(time.time()-t, 1), False

RUNNERS = [("gpt-5.5", run_openai), ("claude", run_claude), ("gemini", run_gemini)]

def main():
    stream = []
    solved = {r: set() for r, _ in RUNNERS}
    print("=== V3 — multi-runner Olympics (gpt-5.5 / claude / gemini) ===\n")
    for tid, diff, prompt, ans, kind in BATTERY:
        line = f"  [{tid:11s} d{diff} {kind:15s}]"
        for rname, fn in RUNNERS:
            reply, eff, dt, ex = fn(prompt)
            ok = (False if ex else verify(ans, reply))
            a = (None if ex else last_int(reply))
            if ok: solved[rname].add(tid)
            stream.append({"provider": rname, "target": tid, "difficulty": diff, "kind": kind,
                           "effort": eff, "seconds": dt, "answer": a, "correct": ok, "exhausted": ex})
            mark = "CEIL" if ex else ("OK" if ok else ("x" if ok is False else "NA"))
            line += f"  {rname}:{mark}{'' if a is None else '('+str(a)+')'}/{dt}s"
        print(line)
    # cross-provider analysis
    all_t = [t[0] for t in BATTERY]
    universal_residue = [t for t in all_t if not any(t in solved[r] for r, _ in RUNNERS)]
    universal_solve   = [t for t in all_t if all(t in solved[r] for r, _ in RUNNERS)]
    split             = [t for t in all_t if t not in universal_residue and t not in universal_solve]
    print(f"\n  leaderboard (verified dissolves): " + " | ".join(f"{r}:{len(solved[r])}/{len(all_t)}" for r,_ in RUNNERS))
    print(f"  UNIVERSAL SOLVE (all 3 dissolve): {universal_solve}")
    print(f"  SPLIT (provider-dependent):       {split}")
    print(f"  UNIVERSAL RESIDUE (resists ALL 3): {universal_residue}  <- the near-objective hard content")
    (HERE/"v3_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream)+"\n", encoding="utf-8")
    print(f"  wrote v3_run.jsonl ({len(stream)} records)")

if __name__ == "__main__":
    main()
