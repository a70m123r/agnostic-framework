Reading prompt from stdin...
OpenAI Codex v0.125.0 (research preview)
--------
workdir: D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ec647-ee64-7820-a6d9-aad08f070c97
--------
user
HYPERDIMENSIONAL CANONICAL-SPACE VIEWER — SPEC BRIEF (design only, do NOT build yet)

We are designing (not building) a viewer. Give out-of-the-box thinking + name real math, theories,
whitepapers, and existing implementations we can build on. Be concrete and cite where you can.

THE VISION (from a hand sketch: a 3D wireframe globe on the left, a flat 2D rectangular map on the
right, and between them the label LOG TRANSFORM (UV)):

1. ONE hyperdimensional space that contains the canonical PHYSICAL and LATENT dimensions, and renders
   them as EITHER a 3D globe OR a 2D unfolded map, switched by a continuous DIAL. The 3D-to-2D unfold
   is a LOG TRANSFORM / UV unwrap (sphere surface to plane).

2. There are N stacked LAYERS, each with a MEMBRANE / WRAPPER (e.g. physical, latent, and more).
   The PHYSICAL domain is stacked in SCALE (log2, observer-tuned by a frame dial set to the human
   observer); the LATENT is stacked ABOVE it (a setting: within, or under) forming the stack.

3. EVENTS at coinciding coordinates make two layers/dimensions OVERLAP = exchange energy / an
   input-output connection between physical and latent (a coupling at contact points).

4. The default frame is EARTH: a rotating globe with a day/night cycle, and the Moon and Sun in
   their positions. A CAMERA can pan around and zoom in, on BOTH the 3D and the 2D views.

5. THE OBJECTIVE: a hyperdimensional space that holds the canonical physical + latent dimensions,
   renders them in 3D or 2D via the dial, and MAPS THE SUBSTRATE INTO IT for full projections,
   like LIGHT HITTING A SENSOR (the substrate facts are the light; the view is the sensor).

CONTEXT (the substrate this projects): a fact-substrate of an event (the 2026 Fable/Mythos AI-model
takedown) with a cast geo-pinned on Earth, dated beats, certainty/route per fact, and a latent reach
axis (local -> civilizational). It already renders as: (a) a 3D log2 cosmic double-cone toy, (b) an
isometric event atlas, (c) a unified globe that flattens-in-log onto the cosmic cone. This new viewer
generalizes those into the hyperdimensional container above.

QUESTIONS WE WANT ATTACKED (out-of-the-box welcome):
A. The 3D<->2D dial via a log/UV transform: which conformal/area-preserving sphere-to-plane maps fit
   (Mercator = log-tangent? stereographic? Lambert? complex log? Riemann sphere?), and how to make the
   DIAL a smooth continuous morph between the 3D globe and the 2D map (not a cut). Any whitepapers /
   implementations (d3-geo, three.js, deck.gl, GPU shaders, conformal morphs)?
B. The N-LAYER MEMBRANE STACK (physical / latent / ...): what existing frameworks model stacked
   layers with membranes that couple at overlaps and exchange energy? (holographic principle /
   bulk-boundary, brane cosmology, fiber bundles, sheaves, manifold layers, multiplex networks?)
   How should within vs under vs above be represented?
C. The OVERLAP = ENERGY EXCHANGE event: how to render an input-output coupling where physical and
   latent coordinates coincide (light/flux between layers? a wormhole/portal? a coupling kernel?).
D. SUBSTRATE-AS-LIGHT-ON-A-SENSOR: rendering-equation / splatting / camera-sensor models for
   projecting a fact-substrate into the space (Gaussian splatting? light transport? the Solomonoff/MDL
   render-in-log2 idea where appearance sharpness = bits of compression?).
E. The hyperdimensional container itself: how to honestly hold >3 dims and project to 3D/2D
   (hyperbolic/Poincare embeddings for the latent hierarchy? dimensionality-reduction? what keeps it
   from lying?).
F. The single most powerful, BUILDABLE (single-file HTML canvas, no heavy libs ideally) approach that
   delivers this, and the biggest risk.

