# Pilot 2 — Ground-truth EWS validation — RESULTS & DISCUSSION (FINAL)

> **Programme-deciding gate.** Implements the LOCKED pre-registration
> `PILOT_groundtruth_validation_PRE_REGISTRATION.md` §3 (method params) + §4 (metrics/falsifier)
> EXACTLY. Every interpretive choice is logged in `confounds_groundtruth.md` (C1–C10). No parameter,
> window, margin, or definition was changed to favor the candidate metric `A_cyc`. **The result is a
> clean FAIL** — an explicitly pre-registered, valid outcome (the §4 falsifier says a FAIL narrows the
> contribution to the cross-field bridge alone and permanently defers Pilot 1 Phase E / the GDELT run).
> All numbers below are from a single real-data end-to-end run (`groundtruth_validation.py`;
> `groundtruth_results.json`), re-verified at finalization.

Run date: 2026-06-05 (finalized). DFA estimator verified **numerically identical** to the tested
`pilots/1f_failsafe/pilot.py dfa()` (`fast_dfa` vectorization, max |Δα| = 4.4e-16). Three independent
adversarial audits (data-integrity / metric-estimator / cardinal-sin lenses) returned **zero confirmed
bugs** and `verdict_honest: true`; an independent end-to-end re-run reproduced every headline number
bit-for-bit. Verification record and the one logged spec-tension (C10) are in `confounds_groundtruth.md`.

---

## 1. VERDICT: **FAIL** (clean, pre-registered)

Per the LOCKED §4 verdict bands:
- **Cascade PRIMARY gate: NOT met** — all three conditions (a), (b), (c) fail; the falsifier requires
  only one to trigger.
- **PhysioNet adds-over-static-α: NOT met** — rolling A_cyc AUC 0.646 < static-α1 AUC 0.813.
- **FAIL** = "Cascade primary gate not met → bridge-only, Pilot 1 Phase E permanently deferred."

The metric-level claim — that the **cycling amplitude `A_cyc` of rolling-DFA-α adds early-warning /
state-discrimination power beyond the one-pole CSD indicators** — is **REJECTED** on ground-truth data.
The programme's contribution narrows to the **cross-field bridge alone** (EWS ↔ physiology
loss-of-complexity synthesis); no new metric; Pilot 1 Phase E (the GDELT cycling real-data run) is
permanently deferred per the frozen §4 falsifier and cont 27 §3.

**The single most important empirical reason:** in this real, documented ecological regime shift, the
rolling-DFA-α cycling amplitude **does not collapse toward the transition — it expands**, the opposite
of the candidate's predicted mechanism. (Peter epoch-`A_cyc` rises 0.81 → 0.92 → **1.48** → 1.27 across
2008→2011, peaking in the 2010 transition year; Kendall-τ = +0.50, p ≈ 1e-27 in the *rising* direction.)
This is consistent with Carpenter et al. 2011's own report that chlorophyll "displayed strong
oscillations in 2009 and the first half of 2010" during the shift. The FAIL is **mechanism-level**, and
it holds at *both* constructions of A_cyc (see §3.1) — it is not an artifact of any analysis choice.

---

## 2. Data & ground truth (the central judgment calls — full detail in `confounds_groundtruth.md`)

| item | decision | source |
|---|---|---|
| **EDI package/entity** | Locked ID `knb-lter-ntl.355.6` resolved to the **zooplankton core-data** package (no sonde / no chlorophyll sonde series). Used the package that matches every locked §3 term — **`knb-lter-ntl.360.2`**, `squealSondesMet_08to11_forOPUS.csv`, the **5-min high-frequency sonde**, 2008–2011, Peter+Paul, with **`chl` = chlorophyll-a** (optical YSI 6025). `355.6` was a mis-recorded ID at lock time; §3 was NOT edited (C1). | EDI/PASTA catalog + EML `360.2` |
| **Texture variable** | **chlorophyll-a (`chl`)** — the §3 PRIMARY (fallback phycocyanin not needed; chl present). | EML `360.2` |
| **Cadence** | §3 daily-median of the high-frequency sonde. After daily-median aggregation, **0% within-season missing days**. | this run |
| **Span** | ice-free seasons **2008, 2009, 2010, 2011** (up to & incl. 2011), Paul over the identical calendar span. Disjoint summer blocks (~107–114 d) separated by ~8-month ice cover → per §3 rule 3, windows never cross a season boundary (C3). | this run |
| **Documented onset** | **earliest documented destabilization onset = day 193 of 2008** (first largemouth-bass addition). Transition **complete ≈ day 230 of 2010**. Sourced VERBATIM from Carpenter et al. 2011 *Science* (not derived from texture values), per §3 confound #3 (C2). | Carpenter 2011 |
| **Window / stride** | §3 LOCKED: window = **50% of usable per-series length** (`earlywarnings` default), stride = **1 daily sample**. Per season W ≈ 54–57 d on ~107–114-d seasons; ~54–58 windows/season; identical for both lakes (C4). | §3 |

