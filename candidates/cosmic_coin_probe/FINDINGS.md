# FINDINGS — Cosmic-Coin Probe (`cosmic_coin v0.1`)

**Date:** 2026-06-12 (§1–§11) · **Updated 2026-06-13 — see §12** (GPT-5.x + Gemini external pass: 1 confirmed bug fixed, harness v0.2, the framing demoted to engineering, 6 more dead children; the §1–§11 numbers stand as taken except where §12 supersedes them — notably the "Student-t hurts the orbit" claim is RETRACTED and "render knob" → "engine-calibration band"). · **Status:** coin DIRECTION holds (on bug-independent evidence); magnitude is an engine-calibration band; **12 dead/demoted children on record** · **Adversary:** 4 internal attacks (3 survive, 1 partial, 0 reversals) + external pass

**Register.** This is an exploratory INSTRUMENT (collect → observe → classify), not a confirmatory test. It LOCATES the replay/simulate coin edge as an observable. Nothing here is pass/fail; readings are 0.99-not-Boolean — and this run literally measured the 0.99 (the flare replays at 0.9982 of its moments, §3). No phenomenon is declared fundamentally incompressible: every "fuzzy" reading means *dear under this fair law*, an open invitation to a better law.

## 0. What was scanned

The claim: *the bits a fair law saves compressing a phenomenon = the sharpness of its appearance* (Solomonoff in miniature: p(appearance) = 2^−bits).

| | ORBIT | FLARE |
|---|---|---|
| Data (real, fetched) | Mars heliocentric position, JPL Horizons / DE441, 366 daily epochs (1 yr) | GOES long-band 0.1–0.8 nm X-ray flux, NOAA SWPC, 10,078 one-minute steps (7 days, peak M1.9) |
| Fair law | Pure two-body Kepler from the t₀ state alone (out-of-sample, no fit) | Persistence on log-flux, f̂(t) = f(t−1) |
| Model bits (counted, never zero) | 448 | 64 |
| Quantization (disclosed) | 1 km, 3 dims | 1e-3 dex, 1 dim |
| Expected face | sharp / REPLAY | fuzzy / SIMULATE, bursty at onsets |

Pinned instrument: lzma-9 primary coder (zlib-1/zlib-9/bz2-9/lzma-9-extreme ladder in re-measure and adversary phases); a single fair common Gaussian predictive for both — with the harness docstring explicitly inviting the skeptic to a heavier-tailed flare predictive. The skeptic took it (§5).

## 1. First-class finding — the units constraint (E-units, promoted)

**Absolute bits/step are not comparable across phenomena. Ever.** The probe's own naive absolute appearance gap came out *backwards*: orbit 43.30 bits/step vs flare 6.17, "separation" −37.13 (it sits in `results.json: coin_edge.separation_bits` as a permanent specimen). Cause, fully diagnosed: bits/step = (#dims) × (signal scale vs grid), and every count carries an arbitrary −log₂(q) offset. The orbit buys 3 spatial dimensions on a coarse 1 km grid; the flare 1 dimension on a fine 1e-3 dex grid — so the flare's absolute bits are deflated regardless of how lawful it is.

Adversary verification (`attack_units.py`): four independent unit-strippings all restore the orbit-sharp ordering —

- z-scored to each series' own σ at a common dimensionless quant: ratio-of-CR **5.77× / 2.70× / 1.86×** at q_z = 0.01 / 0.05 / 0.1;
- the exactly q-invariant per-dim σ-shrink: **14.44 vs 3.50 bits/dim**;
- dimensionless R²: **0.99999999 vs 0.9922** (orbit residual ~1.5e4 km on a 2.2e8 km orbit — real, not numerical zero);
- equalized raw entropy at q = σ_raw/256: CR ratio **7.4× (lzma) / 40× (zlib) / 26× (bz2)**.

The sign never flips under any stripping. The absolute-bits gap is the artifact; the dimensionless reading is the signal.

**Instrument rule going forward:** declare the quantization with the run; cross-phenomenon claims only in dimensionless form — ratios, fractions, per-dim shrink (q cancels exactly), or within-series self-normalized statistics. An absolute bit count never crosses a phenomenon boundary.

## 2. The coin reading — dimensionless, cross-phenomenon

Every unit-free measure, every coder, with and without model bits counted, reads ORBIT sharper:

