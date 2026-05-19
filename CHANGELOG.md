# Changelog

Material changes to the agnostic-framework repo. Granular enough to find what changed; not so granular that it duplicates git log. Entries are reverse-chronological (newest first).

For finer-grained provenance, see the relevant `continuations/NN.md` file — the continuations are the framework's primary self-documentation. This changelog is a navigation aid for repo visitors.

For diagram-specific iteration history, see [`diagrams/CHANGELOG.md`](diagrams/CHANGELOG.md).

---

## 2026-05-19

### Added
- **`manifestos/view.html`** — client-side markdown viewer that renders any `manifestos/*.md` with proper typography matching the rest of the site. Takes `?f=<filename>.md` query parameter (filename validated against safe-character regex), fetches the .md file same-origin, parses with marked.js (loaded from CDN), and applies the site's dark palette + Georgia headings + monospace topbar. Source-on-GitHub link in the topbar. Fixes the previous experience where casual_v4.md, research_v1.md, and engineering_v1.md rendered as unformatted plain text on GitHub Pages.
- **`manifestos/casual_v5.md`** — casual edition refactored to integrate the May 18 round (continuations 16, 18, 19). One new section ("The lineage you are standing on") inserted between the symbiosis section and the canon section, walking through physics → chemistry → biology → cognition → society → person as concentric rings each running the canon-formation loop at its own scale, with energy/symbol/artifact as three forms of residual structure under pressure. Renderer section gained the body-as-outer-membrane move and explicit *mutual rendering* framing from cont 16. Hidden-protocols-as-sequence-knowledge added to the opening section. Loop section gained the friction-band frame (freeze ↔ viability ↔ fuse). Canon section renamed "Canon is not truth — and canon is a moving target" with the cont-19 moving-target meta-rule closing paragraph. Where-this-could-be-wrong substantially rewritten to frame the framework explicitly as a Lakatosian research programme — names the four growth tests, recasts the "too inclusive" worry as design intent (aggregation discipline), adds procedural-lineage rendering as a recent claim that might be wrong. What-you-do gained two prescriptions: "ask which ring the friction lives in" and "check the friction band." Lakatos credit elevated in the shoulders section. Length ~7,500 words, up from v4's ~6,400. v4 preserved at `casual_v4.md`.

---

## 2026-05-18

### Added
- **`continuations/19.md`** — framework's identity named explicitly as **aggregator of procedural connections**. Three primitives added/refactored: *Aggregation discipline* (canon — the positive heuristic stated), *Catalyst principle* (candidate — external substrate is the framework's growth metabolism), *Moving target* (canon — promoted from implicit-across-rotating-key + recursive-timeline-cone + computational-irreducibility). Plus re-emphasizes Lakatosian success criterion vs Popperian falsifiability (cont 05 §3 anchor restored). Triggered by Pav's correction of cont-18 §10 #1 within minutes: "its a framework that aggregates everything for procedural connection... everything is a moving target."
- **`continuations/18.md`** — **Procedural lineage** promoted to canon as new primitive. Canon is procedural for the most part — traceable as stacked heritage from physics → chemistry → biology → cognition → society → person, with rings-on-a-tree / overlap-membrane-wrappers visual. Unity under pressure (energy / symbol / artifact as three forms of residual tension). Subsumes spiral-substrate-cycle and compile-capacity-enrichment that cont 17 had pruned as separate primitives. Triggered by Pav's correction of cont-17's pruning: "the canon it self is procedural for the most part, you can trace its origins."
- **`continuations/17.md`** — housekeeping round on at-risk primitives. Three demotions (Spiral substrate cycle, Compile-capacity enrichment, Monopole question), three folds (Procedural canon → body-domain; Engineered emergence → emergent garden; Mutual render → External Actor Model), two keep-with-sharpening (Slice-viewer + planes-as-nodes; Holographic wrapper + next-test criterion).
- **`index.html` PRIMITIVES updates per cont 17–19**: pruned five primitives that cont 17 demoted/folded; added new canon entry "Procedural lineage" per cont 18; added three new entries per cont 19 (*Aggregation discipline*, *Catalyst principle*, *Moving target*); updated counter on Procedural lineage to reflect cont-19 reframe of cont-18 §10 #1 worry. PRUNED array gained three entries (Spiral substrate cycle, Compile-capacity enrichment, Procedural canon).
- **Case study section** in `index.html` between the voice notes and §01 Read First. Six iterations of diagram 06 shown as schematics, with verbatim Pav-feedback at v3 and v6 (the biggest structural reframes). Names the diagram-iteration loop as worked example of the framework's symbiosis-as-pushout primitive.
- **`diagrams/case_study/06_v1.svg` – `06_v6.svg`** — six uniform 800×500 schematic SVGs reconstructed from the chat session for the case study. Note: v1–v5 of the full-detail original diagrams were NOT preserved on disk during their original creation (see [`diagrams/CHANGELOG.md`](diagrams/CHANGELOG.md) for the provenance gap).
- **`diagrams/06_two_observers_conversation.svg`** (the full v6 at 920×1300). Was missing from the repo despite being referenced in `index.html`; the Map section was showing a broken image before this push.
- **`CHANGELOG.md`** at root (this file).
- **`diagrams/CHANGELOG.md`** for diagram-specific iteration history.
- **PAVPAV's artist statement** + **Claude's counterpart note** in `index.html` between the hero and §01 Read First. The framework's symbiosis-as-pushout claim now has both voices on the front page.
- **`continuations/16.md`** — compile of ten new or refactored primitives surfaced through the diagram-iteration loop: the dial (per-observer modulator), friction regulation, body-as-membrane refactor, planes-as-node-network, unity-from-asymmetry across planes, mutual render, idea-side/body-side asymmetry of action, fuzzy field as named latent space, hidden protocol as sequence-knowledge, membrane penetrability as paradigm shift.

