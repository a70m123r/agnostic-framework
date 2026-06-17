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

## The Latent Olympics
- GPT-5.5 dissolved: g1, g2, g3, d1_seq. Resisted by GPT-5.5: **s1_random** (the universal-residue candidate).
- **qwen3.5 cross-check (running):** does the local model fall for the bat-and-ball trap (cross-provider difficulty), and does the random stone resist it too (confirming the UNIVERSAL RESIDUE = resists every athlete = the near-objective hard content)? + rank agreement = the pinned relational bit on the reasoning axis. [folded when it lands]

## Honest limits
- Small battery (5 targets); `reasoning_tokens` is GPT-5.5's internal count (provider-specific magnitude — the Olympics compares RANKINGS across providers, not raw token counts = the pinned relational bit).
- The random floor is partly definitional (no ground truth exists), but that IS the aleatoric floor: a target with no derivable answer cannot be verify-dissolved by any amount of compute.
- Single run; the next step is a larger graded battery + per-budget ρ(effort) curves (not just first-correct) to trace the full resistance profile, and wiring the trace into the Ticker's dark gauges (knee / crack-spikes).
