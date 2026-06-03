# Candidate operationalization — 1/f as L0-failsafe signature at social substrate (Reading 06 §10.3, Tier 2 conditional)

**Tier:** Tier 2 conditional per [cont 27 §2](../continuations/27.md). Conditional on the empirical-comparison pilot landing the hypothesized spectral-exponent contrast at significance. Operationalization document task #150 completes 2026-06-02; empirical work product (first pilot commit) is the next deliverable per task #167 discipline hard-stop.
**Surfaced:** Reading 06 §10.3 (2026-05-28). Methodologically scoped by Reading 07 §7.2 (BES backward goal-tree decomposition); architecturally NOT applicable per Reading 08 §6 (1/f is measurement-design, not architecture). Operationalized 2026-06-02 per audit v06 §10 substantive-research-displacement-by-infrastructure discipline concern.
**Trigger:** Audit v06 §10 + Reading 08 §9 jointly endorsed the hard-stop on further infrastructure work until task #150 or #151 has a first commit with tangible empirical work product. Pav's call: "lets do 150 and then 151." Task #150 operationalization is the first substantive empirical move the framework has shipped in 6+ weeks.

---

## §1 The claim — restated precisely (per Reading 06 §10.3)

**Tier 2 conditional hypothesis:** 1/f scale-invariance + burstiness IS the SIGNATURE of healthy substrate-level failsafe operation at the social substrate. Concretely:

- **The structural claim** (cont 26 §3 + Reading 06 §10.3): L0 substrate carries evolved failsafes that *prevent clean harmonic resonance from forming*, because harmonic resonance would be brittle. The signature of healthy failsafe operation is therefore **broadband 1/f spectra with characteristic relaxation timescales + burstiness**, not discrete harmonic peaks.
- **The contrast claim** (Reading 06 §10.3, derived): Systems where substrate-level failsafes are *weakened, captured, or suppressed* (cult / authoritarian / locked-in systems) should show **MORE discrete spectral structure + LESS broadband 1/f** — i.e., either β far from 1.0 (white-noise-controlled, β ≈ 0) OR β >> 1 (over-correlated, locked-in) OR discrete harmonic peaks suggesting forced periodicity.
- **The framework's interest:** if this holds, the spectral exponent β of socio-political time series is a **measurable proxy for L0-failsafe-health at social substrate** — operationalizing what was previously a structural claim into a measurement protocol.

**Why this matters for the framework's larger canon:** [cont 26 §3](../continuations/26.md) (L0 evolved failsafes) is currently Tier 1 epistemological canon stated qualitatively. If the 1/f signature lands at the social substrate, cont 26 §3 gains its first quantitative empirical anchor. If it fails to land cleanly, the failsafe-health claim either narrows or is forced into demotion per [cont 27 §3](../continuations/27.md) pruning procedure.

---

## §2 Why this is now operationalizable (methodological maturity check)

Three components had to mature before this pilot could break ground:

**§2.1 Open paired-corpora data with adequate temporal depth.** Without ≥1000 daily points per corpus, DFA estimators become unreliable. The opus scout (task #150 scout report, 2026-06-02) identified [GDELT v2](https://www.gdeltproject.org/data.html) as the candidate that clears the gate: free, 2015–present (~4000+ daily points per country), country-day aggregates of tone + event-counts + event-category-entropy, no API licensing friction.

**§2.2 Mature 1/f spectral analysis tools in Python.** The scout confirmed: `nolds 0.6.2` (DFA, Hurst), `fathon 1.3.3` (MFDFA + DCCA), `MFDFA 0.4.1` (pure-Python multifractal), `powerlaw 1.5` (Clauset-Shalizi-Newman MLE + KS goodness-of-fit), `colorednoise 2.2.0` (surrogate generation), `antropy 0.1.9` (spectral entropy + sample entropy), `scipy.signal.welch` (PSD). All maintained, all citable, all installable via pip.

**§2.3 A defensible statistical test stack.** Three-layer per scout: (a) Welch PSD → log-log slope fit for β with parametric bootstrap CI per Clauset/Shalizi/Newman 2009 (sidesteps heavy-tail bootstrap pathology); (b) IAAFT surrogate ensemble (preserves linear autocorrelation, destroys nonlinear structure) for null distribution; (c) permutation test on Δβ across matched country-pairs with Cohen's d effect-size measure.

All three layers mature as of 2026-06-02. The framework has cleared the methodological gate.

---

## §3 The chosen pilot dataset — GDELT v2 country-day signals, 2015–2026

**Choice:** GDELT v2 event database, six countries paired authoritarian-vs-pluralistic, three signals per country, ~11-year window, daily granularity.

**The six countries:**

| Authoritarian | Open pluralistic |
|---|---|
| China (CHN) | United States (USA) |
| Russia (RUS) | United Kingdom (GBR) |
| North Korea (PRK) | Germany (DEU) |

**The three signals per country (extracted from GDELT v2):**

1. **Event-count time series:** daily count of all GDELT events with source country code = X. This measures the rate-of-event-coverage in that country's media ecosystem.
2. **Average tone time series:** daily mean of GDELT's `AvgTone` field across all events from country X. (Confine to events where source language is the country's primary language to avoid cross-language tone-pipeline drift per Reading 08 §10 confound discipline.)
3. **Event-category entropy time series:** daily Shannon entropy of the distribution over GDELT's `EventRootCode` (top-level event categories) for events from country X. This measures topic-diversity at daily resolution.

