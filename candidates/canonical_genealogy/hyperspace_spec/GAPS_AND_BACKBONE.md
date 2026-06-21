# GAPS AND BACKBONE — the structural spine for the LatentEvent substrate, and what the harvest plan must absorb

**Date:** 2026-06-20 · **Author:** lead synthesizer (Opus 4.8) · **Status:** synthesis of four crawler lenses, ground-truthed against disk
**Companions:** [`DRAFT_HARVEST_PLAN.md`](DRAFT_HARVEST_PLAN.md) (the plan this sharpens) · [`WHERE_WE_ARE.md`](WHERE_WE_ARE.md) (the ground-truth audit) · [`WRAPPER_PROBE_OBSERVER.md`](WRAPPER_PROBE_OBSERVER.md) · [`CANONICALIZER.md`](CANONICALIZER.md) · [`KEYHOLE_BLOCK_UNIVERSE.md`](KEYHOLE_BLOCK_UNIVERSE.md) (the standing audit-corrections, which override two crawler recommendations — see §4 caveat)

This document does three things: (1) names the **backbone** — DAG vs RAG vs both — with the honest tradeoffs; (2) gives the **prioritized gap list** the plan must absorb, separating load-bearing from nice-to-have; (3) lists the **concrete plan amendments**, phase by phase. Every disk claim below was re-checked on 2026-06-20.

---

## 1. THE BACKBONE RECOMMENDATION

### Verdict (one line)
**Both, with a strict split: a DAG is the structural source-of-truth (lineage, acyclic-to-present, compiler-checked); a KG-RAG is the derived retrieval layer over it (the keyhole = spreading activation along typed edges); it is NOT a vector store, and the latent/meaning lane stays blurred until the missing NLI instrument lands.**

### Why a DAG is the spine, not a vector index
The substrate is **already DAG-shaped and we did not notice it was the spine**. The global EVENT record carries a `parents` array of typed edges plus dual-time, `phys_latent`, `bit_unit`, bucket, and lifecycle ([`DRAFT_HARVEST_PLAN.md`](DRAFT_HARVEST_PLAN.md):81-125). The genealogy is a rooted directed graph that stops at the present, with typed edges `weld.parents`, `relatives`, `descendants`, `forcing_events`, `rival_coupling` (`SCHEMA_v2.md`, `data-layer.md`). The keyhole retrieval primitive is *already specified* as graph traversal: the excitation-emission probe seeds the substrate DAG and spreads activation along typed edges, capped by the COIN (`rendered_ping(w) <= measured_bits(w)`) ([`WRAPPER_PROBE_OBSERVER.md`](WRAPPER_PROBE_OBSERVER.md):102-126). AnalyzeImpact and active-aiming already run over the typed-edge DAG with EIG-per-cost retrieval (`K3_observation_to_knowledge.md` §3). The pieces exist; no prior doc *named* a DAG/RAG as THE structural spine — this synthesis does.

### The honest split (a DAG with a bounded cyclic overlay, not a pretend-pure-DAG)
1. **Lineage edges → strict DAG, compiler-enforced no-cycle.** `parents`, `weld`, `descendants`. Acyclic-to-present by construction; topo-sortable; ancestor queries valid.
2. **Genuinely cyclic edges → a separate typed relation layer.** Couplings, forcing-feedback, polarization-backsliding loops, and the Mirror/observer back-reaction are **real cycles**, surfaced twice in the corpus (`K4_democracy_keyhole.md` polarization-backsliding; `SCHEMA_v2.md` rival coupling). They are rendered as first-class diamonds, **excluded from topo-sort and ancestor queries**. Use the `rel:<type>:<target>` predicate lane the plan already hints at ([`DRAFT_HARVEST_PLAN.md`](DRAFT_HARVEST_PLAN.md):86).
3. **Retrieval is the keyhole spreading-activation traversal** (query → keyhole stream → predict-half prior-cut subgraph), which EIG and AnalyzeImpact already use.
4. **Embeddings stay an instrument, never the spine.** Cosine + echo-codelength live *inside* the canonicalizer as a measurement; no vector index over the corpus exists today (`FRONTIER_PLAN.md`, `CHANGELOG.md`). A vector lane is added **only behind the NLI gate** and **only for the WHAT/HOW axes — never WHY/meaning**.
5. **The DAG is a global compile that unions federated stores** with per-contract validity; cross-contract joins render blurred or are compiler-refused. Both external auditors converged on **federate, not physical-merge** (`memory:project_global_substrate_harvest.md`:14-17).

