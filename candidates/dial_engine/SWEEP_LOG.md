# DIAL PROTOCOL — SWEEP LOG (append-only)

> Dated record per sweep, per `DIAL_PROTOCOL_SPEC.md` §3.7. Never edit a prior section.

---

## Sweep 0 — 2026-06-12 (retro-encode of the cosmic-coin probe)

**Seat:** `dial-sweep-00-retro-encode` (Fable, main loop). **No new measurement** — sweep 0 encodes the cosmic-coin probe's actually-measured grid (`../cosmic_coin_probe/`: harness + 3 re-measure agents + Opus adversary, all real JPL/NOAA data) as the first 18 trial records in `runs/dial-sweep-00.jsonl`, exercising the record format end-to-end. Every number traces to `results.json` / `FINDINGS.md` / the adversary scripts; family-level results where the probe retained only ranges (MA family, sub-window bands) are encoded as range-records, disclosed in-line.

**Pairs covered:** (mars-heliocentric-position, position-from-t0-state) and (goes18-xray-long, next-minute log-flux), plus the per-moment mixture `inferred` for both.

**Decomposition (probe §5 adversary table, re-read as protocol output):**
- **Engine band:** coder ladder ratio-of-CR 1.33–2.03× (never inverts); predictive family moves flare saved-frac 0.213→0.454 and deflates onset magnitudes ~26× (599→22.8 bits). Margin = **engine-calibration band** ~1.17×–2.8× [corrected 2026-06-13; was "render band" — see Sweep 0.1].
- **Frame observables:** window sub-splits (orbit 1.92–2.72, flare 1.09–1.23), channel swap (long 1.27 vs short 1.02), onset-removal (1.21 — killed the quieter-reads-sharp conjecture).
- **Interaction flags:** Student-t helps flare / hurts orbit (tail weight is structure of the framed thing) — `dial-mars-0004` × `dial-goes-0008`.
- **Dial-jumps:** none. Persistence holds as flare kernel candidate; `ar1-on-increments` (1.30 vs 1.27) flagged within-band, held for an out-of-sample re-trial before any jump.
- **Dead children inherited:** 6 (FINDINGS §7), encoded where they were trial-shaped (`dial-goes-0004/0005/0006`, the onset-magnitude demotion in 0008/0012 notes).

**NOT done (gated):** `tools/compile_dials.py` (the deterministic compiler), the viewer dial panel, the conjecture-engine seat — all await a Pav/Cowork nod on the spec. Opus skeptic pass on the SPEC itself + the GPT-5.5/Gemini external pass: owed.

**Proposed for sweep 1 (apply after a nod):**
- First live sweep: the S1 coupling pair (framed: LEO satellite orbit residuals × solar indices; inferred: does the joint compress better than the parts — the synergy gate on real sky data).
- Or the Q6 scale-rung sweep: same GOES flux at 1-min / 10-min / daily / monthly rungs — hardness-vs-rung as the first measured frame-relativity curve.
- Candidate registry seeding: regime-switching (HMM quiet/onset), ARFIMA, and a symmetric best-fair-predictive search for BOTH phenomena.

---

## Sweep 0.1 — 2026-06-13 (external-pass corrections)

**Seat:** `dial-sweep-00.1-external-pass-correction` (Fable, main loop). Folds the GPT-5.x + Gemini external pass (`../cosmic_coin_probe/external_pass/SYNTHESIS.md`) back into the protocol. Append-only: Sweep 0's records stand; corrections enter as supersession records + relabels.

**The headline lesson, in protocol terms:** the external pass caught the protocol violating its OWN attribution rule twice — (1) labelling the coder+predictive margin "a render knob" when coder/predictive are ENGINE dials (engine-calibration band), and (2) the `attack_misspec2.py` orbit-Student-t bug, which moved the predictive dial and the quantization dial with one knob (Q=1e-3 applied to the orbit's q=1 km residual, +29.9 bits). Both are now CANONICAL specimens of the rule working: a dial mislabel and an uncontrolled turn.

**Corrections applied:**
- **Supersession:** `runs/dial-sweep-00.jsonl` gains `dial-mars-0004-corr`, superseding `dial-mars-0004`. The orbit Student-t was reported at 71 bits/step ("t HURTS orbit"); the bug fixed, recomputed = **41.10 (NEUTRAL vs Gaussian 41.19)**. The interaction is corrected: **t helps the flare, neutral on the orbit** — the cross-pair sign holds via the orbit's own shrink/saved-fraction (engine-band), not via a t-penalty.
- **Relabel:** "render band/knob" → "engine-calibration band" here (Sweep-0 decomposition line) and across FINDINGS + `DIAL_PROTOCOL_SPEC §2`.
- **New engine dial named:** `formalism/accounting` (Pav: "the formal dressing is the knobs we can turn") — probability semantics x cost model x loop framing, each setting carrying well-formedness conditions on the record (spec §1.2 + the §2 formalism corollary). The overclaims (Solomonoff-as-identity, free-energy-as-equivalence) are now SETTINGS of this dial, not assertions.
- **Harness v0.2** (`../cosmic_coin_probe/harness.py`, `results.json` now `cosmic_coin v0.2`): per-axis-SUM entropy (Jensen fix), debiased NLL (drift miscentering fix), σ-shrink convention NAMED (14.44 per-dim-mean-of-log-ratios PRIMARY vs 13.98 ratio-of-mean-σ), disclosures (flare H_raw iid-proxy inflation; in-sample calibration; conditional MDL). Effect on the trial readings: orbit appearance 43.30→38.56 (the bugs had inflated the orbit; corrected it is sharper); **σ-shrink 14.44 vs 3.50 and comp-ratio separation 1.87× UNCHANGED** — the cross-pair direction is bug-independent.

**Decomposition, corrected:**
- Engine band: coder 1.33–2.03×; predictive moves flare saved-frac 0.213→0.454 and is NEUTRAL on the orbit (was wrongly "hurts"). Symmetric best-fair-predictive: flare gains, orbit holds → gap narrows but orbit stays ahead (0.529 vs 0.454).
- Frame observables: unchanged (window/channel/onset-removal).
- Dial-jumps: still none.
- Dead children: the probe's tally grows 6 → 12 (FINDINGS §12 children 7-12: t-hurts-orbit retracted; Solomonoff-identity, render-knob, rate-of-change-as-law, E-units-law + free-energy-correspondence demoted; harness v0.1 bugs fixed).

**External verdict folded (honest):** both models judge the physics/epistemics as standard MDL + signal-processing repackaged, with the DIAL PROTOCOL engineering as the genuine contribution. Sweep-1 candidates unchanged (S1 drag×solar synergy / Q6 scale-rung curve); ADD experiment **A4 — the formalism dial must pay** (expected-information-gain acquisition vs round-robin; makes "is the active-inference framing decoration?" a measured reading).

---

## Sweep 1 — 2026-06-13 (Q6 scale-rung: the first LIVE sweep)

**Seat:** `q6-scale-rung` workflow (Fable re-measure x3 + Opus adversary + Fable synthesis, 5 agents). The protocol's first real experiment (vs Sweep 0's retro-encode). Tests FINDINGS Q6: is hardness scale-relative — does coarsening the GOES flare's cadence (the scale-rung FRAME dial) change its compressibility? Experiment: `experiments/q6_scale_rung/` (instrument + FINDINGS + 6 agent scripts + workflow result).

