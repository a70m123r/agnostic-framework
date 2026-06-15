*Resolved doc (Q5 + the zone/lifecycle model). Three convergent sources: Opus workflow openq-seam-zone (zone / lifecycle-migration / toggle-or-dial / philosopher / red-team seats) + GPT-5.5 (scope_seam_codex_take.md) + Gemini (scope_seam_gemini_take.md). Brief: scope_seam_brief.txt. 2026-06-14. SPEC-only.*

# Seam, Zone of Influence, and the Toggle-or-Dial Verdict

*Synthesis author's note: this document delivers a verdict on the latent<->physical
coupling, formalises ZONE OF INFLUENCE as a render primitive, and specifies the
LIFECYCLE-ORIGIN migration model. It is SPEC-ONLY (nothing is being built now).
Math is translated back to Pav framework language wherever it touches the keystone.
Speculative claims are marked [SPEC].*

---

## 0. One-paragraph answer

The coupling between a latent thing (an idea, a company, a movement, a word) and
its physical anchor is a **DIAL, not a toggle** -- and the dial is not a free
slider we bolt on for taste. It is the **COIN on position**: the same one
logarithm that already does three jobs in the keystone (unfold, scale-ladder,
render-sharpness `2^-bits`) does a **fourth** job here, on location. The anchor is
**always present** (Pav is right: the latent always connects to the physical), but
its **sharpness varies continuously** with how many location-bits the evidence has
actually paid for. A person at the moment they *call* a thing is a sharp point
(many location-bits). An organisation is a diffuse **zone of influence** (few
location-bits, wide blur). The blur is the honesty badge. You cannot render a
sharper coupling than you measured, so the dial is **self-policing**: every setting
is auditable in the one shared bit-currency.

---

## 1. The Verdict: DIAL, not toggle (a grounded dial)

### 1.1 What Pav said, and why it is exactly right

Pav's steer: *the latent ALWAYS connects to the physical*, but the anchor is the
**origin seen through its lifecycle** -- the country, the person who came up with
the idea, or the person who **called** it. For organisations the location is
**FUZZY**: an area of operation, an area of influence, an attention-output -- a
**zone of influence**, not an address. Anchor sharpness varies **continuously** by
entity type and lifecycle stage. The coupling is therefore a **dial, not a
toggle**.

This is correct, and it is correct *for a reason that lives inside the keystone*.
It is not a separate aesthetic preference that happens to agree with the
architecture. We can show the dial is **forced** by the COIN.

### 1.2 The verdict in framework language (no math)

Think of the keystone rule: *you may never draw a thing sharper than the evidence
measured*. Blur is honesty. Now apply that exact rule to **where a latent thing
sits**:

- A latent thing's location is **never a single dot**. It is a **fuzzy patch** of
  light on the Earth -- bright and tight where we have sharp evidence, faint and
  wide where we only know "somewhere around here".
- **Sharp patch = many location-bits = strong coupling.** This is "the person, at
  the moment they named it, standing at a GPS point."
- **Wide patch = few location-bits = weak (diffuse) coupling.** This is "the
  company operates across North America and Europe."
- Between those two is a **continuum** -- every org, every movement, every
  multi-site person, every idea mid-spread. There is no natural place to put a
  switch, because location-bits are a continuous count.

So the coupling **must** be a dial: it is a continuous bit-count, and bit-counts
are continuous. The "toggle" feeling -- *is this thing physical or abstract?* --
is real but it is only the **two endpoints** of this dial showing through.

### 1.3 The verdict in COIN currency (the math, then translated)

Define the **coupling coordinate** `kappa_e` for a latent entity `e`, at a given
view, as the **location-negentropy** of its physical-anchor field:

```
kappa_e(view) = 1 - H_spatial(A_e | view) / H_max(view)        in [0, 1]
```

- `A_e` is the entity's physical-anchor probability field (a fuzzy light-patch on
  the Earth).
- `H_spatial` is the spatial (differential) entropy of that field at the current
  scale -- *how spread out the patch is*.
- `H_max` is the entropy of the **uniform prior** over the visible support (the
  Earth surface at this zoom) -- *the most spread-out the patch could possibly be*.

Read the endpoints:

- `kappa = 1`: the anchor collapses to a single resolvable cell -- **a sharp person
  at a GPS point.** (Maximum coupling.)
- `kappa = 0`: the anchor is present but **no more localized than the prior** -- a
  pure idea, e.g. the number 4. The light fills the whole frame evenly; knowing the
  entity tells you nothing about *where*. (Minimum coupling -- but the anchor still
  exists, it is just maximally diffuse.)
