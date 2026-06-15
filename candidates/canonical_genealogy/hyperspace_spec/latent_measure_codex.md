**Core Correction**

A universal latent "true content" unit does not exist. Latent content is only measurable after pinning a coder, task family, canon, dependency model, and tolerated error. So the hole closes only if the spec separates two quantities:

```text
cost_ub(W)      = conservative upper bound on bits needed to state wrapper W
evidence_lcb(W) = conservative lower bound on independent evidence supporting W

coin_bits(W) = min(cost_ub(W), evidence_lcb(W))
unpaid_bits(W) = max(0, cost_ub(W) - evidence_lcb(W))
```

Use `coin_bits` for rendered sharpness. Use `unpaid_bits` for blur. Never use a raw upper bound as rendering entitlement.

Let `L_E(X | C)` be codelength in bits under a pinned estimator `E`, canon/context `C`, and arithmetic/entropy coder. Source dependency is handled by source clusters, provenance links, near-duplicate detection, citation graphs, and blocked bootstrap. Redundant sources only get incremental conditional code savings, preferably Shapley-allocated.

**Six Candidate Dials**

| Family | Best Unit | Estimator | Uncertainty | Dependency Model | One-Sided? | Composition |
|---|---|---|---|---|---|---|
| Compression / Expansion | Latent MDL bits: `L_E(W | C)`. Expansion gain: `L_E(D_W | C) - L_E(D_W | C,W)` | MDL, Kolmogorov-style codelength, frozen LLM-as-compressor logloss, sparse/VQ latent code | Block bootstrap over source clusters; coder calibration interval | Conditional codelength gain; Shapley over redundant sources | Cost is an upper bound on ideal code length. Evidence gain needs lower confidence bound | Directly composes with physical entropy bits by chain rule |
| Percent of Frame | Frame share: `alloc_bits(W) / sum alloc_bits(W_i)` | Allocate frame MDL bits by Shapley or ordered MDL | Bootstrap frame membership and allocation order | Shared bits are allocated once | No. It is contextual, not a content bound | Derived ratio only; creates no new bits |
| Kernel Canon | Canonical kernel bits: codelength of minimal sufficient latent core `K_W` | Minimal sufficient statistic, sparse coding, information bottleneck, MDL model selection | Nested-model CI; bootstrap retained features | Encode conditionally on parent canon and shared kernels | Yes for selected kernel codelength; no proof of global minimality | Encode `K_W`, then peripheral residual |
| Connectivity | Conditional link bits plus centrality | PMI/conditional MI graph, graph MDL, k-core, betweenness, eigenvector centrality | Bootstrap edges and graph topology | Partial correlations, separators, source-clustered edges | Link codelength yes; centrality no | Graph edges are entropy-coded relation bits |
| Zoo Unit | Effective taxon-bit: Shapley contribution to `log2(Hill_q)` diversity | Hill numbers, taxonomic distinctness, rarity surprisal, phylogenetic diversity | Bootstrap taxonomy, source weights, clustering | Taxa share branches; count branch evidence once | No for semantic content; yes for taxonomy path code | Encodes taxonomy pointer/path plus residual |
| Deadweight vs Stone | Ablation delta bits: `L_E(D,F | M_without_W) - L_E(D,F | M_with_W)` | Leave-one-out, Shapley ablation, influence functions, k-core prefilter | Block jackknife/bootstrap; interval over refits | Coalitional Shapley for redundancy/synergy | Support should render only from lower bound | Same MDL ledger: loss increase in bits |

**Zoo Unit, Concretely**

The real zoo unit should be an **effective taxon-bit**, not a metaphor.

Build a pinned taxonomy or metric dendrogram over latent specimens. Give each specimen weight:

```text
m_i = dependency-adjusted evidence mass
p_i = m_i / sum_j m_j
```

Then compute Hill diversity:

```text
q = 0: richness-sensitive
q = 1: Shannon effective taxa, H_1 = -sum p_i log2 p_i
q = 2: Simpson/common-taxa-sensitive
```

The wrapper-level unit is its Shapley contribution to `log2(Hill_q)` across the taxonomy. Add two visible sub-dials:

```text
biomass analog      = m_i, how much unique evidence mass supports it
rarity/distinctness = -log2(p_i) plus branch-length distinctness
```

So the zoo dial is not "how important is this idea?" It is: how much effective latent diversity does this wrapper contribute under a declared taxonomy and evidence weighting?

**Deadweight vs Supporting Stone**

Cheap pipeline:

```text
1. Triage with graph signals: k-core, articulation points, betweenness, edge cut.
2. Run local leave-one-out: remove W, repair within radius r, recompute MDL/logloss.
3. For differentiable models, approximate with influence functions.
4. For redundancy/synergy, approximate Shapley over sampled coalitions.
5. Report interval: [ADB_lcb, ADB_ucb].
```

Render rule:

```text
ADB_ucb <= 0      -> deadweight: fade/removable
ADB_lcb > 0       -> supporting stone: sharp support mark, thickness = log(1 + ADB_lcb)
interval crosses 0 -> uncertain: blurred/hatched support
```

Deletion preview should show affected region radius and expected extra bits needed to repair the frame.

**Intrinsic vs Relational**

Almost all latent units are relational.

```text
Compression: coder-relative and context-relative.
Percent of frame: observer/frame-relative.
Kernel canon: task/canon-relative, closest to intrinsic after pinning task.
Connectivity: graph-relative.
Zoo: taxonomy/population-relative.
Deadweight/stone: model/frame/query-relative.
```

There is no absolute intrinsic latent measure comparable to physical entropy-coded reproduction bits. The strongest honest claim is "intrinsic under a declared measurement contract."

**Best Closure**

Use **Canonical Latent Description Bits**, backed by dependency-adjusted evidence:

```text
cost_ub(W) =
  L_E(kernel_W, relation_edges_W, residual_W | canon, task)

evidence_lcb(W) =
  lower_confidence_bound(
    L_E(D | canon, without W) - L_E(D | canon, with W)
  )
  after source dependency correction

coin_bits(W) = min(cost_ub(W), evidence_lcb(W))
```

The other five dimensions should remain dials and diagnostics, but this one closes the COIN hole because it gives a pinned estimator, bits as unit, uncertainty, dependency correction, and physical-bit composition.

**One Validation Experiment**

Use a corpus with many concepts/entities and multiple independent source clusters.

1. Build wrappers from training clusters.
2. Estimate `cost_ub`, `evidence_lcb`, frame share, kernel bits, connectivity, zoo bits, and ablation delta.
3. Hold out whole independent source clusters.
4. Test whether claimed `evidence_lcb` is conservative against realized holdout codelength gain:

```text
realized_gain =
  L_E(D_holdout | C) - L_E(D_holdout | C, W)
```

A 90 percent lower bound should be exceeded by realized independent gain at least 90 percent of the time. If not, the dependency model or estimator is fabricating bits.
