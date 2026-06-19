**STAGING VERDICT: staging-flaw-found.** V11 is staged as claimed; V10 has a real F0 construction bug: only the 6 task chains get `=> final`, while filler arithmetic lines remain unevaluated, so the F0 falsifier is not fully compute-free.

**Measurement**
- PASS: [providers.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/providers.py:37) sends `deepseek/deepseek-v4-flash`, `reasoning: {"effort": "high"}`, `max_tokens=16000`.
- PASS: reasoning tokens read from `usage.completion_tokens_details.reasoning_tokens` at [providers.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/providers.py:57).
- Raw: slug is `deepseek/deepseek-v4-flash` in 784/784 records; `reasoning_tokens` non-null in 784/784; `reasoning` nonempty in 784/784.
- MINOR FAIL: `content` is not always just one integer. Integer-only: V10 437/448, V11 329/336. But `_last_int(content)` equals saved `got` in 784/784, and `correct == (got == truth)` in 784/784. The long working is in `reasoning`, not `content`.

**V10 Construction**
- PASS: raw records match locked labels for `item_id/cond/seed/truth/compute_free`; prompt word counts match locked prompt text.
- PASS: locked-label digest matches lock; raw run uses seed subset 0-13.
- PASS: needle hash byte-identical across `F3/FP/F2/F1_*`; F0 pair hash also equal.
- PASS: exactly one prime-final arithmetic line in every locked prompt.
- PASS: body text is byte-identical across `FP/F2/F1_S`; F0 body text also byte-identical across `F0_DEINDEXED/F0_DISSOLVED`.
- PASS length: raw median prompt tokens `FP=1356`, `F2=1343`, `F1_S=1335`; size axis deliberate: `F1_M=2873`, `F1_L=5347`; F0 pair `1380/1372`.
- FAIL F0 compute-free: in locked V10 F0 prompts, arithmetic lines per prompt median 17.5; only 6 have `=>`; median 11.5 filler arithmetic lines lack final values. Cause: `_substrate()` emits filler as `_line(...)`, while only `task_lines` use `_line0(...)` at [v10_framestrip.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10_framestrip.py:107) and [v10_framestrip.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10_framestrip.py:140).

**V11 Construction**
- PASS: prime and digit-sum predicates select the same unique needle for every locked seed.
- PASS: compute-arm bodies are byte-identical across `NAMED_BARE/NAMED_DEF/RENAMED_PRIME/NOVEL_RULE`.
- PASS: F0 bodies are byte-identical; 6/6 lines have `=>` and verdicts; exactly one PASS in both arms.
- PASS length: definition word counts `22/22/19`; raw median prompt tokens `NAMED_DEF=437`, `RENAMED=439`, `NOVEL=438`; F0 pair `511/511`.

**Validity / Censoring**
- V10 accuracy: 444/448. Bad records: `F0_DEINDEXED` 1, `F1_S` 1, `F1_M` 1, `F1_L` 1. Empty content: 3. `finish="error"`: 2.
- V11 accuracy: 336/336. No empty content, no errors.
- No `finish_reason=length`. Correct calls near 16k completion tokens: 0. Max correct completion: V10 12423, V11 2543. One V10 wrong call hit 16771 tokens, excluded.

**Re-Derived Deltas**
V10, per-seed mean over correct reps, n=14:
- `F1_S - F2`: `+288.8`, p=.180.
- `F0_DISSOLVED - F0_DEINDEXED`: `-46.6`, p=1.000, signs 7/7.
- `F1_M - F1_S`: `+2025.3`, p<.001.
- `F1_L - F1_M`: `+2029.6`, p<.001.
- `FP - F3`: `+1346.0`, p<.001.
- `F2 - FP`: `-390.3`, p=.424.

V11:
- `NOVEL_RULE - NAMED_DEF`: `-69.6`, p=.180, signs 4/10.
- `RENAMED_PRIME - NAMED_DEF`: `+54.4`, p=.424.
- `NAMED_DEF - NAMED_BARE`: `+174.4`, p=.057.
- `F0_NOVEL_RULE - F0_NAMED_DEF`: `+48.3`, p=.791.

**Null Interpretation**
- V10 demotion is directionally supported by the size curve, but the F0 “compute removed” falsifier is overclaimed. The bug is common-mode between F0 arms, so it probably adds noise/base cost rather than manufacturing a directional null, but the clean falsifier has not actually been run.
- V11 demotion is honest. I found no staging artifact that explains the negative headline; digit-sum application is plausibly easier than primality here, so predicate difficulty confounds de-amortization.

**Most Important Fix**
Fix V10 F0: render every arithmetic substrate line with `=> final` or use a full verdict table, then add a selftest asserting zero F0 arithmetic lines without `=>` and rerun the F0 pair before fanning to other models.
