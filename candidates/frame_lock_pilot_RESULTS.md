# Frame-Lock Pilot — first real ΔL-in-bits computation (controlled ground truth)

> **Status:** Tier-3 PILOT, surfaced for Cowork+Pav ratification. **Nothing is promoted.** The cross-substrate convergence list stays at **9**; no tier advances.
> **Scope (honest):** controlled ground-truth weight tensors (numpy, fixed seeds, KNOWN verdicts). This is the disciplined first step — validate the metric against known answers BEFORE trusting it on real data (cf. Pilot-2, where a metric was validated on ground truth and FAILED). **This is NOT real HuggingFace model-merging.** That is an explicit LATER step (bar-to-promote leg 1, real-HF), not this one. No torch / HF / network was used.
> **What this delivers:** the FIRST actual `ΔL` in bits the protocol (`frame_lock_protocol_DRAFT.md §7`) has ever required. The protocol synergy clause was DEFINED, never DEMONSTRATED; this demonstrates it on ground truth, and reports both confirmations and refutations straight.

Pipeline (all absolute paths):
- estimator: `D:/PlatformOperator/research/pav/candidates/frame_lock_data/mdl_synergy.py`
- cases: `D:/PlatformOperator/research/pav/candidates/frame_lock_data/cases.py`
- lock: `D:/PlatformOperator/research/pav/candidates/frame_lock_data/lock_pilot.yaml`
- per-case drivers: `_run_syn.py`, `run_rot.py`, `run_copy.py`, `run_alloy.py`; diagnostics `diag_rot.py`, `diag_floor.py`; smoke `smoke.py`
- environment: python 3.12.9, numpy 2.4.6, pinned `lzma` `FORMAT_RAW` LZMA2 preset 6 (byte count reproducible-to-the-bit); `zlib(level 9)` and `bz2(level 9)` as error-bar siblings.

---

## (a) The lock and its called-shot predictions (filed BEFORE compute)

The lock was filed before any synergy value was computed. Its byte content hashes to:

```
sha256(lock_pilot.yaml) = 747ed7f26b8b8499648d2fd2cb961cbbaef6627a713cb189648b770f6af3713d
```

This hash was **independently recomputed from the on-disk file during this write-up and matches the locked value exactly** (20,686 bytes).

**Frame (k=1).** Single frame: knowledge / algorithmic (Top-Kanon / state substrate). `log2(k) = 0`. `C_frame` objects = float32 (256,256) tensors; morphisms = elementwise affine maps on the (A,B) span — the linear re-coordinatizations the 9f-bis witness quotients out.

**Resolution band (derived, child-anchored ceiling — P3b).** `b ∈ [16, 12, 8, 6, 4, 3]`; `r_floor = 16` (fine, S-faithfulness floor); `r_top = 3` (coarse, child-anchored W_C-faithfulness ceiling). The grid explicitly includes `r_top`. The verdict is taken at `r_top` AND required across the whole band.

**Threshold rule (lock-before-data; fixed before any data was seen).** `k=1`, so `tau_eff = base_delta` where `base_delta := Syn_wit(b=r_top=3)` on the COPY null case, plus `3 × bootstrap_sigma` of that same quantity (n=200, seed=12345). A case PASSES iff `Syn_wit(b) ≥ tau_eff` for EVERY `b` in the band including `r_top`; else FAIL. NULL = the COPY calibrator or any case indistinguishable from the null floor within error bars. **The RULE was fixed pre-data; the realized scalar is computed from the COPY measurement at compute time.**

**The five called shots (binary, pre-recorded in field 13f-analogue `called_shots`):**

