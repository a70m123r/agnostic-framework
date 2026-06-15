# Multi-keyhole tomographic reconstruction

**Status:** SPEC-ONLY analysis. Slots into the hyperdimensional canonical-space viewer keystone (one logarithm, four jobs) and the COIN law (`rendered_sharpness(x) <= measured_bits(x)`). This document resolves the FIDELITY half of the keystone: HOW a region of the block earns its sharpness, and WHERE it is forced to stay blurry. Speculative items are marked `[SPEC]`.

---

## 0. One-paragraph thesis

A latent construct is a static N-D block-universe field `F(z,t)` that the apparatus does not observe all at once. It is reconstructed from many **keyhole-bursts**, each one a directional, time-windowed projection (a spreading-activation probe fired along a concept-angle at an event-time). Reconstruction is the regularized inverse that assembles `F` from the union of bursts. The block "gains fidelity and resolution as it compiles" is exactly the monotone accumulation of (Fisher / mutual) information toward the angular-Nyquist ceiling. The **fidelity law** says resolution grows with the independent, diverse measured-bits the bursts deposit — never with raw burst count — saturates at a knee, and cannot cross a hard error floor. That floor *is* the COIN: "never render a fake measured bit." Wherever concept-angles were never fired, a missing wedge of frequency space stays empty; the renderer is mathematically forced to **blur** there (not streak), and that blur is the honesty badge marking where conjecture-stubs attach.

---

## 1. The keyhole-burst as a projection, and the reconstruction operator

### 1.1 The forward model (one burst = one projection)

Let the latent construct be a field

```
F(z, t),    z in R^D  (construct's latent coordinate, e.g. democracy's axes),
            t         (event-time, the BEFORE/AFTER axis of the v0.3 wrapper).
```

A keyhole-burst `i` is a **linear measurement**:

```
y_i = P_i F + eta_i
```

- `P_i` = the keyhole/projection operator at **concept-angle** `theta_i` and **time-point** `tau_i`.
- `eta_i` = ping-back noise, covariance `Sigma_i`.

Concretely `P_i` is a directional line-integral (the Radon / X-ray transform) along concept-direction `theta_i`, restricted by a temporal window kernel `w(t - tau_i)`:

```
P_i F = integral  F(z, t) * delta(z . theta_i - s) * w(t - tau_i)  dz dt
```

This is the **excitation-emission keyhole made into geometry**, in exact correspondence with the v0.3 OBSERVATION primitive:

| Tomography object        | Keyhole / viewer primitive                              |
|--------------------------|---------------------------------------------------------|
| projection direction `theta_i` | shining a concept-definition `D(t_def)` (the probe vocabulary direction) |
| projection value `y_i`   | the sparks pinging back (spreading activation)          |
| burst noise `eta_i`      | keyhole + ping noise (caps usable resolution)           |
| time window `w(t-tau_i)` | the WHEN of the observation (event-time stamp)          |
| `measured_bits(y_i)`     | cap on usable resolution at this projection             |

So the block `B-hat` *is* the field `F`; bursts are its Radon samples on a `(concept-angle, time)` **acquisition manifold**.

### 1.2 The reconstruction operator (the compiler)

The compiler solves the regularized inverse problem:

```
F-hat = argmin_F  sum_i (1/2) || P_i F - y_i ||^2_{Sigma_i^-1}  +  lambda * R(F)
```

solved by **deep-unrolling** (DUN / MP-DUN) so every stage embeds the forward operator `P_i` *and* a prior `R`. Two exact readings, both load-bearing:

**(a) Fourier-slice reading.** By the Fourier Slice Theorem, `FT_1[P_theta F]` is a central slice of `FT_D[F]` along `theta`. Reconstruction is the inverse FT taken over the **union of measured slices only**. The filled k-space volume *is* `measured_bits`. Everything outside the union is, definitionally, unmeasured.

**(b) Filtered-backprojection reading.** The explicit operator is

```
F-hat = sum_i  P_i^* ( h * y_i )
```

with the ramp filter `h` **replaced by a COIN-clamped filter that has ZERO gain at unsampled frequencies**. This single substitution is what makes missing angles *blur* rather than *streak* — see §4. It is the structural enforcement the keystone demands (not post-hoc styling).

### 1.3 The lock condition (when a region of the block is "compiled")

Reconstruction LOCKS at a coordinate/axis when **all three** hold:

