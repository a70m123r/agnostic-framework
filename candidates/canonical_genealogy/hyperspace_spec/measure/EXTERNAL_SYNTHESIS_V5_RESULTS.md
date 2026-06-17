# External pass — codex + gemini on V5_RESULTS.md (2026-06-17)

Cross-model A− on the V5-LITE PROMOTION. Raw: `../session_arc/codex_v5results_review.md` (gpt-5.5,
xhigh), `../session_arc/gemini_v5results_review.md`. **They converged**: the result is real and the
matched-pair design is sound, but "serial DEPTH" overclaims the mechanism. codex = "overclaims-remain";
gemini = "Promotion Validated but Limited." Demote-not-kill.

## What both AFFIRM
- The matched-pair design is technically sound and **eliminates the literal-transcription + memory-load
  confounds** (gemini: "selftest-gate ensures within each pair word-count and op-multiset are identical").
- **DEEP > WIDE is statistically robust** (+38.5 median tok, 15/16, sign p=0.0003) and **refutes a
  "one scratchpad line per printed op" account** — the V4 pure-transcription reading is dead in its
  literal form.
- The pre-registered SHA-lock + 100% solve prevent p-hacking; the exact paired sign test is the
  load-bearing inference at n=16 (bootstrap CI is descriptive, Efron lineage).

## The residual confounds that force the demotion (both)
1. **Serial-carry ≡ span (the killer, both).** In DEEP one value is transformed K times, so "carry length"
   (cumulative single-variable history) is collinear with critical-path span. Can't separate *logical
   depth* from *carry length*. gemini: "a WIDE program with a single long serial chain would likely show
   the same surcharge → the effect is about ANY long dependency, not deep-vs-wide structure per se."
2. **Routing / self-update (codex).** WIDE updates are `rX = (rX op c)` (self-read, syntactically
   compressible — a recognizable accumulator); DEEP are `rX = (rY op c)` (cross-read, pointer-following).
   Same line count, different parsing burden → the gap may be a **WIDE discount**, not a **DEEP surcharge**
   (mechanistically different claims).
3. **`m`-confound (both)** — the two cells vary `m` and `k` together; WIDE's parallel-bookkeeping cost
   rises with `m`, plausibly masking a depth slope → the ~constant Δ (the "plateau") is not evidence
   against a slope, just uninformative about it.
4. **Nominal ≠ cognitive live-vars (codex)** — both name `m` registers but optimal internal state differs.
5. **Intermediate-value residue (codex actually recomputed oracle intermediates):** DEEP has a *small*
   median excess in assigned-value / pre-mod digits — far too small to explain +38.5 and weakly correlated
   with the deltas, but it keeps a *value-level* (not line-level) transcription account alive.
6. **Arm order (codex, minor):** the runner emits DEEP then WIDE; calls are stateless so low risk, but
   structure should be counterbalanced for a promotion-grade claim.

## Demotions to fold (the converged wording)
- "genuine serial-DEPTH surcharge beyond work/transcription/memory-load" → **"a robust DEEP>WIDE STRUCTURE
  contrast at matched coarse work / length / line / live-var counts; consistent with a serial-dependency
  cost, but not yet isolated from routing, self-update compression, carry-length, or value-level
  transcription."**
- "only critical-path span differs" → **"the matched fields and op-multiset are equal; source-register
  routing and algorithmic affordances still differ."**
- "refutes pure transcription" → **"refutes LITERAL line/op-count transcription; does NOT refute
  value-level or pattern-compression transcription."**
- "not depth-proportional" → **"no clean dose-response evidence"** (the `m`-confounded plateau neither
  supports nor falsifies a depth slope).

## Next move — V5-FULL, sharpened (both converge)
1. **Fix `m`, sweep span via `k`** — let a slope emerge with width-complexity held constant.
2. **A "long-carry WIDE" control** (one long chain + several short ones at the same width) — separates
   "cost of *any* long serial path" from "deep-vs-wide structure," i.e. carry-length from span.
3. **Counterbalance arm order + add an intermediate-digit / pre-mod-magnitude covariate** (the cheap guard
   before the grid).
4. **Match self-vs-cross update counts** where possible (neutralize the routing confound).
5. **Cross-model** (is the surcharge a reasoning-model property or a gpt-5.5@high quirk?). If a grid over
   cells/tiers/models: predeclare the primary contrast, treat the rest as exploratory or apply
   Benjamini-Hochberg.

## Net
V5-LITE is a real, robust, pre-registered result that **kills the literal-transcription reading** of V4:
gpt-5.5 spends materially more reasoning tokens on a long serial / cross-routed dependency than on a
matched parallel one. But the **mechanism is one notch broader than "depth"** — "cost of a long serial
dependency," with carry-length, routing, and `m` not yet separated. V5-FULL (fixed-`m` span ladder +
long-carry-WIDE control + counterbalancing) is the clean isolator.
