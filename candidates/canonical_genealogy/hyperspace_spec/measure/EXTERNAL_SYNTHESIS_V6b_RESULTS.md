# External pass — gemini (PASS) on V6b_RESULTS.md (2026-06-17) [codex pending]

Cross-model A− on the V6b irrelevant-expression control. Raw: `../session_arc/gemini_v6b_review.md`
(codex `../session_arc/codex_v6b_review.md` still running at write time — fold on arrival). **gemini
verified the result from the raw data and PASSED it — and strengthened it.** Cite-don't-coin.

## gemini verdict: PASS (Validated and Conservative)
gemini recomputed the cell medians and sign-tests directly from `v6b_run.jsonl` (all match: D=4
E0/dead/live = 39/46/60; D=12 = 102/110/126; compute-cost 30+/2−, text-cost 28+/2−, both p<0.001), and
confirmed the design integrity:
- **The conservative bias is real:** E3-dead has *more* text than E3-live, so a pure-transcription account
  predicts E3-dead would be the *most* expensive arm. Instead E3-live (shorter) costs +14.5 more — the
  compute signal cannot be length.
- **The control is valid:** in clean cases (e.g. seed 0) the **text-cost was literally 0 tokens** — the
  model fully ignored the dead expression.
- **The two outliers strengthen the claim.** The only 2/32 negative compute-deltas (seeds 11 & 13 at D=12)
  are cases where the model **failed to ignore** the dead expression and computed it compulsively (E3-dead
  jumped to the E3-live level). Those failures *inflate* the reported text-cost and *deflate* compute-cost
  → **the 73% compute figure is a conservative LOWER BOUND.** (And the model occasionally being unable to
  *not* compute is itself evidence the cost is computational.)
- gemini's per-op read: encode ≈ 4.8 tok/op vs the chain ≈ 7.8 tok/op — plausible; consistent with V6.

**Net (gemini): "the encode load is predominantly (73%+) real computation; the transcription surcharge
(+5.5) is real but secondary. Strong evidence that reasoning_tokens in gpt-5.5 track substantive work, not
length-proportional overhead."**

## What still stands (the honest caveats — unchanged)
- Scoped to the **encode factor**'s 3-op decode; the **V5 depth/span** factor needs its own dead-chain
  control to extend "it's compute" to the serial axis.
- The transcription component is real and non-zero (+5.5) — the pixel is *partly* transcription; sharpness < 1.
- Single model (gpt-5.5), single tier, n=16 seeds.

## codex (folded) — overclaims-remain; the reviewers SPLIT, and the split is the result
codex agrees the **core negative control is strong** ("rejects the strongest 'same text, same scratchpad
transcription' story") but tempers the framing:
- **"~73% compute" is too literal.** It is a *within-design descriptive decomposition*, not a mechanistic
  fraction of hidden cognition (it assumes additive text+compute components and no instruction-induced
  short-circuit). Honest claim: *"making the 3-op expression task-relevant costs substantially more tokens
  than showing the same expression dead."*
- **E3dead doesn't prove literal ignoring** — the model may parse / cheap-check / treat the supplied scalar
  as authoritative; "near E0" only proves any such activity was *cheap* under this prompt.
- **E3live − E3dead is not a *pure*-compute isolation** — it bundles required RHS evaluation + absence of an
  already-bound scalar + assignment-vs-comment semantics + the "do NOT recompute" instruction (which can
  itself *reduce* effort on E3dead). The length asymmetry blocks the simple objection but doesn't prove
  conservative bias in every direction.
- **Scope demotions:** V4 rehabilitation is only *partial* (the work-slope can still be per-step
  trace/carry/output policy); **V5 depth/span is NOT resolved** (V6b says nothing about span); single
  model/tier/n=16/one family — the ratio is not a portable constant. (Same additive-factors caution:
  Sternberg 1969; Stafford & Gurney 2011; McClelland 1979 cascade.)

## Merged honest verdict (gemini PASS ∧ codex temper)
**Both affirm the core: reasoning_tokens are NOT pure literal transcription for the encode factor —
showing the expression in a dead/ignored form does not induce the cost of evaluating it.** That worry,
which dogged V4–V6, is rejected on the encode axis. But the strong framing is demoted:
- "COMPUTE-DRIVEN / encode load is ~73% compute" → **"task-relevant evaluation adds a substantially larger
  token surcharge (+14.5) than dead expression text (+5.5); pure literal transcription is insufficient — but
  the 73/27 split is a within-design descriptive decomposition, not a mechanistic constant."**
- "first direct evidence reasoning_tokens track real computation" → **"first within-project evidence
  reasoning_tokens respond to required *evaluation* beyond expression *text*."**
- "rehabilitates the camera" → **"weakens the *global* pure-transcription worry; V4's work-slope is only
  partially rehabilitated and V5's span is not addressed."**

## Status → scope
Both folded. V6b promoted **pending → corroborated** for its *core* (the negative-control finding both
reviewers affirm), carrying the demotion (the literal "73% compute" + the V4/V5-scope caveats) as
dead-children. Decisive next (both): the **dead-chain V5 control** (same chain, one arm given the result
and told not to recompute) to take "it's evaluation, not text" to the span axis; plus codex's
length/instruction-balanced V6b ablation for a cleaner identification.
