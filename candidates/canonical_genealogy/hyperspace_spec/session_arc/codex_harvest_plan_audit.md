# Codex external audit - DRAFT_HARVEST_PLAN

**Date:** 2026-06-20  
**Auditor stance:** adversarial external review, demote-not-kill  
**Inputs read in full:** `WHERE_WE_ARE.md`, `DRAFT_HARVEST_PLAN.md`  
**Spot checks:** `substrate/SUBSTRATE_SPEC.md`, `substrate/compile_substrate.py`, `substrate/compiled/_summary.json`, measurement run logs and locks, `measure/nf_markers.py`, `measure/V10c_NF_MARKERS_RESULTS.md`, `measure/CROSS_MODEL_RUNCARD.md`, `latent_olympics_data/wrapper_classes_phase1.json`, `latent_olympics_phase1_SPEC.md`, `latent_olympics_DESIGN_SKETCH.md`, `dynamics/dynamics.jsonl`, `dynamics/compiled/dynamics.compiled.json`, `COUPLINGS.md`, `FALSIFIER_REPORT.md`, `session_arc/acts.jsonl`, `session_arc/arcs.jsonl`, `session_arc/verify.jsonl`, `session_arc/ARC_DIGEST.md`, `session_arc/EXTERNAL_SYNTHESIS.md`, and `../toys/globe_cone_unified.html`.

## Executive Verdict

The plan is directionally sound: reuse the existing canonical-genealogy substrate envelope, keep source records append-only, compile materialized views, and render the new hyperspace view from a global event projection. Federation is the right recommendation.

The plan is not yet safe as written. The schema records `era` and `signal_type`, but those fields do not themselves prevent invalid cross-era, cross-model, or cross-unit joins. They are labels until `compile_global.py` refuses illegal aggregates. The largest technical risk is therefore not the UI or even the secret. It is **unit collapse**: a single global substrate that makes heterogeneous costs look commensurable and produces a persuasive but false "one board."

The plan should be demoted, not killed: preserve the architecture, but add hard compiler invariants, golden adapter fixtures, bridge tables, and redaction gates before any full harvest.

## 1. Event Schema And `bit_unit`

### Finding: partition keys are necessary but not sufficient

The draft says hard partition keys "prevent invalid joins" (`DRAFT_HARVEST_PLAN.md` lines 29-35): `era`, `signal_type`, `model`/slug, and `arena`. That is the right instinct, but the proposed event schema only stores `era` at top level and `signal_type` inside `bit_unit` (lines 91-97, 116). It does **not** actually include a required top-level `model` or `slug` field, despite the guardrail saying those are always present.

That mismatch matters. I confirmed the actual logs need these keys:

- Era 1 `measure/v4_run.jsonl` keys: `target, family, effective_ops, display_ops, prompt_words, seed, tier, reasoning_tokens, answer, expected, correct, exhausted, seconds`.
- Era 2 `measure/v10c_run.deepseek.jsonl` keys: `item_id, cond, seed, prompt_words, truth, model, rep, got, correct, exhausted, content, reasoning, finish, reasoning_tokens, completion_tokens, prompt_tokens, slug, seconds`.

So the plan correctly spots the schema split, but the event record does not yet force enough dimensions to keep them apart.

### Required invariant

`compile_global.py` must make invalid joins impossible by grouping and validating with a key like:

```text
arena, experiment_id, era, signal_type, unit, model, slug, lock_sha, condition_family
```

Crossing any of those boundaries should fail closed unless a named bridge record exists, for example:

```json
{
  "bridge_id": "bridge:nf:markers-to-rt:deepseek",
  "from_signal_type": "markers",
  "to_signal_type": "reasoning_tokens",
  "scope": "v_nf only",
  "model": "deepseek",
  "valid_operation": "within-model sign comparison only",
  "not_valid_for": ["absolute magnitude", "cross-model magnitude", "era1 comparison"]
}
```