**Three signals × six countries = 18 daily time series**. Each ~4,000 points. Well above the ~1000-point DFA reliability threshold.

**Why GDELT was chosen over alternatives** (per scout report §6):

- Free, public, no API key, no institutional affiliation required.
- ~11 years × 365 days = ~4000 daily points per signal. 365× the DFA reliability minimum.
- Same extraction pipeline applied symmetrically to all six countries → strongest possible "comparable signal across both halves of the pair" property.
- Computational anchor: GDELT has been used in 1000+ papers; DFA-on-text has Altmann/Cristadoro/Esposti 2012 PNAS baseline.
- Sidesteps the Zipf confound on its face — the signals are tone/event/entropy aggregates, not raw word-frequency.

**Why not the other candidates** (per scout report §1):

- People's Daily + Pravda paired with NYT + Times Digital Archive: paywalled (~$5k+/yr institutional licensing). Would burn weeks securing access.
- Wikipedia edit cadence (Plan B): cleaner data access than GDELT but weaker mapping to "political substrate" claim because Wikipedia governance is platform-mediated, not state-mediated.
- Watchtower vs Christian Century: cleanest "cult corpus" mapping but mainstream-religious comparator is the weak link with no equally clean free archive.
- Stock-market regimes: financial-substrate test, not social-substrate test; drift risk away from the framework's discourse-substrate claim.

---

## §4 Pre-registered hypothesis — stated BEFORE data examined (cont 27 §2 Tier 1 promotion-bar discipline)

Per cont 27 §2 three-tier procedure, this hypothesis is locked at 2026-06-02 before the pilot runs the analysis. Subsequent modifications must be explicitly logged with date and reason.

**§4.1 Primary hypothesis (H1):**

For each pair (authoritarian country, pluralistic country) in the three matched pairs, the spectral exponent β estimated via DFA on the **event-category-entropy signal** will satisfy:

**β_authoritarian < β_pluralistic − 0.10**

(Authoritarian systems show significantly less broadband 1/f scaling — meaning either flatter spectra closer to white noise OR clear discrete harmonic peaks — than pluralistic systems on the same signal type, same time window.)

**§4.2 Effect-size threshold:** Cohen's d ≥ 0.5 (medium effect) across the three paired comparisons. Smaller effects are inconclusive at this sample size.

**§4.3 Significance threshold:** permutation test on Δβ across the three pairs, p < 0.05 vs IAAFT surrogate null. Pre-registered to a one-sided test in the direction of H1.

**§4.4 Falsifier (what would refute H1 cleanly):**

If across the three paired comparisons, **β_authoritarian − β_pluralistic > 0** with effect-size Cohen's d ≥ 0.5, **the framework's claim is refuted as stated**. Cont 26 §3 + Reading 06 §10.3 would need to be amended: either the authoritarian/pluralistic axis doesn't map to L0-failsafe-health, OR the spectral signature direction is opposite the framework's prediction.

If across the three paired comparisons, |β_authoritarian − β_pluralistic| < 0.05 (null effect), the claim is *not refuted but not confirmed*. The framework holds at Tier 2 conditional pending stronger signal sources or larger sample.

