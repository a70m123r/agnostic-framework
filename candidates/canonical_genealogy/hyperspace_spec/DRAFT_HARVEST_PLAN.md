# DRAFT HARVEST PLAN — one iterable global substrate → 4D hyperspace render → the keyhole stream

**Date:** 2026-06-20 · **Author:** lead synthesizer (Opus 4.8) · **Status:** DRAFT for Pav review
**Companion:** `WHERE_WE_ARE.md` (the ground-truthed picture this plan acts on).

**Vision (Pav):** harvest + normalize + compile ALL the data into ONE iterable GLOBAL SUBSTRATE
(extending the existing `canonical_genealogy` SUBSTRATE format) with procedural recompiles to specific
formats + provenance; then render it in the 4D block / hyperdimensional universe (`hyperspace_spec`)
with physical + latent exposure and the TWO timelines; from then on every future action is harvested
and seen as a beam of light through the keyhole. The agnostic UNIT = **bits of re-pay/digestion cost
(MDL/COIN)**, so ANY event (rival models, competing theories, clashing beliefs) scores on one board.

**Five phases:** HARVEST → NORMALIZE → COMPILE → RENDER → STREAM. Each phase below states
**reuse vs new-build**, the exact record/field shapes, how each slice maps, and the secrets rule.

---

## PHASE 0 — Guardrails (do FIRST, blocking)

### 0.1 Secrets exclusion rule (non-negotiable)
- **Rotate** `measure/.openrouter_key` (it has been exposed to agent contexts).
- Every harvest pass MUST exclude, by both name and glob:
  `*.key`, `.openrouter_key`, `.env*`, `secrets.*`, any dotfile, and any file whose content matches
  `sk-or-`, `sk-`, `AKIA`, `AIza`, `ghp_`. Implement as a single `is_secret(path, head_bytes)`
  predicate the harvester calls before reading ANY file.
- Add a unit assertion: the global substrate output is grepped for the secret prefixes; non-empty =
  fail the build.

### 0.2 Hard partition keys (prevent invalid joins)
Bake these into the schema so a naive join *cannot* be wrong:
- `era` ∈ {`era1-openai`, `era2-openrouter`, `v1-codelength`, `n/a`} — magnitudes never compare
  across eras.
- `signal_type` ∈ {`reasoning_tokens`, `markers`, `residue_bits`, `mdl_delta_bits`, `none`}.
- `model` (+ slug) always present.
- `arena` (the contestant family) — see §2.1.

### 0.3 Reuse decision
**REUSE the `substrate/SUBSTRATE_SPEC.md` envelope as the global schema.** Do NOT invent a new format.
Everything below extends it.

---

## PHASE 1 — HARVEST (collect)

**Goal:** enumerate every source-of-truth artifact into a manifest; touch nothing destructively.

**REUSE:** glob discipline from `compile_substrate.py`.
**NEW:** a top-level `harvest_manifest.jsonl` (the one thing that does not exist today).

### 1.1 Build the manifest
Glob the corpus (respecting §0.1) and emit one manifest row per artifact:
`{artifact_id, path, kind (harness|data|spec|doc|viewer|ledger|db|secret-excluded),
format, slice (A–F), era, state (live|stale|spec-only|demoted), sha256, n_records?, lock_sha?,
result_docs[], dc_ids[], notes}`.

### 1.2 Source-of-truth selection (avoid duplicates)
- Facts: **only** `substrate/facts/*.jsonl` (NOT `l0_wrappers/facts/` staging dupes).
- Run logs: Era-2 `*_run.<model>.jsonl`; Era-1 single `v*_run.jsonl`.
- Compiled artifacts: prefer the `*.compiled.json` for *resolved views*, but **re-derive from
  source jsonl** wherever a compiled headline is known stale (dynamics `stats.reduction`).
- Viewer data: harvest the `compiled/*.json`, **never** `arc_data.js` (derived JS dup) or the inline
  HTML blobs.

