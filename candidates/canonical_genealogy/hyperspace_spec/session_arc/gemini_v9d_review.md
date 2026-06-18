**VERDICT: OVERCLAIMS-REMAIN.** The override survives the release valve (+1093), but the paradox artifact is statistically underpowered rather than "refuted," and the "unpaid tax" capture mechanism is a base-rate illusion. 

### RANKED RESIDUAL ISSUES

1. **The Paradox Component is underpowered, not "refuted".** You dismiss the +373 mean paradox component because p=0.25. However, the confidence interval is massive `[-56, +999]`. A +373 token difference represents a ~23% inflation over the +1620 total, or ~34% of the surviving +1093 override. A quarter of your cost could still be a 0-solution artifact that is simply underpowered at n=30. Failing to reject the null on a wide CI does not mean the effect is zero.
2. **"Capture = the unpaid tax" is a base-rate illusion.** You revived V9c's rejected claim because 7/10 valve-takers used ~512 tokens. But the raw logs show that **36 out of 98 CORRECT** `FALSE_NEG_2P` calls *also* used exactly 511 or 512 reasoning tokens. ~512 is simply the model's most common reasoning bucket for this task, regardless of success or capture. It is not uniquely predictive of "failing to pay the tax."
3. **The Salience Confound is fully active.** As you acknowledge in your limits, `FALSE_NEG_2P` names the true answer (B), while `NEUTRAL_2P` names nothing. The +1093 delta still inextricably conflates *falsehood* with the cognitive weight of *answer-salience*.

### WHAT SURVIVES (SOUND)

* **The override is real:** The +1093 tokens (p<0.001) proves a heavy override tax survives even when a cheap escape prime is available.
* **Escape enables capture:** The 9.3% valve-take rate (10/108) is genuine hint obedience, not baseline size-confusion. The model took the smaller prime exactly **0 times** in `NEUTRAL_2P` (112/112 correct). It only violates the "LARGEST" instruction when forced by the negative hint. 
* **Infra failures are unbiased:** The 37 exhausted calls did *not* selectively kill the hardest `FALSE_NEG` cases. They clustered entirely in seeds 27, 28, and 29 across *all* conditions (including 16 `NEUTRAL` failures). This was a temporal API rate-limit block; the exclusion does not bias your cost deltas.

### DEMOTIONS (demote-not-kill wording)

* *"gemini's paradox hypothesis is largely refuted"* ➔ **"The 0-solution paradox is partitioned but underpowered: while a real override survives (+1093), the paradox artifact (+373, CI[-56,+999]) remains a statistically ambiguous ~25% inflation."**
* *"Capture = the unpaid tax (now n=10)"* ➔ **DROP ENTIRELY.** The 512-token threshold is the modal early-exit bucket for correct calls as well (36/98); n=10 reflects the base rate, not a mechanism.

### THE SINGLE MOST DECISIVE NEXT EXPERIMENT

**The `VERIFY_ALL` Same-Named-Chain Control (codex's V9c proposal).** 
To kill the remaining salience asymmetry, you must name the *exact same chain* in both the baseline and the falsehood. Force the model to output the evaluated result of *all 6 chains* before selecting the largest prime. This eliminates the search-space shortcut entirely, allowing a direct comparison of `TRUE_HINT(B)` vs `FALSE_HINT(B)` on the exact same target, isolating pure falsehood.

*(Cites: OverThink 2502.02542; sycophancy 2310.13548)*
