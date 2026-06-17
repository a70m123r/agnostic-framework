#!/usr/bin/env python3
"""Probe the two V2 athletes: GPT-5.5 (OpenAI API) + qwen3.5:27b (local ollama).
Confirm each drives, returns an answer, and reports the TOKEN usage we need as the
reasoning-effort / residue signal. A tiny call each — no harness yet."""
import os, json, urllib.request, urllib.error, time
KEY = os.environ.get("OPENAI_API_KEY", "")
Q = "What is 7 times 8? Reply with only the number."

def openai_chat(model, effort=None):
    payload = {"model": model, "messages": [{"role": "user", "content": Q}]}
    if effort: payload["reasoning_effort"] = effort
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, method="POST")
    t = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return resp, round(time.time() - t, 1)

print("=== A. OpenAI GPT-5.5 (chat/completions) ===")
for model in ["gpt-5.5", "gpt-5.5-chat", "gpt-5"]:
    for eff in [None, "low"]:
        try:
            resp, dt = openai_chat(model, eff)
            u = resp.get("usage", {})
            rt = (u.get("completion_tokens_details") or {}).get("reasoning_tokens")
            ans = resp["choices"][0]["message"]["content"][:40]
            print(f"  [{model} effort={eff}] OK in {dt}s | answer={ans!r} | "
                  f"prompt={u.get('prompt_tokens')} completion={u.get('completion_tokens')} reasoning_tokens={rt}")
            break
        except urllib.error.HTTPError as e:
            print(f"  [{model} effort={eff}] HTTP {e.code}: {e.read().decode('utf-8','replace')[:140]}")
        except Exception as e:
            print(f"  [{model} effort={eff}] {type(e).__name__}: {str(e)[:120]}")
    else:
        continue
    break

print("\n=== B. ollama qwen3.5:27b (local) ===")
try:
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=json.dumps({"model": "qwen3.5:27b-q4_K_M", "prompt": Q, "stream": False,
                         "options": {"num_predict": 256}}).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    t = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.loads(r.read().decode("utf-8"))
    dt = round(time.time() - t, 1)
    print(f"  [qwen3.5:27b] OK in {dt}s | answer={resp.get('response','')[:60]!r}")
    print(f"    prompt_eval_count={resp.get('prompt_eval_count')} eval_count(gen tokens)={resp.get('eval_count')} "
          f"total_duration_s={round((resp.get('total_duration') or 0)/1e9,1)}")
except Exception as e:
    print(f"  [qwen3.5:27b] {type(e).__name__}: {str(e)[:160]}")
