# Is there a physics-equivalent for the latent space? — a candidate research program (PROGRAM)

> **Status:** Tier-3 EXPLORATION / candidate research program, surfaced for **Cowork+Pav ratification**. NOT canon, NOT a continuation, NOT a promotion, NOT a build, NOT a 10th convergence. Register: **narrow-factual** (audit v08 §C7 — no grand/celebratory closure). **Default-to-fold** (audit v06 §10.4): each rail below is a *mature existing field*, so each piece **folds**; only the *binding instrument* is candidate-new. The cross-substrate convergence list **stays 9**; nothing is compiled. Single-agent surface (Claude Code) — **owes a cross-model external pass** (GPT-5.5 + Gemini), per the standing rule. Authored 2026-06-10 at Pav's 2026-06-10 steer (the "is there a model-equivalent of physics for the latent space?" question + the recursive focus-the-fuzzy simulation loop + the divergent-rule-sets / spectrum-gradient instinct).
>
> **One-line answer (stated up front):** **No unified physics-of-the-latent-space exists as a named field.** What exists is a set of **mature, disjoint fragments**, each owning one regime and each able to forecast within its slice. Pav's three instincts land *squarely and correctly* on three of those mature rails — they are **good analogies, not coincidences, and they are COVERED, not new**. The genuinely-uncovered part is exactly the **integration layer**: one frame-relative formalism that makes drift laws, stochastic dynamics, denoising compiles, and regime-detection slices of the *same* object, **bound to the genealogy render-system**. That binding instrument — not any single piece — is where the framework program would be new. This is **consistent with, and re-confirms from the outside, the standing `instrument-not-field` verdict** (`latent_cosmology_EXPLORATION.md`, triple-converged Claude + GPT-5.5 + Gemini).

---

## §0 — What was asked

Pav (2026-06-10), three parts:

1. **Viewer / motion** — observers are wrappers; theories are wrappers *anchored* to physical observers in the latent. Ideas **attract and repel** (conflict / union); there are **phases** of change; **+/- unions of various flavours**; beyond squeeze and pull a whole **spectrum of force** whose effect is **magnified by how big the idea is**. Something fuzzy can vanish like a **mirage**; **solid = kernel canon** and solidity is **observer-relative** (depends where you stand relative to it and your harness). Objective: **capture that in the VIEWER as the timeline moves**, made visually cohesive.
2. **Physics-equivalent + simulation** — given the standing verdict "not new physics": is there a **model-equivalent of physics for the latent space**? If we can probabilistically model its dynamics up to the present with a **sharp/fuzzy ratio**, can we **run simulations** to infer probabilities of what happens next as new data streams in to focus the fuzzy — **frame by frame, fill data, improve fidelity, refine the instrument iteration by iteration**, results frame-dependent, developed **recursively in a loop**.
3. **Instinct** — some frames have **divergent rule sets** (quantum vs GR equivalent), but with enough **frame slices** we can construct a **spectrum** and a **gradient** and begin to infer the underlying dynamics.

The honest, in-framework way to answer (2)/(3) is a **census of the existing fields** that already model idea/latent dynamics probabilistically, then **name Pav's instincts against those rails** and report the covered-vs-new residue straight. That is what follows.

---

## §1 — The census table (the rails)

Three independent census panels (web-grounded) converged on the same picture: **fragments-only, no unified field.** Consolidated, de-duplicated, and tagged by **which Pav element each rails**:

