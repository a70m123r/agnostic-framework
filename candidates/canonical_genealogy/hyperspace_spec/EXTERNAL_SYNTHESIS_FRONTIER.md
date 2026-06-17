# External pass — codex + gemini on the frontier plan (2026-06-17)

Two non-Claude models on `FRONTIER_PLAN.md`; they **converged** ([[feedback_cross_model_external_pass]]). Raw: `session_arc/codex_frontier_review.md`, `session_arc/gemini_frontier_review.md`. Demote-not-kill: the plan + sequencing survive; the strong claims get demoted to what the experiments can actually show.

## (1) The graded benchmark (V4) — right move, three guardrails
Both: single-runner-V4-first is correct *because* the multi-runner effort plumbing is known-broken (Claude `output_tokens=6` flat, gemini null). Guardrails:
- **Difficulty MUST be exogenous + pre-registered** — pull from MATH (arXiv:2103.03874), GPQA (2311.12022), ARC (1911.01547), AIME-style exact-answer tasks, with labels FIXED before any run. Author-tuned difficulty makes Spearman ρ **circular** (the model mirrors prompt complexity — the overthinking confound, 2604.10739 / 2507.04023).
- **Demote the claim:** "effort IS difficulty" -> **"GPT-5.5 reasoning-effort correlates with pre-registered external difficulty under this harness."** Spearman on ~25 items is a big-monotone-effect check, not a law; run a tiny instrument/range pilot first.
- **Contamination + variance:** public benchmark items may be in training data; use repeats/seeds, report CIs.

## (2) The PREDICT half — sound as CALIBRATION, not yet a "future camera"
Both: the seal/prior-cut protocol is basically right (plant from C, write `{C_hash, R, s, t_obs}` BEFORE reveal, then score) and it does prevent post-hoc fabrication. But:
- **The seal is weak as built** — a local timestamp isn't a strong commit; use append-only hashes / external timestamping and construct C/T **blind**. v0 is **information-blindness (a holdout), NOT a wall-clock future** — name it honestly.
- **Elicited "sharpness" is the weak point** — a self-declared s is "likely uncalibrated fiction"; LMs self-evaluate imperfectly and worse OOD (Kadavath 2207.05221). **Prefer confidence DERIVED from logprobs / reasoning-tokens**, and score with **proper scoring rules — Brier / log-score / ECE / resolution** (Guo 2017 1706.04599; Gneiting-Raftery), not diagonal eyeballing. ~12 trials is too few to bin.
- **Demote the claim:** "honest forward camera" -> **"calibrated sealed forecaster on this task class."**

## (3) Measurement flaws (both)
- **Claude effort:** thinking-trace length > flat `output_tokens=6`, but it is a PROXY, not bits — provider-policy-dependent, measures verbosity/overthinking, can be non-monotonic with accuracy (2507.04023). Prefer **vendor-reported reasoning/billed tokens**; else report Claude separately / use within-provider budget curves.
- **Never use wall-seconds as effort** — it confounds latency with reasoning.
- **The canonicalizer embedding-cosine gate is STRUCTURALLY WEAK** — cosine conflates *entailment* with *topicality*; it will fail hard negatives. Use an **NLI / entailment model**, not cosine, for the equivalence gate. And 2/3-LLM-agreement "gold" labels are not human ground truth.
- **Mirror coupling** dose-response is fiddly — guard the confound where apparent "back-reaction" is just ordinary V2 digestion of a recovered answer.

## Net — the fixes this pass earns
1. V4: pre-register an **exogenous public-benchmark difficulty** subset; demote "effort is difficulty"; pilot + repeats + contamination check.
2. Predict-half: **hash-seal + blind C/T**; **derive confidence from logprobs/tokens** (not elicitation); **proper scoring** (Brier/ECE); more trials; call it a *holdout* forecaster.
3. Effort: **vendor reasoning-tokens**, never wall-seconds, per-provider; the **canonicalizer needs NLI, not cosine**.
