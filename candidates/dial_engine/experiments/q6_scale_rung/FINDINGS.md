# Q6 — scale-rung experiment (dial-protocol sweep-1): is hardness scale-relative?

**Status (2026-06-13): naive child REFUTED; parent Q6 REFINED and sharpened to a mechanism.** Under the persistence law on the real committed GOES week, coarsening the time cadence DESTROYS the flare's lawfulness rather than revealing it — the exact opposite of the "fuzzy-at-fine becomes lawful-at-coarse" conjecture — and the destruction has a closed-form mechanism (lag-1 autocorrelation). The refutation is LAW-RELATIVE: a fairer coarse-scale law finds the same flare still lawful when coarsened. Register throughout: exploratory INSTRUMENT (collect -> observe -> classify), 0.99-not-Boolean, dimensionless-only cross-series (E-units), no fabrication — flare is the real committed GOES week; noise/AR(1) are seeded synthetic CONTROLS, never read as data.

## Parent and child

- **Parent conjecture (Q6):** the hardness dial and the contextual-zoom dial are coupled — possibly "the same dial seen twice."
- **Child (this experiment):** the naive direction — a phenomenon that is fuzzy minute-to-minute becomes lawful when viewed coarse, so compressibility should RISE as the scale-rung frame dial coarsens.

## Instrument (pins)

`scale_rung_instrument.py`: GOES long-band (0.1-0.8 nm) X-ray flux, 2026-06-05T14:13Z to 2026-06-12T14:10Z, n=10078 at 1-min cadence; log10 series, quantization Q=1e-3 (disclosed); law = persistence f_hat(t)=f(t-1); coder = lzma-9 primary (zlib-9 / bz2-9 siblings); model bits counted (+64); rungs r = 1/2/5/10/30/60 min by BOTH mean-aggregation (variance-reduction confound, by design) AND decimation (every r-th sample, no averaging — the claim-bearing channel); observables: comp-ratio raw/(resid+model) and per-dim sigma-shrink log2(sig_raw/sig_resid), both dimensionless. Controls, matched length, seeded rng(0): iid noise (structureless floor), AR(1) a=0.9 (known-memory reference).

## What the instrument read (committed, lzma-9, decimate)

| rung (min) | n | flare comp | flare shrink (bits) | flare rho1 | noise comp | ar1 comp |
|---|---|---|---|---|---|---|
| 1 | 10078 | **1.270** | +3.502 | 0.996 | 0.951 | 1.031 |
| 2 | 5039 | 1.080 | +2.594 | 0.986 | 0.950 | 1.011 |
| 5 | 2015 | 0.992 | +1.607 | 0.946 | 0.950 | 0.980 |
| 10 | 1007 | 0.966 | +1.063 | 0.885 | 0.941 | 0.948 |
| 30 | 335 | 0.960 | +0.462 | 0.734 | 0.959 | 0.930 |
| 60 | 167 | **0.914** | **-0.014** | 0.484 | 0.886 | 0.922 |

Mean-method flare comp runs 1.270 / 1.096 / 1.002 / 0.959 / 0.966 / 0.967 — same shape. The curve the child needed (rising with rung) appears nowhere; the observed curve is a monotone collapse from a decisive fine-scale edge into the structureless floor.

## Verification (three independent re-measurements + adversarial pass, all real computation)

