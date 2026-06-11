# REVIEW THROUGH THE FRAMEWORK — the review-and-update pipeline as an instance of the agnostic framework's own machinery

> **Status:** Tier-3 working lens, for the review-pipeline agents. NOT canon, NOT a promotion. This document is a **POV lens**: it tells the pipeline's agents to reason about reviews, pins, asks, and gives **in the framework's own vocabulary** (forcing events, the A−/A+ charge canon, the weld lifecycle, the claim-lifecycle's demote-not-kill discipline, the fuzzy-to-canon compile loop, the dated-record discipline). The mapping is the framework **eating its own dogfood** — the same reflexive self-hosting move as `specimens/agnostic_framework.json` (the instrument rendering its own maker), applied one level out to the *tooling around* the instrument. It introduces **no new framework primitive** and promotes **nothing**: the cross-substrate convergence list stays **9**; bits stay qualitative; every claim it makes about its own fidelity carries an honest limit (§7). Where the map is convenient vocabulary rather than load-bearing structure, it says so out loud (§7) — over-claiming the isomorphism would itself violate the discipline this document is trying to teach.

> **How to use this as an agent.** When you process a review pin, do not invent a separate mental model for "reviews." Read the pin as a **forcing event**, read its ask/give as an **A−/A+ charge pair**, drive its status through a **weld lifecycle**, and keep its record under the **dated-record / demote-not-kill** discipline. The sections below give the exact correspondences. §6 is a fully worked example using Pav's real pin #1 — read it first if you want the short path.

---

## §0 — The one-breath mapping

A review pin is a **force from outside the viewer-genealogy that pulls the viewer toward a better shape.** The Pav-observer, standing over the viewer-wrapper, drops a pin (a *forcing event*: a **pull** when it asks for something added, a **squeeze** when it asks for something removed/constrained). The pin carries a **charge pair**: the reviewer's comment is the **A− charge** (the critique — the part that does the real compilation work), and the response/change is the **A+ charge** (the admission of new structure into the canon viewer). The status of the pin (`open → acknowledged → answered → applied → verified`) is a **weld lifecycle** running on the ask — the ask is a candidate child welded onto the viewer, and the lifecycle is its graded path from proposed to consummated. A dead ask is **demoted, not deleted** — a dated record, exactly like a dead experiment-child in `CLAIM_LIFECYCLE.md`. And the whole iteration loop (fuzzy comment → compiled change → updated canon viewer) **is the framework's own fuzzy-to-canon compile loop**, turned on the viewer instead of on a theory.

That is the lens. The rest of this document makes each correspondence precise and names where it is structure vs. vocabulary.

---

## §1 — A review PIN is a FORCING EVENT (D4) acting on the viewer-wrapper

**Source of truth:** `SCHEMA_v2.md` §2.9 (`forcing_events`, the D4 exogenous pull/squeeze layer) and `specimens/agnostic_framework.json` (this specimen is itself **crisis-pulled** — its `forcing_events` layer, "Pav steers + cross-model squeezes," IS its lifecycle spine, per R33).

The framework's `forcing_events[]` layer is the "weather/climate" *over* a genealogy — events **outside** the idea-tree that act **down** onto it, pulling or squeezing welds and lineages (`SCHEMA_v2.md` §2.9). A review pin is precisely such an event, and the correspondence is exact in every field:

| `forcing_events[]` field | What it is in the framework | What it is for a review pin |
|---|---|---|
| the **event** itself | an exogenous force outside the genealogy (a war, a depression, a funding winter) | a **pin dropped on the viewer** — a force from outside the viewer's own code-genealogy |
| **`acted_on[].target`** | the weld/wrapper/actor the event forced | the **viewer element** the pin is attached to (the bottom bar, a panel, a widget) — carried by the pin's `nx/ny` + DOM context |
| **`acted_on[].direction: pull \| squeeze`** | one event can **pull** one lineage while **squeezing** its rival (R20, lineage-relativity) | **pull** = "add / enable / make this richer" (pin #1: *make the bar draggable + collapsible*); **squeeze** = "remove / constrain / simplify this" |
| **`effect: accelerate \| elevate \| suppress \| redirect \| …`** | the graded effect on the target | the concrete edit class the pin demands (add-capability, restyle, delete, reposition) |
| **`when`** | a date or interval | the pin's `savedAt` timestamp |
| **`mechanism`** | HOW it pulled/squeezed (prose) | the pin's **comment text** — the reviewer's account of what is wrong and what they want |
| **`strength ∈ [0,1]`** | the event's influence is a membership, not binary | how load-bearing the ask is (a blocking defect vs. a nice-to-have) — a graded reading, never a fabricated number |
| **`veridical`** (R21) | the force is real but its OBJECT may be false (a phantom threat that still drove a program) | the **honest separation** between "the reviewer's friction is real" (force veridical) and "the fix they proposed is the right one" (object may be false). A pin can be a true signal of a real problem *and* propose the wrong solution — record both, do not collapse them. |

**The Pav-observer as the forcing source.** In `forcing_events[]`, the force originates *outside* the genealogy being rendered. Here the force originates from **Pav-the-reviewer**, who stands *outside* the viewer (he is its observer/user, not part of its code). This is the same observer-relativity the framework makes first-class everywhere else (the observer kernel `{time, space, knowledge, meaning}` that frames what counts as emergence): the viewer-wrapper's evolution is being driven by forces in its observer's frame. A pin is an observer-frame forcing event made concrete and dated.

**Why this is the right primitive (not a discrepancy, not a comment).** The framework reserves `forcing_events[]` for forces that are (a) exogenous, (b) recurring as a *driver type*, and (c) often acting on *multiple* targets at once (`SCHEMA_v2.md` §2.9, "why first-class"). Review pins satisfy all three: they come from outside the code, "a reviewer asks for a change" is a recurring driver type across the whole pipeline (the weather over the viewer), and one review session can drop several pins forcing several elements at once. So the pipeline's central object earns the same first-class slot the framework gives the weather over a theory.

---

## §2 — ASK and GIVE are the A−/A+ adversarial-affirming CHARGE PAIR (the cont-15 asymmetry)

**Source of truth:** `specimens/agnostic_framework.json` sub-wrapper `sw-charge-canon` ("A+ admits structure into the canon graph, A− prunes it; canon stays viable only with slack between them"), the **cont-15 supersession** (symmetric Cayley-table algebra of cont-13 **walked back to asymmetric** at cont-15, 2026-05-16, **A− promoted to primary**), and `SCHEMA_v2.md` §2.10.a (D6a, where `a_charge ∈ [0,1]` is "a FOLD into the framework's existing A−/A+ adversarial canon, NOT a new primitive").

The framework's charge canon is a **pair of operators** that keep a canon alive: **A+** *admits* structure into the canon graph; **A−** *prunes/critiques* it; the canon stays viable only when there is **slack** between them. A review pin carries exactly this pair:

- **ASK = the A− charge.** The reviewer's comment is the **adversarial / pruning** charge — the critique. It says *this is wrong / missing / mis-shaped.* It does not, by itself, add anything to the viewer; it identifies what the viewer lacks or carries wrongly. In the framework's render-slot this is the D6a `opposes[]` relation with an `a_charge ∈ [0,1]`: the ask **opposes** the current viewer (`from: the reviewer`, `target: the viewer element`, `a_charge:` how decisively, `mode:` one of debunk/out-compete/co-opt/…, here typically a constructive *out-compete* — "the panels do it better, this bar should too").
- **GIVE = the A+ charge.** The response/change is the **affirming / admitting** charge — it admits new structure (the implemented capability, the restyle, the deletion-as-simplification) into the canon viewer. It is the actual diff plus its commit ref: text describing what was done, and the SHA that welded it in.

### 2.1 The load-bearing asymmetry: A− does the real compilation work (cont-15)

This is the single most important thing for an agent to carry from this lens, and it is **not** decoration — it is a dated, in-vivo result in the framework's own history. At cont-13 the charge canon was modeled as a *symmetric* Cayley-table algebra (A+ and A− as balanced, interchangeable operators). At **cont-15 (2026-05-16) Pav walked that back to an asymmetric model and promoted A− to primary** (`sw-charge-canon`: "a clean in-vivo SUPERSESSION … A− promoted to primary"; the self-specimen lists this as "an in-vivo supersession," and the symmetric-algebra sub-claim is recorded as the *superseded child*).

The consequence for reviews: **the ASK (A−, the critique) is the part that does the real compilation work, not the GIVE (A+).** The critique is what *drives the improvement* — it identifies the gap, sets the target, and supplies the pressure. The give is downstream: it is the admission of the structure the critique demanded. A pipeline that treats ask and give as symmetric ("a comment and a reply, equal weight") has reproduced the cont-13 mistake the framework already corrected. The asymmetry says: **honor the critique as the engine.** A pin with a sharp ask and no give yet is still doing its job (the A− pressure is live); a pin with a give but a vague ask has skipped the step that does the work.

> **Slack, not war.** The canon "stays viable only with slack between A+ and A−" (`sw-charge-canon`). For the pipeline this means: the goal is **not** to maximize asks (pure A− prunes the viewer to nothing) nor to rubber-stamp every ask into a give (pure A+ bloats it). A healthy review backlog has *slack* — open asks the viewer has not yet answered, held in tension, demoted when they stop earning their place. The status lifecycle (§3) is how that slack is managed over time.

### 2.2 The charge pair is a FOLD, not a new combat construct

`SCHEMA_v2.md` §2.10.a is explicit that D6a **reuses the framework's own adversarial primitive rather than inventing one** — it "merely gives that primitive a render-slot at the weld." Agents should mirror that discipline: the ask/give pair is **not** a new "review-combat" model bolted onto the framework. It is the framework's existing A−/A+ canon given a render-slot **at the pin**. The pin is where the viewer's adversarial charge (the critique) and affirming charge (the change) meet and resolve. Treat it as a fold, never as a new substance — the same design-law restraint the schema imposes on itself.

---

## §3 — The STATUS LIFECYCLE is a WELD LIFECYCLE on the ask (and a dead ask is demoted, not deleted)

**Source of truth:** `SCHEMA_v2.md` §2.2 (the weld's graded life: `risen → active → dormant → resurrected`, the `status_trajectory[]`, the `phase_trajectory[]`) and `CLAIM_LIFECYCLE.md` §1–§3 (demote-not-kill; the append-only dated record; the dead-children tally).

An ask is a **candidate child welded onto the viewer-wrapper.** The viewer is the parent; the ask proposes a specific change (a new child operationalization of "a better viewer"). Driving that ask from proposal to consummation **is a weld lifecycle.** The pipeline's status enum maps onto the framework's lifecycle phases:

| Pin status (the ASK's lifecycle) | Framework weld/lifecycle phase | What it means structurally |
|---|---|---|
| **open** | the candidate child is **proposed** — a forcing event has landed, the weld is named but not yet fired (`open-conjecture` / a `forcing_event` whose target weld has not yet risen) | the A− charge exists; the viewer has not yet responded. Pure slack. |
| **acknowledged** | the weld is **recognized as live** — entered into the `status_trajectory[]` with a date and a `by` (someone owns it) | the pipeline accepts the ask as a real forcing event to act on; the candidate child is admitted to the build queue. |
| **answered** | a candidate child is **designed/proposed in reply** — a give exists as a plan or a draft, the weld is forming | the A+ charge is drafted (here's what we'll do / here's the diff) but not yet consummated/merged. |
| **applied** | the weld **fires / rises** — the give is implemented and committed; `child.status: active`, a `phase_trajectory[]` entry `consolidation`, the commit SHA is the weld's consummation date | the A+ charge has admitted the structure into the canon viewer. The change is in the code. |
| **verified** | the weld is **consolidated** — confirmed against the pin's own replayed slice (the captured settings/timeline/panel-layout), so the give demonstrably answers the ask in the exact context it was raised | the highest-confidence state: the weld held under inspection. Analogous to a claim that not only rose but survived a check. |

**The dead ask = demoted, not deleted (the `CLAIM_LIFECYCLE` discipline, exactly).** When an ask is rejected (wontfix), superseded by a different change, or abandoned, it is **never deleted from the record.** It is **demoted** — a dated `status_trajectory[]` entry (`state: "demoted — open → wontfix"`, `when`, `by: <what forced it>`), and the pin is kept as a permanent dated record. This is `CLAIM_LIFECYCLE.md` §0/§3.4 turned on asks: *a claim is not killed, it is demoted / dormant / friction-logged.* The same three anti-gaming rules carry over verbatim:

1. **A demotion is append-only and dated** — a dead/rejected ask is never silently removed; it is the permanent record (`CLAIM_LIFECYCLE.md` §3.4 rule 1).
2. **A reinterpreted revival does not reset the record** — if an old ask is re-raised in a new form (a new pin on the same element), the prior demoted ask stays on the record; you cannot launder a rejected ask by re-filing it (rule 2).
3. **"Re-ask it again" is itself logged** — re-raising a previously-demoted ask is allowed but *costs a recorded entry every time* (rule 3). A viewer element that keeps attracting the same demoted ask is *signalling* — the accumulated friction is visible, which is the honest analogue of the dead-children tally.

> **Dormant asks have a revisit trigger.** Just as a dormant parent conjecture carries a `revival.trigger` (the event that would wake it, `CLAIM_LIFECYCLE.md` §1), a parked ask ("good idea, not now") should carry the condition under which it gets re-childed — *"revisit when the panel system is refactored," "revisit if a second reviewer asks for the same thing."* Dormant ≠ dead; it is parked with a named wake condition.

---

## §4 — The ITERATION LOOP is the framework's own fuzzy-to-canon COMPILE LOOP

**Source of truth:** `specimens/agnostic_framework.json` parent W_A ("Pav-intuition — the decades-long **fuzzy-to-canon compiler**") and the substrate's compile pipeline (append-only JSONL → SQLite → compiled JSON, the viewer contract).

The framework's deepest self-description is that Pav's creative source is a **fuzzy-to-canon compiler**: fuzzy intuitions (ideas attract/repel, +/− unions, a nesting-space conceives a third) get *compiled* into a canon (the formalized schema, the ratified surface), with **fidelity continually upgrading as the substrate evolves** ("it all started out as nothing and a point… the fidelity is continually upgrading"). The review pipeline **is this same loop**, one level out:

```
   FUZZY INPUT                 COMPILED CHANGE                 CANON ARTIFACT
   a pin comment        →      a designed + committed     →    the updated
   ("make this bar             diff (the give, with a           canon viewer
    draggable…")               commit ref)                      (viewer_v3.html)
   = the A− charge,            = the A+ admission,              = the higher-fidelity
     fuzzy & human               compiled & precise               substrate state
```

- The **fuzzy input** is the reviewer's natural-language comment — imprecise, human, intuition-shaped (exactly the register of Pav-intuition's W_A: "fuzzy"). The pipeline must *translate it back to framework/build concepts* before acting — the same discipline as `feedback_translate_formalization_for_pav` run in reverse (there, formalization is translated back to intuition; here, intuition is compiled forward to a precise change).
- The **compiled change** is the give: a specific, committed diff. This is the "canon" pole of the compiler — precise, dated, append-only (the commit history is the append-only fact store, mirroring the substrate's JSONL→SQLite pipeline).
- The **canon artifact** is the updated viewer. And critically: **fidelity continually upgrades.** Each processed pin leaves the viewer at a higher-fidelity state than before — the viewer is "a fidelity-upgrading garden" (W_A's own words), and the review pipeline is the gardening. This is why pins-as-permanent-records matters: the record of upgrades *is* the substrate's evolution, made auditable.

So an agent processing a review is **running the framework's central compile loop on the viewer**: take fuzzy observer-frame pressure (A−), compile it into a precise admission (A+), weld it into the canon artifact, and record the upgrade as a dated, append-only fact. The pipeline is not *like* the framework's machinery; for this loop it *is* the machinery, pointed at the tool instead of at a theory.

---

## §5 — PINS-AS-PERMANENT-RECORDS is the DATED-RECORD discipline

**Source of truth:** `CLAIM_LIFECYCLE.md` §3.4 (append-only, dated, never deleted) and the substrate's **append-only fact store** (`CHANGELOG.md` 2026-06-10; the self-specimen's "append-only JSONL → SQLite").

The framework's honesty rests on one discipline above all: **records are append-only and dated; nothing is silently un-said.** A demoted claim stays on the record as a demotion; a dead child stays in the tally; the substrate is an append-only fact store. The review pipeline inherits this discipline directly:

- **Every pin persists** in `reviews/pins.json` with its `savedAt`, its captured slice, and its full annotation/comment history — it is the permanent dated record of an observer-frame forcing event.
- **Status changes append, they do not overwrite.** The pin's status history (`open → acknowledged → … `) is a `status_trajectory[]`: each transition is `{state, when, by}`, kept in order. You read the *trajectory*, not just the current state (the same reason the framework keeps `status_trajectory[]` rather than a single lossy enum — see the self-specimen's note that "the single enum is lossy; see status_trajectory").
- **The give is recorded against the ask, with its commit ref.** The A+ admission is welded to the A− critique that demanded it, dated, with the SHA — so the record shows not just *that* the viewer changed but *which critique drove which change when.* That is the audit backbone (`sources`-style citation, `SCHEMA_v2.md` §2.11) applied to the viewer's own evolution.

The payoff is the same as the framework's: **the surviving is auditable.** A viewer that has absorbed fifty pins carries a dated, append-only history of every observer-frame force it answered, demoted, or parked — the viewer's genealogy, rendered in its own review record.

---

## §6 — WORKED EXAMPLE: Pav's pin #1, verbatim, through the lens

This is the pipeline's **first real ticket**, and processing it through the lens is the dogfood test. The pin is real and already on the registry (`reviews/pins.json`, id `20260611-003618-make-this-menu-colapsable-and-dragable-l`).

**The pin, verbatim:**
> page `/viewer_v3.html`, comment: **"make this menu colapsable and dragable like the other overlay panels "** — attached at `nx 0.3159, ny 0.8375` (the bottom control bar: Play / NOW / scrub / sliders), `savedAt 2026-06-10T23:36:17.914Z`, 9 annotations, captured slice in the `.review.json` (observer=all, depth=100, scrub=100, mag=55, mir=62; active controls Maxwell EM / ⛈ Weather / ■ Bedrock / ♪ Narrate / All).

Now read it in framework terms, field by field:

**(1) The pin is a FORCING EVENT (§1), direction = PULL.**
- `acted_on.target` = the viewer's **bottom control bar** (the "v1 bar": Play/NOW/scrub/sliders), localized by `nx/ny` and the captured DOM/canvas context.
- `acted_on.direction` = **pull** — the ask *adds capability* (drag + collapse). It elevates the bar to parity with the already-draggable overlay panels. (Contrast a squeeze, which would ask to remove or constrain the bar.)
- `effect` = **elevate / accelerate** (bring the bar up to the panels' interaction class), `strength` = a graded reading of how load-bearing this is (here: a real usability defect Pav hit in his first test — non-trivial, but not a correctness blocker).
- `mechanism` (the comment text) = *"make this menu colapsable and dragable like the other overlay panels"* — the reviewer's account of the gap (the bar is second-class next to the panels) and the target (panel-parity).
- `veridical`: the **force is plainly veridical** (the bar genuinely lacks drag/collapse; Pav genuinely wanted it). The *object* (the specific implementation) is what the give will settle — separable, and both worth recording.
- The **Pav-observer** is the forcing source: the pressure comes from outside the viewer's code, in the user's frame.

**(2) The ASK is the A− charge (§2), and it does the compilation work.**
- The A− critique: *the bottom bar is not draggable or collapsible like the other panels — it is second-class.* This is the **pruning/adversarial** charge: it does not add code, it identifies the gap and sets the target. Per the **cont-15 asymmetry**, this critique is the **engine** of the improvement — it is the part that does the real work; the give is downstream of it. An agent must honor the ask as primary, not treat it as half of a symmetric comment/reply.
- In D6a terms: `opposes: { from: "Pav-reviewer", target: "viewer_v3 bottom control bar", a_charge: <decisive>, mode: "out-compete" ("the overlay panels do this better; the bar should match"), note: the comment }`.

**(3) The GIVE is the A+ charge (§2), recorded when the build phase lands it.**
- The A+ admission: implement drag + collapse on the bottom bar (using the viewer's existing panel machinery, so the bar joins the same draggable/collapsible system), then record on the pin: a **give text** ("bottom control bar now draggable + collapsible, reusing the overlay-panel drag/collapse harness; position + collapsed-state persisted via the review-state hooks") and a **commit ref** (the SHA that welded it in). This is the structure *admitted into the canon viewer*.

**(4) The STATUS LIFECYCLE is a weld on the ask (§3).**
- Today the pin is **open** — the candidate child (draggable bar) is proposed; the A− charge is live; the viewer has not yet responded. Pure slack.
- The build phase drives it: **acknowledged** (owned, dated) → **answered** (the give is designed/drafted) → **applied** (the diff is committed; the weld fires; `child.status: active`; `phase_trajectory: consolidation`; the SHA is the consummation date) → **verified** (confirmed against the pin's own replayed slice — load the captured observer=all / depth=100 / scrub=100 / mag=55 / mir=62 state and the panel layout, and confirm the bar now drags and collapses *in that exact context*).
- **This is the pipeline processing its own first ticket through itself**: the very pin that asks for the feature becomes the dated record that the feature was welded, with the give and commit attached — the framework's compile loop run on the viewer, recorded under the dated-record discipline.

**(5) The COMPILE LOOP and DATED RECORD (§4, §5).**
- Fuzzy input (the human comment) → compiled change (the committed drag/collapse diff) → canon artifact (a higher-fidelity `viewer_v3.html`). Fidelity upgraded by one increment; the pin persists in `pins.json` as the permanent, dated record of the observer-frame force that drove the upgrade, with its status trajectory and the give's commit ref appended — never overwritten.

> **One-line reading of pin #1:** a *pull* forcing event from the Pav-observer carries an A− critique (the engine) that the build phase answers with an A+ give (drag+collapse, committed); the ask's status runs a weld lifecycle `open→…→verified`; and the pin stays a dated, append-only record of the whole transaction. The framework's machinery, dogfooded on its own viewer.

---

## §7 — HONEST LIMITS: where the map is real structure vs. convenient vocabulary

This is Tier-3, and the discipline this whole document teaches forbids it from over-claiming its own isomorphism. The framework's own self-specimen models exactly this honesty (its `discrepancies[]`, its "convergence-cuts-both-ways" note, the unadopted forced-retirement rule held open as live friction). The same candor, turned on this lens:

**Where the mapping is REAL structure (load-bearing, not decoration):**
- **Forcing event ← pin (§1).** This is genuinely structural. The framework's criteria for `forcing_events[]` (exogenous, recurring driver-type, multi-target) are *met* by review pins, field for field, including the pull/squeeze lineage-relativity and the veridical separation. An agent loses nothing by treating a pin as a forcing event — the abstraction earns its place.
- **Demote-not-kill / dated-record ← pin persistence (§3, §5).** Also genuinely structural and, frankly, the strongest part of the map: the append-only, dated, never-deleted discipline is *the same discipline* whether the object is a claim or an ask, and the three anti-gaming rules transfer without strain. This is the framework's machinery doing real work on the pipeline.
- **A−/A+ as a FOLD ← ask/give (§2).** Structural at the level of *roles* (critique prunes/identifies; change admits structure; slack between them keeps the artifact viable), and the cont-15 asymmetry (critique does the compilation work) is a *useful, dated* corrective the pipeline should actually obey.

**Where the mapping is CONVENIENT VOCABULARY (a helpful frame, not a proof of identity):**
- **The cont-15 asymmetry is a borrowed slogan, not a derived result for reviews.** That A− "does the real compilation work" is established *in the framework's own conceptual history* (cont-13 → cont-15), not *re-derived* for the review domain. It is a genuinely useful heuristic ("honor the critique as the engine"), but an agent should hold it as **borrowed wisdom that fits**, not as a theorem about reviews. Calling it structure would be over-claiming.
- **The weld lifecycle ↔ status enum is an analogy with a real gap.** `open→acknowledged→answered→applied→verified` *rhymes* with `proposed→active→…→consolidated`, but the framework's weld lifecycle is about *theory-merges rising in a field*, and a review status is about *a ticket moving through a queue*. The correspondence is a helpful scaffold for reasoning, not an identity — the underlying processes are different in kind, and the map should never be used to *infer* properties of one from the other beyond the bookkeeping it organizes.
- **"Charge" is a metaphor doing honest work, but a metaphor.** The framework's A+/A− are operators on a *canon graph of concepts*; a review's ask/give are *a comment and a commit*. The charge framing illuminates the asymmetry and the slack, but no one is computing an `a_charge ∈ [0,1]` for a pin from first principles — when a pin records an `a_charge`, that is a graded *judgment*, the same qualitative-membership discipline the framework uses everywhere (and, per the standing rule, **never** a fabricated measured number).
- **The compile-loop mapping (§4) is the most evocative and the most loosely-coupled.** Pav-intuition's fuzzy-to-canon compiler is a description of *decades of private creative work*; a review iteration is *one comment → one diff*. The shared shape (fuzzy in → compiled out → higher-fidelity artifact, append-only) is real and worth carrying, but the scales and the substances differ by a lot. Use it as a *lens for how to behave* (translate the fuzzy comment carefully; record the compiled change; treat the viewer as a fidelity-upgrading garden), not as a claim that a code-review *is* the framework's central compiler.

**The honest net (adopting the self-specimen's own posture).** This lens is the framework **eating its own dogfood at Tier-3**: the bookkeeping discipline (forcing events, demote-not-kill, dated records) transfers *as structure*, and the charge/lifecycle/compile-loop framings transfer *as productive vocabulary that genuinely shapes good behavior* — but the further from the append-only bookkeeping you get, the more the map is a useful way to *think* rather than a proven identity. The mapping's value is not that "a review IS the framework" — it is that **agents who reason about reviews in these terms will keep the right disciplines** (honor the critique, record everything dated, demote-don't-delete, upgrade fidelity each pass) **without the pipeline having to re-invent a model the framework already paid for.** Where it clarifies, use the mapping. Where it would decorate, drop it. And like every claim in this program, this lens is itself a dated record open to demotion — if an agent finds the vocabulary obscuring rather than clarifying a review, that friction goes on the record, and the lens is revised, not defended.

---

*Tier-3 working lens for the review-pipeline agents. Promotes nothing; the cross-substrate convergence list stays 9; bits stay qualitative; all charge/strength readings are qualitative judgments, never fabricated measured values. The structural transfers (forcing-event = pin; demote-not-kill / dated-record = pin persistence) are load-bearing; the charge / weld-lifecycle / compile-loop framings are productive vocabulary, flagged as such in §7. Sources: `CLAIM_LIFECYCLE.md`; `SCHEMA_v2.md` §2.9 (forcing_events / D4), §2.10.a (D6a, the A−/A+ fold); `specimens/agnostic_framework.json` (`sw-charge-canon` + the cont-15 asymmetry, W_A the fuzzy-to-canon compiler, the reflexive self-hosting posture, `discrepancies[]`). Worked example uses Pav pin #1 verbatim from `reviews/pins.json`.*
