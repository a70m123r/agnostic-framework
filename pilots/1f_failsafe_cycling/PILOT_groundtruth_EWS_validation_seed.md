# Ground-truth EWS validation pilot — SEED / DRAFT (validate the instrument before the social substrate)

> **STATUS: DRAFT SEED — NOT a locked pre-registration, NOT canon.** Authored 2026-06-04 (Claude Code)
> from the critical-transitions/EWS scout ([`SCOUT_critical_transitions.md`](SCOUT_critical_transitions.md),
> commit bbb6d9c) + Pav's steer "validate on ground truth first." For Cowork to refine, pre-specify
> fully, and **lock before any Cascade / PhysioNet data is examined.** This is a methods-benchmark
> (does metric A beat metric B on labelled data), simpler than the framework's full pre-reg apparatus.

---

## §0 Why this pilot, and why FIRST

The EWS scout corrected the programme's positioning (honest finding, §1 of the scout):
- The **symmetric two-pole** "over-order OR randomness = failure" claim is **prior art** — Goldberger et al. 2002 (PNAS) states it near-verbatim on the same DFA-α axis. **Drop the symmetry-novelty claim.**
- What is **genuinely under-occupied** (Tier 2): the **cross-field bridge** (EWS ↔ physiology loss-of-complexity, which don't cite each other) **+ the cycling-AMPLITUDE-over-rolling-window metric** (vs static α level) **+ the social-substrate application** (open — Braha 2024 deferred EWS to future work).

Before applying the cycling-amplitude metric to ambiguous **social** data (GDELT), validate it where **ground truth exists** and against the **established one-pole baseline**. If it can't beat one-pole CSD on labelled ecological/physiological data, the metric-level contribution collapses to the bridge alone — and we should know that before any GDELT re-pull. This is the same "validate the instrument first" discipline that the #150b synthetic gate embodied, now against real labelled data.

## §1 The narrowed claim under test

**Tier 2 candidate (the only metric-level novelty that survived the scout):** *Collapse of the temporal **cycling amplitude** of rolling-DFA-α (the oscillation between A⁺ and A⁻ dying over a rolling window) is an early-warning / health-discrimination signal that adds value **beyond** the established one-pole critical-slowing-down indicators (rising lag-1 autocorrelation, rising variance, rising α).*

Explicitly **not** claimed: that the symmetric two-pole picture is novel (it is Goldberger 2002).

## §2 Datasets (ground truth; from scout §2 — URLs there)

| dataset | role | ground truth |
|---|---|---|
| **Cascade — Peter Lake** | forced transition (treatment) | dated experimental regime shift |
| **Cascade — Paul Lake** | **negative control** | no transition (must NULL) |
| **PhysioNet nsr2db** | healthy | α ≈ 1 (broadband 1/f) |
| **PhysioNet chf2db** | over-correlated pole | heart failure (α high — the "squeeze" pole) |
| **PhysioNet Fantasia** | aging | loss of complexity |
| *(secondary)* Lake Veluwe (Wang 2012), 1929–2008 crashes (Diks 2019) | **one-pole-CSD-FAILS** differentiators | where amplitude could add value |

Cascade is the keystone: open CSV, EDI `knb-lter-ntl.355.6`, with a built-in negative control + a dated transition.

## §3 Methods compared (pre-specify, lock before data)

- **Baseline (one-pole CSD):** the `earlywarnings` toolbox indicators — rising lag-1 AR(1), rising variance, rising DFA-α — Kendall-τ trend, on the standard detrended series.
- **Candidate (this programme):** **cycling-amplitude collapse** — rolling-DFA-α τ(t), amplitude A_cyc = inter-decile range (P90−P10) of τ over the rolling window; the validated #150b H1b metric. Decline in A_cyc = warning, **direction-agnostic**.
- **Recovery-rate (folds in the #150b H2b fix):** the scout found the gap-closer — **Delecroix et al. 2024 PNAS "resilience in bursts"** (short-burst estimator + Theil-Sen/sieve-bootstrap, beats the moving window — exactly our 365-day failure) and the analytic **λ = −log(AR1)/dt**. Use this as the recovery-rate channel instead of the 365-day half-life that failed synthetic validation.

## §4 Pre-registered hypotheses + falsifier

- **H-val (primary):** A_cyc cycling-amplitude collapse **beats the best one-pole indicator** on (a) **lead-time** to the dated transition and (b) **AUC** (warning vs control), across the Cascade Peter-vs-Paul pair; **and** distinguishes the PhysioNet healthy/CHF/aging labels.
- **Negative control:** must **NULL on Paul Lake** (no false warning) — the must-NULL, mirroring the synthetic gen-(iv) discipline.
- **FALSIFIER (locked):** if A_cyc does **not** beat the best one-pole indicator on lead-time + AUC (or fires on the Paul control), the **metric-level claim (cycling-amplitude) is rejected** and the programme's contribution **narrows to the cross-field bridge alone** (no new metric). Report cleanly per cont 27 §3 — do not retro-fit.

## §5 Confounds (pre-named)

- **Volume / sampling-rate** — the #150 killer, already validated controllable on synthetic data (Poisson-thin + DFA-α + within-series); in their field this is the **Boers–AMOC λ critique** (credibility asset, not a novel risk).
- Dataset-specific: lake sampling cadence/gaps; physiological artifacts (ectopy, motion) — use the standard PhysioNet cleaning.
- Researcher-DOF in window/stride — pre-register + sensitivity sweep (as #150b §3.3).

## §6 What the result feeds

- **Validates →** the cycling-amplitude metric earns the **GDELT-cycling social application** (the open seam; the Braha-2024-npj-Complexity successor) and supports **Bar B** of the cycling candidate; the cycling pre-reg's H2b is repaired with the Delecroix recovery-rate.
- **Fails →** narrow the programme's claim to the bridge; drop the metric novelty; do **not** demote cont 26 §3.

## §7 For Cowork (the decisions to lock)

1. **Narrow the public claim** to bridge + rolling-amplitude metric + social application; **explicitly drop symmetry-novelty** (Goldberger 2002). This is the canon-level positioning decision the scout surfaced.
2. Lock §3 method parameters, §4 lead-time/AUC definitions + the Paul-control must-NULL threshold, **before** touching Cascade/PhysioNet.
3. Decide ordering vs the GDELT cycling pilot (#150b): this validation should arguably **precede** any GDELT re-pull.
4. Outreach (scout §5): Scheffer/Dakos (EWS), Goldberger/PhysioNet lineage, Boers (λ/coupling), Braha (social event-streams) — gated as usual.

## §8 Cross-references

- Scout + all source URLs: [`SCOUT_critical_transitions.md`](SCOUT_critical_transitions.md) (Goldberger 2002 PNAS; Delecroix 2024 PNAS; Braha 2024 npj Complexity; Cascade EDI `knb-lter-ntl.355.6`; PhysioNet; `earlywarnings`; Diks 2019; Wang 2012).
- Cycling pre-registration (the social pilot this validates the instrument for): [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md).
- Synthetic gate (instrument validated on synthetic data; this is the real-data analogue): [`synthetic_validation/`](synthetic_validation/).
- Discipline: `continuations/27.md` §2–§3 (falsifiability, narrow-before-demote).

*Provenance: seed authored 2026-06-04 (Claude Code) from the EWS scout + Pav's "validate on ground truth first" steer. Not locked, not canon. For Cowork to formalize + lock before data.*
