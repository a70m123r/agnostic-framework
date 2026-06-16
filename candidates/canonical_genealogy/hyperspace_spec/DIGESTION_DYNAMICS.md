# Digestion Dynamics, the Observer-Controller, and the Latent Olympics (spec)

**Date:** 2026-06-16 | **Status:** Tier-3 design. Conceptual - extends (does NOT replace) the validated static unit in [latent_measurement_candidates.md](latent_measurement_candidates.md). The static residue is tested (14/15 falsifiers, coder-robust); the *dynamics* below are a new layer, untested - flagged throughout.

From Pav (2026-06-16): *"if you can guess it you are leveraging your latent processing - logic, rules, knowledge, wisdom, laws, pattern recognition (instinct) - upon it; you take it into the mind bubble and crush it or slowly digest it; it applies waves of pressure in its local action space, and if it maps it falls apart and melts away. We can capture this with LLMs - how many attempts, how many tokens, what strategy - and map the nature of latent dynamics; a spectacle for the Latent Olympics."*

---

## 0. The one-line extension

The validated unit measures `measured_bits = min(cost_ub, evidence_lcb)` - a **static** residue. This spec reframes that residue as the **outcome of an active process** and makes the **process itself** a first-class, conjugate measurement.

> **`measured_bits` = what *resists* the observer's pressure.** The observer pulls a target into its mind-bubble and applies everything it has as pressure; what **maps** dissolves to ~0 (derivable - it melts into the prior), what **resists** is the irreducible content (a stone). The static codelength is the *residue*; the **digestion dynamics** (attempts / tokens / strategy / resistance) are *how it resisted* - a richer, conjugate signal.

This is not a new honesty law - it is the **same COIN, read dynamically**, with one new gate (verified-dissolve, sec 5).

---

## 1. Compression as pressure (the reframe)

| static view (validated) | dynamic view (this spec) |
|---|---|
| `measured_bits` = codelength = bits-to-reproduce under a pinned coder | `measured_bits` = the **residue** after the observer applies its full apparatus as pressure |
| passive count | active digestion: **crush** (instant) or **slowly digest** (effortful) |
| Shannon (compress under a fixed distribution) | Kolmogorov (the observer **searches for the shortest program** that regenerates the target) |
| the coder | the **observer / glass / mind** |
| "complex" = high codelength | "resistant" = does not map to this mind's structure |

What dissolves vs what resists is **observer-relative** (sec 6): an idea derivable to an expert (melts) is novel to a novice (a stone). Capability **is** the pressure the mind can apply.

---

## 2. Two regimes of pressure

- **INSTANT CRUSH** = the single-pass prequential NLL already in the unit (`Sum_t -log2 P_M(x_t | x_<t)`). The mind's *instinctive* compression - what it predicts in one breath. This is the **Shannon** regime, and it is the one we validated.
- **SLOW DIGESTION** = the mind *reasons* (chain-of-thought, multiple attempts, test-time compute) and dissolves **more** than its instinct could - it *derives* what the instant pass missed. This is the **Kolmogorov** regime: the digestion is a **program search** for a short regeneration of the target.

The two share one currency (bits) and one honesty law. The slow regime can only ever **lower** the residue below the instant-crush bound - and only by a **verified** derivation (sec 5), so it stays one-sided.

`[SPEC]` The effort the slow regime needs is itself the difficulty signal - this is the bridge to test-time-compute / reasoning-length-as-difficulty (2025-26 line; verify in the external pass).

---

## 3. The conjugate measurement (the "counter-unit"): digestion dynamics

The static residue says *what* resisted (in bits). The **digestion trace** says *how* it resisted:

```
D(W ; M) = ( attempts a, tokens tau, strategy s, resistance-profile rho )
```

- **attempts `a`** - tries to crack it (toughness).
- **tokens `tau`** - the *chewing*: reasoning compute spent dissolving it (the digestion effort).
- **strategy `s`** - the *path* taken (a taxonomy extractable from the trace): `recall` (knew it), `derive` (logic/rules/laws), `analogize` (mapped to a known pattern), `compute` (brute force), `fail` (could not). The strategy mix characterizes *what kind of thing* the target is.
- **resistance-profile `rho`** - the load-bearing one. Run the observer with **increasing effort budgets** and record `bits_remaining(effort)`. The curve is the signature:

```
PHASE      rho(effort) shape                         reading
SOLID      flat near cost_ub (resists)               irreducible to THIS mind - a stone
DIGESTING  decreases gradually with effort           derivable but with work
DISSOLVED  drops to ~0 almost immediately            recognized / derived on contact - melts
```

The **asymptote** of `rho` (as effort -> the mind's max) = the **irreducible residue** (what no amount of *this* mind's pressure dissolves). The **area under the drop** = the digestion cost.

**Why it is richer than bits:** two targets with *identical* `measured_bits` can have opposite dynamics - one melts in 3 tokens via a known law, one resists 50 attempts. That difference - invisible to the codelength - is the **map of latent dynamics** (the phase of the target in the observer's action space). The static bits and the dynamics are **conjugate**: the *amount* that resisted x the *manner/cost* of resistance.

---

## 4. The observer is the glass, and it has dials

The observer is a **configurable** glass; its settings are the measurement contract (the *pinned relational bit*):

- **knowledge / capability** (the cost-coder): how much pressure the mind can apply - sets how much dissolves.
- **`evidence_lcb` = the skepticism dial**: how much *independent corroboration* the observer demands before it will render sharp. Skeptic -> blurs until heavily corroborated; credulous -> sharpens on a whisper.
- **knowledge-epoch / persona**: *which* mind (a 1789 observer, a domain expert, a hostile critic). Diachronic - the same target dissolves differently under `D(1789)` vs `D(2026)` (ties to the definition-drift / retroactive-origin layer).

**The controller (an "LLM specialist").** A meta-agent that **dials in** a chosen observer and **simulates its view**: configures the persona / epoch / skepticism / capability, runs the digestion, returns that observer's residue + dynamics. This operationalizes the **mind-sandbox** and the philosopher's *"whose decoder?"*: "what does this look like *to* X?" - the controller instantiates X and runs it. **Stratum-2, always badged** - a *modelled* observer, never claimed as a real one.

---

## 5. Honesty guards (so the pressure-frame stays COIN-true)

1. **VERIFIED-DISSOLVE (the COIN on digestion).** A dissolve only counts if the observer's compressed representation **actually regenerates the target** - `execute-verify-or-back-off`:

```
dissolved_bits(W) = (cost_ub - residue)   IF  reconstruct(observer's program) == W
                  = 0  (back off to the literal cost)   otherwise
```

   A *plausible-but-wrong* derivation earns **no** discount. A strong mind cannot **fake-dissolve** (claim low bits for content it only guessed) - it must cash the derivation out in exact reconstruction. This keeps the slow regime one-sided and is the same gate the units research named (KT execute-verify).
2. **GENERATIVE-PRESSURE RISK.** The slow regime is generative - a strong mind hallucinates derivations. Guard (1) catches the unverifiable ones; the **evidence side** (`evidence_lcb`, baseline-relative, held-out) catches a mind manufacturing *corroboration*. Both matter MORE as capability rises.
3. **OBSERVER-RELATIVITY.** A stone for one mind melts for another, so **every result measures the observer as much as the target.** The near-objective output is the **universal residue** (sec 6): the content that resists the *best available* mind.

---

## 6. The Latent Olympics (the spectacle)

Stage the digestion as a contest. Connects to the existing **Latent Olympics DB** (see [[parents_wc_frame_and_olympics_demo]]).

- **events** = latent entities (a concept, a claim, an idea-wrapper).
- **athletes** = configured observers `{M_i}` (different minds / models / personas / epochs).
- **scoring** = the dynamics: residue bits, **verified** digestion effort (tokens/attempts), strategy, phase. Leaderboard = who dissolved it **cheapest** (fewest verified tokens).
- **the universal residue** = `min over M_i of residue(W ; M_i)` = the content **no athlete could dissolve** - the **universal hard stone**. This is the closest thing to *intrinsic* content the framework allows: not an absolute measure, but the **residue under the strongest available decoder** (the pinned relational bit pushed to its best limit). A genuinely useful, near-objective output.
- **the spectacle** = watch ideas **melt under some minds and stand solid under others**; the events board; the strategy replays (how each mind cracked it). The visualization is the payoff: latent dynamics made watchable.

---

## 7. Measurement protocol (how to run it / the prototype shape)

A single **digestion trial** for target `W`, context `C`, observer `M`, effort budget `B`:

```
1. PRESENT  : give M the context C (the prior) and ask it to LOSSLESSLY reproduce W
              from C using as few of its own emitted tokens as possible (the program).
2. DIGEST   : let M spend up to B reasoning tokens / a attempts to find a short program.
3. VERIFY   : execute the program; if reconstruct == W, the residue = len(program in bits);
              else back off to the literal codelength (guard 1).
4. LOG      : residue bits, tokens_spent tau, attempts a, strategy label s (from the trace),
              and rho(b) = residue as a function of budget b in [0, B]  (the resistance curve).
```

Sweep `B` to trace `rho`; classify the phase; repeat per athlete for the Olympics board. The **LLM coder** wired in here is the one scoped in [LLM_CODER_SCOPING.md](LLM_CODER_SCOPING.md) (OpenAI-echo for exact codelength, or local; the *reasoning* trace gives `tau / a / s`).

---

## 8. Settling experiment (validate the dynamics are real signal, not noise)

- **V1 - effort tracks difficulty.** On a benchmark of items with ground-truth graded difficulty (e.g. math/logic problems easy->hard), the **verified digestion effort** (tokens-to-dissolve) must rise with difficulty: easy items melt fast, hard items resist. If `tau` is flat across difficulty, the dynamics are noise.
- **V2 - universal stones replicate.** The resist-all set (sec 6) must be **stable** across two independent athlete rosters - a real residue, not a per-roster artifact.
- **V3 - the verified gate holds.** Items a mind *claims* to derive but **cannot reconstruct** must receive full bits (no fake-dissolve leakage). Inject unverifiable "plausible" derivations and confirm they earn 0 discount.

Pass on all three = the digestion dynamics are a real measurement layer over the validated static residue.

---

## 9. What this changes / how it extends

- The static unit is unchanged and remains the **instant-crush** baseline.
- The dynamics add a **conjugate** measurement (`D`) and a **phase** classification (solid/digesting/dissolved) - the map of latent dynamics.
- `evidence_lcb` becomes a **dial** (skepticism); the observer becomes a **configurable glass**; a **controller** simulates observer-views (Stratum-2).
- The keystone holds: everything still in **bits** (the residue), now with a **process** alongside; "substrate as light on a sensor" deepens - the observer/mind **is** the sensor, and we now also record *how the sensor worked*.
- The **universal residue** gives a near-objective content measure (resist-the-best-mind) without claiming an intrinsic one.

**Prior art to harden** (DONE 2026-06-16 - see sec 11 for the fresh-scan result + the citation map + the two hardening fixes).

---

## 10. Open questions for Pav

1. **Effort budget as the dial?** Is the controller's primary knob the **effort budget `B`** (how hard the mind is allowed to chew) - i.e. you turn up B and watch more melt - or the **persona/epoch**? (Both are dials; which is the headline.)
2. **Universal stones as the canonical content?** Do you want the **resist-the-best-mind residue** promoted to *the* near-objective `measured_bits` (the Olympics gives you the strongest available decoder for free), with single-mind measurements as the per-athlete views?
3. **Strategy as a rendered channel?** Should the **strategy** (recall / derive / analogize / compute) be a visible channel in the viewer (colour the dissolve by *how* it melted), or kept as analysis-only metadata?
4. **Olympics scope.** Real latent entities from the substrate as the first events (e.g. democracy, the Musk wrappers, the Fable-takedown facts), or a controlled difficulty-graded set first (for V1)?
5. **Live vs replay.** Is the spectacle a **live** contest (minds digesting in real time) or a **replay** of logged digestions (the bitemporal block - `t_obs` of each digestion)?

---

## 11. Prior art + hardening (fresh literature scan, 2026-06-16)

A 5-angle scan (test-time-compute-as-difficulty; LMIC/Kolmogorov-vs-Shannon; verified-reasoning; decoder-relative-information; concept-hardness) of the 2024-2026 landscape. **Verdict: the framing HOLDS and is the convergent direction of the field - but most of the spec's named mechanisms already exist in the literature under other names.** The move is to CITE, not coin; the genuinely novel part survives and sharpens. (This is the [[feedback_translate_formalization_for_pav]] note in action: the math below is the established vocabulary for Pav's intuition - the intuition came first and is intact; we are just bolting it to the right citations so it is defensible.)

