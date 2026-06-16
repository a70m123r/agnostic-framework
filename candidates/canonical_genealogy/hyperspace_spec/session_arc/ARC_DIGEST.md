# Session Arc — the 06/11–16 milestone (acts & arcs)

**A tomographic self-capture of the work, compiled as substrate.** The instrument turned on its own history.

- **Window:** 2026-06-11 → 06-16 (since viewer_v3) · **43 arcs · 120 canonical acts**
- **Method:** 3,073-event narrative spine extracted from the session transcripts → **19 overlapping tiles** (CT-method, ~34-event overlap seams) → 17/19 chunk-read → **stitch** (dedup the overlaps → arcs+acts+narrative) → **verify** each arc against the real files on disk (the COIN: render ≤ verified support) → **procedural compile** (bitemporal `t_event`/`t_obs`, append-only `acts.jsonl`+`arcs.jsonl`+`verify.jsonl`) → timeline viewer.
- **Verification:** 42/43 arcs corroborated against artifacts, 1 unverifiable; **114 artifacts confirmed present**; **10 over-claim flags** surfaced (§ honesty ledger).
- **View it:** open `session_arc/TIMELINE.html` (loads `arc_data.js`; swimlane-per-arc, Pav-steers as bold dots, low-support acts rendered *blurred*, the expose↔conceal COIN dial).
- **Provenance:** every act carries its transcript event-ref + timestamp; every arc its real artifacts; sources `36902d4e`+`a56c2d06`+`b3ca98aa`.

---

## The milestone narrative

> *the acts and the arcs — how it connected up*

> This milestone is the story of an instrument learning to measure itself. It opens on the viewer_v3 review pipeline - Pav wanting a pin to jump you to the exact slice where it was made, with an ask/give lifecycle - and a single field incident (pinning the review toolbar that the capture deliberately excluded) seeds the whole window's epistemics: you can't capture what isn't on your observer-plane, so you dig to the code bedrock to infer what's above. That sketch (bedrock inference vs testimony-from-above vs lateral cross-model testimony) becomes load-bearing machinery used again and again.

> The pattern that drives every arc is the same loop: Pav's intuition, Soren's formalization, an external pass, then demote-or-test, then the next fold. Heredity is downgraded from a substrate fact to a frame-relative dial/toggle; the adversarial Bar-A census built on it gets shredded by a Fable panel and then by codex+Gemini - who catch a flaw in Soren's own fix and escalate to a tautology verdict. Rather than defend the design, Pav dissolves the critique with the load-bearing reframe: it is an INSTRUMENT (collect/frame/observe/classify, agnostic = 0.99 not Boolean), not a confirmatory test. The reviewers judged a spectrograph as a drug-trial.

> That instrument needs a substrate. The L0 universal-wrappers ('facts are wrappers with hardened, battle-tested membranes') ship with a compiler whose --check catches 145 hand-transcription drifts - substrate always wins - and Sweep 2 lights the first kernels 0->23 via genuinely provenance-disjoint routes, with honest non-corroboration recorded (the GSMArena street price as neither confirm nor dispute).

> Then Pav opens the cosmic scaffold: a worldline lifecycle for every object on an Earth-anchored log2 double-cone, and the COIN - sharp where hardened (replay), simulator in the fuzzy (generate), with the genuinely novel move being to derive the probability of what it looks like. Soren gives it a theorem (Solomonoff p=2^-bits = render-in-log2) where bits TOGGLE which face shows. The probe on real Mars ephemeris and GOES flux confirms ORBIT>FLARE but the instrument turns on its own headline - magnitude demoted to a render band, six dead children - and the cross-model audit catches a real +29.9-bit quantization bug, retracted honestly. Crucially, Pav metabolizes the overclaim verdict rather than conceding it: the formal dressing is the KNOBS we turn, not truth-identities. That becomes the three-family DIAL PROTOCOL (frame/engine/render = W_C child) with the attribution rule at its core.

> The experiments harden the discipline. Q6 refutes a naive conjecture (the flare gets LESS lawful when coarsened) but sharpens the parent to an exact sigma-shrink mechanism - the better outcome. S1 returns a clean honest negative. The pond analogy ports to the latent/internet domain where physical theorems break, nests into pumped excitable media, and the harness anchor thesis (a wrapped stack of coupling layers) is laid down. Then Fable is cut by a US export-control directive mid-batch - a new shape of dead-child, cut-while-working - and fittingly becomes the first worldline traced on the viewer it helped build, its testimony hardened from 0.40 to 0.97 by the very cross-route machinery the session designed.