1. **Coder/shrink robustness** (`q6_coder_robustness.py`): committed JSON reproduces bit-for-bit (0 mismatches). Fine-end edge under every coder — flare/ar1/noise at rung 1: lzma 1.270/1.031/0.951, zlib 1.439/1.079/0.950, bz2 1.285/1.084/0.953 — so the committed 1.27x is the CONSERVATIVE value and the ordering flare > ar1 > noise is unanimous. Decay monotone under all coders and both methods; flare-minus-noise gap <= 0.013 by rung 30 everywhere. Floor-ARRIVAL is coder-dependent (lzma rung 10; zlib/bz2 rung 30-60) — coder-robust phrasing: "at the floor by 30-60 min."
2. **Error bars** (`verify_bootstrap.py`, moving-block bootstrap B=400, L=120 min): rung-1 comp 1.173 [1.141, 1.204] (point 1.270; bootstrap downward-biased because block joins break persistence — L-sweep 60->600 climbs 1.154->1.200 toward the point), iid floor 0.953 [0.945, 0.959] fully separated. Paired within-replicate decay rung1-rung10 = +0.217 [+0.180, +0.252], rung1-rung60 = +0.237 [+0.178, +0.288] — the decay is real, not floor wander. Coarse rungs 10/30/60 CIs OVERLAP the noise band (rung 5 straddles). Step-resolution: only 1->2 and 2->5 individually significant; coarser adjacent steps n.s. (n shrinks to 167). No-replacement permutation 1.223 [1.194, 1.252] — not an lzma duplicate-block artifact.
3. **Mechanism** (`autocorr_mechanism.py` etc.): see below — identity confirmed to RMS 0.006 bits across all 36 cells; re-verified again in this synthesis pass directly from the raw GOES file (error <= +0.012 bits at every rung).
4. **Adversarial pass** (`opus_skeptic.py`, 4 attacks): NOISE-FLOOR WANDER partial — 200-seed null gives rung-1 z=+89.8 but rungs 30/60 absolutes are INSIDE the cloud (z=+1.69 / -0.75); the load-bearing observable is the collapse (5-15x within-null decay), not coarse-end values. FINE-LAW-BY-CONSTRUCTION partial and STRONGEST — see law-relativity below. WINDOW-TOO-SHORT survives as scoped: toyB (dominant 2-day sinusoid) IS seen at coarse rungs by this very instrument (1.142 -> 1.044, far above floor), toyA (subdominant coarse) is buried; tau ~532 min => ~19 independent samples in 7 days; 27-day/11-yr laws have 0 cycles. MEAN-vs-DECIMATE survives cleanly: the iid floor RISES under mean (0.952 -> ~0.99, the smoothing confound is real) but stays FLAT under decimate (0.952 -> 0.929), and the refutation rides on decimate; sigma-shrink (coder-free, n-independent) and tile-padding to n>=10000 both preserve the decay — variance-reduction and n-shrinkage ruled out three independent ways.

## Mechanism: the persistence-lawfulness IS lag-1 autocorrelation

For the first-difference law, Var(resid) = 2*sigma^2*(1-rho1), so per-dim sigma-shrink = -0.5*log2(2(1-rho1)) — an algebraic identity, and the data sits on it: RMS error 0.006 bits (max 0.017, Pearson 0.999996) across all 36 cells; independent spot-check from raw data in this pass, error <= +0.012 bits per rung. Decimation drives rho1 toward 0 (flare 0.996 -> 0.484; AR(1) follows its theoretical 0.9^r: 0.900/0.808/0.578/0.348 vs predicted 0.900/0.810/0.590/0.349; noise pinned ~0), and shrink is a perfect monotone of it (Spearman 1.000). The compress/expand crossover sits exactly at rho1 = 0.5: the flare compresses through rung 30 (rho1=0.734, +0.462 b) and flips to expansion at rung 60 (rho1=0.484, -0.014 b). "Falling to the floor" = "lag-1 memory crossing 0.5." Two forced refinements: the flare is NOT a single AR(1) (multi-timescale: 0.996^60 predicts rho=0.788 at rung 60 vs actual 0.484; the inline "tracks AR(1) almost exactly" was lzma floor-saturation, with the fine ends significantly separated, 1.270 vs 1.029 [1.024, 1.034]); and "falls to the iid floor" is exact only in coded bits — coder-free, the 60-min flare lands at the ZERO-GAIN line (rho1~0.48), not the iid floor (rho1=0): the persistence EDGE is annihilated, but measurable memory remains at hourly cadence.

## Law-relativity (the strongest surviving critique, kept as a finding)

Persistence f(t)=f(t-1) is a 1-step operator by construction, so "its edge lives at fine scale" is near-tautological — refuting "coarse = more lawful" with ONLY this law is partly circular. The adversary's coarse-law battery confirms the flare itself HAS coarse-scale structure that persistence cannot monetize: a window-mean slow-trend law keeps it compressible at EVERY window 5-720 min (1.085 -> 1.006, never reaching the 0.93-1.0 floor; noise control pinned ~0.99); lag-r persistence ticks back UP at long lag (0.890 at 30-min lag -> 0.926 at 120/240-min); and the decimated flare beats its same-marginal shuffle at ALL rungs including hourly (shuf/raw 1.52 / 1.39 / 1.24 / 1.17 / 1.09 / 1.07). So the correct scope is: **under the persistence law, the flare's persistence-edge is fine-scale memory that coarsening destroys** — not "the flare's lawfulness is fine-scale, full stop."

## What the data licenses (0.99-not-Boolean)