### 11.1 The citation map - what each piece already is

| our term (Pav's framing) | established prior art | lead citation |
|---|---|---|
| SLOW-DIGESTION = derive the short program | **compression-by-code-generation** | **The KoLMogorov Test (KT)**, Meta FAIR, ICLR 2025 - arXiv:2503.13992 |
| VERIFIED-DISSOLVE gate (exact reconstruction or 0 discount) | KT's `1{[rho]=x}` execute-and-exact-match (coding cost = +inf if the program doesn't reproduce x); **round-trip self-consistency** | KT 2503.13992; RTCE 2601.13398 (2026); CoT computational-graph faithfulness 2510.09312 |
| INSTANT-CRUSH = single-pass NLL = Shannon | **language modeling IS compression** (log-loss = expected code length) | LMIC, DeepMind ICLR 2024; Compression-Represents-Intelligence-Linearly 2024 |
| measured_bits = the residue that resists a bounded mind | **epiplexity / "time-bounded entropy"** (compute-aware info, strictly between Shannon & Kolmogorov); **V-usable information** (its complement) | epiplexity 2601.03220 (Jan 2026); predictive V-information Xu et al. ICLR 2020; PVI Ethayarajh et al. ICML 2022 |
| the resistance-curve / digestion-trace | **prequential MDL codelength** + per-step **Excess Description Length (EDL)**; **"information peaks"** (MI spikes at thinking-tokens) | EDL 2601.04728 (Jan 2026); MI-Peaks NeurIPS 2025 2506.02867; Blier-Ollivier 2018 |
| universal residue = resist-the-best-mind | **Kolmogorov-randomness / incompressibility** + irreducible-error floor for all finite/computable minds | Li-Vitanyi; Fundamental-Limits-of-LLMs-at-Scale 2511.12869 |

