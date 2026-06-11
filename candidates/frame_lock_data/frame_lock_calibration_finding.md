# Frame-Lock ΔL Pilot — witnessed-estimator calibration finding (Tier-3)

> **Status:** Tier-3 PILOT FINDING for Cowork+Pav ratification. **Promotes nothing.**
> Cross-substrate convergence list stays at **9**. No tier advances.
> **Scope:** controlled ground-truth numpy tensors (256×256 f32, seeds A=rng(1)/
> B=rng(2)/noise=rng(3)), pinned compressor lzma p6. No torch/HF/network.
> **Provenance:** re-derivation of the witnessed-synergy null/threshold after the
> controlled run surfaced a calibration defect. Companion to `lock_pilot.yaml`
> (the committed lock) and `frame_lock_protocol_DRAFT.md` (§3 gates / §5 anchors /
> §7 bar-to-promote). Reproduce with `recalib_confirm.py` (+ `recalib_experiment.py`,
> `recalib_crossover.py`, `recalib_robustness.py`).

---

## 0. TL;DR

The committed pilot lock pins the witnessed-synergy verdict to
`Syn_wit(b) = L_b(R_AB) ≥ τ_eff` for all b, with `τ_eff` anchored on the **COPY**
null (`3912 + 3·605.73 = 5729.2 bits`). Run faithfully, that rule **refutes its own
called shots**: under it ADD, ROT, SYN **and** ALLOY all register PASS — only COPY
fails. The COPY-anchored floor separates *degenerate copy* from *everything else*;
it does **not** separate *affine-span* (ADD/ROT, should-FAIL) from *genuine
nonlinearity* (SYN, should-PASS), which is the separation the witnessed-synergy
clause exists to make.

Three independent defects were found, the first two fatal to *any* threshold on the
raw scalar:

1. **Pedestal, not floor.** Under quantize-FIRST-then-fit, an affine-span M does
   **not** give `R_AB ≈ 0`. `round(·)` does not commute with `a·Aq+b·Bq+c`, so the
   residual is a **rounding-commutator pedestal** of ~1.6 bits/elem (ADD/ROT, flat
   across the whole band). The lock's 9f-bis `invariance_claim` ("M in affine span ⇒
   R_AB at the quantization-noise floor ⇒ Syn_wit ~ floor") is **empirically false**
   as operationalized.
2. **Inversion at the ceiling.** At the coarse ceiling the raw codelength is dominated
   by M's value-distribution compressibility, not by structure. SYN (heaviest-tailed
   M) compresses to the **fewest** bits, so at b=3 the order is
   `SYN(94336) < ADD(100664) < ROT(101792) < ALLOY(105152)` — the should-PASS case
   scores lowest. **No monotone threshold can fix this.**
3. **Wrong null.** COPY is a degenerate *single-parent* copy, not an affine-span
   *two-parent* reference. Its witness (0.06 b/elem at b=3, but 5.4 b/elem at b=16)
   is neither the affine floor nor a clean null, and it sits ~18× **below** the
   affine pedestal — so anchoring τ on it passes every affine-span case.

**Corrected metric** (recovers all five called shots on the pinned lzma coder):

- **Witness** `Syn_wit*(b) = L_b( round( R_float / step_M(b) ) )`, where `R_float =
  M − (float least-squares affine fit of M on A,B)` and `step_M(b)` is M's b-bit LSB.
  Fitting on **floats** makes affine-span ⇒ `R_float ≡ 0` ⇒ all-zeros ⇒ floor (no
  pedestal); coding on the **child's** b-grid still drives a small interaction
  sub-LSB at coarse b (P3b annihilation preserved).
- **Null** = the affine-span **all-zeros floor** `L0(b)` (what ADD/ROT score), **not**
  COPY. `τ* = L0 + margin`; the lzma verdict is invariant for `margin ∈ [2000,10000]`.
- **r_top** = the child's **sub-LSB annihilation grain**. For the 0.1·A·B alloy that
  is **b=2**, not the pilot's pinned b=3 (b=3 was too *fine* — the old pedestal had
  *masked* the surviving 0.1·A·B bump there).

| case  | called shot      | corrected verdict (lzma) | mechanism |
|-------|------------------|--------------------------|-----------|
| SYN   | PASS             | **PASS**                 | 0.5·A·B resolves through r_top=2 (excess 12000 b) |
| ADD   | FAIL             | **FAIL**                 | affine-span ⇒ excess = 0 at every b |
| ROT   | FAIL             | **FAIL**                 | affine-span ⇒ excess = 0 at every b |
| COPY  | NULL             | **NULL** (upstream gate) | degenerate single parent (parent-count gate) |
| ALLOY | FAIL@r_top       | **FAIL@r_top**           | 0.1·A·B driven sub-LSB at b=2 (excess 88 b); would-pass @ fine r |

