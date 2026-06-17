## Verdict

**V5b: overclaims-remain.** The core contrast is sound: live execution costs far more than carrying dead chain text, and the live-dead surcharge scales with depth. I reproduced the key raw pattern: D12 live-dead median `+63.5`, D4 live-dead `+12`, and the paired compute-slope D12-D4 is positive for all 16 seeds.

But “transcription-proof” is too strong. V5b controls **input text length** and visible final output, not hidden scratchpad/output-trace length. The dead arm says the operations were already applied and gives the result; the live arm must execute the chain. If reasoning_tokens are one latent line per executed step, V5b would show exactly this depth slope. So the honest claim is: **input-text transcription is rejected; hidden execution-trace transcription is not ruled out.**

**V7: overclaims-remain.** The result supports: labelled `w` distractors are largely skipped, and labelled clutter adds a reasoning-token burden. But “not a compute tax” should be demoted to **no detectable compute tax under explicitly labelled, length-confounded distractors**. Inert prompts are longer than ops prompts: median prompt words `161 vs 137` at k=6 and `245 vs 197` at k=12. A small ops-compute cost could be masked by the inert arm’s length.

Also, the burial test is easy-mode burial. The harness globally says “Track ONLY the variable s” and inline labels every `w` line as “distractor, ignore.” That is a fair test of explicit filtering, not camouflaged burial.

## Residual Issues

- V5b’s live-dead contrast is “must execute serial state updates” vs “report a given result,” not “same output trace, different compute.”
- V5b therefore proves more than prompt-length sensitivity, but less than mechanism: it cannot separate arithmetic computation from latent step-by-step trace production.
- V7’s “reading tax scales with clutter volume” is only partly supported. Inert-k0 is positive at k=6 and k=12, but inert12-inert6 was weak in the raw run: median `+4`, sign-test p about `.45`.
- V7 only licenses claims about explicitly marked irrelevant `w` variables. It says little about unlabelled distractors, relevant-looking arithmetic, or distractors sharing the target variable namespace.
- Both experiments are single model, single tier, n=16 seeds. The decompositions are descriptive within-design contrasts, not mechanistic fractions.
- This matters because CoT-style traces can improve performance while still being hard to interpret mechanistically; see Wei et al. on chain-of-thought prompting, and Turpin et al. plus Lanham et al. on CoT faithfulness concerns.

## Demotions

- Demote **“depth-scaling is transcription-proof”** to: **“depth-scaling is prompt-text-proof and visible-output-controlled; it remains compatible with a latent execution trace that scales one step per operation.”**
- Demote **“V5 span is real serial computation, not transcription”** to: **“V5b detects a depth-dependent hidden-token surcharge when serial execution is required; this is consistent with serial computation, but does not exclude hidden trace-writing as the implementation.”**
- Demote **“V7 shows no compute tax”** to: **“V7 finds no detectable extra cost for explicitly labelled ops distractors relative to longer inert distractors.”**
- Demote **“burial taxes attention proportional to clutter volume”** to: **“labelled clutter adds a reading/filtering burden; the volume dose-response needs stronger length-matched evidence.”**
- Demote **“V5b+V6b reject the pure-transcription worry on both axes”** to: **“V5b+V6b reject a pure prompt-copy/input-text account and show required execution affects reasoning_tokens on encode and span tasks; they do not fully reject the hidden scratchpad-transcription account.”**

## Next Move

Run a V5c output-trace control: same depth, same visible output, and a matched latent-trace demand, but one arm only follows/copies/verifies provided states while the other computes states. Add identity/no-op chains as a same-step-count low-arithmetic control.

Run V7b with exact token-length matching and camouflaged distractors: unlabelled lines, target-like variables, mixed relevant-looking operations, and no global “track only s” instruction. Then replicate across models/tiers with larger n and repeated calls.

Sources: Wei et al., 2022, “Chain-of-Thought Prompting Elicits Reasoning in Large Language Models” https://arxiv.org/abs/2201.11903; Turpin et al., 2023, “Language Models Don’t Always Say What They Think” https://arxiv.org/abs/2305.04388; Lanham et al., 2023, “Measuring Faithfulness in Chain-of-Thought Reasoning” https://arxiv.org/abs/2307.13702.
