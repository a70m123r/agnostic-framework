## Verdict (sound / overclaims-remain / unsound, one line)

overclaims-remain: the core rank association is sound; the remaining problem is interpretive wording around “executed op-count,” answer-magnitude control, and budget-gate weakening.

## Residual Overclaims

I independently recomputed the main coefficients from `v4_run.jsonl`: `partial(reasoning_tokens, E | display_ops)=+0.894071`, raw `reasoning_tokens~E=+0.879804`, raw `reasoning_tokens~display_ops=+0.177934`, `corr(E, display_ops)=0.000000`. The magnitude/digit robustness also matches: `+0.876992`, `+0.882792`, `+0.876524`.

The demoted headline is mostly honest, but “E equals the exact arithmetic op-count the model executes” is still too strong. E equals the nominal z-chain update count under the intended straight-line interpreter. It does not prove the model internally executed exactly those arithmetic operations. The affine/modulo chain may be collapsible, and reasoning tokens are vendor telemetry, not a trace.

Answer magnitude is not a strawman, but it is weak evidence. Since `raw(E, answer_magnitude)=+0.365` and `raw(tokens, answer_magnitude)=+0.382`, controlling it is a useful nuisance check. But answer value is downstream of the generator, not an independently randomized confounder. Say “robust to an answer-size sensitivity check,” not “answer magnitude ruled out.”

“No right-truncation weakens budget-gate” is directionally fair but overstated. The data show no obvious hard common cap: `exhausted=0`, no null token counts, no pile-up. But a high soft ceiling, adaptive hidden allocator, or tier-specific policy could still produce monotone token use. Also the doc says “max grows with E,” but the max is `192` at `E=8` and `185` at `E=10`; the upper tail rises broadly, not monotonically.

Statistics interpretation is basically correct. Partial exceeding raw is legitimate suppression/noise removal: display length explains some token variance while being exactly independent of E. The permutation p should be reported as Monte Carlo resolution, e.g. `p=0.0003, 0/3000 exceedances with +1 correction`; I also get the same `0.000333` when permuting within display-op blocks. Bootstrap CI `[~0.862, ~0.916]` matches. But the CI is conditional on this generator family and item bootstrap assumptions, not a general arithmetic-task population.

## Further Demotions

Use this wording:

“gpt-5.5 @ fixed `effort=high` shows a strong rank association between vendor reasoning-token count and the generator’s nominal effective z-update count, net of displayed operation count, in a 100%-solved compositional arithmetic execution task.”

Replace:

“E equals exact arithmetic op-count the model executes”

with:

“E is the intended direct-execution z-chain operation count; internal execution strategy is not observed.”

Replace:

“not merely answer magnitude”

with:

“not eliminated by post-hoc controls for answer magnitude/digit count.”

Replace:

“no right-truncation weakens budget-gate alternative”

with:

“no evidence of a hard common right-censoring ceiling in this sample; soft/adaptive budget explanations remain open.”

Add to “V4 CANNOT claim”:

“Not a validation of reasoning tokens as cognitive effort or reasoning depth; only a vendor-token association with a controlled task knob.”

“Not fully pre-registered at the full-stimulus level for the actual run if the original run lock was the weaker `99ebbc...` lock; current full-stimulus/tier lock appears post-hoc hardened.”

## Next Move

V5 WIDE-vs-DEEP is the right decisive test. This is exactly the work-vs-span separation used in parallel-algorithm thinking: total work and critical-path depth are distinct quantities, classically separated in Brent-style analysis of arithmetic expression evaluation (Brent, 1974, JACM, DOI `10.1145/321812.321815`).

Cheapest decisive version: do a small V5-lite slice before a full grid. Hold displayed statements, total arithmetic ops, answer digits, and answer magnitude bands approximately fixed. Compare one long dependent chain against many independent short chains plus a final reduction. If tokens differ at fixed work, you have depth/span evidence. If they do not, V4 was mainly volume/work.

Also run a cheap tier sweep on a small V4/V5 subset (`low/medium/high`) to test the budget-gate story. That is not a substitute for WIDE-vs-DEEP, but it directly probes whether the slope is an adaptive tier-budget artifact.

Relevant real references: Spearman’s rank association originates with Spearman 1904; bootstrap inference with Efron 1979; permutation/regression residualization concerns are in Freedman & Lane 1983; work vs depth/span separation is grounded by Brent 1974.
