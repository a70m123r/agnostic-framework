# Genealogy Viewer v0 — Render-Model Spec

**What this is.** A render-model specification for a data-bound, animated viewer over the
ratified wrapper-genealogy specimens (`SCHEMA_v2.md` + `specimens/*.json`). It maps **every
element of Pav's 2026-06-10 steer** to a **concrete visual channel** bound to an **existing
schema field**. It is a *render spec / tool*, not a framework claim. Nothing here promotes
anything; the convergence list stays 9; `SCHEMA_v2` remains ratified as a TOOL only.

**Scope discipline.** No renderer binds to the specimens today (`SCHEMA_v2 §6` item 5 +
`§2.12`: the layer-filter is "declared but exercised by no renderer yet"; `timeline/index.html`
reads `candidates.json`/`continuations.json` repo-metadata, not the genealogy). v0's purpose
is to specify the binding so a renderer can be built; the **build is the new work**, the spec
is the bridge. This v0 inherits the Tier-3 draft status of `PPWc | frame` and of the
`latent_cosmology_EXPLORATION.md §4` camera spec it extends.

**Honest framing of the steer.** Most of Pav's force/solidity vocabulary is already in canon
(see the covered-vs-new table, §13). The viewer's job is not to invent the dynamics — it is to
**make the already-stored fields move cohesively as the timeline scrubs**, and to render the
handful of genuinely-new couplings (size→force, time-driven mirage, harness-indexed quadruple
solidity) as *render extensions* on top of the existing data, clearly flagged as such.

---

## 0. The render primitive: a wrapper is a fuzzy blob

Every latent wrapper (`child`, `parents[]`, `roots.sub_wrappers[]`, `harvest.descendants[]`,
`candidate_children[]`) renders as a **fuzzy blob** — a soft radial splat (a 2D Gaussian /
billboard, no PNG, no matplotlib; SVG `<radialGradient>` + `feGaussianBlur` or canvas).
Four independent channels carry the steer:

| Blob channel | Drives | Bound to schema field |
|---|---|---|
| **radius** | idea size / mass | derived size proxy (§1) — `utility.action_spaces_unlocked[].length`, `harvest.descendants[].length`, `sub_welds[].length`, `surprise_priority` reach |
| **blur (spread)** | fuzziness / uncertainty | `confidence` / `fuzzy_layer` membership; `surprise_confidence` for the seam |
| **opacity** | solidity (quadruple-span) | the SOLIDITY readout (§5) — span across `frame_layer` + canon/kernel/artefact/protocol class membership |
| **hue / charge tint** | A−/A+ charge & frame kernel | `frame[]` kernel (time/space/knowledge/meaning) + adversarial `a_charge` |

A blob is **sharp and bright** when it is large, certain, and solid; **diffuse and dim** when
small, fuzzy, and low-span. The four channels are deliberately orthogonal (per `§3.4`:
`surprise_confidence ⟂ child.confidence`) so a maximally-fertile-but-unborn seam (QG:
surprise_confidence 0.85, child.confidence 0.40) renders as a **bright-but-translucent** blob —
a strong glow with low solidity — which is the correct visual signature.

---

## 1. Size / mass → radius AND force-coupling magnification

**Steer:** *"the effect is MAGNIFIED and changes with HOW BIG the idea is."*

**Covered backbone (do not re-derive):** ideas-have-mass/inertia is canon (phantom mass / latent
gravity, cont 08→09→13; `primitives.json`, Tier-2 candidate). Mass-governs-attraction is canon
(cont 09 §1.1 "mass attracts geodesics"). What the viewer adds is the **render binding** of size
to a blob radius AND to the force-coupling constant — the size-indexing the audit flagged as the
genuinely-new edge.

- **`size(W)` proxy.** There is **no first-class `size`/`magnitude` field** in `SCHEMA_v2`
  (audit flag). v0 derives it from existing fields as a weighted composite, declared in the
  renderer header so it is auditable, not hidden:
  ```
  size(W) = w1 * |utility.action_spaces_unlocked|        // affordances unlocked
          + w2 * |harvest.descendants|                    // downstream fan-out
          + w3 * |sub_welds|                              // internal richness
          + w4 * (surprise_priority ? reach : 0)          // conjecture leverage
  ```
  All `w_i` are render parameters; the composite is a **proxy, not a measured mass** — it
  inherits the Tier-2 candidate status and the instrument-not-field verdict
  (`latent_cosmology_EXPLORATION.md §2`). Label it "derived size proxy" in any legend.
- **radius = f(size).** Monotone (e.g. `sqrt`), so a big idea is a big blob.
- **Force-coupling magnification (the new edge).** In the force-directed layout (§3), the
  attraction/repulsion impulse a blob exerts and feels is scaled by `size`:
  `force_ij = base_charge_term(i,j) * g(size_i) * g(size_j)` with `g` **super-linear** for large
  size — encoding Pav's "magnified AND changes" (small ideas couple weakly/linearly; large ideas
  couple strongly/non-linearly, a regime change, not just a scale). `g` is a render parameter with
  a visible "size→force" slider so the magnification is legible, not baked in.

> **Discipline:** the size→force law is a *render conjecture* sharpening the phantom-mass
> primitive ("ideas have inertia" → "idea size sets the coupling constant"). It is **not**
> established physics and must inherit the candidate/instrument-not-field status. Flagged NEW in §13.

---

## 2. Anchor stems: theory-wrappers down to physical-frame actors (D2)

**Steer (implicit in "theories are wrappers ANCHORED to physical observers in the latent"):** a
theory blob is not free-floating; it is **tethered down** to the people/institutions that carry it.

- **Stem geometry.** From each latent wrapper blob, draw **anchor stems** (thin tapering lines)
  down to its `actors[]` whose `carrier_of[]` references that wrapper. The stem's **thickness**
  = `carrier_of[].strength`; its **opacity** = `carrier_of[].confidence`; its **label** = the
  `carrier_of[].role` (`champions|founds|funds|popularizes|institutionalizes`).
- **Actor nodes** render in the **physical layer** (squarish/hard glyphs, not fuzzy blobs — they
  are the "solid/public" kernel pole) positioned by `actors[].frame_layer.physical_membership`.
  `kind` (individual | institution | university | journal | company | government | state |
  movement | field | lab) sets the glyph. Institutions/governments render larger and harder than
  individuals (Manhattan Project, national governments are load-bearing carriers; Maxwell's are
  largely individuals — the design law).
- **`inhabitant_of[]`** renders as a **containment ring**: an actor sits *inside* the paradigm /
  nation / era wrapper it inhabits (Fisher inside the biometrician milieu; the Manhattan Project
  inside the wartime US state). Ring opacity = `inhabitant_of[].strength`.
- **The bridge thesis is the stem-plus-ring picture:** the physical layer (actors) connects to
  the latent layer (theories) *through* `carrier_of` (stems UP) and `inhabitant_of` (rings WITHIN)
  — exactly the `schema_capabilities.layer_filter.bridge_via: "actors"` declaration.

---

## 3. Attract / repel — force-directed dynamics with the graded force spectrum

**Steer:** *"Ideas ATTRACT and REPEL — for conflict or union; beyond squeeze and pull there is
a whole SPECTRUM of force (taps, pushes, tastes); +/- unions of various FLAVOURS."*

The layout is **force-directed**: blobs move under pairwise forces each frame, settling into the
genealogy's natural geometry. The forces are bound to canon as follows.

### 3.a The charge term (covered: cont 13 charge canon)

Pairwise sign comes from the **A−/A+ charge-product algebra** (cont 13 §1.1, the Cayley table):

