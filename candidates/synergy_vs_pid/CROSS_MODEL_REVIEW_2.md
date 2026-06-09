# Cross-model review #2 (2026-06-09) — the reformulation, externally checked

Per the standing rule, **GPT-5.5 + Gemini** were run, blind and independent, on the reformulation finding (the functional-ANOVA interaction gate vs PID; the agent's conclusion "more-than-PID now rests on frame-relativity alone"). They **converged hard**, and walked back more than the bug.

## The two verdicts (terse, both models)

- **RIGHT_BITS_MEASURE (convergent):** the principled bits-measure of pure 2-way interaction is the **MDL gain of the best JOINT model over the best ADDITIVE / GAM main-effects model** — *not* co-information / PID by default. (GPT: "MDL/log-loss gain of joint model over best additive main-effects model, with complexity/noise." Gemini: "the MDL difference between the best unconstrained joint model and the optimal GAM.")
- **CODELENGTH_SALVAGEABLE (both): YES** — with a *flexible* main-effects model (penalized splines / GAM) + proper likelihood / differential-entropy coding + held-out MDL. The raw fixed-grid residual codelength was simply the **wrong instrument**.
- **FRAME_REL_REAL (both — the big one): MOSTLY AN ARTIFACT.** GPT: "mostly artifact … this leak is quantization/readout error." Gemini: "a confound; resolution dependence is purely a quantization artifact of naive fixed-grid entropy estimation." So the resolution-flip we had kept as the *surviving* PID-differentiator is largely a grid-quantization artifact, not a genuine frame-relativity signal.
- **BIGGEST_RISK (convergent):** conflating functional non-additivity with PID synergy while **using an arbitrary-precision grid model that *manufactures* bits** (GPT) / "conflating trivial quantization noise … with fundamental properties of information theory" (Gemini).
- **RECOMMEND (both): GAM-bits** — penalized-spline main effects, likelihood / differential-entropy of the residual, held-out MDL.

## What this means (honest)

1. **The gate is salvageable, and there is now a principled form:** interaction-in-bits = the held-out MDL the best *joint* model buys over the best *separable GAM* model. Done this way it floors **every** separable `f(A)+g(B)` (any shape the GAM fits, including the `|A|+|B|` kink) and flags genuine interaction. This is the correct version of the gate.
2. **But done right, it is a STANDARD quantity** — a GAM interaction / functional-ANOVA term in bits, close to existing statistics and to PID/co-information. **The "more-than-PID" claim does not survive as a property of the *measure*.**
3. **The resolution-"frame-relativity" differentiator is mostly a quantization artifact**, not a deep signal — so it cannot carry the more-than-PID claim either.

**Net:** the framework's genuine contribution is **not a new synergy measure** — the right measure (GAM-bits interaction) is sound but standard. The contribution is the **framing / application** (the frame-indexed genealogy of idea-merges and the fuzzy-LOD render-system), exactly as the latent-cosmology verdict concluded (a new *instrument*, not a new field). The synergy gate should be re-founded as **GAM-bits** (correct + runs on real data); it is a tool, not the novelty. Tier-3; convergence list stays 9; nothing compiled.
