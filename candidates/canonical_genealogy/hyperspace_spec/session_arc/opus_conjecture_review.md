# OPUS REVIEW — the two-halves instrument (measured gather + weighted-conjecture sim)

**Date:** 2026-06-21 · **Auditor:** Opus 4.8 (adversarial external pass) · **Posture:** demote-not-kill.
**Method:** read `REVIEW_BRIEF_CONJECTURE_INSTRUMENT.md`, `GAPS_AND_BACKBONE.md`, `DRAFT_HARVEST_PLAN.md`
in full; ground-checked against `WRAPPER_PROBE_OBSERVER.md` (the v0.3 record source), `K3_observation_to_knowledge.md`
(the conjecture-stub machinery), `K1_block_universe.md` §4.3 (the aggregation COIN), `CANONICALIZER.md`,
`latent_measurement_candidates.md` (the 88%-coder-move fact), and the prior `opus_harvest_plan_audit.md`
+ `gemini_conjecture_review.md` (the parallel pass, to stay complementary not redundant).

**The one finding that frames all five answers (read first):** the brief asks "what scores and prunes the
conjecture fan (the X*n → emergent-reading mechanism)?" and treats the generative half as deferred/dark.
**But that mechanism is already specified on disk, in depth, in `K3_observation_to_knowledge.md` — and the
brief does not cite it.** K3 §2 gives the conjecture-stub as a *first-class typed object* (Skolem term,
three-way `fuzz_type`, ATMS assumption-set, EIG-per-cost, dead-children lifecycle, min-clamp render); §2.4
names and closes the three hardening leaks (Woozle / Resurrection / Laundering) *by construction*; §3 gives
the active-aiming scorer. Meanwhile `GAPS_AND_BACKBONE.md` G12 calls the predict-half "100% dark / unbuilt"
and the brief's v0.3 record reduces the stub to a flat `conjectures[]: [{reading, weight, tag, basis,
followups[]}]`. **The brief is re-opening, in a weaker form, a design K3 already closed.** Most of what
follows is: adopt K3's stub as the home of the generative half; the brief's flat `conjectures[]` is a
lossy projection of it and should be demoted to "the render-time view of a K3 stub," not the schema.

---

## Q1 — The two-halves framing (measured gather + multi-weighted-conjecture sim, COIN-separated)

**VERDICT: sound in principle, RISKY as written** — the dichotomy is right and is the honest spine of the
whole instrument; but the brief's *governance* of the fan ("the X*n → emergent canonical reading mechanism
is the scoring layer") is an undefined promissory note, and the words "emergent canonical reading" name a
COIN violation.

**Why the framing is sound.** "Gather measured + simulate gaps, kept visibly distinct by the COIN, with a
what-is-it tag" is not a new risk surface — it is the *existing* honesty spine (`SPEC` sec 7's three
additive channels MEASURED/ESTIMATE/MODELLED; K3's negative-space grammar where a stub is a *void*, a fact
is a *filled splat*). The two-halves design does not *introduce* laundering risk; it *names a half that
already had to exist* (the COIN's "never render a fake measured bit" is meaningless unless there is a
"generated bit" category to forbid). So lighting the generative half is not a new danger in kind — it is
making an already-implied category explicit, which is *safer* than leaving conjecture to leak in unlabelled.

**The sharpest concrete flaw — "emergent canonical reading" is the forbidden move.** Rendering *n* conjectures
and reading off "an emergent canonical reading" is **exactly the aggregation the second COIN forbids**.
`K1_block_universe.md` §4.3 (lines 164–168): `rendered_bits(parent) <= Σ_children measured_bits −
bits_discarded`, where `bits_discarded` MUST include a **spread-of-means term** "so a high-variance child
set cannot aggregate to a sharp centroid (a broadcaster + audience averaged into one point is the canonical
fake bit)." A fan of 5 mutually-exclusive conjectures is *maximum spread*. Collapsing it to one "canonical"
reading manufactures a crisp bit from pure disagreement — the same fake-bit the broadcaster+audience case
forbids. The honest output of an unresolved fan is **the fan, rendered as a fan** (K3 §2.3 rule 1: a stub
is a ring with a void; the candidate latch-points are ghost-forks, *not* a winner). "Emergent canonical
reading" should be **demoted**: there is no canonical reading until a followup *closes* the stub (Q4); until
then the fan IS the answer, and its weights are an internal RAG voting prior (Gemini's point 3 is right
here) that **never touches render sharpness**.

**What governs how many conjectures + how they are scored/pruned — already answered by K3, not the brief.**
The brief leaves this open; K3 closes it:
- **How many:** not "X*n free generation." K3 §2.1's `candidates: [{H_i, prior, falsifier_i}]` requires
  **each candidate to carry its own falsifier** — a conjecture with no falsifier "is not a stub, it is a
  note/prior" (§2.3 rule 3). That is the natural cap: you may only post as many conjectures as you can post
  *distinct falsifiers* for. No falsifier → not admitted. This is a far stronger governor than a TTL/decay
  count (Gemini's fix), because it prunes *at admission* on a content criterion, not after N steps on a clock.
- **How scored:** K3 §3 — `EIG(P)/cost(P)` against an **explicit compiled posterior, NOT chat/probe history**
  (the BED-LLM warning, §3 refinement (a)) — which is *precisely* Gemini's "don't let the sim eat its own
  tail," but specified two weeks earlier and bound to the substrate.
- **How pruned:** K3 §2.5 — a conjecture that fails its probe becomes a **dead child** (counted, dated,
  append-only), the stub-parent survives with friction +1; under heavy/critical pressure (`>=3` dead probes,
  0 live) the stub is **re-typed to `noise_floor`** ("we fired enough keyholes; the bits are not there").
  That is the prune, and it is auditable.

**FIX (Q1):** (1) Strike "emergent canonical reading" from the directive; replace with "the fan renders as a
fan until a followup closes it; weights are an internal prior, never a render-sharpness input." (2) Re-bind
the brief's `conjectures[]` to the K3 stub: **a conjecture is admissible only if it carries a falsifier and a
`fuzz_type`**; that, not a count, is the fan governor. (3) State the X*n note for what it honestly is — *not a
mechanism but a placeholder for the K3 active-aiming loop* — and cite K3 so the work is not re-derived weaker.

---

## Q2 — The per-axis v0.3 record as the home of BOTH halves

**VERDICT: sound for the measured half, OVERSTATED for the generative half** — per-axis `measured_bits` is
genuinely the right home for the gather half (G1 is load-bearing and correct); but "the same per-axis record
is the home of the conjecture fan" is overstated, because (a) the flat `conjectures[]` is lossy vs the K3
stub, and (b) two of the seven axes are not node-local properties at all.

**The measured half fits cleanly — this part is right and load-bearing.** `WRAPPER_PROBE_OBSERVER.md` §1.3 is
unambiguous: each axis carries its own `measured_bits`; "a wrapper's overall sharpness is per-axis, never a
single scalar"; WHY is "blurriest by construction," WHO carries the Stigler cap. The flat single-`cost` record
in `DRAFT_HARVEST_PLAN.md` §2.1 genuinely cannot express "sharp on WHERE, blurry on WHY," and the second COIN
(K1 §4.3) and the differential 4D render both need per-axis bits. Endorsed without reservation.

**Misfit 1 (the structural one) — WHY and HOW are edges, not node-local axes.** This is the parallel pass's
strongest catch (Gemini Q2) and it is correct and grounded: the backbone IS a DAG (`GAPS_AND_BACKBONE.md` §1),
and WHY/HOW are *relationships between events* ("the commit happened because the bug was filed" → a directed
edge to another node), not scalars local to one record. The prior opus harvest audit found the *same shape* of
defect from the other side: couplings are "typed edges (signed, with loop/falsifier), not subject facts … add
a first-class `edge` sub-object or you lose the control-theory structure." So the corpus already knows edges
resist node-local flattening. **A WHY-axis `measured_bits` is ill-typed: you cannot measure "0.4 bits of why"
on a node; you measure the confidence of a *causal edge* to a parent.** The per-axis record can hold a WHY
*pointer* + the edge's confidence, but the bits live on the edge, not the node.

**Misfit 2 — the cases with no clean WHO/WHY, which the corpus contains in quantity.** The brief asks for "an
event with no clean WHO/WHY." The corpus has whole arenas of them:
- **The κ=0.671 reduction verdict / the 15-item held-out organ test** (`FALSIFIER_REPORT.md`): a *statistic
  about a classifier*. No subject_id, no WHO, no WHY, no `bit_unit` — the prior opus audit already flagged
  this as "the record bending, not fitting." It is a meta-claim, and a per-*content*-axis decomposition has
  nowhere to put it.
- **Authorless / multi-yolk origins** (`WRAPPER_PROBE_OBSERVER.md` §2, §5): "democracy" has *no* clean WHO —
  its origin is "a fuzzy multi-beat spike on an *agreed* (intersubjective) record," explicitly **not a
  yolk-point**. The WHO axis here is not low-bit, it is *categorically* a consensus class, a different
  provenance type. A single `measured_bits` scalar on WHO cannot distinguish "we measured WHO to low
  resolution" from "WHO is intersubjective-by-nature." (K3 §2.2's `fuzz_type` *can* — `evidence_bound` vs a
  would-be `consensus`/`noise_floor` — which is another argument for the stub over the flat field.)
- **Relational/symmetric facts** (a coupling, an `overlaps` edge, a `rival_coupling`): subject–predicate–value
  with a *symmetric* predicate has no asymmetric WHO/WHAT split; forcing it into agent/patient invents a
  direction the data does not carry.

**Misfit 3 — the flat `conjectures[]` is a lossy projection of the K3 stub.** The brief's
`{reading, weight, tag, basis, followups[]}` drops the four things K3 §2.1 makes load-bearing: `fuzz_type`
(noise_floor | compute_bound | evidence_bound — *why* the gap exists, which decides whether a probe can ever
fill it), the per-candidate **falsifier** (without which it is a note not a stub), the **ATMS assumption-set**
label (which makes conjecture-bits count *zero* and makes retraction auto-propagate — the demote-not-kill
machinery for free), and the **EIG/cost** (the aim). The flat record can render a fan but cannot *govern* one.

**Is WHOM-as-observer the right place for the contract? — Yes, but it must be a list, not a scalar.** Putting
`{coder, era, model, frame, skepticism_dial}` at WHOM is consistent with `WRAPPER_PROBE_OBSERVER.md` §3.4
(GLASSES = observer = the decoder `q`) and with the prior audit's conclusion that the unit is a *pinned
relational bit* needing its contract. **But one event has many observers with different contracts**
(a rival's mind-sandbox of Musk vs a fan's — §4 of the same doc makes the observer-relativity explicit, with
valence sign R3). So WHOM must be an **array of contracts**, each carrying its own per-axis confidence, not a
single contract slot. (Gemini reached the same conclusion; it is grounded in §4.)

**FIX (Q2):** (1) Keep per-axis `measured_bits` for the four **intrinsic** axes WHO/WHAT/WHERE/WHEN. (2) Make
WHY/HOW **typed edges** with confidence on the edge, not node-local axes (binds the DAG split in
`GAPS_AND_BACKBONE.md` A0.2). (3) Replace the flat `conjectures[]` with **a reference to a K3 stub** (the stub
is the object; `conjectures[]` is its render-time view). (4) WHOM = **array of `{contract, per-axis-confidence}`**.
(5) Add an explicit **`arena='meta_claim'` escape** for classifier-statistics (κ, test sets) that the
per-content-axis decomposition cannot hold — render them as their own node type, never bent into `value`.

---

## Q3 — Confidence weights: one commensurable thing, or four scalars wearing one name?

**VERDICT: WRONG to treat them as one (they are at least four incommensurable quantities) — but the corpus
already knows this, in two places, so the fix is adoption not invention.**

The four scalars the brief lists — `measured_bits`, per-axis `confidence`, conjecture `weight`, contract
validity — are categorically different, and the corpus has *already ruled* on two of the four pairwise
non-commensurabilities:

1. **`measured_bits` is not even commensurable with itself across coders.** `latent_measurement_candidates.md`
   (the ratified home of THE UNIT): verdicts are coder-invariant **but absolute bits move ~88% across coders**.
   The unit is a *pinned relational bit* — "relational by necessity; there is no intrinsic latent measure;
   honest only under a declared measurement contract." So `measured_bits` is an **ordinal-within-contract**
   quantity, not a magnitude. The prior opus harvest audit reached the identical verdict ("one *name*, several
   incommensurable axes … rescuable as an ordinal, within-frame instrument").

2. **Structure-confidence and corroboration-confidence are *orthogonal axes* that K3 forbids averaging.**
   `K3_observation_to_knowledge.md` §1.4: tau1 (structure, EDL/kink) and tau2 (corroboration, independent
   routes) "are genuinely orthogonal axes … they can disagree … render the disagreement as two distinct
   badges, **never average them into one 'confidence.'**" So what the brief calls "per-axis confidence" is
   *itself* already at least two non-summable scalars (structure-bits and corroboration-bits), plus K3 §1.2's
   third ceiling **reach_bits** (Epiplexity / compute-reach). The render takes the **min** of the three
   (`sigma = max(EWA_floor, k·2^(−min(struct, reach, corrob)))`), *not* a product or a mean. **Min, not blend,
   is the composition rule the corpus already commits to.**

3. **Conjecture `weight` is a normalized intra-fan prior (Σ=1), a different type entirely** — it is the
   generative half's internal voting distribution. It must **never** dictate render sharpness (a low-bit,
   high-weight conjecture is the canonical laundered bit). K3 enforces this by geometry: a conjecture has
   `corrob_bits = log2(1+0) = 0`, so the min-clamp pins it to `EWA_floor` *regardless of its weight* (§1.3:
   "a conjecture … clamps to EWA_floor → maximally blurred → cannot render as crisp as knowledge … enforced
   by geometry"). The weight changes *which ghost-fork is drawn boldest*, never how sharp the region is.

4. **Contract validity is an ordinal frame-distance, not a confidence at all** — it is a *gate* (is cross-contract
   comparison even legal?), rendered as the blurred/disabled COIN seam, not a number that composes.

**The honest composition rule (already latent in the corpus, here made explicit):**
- **WITHIN an axis, across the three bit-ceilings:** compose by **MIN** (K3 §1.3). Sharpness clamps to the
  scarcest of struct/reach/corrob bits.
- **ACROSS axes:** **do NOT compose to a node scalar at all.** The whole point of G1 is that overall sharpness
  is per-axis. A node has a *vector* of (axis → min-ceiling), never a scalar.
- **Conjecture weight:** quarantined to the RAG/voting layer; **categorically barred** from the sharpness
  computation (Gemini's "categorical type system for uncertainty" — correct, and K3's min-clamp already
  implements the bar).
- **Contract validity:** a **predicate gate** on whether the bits may render *unblurred*, applied before the
  min; cross-contract → forced blur. Never a multiplicand.

So: **four scalars, three composition laws (min within-axis, vector across-axis, gate for contract), and a
hard quarantine for conjecture weight.** The danger the brief must avoid is the single "blur number" that
multiplies bits × confidence × weight × validity — which would, in Gemini's phrase, "launder a low-information,
high-confidence guess as sharp." The corpus's existing min-clamp is the antidote; the brief should cite it
rather than leave composition unspecified.

**FIX (Q3):** Adopt K3 §1.3 min-clamp as THE composition rule and name the three laws above in the schema doc.
Forbid any field that is `bits × confidence`. Carry struct/reach/corrob as **three named sub-fields**, never a
collapsed `confidence` scalar (K3 already says: render the tau1/tau2 disagreement as two badges).

---

## Q4 — Follow-ups / deeper research as first-class (generation, tracking, closing, re-scoring)

**VERDICT: RISKY as a free-text `followups[]`; SOUND if bound to the K3 lifecycle + made executable.**

**The flaw the brief's `followups[]: [...]` invites — an unsearchable graveyard of NL strings.** Gemini's Q4 is
right and concrete: `"check if Pav reviewed the doc Tuesday"` cannot close a loop computationally; the fan stays
open forever and bloats the index. But the corpus already has the closure machinery the brief's flat field
lacks — the brief just doesn't wire to it:

- **Generation:** a followup is K3 §2.1's `discharge_evidence: <what probe/source/compute would close it>` +
  `latch_spec.candidates[].falsifier_i`. It is generated *with* the conjecture, as its discharge obligation —
  not bolted on. A conjecture with no dischargeable followup is, by §2.3 rule 3, **not admitted**.
- **Tracking:** K3 §2.5 binds the stub 1:1 to the ratified CLAIM_LIFECYCLE: stub = parent-fn (durable hole),
  probe = child-fn (disposable). Each stub carries `friction_tally {dead_children[], dead_count, live_count,
  best_result_so_far, revisit_trigger, pressure_reading}`. That IS the tracking ledger; it already exists in
  the dead-children discipline this project runs on.
- **Closing (the keyhole loop):** K3 §3 step 6 — a burst arrives as an **append-only** fact (never mutate the
  past; only raise `measured_bits` about a fixed past), recompile, run **AnalyzeImpact cascade over the
  typed-edge DAG** to re-evaluate every downstream node. On success the stub closes: status `corroborated`,
  the Skolem term **binds to a real value**, the dashed ghost renders as a solid splat — *up to the kink only*
  (never to certainty; corroboration is monotone-not-Boolean).
- **Re-scoring the fan on closure:** this is the one place the brief, Gemini, AND K3 each say slightly
  different things, and **the corpus's standing audit settles it against all three.** Gemini says the winning
  conjecture goes to `weight=1.0` and you "delete Conjectures A and C." **That deletion is wrong here** — it
  violates demote-not-kill. `GAPS_AND_BACKBONE.md` §4 caveat is explicit: evidence volume is monotone but
  **credence/confidence is non-monotonic**, retractions are not CALM-safe, "confidence only goes up is wrong";
  and the K1 fork separates **append-only EVIDENCE** from **non-monotonic DERIVED BELIEF**. So on closure: the
  losing conjectures are **demoted to dead-children (counted, dated, retained)**, not deleted; the winner binds;
  and the *re-score* is a recompute of the derived-belief layer over an unchanged evidence log. Deletion would
  erase the falsification record that is this project's honesty gauge.

**The harder, unsolved part the brief should own (not in K3, not in Gemini):** an executable followup predicate
*against a live, drifting substrate* has a presentism hazard. K3 §2.3 rule 2 (NEVER-INTERPOLATE) and the
bitemporal `t_event` gap (`GAPS_AND_BACKBONE.md` G5: `verify.jsonl` has **no `t_event` field**, checks past
acts against *current* disk) together mean a followup that fires *later* can falsely corroborate an *earlier*
`t_event` — "the block sharpens itself with bits it did not have at `t_event`." So an executable followup MUST
carry an **as-of clock**: it may only close a stub with evidence whose `t_obs` post-dates the stub *and* whose
`t_event` is in the stub's claimed window. This is the G5 must-fail build-time test, lifted to the conjecture
loop. Without it, the generative half's *own closure mechanism* becomes a laundering channel.

**FIX (Q4):** (1) `followups[]` are **executable predicates** (Gemini's `EXPECT_EVENT(...)` / a Cypher or
regex watcher on the keyhole stream), never NL — bind to K3 §2.1 `discharge_evidence`. (2) Closure = K3 §3
step-6 append-only + AnalyzeImpact cascade; **losers demote to dead-children, never delete** (corrects Gemini
against `GAPS_AND_BACKBONE.md` §4). (3) Every followup carries an **as-of `t_event` guard** (binds G5); a
followup that would close a stub with anachronistic evidence MUST fail the build.

---

## Q5 — The biggest RISK of lighting the generative half, and the single most important guardrail

**THE BIGGEST RISK: the conjecture fan re-entering the substrate as ground truth — laundering by self-citation,
two ways.** The parallel pass named the RAG-tail-eating path (an LLM retrieves conjectured text, strips the
metadata because tokens carry no provenance, builds on it as fact). That is real and K3 §2.4 already names it
("Laundering: an adjacent real fact is bound to a stub it does not actually support"; "Woozle: a stub
repeatedly cited becomes load-bearing"). But there is a **second, subtler path the brief's own language opens
that Gemini did not flag**: the **"emergent canonical reading" itself is a laundering operation**. Reading a
single canonical answer off a fan of conjectures *manufactures* a crisp derived bit from disagreement (Q1) —
and once that "canonical reading" is written to the substrate, it is indistinguishable from a measured value
on the next read. The most dangerous launderer is not the RAG retrieving a tagged conjecture; it is the
*aggregator* that the directive blesses, which produces an *untagged* consensus the COIN never sanctioned.
Both paths share one root: **a generated bit acquiring the render-grammar of a measured one.**

**THE SINGLE MOST IMPORTANT GUARDRAIL (one, as asked): the K3 min-clamp as a compile-time invariant, enforced
in code before the generative half ships — `rendered_sigma = max(EWA_floor, k·2^(−min(struct, reach, corrob)))`
with `corrob_bits(conjecture) ≡ 0` by construction.** This is the guardrail because it is the only one that is
**geometric, not policed** (K3 §1.3, §4): a conjecture has zero corroboration bits, so the min pins it to the
blur floor *no matter what its weight, confidence, or in-degree says*. Hardening becomes impossible by
construction, not by discipline — which matters precisely because the council is multi-agent and author
discipline is the thing this project repeatedly refuses to trust. Concretely, before lighting the generative
half, ship in `compile_global.py`:
1. **`measured_bits` is summed ONLY over reconstruction-verified evidence leaves; conjecture assumptions count
   ZERO** (K3 §2.4) — so cite-edges and resurrection cannot import bits (closes Woozle + Resurrection).
2. **The min-clamp render law as a build-time assertion** — any event whose render exceeds
   `min(struct, reach, corrob)` fails the build (closes the aggregator/"emergent reading" path: a fan cannot
   render crisp because its corrob is 0).
3. **Negative-space grammar is mandatory** — a conjecture renders as a *void with ghost-forks*, a render
   grammar disjoint from a fact's filled splat (K3 §2.3 rule 1); the renderer is forbidden the splat grammar
   for any `tag != measured`.

Gemini's "dual-RAG / bifurcated context payload" (block conjectured payload from fact-generation, restrict it
to UI exploration) is a **good complementary** guardrail at the RAG boundary — but it is *policed by a system
prompt*, which is weaker than geometry. If only one guardrail ships first, it must be the min-clamp invariant,
because it cannot be prompt-injected around. The dual-RAG bifurcation should ship as the **second** layer.

**Honest demotion, not kill:** the two-halves design is the right instrument and lighting the generative half
is the correct next move — the gather half is *less* honest without an explicit, COIN-clamped place to put
conjecture (today it leaks in unlabelled). The single change that turns the directive from risky to sound is
to **stop calling the output an "emergent canonical reading" and start calling it a fan clamped to the blur
floor until a followup closes it** — and to wire to the K3 stub that already specifies the whole loop, rather
than re-deriving it as a flat field.

---

## SPECULATION (disclosed — register shift; out-of-box, offered as latch-points, each killable)

- **[SPEC] The fan needs a "live-substrate observer-effect" discount that even K3 only flags as open.** K3 §5
  [SPEC] raises it: firing a probe at "who founded X" is *causal* in a live social substrate — naming a
  candidate feeds the concept's own spread. The council is a live social substrate (agents read each other's
  conjectures). So a conjecture's followup, when fired, may *create* its own corroboration. The independence
  count must exclude **instrument-surfaced instances** (a `FROM`-link tagging self-induced corroboration,
  K3 §5). Without it, the generative half's confidence is partly self-fulfilling — the deepest laundering of all.
- **[SPEC] A `consensus`/intersubjective `fuzz_type` is missing from K3's three.** K3 has noise_floor /
  compute_bound / evidence_bound. But `WRAPPER_PROBE_OBSERVER.md` §2 demands a fourth: WHO-of-an-authorless-idea
  is fuzzy *because it is intersubjective by nature* (a "fuzzy spike on an agreed record"), not because evidence
  is missing or compute is short. Probing harder will never sharpen it past the social-consensus grade. This may
  deserve a fourth terminal type, distinct from noise_floor (it has structure) and evidence_bound (no probe fills
  it). Open whether it is a real type or `evidence_bound` with a `provenance_class=consensus` cap.
- **[SPEC] "Emergent canonical reading" might be salvageable as a *render mode*, not a substrate write.** If the
  fan's weighted centroid is only ever computed *at render time for a specific WHOM's glasses* and never written
  back, it is a legitimate observer-relative summary (the keyhole's presentist projection, badged), not a
  laundered bit. The line is: a canonical reading is honest **as a transient view, dishonest as a stored node.**

## QUESTIONS WE SHOULD BE ASKING (register shift — meditations, not tasks)

- **Is the generative half even "the other half," or is it the same half read at a different rung?** K3 §0
  frames OBSERVATION→MEANING→KNOWLEDGE as the COIN read *vertically*; a conjecture is just the bottom rung
  (corrob_bits=0). On this reading there are not two halves (measured vs generative) but **one continuum with
  a blur floor**, and "the generative half" is a UI affordance over the low-bit end of the single ledger. If so,
  the brief's two-halves dichotomy may be *over-separating* what is one clamped scale — which would be safer
  (one ledger, one clamp) than two coupled subsystems. Worth deciding before building two things.
- **Who audits the conjecture generator?** The project's credibility rests on cross-model external passes. The
  *gather* half gets them. Does the *conjecture-proposing model* get a cross-model pass on its fan before the
  fan is admitted, or does one model's hallucination enter the substrate unchallenged? (The prior opus audit's
  "tooling that reshapes data is exempted from the honesty standard" gap, lifted to the generative half.)
- **Does naming a stub make its answer real?** (K3 §6, unresolved.) In a live council, surfacing "who really
  founded X" partly *creates* the answer. Where is the line between an honest probe and a leading question —
  and can an instrument that back-reacts on its subject ever report an independence-clean corroboration?

---

*Demote-not-kill throughout. The two-halves instrument is the right design and the gather half's per-axis
record is load-bearing and correct. The single highest-leverage correction is not a kill but a **re-binding**:
the conjecture fan's home is the `K3_observation_to_knowledge.md` stub (typed, falsifier-bearing, min-clamped,
lifecycle-bound), not the brief's flat `conjectures[]`; and its output is a blur-floored fan, not an "emergent
canonical reading." Cite K3, adopt the min-clamp as a build-time invariant, make WHY/HOW edges, gate followups
on `t_event`, and demote losing conjectures to dead-children rather than deleting them — then light it.*
