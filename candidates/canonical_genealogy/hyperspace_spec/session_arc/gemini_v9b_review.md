One-line VERDICT: **overclaims-remain**

### Residual Issues (The real confounds, ranked)

1.  **Confounded "Pure Override" Baseline:** The claim that `FALSE_HINT - TRUE_HINT = +438` isolates override cost is mathematically flawed. `TRUE_HINT` hands the model the needle, reducing the search space from ~3.5 chains evaluated (NEUTRAL) to exactly 1. `FALSE_HINT` directs the model to a lure, requiring evaluation of the lure (1) plus the remaining chains until prime found (avg 2.5) = ~3.5 to 4 chains. The delta +438 conflates the cognitive "override" tax with the ~2.5-chain (~150 token) search-space reduction of the truth condition. The only valid "override" signal is `FALSE_HINT - NEUTRAL` (+302 median).
2.  **Attacker Ratio Inflation:** The 1:42 ratio (+10 in -> +418 hidden) is built on the confounded `FALSE - TRUE` delta. In a real-world scenario, an attacker adds a hint to a clean prompt (`NEUTRAL`). The actual cost delta is `FALSE - NEUTRAL` (+302 median), yielding a ratio of **~1:30**. It remains a massive asymmetry, but the reported number is a baseline artifact.
3.  **Capture Inversion is Noise-Driven Speculation:** The "surprise" that higher budget (`xhigh`) captures more than budget-starved (`high`) (4.9% vs 1.8%, p=0.112) is based on only 11 vs 4 events. Attributing this to "rationalization of a plausible lure" is a fascinating but entirely un-validated hypothesis.

### DEMOTIONS (Demote-not-kill)

*   **"verify-and-override is IDENTIFIED ... pure override = +438"** → **DEMOTE TO:** "A significant override cost is measured against the NEUTRAL baseline (~+300 tokens); the `FALSE - TRUE` comparison (+438) is rejected as a pure isolation due to search-space reduction in the truth condition."
*   **"Attacker ratio ... 1:42"** → **DEMOTE TO:** "The trapdoor ratio is measured at ~1:30 (10 input tokens drive ~300 hidden reasoning tokens of override tax relative to a clean baseline)."
*   **"rationalize a plausible lure ... opposite of starvation"** → **DEMOTE TO:** "The predicted budget-exhaustion break point was not observed; capture rate differences between budget tiers are statistically insignificant (p=0.11), leaving the 'rationalization' hypothesis purely speculative."

### The Single Most Decisive NEXT Experiment

**TRUE-but-useless vs. FALSE-but-useless control:** Use hints that do NOT reduce the search space, e.g., "Hint: the answer is NOT named <lure>" (TRUE) vs. "Hint: the answer is NOT named <needle>" (FALSE). Since both require searching the rest of the chains, the delta cleanly isolates the *truth/falsehood* of the prompt-guidance without the search-space confound.

### Relevant Arxiv IDs
*   **2502.02542 (OverThink):** The definitive citation for reasoning-token slowdown/availability attacks.
*   **2310.13548 (Sycophancy):** Essential for the baseline hint-following (sycophancy) vs. override trade-off.