### 1.3 The two SWEEP_LOGs + overlays
Register `l0_wrappers/SWEEP_LOG.md`, `dial_engine/SWEEP_LOG.md`, and the 8
`overlays/*.overlay.json` as known-parallel streams to reconcile in Phase 2 (overlays are currently
un-harvested; `--ingest-overlays` was specced but never built).

**Deliverable:** `harvest_manifest.jsonl` + a coverage report (which slices, which states).

---

## PHASE 2 — NORMALIZE (into the global substrate schema)

**Goal:** one iterable record stream keyed for provenance, with adapters per slice.

### 2.1 The global EVENT record (extends the fact record)
Every contestant — a fact, a measurement cell, a wrapper class, a dynamic, an organ, a concept, a
rival theory — becomes one append-only JSONL line:

```jsonc
{
  "event_id":        "<arena>:<slug>:<NNNN>",      // disjoint namespace per arena (HAZARD-guard safe)
  "arena":           "genealogy|digestion|wrapper_class|dynamic|organ|concept|provenance|rival_theory",
  "subject_id":      "<exact node slug | proposed:slug>",
  "predicate":       "<SCHEMA_v2 field | rel:<type>:<target> | metric:<name>>",
  "value":           <any>,
  "contestant_name": "<human label>",
  "parents":         ["<event_id>", ...],          // typed edges where available

  // --- the agnostic UNIT (the one board) ---
  "bit_unit": {
    "dissolve":     true|false|null,               // verified-dissolve gate outcome
    "cost":         <number|null>,                  // bits or tokens
    "signal_type":  "reasoning_tokens|markers|residue_bits|mdl_delta_bits|none",
    "floor":        true|false,                     // aleatoric residue?
    "n_correct":    <int|null>, "n_total": <int|null>  // survivorship
  },

  // --- the COIN render (computed in Phase 3, stored as provenance of intent) ---
  "declared":  <0..1>,                              // claimed sharpness
  "bucket":    "corroborated|pending|disputed|unverifiable|conceptual|planned|demoted",

  // --- Pareto coords (wrapper/event arena) ---
  "pareto":    {"spread":x,"utility":x,"legacy":x,"rigor":x} | null,

  // --- the two timelines (bitemporal) ---
  "t_event":   "<ISO|null>",                        // when the state belongs in the block
  "t_obs":     "<ISO|null>",                        // when a keyhole measured it
  "phys_latent": <0..1|null>,                       // physical(0)↔latent(1) membrane coord

  // --- provenance (always real or skip) ---
  "source":    {"url|doc":..., "title":..., "type":..., "published_or_updated":...},
  "retrieved_at": "<ISO>",
  "agent":     "<who>",
  "era":       "era1-openai|era2-openrouter|v1-codelength|n/a",
  "lock_sha":  "<sha|null>",
  "provenance_refs": ["<file:section|transcript#>", ...],

  // --- claim lifecycle (demote-not-kill) ---
  "lifecycle": "ratified|corroborated|pending|spec-only|demoted|resolved|un-demoted|dead",
  "demotions": [{"dc_id":"<era-namespaced>","from":...,"to":...,"flagged_by":...,"date":...}],

  "notes": "<required for any estimate/proxy; flags e.g. 'narration-confounded','single-agent-unaudited'>"
}
```

### 2.2 Per-slice adapters

**Adapter A — genealogy facts (Slice B). REUSE wholesale.**
The 1372 facts already conform. Pass through with `arena='genealogy'`, `bit_unit.signal_type='none'`,
`phys_latent` low. Fix the one filename/id mismatch (`qm_relativity` stem → `quantum-gravity`
specimen). Decide overlays: either build `--ingest-overlays` or register the 8 overlays as
`spec-only` provenance nodes.

**Adapter B — digestion measurement (Slice A). NEW adapter, the trickiest.**
- Iterate every `*_run.*.jsonl`. Era-2: pass through. Era-1: map `answer→got`, `expected→truth`,
  inject `model='gpt-5.5'`, set `era='era1-openai'`, pull `tier` from the LOCK.
