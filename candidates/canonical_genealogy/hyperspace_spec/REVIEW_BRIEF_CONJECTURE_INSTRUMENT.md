# REVIEW BRIEF — the two-halves instrument: gather (measured) + sim-the-gaps (weighted conjectures)

**For:** an adversarial external pass (opus + Gemini). **Date:** 2026-06-21. Demote-not-kill.
**Companions on disk:** `GAPS_AND_BACKBONE.md` (the backbone + gap findings), `DRAFT_HARVEST_PLAN.md`
(the 5-phase plan), `WHERE_WE_ARE.md` (the ground-truthed corpus picture). Read those for full context.

## The project in one breath
A "latent camera": harvest ALL the project's data into one iterable GLOBAL SUBSTRATE (the unifying record =
the **LatentEvent** class: who/what/where/when/why/how + an observer/WHOM axis + frame{time,space,knowledge,
meaning} + a physical↔latent layer), federate over existing source-of-truth stores, recompile procedurally to
views, render a 4D hyperspace viewer (physical+latent membranes, two bitemporal timelines), and stream every
future action as a "beam of light through the keyhole." Governed by the COIN: **rendered sharpness ≤ measured
bits; blur is the badge; never launder a generated bit as a measured one.** Comparison is ordinal and only valid
**within a declared contract** {coder, era, model, frame}; cross-contract renders blurred. Backbone (from the
crawl): a **DAG** for lineage/provenance (acyclic-to-present + a bounded cyclic overlay for couplings/forcing) +
**KG-RAG** spreading-activation retrieval (NOT a vector store; the meaning axis stays blurred until an NLI
instrument exists).

## Pav's directive being reviewed (the OTHER HALF of the instrument)
> "Gather what we can, and **sim the missing gaps on top with multiple conjectures** — the other half of the
> instrument — while being **clear what is what**, with **confidence weights, follow-ups, and deeper research.**"

So the instrument has TWO HALVES:
1. **MEASURED (gather):** harvest real data → the DAG, per-axis `measured_bits`, the sharp/physical layer.
2. **GENERATIVE (sim):** where data is missing, **simulate/conjecture** to fill the gap — but with **MULTIPLE**
   conjectures (a fan, not one), each carrying a **confidence weight**, a **clear "what is this" tag**
   (measured | estimated | modelled | conjectured), and **follow-up research stubs** (what would raise its bits).
This is the predict-half / forward camera the crawl found is currently 100% dark. The COIN keeps the two halves
visibly distinct; the X*n mechanism (render n conjectures → an emergent canonical reading) is the scoring layer.

## Gap #1 (the foundational fix this review centers on): the record is TOO FLAT
The draft plan's record carries a single subject-predicate-value triple and **ONE scalar `bit_unit.cost`** for
the whole event. That CANNOT express "**sharp on WHERE, blurry on WHY**" (the same event well-measured on one
axis, pure conjecture on another), and it has **no observer (WHOM) axis** and **nowhere for conjectures/the probe
to attach.** Proposed fix = the **v0.3 per-axis record**:

- Decompose every event into its **content axes**: WHO · WHAT · WHERE · WHEN · WHY · HOW · **WHOM (observer)**.
- Each axis independently carries: `measured_bits`, `signal_type` (reasoning_tokens|markers|mdl|residue|nli|none),
  `confidence ∈ [0,1]`, AND a `conjectures[]` list (the sim half): each `{reading, weight ∈ [0,1], tag:
  measured|estimated|modelled|conjectured, basis, followups[]}`.
- The **contract** {coder, era, model, frame} attaches at **WHOM**; the measurement lives **per axis**.
- The COIN renders **per axis**: a node is a sharp point on WHERE/WHEN (physical membrane) and a blurry fan on
  WHY (latent membrane) — the camera honest about its own resolution, axis by axis.

The claim under review: **the per-axis record is the home of BOTH halves** — measured bits per axis AND the
weighted-conjecture fan per axis — so gap #1 is not a schema nicety, it is the structure Pav's two-halves vision
requires. The second COIN (aggregation faithfulness: `rendered(parent) ≤ Σ children − bits_discarded`) and the
4D differential render also depend on per-axis bits.

## What to review (verdict {sound|overstated|risky|wrong} + sharpest flaw + fix, each)
1. **The two-halves framing** — is "measured gather + multiple-weighted-conjecture sim, COIN-separated" a sound
   instrument design, or does it invite laundering / conjecture-inflation? What governs how many conjectures, and
   how they are scored/pruned (the X*n → emergent-reading mechanism)?
2. **The per-axis v0.3 record as the home of both halves** — does it actually carry the two halves cleanly? What
   axis or case does NOT fit (e.g. relational facts, an event with no clean WHO/WHY)? Is WHOM-as-observer the
   right place for the contract?
3. **Confidence weights** — across measured bits, per-axis confidence, conjecture weights, and contract validity,
   are these commensurable or four different scalars wearing one name? How should they compose without faking a
   single number?
4. **Follow-ups / deeper research as first-class** — how should a conjecture's `followups[]` be generated,
   tracked, and closed (the keyhole loop), and how does closing one re-score the conjecture fan?
5. **The biggest RISK** of lighting the generative half, and the single most important guardrail before it ships.

Be concrete, skeptical, grounded in the on-disk docs where possible. Demote-not-kill.
