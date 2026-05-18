# Diagrams Changelog

Iteration history of the framework's diagrams, with explicit version provenance. Acknowledges where the discipline of preserving every iteration on disc was not yet in place (see the diagram 06 gap below).

For repo-wide changelog see [`/CHANGELOG.md`](../CHANGELOG.md).

---

## Discipline (going forward)

**New iterations get versioned filenames.** When a diagram changes structurally:
- Save the new version as `XX_name_vN.svg`
- Move the previous version to `archive/` if it was unversioned, OR keep it in place if it was already versioned
- Update the unversioned canonical name (e.g., `06_two_observers_conversation.svg`) to be a copy of the current latest
- Log the change in this file

**Cosmetic edits** (typo fixes, color adjustments that don't change structure) can be overwrites without a new version.

**Structural edits** (new panels, removed elements, layout changes) get a new version always.

This discipline is the framework's own provenance principle applied to its diagram artifacts. It also fixes the gap that produced the diagram 06 v1–v5 reconstruction problem described below.

---

## Files currently in the directory

### Canonical / current

| File | Status | Notes |
|------|--------|-------|
| `01_compile_loop.svg` | v1 (only) | The compile loop with A⁻ as primary discipline. No iterations needed yet. |
| `02_observer_architecture.svg` | v1 (only) | Action-space → wrapper → harness → canon onion. No iterations. |
| `03_genotype_phenotype.svg` | v1 (only) | Code vs render split. No iterations. |
| `04_four_carrier_convergence.svg` | v1 (only) | Aleph + MAMMAL + ANDI + Lippmann. No iterations. |
| `05_framework_overview.svg` | v1 (only) | Canon primitives grouped + three-lens callout. No iterations. |
| `06_two_observers_conversation.svg` | v6 (current) | The full-detail 920×1300 two-observers diagram. See iteration history below. |

### Case study (preserved iterations)

| File | Subject |
|------|---------|
| `case_study/06_v1.svg` – `06_v6.svg` | Six uniform 800×500 schematic SVGs preserving the structural signature of each iteration of diagram 06. Embedded in the live site's case-study section. Reconstructions (see provenance gap below), not the original full-detail renderings. |

---

## Diagram 06 — iteration history (with provenance gap acknowledged)

Diagram 06 was iterated six times between 2026-05-17 and 2026-05-18. **The first five versions were NOT preserved on disc** — each overwrote the previous file at `06_two_observers_conversation.svg`. Only v6 survived in its original full-detail form.

This was a discipline gap: the framework's own provenance principle (preserve what was tried) wasn't applied to its diagram artifacts. The gap was caught and named by Pav on 2026-05-18; this changelog and the going-forward discipline above is the response.

To recover the structural progression for the live-site case study, six schematic SVGs were reconstructed from chat-session memory and saved at `case_study/06_v1.svg` – `06_v6.svg`. The schematics are uniform 800×500 and show the essential structural signature of each version; they are NOT pixel-perfect copies of the originals. They preserve the iteration story but not the original visual fidelity of v1–v5.

### v1 — 2026-05-17

First pass. Two stylized heads facing each other with the word "home" as a carrier between them. Each observer with a canon graph and an imagine engine. Render annotations underneath for what "home" meant to each.

Original size: ~720×560. Original on disc: lost (overwritten). Schematic preserved: `case_study/06_v1.svg`.

### v2 — 2026-05-17

Added the outer reality container (substrate Ω) wrapping both observers, plus explicit A⁺ and A⁻ chips inside each observer's wrapper. Made the constraint-checking pass visible.

Original size: ~820×620. Original on disc: lost. Schematic preserved: `case_study/06_v2.svg`.

### v3 — 2026-05-17

Major structural reframe after Pav's feedback that "home" is the shared kernel canon, not split-by-observer:

> "hmm its not quite like that for people unless its a homogenous lab test. 'home' is the latent kernel canon (language grounded in physical description of a place you habituating in, in a way everyone has a home — those always on a move: world is their home), the observers overlapping cones their intent defines the meaning of home and the situation the squze and the context the substrate that they are comiling all play into effect. thats the dial, home can be home or home can be a paradigm shift, the agnostic has the scope for it."

Three tiers: kernel canon ("home") at top, dial (single shared in v3) in middle, meaning range at bottom from literal place through belonging and self to paradigm shift.

Original size: ~820×700. Original on disc: lost. Schematic preserved: `case_study/06_v3.svg`.

### v4 — 2026-05-17

Each observer gets their own private dial (not shared). Each renders the other within their wrapper. Wrappers project to each other. Elevation planes stack on the right. Resolution band at the bottom: struggle ↔ negotiation ↔ union.

Original size: ~880×1000. Original on disc: lost. Schematic preserved: `case_study/06_v4.svg`.

### v5 — 2026-05-17

Added explicit idea domain (imagine engine + fuzzy field + personal canon) and body domain (harness with evolved + memory + instinct). The asymmetry of action made explicit: action takes space in both domains.

Original size: ~880×1140. Original on disc: lost. Schematic preserved: `case_study/06_v5.svg`.

## 2026-05-18 — diagram 06b casual companion added

`06b_friction_states_casual.svg` — three-panel companion at 800×420 showing the friction-band states (freeze / viability / explode) in casual-reader form. Two figures per panel, A⁺/A⁻ annotations in the viability panel, plain-language examples for each state. Designed for manifesto v5 and casual contexts where the full v6 diagram (920×1300, ~25 architectural elements) is too dense. v6 stays as the technical reference; 06b is the entry-level companion.

This is the first time the discipline (versioned filenames, changelog entry) is applied at creation rather than retrospectively. Going forward.

---

### v6 — 2026-05-17 (current)

Second major reframe after Pav's feedback on friction, body-as-membrane, and planes-as-nodes:

> "struggle is latent friction, you need it for energy inertia… agnostic doesn't care about home it mediates the process based on do not freeze do not explode… the elevation planes are actually nodes, interconnected… the body domain harness is the membrane, what's inside is a black hole to the outside observer (but now we starting to go into the brain with latest science, drugs and hypnosis, mental probes — so not impenetrable and is another hidden protocol). in a way thats the paradigm shift."

Body-harness becomes the outer membrane (paradigm shift framing). Elevation planes become an interconnected node network with sequence semantics. Resolution band becomes friction band (freeze ↔ viability ↔ explode) — substrate-level regulation, not observer-level outcome.

Original size: 920×1300. Original on disc: **PRESERVED** at `06_two_observers_conversation.svg`. Schematic preserved: `case_study/06_v6.svg`.

---

## 2026-05-17 — initial framework diagrams added

Five diagrams created (01–05). Each was a one-shot rendering, no iteration. Saved as standalone SVG files with dark-theme palette matching the framework site (`#0a0a0a` bg, `#ececec` text, framework accent colors).

---

## Companion notes

The diagram-iteration loop that produced six versions of diagram 06 is also documented in [`continuations/16.md`](../continuations/16.md), where the ten new or refactored framework primitives surfaced through the loop are compiled. The loop is named there as a *methodology* (carrier-before-canon) — and is now also documented in this changelog as a *provenance practice* (versioned filenames + archive + changelog).

The two-faceting (methodology in continuation 16, practice in this changelog) is intentional: continuation 16 says *this is what the iteration loop produced as content*; this changelog says *this is what we lost by not preserving each step, and how we'll preserve them going forward*.
