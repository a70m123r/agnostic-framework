# What ARE the three families? — ontology exploration (Tier-3, exploration register)

> **Status:** exploration, 0 children, nothing locked — Pav intuition + unpacking, candidate sharper definitions, and three cheap audits that would test them. Not part of the protocol until ratified; `DIAL_PROTOCOL_SPEC.md` stands unedited by this file.
> **Pav (2026-06-12, verbatim sense):** *"frame is the sim of observer latent wrapper and plane, engine is the action space L0, viewer is an inference what the observer perceives — this is an intuition, lets explore, perhaps there's a sharper definition."*

## 1. Unpacking the intuition

- **Frame = the sim of (observer latent wrapper ⊕ plane).** The frame is not a neutral settings list — it is the observer's own running simulation of the world (their latent wrapper: kernel + membrane of what they know/mean), *restricted by the plane they stand on* (what is capturable from there — the observer_planes machinery). Frame dials are parameters of that composite.
- **Engine = the action space over L0.** Engine dials are not "calibration knobs" — they are the MOVES available against the framed thing: compress with this law, fit this predictive, code at this grain, hold out this way. Applying Kepler is an *action* on the data. Model-bits-counted = the action's price. The duel = action selection under cost.
- **Viewer = an inference of what the observer perceives.** The render is not presentation — it is a *derivation of the percept*: p(appearance | reading, observer). The viewer is literally the organ of the original coin steer — "not calculate but **derive the probability of what it looks like**" — sharp readings render as delta-percepts (replay), fuzzy readings as sampled fuzz (simulate). **The coin's two faces are viewer inference modes, gated by the engine's bits, over the frame's question.**

## 2. The sentence (candidate sharper definition, recommended)

**A sweep is one turn of an observer's perception–action loop:**
the **frame poses** (observer wrapper ⊕ plane → a question), the **engine acts** (an action from the L0 action space, priced in bits), the **viewer perceives** (infer p(appearance | reading) for that observer) — and **verification feeds the percept back into the wrapper's membranes**, so the next frame poses sharper.

Ask → act → see → harden → ask again. The dial protocol is then exactly: *the methodology for sweeping each component's parameters with the right attribution* — frame variance = world-relativity (signal), engine variance = action calibration (band), viewer variance = inference artifact (mirage candidate).

## 3. What the sharper definition dissolves and explains

1. **The observer-in-two-families wrinkle dissolves.** The observer was never a dial — the observer is the loop's *owner*. They appear twice because the loop passes through them twice: once posing (frame), once perceiving (viewer). Circuit topology, not ambiguity. (Spec §6's disambiguation becomes a corollary.)
2. **Questions live at the membrane.** If the frame is the observer's wrapper, the `inferred` is posed from its FUZZY region — you ask about what is fuzzy *to you*. The (framed, inferred) pair is the observer's membrane-frontier projected onto L0 — which is *why* hardness belongs to the pair, not the phenomenon: it is relative to the asker's wrapper state. (Curiosity = membrane pressure.)
3. **The conjecture engine = action-space expansion.** Minting a new law candidate literally grows the action space; a dial-jump is a policy improvement under fixed cost accounting; the history of science for a phenomenon = the growth trace of A. (FINDINGS S4 restated.)
4. **Mirages get a mechanism.** If the viewer is inference, render artifacts are *inference hallucinating*; the broken-weld law + wiggle test + never-render-fake-measured-bits are the **control** on the hallucination. The capture incident = the inference *occluding* (controlled too hard, the inverse failure).

## 4. Established anchors (disclosed honestly — the structure is not new; the binding is)

- **Active inference / free-energy principle (Friston):** perception–action loops minimizing surprise *in bits* — perception updates beliefs, action changes the world; the coin's replay/simulate = the two ways to be unsurprised. Our duel-in-bits is variational free energy in MDL clothing.
- **POMDP (belief, action space, observation model):** frame ≈ belief+query, engine ≈ A, viewer ≈ O. The three dial families are the three arguments of an agent.
- **Predictive processing — perception as "controlled hallucination" (Clark, Seth):** the viewer-as-inference IS this phrase; the framework's render discipline is the *controlled* part, named and enforced.
- **Gibson's affordances:** the action space is observer-relative — what L0 affords *from this plane*.
- **MDL/Solomonoff:** the shared currency across all three (already the §IT spine).

**Genuinely Pav's, on top:** binding these three roles to a provenance'd fact-substrate with the attribution rule as epistemics; the coin as the viewer's mode-switch; questions-from-the-membrane; and the whole loop running as an auditable sweep protocol rather than a metaphor.

## 5. Three cheap audits (the definition's first children — proposed, not run)