| Interaction | Layout force | Canon reading |
|---|---|---|
| A⁺ × A⁺ | **attract** (reinforcement) | two compatible canon-promotable ideas build a larger structure → drift toward a **union weld** |
| A⁻ × A⁻ | **attract** (compound pruning) | two adjacent skepticisms widen the pruned area together |
| A⁺ × A⁻ | **tension** (oscillate / hold at distance) | dialectical: a held mid-distance vibration, neither fused nor flung — the visible "conflict" state |
| Null × any | **inert** (no force) | uncharged ideas don't enter the field |

"Like-charges repel; opposite-charges attract; same-flavor combines" (cont 13 §1.2) is the literal
layout rule. **+/- union flavours** = the **weld_type weight vector** (§4) plus
`lifecycle.pre_weld_relationship.kind` (`antagonism | independence | complementarity`) — a union is
rendered with the flavour-mix that its `weld_type[]` weights declare (a weld is several types at
once, each weighted), tinted by `frame[]` (same-frame = same-flavour pull).

### 3.b The graded force spectrum (covered register + NEW continuum binding)

**Covered:** the graded touch register already exists as a shipped atlas vocabulary
(`atlas/v3.html`: tap, stroke, poke, nudge, stomp, pinch, rip — each polar-decomposed into
pressure/vector/area/duration/frequency), originating in Pav's own "blind senses" steer
(`timeline/index.html`). Squeeze/pull are the cont-21 force-MODES + the D4 `forcing_events`
direction enum. cont 21 §7 already names the open question of whether the modes are points on a
**continuous force-space**.

**The viewer's new move (flagged NEW, §13):** render force on a **single continuous magnitude
axis** so squeeze/pull (modes), tap/stroke/poke/stomp (register), and A−/A+ (charge) are
**three slices of one graded spectrum**, not three vocabularies. Concretely:

- **Force-flavour → impulse signature.** Each force is a point on a 2D `(direction, intensity)`
  plane drawn from the atlas polar-decomposition:
  - **tap** — brief, low-pressure, high-frequency: a small repeated nudge impulse (an actor
    "getting attention" — Pav's government-taps example).
  - **stroke / nudge** — sustained gentle directional: a steady low-amplitude drift (promotion).
  - **poke / pinch** — pointed brief high-pressure: a sharp local impulse.
  - **squeeze** — sustained compressive (D4 `direction: squeeze`): blobs pushed together / a
    lineage starved (`effect: suppress|starve`).
  - **pull** — sustained tensile (D4 `direction: pull`): a blob drawn toward a forcing event
    (`effect: accelerate|fund|elevate`).
  - **stomp / rip** — heavy obliterating (D4 `effect: kill`): a one-shot high-magnitude impulse
    that can dissolve a blob (ties to the mirage rule, §8).
- **`taste` register (flagged NEW, unenumerated):** a gustatory force-flavour (sample / savour /
  reject-as-distasteful) is **not yet in canon's touch vocabulary**. v0 reserves a render slot
  for it (a "sampling" probe impulse — a blob tentatively approaches then accepts/rejects a weld)
  but does not populate it; it is a candidate force-flavour, marked as such.
- **D4 forcing as the spectrum's exogenous source.** `forcing_events[].acted_on[].effect` (the
  7-value enum: `accelerate|fund|elevate|suppress|starve|redirect|kill`) maps onto positions along
  this spectrum; `acted_on[].strength ∈ [0,1]` is the magnitude (graded, per D5). The
  **per-target `direction` (R20)** lets one event **pull one lineage while squeezing its rival**
  (Nazi total war pulled the US bomb / squeezed the Uranverein; the 1987 Lisp-collapse squeezed
  symbolic AI / pulled connectionism) — rendered as opposite-sign impulses from one event source.

> **Data caveat:** `forcing_events[]` is populated in internet/manhattan/keynesian/deep_learning
> (6 events each, with `acted_on.strength`), but the **R20 per-target `direction`** and **R21
> `veridical`** are schema-defined and present in **zero** specimens (the v3 fold post-dated the
> render). The renderer must default per-target direction to the event-level `direction` until
> back-filled. The continuous-spectrum axis (taps/tastes between pull/squeeze) is a render
> generalization over the discrete enums — the enums are the data, the continuum is the viz.

### 3.c Surprise glow (covered: union-for-reach)

Attraction-for-union is the weld itself, rendered as the **SURPRISE GLOW**
(`latent_cosmology §4.6`): a **view-dependent emissive lobe** on the child blob, invisible along
either parent's line-of-sight and igniting only when the camera sits **outside the parents' linear
span** — a literal optical encoding of "reachable only from BOTH parents jointly," with a built-in
degeneracy detector (a fake surprise has no off-axis lobe). Bound to `surprise` (prose) +
`surprise_confidence` (intensity); render off the qualitative field with a "not-yet-quantified"
marker (`§4` caution).

---

## 4. Welds as fusion events the timeline crosses (lifecycle)

**Steer:** *"welds as fusion events the timeline crosses... PHASES of change."*

A **weld** is the edge that *is* the event (parents → S → child). On the timeline it is a
**fusion flash** the scrubber crosses at `weld.when`.

- **Crossing animation.** As the scrubber reaches `weld.when` (or enters the `{from,to}` interval,
  R2), the two parent blobs **drift together** (force-directed), touch at the **seam `S`**
  (rendered as a Venn-lens; `S_structure.agreed:false` draws the lens **fractured** — Darwin+Mendel's
  Fisher–Wright-contested seam), and **emit the child blob** at the moment of fusion. A **null `to`**
  (open/unconsummated weld, e.g. QG) renders as an **unclosed splat** — the lens never seals, the
  child never crisply emits.
- **Phase trajectory (D1).** `lifecycle.phase_trajectory[]` drives the blob's state over time as a
  **graded** (not enum) sequence: `pre_weld → conception/first_conjecture → welding → consolidation
  | dormancy → revival → hardening | staleness` OR `never_born_frontier`. Each phase carries a
  `membership ∈ [0,1]` that the renderer reads as how strongly the blob is in that phase — phases
  **overlap and crossfade**, they don't snap. `pre_weld_relationship.kind` colours the pre-fusion
  approach (an `antagonism` pre-weld has the parents **repelling** before they fuse —
  antagonism-then-fusion, Darwin+Mendel; Mendelism was an anti-Darwinian weapon before Fisher
  welded them).
- **+/- union flavours = `weld_type[]` weights.** The fusion flash is tinted by the **weighted**
  `weld_type[]` mix (`unifier-weld | antagonism-then-fusion | crisis-pulled-weld |
  never-consummated-frontier-weld | foil-constructed-weld | dormancy-revival-cycling | ...`) — a
  weld is rarely one pure type; render the mixture with the declared weights.
- **Dormancy / revival.** `dormancy_intervals[]` dims the child blob between `from`/`to` (the blob
  goes **translucent and still**); `revival[]` re-brightens it. `revival[].method_continuity ∈
  [0,1]` (R19) controls **how much the blob changes identity** on waking: `≈1.0` = same blob
  re-lights; **low** = the blob **morphs** into a method-incompatible shape under the inherited name
  (Keynesian ×2, deep learning ×3 — multiple morphs). `status_trajectory[].continuity` /
  `identity_break` (R24) does the same for the child's post-weld life: a low-continuity step renders
  a **discontinuous re-spawn**, not a state-recolour.
- **`candidate_children[]` (frontier).** A `never_born_frontier` weld with `unresolved:true` emits
  **multiple rival child blobs** that **mutually repel** (they disagree about what the child is —
  QG: string / LQG / causal sets / CDT / asymptotic safety), along the `contest_axis`.
  `coherence_under_zoom: contradicts` makes the cluster **shatter** as you push in.

