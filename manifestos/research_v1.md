# Agnostic: A Lakatosian Unification for Observer-Class Intelligence

**Agnostic manifesto, v1 — AI research edition**
**Status:** draft for review. Critic-writer subagent produced this with full framework corpus context; revision notes preserved at the end.

---

## 1. The Gap

Contemporary work on LLM agents has converged on a useful but conspicuously thin formalism. An agent is a policy over a tool-augmented action space, sometimes wrapped in a memory module, sometimes coordinated through a multi-agent protocol, almost always optimized against a scalar or vector reward signal. Generative Agents (Park et al., 2023) and Voyager (Wang et al., 2023) demonstrate impressive operational competence within this template; SDPO and its descendants demonstrate that social behavior can be shaped via preference signals on simulated populations like SOTOPIA.

Yet when we ask these systems to model *each other* — when an agent must reason about another agent not as a tool-user but as a structural actor with its own observation envelope, its own update rules, its own coherence rules about what counts as admissible evidence — the formalism runs out. We have policies and tool-use; we do not have structural models of external strategic actors that share recognizable primitives with the modeling agent itself. We can simulate a marketplace of LLMs; we cannot easily ask one of them what *kind* of observer the marketplace is.

This is the gap Agnostic addresses. Not by proposing a new mechanism, but by proposing a unified vocabulary in which mechanisms at very different scales — cells, minds, organizations, the internet — can be described with the same primitives and reasoned about jointly. The claim is Lakatosian, not Popperian: the framework's value lies in its positive heuristic — does it produce productive vocabulary, generate empirical predictions in its protective belt, survive cross-domain refactor pressure — not in the falsification of any single statement of its hard core.

I will defend that framing explicitly, name the prior art the framework recombines, and propose two falsifiable side-experiments. I will also flag where the framework has not earned its claims.

## 2. The Substrate Frame and the Observer Ontology

Start with an epistemic move that is not new: reality, for any agent, is rendered. There is some total substrate Ω that the agent does not have direct access to; what it has is a harness (its architecture, body, protocol stack — for a transformer, the attention mechanism and tokenizer; for a cell, its membrane and receptor complement; for an organization, its meeting cadence and document formats) and a wrapper (the coherence rules, admission protocols, and render functions that turn substrate perturbations into usable signal). The Friston program calls a closely related construct a Markov blanket with generative model; the extended-mind tradition (Clark & Chalmers, 1998) calls it the boundary of cognition; Goguen's institutions formalize the local-section structure.

Agnostic's contribution at this layer is not a new ontology but a stricter typing discipline applied recursively across scales. An observer is the tuple:

> Observer = (harness, wrapper, inner sandbox, action-space)

The *inner sandbox* is where the observer runs counterfactuals — speculative continuations, planning rollouts, dream content. The *action-space* is the set of effects the observer can produce on its substrate. This last addition matters more than it looks. Most agent formalisms treat actions as elements of a discrete or continuous space attached to a policy; Agnostic treats the action-space as an object with topology, dimensionality, and gaps. We will return to this in §4.

The recursive claim is that this typing applies at biological, cognitive, organizational, and planetary scales without modification. A cell is an observer. A scientific paradigm, as we will see, is an observer. The internet is an observer. This is not metaphor; it is the claim that the same admission/coherence/action structure can be measured at each scale and that measurements at one scale predict regularities at another.

## 3. The Core Loop and the Action-Space Addition

