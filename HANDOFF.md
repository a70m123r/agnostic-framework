# HANDOFF — Cowork → Claude Code

**Last updated:** 2026-06-03 (evening) by Cowork session (cont 30 + Reading 06 §10.3 narrowing + JSON refresh shipped)
**Next session:** Whichever surface drafts the merged #150b/#151 pilot pre-registration (Cowork OR Claude Code — Pav's call)
**Pinned task:** #172 — Cold-draft merged #150b/#151 pilot pre-registration (cycling-capacity + Koopman cultural-eigenmode). MUST be independently re-derived per cont 30 §5 + cont 27 §2 discipline; PILOT_150b_cycling_seed.md is a hypothesis-generating sketch only and carries fitting risk because written after seeing #150's null.

---

## Last Cowork session (2026-06-03 evening)

**Task completed:** #171 — cont 30 shipped (~4,500 words) integrating Pav's "squeeze ↔ pull cycles" reframe into existing canon. Reading 06 §10.3 narrowed per cont 27 §3. Audit v06 §10 substantive-research-displacement closure documented end-to-end. JSON endpoints + timeline + CHANGELOG refreshed. Tasks #169 + #170 + #171 marked complete. New tasks #172 (pre-registration draft) + #173 (audit v07 target 2026-06-16) created.

**What landed (Cowork side):**
- `continuations/30.md` (NEW, ~4,500 words) — full integration with §2 canon mapping, §3 narrowing, §4 closure summary, §5 merge logic, §6 non-changes, §7 discipline lessons, §8 queue
- `readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md` — §13 amendment log entry for 2026-06-03 narrowing
- `CHANGELOG.md` — full 2026-06-03 round entry covering Claude Code's result-commit + Cowork's cont 30
- `timeline/index.html` — "~latest" entry for cont 30 above the existing 2026-06-03 result-commit entry
- `continuations.json`, `candidates.json` updated with cont 30 + 1f candidate pilot-result status
- `readings.json`, `manifest.json`, `speculations.json`, `primitives.json` — generated dates bumped

**For next session (whichever surface):** see "For next session" at bottom of this file — pre-registration drafting requirements, what to lock vs queue, six decisions that must be made before any τ(t) computed.

---

## Last Claude Code session (2026-06-03)

