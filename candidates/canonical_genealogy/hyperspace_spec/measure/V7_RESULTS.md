# V7 — the burial gradient: burying the needle costs READING, not extra COMPUTE

**Date:** 2026-06-17 | **Status:** real measurement. Pav's question: *"the more you bury the real thing in,
the more compute?"* Holds the real computation FIXED (a depth-6 chain) and varies how much irrelevant
clutter surrounds it, separating two burial types. 5 conditions (k0; inert/ops at k in {6,12}) x 16 seeds =
80 items, gpt-5.5 @ `high`, sha-locked (`v7_labels.LOCK` 94cc4a72). `v7_burial.py` (selftest: core-chain
oracle 80/80; all conditions share the answer within seed). Clutter is explicitly labelled "distractor,
ignore". inert = dead-expression clutter (value given); ops = live-expression clutter (must evaluate if not
skipped); inert is the *longer* arm, so ops−inert is conservative on length. Cite-don't-coin.

> **External pass folded (gemini PASS + codex temper) — see [EXTERNAL_SYNTHESIS_V5b_V7.md](EXTERNAL_SYNTHESIS_V5b_V7.md).** CORE affirmed: **labelled distractors are filtered** — no detectable compute tax (ops ≈ inert). But two DEMOTIONS (codex): (1) the **volume dose-response is WEAK** — only the k0→k6 jump is solid; **inert12 − inert6 was median +4, p≈0.45**, so "climbs with how much you bury it" is *not* established between k=6 and k=12. (2) This is **easy-mode (labelled) burial** with "track ONLY s" — it licenses claims about *explicitly-labelled* clutter only; **camouflaged burial is untested.** Read "climbs with k" below as just the **k0→k6** step.

## Headline — burial DOES cost more reasoning tokens, but it's a READING tax, not a compute tax
| median reasoning_tokens | k=0 | k=6 | k=12 |
|---|---|---|---|
| **inert** (dead-expr clutter) | 48 | 62 | 66 |
| **ops** (live-expr clutter) | 48 | 58 | 61 |

- **reading-cost** = inert − k0 = **+12 (k=6) → +16.5 (k=12)**, p<0.001 — **climbs with how much you bury it.**
- **burial-of-compute** = ops − inert = **−5.5 (k=6), −2.0 (k=12, null)** — **no computational-burial tax.**
- gradient ops12 − ops6 = +7.5 (p=0.007) — the ops cost climbs with k, but that is the *reading* component.

**The answer (with the twist): YES, the more you bury the real thing, the more reasoning tokens it takes —
but because the model must *read/attend to* more clutter, NOT because it computes the clutter.** Live
clutter costs about the same as (slightly *less* than) dead clutter, so **the model successfully ignores
labelled distractors** rather than being forced to evaluate them. Burial taxes **attention proportional to
clutter volume**, not computation. (The ops−inert being *negative* is just inert being the longer prompt —
both are skipped, so cost tracks length.)

## The contrast that makes it interesting (with V5b + V6b)
The three controls now triangulate what reasoning_tokens *are*:
- **the model computes what it MUST** — V5b (executing the chain scales with depth), V6b (evaluating the encode).
- **the model READS what's THERE** — V7 (a reading tax that climbs with clutter volume, even for ignored junk).
- **the model FILTERS labelled junk well** — V7 (live clutter ≈ dead clutter → labelled distractors don't
  trigger compute), in contrast to V6b where a single *relevant-looking* expression was sometimes computed.

So reasoning_tokens ≈ **compute-on-the-required-path  +  a reading/attention overhead proportional to total
material.** Burial moves the second term, not the first.

## Honest limits
- The distractors were **explicitly labelled "ignore."** *Camouflaged* or *un-labelled* clutter (that looks
  relevant) might well trigger compute — a natural follow-up (and it would connect to the V6b "can't-help-
  computing" effect). This result is about *labelled* burial.
- ops−inert is confounded by the length difference (inert longer); the clean read is "no DETECTABLE
  computational-burial tax," not "exactly zero."
- Single model (gpt-5.5), single tier, n=16 seeds; depth-of-burial only to k=12.

## Next
- A **camouflaged-distractor** variant (unlabelled clutter that looks like the real chain) — does *that*
  trigger the compute tax?
- Pending: codex + gemini external pass.
