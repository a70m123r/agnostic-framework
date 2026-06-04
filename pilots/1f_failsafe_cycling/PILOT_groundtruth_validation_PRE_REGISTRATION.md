# Pilot 2 — Ground-truth EWS validation — PRE-REGISTRATION (LOCKED)

> **STATUS: LOCKED 2026-06-04, BEFORE any Cascade or PhysioNet data VALUES were examined.**
> Accessibility was verified (EDI package `knb-lter-ntl.355.6` resolves with 2 data entities;
> PhysioNet `nsr2db`/`chf2db`/`fantasia` landing pages return 200) — **existence/metadata only,
> no time-series values inspected.** The falsifier in §4 is frozen as of this commit. Any issue
> discovered after data download goes in a NEW `confounds_groundtruth.md` (dated), never by editing
> §3/§4 retroactively (cont 27 §2 / Pilot 1 Phase D discipline). Locks the seed
> [`PILOT_groundtruth_EWS_validation_seed.md`](PILOT_groundtruth_EWS_validation_seed.md) per the
> three Cowork decisions in HANDOFF.md (2026-06-04 late).

---

## §1 The narrowed claim under test (per Cowork Decision #1)

**Tier-2 candidate (the only metric-level novelty surviving the EWS scout):** *Collapse of the temporal **cycling amplitude** of rolling-DFA-α — `A_cyc` — adds early-warning / state-discrimination power **beyond** the established one-pole critical-slowing-down (CSD) indicators (rising lag-1 autocorrelation, rising variance, rising α level), on datasets with KNOWN ground truth.*

**Explicitly NOT claimed (dropped per Reading 06 §10.3 third amendment):** that the symmetric two-pole picture is novel — Goldberger et al. 2002 PNAS owns it on the same DFA-α axis. cont 26 §3 substrate-level canon is untouched. This pilot tests **only** whether the *rolling-amplitude metric* earns its keep over the one-pole baseline. If it does not, the programme's contribution narrows to the cross-field **bridge alone** (no new metric, and Pilot 1's GDELT run is permanently deferred).

## §2 Datasets (ground truth; accessibility pre-verified, values not examined)

| dataset | role | ground truth | source |
|---|---|---|---|
| **Cascade — Peter Lake** | manipulated (transition) | documented experimental destabilization (Carpenter et al. 2011 *Science*) | EDI `knb-lter-ntl.355.6` |
| **Cascade — Paul Lake** | **reference / negative control** | no manipulation → **must NULL** | same package |
| PhysioNet `nsr2db` | healthy | normal sinus rhythm, α ≈ 1 | physionet.org/content/nsr2db |
| PhysioNet `chf2db` | over-correlated pole | congestive heart failure (α high) | physionet.org/content/chf2db |
| PhysioNet `fantasia` | aging | loss of complexity (young vs elderly) | physionet.org/content/fantasia |
| *(tertiary, only if Cascade+PhysioNet pass)* Lake Veluwe (Wang 2012), `earlywarnings` Hopf sim, stock-crash indices (Diks 2019) | one-pole-CSD-FAILS differentiators | where amplitude could add value | per scout §2 |

**Cascade is the decisive primary.** PhysioNet is secondary confirmation (and the "does amplitude add over *static* α" test). Tertiary runs only if the first two pass.

## §3 Methods — LOCKED parameters

**Pre-processing (identical for the candidate and all baselines — a fair comparison):**
1. **Cadence rule (avoids value-peeking):** aggregate each raw series to **daily medians** (Cascade high-frequency sonde) / use the native RR-interval sequence (PhysioNet); the exact native cadence is read from dataset METADATA, not values.
2. Restrict Cascade to the **ice-free field season(s) up to and including the documented Peter manipulation year (2011)**; Paul over the identical calendar span. Primary texture variable: **chlorophyll-a**; if absent in the package, **phycocyanin/BGA** (pre-registered fallback order).
3. Per-series **z-score**; linear-detrend; gaps >2 samples → windowed (not interpolated across), per Pilot 1 §5.2 convention.

**Texture trajectory:** `τ(t) = rolling DFA-α`, reusing the verified `pilots/1f_failsafe/pilot.py` `dfa()` (the `fast_dfa` vectorization proven identical, max |Δα|=4.4e-16, may be used in hot loops). **Rolling window = 50% of the usable per-series length** (the `earlywarnings` toolbox default — same convention as the baseline, so candidate and baseline share the window); **stride = 1 daily sample**.

**Candidate metric:** `A_cyc` = **inter-decile range (P90 − P10) of τ(t)** over the analysis window (the cycling amplitude; the validated Pilot 1 H1b metric). **Decline in A_cyc** toward the transition = warning. Direction-agnostic.

**One-pole CSD baseline (the comparator), in the identical rolling framework:** (i) lag-1 **AR(1)**, (ii) **variance**, (iii) **rising DFA-α level** — each summarized by **Kendall-τ trend** toward the transition (the field-standard EWS statistic). The "best one-pole indicator" = whichever of (i)–(iii) scores highest on the metric being compared.