| # | Field / rail | What it models (one line) | Key works | Maturity | Rails which Pav element |
|---|---|---|---|---|---|
| 1 | **Recursive Bayesian estimation / Kalman filter** | Predict-then-update: propagate state + uncertainty through a known model, correct on each observation, recursively. | Kalman 1960; Kalman-Bucy 1961 | Mature / textbook | **Instinct (a)** the focus-the-fuzzy loop, Gaussian-linear core. Posterior covariance **= the sharp/fuzzy ratio**; Kalman gain **= how new data "focuses the fuzzy."** |
| 2 | **Sequential Monte Carlo / particle filters** | Nonlinear, non-Gaussian recursive Bayes: posterior as a weighted cloud of particles (hypotheses); reweight on each obs, resample to kill low-prob ones. | Gordon-Salmond-Smith 1993; Doucet-de Freitas-Gordon 2001 | Mature (SLAM, tracking, finance) | **"Model the fuzzy compile in ALL the vectors"** — a particle = one candidate future weld; resampling = fuzzy collapsing to sharp. Handles **divergent multi-hypothesis futures** natively. |
| 3 | **Data assimilation — EnKF & numerical weather prediction** | Operationally fuse a high-dim simulation with streaming observations, cycle by cycle; ensemble spread = explicit fuzzy estimate. | Evensen 1994; Houtekamer-Mitchell 1998/2001 | Mature (runs daily at ECMWF/NOAA) | The **literal real-world instance** of "work frame by frame, fill data, improve fidelity, refine the instrument iteration by iteration." Weather forecasting **is** recursive refinement of a fuzzy field as observations focus it. |
| 4 | **Variational assimilation (4D-Var)** | Fit a whole trajectory to all observations in a window by minimizing a cost function — the window-fit variant. | Le Dimet-Talagrand 1986; Talagrand-Courtier 1987 | Mature (the other operational NWP paradigm) | "Model dynamics **up to the present** then simulate forward" = window-fit-then-forecast. Supplies the adjoint/optimization machinery to **back-fit the latent timeline**. |
| 5 | **Latent SDEs / neural ODEs** | Continuous-time hidden-state dynamics: drift (deterministic field) + diffusion (noise) learned from irregular obs, with a probabilistic posterior over futures. | Chen 2018; Rubanova 2019; Li 2020; Kidger 2020-21 | Established tooling (torchsde/diffrax); high-dim scaling active | The most direct rail for **(2)'s simulation engine**. **drift = sharp/solid component; diffusion = fuzzy component**; "probability of the fuzzy compile in all the vectors" = posterior over forward-simulated trajectories. |
| 6 | **World models (Ha-Schmidhuber, Dreamer)** | Learned latent dynamics of an environment; imagine forward rollouts, act in the dream, retrain as experience streams in. | Ha-Schmidhuber 2018; Hafner PlaNet/Dreamer→V3 2019-25; LeCun JEPA 2022 | Mature in RL; industrializing via video world models | The **full recursive loop** of (2): simulate→infer→fill data→improve fidelity each pass→refine the instrument. Also the rail for the **viewer** — rendering imagined rollouts as cohesive motion is what Dreamer decoders do. **Instrument, not field** (per-environment). |
| 7 | **Diffusion / score-based SDEs as latent dynamics** | The fuzzy↔sharp transform itself: forward SDE noises data to fuzz; learned reverse SDE / probability-flow ODE sharpens fuzz to samples; noise level = continuous LOD dial. | Sohl-Dickstein 2015; Ho 2020 (DDPM); Song 2021 (SDE); Rombach 2022 (latent diffusion) | Very mature / industrial | The **fuzzy-compile mechanic**: "new data focuses the fuzzy, each pass improves fidelity" ≈ a **reverse-diffusion denoising pass**; fuzzy-LOD ≈ the noise schedule. The **MIRAGE** = a region with no mode under the reverse SDE (structure in the fuzz that does not survive sharpening). **Song 2021 is the precedent for unification-by-SDE** (two divergent rule sets — SMLD, DDPM — shown to be slices of one SDE spectrum: a worked miniature of instinct (3)). |
| 8 | **Diachronic word embeddings / semantic drift** | Word meanings as points in an aligned space; drift = measured trajectories across time slices. Found statistical *laws of motion* (conformity, innovation). | Kulkarni 2015; Hamilton-Leskovec-Jurafsky 2016; Kutuzov 2018; SemEval-2020 Task 1 | Mature (~10 yrs, shared tasks) | The rail for **(1) idea-motion** and the **timeline viewer**: ideas as tracked objects moving frame-by-frame. **Law of conformity** (drift rate ∝ 1/frequency; big/entrenched ideas move slower) is the empirical anchor for Pav's **"force effect changes with how big the idea is"** (bigger = slower = more SOLID). Alignment-across-snapshots **is** the literature's observer-frame problem (trajectories exist only after choosing an alignment frame — results frame-dependent). |
| 9 | **Concept-drift detection / adaptive stream learning** | *When* the data-generating distribution shifts under a deployed model: sequential-stats / adaptive-window detectors flag regime change and trigger retraining. | Gama 2004 (DDM); Bifet-Gavalda 2007 (ADWIN); Gama 2014; Lu 2019 | Mature (production ML monitoring) | Rails **(3)'s divergent rule sets** and **(1)'s PHASES**: drift detection is the formal machinery for noticing a frame's local rule set has stopped applying (regime boundary); adaptive windows = operationalized frame slices. Within (2)'s loop it is the **trigger** for when to recalibrate. Drift taxonomy (sudden/gradual/recurring) = vocabulary for the weld-lifecycle phase transitions. |
| 10 | **Renormalization Group (Wilsonian coarse-graining)** | Why different scales obey different effective rules and how rules *flow* as you zoom: integrate out short-distance DOF, get an effective action at the next scale. | Kadanoff 1966; Wilson 1971; Wilson-Kogut 1974 (Nobel 1982) | Mature / foundational | The canonical **spectrum-across-scales** machinery for **instinct (3)**: divergent rules per frame, slices → spectrum → gradient. Maps onto **fuzzy-LOD-as-zoom** and the R3 "one weld at coarse grain = chain of sub-welds zoomed in" already in the genealogy specimens. |
| 11 | **Effective Field Theory (theory-per-regime)** | Each regime gets its own predictive theory valid up to a cutoff; microscopic detail enters as a few coefficients. | Weinberg 1979; Donoghue (EFT of gravity) | Mature (modern organizing principle of physics) | Pav's **quantum-vs-GR divergent rule sets** is the textbook EFT/non-renormalizability case — and is **already in the repo's `qm_relativity` specimen** ('t Hooft-Veltman 1973; Goroff-Sagnotti 1985-86). EFT = "a valid local theory per frame, stitched into a spectrum." |
| 12 | **Emergence / "More is Different"** | New, partly-irreducible laws at each level of organization; reduction ≠ construction. | Anderson 1972 | Mature as philosophy-of-science; quantitative law of emergence still open | The warrant for why frame-slices can have **genuinely DIVERGENT** rule sets (not merely rescaled). Underwrites the **synergy gate as an emergence criterion**. |
| 13 | **Science of science / scientometrics** | Literature as a measurable system: citation dynamics (fitness × aging × preferential-attachment), recombination, careers; forecasts long-term impact from early citations. | Wang-Song-Barabasi 2013; Fortunato 2018; Wang-Barabasi 2021 | Mature; forecasting contested on high-impact tails | The forecasting backbone for **(2)**, and a candidate physics for **(1)'s "how big the idea is" magnifies force** (fitness × preferential-attachment). Closest external analogue to a latent-instrument that **improves fidelity as citations accrue**. |
| 14 | **Opinion dynamics (DeGroot + bounded-confidence)** | Opinions evolve on a network: next opinion = weighted average of neighbours; bounded-confidence variants only let agents influence each other within a threshold → consensus / polarization / fragmentation. | DeGroot 1974; Hegselmann-Krause 2002; Deffuant 2000; Bernardo 2024 | Mature mathematical-sociology / control theory | The **literal formal home of (1)'s ATTRACT/REPEL** and union/conflict: bounded confidence **is** a threshold force law (ideas within range attract/average, outside → no effect / effective repulsion / **mirage-disappearance**). The confidence threshold = the **relative-reference-frame / harness distance** that makes solidity observer-relative. Cluster count = the **phases / flavours of union**. |
| 15 | **Memetics / epidemiology of ideas** | Ideas as contagions on a network (SIR/SEIR); estimate a reproduction number / adoption curve, forecast saturation and decay. | Goffman-Newill 1964; Bettencourt 2006 (Feynman diagrams); Wang-Wood 2011 | Epidemic-of-ideas layer active; "memetics-as-theory" abandoned | The **time-axis of the viewer**: rise / spread / saturation / fade as the timeline moves. **Mirage-disappearance** = the Recovered/decay tail; **solid canon** = an endemic high-prevalence state in observers' frames. SEIR's **Exposed** class models the **fuzzy-not-yet-compiled** latent state before adoption. |
| 16 | **Combinatorial-novelty scientometrics** | Novelty = statistical (a)typicality of combinations of prior knowledge vs a randomized null; predict impact from novelty/conventionality mix. | Uzzi 2013 (17.9M papers); Foster 2015; Wang-Veugelers-Stephan 2017 | Mature; the **external baseline-to-beat** (already in canon) | Direct prior art for the **genealogy/weld core**: the existing operationalization of "atypical combinations of prior knowledge" = the +/- unions / weld lifecycle. Its **null-model randomization** is the template for **(2)'s sharp/fuzzy-ratio scoring of a candidate compile**. Per `latent_cosmology_EXPLORATION.md` the bar is to **beat plain PID / Uzzi at distinguishing a real weld from a blend**. |
| 17 | **Digital twins** | A live model kept synchronized to a physical system by streaming data, simulated forward to steer; engineering packaging of the assimilation loop. | Grieves 2002/2014; Grieves-Vickers 2017 | Mature in industry | **Already named in the repo** (`continuations/00_checkpoint.md §7.8`: "real-time data-integrated models, simulation as control surface"). The **productized form of Pav's recursive viewer-instrument** — engineering, not a science of "latent twins." |

**Sociophysics + embedding-geometry + conceptual-blending-as-colimit** (Galam/Sznajd/Deffuant; Tshitoyan 2019; Goguen/Fauconnier-Turner) are the same fragments seen from the "physics-of-ideas" side; **big-history energy-rate-density** (Chaisson) is the only unified-*scope* attempt and it is a **narrative metric, not a dynamical physics.** None of these is a unified field either.

---

## §2 — Pav's three instincts, NAMED against the rails

### Instinct (a) — the recursive focus-the-fuzzy loop **= Data Assimilation / sequential Bayesian filtering**

Pav: *"model to present, simulate forward probabilistically, new data focuses the fuzzy, refine, repeat frame-by-frame, sharp/fuzzy ratio."*

This is **precisely** data assimilation, in order of increasing fit:

- recursive Bayesian estimation → **Kalman filter** (Kalman 1960) for the Gaussian-linear case
- → **particle filters / SMC** (Gordon-Salmond-Smith 1993) for the non-Gaussian, **multi-hypothesis** case ("the fuzzy compile in ALL the vectors")
- → **EnKF and operational NWP** (Evensen 1994; Houtekamer-Mitchell 1998/2001) — the literal working instance
- → **4D-Var** window-fit (Le Dimet-Talagrand 1986) — "model up to the present then forecast"
- → **digital twins** (Grieves 2002) — the productized packaging.

The dictionary is exact:
- **sharp/fuzzy ratio** = posterior covariance / ensemble spread / particle degeneracy
- **"focus the fuzzy as data streams in"** = the Kalman/Bayes update step
- **"frame by frame, improve fidelity"** = the assimilation cycle.

**Weather forecasting is the literal working instance of Pav's instinct (a).** It is mature; the framing **FOLDS**.

### Instinct (b)/(3) — divergent rule sets + spectrum/gradient **= Effective Field Theory per regime + Renormalization-Group flow across frame slices**

Pav: *"some frames have divergent rule sets (quantum vs GR equivalent), but with enough frame slices we can construct a spectrum and a gradient and begin to infer the underlying dynamics."*

This is **Effective Field Theory** (a valid predictive theory **per regime**, up to a cutoff) plus **Renormalization-Group flow / coarse-graining** (how the effective rules *flow* as you change scale), with **Anderson-emergence** as the warrant that the rules can be **genuinely distinct, not merely rescaled**. Machinery: Kadanoff 1966 → Wilson 1971 / Wilson-Kogut 1974 → Weinberg 1979 → Anderson 1972.

The **quantum-vs-GR example Pav names is the textbook EFT/non-renormalizability case, and is ALREADY encoded in the repo's `qm_relativity` specimen** ('t Hooft-Veltman 1973; Goroff-Sagnotti 1985-86; Donoghue EFT-of-gravity). **Song 2021** is the existing *worked miniature* of the spectrum move on the latent/generative side: two divergent generative rule sets (SMLD, DDPM) unified into one continuous SDE — slices → spectrum → underlying dynamics. The framing **FOLDS**.

