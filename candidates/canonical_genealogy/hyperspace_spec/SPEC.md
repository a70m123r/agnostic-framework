# Hyperdimensional Canonical-Space Viewer — SPEC (design only, no build)

**Date:** 2026-06-14 · **Status:** Tier-3 design spec. NOT built. Generalizes `toys/globe_cone_unified.html`.
**Sources (3 independent, convergent):** an Opus research+design workflow (`hyperspace-viewer-spec`, 11 agents — `external_pass`-style prior-art dig + design panel + synthesis), plus cross-model passes from **GPT-5.5 (codex)** and **Gemini** ([codex_take.md](codex_take.md), [gemini_take.md](gemini_take.md), [SPEC_BRIEF.txt](SPEC_BRIEF.txt)). All three landed on the same math and the same honesty spine.

---

## 0. The keystone thesis (why this can exist honestly)

**One logarithm does three jobs:**
- `v = ln(tan(π/4 + φ/2))` — Mercator's isometric latitude = **the 3D→2D unfold** (the sketch's "LOG TRANSFORM (UV)" is *literally exact*: Mercator = stereographic ∘ complex-log).
- `log2(metres)` — **the physical scale ladder** (the existing cosmic cone).
- `2^−bits` — **render sharpness** (Solomonoff/MDL: appearance = 2^−bits; the COIN).

Space, scale, and meaning are all measured in **BITS on one log axis**. The dial doesn't switch datasets — it **chooses which axis of the one log you read**. That is *why* a single honest container can hold the physical and the latent at once. (The deepest open question, below: if the three logs are truly one, the dial isn't a UI feature — it's the thesis, and the viewer is an argument.)

**The governing law (the COIN, as a render invariant — not a label):**
> `rendered_sharpness(x) ≤ measured_bits(x)` everywhere.
An estimate is *mathematically forbidden* from rendering as crisp as a measured fact. **Blur is the badge.** "Never render a fake measured bit" becomes geometry, not a caption.

---

## 1. Architecture — one canonical state space, many projections