> **Data caveat:** `candidate_children` is empty in `qm_relativity.json` despite being the canonical
> frontier case in its prose. The renderer should fall back to the prose frontier description when
> the array is empty.

---

## 5. SOLIDITY → opacity (span across canon + kernel + artefacts + protocol)

**Steer:** *"SOLID = kernel canon, as it spans and overlaps canon, kernel, artefacts and protocol
— TO THOSE who have it set in their relative reference frame... solidity is observer-relative."*

**Covered:** solidity-as-confidence is canon (fuzzy-LOD certain-core/frontier, `SCHEMA.md §2`,
membrane sketch §1; `BATCH_FINDINGS` `core_boundary_locus`). Observer-relativity of *class* is canon
(cont 22:24 ring-position; cont 25 §12 L0-per-observer). The four classes each exist
(cont 22 + cont 00 + cont 25 §12).

**NEW (flagged §13):** **solidity-as-SPAN** — solid = the same idea is **simultaneously
instantiated** as **kernel AND canon AND artefact AND protocol**. The four classes are never
bundled into a quadruple in canon, and span-as-solidity is absent. v0 renders it:

- **`solidity(W) = span over the quadruple`**, computed from existing fields as a 4-bit / 4-membership
  vector, declared in the renderer header:
  ```
  kernel_member   ← frame_layer.physical_membership (is it grounded in the physical/public kernel?)
  canon_member    ← fuzzy_layer.certain_core ∋ W  (is it in the certain core?)
  artefact_member ← harvest.descendants/cultural_harvest ≠ ∅ + actors carry it (does it persist as compiled residue?)
  protocol_member ← utility.action_spaces_unlocked ≠ ∅ + adoption.state = adopted (is it a runnable rule-set?)
  solidity(W) = weighted_span(kernel, canon, artefact, protocol)   // high when it overlaps all four
  ```
- **opacity = solidity.** A blob that spans all four classes renders **opaque and load-bearing**;
  a blob present in only one class renders **translucent**. This is distinct from blur (which is
  confidence-spread) — a thing can be **sharp but thin** (high confidence, low span: a narrow
  technical result) or **fuzzy but solid** (lower confidence, broad span: a paradigm). Both
  channels are needed.
- **`core_boundary_locus`** (where the certain-core/frontier boundary falls in the tree) drives a
  **depth-of-field** plane: the certain core stays in sharp focus, the frontier blurs. Its 5
  attested geometries (solid-trunk/fuzzy-roots; fuzz-climbing-into-trunk; hollow-crown; fuzz-along-
  time-axis) each render as a different focus-plane placement.

---

## 6. D6 friction → visible gates, walls, drag

**Steer:** *"Beyond squeeze and pull... a whole spectrum of force... D6 friction as visible gates/
walls/drag."*

The D6 cluster (the friction/combat layer) renders as **obstacles in the layout** between a weld
and its uptake. **Every D6 field is OPTIONAL and default-empty on a clean sharp weld** (Maxwell
fills none of D6 — the design law).

