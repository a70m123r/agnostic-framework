# FINDINGS — Latent Ponds Experiment (P-L4 / P-L5 / P-L6)
## experiments/latent_ponds/

**Status:** Three probes completed 2026-06-13. All computation real; no synthetic data mixed into measured quantities. Register: exploratory INSTRUMENT (collect-observe-classify), 0.99-not-Boolean, dimensionless-only across phenomena (E-units), model bits counted, read-only.

---

## 0. Provenance and reproduction

**Data sources:** Wikimedia REST API v1 (hourly aggregate pageviews, per-article daily pageviews, top-1000 daily lists) + MediaWiki action API (protection log, letype=protect, ns=0). UA: `agnostic-framework-research/0.1 (research instrument)`. All raw responses cached to disk.

**Scripts (under `experiments/latent_ponds/`):**
- `01_fetch_hourly.py` — fetches 5-language hourly aggregate pageviews 2026-03-01 to 2026-06-01
- `02_harness_analysis.py` — FFT, autocorrelation ladder, Q6 rung instrument, circadian profiles
- `03b_profiles.py` — per-language profiles
- `04_canon_radius.py` — cross-pond daily Pearson r, rolling 7-day co-movement, event detection
- `p_l5_fetch.py`, `p_l5_analyze.py` — avalanche census (240 EN + 120 JA articles)
- `pl6_fetch.py`, `pl6_fetch2.py`, `pl6_analyze.py` — protection damping (311 matched pairs)
- `skeptic_pl4_canon.py`, `skeptic_pl5_run.py`, `skeptic_pl6_probe.py` — adversarial passes

**Result files:**
- `data/` — hourly JSON (5 languages, all-access + desktop + mobile-web), per-article JSON (360 articles), pl6/ dataset
- `results/p_l5_results.json`, `results/p_l5_avalanches.csv`, `pl6_results.json`
- `results/skeptic_pl4_canon.json`, `results/skeptic_pl5_real_data.json`, `results/skeptic_pl6_probe.json`, `results/skeptic_verdict.json`

**Parent instruments:** Q6 rung instrument (GOES X-ray week, D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/q6_scale_rung/), rho identity RMS 0.006 bits (flare) vs 0.053 bits (wiki pond).

---

## 1. P-L4 — Harness Signature (wrapper-layer readings)

**Series:** 5 language ponds (en/ja/de/ar/es), 2232 hourly points each, 93 days, 2026-03-01 to 2026-06-01. Total views in window: en=20.2B, ja=2.59B, de=2.08B, es=1.57B, ar=0.32B.

### 1A. Location wrapper — circadian phase

The 24h spectral line is the dominant spectral feature across all five ponds. FFT power fraction at the 24h bin (Hann-windowed, linearly detrended): es=58.97%, en=55.62%, ar=45.45%, ja=43.57%, de=39.77%. Autocorrelation at lag=24h: ja=0.9730, de=0.9549, es=0.9505, ar=0.9313, en=0.9304.

Peak hours in UTC and their location readings:

| Pond | Peak UTC | Local time | Phase vs en | Peak/Trough | Reading |
|------|----------|-----------|-------------|-------------|---------|
| en   | 20h      | 16h EDT / 13h PDT / 21h BST | 0h | 1.61 | Most phase-smeared; 5 continents averaged; lowest sharpness |
| ja   | 12h      | 21h JST   | -8h | 5.44 | Exact JST readout; single-timezone, second-sharpest |
| de   | 19h      | 21h CEST  | -1h | 9.63 | Sharpest amplitude; European population goes offline overnight most completely |
| ar   | 20h      | 23h AST / 22h EET | 0h | 2.13 | Gulf/ME center; Morocco-Gulf spread smears but does not shift peak |
| es   | 21h      | 23h CET / 18h CDT | +1h | 2.71 | LATAM evening bias; 12-timezone compromise |

