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

## §9 Data acquisition path — BigQuery (2026-06-03, result-commit)

**Discovered via:** result-commit ingest. The machine initially had no cloud CLIs/credentials, so a streaming 15-min-slice downloader (`gdelt_ingest.py`) was built and run. Mid-run, BigQuery auth was set up (browser OAuth via `pydata-google-auth`, sandbox/free tier) and the canonical path (candidate §5.1) was used instead.

**Effect:** none on the locked aggregation — both paths compute GROUP BY SQLDATE on `ActionGeo_CountryCode`. BigQuery is strictly better here: it holds the complete archive (all events ever ADDED, including late-reported), so per-country coverage is higher (all countries ≥ 99.6% of 3970 days) than a partial slice sweep would reach. Query scanned 21.39 GB (free tier, $0), returned 47,610 country-day rows. Not a pre-registration change.

---

## §10 Source-volume → β spectral-floor confound (CRITICAL — discovered in real data)

**Discovered via:** running the locked pipeline on real GDELT data, then correlating per-country β with event volume.

**Issue:** on the PRIMARY signal (category_entropy), Welch β is almost perfectly explained by per-country event volume — **Pearson r(log₁₀ total events, β) = +0.916, Spearman = +0.909.** The four lowest-volume countries (CHL 2.4M, PRK 3.3M, NLD 3.3M, VEN 6.0M) hold four of the five lowest β; highest-volume USA (204M) has the highest β.

**Mechanism:** daily category-entropy estimated from few events is noisy; that sampling noise is ~white → adds a flat high-frequency floor to the PSD → **flattens (lowers) the fitted β for low-volume countries.** Pre-registered z-score normalization (§5.2.1, candidate §5.2) removes amplitude scale but NOT this frequency-domain floor.

**Why it matters for H1:** the small anti-H1 Welch-β contrast (mean Δβ = +0.084) is driven by low-β low-volume countries (NLD, CHL on the pluralistic side of the two largest anti-H1 pairs). The contrast tracks media-volume, not political system. **This is the reason the result-commit reports a "confounded null" rather than a clean falsifier** (see `results/discussion.md` §3–§4).

**Status: NOT mitigated by the locked pipeline.** Surfaced to Cowork. Candidate v2 fixes (pre-register before re-running): Poisson-thin all countries to a common daily rate; volume-matched pairs; use DFA-α (volume-robust, see §13) as primary estimator; or explicitly model the white-noise floor. This supersedes the §4 assumption that z-scoring handles the source-volume confound — it handles amplitude, not the spectral floor.

---

## §11 Bootstrap-CI estimator substitution

**Issue:** pre-registration §5.4.1 specified `powerlaw.Fit(...).power_law.confidence_interval()` parametric bootstrap. The `powerlaw` package is unavailable in this numpy-only environment.

**Substitution:** moving-block bootstrap (block = 64, 1000 resamples) 95% CI on Welch β. Descriptive only; the H1 inference is the locked permutation test, unchanged. The resulting CIs are wide and overlapping across auth/plur (e.g. CHN entropy [0.94,1.61], TUR [0.62,1.72]), consistent with the §10 instability of per-country β. Logged; surfaced to Cowork for whether to re-run with `powerlaw` in a richer env.

---

## §12 IAAFT surrogate is not a clean null for β (non-degenerate)

**Issue:** pre-registration §5.4.2 treats the IAAFT surrogate β distribution as "the null." Expectation was that IAAFT (preserves the global power spectrum) would give surrogate β ≈ observed β — a degenerate null. **In real data this was false:** observed β sits systematically BELOW surrogate β, with |z| scaling by sparsity (USA z=−1.8, CHN −7.3, PRK −14.2, CHL −13.9). Cause: β is fit on a sub-band [1/365,1/10] and the signals are strongly non-Gaussian/zero-inflated; IAAFT's amplitude-matching step shifts the sub-band slope.

**Effect:** IAAFT is reported as a diagnostic (it corroborates §10 — low-volume β is most distribution-dependent), NOT as the H1 null. The locked permutation test remains the inference. Surfaced to Cowork: future pilots should pick a discriminating statistic for IAAFT (β is not one) or drop the IAAFT layer.

---

## §13 DFA-α vs Welch-β divergence

**Observed:** on the primary signal, DFA-α is ≈ flat across all 12 countries (0.827–0.901, spread 0.074) while Welch-β spans 0.348–1.083 (spread 0.735). DFA (integrates before measuring) is far less sensitive to the §10 white-noise floor; it shows essentially NO cross-country difference — consistent with a null and with the floor contaminating the Welch sub-band fit. Per README §4 / candidate §5.3, Welch β is the pre-registered primary estimator, so the verdict is reported on Welch β; but the DFA-α null is the more volume-robust reading and is flagged accordingly (`results/discussion.md` §3, §8.4).

---

## §14 Temporal-gap handling

**Issue:** pre-registration §5.2.4 prescribes interpolating <2-day gaps and windowing around >2-day gaps. Real data has very few missing (zero-event) days: PRK 5, NLD 5, VEN 5, CHL 13, DEU/TUR 1, all others 0 (< 0.4%).

**Done:** all missing days linear-interpolated (edge-clamped); counts logged per (country, signal). Segment-windowing for the rare longer gaps was NOT implemented because (a) gaps are negligible in count and (b) windowing a 3970-point series breaks the 512-day Welch segmentation. Deviation logged; immaterial to the verdict given gap counts.

---

## Audit trail

- **2026-06-02:** §1 amendment locked before any GDELT data examined. All other confounds (§2–§8) inherited from candidate-doc §7 at pre-registration time.
- **2026-06-03 (result-commit):** §9–§14 appended after running the locked pipeline on real GDELT v2 data. §10 (source-volume spectral-floor confound, r=0.92) is the load-bearing finding and the reason H1 is reported as a confounded null. Original pre-registration text never modified; locked H1 permutation test applied exactly as specified.
- Future amendments will be appended with date and reason. Original pre-registration text never modified after lock.
