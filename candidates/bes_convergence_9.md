# Cross-substrate convergence #9 candidate — Bidirectional Evolutionary Search (BES) at the search-methodology substrate

**Tier:** Tier 2 candidate per [cont 27 §2](../continuations/27.md). Conditional on (a) Reading 07 careful writeup confirming the mapping holds at all sections, (b) BES PDF §4.1 entropy-shell proof + §4.2 backward-search proof + §6 Related Work prose verified (residual HTML-truncation gap), (c) at least one BES author recognizing the convergence framing if outreach lands.
**Surfaced:** 2026-05-31 by Pav from external radar after framework's agent-substrate optimization round
**Verified by:** opus subagent careful read of the BES paper (claim-validity audit, 9-section structured report)
**Source paper:** Xu, Qi, Su, Ye, Lakkaraju, Kakade, Du. *"Self-Improving Language Models with Bidirectional Evolutionary Search."* arxiv 2605.28814 (2026). Embodied Minds Lab / Harvard.

---

## §1 The convergence claim

BES is structurally the eighth (or ninth, see §9) instance of the three-force decomposition the framework has been tracking, instantiated at the search-methodology substrate. Adds to the cont 25 §6 + Reading 03 + Reading 06 list:

1. LCAO molecular orbital theory (bonding / antibonding / non-bonding)
2. Cell fusion (membrane mixing / surface tension / cytoplasmic phase separation)
3. Symbiogenesis (endosymbiont uptake / immune rejection / co-evolutionary stabilization)
4. Creole genesis (lexical absorption / grammatical resistance / community-norm stabilization)
5. Conceptual blending (input-space projection / vital-relation contrast / blended-space stabilization)
6. Model merging (parameter averaging / interference resolution / task-vector stabilization)
7. ACMP — Allen-Cahn Message Passing (Dirichlet attraction / pairwise repulsion / Allen-Cahn phase separation)
8. **Cymatics** (Reading 06) — Tier 2 candidate, narrowed to substrate-adjacent per audit v05 §2.1 amendment
9. **BES — Bidirectional Evolutionary Search at search-methodology substrate** (this candidate)

The three forces in BES:
- **Attraction (forward search):** policy-emitted candidate trajectories combined / recombined via evolution operators
- **Repulsion (backward decomposition):** recursive goal-tree decomposition with leaf-verifier checks pruning sub-goals that don't pass
- **Phase-locked stabilization (complementarity selection):** Boltzmann-weighted pair scoring (Eq. 6) selecting parents whose backward-score profiles cover complementary parts of the goal tree, locking in W_C only when both parents contribute non-redundantly

---

## §2 Why this is the load-bearing parents-produce-W_C instantiation

The framework's structural test (per cont 25 §6 + audit v05 §3):
1. Two parent wrappers W_A and W_B pre-exist as distinct entities ✓
2. They interact and produce a third persistent W_C that is itself a wrapper of the same kind ✓
3. The third force is a bistability-creating mechanism that produces a NEW persistent entity ✓ (Boltzmann sampler over backward-score complementarity)
4. The W_C is categorically of the same kind as the parents ✓ (W_C is itself a trajectory; can become parent for next operator)
5. Parents persist as procedural-root stubs after W_C consolidates ✓ (Eq. 3 actively rewards re-selecting under-used parents)

**All five conditions pass cleanly.** BES is the cleanest instantiation of parents-produce-W_C in the convergence list because the parents-produce-W_C move is the *explicit algorithmic novelty being introduced*, not a structural pattern retrofitted to substrate physics after the fact.

The paper's own intro analogy makes this explicit: *"Sexual reproduction fundamentally changed this through chromosomal recombination: gene segments from different lineages are spliced together to produce novel combinations that neither parent possessed."* This is one paragraph away from framework wrapper-overlap vocabulary.

**Direct quote (§3.2):** *"a sub-goal is considered covered if either parent addresses it, so the pair score favors complementary parents that cover different parts of the goal tree."* — the pushout structural condition stated explicitly.

---

## §3 Independence evidence (critical for the convergence claim)

Full reference dump from the paper (verified by subagent):

**Cited:** Fisher 1930, Muller 1932, Holland 1992, Storn-Price 1997, Sipper 1998 (classical evolutionary biology + genetic algorithms canon). Plus modern LLM search literature (MCTS, ToT, GoT, ShinkaEvolve, AlphaEvolve, AlphaCode, DeepSeek-R1, MuSiQue).