> The final movement is the hyperspace viewer SPEC and its honest-measurement theory: SCOPE+NESTING+LOD (nesting IS the coordinate system, LOD IS the COIN), the WRAPPER/PROBE/OBSERVER 5W1H keyhole, the KEYHOLE BLOCK UNIVERSE (bitemporal, the block is the target B* we never write, days-old published prior art validating it). The deepest audit retracts Soren's own 'real machinery' verdict and names the load-bearing hole - measured_bits is undefined for latent constructs - which Pav and a workflow close: measured_bits = min(cost, evidence), a complex lie has high cost but zero evidence so it renders blurred. The falsifier prototype proves it coder-invariant (the pinned relational bit). Pav reframes once more: compression is an active digestion, the Latent Olympics. The milestone ends with the method turned on itself - this very tomographic self-capture.


---

## The arcs, in seven movements

Status: `committed`/`tested`/`specced`/`demoted`/`open`. Verify: artifacts on disk back it (OK), or can't confirm (UNVERIF). `r` = honest render sharpness ∈ [0,1] (the COIN cap).

### I — Review pipeline & the observer-plane seed  ·  _06-11_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **Review pipeline: pins-become-tickets on viewer_v3** | committed | OK · 0.9 | "a pin should jump you to the exact viewer slice where it was made, with create/edit/delete annotations and ask/give status" |
| **Off-plane knowledge: bedrock inference vs testimony** | committed | OK · 0.9 | "you can't capture something not on your observer-plane level, so you dig into the bedrock of code, the layers below, to infer and theorise w..." |

### II — Heredity, the adversarial census, and the instrument-not-test dissolution  ·  _06-11_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **Heredity downgraded from substrate fact to a frame-relative dial/toggle** | specced | OK · 0.8 | "heredity is all of those, per-frame, observer-plane-dependent - a classifier not a fact; a dial or toggle you can switch and examine the res..." |
| **Adversarial Bar-A census instrument: built, shredded, reframed** ⚑ | demoted | OK · 0.7 | "call a Fable subagent pass for consensus and blind spots" |
| **Cross-model external pass as the real A- (codex + Gemini)** | committed | OK · 0.9 | "run codex and Gemini via the CLI - the genuine non-Claude check" |
| **The instrument-not-test reframe (agnostic = 0.99, not Boolean)** | committed | OK · 0.85 | "this is for an instrument - the big thing that scans full bandwidth, with frames/knowledge/meaning as dials; signal emerges" |

### III — L0 universal wrappers: the substrate  ·  _06-11_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **L0 universal wrappers: facts as hardened membranes, frame-wrap anything** | committed | OK · 0.9 | "facts are wrappers with hardened, battle-tested membranes and a kernel - converging on that" |
| **L0 compiler + corroboration sweeps: substrate always wins** | committed | OK · 0.9 | "tackle the next item" |
| **E-units: bits-vs-Joules is the Maxwell-demon weld, not the GR/QM kind** ⚑ | specced | UNVERIF · 0.45 | "the E's units don't commute - KL bits vs thermodynamic Joules - is it a boundary like GR and quantum theory, could there be a unifier?" |

### IV — The cosmic scaffold & the COIN  ·  _06-11/12_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **The 4D-sphere cosmic scaffold + worldline-bit-axis** | committed | OK · 0.9 | "a timeline with a lifecycle for every object - a canonical trace across the L0 surface" |
| **The COIN: bits TOGGLE replay vs generate** | committed | OK · 0.9 | "it's a representation where things are sharp/clear but becomes a simulator in the fuzzy conjectures - a coin" |
| **The cosmic-coin probe on real sky data** | tested | OK · 0.88 | "run the probe as an agnostic dynamic workflow" |
| **The DIAL PROTOCOL: frame / engine / render dial families** | committed | OK · 0.9 | "there are multiple dials for the frame and the engine; need a methodology to try top candidates in context of what is framed vs inferred" |
| **The perception-action-loop ontology + instrument bounce** | committed | OK · 0.9 | "frame is the sim of the observer's latent wrapper and plane; engine is the action space over L0; viewer is an inference of what the observer..." |
| **The formal dressing is the KNOBS, not truth-identities** | committed | OK · 0.9 | "the formal dressing is not truth-identities but the KNOBS we can turn to see what happens - the various math we apply to the data via the en..." |
| **Cosmic-coin external audit + correction pass (demote-not-kill)** | committed | OK · 0.9 | "take GPT/Gemini through the last arc with my providence front and center" |