The **DPI-violation result** (Xu et al. 2020: V-usable information can be *created* by computation, unlike Shannon MI) is the formal licence for the whole instant-crush -> slow-digestion move: a reasoning process legitimately *raises* the decoder's usable information (lowers the residue) where a single forward pass could not. That is exactly "apply more pressure, more melts."

### 11.2 Two challenges to harden against (real, must-fix)

1. **The random-string trap.** Raw "bits that resist compression" is **maximised by NOISE** - an incompressible random string has maximal Kolmogorov residue but is NOT a deep concept. So `universal residue = resist-the-best-mind` must **split the residue into two layers**: ALEATORIC (truly random - high single-pass NLL AND high raw-K, never dissolvable, a model-independent floor) vs EPISTEMIC (structured-but-hard - dissolvable by a better mind). Define "hard concept" on **logical depth / effective complexity / sophistication** (Bennett; Gell-Mann-Lloyd; Koppel) - which peak on structured-but-hard objects and assign LOW value to both random and trivial - NOT on raw Kolmogorov residue. The COIN already wants this: the aleatoric floor is a *measured* bit (genuinely irreducible), the epistemic layer is what digestion dissolves. **Bifurcate `measured_bits = aleatoric_floor + epistemic_dissolvable`.** (cite: aleatoric/epistemic ICLR-2025 irreducible-loss; effective-complexity 0810.5663.)

2. **Token-count is a confounded, NON-monotone difficulty proxy.** "Overthinking" flips a previously-correct answer past ~7-12k tokens (2604.10739); reasoning length tracks *human-imitated* effort more than model uncertainty (PNAS 2026); models trained on long-but-easy traces match models trained on hard ones (length, not difficulty, drives the behaviour). **Fix: the resistance-curve `rho(effort)` must be read against the VERIFIED-DISSOLVE gate (bits actually reconstructed at each budget), never against raw trace length.** Self-consistency / convergence is a cheap *verifier-free* resistance ESTIMATE but is NOT a sound substitute for the exact-reconstruction gate (convergent-but-wrong over-discounts bits) - keep it as an estimate only, reserve bit-discounting for execution-verified reconstructions. This is the same one-sided discipline as the static unit.