**NOT cited (the convergence-independence evidence):**
- LCAO, molecular orbital theory, quantum chemistry: **NONE**
- Cell fusion biology (Margulis, Sapp): **NONE**
- Symbiogenesis: **NONE** (Fisher/Muller are evolutionary genetics, not symbiogenesis)
- Creole genesis (Mufwene, Bickerton, Lefebvre): **NONE**
- Conceptual blending (Fauconnier-Turner, Coulson, Goguen): **NONE**
- Model merging (TIES, DARE, mergekit, Arcee, Yadav et al.): **NONE**
- GNN three-force / oversmoothing / ACMP / GRAFF: **NONE**
- Cymatics, harmonic structure, eigenmode decomposition: **NONE**
- Reservoir computing, Koopman operators: **NONE**

**This is the cleanest convergence-by-independence signal in the framework's list.** Independent research community lands on parents-produce-W_C via a totally separate lineage (1930s evolutionary biology → 1990s genetic algorithms → 2026 LLM search). That's the convergence signal the framework's cross-substrate claim is designed to detect.

**Residual gap (queued for verification):** subagent could not read §4.1 / §4.2 / §6 Related Work prose (HTML mirror truncated at ~85k tokens). Small (<5%) residual risk that §6 mentions LCAO / cell-fusion / etc. as passing analogy without citation. PDF read queued before outreach DM.

---

## §4 Refinements to framework framing this candidate triggers

**§4.1 Don't lump all 4 BES operators together as "wrapper-overlap operators."** Per subagent's tightness ratings:

| BES operator | Framework primitive | Tightness |
|---|---|---|
| Combination | parents-produce-W_C | 5/5 |
| Crossover | creole-genesis at trajectory level | 4/5 |
| Translocation | procedural lineage transfer (cont 18) | 4/5 |
| Deletion | A⁻ pruning (NOT canon dormancy) | 3/5 (remap) |
| Expansion | baseline A⁺ generation | not a wrapper-overlap op |

Only the three two-parent operators instantiate parents-produce-W_C. Deletion remaps to A⁻. Expansion is baseline A⁺. This refinement strengthens the framework — BES becomes a worked example of three distinct framework primitives applied to one substrate.

**§4.2 Backward goal-tree ≠ cont 27 §2 tier-tagging.** Similar shape, different semantics. BES decomposes by task-granularity; cont 27 decomposes by epistemic-certainty. Should be candidate-strength, not canon-strength.

**§4.3 Dense-vs-sparse-feedback IS tight (5/5).** BES gives the framework formal mathematical grounding (Theorem 4.4) for the A⁻-primacy claim cont 13 makes.

---

## §5 Theoretical contribution the framework gets to cite

**BES Theorem 4.4 (entropy-shell escape).** Formal result that auto-regressive sampling from a policy is confined to a "narrow entropy shell" and recombination operators provably escape it. This is the framework's first cite-able formal grounding for the parents-produce-W_C claim being non-trivial — not just that wrapper-overlap produces a third entity, but that the third entity is provably *unreachable from either parent alone via single-rollout expansion.*

Reading 07 should cite this theorem as the math the framework has been intuiting and lacked formal backing for.

---

## §6 Methodological contribution for queued pilots

**§6.1 For task #151 (RC-Koopman pilot on cultural eigenmodes) — backward goal-tree decomposition translates directly:**

1. Decompose "is this cultural eigenmode real?" into sub-goals: (a) persists across time windows, (b) coherent across multiple embeddings of same corpus, (c) corresponds to known sociopolitical event cluster, (d) Koopman spectrum shows stable eigenvalue at claimed mode
2. Each sub-goal becomes a checkable V_g; overall score = recursive average per BES Eq. 5
3. Forward operators recombine pipeline candidates (combination, translocation)
4. Pair-score complementarity gates which forward candidates grow

**Honest limit:** at social-substrate scale, V_g is judgment-laden in a way Knights-and-Knaves V_g isn't. Anchor at least one leaf check to external data (NEXIS, GDELT, sentiment-stable time series).

**§6.2 For task #150 (1/f-as-failsafe operationalization):** less applicable. The 1/f task is measurement-design, not search. BES backward decomposition is useful for scoping sub-goals; forward operators add nothing.

---

## §7 Outreach affinity

**Yilun Du** (Harvard, Embodied Minds Lab) — direct EBM/LeCun lineage. From his homepage: *"some of my early work on EBMs led to the development of diffusion models in 2020"* + *"constructing composable generative models … learning energy landscapes (EBMs)."* Core research program: composable generative models. The framework's wrapper-overlap diagram literally animates what compositional-generation does in latent space.

**Sham Kakade** (Harvard, theoretical ML, co-author on Energy-Based Transformers ICLR 2026 Oral) — theoretical depth + EBM connection.

**Himabindu Lakkaraju** (Harvard, interpretable ML) — interpretability angle matches "make A⁻ visible" principle.