- **A1 — Frame-table bifurcation.** Prediction: if frame = wrapper ⊕ plane, every frame dial splits into *plane-side* (capture constraints: window, channel, cadence) or *wrapper-side* (meaning constraints: inferred, scale-rung-as-abstraction). First look: the spec §1.1 table splits cleanly (window/channel/cadence = plane; inferred/scale-rung = wrapper; observer = the owner, not a dial). A dial that refuses the split falsifies the decomposition or exposes a misfiled dial.
- **A2 — Render-dial castability.** Prediction: every render dial can be written as a parameter of p(percept | reading, observer). Any dial that CANNOT is misfiled (an engine dial in disguise). Audit target found already: the **mirage threshold** — if it only gates what is *shown* solid, it is render; if it changes what enters a compiled view, it is engine leaking into the viewer. Run the cast over the spec §1.4 table.
- **A3 — Dial-jump as policy improvement.** Prediction: across sweep history, law replacements (dial-jumps) are exactly the cells where held-out bits-per-action-cost improves — no jump should ever occur on a render or frame change alone. Testable on the sweep log as it accumulates.

## 6. On "sim"

Two readings, both load-bearing: **sim = simulation** (the frame is the observer's *running* generative model — favored by the active-inference reading, and it nests the coin: the observer's own wrapper has sharp and fuzzy regions, and they pose from the fuzzy edge) and **sim = sum/composition** (frame = wrapper ⊕ plane, the static composite). The protocol can stay agnostic: the composite is what the dials parameterize; whether it "runs" is the observer's business.

## 6b. Physical-instrument bounce (3 instruments, 2026-06-12)

Bouncing the frame/engine/viewer triple off real instruments to find where it clicks and where it strains.

