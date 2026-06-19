# Codex external audit: V10b + V11b

Date: 2026-06-19

## Method

I read `measure/AUDIT_BRIEF_V10b_V11b.md` in full.

I attempted the requested analyzers:

- `python v11b_matched.py --reanalyze --model {deepseek,qwen,gemini} --seeds 28`
- `python v10b_irrelevant.py --reanalyze --model {deepseek,qwen,gemini} --seeds 24`

All six failed in this environment with `ModuleNotFoundError: No module named 'numpy'`. I therefore used the brief's allowed fallback and recomputed from JSONL with the analyzer semantics:

- exhausted calls excluded from accuracy;
- condition medians/means computed on correct calls with non-null `reasoning_tokens`;
- deltas computed as per-seed mean reasoning tokens over reps, then median paired difference;
- exact two-sided sign p from non-zero paired deltas;
- 4000 bootstrap median CI reimplemented with the standard library, so CI endpoints are approximate but medians/sign tests reproduce the locked-run claims.

Lock digests were verified against labels:

| lock | labels | digest | result |
|---|---:|---|---|
| V11b | 168 | `d394534f3512141a9f76dfeb4ad89e8ec663675790470ad99ed7ca58b5834520` | match |
| V10b | 144 | `1c0071d0b47401d137e072df8952ae32f90d7754ec2e9404758b6d68c613bdb9` | match |
| V10 prior | 192 | `cb7ecfdd0f885cb1d9306d6a552b91577174b4349c1227ba01542bc6f801d46d` | match |

V11b and V10b have the advertised 28-seed and 24-seed run files. The V10 prior run files contain 448 records/model, i.e. 14 seeds x 4 reps x 8 conditions, although the label lock contains 24 seeds.

## Reproduction baseline

### V11b deltas

Correct-only, per-seed mean over reps, median paired delta:

| contrast | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `NAMED_DEF - NAMED_BARE` | +124.5, CI +16..+220, p=.087, +19/-9 | +346.0, CI +173..+400, p=.013, +21/-7 | +759.6, CI +596..+1146, p<.001, +26/-2 |
| `RENAMED_PRIME - NAMED_DEF` | +161.9, CI +53..+227, p=.013, +21/-7 | +262.6, CI +92..+382, p=.004, +22/-6 | +241.0, CI +54..+654, p=.036, +20/-8 |
| `NOVEL_RULE - NAMED_DEF` | +307.6, CI +194..+400, p<.001, +25/-3 | +836.1, CI +736..+1121, p<.001, +27/-1 | +2150.8, CI +1678..+2571, p<.001, +28/-0 |
| `F0_NOVEL_RULE - F0_NAMED_DEF` | +77.6, CI +17..+156, p=.013, +21/-7 | -172.1, CI -298..+56, p=.345, +11/-17 | +100.7, CI -176..+354, p=.572, +16/-12 |

V11b condition medians over correct calls also reproduce the brief:

| model | bare | named def | renamed prime | novel rule | F0 named | F0 novel |
|---|---:|---:|---:|---:|---:|---:|
| deepseek | 619 | 783 | 882 | 1057 | 152 | 242 |
| qwen | 2945 | 3226 | 3480 | 4140 | 2643 | 2614 |
| gemini | 2203 | 2984 | 3395 | 5501 | 1489 | 1666 |

All-completed sensitivity:

- F0 all-completed equals correct-only for deepseek and qwen. Gemini becomes +124.4, p=.572, still null by sign test.
- `RENAMED_PRIME - NAMED_DEF` all-completed stays positive for deepseek (+141.4, p=.036) and qwen (+262.6, p=.004), but gemini drops to +211.1, p=.185.

### V10b lookup deltas

Correct-only, per-seed mean over reps:

| contrast | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `F1_S - F2_DEINDEXED` | +19.1, CI +8..+31, p=.023 | +142.5, CI +68..+253, p=.007 | +23.2, CI -30..+167, p=.839 |
| `F1_L - F1_S` paired | +47.2, CI +6..+62, p=.023 | +52.0, CI -146..+126, p=.541 | -8.5, CI -96..+106, p=1.000 |
| `F1_M - F1_S` | +24.2, CI -3..+48, p=.152 | +5.5, CI -117..+201, p=1.000 | -19.2, CI -87..+60, p=.839 |
| `F1_L - F1_M` | +21.1, CI +2..+78, p=.064 | -30.9, CI -264..+107, p=.405 | +43.5, CI -25..+132, p=.405 |

