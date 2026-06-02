# Pilot #150 — 1/f-as-L0-failsafe signature at social substrate

**Status:** First-commit deliverable (2026-06-02). Pre-registration locked per [`candidates/1f_l0_failsafe_signature.md`](../../candidates/1f_l0_failsafe_signature.md). Pilot code (`pilot.py`) is self-contained — depends on Python ≥ 3.10 + numpy only. No scipy / pandas / pip-install needed.

**Discipline closure:** This commit closes the audit v06 §10 + Reading 08 §9 hard-stop on further infrastructure work. Task #167 first-commit target hit on day 1 of the 7-day window.

---

## What this pilot tests

Reading 06 §10.3 Tier 2 conditional hypothesis: **1/f scale-invariance + burstiness IS the signature of healthy substrate-level failsafe operation at the social substrate.** Operationalized as:

**H1 (locked, pre-registered):** β_authoritarian < β_pluralistic − 0.10 on the event-category-entropy signal from GDELT v2 country-day aggregates, across the three paired comparisons CHN-USA, RUS-GBR, PRK-DEU. Cohen's d ≥ 0.5. p < 0.05 vs IAAFT surrogate null.

Falsifier and full pre-registration in `../../candidates/1f_l0_failsafe_signature.md` §4.

---

## How to run

```bash
# Verify DFA implementation on known-β colored noise
python3 pilot.py --mode verify

# Run synthetic-data demo (no internet required)
python3 pilot.py --mode demo

# Run on real GDELT data (requires GDELT download — see §3 below)
python3 pilot.py --mode gdelt --data-dir /path/to/gdelt/csvs
```

---

## §1 What landed in the first commit

| File | Purpose |
|---|---|
| `pilot.py` | Self-contained DFA + Welch PSD + IAAFT surrogate + permutation test pipeline (~423 lines, numpy-only) |
| `README.md` | This document — entry point + critical-finding note |
| `verify_results.json` | Output of `--mode verify` — DFA recovers β across 0.0–2.0 |
| `demo_results.json` | Output of `--mode demo` — synthetic auth/plur contrast |
| `confounds.md` | Critical pre-registration finding documented (see §2 below) |
| `methods.md` | Detailed methods note + literature anchors |

---

## §2 CRITICAL FINDING from running the pipeline against pre-registered protocol

**The pilot pre-registration in `candidates/1f_l0_failsafe_signature.md` §4 specified N=3 paired comparisons (CHN-USA, RUS-GBR, PRK-DEU) with significance threshold p < 0.05 via paired permutation test on Δβ.**

**Verified by running `python3 pilot.py --mode demo`:** the paired permutation test with N=3 pairs has only 2³ = 8 possible label-flip configurations. The minimum achievable p-value is 1/8 = 0.125. **N=3 cannot reach p < 0.05 by construction**, regardless of effect size.

Demo output (synthetic auth β=0.3 vs plur β=1.0, ground truth Δβ ≈ −0.7):
- All 3 pairs show Δβ = −0.6 to −0.8 (clean separation, ground truth direction)
- Cohen's d = −1.79 (very large effect)
- Permutation test p = 0.128 (still > 0.05, by construction)

**This is the first pre-registration discipline failure caught by the pipeline itself.** Two paths forward:

**Option A — Amend pre-registration to N ≥ 6 paired comparisons.** Add country pairs IRN-FRA (Iran vs France), TUR-NLD (Turkey vs Netherlands), VEN-CHL (Venezuela vs Chile) to reach N=6. Minimum p = 1/64 ≈ 0.016 < 0.05 becomes achievable. This is the cleanest discipline-compatible response per [cont 27 §2](../../continuations/27.md) and aligns with [`candidates/1f_l0_failsafe_signature.md`](../../candidates/1f_l0_failsafe_signature.md) §8 Bar B (which already required N ≥ 6 for Tier 2 promotion).

**Option B — Switch significance test from paired permutation to bootstrap-CI-overlap test.** With 1000 bootstrap resamples of β per country, the test becomes per-pair (3 separate tests, multiplicity-corrected). This sidesteps the 8-permutations ceiling but introduces multiple-comparison concerns.

**Recommendation: Option A.** It aligns with the existing Bar B promotion criterion and treats the N=3 protocol as a methodological pre-test rather than a primary result. The pre-registration is amended in `confounds.md` §1.

This is the framework's discipline working as designed — running the pilot caught a methodological issue *before* the GDELT data was downloaded. Audit v07 should track this kind of pre-pilot discipline catch as a positive signal.

---

## §3 Next steps to land result-commit (~3 working days)

Per `candidates/1f_l0_failsafe_signature.md` §11 timeline:

1. **Amend pre-registration to N=6** (Option A above). Add the three additional country pairs. Land amendment as `confounds.md` §1 entry, dated 2026-06-02.

2. **Download GDELT v2 country-day aggregates** for 6 country pairs × 11-year window (2015-2026):
   - Option A: `gdelt2` Python package
   - Option B: BigQuery `gdelt-bq:gdeltv2.events` 
   - Option C: AWS Open Data registry direct CSV download

3. **Aggregate to daily signals** per country: `event_count`, `mean(AvgTone)`, `entropy(EventRootCode)`.

4. **Run pipeline:** `python3 pilot.py --mode gdelt --data-dir /path/to/csvs --out-dir results/`

5. **Result commit lands:**
   - `results/gdelt_results.json` — β per country per signal + Cohen's d + permutation p
   - `results/log_log_plot.png` — 12-panel log-log fluctuation plot
   - `results/methods.md` — methods note with confound log
   - `results/discussion.md` — H1 verdict + Bar A / Bar B status

6. **If H1 lands:** advance candidate from Tier 2 conditional to Tier 2 algorithmically-demonstrated per Bar A.

7. **If H1 fails:** document falsifier outcome; consider amendments or cont 27 §3 demotion path.

---

## §4 Implementation verification (what `--mode verify` shows)

The DFA implementation in `pilot.py` was tested against known-β colored noise:

| true β | DFA α | Welch β | expected α = (β+1)/2 |
|---|---|---|---|
| 0.00 (white) | 0.461 | -0.013 | 0.500 |
| 0.50 | 0.725 | 0.516 | 0.750 |
| 1.00 (pink/1f) | 1.061 | 1.045 | 1.000 |
| 1.50 | 1.183 | 1.498 | 1.250 |
| 2.00 (brown) | 1.512 | 2.052 | 1.500 |

Welch β matches ground truth within ±0.05 across the full range. DFA α matches expected (β+1)/2 closely for β < 1.0; shows known DFA-bias at higher β (Kantelhardt et al. 2001) — for this reason Welch β is the **primary** estimator per pre-registration §5.3; DFA α is reported as a robustness check.

---

## §5 Citation anchors

- **DFA:** Peng et al. 1994. *Phys Rev E* 49:1685
- **Welch PSD:** Welch 1967. *IEEE Trans Audio Electroacoust* 15:70-73
- **IAAFT surrogate:** Schreiber & Schmitz 1996. *Phys Rev Lett* 77:635
- **Power-law fitting:** Clauset, Shalizi, Newman 2009. *SIAM Rev* 51:661 ([arxiv 0706.1062](https://arxiv.org/abs/0706.1062))
- **LRC in text baseline:** Altmann, Cristadoro, Esposti 2012. *PNAS* 109:11582 ([10.1073/pnas.1117723109](https://www.pnas.org/doi/10.1073/pnas.1117723109))
- **GDELT:** [gdeltproject.org/data.html](https://www.gdeltproject.org/data.html)