The peak-hour UTC is the latent ocean's readout of where the observer bodies are and when they sleep. The peak/trough ratio is the location-anchoring coefficient: higher = geography-concentrated pond, lower = diffuse multi-timezone population. Ranking by sharpness: de (9.63) > ja (5.44) > es (2.71) > ar (2.13) > en (1.61).

The monthly amplitude trend for en (testing Crokidakis 2026 monotonic-degradation): Mar FFT@24h=0.557, Apr=0.555, May-Jun=0.568. No monotonic shrinkage over 93 days. Crokidakis gradual-attention-degradation prediction NOT supported on this timescale.

### 1B. Weekly spectral line

The 168h (weekly) line: FFT fractions are weak (0.15%–1.02%) but the autocorrelation at lag=168h is high: ja=0.9812, de=0.9691, es=0.9677, en=0.9407, ar=0.8816.

For en specifically: ac@168h (0.9407) exceeds ac@24h (0.9304). The weekly institutional memory is slightly stronger than the circadian in the aggregate en pond. The autocorrelation ladder confirms:

| Lag  | en rho | en shrink (bits) |
|------|--------|-----------------|
| 24h  | 0.9304 | 1.4226 |
| 48h  | 0.9010 | 1.1683 |
| 72h  | 0.8967 | 1.1376 |
| 96h  | 0.8956 | 1.1298 |
| 120h | 0.8909 | 1.0984 |
| 144h | 0.9177 | 1.3018 |
| 168h | 0.9407 | 1.5377 |

rho rises from lag=120h to lag=168h (day 5 to day 7), confirming a weekly memory bump on top of the circadian. This is the Okamura 2026 confound confirmed in the data: weekly periodicity corrupts naive Hurst estimation and any burstiness metric on the raw hourly series.

### 1C. Q6 rung instrument on en.wikipedia

Persistence law f(t)=f(t-1) on log10 hourly views, lzma-9 coder, quantized int32 (log10*1000), model bits overhead=64. Identity shrink=-0.5*log2(2*(1-rho1)), RMS error 0.053 bits across 4 rungs (vs 0.006 bits for GOES flare).

| Rung  | n    | rho1   | raw CR | resid CR | shrink_id (bits) | shrink_emp | id_error |
|-------|------|--------|--------|----------|-----------------|------------|---------|
| 1h    | 2232 | 0.9249 | 0.276  | 0.2419   | 1.3672          | 1.4215     | 0.0543  |
| 6h    | 372  | 0.0241 | 0.3253 | 0.3199   | -0.4824         | -0.4907    | 0.0083  |
| 24h   | 93   | 0.5141 | 0.5591 | 0.6237   | 0.0207          | 0.0369     | 0.0162  |
| 168h  | 14   | 0.7354 | 1.6429 | 1.7857   | 0.4591          | 0.5482     | 0.0890  |

The 6h rho collapse (rho1=0.024) is the circadian quarter-period zero-crossing — the persistence law is the wrong law at this rung for a 24h periodic signal. This is the Q6 law-relativity finding applied to the wiki pond: each rung selects a different causal regime. The 168h rung (n=14) is indicative only; rho1=0.735 is the raw Pearson (more robust at small n).

Dial placement vs Q6 flare: the flare reached its edge=0 crossover at rung=60min (rho=0.484). The wiki pond at rung=1h already has rho1=0.925 — high persistence entering the ladder. But the wiki's non-monotone rho profile (1h: 0.925 → 6h: 0.024 → 24h: 0.514 → 168h: 0.735) places it as a qualitatively different phenomenon: two-timescale (circadian + weekly) rather than single-timescale (monotone decay). The rung dial is a phenomenon selector here, not a zoom dial.

### 1D. Canon-radius (cross-pond coupling) — adversary-corrected

Raw 93-day Pearson r on daily totals: strongest pairs de-es (0.697) and en-es (0.689). Weakest: ja-ar (0.130).

After detrending, deweeklying, and AR1-whitening (adversary protocol, results/skeptic_pl4_canon.json):