Condition median lookup tokens:

| model | F1_S | F1_M | F1_L | F1_L - F1_S by condition medians | F1_L accuracy |
|---|---:|---:|---:|---:|---:|
| deepseek | 84 | 103 | 121 | +37 | 92/96 |
| qwen | 568 | 529 | 498 | -70 | 96/96 |
| gemini | 173 | 168 | 166 | -7 | 96/96 |

### V10 prior vs V10b lookup

Condition median reasoning tokens:

| model | cond | V10 prime | V10b lookup | difference | ratio |
|---|---|---:|---:|---:|---:|
| deepseek | F1_S | 1680.5 | 83.5 | 1597.0 | 20.1x |
| deepseek | F1_M | 4342.0 | 103.0 | 4239.0 | 42.2x |
| deepseek | F1_L | 8102.0 | 121.0 | 7981.0 | 67.0x |
| qwen | F1_S | 4805.0 | 568.5 | 4236.5 | 8.5x |
| qwen | F1_M | 7629.0 | 529.0 | 7100.0 | 14.4x |
| qwen | F1_L | 10469.0 | 498.0 | 9971.0 | 21.0x |
| gemini | F1_S | 6274.5 | 173.0 | 6101.5 | 36.3x |
| gemini | F1_M | 11944.0 | 168.0 | 11776.0 | 71.1x |
| gemini | F1_L | 12798.0 | 165.5 | 12632.5 | 77.3x |

Because V10 has only 14 seeds and V10b has 24, I also restricted V10b to the same 14 seed ids. The conclusion survives: ratios remain about 20x/37x/72x for deepseek F1_S/M/L, 8.6x/13.6x/24.8x for qwen, and 37x/70x/75x for gemini.

V10 prior size and F0 frame deltas:

| contrast | deepseek | qwen | gemini |
|---|---:|---:|---:|
| `F1_M - F1_S` prime | +2578.0, p=.002 | +3068.1, p=.002 | +4377.0, p<.001 |
| `F1_L - F1_S` prime | +5952.5, p<.001 | +7340.1, p<.001 | +6440.8, p<.001 |
| `F0_DISSOLVED - F0_DEINDEXED` | +149.0, p=.057 | +375.9, p=.180 | +2302.8, p<.001 |

## Claim audit

### C1 - Headline V11b novel concept cost

Verdict: **overstated**.

Reproduced number:

- `NOVEL_RULE - NAMED_DEF`: deepseek +307.6, p<.001; qwen +836.1, p<.001; gemini +2150.8, p<.001.

The positive cross-model effect is real in the locked data. It is large, directionally stable, and not a reproduction artifact.

Refutation attempt:

- The exact same integer is selected by primality and WURF, and the compute-arm needle line hashes match across `NAMED_BARE`, `NAMED_DEF`, `RENAMED_PRIME`, and `NOVEL_RULE`.
- But "compute matched" is not established strongly enough. A simple operation-count proxy changes direction depending on the assumed primality algorithm.
- For the needle only, raw integer trial division gives median prime checks 9.5 vs WURF 7, so WURF is easier. But prime-divisor-only checking gives median prime checks 4.5 vs WURF 7, so WURF is harder.
- Across all six final values, raw trial division gives median prime checks 19 vs WURF 14. Optimized/prime-divisor proxies give prime 13/11 vs WURF 14.

Sharpest residual flaw:

The experiment proves "novel predicate prompt costs more hidden reasoning than named primality prompt" much better than it proves "un-amortized concept costs more with compute held matched." WURF may induce more explicit rule execution than primality under plausible model strategies. The phrase "V11's negative was 100% predicate-difficulty artifact" is stronger than the evidence warrants.

Demotion:

Keep: robust V11b positive novel-rule tax.

Demote: "same-difficulty de-amortization of meaning" -> "novel-predicate application overhead, with de-amortization plausible but not uniquely isolated."

