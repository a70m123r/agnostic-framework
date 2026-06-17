# External pass — gemini (PASS both) on V5b + V7 (2026-06-17) [codex pending]

Cross-model A− on the two controls. Raw: `../session_arc/gemini_v5bv7_review.md` (codex
`../session_arc/codex_v5bv7_review.md` still running at write time — fold on arrival). **gemini verified
both from the raw data and PASSED both.** Cite-don't-coin.

## gemini: V5b VALIDATED, V7 VALIDATED
- **V5b (span is compute):** verified the harness against the raw jsonl; 96/96 correct. text-cost (dead−base)
  flat ~13–16; compute-cost (live−dead) **+12 (D=4) → +63.5 (D=12)** — "the smoking gun." Adversarial
  verdict: *"reasoning_tokens track serial computation is **validated** — the live arm (shorter prompt) costs
  significantly more than the dead arm at D=12 (92 vs 30), so the signal cannot be a transcription artifact."*
  Note: the "do NOT recompute" instruction might suppress some baseline thought, but the live-arm scaling is
  too large to be instruction-following alone.
- **V7 (burial = reading, not compute):** 80/80 correct. reading-cost +12→+16.5; ops−inert negative.
  Verdict: *"the model ignores labelled distractors is **validated** — if it were accidentally computing the
  ops clutter, that cost would overwhelm inert's slight length advantage."* Note: holds for **explicitly
  labelled** distractors; does not rule out a compute tax for **camouflaged/ambiguous** clutter.
- **Triangulation (gemini):** reasoning_tokens = **active execution on the required path (V5b) + per-token
  reading overhead (V7).** "Audit Passed."

## The nuance to watch from codex (flagged in the audit prompt)
For V5b, gemini ruled out the **input**-length-transcription reading (live shorter yet costs more). The
remaining subtlety is **output-execution transcription**: does the live arm scale with depth because it
*computes* 12 steps, or because it *writes one line per executed step*? For an autoregressive model these may
be **the same act** — the model computes *by* generating tokens, so "execute the chain" and "transcribe the
execution" are not separable on this substrate. The honest framing either way: **reasoning_tokens scale with
the REQUIRED SERIAL WORK (the critical path), not with input text** — which is the load-bearing claim and is
robust regardless. (Awaiting codex to sharpen this.)

## codex (folded) — overclaims-remain for both; the reviewers SPLIT on the execution-trace question
codex reproduced the raw patterns (D12 live−dead +63.5, D4 +12, positive slope all 16 seeds) and agrees the
**cores are sound**, but tempers:
- **V5b: "transcription-proof" is too strong.** V5b controls *input* text + visible output, **not hidden
  scratchpad/execution-trace length.** "If reasoning_tokens are one latent line per executed step, V5b would
  show exactly this depth slope." → *input-text transcription is rejected; hidden execution-trace
  transcription is NOT ruled out.* It cannot separate arithmetic computation from latent step-by-step trace
  production.
- **V7: the dose-response is WEAK.** "reading tax scales with clutter volume" is only partly supported —
  **inert12 − inert6 was median +4, sign-test p≈0.45.** Only the k0→k6 jump is solid; the k6→k12 climb is not.
  And "no compute tax" → "no *detectable* compute tax under explicitly labelled, length-confounded distractors"
  (inert is longer, could mask a small ops cost). It is **easy-mode (labelled) burial**, not camouflaged.
- (Cites the CoT-faithfulness lineage: Wei 2022 [2201.11903]; Turpin 2023 [2305.04388]; Lanham 2023 [2307.13702].)

## Merged honest verdict (gemini PASS ∧ codex temper) — the cores both affirm
- **V5b CORE (corroborated):** executing a serial chain produces a **depth-dependent hidden-token surcharge**
  (+12 @D4 → +63.5 @D12) that **carrying the chain text does not** — so reasoning_tokens **scale with the
  required serial WORK, not with input text.** *Demoted:* not "transcription-proof / compute-not-transcription"
  — the hidden execution-trace account (the model writing one latent line per step) is **not excluded** (and
  for an autoregressive model, computing and trace-writing may be the same act).
- **V7 CORE (corroborated):** **labelled** `w`-distractors are **filtered** (no detectable compute tax;
  ops ≈ inert). *Demoted:* the *volume dose-response* is weak (k6→k12 p≈0.45); the claim is scoped to
  **explicitly-labelled, length-confounded** clutter — **camouflaged burial is untested.**
- **The big claim demoted:** "V5b+V6b reject the pure-transcription worry on both axes" →
  **"V5b+V6b reject a pure prompt-copy / *input-text* account and show required *execution* affects
  reasoning_tokens on the encode and span axes; they do NOT fully reject the hidden scratchpad-transcription
  account."** The camera reads *the required work* — whether by computing or by transcribing its own execution
  is the residue.

## Next (both)
- **V5c output-trace control:** one arm computes states, the other only *follows/copies/verifies* provided
  states at matched latent-trace demand; + identity/no-op chains (same step-count, low-arithmetic) — to
  separate computation from trace-writing.
- **V7b:** exact token-length matching + **camouflaged** distractors (unlabelled, target-like variables, no
  global "track only s"); larger n, repeated calls, cross-model.

## Status → scope
Both folded. V5b and V7 promoted **pending → corroborated** for their cores, each carrying its demotion
(V5b: execution-trace not excluded; V7: weak dose-response + labelled-only) as dead-children.
