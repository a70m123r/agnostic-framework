# Specimen — Connectionism + continuous optimization → Deep learning (the connectionist program vindicated)

> **THE MULTI-CYCLE DORMANCY-REVIVAL + INSTITUTIONAL-ACTOR + COMPUTE/FUNDING/FASHION-FORCING CASE.** A ~70-year weld that twice went dormant (the AI winters) and twice revived *reinterpreted*, finally **consummating at 2012 (AlexNet)** when two non-idea **instrument-parents** (GPU compute, ImageNet data) arrived. It is the v2 calibration instrument built to hammer all five new dimensions — **D1** (a double-dormancy graded lifecycle), **D2** (DARPA / CIFAR / NVIDIA / Google / OpenAI as first-class actors), **D3** (a physical layer that drives the latent one), **D4** (AI-winter squeezes vs compute/data/hype pulls), **D5** (deliberately soft dormancy edges).
>
> **Status:** Tier-3 WORKING specimen — exploratory data-harvest, surfaced for **Cowork+Pav ratification**. NOT canon, NOT a tier promotion, does **not** grow the convergence list (stays **9**). A worked example / calibration instrument extending `wrapper_classes_phase1.json` at deeper *historical* zoom — **NOT a 10th convergence.** All confidences are SOFT scores in [0,1]; bits are qualitative only.
> **specimen_id:** `deep-learning` · **generated:** 2026-06-09 · **schema:** `../SCHEMA_v2.md` (v2) · **overall_confidence:** **0.86** (split — HIGH on the child/consummation, FRONTIER on the dormancy-narrative + credit) · **frames:** {time, space, knowledge, meaning} · **layers:** {physical, latent}
> **JSON:** `deep_learning.json` (same dir) · **Extends:** `../latent_olympics_data/wrapper_classes_phase1.json` (#6 model merging / #7 Allen-Cahn message passing / #9 BES are present-edge **descendants** of this child)

---

## TL;DR — why this specimen matters

Where QG is the *unconsummated* frontier (a hollow trunk), this is a **consummated weld with a contested historiography**: the child is real, dominant, hegemonic — but it took **two winters and ~70 years**, and the record fights over *how dormant it really was* (Haigh) and *who produced it* (Schmidhuber). The certain core is **most of the tree** (parents, seam, mediating weld, **child**, consummation, actors, harvest); the frontier is two *lateral* pockets that never touch the trunk — the **winter narrative** and the **credit dispute**.

Its job is to **exercise the v2 machinery at full stretch**: it is the batch's strongest case for **D2** (a *foundation*, CIFAR, literally carried the latent wrapper through a winter; a *government agency*, DARPA, was the chief squeeze; a *company*, NVIDIA, supplied the gating instrument) and **D4** (a "weather" layer of 13 pull/squeeze events), and the cleanest **instrument-enabled-weld** in the set (the idea-weld existed in 1986/1989 but did not *fire* until the apparatus arrived in 2012).

---

## The merge event (the weld)

|  | |
|---|---|
| **W_A** (content) | **Connectionist substrate** — artificial neural networks (adjustable-weight nets). Brain-inspired distributed computation. Lineage: McCulloch-Pitts (1943) → Hebb (1949) → **Rosenblatt perceptron (1958)** → Fukushima Neocognitron (1980). Frame {knowledge, space}. **conf 0.95.** |
| **W_B** (method) | **Continuous optimization / differentiable calculus** — minimize a differentiable objective by gradient descent via the chain rule. Lineage: Ivakhnenko-Lapa GMDH (1965) → **Linnainmaa reverse-mode autodiff (1970)** → Werbos (1974, applied to nets). Frame {knowledge, space}. **conf 0.90.** |
| **Mediating welder** (R1) | **Backprop-as-neural-training + the PDP connectionist framing** (Rumelhart-Hinton-Williams **1986**; + Hopfield 1982 / Boltzmann machine 1985 as the physics-respectability sub-weld). The agent that *performed* the weld — not an ancestral parent but a layer up; recognized that **"neuron weights" and "the variables you differentiate" are the SAME object.** The Darwin+Mendel *population-genetics* analogue. **conf 0.92.** |
| **+2 instrument-parents** (R4, at consummation) | **GPU/CUDA compute** (NVIDIA CUDA 2007; AlexNet trained on two GTX 580s) and **ImageNet data** (Fei-Fei Li 2009; 14M images via Mechanical Turk). The honest parent set is **~5 typed parents** (2 ancestral content/method + 1 mediating welder + 2 gating instruments); the binary {substrate × calculus} is a defensible but **lossy 2-projection** (see Discrepancy 1). |
| **Seam S** | **The differentiable parameterized FUNCTION trained to minimize error** — a neural net *is* a composed differentiable function whose weights live in a continuous space gradient descent can search; **backprop is the chain rule recognizing that identity.** Largely **agreed** (contrast Darwin+Mendel's fractured S). At the 2012 consummation S **widens** to a three-way seam: algorithm + **data manifold** (ImageNet) + **compute substrate** (GPU SIMD ↔ the matrix-multiply structure of layers) coincide. |
| **weld_operator** (R13) | **The GRADIENT** — the d(loss)/d(weights) backward flow. Like Maxwell's d/dt displacement-current term, the weld is welded **BY** a specific operator, not merely *in* a frame. Static W_A + W_B (an untrainable net; a calculus with nothing to optimize) make nothing; the gradient is the active ingredient. |
| **When** (R2) | A **process**, not a date: substrate root 1943; perceptron 1958; **idea-weld 1986** (backprop); **surprise demonstrated 1989** (LeNet); **consummation 2012** (AlexNet); hegemony 2017+ (transformers). The defining fact: the idea-weld and the *firing* are ~26 years apart because the instruments were rate-limiting. |
| **lod_scale** (R3) | **Confirms under zoom** (contrast QG). Zooming in reveals an ordered build-chain of sub-welds — perceptron → Minsky-Papert squeeze → backprop → CNN/LeNet → AlexNet's three-element fire → transformers — each *building on* the last, the signature of a healthy weld. The only twist: two **dormancy gaps** in the chain. `coherence_under_zoom: confirms`. |

### The surprise (synergy) — **conf 0.90**

Neither parent predicts alone that **stacking many layers** of the simple connectionist unit and training the whole stack by gradient descent yields **emergent, hierarchical, distributed representations that automatically discover features** — a single general architecture beating decades of hand-engineered, domain-specific, symbolic solutions across vision, speech, language, and games.

- The **neural substrate alone** (perceptron) is a shallow classifier that *provably cannot do XOR* (Minsky-Papert 1969).
- The **optimization calculus alone** is just curve-fitting.
- Only **jointly** — deep differentiable net + backprop gradient flow + (at consummation) enough compute and data — does **representation learning** appear: the network learns *what* to represent, not just how to weight fixed features.

The **deepest surprise is a meaning-frame shift**: intelligence-as-explicit-symbol-manipulation (the rival paradigm's axiom) is displaced by **intelligence-as-emergent-statistical-structure-in-a-trained-function.** A **second-order surprise** sits on top: **scaling laws** (Kaplan 2020) — loss falls as a smooth power law in compute+data+params — so the child's capability is *predictable from scale*, a regularity neither parent nor even the 1986 welders anticipated.

> **Meta-surprise (the schema's lesson — the most extreme R9 case in the batch):** `surprise_confidence` was ~0.9 and the synergy was **DEMONSTRATED working** (LeNet on real handwritten digits, deployed reading **bank cheques**, 1989) **~23 years before** the child consolidated as the dominant paradigm (2012). A maximally fertile, *repeatedly-demonstrated* weld that stayed unborn-as-paradigm through **two winters** for want of the instrument-parents. The R9 decoupling here bites **in time** (both confidences are high; the gap is the ~23-year adoption lag). Synergy assessed qualitatively only; no bits fabricated.

### survived / dropped

**Survived:** the adjustable-weight unit (W_A) · gradient descent + the chain rule / backprop (W_B) · distributed sub-symbolic representation (vindicated) · **the differentiable composed function (the seam S itself)** · brain-inspiration as loose motivation.
**Dropped:** biological fidelity (backprop is biologically implausible) · the single-layer perceptron's XOR limit (escaped by going *deep*) · **hand-engineered features / symbolic rules** (the rival's core — *displaced, not fused*) · unsupervised deep-belief-net pretraining (the 2006 revival trigger, later shed once labeled data + ReLU/dropout sufficed) · symbolic knowledge representation as the dominant approach.

*Feature-ledger (R7, light use):* the rival's "explicit hand-coded features / symbolic rules" is **dropped by mainstream deep learning** (fusion-by-displacement) and **kept only by neuro-symbolic hybrids** (minority descendants).

---

## D1 — the weld's graded life (the headline: a DOUBLE-dormancy lifecycle)

The richest multi-cycle trajectory in the batch (more cycles than Darwin+Mendel's pluralist→hardened→contested). Phase memberships are weights, not a second confidence.

```
pre_weld:ANTAGONISM (0.85, 1943-58)         connectionism vs symbolic AI as rival programs
  → conception/first_conjecture (0.90, 1958-65)   perceptron; deep-net conjecture latent (Ivakhnenko/Werbos)
  → DORMANCY #1 (0.80, 1969-86)             winter #1 (Minsky-Papert + funding capture)
  → revival:REINTERPRETED (0.85, 1986-95)   perceptron → multi-layer backprop net; LeNet demonstrates (1989)
  → DORMANCY #2 (0.70, 1995-2006)           'Hinton's dark ages' (SVM/kernel fashion); CIFAR carries the flame
  → revival:REINTERPRETED (0.80, 2006-12)   deep belief nets; object returns as DEEP; instruments catching up
  → welding/CONSUMMATION (0.95, 2012)       AlexNet — the three-element fire
  → hardening/HEGEMONY (0.95, 2017→)        transformers → LLMs/ChatGPT
```

**pre_weld_relationship = antagonism (0.85):** connectionism (cybernetics wing) vs symbolic AI (Dartmouth 1956); symbolic proponents "gained control of national funding conduits and ruthlessly defunded" neural-net research by the mid-1960s. *Note:* the fusion was largely **fusion-by-displacement** of the rival, not literal fusion.

**weld_type (weighted, D1):**

| type | weight | note |
|---|---|---|
| **instrument-enabled-weld** | **0.85** | **PRIMARY** — the idea-weld existed by 1986/1989 but only *fired* when GPU-compute + big-data arrived ~2012. The apparatus, not the idea, was rate-limiting. |
| **state/funding-mobilized-weld** | **0.90** | DARPA squeeze, CIFAR carry, NVIDIA instrument, Big-Tech harvest — institutions drive *every* phase. The strongest D2 case in the batch. |
| **mediator-welded** | 0.85 | backprop/PDP (not the ancestral parents) did the welding — the population-genetics analogue. |
| **re-weld / re-attribution** | 0.70 | each revival reinterprets the object (×3); canonical credit disputed (Schmidhuber vs the laureates). |
| **double-dormancy-revival-weld** | 0.90 | **PROPOSED NEW term** (multi-cycle dormancy) — proposed in Discrepancy 3 before use (§6 item 7). |
| antagonism-then-fusion | 0.60 | reduced weight: here it is fusion-by-*displacement* of the rival more than literal fusion. |

---

## D4 — the exogenous "weather" (squeeze vs pull events)

The batch's richest forcing layer: the AI winters as **squeezes**, the compute/data/hype as **pulls**, each acting *through* an actor (D2).

**SQUEEZES (the winters):**
- **Minsky-Papert "Perceptrons" (1969)** — *fashion* (+politics amplifier) / squeeze on the substrate (str 0.85): a rigorous XOR-impossibility critique amplified by MIT prestige, redirecting fashion+funding to symbolic AI → winter #1.
- **Symbolic-AI funding capture (mid-1960s)** — *politics* / squeeze (str 0.85): symbolic proponents captured national funding and "ruthlessly defunded" the cybernetics wing *before* Minsky-Papert formalized it.
- **Mansfield Amendment (1969) + DARPA mission-orientation** — *politics* / squeeze (acts through DARPA): forced near-term-payoff funding; 1974 CMU speech-understanding contract cancelled.
- **Lighthill Report (1973, UK)** — *politics* / squeeze: "complete dismantling of AI research in the UK" — but **mostly symbolic-AI**, weak on the neural-net weld (a framework-vs-record nuance).
- **Lisp-machine collapse (1987)** — *economic-crisis* / squeeze: cheap workstations erased a ~$500M industry (Symbolics bankrupt); **a squeeze on the RIVAL that cleared space for connectionism** (the anti-correlation).
- **DARPA "deep and brutal" cut (1987-89, Jack Schwarz)** — *funding* / squeeze: "surf waves, don't dog-paddle"; AI judged not the next wave.
- **Fifth Generation failure (1981-92, Japan MITI)** — *politics* / **both**: a $850M bet that *pulled* global AI funding then *squeezed* confidence when it ended "with a whimper."
- **Kernel-methods/SVM fashion wave (~1995-2006)** — *fashion* / squeeze on the child (str 0.75): SVMs had cleaner theory and beat nets on small data — the **"Hinton's dark ages"** (dormancy #2) driver.

**PULLS (the un-sticking):**
- **CIFAR program (2004+) + Canadian state** — *funding* / pull (acts through CIFAR/Hinton): deliberately funded and networked the marginalized connectionists *through* dormancy #2 — the institutional carrier that kept the wrapper alive until the instrument caught up.
- **NVIDIA CUDA / GPGPU (2007)** — *technology* / pull (str 0.90): made the matrix-multiply core orders of magnitude cheaper; the gaming-GPU market **accidentally supplied the apparatus that GATED the 2012 weld.**
- **Big-data / ImageNet + Mechanical Turk (2007-12)** — *technology* / pull: web + crowd-labor made 14M-image labeled sets feasible — the second gating instrument.
- **Post-2012 investment + hype boom** — *funding* / pull: $50B (2022) → projected $364B (2025); ChatGPT 100M users in 2 months — the mirror image of the earlier squeezes.
- **2018 Turing Award + 2024 Nobel Physics** — *cultural-focus* / pull: elite consecration that **canonized** the child — and itself triggered re-attribution disputes (a pull that doubles as a re-attribution event).

---

## D2 — actors as the physical↔latent bridge (20 nodes; individuals + lab + government + institution + company)

The genealogy is *unintelligible* without institutional/government/corporate actors. Each has **carrier_of** (champions a latent wrapper UP) and **inhabitant_of** (operates WITHIN). Selected:

| actor | kind | carrier_of (UP) | inhabitant_of (WITHIN) |
|---|---|---|---|
| **Rosenblatt** | individual | the perceptron / W_A | cybernetics milieu; ONR funding |
| **Minsky & Papert** | individual | symbolic AI / the case against perceptrons | the symbolic-AI paradigm; MIT AI Lab |
| **Rumelhart-McClelland / PDP group** | **lab** | the weld (backprop/PDP); deep learning | the 1980s anti-symbolic cognitive-science insurgency |
| **Hinton** | individual | deep learning (THE flame-keeper); the weld | CMU→Toronto→**CIFAR**→Google Brain |
| **LeCun** | individual | CNN/LeNet; deep learning | Bell Labs→NYU→Meta; **CIFAR** |
| **Bengio** | individual | deep learning / representation learning | Montreal/MILA; **CIFAR** |
| **Schmidhuber** | individual | the *originators'* priority (re-attribution) | inside deep learning, *outside* the Hinton-Bengio-LeCun cluster |
| **Ivakhnenko & Lapa** | individual | GMDH / first deep nets (1965) | Soviet cybernetics, Kyiv — *a politically-marginalized deep root (cf. QG's Bronstein)* |
| **Fei-Fei Li** | individual | ImageNet / the data instrument-parent | the computer-vision community |
| **Krizhevsky & Sutskever** | individual | AlexNet (the consummation) | Toronto (Hinton's lab) |
| **DARPA** | **government** | (historically) symbolic AI — and the **chief SQUEEZE** | US DoD; Cold-War funding apparatus; Mansfield-constrained |
| **CIFAR + Canadian govt** | **institution** | deep learning **through the dark ages** (carrier-through-dormancy) | Canadian federal research ecosystem |
| **NVIDIA** | **company** | CUDA / GPGPU (the **gating compute instrument**) | the gaming-GPU industry repurposed for compute |
| **Symbolics / LMI** | **company** | symbolic-AI hardware (rival's commercial arm — **collapsed 1987**) | the 1980s expert-systems boom |
| **Japan MITI / Fifth Gen** | **government** | logic-programming AI ($850M state bet — **failed 1992**) | 1980s techno-nationalism |
| **Google Brain** | **company** | transformers (2017); scaled DL | the post-2012 big-tech gold rush |
| **OpenAI** | **company** | GPT / scaling laws / ChatGPT | the post-2017 transformer ecosystem |

> **The bridge thesis in action:** the **latent** layer (connectionism → backprop → deep learning) is driven through its whole lifecycle by the **physical** layer (DARPA defunds; CIFAR funds-through-winter; NVIDIA/ImageNet supply instruments; Google/OpenAI harvest). CIFAR is the clearest *flame_keeper / dormancy_patron* in the batch — a foundation that deliberately funded a marginalized wrapper through its winter.

---

## Roots (DOWN — physical frame) & Harvest (UP — latent + cultural)

**Sub-wrappers (roots):** McCulloch-Pitts neuron (1943) · Hebbian learning (1949) · Neocognitron (1980, the CNN blueprint) · reverse-mode autodiff / chain rule (1970) · **GMDH (1965, the deepest disputed priority root)** · stochastic gradient / optimization (Amari 1967) · statistical-mechanics / spin-glass (the physics-respectability + 2024-Nobel root) · **CUDA/GPGPU (2007, compute-instrument root, PHYSICAL)** · **ImageNet + Mechanical Turk (2009, data-instrument root, PHYSICAL)**.

**Harvest (lush *and* over a full trunk):**
- **Transformer (2017, Google Brain) → BERT/GPT → GPT-3 → ChatGPT (2022)** — the dominant successor and consumer-facing consummation.
- **Scaling laws** (Kaplan 2020; Chinchilla 2022) — a descendant *theory about the child*.
- **GANs, diffusion, deep RL (AlphaGo/AlphaZero), self-supervised learning, AlphaFold** — the cross-domain cluster.
- **Model merging / BES (#6/#9) + Allen-Cahn message passing (#7)** — **direct descendants that link this specimen back into the Phase-1 DB at the present edge.**
- **Cultural:** the GPU/accelerator industry (NVIDIA's trillion-dollar pivot); the AI-investment boom; the data-labeling gig economy · the AI-safety/ethics + x-risk discourse (Hinton quit Google 2023 to warn); algorithmic-bias/copyright/labor debates · AI-generated art, deepfakes · the consecration harvest (2018 Turing, 2024 Nobel) · the **dark child**: surveillance/facial-recognition + generative-AI misinformation (the deep-learning analogue of Darwin+Mendel's eugenics dark child).

**Relatives (WIDE):** **symbolic AI / GOFAI (rival** — displaced, not fused; *its winter was connectionism's spring*) · cybernetics (influence) · model merging / Allen-Cahn message passing (Phase-1 cousins) · computational neuroscience / Hubel-Wiesel (sibling).

---

## CERTAIN CORE vs FRONTIER (the explicit split)

**The fulcrum sits HIGH** — most of the tree is solid; the fuzz is two *lateral* pockets that never touch the trunk. (Contrast QG, where the core *sinks below* the child; and Darwin+Mendel, where fuzz *climbs into* the trunk at the parent-identity.)

### Certain core (high confidence)
- **The CHILD** — deep learning as a working, dominant paradigm (**0.95**); uncontested as the dominant AI paradigm of the 2010s-2020s.
- **W_A** the connectionist substrate (0.95) and **W_B** the optimization/calculus apparatus (0.90).
- **The 2012 AlexNet three-element convergence** (algorithm + GPU compute + ImageNet data) (**0.95**) — stated verbatim by Wikipedia *and* Fei-Fei Li.
- **The mediating welder** (backprop/PDP 1986: "weights = differentiable variables") (0.92).
- **The seam S** (a net IS a differentiable function trained by gradient descent) — agreed, not fractured (0.90).
- **The surprise was DEMONSTRATED working** (LeNet 1989) (0.90).
- The **instrument-parents** (CUDA 2007; ImageNet 2009) and their gating role (0.88).
- The **institutional actors** driving every phase (DARPA / CIFAR / NVIDIA / Google / OpenAI) (0.85-0.90).
- The **forcing events as a class** (0.80-0.90); the **harvest** incl. the Phase-1 leaves (0.85-0.90).

### Frontier (low confidence / conjectural — the cultivation zone)
- **The exact dormancy intervals** and whether the "AI winter" narrative is clean — **Haigh: "There Was No First AI Winter"** (SIGART membership grew through the 1970s; the freeze hit elite labs, not the field). *The FACT of elite-lab defunding ~0.9; the clean whole-field-froze NARRATIVE ~0.5.*
- **The re-attribution / priority dispute** — popularizers (Hinton/Bengio/LeCun; Hopfield/Hinton) vs originators (Linnainmaa/Werbos/Ivakhnenko/Amari); **live and bitter**; Schmidhuber's claims read partly from his own partisan pages (~0.6).
- **Whether the three winters are one phenomenon or three** differently-caused, differently-timed downturns hitting different sub-fields (~0.6).
- **Anti-correlated rival fortunes** ("A's winter is B's spring") — well-attested but the schema has no clean slot (~0.7).
- **The 2024-Nobel frame-ownership dispute** ("is it even physics?" — physics/CS/cognitive-science) (~0.6).
- Deep priority roots (Ivakhnenko 1965 as "first deep learning"; Amari 1967) (~0.7-0.8).
- **Bits / MDL-on-learned-representations** as a near-principled-null (an open research problem).

---

## Discrepancies carried into the record (all 8 — the real-record frontier)

1. **[framework-vs-record] THE THREE-PARENT CONSUMMATION vs the binary weld (the single biggest framework signal).** AlexNet 2012 is framed by Wikipedia *and* Fei-Fei Li verbatim as "three fundamental elements converged for the **first time**": algorithm + **compute** + **data**. Two of the three are **instruments**, not content. The clean two-parent weld cannot hold the actual consummation. The weld did **not** fire when the algorithm existed (1989) — only when the instruments arrived (~2012). The record's *own language* is a direct hit on **R1** (N-ary parents) + **R4** (parent_kind: instrument), and motivates a **parent_is_gating/rate-limiting** flag.
2. **[priority-dispute] RE-ATTRIBUTION.** "Deep learning" is canonically credited to Hinton/Bengio/LeCun (2018 Turing) and Hopfield/Hinton (2024 Nobel), but the techniques are earlier: backprop reverse-mode = Linnainmaa 1970; applied to nets = Werbos 1974; first deep nets = **Ivakhnenko-Lapa 1965 (GMDH)**; stochastic gradient = Amari 1967. **Schmidhuber's 88-page report accuses the trio of "plagiarism";** LeCun calls him "manically obsessed with recognition." The Maxwell re-attribution analogue ("not the first inventor but the last re-inventor"), but **far hotter** (live, bitter, named primary sources). Instantiates **R10 reattribution{}**. The deepest root (Ivakhnenko, Soviet/Kyiv) faintly echoes QG's Bronstein.
3. **[dormancy-contested] CONTESTED DORMANCY.** Haigh (CACM 2023) argues the 1970s "winter" is substantially a **myth** — ACM SIGART membership ~doubled to 1,241 by 1973 and ~tripled to 3,500 by 1978; the freeze hit a few elite labs, not the growing field. Directly parallels Darwin+Mendel's disputed "35 years of neglect." The fact of elite-lab defunding ~0.9; the clean narrative ~0.5. *Also proposes the new weld-type term `double-dormancy-revival-weld` before use (§6 item 7).*
4. **[contested-genealogy] TWO/THREE WINTERS conflated.** The neural-net dormancy (~1969-86, Minsky-Papert + funding capture) is distinct from the "first AI winter" (~1973-80, Lighthill + Mansfield, mostly *symbolic*) and the "second AI winter" (~1987-93, Lisp-collapse + expert-system brittleness, again *symbolic*). The popular single story flattens ≥3 differently-caused downturns on different sub-fields. **Critically, connectionism's fortunes were sometimes INVERSE to symbolic AI's** — the schema has no slot for "A's winter is B's spring" (→ a `rival_lifecycle_coupling` variable).
5. **[framework-vs-record] SURPRISE DEMONSTRATED-but-NOT-ADOPTED.** The surprise (deep+backprop = universal representation learner) was **demonstrated working** small-scale long before consolidation: Ivakhnenko 1965 (8-layer net by 1971), Werbos 1974, **LeNet 1989 (deployed reading bank cheques)**. A *high-confidence weld demonstrated but not adopted* for ~20-40 years for want of scale — the framework's own conjecture-definition found in the record (**R15**) *plus a stronger state it lacks*: **demonstrated-not-adopted** (distinct from conjectured-not-confirmed). The most extreme **R9** case: surprise ~0.9 was a *deployed product* (1989) while the dominant child waited until 2012.
6. **[framework-vs-record] REVIVED-AS-REINTERPRETED ×3.** The object that revives is never the object that went dormant: single-layer perceptron → multi-layer backprop net (1986); shallow net → deep belief net / deep CNN (2006/2012); and **connectionism (a theory of MIND) → deep learning (an engineering toolkit)** — a science-to-technology reframing. Instantiates **R10 (revival.kind = reinterpreted) three times within one specimen** — the strongest multi-instance support in the batch.
7. **[framework-vs-record] INSTITUTIONAL/STATE actors as first-class lineage nodes.** The genealogy is unintelligible without DARPA (squeeze), CIFAR+Canada (carrier-through-dormancy), NVIDIA (instrument), Symbolics, MITI, Google/OpenAI. A foundation literally *carried* the wrapper through a winter; an agency was the chief squeeze; a company supplied the gating instrument. The v1 `people_0`-only ground kernel cannot hold these — **the strongest case in the batch for D2.**
8. **[contested-genealogy] 2024 NOBEL — "is it even physics?"** Hopfield/Hinton won for neural-network work justified via spin-glass/Ising physics; Hinton was "flabbergasted"; widespread debate that this is CS, not physics. The **same weld is claimed by physics / CS / cognitive science** — a frame-straddle (D3) plus a *which-knowledge-frame-owns-it* dispute; the consecration is contested along the seam's multi-disciplinary origin (echoing QG's "the historiography forks along the same seam").

---

## How each new dimension D1-D5 rendered (the v2 payload)

- **D1 (lifecycle + type).** The richest in the batch: an **8-phase graded trajectory** with a **double dormancy** (two winters) and **three reinterpreted revivals**, plus a **6-entry weighted weld_type** led by *instrument-enabled-weld* (0.85) and *state/funding-mobilized-weld* (0.90). The lifecycle is a **weighted index** over `dormancy_intervals`/`revival`/`status_trajectory`/`weld_chain` — it does not restate them. Forced one **new weld-type term** (`double-dormancy-revival-weld`), proposed in a discrepancy first.
- **D2 (actors generalized).** Exercised at full stretch: **20 actors** across `individual / lab / government / institution / company`, with `carrier_of` (UP) and `inhabitant_of` (WITHIN) populated. The bridge thesis is *load-bearing* here — the latent lineage's whole life is driven by physical-layer institutions. **Strongest D2 case in the batch.**
- **D3 (physical/latent filter).** Hand-checkable under each filter: the **latent view** = connectionism/backprop/deep-learning/transformers + the idea sub-wrappers; the **physical view** = the people + DARPA/CIFAR/NVIDIA/ImageNet-labor/Toronto/Google/OpenAI + the forcing events. The **instrument-parents (CUDA, ImageNet) and all institutions are `physical`**; the ideas are `latent`; actors and the PDP *lab* straddle. `layers_present = [physical, latent]`.
- **D4 (forcing events).** The batch's richest "weather": **13 events**, both **squeeze** (8 winter-drivers) and **pull** (5 un-stickers/accelerators) and one **both** (Fifth Generation). Each acts *through* an actor (Minsky-Papert→fashion; DARPA→funding; CUDA→NVIDIA; ImageNet→Fei-Fei Li), with graded `acted_on.strength`. The 1987 Lisp-collapse is recorded as a **squeeze on the RIVAL that pulled the child** — the anti-correlation.
- **D5 (fuzzy by design).** Graded throughout; the dormancy-interval **endpoints are deliberately soft** (`~1995`/`~2006`; 1969-86 fuzzy) precisely because Haigh disputes whether the first winter had crisp edges at all. The certain-core/frontier split is a *derived digest* of the per-node memberships; the **fulcrum sits high** (`core_boundary_locus`) with fuzz in two lateral pockets (winter-narrative, credit).

---

## Schema gaps surfaced (where v2 was hard to fill)

1. **GRANULAR MULTI-DORMANCY.** Two nested winter-cycles with *different* `why_frame`s (knowledge+politics; fashion+insufficient-instrument) **plus** a contested-dormancy overlay (Haigh) need R11 per-interval (done) **and a `dormancy.contested` flag** the schema lacks (worked around via Discrepancy 3 + frontier).
2. **ANTI-CORRELATED RIVAL FORTUNES.** No field expresses "this weld's winter is its rival's spring." `pre_weld_relationship=antagonism` (R14) captures the rivalry but not the **inverse-phase** dynamic. → proposed **`rival_lifecycle_coupling`** (a signed phase-relation between two welds' lifecycles).
3. **INSTRUMENT-PARENT AS RATE-LIMITER.** R4 tags `parent_kind=instrument`, but here an instrument-parent is the **gating** parent (the algorithm waited ~23 years). → proposed **`parent_is_gating / rate_limiting`** flag, distinct from the kind tag.
4. **DEMONSTRATED-NOT-ADOPTED.** R15 covers "conjectured early"; here the surprise was **demonstrated working** (1989) yet not adopted for ~23 years. The **adoption-lag** (technical proof → paradigm consolidation) is its own variable, stronger than conjecture-lag. → proposed surprise-state **`demonstrated-not-adopted`** + an `adoption_lag` field.
5. **INSTITUTIONAL CARRIER-THROUGH-DORMANCY.** D2's `carrier_of` is supported, but "a foundation/state deliberately funds a marginalized wrapper through its winter" (CIFAR) deserves a **named role (`flame_keeper` / `dormancy_patron`)** beyond generic carrier.
6. **FRAME-OWNERSHIP CONTEST.** The 2024 Nobel shows the same child claimed by physics/CS/cognitive-science — D3's straddle plus a **contested frame-ownership** slot the schema lacks (relevant where consecration/credit follows frame-ownership).
7. **WELD-TYPE VOCABULARY EXTENSION.** Proposed `double-dormancy-revival-weld` (the core 8-vocabulary has single-cycle types but no multi-cycle-dormancy type) — proposed in a discrepancy before use per §6 item 7.
8. **SOURCING CAVEAT.** Haigh's CACM text was **403-blocked** (reconstructed from search summaries, ~0.85); Schmidhuber's claims read partly from his **own partisan pages** (~0.6). No bit-values fabricated — `bits_note` is a **near-principled-null** (MDL-on-learned-representations is itself unresolved).

---

## Sources (with honest reliability + flags)

| source | type | rel. | note |
|---|---|---|---|
| [Wikipedia — *Connectionism*](https://en.wikipedia.org/wiki/Connectionism) | encyclopedia | 0.80 | three waves; roots; connectionism-vs-symbolic; sub-symbolic philosophy |
| [Wikipedia — *AI winter*](https://en.wikipedia.org/wiki/AI_winter) | encyclopedia | 0.80 | multi-cycle timeline; Lighthill; Mansfield; Schwarz "deeply and brutally"; Lisp 1987; Fifth Gen; Haigh note |
| [Wikipedia — *AlexNet*](https://en.wikipedia.org/wiki/AlexNet) | encyclopedia | 0.85 | the **three-element convergence**; GTX 580s; Fei-Fei Li quote |
| [Wikipedia — *Backpropagation*](https://en.wikipedia.org/wiki/Backpropagation) | encyclopedia | 0.80 | Linnainmaa 1970; Werbos 1974; RHW 1986; "last re-inventor" |
| [Haigh — *There Was No First AI Winter* (CACM 2023)](https://cacm.acm.org/opinion/there-was-no-first-ai-winter/) | scholarly-history | 0.85 | dormancy-contested SIGART data — **full text 403-blocked; reconstructed from search summaries** |
| [Wikipedia — *Jürgen Schmidhuber*](https://en.wikipedia.org/wiki/J%C3%BCrgen_Schmidhuber) | encyclopedia | 0.75 | the 17-point dispute; "plagiarism"; LeCun rebuttal |
| [Schmidhuber's own pages](https://people.idsia.ch/~juergen/who-invented-backpropagation.html) | primary | **0.60** | **PARTISAN PRIMARY** — one side of the dispute; flagged |
| [Wikipedia — *GMDH* / *Ivakhnenko*](https://en.wikipedia.org/wiki/Group_method_of_data_handling) | encyclopedia | 0.80 | GMDH 1965; 8-layer net by 1971 (deepest priority root) |
| [CIFAR — Turing/genAI accounts](https://cifar.ca/cifarnews/2019/03/27/turing-award-honours-cifar-s-pioneers-of-ai/) | aggregator | 0.70 | NCAP program 2004, ~$2.5M/5yr, Hinton director — self-reported but factual on dates/$ |
| [Wikipedia — *CUDA*](https://en.wikipedia.org/wiki/CUDA) | encyclopedia | 0.75 | CUDA 2007; GPGPU; the gating compute instrument |
| [Wikipedia — *Attention Is All You Need*](https://en.wikipedia.org/wiki/Attention_Is_All_You_Need) | encyclopedia | 0.85 | transformer 2017; Google Brain; attention lineage; harvest to LLMs |
| [Nobelprize.org / IEEE Spectrum — 2024 Physics](https://www.nobelprize.org/prizes/physics/2024/) | primary | 0.85 | Hopfield+Hinton; spin-glass justification; "is it physics" + "rewards plagiarism" |
| [ImageNet creation (Pinecone/Britannica/Zilliz)](https://www.pinecone.io/learn/imagenet/) | aggregator | 0.70 | ImageNet 2007-09; 14M images; Mechanical Turk |
| [CNN lineage (ETHW; com-cog-book)](https://ethw.org/Milestones:Convolutional_Neural_Networks_(CNN)) | aggregator | 0.70 | Neocognitron 1980 → LeNet 1989 (MNIST) |
| [Dartmouth / cybernetics schism](https://en.wikipedia.org/wiki/Dartmouth_workshop) | encyclopedia | 0.70 | McCarthy vs Wiener; mid-1960s funding capture |
| [Boltzmann machine / Hopfield bridge](https://en.wikipedia.org/wiki/Boltzmann_machine) | encyclopedia | 0.80 | Hopfield 1982 (Ising); Ackley-Hinton-Sejnowski 1985 |
| [Scaling laws (Kaplan 2020; Chinchilla 2022)](https://arxiv.org/abs/2001.08361) | aggregator | 0.65 | the scaling-law harvest into GPT-3/ChatGPT |

---

*End specimen. Reflexivity note carried in-record: the field's canonical history is itself the prize being fought over — the **same consecration** (2018 Turing, 2024 Nobel) that hardened the child triggered the re-attribution dispute, and the "AI winter" through which it slept is itself a whig-vs-revisionist battleground (Haigh). This is a **consummated weld with a contested historiography** — the inverse of QG (an unconsummated weld with a forked historiography), and the calibration counterpart to Darwin+Mendel's disputed dormancy.*