```
(L1)  KL( B-hat_{tau+1} || B-hat_tau ) < epsilon     # new independent bursts no longer move the posterior
(L2)  measured_bits(x, axis) >= disclosed_threshold  # enough independent bits accrued
(L3)  no rival hypothesis sits within delta evidence # the MAP is not contested
```

The lock is **per-axis**, not global: the missing wedge is anisotropic, so some axes (WHO, WHEN) lock while others (WHY) stay fuzzy. `[SPEC]` The deep name for L1+L2 is the **Kolmogorov structure-function kink / minimal sufficient statistic**: the model-complexity level where adding bits stops buying compression (before = structure discovered; after = fitting noise). Conjecture: the structure-function kink and the tomographic saturation knee (§2) are the **same point viewed twice** — observation->meaning->knowledge and angle-coverage->resolution as one curve. Strong if true; currently unshown.

---

## 2. The fidelity law (resolution vs number / diversity / independence of bursts)

The law has three exact forms collapsing to **one inequality with a hard floor**.

### 2.1 Form 1 — sample complexity (the floor in burst-count)

To stably recover an `s`-sparse construct you need

```
m  >~  s    (up to log factors)        [sparse-Radon CS theory, arXiv:2302.03577, J.Eur.Math.Soc.]
```

bursts. Fidelity scales with the number of bursts needed to cover the construct's **description-length** — never fewer. You cannot reconstruct a 100-bit construct from 10 bits of probing.

### 2.2 Form 2 — the angular-Nyquist / Crowther ceiling (the resolution ceiling)

Resolution along a direction requires

```
N_angles  ~  (pi/2) * N_features    over >= 180 deg of concept-coverage    [Crowther; PMC10081563]
```

Below it the construct stays aliased/fuzzy. The block "gains resolution as it compiles" *precisely by* accumulating distinct concept-angles toward this ceiling. **Diversity beats density**: 9 wide-range concept-angles >> many narrow ones (INR electron-tomography, arXiv:2512.08113, SSIM 0.957 vs 0.427). The fidelity term must therefore be a **coverage / condition-number over concept-angles and time-points**, scoring each burst by NEW band filled — not a tally.

### 2.3 Form 3 — the information form (the load-bearing one)

The per-burst meter is the **marginal conditional mutual information**:

```
dbits_i  =  I( F ; y_i | y_1 .. y_{i-1} )
         =  H(B-hat_before) - H(B-hat_after)
         =  EIG (expected information gain) = KL(posterior || prior)
```

This quantity is **submodular** — diminishing returns is a *theorem*, not a heuristic (Krause & Singh, JMLR 2008); greedy max-marginal-bits is within `(1 - 1/e)` of optimal. Three immediate consequences:

1. **An independent concept-angle adds a large `dbits`; a redundant re-fire adds ~0 automatically.** No special-casing — its Jacobian rows are already in the row-space of the accumulated information.
2. **Redundancy must be subtracted, not ignored.** Joint MI < sum of marginal MIs. Crediting bursts additively *fabricates measured_bits* and breaks the COIN. Use conditional MI for the increment.
3. **Effective count, not raw count.** Replace `N` with

```
N_eff = information-dimension / rank of {P_i}, weighted by source independence.
```

Ten outlets copying one wire = **one** projection with ten echoes. When two bursts may share an upstream source (re-derived facts, same route), fuse with **Covariance Intersection** (consistent for *any* unknown correlation), never independence-assuming addition (which is provably overconfident). "Corroborated > pending" must mean corroborated **by an independent route**; same-route repeats stay pending.

### 2.4 The two regimes + the COIN bite

```
error( N_eff )  ~  N_eff^(-1)            # information-limited regime (Cramer-Rao / Baker-Kanade)
              ->   plateau (knee)         # saturation: extra bursts only suppress noise
              >=   ERROR FLOOR            # set by measurement operator + ping-noise
```

Below the **error floor**, NO number of bursts and NO generative prior improves fidelity (DL-reconstruction scaling-laws theorem, OpenReview op-ceGueqc4). **The floor is the formal statement of "never render a fake measured bit."**

### 2.5 The per-region bit budget (the render cap, made operational)

```
bits_region  <=  min( sum_i independent_bits_i,   # what diverse routes actually deposited
                      coin_cap_region,            # the COIN ceiling
                      model_capacity_cap,         # decoder capacity
                      source_provenance_cap )     # provenance tag (measured vs generated)

rendered sigma  =  max( EWA_floor,  k * 2^(-bits_region) )
```

The lock-condition L2 reads this budget per-axis.

### 2.6 Tying to the COIN and the keystone

