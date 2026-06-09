# Cross-model review + falsification (2026-06-09) — the external A− catches a real bug

Per the standing cross-model rule, **GPT-5.5 + Gemini** were run, blind and independent, on this workflow's `more-than-PID` conclusion (see `RESULTS.md`). Both: **SOUND = partly.** The pass walked the headline back.

## The two external verdicts

- **Both agree the gate is genuinely NOT PID** — "fair that it is not PID" (GPT); it "isolates functional novelty that PID conflates with basic summation" (Gemini). So `more-than-PID` holds in the *narrow* sense (different objective from PID's joint-determination), and PID is *not* "wrong" — it answers a different question (don't strawman it: calling PID's joint-determination of a sum a "synergy misflag" is our framing, not PID's error).
- **Both flag the circularity** the synthesis already self-flagged: testing an affine-subtraction gate on affine inputs "validates the subtraction arithmetic, not the underlying concept of emergence" (Gemini); "partly circular" (GPT). The PID *contrast* still shows different objectives, but the additive-FAIL alone does not prove non-affinity is the *right* notion of emergence.
- **GPT's deepest hole:** the benchmark shows *definitional separation, not that residual codelength tracks meaningful emergence outside toy tensors.* Next test: blinded real/simulated systems with known nonlinear interactions vs out-of-sample causal/interventional predictability.
- **Gemini named a specific, falsifiable bug:** the gate "erroneously flags independent non-linear transformations as synergistic emergence even when no interaction between parents occurs," and proposed **M = A² + B²**.

## We ran Gemini's test immediately — the bug is CONFIRMED, and large

`separable_falsification_test.py`, affine-residual excess over floor @ b=16:

| case | excess (bits) | |
|---|---:|---|
| `ADD = 0.5A+0.5B` (affine, no interaction) | **0** | correctly floored |
| `SYN = 0.5A+0.5B+0.5·A·B` (genuine interaction) | 981,024 | flagged |
| `INT = A·B` (pure interaction) | 1,009,536 | flagged |
| **`SEP = A²+B²` (separable, NO interaction)** | **1,040,352** | **flagged — *higher* than the genuine interaction** |
| `SEP3 = A³+B³` (separable, NO interaction) | 866,944 | flagged |

So the affine-residual gate does **not** measure interaction-emergence — it measures **NON-AFFINITY**, which conflates a genuine joint `A·B` interaction with each parent transformed nonlinearly and then *added* (no interaction at all). Every internal case (pilot, recalib, the six here) had either affine or genuine `A·B` structure, so none exposed this; the external eyes did.

## Correction to the headline (walked back)

- The "**decisive differentiator = the affine quotient**" claim is **wrong as stated.** The affine quotient over-flags (separable nonlinearity false-positives), so it is the wrong operationalization of "additive blend = no emergence." **"Additive" must mean SEPARABLE** (`f(A)+g(B)` for arbitrary, possibly nonlinear f,g), **not merely AFFINE** (`aA+bB+c`).
- **The right measure is the interaction residual** `M − best-separable-additive-model` = the functional-ANOVA interaction term `h(A,B)`, which floors `A²+B²` by construction and keeps only genuine joint structure.
- **Honest tension this creates:** the corrected interaction-gate is conceptually *closer* to PID (both isolate joint-only structure), so fixing the bug may **narrow** the more-than-PID gap. The surviving clean differentiator is **frame-relativity** (the resolution knob PID structurally lacks), not the quotient.

## Revised bar status: **NOT discharged.**

The gate needs reformulation (**affine → separable / functional-ANOVA interaction**) and re-benchmarking before any `more-than-PID` claim stands; the real-corpus / real-model-merge leg remains owed. The cross-model pass did exactly its job — it caught a measure that would otherwise have hardened wrong. Tier-3; convergence list stays 9; nothing compiled.