**Four hard caveats this rail donates (instinct (3) over-claims without them):**

1. **The hard direction is blocked by an RG theorem.** "Enough frame slices → reconstruct the *underlying* dynamics" is the **inverse of RG flow**, and RG is a **semigroup**: coarse-graining destroys information irreversibly. The forward (micro→macro) direction is well-posed; the inverse is **not** in general. So a spectrum-of-slices buys an **effective description per frame** (real, useful) but **NOT guaranteed recovery of the deep law.** State this or instinct (3) over-reaches.
2. **Single-axis vs multi-axis scale.** RG flows along **one** control parameter (energy/length). Pav's frames are a **multi-axis** basis `{time, space, knowledge, meaning}`; there is **no off-the-shelf RG over a knowledge/meaning axis** — building one is new work, not a relabel.
3. **Divergent ≠ rescaled.** Anderson-emergence licenses *genuinely* distinct frame rule sets (the synergy/weld gate is an emergence criterion in this lineage), but only **qualitatively** — there is no quantitative law of emergence yet.
4. **Regime boundaries are detectable but not derivable.** Concept-drift detection (rail 9) tells you **when** a frame's rule set stops applying; it does not hand you the next frame's rules.

### The sharp/fuzzy ratio **= Uncertainty Quantification + the agnostic-units sketch**

