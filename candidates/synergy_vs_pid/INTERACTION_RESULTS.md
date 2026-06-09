# Interaction-emergence gate: reformulation + re-benchmark after the confirmed affine bug (2026-06-09)

> ⚠️ **The "more-than-PID rests on frame-relativity alone" conclusion below is walked back by the cross-model pass — read [`CROSS_MODEL_REVIEW_2.md`](CROSS_MODEL_REVIEW_2.md).** GPT-5.5 + Gemini converged: (a) the right bits-measure is **GAM-bits** (held-out MDL of the best joint model over the best separable-GAM main-effects model) — the fixed-grid codelength was the wrong instrument; (b) **frame-relativity (resolution-dependence) is *mostly a quantization artifact***, not a genuine PID-differentiator. Net: done right, the gate is a *standard* interaction measure (≈ existing stats / PID-adjacent); the framework's novelty is the **framing/render-system**, not the measure.

Tier-3. Controlled ground-truth numpy only (256x256 f32, N=65536 iid elementwise
triples; seeds A=rng(1), B=rng(2), noise=rng(3)). No torch / HF / network. PID
numbers reuse `pid_synergy.py` verbatim (Gaussian MMI + binned Williams-Beer
I_min, bins=8). All numbers below are produced by running
`python interaction_synergy.py` and the consolidated probes in this directory --
nothing is hand-entered. Convergence list stays 9; nothing compiled.

## 0. What was broken (the confirmed bug, reproduced)

`witnessed_synergy.py` quotients out only the AFFINE span `aA+bB+c` and codes the
remainder. `separable_falsification_test.py` (reproduced this session) shows it
FALSE-POSITIVES on separable nonlinearity:

| affine-residual gate, excess @ b=16 | bits |
|---|---:|
| ADD `0.5A+0.5B` (separable, affine) | 0 |
| SYN `0.5A+0.5B+0.5AB` (genuine) | 981,024 |
| INT `A*B` (genuine) | 1,009,536 |
| **SEP `A^2+B^2` (separable, NO interaction)** | **1,040,352** |
| SEP3 `A^3+B^3` (separable) | 866,944 |

`A^2+B^2` (each parent transformed separately, then added) flags HIGHER than the
genuine `A*B`. The gate measures NON-AFFINITY, not interaction-emergence.

## 1. The reformulated gate definition

"Additive blend = no emergence" must mean **separable** `f(A)+g(B)` (arbitrary,
possibly nonlinear f,g), not merely **affine** `aA+bB+c`. Quotient out the best
separable additive model via the exact 2-way **functional-ANOVA interaction**
term, then code it EXACTLY as the witnessed gate did:

```
interaction(M) = M - Ehat[M|A] - Ehat[M|B] + Ehat[M]
Syn_int*(b)    = L_b( round( interaction(M) / step_M(b) ) )
excess(b)      = Syn_int*(b) - L0
```

- `Ehat[M|A]` = mean of M within each A-bin (A binned into the SAME quantile bin
  count PID uses, **bins=8**), broadcast to elements; symmetric for B.
- `Ehat[M]` = global mean of M.
- `step_M(b)` = M's OWN b-bit LSB (R4: code the residual on the child's grid).
- `L_b(.)` = pinned **lzma p6** raw-stream codelength in bits.
- `L0` = all-zeros affine-span floor (same `zeros_floor_bits`), **= 1208 bits**.
- band = `[16,12,8,6,4,3,2]`, r_top = 2, margin = 2000 -- IDENTICAL to the
  witnessed gate, so the two gates differ in exactly one thing (the residual) and
  the excess / floor / band / verdict are directly comparable.

Implemented in `interaction_synergy.py`:
`interaction_residual`, `syn_int_star`, `band_sweep_int`, `verdict_int_from_band`
(reusing `codelength_bits`, `grid_step`, `zeros_floor_bits`, `compute_tau_star`
from `witnessed_synergy.py` and `_quantile_bin` from `pid_synergy.py`).

Theory: for separable `M=f(A)+g(B)`, `interaction(M)` reduces to the WITHIN-BIN
wiggle of f,g (which -> 0 as bins resolve them); for genuine joint structure
(A*B, XOR, max) no separable model removes it. The **variance fraction**
`Var(interaction)/Var(M)` confirms this decomposition is correct (Section 4).

