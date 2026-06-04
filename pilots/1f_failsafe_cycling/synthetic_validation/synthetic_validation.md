# Pilot #150b/#151 — §6 Synthetic-Validation Gate — FINAL

> **STATUS: FINAL (post-audit).** Numpy-only pipeline run end-to-end on synthetic systems with
> known ground truth, per `PRE_REGISTRATION.md` §6. **Every number below comes from an executed
> run** (`sv_power_results.json`, the machine-written record of the power study; runtime 1047 s).
> This is the post-adversarial-audit revision: three independent audits found the prior draft's
> numbers were *honest* (it reported FAIL, did not fake a pass) but its **must-NULL was vacuous**
> and several generators/estimators were **mis-calibrated**. Those bugs are fixed below and the
> pipeline was re-run. It does NOT touch real GDELT/V-Dem data (the gate must pass first).

## Headline

**SECTION-6 GATE = FAIL** for the **locked** design — and the failure is now isolated, honest,
and well-understood:

- **(b) Confound control PASSES, and now LOAD-BEARING.** The rebuilt gen (iv) volume confound
  fires the H1b *inferential gate* in **100% of RAW (unthinned) panels** (corr(τ, log-volume)
  ≈ **+0.75**, matching the #150 r = 0.92 regime); after the locked Poisson-thinning it fires in
  **5%** and corr → **≈ 0**. gen (v) co-trending NULLs the E1 spine (3.3%). The volume control is
  demonstrated to work *on a confound that genuinely can fire the test* — not, as in the prior
  draft, on a confound too weak to fire anything.
- **(a) Power FAILS — solely because H2b (shock-recovery) has ~0% power on the locked τ(t)**, a
  genuine 365-day-window design finding (reproduced, not a bug). With H2b in the locked
  classification, power is 0% on all three signal generators.
- **The revision the gate implies PASSES both halves.** If H2b is demoted to a diagnostic and the
  single primary is **H1b cycling-collapse (direction-agnostic) + the lock-sign direction**, the
  executed power is **i = 1.00, ii = 0.95, iii = 1.00** (all ≥ 80%) with the confounds still NULL.

---

## Bugs fixed (from the three adversarial audits)

All three audits agreed the prior run **did not fake** a PASS/null/power (it reported FAIL and the
H1b/DFA numbers were real and reproducible), but flagged the run as **untrustworthy as a
validation** because it nulled for the wrong reasons. The confirmed bugs and their fixes:

| # | Confirmed bug (audit) | Root cause | Fix | Evidence it's fixed |
|---|---|---|---|---|
| **1** | **gen (iv) must-NULL was VACUOUS** — the volume confound could not fire *any* working test even with thinning OFF, so "gen (iv) = NULL" was guaranteed by construction and proved nothing about the volume control. (All 3 audits.) | (a) H1b is an *amplitude* metric, invariant to a monotone volume *trend*; (b) the old gen (iv) used an even/odd up/down drift split + log-uniform volumes that left most systems in the DFA-α-saturated high-volume regime → panel-mean raw corr ≈ +0.04, not +0.5. | Rebuilt gen (iv) as a **single-signed coverage drift in the sub-saturation band**: every system is SPARSE (~45/day, high white-sampling-noise floor) in its high-steer (pseudo-healthy) epochs and DENSE (~3000/day) across its low-steer (pseudo-captured) epoch, with a **sharp** transition aligned to the steer. The sparse epoch's white floor *inflates* τ dispersion → A_cyc spuriously "collapses" into the dense epoch → a **predicted-sign H1b false positive** the thinning must kill. | **H1b gate fires RAW 100% (20/20) → THINNED 5%**; corr(τ, log-vol) RAW **+0.75 → THINNED ≈ 0** (executed). The must-NULL now tests something that *can* fail. |
| **2** | **Squeeze pole mis-calibrated** — squeeze captured τ sat *below* its own healthy baseline, so the lock sign read POSITIVE only ~1% of the time; gen (ii) could never be classified. (Audits 1, 3.) | The healthy oscillation (φ swings to 0.97) already has a high *median* τ (~0.83–0.96). A squeeze pin at the old `PHI_HI = 0.88` reads τ ≈ 0.70 — below that median → a negative departure (wrong sign). | Recalibrated **`PHI_HI` 0.88 → 0.96** (the constant-φ → τ map puts φ = 0.96 at τ ≈ 1.0 sparse … 1.3 dense, clearly above the healthy median), and made the captured-epoch shock kick **decay back to the pin** (was a *held* step that compounded across shocks and dragged the pole down). | **Squeeze lock-sign correct = 0.95**, pull = 1.00 (executed); squeeze captured τ ≈ 1.03 > healthy ≈ 0.93. |
| **3** | **H3b slope was a DEAD test** — first-differencing the **2-level rectangular** synthetic steer left only ~2 nonzero regressor points/system, so γ_std ≈ 0 on *every* generator and gen (iv)'s "NULL on H3b" passed **trivially** (a dead regressor), not by rejecting the confound. (All 3 audits.) | The synthetic steer was a degenerate 2-level step. Real V-Dem `v2x_freexp_altinf` is annual but **multi-level** (changes every year). | Replaced the steer with a **multi-level annual** trajectory (gradual ramp into a sustained trough + per-year wobble), matching real V-Dem (§3.2). Now ~10 nonzero `dS`/system → the H3b null is **well-posed** and the confounds NULL **for the right reason**. | gen (iv)/(v) H3b = 0.000 with a non-degenerate regressor (executed). **See the honest caveat below: even well-posed, the first-differenced *slope* stays underpowered on signal — a real design finding.** |
| **4** | **Epoch labelling manufactured spurious capture episodes** — a midpoint split of any steer wander labelled stable/unrelated systems as "captured," diluting the paired test and (once the multi-level steer was added) firing H1b on the *co-trend* generator ~88% of the time — a false positive on causally-unrelated data. | `epoch_labels_from_steer` cut at the steer-range midpoint, so any varying steer always produced a "captured" half. | Implemented the **locked §3.4 cut rule**: "captured" requires a **sustained substantial drop** (≥ 0.20 steer-points below the system's healthy level, ≥ 6 strides). Stable systems → all-healthy (excluded from the paired test). gen (v) rebuilt as a **gradual** co-trend with a **constant-amplitude** oscillation (level co-trends for E1; A_cyc epoch-invariant → H1b NULLs). | gen (v) any-primary FP **0.00** (was ~0.88); gen (i) paired test now runs only on its genuine capture systems (n ≈ 9). |

**Not changed (Cowork's call, per the task):** none of the locked §4 thresholds
(`d_z ≥ 0.5`, `≥ 25%` decline, `HR ≥ 1.5`, `γ_std ≤ −0.30`, `≥ 70%` population gate, Holm α = 0.05).
All fixes are to **generators** (synthetic ground truth) and **estimator-internal implementation**
(the §3.4 epoch cut-rule parameters, the §3.2 multi-level steer) — never the §4 inference bands.
The DFA estimator is **reused unchanged** (`fast_dfa` verified bit-identical to the prior pilot's
`pilot.dfa`, max |Δα| = **4.44e-16**, 43× faster).

---

## The five generators and their ground truth

| Generator | Planted truth | Must be detected as |
|---|---|---|
| (i) cycling + recovering | φ(t) oscillates (τ cycles, high A_cyc); shocks decay back; ~half carry a capture episode (mixed squeeze/pull poles) | H1b high A_cyc when healthy **AND** H2b fast recovery |
| (ii) locked-squeeze | capture pins φ **high** (DFA-α ≈ 1.0–1.3, over-correlated); cycling collapses | H1b/H2b CAPTURED; lock sign **positive** |
| (iii) locked-pull | capture pins φ **low** (DFA-α ≈ 0.5, white); cycling collapses | H1b/H2b CAPTURED; lock sign **negative** |
| (iv) **volume drift, constant texture** | φ pinned mid (constant true texture); strong single-signed **coverage drift** (sparse↔dense) aligned to the steer | **NULL** on H1b/H2b/H3b — the within-system analogue of the #150 r = 0.92 confound |
| (v) two co-trending unrelated series | τ-level and S-level each carry an **independent gradual trend**; constant oscillation amplitude | **NULL** on the E1 co-movement spine |

## The locked pipeline (as run)

Poisson-thin each system to a common within-system rate floor (1st-pct of daily totals) → daily
Shannon entropy of the EventRootCode histogram → rolling DFA-α **τ(t), window 365 d / stride 30 d**
(reusing the verified DFA) → estimators (A_cyc = P90−P10 of τ; recovery fraction R; L = |τ−τ_1f|)
→ three primary inferential tests with autocorrelation-respecting nulls → **Holm** (family-wise
α = 0.05) → ≥ 70% population gates + the volume-survival gate → combined verdict + the E1 spine.
**N = 18 systems** (≥ 16 per §3.4), ~half with a capture episode.

- **H1b** — one-sided **paired sign-flip permutation** on log-A_cyc (healthy − captured); exhaustive
  2ⁿ enumeration for n ≤ 14, else 20 000 Monte-Carlo sign-flips (the same exact null, sampled);
  gates d_z ≥ 0.5, ≥ 25% median decline, ≥ 70% population.
- **H2b** — per-system **recovery fraction R** (§4.2 complement metric), healthy vs captured, with a
  within-system shock-onset **label-permutation null** and a **placebo-shock arm**; gates HR ≥ 1.5,
  ≥ 70% population, placebo must NULL.
- **H3b** — within-system fixed-effects **first-differenced slope** of L on the steer S, pooled
  standardized γ_std, **phase-randomized null** on dL; gate γ_std ≤ −0.30, ≥ 70% population; plus
  the ≥ 90%-one-signed symmetry check. The **lock-sign direction** is read separately from the
  per-system median captured-epoch signed departure (this is what the §6 pole classification uses).
- **E1** (exploratory spine) — per-system corr(Δτ, ΔS) with a **surrogate-steer (phase-randomized)
  null** — the gen (v) must-NULL.

---

## Power table — generators (i)–(iii)

Run: **N_sim = 60 per generator, N = 18 systems, window 365 d / stride 30 d, n_perm = 120,
seed 2026, runtime 1047 s** (`sv_power_results.json`). "Locked power" = the §6 gate (a)
classification as locked (gen i: H1b ∧ H2b; gen ii/iii: H1b ∧ H2b ∧ correct lock sign).

| Generator | **Locked POWER** (H1b∧H2b[∧lock]) | H1b pass | H2b pass | H3b pass | lock-sign correct | ≥ 80%? |
|---|---|---|---|---|---|---|
| (i) cycling + recovering | **0.000** | **1.000** | 0.000 | 0.000 | — (mixed) | ✗ |
| (ii) locked-squeeze | **0.000** | **1.000** | 0.000 | 0.000 | **0.950** | ✗ |
| (iii) locked-pull | **0.000** | **1.000** | 0.000 | 0.000 | **1.000** | ✗ |

**H1b cycling-collapse detection is at 100% power on all three signal generators, and the lock
SIGN is now correct on both poles** (squeeze 0.95, pull 1.00 — the prior squeeze ~0.01 is fixed).
The locked classification is 0% **only because it requires H2b**, which has 0% power.

## Must-NULL results — generators (iv)–(v)

| Generator | FP: any primary | FP: E1 spine | H1b | H2b | H3b | ≤ ~5%? |
|---|---|---|---|---|---|---|
| (iv) volume drift, constant texture | **0.050** | 0.050 | 0.050 | 0.000 | 0.000 | ✓ (at the bar) |
| (v) two co-trending unrelated series | 0.000 | **0.033** | 0.000 | 0.000 | 0.000 | ✓ |

The gen (iv) any-primary 0.050 (3/60) is the **thinned** H1b at the high end of Monte-Carlo noise:
two **independent fresh-seed** confirmations gave gen (iv) any-primary = **0.000 / 0.000** (NS = 50
each), so the controlled FP is ~0–5%. gen (v) E1 across the three seeds = 0.033 / 0.060 / 0.020 —
hovering around the 5% line (n_sim = 60 MC noise), consistent with ≤ 5% in expectation. **Both
confounds pass gate (b).**

## The LOAD-BEARING volume-survival gate (the fix that matters most)

This is the central correction. The volume control is exercised by an **inferential** test that
**genuinely fires on the confound and is then killed by thinning** — not, as before, by a
descriptive correlation that never gated anything.

On the rebuilt gen (iv) confound (20 panels inside the power run, plus the per-panel survival check):

| | corr(τ, log-volume) | **H1b inferential gate fires** |
|---|---|---|
| **RAW** (unthinned τ) | **+0.75** (≈ the #150 r = 0.92 regime) | **1.00 (20/20 panels)** |
| **After Poisson-thin** to the common 1st-pct floor | **≈ 0.00** | **0.05 (1/20)** |

The confound that fires the H1b gate in *every* raw panel (corr +0.75) is suppressed to ~5% by
thinning (corr → 0). Separately verified: on the **signal** generators thinning does **not** destroy
the real effect (H1b stays at 100%). **The reframe's core promise — that the within-system design +
Poisson-thinning kills the #150 volume confound — is now demonstrated on a confound strong enough to
break the test.**

---

## §6 acceptance gate — verdict

The gate (PRE_REG §6) freezes the pipeline only if **BOTH** (a) power ≥ 80% on (i)–(iii) **AND**
(b) FP ≤ ~5% on (iv)–(v).

- **(b) Confound control — PASSES.** gen (iv) NULLs on H1b/H2b/H3b (any-primary ≤ 5%, ~0% on fresh
  seeds), gen (v) NULLs the E1 spine (3.3%), and the volume control is **load-bearing** (kills a
  confound that fires the H1b gate 100% raw). This is the make-or-break #150 check, and it holds.
- **(a) Power — FAILS, solely on H2b.** Decomposition:
  - **H1b (does texture cycle, and does cycling collapse under capture?) — 100% power, confound-
    robust.** A_cyc collapses sharply and population-wide under capture (d_z ≈ 1.6–3.2 in the power
    run, ≥ 94% population share, paired sign-flip p ≈ 5e-5). Strongly powered at both poles.
  - **Lock-SIGN direction — now reliable** (squeeze + at 0.95, pull − at 1.00). The symmetric-pole
    detection works after the `PHI_HI` recalibration.
  - **H2b (shock-recovery faster when healthy) — ~0% power.** Binding failure for the locked
    classification (which requires H2b), so locked power ≈ 0%.
  - **H3b slope-vs-steer magnitude — ~0% power (a genuine design finding, now correctly
    characterized).** With the multi-level steer the H3b regressor is well-posed (so the confounds
    NULL for the right reason), but the lock-up is a **level** effect (L stays large *throughout* the
    captured low-S plateau) and the **locked first-differencing** — which is exactly what neutralizes
    the spurious-trend confound (so gen v does NOT fire H3b) — also annihilates that level contrast.
    Diff kills the signal *and* the confound; an FE-without-diff estimator recovers the signal but
    then **lets the gen (v) co-trend through** (verified γ_std = −0.43, p = 0.005, a false positive).
    So no estimator *within the locked first-differenced spec* reaches power on signal while keeping
    the gen (v) must-NULL. The lock-sign direction (which gate (a) uses) is unaffected and works.

**OVERALL: SECTION-6 GATE = FAIL** (gate requires both; (a) fails on H2b).

### Why H2b has ~0% power (genuine, reproduced — not a bug)

All three audits independently confirmed H2b = 0 is real. On gen (i), where ground-truth recovery
truly differs by epoch, the 365-day rolling-DFA window **low-pass-filters sub-annual shock-recovery
transients** into near-invisibility; and the strong healthy *cycling* that H1b relies on makes
"return to a pre-shock baseline" ill-defined (τ is always wandering) while a captured/pinned epoch
is flat so small perturbations there look *recovered*. The two epochs are therefore not separable
on τ(t) (R_healthy ≈ R_captured). This echoes the pre-reg's own §3.3 caveat (the decade/window may
be too short to resolve the relevant timescales) and §4.2 ("a locked system has nothing to recover
from"). The placebo arm and the recovery-fraction-vs-T½ metric choice do not change it.

---

## Go / No-Go and the required revision

**NO-GO on the locked design as written.** PRE_REG §6 requires revising **N / window / stride /
estimator before any real data**. A **window/stride** change is insufficient (a prior sweep gave
H2b ≈ 0% at {180, 270, 365}; the smoothing/cycling-baseline problem is structural, not a window-
width problem). **N** is not the issue (effects are 100%/0%, not noisy). The binding levers are the
**estimator** and the **primary-family composition**:

**The revision the gate implies (executed, PASSES both halves):**

1. **Make the single primary test H1b — within-system cycling-collapse, direction-agnostic** — and
   read the **lock-sign direction** as the pole label. This is the load-bearing half of the §10.3
   claim ("Loss of CYCLING CAPACITY … IS the signature"). Executed power under this rule:
   **i = 1.00, ii = 0.95, iii = 1.00** (all ≥ 80%); confounds still NULL (gen iv any-primary ≤ 5%,
   gen v E1 3.3%). **Revised gate = PASS** (`revised_gate: "PASS"` in the JSON).
2. **Demote H2b (recovery) to a diagnostic** pending an estimator not subject to the 365-day-window
   smoothing or the healthy-cycling/captured-flatness asymmetry — e.g. recovery of a **short-window
   local** texture statistic (entropy variance over 60–90 d, or a local AR(1) coefficient) measured
   against the pre-shock level, rather than recovery read off the 365-d rolling DFA-α.
3. **Demote the H3b magnitude-SLOPE to a diagnostic** (keep the lock-sign direction, which works):
   the locked first-differencing cannot detect the level-effect lock-up without re-admitting the
   trend confound. A level-based FE estimator with a **trend-preserving surrogate-steer null** (so an
   independently-trending S reproduces its spurious slope under the null) is the candidate
   replacement — to be re-validated synthetically (it must reach ≥ 80% on i–iii while keeping gen v
   NULL, which the naive FE does not).

Each replacement must be re-validated synthetically — ≥ 80% on (i)–(iii) **and** NULL on (iv)–(v) —
**before re-entering the primary family**. **No real GDELT/V-Dem data should be examined until a
revised pipeline passes both halves of the §6 gate.** This is a *pipeline-freeze* verdict (it gates
whether the estimator is frozen for real data); it is **not** a statement about the cycling claim
itself, and per §8 a synthetic-stage estimator failure prunes nothing — it just blocks data entry.

---

## Implementation judgment calls (carried forward + new)

1. **Texture cycling = time-varying AR(1) φ(t)** (a concentration-*amplitude* mechanism does not
   make τ cycle; verified). Healthy = φ oscillates; captured = φ pinned; squeeze = pin high
   (`PHI_HI = 0.96`, recalibrated), pull = pin low (`PHI_LO = 0.12`).
2. **Histograms persisted, not scalar entropy** — so Poisson-thinning operates on counts, exactly as
   the real ingest must (§3.1, D6). This is what makes the volume control a genuine test.
3. **gen (iv) rebuilt to be load-bearing** (bug #1) — single-signed sparse↔dense coverage drift in
   the sub-saturation regime, with a sharp steer-aligned transition. RAW corr +0.75, H1b fires
   100% raw → 5% thinned. (The old gen (iv) was vacuous: +0.04 raw, fired nothing.)
4. **Common within-system rate floor = 1st percentile** of daily totals (5th left a residual).
5. **Vectorized DFA proven identical to `pilot.dfa`** (max |Δα| = 4.44e-16); reused, not
   reimplemented. H1b's sign-flip null uses exhaustive 2ⁿ for n ≤ 14, else 20 000 MC sign-flips
   (same exact null; avoids a 2¹⁸ blow-up at N = 18 with no change to the answer).
6. **H1b null = paired sign-flip permutation** (the pre-reg's §4.1 primary mechanism). Autocorrelation
   is respected because each A_cyc is computed on the genuinely autocorrelated τ(t).
7. **§3.4 epoch cut = sustained substantial drop** (≥ 0.20 steer-points, ≥ 6 strides) — the locked
   capture-episode rule, replacing a midpoint split that manufactured spurious capture epochs on
   stable/co-trending systems (bug #4).
8. **Multi-level annual steer** (bug #3) — matches real annual-but-multi-level V-Dem; the prior
   2-level rectangular step made H3b's first-difference regressor degenerate.

## Honest limitations (disclosed)

- **The H3b slope and H2b are both underpowered on the locked τ(t)** — genuine design findings the
  gate surfaced, not estimator bugs. The gate **cannot certify or refute** the H3b magnitude-slope
  or H2b as locked; it can certify H1b cycling-collapse and the lock-sign direction.
- **E1 is not a clean general co-movement statistic** (its two-sided surrogate null can catch
  wrong-sign co-movement; gen (iv) E1 ran 4–10% across seeds). E1 is exploratory and enters the gate
  only as the gen (v) must-NULL (E1 = 0.033 in the main run); it cannot upgrade a null (§4.6).
- **gen (v) E1 sits near the 5% line** (2–6% across three seeds at n_sim = 60). It passes in
  expectation but a larger N_sim would tighten the CI; the point estimate is fine.
- **n_sim = 60** (n_perm = 120). Effects are extreme (100% / 0% / ~0–5%), so 60 sims give decisive
  CIs; the must-NULL point estimates carry ±~3% MC uncertainty, bounded by the fresh-seed re-runs.

## Files & reproduction

All under `pilots/1f_failsafe_cycling/synthetic_validation/` (numpy-only):

- `generators.py` — the five generators (i)–(v); `python generators.py` prints a panel summary.
- `fast_dfa.py` — vectorized DFA; `python fast_dfa.py` asserts equality with `pilot.dfa` + speedup.
- `sv_pipeline.py` — the full locked pipeline + power driver.
  - `python sv_pipeline.py --selftest` — one panel per generator through the whole pipeline (prints
    the load-bearing vol-gate per generator).
  - `python sv_pipeline.py --power --nsim 60 --nperm 120 --seed 2026` — the §6 power study (writes
    `sv_power_results.json`; runtime 1047 s). Reports the locked power, the H1b-only revision power,
    the lock-sign rates, and the load-bearing vol-gate fire rate.
- `sv_power_results.json` — machine-written results of the power study (the authoritative record).
- Scratch supports: `_calib.py` (estimator calibration), `_volgate.py` (the load-bearing vol gate
  over panels), `_minicheck.py` (per-generator smoke test), `_winsweep.py` (window sweep).

The DFA is **reused** from `pilots/1f_failsafe/pilot.py` (vectorized as `fast_dfa`, verified
identical), per the instruction to reuse the tested primitive and cut bug surface.
