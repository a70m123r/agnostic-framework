# Data Layer — Agent Onboarding

**What this area is.** The data layer is the schema-governed JSON corpus that drives the viewers. It consists of: one ratified schema spec (SCHEMA_v2.md), 8 specimen JSON files, 8 overlay JSONs, 8 narration JSONs, a substrate fact/verification/compiled tree, and the embed wiring that stitches them into viewer_v3.html. Every viewer panel, timeline node, and narration segment is rendered from these files — the viewer contains no hard-coded content.

**Your mandate.** Modify this area without breaking schema discipline, the ratified-frozen files, or the embed regeneration pipeline.

---

## File Map

```
candidates/canonical_genealogy/
  SCHEMA_v2.md                         — ratified schema spec (FROZEN, never edit)
  one_specimen.v2.template.json        — fill template for v2 specimens (all optional R#/D# fields pre-marked)
  one_specimen.template.json           — v1 fill template (kept for the 3 v1 specimens)

  specimens/
    maxwell.json                       — ratified, FROZEN
    darwin_mendel.json                 — ratified, FROZEN
    qm_relativity.json                 — ratified, FROZEN
    keynesian.json                     — ratified, FROZEN
    deep_learning.json                 — ratified, FROZEN
    manhattan.json                     — ratified, FROZEN
    internet.json                      — ratified, FROZEN
    agnostic_framework.json            — the reflexive self-specimen (living, may be updated
                                         via _reembed_agnostic.js pipeline only)

  overlays/
    <specimen>.overlay.json            — additive overlay per specimen (entity lifecycles,
                                         harvest_dates, rival_fates, theory_dna)

  narration/
    <specimen>.narration.json          — per-era running commentary; refs discipline enforced

  substrate/
    SUBSTRATE_SPEC.md                  — fact-record format, certainty rubric, compiler rules
    facts/<specimen>.entities.jsonl    — append-only entity fact log
    facts/<specimen>.events.jsonl      — append-only event fact log
    verifications/<specimen>.jsonl     — corroboration/dispute records
    compile_substrate.py               — deterministic compiler
    substrate.db                       — compiled SQLite artifact (NOT committed, .gitignore)
    compiled/<specimen>.compiled.json  — best-value exports (committed; viewers ingest these)
    compiled/_summary.json             — coverage/freshness/certainty summary

  _reembed_agnostic.js                 — regenerates the 3 agnostic_framework embed blocks
                                         in viewer_v3.html from the canonical source files

  viewer_v3.html                       — the live viewer (1.28 MB; 32 embedded JSON blocks;
                                         MAY receive surgical additive edits with gates below)
```

Key JS functions in viewer_v3.html relevant to data loading: `document.querySelectorAll('script[type="application/json"]')` (line ~214) iterates all 32 embed blocks to hydrate the data model; `buildModel()` assembles the runtime graph; `selectSpecimen()` switches the active specimen; `ovl()`, `ovlLifecycle()`, `ovlRivalFate()`, `ovlHarvestDate()`, `ovlTheoryDNA()`, `ovlNowExt()` read overlay fields; `render()` draws to canvas; `__lint()` runs the faithfulness lint (call `__lint()` in console or append `#lint` to the URL).

---

## DATA CONTRACTS

### SCHEMA_v2.md — the 11 top-level groups

Every specimen JSON must conform. The groups are:

| Group | Description |
|---|---|
| `child` | The emergent wrapper W_C — `name`, `kernel`, `frame[]`, `frame_layer`, `status`, `status_trajectory`, `confidence`, `utility` |
| `weld` | The merge event — parents, seam (S), surprise, survived/dropped, lifecycle (D1), dormancy/revival, candidate_children, forcing refs |
| `roots` | DOWN recursion — `sub_wrappers[]` toward people and place |
| `harvest` | UP recursion — `descendants[]` and `cultural_harvest[]` |
| `relatives` | WIDE edges — cousin/influence/sibling/rival |
| `actors` | NEW (D2) — generalized ground kernel, single store; replaces v1 `roots.people_0` |
| `fuzzy_layer` | `certain_core[]`, `frontier[]`, `core_boundary_locus` — DERIVED digest of per-node confidences, not an independent source |
| `discrepancies` | Record conflicts, framework-vs-record tensions; a new weld_type/phase term MUST be proposed here before use |
| `forcing_events` | NEW (D4) — external pull/squeeze events (war, funding, fashion, politics, economic-crisis, technology, religion) |
| `sources` | Citation backbone — every load-bearing field must trace here |
| `schema_capabilities` | Static header block — declares D3 `layer_filter` + D5 `graded_membership` |