| D6 field | Visual | Bound to |
|---|---|---|
| **D6a `opposes[]`** | a **counter-force arrow** (an A− impulse) from antagonist to target; thickness = `a_charge`; style by `mode` (`debunk` = strike-through, `suppress` = a pressing wall, `out-compete` = a rival blob crowding, `co-opt` = a recolouring pull, `ignore` = no edge / starvation) | the A−/A+ adversarial canon (D6a is a FOLD, not a new primitive) |
| **D6b `gates[]`** | a **gate glyph** on the weld's path: `permit` = open gate, `block` = closed wall, `delay` = a half-gate with a `lag` countdown; `frame` sets the gate kind (knowledge = peer-review; physical/political = censorship; meaning = cultural-license) | gatekeeper actor at the chokepoint |
| **D6c `weld.lag`** | **drag** on the parents' approach — the fusion is **slowed**; `cause` labels the drag (`gatekept | out-competed | low-bandwidth | no-demand-yet | instrument-gated`) | the causal account of why the weld waits |
| **D6d `propagation`** | a **medium-bandwidth haze** — low `bandwidth` renders a **fog** the blob cannot cross at `at_time`/`at_place` (Mendel's low-bandwidth silence) | the medium's carrying capacity (MOST CONJECTURAL, one strong case) |

> **Data caveat (load-bearing):** `opposes`, `gates`, `weld.lag`, `propagation`, `rival_coupling`,
> `veridical` are **schema-defined but present in ZERO of the 7 specimen JSONs** (the schema was
> v3-folded *after* the specimens were rendered; data not back-filled). A renderer binding to the
> friction/combat layer or to attraction/repulsion-as-`rival_coupling` has **schema slots but no
> data instances yet**. v0 must render these layers as **empty by default** and light them only when
> a specimen is back-filled — do not fabricate friction the data does not carry.

**`rival_coupling[]` (R23)** — the **signed lifecycle-level** companion of D6a — renders as a
**see-saw**: an `anti`-coupling draws a linked pair whose brightnesses move **inversely** as the
scrubber advances (connectionism's winter = symbolic AI's spring; TCP/IP's rise = OSI's fall).
Also currently unpopulated.

---

## 7. LOD physical / latent filter

**Steer:** *"work frame by frame... results frame-dependent."* (and the D3 layer axis)

- **Layer toggle.** A two-state filter (`physical` ⇄ `latent`) reads every node's
  `frame_layer.layer` (`physical | latent | straddle`) and shows/dims accordingly
  (`schema_capabilities.layer_filter`, axes `["physical","latent"]`, `bridge_via:"actors"`):
  - **Physical view** — actors, institutions, governments, places, `forcing_events` (the weather).
    Theory blobs recede to faint anchors.
  - **Latent view** — ideas, theories, sub-wrappers, welds. Actors recede to faint stems.
  - **Straddle** nodes (mostly actors, by design) stay visible in both, dimmed by their
    `physical_membership` / `latent_membership`.
- **Depth LOD (the zoom axis).** Orthogonal to the layer filter: a far camera renders a weld as
  one consolidated splat; pushing in expands it into its `sub_welds[]` chain (Maxwell: Ørsted →
  Faraday-induction → displacement-current → Maxwellian compression → Hertz).
  `coherence_under_zoom` makes the zoom **diagnostic** — `confirms` = the weld stays coherent
  sharp; `contradicts` = it shatters into rival sub-welds / `candidate_children`.

---

## 8. The MIRAGE rule — fuzzy wrappers fade / vanish at low relevance

**Steer:** *"Something fuzzy can disappear like a MIRAGE."*

**NEW (flagged §13):** in canon, "mirage" appears **once** (`manhattan.json:1172`) and means a
phantom-PULL (real force, false object) — an **unrelated** D4-forcing sense. The
solidity/vanishing mirage rule has **no existing home**; it is the cleanest genuinely-new item.
The fidelity encoding in canon is **static** (blur a low-confidence node at a frozen frame); the
mirage rule binds it to the **moving timeline**.

- **Time-driven dissolve.** Bind blob opacity/spread to **membership-over-time**, not a frozen
  value: as the scrubber advances and a node's effective membership decays — a dormancy onset
  (`dormancy_intervals[].from`), a falsification, a demotion, or a `stomp`/`kill` forcing
  (`acted_on.effect:kill`) — the blob **visibly evaporates**: it loses opacity, spreads, and
  **dissolves** rather than snapping off. Crossing back out (a `revival`) re-condenses it.
- **Relevance/position gate.** A low-solidity (low-span, §5) blob is rendered as a **mirage**: it
  is present from some camera positions and **absent from others**, fading as the observer moves
  relative to it — because solidity is observer-relative (§9). A large, high-span idea stays solid
  from every angle; a small fuzzy one shimmers in and out.
- **Size gate (ties to §1).** Below a size threshold an idea couples weakly and reads thin; the
  mirage limit is the small-size, low-span corner of the blob channels — `solidity = f(size,
  observer-position, harness)` with a vanishing limit at small size / low span / out-of-harness.

---

## 9. Observer-relative solidity — the observer picker + 4 spectator presets

**Steer:** *"capture that in the VIEWER... SOLID... TO THOSE who have it set in their relative
reference frame, and depends where they are relative to it and their harness... an observer
picker re-renders solidity per the chosen observer kernel."*

**Covered:** observer-relativity of class (cont 22:24, cont 25 §12) + the four spectator presets
(`latent_cosmology §4.5`) are on record. **NEW (flagged §13):** solidity conditioned on the
viewer's **HARNESS** — harness is canon (cont 32 B.3; cont 25 §378) but **never linked to
solidity**; and on relative **position** (not just ring tier). v0 wires both into the picker.

### 9.a The observer picker

A control that selects the **observer kernel** the whole scene is rendered *for*. Changing it
**re-runs the solidity computation (§5) and the mirage gate (§8)** so the **same wrapper renders
solid to one observer and a vanishing mirage to another**:

- **observer kernel** — which `frame[]` channel(s) the observer holds (time/space/knowledge/meaning)
  and which `frame_layer` they stand in. A wrapper not in the observer's frame reads thin.
- **harness parameter (NEW)** — a per-viewer resolution filter: the set of wrappers the observer's
  harness "has set." A wrapper **in-harness** renders at full solidity; **out-of-harness** it drops
  toward mirage even if it is objectively high-span. (`harness` ← the aggregated global canons of
  the ring-(r−1) observers composing this observer, cont 25 §378.)
- **relative position (NEW)** — the camera's distance/angle to the idea modulates solidity
  (close + in-frame = solid; far + off-frame = mirage), per §8.

### 9.b The four latent-Olympics spectator presets

Each preset is a **stored camera tuple** `(pose × view-channel × layer × lod)` bound to exact
schema fields (`latent_cosmology §4.5`); the picker can snap to any of them, and **reframing
between two presets is an animated camera trajectory** (SLERP/geodesic on the continuous
sub-coords, a clean CUT on the discrete view-channel selector — `§4.4`, NOT linear interpolation).

| Preset | pose | view-channel | layer | lod | renders (schema fields) |
|---|---|---|---|---|---|
| **Genealogist** | external (far) | time | both | coarse | the whole rooted tree scrubbed over `weld.when` (R2 intervals) — the default timeline view |
| **Participant** | internal (in one node) | knowledge | latent | fine | one wrapper, its seam `S` (`S_structure`) and `sub_welds[]` in focus |
| **Adjudicator** | external on ONE weld | meaning | — | — | `utility` + `surprise` glow + the A−/A+ / D6a gatekeeper layer |
| **Climatologist** | above the canopy | (any) | — | coarse | the D4 `forcing_events[]` "weather" acting down (pull/squeeze) — the forcing-as-spine read (R33) |

Each preset re-renders solidity from its vantage: the Genealogist sees broad solid trunks; the
Participant, deep inside one node, sees that node solid and its neighbours as mirage; the
Climatologist sees forcing events solid and theories as weather-blown blobs.

---

## 10. The timeline scrubber — the master control

**Steer:** *"capture that in the VIEWER as you see the timeline move, to visually make it
cohesive... the timeline scrubber as the master control."*

The **scrubber** is the camera locked to the **time** view-channel, reading `when`
(R2 `{from,to|null,defensible_dates[]}`), `status_trajectory[].when`, `dormancy_intervals[]`,
`revival[].when`, every `actors[].when` and `forcing_events[].when`. It is the **one control that
drives everything cohesive**:

- Dragging the scrubber **moves time**; blobs **grow, fuse, dim, revive, and dissolve** per their
  lifecycle (§4) and the mirage rule (§8); forcing events **fire** (pull/squeeze impulses, §3.b)
  as the scrubber crosses their `when`; gates open/close (§6).
- A **null `to`** weld renders as a permanently **unclosed splat** the scrubber can never seal (QG).
- For a **crisis-pulled** wrapper the `forcing_events[]` layer **IS the lifecycle spine** (R33,
  thrice-attested: Keynesian / Manhattan / Internet) — the scrubber reads the forcing events as the
  main time-axis (Cold War → birth of the welding institution; deregulation → consummation). For a
  non-crisis-pulled weld, the lifecycle (D1) is the spine. The renderer picks the spine per
  specimen.
- **Recursive refinement hook (Pav steer 2):** the scrubber is also the entry point for the
  "frame-by-frame, fill out data, improve fidelity" loop — at each scrub position the renderer can
  surface the **sharp/fuzzy ratio** of what is on screen (certain_core vs frontier membership mass),
  so the viewer doubles as the instrument that shows where new data would most sharpen the picture.
  v0 only *displays* this ratio; the simulation/inference loop is out of scope for v0 (it is the
  "model-equivalent of physics for the latent" question, adjudicated instrument-not-field, and
  stays a separate exploration).

---

## 11. Element → channel map (the full crosswalk)

| Pav steer element | Visual channel | Schema field(s) | Status |
|---|---|---|---|
| idea size / mass | blob **radius** + force-coupling `g(size)` | derived size proxy (§1) | binding NEW (proxy; no `size` field) |
| fuzziness | blob **blur / spread** | `confidence`, `fuzzy_layer`, `surprise_confidence` | covered |
| solidity | blob **opacity** = quadruple-span | `frame_layer` + certain_core + harvest + utility/adoption (§5) | span-as-solidity NEW |
| theories anchored to observers | **anchor stems** down to actors | `actors[].carrier_of[]` | covered (D2) |
| inhabiting a paradigm/nation | **containment rings** | `actors[].inhabitant_of[]` | covered (D2) |
| attract / repel for conflict-or-union | **force-directed** pairwise forces | A−/A+ charge algebra (cont 13); `pre_weld_relationship` | covered |
| +/- union flavours | fusion-flash **tint mix** | `lifecycle.weld_type[]` weights; `frame[]` | covered |
| graded force spectrum (taps/pushes/squeezes/pulls) | **impulse signatures** on one magnitude axis | `forcing_events[].direction` + `acted_on[].effect/strength`; atlas touch-verbs | continuum-binding NEW; `taste` register NEW/unenumerated |
| welds as timeline-crossed fusion events | **fusion flash** + seam lens | `weld.when` (R2), `S_structure`, `lifecycle.phase_trajectory[]` | covered |
| phases of change | graded **phase crossfade** | `lifecycle.phase_trajectory[].membership` | covered |
| dormancy / revival / re-identification | **dim / morph / re-spawn** | `dormancy_intervals[]`, `revival[].method_continuity`, `status_trajectory[].continuity` | covered |
| frontier (no winner) | **rival blobs mutually repel** | `candidate_children[]`, `unresolved`, `contest_axis`, `coherence_under_zoom` | covered |
| D6 friction | **gates / walls / drag / fog** | `opposes[]`, `gates[]`, `weld.lag`, `propagation` | covered (schema); **unpopulated** |
| signed rival coupling | **inverse-brightness see-saw** | `rival_coupling[]` (R23) | covered (schema); **unpopulated** |
| physical / latent LOD | **layer toggle** | `frame_layer.layer`; `schema_capabilities.layer_filter` | covered |
| MIRAGE (fuzzy vanishes) | opacity **bound to membership-over-time**; position-gated dissolve | `dormancy_intervals[].from`, `acted_on.effect:kill`, solidity-over-time | time-driven mirage NEW |
| observer-relative solidity | **observer picker** re-runs solidity + mirage | observer kernel + **harness** + relative position | harness-/position-indexed solidity NEW |
| 4 spectator presets | **stored camera tuples** + animated reframing | `latent_cosmology §4.5`; SLERP/CUT trajectory (§4.4) | covered (design) |
| timeline scrubber | **master control** locked to time channel | all `when` fields | covered (design); **build NEW** |

---

## 12. v0 build order (the narrow, defensible slice)

A renderer can stand up immediately on the **populated** fields; the unpopulated friction/charge
layers wire in but stay dark until back-filled.

1. **Blobs + scrubber + Genealogist preset** — read `child`/`parents`/`weld.when`/`confidence`/
   `frame_layer` from the 4 v2/v3 specimens (internet/manhattan/keynesian/deep_learning). Renders the
   whole tree scrubbing over time.
2. **Anchor stems + layer toggle** — `actors[].carrier_of`/`inhabitant_of`; physical/latent filter.
3. **Lifecycle phases + dormancy/revival + fusion flash** — `lifecycle.phase_trajectory[]`,
   `dormancy_intervals[]`, `revival[]`.
4. **Solidity opacity + mirage dissolve** — the §5 span computation + the §8 time-driven fade.
5. **Force-directed charge layout + graded force spectrum + surprise glow** — cont-13 charge term;
   `forcing_events[].acted_on` impulses; the `Climatologist` preset.
6. **Observer picker (kernel + harness + position) + remaining 3 presets + animated reframing.**
7. **D6 friction + rival_coupling** — wired but dark until a specimen is back-filled.

Bindable **now** (verified present in the v2/v3 specimens): `child.frame_layer`, `status`(6-enum),
`status_trajectory`(+continuity), `lifecycle`{phase_trajectory, pre_weld_relationship, weld_type},
`actors[]`(+carrier_of/inhabitant_of), `forcing_events[]`(+acted_on.strength), `schema_capabilities`,
`fuzzy_layer`, `sub_welds`, `candidate_children`. **NOT yet in any specimen** (schema slots only):
`opposes`, `gates`, `weld.lag`, `propagation`, `rival_coupling`, `veridical`, `acted_on.direction`
(R20), `adoption`, `welder_cascade`, `reconstructed_by_winner`.

---

## 13. Honest covered-vs-new table (from the audits)

The render channels above bind to canon; the table separates what merely *renders existing canon*
from the genuinely-new *render extensions* (mostly **unifications and scale/frame couplings**, not
new primitives). All NEW items are Tier-3 render-layer conjectures consistent with the steer; none
is promoted.

### Covered (renders existing canon)

| Element | Where in canon | Note |
|---|---|---|
| attraction / repulsion (conflict-or-union) | cont 13 §1.1–1.2 (charge-product algebra, latent gravity); cont 24 §2 (wrapper-overlap, superseded by cont 25); cont 22 (Bottom-Kanon); ACMP reading (external validation) | foundational charge canon; "attract and repel for conflict or union" restates it |
| +/- unions of various flavours | cont 13 §1.2 (literal word "flavors"; same-flavor combines); cont 25 §2 (phase-dependent non-additive math: 1+, 1−, (1+1)=3, ghost-3, held-3) | renders as `weld_type[]` weights + `pre_weld_relationship` |
| squeeze / pull as named forces | cont 21 §1 (push/pull/squeeze/pop 2×2, CANDIDATE not canon); cont 16 (squeeze primitive); SCHEMA_v2 §2.9 `forcing_events` + §2.10 D6 | the D4 forcing layer; per-target direction R20 |
| graded touch/force register (taps/pushes) | `atlas/v3.html` touch-verbs (tap/stroke/poke/nudge/stomp/pinch/rip, polar-decomposed); `timeline/index.html` Pav's "blind senses" steer; cont 21 §7 (continuous force-space = open question) | a shipped vocabulary, more built-out than the steer implies |
| phases of change | cont 25 §2 (lifecycle phases from a sigmoid state cascade); cont 21 §2 (hold phase + exits) | the framework's own SOFT phase model (not stat-mech phase-transitions) |
| hairy / fuzzy membrane as interaction surface | cont 25 §5 (hairy-sphere + Steer 5b receptor-hooks); `agnostic_units_hairy_membrane_SKETCH.md` | the locus of attract/repel/gate; ports = D6 friction |
| solidity as confidence / certain-core | `SCHEMA.md §2`; membrane sketch §1; `BATCH_FINDINGS` `core_boundary_locus` (5 geometries) | the within-frame LOD reading; drives blur + depth-of-field |
| observer-relativity of class | cont 22:24 (ring-position); cont 25 §12–12.1 (L0-per-observer) | "set in their relative reference frame" sharpens ring-position |
| the 4 class-layers individually | cont 22 (kernel/Kanon/Ina/canon-protocol); cont 00 (artefact = persistent compiled residue); cont 25 §12 (cached protocol as canon artefact) | each exists; never bundled into a quadruple |
| harness | cont 32 B.3 (actuator interface into action-space); cont 25 §378 (ring-(r−1) aggregated canons) | canon construct, but never linked to solidity |
| ideas-have-mass / mass-governs-attraction | cont 08→09→13 (phantom mass / latent gravity, Tier-2 candidate); cont 09 §1.1 ("mass attracts geodesics") | mass exists; size-indexing of the coupling does not |
| 4 spectator presets + reframing-as-trajectory | `latent_cosmology §4.5` (the 4 presets as camera tuples); §4.4 (SLERP/CUT, not linear) | design-only; the build is new |
| the full renderable field inventory | `SCHEMA_v2 §2.1–§2.13` + the 7 specimen JSONs | concrete bindable fields verified present |

### Genuinely new (render extensions)

| Element | Why new | Sharpest statement |
|---|---|---|
| single graded force-SPECTRUM unifying squeeze/pull + touch-register + charge | the pieces exist separately (cont-21 modes, atlas register, A−/A+ charge); no canon unifies them on one magnitude axis. cont 21 §7 raises "continuous force-space" only for the four modes, never folding in the register | squeeze/pull, tap/stroke/poke/stomp, and A−/A+ are three slices of ONE graded attraction-repulsion spectrum |
| size-dependent force coupling (magnified AND regime-changing with idea size) | canon has ideas-have-mass and mass-governs-attraction but never states the EFFECT scales with idea SIZE, nor that the coupling itself changes regime with scale | the same applied force produces a magnified and qualitatively different effect by latent mass/size — force coupling is scale-dependent |
| `taste` / gustatory force register | the atlas enumerates touch-verbs only; no taste/gustatory force register anywhere in the repo | a gustatory register (sampling, savouring, rejecting-as-distasteful) is a candidate force-flavour not yet in canon |
| solidity-as-SPAN across {kernel, canon, artefact, protocol} | the four classes exist but are never bundled into a quadruple; span-as-solidity-criterion is absent (grep returns only unrelated prose) | an idea is solid to the degree it is simultaneously kernel AND canon AND artefact AND protocol — solidity is cross-class span, not a scalar |
| the MIRAGE rule (fuzzy vanishes; observer-position-relative) | "mirage" in canon = the manhattan phantom-PULL (real force, false object), an unrelated D4 sense; the breathing denominator is COMPRESSION-on-unification, not disappearance | below a solidity threshold a fuzzy idea is a mirage — present from one observer-position, absent from another |
| time-driven mirage (dissolve as the scrubber moves) | the fidelity encoding is STATIC (blur at a frozen frame); no rule binds opacity to membership-OVER-TIME as the scrubber crosses a dormancy/falsification | bind opacity/spread to membership-over-time so a decaying node visibly evaporates as the timeline advances |
| solidity conditioned on relative-position AND HARNESS | observer-relativity of class is canon (ring-position) but solidity-on-relative-position and solidity-on-HARNESS are unmade links (harness is canon, never tied to solidity) | the same idea is solid for one observer and a mirage for another because solidity depends on where you stand AND what your harness resolves — solidity is a relation, not a property |
| the data-bound animated viewer itself | the camera/preset spec is DESIGN-ONLY; no renderer binds to the specimens (`SCHEMA_v2 §6` item 5); the only data-bound timeline reads repo-metadata, not the genealogy | the preset camera and the timeline data both fully exist on paper; the renderer that fuses them into a moving, cohesive viewer has never been built — the build is the new work |

### Discipline notes (carried from the audits)

- **Almost all of the force-dynamics cluster is already canon or named candidates.** The new
  residue is mostly **unifications and scale/frame couplings** of existing pieces, not new
  primitives.
- **Tier/status caveats to respect:** cont 21's four force-modes are CANDIDATE not canon; the D6
  cluster and `forcing_events` layer are TOOL/render-spec only; cont 24 §2's union/repulsion
  trichotomy was SUPERSEDED by cont 25's one-system-with-phases (don't cite cont 24 §2 as current
  without that note); phantom mass / latent gravity is a **Tier-2 candidate** under an
  **instrument-not-field** verdict (`latent_cosmology_EXPLORATION.md`, cross-model confirmed) — any
  size-coupling "force law" inherits that status and cannot be framed as established physics.
