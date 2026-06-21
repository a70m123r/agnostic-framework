# OPUS AUDIT — DRAFT_HARVEST_PLAN.md (adversarial, demote-not-kill)

**Date:** 2026-06-20 · **Auditor:** Opus 4.8 (adversarial) · **Method:** read both docs in full, spot-checked
every load-bearing claim against disk (chassis HTML opened line-by-line; W_C DB, run schemas, gitignore,
fact record, `measured_bits` def, dynamics.jsonl, bitemporal builder all inspected).
**Posture:** sharpen, do not kill. The plan is broadly sound; the failures below are about *enforcement,
commensurability, and one mis-stated chassis estimate*, not direction.

**Cross-reference:** a codex (GPT-5.5, xhigh) audit of this same plan was *launched* (`session_arc/
codex_harvest_plan_audit.stdout.log`) but **never wrote its `.md` deliverable** (file absent) — so this is
the only completed external audit on disk. Treat that as a gap, not a corroboration.

---

## 1. SCHEMA — global `event` record + `bit_unit` block

**VERDICT: overstated** (the partition keys *discourage* invalid joins; they do not make them impossible).

The plan (§0.2) says: "Bake these into the schema so a naive join *cannot* be wrong." That is the
strongest claim in the document and it is false as written. `era`/`signal_type`/`model` are **string
fields on a record**, not constraints. I verified the actual enforcement surface: the existing
`compile_substrate.py` resolves best-values strictly within a `(specimen, subject_id, predicate)`
triple (SUBSTRATE_SPEC §6) — there is **no cross-specimen aggregation primitive at all**, and there is
**no machinery that would reject** `mean(cost) GROUP BY subject_id` over mixed eras. A field cannot
forbid a query; only a compiler/typed-accessor can. The partition keys are *documentation that a join is
illegitimate*, enforced by author discipline — exactly the thing the plan elsewhere (correctly) refuses
to rely on.

**Sharpest concrete flaw:** `bit_unit.cost` is a single `<number|null>` column whose meaning is set by a
*sibling* field (`signal_type`). reasoning_tokens (≈10²–10⁴ token counts), markers (small integer
counts), residue_bits (codelength, ~10²), and mdl_delta_bits (never populated — see §2/§4) all land in
the **same numeric column**. Any consumer that reads `cost` without first branching on `signal_type` —
a viewer tooltip, a Pareto sort, a `_summary` aggregate — silently mixes token-counts with bits. The
schema makes the wrong thing the *easy* thing.

**Fix:** (a) Make `cost` un-poolable by construction: rename to per-signal columns
(`reasoning_tokens`, `marker_count`, `residue_bits`, `mdl_delta_bits`) so there is **no single field to
average across types** — a wrong pool becomes a missing-column error, not a plausible number.
(b) Ship a typed accessor in `compile_global.py` (`get_cost(event)` raises unless caller passes the
matching `signal_type`) and route every view through it. (c) Add a build-time assertion: any
aggregate touching `cost`/Pareto must carry an explicit `partition=(era,signal_type,model)` argument or
the build fails. Enforcement lives in code, never in a field name.

**Un-representable in the corpus?** Two things resist the record:
- **The held-out 15-item organ test set and the κ/P_o/P_e reduction verdict** (FALSIFIER_REPORT.md) are
  *meta-claims about a classifier*, not subject/predicate/value facts. The plan (Adapter D) bolts them on
  as `arena='organ'`/`arena='test_item'` but the κ=0.671 record has no natural `subject_id` and no
  `bit_unit` — it is a statistic about a coding experiment. Representable only by abuse of the `value`
  field (stuff the stats object in). Acceptable, but flag it: this is the record bending, not fitting.
- **Couplings are typed *edges* (signed, with loop/falsifier), not subject facts.** The record models
  edges as `parents:[event_id]` (untyped) plus, presumably, predicate `rel:coupling:target`. The
  12 refined edges carry *sign + endpoints + loop membership + falsifier* — four typed attributes on
  one edge. These will be smeared across `predicate` + `value` + `notes`. Add a first-class
  `edge` sub-object or you lose the control-theory structure the refinement was *for*.

