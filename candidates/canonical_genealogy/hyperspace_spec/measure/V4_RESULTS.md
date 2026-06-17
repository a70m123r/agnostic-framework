# V4 — the Parametric Difficulty Ladder (real run, pre-registered, externally audited)

**Date:** 2026-06-17 | **Status:** real measurement. gpt-5.5 @ fixed `effort='high'`, n=180 locked
items (family CHAIN, 5 effective-op bands × 3 display-op levels × 12 seeds), `digestion_v4.py` ->
`v4_run.jsonl`. Design = the `agnostic-v4-design` workflow; design audited by codex+gemini
([EXTERNAL_SYNTHESIS_V4.md](../EXTERNAL_SYNTHESIS_V4.md)); the **built code** audited by the
`v4-code-audit` workflow (4 adversarial lenses). Cite-don't-coin, demote-not-kill.

## Headline
**partial-Spearman(reasoning_tokens, effective_ops | display_ops) = +0.894** — bootstrap 95% CI
[+0.864, +0.917], permutation p = 0.0003, n=180 solved (100%). raw(effort, **display_ops**) = **+0.178**.

Controlling for surface length barely moves the effect (raw(effort,E)=+0.880 → partial +0.894), because
**length is nearly uncorrelated with effort**. The factorial decoupling — `corr(effective_ops,
display_ops) = +0.000` by construction — held empirically: a positive partial **cannot** be the
autoregressive *input*-length tautology that both external reviewers flagged as threat #1.

> **External pass on the RESULT (codex xhigh + gemini, converged) — see [EXTERNAL_SYNTHESIS_V4_RESULTS.md](EXTERNAL_SYNTHESIS_V4_RESULTS.md).** Both independently RE-COMPUTED the number (+0.894071) and validated the decoupling, estimator, integrity, and the hardened lock. Verdict: real and sound, **scoped strictly to mechanical arithmetic work**. The one sharpening: V4 defeated the *input*-length tautology but **not the OUTPUT-transcription one** — tokens climb ~6 per op (40→88), consistent with the model transcribing one scratchpad line per z-step. So this is plausibly *transcription length*, NOT elastic cognitive effort. The demotions below are folded.

## Robustness — the partial survives the volume controls (free re-analysis, `v4_reanalyze.py`)
| control set | partial(effort, E \| …) | p |
|---|---|---|
| display_ops **[primary]** | **+0.894** | 0.0003 |
| display_ops, prompt_words | +0.894 | 0.0003 |
| display_ops, **answer_magnitude** | **+0.877** | 0.0003 |
| display_ops, answer_digits | +0.883 | 0.0003 |
| display_ops, ans_mag, ans_digits | +0.877 | 0.0003 |

raw(effort, answer_magnitude)=+0.382 — magnitude does correlate, but the E→effort partial **survives**
controlling it (+0.877). The signal is not merely "effort tracks the numeric size carried."

## Per-band reasoning_tokens (median) + truncation check
| effective_ops E | n | median tokens | max | #@max |
|---|---|---|---|---|
| 2 | 36 | 40 | 55 | 1 |
| 4 | 36 | 49 | 76 | 1 |
| 6 | 36 | 63 | 87 | 1 |
| 8 | 36 | 74 | 192 | 1 |
| 10 | 36 | 88 | 185 | 1 |

A clean monotone climb in the medians, and **no hard common right-censoring ceiling** (`#@max=1`
everywhere; the upper tail rises broadly but not strictly monotonically — max 87/192/185 at E=6/8/10).
So there's **no evidence of a flat budget cap** in this sample — though soft / adaptive budget
explanations remain open (a tier sweep is the direct probe, deferred to V5-lite).

## What V4 CAN claim
On n=180 solved items, **gpt-5.5's vendor reasoning_token count at fixed `effort='high'` tracks the
pre-registered effective-arithmetic-work knob E, net of surface display length and net of answer
magnitude, as a rank-association** (partial-Spearman +0.894, CI excludes 0, p=0.0003). The design's
load-bearing strengths are independently verified by the code-audit workflow: (1) the E ⊥ display-length
decoupling is **exact** (corr=+0.000, full 5×3 factorial at every T); (2) the oracle is correct (180/180
recompute-match + hand-traced grid-spanning items); (3) the answer key is genuinely hash-bound and the
run is **post-hoc integrity-verified** (180/180 records match the regenerated oracle); (4) the estimator
is a correct partial Spearman, matching the textbook precision-matrix to 1e-15, with a calibrated
permutation null (0.05) and a no-op handling of the collinear control.