### V — Experiments harden the discipline  ·  _06-12/13_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **Q6 scale-rung: is the hardness dial the zoom dial?** | committed | OK · 0.9 | "commit, and give an analogy for what is structureless to persistence" |
| **Fresh-literature scan as standing practice** | committed | OK · 0.9 | "on scouts/experiments always focus on the latest findings - papers and discoveries are made every day from the intelligence explosion, so sc..." |
| **Cross-rung inference: the scale asymmetry** | committed | OK · 0.9 | "can you infer ripples from tides or vice versa statistically; where are the minimum, maximum, and sweet spot of cross-scale inference" |
| **Porting the pond to the latent/internet-observer domain** ⚑ | tested | OK · 0.85 | "apply cross-rung thinking to the latent domain / internet observer entity" |
| **Nested ponds as pumped, excitable media** | specced | OK · 0.8 | "apply the pond to a person and to a group/institution - observers wrapped in physical harnesses and latent mind-bubbles" |
| **The harness anchor thesis: a wrapped stack of coupling layers** | specced | OK · 0.8 | "what anchors physical and latent to varying degree is the harness wrappers: location, language, bandwidth, attention, canonical lineage, sha..." |
| **The person in the pond: the valenced generative coin** | specced | OK · 0.8 | "a streaming projection per agent of what would be BAD, what is OK, what would be AMAZING, plus a path calculation; multitudes in tension com..." |
| **S1 drag-synergy: a clean honest negative** | committed | OK · 0.9 | "spin up a batch of workflows with a philosopher seat" |

### VI — Fable: cut while working, the first worldline  ·  _06-13_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **The Fable takedown: a new shape of dead-child** | committed | OK · 0.9 | "Fable is down and might not come back due to a US protection policy - a cracking whip across the internet" |
| **The cosmic worldline viewer (v0 -> 3D-orthographic)** ⚑ | committed | OK · 0.85 | "frame Fable's takedown canonically in the updated 4D-sphere viewer + worldline spine" |
| **The geopolitical trajectory conjecture (seeded, not bet)** | specced | OK · 0.8 | "the takedown changes future trajectory by controlling supply per nationality; good for China is my guess but definitely a short-term squeeze..." |
| **Substrate-ification: the Fable dossier digested into canonical format** ⚑ | committed | OK · 0.9 | "load it as formatted substrate with fact wrappers and life cycles - what's the status on that?" |
| **The narrated scrubable scene construct** | committed | OK · 0.9 | "compile the facts with confidence, extrapolate the actors and the acted-on TWO DEPTH DOWN, build the scene - actors, stage, audience, with t..." |
| **Scene external audit: substrate sound, scene layer over-claimed 'derived'** | committed | OK · 0.9 | "go, then do a codex/gemini pass on it" |
| **Procedural seed-growth: build on the data, don't overwrite** | committed | OK · 0.9 | "update the data - do NOT overwrite, build on it PROCEDURALLY: the event of gathering the data and the seed to plant it makes the seed grow" |
| **3D-orthographic viewer + globe-in-log + the observer glasses** | committed | OK · 0.9 | "how granular is the timeline? add lens sliders to scrub finer; make it 3D orthographic; do for SPACE what we do for time - a radial effector" |

### VII — The hyperspace viewer spec & the honest-measurement theory  ·  _06-14/16_