(codex's spine, adopted) — model it as ONE state space, and the dial changes the **view map**, never the substrate:

```
X = Earth(S²) × time × log2(scale) × layer_id × latent_axes × provenance × uncertainty
π_view(X) → R³ (globe / cone)  or  R² (flat map)      # the dial picks π; it MUST NOT mutate X
```

**Three ontological strata, kept visibly distinct at all times:**
- **Stratum 0 — the substrate (the light / measured floor):** `scene.json` certainty/route/entailment. The *only* source of legal sharpness. Replayed, never generated.
- **Stratum 1 — the chart (the dial / the eye):** the conformal log-morph + orthographic camera. Changes *how* the substrate is seen; forbidden from changing *what's in it*. **Reversibility is the proof.**
- **Stratum 2 — the readings (latent layer, frame-glasses, couplings, projections):** all derived, all on the fuzzy/generated face of the COIN, all permanently distinguished from Stratum 0.

**The seam is the product:** the single most important property is that the unified container makes the **measured↔modelled boundary *more* visible, not less.**

---

## 2. The 3D↔2D dial (the log/UV transform)

One scalar **`d ∈ [0,1]`**: `d=0` = 3D globe (pixel-identical to today — regression guard), `d=1` = flat Mercator, every value between = a **real published conformal projection** (a continuous angle-preserving homotopy, not a pixel-lerp, not a cut).

**Chosen map: the Daners / Lambert conformal-conic one-parameter family** (Daners, *Amer. Math. Monthly* 119(3):199-210, 2012 — "many in between"). The cone constant `n` is the dial:
```
isoLat(φ) = ln( tan(π/4 + φ/2) )          # THE log transform; Mercator's y
n         = cos(d · π/2)                   # d=0 → n=1 (stereographic / globe);  d=1 → n→0 (Mercator)
ρ(φ)      = exp(−n · isoLat(φ))            # cone radius from apex
θ(λ)      = n · λ
Xc = ρ·sin(θ);  Yc = ρRef − ρ·cos(θ)       # n→0 straightens to x=λ, y=isoLat(φ) = Mercator
```
n=1 → tangent plane at the pole = polar stereographic = the globe the toy already draws; n→0 → cylinder = Mercator. **Build:** one `surfacePoint(lat,lon,d,B)` doing the conformal work in the **raw (lat,lon) domain before projecting** (the d3 "interpolate the raw projection, never the pixels" rule), returned through the existing orthographic projector. Route *every* draw call through it so nothing snaps. Resample rings/graticule to ~2–3° for d>0.5 (anti-tearing).

**Two orthogonal dials (dissolves today's single-`z` conflation):** `d` = SHAPE (globe↔map); `z` = SCALE (local↔cosmic, the existing log2 cone, unchanged).

**Honesty:** conformal = angle-true but **area-false** without bound toward the poles → fade in a Tissot/area-tint + badge *"AREA distorted by projection (conformal)"* the instant d>0; clamp |lat|≤85° + badge *"poles clipped (singularity)"*; a seamless sphere→rectangle unwrap is **topologically impossible** (codex) → disclose the seam (fade it in the Pacific), never fake it.

---

## 3. The N-layer membrane stack

A layer `L = {id, kind, h (signed altitude=world-Y), radialMeaning, coupling-policy, membrane-style}`.
- **PHYSICAL membrane:** radial = `log2 scale` (the SCALE2 ladder; observer=human at r=0). Solid rings/coastlines. `h=0` (measured baseline brane).
- **LATENT membrane:** radial = **hyperbolic Poincaré** reach: `poincare(reach) = R·tanh(reach/2)`, local→civilizational mapped centre→boundary (Nickel-Kiela 2017; replaces the toy's flat Y-lift so deep hierarchy embeds with low distortion — Euclidean radius would lie). Dashed/hazy. `h=+1` default.
- **Extra membranes** (economic/legal/cultural; or a JEPA-style encoding layer) slot at other `h`.

**The seam that lets one container hold both:** physical = log2 radius, latent = hyperbolic radius — **both radial-log, both in bits.**

**within / under / above = a SETTING** (one 3-way toggle on `h_latent`, badged *"stack frame: ABOVE — modelled arrangement"*): ABOVE +1 (dome; holographic bulk-boundary reading), UNDER −1 (sub-stratum), WITHIN 0 (coincident; the fiber-bundle reading — latent = fiber over each geo base-point).

**Coupling regime** (multiplex networks; De Domenico/MuxViz): ORDINAL (adjacent layers, default) / CATEGORICAL (all pairs). Render via NeRF transmittance `T_k = Π_{j<k}(1−α_j)` so a confident physical fact shines *through* a hazy latent membrane. **Formalisms named as organizing vocabulary, badged metaphor-only:** AdS/CFT bulk-boundary, brane cosmology, cellular sheaves, fiber bundles.

---

## 4. Overlap = energy exchange (the coupling)

Fires when the **same entity** exists in two membranes at coinciding coords at time t. **Honest content: what's exchanged is INFORMATION, not joules** — badged *"coupling = modelled information flux, not measured energy."*
- **Geometry:** a vertical coupling thread (interlayer edge) physical-pin → latent-node. Far = glowing flux ribbon; mid = a **kernel/lens** at contact (light focusing through — ties to substrate-as-light); near = a portal ring.
- **Direction (I/O sign):** physical→latent (up) = an event being *encoded/interpreted*; latent→physical (down) = a model/idea *acting* on the world (the directive cutting Fable).
- **Magnitude:** `E = cert_i · cert_j · beatRecency(e)` (a substrate-derived salience, **never a Joule**).
- **The load-bearing addition — sheaf consistency** (Robinson): each layer = a stalk over the Earth/scale base; coupling = a restriction map; colour = the **agreement residual**. AGREE = warm/steady; **DISAGREE (a *measured* cross-layer contradiction) = RED/FLICKERING — rendered LOUD, never smoothed** (smoothing a contradiction into a pretty field is exactly where a fake measured bit sneaks in). One HUD scalar: **consistency-radius CR** = max residual = "how much the projection is lying right now."

---

## 5. Earth default frame

The camera's home: `d=0, z=0`, centred on Earth, observer parked at the human anchor, clock=now. ("frame: EARTH" button snaps there.)
- **Clock-driven real spin:** `spinYaw = −subsolarLon(now)` (one turn / 24h); toggle REAL/FREE (FREE = manual drag + loud *"spin DETACHED from clock (inspect only)"*).
- **Day/night terminator:** NOAA solar equations (subsolar δ, lonS via EoT; ~30s accuracy); per-vertex `illum = dot(n, sHat)`; night→`#0a1018`, twilight band. On the flat map the terminator is the sinusoid `lat(lon)=atan(−cos(lon−lonS)/tan δ)` — falls straight out of the dial.
- **Moon + Sun:** surface sub-points (Sun at subsolar; Moon via truncated Meeus ~10′) — badged *"modelled ephemeris, not measured substrate"* on a visibly-distinct dashed ring. (Sky-dome alt-az + Moon phase = deferred polish.)
- **Observer-tuned scale dial:** the existing `z`, default = human at r=0; an observer selector can re-anchor r=0 (cell/Earth-r/AU) — *re-labels* the rings, never moves a fact.

---

## 6. The unified camera (pan + zoom, both views)

ONE camera state `{center:{lon,lat}, theta, phi, zoomScale, z, d}` — not two cameras.
- **PAN (drag):** globe (d≈0) = **versor / great-circle rotation** (d3 quaternion drag, no pole gimbal-flip); map (d≈1) = 2D translation; between = `d`-blended, resampled in the raw domain so it never tears.
- **ZOOM = two orthogonal gestures:** wheel = `z` (log-scale human↔cosmic trip up the stack); **shift+wheel = optical magnify** (pure pixels, distorts nothing) — keeping them separate stops a magnify reading as a real scale change.
- **Control cross-fade by d:** orbit-tilt live at d=0, fades out as d→1 (a flat map has no tilt). Gesture map: drag=pan · shift+drag=orbit(d→0) · wheel=z · shift+wheel=optical · `d` slider=UV unfold · buttons: frame:EARTH / spin:REAL-FREE / view:3D-FLAT.

---

## 7. Substrate as light on a sensor

Each fact = a **light emitter**; the current view = the **sensor**; pipeline = forward light transport (Kajiya rendering equation — additive in `L_e`, which is *why* the channel-split is honest).
**Primitive: EWA / 3D Gaussian splat** (Zwicker 2001 / INRIA 2023) — a radial-gradient blob; the EWA low-pass (~1px floor) is the anti-lie floor (an estimate can't render below a pixel as a "point measurement").
**Emission vector (read straight from scene.json):**
```
bits  = w_route(route) + log2(1 + corroborations) + a·certainty
L_e   = certainty                                   # emission/opacity
σ     = max(EWA_floor, k·2^(−bits)); if pending: σ = max(σ, pending_floor)   # SHARPNESS = bits
hue   = ENTAIL_COLOR[entailment]                    # observed/attributed/inferred/search-status
```
Measured+corroborated = tight bright splat; single-outlet/inferred = wide dim splat; **disputed = a two-mode mixture / split glyph, never an averaged blob** (preserves the contradiction).
**Three render channels, additively separate:** MEASURED (route=measured-on-plane AND corroborated only; solid/sharp) · ESTIMATE (attributed/inferred + ALL geo/reach/cosmic positions; dashed/hazy/capped/ringed) · MODELLED (projections, coupling flux, transitional distortion; hatched/animated). A measured pixel's brightness never includes estimated radiance.
**Honesty receipts:** a **VarSplat per-pixel uncertainty overlay** (toggle) + a **"snap to measured means"** toggle that strips all fuzz to the bare corroborated points (proves the glow was uncertainty, not decoration).

---

## 8. Build path (single-file canvas, no heavy libs — extend `globe_cone_unified.html`)

~70% of the chassis exists (orthographic camera, log2 ladder, globe skin, scene fetch, narrator, badge engine, GEO estimate table, frame-glasses, scrubber). ~250 new lines, mostly pure math.
- **Increment 1 (the spine):** `surfacePoint(lat,lon,d)` Daners morph + route all draws through it + pole-clamp/badge + the `d` slider/tween; `factToLight()` (one auditable σ~2^−bits law) + the 3-channel router. *Low risk.*
- **Increment 2 (the lie-prone parts):** `poincare(reach)` + per-layer `drawMembrane` + ABOVE/WITHIN/UNDER toggle; `findCouplings`/`drawCoupling` + sheaf residual + CR HUD; NOAA terminator + Meeus Moon/Sun + REAL-spin; versor pan + optical zoom. *Medium — the data model is the real work.*
- **Increment 3 (polish):** VarSplat overlay + snap-to-measured-means + sky-dome alt-az.

**The biggest risk (single, existential): VISUAL CONFLATION** — once physical + latent share one beautiful container, the eye reads modelled latent/coupling positions as measured. Mitigation is the product's whole job: (1) the COIN inequality (generated things *can't* render as sharp — blur is the badge); (2) permanent Stratum-0 (solid/bright) vs Stratum-2 (dashed/hazy) treatment + standing badges; (3) honest-by-default, every departure disclosed + reversible.
**The one-sentence test for any pixel:** *"Did the substrate pay the bits for this sharpness?"* If no → blurrier/dimmer/dashed/badged, or not drawn.

---

## 9. Illustrations (the spec figures — to be rendered)

FIG-1 the dial filmstrip (globe→Mercator at d=0,.25,.5,.75,1) · FIG-2 the one logarithm (unfold / scale / sharpness = three faces) · FIG-3 the membrane stack + within/under/above · FIG-4 the overlap coupling (flux thread + AGREE/DISAGREE) · FIG-5 substrate-as-light (3 splats by bit-budget + the uncertainty buffer) · FIG-6 the Earth frame (terminator on globe vs flat) · FIG-7 the three strata / the seam · FIG-8 the camera gesture map.

---

## 10. Honesty guards (render invariants) + open questions

Guards (full list in the synthesis): the COIN inequality; 3 additive channels; geo-is-not-substrate; certainty-is-disclosed-subjective (use the *bucket* for the hard sharpness floor); dial area/pole honesty; stack/coupling honesty (contradictions LOUD, CR HUD); astronomy badged; frame-as-frozen-probe (warp-mode loud MUTATE); snap-to-measured-means; metaphor-inflation guard.

**Open questions worth your call:** (1) drive sharpness off **corroboration-count** (independent routes) rather than certainty? (leaning yes); (2) should **"snap to measured means" be the DEFAULT first view** — honest base first, beauty earned?; (3) at high latitude when area distorts, shrink the splat (preserve area) or hold+badge? (hold+badge for v1); (4) the meditation: **if the three logs are one, the dial is the central thesis and the viewer is an argument, not just an instrument** — do we build it to make *that* claim?