| Pair  | Raw r | Residual r | SE (n_eff~65) | t-stat | Verdict |
|-------|-------|------------|---------------|--------|---------|
| de-es | 0.697 | 0.425      | 0.135         | 3.15   | Unambiguously non-zero |
| en-es | 0.689 | 0.169      | 0.130         | 1.30   | Indistinguishable from zero |
| de-ar | 0.272 | 0.306      | 0.142         | 2.15   | Anomalous (higher than en-es post-whitening) |
| en-ja | 0.272 | ~0.12      | ~0.14         | <1.0   | Not significant |
| ja-ar | 0.130 | ~0.05      | ~0.14         | <0.5   | Not significant |

Timezone-similarity null (circular UTC peak-hour distance) correlates r=0.534 with the residual matrix. Zero global-canon events (all 5 ponds simultaneously r>0.75 in any 7-day rolling window) found in 93 days. The most coordinated 7-day window found: starting 2026-04-12, mean cross-language r=0.867 across en-ja/de/ar/es. Most fragmented: starting 2026-03-30, mean r=-0.295.

Arabic (ar) shows a structural break beginning approximately 2026-04-01 (negative correlations with en/de/es through mid-May). Consistent with post-Ramadan regional reorientation, unverified geopolitical event, or seasonal pattern; driving content unknown without per-article lookup.

**Anchor thesis verdict:** The 'wrapper coupling coefficient' is not measurable from aggregate daily data. The operationalization fails falsifiability: it makes no prediction distinguishing 'content-level coupling through language wrapper' from 'shared working-hours create same-day volatility.' Demoted to working hypothesis requiring article-level instrument.

**Caveats:** Mobile+desktop traffic folded in aggregate (Piccardi/West 2025 split needed for sharper B9 reading). The de-ar anomaly (residual r=0.306 > en-es=0.169) has no explanation in the wrapper-distance model. The ar structural break cause is unidentified.

---

## 2. P-L5 — Avalanche Census

**Corpus:** 240 EN articles + 120 JA articles reaching top-40 of en/ja.wikipedia on at least one of 11 sampled days (Mar–May 2026, 9-day intervals). Pageview data: 2025-06-01 to 2026-06-10 (375 daily points per article). Avalanche definition (pre-registered): peak day view count R_k = peak / 28-day rolling median baseline; avalanche if R_k > 2x baseline, separated by >3 days. Scripts: p_l5_fetch.py, p_l5_analyze.py.

### 2A. Tail shape

| Metric | EN | JA |
|--------|----|----|
| n_articles | 240 | 120 |
| n_avalanches | 2456 | 2082 |
| R_median | 3.35x | 3.59x |
| R_p90 | 22.2x | 22.8x |
| R_p99 | 844x | 385x |
| R_max | 17,155x | 9,892x |
| alpha_MLE | 1.7758 | 1.7942 |
| CI95_boot | [1.706, 1.844] | [1.734, 1.936] |
| x_min | 4.374 | 7.844 |
| n_tail | 946 | 487 |
| KS_stat | 0.0346 | 0.0241 |
| GOF_p | 0.055 | 0.815 |
| Vuong_p (PL vs LN) | 0.666 | 0.611 |
| Vuong verdict | indistinguishable | indistinguishable |

Alpha < 2 = infinite-variance regime in both languages and across all 18 operationalization cells (threshold x baseline-window x gap). Sensitivity range: 0.185 (EN) / 0.128 (JA). Qualitative conclusion (alpha~1.7–1.9, heavy tail) is robust across all cells.

The tail is real. A ripple can empirically become an earthquake.

### 2B. Stochastic marginality (Okamura 2026 design change applied)

Var[ln v(t/t_0)] growth model comparison (ensemble variance-growth from spike onset):
- EN: log model wins, delta-AIC = -6.99 (log-variance growth), slope b = 0.5973
- JA: log model wins, delta-AIC = -2.64, slope b = 0.245

