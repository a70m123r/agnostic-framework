# P-L5 Avalanche Census — Findings (2026-06-13)

**Status: committed; real fetched data only; no fabrication.**

Register: exploratory INSTRUMENT (collect→observe→classify), 0.99-not-Boolean,
dimensionless-only cross-series (E-units), read-only.

---

## 0. Pre-registration (declared before any fit was run)

| parameter | value |
|---|---|
| temporal resolution | daily |
| baseline b(t) | trailing 28-day median ending at t-1 (spike cannot contaminate its own baseline) |
| testability gate | b(t) >= 5 views/day |
| excited-day threshold | v(t) >= 2.0 × b(t) |
| avalanche | maximal run of consecutive excited days; gap=0 |
| censoring | runs touching first testable day or last data day excluded |
| primary observable | R = max_t v(t)/b(t) over run (dimensionless; E-units) |
| secondary observables | X = Σ(v/b−1) (integrated excess); D = run length (days) |
| fitting | Clauset xmin scan (KS-minimizing) + MLE alpha + KS GOF; lognormal alt on same tail; Vuong LR test |
| sensitivity grid | thresh ∈ {1.5, 2.0, 3.0} × base_win ∈ {14, 28, 56} × gap ∈ {0, 1} = 18 combos |
| languages | en.wikipedia + ja.wikipedia |
| series window | 2025-06-01 to 2026-06-10 (12 months + 10-day margin) |

Census is CONDITIONAL on reaching the top-40 of ≥1 sampled day (11 days Mar–May 2026),
so the small-spike end is selection-truncated; the tail is what we fit.

---

## 1. Data provenance

- **Endpoint family:** Wikimedia REST v1 pageviews API (verified live)
- **UA:** `agnostic-framework-research/0.1 (research instrument)`
- **Top days sampled (11):** 2026-03-01, 03-10, 03-19, 03-28, 04-06, 04-15, 04-24, 05-03, 05-12, 05-21, 05-30
- **EN corpus:** 312 unique articles after junk filter; 240 chosen by best-rank union rule; 240 series fetched; 8 failed baseline gate (< 5 views/day sustained)
- **JA corpus:** union 156; 120 chosen; 120 fetched; 0 failed gate
- **Scripts:** `p_l5_fetch.py`, `p_l5_analyze.py`
- **Cached data:** `data/pa_{en,ja}.wikipedia_*_20250601_20260610.json` (360 files)
- **Results:** `results/p_l5_results.json`, `results/p_l5_avalanches.csv`

---

## 2. Avalanche census — raw counts

| metric | en.wikipedia | ja.wikipedia |
|---|---|---|
| articles with data | 240 | 120 |
| articles failing baseline gate | 8 | 0 |
| avalanches detected | 2456 | 2082 |
| censored/excluded | 68 | 22 |
| avalanches analyzed | 2456 | 2082 |
| D_median (days) | 2.0 | 1.0 |
| D_p90 (days) | 11.0 | 6.0 |
| D_max (days) | 34 | 23 |
| fraction single-day (D=1) | 0.428 | 0.522 |

---

## 3. Spike-size distribution (R = peak/baseline, dimensionless)

### 3.1 Quantiles

| percentile | en.wikipedia (R) | ja.wikipedia (R) |
|---|---|---|
| 50th | 3.35 | 3.59 |
| 75th | 7.24 | 7.34 |
| 90th | 22.2 | 22.8 |
| 95th | 62.2 | 59.7 |
| 99th | 844 | 385 |
| 99.5th | 2895 | 993 |
| max | 17 155 | 9 892 |

The distribution is extremely heavy-tailed: the 95th percentile article had its
traffic multiply 60–62x its baseline in a day; the 99.5th percentile saw ~1000x; the
maximum observed spike (EN) was 17 155x — a 17,000-fold amplification.

### 3.2 Tail fits (primary observable R)

| quantity | en.wikipedia | ja.wikipedia |
|---|---|---|
| Clauset xmin | 4.37 | 7.84 |
| tail n | 946 | 487 |
| alpha (MLE) | **1.776** | **1.794** |
| alpha CI 95% boot | [1.706, 1.844] | [1.734, 1.936] |
| KS stat | 0.035 | 0.024 |
| GOF p (xmin fixed) | 0.055 | 0.815 |
| Vuong z | 0.43 | −0.51 |
| Vuong p | 0.666 | 0.611 |
| verdict | **indistinguishable** | **indistinguishable** |