Without this, a dashboard can still join `bit_unit.cost` across `reasoning_tokens`, `markers`, `residue_bits`, and `mdl_delta_bits` because they are all just numbers.

### Finding: `bit_unit.cost` has ambiguous units

The schema says `"cost": <number|null> // bits or tokens`. That is too loose for the agnostic unit. Tokens, marker counts, residue bits, and MDL deltas are not interchangeable currencies. The existing corpus explicitly says this:

- `WHERE_WE_ARE.md` lines 245-253 says `reasoning_tokens` is a model-dependent, narration-confounded proxy; marker count exists only for NF; V1 codelength/residue is a separate axis.
- `measure/V10c_NF_MARKERS_RESULTS.md` lines 39-63 says marker counts partially rescue compute claims and that `reasoning_tokens` is a noisy per-model proxy.
- `measure/CROSS_MODEL_RUNCARD.md` lines 33-34 says OpenRouter `effort:"high"` fidelity is unresolved.

Required fields:

```json
"bit_unit": {
  "value": 123,
  "unit": "token|marker|bit|score|none",
  "signal_type": "...",
  "extractor": "nf_markers.py@sha256|openrouter_usage|openai_usage|mdl_estimator_x",
  "scope": "trial|seed_mean|cell_mean|experiment_delta|claim_estimate",
  "comparable_with": ["..."],
  "comparison_policy": "same_model_same_experiment_only|bridge_required|never"
}
```

### Finding: COIN render check is dimensionally underspecified

The compile phase says `render = min(declared, BUCKET_CAP[bucket])` and "Verify `render <= measured_bits`" (`DRAFT_HARVEST_PLAN.md` lines 197-200). But `render` is a 0..1 sharpness, while `bit_unit.cost` may be tokens, marker counts, residue bits, or prose-only estimates. There is no defined function from each signal type to render sharpness.

Required fix: define per-signal render functions:

- `residue_bits`: can map through the existing `sigma = k * 2^-bits` story.
- `markers`: task-local compute proxy, not direct sharpness.
- `reasoning_tokens`: proxy, never direct measured bits without a calibrated bridge.
- `mdl_delta_bits`: direct only if the estimator and corpus are defined.
- `none`: render must be provenance/certainty capped, not bit-capped.

### Finding: best-value resolution should not apply to all events

The existing `compile_substrate.py` groups by `(specimen, subject_id, predicate)` and selects a single best value. That is correct for factual slots. It is dangerous for measurements, reps, provenance acts, and demotions. A run row is not a competing "best value"; it is an observation. The global compiler needs at least two storage modes:

- **state facts:** best-value resolution applies.
- **observations/events:** append-only, aggregate only through declared reducers.

Do not let `subject_id + predicate` collapse multiple reps, seeds, model rows, or demotion records.

## 2. Per-Slice Adapters

### Adapter A: genealogy facts

Mostly fits. The source substrate is real and healthy:

- `substrate/compiled/_summary.json` reports `facts: 1372`, `verifications: 359`, `best_values: 1107`, `validation_errors: 0`, `validation_flags: 217`.
- `substrate/facts/` has 19 JSONL files and `substrate/verifications/` has 9 files.
- `compile_substrate.py` has duplicate `fact_id` hazard detection at lines 519-536.

Loss/risk:

- The proposed event record lacks explicit preservation of original `fact_id`, `specimen`, and verification record ids. Store the raw substrate identity or round-trip audits will be weak.
- `qm_relativity.*.jsonl` mapping to compiled `quantum-gravity` is a real mismatch. The adapter must map by `specimen`, not filename stem.
- The 8 overlays exist, but `SUBSTRATE_SPEC.md` only promises future overlay ingestion, and `compile_substrate.py` has no `--ingest-overlays` flag. Registering them as spec-only is honest; folding them without implementing the flag is not.
- `phys_latent` "low" is an invented coordinate unless derived from schema fields or capped as an estimate.

### Adapter B: digestion measurement

The plan correctly identifies this as the hardest adapter.

Spot checks support the plan:

- `v10c_labels.LOCK`: 600 items, 100 seeds, 6 conditions, sha256 `68c451048cff96e870199306027007ce2b3c30e2cbfcf5ba22491c75852a22f5`.
- `v10c_run.deepseek.jsonl`: 1800 rows, reps `0,1,2`, six conditions.
- `v10b_run.deepseek.jsonl`: 576 rows, reps `0,1,2,3`, six conditions.
- Era 1 and Era 2 schemas differ exactly as described above.

Loss/risk:

- The event schema needs first-class `experiment_id`, `condition`, `seed`, `rep`, `correct`, `exhausted`, `prompt_hash`, and `stimulus_hash`. Otherwise raw rows become opaque `value` blobs.
- Correct-only aggregation is not just a display decision. It changes the estimand. Store both all-trial and correct-only aggregates, with the docs' chosen one flagged as primary.
- `target == "s1_random"` is too narrow for `floor`. Aleatoric/floor status needs an experiment-specific mapping table.
- The Era 2 rows contain `content` and `reasoning`. Harvesting raw hidden reasoning is a privacy/security decision, not just a measurement decision. Store raw reasoning only in a private/raw tier, and store marker-derived features in public/global compiled outputs.
- Back-applying `nf_markers.py` to "all experiments where reasoning text is saved" is too broad. The current marker extractor is explicitly for trial-division language, not a universal reasoning-work meter.

### Adapter C: W_C wrapper DB

This adapter is lossy unless reconciled first. The live file is `latent_olympics_data/wrapper_classes_phase1.json`; it has:

- top-level keys: `schema_version, _status, _schema_doc, _source, _method, generated, record_count, wrapper_classes`
- `record_count: 25`, actual 25 records
- live record keys: `name, tier, status, localKernelCanon, netProduct, akaWhoCalledIt, origin, overlaps, localKernelCanon_note, utility, classifierWeights, localKernelCanonExtra, refs`

The embedded `_schema_doc` demands fields the rows do not have: `id`, structured `origin`, typed `overlaps[]`, numeric utility sublegs, `pipeline`, issues, appeals, and observer-relative metadata. The plan accurately calls this blocking.

Loss/risk:

- `overlaps` are bare strings, so parent edges cannot be trusted without slug generation and adjudication.
- `utility.score` is numeric, but `isUnifier`, `actionSpacesUnlocked`, and `compression` are prose. Mapping to `bit_unit.cost = mdl_delta_bits` would be false unless an actual numeric MDL delta is added.
- `status` is long free text. Bucket mapping must preserve the raw status and disclose the mapping. A lifecycle bucket alone loses important demote/resurrect/reinvent nuance.
- `refs` are local absolute paths such as `D:/PlatformOperator/...`; those are provenance but also path leaks.
- The file itself declares the data "Tier-3 WORKING first-pass" and soft-scored. The plan's `single-agent-unaudited` flag is necessary.

Recommendation: migrate rows up only after generating stable ids, typed edge records, and utility subleg objects. Until then, harvest them as raw wrapper-class records plus a low-render normalized projection.

### Adapter D: dynamics, tactics, couplings, organs

The plan is right that this is not a simple pass-through.

Spot checks:

- `dynamics/dynamics.jsonl`: 88 records: 41 `creature`, 37 `tactic`, 10 `coupling`.
- lifecycle values: `classified` 13, `tracked` 60, `sighted` 3, `documented` 12.
- `dynamics/compiled/dynamics.compiled.json` still contains the stale "41:6 ~ 6.8:1" reduction text.
- `COUPLINGS.md` has 12 `###` edge sections, while its own headline says 13 distinct edges.
- `FALSIFIER_REPORT.md` says kappa 0.671, `BANDWIDTH-CAPACITY` drew 1/60 votes, and the honest frame is "5 robust organs + a documented 3-4 organ gap; one organ on probation."

Loss/risk:

- Do not "replace" the 10 couplings with the 12 refined edges in-place. Emit new coupling records and supersession edges, then mark old coupling records demoted/superseded. Replacement would erase provenance.
- Reconcile three counts: 10 substrate couplings, 12 current section headings, 13 claimed in the COUPLINGS headline. The plan says 12, which matches headings, but the headline must be corrected or carried as a demoted count.
- `dynamics.jsonl` source is often `{ "doc": ... }`, while the global event schema requires richer source metadata. Either relax source shape for local docs or add `source_local`.
- Organ extraction from `FALSIFIER_REPORT.md` must preserve votes and held-out items, not just final organ names. The statistics are the evidence.

### Adapter E: provenance and dead-children

The plan is necessary and valuable, but regex-only scraping is too brittle.

Spot checks:

- `session_arc/acts.jsonl`: 120 rows.
- `session_arc/arcs.jsonl`: 43 rows, with `demotions[]` as strings or arrays of strings.
- `session_arc/verify.jsonl`: 43 rows, 42 corroborated and 1 unverifiable.
- `ARC_DIGEST.md` reports the 3073-event spine, 10 over-claim flags, and the 4452-vs-3073 self-catch.
- `EXTERNAL_SYNTHESIS.md` explicitly warns that current verification is anachronistic: checking past acts against final disk state can falsely corroborate earlier claims.

Loss/risk:

- `demotions[]` are not structured. The adapter must parse, but also preserve raw strings and provenance.
- Dead-child identifiers collide across systems (`DC-NN`, arc demotions, organ retirements, cosmic dead children). Namespacing is correct but not enough; include source file, line/section, date, and affected claim id.
- `verify.jsonl` is evidence, not truth. It is partly LLM judgment and subject to file-existence corroboration bias.
- A true stream/keyhole cannot rely on final disk verification. It needs as-of checks keyed by `t_event`.

## 3. Federate vs Merge

Federation is the right call.

Reason:

- The existing stores have different semantics: canonical facts are state slots, measurement rows are observations, session arcs are provenance events, dynamics include taxonomy records, W_C is a soft-scored first-pass DB.
- Physical merging now would force premature schema agreement and destroy the local compilers' trust boundaries.
- Existing dirty/stale areas need isolation: W_C schema drift, dynamics coupling drift, overlays not ingested, L0 validation flags, and measurement-era incompatibility.

Recommended shape:

```text
source stores stay where they are
  -> manifest records every artifact and secret exclusion
  -> adapters emit generated global/events/*.jsonl
  -> compile_global.py materializes views
  -> HYPERSPACE.html reads only compiled/global render JSON
```

So: **federated sources, generated global projection, compiled materialized merge**. Do not make `global/events/` the hand-edited source of truth until all adapters round-trip cleanly.

## 4. Security

### Finding: secret exclusion is necessary but insufficient

I confirmed `measure/.openrouter_key` exists and is 73 bytes. I did not read or print its value. The parent `D:/PlatformOperator/research/pav/.gitignore` excludes `.openrouter_key`, `*.key`, `.env`, and `secrets.*`, but gitignore does not protect a harvester.

The draft predicate (`*.key`, `.openrouter_key`, `.env*`, `secrets.*`, dotfiles, and content prefixes `sk-or-`, `sk-`, `AKIA`, `AIza`, `ghp_`) is a good start, but not sufficient.

Problems:

- `head_bytes` can miss secrets later in a file. Use streaming scanning before persistence, not just head scanning.
- Prefix coverage is incomplete. Add at least `sk-proj-`, `sk-live-`, `github_pat_`, `glpat-`, `hf_`, `xoxb-`, `xoxp-`, `npm_`, `ya29.`, `-----BEGIN PRIVATE KEY-----`, `-----BEGIN OPENSSH PRIVATE KEY-----`, Azure connection strings, JWT-like high-entropy tokens, and generic entropy detection.
- `.log`, `.console.txt`, `.out`, stdout logs, SQLite files, and generated HTML/JS can leak prompts, hidden reasoning, raw outputs, local paths, and sometimes keys. The file search shows many measurement logs and stdout logs under `measure/` and `session_arc/`.
- Era 2 JSONL run rows include `content` and `reasoning`. Hidden reasoning text is not automatically safe to publish into a global substrate.
- Local absolute paths leak usernames, project layout, and memory locations. `WHERE_WE_ARE.md` references `C:/Users/Admin/.claude/projects/D--/memory/`, and W_C refs include `D:/PlatformOperator/...`.
- Grepping final substrate for secret prefixes is necessary but weak. A secret can be transformed, base64 encoded, split, or stored in a compressed/SQLite artifact.

