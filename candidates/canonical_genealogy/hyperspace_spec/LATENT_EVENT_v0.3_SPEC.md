# LatentEvent v0.3 — the unifying record of the global substrate

**Status:** SPEC-ONLY (nothing built). Tier-3 design. **Binds to ratified machinery; does not fork it.**
**Date:** 2026-06-21. **External pass:** the load-bearing moves (per-axis bits, the conjecture-fan, the
geometric min-clamp, the uncertainty type-system) carry an opus + Gemini-3.1-pro cross-model pass
(`session_arc/{opus,gemini}_conjecture_review.md`) — this is the pass K3 sec7.6 owed.
**Discipline (held):** a TOOL / render-spec, not a framework substantive claim. Convergence list stays 9. No
tier promoted. Every bit-verdict is a computable proxy disclosed as a proxy (PROXY_SPEC). Demote-not-kill.

**Binds to (read, not re-derived):** `SCHEMA_v2.md` (the genealogy record; recursion via `sub_wrappers`; the
frame `{time,space,knowledge,meaning}`; `frame_layer` physical/latent; `actors`; `lifecycle`; `candidate_children`;
`harvest/descendants`; the OPTIONAL/default-empty design law) · `K3_observation_to_knowledge.md` (the per-axis
OBS->MEANING->KNOWLEDGE ladder; the typed conjecture-stub; the three-ceiling min-clamp; 3-way fuzz typing;
EIG-per-cost active aiming; the dead-children lifecycle) · `SPEC.md` sec0/7/8 (the COIN; `factToLight`; the 3
render channels MEASURED/ESTIMATE/MODELLED; the one-sentence pixel test) · `SUBSTRATE_SPEC.md` sec3/4/6
(certainty rubric; verification state machine; best-value resolution) · the **Model Cost Stack** (the BUILD
iceberg) · the **contracts reframe** (one protocol, many contracts; cross-contract blurred) · the **DAG+KG-RAG
backbone** (`GAPS_AND_BACKBONE.md`).

---

## 0. One-line thesis
> A **LatentEvent** is the fractal, COIN-honest record of one event/artifact: a **tip of an iceberg** whose six
> content axes (who/what/where/when + the why/how edges) each recurse into their own sub-iceberg, each carry their
> own measured bits + conjecture-fan + canon-lifecycle, observed through a declared contract (WHOM). The MEASURED
> half is what we have paid bits for (sharp, above the waterline); the GENERATIVE half is the weighted-conjecture
> fan that names the blur where we have not (below the waterline). The **COIN is the waterline; the present is the
> waterline in time.**

The same record holds a rival LLM's digestion, a historical weld, a competing theory, and a clashing belief —
they differ only in which axes carry bits and which carry conjecture-fans.

---

## 1. The record (the formal object)

