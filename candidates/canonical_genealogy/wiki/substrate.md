# SUBSTRATE — Agent Onboarding Wiki

Tier-3 exploratory data-harvest infrastructure for the 7 canonical wrapper-genealogy specimens.
It is an **append-only fact log** + a deterministic compiler that resolves facts to best values for viewer ingestion.
Honest discipline is a hard contract: no fabrication, no silent overwrites, estimates/proxies labelled and capped.

---

## File Map

```
substrate/
  facts/
    <specimen>.entities.jsonl   — entity-lifecycle facts (born/died/founded/…)
    <specimen>.events.jsonl     — event/consolidation/friction/theory-DNA facts
    agnostic_framework.dev.jsonl — self-specimen facts (agnostic-framework)
  verifications/
    <specimen>.jsonl            — verification records keyed on fact_id
  compiled/                     — GENERATED, committed; what viewers ingest
    <specimen>.compiled.json    — best values grouped by subject with provenance
    _summary.json               — coverage/freshness/certainty/disputes rollup
  compile_substrate.py          — the compiler (stdlib only; no third-party deps)
  SUBSTRATE_SPEC.md             — canonical spec for all schemas and rules
  SUBSTRATE_REPORT.md           — post-audit build report (headline numbers)
  .gitignore                    — excludes substrate.db and its WAL siblings
  substrate.db                  — NEVER COMMITTED; rebuilt every run (see .gitignore)
```

**Upstream inputs to compilation (read-only):**
`../specimens/*.json` — the 7 ratified frozen base specimens; loaded only for `subject_id` validation.

---

## Key Function Names in compile_substrate.py

| Function | Purpose |
|---|---|
| `load_specimen_index()` | Glob `../specimens/*.json`; collect every `id` slug and `name`/`who` string per specimen for subject_id validation. |
| `load_jsonl(directory)` | Yield `(path, lineno, obj)` for every parseable JSON line; skip blank/comment lines (`//`, `#`). |
| `validate_fact(obj, specimen_index)` | Check required fields, source shape, certainty range, `verification=="pending"` at emit, `contribution_share` certainty cap ≤ 0.6, `subject_id` against specimen index. Returns `(errors, flags)`. |
| `validate_verification(obj)` | Check required fields, status enum, second_source shape. |
| `bucket_for(fact_id, verifs_by_fact)` | Assign a verification bucket from all verification records targeting a fact_id: corroborated > disputed > unverifiable > pending. |
| `sort_key(fact, bucket)` | Build the lexicographic best-value tuple: `(BUCKET_RANK, certainty, epoch, _InvStr(fact_id))`. |
| `_InvStr` | Wrapper class so `max()` picks the **smallest** `fact_id` on a tie (stable tiebreak). |
| `resolve_best(facts, verifs_by_fact)` | Group by `(specimen, subject_id, predicate)`; select best fact; collect `disputed_alternatives`. Returns `best_rows`. |
| `build_db(facts, verifs, best_rows)` | Write `substrate.db` (tables: `facts`, `verifications`, `best_values`). Drops and recreates every run. |
| `write_compiled_exports(best_rows, generated)` | Write `compiled/<specimen>.compiled.json` per specimen. |
| `write_summary(best_rows, facts, verifs, errors, flags, generated)` | Write `compiled/_summary.json`. |
| `main()` | Orchestrates all of the above; prints the build report to stdout; exits 2 on fatal errors, 1 on flags if `--strict`. |

---

## Data Contracts

### Fact record (one JSON object per line in `facts/*.jsonl`)

```jsonc
{
  "fact_id":      "f-maxwell-0001",          // unique stable kebab slug; convention f-<specimen>-<nnnn> (entities)
                                             // or f-<specimen>-e<nnnn> (events) — MUST be disjoint across files
  "specimen":     "maxwell-electromagnetism",// exact specimen_id from ../specimens/*.json
  "subject_id":   "James Clerk Maxwell",     // exact node id slug OR node name/who string OR "proposed:<slug>"
  "predicate":    "born",                    // controlled vocabulary (see SUBSTRATE_SPEC.md §2.1)
  "value":        "1831-06-13",              // string | number | bool | object | array
  "when":         "1831-06-13",              // OPTIONAL: event date (ISO-8601 partial ok); omit for non-temporal
  "source": {
    "url":   "https://...",                  // REQUIRED: real http(s) URL; never fabricated
    "title": "...",
    "type":  "encyclopedia",                 // one of: aggregator | primary | encyclopedia | news | academic
    "published_or_updated": "2026-05-30"    // "" if unavailable
  },
  "retrieved_at": "2026-06-10T02:25:23Z",    // UTC ISO-8601 retrieval stamp
  "certainty":    0.9,                        // [0,1] per certainty rubric; contribution_share MUST be ≤ 0.6
  "verification": "pending",                  // ALWAYS "pending" at emit time; changed only via verification records
  "agent":        "fable-harvester-01",       // harvesting agent/seat identifier
  "notes":        "..."                       // REQUIRED for any estimate/proxy; OPTIONAL otherwise
}
```

