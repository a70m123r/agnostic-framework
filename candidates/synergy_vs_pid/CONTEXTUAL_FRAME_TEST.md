# Contextual frame-relativity test (Phase-2): does the emergence verdict GENUINELY change with CONTEXT/FRAME?

**Status:** ran, real numbers, honest. **Verdict: YES — genuine and principled, distinct from the grid artifact.**

Script: `contextual_frame_test.py` (this directory). Reuses the calibrated measures unchanged:
`cand_predictive_gain.py` (held-out R²[joint] − R²[additive]) and `cand_gam_anova.py`
(held-out functional-ANOVA interaction fraction). numpy + scipy only; no torch/HF/sklearn/network.
All numbers below are pasted from a real run on the exact controlled field
(A=rng(1), B=rng(2), noise=rng(3), shape (256,256)).

---

## The distinction being tested

- **ZOOM** = change RESOLUTION within a FIXED frame (the grid LOD sweep). **Came back a quantization artifact** — at coarse bins everything blew up underpowered; that killed the *resolution proxy*, not the framework's claim.
- **CONTEXTUAL SCALING** = adjust the FRAME ITSELF — the relevance / context / depth cutoff: **which sub-population** of the world and **which variables** are in scope. This is the observer-kernel change. **Not yet tested before now.**

Phase-2 question: does the SAME global system flip between *interactive* and *additive* when you change the **context/frame** (not the grid), in a **principled** way? Principle on offer: **locality of nonlinearity** — a product `A*B` is interactive globally but locally near-linear (a curve looks straight up close).

Two operationalizations, both changing the FRAME, NOT the grid resolution.

---

## OP (I) — Parent-range / sub-population (locality of nonlinearity)

Same system `M = A*B`. Re-measure emergence over relevance bands `{|A − a0| ≤ h}`, shrinking the
window `h`. Measure = held-out predictive gain `R²[joint(A,B)] − R²[additive f(A)+g(B)]`
(flag ≥ 0.05, floor < 0.05). Resolution stays adaptive (quantile bins) so each frame is at full
power for its own support — no coarse-bin starvation.

### a0 = 2.0 (off-center) — THE VERDICT GENUINELY FLIPS

| h (half-width) | n in band | A-range | gain_full | verdict | gain @ **equal-n=1010** | gam-frac |
|---:|---:|---:|---:|:--|---:|---:|
| 3.00 | 55029 | [−1.00,+4.41] | **0.7984** | INTERACTIVE | 0.7569 | 0.8883 |
| 1.50 | 19910 | [+0.50,+3.48] | 0.1507 | INTERACTIVE | 0.1761 | 0.1717 |
| 1.00 |  9994 | [+1.00,+3.00] | 0.0636 | INTERACTIVE | 0.0612 | 0.0704 |
| 0.60 |  4878 | [+1.40,+2.60] | **0.0254** | **additive(floor)** | 0.0285 | 0.0335 |
| 0.30 |  2125 | [+1.70,+2.30] | 0.0114 | additive(floor) | 0.0156 | 0.0079 |
| 0.15 |  1010 | [+1.85,+2.15] | **0.0025** | **additive(floor)** | 0.0025 | 0.0058 |

**The SAME system M=A\*B reads INTERACTIVE (0.80) framed over a wide A-range and ADDITIVE (0.0025) framed in a narrow band around a0=2.** Both calibrated measures (predictive gain *and* GAM functional-ANOVA fraction) flip together. This is the headline result.

### a0 = 0.0 (centered) — correctly does NOT flip (and that is the principle working)

| h | n | gain_full | verdict | rho_pred (Taylor law) |
|---:|---:|---:|:--|---:|
| 3.00 | 65340 | 0.8992 | INTERACTIVE | 1.0000 |
| 0.30 | 15469 | 0.9340 | INTERACTIVE | 1.0000 |
| 0.15 |  7849 | 0.9301 | INTERACTIVE | 1.0000 |

At the center a0=0, `M = (0+d)·B = d·B`: there is **no linear `a0·B` term** to dominate, so the cross
term `d·B` is the *whole* signal — no local linearization exists. The measure correctly stays
interactive at every band width, and the Taylor law (below) predicts exactly this (rho=1 ∀h). **The
measure is not fooled: it flips only where locality-of-nonlinearity actually applies (off-center) and
not where it doesn't (on-center).** That selectivity is itself evidence the effect is structural.

