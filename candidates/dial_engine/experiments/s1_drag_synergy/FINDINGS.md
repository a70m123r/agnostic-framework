# S1 — drag x solar synergy: FINDINGS

**Status (2026-06-13): ANTI-SYNERGY verdict; FRAME-FLIP directionally confirmed, mechanism ambiguous.**
Register: exploratory INSTRUMENT, 0.99-not-Boolean. Real fetched data only. No fabrication anywhere in the chain.

---

## 1. The question

Does the JOINT law `density|(F10.7, Dst)` compress held-out thermospheric density more than a properly-specified additive baseline `f(F10.7) + g(Dst)`? The additive baseline is a joint-OLS backfit (gain_v2 discipline: NEVER the naive sum of separately-fitted marginals). Model bits counted. The frame observable: does driver DOMINANCE flip quiet-sun vs storm (Gannon 2024-05-10/11)?

**Framed phenomenon:** GRACE-FO orbit-averaged neutral density, 2024-03-01 to 2024-07-31, hourly. **Inferred:** next-hour held-out log-density, given (F10.7 lags, Dst lags, altitude covariate).

---

## 2. Numbers table (committed, L-med|lin is the anchor cell)

| model | NLL bits total | NLL b/h | LZMA bits | n_params/fit | bits saved vs null/h |
|---|---|---|---|---|---|
| null (intercept + alt + sigma) | 32 308 | 9.034 | 29 792 | 3 | — |
| marginal F10.7 | 30 346 | 8.486 | 29 120 | 7 | +0.549 |
| marginal Dst | 31 922 | 8.927 | 30 272 | 8 | +0.108 |
| additive backfit (F+G) | 30 111 | 8.420 | 29 728 | 12 | +0.614 |
| joint (additive + F107*Dst interaction) | 32 185 | 9.000 | 29 728 | 17 | +0.035 |

**Synergy delta (joint minus additive, L-med|lin):** NLL = **-2073 bits** (-0.58 b/h); 95% CI block-bootstrap L=72h: **[-4457, -468]** — entirely anti-synergy. LZMA delta = 0 (resolution floor). Permutation-floor p95 (DoF correction): -272 bits; observed delta is well inside the anti-synergy tail.

Engine-calibration band (all 6 cells, 3 lag budgets x 2 model families):

| cell | synergy delta NLL (bits) | all-negative? | exceeds perm floor? |
|---|---|---|---|
| L-small\|lin | -1 698 | yes | no |
| L-med\|lin | -2 073 | yes | no |
| L-large\|lin | -2 833 | yes | no |
| L-small\|quad | -10 303 | yes | no (quad cells disqualified storm window) |
| L-med\|quad | -6 468 | yes | no |
| L-large\|quad | -15 537 | yes | no |

Compression gain vs null: F10.7 marginal 6.9%, Dst marginal 2.2%, additive **8.6%**, joint ~0.4%.

---

## 3. Frame-flip numbers (L-med|lin)

| window | n hours | F10.7 b/h | Dst b/h | dominant | ratio |
|---|---|---|---|---|---|
| quiet pre-storm (Mar–Apr 2024) | 1 333 | +0.909 | +0.133 | F10.7 | 6.8:1 |
| quiet all | 3 078 | +0.621 | +0.154 | F10.7 | 4.0:1 |
| Gannon storm week 2024-05-10..16 | 168 | +0.127 | +0.500 | **Dst** | 3.9:1 Dst/F10.7 |
| quiet post-storm (Jun–Jul 2024) | 1 703 | +0.396 | +0.170 | F10.7 | 2.3:1 |
| disturbed other (Dst < -50, non-storm) | 372 | +0.834 | +0.415 | F10.7 | 2.0:1 |

Flip unanimous across all three linear lag configurations. Window-refit corroborates direction (storm Dst less negative than F10.7: -3.93 vs -4.90 b/h). Scale-free partial-corr: storm partial-r(Dst) = 0.850 vs quiet 0.424 — Dst coupling genuinely strengthens in storm (90th pct of 300 random quiet windows). Adversary partial-succeeds: the flip direction is also consistent with pure variance-ratio mechanics (Dst std 7x higher in storm; F10.7 std 0.12x quiet level).

---

## 4. Synergy gate verdict

**ANTI-SYNERGY.** The interaction term costs 1753 bits of data-fit before any model-bit penalty. The additive law is the better compressor in all 6 cells, under leak-free holdout, under AR(1)-whitened scoring (-611 bits whitened), under a purged 60/40 split (-1286 bits). The weld between the two driver parents is ADDITIVE; no multiplicative coupling detectable at this channel resolution and driver-variance regime.

Mechanism: F10.7 nearly constant during the Gannon storm (std = 0.010 log units, range 218–228 sfu); the F10.7 x Dst product term is near-collinear with Dst alone during the one major storm event. VIF(F107*Dst) = 1848. The common-cause hypothesis (both drivers are downstream projections of the same solar active region) is consistent with this structure and with the co-elevation of F10.7 and Dst during the Gannon event.

---

## 5. Philosopher's surviving reframes

**The weld reading.** Anti-synergy is not a failure of the parents-produce-W_C formalism; it is what the formalism predicts when the weld is additive. Each parent law contributes compression independently; the child inherits both membranes. The interaction term attempts to model a weld-coupling not present at this resolution; it finds noise. This is a strong instance of the additive join — the null case of the formalism, which is the hardest baseline to beat.

