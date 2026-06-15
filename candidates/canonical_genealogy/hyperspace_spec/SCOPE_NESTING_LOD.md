# Scope, LOD, and Nested Domains - SPEC ADDENDUM

**Date:** 2026-06-14 | **Status:** Tier-3 design addendum. NOT built. Extends `SPEC.md` and `toys/globe_cone_unified.html`.

**Question answered:** how one container holds the WHOLE UNIVERSE down to the PLANCK scale (physical) and TOTAL CIVILISATION down to a SINGLE NUMBER OR WORD (latent) in one coordinate system, without ever rendering a fake measured bit.

**Sources (3 independent, convergent):** an Opus workflow `hyperspace-scope-nesting` - 4 fresh-scan scouts (gsplat-LOD, multi-scale coords, latent compression ladder, nesting ontology) + 4 design seats (coord-architect, LOD-as-COIN, nesting-tree, red-team) + a synthesis author - plus cross-model passes from GPT-5.5 ([scope_codex_take.md](scope_codex_take.md)) and Gemini ([scope_gemini_take.md](scope_gemini_take.md)). The philosopher seat is a companion pass in [scope_philosopher_take.md](scope_philosopher_take.md). Brief: [scope_brief.txt](scope_brief.txt).

**Headline verdict:** the dial is real as ONE VARIATIONAL PRINCIPLE (one log axis of BUDGET; rate-distortion, with the RG<->Information-Bottleneck equivalence backing the physical side), but NOT as one coordinate - the distortion metric differs between the axes (an operator family, not a single coordinate). Strong enough to build; honest about what it is. The biggest newly-found honesty gap: the AGGREGATION SEAM - a parent splat can render crisper than its measured children - so the COIN needs a SECOND inequality (section 5.1).

---

# Scope, LOD, and Nested Domains

*Spec addendum. Extends the existing keystone (one logarithm does three jobs: 3D->2D unfold `v = ln(tan(pi/4 + phi/2))`; physical scale ladder `log2(metres)`; render sharpness `2^(-bits)`) and the COIN governing law (`rendered_sharpness(x) <= measured_bits(x)` everywhere; blur is the honesty badge; never render a fake measured bit). This addendum does NOT restate the base spec. It answers one question: how does the container hold the WHOLE UNIVERSE down to the PLANCK scale on the physical axis, and TOTAL CIVILISATION down to a SINGLE NUMBER OR WORD on the latent axis, in one coordinate system, without ever lying about a bit.*

---

## 0. The one-line extension

The keystone gives us a single ruler `b` measured in **bits**. This addendum makes three structural claims about that ruler:

1. **No single number can hold the ruler.** The ~206-bit physical span exceeds any float. So the ruler is paid in TWO currencies: an exact integer **path-ID ladder** (carries unbounded RANGE) and a small **local float** (carries bounded local RESOLUTION). The keystone's `log2` ladder and the precision-rebasing ladder are revealed to be the same ladder.
2. **LOD is the COIN at render time, literally** -- not a performance hack bolted on, but the physical enforcement surface of `rendered_bits <= measured_bits`.
3. **Each membrane node is one rung of the ruler and one enforcement point of the COIN.** The nesting tree is not decoration; it is where measured and rendered bits are reconciled, per-node.

The honest scope of the keystone, sharpened by this work: **one log axis of BUDGET, not one axis of COST.** The bit-count `b` is genuinely shared across physical and latent; what a bit COSTS (the distortion metric `D`) is not. Hold this distinction -- it is load-bearing for the verdict in section 4.

---

## 1. The unbounded-scope coordinate, and how precision is held

### 1.1 The span, stated as a theorem (not a preference)

Physical axis: `b_phys = log2(L / 1 metre)`. Planck length ~ `-116`, observable universe ~ `+89`. The full physical span is ~**205 bits** of dynamic range.

A single IEEE float64 carries ~52 mantissa bits. Double-double / DSFUN90 float-pairs reach ~106 bits (~44 effective on GPU). Both fall short of 205 by roughly 2x-4x. Therefore:

> **Theorem (no-single-coordinate).** No fixed-width floating representation can hold a point's absolute position at uniform resolution across the Planck-to-universe span. The dynamic range MUST be paid in an integer exponent ladder (tree depth); floats may carry only local detail.

This is forced, not chosen. The entire coordinate design follows from it.

### 1.2 The coordinate is a PAIR, not a number

A point `P` is never materialised as one global absolute position. It is addressed as:

```
P = (path, u)
  path = [k0, k1, ..., kd]   integer child-index chain, universe-root -> home membrane
  u                          local offset INSIDE the home membrane's frame
                             physical: float3 with |u| in [0,1) of node extent
                             latent:   Matryoshka prefix vector (first-k dims)
```

`path` is the **exact, lossless containment skeleton** -- it names WHICH membrane. `u` is the **bounded metric content** -- it names WHERE INSIDE. The "unbounded-scope coordinate" is exactly this pair: an arbitrary-length integer ladder plus a near-origin float.

Each node `n` stores one similarity transform to its parent:

```
T_n = ( t_n,  db_n,  R_n )
  t_n   translation in PARENT-local units
  db_n  log2-scale STEP (one rung of the ladder, in bits)
  R_n   rotation (SO(3) on the physical fiber)
```

The absolute scale of node `n` is a running sum down its path:

```
b_n = sum_{i <= depth(n)} db_i
```

**This sum is the only place the full ~206-bit dynamic range lives**, and it lives as an integer-ish accumulation of small per-edge exponents -- never as one float. The keystone's scale ladder IS this accumulation.

### 1.3 How precision is held: hierarchical local frames + LCA rebasing

Precision across the span is held by three mechanisms that share the log idea but **stay distinct organs** (do not fuse them into one number -- the prior art is explicit that position-precision, depth-precision, and scale-span are solved by different mechanisms that merely agree on the unit, the bit):

- **RANGE (unbounded, exact):** the integer path ladder / running `b_n` sum.
- **LOCAL RESOLUTION (bounded ~52 bits):** the float `u`, always near-origin because it is addressed relative to its home membrane.
- **NEAR-FIELD PRECISION (per-frame):** camera re-basing to the nearest resident node (the floating-origin move), so the GPU only ever sees small near-origin numbers.

To compute a relative vector between two points `P1=(path1,u1)`, `P2=(path2,u2)`:

1. Find the **lowest common ancestor (LCA)** = longest common prefix of the two integer chains. `O(depth)` integer compares (~30 compares at ~7 bits/level for the full span).
2. Walk both local `u`'s up to the LCA, composing the cached `T`'s.
3. **Only THEN** do float arithmetic. At the LCA the magnitudes are comparable, so float64's 52 bits are abundant.