**§4.5 Secondary hypotheses (exploratory, not pre-registered to significance threshold):**

- H2: same direction holds for event-count time series (additional signal, additional evidence).
- H3: same direction holds for tone time series (with cross-language tone-pipeline caveat).
- H4: spectral exponent β shifts measurably during known political-stress windows within each country (e.g., 2022-02-24 invasion of Ukraine for RUS; 2019-08 Hong Kong protests for CHN; 2020-2022 COVID for all six).

H4 is the *intra-country temporal-shift* version of H1 and provides within-country control for between-country confounds. If H4 lands and H1 does not, the framework should consider whether the 1/f signature is responding to political-event stress rather than to structural political-system difference.

---

## §5 Protocol — step-by-step, code-level

This is the protocol the pilot code will implement. Locked at 2026-06-02 before data examined.

**§5.1 Data ingest:**

1. Download GDELT v2 event database via BigQuery `gdelt-bq:gdeltv2.events` OR direct CSV from AWS Open Data registry, filtered to `MonthYear >= 201501 AND MonthYear < 202601`.
2. For each country code in {CHN, RUS, PRK, USA, GBR, DEU}, aggregate by `SQLDATE` (day) to compute: `event_count`, `mean(AvgTone)`, `entropy(EventRootCode)`.
3. Store as three CSVs per country (event_count.csv, tone.csv, entropy.csv).

**§5.2 Pre-processing:**

1. **Z-score normalize each signal within country** to remove source-volume confound (high-volume countries have lower-variance daily counts; normalization removes scale bias).
2. **Linear-detrend** each signal (DFA is detrended already but pre-detrending sharpens the fit).
3. **Verify stationarity** via Augmented Dickey-Fuller test. Log result; do not gate on it — DFA is robust to mild non-stationarity by design.
4. **Verify temporal continuity:** any gap >7 days flagged; interpolate gaps <2 days linearly; window around gaps >2 days.

**§5.3 Spectral analysis:**

For each (country, signal) pair (18 total):

1. **Welch PSD estimate** via `scipy.signal.welch(signal, fs=1.0, nperseg=512, noverlap=256, detrend='linear')`.
2. **Log-log slope fit** for β: regress `log(PSD)` on `log(f)` in the scale-window f ∈ [1/365, 1/10] cycles-per-day (sub-annual through sub-fortnightly — the relevant social-substrate timescale band per Reading 06 §3).
3. **DFA estimate** of β-equivalent (α scaling exponent) via `nolds.dfa(signal, nvals=numpy.logspace(1, 2.5, 20).astype(int))`. Report both DFA-α and Welch-β; they should agree to within 0.1 in the fit window.
4. **MFDFA via `fathon` (optional Tier 2 promotion step):** estimate multifractality spectrum h(q) for q ∈ [-5, 5]. If multifractality differs systematically between authoritarian and pluralistic (h(q) range wider in pluralistic), that's secondary evidence.

**§5.4 Statistical testing:**

For each paired comparison (CHN-USA, RUS-GBR, PRK-DEU) × each signal type (event_count, tone, entropy):

1. **Bootstrap CI on β** via `powerlaw.Fit(signal_PSD).power_law.confidence_interval()` with parametric bootstrap (1000 resamples) per Clauset/Shalizi/Newman 2009 to avoid heavy-tailed-bootstrap pathology.
2. **IAAFT surrogate null:** generate 200 IAAFT surrogates of each signal via `colorednoise` or custom IAAFT (preserves linear autocorrelation, destroys nonlinear structure). Recompute β on each surrogate. The surrogate β distribution is the null.
3. **Permutation test on Δβ:** for each paired comparison, compute Δβ_observed = β_authoritarian − β_pluralistic. Shuffle country labels 10,000 times; recompute Δβ each shuffle. p-value = fraction of shuffled Δβ ≤ observed Δβ (one-sided test).
4. **Effect-size:** Cohen's d on the three paired Δβ values.

**§5.5 Confound logging (per scout report §4):**

The first commit MUST include explicit confound logs:

