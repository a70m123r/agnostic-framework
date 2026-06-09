# Ratio frame-relativity test (2026-06-09) — does frame-relativity survive as a dimensionless ratio?

Motivated by `agnostic_units_hairy_membrane_SKETCH.md §6`: the cross-model called the gate's frame-relativity a "quantization artifact" — but it judged the **absolute** grid-codelength. A **dimensionless ratio** cancels the grid-bits. So: does frame-relativity survive as a ratio where it died as absolute bits?

## Construction
`interaction-fraction = Var(interaction)/Var(M)`, where `interaction = M − best separable polynomial main-effects fit f(A)+g(B)` (degree 3, **no cross terms** → floors any separable, incl `A²+B²`), on data quantized to `b` bits, swept across the band. Dimensionless → raw grid-bits cancel. Script: `ratio_frame_test.py`.

## Result (interaction-fraction vs resolution b)

| case | b16 | b12 | b10 | b8 | b6 | b5 | b4 | b3 | b2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SYN `0.5A+0.5B+0.5·A·B` (large interaction) | 0.332 | 0.332 | 0.332 | 0.332 | 0.333 | 0.338 | 0.372 | 0.516 | 0.534 |
| ADD `0.5A+0.5B` (separable/affine) | 0.000 | 0.000 | 0.000 | 0.000 | 0.003 | 0.012 | 0.049 | 0.198 | 0.506 |
| SEP `A²+B²` (separable nonlinear) | 0.000 | 0.000 | 0.000 | 0.000 | 0.006 | 0.023 | 0.080 | 0.290 | 0.884 |
| INT `A·B` (pure interaction) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.998 | 0.990 | 0.987 |
| ALLOY `0.5A+0.5B+0.1·A·B` (small interaction) | 0.019 | 0.019 | 0.019 | 0.020 | 0.022 | 0.031 | 0.068 | 0.214 | 0.629 |

## Read (honest)
- **At FINE resolution (b ≥ 8): clean, frame-STABLE, bug-fixed.** Real interaction (SYN 0.33 / INT 1.0 / ALLOY 0.02) vs separable floored (ADD 0.00 / `A²+B²` 0.00), **flat** across b=16..8. The dimensionless ratio kills the grid-bits artifact **and** fixes the earlier separable false-positive. A sound interaction **diagnostic.**
- **At COARSE resolution (b ≤ 4): everything blows up, including separable** (ADD→0.51, SEP→0.88). A coarse-quantization / underpowered-fit artifact (a separable polynomial on ~4 levels can't fit the step-functions, manufacturing false interaction).
- So **frame-relativity does NOT survive as a genuine signal here** — flat where the measure is clean, artifact where it varies.

## Cross-model (GPT-5.5 + Gemini, per the standing rule)
Both **confirm** the coarse-blowup is an underpowered-fit artifact, and both keep the fine-resolution ratio as a sound **diagnostic** (not a standalone emergence criterion). Two sharpenings:
- **GPT (the important nuance):** this only *weakly refutes one implementation-specific resolution effect* — it does **NOT settle frame-relativity broadly.** A quantization-resolution sweep is **not** a test of the framework's **observer-kernel** frame-relativity ({time, space, knowledge, meaning}); that's a different thing, and it's left untested here, not refuted.
- **Both (the deep caveat):** defining interaction as *residual-variance-after-a-separable-fit* **confounds genuine interaction with main-effect model misspecification** — any underpowered or wrong-basis main-effects model manufactures false "interaction." The measure is only as good as its separable model; it needs a flexible, **held-out GAM** (the earlier GAM-bits recommendation), and even then it's a diagnostic, not the sole criterion.

## Verdict
- **Resolution-as-frame "frame-relativity" is confirmed an artifact — settled.** The ratio instinct was right (it removes the grid-bits artifact and yields a clean fine-resolution measure), but there is no genuine *resolution*-frame-relativity to rescue.
- **The broader observer-kernel frame-relativity is NOT settled by this** — the quantization sweep never tested it; it stays an open, separate question needing a test that varies the actual **frame** ({time/space/knowledge/meaning}), not the grid.
- **Keep:** the fine-resolution dimensionless interaction-fraction as a sound **diagnostic**, built on a properly-specified (flexible + held-out) separable model.

Tier-3; convergence list stays 9; controlled ground-truth only; nothing compiled.