DELIVER: name the real math + papers + implementations; sketch the architecture; recommend the
buildable approach; flag the honesty risks (this must never render a fake measured bit; estimates and
modelled positions must be badged). Spec-level, concrete. No code dump needed, but pseudo-math welcome.

codex
I’ll treat this as a spec/research pass only. I’m going to check a little local context first, then pull primary or implementation references for the map morph, layer coupling, and projection honesty pieces so the recommendation is grounded.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-ChildItem -Force' in D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'if (Get-Command rg -ErrorAction SilentlyContinue) { rg --files } else { Get-ChildItem -Recurse -File | ForEach-Object { $_.FullName } }' in D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec
 declined in 0ms:
`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'if (Get-Command rg -ErrorAction SilentlyContinue) { rg --files } else { Get-ChildItem -Recurse -File | ForEach-Object { $_.FullName } }'` rejected: blocked by policy
2026-06-14T13:17:58.997506Z ERROR codex_core::tools::router: error=`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'if (Get-Command rg -ErrorAction SilentlyContinue) { rg --files } else { Get-ChildItem -Recurse -File | ForEach-Object { $_.FullName } }'` rejected: blocked by policy
 succeeded in 1053ms:


    Directory: D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        14/06/2026     14:17              0 codex_take.md                                                        
-a----        14/06/2026     14:17              0 gemini_take.md                                                       
-a----        14/06/2026     14:16           4016 SPEC_BRIEF.txt                                                       


Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

codex
The local folder only has the brief plus empty take files, so I’ll use your prompt as source context and focus the rest on external math/implementation references.
web search: 
web search: d3-geo projection documentation geoMercator geoOrthographic projectionMutator
web search: 
web search: site:d3js.org/d3-geo d3 geo projectionMutator documentation
web search: 
web search: https://d3js.org/d3-geo
web search: 
web search: 'morphTo2D' in https://cesium.com/learn/cesiumjs/ref-doc/Scene.html
web search: 
web search: https://deck.gl/docs/api-reference/core/globe-view
web search: 
web search: https://d3js.org/d3-geo/projection
web search: 
web search: 'Extended geographic projections' in https://github.com/d3/d3-geo-projection
web search: 
web search: Snyder Map Projections A Working Manual USGS Professional Paper 1395 PDF
web search: 
web search: https://proj.org/en/stable/operations/projections/merc.html
web search: 
web search: 'Conformal azimuthal' in https://proj.org/en/stable/operations/projections/stere.html
web search: 
web search: https://proj.org/en/stable/operations/projections/stere.html
web search: 
web search: Maldacena The Large N limit superconformal field theories and supergravity arXiv holographic principle
web search: 
web search: Multilayer networks Kivela Arenas Barthelemy Gleeson Moreno Porter Journal of Complex Networks 2014
web search: 
web search: https://arxiv.org/abs/1309.7233
web search: 
web search: Robert Ghrist cellular sheaves of data arxiv
web search: 
web search: Kajiya rendering equation 1986 SIGGRAPH pdf
web search: 
web search: Kajiya The Rendering Equation 1986 pdf SIGGRAPH
web search: 
web search: https://dl.acm.org/doi/10.1145/15922.15902
web search: 
web search: pbrt v4 Rendering Equation online pbr-book
web search: 
web search: Poincare embeddings for learning hierarchical representations Nickel Kiela 2017 arXiv
web search: 
web search: Astronomy Engine JavaScript Sun Moon positions GitHub documentation
codex
**Core Recommendation**

Build this as **one canonical state space with multiple projections**, not as separate 3D and 2D scenes. Formalize it as:

`X = Earth(S²) × time × log2(scale/frame) × layer_id × latent_axes × provenance × uncertainty`

Then render through a view map:

`π_view(X) -> R³ or R²`

The dial changes `π_view`; it must not mutate the substrate.

**A. Globe To Map Dial**

Use a shared Earth mesh where every vertex has both:

`G(λ,φ) = sphere position`  
`U(λ,φ) = projected map position`

Then dial:

`P(t) = ease(t) * G(λ,φ) + (1 - ease(t)) * U(λ,φ)`

This is buildable and continuous. It is not a mathematically pure projection at intermediate states, so badge it as a **view morph**.

