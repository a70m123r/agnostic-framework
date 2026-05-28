# Energy-floor failsafe — worked-example library (now canon, preserved as reference)

**Status:** **PROMOTED TO CANON 2026-05-27 per [cont 27 §1](../continuations/27.md).** This doc is preserved as the worked-example library that supported the promotion. The canonical statement is now in PRIMITIVES on the live site index.
**Originally surfaced:** 2026-05-27 in [Reading 03](../readings/2026-05-27_acmp_attraction_repulsion_gnn.md) §5, in light of [cont 26](../continuations/26.md) §3 internal-pressure failsafes
**Promotion criteria (now met):** ≥3 substrate worked examples beyond ACMP/GNN where (a) a candidate coherence quantity can be named, (b) a theoretical or empirical lower-bound argument is available, (c) the bound corresponds to a known failure mode when violated. The four substrate worked examples below are the documented basis for the promotion.

---

## The general claim

Every wrapper-overlap dynamic that produces stable distinction — where W_A and W_B persist as procedural-root stubs even after W_C emerges — does so because the system's *internal coherence quantity* E has a mathematically or empirically demonstrable positive lower bound under the dynamic. The bound is what prevents the wrappers from collapsing into uniformity (oversmoothing in the GNN substrate; over-union in the framework's general substrate).

The bound is the **failsafe**. When the bound is violated, the wrapper has crossed a structural threshold and either undergoes phase transition (cont 20 dormancy), supersession (cont 25 §1 supersede branch), or break (cont 25 §1 break branch).

The framework's claim about L0's evolved failsafes (cont 26 §3) becomes mathematically concrete: the failsafes are coherence-quantity lower bounds, evolved (in a substrate-specific selection environment) to prevent wrapper-rendering pathologies.

This doc collects worked examples across four substrates to test whether the schema is portable.

---

## Worked example 1 — ACMP / Graph Neural Networks (Reading 03)

**Coherence quantity:** Dirichlet energy E(x) = ½ Σ_(i,j)∈edges ‖x_i − x_j‖² of the node-feature vectors x.

**Lower-bound argument:** Wang et al. 2022 prove (Theorem 4.2, ACMP paper) that under their three-force dynamic (attractive + repulsive + Allen-Cahn), there exists a strictly positive lower bound E_min > 0 such that E(x(t)) ≥ E_min for all t. The bound arises from the Allen-Cahn term's phase-separation property and cannot be driven to zero by gradient flow on the combined energy.

**Failure mode when violated:** Oversmoothing — all node representations converge to the same vector (or to the dominant eigenvector of the graph Laplacian). The graph's structural information is lost; the GNN becomes incapable of distinguishing any nodes from any other. In framework terms: over-union; W_A and W_B merge completely; no procedural-root stubs persist.

**Empirical validation:** ACMP achieves SOTA on multiple node-classification benchmarks at depths (100+ layers) where vanilla GNNs collapse. The persistence of distinguishing performance at depth IS the empirical demonstration that the energy floor is being maintained.

**Substrate type:** mathematical / computational. The cleanest worked example because the substrate IS math.

---

## Worked example 2 — Cell metabolism / ATP density

**Coherence quantity:** Intracellular ATP density (energy charge), typically reported as the adenylate energy charge = (ATP + ½ADP) / (ATP + ADP + AMP). Normal cells maintain energy charge in the range 0.8–0.95.

**Lower-bound argument:** Cells maintain ATP density through homeostatic feedback loops (glycolysis, oxidative phosphorylation, substrate-level phosphorylation) that respond to drops in ATP density by upregulating energy production. The lower bound is not a single fixed threshold but a hysteresis-protected range with multiple feedback mechanisms enforcing it. Below energy charge ≈ 0.5, most ATP-dependent processes (active transport, protein synthesis, ion-pump maintenance) fail simultaneously. Below energy charge ≈ 0.3, the cell triggers apoptosis (Atkinson 1968 model; Schramm & Iyengar 2007 review).

**Failure mode when violated:** Apoptosis — programmed cell death. Notably the cell does not just "die" passively when ATP is exhausted; it actively executes a controlled-disassembly program (the "failsafe" in the cont 26 sense) before energy reserves run out completely. The apoptotic program preserves information (genomic content recycled, structural components reabsorbed) rather than scattering it. In framework terms: cont 20 canon dormancy with imparted learning, at the cellular scale.

