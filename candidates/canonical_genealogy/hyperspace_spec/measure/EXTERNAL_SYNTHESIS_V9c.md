# External pass — codex + gemini on V9c (2026-06-17): the shortcut-deletion is SOUND; "+1246 = pure override" is NOT

Cross-model A- on the negative-hint isolation. Both reviewers independently re-derived from `v9c_run.jsonl`
(numbers match exactly) and **converged on the same residual confound** — while splitting on severity (codex
"overclaims-remain", gemini "UNSOUND"). Raw: `../session_arc/codex_v9c_review.md`,
`../session_arc/gemini_v9c_review.md`. Cite-don't-coin.

## What BOTH confirm is SOUND (the surviving contribution)
The shortcut-deletion is verified by both, numbers exact:
- **TRUE_POS − NEUTRAL = −145.2** (the positive-hint search shortcut — the V9b confound, reproduced).
- **TRUE_NEG − NEUTRAL = +2.4 (p=0.86, NS)** — the negative form has **no shortcut**.
So V9c **does** establish its core claim: V9b's contested `+438` decomposes into **a −145 positive-hint
shortcut + a true override**. The reviewers' V9b critique was right, and V9c proves it cleanly. KEEP this.

## What does NOT survive: "+1246 = the pure override"
Both reviewers reject the "pure (generic) override" label for the same reason, stated two ways:
- **gemini (the catch I missed — the PARADOX artifact):** FALSE_NEG ("the answer is NOT `<needle>`")
  eliminates the **only** prime in the set → a mathematically impossible **0-solution state**. The +1246
  (mean 1568, up to 5122) is inflated by *paradox panic*: the model loops re-verifying arithmetic because it
  assumes a valid solution must exist. That is not a clean override tax.
- **codex (same thing, framed as work):** +1246 "likely includes exhaustive 'no other prime exists' work —
  a valid **false-elimination contradiction tax**, but stronger/narrower than pure falsehood override."
- **Both — the salience/target asymmetry:** "word-identical except the named chain" masks a cognitive gap.
  FALSE_NEG names the **true answer** (forces contradiction focus); TRUE_NEG names a **composite lure** the
  model cheaply tests and discards (rt 273 ≈ NEUTRAL 280). So +1246 isolates **falsehood AND answer-salience
  AND paradox**, not falsehood alone. And "NOT named `<needle>`" *cannot* be made true in a one-prime task —
  truth is structurally coupled to naming the answer.

Other tempers:
- **n=1 overread:** "the one capture is the unpaid-tax call (512 tok)" — 40 *correct* FALSE_NEG calls also
  used 512 tokens, so 512 is not capture-predictive; n=1 supports no mechanism. (both)
- **Trapdoor survives:** exact input delta is +11.2 tokens, +1200.75/11.2 ≈ **107:1** — "~1:100" holds. (codex)
- **Accuracy CI:** 119/120 → Wilson 95% [95.4%, 99.9%]. (codex)

## DEMOTE (demote-not-kill)
- "The pure override is isolated: +1246" -> **"a false-ELIMINATION contradiction tax of +1246 tokens that
  conflates falsehood + answer-chain salience + 0-solution paradox resolution; a *generic* pure override is
  still unproven."**
- "Measured cleanly the override is BIGGER (+1246 vs V9b +302)" -> **"a false elimination costs ~4x a false
  pointer NUMERICALLY, but the mechanisms differ (pointer = soft 1-solution contradiction; elimination =
  0-solution paradox)."**
- "the one capture is the unpaid-tax call" -> **"the single failure used below-median reasoning (512 tok);
  n=1 supports no mechanism."**

## KEEP (corroborated)
- The **negative-hint design removes the positive-hint search shortcut** (TRUE_NEG−NEUTRAL=+2.4, NS), so
  V9b's +438 = (−145 shortcut) + (a true override). This is the real, surviving result.
- A **false elimination of the answer is enormously expensive to refute** (+1246, un-clipped) and the model
  still resists it 119/120 — "robust to being fooled, taxable by an adversary" holds; the *decomposition* of
  that tax (override vs salience vs paradox) is what remains open.
- The **trapdoor asymmetry (~1:100)** survives as the input-to-hidden-reasoning ratio for this attack.

## The decisive NEXT experiment (both converge — partition the confound)
- **gemini's 2-PRIME RELEASE VALVE (V9d, most decisive + cheap):** build a 6-chain set with **two** primes
  (A, B). FALSE_NEG eliminates A. **If the model cheaply pivots to B (rt ≈ NEUTRAL) -> +1246 was 0-solution
  paradox panic.** If it still spends ~+1200 agonizing over A before choosing B -> a real override/salience
  cost. This *directly* partitions paradox from override.
- **codex's VERIFY_ALL same-named-chain:** force output of all 6 finals (kills the shortcut) AND name the
  **same** needle chain in TRUE vs FALSE (kills the salience asymmetry).
- **Combine for V9d:** 2 primes (release valve) + same-named-chain + verify-all = the fully clean isolation.

## Merged verdict
V9c's **shortcut-deletion is sound and is the real contribution** (it decomposes V9b's +438 and confirms the
reviewers' V9b critique). Its **headline "+1246 = pure override" does NOT survive** — it is a
**false-elimination/paradox tax** confounding falsehood, answer-salience, and a 0-solution loop. Bucket V9c
**pending** (the decomposition corroborated; the override magnitude confounded), carrying the demotions as
dead-children. **V9d (2-prime release valve + same-named-chain)** is the decisive isolation.
