# DIAL PROTOCOL — frame dials, engine dials, and the candidate-trial methodology (SPEC, Tier-3 DRAFT)

> **Status:** Tier-3 working spec, surfaced for Cowork+Pav ratification — NOT canon, NOT compiled, no tier advanced, convergence list stays **9**. A **sibling spec** in the L0_WRAPPER_SPEC mold: it BINDS to the existing substrate format protocol (append-only JSONL → compiler → compiled views → viewer ingestion) and to the existing frame-lock discipline; it forks nothing and edits nothing ratified.
> **Pav steer (2026-06-12, verbatim sense):** *"there's multiple dials for the frame and the engine and we need a methodology to try the top candidates in context of what is being framed and what is inferred — this is where something like this [AutoScientist] can plug in, specked out to the viewer and substrate format protocol."* **Same-day addendum:** *"there are the render dials as well — the viewer; the W_C of engine and frame, the output if you will."* — the third family (§1.4), folded in below.
> **Born from a measured incident:** the cosmic-coin probe (`../cosmic_coin_probe/FINDINGS.md`) found its reading's *direction* robust but its *magnitude* a knob — and the knobs split cleanly into two families that need **opposite** handling. This spec is that split, made protocol.

---

## 1. The three dial families

Every reading the instrument produces is taken with a vector of dial settings. The load-bearing distinctions:

### 1.1 FRAME dials — *what is being framed*
Dials that change **what is being observed**: turn one and you are asking about a different slice of the world.

| frame dial | examples (measured instances) |
|---|---|
| `phenomenon` | Mars position / GOES long-band flux |
| `scale_rung` (time) | 1-min cadence vs daily vs solar-cycle (FINDINGS Q6) |
| `scale_rung` (space/semantic) | the L0 abstraction ladder rung; generic↔specific |
| `window` | which year, which week (probe: flare halves/quarters CR 1.09–1.23) |
| `channel` | GOES long band CR 1.27 vs short band CR 1.02 |
| `observer/plane` | physical / latent / straddle (SCHEMA_v2 `frame_layer`) |
| `inferred` | **what question is asked** — see §1.3 |

### 1.2 ENGINE dials — *how the instrument reads*
Dials internal to the measuring engine: turn one and you are asking the **same question with a different instrument calibration**.

| engine dial | examples (measured instances) |
|---|---|
| `law` (compressor candidate) | persistence / AR(1) / EWMA / MA(n) / Kepler two-body |
| `predictive` family | Gaussian / Student-t(nu) (probe: flare saved-frac 0.21→0.454) |
| `coder` | zlib-1/zlib-9/bz2-9/lzma-9/lzma-9e (ratio-of-CR 1.33–2.03, never inverts) |
| `quantization` | 1 km / 1e-3 dex (cancels exactly only in σ-shrink form) |
| `null/baseline` + model-bits accounting | "store" floor; model bits counted, never zero |
| `holdout scheme` | in-sample vs out-of-sample fit |
| `formalism/accounting` *(named 2026-06-12, Pav: "the formal dressing is the knobs we can turn")* | which MATH is applied and how it counts: probability semantics (predictive-distribution log-loss / coder codelength / algorithmic-probability ideal), cost model (parameter-bits-only vs +program-bits vs +calibration-bits), loop framing (passive MDL vs active acquisition). Each setting has WELL-FORMEDNESS CONDITIONS that travel with the record (p=2^-bits is exact only for a specified prefix code; free-energy applies only with a generative model + policies acting on the data stream) |

### 1.3 The pair (framed, inferred) — hardness belongs to the QUESTION, not the thing
The same phenomenon under a different `inferred` is a **different trial subject**: the flare is fuzzy for *"next-minute log-flux"* but plausibly much sharper for *"will this week contain an M-class flare"* (coarse-grain question). Dial position is a property of the **(framed, inferred) pair**. This is the meaning-kernel entering the protocol: what you ask determines what is sharp. No trial record without an explicit `inferred`.

### 1.4 RENDER dials — *how the output is shown* (the W_C of frame and engine)
Pav's genealogical reading, adopted as the definition: **the displayed view is the child wrapper (W_C) produced by the weld of frame × engine** — the output. Render dials are the dials ON that child: they change how the reading is shown, and must change **nothing** about the reading itself.