### Verification record (one JSON object per line in `verifications/*.jsonl`)

```jsonc
{
  "fact_id":      "f-maxwell-0001",           // the fact being verified (MUST match an existing fact_id)
  "status":       "corroborated",             // one of: corroborated | disputed | unverifiable
  "second_source": { "url": "...", "title": "...", "type": "...", "published_or_updated": "..." },
  "value_found":  "1831-06-13",               // verbatim value the second source gave
  "retrieved_at": "2026-06-10T02:34:17Z",
  "verifier":     "claude-sonnet-4-6",
  "notes":        ""
}
```

### Compiled export (`compiled/<specimen>.compiled.json`) — GENERATED, do not hand-edit

```jsonc
{
  "_doc": "...",
  "specimen": "maxwell-electromagnetism",
  "generated": "<ISO timestamp>",
  "subjects": {
    "<subject_id>": [
      {
        "predicate": "born", "value": "1831-06-13", "when": "1831-06-13",
        "bucket": "corroborated", "certainty": 0.9,
        "best_fact_id": "f-maxwell-0001",
        "source": { ... },
        "provenance_refs": ["f-maxwell-0001"],
        "disputed_alternatives": [...]   // present only when disputes exist
      }
    ]
  }
}
```

### Append-only / generated / ratified-frozen status

| Path | Status |
|---|---|
| `facts/*.jsonl` | APPEND-ONLY source of truth. Never edit or delete existing lines. |
| `verifications/*.jsonl` | APPEND-ONLY source of truth. Never edit or delete existing lines. |
| `substrate.db` | GENERATED, NEVER COMMITTED. Rebuilt from scratch on every run. |
| `compiled/<specimen>.compiled.json` | GENERATED, committed. Regenerate by running compile_substrate.py; never hand-edit. |
| `compiled/_summary.json` | GENERATED, committed. Same. |
| `SUBSTRATE_SPEC.md` | RATIFIED SPEC. Do not edit without explicit ratification. |
| `SUBSTRATE_REPORT.md` | RATIFIED BUILD REPORT. Do not edit; update by running a new build and appending a new section. |
| `../specimens/*.json` | RATIFIED FROZEN base specimens. compile_substrate.py reads them but never writes them. |

---

## Certainty Rubric

| Band | Situation | Range |
|---|---|---|
| Structured-aggregator-attested | Wikidata, official org page, structured DB entry with exact datum | 0.7 – 0.9 |
| Single encyclopedia | Wikipedia/Britannica prose | 0.5 – 0.7 |
| Single news | One news article | 0.4 – 0.6 |
| Historiographic estimate / proxy | contribution_share, inferred date, modelled value | 0.2 – 0.5; notes MUST state basis |

Hard rules:
- `contribution_share` facts MUST have `certainty <= 0.6`. `validate_fact` enforces this with a FLAG.
- Any proxy/estimate MUST have `"ESTIMATE:"` or `"PROXY:"` in `notes`.
- `certainty` is NEVER changed by verification. Bucket changes resolution rank, not the certainty field.

---

## Verification State Machine

```
emit a fact → pending
  verification record arrives (keyed by fact_id):
    any corroborated  →  bucket = corroborated  (highest trust)
    else any disputed →  bucket = disputed       (demoted below pending)
    else unverifiable →  bucket = unverifiable   (pending-level trust, flagged)
    else (no records) →  bucket = pending
```

Best-value resolution precedence (lexicographic, `sort_key`):
1. `BUCKET_RANK`: corroborated(3) > pending(2) = unverifiable(2) > disputed(1)
2. `certainty` (higher wins)
3. `retrieved_at` epoch (newer wins)
4. Smallest `fact_id` lexicographically (`_InvStr` wrapper, stable tiebreak)

Disputed values are NEVER dropped: `resolve_best` collects them into `disputed_alternatives` on the best-value row and `write_summary` places them in `_summary.json → disputes[]`.

---

## GOTCHAS (the traps)

**1. HAZARD: fact_id reuse across different resolution groups — FATAL exit 2.**
`compile_substrate.py` detects any `fact_id` that appears in facts belonging to DIFFERENT `(specimen, subject_id, predicate)` groups and raises a fatal `HAZARD` error. The only safe fix: use disjoint namespaces across files for the same specimen. Convention: entities file uses `f-<specimen>-<nnnn>`; events file uses `f-<specimen>-e<nnnn>`. (This was a real pipeline defect in the first build: `maxwell` and `manhattan` shared a namespace, causing verification records to leak between unrelated groups, silently inflating corroboration and dispute counts.)

**2. Never read large .jsonl files whole in one pass.**
The 14 fact files total ~1029 records; the largest individual files have 60-80 lines at ~500 bytes each. They are manageable today but will grow. Always use streaming / `load_jsonl` (it reads line-by-line). Do NOT slurp the entire JSONL as a JSON array — it is not valid JSON (no array wrapper).

