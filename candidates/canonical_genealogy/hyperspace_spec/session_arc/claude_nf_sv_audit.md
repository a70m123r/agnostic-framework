# AUDIT — NF (label × compute) + SV (same-task verdict control)

**Date:** 2026-06-19 | **Lead auditor:** Claude (synthesizing 7 adversarial verdicts; codex + Claude skeptics)
**Mandate:** reproduce from locked run files, then refute. Skeptical; **demote-not-kill.** Going to canonical record.
**Status of inputs:** all 7 claims **reproduced exactly** from the locked files (NF lock 354d7d5e, SV lock 9093531, V10 prime, V10b lookup). Not one number failed reproduction. Every demotion below is about **interpretation**, not arithmetic — the apparatus is sound; the labels on the effects are where the over-claims live.

---

## NF — separating label-novelty from compute

### NF-C1 — "the cached WORD 'prime' is cheaper to APPLY than its explicit rule" → **OVERSTATED**

**Recomputed.** HARD_PLAIN − HARD_WORD = **+43.2** (deepseek, p=.003), **+184.8** (qwen, p<.001), **+318.2** (gemini, p=.006); paired bootstrap, n=60. Robust to all-completed (median +44/+302/+616, Mann-Whitney p≤.0005), to paired Wilcoxon (p≤.0007), and not survivorship (accuracy 100/100/98.9%). **The reasoning-token gap is real. The "amortization" reading is not.**