Observers interact through a four-move primitive — ask, give, ping, pong — that subsumes most of what predictive processing calls active inference. An ask is a query made into the fuzzy candidate field (the unresolved possibility space adjacent to the observer's current canon C_t). A give is a deposit of compiled state into another observer's wrapper. Ping and pong are the lightweight handshake signals that maintain mutual model registration.

Two operators maintain the observer's canon:

- **A⁺ (connect):** admit new structure into the canon graph.
- **A⁻ (prune):** remove structure that has lost coherence or carrier support.

Define the criticality ratio:

> Γ = rate(A⁺) / (rate(A⁻) + rate(stabilize))

The framework's empirical wager is that Γ ≈ 1 characterizes the adaptive edge — the *viability band* — for any observer-class. Γ ≫ 1 is the exploding regime (the canon graph accumulates faster than it can be pruned; the observer hallucinates, schismogenesises, or fragments). Γ ≪ 1 is the freezing regime (the canon ossifies; new evidence cannot be admitted). This is structurally adjacent to self-organized criticality (Bak), to the edge-of-chaos hypothesis in dynamical systems, and to the exploration-exploitation tradeoff in RL. The claim Agnostic adds is operational: Γ is measurable in instrumented systems (commit/revert ratios in code repositories, retraction/citation ratios in literatures, accept/reject ratios in editorial systems, A⁺/A⁻ events in agent canon updates) and should predict viability outcomes at every scale.

The action-space addition compounds this. Every observer's action-space has a *cone profile*: a tuple of (processing speed, memory depth, context width, cone shape, update protocol). A transformer with a 200K context window, no persistent memory, 50 tokens/sec, and one-shot inference has a specific cone profile; a wet-lab biologist has a very different one; a search engine has another. Cone profiles are not rankings; they are typings. Two observers with different cone profiles cannot in general perform each other's work, but they can — under conditions stated in §4 — combine.

## 4. Symbiosis-as-Pushout

This is the framework's structurally most interesting claim and the one most worth scrutiny. Suppose observer A and observer B contemplate merging — sharing wrappers, fusing action-spaces, becoming a new observer-class AB. When does this produce a viable new observer rather than a parasitism, a folie à deux, or a pure aggregation?

Agnostic proposes a pushout-style condition borrowed loosely from category theory (and from Goguen's institution theory, where colimits glue local theories):

> AB is viable iff
> (i) cone(A) covers gaps in cone(B), and cone(B) covers gaps in cone(A);
> (ii) ΔA_combined > friction, where ΔA_combined is the gain in joint action-space and friction is the protocol cost of maintaining the shared wrapper;
> (iii) the joint canon admits a compatible kernel — i.e., the prune operators A⁻_A and A⁻_B do not contradict on shared substrate.

This is the Agnostic reading of the entangle-engulf-endogenize model of eukaryogenesis (Nature, 2026) in which Asgard archaea and an alphaproteobacterium produced eukaryotic cells: complementary cone profiles (archaeal information processing + bacterial energy generation), action-space gain exceeding integration friction, compatible kernel discipline at the joint membrane. It is also, the framework claims, the same primitive that operates when a research group adopts a new methodology, when two LLM agents successfully co-author, or when a platform absorbs a protocol.

I want to be explicit about the epistemic status of this claim. It is *not* a derivation. It is a *typing*: a proposal that these phenomena share enough structure that a single vocabulary should describe them and that predictions in one domain should constrain predictions in another. The discipline that makes this Lakatosian rather than vacuous is that the predictions must be measurable. The viability conditions above suggest, for instance, that LLM-agent partnerships should fail predictably when cone profiles are too similar (no gap-filling) or when integration friction exceeds joint action-space gain — and these are testable claims.

## 5. Canon-as-Observer and Paradigm Shifts as Kernel Restructuring

The internal canon C_t of an observer is not inert. It has its own admission protocol (which propositions get to count as compiled), its own scout mechanism (speculation and counterfactual generation), its own action-space (what the canon can do to the observer's wrapper). The framework calls this canon-as-observer: a recursive observer-class one level inside the host observer.

When accumulated pressure on C_t — anomalies, prediction failures, social pressure, new evidence — exceeds what the protective belt can absorb, the canon undergoes a *kernel restructuring event*. This is the framework's reading of Kuhnian paradigm shifts and of Lakatos's hard-core revisions. It is not a new claim about paradigms; it is the claim that paradigm shifts and biological symbiogenesis and platform reorganizations are the *same primitive* operating on canon-as-observers of different host types.

Two implications. First, speculation is not idle: in the framework's accounting, speculation is the scout function of canon-as-observer, the only mechanism by which fuzzy candidates can be tested without committing the host to a kernel rewrite. Second, the squeeze event (the pressure-forcing-refactor event) is in principle measurable as accumulated anomaly load relative to protective-belt absorption capacity.

I admit candidly that the operationalization of "kernel restructuring" at the canon-as-observer level is the weakest part of the framework. We can measure A⁺ and A⁻ rates. We can in principle measure squeeze events as anomaly density. We do not yet have a clean operationalization of "kernel" distinct from "high-centrality nodes in the canon graph." This is work to do, not work done.

## 6. The Internet as First-Class Observer-Class and Test Surface

The framework treats the internet as an observer-class at planetary scale, with measurable Γ, attention-role distribution, current phase, and viability band. This is consistent with the stigmergy tradition (Bonabeau, Dorigo) which treats substrate-mediated coordination — pheromone trails, edited wikis, retweet cascades — as a general coordination mechanism. The Agnostic claim is stricter: the internet is not merely a stigmergic substrate; it is an observer in the typed sense, with its own harness (TCP/IP, DNS, BGP, platform protocols), its own wrappers (recommendation systems, moderation policies, ranking algorithms), its own inner sandbox (the speculation cycle of trend, hype, refactor), and its own action-space (what the internet can do to itself and to its constituent observers).

The attention-role taxonomy operates here: gatekeepers (platforms that arbitrate visibility), harvesters (engagement-mining systems), directors (recommendation algorithms), firewalls (filtering layers), parasites (engagement maximizers extracting value from hosts), symbionts (mutualistic tool ecosystems), weapons (information operations), sanctuaries (low-attention preserves). These are not metaphors but proposed measurable distributions; their relative proportions characterize the phase of the internet at time t.

Two properties make the internet uniquely useful as a test surface for the framework. It is *large* — variance across millions of observer-instances allows statistical claims. It is *instrumented* — every interaction leaves a substrate trace. The framework's wager is that this is where multi-agent systems will actually deploy and that a useful framework for intelligence at deployment scale must be a framework for the internet as observer.

## 7. Worked Example: SDPO+ on SOTOPIA

I propose a falsifiable operational experiment. SDPO (Segment-level Direct Preference Optimization) and its variants train social agents on the SOTOPIA benchmark using preference signals over agent behavior. The signals are typically scalar or low-dimensional vectors.

The Agnostic prediction: scalar preference signals are throwing away structure that is recoverable and useful. Specifically, every preference event has a wavelet-shaped structure — magnitude (how strong), spin (direction in some social-affect space), scale (how long the relevant context is), freshness (how recent the relevant comparison). A preference matrix indexed by (preference dimension, agent action) — the agnostic unit AU = P × A — should outperform scalar preferences on SOTOPIA tasks.

The falsifiable side-claim: SDPO+ with wavelet-shaped preferences (call them four-vector preferences with the components above) should outperform vanilla SDPO on standard SOTOPIA evaluation, by a margin exceeding what equivalent parameter or compute increases produce in vanilla SDPO. If it does not, this particular operationalization of the AU primitive is wrong, and the framework's protective belt must absorb the result or revise. The hard core (observer ontology, recursive primitives) is not threatened by this particular experiment failing; but the framework's empirical credibility is.

A second proposed experiment, briefly: feed a protein language model (ESM-2, trained on amino acid sequences) raw network packet captures and measure the cross-substrate transfer-learning gap against a vanilla LLM, a network-trained model, and a random baseline. The Agnostic prediction is that the differential reveals the *emergent-encryption thickness* of the network substrate — how much structure can be extracted before symbol-decoding, which the framework reads as a measurable property of any substrate's wrapper.

## 8. Relation to Existing Work

I will be explicit about what Agnostic recombines and what it claims as its own contribution.

- **Friston, active inference and the free energy principle.** Agnostic's inner loop is structurally compatible with active inference; the ask/give/ping/pong primitive can be read as a typed version of the variational message-passing that active inference describes. The framework's outer-loop story — symbiosis-as-pushout, canon-as-observer, attention-role taxonomy — extends beyond the single-agent inference setting active inference is usually formulated for. The relation is extension, not contradiction.

- **Walker & Cronin, assembly theory.** Assembly theory provides a selection-signature measure for physical systems; Agnostic reads its assembly index as a special case of carrier-artifact-becoming-canon at biochemical scale. The framework borrows the empirical discipline and tries to lift it to non-biochemical substrates.

- **Kauffman, adjacent possible.** Substrate expansion at each compile cycle is essentially Kauffman's adjacent possible, retyped. The credit is direct.

- **Chaisson, cosmic complexity.** Energy rate density as a complexity arrow is borrowed wholesale; Agnostic adds the observer-class typing on top.

- **Spencer-Brown, Laws of Form.** The distinction-as-primitive operation underlies the harness/wrapper split. Spencer-Brown's recursive generation of structure from a single primitive is the formal ancestor of the recursive observer typing.

- **Goguen, institutions and sheaves of theories.** This is the closest formal precedent for canon-as-colimit. Goguen's work on local sections and gluing conditions is what a future formalization of the framework's canon operations should look like.

- **Clark & Chalmers, extended mind.** Cognition not bounded by skull; the harness/wrapper distinction generalizes this.

- **Hofstadter, strange loops.** The canon-as-observer recursion is a strange loop in Hofstadter's sense; the framework's contribution is to make it typed and operationally measurable rather than illustrative.

- **Lakatos, research programmes.** The hard core / protective belt distinction is the framework's explicit epistemological commitment.

- **Park et al, Wang et al, current LLM-agent literature.** Operational precedents; the framework's added vocabulary is intended to be deployable on top of these systems, not to replace them.

What Agnostic claims as its own is the *synthesis*: the typing discipline that makes the same primitives operate across scales, the cone-profile-and-topology characterization of observer-classes, the pushout condition for symbiosis, and the canon-as-observer recursion as a structural account of paradigm change.

## 9. Where Agnostic Is Most Likely Wrong

I want to be explicit about the failure modes a sophisticated reader will worry about.

First and most seriously: is Agnostic a theory of intelligence that happens to fit LLMs, or a theory of LLMs generalized into a theory of intelligence? The honest answer is that the framework was developed in dialogue with LLMs and that several of its primitives — the canon graph, the protective belt, the wavelet-shaped preferences — have suspiciously natural LLM realizations. The defense is that the primitives also have natural realizations in cell biology (membrane, kernel, anomaly absorption), in organizational dynamics (meeting cadence as wrapper, document format as carrier artifact), and in scientific paradigms. But the worry is legitimate; the framework's cross-scale claims must be tested against domains where LLM-shaped thinking is unhelpful, and if they fail there, that failure must be admitted.

Second: the Γ ≈ 1 viability-band claim is at risk of being unfalsifiable in practice. If every observed viable system can be retro-fitted to Γ ≈ 1 by adjusting what counts as A⁺ and A⁻, the claim is empty. The discipline that rescues this is a *pre-registered* operationalization of A⁺ and A⁻ for each domain before the measurement is taken, with public commitment to what would count as evidence against.

Third: the speculative-cosmology overextension. Earlier rounds of the framework's development proposed a 0-dimensional emergence move at cosmological scale. I am deliberately not leading with this for an AI-research audience because it is the framework's most likely embarrassment risk. It should be quarantined as speculation or formalized rigorously; it should not be advertised at all until one of those has happened.

Fourth: the canon-as-observer recursion is currently illustrative more than operational. A clean operationalization of "kernel" distinct from "high-centrality node" is owed.

Fifth: the attention-role taxonomy is currently a useful descriptive vocabulary but lacks an inferred-from-data construction. We should be able to read role assignments off instrumented behavior rather than assigning them by inspection.

These are the directions in which the framework can fail. The Lakatosian commitment is that operational side-claims — SDPO+, the protein-model-on-packets experiment, real-time Γ measurement on instrumented platforms — can fail individually without the hard core collapsing, but accumulated failure of operational side-claims constitutes the kind of degeneration that should retire the programme.

## 10. Call to Action

Three concrete asks for working researchers.

**Run the experiments.** SDPO+ on SOTOPIA is a small project. The protein-language-model-on-packets experiment is mostly compute. Both are well-typed predictions with clear pass/fail criteria. If they pass, the framework earns operational credibility; if they fail, the framework loses it on those specific points and must revise. This is what Lakatosian discipline looks like in practice.

**Build the framework-reading engine.** An instrumented observer of the internet — a system that measures Γ in real time on public data streams, infers attention-role distributions from observable behavior, detects squeeze events as anomaly-density spikes — would convert the framework from vocabulary into a measurement instrument. This is plausibly the highest-leverage engineering project the framework suggests.

**Formalize the canon-as-colimit construction.** Goguen's institution theory is the right starting point. A clean formalization of canon operations (A⁺, A⁻, stabilize) as colimit and limit operations in an appropriate category, with the pushout condition for symbiosis stated rigorously, would make the framework auditable in a way it currently is not.

The framework offers a unified vocabulary for reasoning about observers at very different scales, a typing discipline that constrains what can be said about each, and a set of operational predictions that can fail. That is the bet. It does not claim to be true; it claims to be productive. The discipline that distinguishes a productive research programme from a degenerating one is exactly the discipline of running the experiments, formalizing the constructions, and admitting the failures. The invitation is to participate in that discipline.

---

## Critic-writer revision notes

The first draft over-claimed in several characteristic ways and the revision tightened each.

**Overreach on cross-scale identity.** The first draft asserted, in several places, that biological symbiogenesis, paradigm shifts, and platform reorganizations *are* "the same primitive." The revision retains this language but pairs each occurrence with an explicit hedge — that the claim is a *typing proposal*, not a derivation, and that its discipline lies in producing measurable predictions that bind across domains. A sophisticated reader will reject identity claims without that discipline attached; pairing the claim with the discipline is the honest move.

**Insufficient engagement with Friston.** The first draft mentioned active inference once and moved on. Because the audience reads Friston seriously, the revision states explicitly how Agnostic's inner loop relates to variational message-passing and where the framework extends past single-agent inference. This is the prior art the audience will check first; underweighting it is fatal.

**The Γ ≈ 1 claim was too cheap.** The first draft asserted criticality without acknowledging that, without pre-registered operationalization, the claim risks being unfalsifiable. The revision adds an explicit pre-registration requirement and treats this as a known failure mode rather than a strength.

**The 0D-emergence cosmology move.** The framework's most embarrassing speculative content was floated briefly in the first draft. The revision implements quarantine, mentioning the issue only as a known overreach risk. Leading with speculative cosmology to an AI-research audience would burn credibility.

**Canon-as-observer was treated as more operational than it is.** The first draft implied that kernel-restructuring events were measurable. The revision admits explicitly that the operationalization is incomplete and owes work.

**Attention-role taxonomy needed an honest status statement.** The first draft presented it as a finished construct. The revision admits it currently lacks an inferred-from-data construction and flags this as a development task.

**The "theory of LLMs generalized?" worry.** The single most important critic question for this audience. The first draft underplayed it; the revision states the worry, gives the honest defense, and admits the worry's residual force. This is the credibility move that buys the rest of the manifesto its hearing.

**Operational specificity.** The revision tightened the SDPO+ proposal into a pass/fail experiment with explicit margin requirements and explicit consequences for the hard core versus the protective belt. The first draft was vaguer about what success would look like.

Net effect: the manifesto reads less as a sales document and more as a research-programme proposal an AI researcher could plausibly engage with, including by attacking it.