Important: a true no-cut sphere-to-rectangle unwrap is topologically impossible. A sphere and rectangle are not globally homeomorphic without a seam or singularity. Hide the seam in the Pacific, fade it, or use a two-atlas/zipper seam rather than pretending there is none.

Best projection candidates:

- **Mercator**: strongest fit to “LOG TRANSFORM / UV”. It is conformal and uses `y = ln tan(π/4 + φ/2)`; D3 documents exactly this formula, and PROJ documents the isometric-latitude form. Good for symbolic “log unwrap”, bad for polar area truth. Sources: D3 geo docs, PROJ Mercator.  
  https://d3js.org/d3-geo  
  https://proj.org/en/stable/operations/projections/merc.html

- **Stereographic / Riemann sphere**: best theoretical bridge. Sphere to complex plane, then complex log gives the Mercator/cylindrical relation. Use this in the spec language.

- **Lambert azimuthal equal-area / cylindrical equal-area**: best for event density honesty. If dots represent counts or “mass”, equal-area is safer than Mercator. PROJ supports Lambert azimuthal equal-area and cylindrical equal-area.  
  https://proj.org/en/stable/operations/projections/laea.html  
  https://proj.org/en/stable/operations/projections/cea.html

- **HEALPix / S2 / ISEA**: use for substrate binning, not necessarily visual display. Equal-area discrete cells are excellent for “sensor pixels”.

Implementation precedents:

- **d3-geo**: projections, spherical GeoJSON, clipping, antimeridian handling, adaptive resampling, custom projections.  
  https://d3js.org/d3-geo/projection

- **d3-geo-projection**: extended, interrupted, polyhedral, quincuncial projections.  
  https://github.com/d3/d3-geo-projection

- **CesiumJS**: direct precedent for 3D/2D scene morphing. It exposes `morphTime`, `morphTo2D`, `morphTo3D`, and map projection control.  
  https://cesium.com/learn/cesiumjs/ref-doc/Scene.html

- **deck.gl GlobeView**: useful reference, but note its own docs flag limitations when mixing globe/map views.  
  https://deck.gl/docs/api-reference/core/globe-view

**B. Layer / Membrane Stack**

The strongest honest model is **multiplex / multilayer networks** plus **fiber bundles / sheaves**.

Use:

- **Base space**: Earth/time/log-scale.
- **Fiber over each base coordinate**: physical state, latent state, provenance, certainty, route.
- **Layers**: membranes indexed by `layer_id`.
- **Couplings**: interlayer edges, not magical “energy” unless explicitly modelled.

Relevant theory:

- **Multilayer networks**: exactly models nodes repeated across layers with intra-layer and inter-layer links. Kivela et al. review the formal vocabulary.  
  https://arxiv.org/abs/1309.7233

- **Sheaves / cellular sheaves**: best for fact-substrate integrity. A sheaf lets local facts with provenance glue into global consistency only where compatible. Robinson explicitly argues sheaves are canonical for sensor integration.  
  https://arxiv.org/abs/1603.01446  
  https://arxiv.org/abs/1303.3255

- **Branes / bulk-boundary / holography**: powerful visual metaphor, but dangerous if overclaimed. Cite as inspiration only. Maldacena’s AdS/CFT and Randall-Sundrum brane-world models give the language of bulk, boundary, brane, coupling.  
  https://arxiv.org/abs/hep-th/9711200  
  https://arxiv.org/abs/hep-th/9906064

Represent `above / within / under` as **render policies**, not ontology:

- `above`: latent membrane offset outward from physical normal.
- `under`: latent membrane offset inward.
- `within`: latent drawn as embedded fields on the same membrane, e.g. contours, halos, tint, or noise texture.

Keep the canonical layer id unchanged.

**C. Overlap Equals Coupling**

Define coupling with a kernel:

`K(a,b) = exp(-d_geo²/σg² - d_time²/σt² - d_scale²/σs² - d_latent²/σl²) * confidence_a * confidence_b`

Render coupling as:

- luminous tube between layer copies,
- flux column through membranes,
- local ripple on both membranes,
- bidirectional particles if mutual,
- arrowed pulse if input-output direction is known.

