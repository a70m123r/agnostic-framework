Here is the first-principles derivation of candidate latent measurement units, addressing the load-bearing hole in the COIN implementation.

### 1. THE SIX FAMILIES AS CONCRETE UNITS

**1. COMPRESSION / EXPANSION (The "MDL" Unit)**
*   **Prior Art:** Minimum Description Length (Rissanen), LLM-as-compressor (negative log-likelihood).
*   **Definition:** The cross-entropy / codelength of the wrapper under a pinned, universally disclosed reference model M (e.g., a quantized open-weights LLM).
*   **Estimator:** `L(w) = -log2 P_M(w | context)`. Pass the canonical text/graph representation of the wrapper through M.
*   **Uncertainty Interval:** The entropy of the predictive token distribution `H(P_M)`.
*   **Dependency Model:** Sequential chain rule. Strongly dependent on M's training prior.
*   **One-Sided Upper Bound:** YES. Any valid executable coding scheme guarantees the empirical codelength is a strict upper bound on true algorithmic complexity.
*   **Composes:** Additive. Direct 1:1 translation to physical EntropyGS bits.

**2. PERCENT OF THE FRAME's CONTENT (The "Relative Entropy" Unit)**
*   **Prior Art:** Pointwise Mutual Information (PMI), Kullback-Leibler (KL) Divergence.
*   **Definition:** The fraction of the current frame's total descriptive complexity that is uniquely explained by the wrapper.
*   **Estimator:** `[ L(Frame) - L(Frame \ w) ] / L(Frame)`.
*   **Uncertainty Interval:** Propagation of variance from the two independent `L()` estimates.
*   **Dependency Model:** Extreme context-dependency. Overlapping wrappers in the same frame will double-count bits unless orthogonalized.
*   **One-Sided Upper Bound:** NO. Subtractive estimators can underestimate true content if the frame contains systemic redundancies.
*   **Composes:** Dimensionless multiplier [0,1]. Requires scaling by the physical bits of the frame to compose.

**3. THE KERNEL CANON (The "Bottleneck" Unit)**
*   **Prior Art:** Minimal Sufficient Statistics, Information Bottleneck (Tishby), Sparse Autoencoders.
*   **Definition:** The minimal bits required to predict the wrapper's external relations/effects without loss, discarding internal syntactic structure.
*   **Estimator:** The active latent dimension capacity in a pinned sparse autoencoder. Lagrangian: `min I(X;T) - B * I(T;Y)`.
*   **Uncertainty Interval:** The gradient of the rate-distortion curve at the chosen bottleneck parameter `B`.
*   **Dependency Model:** Dependent strictly on the target `Y` (what external features the wrapper is obligated to predict).
*   **One-Sided Upper Bound:** YES. Any empirically feasible bottleneck is an upper bound on the theoretical absolute minimum sufficient statistic.
*   **Composes:** Directly additive as bits.

**4. CONNECTIVITY (The "Graph Information" Unit)**
*   **Prior Art:** Von Neumann Graph Entropy, PageRank centrality, k-core decomposition.
*   **Definition:** The structural information capacity of the wrapper's position within the latent network topology.
*   **Estimator:** Degree-weighted Shannon entropy of the local neighborhood, or `-log2` of its stationary distribution probability in a random walk.
*   **Uncertainty Interval:** Jackknife variance over random edge dropouts.
*   **Dependency Model:** Highly coupled. Removing or adding a node instantaneously alters the measurement of all neighbors.
*   **One-Sided Upper Bound:** NO. Centrality metrics are relative flow dynamics and do not strictly bound intrinsic informational content.
*   **Composes:** Poorly. Graph properties are not directly commensurate with Shannon bits without introducing an arbitrary scaling constant.

**5. THE ZOO UNIT (The "Rarity" Unit)**
*   **Prior Art:** Hill Numbers, Rao's Quadratic Entropy, Vector Space Density Estimation.
*   **Definition:** The "surprisal" of encountering this specific wrapper given the distribution of the global latent space.
*   **Estimator:** `Bits = -log2 P(w)`, where `P(w)` is computed via Kernel Density Estimation (KDE) or distance to the k-th nearest neighbor in a global embedding vector database.
*   **Uncertainty Interval:** Confidence intervals of the KDE bandwidth parameter.
*   **Dependency Model:** Globally dependent on the corpus.
*   **One-Sided Upper Bound:** NO. If `P(w)` is overestimated due to embedding collapse, the bits are underestimated.
*   **Composes:** Additive as bits, assuming independence from the physical coding scheme.