```jsonc
LatentEvent = {
  // --- IDENTITY ---
  "event_id":        "<arena>:<slug>:<NNNN>",          // disjoint namespace per arena
  "arena":           "genealogy|digestion|wrapper_class|dynamic|organ|concept|provenance|rival_theory|belief",
  "contestant_name": "<human label>",

  // --- THE FOUR INTRINSIC AXES (node-local point-in-spacetime properties) ---
  "who":   AxisCell,        // the agent / subject / actor
  "what":  AxisCell,        // the content / kernel / claim
  "where": AxisCell,        // the spatial / physical locus
  "when":  AxisCell,        // the temporal locus (t_event)

  // --- THE TWO EXTRINSIC AXES (relational -> DAG edges, NOT local fields; Gemini's correction) ---
  "why": {                  // WHY runs BOTH ways down the worldline:
    "cause":     [Edge],    //   backward edges to causes/parents (often itself conjectural)
    "delivered": [Edge],    //   forward MEASURED edges to realized consequences (sharp where the future arrived)
    "aims":      ConjectureFan   // forward conjecture-fan: intended/projected purpose (blurry; collapses to
                                 //   `delivered` as the keyhole streams forward and history discharges it)
  },
  "how": ProcessTrail,      // THE VERB: the reflexive casting+canonizing process by which this tip connected to
                            //   its iceberg (which probes fired, EIG-aimed, canon-resolved). Itself recursable.

  // --- THE OBSERVER (WHOM) — an ARRAY; the contract attaches here (one protocol, many contracts) ---
  "whom": [ {
    "observer":  "<who measured/asserted this>",
    "contract":  { "coder":..., "era":..., "model":..., "frame": ["time"|"space"|"knowledge"|"meaning"] },
    "t_obs":     "<ISO>",                              // the SECOND timeline (when a keyhole measured it)
    "extraction_confidence": <0..1>
  } ],

  // --- FRAME + LAYER (from SCHEMA_v2) ---
  "frame_layer": { "layer": "physical|latent|straddle", "physical_membership": <0..1>, "latent_membership": <0..1> },

  // --- DERIVED RENDER (computed in COMPILE; stored as provenance-of-intent, NEVER hand-authored) ---
  "render": { "<axis>": { "sigma": <from the min-clamp>, "grammar": "splat|negative-space-void", "channel": "MEASURED|ESTIMATE|MODELLED" } },

  // --- EVENT-LEVEL LIFECYCLE (each AXIS also carries its own; this is the rollup) ---
  "lifecycle":  "ratified|corroborated|pending|spec-only|demoted|resolved|un-demoted|dead",
  "demotions":  [ { "dc_id": "<era-namespaced>", "from":..., "to":..., "flagged_by":..., "date":... } ]
}
```

### 1.1 `AxisCell` — every axis is its own iceberg (Pav: depth + canon-lifecycle)
An axis is **not a leaf string.** It is a tip that points into its own sub-structure and runs its own lifecycle.

```jsonc
AxisCell = {
  "value":     <scalar | EdgeRef to a sub-LatentEvent>,   // a pointer => the iceberg BELOW this axis (recursion)
  "depth_ref": "<event_id of the sub-iceberg this axis expands into, or null at a leaf>",  // LOD / SCOPE_NESTING

  // the MEASURED half (K3 per-axis ladder, in bits):
  "measured": {
    "measured_bits": <n>,                 // summed ONLY over reconstruction-verified evidence LEAVES (not in-degree)
    "signal_type":   "reasoning_tokens|markers|mdl_bits|residue_bits|nli|none",
    "struct_bits":   <n>,                 // is there structure (EDL net-compressive; the AMSS kink)
    "reach_bits":    <n>,                 // is it within compute reach (Epiplexity)
    "corrob_bits":   <log2(1+N_eff)>      // independent corroboration (N_eff, not raw count)
  },

  // the GENERATIVE half (K3 typed conjecture-stub) where measured_bits ~ 0:
  "conjectures": ConjectureFan,

  // this axis-claim's OWN canon-lifecycle (Pav: each axis has its own):
  "lifecycle":   "conjecture|under_test|corroborated|demoted|retired",
  "friction_tally": { "dead_children": [], "dead_count": 0, "live_count": 0, "best_so_far": null,
                      "pressure_reading": "none|normal|accumulating|heavy|critical" }
}
```

### 1.2 `ConjectureFan` — the named blur (binds K3 sec2.1, the typed stub)
```jsonc
ConjectureFan = {
  "fuzz_type":  "noise_floor | compute_bound | evidence_bound",   // K3 3-way: WHY it is fuzzy -> can a probe EVER
                                                                  //   fill it. Mislabel = burn budget OR hide
                                                                  //   recoverable structure. Itself a claim w/ conf<1.
  "bound":      "<typed region (interval|box|RCC-zone) the true fill provably lies in>",
  "candidates": [ {                       // mutually-exclusive latch-points -- the FAN. Stays a fan until discharged.
    "reading":       "<the conjectured fill>",
    "skolem":        "skolem(axis, event_id)",      // typed placeholder, kernel-distinct from any asserted node
    "weight":        <0..1>,                          // INTRA-fan vote only (sum=1) -- NEVER touches sharpness
    "tag":           "conjectured|modelled|estimated",
    "epistemic_type":"grounded|ungrounded|contradicted|complementary",  // GSAR; tool-observed outranks model-inferred
    "falsifier":     "<what would refute this candidate>",   // MANDATORY -- a fan w/o falsifiers is a note, not a stub
    "followup":      "EXPECT_EVENT(<executable predicate the keyhole stream hashes against>) -> discharges|kills"
  } ],
  "evi":          "<EIG-per-cost: expected bits gained / cost -- aims the next keyhole-burst>",
  "atms_label":   "<assumption-set; conjecture assumptions count ZERO bits>",
  "status":       "conjecture|under_test|corroborated|demoted|retired"
}
```

