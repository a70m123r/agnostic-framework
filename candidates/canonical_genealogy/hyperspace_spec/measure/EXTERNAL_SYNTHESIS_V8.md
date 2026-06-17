# External pass — gemini (VALID) on V8 (2026-06-17) [codex pending]

Cross-model A− on the camouflage rung. Raw: `../session_arc/gemini_v8_review.md` (codex
`../session_arc/codex_v8_review.md` still running at write time — fold on arrival). **gemini verified the
null from the raw data and PASSED it — and confirmed I reported the null honestly (no salvage).** Cite-don't-coin.

## gemini: VALID
- **Integrity:** lock hash 4c0258ed matches; medians recomputed from `v8_run.jsonl` (LABEL 48, SUM 220,
  MAX_WIDE 206, MAX_TIGHT 202; primary delta −6.5); 100% accuracy confirmed via spot-checks of negative
  modular wraps (seed 14) → "the model is performing **precise evaluation**, not guessing." Prompt lengths
  tightly matched (210–212 words).
- **The null is ROBUST:** "for exact integer arithmetic, the hardness of disambiguating 999 from 998 is zero
  — the model's reasoning for a 1-unit gap is no more token-intensive than a 40-unit gap." No accuracy
  degradation in TIGHT further falsifies the hard-disambiguation hypothesis.
- **Endorses the framing:** "the adversarial burial effect is **binary (skip vs. evaluate), not graded by
  value-proximity**." Agrees the result is **specific to exact arithmetic** (the model's representation of
  computed values is not fuzzy).
- **One honest caveat gemini adds:** high seed-variance (SD of deltas ~45) at n=16 → the median is a stable
  null, but it's "no *detectable* graded tax," not "exactly zero."

## What this licenses (pending codex)
- **CORROBORATED:** value-proximity camouflage imposes **no detectable** compute tax on exact-arithmetic
  content — the model computes & compares exactly; **find-cost is binary (surface-skippable vs must-evaluate),
  set by the skip cue, not by value-similarity.** The pre-registered camouflage prediction (TIGHT > WIDE) is
  falsified for this form.
- **KEPT as caveat:** the null is likely **exact-arithmetic-specific** (fuzzy/approximate quantities untested);
  n=16 with SD~45 → no-detectable not zero; single model/tier.
- **The +170 forced-evaluation cost stays flagged as the already-known execution cost (V5b/V6b), re-seen** —
  interpretation, not a new camouflage finding.

## codex (folded) — overclaims-remain; converges with gemini, sharpens the demotions
codex verified the data (medians + 64/64 match; reconstructed prompts confirm MAX_WIDE gaps 40–129, MAX_TIGHT
gaps 1–3) and agrees **"the NULL is not hidden... basically honest."** Its tempers:
- **The +170 reframe must stay demoted.** Fair: "removing the skip cue exposes the already-known full-evaluation
  cost." NOT fair: calling that the V8 camouflage result — LABEL→MAX/SUM still changes skip-vs-evaluate AND
  named-selector-vs-rule-selector AND task semantics; SUM controls "selection isn't costly," not the camouflage.
- **The gap knob is the wrong operationalization for exact arithmetic** (gemini agreed): once six exact finals
  are computed, "999>998" is no harder than "988>925." So the clean inference is **"final-value proximity does
  not tax this model on this exact-integer max task,"** not "robust to camouflage."
- **No equivalence bound → "no DETECTED tax," not "zero."** n=16, single model/tier, no pre-declared
  smallest-effect-of-interest: nonsignificance ≠ proof of absence (Lakens 2017, equivalence testing).
- Cites the retrieval/distinctness lineage as *different mechanisms* from exact numeric comparison: Lost in the
  Middle; RULER; NoLiMa; Hidden in the Haystack (2505.18148).

## Merged verdict (gemini VALID ∧ codex temper)
- **KEEP (corroborated):** V8 **falsifies the pre-registered value-gap camouflage prediction** for gpt-5.5@high
  on this generator — making the needle's *value* near-identical to its runner-up imposes no detected compute
  tax (the model computes & compares exactly).
- **DEMOTED:** "robust to camouflage" → **"robust to final-VALUE proximity on exact arithmetic"**; "forced
  evaluation is the real camouflage tax" → **"removing a surface skip route exposes the already-established
  evaluation cost"** (interpretation, not the V8 result); "binary not graded" → **"this graded gap knob didn't
  matter; skip-vs-evaluate dominated here"**; "no compute tax" → **"no DETECTED value-gap tax; small effects
  remain possible without an equivalence bound."**

## Next (both)
- **Content-gravity / attention rung** (the gravity well; NIAH "attention mass lands on distractors" predicts a
  tax) and the **global-substrate / no-frame** rung — the mechanisms most likely to actually bite.
- codex's sharper exact-arithmetic camouflage: make camouflage operate **before/during candidate binding, not
  after final comparison** — near-miss *structural* predicates over traces (easy decoys fail early; hard decoys
  satisfy most selector predicates and fail late) + a SUM-style control + a **pre-declared equivalence bound**.

V8 promoted **pending → corroborated** for the falsification core, carrying the demotions as dead-children.