Pav's **sharp/fuzzy ratio** is the same object three rails already carry as **uncertainty quantification**: posterior covariance (Kalman), ensemble spread (EnKF), particle degeneracy (SMC), and the **drift/diffusion split** of a latent SDE (rail 5) — **drift = sharp/solid, diffusion = fuzzy.** In diffusion (rail 7) the ratio is literally the **noise level** = a continuous LOD dial.

Inside the framework this is **already half-built** as the **agnostic-units hairy-membrane sketch** (`agnostic_units_hairy_membrane_SKETCH.md`): the agnostic unit is a **frame-relative fuzzy RATIO within [min, max]** (dimensionless, so it travels across substrates), grounded on the KL/MDL **§IT spine** as its *normalized* reading. The membrane is **fuzzy on all sides**; reframing = **conditioning** (`H(X | more frames) ≤ H(X)`), which tightens the skin but never fully closes it — **by design, there is always some fuzz.** That is exactly Pav's "sharp/fuzzy ratio that focuses but never reaches zero."

**Honest deflation (carried from `synergy_vs_pid/` + `RATIO_FRAME_TEST.md`):** normalizing to a fuzzy ratio **killed the grid-bits quantization artifact** and fixed the separable bug (a clean frame-stable interaction measure at fine resolution) — but **normalized entropy is itself standard**, so the ratio rescues *"frame-relativity is real, not artifact"* and **does NOT** make the measure novel. Consistent with instrument-not-field.

