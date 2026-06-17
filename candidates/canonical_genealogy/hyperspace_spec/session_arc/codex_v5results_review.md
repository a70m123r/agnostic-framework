## Verdict

**overclaims-remain**: the DEEP>WIDE result is real and important, but “isolates serial dependency beyond transcription/memory-load” is too strong.

## Residual confounds

The honest claim is: **at matched coarse work, prompt words, display lines, nominal live vars, and answer digits, DEEP costs more than WIDE**. That refutes a narrow “one scratchpad line per printed op” account. It does **not** yet isolate Brent-style critical-path span as the only active cause. Work/span is the right vocabulary for the manipulation, but Brent’s result is a parallel-computation framing, not evidence about LLM hidden-token accounting. 

Main confounds:

- **Routing/self-update confound:** every WIDE update is `rX = (rX op c)`, every DEEP update is cross-register `rX = (rY op c)`. Same line count, but not same parsing/pointer-following burden. WIDE may be cheaper because it is syntactically compressible.

- **WIDE discount vs DEEP surcharge:** the result proves a relative contrast. It cannot distinguish “serial depth costs extra” from “parallel/self-chain structure gives an optimization shortcut.” Those are not equivalent mechanistic claims.

- **Carry/magnitude residue:** if “carry length” means recurrence length, that is basically the treatment. If it means intermediate numeric burden, it is not controlled. I recomputed oracle intermediates: DEEP has a small median excess in hidden assigned-value digits and premod digits. It is far too small to obviously explain +38.5 tokens, and weakly correlated with deltas here, but it keeps a value-transcription account alive.

- **Nominal live vars are not cognitive live vars:** both prompts name `m` registers, but optimal state differs. WIDE naturally maintains independent accumulators; DEEP is a rotating dependency chain whose final reduction uses recent chain states. “Track every variable” does not force identical internal bookkeeping.

- **Arm order:** the runner emits DEEP then WIDE for each pair. API calls should be stateless, but for a promotion-level claim, structure and call order should not be perfectly coupled.

## Further Demotions

Demote from **“genuine serial-depth surcharge beyond work/transcription/memory-load”** to:

**“robust DEEP>WIDE structure contrast at matched coarse work/length/line/live-var counts; consistent with a serial-dependency surcharge, but not yet isolated from routing, self-update compression, and intermediate-value transcription.”**

Demote **“only critical-path span differs”** to:

**“the matched fields and op multiset are equal; source-register routing and algorithmic affordances still differ.”**

Demote **“refutes pure transcription”** to:

**“refutes literal line/op-count transcription; does not refute value-level or pattern-compression transcription.”**

Demote **“not depth-proportional”** to:

**“V5-LITE shows no clean dose-response evidence.”** The two cells vary `m`, `k`, total work, prompt length, and WIDE bookkeeping together. The near-constant +35.5 vs +38.5 surcharge could be span growth partly cancelled by higher WIDE bookkeeping. It does not falsify a depth slope.

## Next Move

Do a cheap guard before V5-FULL: rerun fresh or same 16 pairs with **randomized/counterbalanced arm order**, and add a gate or covariate for oracle intermediate digit/premod-digit balance. That is the fastest check against order and magnitude residue.

Then run V5-FULL, but with sharper wording: fixed `m`, fixed total work, span ladder, matched routing/self-vs-cross counts if possible, and an explicit magnitude/intermediate-digit control. The bootstrap CI is fine as secondary, but at `n=16` the exact paired sign test is the load-bearing inference; bootstrap intervals are descriptive, per the Efron bootstrap lineage, not a substitute for a cleaner design. 

If V5-FULL becomes a grid over many cells/tiers/models, predeclare the primary contrast and treat the rest as exploratory or use a multiplicity policy such as Benjamini-Hochberg. 
