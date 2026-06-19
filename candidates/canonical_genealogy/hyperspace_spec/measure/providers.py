#!/usr/bin/env python3
"""
Multi-provider solve layer for the latent camera, via OpenRouter (one OpenAI-compatible key -> the whole
cheap cross-model spectrum). Reads the key from $OPENROUTER_API_KEY or the gitignored ./.openrouter_key file
(NEVER committed). Every model here returns reasoning_tokens (the camera's signal) in
usage.completion_tokens_details.reasoning_tokens -- verified by smoke test 2026-06-18.

Pricing is $/token (multiply by 1e6 for $/Mtok); pulled live-able from OpenRouter /models. The cheap trio +
gpt-5.5 (expensive, the prior series) for back-comparison. cost-estimate gate: estimate(...) BEFORE any run.
"""
import os, json, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _key():
    k = os.environ.get("OPENROUTER_API_KEY", "")
    if not k:
        f = HERE / ".openrouter_key"
        if f.exists():
            k = f.read_text().strip()
    return k


# model registry: short -> (OpenRouter slug, $/input-token, $/output-token). Reasoning/thinking models only.
MODELS = {
    "deepseek": ("deepseek/deepseek-v4-flash",            0.09e-6, 0.18e-6),   # cheapest; clean reasoner
    "qwen":     ("qwen/qwen3-30b-a3b-thinking-2507",      0.08e-6, 0.40e-6),   # explicit thinking
    "gemini":   ("google/gemini-2.5-flash-lite",          0.10e-6, 0.40e-6),   # thoughts tokens
    "gpt5":     ("openai/gpt-5.5",                         5.00e-6, 25.0e-6),   # expensive; the prior series
}
CHEAP3 = ["deepseek", "qwen", "gemini"]
URL = "https://openrouter.ai/api/v1/chat/completions"


def solve(prompt, model="deepseek", effort="high", max_tokens=16000):
    """One clean single-shot call. Returns the camera's usage dict (reasoning_tokens = the signal).
    `effort` maps the harness 'xhigh' down to OpenRouter's 'high' (the max these models accept)."""
    slug = MODELS[model][0]
    eff = "high" if effort in ("xhigh", "max", "high") else effort
    body = {"model": slug, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": eff}, "max_tokens": max_tokens}
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json",
                 "HTTP-Referer": "https://localhost/latent-camera", "X-Title": "latent-camera"}, method="POST")
    t = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.loads(r.read().decode("utf-8"))
    if "choices" not in resp:
        raise RuntimeError("no choices: " + json.dumps(resp)[:200])
    u = resp.get("usage", {})
    msg = resp["choices"][0]["message"]
    return {"content": msg.get("content") or "",
            "reasoning": msg.get("reasoning") or "",
            "finish": resp["choices"][0].get("finish_reason"),
            "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
            "completion_tokens": u.get("completion_tokens"),
            "prompt_tokens": u.get("prompt_tokens"),
            "model": model, "slug": slug, "seconds": round(time.time() - t, 1)}


def estimate(prompts, model, repeats, est_out_tokens=600):
    """$ estimate for running `prompts` x `repeats` on `model`. Input tokens from the prompts (chars/4 proxy);
    output tokens assumed (the dominant uncertainty) -- report a band by varying est_out_tokens."""
    slug, pin, pout = MODELS[model]
    in_tok = sum(max(1, round(len(p) / 4)) for p in prompts) * repeats
    calls = len(prompts) * repeats
    out_tok = calls * est_out_tokens
    cost = in_tok * pin + out_tok * pout
    return {"model": model, "slug": slug, "calls": calls, "input_tokens": in_tok,
            "est_output_tokens": out_tok, "est_cost_usd": round(cost, 4)}


def estimate_table(prompts, repeats, models=None, out_lo=300, out_hi=1200):
    """print a lean->heavy cost band per model (the pre-run gate)."""
    models = models or (CHEAP3 + ["gpt5"])
    print(f"  COST ESTIMATE  ({len(prompts)} items x {repeats} reps = {len(prompts)*repeats} calls)")
    print(f"  {'model':>10}  {'slug':<38} {'input tok':>10}  {'$ lean':>8}  {'$ heavy':>8}")
    for m in models:
        lo = estimate(prompts, m, repeats, out_lo); hi = estimate(prompts, m, repeats, out_hi)
        print(f"  {m:>10}  {MODELS[m][0]:<38} {lo['input_tokens']:>10,}  {lo['est_cost_usd']:>8.3f}  {hi['est_cost_usd']:>8.3f}")
    print(f"  (band = output {out_lo}->{out_hi} tok/call; output dominates cost. cheap models reason MORE so lean toward heavy.)")


if __name__ == "__main__":
    import sys
    print("key present:", bool(_key()))
    print("models:", {k: v[0] for k, v in MODELS.items()})
    if "--smoke" in sys.argv:
        r = solve("Compute 13+29. Output ONLY the number.", model="deepseek")
        print("deepseek smoke:", {k: r[k] for k in ("content", "reasoning_tokens", "completion_tokens", "seconds")})
