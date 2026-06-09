# RESULTS — does the witnessed synergy gate do something plain PID cannot?

> ⚠️ **HEADLINE WALKED BACK by the cross-model pass — read [`CROSS_MODEL_REVIEW.md`](CROSS_MODEL_REVIEW.md) first.** GPT-5.5 + Gemini confirmed the gate ≠ PID but Gemini predicted (and a run **confirmed**) that the affine-residual gate **false-positives on separable nonlinearity** (`A²+B²` flags *higher* than a real `A·B` interaction). So this doc's `more-than-PID` / `bar discharged on controlled ground truth` conclusion is **revised to NOT-discharged**: "additive" must mean *separable* (`f(A)+g(B)`), not merely *affine*; the gate needs reformulating to the functional-ANOVA interaction term before any more-than-PID claim stands.

**The sharpened bar.** GPT-5.5 and Gemini independently judged the framework a new
*instrument*, not a new field, and both flagged the synergy gate as "mostly
Partial Information Decomposition (PID) synergy reframed / redundant with PID." So
computing a synergy value is not enough. The gate must do something a **proper**
PID cannot, or it is PID with extra steps. This file answers that from the numbers
— honestly, in the direction they actually land.

**Register.** Tier-3 exploratory. Controlled ground truth only (numpy; no torch /
HF / network). Every number below was produced by running the committed scripts in
this directory; nothing is asserted from memory. The real-corpus / real-model-merge
run is the explicitly-owed next step and is **not** discharged here.

- Environment: Python 3.12.9, numpy 2.4.6 (matches the upstream recalibration).
- Cases (`cases.py`): shape (256,256) float32, N=65536 iid elementwise triples
  `(a_i,b_i,m_i)`; seeds `A=default_rng(1)`, `B=default_rng(2)`, `noise=default_rng(3)`.
- Reproduce: `python pid_synergy.py` · `python witnessed_synergy.py` · `python compare.py`.
- Companion narrative (more detail, same numbers): `comparison_results.md`.

---

## Headline

**Verdict: MORE-THAN-PID, on controlled ground truth.** The witnessed gate is not
PID-synergy reframed. It measures **non-affinity** — information in M outside the
affine span of (A,B) — which is a strictly different quantity from PID synergy
(joint determination of M by the pair). The decisive, bias-controlled evidence:
on a pure additive blend the witness returns FAIL while a *correctly calibrated*
PID returns strongly-synergistic — **opposite gate verdicts**. A second, weaker
differentiator (frame-relativity) also fires. The cross-model "mostly PID" critique
is **refuted on this synthetic substrate**; whether it survives a real corpus is
the owed step.

---

## The numbers (all run, all real)

### TABLE 1 — per-case synergy + verdict, both methods

| case  | WIT excess @b16 | WIT excess @r_top=2 | **WIT verdict** | PID binned I_min (b) | PID Gaussian MMI (b) | **PID gate** |
|-------|----------------:|--------------------:|:---------------:|---------------------:|---------------------:|:------------:|
| SYN   | 903,904         | 12,000              | **PASS**        | 1.5511               | 0.5009               | FLAG-SYN     |
| ADD   | 0               | 0                   | **FAIL**        | **1.7051**           | **24.6142**          | **FLAG-SYN** |
| ROT   | 0               | 0                   | **FAIL**        | **1.4993**           | **24.4678**          | **FLAG-SYN** |
| COPY  | 353,376         | 0                   | **NULL**        | 0.0013               | 0.0000               | no-synergy   |
| ALLOY | 824,576         | 88                  | **FAIL@r_top**  | 1.6903               | 2.3532               | FLAG-SYN     |
| XOR   | 734,080         | 128,400             | **PASS**        | 0.9687               | 0.0000               | FLAG-SYN     |

- **WIT excess** = bits of M above the affine-span all-zeros floor `L0 = 1208 b`.
  `0` ⇒ M is exactly in the affine span of (A,B) ⇒ FAIL. The witness codes only the
  float-lstsq residual `R_float = M − (aA+bB+c)` on M's own b-bit grid (R4),
  swept over the band `[16,12,8,6,4,3,2]` (R3), against the affine-span floor (R2),
  with no min-of-single-parent-residuals (R1).
- **PID binned** = Williams–Beer I_min synergy (bins=8). **PID Gaussian** = Barrett
  2015 MMI synergy. PID-gate = FLAG-SYN iff *either* estimator ≥ 0.05 bit (the most
  charitable reading for the "gate=PID" hypothesis — it lets PID call a blend
  additive whenever it can; it still flags ADD/ROT/ALLOY).

