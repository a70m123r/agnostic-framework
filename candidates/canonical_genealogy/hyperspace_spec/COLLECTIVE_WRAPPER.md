# The Collective Wrapper — scaling the cost-functional from one solver to many (2026-06-17)

The cost-camera, lifted an octave: from a single observer to **collectives** (agent swarms, human teams,
firms, cities, markets). From the `collective-cost-wrapper` workflow (6 regime cartographers deep-reading
2026 papers → synthesizer → skeptic; 8 agents, fresh WebFetch). Companion to [BIG_MAP.md](BIG_MAP.md).
Cite-don't-claim, demote-not-kill. The skeptic's breaks are kept inline, not buried.

## The unified frame — one new axis
A collective is a **team-shaped observer**, and its cost-functional is the single-observer one **plus
exactly one new term** that a single head never pays:

> **Cost(N) = Σ Workᵢ + Span(DAG) + C(N)**

- **Work** (V4) — total op-count. *Super-additive*: parallelism never reduces work, it redistributes it
  and **adds** a coordination-work term. This is why the **economic flip (cost > gain) arrives before the
  latency flip** — cost-as-work always rises with N.
- **Span** (V5) — the serial critical path. Untouched by N.
- **C(N)** — **coordination**, the new axis, born only when observers must agree.

All six regimes are *the same functional in different dialects*: Amdahl/Brent (silicon), Coase/Williamson
(firms), Dunbar/Brooks (human cognition), multi-agent-LLM-2026 (swarms), Bettencourt–West (cities),
Hayek/stigmergy (markets). The rung is always: **the N where dC/dN overtakes the marginal return of solver
#(N+1).** Because C rides ~O(N²) while useful work is at best linear, **a finite optimum N\* always
exists** (for a fixed problem + naive topology).

The augmented Amdahl that generates every rung: **S(N) = 1 / ( f + (1−f)/N + C(N) )**, non-monotone for
C(N)=cN, peaking at **N\* ≈ √((1−f)/c)** then declining. *Brooks's Law is literally this curve;* the
n(n−1)/2 channel count is the O(N²) term.

