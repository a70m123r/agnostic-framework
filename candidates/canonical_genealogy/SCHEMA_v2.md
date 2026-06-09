# Canonical Wrapper-Genealogy Specimen — SCHEMA v2

> **Status:** Tier-3 exploratory data-harvest schema, **DRAFT for Cowork+Pav ratification** — NOT canon, NOT a tier promotion, NOT a convergence-list change (stays **9**). This file is a *render spec*: it refines the VARIABLES used to capture one merge event as a rooted genealogy. It does not compile canon or promote anything. Specimens remain **calibration instruments / worked examples** extending `latent_olympics_data/wrapper_classes_phase1.json` at deeper zoom — NOT new convergences.
>
> **Provenance:** Authored 2026-06-09. v2 **supersedes** `SCHEMA.md` (v1). v2 = v1 **plus** (a) the 16 cross-cut refinements **R1–R16** from `BATCH_FINDINGS.md` (Maxwell / Darwin+Mendel / QM+GR read against each other), folded into the existing field groups; and (b) **five new first-class dimensions D1–D5** at Pav's steer (weld lifecycle+type · actors generalized · physical/latent LOD filter · external pull/squeeze events · fuzzy-by-design). Single-agent surface (architect + adversarial hardener) — owes external review.
>
> **What changed from v1, in one breath:** the weld stops being a *photograph* (parents → one child, with `revival` an afterthought) and becomes a *process with a graded life*; parents go N-ary with a mediating-welder slot and content/method/instrument kinds; a weld may never resolve (rival candidate children, no winner); **actors** generalize beyond people to institutions/governments/labs and become the **bridge** between the physical and latent layers; an **exogenous-forcing layer** (wars, depressions, fashions, purges, funding) sits over the whole genealogy as its "weather"; and **graded membership in [0,1] becomes the pervasive default** — a crisp boundary is now the special case, not the norm.
>
> ### DESIGN LAW (preserved, load-bearing)
> Every field added in v2 is **OPTIONAL** and **DEFAULTS EMPTY on a clean sharp weld.** A Maxwell-style settled case fills the v1 trunk (`child`, `weld.parents`, `when`, `child.status`) and leaves the new machinery empty or at its trivial default (`weld_necessity_confidence` ⇒ read as 1.0 when empty, `candidate_children = []`, `lifecycle` collapsed to a single consolidated phase, `forcing_events = []`). The schema stays **thin at the certain core and expands only at the frontier** — the framework's own fuzzy-LOD principle applied reflexively to the schema itself. *If filling a v2 field on a sharp case feels forced, leave it empty: that emptiness is correct signal, not missing work.*
>
> **Companion files:** `one_specimen.v2.template.json` (the v2 fill template, every new field pre-marked OPTIONAL) · `one_specimen.template.json` (the v1 template, retained for the three v1 specimens) · `BATCH_FINDINGS.md` (the R1–R16 derivation) · `specimens/{maxwell,darwin_mendel,qm_relativity}.{json,md}` (the three v1 worked examples this draft generalizes).

---

## CHANGELOG vs v1 (what a reader of `SCHEMA.md` needs to know)

**Carried forward unchanged:** the eight v1 groups (`child`, `weld`, `roots`, `harvest`, `relatives`, `fuzzy_layer`, `discrepancies`, `sources`); the frame basis `{time,space,knowledge,meaning}`; the fuzzy-LOD / certain-core→frontier discipline; bits-stay-qualitative; the Phase-1 mapping (`extends`); the harvest discipline (consult the WEB, cite real sources, mark discrepancies).

**Added (R1–R16, folded into existing groups — all optional, default empty):**
- `weld.parents_full[]` (N-ary) + `weld.mediating_wrapper` (the non-parent welder) + per-parent `parent_kind: content|method|instrument` *(R1, R4)*.
- `weld.when` may be an interval `{from, to|null, defensible_dates[]}` *(R2)*.
- `weld.sub_welds[]` (ordered chain) + `weld.coherence_under_zoom: confirms|contradicts` *(R3)*.
- `child.status` gains `open-conjecture`; `child.status_trajectory[]` *(R5)*.
- `weld.candidate_children[]` + `weld.unresolved` + `weld.contest_axis` + `weld.weld_necessity_confidence` *(R6, R8)*.
- `weld.feature_ledger[]` (per-candidate survived/dropped) *(R7)*.
- `weld.surprise_confidence` declared **orthogonal** to `child.confidence` *(R9)*; `weld.surprise_priority` *(R15)*; `weld.bits_note` may be `"principled-null"` *(R16)*.
- `weld.S_structure{components[], internal_conflict?, agreed}` *(R12)*.
- `weld.revival.kind: same|reinterpreted`; `weld.reattribution{}`; `weld.weld_chain[]`; `weld.dormancy_intervals[].why_frame` *(R10, R11)*.
- `weld.weld_operator` *(R13)*; `weld.pre_weld_relationship` (now lives inside `lifecycle`, see D1) *(R14)*.

**Added (D1–D5, new first-class machinery):**
- **D1** — `weld.lifecycle{ phase_trajectory[], pre_weld_relationship, weld_type[] }` (§2.2.h): the weld's graded life + a weighted weld-type classification. A **weighted index** over the R5/R6/R10/R14 fields, not a duplicate of them.
- **D2** — new top-level `actors[]` (§2.6): generalizes v1 `people_0` to institutions/gov/labs/etc., with two role-relations `carrier_of[]` (champion, UP) and `inhabitant_of[]` (operator, WITHIN). The physical↔latent bridge.
- **D3** — `frame_layer` on every node + `schema_capabilities.layer_filter` (§2.11): a second zoom axis (layer) orthogonal to v1 depth (roots↔harvest).
- **D4** — new top-level `forcing_events[]` (§2.9): the exogenous pull/squeeze "weather" layer.
- **D5** — `schema_capabilities.graded_membership` (§2.11): graded membership in [0,1] is now the pervasive default.

**Removed / collapsed vs the v2 *draft* (hardening cuts — see §8):**
- `weld.people_0` is **no longer a storage field**. In v2, `actors[]` is the **single store** for the ground kernel; `roots.people_0` is removed (kept only as a documented rename: a v1 `people_0[]` entry becomes an `actors[]` entry with `kind: individual`). This eliminates the dual-home drift hazard.
- `weld_was_built_by` (prose alias of `mediating_wrapper`) **dropped** — one field, not two.
- Per-leaf `confidence` on `lifecycle.phase_trajectory[]` phases and on `weld_type[]` entries **dropped**: the `membership`/`weight` ∈ [0,1] *is* the graded value ("weights not hard values" — a confidence on a weight is a confidence on a confidence). Confidence stays on every *factual* leaf as in v1; only these two weight-fields shed the redundant second scalar.
- Added one small **optional `id`** convention (§2.0) so D2/D4 cross-references can be made checkable; defaults to reference-by-name (the v1 behavior).

---

## 0. What a "specimen" is (v1, with the v2 lifecycle reframing)

A **specimen** is **one merge event** — a single emergent wrapper `W_C` born from two parents — **rendered as a rooted, directed genealogy graph that STOPS AT THE PRESENT.** Where the Phase-1 DB stores one flat row per wrapper *class*, a specimen stores the whole *living tree* around one such birth:

