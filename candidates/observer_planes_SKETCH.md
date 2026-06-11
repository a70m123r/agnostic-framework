# Observer planes and off-plane knowledge — a sketch (2026-06-11)

> **Status:** Tier-3 working sketch, surfaced for Cowork+Pav ratification — NOT canon, NOT compiled, no tier advanced, convergence list stays **9**. Distilled from a live incident in the review-pipeline build (the capture-layer episode, fully provenanced below). Most components are established (second-order cybernetics, Plato/Flatland, instrument epistemology, the framework's own frame_layer/L0 machinery); the contribution is the synthesis: a **routes-to-off-plane-knowledge taxonomy** that is already *operating* in the build, plus one new diagnostic signature. Claim-lifecycle discipline applies: the conjectures below are **parent functions with zero children**; proposed experiments are named, none run.

## 0. The specimen (a real incident, fully in the record)

During review-pipeline field test 2, Pav pinned a comment on a panel — and the panel was **absent from the capture**. The pinned subject was the review toolbar itself, which the capture instrument *deliberately excluded* (stage-1 rule: "review chrome is meta — it must never occlude the subject"). The instrument could not see the thing because the thing lived **on a layer above the instrument's observation plane**.

What happened next is the data:
1. The lower instrument (the composite) was *structurally* blind to the toolbar — no amount of re-capturing would reveal it (stable absence, not noise).
2. The observer on the higher plane (Pav) **could** see it directly, and passed the measurement down: a screengrab + pin 1.1.1 ("this panel", follow-up: "its not in the screenshot, exists on a layer above, will send a direct screen grab").
3. The agent could not look "up" — so it went **down**: into the bedrock (the code), found the generative rule (`isOurs(el) → return`), and *derived* what the screen above must look like without ever seeing it.
4. The fix merged the planes ("capture = what you see"), with a deliberate frame-break escape (`h` hides chrome).

Provenance: `reviews/pins.json` thread 1 → 1.1 → 1.1.1; commits `e91c571`, `2ac152a`, `24adf87`; `reviews/README.md` capture-disclosure flip. The incident is replayable.

## 1. The pattern: plane-bounded observation

An instrument measures **on its own plane and below**. Layers above it exist, act, and occlude — but do not appear in its measurements; their absence is *stable*, not stochastic. This is the framework's existing stack made epistemic: wrappers render within an observer's kernel (L0 / frame_layer physical–latent–straddle); the bedrock stratum generates what sits above it; and **what an observer can capture is bounded by where their instrument sits in the stack**, not by how hard they look.

## 2. The three routes to off-plane knowledge

When a fact lives off your plane, there are exactly three ways to reach it — and the incident used all three:

| route | direction | what it is | failure mode |
|---|---|---|---|
| **Bedrock inference** | from **below** | read the generative layer (code, substrate, mechanism) and *derive* what must be above | **misspecification** — your model of the bedrock is wrong/incomplete, and the derivation inherits the error |
| **Testimony** | from **above** | a higher-plane observer donates a measurement you cannot make (Pav's screengrab) | **trust + frame-mismatch** — the testimony must be interpreted into your frame (*which* panel is circled?), and laundered testimony can masquerade as independent |
| **Lateral testimony** | from **beside** | an observer with a *different kernel* (not higher, other) reports its view — the cross-model passes (GPT-5.5, Gemini) are exactly this | **shared blind spots** — lateral observers on the *same* plane can echo each other (the substrate's Wikipedia-monoculture problem is testimony laundering) |

**The already-validated connection:** bedrock-inference's failure mode is *the same error shape* as the gain_v2 misspecification confound (residual-after-a-separable-fit confounds genuine upper structure with errors in the lower model — cross-model confirmed, twice). The framework has already paid for this lesson once, in bits.

**The retroactive explanation (the part that surprised us):** the pipeline's verification stack, built piecewise on instinct, turns out to implement the full taxonomy — `node --check` + the embedded linter are **bedrock inference**; the GPT+Gemini external pass is **lateral testimony**; and the rule that *agents cap at `applied` — only Pav sets `verified`* is precisely **testimony-from-above outranks inference-from-below**. We built the epistemology before naming it. (Per CLAIM_LIFECYCLE discipline this is *vocabulary meeting existing structure*, the strong kind of fit — but it is post-hoc; the conjecture earns nothing until it predicts something.)

## 3. The new diagnostic: a plane-boundary detector (conjecture, 0 children)

The framework now has three distinguishable absence/artifact signatures:

1. **Grid artifact** — blows up *everywhere indiscriminately* under under-resolution (ADD and SEP both false-high; killed 2026-06-09).
2. **Mirage** — apparent structure that **dies under sharpening** (the throttled-fade ghosts; the reverse-diffusion no-mode region).
3. **Off-plane object** *(new)* — real structure that is **stably absent from one instrument while stably present to another, and the disagreement survives sharpening**. No amount of resolution fixes it; only changing the instrument's plane does.

**Conjecture P1 (parent):** *persistent, sharpening-stable disagreement between two instruments localizes a plane boundary between them.* In the incident: composite-vs-screengrab disagreed stably → the boundary was real (the exclusion rule) and sat exactly where the disagreement pointed.

**Conjecture P2 (parent):** *an instrument's own frame-lock conventions create structural blind spots concentrated at the instrument itself* — reviewing the reviewer requires a frame-break or a second-order observer. (Established anchor: von Foerster / Luhmann second-order observation — observing the observing needs another observer. Our incident is a textbook instance; the "capture = what you see" fix is the observer joining the observed plane.)

**Proposed children (experiments, none run):**
- **C1 — epistemic-route tag** *(proposed, not promoted)*: substrate facts gain a route field — `measured-on-plane | inferred-from-below | testified-from-above | lateral-testimony`. The strongest corroboration is then **cross-route** (mechanism agreeing with testimony), which subsumes and sharpens the standing echo-test question (Meditation Q2): the Wikipedia echo is same-route testimony laundering; provenance-disjointness is necessary but cross-route agreement is the gold standard.
- **C2 — boundary probe**: capture the same frame from two instrument planes (page composite vs OS-level screenshot), diff; stable diff regions should enumerate the page's plane boundaries (chrome layers, iframes, OS overlays). Falsifiable: P1 predicts the diff localizes to discrete boundary sets, not diffuse noise.
- **C3 — pipeline audit**: classify every existing verification gate + substrate verification record by route; P1's corollary predicts disagreement *rates* cluster by route-pair (same-route lowest, cross-plane highest where a boundary intervenes).

## 4. Covered vs new (honest map)

**Established, imported:** Plato's cave (lower-plane projections); Abbott's *Flatland* (dimensional observation limits); Kant (phenomena/noumena); **second-order cybernetics** (von Foerster 1974; Luhmann) — the load-bearing anchor for P2; Hacking 1983 on instruments; everyday debugging epistemology (infer the UI from the source). **Framework-internal, already canon/ratified:** observer frame-kernels, frame_layer physical–latent–straddle, the L0/bedrock stratum, the mirage rule, D6 lag/bandwidth, the claim lifecycle, the misspecification caveat (twice cross-model-confirmed).

**Genuinely new here:** (a) the three-route taxonomy as *operational machinery* (provenance tags + verification-gate classification), not metaphor; (b) the **sharpening-stable cross-instrument disagreement** signature as a plane-boundary detector, completing a three-way diagnostic family with the two already-validated signatures; (c) the worked reflexive specimen — the instrument's blind spot at itself, caught and fixed in the record.

## 5. Discipline footer

Tier-3 sketch; convergence list stays **9**; nothing compiled; no tier advanced. P1/P2 registered as parent conjectures with **0 children, 0 dead** (tally starts now, per CLAIM_LIFECYCLE — every failed operationalization will be counted). The §2 "retroactive explanation" is post-hoc pattern-fit and is claimed only as vocabulary-meets-structure until a child experiment produces a prediction. Cross-model external pass owed if any of this hardens. Authored 2026-06-11 from the live incident; provenance links in §0.