---

## §3 — The honest verdict

**`fragments-on-solid-rails`, no unified field.**

- **No unified physics-of-the-latent-space exists as a named field.** The dynamics live in **disconnected silos** (rails 1-17): drift measurement, continuous stochastic state evolution, closed-loop forward simulation, fuzzy↔sharp transformation, regime-change detection, citation/impact forecasting, opinion attract/repel, contagion, novelty scoring. They **do not share a state space, have no conservation laws, and are instruments fit per-corpus / per-environment rather than a field theory.** This independently **re-confirms the repo's standing `instrument-not-field` verdict from the outside** (`latent_cosmology_EXPLORATION.md`; triple-converged).
- **The nearest unification precedents are partial:** Song 2021 unified two generative rule sets into one SDE spectrum (a miniature of instinct (3)); NTK / Roberts-Yaida give physics-style limits for **training** dynamics but **not for semantic content.** Big-history energy-rate-density is the only unified-*scope* attempt and is a narrative metric.
- **Pav's instincts are correctly diagnosed and COVERED:** (a) = data assimilation, (b)/(3) = EFT + RG. These are good analogies, not coincidences — which is *why* they fold.

**Where the program would be NEW — the integration layer.** None of the seventeen rails carries the **load-bearing novel moves already isolated in the repo**:
1. **Frame-relativity of the unit as a first-class indexed parameter** — `PPWc(W_A, W_B | frame)`, emergence indexed to observer-kernels `{time, space, knowledge, meaning}`. DA fixes one global state/truth; RG/EFT fixes one observable algebra. **No rail makes the frame a first-class estimand.**
2. **Observer-relative SOLIDITY** — "solidity depends where you stand relative to it and your harness." DA assumes one objective truth; RG assumes one fixed Lagrangian. **Neither has an analog**; the nearest physics is relational/QBist QM, not these. This is the **load-bearing non-overlap.**
3. **The physical/latent hybrid bridged by measured actors** (D2 actors, `SCHEMA_v2 §2.6`) — ANT and big history each touch half; tying them with a **measured emergent-unit** is the genuine "cosmological" move.
4. **The fuzzy-LOD sharp/fuzzy compile ratio** as a first-class render axis with a physical/latent filter and a time-scrubber.
5. **Refining the INSTRUMENT/FRAME, not just the state.** DA estimates state (and a few parameters) against a *fixed* model, state space, and observation operator. Pav wants to recursively refine the **observable basis itself**. The DA analog — **joint online state + parameter + model-STRUCTURE + observation-operator learning** — is a hard, only-partly-solved frontier. **This is the genuinely-unowned edge of instinct (a).**

> **Net.** Every component of Pav's instinct-(2) recursive simulation program has an **existing rail**. The genuinely-new part is the **integration**: one **frame-relative, observer-solidity-aware formalism** in which drift laws (rail 8), SDE/world-model dynamics (5/6), denoising compiles (7), regime detection (9), and the novelty/weld gate (16 + `synergy_vs_pid/`) are **slices of the same object — bound to the genealogy render-system.** The framework program is therefore best named a **SYNTHESIS INSTRUMENT** that binds the rails to the genealogy render-spec, **not** a new physics and **not** a new field. And critically (per `latent_cosmology_EXPLORATION.md §1[B]` and the `synergy_vs_pid` pilots), the binding is **gated on the still-undelivered synergy/weld measure** — the integration is unclaimed in the literature, but it is also **not yet demonstrated here.**

---

## §4 — What a v0 pilot would be (SPEC ONLY — do NOT run)

A minimal, falsifiable demonstration that the rails can be **bound** on a real substrate, frame-sliced. **Spec only; this section authorizes no run, no compile, no tier change.**