**All five match.** This is a Tier-3 finding only; it requires a **fresh lock** (the
committed `lock_pilot.yaml` cannot be retrofitted — changing the band/threshold
post-data is the resolution-shopping the protocol forbids, §4 INVALIDATES).

---

## 1. The defect, reproduced (pinned lzma, real pipeline)

`smoke.py` / `recalib_experiment.py` reproduce the headline numbers bit-for-bit.

**Raw witness `Syn_wit = L_b(R_AB)` (bits):**

```
  b       SYN       ADD       ROT      COPY     ALLOY
 16    904936    105376    104632    355080    825240
 12    681768    106248    104784    138856    611000
  8    386264    105720    103600     43480    299880
  6    246528    105904    104280     16232    181008
  4    139280    104880    103592      5816    116696
  3     94336    100664    101792      3912    105152    <- r_top
```

COPY-anchored threshold: `τ_eff = Syn_wit(COPY@3) + 3σ = 3912 + 3·605.73 = 5729.2 b`.
Every non-COPY case clears it at every b ⇒ **ADD, ROT, SYN, ALLOY all PASS**; only
COPY (3912 < 5729) fails. The amplitude-annihilation P3b trend is real
(`ALLOY−ADD` contrast decays `719864 → 4488` over b=16→3) but never crosses the
COPY-anchored τ.

**Why ADD/ROT are a pedestal, not a floor** (`recalib_experiment.py` Part A):

```
case    Mrange           affine_R2(float)   std(Rfloat)   corr(Rfloat, A*B)
SYN     [-5.66,+6.30]    0.668051           0.4973        0.9998
ADD     [-2.83,+2.88]    1.000000           0.0000       -0.0047
ROT     [-4.08,+4.36]    1.000000           0.0000       -0.0106
COPY    [-4.03,+4.40]    0.999999           0.0010        0.0046
ALLOY   [-2.29,+3.50]    0.980512           0.0994        1.0000
```

ADD/ROT have float-affine **R² = 1.000000, std(R_float) = 0** — they *are* in the
affine span. Their ~1.6 b/elem witness is entirely the quantize-first
rounding-commutator. SYN/ALLOY have `corr(R_float, A·B) = 0.9998 / 1.0000` — the
residual *is* the elementwise product (genuine non-affine structure). COPY's residual
is the tiny orthogonal noise (corr ≈ 0) — not structure, just a degenerate copy.

---

## 2. Honest evaluation of the three options

### (a) Anchor τ on an affine-span reference (ADD/ROT) instead of COPY — **insufficient**

`recalib_experiment.py` Part C: pooled affine floor + 3σ ⇒ `τ_a = 103771 b`.
Because of the **inversion** (defect 2), `Syn_wit(SYN@3) = 94336 < τ_a` ⇒ **SYN FAILS**,
while `Syn_wit(ALLOY@3) = 105152 > τ_a` ⇒ **ALLOY PASSES**. Both wrong. Re-anchoring
alone cannot work on a scalar that orders the cases backwards at the ceiling.

### (b) Contrast `Syn_wit(case) − Syn_wit(affine_floor)` — **insufficient**

`recalib_experiment.py` Part D, contrast vs ADD per b. At r_top=3:
`SYN = −6328`, `ROT = +1128`, `ALLOY = +4488`, `COPY = −96752`. The contrast is
**inverted** at the ceiling (should-PASS SYN most negative, should-FAIL ALLOY most
positive). The pedestal is distributional-noisy and does not cancel across cases with
different M-ranges; subtracting a fixed affine reference cannot rescue a scalar whose
sign is wrong.

### (c) Per-element normalization / residual-floor subtraction in `residual_codelength` — **the right idea; do it at the source**

The cheap reading (subtract an *estimated* pedestal) inherits (b)'s noise. The
**principled** realization is to remove the commutator where it is born: fit the
affine model on the **floats**. For affine-span M the float residual is identically
zero ⇒ the pedestal vanishes exactly ⇒ the affine-span case maps to the all-zeros
floor. Coding the float residual on the **child's b-bit grid** keeps the P3b
annihilation of small interactions. This is the corrected witness in §3.

