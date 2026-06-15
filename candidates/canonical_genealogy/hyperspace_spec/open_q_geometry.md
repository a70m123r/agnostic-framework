# Geometry and Dial-Algebra: Resolving Q3, Q6, Q7, Q8

Synthesis author's note. This resolves the four open geometry/dial questions for the hyperdimensional canonical-space viewer (SPEC-ONLY). The keystone under test throughout: **one logarithm does three jobs** — unfold `v = ln(tan(pi/4 + phi/2))` (SHAPE dial theta), scale ladder `log2(metres)` (SCALE dial b), render sharpness `2^(-bits)`. The headline finding is that all four questions are the **same seam viewed from four sides**, and the keystone survives each — sharpened, not weakened, with its limits now named. Closed forms, costs, and prior art are cited inline. Speculative claims are marked `[SPEC]`.

---

## 0. Verdict table (worth-the-weight vs over-built)

| Q | Question | Verdict | Worth the weight? |
|---|----------|---------|-------------------|
| Q3 | Latent base geometry; one blur operator? | Integer path-ID = **primary base topology** (the hard cap), Poincare radius = **secondary render chart** (the dial). ONE blur **primitive** (heat-flow by sigma), TWO charts — not one literal operator, not one coordinate. | Operator family: WORTH IT. Forcing one literal operator: OVER-BUILT and false. |
| Q6 | One shared budget or two under foveation? | **ONE** budget B_total, steered by TWO foveation signals (gaze + meaning-attention), water-filled across both fibers under one per-frame constraint. | One budget: WORTH IT (it IS the keystone made operational). Two budgets: OVER-BUILT and dishonest. |
| Q7 | Does theta commute with b? Canonical order? | **PARTIAL** commutation, split by an overloaded symbol. Screen-zoom commutes; ladder-position-inside-the-unfold does not; recenter never commutes. Canonical order required. | Canonical order + log-chart fix: WORTH IT (cheap, validates keystone). MapLibre-style scheduling theta=f(b): OVER-BUILT for v1. |
| Q8 | Per-stalk precision filtration + consistency proof? | **BUILD THE PROOF, DEFER THE MACHINE.** One hypothesis (valuation-monotone restrictions) turns the aggregation cap into a theorem. | One-paragraph theorem + per-edge check: WORTH IT (load-bearing). Multigraded-Rees barcode apparatus: OVER-BUILT for v1. |

The unifying thread (stated once, used four times): **a multiplicative move becomes an additive shift on one log axis, and that single log axis is simultaneously the unfold chart, the metres ladder, the sharpness budget, and (Q8) a DVR valuation = bits.** Commutation, single-budget, single-blur, and aggregation-consistency are all corollaries of "the three logs are really one log."

---

## 1. Q3 — Latent base geometry and the one-blur question

### 1.1 Split the question the addendum fused

The original question fused two separable sub-questions. Separate them:

- **(Q3a) What is the latent BASE geometry** — hyperbolic/Poincare, or integer-path-ID?
- **(Q3b) Does "semantic blur = geodesic pull to origin" give ONE blur operator** unifying physical sigma-inflation and latent dimension-truncation?

### 1.2 Q3a verdict: BOTH, layered. Integer-primary for the cap, hyperbolic-secondary for the dial.

Integer path-ID is the **primary base topology** — it carries exact containment `C_child subset C_parent`, and the COIN's hard per-node cap lives here. A Poincare radial coordinate is the **secondary render chart** bolted on top for continuity. This mirrors the spec's own "continuous-underneath, discrete rungs snapped on top" and the two-fibrations-over-one-shared-base architecture: the shared base is the integer poset; hyperbolic geometry is one fiber's **metric**, never the topology.

Why not hyperbolic-primary? It buys free continuity (radius is a smooth real that composes with the keystone log) but **forfeits exact integer containment** — hyperbolic gives only approximate geometric nesting (the H3/S2 lesson), so `C_child subset C_parent` can be violated by float drift and the per-node hard cap leaks. That is the one bit the COIN cannot afford to lose. The literature pins the secondary chart: radius=specificity / angle=branch with parent-near-origin is now solidly established at LLM scale (HiM 2505.18973; HELM 2505.24722).

**Cost of the verdict:** you maintain two registers (integer base + Poincare chart) and must prove they agree at page-in (`local_floor <= measured_bits_node`).

### 1.3 Q3b verdict: ONE blur PRIMITIVE, TWO charts — but only under the wrapped-normal reading. Three candidate "blurs" exist; only two are the same operator.

Carefully separate three distinct objects (this separation IS the answer):