**6. DEADWEIGHT vs SUPPORTING STONE (The "Ablation" Unit)**
*   **Prior Art:** Leave-One-Out (LOO) cross-validation, Shapley Values, Influence Functions.
*   **Definition:** The system-wide increase in description length when the wrapper is deleted (the structural load it bears).
*   **Estimator:** `Delta L = L(System \ w) - L(System)`. 
*   **Uncertainty Interval:** Variance computed via Monte Carlo approximation over random sub-graph ablations.
*   **Dependency Model:** Contextually precise. Resolves redundant evidence gracefully (two identical wrappers have low individual LOO value, but high group value).
*   **One-Sided Upper Bound:** YES. Shapley-based ablations strictly partition the total system bits without exceeding them.
*   **Composes:** Additive bits.

---

### 2. THE ZOO QUESTION CONCRETIZED
If the latent space is a zoo, the unit is **Taxonomic Surprisal (Bits)**, derived from embedding-space density. You do not measure biomass (term frequency); you measure phylogenetic distance (Inverse Document Frequency applied to continuous latent space). 

**Mechanism:** Every wrapper is mapped to a vector embedding. The "measurement" of a specimen is its spatial isolation. A common "concept" (a pigeon) sits in a dense cluster; local `P(x)` is high, so `-log2 P(x)` (bits) is low. A highly unique, anomalous wrapper (a coelacanth) sits alone; `P(x)` is low, bits are high. 

---

### 3. DEADWEIGHT VS STONE
Exact Shapley values are `O(2^N)` and therefore computationally dead on arrival. Influence functions require Hessian inversion.

**Cheap Mechanism: Reconstructive LOO.**
Take the wrapper's immediate neighbors in the graph. Train a fast, sparse linear probe to reconstruct the target wrapper's embedding purely from its neighbors. 
*   **Deadweight:** If the wrapper can be perfectly reconstructed (residual error ~ 0), it is redundant. Its measured bits drop to 0. 
*   **Supporting Stone:** If the reconstruction fails (high residual variance), the wrapper contains orthogonal, non-derivable information. The residual error mathematically maps to its "Stone Mass" in bits.
*   **Rendering:** Deadweight renders as blurred/translucent (the COIN detects ~0 measured bits). Stones render as sharp, solid, opaque anchors.

---

### 4. INTRINSIC VS RELATIONAL
**The Disagreement:** The framing suggests a search for an "intrinsic" latent measure. This is a category error. **There is no purely intrinsic latent measure.** Latent meaning does not exist in a vacuum; it is constitutively relational. 

Even the closest intrinsic candidate (Compression/MDL) requires a "pinned model M" (a relational anchor). A concept only possesses "bits" relative to the prior of an observer/coder. Connectivity is relative to the graph; the Zoo is relative to the corpus; LOO is relative to the system. We must abandon the illusion of the "absolute intrinsic bit" and standardize on the **pinned relational bit**.

---

### 5. CLOSING THE HOLE & THE DIAL EXPERIMENT
**The Solution:** The combination that best closes the hole is **Pinned MDL bounded by Reconstructive LOO**.
*   MDL provides the rigorous, one-sided upper bound on the absolute maximum bits.
*   Reconstructive LOO acts as the discount rate, stripping away bits that are redundant to the local topology.

**The DIAL:** The **"Reconstruction Threshold"** (k-neighbors used in the probe). 
*   Turn the dial to 0: You get raw MDL. Everything that is complex renders sharp, even if repetitive.
*   Turn the dial to high-k: The system aggressively compresses redundancy, blurring out vast swaths of concepts that are logically implied by their neighbors, leaving only the irreducible structural skeleton.

**The ONE Experiment: "The Amnesia Drop"**
1. Take a densely populated latent graph (e.g., 1000 nodes of a technical specification).
2. Measure every node using MDL discounted by LOO.
3. Enforce the COIN strictly: blur nodes proportionally to their discounted bits (redundant nodes become heavily blurred).
4. Task an independent agent (or LLM) to reconstruct the original exact graph from the blurred state using only the sharp "Stones" as context.

**Validation:** If the measurement model is sound, the agent will perfectly infer the blurred "deadweight" from the sharp "stones". If the measurement model is flawed, critical information was blurred improperly, and the reconstruction will fail. Blur is the honesty badge; this experiment tests if the blur is lossless.