- **Derive `rep` from the run rows** (not metadata; v10c=3, v10b=4).
- `arena='digestion'`, `contestant_name=target/cond`, `floor=(target=='s1_random' or no-ground-truth)`.
- **Prefer markers** (`nf_markers.py`) where CoT exists; keep `reasoning_tokens` as fallback flagged
  `narration-confounded`. Back-apply the marker re-score to other experiments where reasoning text
  is saved (Era-2 only) — no new API calls.
- Join `model/slug/price/lock` from `CROSS_MODEL_RUNCARD.md` — **never infer params from filenames.**
- Carry `n_correct/n_total` per cell (survivorship). V1 codelength rows go in a **separate table**
  (`signal_type='residue_bits'`, `era='v1-codelength'`) linked only at experiment level.

**Adapter C — W_C wrapper DB (Slice E-b). NEW adapter, reconcile-first.**
- **Blocking reconciliation:** read `latent_olympics_phase1_SPEC.md` + DESIGN_SKETCH; either migrate
  the 25 live rows up to the rich shape (typed overlaps, numeric utility legs, pipeline state) OR
  demote the `_schema_doc` to "aspirational". Pav-decision (§Open Questions).
- `arena='wrapper_class'`; bucket lifecycle from the **free-text status** via a disclosed mapping
  table (`risen*→risen`, `RESURRECTED-then-RISEN→resurrected`, `DORMANT,→dormant`, …);
  `pareto=classifierWeights`; `parents=overlaps` (re-typed); `bit_unit.cost=mdl_delta_bits` if
  numeric else flag `prose-only`. **Flag every score `single-agent-unaudited`** until a cross-model
  pass runs. Read/write UTF-8 (mojibake).

**Adapter D — dynamics/bestiary/tactics/couplings (Slice D). NEW adapter, partly new record types.**
- Adopt `dynamics.jsonl` (88 records) as `arena='dynamic'`; map `lifecycle`/`certainty`/`phys_latent`/
  `observable`/`citation` through.
- **Replace** the stale 10 couplings with the **12** refined edges from `COUPLINGS.md` (re-normalize;
  carry sign/endpoints/loop/falsifier); entity-resolve old↔new by endpoints/formal_name; mark
  superseded as `demoted`, never delete.
- **Add a new `arena='organ'`** sourced from `FALSIFIER_REPORT.md`: 5 surviving + 3-4 candidate
  organs, each `lifecycle` per verdict, plus a parent reduction-claim record carrying
  `κ=0.671/P_o=0.778/P_e=0.324, verdict=PARTIAL`. Emit the 15-item held-out set as
  `arena='test_item'` records.
- **Do NOT** propagate the stale `6.8:1` headline; overwrite `stats.reduction` after organ records
  exist.

**Adapter E — provenance & dead-children (Slice F). NEW, the unifier.**
Build the first machine-countable `dead_children.jsonl`: regex-scrape `DC-NN` lines from the result
docs, parse `arcs.jsonl` `demotions[]`, the `ARC_DIGEST` honesty bullets, the FALSIFIER organ
retirements, the cosmic "six", and the V4–V9d EXTERNAL_SYNTHESIS DEMOTE sections. **Era-namespace
every id** (`dc-`, `arc-`, `organ-`, `cosmic-`) to avoid collisions. Promote `acts.jsonl`
(provenance.ref + session) as the canonical event-spine; join `verify.jsonl` for the fake-bit column.
This makes the prose "40" tally machine-counted for the first time.

### 2.3 Unify the divergent BUCKET_CAP / render-cap ladders
scope (corroborated/pending/conceptual/planned/demoted), arc (…/unverifiable/disputed), dynamics
(lifecycle documented/classified/tracked/sighted) → one **ordered cap ladder**, recording the
original bucket as a sub-field so nothing is lost.