- **(A) PHYSICAL sigma-inflation.** `sigma_render(x) = sigma_measured(x) * 2^((measured_bits - rendered_bits)/D)`, D approx 2-3 spatial DOF. Covariance growth in metres; the bit-deficit becomes Gaussian spread. (LODGE covariance inflation / Mip-Splatting 3D smoothing filter.)
- **(B) MOBIUS SCALAR RETRACTION (deterministic specificity dial).** `r (x) x = tanh(r * tanh^-1 ||x||) * x/||x|| = exp_0(r * log_0(x))`. r<1 pulls a point along its geodesic ray toward the origin, **exactly preserving angle (=branch)** and shrinking radius (=specificity). This is "geodesic pull toward origin" literally. (Ungar gyrovector; Ganea et al. HNN 1805.09112; geoopt kappa-stereographic.)
- **(C) MRL PREFIX-TRUNCATION.** Zero the late coordinates of the embedding. Per "To MRL or not to MRL" (2605.16608) this is **variance redistribution into early dims, explicitly NOT geometric**, nesting along the Euclidean dimension axis.

**The axis-type theorem (why naive unification fails).** (B) moves along a NORM (radius in a fixed-dimension ball); (C) moves along a COORDINATE/DIMENSION count. A radius is not a coordinate-count. There is no identity "truncate k dims = scale norm by r": truncation changes the SUPPORT (which dims are live), retraction changes the MAGNITUDE (how far out on a fixed ray). So **"semantic blur = drop Matryoshka prefix" is FALSE** — asserting it manufactures a geometric claim the embedding does not honor = a fake bit on the meaning axis.

**The unification that does work.** Adopt:

```
blur := scale-inflation of a wrapped/hyperbolic Gaussian
Blur_sigma(p) = p (*) N_wrapped(0, sigma^2)     [heat-flow / manifold-Gaussian convolution of bandwidth sigma]
```

- On the PHYSICAL fiber (flat tangent, Euclidean exp): this IS sigma-inflation (A) — convolution by a metres-Gaussian widens covariance.
- On the LATENT fiber (Poincare ball): convolution by a hyperbolic Gaussian increases variance; because hyperbolic variance = distance-from-origin uncertainty (Hyp-UML 2310.08390), increasing sigma moves the blurred mass's Frechet mean **root-ward** — exactly SLoD's heat-kernel-weighted Frechet mean `Phi_sigma` (2603.08965): sigma->0 = full detail at focus, sigma->inf = root-ward global average. SLoD's O(sigma) error bound and (1+eps) tree-distortion ARE the aggregation-faithfulness cap expressed as geodesic distortion. Hyperbolic Gaussian-Blurring Mean-Shift (2512.11448, Dec 2025) confirms the same primitive is now a published clustering operator on curved space.

So **ONE primitive (Gaussian-blur-by-sigma = heat flow) lives on BOTH fibers; each fiber's exp/log chart turns the same sigma-dial into (physical) covariance inflation and (latent) root-ward Frechet pull.** The Mobius retraction (B) is the **deterministic mean-only shadow** of that stochastic blur: use (B) for a crisp specificity dial, `Blur_sigma` for honest uncertainty mass.

**Role assignment (the crucial move):** the Matryoshka level (C) is **NOT the blur** — it is the **LOD/zoom budget** (`lod_budget(zoom)`, the integer rung). Truncation picks the rung; blur spreads the bit-deficit. This keeps the integer ladder as the exact cap and the hyperbolic chart as the smooth render — exactly the integer-primary / hyperbolic-secondary verdict.

**COIN binding.** `sigma = k * 2^(-rendered_bits)` on BOTH fibers — the keystone's `2^(-bits)` becomes the bandwidth. `rendered_bits = min(measured_bits, lod_budget(zoom))` sets sigma; physical reads sigma as metres-covariance, latent reads sigma as Poincare bandwidth. The aggregation cap `rendered_bits(parent) <= measured_bits(children) - bits_discarded` becomes, latently, SLoD's `d_H(Phi_s1, Phi_s2) <= C|s2-s1|(1+eps)`; physically, the KL(child-mixture || parent-Gaussian). **One inequality, two metric realizations.**

### 1.4 Q3 preconditions and caveats (bake into the spec)

1. **origin=general is a TRAINING ASSUMPTION, not a fact.** Root-ward-blur = generalize requires Sarkar/Nickel root-at-origin placement (assumed by SLoD/HiM). Flattening-the-Parent-Bias (2404.03778) trains ALL embeddings toward the boundary (norm->1) — the opposite. The spec must **mandate root-at-origin placement as a hard precondition**, or the blur direction inverts.
2. **Varying curvature breaks a single clean SCALE dial `[SPEC]`.** HELM's Mixture-of-Curvature-Experts shows one global curvature is too rigid. If the latent fiber needs locally-varying curvature, the sigma->bits calibration k may be per-region, not global — the one sigma-dial is only piecewise-clean.
3. **N (max latent bits) is a boundary-approach problem, not a ceiling.** Poincare radius saturates (tanh->1 at the boundary), so "total civilisation" maps to the boundary, not infinity — the boundary-singularity needs the same clip-and-badge treatment as the |lat|<=85deg pole-clamp.