- **DOWN** (roots, in the **physical** frame): the smaller sub-wrappers `W_C` is recursively made of, bottoming out in **people/actors** — the ground kernel "(0)" — standing in their time, place, environment, culture.
- **UP** (harvest, in the **latent + cultural** frame): the emergent children `W_C` went on to seed (new theories), plus its spill into art / sci-fi / tech.
- **WIDE** (relatives): cousins, influences, siblings spanning the physical AND the latent.

**The v2 reframing.** v1 rendered the weld as a single exposure. v2 renders it as a **lifecycle**: a weld has a graded life — pre-weld (independence | antagonism | complementarity) → conception/first-conjecture → welding (a *process*, not an instant) → consolidation **or** dormancy → revival (same | reinterpreted) → hardening **or** staleness — **or** it never resolves and lives as a *frontier* (rival candidate children, no winner). Three v1 properties become four:

1. **Frame-relativity** (v1). Every wrapper lives in a **frame** = the observer global kernels `{time, space, knowledge, meaning}`. Whether the parents make a third is frame-relative (two rocks in `space` = nothing; two rocks through `time` = strata).
2. **Fuzzy level-of-detail (LOD) / confidence** (v1, **deepened to D5**). Everything carries `confidence ∈ [0,1]` and a zoom/LOD depth — a **certain core** fading to a **probabilistic frontier** where conjectures live (a conjecture = a low-confidence weld drawn but not yet confirmed). v2 makes this **pervasive**: *every boundary* is graded (node membership, weld extent, actor role-strength, event influence, frame-layer straddle), and a crisp boundary is the special case (D5).
3. **Lifecycle** (NEW, D1). The weld is a graded trajectory through phases, each phase-membership a weight, plus a weighted **weld-type** classification. The certain core is just one frame of this life.
4. **Two-layer rendering** (NEW, D2+D3). Every node carries a `frame_layer ∈ {physical, latent, straddle}` (graded), and **actors** (generalized beyond people) are the explicit **bridge** between the two layers — *carriers* push latent wrappers UP, *inhabitants* live WITHIN other wrappers. The render is **filterable** on this axis (physical view vs latent view).

A specimen is therefore a *fuzzy genealogical render of one weld's whole life*, honest about where the record is solid and where it is conjecture, and renderable at either the physical or the latent layer.

---

## 0.1 (D2/D4 hardening) The optional `id` convention

Cross-references between layers — a `forcing_events[]` entry naming the weld it squeezed, an actor naming the wrapper it carries — must be **checkable**, but a heavyweight id system would violate the design law. v2 adopts the minimal rule:

> Any weld, sub-wrapper, candidate-child, descendant, relative, or actor **may** carry an optional `id` (a short slug, e.g. `"weld-main"`, `"act-fisher"`, `"cand-string"`). A reference field (`acted_on.target`, `carrier_of.wrapper`, `inhabitant_of.wrapper`, `weld_chain.weld_ref`, a discrepancy's `→ field` note) resolves **to an `id` if one is present, else to a `name` by string match.** Reference-by-name (the v1 behavior) remains valid and is the default; ids are added only where a specimen has enough interior cross-talk (Manhattan/Keynes/deep-learning) that name-matching would be ambiguous.

This keeps the sharp case id-free and bounds the "un-checkable name-soup" risk on the heavy cases.

---

## 1. The genealogy graph (informal shape — v2)

```
                       forcing_events[]   (war | depression | fashion | funding | politics | …)   ← D4: EXOGENOUS "WEATHER"
                  pull ↡↡↡        ↑↑↑ squeeze     (each event PULLS or SQUEEZES nodes/welds below)
   ────────────────────────────────────────────────────────────────────────────────────────────
                 cultural_harvest[]  (art | scifi | tech | other)                       ┐
                          ▲                                                              │ LATENT layer
        descendants[]  ───┼───  (new theories seeded by W_C)            ← HARVEST (UP)   │ (D3 filter:
                          ▲                                                              │  ideas/theories)
                   ┌──────────────┐                                                     │
   W_A  ──weld──►  │     W_C      │  ◄──weld──  W_B   ← MERGE EVENT (trunk)              ┘
 (parent)          │  (the child) │           (parent)         ⋮ lifecycle{} + weld_type[] (D1)
                   └──────────────┘             …or candidate_children[] (no winner, R6)
                          │
        sub_wrappers[]  ──┼──  (smaller wrappers W_C is made of)    ← ROOTS (DOWN)       ┐
                          │                                                              │ actors[] (D2)
                       actors[]   ← people + INSTITUTIONS/GOV/LABS/… ; the BRIDGE        │ are the bridge
                          │       (carrier-of ↑ latent ; inhabitant-of ⊂ other wrappers) │ physical↔latent
                       (ground kernel "(0)": who, where, when, culture)                 ┘ PHYSICAL layer
```

Plus, threaded across all of it:
- **`fuzzy_layer`** — partitions nodes/welds into `certain_core` (trunk) vs `frontier` (speculative roots + edges). **(D5 generalizes this to graded membership on every edge; the two-bin split is a DERIVED human digest of the per-node memberships, not an independent source of truth — §2.7.)**
- **`discrepancies[]`** — the real-record fuzzy frontier: priority disputes, contested genealogies, date/attribution conflicts, contested-dormancy narratives, and especially **framework-vs-record tensions** (the most valuable signal).
- **`sources[]`** — the citation backbone; every load-bearing field traceable here.

---

## 2. Field groups (the canonical specimen record — v2)

**Eleven** top-level groups: the **eight from v1** (`child`, `weld`, `roots`, `harvest`, `relatives`, `fuzzy_layer`, `discrepancies`, `sources`) **+ three new first-class groups** (`actors` [D2], `forcing_events` [D4], plus the header `schema_capabilities` block [D3+D5]). Within the eight, **R1–R16** are folded as optional sub-fields. Every leaf that asserts a fact carries (or inherits) a `confidence ∈ [0,1]`; nodes additionally carry an LOD/`depth` and a `frame_layer`. Bit-level MDL values stay **qualitative only** (§3, the `bits_note` discipline).

> **Reading convention.** A field marked **(v1)** is unchanged. **(R#)** marks a v2 refinement folded from `BATCH_FINDINGS.md`. **(D#)** marks a new-dimension field. All R# and D# fields are **OPTIONAL, default empty** (design law).

### 2.1 `child` — the emergent wrapper `W_C`

The thing born in this merge. The trunk node.

| field | type | meaning |
|---|---|---|
| `name` | string | **(v1)** canonical handle of `W_C`. |
| `kernel` | string | **(v1)** net product / what it essentially *is* (its localKernelCanon, Phase-1 sense). |
| `frame` | string[] ⊆ `{time,space,knowledge,meaning}` | **(v1)** which observer global kernel(s) `W_C` is rendered in. |
| `frame_layer` | object | **(D3)** `{layer: physical|latent|straddle, physical_membership ∈ [0,1], latent_membership ∈ [0,1]}`. A child theory is `latent` (≈1.0); defaults to `latent` for an idea-child. The render-filter key (§2.11, D3). |
| `status` | enum | **(v1, R5-extended)** one of `risen \| active \| dormant \| resurrected \| stale \| open-conjecture`. **R5 adds `open-conjecture`** (a.k.a. `live-unconsummated-weld`) for a high-synergy weld that never produced a settled child (QG). Observer-relative lifecycle position. |
| `status_trajectory` | array | **(R5)** OPTIONAL `[{state, when, by, confidence}]` — the child as a *trajectory* of states (Modern Synthesis: pluralist-1937 → hardened-1959 → contested-2007). Empty on a child whose status never moved. |
| `confidence` | number [0,1] | **(v1)** confidence that `W_C` is a real, distinct emergent (not a relabel of a parent / not a pile). **R9: INDEPENDENT of `weld.surprise_confidence` — see §3.4.** |
| `utility` | object | **(v1)** `{ unifier, compressor, action_spaces_unlocked[] }` — Pav's three utility legs as prose + an enumerated affordance list. |

### 2.2 `weld` — the merge (parents → child)

The edge that *is* the event. The heart of the specimen and the locus of the parents-produce-W_C test. **This is where most of R1–R16 and all of D1 land.**

#### 2.2.a Parents (R1, R4) — N-ary + a mediating welder + parent kinds

| field | type | meaning |
|---|---|---|
| `parents` | array of 2 | **(v1, kept)** `[W_A, W_B]`, each `{ name, kernel, frame[], confidence }`. **The clean binary projection — the framework's canonical visualization. Always present.** |
| `parents_full` | array (n-ary) | **(R1)** OPTIONAL the honest N-ary parent set, each `{ name, kernel, frame[], confidence, parent_kind, frame_layer }`. Maxwell ≈ 7; Darwin+Mendel = 2 roots + synthesizers. **Empty when the 2-projection is faithful.** When present, `parents` is the declared 2-projection *of* this set. |
| `parent_kind` (per parent) | enum | **(R4)** `content \| method \| instrument`. Maxwell's EM *content* (Faraday) vs the mechanical-analogy *method* (Thomson) vs the calibration-*target* instrument (Fizeau's light-speed). Default `content`. Reused for `sub_wrappers` and QG's tooling roots. |
| `mediating_wrapper` | object | **(R1)** OPTIONAL `{ name, kernel, who_or_what, confidence }` — the agent that *performed* the weld when it is **not one of the parents** but sits a layer up (population genetics / Fisher-Haldane-Wright welded Darwin+Mendel; the Maxwellians welded birth-2). Empty when a parent welds itself. |

#### 2.2.b The seam and the surprise (R12, R9, R15, R16)

| field | type | meaning |
|---|---|---|
| `shared_sub_object_S` | string | **(v1)** the **seam** the parents fused along (the `S` of the pushout; the "nesting space / Venn-lens"). |
| `S_structure` | object | **(R12)** OPTIONAL `{ components[], internal_conflict?: string, agreed: bool }` — S may be **non-unitary / itself contested**. Darwin+Mendel's S (population genetics) was internally fractured by the Fisher–Wright controversy (`agreed:false`); QG's S is multi-faceted but agreed (`agreed:true`). The `agreed` flag distinguishes a *fractured-and-contested* seam from a *multi-faceted-but-agreed* one. Empty when S is one coherent object. |
| `surprise` | string (PROSE) | **(v1)** what `W_C` does that **neither parent predicts alone** — the synergy. Prose, not a number. |
| `surprise_confidence` | number [0,1] | **(v1, R9-emphasized)** confidence the surprise is real synergy (vs additive blend). **R9: ORTHOGONAL to `child.confidence`.** QG: surprise_confidence 0.85 while child.confidence 0.40 — a maximally fertile seam with an unborn child. Never tie one to the other (§3.4). |
| `surprise_priority` | object | **(R15)** OPTIONAL `{ first_conjectured_by, when, dormant_interval?, confidence }` — the **conjecture-in-a-parent**. Faraday's 1846 "light is a vibration of the lines of force" pre-existed the quantitative weld by ~15 years as a low-confidence weld drawn-but-not-confirmed inside W_A. Empty when the surprise is born with the weld. |
| `bits_note` | string (QUALITATIVE ONLY) | **(v1, R16-extended)** a qualitative note on description-length / synergy-in-bits. **R16:** may be explicitly `"principled-null"` for a frontier weld (you cannot MDL-score a theory you do not have). **Do NOT fabricate bit values.** See §3. |

#### 2.2.c What crossed the weld (R7)

| field | type | meaning |
|---|---|---|
| `survived` | string[] | **(v1)** parent features that persisted into `W_C` (the "stubs" / procedural roots that live on). |
| `dropped` | string[] | **(v1)** parent features lost / not carried through. |
| `feature_ledger` | array | **(R7)** OPTIONAL `[{ feature, kept_by[], dropped_by[] }]` — the **per-candidate** survived/dropped matrix, needed when one weld has multiple candidate children that drop *different* parent-features (string drops GR's background-independence; LQG drops QM's fixed external time). Empty when a single child makes flat `survived[]`/`dropped[]` sufficient. |

#### 2.2.d Frame and zoom (R13, R3)

| field | type | meaning |
|---|---|---|
| `frame_of_weld` | string[] ⊆ `{time,space,knowledge,meaning}` | **(v1)** the frame(s) in which the weld actually holds (may differ from the child's own frame; e.g. a weld that only holds through `time`). |
| `weld_operator` | string | **(R13)** OPTIONAL the **active frame-ingredient** — not just *which* frame but *what in it does the welding*. Maxwell: "the time-derivative (displacement current) / induction-loop closure" — time is the active operator, not a passive backdrop. Empty when no single operator is identifiable. |
| `lod_scale` | string | **(v1)** at what zoom/resolution the weld holds (prose). |
| `sub_welds` | array | **(R3)** OPTIONAL ordered `[{ id?, name, when, confidence }]` — one weld at coarse grain is a **chain/family of sub-welds** zoomed in (Maxwell: Ørsted → Faraday-induction → displacement-current → Maxwellian compression → Hertz). Empty when the weld is atomic at all useful zooms. |
| `coherence_under_zoom` | enum | **(R3)** OPTIONAL `confirms \| contradicts` — **the cross-cut's signature diagnostic.** A healthy weld is *confirmed* by its sub-structure at higher zoom (sharp/dormant); an unconsummated weld is *contradicted* by it (QG shatters into mutually-rejecting sub-welds). Empty (≈`confirms`) on a sharp case. |

#### 2.2.e When (R2)

| field | type | meaning |
|---|---|---|
| `when` | string **or** object | **(v1, R2-extended)** v1 string still valid for a dated merge. **R2:** may be `{ from, to \| null, defensible_dates[] }` — a weld is a *process* with a duration. A **null `to`** marks an open/unconsummated weld (QG: 1916 → present) and is itself diagnostic. Darwin+Mendel: a ~30-year process (1918–1950) with several defensible birth-dates. |

#### 2.2.f Non-resolution (R6, R8) — the frontier case

| field | type | meaning |
|---|---|---|
| `candidate_children` | array | **(R6)** OPTIONAL `[{ id?, name, what, frame[], frame_layer, confidence, drops[], keeps[] }]` — a weld with **competing, mutually-rejecting outputs and no winner.** QG: string / LQG / causal sets / CDT / asymptotic safety — the *same* two parents + *same* seam yielding rival children that **disagree about what the child is** (they behave like lateral rivals, not `descendants`). The single biggest v1 gap. **Empty on any resolved weld.** |
| `unresolved` | bool | **(R6)** OPTIONAL `true` when `candidate_children` has no winner. Default `false`. |
| `contest_axis` | string | **(R6)** OPTIONAL the axis the candidates disagree along — *which-parent-dominates* / *background-dependent-vs-independent* (QG). Empty unless `unresolved`. |
| `weld_necessity_confidence` | number [0,1] | **(R8)** OPTIONAL **"is a third even NEEDED?"** — the falsifier-of-the-weld. A serious minority (semiclassical gravity) holds `W_C` may be a category error (no child). **Empty ⇒ read as 1.0** (the design-law default); `< 1` only on a frontier where the weld itself is in doubt. |

#### 2.2.g Dormancy & revival (R10, R11)

| field | type | meaning |
|---|---|---|
| `dormancy_intervals` | array | **(v1, R11-extended)** `[{ from, to, why, why_frame }]`. **R11:** `why_frame ⊆ {time, space, knowledge, meaning, physical/political}` — a lineage can be cut by a **purge** (physical: Bronstein executed by the NKVD, 1938) as well as by a **theorem** (knowledge: QG no-go results; Mendel's blending-orthodoxy misreading). Default: `why_frame` empty ⇒ inferred from `why`. **NOTE (D4):** when the dormancy was caused by an *external* event, record the event once in `forcing_events[]` and let `why_frame` name only the frame — do not restate the event narrative here. |
| `revival` | object | **(v1, R10-extended)** `{ when, by, trigger, kind }`. **R10:** `kind: same \| reinterpreted` — a revival can *re-frame* the dormant object rather than wake it (Mendel did species-hybridization; revived as heredity). Default `same`. |
| `reattribution` | object | **(R10)** OPTIONAL `{ named_after, actually_produced_by, why }` — the canonical **name attaches to the wrong node.** "Maxwell's equations" (4-eqn vector form) were forged by the Maxwellians 1879–94; Maxwell left 20 coupled equations. Empty when name = producer. |
| `weld_chain` | array | **(R10)** OPTIONAL `[{ birth_label, weld_ref }]` — lets a `weld` **CHAIN**: birth-1's `W_C` becomes a parent of birth-2 (Maxwell's raw form → welded with vector analysis + Hertz's confirmation → the form we use). Empty on a single-birth weld. |

#### 2.2.h `lifecycle` (D1) — the weld's graded life, first-class

**(D1)** OPTIONAL object making the weld's life a **first-class, weighted** structure rather than scattered across `dormancy_intervals`/`revival`/`status`. Three sub-parts — a **graded phase trajectory**, a **pre-weld relationship**, and a **weighted weld-type classification**. **Empty/collapsed on a clean sharp weld** (which is simply "consolidated, membership ≈1.0").

```
lifecycle: {
  phase_trajectory: [          // a GRADED trajectory, NOT an enum — phases overlap and carry weights
    { phase, membership ∈ [0,1], from, to|null, note }
  ],
  // controlled (extensible) phase vocabulary, in canonical order:
  //   pre_weld:{independence|antagonism|complementarity}  → conception/first_conjecture
  //   → welding(process)  → consolidation | dormancy  → revival:{same|reinterpreted}
  //   → hardening | staleness     OR    never_born_frontier:{candidate_children, unresolved}
  // phase_trajectory is the SAME shape as status_trajectory (R5) and when-as-interval (R2);
  //   it is the WELD's life, where status_trajectory is the CHILD's life after the weld.

  pre_weld_relationship: {     // (R14) the parents' relationship BEFORE the weld — a weighted classification
    kind,                      //   antagonism | independence | complementarity
    membership ∈ [0,1],        //   Mendelism was an ANTI-Darwinian weapon (~1900–15) before Fisher welded them
    note
  },
  // NOTE: the pre_weld:* entry in phase_trajectory and this pre_weld_relationship sub-object
  //   describe the SAME fact at two grains. Record the relationship HERE (it carries the kind
  //   + membership cleanly); the phase_trajectory pre_weld entry, if present, just marks WHEN.
  //   Do not double-record the antagonism strength in both places.

  weld_type: [                 // (D1) WEIGHTED classification — a weld may be several types at once,
                               //   each with a weight (weights, not hard values — per Pav)
    { type, weight ∈ [0,1], note }
  ]
  // weld_type CORE controlled vocabulary (the ratified closed set; extend only via a discrepancy row, see §6):
  //   unifier-weld                     (Maxwell: E+M → EM; the classic)
  //   re-weld / re-attribution         (Maxwell birth-2: the Maxwellians' 4-eqn form, mis-named)
  //   antagonism-then-fusion           (Darwin+Mendel: biometrician–Mendelian war → Modern Synthesis)
  //   instrument-enabled-weld          (a weld a new instrument made possible; Fizeau's c as enabler)
  //   mediator-welded                  (welded by a non-parent layer up: population genetics; the Maxwellians)
  //   state/war-mobilized-weld         (Manhattan Project: war mobilizes the weld)
  //   crisis-pulled-weld               (Keynesianism: the Depression pulls the theory into government)
  //   never-consummated-frontier-weld  (QG: rival children, no winner)
}
```

- **`phase_trajectory` and `weld_type` carry weights, not a second confidence.** The `membership`/`weight` ∈ [0,1] *is* the soft value (per Pav, "the classifiers have weights, not hard values"). A weld is rarely purely one type; record the mixture with weights.
- **Cross-references** (so v2 stays one organism, not parallel silos): `phase_trajectory` consumes `dormancy_intervals`/`revival`/`when`; `pre_weld_relationship` is R14; `never_born_frontier` consumes `candidate_children`/`unresolved` (R6); `re-weld` consumes `reattribution`/`weld_chain` (R10). **`lifecycle` is the graded, weighted INDEX over** these existing fields — it does not duplicate their content. (Ratification choice flagged in §6, item 1: keep-both vs collapse vs derive.)
- **Default:** a sharp settled weld leaves `phase_trajectory` empty (≡ a single `consolidation` phase at membership 1.0), `pre_weld_relationship` = `complementarity`, and `weld_type` = `[{unifier-weld, 1.0}]`.

### 2.3 `roots` — DOWN, the physical frame (v1 + R4 + D3)

The recursive descent from `W_C` toward people and place. **Confidence and LOD fade as you go deeper.**

- **`sub_wrappers`** : array of `{ id?, name, kernel, frame, depth, confidence, who_called_it, parent_kind (R4), frame_layer (D3) }` — the smaller wrappers `W_C` is built from, recursively down. `depth` = levels below `W_C`. **R4** lets a sub-wrapper be tagged a *method* root (vector calculus; QG's spin networks / Calabi-Yau / knot theory) vs a *content* root. **D3** lets it declare `physical`/`latent`.
- **The ground kernel "(0)" now lives in `actors[]` (§2.6), not here.** In v1 the people-roots lived in `roots.people_0`; in v2 they are the `kind: individual` subset of the top-level `actors[]` group, so a person who *carries* a theory and *inhabits* a paradigm is recorded once with both bridge-roles. (Migration: a v1 `people_0[]` entry → an `actors[]` entry with `kind: individual`.)

### 2.4 `harvest` — UP, the latent + cultural frame (v1 + D3)

What sat *on top of* `W_C` and what it spilled into. The tree grows up to the present here. **All harvest nodes are `frame_layer: latent` by default (D3).**

- **`descendants`** : array of `{ id?, name, what, frame, confidence, frame_layer }` — emergent children: new theories `W_C` (crossed with others) seeded.
- **`cultural_harvest`** : array of `{ domain: art|scifi|tech|other, what }` — the spill into culture.

### 2.5 `relatives` — WIDE edges (v1, unchanged; still flagged for ratification)

Array of `{ id?, name, relation: cousin|influence|sibling|rival, frame[], confidence, note, frame_layer }`. Lateral edges spanning the physical AND the latent. **(D3 adds `frame_layer`.)** *v1 §5 flag 2 stands: confirm whether WIDE relatives are first-class or fold into roots/harvest/discrepancies.* A **defeated rival framework** (Weber electrodynamics) lives here as `relation: rival`; this + `feature_ledger` partly meets the v1-flagged "superseded_rivals[]" need.

### 2.6 `actors` (D2) — NEW first-class group: actors generalized beyond people

**(D2)** The generalization of v1's `people_0` from individuals to **institutions, governments, labs, journals, companies, movements, fields, universities, states.** Actors are the **BRIDGE between the physical and the latent layers** (D3): *carriers* push latent wrappers UP; *inhabitants* live WITHIN other wrappers. **`actors[]` is the single store for the ground kernel "(0)"** (the v1 `roots.people_0` is folded in here as the `kind: individual` view).

Each actor node:

```
actors: [
  {
    id,                         // OPTIONAL slug (§0.1) so carrier_of/inhabitant_of/forcing refs resolve cleanly
    name,
    kind,                       // (D2) controlled vocabulary, extensible:
                                //   individual | institution | university | journal | company |
                                //   government | state | movement | field | lab
    frame_layer: {              // (D3) actors typically STRADDLE — that is the point of D2
      layer: physical | latent | straddle,
      physical_membership ∈ [0,1],   // a government/lab is strongly physical
      latent_membership ∈ [0,1]      // a movement/field leans latent
    },

    // --- the (0) ground-kernel fields, kept from v1 people_0 (apply mainly to kind:individual) ---
    role, when, where, culture, relation,   // relation: originator|transmitter|patron|rival|popularizer|funder|…
    confidence,

    // --- D2's TWO role-relations: the bridge ---
    carrier_of: [               // (D2-i) CARRIER / CHAMPION-OF: the latent wrappers it carries/pushes/advocates
      { wrapper, role: champions|founds|funds|popularizes|institutionalizes,
        strength ∈ [0,1], when, confidence }
    ],                          //   an actor champions MULTIPLE latent wrappers; carriers point UP into the latent
    inhabitant_of: [            // (D2-ii) INHABITANT / OPERATOR-OF: the latent AND physical wrappers it lives/operates inside
      { wrapper, layer: physical|latent, role: operates_in|lives_in|works_within,
        strength ∈ [0,1], when, confidence }
    ]                           //   a paradigm, a nation, a university, an era; inhabitants point WITHIN other wrappers
  }
]
```

- **The bridge thesis:** the physical layer (people, labs, governments, places) and the latent layer (ideas, theories, paradigms) are connected *through actors*. A person (physical) **carries** a theory (latent) UP; that same person **inhabits** a paradigm (latent) and a nation (physical). Fisher (individual) carried population genetics UP and inhabited the Galton-lab/biometrician milieu; the Manhattan Project (institution/government) carried fission-weapon physics UP and inhabited the wartime US state; a corporate/university AI lab carries connectionism UP and inhabits a compute/funding regime.
- **`carrier_of` is one-to-many:** an actor champions *multiple* latent wrappers (Maxwell carried EM *and* statistical mechanics).
- **Reference discipline (§0.1):** `carrier_of.wrapper` / `inhabitant_of.wrapper` resolve to an in-graph `id`/`name` when the wrapper is a node in *this* specimen, else they are a free-string reference to a wrapper outside the rendered tree (allowed, but flagged in §6 item 3).
- **Default on a sharp case:** fill `actors[]` exactly as v1 filled `people_0` (individuals, with `role/when/where/culture/relation`); leave `carrier_of`/`inhabitant_of`/non-individual kinds **empty** unless an institution/government/lab is genuinely load-bearing (it is for Manhattan / Keynes / deep learning; largely *not* for Maxwell — which is the point of the design law).

### 2.7 `fuzzy_layer` — the LOD / confidence partition (v1 + D5)

Makes the trunk-vs-frontier split explicit, as a **derived digest** of the per-node memberships.

- **`certain_core`** : string[] — **(v1)** high-confidence nodes/welds (the trunk).
- **`frontier`** : string[] — **(v1)** low-confidence / speculative / conjectural nodes/welds/branches (the cultivation zone).
- **`core_boundary_locus`** : string — **(R3-adjacent)** OPTIONAL *where in the tree* the certain-core/frontier boundary falls — itself a confidence-thermometer for the weld. Sharp: core at the trunk, fuzz in roots/edges. Dormant: fuzz climbs *into* the trunk (parent-identity contested). Frontier: core *sinks below* the child, the whole crown is frontier. Empty on a textbook sharp case.

**(D5) Graded-by-default note.** The two-bin `certain_core`/`frontier` lists are a human-readable **summary that is DERIVED from** the per-node/per-edge `confidence`/`membership` already on every field — the memberships are the ground truth; the two-bin digest is a curated reading of them and must not be treated as an independent source (§6 item 6).

### 2.8 `discrepancies` — the real-record frontier (v1, `type` extended)

Array of `{ what, sources_in_conflict, type, why_interesting, confidence_impact }`, where `type ∈ [priority-dispute, contested-genealogy, date/attribution-conflict, framework-vs-record-tension, dormancy-contested, whig-vs-revisionist]`.

- **`framework-vs-record-tension`** remains the highest-value type. **In v2, a tension that motivated a new field should also name the field** (e.g. "→ motivates `candidate_children` (R6)") so the discrepancy log stays the schema's own change-driver. Several v1 multi-parent tensions are now *absorbed* by `parents_full`/`mediating_wrapper` (R1) and no longer need a discrepancy row — record only the *residual* tension.
- **A new weld-type or phase-vocabulary term must be PROPOSED here before use** (§6 item 7): a `framework-vs-record-tension` row naming the new term + why the core set could not hold it.
- **Exogenous-tension note (D4):** a discrepancy may flag a *forcing-vs-internal* tension (was the weld pulled by a war/depression or by its own logic?) — cross-reference the relevant `forcing_events[]` id.

### 2.9 `forcing_events` (D4) — NEW first-class group: external pull/squeeze influence events

**(D4)** A first-class **EXOGENOUS-FORCING layer**: events OUTSIDE the idea-genealogy that **PULL** (accelerate / fund / elevate) or **SQUEEZE** (suppress / starve / redirect / kill) welds and lineages. The "weather/climate" over the genealogy — sitting *above* the tree and acting *down* onto it.

```
forcing_events: [
  {
    id,                         // OPTIONAL slug (§0.1)
    name,                       // e.g. "WWII", "the Great Depression", "the AI winters", "Bronstein's NKVD execution"
    kind,                       // (D4) controlled vocabulary, extensible:
                                //   war | fashion | cultural-focus | funding | politics |
                                //   economic-crisis | technology | religion
    direction,                  // pull | squeeze | both
    acted_on: [                 // which nodes/welds/actors/lineages it forced (by id else name, §0.1)
      { target, target_kind: weld|child|actor|sub_wrapper|lineage|candidate_child,
        effect: accelerate|fund|elevate|suppress|starve|redirect|kill,
        strength ∈ [0,1] }      // (D5) graded — an event's influence is a membership, not binary
    ],
    when,                       // a date or interval (may reuse the R2 {from,to} shape)
    mechanism,                  // HOW it pulled/squeezed (prose): "wartime funding + secrecy + concentration of physicists"
    confidence
  }
]
```

- **Known instances (seeds for the three new specimens):**
  - **Bronstein's NKVD execution (1938)** — `kind: politics`, `direction: squeeze`, `effect: kill`, acted_on a *root lineage* of QG. The starkest physical-frame squeeze in the batch; the *external cause* of the `why_frame: physical/political` dormancy of §2.2.g.
  - **WWII** — `kind: war`, `direction: pull`, acted_on the Manhattan Project weld (`effect: accelerate`, strength ≈1.0): a crisis-pulled ultra-fast weld.
  - **The Great Depression** — `kind: economic-crisis`, `direction: both` (squeezed laissez-faire orthodoxy, pulled Keynesian theory into government), acted_on the Keynesian weld AND the actor "national governments" (which became carriers of the theory).
  - **The AI winters** — `kind: funding` (+ `fashion`), `direction: squeeze`, acted_on connectionism's lifecycle as repeated dormancy cycles; the compute/funding/fashion *pull* of the 2010s is the inverse event.
- **Why first-class (not a discrepancy or a dormancy `why`):** the *same* event often forces *multiple* nodes (WWII pulled the Manhattan weld AND squeezed European basic science AND redirected a generation of physicists), and pull/squeeze is a *recurring driver type* across specimens (the "weather"), not a one-off note. It connects to D2: a forcing event often acts *through* an actor (a government funds via a lab).
- **Default on a sharp case:** `forcing_events: []`. Maxwell's EM had no load-bearing exogenous forcing (the design law: empty is correct). The three new specimens exist precisely to populate this layer.

### 2.10 `sources` — the citation backbone (v1, unchanged)

Array of `{ name, type, url, what_used_for, reliability }`, where `type ∈ [aggregator, encyclopedia, scholarly-history, primary]` and `reliability ∈ [0,1]` (or a labelled band).

> **Harvest discipline (carried forward):** consult the WEB, do **not** work from memory; cite real sources; mark uncertain claims low-confidence. Aggregators: **Wikidata** (influenced-by, discoverer, field-of-work, dates, place), **OpenAlex**, **SEP**/**IEP**, Wikipedia "history of …" sections, the **Mathematics Genealogy Project**, **nLab**, **Semantic Scholar/Google Scholar** citation lineage, named **scholarly histories**. For the three new specimens the actor/forcing layers (D2/D4) add: government/agency archives (Manhattan: AHF/DOE histories), economic-history sources (Keynes: the General Theory's reception, the 1930s–70s policy record, Skidelsky), and AI-history sources (connectionism: Rosenblatt 1958, Minsky-Papert 1969, Rumelhart-Hinton-Williams 1986, the two AI-winter literatures, AlexNet 2012, "Attention Is All You Need" 2017). Mark discrepancies, **especially framework-vs-record tensions.**

### 2.11 `schema_capabilities` (D3 + D5) — declared render capabilities (header block)

**(D3 + D5)** A small declared-capabilities block (carried in the header, §2.12) announcing what a v2 render *supports*, so consumers (and a future renderer) can rely on it:

```
schema_capabilities: {
  layer_filter: {                 // (D3) the render is FILTERABLE on the physical/latent axis
    supported: true,
    axes: ["physical", "latent"],
    bridge_via: "actors",         // actors are the explicit bridge between the two layers
    note: "A render may show the PHYSICAL view (actors, institutions, places, events) OR the
           LATENT view (ideas, theories, sub-wrappers); every node declares frame_layer; actors
           straddle and connect the two."
  },
  graded_membership: {            // (D5) FUZZY EDGES BY DESIGN
    supported: true,
    default: "graded",            // a crisp boundary is the SPECIAL case, not the default
    applies_to: ["node membership", "weld extent (sub_welds)", "actor role-strength (carrier/inhabitant)",
                 "forcing-event influence (acted_on.strength)", "frame-layer straddle (physical/latent membership)",
                 "lifecycle phase membership", "weld_type weight"],
    note: "Every boundary is a membership/confidence in [0,1]; the certain core is just where
           membership ≈ 1.0. Crisp = the membership happens to be ~0/1."
  }
}
```

- **D3 (physical/latent LOD filter):** the genealogy can be rendered at the **physical** layer (actors, institutions, places, forcing events) or the **latent** layer (ideas, theories, sub-wrappers), with **actors the explicit bridge.** Every node's `frame_layer` is the filter key. This is *zoom on a new axis*: not just depth (roots↔harvest) but layer (physical↔latent). **Status:** declared but not yet exercised by a renderer — the three new specimens should at minimum be **hand-checkable** under each filter (§6 item 5).
- **D5 (fuzzy edges by design):** graded membership is the **pervasive default.** A crisp boundary is recorded as a membership that *happens* to be ~0 or ~1 — never as a special "this one is crisp" type.

### 2.12 specimen header (top-level metadata — v1 + v2 additions)

| field | type | meaning |
|---|---|---|
| `schema_version` | string | e.g. `"0.2-canonical-genealogy"`. |
| `specimen_id` | string | stable slug (e.g. `manhattan-project`, `keynesian-economics`, `deep-learning`). |
| `_status` | string | the Tier-3 working-not-canon disclaimer (carried in-record). |
| `extends` | object | linkage back to the Phase-1 class row this specimen instantiates (§5). |
| `generated` | string (date) | authoring date. |
| `frames_present` | string[] | union of all `{time,space,knowledge,meaning}` frames used (convenience index). |
| `layers_present` | string[] | **(D3)** union of `frame_layer`s used — `["physical","latent"]` when both are populated. New in v2. |
| `overall_confidence` | number [0,1] | confidence in the specimen as a whole — **always read paired with `fuzzy_layer` (a split aggregate, never a flat scalar).** |
| `schema_capabilities` | object | **(D3+D5)** the declared-capabilities block of §2.11. |

---

## 3. The fuzzy-LOD / confidence layer (how to read the numbers — v1 §3 + R9/R16)

### 3.1 (v1) `confidence ∈ [0,1]` is everywhere and is SOFT.
A claim near the trunk (the merge event, the two named parents, the date) should be high (≈0.8–1.0); a deep root or a wide edge should be low (≈0.2–0.5) and may live in `fuzzy_layer.frontier`.

### 3.2 (v1) LOD / `depth` is a zoom coordinate.
Zooming in on the trunk reveals more certain structure; zooming into roots/edges reveals the probabilistic frontier. **R3 adds a second zoom axis at the weld:** `sub_welds[]` + `coherence_under_zoom` record whether higher zoom *confirms* or *contradicts* the weld. **D3 adds a third axis:** the physical↔latent layer (§2.11).

### 3.3 (v1, R16) Bits stay qualitative.
`weld.bits_note` and the `compressor` utility leg describe description-length *qualitatively* only. **MDL-in-bits is a LATER step** needing latent embeddings — do **not** fabricate numeric bit values. **R16:** on a frontier the value may be a **principled null** (`bits_note: "principled-null"`) — you cannot MDL-score a theory you do not have; the blank is *intrinsic*, not deferred.

### 3.4 (R9 — the deepest correction) `surprise_confidence` ⟂ `child.confidence`.
**These are ORTHOGONAL axes and must be allowed to diverge sharply.** The v1 schema and Phase-1 logic implicitly tied high synergy to a *risen* child. QG breaks it: `surprise_confidence` 0.85 (the synergy is real — graviton-in-the-string-spectrum, S=A/4) while `child.confidence` 0.40 (the child is unborn after 90 years). **A seam can be maximally fertile and still birth no single child.** Never read one off the other. (This is why `weld_necessity_confidence` (R8) and `candidate_children` (R6) exist — a fertile-but-unborn weld is a normal, recordable state.)

### 3.5 (v1) The frontier is generative, not a defect.
Low-confidence welds in `fuzzy_layer.frontier` are the **conjecture-cultivation surface.** Recording them (with honest low confidence) is the point. The frontier is most generative where the trunk is weakest (QG's whole rival-children canopy).

### 3.6 (v1, D5) Frame-relativity AND layer-relativity interact with confidence.
A weld may be high-confidence in one frame and `∅`/NULL in another (rocks: `time` PASS, `space` NULL → record in `frame_of_weld`). **D5:** likewise every *boundary* is graded — a node may be 0.7-physical/0.4-latent (straddle); an actor's `carrier_of` strength is a membership; a forcing event's `acted_on.strength` is a membership. **Graded is the default; crisp is the membership-≈0/1 special case.**

---

## 4. The five new dimensions D1–D5 — design rationale (the v2 thesis)

A compact statement of *why* each new dimension is first-class and *how* it preserves the design law.

- **D1 — Weld lifecycle + type classification (`weld.lifecycle`, §2.2.h).** v1 rendered a weld as a photograph; the three specimens proved it is a *process with a life*. D1 makes the **lifecycle a graded trajectory** (phases with memberships, not an enum) and the **weld-type a weighted classification** (a weld is often several types at once). It does not duplicate `dormancy_intervals`/`revival`/`status`/`candidate_children` — it is the **weighted index over** them. *Design law:* a sharp weld collapses to one `consolidation` phase (1.0) + `weld_type:[{unifier-weld,1.0}]`; the trajectory array is empty.

- **D2 — Actors generalized (`actors`, §2.6).** v1's `people_0` could only hold individuals. D2 generalizes to **institutions/governments/labs/journals/companies/movements/fields/universities/states**, with **two role-relations** — `carrier_of` (champions latent wrappers UP) and `inhabitant_of` (operates WITHIN other wrappers). Actors become the **explicit bridge** between the physical and latent layers (D3). *Design law:* `actors[]` *is* v1's `people_0` for `kind:individual`; non-individual kinds and the two relations default empty and only fill where an institution is load-bearing.

- **D3 — Physical/latent LOD filter (`frame_layer` on every node + `schema_capabilities.layer_filter`, §2.11).** v2 adds a **second zoom axis**: not just depth (roots↔harvest) but **layer** (physical↔latent). Every node declares `frame_layer ∈ {physical, latent, straddle}` (graded); a render can show the **physical view** or the **latent view**, with **actors the bridge.** *Design law:* an idea-child defaults `latent`; a person defaults `physical`; the filter is free on a specimen that does not care about the split.

- **D4 — External pull/squeeze forcing events (`forcing_events`, §2.9).** A first-class **exogenous layer** — wars, depressions, fashions, funding, purges — that **pull** or **squeeze** welds and lineages: the "weather" over the genealogy. Lifted out of v1's `dormancy.why` string because one event forces *many* nodes and pull/squeeze is a recurring *driver type*. Often acts *through* an actor (D2). *Design law:* `forcing_events:[]` on a case with no load-bearing exogenous forcing (Maxwell).

- **D5 — Fuzzy edges by design (graded membership pervasive; `schema_capabilities.graded_membership`, §2.11).** v2 leans all the way in: **every boundary is graded** — node membership, weld extent, actor role-strength, forcing-event influence, frame-layer straddle, lifecycle phase membership, weld-type weight — each a value in [0,1]. **A crisp boundary is the special case (membership ≈0/1), not the default.** *Design law in its purest form:* the certain core is *defined* as where membership ≈ 1.0; D5 declares that the [0,1] grading already pervading the schema is the *norm*, and the schema's own thin-core/expressive-frontier shape is just the membership field at work.

---

## 5. How v2 EXTENDS Phase-1 and relates to v1 (the mapping is preserved)

**Same organism, deeper zoom — and now a second (physical/latent) axis.** The v1 mapping to `latent_olympics_data/wrapper_classes_phase1.json` is unchanged: a specimen's `child` ↔ one Phase-1 `wrapper_classes[]` row; its `weld` ↔ the frame-indexed, per-node-confidence render of one `overlaps[]` edge; its `roots`/`harvest` make explicit the procedural-lineage tree; its `fuzzy_layer` + per-node `confidence` are the per-node generalization of the single-row `classifierWeights`; its `frame[]` operationalizes `observerRelative:true`. v2 adds:

| | Phase-1 row | v1 specimen | **v2 specimen** |
|---|---|---|---|
| **weld** | one typed `overlaps[]` edge | a pushout (parents→S→W_C) + surprise + dormancy/revival | **+ a graded lifecycle & weighted weld-type (D1); + N-ary parents & a mediating welder (R1); + non-resolution machinery (R6/R8)** |
| **actors** | implicit in `origin` | `people_0` (individuals) | **generalized `actors[]` (institutions/gov/labs) as the physical↔latent bridge (D2)** |
| **layer** | — | implicit (roots=physical, harvest=latent) | **explicit `frame_layer` per node + a filterable physical/latent render (D3)** |
| **exogenous drivers** | — | buried in `dormancy.why` strings | **first-class `forcing_events[]` pull/squeeze layer (D4)** |
| **fuzziness** | one soft score per class | per-node confidence + two-bin certain_core/frontier | **graded membership on *every* boundary as the default (D5)** |

`extends` (header) still points back to the Phase-1 row. A v2 specimen does not restate `classifierWeights`; it refines them with per-node confidence, graded memberships, and (later) real bits.

---

## 6. Underspecified / flagged for ratification (v2 schema gaps + self-flagged weaknesses)

v1's flags 1–6 **carry forward** (header field names; `relatives` first-class-ness; per-node confidence vs `fuzzy_layer`; `frame_of_weld` vs `child.frame`; `bits_note` string-only; multi-parent reality — flag 6 now *largely resolved* by `parents_full`/`mediating_wrapper` R1, leaving only the residual "which 2-projection is canonical" choice). **New v2 items:**

1. **`lifecycle` (D1) overlaps `dormancy_intervals`/`revival`/`status`/`candidate_children`.** Drafted as a *weighted index* over these, not a replacement — a ratifier must decide (a) keep both (index + primitives, as drafted), (b) collapse the primitives *into* `lifecycle`, or (c) make `lifecycle` purely derived (computed, never authored). Drafted as (a) for backward-compatibility. **This is the single most likely place a filler double-records;** the §2.2.h cross-reference rules and the §7 discipline ("`lifecycle` indexes, does not restate") are the mitigation until ratified.
2. **`actors` is now the single store; `roots.people_0` is removed (RESOLVED in v2).** The draft's dual-home drift hazard is closed: v2 has one store (`actors[]`) and a documented migration (v1 `people_0[]` → `actors{kind:individual}`). Flagged only so the three existing v1 specimens get re-homed on their next edit.
3. **`carrier_of`/`inhabitant_of` may reference wrappers not in *this* specimen (D2).** The §0.1 convention resolves an in-graph reference to an id/name; an out-of-graph reference is an allowed free-string. **Residual risk:** out-of-graph references can still accrete into an un-checkable name list — ratify whether out-of-graph carrier references are wanted, or should be promoted to a `relatives[]` node first.
4. **Cross-layer references rest on the optional `id` convention (§0.1, partial RESOLUTION).** v2 adds a minimal optional `id` so `forcing_events.acted_on.target`, `carrier_of`/`inhabitant_of`, `weld_chain.weld_ref`, and discrepancy `→ field` notes resolve cleanly. Ratify whether ids should be **required** on heavy specimens (Manhattan/Keynes/deep-learning) or remain optional everywhere.
5. **D3 layer-filter is declared but exercised by no renderer.** `frame_layer` + `schema_capabilities.layer_filter` are capability claims; the real test is a render that shows physical-only vs latent-only. **The three new specimens should at minimum be hand-checkable under each filter** (every node's `frame_layer` populated, actors straddling).
6. **D5 grading vs the two-bin `fuzzy_layer` (clarified in v2).** `certain_core`/`frontier` is explicitly a **DERIVED digest** of the per-node memberships (§2.7), not an independent source of truth. Confirm the digest is wanted (it aids reading) and accept that it can fall out of sync — the memberships win.
7. **Weld-type and phase vocabularies are extensible controlled vocabularies (D1).** v2 ratifies a **CORE closed set** (the 8 weld-types in §2.2.h) and requires that **any new term be proposed in a `discrepancies` row before use** (§2.8). This bounds vocabulary drift across sibling-agent renders.
8. **The three new specimens are calibration instruments, not validation.** Chosen to hammer D1–D5 (Manhattan = institutions+gov+war at max; Keynes = crisis-squeeze-into-government + multi-cycle dormancy/reinterpretation; deep learning = AI-winter dormancy cycles + corporate/lab/gov actors + compute/funding/fashion forcing). Like the v1 batch, each new dimension rests on a **small N** and is a **well-motivated conjecture pending a second instance of the same stressor.** This is a forward design; **rendering the specimens may force revisions** (the intended next step).

> **Self-flagged overall weakness (honest):** v2 roughly **doubles the field surface.** The design law (optional, default-empty) keeps the *sharp-case* cost near-zero but does **not** bound the *frontier-case* authoring cost — a fully-exercised Manhattan/Keynes/deep-learning specimen will be markedly heavier than Maxwell, and the lifecycle/actor/forcing machinery still has redundancy points (items 1, 6) where a careless filler can double-record. The mitigation is the design law + the companion `one_specimen.v2.template.json` (which pre-marks every new field "OPTIONAL — leave empty unless load-bearing") + the §2.2.h/§2.7 "index/derive, do not restate" rules.

---

## 7. Filling discipline (v2 checklist — extends v1 §6)

For each specimen: (1) pick the merge event + its Phase-1 row (`extends`); (2) fill `child` + `weld.parents` (the 2-projection) + `surprise` first — the certain core; (3) only if the record overflows the dyad, add `parents_full`/`mediating_wrapper`/`parent_kind` (R1/R4); (4) descend `roots.sub_wrappers` toward the ground, lowering `confidence`/raising `depth`; (5) write the ground kernel as `actors[]` (individuals first; add institutions/gov/labs only if load-bearing — D2) and set their `carrier_of`/`inhabitant_of` *only* where the bridge is real; (6) climb `harvest` to the present; (7) tag every node's `frame_layer` (D3 — cheap; default physical for actors/places, latent for ideas) and confirm the specimen is hand-checkable under each filter; (8) if exogenous forces shaped the weld, add `forcing_events[]` with graded `acted_on.strength` (D4) and reference targets by `id`/`name` (§0.1); (9) if the weld has a non-trivial life, fill `weld.lifecycle` (D1) as a *weighted index* over the dormancy/revival/candidate fields — **do NOT re-state them**; (10) partition into `fuzzy_layer` but **trust the per-node memberships as primary** (D5; the two-bin split is a derived digest); (11) WEB-search every load-bearing claim, log `sources[]`; (12) hunt `discrepancies[]` — especially framework-vs-record tensions and forcing-vs-internal tensions (D4); a **new weld-type/phase term goes in a discrepancy row before use** (§6 item 7); (13) keep all bits qualitative (`bits_note`, `principled-null` on a frontier — R16); (14) set `overall_confidence` honestly and **never read it without its `fuzzy_layer` split.** **Above all: if a v2 field feels forced on your case, leave it empty — empty is correct (the design law).**

---

## 8. Hardening notes (what this v2 changed from the architect draft, and why)

The adversarial pass made five cuts and one addition, all in service of the design law (keep the certain core thin; no redundant ways to record one fact):

1. **Removed `roots.people_0` as a storage field.** The draft kept both `actors[]` and a `people_0` "view"; a JSON template cannot enforce a computed view, so a filler would populate both and drift. v2 has **one store** (`actors[]`) and a documented rename. (Closes draft self-weakness #2.)
2. **Dropped `weld_was_built_by`** (a prose alias of `mediating_wrapper`). One concept, one field.
3. **Dropped the per-leaf `confidence` on `lifecycle.phase_trajectory[]` phases and `weld_type[]` entries.** The `membership`/`weight` ∈ [0,1] *is* the soft value ("weights not hard values" — Pav); a separate confidence-on-a-weight is a confidence on a confidence. (Confidence remains on every *factual* leaf, unchanged from v1.)
4. **Made `pre_weld_relationship` the single home for the antagonism strength**, with the `phase_trajectory` `pre_weld` entry marking only *when* — so the same fact is not weighted in two places (§2.2.h note).
5. **Clarified `fuzzy_layer` as DERIVED** from the per-node memberships (not an independent source), and stated the weld-type/phase vocabularies have a **ratified core closed set** extended only via a discrepancy row.
6. **Added one small optional `id` convention (§0.1)** so the D2/D4/discrepancy cross-references are checkable without a heavyweight id system — resolving (partially) draft self-weaknesses #3, #4, #5 at near-zero sharp-case cost.

All five D-dimensions and all sixteen R-refinements are preserved and faithful to Pav's intent; nothing in the architect's *capability* set was removed — only redundant *representations* of the same capability.

*End v2 spec. Tier-3 DRAFT, surfaced for Cowork+Pav ratification. Folds R1–R16 + makes D1–D5 first-class; preserves the optional-fields-default-empty design law; promotes nothing; convergence list stays 9; specimens remain calibration instruments extending wrapper_classes_phase1.json at deeper zoom.*
