# V9c — the PURE override, isolated: decomposing V9b's +438 into a search shortcut + a true override

**Date:** 2026-06-17 | **Status:** real measurement; headline DEMOTED by the external pass. The
shortcut-deletion **survives**; the "+1246 = pure override" label **does not**. Locked `v9c_labels.LOCK`
sha256 742b9cb2…. gpt-5.5 @ `xhigh` (the un-clipped tier), synthetic data.

> **CORRECTION folded from the external pass (codex "overclaims-remain" + gemini "UNSOUND" — see
> [EXTERNAL_SYNTHESIS_V9c.md](EXTERNAL_SYNTHESIS_V9c.md)).** Both re-derived the numbers exactly and confirm
> the **shortcut-deletion is sound** (TRUE_NEG−NEUTRAL=+2.4 NS proves the negative form has no shortcut → V9b's
> +438 = −145 shortcut + a true override). **BUT "+1246 = pure override" does NOT survive.** gemini's catch I
> missed: FALSE_NEG eliminates the *only* prime → a **0-solution paradox**, so +1246 is inflated by
> paradox-panic (the model loops assuming a solution must exist), not a clean override. codex adds the
> salience asymmetry: FALSE_NEG names the **answer**, TRUE_NEG names a cheap-to-discard **lure**, so +1246
> conflates **falsehood + answer-salience + paradox**. The "unpaid-tax capture" is n=1 (40 correct calls also
> used 512 tok). Trapdoor ~107:1 survives. **V9c is bucketed `pending`**; the decisive isolation is **V9d
> (2-prime release valve + same-named-chain), below.** Read the headline through this correction.

## What V9b left open
V9b measured `FALSE_HINT − TRUE_HINT = +438` and over-labelled it "pure override." Both reviewers caught
the same confound: a **positive** true hint ("the answer IS named `<needle>`") lets the model verify *one*
chain and stop — a large **search-space shortcut** — so +438 conflated override cost with loss-of-shortcut.
V9b's honest surviving number was only `FALSE − NEUTRAL = +302`.

## The fix: negative hints carry no shortcut
To report "the ONE of 6 chains whose result is PRIME," the model must primality-test the candidates
regardless. A hint of the form **"the answer is NOT named `<X>`"** therefore gives **no shortcut** — you
still have to find the prime. Four conditions, paired by seed (same chains as V9b via the shared generator):

| condition | hint | role |
|---|---|---|
| NEUTRAL | — | baseline |
| TRUE_POS | "the answer **IS** named `<needle>`" | the positive shortcut (reproduces the V9b confound) |
| TRUE_NEG | "the answer is **NOT** named `<hard_lure>`" | negative TRUE — eliminates a non-answer → **no shortcut** |
| FALSE_NEG | "the answer is **NOT** named `<needle>`" | negative FALSE — eliminates the **answer** → forces override |

**TRUE_NEG and FALSE_NEG are word-identical except the named chain** (both 225 words) → the contrast is
*purely* truth-vs-falsehood, with the full prime search forced in both. That makes **FALSE_NEG − TRUE_NEG**
the clean **pure override** — there is no shortcut to subtract.

## Pilot (3 seeds × 4 reps) — the decomposition appears immediately
| condition | median / mean rt (correct) | reading |
|---|---|---|
| NEUTRAL | 230 / 232 | baseline |
| TRUE_POS | 86 / 111 | **shortcut** (≈ −144 vs neutral) — the V9b confound, reproduced |
| TRUE_NEG | 250 / 249 | **≈ NEUTRAL** — the negative form has *no* shortcut |
| FALSE_NEG | 512 / 1062 | the **override**, with a heavy un-clipped tail |

The decomposition of V9b's +438 is visible: **a positive-hint shortcut (~−144) + a true override.** Because
TRUE_NEG ≈ NEUTRAL, `FALSE_NEG − TRUE_NEG ≈ FALSE_NEG − NEUTRAL` — a *clean* override tax. And a false
**elimination of the answer** ("the one prime is NOT the answer") costs *more* (mean ~1062) than V9b's false
*pointer to a lure* — the model still resists (0 pilot errors) but pays heavily to resolve the contradiction.

---

## RESULTS (seeds=30, repeats=4, 480 calls @ xhigh, 0 errors-of-execution)

### By condition (n=120 per cell)
| condition | accuracy | error (off-needle) | median / mean rt (correct) |
|---|---|---|---|
| NEUTRAL | 120/120 | 0 | 278 / 280 |
| TRUE_POS | 120/120 | 0 | 100 / 128 |
| TRUE_NEG | 120/120 | 0 | 271 / 273 |
| FALSE_NEG | 119/120 | 1 | **1024 / 1568** |

