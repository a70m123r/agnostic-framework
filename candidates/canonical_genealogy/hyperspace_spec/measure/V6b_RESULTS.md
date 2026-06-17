# V6b — the irrelevant-expression control (is reasoning_token cost compute or transcription?)

**Date:** 2026-06-17 | **Status:** real measurement. codex's decisive add-on to V6: separate the ENCODE
effect into text-cost vs compute-cost. 3x2 (E in {E0, E3dead, E3live} x D in {4,12}) x 16 seeds = 96
items, gpt-5.5 @ `high`, pre-registered + sha-locked (`v6b_labels.LOCK` 3cd4589e). `v6b_control.py`
(selftest-gated: oracle 96/96, all 3 E arms share the answer within (D,seed), expr text present in
E3dead+E3live, absent in E0) + `v6b_run.py` -> `v6b_run.jsonl`. Cite-don't-coin.

> **External pass folded (gemini PASS + codex temper, converged on the core) — see [EXTERNAL_SYNTHESIS_V6b_RESULTS.md](EXTERNAL_SYNTHESIS_V6b_RESULTS.md).** Both affirm the **core negative control**: showing the expression *dead* does not induce the cost of *evaluating* it → reasoning_tokens are **not pure literal transcription** for the encode factor (the worry that dogged V4–V6 is rejected on this axis). But the strong framing is **demoted**: read **"~73% compute"** as a *within-design descriptive split, NOT a mechanistic constant* (the E3live−E3dead contrast bundles evaluation + assignment-vs-comment semantics + the instruction); and it **only partially** rehabilitates V4's work-slope and says **nothing about V5's span** (which needs its own dead-chain control). Single model/tier/n=16. Read the sections below through that temper.

## Headline — the encode load is COMPUTE-driven (the camera reads real work, with a transcription overlay)
| reasoning_tokens (median) | D=4 | D=12 |
|---|---|---|
| **E0** (no expression) | 39 | 102 |
| **E3-dead** (expr text present, told to ignore) | 46 | 110 |
| **E3-live** (must compute the expr) | 60 | 126 |

Decomposition of the encode effect (paired per (D,seed), pooled over depth, n=32):
- **text-cost** = E3-dead − E0 = **+5.5 tok** (CI [+4.0,+9.0], p<0.001, 28+/2−) — *carrying* the expression text.
- **compute-cost** = E3-live − E3-dead = **+14.5 tok** (CI [+10.0,+18.0], p<0.001, 30+/2−) — *evaluating* it.
- total encode = E3-live − E0 = +20 tok (32+/0−).

**Verdict: COMPUTE-DRIVEN.** Evaluating the expression costs ~**2.6×** more reasoning-tokens than merely
carrying its text (+14.5 vs +5.5). The encode load is **~73% compute, ~27% transcription.**

## Why it's robust (and what it answers)
- **Robust to the length confound (conservative bias):** E3-live is the *shorter* prompt (median 59 words
  vs E3-dead's 74) yet costs *more* — so the +14.5 compute-cost cannot be a prompt-length artifact; if
  anything length works against it.
- **The control is valid:** E3-dead sits near E0 (+5.5), **not** near E3-live — so the model genuinely
  *ignored* the dead expression rather than compulsively computing it. The "do not recompute" instruction held.
- **This is the first direct evidence against the strong-transcription reading** that dogged V4–V6 (codex+
  gemini's worry that reasoning_tokens are "~6 tok/op of scratchpad transcription"). For the encode factor,
  the cost is **mostly real computation**, with a smaller, real transcription overlay. **reasoning_tokens are
  a MIX — compute-dominant + a transcription component — not pure transcription.**

## What it does NOT claim
- It rehabilitates the **encode** factor specifically. It does **not** directly resolve whether the **V5
  DEPTH/span** surcharge is compute vs transcription (a separate control: a "dead chain" would be needed).
  But it makes the compute-is-real reading more credible across the board.
- It does **not** revive V6's modularity claim — V6's encode×depth interaction stays borderline/demoted; V6b
  is about *what the encode cost IS*, not *whether encode and depth are separable stages*.
- The transcription component is real and non-zero (+5.5) — the camera's pixel is **partly** transcription;
  "sharpness < 1" holds. Single model (gpt-5.5), single tier, n=16 seeds.

## Where it lands the arc
- V4 (cost ~ work, demoted toward "maybe transcription") + V5 (serial surcharge, "maybe transcription") +
  V6 (additive-factors, demoted) → **V6b: the encode cost is demonstrably ~73% compute.** The deepest open
  worry of the single-observer arc — *is reasoning_tokens compute or transcription?* — gets its first direct
  answer: **mostly compute, with a transcription overlay.** A genuine (partial) rehabilitation of the camera.

## Next
1. **The dead-chain control for V5** — the analogous test on the DEPTH/span factor (a serial chain the model
   is told the running value of, vs one it must compute) — to extend the compute-vs-transcription split to span.
2. Escalate seeds + a second model (cross-architecture) for the compute/text ratio.
3. Pending: codex + gemini external pass on this result.