| Case  | Construction (elementwise `*`)                   | Called shot (pre-compute)          | Rationale (pre-compute) |
|-------|--------------------------------------------------|-------------------------------------|-------------------------|
| SYN   | `0.5A + 0.5B + 0.5(A*B) + 0.01·noise`            | **predicted-PASS**                  | `A*B` is a genuine nonlinear interaction OUTSIDE the affine span, large amplitude (std≈1); `R_AB` should carry substantial structure at every `b` incl `r_top`. |
| ADD   | `0.5A + 0.5B`                                     | **predicted-FAIL**                  | Exactly in the affine span; best affine fit reconstructs M up to quantization noise → `R_AB ≈ floor`. Crux: `Syn_pid` should MIS-FLAG this as synergistic. |
| ROT   | `cos(π/5)·A + sin(π/5)·B`                         | **predicted-FAIL**                  | Pure linear combination (coupled-plate mixing angle), in the affine span; the 9f-bis quotient should annihilate it → `R_AB ≈ floor`. |
| COPY  | `A + 0.001·noise`                                | **predicted-NULL/FAIL**             | Degenerate single-parent copy; DEFINES the null floor (`base_delta`). By construction sits at ≈`tau_eff` → cannot exceed its own +3σ except by bootstrap fluctuation. Calibrator. |
| ALLOY | `0.5A + 0.5B + 0.1(A*B)`                          | **predicted-FAIL@r_top** (would-pass at fine r) | Same structure as SYN but 5× smaller nonlinear amplitude. Survives at `r_floor`; coarse `r_top` quantization should annihilate it → `Syn_wit ≈ floor` at `r_top`. Demonstrates P3b. |

---

## (b) The two estimators, and the subtlety of compressing deterministic functions

Let `A, B` = parent weight tensors, `M` = merged/child tensor, all `(256,256)` float32.

At resolution `b`: quantize `A,B,M` to `b`-bit uniform codes over EACH tensor's own `[min,max]` range, **applied BEFORE fitting** (so coarse quantization can annihilate fine structure). Order is strictly **quantize → fit → compress**. Then fit least-squares affine reconstructions on the flattened codes: `Mq ~ a·Aq + c` (residual `R_A`); `Mq ~ a·Bq + c` (`R_B`); `Mq ~ a·Aq + b2·Bq + c` (`R_AB`).

Codelength of a tensor `X` at resolution `b`: `L_b(X) = 8·len( lzma_RAW_preset6( bbit_int_codes(X).tobytes() ) )` bits (pinned headline coder), with `zlib(9)` / `bz2(9)` as error-bar siblings.

- **(1) WITNESSED synergy (the P1 non-additivity witness, operationalized):**
  `Syn_wit(b) = L_b(R_AB)` = bits of M NOT reconstructible from ANY affine combination of `(A,B)`. This quotients out linear re-coordinatizations of the `(A,B)` span — every `a·A + b2·B + c` is annihilated to its residual, giving the P1 rotation/basis invariance. Intended behaviour: `Syn_wit ≈ floor` for any M in the affine span (ADD/ROT/COPY), `> floor` only for genuine nonlinearity (`A*B`).

- **(2) NAIVE synergy (BES Theorem 4.4 / PID form, as literally written):**
  `Syn_pid(b) = min(L_b(R_A), L_b(R_B)) − L_b(R_AB)`.

### The load-bearing subtlety: compressing a deterministic (near-zero) residual

Coding an affine residual is NOT the same as coding a signal, and the naive choice **inverts the witness**. The naive reading — "re-quantize the residual over the RESIDUAL's own min..max, then compress" — fails for residuals that are essentially zero. ADD's `R_AB` is only sub-LSB quantization rounding; its tiny own-range gets STRETCHED across the full `2**b` code span, turning pure rounding into a maximum-entropy, incompressible hash → ~1.05 Mbit at `b=16`, **LARGER** than SYN's structured residual (~0.93 Mbit, which is more compressible). Under own-range coding ADD therefore out-scores SYN — exactly backwards.

This is the general hazard of running an MDL/compression estimator on the output of a deterministic fit: a residual that "should be zero" is a field of LSB rounding noise, and renormalizing its range maximizes its entropy. (Verified directly: the FLOAT-domain affine residual std is `0.000000` for ADD vs `0.497` for SYN — the math is right; only the residual-CODING was wrong.)

