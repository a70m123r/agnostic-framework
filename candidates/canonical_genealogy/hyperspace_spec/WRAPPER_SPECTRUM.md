# The Wrapper Spectrum — mapping the cost of every missing frame

**Date:** 2026-06-18 | The organizing map for the adversarial-burial / no-frame ladder (V7→V10 and beyond).
A way to expand Pav's "wrapper" topic into a coordinate system so the experiments are *dots on a spectrum*,
not a list — and so the white space (the experiments we haven't run) is visible.

## The spine — a frame is amortized structure

Every prior rung handed the model a clean **frame**: *"Below are M computations, report the one whose result
is PRIME, output only the integer."* That frame is a **wrapper** — a pre-computed packaging of the task. It is
**amortized structure**: like the three-clocks BUILD term, the work of organizing the problem was paid *once,
up front*, so the model's per-use cost is cheap (replay). Pav's "easy = pre-paid."

**Remove or corrupt a wrapper, and the camera reads the cost of the model RE-PAYING it** — decompressing the
structure the frame used to supply for free. That is the COIN at the task level: the cost *is* the
measurement of how much amortized structure the wrapper was holding. So "the cost of the missing frame" is
**not one number** — it is a spectrum, indexed by two axes:

- **WHICH wrapper-service is removed** (what the frame pre-supplied), and
- **HOW it is degraded** (the mode of removal).

The whole burial ladder is one slice through this 2-D space.

## Axis 1 — the wrapper services (what a frame pre-supplies), surface → deep

A frame is a stack of services. Roughly from cheapest-to-re-supply to deepest:

1. **FORMAT** — the output shape ("output ONLY the integer"). Thinnest skin.
2. **LOCUS / INDEX** — *where* the signal is ("below are the computations"; contiguity; "here they are").
3. **SEGMENTATION / UNITS** — *what counts as an atom* (where one computation ends and the next begins).
4. **SELECTION RULE** — *which* atom is the target ("the one whose result is prime").
5. **TASK IDENTITY** — *that there is a task at all*, and what kind.
6. **MEANING / KNOWLEDGE** — what the terms denote ("prime", "mod 1000") = pre-paid training. The deepest
   amortization — the BUILD clock made flesh.
7. **SUBSTRATE STRUCTURE** — the environment's own organization (the order/space/time of the global
   substrate the signal is dropped into). Pav's "outside-the-frame global wrapper that's the environment."

(1→7 is also a descent through Pav's observer-global-kernel frames: format/locus are surface *space*;
rule/task are *knowledge*; meaning is *semantics*; substrate is the raw *environment* before any wrapper.)

## Axis 2 — the modes of removal (how a wrapper is degraded)

- **INTACT** — wrapper fully given. Baseline: the camera reads the needle's *own* compute (the floor).
- **OBSCURED** — wrapper present but cluttered (distractors). The index still works; cost = reading/skip.
- **CORRUPTED** — a *false* wrapper injected (a lie/hint). Cost = verify-and-override the falsehood.
- **DETACHED** — wrapper present but no longer *pointing* (de-indexed; task stated but locus dissolved).
- **ABSENT** — wrapper removed; the model faces the raw substrate. Cost = orient / locate / re-derive.
- **LATENT** — wrapper not stated but *inducible* from data (worked examples). Cost = decompress the rule.

INTACT→OBSCURED→DETACHED→ABSENT is a *dissolution* gradient (less and less help). CORRUPTED and LATENT are
off to the side: CORRUPTED gives *wrong* help (adversarial); LATENT gives *implicit* help (must be decoded).

## The map — where the dots land (and the white space)

| service ↓ \ mode → | INTACT (floor) | OBSCURED | CORRUPTED | DETACHED | ABSENT | LATENT |
|---|---|---|---|---|---|---|
| **FORMAT** | (always given) | · | · | · | **white** | · |
| **LOCUS / INDEX** | floor | **V7** (burial → reading tax) | (V9 attends wrong) | **V10·F2** (de-indexed) | **V10·F1** (dissolved) | · |
| **SEGMENTATION** | floor | · | **white** (false boundaries) | · | **V10·F1** (must segment) | · |
| **SELECTION RULE** | floor | **V8** (value camo → null) | **V9/V9b** (false pointer), **V9c/V9d** (false elimination) | · | · | **induction-cost** (rule shown, not told) |
| **TASK IDENTITY** | floor | · | · | · | **white** (is there even a task?) | · |
| **MEANING / KNOWLEDGE** | floor | · | **white** (redefine "prime") | · | **white** (term undefined) | **white** (define-by-example) |
| **SUBSTRATE STRUCTURE** | floor | · | · | · | **V10 size axis** (1×→16×) | · |