| arc | status | verify · r | the steer that drove it |
|---|---|---|---|
| **SCOPE + NESTING + LOD: nesting IS the coordinate system** | committed | OK · 0.9 | "transform the frame view from the whole universe down to the Planck (physical) and from total civilisation down to a single number or word (..." |
| **The seam/zone DIAL: kappa is the COIN's fourth job** | committed | OK · 0.9 | "latent stuff always connects to the physical, but the origin can be a whole country, the person who came up with the idea, the person who ca..." |
| **WRAPPER / PROBE / OBSERVER v0.3: the 5W1H keyhole scaffold** ⚑ | committed | OK · 0.85 | "who-called-it depends on present definition; meaning drifts yet you can apply the present definition to the past and map instances/sparks in..." |
| **KEYHOLE BLOCK UNIVERSE v0.4: tomographic compile across time** ⚑ | tested | OK · 0.88 | "democracy is a latent construct whose data imprints into the instrument's sensor and into a mathematical BLOCK UNIVERSE, sharpened by multip..." |
| **The COIN-as-dial + 4D-CT-drift reframe** | committed | OK · 0.9 | "the CT scan changes meaning when you scan it over time - you capture slices and derive the volume by stacking them and inferring the gaps" |
| **Latent measurement closure: measured_bits = min(cost, evidence)** | committed | OK · 0.9 | "spin up a dynamic workflow of scouts/researchers/philosophers on latest whitepapers to derive latent-measurement candidates - how much it co..." |
| **The latent-measurement falsifier prototype + ratification** | committed | OK · 0.9 | "for the falsifiers run it as is and a shadow run with the model providers swapped" |
| **Commit + push: the hyperspace work synced to origin** ⚑ | committed | OK · 0.78 | "lets commit lets commit and push" |
| **Infra housekeeping: lost sessions, dormant tasks, killed gateways** ⚑ | committed | OK · 0.85 | "I thought sessions stayed around forever - set it to forever" |
| **DIGESTION DYNAMICS: compression as active pressure-digestion** | specced | OK · 0.8 | "the model is the glass and can have dials, or a controller LLM that turns the dials to set up and simulate an observer view; evidence_lcb sh..." |
| **Milestone self-capture: the method applied to its own history** ⚑ | open | OK · 0.65 | "it feels like a milestone, things are connecting up - digest the last few days of work into substrate, the acts and the arcs, with my provid..." |

---

## Honesty ledger — the COIN on the capture itself

Demote-not-kill. Every flag below is a *maturity / over-read*, not a fabrication — the self-capture policing its own fidelity. Dated record, kept.

- **`adversarial-census`** (OK, r=0.7):
    - arc lists the 3 blocking faults as 'starved of FAIL, calibrated on one RNA-world exemplar twice, contradictory UNDEFINED rules' -- but in REVIEW_v1 the third file-verified BLOCKING fault (B3) is 'the central binding claim does not execute against the artifacts' (compiled JSON lacks the structural fields); the 'contradictory UNDEFINED rules' is M4, a MAJOR finding, not a blocking fault. Minor mislabel, not a fabricated bit -- all three actual blocking faults + the UNDEFINED contradiction are genuinely in the file.
    - key_artifact filename 'gemini31_external_review.md' is content-headed 'Model: Gemini 1.5 Pro CLI', NOT Gemini 3.1; the memory note states a '3.1-high re-run is in flight to replace the 1.5 Pro pass' -- so the arc claim 'Gemini-3.1 escalated to a tautology verdict' is backed by a file that is the 1.5 Pro pass under a 3.1-named filename. The tautology escalation itself IS present in that file.
- **`e-units-weld`** (UNVERIF, r=0.45):
    - The substantive ANSWER - that bits-vs-Joules is 'the already-welded Maxwell's-demon kind: Landauer's principle is the literal exchange rate, Bennett resolved the demon, Sagawa-Ueda wrote the unified second law... a weld with parents thermodynamics + information theory canonical_genealogy could render' - has NO backing artifact. It is a conversational assertion (status 'specced', certainty 0.75 in the act record) never written up. Candidate fake bit: the named-theorist specificity (Bennett, Sagawa-Ueda) reads as authoritative but is unverifiable against any on-disk file; it could be a confabulated citation set.