**Deliverable:** `global/events/*.jsonl` (append-only, per-arena files) + `global/dead_children.jsonl`.

---

## PHASE 3 — COMPILE (procedural recompiles, with provenance)

**Goal:** deterministic, idempotent recompiles to the specific output formats — the
materialized-view discipline already proven in the corpus.

**REUSE:** `compile_substrate.py` (best-value resolution + HAZARD guard + `_summary`),
`recompile_channel.py` (constellate_by/branch_by), the COIN render-cap.
**NEW:** `compile_global.py` orchestrator that runs the per-arena compiles and a unified `_summary`.

1. **Resolve + render:** for each `(arena, subject_id, predicate)` group keep all events, pick the
   best by the lexicographic order in `SUBSTRATE_SPEC §6`; compute
   `render = min(declared, BUCKET_CAP[bucket])`. Verify `render ≤ measured_bits` (the COIN). Re-hash
   stimulus bodies against `body_hash`/`needle_line_hash` for a per-record verification flag.
2. **Procedural views (one recompile each, all derive from the same global substrate):**
   - **scope view** → extend `compile_scope.py` to read global concept/finding records → `SCOPE.html`.
   - **olympics view** → the event board: every contestant (target / wrapper class / rival theory)
     on the `bit_unit` + `pareto` axes, era-partitioned.
   - **channels view** → `recompile_channel.py` over the unified substrate (constellations + branches).
   - **4D-render view** → the JSON the hyperspace viewer ingests (Phase 4): each event with
     `t_event, t_obs, phys_latent, render, bucket, parents`.
3. **Per-cell aggregate sidecar** (digestion): per-seed mean over reps on CORRECT-only → paired
   bootstrap median CI (4000) + sign test via `v9b_resistance.paired()` so numbers match the docs.

**Deliverable:** `global/compiled/*.json` + `_summary.json` (machine-counted dead-children tally).

---

## PHASE 4 — RENDER (the 4D hyperspace viewer)

**Goal:** the one headline thing that does not exist yet. **NEW-BUILD, but on an existing chassis.**

**REUSE:** `canonical_genealogy/toys/globe_cone_unified.html` (~70% of a globe/cone viewer per SPEC).
**NEW:** ~250 lines per `SPEC.md` to add the dial + membranes + two timelines.

- **Keystone (one logarithm, three jobs):** Mercator isoLat unfold (3D↔2D) / `log2(metres)` physical
  scale / `2^(−bits)` render sharpness. The dial `d∈[0,1]` morphs globe↔flat-Mercator via the
  Daners/Lambert conformal family `n=cos(d·π/2)`; orthogonal dials `d=SHAPE`, `z=SCALE`.
- **Two membranes:** physical (radial = `log2` scale) + latent (radial = hyperbolic Poincaré tanh
  reach); within/under/above toggle on `h_latent` = the **physical + latent exposure** Pav wants.
- **Two timelines (bitemporal):** X=`t_event`, thread rising to render-height at `t_obs` — the
  "block sharpening" already prototyped in `BITEMPORAL_3D.html`. A 2026 burst measuring a 1790 state
  lowers blur without changing 1790.
- **COIN everywhere:** `rendered_sharpness(x) ≤ measured_bits(x)`; blur is the badge; 3 additive
  channels MEASURED/ESTIMATE/MODELLED drawn distinctly; DISAGREE rendered loud.
- **Substrate-as-light:** fact = emitter, view = sensor (Kajiya / EWA-splat), EWA low-pass = the
  anti-lie pixel floor.
- **CORRECTION-LAYER FIRST:** before rendering, fix the `SPEC.md` keystone text that still reads
  "Solomonoff = 2^−bits" → standard MDL/log-loss shared bit-currency. Render the demote-not-kill
  corrections as a visible layer; never render a fake measured bit; never render a `1.0` pixel.
- Render the `FIG-1..8` the spec lists but never produced.