Thickness = coupling weight.  
Opacity = certainty.  
Blur radius = uncertainty.  
Color = route/provenance.  
Animation speed = dated beat order.

Do not label this “energy” unless the substrate has a measured quantity. Use “coupling”, “influence”, “claim route”, or “modelled exchange”.

**D. Substrate As Light On Sensor**

This is a good metaphor if formalized as splatting:

`I(pixel) = Σ facts f  K(project(f), pixel) * radiance(f) * confidence(f) * visibility(f)`

Each fact emits a “radiance packet” into the view. The viewer’s camera/sensor integrates those packets.

Good references:

- **Rendering equation**: Kajiya 1986 is the canonical light-transport basis; use the idea of emitted plus reflected/integrated radiance, not literal physics.  
  https://en.wikipedia.org/wiki/Rendering_equation

- **3D Gaussian Splatting**: very close to “facts as light blobs projected onto a sensor”. Store each fact as Gaussian mean + covariance + opacity + color. Covariance becomes spatial/time/latent uncertainty.  
  https://arxiv.org/abs/2308.04079

- **MDL / Solomonoff / compression bits**: use only if computed. Sharpness can mean “compressive explanatory power”, but must be badged. Rissanen’s MDL and Solomonoff induction are the right lineage.  
  https://en.wikipedia.org/wiki/Minimum_description_length  
  https://en.wikipedia.org/wiki/Algorithmic_probability

Rule: never render an estimated bit as a measured bit. Use labels like `measured`, `reported`, `inferred`, `modelled`, `MDL-est.`.

**E. Holding More Than 3 Dimensions Honestly**

The viewer cannot literally show >3D. It can hold >3D in data and expose projections.

Use:

- **Hyperbolic / Poincare embeddings** for latent hierarchy or “local → civilizational reach”. Nickel and Kiela’s Poincare embeddings are the obvious citation.  
  https://arxiv.org/abs/1705.08039

- **UMAP / t-SNE / PCA** only as exploratory latent projections, never as ground truth geography. UMAP has a real manifold-learning theory, but output still depends on parameters and metric choice.  
  https://arxiv.org/abs/1802.03426

- **Distortion overlays**: Tissot indicatrices for map distortion; stress/trustworthiness badges for latent projections; uncertainty halos for modelled coordinates.

Every rendered point should carry metadata:

`source_fact_ids`  
`coordinate_basis`  
`projection_name`  
`projection_distortion`  
`certainty`  
`route/provenance`  
`measured_vs_modelled`

That is what keeps the viewer from lying.

**F. Most Buildable Approach**

For a single-file HTML canvas prototype:

1. Build a triangulated lat/lon sphere mesh, e.g. 96 × 48.
2. Give every vertex both sphere coordinates and Mercator or Lambert UV coordinates.
3. Dial-blend vertex positions between sphere and map.
4. Duplicate the mesh per layer with normal/screen offsets.
5. Render facts as Gaussian splats or soft circles using the same projection.
6. Render couplings as curved tubes/columns between duplicated layer positions.
7. Add camera orbit/zoom in 3D and pan/zoom in 2D.
8. Add Sun vector/day-night shading with approximate astronomy first; use SPICE/JPL or Astronomy Engine later if ephemeris accuracy matters. NASA SPICE/JPL ephemerides are the serious reference.  
   https://arxiv.org/abs/1507.04291

The biggest risk is not technical. It is **epistemic over-rendering**: the interface may make inferred latent couplings feel as real as measured locations and dates. The mitigation is mandatory badging, uncertainty glyphs, provenance inspection, and projection-distortion overlays. The viewer should feel powerful, but it must constantly reveal which parts are substrate facts and which parts are modelled projections.
2026-06-14T13:20:29.586554Z ERROR codex_core::session: failed to record rollout items: thread 019ec647-ee64-7820-a6d9-aad08f070c97 not found
tokens used
132,509
**Core Recommendation**

Build this as **one canonical state space with multiple projections**, not as separate 3D and 2D scenes. Formalize it as:

`X = Earth(S²) × time × log2(scale/frame) × layer_id × latent_axes × provenance × uncertainty`

Then render through a view map:

`π_view(X) -> R³ or R²`

The dial changes `π_view`; it must not mutate the substrate.

**A. Globe To Map Dial**

Use a shared Earth mesh where every vertex has both:

`G(λ,φ) = sphere position`  
`U(λ,φ) = projected map position`

Then dial:

`P(t) = ease(t) * G(λ,φ) + (1 - ease(t)) * U(λ,φ)`

This is buildable and continuous. It is not a mathematically pure projection at intermediate states, so badge it as a **view morph**.

Important: a true no-cut sphere-to-rectangle unwrap is topologically impossible. A sphere and rectangle are not globally homeomorphic without a seam or singularity. Hide the seam in the Pacific, fade it, or use a two-atlas/zipper seam rather than pretending there is none.

Best projection candidates:

- **Mercator**: strongest fit to “LOG TRANSFORM / UV”. It is conformal and uses `y = ln tan(π/4 + φ/2)`; D3 documents exactly this formula, and PROJ documents the isometric-latitude form. Good for symbolic “log unwrap”, bad for polar area truth. Sources: D3 geo docs, PROJ Mercator.  
  https://d3js.org/d3-geo  
  https://proj.org/en/stable/operations/projections/merc.html

- **Stereographic / Riemann sphere**: best theoretical bridge. Sphere to complex plane, then complex log gives the Mercator/cylindrical relation. Use this in the spec language.

- **Lambert azimuthal equal-area / cylindrical equal-area**: best for event density honesty. If dots represent counts or “mass”, equal-area is safer than Mercator. PROJ supports Lambert azimuthal equal-area and cylindrical equal-area.  
  https://proj.org/en/stable/operations/projections/laea.html  
  https://proj.org/en/stable/operations/projections/cea.html

- **HEALPix / S2 / ISEA**: use for substrate binning, not necessarily visual display. Equal-area discrete cells are excellent for “sensor pixels”.

Implementation precedents:

- **d3-geo**: projections, spherical GeoJSON, clipping, antimeridian handling, adaptive resampling, custom projections.  
  https://d3js.org/d3-geo/projection

- **d3-geo-projection**: extended, interrupted, polyhedral, quincuncial projections.  
  https://github.com/d3/d3-geo-projection

- **CesiumJS**: direct precedent for 3D/2D scene morphing. It exposes `morphTime`, `morphTo2D`, `morphTo3D`, and map projection control.  
  https://cesium.com/learn/cesiumjs/ref-doc/Scene.html

- **deck.gl GlobeView**: useful reference, but note its own docs flag limitations when mixing globe/map views.  
  https://deck.gl/docs/api-reference/core/globe-view

**B. Layer / Membrane Stack**

The strongest honest model is **multiplex / multilayer networks** plus **fiber bundles / sheaves**.

Use:

- **Base space**: Earth/time/log-scale.
- **Fiber over each base coordinate**: physical state, latent state, provenance, certainty, route.
- **Layers**: membranes indexed by `layer_id`.
- **Couplings**: interlayer edges, not magical “energy” unless explicitly modelled.

Relevant theory:

- **Multilayer networks**: exactly models nodes repeated across layers with intra-layer and inter-layer links. Kivela et al. review the formal vocabulary.  
  https://arxiv.org/abs/1309.7233

- **Sheaves / cellular sheaves**: best for fact-substrate integrity. A sheaf lets local facts with provenance glue into global consistency only where compatible. Robinson explicitly argues sheaves are canonical for sensor integration.  
  https://arxiv.org/abs/1603.01446  
  https://arxiv.org/abs/1303.3255

- **Branes / bulk-boundary / holography**: powerful visual metaphor, but dangerous if overclaimed. Cite as inspiration only. Maldacena’s AdS/CFT and Randall-Sundrum brane-world models give the language of bulk, boundary, brane, coupling.  
  https://arxiv.org/abs/hep-th/9711200  
  https://arxiv.org/abs/hep-th/9906064

Represent `above / within / under` as **render policies**, not ontology:

- `above`: latent membrane offset outward from physical normal.
- `under`: latent membrane offset inward.
- `within`: latent drawn as embedded fields on the same membrane, e.g. contours, halos, tint, or noise texture.