| measure (dimensionless) | orbit | flare | edge |
|---|---|---|---|
| lzma-9 compression ratio raw/resid | 2.46× | 1.27× | 1.94× |
| zlib-9 / bz2-9 CR | 1.92× / 1.97× | 1.44× / 1.29× | 1.33× / 1.53× |
| bits-saved fraction (lzma) | 0.594 | 0.213 | +0.38 |
| Gaussian-floor entropy ratio | 2.12 | 1.57 | 1.36× |
| **q-invariant σ-shrink, bits/dim** | **14.44** (σ ÷ 22,233) | **3.50** (σ ÷ 11.3) | **+10.94 bits/dim** |
| R² of the law | 0.99999999 | 0.9922 | — |

(With model bits counted: 2.37× vs 1.27× → 1.87×; ordering unchanged. Raw lzma totals: orbit 28,288 → 11,488 bits; flare 72,576 → 57,088 — independently recomputed from `series.npz` for this synthesis, exact match to `results.json`.)

Cleanest single sentence: **the Kepler law shrinks Mars's per-dimension appearance uncertainty by 14.4 bits (a σ-factor of ~22,000), while persistence shrinks the flare's by 3.5 bits (~11×)** — an 11-bit/dim edge separation in a quantity where quantization cancels exactly.

Coder ladder (zlib-1 → zlib-9 → bz2-9 → lzma-9 → lzma-9e): ratio-of-CR **1.38 / 1.33 / 1.53 / 1.94 / 2.03** — never inverts; "store" floors both at 1.0. The law does work the coder cannot do alone: it removes 59% / 49% / 48% (lzma/bz2/zlib) of orbit raw bits vs 21% / 22% / 31% for the flare. And lzma *under-credits* the orbit: shuffling the orbit residual ADDS ~8,100 bits, and same-σ pure noise costs 21,056 vs the residual's 11,488 — so the orbit's CR is a floor, and stronger coders should widen, not narrow, the lead.

## 3. The coin reading — per-moment (the refinement)

The coin also flips per MOMENT, and here 0.99-not-Boolean became a measurement:

- **Orbit is the flat face.** Worst day of 366 = 48.86 bits = **1.19× its own mean** (z_max 1.66); **zero** moments past mean+5σ (threshold 64.3 bits); the variation is a smooth 36.4 → 46.1 bits/quarter drift ramp (osculating-element drift accumulating); top 1% of days carry ~1.0–1.3% of bits. Flat means spike-free, not constant.
- **The flare replays 99.82% of its minutes.** Median 5.48 bits (p = 2^−5.48 ≈ 0.022/step); 97.9% of minutes under 10 bits. Quiet sun is the *sharp* face too.
- **It flips fuzzy at 18 onset minutes (7 events):** 61.5–599.5 bits under the pinned Gaussian; 0.18% of moments carrying **5.1% of all bits** (28.6× over-representation); every one a positive-dlogflux brightening; rule-robust against the quiet-sun maximum (53.0 bits) vs onset minimum (61.5 bits).
- Burstiness contrast, orbit ↔ flare: CV 0.112 vs 1.708 (**15.2×**), max/mean 1.19 vs 97.1 (**82×**), p99/p50 1.21 vs 2.64, top-1% bit share ~1% vs 8.36%.
- **Sharpest observation of the run — the coin flips within a single event.** The week's biggest flux moment (M1.9 peak, 1.86×10⁻⁵ W/m²) costs **5.46 bits — below the series median** — while the maximum-surprise minute is a C-class *rise* (+0.50 dex/min, 2026-06-11T08:26Z), 6,865 minutes away from that peak. **The fuzzy face tracks rate-of-change (law-breaking onsets), not amplitude (peaks and decays replay fine).** Solid↔fuzzy is readable per moment — exactly the frame-reversal observable the instrument register predicted.

Magnitude caveat, accepted from the adversary: the 599-bit spike is mostly Gaussian misspecification — the same minute reads ~22.8 bits under a fair Student-t (ν ≈ 2.1), and ~1,193 bits under a quiet-sun-fit Gaussian. The flip PATTERN (onset over-representation) survives; the 2^−599 drama number is demoted (§7, child 2). Per the register these were always "dear under this fair law" moments, never "incompressible" moments.

## 4. The edge, operationally defined

The coin edge is NOT a number in absolute bits. It is a dimensionless observable bundle:

- **E1 — compression edge (cross-phenomenon).** Ratio-of-CR (raw/(resid+model)) under a pinned coder ladder, plus bits-saved fraction — always reported as the band. Current location: 1.33×–2.03× over the coder ladder; saved-fraction 0.594 vs 0.213 under the common Gaussian, tightening to 0.529 vs 0.454 once the flare gets its best fair heavy-tailed predictive. **The magnitude is an ENGINE-calibration band (~1.17× to ~2.8×, set by coder strength and predictive family — both ENGINE dials); only the sign/ordering is the claim-bearing observable.** [corrected 2026-06-13: was "render knob" — coder/predictive are engine dials, so the slip violated the attribution rule; see §12 child 9.]
- **E2 — q-invariant form (preferred single number).** Per-dimension scale shrink log₂(σ_raw/σ_resid): 14.44 vs 3.50 bits/dim (14.4 vs ~4.7 even after the flare's t-upgrade). Quantization cancels exactly — immune to the units trap by construction.
- **E3 — surprise burstiness (per-moment, within-series, self-normalized).** CV, max/mean, p99/p50 of the per-step NLL series; top-1% bit share; count of moments past mean+5σ. E3 locates the edge IN TIME: inside the flare series it sits at positive-rate-of-change onset minutes; inside the orbit series it is absent (zero 5σ moments in 366 days).

Explicitly disqualified as an edge measure: absolute bits/step compared across phenomena (§1).

## 5. Adversary record (4 attacks, 0 reversals)

| attack | result | outcome |
|---|---|---|
| Unit confound | survives (for the coin) | the −37-bit naive gap is the artifact; all four unit-strippings restore orbit-sharp (§1) |
| Misspecification | **partial** | LAW side: persistence already near-optimal among linear flare models (AR(1) 1.257×, EWMA 1.264×, AR(1)-on-increments 1.30×, MA(3–30) worse, vs 1.27×); no flare law reverses. PREDICTIVE side bites: Student-t (ν=2.1) lifts flare saved-fraction 0.21 → 0.454 vs orbit 0.529, collapsing the margin ~2.8× → ~1.17× and deflating the 599-bit spike to 22.8. The same t HURTS the orbit (41 → 71 bits/step: light-tailed residual, Gaussian is its best fair law of those tried) — so the ordering survives on saved-fraction AND on q-free shrink (14.4 vs ~4.7 bits/dim), but the headline magnitude does not |
| Coder erasure | survives | ladder 1.38/1.33/1.53/1.94/2.03 never inverts; the law removes bits the coder cannot find; the orbit CR is a floor (shuffle adds bits), so stronger coders widen the lead |
| Cherry-pick | survives | flare halves/quarters CR 1.09–1.23, all below the orbit's WORST quarter (1.92, vs orbit quarters 1.92–2.72); quiet-sun-only (onsets removed) drops flare CR to 1.21; 3×-amplified onsets drop it to 1.18 (an X-class week would *widen* the gap); the short band (0.05–0.4 nm, same week) is fuzzier still, CR 1.02. Honest limit: n = 1 window per phenomenon |

**Strongest surviving critique, adopted into the edge definition:** the margin is predictive-family- and coder-relative. Report the band (~1.17×–2.8×), never the lzma headline alone. The ordering was un-reversible on every dimensionless measure tried because the same heavy tail that helps the flare hurts the orbit.

## 6. The Solomonoff identity itself (p = 2^−bits)

Tested per-symbol under lzma-9 (coder slack measured, not assumed: 256 bits total container overhead; ~1–2 bits/symbol honest tolerance from int64 byte-packing):

- **Flare (near-iid regime): the identity holds cleanly.** Realized 5.665 bits/symbol inside the bracket [hist 5.049, Gaussian 6.172]; per-symbol probability off by at most ~1.5×. (The sub-0.1-bit decomposition agreement is partly a cancellation — lag-1 autocorr 0.70 gives lzma ~1.0 bit/symbol of temporal structure, offsetting ~1.6 bits of packing slack — so don't over-read it.)
- **Orbit (smooth-drift regime): the identity holds in sandwich form only, and the deviation is diagnostic.** lzma 10.46 bits/symbol BEATS the marginal iid-Gaussian 12.85 by 2.4 bits because the residual is autocorrelated drift (lag-1 = 0.995, still 0.99 after two differencings): innovation-rate proxy 6.53 < lzma 10.46 < marginal 12.85 < shuffled 17.86. The coder finds extra law the disclosed Gaussian appearance does not credit — **the orbit is even sharper than the instrument claims.**
- **The identity-gap sign (orbit −2.39, flare −0.51) is a new dimensionless observable pointing the same way as the coin.**

Instrument quirk logged: the harness orbit NLL is miscentered ~0.88 bits/symbol (resid² against mean-subtracted σ while the residual mean is nonzero drift). Ranking unaffected; fix owed (§9).

## 7. Dead children (the honest falsification gauge)

The parent conjecture stands; six children are dead or demoted, dated 2026-06-12:

1. **Naive absolute-bits appearance gap** (orbit 43.30 vs flare 6.17 bits/step, "−37.13") — RETIRED. Unit confound: dimension×quantization artifact, sign backwards. Never quote it across phenomena.
2. **The 2^−599 onset moment** (599.46 bits, p ≈ 3.5×10⁻¹⁸¹) — DEMOTED to law-relative: ~22.8 bits under fair Student-t (ν≈2.1); ~1,193 under a quiet-sun-fit Gaussian. The magnitude swings two orders with the predictive; only the onset over-representation pattern survives.
3. **lzma 2.8× / 2.37× as "the" margin** — DEMOTED to top-of-band: the edge magnitude is an engine-calibration band spanning ~1.17× (fair t) – 2.03× (lzma-extreme ladder) – 2.8× (lzma saved-fraction ratio). [term corrected 2026-06-13; see §12 child 9.]
4. **Orbit plug-in histogram-entropy "agreement" with lzma** (9.80 vs 10.46 bits/symbol) — INVALIDATED: 87.9% unique symbols; plug-in capped near log₂(n) = 10.1. Undersampling artifact, not identity evidence.
5. **"A quieter flare sub-window would read sharp like the orbit"** — RETIRED: removing onsets LOWERS flare CR (1.27 → 1.21; quiet baseline is quantization-dominated), and 3× onset amplification also lowers it (1.18). No flare sub-window approaches the orbit's worst quarter (1.92).
6. **iid form of the identity for the orbit** (codelength = marginal entropy) — DEMOTED to sandwich/bracket form; marginal entropy is not the entropy rate of a lag-0.995 drift.

## 8. Falsifiers (what would move or flip the located edge)

1. A fair flare law+predictive (out-of-sample, model bits counted, same pinned coder) whose bits-saved fraction exceeds the orbit's — closest approach so far: 0.454 vs 0.529.
2. Ratio-of-CR < 1 anywhere on an extended coder ladder (PPM / context-mixing / neural next) — the shuffle evidence predicts widening instead; an inversion would break the coder-robustness leg.
3. An independent GOES window or channel whose CR exceeds 1.92 (the orbit's WORST sub-window) at the pinned coder+quant.
4. A longer or different orbit arc (or chaotic three-body regime) whose per-step NLL develops mean+5σ moments under its own fair law — would show per-moment flatness was window-luck.
5. Flare onset minutes losing their bit-share over-representation under the fair-t predictive — would erase the per-moment flip observable.
6. Realized codelength exceeding the predictive-entropy bracket by far more than the measured 1–2 bit/symbol coder slack on a near-iid residual — would break p = 2^−bits as the appearance map itself.
7. The q-invariant per-dim shrink reversing (flare > orbit) under ANY disclosed quantization pair — q cancels exactly there, so a reversal would mean unit-stripping had been hiding structure, not revealing it.

## 9. Owed

1. **Cross-model external pass (GPT-5.5 + Gemini) on the load-bearing numbers** — probe, all three re-measures, and the adversary phase were Claude-only; the cross-model pass is the real external check before this synthesis hardens.
2. **Better flare laws, law-side:** regime-switching quiet/onset (HMM), long-memory/ARFIMA, multi-scale — fit out-of-sample, model bits counted. The instrument predicts the gap narrows further but does not flip; that prediction is itself a falsifier.
3. **Symmetric predictive upgrade:** give BOTH phenomena their best fair predictive family selected out-of-sample (the orbit keeps Gaussian only by winning fairly), then re-report the band.
4. **More windows:** ≥3 GOES weeks spanning activity levels (quiet / M / X) and ≥2 more orbit arcs (longer Mars arc; Mercury or a comet as a non-Keplerian stress case). The sign is sub-split-robust; the margin is n=1 — turn it into a distribution.
5. **A mid-coin third phenomenon** (geomagnetic Kp, sunspot number, tides) to show the edge is a continuum locator — a dial, not a two-point contrast.
6. **Harness fixes:** the ~0.88 bits/symbol orbit-NLL miscentering; a Jensen note for the per-axis-sum (81.88) vs mean-σ (85.24) raw-entropy conventions; a docstring rule banning cross-phenomenon absolute bits.
7. **Tighter floors and coders:** a true joint (not iid-marginal) entropy floor; a context-mixing coder as a closer Solomonoff stand-in — predicted to widen the orbit lead; verify.

## 10. Reproduction

All under `D:\PlatformOperator\research\pav\candidates\cosmic_coin_probe\`: `harness.py` (canonical method), `results.json`, `probe_data\series.npz`, raw `probe_data\mars_horizons_raw.txt` + `probe_data\goes_xray_7day.json`; re-measure scripts `coder_robustness_check.py`, `angle_per_moment.py`; adversary scripts `attack_units.py`, `attack_misspec.py` / `attack_misspec2.py`, `attack_coder.py`, `attack_cherry.py`. Headline numbers in this synthesis were independently recomputed from `series.npz` on 2026-06-12 (lzma totals 28,288/11,488 and 72,576/57,088 match `results.json` exactly; σ-shrink 14.44 vs 3.50 bits/dim; flare onset census 18 steps past mean+5σ reproduced).

---

*Reading, in the register it was taken in: the instrument located the coin edge and it is real, dimensionless, and two-layered — between phenomena (Kepler buys ~11 more bits/dim of appearance sharpness than persistence) and within one (the flare replays 99.8% of its moments and flips fuzzy exactly at rate-of-change onsets). The edge's position survived every attack; its width is an engine-calibration band. Nothing here says the flare cannot be compressed further — the misspecification attack already narrowed the gap once, exactly as a better law should, and the next better law is the standing invitation.*
---

## 11. Speculation, out-of-the-box, and the questions we should be asking
*(Added 2026-06-12 per Pav ops note. Register shift disclosed: everything in this section is SPECULATION or open question — nothing here is a finding; nothing is measured unless it cites a section above.)*

**The reframe this section lives under (Pav):** the two faces are the analogy's poles. The instrument does not operate AT the poles — it operates on the **gradient between kernel-canon and phantom-fuzzy**. The probe already measured two dial positions (14.4 and 3.5 bits/dim, §2) and even showed one phenomenon is itself a MIXTURE (the flare: 99.82% replay-mass + 0.18% onset-mass, §3). The dial, not the coin-flip, is the instrument's home.

### Speculations / out-of-the-box approaches

- **S1 — The coupling term is a third specimen (synergy on real physics).** The probe did NOT test orbit↔flare correlation (deliberately — two independent specimens). But the real coupling exists one stage closer to Earth: solar activity → thermospheric density → **satellite drag** → LEO orbit decay. Pull ISS/Starlink TLE history (CelesTrak) + F10.7/Kp indices and ask the synergy question: does the JOINT (orbit-residual + solar-activity) compress better than the parts separately? That is the gain_v2 synergy gate run on real sky data — the weld between our two specimens is itself a phenomenon, and it lives mid-dial. The sharp orbit goes fuzzy BECAUSE of sun weather; the interaction is where the two coin faces touch.
- **S2 — Dial position as the substrate's hardness coordinate.** log2(sigma_raw/sigma_resid) per dim under the best fair law = a measured number per phenomenon. Speculation: this is the missing physical analogue of membrane hardness — wrappers in the cosmic substrate get their sharpness RENDERED from a measured dial position, not an authored confidence. Corollary: sharpness-decay-with-lead-time (how far ahead the law holds: orbit millennia, flare minutes) gives every worldline a measured fuzz-horizon.
- **S3 — Phenomena are mixtures, not points.** The flare result suggests the right object is not a dial POSITION but a DISTRIBUTION over the dial: (replay-fraction, bits-at-the-breaks). Mars = (1.000, none); this flare week = (0.998, 20-600 Gaussian-rendered). Render: kernel-disc radius = replay fraction; membrane spikes = the breaks. This is the L0 membrane partition, measured.
- **S4 — Laws have worldlines too.** Wire the duel as the VERIFIER in a conjecture loop (the AutoScientist organ): generator proposes a law, verifier = held-out bits with model bits counted, dial position MOVES when a better law lands. Saros -> Newton -> GR is three dial-jumps for the same phenomenon. The trace of dial-position-over-time is the history of science for that phenomenon, rendered as an exhaust trail — the lifecycle trace Pav asked for, applied to laws themselves.
- **S5 — The dial's bottom anchor.** At the fuzzy extreme, "lawfully random" (quantum shot noise: the law PREDICTS the distribution and nothing more compresses) is locally indistinguishable from "not yet lawful" (our laws just haven't caught it). Only the TRAJECTORY tells them apart: does the gap keep closing across sweeps, or asymptote? The dead-children tally per phenomenon becomes the discriminator — a phenomenon whose children keep dying at the same dial position is earning its randomness.

### Questions we should be asking

- **Q1 — Is dial position a constant of the phenomenon or of the window?** n=1 window each (§5 cherry-pick attack: sign robust, margin single-window). Does the flare's 3.5 bits/dim drift across the solar cycle (quiet 2019 sun vs active 2026)?
- **Q2 — Where do the COUPLINGS sit?** (S1 operationalized.) Drag, eclipse geometry x flare timing, tide x storm-surge. Is a coupling always fuzzier than its sharpest parent? (Conjecture: yes — interaction terms inherit the worse dial position. Falsifiable.)
- **Q3 — Can dial position be predicted from phenomenon CLASS before measuring?** Do all two-body-dominated systems land near ~14 bits/dim? Is there a taxonomy (integrable / quasi-periodic / driven-dissipative / critical) that predicts the dial to +-2 bits? If yes, the dial is doing physics, not just description.
- **Q4 — Where do LATENT phenomena land on the SAME dial?** The instrument is substrate-agnostic: token streams, market prices, the framework's own commit cadence. Run the identical harness on a latent series and the latent-physics census gets its first measured axis — the bridge between the cosmic program and the latent-physics program, one instrument.
- **Q5 — Is "surprise lives in the first derivative" universal?** The flare flipped fuzzy at RISES, not peaks (§3). Do earthquakes, market crashes, regime changes also break at onsets rather than extremes? If yes, the fuzzy face is universally the DERIVATIVE face — a candidate law OF the dial.
- **Q6 — Is hardness scale-relative (the contextual dial again)?** The flare at 1-min cadence is fuzzy; daily-averaged flux is smoother; the 11-year sunspot cycle at monthly resolution is quasi-lawful. Same phenomenon, different timescale rung = different dial position. If confirmed, hardness is FRAME-RELATIVE in exactly the already-canon contextual-scaling sense — the zoom dial and the hardness dial are the same dial seen twice.


---

## 12. External pass + corrections (2026-06-13)

The first non-Claude review (GPT-5.x via Codex x2 + Gemini, briefed WITH Pav's provenance; `external_pass/SYNTHESIS.md`). Both models, independently: **direction credible, grand framing overclaimed, real code bugs, and the genuine contribution is the dial-protocol engineering, not a new information theory.** All corrections below are append-only (the §1-§11 record stands as taken on 2026-06-12); this section supersedes the specific numbers/terms it names.

### Confirmed bug (recompute-verified) and the harness v0.2 fixes
- **`attack_misspec2.py` orbit Student-t Q-bug** — `nll_t` subtracted the global flare quantization `Q=1e-3` even when called on the ORBIT residual (q=1 km), inflating it by `+3·log2(1000)=+29.9` bits. The "Student-t HURTS the orbit, 41→71" claim (§5 misspecification row) was that artifact. **Fixed; recomputed: orbit Student-t = 41.10 vs Gaussian 41.19 — t is NEUTRAL on the orbit.** Also restored the missing `0.5` Gaussian factor and made quantization an explicit per-call argument (the uncontrolled-turn lesson: never move two dials with one knob).
- **Harness v0.2** (`results.json` now `probe: cosmic_coin v0.2`): per-axis-SUM entropy (was mean-σ ×3 — Jensen overstated the floor); DEBIASED NLL (was uncentered against the ~14,900 km drift mean); σ-shrink emitted with NAMED convention; disclosure fields added; `log_flux_std` renamed to `resid_log_flux_std`. **Deltas:** orbit appearance 43.30→**38.56**, orbit NLL mean 41.19→**38.56**, NLL max 48.86→**40.22** (both bugs had *inflated* the orbit — corrected, it is even sharper). **Unchanged:** the headline σ-shrink **14.44 vs 3.50 bits/dim** (this was already the right convention — per-dim-mean-of-log-ratios; the 13.98 alternative is the Jensen-biased ratio-of-mean-σ, now both emitted and named), the lzma comp-ratio separation **1.87×**, and the flare numbers.

### What the corrections do to the conclusion
**The coin's DIRECTION still holds, but the stated REASON is corrected.** Old (wrong) reason: "the same heavy tail that helps the flare hurts the orbit, so the sign can't flip." Corrected: **t helps the flare (6.17→5.16) and does nothing to the orbit (41.19→41.10) — the orbit leads because its own shrink and saved-fraction are higher, not because t penalizes it.** The direction rests on bug-independent evidence: σ-shrink 14.44 vs 3.50, comp-ratio 2.37× vs 1.27×, and saved-fraction (orbit-Gaussian 0.529 vs flare-best-t 0.454). A symmetric best-fair-predictive upgrade (the owed move) narrows the gap but, on current evidence, the orbit stays ahead.

### Dead children 7-12 (extending the §7 tally; the honest gauge keeps growing)
7. **"Student-t hurts the orbit (41→71)"** — RETRACTED 2026-06-13 (the Q-bug above). The "sign can't flip because t hurts orbit" mechanism dies; the sign holds for a different, correct reason (own-structure lead).
8. **Solomonoff "identity" as literal equality** — DEMOTED to "shared bit-currency (MDL / log-loss)". `p=2^-bits` is exact only for a specified prefix code / predictive; the Solomonoff prior is a universal mixture (`~2^-K(x)`, coding theorem up to machine constants), and lzma is not it. Both externals; prior art: Kolmogorov, Levin coding theorem, Rissanen MDL, Shannon source coding.
9. **"render knob" for the edge magnitude** — RELABELED to "engine-calibration band". Coder and predictive are ENGINE dials, so calling their variance a render artifact violated the attribution rule in the document that introduces it (Codex caught the self-contradiction). Fixed at §4-E1, §7-child-3, the §10 closing reading, and `DIAL_PROTOCOL_SPEC §2`.
10. **"rate-of-change not amplitude" as a general law** — DEMOTED to the narrow frame-relative form. A persistence residual IS the discrete derivative by construction, so surprise must track increments — tautological at this single law-dial setting. Keep only: "for the 1-min univariate persistence frame, flare uncertainty concentrates at positive onsets, not peaks." Generalizing requires the law sweep (HMM/regime-switch), which the instrument predicts will reduce but not erase onset surprise.
11. **The "E-units law" and the active-inference / free-energy "correspondence" as load-bearing claims** — DEMOTED. E-units = the standard non-invariance of differential entropy/codelength under units/quantization/dimension (`h(aX)=h(X)+log|a|`) — a protocol GUARD, not a discovery. Free-energy = a loose POMDP analogy with no formal dependence (the loop never acts on the data stream — the data is passive — so it does no mathematical work *yet*). Per Pav's reframe both are now SETTINGS of the engine `formalism/accounting` dial, each carrying its well-formedness conditions on the record; "decoration" becomes measurable via experiment **A4** (expected-information-gain acquisition vs round-robin — if it wins in held-out bits, the active-inference setting earns its keep).
12. **Harness v0.1 NLL miscentering + Jensen mean-σ entropy** — FIXED in v0.2 (above). Effect: orbit slightly sharper; direction and headline σ-shrink unchanged. (Closes the §6/§9 "owed" items for these.)

### What SURVIVED the external pass (unanimous)
The empirical DIRECTION (narrowly: a strong physical law compresses a smooth integrable system far more than a naive baseline compresses a bursty stochastic one — both externals stress this is an EASY, endpoint-selected contrast), the dimensionless-only discipline (as a guard), and — the unanimous "most defensible genuine contribution" — **the DIAL PROTOCOL as engineering**: provenance-bound append-only trial records, frame/engine/render variance attribution, engine-bands-not-headlines, frame-variance-as-observable, render-wiggle-as-QA (one-way: survival is robustness not truth), dead-child accounting, and the conjecture/verifier boundary. That is the keeper, and it is what to lead with.
