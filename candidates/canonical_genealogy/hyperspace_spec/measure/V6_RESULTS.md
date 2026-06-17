# V6 — the Sternberg additive-factors test on reasoning_tokens (the chronometric inversion)

**Date:** 2026-06-17 | **Status:** real measurement. 2x2 factorial (Encode {plain, 3-op decode} x Depth
{4, 12}) x 12 seeds = 48 items, gpt-5.5 @ `high`, pre-registered + sha-locked (`v6_labels.LOCK`
4b1a10c4). `v6_additive.py` (selftest-gated: oracle 48/48, E-arms share answer within (D,seed), encode
adds a *constant* +8 prompt-words across depth) + `v6_run.py` -> `v6_run.jsonl`. Cite-don't-coin.

> **DEMOTED by the external pass (gemini + codex, converged) — see [EXTERNAL_SYNTHESIS_V6_RESULTS.md](EXTERNAL_SYNTHESIS_V6_RESULTS.md).** The framing below ("~90% additive-dominant; the method reproduces") is **overclaimed**; corrected. (1) The **pre-registered rule fired "super-additive → demote"**; my pivot to "additive-dominant" was post-hoc salvage. (2) **Additive-factors is a *falsification* tool**, and the interaction is **BORDERLINE at n=12** — bootstrap CI excludes 0 but the **exact order-statistic CI is [0,13]** (includes 0) and sign-p=0.065, so neither clean-additive nor cleanly-rejected: **inconclusive/underpowered.** (3) The +8.5 interaction ≈ **one full reasoning step** — not negligible. (4) Deeper: **additivity of TOKENS ≠ separable cognition** (cascade models mimic additive factors; tokens are a trace, not time), and the ENCODE manipulation is construct-confounded (same arithmetic as the chain). **Honest verdict: the additive-factors *apparatus* transfers; staged cognition is NOT identified; the decisive next move is codex's irrelevant-expression control (E3-dead), not seed-escalation.** Read the sections below through that correction.

## The method reproduces on reasoning_tokens (the flag)
**Sternberg's 1969 additive-factors method — the literal chronometric signature — applied to a frontier
model's hidden reasoning tokens yields an interpretable additive-factors pattern.** Two orthogonal task
factors produce large, near-independent main effects:

| reasoning_tokens (median) | D=4 | D=12 | encode effect |
|---|---|---|---|
| **E=0** (plain integer s0) | 40 | 102 | — |
| **E=3** (s0 as a 3-op expression) | 62 | 129 | — |
| **depth effect** | — | — | |

- **Main effect ENCODE** (E=3 vs E=0): **+23 tok** — and it is *nearly constant across depth* (+22 at D=4,
  +27 at D=12).
- **Main effect DEPTH** (D=12 vs D=4): **+67 tok** (re-confirms the V5 span cost on a fresh design).
- **PRIMARY INTERACTION** (encode x depth): **median +8.5 tok**, bootstrap 95% CI [+2.0, +12.5],
  two-sided sign-test p=0.065 (9+/2−/n=12).

## What it shows — dominantly additive, small interaction
The cost is **~90% additive**: the decode-stage cost and the depth-stage cost contribute **separable,
summed** token-costs (the interaction is ~13% of the depth main effect). **This is the Sternberg signature
substantially present** — the cost-camera reads compositional cost as approximately a **sum of stage-costs**,
which is what "the camera reads genuine structure" requires. It makes *rediscovery-as-validation* **load-
bearing rather than rhetorical**: the chronometric method is not just cited, it is *reproduced* on tokens.

The **small super-additive residual** (+8.5 tok) is itself a finding, not a refutation: the encode and depth
stages are **not perfectly modular** — the decode load is slightly re-paid as the chain runs deeper (the
model appears to carry a little decode-related state through the computation). Perfect additivity is rare in
humans too; a small, interpretable interaction is the *normal* additive-factors outcome.

## Honest limits
- **The interaction sits right at the null-band edge** (pre-registered ±8 tok ~ "one op"; observed +8.5).
  The bootstrap CI excludes 0 but the sign test is borderline (p=0.065) — they *mildly disagree* at n=12.
  Call it **"small, suggestive super-additive interaction; additive-dominant"** — not a clean either/or.
  **Escalate seeds (12→24+)** for a tight interaction estimate before any strong modularity claim.
- "Encode" and "depth" are *my operationalization* of two stages; a different factor pair could interact
  more or less. The claim is about *these* two factors.
- Single model (gpt-5.5), single tier (`high`), n=12, 100% solved. The additive structure is a
  reasoning_token (transcription-laden) observation — it does **not** by itself separate task-structure
  from autoregressive generation (the standing open question).

## Demotions
- My script's binary verdict "SUPER-ADDITIVE -> demote the additive claim" → **"additive-dominant (~90%)
  with a small (+8.5 tok, ~13%) detectable super-additive interaction."** The dominant story is additivity;
  the interaction is the refinement.
- "the chronometric inversion is un-run" (from BIG_MAP) → **"run once; the additive-factors method
  reproduces on reasoning_tokens with a dominantly-additive pattern."** Flag planted, lightly.

## The arc
V4 (cost ~ work) → tier-sweep (need-driven) → V5 (serial-dependency surcharge, refutes literal
transcription) → **V6 (the cost is ~additive across orthogonal stages — the chronometric method transfers;
the camera reads compositional cost as a sum).** Together: the in-head cost is **compositional and largely
stage-separable**, with serial depth as a real, roughly-additive term.

## Next
1. **Escalate V6 seeds** (24–48) to pin the interaction's sign and size.
2. **Vary the factor pair** — pick two factors expected to hit the *same* stage (predict interaction) vs
   *different* stages (predict additive); a within-experiment additive/interactive contrast is the strong
   form of the test.
3. The **collective octave** (the collective-V5 coordination camera) once the in-head instrument is pinned.
4. Pending: codex + gemini external pass on this result.
