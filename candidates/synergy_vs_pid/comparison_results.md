# Witnessed synergy gate vs proper PID synergy — head-to-head

**Tier-3 exploratory. Controlled ground truth only** (numpy, no torch/HF/network).
All numbers below were produced by running `compare.py` (which calls the two
committed estimators `witnessed_synergy.py` and `pid_synergy.py`) on the six
cases in `cases.py`. Reproduced here verbatim — nothing fabricated. The
real-substrate (model-merge) run remains the explicitly-owed later step.

- Environment: Python 3.12.9, numpy 2.4.6 (matches the upstream recalibration).
- Cases: shape (256, 256) float32, N = 65536 iid elementwise triples
  `(a_i, b_i, m_i)`; seeds `A=default_rng(1)`, `B=default_rng(2)`,
  `noise=default_rng(3)`.
- Witnessed gate: `Syn_wit*(b) = L_b(round(R_float / step_M(b)))`, where
  `R_float = M − float-lstsq affine fit of M on (A, B, intercept)`; pinned coder
  lzma preset 6; affine-span all-zeros floor `L0 = 1208 bits`; band
  `[16,12,8,6,4,3,2]`; `r_top = 2`; margin 2000 (`tau* = 3208 b`). Excess =
  `Syn_wit* − L0` = bits of genuinely non-affine content.
- PID: two literature-grounded estimators on the same triples, both in bits —
  Gaussian MMI PID (Barrett 2015) and binned Williams–Beer I_min PID (bins=8).
  Both calibrate correctly (XOR binned synergy 0.9687 bit; independent-noise
  synergy ~0 under both — see "PID estimator is calibrated" below).

---

## TABLE 1 — per-case synergy + verdict, both methods (REAL numbers)

| case  | predicted (wit) | WIT excess @b16 (bits) | WIT excess @r_top=2 | **WIT verdict** | PID synergy binned (bits) | PID synergy Gauss (bits) | **PID gate verdict** |
|-------|-----------------|-----------------------:|--------------------:|:---------------:|--------------------------:|-------------------------:|:--------------------:|
| SYN   | PASS            | 903,904                | 12,000              | **PASS**        | 1.5511                    | 0.5009                   | FLAG-SYN             |
| ADD   | FAIL            | 0                      | 0                   | **FAIL**        | 1.7051                    | **24.6142**              | **FLAG-SYN**         |
| ROT   | FAIL            | 0                      | 0                   | **FAIL**        | 1.4993                    | **24.4678**              | **FLAG-SYN**         |
| COPY  | NULL            | 353,376                | 0                   | **NULL**        | 0.0013                    | 0.0000                   | no-synergy           |
| ALLOY | FAIL@r_top      | 824,576                | 88                  | **FAIL@r_top**  | 1.6903                    | 2.3532                   | FLAG-SYN             |
| XOR   | PASS            | 734,080                | 128,400             | **PASS**        | 0.9687                    | 0.0000                   | FLAG-SYN             |

- **WIT excess** = bits above the affine-span floor `L0`. `0` ⇒ M is exactly in
  the affine span of (A, B) ⇒ FAIL. Real positive bits ⇒ non-affine structure.
- **PID synergy binned** = Williams–Beer I_min synergy. **PID synergy Gauss** =
  Barrett MMI synergy (`+inf` would mean a perfectly deterministic affine map;
  ADD/ROT report ~24.6 b because the float32 residual variance is ~1e-15, not
  literally 0 — the finite stand-in for the divergence).
- **PID gate verdict**: FLAG-SYN iff *either* PID estimator reports synergy
  ≥ 0.05 bit. This is the most charitable reading for the "gate = PID"
  hypothesis — it lets PID call a blend additive whenever it can.

---

## THE KEY QUESTION — does the witness FAIL the additive blends where PID FLAGS them?

The pilot showed the *naive* min-minus-joint synergy form mis-flags a pure
additive blend. The sharpened bar asks whether a **proper** PID is *also* fooled.
It is.

### ADD = 0.5·A + 0.5·B  (M exactly in the affine span)
- **Witnessed**: excess over floor = **0 bits at every b** (16→2) ⇒ **FAIL**.
  The affine quotient removes the entire affine reconstruction; nothing is left.
- **PID binned**: I_min synergy = **1.7051 bits** (Miller-Madow 1.7052).
- **PID Gaussian**: MMI synergy = **24.6142 bits** (`I(M;A,B)=25.1161`,
  max single-parent MI = 0.5019 → synergy = joint − max ≈ 24.6).
- **PID gate verdict: FLAG-SYN.**
- ⇒ **WITNESS FAILS, PID FLAGS → they DIFFER on ADD.**

