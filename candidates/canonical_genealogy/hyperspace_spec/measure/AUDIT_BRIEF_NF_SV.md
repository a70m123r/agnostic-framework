# AUDIT BRIEF — NF (label x compute) + SV (same-task verdict control)

**Date:** 2026-06-19 | **For:** adversarial audit (codex CLI + Claude skeptics). REPRODUCE from the locked run
files, then REFUTE each claim. Skeptical; demote-not-kill. These are clarifying controls on the already-dual-
audited V10b/V11b; they will go into the canonical record, so pressure them hard.

## Instrument
reasoning_tokens on CORRECT calls; per-seed mean over reps; paired bootstrap median CI + exact sign test.
Models deepseek/qwen/gemini via OpenRouter, effort high. Reproduce:
`python v_nf_labelcompute.py --reanalyze --model M --seeds 60`, `python v_sv_verdict.py --reanalyze --model M --seeds 24`,
`python compare_3way.py`. Files: v_nf_run.*.jsonl (lock 354d7d5e), v_sv_run.*.jsonl (lock 9093531),
v10fs_run.*.jsonl (V10 prime), v10b_run.*.jsonl (V10b lookup).

## NF — separate label-novelty from compute (all cells select the IDENTICAL needle; finals given)
5 conds: TRIV_PLAIN, TRIV_NONCE (coin ZILP="last digit 3 or 7"), HARD_PLAIN (primality as a rule),
HARD_NONCE (coin FLONK=that rule), HARD_WORD (the word "prime").

| effect | deepseek | qwen | gemini |
|---|---|---|---|
| WORD shortcut HARD_PLAIN−HARD_WORD | +43 p=.003 | +185 p<.001 | +318 p=.006 |
| pure label TRIV_NONCE−TRIV_PLAIN | +35 p<.001 | +59 ns | −306 p=.001 |
| compute HARD_PLAIN−TRIV_PLAIN | +144 p<.001 | +113 ns | +488 p<.001 |

- **NF-C1:** the cached WORD "prime" is cheaper to apply than its explicit rule (robust, all 3, p<.05).
- **NF-C2:** coining a NOVEL name for a TRIVIAL rule does NOT robustly cost (deepseek +35 tiny, qwen null,
  gemini −306 negative) → so V11b's RENAMED +162/+263/+241 was the FLONK→prime translation (C2), not a
  universal pure label-binding tax. "Label-binding always costs" is DEMOTED.
- **NF-C3:** compute (hard vs trivial predicate) costs on deepseek+gemini, null on qwen.

ATTACK: (NF-C1) HARD_WORD is ~10 words SHORTER than HARD_PLAIN — is the shortcut just length? Recompute
controlling for prompt_words; check the all-completed sample. (NF-C2) deepseek's +35 — is it the +6-word
naming clause (TRIV_NONCE longer)? gemini's −306 — real "naming helps", or an accuracy/heavy-tail artifact
(gemini TRIV_PLAIN mean 1010 vs median 817 — skewed)? recompute on all-completed + Wilcoxon. (NF-C3) is qwen's
null real or its chronic noise?

## SV — application-free, SAME TASK (fixes V10b's task-switch confound)
6 conds mirror V10/V10b (F3..F1_L); every line pre-tagged [verdict: PASS/fail], task = "report the PASS
computation's value". compare_3way.py output (median rt):

| model | D_application = prime−verdict (range over conds) | D_frame F1_S−F2_DEINDEXED (app-free, same task) | size under verdict |
|---|---|---|---|
| deepseek | +524 → +7568 (all p<.001) | +113 (p<.001) | null/neg |
| qwen | +2572 → +10926 (F3 anomaly aside) | +372 (p<.001) | neg (p<.05) |
| gemini | +1480 → +11980 (all p<.001) | +405 (p=.023) | null |

- **SV-C1:** D_application is the dominant cost and GROWS with substrate size — cleanly isolated (same task,
  only predicate removed). Application-volume is the dominant reasoning cost.
- **SV-C2:** a real application-INDEPENDENT FRAME-ORIENTING cost SURVIVES clean application removal + same task
  (D_frame +113/+372/+405, all sig). V10b's lookup said ~0 — that was the FLOOR. SV rescues V10's orienting
  (refines DC37). 
- **SV-C3:** size axis null/neg under verdict → size = predicate-evaluation volume, not reading (3rd confirmation).
- **SV-C4:** verdict > lookup (esp gemini +669→+1920) → the prime-task ANSWER FORMAT adds cost beyond application.

ATTACK: (SV-C2 — THE SHARP ONE) F1_S−F2_DEINDEXED STILL confounds header-removal with SELECTOR POSITION
(F2 selector LEADING, F1_S selector TRAILING) — the exact V10 confound the selector-position 2x2 (V10c) was
meant to fix. So D_frame could be late-instruction RESCAN, not orienting. Is the "rescue" real or just the
unfixed position confound? (SV-C1) is verdict truly application-free, or does the model re-verify the PASS tags
(check reasoning traces)? survivorship? (SV-C4) real or accuracy-driven? qwen F3_FRAMED verdict=5248 is an
outlier — investigate.

## Return
Per claim: verdict {reproduced/refuted/overstated/underpowered} + recomputed number + sharpest flaw. Overall
waterline (what survives, what demotes). Single most important next control.