| | **frame** (sim of wrapper ⊕ plane: what's asked) | **engine** (action space over L0: the moves, priced in bits) | **viewer** (infer the percept) |
|---|---|---|---|
| **Digital camera** | vantage + aim (plane), focal length/FOV, subject, the shot you intend (inferred) | exposure triangle, sensor, **ADC → bits literally**, optical low-pass filter, RAW capture | demosaic (Bayer = ⅔ of color is INFERRED), white balance, tone curve, sharpening, JPEG, the screen |
| **Radio telescope (EHT)** | where the dishes stand = an Earth-sized aperture (plane), baselines, frequency, the source | dishes+correlator → sparse samples of the Fourier/uv-plane, priced in SNR/coverage | CLEAN / regularized-ML reconstruction = p(image \| sparse visibilities, priors); M87 ring is ~99% inference |
| **Oscilloscope** | channel, **trigger** (what event you ask for), timebase, V/div | analog bandwidth + ADC sample-rate + bit depth; Nyquist lives here | dot-vs-vector display, **sin(x)/x interpolation** between samples, persistence grading |

**Three things the bounce confirms:**
1. **RAW vs JPEG = the four-tuple vs the baked view, exactly.** RAW keeps (frame, engine reading) and defers the render — re-derivable. JPEG bakes the render in, lossily — the percept overwrites the reading. The protocol's "save the four-tuple" is "shoot RAW."
2. **The percept is ALWAYS inference, even at the sharp end.** A normal photo is ⅔ interpolated color (Bayer demosaic). So viewer-as-inference is definitional, not just a fuzzy-end thing — the camera-end and telescope-end are the SAME viewer axis at different inference-ratios (a dial position, per the coin).
3. **The wiggle/mirage test is already how careful imaging science validates.** The EHT ran multiple INDEPENDENT reconstruction pipelines (different render-dial/prior settings) blind, and believed only features that survived all of them — "is the ring real or a hallucination of the priors?" answered the framework's way. The Samsung moon-photo scandal (a trained texture pasted onto blurry moons) is the canonical **broken-weld** violation shipped in a consumer product: rendered sharp what the sensor held fuzzy = never-render-fake-measured-bits, broken.

**What it TEACHES BACK (a category the protocol lacked): between-family artifacts.**
Oscilloscope **aliasing** (and its camera twin, **moiré**) is neither a render mirage nor frame-relativity — it is a **frame × engine MISMATCH**: the question is posed finer than the action can resolve (signal freq > ½ sample rate). The §2 attribution rule had three *within-family* variance meanings; this is a *between-family* artifact. The fix is itself a named dial — the **anti-alias / optical-low-pass filter** = deliberately blurring the frame to match the engine's resolving power. **Proposed addition to the protocol:** a fourth artifact class — *resolution mismatch* (frame asks finer than engine acts) — with the anti-alias dial as its control. The cosmic-coin analogue: asking next-MINUTE flux of a phenomenon whose lawful structure lives at 10-minute grain would alias; the quantization dial is partly an anti-alias control.

**Where the analogy STRAINS (the honest breakpoints):**
- **The camera is too clean.** Hardware-separated stages flatter the three-way split; in the framework the families are entangled (your wrapper informs which engine-action you'd even attempt). The camera over-sells separability.
- **Cross-family dials exist.** Aperture is an engine setting (light) whose depth-of-field effect isolates the subject (frame-like); focus selects the subject plane (frame) via an optical setting (engine-ish). This mirrors the observer-appears-twice wrinkle — some dials have cross-family effects, which is the interaction structure, not a flaw.
- **The camera observer is EXTERNAL** (photographer ≠ camera), but the framework's observer is partly CONSTITUTED by the frame (their wrapper IS the frame). The EHT is the better mirror here: the priors baked into the reconstruction ARE the observer's wrapper, so the percept is openly observer-relative.
- **Plane under-represented by the camera** (it captures one optical plane). The radio telescope captures a plane invisible to the eye — a cleaner illustration of plane = "what your instrument can even capture," closer to the physical/latent/straddle sense.

**§6c — The user steps into the analogy (Pav, same day): the agnostic-instrument user is the photographer, and the substrate is the light.**

The earlier breakpoint ("the camera's observer is external") is resolved by putting the user — **AI or person, interchangeably** — INSIDE the analogy as the loop-owner:

| photographer | agnostic-instrument user |
|---|---|
| repositions the camera, re-aims | moves the instrument across planes/topics (frame: plane-side) |
| **changes lenses** — wide-angle ↔ macro | **rides the abstraction ladder** — generic rung ↔ instance rung (frame: wrapper-side) |
| focuses; hunts focus by wiggling it | iterates `inferred` at the membrane frontier — "focusing on specific topics to gather data **to find focus**" |
| **autofocus = maximize edge-contrast** | **the duel = maximize bits-saved** — finding focus IS finding the law that sharpens the question |
| half-press to meter before the shot | a cheap probe sweep before the full grid |
| reads the print, adjusts, reshoots | infers the render, moves the dials, sweeps again — the perception-action loop |

And the substrate question answers itself in the same optics:

- **Internet sources = REFLECTED light.** Facts arrive as photons already bounced off the world — testimony-light, secondhand by construction. Primary sources sit closer to direct illumination; the **Wikipedia monoculture is a single lamp lighting the whole scene** — same-lamp glare = testimony laundering, and **cross-route corroboration = multiple independent illuminants** (you only trust a shape lit from two angles — sweep-2's provenance-disjoint rule, stated in optics).
- **`facts/*.jsonl` = the RAW file.** Undeveloped, never edited (append-only doctrine = RAW immutability), every photon carrying **EXIF** (source, retrieved_at, agent = exactly the provenance fields).
- **Corroboration = exposure stacking.** Multiple independent exposures of the same region stacked → noise cancels → the membrane hardens. Astrophotography's stacking discipline IS the verification state machine.
- **The compiler = the prism + development.** `compile_substrate.py` refracts the mixed fact-light into ordered spectra — per-specimen / per-pair compiled views are different spectral decompositions of the SAME light; deterministic development (same RAW → byte-identical negative = the compiler's idempotence). The viewer then **prints from negatives** — the percept-inference stage, where enlarger dials (render) live.

**Strains, disclosed:** (1) internet light is not passive reflection — sources are themselves observers/emitters; testimony can lie, photons cannot; (2) the prism implies lossless separation, but the compiler makes development choices (bucket precedence, best-value selection = a development curve — the compiler carries engine-ish dials of its own, worth an A2-style audit); (3) EXIF can be wrong — provenance is claimed, not guaranteed (the verification machinery exists precisely because of this).

**Degenerate check (the edge of the ontology): a mercury thermometer.** Viewer ≈ identity (the meniscus IS the reading, no inference), engine = one fixed move (thermal expansion, no dial), frame = where you place it. The three-way split collapses toward frame-only — and that is *correct*: a simple instrument is one with a 1-element action space and an identity viewer. The families are always present; they can degenerate. (A Geiger counter is the other edge — bottom-of-dial: the reading is irreducibly Poisson-fuzzy, no engine action sharpens it, the "lawfully random" anchor of FINDINGS S5 made physical.)

## 7. Footer

Exploration register; no protocol text changed; convergence list stays 9. If this hardens: fold §2's sentence into DIAL_PROTOCOL_SPEC §1 as the definitional preamble, run A1–A3 as the first children, and the cross-model external pass (GPT-5.5 + Gemini) on the active-inference correspondence specifically — it is the most import-laden claim here and exactly where an outside check earns its keep.
