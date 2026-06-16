# Digestion-measurement V1 — the first live run (the aleatoric/epistemic split, observed)

**Date:** 2026-06-17 | **Status:** real measurement (not a proof-by-argument). The LLM-coder finally wired to emit a live stream; the first digestion-dynamics settling experiment (V1) RUN on real codelength.

## What was measured

Coder = the validated P1 echo-codelength (OpenAI `davinci-002`, echo+logprobs, exact arithmetic-coding bits). For each target W we hand the observer **increasingly relevant PRIOR** (the digestion) and measure the residue `cond(W | context_depth)` — contexts give *related* prior, never W verbatim (so we measure genuine dissolve, not the lookup/Goodhart confound the external pass flagged). Synthetic, non-sensitive targets; Pav-authorized external call (P1). Harness: `digestion_measure.py` -> `measurement_run.jsonl` -> `TICKER.html`.

## The result

| target | kind | ρ(prior-depth) bits | present→amortized | dissolved |
|---|---|---|---|---|
| common (Earth orbits Sun) | epistemic | 34.9 → 24.4 → 17.7 | 34.9 → 17.7 | **49%** |
| arithmetic (7×8=56) | epistemic | 28.0 → 25.8 → 10.3 | 28.0 → 10.3 | **63%** |
| specific (QX-440 @ 3.2 bar) | mixed | 88.1 → 71.7 → 26.0 | 88.1 → 26.0 | **70%** |
| **random** (incompressible noise) | aleatoric | 188.1 → 186.2 → 184.6 | 188.1 → 184.6 | **2%** |

## What it confirms (and it is a real confirmation, not an argument)

1. **THE ALEATORIC/EPISTEMIC SPLIT IS OBSERVED IN REAL CODELENGTH** — the §11.2 harden fix, empirically. The random string has the **highest** cold cost (188 bits) yet **refuses to dissolve** (2%): high-cost-but-structureless = noise, NOT a deep concept. The structured facts dissolve **49-70%** as the right prior is handed over. So "hardest = most resisting bits" was wrong (it would crown the noise); hardness is the *dissolvable-with-prior* part, and the floor is the part that never moves. The instrument now SEES the difference.
2. **THE TWO CLOCKS ARE REAL + MEASURABLE** — present (cold) vs amortized (deep-prior) is a genuine, exact gap (the `specific` valve: 88→26 bits, a 62-bit amortization credit the right prior pre-pays). The §12 cost-law, instrumented.
3. **THE CODER PATH IS VALIDATED FOR DIGESTION** — complements the canonicalizer finding (codelength is weak for semantic *equivalence* -> embeddings do that; but codelength is exactly right for the *residue-dissolves-with-prior* measurement). Two instruments, used for their right jobs.

## Honest limits (V1)

- Base-model coder (`davinci-002`) — noisier than a frontier model; the *directions* are robust (the split + the two-clock), the absolute bits are coder-relative (the pinned relational bit).
- This measures the **instant-crush / prior-conditioning** axis. The **slow-digestion / reasoning-effort** axis (attempts/tokens/strategy via a reasoning model — `qwen3.5:27b` is local) is V2, and would feed the Ticker's still-dark gauges (EDL per-tick, knee, crack-spikes).
- 4 targets, single run — a demonstrator, not a benchmark. The next step is a graded-difficulty battery (the V1 settling experiment proper: does verified dissolve-effort rise monotonically with ground-truth difficulty?).

## What it feeds

`TICKER.html` — the deferred channel, now built honestly: every needle (ρ tape, twin clocks, dissolved-fraction, the aleatoric-floor flag) is a measured value; the gauges with no stream yet (EDL per-tick / Goodhart gap / knee) stay **dark** (no observable, no needle — the channel rule).
