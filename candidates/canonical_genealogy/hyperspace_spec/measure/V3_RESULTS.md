# V3 — the 3-lab cross-provider Olympics (the floor is provider-invariant)

**Date:** 2026-06-17 | **Status:** real measurement. Roster = three frontier models from three labs: **gpt-5.5** (OpenAI API), **Claude** (`claude -p --output-format json` — subscription, NO api key, ToS-compliant headless), **gemini** (CLI). Same battery + verified-dissolve gate. `digestion_v3.py` -> `v3_run.jsonl`.

## Result

| target | difficulty | gpt-5.5 | Claude | gemini |
|---|---|---|---|---|
| g1 add (13+29) | d1 | OK 42 | OK 42 | OK 42 |
| g2 speed | d2 | OK 40 | OK 40 | OK 40 |
| g3 bat-and-ball (instinct trap) | d4 | OK 5 | OK 5 | OK 5 |
| d1 sequence -> 42 | d3 | OK 42 | OK 42 | OK 42 |
| **s1 random (no rule)** | d5 | **floor (ceiling 90s)** | **floor (NA)** | **floor (NA)** |

**Leaderboard:** gpt-5.5 4/5 · Claude 4/5 · gemini 4/5. **Universal solve:** {g1,g2,g3,d1}. **Split:** none. **Universal residue:** {s1_random}.

## What it shows
**THREE INDEPENDENT LABS AGREE PERFECTLY.** All four structured targets dissolve for all three runners (including the bat-and-ball trap -> 5, not the instinct 10); the random stone resists ALL THREE. **Zero provider-dependent splits.** The aleatoric floor (the near-objective hard content) is **provider-invariant** — confirmed across OpenAI, Anthropic, and Google frontier models. This is the **pinned relational bit** at its strongest: the relational measurement (what dissolves / what is the floor) is the SAME across independent decoders, even though the absolute magnitudes (tokens, seconds) differ. It also fixes the earlier qwen confound — qwen "resisted everything" only because it truncated; three *proper* fast runners agree.

## Honest limits (folded from the codex+gemini frontier pass)
- This is the clean **SOLVE / FLOOR axis**. The cross-provider **EFFORT-RANK is NOT measured here**: Claude's `output_tokens` is flat (~6 = answer length, not reasoning), and **wall-seconds confound latency with effort**. The effort-vs-difficulty rank is the V4 job (exogenous difficulty + vendor-reported reasoning-tokens).
- Small battery (5 toy targets) -> a coarse solve/fail. A graded benchmark (V4, ~20-30 pre-registered exogenous-difficulty items) is needed before the agreement becomes a statistical *law* rather than a clean *demonstration*.
- Public-style items risk contamination; single run (no seeds/repeats yet).