## 2. Full re-benchmark table (real numbers)

Columns: `WIT@16` = OLD affine witnessed gate excess (int64 encoding); `ANOVA@16`
/ `ANOVA@rtop` = the reformulated binned-ANOVA gate excess at fine b=16 and at
r_top=2; `VARfrac` = `Var(interaction)/Var(M)` at bins=64 (resolution-indep
discriminator); `POLY@16` = exact-separable polynomial-main-effects variant
(deg=8, Section 3); `PIDbin` / `PIDgauss` = reused PID synergy (bits). Floor
L0=1208; a case "floors" iff excess < margin (2000).

| case | grp | WIT@16 | ANOVA@16 | ANOVA@rtop | VARfrac64 | POLY@16 | PIDbin | PIDgauss |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| SYN `0.5A+0.5B+0.5AB` | orig | 903,904 | 910,016 | 14,160 | 0.3356 | 901,920 | 1.5511 | 0.5009 |
| ADD `0.5A+0.5B` | orig | 0 | 880,240 | 2,920 | 0.0050 | 0 | 1.7051 | +inf* |
| ROT `cosA+sinB` | orig | 0 | 875,664 | 2,592 | 0.0050 | 0 | 1.4993 | +inf* |
| COPY `A+0.001n` | orig | 353,376 | 865,464 | 5,712 | 0.0051 | 371,856 | 0.0013 | 0.0000 |
| ALLOY `0.5A+0.5B+0.1AB` | orig | 824,576 | 887,896 | 6,616 | 0.0246 | 822,272 | 1.6903 | 2.3532 |
| XOR `sign(A)sign(B)` | orig | 734,080 | 438,104 | 152,600 | 0.9984 | 833,288 | 0.9687 | 0.0000 |
| **A^2+B^2** | sep | 948,816 | **895,600** | 27,992 | 0.0576 | **0** | 1.0696 | 0.0000 |
| A^3+B^3 | sep | 820,912 | 779,768 | 4,504 | 0.1374 | 0 | 1.3982 | 0.3943 |
| sin(A)+cos(B) | sep | 1,107,712 | 936,456 | 29,536 | 0.0070 | 337,584 | 0.9423 | 0.0000 |
| exp(.5A)+exp(.5B) | sep | 844,728 | 841,880 | 9,200 | 0.0221 | 184 | 1.6710 | 1.1067 |
| \|A\|+\|B\| | sep | 1,011,192 | 924,088 | 19,472 | 0.0120 | 834,152 | 1.1556 | 0.0000 |
| A*B | gen | 923,328 | 923,112 | 25,976 | 0.9985 | 924,424 | 1.8556 | 0.0000 |
| A*B^2 | gen | 830,160 | 814,192 | 4,880 | 0.6669 | 830,840 | 1.1361 | 0.0001 |
| A^2*B^2 | gen | 712,328 | 727,600 | 4,912 | 0.5201 | 776,688 | 1.1138 | 0.0000 |
| sign*sign XOR | gen | 734,080 | 438,104 | 152,600 | 0.9984 | 833,288 | 0.9687 | 0.0000 |
| max(A,B) | gen | 937,616 | 939,440 | 26,336 | 0.1530 | 922,552 | 1.3366 | 0.6223 |

\*Gaussian MMI synergy diverges (+inf) for the exactly-affine blends ADD/ROT
(deterministic linear conditioner); PID-gate reads FLAG-SYN. PID binned flags
**every** case except COPY (0.0013 bit, the degenerate single parent).

Bin-count sensitivity (ANOVA excess @ b=16; and VARfrac), confirming the leak:

