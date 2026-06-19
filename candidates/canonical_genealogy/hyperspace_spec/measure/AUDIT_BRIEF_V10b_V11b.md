# AUDIT BRIEF — V10b (compute-isolation) + V11b (compute-matched de-amortization)

**Date:** 2026-06-19 | **For:** external adversarial audit (codex CLI + Claude subagents).
**Your job:** REPRODUCE the numbers from the locked run files, then try to REFUTE each claim below.
Default to skepticism. Flag floor effects, confounds, underpowering, and over-claims. Demote-not-kill.

## The instrument
Cheap cross-model latent camera. Signal = `reasoning_tokens` (`usage.completion_tokens_details.reasoning_tokens`)
on CORRECT calls only. Models: deepseek/deepseek-v4-flash, qwen/qwen3-30b-a3b-thinking-2507,
google/gemini-2.5-flash-lite. effort=high, max_tokens=16000. Stats: per-seed mean over 4 reps, paired
bootstrap (4000) median CI + exact two-sided sign test over seeds (`paired()` in v9b_resistance.py).

## Files to reproduce from (all in measure/)
- V11b: `v11b_matched.py` (lock `v11b_labels.LOCK` sha d394534f), runs `v11b_run.{deepseek,qwen,gemini}.jsonl`
  (672 rec each = 28 seeds x 4 reps x 6 conds). Reproduce: `python v11b_matched.py --reanalyze --model M --seeds 28`.
- V10b: `v10b_irrelevant.py` (lock `v10b_labels.LOCK` sha 1c0071d0), runs `v10b_run.{...}.jsonl`
  (576 rec each = 24 x 4 x 6). Reproduce: `python v10b_irrelevant.py --reanalyze --model M --seeds 24`.
- V10 (prior, for the cross-experiment contrast): `v10_framestrip.py` (lock cb7ecfdd), `v10fs_run.{...}.jsonl`.
- Lineage: V11 was NEGATIVE everywhere (digit-sum predicate cheaper than primality — predicate-difficulty
  confound). V10 claimed (a) a compute-free residual frame-cost and (b) a universal reading-volume cost.

---

## V11b — de-amortization with compute matched (swap prime -> WURF, identical needle)
WURF(n): n>=2, not even (unless 2), and for each d in {3,5,7,11,13,17}, n%d != 1. `_make` forces the unique
prime needle to also be the unique WURF final (true isomorphism — prime-task and WURF-task select the SAME
integer). 6 conds: NAMED_BARE, NAMED_DEF, RENAMED_PRIME (prime->FLONK nonce, SAME concept), NOVEL_RULE (WURF),
F0_NAMED_DEF, F0_NOVEL_RULE (verdicts pre-given => zero predicate application). Defs word-matched (29 words).

**Numbers (median rt; deltas = per-seed-mean, CI, sign-p, n=28):**

| contrast | deepseek | qwen | gemini |
|---|---|---|---|
| NAMED_DEF − NAMED_BARE (read known def) | +124 p=.087 | +346 p=.013 | +760 p<.001 |
| **RENAMED_PRIME − NAMED_DEF** (nonce label, compute IDENTICAL) | **+162 p=.013** | **+263 p=.004** | **+241 p=.036** |
| **NOVEL_RULE − NAMED_DEF** (HEADLINE, novel concept, compute matched) | **+308 p<.001** | **+836 p<.001** | **+2151 p<.001** |
| F0_NOVEL − F0_NAMED (FALSIFIER, no application) | +78 p=.013 | −172 p=.345 | +101 p=.572 |

**CLAIMS:**
- **C1 (headline):** selecting by an un-amortized concept costs more reasoning than the same-difficulty
  amortized concept (prime). Positive + p<.001 on all 3. V11's negative was 100% the predicate-difficulty artifact.
- **C2 (cleanest leg):** RENAMED_PRIME is *literally primality* (identical computation) with only a NONCE label;
  it still costs +162/+263/+241 (all p<.05). => a pure label-de-amortization cost with compute held EXACTLY fixed.
- **C3 (falsifier):** with verdicts pre-given (no application), the novel−named gap VANISHES on 2/3 (qwen, gemini
  CI incl 0); deepseek keeps small +78 (~1/4 of headline). => the tax lives in concept-APPLICATION, not def-holding.