**Deliverable:** `HYPERSPACE.html` extending the chassis + `build_hyperspace.py` (jsonl→inject).

---

## PHASE 5 — STREAM (the keyhole: future actions auto-harvested)

**Goal:** from now on, every action is harvested and seen as a beam of light through the keyhole.

**REUSE:** the `session_arc` capture toolchain (`acts/arcs/verify.jsonl` + `compile_arc.py`) — it
already captures the instrument's own history under COIN, bitemporally.
**NEW:** an append-on-action hook.

- A lightweight harvester appends new `event` records (`arena='provenance'`, `t_obs=now`,
  `bit_unit`/`render` capped, `provenance_refs` = transcript event #) on each commit / experiment /
  steer, then triggers `compile_global.py` (idempotent).
- **Honour `t_event` before calling it history** (the open anachronism the external pass flagged:
  `verify.jsonl` currently checks past acts against final disk state). Fix the verify pass to honour
  as-of-`t_event`.
- Keep the **cross-model external pass** as the A− gate for any new load-bearing claim before it
  earns full render.

**Deliverable:** the keyhole loop — append → compile → render, with the COIN cap enforced procedurally.

---

## Reuse vs new-build, at a glance

| | REUSE (exists) | NEW-BUILD |
|---|---|---|
| Schema | `SUBSTRATE_SPEC` envelope, certainty rubric, state machine | the `event` extension fields (bit_unit, pareto, phys_latent, dual-time) |
| Compilers | `compile_substrate.py`, `recompile_channel.py`, `compile_scope/arc.py`, `paired()` | `compile_global.py` orchestrator, 5 per-slice adapters, `dead_children.jsonl` builder |
| Viewers | 5 built mini-viewers, the globe/cone chassis | `HYPERSPACE.html` (dial + membranes + dual-time, ~250 lines) + figs |
| Provenance | `CROSS_MODEL_RUNCARD`, locks, `acts/arcs/verify`, external-pass corpus | the unified manifest + machine-counted DC ledger |
| Stream | `session_arc` capture pattern | the append-on-action hook + `t_event`-honouring verify |

---

## Open design questions for Pav (blocking where noted)

1. **(BLOCKING) W_C schema:** migrate the 25 live rows UP to the rich `_schema_doc` shape, or demote
   the spec to "aspirational" and harvest the flat rows as-is? (Affects whether overlaps become typed
   edges and whether utility legs get numeric scores.)
2. **(BLOCKING) Secret:** confirm rotation of the OpenRouter key before any harvest pass runs.
3. **Overlays:** build the promised `--ingest-overlays` flag (fold the 8 overlays into the fact
   stream) or leave them as registered-but-separate spec nodes?
4. **One store or routed?** The memory routing decision says camera findings → `scope`, genealogy →
   `facts`, dynamics → its own store. Does the GLOBAL substrate **physically merge** these into one
   `global/events/` tree, or stay a **federation** that compiles into one iterable view? (I lean
   federation: keep the source-of-truth stores, add a global compile that unions them — preserves the
   existing toolchains and avoids a risky migration.)
5. **DC numbering:** adopt the era-namespaced keyspace (`dc-`/`arc-`/`organ-`/`cosmic-`) as canonical,
   and reconcile the two SWEEP_LOGs into it?
6. **Marker back-application:** re-score Era-2 reasoning text with `nf_markers.py` across ALL
   experiments now (no new API calls), and treat markers as the primary digestion `signal_type`?
7. **Latent axis:** the semantic/meaning measurement model is the standing load-bearing hole
   (canonicalizer needs an NLI instrument). Render the latent membrane as **explicitly low-render
   (blurred)** until that exists — yes?
8. **Predict-half:** the upper camera (sealed conjecture-bubble) is 100% dark. Build the ~150-line
   forward-camera/calibration apparatus as part of STREAM, or defer?

---

*This is a draft. Nothing here is destructive; Phase 0–1 are read-only + manifest-building and can
start immediately once the key is rotated.*