The fidelity law is the **fourth job of the one logarithm made dynamic over acquisition**. The render cap `rendered_sharpness(x) <= measured_bits(x)` is the *static* statement; the fidelity law is its **time-integral**: `measured_bits(x)` accretes as the running sum of conditional-MI from independent diverse bursts, climbs as `N_eff^(-1)`, and stops at the error floor / structure-function kink. So `2^(-bits)` (render sharpness), `sigma = 2^(-location_bits)` (the COIN on position), and missing-wedge blur are the **same quantity** — blur is unfilled Fourier coverage; the honesty badge is literally the un-accreted bits.

---

## 3. The Gaussian-splat bridge (the construct sharpens like a multi-view splat scene)

The host spec already renders the substrate as a 3D Gaussian splat with `sigma ~ 2^(-bits)` across measured / estimate / modelled channels, and already states the COIN. Multi-keyhole tomography is the **missing acquisition-and-fidelity half of that same splat**, at ~zero new chassis cost. The bridge is exact via the OUGS Jacobian-Covariance Law (arXiv:2511.09397, Nov 2025):

### 3.1 Splat covariance = inverse accumulated Fisher

Each construct-region is a hyper-Gaussian primitive with covariance `Sigma(x)`. The per-pixel render blur is

```
Sigma_C(u) = J_u . Sigma . J_u^T,     with  Sigma ~ sigma^2 . I_accum^(-1)
```

where `I_accum` is the **accumulated Fisher information** across all bursts and `J_u = dC(u)/d theta` is the existing 3DGS rasterizer Jacobian. Therefore:

```
measured_bits(x) = (1/2) log2 det( I_accum(x) + lambda I )      # Gaussian Fisher <-> bits
sigma(x)        = 2^(-bits(x)) = sqrt( diag( J . I_accum^(-1) . J^T ) )   # Cramer-Rao floor through the render Jacobian
```

This makes `sigma = 2^(-bits)` a **theorem of the splat optimizer**, not a hand-set parameter. The COIN law `rendered <= measured` becomes the **Cramer-Rao inequality**: a splat physically cannot render below the floor set by the bits its keyhole-bursts measured.

### 3.2 The compile = accumulation, with online updates

Maintain a per-primitive Fisher updated online as an EMA of squared gradients (OUGS):

```
I_{t,i} = alpha * I_{t-1,i} + (1 - alpha) * [ grad_{theta_i} loss_t ]^2
```