Hurst exponent (aggregated-variance on log-increments, DOW deseasonalized):
- EN: H_median = 0.3308, IQR [0.204, 0.445], n=232 articles
- JA: H_median = 0.2048, IQR [0.101, 0.333], n=120 articles

H < 0.5 in both languages = anti-persistent (mean-reverting after spikes). EN H=0.33 matches Okamura's ensemble estimate of ~0.32 — cross-validation. EN variance-growth slope 2.4x JA: EN trajectories after a spike are much more uncertain, consistent with EN's deeper embedding in global recommendation traffic.

**SOC criticality claim verdict:** PARTIAL. The heavy tail is real. But: (1) Vuong PL vs LN indistinguishable — no decisive preference for power law; (2) BP = -0.037 (EN) / -0.035 (JA) — near-zero, not bursty, exogenous seeding not internal cascading; (3) H < 0.5 — anti-persistent, not self-amplifying; (4) only one observable measured. The correct frame is stochastic marginality (Okamura 2026, fBm-driven SDE at criticality condition H-eta=0), not a tunable SOC exponent. Reading: 'consistent with heavy-tailed stochastic marginal distribution, alpha~1.78, driven predominantly by exogenous events.'

### 2C. Avalanche duration and burstiness

| Metric | EN | JA |
|--------|----|----|
| D_median (days) | 2 | 1 |
| D_p90 (days) | 11 | 6 |
| D_max (days) | 34 | 23 |
| frac_D=1 | 0.428 | 0.522 |
| BP | -0.0366 | -0.0348 |
| q90/q50 inter-avalanche | 3.302 | 3.088 |
| q90/q50 Poisson null | 3.322 | — |
| Weekly amplitude median | 1.265 | 1.278 |

q90/q50 indistinguishable from Poisson null — confirms near-zero burstiness reading.

### 2D. Active confounds

- Weekly periodicity (Okamura 2026): DOW-deseasonalized alpha for EN = 1.689 vs raw 1.776 (delta=0.087); real but within sensitivity range.
- Baseline heterogeneity: alpha ranges 1.595 (low-traffic tercile) to 1.988 (high-traffic tercile); single aggregate alpha is a mixture.
- Temporal drift: H1 alpha ~2.15 vs H2 alpha ~1.66; confounded by sampling selection (H1-only articles absent from corpus). Cannot claim secular drift.
- EN lognormal degenerate fit: unconstrained sigma diverges; with constrained sigma, PL is 6.98 LL units preferred; 'indistinguishable' label is technically correct per Vuong protocol but overstates LN competitiveness for EN.
- R_max=17,155x for EN is a genuine measured value but may reflect an API redirect artifact; not verified at article level.

---

## 3. P-L6 — Intervention Damping

**Dataset:** 4954 protection log events fetched (en.wikipedia, 2026-03-01 to 2026-05-10). 511 treated candidates pre-screened via top-1000 daily lists; 415 qualifying treated storms (pre-protection burst confirmed); 311 matched pairs (caliper=0.35 on log10 peak excess, pre-peak growth rate g matched, mean |delta_g|=0.016). Controls: 1027 clean qualifying candidates (218 flagged with standing protection, excluded). Bootstrap B=4000, sign-flip permutation inference. Post-event window: 31 days.

### 3A. Primary decay-rate outcome (E1)

| Metric | Treated | Control |
|--------|---------|---------|
| lambda_median (/day) | 0.1944 | 0.1740 |
| lambda IQR | [0.117, 0.282] | [0.124, 0.226] |
| paired mean delta | +0.0251 | — |
| CI95 | [+0.009, +0.041] | — |
| p_signflip | 0.00295 | — |
| paired ratio median | 1.1181 | — |
| frac treated slower than control | 0.4341 | — |

### 3B. Same-weekday residual and DiD