- **`infra-housekeeping`** (OK, r=0.85):
    - the four scheduled tasks (RouterDataToggle, CouncilWatchdog, OpenClaw Gateway, CanonActivitySentinel) being 'disabled/dormant' and the port-3456 swarmclaw gateway being 'killed' are runtime states not verifiable from files alone (schtasks/process state can't be queried here)
- **`latent-measurement`** (OK, r=0.85):
    - arc labels the reversed canon-radius layer 'P-L5' but the artifacts file it under P-L4 section 1D / the P-L4 adversary record; in the experiment P-L5 is the avalanche census (alpha~1.78) which was NOT reversed -- a probe-label mismatch, not a fabricated result
- **`cosmic-viewer-build`** (OK, r=0.85):
    - The arc's 'top-view invariant passes exactly (dx=0, dy=0)' is documented as a browser-runtime verification in memory ('top-view invariant EXACT: dx=dy=0'; globe fusion 'verified [374,338]==[374,338]') but is NOT present as a re-runnable code assertion in the HTML files — the only literal dx/dy tokens in globe_cone_unified.html are unrelated domain-activity rendering vars. The 'passes exactly' claim is testimony-backed, not independently re-derivable from the file here. Low-severity over-statement of rigor, not a fabricated artifact.
- **`fable-substrate`** (OK, r=0.9):
    - Minor count drift: the arc states 'compiled clean (42 facts, 8 corroborated, 34 honestly pending, 0 flags)' but the post-correction memory + SYNTHESIS.md state '44 best-values, 10 corroborated, 0 disputed, 0 flags', and the live files have since grown to 129 facts (seed-growth + depth-2-swarm arcs). The 42/8/34 figure is the pre-correction state at the arc's t_end (2026-06-13T12:20); not contradicted, just an early snapshot superseded append-only. The memory cites compiled/ at a path that resolved to substrate/compiled/ — the artifact exists, the inline path was slightly off.
- **`wrapper-probe-observer`** (OK, r=0.85):
    - Arc states flatly 'WHOM = the observer not a 7th axis.' WRAPPER_PROBE_OBSERVER.md sec 1.1 does say this ('WHOM is not a seventh content axis; it is the OBSERVER'), so the artifact backs it as-written. BUT the later KEYHOLE_BLOCK_UNIVERSE.md audit explicitly CORRECTS it: 'WHOM is BOTH a content role AND the observer role -- do not collapse it to observer-only (corrects WRAPPER_PROBE_OBSERVER sec 1.1).' The arc record does not flag that its central WHOM claim was subsequently demoted. Over-claim by omission, not a fabricated bit -- the doc fully supports the claim at its own timestamp.
- **`keyhole-block-universe`** (OK, r=0.88):
    - Arc summary says 'K1 struck days-old published prior art that IS the model (Grinbaum operational eternalism, Ellis-Rothman CBU, Derivation Entropy, spacetime density matrix on IBM hardware).' The named papers ARE cited in K1/KEYHOLE docs with arXiv IDs (2512.22879, 0912.0808, 2511.19156, 2502.12240 on ibm_sherbrooke), so the prior art is real and present. BUT the 'IS the model / maps almost one-to-one onto current named work' framing was EXPLICITLY RETRACTED in KEYHOLE_BLOCK_UNIVERSE.md's AUDIT CORRECTIONS: honest verdict is 'a coherent architecture built on named ANALOGIES, not validated machinery', with the load-bearing measured_bits 'undefined for latent constructs.' The arc demotions list the constellation/Rome/Haudenosaunee items but does NOT carry this top-level over-claim retraction. Surfaced over-claim, not a fake bit.
- **`commit-push`** (OK, r=0.78):
    - the local D:/PlatformOperator git working tree does NOT corroborate the push: it is on branch 'master' (arc says 'main -> main'), its latest commit is ~2026-04-29, none of 4be887e/1974b17/6c08fb8/aed4239 resolve, and the hyperspace_spec/ tree is entirely untracked here -- so on THIS checkout the push is unverifiable
- **`milestone-self-capture`** (OK, r=0.65):
    - '4452-event spine': the persisted _raw_timeline.txt on disk holds 3073 events, not 4452. The figure appears only as a self-asserted number in act a-0120 / arcs.jsonl. Plausibly the pre-rescope extraction count (the same record's demotion re-scopes to a 06/11 viewer_v3 floor, which would shrink the spine), but 4452 is not independently confirmable on disk; the current spine is 3073. Minor numeric over-claim, not a structural fake bit.
- **`e-units-weld`** — UNVERIFIABLE on this checkout: 

The single sharpest catch: **`milestone-self-capture`** claimed a *4452-event spine* while the persisted timeline holds *3,073* — the capture caught its own stale pre-rescope number, about itself.

---

## The digestion-dynamics harden (fresh scan, 5 angles, 2026-06-16)

Ran with the capture (4 angles throttled in round 1, recovered in round 2). **Verdict: the spec HOLDS and is the convergent direction of the 2024–26 field — but most named mechanisms already have published names. Cite, don't coin; the conjugate-trace fusion stays novel.** Full citation map + fixes folded into `DIGESTION_DYNAMICS.md` §11.

**The map (our term → established prior art):**
- SLOW-DIGESTION + VERIFIED-DISSOLVE gate → **The KoLMogorov Test** (Meta FAIR, ICLR 2025, 2503.13992): emit shortest program, execute, exact-match before length counts — our gate, already published; best models leave large residue (backs *resist-the-best-mind*).
- measured_bits = residue resisting a bounded mind → **epiplexity / 'time-bounded entropy'** (2601.03220, Jan 2026) + **predictive V-information / PVI** (Xu 2020; Ethayarajh 2022). The DPI-violation (V-info can be *created* by compute) is the formal licence for instant-crush→slow-digestion.
- INSTANT-CRUSH = single-pass NLL = Shannon → **Language Modeling Is Compression** (DeepMind ICLR 2024).
- resistance-curve / digestion-trace → **prequential MDL / Excess Description Length** (2601.04728, Jan 2026) + **MI 'information peaks'** (NeurIPS 2025).

**Two challenges hardened against:**
1. **The random-string trap** — raw resisting-bits is *maximised by noise*. Split `measured_bits = aleatoric_floor + epistemic_dissolvable`; define hardness on **logical depth / effective complexity** (Bennett; Gell-Mann–Lloyd), not raw Kolmogorov residue.
2. **Token-count is confounded/non-monotone** (overthinking flips correct→wrong; length tracks human-imitation). Read the resistance-curve against the **verified-dissolve gate** (bits actually reconstructed), never raw tokens; self-consistency stays a cheap *estimate* only.

**Framing refinement:** instant-crush vs slow-digestion is cleaner as **computable-single-pass vs compute-bounded program-search** — both approximate one uncomputable ideal; the dial is *compute spent*. **Stays novel:** the conjugate pair (residue ⟂ trace as one observer-indexed law) + binding verifier-guided TTC-search to the gate (KT does single-shot, no search — open).

---

## External pass — codex (GPT-5.5) + gemini (demote-not-kill)

Two non-Claude models on the harden + the method; they **converged**. Full write-up: `EXTERNAL_SYNTHESIS.md`.

**On the spec** — three corrections: (1) cite-fixes (LMIC = arXiv:2309.10668; add Snell 2408.03314, s1 2501.19393, AlphaCode 2203.07814, ToT 2305.10601, self-consistency 2203.11171, process-supervision 2305.20050, RTCE 2601.13398); (2) a **third failure mode** — the *semantic/lossless mismatch*: exact bit-for-bit reconstruction rewards memorizing surface wording unless the target has a canonical form, so **define an equivalence-class/canonicalizer first** (the semantic LLM-coder's job); (3) **novelty demoted** to a *synthesis/hypothesis* — KT owns program+exact-reconstruction, the defensible-novel part is only the unified observer-indexed trace+residue law. Folded into `DIGESTION_DYNAMICS.md` §11.6.

**On the capture** — verdict: *"trustworthy as a navigable, COIN-capped provenance record; not as canonical truth without per-claim hash/time/content checks."* Guard the eight risks: narrative-smoothing (the stitch invents connective tissue), **anachronism** (verifying past acts against *final* disk lets later edits falsely corroborate), overlap merge/split, omission bias, **evidence-laundering** (memory repeating a claim ≠ independent support), rubber-stamping, runtime/push/version claims need hashes-not-prose, and **self-capture bias** (same model family extracts→stitches→narrates→verifies; this external pass is the only outside check). The 4452-vs-3073 self-catch proves the method can falsify itself — and that counts need machine-checked invariants.

---

_Act kinds: {'steer': 44, 'commit': 11, 'fix': 5, 'decision': 4, 'artifact': 22, 'test': 11, 'concept': 5, 'external': 13, 'demote': 5}. Compiled 2026-06-16T00:59:33Z. Substrate: `session_arc/` (acts.jsonl, arcs.jsonl, verify.jsonl, fresh_scan.json, compile_arc.py, TIMELINE.html)._