Required security gates:

1. Path denylist before opening: key/env/dotfile/cache/db/log/out/stdout.
2. Streaming content scanner before any emitted artifact.
3. Entropy scanner plus provider-specific regexes.
4. Raw/private tier separated from public/global compiled tier.
5. Redaction of local absolute paths in exported views, with path hashes or repo-relative refs.
6. No raw `reasoning` in public compiled outputs; store derived features and raw hash.
7. CI fail on generated `global/`, `compiled/`, `html`, `js`, and `sqlite`, not just JSONL.
8. Secret rotation remains blocking.

## 5. 4D Render Feasibility And `globe_cone_unified.html`

I opened `../toys/globe_cone_unified.html`. It is real and substantial:

- 614 lines, 45,971 bytes.
- Has a canvas app, 3D orthographic camera (`camBasis`, lines 182-193), log2 scale ladder (`L2`, `SCALE2`, lines 141-162), spatial fisheye lens (`fisheye`, lines 164-178), time scrubber (`drawScrubber`, lines 357-393), hard-coded physical/latent objects (`OBJ`, lines 198+), scene fetch (`../scene/fable_takedown.scene.json`, line 474), globe skin fetch (`../world_land.json`, line 531), and a globe-in-log layer (`globeFrame`, `drawGlobe`, `drawGlobeEvent`, lines 503-600).

It is **not** 70% of the planned hyperspace viewer.

Missing core primitives from Phase 4:

- No `Mercator`, `Daners`, `isoLat`, or `surfacePoint` implementation found.
- No globe-to-flat Mercator morph. The existing `z` control shrinks a globe onto Earth's cone dot, not a conformal globe<->Mercator dial.
- No global substrate event ingestion. It fetches only scene JSON and world land.
- No `t_event`/`t_obs` bitemporal thread model. It has a single `now` scrubber and scene beats.
- No render-height sharpening at observation time.
- No explicit physical and latent membranes with `h_latent` within/under/above toggle.
- No `bit_unit`-driven COIN render law, no measured/estimate/modelled additive channels, no disagreement rendering, no correction layer.
- No generated FIG-1..8.

Demote-not-kill verdict: the file is a useful canvas/control/globe/log-cone base, probably **40-55% of a generic visual chassis**, but much less than 70% of the actual hyperspace viewer. The "~250 new lines" estimate is too low. Expect a real build closer to:

- `build_hyperspace.py`
- a dedicated compiled render JSON schema
- 800-1200 lines of viewer code if kept vanilla JS
- browser smoke tests and pixel checks for globe, Mercator, bitemporal threads, and correction layer

## 6. Marker vs `reasoning_tokens`

The endpoint decision should be:

- **Use markers as primary only where a task-specific marker extractor is validated.**
- **Keep `reasoning_tokens` as a fallback proxy for within-model, within-experiment signs, not cross-model magnitudes.**
- **Never compare raw magnitudes across Era 1, Era 2, or signal types without an explicit bridge.**

Evidence:

- `measure/nf_markers.py` says it counts trial-division markers in reasoning text instead of `reasoning_tokens`, because tokens conflate compute with narration length. Its regex is divisibility/trial-division specific.
- `V10c_NF_MARKERS_RESULTS.md` says `reasoning_tokens` is model-dependent/noisy and markers should be preferred for fine compute claims.
- `CROSS_MODEL_RUNCARD.md` says OpenRouter `effort:"high"` fidelity is unresolved.

