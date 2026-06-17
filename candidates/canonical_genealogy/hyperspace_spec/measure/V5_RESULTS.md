# V5-LITE — WIDE-vs-DEEP: a serial-dependency surcharge beyond work (matched-pair, confound-gated)

**Date:** 2026-06-17 | **Status:** real measurement. 16 matched DEEP/WIDE pairs (2 cells × 8 seeds),
gpt-5.5 @ `high`, pre-registered + sha-locked (`v5wd_labels.LOCK` 3a08d918). `v5_widedeep.py` (generator,
selftest-gated) + `v5wd_run.py` (paired runner) -> `v5wd_lite.jsonl`. The design rebuilt after the
`v5-widedeep-design` workflow's audit found the first build confounded (span collinear with length).
Cite-don't-coin, demote-not-kill.

## Headline — a genuine serial-dependency surcharge
At **matched** total work, prompt words, display lines, live-variable count, and answer-digit count
(selftest-verified per pair — only critical-path SPAN differs), a **DEEP** (one long serial chain)
program costs gpt-5.5 **more reasoning tokens than a WIDE** (several independent short chains) program:

- DEEP median **222** tokens vs WIDE median **183** tokens.
- **Paired median(DEEP − WIDE) = +38.5 tokens** — one-sided sign-test p=0.0003, two-sided 0.0005,
  bootstrap 95% CI **[+26.0, +55.0]**, **15 of 16 pairs** DEEP>WIDE.

**This refutes the LITERAL-transcription and pure-work readings** the V4 external pass favored:
line/op-count transcription predicts DEEP≈WIDE (identical line/op count), work predicts DEEP≈WIDE
(identical op-count), memory-load predicts DEEP≈WIDE (identical live-vars). The surplus is attributable to
what differs — **a long serial / cross-routed dependency structure.** So the V4 effect was **not only**
arithmetic volume or scratchpad lines: serial structure costs extra. (Brent 1974 work-vs-span, the framing.)

> **External pass (codex xhigh + gemini, converged) — see [EXTERNAL_SYNTHESIS_V5_RESULTS.md](EXTERNAL_SYNTHESIS_V5_RESULTS.md).** Both affirm the result is real + robust and **kills the literal-transcription reading**, but **demote "serial DEPTH" → "a robust DEEP>WIDE STRUCTURE contrast, not yet isolated from routing / self-update compression / carry-length / value-level transcription."** Key unbeaten confounds, folded below: (1) **carry-length ≡ span** (one value transformed K times) — a single long chain inside a WIDE program would likely show the same surcharge, so it's "any long dependency," not deep-vs-wide per se; (2) **routing** — WIDE is self-read `rX=(rX..)` (compressible), DEEP is cross-read `rX=(rY..)`, so the gap may be a WIDE discount not a DEEP surcharge; (3) `m`-confound explains the plateau. "Refutes pure transcription" → "refutes LITERAL line/op transcription; value-level transcription stays alive (codex recomputed a small DEEP intermediate-digit excess)."

## The bounded claim — NOT a depth-proportional law (the dose-response caveat)
| cell | span DEEP/WIDE | span gap | n | median Δ | Δ per span-step |
|---|---|---|---|---|---|
| m2k6 | 13 / 7 | 6 | 8 | +35.5 | +5.9 tok |
| m4k4 | 19 / 7 | 12 | 8 | +38.5 | +3.2 tok |

The surcharge is **~constant (+35.5 vs +38.5)** even though the span gap **doubled** — it does **not**
scale linearly with span (per-span-step cost *halves*, 5.9→3.2). Per the pre-registered decision rule,
that blocks a "tokens ∝ depth" claim. What we have is a **serial-vs-parallel cost**, not a calibrated
depth meter.

## What V5-LITE CAN claim
**At fixed work / length / memory-load, a serial (deep) dependency structure costs gpt-5.5 materially
more reasoning tokens than a parallel (wide) one** (~+37 tok, +17–23%, 15/16 pairs, p=0.0003) — a real
seriality/critical-path effect that pure transcription, work, and memory-load cannot explain.

## What V5-LITE CANNOT claim
- **Not a depth-proportional law.** The surcharge is ~constant across a 6-vs-12 span gap; the functional
  form is unresolved (fixed serial-overhead? saturation? scales with something else?).
- **Span is confounded with register-count `m`.** The two cells vary `m` (2 vs 4) *and* `k` together, so
  WIDE's parallel-bookkeeping load (rises with `m`) and DEEP's span (rises with `m·k`) move together; the
  near-constant Δ could be DEEP-span-cost partly cancelled by WIDE-`m`-cost. A clean depth law needs span
  swept at **fixed `m`**.
- **Carry-length disclosure:** the DEEP chain threads one running value through more serial mod-1000
  reductions; "serial-carry length along the answer path" numerically coincides with span here and is not
  separated from abstract critical-path depth.
- Single tier (`high`), single model (gpt-5.5), single seed-set, n=16 pairs, 100% solved.

## The arc (V4 → tier-sweep → V5-LITE)
1. **V4:** reasoning_tokens track arithmetic WORK net of input length (partial-Spearman +0.894), but the
   pure-transcription reading was unbeaten.
2. **Tier-sweep:** the work-slope survives at the lowest budget (ρ=+0.889 ≈ +0.852 at high) → **NEED-DRIVEN,
   not budget-gated** (one V4 open question closed).
3. **V5-LITE:** at matched work/length/memory, **serial > parallel** by +37 tok (p=0.0003) → **the effect
   is not only transcription/volume; serial dependency costs extra** (the second open question, answered
   in the promote direction) — but the cost is structure-sensitive, not depth-proportional.

## Next
**V5-FULL** — sweep span at **fixed `m`** (vary `k` and the deep/wide split independently of register
count) + a **carry-length control** (a wide variant whose longest single-value carry equals the deep's,
to separate carry from abstract span). Estimate the functional form (is there a true per-span slope once
`m` is held fixed?). Reuses the matched-pair harness.

## Provenance
`v5-widedeep-design` workflow (7 agents; first build found confounded, superseded) -> rebuilt
`v5_widedeep.py` (per-pair match gate: 16/16 equal on words/lines/vars/work/digits, oracle 32/32) ->
tier-sweep (need-driven) -> V5-LITE paired run. Pending: codex + gemini external pass on this promotion.
