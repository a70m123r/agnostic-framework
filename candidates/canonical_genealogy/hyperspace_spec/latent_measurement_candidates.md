# Latent measurement candidates - canonical menu (v0.1)

*Provenance: a 13-agent Opus workflow (`latent-measurement-candidates`) + cross-model passes from GPT-5.5 ([latent_measure_codex.md](latent_measure_codex.md)) and Gemini ([latent_measure_gemini.md](latent_measure_gemini.md)); brief [latent_measure_brief.txt](latent_measure_brief.txt). 2026-06-15. Closes the load-bearing hole the audit named: latent `measured_bits` was undefined.*

## Convergent recommendation (all three sources agree)

**THE UNIT.** Latent `measured_bits` = **prequential codelength under a pinned, disclosed coder**: `L = sum_t -log2 P_M(x_t | x_<t, frame)`. This is a **sound one-sided upper bound** on Kolmogorov complexity (`K(x) <= |C(x)| + c_C` for ANY model - a worse model only spends MORE bits, never under-counts), it needs **no model-complexity penalty** (the model is never transmitted), and it is the **same unit as the settled physical bits-to-reproduce** (composes by the chain rule). This IS Pav's dial #1.

**THE COIN FIX (codex's structural insight).** Never render a raw upper bound as entitlement - a complex *lie* has high codelength but ~0 evidence. So:
```
cost_ub(W)      = prequential codelength      (upper bound on bits to STATE W)
evidence_lcb(W) = conservative lower bound on independent evidence SUPPORTING W
                  (the ablation / holdout codelength gain, dependency-corrected)
measured_bits(W) = min(cost_ub, evidence_lcb)     -> rendered sharpness
unpaid_bits(W)   = max(0, cost_ub - evidence_lcb) -> blur
```
Report every latent measurement as an **interval**; render to the honest (lower) end.

**FOUR of Pav's six dials are ONE codelength family** - absolute / normalized / residual / leave-one-out views of the same bits:
- #1 compress-expand = `L(W)` absolute.
- #2 percent-of-frame = `L(W)/L(frame)` (or a Shapley allocation for an additive partition that sums to 100%).
- #3 kernel canon = the residual codelength that will NOT shrink under more context (the sufficient-statistic core); 2025 proxy = the **Local Learning Coefficient** (high-LLC = incompressible canon, low-LLC = removable periphery).
- #6 deadweight-vs-stone = ablation delta `L(frame) - L(frame minus W)` (counterfactual codelength increase). Building the Shapley/ablation harness yields #2 and #6 at once.

**SOURCE-DEPENDENCY is automatic via CONDITIONAL codelength:** `delta(new | existing) = L(new | existing_facts)` under the same coder - a redundant source compresses to ~0 extra bits, so it cannot fabricate content. **Independence is an OUTPUT of the measurement, not an assumption** (NCD / conditional-Kolmogorov; plus a total-correlation / PID subtraction for higher-order redundancy).

**Dials #4 (connectivity) and #5 (zoo) are NOT pure codelength** - they need a graph/diversity layer (an NCD-distance graph; the zoo unit = an **effective taxon-bit** = a wrapper's Shapley contribution to Hill-number diversity, with `biomass = evidence mass` and `rarity = -log2 p(W)` sub-dials). They are honest **diagnostics/dials, not content bounds** (not one-sided).

**INTRINSIC vs RELATIONAL (unanimous):** there is **no intrinsic latent measure**; every unit is relational (coder / frame / graph / corpus / system-relative). The honest standard is the **pinned relational bit** - "intrinsic under a declared measurement contract." Whatever is declared must be disclosed for the COIN to stay honest.

**VALIDATION (two runnable falsifiers):** (a) codex's **holdout calibration** - is the claimed 90% `evidence_lcb` exceeded by the *realized* independent-holdout codelength gain at least 90% of the time? If not, the estimator is fabricating bits. (b) gemini's **Amnesia Drop** - blur a dense graph by discounted bits, then reconstruct the original from only the sharp "stones"; if the blur was lossless an agent recovers the deadweight, if not it fails.

**Prototype RUN (2026-06-15, [tests/latent_measure_tests.py](tests/latent_measure_tests.py), [tests/LATENT_RESULTS.md](tests/LATENT_RESULTS.md)).** A first runnable instantiation using real lossless compressors as the pinned coders (gzip / bz2 / lzma - the LLM-coder version needs logprob access, same mechanism) on a synthetic corpus with known ground truth (independent *stones*, redundant *duplicates*, a high-cost **uncorroborated fabrication** = the complex lie). Result: **11/12 checks; 3 of 4 falsifiers robust across ALL three coders** - the **complex lie is blurred** (`measured_bits` renders at 0-1% of its cost: `min(cost, evidence)` works), **evidence discriminates** corroborated from fabricated, and **deadweight vs stone separates** (pairwise conditional). The 4th (conditional-redundancy) is robust across the LZ-family coders; **bz2/BWT is unsuitable for the conditional measures** = a coder-choice finding (use LZ-family or LLM coders). **Coder-relativity:** absolute bits move ~88% across coders but the render *verdicts* hold = the **pinned relational bit confirmed**. The first pass also surfaced (and the corrected estimators fixed) two issues the research had predicted: a strong coder manufactures spurious holdout-evidence (fixed by **baseline-relative evidence**) and leave-one-out can't separate mutually-redundant pairs (fixed by the **pairwise conditional**; full fix = Shapley).

---

# Latent Measurement Candidates - A Menu of Units to Close the COIN Hole

**Scope.** The COIN says `rendered_sharpness(x) <= measured_bits(x)` and "never render a fake measured bit." On the physical/text axes `measured_bits` is settled: entropy-coded bits-to-reproduce under a pinned coder (lzma-9 / LLM-as-arithmetic-coder, `harness.py`). On the latent axes (WHAT / WHO / WHY) `measured_bits` is currently a **badge** - no coding scheme, no unit scale, no estimator, no interval, no source-dependency model, no per-axis calibration. This document is the menu of candidate UNITS that can replace the badge with a real measurement, each turned into a DIAL, each scored against the five soundness requirements:

```
[a] one-sided upper bound on true content (so blur can only be honest)
[b] computable under a pinned/disclosed estimator
[c] stated uncertainty interval
[d] source-dependency / independence model (redundant evidence must not fabricate bits)
[e] composes with the settled PHYSICAL unit (entropy-coded bits under one pinned coder)
```

**The one structural finding that organizes the whole menu.** There is **no absolute intrinsic latent bit.** Every candidate is constitutively relational (coder-relative, frame-relative, graph-relative, query-relative, or corpus-relative). The honest object is therefore not a number but a **measurement CONTRACT**, and the COIN is enforced by a two-sided split that both external models (codex + gemini) converged on independently:

```
cost_ub(W)       = bits to STATE wrapper W under a pinned coder, given the disclosed frame   (UPPER bound)
evidence_lcb(W)  = bits of INDEPENDENT support for W, dependency-corrected, lower-confidence  (LOWER bound)
coin_bits(W)     = min(cost_ub, evidence_lcb)        <- this is what rendered_sharpness is capped by
blur(W)          = unpaid_bits = max(0, cost_ub - evidence_lcb)
```

A raw upper bound is **not** a rendering entitlement: a coder can spend many bits stating an elaborate *unsupported* claim, and rendering THAT sharp is exactly the fabricated bit the COIN forbids. Sharpness must be *paid for by evidence, capped by statability*. Five of Pav's six dials are READOUTS of one prequential-codelength meter `L_E(. | C)`; the other piece (zoo) is a set-level read of the same logarithm. Two of the six (connectivity, zoo) only become bits in narrow pinned forms and otherwise must be carried as **metadata that locates/weights content, never substituted for bits**.

---

## THE SIX UNITS - the menu

For each: definition / estimator / uncertainty / dependency model / one-sided? / composition-with-physical / DIAL semantics / audit scorecard `[a|b|c|d|e]`.

---

### (1) COMPRESSION / EXPANSION - the spine

**Definition.** `cost_ub(W) = L_E(kernel_W, edges_W, residual_W | C)` = prequential / MDL codelength to STATE the wrapper under a pinned coder E, conditioned on the disclosed frame C. Expansion gain = `L_E(D_W | C) - L_E(D_W | C, W)` = the bits W lets you save when re-deriving its consequences.

**Estimator.** Pinned coder: either lzma-9 on the canonical serialization (already in `harness.py`) or a frozen open-weights LLM as arithmetic coder, `codelength = sum_t -log2 p_model(x_t | x_<t)` (Deletang, *Language Modeling Is Compression*, ICLR 2024). No model-complexity penalty needed - the model is never transmitted, so a complex-but-useless model simply wastes prediction bits and is penalized automatically (*In-context Learning and Occam's Razor*, arXiv:2410.14086).

**Uncertainty.** Block bootstrap over SOURCE CLUSTERS (not tokens), plus a coder-calibration band (lzma vs zlib vs bz2 spread, exactly as `harness.py` already reports; the cosmic-coin probe found a ~1.17-2.8x band). Report the band, render the upper-bits / lower-sharpness end.

**Dependency model.** Native: CONDITIONAL codelength `delta_bits(new | existing) = L_E(new | existing_facts)`. A redundant source compresses to ~0 extra bits because the coder already predicts it (NCD machinery, Cilibrasi-Vitanyi). Independence becomes an OUTPUT, not an assumption.

**One-sided?** YES. Any achieved lossless codelength upper-bounds K: `K(x) <= |C(x)| + c_C`, `c_C` = decompressor size (Shportko 2026, arXiv:2603.21567). A worse coder spends MORE bits, never fewer.

**Composition.** IDENTITY - same unit as the physical axis, additive by chain rule. This is what makes the keystone's "one logarithm" literal, not analogical.

**DIAL semantics.** Knob = coder strength + conditioning context. Range: coder - {lzma-9, frozen-LLM-v}, context - {empty ... full-log}. Default: frozen-LLM coder, conditioned on canon + immediate frame. Reaction when you turn it: stronger coder - some periphery becomes compressible (blurs), canon survives; growing context - conditional bits shrink as the frame predicts more of W.

**Scorecard.** `[a:YES | b:YES | c:YES | d:YES | e:YES]` - **the only family that passes all five natively.** This is the unit; the other five calibrate, normalize, locate, or weight it.

---

### (2) PERCENT-OF-FRAME - derived ratio (needs an additive backbone)

**Definition.** `share(W) = alloc_bits(W) / sum_i alloc_bits(W_i)` = W's bits as a fraction of the frame's total bits.

**Estimator.** Allocate the frame's MDL bits by a backbone that *partitions*: Shapley (efficiency axiom - shares sum EXACTLY to the frame total; llmSHAP, arXiv:2511.01311) OR in-model context-mixing share (Value Zeroing / ALTI, which sum to 1). **Never raw attention weight** - the 2025 faithfulness result shows layernorm/FFN/value-projection rescale it, so raw softmax is an artifact, not a measurement.

**Uncertainty.** Bootstrap frame membership + allocation order.

**Dependency model.** Shared bits allocated ONCE (that is what Shapley efficiency buys); redundancy decomposed via the hierarchical KL / total-correlation split (arXiv:2504.09029) so double-counted evidence is subtracted before shares are formed.

**One-sided?** NO. It is contextual/relative - can under- or over-state under systemic frame redundancy. (Subtractive normalization is not bounded.)

**Composition.** Dimensionless [0,1]; multiply by frame physical bits to re-enter the ledger.

**DIAL semantics.** Knob = frame boundary + allocation rule (Shapley vs context-mixing). Range: frame - {sub-frame ... whole log}. Default: current sub-frame, Shapley allocation. Reaction: shrink the frame - W's share rises; swap allocation rule - shares re-partition live; this is the SAME number as dial #1, normalized.

**Scorecard.** `[a:NO | b:YES | c:YES | d:YES via Shapley | e:partial]`. Pav dial #2. Honest use: report as a relative share, never let the ratio alone drive sharpness.

---

### (3) KERNEL CANON - the irreducible residual of the codelength

**Definition.** `K_W` = codelength of the minimal sufficient latent core = the part of `L_E(W | C)` that will NOT shrink under more context. The algorithmic-sufficient-statistic floor: Kolmogorov structure function / AMSS split, canon = `K(S*)` (structure), periphery = `log|S*|` (residual index) - Vereshchagin-Vitanyi; Epstein 2024 (arXiv:2406.05903).

**Estimator.** Nested-model MDL selection / information-bottleneck elbow (`min I(X;T) - beta*I(T;Y)`) / sparse-code active dimension. **2025 computable proxy:** the Local Learning Coefficient is ~linearly correlated with compressibility (arXiv:2510.12077) - high-LLC = incompressible canon, low-LLC = removable periphery. SAE structure gives a geometry: canon = minimal spanning atom-community near the root of the HSAE tree (arXiv:2602.11881), size ~ intrinsic manifold dimension up to the "geometric wall" (arXiv:2605.09887); periphery = diluted redundant atoms past the wall.

**Uncertainty.** Nested-model CI / rate-distortion curve gradient at the chosen beta.

**Dependency model.** Encode CONDITIONALLY on parent canon + shared kernels, so siblings don't re-pay the shared core.

**One-sided?** YES for the SELECTED kernel's codelength (it is an achieved code). NO proof of GLOBAL minimality - true AMSS is uncomputable. **Disclose this:** the kernel/periphery split is the prequential UPPER approximation to an uncomputable ideal.

**Composition.** Encode `K_W` then the peripheral residual; additive.

**DIAL semantics.** Knob = complexity budget alpha / bottleneck beta (the "how much structure do I keep" dial). Range: alpha - [0, L_E(W|C)]. Default: the structure-function kink k* (where compression stops buying anything). Reaction: lower alpha - only the hardest canonical core survives, periphery blurs; this dial is the closest thing to "intrinsic" the latent axis has - but it is intrinsic as a SHAPE (the kink exists), not as a number (its location drifts with coder strength).

**Scorecard.** `[a:YES local | b:YES | c:YES | d:YES | e:YES]`. Pav dial #3.

---

### (4) CONNECTIVITY - a LOCATING measure; bits only via the ablation/MDL route

**Definition.** Bits-valid form = graph-MDL contribution `DL(graph \ W) - DL(graph with W)`, OR the von-Neumann spectral-entropy ablation delta `C_E(W) = |S(G) - S(G\W)|` with `S(G) = -sum (lambda_i/2) log2(lambda_i/2)` over the normalized-Laplacian spectrum (log base 2 - bits; non-negative by construction since removing a node cannot increase complexity). Use the **hypergraph (s-line-graph)** version because fact wrappers bind 6 axes at once = higher-order edges.

**Estimator.** Pinned spectrum/coder; ablation granularity (node / k-core peel / hyperedge) is a disclosed dial. There is NO canonical connectivity bit - the Nov-2025 "Zoo of Centralities" (arXiv:2511.05122) catalogs 400+ measures and names redundancy/naming-chaos as the field's core problem, so the COIN must PIN ONE and disclose it.

**Uncertainty.** Jackknife / bootstrap over fact-log edges - distribution over the bits estimate; render the upper end.

**Dependency model.** Use **effective-resistance / current-flow** centrality, NOT betweenness. Parallel redundant routes LOWER resistance, so redundant corroboration adds ~0 bits (the structural analogue of parallel resistors). Betweenness double-counts and is provably not a resilience metric (Bhagat-Conway, Findings 2025).

**One-sided?** The entropy-ablation / MDL form is non-negative (one-sided). Raw loss-delta centralities are SIGNED - **must clamp negatives to 0** (deadweight = 0 bits) or they fabricate/subtract content. The pure spectral form needs an arbitrary scale and does NOT compose without the MDL route.

**Composition.** Via the MDL route ONLY (same coder, same units). The raw spectral form does not compose - disclose.

**DIAL semantics.** Four knobs: (i) which spectrum/coder (estimator dial); (ii) ablation granularity node-k-core-hyperedge (load-bearing-depth dial); (iii) redundancy-discount strength raw-count - effective-resistance (the source-independence dial - **turning this is what makes the COIN honest**); (iv) frame scope, feeding `C_E(W)/S(G)` = W's relative share of structural entropy (Pav dial #2 link). Default: hypergraph MDL route, effective-resistance discount, current sub-frame.

**Scorecard.** `[a:YES MDL/clamped | b:YES | c:YES | d:YES eff-resistance | e:partial]`. Pav dial #4. **HONESTY FLAG:** report raw centrality as importance METADATA that weights/locates content, never as `measured_bits`. Rendering a high-centrality node sharp because it "looks important" is exactly the fabricated bit.

---

### (5) THE ZOO UNIT - effective-taxon-bits (the rarity/diversity layer)

**Definition.** W's contribution to `log2(qD^Z)`, the log2 of the similarity-discounted **effective-specimen-count** of the menagerie, under a PINNED latent similarity kernel Z and a dependency-adjusted evidence-mass abundance p. Leinster-Cobbold order-q true diversity:

```
qD^Z(p) = ( sum_i p_i (Zp)_i^{q-1} )^{1/(1-q)},   (Zp)_i = sum_j Z_ij p_j  = "ordinariness" of specimen i
zoo_bits(W) = log2 qD^Z(P) - log2 qD^Z(P \ W)     (leave-one-out form)
            = Shapley_W[ log2 qD^Z ]               (order-fair / redundancy-correct form)
```

This is "how many bits of effective latent DISTINCTNESS W adds to the collection." Sub-dials: biomass = `p_i` (unique evidence mass); rarity/distinctness = `-log2 (Zp)_i` + EDGE/ED fair-proportion branch-length distinctness.

**Estimator.** Similarity-aware Vendi family = `exp(order-q entropy of the eigenvalue spectrum of a pinned similarity kernel)` (Pasarkar-Dieng, AISTATS 2024, arXiv:2310.12952). The probability-weighted Vendi Score (pVS, arXiv:2509.16133) is PROVEN set-monotone (a genuinely new specimen never decreases diversity - `zoo_bits >= 0`) + redundancy-invariant (a duplicate / shared eigen-direction adds ~0).

**Uncertainty.** Chao-Jost COVERAGE-based rarefaction with bootstrap CIs. Sample-COVERAGE literally IS the blur knob - low coverage - wide CI - render blurry. (Caveat: if the fact-log is a CENSUS not a sample, coverage collapses and the interval must come from kernel/coder uncertainty instead - see open questions.)

**Dependency model.** Redundant sources collapse into a shared eigen-direction - contribute 0 unique bits. PID unique/redundant/synergistic split. **Critical:** abundance `p_i` must be dependency-adjusted (source-clustered, near-duplicate-collapsed) BEFORE diversity is computed - if `p_i` is raw mention-count, the unit *rewards repetition* (the model-collapse failure Sweep-2 guards against).

**One-sided?** YES for the taxonomy-path code and for `log2(effective-number)` **RELATIVE TO A PINNED KERNEL**. NO in general - a richer embedding can reveal previously-collapsed distinctions and RAISE the count. So it is upper-bound w.r.t. a DISCLOSED kernel, not absolute.

**Composition.** `log2(effective number)` is already in bits; additive given independence from the physical coder - **but only as a SIBLING fiber** (a taxonomic-locator axis), not folded into the compression axis (a reproduction cost and an effective-count log are commensurable, not obviously summable; see open Q).

**DIAL semantics.** Headline knob = Hill order q (q=0 richness/rare-sensitive - q=1 Shannon/Vendi - q=2 Simpson/common-sensitive - q-inf dominant cluster). Secondary knobs = kernel bandwidth (lump-split the taxonomy), coverage (sharpen-blur), abundance rule (raw-dependency-adjusted). Default: q=1, pinned embedding kernel, dependency-adjusted mass. Reaction: turn q toward 0 and watch rare lonely specimens light up; widen bandwidth and watch specimens merge and the effective-N collapse.

**Scorecard.** `[a:YES rel. kernel | b:YES | c:YES coverage | d:YES eigen-collapse | e:conditional-on-pinned-kernel]`. Pav dial #5.

---

### (6) DEADWEIGHT vs SUPPORTING STONE - the leave-one-out / keystone dial

**Definition.** `LB(W) = max(0, L_E(Frame \ W | C) - L_E(Frame | C))` = the extra bits the rest of the log costs to reproduce once W is deleted - the structural load W bears. **This is NOT W's own `measured_bits`** - it is an importance/structure score that LOCATES and WEIGHTS W's content. Reporting an ablation drop AS W's `measured_bits` would fabricate a bit. It renders as a separate **load-bearing GLOW** channel, orthogonal to sharpness.

**Estimator (cheap - faithful ladder).**
- Rung 0 (graph-only): k-core / k-truss coreness + corona membership. The keystone test is exact percolation math (Dorogovtsev-Goltsev-Mendes, arXiv:1505.05484): k-core collapse is a **hybrid discontinuous transition** - removing one corona vertex can trigger a diverging avalanche. corona member = keystone; interior-core = deadweight.
- Rung 1 (one-pass): attribution patching (2 fwd + 1 bwd). Screen only - LayerNorm makes the Taylor term vanish for residual-aligned directions. Clamp negatives to 0.
- Rung 2 (retraining-free counterfactual): Ablation-Based Counterfactuals (arXiv:2406.07908) / AttriBoT (ICLR 2025, ~300x cheaper). Use **Optimal Ablation** (Li-Janson, NeurIPS 2024) as the canonical baseline `c* = argmin_c E[loss after replacing W with c]` - this pins ONE baseline and fixes the documented flaw that importance flips with zero/mean/resample ablation.
- Rung 3 (the bound): LOO re-compression delta under the pinned coder; averaged-over-coalitions via In-Run Data Shapley (ICLR 2025, arXiv:2406.11011, ghost dot-product, one pass).

**Uncertainty.** Block jackknife / refit ensemble - `[ADB_lcb, ADB_ucb]`; OR Daunce (arXiv:2505.23223) for attribution-with-error-bars. Render the glow at the LOWER CI end. Note: corona wrappers are near a discontinuity - genuinely heavy-tailed, high-variance estimates exactly where they matter most - render the most important stones with a deliberately flickering/uncertain glow.

**Dependency model.** Intrinsically redundancy-safe - deleting one of K mirrored wrappers costs ~0 extra bits (survivors already encode it). For the Shapley form, wrap with **ReSHAP** (OpenReview Ezfgx1RVdY), which PROVES no attribution is both equal-division AND duplication-invariant - **deliberately choose duplication-invariance** (K mirrors share ONE keystone credit). Effective-resistance is the graph analogue.

**One-sided?** YES, lcb-clamped. Removing useful structure can only RAISE survivors' codelength, so `LB` over-states load, never under-states - glow can only be honest. Raw loss-deltas are signed; clamping discards the "actively harmful wrapper" signal, which should be logged separately as an **anti-keystone / contradiction flag** (feeding the dead-children tally), not silently zeroed.

**Composition.** Identical MDL ledger (a loss increase in bits) - but sits BESIDE per-axis `measured_bits`, never inside it.

**DIAL semantics.** Knobs: k (k-core depth - raise it and watch the arch shed peripheral stones); what-you-delete (wrapper / hyperedge / k-shell); counterfactual baseline c* (sweep optimal-mean-zero-resample and watch importances flip - the spread IS a faithfulness readout); redundancy-discount strength (raw LOO - ReSHAP - effective-resistance - **this is the COIN-honesty knob**); frame scope (`LB(W)/L(Frame)` = percent-of-frame LOAD, ties to dial #2). Default: Rung-3 re-compression delta, optimal-ablation baseline, duplication-invariant discount.

**Render rule.** `ADB_ucb <= 0` - deadweight (fade/removable, no glow); `ADB_lcb > 0` - stone (bright glow, thickness = `log(1+ADB_lcb)`, cascade-shimmer if in corona); interval crosses 0 - uncertain (hatched/flickering).

**Scorecard.** `[a:YES lcb-clamped | b:YES sketching | c:YES | d:YES Shapley/ReSHAP | e:YES]`. Pav dials #4+#6 are built by ONE ablation harness. A Shapley value IS an averaged leave-one-out AND a normalized share - dial #6 and dial #2 are the same object.

---

## Scorecard summary

```
UNIT                         a:bound   b:comp  c:interval  d:depend   e:compose   VERDICT
(1) Compression/expansion      YES       YES      YES         YES        YES(=)     SPINE - closes the hole
(2) Percent-of-frame           NO        YES      YES         YES(Shap)  partial    derived ratio of (1)
(3) Kernel-canon               YES(loc)  YES      YES         YES        YES        residual view of (1); near-intrinsic SHAPE
(4) Connectivity               YES(MDL)  YES      YES         YES(eff-R) partial    LOCATES bits; metadata otherwise
(5) Zoo-diversity              YES(ker)  YES      YES(cov)    YES(eig)   sibling    WEIGHTS bits; set-level monopoly
(6) Deadweight/keystone        YES(lcb)  YES      YES         YES(ReSHAP) YES       LOO view of (1); load GLOW, not bits-of-W
```

**Banned as a bit-source:** V-usable / Conditional V-information. It is in bits and baseline-relative so it LOOKS perfect - but it VIOLATES the data-processing inequality (a stronger predictive family V *manufactures* apparent bits; Xu 2020, arXiv:2002.10689) and held-out estimates are LOWER bounds. That is the WRONG-SIDED error: it would let the viewer render SHARPER than true content. Permitted at most as a ranking signal on a clearly-non-bit channel. This is the single most dangerous near-miss in the digest.

---

## The ZOO unit, answered concretely

**Question: if latent space were a zoo of specimens, what is the unit?**

**Answer: effective-taxon-bits** = `log2` of the similarity-discounted effective-specimen-count a wrapper adds to the menagerie (`zoo_bits(W)` above). Concretely, this is **NOT**:
- **not biomass** (raw frequency / mention-count) - that rewards repetition and inverts the COIN;
- **not rarity surprisal** (`-log2 P(x)`) - that is sound as bits but is just the *compression dial in disguise* (surprisal under a density model).

The genuinely new thing the zoo unit measures is **set-relative non-redundant distinctness**: a wrapper's marginal contribution to the effective number of *mutually-dissimilar* specimens, where `qD^Z = exp(order-q entropy of the similarity-kernel eigenspectrum)`. A duplicate adds 0 to the eigenspectrum exactly as a redundant bit adds 0 entropy under the pinned coder - redundancy-invariance is the set-level form of "never render a fake measured bit."

**The zoo's monopoly and its blind spot.** It is the ONLY unit that sees the COLLECTION as a whole. It is therefore blind to three things the other five catch: (i) internal reproduction cost - a baroque-but-lonely specimen and a simple-but-lonely specimen get the same `zoo_bits` (compression separates them); (ii) load-bearing-ness - a maximally-distinct specimen can still be deadweight (ablation separates them); (iii) graph position (connectivity separates them). Use it as the **diversity/rarity WEIGHT**, paired with the compression bit-bound - never substituted for it.

**The leak to nail down:** `zoo_bits` is upper-bound only relative to a pinned kernel Z. Ship `Z + q + bandwidth + coverage` as the declared frame-lock, or the bound leaks the instant the embedding is swapped. On cross-model kernel disagreement, render the MAX-blur (smallest effective-N), which preserves the bound.

---

## The philosopher's verdict: INTRINSIC vs RELATIONAL

**Verdict: there is no intrinsic latent scalar. Every candidate is relational - but the COIN survives because it rests only on what is frame-INVARIANT.** The right frame is a **gauge theory**: `measured_bits` is a *coordinate* (gauge-dependent); the COIN inequality and the differences/orderings are the gauge-invariant *physics*.

There are five distinguishable relativities (separate them or the audit cannot bite):
1. **CODER-relative** (compression, kernel-canon) - `K` defined up to `+c_C`; a choice of origin on the bit axis.
2. **FRAME/CONTEXT-relative** (percent-of-frame, conditional codelength) - the conditioning prefix is the frame.
3. **GRAPH-relative** (connectivity) - defined against the current edge set.
4. **QUERY/SYSTEM-relative** (deadweight-vs-stone) - defined against a value-function + ablation baseline.
5. **CORPUS-relative** (zoo, rarity) - defined against a pinned kernel + reference population.

Relativities 1, 2, 4 and the bit-forms of 3, 5 all collapse to ONE object: prequential conditional codelength `L_E(x | C)`, read four ways (absolute / normalized / residual-after-kernel / leave-one-out).

**The proof there is no intrinsic bit:** the Kolmogorov invariance theorem gives `K_U(x) <= K_V(x) + c_{U,V}` - the constant is bounded but unbounded in magnitude for a fixed finite object, so two coders can disagree arbitrarily on a single concept. And a concept carries *no canonical measure* (no metres, no volume), so there is no canonical probability and hence no canonical `-log2 P(x)`. **This is the deep asymmetry to post, not hide:** the physical axis is first-order (metres are decoder-free); the latent axis is second-order - a measurement *of a model*. The latent viewer is honestly a viewer of one coder's model of the domain, not a view-from-nowhere.

**The near-intrinsic residue:** kernel-canon is closest to intrinsic because the *claim that the structure-function has a kink* (that compression goes flat at the AMSS) is more coder-stable than the bit-value at the kink. The intrinsic content is a **SHAPE**, not a number.

**What survives every gauge transformation (so the COIN holds):**
- **One-sidedness** - any achieved lossless codelength upper-bounds K in EVERY gauge (the load-bearing invariant; max of two upper bounds is an upper bound, which is why "render the blurrier of two coders" is honest).
- **Sign/order of differences** - deadweight-vs-stone and the ranking of load-bearing-ness cancel the shared additive gauge constant (bits-per-byte ratios are empirically stable, arXiv:2404.09937). Render the COMPARATIVE sharply; render the ABSOLUTE count with the coder-disagreement band as blur.
- **The structure-function kink exists** (even though its location drifts).

**If relational (it is), this MUST be disclosed - the minimal gauge-fixing set:** `{ coder + tokenizer + quantization + fidelity tau ; frame/ancestry prefix ; ablation baseline + value-function ; similarity kernel + bandwidth + reference population ; source-dependency / provenance model ; uncertainty interval }`. These six tags ARE the observer's "glasses" in the substrate's FRAME=agnostic-substrate / GLASSES=observer split. Disclosing them converts "observer-shaped space" from an objection into a posted, auditable frame-lock - the identical discipline already ratified for the heredity / gate-terms frame-relative classifier. **Forbidden:** cross-contract differencing (the E-units guard - absolute appearance-bits are unit-incommensurate across phenomena; never difference them across pinned contracts).

---

## RECOMMENDATION - what to prototype first

**Prototype FIRST: the conditional/prequential codelength harness (dial #1), split into `cost_ub` and `evidence_lcb`, yielding dials 1/2/3/6 from one artifact.**

Rationale:
1. It is the **only** unit that closes the hole natively (passes all five requirements).
2. It is the **same harness already built** for the physical/text axes (`candidates/cosmic_coin_probe/harness.py`, lzma-9 + per-axis Gaussian) - you EXTEND the pinned coder to score WHAT/WHO/WHY axis-content conditioned on the disclosed frame and the prior log. You build essentially nothing new.
3. It instantiates **four of Pav's six dials at once** (absolute / normalized / residual-after-kernel / leave-one-out are all readouts of the same meter) and composes with the physical axis by construction.

**Sequence (cheapest-first ladder):**
- **Step A.** Pin the latent serialization (the gating decision - see open Qs) + the coder E. Implement `cost_ub(W) = L_E(W | frame)`.
- **Step B.** Implement `evidence_lcb(W)` = lower-confidence-bound on the conditional marginal codelength gain over the prior log, with blocked bootstrap over source clusters (so ten newspapers copying one wire count as ONE). Render `coin_bits = min(cost_ub, evidence_lcb)`, `blur = max(0, cost_ub - evidence_lcb)`.
- **Step C.** Add the LOO ablation harness (dial #6) - reuses the same coder; gives connectivity (dial #4) via the graph-MDL route as a near-freebie.
- **Demote** connectivity-as-centrality and zoo-as-count to **Stratum-2 render-prominence metadata** until the validating experiment proves they earn a place on the ledger (the "formalism-must-pay" test).

**The DIAL to ship first:** the **redundancy-discount knob** on `evidence_lcb` (raw marginal - conditional - source-cluster-blocked). This is the single knob that makes the COIN honest, and turning it is the most diagnostic watchable reaction (redundant corroborators visibly collapse toward 0 bits).

**THE ONE VALIDATING EXPERIMENT - the unified holdout / "Amnesia-Drop" / redundant-source non-inflation test:**

On the existing ~1029-fact substrate (or a 1000-node densely-redundant technical spec), measure every node with `cost_ub + evidence_lcb`, blur by `coin_bits`. Then:
1. **Redundant-source leg (cheapest, run first):** take a fact from one route (e.g. iPhone-15-Pro via apple.com), add its independent corroborator already on disk (GSMArena), measure `delta_bits(second_source | log_with_first)`. PASS = near-zero marginal bits. **Adversarial sub-leg:** paste the SAME source text twice - the second paste must score ~0. If it scores full bits again, the dependency model is broken and the COIN leaks.
2. **Holdout leg (the falsifier):** hold out whole INDEPENDENT source clusters; check the claimed 90% `evidence_lcb` is exceeded by realized held-out codelength gain -90% of the time. If not, the estimator is FABRICATING bits - demote the unit (claim-lifecycle: demoted-not-killed, dated record).
3. **Reconstruction leg:** can an independent agent rebuild the blurred deadweight from the sharp stones? If reconstruction fails, the blur was lossy = the model hid bits.

This single experiment validates requirements [a], [d], and the dial simultaneously, on data already on disk. It is the cheapest real falsifier and it is not yet run.

---

## SPECULATION [SPEC] (disclosed, register-shift)

*The following are out-of-box conjectures, explicitly NOT load-bearing for the recommendation above.*

- **[SPEC] The structure-function kink as a "latent Planck floor."** If the AMSS kink k* turns out to be *coder-compute-dependent* (an epiplexity-style horizon that recedes as the learner's budget grows) rather than a fixed constant, then "the smallest meaningful word" is scale-relative, and kernel-canon is not near-intrinsic but just another gauge choice. The decisive observable: does a 2x-stronger coder always find more canon, or does k* converge? If it converges across a coder ladder, we have a genuine latent invariant - the first thing on the latent axis that earns the word "intrinsic."
- **[SPEC] Render gauge-disagreement as TEXTURE, not as max-blur.** The unexplored option-c: instead of collapsing two coders/baselines to the blurrier one, render the *invariants* (sign/order/kink-exists) sharp and render the gauge-variant absolute count as a BAND whose width IS the disagreement. This makes the gauge-dependence honest-by-display rather than hidden - arguably the strongest move, and the natural visual home for the intrinsic/relational truth.
- **[SPEC] Anti-keystones deserve a "rot" channel.** Wrappers whose removal *improves* survivor compression (contradictions, stale facts, noise) are currently clamped to glow=0. They may deserve a NEGATIVE-glow channel feeding the dead-children falsification tally - turning the deletion dial into a contradiction-detector, not just an importance meter.
- **[SPEC] The zoo and compression dials are the same logarithm at two scopes.** `qD^Z = exp(order-q entropy of an eigenspectrum)` is the identical exp-of-entropy functional whether applied to one object's token distribution (compression) or the collection's eigenvalues (zoo). If this is literally one operator parameterized by scope, the six dials may be *three* (compress / locate / weight), each readable at object-scope or set-scope - a cleaner taxonomy than six.
- **[SPEC] Per-axis coders.** WHY is structurally the blurriest axis, WHO carries a Stigler attribution cap, WHERE/WHEN are Radon-tomographable but WHAT/WHO/WHY are only graph-coverage-measurable. It is plausible the COIN needs SIX pinned coders, not one - each axis a different second-order measurement of a different model-facet. This would multiply the harness cost but might be the only honest design.

---

## QUESTIONS WE SHOULD BE ASKING *(register-shift: stepping out of the formalism to interrogate the frame itself)*

- **Is cross-model agreement the whole game rather than a calibration detail?** If a latent bit is only trustworthy when two pinned coders agree within a rung, then the canonical atlas should *require* -2 disclosed coders and treat divergence > one rung as forced blur (or as rendered texture). That reframes the COIN from "measure once, render" to "triangulate, then render the agreement." Are we building a measurement or a consensus instrument?
- **Should the pinned coder be the SUBJECT, not a nuisance parameter?** If the latent viewer is honestly a viewer of *one coder's model of civilization*, maybe the right product is not "a view of the domain" but "a view of what THIS coder believes the domain is" - and the interesting signal is where coders *disagree*, which is exactly the map of contested knowledge. Are we hiding the most valuable layer by averaging it out?
- **Census or sample?** The whole zoo-uncertainty machinery (Chao-Jost coverage) assumes the fact-log is a SAMPLE from a larger population with unseen species. But we *control* the append-only log - it may be a census, in which case the CI collapses and the blur must come entirely from coder/kernel uncertainty. Which is it, and does the answer differ per axis?
- **What is the MEASURED additivity defect, in bits, on real data?** The keystone claim is `anchor_bits + window_bits = path_bits` (chain rule). Shared-ancestor double-counting and prefix non-monotonicity threaten it. The right question is not "is it additive?" but "what is the additivity defect in bits on the real 1029-fact corpus, and is it below one rung?" If not, the COIN is *approximate* on the latent fiber and must say so - in bits.
- **Does the bitemporal substrate need to version the coder?** The frozen-coder assumption gives `K(x) <= |C(x)| + c_C`. If a deprecated coder is swapped (cf the Fable takedown), `c_C` shifts and all historical `coin_bits` move. Should the coder be part of the as-of-tau clock - i.e. is `measured_bits` a function of *when you measured*, not just *what you measured*?

---

## Open sub-questions for Pav

1. **Serialization is the gate.** What is the canonical, pinned string/graph rendering of a latent wrapper (kernel + edges + residual) that the coder ingests? Two serializations of "the same idea" give different bit counts. Nothing is comparable until this is fixed - it is the latent analogue of `harness.py`'s 1km / 1e-3 dex quantization, and it is currently undefined. **This blocks every number.**
2. **One coder or six?** Does `evidence_lcb` need a per-axis coder (WHY blurriest, WHO Stigler-capped, WHERE/WHEN tomographable but WHAT/WHO/WHY only graph-coverage-measurable)? One pinned latent coder, or six?
3. **Duplication-invariance vs additivity** - ReSHAP proves you cannot have both. Confirm we want duplication-invariance (K mirrored facts credited as one) and accept that per-wrapper bits will NOT naively sum to the frame total (percent-of-frame is then defined against the non-redundant union, not a sum). Sign off on the chosen axiom.
4. **Do connectivity (#4) and zoo (#5) earn the LEDGER or only metadata?** They pass the audit only in narrow pinned forms. The "formalism-must-pay" test: if including their bits in `coin_bits` changes no held-out reconstruction outcome, they are decoration *by measurement* and should be demoted to Stratum-2 prominence modulators - keeping only 1/3/6 (+2 as a derived ratio) as bit-bearing. Run experiment A4 to decide.
5. **Glow per-axis or per-wrapper?** A wrapper can be a keystone on WHY but deadweight on WHEN. Six glows (more honest, 6x ablation cost) or one (cheaper, coarser)?
6. **Census vs sample for the blur source** (see Questions above) - which supplies the honest interval when coverage-rarefaction doesn't apply?

---

**Files of record:** the recommended prototype extends the existing pinned harness at `candidates/cosmic_coin_probe/harness.py` (lzma-9 + per-axis Gaussian, model-bits counted) - the latent axis is the same harness over a different, pinned content serialization. The cost_ub/evidence_lcb/coin_bits split and the held-out source-cluster falsifier are the two external-model (codex + gemini) convergence points and should be treated as ratified design seats.