**Q3 worth-the-weight:** the operator FAMILY (one variational primitive read through two charts) is worth it. Forcing one literal operator, or making hyperbolic the base topology, is over-built and breaks the exact cap.

---

## 2. Q6 — One shared budget vs two under foveation

### 2.1 Verdict: ONE budget, reallocated by attention; NOT two. One pool, two steering signals.

It is one budget steered by TWO foveation signals (a physical-gaze term and a meaning/attention term), water-filled across both fibrations under a single per-frame constraint `B_total`. This is the strict reading of the COIN: the COIN is already a single accounting in bits (`rendered_bits <= measured_bits`), and **a bit is a bit** whether it buys a halved metre (sigma->sigma/2) or a Matryoshka summary rung — spending it from one shared ledger is what makes the unit honest.

The literature converges on ONE pool from two independent directions:

- **Human vision.** Attention-aware foveated rendering (Krajancich/Kellnhofer/Wetzstein, SIGGRAPH 2023, 2302.01368): peripheral contrast sensitivity drops when attention concentrates foveally because of "the limited processing capacity of the brain" — ONE capacity pool drawn down by both gaze location AND semantic/task attention.
- **Information theory.** The 2026 semantic-rate-distortion framework (2602.03949) puts a SINGLE rate constraint `I(Z^(m); M) <= R` on a joint message across all modalities, with cumulative precision `J_m = sum_j H_j^T R_j^-1 H_j` growing **additively** per modality. That is exactly "one budget R, two fibers j," and it kills the geometric-mean information collapse a per-modality split would reintroduce.

**Why two budgets is the wrong primitive:** it forces an exchange-rate between physical and meaning bits that the COIN already provides for free (they are the same bit), and it breaks the aggregation cap (you could overspend one fiber while the shared substrate paid nothing). Ergonomics does NOT demand two budgets — it demands one budget with a richer steering kernel.

### 2.2 Budget policy: the water-filling rule

One global per-frame budget `B_total` (bits/frame, hardware-set). A single foveation gain `g(x)` multiplies it, factoring into TWO multiplicative steering terms that draw on the SAME pool:

```
g(x) = g_gaze(theta_x) * g_attn(x)
   g_gaze  = physical-gaze kernel (eccentricity falloff on the log2-metres radial)
   g_attn  = meaning-attention kernel (concentration on the Poincare-reach radial)

lod_budget(x) = waterfill over { physical splats } U { latent rungs } ( B_total * g_gaze(theta_x) * g_attn(x) ),
                ranked by ONE shared rate slope dD/dR
```

The rank is by one common rate slope even though the two fibers use different distortion metrics D (physical D = L2/sigma-in-metres; latent D = NLL under decoder q). These ARE comparably rankable because **L2 is itself an NLL under a Gaussian q**, so both slopes are dNLL/dR — this is what makes a single water-fill well-posed across fibers. The per-node COIN clamp is where the single budget meets each fiber:

```
rendered_bits(x | ancestry) = min( measured_bits(x | ancestry), allocated_bits_from_waterfill )
```

The chain-rule COIN and the aggregation cap are enforced **per fiber on the allocated slice** — one budget, two clamps. Foveation re-weights WHICH `H_j` term the marginal bit feeds, never splits R.

### 2.3 The per-observer audit rule (the load-bearing honesty addition)

Foveation makes `rendered_bits` **observer-relative** (two observers with different gaze+attention see different rendered_bits at the same node) while `measured_bits` stays **observer-absolute** (a substrate property). The audit is therefore two-layered:

1. **ABSOLUTE invariant** (checked once per node, observer-free): `rendered_bits <= measured_bits` for EVERY reachable (gaze, attention) setting — i.e. the COIN must hold for the **sup over all observers**: `sup_observers rendered_bits(x) <= measured_bits(x)`. This is the tripwire the smooth foveation dial cannot slide a fake bit past.
2. **RELATIVE receipt** (stamped per frame per observer): log `(observer_id, gaze, g_attn field, B_total, allocated_bits per node)` so any frame is reconstructible and its blur is attributable to budget-starvation vs measurement-starvation. The VarSplat / snap-to-measured-means toggle is the observer-invariant ground truth both observers collapse to when foveation is removed.