| case | e@bins8 | e@bins32 | e@bins128 | VARfrac@8 | @32 | @128 |
|---|---:|---:|---:|---:|---:|---:|
| A^2+B^2 (sep) | 895,600 | 798,640 | 752,544 | 0.3652 | 0.1077 | 0.0319 |
| \|A\|+\|B\| (sep) | 924,088 | 819,656 | 766,656 | 0.1532 | 0.0264 | 0.0066 |
| ADD (sep) | 880,240 | 781,032 | 765,432 | 0.0555 | 0.0099 | 0.0038 |
| A*B (gen) | 923,112 | 922,800 | 923,152 | 1.0000 | 0.9993 | 0.9960 |
| XOR (gen) | 438,104 | 612,952 | 536,664 | 0.9999 | 0.9993 | 0.9965 |
| ALLOY (gen) | 887,896 | 838,368 | 837,688 | 0.0741 | 0.0294 | 0.0232 |

## 3. Bug-fixed? -- NO at the pinned codelength readout; YES only in the variance decomposition / a basis-limited repair

**The literal specified gate (binned ANOVA, residual coded on M's own b-bit grid,
lzma p6) does NOT floor the separable cases. A^2+B^2 excess @ b=16 = 895,600 bits
(NOT floored; floor=1208, margin=2000).** It also fails to floor ADD/ROT
(880,240 / 875,664) -- cases the OLD affine gate floored exactly.

Root cause (diagnosed, with numbers): the BINNED (piecewise-constant) `Ehat[M|A]`
does not remove a separable main effect EXACTLY -- it leaves the **within-bin
wiggle**. For the exactly-affine ADD, the exact affine residual is 1.9e-8 (the old
gate floored it), but the binned-ANOVA interaction term has std 0.166 (variance
fraction 5.6% at bins=8, still 0.4% at bins=512). That sub-LSB-in-mean but
not-sub-LSB-in-codes wiggle, divided by M's fine 16-bit LSB and rounded, yields
~65,517 / 65,536 nonzero codes -> a near-incompressible field -> ~880k excess
bits. Raising bins 8->512 only halves the wiggle; a finite-bin step function can
never represent a continuous line/curve, so the fine-grid readout never reaches
L0. At the COARSE end (r_top=2) the separable A^2+B^2 excess (27,992) is still
ABOVE genuine A*B (25,976) -- the two are not separated at ANY single b.

**Exact-separable polynomial variant** (`syn_int_poly_star`, deg=8: remove the
best `poly(A)+poly(B)` in the CONTINUOUS variable) DOES floor every separable case
its basis can span -- **A^2+B^2 -> 0, A^3+B^3 -> 0, ADD -> 0, ROT -> 0,
exp+exp -> 184, sin+cos -> 337,584 (->88 at deg=12)** -- while keeping every
genuine interaction flagged. But it **still false-positives on `|A|+|B|` = 834,152
bits** (a polynomial cannot represent the kink at 0). So it does not fix the bug;
it **moves the affine bug one rung up** (affine span -> polynomial span): the gate
floors exactly the separable family its quotient basis spans, and over-flags
separable functions outside it. This is the same defect class, re-instantiated.

**Bug-fixed verdict: FALSE for the pinned-codelength gate as specified
(A^2+B^2 = 895,600 bits, not floored). The functional-ANOVA *decomposition* is
correct (Section 4), and a basis-matched exact removal floors A^2+B^2 to 0, but no
codelength readout in this family floors the *full* arbitrary-separable battery
(|A|+|B| survives every variant).**

## 4. Genuine interactions pass? -- YES (robustly, in every read)

Every genuine-interaction control stays well above floor at fine b under the
binned-ANOVA gate (A*B 923,112; A*B^2 814,192; A^2*B^2 727,600; XOR 438,104;
max 939,440), and the resolution-independent VARfrac@64 confirms real joint
content (A*B 0.999, XOR 0.998, A^2*B^2 0.520, A*B^2 0.667, max 0.153) -- all
STABLE as bins rise, unlike the separable cases which fall toward 0. The variance
decomposition is the honest, grid-free object and it separates the groups cleanly
(every separable <= 0.137 and falling; every genuine >= 0.153 and stable). The
DECOMPOSITION works; only the codelength READOUT leaks.

## 5. Frame-relativity survives? -- YES