| render dial | examples (all already shipped, now named) |
|---|---|
| sharpness/hardness mapping | `l0-membrane-proxy-v0.1` (h = B(bucket)·certainty) — a *versioned render dial*, PROXY_SPEC-disclosed |
| LOD / depth-context cutoff | the viewer's depth dial, quality ladder, fuzzy-LOD |
| axis warps | time-axis calendar↔order blend, scrub fisheye, log2 radius |
| prominence weights | observer-kernel re-weighting in group renders (§2.5 frame weights — estimate-proxies) |
| thresholds & encodings | mirage threshold, mass→force, color/pattern-for-same-colour, band→edge-thickness |
| layout & state | panel positions, toggles, selected node — everything `__getReviewState()` captures |

**The view inherits both parents' membranes** — frame-relativity from the frame parent, the calibration band from the engine parent. The render dials set how those inherited fuzzes are *shown*. **Broken-weld law:** a view that renders sharp what either parent holds fuzzy is a broken weld — the no-invented-precision UI law restated genealogically (and never-render-fake-measured-bits is its generative-face form).

**Retroactive naming (vocabulary meets existing structure):** `group_configs/*.json` are saved render-dial presets; the review pipeline's `__getReviewState`/`__applyReviewState` is render-dial state capture/replay (a pin's frame-replay = restoring the render vector); PROXY_SPEC is the render-dial disclosure discipline, already ratified. The family existed; it now has a name and a seat in the protocol.

## 2. The attribution rule (the epistemic core)

When a reading varies under a dial sweep, **which family moved decides what the variance means**:

- **ENGINE-dial variance = instrument calibration.** Report the **band**, never one headline; pin defaults; disclose per PROXY_SPEC (versioned, falsification target). *Measured instance:* the coin margin ~1.17×–2.8× across coder × predictive is an **engine-calibration band** (corrected 2026-06-13 — it had been mislabelled "a render knob"; coder and predictive are ENGINE dials, so calling its variance a render artifact violated this very rule — the external pass caught it; FINDINGS dead-child 9).
- **FRAME-dial variance = frame-relativity, an OBSERVABLE.** Not noise to average away, not a flaw — the solid↔fuzzy reversal under re-framing is signal to investigate (already canon: the contextual-scale dial; the agnostic-instrument register). *Measured instance:* long band 1.27 vs short band 1.02; quiet-sun window 1.21.
- **Mixed variance** (engine dial behaving differently per frame setting — e.g. Student-t HELPS the flare, HURTS the orbit) is the most informative cell: it localizes *structure* (tail weight is a property of the framed thing, revealed by the engine sweep). Flag it `interaction`.
- **RENDER-dial variance = presentation-relativity, and the cheapest mirage detector.** A render dial must never alter a recorded number — so any feature of the *view* that appears or dies under a render-dial sweep, with frame and engine untouched, is a **render artifact (mirage candidate), never a finding**. "Wiggle the render before believing the view" is the sharpening test generalized: real structure survives the render sweep; mirage dies with the dial. (The capture-layer incident is the inverse failure on record: a render-layer rule *hid* real structure — render dials can occlude as well as conjure, which is why the sweep goes both ways.)

A sweep's deliverable is therefore a **variance decomposition over the dial grid**, not a number — with three meanings of variance, one per family.

**The formalism corollary (from the 2026-06-12 external pass):** a formalism is a **dial setting, never an identity**. Asserting "the duel IS Solomonoff / IS free energy" is mistaking a dial position for a reading — the same error as quoting one coder's margin as THE margin. The honest form: state the setting's well-formedness conditions, turn it, and report what it CHANGES (held-out bits, decomposition, decisions). A formalism setting that changes nothing measurable is decoration *by measurement* — which converts "is this framing legitimate?" from an opinion into an instrument reading.

## 3. The trial methodology ("try the top candidates")

