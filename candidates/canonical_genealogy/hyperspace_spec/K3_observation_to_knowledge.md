# Observation to knowledge, and conjecture-stubs

**Status:** Tier-3 design analysis (SPEC-ONLY). Binds to ratified machinery; does not fork it. Single-agent surface (architect + adversarial hardener) -- owes a cross-model external pass.
**Date:** 2026-06-15
**Scope discipline (held):** this is a TOOL / render-spec analysis, not a framework substantive claim. Convergence list stays 9. No tier promoted. The structure-bit verdicts below are **computable proxies, disclosed as proxies** per `PROXY_SPEC` discipline -- never presented as measurements.

**Binds to (read, not re-derived here):**
- `hyperspace_spec/SPEC.md` sec 0 (the COIN keystone) + sec 7 (`factToLight`: `bits = w_route + log2(1+corroborations) + a*certainty`; `sigma = max(EWA_floor, k*2^-bits)`; 3 additive render channels MEASURED/ESTIMATE/MODELLED) + sec 8 (the one-sentence pixel test).
- `substrate/SUBSTRATE_SPEC.md` sec 3 (certainty rubric), sec 4 (verification state machine: `pending -> corroborated | disputed | unverifiable`), sec 6 (best-value resolution; bucket order `corroborated > pending > disputed`).
- `SCHEMA_v2.md` R5 (`child.status` gains `open-conjecture`; `status_trajectory[]`), D5 (fuzzy-by-design), the OPTIONAL/default-empty design law.
- The ratified CLAIM_LIFECYCLE machinery (parent-fn = conjecture, child-fn = experiment, dead-children tally as the honest falsification gauge; 0.99-not-Boolean; demoted-not-killed).
- Confirmed-current 2026 cites: Epiplexity ([arXiv:2601.03220](https://arxiv.org/abs/2601.03220)), Excess Description Length ([arXiv:2601.04728](https://arxiv.org/abs/2601.04728)).

---

## 0. The one-line thesis

> The OBSERVATION -> MEANING -> KNOWLEDGE ladder is the COIN read **vertically**, in bits, **per wrapper axis**. A rung is a height on the one log's `-log2(bits)` sharpness axis. A conjecture-stub is the **named** version of the blur that the COIN demands wherever the substrate has not paid the bits -- so a fuzzy region is never a silent blank the eye fills in, and a conjecture can **never** render as crisp as knowledge.

Two posted thresholds separate the three rungs, and the renderer is mechanically forbidden from collapsing them. Where a rung is not reached, a **typed conjecture-stub** sits in the gap: a falsifiable hole, dashed not solid, carrying its own expected-value-of-information so the instrument knows where to fire next, and lifecycle-bound to the ratified dead-children tally so the blur is auditable, not decorative.

---

## 1. The ladder in measured_bits, with disclosed thresholds (never collapsed)

The ladder is computed **per axis** of the v0.3 wrapper -- WHAT / WHEN / WHERE / WHO / HOW / WHY each get their own ladder. They are separate sufficiency questions; a fact can be KNOWLEDGE on WHEN and OBSERVATION on WHY at the same time. WHY is blurriest by construction; WHO carries the Stigler cap. The ladder is **never per-fact** -- collapsing it to one rung per fact silently re-collapses the very distinction this analysis exists to keep.

### 1.1 The three rungs

**RUNG 0 -- OBSERVATION (a raw ping).** One keyhole-probe return on an axis. In substrate terms: a single emitted fact (a real fetched source asserting value `v` with emit-time `certainty in [0,1]` per `SUBSTRATE_SPEC` sec 3, `verification = "pending"`). Its bit-content is the emission term of `factToLight` **before any corroboration**:

```
obs_bits(axis) = w_route(route) + a*certainty
```

An observation has never been battle-tested. It can **light** (it is real, it has provenance) but it cannot be **sharp**. One splat, wide and dim.

**RUNG 1 -- MEANING (structure detected, not yet locked).** The probe stream on an axis has accumulated enough that a non-trivial model fits -- structure, not noise. This is the algorithmic-statistics **STRUCTURE gate**: build the two-part code (model `S`, then `x`'s index inside `S`) and watch the computable Kolmogorov structure function `h_x(alpha) = min_{K(S)<=alpha} log|S|` descend. MEANING = "we are below the kink, still extracting" -- a resonance has registered but the model has not absorbed all extractable structure.

The crossing test into meaning is **Excess Description Length** ([arXiv:2601.04728](https://arxiv.org/abs/2601.04728)): a derived WHAT/HOW is genuine structure only if its description costs **fewer** bits than the noise it explains (EDL net-compressive). Below that line it is overfit = a fake measured bit = must be blurred. EDL is the per-channel honesty test in bits.

**RUNG 2 -- KNOWLEDGE (corroborated past a disclosed line).** Two conditions, both required, both in bits:

- **(a) STRUCTURE-COMPLETE.** `h_x(alpha)` has hit the sufficiency line `h_x(alpha) + alpha = K(x)` and gone flat -- the **kink**. The complexity `alpha*` at the kink is the Algorithmic Minimal Sufficient Statistic (AMSS): the exact "stop here, this is all the structure there is" point. Bits past the kink (the flat residual `log|S|`) are **irreducible noise that must render fuzzy**.
- **(b) CORROBORATION-COMPLETE.** Credence has crossed a **posted** level under the substrate's existing justification condition: verification `bucket = corroborated` AND `battle_count >= N_min` independent routes AND `certainty >= c_min`. This is exactly the L0 kernel-admission rule read as the knowledge gate. The corroboration term is what **buys** sharpness:

```
corrob_bits(axis) = log2(1 + independent_corroborations)
```

Note the word **independent**: ten newspapers copying one wire = one projection with ten echoes, not ten corroborations. Use `N_eff` = the information dimension of the projection set weighted by source independence (PubChem-vs-wiki, GSMArena-vs-apple.com is the right instrument precisely because independence is what moves the posterior).

### 1.2 The third ceiling: compute-reach (Epiplexity)

Beyond "is there structure" sits a third question the original COIN did not have: **can a bounded observer compiling in bursts actually reach it within the current budget?** ([arXiv:2601.03220](https://arxiv.org/abs/2601.03220)).

```
reach_bits(axis) <= struct_bits(axis)   always   (you cannot extract more than exists)
```

A region can be fuzzy for a reason that is **neither noise nor lack-of-corroboration**: structure is present (`struct_bits` high) but out of compute reach (`reach_bits` low). The viewer needs a third blur treatment for this, or it tells an epistemic lie -- conflating "we cannot compute it yet" with "there is nothing there."

### 1.3 The render law over all three rungs (the non-collapse guard)

The COIN, sharpened to a **three-ceiling minimum**:

```
rendered sigma(axis) = max( EWA_floor,  k * 2^( - min( struct_bits, reach_bits, corrob_bits ) ) )
```

Sharpness clamps to the **lowest** of the three ceilings. This is the load-bearing forbidden move: **the renderer never reads `obs_bits` or `struct_bits` alone for sharpness -- it always takes the min across all three.** Consequences, mechanical not policed:

- A conjecture (structure present, but `corrob_bits = log2(1+0) = 0`) clamps to `EWA_floor` -> maximally blurred -> **cannot render as crisp as knowledge.** This is "a conjecture must never render as knowledge," enforced by geometry.
- Structure-present-but-compute-unreachable clamps to `reach_bits` -> stays fuzzy **honestly** (a different badge from noise).
- Corroborated-but-structureless (many sources repeating noise, past the kink) clamps to `struct_bits` -> the noise residual stays fuzzy. **Repetition of noise is not knowledge.**

### 1.4 The two thresholds, posted and disclosed

| Threshold | Crossing test (in bits) | What stays below it |
|---|---|---|
| **tau1 (obs -> meaning)** | `EDL(axis) < 0` (model-bits < noise-bits-explained) | a single wide dim splat -- observation only |
| **tau2 (meaning -> knowledge)** | kink reached (`|slope+1| < eps`) AND `bucket = corroborated` AND `battle_count >= N_min` AND `certainty >= c_min` | a conjecture-stub, clamped to `EWA_floor` by the min |

**These two thresholds are genuinely orthogonal axes** -- structure is about the model, corroboration is about independent routes. They can **disagree**: structurally sufficient on few clean observations yet under-corroborated (one route); or heavily corroborated yet structureless (echoes of noise). Knowledge demands **both**; render the disagreement as two distinct badges, never average them into one "confidence."

**Posted values (leaning, disclosed for ratification, not yet locked):** reuse the ratified L0 kernel bar -- `c_min = 0.7`, `N_min >= 1` -- so **knowledge = kernel-admission exactly** (do not invent a second bar), with `battle_count` surfaced so the viewer shows the **degree** of corroboration above the line. WHY may be allowed to close looser than WHO (per-axis dials), but that is an open call (sec 7).

### 1.5 The ladder is not a clean one-pass pipeline [SPEC]

Per the DIKW critique (Fricke), a meaning-structure must pre-exist for an observation to register at all -- a keyhole-probe only excites what the compiled block can already resonate with (spreading activation). So KNOWLEDGE **flows back** and reshapes how new pings are read; the compile is iterative, not one-pass. The "rung" metaphor is a **current-compile snapshot**, not a fixed temporal order. This is a feature (it is exactly FRAME=substrate / GLASSES=observer), but it means a strictly bottom-up obs->meaning->knowledge spec would be wrong, and the ladder must be recomputed as the block compiles.

---

## 2. The conjecture-stub: typed latch-point at a fuzzy axis

A conjecture-stub is the **dual of a measured fact**: a fact wrapper carries positive `measured_bits` on an axis; a stub is the **same wrapper shape** with `measured_bits ~ 0` on that axis, plus a typed discharge-obligation and an attached expected-value-of-information. The COIN already forbids rendering bits you did not measure; **the stub is the renderable NAME for that forbidden region**, so the viewer never leaves a silent blank.

A stub is a **first-class typed hole, not a weak fact.** It is a Skolem term ([arXiv:2509.10837](https://arxiv.org/abs/2509.10837)): a typed function-expression, syntactically distinct from any asserted node (it can never be mistaken for measured), type-constrained on what can bind, open to future binding. Enforced kernel-distinct by a proof-sketch `sorry`-hole discipline (the compiler refuses to **certify** any downstream conclusion while a hole it depends on is open) and an ATMS assumption-set label (so retraction propagates automatically -- demoted-not-killed for free).

### 2.1 The formal object

```
stub = {
  target:    { wrapper_id, axis in {WHAT,WHEN,WHERE,WHO,HOW,WHY} },   # per-axis, never per-fact
  fuzz_type: noise_floor | compute_bound | evidence_bound,           # WHY it is fuzzy; a falsifiable claim w/ its own confidence
  bound:     <typed region>,                                          # interval / box / RCC-zone the true fill provably lies in
  latch_spec: {
     skolem:     skolem(axis, wrapper_id),                            # typed placeholder, type-constrained on what can bind
     candidates: [ { H_i, prior, falsifier_i } ],                     # mutually exclusive latch-points; EACH must carry a falsifier
     discharge_evidence: <what probe / source / compute would close it>
  },
  support:   { measured_bits ~ 0, conformal_interval },               # calibrated sharpness, NOT a Boolean (UnKGCP arXiv:2510.24754)
  evi:       <expected bits gained if discharged> / cost,             # the EIG-per-cost that aims the next burst
  provenance_label: ATMS assumption-set,                             # conjecture assumptions count ZERO bits
  epistemic_type:   grounded|ungrounded|contradicted|complementary,  # GSAR gate; tool-observed outranks model-inferred
  status:    conjecture | under_test | corroborated | demoted | retired,
  created_by, compiler_time
}
```

### 2.2 The three-way fuzz typing (the genuinely new contribution)

The single most important distinction: a stub is fuzzy for one of **three provably-different reasons**, and the type determines whether the stub can ever be filled.

| `fuzz_type` | Diagnosis (in bits) | Can a probe fill it? | Render reading |
|---|---|---|---|
| **noise_floor** | kink reached; residual provably structureless (`struct_bits` is the binding ceiling) | **No.** More probes waste budget (EIG ~ 0). | terminal blur that never sharpens |
| **compute_bound** | structure demonstrably exists (`struct_bits > reach_bits`, the Epiplexity gap) | **By more compute / a better coder**, not more data. | fuzzy, distinct badge from noise |
| **evidence_bound** | structure exists and is reachable; no keyhole has fired at it yet (`corrob_bits` binds) | **Yes -- the legitimate target of active learning.** | dashed hole with ghost-fork candidates |

**Mislabelling is the central danger.** Mislabelling `evidence_bound` as `noise_floor` hides a fillable hole (a silent dead spot -- the instrument permanently stops looking at recoverable structure). Mislabelling `noise_floor` as `evidence_bound` burns the probe budget forever on a noise floor. So **the type is itself a falsifiable claim and carries its own confidence.** This three-way typing is what is new beyond the prior keyhole_block takes, which typed stubs only by *which axis* is missing, not by *why* it is fuzzy.

### 2.3 The three-rule render contract (so a stub can never silently harden)

1. **NEGATIVE-SPACE GRAMMAR.** A stub uses a render grammar **disjoint** from facts. Facts are solid Gaussian splats (`sigma = 2^-measured_bits`); stubs are an outline / dashed-dithered hollow region with **no interior fill**. The diagnostic: zoom into a fact and you get detail; zoom into a stub and you get **empty space inside its bound** -- the inverse of a splat (a fact accumulates radiance toward its center; a stub is a ring with a void). This is the limiting case of the ratified ESTIMATE channel at `measured_bits -> 0`, plus a falsifier badge.

2. **NEVER-INTERPOLATE.** The COIN forbids fabricating a missing bit, so a stub is **never** filled by interpolating its neighbours. The sharpest test (the presentism leak): an unmeasured `t_event = 1900` value on a drifting concept must render as a blurry box that **contains** the true 1900 vector -- never a sharp average of 1850 and 1950. An honest instrument emits the bounding box and flags internal variance as unmeasured bits; a leaking one emits a sharp wrong average. The aggregation-faithfulness inequality already in the spec (`rendered_bits(parent) <= measured_bits(children) - bits_discarded`) is the same law one rung up: a parent stub cannot render crisper than its measured children.

3. **ALWAYS-SHOW-THE-FALSIFIER.** A stub that cannot display what would discharge it is **not a stub** -- it is a note/prior, and must be re-tagged. The falsifier **is** the render: the dashed candidate latch-points are drawn as ghost-forks emanating from the bound.

### 2.4 The hardening leak, closed by construction

A stub hardens only by **importing bits it never paid for**, through three named channels:

- **Woozle** (evidence-by-citation): a stub repeatedly cited becomes load-bearing. **Closed by support-label directionality** -- `measured_bits` depends on the node's own evidence **leaves**, not its in-degree, so cite-edges cannot enter the ATMS label.
- **Resurrection**: a demoted child's bits re-attach to its live parent. **Closed by append-only versioned memory** (Kumiho-style, [arXiv:2603.17244](https://arxiv.org/html/2603.17244v1)) with AGM Recovery rejected + dead-child content-hash + an AnalyzeImpact cascade that re-floors downstream bits on demotion. The tally only ever grows.
- **Laundering**: an adjacent real fact is bound to a stub it does not actually support. **Closed by entailment-not-similarity** (a symbolic consistency gate) + provenance-disjoint routes counted once.

Because `measured_bits` is summed **only over reconstruction-verified evidence leaves** (conjecture assumptions = zero), a stub floors near zero and the COIN forces terminal blur. **Hardening is impossible by construction, not policed.** The inequality `rendered_sharpness <= measured_bits` is the conservation law; the EDL + kink + at-least-one-disjoint-verified-leaf check is the per-node conservation audit.

### 2.5 The lifecycle (binds 1:1 to the ratified CLAIM_LIFECYCLE -- this is the load-bearing reuse)

- **A stub IS a parent-fn instance.** The stub = a parent conjecture `W_conj` ("there is a fillable value of axis A here"). Its status starts at the ratified `open-conjecture` state (`SCHEMA_v2` R5: `child.status` gains `open-conjecture`, the "live-unconsummated-weld").
- **A probe/experiment IS a child-fn.** Firing a keyhole-burst at the stub = welding a child experiment `W_exp = pushout(W_conj welded to a method-parent W_probe)`. The child is disposable; the parent (the hole) is durable.
- **DISCHARGE = CORROBORATE.** If the burst returns `measured_bits` that move the conformal interval past the posted credence under independent corroboration (the Bayesian threshold) AND past the AMSS kink (the structure threshold) AND the structure is compute-reachable (the Epiplexity threshold), the stub **closes**: it becomes a measured axis, status `corroborated`, the Skolem term binds to a real value, and the dashed ghost renders as a solid splat -- **up to the kink only.** Corroboration is monotone-not-Boolean (Popper / Hume-to-Jaynes, [arXiv:2511.02881](https://arxiv.org/abs/2511.02881)): the stub never reaches certainty, it crosses a posted line and retains a residual blur floor (`sigma` never goes fully to 0).
- **FAILED PROBE = DEAD CHILD, not dead stub.** If the burst fails to move the posterior, the **child** (that probe operationalization) is demoted/retired and **counted**, but the **stub-parent survives**, now dormant-pending-a-better-child, with friction +1. This is the ratified asymmetry exactly: a child can fail without the parent failing.
- **DEAD-CHILDREN TALLY = the honest gauge** (ratified, with the anti-gaming clause transferred verbatim). Each stub carries `friction_tally { dead_children[], dead_count, live_count, best_result_so_far, revisit_trigger, pressure_reading }`. Append-only dated deaths; a reinterpreted re-probe does **not** reset the count; "fire another probe at it" costs +1 dead child every time. `pressure_reading` bands: none / normal / accumulating / heavy / critical.
- **DEMOTE-TO-NOISE-FLOOR is the stub-specific demotion.** A stub under heavy/critical pressure (e.g. `>= 3` dead evidence_bound probes, 0 live, stalled high-water mark) is **re-typed** from `evidence_bound` to `noise_floor`: the honest reading "we have fired enough independent keyholes and the bits are not there; treat this as irreducible blur." This is the falsifiable, pre-registerable commitment -- name the `dead_count` at which you stop probing. **Caveat:** re-typing to `noise_floor` is itself a claim with confidence < 1 (the noise-floor verdict is non-computable; see sec 5), revisitable if a new instrument/coder arrives -- so it is `dormant-noise-floor`, **not killed.**

---

## 3. Active aiming: fuzzy regions choose the next keyhole-burst

This makes Pav's intuition formally exact: **the fuzzy region IS argmax-EIG.** The shortfall to an axis's kink, `gap_a(z) = bits_kink_a(z) - bits_a(z)`, is both how blurry the region must render **and** how much information a probe there can yield. Blur is simultaneously the honesty badge and the targeting fuel.

The loop, bound to the substrate at `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate\`:

1. **READ THE DEFICIT MAP.** `compile_substrate.py` already resolves each `(specimen, subject_id, predicate)` to a best value + bucket + certainty. Lift to per-axis `measured_bits` via `factToLight`; per axis `sigma_a = 2^-bits_a`.
2. **LOCATE THE KINK PER AXIS.** Use the already-built pinned-coder two-part-code MDL harness (tasks #25/#32) as the computable proxy for the non-computable randomness-deficiency verdict. `bits_kink_a = alpha*_a` at the kink.
3. **TYPE EACH STUB** by which ceiling binds (sec 2.2). Only `compute_bound` and `evidence_bound` stubs are probe targets; `noise_floor` is not.
4. **SCORE EVERY FILLABLE STUB BY EIG-PER-COST.** `P_next = argmax_P EIG(P)/cost(P)`, with four refinements from the active-learning literature:
   - **(a) Score against an EXPLICIT compiled posterior** (the compiling block-universe), **NOT** chat/probe history -- the central BED-LLM warning ([arXiv:2508.21184](https://arxiv.org/abs/2508.21184)).
   - **(b) Aim at PREDICTIONS, not parameters** (EPIG, [arXiv:2304.08151](https://arxiv.org/abs/2304.08151)): target the observer's question (the GLASSES / WHOM axis), with pool != test = the FRAME-vs-GLASSES split. Compute EIG toward what the observer asked, or you sharpen WHATs nobody asked about.
   - **(c) Do not be greedy:** per-probe greedy EIG is myopic; score against a contrastive **lower bound** on total information gain over the **whole burst** (DAD's sPCE). This lower-bound discipline is **identical to the COIN**: never claim more resolved bits than you can certify.
   - **(d) Use an honesty-preserving estimator** (IPM-BOED Wasserstein/MMD/Energy, [arXiv:2604.21849](https://arxiv.org/abs/2604.21849)) **not KL**, because classical KL-EIG is a log-density-ratio that underestimates tails and rare events -- it will pretend it measured bits it did not (a fake measured bit) precisely at the fuzzy regions you aim at, which the COIN forbids.
5. **FIRE A BURST, NOT ONE PROBE.** BADGE (gradient-embedding: magnitude = fuzziness, k-means++ over directions = axis/region diversity) + BatchBALD redundancy correction, so many keyholes hit **different** stubs at once, not all the same spot.
6. **UPDATE, LOCK, OR RE-STUB.** New bursts arrive as **append-only** facts (never mutate `B*`; only raise `measured_bits` about a fixed past). Recompile; run AnalyzeImpact cascade over the typed-edge DAG to re-evaluate every downstream node the burst touched. Then LOCK (knowledge), DEMOTE a contradicted candidate to dead-child (logged, not deleted), or RE-STUB the residual fuzz (spawn the next typed stub). The loop self-directs indefinitely; it halts a region only at a `noise_floor` stub or budget exhaustion.

**VALENCE = the third coin = EIG.** Each stub's curiosity-valence is its expected information gain; the viewer fires the **highest-valence** burst (the active-inference epistemic-value framing). The viewer is therefore not a passive display of the block -- it is a **self-directing epistemic instrument** whose every aim is bounded by the same inequality that bounds every pixel.

**Render the aim:** show the EIG field as a heat-map -- bright = where the instrument wants to look next. Firing is **badged as a back-reaction** (choosing the probe partly defines the construct in a live social substrate -- participatory, not passive).

---

## 4. The honesty guard: stubs never harden silently

This pulls together the guarantees scattered above into one contract:

- **The min-clamp (sec 1.3)** mechanically forbids a conjecture (corrob_bits = 0) from rendering as crisp as knowledge. Not a label -- geometry.
- **Negative-space grammar (sec 2.3 rule 1)** makes a stub visually un-confusable with a fact: a stub is a void, a fact is a filled splat.
- **The three hardening-leak closures (sec 2.4)** stop bits being imported by citation (Woozle), resurrection, or laundering -- because `measured_bits` is sourced **only** from reconstruction-verified, route-independent evidence leaves, counted once.
- **The falsifier-mandatory rule (sec 2.3 rule 3)** demotes any falsifier-less "stub" to a mere note/prior.
- **The dead-children tally (sec 2.5)** with the anti-gaming clauses is the auditable record that the blur is honest -- every failed probe is a dated, append-only dead child; re-probing costs +1 every time.
- **The provenance gate (GSAR four-way typing + WHO-asserted tag).** Machines collapse belief / justified-belief / knowledge: post-May-2024 LLMs are 34.3% worse at flagging a **false** belief than a true one despite ~91% fact accuracy (Zou et al., Nature Machine Intelligence). A stub's candidate latch-points are often LLM-proposed; without the ATMS assumption-set label + GSAR epistemic type (grounded/ungrounded/contradicted/complementary, [arXiv:2604.23366](https://arxiv.org/abs/2604.23366), tool-observed outranking model-inferred), a model-**inferred** candidate would render with the same grammar as a tool-**observed** one, and the viewer would render a fake measured bit. The provenance type **gates every candidate** before it can sharpen a stub.

**The one-sentence test, verbatim from SPEC sec 8, is the promotion criterion:** *"Did the substrate pay the bits for this sharpness?"* If no -> blurrier / dimmer / dashed / badged, or not drawn. Meaning becomes knowledge at exactly the point where the substrate has paid the bits.

---

## 5. SPECULATION (disclosed)

> Register shift: the items below are not derived from the digests or the ratified spec. They are out-of-box conjectures, marked [SPEC], offered as latch-points themselves -- each is a stub the reader can probe or kill.

- **[SPEC] A fourth fuzz_type: `horizon_bound`.** The three types cover "no structure," "structure out of compute reach," and "structure not yet probed." But there is a recursive case: a stub whose own **discharge-evidence is unknown** -- we cannot even name the probe that would fill it. No EIG can be computed for it (`evi` is undefined, not just low). This may deserve its own terminal type, distinct because it cannot enter the active-aiming argmax at all. It is the formal home for "unknown unknowns." Open whether it is a real fourth type or just `evi = undefined` on an `evidence_bound` stub.

- **[SPEC] An UNKNOWN-UNKNOWN meta-stub against frame entrenchment.** Pure EIG-driven aiming sharpens only what the current GLASSES can already ask about -- it starves structure that needs a vocabulary the observer does not yet have. A meta-stub spawned where **compression plateaus but corroboration is high and stable** (a structure-resistant region) would flag "the current glasses may be missing an axis here." This is the formal hedge against the instrument entrenching its own blind spots. Reserve a small exploration budget aimed at high **global** uncertainty (frame-relative, BALD-style), not just GLASSES-relevance.

- **[SPEC] Second-order blur: rendering the fuzz_type's own uncertainty.** The `fuzz_type` is a falsifiable claim with confidence < 1. An `evidence_bound` stub that **might** be `noise_floor` is epistemically different from one we are confident is fillable. Should the viewer render a "blur on the blur" -- a second-order texture encoding type-confidence? Risk: an unreadable hall-of-mirrors. Candidate resolution: render type-confidence as **border texture** (solid dashes = confident type, dithered dashes = uncertain type), keeping the interior void grammar intact.

- **[SPEC] An observer-effect term in the cost function.** In a **live** social substrate, firing a probe at "who founded X" is itself causal -- naming a candidate feeds the concept's own spread, changing `B*` not just `B_hat`. The participatory badge **discloses** this, but the EIG estimator does not yet **model** its own causal footprint. A fully honest controller might price `minimise distortion-of-target` into the design score alongside `maximise info-gain`. This may be the line between an honest instrument and a manipulative one. Corollary: discount **self-induced corroboration** -- a provenance-direction FROM-link marking instrument-surfaced instances, excluded from the independence count.

- **[SPEC] Frame-locked noise-floor verdicts.** Per the heredity/frame-relative-classifier work, a frame toggle can reveal structure that was noise in another frame. So a `noise_floor` stub in frame F may be a `compute_bound` stub in frame F'. "Provably no more bits" should perhaps always be **frame-scoped** (carry the frame it was computed under), never absolute -- which would make the noise-floor verdict revisitable on a frame change, not only on a coder upgrade.

---

## 6. QUESTIONS WE SHOULD BE ASKING

> Register shift: these are meditation-level questions about whether the apparatus is even pointed the right way -- not tasks, not settled design calls.

- **Is "knowledge" the right top rung, or is it a way-station?** The ladder stops at corroborated-structure-compute-reachable. But the DIKW critique says knowledge flows **back** to reshape reads. If the top rung re-enters at the bottom (knowledge becomes the meaning-structure that lets the next observation register), the ladder is really a **loop**, and "the top" is an artifact of taking a snapshot. Are we drawing a ladder when the honest object is a compiling cycle?

- **Are we measuring the bits we can measure, or the bits that matter?** EIG aims at the observer's question (EPIG). But the most truth-critical gap may be one the observer did not think to ask about. An instrument that is perfectly honest about `rendered <= measured` can still be **systematically blind** -- never lying, never looking where it counts. Is honesty-of-render a sufficient virtue, or do we owe a separate account of **coverage**?

- **Whose kink is it?** The AMSS kink is computed under a pinned coder. A sharper coder moves the kink. So "this is irreducible noise" is always **coder-relative**. When two coders disagree on where the kink sits, do we render the **disagreement as visible texture**, or collapse to the more generous coder (risking a fake bit) or the stingier one (risking a missed bit)? The choice is itself an epistemic stance we have not posted.

- **Does naming a stub make it real?** In a live substrate, surfacing "who really founded X" partly **creates** the answer (attention is causal). If the act of stubbing back-reacts on the substrate, is the instrument still observing, or has it become a participant whose corroborations are partly self-fulfilling? Where is the line between an honest probe and a leading question?

- **Can a stub be honest about being a metaphor?** Pav's "block universe that compiles in bursts" is load-bearing intuition. At what point does the metaphor itself need a stub -- a typed hole that says "we are using a CT-tomography model of a thing that may not be tomographable" (concept drift rotates the latent basis; the Radon math hallucinates coherence across a rotated frame)? The deepest honesty guard may be a stub **on the apparatus**, not on the data.

---

## 7. Open sub-questions for Pav

1. **Posted thresholds:** ratify `c_min = 0.7`, `N_min >= 1` so **knowledge = kernel-admission exactly** (don't invent a second bar)? And per-axis dials (WHY closes looser than WHO) or one global level?
2. **Forced re-type:** should `evidence_bound -> noise_floor` at "critical" pressure be **automatic** (binds the unadopted forced-retirement rule, makes the stub falsifiable-by-mechanism) or stay **human-gated** (avoids a too-aggressive coder declaring noise floors prematurely)? Same gauge-vs-mechanism call the ratified claim-lifecycle left open, now inherited by the stub.
3. **Fourth fuzz_type:** is `horizon_bound` (a stub whose own discharge-evidence is unnameable, `evi` undefined) a real type, or just `evi = undefined` on an `evidence_bound` stub?
4. **Settling experiment:** approve the minimal toy -- a hidden block with a **known** noise-floor region and a **known** fillable region; success = the compiler types them correctly, fires probes ONLY at the fillable one, re-types fillable->corroborated and unfillable->noise_floor after the pre-registered `dead_count`, and **never interpolates a fake sharp value** into either.
5. **Two ledgers or one:** keep measured-route bits and social-consensus bits (the WHO/Stigler axis) as **permanently separate channels** the COIN caps independently, or allow them to sum? (Leaning: permanently separate -- consensus is a distinct provenance class.)
6. **External pass:** this is single-agent. Run the GPT-5.5 + Gemini cross-model pass on the three load-bearing moves (the min-clamp non-collapse guard; the three-way fuzz typing; the stub-as-parent-fn lifecycle reuse) before any ratification.

---

**Files this analysis binds to (all absolute):**
- `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\hyperspace_spec\SPEC.md` (sec 0 keystone, sec 7 `factToLight`, sec 8 pixel test)
- `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate\SUBSTRATE_SPEC.md` (sec 3 certainty rubric, sec 4 verification state machine, sec 6 best-value resolution)
- `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\SCHEMA_v2.md` (R5 `open-conjecture`, D5 fuzzy-by-design, OPTIONAL/default-empty design law)
- `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\PROXY_SPEC.md` (honest-proxy discipline; per-channel falsification target)
- `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate\compile_substrate.py` (the deficit-map source for active aiming)

*This is a SPEC-ONLY analysis. Nothing here is built. The structure-bit verdicts are computable proxies disclosed as proxies; no fact's sharpness was changed; the convergence list stays 9; no tier is promoted.*
