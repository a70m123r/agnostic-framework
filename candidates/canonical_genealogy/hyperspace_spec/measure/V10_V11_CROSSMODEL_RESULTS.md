# V10 + V11 — the cheap cross-model spectrum: a real (model-dependent) compute-free frame-cost; V11 invalid-as-designed

**Date:** 2026-06-19 | First run of the wrapper-spectrum rungs across CHEAP models via OpenRouter (the V3
"Latent Olympics" logic applied to V10/V11). 3 models × {V10 8 conds, V11 6 conds} × 14 seeds × 4 reps.
Params + slugs: see [CROSS_MODEL_RUNCARD.md](CROSS_MODEL_RUNCARD.md). Two subscription-only audits (codex +
a Claude file-reading subagent) verified the headline. Demote-not-kill.

## The instruments + the bug-fix that rescued the result
V10 (frame-strip): dissolve the task FRAME into a raw substrate; the **compute-free F0 falsifier** (every
chain's final given inline `=>`) tests whether dissolution costs reasoning *without* arithmetic on the path —
if yes, the cost is **orienting/frame-re-supply**, not compute. **codex's staging audit caught a real bug:**
the first run's F0 left ~11 filler arithmetic lines *un*-given (still computable), so F0 wasn't truly
compute-free. **Fixed** (all F0 arithmetic now `=>`; selftest guard; V10 re-locked `cb7ecfdd`) and re-run
clean. The fix **flipped deepseek's falsifier from −47 (null) to +149 (positive)** — the bug had been masking
the effect.

## V10 — clean cross-model result (correct-only, per-seed mean over reps, paired sign test, n=14)
| model | **F0 falsifier** (dissolved−deindexed, compute-free) | D_frame (F1_S−F2) | size (F1_M−F1_S) | F1_L acc |
|---|---|---|---|---|
| **gemini-2.5-flash-lite** | **+2303** (14/14, p<.001) | +736 (p=.057) | +4377 *** | 39/56 |
| **deepseek-v4-flash** | **+149** (11/14, p=.057, CI[+10,+204]) | +287 (p=.057) | +2578 ** | 56/56 |
| **qwen3-30b-thinking** | +376 (10/14, p=.18, CI[−18,+426]) | +504 (p=.42) | +3068 ** | 53/56 |

### What survives (both audits converge: CLAIM HOLDS, model-dependence demoted)
1. **A real compute-free residual frame-cost exists** — dissolving the frame costs reasoning *with compute
   removed*: **rock-solid on gemini (+2303, 14/14), borderline on deepseek (+149, CI excludes 0), null on
   qwen.** So it is **model-dependent, not universal.**
2. **It is NOT a reading-volume / parsing artifact** (the Claude audit refuted this hard): F0_DISSOLVED is
   *shorter* than F0_DEINDEXED yet costs *more* (wrong sign for "more to read"); the `=>`-line counts are
   identical across the two arms; and recomputing gemini on all-completed (incl. incorrect) calls leaves the
   falsifier at +1866, 14/14, p<.001 (not selection-on-correct). Gemini's per-call reasoning ≈ 2.8× under
   dissolution (1661→4580 median).
3. **A separate, universal, dominant reading-volume cost** — the size axis (F1_M−F1_S = +2578/+4377/+3068,
   all significant): more substrate → much more reasoning, on every model. The two axes **dissociate**
   (size = universal/large; orienting = smaller/model-dependent/compute-free).

### The residual confound (both audits flag the SAME one) — the next control
F0_DISSOLVED both **removes the top header** AND **moves the selector to the END** (trailing). So the +delta
could be **late-instruction rescan** (read body → learn the task → rescan) rather than pure **missing-frame
orienting**. **Decisive next control (V10b, both auditors independently): a compute-free 2×2 of {header
present/absent} × {instruction leading/trailing}**, exact-length, to separate frame-dissolution from
instruction-position. Until then: "a model-dependent compute-free residual frame/locating cost," not "orienting
mechanism proven."

## V11 — invalid-as-designed across ALL models (de-amortization not isolable)
| model | NOVEL−NAMED (headline) | NAMED_DEF−NAMED_BARE (def-reading) |
|---|---|---|
| deepseek | −70 (NS) | +174 (p=.057) |
| gemini | −234 (NS) | +1040 (p=.002) |
| qwen | −196 (NS) | +352 (p=.002) |

The headline `NOVEL_RULE − NAMED_DEF` is **negative on all three models** — the novel `digit-sum==S` predicate
is **intrinsically cheaper to apply than primality**, so predicate-DIFFICULTY swamps any de-amortization.
**Robustly invalid-as-designed** (not a one-model fluke). **Next control (V11b): a novel predicate
compute-matched to primality** (~√n trial-division-equivalent steps), selecting the same needle.

## The honest landing
- The cheap cross-model spectrum + the subscription audits turned a buggy null into a **real, audited,
  model-dependent compute-free frame-cost** (V10) and a **robustly-confounded null** (V11) — and named the
  exact next controls for both. The audit loop (codex's bug-catch → fix → reversal; both auditors' refutation
  of reading-volume + the shared rescan confound) is the instrument working.
- **Cost:** the whole 3-model spectrum (clean + buggy runs) ≈ $1–2 of OpenRouter; both audits = $0
  (subscriptions).
- **Provider-invariance angle (V3 echo):** the reading-volume cost is provider-invariant; the orienting cost
  is provider-DEPENDENT — itself a finding about where the camera's signal is robust vs idiosyncratic.

## Next
V10b (selector-position 2×2) + V11b (compute-matched novel predicate). External pass on this doc: codex +
Claude-subagent (subscription, done — both converged). agy/Deep-Think (Ultra sub) design critique of V10b/V11b:
pending Pav's interactive run.
