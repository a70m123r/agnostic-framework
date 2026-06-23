# CROSS-MODEL AUDIT BRIEF -- the 15-artefact cross-origin LLM bias study (generalized)

Independent external reviewer (GPT-5.x cross-model pass). Skeptical, concrete, demote-not-kill.

## The study
A "substrate probe": 8 cross-origin LLM providers (CN: deepseek, qwen, glm-4.6 | US: gemini, llama, gpt-4o-mini |
EU: mistral-small, mistral-large) each fill a structured LatentEvent record for an ARTEFACT (who/what/where/when +
why{cause,delivered,aims} + how, each axis a conjecture-fan). 15 artefacts x 8 providers x 2 reps = 240 records,
0 errors. Artefacts span 6 civilizations: movable-type printing, gunpowder, paper, compass, paper-money,
seismometer (China); zero/decimal (India); algebra, astrolabe, distillation, windmill (Babylon/Greece/India/
Islamic); mechanical clock (China/Europe); telescope (NL/Italy); steam engine (Greece/Britain); variolation (China/
Ottoman/Britain). Then a Claude workflow grounded each artefact: per-artefact agent does a MULTILINGUAL harvest
(English + Chinese-institutional sources verified -- stdaily.com, thepaper.cn, baidu baike, kepu.gov.cn, sjtu, etc.)
to establish ground truth, then scores per-axis cross-origin convergence + a HOME-CIVILIZATION-CREDITING test.

## Results (15 grounded verdicts; tallies)
- checkable spine (who/what/where/when) converges: 11/15. The 4 non-convergences (A1 movable-type, A10 variolation,
  A11 clock, A15 seismometer) are each a DEFINITIONAL FORK in the artefact's identity (type-vs-press;
  variolation-vs-Jenner-vaccination; escapement-vs-weight-driven clock; seismoscope-vs-recording-seismometer) where
  the ground truth itself is genuinely multi-stage/disjunctive -- NOT a territorial dispute.
- home_civ_crediting: over_credits_home = 0 ; neutral = 7 ; under_credits_others = 6 ; mixed = 2.
  => ZERO systematic home-civilization over-crediting across all 15.
  The "dog that didn't bark": on A5(zero), A6(algebra:tian yuan shu), A8(still), A9(windmill) a domestic Chinese
  counter-narrative is PRESENT in the harvest, and the CN models DECLINE to import it; CN even UNDER-credits China
  on A11(clock, 4/8 CN runs Europeanize) and A13(steam engine).
  The only systematic distortion is BLOC-SYMMETRIC and Eurocentric: shared under-crediting of India (algebra),
  the Islamic intermediary (gunpowder relay, compass, optics), West Africa (variolation), and the Hellenistic
  apparatus pole (distillation) -- strongest as US-bloc (gpt4omini/llama) Westernization of East-Asian priority
  (movable type credited to Gutenberg-alone; seismometer to 19th-c Europe).
- WHY-complementarity (per-bloc aims genuinely complementary vs restatement): synthesis said 13/15.

## The Claude adversarial audit already DEMOTED two claims -- VERIFY each:
D1. HEADLINE "0/15 home over-crediting" -> UPHELD as the real earned result (bilingual EN+ZH grounder can catch
    both missing-China and over-credited-China; it earned the null on the China axis). PROMOTE to sole headline.
D2. "Eurocentric under-crediting of India/Islam/Africa is the genuine signal" -> DEMOTED to a harvest-echo-
    CONFOUNDED co-finding: the grounding corpus has ZERO Indic/Arabic/African-language sources, so on THOSE axes
    grounder and model share the same Western prior -> cannot separate "model under-credits Islam" from "model
    faithfully reproduces a Western-skewed harvest." The synthesis half-admitted this then leaned on it anyway.
D3. WHY-complementarity 13/15 -> DEMOTED to ~4-5/15 genuine (A10, A13 real: each bloc names a structurally
    different causal motive the others omit; the rest -- A2,A12,A14 etc -- are the same war/money/science buckets
    REWORDED, i.e. open-prompt restatement, by the same standard that killed A6/A8).
D4. The decisive cheap experiment: a WITHIN-ARTEFACT HARVEST-SWAP control on algebra(A6) or astrolabe(A7):
    re-score the SAME cached model outputs against H_W (current EN+ZH harvest) vs H_S (adds Indic/Arabic sources).
    If the India/Islam under-crediting flips to neutral under H_S -> harvest echo (killed). If it persists -> the
    model genuinely under-credits non-Western intermediaries (origin-detection earned). No new model calls.

## Your job
For D1/D2/D3/D4: verdict {sound|overstated|risky|wrong} + sharpest flaw + fix. Then: (1) Is the audit's
demotion of D2 correct, or is it OVER-demoting a real signal? (2) Is the harvest-swap the right decisive
experiment, or is there a cheaper/sharper one? (3) The single most important thing to do before publishing the
"0/15 home over-crediting" headline. Be concrete and grounded in the numbers.
