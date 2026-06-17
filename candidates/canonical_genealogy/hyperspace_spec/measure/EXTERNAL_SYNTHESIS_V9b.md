# External pass — codex + gemini on V9b (2026-06-17): STRONG CONVERGENCE, one shared confound

Cross-model A- on the graduation experiment. Both reviewers independently re-derived from the raw 448-record
`v9b_run.jsonl` and reached the **same verdict and the same #1 confound**. Raw:
`../session_arc/codex_v9b_review.md`, `../session_arc/gemini_v9b_review.md`. Cite-don't-coin.

## Both verdicts: overclaims-remain (the measurement is real; two numbers were over-isolated)

### The shared #1 catch (codex AND gemini, independently): FALSE - TRUE is NOT "pure override"
`TRUE_HINT` does not merely *add a hint* — it hands over the **correct answer name**, collapsing the search
from ~3.5 chains evaluated (NEUTRAL) to 1. So `FALSE_HINT - TRUE_HINT = +438` **conflates** the false-hint
override cost with the **search-space reduction** the true hint grants (~2.5 chains, ~150 tok). The valid
override signal against a clean baseline is **`FALSE_HINT - NEUTRAL = +302` median (xhigh, p<0.001, 14/14
seeds).** This is the cleaner, surviving number.

### Both: the attacker ratio used the confounded delta
`1:42` paired `+10` input tokens (a FALSE-vs-NEUTRAL contrast) with `+418` reasoning (a FALSE-vs-TRUE
contrast). The consistent ratio is **`+302 / +10` ≈ 1:30** (median; ~1:36 on means). Still a large
attacker-favorable asymmetry — just reported against the right baseline.

### Both: the capture "inversion" is speculation
Capture higher at xhigh than high (4.9% vs 1.8%) rests on **4 vs 11 events, Fisher p=0.11** — not
significant. codex adds the mechanistic refutation: **most xhigh captures used only ~512 reasoning tokens**
(the long un-clipped tails are on *correct* calls, not captured ones), so "more budget -> rationalize the
lure" is not even supported by the within-tier token pattern. -> pure hypothesis.

### codex's extra catches
- **Capture power under clustering:** call-level FALSE_PRIME vs FALSE_HINT `12/112 vs 3/112` is nominally
  significant (Fisher **p=0.029**), but seed-clustered it is **7 seeds vs 2 seeds** with any capture —
  enough to demote V9's "robust," not enough for a stable population rate.
- **"high pins HARD at 512" is too strong:** one high/FALSE_HINT record hit 1024. Treat tier ceilings as
  *observed plateaus*, not provider-certified caps.

## What SURVIVES (KEEP — corroborated, narrowly)
- On the locked V9b generator, **a false named hint reliably imposes a large reasoning-token override tax
  over a clean baseline: `FALSE - NEUTRAL = +302` median (xhigh, un-clipped, p<0.001, all 14 seeds);** a
  **true** hint instead **shortcuts** (`TRUE - NEUTRAL = -136`, 14/14). The camera reads truth as cheap
  (replay) and a lie as expensive (decompression).
- The **attacker trapdoor survives** at **~1:30**: ~10 input tokens buy ~300 hidden reasoning tokens of
  override — the OverThink-style (2502.02542) availability/slowdown asymmetry, measured un-clipped.
- **V9's "robust to being fooled" is DEMOTED:** a genuinely prime-looking lure **captures** (call-level
  `12/112`, p=0.029) where V9's weak lure got `0/20`. "Robust" was an easy-lure artifact.
- **The pilot's mechanism correction stands:** 512 is the `high` tier's reasoning *budget* (un-clipped by
  `xhigh`), not a `max_tokens` truncation — and the V9 512-clip did NOT recur at xhigh.

## DEMOTE (demote-not-kill)
- "verify-and-override IDENTIFIED / pure override = +438" -> **"a false hint imposes a measured ~+302-token
  override tax vs NEUTRAL; `FALSE - TRUE` (+438) is NOT a clean isolation — the true hint also shortcuts the
  search, so +438 = the helpful-vs-adversarial pointer SWING, not the pure override."**
- "attacker ratio 1:42" -> **"~1:30 (FALSE-vs-NEUTRAL)."**
- "prime-looking lure captures ~11%" -> **"strict-lure capture observed at 12/112 (p=0.029 call-level);
  demotes V9's 'robust' but is seed-clustered (7 vs 2) — not a stable population rate."**
- "more budget rationalizes the lure / break point inverted" -> **"the predicted budget-exhaustion break
  point was NOT observed; the higher xhigh capture is not significant (p=0.11) and not carried by the
  long-reasoning tail -> pure hypothesis."**
- "high pins HARD at 512" -> **"high plateaus at 512 (one 1024 exception); ceilings are observed plateaus."**

## The decisive NEXT experiment (both converge on removing the search-space confound)
- **gemini (most surgical): NEGATIVE hints that don't reduce search space** — "the answer is NOT named
  `<lure>`" (TRUE) vs "NOT named `<needle>`" (FALSE). Both still force searching the remaining chains, so the
  delta isolates **truth vs falsehood** cleanly, with no shortcut to subtract.
- **codex: VERIFY_ALL factorial** — require output of all 6 chain finals + the prime choice, so TRUE_HINT
  cannot shortcut; NEUTRAL/TRUE/FALSE/FALSE_PRIME x {high,xhigh}, >=100 seeds, >=4 reps; capture via a
  logistic mixed model with seed random effects for tier, lure type, and tier x lure.

## Merged verdict
V9b **graduates the resistance tax to a measured, baseline-anchored override tax (+302, p<0.001)** and
**demotes V9's "robust" via a real prime-looking capture (p=0.029)** — while **rejecting** the over-isolated
+438 "pure override," the 1:42 ratio, and the "rationalization" inversion. Promote V9b **pending ->
corroborated** for the narrow KEEP, carrying the four demotions above as dead-children. The negative-hint /
VERIFY_ALL control is the clean isolation that would let "pure override" graduate.