---

## 2. The render law (the COIN, two levels) -- honesty by GEOMETRY, not policy

**2.1 Per-leaf (K3 sec1.3 three-ceiling min-clamp):**
```
rendered_sigma(axis) = max( EWA_floor,  k * 2^( - min( struct_bits, reach_bits, corrob_bits ) ) )
```
A conjecture has `corrob_bits = log2(1+0) = 0`, so the min pins it to `EWA_floor` -> **maximally blurred -> cannot
render as crisp as knowledge.** Not a label the compiler checks -- a geometry the formula cannot escape.

**2.2 Aggregation faithfulness (the second COIN -- the corpus's most-cited missing half):**
```
rendered_bits(parent) <= SUM over children( measured_bits ) - bits_discarded     (per axis, with spread-of-means + N_eff)
```
A zoomed-out aggregate may never render crisper than the children it is made of. Enforced in COMPILE + RENDER.

**2.3 Negative-space grammar:** a fact is a filled Gaussian splat (`sigma = 2^-measured_bits`); a conjecture is a
**dashed/dithered VOID** with no interior fill, ghost-forks for its candidates, a falsifier badge. Zoom a fact ->
detail; zoom a stub -> empty space inside its bound. **Never interpolate** (an unmeasured 1900 value renders as a
blurry box *containing* the truth, never a sharp average of 1850 and 1950).

---

## 3. The uncertainty TYPE SYSTEM (four scalars, NEVER one blended number -- both reviewers)
| scalar | what it is | its ONE job | may it touch sharpness? |
|---|---|---|---|
| `measured_bits` | information actually paid for | sets **maximum sharpness** | YES -- the only thing that buys focus |
| `contract_validity` | frame/observer distance (WHOM) | render **permission** (use bits un-blurred?) | as a GATE, never a multiplicand |
| `conjecture_weight` | intra-fan vote (sum=1) | picks the **leading candidate** for the UI | **NO -- voting only** |
| `confidence` (3 badges) | struct / reach / corrob, composed by **MIN** | **probability** of the gap-fill | NO (renders as 3 distinct badges, never averaged) |

**Render consequence:** only physical bits dictate FOCUS; conjectures dictate **COLOR / SHAPE** (a vivid ghost is
still out of focus). Blending these four is the "one false board" laundering, re-created inside one record.

---

## 4. WHY in depth (Pav's split) and the iceberg dynamic
WHY is forward-facing, and splits along the arrow of time x the measured/generative line:
- **`why.cause`** (backward edge) -- the motive/cause; often conjectural (we *infer* why).
- **`why.delivered`** (forward MEASURED edges) -- what it actually delivered downstream. **Sharp for historical
  events** (the forward light-cone is filled in by now); it IS the genealogy's UP / `harvest` / `descendants`.
- **`why.aims`** (forward ConjectureFan) -- what it is *trying* to do; **conjectural** (the fan), each aim a stub
  whose falsifier is "did it deliver X?".

**The dynamic (the camera watching the future arrive):** each `aim` is a forward stub. As the keyhole streams
forward, an aim either **discharges** (it delivered -> hardens into a `delivered` measured-edge; ghost-fork ->
solid line) or **dies** (-> dead child, counted not deleted). So the predict-half **resolves into the measured
half along the worldline.** A 1790 event's aim-fan is mostly already collapsed; a live 2026 event's is wide open.
**Blur on WHY = how much of the forward light-cone is still unrealized** -- which is why WHY honestly closes
looser than WHO: part of WHY is structurally in the future.

This **reconciles the two reviewers:** WHY is a forward *edge* (Gemini) that is *measured* where delivered and a
*fan* of candidate edges (K3) where still only aimed. The fan hardens into a solid edge as history delivers it.

---

## 5. Depth, HOW, and the iceberg (Pav)
- **Every axis recurses** (sec1.1 `depth_ref`): zoom into any axis of any event and find a full sub-LatentEvent
  with its own six axes, bits, fan, lifecycle. The substrate is **self-similar** (SCHEMA_v2 `sub_wrappers`; LOD).
- **HOW is the verb, not a content-axis.** who/what/where/when/why = what the iceberg is MADE OF; HOW = the
  reflexive PROCESS that connected the tip to the iceberg (the casting = active-aiming; the canonizing =
  entity-resolution + the lifecycle). HOW is itself an iceberg (the build-history -> the **Model Cost Stack**
  generalized to every artifact; `acts.jsonl`/`arcs.jsonl` are HOW recording itself).
- **Casting:** a fresh event enters as Rung-0 (one splat, the tip). Active-aiming (argmax-EIG) fires keyholes
  **backward/down** (causes, provenance -> the causal iceberg connects) and reads **forward/up** (delivered +
  aims). **Waterline = the COIN** (above = paid-for sharp structure; below = the dark un-probed iceberg; blur =
  how much is still submerged). **Present = the waterline in time.** No bottom: you can always cast deeper
  (toward the Big Bang / cost-stack L17).

---

## 6. The backbone (from the crawl) and federation
- **DAG** = the structural source-of-truth: lineage/welds/`why.cause`/`why.delivered` edges, **acyclic-to-present
  with a compiler no-cycle check**; genuinely cyclic edges (couplings, forcing-feedback, back-reaction) live in a
  **bounded cyclic OVERLAY** excluded from topo-sort, rendered as first-class diamonds.
- **KG-RAG** = the retrieval/use layer = **spreading activation along typed edges** (the keyhole probe; the
  predict-half prior-cut subgraph). **NOT a vector store**; embeddings stay an instrument inside the canonicalizer,
  gated behind the (unbuilt) NLI instrument, only for what/how axes, **never why**. The latent/meaning lane renders
  **blurred until NLI exists.**
- **Federation:** keep source-of-truth stores; `compile_global.py` unions them into one iterable `LatentEvent`
  view with per-contract validity. Cross-contract joins render blurred or are **compiler-refused.**
- **Anti-laundering:** the geometric min-clamp + measured_bits-from-verified-leaves are the primary guard;
  Gemini's dual-RAG payload-bifurcation (`<MEASURED>` vs `<CONJECTURED>`, never promote 2->1) is the **second,
  prompt-policed layer** for the generative phase.

---

## 7. Worked shape (one record, three arenas)
- **Historical weld (Maxwell, ~1865):** who=Maxwell (measured), where=Britain (measured), when=~1865 (measured,
  interval), what=EM-unification (measured), why.cause=[Faraday, Thomson...] (part-conjectural edges),
  why.delivered=[radio, relativity, EM-tech] (MEASURED edges -- the harvest), why.aims=mostly collapsed,
  how=the Maxwellians' canonization trail. WHOM=our harvest-contract.
- **Digestion measurement (deepseek on a prime task):** who=deepseek, what=the task, how=the predicate-application
  (markers as `signal_type`, reasoning_tokens flagged narration-confounded), measured_bits on what/how, WHOM=the
  {OpenRouter, era2, deepseek, frame} run-contract.
- **Live 2026 event:** who/what/where/when measured; why.delivered nearly empty; why.aims a WIDE conjecture-fan
  (the forward cone is open) -- honestly blurry.

---

## 8. The populate mechanism (internet -> LLM-sketch -> harvest -> evaluate)
The internet is the **aggregate**, NOT a test surface. Its three faces map to three roles:
- **archive (<= training cutoff)** -> the **LLM** (its lossy compression) -> the **SKETCH** (the fuzzy first pass / prior),
- **realtime (post-cutoff, verifiable)** -> the **live HARVEST** (the evidence),
- **sentiment** -> the **social-consensus / Stigler ledger** (the second ledger of sec11.2).

**Populate-any-event loop:**
1. **SKETCH (below the waterline).** Fire **n BLIND providers** -> conjecture-fans on the empty axes. Sample the
   net's **DIVERGENCE, not its mode** (a naive n-provider run clusters on shared-prior consensus = a false-tight
   fan). The **divergence-probe family**: `consensus` (the mode) · `forced-counter-consensus` critic (off-mode) ·
   `counter-both` (a third region; "under the rocks") · `personality-primed-roleplay` (the net under a relevant
   persona) · **`interview-the-object/theory`** (personify the LatentEvent as an agent and interrogate it -- the
   chameleon X simulating the event itself). Each candidate carries `elicitation_method` as provenance (a
   forced-divergence or roleplay take is NOT a held position), the asserting provider, and
   `epistemic_type = model-inferred / ungrounded`.