Critical sub-contracts:

**Weld / lifecycle (D1).** `weld.lifecycle` is a weighted INDEX over `dormancy_intervals`, `revival`, `status_trajectory`, `candidate_children` — it does NOT restate their content. `phase_trajectory[]` entries carry `membership ∈ [0,1]`, no separate confidence (weights not hard values). `weld_type[]` same. Default for a sharp weld: empty `phase_trajectory` (= single `consolidation` at 1.0) + `{type:"unifier-weld", weight:1.0}`.

**Weld / D6 cluster.** `opposes[]` (D6a) reuses the framework's `a_charge` adversarial primitive; `gates[]` (D6b) records permit/block/delay gatekeepers; `weld.lag` (D6c) gives causal why-it-waited; `propagation` (D6d) is the most-conjectural field (one attested case). All default-empty.

**Actors (D2).** `actors[]` is the single store for the ground kernel — v1's `roots.people_0` is folded in as `kind:individual`. Each actor node carries `carrier_of[]` (champions latent wrappers UP) and `inhabitant_of[]` (operates WITHIN other wrappers). These are the explicit physical/latent bridge. On a sharp case fill individuals as in v1; leave `carrier_of`/`inhabitant_of` and non-individual kinds empty unless genuinely load-bearing.

**fuzzy_layer is DERIVED.** `certain_core[]`/`frontier[]` are a human-readable summary derived from the per-node `confidence`/`membership` values — the memberships are the ground truth. Never treat the two-bin lists as an independent source.

**Confidence orthogonality.** `weld.surprise_confidence` ⊥ `child.confidence` — a maximally fertile seam (high `surprise_confidence`) can coexist with an unborn child (low `child.confidence`). Never read one off the other.

**Design law.** Every R# and D# field is OPTIONAL and DEFAULTS EMPTY on a clean sharp weld. If filling a v2 field feels forced, leave it empty — empty is correct signal.

**Convergence list stays 9.** Specimens are calibration instruments, not new convergences. No tier promotion. Surprise stays qualitative (no fabricated bit values). `bits_note` is qualitative only; may be `"principled-null"` on a frontier.

---

### Overlays — additive contract

Each `overlays/<specimen>.overlay.json` is ADDITIVE — it never duplicates base specimen fields. Shape:

```json
{
  "_doc": "...",
  "specimen": "<id>",
  "now_extension": [{ "when", "what", "kind", "confidence" }],
  "entity_lifecycles": {
    "<entity name>": { "born"/"died"/"conceived"/"formulated"/"named"/"dissolved", "confidence", "_note" }
  },
  "harvest_dates": {
    "descendants[N]": { "emerged", "consolidated", "confidence", "_note" },
    "cultural_harvest[N]": { ... },
    "action_spaces_unlocked[N]": { ... }
  },
  "rival_fates": {
    "<rival name>": { "fate", "when", "confidence" }
  },
  "theory_dna": {
    "_estimate_note": "(MANDATORY: must disclaim these are historiographic ESTIMATES, never measured bits)",
    "parents": {
      "<parent name>": { "load_bearing_share", "basis" }
    },
    "novel_residue": { "share", "basis" }
  },
  "sources": [{ "name", "year", "url", "used_for" }],
  "web_grounded": true
}
```

**theory_dna discipline.** Shares are historiographic ESTIMATES (confidence ≤ 0.6, overall cap). They are conceptually `gain_v2` decompositions — no measured `gain_v2` numbers exist for any specimen. Never render these as measured bits. `_estimate_note` is mandatory to prevent a future agent from presenting them as data-bound.

---

### Narration — segment shape and refs discipline

Each `narration/<specimen>.narration.json` has:

```json
{
  "_doc": "...",
  "specimen": "<id>",
  "voice": "...",
  "generated": "<date>",
  "segments": [
    {
      "from": <year>,
      "to": <year>,
      "title": "...",
      "text": "...",
      "refs": ["f-<specimen>-NNNN", "specimen:<dot.path>", "overlay:<key>"],
      "era_kind": "pre-history|roots|dormancy|forcing|weld|hardening|..."
    }
  ]
}
```

