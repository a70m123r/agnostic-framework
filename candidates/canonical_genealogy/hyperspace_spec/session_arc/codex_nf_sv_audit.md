# Codex adversarial audit: NF label/compute and SV same-task verdict control

Date: 2026-06-19

I read `measure/AUDIT_BRIEF_NF_SV.md` in full and recomputed from the locked JSONL artifacts only:
`v_nf_run.*.jsonl`, `v_sv_run.*.jsonl`, `v10fs_run.*.jsonl`, and `v10b_run.*.jsonl`.

Method: plain Python, no numpy. For each condition and seed I averaged `reasoning_tokens` across correct reps, then
formed paired seed deltas and took the median. P values below are exact sign-test p values unless noted. I also
computed exact signed-rank/Wilcoxon checks for the main attacks and a conservative NF prompt-word residualization
stress test.

Important artifact note: NF has 60 seeds x 3 reps. SV and V10b have 24 seeds x 4 reps. `v10fs_run.*.jsonl` has
only 14 seeds x 4 reps, so every V10 prime minus SV verdict cross-experiment `D_application` number is based on
the 14-seed intersection, not 24 seeds.

## NF reproduction

Primary paired medians:

| claim contrast | deepseek | qwen | gemini |
|---|---:|---:|---:|
| NF-C1 `HARD_PLAIN - HARD_WORD` | +43.2, p=0.00267 | +184.8, p=0.000135 | +318.2, p=0.00622 |
| NF-C2 `TRIV_NONCE - TRIV_PLAIN` | +35.3, p=1.62e-07 | +59.0, p=0.519 | -305.8, p=0.00107 |
| NF-C3 `HARD_PLAIN - TRIV_PLAIN` | +144.0, p=3.18e-15 | +112.8, p=0.699 | +488.3, p=1.21e-05 |

All NF calls completed. Deepseek and qwen were all correct. Gemini had small accuracy losses:
`TRIV_PLAIN` 178/180, `TRIV_NONCE` 179/180, `HARD_PLAIN` 180/180, `HARD_NONCE` 175/180, `HARD_WORD` 178/180.

Prompt-word medians in NF:

| condition | median prompt_words |
|---|---:|
| `TRIV_PLAIN` | 242 |
| `TRIV_NONCE` | 248 |
| `HARD_PLAIN` | 246 |
| `HARD_NONCE` | 256 |
| `HARD_WORD` | 236 |

The WORD contrast therefore makes `HARD_WORD` 10 words shorter than `HARD_PLAIN`. The pure trivial nonce contrast
makes `TRIV_NONCE` 6 words longer than `TRIV_PLAIN`.

### NF prompt-length stress test

I fit, per model, a simple seed-cell OLS sensitivity `reasoning_tokens ~ prompt_words` over the NF grid and
recomputed paired deltas on residuals. This is not a definitive control because selector identity and selector
length are not crossed in the locked design, but it is a useful adversarial check.

| contrast | deepseek raw -> adjusted | qwen raw -> adjusted | gemini raw -> adjusted |
|---|---:|---:|---:|
| `HARD_PLAIN - HARD_WORD` | +43.2 -> +2.8, p=0.897 | +184.8 -> +273.4, p=5.21e-09 | +318.2 -> +47.9, p=0.366 |
| `TRIV_NONCE - TRIV_PLAIN` | +35.3 -> +11.1, p=0.00267 | +59.0 -> +112.2, p=0.245 | -305.8 -> -468.0, p=4.22e-05 |
| `HARD_PLAIN - TRIV_PLAIN` | +144.0 -> +127.8, p=6.25e-14 | +112.8 -> +148.3, p=0.366 | +488.3 -> +380.2, p=0.000394 |

This sharply weakens NF-C1 for deepseek and gemini. It does not weaken qwen.

### NF-C2 heavy-tail and accuracy check

Gemini `TRIV_PLAIN` is skewed: row median/mean = 817/1010, versus `TRIV_NONCE` 340/776. However the paired effect
is not just one tail event: sign split is 43 negative versus 17 positive, Wilcoxon p=0.00477, and the all-correct
seed subset remains negative at -281.3, sign p=0.00320. The gemini negative result is real in this run, but it
should not be interpreted as universal "naming helps"; it is likely wording/strategy specific.

## SV/V10/V10b reproduction