2. **HARVEST (above the waterline).** Search/fetch **independent** realtime/verifiable sources -> measured
   evidence (tool-observed, grounded).
3. **EVALUATE.** Score sketch vs harvest -> **discharge** (corroborate -> becomes measured) or **kill** (dead
   child). The COIN pays the bits.

**HONESTY (load-bearing):** provider **AGREEMENT != corroboration** -- the providers share a training archive
(correlated, like ten newspapers copying one wire); agreement buys **zero** `corrob_bits`, only the **spread** is
informative. The sketch stays pinned to the blur floor (min-clamp, `corrob_bits = 0`) until **independent**
harvest pays for it. Two measurements are recorded and NEVER conflated: *"provider P asserted X"* (measured,
grounded) vs *"X is true"* (conjecture, ungrounded). **Dual-RAG:** sketch in `<CONJECTURED>`, harvest in
`<MEASURED>`, never promoted. **Blind** is the independence that makes the spread honest AND breaks the
hallucination feedback loop.

### 8.1 One-pass two-layer sketch · WHO grounds WHY · cross-origin divergence
- **One pass, the whole iceberg.** The sketch fires the providers ONCE and returns BOTH directions together --
  the backward causes AND the forward projection (sec9), all six axes. Not sketch-past-then-sketch-future.