---

## Why this is a FRAME effect, not the grid/power artifact (the discriminators)

The grid sweep failed because "everything blew up underpowered" — the verdict moved for a
**measurement** reason (coarse bins lose power). Three independent guards show op(I) is **not** that:

### 1. Equal-n control — flip survives at FIXED sample size
Holding `n = 1010` across *all* bands (subsampling every frame to the smallest), the gain still
falls 0.757 → 0.0025 (column `gain @ equal-n` above). **Same n, opposite verdict → not a sample-size effect.**

### 2. Irrelevant-axis control — the decisive discriminator
Narrow the band on an **irrelevant axis Z** (independent of A,B). This drops n *exactly* like the
relevant-axis narrowing, but leaves the A,B frame of `M=A*B` untouched. A power artifact would floor
here too. It does not:

| h(Z) | n | gain (narrow Z) | verdict | A-frame @ **matched n** |
|---:|---:|---:|:--|:--|
| 3.00 | 65363 | 0.8925 | INTERACTIVE | n=55029 → 0.7984 |
| 1.00 | 44874 | 0.8909 | INTERACTIVE | n=44874 → 0.7998 |
| 0.60 | 29620 | 0.8917 | INTERACTIVE | n=29620 → 0.7993 |
| 0.30 | 15463 | 0.8893 | INTERACTIVE | n=15463 → 0.8094 |
| 0.15 |  7873 | 0.8855 | INTERACTIVE | n=7873  → 0.8072 |

**Same n-reduction, but narrowing the IRRELEVANT axis keeps gain pinned at ~0.89.** Only narrowing the
*relevant* axis's **range** moves the verdict. The driver is **what range of the relevant variable is in
frame**, never n. This is the clean separation the grid sweep never had.

### 3. The flip follows the Taylor curvature law quantitatively
In a band of half-width h, write A = a0 + d. Then `M = a0·B + d·B`; the best separable model absorbs the
`a0·B` (B-linear) and the d-dependence, leaving the cross term `d·B` as the irreducible interaction.
Interaction-to-total ratio `rho = Var(d) / (a0² + Var(d))`. Measured gain vs this law (realised Var(d),
realised mean_A per band):

| h | measured gain | law rho | ratio |
|---:|---:|---:|---:|
| 3.00 | 0.7984 | 0.8885 | 0.90 |
| 1.50 | 0.1507 | 0.1711 | 0.88 |
| 1.00 | 0.0636 | 0.0703 | 0.91 |
| 0.60 | 0.0254 | 0.0277 | 0.92 |
| 0.30 | 0.0114 | 0.0074 | (noise floor) |
| 0.15 | 0.0025 | 0.0018 | (noise floor) |

**Pearson corr(measured, h²-law) = 1.0000.** The decline shape is *predicted from first principles* (the
Taylor remainder of the product), with a constant ~0.9 efficiency factor across the entire flip. A power
collapse would not track `Var(d)/(a0²+Var(d))`. This is the signature of structure, not measurement.

### Direct contrast with the grid artifact (same system, fixed frame, vary the GRID)
| bins | INT=A*B gain | SEP=A²+B² gain |
|---:|---:|---:|
| 2 | 0.4031 | −0.0000 |
| 3 | 0.6263 | −0.0001 |
| 4 | 0.7370 | −0.0002 |
| 8 | 0.8922 | −0.0003 |
| 16 | 0.9563 | −0.0007 |

ZOOM keeps INT interactive and SEP floored at **all but the very coarsest** bins; the only movement is
underpower at bins 2–3 — a measurement defect of the proxy, the frame unchanged. **Contrast:** op(I)
*changes the frame* and produces a clean structural flip that obeys a curvature law. The two are
mechanistically distinct.

---

## SECOND CONFIRMATION — XOR, same locality law, different system

`XOR = sign(A)·sign(B)`; its nonlinearity is **local to the A=0 sign-seam**.

