# BATCH FINDINGS — three rendered specimens, read across each other

> **What this is.** A synthesis *across* the first three canonical-genealogy specimens — Maxwell (sharp), Darwin+Mendel (dormancy), QM+GR (frontier) — read against one another to extract what the **real record** teaches the **schema**. The point is not the three trees; it is the *friction* where each tree refused to fit its slots. That friction is the deliverable: it tells us which VARIABLES `SCHEMA.md` is missing or must change.
>
> **Status:** Tier-3 exploratory data-harvest, surfaced for **Cowork+Pav ratification**. NOT canon, NOT a tier promotion, does **NOT** grow the convergence list (stays **9**). Refines the schema's variables from real friction; promotes nothing. All confidences are SOFT scores in [0,1]; surprise/synergy assessed **qualitatively, never in bits** (MDL-in-bits needs latent embeddings — a later step). Generated 2026-06-09.
>
> **Inputs:** `specimens/maxwell.{json,md}`, `specimens/darwin_mendel.{json,md}`, `specimens/qm_relativity.{json,md}`, read against `SCHEMA.md` (esp. its §5 already-flagged gaps) and the enriched-model brief. Three independent render passes (sibling agents), now cross-cut.

---

## HEADLINE

**Three cases chosen to span the lifecycle of a weld — a settled unifier, a dormancy→resurrection, and a never-consummated frontier — independently broke the schema at the same three joints and at six case-specific ones. The convergent breaks (the weld is N-ary not binary; the weld is a *process* with a duration, not a dated event; one weld at coarse grain is a *chain/family of sub-welds* zoomed in) are now triple-attested and should be ratified. The case-specific breaks are the real prize: each phase of a weld's life reveals a variable the other phases hide. The sharp case exposed that a child can be *re-welded and re-attributed* (the surviving "Maxwell's equations" are the Maxwellians', named after the wrong node) and that parents come in *kinds* (content / method / instrument). The dormancy case exposed that the child is *status-at-a-time* (a trajectory, not an enum), that a revival can *re-interpret* the dormant object rather than wake it, and that the seam S can be *internally fractured*. The frontier case exposed the deepest gap: the schema assumes welds *resolve* — it has no slot for one seam yielding a *family of mutually-rejecting candidate children with no winner*, no way to say *"is a third even needed?"*, and it wrongly couples synergy to consolidation (QG has enormous synergy and an unborn child after 90 years). Net: the schema's `parents→one W_C` core is a clean *projection* the record routinely overflows in a structured, recordable way — and the overflow is exactly the fuzzy frontier the framework set out to make first-class.**

---

## A. THE VARIABLES THE DATA REVEALS THE SCHEMA IS MISSING OR MUST CHANGE

The honest finding is a **two-tier list**: variables *all three* cases forced (high confidence, ratify now), and variables a *single phase* of weld-life forced (the phase-diagnostic variables — the reason you render a sharp AND a dormant AND a frontier case rather than three sharp ones).

### A.0 The frame that organizes everything: a weld has a LIFECYCLE, and the schema only renders one frame of it

The single most useful thing reading the three together surfaces: **the current schema renders a weld as a *photograph* (parents → child, with a `revival` afterthought), but a weld is a *process with a life*.** Each specimen is a different exposure of that life:

| phase of weld-life | specimen | what that phase makes visible that the others hide |
|---|---|---|
| **pre-weld** (parents independent / antagonistic) | Darwin+Mendel | parents can *fight* before fusing (Mendelism was an anti-Darwinian weapon ~1900–15) → **pre-weld relationship** variable |
| **the weld fires** | Maxwell | the weld is welded *by a specific frame-operator* (the d/dt term); static parents make nothing → **weld-operator** variable |
| **child consolidates** | Maxwell | the child can consolidate *as a structurally different, re-attributed object* (4 eqns by the Maxwellians, named after Maxwell) → **re-weld + re-attribution** |
| **dormancy** | Darwin+Mendel, QG | dormancy has a *cause-frame* (internal no-go vs a political execution) and the revived object may be *re-interpreted* → **dormancy.why_frame**, **revived-as-reinterpreted** |
| **status over time** | Darwin+Mendel | the child is a *trajectory* of states (pluralist→hardened→contested), not one enum → **status-trajectory** |
| **non-consummation** | QG | the weld may *never resolve*, yielding *rival children* with no winner → **open-conjecture status, candidate_children[], weld-necessity** |

Everything in A.1–A.2 below is a consequence of taking this lifecycle seriously.

### A.1 Convergent variables — forced by ALL THREE cases (ratify now)

These are the high-confidence refinements: three independent renders, three phases of weld-life, same wall.

