# V10 frame-strip — adversarial audit of the CLEAN F0 falsifier

**Auditor:** independent re-derivation from raw JSONL (Claude). **Date:** 2026-06-19.
**Data:** `measure/v10fs_run.{deepseek,gemini,qwen}.jsonl` (448 records each, 0 exhausted, 0 null reasoning_tokens).
**Harness:** `measure/v10_framestrip.py`, lock sha256 `cb7ecfdd…` (the post-F0-fix lock).

---

## ONE-LINE VERDICT

**CLAIM HOLDS, with one honest demotion: the orienting-cost falsifier is REAL on gemini (decisive),
SUGGESTIVE on deepseek (borderline, CI excludes 0 but fragile at n=14), and NULL on qwen (the brief already
labels it NS — correct).** No artifact found; the two F0 arms are length-matched and the "grep the `=>` lines"
confound is structurally controlled. The headline framing — "orienting cost is real, on top of a larger
universal reading-volume cost" — is **honest**.

---

## 1. Is F0 genuinely compute-free now? — YES, and the data on disk is the FIXED run (not stale)

- Regenerated prompts (fixed harness): across 14 seeds, F0_DEINDEXED and F0_DISSOLVED each contain **235
  arithmetic lines (with `%`), 0 of which lack `=>`**. Truly compute-free.
- **Proof the JSONL is the clean re-run, not the buggy one:** `prompt_words` for every one of the 448
  records/model matches the fixed harness exactly (0 mismatches). The *buggy* F0 would have produced
  `prompt_words=763` for F0_DISSOLVED s0 (13 filler arith lines without `=>`); the fixed harness produces
  `789`; the data on disk holds **789**. The +26-word gap is a clean discriminator, so the data is
  unambiguously post-fix.

## 2. Re-derived clean falsifier (per-seed mean over reps, correct calls; median + exact two-sided sign test)

| model | falsifier median (DISSOLVED−DEINDEXED) | pos seeds | sign p | Wilcoxon p | boot 95% CI (median) | claim said |
|---|---|---|---|---|---|---|
| **deepseek** | **+149** | 11/14 | .057 | .049 | **[+10, +204]** (excl. 0) | +149 (p=.057) ✓ |
| **gemini** | **+2303** | **14/14** | **.0001** | .0001 | [+1400, +3265] | +2303 (p<.001) ✓ |
| **qwen** | **+376** | 10/14 | .18 (NS) | .049 | **[−18, +426]** (incl. 0) | +376 (NS) ✓ |

All three reproduce the headline numbers to within rounding. Size axis also reproduces exactly:
F1_M−F1_S = **+2578 / +4377 / +3068** (deepseek/gemini/qwen), all sign-significant; F1_L−F1_M positive and
significant for all three.

**Is the deepseek −47 → +149 flip real or noise at n=14?** *Borderline real, not decisive.* The clean
falsifier is **consistently positive**: 11/14 seeds positive, median +149, bootstrap 95% CI [+10,+204]
**excludes zero**, Wilcoxon p=.049. Two independent tests sit right at α=.05; the conservative sign test is
.057. One large negative outlier (−310) is what keeps it off significance. Verdict: the sign reversal from the
buggy −47 is **credible** (the buggy run mixed filler-compute into the delta, which is exactly the kind of
common-mode-broken contamination that could mask a real +effect), but deepseek alone would be reported as
*suggestive (p≈.05)*, not proven. Gemini is what carries the claim.

## 3. The key attack — residual confound between the two F0 arms — REFUTED

The two arms are byte-identical in substrate, selector, and the 6 task chains. The **only** difference:
F0_DEINDEXED has a top header (`"The text below is a system log."`) + the selector at the TOP; F0_DISSOLVED
has NO header and the selector TRAILING. Checks:

- **(a) Length difference?** NO — and it cuts *against* a reading-volume explanation. F0_DISSOLVED is
  **shorter**: median word diff −7, token diff **−8/−9/−8** (deepseek/gemini/qwen). The arm that costs MORE
  reasoning is the SHORTER one. A pure reading-volume confound predicts the opposite sign. ✓ refuted.
- **(b) "Model just greps the `=>` lines, so it's more lines in the dissolved layout"?** NO — the number of
  `=>` lines is **identical per seed across the two arms** (verified all 14 seeds), and total line count is
  *higher* in DEINDEXED (+2 header lines). Same greppable content, same substrate; only frame placement
  differs. ✓ refuted.