1. **Declare the pair** — `framed` (phenomenon + frame-dial settings) and `inferred` (the question). One line each, before any run.
2. **Enumerate top-K candidates per engine dial** — laws from the candidate registry (§5) + the conjecture engine (§6); predictive families; the pinned coder ladder. K small (3–5); breadth comes from sweeps, not one giant grid.
3. **Lock the frame** — frame dials are FROZEN for the sweep (the existing frame-lock discipline, same move as L0 §7.3 / the census dial-lock). Frame-dial changes are *proposed in the sweep log, applied next sweep*.
4. **Run the grid** — every candidate × the engine-dial ladder, held-out where fit is involved, model bits counted. Each cell = one **trial record** (§5), append-only.
5. **Read the decomposition** — per §2: the band (engine), the relativity observables (frame, from comparisons *across* sweeps), the interactions.
6. **Advance the lifecycle** — best candidate per (framed, inferred) = the **current kernel candidate**; beaten candidates stay as dated dead/demoted children (never deleted); a candidate that wins = a dial-jump, appended to the law's worldline (laws have lifecycles too — FINDINGS S4).
7. **Log the sweep** — dated section in `SWEEP_LOG.md`: grid run, decomposition, dial-jumps, dead-children tally, PROPOSED frame/engine vocabulary for next sweep.

## 4. The AutoScientist plug-in seat (conjecture engine)

Pav's pointer: `https://autoscientists.openscientist.ai/` — decentralized agent teams alternating **discussion** (form teams around directions, propose experiments) and **execution** (parallel runs, reorganize on stagnation), sharing best-result + experiment logs + forums + **dead-end registries**. The mapping onto machinery we already run is almost 1:1 — this seat is a *generator*, the protocol is the *verifier*:

| AutoScientist | this protocol |
|---|---|
| hypothesis generation | **candidate minting** — propose a new `law`/`predictive` for a (framed, inferred) pair, with its prior-art note |
| experiment design + execution | the **trial grid** (§3.4), run by workflow seats (Sonnet scouts / Fable judges / Opus skeptic, the standing pattern) |
| the score | **held-out bits** with model bits counted — the duel is the verifier; no narrative wins |
| best shared result | the **current kernel candidate** per pair, in the compiled view |
| dead-end registry | the **dead-children tally** (CLAIM_LIFECYCLE — demoted/dormant/dated, never deleted) |
| team re-org on stagnation | sweep-log **frontier**: pairs whose gap stopped closing get new candidate families next sweep |
| compute budget | per-sweep token/run budget, declared in the sweep log |

**Boundary (hard):** the conjecture engine *proposes and scores*; it never writes canon, never edits a prior record, never renders. Its output is candidates + trial records into the append-only log. Ratification stays with Pav/Cowork. External A− (GPT-5.5 + Gemini) stays the cross-model check on load-bearing readings — workflow seats are Claude-only.

## 5. Substrate binding (format protocol)

Same machinery, new record type — **nothing in SCHEMA_v2 or SUBSTRATE_SPEC edited**:

- **`runs/<sweep>.jsonl`** — append-only, one **trial record** per line:
  ```jsonc
  { "trial_id": "dial-<pair-slug>-NNNN",        // globally unique, HAZARD-guard style
    "sweep": "dial-sweep-NN",
    "framed":   { "phenomenon": "...", "frame_dials": { "scale_rung": "...", "window": "...", "channel": "..." } },
    "inferred": "next-step log-flux",
    "engine_dials": { "law": "...", "predictive": "...", "coder": "...", "quant": "..." },
    "candidate_source": "authored | conjecture-engine | adversary",
    "data": { "source_url": "...", "n": 0, "real": true },   // NO fabrication; real fetched data only
    "reading": { /* bits_raw, bits_resid, model_bits, comp_ratio, saved_fraction,
                    sigma_shrink_bits_per_dim, appearance_bits_per_step ... whichever were MEASURED */ },
    "dimensionless_only_across_pairs": true,     // the E-units law, in-band
    "verifier": "dial-sweep-NN-<seat>", "retrieved_at": "ISO", "notes": "..." }
  ```
  Append-only correction discipline: a wrong reading is superseded by a new record naming it, never edited (same as fact retractions).