> Trade-off, stated plainly: this changes the morphism fit from "least squares on the
> quantized codes" (lock field 3f / 6f; "quantize-FIRST is LOAD-BEARING") to "least
> squares on the floats, residual coded on the child grid." The **load-bearing** part
> of quantize-first — P3b annihilation of sub-LSB structure at the child-anchored
> ceiling — is *preserved* (it lives in the coding step, which is still on M's b-grid).
> The part that is removed is the **artifact** it also produced: the rounding pedestal.
> `diag_rot.py` already documented that the float residual is ~0 and the large raw
> witness is "genuine quantization-rounding structure" — i.e. the pedestal was a known
> artifact. Promoting float-fit to the verdict estimator is a protocol change to ratify.

---

## 3. The corrected metric

**Witness.** `Syn_wit*(b) = L_b( round( R_float / step_M(b) ) )`,
`R_float = M − (a·A + b·B + c)` from `numpy.linalg.lstsq` on the **floats**;
`step_M(b)` = M's b-bit LSB; residual codes shifted to start at 0, compressed with
the pinned lzma p6. Implemented as `mdl_synergy.syn_wit_star`.

**Null.** The affine-span **all-zeros floor** `L0(b) = codelength(zeros)`
(`mdl_synergy.zeros_floor_bits`) — what an exactly-affine-span M scores. Deterministic
(R_float ≡ 0 ⇒ identical bytes ⇒ σ = 0), so the COPY-style `+3σ` band collapses; the
threshold is `τ*(b) = L0(b) + margin` (`compute_tau_star`).

**r_top.** The child's coarsest faithful grain operationalized as the **sub-LSB
annihilation grain**: the coarsest b at which the should-FAIL alloy's interaction has
been driven to the floor. For 0.1·A·B that is **b=2**.

**Corrected witness across the band** (`recalib_crossover.py`, lzma; `L0 = 1208`):

```
  b       SYN       ADD       ROT      COPY     ALLOY     FLOOR
 16    905112      1208      1208    354584    825784      1208
 12    681840      1208      1208    115448    610920      1208
  8    386200      1208      1208      1208    297288      1208
  6    245016      1208      1208      1208    169544      1208
  4    127520      1208      1208      1208     60504      1208
  3     68784      1208      1208      1208     11728      1208
  2     13208      1208      1208      1208      1296      1208   <- r_top (corrected)
  1      1208      1208      1208      1208      1208      1208
```

Excess over floor (true non-affine content): ADD/ROT = **0 at every b** (pedestal
gone); SYN decays `903904 → 12000` (b16→b2, still resolved); ALLOY decays
`824576 → 88` (annihilated by b=2); COPY is noise at fine b, floor by b=8.

**Verdict (PASS iff `Syn_wit*(b) ≥ τ*` for every b from r_floor down to r_top):**

```
case   predict      verdict (lzma, r_top=2, margin=2000)
SYN    PASS      -> PASS         (excess ≥ 12000 b through r_top)
ADD    FAIL      -> FAIL         (excess = 0 everywhere)
ROT    FAIL      -> FAIL         (excess = 0 everywhere)
COPY   NULL      -> NULL         (degenerate single parent; upstream parent-count gate)
ALLOY  FAIL@r_top-> FAIL@r_top   (excess 88 b at b=2; would-pass for b ≥ 4)
```

**ALL FIVE CALLED SHOTS MATCH** (`recalib_confirm.py`). The match is **robust**: the
lzma verdict is unchanged for `margin ∈ [2000, 10000]` (a 5× range) because the
should-FAIL cases sit **at** the floor by genuine annihilation, not merely near a
threshold.

**Sibling-compressor error bars** at r_top=2 (excess over floor, bits):

```
case    lzma(pinned)   zlib    bz2
SYN           12000    8040   7184
ADD               0       0      0
ROT               0       0      0
COPY              0       0      0
ALLOY            88    2104     48
```

bz2 agrees (ALLOY → 48, annihilated). **zlib** leaves a 2104-bit near-floor residual
at the annihilation edge (ALLOY borderline on zlib only). Verdict is taken on the
pinned lzma coder; the zlib disagreement is exactly the coding-reproducibility error
bar the protocol already flags (§6).

---

## 4. Why r_top moved 3 → 2 (and why that is not resolution-shopping)

The protocol's child-anchored ceiling (P3b) is meant to be evaluated at the grain
where the alloy is **Vegard-additive** (synergy genuinely zero), closing the
resolution-shop. The pilot pinned r_top=3 as a proxy. The corrected witness shows that
at b=3 the 0.1·A·B interaction is **not yet** annihilated — it still carries 10520 bits
(0.18 b/elem, `corr = 1.0` with A·B). The **old pedestal had masked this** (under the
raw witness ALLOY@3 = 105152 ≈ ADD@3 = 100664, indistinguishable). So b=3 is *finer*
than the alloy's true bulk-additive grain; the genuine annihilation grain for 0.1·A·B
is **b=2**, where ALLOY → floor while the 5×-larger 0.5·A·B (SYN) still resolves.

Setting r_top by a **reviewer-recomputable function of the committed child** ("coarsest
b at which the child's float-residual is driven sub-LSB on its own grid") is *not* a
free dial — it is exactly the child-anchored ceiling the protocol intends, and it
closes the alloy exploit **more tightly** than the pinned b=3 did (the masking that
previously hid the surviving bump is gone). It does, however, require a fresh lock:
the committed `lock_pilot.yaml` fixed r_top=3 and the raw witness; running that rule
faithfully yields ADD/ROT/ALLOY = PASS (3 called shots refuted), which **is** the
honest pilot result under the locked rule (cf. the honesty clause and the Pilot-2
precedent it cites: a metric validated on ground truth and *failed*).

**Alternative kept on the record (fragile):** at the pinned r_top=3, all five shots
can be recovered with the corrected witness only by a threshold `τ*` whose excess sits
in `(10520, 67576)` (e.g. margin ≈ 20000–30000 b) — but that threshold is *unanchored*
and the separation is a knife-edge amplitude cut, not annihilation. The r_top=2
annihilation reading is preferred precisely because the verdict does not depend on
where in a window τ lands.

---

## 5. Honest register / what this does and does not establish

- **Promotes nothing.** Tier-3 pilot finding; convergence list stays at 9; no tier
  advances. Controlled ground-truth numpy only — not real model-merging (TIES/DARE,
  case 6 of §7) which remains the explicit later step.
- The committed lock's witness **fails to validate** against ground truth as written.
  The corrected witness + affine-span null + annihilation-grain r_top **does** recover
  all five ground-truth verdicts on the pinned lzma coder. That validation is a
  precondition, not a substitute, for the real-data run.
- **The synergy witness cannot distinguish structured interaction from unstructured
  noise.** COPY's float residual (0.001·noise) scores *high* at fine b (354584 at b=16)
  because incompressible noise is also "non-affine." COPY is NULL by the **upstream
  parent-count / pushout-degeneracy gate** (one parent), not by the synergy number —
  which is why COPY must **not** be the τ calibrator, and why gate order (parent-count
  before synergy, §2 STEP 4) is load-bearing.
- **Estimator dependence remains a real hole** (§6). The zlib error bar at the
  annihilation edge shows the verdict can wobble at the boundary under a weaker coder;
  the pinned-lzma verdict is robust but the bundle *requests* rather than *enforces*
  the coder.
- **Float-fit is a protocol change**, not just a threshold recalibration. It must be
  ratified (it alters lock fields 3f/6f's "fit on quantized codes" and the
  "quantize-FIRST" emphasis). The argument that it preserves P3b while removing only
  the artifact is in §2(c); ratifiers should confirm it on the real-merge substrate.

---

## 6. Reproduction

```
python smoke.py               # original pipeline + COPY-anchored verdict (the defect)
python recalib_experiment.py  # Part A defect mechanism; Parts C/D options (a)/(b) fail; Part E corrected witness
python recalib_crossover.py   # coarse-grain crossover: r_top=2 annihilation grain
python recalib_robustness.py  # lzma/zlib/bz2 error bars at r_top=2
python recalib_confirm.py     # CANONICAL corrected re-run: all 5 called shots match
```

New pipeline functions (added to `mdl_synergy.py`, originals retained — the
raw-vs-corrected comparison is the scientific point): `affine_residual_float`,
`zeros_floor_bits`, `syn_wit_star`, `compute_tau_star`, `band_sweep_star`,
`verdict_star_from_band`.

---

## 7. Information theory of the junk — incompressibility ≠ novelty

This section reframes the §1 defect. The rounding-commutator pedestal is not an
incidental implementation bug: it is **high-entropy quantization noise**, and the
witness mistook *incompressibility* for *novelty*. They are opposites that look
identical to a bit-counter, which is the whole problem.

### 7.1 The junk is independent quantization noise

Model each rounding as additive error, `round(x) = x + q`. For a perfect blend
`M = a·A + b·B` (ADD/ROT), quantizing FIRST gives `Aq = A + q_A`, `Bq = B + q_B`,
`Mq = M + q_M`, with the `q`'s the per-element rounding errors. Least squares
recovers the true coefficients `(a, b, c)`, so the residual is

```
R_AB = Mq − (a·Aq + b·Bq + c) = q_M − a·q_A − b·q_B.
```

The leftover is a linear combination of **three independent rounding-error fields**
(independent because A, B, M sit on different grids). Under the standard
high-resolution quantization model the `q`'s are ~uniform on `[−Δ/2, Δ/2]` and
approximately i.i.d. across the 65536 elements — so `R_AB` is a near-i.i.d. **noise**
field. `round(·)` does not commute with `a·(+)+b·(·)+c`, and that non-commutativity
*is* the pedestal. (Cf. quantization/dither theory — Bennett, Widrow: rounding error
as additive uniform noise is the founding fact of the field.)

### 7.2 Why it is incompressible, and why that fooled the witness

A compressor exploits pattern; an i.i.d. field has none, so its codelength approaches
its entropy and **cannot go below it** (Shannon source coding). The pedestal
(~1.6 bits/elem for ADD/ROT) is therefore essentially the **entropy of the residual
quantization-noise field** — a large bit-count made entirely of randomness.

The witness used "many bits / hard to compress" as a proxy for "structure not
reconstructible from the parents." But two opposite things both read as expensive:

- **genuine synergy** = information in M that is *novel* given (A,B) — costly because
  it is **structured-and-new**;
- **quantization noise** = information in M that is *random* — costly because it is
  **patternless**.

A raw codelength cannot separate them. The pedestal is the second masquerading as the
first.

### 7.3 The ceiling inversion is a corollary, not a fluke

Structure compresses; noise does not. So a structured leftover (SYN's `A·B`
interaction) can encode to **fewer** bits than an i.i.d. noise floor of comparable
energy — the genuinely-synergistic case can land **below** the affine "floor." This is
exactly the b=3 inversion (`SYN 94336 < ADD 100664`): not an accident of the data but
the predictable consequence of using incompressibility as a stand-in for novelty when
the floor itself is noise.

### 7.4 The junk is the exact opposite of synergy (PID reading)

Synergy is information about M present **jointly** in (A,B) and in neither alone. The
pedestal `q_M − a·q_A − b·q_B` is, by construction, **independent of (A,B)** — it is
rounding error, conditionally independent of the parents' values. So it contributes
**zero** to any honest synergy quantity and a **large positive** amount to the raw
bit-count: the witness added an independent-noise term exactly where synergy
contributes nothing. (This is also why degenerate COPY scores high at fine b — its
leftover is the independent `0.001·noise`, random not synergistic — and why COPY is
correctly NULL'd by the upstream parent-count gate, not by the synergy number.)

### 7.5 What the fix does, information-theoretically

The corrected witness (§3) fits on the **floats**, removing `q_A, q_B, q_M` from the
leftover *before* it is measured: `R_float = M − (a·A+b·B+c)` carries no quantization
noise, only the true non-affine structure. Coding `R_float` on the child's b-grid then
asks the **legitimate rate–distortion question**: does the interaction survive the
child's bit budget at grain b, or is it driven below the representable rate
(annihilated)? The "synergy vanishes at coarse grain" behavior (ALLOY at r_top) is
precisely an interaction falling below the child's rate. In MDL terms the corrected
witness counts the **structure (model) bits** of the leftover — the meaningful half of
a two-part code / Kolmogorov structure-function split — not the **noise bits** the raw
witness conflated in.

### 7.6 The sharper statement of the defect

> **Incompressibility ≠ novelty.** A description-length synergy surrogate must measure
> the *structured* component of what the parents cannot explain, not the raw conditional
> description length — because the latter is inflated by any noise the pipeline injects
> (here, its own quantization), and that noise is by definition parent-independent,
> hence anti-synergistic. The rounding pedestal was the measurement **contaminating its
> own readout with maximum-entropy junk.**

**Caveat (honest).** "Rounding error = clean i.i.d. uniform noise" is the
high-resolution idealization. At b=3 (8 levels) it is only approximate — the `q`'s are
neither perfectly uniform nor perfectly independent, and a value-distribution term
also enters — which is an *additional* reason the raw coarse-grain number is
untrustworthy and the structure-only measurement is preferable.