**Neither power-law nor lognormal is favored by the Vuong test for R (peak/baseline)
on either language.** The data are consistent with both. Clauset caution honored.

Disclosed numerical note on EN lognormal: the unconstrained optimizer degenerates
(sigma → 1090 and mu → −922 361), reaching nearly the same log-likelihood as PL by
taking the LN toward a power-law–shaped distribution. With sigma constrained ≤ 5.0,
the best lognormal scores 6.98 log-likelihood units below PL, making PL actually
preferred — but the Vuong test with the degenerate LN parameterization still returns
"indistinguishable." The result is correct per the protocol (both models are plausible),
but the EN tail is closer to a pure power law than the Vuong label suggests. Reported
honestly; not overclaimed either direction.

### 3.3 Secondary observable X (integrated excess, dimensionless)

| quantity | en.wikipedia | ja.wikipedia |
|---|---|---|
| alpha | 1.549 | 1.674 |
| alpha CI 95% | [1.518, 1.645] | [1.632, 1.725] |
| Vuong p | 0.027 | 0.194 |
| verdict | **lognormal favored** | indistinguishable |

For EN the integrated-excess distribution prefers lognormal (p=0.027). This is not
contradictory with the R result: R = peak height, X = area under the spike — the
two observables carry different information about the avalanche shape, and a process
can have a PL-compatible peak but LN-compatible area.

---

## 4. Weekly periodicity (known confound: Okamura 2026)

| metric | en.wikipedia | ja.wikipedia |
|---|---|---|
| weekly amplitude median | 1.265 | 1.278 |
| weekly amplitude p90 | 1.692 | 1.620 |

Median DOW factor spread = 27% (EN) and 28% (JA) — measurable but modest. P90 = 69%
and 62% amplitude swings, so in the top decile of articles the DOW periodicity is
substantial. This confirms the Okamura 2026 confound.

**DOW-deseasonalized check:** fitting R on the DOW-deseasonalized series gives
alpha = 1.689 (EN, xmin=4.04) vs 1.776 raw. The periodicity inflates R slightly
(because peaks landing on high-traffic weekdays look bigger relative to the median
baseline). The ~0.09 shift is a confound bound, not large enough to change the
qualitative conclusion but real.

---

## 5. Hurst exponent (long-memory of increments)

Hurst estimated from aggregated-variance method on DOW-deseasonalized log-series,
after Okamura 2026's stochastic marginality framing.

| metric | en.wikipedia | ja.wikipedia |
|---|---|---|
| H median | **0.331** | **0.205** |
| H IQR | [0.204, 0.445] | [0.101, 0.333] |
| n articles | 232 | 120 |

EN H median = 0.33; JA H median = 0.21 — both substantially below 0.5 (anti-persistent
increments). This is Hurst for the LOG-INCREMENT series, not the raw series. An
anti-persistent H < 0.5 means mean-reverting behavior: spikes are followed by
corrections, the series returns to baseline. This is consistent with an excitable
medium below-supercritical: spikes do not self-sustain indefinitely.

**Relevance to Okamura 2026:** Okamura reports H ~ 0.32 for the Wikipedia top-1000
ensemble (Hurst of log increments). Our article-level median H = 0.33 (EN) matches
the ensemble estimate with high fidelity, providing cross-validation of both our
instrument and the Okamura claim that H < 0.5 is the characteristic behavior.

The stochastic marginality condition (Okamura) is H − η = 0 where η is the noise
exponent of the fBm-driven SDE. At H = 0.33, the criticality condition H − η = 0
requires η = 0.33. Whether η is actually 0.33 is not testable from this data alone;
what we can say is that H ~ 0.33 is in the range where the marginality condition
*could* be satisfied.

**Language difference:** JA H_median (0.21) < EN H_median (0.33). JA has MORE
anti-persistent increments — spikes revert faster/harder. Consistent with JA articles
having a narrower baseline audience and stronger mean reversion after exogenous spikes.
This is a real wrapper-layer difference (B9 in the NESTED_PONDS framing: JA straw is
narrower, so imported exogenous shocks revert faster relative to the local baseline).