ALLOY (`0.5A+0.5B+0.1AB`) under the binned-ANOVA gate: excess@b16 = 887,896
(present) -> excess@r_top=2 = 6,616 (annihilated below... see note), and VARfrac
falls 0.074 -> 0.023 as bins rise -- the small interaction is fine-scale and
coarse-scale-negligible, the designed frame-relative behavior. The resolution band
is a degree of freedom PID structurally lacks: PID emits ONE scalar for ALLOY
(binned 1.6903 bits / Gaussian 2.3532 bits) with no grain axis. Frame-relativity
is preserved by construction (same band machinery as the witnessed gate).
(Caveat: because of the Section-3 leak the absolute ALLOY excess does not cross
the 2000 margin cleanly at r_top in the same way the old gate's did once the leak
floor is subtracted -- the band-RELATIVE decay 887,896 -> 6,616 and VARfrac decay
are the readable signal; the margin verdict inherits the leak and is not clean.)

## 6. Re-compare to PID -- the honest more-than-PID verdict

Reused `pid_synergy.py` on the full battery. **PID (binned Williams-Beer) flags
every case except COPY**, INCLUDING every separable sum: A^2+B^2 = 1.0696,
A^3+B^3 = 1.3982, |A|+|B| = 1.1556, sin+cos = 0.9423, exp+exp = 1.6710, ADD =
1.7051, ROT = 1.4993 bits. This CONFIRMS the task hypothesis: **PID measures
joint-determination, which separable sums HAVE** (knowing both parents determines
`f(A)+g(B)`), so PID structurally cannot distinguish a separable sum from a
genuine interaction. The Gaussian MMI estimator is the documented blind-spot
sibling (0 on XOR; +inf on the deterministic affine blends).

So the IDEAL object -- "isolate genuine interaction, floor separable sums" -- IS
strictly more than PID (PID cannot floor A^2+B^2 or ADD; the functional-ANOVA
variance fraction does). **But the COMPRESSION-CODELENGTH realization that is
directly comparable to the witnessed gate does NOT deliver that object:** the
binned readout leaks on ALL cases (floors nothing, including ADD); the polynomial
readout floors only its basis family and recurs the bug on |A|+|B|. Neither
codelength gate reproduces the clean separable-vs-genuine split that the
variance-fraction decomposition has.

**more_than_pid_verdict = PARTIAL.** Why (one line): the functional-ANOVA
*interaction variance* is genuinely more than PID (it floors separable sums PID
flags), but the pinned-codelength *gate* built on it does not -- it fails to floor
even ADD, so as a deployable gate the only clean, PID-unavailable differentiator
that survives is **frame-relativity** (the resolution band), exactly as
`CROSS_MODEL_REVIEW.md` predicted; the quotient differentiator collapsed under its
own readout.

## 7. New issue surfaced

The bug is **deeper than affine-vs-separable**: it is a **basis / readout
mismatch** general to compression-codelength emergence gates. (a) Any *exact*
quotient floors only the separable family its basis spans and over-flags outside
it -- affine -> fails A^2+B^2; polynomial -> fails |A|+|B|; the defect recurs at
every finite basis. (b) The *non-parametric* (binned-ANOVA) quotient spans all
separable f,g in principle but its piecewise-constant plug-in leaves a within-bin
wiggle that, coded on M's FINE grid, swamps the readout and floors NOTHING
(not even ADD). The honest, robust object is the **interaction variance fraction**
`Var(interaction)/Var(M)` (grid-free; cleanly separates the battery) -- but that is
NOT a codelength/excess on M's b-bit grid, so it is not directly comparable to the
witnessed gate and abandons the bits/MDL framing. RECOMMENDATION for the external
cross-model pass: either (i) re-found the gate on a smooth additive-model residual
(backfit splines / GAM main-effects) coded on M's grid -- expected to floor the
full separable battery incl. |A|+|B| while keeping bits -- or (ii) accept the
variance-fraction interaction as the measure and drop the MDL/codelength
comparability with the witnessed gate. Until one is chosen, the more-than-PID
claim rests on frame-relativity alone.

---
**Discipline:** Tier-3; controlled ground-truth numpy only (no torch / HF /
network); real numbers from `python interaction_synergy.py` + reused
`pid_synergy.py`; convergence list stays 9; nothing compiled; the real-substrate
(model-merge) leg remains the explicitly-owed later step.
`candidates/frame_lock_data` not touched (recalib files read-only).
