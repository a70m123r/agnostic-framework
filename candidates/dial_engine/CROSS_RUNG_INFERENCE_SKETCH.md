# Cross-rung inference — ripples ↔ tides: min, max, sweet spot (SKETCH, 2026-06-13)

> Tier-3 sketch from Pav's question after Q6: *"if you can infer the ripples → tides or vice versa, mathematically or statistically — where is the minimum, max and sweet spot?"* Established theory named honestly (post-external-pass discipline: this is mostly known math, organized for the instrument; the proposed B(r→r′) reading is the new operational piece). Nothing run yet.

## 1. The asymmetry (the load-bearing fact)

- **Ripples → tides (fine → coarse): always possible, given WINDOW.** Fine data is a superset — aggregation is computable, so the coarse structure is contained in it. The only limit is observation length: to see a tide of period P you need T ≳ a few P (the slow-end "Nyquist"); the effective sample count is T/τ (Q6's adversary measured exactly this: τ ≈ 532 min → ~19 independent samples in 7 days → the 27-day rotation is unsampled, 0 cycles).
- **Tides → ripples (coarse → fine): impossible for the WAVEFORM, partially possible for the STATISTICS.** Two hard theorems: the **data-processing inequality** (coarse-graining is a non-invertible channel — you cannot un-average) and **Nyquist–Shannon aliasing** (structure faster than half the sampling rate folds irrecoverably into noise). What survives aggregation and can be read back: variance-vs-aggregation scaling (the variance-time plot — how block-mean variance decays with block size betrays fine-scale long memory; this is literally how Hurst exponents are estimated from coarse data), heavy tails (a big enough flare still dominates an hourly mean), and spectral slope.

## 2. Maximum, minimum, and the middle

- **MAXIMUM — self-similar / scale-free processes.** Power-law spectrum, fractal, critical: every rung is the same law at different magnification, so ONE rung determines ALL rungs (up to exponent + amplitude). Cross-scale inference is perfect by construction. Note: flare ENERGIES famously follow power laws (self-organized criticality, Lu & Hamilton 1991), so the sun sits closer to the inferable end than naive intuition suggests — in places.
- **MINIMUM — scale-separated processes (a spectral gap).** Distinct mechanisms at distinct scales: wind makes the ripples, the moon makes the tides — knowing one tells you nothing about the other. A gap in the power spectrum = the rungs are informationally independent. (Pure white noise is the degenerate case: no rung says anything about any other because there is nothing to say.)
- **THE MIDDLE — multi-timescale coupling (our flare).** Q6 measured it: ρ₁=0.996 at 1-min but ρ decays FASTER than the single-exponential extrapolation (0.996^60 = 0.788 predicted vs 0.484 actual) — a spectrum of correlation times (flare rise/decay + active-region evolution), neither scale-free nor scale-separated. Partial cross-rung inference, quantifiable.

## 3. The deep frame (named, not invented here)

- **Renormalization group:** THE theory of how laws transform under coarse-graining. Relevant operators survive zooming out; irrelevant ones wash out; many different ripple-worlds flow to the SAME tide-law (universality) — which is precisely WHY tides→ripples fails: many microstates per macrostate. The coarse law tells you only the fine law's universality class.
- **Mori–Zwanzig (the framework-native gem):** eliminate the fine scale and its effect does NOT vanish — it reappears in the coarse equation as a memory kernel + a NOISE term. And the slow scale, viewed from the fine frame, appears as a DRIFT (a slowly-moving baseline). So, in wrapper vocabulary: **each scale's membrane IS the other scale's kernel.** Viewed coarse, the ripples are the tide-law's residual fuzz; viewed fine, the tide is the ripple-law's unexplained drift. Q6's data already shows BOTH faces: the flare's hourly residual noise (fine scale demoted to membrane) and the orbit's smooth 36→46-bit drift ramp (slow osculating structure appearing as bias in the daily frame). Zooming never deletes the other scale; it relocates it between kernel and membrane.

## 4. The sweet spot (budget-relative, and Q6 already touched it)

- **Without a budget there is no sweet spot:** finer + longer always weakly wins (superset). The sweet spot exists only under a constraint (fixed n samples, fixed cost per sample).
- **Under a fixed budget, for a process with correlation time τ:** sample at **Δt ≈ τ/a-few**, i.e. keep consecutive samples PARTIALLY correlated. At ρ→1 samples are redundant (you re-measure the same state, burning budget); at ρ→0 you are dynamics-blind (each sample independent — you learn the marginal, not the law). Information about the LAW per sample peaks at mid-ρ (the optimal-sampling literature for OU/diffusion parameter estimation puts the optimum at Δt ~ O(τ)). Q6's exact identity (shrink = −½·log₂(2(1−ρ₁))) makes this concrete: our rung ladder walked ρ₁ from 0.996 (redundant end) down to 0.48 — the ladder IS a sweet-spot scan for the persistence law.
- **Multi-timescale processes have no single sweet spot — the answer is an ALLOCATION:** a sampling ladder (short fine bursts for the fast law + long sparse coverage for the slow law), which is exactly how astronomy designs cadences. "Sweet spot" generalizes to "sweet allocation across rungs."

## 5. The measurable (the proposed instrument — the new piece)

**The cross-rung transfer reading B(r→r′):** held-out bits about the rung-r′ law bought per sample of rung-r data — a matrix over the rung ladder, estimated per phenomenon. Operationally: fit the law at rung r′ using data observed at rung r (aggregated if r<r′; via the surviving statistics if r>r′), score in held-out bits vs the rung-r′-native fit, normalize per sample.
- **Minimum** = B block-diagonal (spectral gap: rungs mute about each other).
- **Maximum** = B dense/flat (scale-free: any rung buys every rung).
- **Sweet spot** = argmax over r of B(r→target)/cost — per target, per budget.
- The Q6 identity gives the persistence-law row analytically; the owed "lag-matched zooming law" is B's diagonal; the orbit is the dense-B reference candidate (its law should hold at every rung), the GOES week the mixed case. Cheap to run on already-committed data → natural Sweep-2 instrument, gated on a nod.

**Honest scope:** §1–§4 is established mathematics (DPI, Nyquist, variance-time/Hurst, RG, Mori–Zwanzig, optimal sampling) organized for the dial protocol; the operational B(r→r′) reading bound to the trial-record format is the contribution, and it is engineering. Register: exploratory instrument; E-units law applies (per-sample bits compared within a phenomenon, dimensionless across).