- **Absolute reasoning confirms it's orienting, not noise-floor:** in compute-free F0, models still burn real
  reasoning (deepseek median 555→584; gemini **1661→4580** ≈ 2.8×; qwen 1750→2074), min tokens 178–976 (well
  off zero), so the deltas are not quantization artifacts. With arithmetic removed, that reasoning is spent
  locating structure = orienting.

**Conclusion:** the +delta is attributable to FRAME PRESENCE/PLACEMENT, the intended manipulation. The single
remaining (small) uncontrolled variable is **position-of-instruction itself** — DEINDEXED states the task
before the body (model reads instruction → then scans), DISSOLVED states it after (model reads body "blind" →
then learns the task → must re-scan/re-orient). That serial-position effect *is* the orienting cost the rung
intends to measure, but a purist could call it "instruction-position" rather than "frame-dissolution." See
the recommended control below.

## 4. Gemini accuracy collapse & selection-on-correct bias — does NOT drive the result

Gemini accuracy: F3 100%, F1_S 93%, F1_M 88%, **F1_L 70% (39/56)**, F0_DEINDEXED 100%, F0_DISSOLVED 98%.
The collapse is on the **size axis (F1_L)**, NOT the falsifier — both F0 arms are ~100% accurate, so the
falsifier is computed on essentially the full sample (no selection). Test: recomputing gemini deltas on
**all completed calls** (correct + incorrect) instead of correct-only:

- Falsifier: +2303 → **+1866**, still **14/14 seeds positive, p<.001**.
- F1_L−F1_M: +1608 → +1275, still significant.
- D_frame (F1_S−F2): +736 → +721, unchanged (NS-ish either way, p≈.06–.18).

Selection-on-correct changes magnitudes by <25% and flips **nothing**. deepseek and qwen are ~100% accurate
on the relevant conditions, so no selection issue there at all.

---

## Is "orienting cost is real, ON TOP OF reading-volume" honest? — YES

- **Reading-volume (size) axis** is the dominant, universal, robust effect: F1_M−F1_S +2578/+4377/+3068, all
  three models significant; monotone through F1_L. Not in dispute.
- **Orienting (falsifier)** is a *separate, smaller, compute-free* effect that survives length-matching (and
  in fact runs against the length gradient, since DISSOLVED is shorter). It is decisive on gemini, suggestive
  on deepseek, null on qwen. So "on top of reading-volume" is fair: it's an additional axis, not a relabeling
  of size — the two are dissociated (size is universal; orienting is model-dependent).
- The earlier "orienting is free" (buggy deepseek −47) being a **bug artifact** is the right call: the buggy
  F0 leaked ~11–13 filler arithmetic lines of *real compute* into both arms, which both inflates baselines and
  can mask a modest orienting delta. The clean run reverses the deepseek sign and turns gemini strongly
  positive. Consistent with a real-but-small effect that was buried under compute noise.

**Honest caveat to keep attached:** the claim is **model-dependent**, not universal. Reported as a single
headline ("orienting cost is REAL") it slightly over-generalizes — it is real on gemini, marginal on deepseek,
absent on qwen. The honest framing is "real and large on gemini; weak/marginal elsewhere; the *size* cost is
the universal one."

---

## THE SINGLE MOST IMPORTANT REMAINING CONTROL

**Disentangle "frame dissolution" from "instruction position."** The two F0 arms differ in *both* (i) presence
of a top header and (ii) whether the task instruction precedes or follows the body. Add a third arm:
**F0_DEINDEXED_TRAILING** — same substrate, NO top header, but the selector still placed at the BOTTOM (i.e.
instruction-trailing like DISSOLVED, header-absent like DISSOLVED, differing from DISSOLVED only by… nothing —
so actually the needed arm is the cross-cell: **header-present + trailing-instruction**, or
**header-absent + leading-instruction**). Concretely, run a 2×2 of {header present/absent} × {instruction
leading/trailing} on the compute-free substrate. If the orienting delta tracks the *instruction-position*
factor and is flat across the *header* factor, the effect is a serial-position/re-scan cost (still real, but
should be named "read-then-learn-task re-orientation"), not "missing wrapper." If it tracks the *header*
factor, the "frame dissolution" label is earned. This single 2×2 is what converts the gemini result from
"real orienting cost" to a *mechanistically named* one — and it is cheap (compute-free, ~2 extra arms × 14
seeds × 4 reps).
