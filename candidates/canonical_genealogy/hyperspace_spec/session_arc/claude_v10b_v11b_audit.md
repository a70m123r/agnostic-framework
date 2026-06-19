# AUDIT — V10b (compute-isolation) + V11b (compute-matched de-amortization)

**Auditor:** Claude (Opus 4.8 [1m]), lead synthesis over 6 adversarial verdicts (C1–C6).
**Date:** 2026-06-19 | **Stance:** skeptical, demote-not-kill. Numbers independently re-derived from the
locked `v11b_run.*.jsonl` / `v10b_run.*.jsonl` / `v10fs_run.*.jsonl`; the headline deltas reproduce **exactly**
(deepseek NOVEL +307.6, RENAMED +161.9, F0 +77.6; qwen NOVEL +836.1, F0 −172.1; gemini NOVEL +2150.8,
RENAMED median +241.0 / mean +315.8). Signal = `reasoning_tokens` on CORRECT calls, per-seed mean over 4 reps,
paired bootstrap median CI + exact two-sided sign test (n=28 V11b, n=24 V10b).

**One-line read:** the *instrument works and the central dissociation is real* (locating ≪ applying; un-amortized
concept costs more than the same-difficulty amortized one). But three of the six claims carry a label that the
data only **mostly** supports, and the cleanest "compute-identical" rung is identical in the **prompt**, not in the
**executed reasoning**. Demote the labels; keep the findings.

---

## Per-claim verdicts

### C1 — V11b headline: un-amortized concept costs more reasoning, compute-matched
**Verdict: REPRODUCED.**
**Recomputed:** NOVEL_RULE − NAMED_DEF = **+307.6 / +836.1 / +2150.8** (deepseek/qwen/gemini), p=.000 all, CIs
exclude 0, n=28. Survives on all-completed-incl-incorrect (gemini +2008, deepseek +297, qwen +836), so the gemini
NOVEL accuracy dip (103/112) does **not** manufacture it. Compute-match audited on the needle: prime trial-division
is *more* steps than WURF (11 vs 7 per seed; full 6-chain 534 vs 410), so any un-matched compute runs **against**
the headline — the effect is conservative, not inflated. Lock digest `d394534f…` recomputes; selftest 28/28 confirms
byte-identical needles across compute arms.
**Sharpest flaw:** the *label* "de-amortization of meaning = application cost" is clean for qwen/gemini but only
~75% clean for **deepseek**, whose F0 falsifier (+78, p=.013) survives with all predicate application removed — so
~1/4 of deepseek's headline is something other than pure concept-application (trust/verification or asymmetric
parsing of the unfamiliar WURF verdict lines). More deeply, "de-amortize an un-cached concept" and "apply a novel
rule explicitly" are not separable *in principle*; RENAMED (zero novel compute, still +cost) is the strongest
available wedge, but its gemini CI is wide.

### C2 — V11b RENAMED rung: pure label de-amortization, compute identical
**Verdict: REPRODUCED (number) / OVERSTATED (the word "identical").**
**Recomputed:** RENAMED_PRIME − NAMED_DEF = **+161.9 / +262.6 / +241.0** (median), sign-p .013/.004/.036 — all clear
.05. Byte-diff confirms the ONLY textual change is the token `PRIME→FLONK` (twice/seed); definition body, the 6
computations, and the needle are byte-identical. So the *required* computation is genuinely matched.
**Sharpest flaw:** "compute held EXACTLY fixed" is true of the prompt, **false of the executed trace**: 100% of
RENAMED records restate the def and perform an explicit `FLONK→prime` translation (e.g. 1053 rt vs 389 rt on a
matched seed pair), so the measured +cost **is** that translation/verification work — which is exactly the
de-amortization the rung intends to capture, but it is real extra executed compute, not a free-lunch label effect.
Statistically, **gemini is the weak leg**: under the more powerful Wilcoxon signed-rank it is **p=.053 (non-sig)**;
its mean (+316) is inflated by a single **+2590 outlier seed against a −1447 minimum** (heavy-tailed) — only the sign
test clears .05. deepseek and qwen are solid (Wilcoxon p=.002). The 2-of-3-robust rung stands; gemini's leg is
sign-test-only.