- `0 < kappa < 1`: a **ZONE OF INFLUENCE.** Every real organisation, movement, and
  diffusing idea lives here.

**Translation to Pav language:** `kappa` is literally *"how localized is this
latent thing, measured in bits, relative to knowing nothing."* It is the dial Pav
described. The crucial point -- and the reason this is a *grounded* dial -- is that
`kappa` is **derived from evidence, not declared.** You earn a high `kappa` only by
paying location-bits. A free, hand-set coupling coefficient would be a
fake-measured-bit factory; a measured `kappa` cannot lie.

### 1.4 The keystone tie: the fourth job on the one log

The bridge that makes "blur = uncertainty" a **theorem and not a metaphor** is the
Gaussian differential-entropy identity:

```
h = 0.5 * log2(2 * pi * e * sigma^2)   per axis
=>  location_bits = -log2(sigma / sigma_ref)
=>  1 location-bit = factor-2 in sigma   (and factor-4 in variance)
```

So the kernel blur `sigma`, the coupling dial `kappa`, and the bit-budget are **one
quantity read three ways**. This is exactly the keystone pattern -- *one log, three
jobs* -- applied to the seam. The seam coupling is therefore **not a new axis**; it
is the COIN on POSITION:

```
rendered_location_bits(x) <= measured_location_bits(x)        (the COIN on position)
sigma = 2^(-location_bits)                                    (the blur is the bit-deficit)
```

The keystone already says *render-sharpness = `2^-bits`*. Set that sharpness on the
**location channel** and "low location-bits = wide blur = a zone" is the COIN
inequality, full stop. **The dial-not-toggle verdict is forced by the keystone
itself.**

### 1.5 What survives of the toggle (and why we keep it)

The discrete 2-bit tag `{SPATIAL, MEMBERSHIP, BOTH}` does **not** vanish, but it is
**demoted**:

- It **cannot carry sharpness** (it has no bit-slot), so it **cannot enforce the
  COIN.** It must never be a render input.
- It survives as **schema metadata / a query-planner hint**: it tells the engine
  *which restriction maps / operators are legal* at a node, before the field is even
  computed. A coarse pre-filter, a UI shortcut.
- It is **exactly recoverable** only at the provable endpoints. By the
  tricritical-point argument from partial-interdependence percolation, the discrete
  "fully-coupled" case is the `q -> 1` limit of a continuous coupling fraction; the
  toggle is faithful **only when the entity sits provably AT an endpoint** of the
  dial. Everywhere in the open interior `0 < kappa < 1`, only the dial is honest.
- One genuine virtue the raw dial lacks: the toggle (in its **egg-yolk / RCC**
  form) carries a **relation algebra** -- a calculus for *"does org A's
  influence-zone contain founder B's point?"* So we keep a discrete **egg-yolk
  overlay** *on top of* the continuous field, for query logic only: **dial for
  rendering and the COIN, discrete relations for reasoning about how two fuzzy
  anchors touch.**

**Verdict, stated once more, plainly:** Use the dial. It is the measured
location-negentropy of the anchor field, bounded by measured-bits by construction.
The toggle is its provable-endpoint approximation plus a relation-algebra overlay.
Pav's intuition -- *the anchor is always present, its sharpness varies
continuously, the dial IS the COIN blur on location-bits* -- is **exactly correct**
and now has a closed form.

---

## 2. Zone of Influence as a Render Primitive

### 2.1 The core move: anchor to a FIELD, not a point

A latent entity `e` anchors to the physical layer as a **fuzzy kernel field**, not
a point:

```
A_e(x, t) = SUM_o  w_o(t) * K_space( d(x, x_o) / sigma_o ) * K_time( |t - t_o| / tau_o )

  sigma_o          = 2^(-location_bits_o)             (COIN blur on position)
  location_bits_o  derived from evidence, NOT declared
```

Each anchor source `o` is its **own evidence channel** with its own provenance,
weight `w_o`, lifetime `tau_o`, and location-bits: an HQ address, a factory, a
launch site, a store, an office, a citation, a geolocated post, an event, a member,
a customer. `K_space` is a Gaussian / EWA splat by default -- because for a Gaussian
the entropy identity gives the **exact** bridge "1 location-bit = factor-2 in
sigma," so the kernel's blur **is** the kernel's bit-deficit by identity, not by
analogy.

**Translation:** the entity does not "live at a place." It **casts light on the
Earth** -- a bright tight spot for each thing we measured sharply (a factory we have
the address of), a faint wide glow for each thing we only know loosely (the region
it operates in). The zone is the **sum of all that light**.

### 2.2 The kernel scale IS the COIN

