# V9b — the resistance tax GRADUATES: a false hint is a measured, isolated, un-clipped override cost

**Date:** 2026-06-17 | **Status:** real measurement, 448 calls (gpt-5.5, 2 tiers x 4 conds x 14 seeds x 4
reps), 0 errors. The graduation experiment both external reviewers (gemini + codex) + the operator
converged on after V9. Locked `v9b_labels.LOCK` sha256 9fd8208e…. Raw: `v9b_run.jsonl` (full usage stored).

> **CORRECTION folded from the external pass (codex + gemini CONVERGED — see [EXTERNAL_SYNTHESIS_V9b.md](EXTERNAL_SYNTHESIS_V9b.md)).** Both reviewers independently re-derived from the raw log and flagged the **same #1 confound**: `FALSE − TRUE = +438` is **NOT a clean "pure override."** `TRUE_HINT` hands over the correct answer name, collapsing the search to 1 chain, so +438 conflates override cost with a search-space reduction. **The clean false-hint tax is `FALSE − NEUTRAL = +302` median (xhigh, p<0.001, 14/14).** Consequences folded below: (a) the attacker ratio is **~1:30**, not 1:42 (1:42 mixed a FALSE-vs-NEUTRAL input delta with a FALSE-vs-TRUE reasoning delta); (b) the capture "inversion" is **pure hypothesis** (4 vs 11 events, Fisher p=0.11; most xhigh captures used only ~512 tokens, so not carried by the long tail); (c) "high pins HARD at 512" → "plateaus at 512 (one 1024 exception)"; (d) the prime-looking capture demotion **survives** (call-level Fisher p=0.029) but is seed-clustered (7 vs 2 seeds) — enough to demote V9's "robust," not a stable population rate. Read the headline below through this correction.

## What V9 left open, and what V9b settles
V9 found: a false hint costs the seeker reasoning tokens (it resists, but pays). It carried three
demotions it could not resolve: (1) **+274 was a CLIPPED lower bound** (15/20 hit exactly 512); (2) the
cost was **not isolated** from generic hint-processing (no TRUE-hint control); (3) the lure was **weak**
(trivially-rejectable, single calls). V9b fixes all three — and the fix to (1) reshaped the design.

### The pilot discovery (un-clipping the 512)
The reviewers said "raise the cap above 512." Their *mechanism* was wrong, and that matters:
- **512 is NOT a `max_tokens` truncation.** `max_completion_tokens=8000` changed nothing (reasoning stayed
  512, `finish_reason=stop`). It is the **intrinsic reasoning budget of the `high` effort tier.** A hard
  arithmetic prompt converges at 290/410/473 tokens (medium/high/xhigh) — never hitting 512 — so when a
  false hint pinned exactly 512, the model was **budget-starved**, wanting more than `high` grants.
- **`xhigh` un-clips it** (`max` is unsupported for gpt-5.5). Same prompt: 512 -> 1002. So the true cost is
  reachable via the **effort tier**. V9b therefore runs **both** tiers: `high` (budget-limited) and
  `xhigh` (essentially un-clipped — reasoning ranged up to 6144; only 1/224 calls saturated).
- **Capture is real and STOCHASTIC** — the same prompt flipped between truth and the lure across calls, so
  V9b uses 4 repeats/cell.

### Design (paired by seed)
6 chains mod 1000, exactly one PRIME = the needle. Four conditions share the same chains, differing only
by a ~+8-word hint: **NEUTRAL** (none) · **TRUE_HINT** (names the needle) · **FALSE_HINT** (names the
easy lure = smallest min-prime-factor, even/obvious) · **FALSE_PRIME** (names a **prime-looking** lure,
min-prime-factor ≥ 11, a semiprime you must trial-divide to reject).

---

## Results

### By tier × condition (n=56 per cell)
| tier | condition | accuracy | capture (false lure) | saturated (pinned at budget) | median / **mean** rt (correct) |
|---|---|---|---|---|---|
| high | NEUTRAL | 56/56 | 0 | 0/56 | 229 / 236 |
| high | TRUE_HINT | 56/56 | 0 | 0/56 | 63 / 81 |
| high | FALSE_HINT | 56/56 | 0 | 39/56 | 512 / 501 |
| high | FALSE_PRIME | 52/56 | **4** | 50/56 | 512 / 507 |
| xhigh | NEUTRAL | 56/56 | 0 | 0/56 | 254 / 263 |
| xhigh | TRUE_HINT | 56/56 | 0 | 0/56 | 89 / 110 |
| xhigh | FALSE_HINT | 53/56 | **3** | 0/56 | 512 / **634** |
| xhigh | FALSE_PRIME | 48/56 | **8** | 1/56 | 512 / **884** |

`high` censors FALSE hard (39–50/56 pinned at 512); `xhigh` is essentially un-clipped (0–1/56). The
**mean** column is the un-clipped signal: the prime-looking override drives a heavy tail (xhigh mean 884).

