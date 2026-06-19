**Verdict: overstated.** The raw V10c artifacts reproduce the reported result, but the mechanism claim should be demoted from "orienting, not late-instruction rescan" to "a semantic first-line wrapper cost, with orienting favored but not isolated."

I recomputed directly from `measure/v10c_run.{deepseek,qwen,gemini}.jsonl` with plain Python: group by model, seed, and cell; average `reasoning_tokens` over correct reps within each seed/cell; then compute paired seed deltas and an exact two-sided sign test. The lock also verifies: `measure/v10c_labels.jsonl` hashes to `b15c6c99944eb475c38893bbc0d8f6b37e75f98e5034bc5b02100723a947f565`, matching `measure/v10c_labels.LOCK`.

One bookkeeping correction: the four cells are length-matched within each seed, but the prompts are not all 810 words. The run records range from 727 to 944 `prompt_words`; there are no within-seed cell mismatches.

| model | POSITION median | POSITION mean | sign | p | HEADER median | HEADER mean | sign | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek | +3.6 | +8.8 | 22+/18- | .636 | +7.9 | +3.2 | 31+/9- | .001 |
| qwen | -22.9 | -1.8 | 19+/21- | .875 | +92.2 | +106.4 | 31+/9- | .001 |
| gemini | +41.8 | +78.2 | 26+/14- | .081 | +105.6 | +136.9 | 29+/11- | .006 |

The reported headline deltas reproduce exactly as the median paired deltas used by the local `paired()` helper. If the claim is worded as arithmetic means, it is imprecise; the arithmetic means are shown separately above. The sign-test p-values are unchanged because they depend only on paired signs.

Accuracy is not a useful confound here. DeepSeek and Qwen are 640/640 correct. Gemini has only four misses: H_LEAD 158/160, H_TRAIL 159/160, N_LEAD 160/160, N_TRAIL 159/160. Including all non-exhausted Gemini token counts instead of correct-only counts leaves the result effectively unchanged: POSITION median +37.1, p=.081; HEADER median +105.6, p=.006.

The sharpest flaw is the "HEADER absent" implementation. It is not true absence; it is the active seven-word sentence "Several notes were filed during the cycle." That sentence can itself set a document frame, a notes/files/cycle frame, or simply add a first-line distraction before the selector/body. Therefore the H/N main effect currently identifies that the first-line semantic frame matters, but it does not uniquely identify "header helps" over "neutral line hurts."

There is evidence the neutral line is not inert. In model rationales, DeepSeek and Qwen mention neutral-line terms such as "notes", "filed", or "cycle" in N cells, while H cells often mention "system log" or "log". That does not refute orienting - Gemini shows the same large H/N effect with little explicit neutral-term reuse - but it prevents the strong causal wording. The current result is consistent with header orienting, neutral confusion, or both.

Gemini POSITION is also not a clean late-rescan win. It is directionally coherent inside Gemini: both header levels show positive trailing-leading medians, and the aggregate sign is 26+/14-, p=.081. But the spread is large, the interaction is null, and the other two models are position-null. Treat Gemini position as a possible underpowered Gemini-specific position cost, not as established and not as a reason to overturn the header result.

Single next control: add a TRUE_ABSENT / NULL_PAD bridge to V10c, keeping the same bodies and crossing selector position as before. The decisive design is H vs N vs Z, where Z has no semantic first sentence and any required length padding is relocated to an identical inert footer or otherwise balanced across all arms. If Z tracks N while H is lower, orienting survives. If Z tracks H while N is higher, the old result was neutral-line-hurts. If Z sits between them, both mechanisms contribute.

Bottom line: reproduce the data; demote the claim. V10c kills the strong "late-instruction rescan is the main explanation" story across the three-model panel, but it has not yet isolated orienting from an active neutral-pad artifact.