**Diagnostic-only channels (NOT in the §4 falsifier; per Cowork Decision #2):** Delecroix 2024 burst recovery-rate `λ = −log(AR1)/dt`; reported for completeness, cannot change the verdict.

## §4 Metrics + FALSIFIER (LOCKED)

**Metrics (computed identically for `A_cyc` and each one-pole indicator):**
- **AUC** — ROC area discriminating manipulated (Peter, transition-approaching windows) vs reference (Paul, same-span windows). Range [0,1]; 0.5 = chance.
- **Lead-time** — days before the documented Peter destabilization onset at which the indicator's trailing Kendall-τ trend first reaches p < 0.05 (or crosses a pre-shift +2σ band). Larger = earlier warning.

**PRIMARY GATE (Cascade — decisive):** the cycling-amplitude metric PASSES iff **all three**:
- **(a)** `AUC(A_cyc) ≥ max_i AUC(one-pole_i) + 0.05` — strictly better discrimination by a ≥ 0.05 margin;
- **(b)** `lead-time(A_cyc) ≥ max_i lead-time(one-pole_i)` — warns at least as early as the best one-pole indicator;
- **(c)** **Paul-control must-NULL:** `A_cyc` shows **no** significant decline on Paul (Kendall-τ p > 0.05, no +2σ crossing).

**FALSIFIER (frozen):** if **(a) OR (b) fails, OR (c) fires** on Paul, the **metric-level claim is REJECTED**. The programme's contribution narrows to the cross-field **bridge alone**; **Pilot 1 Phase E (the GDELT real-data run) is permanently deferred.** Report per cont 27 §3 — no retro-fitting, no moving the margin.

**SECONDARY (PhysioNet):** (sanity) static α separates healthy (`nsr2db`, α≈1) / over-correlated (`chf2db`, α high) / aging (`fantasia`) — expected to hold (it is Goldberger's own result; proves only the known). (test) does a **rolling-amplitude** feature add discrimination **OVER static α** (AUC_rolling ≥ AUC_static-α + 0.05)? If not, the metric novelty fails to generalize beyond ecology and the framing must say so.

**VERDICT BANDS:** **PASS** = Cascade primary gate met (decisive for Pilot 1 unlock) AND PhysioNet adds-over-static-α. **MIXED** = Cascade passes, PhysioNet does not (metric works on ecology, not physiology — report the boundary). **FAIL** = Cascade primary gate not met → bridge-only, Pilot 1 Phase E permanently deferred.

## §5 Confounds (pre-named)

1. **Volume / sampling-rate floor** — the #150 killer; in this field it is the **Boers–AMOC λ critique**. Already validated controllable on synthetic data (Poisson-thin + DFA-α + within-series). Lake sonde + RR series are not volume-confounded the way GDELT is, but the **daily-median aggregation rule is fixed in §3** so it is not a researcher DOF.
2. **Season-length / short-series** — DFA-α on a 50%-window of a single short lake season may be unstable; mitigated by pre-committing the window rule and reporting the per-window DFA fit quality; flagged as a limitation, logged in `confounds_groundtruth.md` if it bites.
3. **Shift-date definition** — the documented Peter onset is taken from Carpenter et al. 2011 / the EDI metadata (published, not derived from the texture values). If multiple candidate dates exist, the **earliest documented destabilization onset** is used (pre-committed).
4. **Multiple comparisons** — exactly ONE primary gate (Cascade, §4). PhysioNet and tertiary are secondary/diagnostic and cannot upgrade a Cascade FAIL.
5. **Researcher DOF** — window, stride, aggregation, variable choice, margins, and the shift-date rule are ALL locked in §3/§4 above, before data.

## §6 What the result feeds (gate logic)

- **PASS →** the rolling-amplitude metric earns **Pilot 1 Phase E** (the GDELT cycling real-data run, using the revised pre-reg per Cowork Decision #2) + **Bar B** of the cycling candidate; Cowork ships Reading 06 §10.3 *fourth* amendment promoting bridge+metric to Tier-2-confirmed.
- **FAIL →** contribution narrows to the **bridge alone**; cycling-amplitude metric demoted per cont 27 §3 (NOT cont 26 §3 canon); Pilot 1 Phase E permanently deferred; outreach becomes a "we synthesize your two literatures" pitch, not "we extend with a new metric."

## §7 Protocol (run order)
1. Lock this pre-registration; commit BEFORE any data download (this commit). ✓
2. Download Cascade EDI `knb-lter-ntl.355.6` (Peter + Paul); compute τ(t), A_cyc, the 3 one-pole baselines, AUC + lead-time; evaluate the §4 primary gate.
3. Download PhysioNet `nsr2db`/`chf2db`/`fantasia`; static-α sanity + the adds-over-static-α test.
4. (Only if both pass) tertiary differentiators.
5. Result-commit: `results_groundtruth/discussion.md` + verdict per §4 + plots + methods.

## §8 Cross-references
- Seed + scout (sources/URLs): [`PILOT_groundtruth_EWS_validation_seed.md`](PILOT_groundtruth_EWS_validation_seed.md), [`SCOUT_critical_transitions.md`](SCOUT_critical_transitions.md).
- Cycling pilot this validates the instrument for: [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md); synthetic gate: [`synthetic_validation/`](synthetic_validation/).
- Canon: Reading 06 §10.3 (third amendment, 2026-06-04); cont 30 §3 (amendment, 2026-06-04); cont 27 §2–§3.
- Key external: Carpenter et al. 2011 *Science* (Cascade); Goldberger et al. 2002 *PNAS*; Dakos `earlywarnings`; Delecroix et al. 2024 *PNAS*.

## §11 Lock attestation (cont 27 §2 discipline)

I locked §3 (method parameters) and §4 (metrics + falsifier) on **2026-06-04 BEFORE examining any Cascade or PhysioNet data values.** Only dataset *existence/metadata* was checked (EDI package + 2 entity IDs; PhysioNet HTTP 200) — no time-series values were inspected. All parameters are pinned in physical-time / convention terms (daily-median cadence; 50% `earlywarnings` window; δ = 0.05 AUC margin; earliest-documented-onset shift date) so that exact sample counts follow mechanically from metadata, not from values. The empirical A_cyc-vs-one-pole comparison is genuinely fresh: I wrote the seed and Cowork locked the framework decisions, but neither I nor any prior step has seen how A_cyc behaves on this data. Provenance: locked by Claude Code per HANDOFF 2026-06-04-late Cowork Decision #3.