### Discipline established
- **Iterations on disc**: new diagram versions get versioned filenames (e.g., `06_v7.svg`); the unversioned canonical name (`06_two_observers_conversation.svg`) always points to the current. Earlier versions move to `diagrams/archive/` when superseded.
- **Changelogs**: this file tracks repo-wide changes; `diagrams/CHANGELOG.md` tracks diagram-specific history with version provenance.

---

## 2026-05-17

### Added
- **Outreach drafts** in `outreach/initial_contact_drafts.md` — five one-paragraph framings tuned per audience (Yann LeCun, Litman & Guo, Walker/Cronin, Logical Intelligence team, generic).
- **Scheduled-task checkpoint prompts** in `outreach/scheduled_checkpoints.md` — Reading 01 6-month (2026-11-17) and 12-month (2027-05-17) checkpoint prompts for manual scheduling.
- **Five framework diagrams** in `diagrams/` — compile loop, observer architecture, genotype/phenotype split, four-carrier convergence, framework overview map. Embedded as a new Map section in `index.html`.
- **`readings/2026-05-17_google_algo_phase.md`** — first dated operational reading of the framework against the Google search ecosystem. Six predictions with explicit scoring criteria, 6mo and 12mo checkpoint windows.
- **`audits/v03.md`** — refresh of the framework audit covering continuations 05–15. Three canon refactors, six candidates, the diagram-iteration round assessed structurally.
- **`manifestos/casual_v4.md`** — incorporates the A⁻-as-primary refactor from continuation 15 and adds the "easy half / hard half" section using the LLM-vs-EBM contrast as the casual hook.
- **`continuations/14.md`** and **`continuations/15.md`** — genotype/phenotype split as canon; slice-viewer + multi-architecture universal approximation + monopole question as candidates (14); A⁻-as-primary refactor with four-carrier convergence (Aleph, MAMMAL, ANDI, Lippmann) as the central insight of the May 2026 round (15).

### Changed
- **`continuations/09.md`** and **`continuations/13.md`** — added forward-reference notes pointing readers to cont-15 §2 for the A⁺/A⁻ asymmetry refactor (housekeeping debt from audit v03 §4).
- **`index.html` Imagine Engine canon entry** — resolved the Imagine-Engine-vs-A⁺ ambiguity by naming the relationship explicitly (Imagine Engine = process; A⁺ = operator acting on its output).
- **`index.html` Wolfram four-class canon entry** — names the viability-band / criticality Γ / Wolfram four-class three-way relationship as different measurement faces of the same substrate property.

### Fixed
- **Broken file links** in `index.html` post-restructure — manifesto cards, provenance corpus footer, version stamp updated to v0.2.
- **Repository description typo** ("hyothesis" → "hypothesis").

### Initial
- **Initial commit (v0.2)** — agnostic-framework repo created on GitHub, CC BY 4.0 license, CITATION.cff, GitHub Pages enabled at https://a70m123r.github.io/agnostic-framework/. Repository structure: `index.html`, `continuations/`, `manifestos/`, `audits/`, `v0.1/`, plus `README.md`, `LICENSE`, `CITATION.cff`, `.gitignore`.
- **agnostic-agents repo** created separately at https://github.com/a70m123r/agnostic-agents with `ARCHITECTURE.md` (v0.1 spec), `README.md`, `LICENSE` (MIT), `CITATION.cff`.

---

## Pre-repo (May 7 – May 17, 2026, kept privately)

Continuations 02–15, manifestos v1–v4 (casual), audit v01 + v02, all framework primitive development. See `continuations/` for the granular provenance log.
