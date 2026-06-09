> **Superseded by [`SCHEMA_v2.md`](SCHEMA_v2.md) — ratified 2026-06-09.** Retained as the v1 historical render-spec.

# Canonical Wrapper-Genealogy Specimen — SCHEMA

> **Status:** Tier-3 exploratory data-harvest schema, surfaced for **Cowork+Pav ratification** — NOT canon, NOT a tier promotion, NOT a convergence-list change (stays **9**). This file is a *render spec*: it refines the VARIABLES used to capture one merge event as a rooted genealogy. It does not compile canon or promote anything.
>
> **Provenance:** Authored 2026-06-09 by the Schema Agent at Pav's steer, from the enriched-model brief + `frame_lock_protocol_DRAFT.md`, `parents_produce_WC_FORMALIZATION_DRAFT.md`, `observer_frame_kernels_DRAFT.md`, and the Phase-1 wrapper-class DB (`../latent_olympics_data/wrapper_classes_phase1.json`, read in full). Single-agent surface — owes external review.
>
> **Companion file:** `one_specimen.template.json` — an empty, every-field-present JSON template ready to fill for one specimen.

---

## 0. What a "specimen" is

A **specimen** is **one merge event** — a single emergent wrapper `W_C` born from two parents — **rendered as a rooted, directed genealogy graph that STOPS AT THE PRESENT.** Where the Phase-1 DB stores one flat row per wrapper *class*, a specimen stores the whole *living tree* around one such birth:

- **DOWN** (roots, in the **physical** frame): the smaller sub-wrappers `W_C` is recursively made of, bottoming out in **people-wrappers** — the ground kernel "(0)" — standing in their time, place, environment, culture.
- **UP** (harvest, in the **latent + cultural** frame): the emergent children `W_C` went on to seed (new theories), plus its spill into art / sci-fi / tech.
- **WIDE** (relatives): cousins, influences, siblings spanning the physical AND the latent.

Two properties are first-class and pervade every field:

1. **Frame-relativity.** Every wrapper lives in a **frame** = the observer global kernels `{time, space, knowledge, meaning}`. Whether the parents make a third is frame-relative (two rocks in `space` = nothing; two rocks through `time` = strata). Each node, each weld, and the specimen as a whole declare which frame(s) they hold in. (Grounds: `observer_frame_kernels_DRAFT.md` §1-§3; `parents_produce_WC_FORMALIZATION_DRAFT.md` §1.F.)
2. **Fuzzy level-of-detail (LOD) / confidence.** Everything carries a **`confidence ∈ [0,1]`** and a **zoom/LOD depth**. There is a **certain core** near the surface (the trunk: the merge event and its immediate parents, well-attested) **fading into a probabilistic frontier** in the deep roots (down to people/place) and at the wide edges (distant cousins, speculative influences). The frontier is *not* noise to be cleaned — it is **where new conjectures are cultivated and tried**. A **conjecture = a low-confidence weld drawn but not yet confirmed.** (Grounds: the enriched-model brief; mirrors the Phase-1 DB's soft-scores-in-[0,1] discipline.)

A specimen is therefore a *fuzzy genealogical render of one weld*, honest about where the record is solid and where it is conjecture.

---

## 1. The genealogy graph (informal shape)

```
                 cultural_harvest[]  (art | scifi | tech | other)
                          ^
        descendants[]  ---+---  (new theories seeded by W_C; latent + culture)   ← HARVEST (UP)
                          ^
                   ┌──────────────┐
   W_A  ──weld──►  │     W_C      │  ◄──weld──  W_B        ← the MERGE EVENT (certain core / trunk)
 (parent)          │  (the child) │           (parent)
                   └──────────────┘
                          |
        sub_wrappers[]  --+--  (the smaller wrappers W_C is made of, recursively)   ← ROOTS (DOWN, physical)
                          |
                       people_0[]   (the ground kernel "(0)": who, where, when, culture)
```

Plus, threaded across all of it:
- **`fuzzy_layer`** — partitions the above nodes/welds into `certain_core` (trunk) vs `frontier` (speculative roots + edges).
- **`discrepancies[]`** — the real-record fuzzy frontier: priority disputes, contested genealogies, date/attribution conflicts, contested-dormancy narratives, and especially **framework-vs-record tensions** (where the clean two-parent weld does not match the messy multi-parent history — the most valuable signal).
- **`sources[]`** — the citation backbone; every load-bearing field should be traceable here.

---

## 2. Field groups (the canonical specimen record)

Eight top-level groups. Every leaf that asserts a fact about the world carries (or inherits) a `confidence ∈ [0,1]`; nodes additionally carry an LOD/`depth`. Bit-level MDL values are **qualitative only** at this stage (see §3, the `bits_note` discipline).

### 2.1 `child` — the emergent wrapper `W_C`
The thing that was born in this merge. The trunk node.

| field | type | meaning |
|---|---|---|
| `name` | string | canonical handle of `W_C`. |
| `kernel` | string | net product / what it essentially *is* (its localKernelCanon, in the Phase-1 sense). |
| `frame` | string[] ⊆ `{time,space,knowledge,meaning}` | which observer global kernel(s) `W_C` is rendered in. |
| `status` | enum | one of `risen | active | dormant | resurrected | stale`. Observer-relative lifecycle position. |
| `confidence` | number [0,1] | confidence that `W_C` is a real, distinct emergent (not a relabel of a parent / not a pile). |
| `utility` | object | `{ unifier: <how it bridges>, compressor: <how it shortens description>, action_spaces_unlocked: string[] }` — Pav's three utility legs as prose + an enumerated affordance list. |

### 2.2 `weld` — the merge (parents → child)
The edge that *is* the event: how `W_A` and `W_B` fused into `W_C`. This is the heart of the specimen and the locus of the parents-produce-W_C test.

| field | type | meaning |
|---|---|---|
| `parents` | array of 2 | `[W_A, W_B]`, each `{ name, kernel, frame[], confidence }`. |
| `shared_sub_object_S` | string | the **seam** they fused along — what overlapped (the `S` of the pushout; the "nesting space / Venn-lens"). |
| `surprise` | string (PROSE) | what `W_C` does that **neither parent predicts alone** — the synergy. Prose, not a number. |
| `surprise_confidence` | number [0,1] | confidence that the surprise is real (genuine synergy vs additive blend). |
| `bits_note` | string (QUALITATIVE ONLY) | a qualitative note on description-length / synergy-in-bits. **Do NOT fabricate bit values** — real MDL-in-bits needs latent embeddings (a later step). See §3. |
| `survived` | string[] | which features of the parents persisted into `W_C` (the "stubs" / procedural roots that live on). |
| `dropped` | string[] | which features were lost / not carried through the weld. |
| `frame_of_weld` | string[] ⊆ `{time,space,knowledge,meaning}` | the frame(s) in which the weld actually holds (may differ from the child's own frame; e.g. a weld that only holds through `time`). |
| `lod_scale` | string | at what zoom/resolution the weld holds (e.g. "holds at the field-level grain; dissolves into many sub-welds when zoomed in"). |
| `when` | string | date / era of the merge. |
| `dormancy_intervals` | array | `[{ from, to, why }]` — periods the weld/child went dormant. |
| `revival` | object | `{ when, by, trigger }` — if resurrected, when and what woke it. |

### 2.3 `roots` — DOWN, the physical frame
The recursive descent from `W_C` toward people and place. **Confidence and LOD fade as you go deeper** (the certain core → probabilistic frontier gradient lives here).

- **`sub_wrappers`** : array of `{ name, kernel, frame, depth, confidence, who_called_it }` — the smaller wrappers `W_C` is built from, recursively down. `depth` = how many levels below `W_C` (0 = immediate constituents; larger = deeper roots, typically lower confidence).
- **`people_0`** : array of `{ who, role, when, where, culture, relation }` — the **ground kernel "(0)"**: the people-wrappers the deepest roots plug into, standing in the PHYSICAL frame (their time, place, environment, culture). `relation` = how they relate to the lineage (e.g. originator, transmitter, patron, rival).

### 2.4 `harvest` — UP, the latent + cultural frame
What sat *on top of* `W_C` and what it spilled into. The tree grows up to the present here.

- **`descendants`** : array of `{ name, what, frame, confidence }` — emergent children: new theories `W_C` (crossed with others) went on to seed.
- **`cultural_harvest`** : array of `{ domain: art|scifi|tech|other, what }` — the spill into culture: art, science fiction, technology, other (the emergent clusters of this theory crossed with others).

### 2.5 `fuzzy_layer` — the LOD / confidence partition
Makes the trunk-vs-frontier split explicit and first-class.

- **`certain_core`** : string[] — which nodes/welds are **high-confidence** (the trunk).
- **`frontier`** : string[] — which nodes/welds/branches are **low-confidence**, speculative, or **conjectural** (the cultivation zone). A conjecture = a weld drawn here but not yet confirmed.

### 2.6 `discrepancies` — the real-record frontier (Pav's explicit ask)
Interesting conflicts in the historical record. **These are SIGNAL, not noise.**

Array of `{ what, sources_in_conflict, type, why_interesting, confidence_impact }`, where `type` ∈
`[priority-dispute, contested-genealogy, date/attribution-conflict, framework-vs-record-tension, dormancy-contested, whig-vs-revisionist]`.

- **`framework-vs-record-tension`** is the highest-value type: it flags where the schema's clean two-parent weld does **not** match the messy multi-parent historical reality — i.e. which variables the schema is missing.
- `confidence_impact` = how this discrepancy moves the confidence on the affected node(s)/weld.

### 2.7 `sources` — the citation backbone
Array of `{ name, type, url, what_used_for, reliability }`, where `type` ∈
`[aggregator, encyclopedia, scholarly-history, primary]` and `reliability ∈ [0,1]` (or a labelled band).

> **Harvest discipline (from the brief):** consult the WEB, do **not** work from memory; cite real sources; mark uncertain claims low-confidence. Aggregators to consult: **Wikidata** (influenced-by, discoverer, field-of-work, dates, place), **OpenAlex** (concept + works graph), **SEP** / **IEP**, **Wikipedia** "history of …" sections, the **Mathematics Genealogy Project** / academic family trees, **nLab**, **Semantic Scholar / Google Scholar** citation lineage, and named **scholarly histories** (e.g. Hunt *The Maxwellians*; Provine on population-genetics history; Rovelli/Smolin on quantum gravity). Find more as needed. Be honest about reliability.

### 2.8 specimen header (top-level metadata)
| field | type | meaning |
|---|---|---|
| `schema_version` | string | e.g. `"0.1-canonical-genealogy"`. |
| `specimen_id` | string | stable slug for this merge event (e.g. `special-relativity`, `lcao`). |
| `_status` | string | the Tier-3 working-not-canon disclaimer (carried in-record, mirroring the Phase-1 DB convention). |
| `extends` | string | path back to the Phase-1 class row this specimen instantiates (see §4). |
| `generated` | string (date) | authoring date. |
| `frames_present` | string[] | union of all frames used anywhere in the specimen (convenience index). |
| `overall_confidence` | number [0,1] | confidence in the specimen as a whole render (the trunk-weighted aggregate). |

---

## 3. The fuzzy-LOD / confidence layer (how to read the numbers)

- **`confidence ∈ [0,1]` is everywhere and is SOFT.** Like the Phase-1 DB's `classifierWeights`/utility legs, no field is hard-categorical. A claim near the trunk (the merge event, the two named parents, the date) should be high (≈0.8–1.0); a deep root (which 17th-century artisan's practice seeded a sub-wrapper) or a wide edge (a contested influence) should be low (≈0.2–0.5) and may live in `fuzzy_layer.frontier`.
- **LOD / `depth` is a zoom coordinate.** Zooming in on the trunk reveals more certain structure; zooming into the roots/edges reveals the probabilistic frontier. `roots.sub_wrappers[].depth` and `weld.lod_scale` carry this. A weld that "holds at coarse grain but dissolves into many sub-welds when zoomed in" is recording its LOD honestly.
- **Bits stay qualitative.** `weld.bits_note` and the `compressor` utility leg may describe description-length / synergy *qualitatively* ("the joint description is clearly shorter than either parent's; order-of-magnitude only"). **MDL-in-bits is a LATER step** that needs latent embeddings — do **not** fabricate numeric bit values here. (Consistent with `parents_produce_WC_FORMALIZATION_DRAFT.md` §1.B "order-of-magnitude only on social/meaning frames" and `frame_lock_protocol_DRAFT.md`'s "first real ΔL" being a controlled-pilot-only result.)
- **The frontier is generative, not a defect.** Low-confidence welds in `fuzzy_layer.frontier` are the **conjecture-cultivation surface**: the place new welds are drawn and tried. Recording them (with honest low confidence) is the point, not a failure of rigor.
- **Frame-relativity interacts with confidence.** A weld may be high-confidence in one frame and `∅`/NULL in another (rocks: `time` PASS, `space` NULL). When that happens, record it in `weld.frame_of_weld` and note the frame-dependence in `discrepancies[]` if it is historiographically live.

---

## 4. How this EXTENDS `latent_olympics_data/wrapper_classes_phase1.json`

**Same organism, deeper zoom — not a new silo.** The Phase-1 DB and the specimen schema are two resolutions of the *same* wrapper ontology:

| | Phase-1 `wrapper_classes_phase1.json` | Canonical specimen (this schema) |
|---|---|---|
| **unit** | one **wrapper CLASS** (the abstract shape) | one **merge EVENT** (`W_C`'s birth) rendered as a genealogy |
| **grain** | flat summary row | recursive rooted graph (down to people, up to culture) |
| **direction** | the class and its `overlaps[]` (lateral edges) | DOWN (`roots`) + UP (`harvest`) + WIDE (relatives) |
| **scoring** | `classifierWeights {spread,utility,legacy,rigor}` + `utility {actionSpaces,unifier,compression}` | `child.utility {unifier,compressor,action_spaces_unlocked}` per node; per-node `confidence`/LOD |
| **confidence** | soft scores in [0,1], one set per class | `confidence ∈ [0,1]` on **every** node, weld, root, and edge, with an explicit `certain_core` vs `frontier` partition |
| **frame** | implicit (`observerRelative: true`) | **explicit** per node/weld via `frame[]` over `{time,space,knowledge,meaning}` |
| **provenance** | `refs[]` (internal file:section) | `sources[]` (external WEB aggregators) + `discrepancies[]` (record conflicts) |

**The mapping is direct:**
- A specimen's `child` corresponds to one Phase-1 `wrapper_classes[]` row (its `name`/`localKernelCanon`/`netProduct`/`utility` are the same fields, zoomed in).
- A specimen's `weld` is the **expanded, frame-indexed, per-node-confidence render of one entry in that row's `overlaps[]`** — what the Phase-1 row records as a single typed edge (`overlap | supersession | break-apart | dormant-resurrection`), the specimen renders as a full pushout (parents → S → W_C) with surprise, survived/dropped, and dormancy/revival.
- A specimen's `roots`/`harvest` make explicit the **procedural-lineage tree** the Phase-1 `origin.howItCameToBe` / `origin.parents[]` only gesture at (rings-on-a-tree; cont 18 procedural lineage).
- The specimen's `fuzzy_layer` + per-node `confidence` are the **per-node generalization** of the Phase-1 single-row soft `classifierWeights` — instead of one confidence for the class, every node and weld in the genealogy carries its own, so the certain-core-to-frontier gradient becomes visible.
- The specimen's `frame[]` makes operational the Phase-1 `observerRelative: true` flag, using the `{time,space,knowledge,meaning}` basis from `observer_frame_kernels_DRAFT.md`.

**Linkage field:** every specimen carries `extends` (header §2.8) pointing back to the Phase-1 row it instantiates, so the two files stay one graph. A specimen does **not** restate the Phase-1 `classifierWeights`; it *refines* them with per-node confidence and (later) real bits.

---

## 5. Underspecified-in-brief, flagged for ratification (schema gaps)

The brief's field list was followed faithfully. The following are places the spec was **clearly underspecified**; the template adds the minimum scaffolding and flags it here rather than inventing structure silently:

1. **Top-level header fields** (`schema_version`, `specimen_id`, `extends`, `generated`, `frames_present`, `overall_confidence`) are **not named in the brief** but are required to make a fillable, linkable JSON file and to mirror the Phase-1 DB's header convention. *Flag: ratify field names.*
2. **`relatives` / WIDE edges.** The brief's prose stresses "wide relatives (cousins, influences) spanning the physical AND the latent," but the explicit field list only enumerates DOWN (`roots`) and UP (`harvest`). The template adds an **optional `relatives[]`** array (`{ name, relation: cousin|influence|sibling|rival, frame[], confidence, note }`) to hold lateral edges. *Flag: confirm whether WIDE relatives are a first-class group or should be folded into `roots`/`harvest`/`discrepancies`.*
3. **Per-node `confidence` vs a single specimen confidence.** The brief says "every node and edge carries a confidence" AND describes a `fuzzy_layer`. The template puts `confidence` on each node/edge **and** keeps `fuzzy_layer` as the human-readable trunk/frontier partition (the two are complementary: numbers per node, plus a curated list). *Flag: confirm this is the intended relationship and not a redundancy to collapse.*
4. **`frame_of_weld` vs `child.frame`.** The brief lists both a child `frame[]` and a `frame_of_weld`. They can differ (a weld holding only through `time` whose child is later read in `knowledge`). The template keeps both. *Flag: confirm both are wanted, or whether `frame_of_weld` subsumes `child.frame`.*
5. **`bits_note` is intentionally string-only.** No numeric `bits` field exists, by the brief's explicit instruction (MDL-in-bits is a later step). *Flag: when latent embeddings arrive, add a numeric `synergy_bits` + error-bar field then, locked-before-data per the frame-lock protocol.*
6. **Multi-parent reality.** The schema renders a **two-parent** weld (`parents` is length 2), matching the framework's binary visualization. The real record is often multi-parent (`parents_produce_WC_FORMALIZATION_DRAFT.md` §3 "multi-parent is the general case"). The template handles this by **recording extra parents as `discrepancies[]` of type `framework-vs-record-tension`** (the clean-two-vs-messy-many tension), rather than widening `parents`. *Flag: this is a deliberate schema choice surfaced for ratification — it is exactly the kind of framework-vs-record tension Pav asked to mark.*

---

## 6. Filling discipline (one-paragraph checklist)

For each specimen: (1) pick the merge event and its Phase-1 row (`extends`); (2) fill `child` + `weld` first — that is the certain core; (3) descend `roots` toward `people_0`, lowering `confidence` and raising `depth` as the record thins; (4) climb `harvest` to the present; (5) add `relatives[]` for cousins/influences; (6) partition everything into `fuzzy_layer.certain_core` vs `.frontier`; (7) WEB-search every load-bearing claim and log `sources[]`; (8) actively hunt `discrepancies[]` — priority disputes, contested genealogies, framework-vs-record tensions — because those are the deliverable's most valuable rows; (9) keep all bits qualitative (`bits_note`); (10) set `overall_confidence` honestly. Be honest about source reliability and confidence; cite everything; flag any new schema gap you hit.

*End spec.*