This generalises floating-origin: **the origin is not the camera, it is the per-pair LCA membrane.** A direct consequence, which must be stated plainly to users: **there is no well-defined global metric.** There are only metrics-within-a-common-ancestor. Two objects both distant from the camera but near each other are rendered precisely (rebased to their shared ancestor), where naive camera-rebasing would give both huge, precision-poor coordinates. Precision is pair-relative, by construction.

### 1.4 The latent axis on the same ruler

Latent: `b_lat` = description length in bits of the rendered meaning. `0` = one word (~a few bits); `N` = total civilisation corpus. Same affine bit-ruler, different chart:

- Physical zoom by one notch = +1 bit of spatial address = halve the metre extent.
- Latent zoom by one notch = +1 bit of description = one more Matryoshka prefix dimension / one finer summary rung.

The unroll dial `theta in [0=3D globe, 1=2D map]` selects how the local frame's sphere is unrolled; the keystone `v = ln(tan(pi/4 + phi/2))` is just `b` re-expressed in the conformal (Mercator) chart. So one `b`, three readings: position-on-ladder (`log2 m`), unroll-coordinate (`ln tan`), and sharpness cap (`2^-b`).

**[SPEC] Latent continuity caveat.** `b_lat` is continuous in theory (embedding eigen-spectrum, Matryoshka prefix-length, soft-length-controller) but real summary rungs are DISCRETE (RAPTOR levels; SciZoom abstract->TL;DR). Design the latent axis **continuous-underneath with discrete rungs snapped on top**, or latent zoom feels like teleporting between summaries rather than smooth semantic zoom.

### 1.5 Camera state

```
camera = ( s,  delta_b,  theta,  gaze )
  s        point on the b-ruler: a path + fractional b within the focused membrane
  delta_b  half-window width in bits (the zoom level)
  theta    3D<->2D unroll dial
  gaze     optional foveation centre
```

The set of RESIDENT nodes is exactly:

```
{ n : b_n in [s - delta_b, s + delta_b]  AND  n intersects the view frustum }
```