1. **Linguistic-substrate baseline:** repeat the entire analysis on **Russian-state-media vs Russian-émigré-media** if data available (Meduza, Novaya Gazeta archive). If Δβ direction reverses, the cross-country effect was linguistic, not political — revise hypothesis or scope.
2. **GDELT pipeline drift:** confine to v2 only (post-2015). If results are sensitive to v2.0 vs v2.1 schema changes (logged in GDELT's update history), flag clearly.
3. **Publication-cadence asymmetry:** all six countries are aggregated to daily, so this is mitigated by construction. Log the daily aggregation method explicitly.
4. **Tone-pipeline confound:** GDELT tone is computed by an English-trained sentiment model. **Tone signal is reported with explicit caveat** and not treated as primary evidence; event_count and entropy are primary.
5. **Scale-window selection:** β depends on the fit window. Report **multi-scale fluctuation plots**, not single β numbers. Pre-register the scale window: f ∈ [1/365, 1/10] cycles-per-day.

---

## §6 What gets committed (the first-commit deliverable per task #167)

**Target: first commit within 7 days of task #150 operationalization shipping (i.e., by 2026-06-09).**

Per scout report §6 estimate, ~3 working days from GDELT data ingest to first plotted result. The first commit lands the following artifacts in `/pilots/1f_failsafe/` of the framework repo:

- `pilots/1f_failsafe/README.md` — pilot pre-registration (this document distilled + executable plan)
- `pilots/1f_failsafe/data_ingest.py` — GDELT v2 query + per-country aggregation
- `pilots/1f_failsafe/dfa_pipeline.py` — Welch PSD + DFA + MFDFA computation
- `pilots/1f_failsafe/stats_test.py` — bootstrap CI + IAAFT surrogate null + permutation test
- `pilots/1f_failsafe/results.md` — Cohen's d effect sizes, p-values, 6-panel log-log fluctuation plot
- `pilots/1f_failsafe/confounds.md` — explicit log per §5.5 above
- `pilots/1f_failsafe/methods.md` — methods note, citing scout report + Altmann 2012 + Clauset 2009
- `pilots/1f_failsafe/requirements.txt` — Python version pins

**The first commit is the pre-registration + ingest scripts.** The result deliverable (the 6-panel plot + effect sizes + p-values) lands as the second commit, ~3 days later.

**Success criterion for "task #150 has broken ground":** the pre-registration commit lands at the repo with the analysis plan locked. This unblocks the audit v06 §10 + Reading 08 §9 hard-stop on further infrastructure / outbound-responsive work.

---

## §7 Confounds explicitly named and not yet mitigated (per scout report §4)

The framework's discipline (cont 27 §2) requires naming what could explain the result *without* the framework's claim. Six confounds identified by the scout:

1. **Linguistic-substrate baseline (Zipf-and-LRC confound).** Word frequency follows Zipf with exponent ≈1, which translates to 1/f-ish behavior at the word-level independent of political system. The pilot avoids this by using tone/event/entropy signals not raw word frequency, but the confound at the *meta* level (does GDELT's NLP pipeline propagate Zipf-like structure into its tone aggregates?) is not fully eliminated. Mitigation: within-language baseline (Russian state vs Russian émigré) addresses this directly if data exists.

2. **GDELT pipeline drift.** GDELT NLP changed in 2015 (v1→v2). Confined to v2 by pre-registration. Any future minor GDELT updates within v2 are logged.

3. **Source-volume confound.** High-volume sources have lower-variance daily counts. Mitigation: per-country z-score normalization before DFA (§5.2 step 1).

4. **Publication-cadence asymmetry.** All six countries aggregated to daily; mitigated by construction. Logged.

5. **Tone-pipeline confound.** GDELT tone computed by English-trained sentiment model. Cross-language tone comparison is suspect. Mitigation: tone treated as secondary signal with explicit caveat; primary signals are event_count and event-category-entropy which are language-agnostic.

6. **Scale-window selection.** β depends on the fit window. Mitigation: multi-scale fluctuation plots required; scale window pre-registered to f ∈ [1/365, 1/10] cycles-per-day.

**Unaddressed confounds (honest gap):**

- **Regime-intensity drift within country.** Russian state media in 2015 ≠ Russian state media in 2024. If β shifts within country during the window, the cross-country comparison is harder to interpret. H4 (within-country temporal shifts) addresses this exploratorily but not pre-registered to significance threshold.
- **Selection effects in GDELT source set.** GDELT indexes a curated set of media sources, weighted toward English-language outlets. The "Chinese coverage" available in GDELT is not a representative sample of all Chinese media — it's the subset GDELT chose to index. This could bias the signal in unknown directions.
- **N=3 pairs is a small sample.** Three paired comparisons is the minimum for Cohen's d. If the pilot lands H1 at d ≥ 0.5 and p < 0.05, the result is suggestive but not conclusive. Bar B promotion (§8 below) requires N ≥ 6 paired comparisons.

---

## §8 Promotion bars

Per cont 27 §3 procedure, this Tier 2 conditional candidate names explicit bars that would advance the claim toward Tier 2 algorithmically-demonstrated then Tier 1 epistemological canon.

**Bar A (advances to Tier 2 algorithmically-demonstrated):** The GDELT pilot lands H1 (β_authoritarian < β_pluralistic − 0.10) at Cohen's d ≥ 0.5 across all three paired comparisons, with p < 0.05 vs IAAFT surrogate null. **Plus** the within-language baseline (§7 confound 1) reproduces direction with d ≥ 0.3. **Plus** confound log (§5.5) is publicly committed and inspectable.

> **Bar A status — NOT satisfied (result-commit 2026-06-03).** GDELT v2 N=6 pilot returned mean Δβ = **+0.084** (wrong sign), Cohen's d = +0.380, permutation p = 0.792 on the primary entropy signal — H1 not supported. The small anti-direction Welch-β contrast is a source-volume sampling artifact (β vs log-volume r = 0.92; `pilots/1f_failsafe/confounds.md` §10), and the volume-robust DFA-α estimator shows no cross-country difference (spread 0.074). Neither a clean falsifier (d < 0.5 on primary) nor a strict null — a **confounded null**. Full verdict: [`pilots/1f_failsafe/results/discussion.md`](../pilots/1f_failsafe/results/discussion.md). The Tier 2 conditional claim is **neither advanced nor demoted** here; recommended next move is to narrow Reading 06 §10.3 and run the volume-robust Wikipedia edit-cadence replication (Bar B) before any demotion (Cowork's call).

**Bar B (advances toward Tier 1):** Replication on at least two additional independent signal sources (Wikipedia edit cadence pilot for matched-topic articles across zh/ru/en/de wikis per scout report alternative #1, AND Watchtower vs mainstream-religious-publication monthly time series per scout report alternative #2) shows directional consistency with the GDELT pilot result. Total N ≥ 6 paired comparisons across at least 3 substrate types.

**Bar C (would advance to Tier 1 epistemological canon):** External replication by independent research community using framework-naive methodology, with results citing the framework's interpretation. (This is the long-horizon promotion bar; not pre-registered to any specific timeline.)

---

## §9 What this does NOT change

Per cont 27 §2 discipline, explicit non-change notes:

**§9.1 Cont 26 §3 L0 evolved failsafe environment Tier 1 epistemological canon is unchanged.** Task #150 operationalizes a TESTABLE predictive consequence of cont 26 §3, but cont 26 §3 itself doesn't depend on the pilot result. If the pilot refutes H1, cont 26 §3 stays at Tier 1 epistemological canon but Reading 06 §10.3's Tier 2 conditional is forced into demotion.

**§9.2 Reading 06 §2.1 cymatics narrowing is unchanged.** Reading 08 demoted γ-World to L0-mediator candidate not convergence #10; this pilot is independent of the convergence-list discussion.

**§9.3 Task #151 RC-Koopman cultural-eigenmode pilot is queued, not in_progress.** Per Pav's "lets do 150 and then 151" steer, #151 comes after #150's first commit lands.

**§9.4 The framework's stance on consciousness is unchanged.** Per cont 17, brackets consciousness questions agnostically. This pilot operates entirely at the social-substrate spectral level; no consciousness commitment carried.

**§9.5 The fringe rejections from Reading 06 §11.2 are unchanged.** No pilot finding (positive or negative) advances or weakens fringe cycle theories. The 1/f signature is the framework's L0-failsafe-health claim; it is not a cycle theory.

**§9.6 The audit v06 + Reading 08 hard-stop on further infrastructure is unchanged.** Task #150 operationalization is substantive empirical work product per audit v06 §10.5. The hard-stop on *infrastructure* still holds; the pilot work itself is the discipline-prescribed move.

---

## §10 Cross-references

- [readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md](../readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md) §10.3 — original Tier 2 conditional hypothesis
- [readings/2026-05-31_bes_bidirectional_evolutionary_search.md](../readings/2026-05-31_bes_bidirectional_evolutionary_search.md) §7.2 — BES backward decomposition is partial methodology gift (sub-goal decomposition)
- [readings/2026-06-02_gamma_world_multi_agent_world_modeling.md](../readings/2026-06-02_gamma_world_multi_agent_world_modeling.md) §6 — γ-World NOT applicable (1/f is measurement-design not architecture)
- [continuations/26.md](../continuations/26.md) §3 — L0 evolved failsafes (Tier 1 epistemological canon this candidate operationalizes a predictive consequence of)
- [continuations/27.md](../continuations/27.md) §2-3 — three-tier procedure + pruning rules under which this candidate operates
- [audits/v06.md](../audits/v06.md) §10 — substantive-research-displacement-by-infrastructure concern; this operationalization is the substantive-research move
- [candidates/energy_floor_failsafe.md](energy_floor_failsafe.md) — promoted to canon per cont 27; structural precedent for candidate-promotion workflow
- [candidates/cultural_eigenmode_analysis.md](cultural_eigenmode_analysis.md) — parallel Tier 3 candidate (task #151)
- [candidates/bes_convergence_9.md](bes_convergence_9.md) — Tier 2 candidate (Reading 07)

**Key sources** (per scout report, full bibliography in commit's `methods.md`):

- [GDELT Project](https://www.gdeltproject.org/data.html) — primary data source
- [Altmann/Cristadoro/Esposti 2012 PNAS](https://www.pnas.org/doi/10.1073/pnas.1117723109) — LRC-in-text baseline
- [Clauset, Shalizi, Newman 2009 arxiv](https://arxiv.org/abs/0706.1062) — power-law fitting + KS goodness-of-fit
- [Alstott, Bullmore, Plenz 2014 PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0085777) — `powerlaw` Python package
- [nolds GitHub](https://github.com/CSchoel/nolds) — DFA + Hurst implementation
- [fathon GitHub](https://github.com/stfbnc/fathon) — MFDFA + DCCA implementation
- [colorednoise GitHub](https://github.com/felixpatzelt/colorednoise) — IAAFT surrogate generation
- [Surrogate data testing Wikipedia](https://en.wikipedia.org/wiki/Surrogate_data_testing) — null distribution methodology

---

## §11 Operationalization status

- **Operationalization document shipped:** 2026-06-02 (this file).
- **Pre-registration locked:** H1 with effect-size + significance thresholds locked at 2026-06-02 before any GDELT data examined.
- **Scout report completed:** task #150 scout report by opus subagent, 2026-06-02 (synthesized into this document's §3 + §7).
- **First-commit target:** 2026-06-09 (within 7-day discipline hard-stop window per task #167).
- **Result-commit target:** 2026-06-12 (3 working days after first commit per scout report §6).
- **Bar A evaluation target:** within 30 days of result commit, by audit v07 (target 2026-06-16 per audit v06 §9) at latest.
- **Result-commit LANDED 2026-06-03** (Claude Code, task #169) — 2 days after first-commit, well inside the 7-day window. **Verdict: H1 NOT SUPPORTED (confounded null).** Primary entropy signal Δβ = +0.084, d = 0.380, p = 0.792; contrast confounded by source volume (r = 0.92); volume-robust DFA-α null. Bar A unmet. Deliverables: `pilots/1f_failsafe/results/{gdelt_results.json, log_log_plot.png, discussion.md, methods.md}`. New confounds logged at `pilots/1f_failsafe/confounds.md` §9–§14. Candidate held at Tier 2 conditional pending Cowork decision (narrow §10.3 + run Wikipedia replication before any demotion).

**The substantive-research-displacement pattern starts closing here.** Reading 08 §9 was firm: the framework hard-stops on further infrastructure / outbound-responsive work until task #150 or task #151 has a first commit. Task #150 operationalization clears the first half of that gate. The pilot code commit clears the second half.

Per Pav's steer ("lets do 150 and then 151"): once task #150's first commit lands, the framework moves to task #151 (RC-Koopman cultural-eigenmode pilot, architecturally scoped by Reading 08 §6).
