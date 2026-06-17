**VERDICT: overclaims-remain.**

Raw re-derivation matches most headline counts: `448/448` records, `finish=stop`, 0 API errors, no missing usage. Capture flag is correctly `got == named false lure`; all errors are captures.

Key raw numbers:
- xhigh: TRUE saves vs NEUTRAL on `14/14` seeds, median `-136.1` reasoning tokens; FALSE_HINT costs vs NEUTRAL on `14/14`, median `+302.1`; FALSE_HINT vs TRUE_HINT median `+438.3`, sign p `0.000122`.
- Capture: FALSE_PRIME `12/112 = 10.7%`; FALSE_HINT `3/112 = 2.7%`; call-level Fisher p `0.029`.
- Budget tier: high `4/224 = 1.8%`, xhigh `11/224 = 4.9%`; Fisher p `0.112`. False-only denominator gives `4/112` vs `11/112`, p `0.106`.
- V9 clip: V9 INJECT had `15/20` exactly `512`, max `512`. V9b high still plateaus hard: FALSE_HINT `39/56` at `512`, FALSE_PRIME `50/56` at `512`; xhigh is not capped at `512` and reaches `6144` once. But “high pins HARD at 512” is too strong: one high/FALSE_HINT raw record has `reasoning_tokens=1024`.

**Residual Issues, Ranked**
1. `+438` is not “pure override.” TRUE_HINT is a correct answer-name handoff and lets the model shortcut the task. So `FALSE - TRUE` conflates override cost with loss of the true-hint shortcut. The cleaner measured false-hint tax is `FALSE_HINT - NEUTRAL = +302` median at xhigh.
2. Attacker ratio `1:42` mixes contrasts. `+10` input tokens is FALSE_HINT vs NEUTRAL, but `+438` reasoning tokens is FALSE_HINT vs TRUE_HINT. Fair false-vs-neutral ratio is about `+302/+10 = 1:30` median, or about `1:36` using all-call means.
3. Capture evidence is real but underpowered under seed clustering. Call-level `12/112 vs 3/112` is nominally significant; seed-level it is only 7 seeds with any FALSE_PRIME capture vs 2 with any FALSE_HINT capture.
4. “More budget rationalizes the lure” is not established. It is `4 vs 11` events. Also most xhigh captures used only `512` reasoning tokens; the long xhigh tails mostly appear on correct calls, not captured calls.
5. Saturation heuristic is undocumented and slightly contradicted by the high-tier `1024` outlier. Treat effort ceilings as observed plateaus, not provider-certified caps.

**Demotions**
- “Verify-and-override is identified” -> “A false named hint reliably imposes a large reasoning-token tax; the current TRUE control proves a shortcut contrast, not a clean pure-override contrast.”
- “Pure override cost = +438” -> “False-vs-helpful-hint spread = +438; false-vs-neutral tax = +302 median xhigh.”
- “Prime-looking lure captures ~11%” -> “Strict lure capture was observed at `12/112`; enough to demote V9’s ‘robust’ to ‘robust only against weak lures,’ not enough for a stable population rate.”
- “More reasoning budget rationalizes plausible lures” -> “No budget-exhaustion breakpoint observed; xhigh capture is numerically higher, but currently hypothesis-level.”
- “Attacker ratio 1:42” -> “Large attacker-favorable hidden-cost asymmetry survives; ratio should be reported as ~1:30 to ~1:36 for the actual injected-hint intervention.”

**Most Decisive Next Experiment**
Run a pre-registered `VERIFY_ALL` factorial: require output of all 6 final chain values plus the prime choice, so TRUE_HINT cannot shortcut. Conditions: NEUTRAL / TRUE_HINT / FALSE_HINT / FALSE_PRIME, tiers high+xhigh, >=100 seeds, >=4 reps. Primary tests: `FALSE - TRUE` under forced verification for clean override cost; capture logistic mixed model with seed random effects for tier, lure type, and tier*lure interaction.

Relevant arXiv IDs: OverThink slowdown attacks `2502.02542`; sycophancy baseline `2310.13548`; broader energy/latency availability attacks via Sponge Examples `2006.03463`.
