# External pass — codex + gemini on V4_RESULTS.md (2026-06-17)

Cross-model A− on the RESULT (the design passed an earlier pass). Raw:
`../session_arc/codex_v4results_review.md` (gpt-5.5, xhigh), `../session_arc/gemini_v4results_review.md`.
**They converged**: the number is real and the pipeline is sound; the remaining issue is interpretive
scope. Demote-not-kill.

## Both independently re-verified the result (not just read it)
- **codex** recomputed from `v4_run.jsonl`: partial=+0.894071, raw(tok,E)=+0.879804, raw(tok,display_ops)=
  +0.177934, corr(E,display_ops)=0.000000, and the magnitude/digit robustness (+0.876992 / +0.882792 /
  +0.876524) — all match the reported numbers.
- **gemini** validated the factorial decoupling, the partial-Spearman estimator, the answer-magnitude
  control, and confirmed the **new lock binds the full stimulus + tier** ("patching the previous
  vulnerability where only the answer key was locked").
- Convergent verdict: **the headline is empirically supported; scope it strictly to mechanical arithmetic
  work/volume.** codex = "overclaims-remain" (wording only); gemini = "PASSED, with strict scoping."

## The one finding that sharpens the claim: the OUTPUT-transcription tautology (gemini)
V4 defeated the **input**-length tautology (prompt length ⊥ E by construction). It did **not** defeat the
**output**-length one: per-band tokens climb ~6 per added op (E2→E10 ≈ 40→88 ≈ 6 tok/op), consistent with
the model transcribing **one scratchpad line per z-step**. So reasoning_tokens here is plausibly
*mechanical transcription length*, not elastic cognitive allocation. codex's parallel: "E equals the
*nominal* z-chain update count under the intended interpreter; it does not prove the model internally
executed those ops" (the chain is affine-collapsible; reasoning_tokens are vendor telemetry, not a trace).
→ The doc's own demotion ("WORK," not "depth") is correct and **necessary**; state it harder.

## gemini Threat A — the distractor control is "weak" by design
The prompt hands the model the filter ("ignore w0,w1…; track only z"), so display_ops barely touches the
model's processing. Therefore raw(effort, display_ops)=+0.178 is **not** evidence the model "overcame
surface complexity" — it trivially followed the ignore-instruction. (This does not hurt the length-
tautology defense, but it means the T-control is a length control, not a distraction-load control.)

## Wording demotions to fold (codex's exact replacements)
- "E equals the exact arithmetic op-count the model executes" → **"E is the intended direct-execution
  z-chain operation count; internal execution strategy is not observed."**
- "not merely answer magnitude" → **"not eliminated by post-hoc controls for answer magnitude / digit
  count"** (a sensitivity check, not an independently-randomized confounder; answer value is downstream).
- "no right-truncation weakens the budget-gate alternative" → **"no evidence of a hard common
  right-censoring ceiling in this sample; soft / adaptive budget explanations remain open."** (Also the
  upper tail is not strictly monotone: max 87 / 192 / 185 at E=6 / 8 / 10.)
- Add to "What V4 CANNOT claim": **"Not a validation of reasoning tokens as cognitive effort or reasoning
  depth — only a vendor-token association with a controlled task knob, plausibly output-transcription
  length."** And: the original run used the weaker answer-key lock (`99ebbc…`); the full-stimulus+tier
  lock (`195eed4a…`) is post-hoc hardening (the run is separately integrity-verified 180/180).

## Stats notes (both, minor)
- Report the permutation p as Monte-Carlo resolution: **p = 0.0003 = (0/3000 exceedances, +1 smoothing)**;
  codex reproduced 0.000333 even permuting within display-op blocks (Freedman & Lane 1983).
- The bootstrap CI is conditional on **this generator family + item-bootstrap**, not a general
  arithmetic-task population. (Spearman 1904; Efron 1979.)

## Next move — V5 WIDE-vs-DEEP is the right decisive test (both)
Hold total arithmetic op-count (work) constant; vary serial **depth** (one long dependent chain) vs
**width** (several independent short chains + a final reduction). This is the classical **work-vs-span**
separation (Brent 1974, JACM, 10.1145/321812.321815). If tokens differ at fixed work → genuine depth
signal; if not → V4 was volume/transcription. Reuses the whole harness.

**Cheaper pre-tests before a full V5 grid (codex):**
1. A **V5-LITE slice** — a few matched long-chain vs many-short-chain items at fixed work/display/answer-
   magnitude. Decisive direction at ~20–40 calls.
2. A **tier sweep** (low/medium/high) on a V4 subset — directly probes the budget-gate story (does the
   slope survive a different token budget?) and, combined with the transcription reading, whether effort
   is elastic. ~30 calls.

## Net
V4 stands as a clean, pre-registered, externally-reproduced result — **scoped to: at fixed effort='high',
gpt-5.5's reasoning-token count scales with required arithmetic work, net of input length, robust to an
answer-size sensitivity check.** It is NOT yet evidence of reasoning depth or elastic effort; the leading
benign explanation is output transcription. V5 WIDE-vs-DEEP (+ the two cheap pre-tests) is the decisive
next experiment.