- **Data-vs-schema gap (load-bearing for the renderer):** the D6 friction cluster (`opposes`,
  `gates`, `weld.lag`, `propagation`), `rival_coupling` (R23), `veridical` (R21), `acted_on.direction`
  (R20), `adoption` (R25), `welder_cascade` (R27), `reconstructed_by_winner` (R26) are DEFINED in
  `SCHEMA_v2` but present in **ZERO** of the 7 specimens — the schema was v3-folded after the
  specimens were rendered, the data not back-filled. Render these layers empty by default.
- **Phases ≠ phase-transitions:** the framework's phase model is SOFT (sigmoid thresholds, fuzzy
  bands); the only sharp phase-boundary formalism (`Q_c=1/a`, error catastrophe) lives in the
  Tier-3 `BAR_A_SKETCH`, not canon. A true phase-TRANSITION (order-parameter / critical-point)
  treatment is an open seam, not covered.

---

## 14. Tier-3 footer

**Status: Tier-3 exploratory — working, not canon.** This is a **render-model spec (a tool)**, not
a framework claim. It maps an already-ratified data schema (`SCHEMA_v2`, itself ratified as a TOOL
only) to visual channels. The **convergence list stays 9**; nothing here is compiled, promoted, or
a 10th anything. The genuinely-new items (§13) are render-layer extensions consistent with Pav's
2026-06-10 steer — they inherit the candidate / instrument-not-field status of the primitives they
ride on (phantom mass, the charge algebra, fuzzy-LOD) and are flagged NEW, not folded into canon.
This v0 inherits the Tier-3 draft status of `PPWc | frame` and of the `latent_cosmology §4` camera
spec it extends. No committed files were edited; this is a new candidate file. Author date:
2026-06-10.

