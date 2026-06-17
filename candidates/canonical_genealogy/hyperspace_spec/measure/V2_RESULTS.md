# Digestion V2 — the reasoning-effort axis + the Latent Olympics (live run)

**Date:** 2026-06-17 | **Status:** real measurement. V1 measured ρ(PRIOR) — dissolve as context is handed over. **V2 measures ρ(EFFORT) — dissolve as the observer THINKS HARDER** (the conjugate axis; the slow-digestion / Kolmogorov side; the genuinely-novel conjugate-trace the external pass flagged). Multi-provider (Pav: "few providers in play") = the Latent Olympics. `digestion_v2.py` (+ `digestion_v2_ollama.py`) -> `v2_run.jsonl`.

## Athletes
- **GPT-5.5** (OpenAI API) — frontier reasoning; `reasoning_tokens` is the exact effort signal; reasoning_effort swept low/medium/high. Fast (~2-40 s/call).
- **qwen3.5:27b** (local, ollama) — different family, free/offline; ~minutes/call -> discriminating subset only (the cross-family check + the universal-residue confirmation).

## The verified-dissolve gate
A target dissolves only if the answer == ground truth (exact integer match). The random stone has NO ground truth -> any answer is a fabrication -> it can NEVER achieve a verified dissolve = the honest floor.

## GPT-5.5 result — ρ(effort) sweep

| target | a-priori diff | effort → first verified dissolve | reading |
|---|---|---|---|
| g1 add (13+29) | d1 | **6 reasoning-tokens** | melts on contact |
| g2 speed | d2 | **15** | easy |
| g3 bat-and-ball (the instinct trap) | d4 | **15** | a frontier model is NOT fooled — solves cheap |
| d1 sequence 2,6,12,20,30,? → 42 | d3 | **33** | needs real derivation — costliest of the solved |
| **s1 random sequence (no rule)** | d5 | **512 tokens, NEVER dissolves** | **the floor: reasoning cannot crack noise** |

### What it shows (measured, not argued)
1. **EFFORT TRACKS DIFFICULTY** — verified dissolve-effort rises 6 → 15 → 33 tokens across the structured targets. The settling experiment (DIGESTION_DYNAMICS V1) passes in the direction that matters.
2. **THE MODEL'S OWN EFFORT IS THE TRUER DIFFICULTY** — GPT-5.5 spent MORE on the sequence-derivation (33t) than on the bat-and-ball trap (15t), inverting my a-priori labels. The instinct trap only fools a weak mind; a strong one derives cheaply but must still pay to *derive a pattern*. So the effort readout is the difficulty, not the label — exactly the digestion-trace claim.
3. **THE ALEATORIC FLOOR, NOW ON THE REASONING AXIS** — GPT-5.5 spent the MOST reasoning (512 tokens) on the random sequence and NEVER achieves a verified dissolve; it can only fabricate a guess. V1 showed prior cannot dissolve noise; V2 shows EFFORT cannot either. Together they give the **3-way split** V1 alone could not see:
   - **epistemic-easy** (g1, g2): dissolves at low effort.
   - **epistemic-deep** (d1_seq, g3): dissolves, but costs real reasoning.
   - **aleatoric** (s1_random): never dissolves under prior OR effort — and *costs the most* trying. The true floor.

## The Latent Olympics (2 athletes)
- **GPT-5.5** dissolved g1, g2, g3, d1_seq; resisted by it: **s1_random**.
- **qwen3.5:27b-q4 (local)** on the subset {g3_batball, d1_seq, s1_random}: dissolved **NONE** — all three returned `tokens=900 (budget cap), answer=None`, i.e. its reasoning consumed the full 900-token budget **without terminating to a final answer**.

**Honest verdict (demote-not-kill on my own measurement):** the cross-provider **rank-agreement test is INCONCLUSIVE** — qwen3.5's "resistance" on g3/d1 is a **CONFOUND** (a weaker q4-quantized local model + a 900-token budget cap that truncated its chain-of-thought before it emitted an answer + answer-extraction that found no final integer), NOT evidence those targets are universally hard. The clean takeaways that DO survive:
1. **GPT-5.5 wins the Olympics decisively** — it dissolves every structured target cheaply; qwen3.5-as-configured cannot reach an answer within budget. A real, if lopsided, leaderboard.
2. **s1_random is the UNIVERSAL-RESIDUE candidate** — it resisted BOTH athletes (GPT-5.5 fabricated a guess at 512t; qwen3.5 never answered at 900t). Neither *verify-dissolved* it. (Caveat: qwen's resistance is budget-confounded, but a no-ground-truth random target floors any athlete by construction.)

**The fix for a clean rank-agreement test:** a properly-configured second athlete — a much larger reasoning budget for qwen (it did not terminate), OR read ollama's separate `thinking` field instead of `response`, OR a stronger second provider. As-is, qwen3.5-q4-local is too weak/truncated to *rank* difficulty; it can only confirm the floor.

## Honest limits
- Small battery (5 targets); `reasoning_tokens` is GPT-5.5's internal count (provider-specific magnitude — the Olympics compares RANKINGS across providers, not raw token counts = the pinned relational bit).
- The random floor is partly definitional (no ground truth exists), but that IS the aleatoric floor: a target with no derivable answer cannot be verify-dissolved by any amount of compute.
- Single run; the next step is a larger graded battery + per-budget ρ(effort) curves (not just first-correct) to trace the full resistance profile, and wiring the trace into the Ticker's dark gauges (knee / crack-spikes).
