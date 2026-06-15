# The block-universe substrate and the compiler

SPEC-ONLY analysis for the hyperdimensional canonical-space viewer. Resolves four questions: (1) the block as a static N-D coordinate object keyholes write into; (2) compile = monotone fidelity accretion from an append-only fact-log; (3) the eternalism verdict; (4) the honesty guards. Binds to `D:\hyperspace_units\UNITS_latent_radix_ceiling.md` (the `measured_bits` unit, radix, ceiling) and to the already-built `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate\compile_substrate.py` (the ~80%-present compiler). It does not fork either.

Everything below is anchored to the keystone (one logarithm does FOUR jobs) and the COIN law `rendered_bits(x) <= measured_bits(x)` (blur is the honesty badge; never render a fake measured bit).

---

## 0. One-paragraph statement of the resolution

There are TWO blocks, and conflating them is the only reason the question feels hard. The **territory-block T** is the static N-D manifold of what actually happened/exists (spacetime + latent axes); nothing about it changes. The **substrate-block S** is the compiled record of `measured_bits` ABOUT T -- a materialized view, a pure function of the append-only keyhole-event log. S is *also* static in the precise sense that it is a deterministic function of its log (replay the log, get the same S), but S GROWS as the log grows. "Observation across time" appends events that raise `measured_bits(x)` about a FIXED region x of T; we never edit T, we monotonically sharpen our chart S of it. The COIN law `rendered_bits(x) <= measured_bits(x)` is exactly the seam between the two: S may never render a cell of T crisper than its log of observations licenses. That single split makes all four sub-questions answerable, and it is published cover, not metaphor: Grinbaum's operational eternalism (arXiv:2512.22879) is eternalism applied to INFORMATION not geometry -- which is precisely S, not T.

---

## 1. The block as a static N-D coordinate object keyholes write into (the agnostic FRAME)

### 1.1 What the block IS

The substrate is a static N-D mathematical coordinate object. Its axes are:

- the shared **base poset P** of path-IDs (the nesting coordinate from the UNITS doc: integer rung ladder for range + near-origin float for resolution; power-of-2 radix so `LCA = clz(a XOR b)/b` in O(1)),
- two fibrations over P -- **physical** (octree, 3 bits/level, decoder-free metres) and **latent** (radix-2, 1 auditable conditional bit/level), per UNITS Q2,
- the **six fact-axes** WHAT / WHEN / WHERE / WHO / HOW / WHY (v0.3), plus observer WHOM and BEFORE/AFTER typed edges,
- the **two clocks** the existing compiler already carries: `when` = `t_event` (when it happened in T) and `retrieved_at` = `t_obs` (when the system learned it). These are the two time-axes of an eternalist block; the compiler stores them but has not yet named them as such.

A **CELL** is addressed by `(path-ID, six-axis key)`. The block assigns to each cell a value -- but critically, the value is not a fact, it is a *measurement summary*. The block is a **sheaf**: to each cell it assigns a lattice element

```
L(cell) = ( measured_bits      : max-lattice,        # the COIN cap, from UNITS Q1
            fidelity-tau curve  : the structure-function h_x(alpha),
            provenance-set      : union-lattice,      # every contributing log event
            conjecture-flag     : bool )              # true => this cell is a STUB
```

`measured_bits` is exactly the UNITS-Q1 unit: the prequential/KT-gated codelength a pinned coder pays to losslessly reproduce the cell's content to fidelity tau, hard-capped at the entropy-coded literal. As a **max-lattice** it can only ever rise -- so "meaning -> knowledge as the block compiles" is a monotone climb, and `rendered_bits <= measured_bits` is a structural INVARIANT, not a hope.

### 1.2 Why "agnostic FRAME" is structural, not aspirational