| Outcome | Value | CI95 | p_signflip |
|---------|-------|------|-----------|
| d_lnR7 (day+7 residual) | -0.310 | [-0.472, -0.141] | 0.0003 |
| d_lnR14 | -0.430 | [-0.659, -0.188] | 0.0004 |
| DiD at k=7 | -0.310 | [-0.476, -0.147] | — |
| DiD at k=21 | -0.506 | [-0.752, -0.262] | — |
| tail_AUC21 d_ln | -0.178 | [-0.290, -0.062] | 0.00165 |
| protection-anchored delta_lambda (n=189) | +0.0346 | [+0.015, +0.054] | 0.0009 |

The statistical association is real and survives three alternative matching schemes. The DiD gap widens monotonically from day 1 through day 21, with no sharp post-protection inflection.

### 3C. Stratum readings

| Stratum | n | mean delta_lambda | Direction |
|---------|---|-------------------|-----------|
| Semi-protection | 265 | +0.031 | Drives aggregate |
| Extended-confirmed | 41 | -0.015 | REVERSAL — treated decays slower |
| Disruptive trigger | 78 | +0.040 | Strongest positive |
| Vandalism trigger | 82 | +0.021 | Positive |
| BLP trigger | 59 | +0.032 | Positive |

EC stratum reversal: extended-confirmed protection shows null/reversed effect. EC articles are the most prominent; protection may broadcast a prestige/salience signal that sustains attention (meaning-signal reading, not friction reading). n=41 too small to adjudicate.

### 3D. Lag and pre-peak structure

Protection lag from peak day: p10=-2d, p25=0d, p50=+1d, p75=+3d, p90=+9d, mode=0d (n=88). 50% of treated articles protected on or before peak day. Pre-peak cascade: median growth g=0.596/d (doubling time 1.16 days), well-matched between arms.

Streisand rebound rate: 0.96% treated vs 1.07% controls — rare and similar across arms.

### 3E. Mechanism challenge

Three independent lines from the data challenge the 'circuit breaker on the attention ocean' causal framing:
1. Zero protection events were traffic-triggered; all triggers are editorial-conduct-driven (arbitration 18%, vandalism 16%, disruptive 15%, sock 8%). Edit-protection blocks editors, not readers.
2. 50% of treated articles protected on or before peak day; the surge occurred into an already-protected state.
3. EC stratum reversal (-0.015, n=41): protection can sustain attention, not only damp it.