1. **`parents` must be N-ary (and must distinguish a MEDIATING parent from ancestral parents).** Every case overflowed the 2-slot:
   - **Maxwell:** the honest parent set is **~7** (Coulomb, Ørsted, Ampère, Faraday, Gauss, Neumann/Weber, Thomson/Kelvin). `{Faraday-field, continental-math}` is a defensible but **lossy 2-projection**.
   - **Darwin+Mendel:** the structure is **two ancestral roots** (Darwin, Mendel) **+ a mediating parent that did the welding** (population genetics / Fisher-Haldane-Wright) **+ ~5 empirical synthesizers** (Dobzhansky/Mayr/Simpson/Stebbins/Huxley). The 2-slot cannot even *name* the thing that did the welding.
   - **QG:** the origin is **multi-rooted** (Einstein / Klein / Rosenfeld / the Gamow-Ivanenko-Landau cube / Bronstein) — *no single founder*.
   - **This was already predicted** by `SCHEMA.md` §5 gap #6 (which chose the 2-projection deliberately and pushed extras into `discrepancies`). It is now **triply ratified by real friction.** The Darwin+Mendel case adds a sharper demand than "more slots": the welding agent is *not one of the parents* — it sits a layer up. → Recommend `parents_full[]` (n-ary) **alongside** the clean `parents` 2-projection, **plus** a distinct `mediating_wrapper` / `weld_was_built_by` slot. Keep the binary (it is the framework's visualization); stop forcing the truth into the discrepancy log.

2. **`when` must allow a DURATION / interval, not just a date — because a weld is a process.** All three:
   - **Maxwell:** a chain 1856 → 1861–62 → 1865 → 1884–85 → 1887–88 (two *births*, see A.2).
   - **Darwin+Mendel:** a **~30-year process (1918–1950)** with several defensible birth-dates and no single event (any single date <0.60; the *range* ~0.95).
   - **QG:** 1916 → **present, unresolved** — no end date at all.
   - → Recommend `when` accept `{from, to|null, defensible_dates[]}`. A null `to` is itself diagnostic (an open weld).

3. **LOD: one weld at coarse grain is a CHAIN/FAMILY of sub-welds zoomed in — and the *sign* of that sub-structure is itself a variable.** All three exhibit it; the cross-cut reveals a discriminator the single cases miss:
   - **Maxwell (sharp):** zoom in → an ordered **chain** of sub-welds (Ørsted seam → Faraday induction → displacement-current closure → Maxwellian vector compression → Hertz confirmation). The sub-structure **confirms** the weld.
   - **Darwin+Mendel (dormant):** zoom in → a **cascade** of pairwise welds among ~8 architects. Sub-structure **confirms**.
   - **QG (frontier):** zoom in → the weld **SHATTERS** into mutually-rejecting sub-welds (string / LQG / sum-over-histories / asymptotic safety). Sub-structure **CONTRADICTS** the weld.
   - → The signature: **a healthy weld is confirmed by its sub-structure at higher zoom; an unconsummated weld is contradicted by it.** This is a *diagnostic*, not just an LOD note. Recommend `weld.lod_scale` gain a structured `sub_welds[]` expansion **and** a `coherence_under_zoom: confirms | contradicts` flag. (This is the cleanest single output of reading the three together — no individual specimen could state it.)

### A.2 Phase-diagnostic variables — forced by ONE phase of weld-life (the reason to span sharp→dormant→frontier)

These are the variables a single case *type* would never have surfaced. Listed by which case forced them.

**The SHARP case (Maxwell) forced — because only a *settled, taught, re-derived* weld shows its own afterlife:**