## What V4 CANNOT claim (the honest ceiling)
- **Not "reasoning DEPTH," and not elastic "effort."** effective_ops E is the **nominal** z-chain
  op-count under the *intended* interpreter — internal execution strategy is **not observed** (the chain
  is affine-collapsible; reasoning_tokens are vendor telemetry, not a trace). A positive partial is
  equally consistent with "effort tracks mechanical arithmetic **work/volume**" and, per the external
  pass, with **output-transcription length** (~6 tokens per op ≈ one scratchpad line per step). This is
  **not a validation of reasoning tokens as cognitive effort.** **Separating depth from op-count is the
  V5 job (WIDE-vs-DEEP: hold op-count fixed, vary serial depth vs width — the classical work-vs-span
  separation, Brent 1974).** This is the one next experiment.
- **Not "net of two independent length controls."** `prompt_words = 7·display_ops + 40` exactly on this
  grid → there is **one** length axis (display_ops); prompt_words adds nothing (verified no-op).
- **No monotone "ladder" guarantee at the item level** — reasoning_tokens are quantized small ints with
  cross-item ties; the claim is a rank-association (band medians happen to be monotone here).
- **No difficulty ceiling / universal residue** — V4 is fully solvable (180/180); the aleatoric floor
  lives only in v2/v3 (the random stone). V4 validates the *effort axis*, it doesn't manufacture a floor.

## Demotions (folded from the external pass + the code audit)
- "effort tracks reasoning DEPTH" → **"effort tracks effective arithmetic WORK net of display length and
  answer magnitude, on execution-under-compositional-load, gpt-5.5 @ high."**
- "effort IS difficulty" (the original live claim, half-falsified at n=4 in v2) → **the demoted form
  above, now confirmed at ρ=+0.894 with a pre-registered, length-controlled, powered design.**
- "net of length (two controls)" → "net of a single length proxy (display_ops)."
- the smoke headline (+0.732) → **pipeline-corroboration only** (n=15 stride, not results-grade).
- "the run is bound to the pre-registration" → "the **answer key** (E,T,answer,seed) is hash-bound and
  the stimulus is **post-hoc integrity-verified** (180/180); the prompt text + effort tier were not
  bound by the original lock — hardened afterward (prompt+tier now in the lock) for V5."

## Disclosures
- **The answer VALUE leaks E** (raw Spearman(answer, E)=+0.365; mean answer 263→546 across bands).
  NOT exploitable as built — the model must *produce* the answer under exact-match grading (~0.1% guess
  rate), so it cannot enter the solved-only estimand — but disclosed as a known target property.
- Pure-additive (shortcut-prone) chains concentrate at LOW E (corr −0.425), so any summing shortcut makes
  *low*-E items cheaper → **biases the estimand toward zero** (conservative; cannot manufacture the result).

## Dead children
- "effort = vendor budget not need" — **weakened** (no right-truncation; effort grows with E within a
  fixed tier). Not killed (a single tier can't fully separate budget from need); demoted to a V5 check
  (sweep the tier).
- the public-benchmark V4 (GPQA/HLE) — killed earlier (saturation); the parametric pivot is vindicated.

## The one next experiment
**V5 — WIDE-vs-DEEP**: hold arithmetic op-count constant, vary serial DEPTH (one long chain) vs WIDTH
(several independent short chains). It is the only clean way to separate "effort tracks reasoning depth"
from "effort tracks arithmetic volume," and it reuses this entire harness. Free follow-ups already banked:
the partial survives answer-magnitude + digit controls.

## Provenance
design workflow `wf_f7a5eca8` (7 agents) → codex+gemini design audit → build (`v4_generator/stats/
digestion_v4/power_sim`) → free verification (oracle 180/180, decoupling 0.000, power) → smoke (15) →
full run (180) → `v4-code-audit` workflow `wf_2c2fb165` (5 agents, estimator verified to 1e-15) →
free re-analysis. Pending: codex+gemini external pass on THIS result.
