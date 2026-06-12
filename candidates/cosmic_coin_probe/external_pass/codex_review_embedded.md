OpenAI Codex v0.125.0 (research preview)
--------
workdir: D:\PlatformOperator\research\pav
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ebdfd-befb-7261-84c5-f9734c582625
--------
user
IMPORTANT: This machine's shell is locked (ConstrainedLanguage PowerShell); any tool/shell/file-read calls WILL be rejected by policy. Everything you need is embedded in this message. Do NOT attempt any shell or tool calls. Read the briefing and the embedded files below, then output your written external review as TEXT ONLY.

EXTERNAL REVIEW REQUEST -- the "cosmic-coin" arc (2026-06-12)
Pure-ASCII briefing. You are an independent, skeptical external reviewer. Do NOT be agreeable; your value is independent judgment. Where this restates known prior art, name the prior art specifically. Where it breaks, say so. Where (if anywhere) it is genuinely novel, say that too, narrowly.

=== PROVENANCE (read this first; it is the point) ===
This is a research collaboration. The INTUITIONS below are the human collaborator's (call him Pav, the originator) -- the coin, "derive the probability of what it looks like", "render in log2", the multiple-dials taxonomy, "frame is the sim of observer wrapper and plane / engine is the action space / viewer is an inference of the percept", and the substrate-as-reflected-light reading. An AI assistant (Claude/Fable) did the FORMALIZATION, built the harness, ran the probe, and ran a Claude-only adversarial workflow. EVERYTHING so far has been judged by Claude models only. You (GPT-5.x via Codex / Gemini) are the FIRST non-Claude eyes. We want to know where you land -- especially where Claude may have been too agreeable with itself.

The broader program: a "world-substrate" that is a REPRESENTATION where things are sharp/hardened (replay measured data) and a SIMULATOR where things are fuzzy (generate from a model), with the switch gated by compressibility. Built on a provenance'd, append-only fact-substrate (real fetched data, no fabrication; every claim Tier-3, nothing promoted to canon).

=== THE ARC (what to assess) ===

(1) THE COIN. A phenomenon's appearance is sharp where a short law compresses it (replay the law) and fuzzy where no short law fits (sample from a model). Pav's phrasing: "not calculate but derive the probability of what it looks like, and derive from that." Claim made: this is Solomonoff/algorithmic probability, p(appearance) = 2^-(bits of shortest description), so "derive the probability" and "render in log2" are the same statement, and it is the same bit-axis as MDL model selection.

(2) THE PROBE (the empirical test; files: candidates/cosmic_coin_probe/FINDINGS.md, harness.py, results.json, and the attack_*.py / *_check.py agent scripts). Two REAL datasets:
  - ORBIT: Mars heliocentric position, JPL Horizons / DE441 ephemeris, 366 daily state vectors (2024). Law = pure two-body Kepler propagated from the t0 state vector ALONE (osculating elements at epoch 0 -> predict all later epochs; strictly out-of-sample, no fit). Residual = what two-body misses.
  - FLARE: GOES-18 long-band (0.1-0.8nm) X-ray flux, NOAA SWPC, 10078 one-minute steps (real week, peak M1.9). Law = persistence on log-flux (f_hat(t)=f(t-1)).
  Instrument: pinned lzma-9 coder (zlib/bz2 as siblings), disclosed quantization (1 km positions; 1e-3 dex log-flux), model bits counted, a common Gaussian predictive (Student-t tried by the adversary).
  RESULT (Claude-internal, after a 4-attack Opus adversary, 0 reversals): the coin DIRECTION holds -- orbit reads sharper/more-compressible than flare on every DIMENSIONLESS measure -- but the MARGIN was demoted to a render band. Key numbers:
    * q-invariant per-dimension sigma-shrink (quantization cancels exactly): log2(sigma_raw/sigma_resid) = 14.4 bits/dim (Kepler/Mars) vs 3.5 bits/dim (persistence/flare).
    * lzma compression ratio raw/resid: 2.46x (orbit) vs 1.27x (flare); ordering never inverts across zlib-1..lzma-9-extreme (ratio-of-ratios 1.33x-2.03x).
    * bits-saved fraction: 0.594 vs 0.213 (Gaussian); 0.529 vs 0.454 after giving the flare a fair Student-t (nu~2.1) predictive -- the SAME heavy tail that helps the flare HURTS the light-tailed orbit (41->71 bits/step), which is the stated reason the sign cannot flip.
    * R^2 of the law: 0.99999999 (orbit) vs 0.9922 (flare).
    * PER-MOMENT (the "gem" finding): orbit per-step surprise is flat (max/mean 1.19, zero moments past mean+5sigma in 366 days). Flare replays at 99.82% of minutes (median 5.48 bits) and spikes at 18 onset minutes (7 events). Crucially the spikes track RATE-OF-CHANGE not amplitude: the week's M1.9 flux PEAK costs 5.46 bits (below median, replays), while the max-surprise minute (599 bits Gaussian-rendered, ~22.8 under fair t) is a C-class RISE (+0.50 dex/min).
    * DEAD CHILDREN tallied (honest demotions): (a) the naive ABSOLUTE bits/step gap came out BACKWARDS (orbit 43 > flare 6 bits/step, "separation" -37) because absolute bits = dims x (scale/grid) with an arbitrary -log2(q) offset -> promoted to an "E-units law": cross-phenomenon comparisons are valid ONLY dimensionless. (b) the 2^-599 onset drama demoted to law-relative (22.8 bits under fair t). (c) the lzma 2.8x margin demoted to top-of-a-render-band. (d) orbit histogram-entropy "agreement" invalidated as undersampling. (e) "a quieter flare window reads sharp" retired (removing onsets LOWERS flare compression). (f) iid Solomonoff identity for the orbit demoted to a sandwich/bracket because the orbit residual is autocorrelated drift.
    Solomonoff p=2^-bits was checked per-symbol: it held cleanly on the near-iid flare (lzma 5.66 bits/symbol inside [hist 5.05, Gaussian 6.17]) and only in sandwich form on the orbit (lzma 10.46 BEAT the marginal Gaussian 12.85 -> the coder found law the marginal entropy missed).