**Sourced manipulation timeline (Carpenter et al. 2011 *Science* 332:1079, verbatim):** "We added 12
largemouth bass on **day 193 of 2008**, and 15 largemouth bass on each of **days 169 and 203 of 2009**."
… "monitored daily … three years of summer stratification **(2008–2010)**." … "By **day 230 of 2010**,
manipulated and reference lakes were similar in planktivore numbers, zooplankton biomass, and
chlorophyll." … warning signals "more than a year before the food web transition was complete."

---

## 3. CASCADE — `A_cyc` vs each one-pole indicator (the §4 PRIMARY gate)

All indicators computed in the **identical** single locked rolling window (W = 50% of season length,
stride 1) on the per-season z-scored, linear-detrended daily-median chlorophyll-a (C4, C7). AUC is
direction-agnostic (§3), applied identically to all indicators. Lead-time uses the locked earliest-onset
anchor (day 193/2008) for the gate, with the transition-complete anchor (day 230/2010) reported as a
field-standard cross-reference (C2, C6). Discrimination unit: 228 Peter windows vs 228 Paul windows.

### 3.1 Discrimination AUC (Peter, transition-approaching vs Paul, same-span)

| indicator | dir-agnostic AUC | vs best one-pole |
|---|---|---|
| **`A_cyc`** (P90−P10 of rolling τ) | **0.677** | candidate |
| one-pole (i) **AR(1)** | 0.651 | ← **best one-pole** |
| one-pole (ii) **variance** | 0.514 | |
| one-pole (iii) **DFA-α level** (τ) | 0.541 | |
| **best one-pole + 0.05 margin (required)** | **0.701** | A_cyc 0.677 < 0.701 |

**Condition (a) — AUC ≥ best one-pole + 0.05: FAILS.** A_cyc (0.677) beats the best one-pole (AR(1)
0.651) by only **+0.026**, short of the required +0.05 margin.

