# V10b + V11b — cross-model audited: predicate-APPLICATION is the cost; reading-volume DEMOTED; de-amortization tax robust

**Date:** 2026-06-19 | The two controls the V10/V11 auditors demanded, built by Pav's gemini/agy Deep-Think
session, run across the cheap cross-model spectrum (deepseek/qwen/gemini via OpenRouter), then put through
**two independent subscription audits** — a Claude 6-skeptic adversarial workflow + a codex/GPT external pass.
Both audits independently re-derived every headline from the locked run files; **all numbers reproduce exactly.**
Params + slugs: [CROSS_MODEL_RUNCARD.md](CROSS_MODEL_RUNCARD.md). Demote-not-kill.

## The two instruments
- **V11b** (`v11b_matched.py`, lock `d394534f`): de-amortization with compute MATCHED. Swap `prime` for a novel
  predicate **WURF** (n>=2, not even unless 2, and for d in {3,5,7,11,13,17}: n%d != 1) that selects the
  IDENTICAL needle (the unique prime is forced to also be the unique WURF). 6 conds incl RENAMED_PRIME
  (prime->FLONK nonce, SAME concept) and F0 verdict-given falsifier. 28 seeds x 4 reps.
- **V10b** (`v10b_irrelevant.py`, lock `1c0071d0`): irrelevant-task LOOKUP. Same V10 substrate, but the task is
  "report the value variable X is initialized to" — zero arithmetic, zero predicate. 6 frame conds. 24 seeds x 4.

## Findings ABOVE the waterline (both audits concur — bankable)

**1. The camera dissociates LOCATING from APPLYING by 1-2 orders of magnitude.** Cross-experiment, same
substrate, median reasoning_tokens, PRIME-task (V10) vs LOOKUP-task (V10b):

| model | F1_S prime/lookup | F1_M | F1_L | D_compute ratio |
|---|---|---|---|---|
| deepseek | 1680 / 84 | 4342 / 103 | 8102 / 121 | 20x -> 67x |
| gemini | 6274 / 173 | 11944 / 168 | 12798 / 166 | 36x -> 77x |
| qwen | 4805 / 568 | 7629 / 529 | 10469 / 498 | 8.5x -> 21x |

Survivorship makes this CONSERVATIVE (gemini prime accuracy collapses with size 52->49->39/56 — hardest items
censored out — biasing the prime cost DOWN). The reasoning the camera reads is overwhelmingly predicate
APPLICATION, not search/reading.

**2. An un-amortized concept costs more reasoning than the same-difficulty amortized one (V11 RESCUED).**
NOVEL_RULE - NAMED_DEF = **+307.6 / +836.1 / +2150.8** (deepseek/qwen/gemini), p<.001 all, n=28. Needle
isomorphic; survives on all-completed (gemini +2008). Compute residual runs AGAINST the effect (prime
trial-division is MORE steps than WURF: 11 vs 7 on the needle) -> conservative. V11's old NEGATIVE was 100% the
digit-sum predicate-difficulty artifact.

**3. A pure-label de-amortization (nonce-binding) cost exists on >=2/3 models.** RENAMED_PRIME - NAMED_DEF =
+161.9 / +262.6 / +241.0 (sign-p .013/.004/.036). deepseek+qwen robust (Wilcoxon p=.002). Renaming primality to
a nonce (FLONK) costs reasoning with the REQUIRED computation byte-identical.

**4. V10's "universal reading-volume cost" is predicate-EVALUATION volume, not reading.** Under lookup, 5x more
substrate adds ~nothing (deepseek +47, gemini -7, qwen -70 across F1_S->F1_L); under prime the SAME bytes scale
+6400/+6500/+5660. The size cost is the number of candidates evaluated, not bytes read.

## DEMOTIONS — dated dead-children (labels that oversold; both audits flagged each)

- **DC-34 "compute-matched de-amortization of MEANING"** -> **"novel/nonce predicate-APPLICATION overhead."**
  (codex C1 + Claude C1/C2.) WURF compute-match is not *proven* (operation-count direction depends on the
  assumed model algorithm); "de-amortize an un-cached concept" and "apply a novel rule explicitly" are not
  separable in principle. The effect is robust; the *mechanism label* "pure meaning de-amortization" is not earned.
- **DC-35 "the tax is concept-APPLICATION, not def-holding"** -> **"application-DOMINANT; a real def-comprehension
  residual survives."** (both C3.) deepseek's F0 falsifier (+78, p=.013) survives with application removed; trace
  inspection shows it is the cost of reading/orienting around the unfamiliar ZILP def (94/112 novel traces engage
  the def vs 22/112 named, ~2x rt). F0 localizes MOST (53%/4%/16% of headline) but not ALL of the tax to
  application. gemini's "vanish" is underpowered (+101 below its MDE ~274).
- **DC-36 "lookup is FLAT / reading is free"** -> **"lookup is NEAR-FLOOR, not zero."** (both C4/C5.) deepseek
  lookup has a *significant* +47 climb F1_S->F1_L (p=.023), ~0.7% of the compute slope. The 2-orders dissociation
  is unscathed; "literally flat / reading is free" is not — the floor is not excluded.
- **DC-37 "V10's compute-free frame-cost WAS primality-application"** -> **"it disappears under a DIFFERENT
  application-free task (lookup); not a clean subtraction."** (both C6.) V10-F0 runs an evaluate-ALL-6 primality
  sweep; lookup reads ONE named line — so the contrast confounds 'predicate' with 'process-6-vs-1'. Holds only for
  gemini (deepseek/qwen had small F0 residuals; qwen's lookup residual +142 p=.007 is itself positive). gemini's
  gap is partly a dissolution-triggered TRUST-flip (re-derive when dissolved) — itself an orienting phenomenon.

**Invalid-as-designed: none.** (V11 itself remains demoted; V11b supersedes it.)

## Cross-model convergence (the real A-)
Claude (Opus) and codex (GPT-5.5) agree on all six verdicts (modulo C1/C5 verdict-vs-label wording). Independent
re-derivation on two model families = strong external validation of both the numbers AND the demotions.
Audit docs: `session_arc/claude_v10b_v11b_audit.md`, `session_arc/codex_v10b_v11b_audit.md`.

## NEXT CONTROLS — each audit named one; they are COMPLEMENTARY (different confounds)
- **NF — NOVEL_FAMILIAR (Claude, for the V11b de-amortization half):** a novel NAME bound to a trivial CACHED
  predicate (e.g. ZILP = "ends in 3 or 7"), token-matched, n>=60. Independently varies label-novelty vs
  uncached-compute — the one axis every contested V11b verdict (C1/C2/C3) turns on — and powers gemini's nulls.
- **SV — same-task application-free VERDICT control (codex, for the V10/V10b frame-application half):** keep the
  "report the value of the unique PASS computation" task, pre-give PASS/fail verdicts for prime/FLONK/WURF on EVERY
  line, vary frame + substrate size, and add calibrated distractor load to lift reasoning ABOVE floor. Removes
  application WITHOUT switching to name-lookup (fixes the C6 confound) AND beats the floor (fixes C4).

## Cost / provenance
Whole V10b+V11b spectrum ~$2-3 OpenRouter (incl a ~$1 double-spend from a script-overwrite collision — V11b ran
twice concurrently; atomic deterministic writes meant zero corruption, all files validated 672/576 rec full
coverage). Both audits = $0 (Claude workflow = Max sub; codex = ChatGPT sub; codex needed `-c service_tier=fast`
to dodge a stale config). gemini/agy Deep-Think built the two controls (Ultra sub).