**Substrate.** A real diachronic corpus already standard in rail 8 (e.g. the Google Books / COHA-style decade slices used by Hamilton-Leskovec-Jurafsky 2016) — *or* the framework-internal **Latent Olympics DB** (`candidates/latent_olympics_data/`) if a controlled idea-corpus is preferred. **Read-only**; `candidates/frame_lock_data/` is untouched.

**Pipeline (each step = an existing rail, bound):**
1. **Drift trajectories (rail 8).** Align embedding snapshots across time slices (the alignment **is** the frame choice — log it, per the frame-lock discipline). Track each idea-wrapper as a moving object → the **viewer's timeline motion** (steer 1).
2. **Assimilation updates (rails 1-4).** Fit a latent-SDE / Kalman-style predict-update to the trajectories **up to slice _t_**; carry the **posterior covariance as the sharp/fuzzy ratio**. Roll forward to _t+1_; when the next real slice arrives, **focus the fuzzy** (Bayes update) and score the forecast. This is the **recursive loop** of steer (2), made literal on real drift.
3. **Regime/phase detection (rail 9).** Run ADWIN/DDM-style drift detection on each tracked wrapper to flag **phase transitions** (steer 1's "phases of change") and to **trigger recalibration** (when the local rule set stops applying — instinct (3)'s regime boundary).
4. **Weld-event gate (`synergy_vs_pid/`, gain_v2).** At each candidate merge of two wrapper-trajectories, compute the **held-out predictive-gain `gain_v2`** gate — `R2_oos(joint) − R2_oos(additive-backfit)` — to test whether the child is **more than a separable blend** of its parents (a real weld vs an additive merge). This is the framework's own emergence criterion, on real (correlated) parents. **gain_v2 is mandatory** (v1 false-flags every correlated merge).
5. **Frame slices (steer 3).** Repeat steps 1-4 under **multiple observer-kernel frames** (at minimum: time-view vs a context/relevance-cutoff frame, per the **REAL-AND-PRINCIPLED contextual frame-relativity** in `synergy_vs_pid/CONTEXTUAL_FRAME_TEST.md` — range-framing can hide a real interaction but **never manufacture one**, one-directional). Assemble the per-frame weld verdicts into a **spectrum** and look for a **gradient** — the instinct-(3) move, with the **RG-irreversibility caveat (§2)** stated: a spectrum yields an effective per-frame description, **not** guaranteed recovery of a deep law.

**Pre-registration (the load-bearing discipline).** Before any number is computed: **lock the frame, the category's morphisms, and the coding resolution** (`frame_lock_protocol_DRAFT.md`); file a content-hashed / git-strict-ancestor lock with **called shots** (`frame_lock_pilot_RESULTS.md §g`). Without this the synergy verdict is post-hoc-gameable (the triple-converged #1 residual).

**Success / kill criterion.** The pilot **succeeds** only if the bound instrument **beats plain PID / Uzzi** at telling a real weld from an additive blend on the real corpus, **frame-sliced**, with the forecast-scored assimilation loop adding predictive value the static novelty z-score lacks. If it cannot beat Uzzi, **the novelty narrows further** and the program stays a vocabulary, not an instrument. **Negative results are reported straight.**

**Viewer deliverable (steer 1).** The pilot's output is the **timeline VIEWER**: tracked wrappers as moving splats (`latent_cosmology_EXPLORATION.md §4` camera/focus system), **splat-spread = the sharp/fuzzy ratio**, drift = motion, weld-events = the gain_v2 glow (driven by the **qualitative** surprise field with a visible "not-yet-quantified" marker — never rendered as measured bits), phase transitions = drift-detector flags, **solidity = observer-relative opacity** keyed to the active frame.

**Constraints (held).** Controlled / real-corpus only; **no PNGs, no matplotlib**; no torch/HF required for the gate (gain_v2 runs on numpy as in `synergy_vs_pid/`); the embedding step for a real vector space remains the deferred prerequisite for the quantitative interpretability borrows.

---

## §5 — Honest covered-vs-new ledger

**COVERED (folds — each reachable from a single mature rail):**