The draft's "Back-apply the marker re-score to other experiments where reasoning text is saved" is too broad unless implemented as an extractor registry:

```json
{
  "extractor_id": "nf_trial_division_markers_v1",
  "valid_for": ["v_nf"],
  "patterns": ["divisib", "remainder", "mod", "/N", "trial-divi"],
  "invalid_for": ["v10c locate-only", "sv verdict", "generic prose reasoning"],
  "output_unit": "marker_count"
}
```

For non-NF experiments, keep both:

- raw usage `reasoning_tokens`
- raw reasoning hash
- optional derived task-local markers if a validator exists
- a `notes` flag that says exactly what the endpoint can and cannot support

## 7. Biggest Risk

The biggest risk is **global substrate over-unification**: a single event stream makes all records feel joinable, but the corpus contains different epistemic objects:

- verified factual slots
- measurement trials
- model-specific proxies
- prose-only conceptual claims
- soft W_C scores
- stale/demoted dynamic claims
- session provenance with as-of-time hazards

If the global compiler does not enforce unit, era, model, experiment, source, and lifecycle boundaries, the render will become a beautiful laundering machine: it will turn caveats into geometry.

Security is a blocking operational risk, but it is tractable. The deeper system risk is semantic: wrong joins will look canonical.

## 8. What Is Missing

### Hard invariants and negative tests

Add tests that must fail:

- join `era1-openai` reasoning tokens with `era2-openrouter` reasoning tokens
- join `markers` with `reasoning_tokens` without bridge
- aggregate across models without `model` in group key
- best-value-collapse measurement reps
- render `prose-only` W_C utility as measured bits
- ingest `.openrouter_key`, `.log`, `.out`, stdout logs, SQLite, or dotfiles
- export raw `reasoning`
- verify an old `t_event` against a file that did not exist then

### Adapter golden fixtures

For each adapter, create 5-10 raw input rows and exact expected global events. Include ugly cases:

- Era 1 run row
- Era 2 run row with reasoning
- W_C row with missing id and prose utility
- stale dynamics coupling
- FALSIFIER organ retirement
- arc demotion string
- overlay file
- L0 validation flag

### Bridge records

Any cross-unit display needs a bridge record with scope, math, and "not valid for" limits. Without this, `bit_unit` will be abused.

### Raw preservation

Every normalized event needs `raw_ref` and `raw_sha256`. For small records, keep `raw` in a private/raw tier. For large/private records, store a hash and a pointer only.

### Public/private artifact policy

The plan needs a rule for what can ship:

- public compiled views: no secrets, no raw hidden reasoning, no local absolute paths, no private memory refs
- private raw store: can hold raw logs/reasoning behind a denylisted path and explicit retention policy

### As-of verification

The stream/keyhole phase must implement as-of verification before it claims history. The existing `EXTERNAL_SYNTHESIS.md` explicitly says this is not solved.

### Render acceptance tests

Before calling the 4D viewer built, require:

- desktop and mobile screenshot checks
- canvas nonblank pixel checks
- globe visible
- Mercator flatten visible
- bitemporal thread visible
- correction layer visible
- events loaded from compiled global JSON, not hard-coded fixtures
- no overlap/label blowouts

## Final Recommendation

Proceed, but change the plan's gate order:

1. Rotate the key and implement redaction/denylist CI.
2. Add global event schema with enforced `model`, `slug`, `experiment_id`, `unit`, `extractor`, `raw_ref`, and comparison policy.
3. Build adapter golden fixtures and invalid-join tests before bulk harvest.
4. Federate source stores; generate `global/events/` as compiled projection.
5. Normalize W_C and dynamics without deleting superseded claims.
6. Treat marker counts as task-specific primary endpoints, not universal replacements.
7. Downgrade the 4D chassis estimate and build a proper render JSON plus browser tests.

This keeps the plan alive and much stronger. The architecture is good. The missing piece is not more ambition; it is compiler-enforced honesty.