### C2 - Renamed primality as pure label de-amortization

Verdict: **reproduced**.

Reproduced number:

- `RENAMED_PRIME - NAMED_DEF`: deepseek +161.9, p=.013; qwen +262.6, p=.004; gemini +241.0, p=.036.

Integrity checks:

- The definition is the same primality definition with the predicate name changed from `PRIME` to `FLONK`.
- The selected truth and needle line hash are identical across compute arms for all 28 seeds.

Refutation attempt:

- The computation is identity-matched at the problem level, but the model's strategy need not be identity-matched. A nonce predicate can cause re-reading, distrust, definition binding, or explicit verification of "FLONK means prime" even if the arithmetic predicate is primality.
- The all-completed sensitivity weakens gemini: +211.1 with p=.185, because the correct-only analysis drops some incorrect cells.

Sharpest residual flaw:

The number is clean, but "pure label-de-amortization" is mechanistic overreach. The safer claim is a nonce-binding cost under byte-identical primality substrate, not proof that only semantic label amortization changed.

Demotion:

Keep: a small-to-moderate, cross-model, significant correct-only nonce cost under exact substrate identity.

Demote: "pure label cost" -> "nonce binding / re-verification cost with compute identity at the prompt level."

### C3 - F0 falsifier removes the novel-vs-named gap

Verdict: **underpowered**.

Reproduced number:

- `F0_NOVEL_RULE - F0_NAMED_DEF`: deepseek +77.6, p=.013; qwen -172.1, p=.345; gemini +100.7, p=.572.
- All-completed F0: deepseek +77.6, qwen -172.1, gemini +124.4, with the same sign-test conclusions.

Refutation attempt:

- "Vanishes on 2/3" is technically true for sign-test significance, but it is a null claim from n=28 with broad CIs.
- Deepseek does not vanish. It retains a significant +77.6 tax, about one quarter of its headline +307.6.
- Gemini's F0 CI is wide enough to include a moderate positive effect. Qwen's CI includes zero and modest positive values.

Sharpest residual flaw:

The F0 result supports a large reduction, not a clean disappearance. The falsifier is directionally useful, but it is underpowered for claiming that definition holding has no residual cost.

Demotion:

Keep: headline application gap is much larger than F0 gap, especially for qwen and gemini.

Demote: "the gap vanishes" -> "the gap mostly collapses when verdicts are pre-given, with a surviving deepseek residual and nulls too imprecise to prove zero."

### C4 - V10b compute isolation: lookup is near-floor and frame-insensitive

Verdict: **overstated**.

Reproduced number:

- Lookup medians are near-floor for deepseek and gemini: deepseek F1_S/M/L = 84/103/121; gemini = 173/168/166.
- Qwen is not as low in absolute terms but is still much lower than prime: qwen F1_S/M/L = 568/529/498.
- F1_L lookup accuracy is high: deepseek 92/96, qwen 96/96, gemini 96/96.
- `F1_S - F2_DEINDEXED`: deepseek +19.1, p=.023; qwen +142.5, p=.007; gemini +23.2, p=.839.

Refutation attempt:

- Floor effect is real. Deepseek and gemini lookup calls sit close to a low reasoning baseline, so absence of a large size/frame slope cannot prove reading or search is free.
- "Frame-insensitive" is also too strong. Deepseek and qwen have significant positive `F1_S - F2_DEINDEXED` deltas, just small in absolute terms.
- Qwen shows large condition-level shifts among the framed lookup conditions: F3 median 2020, FP 1232, F2 423, F1_S 568. This is not a uniformly frame-insensitive lookup process.

Sharpest residual flaw:

Lookup is an easier and different task, probably close to a measurement floor for two models. It can show that predicate application dominates this task family, but it cannot prove that reading/search/orienting costs are intrinsically negligible.

Demotion:

Keep: lookup cost is tiny relative to prime-task cost.

Demote: "reading/search is free or frame-insensitive" -> "this lookup task does not elicit a large reasoning-token reading/search slope."

### C5 - V10 size-axis reinterpretation as compute/evaluation volume, not reading volume

Verdict: **overstated**.