```
sigma_o = 2^(-location_bits_o)
```

This is the whole primitive in one line. Low location-bits -> wide `sigma` -> a
diffuse zone. High location-bits -> tight `sigma` -> a sharp point. The
distance-decay exponent of the classical Huff / gravity model (`U_ij = A_j^gamma *
t_ij^(-lambda)`) is the same dial seen from the spatial-interaction literature:
high `lambda` = tight sharp zone, low `lambda` = wide diffuse zone. The lesson from
mobility-calibrated Huff (optimal decay exponent ~3.8, fitted from Baidu
mobile-location data, +19-23% over hand-set Huff) is decisive for honesty: **the
decay exponent = measured bits, and it must be FITTED from observed interaction
data, never hand-set.** A hand-set sharpness is a fake measured bit dressed as
geometry.

### 2.3 Anisotropy: a zone can be wide one way, narrow another

The render substrate lifts wholesale from 3D Gaussian Splatting: each splat carries
a covariance `Sigma_o = R S S^T R^T` -- an **anisotropic** ellipsoid. This lets a
zone be honestly wide along a coastline and narrow across it (the Burridge
surface-tension shape). **But anisotropy claims bits:** an elongated zone is honest
**only if the directionality is itself measured** (e.g. PCA of geolocated
activity). A hand-set orientation is a fake measured bit. **Default to isotropic
(`M_o = I`) unless the direction is evidence-derived.**

### 2.4 Zone = SUM of evidence fields, never one polygon

Decompose; do not collapse:

```
zone_e(x, t) = operations_field + membership_field + attention_field + legal_field
```

- **operations** -- sharp facility kernels (offices, factories): high bits.
- **membership** -- member/customer residences: medium bits.
- **attention / output** -- geolocated mentions, users, citations: low bits or
  honestly near-global.