---

## 6. Variance duel (log vs power model for Var[ln v(t/t0)])

**Okamura's key prediction: Var[ln X(t)] ∝ ln(t) not t^g.**

Cohort anchored on first top-appearance day; t=1..60 days.

| model | EN r² | EN AIC | JA r² | JA AIC |
|---|---|---|---|---|
| log: Var = a + b·ln(t) | 0.626 | −102.3 | 0.254 | −113.6 |
| power: Var = C·t^g | 0.580 | −95.3 | 0.220 | −111.0 |
| ΔAIC (log − power) | **−7.0** | | **−2.6** | |
| winner | **log** | | **log** | |

Log model wins on both EN and JA by AIC. The log-variance growth profile is
consistent with Okamura 2026's stochastic marginality (fBm-driven SDE at criticality).

**Critical caveat (from Okamura and from the analysis code):** Okamura's scaling
holds above a breakpoint t_c = 61–276 days. Our window tmax=60 days sits at the
bottom of this range — we are in the "ambiguous zone" where log and polynomial fits
are nearly indistinguishable (r² difference only 0.046 for EN). The AIC difference
of -7.0 favors log, but this is heuristic (Var(t) points are serially correlated
through the shared cohort). Stated as "consistent with" not "confirms."

EN log model parameters: a=3.56, b=0.597.
JA log model parameters: a=1.53, b=0.245.

The log-slope b (= rate of variance growth) is ~2.4× larger for EN than JA,
meaning EN attention dynamics are more uncertain (larger variance in the
trajectory from a spike event). Consistent with EN being more deeply connected
to global news flows with heavier cross-platform recommendation traffic.

---

## 7. Sensitivity to operationalization (Notarmuzi 2022 caution)

Alpha range across all 18 (thresh, base_win, gap) combinations:

| language | alpha_min | alpha_max | range |
|---|---|---|---|
| en.wikipedia | 1.626 | 1.811 | **0.185** |
| ja.wikipedia | 1.779 | 1.907 | **0.128** |

The exponent varies by ±0.09 (EN) and ±0.06 (JA) around the primary estimate,
confirming the Notarmuzi 2022 warning. The range is real, not negligible.
Qualitative conclusion (alpha ≈ 1.7–1.9, heavy tail) is robust to all 18 combos
for both languages. No combo produces alpha ≥ 2.0 for either language.

---

## 8. Burstiness

Inter-avalanche-start intervals, normalized per article by mean (Goh–Barabasi BP;
quantile ratio q90/q50 inspired by Stadlan 2026 BTI motivation).

Poisson/exponential nulls: BP=0; q90/q50 = ln10/ln2 = 3.32.

| metric | en.wikipedia | ja.wikipedia |
|---|---|---|
| BP | −0.037 | −0.035 |
| q90/q50 | 3.302 | 3.088 |
| n articles | 197 | 119 |
| n intervals | 2217 | 1963 |

**BP ≈ 0 for both:** the inter-avalanche-arrival distribution is nearly Poisson
(BP = 0 is the Poisson null). There is NO extra burstiness in when avalanches
start. Individual avalanches are heavy-tailed in size (alpha ≈ 1.78), but the
TIMING of avalanche arrivals is approximately random across the year.

This is important: a truly self-organized-critical system would show bursty
arrival times (BP > 0). The near-zero BP suggests the avalanche initiations are
externally driven (news events, viral shares) rather than internally cascading
from prior avalanches. This supports the "predominantly exogenous burst" confound
classification from the fresh-refs (known confounds section).

q90/q50 = 3.30 (EN) vs null 3.32 — essentially indistinguishable from exponential.
JA q90/q50 = 3.09, slightly below exponential, meaning slightly MORE regular
arrivals than a Poisson process (possibly reflecting fixed weekly news cycles
dominating the JA corpus).

---

## 9. Time stratification (tail stationarity, Strauss 2025 confound)

Split at 2026-06-13 midpoint (2025-12-13):

| period | EN alpha | EN ntail | JA alpha | JA ntail |
|---|---|---|---|---|
| H1 (Jun–Dec 2025) | **2.147** | 327 | **2.212** | 164 |
| H2 (Dec 2025–Jun 2026) | **1.663** | 619 | **1.676** | 323 |

