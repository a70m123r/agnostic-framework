# CLAIM LIFECYCLE — a claim is not killed, it is demoted / dormant / friction-logged

> **Status:** Tier-3 WORKING DRAFT, surfaced for **Cowork+Pav ratification**. NOT canon, NOT a promotion. This formalizes Pav's claim-lifecycle reframe (2026-06-10) and is the conceptual companion to the `canonical_genealogy/specimens/agnostic_framework.json` self-specimen — it gives that specimen its vocabulary for rendering the framework's OWN claims as a genealogy. It introduces **no new framework primitive**: every state below either reuses a `SCHEMA_v2.md` field or is marked **PROPOSED-not-promoted** with the gap it fills. The cross-substrate convergence list **stays 9**; nothing is promoted; demoted/dormant claims stay demoted/dormant. Bits stay qualitative.

---

## §0 — The reframe in one breath

A load-bearing claim in this program is **never killed.** It is **DEMOTED** (loses tier/standing), goes **DORMANT** (parked, awaiting a better operationalization), or is marked with **FRICTION** (a dated record of a failed attempt against it) — each a dated **RECORD**, periodically revisited as the field and our understanding grow. This is deliberately the same lifecycle the framework already grants its *wrappers* (`risen → active → dormant → resurrected`, D6 friction, revival) — the framework applied **reflexively to its own claims.**

The reframe carries one **load-bearing distinction**: a **CONJECTURE / HYPOTHESIS is a PARENT** (a wrapper — broad, durable, the thing we actually believe); a **TECHNICAL APPROACH / EXPERIMENT is its CHILD** (a specific operationalization — narrow, disposable, the thing we test). **When a child experiment fails, the parent conjecture is not killed; the child is demoted/retired, and the parent at most goes dormant and accrues friction, awaiting a better child.**

And it carries one **honest tension, encoded not hidden:** this exact structure is what makes a parent conjecture hard to falsify (you can always blame the child). So the record must be **disciplined** — every demotion dated, every dead child named, a revisit trigger noted, and a **TALLY of how many children have died for that parent.** That tally is the **falsification-pressure gauge**: the claim cannot be killed, but accumulated friction is *visible*, and visibility is the honest answer to the meditation's "a vocabulary that cannot lose" (`MEDITATION_QUESTIONS.md` #1/#11; `CHANGELOG.md` 2026-06-10: *"three refutations have been absorbed as estimator-not-claim failures — 'a vocabulary that cannot lose' until the claim itself can fail"*).

---

## §1 — The states, mapped onto `SCHEMA_v2.md` (reuse first; PROPOSE only what is genuinely new)

The discipline is **reuse where it fits.** `SCHEMA_v2.md` already gives the framework a status enum, a status/phase trajectory, and a friction (D6) layer. The claim-lifecycle states bind to those existing fields; only two states are genuinely new, and both are marked **PROPOSED-not-promoted** (they do not enter canon and promote nothing — they are render-slots awaiting ratification).