---

## 15. Cross-Claude review addendum (Opus)

A second Claude (Opus) audited the spec + the `viewer_v0.html` build against canon. It rated the
work "PROCEED, with fixes — solid Tier-3, discipline largely holds," but flagged that the spec
**reads more data-bound than the instrument actually is** and caught two covered-vs-new / canon
corrections. Folding them in here, honesty first:

**Covered-vs-new corrections (the load-bearing ones):**

1. **"Four classes never bundled into a quadruple" was overstated.** `cont 25:412` references an
   existing **cont-22 four-layer stack** `{kernel canon → compiled canon → canon artefact →
   function canon}`. The genuinely-new bit is therefore **not** "assembling four unbundled classes"
   — it is the **`protocol` relabel of `function-canon` + the span-as-solidity *criterion*.** The
   criterion is new; the four-layer set is not. (The §13 default-to-fold note partly anticipated
   this; this makes it explicit.)
2. **The cont-13 charge Cayley table was SUPERSEDED to ASYMMETRIC by cont 15 §1.** §3.a (and the
   audits) cite the cont-13 charge-product table as if symmetric; **cont 15 §1 corrected it** — "A−
   does the real compilation work … they are not symmetric." This is the **same supersession class**
   the audit correctly caught for cont 24 → cont 25 but missed here. **Any future charge-driven
   force layout must use the A− primary / asymmetric reading**, not a symmetric table.

**Spec-binding down-ranks (the spec described a more capable instrument than was built):**

3. **§3.a (charge-driven attract/repel) → role-proxy.** **No specimen carries `a_charge`**; the
   build derives edge sign from ROLE (parents/roots → attract, candidates/rivals → repel). The
   charge-table binding is **deferred / unpopulated**, and when populated must use the cont-15
   asymmetric reading. The viewer legend now discloses edges as "role-proxy (no `a_charge` in any
   specimen)."
4. **§5 (solidity-as-span) → PROXY span, not a measured quadruple-span.** Only the **canon axis**
   (confidence + `certain_core`) is fully data-bound. **`kernel`** (`frame_layer.physical_membership`)
   is absent on the abstract `w.parents` and on all v1 specimens, so it **defaults**; **`artefact` /
   `protocol`** are role/utility proxies (the build now also reads `child.adoption.state` for the
   protocol axis, but that field is `null` in all 7 specimens). The viewer legend now discloses
   solidity as a **proxy** span. The flagship new channel demonstrates the **visual** of
   span-solidity, not a grounded measurement.
5. **`size` is a hand-tuned proxy, not a first-class field** (`action_spaces_unlocked` +
   `descendants` + `sub_welds` + surprise reach). The size→force-magnification coupling is real in
   the render but rests on this proxy — consistent with the Tier-2 / instrument-not-field status of
   phantom mass.
6. **Deferred (in spec text but NOT in the build):** `weld_type`-weighted fusion tint as a
   continuous blend, `pre_weld_relationship` antagonism-repel pre-weld, and `revival.method_continuity`
   morph. (v0 now renders the **dominant** `weld_type` label + a **fractured seam lens** when
   `S_structure.agreed===false`, but not the full weighted blend.)

**Build fixes applied to `viewer_v0.html` after the review** (verified against the real specimens):

- **Open-weld detection fixed.** `qm_relativity` (the canonical open/never-consummated frontier)
  was mis-detected as closed — its string `when` ("Still OPEN as of 2026 … no end date") set
  `to=2026`, so the viewer fired a **false fusion flash at 2026** and never drew the unclosed splat.
  `weldOpen` now ORs in the `when`-string open-hint and `child.status` (`open-conjecture`); for open
  welds `weldFire=weldStart` (1916, the seam-notice year), **no fusion flash**, and the **dashed
  unclosed ring + "OPEN — unconsummated weld" label** render.
- **`YEAR_RE` decade bug fixed.** `/\b…\b/` failed on every `YYYYs` form (`1930s`, `mid-1840s`,
  `2010s`) because the trailing `s` defeats `\b` after four digits — silently dropping dates from
  ranges, dormancy bounds (`darwin_mendel`'s 2nd interval, `qm`'s ~1990s window), and descendant
  births. Now `…s?\b` + `parseInt`.