| frame | h=3.0 | h=1.5 | h=0.6 | h=0.3 |
|:--|---:|---:|---:|---:|
| **a0=0** (seam IN frame) | 0.982 | 0.985 | 0.994 | 0.997 → INTERACTIVE |
| **a0=2** (seam OUT of frame) | 0.868 | 0.0003 | 0.0030 | 0.0050 → **floors** |

Narrowing around a0=0 keeps the sign-seam in frame → stays interactive. Narrowing around a0=2 pushes the
seam out of frame → `sign(A)` becomes constant → `M = sign(B)`, a function of B alone = additive. **Same
locality-of-nonlinearity law, predicted direction, second system.** (This is why an earlier "XOR must not
floor" framing was wrong: XOR's nonlinearity *is* local to the seam, so it *should* floor off-seam — the
true power discriminator is the irrelevant-axis Z control above, which it passes.)

---

## OP (II) — Context variable C (in-scope vs out-of-scope)

`M = A*C` with C a real third variable (the B field). OUT of context the predictor space is `{A}`; IN
context it is `{A, C}`. Held-out R²:

| frame | predictor | held-out R² | reading |
|:--|:--|---:|:--|
| OUT of context | {A} | **−0.0002** | A alone cannot reach M → looks irreducible/emergent |
| IN context | {A, C} | **+0.8920** | M fully explained once C is in frame |
| | **explained by bringing C into frame** | **+0.8921** | |

**Same system, two frames, opposite verdict.** Out of context M looks like an irreducible emergent merge;
bring the relevant context variable C into scope and within each C-stratum `M = A·c` is **linear in A**,
fully explained — additive. The verdict flips with **what variable is in scope** (the relevance/depth
cutoff), not with the grid. A second, independent operationalization of the same conclusion.

---

## Verdict

**The emergence verdict GENUINELY flips with the CONTEXT/relevance-frame, in a principled way, and it is
distinct from the grid-resolution artifact.**

- Op (I): the SAME `M=A*B` is **interactive over a wide range of A (0.80) and additive in a narrow off-center band (0.0025)** — flipping on **both** calibrated measures.
- It is **not** the grid/power failure mode: it **survives equal-n**, it is **absent when an irrelevant axis is narrowed by the same amount**, and it **tracks the Taylor curvature law `Var(d)/(a0²+Var(d))` with r = 1.0000**.
- It is **selective and correct**: it does **not** flip on-center (a0=0), where no local linearization exists — exactly as the principle predicts.
- A **second system (XOR)** flips in the predicted direction by the same locality-of-nonlinearity law (seam in-frame vs out-of-frame).
- Op (II): a **second operationalization** (include vs exclude context variable C) flips the verdict 0.00 → 0.89 the SAME way, driven by what is in scope.

This is **observer-kernel frame-relativity, made real**: the locality-of-nonlinearity mechanism is a
principled, quantitatively-predicted law of *what region / what variables are in frame*, mechanistically
separate from the quantization artifact that the grid-resolution proxy conflated it with.

### Honest caveats (it is real, but bounded)
1. **It is a property of the FRAME and the FUNCTION, not a free dial.** The flip happens only where the
   true function has a dominant local linear term (off-center products; seams pushed out of frame). On a
   centered product or any genuinely non-local interaction kept in frame, narrowing does **not** flip it
   (a0=0 rows; Z-control). So "context-relativity" is real but **constrained by where the nonlinearity
   actually lives** — it is not "anything can be made additive by reframing."
2. **At the tiniest bands (h ≤ 0.3) the held-out estimator hits its own noise floor** (ratio drifts to
   ~1.4 while both numbers are ≲0.015). The verdict (floor) is robust there, but the precise magnitude is
   estimator-limited — the *law* is read from the wider, well-powered bands.
3. **Measure-relative threshold.** "flag ≥ 0.05" is a chosen cut; the *flip* (0.80 → 0.003, two orders of
   magnitude) is threshold-independent, but the exact h at which it crosses 0.05 is not canonical.
4. **Op (II) is a conditioning/common-cause story.** That a merge is "explained by a third variable once in
   scope" is the standard Simpson/confounding structure; what is *framework-relevant* is that it is the same
   relevance-cutoff dial as op (I), giving two faces (sub-population, in-scope variables) of one frame change.