(3) THE DIAL PROTOCOL (file: candidates/dial_engine/DIAL_PROTOCOL_SPEC.md). Claim: every reading is taken with a vector of dial settings in THREE families that need DIFFERENT handling:
  - FRAME dials = what is framed (phenomenon, scale-rung, window, channel, observer, and "inferred" = the question asked).
  - ENGINE dials = how the instrument reads / the action space over the data (law candidate, predictive family, coder, quantization, null, holdout).
  - RENDER dials = how the output is shown (the viewer; described as the "child wrapper W_C of frame x engine"): sharpness mapping, LOD/depth, axis warps, prominence weights, thresholds, panel state.
  THE ATTRIBUTION RULE (the claimed epistemic core): when a reading varies under a dial sweep, which FAMILY moved decides the meaning -- engine-dial variance = instrument calibration (report a BAND, never one headline; the probe's margin is exactly this), frame-dial variance = frame-relativity, an OBSERVABLE to investigate (not noise to average away), render-dial variance = presentation, so a view-feature that dies under a render sweep is a MIRAGE candidate ("wiggle the render before believing the view"). A claimed corollary from bouncing the idea off instruments: a 4th, BETWEEN-family artifact class -- "resolution mismatch" (aliasing/moire: the frame asks finer than the engine can resolve), with the anti-alias/low-pass filter as its control. Hardness is claimed to belong to the (framed, inferred) PAIR, not the phenomenon. An autonomous "conjecture engine" (the AutoScientist project) is proposed as a seat that PROPOSES and SCORES candidate laws (scored in held-out bits) but never ratifies.

(4) THE ONTOLOGY (file: candidates/dial_engine/ONTOLOGY_EXPLORATION.md). Pav's sharpening: "frame is the sim of observer latent wrapper and plane; engine is the action space L0; viewer is an inference of what the observer perceives." Claim reached: a sweep = one turn of an observer's PERCEPTION-ACTION loop (frame poses a question from the observer's wrapper+plane; engine acts a priced move; viewer infers p(appearance|reading,observer); verification hardens the wrapper's membranes; the next frame poses sharper). Claimed correspondence to active inference / free-energy (Friston), POMDP (belief / action-space / observation-model), and predictive-processing "controlled hallucination" (Clark, Seth), with the framework's render discipline as "the control". Physical-instrument bounce: digital camera / radio telescope (EHT) / oscilloscope; claims RAW-vs-JPEG = "save the four-tuple vs the baked view", percept is ALWAYS inference (Bayer demosaic), EHT multi-pipeline blind imaging = the mirage/wiggle test as real science, Samsung moon-photo = a "broken-weld" (rendering sharp what the sensor held fuzzy). Substrate-as-light reading: internet sources = reflected light, the append-only fact-log = the camera RAW file (with source/timestamp as EXIF), corroboration = exposure stacking, the deterministic compiler = a prism + development, the viewer = printing from negatives.

=== WHAT WE WANT FROM YOU (independent verdict) ===
Please address, concretely:
  V1. The Solomonoff/MDL claim: is "derive the probability of what it looks like = render in log2 = p=2^-bits" a correct identification, or sloppy? Is the orbit-vs-flare result a fair, non-circular test of it, or is it just "a smooth signal compresses, a bursty one does not" dressed up? Is the per-symbol identity check sound (the sandwich/bracket handling of the autocorrelated orbit)?
  V2. The "rate-of-change not amplitude" finding: is it real signal or an artifact of the persistence baseline (a differencing model will of course be surprised by derivatives)? Does a fairer flare model dissolve it?
  V3. The E-units / dimensionless-only law: correct and important, or trivially obvious (you cannot compare bits across different alphabets/dimensions)? Did the team over-credit a basic units mistake as a "finding"?
  V4. The 3-dial-family taxonomy + attribution rule: useful and non-trivial, or a relabeling of standard experimental-design hygiene (control vs treatment vs presentation; pre-registration; sensitivity analysis)? Is the "render variance = mirage detector" claim sound? Is the "resolution mismatch as a 4th between-family artifact" a real addition or just aliasing renamed?
  V5. The active-inference / perception-action-loop correspondence: is it a legitimate mapping or an over-reach analogy? Does calling the duel "free energy" actually buy anything, or is it decoration?
  V6. Overall: of this arc, what (if anything) is genuinely novel versus a re-derivation of MDL / Solomonoff / active inference / standard signal processing? What is the single strongest reason a skeptic would say "this is elaborate repackaging"? And conversely, what is the most defensible genuinely-new contribution, stated narrowly?
  V7. Anything materially WRONG (a false claim, a bad number, a method error) in FINDINGS.md / harness.py / results.json -- you may read those files directly to check.

Discipline note for your reply: this is an exploratory instrument, not a confirmatory test; the team's own register is "0.99 not Boolean" and "nothing is promoted to canon." Judge it as such, but do not let that excuse real errors. Be specific, cite files/sections, and rank your criticisms by importance. Read-only: do not modify any files; output your assessment as text only.

=== EMBEDDED FILE CONTENTS (your evidence; review directly from these) ===
----- FILE: candidates/cosmic_coin_probe/FINDINGS.md -----
# FINDINGS — Cosmic-Coin Probe (`cosmic_coin v0.1`)

**Date:** 2026-06-12 · **Status:** coin DIRECTION holds; margin demoted to a band; six dead/demoted children on record · **Adversary:** 4 attacks — 3 survive, 1 partial, 0 reversals

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

- **E1 — compression edge (cross-phenomenon).** Ratio-of-CR (raw/(resid+model)) under a pinned coder ladder, plus bits-saved fraction — always reported as the band. Current location: 1.33×–2.03× over the coder ladder; saved-fraction 0.594 vs 0.213 under the common Gaussian, tightening to 0.529 vs 0.454 once the flare gets its best fair heavy-tailed predictive. **The magnitude is a render knob (~1.17× to ~2.8×, set by coder strength and predictive family); only the sign/ordering is the claim-bearing observable.**
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
3. **lzma 2.8× / 2.37× as "the" margin** — DEMOTED to top-of-band: the edge magnitude is a render knob spanning ~1.17× (fair t) – 2.03× (lzma-extreme ladder) – 2.8× (lzma saved-fraction ratio).
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

*Reading, in the register it was taken in: the instrument located the coin edge and it is real, dimensionless, and two-layered — between phenomena (Kepler buys ~11 more bits/dim of appearance sharpness than persistence) and within one (the flare replays 99.8% of its moments and flips fuzzy exactly at rate-of-change onsets). The edge's position survived every attack; its width is a render knob. Nothing here says the flare cannot be compressed further — the misspecification attack already narrowed the gap once, exactly as a better law should, and the next better law is the standing invitation.*
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

----- FILE: candidates/cosmic_coin_probe/harness.py -----
# -*- coding: utf-8 -*-
"""
Cosmic-coin probe -- the canonical MDL + appearance-entropy instrument.

Claim under scan (INSTRUMENT register, not pass/fail): for a real phenomenon,
the bits a fair law saves when compressing it = the (in)sharpness of its
appearance. Solomonoff in miniature: p(appearance) = 2^-bits.

Two phenomena at the ends of the coin:
  ORBIT  -- Mars heliocentric position (real, JPL Horizons DE441). The LAW is a
            pure two-body Kepler propagation from the t0 state vector ALONE
            (osculating elements at epoch 0 -> predict all later epochs;
            strictly out-of-sample, no fit). Residual = what two-body misses
            (real perturbations + osculating drift). Expect: tiny residual ->
            few bits -> sharp appearance -> REPLAY face.
  FLARE  -- GOES long-band (0.1-0.8nm) X-ray flux (real, NOAA SWPC). The LAW is
            a fair persistence baseline on log-flux (f_hat(t)=f(t-1)). Residual
            = log-flux increments; tiny in quiet sun, heavy-tailed spikes at
            flare onsets. Expect: poor compression -> many bits at onsets ->
            broad appearance -> SIMULATE face.

DISCLOSED PROXIES (PROXY_SPEC discipline -- these are render/measurement
heuristics with knobs, not laws):
  * coder            : Python lzma preset 9 (pinned). Sibling coders reported by
                       the workflow re-measure phase (zlib/bz2) to test robustness.
  * quantization     : positions 1 km; log10(flux) 1e-3 dex. Same encoding for
                       raw vs residual so the comparison is fair (gain_v2 lesson:
                       compare like-for-like, floor the model).
  * model cost       : Kepler = 6 elements + mu (float64); persistence = 1 number.
                       Negligible vs the series, but COUNTED, never zero.
  * predictive dist  : a single fair common instrument for both -- Gaussian about
                       the model's point prediction with sigma = residual std.
                       (The skeptic phase is invited to give the flare a heavier-
                       tailed predictive dist; the separation should survive.)

NO fabrication. Real fetched data only. This is a scan that LOCATES the coin
edge as an observable; it does not declare a phenomenon "incompressible" (that
stronger claim is handed to the adversary -- a better flare model could close
the gap; the misspecification confound is the same shape as gain_v2's).
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "probe_data"
MU_SUN = 1.32712440018e11  # km^3/s^2  (heliocentric gravitational parameter, IAU)
Q_POS_KM = 1.0             # position quantization (km)
Q_LOGFLUX = 1e-3           # log10-flux quantization (dex)
LOG2E = 1.0 / math.log(2.0)

# --------------------------------------------------------------------------
# coders (pinned lzma primary; zlib/bz2 reported as siblings)
# --------------------------------------------------------------------------
def clen_bits(int_array, coder="lzma"):
    """Codelength in bits of an integer array under a pinned general coder.
    Same dtype/encoding is used for raw and residual so the contrast is fair."""
    b = np.ascontiguousarray(int_array.astype(np.int64)).tobytes()
    if coder == "lzma":
        c = lzma.compress(b, preset=9)
    elif coder == "zlib":
        c = zlib.compress(b, 9)
    elif coder == "bz2":
        c = bz2.compress(b, 9)
    else:
        raise ValueError(coder)
    return len(c) * 8

def gaussian_entropy_bits(sigma, q):
    """Discrete entropy (bits) of a Gaussian source quantized at step q,
    valid for sigma >> q: 0.5*log2(2*pi*e*sigma^2) - log2(q)."""
    sigma = max(float(sigma), 1e-12)
    return 0.5 * math.log2(2 * math.pi * math.e * sigma * sigma) - math.log2(q)

# --------------------------------------------------------------------------
# ORBIT: parse Horizons, two-body propagate from t0 state, residual
# --------------------------------------------------------------------------
def parse_horizons(path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    lines = txt.splitlines()
    try:
        i0 = next(i for i, l in enumerate(lines) if "$$SOE" in l)
        i1 = next(i for i, l in enumerate(lines) if "$$EOE" in l)
    except StopIteration:
        raise RuntimeError("Horizons markers not found")
    jds, R, V = [], [], []
    blk = lines[i0 + 1:i1]
    k = 0
    while k < len(blk):
        head = blk[k]
        if "=" in head and ("A.D." in head or "B.C." in head):
            jd = float(head.split("=")[0].strip())
            xrow = blk[k + 1]; vrow = blk[k + 2]
            def g3(row):
                # rows like " X =-4.38E+07 Y =-2.17E+08 Z =-3.47E+06"
                parts = row.replace("X =", " ").replace("Y =", " ").replace("Z =", " ")
                parts = parts.replace("VX=", " ").replace("VY=", " ").replace("VZ=", " ")
                return [float(t) for t in parts.split()]
            R.append(g3(xrow)); V.append(g3(vrow)); jds.append(jd)
            k += 3
        else:
            k += 1
    return np.array(jds), np.array(R), np.array(V)

def elements_from_rv(r, v, mu):
    R = np.linalg.norm(r); V = np.linalg.norm(v)
    h = np.cross(r, v); H = np.linalg.norm(h)
    n = np.cross([0, 0, 1.0], h); N = np.linalg.norm(n)
    evec = ((V * V - mu / R) * r - np.dot(r, v) * v) / mu
    e = np.linalg.norm(evec)
    energy = V * V / 2 - mu / R
    a = -mu / (2 * energy)
    i = math.acos(np.clip(h[2] / H, -1, 1))
    Om = math.acos(np.clip(n[0] / N, -1, 1));  Om = 2 * math.pi - Om if n[1] < 0 else Om
    om = math.acos(np.clip(np.dot(n, evec) / (N * e), -1, 1));  om = 2 * math.pi - om if evec[2] < 0 else om
    nu = math.acos(np.clip(np.dot(evec, r) / (e * R), -1, 1));  nu = 2 * math.pi - nu if np.dot(r, v) < 0 else nu
    return a, e, i, Om, om, nu

def kepler_E(M, e, tol=1e-12):
    M = (M + math.pi) % (2 * math.pi) - math.pi
    E = M if e < 0.8 else math.pi
    for _ in range(100):
        d = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= d
        if abs(d) < tol:
            break
    return E

def propagate(elem, mu, dt):
    a, e, i, Om, om, nu0 = elem
    E0 = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu0 / 2), math.sqrt(1 + e) * math.cos(nu0 / 2))
    M0 = E0 - e * math.sin(E0)
    nmot = math.sqrt(mu / a ** 3)
    M = M0 + nmot * dt
    E = kepler_E(M, e)
    nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
    r = a * (1 - e * math.cos(E))
    # perifocal -> inertial via 3-1-3 (Om, i, om)
    rp = np.array([r * math.cos(nu), r * math.sin(nu), 0.0])
    cO, sO, ci, si, cw, sw = math.cos(Om), math.sin(Om), math.cos(i), math.sin(i), math.cos(om), math.sin(om)
    Rm = np.array([
        [cO * cw - sO * sw * ci, -cO * sw - sO * cw * ci,  sO * si],
        [sO * cw + cO * sw * ci, -sO * sw + cO * cw * ci, -cO * si],
        [sw * si,                 cw * si,                 ci]])
    return Rm @ rp

def analyze_orbit():
    jd, R, V = parse_horizons(DATA / "mars_horizons_raw.txt")
    secs = (jd - jd[0]) * 86400.0
    elem = elements_from_rv(R[0], V[0], MU_SUN)
    pred = np.array([propagate(elem, MU_SUN, dt) for dt in secs])
    resid = R - pred                        # km, 3-vector per epoch
    rabs = np.linalg.norm(resid, axis=1)
    # MDL via pinned coder: same int64 km encoding for raw vs residual
    raw_i = np.round(R / Q_POS_KM).astype(np.int64).reshape(-1)
    res_i = np.round(resid / Q_POS_KM).astype(np.int64).reshape(-1)
    out = {}
    for coder in ("lzma", "zlib", "bz2"):
        raw_b = clen_bits(raw_i, coder)
        res_b = clen_bits(res_i, coder)
        model_b = 7 * 64  # 6 elements + mu, float64; counted not zero
        out[coder] = dict(raw_bits=raw_b, resid_bits=res_b, model_bits=model_b,
                          comp_ratio=raw_b / (res_b + model_b))
    # analytic appearance-entropy (fair common Gaussian instrument), bits/step
    sig_raw = np.std(R, axis=0).mean()
    sig_res = np.std(resid, axis=0).mean()
    H_raw = 3 * gaussian_entropy_bits(sig_raw, Q_POS_KM)      # marginal
    H_app = 3 * gaussian_entropy_bits(sig_res, Q_POS_KM)      # under the law
    # per-step NLL (bits) under N(pred, sig_res) -- the appearance entropy series
    sig = np.std(resid, axis=0)
    nll = 0.5 * np.sum(np.log2(2 * math.pi * sig ** 2) + (resid ** 2) / (sig ** 2) * LOG2E, axis=1) - 3 * math.log2(Q_POS_KM)
    rng = np.random.default_rng(0)
    sample = pred + rng.normal(0, sig, size=pred.shape)       # a draw from the predictive dist
    return dict(
        n=len(jd), span_days=float(jd[-1] - jd[0]),
        elements=dict(a_km=elem[0], e=elem[1], i_deg=math.degrees(elem[2])),
        resid_km=dict(mean=float(rabs.mean()), p50=float(np.percentile(rabs, 50)),
                      p99=float(np.percentile(rabs, 99)), max=float(rabs.max())),
        orbit_radius_km=float(np.linalg.norm(R, axis=1).mean()),
        rel_resid=float(rabs.mean() / np.linalg.norm(R, axis=1).mean()),
        mdl=out,
        appearance_bits_per_step=H_app, raw_bits_per_step=H_raw,
        bits_saved_per_step=H_raw - H_app,
        nll_bits=dict(mean=float(nll.mean()), p50=float(np.percentile(nll, 50)),
                      p99=float(np.percentile(nll, 99)), max=float(nll.max())),
        _nll_series=nll, _resid=resid, _truth=R, _pred=pred, _sample=sample,
    )

# --------------------------------------------------------------------------
# FLARE: parse GOES long band, persistence baseline on log-flux
# --------------------------------------------------------------------------
def analyze_flare():
    rows = json.loads((DATA / "goes_xray_7day.json").read_text(encoding="utf-8"))
    long = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    long.sort(key=lambda r: r["time_tag"])
    flux = np.array([r["flux"] for r in long], dtype=float)
    flux = np.clip(flux, 1e-9, None)
    flux = flux[np.isfinite(flux)]
    lf = np.log10(flux)                       # work in log-flux (spans orders of mag)
    pred = np.empty_like(lf); pred[0] = lf[0]; pred[1:] = lf[:-1]   # persistence f_hat(t)=f(t-1)
    resid = lf - pred                          # log-flux increments
    raw_i = np.round(lf / Q_LOGFLUX).astype(np.int64)
    res_i = np.round(resid / Q_LOGFLUX).astype(np.int64)
    out = {}
    for coder in ("lzma", "zlib", "bz2"):
        raw_b = clen_bits(raw_i, coder); res_b = clen_bits(res_i, coder)
        out[coder] = dict(raw_bits=raw_b, resid_bits=res_b, model_bits=64,
                          comp_ratio=raw_b / (res_b + 64))
    sig_raw = float(np.std(lf)); sig_res = float(np.std(resid))
    H_raw = gaussian_entropy_bits(sig_raw, Q_LOGFLUX)
    H_app = gaussian_entropy_bits(sig_res, Q_LOGFLUX)
    nll = 0.5 * (np.log2(2 * math.pi * sig_res ** 2) + (resid ** 2) / (sig_res ** 2) * LOG2E) - math.log2(Q_LOGFLUX)
    rng = np.random.default_rng(0)
    sample = pred + rng.normal(0, sig_res, size=pred.shape)
    # flare census (NOAA classes by long-band flux: C>=1e-6, M>=1e-5, X>=1e-4)
    peak = float(flux.max())
    cls = ("X" if peak >= 1e-4 else "M" if peak >= 1e-5 else "C" if peak >= 1e-6 else "B/A")
    return dict(
        n=len(lf), peak_flux=peak, peak_class=cls,
        log_flux_std=sig_res,
        mdl=out,
        appearance_bits_per_step=H_app, raw_bits_per_step=H_raw,
        bits_saved_per_step=H_raw - H_app,
        nll_bits=dict(mean=float(nll.mean()), p50=float(np.percentile(nll, 50)),
                      p99=float(np.percentile(nll, 99)), max=float(nll.max())),
        _nll_series=nll, _resid=resid, _truth=lf, _pred=pred, _sample=sample,
    )

# --------------------------------------------------------------------------
def main():
    orb = analyze_orbit(); fla = analyze_flare()
    # save arrays for the workflow re-measure/adversary phases
    np.savez(HERE / "probe_data" / "series.npz",
             orbit_nll=orb["_nll_series"], orbit_resid=orb["_resid"],
             orbit_truth=orb["_truth"], orbit_pred=orb["_pred"], orbit_sample=orb["_sample"],
             flare_nll=fla["_nll_series"], flare_resid=fla["_resid"],
             flare_truth=fla["_truth"], flare_pred=fla["_pred"], flare_sample=fla["_sample"])
    for d in (orb, fla):
        for k in list(d):
            if k.startswith("_"):
                del d[k]
    results = dict(
        probe="cosmic_coin v0.1", coder_primary="lzma-9",
        quant=dict(pos_km=Q_POS_KM, logflux_dex=Q_LOGFLUX),
        orbit=orb, flare=fla,
        coin_edge=dict(
            orbit_comp_ratio=orb["mdl"]["lzma"]["comp_ratio"],
            flare_comp_ratio=fla["mdl"]["lzma"]["comp_ratio"],
            orbit_appearance_bits=orb["appearance_bits_per_step"],
            flare_appearance_bits=fla["appearance_bits_per_step"],
            separation_comp=orb["mdl"]["lzma"]["comp_ratio"] / fla["mdl"]["lzma"]["comp_ratio"],
            separation_bits=fla["appearance_bits_per_step"] - orb["appearance_bits_per_step"],
        ),
    )
    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    # headline
    print("=" * 64)
    print("COSMIC-COIN PROBE -- headline (pinned lzma-9, real data)")
    print("=" * 64)
    o, f = orb["mdl"]["lzma"], fla["mdl"]["lzma"]
    print(f"ORBIT (Mars, {orb['n']}d)  two-body-vs-DE441")
    print(f"   rel.residual      : {orb['rel_resid']:.2e}  (mean {orb['resid_km']['mean']:.0f} km / {orb['orbit_radius_km']:.3e} km)")
    print(f"   lzma comp ratio   : {o['comp_ratio']:.2f}x   (raw {o['raw_bits']} -> resid {o['resid_bits']} bits)")
    print(f"   appearance entropy: {orb['appearance_bits_per_step']:.2f} bits/step   (raw {orb['raw_bits_per_step']:.2f})")
    print(f"   per-step NLL      : mean {orb['nll_bits']['mean']:.2f}  p99 {orb['nll_bits']['p99']:.2f}  max {orb['nll_bits']['max']:.2f} bits")
    print(f"FLARE (GOES long, {fla['n']}m)  persistence baseline   peak {fla['peak_flux']:.2e} W/m2 ({fla['peak_class']}-class)")
    print(f"   lzma comp ratio   : {f['comp_ratio']:.2f}x   (raw {f['raw_bits']} -> resid {f['resid_bits']} bits)")
    print(f"   appearance entropy: {fla['appearance_bits_per_step']:.2f} bits/step   (raw {fla['raw_bits_per_step']:.2f})")
    print(f"   per-step NLL      : mean {fla['nll_bits']['mean']:.2f}  p99 {fla['nll_bits']['p99']:.2f}  max {fla['nll_bits']['max']:.2f} bits")
    print("-" * 64)
    ce = results["coin_edge"]
    print(f"COIN EDGE  compression separation {ce['separation_comp']:.1f}x | appearance-entropy gap {ce['separation_bits']:.2f} bits/step")
    print(f"   orbit -> {'SHARP/REPLAY' if ce['orbit_comp_ratio']>ce['flare_comp_ratio'] else '??'}  | flare -> {'FUZZY/SIMULATE' if ce['flare_comp_ratio']<ce['orbit_comp_ratio'] else '??'}")
    print("results.json + probe_data/series.npz written")

if __name__ == "__main__":
    main()
----- FILE: candidates/cosmic_coin_probe/results.json -----
{
  "probe": "cosmic_coin v0.1",
  "coder_primary": "lzma-9",
  "quant": {
    "pos_km": 1.0,
    "logflux_dex": 0.001
  },
  "orbit": {
    "n": 366,
    "span_days": 365.0,
    "elements": {
      "a_km": 227938934.4298894,
      "e": 0.09329526776397692,
      "i_deg": 1.8478708516317703
    },
    "resid_km": {
      "mean": 14904.416669035612,
      "p50": 9643.705178357748,
      "p99": 37809.33244065283,
      "max": 37816.13469970179
    },
    "orbit_radius_km": 217875089.0938863,
    "rel_resid": 6.840808066227815e-05,
    "mdl": {
      "lzma": {
        "raw_bits": 28288,
        "resid_bits": 11488,
        "model_bits": 448,
        "comp_ratio": 2.3699731903485253
      },
      "zlib": {
        "raw_bits": 36032,
        "resid_bits": 18784,
        "model_bits": 448,
        "comp_ratio": 1.8735440931780365
      },
      "bz2": {
        "raw_bits": 41464,
        "resid_bits": 21072,
        "model_bits": 448,
        "comp_ratio": 1.9267657992565055
      }
    },
    "appearance_bits_per_step": 43.30012280024418,
    "raw_bits_per_step": 85.23517071791309,
    "bits_saved_per_step": 41.93504791766891,
    "nll_bits": {
      "mean": 41.18644382846835,
      "p50": 40.4346368347402,
      "p99": 48.84911831572228,
      "max": 48.85831175062065
    }
  },
  "flare": {
    "n": 10078,
    "peak_flux": 1.863967554527335e-05,
    "peak_class": "M",
    "log_flux_std": 0.0174441199453243,
    "mdl": {
      "lzma": {
        "raw_bits": 72576,
        "resid_bits": 57088,
        "model_bits": 64,
        "comp_ratio": 1.2698768197088466
      },
      "zlib": {
        "raw_bits": 111600,
        "resid_bits": 77472,
        "model_bits": 64,
        "comp_ratio": 1.4393314073462649
      },
      "bz2": {
        "raw_bits": 69720,
        "resid_bits": 54200,
        "model_bits": 64,
        "comp_ratio": 1.284829721362229
      }
    },
    "appearance_bits_per_step": 6.171764495568608,
    "raw_bits_per_step": 9.673529180998328,
    "bits_saved_per_step": 3.5017646854297197,
    "nll_bits": {
      "mean": 6.171765864636694,
      "p50": 5.481174476435447,
      "p99": 14.471029699725312,
      "max": 599.458928995495
    }
  },
  "coin_edge": {
    "orbit_comp_ratio": 2.3699731903485253,
    "flare_comp_ratio": 1.2698768197088466,
    "orbit_appearance_bits": 43.30012280024418,
    "flare_appearance_bits": 6.171764495568608,
    "separation_comp": 1.8663016393132568,
    "separation_bits": -37.12835830467557
  }
}----- FILE: candidates/dial_engine/DIAL_PROTOCOL_SPEC.md -----
# DIAL PROTOCOL — frame dials, engine dials, and the candidate-trial methodology (SPEC, Tier-3 DRAFT)

> **Status:** Tier-3 working spec, surfaced for Cowork+Pav ratification — NOT canon, NOT compiled, no tier advanced, convergence list stays **9**. A **sibling spec** in the L0_WRAPPER_SPEC mold: it BINDS to the existing substrate format protocol (append-only JSONL → compiler → compiled views → viewer ingestion) and to the existing frame-lock discipline; it forks nothing and edits nothing ratified.
> **Pav steer (2026-06-12, verbatim sense):** *"there's multiple dials for the frame and the engine and we need a methodology to try the top candidates in context of what is being framed and what is inferred — this is where something like this [AutoScientist] can plug in, specked out to the viewer and substrate format protocol."* **Same-day addendum:** *"there are the render dials as well — the viewer; the W_C of engine and frame, the output if you will."* — the third family (§1.4), folded in below.
> **Born from a measured incident:** the cosmic-coin probe (`../cosmic_coin_probe/FINDINGS.md`) found its reading's *direction* robust but its *magnitude* a knob — and the knobs split cleanly into two families that need **opposite** handling. This spec is that split, made protocol.

---

## 1. The three dial families

Every reading the instrument produces is taken with a vector of dial settings. The load-bearing distinctions:

### 1.1 FRAME dials — *what is being framed*
Dials that change **what is being observed**: turn one and you are asking about a different slice of the world.

| frame dial | examples (measured instances) |
|---|---|
| `phenomenon` | Mars position / GOES long-band flux |
| `scale_rung` (time) | 1-min cadence vs daily vs solar-cycle (FINDINGS Q6) |
| `scale_rung` (space/semantic) | the L0 abstraction ladder rung; generic↔specific |
| `window` | which year, which week (probe: flare halves/quarters CR 1.09–1.23) |
| `channel` | GOES long band CR 1.27 vs short band CR 1.02 |
| `observer/plane` | physical / latent / straddle (SCHEMA_v2 `frame_layer`) |
| `inferred` | **what question is asked** — see §1.3 |

### 1.2 ENGINE dials — *how the instrument reads*
Dials internal to the measuring engine: turn one and you are asking the **same question with a different instrument calibration**.

| engine dial | examples (measured instances) |
|---|---|
| `law` (compressor candidate) | persistence / AR(1) / EWMA / MA(n) / Kepler two-body |
| `predictive` family | Gaussian / Student-t(nu) (probe: flare saved-frac 0.21→0.454) |
| `coder` | zlib-1/zlib-9/bz2-9/lzma-9/lzma-9e (ratio-of-CR 1.33–2.03, never inverts) |
| `quantization` | 1 km / 1e-3 dex (cancels exactly only in σ-shrink form) |
| `null/baseline` + model-bits accounting | "store" floor; model bits counted, never zero |
| `holdout scheme` | in-sample vs out-of-sample fit |

### 1.3 The pair (framed, inferred) — hardness belongs to the QUESTION, not the thing
The same phenomenon under a different `inferred` is a **different trial subject**: the flare is fuzzy for *"next-minute log-flux"* but plausibly much sharper for *"will this week contain an M-class flare"* (coarse-grain question). Dial position is a property of the **(framed, inferred) pair**. This is the meaning-kernel entering the protocol: what you ask determines what is sharp. No trial record without an explicit `inferred`.

### 1.4 RENDER dials — *how the output is shown* (the W_C of frame and engine)
Pav's genealogical reading, adopted as the definition: **the displayed view is the child wrapper (W_C) produced by the weld of frame × engine** — the output. Render dials are the dials ON that child: they change how the reading is shown, and must change **nothing** about the reading itself.

| render dial | examples (all already shipped, now named) |
|---|---|
| sharpness/hardness mapping | `l0-membrane-proxy-v0.1` (h = B(bucket)·certainty) — a *versioned render dial*, PROXY_SPEC-disclosed |
| LOD / depth-context cutoff | the viewer's depth dial, quality ladder, fuzzy-LOD |
| axis warps | time-axis calendar↔order blend, scrub fisheye, log2 radius |
| prominence weights | observer-kernel re-weighting in group renders (§2.5 frame weights — estimate-proxies) |
| thresholds & encodings | mirage threshold, mass→force, color/pattern-for-same-colour, band→edge-thickness |
| layout & state | panel positions, toggles, selected node — everything `__getReviewState()` captures |

**The view inherits both parents' membranes** — frame-relativity from the frame parent, the calibration band from the engine parent. The render dials set how those inherited fuzzes are *shown*. **Broken-weld law:** a view that renders sharp what either parent holds fuzzy is a broken weld — the no-invented-precision UI law restated genealogically (and never-render-fake-measured-bits is its generative-face form).

**Retroactive naming (vocabulary meets existing structure):** `group_configs/*.json` are saved render-dial presets; the review pipeline's `__getReviewState`/`__applyReviewState` is render-dial state capture/replay (a pin's frame-replay = restoring the render vector); PROXY_SPEC is the render-dial disclosure discipline, already ratified. The family existed; it now has a name and a seat in the protocol.

## 2. The attribution rule (the epistemic core)

When a reading varies under a dial sweep, **which family moved decides what the variance means**:

- **ENGINE-dial variance = instrument calibration.** Report the **band**, never one headline; pin defaults; disclose per PROXY_SPEC (versioned, falsification target). *Measured instance:* the coin margin ~1.17×–2.8× across coder × predictive — a render knob, demoted accordingly (FINDINGS §7 child 3).
- **FRAME-dial variance = frame-relativity, an OBSERVABLE.** Not noise to average away, not a flaw — the solid↔fuzzy reversal under re-framing is signal to investigate (already canon: the contextual-scale dial; the agnostic-instrument register). *Measured instance:* long band 1.27 vs short band 1.02; quiet-sun window 1.21.
- **Mixed variance** (engine dial behaving differently per frame setting — e.g. Student-t HELPS the flare, HURTS the orbit) is the most informative cell: it localizes *structure* (tail weight is a property of the framed thing, revealed by the engine sweep). Flag it `interaction`.
- **RENDER-dial variance = presentation-relativity, and the cheapest mirage detector.** A render dial must never alter a recorded number — so any feature of the *view* that appears or dies under a render-dial sweep, with frame and engine untouched, is a **render artifact (mirage candidate), never a finding**. "Wiggle the render before believing the view" is the sharpening test generalized: real structure survives the render sweep; mirage dies with the dial. (The capture-layer incident is the inverse failure on record: a render-layer rule *hid* real structure — render dials can occlude as well as conjure, which is why the sweep goes both ways.)

A sweep's deliverable is therefore a **variance decomposition over the dial grid**, not a number — with three meanings of variance, one per family.

## 3. The trial methodology ("try the top candidates")

1. **Declare the pair** — `framed` (phenomenon + frame-dial settings) and `inferred` (the question). One line each, before any run.
2. **Enumerate top-K candidates per engine dial** — laws from the candidate registry (§5) + the conjecture engine (§6); predictive families; the pinned coder ladder. K small (3–5); breadth comes from sweeps, not one giant grid.
3. **Lock the frame** — frame dials are FROZEN for the sweep (the existing frame-lock discipline, same move as L0 §7.3 / the census dial-lock). Frame-dial changes are *proposed in the sweep log, applied next sweep*.
4. **Run the grid** — every candidate × the engine-dial ladder, held-out where fit is involved, model bits counted. Each cell = one **trial record** (§5), append-only.
5. **Read the decomposition** — per §2: the band (engine), the relativity observables (frame, from comparisons *across* sweeps), the interactions.
6. **Advance the lifecycle** — best candidate per (framed, inferred) = the **current kernel candidate**; beaten candidates stay as dated dead/demoted children (never deleted); a candidate that wins = a dial-jump, appended to the law's worldline (laws have lifecycles too — FINDINGS S4).
7. **Log the sweep** — dated section in `SWEEP_LOG.md`: grid run, decomposition, dial-jumps, dead-children tally, PROPOSED frame/engine vocabulary for next sweep.

## 4. The AutoScientist plug-in seat (conjecture engine)

Pav's pointer: `https://autoscientists.openscientist.ai/` — decentralized agent teams alternating **discussion** (form teams around directions, propose experiments) and **execution** (parallel runs, reorganize on stagnation), sharing best-result + experiment logs + forums + **dead-end registries**. The mapping onto machinery we already run is almost 1:1 — this seat is a *generator*, the protocol is the *verifier*:

| AutoScientist | this protocol |
|---|---|
| hypothesis generation | **candidate minting** — propose a new `law`/`predictive` for a (framed, inferred) pair, with its prior-art note |
| experiment design + execution | the **trial grid** (§3.4), run by workflow seats (Sonnet scouts / Fable judges / Opus skeptic, the standing pattern) |
| the score | **held-out bits** with model bits counted — the duel is the verifier; no narrative wins |
| best shared result | the **current kernel candidate** per pair, in the compiled view |
| dead-end registry | the **dead-children tally** (CLAIM_LIFECYCLE — demoted/dormant/dated, never deleted) |
| team re-org on stagnation | sweep-log **frontier**: pairs whose gap stopped closing get new candidate families next sweep |
| compute budget | per-sweep token/run budget, declared in the sweep log |

**Boundary (hard):** the conjecture engine *proposes and scores*; it never writes canon, never edits a prior record, never renders. Its output is candidates + trial records into the append-only log. Ratification stays with Pav/Cowork. External A− (GPT-5.5 + Gemini) stays the cross-model check on load-bearing readings — workflow seats are Claude-only.

## 5. Substrate binding (format protocol)

Same machinery, new record type — **nothing in SCHEMA_v2 or SUBSTRATE_SPEC edited**:

- **`runs/<sweep>.jsonl`** — append-only, one **trial record** per line:
  ```jsonc
  { "trial_id": "dial-<pair-slug>-NNNN",        // globally unique, HAZARD-guard style
    "sweep": "dial-sweep-NN",
    "framed":   { "phenomenon": "...", "frame_dials": { "scale_rung": "...", "window": "...", "channel": "..." } },
    "inferred": "next-step log-flux",
    "engine_dials": { "law": "...", "predictive": "...", "coder": "...", "quant": "..." },
    "candidate_source": "authored | conjecture-engine | adversary",
    "data": { "source_url": "...", "n": 0, "real": true },   // NO fabrication; real fetched data only
    "reading": { /* bits_raw, bits_resid, model_bits, comp_ratio, saved_fraction,
                    sigma_shrink_bits_per_dim, appearance_bits_per_step ... whichever were MEASURED */ },
    "dimensionless_only_across_pairs": true,     // the E-units law, in-band
    "verifier": "dial-sweep-NN-<seat>", "retrieved_at": "ISO", "notes": "..." }
  ```
  Append-only correction discipline: a wrong reading is superseded by a new record naming it, never edited (same as fact retractions).
- **Compiled view** (`compiled/dial-<pair>.compiled.json`, deterministic compiler to be built as `tools/compile_dials.py`): per (framed, inferred) pair — the current kernel candidate, the **band** over engine dials, the frame-relativity observables, the interaction flags, the law worldline (dial-jump history), the mixture profile (replay-fraction, break census) where measured.
- **PROXY_SPEC compliance:** every render-bearing engine default (pinned coder, predictive family, quant) is a versioned disclosed proxy with a falsification target. v0 pins: `lzma-9`, Gaussian-unless-beaten-fairly, declared quant per phenomenon, model-bits-counted, **no absolute bits across pairs** (the E-units law).
- **View reproducibility:** any visual artifact derived from trials (a FINDINGS plot, a toy config, a viewer slice) is fully determined by `(framed, inferred, engine_dials, render_dials)` — so view-bearing records MAY carry an optional `render_dials` vector, and a saved view = a saved four-tuple. `group_configs/*.json` and review-pin `state.viewer` blobs already ARE this object; the protocol just names them.

## 6. Viewer plug (specked, not built)

- **Dial panel — three tiers, one per family:** FRAME dials render as user-turnable controls (the scrubber, the zoom/abstraction dial, observer picker — all already exist in viewer_v3; `window`/`channel`/`inferred` join them). ENGINE dials render as **pinned chips** showing the band on hover ("margin 1.17×–2.8× over coder × predictive") — turnable only in an explicit calibration mode, per the attribution rule. RENDER dials are freely turnable but disclosure-bound (every one a PROXY_SPEC entry) — plus a **"wiggle" affordance**: one control that jitters the render dials so the eye can run the mirage test live (what survives the wiggle is structure; what dances with it is render).
- **Observer disambiguation:** "observer" appears twice and the panel must keep the two apart — observer-as-FRAME (whose kernel poses the question; changes what is measured) vs observer-as-RENDER (prominence re-weighting in a group view; changes only what is shown). Same word, different families, different tier of the panel.
- **Reading render:** dial position (σ-shrink bits/dim) drives wrapper sharpness; the band renders as edge thickness (a wide band = a wide coin edge); mixture profiles render as kernel-disc radius (replay fraction) + membrane spikes (the breaks).
- **Law worldlines:** each (framed, inferred) pair carries its dial-jump trace (Saros→Newton→GR style) as an exhaust trail — the lifecycle render the viewer already does for claims, applied to laws.
- **Provenance hover:** every rendered sharpness links its trial records (fact_refs pattern).

## 7. Worked binding — sweep 0 (retro-encoded from the cosmic-coin probe, real numbers only)

`runs/dial-sweep-00.jsonl` encodes the probe's actually-measured grid as the first trial records: Mars × {Kepler} × {Gaussian} × {lzma-9, zlib-9, bz2-9} and GOES × {persistence, AR(1), EWMA, AR(1)-on-increments} × {Gaussian, Student-t(2.1)} × coder ladder, plus the frame-dial trials (window sub-splits, quiet-sun-only, channel swap, onset-amplification). Every number traces to `../cosmic_coin_probe/results.json` / `FINDINGS.md` / the adversary scripts; nothing re-derived, nothing invented. Sweep 0's decomposition is the probe's §5 adversary table, re-read as protocol output:
- engine band: coder 1.33–2.03× (ratio-of-ratios), predictive 0.21→0.454 (flare saved-frac);
- frame observables: window 1.09–1.23, channel 1.27 vs 1.02, quiet-sun 1.21;
- interaction: Student-t helps flare / hurts orbit (tail weight is structure);
- dial-jump: none (persistence survived as flare kernel candidate; AR(1)-on-increments 1.30 vs 1.27 is within engine band — flagged, not promoted);
- dead children: inherited 6 from the probe (FINDINGS §7).

## 8. Discipline footer

Frame-lock per sweep; append-only everywhere; NO fabrication (every trial on real fetched data, `data.real` mandatory); model bits counted; **dimensionless-only across pairs** (E-units, in-band); proxies versioned + falsifiable; **render dials never alter a recorded number, and a view never renders sharp what either parent holds fuzzy (the broken-weld law)**; conjecture engine proposes, never ratifies; verified = Pav's call; Tier-3 throughout, convergence list stays **9**. Owed before this hardens: an Opus skeptic pass on this spec, the GPT-5.5+Gemini external pass (Claude-only so far), and `tools/compile_dials.py` + the viewer dial panel as the build steps — gated on a Pav/Cowork nod.
----- FILE: candidates/dial_engine/ONTOLOGY_EXPLORATION.md -----
# What ARE the three families? — ontology exploration (Tier-3, exploration register)

> **Status:** exploration, 0 children, nothing locked — Pav intuition + unpacking, candidate sharper definitions, and three cheap audits that would test them. Not part of the protocol until ratified; `DIAL_PROTOCOL_SPEC.md` stands unedited by this file.
> **Pav (2026-06-12, verbatim sense):** *"frame is the sim of observer latent wrapper and plane, engine is the action space L0, viewer is an inference what the observer perceives — this is an intuition, lets explore, perhaps there's a sharper definition."*

## 1. Unpacking the intuition

- **Frame = the sim of (observer latent wrapper ⊕ plane).** The frame is not a neutral settings list — it is the observer's own running simulation of the world (their latent wrapper: kernel + membrane of what they know/mean), *restricted by the plane they stand on* (what is capturable from there — the observer_planes machinery). Frame dials are parameters of that composite.
- **Engine = the action space over L0.** Engine dials are not "calibration knobs" — they are the MOVES available against the framed thing: compress with this law, fit this predictive, code at this grain, hold out this way. Applying Kepler is an *action* on the data. Model-bits-counted = the action's price. The duel = action selection under cost.
- **Viewer = an inference of what the observer perceives.** The render is not presentation — it is a *derivation of the percept*: p(appearance | reading, observer). The viewer is literally the organ of the original coin steer — "not calculate but **derive the probability of what it looks like**" — sharp readings render as delta-percepts (replay), fuzzy readings as sampled fuzz (simulate). **The coin's two faces are viewer inference modes, gated by the engine's bits, over the frame's question.**

## 2. The sentence (candidate sharper definition, recommended)

**A sweep is one turn of an observer's perception–action loop:**
the **frame poses** (observer wrapper ⊕ plane → a question), the **engine acts** (an action from the L0 action space, priced in bits), the **viewer perceives** (infer p(appearance | reading) for that observer) — and **verification feeds the percept back into the wrapper's membranes**, so the next frame poses sharper.

Ask → act → see → harden → ask again. The dial protocol is then exactly: *the methodology for sweeping each component's parameters with the right attribution* — frame variance = world-relativity (signal), engine variance = action calibration (band), viewer variance = inference artifact (mirage candidate).

## 3. What the sharper definition dissolves and explains

1. **The observer-in-two-families wrinkle dissolves.** The observer was never a dial — the observer is the loop's *owner*. They appear twice because the loop passes through them twice: once posing (frame), once perceiving (viewer). Circuit topology, not ambiguity. (Spec §6's disambiguation becomes a corollary.)
2. **Questions live at the membrane.** If the frame is the observer's wrapper, the `inferred` is posed from its FUZZY region — you ask about what is fuzzy *to you*. The (framed, inferred) pair is the observer's membrane-frontier projected onto L0 — which is *why* hardness belongs to the pair, not the phenomenon: it is relative to the asker's wrapper state. (Curiosity = membrane pressure.)
3. **The conjecture engine = action-space expansion.** Minting a new law candidate literally grows the action space; a dial-jump is a policy improvement under fixed cost accounting; the history of science for a phenomenon = the growth trace of A. (FINDINGS S4 restated.)
4. **Mirages get a mechanism.** If the viewer is inference, render artifacts are *inference hallucinating*; the broken-weld law + wiggle test + never-render-fake-measured-bits are the **control** on the hallucination. The capture incident = the inference *occluding* (controlled too hard, the inverse failure).

## 4. Established anchors (disclosed honestly — the structure is not new; the binding is)

- **Active inference / free-energy principle (Friston):** perception–action loops minimizing surprise *in bits* — perception updates beliefs, action changes the world; the coin's replay/simulate = the two ways to be unsurprised. Our duel-in-bits is variational free energy in MDL clothing.
- **POMDP (belief, action space, observation model):** frame ≈ belief+query, engine ≈ A, viewer ≈ O. The three dial families are the three arguments of an agent.
- **Predictive processing — perception as "controlled hallucination" (Clark, Seth):** the viewer-as-inference IS this phrase; the framework's render discipline is the *controlled* part, named and enforced.
- **Gibson's affordances:** the action space is observer-relative — what L0 affords *from this plane*.
- **MDL/Solomonoff:** the shared currency across all three (already the §IT spine).

**Genuinely Pav's, on top:** binding these three roles to a provenance'd fact-substrate with the attribution rule as epistemics; the coin as the viewer's mode-switch; questions-from-the-membrane; and the whole loop running as an auditable sweep protocol rather than a metaphor.

## 5. Three cheap audits (the definition's first children — proposed, not run)

- **A1 — Frame-table bifurcation.** Prediction: if frame = wrapper ⊕ plane, every frame dial splits into *plane-side* (capture constraints: window, channel, cadence) or *wrapper-side* (meaning constraints: inferred, scale-rung-as-abstraction). First look: the spec §1.1 table splits cleanly (window/channel/cadence = plane; inferred/scale-rung = wrapper; observer = the owner, not a dial). A dial that refuses the split falsifies the decomposition or exposes a misfiled dial.
- **A2 — Render-dial castability.** Prediction: every render dial can be written as a parameter of p(percept | reading, observer). Any dial that CANNOT is misfiled (an engine dial in disguise). Audit target found already: the **mirage threshold** — if it only gates what is *shown* solid, it is render; if it changes what enters a compiled view, it is engine leaking into the viewer. Run the cast over the spec §1.4 table.
- **A3 — Dial-jump as policy improvement.** Prediction: across sweep history, law replacements (dial-jumps) are exactly the cells where held-out bits-per-action-cost improves — no jump should ever occur on a render or frame change alone. Testable on the sweep log as it accumulates.

## 6. On "sim"

Two readings, both load-bearing: **sim = simulation** (the frame is the observer's *running* generative model — favored by the active-inference reading, and it nests the coin: the observer's own wrapper has sharp and fuzzy regions, and they pose from the fuzzy edge) and **sim = sum/composition** (frame = wrapper ⊕ plane, the static composite). The protocol can stay agnostic: the composite is what the dials parameterize; whether it "runs" is the observer's business.

## 6b. Physical-instrument bounce (3 instruments, 2026-06-12)

Bouncing the frame/engine/viewer triple off real instruments to find where it clicks and where it strains.

| | **frame** (sim of wrapper ⊕ plane: what's asked) | **engine** (action space over L0: the moves, priced in bits) | **viewer** (infer the percept) |
|---|---|---|---|
| **Digital camera** | vantage + aim (plane), focal length/FOV, subject, the shot you intend (inferred) | exposure triangle, sensor, **ADC → bits literally**, optical low-pass filter, RAW capture | demosaic (Bayer = ⅔ of color is INFERRED), white balance, tone curve, sharpening, JPEG, the screen |
| **Radio telescope (EHT)** | where the dishes stand = an Earth-sized aperture (plane), baselines, frequency, the source | dishes+correlator → sparse samples of the Fourier/uv-plane, priced in SNR/coverage | CLEAN / regularized-ML reconstruction = p(image \| sparse visibilities, priors); M87 ring is ~99% inference |
| **Oscilloscope** | channel, **trigger** (what event you ask for), timebase, V/div | analog bandwidth + ADC sample-rate + bit depth; Nyquist lives here | dot-vs-vector display, **sin(x)/x interpolation** between samples, persistence grading |

**Three things the bounce confirms:**
1. **RAW vs JPEG = the four-tuple vs the baked view, exactly.** RAW keeps (frame, engine reading) and defers the render — re-derivable. JPEG bakes the render in, lossily — the percept overwrites the reading. The protocol's "save the four-tuple" is "shoot RAW."
2. **The percept is ALWAYS inference, even at the sharp end.** A normal photo is ⅔ interpolated color (Bayer demosaic). So viewer-as-inference is definitional, not just a fuzzy-end thing — the camera-end and telescope-end are the SAME viewer axis at different inference-ratios (a dial position, per the coin).
3. **The wiggle/mirage test is already how careful imaging science validates.** The EHT ran multiple INDEPENDENT reconstruction pipelines (different render-dial/prior settings) blind, and believed only features that survived all of them — "is the ring real or a hallucination of the priors?" answered the framework's way. The Samsung moon-photo scandal (a trained texture pasted onto blurry moons) is the canonical **broken-weld** violation shipped in a consumer product: rendered sharp what the sensor held fuzzy = never-render-fake-measured-bits, broken.

**What it TEACHES BACK (a category the protocol lacked): between-family artifacts.**
Oscilloscope **aliasing** (and its camera twin, **moiré**) is neither a render mirage nor frame-relativity — it is a **frame × engine MISMATCH**: the question is posed finer than the action can resolve (signal freq > ½ sample rate). The §2 attribution rule had three *within-family* variance meanings; this is a *between-family* artifact. The fix is itself a named dial — the **anti-alias / optical-low-pass filter** = deliberately blurring the frame to match the engine's resolving power. **Proposed addition to the protocol:** a fourth artifact class — *resolution mismatch* (frame asks finer than engine acts) — with the anti-alias dial as its control. The cosmic-coin analogue: asking next-MINUTE flux of a phenomenon whose lawful structure lives at 10-minute grain would alias; the quantization dial is partly an anti-alias control.

**Where the analogy STRAINS (the honest breakpoints):**
- **The camera is too clean.** Hardware-separated stages flatter the three-way split; in the framework the families are entangled (your wrapper informs which engine-action you'd even attempt). The camera over-sells separability.
- **Cross-family dials exist.** Aperture is an engine setting (light) whose depth-of-field effect isolates the subject (frame-like); focus selects the subject plane (frame) via an optical setting (engine-ish). This mirrors the observer-appears-twice wrinkle — some dials have cross-family effects, which is the interaction structure, not a flaw.
- **The camera observer is EXTERNAL** (photographer ≠ camera), but the framework's observer is partly CONSTITUTED by the frame (their wrapper IS the frame). The EHT is the better mirror here: the priors baked into the reconstruction ARE the observer's wrapper, so the percept is openly observer-relative.
- **Plane under-represented by the camera** (it captures one optical plane). The radio telescope captures a plane invisible to the eye — a cleaner illustration of plane = "what your instrument can even capture," closer to the physical/latent/straddle sense.

**§6c — The user steps into the analogy (Pav, same day): the agnostic-instrument user is the photographer, and the substrate is the light.**

The earlier breakpoint ("the camera's observer is external") is resolved by putting the user — **AI or person, interchangeably** — INSIDE the analogy as the loop-owner:

| photographer | agnostic-instrument user |
|---|---|
| repositions the camera, re-aims | moves the instrument across planes/topics (frame: plane-side) |
| **changes lenses** — wide-angle ↔ macro | **rides the abstraction ladder** — generic rung ↔ instance rung (frame: wrapper-side) |
| focuses; hunts focus by wiggling it | iterates `inferred` at the membrane frontier — "focusing on specific topics to gather data **to find focus**" |
| **autofocus = maximize edge-contrast** | **the duel = maximize bits-saved** — finding focus IS finding the law that sharpens the question |
| half-press to meter before the shot | a cheap probe sweep before the full grid |
| reads the print, adjusts, reshoots | infers the render, moves the dials, sweeps again — the perception-action loop |

And the substrate question answers itself in the same optics:

- **Internet sources = REFLECTED light.** Facts arrive as photons already bounced off the world — testimony-light, secondhand by construction. Primary sources sit closer to direct illumination; the **Wikipedia monoculture is a single lamp lighting the whole scene** — same-lamp glare = testimony laundering, and **cross-route corroboration = multiple independent illuminants** (you only trust a shape lit from two angles — sweep-2's provenance-disjoint rule, stated in optics).
- **`facts/*.jsonl` = the RAW file.** Undeveloped, never edited (append-only doctrine = RAW immutability), every photon carrying **EXIF** (source, retrieved_at, agent = exactly the provenance fields).
- **Corroboration = exposure stacking.** Multiple independent exposures of the same region stacked → noise cancels → the membrane hardens. Astrophotography's stacking discipline IS the verification state machine.
- **The compiler = the prism + development.** `compile_substrate.py` refracts the mixed fact-light into ordered spectra — per-specimen / per-pair compiled views are different spectral decompositions of the SAME light; deterministic development (same RAW → byte-identical negative = the compiler's idempotence). The viewer then **prints from negatives** — the percept-inference stage, where enlarger dials (render) live.

**Strains, disclosed:** (1) internet light is not passive reflection — sources are themselves observers/emitters; testimony can lie, photons cannot; (2) the prism implies lossless separation, but the compiler makes development choices (bucket precedence, best-value selection = a development curve — the compiler carries engine-ish dials of its own, worth an A2-style audit); (3) EXIF can be wrong — provenance is claimed, not guaranteed (the verification machinery exists precisely because of this).

**Degenerate check (the edge of the ontology): a mercury thermometer.** Viewer ≈ identity (the meniscus IS the reading, no inference), engine = one fixed move (thermal expansion, no dial), frame = where you place it. The three-way split collapses toward frame-only — and that is *correct*: a simple instrument is one with a 1-element action space and an identity viewer. The families are always present; they can degenerate. (A Geiger counter is the other edge — bottom-of-dial: the reading is irreducibly Poisson-fuzzy, no engine action sharpens it, the "lawfully random" anchor of FINDINGS S5 made physical.)

## 7. Footer

Exploration register; no protocol text changed; convergence list stays 9. If this hardens: fold §2's sentence into DIAL_PROTOCOL_SPEC §1 as the definitional preamble, run A1–A3 as the first children, and the cross-model external pass (GPT-5.5 + Gemini) on the active-inference correspondence specifically — it is the most import-laden claim here and exactly where an outside check earns its keep.

codex
**External Review Verdict**

Bottom line: this is a useful exploratory MDL/provenance instrument, not a new information theory result. The probe's direction is credible under the stated frame and engine: Kepler compresses Mars positions much more than one-step persistence compresses GOES flare flux. But the stronger language around Solomonoff identity, "free energy", and novelty is overclaimed.

**Ranked Criticisms**

1. The Solomonoff claim is too exact. Solomonoff probability is not simply `2^-shortest_bits`; it is a sum over all prefix programs, with `K(x)` linked by the coding theorem only up to machine-dependent constants. MDL/log loss/codelength share the same bit currency, but `p(appearance)=2^-bits` is only exact for a specified predictive distribution or valid prefix code.

2. The probe mostly demonstrates a known asymmetry: a strong physical law for a smooth orbital process beats a weak baseline for a bursty solar process. That is not circular, but it is endpoint-selected and law-asymmetric. `harness.py` also counts only parameter bits for Kepler, not the law/program/background theory, so this is conditional MDL, not full algorithmic probability.

3. The "rate-of-change not amplitude" result is real under the persistence baseline, but partly tautological. In `harness.py`, flare residual is exactly `lf[t] - lf[t-1]`; Gaussian or Student-t surprise must track large increments. The M-class peak being cheap is expected because persistence predicts plateaus and slow decays. A regime-switching/template/multichannel flare model would likely reduce, though not necessarily erase, onset surprise.

4. The E-units rule is correct but standard. `FINDINGS.md sec 1` properly retires the absolute cross-phenomenon bit gap, but this is the familiar non-invariance of differential entropy/codelength under units, quantization, coordinate choice, dimension count, and alphabet. It is a good protocol guard, not a discovery.

5. There is a terminology bug: `DIAL_PROTOCOL_SPEC.md sec 2` says coder/predictive changes are ENGINE-dial variance, but `FINDINGS.md sec 4` calls the margin "a render knob" even though it is set by coder and predictive family. That should be fixed to "engine-calibration band." Otherwise the taxonomy blurs its own core distinction.

6. The active-inference mapping is plausible as analogy, weak as formal claim. "Frame/engine/viewer" maps loosely to belief/query/action/observation-model, but calling the bit duel "variational free energy" buys little unless you define priors, likelihoods, variational posteriors, policies, and expected free energy. As written, it is decoration more than machinery.

7. A number inconsistency needs resolution. `FINDINGS.md` repeatedly reports orbit sigma-shrink as 14.44 bits/dim, but `results.json` and `harness.py` imply `(85.23517071791309 - 43.30012280024418)/3 = 13.98` bits/dim under the displayed entropy convention. Maybe a different sigma convention was used, but then it must be named.

**Specific V1 Answer**

The Solomonoff/MDL identification is directionally useful but mathematically sloppy if stated as equality. The per-symbol LZMA check is a sanity check, not a validation of Solomonoff probability. The flare bracket `[hist 5.05, Gaussian 6.17]` with LZMA at `5.66` is plausible, but it only says the byte coder is in the expected range. The orbit "sandwich" handling is conceptually better than pretending iid entropy applies, but it is residual autocorrelation/coder behavior, not proof of algorithmic probability.

**Specific V2 Answer**

The rate-of-change finding is a law-relative signal, not an intrinsic solar fact. Under persistence, the law-breaking variable is the derivative by construction. The robust version is: "for this one-minute univariate persistence frame, flare uncertainty concentrates at positive onsets, not peaks." That is worth keeping. Do not generalize it to "surprise lives in derivatives" without better flare laws and other phenomena.

**Specific V3 Answer**

Correct, important operationally, but basic. Absolute bits can be compared only inside a fully specified communication task with shared precision and utility. They should not be compared as cross-phenomenon "hardness." The team deserves credit for catching and retiring the mistake, not for discovering a new law.

**Specific V4 Answer**

The three dial families are useful protocol engineering. They relabel known practices: framing, model/instrument calibration, visualization sensitivity, preregistration, and robustness analysis. "Render variance = mirage detector" is sound as a warning, but only one-way: a feature dying under a render sweep is render-dependent; a feature surviving render sweeps can still be an engine or frame artifact. "Resolution mismatch" is real, but it is standard aliasing/Nyquist/moire renamed.

**Specific V5 Answer**

Legitimate metaphor, overreach as ontology. The POMDP analogy is cleaner than the free-energy one. Active inference may inspire the loop, but no result in these files depends on Friston machinery.

**Specific V6 Answer**

Most prior art: Solomonoff induction, Kolmogorov complexity, Levin coding theorem, MDL/Rissanen, Shannon source coding, log loss, residual analysis, algorithmic statistics, rate-distortion, sensitivity analysis, sampling theory, POMDPs, and active inference.

Strongest skeptic line: this is elaborate repackaging of "good predictive models save bits; smooth lawful systems compress; bursty residuals cost log loss; vary your hyperparameters and visualization."

Most defensible narrow novelty: a provenance-bound workflow for rendering predictive compressibility as "sharpness," with explicit frame/engine/render attribution, engine bands instead of single numbers, frame variance treated as observable, and render wiggle used as visualization QA.

**Material Issues In The Files**

`harness.py` estimates predictive sigmas on the evaluated residuals and does not count those calibration bits; exploratory OK, confirmatory not OK.

The LZMA tests use int64 byte packing, which introduces representation effects from sign extension and integer magnitude. Good enough as a proxy, not a clean entropy estimator.

`FINDINGS.md sec 6` already notes orbit NLL miscentering. I agree it needs fixing or rewording as cross-entropy under a biased predictor.

Attack-script claims are not independently checkable from the embedded evidence because the attack scripts themselves were not included. Treat those numbers as reported, not externally verified.
2026-06-12T22:41:54.634481Z ERROR codex_core::session: failed to record rollout items: thread 019ebdfd-befb-7261-84c5-f9734c582625 not found
tokens used
33,158
**External Review Verdict**

Bottom line: this is a useful exploratory MDL/provenance instrument, not a new information theory result. The probe's direction is credible under the stated frame and engine: Kepler compresses Mars positions much more than one-step persistence compresses GOES flare flux. But the stronger language around Solomonoff identity, "free energy", and novelty is overclaimed.

**Ranked Criticisms**

1. The Solomonoff claim is too exact. Solomonoff probability is not simply `2^-shortest_bits`; it is a sum over all prefix programs, with `K(x)` linked by the coding theorem only up to machine-dependent constants. MDL/log loss/codelength share the same bit currency, but `p(appearance)=2^-bits` is only exact for a specified predictive distribution or valid prefix code.

2. The probe mostly demonstrates a known asymmetry: a strong physical law for a smooth orbital process beats a weak baseline for a bursty solar process. That is not circular, but it is endpoint-selected and law-asymmetric. `harness.py` also counts only parameter bits for Kepler, not the law/program/background theory, so this is conditional MDL, not full algorithmic probability.

3. The "rate-of-change not amplitude" result is real under the persistence baseline, but partly tautological. In `harness.py`, flare residual is exactly `lf[t] - lf[t-1]`; Gaussian or Student-t surprise must track large increments. The M-class peak being cheap is expected because persistence predicts plateaus and slow decays. A regime-switching/template/multichannel flare model would likely reduce, though not necessarily erase, onset surprise.

4. The E-units rule is correct but standard. `FINDINGS.md sec 1` properly retires the absolute cross-phenomenon bit gap, but this is the familiar non-invariance of differential entropy/codelength under units, quantization, coordinate choice, dimension count, and alphabet. It is a good protocol guard, not a discovery.

5. There is a terminology bug: `DIAL_PROTOCOL_SPEC.md sec 2` says coder/predictive changes are ENGINE-dial variance, but `FINDINGS.md sec 4` calls the margin "a render knob" even though it is set by coder and predictive family. That should be fixed to "engine-calibration band." Otherwise the taxonomy blurs its own core distinction.

6. The active-inference mapping is plausible as analogy, weak as formal claim. "Frame/engine/viewer" maps loosely to belief/query/action/observation-model, but calling the bit duel "variational free energy" buys little unless you define priors, likelihoods, variational posteriors, policies, and expected free energy. As written, it is decoration more than machinery.

7. A number inconsistency needs resolution. `FINDINGS.md` repeatedly reports orbit sigma-shrink as 14.44 bits/dim, but `results.json` and `harness.py` imply `(85.23517071791309 - 43.30012280024418)/3 = 13.98` bits/dim under the displayed entropy convention. Maybe a different sigma convention was used, but then it must be named.

**Specific V1 Answer**

The Solomonoff/MDL identification is directionally useful but mathematically sloppy if stated as equality. The per-symbol LZMA check is a sanity check, not a validation of Solomonoff probability. The flare bracket `[hist 5.05, Gaussian 6.17]` with LZMA at `5.66` is plausible, but it only says the byte coder is in the expected range. The orbit "sandwich" handling is conceptually better than pretending iid entropy applies, but it is residual autocorrelation/coder behavior, not proof of algorithmic probability.

**Specific V2 Answer**

The rate-of-change finding is a law-relative signal, not an intrinsic solar fact. Under persistence, the law-breaking variable is the derivative by construction. The robust version is: "for this one-minute univariate persistence frame, flare uncertainty concentrates at positive onsets, not peaks." That is worth keeping. Do not generalize it to "surprise lives in derivatives" without better flare laws and other phenomena.

**Specific V3 Answer**

Correct, important operationally, but basic. Absolute bits can be compared only inside a fully specified communication task with shared precision and utility. They should not be compared as cross-phenomenon "hardness." The team deserves credit for catching and retiring the mistake, not for discovering a new law.

**Specific V4 Answer**

The three dial families are useful protocol engineering. They relabel known practices: framing, model/instrument calibration, visualization sensitivity, preregistration, and robustness analysis. "Render variance = mirage detector" is sound as a warning, but only one-way: a feature dying under a render sweep is render-dependent; a feature surviving render sweeps can still be an engine or frame artifact. "Resolution mismatch" is real, but it is standard aliasing/Nyquist/moire renamed.

**Specific V5 Answer**

Legitimate metaphor, overreach as ontology. The POMDP analogy is cleaner than the free-energy one. Active inference may inspire the loop, but no result in these files depends on Friston machinery.

**Specific V6 Answer**

Most prior art: Solomonoff induction, Kolmogorov complexity, Levin coding theorem, MDL/Rissanen, Shannon source coding, log loss, residual analysis, algorithmic statistics, rate-distortion, sensitivity analysis, sampling theory, POMDPs, and active inference.

Strongest skeptic line: this is elaborate repackaging of "good predictive models save bits; smooth lawful systems compress; bursty residuals cost log loss; vary your hyperparameters and visualization."

Most defensible narrow novelty: a provenance-bound workflow for rendering predictive compressibility as "sharpness," with explicit frame/engine/render attribution, engine bands instead of single numbers, frame variance treated as observable, and render wiggle used as visualization QA.

**Material Issues In The Files**

`harness.py` estimates predictive sigmas on the evaluated residuals and does not count those calibration bits; exploratory OK, confirmatory not OK.

The LZMA tests use int64 byte packing, which introduces representation effects from sign extension and integer magnitude. Good enough as a proxy, not a clean entropy estimator.

`FINDINGS.md sec 6` already notes orbit NLL miscentering. I agree it needs fixing or rewording as cross-entropy under a biased predictor.

Attack-script claims are not independently checkable from the embedded evidence because the attack scripts themselves were not included. Treat those numbers as reported, not externally verified.
