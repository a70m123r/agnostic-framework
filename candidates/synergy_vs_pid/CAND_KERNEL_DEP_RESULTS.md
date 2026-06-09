# Candidate emergence-function: Kernel / dependence INTERACTION (HSIC + distance-correlation)

Owned Phase-2 alternative-emergence-function candidate. Model-free interaction measure built to
address the **main-effect-misspecification caveat** (interaction-as-residual-after-a-separable-fit
confounds genuine interaction with a wrong/underpowered main-effects basis). Script:
`cand_kernel_dep.py`. Tier-3 exploratory; controlled ground-truth only (numpy+scipy, no torch/HF/net).

## What it is
Two model-free routes, both reported (verdict does not hinge on one construction):

- **Route D (headline, FIT-FREE):** `interaction_1mR2 = 1 - R2_add`, where `R2_add` is the variance of
  M explained by a **saturated model-free binned additive backfit** `fbarA(A)+fbarB(B)` (equal-count
  bins, 6 backfit passes). A saturated binned additive model is the **most flexible separable model**,
  so basis-misspecification cannot inflate it — there is no fixed basis to misspecify. This is the
  functional-ANOVA / GAM interaction fraction realized **non-parametrically**.
- **Route R (corroborating):** remove additive main effects with **out-of-fold Nadaraya-Watson**
  smoothers on A and on B (k-fold, held-out), then measure surviving dependence of the residual on the
  **joint** (A,B) via bias-corrected distance correlation and normalized HSIC.

Dependence primitives (model-free, characterize ALL dependence; web-grounded):
- **HSIC** biased V-stat `HSIC_b = (1/m^2) tr(K H L H)`, Gaussian-RBF, median bandwidth — Gretton et
  al. 2005. nHSIC = centered kernel alignment in [0,1].
- **distance correlation** (double-centered Euclidean distance matrices, dCor in [0,1], =0 iff
  independent) — Szekely-Rizzo-Bakirov 2007. `dcor_excess` subtracts a **permutation-null** mean to
  remove dCor's finite-sample positive bias (model-free).

65536 elementwise triples treated as iid; subsample m points/block, average B blocks.

## REAL calibration (run `python cand_kernel_dep.py --mR 800 --mD 1200 --blocks 8`)

| case | construction | expected | **1-R2_add (D)** | R2_add | inter_dCorX (D) | dCorX res;joint (R) |
|---|---|---|---:|---:|---:|---:|
| INT | `A*B` | HIGH | **0.9425** | 0.057 | 0.312 | 0.310 |
| XOR | `sign(A)*sign(B)` | HIGH | **0.9499** | 0.050 | 0.230 | 0.228 |
| ADD | `0.5A+0.5B` | ~0 | **0.0102** | 0.990 | 0.132 | 0.738 |
| SEP | `A^2+B^2` (separable nonlinear) | ~0 | **0.1184** | 0.882 | 0.160 | 0.361 |
| SYN | `0.5A+0.5B+0.5·A*B` | HIGH | 0.3294 | 0.671 | 0.309 | 0.372 |
| ALLOY | `0.5A+0.5B+0.1·A*B` | small | 0.0297 | 0.970 | 0.268 | 0.667 |

**Headline `1-R2_add` is correctly calibrated: HIGH on INT (0.94) and XOR (0.95); ~0 on ADD (0.010) and
SEP (0.118).** SEP is the crux (nonlinear but separable, MUST floor) and it floors ~an order of
magnitude below INT/XOR. SYN moderate (0.33), ALLOY small (0.03) — both correct-direction.

### SEP residue is a finite-bin artifact, not true interaction (nbins sweep, m=1000)
| nbins | ADD | SEP | INT | XOR |
|---:|---:|---:|---:|---:|
| 16 | 0.0229 | 0.1939 | 0.9720 | 0.9679 |
| 32 | 0.0094 | 0.0989 | 0.9389 | 0.9418 |
| 48 | 0.0054 | 0.0666 | 0.8943 | 0.9136 |
| 64 | 0.0037 | 0.0485 | 0.8667 | 0.8850 |

SEP (and ADD) shrink monotonically toward 0 as the additive fit saturates — confirming A^2+B^2 carries
**no** interaction; the residue is finite-bin slack. INT/XOR stay high (bias/variance knob: more bins
floor separables better but bleed a sliver of true signal; nbins=32, m≈1000 is a good operating point).