Structural checks on `v_sv_labels.jsonl`: 144/144 prompts have exactly one `[verdict: PASS]`; 0 prompts have an
arithmetic line containing `%` without an inline `=>` final. The SV stimuli are structurally application-free with
respect to primality. Trace check: prime/divisibility language is almost absent in SV reasoning (deepseek 1 correct
row total; qwen 0; gemini 0). Qwen nevertheless often treats `PASS/fail` as a correctness verdict and sometimes
recomputes arithmetic, especially in `F3_FRAMED`; this is a qwen-specific cognitive artifact.

### D_application: V10 prime minus SV verdict

Cross-experiment deltas use only the V10/SV seed intersection. Thus n=14 except gemini `F1_L`, where n=13 because
one paired correct cell is missing.

| condition | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `F3_FRAMED` | +523.5, p=0.0129 | -2416.2, p=0.000122 | +1480.0, p=0.000122 |
| `FP_POINTED` | +1447.5, p=0.000122 | +3457.5, p=0.000122 | +5419.4, p=0.000122 |
| `F2_DEINDEXED` | +1674.9, p=0.000122 | +3511.8, p=0.000122 | +5047.1, p=0.000122 |
| `F1_S` | +1656.2, p=0.000122 | +2571.5, p=0.000122 | +4885.2, p=0.000122 |
| `F1_M` | +4178.6, p=0.000122 | +6443.8, p=0.000122 | +9300.3, p=0.000122 |
| `F1_L` | +7567.9, p=0.000122 | +10926.0, p=0.000122 | +11979.8, p=0.000244 |

Qwen `F3_FRAMED` is the anomaly: SV verdict median is 5248, while V10 prime median is 3169 and V10b lookup median
is 2020. The non-F3 qwen application range reproduces the brief (+2572 to +10926).

### SV internal deltas

| contrast | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `F1_S - F2_DEINDEXED` (`D_frame`) | +113.0, p=3.59e-05 | +372.1, p=0.000277 | +405.0, p=0.0227 |
| `F2_DEINDEXED - FP_POINTED` | +26.2, p=0.541 | -1274.6, p=1.19e-07 | -1360.8, p=3.59e-05 |
| `F1_M - F1_S` | -55.0, p=0.307 | -283.1, p=0.0227 | +155.8, p=0.839 |
| `F1_L - F1_M` | -85.4, p=0.0931 | -175.8, p=0.0347 | -307.0, p=0.541 |

Gemini size is even weaker on all-correct seeds: `F1_M - F1_S` drops from +155.8 to +5.0, p=1.0.

Critical SV-C2 structural confound: in the labels, `F2_DEINDEXED` has the selector before the body, while `F1_S`,
`F1_M`, and `F1_L` have the selector after the body. For `F1_S - F2_DEINDEXED`, the median prompt-word difference
is -7 words, so length is not the issue. The issue is that header removal and selector position move together.
The measured `D_frame` is therefore also a late-instruction rescan contrast.

### Verdict minus lookup

| condition | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `F3_FRAMED` | +12.2, p=0.307 | +3099.2, p=1.19e-07 | +730.2, p=1.19e-07 |
| `FP_POINTED` | +28.6, p=0.00154 | +588.1, p=0.000277 | +1920.5, p=1.19e-07 |
| `F2_DEINDEXED` | +67.5, p=1.19e-07 | +225.9, p=0.00661 | +668.6, p=1.19e-07 |
| `F1_S` | +138.2, p=2.98e-06 | +360.4, p=0.00154 | +1124.2, p=1.19e-07 |
| `F1_M` | +118.9, p=0.0227 | +143.2, p=0.152 | +1325.3, p=1.19e-07 |
| `F1_L` | +20.5, p=0.541 | +35.1, p=0.839 | +446.9, p=0.00154 |

Gemini strongly supports verdict > lookup. Deepseek and qwen support it in the middle conditions, but not at
both extremes; qwen `F3_FRAMED` is inflated by the same verdict/correctness artifact.

## Claim verdicts

### NF-C1

Claim: cached word "prime" is cheaper to apply than the explicit rule; robust in all three models.

Verdict: overstated. The headline numbers reproduce exactly enough: +43/+185/+318. The sharpest flaw is the
10-word selector-length confound. In a conservative prompt-word residualization, deepseek collapses to +2.8
(p=0.897) and gemini to +47.9 (p=0.366). Qwen survives, so this is not killed; it is not robust across all three
after the length attack.

### NF-C2

