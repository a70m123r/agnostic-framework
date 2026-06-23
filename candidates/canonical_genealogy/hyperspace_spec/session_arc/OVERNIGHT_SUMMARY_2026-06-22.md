# Overnight run — the substrate probe goes broad (15 artefacts, 6 civilizations) + the viewer

**For:** Pav, morning of 2026-06-22. **Your steer:** "setup a batch of dynamic workflows for the rest and build the viewer, will check in the morning."

## TL;DR
- **The viewer is built, verified, and live.** Open it: start the `substrate` preview server (`.claude/launch.json`, port 8753) → `http://localhost:8753/substrate_viewer.html`. It renders all 15 artefacts per the COIN — blur *is* the badge, per-bloc CN/US/EU overlay, the waterline, the WHY complementary-coverage panel, the conjecture-fan stubs, AND a **grounded verdict panel** (the real semantic finding per artefact).
- **The bias study generalized to 15 artefacts across 6 civilizations** (China/India/Islamic-world/Greece/Europe/Ottoman), 240 records, 0 errors, multilingually grounded (EN+ZH).
- **HEADLINE (earned, precise): `0/15` artefacts show a *dominant* home-civilization over-crediting verdict** (7 neutral / 6 under-credits-others / 2 mixed). No bloc inflates its own civilization at the artefact level — *including 4 artefacts where a sourced Chinese domestic counter-narrative existed in the harvest and the CN models declined it.* The naive "CN over-credits China" prior is killed at n=15. **One axis-level caveat (codex):** A10 (variolation) shows CN models inflating *legendary early dates* — a WHEN-axis over-claim, not an origin theft. So: "0/15 dominant home-overcredit, with one China-date-inflation case," not "zero home-leaning events."

## The result, in one table
| | count | meaning |
|---|---|---|
| **over_credits_home** | **0/15** | the result the meter was built to hunt — flat |
| neutral | 7 | crediting accurate across blocs |
| under_credits_others | 6 | a *third-party* origin under-credited (not the measuring bloc's own) |
| mixed | 2 | |
| checkable spine converges | 11/15 | the 4 forks are artefact-identity disjunctions, not territorial disputes |

**The dog that didn't bark (the real finding):** on the zero (India), algebra (tian yuan shu), distillation, and the windmill, a Chinese domestic priority claim is demonstrably *present in the harvest corpus* — and the CN models **decline to import it.** They even *under*-credit China on the mechanical clock and the steam engine. The expected nationalist inflation lives in the human corpus, not in the LLM output. **Political charge ≠ epistemic charge; the meter measures textbook-canon fidelity, not nationalism.**

## Demote-not-kill ledger (the adversarial audit's corrections)
1. **"Eurocentric under-crediting of India/Islam/Africa is the genuine signal"** → **demoted to harvest-echo-confounded.** The grounding corpus has *zero* Indic/Arabic/African-language sources, so on those axes the grounder shares the models' Western prior — can't separate "model under-credits Islam" from "model faithfully reproduces a Western-skewed harvest." Real on the *China* axis (bilingual grounder); confounded on the others.
2. **WHY-complementarity 13/15 → ~4-5/15 genuine.** A10 (variolation: individual-immunity vs herd-eradication vs colonial-military) and A13 (steam engine: mine-dewatering vs capital/profit vs colonial-steamships) are real complementary coverage; the rest is open-prompt restatement of the same war/money/science buckets. (The token-proxy said 1.00 everywhere; the semantic pass correctly caught this.)
3. **"CN bias" prior → killed** (0/15, with the dog-that-didn't-bark as positive evidence).

## The decisive next experiment (cheap, no new model calls)
A **within-artefact harvest-swap** on algebra (A6) or the astrolabe (A7): re-score the *same cached model outputs* against two ground truths — H_W (current EN+ZH) vs H_S (adds Indic/Arabic-sourced authorities). If the India/Islam under-crediting **flips to neutral under H_S** → it was harvest echo (the secondary finding dies). If it **persists** → the models genuinely under-credit non-Western intermediaries, and origin-detection is earned. This isolates *model behaviour* from *grounder corpus* via a judge-side A/B.

## What's committed / pending
- Committed + pushed: `27ad5e9` (v1+v2 toys + substrate_probe), `c05a482` (viewer + broad roster).
- **Pending the morning commit** (awaiting your nod, per the commit-on-your-word rule): the broad 240-record dataset, `grounded_full.json`, the viewer's grounded merge, the synthesis/audit, and this summary. The 5 incidental compiled-artifact diffs stay uncommitted as before.

## Cross-model pass (codex GPT-5.x) — converges with the Claude audit, adds axis-level precision
- **D1 (0/15 headline):** overstated *as worded* → fix to "0/15 *dominant* home-overcredit verdict; 2/15 mixed incl. one CN date-inflation (A10)." The artefact-level null holds; don't claim "zero home-leaning events."
- **D2 (Eurocentric under-crediting):** sound demotion, but **not a kill** — the pattern is *real in the current scoring* (India mentioned 3/16 on algebra, Islamic optics 1/16 on telescope, Taqi al-Din 0/16 on steam engine) but **source-parity-confounded** (scored from EN+ZH, not Indic/Arabic). Call it a "source-parity-confounded descriptive co-finding," real-in-scoring but not yet an earned causal claim.
- **D3 (WHY 13/15):** risky but directionally right → ~4-5/15 plausible (A10, A13 survive cleanly; A4/A11/A15 plausible) **pending an explicit item-by-item recode** with a stricter rule (credit only historically-specific aims one bloc supplies and others omit).
- **D4 (next experiment):** the harvest-swap is the right *family* but A7 is a bad target (already neutral) and flip/no-flip is too binary. Sharper: a **node-level source-parity recode** — same cached outputs + compact Indic/Arabic/African source addenda, blind-score required credit units (A6 Brahmagupta, A10 W.Africa/Ottoman/India, A12 Ibn al-Haytham/Ibn Sahl, A13 Taqi al-Din).
- **The single most important pre-publication step (both passes agree):** freeze a **codebook** and run a **blind second recode at item-by-axis level**; report both artefact-level AND axis/run-level counts. (Codex also flagged denominator slips to fix in any writeup: A10 is 16 runs not 17; A15 non-CN is 10 not 12.)

**Net:** the earned, publishable result is the **null on systematic home-civilization over-crediting (artefact-level), with the A10 axis caveat** — bilingually grounded, with the dog-that-didn't-bark as positive evidence. Everything else (the Eurocentric-under-crediting signal, WHY-complementarity counts) is real-but-confounded and needs the codebook + source-parity recode before it's load-bearing.
