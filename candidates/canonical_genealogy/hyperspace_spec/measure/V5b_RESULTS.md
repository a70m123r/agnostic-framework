# V5b — the dead-chain control: the SPAN surcharge is real serial COMPUTATION (scales with depth)

**Date:** 2026-06-17 | **Status:** real measurement. Extends V6b's compute-vs-transcription test from the
ENCODE stage to the SERIAL/SPAN stage (V5's DEEP>WIDE surcharge). 3 arms (base / dead / live) x D{4,12} x
16 seeds = 96 items, gpt-5.5 @ `high`, sha-locked (`v5b_labels.LOCK` b0c85bda). `v5b_deadchain.py`
(selftest: oracle 96/96, all 3 arms share the answer within (D,seed)). Cite-don't-coin.

> **External pass folded (gemini PASS + codex temper) — see [EXTERNAL_SYNTHESIS_V5b_V7.md](EXTERNAL_SYNTHESIS_V5b_V7.md).** CORE affirmed by both: executing the chain produces a **depth-dependent hidden-token surcharge** (+12→+63.5) that carrying the chain text does not → **reasoning_tokens scale with the required serial WORK, not with input text.** But **"transcription-proof" is DEMOTED** (codex): V5b controls *input* text, not the hidden *execution trace* — "one latent line per executed step" would show the same depth slope, so **hidden execution-trace transcription is not excluded** (and for an autoregressive model, computing and trace-writing may be the same act). Read "span is COMPUTE" below as **"span scales with required serial work; input-text transcription rejected, execution-trace not."**

## Headline — span is COMPUTE, and the compute cost scales with the critical path
| reasoning_tokens (median) | D=4 | D=12 |
|---|---|---|
| **base** (answer given, no chain text) | 16 | 18 |
| **dead** (chain shown as ALREADY-applied, told the result) | 32 | 30 |
| **live** (must execute the chain) | 43 | 92 |

- **chain-text-cost** = dead − base = **+16 (D=4), +13 (D=12)** — roughly **flat**: carrying the chain text
  costs the same whether the chain is short or long (the dead arm just reads off the given answer).
- **chain-compute-cost** = live − dead = **+12 (D=4) → +63.5 (D=12)** (p<0.001) — **scales hard with depth.**

**The depth-scaling is the transcription-proof signature.** Text length does not scale with chain *depth*
(dead is the same cost at D=4 and D=12); *executing the serial steps* does (+12 → +63.5, ~5–6 tok/step at
D=12). So **V5's serial surcharge is real serial computation, not transcription.** Robust: `live` is the
*shorter* prompt than `dead` (110 vs 120 words at D=12) yet costs +63.5 more — the compute signal cannot be
length.

## What it closes
Combined with V6b, reasoning_tokens are now shown to track **real computation on BOTH axes** of the single-
observer octave:
- **V6b (encode):** evaluating an expression costs ~2.6× more than carrying its text.
- **V5b (span):** executing a serial chain costs more than carrying its text, **and scales with depth** — the
  cleaner result, because depth-scaling is a property text cannot mimic.

→ The **pure-transcription worry** that demoted V4, V5, and V6 is now **rejected on both the encode and the
span axes.** The camera's pixel reads compute (with a smaller, real reading/transcription overhead).

## Honest limits
- The "compute vs text" split is a **descriptive within-design decomposition** (codex's V6b caution carries
  over: live−dead bundles execution + the "already-applied / report it" instruction + assignment semantics).
  But the **depth-scaling of compute-cost is robust to those** — none of them scale with D the way execution does.
- Single model (gpt-5.5), single tier (`high`), n=16 seeds, one generator family.
- The reading/text component is real and non-zero (+13–16) — sharpness < 1 holds; the pixel is partly text.

## Next
- A **cross-model** replication (does the depth-scaling slope hold on a different architecture?).
- Pending: codex + gemini external pass.