- **Compiled view** (`compiled/dial-<pair>.compiled.json`, deterministic compiler to be built as `tools/compile_dials.py`): per (framed, inferred) pair — the current kernel candidate, the **band** over engine dials, the frame-relativity observables, the interaction flags, the law worldline (dial-jump history), the mixture profile (replay-fraction, break census) where measured.
- **PROXY_SPEC compliance:** every render-bearing engine default (pinned coder, predictive family, quant) is a versioned disclosed proxy with a falsification target. v0 pins: `lzma-9`, Gaussian-unless-beaten-fairly, declared quant per phenomenon, model-bits-counted, **no absolute bits across pairs** (the E-units law).
- **View reproducibility:** any visual artifact derived from trials (a FINDINGS plot, a toy config, a viewer slice) is fully determined by `(framed, inferred, engine_dials, render_dials)` — so view-bearing records MAY carry an optional `render_dials` vector, and a saved view = a saved four-tuple. `group_configs/*.json` and review-pin `state.viewer` blobs already ARE this object; the protocol just names them.

## 6. Viewer plug (specked, not built)

- **Dial panel — three tiers, one per family:** FRAME dials render as user-turnable controls (the scrubber, the zoom/abstraction dial, observer picker — all already exist in viewer_v3; `window`/`channel`/`inferred` join them). ENGINE dials render as **pinned chips** showing the band on hover ("margin 1.17×–2.8× over coder × predictive") — turnable only in an explicit calibration mode, per the attribution rule. RENDER dials are freely turnable but disclosure-bound (every one a PROXY_SPEC entry) — plus a **"wiggle" affordance**: one control that jitters the render dials so the eye can run the mirage test live (what survives the wiggle is structure; what dances with it is render).
- **Observer disambiguation:** "observer" appears twice and the panel must keep the two apart — observer-as-FRAME (whose kernel poses the question; changes what is measured) vs observer-as-RENDER (prominence re-weighting in a group view; changes only what is shown). Same word, different families, different tier of the panel.
- **Reading render:** dial position (σ-shrink bits/dim) drives wrapper sharpness; the band renders as edge thickness (a wide band = a wide coin edge); mixture profiles render as kernel-disc radius (replay fraction) + membrane spikes (the breaks).
- **Law worldlines:** each (framed, inferred) pair carries its dial-jump trace (Saros→Newton→GR style) as an exhaust trail — the lifecycle render the viewer already does for claims, applied to laws.
- **Provenance hover:** every rendered sharpness links its trial records (fact_refs pattern).

## 7. Worked binding — sweep 0 (retro-encoded from the cosmic-coin probe, real numbers only)

`runs/dial-sweep-00.jsonl` encodes the probe's actually-measured grid as the first trial records: Mars × {Kepler} × {Gaussian} × {lzma-9, zlib-9, bz2-9} and GOES × {persistence, AR(1), EWMA, AR(1)-on-increments} × {Gaussian, Student-t(2.1)} × coder ladder, plus the frame-dial trials (window sub-splits, quiet-sun-only, channel swap, onset-amplification). Every number traces to `../cosmic_coin_probe/results.json` / `FINDINGS.md` / the adversary scripts; nothing re-derived, nothing invented. Sweep 0's decomposition is the probe's §5 adversary table, re-read as protocol output:
- engine band: coder 1.33–2.03× (ratio-of-ratios), predictive 0.21→0.454 (flare saved-frac);
- frame observables: window 1.09–1.23, channel 1.27 vs 1.02, quiet-sun 1.21;
- interaction: Student-t helps flare / hurts orbit (tail weight is structure);
- dial-jump: none (persistence survived as flare kernel candidate; AR(1)-on-increments 1.30 vs 1.27 is within engine band — flagged, not promoted);
- dead children: inherited 6 from the probe (FINDINGS §7).

## 8. Discipline footer

Frame-lock per sweep; append-only everywhere; NO fabrication (every trial on real fetched data, `data.real` mandatory); model bits counted; **dimensionless-only across pairs** (E-units, in-band); proxies versioned + falsifiable; **render dials never alter a recorded number, and a view never renders sharp what either parent holds fuzzy (the broken-weld law)**; conjecture engine proposes, never ratifies; verified = Pav's call; Tier-3 throughout, convergence list stays **9**. Owed before this hardens: an Opus skeptic pass on this spec, the GPT-5.5+Gemini external pass (Claude-only so far), and `tools/compile_dials.py` + the viewer dial panel as the build steps — gated on a Pav/Cowork nod.
