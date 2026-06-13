# S1 drag×solar synergy — OPUS SKEPTIC pass (2026-06-13)

Register: exploratory INSTRUMENT, 0.99-not-Boolean, real fetched data only, model bits counted, held-out by time blocks. The DATA seat (fetch_align.py + provenance) is honest and solid; the gain_v2-disciplined gate (synergy_gate.py) **had not been run** before this pass — no `synergy_gate_results.json` existed. I ran it, then attacked it on the saved aligned data (`data/s1_aligned_hourly.csv`, n=3672 h, n_valid=3576 after MAX_LAG=72 + density gap).

## Headline reversal
**The synergy gate FAILS in every cell.** Joint `density|(F107,Dst)` compresses held-out density *worse* than the proper additive backfit `f(F107)+g(Dst)`:

| cell | dNLL (joint−add, +model bits) | data-only dNLL | exceeds perm-floor? | dLZMA |
|---|---|---|---|---|
| L-small\|lin | **−1698** | −1506 | no | −672 |
| L-med\|lin | **−2073** | −1753 | no | +0 |
| L-large\|lin | **−2833** | −2321 | no | −1408 |
| (quad cells) | −6468…−15537 | −6148…−15025 | no | −864…−1760 |

All 6 cells dNLL<0; **0/6 exceed the permutation (DoF) floor**. The loss is in *data-only* bits too, so it is not merely a model-bit penalty — the cross term genuinely degrades held-out prediction. Mechanism (train/test decomposition, L-med|lin): the F107×Dst interaction buys **+0.082 b/h in-sample but −1.065 b/h out-of-sample** — textbook overfit; it fits training noise.

## Attack results
1. **Collinearity/common-cause — SURVIVES (favors proponent).** corr(F107,Dst)=−0.12; among Dst<−50 h, F107 mean 200 vs 182 overall (mild storm-clustering). Synergy is not raw double-counting. Moot anyway: the gate already finds *no* synergy.
2. **DoF/model-bits — SURVIVES.** Loss holds in data-only bits and under a permutation-shift DoF floor (joint never beats floor p95). Honest accounting does not rescue a positive synergy because there is none to rescue.
3. **Lags — SURVIVES.** Additive G and interaction X use the SAME Dst lag set {0,3,6,12,24}h. Giving additive 5 EXTRA Dst lags changes nothing material (−58 data-bits); the cross term still hurts (−1695). Lags are not the (absent) synergy's source.
4. **Physical confounds — PARTIAL.** alt_s is a covariate in every model incl. null (corr(alt,logρ)=−0.05, weak). log-transform applied. BUT storm-time composition change (O/N₂, thermosphere literally re-composes in storms) is a real "wrong model class" concern that this design cannot address — disclosed, not solved. Does not change the verdict; would only further explain *why* one smooth law + interaction fails in storms.
5. **Leakage — SURVIVES.** Reran with a purged contiguous 60/40 split (168-h purge gap, τ≈22h): dNLL still −1286 (lin) / −743 (quad). Parity-by-alternate-weeks did not manufacture the result.
6. **The FLIP — PARTIAL / largely variance-ratio.** Storm-week F107 spans **16 sfu** (std 0.010 in log) vs Dst **472 nT** (std 0.98); quiet F107 spans 301 sfu vs Dst 123 nT. The "bits-bought" flip (quiet F107-dom, storm Dst-dom) is mechanically the driver-that-moves. Scale-free partial-corr (alt removed, each driver own best lag): quiet F107 0.720 / Dst 0.424; storm F107 0.564 / Dst **0.850**. So Dst's coupling *genuinely strengthens* in storm (90th pct of 300 random quiet windows) — that half is real. But F107-dominance in quiet is NOT robust (F107 wins only ~55% of random quiet windows; Dst-dom appears in 45%), and the F107 storm number rests on near-zero dynamic range. A CLEAN flip needs a storm window where F107 *also* varies — 2024-05 does not provide one.

## Robustness of the reversal
The rho1≈0.98 residual autocorrelation makes the raw iid-Gaussian NLL an invalid codelength (over-counts). Under AR(1)-whitened honest codelength the magnitude shrinks but the **sign is unchanged**: dNLL −611 (lin) / −1028 (quad). The reversal is robust to the autocorrelation confound and to the leakage confound.

## strongest surviving critique
The reversal itself: under the proponent's own properly-disciplined gate, the joint law does NOT beat the proper additive baseline on held-out density — across all lag budgets, both families, both scoring channels, leak-free splits, and autocorrelation-corrected scoring. The headline "two drivers synergize" is not supported; the additive law `f(F107)+g(Dst)` is the better compressor, and the F107×Dst interaction is an overfit.

## reversed_any: YES
The driver-DOMINANCE FLIP is the only directional finding that partly survives, and it survives only PARTIALLY (the Dst-strengthens-in-storm half is real; the F107-dominates-in-quiet half and the magnitude are a variance-ratio artifact). The primary synergy-gate claim is REVERSED.

Artifacts: `synergy_gate_results.json` (now generated). Battery run inline (AR1-whiten, purged split, lag-enrich, scale-free flip, flip-null, train/test) — real computation on the cached CSV, no fabrication.