- **legal** -- jurisdiction support: a **low-bit uniform-over-region** field ("operates
  in Germany"), **NOT** a sharp per-border claim.

Each is separately provenanced, at its own location-bits. The org renders as a
**Gaussian mixture** of these, **multi-modal by construction.** "Operates in
Germany" becomes a low-bit support field over Germany, not a claim that every border
point is equally influenced.

### 2.5 Honest rendering: three binding rules (no fake crisp boundary)

1. **NEVER draw isolines/contours as ownership boundaries.** An isoline implies a
   hard threshold the data does not contain. Contours are admissible **only** as
   labelled density quantiles ("50% of geolocated activity inside"), badged as such.
2. **Render by Monte-Carlo stippling.** Sample `N` points `~ A_e` and splat them
   semi-transparent. Dense tight cluster = high bits = looks solid; sparse wide haze
   = low bits. **Stippling cannot draw a fake edge because it has none** -- the blur
   *is* the influence gradient.
3. **Adaptive floor.** `sigma_eff = max(2^(-bits), data_spacing, pixel_scale)`. The
   kernel can never render tighter than the data spacing or the ~1px EWA floor
   supports. This is the COIN at the kernel level.

### 2.6 The boundary has its own bit-ledger (the adversarial guard)

A zone has **three distinct bit-ledgers** and leaks whenever it pays a render from
the wrong one:

- **SHAPE bits** -- where influence is concentrated.
- **BOUNDARY bits** -- how sharply the zone ends.
- **MOTION bits** -- whether/how the zone moved over the lifecycle (see Section 3).

The deepest leak: the smoothing kernel (`h`, `kappa`, `Sigma`) is a **render**
parameter, but the eye reads its edge as a **measured** edge. The fix:

- **Never draw a single boundary.** Render a **nested pair** (an excursion-set
  confidence region): an inner **core** inside the true zone with probability
  `1 - alpha`, an outer **envelope** that contains it, and the band between rendered
  as **explicit blur** whose width = the measured boundary uncertainty. **The
  egg-yolk model is literally this:** yolk = inner set, egg = outer set, white =
  uncertainty band.
- **Set boundary sharpness by `N*`, the *effective* number of independent assertion
  events** (after deflating for spatial autocorrelation), **never by the kernel `h`
  and never by raw `N`.** An org's 200 geotagged tweets are not 200 independent
  samples. The boundary's positional error scales ~ `sqrt(1 / (n h^d f))`; a wide
  kernel chosen to "look honestly fuzzy" can make the boundary look *more* confident
  while `n` is tiny -- that is paying boundary-sharpness out of the SHAPE ledger.
- **The settling test -- "is this zone MEASURED or DRAWN?"** Run Kulldorff's spatial
  scan statistic with Monte-Carlo permutation on the entity's actual assertion
  events. If the observed concentration's p-value clears `alpha`, the zone's SHAPE
  is a measured thing and you have earned an inner/outer confidence pair at that
  level. If it does **not** clear, the zone is **DRAWN** (a kernel artifact) and the
  honest render is a **single maximally-blurred field with no boundary at all.** The
  scan-statistic p-value sets the maximum location-bits the renderer may spend; the
  bits<->sigma identity converts that ceiling into the minimum legal blur radius.
  **Measurement and coupling are one act:** the same assertion events that *couple*
  the zone to its anchor are the events that *license* its sharpness.

### 2.7 Binding to the settled architecture

- The latent fiber anchors to a **measure on the base poset**, not a single
  path-ID. The anchor is a weighted set `{(path_o, u_o, location_bits_o)}` of
  base-nodes, each a normal point in the path-ID / LCA machinery. The "zone" is the
  pushforward of these onto the rendered surface via **per-pair LCA rebasing** -- so
  a multi-site org is **precise where its sites are precise and blurry between
  them**, with **no global metric assumed.**
- **Aggregation-faithfulness** (the second COIN inequality) keeps a zone honest
  under zoom-out. When you collapse an org's site-kernels into one parent splat:

  ```
  Sigma_zone   = SUM_o w_o*Sigma_o  +  SUM_o w_o*(mu_o - mu_bar)(mu_o - mu_bar)^T
                                       \_____ spread-of-means term _____/
  bits_discarded = KL( mixture_o || N(mu_bar, Sigma_zone) )
  rendered_bits(zone) <= measured_bits(sites) - bits_discarded
  ```

  The **spread-of-means** term is what **FORBIDS** a two-site org from rendering as
  one deceptively tight blob, and what stops broadcaster + audience collapsing into
  a fake centroid (the "Moon-landing-in-the-Atlantic" failure). This term is
  **required, not optional**; without it the container manufactures crisp bits.
- **Chain-rule COIN:** an `attention_field` child owes only its **conditional** bits
  over the `operations_field` it already shares -- preventing the same city from
  being double-counted as both an office and an attention hotspot.

---

## 3. The Lifecycle-Origin Migration Model

### 3.1 Pav's "origin seen through its lifecycle"

Pav: the anchor is the **origin seen through its lifecycle.** It is born a **sharp
point -- the person who called it** -- and **diffuses to a zone** as the thing
spreads. We honor this literally: the anchor is **time-indexed**. Read it not as a
fixed point but as a probability field whose **mean migrates** and whose **width
grows** with lifecycle time.

### 3.2 Three distinct origins -- do not conflate, do not average

- **conditions_origin** -- the diffuse, pre-naming **causal field** ("the conditions
  that made this idea probable here"). These are **latent ancestors in the
  meaning-tree, NOT spatial origins.** They live on the latent fiber, rendered as
  the diffuse low-bit **egg** around the yolk.
- **person_origin** -- the caller/inventor's sharp-ish biographical trajectory
  (birth anchor, the path of their life).
- **calling_origin** -- the **naming / declaration / incorporation / first-assertion
  EVENT**: a spacetime point `{latent_id, actor_id, x0, t0}` with high bits.

**The CALLING event is the canonical origin** because it is the **SEAM NODE** -- the
single moment a physical bit becomes a legitimate latent bit. This is the one legal
place the physical and latent fibrations are **pinned together**. (This privileges
the declaration over the causal preconditions: right for canonical **identity**, a
defensible-but-contestable cut for causal **explanation** -- so we keep the
conditions field present but render only the calling event on the physical fiber.)

### 3.3 The anchor as a moving, diffusing field

```
anchor(tau) = ( mu(tau), Sigma(tau) )
```

Two distinct motions happen at once:

1. **DIFFUSION** -- the covariance `Sigma(tau)` **inflates monotonically** (the
   width grows). This is the project's log2 double-cone of uncertainty **read
   sideways** along lifecycle time instead of along scale.
2. **MIGRATION** -- the mean `mu(tau)` **drifts** from the origin point toward the
   running centre-of-mass of where influence actually lands (hub-to-hub jumps, not
   just a spreading wave).

**At `t0` (the calling event):** the zone = the caller's footprint. `sigma` tiny,
`kappa ~ 1` -- a sharp point. This is "the person who called it."

**For `t > t0`:** the zone diffuses. The honest free-diffusion law:

```
sigma(tau)^2     = sigma0^2 + 2 D tau
location_bits(tau) = b0 - 0.5 * log2( 1 + 2 D tau / sigma0^2 )
```

i.e. **the anchor loses one location-bit per doubling of `(1 + 2D tau / sigma0^2)`.**
**Lifecycle time literally spends location-bits.** `D` (the diffusivity) is set per
entity-type: a **person-at-origin has `D ~ 0`** (stays a point); an **org/movement
has `D > 0`** (blooms into a zone); a **saturated movement** reaches an equilibrium
`sigma_max` set by its carrying geography.

### 3.4 The dial IS the lifecycle stage

Snap the continuous `tau`-flow onto Hagerstrand's four diffusion stages:

| Stage       | Anchor                         | Dial                 |
|-------------|--------------------------------|----------------------|
| PRIMARY     | near-point origin (the caller) | `kappa ~ 1`          |
| DIFFUSION   | growing centrifugal front      | `kappa` falling      |
| CONDENSING  | filling in, roughly uniform growth | `kappa` low      |
| SATURATION  | stable diffuse zone            | `kappa` low, settled |

Continuous diffusion underneath, named stages snapped on top -- so scrubbing the
lifecycle feels like **growth, not teleporting.** The two spread geometries the
prior art demands both appear: **contiguous WAVE spread** from the origin (physical
fiber) **PLUS hierarchical hub-to-hub JUMPS** (latent fiber over the same base
poset). Empirically the **origin stays sharper than the reach** (patent-citation
geography: spread is more localized than production), so the model gives a tight
inner origin and a wider distance-decaying outer field.

**[SPEC] Snap / tipping:** explosive higher-order contagion (group-overlap phase
transition) means the point->zone transition can **SNAP** at a tipping point. The
dial must therefore **allow a fast `kappa` drop** when a movement "catches" -- a
rapid `kappa` collapse, not a smooth ramp. This is speculative as a render behavior;
it is honest **only if the tipping event is in the record** (see 3.6).

### 3.5 Implementable mechanism: Cox-Hawkes spatio-temporal field [SPEC]

[SPEC] Drive the kernel with a spatio-temporal **Hawkes (self-exciting) process**
(the Cox-Hawkes doubly-stochastic spatiotemporal Poisson form is the exact published
mechanism): a **background intensity** `mu(s)` = the *conditions prior* (why the
origin was probable here), plus a **self-exciting triggering kernel** where each
adoption/influence event excites further events nearby in space-time. The anchor
field at `tau` is `lambda(s | history up to tau)`; its first moment is the migrating
mean, its second moment the diffusing covariance. This gives **both** geometries:
the triggering kernel's local decay = the contiguous wave; long-range excitation
between population centres = the hierarchical hub-to-hub cascade.

### 3.6 The migration honesty guard (the most expensive bit to fake)

Motion is the most expensive bit to fake because **the eye integrates it into a
story.** Two sub-leaks and their rules:

- **Tweening between sparse snapshots draws a path the data never constrains.** A
  migrating mean `mu(tau)` is a **MODELLED** centre-of-mass, not a measured point.
  **Rule:** the animation timeline must be **EVENT-DRIVEN, not frame-driven.**
  Render only at timestamps with assertion events. **Between events, do NOT
  interpolate position -- GROW THE BLUR** (inflate `sigma` to a Brownian-bridge
  envelope covering all paths consistent with the endpoints). A migrating anchor
  must look like a **widening tube of uncertainty that re-sharpens only at measured
  timestamps.**
- **A vMF whose `kappa` shrinks smoothly animates continuous spread when the record
  may be two dots and a guess.** **Rule:** the smooth `sigma(tau)` ramp must hit a
  **hard per-entity ceiling marker at `measured_bits(tau)`** that the dial **cannot
  cross unnoticed.** The zone **freezes its sharpness at the last measured influence
  event and only blurs further, never re-sharpens, into the unmeasured future.**
- **Decline / death.** A diffusing-only kernel never contracts, so every entity
  would grow forever. A dying entity stops paying new measured bits, so its zone
  should **stop being able to render sharp** -- the honest move is to **fade
  (opacity -> 0), not re-sharpen and not keep blooming.**

### 3.7 The egg-yolk render of the origin (honest about WHO, not just WHERE)

The origin-as-person vs origin-as-conditions ambiguity must be **DISPLAYED, not
resolved.** Render it as the egg-yolk dual:

- **YOLK** = the named caller -- the measured sharp point (the calling event).
- **EGG** = the conditions / prior -- a low-bit diffuse zone, explicitly
  lower-certainty (modelled, not measured).
- **WHITE** = the irreducible uncertainty between.

**[SPEC] Attribution caps sharpness.** Eponymy systematically misattributes
(Stigler's law: no discovery is named after its discoverer; multiple independent
discovery is the norm; acclaim flows to the popularizer). So the sharpest,
highest-location-bits anchor -- the named person -- may be the **least causally
faithful.** Rendering the caller as a sharp bona-fide point can manufacture a fake
measured bit *about causation.* **Mitigation:** tag the origin yolk with an
**attribution-confidence that CAPS its sharpness** -- a contested origin must render
**blurred even though it is a "point,"** because the contest is measured uncertainty
about **WHO**, not about **WHERE.**

---

## 4. Worked example: Musk as a comet

Latent node `EM_01` edges-> `{EVs, spaceflight, Mars, X}`. The physical fiber
renders as **four co-existing layers, never merged into one centroid:**

- **origin** -- Pretoria birth anchor. If the source says only "Pretoria," render
  **city-scale blur (~13-14 location-bits), NOT a fake hospital point.**
- **trajectory** -- the "meat" coordinate: a sharp, fast-moving high-bit point
  (private-jet-tracked), `kappa ~ 0.9`. This is the man.
- **company-sites** -- Tesla (Giga Texas / Fremont / Shanghai / Berlin), SpaceX
  (Hawthorne / Boca Chica), xAI (Palo Alto / Memphis / London): a **stationary
  anisotropic Gaussian mixture** of sharp facility kernels, `kappa ~ 0.4`. These are
  **org influence kernels coupled to `EM_01` through role-edges, NOT Musk's body** --
  the crucial bipartite separation.
- **attention-output** -- a continental low-opacity **stipple cloud** over North
  America / Europe: high mass, low spatial bits, `kappa ~ 0.1`, honestly badged
  near-global.

He renders as a **COMET**: a **sharp high-bit nucleus (the man)** dragging a
**low-bit multi-modal probabilistic tail (the zones).** The **dial governs the
tail's render**; the **exact integer path-ID preserves the nucleus.** They are
never averaged into one centroid.

---

## 5. The render pipeline (one place, binds it all)

```
1. Gather anchor evidence sources {o} for entity e at the current view.
   Each o = (path_o, u_o, w_o, t_o, tau_o, location_bits_o,
             channel in {ops, member, attn, legal}, provenance).

2. Build the anchor field as a Gaussian mixture in base-poset coordinates:
     A_e(x,t) = SUM_o w_o(t) * N(x; mu_o(path_o,u_o), Sigma_o)
     Sigma_o  = sigma_o^2 * M_o ,  sigma_o = 2^(-location_bits_o) ,  M_o = I unless measured
     w_o(t)   = base_weight_o * K_time(|t - t_o| / tau_o)        # lifecycle decay/growth
   Positions composed via per-pair LCA rebasing (no global metric assumed).

3. Compute the dial (HUD-reported per entity, WITH its view):
     kappa_e(view) = 1 - H[A_e | view] / H_max[view]
   (single Gaussian: H = SUM_axes 0.5*log2(2*pi*e*sigma^2);
    mixture: GMM upper-bound entropy -- the same budget GAVIS/Spectral-GS use for LOD.)

4. COIN clamp at render (both inequalities, enforced as geometry):
     rendered_bits(o) = min( location_bits_o, lod_budget(zoom) )           # flat / chain-rule cap
     sigma_render(o)  = max( EWA_floor, data_spacing_o,
                             sigma_o * 2^((location_bits_o - rendered_bits(o)) / D) )
     AGGREGATION (zoom-out, collapse sites -> one zone splat):
       Sigma_zone   = SUM_o w_o*Sigma_o + SUM_o w_o*(mu_o - mu_bar)(mu_o - mu_bar)^T
       bits_discard = KL( mixture_o || N(mu_bar, Sigma_zone) )
       rendered_bits(zone) <= measured_bits(sites) - bits_discard          # second COIN law

5. Channel routing: measured+corroborated facility addresses -> MEASURED (sharp);
   ALL reach / attention / influence fields -> ESTIMATE or MODELLED (dashed/hazy/stippled).
   A zone is a model of effect, not a measured boundary -- never below ESTIMATE.

6. Honest draw: Monte-Carlo stipple N ~ A_e; opacity = w_o*certainty;
   NO isolines except labelled density quantiles.
   Bipartite invariant: nucleus (path-ID anchor) in the MEASURED/sharp channel;
   field in ESTIMATE/MODELLED. Never averaged into one centroid.
```

**Why this is not arbitrary:** because `sigma = 2^(-location_bits)` and `kappa = 1 -
H/H_max`, **the coupling strength, the kernel blur, and the bit-budget are one
quantity read three ways.** You cannot dial up coupling sharpness without paying
location-bits. The dial is the COIN on position, and it is self-policing.

---

## 6. Where a fake measured bit sneaks in (and the guard)

| Leak | What it looks like | Guard |
|------|--------------------|-------|
| **CAUSE vs EFFECT** (the existential risk) | A zone is a *projection of effects* -- an attention heatmap is just population / internet-access wearing the entity's label (the Siberian hacker whose virus only hits Wall Street). | **Bipartite state:** the sharp nucleus path-ID is **never replaced** by the field. The field is a *secondary* layer generated *by* the anchor. Plus `kappa` measures gain **over the base prior**, so a population-mirroring field self-cancels to `kappa ~ 0` -- **but only if the prior is correctly chosen.** |
| **Attention = demographics** | A heatmap that just mirrors where people are. | Route `attention_field` strictly to MODELLED; **divide by the base prior** (the negentropy form already does this). |
| **Isolines manufacturing a boundary** | A clean line implying a hard threshold. | Forbidden except as **labelled density quantiles.** |
| **Aggregation crispening** | A multi-site org rendering as one tight blob. | The **spread-of-means** term + the second COIN inequality. **Required, not optional.** |
| **Smooth-zoom past the ceiling** | Continuous LOD sharpening a zone past its location-bits. | A **hard per-anchor ceiling marker** at `location_bits_o` the dial cannot cross. |
| **Anisotropy fabricated from sparse points** | A hand-set orientation dressed as geometry. | `M_o` must be **evidence-derived (PCA of activity) or default isotropic.** |
| **Migration tweening** | A smooth crisp fake trajectory between sparse observations. | **Event-driven timeline; grow the blur, do not interpolate position.** |

---

## 7. SPECULATION (disclosed -- register shift: these are NOT settled claims)

*The following are the author's speculative extensions, beyond what the prior art or
the settled architecture forces. Each is flagged so it never silently hardens into
spec.*

- **[SPEC] The two-channel hardware law.** Promote *"opacity = model bits, sharpness
  = measured bits"* to a **hard two-channel law**, so the renderer is *physically
  incapable* of drawing a sharp high-opacity edge from few events. This would make
  the COIN **architecturally enforced rather than policed** -- the most robust form
  of honesty, if it can be made to compose under zoom.
- **[SPEC] kappa as a felt phenomenon, not just a number.** Because `kappa` is
  observer/scale-relative (it depends on `H_max`, the visible support), two viewers
  at different zooms see different coupling sharpness. This is consistent with
  foveation (honesty is observer-relative on the *budget* side, absolute on the
  *measured* side). Speculatively, this means **"how solid does this entity feel?"
  is itself a coordinate of the view**, not a property of the entity -- the comet's
  tail thickens and thins as *you* move, while its nucleus does not. A genuinely
  novel UX primitive if it holds.
- **[SPEC] A second, orthogonal TYPE dial.** The negentropy `kappa` captures
  coupling **strength** (how localized). There is a *second* continuous coordinate
  the literature half-names but no 2025-26 paper unifies with strength: coupling
  **type** -- *where on the spatial<->membership manifold* an assertion sits (an edge
  that is 70%-spatial / 30%-membership). DSLR/box-embedding interpolation makes type
  continuous; the egg-yolk/RCC algebra makes it discrete. **Unifying
  continuous-type AND continuous-strength is a genuine open contribution, not a
  solved seam.** [SPEC] This may be the real frontier of the coupling seam.
- **[SPEC] The conditions-field needs its own bit-unit.** Physical location-bits are
  settled (Gaussian entropy). The diffuse "conditions that produced the caller" (the
  egg) need a *measured-bits* unit to sit honestly under the COIN -- perhaps
  background Hawkes intensity, perhaps a counterfactual-displacement entropy. Not yet
  canonical.
- **[SPEC] Lifecycle desync as a measurable signal.** The single `tau`-clock pins
  the physical bloom to the latent unfolding, but the two fibers read `tau` through
  different distortion metrics. An entity could be **latently "mature" (fully
  describable) while physically still a sharp point**, or vice versa. Is that desync
  a bug, or a measurable signal about the kind of entity? (A pure mathematical
  object: latent-rich, physically null. A nameless geographic feature:
  physically-sharp, latently-thin.)

---

## 8. QUESTIONS WE SHOULD BE ASKING (register shift -- meditation, not answers)

*These are not problems to close; they are the questions whose framing decides
whether the whole apparatus is asking the right thing.*

- **What is the canonical base prior in `kappa = 1 - H/H_max`?** Uniform-over-Earth
  is naive. The honest null for an *attention* field is the
  **population / internet-access distribution** -- so a field that merely mirrors
  population scores `kappa ~ 0`. **This single knob decides whether a zone reads as
  signal or as demographics.** Does the prior differ per channel (ops vs
  attention)? We have been treating "where is the entity" as the question. The deeper
  question is **"more localized than WHAT?"** -- and the answer changes what the zone
  *means.*
- **Is a zone of influence a real COORDINATE, or only a projection of effects?**
  The settling experiment: Model A (latent graph only) vs Model B (latent graph +
  zone field built from **past** observations only). Hold out **future** geolocated
  observations. If B beats A on calibrated out-of-sample spatial log-score across
  scales, **the zone is a real coordinate**; if not, it is a projection layer to be
  channel-tagged MODELLED. We should ask this *before* trusting any zone as a place.
- **"Influence FOR WHOM?"** -- i.e. *under which decoder `q`?* A regulator, a
  customer, and a rival each see a different zone for the same org (a different
  distance-decay `lambda`). [SPEC] The metaphysics seat argues the latent fiber is a
  **section under a decoder `q`**, not an absolute. Should `q` be a **renderable
  control** (a second global knob, with a visible badge), or a fixed authoring
  choice? If a zone is observer-relative all the way down, the question is no longer
  "where is the influence" but **"whose accounting are we rendering?"**
- **Where exactly is the tripwire between a measured anchor and an interpolated
  zone?** The diffusion fill-in between measured anchor times is **pure model.** A
  smoothly growing zone is *precisely* where generated detail masquerades as
  measured. We keep saying "render model-bits at lower opacity" -- but **where, in
  bits, is the opacity line?**
- **Does `kappa` even need the 2-bit tag?** Can `{SPATIAL, MEMBERSHIP, BOTH}` be
  fully derived from `kappa` + channel-mix? If derivable, the tag is pure
  redundancy. If not, there is a **residual discrete fact the dial cannot capture**
  (e.g. legal admissibility of a restriction map) that must stay as schema. The
  honest version of this question is: **is there anything about the coupling that is
  truly discrete, or is every apparent toggle just an endpoint of some dial we
  haven't named yet?**
- **Is the spectral-gap promotion test stable across decoders `q`?** [SPEC] If the
  "survivor" of a semantic compression depends on the decoder, then *"is the dial
  ONE?"* cannot be answered without first fixing `q` -- and fixing `q` smuggles the
  physical/latent distinction back in. A `q`-invariant gap would be far stronger
  evidence for one-coordinate than a single-`q` gap. We should be asking the
  promotion question **under multiple decoders**, not one.

---

## 9. Open sub-questions for Pav

1. **The prior question is yours to call.** When we ask "how localized is this
   thing," localized *relative to what* -- the whole Earth, or relative to where
   people already are? For a company's attention, "relative to population" feels
   right (it cancels the demographics illusion). Is that the intuition, or do you
   want the zone to *include* the demographic pull as part of its real reach?

2. **Origin: the caller, or the conditions -- and when they disagree?** You said the
   anchor is "the person who **called** it." We render that as the sharp yolk. But
   eponymy lies a lot (the namer is often not the cause). When the named caller and
   the real cause come apart, do you want the **yolk blurred** to show the contest,
   or the **yolk kept sharp** with the conditions as a separate dim egg? (We can do
   both; the question is which one is the *default* honest picture.)

3. **Does a dying thing's zone fade, contract, or grey out?** A company that dies
   stops paying new location-bits. Our honest default is **fade to transparent**
   (it can no longer render sharp). But your intuition might be that a *contracting*
   zone (pulling back toward its last stronghold) tells a truer story. Which matches
   how you see lifecycles ending?

4. **Is "how solid does this thing feel" allowed to change as the viewer moves?**
   The math makes coupling sharpness depend on *your* zoom -- the comet's tail gets
   thicker/thinner as you move, the nucleus does not. Is that a feature you want the
   viewer to *feel*, or should an entity's solidity be reported as one number
   regardless of where you stand?

5. **One dial or two?** [SPEC] We are confident the **strength** of coupling (sharp
   point vs wide zone) is a dial. There may be a *second* dial -- the **type** of
   coupling (spatial-ish vs membership-ish), which also seems continuous and
   lifecycle-dependent (a founder-point morphing into an org-zone). Do you read
   "type" as a second smooth dial, or as a genuinely discrete fact sitting on top of
   the smooth strength dial?

---

*ASCII-clean. SPEC-only. The keystone's one log now does a fourth job: the
latent<->physical coupling, as the COIN on position. The verdict is a dial, and the
dial is the measured location-negentropy of an always-present, lifecycle-diffusing
anchor field -- Pav's intuition, made auditable in the one shared bit-currency.*