### The honest tradeoffs (the two seams that make this hard)
- **Acyclicity vs real cycles.** A pure DAG mis-models causal cycles (couplings, forcing-feedback, back-reaction). A pure relation-graph loses the lineage guarantees (topo-sort, ancestor queries, the demote-not-kill supersession spine). The split above is the price: two namespaces, one cycle-segregation invariant the compiler enforces. This is load-bearing, not cosmetic — the cycles are *on disk* (`K4`, `SCHEMA_v2`).
- **The latent axis needs an instrument that does not exist.** The meaning/WHY axis cannot be embedded honestly yet. The canonicalizer's symmetric paraphrase case is **VALIDATED** by embedding cosine (paraphrase 0.684 vs distinct 0.062, separation 0.622 — [`CANONICALIZER.md`](CANONICALIZER.md) §4), but the **asymmetric "derivable-not-just-reworded" case needs an NLI entailment check that is explicitly "still to wire"** ([`CANONICALIZER.md`](CANONICALIZER.md):79). Cosine conflates entailment with topicality. **Until the NLI instrument exists, the latent membrane renders blurred — a hard sharpness ceiling, not a placeholder zero.** A pure-vector-RAG over meaning would launder this unmeasured axis and lose provenance; that is the failure mode the COIN exists to forbid.
- **Pinned-relational, not intrinsic.** Even the validated latent unit is a *pinned relational bit*: verdicts are coder-invariant but absolute bits move **~88% across coders** (`latent_measurement_candidates.md`). So every latent bit must carry its measurement contract `{coder, era, model, frame, skepticism_dial}` — there is no single number line for meaning.

---

## 2. THE PRIORITIZED GAP LIST (what the plan must absorb)

The plan is **correct as a data-harvest skeleton** and both auditors endorse its federate-not-merge spine, append-only/demote-not-kill discipline, and chassis-reuse. Its defect is uniform: it **under-weights the use/measurement/navigation layer** that turns the harvest from a database into a latent camera. Several of these gaps are parked in the plan as *Open Questions* — which is precisely the problem, because the backbone needs **blocking guardrails** where the plan poses deferred questions.

### LOAD-BEARING (the backbone fails without these)

**G1 — The v0.3 wrapper record shape is missing; §2.1 carries a flat triple.** The canonical record must be **six content axes (WHAT/WHEN/WHERE/WHO/HOW/WHY) + WHOM observer + BEFORE/AFTER/FROM links + PER-AXIS `measured_bits`** ([`WRAPPER_PROBE_OBSERVER.md`](WRAPPER_PROBE_OBSERVER.md) §1.1-1.3). The plan's event record has only a flat `predicate/value` + single `parents` list + a single scalar `bit_unit.cost` — no per-axis ledger, no WHOM, no place for the probe/sandbox to attach. Without per-axis bits the COIN cannot say "sharp on WHERE/WHEN, blurry on WHY," which is the whole honesty claim. **This is the foundational schema gap; most other gaps attach to it.**

**G2 — The latent measurement unit and canonicalizer are BUILT-AND-TESTED but un-wired.** The plan's `bit_unit.signal_type` enum (`reasoning_tokens|markers|residue_bits|mdl_delta_bits|none`) never includes the validated unit `measured_bits = min(cost_ub, evidence_lcb)` (`latent_measurement_candidates.md`, RATIFIED + VALIDATED, 11/12 falsifiers) and never references the existing `cosmic_coin_probe/harness.py` the recommendation says to extend. The canonicalizer (embedding/NLI canon + codelength `residual_surface_bits`) is mentioned only as a *single parenthetical* in Open Q7. **Both instruments are on disk and validated today — this is wiring, not research.** (Honest scope: the NLI half of the canonicalizer is *not* built — see the §1 latent caveat.)

**G3 — The aggregation-faithfulness COIN (the "missing half of the COIN") is absent.** The plan enforces only `render = min(declared, BUCKET_CAP)` and per-leaf `render <= measured_bits`. The second inequality — `rendered_bits(parent) <= Σ measured_bits(children) − bits_discarded`, with a **mandatory spread-of-means term and `N_eff` for dependent sources** — is missing (`SCOPE_NESTING_LOD.md`:318 "this is the missing half of the COIN"; `K1_block_universe.md` §4.3 Guard 3). Without it, **zoomed-out parent aggregates manufacture crisp bits the substrate never paid for** (a broadcaster + audience averaged to one sharp point). This is the single most-cited gap in the corpus and it is a render-correctness bug.

