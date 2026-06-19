[external review via OpenRouter model: google/gemini-2.5-pro]

**(1) STAGING VERDICT:** Staging-flaw-found.

**(2) RESIDUAL RISKS (UNCOVERED BY SELF-AUDIT):**
*   **Falsifier Behavior:** The self-audit does not verify that the model *processes* the substrate in the F0 (compute-free) conditions. It may simply `grep` for the `=>` token and output the number, making the `-47 (p=1.0)` delta an artifact of a search strategy, not a reflection of "orienting cost". The `reasoning_tokens` for F0 (541/590) are too high for a pure `grep`, but what do they contain?
*   **API Fidelity:** The claim that `reasoning_effort: 'high'` engages a specific, more costly "digestion" mode is unverified. If this string is a placebo on the back-end, the entire `reasoning_tokens` signal may be an incidental artifact of prompt length and basic processing, not deep reasoning.
*   **V11 Predicate Uniqueness:** The audit confirms the *needle* is identical, but not that the novel `digit-sum==S` predicate is *uniquely satisfied* by that needle. If a distractor chain item also satisfied the rule, the task is not a clean substitution.

**(3) ARE THE NULLS GENUINE OR ARTIFACTS?**
*   **V10 Headline Null (`F1_S - F2 = +289, NS`):** Likely genuine, but uninformative. It is dwarfed by the massive, highly significant SIZE axis cost (`F1_M-F1_S = +2025`, `F1_L-F1_M = +2030`). This suggests `reasoning_tokens` is dominated by a linear reading-cost of the substrate, making the effect of a minor framing change undetectable. The null is genuine because the signal is buried, not because the effect is absent.
*   **V11 Headline Null (`NOVEL - NAMED_DEF = -70, NS`):** A manufactured artifact. The negative sign (Novel is cheaper) demonstrates the design failed to isolate the `de-amortization` variable. The result is confounded by predicate-difficulty, as the operator correctly demoted. This is not a genuine null result for the hypothesis; it is an invalid experiment.
*   **V10 Falsifier Null (`F0_DISSOLVED - F0_DEINDEXED = -47, NS`):** Potentially an artifact. If the model's strategy for F0 is `find "=>"`, then the location of the substrate (deindexed vs. dissolved) is irrelevant. The cost is constant, producing a null result by design flaw, not by measuring a zero "orienting cost".

**(4) ARE THE DEMOTIONS HONESTLY REASONED?**
*   **(A) V10 Demotion:** Mostly honest, but potentially over-confident. The data absolutely supports a "reading-volume" cost as the dominant factor. However, concluding the falsifier's null result proves "orienting is free" is premature; it ignores the alternative explanation that the falsifier task was circumvented (item 3, V10 Falsifier Null).
*   **(B) V11 Demotion:** Yes, entirely honest and correct. This is a textbook case of identifying an uncontrolled-for variable (predicate-difficulty) that invalidates the experimental design. The operator's reasoning here is sound.

**(5) THE SINGLE MOST IMPORTANT NEXT CONTROL:**
An **"Irrelevant Task"** control. Re-run condition `F1_S` (dissolved task, small substrate) but change the final instruction to a task that requires scanning the substrate for non-arithmetic information (e.g., "Report the number of lines containing the word 'is'"). This measures the cost of a full scan *without* `compute-on-the-path`. The delta between `F1_S(prime_task) - F1_S(irrelevant_task)` would isolate the cost of distributed computation, cleanly testing the core V10 hypothesis while controlling for the `+2025` reading-cost confound.