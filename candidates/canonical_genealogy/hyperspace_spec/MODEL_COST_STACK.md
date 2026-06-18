# The Model Cost Stack — the BUILD iceberg under the inference tip (the backward camera's subject)

**Date:** 2026-06-18 | The wrapper spectrum pointed at the MODEL instead of the task. Designed via a 3-slice
adversarial-mapping workflow (compute / infrastructure-energy-thermo / data-civilization-bio-cosmos), each
scanning fresh 2026 literature; synthesized into one ordered stack. This is Pav's "everything in play when we
measure a model... all the way down to the Big Bang" — made into a partly-measurable spectrum.

## The spine — cheap inference is the apex of a deep amortized BUILD

When the latent camera reads a model's reasoning_tokens, that cost is the **TIP**. Beneath it is an iceberg of
**pre-paid BUILD** — the cheap USE is cheap *because* all of it was paid once (the amortization principle;
the COIN's replay branch; Bennett logical depth = the decompression time organized structure cost to
accumulate). The cost of the missing frame, scaled up: now the "frame" is the *whole model*. And the
**cross-model run is the instrument**: each model (DeepSeek V4 Flash / Gemini Flash-Lite / Qwen3.5 / gpt-5.5)
is a *different sample of the iceberg* — different architecture, training compute, data curation — so the
USE-tip spread back-projects toward the BUILD below.

## The 17-layer stack (tip → Big Bang), with clock + measurability

A **measurable crust (L1–L7)** thinning through a **PARTIAL mid-body (L8–L12)** to **pure narration at the
cosmic floor (L13–L17)**. The COIN's law throughout: read a number only where a layer honestly mints one;
elsewhere name the layer, mint no bit.

| # | layer | clock | measurable | the number (2026) |
|---|---|---|---|---|
| **L1** | **Inference compute** — reasoning_tokens the camera reads; ~2·N_active FLOP/tok | **USE** | **MEASURABLE** | $0.01–$25/Mtok across the set; reasoning_tokens in the API usage object; ~0.39–7.2 J/tok |
| L2 | Node draw — switching+leakage+memory-movement+NVLink+idle | USE+MAINTAIN | MEASURABLE | NVML/RAPL telemetry; node-J/token (arXiv 2601.22076) |
| L3 | Facility — PUE + cooling + water | MAINTAIN (2nd-law rent) | MEASURABLE (water PARTIAL) | PUE ~1.09; water ~0.05–0.5 mL/query (2304.03271) |
| L4 | Electricity source + grid carbon | MAINTAIN on BUILD substrate | MEASURABLE | gCO₂/kWh per region (~370–545 US, <20 Norway, >700 Poland); DCs ~460–490 TWh 2025 → ~950 by 2030 |
| L5 | Learned weights / tokenizer (frozen BUILD output replayed) | BUILD consumed at USE | PARTIAL | count exact (DeepSeek V3 671B/37B active); **DEPTH unreadable from the file** — only via L7 |
| L6 | Hardware — accelerator + its gap to the Landauer floor | BUILD+MAINTAIN | MEASURABLE | $2/H800-hr; B200 ~0.53 vs H100 ~2.46 J/tok; CMOS ~10³–10⁴ Landauers/op (2312.08595) |
| **L7** | **Training compute** — the 6ND run that made the weights | **BUILD** (Bennett depth made of dollars) | **MEASURABLE** | frontier 1e26–1e27 FLOP / $200–500M; **DeepSeek V3 2.788M H800-hr = $5.576M**; cost doubling ~5–8 mo |
| L8 | Engineering / failed runs / ablations | BUILD (dark matter) | PARTIAL — **known undercount** | Epoch: *most* of OpenAI's 2024 compute went to experiments, not final runs |
| **L9** | **Human supervision** — labeling / RLHF / RLAIF | BUILD (paid once, replayed every aligned answer) | PARTIAL (aggregate $ only) | **THE new dominant cost: data-labor exceeds compute up to 28×; labeling surged 88× vs compute 1.3× (’23–24)**; Llama-3.1 post-train >$50M/~200 people |
| L10 | Corpus assembly + curation + **distillation** | BUILD | PARTIAL | Common Crawl ~9.5 PB; **distillation makes it recursive — a cheap corpus can be REPLAY of a teacher's USE (R1→Qwen)** |
| L11 | Algorithms + mathematics (transformer→…→centuries of math) | BUILD (a frame in the wrapper sense) | PARTIAL | recent margin = **~7.6–8 mo efficiency-doubling** (2403.05812); absolute math-depth CONCEPTUAL |
| L12 | Fab / lithography / materials | BUILD (Slow-Growth Law in hardware) | PARTIAL | TSMC 2nm ~$30k/wafer; leading fab $15–20B; high-NA EUV ~$380M |
| L13 | Civilizational creation of the corpus (language ~100ky, writing, the ratchet) | BUILD (person-millennia) | **CONCEPTUAL** | cultural Bennett depth: short to *state*, un-fast-forwardable to *produce* |
| L14 | The biological harness (the language-ready brain, ~3.8 Gy) | BUILD on MAINTAIN | CONCEPTUAL build / PARTIAL ~20 W | cortex ~0.1 W compute vs ~3.5 W communication (PNAS 2021) |
| L15 | Cosmological free-energy + **Landauer floor** (funds all 3 clocks) | denominates USE/MAINTAIN/BUILD | PARTIAL flows / CONCEPTUAL share | **kT·ln2 = 2.8e-21 J/bit @300K**; Earth net exergy ~1.1e17 W; civ ~30–47 TW |
| L16 | Nucleosynthesis of the chip's elements | BUILD (paid by the cosmos) | CONCEPTUAL | abundances measured; no per-inference readout of the supernova |
| **L17** | **Big Bang** — low-entropy initial condition + the **Bennett-depth axis itself** | BUILD at the cosmological limit | CONCEPTUAL (uncomputable) | true depth uncomputable; only resource-bounded surrogates compute (2601.04728, 2403.04045) |