### The PID estimator is calibrated (so the comparison is fair)

- **XOR** (`sign(A)·sign(B)`, the canonical PID-synergy archetype): each parent alone
  ~0 info (`I(M;A)=0.00002`, `I(M;B)=0.00008` b); joint `I(M;A,B)=0.96877` b;
  **binned I_min synergy = 0.96869 b** (Miller-Madow 0.96862) — HIGH, as PID requires.
  Gaussian MMI synergy on XOR = **0.00000 b** (documented blind spot: sign-XOR is
  second-order-uncorrelated, invisible to a linear estimator). The witness also
  PASSes XOR (excess flat ~128,400 across the whole band) — agreement on the archetype.
- **Independent noise** (`M=fresh rng(99)`): Gaussian synergy 0.00001 b; binned raw
  0.00426 → **0.00011 b Miller-Madow** — both ~0. `ESTIMATOR CALIBRATED = True`.

So when PID flags ADD/ROT it is **not** a broken estimator: the *same* estimator
reads XOR as synergistic and noise as not.

---

## Differentiators that SURVIVED the numbers

### (ii) The affine quotient — PRIMARY, strong, bias-controlled

On the two additive blends the methods give **opposite gate verdicts**:

- **ADD** = `0.5A+0.5B` (exactly in the affine span). Witness: excess **0 bits at
  every b** → **FAIL** (the float-fit removes the entire reconstruction; nothing is
  left). PID: binned I_min synergy **1.7051 b** (MM 1.7052), Gaussian MMI **24.6142 b** →
  **FLAG-SYN**.
- **ROT** = `cos(π/5)A+sin(π/5)B` (an affine mixing rotation). Witness: excess **0 at
  every b** → **FAIL**. PID: binned **1.4993 b** (MM 1.4988), Gaussian **24.4678 b** →
  **FLAG-SYN**.

**Not a binning artifact.** A bins-sweep on ADD vs an independent-noise bias control
(both run) shows the ADD flag is real I_min content, not discretization noise:

| bins | ADD I_min syn | ADD (Miller-Madow) | indep-noise syn | indep-noise (MM) |
|-----:|--------------:|-------------------:|----------------:|-----------------:|
| 2    | 0.3104        | 0.3104             | 0.0000          | −0.0000          |
| 4    | 0.8977        | 0.8977             | 0.0005          | 0.0001           |
| 8    | 1.7051        | 1.7052             | 0.0043          | 0.0001           |
| 16   | 2.6165        | 2.6168             | 0.0407          | 0.0016           |
| 32   | 3.5858        | 3.5870             | 0.3906          | 0.1023           |

On ADD, Miller-Madow barely moves the value (1.7051→1.7052) — genuine synergy that
*grows* with resolution as the deterministic affine relation sharpens. On the noise
control, MM crushes the finite-bin bias (0.39→0.10 at bins=32). The PID flag on the
additive blend is real.

**The sharp, telling sub-result:** PID rates the *pure additive blend* (ADD,
binned 1.7051 b) as **more synergistic than the genuinely nonlinear SYN** (binned
1.5511 b). That inversion is the pathology the affine quotient exists to remove —
the witness floors ADD (0 b) and passes SYN (903,904 → 12,000 b). PID has no notion
that "this joint information is just an affine remix of the parents"; it counts the
pair's joint determination of M as synergy, and an affine blend *maximizes* joint
determination. **This is the decisive differentiator: the gate ≠ PID synergy.**

> Honest caveat on the Gaussian "24.6 b": that number is a *divergence artifact*,
> not higher-order synergy. ADD is deterministic, so `Var(M|A,B) ≈ 1e-15`,
> `I(M;A,B) → ∞`, and MMI synergy = joint − max-single blows up. It is the correct
> finite stand-in for the divergence, but the *load-bearing* "PID flags the additive
> blend" evidence is the **binned I_min 1.70 b** (finite, bias-controlled), not the
> Gaussian number. Reported this way so the result is not overclaimed.

### (i) Frame-relativity — SECONDARY, confirmed only in the narrow sense

ALLOY = `0.5A+0.5B+0.1(A·B)`. The witnessed **binary verdict flips across resolution**:

| b (resolution) | WIT excess (bits) | synergy present? (excess ≥ 2000) |
|---------------:|------------------:|:--------------------------------:|
| 16 (finest)    | 824,576           | **YES**                          |
| 8              | 296,080           | YES                              |
| 4              | 59,296            | YES                              |
| 3              | 10,520            | YES                              |
| 2 (coarsest)   | 88                | **no**                           |

Fine frame → synergy PRESENT; coarse frame → synergy ABSENT (the `0.1·A·B` interaction
is driven sub-LSB on M's own grid at b=2). PID on the same ALLOY emits **one frame-free
number** (binned 1.6903 b; Gaussian 2.3532 b) with **no resolution / coarse-graining
parameter** — it structurally cannot say "synergistic at this grain, additive at that
grain." PID has no knob that could be swept to reproduce the flip.

> Honest caveat on (i): the *raw scalar magnitude* of witnessed synergy is
> frame-dependent for **every** case (it is a codelength on a grid), and PID's
> frame-freeness can legitimately be read as a feature, not a bug. The non-trivial,
> defensible claim is the **narrow** one: there exists a case (ALLOY) where the
> witnessed *binary verdict* changes sign between two frames, and PID has no
> parameter that could do likewise. This is real but weaker than the affine quotient.

### (iii) Tractability on high-dim — PLAUSIBLE but NOT measured here (do not claim)

The witness is O(N): one `lstsq` affine fit + one compressor pass. The Williams–Beer
binned PID needs a joint histogram over the composite source `(A,B)` — `bins²`
source cells — and the curse of dimensionality bites hard once "parent" means a
*weight tensor*, not a scalar: estimating I(M; A,B) for multivariate A,B is the
classic PID intractability. The Gaussian MMI PID stays closed-form but *is* the
affine model, so on high-dim it would inherit the very affine-blindness the witness
is built to escape. **This is a real structural advantage of the witness — but this
run does not measure it** (everything here is scalar elementwise triples). It is
listed as a *hypothesis the real-substrate step should test*, not as a discharged
result. No high-dim numbers were produced; claiming the tractability win now would
be fabrication.

---

## Where it is JUST PID (honest flags)

- **On XOR the two AGREE** (witness PASS, binned PID 0.97 b synergy). On a genuinely
  non-affine, non-additive interaction the gate carries no verdict information PID
  doesn't already carry. The gate's *distinctive* behavior shows up specifically on
  **additive / affine** inputs (where it floors and PID flags) and across
  **resolution** (where it flips and PID can't) — not everywhere.
- **At a single fixed frame, the witness is a codelength, and its scalar magnitude is
  frame-dependent.** If one pins one resolution and reads only the scalar, the
  "frame-relativity" differentiator evaporates; only the affine-quotient sign
  difference (FAIL-vs-FLAG on additive blends) remains. The strong claim rests on
  (ii), not (i).
- **The affine quotient is a *design choice*, not a discovered law.** The witness
  FAILs additive blends *because it is constructed to* (it subtracts the affine fit).
  That this matches the framework's "additive blend = no emergent third" axiom is the
  point — but it means the result demonstrates *internal consistency of the gate with
  its own thesis*, established against a PID baseline; it is not independent
  confirmation that non-affinity is the *right* notion of emergence. A real corpus
  with impact labels is what would adjudicate "right."

---

## Frame-relativity verdict

**CONFIRMED in the narrow (binary-verdict) sense; NOT in the scalar-magnitude sense.**
There exists a case (ALLOY) where the witnessed gate's *binary* synergy verdict flips
between a fine and a coarse frame, and PID — defined on fixed variables with no
coarse-graining parameter — cannot reproduce that flip. The scalar magnitude of the
witness is frame-dependent for all cases, so the honest claim is the capability
("a resolution at which additive and synergistic are distinguished"), not a
frame-invariant number. Secondary to the affine quotient.

## Uzzi differentiation

**DIFFERENT AXIS: rarity vs emergence.** Uzzi (2013, Science 342:468) measures the
*statistical rarity of a combination across a population* — a z-score that exists only
relative to a rewired-citation null, so every Uzzi quantity presupposes a corpus. The
witnessed gate measures *non-additivity of a single weld in information bits*, with no
reference to any population — it is computable at N=1. Four concrete contrasts:

1. **Population vs single-instance.** Uzzi's z-score requires a corpus null ("has this
   pairing been seen before, more/less than chance?"); the gate asks of one weld
   A,B→M "does M carry joint, non-affine structure beyond the parents' best additive
   combination?"
2. **Rare-but-additive passes Uzzi, fails the gate.** Two never-co-cited journals
   placed side-by-side with zero interaction give a maximally atypical z-score, yet the
   gate FAILs pure juxtaposition (the controlled ADD/ROT: excess 0 at every b).
3. **Common-but-emergent fails Uzzi, passes the gate.** A conventional (high-z),
   frequently-co-cited pair that nonetheless interacts nonlinearly reads as
   conventional to Uzzi yet PASSes the gate (SYN: residual corr ≈ A·B, excess 12,000 b
   through r_top). The two can be orthogonal.
4. **Frame-dependence.** Uzzi yields one number on fixed variables (frame-free, like
   PID); the gate's verdict changes with resolution (ALLOY). Uzzi has no analogue.

Net: Uzzi = *how unusual is the pairing in the literature* (a prior over combinations);
gate = *is the offspring more than the sum of its parents, here, at this grain* (the
function the combination computes). Rarity ≠ emergence.

---

## Bar status

**PARTIAL — discharged on controlled ground truth; the real-corpus / real-model-merge
leg is owed and env-blocked here.**

- **Discharged (synthetic):** A proper, calibrated PID (binned Williams–Beer I_min +
  Gaussian MMI) flags the additive blends ADD/ROT as strongly synergistic, while the
  witnessed gate floors them — **opposite verdicts**, bias-controlled (Miller-Madow,
  bins-sweep, calibrated on XOR=0.97 b and noise≈0). The gate is **not** PID-synergy
  reframed on this substrate. Frame-relativity confirmed in the narrow sense.
- **Owed (real substrate) — what the next step must deliver to move PARTIAL → full:**
  1. **Tractability**, actually measured: run the witness and a PID baseline where A,B,M
     are *weight tensors* (multivariate parents), and show the witness stays O(N) while
     the binned PID's source-cell count explodes. Not done here (all cases are scalar).
  2. **Incremental signal over Uzzi on a real corpus** (WoS/OpenAlex slice with a
     top-5%-citation HIT label): nested logistic `hit ~ Uzzi_median + Uzzi_tail`
     vs `+ gate_synergy`; the gate earns its keep iff the added term lifts out-of-sample
     AUC / log-loss and `corr(gate, hit | Uzzi) ≠ 0`. **NULL result to report honestly:**
     if gate synergy is collinear with Uzzi's tail z and adds no AUC and the
     disagreement cells are impact-flat, then on real data the gate is Uzzi-novelty (and
     PID-synergy) reskinned and the differentiation fails.
  3. **Frame-curve-as-feature:** test whether a merge's *annihilation grain* (the b at
     which it stops being synergistic) predicts impact beyond the scalar — something
     PID and Uzzi structurally cannot represent.
  4. **Real model-merge:** TIES/DARE-merged checkpoints A,B→M with a benchmark-delta
     label, where "combination" is literal weight composition and the affine span is a
     meaningful null. This is the substrate the framework still owes outright.

---

### Grounding (web-checked)

- **Williams & Beer (2010)**, *Nonnegative decomposition of multivariate information*,
  arXiv:1004.2515 — original PID; I_min redundancy; synergy = info provided only by the
  sources jointly; XOR = 1 bit synergy.
- **Barrett (2015)**, *Exploration of synergistic and redundant information sharing in
  static and dynamical Gaussian systems*, Phys. Rev. E **91**, 052802 (arXiv:1411.2832)
  — for a univariate Gaussian target + two predictors, every operationally-motivated PID
  collapses to MMI: redundancy = min MI, synergy = I(M;A,B) − max single MI, Gaussian MI
  via residual/conditional variance. Exactly the closed form `pid_synergy.py` implements.
- **Uzzi, Mukherjee, Stringer & Jones (2013)**, *Atypical Combinations and Scientific
  Impact*, Science **342** (6157), 468–472, doi:10.1126/science.1240474 — highest-impact
  science pairs high conventionality with a tail of atypical combinations; the grounding
  for the rarity-vs-emergence axis distinction.

---

## Discipline footer

Tier-3 exploratory. Controlled ground truth (numpy), **not** a real corpus — surprise
in real bits but scoped to synthetic tensors. Convergence list stays **9**. Nothing
compiled. The recalibration files in `frame_lock_data/` were treated **read-only**
(reproduced bit-for-bit, never edited). All numbers in this file were produced by
running `pid_synergy.py`, `witnessed_synergy.py`, and `compare.py` in this directory
(Python 3.12.9, numpy 2.4.6); no committed or recalib file was modified.