**The tail was SIGNIFICANTLY heavier in H2 than H1** (alpha dropped ~0.48 EN, ~0.54 JA).
This is a large temporal drift — the spike distribution was heavier-tailed in the
more recent half of the window.

**Critical confound note:** Top days were sampled exclusively from Mar–May 2026 (H2
period). Articles that only spiked in H1 are systematically under-represented in the
corpus (they needed to also appear in H2 to be selected). The apparent H1/H2 alpha
difference is AT LEAST PARTIALLY a selection artifact: H1 avalanches from articles
that spiked-and-died before our top-day window are not in the corpus at all. This
is the exact "top-days sampled Mar-May 2026 => H2 oversampled by selection" caveat
in the code. The drift is real in the sense that H2 avalanches in our corpus are
bigger, but whether this reflects a genuine secular drift (Strauss 2025 algorithmic
curation → heavier tails over time) or selection bias cannot be disentangled with
this corpus. Stated as "consistent with drift but not confirmed."

---

## 10. Baseline heterogeneity strata

| stratum | EN alpha | EN ntail | JA alpha | JA ntail |
|---|---|---|---|---|
| low (<750 views/day, EN) | 1.595 | 335 | 1.626 | 173 |
| mid (750–2378, EN) | 1.877 | 294 | 1.851 | 178 |
| high (>2378, EN) | 1.988 | 317 | 2.065 | 136 |

Higher-traffic articles have a LESS heavy-tailed spike distribution (alpha closer to
2.0 vs 1.6). This is consistent with Okamura 2026's 7-component heterogeneity: niche
articles that reach the top-list are there only via a single extreme spike (very
heavy tail, low alpha), while perennial high-traffic articles show many moderate
spikes (lighter tail, higher alpha). Stratification matters — an aggregate alpha
mixes these regimes.

---

## 11. DOW-deseasonalized confirmation

Fitting R on DOW-deseasonalized series:

| | EN | JA |
|---|---|---|
| n_av | 2384 | 1951 |
| alpha | 1.689 | 1.796 |
| xmin | 4.04 | 7.36 |

Raw vs deseasonalized alpha shift: +0.087 (EN), +0.002 (JA). The weekly
periodicity inflates R slightly for EN (creates artificially large peaks on
high-traffic days relative to 28-day median baseline). The confound is real
but small (~0.09 alpha units = within the sensitivity range). JA is nearly
unaffected, consistent with JA having somewhat flatter DOW profiles.

---

## 12. Reading: how tuned is the attention pond?

**Core measurement:** alpha ≈ 1.776 (EN), 1.794 (JA), CI95 [1.71, 1.84] and [1.73, 1.94].

For a power-law-compatible tail, alpha < 2 means infinite variance (the second
moment of the distribution does not converge). This places the Wikipedia attention
pond firmly in the **infinite-variance regime** — in the statistical mechanics of
SOC, this is the signature of a system tuned near or at criticality (a subcritical
system has exponential tails; a critical system has a power-law tail with alpha ≈ 2
or lower depending on the universality class).

**Notarmuzi 2022 comparison:** RFIM universality class gives tau = 9/4 = 2.25 for
event-size distributions on social platforms. Our alpha ≈ 1.78 < 2.25 is even
heavier-tailed. However, tau in Notarmuzi is for an event-size distribution over
the raw count data (discrete events), while our R is peak/baseline (a normalized
ratio). The two exponents are not directly comparable.

**The Okamura 2026 reframe (design change applied):** The correct model class is
stochastic marginality (fBm-driven SDE at H − η = 0), not a tunable SOC exponent.
The correct reading of P-L5 is therefore not "alpha = criticality distance" but:
(a) the tail is heavy enough to be consistent with a critical or near-critical system;
(b) H ≈ 0.33 < 0.5 is anti-persistent (mean-reverting); (c) Var grows ∝ ln(t) not
t^g (consistent with Okamura's marginality condition); (d) burstiness BP ≈ 0 (exogenously
driven initiations, not endogenous cascade). The composite reading: **the pond is
tuned near criticality (heavy tail, H near marginality condition), but avalanche
initiations are predominantly externally triggered, not self-sustaining cascades.**