**3. compiled/*.compiled.json and _summary.json are GENERATED — never edit by hand.**
The `_doc` key states this explicitly. Any hand-edit will be clobbered by the next `python compile_substrate.py` run. To change a compiled value, edit the source fact in `facts/*.jsonl` and recompile.

**4. substrate.db is NEVER committed.**
It is in `.gitignore`. If you see it in a working tree diff, do not stage it. It is rebuilt from scratch on every compile run (`build_db` calls `DB_PATH.unlink()` before recreating).

**5. `verification` field in a fact record is always "pending" at emit time.**
`validate_fact` flags any other value. A verifier changes effective status by appending a verification RECORD in `verifications/*.jsonl` — not by editing the fact's own `verification` field.

**6. `subject_id` must be the exact base-specimen node id slug or node name/who string.**
`load_specimen_index` / `_walk_collect` walks every `id`, `name`, and `who` key in the specimen JSON. If your subject is not in the specimen, use `proposed:<slug>`. Unknown non-proposed subject_ids are flagged (non-fatal) but visible in the build output.

**7. `source.url` must be a real http(s) URL.**
`validate_fact` flags non-http URLs as "provenance suspect" but does not error. The `agnostic_framework.dev.jsonl` facts correctly use local file paths for self-specimen data (`type: "primary"`) — these will be flagged, which is expected and honest.

**8. CRLF warnings are normal** on Windows. The JSONL files were authored on Unix; `git diff` may show CRLF noise. This does not affect the compiler (it reads `encoding="utf-8"` via `Path.read_text`).

**9. No third-party dependencies.** compile_substrate.py uses only `json`, `sqlite3`, `argparse`, `pathlib`, `datetime`. Do not introduce imports without checking this constraint.

**10. Retraction records, not deletions.** When a fact's provenance is found to be wrong, the correct fix is: (a) append a new corrected fact with proper provenance, and (b) append a verification record on the OLD fact with `status: "unverifiable"` and a `notes` explaining the provenance failure. The old line stays in the JSONL. See `f-qm-relativity-0025` / `f-qm-relativity-0057` in SUBSTRATE_REPORT.md §10.1 for the canonical example.

---

## How to Add Data Safely (checklist)

1. **Identify the correct file.** Entities (people, orgs, theories with lifecycle dates) → `facts/<specimen>.entities.jsonl`. Events (dated occurrences, consolidations, friction, now-refresh, theory-DNA) → `facts/<specimen>.events.jsonl`. New specimen → create `facts/<newspecimen>.entities.jsonl` and `facts/<newspecimen>.events.jsonl`.

2. **Assign a disjoint `fact_id`.** Check the last id in both `.entities.jsonl` and `.events.jsonl` for that specimen. Entities: `f-<specimen>-<nnnn>` (e.g. `f-maxwell-0135`). Events: `f-<specimen>-e<nnnn>` (e.g. `f-maxwell-e0070`). Never reuse an id from another file in a different group.

3. **Set `verification: "pending"`** in the fact record. Always. Never set `corroborated` etc. directly on the fact.

4. **Set `certainty` per the rubric.** If the fact is a `contribution_share`, cap at 0.6. If it is any estimate or proxy, put `"ESTIMATE:"` or `"PROXY:"` in `notes` and score in 0.2–0.5.

5. **Never fabricate a URL.** If you cannot find a real source, skip the fact. If the source dies or fails to attest the value after the fact is emitted, append a retraction verification record (status `unverifiable`), then append a re-sourced fact.

6. **Append, never edit.** Open the target `.jsonl` in append mode. Write one JSON object per line, no trailing commas, no array wrapper. The file must remain valid JSONL.

7. **To add a verification**, append to `verifications/<specimen>.jsonl`. Key it to an existing `fact_id` from step 2. Use `status` in `{corroborated, disputed, unverifiable}`. Always provide a real `second_source`.

8. **Recompile and verify the build is clean:**
   ```
   python compile_substrate.py
   ```
   Expected: `validation errors: 0`. Review any new flags in the output. If a HAZARD error appears, your `fact_id` namespace collides — renumber.

---

## Verification (how to prove your change works)

1. Run `python compile_substrate.py` from `substrate/`.
2. Check stdout: `validation errors: 0`. Any non-zero error count means a record was skipped.
3. Check that your new fact appears in `compiled/<specimen>.compiled.json` under the correct `subject_id` and `predicate`.
4. Check `compiled/_summary.json → totals.facts` incremented by the number of new facts you added.
5. If you added a verification record, check `compiled/_summary.json → totals.verifications` and that the affected `best_values` entry shows the updated `bucket`.
6. If `--strict` is required (CI gate), run `python compile_substrate.py --strict` — exits non-zero on any flag.
7. `substrate.db` is generated but never committed. Do not stage it.
8. Commit only `facts/*.jsonl`, `verifications/*.jsonl`, and `compiled/*.json` / `compiled/_summary.json`.

---

*This wiki page was generated by a Wiki Scout agent reading the actual substrate files. Cite SUBSTRATE_SPEC.md for the authoritative schema and SUBSTRATE_REPORT.md for build history.*