> **Construction note (corrected at finalization; see C10 disposition #5).** The table uses the
> **implemented pooled-per-window τ-spread** construction (A_cyc(t) = trailing-50% inter-decile range of
> τ; C4). This is the *conservative-against-the-candidate* reading: a *more* A_cyc-favorable framing —
> the **epoch-level** A_cyc (one P90−P10-of-τ scalar per season, the validated Pilot-1 H1b form) — scores
> a **higher** dir-agnostic AUC of **0.812** (n = 4 Peter seasons vs 4 Paul seasons, a statistically weak
> framing). We report the conservative 0.677 in the gate, NOT the cherry-pickable 0.812. **Even at 0.812
> A_cyc would clear (a) but still fail (b)** — because, as §3.2 shows, A_cyc *rises* toward the transition
> rather than declining, so its predicted warning never fires. (A_cyc's *raw* AUC is also 0.677 > 0.5, so
> the direction-agnostic `max(a,1−a)` transform — which actually only flips *variance*, 0.486→0.514 — gives
> A_cyc no artificial lift.)

### 3.2 Trend toward the transition + lead-time (days)

Warning direction per §3: A_cyc → **decline**; one-pole CSD → **rise**. Lead-time = onset_day − first day
the **trailing** Kendall-τ reaches p<0.05 in the warning direction. The detector was unit-tested as
**causal** (uses only `v[:i+1]`) and **direction-symmetric** (fires for a declining series under sign=−1
and a rising series under sign=+1), so A_cyc's null lead-time is a genuine miss, not suppressed detection.

| indicator | Kendall-τ (Peter, toward transition) | p | warning-dir trend fires? | lead vs **onset** (day193/2008) | lead vs **transition-complete** (day230/2010) |
|---|---|---|---|---|---|
| **`A_cyc`** | **+0.495** (RISES) | 1e-27 | **No** — A_cyc rises; predicted *decline* never fires | **none** | **none** |
| AR(1) | +0.015 | 0.74 | yes (trailing) | **+5 d** | +772 d |
| variance | −0.180 | 5e-5 | (+2σ band) | −362 d (Kendall) / **+65 d** (+2σ) | +405 d (Kendall) / +65 d (+2σ) |
| DFA-α level (τ) | +0.064 | 0.15 | (+2σ band) | none (Kendall) | +49 d (+2σ) |

**Condition (b) — lead-time(A_cyc) ≥ best one-pole: FAILS.** A_cyc's **predicted (declining) warning
never fires in Peter** (its trend is significantly *rising*), so it yields **no lead-time under either
anchor**. At least one one-pole indicator warns ahead of both anchors (AR(1): +5 d vs onset, +772 d vs
transition-complete; variance/τ cross the +2σ band 49–65 d before transition-complete). A_cyc loses
lead-time outright. **This condition fails independently of the AUC construction in §3.1.**

### 3.3 Paul reference must-NULL (§4c)

| indicator | Paul Kendall-τ | p | declining-warning significant? | +2σ decline crossing? |
|---|---|---|---|---|
| **`A_cyc`** | −0.281 | 6e-10 | **yes** (significant *decline* on Paul) | **yes** |
| AR(1) | +0.393 | 1e-18 | (rises on Paul too) | yes |
| variance | +0.063 | 0.15 | no | yes |
| DFA-α level | +0.141 | 0.002 | (rises) | yes |

**Condition (c) — Paul must-NULL for A_cyc: FAILS (the control FIRES).** On the unmanipulated reference
lake, A_cyc shows a *significant decline* (Kendall p ≈ 6e-10) and a +2σ crossing — a false alarm on the
negative control.

> **Honest caveat (does not rescue the metric; logged in C6 / C10).** This Paul-null firing is partly an
> artifact of the *pooled-across-disjoint-seasons* trailing construction (the four summer blocks create
> cross-season structure that the trailing statistics pick up — note the **one-pole AR(1) also "fires"**
> on Paul under the same pooled construction). At the cleaner **epoch level** (P90−P10 of τ *within each
> season*), Paul's `A_cyc` does **not** decline significantly (Kendall across seasons τ = −0.33, p =
> 0.75). So condition (c) **alone** is construction-sensitive. **But the verdict does not depend on it:**
> the §4 falsifier is "(a) OR (b) fails, OR (c) fires," and **(a) and (b) fail robustly and independently**
> of the Paul-null question — A_cyc beats the best one-pole by only 0.026 on AUC, and its predicted
> decline never materializes (it rises). The verdict is therefore stated as resting on (a) and (b).

### 3.4 §4 PRIMARY GATE result

| condition | requirement | result |
|---|---|---|
| (a) AUC margin | AUC(A_cyc) ≥ best one-pole + 0.05 | **FAIL** (0.677 vs 0.701; +0.026) |
| (b) lead-time | lead(A_cyc) ≥ best one-pole | **FAIL** (A_cyc never warns in predicted direction; AR(1) leads +5 d) |
| (c) Paul must-NULL | A_cyc no significant decline on Paul | **FAIL (fires)** *(construction-sensitive — see caveat)* |
| **PRIMARY GATE** | **all three** | **NOT MET → FALSIFIER TRIGGERED** |