The block is observer-NEUTRAL because the log stores only operationally-primary input/output events plus their `measured_bits` caps -- **never a decoded interpretation**. The decoder/observer (the GLASSES) is a separate read-side functor `G_obs : Block -> RenderedView` that picks decoder, frame, and LOD budget. Different glasses render the IDENTICAL block differently; the block references no observer. This is FRAME(agnostic substrate) = the sheaf S; GLASSES(observer) = `G_obs`. Coder-relativity (UNITS 1.8) therefore lives entirely in `G_obs`, not in the substrate -- which is why pinning/disclosing the coder is a render-side discipline.

> [SPEC] The strong form: under Grinbaum operational eternalism, observers are SECONDARY constructs that arise from groupings of the log's data. If so, the WHOM axis is not privileged input but **compiled output** -- a stub the block fills in retroactively. This would invert the usual frame/glasses split (the observer becomes a thing the block reconstructs). Out-of-box; flagged for a dedicated seat, not load-bearing here.

### 1.3 The keyhole WRITE

A keyhole observation = a **Z-set delta** (DBSP): `+1` assert / `-1` retract, weight-carrying so the log stays append-only even for corrections. One write =

```
{ target cell(s), six-axis coords, payload value, per-axis measured_bits,
  observer WHOM, BEFORE/AFTER typed edges, coder-id, t_event, t_obs }
```

The block is the **integral** `S = I(log)`. The existing `compile_substrate.py` realizes this literally: `substrate.db` is rebuilt from the JSONL logs every run, never committed; `compiled/*.json` is the snapshot. It IS an event-sourced materialized view already; it just is not yet *named* as the integral of a delta-stream.

### 1.4 Fuzzy + conjecture-stub = the lattice bottom

The lattice BOTTOM is a typed STUB (`measured_bits = 0`, `conjecture-flag = true`). Where no write touches a cell, the sheaf IS the bottom element. Crucially this must be a **typed null** -- structurally distinct from "a wrapper measured value ~ 0". The decisive render property: zoom into a fact yields detail; zoom into a stub yields bounded empty space (negative-space outline), never a faint point. A stub must carry its own falsifier, or it is a prior masquerading as a conjecture. Conjectures can only ever SHARPEN a stub (raise it off bottom), never un-sharpen -- monotone.

---

## 2. Compile = monotone fidelity accretion from the append-only fact-log

### 2.1 The compile equation

```
S_tau = C(L_tau) = I(L_tau)
```

