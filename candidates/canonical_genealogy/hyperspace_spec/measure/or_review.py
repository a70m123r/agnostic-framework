#!/usr/bin/env python3
"""Route an external-review prompt to a STRONG model via OpenRouter (replacing the now-dead gemini CLI:
Google cut the free Code-Assist-for-individuals tier). Self-contained text-in/text-out; for audits that don't
need raw-file access (the operator embeds the data). Usage: python or_review.py <brief.txt> <out.md> [model]"""
import sys, json, urllib.request, urllib.error
from pathlib import Path
HERE = Path(__file__).resolve().parent


def _key():
    import os
    return os.environ.get("OPENROUTER_API_KEY") or (HERE / ".openrouter_key").read_text().strip()


def review(prompt, model):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], "reasoning": {"effort": "high"}, "max_tokens": 12000}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json",
                 "HTTP-Referer": "https://localhost/latent-camera", "X-Title": "latent-camera"}, method="POST")
    with urllib.request.urlopen(req, timeout=400) as r:
        resp = json.load(r)
    return resp["choices"][0]["message"].get("content") or resp["choices"][0]["message"].get("reasoning") or ""


if __name__ == "__main__":
    brief = Path(sys.argv[1]).read_text(encoding="utf-8")
    out = sys.argv[2]
    candidates = [sys.argv[3]] if len(sys.argv) > 3 else ["google/gemini-3.1-pro-preview", "google/gemini-2.5-pro", "qwen/qwen3-235b-a22b-thinking-2507"]
    for m in candidates:
        try:
            txt = review(brief, m)
            if txt.strip():
                Path(out).write_text(f"[external review via OpenRouter model: {m}]\n\n" + txt, encoding="utf-8")
                print(f"OK via {m}: {len(txt)} chars -> {out}"); break
        except urllib.error.HTTPError as e:
            print(f"  {m} HTTP {e.code}: {e.read().decode()[:120]}")
        except Exception as e:
            print(f"  {m} {type(e).__name__}: {str(e)[:120]}")
    else:
        print("all candidate models failed")
