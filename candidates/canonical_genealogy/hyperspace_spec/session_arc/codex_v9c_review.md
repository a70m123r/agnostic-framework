VERDICT: **overclaims-remain**. The V9c deltas are real and large, but `+1246` is best stated as a **false answer-elimination / contradiction tax**, not yet a generic “pure override” isolation.

**Raw re-derive:** `480` records, `30` seeds x `4` reps x `4` conditions. Correct-token med/mean: NEUTRAL `277.5/279.9`, TRUE_POS `100.5/127.7`, TRUE_NEG `271/273.0`, FALSE_NEG `1024/1567.6`; FALSE_NEG max `5122`, `0/120` at `6144`. Paired seed-level **median** deltas: TRUE_POS-NEUTRAL `-145.25`, TRUE_NEG-NEUTRAL `+2.375` (`16/14`, p=`0.856`), FALSE_NEG-NEUTRAL `+1200.75`, FALSE_NEG-TRUE_NEG `+1246.5` (`30/30`, p=`1.86e-9`).

**Ranked residual issues:**
1. **Main confound remains:** FALSE_NEG names the needle; TRUE_NEG names the hard lure. In this one-prime task, “NOT named `<needle>`” cannot be true. So truth is still coupled to **answer-chain salience + contradiction localization**.
2. **`+1246` is not generic override:** it likely includes exhaustive “no other prime exists” work. That is a valid false-elimination tax, but stronger/narrower than “pure falsehood override.”
3. **V9b decomposition:** sound only as `+438 ≈ +302 false-pointer tax - (-136 true shortcut)`. Do not splice V9c’s `+1246` into V9b’s pointer contrast.
4. **Trapdoor:** fairer now. Exact prompt-token delta is mean `+11.23`, not exactly `+12`; `+1200.75 / 11.23 ≈ 107:1`. “~1:100” survives.
5. **Near-unfoolable:** `119/120` is real, but Wilson 95% accuracy CI is `95.4%-99.9%`. The single capture used `512` tokens, but `40` correct FALSE_NEG calls also used `512`, so “unpaid-tax call” is an n=1 story, not a mechanism.

**Demotions:**
- “PURE override isolated = +1246” -> “large, cleanly measured **false-elimination contradiction tax**; pure generic override still unproven.”
- “Override bigger than V9b false-pointer” -> “false elimination costs ~4x V9b false pointer numerically, but mechanisms differ.”
- “Near-unfoolable / unpaid-tax capture” -> “high call-level resistance in this run; capture mechanism unresolved.”

**Decisive next experiment:** VERIFY_ALL same-named-chain factorial. Force output of all six finals before choosing, then compare hints that name the **same needle chain**: TRUE_POS “answer is named X” vs FALSE_NEG “answer is not named X”, plus TRUE_NEG hard-lure control. This removes positive shortcut and answer-chain salience as separable confounds.

arXiv ids: **2502.02542** OverThink/slowdown; **2310.13548** sycophancy baseline.