`L_tau` = the append-only fact-log up to compiler-time tau; `C` = compile = the integral of the Z-set delta-stream (DBSP, Budiu et al., VLDB'23 best paper). The block is a derived, ephemeral, fully-rebuildable materialized view (Azure/AWS event-sourcing). The honest semantics: the system **never writes the unknown referent** `B*` (the true cell of T). It appends measurements `y_i = M_i(B*) + noise` and compile solves

```
S_tau = argmin_B [ sum_i loss(M_i(B), y_i) + prior(B) ]
```

A 2026 observation that sharpens an 1865 latent state does NOT change 1865; it moves `S_tau`, not `B*`. Any bit in S traceable to the `prior(B)` term rather than to a `y_i` is a candidate fake bit and must render on the ESTIMATE channel, never MEASURED. (This "a fact is a MEASUREMENT, not a fact" framing is the codex-keyhole take, and it is correct.)

### 2.2 The merge must be a join-semilattice (the law behind "monotone AND idempotent")

Accretion is a MERGE that is **associative + commutative + idempotent** (the CALM theorem; "Keep CALM and CRDT On"):

- **idempotent** -- `C(L) = C(L join L)`: replaying the same facts yields the same block. This is the existing task-15 "re-check = 0" raised to a LAW, plus free dedup of replayed events.
- **commutative** -- keyhole bursts fire in ANY temporal order and converge. This is precisely Pav's tomographic / multi-exposure model: bursts across time sharpen one shape regardless of arrival order.
- **associative** -- compile log segments in parallel and fold (stream-program-as-monoid-homomorphism, arXiv:2507.10799). License to shard the compile.

By CALM, monotone => coordination-free convergence to ONE block regardless of who compiled it or in what order. That is *why* the block is observer-neutral: it is a coordination-free fixpoint of the log.

### 2.3 Bits accrete, but evidence is not addition

The carrier is `(measured_bits, max)`. But independent observations add information; dependent ones do not (ten newspapers copying one wire = one projection with ten echoes). So when fact `f_j` lands in group g:

```
Delta            = independent_bits(f_j | f_1..f_{j-1})        # info conditional on prior facts,
                                                                # discounted by source overlap
measured_bits(g) = min( measured_bits(g) + Delta,
                        coin_cap, model_capacity_cap, provenance_cap )
```

At the cap, `Delta` clamps to 0 -- more corroboration is informationally free. This is the discrete form of Bayesian/GP-tomography posterior variance that monotonically tightens with exposures; that closed-form per-cell variance IS the estimator for `sigma = 2^-measured_bits`, the blur honesty badge with a real number behind it.

### 2.4 The chain rule = "compile per-axis, then compose"

DBSP's incrementalization theorem + **chain rule** prove that incrementalizing each operator independently and composing is **bit-identical to from-scratch recompute**, with work proportional only to the change. Applied here: each of v0.3's six axes gets its own `measured_bits` lattice; compile each independently and compose. This is precisely the UNITS chain-rule COIN `anchor_bits + window_bits = path_bits` -- the SAME additivity claim, viewed as compilation. (Caveat in §4.4: on the latent fiber that additivity is only NEAR-exact.)

### 2.5 How the existing compiler generalizes (it is ~80% there)

`compile_substrate.py` already implements the event-sourced spine. Three precise reframes complete it:

1. **`resolve_best` (lines 259-307) is already a deterministic, commutative, idempotent join on a total order** -- the lexicographic `max()` over `(bucket, certainty, freshness, fact_id)` with the `_InvStr` stable tiebreak (lines 245-256). But it selects ONE winning fact's scalar certainty; it does NOT accumulate bits across corroborating facts. Generalize by SPLITTING two concerns: best-VALUE selection (the existing argmax, keep it) from FIDELITY (a new lattice fold over the group per §2.3).

2. **The verification bucket (`BUCKET_RANK`, line 53; `bucket_for`, lines 217-229) is NON-MONOTONE today** -- a later `disputed` verification demotes a value BELOW a bare `pending` one. That is a latest-wins/retract move; it breaks CALM order-freedom. Fix per CALM/DBSP: encode disputes as **negative-weight Z-set wrappers** (`+1` assert / `-1` retract) so the log stays append-only, and carry corroboration on a SEPARATE max-lattice channel rather than mutating the chosen value's rank. The compiler already RETAINS disputed alternatives (lines 276-288) -- it just must stop letting them REORDER the lattice. (This is a deliberate honesty choice in the current SPEC sec.6, so it is a real design fork, not a free bug-fix -- see §5.)

3. **Reframe scalar `certainty in [0,1]` as `measured_bits >= 0`**: `measured_bits = -log2(sigma)`. Then "compile" is monotonically raising bits toward the cap, and the contribution-share guard (line 175, "theory-DNA is an estimate, cap at 0.6") becomes a per-axis `coin_cap`.

### 2.6 When a recompile is a no-op (idempotence made operational)

Content-address each group's inputs (blake3 of contributing `fact_id`s + values + verifications -- the Salsa/rustc query-cache model). Recompute only groups whose input-hash changed (red/green change propagation).

- **Whole-block no-op**: `hash(L_tau) == hash(L_{tau-1})` -> identical block, zero work past the hash check.
- **Per-group no-op (the useful one)**: a group is a no-op if no new fact targets it, OR a new fact targets it but the group is already at `coin_cap` AND the new value does not move the lexicographic argmax. This is the COIN making recompile idempotent: at the cap, more corroboration changes nothing.

The current compiler gets the CONTENT no-op partly free (deterministic sort + stable tiebreak) but recomputes everything every run; the generalization adds memoization so unchanged groups are skipped.

---

## 3. The eternalism verdict

**Observation across time = accreting `measured_bits` about a static block, not changing it.** Stated precisely with the two-block split:

- **T (territory) is eternalist in the standard physics sense.** Facts coexist tenselessly; the past does not change. [SPEC]/weak-commitment note: the instrument does NOT strictly need full 4D eternalism for T -- it only needs T to be FIXED-ONCE-MEASURED (a frozen past to chart), which growing-block and presentist-with-records views also grant. Leading with full eternalism for T OVERCLAIMS; pin the weaker "crystallized past" commitment to stay falsifiable.
- **S (substrate) is eternalist in Grinbaum's operational sense** (arXiv:2512.22879): eternalism of INFORMATION. S's cells coexist as information; observers are secondary constructs the log's groupings crystallize. This is the load-bearing commitment.

The static-vs-growing tension is resolved by lifting Ellis & Rothman's **Crystallizing/Evolving Block Universe** (arXiv:0912.0808) one level: in CBU the TERRITORY past crystallizes as quantum indeterminacy reduces at the present boundary; in S the CHART crystallizes as `measured_bits` accumulates at the observation boundary. Same formal move (indefinite -> definite at a boundary), applied to information instead of geometry. Two explicit upgrades over CBU:

1. crystallize along **LATENT axes** too (not just spacetime), and
2. leave **FUZZY + typed CONJECTURE-STUB** where derivation fails, instead of freezing a value.

**Compiler progress = motion along an entropy/compiler-time gradient INSIDE the static block** (Ewing 2025, "passage as entropy-boundary structure of a static block"), never a moving spotlight. Each render carries `as_of_tau` -- "what did the system know as of compiler-time tau". No `as_of_tau`, no honesty: drop it and eternalism becomes the alibi for false completeness.

Two cognates make this hardware-real rather than philosophical:
- Cross-time correlations as ONE static object: Milekhin-Adamska-Preskill's **spacetime density matrix** (arXiv:2502.12240, run on ibm_sherbrooke), whose imaginary part flags causal influence -- a ready signature for our BEFORE/AFTER typed edges.
- Resolution-bounded-by-information as a working dictionary: Takayanagi's entanglement-entropy = area (arXiv:2506.06595) is `rendered_sharpness <= measured_bits` instantiated in physics.

### 3.1 The delayed-choice / retroactive-ORIGIN trap (and its resolution)

CBU invokes present observation actualizing which past crystallizes -- which SOUNDS like editing T. Resolution under the split: delayed-choice changes which definite value enters T at the quantum boundary (a territory event); our keyholes only change S. **We must NOT smuggle delayed-choice into S as a license to lower `measured_bits`** -- that breaks monotonicity and the CALM guarantee. Retroactive, definition-relative ORIGIN (the diachronic `D(t)` spike) is the sharp test case: it looks like editing the past, but it is really appending a NEW projection (a present-definition probe) that LIGHTS UP old cells. The underlying per-axis `measured_bits` of those cells never decreases; a new typed view is added. The append-only log makes "rewrite the past" structurally impossible -- you can only append, including appending a `-1` retraction (itself an event).

---

## 4. The honesty guards -- a compiled block must never look more complete than its observations

The COIN law upgrades from a render-time label to a **compile-time invariant** enforced at named seams. Each seam is a place where `S` could render crisper than `L` licenses -- a leaked fake measured bit.

### 4.1 Guard 1 -- typed null (completeness / silent-default leak)

Partition every cell as MEASURED (>=1 wrapper) or STUB (no wrapper, prior-only). Render invariant: `measured_bits(x) = 0  =>  x renders as bounded negative space, never a low-opacity point`. The deadliest leak is the silent default: answering a query about an un-probed coordinate with the model's prior in the same data slot a true measurement would occupy. The compiler MUST be able to answer "is this value measured or imputed?" for every cell; if it cannot, the architecture is leaking. The stub-as-lattice-bottom encoding must be the DEFAULT, not an opt-in -- a performance shortcut that treats `absent == prior` silently re-introduces the leak. (Open cost concern in §6: at ~618-bit path scale most cells are un-probed, so typed-null-by-default is a real storage question.)

### 4.2 Guard 2 -- bounded time-interpolation (presentism leak)

A 2026 probe of an 1825 latent state plus a 1900 probe must NOT let the compiler fill 1860 by sharp interpolation -- that is a fake bit at an event-time never measured. Keep the two clocks; forbid MAP-collapse between bracketing observations. Permit interpolation ONLY under a logged drift bound `|F(z,t2) - F(z,t1)| <= K|t2-t1|`, with `K` itself a declared, falsifiable wrapper. Rendered sharpness at an un-probed t is then capped by the WIDTH of the reachable set, which GROWS with distance from the nearest exposure -- blur grows in the gap, never a sharp average. "Smooth latent" without a logged K is an unmeasured assumption rendering as data.

### 4.3 Guard 3 -- aggregation cap (false determinism via averaging)

A PARENT cell may not render crisper than its measured children:

```
rendered_bits(parent) <= sum_children measured_bits - bits_discarded
```

`bits_discarded` MUST include a **spread-of-means** term, so a high-variance child set cannot aggregate to a sharp centroid (a broadcaster + audience averaged into one point is the canonical fake bit). Use `N_eff` (effective independent evidence), not raw count, so dependent sources do not inflate fidelity:

```
bits_region <= min( sum_i independent_bits_i, coin_cap, model_capacity_cap, provenance_cap )
```

### 4.4 Guard 4 -- provenance equivalence under incremental recompile

The materialized-view pattern gives the gold standard: "delete the view, replay the log; every rendered bit traces to a log event." Incremental recompile for speed (DBSP Z-sets, chain-rule) is safe ONLY for monotone merges. The hazard: any latest-wins / max-so-far / retract op can leave a retracted source's contribution baked into a cached aggregate, so a bit no live source supports still renders. The honesty test is concrete and assertable: after any incremental recompile, `maintained_provenance(bit) == from_scratch_provenance(bit)` on a sampled set -- any mismatch is a leaked bit. (Fresh anchor: IMP, Li & Glavic, EDBT 2026, arXiv:2505.20683, gives the first incremental-equals-recomputed lineage theorem; open question whether it covers OUR aggregators -- §6.)

### 4.5 Guard 5 [SPEC] -- latent gauge-strip (the new one)

Latent axes are identified only up to an orthogonal transform (`P = XX^T` invariant under `X -> XQ`, `Q in O(d)`). When the compiler reconstructs latent MOTION across tomographic exposures taken in different embedding frames, the per-exposure gauge choice injects a SKEW-symmetric component into inferred latent velocity that is pure coordinate artifact -- it renders as a construct "moving / sharpening" with zero measured support. This is the latent twin of presentism. Detector (arXiv:2603.05703, Mar 2026): decompose `V_hat = (X^{t+1} - X^t)/dt`; `X^T V_hat` symmetric = real latent dynamics, skew-symmetric excess = gauge contamination. Operationally: Procrustes-align exposures and STRIP the skew part before claiming the construct moved. Publishable scalar: `skew/(skew+sym)` velocity ratio of the honest renderer vs the naive one. This is currently the STRONGEST candidate for a render decision the entropy arrow alone does NOT make (see §5).

### 4.6 The single fidelity law that binds the guards

Each burst `y_i = P_i F + eta_i` (Radon/CT; Fourier-slice: each projection fills one slice of k-space). Fidelity grows with **frequency-space coverage weighted by source independence**, not burst count. Limited-angle gaps MUST render as honest low-pass blur (explicit bandpass mask), never as compressed-sensing streaks (textbook fake high-frequency bits). Reconstruction "locks" only when `KL(S_{tau+1} || S_tau) < eps` AND `measured_bits >= disclosed_threshold` AND no high-impact alternative within delta evidence.

---

## 5. The pre-registered falsifier (the thing that earns the COIN its keep)

The whole edifice has ONE honest falsifier, and it must be pre-registered before building:

> If `measured_bits` / derivation-entropy minimization (the COIN gate; Xu & Li "Derivation Entropy", arXiv:2511.19156, is the quantitative name for retrieve-vs-generate) predicts the SAME crystallization order -- which cells sharpen when -- as a pure entropy-boundary account (Ewing 2025), then the COIN gate adds NO observable structure beyond the arrow of time. The block-of-information reduces to bookkeeping on top of the block-of-geometry, and "static substrate that compiles" reduces to the trivially-true "we learn the past in entropy order."

The instrument must exhibit at least ONE render/crystallization decision the entropy arrow alone does not predict. Candidates, in order of current strength:

1. **The gauge-strip (Guard 5):** a latent-motion render the entropy arrow does not make (it has no notion of O(d) gauge). Leading candidate, but unproven.
2. **Keyhole-priority over a quiet-but-pivotal cell:** a low-physical-entropy-flux region of T that is latently HIGH-bit (a quiet bureaucratic record that later proves pivotal). The entropy arrow says "nothing happening, sharpen later"; the spreading-activation probe (a present concept-light) says "sharpen NOW". If S sharpens it before the arrow would, the COIN adds real structure.

The settling experiment is the **latent gauge-tomography honesty harness**: a synthetic hidden block `F*(z,t)` with built-in concept-drift, each exposure in a randomly-rotated gauge frame, bursts limited-angle and partly copied. Three renderers -- A (naive: MAP, interpolates, raw-count, no gauge align), B (COIN-capped), C (COIN + typed stubs + Procrustes gauge-strip + active learning). Pre-registered success for C: reconstructs the true symmetric drift with fewer probes; marks gaps as stubs that BOUND the truth; reports near-zero skew velocity while A reports large fake "motion"; aims probes at highest-EIG stubs. If C's decisions are reproducible by a plain probabilistic graph + standard UQ + a Procrustes step, the block is a pretty metaphor; it earns "real machinery" iff it makes >=1 honest render call (a stub where A shows a fact; a gauge-strip where A shows motion; a blur where A shows a sharp centroid) the baseline does not.

---

## 6. SPECULATION (disclosed)

> Register shift: conjectures, not load-bearing claims. Each marked [SPEC].

- **[SPEC] The two fibrations are literally one code.** If a single pinned coder over a joint token stream (splat-tokens + concept-tokens) can measure both physical and latent prequential codelengths (UNITS 476-486), the cross-half COIN becomes an IDENTITY, not an analogy, and there is ONE sheaf with two sections rather than two sheaves glued at the coupling seam. A small joint-stream NLL experiment decides it.
- **[SPEC] The observer (WHOM) is compiled output, not input.** Under operational eternalism, "who observed" is a derived, retroactively-assignable grouping of the log -- a stub the block fills in. This inverts the frame/glasses split and would make `G_obs` itself partly a thing S reconstructs.
- **[SPEC] `k*` is a measurable latent Planck constant.** If the structure-function kink (AMSS) is stable across coders, the "smallest meaningful semantic quantum" is a real constant of the latent medium, and the fine-end peg of the sharpness normaliser is principled rather than conventional.
- **[SPEC] The spacetime-density-matrix imaginary part is computable on OUR log.** If so, BEFORE/AFTER edges get a MEASURED direction (causal influence), not merely an asserted one -- the typed temporal edges become derived. If only a physics cognate, they stay asserted.
- **[SPEC] Snapshot/compaction preserves the lattice exactly.** Log compaction folds redundant events to bound replay cost. Open whether it preserves the `N_eff` independence structure needed to bound bits, or whether folding silently re-inflates fidelity. If compaction loses independence structure, snapshots are not lattice-faithful.

---

## 7. QUESTIONS WE SHOULD BE ASKING

> Register shift: meta-level framing questions about the substrate programme, not tasks with known answers.

- **Are we building a viewer of civilisation, or of one coder's MODEL of civilisation?** On the physical fiber metres are coder-free, so `2^-bits` is near a world-property. On the latent fiber it is irreducibly a coder-property (UNITS 1.8). If the latent substrate is constitutively second-order -- a block of one coder's model -- then the pinned coder is not a nuisance parameter but the SUBJECT, and cross-model agreement is the whole game, not a calibration detail.
- **Does the chain rule actually hold on the latent fiber, or only nearly?** The "compile per-axis then compose is bit-identical" guarantee imports a DBSP theorem onto an assumption (exact conditional-codelength additivity) the latent fiber may not satisfy -- MRL prefixes are only near-monotone, and shared-ancestor double-counting threatens additivity. The right question is not "is it additive?" but "what is the MEASURED additivity defect, in bits, on a real corpus, and is it below one rung?" If not, the COIN is APPROXIMATE on the latent half and we should say so in bits.
- **Is concept drift gauge or content?** The gauge-strip (Guard 5) assumes a fixed latent metric across exposures. But genuine semantic drift can ROTATE the axes themselves (democracy-1800 vs democracy-2000). Then a real change masquerades as gauge and gets stripped -- fake-bit PREVENTION becomes real-bit DELETION, exactly where the most interesting contested constructs live. May be undecidable from the network alone without an explicit logged metric-drift wrapper.
- **Do per-observer keyholes converge to ONE block or to incompatible blocks?** Fragmentalism licenses observer-relative slices of S, but CALM convergence needs a single join-lattice. Is `sup_observers rendered <= measured` (the per-observer audit) sufficient as a theorem, or only a hope? One block, many charts -- or genuinely many blocks?
- **Should retraction be a first-class block op, or banned in favour of pure-monotone negative-weight wrappers?** Differential dataflow handles retractions and recursive BEFORE/AFTER queries natively (good for spreading-activation probes), but any in-place retract is non-monotone and forfeits free CALM convergence. Expressiveness vs guaranteed order-free correctness -- a genuine architecture fork.
- **Is the verification-bucket non-monotonicity a bug or a value?** SPEC sec.6's "disputed demoted below pending" is a deliberate honesty choice that VIOLATES order-free convergence. Either accept a coordination cost at that one point, or move disputes off the value-lattice onto a separate channel. Not a free lunch -- pick deliberately.

---

## 8. Open sub-questions for Pav

1. **Two blocks or one?** Ratify the T/S split as canonical (territory-block fixed; substrate-block = compiled chart that grows). This is the move that makes eternalism answerable -- needs your sign-off as the framing, because everything downstream assumes it.
2. **Verification-bucket fork:** keep SPEC sec.6's honesty-first "disputed demoted below pending" (accept a coordination point + flag it) OR move disputes to a separate max-lattice channel so the merge stays fully CALM-monotone? I lean toward the separate channel (it preserves both honesty and order-freedom), but it changes the compiler's selection contract.
3. **Typed-null default at scale:** at ~618-bit path width most cells are un-probed. Is stub-as-lattice-bottom affordable as the DEFAULT encoding, or do we need a sparse "absence is the default, presence is logged" representation that still answers "measured or imputed?" per cell without materializing every null?
4. **Which one render decision earns the COIN its keep?** Pre-register the falsifier target before building: the gauge-strip (Guard 5) or the quiet-but-pivotal keyhole-priority case? I rank the gauge-strip first because it has a closed-form detector and a publishable scalar (`skew/(skew+sym)`).
5. **Retraction policy:** first-class differential-dataflow retract (expressive) vs append-only negative-weight wrappers (free CALM convergence)? This decides whether the compiler can ever do an in-place update.
6. **Discharge the latent additivity obligation** (carried from UNITS §2.6): approve a prefix-length-vs-NLL sweep on a real MRL model to measure the per-rung defect in bits. Until measured, "compile is bit-identical to from-scratch" rests on an assumption the latent fiber may not satisfy, and Guard 3/4 are only approximate on the latent half.

---

*Binds to: `D:\hyperspace_units\UNITS_latent_radix_ceiling.md` (measured_bits unit, radix, ceiling) and `D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate\compile_substrate.py` (the existing event-sourced compiler this analysis generalizes, not forks). Standing frame: exploratory INSTRUMENT not confirmatory test (0.99-not-Boolean); claims demoted not killed.*