| Lifecycle state | Meaning (for a CLAIM) | Maps onto existing `SCHEMA_v2.md` field | Reuse / PROPOSED |
|---|---|---|---|
| **active** | The claim currently stands at its stated tier; its current child is live (running, or pending real data). | `child.status: active` (§2.1) — and, for the framework's never-consummated claims, `child.status: open-conjecture` ("live-unconsummated-weld"). | **REUSE.** `open-conjecture` already exists precisely for "a high-synergy weld that never produced a settled child" — the canonical state of a parent whose children have all died. |
| **demoted** | Standing is reduced on the merits (e.g. Tier-2 candidate → illustrative; "differentiator" → "standard method"), recorded with a date and a reason. | `child.status_trajectory[]` (§2.1, R5) — an entry `{state, when, by, confidence}`; for a demotion that breaks identity (the claim is no longer "the same" claim), `continuity ∈ [0,1]` / `identity_break` (R24). | **REUSE.** A demotion is one entry in the trajectory: `state: "demoted — <from> → <to>"`, `when`, `by: "<what forced it>"`. `status: stale` is the enum endpoint when a claim is demoted and *not* being revived. |
| **dormant** | The parent is parked pending a better child; not refuted, not active. A revisit trigger is attached. | `child.status: dormant` (§2.1); `weld.dormancy_intervals[]` (§2.2.g) with `{from, to, why, why_frame}`; the `dormancy` phase in `lifecycle.phase_trajectory[]` (§2.2.h). | **REUSE.** Dormancy with a *reason-frame* is already first-class. The **revisit trigger** rides in `revival.trigger` (§2.2.g, the event that would wake it). `dormancy_intervals[].contested` (R32) covers "is the dormancy real or just narrated." |
| **friction** | A dated record that an attempt against the claim produced resistance / a partial refutation — without resolving it either way. | `D6` friction cluster (§2.10): `opposes[]` with `a_charge ∈ [0,1]` (D6a, the framework's existing A−/A+ adversarial charge); `weld.lag {value, cause}` (D6c) for *why* the claim still waits; `gates[]` (D6b) for a gate it failed to pass. | **REUSE.** D6a is explicitly *"a FOLD into the framework's A−/A+ adversarial canon, NOT a new primitive."* A friction record is an `opposes[]` row whose `from` is the experiment/critique, `target` is the claim, `a_charge` is the strength of the resistance. **The tally of these rows is §3.** |
| **revival** | A new child is welded onto a dormant parent; if it succeeds, the parent re-rises (possibly reinterpreted). | `weld.revival {when, by, trigger, kind: same\|reinterpreted}` (§2.2.g, R10); array-valued with `method_continuity ∈ [0,1]` per revival (R19); `child.status: resurrected`; the `revival:{same\|reinterpreted}` phase in `lifecycle.phase_trajectory[]`. | **REUSE.** A revival is *exactly* the welding of a new child. `kind: reinterpreted` / low `method_continuity` marks the case where the parent wakes as a method-incompatible object under the inherited name. |

**Two PROPOSED-not-promoted additions** (genuinely new; they fill a gap the existing fields do not cleanly hold; per `SCHEMA_v2.md` §6 item 7 + §2.8, a new vocabulary term is **proposed in a `discrepancies[]` row before use** — these are surfaced, not folded into canon):

- **`claim_status: friction-logged`** *(PROPOSED)* — a top-level rollup state on a *claim node* (distinct from a *weld* node) meaning "active-but-carrying-N-dead-children." `SCHEMA_v2.md`'s status enum lives on `child` (a wrapper); a *claim* needs the same enum **plus** a friction count. Proposed as `child.status: open-conjecture` **+** a `friction_tally` block (§3). Not promoted: it reuses `open-conjecture` for the status and only *adds* the tally; if ratification rejects the tally, the state collapses back to plain `open-conjecture`.
- **`parent_dormant_pending_child`** *(PROPOSED)* — the specific dormancy sub-type "the **conjecture** is dormant because its latest **experiment** died, not because the conjecture was refuted." Existing `dormancy_intervals[].why_frame` records *which frame* cut the lineage (time/space/knowledge/meaning/physical-political); this proposes one more `why_frame` value — `why_frame: operational` (the cut came from a failed operationalization, an internal cause) — distinguishing an **internally-caused** dormancy (the child failed) from an **externally-caused** one (a forcing event squeezed it). Proposed, pending a 2nd instance per the schema's own deferral discipline.

> **Design-law parity (held).** Exactly as in `SCHEMA_v2.md`: on a *sharp* claim — one that simply stands, with no dead children and no live dispute — every lifecycle field is **empty/default.** A sharp claim is `status: active`, empty `status_trajectory`, empty `dormancy_intervals`, empty `opposes[]`, `friction_tally: 0`. The machinery expands only at the contested frontier. If a lifecycle field feels forced on a settled claim, leave it empty — emptiness is correct signal.

---

## §2 — The CONJECTURE-parent vs EXPERIMENT-child distinction, formalized in framework terms

### 2.1 The two are a parent wrapper and a child wrapper sharing a weld

The framework's own `parents_produce_WC_FORMALIZATION_DRAFT.md` gives the machinery directly. Read the conjecture and its experiment as **two wrappers joined by a weld**:

- The **CONJECTURE** is a **parent wrapper** `W_conj` — broad, durable, frame-indexed (it lives in a `frame ∈ {time, space, knowledge, meaning}`). Example: *parents-produce-W_C* lives in the **knowledge** frame.
- The **EXPERIMENT** is a **child wrapper** `W_exp = pushout(W_conj ⊔_S W_method)` — the conjecture welded to a **method/instrument parent** `W_method` (a statistic, an estimator, a sweep) along a shared seam `S` (the operational commitment they agree on). The experiment is the conjecture's **offspring**: a specific operationalization, narrower and disposable.
- They **share a weld** (the `i: S → W_conj` inclusion). The experiment **inherits** the conjecture's content as a procedural-root stub (`SCHEMA_v2.md` §2.2.c `survived[]`; the formalization's hairy-sphere stubs) and **adds** the method parent's machinery.

