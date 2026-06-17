## Verdict

**overclaims-remain** — V6b is a strong negative control against **pure expression-text transcription** for the ENCODE factor, but “~73% compute” is too literal. The honest claim is: **making the 3-op expression operationally task-relevant costs substantially more reasoning tokens than merely showing the same expression in a dead/commented form.**

## Residual Issues

E3dead is a valid control, but not a perfect one. It shows the expression text does not automatically induce E3live-level tokens: raw data are 96/96 correct, text deltas are positive in 28/32 pairs, compute deltas in 30/32, with medians matching the report. That rejects the strongest “same text, same scratchpad transcription” story.

But E3dead does **not** prove the model literally ignored the dead expression. It may parse it, cheap-check it, partially verify it, or treat the supplied scalar as authoritative. “Near E0” proves only that any such activity was not expensive under this prompt.

`E3live - E3dead` is not a clean pure-compute isolation. It bundles: required RHS evaluation, absence of an already-bound scalar, assignment semantics versus comment semantics, and the strong “already computed / do NOT recompute” instruction. The length asymmetry blocks a simple “longer prompt caused more reasoning tokens” objection, but it does not prove conservative bias in all directions. The longer E3dead prompt also contains the shortcut and the prohibition, which can reduce effort.

The 73/27 split should be treated as a **within-design descriptive decomposition**, not a mechanistic fraction of hidden cognition. It assumes additive text and compute components and no instruction-induced short-circuit. That assumption is plausible enough for a project note, not for a decisive mechanistic claim.

Methodologically, this sits near the additive-factors caution: factor contrasts are useful probes, but they do not identify internal architecture without extra assumptions. Sternberg’s additive-factors method is the relevant ancestor; Stafford & Gurney show why additive patterns can mislead about stages, citing McClelland’s cascade result. See Sternberg 1969, Stafford & Gurney 2011, and McClelland 1979. ([frontiersin.org](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2011.00287/full)) ([frontiersin.org](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2011.00287/full)) ([frontiersin.org](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2011.00287/full))

## Demotions

Demote “COMPUTE-DRIVEN, encode load is ~73% compute” to: **“For this gpt-5.5@high 3-op ENCODE manipulation, task-relevant evaluation adds a larger token surcharge than dead expression text; pure literal transcription is not sufficient.”**

Demote “first direct evidence reasoning_tokens track real computation” to: **“first direct within-project evidence that reasoning_tokens respond to required evaluation beyond expression text.”**

Demote V4 rehabilitation to partial: **V6b weakens the global pure-transcription worry, but V4’s work-slope can still be per-step trace/carry/output policy, not necessarily computation in the strong sense.**

Demote V5/DEPTH rehabilitation harder: **not resolved.** V6b says little about span, serial carry, routing, or value-level transcription. Brent-style work/span separation is still the right conceptual frame, but this experiment only tests an encode-side 3-op decode. Brent 1974: https://doi.org/10.1145/321812.321815

Demote external validity: **single model, single tier, n=16 seeds, one generator family, one call per item.** The p-values are strong conditional on this item family; the ratio is not a portable constant.

## Next Move

Yes: run the **dead-chain V5 control** next. Same chain text, same final answer, but one arm must execute the serial chain and the dead arm is given the chain result and told not to recompute. That directly attacks the remaining DEPTH/span worry.

Add one small V6b ablation if budget allows: length/instruction-balanced variants where E3live also gets an explicit “you must compute this RHS” annotation and E3dead gets neutral filler matched in length. That would turn the current strong result into a cleaner identification.