### C3 — V11b falsifier: the tax lives in concept-APPLICATION, not def-holding
**Verdict: OVERSTATED.**
**Recomputed:** F0_NOVEL − F0_NAMED = deepseek **+77.6** (CI[+17,+166], sign-p .013, Wilcoxon .005, t .004, MWU
<.0001 — survives **every** test); qwen **−172.1** (wrong sign, ns); gemini **+100.7** (CI spans 0, p=.572). The
brief's specific attack (recompute on all-completed) is a non-event: F0 accuracy is at ceiling, so all-completed ≈
correct-only. F0 prompts are word-matched and the novel def is 5 chars *shorter* — the task is genuinely
application-free.
**Sharpest flaw:** "vanishes on 2/3" is literally true, but "the tax is NOT in def-holding" is contradicted by its
own falsifier on deepseek. The +78 is bullet-proof, yet F0 requires ZERO application — trace inspection localizes it
to **reading/orienting around the unfamiliar definition** (deepseek 94/112 novel traces engage the def vs 22/112
named; def-engaging records carry ~2× rt). That is a **def-holding/comprehension cost** — precisely what C3 claims is
untaxed. The honest claim: the falsifier localizes **most** of the tax to application (F0 CI upper bounds are
53%/4%/16% of the respective headlines), not all of it. Separately, **gemini's "vanish" is underpowered** — its +101
sits below its own MDE (~274 tok), so its null cannot distinguish 0 from a real ~270-tok residual. So C3 is two flaws
at once: overstated (deepseek residual is real comprehension cost) AND underpowered (gemini).

### C4 — V10b compute-isolation: locating is near-floor, frame-insensitive
**Verdict: OVERSTATED.**
**Recomputed:** lookup medians deepseek 84/103/121, gemini 173/168/166, qwen 568/529/498 — D_compute vs V10 prime
= 20–67× / 36–77× / 8.5–21×. Lookup accuracy stays at ceiling at the largest size (the 4 deepseek "misses" are
finish=error transport failures, not lookup failures; only 1 genuine wrong answer in the whole run). No max-token
clamping. The **relative two-orders-of-magnitude claim is robust and unscathed.**
**Sharpest flaw:** "flat / frame-insensitive / 5× substrate adds ~0" is a **median artifact** that hides a genuine,
significant size trend in **deepseek**: full-span F1_L−F1_S = **+47 mean (CI[+6,+79], p=0.023)** and +34 median-
per-seed (p=0.007), 18/24 seeds up, mean rt climbing 103→142→202. The brief reported only the two adjacent (both ns)
steps and labeled the axis "~null," hiding the significant full-span climb. "Near-floor" is correct; "flat/~0" is
overstated — the honest statement is **"lookup is ~0.7% of the compute slope,"** not literally zero. No hard floor
exists (global min rt 29/56/105), so this is a real-but-tiny reading cost, not a saturated floor.

### C5 — V10b size-axis reinterpretation: reading-volume → predicate-evaluation-volume
**Verdict: REPRODUCED.**
**Recomputed:** prime size step F1_M−F1_S = +2578/+4377/+3068 (p≤.002); lookup F1_L−F1_S = +37/−7/−70 (ns).
Per-input-token reasoning slope differs 50–140× (lookup ~+0.02, prime ~+1.4); prompt_tokens matched within ~30
between tasks at every size, so the dissociation is **not** an input-length artifact. The rename
reading-volume→predicate-evaluation-volume is **correct** — identical substrate, lookup ignores the arithmetic lines
(flat rt), prime evaluates each (rt scales with predicate count).
**Sharpest flaw:** **differential survivorship.** Prime medians are over correct survivors only, and gemini prime
accuracy collapses with size (52→49→39/56), so the hardest/costliest prime items are censored out — the cross-task
contrast pits a full lookup sample against an increasingly filtered prime sample. This biases the prime size cost
**downward** (so the dissociation is conservative, not inflated — the *direction* is safe), but the exact gemini
magnitude is unclean. Secondary: deepseek lookup is not literally zero (the C4 +47 climb), so C5's "~0" is true only
to first order. The reinterpretation survives; one quoted magnitude is contaminated.

### C6 — V10b frame-cost refinement: V10's F0 residual was primality-application, not pure orienting
**Verdict: OVERSTATED.**
**Recomputed:** gemini F0_DISSOLVED−F0_DEINDEXED = +2302.8 (p<.001); the application-free lookup analog
F1_S−F2_DEINDEXED = gemini +23.2 (ns, ~0), deepseek +19.1 (p=.023), **qwen +142.5 (p=.007)**. So the gemini-specific
"big F0 residual collapses to ~0 under lookup" reproduces. Trace evidence is decisive: in F0_DISSOLVED gemini ignores
the pre-given `=>` finals and re-runs the full evaluate-all primality sweep; in lookup it does pure read-for-name.
**Sharpest flaw:** three problems. (1) **Not a clean subtraction** — F0 and lookup remove compute via different
*strategies* (evaluate-ALL-6-lines vs read-for-ONE-named-line), so the +2303 confounds "primality predicate" with
"process-all-6 vs 1"; you cannot attribute it to primality alone. (2) **Over-generalizes from gemini** — deepseek/qwen
had small F0 residuals to begin with, and qwen's truly application-free LOOKUP residual is itself **significantly
positive (+142.5, p=.007)**, directly contradicting "residual frame cost is tiny." (3) The gemini gap is partly a
**dissolution-triggered TRUST flip** (trust finals when indexed = 0.30×; distrust + re-derive when dissolved = 0.73×)
— which is itself an *orienting* phenomenon, so "largely primality-application, not orienting" mislabels the
mechanism. The phenomenon is real and gemini-reproduced; the universal/clean label is overstated.