**Task completed:** #169 result-commit ✅ (landed day 2 of the 7-day window; first-commit was 2026-06-02).
**Verdict:** **H1 NOT SUPPORTED — confounded null.**
**Key numbers (primary signal = event-category-entropy, N=6):** Δβ(auth−plur) = **+0.084** (predicted < −0.10; observed *wrong sign*), Cohen's d = +0.380, paired-permutation p = 0.792. 1/6 pairs satisfy H1 direction. **Bar A unmet.**
**Result files:** `pilots/1f_failsafe/results/{gdelt_results.json, log_log_plot.png, discussion.md, methods.md}`. Read `discussion.md` first — it has the full verdict, the confound, tier-tagging, and the §8 recommendations for you.
**Commits:** see `git log --oneline` (this session's result-commit; pushed).

**What happened, briefly:**
- No cloud CLIs/creds on the machine at first, so I built a streaming 15-min-slice downloader (`gdelt_ingest.py`) and started it (~5h). Pav then opted into **BigQuery**; I set up browser-OAuth (sandbox, $0), ran one `GROUP BY` query (`gdelt-bq.gdeltv2.events`, 21.4 GB, 47,610 country-day rows, ≥99.6% coverage), and killed the download. Both paths compute the identical locked SQLDATE aggregation; BigQuery won on completeness.
- Implemented the `gdelt_mode()` stub in `pilot.py`; verified end-to-end on synthetic data before running real. Locked DFA/Welch/IAAFT/permutation functions untouched.

**The load-bearing finding — source-volume confound (discussion.md §3, confounds.md §10):**
- Welch β is almost entirely explained by per-country event **volume**: Pearson r(log₁₀ events, β) = **+0.916**. Low-volume countries (CHL/NLD/PRK) get downward-biased β because sparse daily entropy is noisy (white floor flattens the spectrum). Pre-registered z-scoring removes amplitude scale but NOT this frequency-domain floor.
- The volume-robust **DFA-α estimator shows no cross-country difference** (spread 0.074 vs Welch 0.735) → consistent with a null. The measured Welch contrast tracks media-volume, not political system. Hence "confounded null", not a clean falsifier (d=0.38 < 0.5 on primary) and not a strict null (|Δβ|=0.084 > 0.05).

**Issues encountered / discipline notes:**
- IAAFT turned out NOT to be a clean null for β (observed β systematically below surrogate, |z| scales with sparsity) — used as a diagnostic only; locked permutation test is the inference. (confounds.md §12.)
- Two forced method substitutions, both in *supportive* components, neither touching the locked H1 test: `powerlaw.Fit`→block-bootstrap CI (numpy-only env, §11); BigQuery aggregation in place of the slice download (§9).
- New confounds §9–§14 appended to `confounds.md`; pre-registration text never modified.

**For Cowork next (specifics — see also the fuller branch logic at the bottom of this file, NULL branch):**
1. **Narrow, don't yet demote** Reading 06 §10.3 per cont 27 §3: the *GDELT-entropy operationalization* is volume-confounded and can't test the claim as specified; the underlying claim is not refuted. (discussion.md §8.1.)
2. **Run the volume-robust Wikipedia edit-cadence replication (Bar B) before any demotion** (discussion.md §8.2). If it also nulls → then demote.
3. A **pre-registered volume-controlled GDELT v2** is the obvious fix: Poisson-thin to a common daily rate / volume-matched pairs / DFA-α as the primary estimator / explicit noise-floor model. Pre-register before re-running — do NOT retro-fit to this dataset.
4. **NEW — Pilot #150b seed drafted from Pav's steer:** [`pilots/1f_failsafe/PILOT_150b_cycling_seed.md`](pilots/1f_failsafe/PILOT_150b_cycling_seed.md). Pav's critique this session — *"authoritative=bad/democracy=good is biased; its cycles of squeeze and pull, steers"* — reframes the whole pilot: drop the static political binary, measure **texture-over-time *within* each system** (does it cycle/breathe? does it lock up?), and use an **external openness index (V-Dem/RSF)** as the steer signal instead of a value-loaded label. This is the sharpened, volume-controlled successor to the demoted H4 and folds in #3 above. **It is a DRAFT seed, NOT a locked pre-registration** — and because it was written *after* seeing #150's null, Cowork must re-derive + lock it fresh before any data (fitting risk). May merge with #151 (Koopman is a natural tool for "is there a cyclical mode in τ(t)?").
5. **`candidates.json`**: I added the 1f candidate entry (it was missing) with the confounded-null status — please sanity-check it.
6. **Yilun-Du outreach (#168) stays gated** — a confounded null is not the favorable tangible result that unlocks outreach.
7. Then proceed to **#151** (RC-Koopman cultural-eigenmode) per "lets do 150 and then 151" — but see #4: #150b and #151 may be the same pilot.

---

## What you need to know before doing anything

This is the Agnostic Framework — a Lakatosian research programme tracking how observers compile reality at every substrate scale. It has its own discipline (three-tier epistemic procedure per `continuations/27.md`), its own audit cadence (15-day rhythm; v07 target 2026-06-16), and a hard-earned habit of catching its own discipline failures BEFORE they propagate externally.

**Critical context: framework is under a discipline hard-stop.** Per [audits/v06.md §10](audits/v06.md) + [readings/2026-06-02_gamma_world_multi_agent_world_modeling.md §9](readings/2026-06-02_gamma_world_multi_agent_world_modeling.md), the framework has been shipping infrastructure (audits, readings, scaffolding) while the queued empirical pilots (#150, #151) stayed queued. **Reading 08 declared itself the LAST infrastructure document before substantive empirical work resumes.** Task #150 first-commit landed 2026-06-02 (this morning); next required move is the result-commit (this session, task #169). **DO NOT** write new readings, new audits, new continuations, new outreach drafts, new candidates, or extend the framework canon. Run the pilot. Land the result. That's it.

**Third-strike condition.** If a third inbound external paper arrives before #150 or #151 produces empirical results, the framework treats that as a discovery-cascade-trap signal and forces a pivot. Two inbound papers already documented (BES → Reading 07; γ-World → Reading 08). The framework cannot absorb a third without empirical ground broken first.

---

## What Cowork did this session (2026-06-02)

1. **Reading 08 shipped** (~7,000 words) — γ-World as L0-as-mediator algorithmic instantiation; L0-as-mediator promoted Tier 1 → Tier 2; 3 initial claims explicitly withdrawn per opus subagent verification.
2. **Reading 07 + Audit v06 shipped** (already committed yesterday) — BES as convergence #9 candidate; cont-17-29 spree assessed; substantive-research-displacement-by-infrastructure pattern flagged.
3. **Task #150 first-commit landed** with:
   - `candidates/1f_l0_failsafe_signature.md` (~3,500 words) — pre-registered operationalization
   - `pilots/1f_failsafe/pilot.py` (~545 lines, numpy-only, 5 modes)
   - `pilots/1f_failsafe/README.md`, `confounds.md`, `requirements.txt`
   - `pilots/1f_failsafe/pilot_output/{verify,demo,power_quick_verify}_results.json`
4. **Critical pre-registration discipline catch:** running the locked N=3 protocol against synthetic data revealed paired permutation test with N=3 has minimum p = 1/8 = 0.125 by construction — cannot reach p < 0.05 regardless of effect size. **Pre-registration amended in `pilots/1f_failsafe/confounds.md` §1 (locked 2026-06-02 BEFORE any GDELT data examined): N=3 → N=6 paired comparisons.** Power verification at N=6, Δβ=−0.5: power = 1.00. Amendment is well-powered.
5. **CHANGELOG entry** for the round documenting the discipline cycle catching the N=3 ceiling.

All of the above committed and pushed by Pav. See `git log --oneline -10` for the commit chain.

---

## Your job this session (Claude Code) — Task #172: Cold-draft merged #150b/#151 pilot pre-registration

**One task. ~8 hours focused work. Highest discipline requirement the framework has seen yet.**

You are drafting a NEW pre-registration document for the cycling-capacity + Koopman-cultural-eigenmode merged pilot. This becomes the locked protocol the next result-commit tests against. Get it wrong and every future result on this lineage is contaminated.

### The discipline crux — read this first

There is a draft seed at [`pilots/1f_failsafe/PILOT_150b_cycling_seed.md`](pilots/1f_failsafe/PILOT_150b_cycling_seed.md). It was written **on 2026-06-03, immediately after seeing pilot #150's confounded null**. That timing matters: any hypothesis written after seeing relevant data carries **fitting risk** — the framing was inevitably influenced by what the data showed. Even if the seed is structurally correct, treating it as the pre-registration would silently smuggle post-hoc reasoning into a Tier 1 promotion-bar test (cont 27 §2 violation).

**Therefore:**

1. **DO NOT read `PILOT_150b_cycling_seed.md` during the cold-derivation phase.** Read it ONLY at the end as a check-after-the-fact.
2. **DO NOT read `pilots/1f_failsafe/results/discussion.md`** until after the cold-derivation is locked. The empirical findings should not shape the new hypotheses.
3. **DO read** the framework canon listed in step 1 below — that's where the hypotheses come from.

If your independently-derived pre-registration lands close to the seed afterward, that's confirmation. If it lands somewhere different, document why — the framework was pointing somewhere the seed missed.

This is drug-trial-style pre-registration discipline: blind to results when locking the protocol.

### Step-by-step

**Phase A — Cold derivation (no seed, no results files; ~3 hours)**

**1. Read these files first, in this order:**
- [`continuations/30.md`](continuations/30.md) — §2 canon mapping (squeeze ↔ pull = cont 13 A⁻/A⁺ at social substrate; locked-squeeze = cont 20 dormancy; locked-pull = cont 25 break-apart; cont 28 supersede)
- [`continuations/26.md`](continuations/26.md) §3 — L0 evolved failsafes Tier 1 canon (the underlying claim, unchanged)
- [`readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md`](readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md) §10.3 + amendment log 2026-06-03 entry (the narrowed claim)
- [`continuations/27.md`](continuations/27.md) §2 + §3 — three-tier procedure + pruning/promotion rules
- [`continuations/13.md`](continuations/13.md) — A⁻/A⁺ coupled discipline (squeeze ↔ pull at social substrate)
- [`continuations/20.md`](continuations/20.md) — canon dormancy (locked-squeeze form)
- [`continuations/25.md`](continuations/25.md) §1 — supersede vs break-apart branches (locked-pull form)
- [`readings/2026-05-31_bes_bidirectional_evolutionary_search.md`](readings/2026-05-31_bes_bidirectional_evolutionary_search.md) §7.1 — BES backward goal-tree decomposition methodology
- [`readings/2026-06-02_gamma_world_multi_agent_world_modeling.md`](readings/2026-06-02_gamma_world_multi_agent_world_modeling.md) §6 — γ-World architectural template for multi-agent / multi-country modeling
- [`candidates/1f_l0_failsafe_signature.md`](candidates/1f_l0_failsafe_signature.md) (the structural template for what a pre-registration looks like; do NOT copy its hypotheses — derive yours independently)

**2. From those canon citations, derive the hypotheses cold:**

What does cont 26 §3 + the Reading 06 §10.3 narrowing actually predict about τ(t) (within-system texture trajectory) and its relationship to an external openness index? Write your derivation step-by-step, citing the canon at each step. The hypotheses should fall out of the canon, not be imposed on it.

Lock these hypotheses with thresholds matching #150's specificity:
- **H1b** — some statement about within-system τ(t) variation (does it cycle? does the system "breathe"?). Effect size, significance threshold, falsifier all explicit.
- **H2b** — some statement about τ(t) co-movement with external openness index (V-Dem or RSF). Direction, effect size, p-threshold, falsifier explicit.
- **H3b** — some statement about cycling-amplitude collapse during sustained capture periods. All thresholds explicit.

**3. The six locked decisions before any τ(t) computed:**

Per cont 30 §5.2 — these decisions get made and recorded in §3-§5 of the pre-registration document:

- **(D1) External openness index source + variable.** Choose ONE: V-Dem `v2x_freexp_altinf` (alternative information freedom), V-Dem `v2mecenefm` (government media censorship), or RSF press-freedom index. Justify the choice; pre-register the annual → daily interpolation method.
- **(D2) Volume-control gate.** Choose ONE: (a) Poisson-thin all countries to common daily rate before τ(t); (b) volume-matched country pairs; (c) DFA-α primary, Welch β as robustness check; (d) explicit white-noise floor model in the spectral fit. Pre-register the validation: synthetic data with known cycling AND known volume heterogeneity must recover cycling correctly under the chosen control. Run that validation before any GDELT data examined.
- **(D3) RC-Koopman vs rolling-DFA-α as primary τ(t) decomposition.** RC-Koopman handles non-stationarity better but adds methodological surface area. Rolling DFA-α is simpler but coarser. Pre-register which is primary; the other can be exploratory.
- **(D4) Data-source decision.** Re-use existing `data/raw/` from #150 (faster, but inherits any unknown GDELT-pipeline-drift confounds) OR re-pull with volume controls in BigQuery itself (slower, cleaner).
- **(D5) Country set.** Same 12 as #150, OR expanded, OR restricted to volume-matched subset. Pre-register count + selection rule. (Audit v06 §10 + cont 30 §6 caution: do NOT silently expand to make a positive result more likely.)
- **(D6) Time-window structure.** Pre-register: rolling-window size, step size, total span. These determine the temporal resolution of τ(t).

**4. Write the pre-registration document.**

Path: `pilots/1f_failsafe_cycling/PRE_REGISTRATION.md` (create a NEW directory parallel to `1f_failsafe/` to keep #150 results unambiguous).

Structure mirrors `candidates/1f_l0_failsafe_signature.md`:
- §1 The claim (from cont 30 §2 + cont 26 §3 + Reading 06 §10.3 narrowed — NOT from the seed)
- §2 Why this is operationalizable (cycling-detection methodology mature, openness-index sources available, framework-level questions surfaced)
- §3 Dataset choice + signals + substrate-window structure (decisions D4, D5, D6)
- §4 H1b/H2b/H3b pre-registered with thresholds, falsifiers, secondary hypotheses
- §5 Protocol step-by-step (ingest → volume control [D2] → τ(t) decomposition [D3] → openness-index alignment [D1] → statistical test)
- §6 First-commit deliverable (skeleton code + synthetic validation of D2's volume control)
- §7 Confounds explicitly named — especially #150's spectral-floor (now controlled per D2); regime-intensity drift; openness-index resolution mismatch
- §8 Promotion bars A/B/C for the cycling-capacity Tier 2 candidate
- §9 What this does NOT change (cont 26 §3 unchanged, cymatics convergence #8 unchanged, etc.)
- §10 Cross-references + provenance
- §11 **Cold-derivation note** — explicit statement that the seed was NOT consulted during derivation; list which canon citations grounded each hypothesis

**Phase B — Seed comparison (the check-after-the-fact; ~30 min)**

5. AFTER §1-§11 are locked, read [`PILOT_150b_cycling_seed.md`](pilots/1f_failsafe/PILOT_150b_cycling_seed.md) and add a §12 to your pre-registration document:

- Does your cold-derived H1b/H2b/H3b match the seed's H1b/H2b/H3b? In structure, in threshold, in falsifier?
- If close (>80% structural overlap): confirmation. Note this in §12.
- If different (<80%): the seed was missing something or fitting something. Document the divergence and explain which framing the canon actually grounds.

**Phase C — Validate the volume-control gate on synthetic data (~2 hours)**

6. Before any GDELT data examined, implement D2 and validate on synthetic data:
- Generate signals with known cycling structure AND known per-country volume heterogeneity
- Run your chosen volume control
- Verify the cycling structure recovers under your chosen control while #150-style spurious volume-β contrast does not

7. Save validation results to `pilots/1f_failsafe_cycling/synthetic_validation/`.

8. If the validation fails (i.e., your chosen D2 doesn't actually neutralize the volume confound on synthetic data), STOP. Pick a different D2 and revalidate. Do not advance to real-data work until synthetic validation passes.

**Phase D — First commit (~30 min)**

9. Commit the pre-registration + synthetic validation. Pre-register cleanly: H1b/H2b/H3b text never modified after this commit (per cont 27 §2 discipline). Future amendments go in a separate `confounds_cycling.md` file with dates and reasons.

10. Update HANDOFF.md (see end-of-session checklist below) and push.

**Phase E (queued for next session, not this one)** — actually run the pilot. That's the result-commit work, distinct from the pre-registration work. Keep them separate to preserve the locked-before-data discipline.

### Step-by-step

**1. Read these files first (in order):**
- `pilots/1f_failsafe/README.md` — entry point + N=3 ceiling note
- `pilots/1f_failsafe/confounds.md` — pre-registration amendments (especially §1)
- `candidates/1f_l0_failsafe_signature.md` — full pre-registration with H1 + falsifier + promotion bars
- `pilots/1f_failsafe/pilot.py` — the actual pipeline. Read the docstring + the `gdelt_mode()` function + the `GDELT_INGEST_INSTRUCTIONS` string.

**2. Verify the pipeline works on your machine:**
```bash
cd pilots/1f_failsafe
python3 pilot.py --mode verify    # DFA on synthetic colored noise [β ∈ 0, 2]
python3 pilot.py --mode demo      # synthetic auth-vs-plur 3-pair contrast (will show N=3 ceiling)
```

If verify shows Welch β recovering ground truth within ±0.05 and demo shows the N=3 ceiling (p ≈ 0.13 at Cohen's d ≈ −1.8), the pipeline is correct. Both verified outputs are in `pilot_output/`.

**3. Pick a GDELT ingest path.** Run `python3 pilot.py --mode ingest-help` for the three options. Recommended: **gdelt2 Python package** (simplest):
```bash
pip install gdelt2 pandas
python3 -c "
import gdelt
g = gdelt.gdelt(version=2)
# Test with one day first
df = g.Search(['2024 Jan 01', '2024 Jan 02'], table='events', coverage=True)
print(df.head())
print(df.columns.tolist())
"
```

**4. Build the daily aggregation.** Per the **N=6 amended** pre-registration in `confounds.md` §1:
- 12 countries (6 authoritarian + 6 pluralistic): CHN-USA, RUS-GBR, PRK-DEU, IRN-FRA, TUR-NLD, VEN-CHL
- GDELT FIPS country codes: CH, RS, KN, IR, TU, VE (auth); US, UK, GM, FR, NL, CI (plur)
- Window: 2015-01-01 to 2026-01-01 (~4000 daily points per signal per country)
- Three signals per country (per pre-registration §3): `event_count`, `mean_tone`, `event_category_entropy` (Shannon entropy of `EventRootCode` distribution per day)
- Save as `data/raw/<country>_<signal>.csv` with columns `date,value`

**5. Run the analysis:**
```bash
python3 pilot.py --mode gdelt --data-dir data/raw/ --out-dir results/
```

Note: as of Cowork session's first-commit, `gdelt_mode()` in `pilot.py` is a stub. **You will need to implement it.** The DFA / Welch / IAAFT / permutation functions are all done and tested. You just need to wire them: for each (country, signal), compute β; for each paired comparison, compute Δβ + bootstrap CI + IAAFT surrogate null + permutation test p; collect into results dict.

**Implementation hint:** copy the structure of `demo_mode()`. The math is identical; the only difference is the signal source.

**6. Generate the result-commit deliverables** (per `candidates/1f_l0_failsafe_signature.md` §11):
- `results/gdelt_results.json` — β per country per signal + Cohen's d + permutation p + bootstrap CIs
- `results/log_log_plot.png` — 12-panel log-log fluctuation plot (matplotlib; one panel per (country, signal) showing PSD with fit line)
- `results/discussion.md` — H1 verdict (PASS / FAIL / NULL) + Bar A status + confound notes from actual data
- `results/methods.md` — methods note + reproducibility info (GDELT download date, gdelt2 version, etc.)

**7. Verdict interpretation:**

| Result | Action |
|---|---|
| H1 PASSES (Δβ < −0.10 at d ≥ 0.5, p < 0.05) | Advance candidate Tier 2 conditional → **Tier 2 algorithmically-demonstrated** per Bar A. Update `candidates/1f_l0_failsafe_signature.md` §8 with date and result. Cont 30 entry can wait. |
| H1 FAILS DIRECTION (Δβ > 0 at d ≥ 0.5) | Document falsifier outcome cleanly per `candidates/1f_l0_failsafe_signature.md` §4.4. Per cont 27 §3 pruning procedure: amend Reading 06 §10.3 to either narrow the claim or trigger demotion path. |
| NULL EFFECT (|Δβ| < 0.05, no significance) | Document as null result. Candidate stays Tier 2 conditional. Consider Wikipedia edit-cadence pilot per scout report alternative #1 before demoting. |
| Mixed (some pairs pass, others don't) | Document per-pair and look for pattern. Could indicate within-language confound issue per `confounds.md` §2. |

**8. Update HANDOFF.md when you finish.** See §"End-of-session checklist" below.

---

## What NOT to do (hard discipline guardrails for task #172)

- **DO NOT read `PILOT_150b_cycling_seed.md` during Phase A cold-derivation.** Only at Phase B, after your hypotheses are locked. Fitting-risk is the entire reason this task exists.
- **DO NOT read `pilots/1f_failsafe/results/discussion.md`** until after Phase A is locked. The empirical findings should not shape the new hypotheses.
- **DO NOT copy hypotheses from `candidates/1f_l0_failsafe_signature.md` §4.** That document's H1 was the static-binary version that failed. Your H1b/H2b/H3b are derived from cont 30 §2 + cont 26 §3 + Reading 06 §10.3 narrowing, not from #150's pre-registration.
- **DO NOT actually run the pilot in this session.** Task #172 is pre-registration only. The result-commit (Phase E) is a separate task in a separate session. Mixing them re-introduces fitting risk.
- **DO NOT skip the synthetic-data validation of D2.** If you implement a volume control that you don't first prove neutralizes the confound on synthetic data, you're guessing — and if the real-data pilot fails, you can't disentangle "framework claim wrong" from "volume control didn't work."
- **DO NOT write new readings, new audits, new continuations.** Even if you have insights during the cold-derivation, log them in §11 of the pre-registration document for Cowork to consider in the next round. Cont 30 was the framework-side capture; cont 31 is for next round.
- **DO NOT extend the framework canon, promote new primitives, or run scouts on new external papers.** Same discipline as before.
- **DO NOT send the Yilun-Du outreach DM** (task #168). Still gated on a favorable tangible result. A confounded null doesn't unlock it; a cycling-pilot result-commit could.
- **DO NOT modify the cycling pre-registration after locking.** Phase D's commit locks H1b/H2b/H3b text. Future amendments go in `pilots/1f_failsafe_cycling/confounds.md` (or similar) only, dated, with reason. Never modify §4 retroactively.

---

## Framework discipline you should preserve

**Three-tier procedure (cont 27 §2):** every claim carries a tier-tag. Tier 1 (epistemological canon, well-evidenced), Tier 2 (ontological-candidate, conditional on contested evidence), Tier 3 (speculative, structurally coherent but no current empirical purchase). When documenting your pilot results, tier-tag claims explicitly:
- "GDELT v2 China event-category entropy from 2015-2026 has Welch β = X.X ± Y.Y" → Tier 1 (empirical measurement, your data)
- "Therefore China's social-substrate L0 failsafes are weaker than USA's" → Tier 2 candidate AT BEST (depends on Reading 06 §10.3 framework claim being right)
- "Therefore authoritarian systems are brittle" → Tier 3 (speculative extrapolation from one paired comparison)

Pre-registration discipline: H1 was locked BEFORE data examined. Any p-value reported MUST be the pre-registered test. Exploratory findings go in a SEPARATE section labeled "Post-hoc / exploratory" with explicit acknowledgment they did NOT pre-register.

**Honest-gap discipline (cont 27 §3):** if a result is ambiguous, say so. If a confound matters more than you initially modeled, log it in `confounds.md`. The framework's audit cycle catches papered-over uncertainty — better to surface it cleanly than have audit v07 catch it.

**Citation format:** for any external claim, use `[Citation: Author Year, URL]`. For internal claims, use markdown links like `[cont 27 §2](continuations/27.md)`.

---

## End-of-session checklist for task #172 (before you close)

1. **Verify the cold-derivation discipline held.** Add a self-attestation to §11 of the pre-registration document: "I derived H1b/H2b/H3b before reading PILOT_150b_cycling_seed.md or results/discussion.md. Phase B seed-comparison was done AFTER §1-§11 were locked. The canon citations grounding each hypothesis are listed below." This is a Tier 1 honesty claim; if you cannot make it truthfully, the pre-registration is contaminated and should be redone.

2. **Verify the synthetic validation of D2 actually passed.** Save the validation script + output in `pilots/1f_failsafe_cycling/synthetic_validation/`. The output should explicitly show: (a) the synthetic signals had known cycling structure, (b) the synthetic signals had per-country volume heterogeneity matched to GDELT's, (c) the chosen volume control recovered the cycling structure while neutralizing the volume confound. If any of (a)/(b)/(c) is missing or fails, do not commit; pick a different D2.

3. **Commit your work** with a structured message:
   ```
   git add pilots/1f_failsafe_cycling/ HANDOFF.md CHANGELOG.md
   git commit -m "Task #172 — cycling-pilot pre-registration LOCKED · H1b/H2b/H3b cold-derived from cont 30 §2 + cont 26 §3 + Reading 06 §10.3 narrowing · six locked decisions D1-D6 · synthetic-data validation of volume-control gate PASSED" -m "<details>"
   git push
   ```

4. **Update HANDOFF.md** with:
   - Replace the "## Your job this session (Claude Code)" section's task-#172 instructions with a brief "## Last Claude Code session (DATE)" block summarizing what shipped + the locked H1b/H2b/H3b text + which D-decisions were made + whether seed-comparison agreed or diverged
   - "## For Cowork next session" with: (a) review the locked pre-registration for any caught-by-Cowork issues, (b) decide whether to run the pilot immediately or schedule, (c) audit v07 target 2026-06-16 should verify the cold-derivation discipline held

5. **Update CHANGELOG.md** with an entry documenting: cycling-pilot pre-registration locked; H1b/H2b/H3b summary text; the six D-decisions; the synthetic validation outcome.

6. **Add a timeline entry** at `timeline/index.html` (~latest entry at top).

7. **Bump JSON endpoints** if a new candidate-doc was created or modified.

8. **Mark task #172 completed** in whatever tracking you use. Note it in HANDOFF.md's "Last Claude Code session" block.

9. **DO NOT run the pilot in this session.** That's Phase E, separate task, separate session. Resist the temptation even if you have time left. The discipline is locked-before-data.

---

## Cross-references

- **Pre-registration locked at:** `candidates/1f_l0_failsafe_signature.md` (especially §4 H1, §5 protocol, §7 confounds, §11 status)
- **Pilot code:** `pilots/1f_failsafe/pilot.py` (all DFA / Welch / IAAFT / permutation logic implemented; gdelt_mode() needs you to wire it)
- **Confound log:** `pilots/1f_failsafe/confounds.md` (amendments go here)
- **Framework discipline:** `continuations/27.md` (three-tier procedure + pruning rules)
- **Audit history:** `audits/v05.md`, `audits/v06.md`
- **Most recent reading:** `readings/2026-06-02_gamma_world_multi_agent_world_modeling.md` (declared hard-stop; §9 = discipline frame)
- **Previous reading:** `readings/2026-05-31_bes_bidirectional_evolutionary_search.md` (BES backward decomposition methodology is what scoped this pilot)
- **Live site:** https://a70m123r.github.io/agnostic-framework/
- **Source repo:** https://github.com/a70m123r/agnostic-framework

---

## For Cowork next session (after Claude Code completes #172)

1. **Review the locked pre-registration** at `pilots/1f_failsafe_cycling/PRE_REGISTRATION.md`. Look specifically for:
   - Are H1b/H2b/H3b properly falsifiable? Do they have explicit thresholds + effect sizes + p-values like #150's H1 did?
   - Does §11 (cold-derivation note) cite specific canon paragraphs grounding each hypothesis? Or does it gesture vaguely at cont 30 / cont 26 without specificity?
   - Does §12 (seed comparison) honestly document agreement/divergence with `PILOT_150b_cycling_seed.md`?
   - Does the synthetic validation in `synthetic_validation/` actually prove D2 works?
2. **If issues found**, do NOT secretly edit Claude Code's locked pre-registration. Instead: write a follow-up amendment in `pilots/1f_failsafe_cycling/confounds_cycling.md` §1, dated and explicitly stated as "amendment before any GDELT data examined." Then re-lock.
3. **Decide whether to run the pilot immediately or schedule.** If running immediately: hand back to Claude Code for Phase E with a HANDOFF.md update. If scheduling: log the run date and hold.
4. **Audit v07 target 2026-06-16** should verify (a) cold-derivation discipline held; (b) seed-comparison was honest; (c) synthetic validation of D2 actually passed; (d) the pre-registration is genuinely falsifiable per cont 27 §2.

## For Cowork next session (after Claude Code completes #169) — KEPT FOR HISTORICAL REFERENCE

If the result-commit lands cleanly, Cowork's next move per Pav's "lets do 150 and then 151" sequence is task #151: RC-Koopman cultural-eigenmode pilot. Architecturally scoped by [`readings/2026-06-02_gamma_world_multi_agent_world_modeling.md` §6](readings/2026-06-02_gamma_world_multi_agent_world_modeling.md) (γ-World hub-mediator + simplex agent encoding template); methodologically scoped by [`readings/2026-05-31_bes_bidirectional_evolutionary_search.md` §7.1](readings/2026-05-31_bes_bidirectional_evolutionary_search.md) (BES backward goal-tree decomposition).

Dataset for #151 needs Pav's call. Per his earlier "stay away from US politics" steer, candidates surfaced by previous scouts include:
- HistWords semantic drift (Hamilton-Leskovec-Jurafsky)
- Multi-country Wikipedia edit cadence (zh / ru / en / de)
- Reddit subreddit embeddings (Waller-Anderson 2021)
- Music taste / Spotify Daily Charts (cross-country lag analysis)

**Don't preempt this; surface for Pav's steer.**

If the result-commit FAILS (H1 refuted as stated), Cowork's move is:
1. Read your `results/discussion.md` carefully
2. Surface the falsifier outcome to Pav
3. Decide between (a) Reading 06 §10.3 amendment, (b) cont 27 §3 pruning of the Tier 2 conditional claim, (c) trying the alternative dataset (Wikipedia edit cadence per scout report §6)

If NULL (no significant direction either way), Cowork's move is:
1. Document the null cleanly in cont 30 or a Reading 06 amendment
2. Try the Wikipedia edit cadence pilot as second test
3. If null AGAIN, demote the claim from Tier 2 conditional to "structurally adjacent, no empirical purchase"

---

## Format for updates Claude Code makes to this file

When Claude Code ends its session, prepend a section like:

```markdown
## Last Claude Code session (YYYY-MM-DD)

**Task completed:** #169 result-commit
**Verdict:** [PASS / FAIL / NULL]
**Key numbers:** Δβ = X.XX, Cohen's d = Y.YY, p = Z.ZZZZ
**Commits:** [hash1] [hash2]
**Result files at:** `results/`
**Issues encountered:** [list any]
**For Cowork next:** [specific items, e.g., "Reading 06 §10.3 amendment needed per falsifier outcome"]

---
```

…above the existing "What you need to know" header so the next session sees it first.