- **Forcing impulses no longer no-op.** `acted_on` targets pointing at actors (`act-*`), the weld
  (`weld-*`), non-instrument `parents_full` (`par-*`/`pf-*`), or a `weld.sub_welds` id (`sw-*`,
  which is never rendered as a node) previously did nothing (internet 4/15, deep_learning ~7/26,
  manhattan 13/14 inert). A `resolveForcingTargets()` now resolves to nodes → actors → child (for
  `weld-*` and any unresolved `sw-*` sub-weld) → parent nodes (for `par-*`/`pf-*`). Verified by a
  Node harness that builds all 7 specimens: resolution is now **15/15 (internet)**,
  **26/26 (deep_learning)**, **22/22 (keynesian)**, and **14/14 (manhattan)** — every populated
  forcing target now lands. (Root sub_wrappers like internet's `sw-datagram-root` already resolved
  via `byId` first, so the `sw-*` fallback only catches genuine sub_welds.)
- **Solidity legend relabeled** to "proxy span" (see #4).
- **Minor:** dormancy dimming now re-brightens per explicit interval `to` (multi-cycle correct);
  forces are frame-rate-scaled (`fs=clamp(dt*60,…)`) to reduce FPS-coupled jitter; the computed
  `weld_type` and `S_structure.agreed` are now actually rendered.

**Physics census / program:** the review accepted the `latent_physics_PROGRAM.md` verdict and
instinct-mappings **as-is** (the RG-semigroup caveat on instinct (3) was called a "genuine catch").
See that file's own review addendum for detail. Nothing here promotes anything; **convergence list
stays 9.** Addendum date: 2026-06-10.

---

# v1 addendum (Pav test-drive round)

**What this is.** `viewer_v1.html` is a NEW file built by COPYING `viewer_v0.html` as the base
(`viewer_v0.html` stays as-is, for lineage) and implementing all eight asks Pav raised on the v1
test-drive (2026-06-10). It inline-embeds all 7 base specimens (verbatim, unchanged) **and** all 7
NEW additive overlays from `overlays/*.overlay.json`, so it is fully self-contained (no CDN, vanilla
JS). The overlays are read at load via a second class of `<script type="application/json"
data-kind="overlay">` blocks. Convergence list stays 9; nothing here is canon (Tier-3 render tool).

## The 8 asks → what was built

1. **NET OUTCOME latent→physical (the harvest band).** A THIRD band now sits ABOVE latent:
   `HARVEST ↑`. It renders the previously-unrendered schema arrays as nodes — `harvest.descendants[]`
   (new theories seeded), `harvest.cultural_harvest[]` (icon + colour by `art|scifi|tech|prizes|
   safety|other`), and `child.utility.action_spaces_unlocked[]` (the new affordances). Each appears
   at its overlay `harvest_dates` `emerged` year (disclosed-default post-weld stagger when absent),
   connected to the child by harvest edges. A subtle dashed **feedback arc** runs from each
   action-space node back DOWN into the physical band with an arrowhead — the "function utilised →
   expanding the action space" loop Pav named (theories → kernel canon → feedback loop). In v0 these
   arrays were dropped on the floor (cultural_harvest used only as a boolean; action_spaces only
   counted into a size scalar). The harvest band binds DIRECTLY to existing populated base data.

2. **Entity lifecycles.** Actors and ideas now carry web-grounded lifecycle dates from the overlay
   `entity_lifecycles{}` (people: born/died; institutions: founded/dissolved; ideas:
   conceived→formulated→named). Actors fade IN at born/founded, and after `died`/`dissolved` fade to
   an **outline glyph** (death dim, ~12y to a 0.30 floor). Ideas use conceived→formulated as their
   render-birth. Hover shows a **lifecycle strip** (`conceived → born → founded → formulated → named
   → died → dissolved`) plus the overlay `_note`. Matching is by actor `id` first (v2 specimens:
   `act-*`), then by name (maxwell/darwin/qm use `people_0[].who` name strings) — graceful when an
   actor has no overlay entry (falls back to the base `when` year).

3. **Depth/context dial.** A `Depth/context` slider (0–100%) controls render depth along
   roots↔child↔harvest: at low depth only the child shows; raising it admits parents, then
   harvest, then roots/actors (outermost). The SAME dial doubles as the relevance cutoff — as depth
   drops, low-confidence nodes drop FIRST (`conf < (1−depth)·0.85`). This is Pav's contextual-scale
   dial (zoom a fixed frame, or contextually scale by adjusting it). It applies in both single and
   GLOBAL views.

4. **Stale data + NOW.** The time range now ALWAYS extends to `NOW = 2026.5`, and every specimen
   **opens at NOW** (`year = NOW` on select; a `⟲ NOW` footer button re-jumps there). Overlay
   `now_extension[]` (2024–2026 events, coloured by `harvest|event|revival|decay`) render as diamond
   ticks near NOW; a dashed teal **NOW 2026-06 marker line** is always drawn. So the timeline no
   longer dead-ends at ~2024.

5. **Math (honest answer — wired + disclosed).** The sharp/fuzzy meter is **relabelled and
   recomputed** as the AGNOSTIC-UNITS frame-relative ratio: each node's confidence and size are
   normalized to a ratio in its own specimen's `[min,max]` frame, and the meter reports
   `Σ(ratioMass·ratioConf) / Σ ratioMass` as "% agnostic-ratio certain-mass". Its tooltip discloses
   exactly what it is and is NOT. **Honest truths, as Pav asked:**
   - v0's blobs were (and v1's still are) **gaussian radial-gradient splats — NOT wavelets**
     (`createRadialGradient`, spread `= r·(1+fuzz·1.4)`).
   - v0's sharp/fuzzy meter was **certain-core mass fraction** (a `confidence ≥ 0.8` threshold on a
     size proxy), **NOT** the MDL / `gain_v2` machinery. v1 rewires it to the agnostic frame-ratio
     and relabels it honestly.
   - **`gain_v2` / MDL-in-bits numbers DO NOT EXIST for these specimens** (the real-corpus pilot is
     owed; the frame-lock pilot only validated the synergy metric on synthetic ground truth, not
     these merges). The viewer **never renders fake bits** — every quantitative readout is either a
     real base field or a disclosed proxy/estimate.
   - **The honest resonance:** wavelets ARE the multi-resolution / level-of-detail idea, and gaussian
     splatting is the graphics cousin — a principled FUTURE rendering basis (gaussian-mixture /
     wavelet LOD over the depth dial), not what v0/v1 use today.

6. **Global view.** A `GLOBAL` button shows all 7 specimens as swimlanes on one shared
   **absolute-year** axis (dates are absolute years → directly comparable, no normalization needed).
   Per-specimen **on/off chips** toggle lanes; the observer select and the depth dial apply globally.
   **Cross-specimen normalization:** node **size and opacity are normalized per-specimen to the
   agnostic [min,max] frame-ratio** so the per-specimen proxies (sizes, confidences) become
   comparable across specimens — disclosed in the GLOBAL legend. A NOW line and per-specimen weld-span
   bars + now-extension ticks are drawn per lane.