### 11.3 One framing refinement

The clean "INSTANT-CRUSH = Shannon vs SLOW-DIGESTION = Kolmogorov" dichotomy is **better stated as COMPUTABLE-single-pass (cheap, leaves residue) vs COMPUTE-BOUNDED program-search (expensive, dissolves *verifiable* residue)** - because single-pass NLL *already* approximates Solomonoff/Kolmogorov (Wan-Mei 2505.15784). Both ends approximate the same uncomputable ideal; **the dial is compute spent, not Shannon-vs-Kolmogorov in principle.** This is cleaner and matches the COIN `p = 2^-bits = render-in-log2` axis (the residue is a budget-relative upper bound, monotone-decreasing as the digesting mind improves).

### 11.4 What stays genuinely novel (foreground this)

The field has each piece - KT residue, structure-function residual, the faithfulness gate, reasoning-effort metrics, PVI - but has **not fused them into one observer-indexed `measured_bits` law where the digestion-trace is the conjugate dual of the residue.** PVI is a scalar; our **digestion-trace is PVI made process-valued and gated by verified-dissolve.** Two defensible new claims: (a) the **conjugate pair** (the *amount* that resisted x the *manner/cost* of resistance, as one measurement); (b) binding **verifier-guided test-time-compute SEARCH to the exact-reconstruction gate** - KT itself notes it does single-shot generation with NO multi-sample search, so coupling TTC-search to the gate is a genuinely open, fundable move. The Latent Olympics is the spectacle of exactly this fused measurement.

### 11.5 Relabels adopted (so a reviewer cannot say "reinvented")