Fisher from conditionally-independent bursts is **additive** (exactly FisherRF's additive-Hessian accumulation), so Pav's "block compiles, gains fidelity and resolution" = `I_accum` monotonically growing toward the Crowther ceiling. The marginal-bit meter falls out as a log-det ratio:

```
dbits_i = (1/2) log2 ( det I_after / det I_before )
```

### 3.3 Views intersect — the multi-exposure imprint, verbatim

A burst = a 3DGS supervision view = a Radon angle. The block sharpens by the same mechanism in all four fields: **views are constraints that collapse the ambiguity volume** (sparse-view 3DGS survey arXiv:2507.16406; SuperF arXiv:2512.09115 — differing sub-pixel aliasing across shifted frames IS the complementary high-frequency information, which is Pav's "multi-exposure imprint into a shared continuous block" word-for-word). Diverse, well-spread views outperform redundant ones; you can prune 10k-20k redundant Gaussians without fidelity loss (arXiv:2508.12720) — direct proof that redundant bursts carry ~0 bits.

### 3.4 Reference architecture to mirror

**FisherRF** (ECCV'24 -> ActiveGS / ActiveGAMER CVPR'25 -> Opt3DGS AAAI'26) is a *deployed* instance of multi-keyhole tomography: each view = a burst; the accumulated Fisher matrix = the compiling block's information content; per-pixel Fisher = the `measured_bits` / blur map; candidate views are scored by information **conditioned on** the accumulated matrix, so well-covered regions score ~0. **One object serves three roles: the fidelity map IS the blur map IS the next-burst targeting map.**

### 3.5 Honesty caveat on the bridge (the diagonal-Fisher gap)

`[SPEC-adjacent, real fidelity gap]` OUGS uses a *diagonal* Fisher (per-parameter). But the missing wedge is fundamentally **off-diagonal / rank-deficient along correlated concept-directions**. A diagonal `I` will **under-report directional streaking** — rendering a region uniformly fuzzy when it is actually sharp-along-probed and streaked-perpendicular. The anisotropic honesty badge needs at least a **low-rank (block) Fisher** to be faithful; pure-diagonal is cheaper but can hide a missing wedge. Also: `measured_bits = (1/2) log2 det I` assumes a locally-Gaussian likelihood, but the ping-back is non-Gaussian (multi-modal tails). Treat Fisher-bits as the **fast render-time proxy** that must never exceed the **prequential online-NLL bits** (the honest audit-time meter the host spec already pins).

---

## 4. The honesty guard against limited-angle streaking (gaps -> blur / stubs)

This is the rigorous core. Limited-angle coverage is a **fuzzy axis**, and its fuzziness is geometrically forced, not stylistic.

### 4.1 Missing wedge = direction-specific blur

A missing wedge in concept-angle leaves a wedge of k-space empty -> **anisotropic** distortion: SHARP along probed directions, SMEARED / elongated along never-probed directions (Nature s41598-019-49267-x). Severity scales with the size of the missing wedge (60/90/120 deg standard cases).

### 4.2 Quinto's visibility criterion (the exact statement)

`measured_bits` is **directional**, not scalar. Carry it as `measured_bits(x, theta)`. A singularity `(x0, xi0)` — a sharp boundary/feature with frequency direction `xi0` — is:

```
VISIBLE    iff xi0 is parallel to some probed concept-angle v in S_delta
              -> survives in WF(R_delta f), stably recoverable
              -> sharp estimate || chi_delta(D) f ||_{H^-1/2} <= || R_delta f ||_{L2}

INVISIBLE  iff xi0 is parallel to NO probed angle
              -> sits in the KERNEL of R_delta; NO stability estimate exists
              -> provably must stay blurred
```

So the wavefront set `WF(F)` partitions cleanly into visible (render sharp) and invisible (render fuzz). **The render cap, directional form:**

```
rendered_sharpness(x, theta) <= measured_bits(x, theta),
and in the missing wedge W(x), the RHS is provably ZERO -> blur is forced by the null space.
```

The COIN-clamped filter (§1.2b) with zero gain at unsampled frequencies enforces exactly this.

### 4.3 The real fabrication trap: ADDED singularities (not blur)

The dangerous fake bits are **not blur** — they are *confident new edges*. Quinto's Principle 2: artifacts appear on lines **parallel to `v` in the boundary of `S_delta` and tangent to a real feature**. The apparatus invents new oriented edges at the missing-wedge rim that were never in the object. Detector (checkable from geometry alone, no ground truth):

```
Any rendered singularity (x, xi) whose xi lies in the missing wedge AND whose location lies on a
wedge-boundary tangent line to an already-sharp feature  ->  FLAG as streak artifact  ->  demote to stub.
```

### 4.4 Where conjecture-stubs attach

Every **invisible singularity** gets a typed conjecture-stub at exactly its position **and its missing-normal direction** `xi`. The stub is not a scalar "fuzzy here" tag — it must carry the *specific unprobed `xi`-direction* so the next-best-view policy knows which concept-angle to fire. `[SPEC]` Candidate canonical primitive: a typed edge in the DAG (or an oriented attribute on the location node) keyed by the missing `xi`.

### 4.5 Generative wedge-fill is allowed — but the COIN bites hardest here

A diffusion / INR prior MAY fill the wedge (TomoSelfDEQ 16-angle arXiv:2502.21320; projector-guided 3D diffusion arXiv:2510.06516; TomoGRAF; MR-SDE sinogram inpainting; DM4CT ICLR'26) — the direct analog of conjecture-stubs / COIN generate-mode. But every filled voxel renders bits **never measured**. Discipline (non-negotiable):

1. **Render order: measured-first, generate-second** (TomoGRAF).
2. Filled orientations carry **strictly lower `measured_bits` / weaker entailment tag** (a Stratum-2 badge) than fired orientations.
3. **"Learning the invisible" gate.** A prior may widen the recoverable cone from `S_delta` to `S_{delta+eps}` **only** under the verifiable membership condition with a *bounded* `N`:

```
f in D_{N,eps} = { || f ||_{L2}  <=  N * || chi_{delta+eps}(D) f ||_{H^-1/2} },   N <= fixed budget.
```

Outside that set, the prior's extra bits are fabrication and must be demoted to blur+stub, not rendered.

4. **Per-pixel hallucination flagging.** Mirror HAD (arXiv:2605.16873): compute a per-pixel hallucination score, mask unreliable generated pixels; DynamicDPS-style tuning suppresses fill inconsistent with measurements.

### 4.6 The runtime confabulation audit (free from the splat machinery)

The **observed-vs-novel-angle PSNR gap.** Under-exposed blocks **co-adapt** — overfit the bursts they have and fabricate floaters in unprobed gaps that look perfect on observed concept-angles and collapse on held-out ones (sparse-view 3DGS co-adaptation, arXiv:2508.12720). A large observed/held-out gap is a *measurable confabulation alarm* -> demote that region to fuzzy/stub. This turns the COIN into a continuous **runtime audit**, not just a render-time cap. `[SPEC]` Run it **per concept-angle** (hold out one probe-direction, reconstruct, measure ping-back error) to localize confabulation to specific WHAT/WHY axes — yielding a per-axis honesty map aligned with the v0.3 six-axis wrapper.

### 4.7 Time as a projection axis (the presentism leak)

Because bursts arrive at different `tau_i` while `F` drifts, this is **dynamic / spacetime tomography** (Space-Time Tomography, Zang et al. SIGGRAPH 2018; X-Hexplane Adv.Sci. 2026). You may NOT reconstruct one t-slice from inconsistent-time projections directly. Fix with a spacetime forward model + temporal regularizer, constrained by a **Lipschitz / total-variation drift bound** in `t`. Honest consequence (operator-level): you may not interpolate a measured `t-100` and `t+100` into a sharp `t-0`; the unmeasured `t-0` stays blurred, bounded only by `F`'s max rate of change. This is the presentism leak sealed at the operator.

---

## 5. The active-acquisition policy (the apparatus self-targets its missing wedge)

Fire the next keyhole where expected marginal bits are maximal = where `I_accum` is weakest = the spec's blurriest splat = where competing hypotheses diverge most:

```
P_next = argmax_P  E[ H(B-hat) - H(B-hat | y_P) ] / cost(P)
       = maximum-entropy sampling                  [BOED, arXiv:2510.00734 — pick the least-predictable measurement]
```

Perturbed Gaussian Ensemble (arXiv:2603.06852, Mar 2026): perturb uncertain primitives, render candidate views, pick the **max projection-space disagreement** angle. **Stopping rule:** halt when marginal `dbits < threshold` (the saturation knee). This single move unifies three primitives — maximizes fidelity gain per burst, avoids redundant re-imprinting, and fires exactly into where conjecture-stubs live.

---

## SPECULATION (disclosed)

*Register shift: the following are conjectures and design bets, not established results. They are flagged so they are not mistaken for the rigorous core above.*

- `[SPEC]` **Structure-function kink = tomographic knee.** If observation->meaning->knowledge and angle-coverage->resolution are the *same* concave curve viewed twice, then the Kolmogorov minimal-sufficient-statistic and the angular saturation knee coincide. This would unify the COIN's "knowledge" threshold with the acquisition stopping-rule under one online-detectable signal (the Fisher-slope maximum). Strong unification; currently unshown. Leaning: detect-and-propose, human-confirm — do not auto-fire the lock on it.
- `[SPEC]` **Concept-Nyquist.** Is there a finite `N_concept-angles` above which a construct of given description-length is provably fully reconstructed (a latent Crowther ceiling), or does latent space's unbounded dimensionality mean residual blur is *mandatory* and no construct ever renders fully solid? This sets whether SOLID is ever attainable or whether the honest default is permanent residual fuzz.
- `[SPEC]` **Min-eigenvalue vs log-det as the render cap.** `measured_bits = (1/2) log2 det I` rewards total coverage but can *mask* a missing wedge. The COIN's never-overclaim spirit argues for the **min-eigenvalue** (worst-probed direction) as the render cap, with log-det demoted to a fidelity gauge only — or, better, a full per-direction bit-field `b(x, theta)`.
- `[SPEC]` **Acquisition trajectory as data.** The *order* in which next-best-views were chosen traces the construct's information geometry (which directions were ambiguous when). The sharpening trajectory may carry bits about the construct beyond the final block — relevant to the retroactive-origin / Stigler attribution axes.
- `[SPEC]` **Concept-drift meta-keyhole recursion.** The deformation field that absorbs concept-drift (democracy-1800 vs democracy-2000) is itself unmeasured. Does it get its own tomographic reconstruction (a meta-keyhole problem), and does that recursion bottom out — or just push the unmeasured-bits problem up one level? If it doesn't bottom out, the deformation field is a fake-bit smuggler unless it carries its own `measured_bits` cap.

---

## QUESTIONS WE SHOULD BE ASKING

*Register shift: stepping back from "is the machinery correct" to "are we even pointing it at the right thing."*

- **Is `P_i` for a CONCEPT-angle actually well-defined?** A physical Radon ray is unambiguous; a concept-direction `theta_i` in latent space is not. Is it a probe-vocabulary vector? An embedding-space direction? A question template? The entire fidelity law is only as rigorous as `P_i`. Candidate: `theta_i` = a normalized direction in the construct's embedding basis; burst = nearest-neighbor resonance projected onto `theta_i`. If we cannot pin this, the law is a shaped intuition, not a theorem.
- **Can we measure the construct's sparsity `s` / feature-count `N_features` at all?** Without an estimate of intrinsic description-length, both the `m >~ s` floor and the Crowther ceiling are *directions*, not *numbers*. And `s` is **decoder-relative** (a philosopher's `q`) — the same construct needs more bursts under a richer decoder. The law's threshold *floats with the glasses*. Should it be reported strictly per-decoder, or does the frame-relativity make it look falsifiable when it is not?
- **Is "angular coverage" itself epoch-relative?** Concept-angles are embeddings whose geometry drifts. Two probes orthogonal under `D(t1)` may be near-parallel under `D(t2)`. The same burst set then has *different fidelity at different reading-epochs*. Must coverage always be computed in the probe's own pinned epoch — and if so, can we ever compare fidelity across epochs honestly?
- **Can a confident hallucination pass the audit?** The co-adaptation PSNR gap catches floaters, not *confident hallucination that matches the prior*. A strong prior can reconstruct plausible held-out views even where bits were synthesized. If the measured/generated split cannot be detected from reconstruction quality alone, then **provenance metadata (which bursts were real) is load-bearing and cannot be inferred post-hoc** — the Stratum tag must be carried, never recomputed.
- **What is the settling experiment that would FALSIFY the whole metaphor?** (Both external models converge on this.) Hidden ground-truth latent block; generate limited / biased / copied / independent bursts; compare renderer A (naive sharp MAP) vs B (COIN-capped) vs C (COIN + stubs + active learning). C must reconstruct the true shape with *fewer* probes, mark limited-angle gaps as fuzz/stubs, aim new probes into them, and produce fewer false sharp bits. **If C cannot beat a plain probabilistic graph + uncertainty viz, "block-universe-compiled-by-keyholes" is a metaphor, not machinery.** Are we willing to run this and accept a null?

---

## Open sub-questions for Pav

1. **`measured_bits(x)` = full log-det (information volume) or min-eigenvalue (worst concept-direction)?** The COIN's never-overclaim spirit argues min-eigenvalue (or a per-direction bit-field) as the render cap, log-det only as a fidelity gauge. Your call sets whether a well-covered-but-one-axis-missing region reads as sharp or honest-fuzzy.
2. **Is the lock driven off corroboration-count (independent routes) rather than certainty?** Leaning yes — then `N_eff` is computed from route-independence and Covariance Intersection sets the fusion weight when route-independence is uncertain.
3. **`disclosed_threshold` in absolute bits — per-axis or per-region?** Proposal: per-axis (six-axis wrappers), since missing-wedge blur is axis-directional. Confirm.
4. **What is the canonical primitive for an oriented missing-wedge stub** that carries the specific unprobed `xi`-direction — a typed DAG edge, or an attribute on the location node?
5. **Diagonal vs block (low-rank) Fisher for the splat covariance** — pay the cost for off-diagonal faithfulness (true anisotropic badge), or accept that pure-diagonal can hide a missing wedge?
6. **Do we run the settling experiment now** (renderer A vs B vs C against a hidden ground-truth block), and are we prepared to demote the whole tomographic framing to "metaphor" if C cannot beat a plain uncertainty-viz baseline?

---

**Note on file paths:** the canonical_genealogy spec tree referenced in project memory (`D:\candidates\canonical_genealogy\hyperspace_spec\SPEC.md`, `SCOPE_NESTING_LOD.md`, `WRAPPER_PROBE_OBSERVER.md`, toy `D:\candidates\canonical_genealogy\toys\globe_cone_unified.html`) is **not present at that path on disk** — the only related file found was `D:\hyperspace_units\UNITS_latent_radix_ceiling.md`. The candidates tree appears to have moved or been archived. This analysis was grounded in the prior-art digest and design seats supplied in the brief, which carry the load-bearing spec content; if you want it cross-checked against the live SPEC.md, point me at the current path.
