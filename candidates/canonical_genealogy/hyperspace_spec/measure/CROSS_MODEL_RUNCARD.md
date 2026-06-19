# Cross-model run-card — the exact models + parameters (keep score)

**Date:** 2026-06-19 | The authoritative record of WHAT was run with WHICH parameters, so every result is
reproducible and comparable. Two eras: the gpt-5.5 series (V4–V9d, OpenAI API) and the cheap cross-model
spectrum (V10/V11, OpenRouter).

## The measurement signal (both eras)
`reasoning_tokens` = `usage.completion_tokens_details.reasoning_tokens` (hidden reasoning effort).
Answer = `choices[0].message.content`; hidden reasoning text = `choices[0].message.reasoning` (OpenRouter)
or interleaved (OpenAI). `_last_int(content)` extracts the final integer. Verified (codex audit): content
holds the bare answer, reasoning is a separate field → no parse contamination.

## ERA 2 — the cheap cross-model spectrum (V10, V11) — via OpenRouter
- **Endpoint:** `https://openrouter.ai/api/v1/chat/completions` (OpenAI-compatible). Key: gitignored
  `measure/.openrouter_key` ($30 cap). Provider layer: `providers.py`.
- **Request params (every call):** `reasoning: {effort: "high"}`, `max_tokens: 16000`. (The harness 'xhigh'
  maps to 'high' — OpenRouter cheap models cap reasoning at 'high'.) Headers: HTTP-Referer + X-Title.
- **Models selected (slug · $/Mtok in · $/Mtok out · reasoning-tokens confirmed):**

| short | OpenRouter slug | $/M in | $/M out | reasoning tokens? | role |
|---|---|---|---|---|---|
| **deepseek** | `deepseek/deepseek-v4-flash` | 0.09 | 0.18 | yes (137 in smoke) | primary cheap; clean answerer |
| **qwen** | `qwen/qwen3-30b-a3b-thinking-2507` | 0.08 | 0.40 | yes (1287) | explicit thinking |
| **gemini** | `google/gemini-2.5-flash-lite` | 0.10 | 0.40 | yes (625) | thoughts tokens |
| (gpt5) | `openai/gpt-5.5` | 5.00 | 25.0 | yes | NOT run via OpenRouter (the Era-1 series) |

- **Run config:** V10 = 8 conds × **14 seeds × 4 reps** = 448 calls/model; V11 = 6 conds × 14 × 4 = 336
  calls/model. **workers:** 16 (deepseek), 12 (qwen, gemini). 3-try retry + `exhausted` flag (excluded from
  accuracy). Output: `v10fs_run.<model>.jsonl`, `v11_run.<model>.jsonl`.
- **Locks (sha256):** V10 `cb7ecfdd` (AFTER the F0 fix — see below; was `9fedb5d8` before). V11 `b790f43a`.
- **Stats:** per-seed mean over reps on **correct calls only**; paired bootstrap (4000 samples) median CI +
  exact two-sided sign test over the 14 seeds.
- **Effort fidelity caveat (flagged by gemini-pro audit, unresolved):** whether OpenRouter's `effort:"high"`
  actually engages a costlier mode per backend is unverified; treat reasoning_tokens as the model's reported
  count, not a guaranteed depth.

### ⚠ F0-falsifier bug + fix (keep score — what is clean vs compromised)
codex's audit found V10's F0 (compute-free) condition was **NOT fully compute-free**: only the 6 task chains
got `=> final`; the ~11 filler arithmetic lines lacked finals (still computable). **Common-mode** (both F0
arms), so the falsifier *delta* is probably unbiased, but the clean test was never run.
- **FIXED 2026-06-19:** all F0 arithmetic lines now render with `=>` (+ a selftest guard); V10 re-locked
  `cb7ecfdd`.
- **Status of runs: RESOLVED 2026-06-19.** Clean V10 re-run (fixed F0) completed on all 3 models;
  `v10fs_run.<model>.jsonl` now hold the clean data. The bug-fix **flipped deepseek's falsifier −47 (buggy) →
  +149 (clean)**. Both subscription audits (codex + Claude-subagent) verified the clean run, re-derived the
  falsifier, and refuted the reading-volume confound. Clean falsifier: deepseek +149 (p=.057), gemini +2303
  (p<.001), qwen +376 (NS) — see V10_V11_CROSSMODEL_RESULTS.md.

## ERA 1 — the gpt-5.5 series (V4 → V9d) — via OpenAI API (for the record)
- **Endpoint:** OpenAI `/v1/chat/completions`, model `gpt-5.5`. Key: `OPENAI_API_KEY` (now
  `insufficient_quota` — exhausted ~$40 of usage).
- **Params:** `reasoning_effort: "xhigh"` (the un-clipped tier; 'high' pins reasoning at 512), and for the
  later runs `max_completion_tokens: 16000`. reasoning_tokens from the same usage path.
- **Run config (typical):** 4 conds × 14 seeds × 4 reps ≈ 448 calls (V9b/V9d); workers 8.
- These results (V4–V9d) are NOT directly comparable in MAGNITUDE to Era 2 (different model, different
  verbosity) — only the within-model deltas compare in sign/significance (the V3 provider-invariance logic).

## Results (Era 2, CLEAN) — full write-up in V10_V11_CROSSMODEL_RESULTS.md
- **V10:** a real **compute-free residual frame-cost** (clean F0 falsifier), **model-dependent** — gemini
  +2303 (14/14, p<.001) rock-solid, deepseek +149 (p=.057) borderline, qwen +376 NS. NOT reading-volume (both
  audits refuted: dissolved is shorter yet costs more). A separate UNIVERSAL reading-volume cost (size axis
  +2578/+4377/+3068). Residual confound (both audits): F0_DISSOLVED also moves the selector to trailing →
  "frame-orienting vs late-instruction rescan" unresolved → next control V10b = compute-free 2x2
  {header present/absent} x {instruction leading/trailing}.
- **V11:** invalid-as-designed across ALL 3 models — NOVEL−NAMED negative everywhere (−70/−234/−196); the
  novel digit-sum predicate is intrinsically cheaper than primality (predicate-difficulty confound). Next
  control V11b = a novel predicate compute-matched to primality.