**Sharpest flaw — HARD_NONCE is the smoking gun.** The actual primality compute is *identical* across HARD_PLAIN and HARD_WORD: paired trial-division-marker delta is **null** on all three (deepseek +0.67 p=.065, gemini +0.00 p=.219, qwen +2.17 p=.289); ≥3-trial-mult rate identical; known-prime recognition identical. The rt delta tracks reasoning-**CHAR** (narration) delta (corr .957/.944/.862), **not** compute-marker delta (gemini .155). And the freshly-coined nonce FLONK — *definitionally un-amortized*, the model must dereference it — is the **most expensive** of the three HARD cells (deepseek 292, gemini 1814 rt_med), purely because its selector is the longest (41 words vs WORD 21w vs PLAIN 31w). Within-HARD rt rises **monotonically with selector word count** on deepseek+gemini, and length explains ~67% (deepseek) / ~49% (gemini) of the "WORD shortcut." Application is identical; what shrinks is **reading + restating the 10-word-longer explicit rule.** (qwen's +185 is *not* length-explained — wrong-signed within-HARD slope — but qwen is the chronically noisy model with an erratic NONCE cell, so it corroborates no clean amortization reading either.)

**Verdict:** the +43/+318 is a **reading-length / narration artifact**, not an application-amortization signal. Demote NF-C1 from "cached word cheaper to apply" to "**spelling out a rule costs more tokens to read and restate than naming it** — application cost is identical (compute-marker delta null)."

---

### NF-C2 — "pure label-binding does not robustly cost; 'label-binding always costs' demoted" → **REPRODUCED**

**Recomputed.** TRIV_NONCE − TRIV_PLAIN (per-seed paired, correct-only, n=60): deepseek **+35.3** (CI[+30,+44], sign-p=.000, 50+/10−); qwen **+59.0** (sign-p=.519, Wilcoxon p=.369, 33+/27−); gemini **−305.8** (sign-p=.001, Wilcoxon p=.005, 17+/43−). All three match the brief. Gemini's negative survives every robustness cut (log-ratio 0.69× p=.0003; median-over-reps −230; full-accuracy 57-seed subset −281; NONCE accuracy ≥ PLAIN — not an artifact). **Bidirectional and model-dependent confirmed; the demotion of "label-binding always costs" stands.**

**Sharpest flaw — the demotion is right but its *warrant* is mis-pinned.** V11b's RENAMED was FLONK vs the WORD "prime" with the full primality **definition present in both cells** — its true NF analog is **HARD_NONCE − HARD_WORD**, not the trivial TRIV contrast. That HARD analog *does* reproduce RENAMED's positive direction (deepseek +72, gemini +614, p<.001). So NF-C2's pure-label null does not *by itself* refute label-binding. The real isolating evidence is the **gemini sign-flip**: same coin/deref operation gives HARD_NONCE−HARD_WORD **+614** vs TRIV_NONCE−TRIV_PLAIN **−306** — opposite sign by rule difficulty alone. That pins V11b RENAMED's cost to the **word-amortization/concept component**, not content-free naming. Secondary: deepseek's **+35 is a small, sign-robust (50/10), real positive** pure-label effect, so "no cost" overstates it for that model — the honest statement is "not robust across models / bidirectional," which the brief does say.

**Verdict:** **reproduced and survives.** Keep the demotion; re-anchor its warrant on the gemini difficulty-driven sign-flip (HARD_NONCE−HARD_WORD vs TRIV), not on the pure-label null alone.

---

### NF-C3 — "applying a harder predicate costs more; robust on 2/3 models" → **REPRODUCED** (qwen = underpowered, not flatly null)

**Recomputed.** HARD_PLAIN − TRIV_PLAIN: deepseek **+144** (CI[+97,+188], p<.001, 58/60 positive, d=0.84); gemini **+488** (CI[+305,+864], p<.001, 47/60, d=0.72); qwen **+112.8** (CI[−78,+242], p=.699, 32/28, d=0.19). All-completed identical (accuracy at ceiling). Stronger length control HARD_WORD − TRIV_PLAIN (WORD is 6 words *shorter*): deepseek +84 p<.001, gemini +265 p=.027, qwen −198 ns — **so the compute tax survives a length control that runs against it** on deepseek/gemini. This is the cleanest survivor in the NF battery.

**Sharpest flaw — "qwen null/noisy" conflates genuinely-null with underpowered.** Power analysis (bootstrap qwen's own deltas + injected shift) shows the apparatus detects a gemini-sized +488 ~100% of the time but a deepseek-sized +144 only **~66%** of the time. So qwen is genuinely null against a *large* effect but **underpowered against a deepseek-scale one** (could miss +144 a third of the time). qwen's noise is real symmetric dispersion (SD=640, skew=0.31, not a heavy tail), not truncation/accuracy. The +113 point estimate is same-signed but inside noise; at 4.5% of qwen's ~2516-token baseline (vs 111%/53% for deepseek/gemini), qwen's token count simply does not track predicate hardness. **"Robust on 2/3" is correct; qwen should be logged as underpowered-leaning-null, not "no effect."**

**Verdict:** **reproduced; the compute component is the most robust effect in NF.** Relabel qwen "underpowered-leaning-null."

---

## SV — application-free, same-task control

### SV-C1 — "D_application is the dominant cost and GROWS with substrate size, cleanly isolated" → **OVERSTATED**

**Recomputed.** D_app = rt(prime) − rt(verdict): deepseek +524/+1448/+1675/+1656/+4179/+7568; gemini +1480/+5419/+5047/+4885/+9300/+11980; qwen **−2416(F3)**/+3458/+3512/+2572/+6444/+10926. Growth is real, driven by the **prime side rising** with size while the verdict baseline stays small and *declines*. **Direction and dominance survive. Three over-claims attach to it.**

**Sharpest flaw — three concrete overstatements, none fatal:**
1. **"all p<.001" is false.** deepseek F3_FRAMED is p=.013 (12/2) and **qwen F3 sign-REVERSES to −2416.** The quoted p=.0001 is merely the **exact sign-test floor at n=14** — and V10 prime was run at **only 14 seeds**, not the 24 the instrument line implies (SV=24; intersection=14).
2. **"application-free" fails for qwen.** Traces show qwen misreads "verdict: PASS" as "verify the arithmetic" and **re-computes every chain** (100% of F3 traces, 58 arith-ops median) — the exact re-verification the attack warned of, and the cause of the F3 anomaly. Holds for deepseek/gemini ("prime" appears 0–1/576 traces, <5% recompute). So D_app is a **conservative lower bound** for qwen, but the verdict cell is not truly application-free.
3. **"only predicate removed" overstates isolation.** Prime and verdict share the needle arithmetic + truths (144/144 match), but **filler content, scatter positions, and per-line [verdict] tags all differ** — SV is a different, ~15% **longer** prompt. The length confound runs the *safe* way (the shorter prime prompt costs 30–50× more rt, so D_app is not a reading artifact), and gemini prime-accuracy survivorship (F1_L acc 0.696) censors the hardest prime items — **both make the headline conservative.**

**Verdict:** **direction survives, headline qualifiers do not.** Demote "all p<.001 / cleanly isolated / application-free" to "**application volume is the dominant, size-growing reasoning cost on deepseek/gemini; on qwen the verdict baseline is contaminated by re-verification (so D_app is a lower bound and F3 reverses).**"

---

### SV-C2 — "a real application-INDEPENDENT FRAME-ORIENTING cost survives; rescues V10's orienting" → **OVERSTATED** (the sharp one)

**Recomputed.** D_frame = F1_S − F2_DEINDEXED: deepseek **+113** (CI[+30,+140], p=.000); qwen **+372.1** (CI[+180,+598], p=.000); gemini **+405.0** (CI[+218,+794], p=.023); all n=24. Real effect, not artifact: prompt length is **matched** (F1_S median prompt_tokens is actually 8 *fewer* than F2) and accuracy is at ceiling (96/96 all models). **An application-independent frame cost is real. The "orienting" label is unwarranted.**

**Sharpest flaw — D_frame is a two-way confound, and V10c (the fix) was specified but never built.** Verified in `v_sv_verdict.py` (lines 87–95) that F2_DEINDEXED and F1_S share a **byte-identical body** (checked across 5 seeds) and differ in exactly **two entangled ways at once**: F2 = header present (*"The text below is a system log."*) + selector **LEADING**; F1_S = no header + selector **TRAILING**. So D_frame = (N_TRAIL − H_LEAD) = HEADER_main + POSITION_main + interaction — an **undecomposed sum.** A trailing selector forces the model to read ~24 substrate lines before learning the task, then re-locate the PASS line — a textbook **late-instruction rescan** that could fully account for 100–400 tokens. `AGY_V10C_BRIEF.txt` (lines 13–21) documents this *exact* {header}×{position} 2×2 confound and records that **both prior auditors (codex + Claude-subagent) independently named the 2×2 as the decisive next control.** There is **no `v10c_*.py` and no `v10c_run.*.jsonl`** — V10c was specified but **never built or run.** SV does not fix it: SV's clean contribution is on the **orthogonal task axis** (removing application volume: verdict vs prime); on the header/position axis it **inherits the V10 confound verbatim.** SV's D_frame is merely the verdict-task analogue of V10's still-confounded F0 falsifier.

**Verdict:** **demote.** "Orienting survives" → "**an application-independent frame-POSITION cost survives (real, length-matched), but orienting (header) vs late-instruction rescan (position) remains unseparated — V10c still required.**" The "rescue of V10's orienting" wording must be **held** until V10c runs.

---

### SV-C3 — "size axis null/negative under verdict → size cost is predicate-evaluation volume, not reading" → **OVERSTATED**

**Recomputed.** Size under verdict (per-seed paired, n=24): deepseek F1_M−F1_S=−55 (p=.307), F1_L−F1_M=−85 (p=.093); gemini +156 (p=.839), −307 (p=.541); qwen −283 (p=.023 sig-neg), −176 (p=.035 sig-neg). "Null/neg on all 3" confirmed and **robust**: per-seed monotone slope negative on all 3 (deepseek p=.002, qwen p=.002); pooled Spearman(size,rt) negative+sig on all 3 (ρ −0.26/−0.24/−0.49, p<1e-4); mean→median makes it *more* negative (not tail-inflation); input grows 3.8× while rt is flat/falls; accuracy ~100% (no survivorship). **The core conclusion — rt does not rise with reading volume — is the strongest-supported claim in SV.**

**Sharpest flaw — the "above the V10b lookup floor" premise degrades exactly at L, where the slope is read.** SV-verdict/lookup median ratio falls S→L: deepseek 2.31×→1.20×, gemini 6.83×→2.23×, qwen 1.59×→**0.98×**. Paired verdict−lookup at F1_L: deepseek +20 (p=.541) and qwen +35 (p=.839) are **statistically at the floor**; only gemini stays clearly above (+447, p=.002). So on **2 of 3 models the size null at the largest substrate is measured where SV has collapsed onto the locate-by-PASS floor** — the above-floor advantage the brief invokes has evaporated by L. (The brief's table also misstates gemini F1_L verdict as 800–1200; true value 370.)

**Verdict:** **conclusion survives** (rt *falls* with size — refutes any reading-volume cost regardless of floor proximity), but the **stated floor-margin is oversold.** Demote the "3rd confirmation, comfortably above floor" framing to "**size null/negative confirmed; on 2/3 models the largest cell sits at the lookup floor, so 'above-floor' is not the warrant — the negative slope itself is.**"

---

### SV-C4 — "verdict > lookup → the prime-task ANSWER FORMAT costs more, beyond application" → **OVERSTATED**

**Recomputed.** verdict − lookup: deepseek +12/+29/+68/+138/+119/+20; gemini +730/+1920/+669/+1124/+1325/**+447** (the brief's "+669→+1920" drops the true low cell +447 at F1_L); qwen +3099/+588/+226/+360/+143/+35. qwen F3_FRAMED verdict=5248 confirmed (vs prime 3170 → D_app = **−2416**, negative). **The gap is real; its attribution to "answer format" is wrong.**

**Sharpest flaw — the verdict task is not application-free, so "answer-format cost beyond application" is mislabeled.** The "exactly one PASS, report its value" framing makes the model **distrust the [verdict] tags and re-execute the arithmetic to audit them** — leaking back the application SV claimed to remove. qwen traces show median **35 "% 1000 =" evals at F3** (full re-run of all six five-op chains) vs 8 in lookup; re-verify-language fraction tracks the gap (qwen 90–100%, gemini 45%→6% F3→F1_L, deepseek 64%→9%). On qwen traces with **zero** arithmetic re-execution the F3 gap leaves only 1/24 seeds and goes non-significant at F1_S/M. It is also the **wrong contrast** for answer-format: lookup answers a literal, **unauditable** init value (51), while verdict answers a chain **final the model can and does re-derive** — that **auditability gap**, not "report-a-final format," drives the cost. Input-length refuted (d_rt/d_pt = 35 at the shortest cell → ~0 at the longest). **deepseek's small surviving gap (+12..+138, lowest re-verify rate) is the only part plausibly attributable to format/scan; gemini/qwen's large gaps are re-application.**

**Verdict:** **demote.** "Answer format adds cost" → "**the verdict framing re-triggers application (auditing the tags); only deepseek's small residual gap is plausibly format/scan.**"

---

## WATERLINE

**Everything reproduced. Nothing is killed. The apparatus is sound; the demotions are all interpretive over-reach corrected by trace evidence and confound disclosure.**

### The three-component decomposition — status

| Component | Status | What the audit did to it |
|---|---|---|
| **(1) APPLICATION volume** | **SURVIVES — strongest pillar.** | D_app dominant and size-growing on deepseek/gemini (SV-C1); the compute predicate-tax replicates under a length control that runs *against* it (NF-C3, d≈0.7–0.8). **But "all p<.001 / cleanly isolated / application-free" demoted:** qwen re-verifies (F3 reverses), prompts are not byte-isolated, V10-prime is 14 seeds not 24. Read it as a **lower bound**, robust in direction. |
| **(2) AMORTIZATION word-shortcut** | **DEMOTED to reading-length / concept-displacement.** | The headline "cached word cheaper to APPLY" (NF-C1) is a **narration-length artifact** — compute-markers are null, the un-amortized nonce FLONK is the *most* expensive HARD cell, length explains ~50–67%. What *does* survive is **NF-C2's residual**: a difficulty-driven concept cost isolated by gemini's HARD_NONCE−HARD_WORD (+614) vs TRIV (−306) sign-flip. So amortization is **not** "applying a cached word is cheaper"; it is at most "**displacing the spelled-out hard rule with one word removes reading+restating cost,**" with a small real concept component only at HARD difficulty. **"Label-binding always costs" stays demoted.** |
| **(3) FRAME-orienting** | **DEMOTED to frame-POSITION cost of unresolved mechanism.** | A real, length-matched, application-independent frame cost survives (SV-C2: +113/+372/+405). **But it is a header×position two-way confound** — orienting vs late-instruction rescan is **unseparated**, and the control that separates them (**V10c**) was specified in `AGY_V10C_BRIEF.txt` but **never built.** "SV rescues V10's orienting" is **not yet earned.** |

### One-line waterline
- **Survives clean:** the **compute predicate-tax** (NF-C3, deepseek/gemini, length-control-robust) and the **size→reading-volume demotion** (SV-C3, negative slope on all 3, survivorship-clean).
- **Survives as lower-bound / direction-only:** **application dominance** (SV-C1) — strip "all p<.001 / application-free / cleanly isolated."
- **Demoted, not killed:** the **word-shortcut amortization reading** (NF-C1 → reading-length), **frame-orienting** (SV-C2 → unseparated frame-position), and **answer-format cost** (SV-C4 → re-triggered application).
- **Reproduced and standing:** **NF-C2** (label-binding bidirectional/model-dependent), re-anchored on the difficulty sign-flip.

### SINGLE most important next control
**Build and run V10c** — the compute-free / verdict-task **{HEADER present | absent} × {selector LEADING | TRAILING}** 2×2, byte-identical body, length-matched neutral pad in the header slot (spec already fully written in `AGY_V10C_BRIEF.txt`). Report the **POSITION main effect** (mean(*_TRAIL) − mean(*_LEAD), perfectly length-matched) and the **HEADER main effect with position held constant.** This is the single control that gates the entire frame component: if POSITION swamps and HEADER's CI includes 0, the "orienting" survivor collapses to **late-instruction rescan** and SV-C2/V10 orienting demote; if HEADER stays significant with position held, orienting survives **sharpened.** Two prior independent auditors already named this 2×2 as decisive; it is specified and unbuilt. Until it runs, the "rescue of orienting" wording must be held.

*(Runner-up, decisive for the amortization component and cheaper: pre-register the **trial-division-marker count** — already null in NF — as the PRIMARY amortization endpoint instead of reasoning_tokens, which conflates compute with narration length. And a clean qwen fix for the application axis: re-tag the SV selector as a neutral non-evaluative marker — e.g. `[tag: KEEP]` — so qwen cannot read "PASS" as "verify the arithmetic," removing the re-verification contamination that reverses F3.)*
