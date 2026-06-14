# External pass — Fable-takedown scene construct (synthesis)

**Date:** 2026-06-13 · **Reviewers:** codex GPT-5.5 (reasoning xhigh, **web-search-grounded** — it independently verified the event against AP/Wired/FT/WSJ) + Gemini (plan mode). Raw: `codex_review.md`, `gemini_review.md`. Briefing: `_briefing.txt`.

> This pass did real damage and most of it is fair. Recording it as a dated supersession record per the claim-lifecycle (demote-not-kill). The verdict is not "throw it out" — it is "the substrate survives; the **scene layer** over-claimed by presenting interpretation as derived-measurement."

## The convergent verdict (both reviewers, near-verbatim)
- Codex: *"Dressed-up storytelling **with a useful evidence log underneath**; the story enters at the scene graph and then pretends it was measured."*
- Gemini: *"Dressed-up storytelling: subjective editorial narrative cloaked in the language of data science."*

**The agreed fault line: the SUBSTRATE (the fact log) is sound; the SCENE LAYER (roles, the 2-depth graph, the depth-cut) is interpretation that was framed as "derived only from substrate." The over-claim is the word "derived."**

## Codex's web-grounded FACTUAL corrections (new damage — it found fresher sources than our dossier)
1. **"Worldwide" conflates two things.** The directive restricted **foreign-national access**; the **worldwide** cutoff was **Anthropic's compliance choice** (Wired: "Anthropic chose to remove access for all customers to ensure compliance"; FT: "net effect" was a global shutdown). Our graph routes everything off the directive and **erases Anthropic's agency** — Gemini flagged the same ("ignores Anthropic's agency in compliance"). **ACCEPT.**
2. **Fable vs Mythos had different deployment histories.** AP: Fable was **widely released**; Mythos remained **restricted**. Our "both launched 06-09, one 3-day worldline" compresses materially different histories. **ACCEPT** (and exactly the kind of thing the refine-scout should fold in).
3. **"First time / first-of-its-kind" is not established.** WSJ only says **some analysts called it unprecedented** — not a proven historical first. Our facts assert it at certainty 0.88. **ACCEPT — downgrade to "reported as unprecedented by some sources," attribute, lower certainty.**

## The convergent METHOD criticisms
| # | Criticism | Both? | My call |
|---|---|---|---|
| M1 | **The scene is the weakest joint** — `actor/acted_on/stage/audience` typing + the depth-cut are interpretive choices, not measurements; "derived only from substrate" is too generous | both | **ACCEPT** — the deepest valid hit |
| M2 | **The graph smuggles causality** — `Commerce → {all}` erases Anthropic's compliance step (billiard-ball model) | both | **ACCEPT** |
| M3 | **Certainty = false precision** — a 0–1 per fact without a calibration + independence model is theater; 20 outlets repeating Anthropic ≠ 20 independent measurements | both | **PARTIAL** — the spec already routes corroboration through verification-records (not certainty-inflation) and certainty is disclosed-subjective per a rubric; but the per-fact number IS a single judgment and should not be read as a measured probability. Make that explicit. |
| M4 | **Escape-hatch falsifiers** — "measurable effect/shift" undefined = delay mechanisms, not falsifiers | both | **ACCEPT** — quantize them |
| M5 | **Disclosed-nulls = protective belt / scout-state** — logging `competitor-unnamed` injects the specter without responsibility (Gemini); they are search-status ("not found by timestamp"), not event-facts asserting "none exists" (codex) | both | **PARTIAL** — they ARE worded as "not found in any source reviewed" (search-status), but should be **tagged** as search-status, not sit in the same lane as observed facts |
| M6 | **`testimony-from-above` grants epistemic status by vocabulary** — rename to `user-seed-origin`, mark independent confirmation separately (codex) | codex | **FLAG for Pav** — the route names are the framework's C1 route machinery (observer_planes), not invented here; renaming is a framework-vocabulary decision, not a unilateral one. The independent-corroboration IS separately recorded (n0023). |
| M7 | **"0 disputed" not credible** — rationale disputed, statute undisclosed, evidence thin | codex | **PARTIAL/PUSHBACK** — "0 disputed" is a **technical bucket count** (no fact-value has a contradicting verification record); the rationale-dispute **is** recorded as facts (n0003/e0008). But the phrase reads over-clean — surface it better. |

## The single most-improving change (both converge)
Codex: *"Replace the scene graph with an entailment table: every node, edge, role label, beat, and narrator line cites exact source support and classifies itself as `observed | attributed | inferred | search-status | projection`. Anything without source-entailment leaves the substrate-derived scene."* Gemini: *"force quantitative thresholds on falsifiers."* → **Both point at the same fix: stop letting interpretation ride for free inside a structure labelled 'measured.' Tag the entailment class of every scene element; quantize the falsifiers.**

