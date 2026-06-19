# Experimental Design Critique & Controls for the Latent Camera Project

**Date:** 2026-06-19  
**Status:** Implemented, verified, and locked.  
**Related files:**
*   V10b Irrelevant Task: [v10b_irrelevant.py](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10b_irrelevant.py) (Lock: `1c0071d0b47401d1`)
*   V11b Compute-Matched: [v11b_matched.py](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v11b_matched.py) (Lock: `d394534f3512141a`)
*   V10 Frame-Strip: [v10_framestrip.py](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10_framestrip.py)
*   V11 De-amortization: [v11_deamortize.py](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v11_deamortize.py)
*   Audits: [codex_v10v11_audit.md](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/session_arc/codex_v10v11_audit.md) and [gemini_or_v10v11_audit.md](file:///D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/session_arc/gemini_or_v10v11_audit.md)

---

## Executive Verdict & Waterline Summary

A rigorous audit of the V10 and V11 rungs reveals that while the measurement instrument is sound (capturing `reasoning_tokens` on correct responses), the experimental controls suffered from critical structural confounds:
1.  **V10's F0 Falsifier** was buggy (unevaluated filler arithmetic lines), meaning we did not have a clean "compute-free" baseline.
2.  **V11's Headline Result** was confounded by predicate-difficulty: `digit-sum == S` ($O(1)$ operations) is intrinsically cheaper than trial-division primality ($O(\sqrt{N})$ operations), swamping any de-amortization signal.

This document details the critiques, improved designs, and pre-registered kill-criteria for **V10b (Irrelevant-Task)** and **V11b (Compute-Matched Predicate)**.

---

## 1. V10b — The Irrelevant-Task Control

**Objective:** Isolate the reasoning tax of distributed compute (performing calculations on the path) from search/reading volume.

### (a) The Sharpest Residual Flaw of the Proposed V10b
The proposed irrelevant task ("count how many lines contain the word 'is'") is a **cognitive mismatch**. It is shallow (regex/token-based) and targets prose lines. The model can completely skip parsing or looking at the equations. 
This introduces a **scanning depth confound**: the delta $rt(\text{prime-task}) - rt(\text{scan-task})$ measures *both* the arithmetic execution *and* the semantic parsing of mathematical syntax.

### (b) Cleanest Concrete Buildable Design
We replace the prose-scanning task with a **Variable-Initial Lookup Task**. The model must scan the same equations and locate a specific variable name, but perform zero arithmetic steps.

*   **Task Instruction:**
    > "Below are several computations. Report the value that variable `{VAR}` is initialized to on its first assignment. Output ONLY that integer."
*   **Prompt Example:**
    If the substrate contains:
    `echo = 412; echo = (echo + 10) % 997; ...`
    The model must locate the variable `echo` and report `412`.
*   **Why it works:**
    *   **Identical Substrate & Length:** Uses the exact same `F1_S` dissolved substrate.
    *   **Attentional Alignment:** The model must still segment the equations, scan variable names, and ignore prose.
    *   **Zero Arithmetic:** No multi-step modular arithmetic or trial division is performed.
*   **Exact Reasoning Token Contrast:**
    $$D_{\text{compute}} = rt(F1\_S, \text{prime-task}) - rt(F1\_S, \text{variable-lookup-task})$$

### (c) Pre-registered Kill-Criteria
*   **Demote to NULL if:** $D_{\text{compute}} \le 0$ or is statistically non-significant ($p > 0.05$). This indicates that executing arithmetic on the search path does not impose a distinct token cost beyond the search/reading volume itself.
*   **Confirm if:** $D_{\text{compute}} > 0$ with high significance ($p < 0.01$) and remains stable as the substrate scales ($F1\_M$, $F1\_L$).

---

## 2. V11b — The Compute-Matched Novel Predicate

**Objective:** Isolate concept de-amortization (un-amortized concept in working memory) from predicate execution difficulty.

### (a) The Sharpest Residual Flaw of the Proposed V11b
Primality checking for $n \le 997$ requires up to 11 trial divisions ($\le \sqrt{997} \approx 31.5$). The original novel predicate `digit-sum == S` required only two additions and a comparison. The negative delta was a structural artifact of this complexity mismatch.

### (b) Cleanest Concrete Buildable Design
We define a novel predicate **`WURF`** (Coprime-to-D / Non-Remainder Rule) that mirrors the exact execution loop of trial division but lacks any pre-paid training concept representation.

*   **The Predicate Definition (`WURF`):**
    > "Call a number $n$ a `WURF` iff $n \ge 2$, and for every divisor $d$ in the set $D = \{3, 5, 7, 11, 13, 17\}$, the remainder of $n$ divided by $d$ is NOT 1 (unless $n = d+1$)."
*   **Why it matches primality:**
    *   It requires checking 6 specific test divisors.
    *   For a valid needle, the model must run the modulo operation and check the remainder for all 6 divisors (just like a prime check runs to completion).
    *   For non-needles, the test can terminate early (just like composite checks do).
    *   The arithmetic operations (modulo/division) are identical.
*   **Isomorphism & Generator Implementation:**
    In `_make(seed)`, we filter seeds to ensure that the unique prime needle is also the unique final that satisfies the `WURF` condition.
*   **Exact Reasoning Token Contrast:**
    $$D_{\text{de-amort}} = rt(\text{NOVEL\_RULE}) - rt(\text{NAMED\_DEF})$$

### (c) Pre-registered Kill-Criteria
*   **Demote to NULL if:** $D_{\text{de-amort}} \le 0$ or is statistically non-significant ($p > 0.05$) after matching the trial-division complexity. This would prove that once arithmetic execution difficulty is matched, holding and applying an un-amortized concept in working memory carries no additional reasoning cost.
*   **Confirm if:** $D_{\text{de-amort}} > 0$ with $p < 0.05$, validating that de-amortized meaning carries a distinct cognitive tax.

---

## 3. Prioritization & Value Assessment

We recommend building and running **V11b (Compute-Matched Predicate) first**.

*   **Rationale:** The V11 null result was a direct consequence of a **broken experimental design** (confounded by predicate difficulty). We currently have zero valid data on de-amortization. 
*   In contrast, V10's null result, while swamped by reading volume, is directionally valid (reading cost scales linearly). Fixing V11b rescues the core hypothesis of the de-amortization rung, whereas V10b simply refines the partition of an already partially-quantified effect.