- **Two layers in the same pass.** Each sketch is simultaneously (a) a **claim about the world** -- conjecture,
  ungrounded, blurred, below the waterline -- and (b) a **sketch-EVENT** -- *measured*: "provider P asserted X at
  `t_obs`, with this divergence and this digestion cost." We **measure the MODELS** (the Latent Olympics datum:
  who-said-what, the spread, the cost) in the very pass we **conjecture the WORLD.** The world-claim stays
  conjecture; the model-assertion is grounded provenance (HOW/WHOM).
- **Scout AFTER; take notes on each model.** Harvest/verify (sec8 steps 2-3) runs after the one-pass sketch; the
  EVALUATE step accumulates a **per-model profile** (the athlete-card, now TOPIC-conditioned: which provider is
  reliable / biased on which topic), keyed by a `provider_origin` tag on the WHOM contract.
- **WHY is the semantic hub; WHO grounds it.** WHY **composes** the others -- "why [for-whom] [what-for] [there]
  [then]" -- so it is the highest-connected, **MEANING-kernel** axis: most important AND fuzziest by construction
  (its blur is the *price* of its semantic reach; it is the latent axis that needs the NLI instrument). **WHO is
  the grounded action-map provenance** (who did/asserted what -- the Stigler/consensus ledger, the physical layer)
  that **bridges to WHY by inference**: read the measured action-map, conjecture the latent motive. WHO grounds
  the otherwise-ungrounded WHY (SCHEMA_v2 actors-as-physical<->latent-bridge). WHO **is** the second (consensus)
  ledger of sec11.2.
- **Cross-origin divergence is a first-class signal.** On a neutral topic the providers converge (V3
  floor-is-provider-invariant); on a **contested** topic they **split by origin** (Chinese / European / US), and
  that split -- the fan's spread decomposed by `provider_origin` -- **measures the topic's contestedness + each
  origin's prior/bias.** COIN-scoped: divergence is conjecture-SPREAD, not truth; the harvest grounds it. The
  multi-provider sketch is thereby also a **bias/contestedness meter.**