**Frame-relativity vs regime change.** The flip is consistent with two hypotheses that the data cannot distinguish: (a) frame-relativity — the information budget shifts (Dst unsaturates, F10.7 saturates its contribution), physics unchanged; (b) genuine regime change — coupling coefficients change inside the storm. Separating these requires fitting coefficients with matched driver variances.

**Common-cause (unresolved).** F10.7 and Dst may both be downstream of a single solar-state variable. The anti-synergy result is consistent with this: two projections of a common parent each carry signal, but their product term adds nothing because the parent's structure is already captured additively.

---

## 6. Questions (meditation register)

1. What is the minimum-entropy representation of the common solar-state parent, and does density compress more against that latent parent than against either proxy?

2. The rho1 = 0.983 residual is the loudest number and is treated as a caveat. What law models the residual structure — AR(1), thermospheric relaxation parametric (known timescales: photoionization hours; O/N2 composition days; NO cooling recovery days), or a storm-hysteresis state variable? The current best model explains ~2% of available compression.

3. Is the altitude covariate absorbing the storm signal? The linear static altitude coefficient may systematically mis-correct storm-time orbital contraction. Test: interact altitude with Dst; compare frame-flip ratios.

---

## 7. Speculation (disclosed, out-of-box register)

**Stealth-CME falsification:** Run the gate on Dst storms where F10.7 was NOT co-elevated. DONKI event list https://kauai.ccmc.gsfc.nasa.gov/DONKI/search/ (auth-free REST JSON). If Dst still saves comparable bits in stealth-CME windows, the two-driver framing is vindicated. If Dst marginal collapses without co-elevated F10.7, the common-cause structure dominates. Drop-in experiment using existing instrument and data.

**FISM2 proxy swap:** Replace F10.7 with direct EUV irradiance from LASP LISIRD (https://lasp.colorado.edu/lisird/data/fism_daily_bands/, auth-free, daily). If FISM2 marginal > F10.7 marginal AND synergy delta less negative, the anti-synergy verdict is partly a proxy-quality artifact. This changes the claim lifecycle from dead-child to demoted-pending-better-proxy.

---

## 8. Dead children (dated)

1. "Joint density|(F10.7,Dst) synergizes beyond the additive law" — DEAD 2026-06-13. Reversed in all 6 cells, both scorers, leak-free, autocorrelation-corrected.
2. "The quiet-sun F10.7 dominance is a robust physical signal" — DEMOTED 2026-06-13. Wins only ~55% of random quiet windows; partly variance-ratio artifact.
3. "Quadratic Dst terms improve storm-window fit" — DEAD 2026-06-13. Dst^2 catastrophically overfits Dst = -406 nT; storm-window quad scores uninterpretable.
4. "The additive model is well-specified across all regimes" — DEMOTED 2026-06-13. Storm window additive saves -2.03 b/h (worse than null); O/N2 composition change not modeled.
5. "rho1 = 0.983 invalidates the gate" — DEAD AS STATED 2026-06-13. AR(1)-whitened scoring preserves anti-synergy sign (-611 bits).

---

## 9. Owed

1. Stealth-CME comparison — DONKI REST + existing instrument. Priority HIGH.
2. FISM2 proxy swap — LASP LISIRD daily bands, drop-in column substitution. Priority HIGH.
3. Residual structure decomposition — lag-64 PACF, relaxation parametric, storm-hysteresis test. Priority HIGH.
4. Matched-variance flip test — separate frame-relativity from regime change. Priority MEDIUM.
5. Composition state variable — add O/N2 proxy or Wu et al. 2026 Jp^T index. Priority MEDIUM.
6. Hemisphere stratification — re-bin raw 10-s GRACE-FO files by N/S hemisphere. Priority MEDIUM.
7. Synthetic calibration — verify gate recovers known synergy magnitudes on synthetic data before claiming validation. Priority MEDIUM.

---

## 10. Provenance and reproduction

Data (real, no fabrication, data.real = true for all records):
- Thermospheric density: TU Delft thermosphere portal, GRACE-FO 1 version_02c, accelerometer-derived, CC BY 4.0. Reference: Siemes et al., J. Space Weather Space Clim. 2023. 1 312 801 raw 10-s rows, flag==0.
- Solar/geomagnetic drivers: NASA SPDF OMNI2 hourly, omni2_2024.dat. 8784 rows, zero fill-value contamination in study window.
- Aligned CSV: D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/s1_drag_synergy/data/s1_aligned_hourly.csv, n=3672 grid hours, n_valid=3576.

Scripts: fetch_align.py, synergy_gate.py. Committed results: synergy_gate_results.json.

Normalization: orbit-average channel (column 10 of TU Delft file). Mitigates within-orbit LST/altitude aliasing. Does NOT correct secular orbit decay or storm-time altitude contraction (20.5 km spread, scale height ~60-70 km; ~25-35% density variation — altitude included as linear covariate in every model including null).

Key caveats: F10.7 outlier 2024-07-30 (412.9 sfu) capped at 300 sfu; F10.7 > 200 sfu for 1200/3672 hours; F10.7 co-elevated during Gannon main phase; hemispheric asymmetry not controlled; single 24-hour density gap 2024-07-12/13 excluded.

Fresh literature scan: 17 references, 10 design changes incorporated, 10 confounds registered. No prior PID/synergy application to thermospheric density found in the literature — no external benchmark for expected synergy magnitude in this domain.