**The asymmetry that makes the reframe work:** the weld is directional. The child is *downstream* of the parent. So **a child can fail without the parent failing** — killing `W_exp` (the estimator was wrong) removes one offspring but leaves `W_conj` (the conjecture) intact, now **dormant and one-child-poorer**, awaiting a better child `W_exp'`. This is the categorical reading of "the operationalization was wrong, the idea is sound." It is *legitimate once* (a child genuinely can be a bad operationalization) and *suspicious in accumulation* (a parent that keeps eating its children is signalling). §3 makes the accumulation visible.

### 2.2 Mapping to the lifecycle states

| In the experiment story | Wrapper-genealogy term | Lifecycle state (§1) |
|---|---|---|
| Conjecture is proposed | parent wrapper `W_conj` born | `active` / `open-conjecture` |
| Experiment is designed | child `W_exp` welded to `W_conj` | a sub-weld; `weld.sub_welds[]` |
| Experiment runs and **fails** | child `W_exp` demoted/retired | child: `status_trajectory` entry `demoted`; **does not touch the parent's status** |
| Parent now lacks a live child | parent `W_conj` parked | parent: `dormant`, `why_frame: operational` *(PROPOSED)* + a **friction** row (§3) |
| A better experiment is tried | new child `W_exp'` welded | `revival` (`kind: reinterpreted` if the operationalization changed shape) |
| The new experiment **succeeds** | child consolidates | parent: `resurrected` → `risen` |

### 2.3 Worked end-to-end: **parents-produce-W_C** (the parent) and its children

This is the canonical case and the one the meditation is about (`MEDITATION_QUESTIONS.md` #1). The repo's own record (`CHANGELOG.md` 2026-06-09 entries; `synergy_vs_pid/`; `frame_lock_pilot_RESULTS.md`) supplies the children.

- **PARENT (the conjecture):** *parents-produce-W_C* — two co-equal parent wrappers produce a genuine emergent third, gated by positive synergy. Frame: **knowledge**. Lifecycle state today: **`open-conjecture` / dormant-pending-a-child** — *the criterion is DEFINED, not yet demonstrated on a real two-parent model merge* (`parents_produce_WC_FORMALIZATION_DRAFT.md §5`).

| Child experiment | What it operationalized | Outcome on the record | Child state | Effect on the parent |
|---|---|---|---|---|
| **child #1 — the witnessed / affine-residual gate** (`witnessed_synergy.py`) | synergy = codelength of M after removing its best **affine** fit from A, B | **DEAD.** Cross-model pass (GPT-5.5 + Gemini) + the run confirmed it false-positives on **separable nonlinearity**: `A²+B²` flags at 1,040,352 b, *above* a genuine `A·B`. It measures **non-affinity, not interaction** (`CHANGELOG.md` 2026-06-09; `CROSS_MODEL_REVIEW.md`). | `demoted` → retired; `status_trajectory: "demoted — differentiator → measures-wrong-thing"`, low `continuity` (identity broke). | Parent **not killed.** One dead child. Friction +1. |
| **child #2 — the fixed-grid functional-ANOVA / quotient gate** (`interaction_synergy.py`) | synergy = binned functional-ANOVA interaction residual as a **codelength** | **DEAD.** Correct in *variance* but as a fixed-grid *codelength* it floors **nothing** — even affine ADD leaks ~880k bits; the polynomial-quotient variant recurs the bug on `|A|+|B|`. A general **basis/readout mismatch** (`CHANGELOG.md` 2026-06-09; `INTERACTION_RESULTS.md`; `CROSS_MODEL_REVIEW_2.md`). | `demoted` → retired. | Parent **not killed.** Two dead children. Friction +1. The cross-model pass also walked back the *more-than-PID* sub-claim — recorded as friction on the parent. |
| **child #3 — gain_v2** (`cand_predictive_gain.py`) | synergy = held-out `R²[joint] − R²[additive]`, additive baseline fit by **joint least-squares/backfit** (floors `A²+B²`, correlated-parent additive merges, and noise) | **PENDING — real-corpus.** Validated on *controlled* ground truth (four models converge it is sound; the v1 marginal-means baseline it replaced false-flagged correlated parents at +0.73). **Never run on a real two-parent model merge** (`CHANGELOG.md` 2026-06-09; the `frame_lock` pilot was controlled-only, partial-with-refutation). | `active` / pending. | Parent stays `open-conjecture` **pending child #3's real-corpus verdict.** |

Two predecessor operationalizations also died upstream and belong in the same parent's tally as friction:
- the **naive BES-4.4 / PID synergy form** `min[K(M|A),K(M|B)] − K(M|A,B)` — **inverted** on additive blends (rates a pure average ~28× above genuine synergy; `frame_lock_pilot_RESULTS.md`, the P1 witness finding);
- the **frame-lock protocol's 3 operational specifics** (R1 witnessed-residual / R2 copy-null+absolute-threshold / R3 coarse-r_top verdict) — all **refuted** by the pilot; the *protocol* (the parent's pre-registration discipline) survived, the *specifics* (children) were retired (`HANDOFF.md`; `frame_lock_pilot_RESULTS.md`).