**Refs discipline (non-negotiable).** Every factual claim in `text` must trace to one of:
- `f-<specimen>-NNNN` — a substrate fact_id in `substrate/facts/*.jsonl`
- `specimen:<dot.path>` — a field path in the base specimen JSON
- `overlay:<key>` — a key in the overlay JSON

No new claims may appear in narration text without a corresponding ref. The `#lint` mode in viewer_v3.html validates that every `f-*` ref resolves to a compiled substrate entry — a missing ref renders as a `miss` chip, which is the visible signal of a broken ref.

---

### Data-key embed wiring

viewer_v3.html contains 32 `<script type="application/json">` blocks, each identified by an `id` attribute:

| Prefix | Count | Example | Source |
|---|---|---|---|
| `spec-` | 8 | `spec-maxwell` | `specimens/<specimen>.json` |
| `ovr-` | 8 | `ovr-maxwell` | `overlays/<specimen>.overlay.json` |
| `narr-` | 8 | `narr-maxwell` | `narration/<specimen>.narration.json` |
| `subs-` | 8 | `subs-maxwell` | `substrate/compiled/<specimen>.compiled.json` (slim/compiled form) |

The 7 base specimens' embed blocks are static (written at build time, not regenerated automatically). The `agnostic_framework` blocks (the 8th set) are regenerated by `_reembed_agnostic.js`:

```
node _reembed_agnostic.js
```

This script reads the canonical files, applies `embedJSON()` (ASCII-safe, `</`→`<\/` guarded), and calls `replaceBlock()` to patch the 3 agnostic data blocks in place. It does NOT regenerate the substrate embed — that uses a pre-compiled slim form from the substrate compiler.

---

## GOTCHAS

**1. Huge files — never read whole.** viewer_v3.html is ~1.28 MB (~515,000 tokens). Do NOT read it whole. Use offset+limit for specific sections, or grep for function/variable names by pattern. The embedded JSON blocks (lines 162–193) are all on single minified lines — grep content on those lines returns `[Omitted long matching line]`.

**2. Embeds are GENERATED, never hand-edited.** The 3 agnostic_framework blocks inside viewer_v3.html have a comment at line 190: `<!-- GENERATED EMBED (do not hand-edit) -->`. Re-run `node _reembed_agnostic.js` after editing any of `specimens/agnostic_framework.json`, `overlays/agnostic_framework.overlay.json`, or `narration/agnostic_framework.narration.json`. The 7 base specimen embeds are static and must be patched by a similar mechanism if their source files ever change (they are FROZEN — they should not change).

**3. ASCII-only commit text / embed encoding.** `embedJSON()` in `_reembed_agnostic.js` escapes every non-ASCII character to `\uXXXX`. The VIEWER_SPEC.md notes this style keeps the HTML ASCII-safe. When writing any JSON that will be embedded, non-ASCII characters will be escaped. This is correct behavior, not corruption.

**4. `node --check` gate.** The extracted app script in viewer_v3.html must pass `node --check` both standalone and as embedded. This is the syntax gate. After ANY edit to viewer_v3.html's script section, run: `node --check viewer_v3.html` (Node can syntax-check an HTML file's embedded scripts this way, or extract the script block and check it). The VIEWER_SPEC.md records this gate as a build requirement at every addendum.

**5. The `#lint` gate.** Append `#lint` to the URL (e.g. `http://localhost:8742/viewer_v3.html#lint`) or call `window.__lint()` in the console. This runs the render-faithfulness linter which asserts: (a) every narration `f-*` ref resolves in the embedded substrate (no silent miss-chips); (b) no fabricated proxy values render as data-bound; (c) every substrate fact carries a source. A lint badge appears in the header. Pass this before declaring a viewer change correct.

**6. CRLF warnings are normal.** The repo has Windows line endings in some files. `node --check` may emit CRLF-related warnings — these are non-fatal and expected. Do not conflate them with syntax errors.

**7. substrate.db is NOT committed.** It is in `substrate/.gitignore`. Only `compiled/*.compiled.json` and `compiled/_summary.json` are committed. If you need to regenerate substrate artifacts, run `compile_substrate.py` — it emits `substrate.db` locally and re-writes the committed compiled JSONs.

**8. The 7 base specimens are RATIFIED-FROZEN.** `specimens/maxwell.json`, `darwin_mendel.json`, `qm_relativity.json`, `keynesian.json`, `deep_learning.json`, `manhattan.json`, `internet.json` — DO NOT EDIT. Any data gap these specimens have is filled via the overlay and substrate, not by editing the base. `agnostic_framework.json` is living but must be edited only via the `_reembed_agnostic.js` pipeline to stay consistent with its viewer embed.