**G4 — Entity resolution is a standing, un-solved liability the plan names but does not solve.** Three concrete collisions are on disk: (a) **couplings are three-way inconsistent** — `dynamics.jsonl` holds **10** records typed `coupling`, `COUPLINGS.md` has **12** `###` edge headings and a headline asserting **13** distinct edges (all verified on disk 2026-06-20); the refined edges were never re-normalized. (b) the **`qm_relativity` → `quantum-gravity` specimen mismatch** — fact stems are `qm_relativity.*` but the compiled output is `quantum-gravity.compiled.json`, so a filename-keyed harvester mis-keys exactly one specimen. (c) **cross-store name collisions** — W_C `overlaps` are bare strings pointing at concepts that also live as `creature`/`tactic` records, and dead-children carry four colliding numbering schemes (`DC-`/`arc-`/`organ-`/`cosmic-`). The plan relies on author discipline ("entity-resolve old↔new by endpoints/formal_name") — the exact thing it elsewhere refuses to trust. **Federation moves reconciliation from migration-time to query-time; it does not remove it.** The missing piece is a first-class `entity_aliases.jsonl` cross-store identity map with unresolved aliases as *counted visible debt*.

**G5 — The bitemporal as-of verify is unsolved; the plan parks the fix in the last phase.** `verify.jsonl` (43 records) checks past acts against **final disk state** — every record carries `artifacts_present` as *current absolute paths* with **no `t_event` field** (confirmed on disk: keys are `artifacts_present`/`artifacts_missing`/`verdict`, no as-of field). So a later edit can falsely corroborate an earlier `t_event` (`session_arc/EXTERNAL_SYNTHESIS.md` anachronism failure-mode). The bitemporal *schema* is in place (`t_event` + `t_obs`; `BITEMPORAL_3D.html` already separates them) but the *verify pass that honours it is not built*. Risk: if STREAM ships before the as-of verifier, the keyhole renders later edits as corroboration of earlier states — **the block sharpens itself with bits it did not have at `t_event`.** "Verify an old `t_event` against a file that did not exist then" must be a build-time test that **FAILS**.

**G6 — The unit-collapse risk: one `cost` column makes incommensurable axes look poolable.** Of five arenas: V1 `residue_bits` are bits-but-walled-off; W_C `mdl_delta_bits` is bits-but-empty (the field does not exist — 100% of W_C rows have `bit_unit=null` by construction, `netProduct` is pure prose); `reasoning_tokens` and `markers` are counts-not-bits; genealogy is `signal_type=none`. The partition keys (`era`/`signal_type`/`model`) are **string fields, not constraints** — "documentation that a join is illegitimate, enforced by author discipline." Any RAG consumer reading `cost` without branching on `signal_type` silently pools token-counts with bits. **The schema makes the wrong thing the easy thing.** Fix: per-signal columns + a typed accessor that raises unless the caller passes the matching `signal_type` + bridge records for any cross-unit display.

### USEFUL (the camera is materially weaker without these, but the spine stands)

**G7 — The K-pipeline (K1-K4) is the conceptual backbone of the keyhole vision and the plan never builds it.** K1 (block-universe/compiler laws, 5 honesty guards), K2 (tomography/fidelity-law, missing-wedge), K3 (the three per-axis knowledge gates + conjecture-stub lifecycle + EIG active-aiming), K4 (the democracy worked example) are the conceptual spine; the plan reduces the keyhole to a STREAM append-hook (Phase 5) + a bitemporal render (Phase 4) and references K2/K3/K4 **zero times**. Register K1-K4 + the KEYHOLE_BLOCK_UNIVERSE AUDIT CORRECTIONS as first-class correction-layer/spec records.

