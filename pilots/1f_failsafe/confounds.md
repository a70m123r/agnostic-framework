# Confounds log — Pilot #150

Per `candidates/1f_l0_failsafe_signature.md` §7. Updated as confounds are discovered or mitigated.

---

## §1 Pre-registration amendment 2026-06-02 — N=6 paired comparisons required

**Discovered via:** Running `python3 pilot.py --mode demo` against the locked pre-registration protocol with N=3 pairs.

**Issue:** The paired permutation test with N=3 pairs has only 2³ = 8 possible label-flip configurations. The minimum achievable p-value is 1/8 = 0.125. **N=3 cannot reach the pre-registered p < 0.05 threshold by construction**, regardless of effect size.

**Demo evidence:** synthetic auth (β=0.3) vs plur (β=1.0) signals — ground truth Δβ ≈ -0.7, Cohen's d = -1.79 (very large effect) — permutation test p = 0.128 > 0.05.

**Amendment:** N is raised from 3 to 6 paired comparisons before the GDELT analysis runs. The six pairs (all locked at 2026-06-02 before any GDELT data examined):

| # | Authoritarian | Open pluralistic |
|---|---|---|
| 1 | China (CHN) | United States (USA) |
| 2 | Russia (RUS) | United Kingdom (GBR) |
| 3 | North Korea (PRK) | Germany (DEU) |
| 4 | Iran (IRN) | France (FRA) |
| 5 | Turkey (TUR) | Netherlands (NLD) |
| 6 | Venezuela (VEN) | Chile (CHL) |

**Effect on power:** with N=6, minimum p via paired permutation = 1/64 ≈ 0.016. p < 0.05 becomes achievable at Cohen's d ≥ 0.5 effect size.

**Alignment with promotion bars:** the amendment aligns with `candidates/1f_l0_failsafe_signature.md` §8 Bar B (Tier 2 → Tier 1 promotion required N ≥ 6 paired comparisons across at least 3 substrate types). Bar A (Tier 2 conditional → Tier 2 algorithmically-demonstrated) is now satisfied by N=6 GDELT comparison alone if H1 lands.

**Discipline note per cont 27 §2:** the original N=3 was a methodological pre-test; the substantive analysis is N=6. The amendment is logged here at 2026-06-02 before any data examined, preserving the pre-registration discipline. This is the framework's three-tier procedure working as designed — a methodological issue caught BEFORE the empirical analysis runs is exactly the discipline cycle the framework's audit cadence rewards.

**Alternative considered and rejected:** Bootstrap-CI-overlap test per pair (multiplicity-corrected). Rejected because it abandons the paired structure that makes the cross-country comparison meaningful; the framework's claim is about *paired* authoritarian-vs-pluralistic difference, not unpaired per-country β estimation.

---

## §2 Linguistic-substrate baseline (Zipf-and-LRC confound)

**Status:** Mitigated by signal choice. Pre-registered signals are event-count, mean-tone, event-category-entropy — all aggregate / categorical signals, not raw word frequency.

**Outstanding risk:** GDELT's NLP pipeline may propagate Zipf-like structure into its tone aggregates even though the final aggregate is not a word-frequency signal. Mitigation deferred to v2 of pilot — within-language baseline (Russian state vs Russian émigré press).

---

## §3 GDELT pipeline drift

**Status:** Confined to GDELT v2 only (2015+). Pre-registration §5.5 step 2.

**Outstanding risk:** Minor GDELT v2.0 → v2.1 schema changes (logged in GDELT update history). Pilot code should snapshot data download date and log GDELT version explicitly in results.

---

## §4 Source-volume confound

**Status:** Mitigated by per-country z-score normalization before DFA. Pre-registration §5.2 step 1.

**Outstanding risk:** Z-score normalization assumes stationarity within country. If country has regime change mid-window (e.g., Russia 2022 invasion), normalization smears across regime boundaries. Mitigation deferred to v2 — within-country regime-window analysis (H4 secondary hypothesis).

---

## §5 Publication-cadence asymmetry

**Status:** Mitigated by construction. All six country pairs aggregated to daily granularity. Pre-registration §5.5 step 3.

---

## §6 Tone-pipeline confound

**Status:** Mitigated by demoting tone signal to secondary. Primary signals are event-count and event-category-entropy (language-agnostic aggregates). Tone results reported with explicit caveat.

---

## §7 Scale-window selection

**Status:** Mitigated by pre-registered scale window f ∈ [1/365, 1/10] cycles-per-day. Multi-scale fluctuation plots required in result commit. Pre-registration §5.3 step 2.

---

## §8 Unaddressed confounds (honest gaps)

Per `candidates/1f_l0_failsafe_signature.md` §7:

1. **Regime-intensity drift within country** — Russian state media 2015 ≠ Russian state media 2024. H4 (within-country temporal shifts) addresses this exploratorily but not pre-registered to significance threshold.

2. **Selection effects in GDELT source set** — GDELT indexes a curated set of media sources, weighted toward English-language outlets. The "Chinese coverage" available in GDELT is not a representative sample of all Chinese media. Could bias signal in unknown directions.

3. **N=6 is still small** — six paired comparisons is the minimum for the pre-registered statistical test, not sufficient for strong cross-domain claims. Bar C promotion (Tier 1 epistemological canon) requires external replication.

---

## Audit trail

- **2026-06-02:** §1 amendment locked before any GDELT data examined. All other confounds inherited from candidate-doc §7 at pre-registration time.
- Future amendments will be appended with date and reason. Original pre-registration text never modified after lock.
