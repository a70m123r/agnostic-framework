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