7. **Rival fade + connection fix.**
   - **Rival fade:** defeated rivals now DECAY as the weld hardens. The decay reads overlay
     `rival_fates{}` (`faded` → ~15y to a 0.10 ghost; `niche` → ~25y to 0.32; `absorbed` → ~18y to
     0.22; `persists` → slow to a 0.55 floor) and falls back to a **disclosed default** (fade to
     ghost over ~15y after hardening) when no fate is present. Faded rivals get a dashed ghost
     outline. Honest inversion respected: for OPEN welds (qm_relativity) rivals do **not** fade — the
     frontier keeps all rivals alive (per the qm overlay's `rival_fates._note`).
   - **Parent→unifier connection (the diagnosed v0 bug):** in v0 the parent→child edge was a
     near-invisible 1px muted-blue thread gated on the child's still-ramping opacity
     (`if(a.op<=0.05||b.op<=0.05) return;`), and for maxwell the prose `weld.when` parsed
     `weldStart=1861 / weldFire=1888` (text-order years) leaving a 27-year column gap so the line was
     absent exactly when the weld fired. v1 draws `kind:'parent'` edges with a **brightness floor
     through the weld-fire window** (`near = 1−|year−weldFire|/8`), thickening to a bright `#bfe0ff`
     weld line with a white spark at fire — so parents VISIBLY connect at the moment the unifier hits
     the timeline, in maxwell and all specimens. (The v2 specimens additionally now ingest ALL
     `parents_full` granular lobes, not just `instrument` ones, fixing the v0 ingestion gap.)

8. **Encompass / absorption + Theory DNA.** At weld-fire, parents are **drawn INTO the child
   membrane** (`absorbT` ramps 0→1 over ~4y after fire): each parent becomes an internal **lobe**
   whose size is scaled by its `theory_dna.load_bearing_share`, with a **stub** (receptor-hook spike
   in the parent's frame-colour, length scaled by share) poking OUT through the child's membrane ring
   — the cont-25 Steer-5b "parents persist as procedural-root stubs" reading. The free parent blob
   dissolves as its lobe forms. A **THEORY DNA bar** (bottom-left) renders per-child:
   `parent-A share | parent-B share | … | novel residue` segments, each labelled with its share % and
   `confidence`, tagged **"estimate · not measured bits"**, with a disclosure line that load-bearing
   shares are historiographic ESTIMATES (conceptually the `gain_v2` synergy quantity) and that no
   `gain_v2` bits exist for these specimens. The novel residue is the child-coloured remainder (the
   synergy share).

## The MATH answer (verbatim honest)

We are **not** using the MDL / `gain_v2` machinery under the hood for these renders, and we never
fabricate it. The blobs are **gaussian radial-gradient splats, not wavelets**. The sharp/fuzzy meter
in v0 was a **certain-core mass fraction** (a confidence threshold on a size proxy), NOT MDL; v1
**rewires it to the agnostic-units frame-relative ratio** (per-specimen `[min,max]` normalized
certain-mass) and discloses precisely that in its tooltip. **`gain_v2`/MDL-in-bits numbers do not
exist for these specimens** — the real-corpus pilot is owed — so the THEORY-DNA shares and the
novel-residue/synergy figure are rendered ONLY as **disclosed historiographic estimates** (overlay
`theory_dna`, confidence ≤ 0.6), never as measured bits. The principled future basis is exactly the
wavelet / gaussian-mixture multi-resolution idea (gaussian splatting is its graphics cousin), which
would sit naturally under the depth dial as a real LOD spine — a future, not a present claim.

## The NORMALIZATION answer

**Is the dataset normalized?** Dates are **absolute years → already cross-specimen comparable** (the
GLOBAL view plots all 7 on one absolute-year axis with no date normalization). Sizes and
confidences are **per-specimen proxies** and are therefore NOT directly comparable — so v1 maps each
specimen's values to a **ratio of its own frame `[min,max]`** (the agnostic-units dimensionless
fraction-of-frame, per `agnostic_units_hairy_membrane_SKETCH.md`). This per-specimen ratio drives
both the sharp/fuzzy meter and the GLOBAL-view node size/opacity, and it is **disclosed** in the
legend and the GLOBAL legend. It is a frame-relative ratio with fog attached, not a measured
absolute.

## Overlay-data provenance note

The seven `overlays/*.overlay.json` files are **ADDITIVE and web-grounded** (`web_grounded:true`),
authored 2026-06-10. They never duplicate or mutate base specimen fields and never touch ratified
files. Each carries: `now_extension[]` (2024–2026 events, with `sources[]` URLs), `entity_lifecycles{}`
(born/died/founded + idea conceived/formulated/named — structured dates the base lacks),
`harvest_dates{}` (emerged/consolidated dating for harvest + action-space items), `rival_fates{}`
(decay/absorption fates for the fade law), and `theory_dna{}` (load-bearing-share ESTIMATES, capped
confidence ≤ 0.6). Lifecycle and rival-fate keys match base ids exactly where ids exist (`act-*`,
`rel-*`, `pf-*`/`par-*`, `child-*`) and fall back to exact name strings for the v1 specimens
(maxwell/darwin/qm) whose roots/parents/rivals are name-keyed. Where a base entry has no overlay
match, the viewer degrades gracefully to the base `when` year and omits the missing strip — nothing
is invented. Binding was verified across all 7 specimens (every theory-DNA parent and every rival
fate matched; lifecycles matched all `act-*` actors and the overlay-covered `people_0` subset).

**Build/quality:** vanilla JS, no CDN; `node --check` passes on the extracted app script; all 14
embedded JSON blocks parse; per-frame pairwise work is capped and absorbed parents are skipped to
hold ~60fps with ~100 nodes; all proxies disclosed in the legend / ratio tooltip / DNA tag.
Convergence list stays 9. Addendum date: 2026-06-10.

## Opus review fold (corrections applied 2026-06-10)

An Opus review scored all 8 v1 asks as MET from the extracted app code (not from claims) and both
v0 bugs as genuinely fixed (parent→unifier brightness-floor connection at weld-fire; rival fade by
overlay `fate` enum, with open welds correctly held alive). Recommendation was **ACCEPT** with four
LOW-priority cleanups, all now folded in:

- **(a) Debris removed.** The 15 `__script_0.js … __script_14.js` extraction temps a prior build
  left in the `canonical_genealogy/` dir were deleted — they were never referenced by the viewer
  (which embeds its JSON inline) and must not be committed.
- **(b) Depth label tracks the real gate.** The `depthVal` readout thresholds were
  `<0.2 child / <0.5 +parents / <0.85 +harvest`, which lagged the actual `depthVisible` gates
  (parents un-gate at 0.34, harvest at 0.7, roots at 0.85). Relabelled to
  `<0.34 child / <0.7 +parents / <0.85 +harvest / full` so the readout matches what is rendered.
  Gating logic itself was already correct and is unchanged.
- **(c) `fracYear` rejects range-style strings.** A `now_extension` `when` like `"2022-2025"`
  mis-parsed: the month group captured `20`, landing the marker tick at ~2023.58. Added a guard —
  if the parsed month `>12` (or day `>31`) it falls back to the year start. Affected only the
  x-position of a couple of marker ticks (never shown as a date), now corrected.
- **(d) Inert rival-fate entries wired, not deleted.** The review noted several `rival_fates` keys
  target nodes that are not `relation:'rival'` edges (e.g. maxwell *Luminiferous ether* / *molecular
  vortex*, darwin *Symbiogenesis* / *Mendel-Fisher* / *Mutationism*, deep_learning *rel-cybernetics*
  + the `act-*` actor ids, keynesian *stockholm/kaleckian/marginalist*, manhattan *tube-alloys/qg/
  apollo*, internet *arpanet*) and so drove no render. Rather than discard this web-grounded,
  disclosed research, the hover tooltip now surfaces the fate for **any** relative that has one,
  tagged `(not a rival — no opacity decay)` so the distinction stays honest. The opacity/decay law is
  unchanged — only genuine rivals fade — so there is **zero visual regression**, and the one true
  rival per specimen still fades by its overlay fate exactly as before. The handful of fate keys that
  match **no** node at all (ether / vortex / mutationism / `act-*` actor ids) are retained as
  documented research and remain unrendered **by design** — no nodes are invented for them, per the
  never-fabricate discipline.

No ratified files were touched; only `viewer_v1.html`, this addendum, and (deletion only) the stray
`__script_*.js` temps. `node --check` still passes after the fixes. Review-fold date: 2026-06-10.