## 9. The forward cone (the future half -- the symmetric completion)
The other side of the past is the future. Project a **full future-LatentEvent -- all six axes forward** (future
who/what/where/when/why/how, to whom) -- at three horizons: **SHORT** (near-future; most constrained by the
present; partially realtime-harvestable -> least blur) · **MEDIUM** (partial) · **FUZZY-LONG** (the cone has
widened; only time verifies -> most blur).

The forward cone is **entirely conjecture by construction** (the future is unmeasured -> `corrob_bits = 0` on
every forward axis -> the min-clamp pins the whole cone to the blur floor; it can NEVER render as crisp as a
measured past). **Blur grows with horizon = the forward light-cone widening.** This generalizes `why.aims ->
why.delivered` to ALL axes. The **advancing present (the keyhole = the waterline IN TIME) continuously COLLAPSES
the forward fan**: short-term discharges first (the near-future arrives / realtime confirms), then medium, then
long. **Asymmetry vs the past:** backward-conjectures discharge by **active harvest** (the past exists -- fetch
it now); forward-conjectures discharge only by **passive verification** (wait) + partial realtime-harvest for
short-term. So the forward half's blur is structurally deeper and only time fully resolves it -- "fuzzy long" is
honest, not lazy. **Every event is a tip with TWO icebergs:** backward (causal, mostly measurable for historical)
+ forward (projected, entirely conjectural, collapsing as time arrives). The LLM populates **both** conjecture-
fans (the past from its compressed archive, the future by simulation); **harvest discharges the past fan, time
discharges the future fan.**

## 10. Substrate self-test (dogfooding)
The same multi-provider apparatus is also the substrate's **standing red-team**: a test-mode LLM/council is asked
to try to **launder** a conjectured bit into measured (must fail BY GEOMETRY), navigate/query a lineage,
**interview** an event and confirm the answer renders blurred, attempt an **invalid cross-contract join** (must
be refused), and stress entity-resolution. Failures log as substrate dead-children. The settling toy (sec11.4) is
the first such self-test; this generalizes it to a standing check that the instrument drives as specified.

## 11. Open calls for Pav (K3 sec7 + the dials)
1. **Per-axis close-dials:** WHY closes looser than WHO (the light-cone reason). Confirm per-axis dials, not one
   global level?
2. **Two ledgers:** measured-route bits vs social-consensus (Stigler/WHO) bits -- **permanently separate channels**,
   COIN-capped independently? (Leaning: yes, separate -- matches the contracts reframe.)
3. **Re-type `evidence_bound -> noise_floor`** at critical pressure: **human-gated to start** (pre-register the
   `dead_count`), automate later?
4. **The settling toy experiment** (exercises BOTH loops end-to-end): a hidden block with a *known* noise-floor
   region + a *known* fillable region. **Backward loop:** n BLIND providers sketch the fuzzy (the divergence-probe
   family) -> harvest the planted verified data -> success = the compiler types noise-floor vs fillable right,
   probes ONLY the fillable, **discharges the right candidate and kills the wrong ones, lets provider-AGREEMENT
   alone harden NOTHING** (only independent harvest buys bits), re-types unfillable->noise_floor after the
   pre-registered `dead_count`, and **never interpolates a fake sharp value.** **Forward loop:** project a
   short/medium/long future fan -> advance the clock -> the short-term collapses to measured, the long stays
   blurred. The cheapest proof the whole two-direction instrument focuses correctly before any real harvest.
   **Build next?**
5. **Divergence-probe roster + forward-horizon dials:** which blind-provider configs in the standing roster
   (consensus / counter-consensus / counter-both / roleplay / interview), and the short/medium/long horizon
   cutoffs -- lock now or tune on the toy?

---
*SPEC-ONLY. Nothing here is built. Binds to ratified machinery; forks nothing. The convergence list stays 9; no
tier promoted; every bit-verdict is a disclosed proxy; demote-not-kill throughout.*
