## Fatal flaws

- The design is not actually locked. It states the primary effort statistic is `reasoning_tokens@high`, then later says Spearman uses `effort-to-first-correct = min reasoning_tokens over {low,medium,high}` with failed items censored at the ceiling, then demotes that same min-over-grid metric near the end. That is fatal for preregistration: the primary estimand is ambiguous.

- The knob is only exogenous in the weak sense “chosen before the model call.” For mod-arithmetic chains, nested parens, SAT lists, and partly multiplication, the knob directly changes visible operation count, prompt length, candidate count, symbol count, and the minimum possible scratchpad trace. A positive rho can mean “the model emitted more hidden tokens because the prompt visibly contains more steps,” not “effort tracks latent difficulty.” Partial Spearman controlling `prompt_token_count` is not sufficient; for F1/F4 the control is almost collinear with the knob, so the residualized test is underidentified or just noise.

- The stated power is not credible. Per-family `n=15` with five tied ordinal bands and only three seeds per band is too thin for bootstrap CIs with real meaning. A 4000-permutation p-value may be computationally neat, but it does not create information. Small-sample Spearman tests are fragile; Yu & Hutson explicitly warn that standard Spearman inference performs poorly at small sample sizes and under non-normal dependence, motivating robust permutation methods. ([arxiv.org](https://arxiv.org/abs/2008.01200))

- The effort metric may measure a vendor controller, not need. `reasoning_effort='high'` can be a budget/policy gate: “allowed to think this way,” not “needed this many tokens.” The design notices this in open questions but still builds the headline on it. The Illusion-of-Thinking paper is directly relevant: reasoning effort can rise with complexity and then fall despite remaining budget. ([arxiv.org](https://arxiv.org/abs/2506.06941)) Pinning failures to a ceiling or falling back to solve-rate does not rescue the effort claim; it changes the claim.

- The seal is not adversarially committing. `sha256(answer||nonce)` fixes the brute-force problem for tiny answers, but the local hash chain can be regenerated after seeing outcomes unless a chain head is externally witnessed before reveal. Residual trust assumption: the operator did not rewrite the whole local log, did not backdate `t_obs_iso`, and did not regenerate nonces. That is self-attestation, not an external seal.

- The confidence channel is probably overclaimed. `top_logprobs` over a small answer set is only a probability over the actually observed/top-k tokens unless every candidate token is scored. Temperature or Platt scaling can correct monotone miscalibration, but it cannot manufacture resolution if all raw scores are collapsed near 0.99. This is exactly the danger in LM calibration work: Jiang et al. find generative LM probabilities poorly calibrated for QA, and Tian et al. report RLHF model conditional probabilities can be very poorly calibrated. ([arxiv.org](https://arxiv.org/abs/2012.00955)) ([arxiv.org](https://arxiv.org/abs/2305.14975))

## Fixable flaws (each with the concrete fix)

- Fix the estimand conflict: rewrite the spec so there is one primary test only: `partial Spearman(reasoning_tokens@high, effective_ops | display_features)` on correctly completed, non-instrument-limited calls. Put min-over-effort, solve-rate, censored failures, and low/medium/high curves in explicitly secondary tables.

- Fix the tautology: make display length and effective difficulty independently manipulable. Add a factorial generator with `display_ops` and `effective_ops`: same number of visible tokens/operators, different dependency depth; same dependency depth, different filler/surface length. For F1/F4, include no-op/independent-operation controls. For F3, hold candidate-list length constant while varying constraint dependency. Then control `display_ops`, `prompt_tokens`, number count, operator count, and candidate count.

- Fix power before calling models: run a simulation-based power analysis using plausible within-band token variance. Minimum revision: 4 families x 5 bands x 10 seeds = 200 primary calls at fixed high. Better: 15-20 seeds per band if the expected rho is below 0.5. Add repeated calls for at least 20% of cells to estimate run-to-run token variance and report ICC.

- Fix permutation/bootstrap: use stratified or residual permutation appropriate to the partial-rank model, not vague “4000 perms.” Bootstrap by item/seed within family, not by three seeds pretending to support stable CIs. Predeclare tie handling.

- Fix non-monotonicity: do not convert failed solves into fake high effort. Treat failures as a separate binary outcome and analyze token effort conditional on success. If censoring is central, use a censored-rank or survival-style analysis; otherwise call it solve-rate, not effort.

- Fix the seal: publish the preregistration hash and each prediction-chain head to an external witness before reveal: OSF, GitHub commit pushed to remote, OpenTimestamps, RFC3161 TSA, Sigstore/Rekor, or an emailed hash to external auditors. Without that, call it a local tamper-evident log.

- Fix confidence scoring: first run a blinded calibration pilot measuring raw logprob dynamic range and rank discrimination. Score every candidate, not just top-k if possible; otherwise restrict candidates to a small fixed alphabet guaranteed to appear in top-logprobs or use pairwise forced scoring. Use train/calibration/test splits. With only ~40 trials, do not make strong ECE claims; Nixon et al. show ECE is highly sensitive to binning choices. ([arxiv.org](https://arxiv.org/abs/1904.01685)) Use Brier/log loss plus Murphy reliability-resolution-uncertainty decomposition as descriptive, not decisive, unless N is much larger. Brier and Murphy are the right lineage, but the sample size must match the claim: [Brier 1950](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2), [Murphy 1973](https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2).

- Fix contamination/circularity: remove the GSM8K/MATH/AIME anchor gate from the primary design or demote it to descriptive sanity check. It reintroduces public benchmark contamination and human-hard/model-hard mismatch. Also stop saying “contamination-free”; say exact-item contamination-minimized.

## Claims to demote (demote-not-kill, give the demoted wording)

- Demote “the parametric knob is exogenous difficulty” to: “the knob is a preregistered synthetic operation-count/display-complexity variable; whether it isolates model difficulty is tested by length- and display-matched controls.”

- Demote “partial Spearman controls the length confound” to: “partial Spearman is a sensitivity check; causal separation requires matched generators where prompt length and effective operation depth vary independently.”

- Demote “reasoning_tokens measure effort needed” to: “reasoning_tokens are a vendor-reported hidden-token consumption signal under a fixed inference policy.”

- Demote “solve-rate fallback confirms difficulty if token effort fails” to: “solve-rate validates task difficulty, not the reasoning-token effort axis.”

- Demote “sealed forecaster” to: “locally tamper-evident information-blindness holdout unless chain heads are externally witnessed before reveal.”

- Demote “logprob confidence is a rigorous probability” to: “raw conditional token scores from RLHF/non-reasoning models, usable only if a held-out calibration test shows non-collapsed resolution.”

- Demote “contamination-free by construction” to: “fresh exact instances from familiar synthetic task families; exact-item leakage is minimized, task-distribution familiarity remains.”

## Verdict (build / revise / drop, one-line why)

Revise: the idea is worth building, but the current locked design would mostly measure visible operation/display length plus vendor budget behavior, with too little power and no adversarial seal.