---

## 2. ADAPTERS — find the lossiest mapping + silent drops

**VERDICT: risky** (one adapter is built on a field that does not exist; another silently drops the
richest column).

**Lossiest mapping: Adapter C (W_C wrapper DB).** I opened all 25 rows. The plan says
`bit_unit.cost = mdl_delta_bits if numeric else flag 'prose-only'`. **There is no `mdl_delta_bits` field,
and no numeric bit cost anywhere in the DB.** The "W_C compiled" the plan points at is `netProduct` — and
`netProduct` is **pure prose** ("A W_C composite = the molecular orbital ψ_bond conceived inside the
parents' overlap integral…"). So Adapter C's bit_unit will be `prose-only` for **100% of rows, always**.
The plan's framing ("`netProduct` (the W_C compiled)" in WHERE_WE_ARE §3) implies a compiled numeric
object; it is a sentence. **This means the W_C arena contributes ZERO measured bits to "the one board."**
Every wrapper-class contestant scores `null` on the agnostic unit and is ranked only by
`classifierWeights` (the Pareto axes) — which are **self-assigned, single-agent, unaudited** numbers
(WHERE_WE_ARE 6.7 confirms; I confirmed the values are bare floats with prose justifications).

Also: WHERE_WE_ARE §1 Slice-E states "utility legs are **prose**, not numeric." **Wrong** — I checked:
`utility` is a dict `{"score": 0.92, "isUnifier": "<prose>", ...}` carrying a numeric `score` plus prose
legs. Minor, but it is a factual error in the survey the plan trusts, and it changes the adapter (there
IS a numeric utility score to harvest). The survey under-inspected this slice.

**Silent drop: Adapter B (digestion).** The plan keeps `n_correct/n_total` (good — survivorship) and
"prefers markers." But markers exist **only for NF today** (WHERE_WE_ARE 6.3, confirmed). The plan says
"back-apply the marker re-score to Era-2 where reasoning text is saved — no new API calls." That is the
right instinct, but until that re-score is actually *run and locked*, every non-NF digestion cell falls
back to `reasoning_tokens` flagged `narration-confounded`. The risk: the plan treats marker-coverage as
present-tense ("prefer markers") when it is a **future task gated on a script that hasn't been run across
experiments**. If RENDER ships before that back-application, the board is reasoning_tokens-dominated —
the project's own demoted proxy — wearing the honest "markers" label in the schema's `signal_type` enum.

**Smaller real drops I confirmed:**
- `qm_relativity.*` stem → `quantum-gravity.compiled.json` mis-key: real, will mis-route one specimen
  under a glob-keyed harvester. Plan flags it (Adapter A). Good.
- 8 `overlays/*.overlay.json` are un-harvested and `--ingest-overlays` was specced-not-built — the plan
  defers this to an Open Question. Acceptable but it is *data currently dropped*.
- `l0_wrappers/facts/` staging dupes vs `substrate/facts/`: plan correctly says harvest only the latter.

**Fix:** (a) Rewrite Adapter C honestly: W_C contestants are **`bit_unit=null` by construction**, rendered
**explicitly blurred / "prose-only, unscored on the bit board"** — never a placeholder zero, never a
borrowed Pareto number masquerading as a measured bit. Make "this arena has no measured bits yet" a
*visible verdict*, not a silent null. (b) Gate the `signal_type='markers'` enum value behind the
actual marker re-score: forbid emitting `markers` for any experiment the re-score has not been run+locked
on. (c) Correct the survey's "utility is prose" error and harvest `utility.score`.

---

## 3. FEDERATE vs MERGE

**VERDICT: sound (federate is right) — but the plan under-states what federation defers.**

Federation (keep source-of-truth stores; a global compile unions them into one iterable view) is the
correct call, and for a concrete reason I verified: the existing toolchains
(`compile_substrate.py`, `compile_scope.py`, `recompile_channel.py`, the 5 builders) all already work and
all already run clean. A physical merge into one `global/events/` tree would force a one-time migration
that breaks each of those compilers and throws away the per-store `.gitignore`/disposability discipline
(e.g. `substrate.db` is gitignored and rebuilt; the scale-out story explicitly lifts the *per-store*
schema to Postgres). Merge buys nothing the union-compile doesn't, and costs a migration.

**What it defers (and the plan should name as a standing liability, not a win):** federation defers
**cross-store entity resolution**. The same real entity appears in multiple stores under different ids —
the 12-vs-10 couplings (two naming conventions, never entity-resolved), the W_C `overlaps` that are bare
strings pointing at concepts that also live in `dynamics.jsonl` as creatures, the dead-children with four
colliding numbering schemes. Federation lets you *defer* reconciling these, but the global compile then
either (a) shows the same thing twice, or (b) needs a cross-store identity map — which is exactly the
"hard reconciliation" the plan claims federation lets it skip. **Federation moves the reconciliation
from migration-time to query-time; it does not remove it.**

**What breaks under federation specifically:** the COIN cap is enforced *per existing compiler today*,
and each uses a *different bucket ladder* (the plan acknowledges this in §2.3). Under federation the cap
is only as strong as the **weakest** store's compiler. If `compile_global.py` unions already-compiled
outputs (Phase 1.2 leans toward harvesting `*.compiled.json`), a stale compiled headline (dynamics
`stats.reduction` 6.8:1, SUBSTRATE_REPORT 1029/7) **enters the global view pre-laundered** — already
shaped as a "best value," its staleness invisible. The plan's own rule ("re-derive from source jsonl
where a compiled headline is known stale") is the right patch but it is **per-known-case**; an *unknown*
stale compiled artifact passes through.

**Fix:** (a) `compile_global.py` re-derives from source jsonl **by default**, and ingests a
`*.compiled.json` only when its content-hash matches a fresh recompile (else fail loud). Staleness
becomes a build error, not a silent inheritance. (b) Ship a single cross-store **identity map**
(`entity_aliases.jsonl`) as a first-class federation artifact — the place couplings, overlaps, and DC ids
are reconciled — and treat unresolved aliases as a counted, visible debt, not absence.

---

## 4. THE AGNOSTIC UNIT — is "bits of re-pay / digestion cost" one commensurable unit?

**VERDICT: wrong as stated (one *name*, several incommensurable axes) — but rescuable as an ordinal,
within-frame instrument, which is what the rest of the corpus already says.**

This is the conceptual crux and the plan's framing ("the agnostic UNIT = bits of re-pay/digestion cost…
so ANY event scores on one board") does not survive contact with the four `signal_type`s. I checked the
canonical definitions:

1. **digestion `reasoning_tokens`** — a *token count*, not bits. The project's **own** verdict
   (WHERE_WE_ARE §3, V10c/NF capstone): "model-dependent, noisy, narration-confounded compute proxy."
   Magnitudes "NOT comparable across eras/models" (6.3). This is not bits and not commensurable even
   with *itself* across models.
2. **digestion `markers`** — trial-division marker *counts*. A different physical quantity from tokens
   (the whole point of the re-score was that tokens ≠ work). Also a count, not bits.
3. **V1 `residue_bits`** — genuine codelength under davinci-002. These ARE bits — but under one frozen
   coder, and the plan itself walls them in a "separate table, linked only at experiment level, never
   merged" (6.4). The plan *already concedes these cannot be pooled.*
4. **W_C `mdl_delta_bits`** — **does not exist** (§2 above). The wrapper arena has no bit cost at all.
5. **genealogy** — `signal_type='none'`. Facts carry `certainty`, not bits.

So of five arenas: one is bits-but-walled-off (V1), one is bits-but-empty (W_C), two are counts not bits
(tokens, markers), one has no unit (genealogy). **"One board" is at best two genuinely-bit arenas that
the plan forbids merging.**

The deepest point — and the one that decides it — is in `latent_measurement_candidates.md`, the ratified
home of "THE UNIT." Its own validation status reads: *"verdicts coder-invariant **though absolute bits
move ~88% across coders**."* So **even the canonical latent `measured_bits` is not commensurable as an
absolute magnitude** — only its *ordinal verdicts* (lie blurs, evidence discriminates, redundancy→0) are
stable. The unit is, by its authors' own words, a **pinned *relational* bit** ("relational by necessity;
there is no intrinsic latent measure; honest under a *declared measurement contract*").

That is the rigorous answer: **there is no absolute commensurable unit, and the corpus already knows it.**
What is commensurable is a *frame-relative ordinal*: within a fixed (era, model, coder, signal_type)
contract, "did it dissolve / how much resisted" is a comparable verdict. The plan's headline over-reads
this relational ordinal as an absolute scalar ("score on one board"). That is precisely the
over-claim that the demote-not-kill ledger exists to catch — and the plan would be importing it into the
schema as a *feature*.

**Fix:** Demote "one board" to its honest form: **one *protocol*, many *contracts*; contestants compare
only within a declared contract.** Concretely — `bit_unit` must carry the **measurement contract**
(`{coder, era, model, frame, skepticism_dial}`) as a required sub-object, and the board renders as
**facets keyed by contract**, with cross-facet comparison rendered as a *disabled/blurred* operation
(the COIN seam made literal). The agnostic axis is the **verb** (re-pay/dissolve), measured ordinally;
it is honest as "everything is *scored by the same kind of question*," dishonest as "everything is *on
the same number line*." Rename the vision line accordingly.

---

## 5. SECURITY — secrets-exclusion predicate

**VERDICT: risky** (the predicate is good; the *survey's claim about current protection is wrong*, and
the leak surface is wider than the predicate covers).

I verified the live state and found a discrepancy the plan inherits:
- WHERE_WE_ARE 6.1 says "`.gitignore` lists `.openrouter_key`, `*.key`, `secrets.*`" *(implying a local
  measure/.gitignore)*. **The `measure/.gitignore` is empty/absent.** The actual protection lives in
  `research/pav/.gitignore` lines 44–47, three directory levels up. `git check-ignore` **does** confirm
  the key is ignored via that ancestor file — so the key is NOT committed (good) — but the plan's stated
  *reason* it's safe is mislocated. If anyone trusts "the measure dir gitignores its secrets," they are
  trusting a file that isn't there. A future `git add -f` or a move of the directory out from under that
  ancestor would silently un-protect it.
- The `is_secret(path, head_bytes)` content/name/glob predicate (§0.1) is genuinely good and the
  build-time grep-the-output assertion is the right backstop. I scanned `measure/` for other key-shaped
  content (`sk-or-v1`, `sk-proj-`, `AKIA`, `AIzaSy`, `ghp_`) and found none beyond `.openrouter_key`. So
  the predicate as specified would catch the one known secret.

**What else can leak (the predicate does not cover):**
- **PII / personal data in *content*, not credentials.** I confirmed `world_land.json`-adjacent
  `globe_cone_unified.html` hardcodes a `GEO{}` map with named real people pinned to lat/lon
  (e.g. `aud-willison` at Sydney, `aud-pav` at an Australia centroid). Provenance/`acts.jsonl` and the
  scene files name real individuals and tie them to locations and actions. **The rendered viewer
  geolocates named people.** The secrets predicate (key-shaped) will not flag a name+coordinate. If
  HYPERSPACE.html or the global substrate is ever shared, that is the real disclosure risk, not the API
  key.
- **Local absolute paths as "provenance."** Confirmed: `agnostic_framework.dev.jsonl` and the W_C `refs`
  use `D:/PlatformOperator/research/pav/...` source URLs. These leak the author's filesystem layout and
  directory names into committed JSON and into the viewer's provenance tooltips.
- **Transcript references** (`provenance_refs: "transcript#"` in the STREAM phase) can pull raw
  conversation content into the substrate. The predicate scans for key prefixes, not for whatever a
  transcript line contains.

**Fix:** (a) Correct the survey: state that protection is the **ancestor** `research/pav/.gitignore` and
add a redundant `measure/.gitignore` so the protection is local to the harvest path (defense in depth —
a moved directory stays safe). (b) Extend `is_secret` into `is_excludable` with a **PII/path tier**:
flag records whose `source.url|doc` is a local absolute path (rewrite to repo-relative or redact), and
add a disclosure gate before any *external* share that scans for person-name + coordinate pairs. (c) Keep
the rotation action — and add: rotate is necessary but the bigger exposure is the geolocated-people layer,
which rotation does nothing for.

---

## 6. 4D RENDER FEASIBILITY — is `globe_cone_unified.html` ~70% of the chassis? Is "~250 lines" realistic?

**VERDICT: overstated** (I opened the file in full — it is real and impressive, but it is ~70% of a
*different* viewer than the SPEC describes, and "~250 lines" is optimistic by a multiple).

I read all 614 lines. What the chassis **has** (genuinely reusable, ~70% of *a* viewer):
- An orthographic 3D camera (no perspective divide → "one log2 bit = one fixed pixel") — exactly the
  honesty property the SPEC wants. ✓
- A log2 double-cone scale ladder (Planck→horizon), real anchors. ✓
- A globe-in-log morph (`z∈[0,1]`: globe fills stage → shrinks to Earth's cone dot), with land rings,
  graticule, limb-clipping, slerp. ✓ This is the hardest graphics already done.
- A time scrubber with fisheye zoom down to 1h, frame-glasses (T/S/K/M salience dials), MUTATE badging,
  a substrate-bound narrator. ✓ The honesty-badge discipline is already wired.

What the chassis **does NOT have** — i.e. what Phase 4's "~250 lines" must actually build:
1. **The Mercator/Daners conformal dial — the SPEC's *keystone* — is entirely absent.** There is no
   `surfacePoint(lat,lon,d)`, no `v = ln(tan(π/4+φ/2))`, no `n=cos(d·π/2)` morph, no 3D↔2D-flat tween.
   The globe here morphs *toward a cone dot* (`smooth01(z)`), not *toward a flat Mercator map*. The
   keystone increment the SPEC calls "the spine" (`surfacePoint` + route all draws through it +
   pole-clamp + the `d` slider) is **0% present**. This is the conceptually load-bearing piece and it is
   not 70% done — it is not started.
2. **Substrate ingestion is non-existent.** The chassis is **hardwired to the Fable-takedown scene**: a
   9-element `OBJ[]` array literally typed into the source, a ~24-entry `GEO{}` map of hardcoded
   lat/lon/pins, and `fetch("../scene/fable_takedown.scene.json")`. There is **no path that ingests a
   `compiled/*.json` of arbitrary events.** Phase 4 needs a `build_hyperspace.py` (jsonl→inject) AND a
   generic renderer loop that consumes N events of M arenas — replacing the bespoke scene logic. That is
   not in the 70%.
3. **Bitemporal is partial.** Good news, partly verified: `BITEMPORAL_3D.html`/`build_bitemporal.py`
   *already* separate `t_event` and `t_obs` (threads rising to render-height at t_obs). But that is a
   **different file**; the globe_cone chassis has a single `now` scrubber, not the two-timeline block.
   Merging the bitemporal thread logic into the globe chassis is real work, not a line-count rounding
   error.
4. **The latent membrane** (hyperbolic Poincaré tanh reach) is absent; the chassis has a flat "latent
   stratum" dome at a fixed Y-lift, not a hyperbolic radial membrane.
5. `FIG-1..8` do not exist (confirmed).

**Is "~250 lines" realistic?** No. A defensible estimate: the conformal dial + generic substrate
ingestion + the latent membrane + folding in bitemporal threads + the 3-channel MEASURED/ESTIMATE/
MODELLED router is closer to **600–1000 new/refactored lines**, and crucially it requires *rewiring* the
hardcoded scene path (deletion + generalization), which the "add ~250 lines" framing hides. The honest
statement: the chassis gives ~70% of the *camera/cone/globe/scrubber/badging* machinery, and ~0% of the
*keystone dial* and *substrate ingestion* — which are the two things that make it "the hyperspace viewer"
rather than "the Fable toy."

**Fix:** Re-scope Phase 4 into two increments matching the SPEC's own "Increment 1 = the spine":
(4a) generalize ingestion — replace `OBJ[]`/`GEO{}`/scene fetch with `build_hyperspace.py` feeding a
generic event loop, rendering the *existing* cone+globe (proves the pipeline on real data, low risk);
(4b) add `surfacePoint(d)` Daners dial + latent membrane + bitemporal threads. Budget 4b at
~500–800 lines and treat it as the actual headline build, not a garnish. Drop the "~250 lines" number
from the plan — it will set a false expectation and pressure a corner-cut on the keystone.

---

## 7. COIN HONESTY — does render ≤ measured bits hold end-to-end?

**VERDICT: risky** (the *law* is correctly stated and the cap is real per-compiler; three concrete paths
let a fake/overstated bit through, and the plan patches only one).

The render invariant (`rendered_sharpness ≤ measured_bits`, "blur is the badge") is genuinely wired into
the chassis (MUTATE badges, EWA floor, "never render a fake measured bit" in code comments) and into each
existing compiler's bucket cap. The leaks:

1. **Stale compiled artifacts (the biggest hole).** Confirmed live: dynamics `stats.reduction` still
   asserts the *pre-falsifier* "6.8:1 / ~6 organs" headline, contradicted by FALSIFIER_REPORT
   (κ=0.671, 5 organs); SUBSTRATE_REPORT is stale (1029/7 vs live 1372/10). Phase 1.2 leans toward
   harvesting `*.compiled.json`. A stale compiled value enters the global view **already shaped as a
   best-value with a high bucket** — its overstatement is invisible because the staleness lives in the
   gap between source jsonl and the compiled snapshot. The plan patches *known* stale cases by name; an
   unknown one passes. (See §3 fix: re-derive by default, hash-gate compiled inputs.)
2. **Prose-scraped tallies.** Adapter E regex-scrapes "DC-NN" lines and the prose "40 dead-children"
   tally into `dead_children.jsonl`, "machine-counted for the first time." But the *input* is prose with
   four colliding numbering schemes (DC- / arc- / organ- / cosmic-). A regex over inconsistent prose
   will mis-count (double-count a DC that's also an arc-demotion; miss a cosmic "six" phrased as words).
   The resulting count will be *presented as machine-counted* (high trust) while being **scrape-fragile**
   (low actual reliability) — a confidence/accuracy mismatch, which is itself a COIN violation (rendering
   a derived number crisper than its evidence supports).
3. **Single-agent-unaudited Olympics scores.** Confirmed: the 25 W_C `classifierWeights` are bare
   self-assigned floats, single-agent, never cross-model-passed (WHERE_WE_ARE 6.7). The plan flags them
   `single-agent-unaudited` (good) — but they are the **only** numeric axis the W_C arena has (since
   bit_unit is empty, §2/§4). So on "the board," wrapper classes are ranked **entirely** by unaudited
   numbers wearing a Pareto label. The flag exists; whether the *render* actually blurs them to match the
   flag is unverified and must be enforced, not assumed.
4. **The SPEC keystone over-claim travels into the render.** Confirmed: `SPEC.md` line 13 still reads
   "render sharpness (Solomonoff/MDL: appearance = 2^−bits)" — the exact Solomonoff=2^−bits identity the
   cosmic-coin note + external pass DEMOTED to standard MDL/log-loss shared-bit-currency (lzma ≠
   universal mixture). The plan's Phase 4 *does* say "CORRECTION-LAYER FIRST: fix the SPEC keystone text"
   — credit where due. But the demotion is not yet applied to the live spec, and if RENDER is built from
   the current SPEC text the over-claim is rendered as the headline thesis.

**Fix:** (a) Re-derive-by-default + hash-gate compiled inputs (§3). (b) Make `dead_children.jsonl` a
**reviewed** artifact: regex-scrape proposes, a human/cross-model pass confirms, and the record carries
`extraction_confidence` so the count renders with appropriate blur — never "40, machine-counted" as a
crisp fact. (c) Add a render test: any event with a `single-agent-unaudited` or `prose-only` flag MUST
render below a hard sharpness ceiling; assert it in `compile_global.py`. (d) Apply the
Solomonoff→MDL demotion to `SPEC.md` *before* Phase 4 reads it (the plan says this — elevate it from a
Phase-4 step to a Phase-0 guardrail, since the spec is the render's source of truth).

---

## 8. SEQUENCING / BIGGEST RISK / WHAT'S MISSING

**VERDICT: phase order mostly sound; one inversion; one missing phase.**

**Phase order:** HARVEST→NORMALIZE→COMPILE→RENDER→STREAM is right, and Phase 0 (secrets + partition keys
+ reuse decision) correctly precedes everything. **One inversion:** the SPEC-keystone correction
(Solomonoff→MDL) is filed under Phase 4; it must move to **Phase 0**, because SPEC.md is the render's
contract and the demotion is load-bearing on the central thesis. Correcting it last means building on a
known-wrong keystone.

**Single highest-risk part: Phase 4 (the 4D render), for the reasons in §6** — it is the only
green-field build, its keystone (the conformal dial) is 0% done not 70%, the line estimate is off by a
multiple, and it requires *deleting* the chassis's hardwired scene path before it can ingest the
substrate. Everything upstream is "adopt existing formats" (genuinely lower risk, as the plan says);
Phase 4 is where the project can stall. **Second-highest:** Adapter C / the agnostic-unit framing (§2,
§4) — because if "one board" ships as an absolute number line, it imports the exact over-claim class the
whole project's honesty discipline exists to prevent.

**What is MISSING from the plan entirely:**
1. **An idempotency / re-run contract for the STREAM keyhole.** Phase 5 appends event records on every
   action and triggers `compile_global.py` "(idempotent)". But append-on-action + re-compile has no
   stated **dedup key** (what stops the same commit appended twice?), no **ordering guarantee** under
   concurrent agents (the council is multi-agent), and no **back-pressure** (a 20MB hang is in living
   memory — "the big one"). The streaming half is sketched as one bullet; it is the part that runs
   forever and the part most likely to corrupt the substrate. Needs its own mini-spec: event dedup key,
   append-only WAL discipline, compile debounce, and a size/row ceiling with a graceful-degrade.
2. **A verification/falsification budget for the NEW infrastructure itself.** The corpus's whole
   credibility rests on cross-model external passes and a dead-children ledger. The *harvest code* —
   `compile_global.py`, the 5 adapters, the dead_children scraper — gets none of that discipline in the
   plan. There is no "run the global compile, then cross-model-audit its `_summary` against the source
   docs" gate. The plan applies the project's honesty standard to the *data* but exempts the *tooling
   that reshapes the data* — the single place a silent transform error would poison everything
   downstream. Add a Phase-3.5: lock the global `_summary`, cross-model re-derive 3–5 headline numbers
   from source, before any render trusts it.
3. **A rollback / provenance-of-the-harvest-itself record.** The harvest is non-destructive (good) but
   produces a new `global/` tree that becomes load-bearing. There is no stated way to answer "which
   harvest run produced this event, under which adapter version, and how do I reproduce it" — i.e. the
   harvest needs the same `lock_sha` discipline it imposes on the science. (The `harvest_manifest.jsonl`
   is close, but it inventories *sources*, not *runs*.)

---

## Bottom line

The plan is the right shape — federate, reuse the substrate envelope, carry demotions as first-class
records, build the one missing viewer on the existing chassis — and most of it is honest adoption of
working formats. Its failures are concentrated and fixable: (1) partition keys are documentation
masquerading as constraints; (2) the agnostic "one board" over-reads a frame-relative ordinal as an
absolute number line, and one of its five arenas (W_C) has no measured bits at all; (3) the Phase-4
chassis estimate ("~70% / ~250 lines") is true for the cone/globe but false for the keystone dial and
substrate ingestion, which are ~0% done. Fix enforcement-in-code, demote "one board" to "one protocol /
many contracts," re-scope Phase 4 honestly, and add the missing streaming-idempotency + tooling-audit
guardrails — then execute.