**Empirical validation:** Decades of cell-biology research on apoptosis triggers (cytochrome c release, caspase cascade, mitochondrial outer-membrane permeabilization) all point to ATP availability as a primary upstream signal. Cells in vitro deprived of glucose and oxygen for extended periods consistently trigger apoptosis at energy-charge thresholds that vary by cell type but cluster in the 0.3–0.5 range.

**Substrate type:** biological. The lower bound is enforced by evolved homeostatic mechanisms (the cell's compiled failsafe network), not by mathematical theorem. The fit to the energy-floor schema is high: there is a clear coherence quantity, a clear bound, a clear failure mode when violated, and the failure mode is itself an evolved program rather than uncontrolled collapse.

---

## Worked example 3 — Creole genesis / mutual intelligibility

**Coherence quantity:** Mutual intelligibility within the speech community. Operationalized as the percentage of utterances by community member A that community member B comprehends correctly without prior explicit instruction. Standard methodology in sociolinguistics (e.g., Casad 1974 intelligibility-testing protocol).

**Lower-bound argument:** A speech community maintains a roughly 80%+ mutual-intelligibility floor through continuous use, child language acquisition (children resolve adult variation by acquiring a converging grammar), and explicit pedagogy. Below ~70% mutual intelligibility, communication failures become frequent enough that pragmatic strategies shift — speakers code-switch, simplify, or fragment into sub-communities. Below ~50%, the community fragments into mutually unintelligible dialects within one or two generations (Trudgill 1986, Mufwene 2001).

**Failure mode when violated:** Dialect fragmentation. The original wrapper (the unified creole or pidgin) does not "die" — it bifurcates into descendant wrappers each with its own internal coherence floor. The procedural-root stubs (lexical and grammatical features inherited from the parent) persist in each descendant. In framework terms: cont 25 §1 break-apart branch, but at language-wrapper scale, with cont 18 procedural lineage preserved.

**Empirical validation:** Documented cases include the divergence of Tok Pisin creole varieties in Papua New Guinea (Romaine 1989), the fragmentation of Hawaiian Pidgin into multiple sub-creoles before standardization (Sakoda & Siegel 2003), and the historical splits of Romance languages from Vulgar Latin (each Romance language retains procedural-root stubs from Latin while no longer being mutually intelligible with the others).

**Substrate type:** social / linguistic. The lower bound is not enforced by a mathematical theorem nor by genetic/biochemical homeostasis but by communicative pragmatics + child-acquisition dynamics. The fit to the energy-floor schema is moderate-to-high: the coherence quantity is well-defined and measurable; the bound is empirically observable; the failure mode is structurally predictable. Less clean than ACMP or cell metabolism because the bound has no closed-form expression and varies by community size, contact intensity, and external pressure.

---

## Worked example 4 — Institutions / coordination capacity

**Coherence quantity:** Coordination capacity = the number of decisions per unit time the institution can make coherently (without contradicting prior decisions, without losing track of commitments, without producing internally inconsistent outputs). Hard to measure directly; proxies include meeting throughput, decision-cycle time, internal-contradiction rate, employee survey questions about "things falling through the cracks."

**Lower-bound argument:** Below a coordination-capacity floor, the institution cannot maintain its commitments. Decisions get made but are inconsistent across the institution; promises are forgotten; the same problem gets re-solved in different units of the institution; the wrapper begins to fragment into independent sub-wrappers that operate as if the parent didn't exist. The Dunbar number (~150 stable relationships) is one widely-discussed proxy for one mechanism (cognitive limit on personal coordination); managerial-span-of-control research (typical 5–10 direct reports) is another. Across all of these, the empirical pattern is that institutions which grow beyond their coordination-capacity ceiling either (a) install new coordination mechanisms (the failsafe being engineered explicitly), (b) fragment (the failsafe being violated), or (c) collapse the wrapper into a smaller scope where coordination is sustainable (a controlled retreat to a higher floor).

**Failure mode when violated:** Institutional fragmentation. Classical examples: Roman Empire splitting into Eastern and Western halves under Diocletian, then further fragmenting in the West; corporate spinoffs (often performance-positive because each spinoff has higher coordination capacity for its narrower scope); the routinized "decentralization initiatives" of large companies (which usually amount to formalizing the fragmentation that has already happened). The framework reads each of these as cont 25 §1 break or supersede branch at the institutional scale.

**Empirical validation:** Span-of-control literature (Graicunas 1937 onward), Dunbar number research (Dunbar 1992, Hill & Dunbar 2003), corporate-spinoff performance studies (Krishnaswami & Subramaniam 1999, Cusatis et al. 1993), organizational-collapse case studies (Diamond 2005 Collapse focuses on this at civilizational scale).

**Substrate type:** institutional / organizational. The bound is enforced by cognitive/coordination limits + selection pressure (institutions that exceed without engineering new mechanisms get outcompeted). Fit to the energy-floor schema is moderate: the coherence quantity is real but harder to measure; the bound is real but soft and context-dependent; the failure mode is well-attested.

---

## Substrate coverage so far

| Substrate | Coherence quantity | Bound nature | Failure mode | Fit |
|---|---|---|---|---|
| 1. ACMP / GNN | Dirichlet energy | Mathematical theorem | Oversmoothing | Excellent |
| 2. Cell metabolism | ATP / energy charge | Evolved homeostasis | Apoptosis (controlled) | Strong |
| 3. Creole genesis | Mutual intelligibility | Pragmatic + acquisition | Dialect fragmentation | Strong |
| 4. Institutions | Coordination capacity | Cognitive + selection | Institutional fragmentation | Moderate |

The four substrates span mathematical, biological, social-linguistic, and organizational. Together they meet the Reading 03 §5 promotion criteria of "≥3 worked examples beyond ACMP" — examples 2, 3, 4 are the three.

---

## Promotion proposal

Promote energy-floor failsafe from candidate to canon as **a structural primitive of L0 internal-pressure failsafes** (cont 26 §3 class).

**Canonical statement:** For any wrapper W that participates in an overlap dynamic with other wrappers and that exhibits stable distinction (parents persist as procedural-root stubs through and after the overlap), there exists a substrate-specific coherence quantity E_W with a positive lower bound E_min > 0, such that the wrapper-overlap dynamics preserve E_W(t) ≥ E_min. The lower bound is the wrapper's internal failsafe; its violation triggers a substrate-specific phase transition (dormancy, supersession, or break, per cont 25 §1).

**What this changes:**
- Adds the energy-floor language to the framework's wrapper primitive
- Makes cont 26 §3 internal-pressure failsafes mathematically concrete
- Provides a four-substrate worked-example library that future construct studies can pattern-match against
- Sharpens the contrast with external-pressure failsafes (cont 26 §3, second class) — internal ones bound a coherence quantity; external ones impose a constraint from the surrounding wrapper field. Both can fail simultaneously in cont 25 §1 break branch.

**What this does NOT claim:**
- That every wrapper has a single, clean, closed-form coherence quantity (cell metabolism and institutions have softer bounds than ACMP)
- That the bound is fixed (it can be raised or lowered by evolved or engineered changes to the wrapper's internal architecture)
- That the bound is the only failsafe (external pressures from neighbouring wrappers are independent)

**Open questions deferred:**
- Cross-substrate scaling: does E_min scale predictably with wrapper size or complexity? Possibly testable on construct studies (marriage, religion, language, nation-state, internet).
- Multi-quantity wrappers: can a wrapper have multiple coherence quantities each with its own floor? Probably yes; cells have ATP + pH + redox state + osmotic balance, each with floors.
- The relationship to cont 22 four-layer stack: is the floor at kernel canon (cont 22 layer 1) or function (cont 22 layer 2)? Likely at kernel canon for clean biological/computational substrates, and at function for social substrates where the kernel is more diffuse.

---

## Cross-references

- [Reading 03](../readings/2026-05-27_acmp_attraction_repulsion_gnn.md) §5 — original surfacing of the candidate
- [continuations/26.md](../continuations/26.md) §3 — internal-pressure failsafe class
- [continuations/26.md](../continuations/26.md) §5 — "where this changes the framework"
- [continuations/20.md](../continuations/20.md) — canon dormancy (the failure-mode primitive this fails into)
- [continuations/25.md](../continuations/25.md) §1 — lifecycle break/supersede branches (alternative failure modes)
- [continuations/18.md](../continuations/18.md) — procedural lineage (what persists through the failure)
- [artifacts/wrapper_overlap_animated.html](../artifacts/wrapper_overlap_animated.html) v16 — visual demonstration including ACMP-force overlay