**Result: the naive child is DEAD; the parent is REFINED and SHARPER. 0 reversals.**
- **Refutation (coder-robust, significant):** under the persistence law the flare is decisively lawful at 1-min (comp-ratio 1.270, **z=+89.8** vs the 200-seed iid-noise floor) and DECAYS monotonically into the floor by 30-60 min — the OPPOSITE of the naive "fuzzy-at-fine becomes lawful-at-coarse." Paired drop rung1-rung60 = +0.237 [+0.178,+0.288], 5-15x the within-null wander; holds across lzma-9/zlib-9/bz2-9, mean AND decimate, coded-bits AND coder-free sigma-shrink. The decimate control is the clincher: the iid floor stays FLAT under decimate (rises under mean = variance-reduction contamination, as the design feared) — so the decay is NOT a smoothing artifact.
- **The EXACT mechanism:** for the first-difference (persistence) law, Var(resid)=2 sigma^2 (1-rho1), so per-dim sigma-shrink = exactly **-0.5*log2(2(1-rho1))** — verified to RMS 0.006 bits (max 0.017, Pearson 0.999996) across all 36 cells. So "the flare's persistence-lawfulness IS its lag-1 autocorrelation," by identity; decimation drives rho1 0.996 -> 0.484, destroying the edge. A clean, exact, dial-protocol-grade linkage.
- **Strongest surviving critique (Opus, PARTIAL): LAW-RELATIVITY.** Persistence is a 1-step law by construction, so "coarsening kills its edge" is near-tautological. The adversary BUILT a coarse-law battery and showed the flare HAS coarse structure persistence cannot see: a window-mean slow-trend law keeps it compressible at every window to 720 min (1.085->1.006, never hits floor); lag-r persistence ticks back UP at long lag (0.890->0.926); the decimated flare beats its same-marginal shuffle at all rungs incl. hourly (1.07x). So the flare is structureless TO PERSISTENCE at coarse scale, not structureless. And toyB (a dominant 2-day sinusoid) stays compressible at coarse rungs under the SAME instrument — proving it would see a DOMINANT coarse law if present; tau~532 min => only ~19 independent samples in 7 days, so the 27-day rotation / 11-yr cycle are genuinely unsampled (0 cycles).

**Zoom vs hardness — the sharpened reading (kills "same dial seen twice"):** COUPLED, NOT THE SAME DIAL. For a fixed law the coupling is exact and TIGHTER than conjectured — rung sets rho at the law's lag, rho sets hardness via the -0.5*log2(2(1-rho)) identity (Spearman 1.000). But the GEARING is **law-indexed in both gain and SIGN**: under persistence the flare gets HARDER zooming out; under a window-mean law it stays lawful at every window; a dominant slow signal stays lawful at coarse scale. So zoom and hardness are **coupled dials geared THROUGH the law**, not one dial seen twice — a more precise and more interesting statement than the conjecture.

**Dead children (4):** naive-coarse=more-lawful (dead, direction reversed with error bars); "tracks AR(1) almost exactly" (dead as stated — lzma compression-saturation coincidence; flare is multi-timescale rho1=0.996, not single-exponential AR(1)); "at the floor by 10 min" (demoted — coder-dependent, lzma-specific); "the flare's lawfulness IS fine-scale memory" (dead as a GENERALIZATION; survives law-scoped as "the flare's persistence-EDGE is fine-scale memory").

**Owed / promoted to next sweeps:** longer GOES window (60-90 d for the 27-day rotation; archival multi-year for the 11-yr cycle); promote the adversary's coarse-law battery (window-mean/slow-trend law, lag-r persistence, same-marginal shuffle gap) to committed sweep instruments; the **lag-matched "zooming law"** (let the law's lag scale WITH the rung — the cleanest direct same-dial probe: if hardness goes flat when the law zooms with the frame, the residual scale-relativity was pure law-lag mismatch); the orbit as the lawful-at-all-scales anchor; seed sweep for the synthetic controls.

---