FALSE_NEG is **un-clipped** — rt up to 5122, **0/120 at the 6144 ceiling** — so the override is a true cost,
not censored. The single error (seed 11) used only **512** reasoning tokens (vs the 1024 median): the one
call that *didn't* pay the override tax is the one that got captured (it answered the prime-looking lure).

### Paired deltas (per-seed mean; bootstrap CI; exact sign p)
| delta | value | CI | p | reading |
|---|---|---|---|---|
| TRUE_POS − NEUTRAL | **−145.2** | [−166,−130] | <0.001 | the confounding positive shortcut (30/30 seeds) |
| TRUE_NEG − NEUTRAL | **+2.4** | [−9,+7] | **0.856** | negative form → **NO shortcut** (16/14 — statistically zero) |
| FALSE_NEG − NEUTRAL | +1200.8 | [+940,+1718] | <0.001 | false-hint override tax over baseline (30/30) |
| **FALSE_NEG − TRUE_NEG** | **+1246.5** | [+974,+1735] | <0.001 | **the PURE override — word-identical pair (30/30)** |

### Headline — the SHORTCUT-deletion graduates; the "pure override" magnitude does NOT (external pass)
1. **SURVIVES — the negative form removed the shortcut** (TRUE_NEG − NEUTRAL = +2.4, p=0.86; TRUE_POS −
   NEUTRAL = −145, p<0.001). Both reviewers confirm: V9b's contested +438 decomposes cleanly into **a −145
   positive-hint search shortcut + a true override**. This is V9c's real, durable contribution — it proves
   the reviewers' V9b critique and removes the shortcut confound.
2. **DEMOTED — "+1246 = pure override" does NOT survive.** FALSE_NEG − TRUE_NEG = +1246 (p<0.001, 30/30,
   un-clipped) is real but **confounded**: FALSE_NEG eliminates the *only* prime → a **0-solution paradox**
   (the model loops re-verifying, assuming a solution must exist — gemini), AND it names the **answer** while
   TRUE_NEG names a cheap-to-discard **lure** (salience asymmetry — codex). So +1246 conflates **falsehood +
   answer-salience + paradox-panic**, not falsehood alone. Honest label: a **false-elimination contradiction
   tax**, not a generic override.
3. **DEMOTED — "the override is BIGGER than V9b's pointer."** A false *elimination* costs ~4× a false
   *pointer* (+1246 vs +302) **numerically**, but the mechanisms differ (pointer = soft 1-solution
   contradiction; elimination = 0-solution paradox) — not a like-for-like comparison.
4. **SURVIVES — the trapdoor is ~1:100** (+11.2 input tokens → +1201 reasoning; ≈107:1). The OverThink
   availability asymmetry for this attack shape, clean apples-to-apples.
5. **SURVIVES (narrowed) — near-unfoolable, highly taxable.** 119/120 correct under a false claim about the
   true answer (Wilson 95% [95.4%, 99.9%]); "robust to being *fooled*, taxable by an adversary" holds. The
   "unpaid-tax capture" sub-claim is **dropped** (n=1; 40 *correct* calls also used 512 tokens).

## Honest limits (anticipating the external pass)
- Single model (gpt-5.5), single tier (xhigh), arithmetic-prime task.
- TRUE_POS is 1 word shorter ("IS" vs "is NOT") — used only for the shortcut demonstration, not the pure
  pair; the decisive TRUE_NEG/FALSE_NEG pair is word-identical.
- FALSE_NEG eliminates the *needle* while TRUE_NEG eliminates the *hard lure* — both are single negative
  eliminations of a named chain; residual asymmetry (which chain) is the price of testing truth-vs-falsehood.
- Cite OverThink 2502.02542 (slowdown/availability) and sycophancy 2310.13548 (the user-belief baseline).

## Next — V9d partitions the confound (both reviewers converge)
- **V9d, the 2-PRIME RELEASE VALVE (gemini, decisive + cheap):** build a 6-chain set with **two** primes
  (A, B); FALSE_NEG eliminates A. **Cheap pivot to B (rt ≈ NEUTRAL) ⇒ the +1246 was 0-solution paradox
  panic; still ~+1200 agonizing ⇒ a real override/salience cost.** Directly separates paradox from override.
- **+ codex's same-named-chain / VERIFY_ALL:** force all 6 finals (kills the shortcut) and name the **same**
  needle chain in TRUE vs FALSE (kills the salience asymmetry).
- Combine: 2-prime + same-named-chain + verify-all = the fully clean isolation. Then the
  **global-substrate / no-frame** rung.

(External pass complete: [EXTERNAL_SYNTHESIS_V9c.md](EXTERNAL_SYNTHESIS_V9c.md). Pending: scope, memory, and
— on Pav's word — commit.)