- Hardness is NOT scale-invariant: the rung dial moves compressibility decisively and reproducibly (paired drop +0.237 [+0.178, +0.288]; 5-15x null wander).
- For the persistence law the direction is OPPOSITE the naive child: lawful at fine, floor at coarse — with error bars, under 3 coders, 2 coarsenings, coded and coder-free.
- The mechanism is exact and closed-form for this law family (the rho1 identity).
- The same flare is STILL lawful when coarsened under a fair coarse-scale law — scale-relativity of hardness is a property of the (law, phenomenon, rung) triple, not of the phenomenon alone.

NOT licensed: coarse-end absolute comp-ratios (inside the noise cloud); any claim about 27-day/11-yr coarse laws (unsampled, ~19 independent samples in window); week-to-week generality (within-week error bars, single control seed).

## The coupled-dials reading (zoom vs hardness)

The Q6 parent asked whether the hardness dial and the contextual-zoom dial are "the same dial seen twice." Verdict: **COUPLED, NOT THE SAME DIAL.** The coupling is tighter than conjectured — for a fixed law, zoom moves hardness deterministically through a derived linkage (rung -> rho at the law's lag -> hardness via the identity; Spearman 1.000) — but the gearing is law-indexed in SIGN: persistence law => harder when zooming out (1.270 -> floor); window-mean law => lawful at every window (1.085 -> 1.006); dominant slow signal (toyB) => lawful at coarse under the very same instrument (1.142 -> 1.044). Hardness can rise OR fall with zoom depending on where the law's structure lives relative to the rung. One dial seen twice would fix the correspondence; the data shows two dials joined by a gearbox whose sign is set by the (law, phenomenon) pair. Refined Q6: hardness = f(phenomenon, law, rung) — zoom is an argument of hardness, not its alias; the weak form of "same dial" that survives is that neither dial can be read without setting the other.

## Dead children (dated tally — demoted/dormant, not erased)

1. **naive-coarse=more-lawful** (persistence law + 7-day window) — DEAD 2026-06-13. Direction reversed with error bars, unanimous across coders/methods/observables.
2. **"tracks the AR(1) control almost exactly"** — DEAD AS STATED 2026-06-13. Floor-coincidence under lzma saturation; fine ends significantly separated; flare multi-timescale vs single-exponential control.
3. **"at the iid floor by 10 min"** — DEMOTED 2026-06-13. Coder-dependent arrival (lzma 10 / zlib+bz2 30-60); coarse absolutes inside the noise cloud; coder-free endpoint is the zero-gain line, not the iid floor.
4. **"the flare's lawfulness IS fine-scale memory"** (phenomenon-level) — DEAD AS GENERALIZATION 2026-06-13; survives law-scoped as "the flare's persistence-EDGE is fine-scale memory."

Surviving children: scale-relativity of hardness (sharpened, sign-indexed by law); the rho1 identity mechanism; the decimate-vs-mean confound control (worked exactly as designed — the mean floor inflated, the decimate floor stayed flat).

## Owed

1. **Longer GOES window** — >=60-90 days (2-3 solar rotations) for the 27-day law; archival multi-year for the 11-yr cycle. toyB/toyA establish the instrument sees DOMINANT coarse signal and misses SUBDOMINANT — so the longer window is a real test, not a formality.
2. **Coarse-scale law candidates as committed instruments** — promote the adversary's battery: window-mean/slow-trend law, rung-matched lag-r persistence, same-marginal shuffle gap as a standard observable.
3. **The orbit at coarse rungs** — the lawful-at-all-scales reference series, anchoring the flat end of the zoom-hardness gearing for cross-series comparison (dimensionless, E-units).
4. **Lag-matched "zooming law" sweep** — let the law's lag scale with the rung; if hardness goes flat, the residual scale-relativity was law-lag mismatch. Cleanest direct probe of the same-dial question.
5. **Seed sweep + week generality** — controls currently single-seed rng(0); 200-seed null exists only for lzma/decimate; error bars are within-week only.

## Artifacts

All under `D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/q6_scale_rung/`: `scale_rung_instrument.py`, `scale_rung_results.json` (committed, reproduces bit-for-bit), `q6_coder_robustness.py` + `q6_coder_robustness_results.json`, `verify_bootstrap.py`, `autocorr_mechanism.py`, `autocorr_tests.py`, `autocorr_final.py`, `autocorr_mechanism_rows.json`, `opus_skeptic.py`. Data: `../../../cosmic_coin_probe/probe_data/goes_xray_7day.json` (real GOES week, 2026-06-05 to 2026-06-12, long-band n=10078). Controls are clearly-labelled seeded synthetics; no fabricated measured bits anywhere in the chain.