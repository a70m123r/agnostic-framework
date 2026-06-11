Model: OpenAI Codex, GPT-5.

**1. Independent Verdict**

Not sound, not lockable, not runnable as written.

The design is a useful research skeleton: heredity and niche-presence are treated as matched frame-relative classifiers, and the drafts correctly recognize that the lock must bind the dial settings, predictions, and scoring rule. But the runnable experiment does not yet exist. The scoring statistic is placeholder/ambiguous, the Q/Q_c/E estimators are still TBD, the substrate corpus is deferred, “first opportunity” is not operationalized, and the compiled artifact contract is broken. See [heredity_classifier_section_DRAFT.md §H.6-H.7, §H.10], [niche_presence_classifier_section_DRAFT.md §N.7, §N.10], [WORKFLOW_PROTOCOL_DRAFT.md §2-§3], and [adversarial_substrate_dynamics_BAR_A_SKETCH.md §5.1-R].

Blunt version: locking now would lock a vocabulary and ceremony, not a falsifiable census.

**2. Audit Of REVIEW_v1 Blocking Faults**

**B1: CONFIRM.**  
The panel is right that raw “concordance” is structurally biased toward PASS/INCONCLUSIVE. H.7 says BELOW/UNDEFINED should agree with niche-absent, while N.1 says co-UNDEFINED cells are excluded; that contradiction alone makes the statistic undefined. The panel slightly overstates “selected on units of selection” because no corpus is actually locked yet, but the illustrative design and deferred corpus leave exactly that failure mode open. [heredity_classifier_section_DRAFT.md §H.7], [niche_presence_classifier_section_DRAFT.md §N.1], [REVIEW_v1.md §2 B1]

**B2: PARTIALLY CONFIRM.**  
The circularity risk is real: heredity is anchored on Eigen-style Q/Q_c, and the strongest niche exemplar is RNA-world/Eigen parasite dynamics. As written, the molecular positive can become one theoretical structure read twice. The panel overstates the strict identity claim: Eigen error thresholds and parasite takeover are related quasispecies/replicator physics, but not necessarily the same inequality unless the implementation makes Q, a, host order, and beneficiary identity coextensive. The draft currently fails to prevent that collapse. [heredity_classifier_section_DRAFT.md §H.2-H.3], [niche_presence_classifier_section_DRAFT.md §N.3, §N.7], [adversarial_substrate_dynamics_BAR_A_SKETCH.md §5.1-R], [REVIEW_v1.md §2 B2]

**B3: CONFIRM.**  
The workflow says instruments consume compiled JSON and maps dial axes onto SCHEMA_v2 structural fields, but the compiler emits subject-grouped predicate/value facts, not the structural frame/actor/layer fields. I independently checked `compile_substrate.py`; `write_compiled_exports()` emits `predicate`, `value`, `when`, `bucket`, `certainty`, `source`, and provenance refs under `subjects`. The specimen JSON contains `frame_layer` and `actors`, but the compiled contract does not. [WORKFLOW_PROTOCOL_DRAFT.md §2-§3], [compile_substrate.py `write_compiled_exports`], [REVIEW_v1.md §2 B3]

**3. What The Claude Panel Missed**

The biggest miss: the proposed statistic changes the estimand. §5.1-R is stated as a near-universal boundary claim: every above-heredity substrate grows a niche, below it does not. A conditional contrast Δ tests association, not universality. A single well-adjudicated above/absent or below/present counterexample should be dispositive, not merely lower Δ. [adversarial_substrate_dynamics_BAR_A_SKETCH.md §5.1-R], [REVISION_v1_upstream_DRAFT.md Fix 1.2, Fix 1.6]

Second: the heredity threshold is mathematically under-specified outside narrow molecular cases. `Q_c = 1/a` ignores genome length, mutation distribution, neutral networks, population structure, drift, recombination, and the distinction between per-site and whole-replicator fidelity. Porting that directly to oral traditions, institutions, or latent renderings is not an estimator; it is an analogy awaiting an estimator. [heredity_classifier_section_DRAFT.md §H.2, §H.9]

Third: conditioning on “both instruments DEFINED” creates selection bias. If definability itself depends on recognizability of a replicating unit and compiled order, then Δ is estimated only after filtering on variables related to both heredity and niche detectability. That weakens the “below the heredity line it does not” arm. [niche_presence_classifier_section_DRAFT.md §N.1-N.2], [REVISION_v1_upstream_DRAFT.md Fix 1.1]

Fourth: the permutation null proposed in Revision v1 is not exchangeable. Cells are nested within substrates, planes, observer levels, and copy lenses; shuffling niche labels across all scorable cells treats dependent cells as independent observations. That can manufacture significance from grid granularity. [REVISION_v1_upstream_DRAFT.md Fix 1.5], [heredity_classifier_section_DRAFT.md §H.1, §H.4]

Fifth: “first opportunity” remains mostly ceremonial. The claim includes first-opportunity timing, but H.7 calls it an ordinal companion and defers full operationalization; N.10 also defers it. A census that only estimates co-presence does not test the temporal/rung-onset part of §5.1-R. [adversarial_substrate_dynamics_BAR_A_SKETCH.md §5.1-R], [heredity_classifier_section_DRAFT.md §H.7], [niche_presence_classifier_section_DRAFT.md §N.10]

**4. Evaluation Of REVISION_v1 Fixes**

**Fix 1: Δ + permutation null.**  
Directionally right, insufficient. It correctly removes co-UNDEFINED inflation, names a statistic, adds power gates, and makes FAIL reachable. But it redefines a universal falsifier into a probabilistic association test, inherits exchangeability problems, and risks burying counterexamples inside an aggregate. The better design is: primary endpoint = pre-registered counterexample adjudication; secondary endpoint = Δ or odds ratio with cluster-aware permutation by substrate/stratum. [REVISION_v1_upstream_DRAFT.md Fix 1.1-Fix 1.8]

**Fix 2: native census-substrate record.**  
Correct and necessary. A hurricane, RNA-world pool, or cultural tradition is not a genealogy merge specimen, so dropping SCHEMA_v2-specimen conformance is the right walk-back. The new risk is fragmentation: a native record needs its own schema, compiler contract, validation harness, and lock inputs, or “bind, don’t fork” just becomes a slogan. [REVISION_v1_upstream_DRAFT.md Fix 2], [WORKFLOW_PROTOCOL_DRAFT.md §1-§3]

**5. Single Most Important Next Step**

Before touching estimators, write and ratify the estimand/counterexample protocol: unit of analysis, what counts as a decisive FAIL, how universal §5.1-R differs from an association Δ, and which native census records must exist before the run is admissible. Without that, every downstream fix can still produce a polished but non-falsifying census.