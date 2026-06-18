**VERDICT: overclaims-remain.** Core numeric survival is real; mechanism wording is too strong.

**Ranked Residual Issues**
1. **Paradox not killed.** Recomputed `override_2P = +1093` median seed-delta, 27/27 positive, `p=1.49e-8`: real tax survives the valve. But paradox component is not negligible: per-seed-mean component is **median +373, mean +574**, 17+/10-, `p=0.2478`, CI about `[-56,+999]`. “Not significant” is fair; “largely refuted” overstates. You cannot rule out a several-hundred-token paradox contribution.
2. **Mean/median wording is wrong.** The code’s `paired()` reports **median**, not mean. `+373` is the median of per-seed mean components. `+539` appears when using per-seed condition medians. The claim “+373 mean / +539 median” is not the actual statistic.
3. **Valve capture is likely hint-induced, not ordinary size confusion.** All 10 `FALSE_NEG_2P` errors output exactly `escape_final`; `NEUTRAL_2P` outputs escape **0/112**. False-neg valve rate: **10/108 = 9.26%**, Wilson `[5.1%,16.2%]`, Fisher vs neutral escape `p=6.5e-4`. But output-only integers cannot prove whether the model computed `B>A` and obeyed the hint, or shortcut-stopped at the remaining prime.
4. **“Capture = unpaid tax” is only suggestive.** Valve-taker tokens: `511, 512x6, 1024x2, 2048`; median **512**, mean **768**. Correct `FALSE_NEG_2P`: median **1024**, mean **1655**. But **36/98 correct** calls also used `<=512`; low-reasoning threshold Fisher `p=0.085` though rank test is directionally significant. Demote mechanism; n=10 is still thin.
5. **Infra bias is real.** Exhausted: **37/480**, with `FALSE_NEG_2P` worst at **12/120**. Seeds 28-29 are missing across all conds; seed 27 is missing all `FALSE_NEG_2P`. Cost estimates are completed/correct-responder estimates and likely lower bounds if failures were slow. FN2P true accuracy could range from **98/120 = 81.7%** to **110/120 = 91.7%** depending on exhausted outcomes.
6. **Salience remains.** V9d removes the 0-solution-only objection partly, but `FALSE_NEG_2P` still names the answer `B`. So `+1093` is acceptable as a **false elimination of the named answer, with release valve, among resisters**. It is not a generic salience-free override.

**Demotions**
- “Gemini’s paradox hypothesis is largely refuted” -> “pure 0-solution-only explanation is refuted; a substantial paradox component remains plausible.”
- “Paradox component not significant” -> “not conventionally significant, but effect size is meaningful and underpowered.”
- “9% obeyed the false hint” -> “10/108 chose the smaller prime only under false-neg; likely hint-induced valve capture, not proven trace-level obedience.”
- “Capture = unpaid tax” -> “capture is associated with lower reasoning, but not cleanly diagnostic.”
- “Infra failures don’t bias deltas” -> “exhaustions censor hardest calls; costs are lower-bound-ish.”

**Next Experiment**
Run one **2P VERIFY_ALL same-salience** experiment: force JSON with every chain’s final value, prime flag, largest-prime name/value, then final answer. Conditions: `NEUTRAL`, `TRUE_POS_B` naming the answer, `FALSE_NEG_B` naming the same answer, `TRUE_NEG_A` naming the smaller prime. Fixed/counterbalanced prompt order, serial/retry until no exhausted calls. Decisive contrast: `FALSE_NEG_B - TRUE_POS_B`, on trace-correct records only.

**arXiv IDs:** `2502.02542`, `2310.13548`.