Reproduced number:

- V10 prime size axis is huge:
  - `F1_M - F1_S`: deepseek +2578.0, qwen +3068.1, gemini +4377.0.
  - `F1_L - F1_S`: deepseek +5952.5, qwen +7340.1, gemini +6440.8.
- V10b lookup condition-median `F1_L - F1_S`: deepseek +37, qwen -70, gemini -7.
- V10b lookup paired `F1_L - F1_S`: deepseek +47.2, p=.023; qwen +52.0, p=.541; gemini -8.5, p=1.000.
- Prime-vs-lookup same-condition ratios are very large: about 20x-77x in the all-V10b median comparison and still about 8.6x-75x when lookup is restricted to V10's 14 seeds.

Refutation attempt:

- The reinterpretation is directionally right: the old "universal reading-volume cost" is not supported as stated.
- But the lookup control does not prove zero reading-volume cost because it is too easy and task-switched.
- Deepseek has a small but significant paired lookup size increase (+47.2, p=.023), although it is tiny relative to the prime size effect.

Sharpest residual flaw:

The data strongly demote "universal reading-volume cost," but they do not isolate "predicate-evaluation volume" as the only source. A reading-volume cost could appear above the lookup floor or under a more demanding application-free reading task.

Demotion:

Keep: V10's size-axis effect is dominated by predicate/evaluation work, not mere token volume.

Demote: "NOT reading" -> "not explained by this low-cost lookup reading control."

### C6 - V10 frame-cost refinement by truly application-free lookup

Verdict: **overstated**.

Reproduced number:

- V10 F0 `F0_DISSOLVED - F0_DEINDEXED`:
  - deepseek +149.0, p=.057;
  - qwen +375.9, p=.180;
  - gemini +2302.8, p<.001.
- V10b lookup `F1_S - F2_DEINDEXED`:
  - deepseek +19.1, p=.023;
  - qwen +142.5, p=.007;
  - gemini +23.2, p=.839.

Refutation attempt:

- The gemini contrast is compelling as a demotion of the old V10 "compute-free residual frame-cost": +2303 under V10 F0 vs about +23 under lookup.
- But V10 F0 and V10b lookup remove compute in different ways. V10 F0 still asks the model to identify which final value is prime. V10b lookup asks for the initial value of a named variable.
- That is not a clean subtraction. It changes the objective, the search key, the answer target, and likely the model strategy.
- Deepseek and qwen lookup frame deltas are small but significant, so the residual frame cost is not universally zero even under lookup.

Sharpest residual flaw:

The attribution "largely primality-application-under-dissolution" is plausible but not cleanly identified. The current control confounds predicate removal with a switch to name lookup.

Demotion:

Keep: V10's gemini F0 residual should not be called pure orienting/search cost.

Demote: "it was primality application" -> "it disappears under a different, application-free lookup task; same-task verdict controls are needed for attribution."

## Overall WATERLINE

Above the waterline:

- The locked-run numbers reproduce.
- V11b shows a robust cross-model novel-rule reasoning-token tax.
- V11b renamed primality shows a smaller but reproducible nonce-binding cost under byte-identical substrate.
- V10b strongly demotes V10's broad "reading-volume" interpretation: prime/evaluation tasks cost orders of magnitude more reasoning than lookup on the same substrate family.

Below the waterline:

- Do not claim WURF is proven compute-matched to primality. The operation-count direction depends on the assumed model algorithm.
- Do not claim a pure de-amortization mechanism from V11b alone. The defensible label is novel/nonce predicate application overhead.
- Do not claim lookup proves reading/search is free. It is likely near a reasoning floor for deepseek and gemini.
- Do not treat V10 F0 vs V10b lookup as a clean compute-removal subtraction. It changes the task.

Single most important next control:

Run a same-task, above-floor, application-free verdict control: keep the V10/V11 answer format as "report the final value of the unique PASS computation," pre-give final values and PASS/fail verdicts for prime/FLONK/WURF on every line, vary frame and substrate size, and add enough calibrated distractor/reading load to lift lookup-style reasoning above floor. This removes predicate application without switching to name lookup, so it directly tests whether residual size/frame costs survive when application is removed.