**The honest reading of this worked example:** parents-produce-W_C is a parent conjecture with **multiple dead children and zero successful real-corpus child.** Under the reframe it is correctly *not killed* — but its **dead-children tally is high and its live-child count is zero**, which §3 says is itself the loudest falsification signal the program currently carries. The reframe does **not** rescue the claim; it makes the claim's actual standing *legible.*

---

## §3 — The DEAD-CHILDREN TALLY: the honest falsification-pressure gauge

The reframe's hardest objection is its own: *"a structure where the claim cannot be killed is unfalsifiable."* The answer is not to deny it — it is to make the **accumulated friction visible and quantitative**, so that "cannot be killed" does not mean "cannot lose standing."

### 3.1 The tally (a PROPOSED block on a claim node)

For each parent conjecture, maintain a `friction_tally` *(PROPOSED-not-promoted; collapses to plain `open-conjecture` if ratification rejects it)*:

```
friction_tally: {
  parent,                       // the conjecture (by id/name, SCHEMA_v2.md §0.1)
  dead_children: [              // every retired operationalization — the named offspring
    { child, what_it_operationalized, killed_by, when, identity_break }
  ],
  dead_count,                   // = dead_children.length  (the gauge's numerator)
  live_children: [ ... ],       // currently active/pending experiments (≥0)
  live_count,                   // 0 = the danger reading: a parent with deaths and no live child
  best_result_so_far,           // the closest any child came (honest high-water mark)
  revisit_trigger,              // what new instrument/data/field-development would justify a new child
  pressure_reading              // a QUALITATIVE band (§3.3), never a fabricated number
}
```