**Fix (implemented in `residual_codelength(R, ref=Mq, b)`):** code each residual on **M's own `b`-bit grid** (same LSB as the child), not on the residual's own range. Then "residual ≈ 0" → ≈ all-zeros → ≈ 0 bits, and a large structured residual costs real bits in M's code units. After the fix the absolute scales are correct (SYN `R_AB`=905k ≫ ADD=105k at `b=16`). The standalone `L_b(X)` keeps the brief's own-range form; ONLY residuals use the M-grid coding. **This subtlety is the single most important implementation finding of the pilot and is documented in the estimator docstring.**

---

## (c) Results table (per case)

**Realized threshold (computed from the COPY measurement at compute time, rule fixed pre-data):**
`base_delta = Syn_wit(COPY @ r_top=3) = 3912` bits; `bootstrap sigma (n=200, seed=12345) = 605.732` bits; **`tau_eff = base_delta + 3σ = 5729.196` bits.** (Independently reproduced during this write-up.)

### Headline table — called shot vs realized

| Case  | Called shot     | `Syn_wit(r_top=3)` | `Syn_pid(r_top=3)` | Realized verdict (witness, vs `tau_eff`) | Realized verdict (PID: does it exonerate?) | Matches called shot? |
|-------|-----------------|--------------------:|--------------------:|------------------------------------------|---------------------------------------------|----------------------|
| SYN   | PASS            | 94,336              | 18,976              | **PASS** (94,336 ≥ 5,729 by ~16.5×)      | PASS (`Syn_pid>0`, correct for SYN)         | **YES** |
| ADD   | FAIL            | 100,664             | 41,816              | **PASS** (100,664 ≥ 5,729 by ~17.6×) — *false PASS* | FAIL (PID = +41,816 > 0 → mis-flags additive as synergistic) | **NO** |
| ROT   | FAIL            | 101,792             | 27,360              | **PASS** (101,792 ≥ 5,729 by ~17.8×) — *false PASS* | PASS/flag (PID = +27,360 > 0 → mis-flags rotation as synergistic) | **NO** |
| COPY  | NULL/FAIL       | 3,912               | 0                   | **NULL** (3,912 < 5,729; sits at its own floor) | NULL (`Syn_pid ≈ 0`, correct)               | **YES** |
| ALLOY | FAIL@r_top      | 105,152             | 37,880              | **PASS** (105,152 ≥ 5,729 by ~18.4×) — *false PASS* | PASS/flag (`Syn_pid>0`)                     | **NO** |

> Verdict-column convention: "witness verdict" applies the LOCKED absolute rule `Syn_wit ≥ tau_eff` across the band. "PID verdict" reads whether the naive estimator correctly exonerates a non-synergistic case; for ADD/ROT a positive `Syn_pid` is a **mis-flag** (it asserts synergy where there is none).

### Per-`b` witness curves `Syn_wit(b)` (pinned lzma, bits)

| Case  | b=16    | b=12    | b=8     | b=6     | b=4     | b=3 (r_top) |
|-------|--------:|--------:|--------:|--------:|--------:|------------:|
| SYN   | 904,936 | 681,768 | 386,264 | 246,528 | 139,280 | 94,336      |
| ADD   | 105,376 | 106,248 | 105,720 | 105,904 | 104,880 | 100,664     |
| ROT   | 104,632 | 104,784 | 103,600 | 104,280 | 103,592 | 101,792     |
| COPY  | 355,080 | 138,856 | 43,480  | 16,232  | 5,816   | 3,912       |
| ALLOY | 825,240 | 611,000 | 299,880 | 181,008 | 116,696 | 105,152     |

### Per-`b` PID curves `Syn_pid(b)` (pinned lzma, bits)

| Case  | b=16    | b=12    | b=8     | b=6     | b=4    | b=3 (r_top) |
|-------|--------:|--------:|--------:|--------:|-------:|------------:|
| SYN   | 31,056  | 16,712  | 20,040  | 38,336  | 24,392 | 18,976      |
| ADD   | 880,448 | 641,608 | 361,448 | 232,720 | 92,576 | 41,816      |
| ROT   | 859,968 | 623,776 | 337,696 | 209,464 | 76,896 | 27,360      |
| COPY  | 112     | 320     | 0       | 0       | 0      | 0           |
| ALLOY | 164,848 | 135,616 | 171,352 | 157,616 | 81,232 | 37,880      |

