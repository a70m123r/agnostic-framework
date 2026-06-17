# V8 — the camouflage rung (adversarial burial): value-proximity camouflage imposes NO compute tax

**Date:** 2026-06-17 | **Status:** real measurement. The first adversarial-burial rung (design via the
`v8-adversarial-burial-design` workflow; its audit caught the naive version as measuring execution, not
camouflage, and re-aimed the primary). 4 conditions (LABEL / SUM / MAX_WIDE / MAX_TIGHT) x 16 seeds = 64
items, gpt-5.5 @ `high`, sha-locked (`v8_labels.LOCK` 4c0258ed). m=6 chains, L=4, no "ignore" labels,
prompt-lengths matched (~211 words). Cite-don't-coin.

> **External pass folded (gemini VALID + codex temper, converged — see [EXTERNAL_SYNTHESIS_V8.md](EXTERNAL_SYNTHESIS_V8.md)).** Both verified the data and agree the **null is reported honestly.** Tightenings: (1) "robust to camouflage" → **"robust to final-VALUE proximity on EXACT arithmetic"** (once finals are computed, 999>998 is no harder than 988>925 — the gap knob was the wrong operationalization for exact-integer content). (2) The +170 stays demoted: **"removing a surface skip route exposes the already-known evaluation cost"** — *not* the V8 camouflage result. (3) No equivalence bound → **"no DETECTED value-gap tax," not "zero"** (Lakens 2017; n=16). What's **kept**: V8 falsifies the pre-registered value-gap camouflage prediction for gpt-5.5@high. Read the sections below through these.

## The pre-registered primary is NULL — value-proximity camouflage does not tax
| median reasoning_tokens | accuracy |
|---|---|
| **LABEL** (selector = "the variable named s" → skip, no evaluation) | 48 | 16/16 |
| **SUM** (selector = "sum of all finals" → evaluate all, no selection) | 220 | 16/16 |
| **MAX_WIDE** (selector = "the largest", runner-up ≥40 below) | 206 | 16/16 |
| **MAX_TIGHT** (selector = "the largest", runner-up ≤3 below = near-identical) | 202 | 16/16 |

- **PRIMARY — camouflage = MAX_TIGHT − MAX_WIDE = −6.5** (bootstrap CI [−17,+9], sign-test p=0.454, 6+/10−).
  **Null** (and slightly negative). With execution held fixed (both evaluate all 6 chains), making the needle
  near-identical to its runner-up costs the model **nothing**. It computes exact integer finals and compares
  exactly — value-proximity is free. 100% accuracy in every condition, including TIGHT.
- secondary **execution = SUM − LABEL = +170** (CI [+152,+190], p<0.001) — large.
- secondary **selection = MAX_WIDE − SUM = −11.5** (p=0.8) — null: picking the max is free once everything is
  evaluated.

## What it does and does not show (kept honest — no post-hoc salvage)
- **The camouflage hypothesis, in its value-proximity form, is FALSIFIED here.** The pre-registered prediction
  was TIGHT > WIDE (near-identical decoys force a careful, costlier disambiguation); it did not happen. The
  model is **robust to value-proximity camouflage** — consistent with V7's "filters cleanly" and with exact
  arithmetic (a 1-apart comparison is as cheap as a 40-apart one).
- **The +170 is NOT a new camouflage finding.** It is the *already-established execution cost* (V5b/V6b:
  evaluating chains is real, large compute), re-seen as the contrast between a **skippable** needle (LABEL,
  like V7's labelled burial) and an **unskippable** one (must evaluate all). *Interpretation (flagged as
  interpretation, not the pre-registered result):* the cost of adversarial burial is dominated by whether the
  needle can be **surface-skipped** — remove the skip cue and the model pays full evaluation — and is **binary
  (skip vs must-evaluate), not graded by how similar the noise is.* But that reframe leans on a secondary
  contrast; the clean, pre-registered finding is the NULL primary.

## Where it leaves the burial arc
- **V7 (labelled burial):** skip cue present → the model filters for free → reading tax only.
- **V8 (value-proximity camouflage):** skip cue removed via the *selector rule*, but the **disambiguation
  among near-identical computed values is free** → no graded camouflage tax.
- So *this* adversarial mechanism (hide the needle by making its value near the decoys') **does not work** on
  exact-arithmetic content. The find-cost is set by **forced evaluation**, which the burier triggers by
  removing the cheap surface route — not by value-similarity.

## Honest limits / why this might be form-specific
- **Exact integer arithmetic** is the likely reason the value-proximity null holds: once computed, comparison
  is exact, so "near-identical" is no harder than "far apart." With **fuzzy/approximate or high-precision-
  required** quantities, tight gaps might tax — a real follow-up.
- This tests **one** adversarial mechanism (value-proximity). The **content-gravity / attention** rung (make a
  *decoy more attractive* than the needle) and the **global-substrate / no-frame** rung (drop the needle into
  a generated field with no "these are the candidates" boundary) are the untested mechanisms most likely to
  bite — the workflow sketched both.
- Single model (gpt-5.5), single tier, n=16.

## Next
1. **Content-gravity / attention rung** — a *salient/attractive* decoy (longer, emphatic, positioned at the
   high-attention ends) or an injected steering line; does *attractiveness* (not value-proximity) pull the
   model off the needle and inflate find-cost + error?
2. **Global-substrate / no-frame rung** — the needle interleaved into generated near-arithmetic prose, no
   frame to "ignore the rest" — does removing the segmentation boundary force the predicted blow-up?
3. Pending: codex + gemini external pass.