The tally **reuses** the friction substrate from `SCHEMA_v2.md` §2.10: each `dead_children[]` entry is the bookkeeping twin of a D6a `opposes[]` row (the experiment that out-competed the claim's operationalization, `a_charge` = how decisively). `revisit_trigger` reuses `revival.trigger` (§2.2.g). The block adds only the **count and the rollup**, which the per-row fields cannot express.

### 3.2 Why the tally is the falsification gauge

- A parent with **`dead_count = 0`** and one live child is a young, healthy claim — no pressure.
- A parent with **`dead_count = 1`** is normal science — one operationalization was wrong; legitimate.
- A parent with **`dead_count ≥ 3` and `live_count = 0`** is a claim under **heavy falsification pressure**: every attempt to operationalize it has died and none currently stands. The claim is not *refuted* (no single experiment can refute a parent), but the *pattern of dead children is itself the disconfirming evidence* — "the signature of an unfalsifiable core protected by an auxiliary belt" (`MEDITATION_QUESTIONS.md` #1) is now **measured, not just alleged.** parents-produce-W_C sits here today (3 dead children + 2 dead predecessors, 0 successful real-corpus child).
- The gauge **answers "a vocabulary that cannot lose"**: the claim cannot be killed by one result, but the **tally can rise without bound**, and a high tally with no live child is the visible, dated, public statement that the claim is *losing* — exactly the falsification-pressure the meditation said was missing.

### 3.3 The pressure reading is qualitative (bits stay qualitative)

Consistent with the program's standing discipline (`SCHEMA_v2.md` §3.3; bits-stay-qualitative), `pressure_reading` is a **band**, never a fabricated number:
`none` (0 deaths) · `normal` (1 death, ≥1 live) · `accumulating` (2 deaths, or ≥1 death with 0 live) · `heavy` (≥3 deaths, 0 live) · `critical` (≥3 deaths, 0 live, AND the best_result_so_far has not improved across the last 2 children — a stalled high-water mark). The bands are a reading of the counts; the counts are the ground truth.

### 3.4 The anti-gaming clause (the discipline that makes the tally honest)

The tally is only honest if a child cannot be quietly un-counted. Three rules, mirroring the audit discipline already in the repo:
1. **A demotion is append-only and dated.** A dead child is never deleted from `dead_children[]`; it is the permanent record (mirrors the substrate's append-only fact store, `CHANGELOG.md` 2026-06-10).
2. **A reinterpreted revival does not reset the count.** If a parent revives with a method-incompatible child (`kind: reinterpreted`, low `method_continuity`), the prior dead children **stay tallied** — the new child starts the *live* count at 1 but the *dead* count is preserved. You cannot launder friction by renaming the experiment.
3. **"Refine the estimator again" increments the tally.** The reframe's whole risk is that every refutation becomes "the operationalization was wrong, refine it." That move is *allowed* — and it **costs +1 dead child every time.** The cost is the gauge. (This is the structural fix for `MEDITATION_QUESTIONS.md` #11's "forced-retirement" concern: the program need not *kill* a claim to be falsifiable, if every failed child is *counted*.)

---

## §4 — How this REFINES meditation Q1

`MEDITATION_QUESTIONS.md` #1/#11 asks for a **KILL threshold**: *"name the numerical result that makes us abandon parents-produce-W_C rather than refine the estimator again."* The reframe says that framing is subtly wrong, and sharpens it:

- **Old Q1 (kill threshold):** "What single gain_v2 number kills the *claim*?" — This presumes a child's result can kill a parent. Under the parent/child distinction it cannot: a bad number kills the *child* (gain_v2), not the *parent* (parents-produce-W_C). Demanding a claim-kill from an experiment-result is a category error — and pretending otherwise is what produces the *un-credible* pre-commitment ("we promise to abandon decades of conjecture on one estimator run") that never actually fires.
- **Refined Q1 (friction threshold):** **"Name the friction threshold at which the *parent* is marked DORMANT pending a new child — i.e. the `dead_count` (and stalled-high-water-mark condition) at which we stop welding new children and park the conjecture as `open-conjecture / dormant`, publicly, with the tally attached."**

This is the falsifiable, *creditable* commitment the reframe can actually keep, because it acts on the right object:
- It is **pre-registerable now**: e.g. *"if gain_v2 (child #3) fails on the first real two-parent merge corpus, `dead_count` reaches 4 with `live_count` 0 and a stalled high-water mark → `pressure_reading: critical` → parents-produce-W_C is marked **dormant**, removed from any load-bearing role, and not re-childed until a **new instrument or a new substrate** (the `revisit_trigger`) exists."* That is a real, dated, public down-grade — a demotion, not a fictional execution.
- It **preserves the legitimate move** (a parent genuinely can outlive a bad child) **while pricing it** (every child costs +1, and the dormancy threshold is pre-named), so the structure stops being "a vocabulary that cannot lose."
- It **maps to existing fields**: the threshold is a pre-committed `pressure_reading` band (§3.3) that triggers a `child.status: dormant` + `dormancy_intervals[]` entry with `why_frame: operational` *(PROPOSED)* + `revival.trigger` = the named revisit condition.

> **The refinement in one line:** Q1 stops asking the experiment to kill the conjecture (impossible, and so never credibly pre-committed) and starts asking the conjecture to **name the count of dead experiments at which it parks itself** (possible, dated, and exactly the falsification-pressure the meditation was reaching for).

---

## §5 — Reflexive note (the framework rendering its own claim-handling)

This document is itself an instance of what it describes. Writing it does **not** promote parents-produce-W_C — it **demotes it to legibility**: by tallying its dead children (3 + 2 predecessors) and its live count (0 real-corpus), the reframe makes the claim's *weak* standing visible rather than narrating around it. That is the self-hosting test the agnostic-framework self-specimen exists to run: the instrument renders its own maker, and the first thing it renders honestly is that its central claim is a parent under heavy friction with no surviving child — *yet.* The reframe's value is not that the claim survives; it is that **the surviving is now auditable.**

---

## §6 — The special-pleading objection, recorded and answered (Opus review, 2026-06-10)

The skeptical review of the self-specimen put the hardest question to this whole construction directly: **is the parent-conjecture / experiment-child distinction special-pleading — a device whose only function is to keep a favored conjecture alive?** The objection is recorded here, not deflected, because the reframe is exactly the kind of move that *should* attract it.

**The objection, stated at full strength.** The parent/child split makes a conjecture structurally hard to falsify: any refutation can be absorbed as "the *operationalization* (child) was wrong, the *idea* (parent) is sound," and the parent walks away each time. A vocabulary in which the load-bearing claim can never be the thing that fails is, on its face, "a vocabulary that cannot lose" (`MEDITATION_QUESTIONS.md` #1).

**The review's verdict: sound, not special-pleading — with one honest residual limit.** Three findings carried it:

1. **The structure is named as the tension, not hidden behind it.** The reframe does not quietly *use* the parent/child asymmetry to protect the claim; it *foregrounds* it as the central problem (§2.1, §0; `MEDITATION_QUESTIONS.md` #1; the specimen's `discrepancies[1]`). §2.3 and §5 say outright that the reframe **does not rescue** parents-produce-W_C — it makes its weak standing legible. A special-pleading device argues the claim *survives*; this one argues only that the surviving is now *auditable*, and reports the claim as a parent under **heavy** friction with **zero** surviving real-corpus child.
2. **The dead-children tally converts the objection from alleged to measured, and creates real pressure.** The anti-gaming clause (§3.4) is what does the work: demotions are append-only + dated, a reinterpreted revival does **not** reset the dead count, and "refine the estimator again" **costs +1 dead child every time.** So friction accumulates *monotonically and visibly* — the move the objection fears (endless re-operationalization) is permitted but **priced**, and the price is the gauge. "An unfalsifiable core protected by an auxiliary belt" stops being a rhetorical charge and becomes a **count** (synergy parent: 4 dead + 1 unrun + 0 success).
3. **Refined-Q1 is a creditable, pre-registerable commitment (§4).** Asking an experiment-result to kill a conjecture is a category error that yields a pre-commitment which never fires; asking the conjecture to **pre-name the dead_count at which it parks itself dormant** is a commitment that *can* fire, is dated, and acts on the right object.

**The residual limitation, recorded honestly (this is the discipline that answers the objection rather than the rhetoric).** The tally is today a falsification-**pressure gauge**, not yet a falsification **mechanism**. The pressure bands (§3.3) are qualitative and the auto-park trigger — the forced-retirement rule (`MEDITATION_QUESTIONS.md` #11) — is **PROPOSED-NOT-ADOPTED** (`status: needs-decision`). So "heavy" pressure presently carries **no automatic consequence**: nothing yet *forces* the park. The gap between gauge and mechanism is exactly the unadopted #11 rule, and the self-specimen records it as its own **live open friction** (`_claim_lifecycle_tally._meditation_link`; `fuzzy_layer.frontier`).

**Why recording the limit is the answer.** Special-pleading hides the move that protects the claim; this reframe does the opposite — it **publishes** the one place where protection still outruns consequence, names the rule that would close it, and pre-registers the trigger that rule would fire (§4). The honest net, adopted from the review: *the reframe creates real, monotonic, dated falsification-pressure and is not special-pleading — but it stops one step short of binding consequence, and says so until #11 is ratified.* Until then, the standing framing is kept exactly as the review requires: **"heavy" pressure is a visible signal, not an automatic demotion.**

---

*Tier-3 exploratory. PROPOSED states (`friction-logged`, `parent_dormant_pending_child` / `why_frame: operational`, the `friction_tally` block) are surfaced-for-ratification, promote nothing, and collapse back to existing `SCHEMA_v2.md` fields if rejected. All other states REUSE existing fields (`status`/`status_trajectory`/`lifecycle`/`dormancy_intervals`/`revival`/D6). The cross-substrate convergence list stays **9**. Bits stay qualitative. Demoted/dormant claims stay demoted/dormant; nothing here advances a tier. §6 records the special-pleading objection (Opus review 2026-06-10) and the discipline that answers it; the gauge-not-yet-mechanism limit (the unadopted forced-retirement rule, `MEDITATION_QUESTIONS.md` #11) is held open, not papered over.*
