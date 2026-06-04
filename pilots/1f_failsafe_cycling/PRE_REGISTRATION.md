# Pilot #150b/#151 — Cycling-Capacity Failsafe Signature — PRE-REGISTRATION

> **STATUS: DRAFT — produced by a results-blind synthesis workflow. PENDING COWORK REVIEW + LOCK.**
>
> This document is a consolidated pre-registration synthesized from **three independent
> cold derivations**, each drafted from the framework canon in isolation (none read the prior
> pilot's seed, results, or confounds). The synthesis step likewise adjudicated against canon
> only (continuations 30, 26, 27, 13, 20, 25; cymatics Reading 06 §10.3 as narrowed 2026-06-03).
> It is **NOT yet locked**. No GDELT or V-Dem data has been examined. No thresholds may be
> changed after data is touched except per the disclosed amendment discipline (cont 30 §7.4).
> Cowork must review §4 (hypotheses + thresholds), §5 (protocol), and §8 (promotion bars)
> and explicitly LOCK before any synthetic-validation or real-data step proceeds.
>
> Cold-derivation provenance and a frank converged-vs-diverged accounting are in **§11**.

---

## §1 The claim

**Tier-1 parent (unchanged, cont 26 §3 + §2).** Every wrapper carries unbounded
infinite-expansion inertia (cont 26 §2). L0 is not a neutral substrate but an *evolved
failsafe environment* that bounds expansion through internal pressures (coherence) and
external pressures (neighbouring wrappers, substrate limits) (cont 26 §3). The load-bearing
move: **the visible stability of a mature wrapper is an ACTIVE phenomenon — continuous
failsafe activation, not a settled state** (cont 26 §2, third corollary). The lifecycle
phases re-read as failsafe-states: wake = inertia detected, negotiation = failsafe engaged,
dormancy = failsafe succeeded, supersede = failsafe accommodated, break = failsafe enforced
(cont 26 §3).

**What the failsafe IS, in A⁻/A⁺ terms (cont 13 + cont 30 §2.1).** Cont 13 §1.1/§1.4 makes
A⁺ (admit/generate variety) and A⁻ (prune/verify/enforce concordance) coupled latent
dimensions whose health is *working slack in both* — the Wolfram Class-4 viability band
(Γ ≈ 1); Class 1/2 = freeze (A⁻ dominant), Class 3 = explode (A⁺ unbounded). A⁺ × A⁻ is
"dialectical tension — productive when generative, paralytic when locked" (cont 13 §1.1 table).
Cont 30 §2.1 maps this to the social substrate: **squeeze = system-wide A⁻ tightening**,
**pull = system-wide A⁺ generation**; **healthy cycling = both phases active, alternating —
the substrate retains the *capacity to oscillate*.**

**The narrowed Reading 06 §10.3 claim being tested (locked 2026-06-03, cont 30 §3).**
Verbatim:

> "Loss of CYCLING CAPACITY (the ability to alternate between dense-feedback A⁻ tightening and
> broadband A⁺ generation, recovering toward 1/f after each shock) IS the signature of
> substrate-level failsafe failure. Substrate-level failsafe HEALTH is the *capacity* to cycle
> — not a fixed spectral value. Captured / locked systems show collapse of τ(t) cycling, in
> either direction (locked-squeeze → β ≫ 1, over-correlated; locked-pull → β ≈ 0,
> white-noise-random). The static-binary 'authoritarian = brittle, pluralistic = healthy'
> operationalization is rejected as value-coded and not framework-grounded; the symmetric
> capacity-to-cycle measure is the framework's actual claim."

**The two symmetric failure poles (cont 30 §2.2).** Locked-squeeze = cont 20 dormancy at
substrate scale (A⁻ total, expression collapses, substrate preserved → over-correlated texture,
β ≫ 1). Locked-pull = cont 25 §1 break-apart (A⁺ runs without dense feedback, no stable W_C
forms, fragmentation → white-noise texture, β ≈ 0). Both are losses of the *capacity to cycle*.

**Operational core.** This converts a static, value-coded claim (explicitly rejected) into a
**within-system, over-time** measurable: a rolling texture trajectory **τ(t)** along the
squeeze↔pull axis, whose **cycling** (presence, amplitude, recovery, symmetric lock-up) is the
failsafe-health signature, and whose movement is steered by an **independently-measured external
openness signal S(t)** (cont 30 §1.2 move 3).

---

## §2 Why this is operationalizable now

1. **The prior static design was structurally mismatched to the claim and confounded.** The
   #150 cross-system static design tested "authoritarian = lower β" and returned a confounded
   null: Welch-β correlated with per-country event volume at r = 0.916 (cont 30 §1.1). A claim
   about a *dynamic capacity* cannot be tested by a static between-system level contrast. The
   within-system, over-time reframe (cont 30 §2.3) matches the claim's actual shape **and**
   dissolves the dominant confound: each system is its own baseline, and event volume is far
   more stable within a country across a decade than across countries.

2. **Cont 30 §2.3 already names the three measurable handles** directly: (i) within-system τ(t)
   variance over the decade — *does it cycle? does the variance collapse during sustained
   capture?*; (ii) within-system τ(t) trajectory vs an independently-measured openness
   trajectory — *do they co-move, in either direction?*; (iii) recovery toward 1/f after each
   shock (from the narrowed §10.3 text + cont 26 §2 active-stability). These map one-to-one onto
   H1b / H3b-steer-coupling / H2b below.

3. **An external, value-neutral steer exists and is lockable before τ(t) is computed**
   (cont 30 §1.2 move 3, §5.2 item 2): V-Dem `v2x_freexp_altinf`. This replaces the value-coded
   label with a continuous information-openness index, making the directional claim falsifiable
   rather than tautological.

