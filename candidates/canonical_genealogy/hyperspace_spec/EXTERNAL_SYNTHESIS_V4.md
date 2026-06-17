# External pass — codex + gemini on V4_DESIGN.md (2026-06-17)

Two non-Claude reviewers on the workflow's locked V4 spec (`V4_DESIGN.md`). Raw:
`session_arc/codex_v4_review.md` (gpt-5.5, xhigh), `session_arc/gemini_v4_review.md`.
They **split on the verdict but converged on the substance** — and the split is informative:
gemini says *build it, the partial-Spearman|length result is the honest payload*; codex says
*revise first, as written it would mostly measure display-length + vendor budget*. Demote-not-kill.

## Where they CONVERGE (4 shared threats — these are now load-bearing)
1. **The autoregressive / display-length tautology (both, top flaw).** For the chain-step families
   (MODARITH-CHAIN F1, NEST-PARENS F4) the difficulty knob *is* visible operation-count = prompt
   length. `prompt_token_count` is then near-**collinear** with the knob, so the partial-Spearman is
   "underidentified or just noise" (codex) and "may go negative or become uninterpretable" (gemini).
   The length control as specified is **not sufficient**.
2. **Censoring manufactures monotonicity (both).** Pinning failed items at the effort ceiling *forces*
   a positive rho — "a model incompetent at Band 5 appears to have infinite effort" (gemini). Report
   **solved-only rho alongside** any censored version; if solved-only is flat, "effort=difficulty" is
   false and only the "failure=hard" tautology survives.
3. **Effort may be a vendor budget, not need (both).** `reasoning_effort='high'` can gate "allowed to
   think this much," not "needed this much." Cites the corrected **Illusion-of-Thinking (arXiv
   [2506.06941](https://arxiv.org/abs/2506.06941))** — effort rises with complexity then *falls* despite budget.
4. **The seal is self-attestation, not a commitment (both).** `sha256(answer||nonce)` fixes brute-force,
   but a local hash chain "can be regenerated after seeing outcomes unless a chain head is externally
   witnessed before reveal." Residual trust = the operator didn't backdate/regenerate.

## What codex adds (the two that block "locked")
5. **Estimand conflict — the design is NOT actually locked (fatal for pre-reg).** It names three
   different primary effort statistics (`reasoning_tokens@high`, then `min-over-{low,med,high}
   effort-to-first-correct`, then demotes that same min-metric). A pre-registration must have **one**
   primary estimand. (The workflow itself flagged the min-over-grid metric as downward-biased — codex
   makes it fatal: pick one and only one.)
6. **Power is not credible.** n=15/family with 5 tied ordinal bands and 3 seeds is too thin for a
   bootstrap CI to mean anything; a 4000-permutation p-value "is computationally neat but does not
   create information." Cites **Yu & Hutson (arXiv [2008.01200](https://arxiv.org/abs/2008.01200))** on small-sample
   Spearman fragility.

## The three revisions that turn it into a real pre-registration
1. **ONE primary estimand.** `partial Spearman(reasoning_tokens @ FIXED 'high', effective_ops |
   display_ops, prompt_tokens)` on **solved, non-instrument-limited** calls only. min-over-effort,
   solve-rate, censored variants, low/med/high curves → all explicitly **secondary** tables.
2. **A FACTORIAL generator that decouples `display_ops` from `effective_ops`** (the fix both demand).
   Same number of visible tokens/operators, different dependency depth; and same depth, different
   filler/surface length. No-op / independent-operation controls for F1/F4; hold candidate-list length
   constant while varying constraint dependency for F3. Only then can the length confound be *tested*
   rather than assumed away. Without this, the headline measures length.
3. **Power up before any model call.** Simulation-based power analysis; minimum **4 families × 5 bands
   × 10 seeds = 200 primary calls** at fixed 'high' (15–20 seeds if expected rho < 0.5); repeat ≥20%
   of cells to estimate run-to-run token variance + report ICC. **Never convert failures into fake high
   effort** — failure is a separate binary outcome; analyze token effort *conditional on success*
   (censored-rank / survival if censoring is central).

## Plus
- **Seal:** publish the prereg hash + each chain head to an **external witness before reveal**
  (OSF / a pushed GitHub commit / OpenTimestamps / RFC3161 TSA / Sigstore-Rekor). Until then call it a
  "locally tamper-evident log," not a seal.
- **Confidence (PREDICT-half):** run a **blinded calibration pilot first** to measure raw-logprob
  dynamic range + rank discrimination; score every candidate token (not just top-k); train/cal/test
  splits. With ~40 trials **do not make strong ECE claims** — ECE is binning-sensitive (Nixon et al.,
  arXiv [1904.01685](https://arxiv.org/abs/1904.01685)); use Brier + Murphy reliability-resolution-uncertainty
  decomposition as *descriptive*. RLHF/LM logprobs are often poorly calibrated for QA (Jiang et al.,
  [2012.00955](https://arxiv.org/abs/2012.00955); Tian et al., [2305.14975](https://arxiv.org/abs/2305.14975)).
- **Drop the GSM8K/MATH/AIME anchor gate from the primary** (reintroduces contamination + human-hard ≠
  model-hard); demote to a descriptive sanity check. Say **"exact-item contamination-minimized,"** not
  "contamination-free."

## Merged demotions (fold into the build)
- "the parametric knob is exogenous difficulty" → "a preregistered synthetic operation-count/display
  variable; whether it isolates *model* difficulty is *tested* by length- and display-matched controls."
- "partial Spearman controls the length confound" → "a sensitivity check; causal separation requires the
  factorial matched generator."
- "reasoning_tokens measure effort needed" → "vendor-reported hidden-token consumption under a fixed
  inference policy."
- "sealed forecaster" → "locally tamper-evident information-blindness holdout unless chain heads are
  externally witnessed before reveal."
- "logprob confidence is a rigorous probability" → "raw conditional token scores from RLHF/non-reasoning
  models, usable only if a held-out calibration test shows non-collapsed resolution."
- "contamination-free by construction" → "fresh exact instances from familiar synthetic families;
  exact-item leakage minimized, task-distribution familiarity remains."

## Net
The pivot to a parametric generator was right — it killed the contamination + saturation that sank the
public-benchmark design. But the external pass shows the *generator must do more work*: decouple display
from effective difficulty, pin one estimand, and power up — or the honest headline is "effort tracks
prompt length." That is a buildable revision, not a redesign. **The single decisive observable is
unchanged and now sharper: partial-Spearman(effort, effective_ops | display_ops) on solved items.**