### Contrast against the affine floor — `ΔWit(b) = Syn_wit(case) − Syn_wit(ADD)` (bits)

This is the quantity that actually behaves as the protocol's P1 witness intends (ADD defines the affine floor):

| Case  | b=16    | b=12    | b=8     | b=6     | b=4    | b=3 (r_top) |
|-------|--------:|--------:|--------:|--------:|-------:|------------:|
| SYN   | +799,560| +575,520| +280,544| +140,624| +34,400| **−6,328**  |
| ROT   | −744    | −1,464  | −2,120  | −1,624  | −1,288 | +1,128      |
| ALLOY | +719,864| +504,752| +194,160| +75,104 | +11,816| +4,488      |
| COPY  | +249,704| +32,608 | −62,240 | −89,672 | −99,064| −96,752     |

Reading: at fine `b`, SYN and ALLOY tower above the affine floor (hundreds of thousands of bits) while ROT sits AT the floor (±2k) — the witness separates nonlinear from affine cleanly. By `r_top=3` the separation collapses: ALLOY decays to +4,488 (the designed P3b annihilation), and **SYN actually dips BELOW the floor to −6,328** (its large product residual exceeds M's range and re-coordinatizes under the M-grid coding at 8 code levels).

### Error bars (compressor siblings at `r_top=3`, `Syn_wit` bits)

| Case  | bz2     | lzma (pinned) | zlib    | spread | verdict robust? |
|-------|--------:|--------------:|--------:|-------:|-----------------|
| SYN   | 80,320  | 94,336        | 108,576 | 28,256 | yes — smallest sibling clears `tau_eff` by ~14× |
| ADD   | 95,200  | 100,664       | 124,464 | 29,264 | yes — all ≫ `tau_eff` |
| ROT   | 96,640  | 101,792       | 126,576 | 29,936 | yes — all ≫ `tau_eff` |
| COPY  | 1,744   | 3,912         | 7,536   | 5,792  | mixed — bz2/lzma below `tau_eff`, zlib nudges marginally above |
| ALLOY | 94,472  | 105,152       | 129,608 | 35,136 | yes — all ≫ `tau_eff` |

Compressor ordering is stable across the band (`bz2 < lzma < zlib`; zlib = weaker compression → more residual bits). The only bootstrap CI computed is on the COPY null floor that sets `tau_eff` (`σ = 605.732` bits); no bootstrap CI was computed on the SYN/ADD/ROT/ALLOY witnesses themselves, but each sits ~95k bits above `tau_eff`, i.e. >150σ clear of the floor — so the (false) PASSes are not error-bar artifacts.

---

## (d) Headline findings (what the numbers actually say)

**1. Does the naive PID form mis-flag the additive blend as synergistic? — YES, decisively, exactly as predicted.**
`Syn_pid` is strongly POSITIVE for ADD (+880,448 bits @b16; +41,816 @r_top) and ROT (+859,968 @b16; +27,360 @r_top). The naive BES-4.4 / PID form calls a purely additive average and a pure rotation "synergistic." COPY (a copy) correctly gives `Syn_pid ≈ 0` (112 → 0). **This numerically proves the BES-4.4 `min(L_RA,L_RB) − L_RAB` form is insufficient on its own — it cannot distinguish "needs both parents" (true of any additive blend) from "genuine nonlinear interaction." This is the core motivation for the P1 witness, now exhibited in real bits rather than asserted.**

**2. Does the witnessed form separate SYN from {ADD, ROT, COPY}? — PARTLY: cleanly at fine `b`, but it FAILS at the locked threshold and at `r_top`.** Two distinct sub-findings, both honest:

- **(2a) As a CONTRAST against the affine floor, the witness IS load-bearing in `b ∈ [16..4]`.** `ΔWit(SYN)` runs +799,560 @b16 down to +34,400 @b4; `ΔWit(ALLOY)` runs +719,864 → +11,816; both ≫ ROT, which sits AT the floor (±2k). So `Syn_wit > floor` iff genuine nonlinearity — the P1 witness behaves exactly as the protocol intends — **at fine resolution**.

- **(2b) At `r_top=3` the witness LOSES discriminating power, biting even the genuine SYN case.** SYN's wit/elem (1.4395) drops BELOW ADD's (1.5360) and ROT's (1.5532); `ΔWit(SYN)@b3 = −6,328` (negative). With only 8 code levels, SYN's `0.5·A*B` structure quantizes too coarsely to beat the affine rounding-noise pedestal. This is the P3b child-anchored-ceiling phenomenon biting the genuine SYN case — internally consistent with the protocol's own "verdict at `r_top`" rule, but it means the clean "`Syn_wit>0` iff nonlinearity" reading **holds at fine `b` and fails at `r_top`**.

- **(2c) The LOCKED COPY-anchored absolute threshold does NOT separate the cases at the verdict level.** Under `tau_eff = 5,729` bits the witnessed verdicts are SYN=PASS, ADD=PASS, ROT=PASS, COPY=FAIL, ALLOY=PASS. Reason: COPY is a near-perfect copy whose affine residual ROUNDS AWAY (~0.06 bits/elem → 3,912 bits), so the COPY null floor sits far BELOW the affine-blend pedestal (~1.6 bits/elem ≈ 100k bits) that ADD/ROT/SYN/ALLOY all carry. **A COPY-derived `tau` can only exclude the degenerate single-parent copy; it cannot exclude affine blends.** The correct null for THIS witnessed quantity is the affine-blend floor (ADD/ROT defines it), NOT the copy floor. The cross-case ordering at `r_top` is in fact WRONG for an absolute rule: COPY=3,912 < SYN=94,336 < ADD=100,664 < ROT=101,792 < ALLOY=105,152 (SYN below the affine cases).

**3. Does ALLOY fail at `r_top` while showing synergy at fine `r` (P3b)? — The P3b ANNIHILATION is physically present and visible, but the VERDICT does not flip, because the threshold is mis-calibrated (not because annihilation failed).** `ΔWit(ALLOY)` decays monotonically +719,864 → +504,752 → +194,160 → +75,104 → +11,816 → +4,488 as `b` goes 16→3 — the `0.1·A*B` term is being progressively annihilated by coarse quantization, exactly as the called shot predicted. But under the locked COPY-anchored `tau_eff`, ALLOY's absolute `Syn_wit@r_top = 105,152` (the incompressible affine-rounding pedestal) still clears 5,729 by ~18×, so the rule returns PASS. **P3b is demonstrated as a mechanism (the fine-`b` synergy genuinely decays to the floor at `r_top`); it is NOT demonstrated as a verdict flip, because the COPY null floor is too low to be the right reference.** An exploratory ADD-anchored `tau` (≈103,207) separates SYN(FAIL@r_top) and ROT(FAIL) but STILL marks ALLOY PASS by ~1,945 bits — so even an affine-anchored null does not by itself recover ALLOY=FAIL@r_top; the ~1.6 bits/elem residual-rounding pedestal is the limiting factor.

---

## (e) Called-shot scorecard

| Case  | Predicted        | Realized (witness, locked rule) | Hit / miss |
|-------|------------------|----------------------------------|------------|
| SYN   | predicted-PASS   | PASS                             | **HIT** |
| ADD   | predicted-FAIL   | PASS (false PASS)                | **MISS** |
| ROT   | predicted-FAIL   | PASS (false PASS)                | **MISS** |
| COPY  | predicted-NULL   | NULL                             | **HIT** |
| ALLOY | predicted-FAIL@r_top | PASS (false PASS; annihilation present, verdict not flipped) | **MISS** |

Scorecard: **2 hits / 3 misses** against the locked absolute rule. Under the protocol's called-shot arithmetic (`headline_score = confirmed predicted-PASS − predicted-PASS misses`): SYN was the only predicted-PASS and it confirmed (+1); COPY's predicted-NULL confirmed (free null control, no credit, no penalty). The three predicted-FAIL cases that surprise-PASSed (ADD, ROT, ALLOY) are the substantive misses — and they MISS **for a diagnosable reason** (wrong null reference + incompressible affine pedestal), not noise. **Crucially, the cross-estimator comparison still lands:** on ADD/ROT the PID estimator emits a HUGE false-synergy signal (+880k/+860k @b16) while the witness puts those cases at the affine FLOOR relative to ADD (ΔWit ≈ 0) — so the witness IS load-bearing in the floor-relative reading even though the locked absolute threshold does not capture it.

---

## (f) Scope and negative/refuting results (stated straight)

- **Scope:** controlled ground-truth numpy tensors with known verdicts only. **NOT real HuggingFace model-merging** (TIES/DARE on real `θ_A, θ_B, θ_M`) — that is bar-leg 1's real-HF target and remains undone. No torch / HF / network was touched.
- **Refutation 1 (threshold clause).** The locked COPY-as-null rule does not separate the cases at the verdict level: under `tau_eff=5,729` the witnessed verdicts are SYN/ADD/ROT/ALLOY = PASS, COPY = FAIL. COPY's floor (≈ a degenerate copy) is mismatched to the witnessed estimator's actual noise floor (the affine-blend pedestal, ≈ 100k bits). **The protocol's null case for this estimator should be an affine blend (ADD/ROT) or a floor-relative contrast, NOT a copy.** An absolute `Syn_wit ≥ tau_eff` rule is the wrong decision rule; `ΔWit` against the per-band affine floor is what separates.
- **Refutation 2 (resolution dependence).** The clean "`Syn_wit > 0` iff genuine nonlinearity" reading holds at fine `b` and FAILS at `r_top=3`: even genuine SYN is annihilated to BELOW the affine floor at 8 code levels (`ΔWit@b3 = −6,328`). So the witness is resolution-sensitive in exactly the regime the protocol takes its verdict (P3b cuts both ways — it annihilates real synergy too).
- **Refutation 3 (ROT estimator pathology).** ROT = `cos(π/5)A + sin(π/5)B` is exactly affine (float lstsq recovers `(0.809017, 0.587785) = (cos π/5, sin π/5)`, residual max|r|≈2.2e-7). But because A, B, M are each quantized over their OWN `[min,max]` BEFORE fitting, the integer-code tensors do NOT satisfy the exact affine relation; the per-element code-rounding cross-talk (R_AB std ≈ 0.41 in M-code units) yields a wide ~104k-bit residual at every `b`. So `Syn_wit` does NOT collapse to the floor for a pure rotation — the witness carries a large quantization cross-talk pedestal for any non-identity affine mix with different per-tensor scales. This is precisely the kind of metric-on-ground-truth pathology the disciplined first step exists to catch (cf. Pilot-2).
- **What the comparison DID confirm (positive):** the naive PID mis-flags ADD/ROT as strongly synergistic (large +bits) while the witness, read floor-relative, puts them at the affine floor. The central hypothesis — that the naive BES-4.4 form is unsafe and the P1 witness is load-bearing — is **CONFIRMED in the right regime (fine `b`, floor-relative)** and the failure modes (absolute-threshold + `r_top` annihilation) are mapped, not hidden.
- **Estimator-dependence is the §3 hole, now exhibited.** `frame_lock_protocol_DRAFT.md §6` flags "the MDL `ΔL` is estimator-dependent … sharply decidable only on instrumented frames" and the formalization §3 calls estimator/threshold dependence "the single most exploitable hole." This pilot exhibits exactly that with real bits: the verdict depends on (i) how residuals are coded (own-range inverts it), (ii) which null anchors `tau`, and (iii) where in the band the verdict is read.

---

## (g) Bar-to-promote verdict

The §7 promotion bar has three legs:

1. **Compute the MDL synergy on model-merging weight-space across the full derived band incl. `r_top`, with error bars** — "the first actual `ΔL` in bits the protocol has ever required."
2. File a real `lock.yaml` before computing (STEP 0–3 end-to-end, called-shot recorded, hash anchored, lock a strict ancestor of the artifact).
3. **Exhibit the 9f-bis witness concretely on a PASS and a FAIL on the same rule.**

**Verdict: PARTIAL.**

- **Leg 1 (on CONTROLLED ground truth): MET.** A real `ΔL`-in-bits was computed across the full band including `r_top=3`, with compressor error bars, on tensors with known verdicts. **But leg 1's actual target — real HF model-merging weight-space (TIES/DARE on `θ_A, θ_B, θ_M`) — is NOT met.** This pilot is the disciplined ground-truth precursor, deliberately upstream of real merging.
- **Leg 2: MET in spirit (lock-before-data demonstrated).** A lock with binary called shots was filed and content-hashed (`747ed7f2…3713d`, recomputed and matching) before compute; the threshold rule was fixed pre-data and the realized scalar computed afterward. The git strict-ancestor / external-anchor mechanics (STEP 3 `T_lock`) were not exercised here (no git repo in this dir), so the tamper-evidence leg is demonstrated as content-hash discipline, not as commit-ancestry.
- **Leg 3 (the 9f-bis witness, PASS-and-FAIL on one rule): PARTIAL — and this is the substantive finding.** The witness was exhibited on a PASS-shaped case (SYN, genuine `A*B`) and FAIL-shaped cases (ADD/ROT, affine span) by ONE rule (`Syn_wit = L_b(R_AB)`). **Floor-relative, it discriminates** (ΔWit: SYN ≫ 0, ROT ≈ 0 at fine `b`) — the witness is load-bearing. **As an absolute locked threshold, it does NOT** (ADD/ROT false-PASS; SYN annihilated at `r_top`). So leg 3 is demonstrated to *work* as a contrast and to *fail* as an absolute gate — which refines, rather than satisfies, the protocol's synergy clause.

**Net:** leg-1-on-controlled-ground-truth + leg-3-witness is **PARTIAL/MET-with-refutation** — the ground-truth `ΔL` exists and the witness separates in the right regime, but the locked absolute-`tau` clause and the `r_top` verdict point are refuted on these known answers. This is the success condition for a Pilot-2-style disciplined first step: the metric was validated against known verdicts and its failure modes were caught BEFORE being trusted on real data.

**What the real-HF-model-merging step that remains looks like (leg 1 proper):**
1. Take real `θ_A, θ_B` (two fine-tunes of one base) and a real merge `θ_M` (TIES or DARE), per-tensor or per-layer.
2. Apply the SAME quantize→affine-fit→M-grid-residual→compress pipeline per weight tensor, across the derived band with a child-anchored `r_top` defined by W_C's own coarsest faithful grain.
3. **Carry the threshold refinement from this pilot:** anchor the null on an AFFINE blend (or use the `ΔWit` floor-relative contrast / residual-floor subtraction), NOT on a degenerate copy; and verify whether the `r_top` verdict point survives or whether genuine synergy is annihilated there as SYN was here.
4. Report with error bars (compressor siblings + bootstrap) and a pre-filed lock with git strict-ancestry, before computing.

The threshold/estimator refinements this pilot surfaced (re-derive the null on an affine-span anchor or a contrast-against-affine-floor witness; re-examine the `r_top` verdict) are flagged for ratification and were spawned as a follow-up task (`task_f03d8244`).

---

> **Discipline footer.** Tier-3 PILOT, surfaced for Cowork+Pav ratification. **Nothing is promoted.** The cross-substrate convergence list stays at **9**; no tier advances. Scope is controlled ground-truth numpy tensors with known verdicts — **NOT** real HuggingFace model-merging, which remains the explicit later step (bar-leg 1 proper). All numbers above were produced by the validated pipeline (`mdl_synergy.py` + `cases.py`, python 3.12.9 / numpy 2.4.6, pinned lzma FORMAT_RAW preset 6) and the lock hash, `tau_eff`, cross-case ordering, and `ΔWit` contrast were independently recomputed during this write-up. Negative and refuting results are reported as found; no PASS was railroaded.
