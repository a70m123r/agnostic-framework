# WHERE WE ARE — the ground-truthed picture of the latent-camera corpus

**Date:** 2026-06-20 · **Author:** lead synthesizer (Opus 4.8) · **Status:** ground-truth audit, pre-harvest
**Scope:** the full latent-camera / canonical-genealogy corpus across
`D:/PlatformOperator/research/pav/candidates/` and the memory layer at
`C:/Users/Admin/.claude/projects/D--/memory/`.

This document is the honest snapshot before the big harvest: **what exists, what state it is in
(live / stale / spec-only), what is durably true, what infrastructure already exists to build on,
the demote-not-kill ledger, and the verified discrepancies + blockers.** It is itself written under
the COIN: every number below was independently re-checked against disk on 2026-06-20; claims I did
**not** re-derive are marked `[not re-derived]`.

---

## 0. The one-line picture

We have **two mature, working substrate+compiler+viewer systems** (the canonical-genealogy fact
substrate and the camera's `scope`/`session_arc`/`dynamics` mini-substrates), **a deep and honest
measurement program** (V1→V10c/NF/SV, two model-eras, cross-model audited, with a dated
dead-children ledger), **a third lighter event DB** (the Latent Olympics `wrapper_classes_phase1.json`),
and **a fully-specced-but-unbuilt headline viewer** (the 4D hyperspace globe↔Mercator dial). The
harvest is mostly **adoption + normalization of formats that already exist**, not green-field
invention. The single thing that must be handled before any glob-based harvest runs is a **live API
key sitting in the measurement directory.**

---

## 1. The slices — what exists, by area

### Slice A — The digestion measurement program (`hyperspace_spec/measure/`)
**State: LIVE, the richest empirical asset (~57 MB).** The place the camera's pixel was actually
measured and calibrated.

- **Harnesses (all live, stdlib + OpenRouter/OpenAI):** `providers.py` (Era-2 solve layer),
  `digestion_measure.py` (V1), `digestion_v2.py`/`v3.py`/`v4.py`/`v5.py` + companions,
  `v6_additive.py`, `v7_burial.py`, `v8_camo.py`, `v9_gravity.py` (+ v9b/c/d),
  `v10_framestrip.py` (the shared substrate factory), `v10b_irrelevant.py`, `v10c_selpos.py`,
  `v11b_matched.py`, `v_nf_labelcompute.py`, `v_sv_verdict.py`, `compare_3way.py`,
  `nf_markers.py` (the marker-count re-score), `v9b_resistance.py` (the shared `paired()` stats util).
- **Data:** per-experiment `*_labels.LOCK` (sha256 pre-registration) + `*_labels.jsonl` (frozen
  stimuli) + `*_run.<model>.jsonl` (Era-2 per-model run logs) / `v*_run.jsonl` (Era-1 single file).
- **Result docs (live):** `CROSS_MODEL_RUNCARD.md` (authoritative provenance ledger),
  `V10c_NF_MARKERS_RESULTS.md` (2026-06-20 capstone), `V_NF_SV_CROSSMODEL_RESULTS.md`,
  `V10b_V11b_CROSSMODEL_RESULTS.md`, `V10_V11_CROSSMODEL_RESULTS.md`, `MEASUREMENT_RESULTS.md`,
  and the Era-1 `V2_RESULTS.md … V9d` family + `EXTERNAL_SYNTHESIS_V*.md` (12 folded external passes).
- **Viewer:** `TICKER.html` (V1-only, stale).

**Verified live state:**
- `v10c_labels.LOCK` sha256 = `68c451048cff96e8…` — reproduces byte-for-byte ✓; `n_items` 600,
  100 seeds, 6 conds `[H/N/Z × LEAD/TRAIL]`.
- `v10c_run.deepseek.jsonl` = **1800 rows** (600 items × 3 reps); `v10b_run.deepseek.jsonl` = **576
  rows** (24 seeds × 6 conds × 4 reps). **Rep count differs per experiment (3 vs 4) and is NOT in
  the LOCK** — a normalizer must derive reps from the run rows.

### Slice B — The existing GLOBAL substrate format (the harvest TARGET) (`substrate/` + `l0_wrappers/`)
**State: LIVE, ratified, this is what we harvest INTO.**

- `SUBSTRATE_SPEC.md` — the canonical contract (fact record, verification record, certainty rubric,
  state machine, best-value resolution, scale story).
- `compile_substrate.py` — 622-line stdlib deterministic compiler (globs `facts/*.jsonl` +
  `verifications/*.jsonl` → `substrate.db` + `compiled/<spec>.compiled.json` + `_summary.json`).
- `facts/` (19 files), `verifications/` (9 files), `compiled/` (10 exports), `substrate.db`
  (gitignored, disposable).
- `SCHEMA_v2.md` (ratified merge-event field vocabulary), `PROXY_SPEC.md` (render weights).
- L0 sibling: `candidates/l0_wrappers/` — `L0_WRAPPER_SPEC.md`, `l0_compile_wrappers.py`,
  `wrappers/`, `group_configs/`, `SWEEP_LOG.md`.

**Verified live state (`compiled/_summary.json` → `totals`):**
`{facts: 1372, verifications: 359, best_values: 1107, specimens_with_facts: 10,
validation_errors: 0, validation_flags: 217, disputed_best_values: 11,
best_values_with_disputed_alternatives: 22}` ✓ exactly as inventoried.
`SUBSTRATE_REPORT.md` (1029 facts / 7 specimens) is **STALE** — read `_summary.json` for live numbers.

### Slice C — Viewers + the 4D/hyperspace render spec (`hyperspace_spec/`)
**State: MIXED — four small viewers BUILT, the headline viewer SPEC-ONLY.**

- **BUILT, self-contained, substrate-injected (sizes verified):** `scope/SCOPE.html` (98 854 B),
  `session_arc/BITEMPORAL_3D.html` (59 114 B), `session_arc/TIMELINE.html` (188 237 B),
  `dynamics/GUESS_WHO.html` (81 236 B), `measure/TICKER.html` (6 021 B).
- **Matching compilers (all live, stdlib, jsonl→compiled.json→inject):** `compile_scope.py`,
  `compile_arc.py`, `build_bitemporal.py`, `build_guesswho.py`, `normalize_dynamics.py`,
  `recompile_channel.py`, `build_ticker.py`.
- **SPEC-ONLY (NOT built):** `SPEC.md` (header literally reads *"design only, no build … NOT
  built"*), `SCOPE_NESTING_LOD.md`, `SPEC_BRIEF.txt`. The 3D globe↔2D-Mercator dial (Daners
  conformal morph, physical+latent membranes, substrate-as-light splats) **is not implemented in any
  HTML** — confirmed: `isoLat`/`Daners`/`surfacePoint` appear only as descriptive *text inside* the
  SCOPE/GUESS_WHO data blobs, never as a working dial. `FIG-1..8` do not exist as files.
- **Intended chassis** `toys/globe_cone_unified.html` exists **one level up** in
  `canonical_genealogy/toys/` (out of the `hyperspace_spec/` slice).

### Slice D — Dynamics / bestiary / tactics / couplings (`hyperspace_spec/dynamics/` + docs)
**State: LIVE substrate, with one stale compiled headline + one un-reconciled coupling generation.**

- `dynamics/dynamics.jsonl` — **88 records: 41 creatures + 37 tactics + 10 couplings** ✓.
- `dynamics/compiled/dynamics.compiled.json` — compiled view; **`stats.reduction` is STALE**
  (still asserts the pre-falsifier "~6 organs / 6.8:1" headline).
- Prose parents (live): `LATENT_DYNAMICS_BESTIARY.md`, `ADVERSARIAL_TACTICS.md`, `COUPLINGS.md`,
  `DIGESTION_DYNAMICS.md`, `CHANNELS.md`, `FALSIFIER_REPORT.md`, `EXTERNAL_SYNTHESIS_TACTICS.md`.
- Channel views: `compiled/channel_jungle.json`, `compiled/channel_battlefield.json`.

**Verified:** `COUPLINGS.md` carries **12** refined control-theory edge headers (not 13) vs the
substrate's **10** older couplings → real, un-reconciled mismatch, magnitude 12-vs-10.

### Slice E — The Latent Olympics (two referents)
**State: (a) the digestion Olympics = Slice A; (b) the W_C-emergence DB = LIVE but spec-drifted.**

- (b) `candidates/latent_olympics_data/wrapper_classes_phase1.json` — **25 records** ✓,
  `_status:"Tier-3 WORKING first-pass"`, `schema_version:0.1-phase1`. Rows carry
  `name/tier/status/localKernelCanon/netProduct/akaWhoCalledIt/origin/overlaps/utility/
  classifierWeights/refs`.
- Specs: `latent_olympics_phase1_SPEC.md`, `latent_olympics_DESIGN_SKETCH.md` (the grander arena).

**Verified schema drift:** `overlaps` are **bare strings** (not typed edges); `classifierWeights`
**are** numeric `{spread,utility,legacy,rigor}`; utility legs are **prose**, not numeric; **no `id`
field, no `pipeline` field** — the live rows are the flatter shape, diverging from the embedded
`_schema_doc`/DESIGN_SKETCH. **Status is unnormalized free-text** (`risen-to-top`, `RISEN`,
`ESTABLISHED`, `DORMANT,` with trailing comma, `RESURRECTED-then-RISEN`, …) — the clean
"15 risen / 3 dormant…" buckets require fuzzy grouping.

### Slice F — Provenance, external-pass history, demote-not-kill ledger
**State: LIVE, dense, consistent — but fragmented across many files.**

- `session_arc/` — `acts.jsonl` (**120**), `arcs.jsonl` (**43**), `verify.jsonl` (**43**, 42/43
  corroborated, 10 over-claim flags), `ARC_DIGEST.md` (the prose honesty ledger),
  `EXTERNAL_SYNTHESIS.md`, raw `codex_*`/`gemini_*`/`claude_*` audit files (44 in session_arc).
- `FALSIFIER_REPORT.md` — the blind-coded organ experiment (Fleiss κ=0.671, 5 robust organs,
  1 dead, 3-4 named-missing) — **prose + one embedded JSON vote block, not a record set.**
- `CROSS_MODEL_RUNCARD.md` — exact models/slugs/prices/lock-hashes per era.

---

## 2. Formats present (corpus-wide)

`md` (specs, ledgers, syntheses, results) · `jsonl` (append-only fact/verification/relation/run logs
+ frozen stimuli) · `json` (compiled exports, `_summary`, wrapper views, group_configs, the W_C DB,
templates) · `sqlite` (`substrate.db`, gitignored, disposable) · `py` (compilers + harnesses, all
stdlib/offline) · `html` (5 built viewers) · `js` (`arc_data.js`, a derived viewer include) ·
`txt` (briefs, console logs) · `LOCK` (sha256 pre-registration sidecars) · `.openrouter_key`
(**secret — see §5**) · `pyc`/`*.out`/`*.console.txt` (caches, low-value provenance).

---

## 3. The durable findings (audit-survived, demote-not-kill applied)

**The camera SPINE (cross-model, confirmed 3 ways):** the reasoning cost the camera reads is
**PREDICATE APPLICATION whose volume scales with the number of candidates evaluated, NOT bytes read**
(V10b lookup near-floor; SV verdict flat-to-negative under 5× substrate; NF compute contrast).

- **Dissociation:** LOCATING vs APPLYING differ 20×→77× (deepseek), 36×→77× (gemini), 8.5×→21×
  (qwen) on identical substrate — conservative lower bounds (correct-only censoring).
- **D_application (SV clean subtraction, task held fixed):** +524…+11 980 across models, **growing
  with size** — the dominant cost.
- **V1 aleatoric/epistemic split (real codelength):** incompressible noise = highest cold cost
  (188 bits) yet 2% dissolve; structured facts dissolve 49–70%. Two-clock gap is exact.
- **V4 parametric ladder:** partial-Spearman(reasoning_tokens, effective_ops | display_ops) =
  **+0.894** (CI [+0.864,+0.917], n=180) — camera tracks real work, not display volume (+0.178 raw).
- **Frame decomposed (V10c n=100):** a robust cross-model **ORIENTING** cost (header HELPS:
  H < Z ≈ N on all 3) + a **model-dependent late-rescan** cost (gemini +93, deepseek +17, qwen null).
- **De-amortization:** losing an amortized word ("prime") costs reasoning **only when a hard rule
  must then be applied** = word-amortization × rule-difficulty (V11b RESCUED +307/+836/+2150).
- **NF marker-fix:** re-scoring on trial-division MARKER counts (no new API calls; CoT saved)
  partially un-demotes DC-38 and establishes **`reasoning_tokens` as a model-dependent, noisy,
  narration-confounded compute proxy** — markers preferred for fine compute claims.

**The conceptual canon (where each canonical equation is written):**
1. The agnostic UNIT: `measured_bits(W) = min(cost_ub, evidence_lcb)`;
   `unpaid_bits = max(0, cost_ub − evidence_lcb) = blur` — `latent_measurement_candidates.md`
   (ratified + 11/12 falsifiers pass).
2. The three strict-COIN laws (FIDELITY-not-truth · SHARPNESS<1-always · both-halves-one-law) —
   `THE_LATENT_CAMERA.md`.
3. `σ = 2^(−bits)` as a Cramér-Rao theorem via OUGS Jacobian-Covariance — `K2_tomography.md`
   (physical axis validated; latent axis spec).
4. The cost-law / two-clocks (shutter + film-ISO; Bennett depth; Landauer tie) —
   `DIGESTION_DYNAMICS.md §12`.
5. Render law `σ = max(EWA_floor, k·2^(−bits))`, 3 channels MEASURED/ESTIMATE/MODELLED —
   `SPEC.md §7`. Landauer denominator `kT·ln2 = 2.8e-21 J/bit`, 17-layer iceberg —
   `MODEL_COST_STACK.md`.

**The W_C-emergence DB (Slice E-b):** 25 named wrapper-class "parents" with lifecycle status,
`netProduct` (the W_C compiled), `classifierWeights`, and `refs` provenance — the seed of an
"any-event arena" where a rival theory/belief/model is just another contestant scored on the same
dissolve/cost + Pareto + dated-lifecycle columns.

---

## 4. The infrastructure we already have (reuse, don't rebuild)

| Asset | Path | Reuse for the harvest |
|---|---|---|
| Fact-record contract + state machine + best-value resolution | `substrate/SUBSTRATE_SPEC.md` | **The global schema.** Adopt, don't reinvent. |
| Deterministic compiler (glob→validate→resolve→compile) | `substrate/compile_substrate.py` | The recompile engine; folds new fact files automatically. |
| Second-stage wrapper/channel builder | `l0_wrappers/l0_compile_wrappers.py` | Template for derived views + group_configs. |
| 5 stdlib jsonl→compiled→inject compilers | `hyperspace_spec/{scope,session_arc,dynamics}/*.py` | The proven substrate→viewer toolchain; all run clean. |
| COIN render-cap (`render = min(declared, BUCKET_CAP[bucket])`) | every compiler above | The render-invariant; unify the divergent cap ladders. |
| Materialized-view pattern (`constellate_by`/`branch_by`) | `dynamics/recompile_channel.py` | Template for re-projecting the unified substrate to any global viewer. |
| Stats util (`paired()` bootstrap + sign test) | `measure/v9b_resistance.py` | Reuse so harvested numbers match the docs exactly. |
| Provenance ledger (models/slugs/locks/prices) | `measure/CROSS_MODEL_RUNCARD.md` | The join key for normalizing run files — do NOT infer params from filenames. |
| Marker re-score (no new API calls) | `measure/nf_markers.py` | The honest compute endpoint; back-apply to other experiments. |
| Intended 4D chassis (~70% of a globe/cone viewer) | `canonical_genealogy/toys/globe_cone_unified.html` | The base the hyperspace viewer extends (~250 new lines per SPEC). |

---

## 5. The demote-not-kill ledger (the honest falsification gauge)

Demote-not-kill is fully instantiated and dated, in **multiple disjoint encodings**:

- **Numbered dead-children DC-34…DC-40** across `V10b_V11b_…`, `V_NF_SV_…`, `V10c_…` result docs
  (running tally asserted as **"40 dead-children"** in prose — not machine-counted).
- **Per-arc `demotions[]`** in `session_arc/arcs.jsonl` + the prose Honesty ledger in `ARC_DIGEST.md`
  (~11 dated over-claim flags; sharpest self-catch: claimed 4452-event spine, disk holds 3073).
- **Organ retirements** in `FALSIFIER_REPORT.md` (BANDWIDTH-CAPACITY dead, 1/60 votes; 3-4 missing
  organs named blind).
- **Cosmic "six dead children"** + the V4–V9d `EXTERNAL_SYNTHESIS` DEMOTE sections.

**Lifecycle, not graveyard:** DC-38 was *partially un-demoted* by the V10c marker re-score; DC-39
was *resolved* by the Z-arm control. Demotions can reverse with a better control.

**Standing external-pass record:** codex (GPT-5.5) + gemini + Claude(Opus) independently re-derive
every headline from locked files and converge — *"not one number failed reproduction"*; the
demotions are about interpretation/labels, not arithmetic.

---

## 6. Verified discrepancies & blockers

### 6.1 BLOCKER — live secret in the harvest path (top priority)
`measure/.openrouter_key` is a **live plaintext OpenRouter credential** (73 bytes, present on disk).
It **is** correctly gitignored (`.gitignore` lists `.openrouter_key`, `*.key`, `secrets.*`), so it
has not been committed — but **any harvester that globs `measure/*` would ingest it**. The survey
under-stated this as "provenance context."
**Rule:** exclude by name AND by `*.key`/dotfile glob from every harvest pass; **rotate the key**
(it has been exposed to agent contexts).

### 6.2 BLOCKER — two incompatible run-record schemas (no shared key)
Verified: **Era-1** `v4_run.jsonl` keys =
`[answer, correct, display_ops, effective_ops, exhausted, expected, family, prompt_words,
reasoning_tokens, seconds, seed, target, tier]` (has `tier/answer/expected`, **no
model/slug/reasoning**). **Era-2** `v10c_run.deepseek.jsonl` keys =
`[completion_tokens, cond, content, correct, exhausted, finish, got, item_id, model, prompt_tokens,
prompt_words, reasoning, reasoning_tokens, rep, seconds, seed, slug, truth]` (**no `tier`**).
Normalization must map `answer→got`, `expected→truth`, inject `model='gpt-5.5'`, pull `tier` from the
LOCK. **Rep count differs (v10c=3, v10b=4) and is only derivable from the run rows.**

### 6.3 BLOCKER — noisy-proxy signal
`reasoning_tokens` is the project's **own** documented model-dependent, narration-confounded proxy.
The durable endpoint (trial-division marker count) exists **only for NF** today. OpenRouter
`effort:'high'` fidelity is **unverified**. **Magnitudes are NOT comparable across eras/models** —
only within-model sign/significance deltas. Era must be a hard partition key.

### 6.4 BLOCKER — incommensurable measurement axes
V1 uses `residue_bits`/codelength (davinci-002); V4+ uses `reasoning_tokens`. **Separate tables,
linked only at experiment level — never merged.**

### 6.5 Stale compiled headlines
`dynamics/compiled/dynamics.compiled.json` `stats.reduction` and the `ADVERSARIAL_TACTICS.md`
headline still assert the pre-falsifier "6.8:1 / ~6 organs" — **contradicted by
`FALSIFIER_REPORT.md` (κ=0.671, 5 organs)**. Harvest must carry the falsifier verdict, not the
compiled headline. `SUBSTRATE_REPORT.md` is likewise stale (1029/7 vs 1372/10).

### 6.6 Coupling generation un-reconciled
`COUPLINGS.md` = **12** refined control-theory edges; `dynamics.jsonl` = **10** older couplings;
two naming conventions; never entity-resolved. The refined edges were never re-normalized into the
substrate.

### 6.7 Olympics schema drift (blocks the W_C harvest)
Live rows are the flatter shape (bare-string overlaps, prose utility legs, no id/pipeline) vs the
embedded `_schema_doc`/DESIGN_SKETCH. **Single-agent-generated; never got the cross-model external
pass** the digestion line applies religiously. **Status is unnormalized free-text.** Reconcile
(migrate rows up OR demote spec to aspirational) before merge.

### 6.8 SPEC.md carries an un-corrected over-claim
`SPEC.md` line 13 still presents the keystone as *"Solomonoff/MDL: appearance = 2^−bits"* — the very
**Solomonoff = 2^−bits identity that the cosmic-coin note + external pass DEMOTED** to standard
MDL/log-loss shared bit-currency (lzma ≠ universal mixture). The live spec text has not been
corrected. **Demotions must travel with the equations as a correction layer.**

### 6.9 Provenance fragmented, not missing
The "40 dead-children" tally is prose-asserted across ≥6 files with **colliding numbering schemes**
(`DC-NN` vs arc-demotions vs organ-retirements vs cosmic "six"). No single `dead_children.jsonl`; no
top-level manifest tying `experiment → lock sha → run files → result doc → DC ids`.
**Two `SWEEP_LOG.md` files exist** (`l0_wrappers/` AND `dial_engine/`) — both must be reconciled,
namespaced by era.

### 6.10 Smaller verified items
- **Specimen filename/id mismatch:** fact stem `qm_relativity.{entities,events}.jsonl` but compiled
  output `quantum-gravity.compiled.json` — a glob-keyed harvester would mis-key this one specimen.
- **`v10c_labels.LOCK` note self-contradicts:** says "2x2 (header × position)" but lists 6 conds =
  3×2. Cosmetic label error in a provenance anchor.
- **Split-brain residue:** `l0_wrappers/facts/` (5 staging files) duplicates the canonical
  `substrate/facts/l0_catalog.*.jsonl`; the compiler does NOT glob it, but a naive whole-tree
  harvester would double-count. **Harvest only from `substrate/facts/`.**
- **Overlay spec/code drift:** `SUBSTRATE_SPEC.md` promises `--ingest-overlays`; `compile_substrate.py`
  has no such flag; **8 `overlays/*.overlay.json`** sit un-harvested.
- **L0 validation OFF:** all ~166 `l0_catalog.*` facts raise the expected "specimen 'l0-catalog' not
  found" flag (no anchor specimen) — subject_id typos in the L0 layer would not be caught.
- **`agnostic_framework.dev.jsonl`** (48 self-specimen facts) uses local-path `D:/…` sources →
  "provenance suspect" flags; 100% pending, unaudited.
- **Mojibake** in committed JSON (W_C DB utility prose + non-ASCII source titles) → read/write
  explicit UTF-8.
- **`normalize_dynamics.py`** depends on a machine-local Temp `.output` file (currently present but
  volatile/uncommitted) — the durable parents are the `.md` docs.
- **Empty external arm:** `session_arc/gemini_v10v11_audit.md` is 0 bytes (IneligibleTierError) —
  a real gap to mark, not drop.

---

## 7. Bottom line

The architecture is sound and most of the harvest is **adoption of existing formats**. The work that
remains is: (1) **safely** harvest around the secret; (2) write **adapters** that reconcile the two
run-schemas, the two coupling generations, and the W_C schema drift; (3) **carry the
demote-not-kill ledger** as first-class records so over-claims never travel without their correction;
(4) build the **one headline thing that does not yet exist** — the 4D hyperspace viewer — by
extending the chassis that already does. The concrete phased plan is in
`DRAFT_HARVEST_PLAN.md`.