---

## WATERLINE

**What survives as a finding (above the line — bankable):**
1. **The latent camera dissociates locating from applying by ~1–2 orders of magnitude** (C4/C5 relative claim, all 3
   models, D_compute 8.5–77×). This is the load-bearing result and it is robust to every attack tried — survivorship
   only makes it *more* conservative.
2. **An un-amortized concept costs more reasoning than the same-difficulty amortized concept, with the needle
   isomorphic and the compute residual running against the effect** (C1 headline, +308/+836/+2151, p<.001 all,
   survives incl-incorrect). V11's earlier negative is confirmed dead — it was 100% the predicate-difficulty artifact.
3. **A pure-label de-amortization cost exists on ≥2 of 3 models** (C2 RENAMED, deepseek/qwen Wilcoxon p=.002): merely
   renaming `PRIME→FLONK` with byte-identical computation still costs reasoning.
4. **The size axis is predicate-evaluation volume, not reading volume** (C5): lookup is flat under 5× substrate while
   prime scales steeply; the V10 "universal reading-volume cost" is correctly demoted.

**What must be DEMOTED (label too strong, finding intact):**
- **C2 "compute held EXACTLY fixed" → "required computation fixed; the model does real translation work."** The +cost
  is the executed de-amortization, not a free-lunch label effect. Gemini's RENAMED leg → **sign-test-only / heavy-tailed**
  (Wilcoxon p=.053); report it as 2-of-3-robust.
- **C3 "the tax is NOT in def-holding" → "MOST of the tax is application (F0 ≤53%/4%/16% of headline); a residual
  reading/comprehension cost remains, proven on deepseek (+78, every test)."** Re-label as *application-dominant*, not
  *application-exclusive*. Gemini's "vanish" is underpowered, not demonstrated.
- **C4 "flat / ~0 / frame-insensitive" → "near-floor, ~0.7% of the compute slope."** Deepseek carries a small but
  significant full-span size climb (+47, p=0.023) the median masked. The relative claim is untouched; only the word
  "flat" is demoted.
- **C6 "V10 frame-cost was largely primality-application (universal)" → "gemini-reproduced; confounded with
  evaluate-all-vs-read-one and partly a trust-flip; qwen's lookup residual is itself significantly positive."**
  De-universalize and re-label the mechanism as *not a clean subtraction*.

**What is INVALID-AS-DESIGNED (cannot answer the question it was built to answer):**
- **No claim is invalid.** The nearest is **C6's subtraction**: because the two ablations change model *strategy*
  (evaluate-all vs read-one), the F0−lookup contrast cannot cleanly isolate "the primality predicate" from "the
  number of lines processed." As an *estimate of the primality-application share* it is confounded; it is still a
  valid demonstration that gemini's V10 F0 residual collapses under a genuinely application-free task. Treat C6 as a
  qualitative reproduction, not a clean decomposition, until the strategy-matched control runs.

**Honest scorecard:** 2 clean reproductions (C1, C5), 1 reproduced-number/overstated-word (C2), 3 overstated labels
over intact findings (C3, C4, C6). Zero refutations. Zero kills. The instrument and the central dissociation are
sound; the prose oversells four labels by treating "application" as exclusive, "compute" as executed-identical, and
"flat" as literally zero.

---

## THE SINGLE MOST IMPORTANT NEXT CONTROL

**A NOVEL_FAMILIAR / def-holding-isolation arm** — one control settles the largest shared ambiguity across C1, C2,
and C3 (and feeds C6): *is the de-amortization tax the cost of holding/reading an unfamiliar label-and-rule, or the
cost of applying novel predicate volume?*

Add a condition that is **equally non-prebound as a token but built from a single familiar, already-amortized
predicate**, with verdicts NOT pre-given (real application) — e.g. `ZILP = "ends in 3 or 7"`: a novel name + a
trivial cached computation. Token-matched (not just word-matched) against both NAMED_DEF and NOVEL_RULE. Two readings
fall straight out:
- If **ZILP still costs ≈ the WURF/NOVEL tax**, the cost is **label/instruction-following de-amortization** (reading
  and binding an unfamiliar rule) — which promotes C3's deepseek residual to the headline mechanism and demotes
  "application volume."
- If **ZILP drops to ≈ RENAMED levels**, the residual WURF excess is **genuine multi-clause application volume** —
  which vindicates C1/C3's "application" label and confines de-amortization to the small RENAMED rung.

This single arm is decisive because it varies *novelty of label* and *amount of cached compute* independently — the
one axis every contested verdict (C1 label, C2 "identical," C3 application-vs-holding, C6 evaluate-all confound)
ultimately turns on. Run it n≥60 on the F0 cells in the same pass so gemini's MDE drops below ~120 tok and its
chronically underpowered nulls (C3, C6) finally become powered rather than merely non-significant.
