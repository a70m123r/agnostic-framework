# Pilot #150 — Methods & reproducibility (result-commit)

**Result-commit date:** 2026-06-03. **Pre-registration locked:** 2026-06-02 (before any data examined).
**Verdict + interpretation:** [`discussion.md`](discussion.md). **Confound log:** [`../confounds.md`](../confounds.md).

---

## §1 Data source and acquisition

- **Dataset:** GDELT 2.0 Event Database, public BigQuery table `gdelt-bq.gdeltv2.events`.
- **Acquisition:** single aggregation query via BigQuery, run **2026-06-03**.
  - **Bytes scanned:** 21.39 GB (within BigQuery's 1 TB/month free tier → $0).
  - **Rows returned:** 47,610 (country × SQLDATE) aggregate rows.
  - **Auth:** browser OAuth (BigQuery sandbox) via `pydata-google-auth` 1.9.1 — no gcloud install, no billing account. Billing/quota project: a user project (free tier).
- **Why BigQuery rather than the 15-min-slice download.** The pre-registration (candidate §5.1) names BigQuery `gdelt-bq.gdeltv2.events` as the canonical ingest path. A streaming direct-download aggregator (`gdelt_ingest.py`) was also built and run as a fallback (no cloud creds initially available); it was superseded once BigQuery auth was set up, because BigQuery returns the **complete** archive (all events ever ADDED, including late-reported ones), giving higher per-country coverage. Both paths compute the identical locked aggregation (GROUP BY SQLDATE). Logged in `confounds.md` §9.

### The exact query (reproducible)

Aggregation is keyed by **SQLDATE** (candidate §5.1 step 2) and country is matched on **ActionGeo_CountryCode** (FIPS 2-letter), per the locked operationalization. Three signals per (country, day):

- `event_count` = COUNT(*)
- `mean_tone`   = AVG(AvgTone)            [secondary — cross-language caveat, candidate §5.5.4]
- `category_entropy` = Shannon entropy (bits) of the EventRootCode distribution   [**PRIMARY / H1**]

```sql
WITH base AS (
  SELECT SQLDATE AS d, ActionGeo_CountryCode AS cc, EventRootCode AS root, AvgTone AS tone
  FROM `gdelt-bq.gdeltv2.events`
  WHERE SQLDATE BETWEEN 20150218 AND 20251231
    AND ActionGeo_CountryCode IN ('CH','US','RS','UK','KN','GM','IR','FR','TU','NL','VE','CI')
),
day_agg AS (SELECT d, cc, COUNT(*) AS event_count, AVG(tone) AS mean_tone FROM base GROUP BY d, cc),
per_root AS (SELECT d, cc, root, COUNT(*) AS n FROM base WHERE root IS NOT NULL AND root != '' GROUP BY d, cc, root),
roots_tot AS (SELECT d, cc, SUM(n) AS tot FROM per_root GROUP BY d, cc),
ent AS (
  SELECT pr.d, pr.cc, -SUM((pr.n/rt.tot) * (LN(pr.n/rt.tot)/LN(2.0))) AS category_entropy
  FROM per_root pr JOIN roots_tot rt ON pr.d=rt.d AND pr.cc=rt.cc GROUP BY pr.d, pr.cc
)
SELECT da.d AS sqldate, da.cc AS cc, da.event_count, da.mean_tone, e.category_entropy
FROM day_agg da LEFT JOIN ent e ON da.d=e.d AND da.cc=e.cc
ORDER BY da.cc, da.d
```

(`bq.py` in the pilot dir runs auth → dry-run → query → CSV write end-to-end.)

### Countries (confounds.md §1 N=6 amendment), FIPS → label

| pair | authoritarian (FIPS→label) | pluralistic (FIPS→label) |
|---|---|---|
| 1 | CH → CHN | US → USA |
| 2 | RS → RUS | UK → GBR |
| 3 | KN → PRK | GM → DEU |
| 4 | IR → IRN | FR → FRA |
| 5 | TU → TUR | NL → NLD |
| 6 | VE → VEN | CI → CHL |

### Window and coverage

- **Window:** 2015-02-18 (GDELT v2's first available date — pre-registration window was 2015-01-01, but v2 does not exist before 2015-02-18; data-availability limited, not a pre-registration change) → 2025-12-31. **3,970 daily points per signal per country.**
- **Coverage (days with ≥1 event / 3970):** CHN/USA/RUS/GBR/IRN/FRA 3970; DEU/TUR 3969; PRK/NLD/VEN 3965; CHL 3957. All ≥ 99.6%.
- Output CSVs: `data/raw/<LABEL>_<signal>.csv` with columns `date,value` (empty value = no events that SQLDATE for mean_tone/category_entropy; 0 for event_count).

---

## §2 Analysis pipeline (`pilot.py --mode gdelt`)

Per the locked protocol (candidate §5.2–§5.4). The DFA / Welch / IAAFT / permutation functions were verified independently (`--mode verify` recovers known β within ±0.05; `--mode demo` reproduces the N=3 ceiling).

**Pre-processing (§5.2), per signal per country:**
1. Gap-fill: linear interpolation of missing (zero-event) days; edge clamp. Missing-day counts are tiny (PRK 5, NLD 5, VEN 5, CHL 13, DEU/TUR 1; all others 0) → < 0.4%. See `confounds.md` §14.
2. Z-score normalization within country (§5.2.1).
3. Linear detrend (§5.2.2).
4. ADF stationarity reported (lightweight numpy ADF, logged not gated, §5.2.3).

**Spectral estimation (§5.3), per (country, signal):**
- **Welch PSD → log-log slope in f ∈ [1/365, 1/10] cycles/day = β** (PRIMARY estimator per candidate §5.3 / README §4). `nperseg = min(512, N//4) = 512`, Hann window, 50% overlap, per-segment linear detrend.
- **DFA → α** over window sizes 10–365 days (β-equivalent robustness check; reported alongside).

**Statistical inference (§5.4):**
- **H1 test = paired permutation test on Δβ** across the 6 pairs (`permutation_test_delta_beta`, locked/tested; n_perm = 10,000; seed 2026). One-sided, H1: mean Δβ < 0. Returns observed mean Δβ, p, Cohen's d. **This is the sole inferential test for the verdict — unchanged from pre-registration.**
- **Block-bootstrap 95% CI on β** (moving-block, block = 64, 1000 resamples) — descriptive uncertainty, substituting for the pre-reg's `powerlaw.Fit` parametric bootstrap (the `powerlaw` package is unavailable in this numpy-only environment). Does **not** feed the H1 verdict. Logged `confounds.md` §11.
- **IAAFT surrogate β** (100 surrogates × 100 iterations, primary signal only) — reported per §5.4.2; found to be non-degenerate and itself diagnostic of the volume artifact (discussion §5; `confounds.md` §12).

---

## §3 Deviations from the pre-registration (all logged, none affecting the locked H1 test)

| # | pre-registration said | what was done | why | confound entry |
|---|---|---|---|---|
| 1 | BigQuery **or** AWS direct CSV (§5.1) | BigQuery (sandbox/free tier) | canonical path; complete archive | §9 |
| 2 | `powerlaw.Fit` parametric bootstrap CI (§5.4.1) | moving-block bootstrap CI | `powerlaw` unavailable (numpy-only) | §11 |
| 3 | IAAFT surrogate β as "the null" (§5.4.2) | computed + reported as diagnostic | IAAFT β not a clean null for a sub-band slope; non-degenerate in practice | §12 |
| 4 | interpolate <2-day gaps, window >2-day gaps (§5.2.4) | linear-interpolate all missing days, flag counts | gaps are tiny (<0.4%) and segment-windowing breaks the 512-day Welch design | §14 |

The **locked H1 inference** (paired permutation test on Welch-β Δβ across 6 pairs, p<0.05, d≥0.5, Δβ<−0.10) was applied exactly as pre-registered. No test was swapped to change the verdict.

---

## §4 Software & reproducibility

- Python 3.12.9, numpy 2.4.6, matplotlib 3.10.9, google-cloud-bigquery 3.41.0, pydata-google-auth 1.9.1, requests 2.32.5.
- All RNG seeds = 2026 (permutation, bootstrap, IAAFT).
- Re-run: `python bq.py auth` → `python bq.py query --project <ID>` → `python pilot.py --mode gdelt --data-dir data/raw --out-dir results` → `python make_plot.py`.
- Artifacts: `results/gdelt_results.json` (all β / α / CI / p / d / IAAFT, machine-readable), `results/log_log_plot.png` (12-panel Welch PSD), `results/discussion.md`, `results/methods.md`. Raw daily CSVs in `data/raw/` (committed for reproducibility).

---

## §5 Citation anchors

- **DFA:** Peng et al. 1994, *Phys Rev E* 49:1685.
- **Welch PSD:** Welch 1967, *IEEE Trans Audio Electroacoust* 15:70.
- **IAAFT surrogate:** Schreiber & Schmitz 1996, *Phys Rev Lett* 77:635.
- **Power-law fitting / heavy-tail bootstrap:** Clauset, Shalizi, Newman 2009, *SIAM Rev* 51:661 ([arxiv 0706.1062](https://arxiv.org/abs/0706.1062)).
- **LRC-in-text baseline:** Altmann, Cristadoro, Esposti 2012, *PNAS* 109:11582.
- **Data:** [GDELT Project](https://www.gdeltproject.org/data.html); BigQuery `gdelt-bq.gdeltv2.events`.
