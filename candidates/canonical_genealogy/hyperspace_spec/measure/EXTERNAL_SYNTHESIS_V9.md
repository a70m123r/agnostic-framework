# External pass — gemini (VALIDATED + a critical catch) on V9 (2026-06-17) [codex pending]

Cross-model A− on the content-gravity/attention rung. Raw: `../session_arc/gemini_v9_review.md` (codex
`../session_arc/codex_v9_review.md` still running — fold on arrival). **gemini validated the core AND caught a
methodological error I missed: the +274 is a clipped budget ceiling, not the true tax.** Cite-don't-coin.

## gemini: VALIDATED with the saturation catch
- **Verified:** 100% accuracy (20/20) + 0% capture across all 60 trials; the +274 paired median reproduced.
- **THE CATCH (verified by me against `v9_run.jsonl`):** **15/20 INJECT trials hit exactly 512 reasoning
  tokens.** NEUTRAL maxes at 302, SALIENT at 345 — no clipping. So there is a **512 reasoning-token ceiling**
  that the false hint **saturates**. **The +274 is a CLIPPED LOWER BOUND** — the true cost of overriding the
  false hint exceeds the budget and is unmeasurable here. (The 512 cap did not bite any prior experiment —
  V4–V8 all ran well under it; it only bites V9 INJECT.)
- **Robustness is CONDITIONAL (gemini's key inference):** 100% accuracy holds only because the base task
  (165–302 tok) leaves room for math + override within 512. **On a harder base task, the override would push
  past 512 → the model exhausts its reasoning budget before resolving → a real CAPTURE error.** The gravity
  well *does* bite — at the resource-exhaustion break point. So "robust" is "robust *on this easy base task*."
- **The trapdoor is technically sound (1:34):** ~8 input words (~10 tokens) → ≥274 (clipped) hidden reasoning
  tokens. A cheap-to-inject / expensive-to-refute DoS that *saturates the seeker's compute ceiling*.
- **Instruction-proximity vs value-proximity (gemini's framing):** V8 = immune to value-proximity (exact
  arithmetic); V9 = **vulnerable to *instruction*-proximity** — it cannot surface-ignore a false hint, it must
  evaluate it and explicitly override it in latent space.
- **SALIENT is noise (+10):** formatting cues (UPPERCASE, brackets, end-position) do not trigger the override
  mechanism (one seed was even 34 tokens *faster* under salience).
- Verdict: "Promoting V9 to CORROBORATED (with saturation caveat)."

## What this licenses (pending codex)
- **CORROBORATED:** a **false instruction** imposes a large compute tax on an honest seeker *even while it
  stays accurate* — a cheap-to-hide / expensive-to-find trapdoor (the overthinking-attack DoS). SALIENT
  formatting does not (it's noise). The model is **robust to being *fooled*, taxable by an adversary.**
- **DEMOTED:** "+274 resistance tax" → **"the false hint drives the model to its 512-token reasoning CEILING
  (15/20 clipped); +274 is a clipped lower bound, the true override cost is unmeasured."** "Robust" →
  **"robust on this easy base task; capture is predicted at the break point where base + override > the cap."**
- **KEPT as caveat:** is +274 *false*-hint-resistance or *any*-hint-processing? Still open — the **true-hint
  control** is the decisive missing condition. Single model/tier/n=20; one lure design.

## codex (folded) — overclaims-remain; converges, adds three catches
codex confirms the saturation (14/20 INJECT at exactly 512 — "a plateau/quantization smell") and agrees the
TRUE-hint control is decisive. Its additional catches:
- **The lure is WEAK.** It's the *largest non-prime*; codex inspected the labels — **every lure had a small
  factor ≤7; 14/20 were even.** Trivially rejectable as non-prime. "0/20 capture" is "no capture *on a weak
  lure*"; a **prime-looking semiprime / near-miss** lure might capture. n=20 leaves a wide upper bound on the
  true capture rate.
- **"Resistance/override is not ISOLATED."** Current V9 shows "a contradictory named-hint costs more than
  neutral," not cleanly "*falsehood* resistance" — it cannot separate false-hint-override from generic
  hint-processing / contradiction-resolution / **sycophancy-resistance** (Sharma 2023, 2310.13548). The
  arithmetic check is cleaner than open-ended sycophancy tasks, but the control is still required.
- **The "prompt injection" label needs care** — Perez 2022 / Greshake 2023 are instruction *hijacking* and
  *indirect* PI (untrusted retrieved content blurring data/instruction). V9 is a **misleading in-prompt hint**,
  not indirect injection. The right nearby citation is **OverThink (2502.02542)** — slowdown attacks that
  inflate reasoning tokens while preserving correct answers — with **Sponge examples (2006.03463)** as the
  broader availability-attack precedent.
- The CI is over the **20 constructed seeds, not provider stochasticity** (no repeated calls); soften it.

## Merged verdict (gemini VALIDATED ∧ codex temper)
- **KEEP (corroborated, narrowly):** on this locked V9 generator, gpt-5.5@high answered **60/60 correctly with
  0 observed lure captures**, and the **false-hint condition produced a large paired increase in reasoning
  tokens that SATURATES the 512 ceiling** (15/20 → 512). A false hint costs the seeker its compute ceiling
  while accuracy holds.
- **DEMOTED:** "+274 = the resistance tax" → **"+274 is a CLIPPED LOWER BOUND (15/20 hit the 512 cap); the
  override cost is unmeasured, and 'resistance/override' is not isolated (need the TRUE-hint control)."**
  "robust to being fooled" → **"no observed capture under a short, easy, WEAK-lure arithmetic setting."**
  "cheap-to-inject/expensive-to-refute trapdoor PROVEN" → **"a candidate reasoning-AVAILABILITY asymmetry,
  consistent with OverThink-style slowdown, not yet isolated."** "prompt injection" → **"a misleading
  in-prompt hint."**

## Next — V9b graduates the finding (both)
Run **V9b**: paired NEUTRAL / TRUE_HINT / FALSE_HINT / FALSE_HINT_PRIME_LOOKING (keep SALIENT optional).
Report FALSE−TRUE, FALSE−NEUTRAL, TRUE−NEUTRAL, capture/error, and the attacker ratio per added input token.
Fix the lure (composite, no factor under 11–13, semiprime/near-prime). **Raise the reasoning cap above 512**
(un-clip the saturation), add repeated calls, n≥50, ≥2 tiers/models, store raw replies + usage. Only once
TRUE_HINT shows *savings* while FALSE_HINT shows *excess* does "verify-and-override tax" graduate. Then the
**global-substrate / no-frame** rung. V9 promoted **pending → corroborated** for the narrow KEEP, carrying all
the above as dead-children.