### ROT = cos(π/5)·A + sin(π/5)·B  (still affine — a mixing rotation)
- **Witnessed**: excess = **0 bits at every b** ⇒ **FAIL**.
- **PID binned**: I_min synergy = **1.4993 bits** (Miller-Madow 1.4988).
- **PID Gaussian**: MMI synergy = **24.4678 bits** (`I(M;A,B)=25.2345`,
  max single = 0.7668).
- **PID gate verdict: FLAG-SYN.**
- ⇒ **WITNESS FAILS, PID FLAGS → they DIFFER on ROT.**

### Why the PID flag on ADD is genuine, not a binning artifact
A critic could object that the 1.7-bit binned synergy on a *linear* blend is just
finite-bin discretization noise. It is not. A bins-sweep on ADD vs the
independent-noise bias control (run inline; reproducible from the committed
files):

| bins | ADD I_min synergy | ADD synergy (Miller-Madow) | INDEP-NOISE synergy | INDEP-NOISE (MM) |
|-----:|------------------:|---------------------------:|--------------------:|-----------------:|
| 2    | 0.3104            | 0.3104                     | 0.0000              | −0.0000          |
| 4    | 0.8977            | 0.8977                     | 0.0005              | 0.0001           |
| 8    | 1.7051            | 1.7052                     | 0.0043              | 0.0001           |
| 16   | 2.6165            | 2.6168                     | 0.0407              | 0.0016           |
| 32   | 3.5858            | 3.5870                     | 0.3906              | 0.1023           |

On ADD the Miller-Madow debias barely moves the value (1.7051 → 1.7052) — so the
synergy is **real I_min content**, and it *grows* with resolution because the
deterministic affine relation becomes ever more sharply determined as the grid
refines. On the independent-noise control the same machinery sits at ~0 and MM
crushes the residual finite-bin bias (0.39 → 0.10 at bins=32). The ADD flag is
not bias; a proper PID genuinely reports the additive blend as synergistic.

**This is the affine-quotient differentiator, confirmed.** The witnessed gate
quotients out the entire affine span of (A, B) by construction, so a pure
additive blend lands on the floor (excess 0, FAIL). A PID synergy term has no
notion of "this joint information is just an affine remix of the parents" — it
counts the joint determination of M by the pair as synergy, and on a
deterministic blend that joint determination is large (binned 1.5-1.7 b) or
divergent (Gaussian MMI). On ADD and ROT the two methods give **opposite gate
verdicts**.

---

## FRAME-RELATIVITY DEMO — ALLOY verdict flips across resolution; PID emits one scalar

ALLOY = 0.5·A + 0.5·B + 0.1·(A·B): a small nonlinear interaction. Witnessed
synergy across the resolution band (excess over floor; "synergy present" iff
excess ≥ margin = 2000):

| b (resolution) | WIT excess (bits) | synergy present? |
|---------------:|------------------:|:----------------:|
| 16 (finest)    | 824,576           | **YES**          |
| 12             | 609,712           | YES              |
| 8              | 296,080           | YES              |
| 6              | 168,336           | YES              |
| 4              | 59,296            | YES              |
| 3              | 10,520            | YES              |
| 2 (coarsest)   | 88                | **no**           |

- **FINE frame (b=16):** excess = 824,576 → synergy **PRESENT**.
- **COARSE frame (b=2):** excess = 88 → synergy **ABSENT**.
- **The verdict FLIPS across the frame: True.** The 0.1·A·B interaction is
  resolved at a fine grid and driven sub-LSB (annihilated) on M's own grid at the
  coarse end. Witnessed overall verdict: **FAIL@r_top** (synergy at fine grain,
  gone by the coarse ceiling).

**PID on the same ALLOY gives one frame-free number:**
- binned I_min synergy = **1.6903 bits** — a single scalar.
- Gaussian MMI synergy = **2.3532 bits** — a single scalar.

PID is defined on fixed variables and has **no resolution / coarse-graining
parameter**. It cannot express "synergistic at this grain, additive at that
grain" — it emits one value (1.6903 b) and stops. The witnessed gate's resolution
band is a genuine degree of freedom PID does not possess. The flip in TABLE-above
is a verdict PID structurally cannot produce.

> Honest caveat on (i): the *raw scalar magnitude* of the witnessed synergy is of
> course frame-dependent for every case (it is a codelength on a grid), and one
> could argue PID's frame-freeness is a feature, not a bug. The non-trivial claim
> is narrower and it holds: there exists a case (ALLOY) where the witnessed gate's
> *binary synergy verdict* changes sign between two frames, and PID has no
> parameter that could be swept to reproduce that change. The capability — a
> resolution at which "additive" and "synergistic" are distinguished — is one PID
> lacks.

---

## PID estimator is calibrated (so the comparison is fair)

From `pid_synergy.py` (`python pid_synergy.py`), real numbers:

- **XOR** (`M = sign(A)·sign(B)`, the canonical PID-synergy archetype): each
  parent alone ~0 info (`I(M;A)=0.00002`, `I(M;B)=0.00008` bit); joint
  `I(M;A,B)=0.96877` bit; **binned I_min synergy = 0.96869 bit** (Miller-Madow
  0.96862) — HIGH, as PID requires. Gaussian MMI synergy on XOR = **0.00000 bit**
  (its documented blind spot: sign-XOR is second-order-uncorrelated, so the
  linear estimator cannot see it). The witnessed gate also PASSes XOR
  (excess 734,080 @b16 down to 128,400 @r_top) — agreement on the archetype.
- **Independent noise** (`M = fresh rng(99)`): Gaussian synergy 0.00001 bit;
  binned synergy 0.00426 raw → **0.00011 bit Miller-Madow** — both ~0, as
  required. CALIBRATION VERDICT printed: `ESTIMATOR CALIBRATED = True`.

So when PID flags ADD/ROT it is not a broken estimator — the *same* estimator
correctly reads XOR as synergistic and noise as not. A working PID flags the
additive blend; the witness floors it.

---

## Context — the naive min-minus-joint surrogate (the form R1 rejected)

For completeness, the in-pilot naive synergy form
`min(L(R_A), L(R_B)) − L(R_AB)` at b=16 (the thing R1 replaced), in bits:

| case  | naive syn_pid (bits) |
|-------|---------------------:|
| SYN   | 31,056               |
| ADD   | 880,448              |
| ROT   | 859,968              |
| COPY  | 112                  |
| ALLOY | 164,848              |
| XOR   | −122,440             |

The naive form ranks the additive blends ADD/ROT *above* the genuinely
synergistic SYN — and goes negative on XOR. This is the defect that motivated
the witnessed fix; the corrected witness (TABLE 1) instead floors ADD/ROT.

---

## Bottom line

**Does the witnessed gate do something plain PID cannot, or is it PID with extra
steps? On controlled ground truth, it does two things PID cannot.**

1. **(ii) Affine quotient — CONFIRMED, and it is the strong result.** On the pure
   additive blends ADD and ROT the witnessed gate returns **FAIL** (excess 0)
   while a proper PID returns **FLAG-SYN** (binned I_min synergy 1.70 / 1.50 b,
   robust under Miller-Madow and across bin counts; Gaussian MMI synergy ~24.6 b).
   The two methods give **opposite gate verdicts** on these cases. The gate is
   *not* "PID synergy reframed": it measures non-affinity (information outside the
   affine span of the parents), which is a strictly different quantity from PID
   synergy (joint determination of M by the pair). PID counts an affine remix as
   synergy; the witness does not.

2. **(i) Frame-relativity — CONFIRMED in the narrow sense.** The witnessed binary
   verdict on ALLOY flips between a fine frame (synergy present) and a coarse
   frame (synergy absent); PID emits a single scalar (1.6903 b) with no
   resolution axis to sweep. PID cannot reproduce the flip.

**The witnessed gate is NOT PID-equivalent at this test: True.** Both
differentiators fire. The cross-model critique ("mostly PID reframed") is refuted
*on this controlled ground truth* — the affine quotient is the decisive
difference, with frame-relativity a secondary capability. The honest scope limit
stands: this is synthetic numpy, and the gate's value on a real model-merge
substrate (where M, A, B are weight tensors and the affine span is a meaningful
null) is the owed next step — but the *conceptual* claim that the gate ≠ PID is
now backed by real bits, not assertion.

---

## Grounding (web-checked)

- **Williams & Beer (2010)**, *Nonnegative decomposition of multivariate
  information*, arXiv:1004.2515 — the original PID; I_min redundancy; synergy =
  information provided only by the sources jointly. (Confirmed: the framework
  decomposes joint MI into nonnegative redundant / unique / synergistic atoms.)
- **Barrett (2015)**, *Exploration of synergistic and redundant information
  sharing in static and dynamical Gaussian systems*, Phys. Rev. E **91**, 052802
  (arXiv:1411.2832) — for a univariate Gaussian target and arbitrary-dimension
  sources, every operationally-motivated PID collapses to the MMI PID:
  redundancy = min(I(M;A), I(M;B)), synergy = I(M;A,B) − max(I(M;A), I(M;B)).
  This is exactly the closed form `pid_synergy.py` implements.
- **Uzzi, Mukherjee, Stringer & Jones (2013)**, *Atypical Combinations and
  Scientific Impact*, Science **342** (6157), 468–472,
  doi:10.1126/science.1240474 — highest-impact science combines high
  conventionality with a tail of atypical (novel) combinations; the grounding for
  "two ideas welding into an emergent third that carries information neither
  parent carries alone."

### Reproduce
```
cd D:/PlatformOperator/research/pav/candidates/synergy_vs_pid
python pid_synergy.py        # PID calibration (XOR high, noise ~0)
python witnessed_synergy.py  # witnessed band + all-shots-match
python compare.py            # the head-to-head table + frame-relativity demo
```