Keep the canonical layer id unchanged.

**C. Overlap Equals Coupling**

Define coupling with a kernel:

`K(a,b) = exp(-d_geo²/σg² - d_time²/σt² - d_scale²/σs² - d_latent²/σl²) * confidence_a * confidence_b`

Render coupling as:

- luminous tube between layer copies,
- flux column through membranes,
- local ripple on both membranes,
- bidirectional particles if mutual,
- arrowed pulse if input-output direction is known.

Thickness = coupling weight.  
Opacity = certainty.  
Blur radius = uncertainty.  
Color = route/provenance.  
Animation speed = dated beat order.

Do not label this “energy” unless the substrate has a measured quantity. Use “coupling”, “influence”, “claim route”, or “modelled exchange”.

**D. Substrate As Light On Sensor**

This is a good metaphor if formalized as splatting:

`I(pixel) = Σ facts f  K(project(f), pixel) * radiance(f) * confidence(f) * visibility(f)`

Each fact emits a “radiance packet” into the view. The viewer’s camera/sensor integrates those packets.

Good references:

- **Rendering equation**: Kajiya 1986 is the canonical light-transport basis; use the idea of emitted plus reflected/integrated radiance, not literal physics.  
  https://en.wikipedia.org/wiki/Rendering_equation

- **3D Gaussian Splatting**: very close to “facts as light blobs projected onto a sensor”. Store each fact as Gaussian mean + covariance + opacity + color. Covariance becomes spatial/time/latent uncertainty.  
  https://arxiv.org/abs/2308.04079

- **MDL / Solomonoff / compression bits**: use only if computed. Sharpness can mean “compressive explanatory power”, but must be badged. Rissanen’s MDL and Solomonoff induction are the right lineage.  
  https://en.wikipedia.org/wiki/Minimum_description_length  
  https://en.wikipedia.org/wiki/Algorithmic_probability

Rule: never render an estimated bit as a measured bit. Use labels like `measured`, `reported`, `inferred`, `modelled`, `MDL-est.`.

**E. Holding More Than 3 Dimensions Honestly**

The viewer cannot literally show >3D. It can hold >3D in data and expose projections.

Use:

- **Hyperbolic / Poincare embeddings** for latent hierarchy or “local → civilizational reach”. Nickel and Kiela’s Poincare embeddings are the obvious citation.  
  https://arxiv.org/abs/1705.08039

- **UMAP / t-SNE / PCA** only as exploratory latent projections, never as ground truth geography. UMAP has a real manifold-learning theory, but output still depends on parameters and metric choice.  
  https://arxiv.org/abs/1802.03426

- **Distortion overlays**: Tissot indicatrices for map distortion; stress/trustworthiness badges for latent projections; uncertainty halos for modelled coordinates.

Every rendered point should carry metadata:

`source_fact_ids`  
`coordinate_basis`  
`projection_name`  
`projection_distortion`  
`certainty`  
`route/provenance`  
`measured_vs_modelled`

That is what keeps the viewer from lying.

**F. Most Buildable Approach**

For a single-file HTML canvas prototype:

1. Build a triangulated lat/lon sphere mesh, e.g. 96 × 48.
2. Give every vertex both sphere coordinates and Mercator or Lambert UV coordinates.
3. Dial-blend vertex positions between sphere and map.
4. Duplicate the mesh per layer with normal/screen offsets.
5. Render facts as Gaussian splats or soft circles using the same projection.
6. Render couplings as curved tubes/columns between duplicated layer positions.
7. Add camera orbit/zoom in 3D and pan/zoom in 2D.
8. Add Sun vector/day-night shading with approximate astronomy first; use SPICE/JPL or Astronomy Engine later if ephemeris accuracy matters. NASA SPICE/JPL ephemerides are the serious reference.  
   https://arxiv.org/abs/1507.04291

The biggest risk is not technical. It is **epistemic over-rendering**: the interface may make inferred latent couplings feel as real as measured locations and dates. The mitigation is mandatory badging, uncertainty glyphs, provenance inspection, and projection-distortion overlays. The viewer should feel powerful, but it must constantly reveal which parts are substrate facts and which parts are modelled projections.