| Pav element | Covered by | Status |
|---|---|---|
| The recursive focus-the-fuzzy simulation loop (instinct a) | Data assimilation / sequential Bayesian filtering (rails 1-4, 17) | **Mature; folds.** Weather forecasting is the literal instance. |
| Sharp/fuzzy ratio | Uncertainty quantification (posterior covariance / ensemble spread / drift-diffusion split / noise level) (rails 1-7) | **Standard; folds.** Normalized-entropy ratio = standard (not novel). |
| "Model the fuzzy compile in ALL the vectors" | Particle filters / SMC; posterior over SDE trajectories (rails 2, 5) | **Mature; folds.** |
| Divergent rule sets + spectrum/gradient (instinct b/3) | EFT per regime + RG flow + emergence (rails 10-12); Song 2021 SDE-unification (7) | **Mature; folds** (with 4 caveats, §2). QM-vs-GR already in `qm_relativity` specimen. |
| Fuzzy thing vanishing like a MIRAGE | A region with no mode under the reverse SDE (7); SIR Recovered/decay tail (15); below-confidence-threshold in bounded-confidence (14) | **Folds.** |
| Attract / repel, +/- unions, flavours | Bounded-confidence opinion dynamics (14) | **Folds** (threshold force law). |
| "Force magnified by how big the idea is" | Law of conformity (8: drift ∝ 1/frequency) + citation fitness×preferential-attachment (13) | **Folds** (empirical: bigger = slower = more solid). |
| Phases of change / regime boundaries | Concept-drift detection + taxonomy (9) | **Folds.** |
| Recursive instrument refinement / digital twin | World models (6) + digital twins (17) | **Folds** (already named in `00_checkpoint.md §7.8`). |
| Idea rise/spread/saturation/fade on the timeline | Epidemiology of ideas (15) | **Folds.** SEIR Exposed = fuzzy-not-yet-compiled. |
| +/- union counting / novelty scoring | Combinatorial-novelty (16, Uzzi) | **Folds** — and is the **baseline-to-beat.** |

**NEW (the residue no single rail states — narrow, gated, NOT yet delivered):**

1. **The integration layer itself** — one frame-relative formalism binding rails 5/6/7/8/9/16 as slices of the same object, **bound to the genealogy render-system.** Unclaimed in the literature; **not yet built.**
2. **Frame-relativity of the unit as a first-class indexed parameter** (`PPWc | frame`) — real conceptual contribution, gated on the frame-lock discipline. *(Cross-model trim: the contextual frame-relativity is REAL-AND-PRINCIPLED but reads as **standard effect-modification statistics**, not a new phenomenon — `synergy_vs_pid/EMERGENCE_CANDIDATES_AND_FRAME.md`.)*
3. **Observer-relative SOLIDITY** — the **load-bearing non-overlap** with both DA and RG; nearest physics is relational/QBist QM, not these rails. **Defined, not demonstrated.**
4. **The physical/latent hybrid with measured actors as the bridge** — structurally argued, rests on a small specimen N.
5. **Refining the instrument/frame, not just the state** — the genuinely-unowned frontier edge of instinct (a) (joint online state+parameter+structure+observation-operator learning).