4. **The volume confound is now understood and controllable** (cont 30 §1.1, §7.1 lesson 1):
   DFA-α is volume-robust (cross-country range 0.074 vs Welch-β's 0.735); the white-noise
   spectral floor can be held constant by Poisson-thinning to a common within-system rate. The
   pre-registration commits to the controls *before* re-running.

5. **The methodology aids are in place.** Reading 07 §7.1 backward goal-tree decomposition
   (decompose the top goal into checkable sub-goals, each with a pre-registered verifier, ≥1
   anchored to external data — the steer is exactly that anchor). Reading 08 §6 multi-system
   panel template (each system = its own control, analyzed jointly but per-system). Cont 27 §2–§3
   three-tier falsifiability + narrow-before-demote. Cont 30 §7.2 mandates synthetic pre-validation.

---

## §3 Dataset + signals + within-system time-window structure

### §3.1 Texture signal (per system, daily)

- **Source:** GDELT v2 Events, country-day aggregation, window 2015-02-18 → 2026-01-01 (GDELT
  v2 availability floor to the prior window's ceiling), keyed on `SQLDATE` and
  `ActionGeo_CountryCode` (FIPS), exactly as in `pilots/1f_failsafe/gdelt_ingest.py`.
- **PRIMARY texture channel:** daily **Shannon entropy (bits) of `EventRootCode`** ("event-category
  entropy") — the same primary signal as #150, now read as a *trajectory* rather than a single
  spectral summary. Secondary channels (mean tone, event count) retained as diagnostics /
  covariates only.
- **CRITICAL ingest change vs #150 (see D6, §4.6):** the per-(system, day) **event count** and the
  full **`EventRootCode` histogram** must be retained at ingest, because Poisson-thinning to a
  common within-system rate (the volume control, D3) operates on counts/histograms, not on the
  already-collapsed entropy value. The existing `data/raw/*_category_entropy.csv` store only the
  scalar entropy and are therefore **insufficient** for the locked volume control. The signal
  must be re-derived (re-pull, or re-finalize from a checkpoint that retains `root_hist`) with
  counts + histograms persisted.

### §3.2 External steer signal S(t) (per system, annual → interpolated)

- **PRIMARY (the inferential steer):** V-Dem **`v2x_freexp_altinf`** (Freedom of Expression and
  Alternative Sources of Information), annual, decade-spanning. Locked before any τ(t) is
  computed (cont 30 §5.2 item 2).
- **Aggregation rule (locked):** annual S is assigned to all days in that calendar year as a
  step function (no smoothing interpolation by default, to avoid manufacturing within-year
  trend); a monotone-cubic interpolated variant is pre-registered as a *robustness* check only.
  S(t) is resampled to the τ(t) stride (see §3.3) by taking the step value at each window centre.
- **ROBUSTNESS replication (diagnostic, not a second inferential test):** V-Dem `v2mecenefm`
  (government media-censorship effort). RSF press-freedom is a **tertiary diagnostic only**
  (rejected as primary or robustness: short history + documented methodology breaks, cymatics
  Reading 06 §9 gotcha 5).

### §3.3 Texture trajectory τ(t) (rolling, volume-robust)

- **τ(t) = rolling DFA-α** of the (Poisson-thinned) daily event-category-entropy series.
- **Window = 365 days; stride = 30 days** (resolves the squeeze↔pull band over the ~11-year
  record while keeping ≥ ~120 τ samples per system). A window-length sensitivity sweep
  {180, 270, 365, 540} days is pre-registered as **secondary/diagnostic** (cymatics Reading 06
  §6 notes social relaxation timescales — demographic ~25 yr, fiscal ~50–80 yr — exceed the GDELT
  span; the decade may be too short to resolve the slowest failsafe cycles, an acknowledged limit,
  §7).

### §3.4 Within-system time-window structure (panel)

- **Unit of analysis:** system × rolling-window panel (Reading 08 §6 template). Each system is
  analyzed **as its own control**; systems are pooled only via per-system summaries / random
  effects, never via a raw between-system level contrast.
- **System set (locked before data, results-blind selection rule):** **N ≥ 16** systems chosen by:
  (a) GDELT daily-coverage floor ≥ 99% of country-days over the window (matching the #150 ingest
  standard); (b) full V-Dem coverage 2015–2026; (c) **stratified to span the steer trajectory
  range** — approximately half with large monotone steer movement (a sustained opening OR a
  sustained capture episode), approximately half steer-stable — because H2b/H3b-coupling are
  untestable in systems whose steer never moves (cont 30 §2.3 "in either direction"). The #150
  twelve-country set (CHN, USA, RUS, GBR, PRK, DEU, IRN, FRA, TUR, NLD, VEN, CHL) is a candidate
  seed for the list but is **extended to ≥16 and re-selected by the rule above**, blind to τ(t).
- **Epoch labelling for the paired tests (H1b, H2b):** within each system, **healthy/open
  epochs** and **captured epochs** are defined from S(t) by a pre-registered, results-blind cut
  on `v2x_freexp_altinf` (within-system terciles of the system's own S trajectory, OR a fixed
  sustained-drop rule defining a "capture episode" as ≥ X index-point drop sustained ≥ Y months —
  exact X, Y and the tercile-vs-threshold choice to be **frozen at lock time, after V-Dem is
  pulled but before τ(t) is computed**). Epoch labels are held by a separate key; the analyst
  computing τ(t) is **blind to labels** until all estimators are frozen (D8).
- **N is provisional on power:** if the §6 synthetic power study does not reach ≥ 80% power at the
  pre-registered effect sizes with autocorrelation-respecting nulls, **N, window, or stride is
  revised before any real data is examined** (cont 30 §7.2).

---

## §4 Hypotheses

The narrowed §10.3 claim decomposes (Reading 07 §7.1 backward goal-tree) into **three
falsifiable sub-goals**, each its own hypothesis:

- **H1b — does it CYCLE, and does the cycling collapse under capture?** (cont 30 §2.3 handle i)
- **H2b — does it RECOVER toward broadband-1/f after a shock, faster when healthy?** (handle iii;
  cont 26 §2 active-stability; cont 20 reversibility)
- **H3b — is the lock-up SYMMETRIC in direction, and does its magnitude track the steer?**
  (cont 30 §2.2; the rejection of the value-coded binary)

**Steer-coupling (S(t) → τ(t)) is the measurement spine shared by all three**, not a fourth
hypothesis. It is the cont 30 §1.2 move-3 requirement and enters H1b (epoch labelling), H2b
(epoch labelling), and H3b (the directional co-movement test) directly. A standalone continuous
co-movement statistic is reported as **exploratory** (§4.5).

> **A genuine divergence is recorded here, not papered over.** The three derivers did not agree
> on which facet occupies which "slot." Deriver 1 and Deriver 3 made H2b = shock-recovery and
> H3b = symmetric lock-up (the assignment adopted below). Deriver 2 made H2b = steer-co-movement
> and H3b = shock-recovery, treating co-movement as a primary inferential test in its own right.
> **Synthesis ruling:** the narrowed §10.3 text names exactly three *facets of the capacity*
> (cycle / recover / symmetric-direction); "co-movement with an independent steer" is the
> *mechanism cont 30 §1.2 prescribes for measuring* those facets, not a fourth facet. Promoting
> co-movement to its own inferential slot risks the autocorrelation-artifact failure mode
> (two trending series co-move spuriously) becoming a "pass." So co-movement is the spine and the
> three slots are the three facets. Cowork may overrule this and split co-movement back out as a
> fourth primary hypothesis (Holm family of four) — flagged explicitly as the single largest
> open decomposition choice. See §11.

Standard rigor for all three (cont 27 §2; cont 30 §5.2 item 4, §7.3): exactly **one
pre-registered primary inferential test per hypothesis**; pre-registered effect-size band;
one-sided where directional; an autocorrelation-respecting permutation/block-bootstrap null;
**Holm correction across the three-hypothesis family at family-wise α = 0.05**; an explicit
**clean-PASS / clean-NULL / confounded** band; a **≥ 70% population-wideness gate** (mirroring the
#150 lesson that a 1/6-pairs pattern is not population-wide); and a mandatory **synthetic power +
validity check before any real data** (§6).

### §4.1 H1b — within-system cycling, and its collapse under capture

**Statement.** Within a single system, the volume-robust texture trajectory τ(t) **cycles** while
the system is healthy, and cycling **collapses** when the system undergoes sustained capture — in
**either** direction (locked-squeeze: τ pinned high, DFA-α ≫ 1; locked-pull: τ pinned low,
DFA-α ≈ 0.5). Capture is detected as **loss of oscillation amplitude**, not as a low mean level
(symmetric per cont 30 §1.2 move 2 / §2.2). Tested as a **paired within-system contrast**: each
system contributes its own healthy-epoch cycling amplitude and its own captured-epoch cycling
amplitude.

> **Most-falsifiable formulation chosen (divergence resolved).** D3's paired
> baseline-vs-capture-epoch contrast within the *same* system is adopted as primary over D2's
> open-vs-capture *cross-group* contrast (which partially reintroduces a between-system
> comparison and its volume risk) and over D1's continuous panel slope (which the annual→stride
> steer-resolution mismatch attenuates). The paired form makes each system literally its own
> control — the strongest guard against the #150 volume confound — and yields the cleanest
> falsifier.

**Metric.** Cycling amplitude **A_cyc(system, epoch)** = robust dispersion of τ(t) within the
epoch, operationalized as the inter-decile range (P90 − P10) of τ(t); reported alongside MAD and
SD of τ(t) as convergent diagnostics. Epochs are equal-length (≥ 24 monthly τ samples each) drawn
from the same system per §3.4.

**Primary inferential test.** One-sided **paired permutation test** (sign-flip of the within-pair
log-A_cyc differences, healthy − captured) across the set of capture-episode systems, with the
null preserving within-series autocorrelation (phase-randomization of the underlying τ(t) within
epoch). **Holm-corrected** within the three-hypothesis family.

**Effect size.** Standardized paired effect **Cohen's d_z ≥ 0.5** on log-A_cyc (healthy >
captured); and a within-system **relative decline ≥ 25%** (A_cyc,captured ≤ 0.75 × A_cyc,healthy)
in the median affected system; 95% CI reported.

**Significance.** One-sided **α = 0.05**, Holm-corrected across the family; permutation p from the
autocorrelation-respecting null above.

**Population-wideness gate.** **≥ 70%** of capture-episode systems must individually show
A_cyc,captured < A_cyc,healthy (predicted sign) for a clean PASS.

**Volume gate (D3).** The decline must **survive** the volume control: (a) computed on
Poisson-thinned τ(t); and (b) robust to including within-system log event-volume per epoch as a
covariate / matching the two epochs on volume. If the decline is fully explained by within-system
volume drift, the result is logged **confounded**, not PASS.

**Falsifier.** H1b is falsified if A_cyc does **not** decline under capture (paired permutation
p ≥ 0.05) **OR** median decline < 25% **OR** the population gate fails (capture systems cycle as
much as healthy) **OR** the decline vanishes under the volume control. Clean NULL band:
|median log-A_cyc difference| < 0.10 with d_z < 0.2. Confounded band: decline present but explained
by the within-system volume-drift covariate.

### §4.2 H2b — shock-recovery toward broadband-1/f, faster when healthy

**Statement.** A healthy failsafe system, after an **exogenous shock** displaces its texture,
**returns τ(t) toward its pre-shock broadband-1/f baseline** within a characteristic relaxation
time (cont 30 §3 "recovering toward 1/f after each shock"; cont 26 §2 active-stability is the
*restorative* failsafe doing work; cont 20 reversibility/wakeability). A captured/locked system
either fails to return (locked-squeeze) or has no broadband structure to return to (locked-pull).
**Within the same system**, post-shock recovery is **faster** during healthy/open epochs than
captured epochs.

**Baseline.** Per-system **τ_1f** = trailing-12-month median τ(t) immediately before each shock,
plus a per-system broadband-epoch median τ as a cross-check; both frozen before shock labelling.

**Shocks (pre-registered, exogenous, blind to τ).** A fixed external shock list, locked before
analysis, from an archive independent of GDELT (e.g., coup / state-of-emergency / major
conflict-onset / mass-protest onset dates from a recognized event catalog). Shock onset is blind
to τ(t); shocks lacking sufficient pre/post coverage are excluded by **pre-registered rule**.
Minimum **≥ 5 qualifying shocks per system**; systems below threshold excluded a priori. A
**placebo-shock control** (random non-shock months) is pre-registered: if "recovery" appears at
placebo shocks, the recovery metric is a mean-reversion artifact and H2b is reported a
methodological null.

**Metric.** **Return half-life T_½** = time for |τ(t) − τ_1f| to fall to 50% of its post-shock
peak deviation (censored if no return within 24 months); per-system recovery fraction **R** =
share of shocks that return within H = 12 months (within 0.5 pre-shock SD, sustained ≥ 3 months)
as a robust complement.

**Primary inferential test.** Within-system **mixed-effects** comparison of recovery between
healthy and captured epochs of the same system (system as random effect; shock nested in system):
a likelihood-ratio test on the epoch-state term for log-T_½ (one-sided: captured slower), with a
permutation null over shock-onset assignment that preserves the event-rate envelope.
**Holm-corrected** within the family. (This is a difference-in-differences in the **time domain**
— cont 30 §2.3 "handled in the time domain" — and is itself a guard against the static spectral
floor, which is a level effect, not a recovery-rate effect.)

**Effect size.** Standardized epoch-state effect equivalent to **Cohen's d ≥ 0.5** on log-T_½;
**OR** a return-to-baseline **hazard ratio HR ≥ 1.5** (healthy epochs recover faster), 95% CI
excluding 1; **AND** median **T_½(captured) / T_½(healthy) ≥ 1.5**.

**Significance.** One-sided **α = 0.05**, Holm-corrected; permutation null over shock onset.

**Population-wideness gate.** **≥ 70%** of systems show T_½(captured) > T_½(healthy).

**Falsifier.** H2b is falsified if recovery does **not** differ between healthy and captured
epochs (|d| < 0.2 and HR CI spans 1) **OR** captured epochs recover **faster** (HR < 1, CI
excludes 1) **OR** the effect disappears under the within-system volume covariate **OR** T_½ cannot
be estimated for a pre-registered majority of shocks (declared underpowered/inconclusive, not
support) **OR** the placebo-shock control reproduces the recovery pattern. Clean NULL band:
|d| < 0.10 with T_½ ratio in [0.8, 1.25].

### §4.3 H3b — symmetric lock-up; magnitude tracks the steer

**Statement.** Failsafe failure is **symmetric in direction** (cont 30 §2.2): capture can lock
texture toward over-correlation (locked-squeeze, τ high) **or** toward fragmentation (locked-pull,
τ low). The framework's claim is therefore tested as a **two-sided lock-up**: within system, the
**direction-agnostic** departure of τ(t) from its broadband baseline,
**L(t) = |τ(t) − τ_1f|**, *increases* as the openness steer S(t) *decreases* — and the **sign** of
the departure is permitted to differ across systems/epochs. A directional, single-signed result
that resurrects "less open ⇒ uniformly lower τ" (the rejected value-coded binary) does **not**
confirm H3b; symmetric magnitude-increase does.

**Primary inferential test.** Within-system **fixed-effects panel regression** of lock-up
magnitude L on the openness steer S (system fixed effects difference out all between-system
levels including mean volume; first-differenced / pre-whitened to neutralize shared trend), with
an autocorrelation-respecting block / phase-randomization permutation null on the slope.
**Holm-corrected** within the family. **PLUS a pre-registered symmetry check** (below), which is
*not* a separate inferential test but a gate on the *interpretation* of the H3b result.

**Effect size.** Standardized within-system slope **γ_std ≤ −0.30** (lower openness → larger
lock-up magnitude), 95% CI reported.

**Significance.** One-sided **α = 0.05** on γ_std, Holm-corrected; autocorrelation-respecting null.

**Population-wideness gate.** **≥ 70%** of systems show the predicted-sign (negative) within-system
association.

**Symmetry sub-claim + its own falsifier (the falsifier-of-the-reframe).** Across all capture
epochs pooled, the signed departure (τ − τ_1f) must include **both** directions, with neither
exceeding a pre-registered **90%** one-signed share. **If capture epochs are overwhelmingly
one-signed (≥ 90% in a single direction across systems), the symmetry sub-claim is FALSIFIED** —
which means the dynamics are *not* symmetric and the value-coded directional reading was closer to
correct after all. Per cont 27 §3, that outcome forces a **re-narrowing** of Reading 06 §10.3, not
a copy-back of the prior result and not a demotion of cont 26 §3.

**Falsifier.** H3b (magnitude) is falsified if L does **not** increase as openness drops
(|γ_std| < 0.10, CI spans 0) **OR** the sign reverses **OR** the coupling vanishes under volume
partialling. **Separately**, the symmetry sub-claim is falsified by the ≥ 90% one-signed condition
above.

### §4.4 Combined verdict (pre-registered inference rule)

- **≥ 2 of 3** primary hypotheses PASS (Holm-corrected, gates met, volume-survived) **AND** the
  H3b symmetry sub-claim is **not** falsified → the narrowed §10.3 cycling-capacity claim is
  **supported**; the candidate `1f_l0_failsafe_signature` cycling-capacity Tier-2 variant
  **advances** (see §8 bars).
- **Exactly 1 of 3** PASS → **mixed / hold**; no advance, no demotion.
- **0 of 3** PASS (clean nulls) → the within-system operationalization **also nulls**; per cont 27
  §3 narrow-before-demote, the pre-registered next step is the **Wikipedia edit-cadence
  second-substrate test** (cont 30 §3 Bar B), **NOT** demotion of cont 26 §3 and **NOT**
  re-derivation from the prior result.
- **H3b symmetry sub-claim falsified** (capture overwhelmingly one-signed) → re-narrow Reading 06
  §10.3 per cont 27 §3 regardless of the H1b/H2b outcome; report that the value-coded directional
  reading was closer to correct than the symmetric reframe.

### §4.5 Secondary / exploratory (NOT error-rate-protected, cannot upgrade a null)

- **E1 — continuous steer co-movement.** Per-system partial cross-correlation ρ between
  pre-whitened Δτ(t) and ΔS(t) at steer-leading lags 0–12 months, controlling for per-window log
  event volume; predicted sign negative (openness ↓ → DFA-α ↑). Reported with a phase-randomized
  **surrogate-steer null** (must give chance-level co-movement) and a **reverse-lag placebo**
  (τ-leads-S must be weaker). This is D2's H2b demoted to exploratory per the §4 divergence ruling.
- **E2 — RC-Koopman / DMD cyclical-mode layer (D5).** Whether a discrete squeeze↔pull eigenmode
  exists in τ(t) and its decay rate; reported as convergent-or-divergent with H1b. **Diagnostic
  only**, never the locked inference (cont 30 §5.1/§5.2 item 5: natural cyclical-mode tool but adds
  methodological surface area). NB open question: "cycling" as a discrete spectral mode vs simply
  maintained broadband variance are not identical and the §10.3 text is ambiguous between them
  (§7).
- **E3 — Welch-β texture.** Reported for continuity with #150; **diagnostic only** (the #150
  volume-confounded estimator).
- **E4 — robustness replications.** `v2mecenefm` steer; interpolated-S variant; window sweep
  {180, 270, 365, 540}; IAAFT-style surrogates. All exploratory.

### §4.6 Inference-vs-diagnostic designation (cont 30 §7.3)

The **only** inferential tests are the three Holm-corrected within-system permutation tests in
§4.1–§4.3. Welch-β, RC-Koopman amplitudes/eigenmodes, the continuous co-movement ρ, the `v2mecenefm`
/ RSF replications, and all surrogates are **diagnostic only** and **cannot upgrade a null to a
pass** (mirrors #150's correct demotion of IAAFT to diagnostic).

---

## §5 Protocol (step by step)

1. **Lock this pre-registration (Cowork).** Freeze §3 system-selection rule, §3.4 epoch
   cut-rule parameters, §4 hypotheses + thresholds, §4.4 combined-verdict rule, §6 synthetic
   acceptance criteria, §8 bars. Record the lock commit hash. **No real data examined yet.**

2. **Re-derive GDELT signals with volume controls at ingest (D6).** Re-run the country-day
   aggregation (or re-finalize from a checkpoint retaining `root_hist`) over 2015-02-18 →
   2026-01-01, **persisting per-(system, day) event count + `EventRootCode` histogram** in addition
   to the entropy scalar, and a per-system-day coverage flag. (The existing scalar-only CSVs are
   insufficient for thinning — §3.1.)

3. **Volume / confound control (D3, the locked triple-lock).**
   (a) **DFA-α is the primary, volume-robust estimator** (not Welch-β).
   (b) The **within-system design** differences out all between-system volume.
   (c) On **every 365-day window**, **Poisson-thin** the daily event stream down to the system's
   pre-registered common within-system rate floor *before* computing entropy and τ; **and** carry
   per-window log event volume as a covariate in H1b/H2b/H3b. Results must **survive thinning**.

4. **Texture-trajectory estimation.** Compute τ(t) = rolling DFA-α (window 365 d, stride 30 d) on
   the thinned entropy series, per system. (Window sweep is secondary, step 10.) RC-Koopman/DMD
   cyclical-mode layer computed in parallel as **diagnostic** (E2).

5. **External-signal alignment.** Pull V-Dem `v2x_freexp_altinf` (and `v2mecenefm` for robustness)
   for the locked system set; resample S(t) to the τ(t) stride by the locked step-function rule
   (§3.2). **Assign epoch labels (healthy/open vs captured) from S(t) by the locked cut-rule**,
   and **seal them in a separate key** — the τ-computing analyst is blind to labels (D8). Pull /
   freeze the exogenous shock list (H2b), blind to τ.

6. **Statistical tests (run once, in the locked order).** H1b paired permutation; H2b
   mixed-effects survival/half-life with shock-onset permutation; H3b fixed-effects panel slope
   with autocorrelation null + the symmetry-share check. Apply **Holm** across the three.
   Evaluate **population-wideness gates** and **volume gates**. Record clean-PASS / clean-NULL /
   confounded per hypothesis.

7. **Unblind labels; compute the combined verdict** per §4.4. If 0/3, trigger the Wikipedia Bar B
   second-substrate protocol (do **not** demote cont 26 §3). If the H3b symmetry sub-claim is
   falsified, trigger the §10.3 re-narrowing.

8. **Diagnostics + robustness (E1–E4)** reported as exploratory, explicitly flagged
   non-error-rate-protected, unable to change the verdict.

9. **Result-commit** with discussion + methods + tier-tagging, mapping observed outcomes to the
   pre-registered bands (the #150 discipline). Disclose any supportive-component substitution
   (cont 30 §7.4) without touching the locked tests.

10. **(Secondary, pre-declared)** window-length sweep; interpolated-S variant; `v2mecenefm`
    replication — reported as robustness, never as the inference.

---

## §6 First-commit deliverable (skeleton + synthetic validation that the confound-control works)

Per cont 30 §7.2 ("every locked pre-registration should be tested against synthetic data with
known properties before any real data examined") and the #150 lesson that the N=3 permutation
ceiling was caught at the synthetic stage. **No real GDELT/V-Dem data may be examined until the
synthetic gate passes.**

**Deliverable = a numpy-only pipeline skeleton + a synthetic-validation report** that runs the
**entire locked pipeline** (Poisson-thin → rolling DFA-α → A_cyc / T_½ / L estimators →
permutation/mixed-effects nulls → Holm → gates → combined verdict) against synthetic systems with
**known ground truth**:

| Synthetic generator | Must be detected as | Guards |
|---|---|---|
| (i) cycling + recovering system | healthy by H1b (high A_cyc), fast recovery by H2b | true-positive sensitivity |
| (ii) locked-squeeze (DFA-α high, variance collapsed, no recovery) | captured by H1b/H2b; lock sign **positive** | symmetric-pole detection |
| (iii) locked-pull (DFA-α ≈ 0.5, variance collapsed, no recovery) | captured by H1b/H2b; lock sign **negative** | symmetric-pole detection (other pole) |
| (iv) **strong event-volume DRIFT, constant true texture** | **NULL** on H1b/H2b/H3b | **the critical confound check** — the within-system longitudinal analogue of the #150 volume confound |
| (v) two co-trending but causally unrelated series | **NULL** on the E1 co-movement spine | spurious-co-movement / autocorrelation-artifact check |

**Acceptance criteria (locked):** the pipeline is frozen only if it (a) recovers the planted
effects in (i)–(iii) at **≥ 80% power** at the pre-registered effect sizes and N, with the
autocorrelation-respecting nulls; **and** (b) returns the pre-registered **null** on (iv) and (v)
(the confound generators must NOT fire). If power < 80% or a confound generator fires, **N / window
/ stride / estimator is revised in the pre-registration before any real data is touched**, and the
revision is disclosed.

The first commit ships: `pipeline/` skeleton (ingest hook, thinning, rolling DFA-α, the three
estimators + nulls, Holm, verdict), `synthetic/` generators (i)–(v), and a
`synthetic_validation.md` reporting power + the confound-null results. This is the analogue of the
#150 first-commit-before-data discipline.

---

## §7 Confounds explicitly named

1. **Spectral-floor / event-volume confound (the #150 killer — now controlled).** Sparse daily
   entropy → white sampling noise → flat high-frequency floor → biased β; cross-country Welch-β ↔
   log-volume r = 0.916 (cont 30 §1.1). **Controlled** by: DFA-α primary (volume-robust, range
   0.074 vs 0.735), within-system design, Poisson-thinning to common within-system rate, per-window
   volume covariate, and **synthetic generator (iv)** as the explicit must-null check (§6).

2. **Residual within-system volume DRIFT.** The within-system design kills the *between*-system
   confound, but a country whose GDELT coverage/volume grows or shrinks monotonically over the
   decade could induce a spurious τ trend correlated with the steer. Guards: per-window thinning to
   a common rate + per-window volume covariate + first-differencing/pre-whitening in H3b +
   synthetic generator (iv). **Sufficiency is an empirical question to be confirmed at the synthetic
   stage** (open).

3. **Regime / non-stationarity drift.** Rolling DFA-α assumes piecewise-stationary 365-day
   windows; a regime shift inside a window is unmodelled. Hedge: RC-Koopman secondary layer (E2),
   window sweep (E4). The inferential test's robustness to within-window regime shifts is
   **unverified until the §6 synthetic check** (open).

4. **External-index resolution mismatch.** `v2x_freexp_altinf` is annual; τ(t) is at 30-day
   stride. The locked step-function rule (§3.2) avoids manufacturing within-year trend but may
   **attenuate** within-system effect sizes; an interpolated-S variant is a pre-registered
   robustness check (E4).

5. **Shock exogeneity / shock-openness confound (H2b).** Openness itself may change *at* a shock,
   so "open vs captured epoch" and "shock" can be confounded. The pre-registered shock list must be
   exogenous to the steer; whether a clean such list exists per system is **open**. The placebo-
   shock control (§4.2) guards against the recovery metric being a pure mean-reversion artifact.

6. **Global common-mode events.** Shocks that hit many systems simultaneously (e.g., a global
   pandemic, a global financial event) induce cross-system correlated τ excursions that are not
   per-system failsafe dynamics. Guards: H2b uses **within-system** epoch contrasts (a common-mode
   shock affects healthy and captured epochs of the same system similarly, partially differencing
   out); a pre-registered **common-mode diagnostic** removes a cross-system τ(t) common factor
   (first principal component across systems) and re-runs as robustness; global-shock dates are
   flagged in the shock list.

7. **Symmetry-operationalization researcher choice (H3b).** Defining τ_1f and the ±90% one-signed
   threshold is a researcher choice that could bias the symmetric-vs-directional verdict. Guard: a
   pre-registered baseline-free robustness variant of the symmetry check; the threshold is frozen at
   lock (open until then).

8. **Decade may be too short for the slowest failsafe cycles.** Social relaxation timescales
   (~25 yr demographic, ~50–80 yr fiscal; cymatics Reading 06 §6) exceed the ~11-year GDELT span;
   the pilot can only resolve sub-decadal cycling. This **bounds the claim** the pilot can support
   and is stated as a limitation, not a confound to be removed.

9. **Provenance / fitting risk.** The reframe seed was written after seeing the #150 null and
   carries fitting risk (cont 30 §7.6); this pre-registration was therefore **cold-derived from
   canon** (§11, D1). The single-substrate result (GDELT only) cannot by itself promote a
   substrate-level claim; the Wikipedia second substrate is the pre-named next bar (§8).

---

## §8 Promotion bars for the cycling-capacity Tier-2 candidate

The pilot tests the **Tier-2 narrowed Reading 06 §10.3 conditional**; **cont 26 §3 (Tier-1) is not
on trial** (§9). Bars at promotion-bar rigor (cont 27 §3):

- **Bar A — within-system cycling-capacity signal, single substrate (GDELT).** Met when the §4.4
  combined verdict is **≥ 2 of 3** primary hypotheses PASS (Holm-corrected, gates + volume-gate
  met) **AND** the H3b symmetry sub-claim is not falsified. Effect → the candidate
  `1f_l0_failsafe_signature` advances from "held" to a **supported Tier-2 cycling-capacity
  variant**, *single-substrate*.

- **Bar B — second substrate (Wikipedia edit-cadence).** Met when an independent within-system
  cycling-capacity test on a **second substrate** (Wikipedia edit-cadence / revert dynamics per
  system over time, cont 30 §3 Bar B) reproduces a consistent cycling/recovery/symmetric-lock
  signature. **Required before any cross-substrate generalization** of the Tier-2 claim — a single
  GDELT pass cannot generalize a substrate-level claim (§7 #9; cont 27 §3). Whether convergent
  evidence across ≥ 2 substrates is *required before any promotion at all* vs whether Bar A alone
  permits a single-substrate advance is a **decision to lock with Cowork before results are read**
  (flagged open by two derivers).

- **Bar C — cross-substrate convergence / external replication.** Met when the cycling-capacity
  signature is reproduced on a third substrate **or** independently replicated by an external group
  (e.g., the Sornette/ETH or Turchin/Cliodynamics lineages, cymatics Reading 06 §10.5). Effect →
  candidate eligible for Tier-1 consideration per cont 27 §2 promotion procedure.

**Pruning direction (cont 27 §3).** A clean **0/3** null prunes the *GDELT operationalization*, not
the claim; it triggers Bar B. The Tier-1 cont 26 §3 parent is **never** demoted by a within-system
null on a single social substrate.

---

## §9 What this does NOT change

- **Cont 26 §3 (L0 evolved failsafes) Tier-1 epistemological canon: UNCHANGED** (cont 30 §6.1).
  The substrate-level claim was always about failsafe *dynamics*, not political labels; this
  pre-registration aligns the test with cont 26 §3 more tightly than the static binary did. A null
  narrows the *operationalization*, never the Tier-1 parent.
- **Cont 13 A⁺/A⁻ coupled-discipline canon + the Wolfram Class-4 viability band: unchanged.** Used
  as the grounding for the squeeze↔pull axis, not modified.
- **Cont 20 dormancy + cont 25 supersede/break: unchanged.** Used as the canonical readings of the
  two symmetric lock poles (locked-squeeze = dormancy; locked-pull = break-apart), not modified.
- **The three-tier discipline (cont 27): reinforced**, not changed — this is the narrow-before-
  demote procedure executing.
- **The cross-substrate convergence list, the cymatics-as-convergence-#8 narrowing, and the
  Reading 06 §11.2 fringe rejections (Strauss-Howe, Elliott waves, Gann, 528 Hz, Chizhevsky,
  sacred geometry): unchanged.**
- **The framework's stance on consciousness (cont 17 bracket): unchanged.** Cycling-capacity-as-
  failsafe-health is a substrate-dynamics claim with no consciousness commitment.
- **The value-coded "authoritarian = brittle / pluralistic = healthy" mapping: remains rejected**
  (cont 30 §1.2/§2.3/§3). H3b's symmetry sub-claim is precisely the test that keeps this rejection
  honest — and would itself force a re-narrowing if symmetry fails.

---

## §10 Cross-references + provenance

- Narrowed claim: `readings/2026-05-28_cymatic_harmonic_structure_in_social_systems.md` §10.3 +
  amendment log 2026-06-03.
- Tier-1 parent: `continuations/26.md` §2 (active stability), §3 (L0 evolved failsafes,
  lifecycle-as-failsafe-states).
- Squeeze↔pull = A⁻/A⁺: `continuations/13.md` §1.1/§1.4 (coupled latent dimensions, viability
  band, dialectical-vs-locked) + `continuations/30.md` §2.1.
- Symmetric poles: `continuations/30.md` §2.2; `continuations/20.md` §1/§3 (dormancy = locked-
  squeeze, reversible); `continuations/25.md` §1 (break-apart = locked-pull).
- Reframe + operational handles + the six decisions to lock: `continuations/30.md` §1.1–§1.3,
  §2.3, §3, §5.1–§5.2, §7.1–§7.6.
- Falsifiability + narrow-before-demote: `continuations/27.md` §2–§3.
- Methodology aids: Reading 07 §7.1 (backward goal-tree); Reading 08 §6 (multi-system panel
  template).
- Data pipeline reference (not a forbidden file): `pilots/1f_failsafe/gdelt_ingest.py` (signal
  definitions, FIPS map, window).
- **Blindness boundary observed:** this synthesis did **not** read
  `pilots/1f_failsafe/PILOT_150b_cycling_seed.md`, `pilots/1f_failsafe/results/*`,
  `pilots/1f_failsafe/confounds.md`, `candidates/1f_l0_failsafe_signature.md` §8/§11, or
  `HANDOFF.md`. The §10.3 narrowed text was read directly from the cymatics reading's amendment
  log (canon), not from the results docs.

---

## §11 COLD-DERIVATION NOTE

**Self-attestation.** This pre-registration was derived from the framework **canon only**. The
three upstream derivers each cold-drafted hypotheses + operational decisions from
`continuations/30.md`, `26.md`, `27.md`, `13.md`, `20.md`, `25.md`, and the cymatics reading
§10.3, **in isolation from one another** and **blind** to `PILOT_150b_cycling_seed.md`, the prior
results (`pilots/1f_failsafe/results/*`), the prior `confounds.md`, the candidate doc §8/§11, and
`HANDOFF.md`. The synthesis step (this document) re-read the same canon to adjudicate and **also
did not** open any forbidden file. This satisfies cont 30 §7.6: a reframe written after seeing a
null is **not** a clean pre-registration, so the pre-registration was independently re-derived
from the framework's claims rather than from the post-null seed.

**Canon citations grounding each hypothesis.**

- **H1b (within-system cycling presence + collapse, symmetric):** cont 26 §2 (visible stability =
  active failsafe activation), §3 (L0 evolved failsafes); narrowed Reading 06 §10.3 (capacity to
  cycle, collapse "in either direction"); cont 30 §2.3 handle (i) (within-system τ(t) variance,
  collapse under sustained capture), §1.2 move 2 (symmetrize), §2.2 (locked-squeeze β≫1 =
  cont 20 dormancy; locked-pull β≈0 = cont 25 §1 break); cont 13 §1.1/§1.4 (A⁺/A⁻ viability band);
  Reading 08 §6 (per-system-as-control panel).
- **H2b (shock-recovery toward broadband 1/f, faster when healthy):** narrowed Reading 06 §10.3
  ("recovering toward 1/f after each shock"); cont 26 §2 (active stability = restorative failsafe);
  cont 20 §1/§3 (dormancy reversibility / wakeability); cont 30 §2.2 (locked states = no recovery),
  §2.3 ("handled in the time domain"); cont 13 §2 (Class-4 = recoverable complex dynamics; Class
  1/3 = non-recovering freeze/explode); Reading 07 §7.1 (decompose into checkable sub-goals).
- **H3b (symmetric lock-up; magnitude tracks steer; value-coded binary rejected):** cont 30 §2.2
  (two symmetric poles), §1.2/§2.3/§3 (explicit rejection of the value-coded binary; symmetric
  capacity-to-cycle is the framework's actual claim); cont 20 (dormancy pole), cont 25 §1
  (break-apart pole); cont 27 §3 (if symmetry fails, re-narrow not copy-back).
- **Cross-cutting method:** cont 27 §2–§3 (three-tier falsifiability, precise thresholds, promotion
  bars, narrow-before-demote); cont 30 §1.1 + §7.1 (r=0.916 volume confound; mandate to control the
  white-noise floor via Poisson-thin / volume-match / DFA-α primary), §7.2 (synthetic validation
  before real data), §7.3 (surrogate/secondary = diagnostic, locked permutation = inference),
  §5.1/§5.2 item 5 (RC-Koopman natural but adds surface area → secondary), §5.2 items 1–6 (the six
  decisions locked in §4.6/§5/D-table); Reading 07 §7.1 + Reading 08 §6 (backward decomposition +
  multi-system template).

**How much the three derivers converged vs diverged (frank accounting).**

*Near-total convergence (all three independently landed the same):*
- The **claim reconstruction**: failsafe health = capacity to cycle; capture = loss of cycling,
  symmetric in direction; within-system over-time is the right design *and* the volume-confound fix.
- **Steer = V-Dem `v2x_freexp_altinf`**, locked before τ(t). Unanimous.
- **Volume triple-lock**: DFA-α primary + within-system design + Poisson-thin/volume-covariate.
  Unanimous.
- **τ method**: rolling DFA-α primary/inferential, **RC-Koopman secondary/diagnostic only**.
  Unanimous.
- **Mandatory synthetic pre-validation with a must-null volume-drift generator**, before any real
  data. Unanimous.
- **Inference vs diagnostic** designation; **Holm/Bonferroni family correction** across the three;
  **≥70% population-wideness gate**; explicit clean-PASS/clean-NULL/confounded bands;
  autocorrelation-respecting nulls. Unanimous in substance (minor numeric differences below).
- **0/3 → Wikipedia second substrate, not demotion of cont 26 §3.** Unanimous.
- The **H3b "falsifier-of-the-reframe"** (if capture is overwhelmingly one-signed, the symmetric
  reframe itself fails and the value-coded binary was closer to right → re-narrow). All three.

*Genuine divergences (recorded, not papered over):*
1. **Biggest: which facet occupies the H2b vs H3b slot.** D1 and D3 set H2b = shock-recovery,
   H3b = symmetric lock-up. D2 set H2b = steer-co-movement, H3b = shock-recovery — treating
   continuous co-movement as a primary inferential test. **Synthesis ruling (§4):** the §10.3 text
   names three *facets* (cycle / recover / symmetric-direction); co-movement with the steer is the
   cont 30 §1.2 *mechanism* for measuring them, not a fourth facet, and promoting it to its own
   inferential slot invites the autocorrelation-artifact failure mode to read as a pass. So
   co-movement is the shared spine and is demoted to **exploratory E1**. **This is the single
   largest call Cowork should sanity-check**; Cowork may split co-movement back out as a fourth
   primary hypothesis.
2. **H1b comparison structure.** D3 = paired within-system epoch contrast (same system, healthy vs
   captured epoch); D2 = open-vs-capture cross-group contrast; D1 = continuous within-system panel
   slope. **Synthesis chose D3's paired form** as the most falsifiable and most volume-robust (each
   system literally its own control; cross-group reintroduces between-system volume risk; the
   continuous slope is attenuated by the annual→stride steer mismatch).
3. **Re-pull vs reuse GDELT.** D1, D3 = re-pull with volume controls at ingest. D2 = reuse and
   thin at signal-construction (arguing the confound lives in the estimator's rate-response, not
   the query). **Synthesis ruling:** D2's diagnosis is correct, but the existing CSVs store only
   the scalar entropy, and Poisson-thinning needs the per-day counts + root-code histograms — so
   the signal must be **re-derived retaining counts/histograms** (re-pull or re-finalize from a
   histogram-retaining checkpoint). Net effect = D1/D3's action, motivated by D2's reasoning.
4. **N.** D1 = N ≥ 12; D2, D3 = N ≥ 16. **Synthesis chose N ≥ 16** (supports both the paired and
   stratified designs), with final N **contingent on the synthetic power study** — revise N before
   data if underpowered.
5. **Robustness steer.** D1 = RSF; D2 = `v2mecenefm` (RSF rejected for methodology breaks); D3 =
   both. **Synthesis chose `v2mecenefm`** as the pre-registered robustness replication (same V-Dem
   coverage/cadence; avoids RSF's documented breaks per cymatics §9 gotcha 5); RSF tertiary
   diagnostic only.
6. **Family α numerics.** D1, D3 = Holm at family α (0.05 or 0.01); D2 = Bonferroni 0.0167.
   **Synthesis chose Holm at family-wise α = 0.05** (uniformly more powerful than Bonferroni at the
   same family level; Cowork may tighten to 0.01 for drug-trial rigor — a one-line change that does
   not touch the test structure).

*Net assessment.* The three independent cold derivations **agree on the load-bearing science**
(claim, design, steer, volume control, estimator, synthetic gate, inference/diagnostic split,
narrow-before-demote) and **diverge only on decomposition packaging and a few tunable numerics**.
The agreement is strong evidence the operationalization follows from canon rather than from the
post-null seed; the one substantive divergence worth Cowork's explicit attention is **#1 (whether
steer co-movement is a primary hypothesis or the shared measurement spine)**.

---

## §12 Seed comparison (post-hoc)

> **Provenance note.** This section was written **after** §1–§11 were locked, and only then was
> `pilots/1f_failsafe/PILOT_150b_cycling_seed.md` opened for the first time. The seed is a
> hypothesis-**generating** sketch authored 2026-06-03 *with knowledge of #150's confounded null*
> (it explicitly carries fitting risk, seed §0/preamble). The purpose here is to check the
> blind cold-derivation against it: where they agree is independent corroboration; where they
> diverge, the question is which framing the **canon** actually grounds. §1–§11 are unchanged.

### §12.1 Headline mapping (the slots do not line up one-to-one)

The single most important finding is that **the seed's H-numbering and the locked H-numbering are
not the same partition of the claim.** A naive label-match (seed-H1b ↔ locked-H1b, etc.) is
misleading. The actual content maps as follows:

| Seed facet | Locked home | Relationship |
|---|---|---|
| seed-H1b "texture is dynamic / breathing exists" (τ varies above a noise null) | **folded into locked-H1b** (the "does it cycle" half) | seed's standalone variance-vs-null test becomes the healthy-epoch leg of the locked **paired** contrast |
| seed-H3b "capture = collapse of cycling" (rolling variance of τ shrinks during capture) | **the other half of locked-H1b** | seed-H1b + seed-H3b are **fused** into one paired within-system test in the locked doc |
| seed-H2b "texture co-moves with an independent openness signal," directional | **demoted to locked E1 (exploratory)**; its directional content re-expressed as the locked **H3b magnitude-vs-steer** test | the seed's **centerpiece** is the locked doc's **explicitly-demoted spine** |
| (seed prose only: "recover toward broadband 1/f after a shock," §0 + §1, never an H) | **promoted to locked-H2b** (shock-recovery half-life, faster when healthy) | the locked doc **operationalizes as a primary inferential test** something the seed names in prose but never made falsifiable |
| seed §1 "symmetric — squeeze and pull, in whichever direction it moves" | **promoted to locked-H3b symmetry sub-claim + its falsifier-of-the-reframe** | seed asserts symmetry as a framing; locked doc makes it a **gated, separately-falsifiable** sub-claim |

So: the cold derivation did not reproduce the seed's three slots. It **re-cut the same raw
material into a more falsifiable partition** — fusing two seed hypotheses, demoting the seed's
primary, and promoting two things the seed left as prose into primary/gated tests.

### §12.2 Per-hypothesis / per-decision comparison

**H1b (locked: within-system cycling + collapse under capture; structural overlap ≈ 80%).**
- **MATCH (structure):** the *substance* of locked-H1b is exactly seed-H1b ∪ seed-H3b — "does
  it breathe, and does the breathing collapse under capture." Both are **within-system**, both use
  **τ-cycling amplitude / rolling variance** as the metric, both define capture **only** from the
  external index, both demand collapse rather than a low mean. This is genuine independent
  corroboration: the canon (cont 26 §2 active-stability + §10.3 "collapse in either direction" +
  cont 30 §2.3 handle i) grounds the same construct Pav's steer reached.
- **MATCH (threshold):** both pre-register an autocorrelation-respecting / block-bootstrap /
  phase-randomized null. Corroborated.
- **DIVERGE (structure, in the canon's favour):** the seed keeps "breathing exists" (H1b) and
  "breathing collapses" (H3b) as **two separate hypotheses**; the cold derivation **fuses them into
  one paired epoch contrast** (healthy epoch vs captured epoch, *same system*). The canon grounds
  the fused form better: cont 30 §2.3 handle (i) names a *single* measurable — "does the variance
  collapse during sustained capture" — i.e. cycling and its collapse are one question, not two. The
  seed's split risks a vacuous "yes it varies" pass (seed-H1b) that says nothing about failsafe
  health. **Canon supports the locked fusion; the seed's two-slot split was looser.**
- **DIVERGE (threshold, canon adds rigor the seed lacked):** the seed states no effect-size band,
  no population-wideness gate, and no explicit volume-survival gate on H3b-collapse. The locked doc
  adds d_z ≥ 0.5, ≥ 25% relative decline, the ≥ 70% population gate, and the Poisson-thin + volume-
  covariate survival gate. None of these were *caught* by the seed; the cold derivation supplied
  them from cont 27 §2 + cont 30 §7.1/§7.3. **Cold derivation is stricter; nothing lost.**

**H2b (locked: shock-recovery toward 1/f, faster when healthy; structural overlap ≈ 35%).**
- **The largest content gap, and it runs in the canon's favour.** The seed mentions "recover
  toward broadband 1/f after a shock" twice (§0 reframe, §1 τ-definition prose) but **never makes it
  a hypothesis** — it has no shock list, no half-life metric, no placebo control, no recovery test.
  The cold derivation **promoted recovery to a full primary inferential test** with a pre-registered
  exogenous shock list, return-half-life T½, hazard-ratio effect size, a within-system mixed-effects
  difference-in-differences in the **time domain**, and — critically — a **placebo-shock control**
  to catch mean-reversion artifacts.
- **Where they AGREE:** only the bare idea ("recovery toward 1/f matters") — hence the low ~35%
  overlap, almost all of which is the shared word "recover."
- **Where they DIVERGE:** the cold derivation **caught something the seed under-developed.** The
  canon clearly grounds a recovery test (§10.3 "recovering toward 1/f after each shock"; cont 26 §2
  active-stability is *restorative* work; cont 20 reversibility; cont 13 Class-4 = recoverable). The
  seed glossed this into a phrase and spent its hypothesis budget on co-movement instead. **The cold
  derivation is the richer, more canon-faithful reading here — the seed was the weaker document on
  this facet.** This is the clearest case of "cold derivation caught something the seed missed."

**H3b (locked: symmetric lock-up, magnitude tracks the steer; structural overlap ≈ 55%).**
- **MATCH (the core insight — strong corroboration):** both documents reject the value-coded
  authoritarian/pluralistic binary and both insist the dynamics are **symmetric** — squeeze and pull
  are two poles of one failure-to-cycle, "in whichever direction it moves" (seed §1) ≈ "collapse of
  τ(t) cycling in either direction" (§10.3). That Pav's steer and the canon-only derivation
  independently land symmetric-rejection-of-the-binary is **the single most valuable corroboration
  in this comparison**: it shows the symmetry reframe is not merely Pav's preference fitted to the
  null — it is what cont 30 §2.2 + §10.3 actually say.
- **DIVERGE (which series carries the directional test — the consequential one):** the seed makes
  the steer-directional claim its **H2b**, a *standalone primary test of continuous co-movement*
  ("τ moves away from 1/f when openness↓, returns when openness↑"). The cold derivation **refuses to
  let raw co-movement be a primary test** — it demotes continuous co-movement to **exploratory E1**
  (§4.5) and instead tests the steer-link as locked-H3b's **lock-up-magnitude-vs-steer panel
  regression** (first-differenced / fixed-effects, on |τ − τ_1f|, not on signed τ).
  - **Which framing does the canon ground?** The canon grounds the **locked** framing. Cont 30
    §1.2 names the steer as the **mechanism for measuring** the capacity, and the §4 synthesis ruling
    (and §11 divergence #1) records *why* a bare co-movement test is dangerous: two trending series
    co-move spuriously, so promoting co-movement to a primary slot **invites the very
    autocorrelation/volume artifact that killed #150 to re-enter as a "pass."** The seed — written
    in the shadow of that null — nonetheless put the un-pre-whitened co-movement test at its centre.
  - **Verdict on this divergence:** **the seed was fitting something the canon does not cleanly
    support as a *primary* test.** Not wrong in spirit (the steer must enter the design — and it
    does, as H3b's regressor and as E1), but wrong in *inferential weight*. The cold derivation's
    demotion is the more defensible, more #150-scarred reading. (Caveat already on the record: §11
    flags that Cowork *may* re-promote co-movement to a fourth primary hypothesis — so the seed's
    instinct is preserved as an explicit, reviewable option, not erased.)
- **DIVERGE (the seed lacks the falsifier-of-the-reframe):** the seed asserts symmetry but provides
  **no test that could falsify symmetry itself.** The cold derivation adds the ≥ 90%-one-signed
  symmetry sub-claim falsifier (§4.3) — "if capture is overwhelmingly one-signed, the symmetric
  reframe FAILS and the value-coded binary was closer to right, → re-narrow." This is a guard
  **against the seed's own framing**, grounded in cont 27 §3. **Cold derivation caught a
  self-falsification the seed missed** — and it is precisely the guard that keeps the corroboration
  in the bullet above honest rather than circular.

**Operational decisions (structural overlap ≈ 90% — near-total agreement, this is the strongest corroboration zone):**

| Decision | Seed | Locked | Match? |
|---|---|---|---|
| Within-system, each system its own control | yes (§0, §1) | yes (§3.4) | **MATCH** |
| Texture over time, not a static β | yes (§0) | yes (§3.3) | **MATCH** |
| Primary estimator = rolling DFA-α (volume-robust) | yes (§3.1) | yes (§3.3) | **MATCH** |
| Volume confound is the #1 design requirement | yes (§3, "non-negotiable") | yes (§7.1, triple-lock) | **MATCH (corroborated)** |
| Poisson-thin to common rate + regress volume out | yes (§3.2/§3.3) | yes (§3.3 + §4 covariate) | **MATCH** |
| Steer = V-Dem, locked before τ(t) | yes (candidate, §2) | yes, **`v2x_freexp_altinf` primary** (§3.2) | **MATCH on family; locked is more specific** |
| `v2mecenefm` as a steer option | yes (§1, listed) | yes, **as robustness** (§3.2) | **MATCH** |
| RSF press-freedom | offered as co-equal candidate (§1) | **rejected to tertiary** (methodology breaks, §3.2) | **DIVERGE — canon (cymatics §9 gotcha 5) downgrades RSF; seed over-trusted it** |
| Window/step | 730 d / 30 d (~120 windows) | **365 d / 30 d** + sweep {180,270,365,540} (§3.3) | **DIVERGE on window length (a tunable, not structural)** |
| Annual-index ↔ sub-annual-τ resolution mismatch named | yes (§4.6) | yes (§3.2 step-function + §7.4) | **MATCH** |
| Reuse `data/raw/` vs re-pull | **reuse, "no new ingest"** (§2, §6.4) | **must re-derive** retaining counts+histograms (§3.1, D6) | **DIVERGE — the seed is materially WRONG here** |
| GDELT pipeline drift / schema-version confound | yes (§4.2) | (subsumed under non-stationarity §7.3; not called out by version) | seed slightly more specific on this one item |
| Global common-mode (COVID/wars) confound | yes (§4.3) | yes (§7.6) | **MATCH** |
| Synthetic pre-validation before real data | **absent** | yes, hard gate with must-null generators (§6) | **DIVERGE — cold derivation caught a gate the seed lacked** |
| 0/3 → narrow-not-demote → Wikipedia 2nd substrate | "narrow don't demote" spirit (§5) | full Bar A/B/C ladder (§8) | **MATCH in spirit; locked is operationalized** |
| Merge with #151 (RC-Koopman) | open question (§5) | resolved: **Koopman = diagnostic E2 only** (§4.5) | seed left open; cold derivation resolved it from cont 30 §5.1 |

Two operational divergences are not mere tuning and deserve emphasis:
- **The `data/raw/` reuse error.** The seed twice asserts a first pass "can reuse `data/raw/`, no
  new ingest." The cold derivation establishes (D6, §3.1) that this is **impossible for the locked
  volume control**: the existing CSVs store only the *scalar* entropy, but Poisson-thinning operates
  on per-day counts + `EventRootCode` histograms, which were discarded. **The seed's stated
  shortcut would have silently defeated its own #1 non-negotiable requirement.** The cold derivation
  caught this; the seed did not.
- **The missing synthetic gate.** The seed has no synthetic-validation step at all. The cold
  derivation makes it a hard pre-data gate (§6) with an explicit must-NULL volume-drift generator
  (the within-system analogue of the #150 confound) and a must-NULL co-trending-series generator.
  This is exactly the discipline that caught #150's N=3 permutation ceiling. **Cold derivation
  materially stronger.**

### §12.3 Aggregate structural overlap

Weighting by inferential load (hypotheses heavier than tunables): **overall ≈ 60–65% structural
overlap.** It decomposes as: claim/design/volume-control/steer-family **≈ 90% (strong
corroboration)**; H1b construct **≈ 80%**; H3b symmetry-insight **≈ 55%** (core idea shared,
inferential placement diverges); H2b **≈ 35%** (seed under-specified it). The agreement is
concentrated in exactly the load-bearing science that §11 reports the three blind derivers *also*
converged on — so the seed corroborates the same core the cold derivers reached independently.
The divergences are concentrated in (a) inferential *packaging* of the steer (co-movement primary
vs spine/H3b), (b) two facets the seed left thin that the canon grounds more fully (recovery,
symmetry-falsifier), and (c) operational rigor the seed lacked (re-pull, synthetic gate, RSF
downgrade).

### §12.4 Where the seed may have caught something the cold derivation under-weighted

In fairness, two items the seed flagged are *thinner* in the locked doc:
- **GDELT v2.0→v2.1 schema-version drift** (seed §4.2) is named explicitly by the seed as a source
  of spurious τ *trends*; the locked doc folds this into generic non-stationarity (§7.3) without
  calling out the dated schema changes. This is a real, datable artifact and is worth an explicit
  line — **a candidate amendment**, not a flaw in the locked tests (the within-system + thinning +
  first-differencing guards plausibly absorb it, but it should be named).
- **The explicit #151/Koopman merge question** (seed §5) is resolved in the locked doc by demoting
  Koopman to diagnostic E2; that is defensible from cont 30 §5.1, but the seed's framing ("is there
  a discrete cyclical *mode*?") is a sharper scientific question than "is broadband variance
  maintained?", and §7's own open note already concedes §10.3 is ambiguous between the two. The
  cold derivation chose the safer (broadband-variance) reading; the seed's mode reading is not
  wrong, just higher-surface-area. Neither is a defect; both are on the record.

Neither item touches an inferential threshold or falsifier; both are diagnostic/exposition
additions, safely handled under the disclosed amendment discipline (cont 30 §7.4) without
unlocking §1–§11.

### §12.5 Verdict

**The locked pre-registration is safe to take forward; the comparison reveals no problem and is
strongly reassuring.** Every point at which the seed (Pav's results-aware steer) and the blind
canon-only derivation agree — within-system design, texture-over-time, DFA-α, the volume triple-
lock, V-Dem as the steer, symmetric rejection of the value-coded binary, narrow-don't-demote — is
genuine independent corroboration that those choices follow from the framework's canon rather than
from fitting the #150 null, and these agreements sit exactly on the load-bearing science the three
blind derivers also converged on (§11). Critically, every point at which the two **diverge** runs
in the locked document's favour or is preserved as an explicit reviewable option: the cold
derivation *demotes* the seed's centerpiece (continuous steer co-movement) out of the primary slot
precisely because promoting it would re-admit the autocorrelation/volume artifact that killed
#150 — i.e. the seed was fitting an inferential weight the canon does not support — while still
flagging (§11 #1) that Cowork may re-promote it; it *promotes* two facets the seed left as prose
(shock-recovery, and a falsifier *of* the symmetry reframe) into properly-gated tests grounded in
cont 26 §2 / cont 20 / cont 27 §3; and it *catches* two operational errors the seed would have
shipped (the `data/raw/` reuse that silently defeats the volume control, and the absent synthetic
pre-validation gate). The only things the seed caught that the locked doc under-weights — the
GDELT schema-version drift line and the discrete-cyclical-mode reading of §10.3 — are
diagnostic/exposition additions that change no threshold or falsifier and are absorbable under the
disclosed amendment discipline without unlocking §1–§11. In short: the seed corroborates the core,
the canon out-grounds the seed everywhere they part, and nothing in the seed exposes a fitting
error or missing falsifier in the locked design. Proceed to lock-review and the §6 synthetic gate.
