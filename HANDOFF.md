# HANDOFF — Cowork → Claude Code

**Last updated:** 2026-06-02 by Cowork session (Claude in Cowork mode)
**Next session:** Claude Code (CLI) on Pav's machine to run GDELT pilot
**Pinned task:** #169 — Run `pilots/1f_failsafe/pilot.py --mode gdelt` against real GDELT v2 data → result-commit

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

## Your job this session (Claude Code)

**One task: Run `pilots/1f_failsafe/pilot.py --mode gdelt` against real GDELT v2 data and land the result-commit.**

Per `candidates/1f_l0_failsafe_signature.md` §11 timeline + `pilots/1f_failsafe/README.md` §3, the result-commit target is 2026-06-09 (within 7-day window). Realistically this is ~3 working days of pipeline work. Could fit in one focused session if GDELT ingest goes smoothly.

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

## What NOT to do (hard discipline guardrails)

- **DO NOT write new readings.** Reading 08 was the framework's LAST infrastructure document before pilots resume.
- **DO NOT write new audits.** Audit v07 target is 2026-06-16, scoped by Cowork.
- **DO NOT write new continuations.** Cont 29 stands; cont 30 is for the NEXT round, not for documenting your pilot run (that's `results/discussion.md`).
- **DO NOT extend the framework canon, promote new primitives, or run scouts on new external papers.** Even if you discover something interesting in GDELT, log it in `results/discussion.md` for Cowork to evaluate next session — don't promote anything to canon-level yourself.
- **DO NOT send the Yilun-Du outreach DM** (task #168). Outreach is firmly gated on at least one pilot result-commit landing first. Even after this commit lands, hold outreach for Cowork to draft per Pav's voice.
- **DO NOT modify the locked pre-registration.** H1 is locked at 2026-06-02 in `candidates/1f_l0_failsafe_signature.md` §4. N=6 amendment is locked in `confounds.md` §1 (2026-06-02). New amendments go in `confounds.md` only, dated, with reason, and only for issues discovered after running real data — never modify the pre-registration retroactively to make a result land.
- **DO NOT skip the confound log.** §5.5 of the pre-registration requires explicit confound documentation in the result commit. Even null findings need this.
- **DO NOT silently change the statistical test stack.** The Welch PSD + log-log slope fit + paired permutation test stack is locked. If a problem arises (e.g., distribution non-normality), document it in `confounds.md` as a new entry and surface to Cowork for next-session decision rather than swapping methods mid-run.

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

## End-of-session checklist (before you close)

1. **Commit your work** with a structured message. Example pattern:
   ```
   git add results/ pilots/1f_failsafe/pilot.py CHANGELOG.md HANDOFF.md
   git commit -m "Pilot #150 result-commit — GDELT v2 H1 [PASS/FAIL/NULL] · Δβ = X.XX, Cohen's d = Y.YY, permutation p = Z.ZZZZ" -m "<details>"
   git push
   ```

2. **Update HANDOFF.md** with:
   - Section "## Last Claude Code session (DATE)" with what shipped + verdict
   - "## For Cowork next session" with anything Cowork should action

3. **Update CHANGELOG.md** with a result-commit entry (mirror the structure of the 2026-06-02 first-commit entry that's already there).

4. **Update `candidates/1f_l0_failsafe_signature.md` §11** with the result-commit date and Bar A status.

5. **Add a timeline entry** at `timeline/index.html` (~latest entry at top, mirror the format).

6. **Bump JSON endpoints** (`readings.json` if you ship anything reading-shaped, `candidates.json` if candidate promotion bar changed). Use the bash script in `scripts/` for IndexNow if Bing should re-crawl.

7. **Mark task #169 completed** in whatever tracking you use. Cowork's TodoList is not shared, so just note it in HANDOFF.md's "Last Claude Code session" block.

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

## For Cowork next session (after Claude Code completes #169)

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