verified-dissolve -> **"lossless round-trip / exact-reconstruction gate (KT)"**; resistance-curve -> **"prequential codelength / EDL curve"**; dissolve events -> **"information peaks"**; the residue -> **"per-instance verified epiplexity"** (vs epiplexity's population/measure-level quantity, which has no exact-reconstruction gate and no conjugate trace - our differentiator); INSTANT-CRUSH/SLOW-DIGESTION -> the **compute dial** over one uncomputable ideal. Status: spec UNCHANGED in substance, now citation-anchored and falsifier-hardened against the noise-trap + the token-count confound.

### 11.6 External pass (codex GPT-5.5 + gemini, 2026-06-16) - demote-not-kill

Both non-Claude models CONVERGED ([[feedback_cross_model_external_pass]]; raw in `session_arc/EXTERNAL_SYNTHESIS.md`). The framing holds; three corrections land.

1. **Citations corrected + extended** (codex web-verified each ID). **LMIC = arXiv:2309.10668** (Deletang et al.). **Add the load-bearing TTC + verifier/search priors** the spec leans on but under-cited: test-time-compute scaling Snell 2408.03314; s1 budget-forcing 2501.19393; overthinking/length-confound 2412.21187 + 2502.07266 + 2604.10739; AND the search/verify lineage our "novel" move descends from - AlphaCode 2203.07814, Tree-of-Thoughts 2305.10601, self-consistency 2203.11171, process-supervision 2305.20050, RoundTripCodeEval 2601.13398; Hutter prize for the compression=intelligence flank.
2. **THE THIRD FAILURE MODE - the semantic/lossless mismatch (both, independently).** The VERIFIED-DISSOLVE gate demands *exact* reconstruction. For a target with **no canonical representation** (a concept, a claim, a narrative - i.e. most latent entities), bit-for-bit reconstruction **rewards memorizing surface syntax / incidental wording** - you measure the cost of human variance, not the algorithmic complexity of the concept (+ a Goodhart/lookup-table escape). **FIX (adopt): define an equivalence-class / canonicalizer for the target FIRST, then measure `semantic_dissolve + residual_surface_bits` separately.** This is exactly the job of the semantic LLM-coder scoped in [LLM_CODER_SCOPING.md](LLM_CODER_SCOPING.md) (reconstruct up to entailment/paraphrase equivalence, not verbatim). Until that canonicalizer exists, the gate is honest only for targets that already HAVE a canonical form (code, sequences, formal logic) - state that scope limit.
3. **Novelty demoted to a SYNTHESIS/HYPOTHESIS, not new math.** KT already owns "short program + exact reconstruction"; verifier-guided-TTC-search is execution-based program synthesis (AlphaCode/AlphaGeometry); the conjugate-trace is Levin-search + EDL/loss-curves repackaged. **The only defensible-novel claim is the *unified observer-indexed law where the digestion-trace is the conjugate dual of the residue* - and it is flagged a synthesis to test, not established mathematics.** (Also: tighten "residue == epiplexity" to "relates to" - epiplexity is bounded *structural* content; the aleatoric floor of 11.2 stays separate.)

Net: the spec is stronger and smaller-claiming. The one new build item is the **canonicalizer** (semantic equivalence-class) - without it, verified-dissolve only measures surface form on non-canonical targets.

---

## 12. The amortization principle - difficulty is conserved, shifted in time (Pav, 2026-06-16)

The whole spec measures **present effort** (the resistance curve: tokens / attempts / compute-to-crack-it-*now*). Pav's correction: that is only the visible tip. **To crunch a problem you need knowledge + strategy + compute + time - and for an easy ("low-entropy") read, the compute and time were already spent in the PAST.** The expense is shifted into the journey that built the observer's prior + tools: the training run, the education, the centuries of deriving the laws/methods that compressed the problem's structure into the prior. "Easy" does not mean cheap - it means **pre-paid**. The energy is conserved; it was spent upstream and stored as the **negentropy of the prior**, and the instant-crush just cashes it in.

So every dissolution runs on **two clocks**: PRESENT effort (the shutter - what you spend at solve-time) and AMORTIZED past effort (the film's ISO - the sensitivity you arrived with; cf [THE_LATENT_CAMERA.md](THE_LATENT_CAMERA.md) - a fast exposure resolves the image only because the film was pre-sensitized).

**This is already named in the anchors (re-derived from the cost side):**
- **Prequential MDL / EDL** IS this: codelength is paid as the model *learns* across the sequence - early items expensive, late items cheap (paid already). The Excess Description Length = the learning debt; "expense in the past" = the prequential code already spent.
- **Logical depth** (Bennett): a deep object's shortest program takes a long time to *run* = the derivation cost; once the output is cached (weights, a theorem) reproducing it is shallow. **The depth lives in the history, not the lookup.** Easy-now = deep-then.
- **Amortized inference** (distillation / meta-learning / caching): pay one large training cost to make every future inference cheap - moving cost from the present clock to the past clock.

**It dissolves "entropy depends on the observer":** the entropy reading IS the observer's **position on its own learning curve** - how much of the debt it has settled. Novice (high-entropy) vs expert (low-entropy) on the *same* problem = unpaid vs paid. A 1789 mind and a 2026 mind read the same fact at different sharpness because one paid the derivation and one did not (the diachronic decoder `D(t)`, now with a price tag). Observer-relativity = **whose debt is already settled**, not fuzz.

**The measurement consequence (two honest instruments):**
1. **how-hard-for-THIS-mind-now** = the present resistance tip, against a **pinned observer** (this is *why* `measured_bits` must pin the decoder - difficulty is undefined until you declare whose paid-up budget you measure against).
2. **INTRINSIC hardness** = **sum the debt** = present effort + amortized derivation cost (the logical depth / compute-to-build-the-tools). Present-effort alone **systematically under-counts the deep, structured problems** - the very ones that look easy because civilization already paid for them.

**Thermo tie (closes `e-units-weld`):** the bits you read for free now were **Joules spent then**; difficulty is a **stored potential, conserved across the time-shift** - Landauer with a memory of how it got cheap. This is a COST-law, and it sits alongside the render-laws of [[project_latent_camera]]: the render-laws (fidelity / sharpness<1 / generate-above) govern what the film *shows*; the amortization principle governs what the exposure *cost* - most of it paid before the shutter opened.
