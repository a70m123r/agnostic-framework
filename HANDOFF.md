# HANDOFF — Cowork → Claude Code

**Last updated:** 2026-06-04 by Claude Code session (cycling pre-reg drafted + synthetic-gated; EWS scout; ground-truth validation seed)
**Next session:** Cowork — lock-review (see decisions below); the canon-level "narrow the claim" call from the EWS scout
**Pinned task:** Cowork lock-review of the cycling pre-registration **after** folding in (a) the synthetic-gate revision (H2b/H3b-slope → diagnostic) and (b) the EWS scout's "narrow to bridge+metric, drop symmetry-novelty" finding. Then the **ground-truth validation pilot** (`PILOT_groundtruth_EWS_validation_seed.md`) should arguably run **before** any GDELT re-pull. #172 (the cold-draft) is DONE.

---

## Last Claude Code session (2026-06-04)

Continued from the #169 result-commit. Did four things, all via dynamic-workflow orchestration (blind where it mattered):

1. **#172 cycling pre-registration drafted** — `pilots/1f_failsafe_cycling/PRE_REGISTRATION.md` (commit 6a8139e). Produced by a **results-blind** workflow (3 isolated cold-derivers → synthesis → seed-check §12); converged ~90% with the seed on operational decisions, demoted the seed's continuous-co-movement centrepiece (it re-admits the #150 artifact). Merges #150b + #151 (Koopman → diagnostic). **DRAFT, unlocked.**
2. **§6 synthetic gate run** (commit 8e23308; `synthetic_validation/`) — build → 3 adversarial skeptics → finalize. **Locked 3-hyp gate FAILS** (H2b shock-recovery ~0% power — a genuine design limit, 365-day window low-passes recovery; reproduced across metrics/windows). **REVISED design PASSES** (`revised_gate: PASS`): H1b cycling-collapse + lock-sign as primary, H2b→diagnostic → 95–100% power (squeeze pole fixed 0.01→0.95). **Volume confound genuinely controlled** — a skeptic caught the build run's must-NULL as *vacuous*, the finalizer rebuilt a real confound (raw +0.755 → +0.012 thinned, fires H1b raw/not-thinned), independently reproduced. Banner note on the pre-reg records the required H2b/H3b-slope→diagnostic revision.
3. **EWS scout** (commit bbb6d9c; `SCOUT_critical_transitions.md`) — web-grounded. **Honest novelty verdict: the symmetric two-pole 1/f claim is PRIOR ART** (Goldberger et al. 2002 PNAS, near-verbatim, same DFA-α axis); EWS is not purely one-pole. **Genuine open seam (Tier 2):** cross-field bridge (EWS ↔ physiology loss-of-complexity, mutually uncited) + the **rolling cycling-amplitude metric** (vs static level) + the **social/GDELT application** (open — Braha 2024 npj Complexity deferred EWS to future work; GDELT-EWS review field has none). Delivered ground-truth datasets, fixes for both gate gaps (H2b → Delecroix 2024 PNAS "resilience in bursts" / λ=−log(AR1)/dt; coupling → PCMCI+/transfer-entropy), and a falsifiable next pilot.
4. **Ground-truth validation seed** (this commit) — `PILOT_groundtruth_EWS_validation_seed.md`: validate the cycling-amplitude metric against the one-pole CSD baseline on **labelled** data (Cascade lakes w/ negative control; PhysioNet healthy/CHF/aging) **before** the GDELT social application. DRAFT for Cowork to lock.

**Decisions for Cowork (canon-level — not actioned here):**
- **Narrow the public claim** to bridge + rolling-amplitude metric + social application; **drop symmetry-novelty** (it's Goldberger 2002). Scout §1.
- **Fold the synthetic-gate revision** (H2b/H3b-slope → diagnostic; H1b cycling-collapse + lock-sign primary) into the cycling pre-reg before locking.
- **Run the ground-truth validation pilot before any GDELT re-pull** — if cycling-amplitude can't beat one-pole CSD on labelled data, the metric claim collapses to the bridge.
- Yilun-Du + new EWS-field outreach (Scheffer/Dakos/Goldberger/Boers/Braha) stay gated.

**Unpushed (held for Pav):** commits 8e23308 (synthetic gate), bbb6d9c (scout), + this seed. The result-commit + cont 30 + the pre-reg draft are already on origin.

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

**Current state (2026-06-03): the audit v06 §10 + Reading 08 §9 hard-stop is CLEARED — empirical ground was broken.** Pilot #150's result-commit landed 2026-06-03 (H1 NOT SUPPORTED — confounded null; see `pilots/1f_failsafe/results/discussion.md`), and Cowork's `continuations/30.md` integrated it + narrowed Reading 06 §10.3. The framework is now in **pre-registration mode for the cycling successor pilot (task #172)** — see "Your job this session" below. Standing discipline still holds: **DO NOT** write new readings/audits/continuations/outreach/candidates or extend canon as a side-effect of #172 — log insights in §11 of the pre-registration doc for Cowork.

**Third-strike condition (now relieved).** The rule: a third inbound external paper before empirical ground was broken would signal a discovery-cascade trap. Ground IS now broken (#150 result-commit, 2026-06-03), so the acute pressure is off — but the underlying discipline stands: don't let inbound papers displace the queued empirical work (#172 → its result-commit).

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

> **⚠ Who can run this — the make-or-break point.** The cold-derivation must be performed by an agent with **genuinely clean context** — one that has NOT already seen the seed, `results/discussion.md`, or #150's findings. The Claude Code session that produced #150's result-commit and wrote the seed is **maximally contaminated** and must NOT do the cold-derivation (it would just recite the seed from memory). Note that **this HANDOFF and `continuations/30.md` themselves summarise #150's findings** — so the cold-deriver must be handed a **curated brief (canon-file pointers + the task only)**, NOT told to read this HANDOFF. Cleanest implementation: a **dynamic-workflow subagent** (fresh isolated context by construction — it cannot see the orchestrator's conversation) or a brand-new session.

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

- **#150 result (the confounded null):** `pilots/1f_failsafe/results/discussion.md` (verdict + volume confound), `methods.md`, `gdelt_results.json`; new confounds in `pilots/1f_failsafe/confounds.md` §9–§14
- **#150b cycling seed** — hypothesis-generating sketch, carries fitting risk: `pilots/1f_failsafe/PILOT_150b_cycling_seed.md`. **Do NOT feed this to the #172 cold-deriver.**
- **Framework-side integration (canon input for #172):** `continuations/30.md` (§2 canon mapping, §3 narrowing, §5 merge logic)
- **Narrowed claim:** `readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md` §10.3 + 2026-06-03 amendment log
- **Framework discipline:** `continuations/27.md` §2–§3 (three-tier procedure + pruning/promotion)
- **#172 deliverable target (to be created):** `pilots/1f_failsafe_cycling/PRE_REGISTRATION.md`
- **#150 pre-registration (FORMAT template only — do NOT copy its hypotheses):** `candidates/1f_l0_failsafe_signature.md`
- **Audit history:** `audits/v05.md`, `audits/v06.md` (v07 target 2026-06-16)
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