**Diagnostic-only (cannot change verdict, §3 / Cowork Decision #2):** Delecroix λ = −log(AR1)/dt: Peter
0.104, Paul 0.152 (Peter's lower restoring-rate λ is the expected CSD direction, but this channel is
diagnostic-only and not in the falsifier).

---

## 4. PHYSIONET — static-α sanity + adds-over-static-α (§4 SECONDARY)

NSR `nsr2db` (n=54, healthy) vs CHF `chf2db` (n=29). RR = normal-to-normal intervals from `.ecg` beat
annotations (annotation-only DBs; no raw ECG downloaded). Static-α = DFA over the whole NN series;
rolling A_cyc = inter-decile range of rolling DFA-α (C8). RR units verified physiological (median ~711 ms
NSR / ~734 ms CHF → 82–84 bpm; the 300–2000 ms filter drops 0 beats).

| feature | NSR mean | CHF mean | dir-agnostic AUC (CHF vs NSR) | separates (≥0.70)? |
|---|---|---|---|---|
| **static α1 (canonical HRV scales 4–16)** | 1.267 | 0.996 | **0.813** | **yes — reproduces Goldberger** |
| static α (tested-DFA *default* scales 8…N/4) | 1.121 | 1.124 | 0.515 | no |
| **rolling A_cyc** (the test feature) | 0.293 | 0.256 | **0.646** | — |

- **Sanity (does static α separate healthy/CHF?):** **YES** in the canonical short-term HRV configuration
  (α1, scales 4–16 beats; AUC 0.813) — Goldberger et al. 2002's own result reproduced. *Note:* the
  tested-DFA **default** scale range (8…N/4, designed for ~110-day lake seasons) spans far beyond the
  canonical HRV band and washes the separation out (AUC 0.515). This is an honest scale-domain observation
  about the locked estimator's defaults on very long RR series — the **data and RR extraction are
  correct** (the canonical α1 separates cleanly, and the sonde `chl` cross-validates r=0.84–0.90 against
  the independent Carpenter-2011 daily companion 374.2). This baseline ambiguity is logged as **C10**.
- **The test (does rolling A_cyc add over static α by +0.05?):** **NO.** Rolling A_cyc AUC 0.646 is **well
  below** the proper static-α1 baseline (0.813) — the rolling amplitude is a *weaker* NSR/CHF
  discriminator than plain static α, not an additive one. A_cyc clears +0.05 *only* over the deliberately
  mis-scaled default-scale static-α (0.515) — comparing against a baseline that fails to reproduce
  Goldberger would be misleading, and §4 SECONDARY explicitly references "Goldberger's own result," i.e.
  the canonical baseline (C10). **The implementation deliberately uses the harder, correct HRV baseline —
  the anti-candidate choice — and reports both transparently.**

**PhysioNet conclusion:** the rolling-amplitude metric does **not** add discrimination over static α in
physiology either. (Per §4, PhysioNet cannot upgrade a Cascade FAIL regardless. Fantasia was not run —
SECONDARY/optional, not needed once the PRIMARY and the NSR/CHF secondary both went against A_cyc.)

---

## 5. Interpretation — why the candidate fails, honestly

1. **Direction is wrong on real data.** The candidate predicts cycling-amplitude *collapse* toward a
   transition. In the textbook ecological regime shift (Carpenter's Cascade), the rolling-DFA-α cycling
   amplitude **expands** through the transition (Peter epoch-A_cyc peaks in the 2010 shift year; rising
   Kendall τ=+0.50). The transition is an *oscillatory* food-web reorganization (predator–prey cycles,
   "strong oscillations in 2009–2010"), which *increases* α-variability rather than flattening it. The
   amplitude-collapse mechanism that motivated the metric is not what a real approaching transition looks
   like here.
2. **Even direction-agnostically, it doesn't clear the bar.** Treating A_cyc as a pure discriminator
   (ignoring sign), it beats the best one-pole by only +0.026 AUC — below the pre-registered +0.05 margin —
   and provides no earlier warning than AR(1)/variance.
3. **It does not generalize to physiology.** On NSR/CHF, static α1 already separates classes (AUC 0.813);
   the rolling amplitude is *weaker* (0.646), not additive.
4. **The one-pole baselines remain the stronger, earlier signal** on this ground truth (AR(1) AUC 0.651,
   warns ahead of both onset anchors; variance/τ cross +2σ ~7–9 weeks before the completed transition) —
   consistent with the established CSD literature this programme was hoping to *beat*.

---

## 6. Evidence tiering (cont 27 §2)

- **Tier 1 (measured, direct):** every number in §3–§4 — the AUCs (A_cyc 0.677; AR(1) 0.651; var 0.514;
  τ 0.541; PhysioNet static-α1 0.813, rolling A_cyc 0.646), the Kendall-τ trends and p-values, the
  lead-times, the Paul-control statistics, the window/season counts, the DFA-identity check
  (max|Δα|=4.4e-16). These are direct outputs of the locked pipeline on real downloaded data,
  independently reproduced bit-for-bit and audited (zero confirmed bugs).
- **Tier 2 (interpretive, conditional on this result):** "the cycling-amplitude metric A_cyc **does not**
  add value over one-pole CSD" — this is the Tier-2 *conclusion* the gate was built to adjudicate, and on
  this ground truth it lands on the **REJECT** side. Equivalently, the surviving Tier-2 claim is the
  **cross-field bridge** (EWS ↔ physiology loss-of-complexity synthesis), which this pilot does not test
  and does not damage.
- **Tier 3 / honest caveats (logged, none change the verdict):** Paul-null construction-sensitivity (§3.3);
  lead-time anchor near-degeneracy (the sonde record starts ~day 134/2008, ~2 months before the day-193
  onset — C2); the PhysioNet static-α scale-domain ambiguity (C10); short within-season series for DFA
  (§5.2 confound). All are disclosed; (a) and (b) fail robustly regardless.

---

## 7. For Cowork next (gate logic, per §6 of the pre-reg)

**Outcome = FAIL → execute the FAIL branch (NOT the PASS branch).**

- **Narrow the contribution to the cross-field BRIDGE ALONE.** Outreach/positioning becomes "we
  *synthesize* your two literatures (ecological EWS ↔ physiological loss-of-complexity, which do not cite
  each other)" — **not** "we *extend* EWS with a new metric." No new-metric claim ships.
- **DEMOTE the cycling-amplitude metric per cont 27 §3** (the metric-novelty layer) — **NOT** cont 26 §3
  (the substrate-level canon, which is untouched: the symmetric two-pole DFA-α picture was already ceded to
  Goldberger 2002 per Reading 06 §10.3 third amendment, and nothing here disturbs it).
- **Pilot 1 Phase E (the GDELT cycling real-data run) is PERMANENTLY DEFERRED** per the frozen §4
  falsifier. Do not schedule it.
- **Do NOT trigger the PASS-branch actions:** no Pilot 1 Phase E unlock, no **Bar B** of the cycling
  candidate, and **no Reading 06 §10.3 *fourth* amendment** promoting bridge+metric to "Tier-2-confirmed."
  Those were contingent on a PASS and are now closed.
- **Reading 06 §10.3 amendment to file (FAIL form):** record that the rolling-amplitude metric was tested
  on ground truth and **rejected** (Cascade primary gate not met; mechanism runs opposite to prediction —
  amplitude *expands* toward the transition), so the programme's contribution is the bridge synthesis only.
- Report cleanly, no retro-fitting, no margin-moving (cont 27 §2–§3). The FAIL is the expected,
  pre-registered valid outcome.

---

## 8. Reproduce

```
cd pilots/1f_failsafe_cycling/results_groundtruth
python groundtruth_validation.py
```
Inputs (downloaded, real): `../data_groundtruth/cascade/sonde_360_squeal.csv` (EDI `knb-lter-ntl.360.2`);
PhysioNet `nsr2db`/`chf2db` via `wfdb` (annotation-only, no raw ECG). Outputs: `groundtruth_results.json`,
`cascade_tau_trajectories.png`, `physionet_dfa.png`. DFA reused verbatim from the tested
`pilots/1f_failsafe/pilot.py` (via the proven-identical `fast_dfa`). All judgment calls + the
finalization verification record: `confounds_groundtruth.md` (C1–C10).

### Limitations (logged, none change the verdict)
- **Short within-season series** (§5.2 confound): DFA-α on a 50%-window of a ~110-day season is short;
  pre-committed window rule honored; per-window fit uses the tested estimator unchanged.
- **Lead-time anchor degeneracy** (C2): the sonde record starts ~day 134/2008, ~2 months before the
  day-193/2008 first bass addition, so "lead time before the 2008 onset" is near-degenerate by experiment
  design; both the locked-onset and the transition-complete anchors are reported, and A_cyc loses under
  *both*.
- **Paul-null construction-sensitivity** (§3.3 caveat): condition (c) depends on the pooled-vs-epoch
  construction; (a) and (b) fail robustly regardless, so the FALSIFIER is triggered independently.
- **PhysioNet DFA scale domain** (C10): the tested-DFA default scales under-separate NSR/CHF on long RR
  series; the canonical HRV α1 (4–16) reproduces Goldberger and is the proper baseline used for the
  verdict; both reported.