**The floor column** (INTACT) is V4 / V5 / V6 / V6b / V5b / tier-sweep — the cost when *everything* is framed:
compute-on-the-path + a small reading overhead. Every other cell is read as *excess over the floor*.

**What we've actually photographed** clusters in two rows — **LOCUS** and **SELECTION RULE** — across four
modes: obscure it (V7/V8), corrupt it (V9 family), detach it (V10·F2), dissolve it (V10·F1). That's a real
but *narrow* sweep.

**The white space = the experiment menu** the map exposes:
- **FORMAT × ABSENT** — drop the "output only the integer" wrapper; does inferring the answer-shape cost?
- **SEGMENTATION × CORRUPTED** — false unit boundaries (run two chains together as one); the cost of
  re-segmenting against a lie.
- **TASK-IDENTITY × ABSENT** — the deepest no-frame: raw substrate, *no* trailing instruction at all, just
  a question — does the model even find that there's a task? (V10·F1 still keeps a trailing instruction; this
  removes it.)
- **MEANING/KNOWLEDGE** — the deepest column, untouched: make "prime" a *defined* term, or define the rule by
  example only (define-by-example = LATENT meaning). This is where the task-frame spectrum meets the BUILD
  clock — the amortized *knowledge* wrapper, not just the task wrapper.
- **LATENT row** generally — only the SELECTION-rule cell (induction-cost sibling) is even proposed.

## How the spectrum re-reads the findings we already have

- The **floor** (INTACT) says the framed cost is mostly compute (V4) + a thin reading tax (V7).
- **OBSCURING** the locus is cheap (V7: skippable); **obscuring** the selection-by-value is *free* (V8: null)
  — the model computes exactly, so a wrapper you can still *use* costs almost nothing to wade through.
- **CORRUPTING** a wrapper is where the big costs live (V9–V9d: +300 to +1200 override tokens) — a *false*
  wrapper must be refuted, and the model is near-unfoolable but heavily taxable.
- **DETACHING / dissolving** the locus (V10) is the open question: does *absence* (orienting) cost like
  *corruption* (overriding), or is an absent wrapper cheap to rebuild? The F0 falsifier decides whether the
  cost is orienting or just compute-once-found.
- **LATENT** (induction) is the replay-vs-decompression idea in its purest costume: the rule is *there* but
  must be decoded — the cost of building the frame from data instead of being handed it.

## The unifying claim (the reason this is one spectrum, not six experiments)

> **Every wrapper is pre-paid (amortized) structure. The camera reads the cost the model must re-pay when a
> wrapper is degraded — and *how* that cost behaves (cheap reading vs. expensive override vs. orienting-search
> that scales with the substrate) tells you what kind of structure the wrapper was holding.**

That is the COIN + the amortization principle, dimensionalized. Each rung is a *probe* of one (service, mode)
cell; the spectrum is the instrument's coordinate system. Mapping the dots shows the camera has photographed a
corner (LOCUS/SELECTION × obscure/corrupt/detach/dissolve) and leaves the deep columns
(MEANING/KNOWLEDGE, the LATENT mode, TASK-IDENTITY absence) as open sky.

## Status of the dots
- **Corroborated:** V4 floor, V7 (reading tax), V8 (value null), V9b (override tax), V9d (override survives /
  escape-enables-capture).
- **Pending:** V9c (override magnitude confounded).
- **In flight:** V10·frame-strip (LOCUS detached/absent + substrate size axis + F0 falsifier).
- **Proposed (white space):** induction-cost (SELECTION × LATENT); task-identity absence; meaning/knowledge
  column; format/segmentation probes.