Most parsimonious reading: protected articles are more topically volatile (attracting both vandalism and high traffic); matching on peak magnitude and growth rate does not fully control for topic-class volatility; the lambda difference is a selection residual plus a meaning-signal effect (protection status changes the article's social valence per B6). The association is real; the circuit-breaker mechanism claim is not supported.

---

## 4. Philosopher's reframes (surviving; marked as speculation register)

**[SPECULATION] The pond as resonance system, not information system.** The weekly rho data reveals that ponds primarily carry RHYTHM, not content. rho@168h (0.9407) exceeds rho@24h (0.9304) for en. The spectral lines are not noise in the content measurement; they ARE the measurement. The ponds are resonators whose resonant frequencies read out the physical and social harnesses of the observer bodies. Events are perturbations on the resonator, not the signal itself. This reframes the entire instrument: the probes are reading the surface tension of mind-bubbles, not their contents.

**[SPECULATION] Intervention as ontological, not instrumental (B6 reading of P-L6).** The protection event is itself a social fact that changes the meaning of the article for the editing community. Protection broadcasts a status signal ('disputed' or 'under attack'), which may reduce emotional valence of engaging. The EC stratum reversal is consistent with protection broadcasting a PRESTIGE signal rather than a dispute signal. If so, the mechanism is meaning-selective gain (B6) operating THROUGH the intervention signal, not despite it. The observed decay difference reflects meaning, not friction.

**[SPECULATION] Time-rung as phenomenon selector, not zoom dial.** At rung=1h, the observer tracks persistence. At rung=6h, persistence inverts (circadian node). At rung=24h, near-zero-gain daily memory. At rung=168h, resurgent institutional rhythm. These are four categorically different processes sharing a substrate. The B(r,r') matrix is not a correlation matrix within one phenomenon — it is a coupling matrix across distinct causal regimes. The rung dial does not magnify; it selects the phenomenon.

**The lurker as the null case.** Pageviews are the tip. ~0.1% of Wikipedia readers ever edit. The 'attention pond' is the pond of the behaviorally activated minority, not the latent ocean. The majority lurkers are the tidal force the instrument cannot see and is currently attributing to the articles themselves. The dark matter triangulation experiment (out-of-box, below) is the read-only path toward this.

**Category error: 'the internet observer entity' is not coherent.** The internet is a plane, not an observer. An observer is a (wrapper stack, plane) pair. Pageviews are the aggregate residue of millions of distinct (harness, wrapper-stack, plane) triples. The moment 'the internet reads itself' is stated, the pond is reified into an agent.

---

## 5. Questions from the instrument (speculation/out-of-box register)

**Q1: Is the critical point locked in by design or discovered by evolution?** Two worlds are consistent: (a) platforms deliberately tune toward criticality to maximize engagement; (b) criticality is a fixed point of evolutionary dynamics (subcritical loses users, supercritical burns users, near-critical is the only stable equilibrium). The probe data cannot distinguish them. What experiment could? Controlled comparison of platform populations where recommendation algorithms are known to differ in their tuning objectives.

**Q2: What is the transfer function of the wrapper stack?** The probes have measured phase offsets and peak/trough ratios (location wrapper) and FFT fractions (language wrapper passband strength). The full transfer function — what happens at nonlinear high-salience regimes, how the language wrapper attenuates different topics, whether the bandwidth wrapper is low-pass or bandpass — has not been characterized.

**Q3: Does the pond drain into the substrate or back through the straw?** The full loop is: ocean → straw → mind → behavior → world → ocean. The probes read only the ocean side. Is the round-trip oscillatory? If unstable, it is a different kind of tsunami — one that builds on each pass through the loop.

**Q4: At what rung does meaning enter the wave equation?** If meaning-selective gain (B6) is rung-specific — outrage amplifies at fast rungs, epistemic needs at slow rungs — then the 'meaning-kernel enters the wave equation' claim is underspecified. What is the spectral structure of meaning-selective gain?

**Q5: Is the framework's own membrane adversarial?** Publishing findings about how attention ponds work is itself a pond-perturbation (B2, B5). The framework has no theory of its own perturbative effect. At scale, a widely-read model of how viral cascades work would be used by actors trying to engineer viral cascades. This is not a small concern.

---

## 6. Out-of-box experiments (read-only; no live perturbation)

**Dark matter triangulation:** Cross-correlate Wikipedia attention avalanches with publicly published downstream behavioral datasets (election results, Google Trends, Nielsen surveys) at varying lags. The lag structure between wiki spike and downstream behavioral shift measures how far the event penetrated below the membrane. Events that spike pageviews but show zero downstream behavioral correlation were surface noise; strong lagged correlations indicate the event reached the tides. All data sources are public, read-only, archivable.

**Phase-inversion probe for meaning-selective gain:** Compute the rolling 6h autocorrelation time series from the P-L4 cached data (already available). During global-canon events (windows where all 5 ponds co-spike), the 6h anti-correlation should flatten toward zero because emotional urgency overrides circadian damping. This is the first direct measurement of B6 as suppression of a structural physical signal — not amplitude amplification but phase structure disruption by content. Uses data already collected.

**Temporal holography (B5 applied to behavioral time series):** Does a single article's spike SHAPE (duration, peak/trough ratio, return-to-baseline curve) carry enough information to classify the event's semantic category (political crisis vs. sports vs. scientific discovery vs. celebrity death)? If yes, the spike is a holographic readout of event semantics — the wave's shape carries the meaning signature. Operationalizes B5 applied to the P-L5 avalanche dataset, fully read-only.

---

## 7. Adversary record (honest reversals)

| Target | Verdict | Key reversal |
|--------|---------|--------------|
| P-L4 circadian phase as non-trivial | PARTIAL | Phase offsets are exact demographic/timezone readouts; no framework concept needed for the trivial portion. Q6 rung identity (non-monotone rho profile) and weekly-rho resurgence survive as non-trivial. |
| Canon-radius Western-canon-bloc claim | REVERSES | After whitening, en-es drops to residual r=0.169 (t=1.30, zero). Only de-es survives (t=3.15). Zero global-canon events found. Timezone null correlates r=0.534 with residual matrix. |
| P-L5 'criticality-tuned' framing | PARTIAL | Heavy tail real (alpha~1.78, all 18 cells). But Vuong PL vs LN indistinguishable (p=0.67); BP~0 (exogenous, not bursty); H<0.5 (anti-persistent). SOC framing not supported; stochastic marginality is the correct frame. |
| P-L6 circuit-breaker mechanism | PARTIAL | Statistical association real (p=0.003, three matching schemes). But zero events traffic-triggered; 50% protected before peak; EC stratum reversal. Mechanism is selection residual + meaning-signal, not direct traffic damping. |
| Anchor thesis wrapper-coupling as measurable | REVERSES | No operational definition distinguishing wrapper-coupling from Pearson r on daily totals that cannot see article-level co-spiking. Unfalsifiable as operationalized. Demoted to working hypothesis. |

**Strongest surviving critique (adversary):** The anchor-thesis operationalization failure on P-L4. After whitening, only de-es survives. The 'wrapper coupling coefficient' cannot be measured from aggregate data. The thesis is unfalsifiable in current form.

---

## 8. Dead children (dated tally — demoted/dormant, not erased)

1. **canon-radius-as-aggregate-Pearson-r** — DEAD 2026-06-13. Collapses after whitening; en-es drops to t=1.30. Timezone null accounts for ~half of residual structure. Demoted to working hypothesis pending article-level instrument.
2. **SOC-criticality-as-empirical-claim from single-alpha fit** — DEAD AS STATED 2026-06-13. Vuong indistinguishable from lognormal; BP~0; H<0.5; only one observable measured. Replaced by stochastic marginality reading.
3. **circuit-breaker as direct traffic damper** — DEAD AS MECHANISM 2026-06-13. Zero events traffic-triggered; 50% protected before peak; EC reversal. Survives as association finding with agnostic mechanism.
4. **wrapper-coupling-coefficient as measurable from aggregate daily data** — DEAD AS OPERATIONALIZATION 2026-06-13. Unfalsifiable without article-level cross-language concordance instrument.
5. **temporal-alpha-drift (H1 alpha~2.15 to H2 alpha~1.66)** — DEAD AS SECULAR DRIFT CLAIM 2026-06-13. Confounded by sampling selection; demoted to hypothesis requiring temporally uniform design.
6. **Crokidakis-2026 monotonic-circadian-degradation over 93 days** — FALSIFIED 2026-06-13. Monthly FFT@24h fractions flat (0.555–0.568). Not supported on this timescale.

---

## 9. Owed (ordered by load-bearing status)

1. Article-level cross-language concordance instrument (the only path to operationalizing the anchor thesis)
2. Mobile vs desktop split for P-L4 (Wikimedia per-article API, access-type parameter)
3. Temporally uniform avalanche sampling for P-L5 (monthly top-40 across full year)
4. BTI (Stadlan 2026) implementation alongside BP
5. Weekly-component removal before Hurst estimation
6. P-L6 extended post-event window (90 days)
7. P-L6 trigger stratification with bot-flag check (McGrady 2025 structural break)
8. Phase-inversion probe for B6 (uses cached P-L4 data, read-only)
9. P-L2 archive-breaker probe (B1 operationalization)
10. P-L3 one-ripple-dates-the-tide probe (B5 operationalization, applied to P-L5 spike shapes)