This is a pure interval test on the b-ruler. **The ladder doubles as the LOD selector and the streaming predicate.** Use a `log` depth buffer for the render (`d(log z)/dz = 1/z =` projected screen size, the hardware twin of the keystone: log distributes depth precision as uniform bits-on-screen, proven by Cesium's 0.1 m -> 1e8 m single frustum).

---

## 2. LOD / chunking AS the COIN

### 2.1 The render law, in its correct shape

```
rendered_bits(x, zoom) = min( measured_bits(x),  lod_budget(zoom) )
```

This is the seed intuition, and it is correct. But the `min()` has two caps with different characters, and the distinction is the whole honesty story:

- **`measured_bits(x)` -- the COIN honesty cap. HARD.** The per-object rate-distortion ceiling (Vereshchagin-Vitanyi: every object owns its own RD function; the Kolmogorov Structure Function is the formal name on the lossy side). The renderer may never exceed it.
- **`lod_budget(zoom)` -- a SOFT, reallocatable screen-space budget** set by projected angular size and foveation.

The renderer always takes the `min()`. **Blur is the badge** precisely because when `lod_budget > measured_bits`, the `min()` clamps to `measured_bits` and the splat refuses to sharpen. This is exactly Mip-Splatting's 3D smoothing filter (caps each splat below half the training sampling rate -- physically refuses to render finer than measured), **generalised from anti-aliasing to a global law across the 206-bit ladder.** Mip-Splatting is the existing primitive form of the COIN inequality; this spec promotes it to a universal render law.

### 2.2 `lod_budget` concretely, and the splat as the rendering primitive

A splat of world scale `sigma_w` at distance `d`, focal `f`, viewport `H` px, subtends `s_px = f * sigma_w / d` pixels. Screen-space information is bounded by footprint:

```
lod_budget_pixels = c * log2(1 + s_px^2)   bits
```

One zoom octave = exactly one resolvable bit. Equivalently, a global `B_total` bits/frame is **water-filled**: spend bits on primitives in descending RD slope `dD/dR` (RDO / importance-prefix order) until the sum reaches `B_total`; foveation multiplies by a gaze kernel `g(theta_x)`. So:

```
lod_budget(x, zoom) = waterfill_i( B_total * g(theta_x) )  ranked by RD slope
```

The bit deficit becomes geometry -- this is the keystone's sharpness job made literal:

```
sigma_render(x) = sigma_measured(x) * 2^( (measured_bits(x) - rendered_bits(x)) / D )
                  D = spatial DOF ~ 2-3
```

When `rendered < measured`, the splat INFLATES (blurs) by the bit deficit. This re-derives **LODGE covariance inflation** and **CLoD-GS opacity/scale decay** as the geometric image of the bit gap. `sigma ~ 2^(-rendered_bits/D)` is `2^(-bits)` made physical.

**Folded-in gsplat-LOD primitives (the rendering substrate):**

- **Continuous LOD per primitive:** CLoD-GS gives smooth distance-dependent detail = `rendered_bits(x, zoom)` with no discrete pop.
- **Distance->covariance inflation:** LODGE is the blur operator above.
- **Container:** inherit Cesium 3D Tiles' geometric-error LOD tree + glTF/SPZ payloads (Earth-anchored, standardised, shipping). **Re-type the single geometric-error scalar into the unified `log2` bit-axis** -- this is the seam where the existing container meets the keystone.
- **measured-bits unit (physical):** entropy-constrained quantization per primitive (PCGS / EntropyGS), or SPZ compressed size (now in glTF `KHR_gaussian_splatting_compression`, ratifying ~Q2 2026). One of these is `measured_bits(x)`.
- **Streaming engine:** Spark 2.0-style unified cross-object page-table + LRU under one global bit budget -- the proven pattern for many nested membranes.
- **Authoring vs delivery = two traversals of one structure.** Top-down PRUNE/DISTILL is the AUTHORING story (author the finest fact once, derive faithful coarse views by truncating the RD-ordered prefix -- Matryoshka GS, EvoGS deltas), matching Pav's "transform FROM the whole down TO a word." Bottom-up GROW is the DELIVERY story (stream coarse prefix first, refine). Same RD-ordered structure, two directions; do not pick one storage order or you break one use-case.

### 2.3 Chunking falls out of the COIN for free

Each membrane node carries `measured_bits_node` = sum of leaf RD-costs (the Cesium geometric-error scalar, re-typed as bits). The residency rule is one test:

```
node RESIDENT  iff  measured_bits_node >= floor(zoom)
```

A node whose entire bit-content is below the floor renders as **one parent dot / one parent word** and is never paged in. **Culling is the COIN doing its job:** a sub-tree whose screen-projected `lod_budget(zoom)` drops below 1 bit cannot contribute even one honest bit, so the COIN inequality IS the cull test. One rule serves both axes: physical (page in planet-surface splats) and latent (page in org member-level text).

### 2.4 [SPEC] The chain-rule correction to the flat min()

The flat `min()` is the RD ceiling for `x` ALONE. But a coarse parent has already paid for shared low-frequency bits; the child should owe only its CONDITIONAL bits. EvoGS/codebook deltas store exactly this. The honest law is:

```
rendered_bits(x | ancestry) <= measured_bits(x | ancestry)     [chain-rule COIN]
```

This is a real correction to the seed formula. Cumulative bits down a chain = description length = the keystone's `log2`/MDL axis; truncating the tree at any depth = a valid scene scaled to the received bits. **Open obligation:** prove the chain-rule composes transitively across ~206 levels without accumulated conditional-bit rounding silently violating the flat global cap (sum of honest conditional caps `<=` honest joint cap). See section 5.

### 2.5 [SPEC] Latent blur has no covariance

`sigma`-inflation is spatial; "blur a word" has no covariance matrix. On the latent fiber the COIN is enforced as **Matryoshka-prefix truncation + an explicit entailment/uncertainty tag** -- render "a primate" not "a chimpanzee" at low bits, NOT visual fuzz. Blur-is-the-badge survives only if "badge" = **semantic generality**. KARL's never-waste-tokens (approximate Kolmogorov complexity = min tokens to reconstruct within an error budget, framed as Solomonoff induction) is the closest published honesty primitive on the meaning axis.

---

## 3. The nested-domain tree

### 3.1 Verdict on "same tree?": two fibrations over one shared base

The physical-nesting tree and the latent-containment tree are **NOT the same tree, and NOT two separate trees.** They are **two co-registered fibrations over one shared base.**

- **Base:** a single containment poset of membrane-nodes (`galaxy > system > planet > region > org > person > artefact`), each carrying an integer path-ID encoding its full ancestry. The base **topology** (who-contains-whom) is shared and EXACT.
- **Physical fiber:** local origin + `log2`-metres scale + rotation (Cesium-RTC style).
- **Latent fiber:** convex meaning-subspace + Matryoshka prefix-length budget (N2F2-style on-field semantics).

The two fibers share the base but their **metrics differ**. The clean, falsifiable form (sharper than "same tree"), borrowed from DGGS H3/S2: **the two trees share the integer-ID topology EXACTLY but agree on metric only APPROXIMATELY.** H3/S2 give exact logical (integer-ID) containment but only approximate geometric containment up the hierarchy. So the base path-ID can be exact even where the physical fiber's geometric containment is only approximate -- the seam must tolerate metric slack on the physical side while keeping topology exact (do not assume a child's bounding volume sits cleanly inside the parent's).

**Why not literally one tree:** a person belongs to an org that is not spatially nested inside it (remote workers, multinationals; a satellite belongs to a nation it is not above). Forcing the trees identical would corrupt one axis. The live precedent HiGS/PHiSSG keeps spatial AND semantic relations on one graph with per-node frame+label and recursive pose propagation -- but does NOT cleanly factor spatial-containment from semantic-membership. The two-fibrations framing is the honest repair; the unfactored single graph is the thing to AVOID.

### 3.2 Node schema

```
MembraneNode N {
  path_id        variable-length integer; full ancestor chain (H3/S2-style, EXACT)
  // physical fiber
  anchor_double  vec3 (double precision)   world origin of N
  R_parent       SO(3)                      rotation relative to parent
  db_N           log2(metres-per-local-unit) -- scale RELATIVE TO PARENT, in bits
  // latent fiber
  C_N            convex region in meaning-space (containment = convex inclusion)
  k_max_N        max meaning budget, in Matryoshka dims
  // COIN
  measured_bits_node   physical: PCGS/EntropyGS/SPZ bit-cost
                       latent:   [SPEC] KARL min-token-count OR embedding-eigen-index
  // base edges
  edges_to_children    each tagged in { SPATIAL, MEMBERSHIP, BOTH }
}
```

Absolute physical scale = `sum(db along path)` -- the `log2` ladder doubling as the precision-rebasing ladder. Absolute meaning at budget `k` = first-`k` dims of `C_N` (Matryoshka prefix), with `C_child` convex-included in `C_parent`.

### 3.3 The parent->child transforms (the connection on the bundle)

```
PHYSICAL:  x_parent = anchor_child + 2^(db_child) * R_child * x_child_local
LATENT:    meaning_at_budget(N, k) = first-k dims of C_N's coordinate
           containment: C_child subset-of C_parent
```

The physical transform carries exactly ONE `log2`-scale step; composing down a path sums the `db_i`. The latent transform carries one Matryoshka-prefix step = one rung of description-length bits. **Traversing the tree DOWN is literally accumulating bits on the keystone's single log axis** -- physical depth and semantic depth are the same currency (bits), read through two metrics.

### 3.4 The coupling seam

`same tree?` is answered **locally, per-edge**, by the edge tag:

- **BOTH** (spatial AND membership): the two fibers coincide here.
- **MEMBERSHIP-only:** the fibers fork (semantic nesting without spatial nesting).
- **SPATIAL-only:** geometric nesting without semantic membership.

**[SPEC] The seam may be a DIAL, not a switch.** To match the project's continuous-dial philosophy, replace the 2-bit tag with a continuous coupling coefficient `kappa in [0,1]` (`0` = pure membership, `1` = pure spatial coincidence). Then the degree to which the two trees coincide at a node is itself a renderable, dial-able quantity.

**The seam node is where a physical bit becomes a semantic bit -- and the ONLY place that conversion is legitimate.** The conversion event is: physical event -> measured signal -> latent claim. A single PERSON is the canonical seam node: physically (person in room in building in city in planet) and latently (person in project in org in civilisation) the two fibrations meet at the person.

**[SPEC] Two unresolved coupling problems** (carried to section 5 / open questions): (a) the physical fiber re-bases continuously on the camera; the latent fiber has no spatial origin to re-base on (its "origin" is a meaning-subspace, not a point) -- coupling the two re-basing schemes at the seam is underspecified. (b) With two edge types, the LCA differs per fiber; a camera-node and target-node in different membership branches but the same spatial branch have two different lowest common ancestors -- whether there is one canonical walk or two parallel walks reconciled at render is open.

### 3.5 [SPEC] Membrane = Markov blanket

Adopt **nested Markov blankets (FEP)** as the non-arbitrary definition of where each membrane boundary sits and why the wrapper pattern recurs `galaxy -> ... -> artefact`. This turns "wrapper" from a UI metaphor into a statistical boundary that gates inside/outside information flow -- which aligns with the COIN: **the membrane is exactly where measured vs rendered bits are reconciled.**

---

## 4. The collapse symmetry, and the verdict on dial-as-thesis

### 4.1 The symmetry

Both ends of the dial collapse to a single token: the whole universe collapses to a dot, total civilisation collapses to a word. Both are the same variational move -- minimise a rate-distortion functional under a budget `B`:

```
render_B(X) = argmin_Y D_X(Y)   subject to   codelen(Y) <= B
```

The budget `B` and the `argmin` template are shared across physical and latent. The RG <-> Information Bottleneck equivalence is PUBLISHED (Gaussian IB IS the non-perturbative RG; RG-relevance = IB-relevant-information), so "zoom-out = integrate out short-distance / irrelevant DOF" is a real theorem on the physical side, not a vibe.

### 4.2 The verdict: ONE OPERATOR FAMILY, not one coordinate

This is the load-bearing honest call, and it is a **demotion from the strongest reading of the thesis:**

> **The dial is REAL as a shared variational principle (one log axis of BUDGET `B`). It is NOT real as a single coordinate, because the distortion metric `D` differs between the two axes.**

The reasoning:

- **What a bit COSTS differs.** Physical `D` = pointwise / projection L2 metric error (a Gaussian's `sigma` in metres). Latent `D` = negative-log-likelihood under a prescribed generative conditional (2026 semantic-compression work: distortion is measured in a model's BELIEF, not in any metric on the embedding space). Two different `D`'s sharing one `argmin` template is an operator FAMILY, not one coordinate. The keystone's "all bits on ONE log axis" is true at the level of `B` (codelength) and FALSE at the level of `D` (cost). **Pav's dial reads the same `B`; it does not read the same axis.**

- **The collapse symmetry over-claims in DYNAMICS.** Physical RG is ~isotropic and has a fixed-point structure (universality -- this is WHY coarse-graining yields clean mass/charge/spin). Semantic abstraction is anisotropic with **no universality theorem** -- there is no proof that summarising "US Government" -> "Gov" flows to a fixed point rather than chaotically losing the functional geometry. The symmetry holds in NOTATION (both discard bits monotonically) and is unproven in DYNAMICS (one has a renormalization fixed point; the other has no guarantee of one).

- **The literal-one-bit reading is wrong.** A word from a 50k vocabulary is ~16 bits, not 1. It is a "one-token collapse," not a "one-bit collapse."

So: **coincidence at the level of notation and budget; genuine shared structure at the level of the variational principle; NOT identity at the level of coordinate or dynamics.** The dial is a real instrument built on a real shared principle. Calling it "one coordinate" is the over-claim an external pass will shoot down; calling it "one variational principle read with two distortion metrics" is the defensible thesis. That is still a strong, original claim -- **and it is exactly enough to build the viewer.**

### 4.3 The philosopher's adjudication: is `q` a coordinate or a category?

The dedicated philosopher pass ([scope_philosopher_take.md](scope_philosopher_take.md)) tightened this verdict without overturning it, via one move the externals missed:

**L2 distortion IS a negative-log-likelihood.** Under a Gaussian observation model `q(X|Y) = N(X; Y, sigma^2 I)`, `-log q = ||X-Y||^2 / 2sigma^2 + const`. So `D_physical = NLL[q = Gaussian]` and `D_latent = NLL[q = generative conditional]` are **one distortion (NLL) under two likelihoods**, not two different metrics. "The metric on metres was a likelihood in a lab coat." This collapses the red-team's "two cost spaces" into **one cost space (NLL) foliated by the decoder `q`** -- a real promotion of the demotion.

But it stops there, because **`q` carries the physics**: the Gaussian `q` is isotropic + shift-covariant (cost depends only on `X-Y`), which is *why* physical RG has a fixed-point structure; the LM `q` is neither. The duality did not vanish -- **it migrated from "two `D`" into "two `q`."** So the deepest question is reframed and made answerable:

> **Is the observation model `q` a COORDINATE (one knob whose settings include both decoders) or a CATEGORY (two different machines)? The dial is the thesis iff `q` is a knob.**

**On the anisotropy / no-fixed-point objection (Gemini's falsifier): not fatal -- it is the CONTENT.** Build the **viewer-as-instrument** (a semantic-fixed-point *detector*), not the viewer-as-claim. A semantic flow that loses functional geometry should render as terminal blur -- so the COIN honesty badge *doubles as the no-fixed-point detector*. This is consistent with the project's ratified epistemics (exploratory instrument, 0.99-not-Boolean); building the viewer-as-claim would contradict them. 2026 work (RG-for-DNN fixed points, arXiv 2510.25553; Semantic Identity Compression zero-error laws, arXiv 2601.14252; RGMem, arXiv 2510.16392) reads early-positive, so the experiment is live, not hopeless.

**The promotion theorem** (what would make it TRUE, not just false). The single-coordinate thesis holds iff: **(a) decoder-as-coordinate** -- a single parametric family `q_theta` with a continuous path connecting the Gaussian and LM decoders (e.g. exponential-family decoders with continuously-deforming sufficient statistics); **(b) semantic fixed points** -- the budget-lowering flow has non-trivial fixed points with a relevant/irrelevant operator split (Wilsonian universality for meaning); **(c) symmetry alignment** -- the physical fixed points (mass/charge/spin) and the semantic survivors are images of one another under one shared symmetry. **Attack (b) first**, and it is measurable *today*: iterated rate-distortion compression of a fixed corpus, as `B` decreases, should show a **relevant/irrelevant spectral gap** in the linearized flow (a few `O(1)` survivors + a decaying tail). Gap present -> reading a real fixed point; gapless/chaotic -> the family verdict stands. **The spectral gap is the one number the viewer should be built to display.**

**Meditation (register shift, speculation).** Both collapses keep what *a particular observer could not afford to lose*; the survivor is a property of *the budget meeting the decoder*, not of the system. Physical RG hides this because its Gaussian-isotropic `q` pretends to be the view-from-nowhere. The question we are not asking is **"whose decoder?"** -- the real dial has a second knob (`q`) we have been holding fixed, and the deepest setting is not a budget at all, it is `q`. What does the universe look like collapsed under the *civilisation's* decoder rather than the Gaussian's?

---

## 5. Honesty and risks: where a fake measured bit sneaks in

The COIN as originally stated (`rendered <= measured`, per leaf) guards the EXTREMES that everyone watches (universe-dot, civilisation-word). The leaks are in the MIDDLE, and unbounded LOD/nesting opens three new doors:

### 5.1 The aggregation seam (the single biggest gap)

When zoomed out you do not show measured child splats -- you show a **parent aggregate** (`Sigma_parent` = weighted sum of child covariances + variance of child means). That parent splat is a MODELLED summary. If even ONE child was measured-crisp, the parent can inherit a deceptively tight covariance and render as if the AGGREGATE were measured. **The COIN as written does not constrain the aggregation operator.** A second inequality is required, and is currently missing from the base spec:

```
rendered_bits(parent) <= measured_bits(children) - bits_discarded_by_summary
```

where `bits_discarded_by_summary` is defined operationally as e.g. the KL between the true child mixture and the single parent Gaussian. **This is the missing half of the COIN.** Without it, the container can manufacture crisp bits the substrate never paid for.

### 5.2 Generative LOD past the measured ceiling

At high zoom past `measured_bits`, any neural upsampler paints plausible detail. Under the COIN this MUST stay blurred or be channel-tagged MODELLED. But continuous LOD (CLoD-GS) interpolates SMOOTHLY through the measured ceiling with no natural discontinuity -- **smoothness and the honesty cap are in direct tension.** There is no built-in tripwire at the exact bit where measurement runs out. **You must INSERT a hard per-node ceiling marker at `measured_bits` that the smooth dial cannot slide past unnoticed.**

### 5.3 The dial middle (`0 < theta < 1`)

At an intermediate dial position, an entity is interpolating between its physical coordinate and its semantic coordinate. That intermediate position is **pure model** (a force-directed / UMAP-style layout), yet it would render with whatever sharpness the endpoints had. Every pixel at `0 < theta < 1` is a modelled position that can masquerade as measured. **Render law for the middle: force maximal blur / MODELLED-channel tagging everywhere the coordinate is an interpolation, and earn sharpness back only as `theta` approaches a frame where the coordinate is actually measured.** Without this rule the dial middle is a fake-measured-bit factory.

### 5.4 Two more leak points under nesting

- **Per-node local floor leak.** The per-node local bit-budget is the genuinely UNBUILT piece (precision-graded cohomology applies precision GLOBALLY, not per-stalk). A sloppy node could set a high local floor and render fake-crisp. The law needs a global invariant enforced at page-in: **a node's local floor can never exceed its `measured_bits_node`**, or the honesty cap leaks at membrane boundaries.
- **measured-bits estimator soundness.** Algorithmic RD is uncomputable; the practical proxy is entropy-constrained quantization (PCGS/EntropyGS/SPZ). The honesty cap is only as strong as that estimator: **the quantizer's bit-count must UPPER-bound the true RD function.** If it can under-count, a fake bit passes. The latent estimator (KARL token-count vs embedding-eigen-index vs Matryoshka prefix length) is not yet canonical -- the COIN inequality is only meaningful once one unit is fixed.

### 5.5 The ONE settling experiment

**Build a static BIT-SLICE ATLAS on ONE shared entity that lives on both fibers -- a single PERSON (the seam node).** Physical chain: person in room in building in city in planet. Latent chain: person in project in org in civilisation. Annotate every node on BOTH chains with `{scale_bits, measured_bits, required_bits_to_refine, summary_codelength}`. Sweep ONE budget `B = 0..N` and check THREE conditions (failure on any one kills the single-coordinate reading and confirms "two logs sharing a formula"):

- **PASS-1 (shared budget):** the same `B` drives both physical refinement (`sigma` halves per bit) AND latent refinement (summary gains one rung per bit) with **NO per-side tuning.**
- **PASS-2 (middle is structured):** freeze the morph at `theta = 0.5` on the person node -- is the physical<->semantic intermediate **cognitively structured or spaghetti?**
- **PASS-3 (the actual COIN test):** at every `B`, verify NO node renders sharper than its `measured_bits` AND **no PARENT renders sharper than its faithful aggregate of children** (section 5.1). If a parent ever out-sharpens its measured children, the single-coordinate claim is dead even if PASS-1 and PASS-2 succeed -- it proves the container manufactures crisp bits the substrate never paid for.

PASS-1 and PASS-2 test whether the dial is one thing; PASS-3 tests whether it is HONEST. You need all three.

**The second experiment (the PROMOTION test, from the philosopher pass).** The bit-slice atlas tells you whether the dial is honest and self-consistent as a *family*; it does NOT tell you whether the family collapses to a single coordinate. For that, run the **semantic spectral-gap probe**: take a fixed corpus, apply iterated rate-distortion compression at decreasing budget `B`, linearise the budget-lowering flow, and inspect its eigenvalue spectrum. A **relevant/irrelevant gap** (a few `O(1)` survivors + a decaying tail) is the semantic analogue of a Wilsonian fixed point -- evidence that "civilisation-to-word" flows to an attractor the way "universe-to-dot" provably does, and exactly the condition (section 4.3b) that would promote the thesis from operator-family to one coordinate. Gapless or chaotic -> the family verdict is final. It is measurable today on a real embedding model, independent of building the viewer, and **the gap is the one scalar the viewer should display.** Atlas asks *is it honest?*; spectral gap asks *is it ONE?*

---

## Open questions for Pav

> **RESOLUTION STATUS - batch 2026-06-14.** All eight resolved or given provisional defaults by a four-workflow Opus batch + a codex/gemini cross-pass. Detailed verdicts: [open_q_seam_zone.md](open_q_seam_zone.md) (Q5 + the zone/lifecycle model), [open_q_units.md](open_q_units.md) (Q1/Q2/Q4), [open_q_geometry.md](open_q_geometry.md) (Q3/Q6/Q7/Q8), [open_q_musk_sample.md](open_q_musk_sample.md) (data-grounded test on Elon Musk). **Headline: the keystone's one log now does a FOURTH job - the latent<->physical coupling is the COIN on POSITION (`sigma = 2^-location_bits`).**

| Q | Verdict (provisional) | Doc |
|---|---|---|
| Q1 latent unit | prequential online-NLL codelength under a pinned coder, KT-gated; KARL demoted winner->dial; canonical object is a CURVE `measured_bits(tau)`, kink `k*` = latent Planck floor | units |
| Q2 radix | power-of-2 both fibers (O(1) LCA); octree (3b) physical, radix-2 (1b) latent. CORRECTION: one octree level = ONE octave -> ~618-bit path -> integer-rung+float split is MANDATORY (not "~69 rungs") | units |
| Q3 geometry/blur | integer path-ID PRIMARY (hard cap) + Poincare SECONDARY (dial); ONE blur primitive (heat-flow, `sigma=k*2^-bits`) read through two charts; Matryoshka prefix = the LOD budget, NOT the blur | geometry |
| Q4 ceiling N | NO honest fixed N and none needed (rendering is window-relative; pay the ancestry path, not the corpus); optional soft blurred dated scale-bar `N_soft ~ log2 48` text / `71` all-media | units |
| Q5 seam toggle-or-dial | **DIAL** = the COIN on position; `kappa = 1 - H_spatial/H_max` (location-negentropy, derived not declared). Toggle demoted to a query-algebra overlay (egg-yolk/RCC), legal only at provable endpoints | seam_zone |
| Q6 budget | **ONE** budget, two steering signals (gaze + meaning-attention), water-filled; two-layer per-observer audit (`sup over observers rendered <= measured`) | geometry |
| Q7 theta commute b | PARTIAL; fix = carry b as an ADDITIVE shift in the log chart, all multiplicative zoom in the final screen affine; canonical order specified; `d=0` pixel-identity = a cheap keystone falsifier | geometry |
| Q8 per-stalk filtration | BUILD THE PROOF (one hypothesis turns the aggregation cap into a theorem + gives transitivity free), DEFER the machine; cheap per-edge integer check at page-in | geometry |

**New findings beyond the eight (from the batch):** the keystone may do a FIFTH job (Q8: valuation = bits, a DVR grading); the base is a **DAG with diamonds**, not a tree (the Musk 2026 SpaceX-xAI merger); the two fibers have **different bit-ceilings** (latent attribution is irreducibly fuzzy); latent edges are **typed** (contains vs originated-vs-amplified); **influence is sign-bearing** -> a candidate **VALENCE third coin** (`valence_bits`); the aggregation cap needs the **spread-of-means term** (forbids broadcaster+audience collapsing to a fake centroid); zones render as **Monte-Carlo stipple, never isolines**; migration must be **event-driven** (grow the blur between measured events, never interpolate a fake path).

**Decisions that were genuinely Pav's** — RESOLVED 2026-06-14, see *Ratified refinements* below (per-channel prior, typed-edge DAG, valence third coin, and the render-detail forms adopted; only the hostile-subject test and the strength x type unification remain open). The forks, as originally posed: the **base prior** for `kappa` (uniform-Earth vs population/attention - decides whether a zone reads as signal or demographics); **tree vs typed-edge DAG** as the primitive; whether to add a **valence third coin**; the **origin-default render** (blurred yolk when attribution is contested, vs sharp yolk + dim conditions-egg); **dying-entity render** (fade vs contract); **observer-relative solidity** (felt vs one-number); **one dial or two** (coupling strength vs coupling type); and the **next test subject** (B recommends a deliberately HOSTILE case - a pseudonymous founder / authorless idea - to try to falsify the model rather than confirm it).

---

1. **Unit of `measured_bits` on the LATENT axis.** Physical is settled (PCGS/EntropyGS bits-per-splat, or SPZ size). Latent: KARL min-token-count, embedding-eigen-index, or Matryoshka prefix length? They give different numbers; the COIN is only meaningful once one is canonical.
2. **Bits per ladder level (the branching radix).** 7 bits/level -> ~30 levels, LCA ~30 compares; 1 bit/level -> 206 levels. This sets tree depth, path-ID width (64-bit / 128-bit / variable), and LCA cost. Choose a radix per axis.
3. **Latent base geometry: hyperbolic/Poincare or integer path-ID?** Hyperbolic gives continuity for free (radius = specificity, log-metric composes with the keystone) but loses exact-integer containment; integer gives exact containment but needs continuity bolted on. Which is primary -- and does "semantic blur = geodesic pull toward the origin" give us ONE blur operator for both fibers?
4. **What is `N` (max latent bits = "total civilisation")?** Physical has a hard ceiling (`+89`). The latent ceiling is undefined. Without one, `delta_b` windowing on the latent axis has no normalisation.
5. **Seam coupling: 2-bit tag or continuous `kappa` dial?** And how do the two re-basing schemes (physical floating-origin vs latent meaning-subspace, no shared zero) couple at the seam without desyncing meaning-LOD from physical-LOD as the camera moves?
6. **One budget or two under foveation?** When the observer attends to a node, do physical-bits and meaning-bits reallocate by the SAME policy (the COIN suggests one budget) or two? Note foveation makes honesty observer-relative on the budget side (two observers see different `rendered_bits`) while staying absolute on the measured side -- audits must be per-observer.
7. **Does the unroll dial `theta` commute with the scale ladder `b`?** Can you zoom and unroll in either order and get the same view? If the conformal chart transition is not scale-equivariant, `(s, delta_b, theta)` is not a clean product and dial interactions need explicit ordering.
8. **Formalise per-node precision as a per-stalk filtration?** Extending precision-graded cohomology from GLOBAL to per-node makes the COIN a per-node, per-level cohomological obstruction -- the rigorous form of the per-node bit budget, but possibly heavier than the engineering needs. Worth it, or over-built?

---

## Ratified refinements (2026-06-14, Pav decisions)

Four forks were put to Pav after the open-Q batch. His calls, and how each lands in the spec:

### R1. The `kappa` base prior is PER-CHANNEL (not uniform-Earth)

The coupling dial `kappa = 1 - H_spatial(A_e)/H_max` measures localization relative to a PRIOR, and the prior is chosen **per evidence channel**:

- **operations / facilities / legal-domicile** -> prior = **UNIFORM** over the visible support. A factory is genuinely localized against "anywhere on Earth."
- **attention / influence / membership** -> prior = the **POPULATION x internet-access** (x language, where known) distribution. A field that merely mirrors where people already are scores `kappa ~ 0` = honest (it is demographics, not reach). **Reach is only what EXCEEDS the population prior.**

The honesty win: the "Siberian-hacker / virus-only-hits-Wall-Street" and "attention = demographics" leaks **self-cancel by construction** — an attention zone must beat the population baseline to register any coupling at all. Each channel **discloses its prior**, and the prior is a dated, versioned object (population rasters change). Composes with the per-channel `measured_bits` split already in the addendum.

### R2. The primitive is ONE TYPED-EDGE DAG; physical and latent are PROJECTIONS

The Musk data falsified the clean-tree reading (the 2026 SpaceX-xAI merger + orbital data centers put single nodes in two fibers at once = a diamond). Ratified model:

- **ONE base:** a directed acyclic graph `G` of membrane-nodes, each with a path-ID-style address generalized to a DAG (a node may have >1 parent).
- **TYPED edges:** each edge carries a type in `{CONTAINS-spatial, CONTAINS-member, ORIGINATED, AMPLIFIED, RE-POINTED, ...}` plus a continuous coupling coefficient (R4).
- **Physical and latent are two PROJECTIONS** `pi_phys(G)`, `pi_lat(G)` of the one DAG — not two separate trees. `pi_phys` follows spatial-containment edges; `pi_lat` follows membership/origination edges; where an edge is BOTH, the projections coincide (the seam).
- **LCA -> lowest-common-ancestor-SET** on a DAG (a node may have several); per-pair rebasing uses the nearest common ancestor in the relevant projection. Cost rises from `O(depth)` to `O(depth x in-degree)`, bounded because membrane in-degree is small.
- **Per-fiber bit-ceilings** (Musk PASS-1): the shared budget carries a ceiling PER PROJECTION, so the latent projection (attribution, irreducibly fuzzy) is never over-sharpened by physical bits.

This **supersedes** the "two fibrations over a base poset" wording where they conflict: the poset becomes a DAG, the fibrations become projections, and the diamonds are first-class.

### R3. VALENCE is a THIRD coin

Influence is sign-bearing and observer-relative, so the COIN currency gains a third axis alongside location-bits and render-sharpness:

- **`valence_bits(x | observer)`** — a signed, observer-relative field. Magnitude = how confidently we can measure the SIGN of an effect for that observer; sign = `+` / `-` (favorable / hostile). "We can measure he is salient (location/attention bits) far more confidently than we can measure that he persuades (valence bits)."
- **Render:** an influence zone carries BOTH a magnitude field (location-negentropy, R1 per-channel) AND a valence field (`+` lobes warm, `-` lobes cool, unknown = grey). **A single 'influence' magnitude is FORBIDDEN** — it averages away the sign (the load-bearing Musk finding).
- **Honesty:** valence is Stratum-2 (modelled / observer-relative), ALWAYS badged, and obeys its own COIN (never render a sharper sign than measured). The observer enters the render (ties to the per-observer audit and to the frame-relative-classifier frame — valence is a frame/dial-setting; frame-lock keeps it falsifiable).

### R4. The remaining render-detail forks — resolved to the batch defaults

Pav chose "keep refining the spec," so the smaller forks close with the honest defaults the batch recommended:

- **ORIGIN render:** egg-yolk ALWAYS (yolk = the calling event, egg = the conditions prior, white = the gap). Yolk sharpness is **capped by attribution-confidence** (Stigler's law): a contested origin renders BLURRED even though it is a "point" — the contest is measured uncertainty about WHO, not WHERE.
- **DYING entity:** **FADE** (opacity -> 0), never re-sharpen and never keep blooming, and **not** contract toward a last stronghold (contraction would assert a motion we did not measure). A dead entity stops paying measured bits, so it loses the right to render sharp.
- **OBSERVER-RELATIVE SOLIDITY:** **YES** — `kappa` is view-relative (it depends on `H_max` = the visible support), so an entity's "solidity" (the comet-tail thickness) legitimately changes as the viewer zooms; the nucleus does not. Consistent with the one-budget foveation model, and guarded by the two-layer per-observer audit: blur from budget/view is per-observer + reversible; blur from measurement is global + permanent — never let the first masquerade as the second.
- **ONE DIAL OR TWO:** **TWO, but ranked.** `kappa` (coupling STRENGTH = the COIN on position) is the primary, fully-ratified dial. Coupling TYPE (spatial <-> membership) is the continuous coefficient on the typed DAG edge (R2) — **provisional [SPEC]**, the genuine open frontier (no 2025-26 work unifies continuous-strength with continuous-type). v1 ships the strength dial; the edge type is authored discretely, with continuous type-interpolation reserved for v2.

### Still open (deferred, not decided)

- A **HOSTILE falsification subject** (pseudonymous founder / authorless idea / anonymous collective) — Pav chose spec-refinement over running it now; it remains the strongest next falsification test, and the right move before trusting any zone as a real coordinate (cf. the Model-A-vs-B settling test).
- The **unification of continuous-strength x continuous-type** into one coupling manifold (R4).
- The **estimator-soundness gap** (does `measured_bits` upper-bound true content?) — outside the cohomology; stays open.

### R5. New conceptual layer (2026-06-15): wrappers, the probe, the observer

A v0.3 layer is added in [WRAPPER_PROBE_OBSERVER.md](WRAPPER_PROBE_OBSERVER.md): every fact wrapper = six honest axes (WHAT/WHEN/WHERE/WHO/HOW/WHY) + the observer axis (WHOM) + BEFORE/AFTER links + **per-axis `measured_bits`** (the six axes ARE the per-channel COIN; each spawns a latent FIELD + a CLASS on "the sphere of a fact"; WHY is the structurally-blurriest axis, WHO carries the Stigler cap). **Origin** is retroactive + definition-relative — a fuzzy multi-beat spike on an *agreed* (intersubjective) record; identity = the diachronic definition trajectory `D(t)`. **Observation** is the **excitation-emission keyhole probe = spreading activation**: shine a time-indexed concept-light `P = D(t_def)` into the agnostic substrate, resonance spreads along typed edges, excited wrappers ping back as **sparks** (instance/principle matches across disconnected space-time), the ping capped by the COIN, with a **participatory back-reaction** (observing influences the global dynamics — badged). **Glasses = observer/decoder, frame = agnostic substrate.** Person-nodes gain a Stratum-2 **mind-sandbox** (inner canon distilled from said+did, + tribe), with the said-vs-did gap rendered as a measured signal. Taxonomy fix: **democracy != the number 4** (R1's population prior is why), the `kappa` spectrum runs formal-content -> socio-historical structure -> concrete entity, and even **0 has a zone** (the probe chooses formal-content vs social-instantiation).

### R6. The keyhole block universe (2026-06-15): how the substrate is built and observed

A v0.4 layer is consolidated in [KEYHOLE_BLOCK_UNIVERSE.md](KEYHOLE_BLOCK_UNIVERSE.md) (4-workflow batch K1-K4 + codex/gemini). Verdict: real machinery, not metaphor. **The block is the TARGET (`B*`), never the stored artifact** - we accrete `measured_bits` in our estimate `B_hat_tau`, never write the past; the substrate is **bitemporal** (`t_event` vs `t_obs`; "no as-of-tau, no honesty"). **The compiler** = DBSP delta-stream + a CALM **join-semilattice merge** (monotone, idempotent, order-free) with `measured_bits` as an **up-only lattice** and a fuzzy **stub as the lattice bottom**; the block is a **materialized view over the append-only log**, so every rendered bit traces to an event. **Observation = multi-keyhole tomography:** each burst is a projection, `measured_bits` = the frequency-volume the slices fill, fidelity accrues as **conditional mutual information** (submodular - **diversity beats density; corroborated = independent route**), with a two-regime curve and a hard **error floor** (= "never render a fake measured bit"). **Honest fuzz:** the missing wedge marks where to place stubs; gaps **blur not streak** (bandpass/compressed-sensing); generate-second, flagged, lower-bits; a **held-out-view confabulation audit** as a runtime COIN check. **Obs->meaning->knowledge = three per-axis gates** (Kolmogorov structure-kink / corroboration-credence / epiplexity compute-reach); the existing MDL harness is the structure proxy. **Conjecture-stubs** are typed falsifiable holes (noise-floor vs compute-bound; missing what/how/why/link/actor), rendered in a distinct grammar (zoom a fact -> detail, zoom a stub -> empty space), and **a stub's VALENCE = its Expected Information Gain** - the third coin doubles as the next-best-burst objective, so the instrument self-aims at the highest-valence fuzzy region. **Constellation correction (from the democracy run):** a contested construct is a **constellation of sub-principle axes** (a principle-vector), not one blob - the single-blob render is a measurement artifact. **Deep open risk:** the latent axes themselves **drift/rotate over time** (you cannot tomographically scan a concept whose dimensions rotate) - the next design target; three pre-registered falsifiers are listed in the v0.4 doc.

### R7. The honesty DIAL, the 4D drift reframe, and the settling tests (2026-06-15, Pav)

Two corrections folded into [KEYHOLE_BLOCK_UNIVERSE.md](KEYHOLE_BLOCK_UNIVERSE.md) sections 0 and 9:
- **The COIN is a DIAL, not an absolute.** EXPOSE pole = never render a fake bit (forensic, default); CONCEAL pole = hide all the fakes (seamless / immersive). The invariant keeping every setting honest: the **substrate never lies** (provenance + measured-vs-generated map stay queryable and unchanged) AND **the dial position is always disclosed**; **reversibility** (turn back to expose -> the seams reappear, the audit unchanged) is the proof. **Fraud = passing a conceal-render off as an expose-render.** A new render-intent dial `h_honesty` alongside `theta` (shape) and `b` (scale).
- **A construct genuinely changes over time -> reconstruct as a 4D volume (dynamic / 4D CT):** capture slices, stack, infer the gaps; the earlier latent-axis-drift "risk" was backwards - drift is the *time axis*, not a failure. The only residual fault = **inferring a gap-slice sharper than the bracketing measured slices justify** (a Lipschitz bound = the COIN read along `t_event`).

**Settling experiments RUN - 10/10 checks pass** ([tests/keyhole_tests.py](tests/keyhole_tests.py), [tests/RESULTS.md](tests/RESULTS.md); pure numpy/FFT, a *falsification* harness where the honest policy must beat the dishonest one): **T1** drifting-concept tomography (presentism renders a confident point 0.64 from truth; the honest Lipschitz lens *contains* truth -> blur is honest) validates the 4D reframe + the COIN on the time axis; **T2** Fourier-slice fidelity (diversity beats density; a duplicate burst adds *exactly 0* bits; greedy marginals non-increasing = diminishing returns; active selection reaches 90% coverage in 14 bursts vs 20 even, clustered-in-60deg never; a sharp guess in the unmeasured wedge correlates 0.009 with truth -> only honest render is blur) validates the fidelity law + missing-wedge honesty. One initial check failed = a **test bug** (submodularity tested via fixed-order marginals, which need not be monotone), corrected to the nested-set definition; re-run clean. A cross-model AUDIT (codex + gemini) of the v0.3 + v0.4 docs LANDED ([audit_codex.md](audit_codex.md), [audit_gemini.md](audit_gemini.md)) and **converged on a real demotion**: the docs promote analogies into mechanisms on top of an **undefined latent measurement model** - `measured_bits` on WHAT/WHO/WHY is currently *just a badge*, which gates the COIN, the tomography, EIG, and conceal/expose. Consolidated correction-log folded in as the **AUDIT CORRECTIONS** section atop [KEYHOLE_BLOCK_UNIVERSE.md](KEYHOLE_BLOCK_UNIVERSE.md) (demote-not-kill): two-invariant honesty law (expose cap + a provenance invariant "never render generated AS measured"; conceal needs a non-removable watermark + out-of-viewer threat model); separate append-only EVIDENCE from non-monotonic DERIVED BELIEF (drop "confidence only goes up"); tomography is an INVERSE PROBLEM, Radon/Fourier-slice only on physical WHERE/WHEN; drift is an ALIGNMENT/identifiability problem (anchors + transport maps; anchorless gaps are UNDERIDENTIFIED, not blurry; paradigm shift = a rift); **valence != EIG** (objective = expected utility/cost, EIG one term; valence = the signed field); WHOM is both a content role AND the observer; prior-art = analogy/inspiration not validated machinery. SURVIVES: block-as-target + bitemporal, keyhole=spreading-activation (retrieval), conjecture-stub, constellation, and the physical-axis fidelity law (10/10 tests). **Next work item: define the latent measurement model** (the load-bearing hole). PAV decision pending: conceal-pole watermark floor vs declared-fiction full-conceal.

---

## Note: how this extends `toys/globe_cone_unified.html` and `SPEC.md`

This addendum leaves the keystone untouched and bolts structure onto it. For `SPEC.md`: the single scale coordinate `b` is promoted from a render transform to the literal UNIT of the coordinate, paid in an integer path-ID ladder (range) plus a near-origin float (resolution); the COIN gains its missing second inequality (the aggregation-faithfulness cap) and a sharpened scope statement (one log axis of BUDGET, two distortion metrics -- an operator family, not one coordinate). For `toys/globe_cone_unified.html`: the existing globe<->cone unroll becomes the `theta` dial of one node's local frame, now embedded as a single membrane in a streamable nested tree; the toy's single Earth-anchored frame generalises to per-node local frames with LCA rebasing, and its detail level becomes `rendered_bits = min(measured_bits, lod_budget(zoom))` with a hard per-node ceiling marker so the smooth dial cannot slide past the measured bit. This is a spec addendum, not a build plan -- the one concrete next step it authorises is the static bit-slice atlas of section 5.5, on a single person as the seam node.