**Audit law in one line:** *blur from budget is per-observer and reversible; blur from measurement is global and permanent — the audit must never let the first masquerade as the second.*

### 2.4 Q6 caveats

- **Steering cost must be charged (A3FR 2507.04147).** The cost of MEASURING where to attend (gaze tracking; computing g_attn) can exceed render savings. The honest single-budget ledger must include the bits/compute spent deciding where to spend bits. Favor incremental-delta reallocation (re-spend only where gaze/attention moved).
- **Commensurability risk.** The single RD slope assumes both fibers' dNLL/dR are commensurable. If the latent decoder q is mis-specified/anisotropic with no fixed point (the Gemini falsifier), the latent slope is not a clean rate and the water-fill can mis-rank. Mitigation: the no-fixed-point case renders as **terminal blur** — the honesty badge IS the detector, so a mis-ranked fiber fails loud, not silent.
- **Ergonomic clash.** A user staring at a building (max g_gaze) while reading its org-chart (max g_attn) demands more than B_total from both fibers. One budget forces an honest trade (org-text blurs as bricks sharpen). Fix is UX (let the user **pin** one fiber's budget floor), not a second ledger — and a pin must count against B_total honestly (a reallocation within one budget, never a smuggled second budget).
- **g_attn provenance tagging `[SPEC]`.** Gaze is measured; semantic attention is modelled. If g_attn is inferred, the steering signal is Stratum-2 — the per-observer receipt must tag which bits were steered by a measured signal vs a modelled one, else a modelled attention field can quietly concentrate budget and read as if measured.

**Q6 worth-the-weight:** one budget is worth it — it is the keystone made operational ("one log does three jobs" => one currency). The two-layer per-observer audit is the cost of honesty going observer-relative; it is load-bearing, not optional.

---

## 3. Q7 — Does the unroll dial theta commute with the scale ladder b?

### 3.1 Verdict: PARTIAL commutation, split exactly along the ambiguity that "b" hides.

The symbol b means two different things in the spec, with **opposite** answers:

- **(A) Screen ZOOM** (the post-projection scalar, d3's `pixel = b * U_theta(P) + t`). **COMMUTES** with the unfold (up to the conformal scale factor). `U_theta` is conformal — angle-preserving with one isotropic local scale factor (the isothermal property of `v = ln(tan(pi/4 + phi/2))` = complex-log of stereographic). A pure global dilation D about the same fixed point the unfold uses is a conformal-group element that commutes with the conformal structure and with rotations; in d3's post-multiply form it factors out trivially. Order-free.
- **(B) Ladder-position b** (the log2-metres radial position, entering INSIDE the unfold as `rho(phi) = exp(-n * isoLat(phi))`, `n = cos(theta * pi/2)`). **Does NOT commute.** Here b sits inside the nonlinear map; `exp(-n*(isoLat + db))` is not `exp(-n*isoLat)` times any theta-independent factor unless you are already in the log chart. The raw `(s, delta_b, theta)` is NOT a clean product as-is.
- **(C) The real-viewer killer is RECENTER, not the dial.** Every interactive frame recenters/focal-zooms on the cursor (d3 interpolatedProjection and the toy both re-interpolate center/translate per frame). Conformal-group algebra makes it exact: `[D,P] = P` and `[D,K] = -K` (P = recenter-translation, K = focal/anchored zoom). D commutes with rotations but NOT with P or K. So zoom-then-recenter != recenter-then-zoom — order matters the instant a recenter is interleaved, which is always.

**Net:** theta and b commute IFF (i) the zoom is a global uniform dilation about the projection's fixed point and (ii) the unfold's internal fit/normalization does not depend on b. Neither holds automatically, so **an explicit canonical order is required.**

### 3.2 The fix (and it validates the keystone): do both moves as additive shifts on the shared log axis

The ln-tan unfold IS the isothermal chart that flattens the sphere (`ds^2 = Lambda(u,v)(du^2 + dv^2)`); in that chart a multiplicative zoom by `2^db` becomes an **additive shift db** along the SAME log-radial axis as the log2(metres) ladder and the `2^(-bits)` sharpness cap. Additive shifts along one axis commute. This is the AdS-GNN strategy (2505.12880: lift to a chart where conformal maps become isometries) and it is literally the keystone "one log does three jobs": unfold-chart, scale-ladder, sharpness are all affine moves on ONE log axis, so **commutation is a free corollary of the keystone**, not an extra assumption.

### 3.3 Canonical operation order for camera state (s, delta_b, theta)

Because the recenter P does not commute, reproducibility demands a declared order. Do steps 1-3 in the log chart, every zoom anchored at the projection center:

```
1. RESOLVE s    : pick the LCA-rebased local frame. This is the ONE place a P-translate /
                  chart-origin choice is legal; it is non-commuting, so it is fixed FIRST.
2. APPLY delta_b: shift ladder position + zoom window by db ADDITIVELY on the shared log axis,
                  anchored at that origin. NEVER as a focal zoom about the cursor in screen
                  space (that injects a non-commuting K).
3. APPLY theta  : LAST, in the RAW (lat,lon) domain (d3 rule: morph the raw projection, never
                  the pixels). Feed a FIXED reference scale into the raw unfold so U_theta's
                  internal normalization never depends on b (keeps the unfold scale-equivariant).
4. POST-MULTIPLY: the single screen affine (optical magnify + translate). The ONLY multiplicative
                  zoom; it is conformal-commuting (pure post-composition scalar).
```

**One-line invariant:** *carry b additively in the log chart; carry all multiplicative zoom in the final post-affine; never let U_theta's fit depend on b.* Under that rule `(s, delta_b, theta)` IS a clean product and views are order-independent up to the step-1 recenter, whose order the canonical sequence fixes.

**Engineering precedent:** nobody treats these as freely commuting. MapLibre GL JS 5.0 (Jan 2025) deliberately BINDS theta = linear-function-of-zoom over a fixed zoom band (`u_projection_transition`), which only makes sense if they are coupled. The spec's choice is to instead **decouple cleanly via the log chart** rather than schedule one to the other.

### 3.4 Q7 caveats

- **The spec must split the overloaded symbol b** (screen-zoom vs ladder-position) or the camera-state product is ill-defined — the commutation answer is opposite for the two readings.
- **The "fixed point" is itself moving.** Per-pair-LCA floating origin means the chart origin changes per target pair. Anchoring zoom at a per-pair-varying origin needs a stated tie-break (recommendation: rebase to the FOCUSED membrane's frame, not the per-pair LCA, for camera-state purposes).
- **Variable-curvature latent fiber `[SPEC]`.** Clean commutation assumes a single global conformal structure. HELM MiCE suggests the latent fiber may need locally-varying curvature, under which the additive-shift commutation can fail locally. Commutation is solid on the physical/Mercator fiber; flag it as **conjectural on a variable-curvature latent fiber.**
- **Mid-dial 0<theta<1 is "pure model"** (interpolated coordinate). Commutation makes the geometry reproducible but does NOT make the mid-dial position measured — the canonical order must run alongside the "force maximal blur at 0<theta<1" rule, or reproducible-but-fake-crisp views result.
- **Recommended render invariant:** for the d=0 global-uniform-dilation reference camera, assert zoom-then-unfold is **pixel-identical** to unfold-then-zoom — a cheap continuous proof that the three logs are still one, logged alongside the COIN inequality.

**Q7 worth-the-weight:** canonical order + the log-chart fix is worth it (cheap, validates keystone). MapLibre-style scheduling theta=f(b) is over-built for v1 — offer it only as an optional "guided" mode on top of the decoupled product.

---

## 4. Q8 — Per-stalk precision filtration + consistency-obstruction sketch

### 4.1 Verdict: BUILD THE PROOF, DEFER THE FULL MACHINE.

The per-stalk filtration is worth specifying because it converts the aggregation cap from a hoped-for inequality into a **theorem with an explicit, checkable hypothesis** — and that hypothesis turns out to BE the design constraint you already wanted on restriction maps. But the full multigraded-Rees apparatus is over-built for v1: spec the one-paragraph theorem now; gate the heavy algebra behind "if/when we actually compute per-node arithmetic barcodes."

### 4.2 The object: per-stalk valuation filtration

Extend Ghrist-Ding precision-graded cohomology (2511.00677) from their **single global** `pi^k` to **one `pi^{deg(v)}` per stalk.** Concretely:

- **Base** = containment poset P of membrane-nodes (faces = parent-child edges) — exactly a cell complex on which a cellular sheaf F lives (the shared base of the two fibrations).
- **Sheaf** F: stalk F(v) at node v; restriction `F_{v<=e}: F(v) -> F(e)` along each face.
- **Per-stalk degree:** `deg(v) := measured_bits(v)` (per-node bit ceiling; physical fiber = PCGS/EntropyGS/SPZ bit-cost, latent fiber = chosen latent unit).
- **DVR** with uniformizer pi (take pi = 2, valuation = bits — Ghrist-Ding's Z_p with the p-adic valuation reading as bit-depth).
- **Filtration on i-cochains** `C^i = prod_{dim e = i} F(e)`:

```
F_k C^i = { c : val(c_e) >= deg(e) - k  for all e }
```

i.e. a cochain is "at precision k" iff every coordinate is within k bits of its own node's ceiling. **Clean reduction:** rescale each stalk by `pi^{deg(e)}` and apply Ghrist-Ding's single global filtration to the rescaled complex — per-stalk = global-filtration-on-a-reweighted-complex.

### 4.3 The consistency proof sketch (the deliverable)

**THE ONE HYPOTHESIS (H):** the coboundary delta preserves this filtration, `delta(F_k C^i) subset F_k C^{i+1}`. Unpacked at a single face `v <= e`:

```
val( F_{v<=e} x ) >= val(x) + ( deg(e) - deg(v) )    for all x
```

i.e. each restriction can only LOSE bits going parent v -> child face e by at most the declared budget drop, never GAIN precision. This is precisely "a child face never carries more measured precision than its parent stalk grants it" — the aggregation cap read upward.

**THE PAYOFF.** Under (H), the filtered cochain complex `(C^*, delta, F_*)` has a **spectral sequence of a filtered complex** (standard). A decreasing filtration whose differential preserves it yields a well-defined induced filtration `F_k H^i` on cohomology, graded pieces = E_infinity subquotients. The induced filtration degree on a parent class is bounded by the children cochains' degrees — and THAT bound IS:

```
rendered_bits(parent) <= measured_bits(children) - bits_discarded
```

where `bits_discarded` = the spectral-sequence differentials `d_r` that kill precision crossing a page (the algebraic image of the KL(child-mixture || parent-Gaussian)). **So the cap is a THEOREM under (H), not an axiom.**

**THE TEETH.** Without (H) it is FALSE — a coboundary can drop valuation. Ghrist-Ding's Smith-normal-form exponents `a_j` are exactly the precisions at which classes fail to lift; a restriction with the wrong valuation manufactures a class that lifts higher than its children paid for = **a fake measured bit at the aggregation seam.** So tree-consistency is a **design constraint you build into the restriction maps** (a cheap, local, per-edge valuation-monotonicity test at page-in: an integer comparison, NOT a cohomology computation), then get globally for free.

**TRANSITIVITY FOR FREE.** Filtration-preservation **composes** (the composite of two filtration-preserving maps is filtration-preserving), so the global cap across ~206 levels is the telescoped sum of local per-edge caps — the spectral sequence does the telescoping, no separate accumulation argument needed. This discharges the open obligation to prove the chain-rule COIN composes transitively.

**THE HEAVY, DEFERRABLE HALF (the constructive recipe).** Model the per-stalk degree as a **multigraded Rees algebra** with one shift variable `t_v` per stalk (vs Ghrist-Ding's single t). "Consistent per-node filtration" = "the multigraded Rees module is good/well-defined" (a decidable algebra condition); associated-graded Smith-normal-form yields per-node arithmetic bars whose length `a_{v,j}` = the precision at which node v's class fails to lift = the exact per-node honest-bit ceiling. That is the rigorous form of the per-node bit budget — defer until per-node barcodes are actually needed.

**Recommended two-layer COIN architecture:** (a) Ghrist-Ding arithmetic barcodes for the HARD exact integer bit-ceiling per node (the clamp); (b) Yokoyama (2601.19056) per-cell spectral witnesses `W_{j,delta}(e)` for the SMOOTH differentiable per-node blur falloff a renderer wants (`delta` = continuous precision dial = `lod_budget(zoom)`). The hard clamp gives the honesty guarantee; the spectral channel gives the continuous LOD dial.

### 4.4 Q8 caveats

- **The proof certifies consistency RELATIVE TO declared deg(v) = measured_bits(v); it does NOT certify that deg(v) upper-bounds the true rate-distortion function.** That soundness gap (the quantizer must upper-bound true RD; `local_floor <= measured_bits_node`) lives outside the cohomology and stays open. The filtration makes the cap consistent; it does not make the estimator honest. **State this boundary explicitly or the proof over-claims.**
- **Latent-fiber friction `[SPEC]`.** The proof assumes a DVR/module-valued sheaf (linear restriction maps). Physical fiber fits (similarity transforms, SO(3), real stalks). Latent fiber's restriction = Matryoshka-prefix truncation + convex inclusion `C_child subset C_parent` — truncation is filtration-like (prefix nesting = valuation) but convex inclusion is not obviously a module map over a DVR, and 2605.16608 shows truncation is variance-redistribution, not a clean valuation retraction. So **(H) is provable on the physical fiber and only conjectural on the latent fiber** — flag the latent per-stalk filtration as an experiment (child fn), not an asserted theorem.
- **Single uniformizer across varying curvature.** HELM MiCE warns a single global curvature is too rigid; a single pi (single bit-unit) across all latent stalks may not hold.
- **Integer vs real grading.** Real measured_bits are non-integer (`log2(1+corroborations) + a*certainty`); a valuation filtration is integer-graded. Recommendation: floor to integer bit-rungs for the COIN clamp (matches "discrete rungs snapped on top"); keep the real value only for the soft `lod_budget`. This matches the existing hard-clamp/soft-falloff split.

**Q8 worth-the-weight:** the PROOF is cheap and load-bearing (one hypothesis + one citation converts the wished-for inequality into a theorem AND discharges transitivity for free — high value for ~one paragraph). The MACHINE (multigraded Rees, per-node barcode computation) is over-built for v1 — the engineering only needs the local per-edge check `val(F_{v<=e} x) >= val(x) + (deg(e) - deg(v))` at page-in.

---

## 5. Cross-question synthesis: the four answers are one seam

| Seam-face | The move | Where it commutes/holds | Where it breaks |
|-----------|----------|-------------------------|-----------------|
| Q3 blur | sigma = k*2^(-bits) heat-flow, one primitive two charts | physical (constant-curvature flat tangent) | latent variable-curvature; boundary-trained embeddings invert direction |
| Q6 budget | one B_total water-filled, multiplicative gain g_gaze*g_attn | when both fibers' dNLL/dR commensurable (L2 = Gaussian-NLL) | mis-specified latent q -> mis-rank -> renders as terminal blur |
| Q7 dials | additive shift on shared log axis | global dilation about fixed point, b-independent unfold fit | recenter P, focal-zoom K, variable-curvature latent |
| Q8 cap | valuation = bits on the SAME log axis (4th job) | valuation-monotone restrictions (H) | latent truncation = variance redistribution, not valuation |

The keystone "one logarithm does three jobs" is, after Q8, **doing four** — the `2^(-bits)` sharpness axis IS the DVR valuation grading, so the aggregation honesty cap lives on the same single log axis as unfold / scale / sharpness. Every "where it breaks" column is the **same failure mode**: the latent fiber's variable curvature + non-geometric truncation is where "one log" degrades to "one budget B, two distortion metrics D." The physical fiber is clean across all four; the latent fiber is conjectural across all four, **for one shared reason.** That convergence is itself the strongest evidence that these are not four questions but one.

---

## 6. SPECULATION (disclosed)

The following go beyond what the cited literature or the design seats establish. Marked for honest separation.

- `[SPEC]` **The latent fiber's four conjectural breakages are a single object.** Q3 (curvature-dependent k), Q6 (q-anisotropy mis-rank), Q7 (variable-curvature non-commutation), Q8 (truncation != valuation) may all be one quantity: the **local curvature field's deviation from constant.** If true, a single measured field `kappa(node)` would simultaneously calibrate the blur, the budget slope, the commutation residual, and the valuation step — collapsing four open experiments into one probe. This is a guess, not a result.
- `[SPEC]` **bits_discarded = KL = spectral-sequence differential `d_r` as literally the same number.** The seat flags this as "the highest-value follow-up" and currently only an analogy. If the KL between the child mixture and the parent Gaussian equals the precision killed by the page-crossing differential, it would tie the honesty cap to an information-theoretic AND a cohomological quantity at once — a genuine result. Unproven.
- `[SPEC]` **The Mobius deterministic dial and the SLoD stochastic Frechet pull land the blurred mean at the same point at matched bit-budget.** If `r (x) x = mean(Blur_sigma(x))` within tolerance, the crisp dial and the honest-uncertainty dial are the same operator viewed two ways and the spec needs only one canonical operator. If they diverge, the spec must pick one. Testable today on a Nickel-Kiela WordNet embedding; currently assumed, not checked.
- `[SPEC]` **The per-observer sup-over-observers audit is decidable cheaply via the gain kernel's structure.** Because g(x) = g_gaze * g_attn is a product of two monotone falloffs, the sup over all (gaze, attention) might be attained at a corner of the reachable set (max-gaze, max-attn), reducing the expensive sup to a single corner-check per node. Plausible from monotonicity but not proven.

---

## 7. QUESTIONS WE SHOULD BE ASKING (register-shift)

*(Shifting from "resolve the spec's questions" to "interrogate the frame the questions assume.")*

- We keep asking whether the latent fiber **behaves like** the physical fiber (commutes, blurs, caps the same way). The deeper question: **is "fiber" even the right primitive for meaning?** A physical fiber has a genuine metres-radial. The latent "fiber" is a chart we chose to bolt onto an integer poset. We may be importing the physical fiber's geometric intuitions into a place where only the **poset** is real and the geometry is decoration. What would the spec look like if the latent side were a **pure order** (no radial, no curvature, just containment + a soft LOD dial), with the Poincare chart demoted to a rendering convenience that is never audited?
- We treat `measured_bits` as observer-absolute and `rendered_bits` as observer-relative (Q6). But **who measures the measured bits?** The estimator soundness gap (Q8 §4.4) says the whole COIN rests on a quantizer we haven't proven upper-bounds true RD. The honest question is not "does the cap compose?" (it does, under H) but "**is there any node where we know the measured-bits estimate is itself a fake bit?**" — and if so, the entire filtration is consistent atop a lie.
- The keystone's power is that it makes four problems one. **That is also its danger.** A frame that explains everything risks being unfalsifiable. The sharpest question: **what would the world look like if the keystone were FALSE** — if scale, shape, and meaning were genuinely three different logs that only approximately align? The d=0 pixel-equality render invariant (Q7 §3.4) is the one concrete falsifier we have. Are there others? We should be hunting for the experiment that **breaks** "one log," not just the ones that confirm it.
- We assume origin=general requires root-at-origin placement (Q3 §1.4) and treat boundary-trained embeddings (Flattening-the-Parent-Bias) as a precondition violation. But what if **both placements are true simultaneously in different regions** of a real deployed embedding? Then "blur direction" is not a global setting but a per-region sign — and the single sigma-dial has a hidden orientation field. We are not currently asking whether the blur **direction** itself needs to be measured per-node.

---

## 8. Open sub-questions for Pav

1. **Bit-calibration of the bandwidth (Q3):** is `sigma = k * 2^(-rendered_bits)` with ONE global k, or must k be per-curvature-region (HELM MiCE)? This is the difference between one clean SCALE dial and a piecewise one. Your call on whether v1 assumes constant curvature.
2. **Canonical form of g_attn (Q6):** the latent foveation kernel — (a) cursor/selection on a latent node, (b) query relevance, or (c) an inferred attention model? (a)/(b) are measured-ish and cheap to audit; (c) is Stratum-2 and needs the modelled-steering tag. Your pick.
3. **Anchor for camera-state zoom (Q7):** per-pair LCA (precision-optimal but moving) or focused-membrane frame (stable but precision-suboptimal for distant pairs)? Both give reproducible-but-different view sequences.
4. **Schedule theta to b or keep decoupled (Q7)?** Full decoupling (current spec choice) vs an optional MapLibre-style "guided" mode where theta=f(zoom). Decoupling is cleaner; scheduling matches shipped UX convention.
5. **Integer vs real grading for the COIN clamp (Q8):** confirm integer bit-rungs for the hard clamp + real value only for the soft lod_budget. Does this break the latent continuous-underneath-discrete-on-top design?
6. **Three child experiments to log (dead-child candidates if they fail):**
   - Does decreasing the Matryoshka prefix track decreasing Poincare radius along a fixed angular branch? (If not, integer-rung and hyperbolic-radius are genuinely orthogonal and must never be visually conflated — testable on Jina-v5/Qwen3-Embedding/EmbeddingGemma.)
   - Do `r (x) x` (Mobius) and `mean(Blur_sigma(x))` (SLoD) agree at matched bit-budget? (Testable today on a Nickel-Kiela WordNet embedding.)
   - Does the d=0 global-uniform-dilation reference camera give pixel-identical zoom-then-unfold vs unfold-then-zoom? (The cheap keystone falsifier — add as a logged render invariant.)
7. **Highest-value theory follow-up (Q8):** is `bits_discarded_by_summary` (operationally KL(child-mixture || parent-Gaussian)) literally the spectral-sequence differential `d_r`, or only analogous? If they coincide it is a genuine result tying the honesty cap to one information-theoretic AND one cohomological quantity.

---

*Sources referenced inline: SLoD (2603.08965), HiM (2505.18973), HELM (2505.24722), To-MRL-or-not (2605.16608), Hyperbolic Gaussian-Blurring Mean-Shift (2512.11448), Hyp-UML (2310.08390), Mobius/Ganea HNN (1805.09112), MRL (2205.13147), Flattening-the-Parent-Bias (2404.03778), Krajancich attention-aware foveation (2302.01368), Semantic Rate Distortion (2602.03949), PromPrune (2603.14892), Budgeted Attention Allocation (2605.05697), LODGE (2505.23158), Matryoshka GS (CGF 2025), A3FR (2507.04147), Ghrist-Ding precision-graded cohomology (2511.00677), Yokoyama relative obstructions (2601.19056), AdS-GNN (2505.12880), conformal-group algebra (1907.05147), Daners conformal-conic family (AMM 119:3). Spec anchors: `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec\SPEC.md` and `SCOPE_NESTING_LOD.md`; toy ground truth `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\toys\globe_cone_unified.html`.*