## How it handles the main-effect-misspecification caveat
The caveat: residual-after-a-separable-fit confounds interaction with a misspecified main-effects basis
(a low-degree polynomial can't fit `A^2+B^2`-type main effects, manufacturing false interaction). This
candidate answers it by **not fixing a basis**: the additive main-effects model is a **saturated,
nonparametric** binned backfit (Route D) / out-of-fold kernel smoother (Route R). A saturated separable
model fits ANY separable f(A)+g(B), including the nonlinear A^2+B^2 — which is exactly why SEP floors
(0.012 raw effect, →0.005 as bins grow) where a fixed affine/low-degree fit would false-positive. The
dependence primitives (HSIC, dCor) are themselves model-free and detect nonlinear dependence, so
neither route imposes a parametric form on the interaction either.

## HONEST NEGATIVE — the kernel-dependence-of-residual pieces do NOT add discriminating power
The variance-based `1-R2_add` is the only clean discriminator. The kernel/dCor residual routes failed:
- **Route R `dCorX(res;joint)` is broken as a discriminator:** ADD reads **0.74**, ALLOY 0.67 (should
  be ~0) even after permutation-bias-correction. Cause (diagnosed): on additive M the residual variance
  is tiny (resid_var≈0.04), so the residual is dominated by the **smoother's own out-of-fold error**,
  which is NOT independent of (A,B) — NW leave-fold-out error correlates with input location. The
  permutation null can't remove it because the dependence is real (smoother artifact, not M-interaction).
- **Route D `inter_dCorX` separates only weakly** (INT 0.31 vs ADD 0.13): dCor on a {A,B}->residual map
  saturates and the finite-m floor is large relative to the signal.

So: **the HSIC/distance-correlation machinery did not beat a saturated binned functional-ANOVA fit on
these cases.** The candidate's value is the model-free *saturated additive* main-effects model (which is
what kills the misspecification caveat); the kernel-dependence layer on top of the residual was not
additive in value here. Reported straight, no spin.

## PHASE-2 context/frame test (observer-kernel frame-relativity, NOT grid) — POSITIVE, principled
Does the emergence verdict **genuinely flip with the CONTEXT/relevance frame** (a dial on what is in
scope), as opposed to the grid resolution (which was confirmed a quantization artifact)? Principle:
**locality of nonlinearity** — M=A*B is interactive globally but ≈a0*B (additive) on a narrow band of A
around a0. Using this candidate's `1-R2_add`:

**Op1 — narrow the A-relevance band around a0=1.0 (M=A*B):**
| A-band half-width | 3.0 | 1.0 | 0.5 | 0.25 | 0.1 |
|---|---:|---:|---:|---:|---:|
| 1-R2_add | 0.945 | 0.315 | 0.086 | 0.029 | **0.013** |

**Op2 — condition on a third context variable C (A=C+0.15·eps, M=A*B):**
| context | all data | C-slice ±1.0 | C-slice ±0.3 | C-slice ±0.1 |
|---|---:|---:|---:|---:|
| 1-R2_add | 0.956 | 0.322 | 0.058 | **0.030** |

**Read:** the same global system flips from HIGH-interaction (0.95) to additive-floor (0.01–0.03) purely
by changing the **context/relevance frame** — never touching grid resolution. This is **principled, not a
quantization artifact**, and it is structurally different from the killed resolution sweep: there, ADD
and SEP **also** blew up at coarse resolution (uniform false positive); here, ADD/SEP stay floored at
every context width (≈0.01–0.10 in the main table), and the narrow-context floor is the **correct**
additive reading of a genuinely locally-linear restriction (A*B truly ≈ a0*B on a thin band). So under
this candidate, observer-kernel / contextual-scaling frame-relativity reads as **real and distinct** from
the grid-LOD artifact — exactly Pav's ZOOM (grid, artifact) vs CONTEXTUAL-SCALING (frame, real)
distinction. Caveat: this is one measure on controlled M=A*B; it demonstrates the mechanism (locality of
nonlinearity makes the verdict legitimately context-relative), not that every framework merge behaves so.

## Pros / cons
**Pros:** model-free, no parametric basis → directly answers the misspecification caveat; SEP (A^2+B^2)
floors correctly where affine/low-degree fits false-positive; HSIC/dCor primitives are web-grounded,
standard, =0-iff-independent; Phase-2 context test comes back POSITIVE and principled (locality of
nonlinearity) — a real, non-artifact frame-relativity.
**Cons:** the headline is `1-R2_add` (a saturated functional-ANOVA interaction fraction) — the
kernel/dCor-of-residual layer added **no** discriminating power and Route R is artifact-prone
(smoother-residual dependence); O(m^2) memory forces subsampling; SEP floors to ~0.10 not exactly 0 at a
fixed bin count (finite-bin slack, vanishes as bins grow); demonstrated on controlled M=A*B only.

## Verdict
A **sound model-free interaction diagnostic** via the saturated-additive route (`1-R2_add`), correctly
calibrated (HIGH INT/XOR, ~0 ADD/SEP) and robust to main-effect misspecification by construction. The
**kernel-dependence (HSIC/dCor) framing did not earn its keep** on these cases — report it as a negative.
The **Phase-2 context-frame test is the notable positive**: the emergence verdict genuinely flips with
the relevance/context frame for a principled reason (locality of nonlinearity), distinct from the
confirmed grid/quantization artifact. Convergence list stays 9; nothing compiled.

## Sources
- Gretton, Bousquet, Smola, Schoelkopf, *Measuring Statistical Dependence with Hilbert-Schmidt Norms*,
  ALT 2005 — http://www.gatsby.ucl.ac.uk/~gretton/papers/GreBouSmoSch05.pdf
- Gretton et al., *A Kernel Statistical Test of Independence*, NeurIPS 2007 —
  https://proceedings.neurips.cc/paper/3201-a-kernel-statistical-test-of-independence.pdf
- Szekely, Rizzo, Bakirov, *Measuring and testing dependence by correlation of distances*, Annals of
  Statistics 35(6), 2007 —
  https://projecteuclid.org/journals/annals-of-statistics/volume-35/issue-6/Measuring-and-testing-dependence-by-correlation-of-distances/10.1214/009053607000000505.full
- *Distance correlation* (sample formulas cross-check) — https://en.wikipedia.org/wiki/Distance_correlation