**ATTACK THESE:**
- C1: Is WURF truly compute-matched? It has 6 divisors vs primality's ~11 (up to sqrt 997). For the NEEDLE,
  prime trial-division is MORE steps than WURF — so the compute residual runs AGAINST the headline (prime should
  cost more if computed; it doesn't, because it's recalled). Does that make the headline conservative, or is there
  a path where WURF-application alone (not de-amortization) inflates it? Is "de-amortization of meaning" the right
  label, or is it just "novel predicate = more explicit compute"? (The F0 falsifier is meant to settle this.)
- C2: Is compute REALLY identical for RENAMED? Could the model distrust/re-derive the FLONK definition, or treat
  a nonce-named predicate as needing verification? Is +162/+263/+241 robust or noise? (n=28, sign test.)
- C3: Is "vanishes" over-claimed given deepseek's +78 survives (p=.013)? Is F0 underpowered? Recompute F0 on
  all-completed (incl incorrect) calls.

---

## V10b — irrelevant-task / lookup control (isolate compute from search/reading)
Same V10 substrate, but the task is "report the value variable {X} is initialized to" (zero arithmetic, zero
predicate). 6 frame conds F3_FRAMED..F1_L. Compare to V10's PRIME task at matched conditions.

**Within-V10b (lookup) — frame + size deltas are TINY:**
- F1_S − F2_DEINDEXED (clean frame removal, both full-length): deepseek +19 p=.023, qwen +143 p=.007, gemini +23 ns.
- Size axis F1_L − F1_S (lookup): deepseek +37, gemini −7, qwen −70 (all ~null/ns).

**Cross-experiment — median rt, PRIME (V10) vs LOOKUP (V10b), SAME substrate:**

| model | cond | V10 prime | V10b lookup | D_compute | ratio |
|---|---|---|---|---|---|
| deepseek | F1_S | 1680 | 84 | 1597 | 20x |
| deepseek | F1_M | 4342 | 103 | 4239 | 42x |
| deepseek | F1_L | 8102 | 121 | 7981 | 67x |
| gemini | F1_S | 6274 | 173 | 6102 | 36x |
| gemini | F1_L | 12798 | 166 | 12632 | 77x |
| qwen | F1_S | 4805 | 568 | 4236 | 8.5x |
| qwen | F1_L | 10469 | 498 | 9971 | 21x |

**CLAIMS:**
- **C4 (compute isolation):** pure locating costs near-floor reasoning, frame-insensitive (deepseek ~80-125,
  gemini ~155-177 flat). The reasoning the camera reads is dominated by predicate APPLICATION, not search/reading.
- **C5 (size-axis reinterpretation):** V10's "universal reading-volume cost" (size axis +2578/+4377/+3068 under
  prime) is NOT reading — it's COMPUTE/EVALUATION volume. Under lookup, 5x more substrate adds ~0 reasoning
  (deepseek +37, gemini −7, qwen −70). DEMOTE "reading-volume cost" -> "predicate-evaluation-volume cost."
- **C6 (frame-cost refinement):** V10's "compute-free residual frame-cost" (F0_DISSOLVED−F0_DEINDEXED = +2303
  gemini) used an F0 that STILL required primality-application (finals given, but "which is prime?" still applied).
  Under the truly application-free lookup, the residual frame cost is tiny (gemini ~0). => V10's F0 frame-cost was
  largely primality-application-under-dissolution, not pure orienting/search.

**ATTACK THESE:**
- C4/C5: FLOOR EFFECT. Is lookup so easy it bottoms out near a reasoning floor, so it CANNOT show scaling
  regardless? Then "lookup is flat" wouldn't prove "reading is free" — only "this task is below threshold."
  Is there a reading-volume cost that only manifests above some complexity the lookup never reaches? Check: does
  lookup accuracy stay ~perfect at F1_L (it does, 92-96/96)? Does lookup rt have ANY size trend at all?
- C6: V10-F0 and V10b-lookup remove "compute" DIFFERENTLY (F0 = pre-give chain finals, keep primality; lookup =
  remove primality too). Is it fair to attribute the gap to "primality-application"? Could the lookup task change
  the model's strategy wholesale (read-for-a-name vs evaluate-all) in a way that isn't a clean subtraction?

---

## What a clean audit returns
For each claim C1–C6: (verdict ∈ {reproduced / refuted / overstated / underpowered}), the recomputed number,
and the single sharpest residual flaw. Name the most important NEXT control. Be adversarial; this is demote-not-kill.
