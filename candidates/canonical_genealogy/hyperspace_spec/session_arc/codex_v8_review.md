## Verdict
**overclaims-remain** — the primary NULL is reported honestly, but the interpretation still leans too hard on “forced evaluation is the real camouflage tax.”

## Residual Issues
I checked `V8_RESULTS.md`, `v8_camo.py`, and `v8_run.jsonl`. The reported medians and 64/64 accuracy match the raw data. Reconstructing the locked prompts confirms the gap manipulation worked: `MAX_WIDE` top-runner gaps are 40-129; `MAX_TIGHT` gaps are 1-3.

The NULL is not hidden. The doc explicitly says primary `MAX_TIGHT - MAX_WIDE = -6.5`, CI `[-17,+9]`, `p=0.45`, and calls the +170 secondary “not a new camouflage finding.” That is basically honest.

But the +170 reframe should stay demoted. It is fair to say removing the skip cue exposes the already-known full-evaluation cost. It is not fair to call that the V8 camouflage result. `LABEL -> MAX/SUM` still changes skip-vs-evaluate, named-selector vs rule-selector, and task semantics. `SUM` is a good control for “selection is not costly once everything is evaluated,” but it does not purify the LABEL jump into camouflage.

The gap knob is probably the wrong operationalization for exact arithmetic. Once six exact finals are computed, comparing `999 > 998` is not meaningfully harder than `988 > 925`. So the clean inference is not “the model is robust to camouflage”; it is “final-value proximity does not tax this model on this exact-integer max task.” That matters because long-context work shows retrieval can fail under position, distractor complexity, and low lexical/structural distinctness, but those are different mechanisms from exact numeric comparison. See Lost in the Middle, RULER, NoLiMa, and Hidden in the Haystack for the relevant retrieval/distinctness cautions.    

Also: with `n=16`, single model, single tier, and no predeclared equivalence bound, “no detected tax” is stronger than “zero tax.” Lakens’ equivalence-testing point applies: nonsignificance alone is not evidence of exact absence without a smallest-effect-of-interest bound. ([journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/1948550617697177))

## Demotions
Keep: V8 falsifies the preregistered value-gap camouflage prediction for `gpt-5.5@high` on this generator.

Demote: “model is robust to camouflage” -> “model is robust to final-value proximity on exact arithmetic.”

Demote: “forced evaluation is the real camouflage tax” -> “removing a surface skip route exposes the already-established evaluation cost.”

Demote: “binary not graded” -> “this graded gap knob did not matter; skip-vs-evaluate dominated here.”

Demote: “no compute tax” -> “no detected primary value-gap tax; small effects remain possible unless equivalence bounds are set.”

## Next Move
The proposed content-gravity/attention and global-substrate/no-frame rungs are the right direction.

Sharper exact-arithmetic next rung: keep all chains equally executable, but make camouflage operate before or during candidate binding, not after final comparison. Use near-miss structural predicates over traces: easy decoys fail early; hard decoys satisfy most selector predicates and fail late. Pair that with a `SUM`-style full-evaluation control and predeclare an equivalence bound.

Then run the attention version: same arithmetic, same selector, but manipulate salience of the wrong chain by position, variable name, formatting, and lure text. That tests camouflage as attentional capture, not exact value proximity.
