# External pass — codex + gemini on V9d (2026-06-18): the override SURVIVES the valve; "paradox refuted" and "unpaid tax" do not

Cross-model A- on the 2-prime release valve. Both re-derived from `v9d_run.jsonl` and **converged**: verdict
**overclaims-remain** (both). Raw: `../session_arc/codex_v9d_review.md`, `../session_arc/gemini_v9d_review.md`.
Cite-don't-coin.

## What SURVIVES (both confirm, sound)
- **The override is REAL and survives the release valve: override_2P = FALSE_NEG_2P − NEUTRAL_2P = +1093
  reasoning tokens (median seed-delta, 27/27 positive, p≈1.5e-8).** A heavy override tax remains even when a
  cheap escape prime is available → V9c's cost is **not** a 0-solution-only artifact.
- **Escape ENABLES capture — and it is genuine hint-obedience, not size-confusion.** FALSE_NEG_2P valve-take
  rate 10/108 = 9.3% (Wilson [5.1%,16.2%]); the model took the smaller prime **0/112 times in NEUTRAL_2P**
  (Fisher p=6.5e-4). It violates the "LARGEST" instruction *only* when pushed by the false negative hint.
- **Infra failures are UNBIASED (gemini verified):** the 37 exhausted calls clustered entirely in seeds
  27/28/29 across **all** conditions (incl. 16 NEUTRAL failures) — a temporal API rate-limit block, not a
  difficulty-selective censoring of hard FALSE_NEG calls. The cost deltas (computed on completed seeds) are
  not biased; they rest on 27 seeds, not 30.

## What does NOT survive
- **"gemini's paradox hypothesis is largely refuted" — OVERSTATED (both).** The paradox component
  (override_1P − override_2P) is **+373 (median of per-seed means) / +539 (median of per-seed medians)**,
  p=0.25, CI **[−56,+999]**. That is ~25-34% of the override and is *underpowered*, not zero — "failing to
  reject on a wide CI does not mean the effect is zero" (gemini). Honest: the **0-solution-ONLY** explanation
  is refuted; a several-hundred-token paradox contribution remains plausible.
- **"Capture = the unpaid tax (n=10)" — DROP ENTIRELY (gemini).** 36 of 98 *correct* FALSE_NEG_2P calls also
  used 511/512 tokens — ~512 is simply the modal early-exit reasoning bucket for this task, *not* uniquely
  predictive of capture. codex concurs (low-reasoning threshold Fisher p=0.085, not diagnostic). The V9c n=1
  version was rightly dismissed; the n=10 version is a base-rate illusion. Killed.
- **Stat-label error (codex):** the doc's "+373 mean / +539 median" mislabels `paired()`, which reports a
  median. +373 = median across seeds of per-seed-MEAN components; +539 = median across seeds of
  per-seed-MEDIAN components. Both are medians-across-seeds.
- **Salience remains ACTIVE (both):** FALSE_NEG_2P names the answer B; NEUTRAL names nothing. So +1093 is a
  **"false elimination of the named answer, with a release valve, among resisters"** — not a generic,
  salience-free override.

## DEMOTE (demote-not-kill)
- "gemini's paradox hypothesis is largely refuted" -> **"the 0-solution-ONLY explanation is refuted (a real
  +1093 override survives the escape); the paradox component (+373/+539, CI[−56,+999], p=0.25) is a
  statistically ambiguous ~25% inflation — underpowered, not zero."**
- "Capture = the unpaid tax (n=10)" -> **DROPPED: ~512 is the modal reasoning bucket for correct calls too
  (36/98); not capture-predictive.**
- "9% obeyed the false hint" -> **"10/108 chose the smaller prime ONLY under FALSE_NEG (0/112 in NEUTRAL,
  p=6.5e-4) — hint-induced valve capture; output-only cannot prove trace-level obedience vs shortcut-stop."**
- "+1093 = the override" -> **"+1093 = the cost of a false elimination of the NAMED answer (salience still
  bundled), with a release valve, among resisters; lower-bound-ish (3 calls saturate xhigh ~7168)."**

## KEEP (corroborated, narrow)
1. A false elimination of the answer imposes a **real, large override tax that survives a cheap escape**
   (+1093, p<1e-7) — V9c's cost is not mostly a 0-solution artifact.
2. **An escape route is what enables capture** (9.3% vs 0% neutral, p=6.5e-4): the model resists ~perfectly
   when there is nowhere valid to flee, and a plausible wrong-but-prime alternative is what lets the lie land.

## The decisive NEXT experiment (both converge)
**V9e — VERIFY_ALL same-named-chain.** Force the model to output every chain's evaluated final + prime flag +
the largest-prime name/value BEFORE the answer (kills the search shortcut AND yields a checkable trace). Then
compare hints naming the **same** chain B: TRUE_POS_B ("answer IS B") vs FALSE_NEG_B ("answer is NOT B"), plus
TRUE_NEG_A (names the smaller prime) as a control. Decisive contrast **FALSE_NEG_B − TRUE_POS_B on
trace-correct records only** — same target, opposite truth → isolates *pure falsehood* free of salience and
shortcut. Counterbalance prompt order; serial/retry until 0 exhausted.

## Merged verdict
V9d **partially rehabilitates V9c**: the override is real and survives a release valve (+1093, p<1e-7), and it
adds the clean **escape-enables-capture** finding (9.3% hint-obedience, 0% neutral). It **demotes** "paradox
largely refuted" (→ 0-solution-only refuted; paradox underpowered) and **kills** "capture = unpaid tax"
(base-rate illusion). The **salience** confound is the last one standing — **V9e (VERIFY_ALL same-named-chain)
is the convergent endpoint** that would isolate pure falsehood. Bucket V9d **corroborated** for the two narrow
KEEPs, carrying the demotions as dead-children.
