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
