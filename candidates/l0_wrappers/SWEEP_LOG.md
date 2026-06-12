# L0 Wrapper Catalog — SWEEP LOG (append-only)

> Append-only dated record of each recursive sweep over the L0 entity catalog, per `L0_WRAPPER_SPEC.md` §7.2 step 6.
> A cold sweep-N+1 agent reads this top-to-bottom to learn the last sweep's state, the locked dials, the proposed-vocabulary queue, and the frontier list. **Never edit or delete a prior sweep's section** — append a new one.

---

## Sweep 1 — 2026-06-11 (harvest + finalize)

**Seats:** `l0-sweep-01-sonnet` (harvest), `l0-sweep-01-finalize` (Fable finalize pass).
**Dials locked this sweep** (frame-lock §7.3): kind vocab + 16-term relation vocab + kernel-admission rule (§2.3) + membrane proxy `l0-membrane-proxy-v0.1` (§3.1), all per spec as authored.

### What was harvested
Six samples (Pav's L0 list, §5), all `verification: pending` at emit — real fetched sources only, no fabrication.

| slug | kind | entity facts | relation facts | notes |
|---|---|---|---|---|
| `smartphone` | object (generic) | l0-smartphone-0001..0021 (21) | l0-smartphone-r0001..r0004 (4) | Wikipedia/BankMyCell/Statista/Ericsson |
| `iphone-15-pro` | device-model (instance) | l0-iphone-15-pro-0001..0021 (21) | l0-iphone-15-pro-r0001,r0002,r0004 (3) | Apple/Wikidata; r0003 not emitted |
| `claude` | ai-model (class) | l0-claude-0001..0025 (25) | l0-claude-r0001..r0008 (8) | Anthropic/Wikidata/Wikipedia |
| `alan-turing` | person | l0-alan-turing-0001..0025 (25) | l0-alan-turing-r0001..r0006 (6) | Wikipedia/Wikidata; r0006 added in finalize |
| `acetylsalicylic-acid` | compound (scope-relative) | l0-acetylsalicylic-acid-0001..0023 (23) | l0-acetylsalicylic-acid-r0001,r0002 (2) | Wikidata/Wikipedia/Harvard-Berkman |
| `turing-enigma-hodges` | book | l0-turing-enigma-hodges-0001..0023 (23) | l0-turing-enigma-hodges-r0001..r0005 (5) | Wikidata/Wikipedia/PUP/Amazon |

**Totals after finalize:** 138 entity facts + 28 relation facts = **166 l0 facts**; 7 verification records; **8 compiled subjects** (the six samples + `proposed:bayer-aspirin` + `proposed:turing-award`). Best-row buckets: **pending 152, unverifiable 7, corroborated 0** — an honest un-battle-tested catalog (every kernel empty by §2.3; hardening is sweep-2's first job).

### Finalize pass (Fable, `l0-sweep-01-finalize`) — corrections applied
All corrections are **append-only** (new lines / verification records / one new fact); no emitted line was edited or deleted.

1. **Split-brain data location RESOLVED (the primary Opus issue).** Five samples' facts had been written to `candidates/l0_wrappers/facts/<slug>.jsonl`, which `compile_substrate.py` does not glob — only aspirin reached the substrate, so the compiled view covered 1/6. Appended all 140 staging facts (115 entities + 25 relations) into `../canonical_genealogy/substrate/facts/l0_catalog.{entities,relations}.jsonl`, routing by id namespace (`l0-<slug>-NNNN` → entities, `l0-<slug>-rNNNN` → relations). Unmodified facts were passed through byte-for-byte. The staging files remain as the harvest record; **the substrate `l0_catalog.*.jsonl` is now the canonical append-only source.** Compiled view now covers all six samples.

2. **Two over-certain ESTIMATE facts re-banded on import** (breached SUBSTRATE_SPEC estimate band 0.2–0.5):
   - `l0-smartphone-0005` (mass_adoption interval) certainty **0.82 → 0.45**;
   - `l0-claude-0017` (frame_layer) certainty **0.70 → 0.45**.
   Values unchanged; a `RE-BAND` note was appended to each. Done at canonical emission (not a later re-emit) because best-value resolution prefers higher certainty, so a downward correction must be made at emit. Toy inline data for `l0-smartphone-0005` updated to 0.45 to stay in lockstep.

3. **One convergence-hook URL normalized:** `l0-claude-0018` source.url `file://D:/...` → bare `D:/...` to match the established `agnostic_framework.dev` local-path convention (cosmetic; the local-path flag is expected per SUBSTRATE gotcha 7).

4. **Seven relation edges demoted to `unverifiable` (membrane)** via append-only verification records in the new `../canonical_genealogy/substrate/verifications/l0_catalog.jsonl` — these encoded **reversed-direction** or **multi-hop-candidate** claims that the compiled relation graph would otherwise draw as false. Each record names the retained correct edge; the bad line stays (superseded, not deleted):
   - `l0-smartphone-r0002` ("smartphone available-on iphone-15-pro") — reversed/mis-predicated; correct = `l0-iphone-15-pro-r0001` (instance-of).
   - `l0-smartphone-r0003` ("smartphone available-on claude") — reversed; correct = `l0-claude-r0004`.
   - `l0-smartphone-r0004` ("smartphone conceptual-ancestor-of claude") — multi-hop candidate; belongs in membrane (§2.7 hard rule, §5).
   - `l0-alan-turing-r0003` ("alan-turing about turing-enigma-hodges") — reversed `about` (work→subject); correct = `l0-turing-enigma-hodges-r0002`.
   - `l0-alan-turing-r0004` ("alan-turing named-after turing-award") — reversed `named-after` (thing→eponym); the Award is named after the man. **Corrected edge emitted** (item 5).
   - `l0-alan-turing-r0005` ("alan-turing influenced iphone-15-pro") — multi-hop candidate; spec §5 sample 4 mandates membrane.
   - `l0-claude-r0008` ("claude influenced alan-turing") — temporally impossible as written; the real Turing→Claude lineage is the retained conceptual-ancestor edges `l0-alan-turing-r0002`/`l0-claude-r0005`.
   *Context:* the sweep-1 constellation harvest emitted "mirror" edges from multiple vantage points; the correctly-directed counterpart of each demoted edge already existed (the toy's `EDGES` array had already drawn only the correct directions, citing these as "(inverse)"). The substrate is now honest to match.

5. **One corrected fact emitted:** `l0-alan-turing-r0006` — subject `proposed:turing-award`, predicate `rel:named-after:alan-turing` (award→eponym, correct direction), certainty 0.90, source Wikipedia Turing Award. Replaces the reversed r0004. Preserves the two-hop convergence hook into the FROZEN `deep_learning` specimen's 2018 Turing Award nodes.

6. **Spec edits** (`L0_WRAPPER_SPEC.md`, a Tier-3 draft, editable): added a **"by analogy" caveat** to §2.2 (the 2026-06-09 contextual-frame-relativity canon is reused across a different mechanism, not the identical phenomenon — per Opus); added a **§9 LIMITS section** consolidating the honest standing.

7. **Toy** (`../canonical_genealogy/toys/l0_constellation_toy.html`): updated the re-banded certainty, annotated the three "(inverse)" refs as retracted/demoted, and pointed the named-after edge at the corrected `r0006` with a direction-honest label. `node --check` on the extracted script: **PASS**.

### Verification (this sweep)
- `python compile_substrate.py` from `../canonical_genealogy/substrate/`: **validation errors 0**, no HAZARD, exit 0. Expected non-fatal flags only: 28 × `specimen 'l0-catalog' not found among ../specimens/*.json` (per §2.9.3, until the gated anchor lands) + the pre-existing `f-agf-0027` local-path flag.
- Compiled output `compiled/l0-catalog.compiled.json`: 8 subjects; all 25 retained relation edges resolve distinct (no collapse); the 7 demoted edges resolve to bucket `unverifiable`; `r0006` resolves `pending`.
- All 166 l0 fact_ids globally unique and namespace-compliant (HAZARD guard satisfied).

### NOT done (deliberately — gated / deferred)
- **Subject-index anchor (`specimens/l0_catalog.json`, §2.9.4) NOT created.** It would silence the 28 unknown-specimen flags and enable exact `subject_id` validation, but it adds a 9th file to a directory the wiki documents as holding 8 — **awaits a Pav/Cowork nod** (propose-before-execute). The flags are expected-and-honest until then.
- **`tools/l0_compile_wrappers.py` NOT built.** Wrapper views + toy embeds remain hand-assembled snapshots (drift-prone on re-harvest). Building it is a sweep-2+ task; it must reproduce hand-assembled wrappers byte-for-byte (modulo `generated`).
- **No `wrappers/<slug>.wrapper.json` files written this sweep.** Compiled substrate is the source of record; the toy reads a hand-transcribed snapshot.

### Proposed vocabulary queue (apply from sweep-2 after a nod)
- **Relation-direction discipline (PROPOSED dial):** relation facts must be emitted in the canonical direction defined in §2.7 (e.g. `named-after` = thing→eponym; `about` = work→subject; `available-on` = software→platform). "Mirror"/inverse edges from the non-canonical endpoint are NOT separate facts. Sweep-1 demoted 7 such edges; lock this rule from sweep-2.
- **Proposed-subject edge namespacing (PROPOSED convention, already used twice):** an edge whose subject is a `proposed:<slug>` frontier entity (no catalog file of its own) is namespaced under the related catalog entity's slug — e.g. `l0-acetylsalicylic-acid-r0002` (subject `proposed:bayer-aspirin`) and `l0-alan-turing-r0006` (subject `proposed:turing-award`). Document/ratify this so it is a rule, not a deviation.
- No new `kind` terms proposed this sweep.

### Frontier for sweep 2 (promote these `proposed:` targets to catalog entities)
`apple`, `iphone` (class rung between smartphone↔iphone-15-pro), `anthropic`, `large-language-model`, `bayer`, `bayer-aspirin`, `andrew-hodges`, `imitation-game`, plus newly minted: `turing-award`, `iphone-14-pro`, `breaking-the-code-play`, `biography`, `mobile-device`.

### Sweep-2 first move (the highest-value one)
**Harden, don't broaden.** Verify standing `pending` facts: fetch an INDEPENDENT second source per fact, append `corroborated`/`disputed` verification records (a second source from the SAME harvest seat does not count as independent, §7.3). Sweep-1 has **zero corroborated facts**, so every kernel is empty — the first corroborations are what light up the kernel-core render and prove the facts-as-wrappers hardening loop with real data. A sweep that only verifies and disputes — adding zero entities — can be the best sweep of the year (§7.4).

---

## Sweep 1.1 — 2026-06-11 (builder landed: `tools/l0_compile_wrappers.py v1`)

**Seat:** `l0-sweep-01b-builder` (Fable). **Closes the §9 LIMITS gap** "the wrapper-view builder is unbuilt": the six `wrappers/<slug>.json` files and the constellation toy's inline data were hand-assembled / hand-transcribed snapshots that drift on re-harvest. They are now **GENERATED** from `compiled/l0-catalog.compiled.json`.
**No substrate change:** zero edits to `facts/*.jsonl`, `verifications/*.jsonl`, `SCHEMA_v2.md`, the 7 base specimens, or `frame_lock_data/` (append-only doctrine honoured). `compile_substrate.py` re-run after the build: **validation errors 0, exit 0** — no regression.
**Dials locked this sweep** (frame-lock §7.3): kind vocab + 16-term relation vocab + kernel-admission rule + membrane proxy `l0-membrane-proxy-v0.1`, all per spec as authored.

### What was built
- **`tools/l0_compile_wrappers.py` v1** — STDLIB-ONLY (json, argparse, re, pathlib, datetime, difflib), same constraint as `compile_substrate.py`. Modes: `--check` (semantic diff vs hand wrappers), `--write` (regenerate wrappers + toy data block + group configs), `--substrate` override, `--no-toy`/`--no-groups`. Resolves all paths repo-relative.
- **Derivation (substrate-faithful, fact-backed):** names, abstraction (level / ladder via outgoing subclass-of|instance-of + INVERSE instance-of|subclass-of|brand-of edges + `generalizes_to`/`specializes_to` facts / level_by_scope from scoped `abstraction_level:<scope>` facts), the whole membrane partition (kernel / corroborated_soft / pending / unverifiable / disputed / scars — mechanical from bucket+certainty+estimate-tag), lifecycle (date-valued lifecycle predicates only), relations (outgoing pending/corroborated `rel:*`; the 7 retired `unverifiable` edges land in `membrane.unverifiable`, never `relations[]`), specimen_refs (from `specimen_ref`/`specimen_convergence_ref` facts).
- **Authored render-estimate fields** (spec §2.5 frame weights, §2.8 frame-layer memberships are NOT substrate facts): derived from frame-weight/frame-layer facts WHERE they exist (turing-enigma-hodges has 4 `frames_*` facts; smartphone/aspirin/turing/tueh have structured frame-layer facts), else carried as disclosed compiler constants so group renders keep working. Toy node positions / proposed-node labels / ladder titles are likewise display-only config in the builder, not substrate.

### Check results (compiled substrate vs the 6 hand wrappers)
**145 content diffs found pre-write**, every one categorized — and per doctrine the **substrate value/bucket/predicate wins; the builder never adopts a hand value over the substrate**. After `--write` the wrappers ARE the builder output: re-running `--check` gives **0 diffs (byte-stable / idempotent)**, confirmed again after the substrate recompile.

Diffs by category (all resolved as documented hand-assembly drift / hand-enrichment-beyond-substrate):
1. **Value-snippet transcription drift (~28)** — hand snapshots abbreviated/destructured the substrate value; the substrate (fuller/canonical) value now wins. E.g. `l0-claude-0006` description, `l0-claude-0010` training_method, `l0-alan-turing-0013/0018/0019` (structured dicts flattened by hand), `l0-smartphone-0011/0012` (dropped sub-fields), `l0-acetylsalicylic-acid` aka 3rd element (`acetyl salicylic acid` ← substrate, not the hand's IUPAC `2-acetyloxybenzoic acid`).
2. **Stale certainty not propagated (1)** — `l0-smartphone-0005` hand wrapper still showed `0.82`; substrate was re-banded to `0.45` in the sweep-1 finalize (the finalize updated the TOY but not the hand wrapper JSON). Substrate `0.45` wins.
3. **Predicate-name drift (3)** — hand appended descriptive suffixes (`adapted_imitation_game`, `updated_edition_2014`, `reception_guardian_essential_2002`); the substrate's canonical predicate (`adapted`, `updated_edition`, `reception_guardian_essential`) wins.
4. **7 retired edges moved to `membrane.unverifiable`, out of `relations[]` (~12)** — the sweep-1 finalize demoted 7 reversed/multi-hop edges to `unverifiable`; the hand wrappers still carried some in `relations[]`/`pending` at `pending`. Now: `smartphone-r0002/r0003/r0004`, `alan-turing-r0003/r0004/r0005`, `claude-r0008` are in `membrane.unverifiable`; `relations[]` carries only the pending/corroborated outgoing edges.
5. **Phantom ladder rung dropped + ladder corrected (3)** — `proposed:iphone` had **no backing fact** (spec §2.2: "no ladder edge without a backing fact"), so it is gone: `iphone-15-pro.generalizes_to` = `l0:smartphone` (substrate `rel:instance-of:smartphone`); `smartphone.generalizes_to` = `proposed:device-category` (substrate `rel:instance-of:device-category r0001`, which the hand had dropped).
6. **Bucket correction (2)** — `l0-claude-0021` parameter_count: substrate bucket is `pending` (the hand had pre-classified it `unverifiable` out-of-band). Substrate `pending` wins.
7. **Disputed→pending (3 facts, ~6 diffs)** — `l0-smartphone-0021`, `l0-alan-turing-0007`, `l0-acetylsalicylic-acid-0021` are `bucket=pending` in the compiled view with **no disputed VERIFICATION record** (the `disputed_alternatives` prose lived in the harvest `notes`, which the compiler drops). The substrate-faithful view keeps them in `pending`; a disputed-section appears only when a verifier records a contradiction. (The fact VALUE matches the substrate.)
8. **Membrane completeness (~30)** — the builder lists EVERY pending non-relation fact in the membrane (the full micro-wrapper population, §3); the hand wrappers had selectively omitted meta facts (`kind`, `abstraction_level`, `frame_layer_*`, `iupac_name`, `drug_class`, `term_precursor_1985`, `frontier_replacement_vector`, `specializes_to`, `specimen_ref`, …). Substrate-faithful superset.
9. **Lifecycle date-only (~25)** — the builder emits lifecycle rows only for lifecycle predicates whose VALUE is date-like (event = substrate predicate, when = value, one fact_ref). Hand enrichment dropped: derived `active_from` (no fact), event renames (`claude_first_trained`→`trained`), descriptive-value events parsed into dates by hand (`adapted`/`centenary_edition`/`named "Aspirin"`→`1899-01`), multi-fact_ref groupings, and `description` fields. A future sweep should emit dedicated date facts for the descriptive lifecycle events rather than hand-parsing prose (UI law §5.4: no invented precision).
10. **Hand enrichment with no substrate backing, emptied (~12)** — `membrane.open_questions` (hand-authored candidate-edge prose), unbacked `names.aka` entries (`iphone-15-pro` and `turing-enigma-hodges` have NO `aka` fact), `acetylsalicylic-acid.skipped_relations` (prose block), and `specimen_refs` not backed by a `specimen_ref` fact (`alan-turing`, `turing-enigma-hodges`, `iphone-15-pro`). Builder emits empty (data-absent = nothing).
11. **frame_layer.layer correction (1)** — `alan-turing` hand `straddle` vs substrate fact `l0-alan-turing-0024` `physical`. Substrate fact wins.
12. **fact_refs derivation + cosmetic (~14)** — abstraction/names/frame_layer fact_refs now follow the builder's derivation rule (frame_layer gains fact_refs where a fact backs it); `substrate_binding.fact_id_namespaces` uses the clean template form (hand had appended a parenthetical range).

### Toy regenerated
`../canonical_genealogy/toys/l0_constellation_toy.html`: the inline data region (W / EDGES / CANDS / PLAB / LADDERS) is now wrapped in `/* GENERATED L0 DATA (do not hand-edit — l0_compile_wrappers.py) */ … /* END GENERATED L0 DATA */` (mirrors the `_reembed_agnostic.js` marker/idempotent pattern) and regenerated from the compiled view: per-fact membrane segments (bucket / certainty / predicate / value-snippet / fact_id / source note), the **17 solid fact-backed EDGES**, the **7 retired/inverse edges as CANDS ghosts** (`(retired/inverse)`, never in the solid list — preserving the sweep-1 retired-edge semantics), ladder links, frame weights, and lifecycle events. The render logic below the markers is preserved unchanged. Splice is idempotent (single marker pair on re-run). `node --check` on the extracted `<script>` (to `%TEMP%`): **PASS**.

### Group configs emitted (spec §4)
`group_configs/grp-six-sample-constellation.json` (constellation, depth 1, kernel+membrane, frontier ghosts), `grp-turing-lineage-timeline.json` (timeline, person→book→ai-model→device, `lam` 0.45), `grp-two-ladders.json` (abstraction-ladder, scope toggle global/US/DE, the genericide dial) — first-class JSONs, parameters lifted from the toy's config definitions.

### Spec discrepancy resolved
`L0_WRAPPER_SPEC.md` §1.1 file-map wrote `wrappers/<slug>.wrapper.json` on one line, but every shipped view, the template's `substrate_binding`, the toy embed comment, and the sweep-1 log use the bare `wrappers/<slug>.json` form. **Kept the existing `<slug>.json` naming** (the de-facto convention) and corrected the spec file-map line to match (one-line edit), noted in the builder docstring.

### Verification (this sweep)
- `python tools/l0_compile_wrappers.py --check` → **exit 0, 0 content diffs** (post-write, idempotent; re-confirmed after substrate recompile).
- `python tools/l0_compile_wrappers.py --write` then `--check` → **byte-stable** (0 diffs).
- `node --check` on the toy's extracted script → **PASS**.
- `python ../canonical_genealogy/substrate/compile_substrate.py` → **validation errors 0, exit 0** (no-regression; substrate untouched).
- Open-file sanity: all 6 regenerated wrappers parse; every populated field carries `fact_refs`; `hand_assembled: false`, `compiler: "tools/l0_compile_wrappers.py v1"` on every wrapper. Bucket roll-up matches the substrate (pending 21/21/25/21/23/22; unverifiable 3/0/1/3/0/0; disputed 0 across the board — the 3 hand-disputed facts now sit in `pending`, faithful to the substrate).

### NOT done (deliberately — gated / out of scope)
- **Subject-index anchor (`specimens/l0_catalog.json`, §2.9.4) still NOT created** — remains Pav/Cowork-gated; the 26 expected `specimen 'l0-catalog' not found` flags stay expected-and-honest.
- **No new entities / facts / verifications** — this sweep is tooling only; hardening `pending→corroborated` remains sweep-2's first job (every kernel is still empty, correctly).
- **Lifecycle descriptive-date facts** — the builder intentionally does not hand-parse dates out of prose values; a future sweep should emit dedicated date facts (e.g. for `adapted`, `centenary_edition`, the aspirin `named` event) so those lifecycle rows regenerate from the substrate.

### Proposed vocabulary queue (apply from next sweep after a nod)
- **`generated`/`compiler`/`hand_assembled` are the only stamp fields** the wrapper-view check ignores (plus `_`-prefixed prose and the render-helper keys `note`/`hardness_proxy`/`statement`). Lock this as the wrapper-diff contract.
- Carry forward the sweep-1 proposed dials (relation-direction discipline; proposed-subject edge namespacing) — both are now exercised by the builder and ready to ratify.

---

## Sweep 2 — 2026-06-11 (corroboration: first kernels lit)

**Seat:** `l0-sweep-02-corroborate` (Fable). **The highest-value move per §7.2 step 1 / the sweep-1 "harden, don't broaden" directive.** Sweep 1 left **zero corroborated facts** — every kernel empty. This sweep verifies standing `pending` facts against **genuinely independent, provenance-disjoint second sources** and appends `corroborated` verification records. No entities added, no breadth — verification-only, by design (§7.4: "a sweep that only verified and disputed can be the best of the year").
**No fact edited.** 23 new **append-only** verification records to `../canonical_genealogy/substrate/verifications/l0_catalog.jsonl` (7 → 30 lines). Zero edits to `facts/*.jsonl`, `SCHEMA_v2.md`, the 7 base specimens, or `frame_lock_data/`.
**Dials locked this sweep** (frame-lock §7.3): kind vocab + 16-term relation vocab + kernel-admission rule (§2.3) + membrane proxy `l0-membrane-proxy-v0.1`, all per spec as authored. Verifier seat ≠ the sweep-1 emitter seat (independence, §7.3/§8 agent-stamp rule).

### What was hardened (23 corroborations across all 6 samples + 1 proposed)
Each fact verified against a route **provenance-disjoint** from its sweep-1 harvest source (the cross-route discipline — Wikipedia corroborating Wikidata would be testimony-laundering, per `observer_planes_SKETCH.md` C1).

| subject | route used (independent of harvest source) | corroborated | kernel now |
|---|---|---|---|
| `acetylsalicylic-acid` | **PubChem PUG REST** (NIH/NLM primary registry) | cas, molecular_formula, molecular_weight, iupac_name, canonical_name (5) | **5 kernel** |
| `alan-turing` | **Encyclopaedia Britannica** (disjoint from Wikidata/Wikipedia) | born, died, educated_at, key_publication, fields (5 entity) + instance-of:person (1 rel) | **5 kernel + 1 hardened edge** |
| `iphone-15-pro` | **GSMArena** (disjoint from apple.com + Wikidata) | announced, chip_name, display_size, mass (4) | **4 kernel** |
| `claude` | **claude.com** (Anthropic primary, disjoint from Wikidata) | made_by (1 entity) + made-by:anthropic (1 rel) | **1 kernel + 1 hardened edge** |
| `turing-enigma-hodges` | **Princeton University Press** (publisher primary, disjoint) | subject_person (1 entity) + authored-by:andrew-hodges, adapted-into:imitation-game (2 rel) | **1 kernel + 2 hardened edges** |
| `smartphone` | **Encyclopaedia Britannica** (disjoint from Wikipedia) | definition, emerged, first_commercial_prototype (3) | **3 kernel** |

**Verifications by outcome:** corroborated **23**, disputed **0**, unverifiable **0** (this batch). **Kernel growth: 0 → 19 entity-kernel facts + 4 hardened relation edges** (relations harden in `relations[]` at `bucket=corroborated`, not in `kernel.facts`, which is entity-only — §2.3/§3). Every sample wrapper's kernel went from empty to populated; the kernel-core render lights up for the first time with real battle-tested data.

### Route-character disclosure (the C1 epistemic-route honesty)
Independence is not uniform, and the records say so per-fact rather than claiming a flat "independent":
- **Registry-level physical constants** (aspirin CAS / formula / weight): PubChem is the NIH primary, but Wikidata chem data may sync from CAS/PubChem upstream, so strict provenance-disjointness is *weak*. For a measurable molecular constant the relevant hardening is **multi-registry concordance**, not interpretive independence — disclosed in each note. (The IUPAC name is the one genuinely disjoint chem fact: substrate value was Wikipedia prose, PubChem value is the NIH-computed name.)
- **Provenance-disjoint authority** (Turing dates/publication via Britannica; iPhone specs via GSMArena; book via PUP; smartphone via Britannica): independent editorial line from the harvest source — the strong kind.
- **Primary-vs-aggregator disjoint** (Claude made_by via claude.com): the developer's own site is a distinct route from the Wikidata-sourced harvest fact.
- **Semantic vs verbatim**: the smartphone `definition` is concept-level agreement (two encyclopedias phrase it differently but assert the same thing), flagged as semantic — not a verbatim value-match. Date-range corroborations (smartphone `emerged` 1992–1994 ⊇ Britannica's IBM/1993) are flagged as within-range.

This per-fact route tagging is exactly the proposed **C1 epistemic-route tag** (`observer_planes_SKETCH.md` §3) exercised in anger: cross-route agreement is the gold standard, and the notes record *which* route-character each corroboration rests on so a future reader can weight them.

### Why zero disputes — and the queued dispute-probe (honest)
No disputes is **not** rubber-stamping: this batch deliberately targeted **high-certainty identity facts** (chemical constants, well-attested biographical dates, official product specs, publisher-confirmed authorship) where authoritative independent records agree by construction. The **dispute-likely** facts were *not* probed this sweep and are queued for Sweep 3:
- `l0-smartphone-0011` first_named_device (Ericsson GS88, 1997) — **cert 0.82 from a single blog** (`ericssoners.wordpress.com`), the weakest-sourced kernel-eligible fact; prime dispute-probe candidate.
- `l0-smartphone-0003` named (1997) vs the broader "first use of the term smartphone" literature — contested.
- the population/adoption estimates (`l0-smartphone-0009/0010`, global users/subscriptions) — figures vary by source and date.
- `l0-iphone-15-pro-0013` launch_price_usd 999 — GSMArena showed a *current street price* ($474.53), which neither corroborates nor disputes the $999 MSRP; needs a launch-day primary. **Left pending, honestly** (not recorded as either).

### NOT done (deliberately — gated / deferred)
- **Subject-index anchor (`specimens/l0_catalog.json`) still NOT created** — Pav/Cowork-gated; the ~28 expected `specimen 'l0-catalog' not found` flags stay expected-and-honest.
- **No entities / facts added** — verification-only sweep.
- **`drug_class`, launch_price, original-1983-publication, predecessor edges** — kernel-eligible but not corroborated this batch (no clean independent route fetched yet); carried to Sweep 3.
- **Cross-model external pass owed** — this corroboration is Claude-only; a GPT-5.5 + Gemini pass on the route-character calls is owed if the C1 tagging hardens toward canon.

### Proposed vocabulary queue (apply from Sweep 3 after a nod)
- **Route-character field (PROPOSED):** promote the per-note route disclosure to a structured `route_character ∈ {registry-concordance | provenance-disjoint | primary-vs-aggregator | semantic | within-range}` on the verification record — the operational form of `observer_planes_SKETCH.md` C1. Lets the compiler weight a corroboration by route strength and report a per-route-pair disagreement rate (C3).
- Carry forward the sweep-1 dials (relation-direction discipline; proposed-subject edge namespacing).

### Frontier for Sweep 3
1. **Dispute-probe** the four queued contested facts above (the honest other half of hardening).
2. **Finish the kernel-eligible tail** with clean independent routes: `drug_class` (PubChem MeSH pharm-class), iPhone launch price (launch-day primary), book 1983 first-edition (first publisher / Britannica), the predecessor/successor edges.
3. Then resume **breadth**: promote the `proposed:` frontier entities (apple, anthropic, large-language-model, bayer, andrew-hodges, imitation-game, turing-award, …) to catalog entities.

### Verification (this sweep)
- `python compile_substrate.py` (substrate root): **validation errors 0**, no HAZARD, exit 0; facts 1243, verifications 333. The 23 targets resolve `bucket=corroborated`; per-subject corroborated counts 5/6/4/2/3/3.
- `python tools/l0_compile_wrappers.py --check` pre-write: 42 content diffs, all the expected `membrane.pending → kernel.facts` migration + relation `pending → corroborated`. After `--write`: re-check **0 diffs (idempotent / byte-stable)**.
- Toy `l0_constellation_toy.html` GENERATED block re-spliced (W=6 EDGES=17 CANDS=7 LADDERS=5); the 3 group configs re-emitted.
- Every regenerated wrapper carries `_status` Tier-3 stamp; kernel populations match the compiled buckets (entity-only kernel + corroborated edges in `relations[]`).

---