Claim: coining a novel name for a trivial rule does not robustly cost; V11b RENAMED was not a universal pure
label-binding tax.

Verdict: reproduced. Deepseek has a small +35 cost, qwen is null, gemini is significantly negative. Deepseek's
small effect is partly compatible with the +6-word naming clause, though the residualized effect is still a small
+11. Gemini's -306 is not explained by accuracy exclusion or a single heavy tail: all-correct remains negative
and Wilcoxon is significant. The sharpest flaw is interpretive: do not canonize "naming helps"; the safe claim is
only "pure nonce binding is not a robust universal cost."

### NF-C3

Claim: hard predicate compute costs on deepseek and gemini, null on qwen.

Verdict: reproduced. Deepseek +144 and gemini +488 are strong; qwen +113 is sign-null and high-variance. The
sharpest flaw is that qwen is not evidence of zero compute cost; it is an uninformative noisy model for this
contrast in this run.

### SV-C1

Claim: application cost is dominant and grows with substrate size; same task, predicate removed.

Verdict: overstated. The core application-volume signal survives strongly outside qwen `F3_FRAMED`, and it grows
on the size axis for all three models. But "cleanly isolated" is too strong: V10 prime comparisons have only
14 seeds, V10 accuracy degrades in large gemini conditions, and qwen `F3_FRAMED` shows a verdict/correctness
artifact that reverses the application delta. The waterline version is: application volume is still the dominant
cost in deindexed/large substrates, but the control is not perfectly application-free cognitively for qwen and is
under-seeded cross-experiment.

### SV-C2

Claim: an application-independent frame-orienting cost survives clean application removal and rescues V10's
orienting claim.

Verdict: overstated. The numeric `D_frame` reproduces (+113/+372/+405, all sign-significant), but the causal
label does not. `F2_DEINDEXED` is leading-selector; `F1_S` is trailing-selector. Therefore `F1_S - F2_DEINDEXED`
still confounds header removal with selector position and possible late-instruction rescan. This is the sharpest
flaw in the brief. Do not canonize this as a clean rescue of orienting until selector position is crossed.

### SV-C3

Claim: size axis is null/negative under verdict, so size is predicate-evaluation volume rather than reading.

Verdict: reproduced, with scope limits. Deepseek is null/negative, qwen is significantly negative, and gemini is
null once all-correct sensitivity is considered. The sharpest flaw is overgeneralization: the result shows no
positive size slope for this PASS-scan task, not a universal absence of reading/search cost.

### SV-C4

Claim: verdict > lookup means the prime-task answer format adds cost beyond application.

Verdict: overstated. The verdict-minus-lookup numbers reproduce, and gemini is strongly positive across all
conditions. But deepseek and qwen are mixed/null at the extremes, qwen `F3_FRAMED` is an outlier, and verdict vs
lookup changes the search key and objective, not merely answer format. The safest claim is that same-task PASS
selection can cost more than named-variable lookup, especially for gemini; it is not a clean answer-format
isolate.

## Overall waterline

Survives:

- NF-C2: pure nonce label binding is not a robust universal tax. V11b RENAMED should remain demoted toward
  FLONK-to-prime translation and compute/label interaction.
- NF-C3: hard predicate compute cost is real on deepseek and gemini; qwen does not adjudicate.
- SV-C1, demoted: application volume is still the biggest driver in deindexed and large substrates, but the
  cross-experiment evidence is 14-seed and qwen shows a verdict artifact.
- SV-C3: replacing primality with PASS removes the positive size curve; this supports predicate-evaluation volume
  over plain reading volume for these stimuli.

Demotes:

- NF-C1 as a three-model causal word shortcut. The number reproduces, but the locked design cannot cleanly
  separate cached-word advantage from the 10-word selector shortening in deepseek/gemini.
- SV-C2 as a clean frame-orienting rescue. It is still a leading-selector versus trailing-selector contrast.
- SV-C4 as "answer format" specifically. The contrast changes task semantics and search key.

Single most important next control:

Run the SV selector-position 2x2 with a neutral tag: same body, same PASS-equivalent target marker, header
present/absent crossed with selector leading/trailing, prompt words matched. Use a neutral marker such as
`[target: YES/no]` rather than `PASS/fail` to avoid qwen treating the tag as a computation-correctness verdict.
This one control directly attacks the SV-C2 waterline and also reduces the qwen artifact in SV-C1/SV-C4.