**G8 — The collective/observer/probe machinery is absent from the schema.** No `collective` arena exists. `COLLECTIVE_WRAPPER.md` adds the coordination term `C(N)` (`Cost(N) = Σ Workᵢ + Span(DAG) + C(N)`, the one new axis solver→swarm), the **DPI handoff-loss floor** (the skeptic's one genuinely-robust claim: `render <= measured-bits` lifted to the collective), and the BUILD/MAINTAIN/USE three-clock decomposition (the backward camera = Bennett depth). The probe/observer/mind-sandbox (`WRAPPER_PROBE_OBSERVER.md` §3-4) has nowhere to attach without G1.

**G9 — The USE / query / navigation layer does not exist.** There is no general query API or search box — the only access path is compile → inject → static HTML (`scope/compile_scope.py`; `build_guesswho.py`). The keyhole/spreading-activation probe IS the query primitive but is unbuilt as an interface. Needs a three-tier USE layer: (a) attribute retrieval, (b) semantic RAG via the validated embedding gate (WHAT/HOW only, behind the NLI gate for WHY), (c) DAG lineage traversal.

**G10 — Versioning/identity is named only as point-fixes, not a systematic layer.** Identity is a *trajectory* `D(t)`, not a fixed node (`WRAPPER_PROBE_OBSERVER.md` §2.1) — an entity IS its diachronic definition trajectory; "who called it" is definition-epoch-relative. 4D time-stacked reconstruction needs **anchor-based inter-slice transport maps** (drift is an alignment/identifiability problem; anchorless gaps are UNDERIDENTIFIED, `KEYHOLE_BLOCK_UNIVERSE.md` §9). The plan's entity-resolution is two ad-hoc joins with no `D(t)` identity and no transport-map alignment.

**G11 — Stale compiled artifacts launder as measured at the retrieve/generate boundary.** Phase 1.2 leans toward harvesting `*.compiled.json`, but `dynamics.compiled.json` still asserts the pre-falsifier `6.8:1 / ~6 organs` headline contradicted by `FALSIFIER_REPORT.md` (κ=0.671, 5 organs), and `SUBSTRATE_REPORT.md` is stale (1029/7 vs live 1372/10). `SPEC.md` still carries the demoted `Solomonoff = 2^−bits` identity. Fix: `compile_global.py` re-derives from source jsonl **by default** and ingests a `*.compiled.json` only when its content-hash matches a fresh recompile (else fail loud) — so stale headlines become *build errors*, not silent laundering.

### NICE-TO-HAVE (defer honestly; do not pretend they are built)

**G12 — The predict-half / forward camera stays 100% dark.** The upper camera (sealed conjecture-bubble) is unbuilt (Open Q8). Keep it explicitly deferred — but enforce **"never write a generated/predicted bit below the measured floor"** as a STREAM-hook invariant, so the deferral is honest rather than a silent gap.

**G13 — Path corrections before the manifest glob.** The 8 `*.overlay.json` live at `canonical_genealogy/overlays/` (confirmed: 8 files at `../overlays/`), **not** `substrate/overlays/`; both SWEEP_LOGs are at `candidates/` root level. Fix the path assumptions before Phase-1 globs.

---

## 3. CONCRETE PLAN AMENDMENTS (phase by phase)

**PHASE 0 (Guardrails — promote three deferrals here):**
- **A0.1** Apply the `Solomonoff → MDL/log-loss` correction to `SPEC.md` **now** (it is the render's contract), not in Phase 4. *(fixes G11)*
- **A0.2** Add a **DAG-validity invariant** to the schema: two edge namespaces — acyclic lineage (`parents/weld/descendants`, compiler no-cycle) and cyclic relations (`rel:coupling/forcing/rival`, excluded from topo-sort). *(the backbone split, §1)*
- **A0.3** Make Open Q7 a **hard render-ceiling assertion** in `compile_global.py`, not a yes/no question: any event whose latent axis lacks a validated meaning instrument renders **below a sharpness ceiling**. *(fixes the §1 latent caveat + part of G2)*

**PHASE 2 (NORMALIZE — schema + adapters):**
- **A2.1** Replace the §2.1 flat event record with the **v0.3 six-axis + WHOM + BEFORE/AFTER/FROM + per-axis `measured_bits`** wrapper. *(fixes G1)*
- **A2.2** Change `bit_unit` to **per-signal columns** (`reasoning_tokens / marker_count / residue_bits / mdl_delta_bits / cost_ub / evidence_lcb`) + a typed accessor that raises on a signal mismatch + a bridge-record requirement for any cross-unit display. *(fixes G6)*
- **A2.3** Route Adapter B (digestion) concept targets through the **canonicalizer** (embedding/NLI canon + codelength residual), not verbatim verified-dissolve; wire `measured_bits = min(cost_ub, evidence_lcb)` extending `cosmic_coin_probe/harness.py`. *(fixes G2)*
- **A2.4** Add `entity_aliases.jsonl` as a **first-class federation artifact**; unresolved aliases are counted visible debt. Map `qm_relativity` by its `specimen` field (never filename stem). Fix Adapter D to **emit new 12-edge records + supersession edges and mark the 10 old `demoted`** (never replace in place — that erases provenance); reconcile/demote the 13-claim headline. *(fixes G4)*
- **A2.5** Add a **`collective` arena** adapter (`C(N)`, DPI floor, BUILD/MAINTAIN/USE clocks). *(fixes G8)*
- **A2.6** Make `dead_children.jsonl` a **reviewed artifact** (regex proposes, cross-model confirms, count carries `extraction_confidence`) so "40" never renders as a crisp machine-counted fact. *(fixes G4c/G11)*

**PHASE 3 (COMPILE):**
- **A3.1** Add the **second COIN inequality** (`rendered_bits(parent) <= Σ measured_bits(children) − bits_discarded`, with spread-of-means + `N_eff`). *(fixes G3)*
- **A3.2** `compile_global.py` **re-derives from source by default**; ingests `*.compiled.json` only on a content-hash match (else fail loud). *(fixes G11)*
- **A3.3** Add a **cycle-segregation + no-cross-contract-aggregate** validity test (rejects lineage cycles and cross-contract joins, alongside the planned invalid-join tests). *(the backbone split, §1)*

**PHASE 4 (RENDER):**
- **A4.1** The CORRECTION-LAYER must also render the **KEYHOLE_BLOCK_UNIVERSE AUDIT CORRECTIONS** (conceal ≠ expose; evidence-monotone-not-credence; gaps-can-streak; valence ≠ EIG) — not only the Solomonoff text. *(fixes G7; see §4 caveat)*
- **A4.2** W_C wrapper classes (`bit_unit=null` by construction) render as an explicit **visible "no measured bits yet" verdict**, never a placeholder zero or a borrowed `classifierWeight`/Pareto number masquerading as a measured bit. *(fixes G6)*

**PHASE 5 (STREAM):**
- **A5.1** Make the **keyhole probe = spreading activation** the explicit query/navigation primitive; add `D(t)` trajectory-identity + anchor-based 4D transport maps as the entity-resolution/versioning layer. *(fixes G9/G10)*
- **A5.2** Move the **`t_event`-honouring verify** out of Phase 5 to-do into a build-time **MUST-FAIL test** ("verify an old `t_event` against a file that did not exist then" must fail). *(fixes G5)*
- **A5.3** Enforce **"never write a generated bit below the measured floor"** as a STREAM-hook invariant; keep the predict-half explicitly 100%-dark. *(fixes G12)*

**NEW Open Question to add:** the USE layer (G9) — is it a Phase-6 concern between RENDER and STREAM, or folded into STREAM's keyhole hook? (One crawler proposes a discrete Phase 6; I lean folding it into STREAM, since the keyhole probe is already STREAM's primitive.)

---

## 4. CAVEAT — where the crawlers conflict with the standing audit (honest flag, not laundered)

Two crawler lenses recommend adopting an **"up-only `measured_bits` lattice"** and treating **"valence = EIG"** / **"the fuzzy region IS argmax-EIG."** The standing audit in [`KEYHOLE_BLOCK_UNIVERSE.md`](KEYHOLE_BLOCK_UNIVERSE.md) (AUDIT CORRECTIONS, lines 11-42) **explicitly demotes both**:
- *Evidence volume* is monotone (CALM, with event-ID dedup); *credence/confidence* is **non-monotonic** and ordered by the bitemporal `tau` clock — retractions are not CALM-safe. So "confidence only goes up" is **wrong**. The K1 merge fork should be adopted as **append-only EVIDENCE separated from non-monotonic DERIVED BELIEF**, not a naive up-only lattice.
- The next-burst objective is **expected utility/cost**, of which EIG is one term; **"valence := EIG" is false** (high uncertainty can be irrelevant, costly, or low-utility). Valence (R3) is the signed sentiment field, a different quantity from unsigned EIG.

I have written the amendments above to the **corrected** form (A4.1 renders these very corrections as a visible layer). Adopting the crawler shorthand verbatim would re-introduce demoted claims — the demote-not-kill discipline forbids it. This is the one place the survey's own recommendations needed correction against disk.

---

*Demote-not-kill throughout: the plan's federate-not-merge spine, append-only discipline, and chassis-reuse are retained. Nothing here is destructive. The single highest-leverage change is the schema one (A2.1 + A2.2): the per-axis, per-signal record is the foundation every other guardrail attaches to.*