**Connection to existing framework shoulders:**
- **Strong** to LeCun lineage via Du's EBM work
- **Strong** to Tenenbaum (Du's MIT advisor; conceptually adjacent to wrapper/compile-loop — should be added to Shoulders)
- **Moderate** to Kaelbling (Du's MIT advisor; planning under uncertainty, sub-goal decomposition relevant)

**Recommended outreach framing:** lead with convergence-by-independence observation. *"You arrived at parents-produce-W_C via Fisher-Muller-Holland; we arrived at it via LCAO + cell fusion + creole genesis + model merging + ACMP. Independence is the headline. Theorem 4.4 is the formal math we've been intuiting and lacked grounding for — happy to be wrong about the convergence."*

**Outreach contingent on:** §4.1 / §4.2 / §6 PDF re-read confirming independence claim, and Reading 07 written sharp enough that Du can engage substantively rather than glance.

---

## §8 Promotion bars

Per cont 27 §3, Tier 2 candidates name explicit bars that would advance to Tier 1:

**(A) Reading 07 careful writeup confirms mapping holds at all sections, ships, and survives audit v06 (or equivalent).** Framework-internal verification.

**(B) PDF re-read of §4.1 entropy-shell proof + §4.2 backward-search proof + §6 Related Work prose confirms no citation of the framework's existing convergence-list traditions.** Residual independence-claim gap closed.

**(C) At least one BES author recognizes the convergence framing.** External validation. If Yilun Du or co-authors respond substantively to the outreach DM acknowledging the structural pattern (even to dispute or refine it), promotion bar C is met. Total non-response is null evidence (could mean disagreement, could mean inbox volume).

**Any one bar met advances to Tier 2 (which is already the candidate's current tier — confusing because of the Reading 06 amendment naming framework). Combined evidence on multiple bars advances toward Tier 1 epistemological canon.**

---

## §9 Why this might be #8 or #9

The convergence list currently has seven canon (LCAO, cell fusion, symbiogenesis, creole genesis, conceptual blending, model merging, ACMP) and one Tier 2 candidate (cymatics, narrowed to substrate-adjacent per audit v05 §2.1 amendment).

If cymatics holds at Tier 2 candidate status → BES is #9.
If cymatics is downgraded further (or held as different-species due to substrate-adjacency vs structural-isomorphism distinction) → BES is #8 and cymatics is reframed as adjacent/illustrative.

Reading 07 should clarify this. The framework's discipline prefers explicit-list-ordering with tier-tags over silent renumbering.

---

## §10 Cross-references

- [continuations/29.md](../continuations/29.md) — surfacing capture with provenance
- [continuations/25.md](../continuations/25.md) §6 — original seven-convergence list (will receive #9 BES candidate addition)
- [readings/2026-05-27_acmp_attraction_repulsion_gnn.md](../readings/2026-05-27_acmp_attraction_repulsion_gnn.md) — Reading 03, convergence #7 ACMP (precedent for mathematically-rigorous convergence claim)
- [readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md](../readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md) §2.1 — Reading 06 amendment with OE1 (closed by convergence multiplication per cont 29 §1)
- [audits/v05.md](../audits/v05.md) §3 — audit v05 OE1 (closed by convergence multiplication per cont 29 §1)
- [continuations/27.md](../continuations/27.md) §2-3 — three-tier procedure + promotion bars + pruning rules under which this candidate operates
- [continuations/28.md](../continuations/28.md) §5 — agent-substrate as observer-class; cont 29 §4 logs first inbound-discovery worked example
- [continuations/13.md](../continuations/13.md) — A⁻ promoted to primary discipline; BES gives this formal mathematical grounding (Theorem 4.4)
- [continuations/18.md](../continuations/18.md) — procedural lineage; translocation operator maps to this
- [candidates/cultural_eigenmode_analysis.md](cultural_eigenmode_analysis.md) — Tier 3 speculative candidate; BES backward-decomposition methodology gifts it a procedure for promotion bar A
- [candidates/energy_floor_failsafe.md](energy_floor_failsafe.md) — promoted to canon per cont 27; structural precedent for candidate-promotion workflow

---

## §11 Risks the framework should NOT overclaim

1. **Don't claim convergence on the evolutionary operators themselves.** They're 60-year-old GA primitives. The convergence is on the architectural decision to make them load-bearing for LLM search with dense intermediate verification.

2. **Don't lump deletion/expansion with two-parent operators.** Only combination/translocation/crossover instantiate parents-produce-W_C.

3. **Don't claim BES tier-tagging = cont 27 tier-tagging.** Similar shape, different semantics. Loose analogy.

4. **Don't claim empirical validation at social substrate.** BES is tested on logical reasoning, multi-hop QA, geometric packing — none of which are social substrate. The convergence is architectural; social-substrate extensions are speculative.

5. **Don't promote to Tier 1 until promotion bars A and B are met.** Reading 07 + PDF gap-fill.

6. **Don't pre-frame outreach with overconfidence.** "Happy to be wrong" close per Pav's voice. Du is a senior researcher; the framework's posture should be invitational, not declarative.