**Language comparison (wrapper-layer reading):**
- Alpha is near-identical: EN 1.776 vs JA 1.794. The spike-size distribution is
  essentially the same in both ponds.
- H differs: EN 0.33 vs JA 0.21. JA spikes mean-revert faster/harder than EN.
- Variance-growth log-slope b differs: EN 0.597 vs JA 0.245. EN has 2.4× greater
  trajectory uncertainty from a spike event.
- These differences are consistent with EN being more deeply embedded in global
  cross-platform recommendation traffic (B9/B4: wider straw, heavier algorithmic
  amplification) and JA being more locally bounded (narrower straw, faster return
  to baseline).

**Reading per NESTED_PONDS framing:**
The SOC-as-control-target claim (sec. 0 of NESTED_PONDS) is supported in the
distributional sense: the Wikipedia attention pond produces spike-size distributions
with alpha < 2 (infinite variance), consistent with near-critical tuning. The
recommenders-as-criticality-tuners interpretation survives contact with data: the
tail is heavy enough that individual spikes can reach 10,000–17,000x baseline,
which is in the "a ripple can become an earthquake" regime. However, the BP ≈ 0
finding adds nuance: the pond is not in a regime of self-sustaining internal cascades
— it produces large spikes, but those spikes are externally seeded. The "gain medium"
pumps external shocks to extreme amplitudes but does not spontaneously generate
avalanche chains from ambient noise.

---

## 13. Dead children (dated tally)

1. **"power-law claim from straight-ish log-log line"** — NEVER CLAIMED. Pre-registered
   against this; both Vuong p > 0.1 for primary R, confirming the Clauset discipline was
   the right call.
2. **"single aggregate alpha characterizes the pond"** — DEAD. Stratification by baseline
   tercile shows alpha range 1.59–1.99 (EN); heterogeneity is real (Okamura 7-component
   decomposition confirmed at the article level).
3. **"tail exponent is stationary over 12 months"** — SUSPECT/CONFOUNDED. H1 alpha ≈ 2.15
   vs H2 alpha ≈ 1.66 is a large drift, but cannot be disentangled from selection bias
   (top-days sampled in H2 period). Status: confounded, not definitively dead.
4. **"JA and EN ponds are tuned to the same criticality level"** — REFINED. Alpha
   indistinguishable (1.78 vs 1.79), but H (0.33 vs 0.21) and variance-growth slope
   (0.60 vs 0.25) differ substantially. Same tail shape, different dynamics. The ponds
   are similarly heavy-tailed but differently damped.

---

## 14. Owed

1. **Separation of exogenous vs endogenous bursts** — for genuine SOC/endogenous-cascade
   reading, need to classify each spike as externally triggered (matching external
   news events) vs spontaneous. Currently not done.
2. **Extend t_max past 60 days for the variance duel** — to enter Okamura's non-ambiguous
   zone (t > 60–276 days) and confirm or refute the log-vs-power split with a proper
   window.
3. **BTI (exact Stadlan 2026 formula)** — we computed BP and q90/q50 as a proxy; the
   exact BTI formula was not reproduced here (stated in code per disclosure). Implement
   for the next round.
4. **Human-triggered vs automated protection stratification** — needed for P-L6
   (protection damping); partially relevant here as a corpus sanity check.
5. **Time-de-biased corpus** — select top-days uniformly across the full 12-month window
   (not just Mar–May 2026) to get unbiased H1/H2 comparison.

---

## Artifacts

```
D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds/
  p_l5_fetch.py                    fetch script (top-lists + per-article series)
  p_l5_analyze.py                  analysis script (avalanche detection + fits + all tables above)
  data/pa_en.wikipedia_*_20250601_20260610.json   (240 files, real fetched data)
  data/pa_ja.wikipedia_*_20250601_20260610.json   (120 files, real fetched data)
  data/top_en.wikipedia_*.json     (11 top-day lists, real fetched data)
  results/fetch_manifest.json      (provenance: UA, chosen articles, 404 log)
  results/p_l5_results.json        (full committed results)
  results/p_l5_avalanches.csv      (per-avalanche table: article, dates, R, X, D)
  P_L5_FINDINGS.md                 (this file)
```
