# Gemini review (google/gemini-3.1-pro-preview)

**AUDIT REPORT: The Two-Halves Instrument**
**AUDITOR:** Gemini (External Pass, Adversarial)
**DATE:** 2026-06-21
**DIRECTIVE:** Demote-not-kill. Stress-test the structural integrity of the gather/sim dichotomy, the per-axis record schema, the math of confidence, and the physical/latent feedback loop. 

Here is the adversarial evaluation of the proposed v0.3 per-axis architecture.

---

### 1. The Two-Halves Framing (Measured Gather + Simulated Gaps)
*Is "measured gather + multiple-weighted-conjecture sim" sound, or does it invite laundering? What governs the fan?*

* **VERDICT:** **Risky.**
* **SHARPEST FLAW:** **Conjecture Inflation and the "Feedback Loop of Hallucination."** A multi-conjecture fan (X*n) without a strict, computable pruning mechanism will inevitably lead to exponential noise. If a model hallucinates 5 conjectures to explain a gap, and the next gap reads those 5 conjectures as context to generate 5 more, you don't get an "emergent canonical reading"—you get a combinatorial explosion of fan-fiction. You have vaguely deferred the pruning layer to "the X*n mechanism," but without defining a decay function or a validation trigger, the latent membrane will simply drown the physical one.
* **FIX:** **Radioactive Dye and Time-To-Live (TTL).** 
    1. A simulated bit must carry a strict "radioactive dye" (a permanent metadata taint). 
    2. *Generative layers must be barred from reading other unverified conjectures as context* unless explicitly simulating conditional futures. 
    3. Every conjecture fan must have a TTL. If the physical stream ("light through the keyhole") does not hit any of a conjecture's `followup` conditions within $N$ steps, the conjectured fan decays to zero. It must prune itself by default.

### 2. The Per-Axis v0.3 Record as the Home of Both Halves
*Does the WHO/WHAT/WHERE/WHEN/WHY/HOW/WHOM split work? Are there misfits?*

* **VERDICT:** **Overstated.**
* **SHARPEST FLAW:** **Collapsing Graph Edges into Node Properties.** You are building a DAG, but you are trying to stuff relational causality (WHY and HOW) into the internal axes of a single `LatentEvent` record. WHO, WHAT, WHERE, WHEN, and WHOM are discrete scalars/vectors belonging to a point in spacetime. WHY and HOW are *relationships to other events*. If a commit happened (WHAT) because a bug was filed (WHY), that "WHY" is not an axis with `measured_bits`—it is a *directed graph edge* to another node. Stuffing it into a local axis flattens and blinds your DAG. 
* **FIX:** Split the `LatentEvent` schema. 
    * **Intrinsic Axes (Node properties):** WHO, WHAT, WHERE, WHEN. These hold your scalar measurements and localized conjecture fans.
    * **Extrinsic Axes (Edge properties):** WHY, HOW. These are strictly *pointers* (edges in the DAG/KG) that carry their own `confidence` and `signal_type`. 
    * **The Contract (WHOM):** WHOM as observer is sound, but it must be an array or a wrapper, not just another axis, because a single event can be observed by multiple WHOMs with entirely different contracts.

### 3. Confidence Weights: The Commensurability Problem
*Are measured bits, per-axis confidence, conjecture weight, and contract validity one thing or four?*

* **VERDICT:** **Wrong.**
* **SHARPEST FLAW:** **Math Soup.** You are at severe risk of multiplying epistemic boundaries by Shannon entropy by statistical probability, and rendering the result as a single "blur" value. They are four fundamentally strictly incommensurable scalars:
    * `measured_bits`: Absolute payload weight (Information Theory).
    * `confidence ∈ [0,1]`: The predictive probability of a simulated gap (Probability).
    * `conjecture weight`: The normalized *intra-fan* distribution ($\Sigma w = 1.0$) deciding the winner (Statistics).
    * `contract validity`: An ordinal distance metric describing epistemic context (Frame).
    If you blend these to create a unified score, the COIN is broken; you will launder a low-information, high-confidence guess as "sharp."
* **FIX:** **Categorical Type System for Uncertainty.** Never allow these variables to touch mathematically. `measured_bits` dictates the *maximum possible sharpness* of the render. `contract validity` dictates whether the render is *allowed* to use those bits without a blur penalty. `conjecture weight` is purely for the RAG/Generative layer's internal voting and *never* dictates render sharpness. Only physical bits dictate sharpness; conjectures dictate *color* (or shape) in the UI, but remain physically blurry.

### 4. Follow-ups / Deeper Research Primary Mechanisms
*How are followups generated, tracked, closed, and how do they re-score the fan?*

* **VERDICT:** **Risky.**
* **SHARPEST FLAW:** **Unexecutable Natural Language Stubs.** If your LLM generates a follow-up like `"Check if Pav reviewed the doc on Tuesday"`, your system cannot close the loop. "Deeper research" becomes an unsearchable graveyard of text strings. If the loop cannot close computationally, the conjecture fan remains open forever, bloating the RAG index.
* **FIX:** **Executable Predicates.** A `followup` must be generated as a strict, computable query (e.g., a Cypher query on the DAG, or a reg-ex watcher on the incoming physical corpus stream). 
    * *Format:* `EXPECT_EVENT (WHAT=Pass/Fail, WHO=Pav, WHEN=Tuesday) -> resolves Conjecture_B`. 
    * The streaming physical layer ("keyhole") continuously hashes against the table of active predicates. The exact millisecond the physical query returns `TRUE`, the event fires a spreading-activation wave back down the DAG, collapsing the fan: Conjecture_B hits `weight=1.0`, converts to `measured_bits`, and deletes Conjectures A and C.

### 5. The Biggest Risk and the Ultimate Guardrail

* **THE BIGGEST RISK:** **Hypothesis Laundering via RAG.** The generative half produces a highly plausible, heavily weighted conjecture to fill a gap (e.g., "This code was written to fix Bug #402"). Later, another process queries the KG-RAG. The RAG retrieves this conjectured text, completely strips the metadata because LLMs operate on raw text tokens, and feeds it into the context window of a new simulation. The new simulation reads it as a fact, builds upon it, and outputs *new* nodes. You have just laundered simulated bits into foundational facts, entirely breaking the core COIN mandate ("never launder a generated bit as a measured one").

* **THE MOST IMPORTANT GUARDRAIL BEFORE SHIPPING:** **Compute-Level Taint Tracking (The Dual-RAG pass).**
    Before the generative half is allowed to operate over the substrate, the retrieval/RAG pipeline must be strictly bifurcated. 
    When an LLM is queried to resolve a new hypothesis, it receives TWO strictly separated context payloads:
    1. `<MEASURED_GROUND_TRUTH>` (Only data carrying hard physical bits).
    2. `<CONJECTURED_LATENT_THEORIES>` (Previously simulated gaps).
    The system prompt must enforce that the model cannot promote anything from Payload 2 into Payload 1. Better yet, *block Payload 2 entirely* from the generation phase of new facts, restricting its use exclusively to UI-rendering and user-facing "exploration" mode. If the sim-layer cannot eat its own tail, the hallucination loop breaks.