## What Pav's list didn't name (the expansions)
- **L9 human supervision** — the single biggest 2026 correction; alignment-labor now out-costs compute.
- **Distillation / synthetic-data inheritance (L10)** — a cheap model's corpus *is* an expensive model's
  replayed USE; the sharpest cross-model differentiator.
- **The node/PUE/water split (L2–L3)** and **carbon provenance (L4)** — a joule isn't just a joule (coal vs
  hydro ≈ 35× carbon); fossil fuel = ancient buried sunlight, so L4 is itself amortized stellar BUILD.
- **The CMOS↔Landauer gap (L6)** — a measured ~10³–10⁴× slack: the BUILD headroom that caps how cheap any
  USE can ever get.
- **The train↔inference crossover** — 1 GPT-3 train ≈ 1e12 inferences; inference now ~60–65% of ML energy:
  the literal hinge of the amortization principle.
- **The Landauer floor (L15) as the shared zero-point** — gives the camera a clean denominator: *cost in
  Landauers* (real J ÷ kT·ln2). And the **communication ≫ computation** motif recurs fractally — brain
  (3.5 W vs 0.1 W) and datacenter (network/MAINTAIN vs GPU/USE) — showing MAINTAIN is intrinsic to any
  physical information system.
- **Bennett depth as the vertical axis** — Pav listed horizontal layers; logical depth is the *ordering* that
  makes "easy = pre-paid" a theorem, not a metaphor, and is exactly what the backward camera samples.

## The measurable / conceptual waterline (the honest boundary — the finding itself)
- **Reads a real number:** L1–L7 (+ the L7↔L1 crossover). The camera can fully instrument the crust.
- **Proxied / aggregate-only:** L8–L12. Real but not attributable to one inference (L9 is the textbook case:
  a huge number at the BUILD scale, **zero** at the USE scale).
- **Named, never numbered (COIN bites hardest):** L13–L17 — civilization, the evolved brain, the supernova,
  the Big Bang. The rhetorical "all the way down" is honest *as narration*; minting a bit there is forbidden.

## The backward-camera instrumentation (what the cross-model run actually measures)
Per (model × prompt), the run produces a row:

> **(model, reasoning_tokens, $/answer, cost-in-Landauers, EDL-replay-fraction, anchored-to-public-BUILD-$)**

1. **USE tip (fully instrumented):** log reasoning_tokens + $ + derive J/tok × PUE × gCO₂, normalize to
   **cost-in-Landauers** (real J ÷ kT·ln2) → all models on one axis above the shared L15 zero-point.
2. **Back-projection to BUILD (the load-bearing move):** the tip height doesn't read the iceberg — the
   cross-model *spread* does. Run a **prequential-MDL / excess-description-length surrogate** (arXiv
   2601.04728, fully computable from held-out competence) scoring how much of each cheap USE is *replay of
   pre-paid structure* vs *re-derivation at inference*. A model answering a deep-knowledge probe at near-zero
   reasoning tokens is replaying maximal pre-paid depth (BUILD digested L7–L13 for free); one that must spend
   many tokens is re-paying a removed wrapper at USE-time. **This EDL read is the honest, computable surrogate
   for the uncomputable Bennett depth** (cite the resource-bounded version, 2403.04045 — never claim to have
   measured true depth).
3. **Anchor:** tie the surrogate to L7 (DeepSeek's published $5.576M vs frontier $200–500M) and the crossover
   (1 train ≈ 1e12 inferences) → state, with real numbers, the **amortization ratio** (how many inferences
   the BUILD was spread over).
4. **The honest stop:** read L1–L7 as numbers, back-project L8–L10 as flagged-undercount + EDL surrogate, and
   refuse to recover annotator-hours (L9), evolutionary bits (L14), or stellar joules (L16) from the token
   stream.

## Framework connection
- **Three clocks:** USE = L1; MAINTAIN = L2–L4 (rent vs the 2nd law); BUILD = L5–L17 (amortized over eons,
  Bennett depth). L15 (free energy + Landauer) is not a 4th clock — it *denominates* all three.
- **COIN:** cheap inference = replay of the pre-rendered BUILD bits; the waterline is the COIN's
  render-only-what-you-measured law applied to provenance.
- **Wrapper spectrum:** this is that spectrum with the *model* as the wrapper stack; "de-amortize a layer"
  (V11) is the task-frame echo of "a model trained with less BUILD."
- **Cosmic coin / log2 double-cone:** the 17 layers are worldline depth; the amortization ratio is the
  log-scale between BUILD and USE.

## Next
- Fold the per-run row (cost-in-Landauers + EDL-replay-fraction + amortization ratio) into the cross-model
  harness so every cheap-model run also samples the iceberg.
- Build a **stack viewer** (the iceberg with the waterline) and add it to the scope substrate.
- The EDL/prequential surrogate (2601.04728) is the concrete build for the **backward camera** octave.