4. **`re-weld` + `re-attribution` (the load-bearing single variable of the sharp case).** "Maxwell's equations" as taught were **not written by Maxwell** — he left 20 coupled equations in potentials/quaternions; the 4-equation vector form was forged 1879–1894 by the Maxwellians (Heaviside, Hertz, FitzGerald, Lodge). The **canonical name attaches to the originator of the raw form, not the producer of the surviving form.** The single `weld` + `revival{when,by,trigger}` can record a dormancy-resurrection but **cannot express that the revived object is structurally different AND mis-named.** → Recommend allowing `weld` to **CHAIN** (birth-1's `W_C` becomes a parent of birth-2) and adding a `reattribution{named_after, actually_produced_by, why}` field. *Counterpart in the dormancy case:* Darwin+Mendel's "revived-as-reinterpreted" (#7) is the same underlying gap from the other side — both say **the object that comes out of a revival is not always the object that went in.**

5. **`parent_kind: content | method | instrument`.** Maxwell got *EM content* from Faraday/Ampère, but the *mechanical-analogy METHOD* from Thomson/Kelvin, vector calculus as a *method* at the 2nd birth, and the *calibration TARGET* (light's measured speed) from Fizeau — an **instrument**, not content. `parents[]` and `sub_wrappers[]` both implicitly mean *content*, so the method-parent and instrument-parent get mis-filed. → Recommend a `parent_kind` tag. (Generalizes: QG's "tooling roots" — spin networks, Calabi-Yau, knot theory — are *method* roots too; the tag is reusable.)

6. **`surprise_priority` / `surprise_first_conjectured_by` (the conjecture-in-a-parent).** Faraday's 1846 "Ray-Vibrations" guessed *light is a vibration of the lines of force* — but speed-less, "for want of data." The surprise (light = EM) thus **pre-existed as a low-confidence weld "drawn but not confirmed" for ~15 years inside parent W_A**, with its own dormancy interval and priority, until the *other* parent (the math) arrived to make it calculable. The schema treats surprise as a property of the child/weld only. → Recommend a `surprise_priority` field. **This is the framework's own definition — "a conjecture = a low-confidence weld drawn but not yet confirmed" — found living verbatim in the historical record**, which makes it especially worth a first-class slot.

7. **`weld_operator` (the weld is welded BY a frame-operator, not just IN a frame).** Maxwell's weld fires through **{time} only** — static E + M side-by-side make *nothing*; the displacement current is *literally a d/dt term*. `frame_of_weld=[time]` records the frame but not that **time is the *active ingredient* (the derivative) rather than a passive backdrop.** → Recommend a `weld_operator` note ("time-derivative / induction-loop closure"). This is the cleanest positive confirmation in the whole batch of the brief's frame-relativity thesis (two rocks in space = nothing; through time = strata).

**The DORMANCY case (Darwin+Mendel) forced — because only a *resurrection* shows that the dormant object can change identity:**

8. **`status` must be a TRAJECTORY, not a single enum.** The Modern Synthesis is *status-at-a-time*: pluralist-1937 → hardened-1959 → contested-2007. These are different states of the **same** `W_C` (the Gould/Provine "hardening" thesis has nowhere clean to live in a single enum). → Recommend a `status_trajectory[]` of `{state, when, by}`. *Cross-link:* this is the same shape as #2 (weld-as-process) but applied to the *child's* life rather than the *weld's* firing — the child keeps living and changing state long after the weld.

9. **`revived-as-same` vs `revived-as-reinterpreted`.** `dormancy_intervals`/`revival` silently assume the object that revives **is** the object that went dormant. But Mendel's revived object may have been **re-framed** (he did *species-hybridization*; it came back as *heredity*). A revival can be a **re-weld into a new role**, not a wake-up. → Recommend a `revival.kind: same | reinterpreted` flag. (Pairs with #4 — the sharp case's re-attribution and the dormancy case's re-interpretation are two faces of "revival changes the object.")

10. **`shared_sub_object_S` must be allowed NON-UNITARY / itself contested.** S is treated as one coherent string, but for Darwin+Mendel the real S (population genetics) was **internally fractured** by the Fisher–Wright controversy (mass-selection vs shifting-balance, 1929–62). The seam itself had a rift. → Recommend `S` accept a structured `{components[], internal_conflict?}`. *Cross-link:* QG's S is *also* multi-faceted (graviton / S=A/4 / singularities) but there *agreed*; the contrast (fractured-and-contested vs multi-faceted-but-agreed) is exactly what distinguishes the dormant case from the frontier case at the seam.

11. **`pre_weld_relationship: antagonism | independence | complementarity`.** Mendelism arrived as an **anti-Darwinian weapon** (the biometrician–Mendelian war, ~1900–15) **before** Fisher 1918 welded the parents — they were neither dormant nor neutral, they were *fighting*. `survived`/`dropped` exist, but there is no **antagonism-then-fusion lifecycle** on the weld. → Recommend a `pre_weld_relationship` variable. (Only a case where the parents have a documented social history before the weld could surface this — the sharp case's parents were complementary from the start.)

**The FRONTIER case (QG) forced — because only a *non-consummated* weld shows what the schema assumed away:**

12. **`status` enum needs `open-conjecture` / `live-unconsummated-weld`.** None of `{risen, active, dormant, resurrected, stale}` fits a ~90-year-old high-synergy weld that **never produced a settled child.** The schema *assumes welds resolve.* → Add the enum value. (The single most direct "the schema literally has no value for this state" finding.)

13. **`candidate_children[]` with `unresolved: true` and a `contest_axis` (the biggest single gap in the batch).** `weld` maps parents → **one** `W_C`. QG has the *same two parents* and the *same seam S* yielding a **family of mutually-rejecting candidate children** (string, LQG, causal sets, CDT, asymptotic safety) — and *no winner*. These are not sub-welds of one pushout; they **disagree about what the child is.** Tellingly, in the render they behave like **lateral rivals** rather than `descendants` (up) — a structural symptom that none is *the* child. → Recommend `{candidate_children[], unresolved, contest_axis}` where `contest_axis` = *which-parent-dominates* / *background-dependent-vs-independent*. **No settled case could ever reveal this** — it is the entire reason the frontier specimen exists.

14. **`survived`/`dropped` must be PER-CANDIDATE (a `{feature, kept_by[], dropped_by[]}` matrix), not flat arrays.** Each QG rival drops a *different* parent-feature: string drops GR's **background-independence**; LQG drops QM's **fixed external time + continuum**; semiclassical drops **the weld itself**. Flat `survived[]`/`dropped[]` cannot record *dropped-by-which-child*. → Recommend the matrix. (Latent in the sharp case too — Maxwell "dropped" the ether-scaffold but kept the displacement-current it birthed — but only the multi-child frontier case makes the per-branch bookkeeping *necessary*.)

15. **`weld_necessity_confidence` — "is a third even NEEDED?" must be first-class.** A serious minority (semiclassical gravity; Rosenfeld → Mattingly) holds gravity may couple to *classical* spacetime — i.e. **there is no child; `W_C` is a category error.** This is the *falsifier of the weld*, the strongest form of the fuzzy frontier, and it is currently buried in `discrepancies`. → Recommend a top-level `weld_necessity_confidence`. (A settled weld has this implicitly at 1.0; only the frontier case forces it to be *named* because only there is it < 1.)

16. **`surprise_confidence` and `child.confidence` are INDEPENDENT axes and must be allowed to diverge sharply.** The schema (and the Phase-1 DB's logic) ties high synergy to a *risen* child. QG breaks the coupling: `surprise_confidence` **0.85** (the synergy is enormous and real — graviton-in-the-string-spectrum, S=A/4, discrete area) while `child confidence` **0.40** (the child is unborn after a lifetime). → Recommend they be explicit orthogonal axes. **This is the deepest conceptual correction in the batch:** synergy does not imply consolidation; a seam can be maximally fertile and still birth no single child for 90 years.

17. **`dormancy.why_frame` (dormancy has a CAUSE-FRAME).** QG has three dormancies at three grains with **different-frame causes**: field stagnation 1970–83 (*knowledge*-frame: no-go theorems), spin-networks orphaned ~1964/71–88 (*knowledge*-frame: tool awaiting a host), and **Bronstein's lineage severed by the NKVD executing him in 1938** (*physical/political*-frame: a death, external to the idea). A single `why` string cannot capture that a lineage can be cut by a **purge** as well as by a **theorem**. → Recommend `dormancy.why_frame`. *Cross-link:* Darwin+Mendel's dormancy was *knowledge*-frame (misreading + blending orthodoxy); QG adds the *physical*-frame cause — the two cases together populate the frame-tag with real contrast.

18. **`bits_note` as a PRINCIPLED NULL on the frontier.** You cannot MDL-score a theory you do not have, so QG's compressor leg is **intrinsically undefined** while the child is unborn — a blank *by necessity, not by laziness*. → Recommend frontier specimens be allowed an explicit `bits_note: principled-null` so the empty field is not read as missing work. (Consistent across the batch: *all three* keep bits qualitative per discipline; QG additionally shows that on a frontier the value is not merely deferred but *undefinable in principle*.)

---

## B. CONSOLIDATED DISCREPANCY REGISTER (ranked — framework-vs-record tensions first)

Every interesting discrepancy across the three specimens, merged and ranked by how **load-bearing / interesting** it is — i.e. how much it tells us which variable the schema is missing. **Framework-vs-record tensions lead** (per the brief, they are the most valuable: they are the places the clean two-parent weld does not match the messy multi-parent record).

> Legend: **FvR** = framework-vs-record-tension · **CG** = contested-genealogy · **PD** = priority-dispute · **DC** = dormancy-contested · **DA** = date/attribution-conflict · **WvR** = whig-vs-revisionist.

### Tier 1 — Framework-vs-record tensions (the highest-value rows: each names a missing variable)

| # | specimen | type | what | why it is load-bearing (→ the variable it names) |
|---|---|---|---|---|
| **1** | **QG** | **FvR** | **Rival children, no winner.** Same two parents + same seam S → a *family* of mutually-rejecting candidate children (string / LQG / causal sets / CDT / asymptotic safety). Not sub-welds of one pushout — they disagree about what the child *is*. | **The single biggest gap.** The schema has *no slot* for a weld with competing outputs and no resolution. → `candidate_children[]` + `contest_axis` (variable #13). Caps child-confidence at ~0.4 and is the entire justification for the frontier specimen. |
| **2** | **Darwin+Mendel** | **FvR** | **The clean dyad is wrong; the weld is multi-parent and the real S sits a layer UP.** Darwin & Mendel are the two *deep roots*; the proximate parent is **population genetics** (Fisher-Haldane-Wright), with ~5 empirical synthesizers. "1866 paper meets 1859 book" is the popular myth, not the structure. | Ratifies `SCHEMA.md` §5 gap #6 with the strongest evidence in the batch, **and sharpens it**: the welding agent is not a parent but a *mediating wrapper*. → `parents_full[]` + `mediating_wrapper` (variable #1). Dyad-as-parents drops to **0.55**; population-genetics-as-S holds at **0.90**. |
| **3** | **Maxwell** | **FvR** | **Second birth + misattribution.** The taught 4-equation "Maxwell's equations" were forged by the Maxwellians (Heaviside/Hertz, 1879–94) from Maxwell's 20-equation raw form. The canonical **name attaches to the wrong node** — the originator of the raw form, not the producer of the surviving structure. | The clean parents→one-child diagram hides a *whole second merge event*, and credit is mis-assigned. → `weld` must **chain**; `reattribution{}` (variable #4). Splits one rendered weld into two real events — the load-bearing variable-refinement of the sharp case. |
| **4** | **QG** | **FvR** | **Is the weld even NEEDED?** A serious minority (semiclassical gravity; Rosenfeld → Mattingly) holds gravity may stay classical → *there is no child; `W_C` is a category error.* | The falsifier-of-the-weld; currently buried as a discrepancy. → first-class `weld_necessity_confidence` (variable #15). Forces "is a third needed?" to be a number, not an assumption. |
| **5** | **Darwin+Mendel** | **FvR** | **Antagonism-then-fusion.** Mendelism arrived as an *anti*-Darwinian weapon (biometrician–Mendelian war, ~1900–15) *before* Fisher welded the parents. Neither dormant nor neutral — *fighting*. | No `survived`/`dropped` field captures a *pre-weld social history* between the parents. → `pre_weld_relationship: antagonism | independence | complementarity` (variable #11). Antagonism phase ~0.90; flags the variable with no confidence drop. |
| **6** | **Maxwell** | **FvR** | **Multi-parent reality vs the 2-parent weld.** Honest parent set ≈ 7 (Coulomb/Ørsted/Ampère/Faraday/Gauss/Weber/Thomson). The residue is *typed*: Thomson's analogy *method*, Ørsted's founding *observation*, Fizeau's calibration *target*. | Same core tension as #2, but it additionally exposes that the extra parents are **different KINDS**. → `parent_kind: content|method|instrument` (variable #5) on top of `parents_full[]`. Flags `parents`-length-2 as a lossy projection. |
| **7** | **Maxwell** | **FvR** | **Frame-relativity of the weld.** Static E + M in {space} make *nothing*; only through {time} (the d/dt displacement-current term) does the wave appear. The weld is welded **by time**. | A *positive* confirmation that the schema's frame machinery discriminates correctly on a top-tier settled case — and that `frame_of_weld` should name the *active operator*, not just the frame. → `weld_operator` (variable #7). Strengthens the render rather than lowering confidence. |

### Tier 2 — Contested genealogies & the surprise's own priority (which parents were real; who conjectured the synergy first)

| # | specimen | type | what | why interesting (→ variable) |
|---|---|---|---|---|
| **8** | **QG** | **CG** | **Which parent dominates is the fault line.** Covariant/string = QFT-method on gravity (**W_B swallows W_A**); canonical/LQG = background-independence primary (**W_A swallows W_B**). SEP: "two camps almost certainly talking past each other." | The *direction* of a symmetric two-parent weld is itself disputed and is the contest's defining axis. → feeds `contest_axis` on `candidate_children[]` (variable #13). The schema flattens weld direction. |
| **9** | **Maxwell** | **CG** | **Field vs action-at-a-distance.** Was the lineage Faraday's *field/contiguous-action* or the continental *action-at-a-distance* (Ampère/Gauss/Weber/Helmholtz)? The weld kept W_A's *ontology* but W_B's *calculus*, so each losing parent owns half. | The brief's "what were the real parents?" problem (the special-relativity Einstein-vs-Lorentz-Poincaré analogue), and it is **frame-relative**: in {knowledge} the continental math is the parent; in {space}/ontology Faraday's field is. The 0.95/0.90 parent split is a projection, not a neutral fact. |
| **10** | **Maxwell** | **PD** | **Priority on the light claim.** Faraday's 1846 "Ray-Vibrations" already proposed light *is* a vibration of the lines of force; Maxwell called it "the same in substance… except [no] data to calculate the velocity." | The surprise is **older than the weld** in qualitative form — a low-confidence weld "drawn but not confirmed" for ~15 years inside one parent. → `surprise_priority` (variable #6). The framework's own conjecture-definition, in the record. |
| **11** | **QG** | **PD** | **Origin of the field is multi-rooted.** Einstein 1916 / Klein 1927 / Rosenfeld early-1930s / the Gamow-Ivanenko-Landau cube 1928 / Bronstein 1935–36 / "graviton" named ~1934. **No single founder.** | The fuzzy deep-root frontier the schema predicts — `people_0` has no single originator, and which root counts as "first" is contested (see #15). Confirms multi-origin is normal at the roots. |
| **12** | **Darwin+Mendel** | **PD** | **The rediscovery was a contested 3-/2-way event.** de Vries published 1900 *without citing Mendel* (added it only after Correns objected); Tschermak's grasp of segregation is doubted — the "three rediscoverers" may reduce to ~two. | The *revival trigger itself* is a priority dispute. → bears on `revival.by` granularity and couples to the dormancy-contested row (#14). de Vries/Correns ~0.95; Tschermak co-equal ~0.50. |

### Tier 3 — Contested dormancy (the dormant object's identity and the cause of its sleep)

| # | specimen | type | what | why interesting (→ variable) |
|---|---|---|---|---|
| **13** | **QG** | **DC** | **Bronstein's neglect was EXTERNAL.** A root node went dormant because its author was **executed by the NKVD in 1938** (age 32) — a *physical/political*-frame cause, not internal-to-the-idea. Reconstructed only recently (Stachel; Gorelik & Frenkel). | The schema's dormancy `why` is a bare string and cannot say *what frame severed the lineage* (a purge vs a theorem). → `dormancy.why_frame` (variable #17). The starkest case in the batch of a physical-frame dormancy. |
| **14** | **Darwin+Mendel** | **DC** | **"35 years of neglect" is disputed.** Olby 1979 / Brannigan: Mendel did *species-hybridization*; the "long neglect" framing traces to Glass 1953 — *and* the revisionism is itself contested back (Oxford Genetics 2023; John Innes). A **three-pole** literature. | The *fact* of ~3 citations is solid (~0.90); the *clean-neglect narrative* is frontier (~0.50). The revived object may differ from the dormant one. → `revived-as-reinterpreted` (variable #9). |

### Tier 4 — Internal-rift, whig-vs-revisionist, and date/attribution wobble (real but lower variable-yield)

| # | specimen | type | what | why interesting (→ variable) |
|---|---|---|---|---|
| **15** | **Darwin+Mendel** | **CG** | **Fisher vs Wright (1929–62):** mass-selection (drift negligible) vs shifting-balance (drift important). The seam S (population genetics) contained an **unresolved internal rift** — non-unitary. | → `shared_sub_object_S` must be allowed non-unitary/contested (variable #10). S-as-single-object ~0.70; the rift itself ~0.95. |
| **16** | **Darwin+Mendel** | **WvR** | **Hardening of the synthesis** (Gould/Provine): pluralist 1930s → rigid pan-selectionism by 1959. `W_C` at t=1937 ≠ `W_C` at t=1959. | The child is **time-indexed**. → `status_trajectory` (variable #8). Child-as-fixed-object ~0.70. |
| **17** | **QG** | **WvR** | **"Which child is winning" is era-relative.** String dominant by headcount since mid-1980s (Witten 1995); revisionist counter (Smolin/Woit 2006: unfalsifiable landscape, no SUSY at LHC); Rovelli 2016: "the string planet is infinitely less arrogant than ten years ago." | Status on a frontier weld is **observer- and era-relative** — which is *why* `frame_of_weld` here engages {meaning}. Couples to variables #13/#16. |
| **18** | **QG** | **DA** | **The Wheeler-DeWitt name was unstable ~20 years.** DeWitt called it the "Einstein-Schrödinger equation"; Wheeler called it the "DeWitt equation"; settled only at the 1988 Osgood Hill conference. | `who_called_it` is genuinely *time-dependent* and disputed *among the originators themselves* — a micro-version of the Maxwell re-attribution (#3) at node level. |
| **19** | **Maxwell** | **DA** | **Date wobble on the load-bearing number.** Weber–Kohlrausch unit-ratio dated **1855 *and* 1856**; Maxwell's c-realization **late 1861 / 1862**. | A small fuzzy flicker on the *single most load-bearing number* (the bench c that = light-speed), sitting right at the revival hinge. Negligible on substance; a clean example of a *frontier date on a core fact*. |
| **20** | **Darwin+Mendel** | **DA** | **No single birth-date** for the synthesis: Fisher 1918 vs the 1930–32 trio vs Dobzhansky 1937; *named* 1942. | → `when` as a duration/interval (variable #2). No single date >0.60; the 1918–1950 range ~0.95. |

**Register-level reading.** The Tier-1 block is the deliverable's core: **seven framework-vs-record tensions, and every one names a distinct missing variable.** Three of the seven (#1, #2, #3) are *the* defining gap of their respective specimen. The pattern across the register is unmistakable — **the discrepancies are not scattered noise; they cluster on exactly the joints where a binary, single-shot, resolving weld-model meets a record that is N-ary, processual, and sometimes non-resolving.**

---

## C. PROPOSED SCHEMA REFINEMENTS

Concrete, minimal additions — each traceable to the variables (A) and discrepancies (B) above. Ordered by confidence/priority. Nothing here promotes anything or changes the convergence count; these refine `SCHEMA.md`'s VARIABLES only.

### C.1 Ratify now (triple-attested across all three cases)

- **R1 — N-ary parents + a mediating-parent slot.** Add `weld.parents_full[]` (n-ary, each `{name, kernel, frame[], confidence, parent_kind}`) **alongside** the existing 2-slot `weld.parents` (kept as the clean binary projection). Add `weld.mediating_wrapper` / `weld.weld_was_built_by` for the agent that *performed* the weld when it is not one of the parents (population genetics; the Maxwellians). *Resolves discrepancies #2, #6; ratifies SCHEMA.md §5 gap #6.* **Confidence ~0.95.**
- **R2 — `when` as an interval.** Change `weld.when` to accept `{from, to|null, defensible_dates[]}`; a null `to` marks an open/unconsummated weld. *Resolves #20, supports #1.* **Confidence ~0.95.**
- **R3 — structured `sub_welds[]` + `coherence_under_zoom`.** Let `weld.lod_scale` carry an ordered `sub_welds[]` expansion **and** a flag `coherence_under_zoom: confirms | contradicts` (sharp/dormant → *confirms*; frontier → *contradicts*). *This is the cross-cut's signature finding — the single best thing reading the three together produced.* **Confidence ~0.9.**
- **R4 — `parent_kind: content | method | instrument`** on every parent/sub-wrapper. *Resolves #6; reused by QG's tooling roots.* **Confidence ~0.9.**

### C.2 Strong (each forced hard by one phase; high value)

- **R5 — `status` gains `open-conjecture` (a.k.a. `live-unconsummated-weld`)**, and `child.status` is supplemented by a `status_trajectory[]` of `{state, when, by}`. *Resolves #12 (QG enum gap) and #16 (Darwin+Mendel hardening). Note these are two needs the same field upgrade serves: a new value AND a time-series of values.* **Confidence ~0.9.**
- **R6 — `weld.candidate_children[]` + `unresolved: bool` + `contest_axis`** for a weld with competing, mutually-rejecting outputs and no winner. *Resolves the batch's biggest gap (#1); feeds on #8's "which parent dominates" axis.* **Confidence ~0.9.**
- **R7 — per-candidate survived/dropped matrix:** replace flat `survived[]`/`dropped[]` with (or add) `feature_ledger[]` of `{feature, kept_by[], dropped_by[]}`. *Resolves #1's bookkeeping; latent in Maxwell's scaffold-vs-product drop.* **Confidence ~0.85.**
- **R8 — `weld.weld_necessity_confidence`** (top-level): "is a third even needed?" *Resolves #4; implicitly 1.0 for settled welds, <1 only on the frontier.* **Confidence ~0.85.**
- **R9 — decouple `surprise_confidence` from `child.confidence`** explicitly in the spec as **independent orthogonal axes** (the schema/Phase-1 logic currently couples synergy→risen-child). *Resolves the deepest conceptual issue surfaced by QG; the frontier proves a seam can be maximally fertile with an unborn child.* **Confidence ~0.9.**
- **R10 — `revival.kind: same | reinterpreted`** and **`weld` chaining + `reattribution{named_after, actually_produced_by, why}`**. The two faces of "a revival/consolidation can change the object." *Resolves #3 (Maxwell re-attribution) and #14/#9 (Mendel re-interpretation) — register them together; they are one phenomenon seen from the sharp side and the dormant side.* **Confidence ~0.85.**
- **R11 — `dormancy.why_frame ⊆ {time, space, knowledge, meaning, physical/political}`.** A lineage can be cut by a purge (physical) as well as a theorem (knowledge). *Resolves #13; contrasts with #14.* **Confidence ~0.85.**

### C.3 Refinements to existing structure (lower-priority, but real)

- **R12 — `shared_sub_object_S` may be non-unitary/contested:** allow `S` a structured `{components[], internal_conflict?, agreed: bool}`. Captures both Darwin+Mendel's *fractured-and-contested* S (#15) and QG's *multi-faceted-but-agreed* S — the agreed flag distinguishes them. **Confidence ~0.8.**
- **R13 — `weld_operator`** note on `frame_of_weld` (the *active* frame-ingredient, e.g. the d/dt term). *Resolves #7.* **Confidence ~0.8.**
- **R14 — `pre_weld_relationship: antagonism | independence | complementarity`.** *Resolves #5.* **Confidence ~0.8.**
- **R15 — `surprise_priority` / `surprise_first_conjectured_by`** (the conjecture-in-a-parent, with its own dormancy/priority). *Resolves #10.* **Confidence ~0.8.**
- **R16 — `bits_note` may be explicitly `principled-null`** for frontier specimens (undefinable, not deferred). *Resolves #18; keeps the no-fabricated-bits discipline intact.* **Confidence ~0.85.**

**Design note (how to add without bloating the trunk).** Most of R1–R16 are *optional* fields that default empty on a healthy sharp weld — a Maxwell-style settled case fills `parents`, `when`, `child.status`, `weld_necessity_confidence=1.0` and leaves `candidate_children`, `pre_weld_relationship`, `revival.kind` empty. The schema stays light for the common case and only *expands* where the record forces it. That keeps the **certain core thin and the frontier expressive** — which is the framework's own fuzzy-LOD principle applied reflexively to the schema itself.

---

## D. HOW THE FUZZY-LOD / CONFIDENCE LAYER PLAYED OUT — sharp → dormant → frontier

The three cases were *chosen* to walk the confidence gradient, and reading them together shows the `certain_core`/`frontier` partition behaving like an **instrument with a moving fulcrum**. The crucial discovery: **where the certain core sits in the tree is itself diagnostic of the weld's health.**

| | **Maxwell (SHARP)** | **Darwin+Mendel (DORMANT)** | **QG (FRONTIER)** |
|---|---|---|---|
| **overall_confidence** | ~0.88 | ~0.90 | **0.45** |
| **where the certain core sits** | the **trunk** (child 0.97, weld 0.96, surprise 0.96) — classic shape: solid centre, fuzzy roots & cultural edges | the **trunk** (the *fact* of the merge ~0.95) but the **proximate-parent identity is frontier** (dyad-as-parents 0.55) — the fuzz reaches *into the trunk* | the **LOWER half** (parents 0.99, seam 0.90) — **the crown is hollow** (child 0.40); the certain core is *under* the child, not *at* it |
| **what is frontier** | deep depth-2 roots (ether scaffold 0.85), cultural harvest (psychic-wireless 0.75, electrical-sublime 0.70), a date-flicker on c | the *narrative* around solid facts (clean-dormancy story 0.50, Tschermak-as-rediscoverer 0.50), the fractured S (0.70), the child-as-fixed-object (0.70) | **THE CHILD ITSELF** (0.40), which candidate is right (0.3–0.7, no winner), whether the weld is needed (0.45) — *plus* the usual deep roots |
| **the conjecture-in-the-record** (framework's "low-confidence weld drawn but not confirmed") | **a single dormant conjecture**: Faraday's 1846 light-guess, drawn-not-confirmed for 15 years inside a parent, later confirmed | **a re-interpreted revival**: the dormant object may not be the revived object | **the entire child is the conjecture** — a 90-year-old unconfirmed weld; the frontier *is* the canopy |

**Three readings that only the cross-cut yields:**

1. **The fulcrum moves up the tree as the weld gets less consummated.** Sharp: core at the trunk, fuzz in the roots/edges (textbook). Dormant: the fuzz *climbs into the trunk* (the parent-identity itself is contested even though the merge-fact is solid). Frontier: the core *sinks below the child* and the entire crown is frontier. **The vertical position of the certain-core/frontier boundary is a confidence-thermometer for the weld** — a genuinely new, schema-level observable that no single specimen states.

2. **`overall_confidence` is a *split aggregate*, not an average — and the split pattern is the signal.** QG's 0.45 is not "moderately confident everywhere"; it is **0.99 on the parents AND 0.40 on the child** held in one number. Reading it as a mean destroys the information. The fuzzy-layer's job is precisely to *un-average* it back into "what is solid (the lower tree) vs what is conjecture (the canopy)." Recommend `overall_confidence` always be paired with its `certain_core`/`frontier` split and never read as a scalar — the three cases make this non-negotiable.

3. **The frontier is generative exactly as the framework predicted — and most generative where the trunk is weakest.** The richest *cultivation surface* in the batch is QG (a whole canopy of rival children, a holography *grandchild* — AdS/CFT at 0.80 — that **outgrew the unborn parent**, and a live "is a third even needed?" dissent). The framework's claim that "the frontier is where conjectures are cultivated, not noise to clean" is **most vividly true in the case with the lowest trunk-confidence.** The fuzzy-LOD layer is not a confidence-decoration on a settled tree; it is the *primary structure* of a frontier specimen. Equally, the discipline held in the other direction: across all three, **bits stayed qualitative** — and QG sharpened "qualitative-for-now" into "principled-null" (you cannot MDL-score a theory you do not have), which is the fuzzy-LOD layer being honest about an *intrinsic* limit, not a deferred one.

**Net on the fuzzy layer:** it worked, and it earned its first-class status. It correctly drew a thin solid trunk for Maxwell, correctly flagged that Darwin+Mendel's solidity is in the *fact* not the *story*, and correctly reported that QG's certain knowledge is everything *except* the thing the specimen is named after. A single-confidence-per-class scheme (the Phase-1 style) would have collapsed all three to a middling scalar and lost every one of these distinctions. **Per-node confidence + an explicit certain-core/frontier partition is the right resolution** — and the cross-cut adds one refinement to it: record *where in the tree* the partition boundary falls (R3's `coherence_under_zoom` is the weld-level version of the same idea).

---

## E. HONEST SCOPE + TIER-3 DISCIPLINE FOOTER

**Scope and limits (honest):**
- **Three specimens is a small N**, deliberately spanning the lifecycle extremes (sharp / dormant / frontier). The convergent variables (A.1) are triple-attested and safe to ratify; the phase-diagnostic variables (A.2) each rest on a **single** case and should be treated as **well-motivated conjectures pending a second instance** of the same phase (e.g. a second frontier weld to re-confirm `candidate_children[]`; a second re-attribution case — special relativity's Einstein-vs-Lorentz-Poincaré is the obvious next test — to re-confirm `weld`-chaining).
- **Source reliability is mixed and was kept honest per specimen.** Trunk facts were web-verified during each render (Maxwell: Wikipedia "History of Maxwell's equations" + IEEE Spectrum + Hunt *The Maxwellians*; Darwin+Mendel: the ~3-citations fact, Fisher 1918, Huxley 1942, Olby 1979 + the 2023 counter-revisionist rebuttal; QG: Goroff-Sagnotti 1985–86 two-loop, the spin-network revival). **Softer edges are flagged in-record:** Maxwell's cultural harvest rests on media-history scholarship (~0.65); Darwin+Mendel's Provine/Olby claims were read via search-summaries not full primary text (held ~0.9); QG's two best histories (Rovelli, Schwarz) are each **partisan of a rival child** (a reflexivity flag carried in-record — the historiography forks along the same seam as the physics), and the Wikidata structured influence-graph was not cleanly harvested for QG (a real provenance gap).
- **This synthesis is a meta-render, not new harvesting.** It re-reads the three completed specimens against each other and against `SCHEMA.md`; it does not re-run the web searches. Where the three specimens disagree on a fact, none was found — they are consistent (same house pattern, paired json+md, same disclaimer).
- **Surprise/synergy is assessed QUALITATIVELY, never in bits**, across all three (per `SCHEMA.md` §3). No numeric bit value is asserted anywhere; QG additionally demonstrates a *principled* null (R16). MDL-in-bits remains a later step requiring latent embeddings.

**Tier-3 discipline footer.** Exploratory data-harvest, surfaced for **Cowork + Pav ratification.** This refines the schema's **VARIABLES** from real friction; it does **NOT** compile canon, promote anything, or grow the convergence list — **which stays 9.** Nothing here is a 10th convergence (the three specimens are *worked examples / calibration instruments* extending `latent_olympics_data/wrapper_classes_phase1.json` at deeper zoom — Maxwell as the calibration ruler, Darwin+Mendel as the dormancy worked example, QG as the deliberate negative control — not new cross-substrate convergences). Every load-bearing claim traces to the per-specimen `sources[]`; confidences are SOFT scores in [0,1]; the certain-core/frontier split is carried so `overall_confidence` is never read as a flat scalar. Schema refinements (C) are **proposals**, owing review before any change to `SCHEMA.md`.

---

*End batch findings. Synthesizes `specimens/maxwell.*`, `specimens/darwin_mendel.*`, `specimens/qm_relativity.*` across the sharp→dormant→frontier axis. The deliverable is the refined variable-set (A) + the ranked discrepancy register (B) + the proposed refinements (C) — the places the real record taught the schema what it was missing.*