**The honest concentration:** the load-bearing novelty is the **synthesis instrument** (#1) resting on **observer-relative solidity** (#3) and **frame-as-estimand** (#2/#5) — and **all of it is gated on the still-undelivered synergy/weld measure** (`synergy_vs_pid` gain_v2 is the soundest candidate gate but is **NOT novel** — functional-ANOVA / PID-adjacent — and the **real model-merge run is still owed**). **A program, not a result.**

---

## §6 — Discipline footer (Tier-3)

Tier-3 EXPLORATION / candidate research program, **surfaced for Cowork+Pav ratification — not compiled, not promoted, not a continuation, not a build, not a 10th convergence.** **Default-to-fold honored:** each of the seventeen rails is a mature existing field and **folds**; the verdict is **`fragments-on-solid-rails`, no unified physics-of-the-latent-space** — re-confirming the standing `instrument-not-field` verdict from the outside. The candidate-new contribution is the **synthesis instrument binding the rails to the genealogy render-system**, resting on **observer-relative solidity** and **frame-as-first-class-parameter**, and it is **gated on the still-undelivered synergy/weld measure** (defined, one partial pilot in; the real model-merge run owed). The cross-substrate **convergence list stays 9**; **nothing is compiled**; no tier advances; **surprise stays qualitative** (no bits in the viewer). Single-agent surface (Claude Code) — **owes a cross-model external pass** (GPT-5.5 + Gemini) on the load-bearing claims (the rail-mappings, the RG-irreversibility caveat on instinct (3), and the "integration is the only new part" verdict), per the standing rule. This is a **NEW file**; no committed files edited; `candidates/frame_lock_data/` and any Cowork files untouched; no PNGs / no matplotlib. Web-grounded census inputs cited inline. Authored 2026-06-10.

---

## §7 — Cross-Claude review addendum (Opus)

A second Claude (Opus) audited the census + verdict + instinct-mappings against the repo and the
cited literature. The physics side was **accepted as-is** — "Sound and well-disciplined … nothing
is over-claimed; if anything it is appropriately deflationary." Recording what it confirmed and the
one upstream covered-vs-new correction that touches this program:

**Confirmed correct (verified, not just asserted):**

- **Instinct (a) → Data Assimilation / sequential Bayesian filtering.** recursive-Bayes → Kalman
  1960 → particle filters (Gordon-Salmond-Smith 1993) → EnKF (Evensen 1994) → 4D-Var
  (Le Dimet-Talagrand 1986) → digital twins (Grieves 2002). The mapping "**posterior covariance /
  ensemble spread = sharp/fuzzy ratio**, **Bayes update = focus-the-fuzzy**" is apt, **not**
  overclaimed.
- **Instinct (b)/(3) → Effective Field Theory per regime + Renormalization-Group flow + Anderson
  emergence.** Kadanoff 1966 → Wilson 1971 → Weinberg 1979 → Anderson 1972. **QM-vs-GR is the
  textbook EFT case AND is verified present in `qm_relativity.json`** (cites 't Hooft-Veltman,
  Goroff-Sagnotti, Donoghue, non-renormalizability, EFT).
- **The RG-semigroup caveat is a genuine catch and correctly applied.** Coarse-graining destroys
  information, so instinct (3)'s "enough slices → recover the deep micro law" is the **ill-posed
  inverse** and is NOT guaranteed. The census stating this (rather than letting instinct (3)
  overclaim) was flagged as the census's **strongest move.** Keep it load-bearing.
- **Song 2021** (SDE-unification of SMLD + DDPM) is a real, aptly-cited **worked miniature** of
  slices → spectrum.
- **`fragments-on-solid-rails` / no unified physics-of-the-latent-space** is consistent with the
  standing triple-converged (GPT-5.5 + Gemini + internal) `instrument-not-field` verdict in
  `latent_cosmology_EXPLORATION.md`. The uncovered residue (frame/instrument-as-estimand,
  observer-relative solidity, multi-axis non-scale "scale") is **correctly gated on the undelivered
  synergy/weld measure, not on new dynamics.**

**Upstream covered-vs-new correction (carried from the VIEWER_SPEC review, affects the shared
"observer-relative solidity" residue, item #3 above in §5):**

- The companion viewer audit's claim that the **`{kernel,canon,artefact,protocol}` quadruple was
  "never bundled"** was **overstated** — `cont 25:412` references an existing **cont-22 four-layer
  stack** `{kernel canon → compiled canon → canon artefact → function canon}`. The new contribution
  is the **`protocol` relabel + the span-as-solidity *criterion***, not the bundling. This does
  **not** change this program's verdict (observer-relative SOLIDITY remains the load-bearing
  non-overlap with both DA and RG — nearest physics is relational / QBist QM), but the "solidity"
  residue should be described as a **new criterion on an existing stack**, not a new stack.
- Relatedly, where this program or the viewer cites the **cont-13 charge Cayley table**, note it was
  **superseded to ASYMMETRIC by cont 15 §1** ("A− does the real compilation work … not symmetric").
  Any charge-driven force model inherits the asymmetric reading.

**Standing external pass (unchanged, still owed):** this remains a single-agent (Claude-only)
surface. The **GPT-5.5 + Gemini external pass** must still verify the load-bearing mappings — (a)→DA,
(b)/(3)→RG/EFT — the **RG-irreversibility caveat**, and the "**integration is the only genuinely-new
part, and it is gated on the undelivered gain_v2 synergy measure**" verdict. The review explicitly
notes the pilot "reads more shovel-ready than it is until that measure runs on a real corpus with
pre-registration" — so the pilot stays SPEC-ONLY. **Convergence list stays 9; nothing promoted.**
Addendum date: 2026-06-10.

*End program.*

---

## Cross-model addendum (2026-06-10): the owed external pass RAN

See `latent_physics_CROSS_MODEL_REVIEW.md` for full verdicts (GPT-5.5 + Gemini). Both mappings CONFIRMED ((a)->DA "the precise machinery"; (b)/(3)->RG/EFT with the semigroup caveat "correctly identifies the lossy, ill-posed inverse"); fragments-only CONFIRMED (add cognitive science / semantic-change + information geometry + manifold learning to the census). ONE DOWNGRADE folded: observer-relative solidity is NOT analog-free everywhere - no analog in the dynamics rails (confirmed), but epistemology supplies adjacent analogs (perspectival realism, Bayesian credence, active inference, QBism); the new move is making it a first-class parameter of a dynamics instrument, not the concept itself. SHARED RISK (both models): no conserved Hamiltonian/metric in idea-space -> the mapping is metaphor, non-predictive, until the pilot operationalizes explicit state + observation operators, pre-registered, gain_v2-gated. External pass debt for this doc: PAID.
