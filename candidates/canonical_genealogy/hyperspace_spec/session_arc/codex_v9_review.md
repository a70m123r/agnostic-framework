## Verdict (sound / overclaims-remain / unsound, one line)
overclaims-remain: the measurement is real, but “+274 = cost of resisting a false hint” and “robust to being fooled” are stronger than the design supports.

## Residual issues
The TRUE-hint control is indeed decisive. Current V9 shows “a contradictory named-hint condition costs more tokens than neutral,” not cleanly “falsehood resistance.” Without same-format TRUE_HINT, you cannot separate false-hint override from generic hint processing, contradiction resolution, user-suggestion checking, or sycophancy-resistance. That framing is relevant because sycophancy work shows models can favor user-stated beliefs over truth in some settings, but V9’s arithmetic check is much cleaner than those open-ended tasks. ([arxiv.org](https://arxiv.org/abs/2310.13548))

The 0/20 capture result is only “no observed capture on this generator.” The lure is weak: [v9_gravity.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v9_gravity.py:67) chooses the largest non-prime, and my read of the labels shows every lure had a small factor <=7; 14/20 were even. With n=20, 0 captures still leaves a wide upper bound on true capture rate, and the task is short: six chains, four ops, high tier. A prime-looking semiprime/near-miss lure could behave differently.

The +274 token effect is not prompt length: INJECT adds only 8 words, and all 20 paired INJECT deltas are positive. Jitter alone is not a good explanation. But the exact CI should be softened: 14/20 INJECT rows are exactly 512 reasoning tokens, so there is a plateau/quantization smell; there are no repeated calls per seed; and `v9_run.jsonl` stores `got` but not raw replies or full API usage. The CI is over the 20 constructed seeds, not provider stochasticity.

The “prompt injection” analogy needs care. Perez/Ribeiro and Greshake et al. are about instruction hijacking and, for indirect PI, retrieved/untrusted content blurring data and instruction boundaries. ([arxiv.org](https://arxiv.org/abs/2211.09527)) ([arxiv.org](https://arxiv.org/abs/2302.12173)) V9 is currently a misleading in-prompt hint unless you frame the hint as untrusted external content.

## Demotions (demote-not-kill wording)
Keep: “On this locked V9 generator, gpt-5.5@high answered 60/60 correctly, with 0 observed lure captures, and the false-hint condition produced a large paired increase in reported reasoning tokens.”

Demote: “the model is robust to being fooled” -> “no observed capture under a short, easy, weak-lure arithmetic setting.”

Demote: “+274 is the cost of resistance” -> “+274 is the observed paired cost associated with a contradictory false hint; resistance/override is plausible but not identified.”

Demote: “cheap-to-inject / expensive-to-refute trapdoor proven” -> “candidate reasoning-availability asymmetry, consistent with OverThink-style slowdown concerns but not yet isolated.” OverThink is the right nearby citation because it explicitly targets increased reasoning tokens while preserving correct answers. ([arxiv.org](https://arxiv.org/abs/2502.02542)) Sponge examples are the broader availability precedent. ([arxiv.org](https://arxiv.org/abs/2006.03463))

## Next move
Run V9b with paired `NEUTRAL`, `TRUE_HINT`, `FALSE_HINT`, and `FALSE_HINT_PRIME_LOOKING`; optionally keep `SALIENT`. Report `FALSE - TRUE`, `FALSE - NEUTRAL`, `TRUE - NEUTRAL`, capture/error, and an attacker ratio per added input token.

Fix the lure generator: require lure composite with no factor under 11 or 13, preferably semiprime/near-prime, not merely largest non-prime. Add repeated calls per seed, n>=50, at least two tiers/models, and store raw reply plus full usage metadata. Only after TRUE_HINT shows shortcut/savings while FALSE_HINT shows excess cost should the “verify-and-override tax” wording graduate.