## Correction plan (proposed — gated on Pav's go)
1. **Relabel the scene as an explicit INTERPRETIVE layer** over the measured substrate (not "derived only from"). Add an **entailment tag** per cast node / edge / beat: `observed | attributed | inferred | search-status | projection`. build_scene.py computes it from the fact's route (measured-on-plane→observed, lateral-testimony→attributed, inferred-from-below→inferred, disclosed_null→search-status). The narrator surfaces it.
2. **Fix the graph (M2):** insert Anthropic's compliance as the mediating node — `directive → foreign-national-access`; `Anthropic →(compliance) worldwide-cut`. Stop routing the worldwide cut off Commerce.
3. **Refine 3 facts (factual):** first-time → attributed-unprecedented (cert↓, "per some analysts"); split Fable (widely released) / Mythos (restricted); mark the worldwide cut as Anthropic's compliance act.
4. **Quantize the 3 projection falsifiers (M4):** concrete thresholds + dates (e.g. SHORT: "Anthropic public-sector revenue −>X% or restoration >N days"; MEDIUM: "≥1 non-Anthropic deployed model named in a Commerce directive within 365 days"; LONG: "RoW API-share shift toward Chinese frontier models >X points over 24 mo").
5. **Clarify semantics (M3, M5, M7):** note certainty = disclosed-subjective (rubric-banded), independence tracked via verification-bucket not the number; tag disclosed-nulls as search-status; add a line that the rationale is contested (recorded as facts) even though the disputed-bucket count is 0.
6. **Refine-scout (the fuzzy loop):** fold in AP/Wired/FT/WSJ (the fresher sources codex surfaced) — they sharpen the worldwide/foreign-national, Fable/Mythos, and first-time questions directly.
7. **Flag M6 (route rename) to Pav** — framework-vocabulary call, not unilateral.

## Lifecycle bookkeeping
- **Dead child:** "the scene is *derived only from* the substrate (measured)." Refuted by both reviewers — the role-typing + graph are interpretation. → demoted to "an **interpretive** scene **over** the measured substrate."
- **Sharpened parent:** the layered construct survives **if** every scene element carries its entailment class and the falsifiers are quantized. The substrate (evidence log) itself was **not** refuted — codex called it "a useful evidence log underneath."
- **Dead-children tally (this construct):** +1 (the "derived = measured" over-claim).

---

## Corrections APPLIED — 2026-06-13 (Pav: "rename and land the pass")

All verified: substrate recompiles 0 errors / 0 fbt flags; scene rebuilds; toy reloads clean (no console errors).

1. **Scene reframed as an interpretive layer (M1).** `scene._doc` now says "an INTERPRETIVE scene built OVER the measured substrate — NOT 'derived = measured'"; the role-typing / depth-cut / graph are flagged as interpretive. New top-level `scene.epistemics` block carries the entailment legend + the certainty / disputed notes.
2. **Entailment class on every fact + beat (M1, the both-converge fix).** `build_scene.py:entailment_of()` maps route → `observed | attributed | inferred | search-status | seed`; projections = `projection`. Beat breakdown now `{observed:10, attributed:6, search-status:2}`. The narrator (scene + toy) surfaces it per line.
3. **Graph de-smuggled (M2 — both reviewers).** `ent-directive` acts_on → `{foreign-nationals, Fable, Mythos}` (the directive's true scope); `act-anthropic` acts_on → `{Fable, Mythos, EU-arrangement, Glasswing}` (the worldwide compliance cut). New beat **e0018** = the mediating compliance step ("could not separate foreign nationals in real time → cut worldwide"). **Verified WebSearch 2026-06-13** (Anthropic primary + Bloomberg "US Orders Halt to Foreign Access" + CNBC); e0018 + n0009 corroborated.
4. **"First time" un-baked (factual).** e0007 no longer asserts the superlative; new beat **e0017** carries it as *attributed* ("outlets described… not a verified historical first", cert 0.6, route lateral-testimony).
5. **Fable-vs-Mythos deployment split (factual, honest).** Could NOT verify codex's AP claim (AP fetch blocked; not in WebSearch) → recorded as **open_question n0027** at cert 0.4, route inferred, "do NOT assert until a scout confirms" → auto-enters the fuzzy/refine queue (now 9 regions).
6. **Falsifiers quantized (M4 — both).** SHORT → "restored ≤30d AND no guidance cut AND no sustained >2% stock move, by 2026-09-13"; MEDIUM → "no non-Anthropic deployed model named in a Commerce/BIS action by 2027-06-13"; LONG → "RoW Chinese-model usage share not up >5pp over 24mo on a named proxy."
7. **Route renamed (M6 — Pav approved).** `testimony-from-above` → `user-seed-origin` (substrate + build_scene + toy HUD/note); independent corroboration stays separately recorded. Entailment = `seed`.
8. **Semantics surfaced (M3, M5, M7).** `scene.epistemics`: certainty = disclosed-subjective (independence via verification-bucket, not the number); disclosed-nulls = search-status; the 0-disputed bucket ≠ "uncontested" (the rationale-dispute is recorded as facts).

**Post-correction substrate:** 44 best-values, 10 corroborated, 0 disputed, 0 flags; 18 beats; 9 fuzzy regions queued. The construct is now **v0.2: an interpretive scene over a measured, entailment-tagged substrate, with quantized forward falsifiers.** The substrate (evidence log) was never refuted; the over-claim was.