## The ladder of rungs (where the numbers flip)
| scale | the rung | flips when | tech that dissolves it |
|---|---|---|---|
| **1** | none — the camera lives here; DEEP>WIDE is the seed | n/a | long context |
| **2–4** | **the sharpest rung** — dense-serial flips at N=2; mixed/serial goes **net-negative past 3–4 agents** ([2603.12229](https://arxiv.org/abs/2603.12229): decentralized teams <1.5× or negative; 5-agent serial = 0.76–1.18×) | dC/dN > marginal return | star/orchestrator topology (O(N) not O(N²)) |
| **5–15** | span-of-control — one coordinator's attention is scarce | O(N) reports saturate one supervisor | forms/telegraph/dashboards |
| **~150** | **Dunbar** — O(N²) mutual monitoring exceeds the next layer's cost | trust-memory limit | **externalize memory** (writing) → forces a hierarchy layer |
| **10³–10⁶** | market / network / city — direct coordination impossible | *(a city never flips from coordination collapse — it's super-linear)* | **compress the signal** (price = one scalar; Hayek) |
| **10⁴+** | swarm / society | coordinated-channel regime died long before | **statistical emergence**, not channels |

The headline empirical fact: in 2026, **a single agent given the same total compute often matches or beats
the swarm** — coordination (58–285% token tax) eats the parallelism. **Brooks reborn for agents** (MAST
taxonomy, NeurIPS 2025: failures are coordination/verification, not capability).

## The dissolution dynamic — every coordination technology attacks one term
Of S(N) = 1/(f + (1−f)/N + C(N)):
- **(A) lower c** — topology O(N²)→O(N log N)/O(N): the org chart, the M-form division, orchestrator-worker, MPI tree-reductions.
- **(B) compress communication** — fewer bits/message: **price compresses "all the reasons tin is scarce" to one scalar** (Hayek); jargon/APIs/schemas; CRDT conflict-free merges; latent-channel / KV-cache handoff below natural-language cost.
- **(C) externalize memory** — move serial state out of the critical path: the **blackboard / shared store / version-controlled artifact = stigmergy** (the ant's pheromone field); converts O(N²) pairwise sync into O(N) reads/writes.
- **(D) reduce f itself** — the *only* move that lifts the Amdahl **ceiling** (not just the knee): decompose the serial dependency, or — the optimistic escape — **grow the problem** (Gustafson) so the parallel part outpaces f.

## The kernel-canon history — the kernel *breathes* with c/f
Your "kernel canon" at the organizational octave: the canonical *unit* of organization is **frame-relative
to the coordination substrate.** Cut c (cheaper coordination) → the kernel **grows**, absorbing the prior
kernel as a wrapped sub-unit. Let the serial span reassert (power wall, the *novelty bottleneck*
[2603.27438](https://arxiv.org/abs/2603.27438)) → it **shrinks** back to the smallest self-contained loop.
- **pre-1840** — kernel = **individual / household / artisan**; direct reciprocity; almost everything is "market." *(Bio floor: the ant colony, coordinating by pheromone — stigmergy before economics.)*
- **post-language** — kernel = the **~150 community** (clan, Roman century, the "natural company"); language + social memory; bounded by neocortex O(N²) monitoring (Dunbar).
- **1840–1920** — kernel = the **integrated managerial firm** (Chandler's *Visible Hand*): double-entry + **railroad + telegraph** made administrative coordination beat market coordination — the visible hand replaces the invisible one.
- **20th c.** — the **M-form / multidivisional** (a kernel of kernels); telephone + computer.
- **internet era** — swings *back* toward **market / network / platform** (Malone): IT drops c so far the market beats the hierarchy again.
- **2026** — the **agent swarm** — and the open question of whether the firm boundary dissolves entirely or just relocates to context + verification.

## The two floors that never dissolve (the deep landing)
After every coordination technology has done its best, **two floors remain — and they are the same
conservation law with two faces:**

1. **The span floor (latency face) — Brent/Amdahl.** T_N ≥ max(W/N, **D**). No coordination tech pushes
   completion below the **span D** (critical-path depth). f = D/W is the *conserved quantity* — tech moves
   *where* the knee sits, never removes the floor. **This is V5 made absolute:** the one rung that survives
   a civilization of perfect agents is the *problem's own serial path.* What we measured in one LLM is what
   ultimately bounds any number of them.

2. **The information floor (truth face) — the Data Processing Inequality.** I(output; task) ≤ I(input; task):
   **a handoff can only *lose* information about the truth, never create it.** Natural-language handoffs
   between agents are lossy by construction. **This is our render ≤ measured-bits honesty law, lifted to
   the collective** — and *the skeptic, primed to debunk, called it "the one genuinely new, genuinely
   robust claim" in the whole wrapper.* The blur is not optional at the seams; it compounds along the chain.

## What the skeptic broke (kept honest)
- **Lossy vs lossless is a *category* difference, not degree.** A parallel computer passes *exact* bits over
  coherent caches; it does **not** pay the DPI handoff tax. So **agent-swarms ≠ parallel computers** on the
  information axis — the analogy is strongest for work/span, weakest for C(N).
- **C(N)=O(N²) is a worst-case *topology*, not a law.** "A finite optimum always exists" assumes naive
  all-to-all; the regimes themselves dissolve it (star, blackboard).
- **C(N) conflates three different costs:** silicon (latency/bandwidth — physical, symmetric, lossless),
  human (trust/attention), agent (lossy NL tokens). Lumping them under one symbol is facile.
- **The "3–4 agent" number is harness-relative and already dated** — a property of today's NL-token harness,
  not a constant.
- **Span (V5) and the serial fraction f are not yet *proven* the same object** across levels — asserted, not
  shown (and it ties to the open question below).

## Agents *invert* humans (the key disanalogy)
- **Cloning/forking is ~free for agents, impossible for humans.** This **inverts the binding constraint**:
  humans asked *"how many can I afford?"* → kernels **grew**; agents ask *"how many can I coordinate /
  verify?"* → kernels **shrink**. Today's optimum (3–4) is *smaller* than a human team's, not larger.
- **Forked agents are highly correlated** (shared weights) → ensembling/voting buys far less than the
  independent-human ideal; the redundancy discount bites earlier and steeper.
- **No Dunbar trust, but unbounded context** → the right human analogue for a swarm may **not be the
  firm/team at all, but the *single mind with externalized working memory.***

## Questions the wrapper opens (register-shift)
- What is the **information-theoretic floor** on the *self-inflicted* NL-handoff loss — and does a latent /
  KV-cache channel beat it?
- Is **forking (perfectly correlated agents) ever a *feature*** — speculative execution / branch prediction?
- When the **same model is orchestrator and worker** (self-consistency, tree-of-thought) vs different
  families — what does the camera read differently?
- Is **"coordination cost is conserved, only relocatable"** actually false — can a better algorithm
  *destroy* coordination cost rather than move it?
- **Where does the in-head V5 DEEP>WIDE surcharge come from** — the *task's* dependency (true Amdahl f) or
  the *model's* autoregressive generation? (The single deepest open question — it decides whether V5 is
  substrate-invariant.)

## The sharpest testable handle — the collective V5
**Measure the swarm's Amdahl-f and C(N) curvature directly with the cost-camera, by topology.** Run the
*same* task at matched per-agent compute across N = 1, 2, 3, 4, 6, 8, 12 under three fixed topologies
(**all-to-all mesh; star/orchestrator; blackboard/shared-store**), and fit
**Cost(N) = Σ Workᵢ + Span(N) + C(N).** Three pre-registered, falsifiable predictions:
1. C(N) is **linear** for blackboard, **linear** for star, **quadratic** (slope ∝ N−1) for all-to-all;
2. the mesh goes **net-negative** at the predicted N\* ≈ √((1−f)/c);
3. the asymptotic floor reads off the **collective serial fraction f** — V5 at the scale of a team.

It reuses our entire harness and would photograph Brooks's Law and Amdahl's ceiling in token-currency — the
same instrument, one octave up. ([2603.12229](https://arxiv.org/abs/2603.12229) already did the embryo of
this; the contribution is the *honesty-law framing + the topology-resolved C(N) + the DPI floor*.)

## One-line
Scaling a solver into a collective adds exactly **one** cost axis — coordination C(N) on an O(N²) curve
against at-best-linear work — so a finite optimum rung **always** exists (3–4 agents now, Dunbar's 150 for
humans, planetary for a price system); every coordination technology in history is the *same move* (cut c,
externalize memory, drown f) that **re-canonizes the kernel** (band→firm→M-form→network→platform→swarm) by
dissolving a costly wrapper-membrane into the next atom — but **two floors never dissolve: Brent's span
(you can't beat the critical path) and the Data Processing Inequality (a handoff can only lose the truth,
never make it) — which is our camera's honesty law, lifted to the collective.**

---

## The other side of the equation — BUILD (CAPEX, the eons) + MAINTAIN (OPEX, against decay)

*(Pav's completion — the per-use cost above is only the visible tip; underneath are two more terms with
different time-signatures.)* The full cost-functional has **three terms on three clocks:**

> **Total = USE(now)  +  MAINTAIN(continuous)  +  BUILD(amortized over eons)**
> = [Σ Workᵢ + Span + C(N)]  +  [standing dissipation to hold the structure against decay]  +  [the resource + compute frozen into the infrastructure]

- **BUILD = Bennett's logical depth** ([Bennett, *Logical Depth and Physical Complexity*](https://web.cs.ucdavis.edu/~doty/papers/LogicalDepthAndPhysicalComplexity.pdf)).
  Logical depth = the *running time to unfold a structure from its shortest description* — "decompression
  time," not "compression length." It is **literally the eons of build-cost**, and it has a theorem attached:
  the **Slow-Growth Law** — *logical depth cannot increase quickly; organized structure (biological,
  cultural, technological) can only be accumulated over time, never fast-forwarded.* That is why "the cost
  paid over the eons" is irreducible: depth ≠ description; you cannot shortcut the build. (Note: random AND
  trivial objects both have *low* depth — only *organized* structure is deep. The infrastructure is the deep
  thing.)
- **MAINTAIN = the rent against the second law.** A low-entropy structure (a brain, a firm, a trained model)
  decays without continuous energy input; maintenance is the standing dissipation that holds it. In biology
  this is metabolism: the body's maintenance scales *sublinearly* (Kleiber M^¾ — the same economy-of-scale
  as Bettencourt's β≈0.83 infrastructure), but **the brain scales *linearly*** (fixed energy budget *per
  neuron*; 2% of human mass, 20% of its energy) — the expensive organ is the one that computes. ([COCO,
  bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.06.18.660368v2.full): the energy cost of
  non-equilibrium computation.)
- **USE = what the camera measures** (V4 work, V5 span, C(N) coordination) — the *marginal* present cost.

**The amortization principle, exactly.** Your *"easy = pre-paid"* is this: the **USE cost is low because the
BUILD cost was paid.** A problem reads as "low-entropy / easy" precisely when its difficulty was **amortized
into the infrastructure** — the trained weights, the evolved circuits, the institutional routines. In COIN
terms, the build cost *is* the pre-rendered `measured_bits`; cheap inference is just **replay** of a structure
whose sharpness was bought, once, slowly. Difficulty is conserved — it was shifted into the deep clock.

**The substrate sets which term dominates — and it can flip.**
- *Biology:* BUILD ≫ everything — ~hundreds of My of selection vs ~20 W of present metabolism. The eons dwarf
  the use.
- *A frontier LLM:* the flip. **Inference (maintain+use) is ~80–90% of lifetime compute, training (build)
  only ~10–20%** ([Stanford HAI; AI training-vs-inference economics](https://telnyx.com/resources/ai-training-vs-inference)):
  GPT-4 training ≈ $100M one-time vs ChatGPT inference ≈ $700k/**day**. For a heavily-used model the **OPEX
  exceeds the CAPEX** — the opposite of biology. (And the 280× inference-cost drop 2022→2024 = the maintenance
  term falling fast.)

**This closes the kernel-canon loop.** A kernel *crystallizes* when its BUILD cost has been amortized enough
that its USE cost drops below the coordination cost of re-assembling it from parts (the firm, the model, the
institution = a frozen amortized structure). It *persists* while MAINTAIN < the value of the USE it enables.
It *dissolves* when maintenance exceeds that value (decay, obsolescence, a cheaper substrate) — the kernel
breathes on the **(build-amortization) / (maintenance-rent)** ratio, not just on c/f. And the optimistic city
(super-linear β≈1.15 output on sublinear β≈0.83 infrastructure) is exactly **a cheap marginal USE riding on a
heavily-amortized BUILD** — scale pays when the eons subsidize the present.

**The open instrument question this raises:** our cost-camera currently photographs only the USE term (marginal
reasoning_tokens). Can it be made to read the **amortized** terms — e.g., a *prequential / MDL* read where the
"easy" present cost is scored against the build that pre-paid it (Bennett depth as the hidden axis behind V4's
work-slope)? That is the camera pointed *backward in time* — measuring not what a digestion costs now, but what
was paid to make it cheap.