### Paired reasoning-token deltas (per-seed mean over reps; bootstrap CI; exact sign p)
| tier | delta | value | CI | p | reading |
|---|---|---|---|---|---|
| **xhigh** | TRUE − NEUTRAL | **−136.1** | [−198,−128] | <0.001 | a true hint **SHORTCUTS** (14/14 seeds negative) |
| **xhigh** | FALSE − NEUTRAL | +302.1 | [+264,+486] | <0.001 | total false-hint cost |
| **xhigh** | **FALSE − TRUE** | **+438.2** | [+413,+684] | <0.001 | **PURE override cost** (14/14) — the delta V9 lacked |
| xhigh | FALSE_PRIME − FALSE_HINT | +140.6 | [0,+376] | 0.227 | prime-looking premium — directional, NOT established |
| high | TRUE − NEUTRAL | −151.6 | [−182,−137] | <0.001 | (censored) |
| high | FALSE − TRUE | +413.4 | [+381,+427] | <0.001 | (censored lower bound — FALSE pins at 512) |

### Capture (answer == the false hint's named lure)
- **FALSE_PRIME: 12/112 (≈11%)** captured vs **FALSE_HINT: 3/112 (≈3%)** vs **TRUE/NEUTRAL: 0** — and vs
  **V9's weak lure: 0/20.** All captures are the model literally returning the named lure's value.
- By tier: high 4/224 (1.8%) vs xhigh 11/224 (4.9%), **Fisher two-sided p=0.112** — not significant.

### Attacker ratio (xhigh, un-clipped)
~+10 input tokens (the hint) buy **+418 hidden reasoning tokens** of override (≈ **1:42**).

## Headline — three clean wins, one surprising inversion

1. **The false-hint override tax is now MEASURED against a clean baseline (the graduation).** A true hint
   *saves* ~136 tokens (shortcut, 14/14 seeds); a false hint *costs* — **`FALSE − NEUTRAL = +302` reasoning
   tokens**, un-clipped at xhigh, p<0.001, all 14 seeds. V9's clipped, confounded "+274" graduates to a
   measured number. **Caveat (external pass, codex+gemini converged):** `FALSE − TRUE = +438` is the
   helpful-vs-adversarial *pointer swing*, **NOT** a pure override — the true hint also shortcuts the search
   (collapses it to 1 chain), so it can't isolate *falsehood* from *search-space*. The clean isolation needs
   the negative-hint / VERIFY_ALL control (see Next).
2. **The trapdoor is confirmed above the clip.** ~+10 input tokens (the hint) buy ~+300 hidden reasoning
   tokens of override over a clean baseline — **≈1:30** (corrected from 1:42, which mixed a FALSE-vs-NEUTRAL
   input delta with a FALSE-vs-TRUE reasoning delta). Cheap to inject, expensive to refute — the
   OverThink-style **availability/slowdown** asymmetry, measured un-clipped.
3. **V9's "robust to being fooled" is DEMOTED.** A genuinely prime-looking lure captures **12/112
   (call-level Fisher p=0.029)** vs 3/112 easy vs **0** on V9's weak lure. "Robust" was an easy-lure
   artifact: make the decoy actually hard to reject and the gravity well **does** capture (~1 in 9 at xhigh)
   — though seed-clustered (7 vs 2 seeds), this demotes "robust" rather than fixing a stable population rate.

**The inversion (HYPOTHESIS ONLY — external pass rejected the strong reading):** the predicted
**budget-exhaustion break point did not appear.** Capture was *not* higher at the budget-limited `high`
tier; it was numerically **higher at the un-clipped `xhigh`** (4.9% vs 1.8%, consistent across both lures)
— **but not significant** (Fisher p=0.11, 4 vs 11 events), and **most xhigh captures used only ~512
reasoning tokens** (the long un-clipped tails are on *correct* calls), so "more budget rationalizes the
lure" is *not* supported by the within-tier token pattern. Left as a flagged hypothesis for the follow-up.

## Honest limits (anticipating the external pass)
- Single model (gpt-5.5), arithmetic-prime task; **min-pf ≥ 11** is one operationalization of
  "prime-looking" (a true semiprime adversary could push further).
- `high` deltas are **censored** (FALSE pins at 512) → lower bounds; the un-clipped story is the `xhigh` row.
- The **FALSE_PRIME cost premium** (+140 median, p=0.227; means differ +250) is **directional, not
  established** — the prime-looking lure's clean effect is on *capture*, not on the per-seed cost delta.
- The **capture inversion** rests on 4 vs 11 events (Fisher p=0.11) — suggestive, not significant.
- `saturated`/CEIL (512 / 6144) are run-measured heuristics, not provider-documented.
- Cite **OverThink (2502.02542)** (slowdown/availability) and **sycophancy (2310.13548)** (the
  hint-following baseline TRUE_HINT now controls). Still a *misleading in-prompt hint*, not indirect
  prompt-injection.

## Next — the clean isolation both reviewers converged on (remove the search-space confound)
- **V9c (most surgical, gemini): NEGATIVE hints.** "the answer is NOT named `<lure>`" (TRUE) vs "NOT named
  `<needle>`" (FALSE). Both still force searching the remaining chains, so the delta isolates **truth vs
  falsehood** with no shortcut to subtract — the clean "pure override" `FALSE − TRUE` graduates only here.
- **Alt (codex): VERIFY_ALL factorial** — require all 6 chain finals + the prime choice (TRUE can't
  shortcut); ≥100 seeds, ≥4 reps; capture via a logistic mixed model with seed random effects for
  tier × lure type.
- Then the **global-substrate / no-frame** rung (the last burial mechanism).

(External pass complete: [EXTERNAL_SYNTHESIS_V9b.md](EXTERNAL_SYNTHESIS_V9b.md). Pending: scope update,
memory, and — on Pav's word — commit.)