**9. `roots.people_0` is removed in v2.** v1 specimens used `roots.people_0[]`; v2 folds this into `actors[]` with `kind:individual`. If you are reading v1 specimens, expect `people_0` there. For any new work use `actors[]` only. Do not create a dual-store.

**10. `theory_dna` shares are proxies — never present as measured.** The overlay `_estimate_note` is the disclosure. If you render or quote these shares, always accompany them with the disclosure text. Proxy-disclosure is a standing discipline in this repo.

**11. `lifecycle` indexes, does not restate.** A common authoring mistake is duplicating content between `weld.dormancy_intervals[]` / `weld.revival` and `weld.lifecycle.phase_trajectory[]`. The lifecycle carries phase membership weights and timing; the primitives carry the causal content. Write the causal content in the primitives; let the lifecycle reference them by phase label.

---

## HOW TO MODIFY SAFELY

For overlay edits (adding `entity_lifecycles`, `harvest_dates`, `rival_fates`, `now_extension`):
1. Edit the source `overlays/<specimen>.overlay.json` only.
2. Confirm the JSON is valid (`python -c "import json; json.load(open(...))"`) .
3. For the 7 base specimens: the overlay embed (`ovr-<specimen>` block) in viewer_v3.html is static and must be updated by extracting that block, replacing its content, and re-inserting using the same `replaceBlock()` pattern as `_reembed_agnostic.js`.
4. For `agnostic_framework`: run `node _reembed_agnostic.js`.
5. Run `node --check viewer_v3.html` (syntax gate).
6. Open `http://localhost:8742/viewer_v3.html#lint` and confirm lint passes.

For narration edits:
1. Every new factual claim must have a ref (`f-*`, `specimen:`, or `overlay:`).
2. `f-*` refs must match real `fact_id` values in `substrate/facts/*.jsonl`.
3. Same re-embed, node --check, and lint steps as overlays.

For substrate edits (adding facts):
1. Append-only to `substrate/facts/<specimen>.entities.jsonl` or `.events.jsonl`. Never edit existing lines.
2. Run `python substrate/compile_substrate.py` to regenerate `compiled/*.compiled.json`.
3. The compiled JSON is the subs-embed source — update the `subs-<specimen>` block in viewer_v3.html using the `replaceBlock()` pattern.
4. `node --check` and `#lint` gates.

For viewer_v3.html surgical edits (state hooks, new panels):
1. Read only the relevant offset+limit range; do not read the whole file.
2. Additive only — do not remove or rewrite existing logic.
3. `node --check` must pass after the edit.
4. `#lint` must pass.
5. Reload in browser via `http://localhost:8742/viewer_v3.html` to confirm rendering.

For new specimens (if ever):
1. Use `one_specimen.v2.template.json` as the fill template.
2. Fill `child` + `weld.parents` + `surprise` first (the certain core); add v2 fields only where the record forces it.
3. Add `specimen_id` to header; fill `extends.phase1_class_name` to link back to wrapper_classes_phase1.json.
4. A new `weld_type` or lifecycle phase term must first appear as a `discrepancies[]` row of type `framework-vs-record-tension` before being used in the `lifecycle.weld_type[]` field.
5. Create matching overlay, narration, and substrate files.
6. Embed all 4 blocks in viewer_v3.html using `replaceBlock()` pattern.
7. `node --check` + `#lint` + browser verification.

---

## VERIFICATION

After any change, the full verification sequence is:

```
# 1. JSON validity (all data files)
python -c "import json, glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True) if '.git' not in f]"

# 2. Reembed agnostic if agnostic_framework files changed
node _reembed_agnostic.js

# 3. JS syntax gate
node --check viewer_v3.html

# 4. Substrate recompile if facts changed
python substrate/compile_substrate.py

# 5. Browser lint gate
# Open: http://localhost:8742/viewer_v3.html#lint
# Assert: lint badge = PASS, zero miss-chips in narration refs

# 6. Visual regression
# Single specimen: select each affected specimen, scrub timeline, open detail panel
# Global view: toggle GLOBAL, verify all 7+1 lanes render
```

CRLF warnings from Node are non-fatal. A `miss` chip in the narration refs panel means a narration `f-*` ref does not resolve in the substrate — that is a broken ref and must be fixed before shipping.
