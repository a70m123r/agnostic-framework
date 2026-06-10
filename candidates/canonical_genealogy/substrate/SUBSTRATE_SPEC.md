# Compiled Substrate — fact schema, certainty rubric, verification state machine, scale story

**Status:** Tier-3 exploratory data-harvest infrastructure for the canonical wrapper-genealogy specimens. NOT canon, NOT a tier promotion, does NOT grow the convergence list. This directory is the **harvest substrate**: an append-only fact log + a deterministic compiler that resolves facts to best values for viewer ingestion.

**Honest discipline (non-negotiable):** NO fabrication, ever. Skip a fact rather than guess. Every fact carries provenance (a real source URL + retrieval stamp). Proxies and estimates are labelled as such, with a stated basis, and capped low on certainty. Disputed facts keep BOTH values — the compiler never silently overwrites.

This spec defines:
1. the **fact record** format (one JSON object per line in `facts/*.jsonl`),
2. the **verification record** format (`verifications/*.jsonl`),
3. the **certainty rubric** (how to score `certainty ∈ [0,1]`),
4. the **verification state machine** (`pending → corroborated | disputed | unverifiable`),
5. **freshness conventions**,
6. the **best-value resolution order** the compiler applies,
7. the **scale story** (git-native source of truth, SQLite compiled artifact, committed JSON exports).

---

## 1. What the substrate is (and is not)

The 7 base specimens at `../specimens/*.json` are **ratified and frozen**. They are NOT edited by the harvest. Instead, harvesters **append facts** that fill the known gaps (entity lifecycles, consolidation dates, now-refresh events, rival fates, D6 friction data, theory-DNA bases). Each fact names the exact specimen node it augments (`subject_id`) and the schema-ish field it fills (`predicate`).

The compiler reads all facts + verifications, validates them, resolves each `(specimen, subject_id, predicate)` triple to a single **best value** while keeping the full history, and emits:
- `substrate.db` — a SQLite compiled artifact (**never committed**, see `.gitignore`),
- `compiled/<specimen>.compiled.json` — best values grouped by subject, with provenance refs (**committed**; this is what viewers ingest),
- `compiled/_summary.json` + a stdout summary — coverage, freshness, certainty, and disputes.

The base specimens are **inputs to validation only** — the compiler loads them to check that each non-`proposed:` `subject_id` is a real node id (or node `name`) somewhere in the specimen. Unknown subjects are **flagged, not fatal** (the harvest can run ahead of node-id reconciliation).

---

## 2. The fact record (`facts/*.jsonl`)

One fact per line. One JSON object per line (JSONL — no array wrapper, no trailing commas, no comments). Append-only: never edit or delete an emitted line; to revise, append a **newer** fact (the compiler prefers fresher + more-certain + corroborated values).

```jsonc
{
  "fact_id":     "f-maxwell-0001",          // REQUIRED. Unique, stable, kebab/slug. Convention: f-<specimen>-<nnnn>.
  "specimen":    "maxwell-electromagnetism", // REQUIRED. Exact specimen_id from ../specimens/<file>.json.
  "subject_id":  "act-faraday",             // REQUIRED. The EXACT base-specimen node id (the "id" slug if the node has one,
                                            //   else the node "name" / "who" string, matched verbatim),
                                            //   OR "proposed:<slug>" for a NEW node that this fact-set introduces.
  "predicate":   "born",                    // REQUIRED. The schema-ish field this fact fills (see §2.1 vocabulary).
  "value":       "1791-09-22",              // REQUIRED. The asserted value (string | number | bool | object | array).
  "when":        "1791-09-22",              // OPTIONAL. Event date for a TEMPORAL fact (ISO-8601, partial OK: "1885",
                                            //   "1887-11"). Omit for non-temporal facts (e.g. a contribution share).
  "source": {                               // REQUIRED. Real, fetched provenance. NEVER fabricate a URL.
    "url":   "https://en.wikipedia.org/wiki/Michael_Faraday",
    "title": "Michael Faraday — Wikipedia",
    "type":  "encyclopedia",                // one of: aggregator | primary | encyclopedia | news | academic
    "published_or_updated": "2026-05-30"    // page's published/last-updated date if available, else best estimate; "" if none.
  },
  "retrieved_at": "2026-06-10T02:18:07Z",   // REQUIRED. UTC stamp at retrieval. Get via shell: date -u +"%Y-%m-%dT%H:%M:%SZ".
  "certainty":    0.6,                       // REQUIRED. [0,1] per the rubric in §3.
  "verification": "pending",                 // REQUIRED. Always "pending" at fact-emit time. Verifiers act via §4 records.
  "agent":        "fable-harvester-01",      // REQUIRED. Identifier of the harvesting agent/seat.
  "notes":        "Aggregator-attested DOB; basis stated here for any estimate/proxy."  // OPTIONAL but REQUIRED for any estimate/proxy.
}
```

### 2.1 `predicate` vocabulary (the gap-targets)

Predicates are **schema-ish field names** — they should map to a SCHEMA_v2 field or be a clearly-named harvest extension. Suggested controlled set (extend as needed, but prefer reuse):

- **Entity lifecycles** — `born`, `died`, `founded`, `dissolved`, `conceived`, `formulated`, `named`, `active_from`, `active_to`.
- **Consolidation dates** — `consolidated`, `unlocked_when` (for an `action_spaces_unlocked` item), `harvested_when` (for a `cultural_harvest` / `descendants` item).
- **Now-refresh (2024–2026)** — `now_refresh_event` (value is the event; `when` is the date).
- **Rival fates** — `rival_fate` (value ∈ `faded | absorbed | persists | niche`), with `when` = the date the fate consolidated.
- **D6 friction** — `gatekeeping_event`, `publication_lag`, `adoption_lag`, `propagation_fact`, `bandwidth_fact`.
- **Theory-DNA** — `contribution_share` (value is a number in [0,1] or a labelled object; certainty MUST be ≤ 0.6 with basis in `notes`).
- **Misc cleanly-aggregated** — any other field an aggregator provides that maps to a schema field; name it after the schema field.

If a predicate fills a slot **inside** a list item (e.g. one of several `action_spaces_unlocked`), disambiguate it in `subject_id` (use the item's `id` if present, else `proposed:` it) — do not collide many list-items onto one subject.

### 2.2 `subject_id` resolution

- If the targeted base node has an `id` slug (v0.2 specimens: `manhattan`, `internet`, `deep_learning`, `keynesian` use `act-*`, `sw-*`, `pf-*`, `h-*`, `rel-*`, `fe-*`, `child-*`, `weld-*`), use that **exact slug**.
- If the node has no `id` (v0.1 specimens: `maxwell-electromagnetism`, `quantum-gravity`, `darwin-mendel-modern-synthesis` reference by name), use the node's exact `name` or `who` **string**, matched verbatim.
- For a **new** node the harvest introduces (one that carries its own lifecycle data and does not exist in the base specimen), use `proposed:<slug>` (e.g. `proposed:oliver-heaviside`). The compiler treats `proposed:` subjects as valid-by-construction (never flagged as unknown).

---

## 3. The certainty rubric (`certainty ∈ [0,1]`)

`certainty` is the harvester's calibrated confidence that the asserted `value` is correct, BEFORE verification. Score by source strength:

| Band | Source situation | Range |
|------|------------------|-------|
| **Structured-aggregator-attested** | Wikidata / Our World in Data / an official org page / a structured database entry with the exact datum | **0.7 – 0.9** |
| **Single encyclopedia** | One Wikipedia / Britannica / Stanford Encyclopedia article asserting it (prose, not a structured field) | **0.5 – 0.7** |
| **Single news** | One news article | **0.4 – 0.6** |
| **Historiographic estimate / proxy** | A contribution share, an inferred date, any modelled/derived value | **0.2 – 0.5** — and `notes` MUST state the basis |

Hard rules:
- A `contribution_share` (theory-DNA) is ALWAYS an estimate → **certainty ≤ 0.6**, basis in `notes`, even if a source states a number (historiography is contested).
- Any proxy/estimate is labelled in `notes` ("ESTIMATE:" / "PROXY:") and capped per the bottom band.
- Two **independent** structured sources at emit time → you may emit at the top of the aggregator band (0.9), but corroboration is recorded via a verification record (§4), not by inflating certainty.
- When in doubt, score LOW. Skipping a fact is always allowed; guessing is never.

`certainty` is NOT changed by verification. Verification status is tracked separately and dominates resolution (§6).

---

## 4. The verification record (`verifications/*.jsonl`) + state machine

Verifiers do NOT edit facts. They append a separate record keyed by `fact_id`:

```jsonc
{
  "fact_id":      "f-maxwell-0001",          // REQUIRED. The fact being verified.
  "status":       "corroborated",            // REQUIRED. one of: corroborated | disputed | unverifiable
  "second_source": {                          // REQUIRED. The independent source consulted (REAL, fetched).
    "url":   "https://www.britannica.com/biography/Michael-Faraday",
    "title": "Michael Faraday | Biography & Facts | Britannica",
    "type":  "encyclopedia",
    "published_or_updated": "2026-04-01"
  },
  "value_found":  "1791-09-22",              // REQUIRED. The value the second source gave (verbatim).
  "retrieved_at": "2026-06-10T03:00:00Z",    // REQUIRED. UTC stamp of the verification fetch.
  "verifier":     "sonnet-verifier-02",      // REQUIRED. Identifier of the verifying agent/seat.
  "notes":        ""                          // OPTIONAL. Reconciliation note for disputes.
}
```

### State machine

```
                emit a fact
                    │
                    ▼
                ┌────────┐
                │ pending│◄──────────────── (no verification record yet)
                └───┬────┘
                    │  a verification record arrives, keyed by fact_id
        ┌───────────┼─────────────────┬─────────────────────────┐
        ▼           ▼                 ▼                         ▼
  corroborated   disputed        unverifiable             (stays pending)
  second source  second source   no independent           if every verification
  AGREES with    DISAGREES with  source could be          record is missing
  fact.value     fact.value      found / source dead
```

Rules:
- A fact is **`pending`** until at least one verification record references its `fact_id`.
- **`corroborated`**: `value_found` matches `fact.value` (semantically — dates normalised, whitespace/case-folded). The compiler treats this as the most trustworthy bucket.
- **`disputed`**: `value_found` ≠ `fact.value`. **BOTH values are kept** — the compiler records the disputed alternative in the best-value provenance and in `_summary.json`. NEVER silently overwrite.
- **`unverifiable`**: the verifier could find no independent corroboration (source dead, paywalled, nothing else asserts it). Lowers trust but does not delete the fact.
- Multiple verification records may target one fact (e.g. two verifiers). Resolution: **any `corroborated` wins** the bucket; else if any `disputed`, bucket is `disputed`; else if any `unverifiable`, bucket is `unverifiable`; else `pending`. (corroborated > disputed > unverifiable > pending for *bucket assignment*; see §6 for how the bucket drives best-value selection.)
- A later **corroborating** verification can lift a previously disputed/unverifiable fact out of dispute IF its `value_found` agrees with `fact.value`; the disputed alternative is still retained in history.

---

## 5. Freshness conventions

Two timestamps matter, both UTC ISO-8601:
- `retrieved_at` — when the harvester/verifier fetched the source. This is the **freshness** signal the compiler uses as a tie-breaker (newer wins). Always stamp via `date -u +"%Y-%m-%dT%H:%M:%SZ"`.
- `source.published_or_updated` — when the SOURCE itself was last published/updated (page freshness). Recorded for the freshness log; `""` if the source exposes no such date.

Conventions:
- Re-harvesting a datum = **append a new fact** with a newer `retrieved_at`. The compiler prefers the fresher fact when buckets and certainties are otherwise equal.
- A stale `retrieved_at` is never deleted; it remains in history and the compiler reports the **oldest** and **newest** retrieval per specimen in the freshness summary.
- `when` (event date) is about the WORLD (when the event happened); `retrieved_at` is about the HARVEST (when we looked). Do not conflate them.

---

## 6. Best-value resolution (what the compiler picks)

For each `(specimen, subject_id, predicate)` group, the compiler keeps **all** facts (full history) and selects ONE best value by this strict lexicographic order:

1. **Verification bucket** — `corroborated` > `pending` > `disputed`. (A `disputed` fact is demoted BELOW a bare `pending` one: an actively-contradicted value should not be presented as best while an un-checked candidate exists. `unverifiable` is treated as `pending`-level trust but flagged.)
2. **Certainty** — higher `certainty` wins.
3. **Freshness** — newer `retrieved_at` wins.
4. **Stable tiebreak** — lexicographically smallest `fact_id` (deterministic output).

The chosen fact's `value` becomes the best value. The group's full provenance (every contributing `fact_id`, its bucket, certainty, source) is attached to the compiled output. If the group contains any `disputed` fact, the compiled record carries a `disputed_alternatives` list (the contradicting `value_found`s + their verification refs) so viewers can surface the conflict. **Disputed values are never dropped.**

---

## 7. The scale story

Append-only logs are the source of truth; everything else is derived.

- **`facts/*.jsonl` + `verifications/*.jsonl`** — git-native, append-only, the **source of truth**. Diff-friendly, mergeable, one fact per line. New specimens ⇒ new fact files. Re-harvest ⇒ append newer facts. Never rewritten.
- **`substrate.db`** (SQLite) — a **compiled artifact**, rebuilt from the logs on every run. **Never committed** (see `.gitignore`). Tables: `facts`, `verifications`, `best_values`. This is the queryable index for analysis; it is disposable.
- **`compiled/<specimen>.compiled.json`** — **committed** best-value exports, grouped by subject, with provenance refs. This is **what viewers ingest**.
- **`compiled/_summary.json`** — **committed** coverage + freshness + certainty + disputes rollup.

Forward path:
- **Overlay ingestion** — a future `--ingest-overlays` flag folds `../overlays/*.overlay.json` into the same fact stream (an overlay datum becomes a fact with an `aggregator`/`primary` source and a recorded `retrieved_at`), so overlays and harvest facts resolve through one pipeline.
- **New specimens** = new fact files; no schema change. The compiler discovers specimens by reading every `../specimens/*.json` for validation and every `facts/*.jsonl` for content.
- **Re-harvest** = append newer facts; the compiler automatically prefers fresher + more-certain + corroborated values, so the latest pass wins without deleting the record of earlier passes.
- **Scale-out (optional)** — if the SQLite compiled artifact outgrows a single file, the same `facts`/`verifications`/`best_values` schema lifts unchanged to **Postgres** (swap the `sqlite3` connection for a DB-API connection; the resolution logic is engine-agnostic SQL-free Python over the loaded rows). The committed JSON exports remain the stable viewer contract regardless of backend.

---

## 8. Compiler usage

```
python compile_substrate.py            # read facts/ + verifications/, validate, build substrate.db,
                                        #   write compiled/*.compiled.json + compiled/_summary.json,
                                        #   print coverage/freshness/certainty/disputes to stdout
python compile_substrate.py --strict   # exit non-zero if any validation flag is raised (CI gate)
python compile_substrate.py --no-db    # skip writing substrate.db (exports + summary only)
```

Stdlib only (`json`, `sqlite3`, `argparse`, `pathlib`, `datetime`). No third-party dependencies. Runs offline.

---

*Tier-3 exploratory data-harvest substrate for Cowork+Pav ratification — NOT canon, NOT a tier promotion, does NOT grow the convergence list. Honest discipline: no fabrication; every fact carries real provenance; estimates/proxies labelled with basis and capped low; disputed facts keep both values.*
