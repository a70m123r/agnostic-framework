# confounds_groundtruth.md — post-lock implementation decisions (dated)

> Per the LOCKED pre-registration §0: "Any issue discovered after data download goes in a NEW
> `confounds_groundtruth.md` (dated), never by editing §3/§4 retroactively." This file logs every
> judgment call made while implementing the locked §3/§4 against the real data. **No §3 parameter,
> §4 metric, margin, or falsifier was changed.** Where the lock is silent or genuinely ambiguous, the
> choice taken is the one that is (a) standard in the named `earlywarnings` convention and (b) does
> NOT advantage the candidate metric A_cyc (CARDINAL RULE).

Author: Claude Code, 2026-06-05. Run is end-to-end on real downloaded data.

---

## C1 — EDI package/entity correction (the central data judgment call)

**Issue.** The locked pre-reg names EDI package `knb-lter-ntl.355.6` with two entities
(`374245bd…`, `6840b59648…`). On download these resolve to:
- `374245bd…` = `cascade_zooplankton_v06.csv` — **Cascade Project CORE DATA ZOOPLANKTON 1984–2019**
  (net-tow zooplankton counts; lakeid/taxon/biomass). NOT a high-frequency sonde series.
- `6840b59648…` = `CascadeManual1998.pdf` — a methods PDF (not data).

So package `355.6` is the zooplankton core-data package; it contains **no high-frequency sonde
series and no chlorophyll-a / phycocyanin sonde variable.** The lock's §11 attestation verified only
that "the package resolves with 2 data entities" — it did not verify those entities were the sonde
series. (Lock discipline was preserved: existence/metadata only, values unexamined.)

**Resolution (faithful to §3, not a §3 edit).** §3 locks the *data type and variable*, not just an ID:
"aggregate each raw series to daily medians (**Cascade high-frequency sonde**)"; "Primary texture
variable: **chlorophyll-a**; if absent … phycocyanin/BGA"; "ice-free season(s) up to and including
the documented Peter manipulation year (2011); Paul over the identical calendar span." I searched the
EDI/PASTA catalog for the Cascade high-frequency sonde package that matches these locked terms. The
unique match is:

- **`knb-lter-ntl.360.2`** — "Cascade Project at North Temperate Lakes LTER **High Frequency Sonde
  Data** from Food Web Resilience Experiment **2008–2011**", entity
  `squealSondesMet_08to11_forOPUS.csv` (254 526 records). EML methods: "Data were collected at **5
  minute intervals** using in-situ automated sensors (sondes)… **optical Chl-a (model 6025)**… Peter
  and Paul lakes… food web of **Peter** Lake was slowly transformed by **gradual additions of
  Largemouth bass**… **Paul** Lake was an unmanipulated reference." Variable **`chl`** = "Water
  chlorophyll concentration."

This package matches every locked §3 term exactly: high-frequency sonde (5-min), chlorophyll-a
present, Peter(manipulated)+Paul(reference), span 2008-up-to-and-including-2011. It is the dataset §3
*describes*; `355.6` was a mis-recorded ID at lock time. Using `360.2` implements §3 as written.
The mis-ID is logged here, not fixed by editing §3.

**Cross-check companion (not the analysis input).** `knb-lter-ntl.374.2` ("Daily data for key
variables in whole lake experiments on **early warnings of critical transitions, Paul and Peter
Lakes, 2008-2011**", entity `Paul_Peter_2008-2011.csv`, columns `Chla`, `LMinnCPE`) is the
already-daily-aggregated Carpenter-2011 companion. Downloaded for provenance/sanity only; the locked
"daily-median high-frequency sonde" rule means the **360.2 sonde, daily-median-aggregated by us, is
the analysis input** (not the pre-aggregated 374.2). 374.2 is used only to sanity-check magnitudes.

## C2 — Documented Peter destabilization onset date (sourced, not derived from values)

Per §3 confound #3: shift date "taken from Carpenter et al. 2011 / EDI metadata (published, not
derived from the texture values). If multiple candidate dates exist, the **earliest documented
destabilization onset** is used (pre-committed)." Sourced verbatim from Carpenter et al. 2011
*Science* 332:1079 (Cary Institute preprint PDF, text-extracted):

- "We added 12 largemouth bass on **day 193 of 2008**, and 15 largemouth bass on each of **days 169
  and 203 of 2009**." → **earliest documented destabilization onset = day 193 of 2008** (first
  piscivore addition; this is the pre-committed "earliest" anchor for §4 lead-time).
- "monitored daily in both lakes for three years of summer stratification **(2008–2010)**."
- "By **day 230 of 2010**, manipulated and reference lakes were similar in planktivore numbers,
  zooplankton biomass, and chlorophyll." → **food-web transition COMPLETE ≈ day 230 of 2010.**
- "Warning signals … evident … **more than a year before the food web transition was complete**";
  chlorophyll "displayed **strong oscillations in 2009 and the first half of 2010**."

**Decision.** The locked §4 lead-time is "days before the documented Peter destabilization **onset**"
and confound #3 fixes "earliest documented destabilization onset." The literal locked anchor is
therefore **day 193 of 2008** (first bass addition). I report lead-time against that locked anchor.
**Caveat (logged, not a change):** the sonde record begins 2008-05-13 (≈ day 134), only ~2 months
before day 193, so there is essentially no pre-manipulation baseline — "lead time before the 2008
onset" is therefore near-degenerate by construction (a property of the experiment, not the metric).
I therefore ALSO report, as a transparency cross-reference, the lead-time against the **transition-
COMPLETION anchor (day 230 of 2010)** — the field-standard reference Carpenter 2011 itself uses
("more than a year before"). Neither anchor was chosen to favor A_cyc; both are reported for every
indicator identically. The §4 PASS/FAIL verdict uses the **locked earliest-onset anchor**.

## C3 — Seasonal (ice-covered) gaps → within-season windowing (§3 rule 3)

The sonde series is four disjoint ice-free summer blocks (May–Sept) per lake: 2008 (≈107 d), 2009
(≈114 d), 2010 (≈113 d), 2011 (≈113 d), separated by ~8-month ice-covered winters with NO data. §3
pre-processing rule 3: "gaps >2 samples → windowed (not interpolated across)." The winter gaps are
~250 samples, so DFA/rolling windows are **never run across a season boundary**; each season is an
independent windowed segment. After daily-median aggregation, **0% of within-season days are missing**
(every sampled day has ≥1 valid 5-min chl reading), so no within-season interpolation is needed.

## C4 — "Usable per-series length" and the single locked rolling window

§3 locks ONE rolling window: "Rolling window = **50% of the usable per-series length** (the
`earlywarnings` toolbox default …); **stride = 1 daily sample**." `earlywarnings::generic_ews`
default is `winsize = 50` (percent of series length). I apply it **per season** (the continuous
usable series, per C3): window W = round(0.50 × season_length) days, stride = 1 day. Within each
window position I compute, in the **identical** framework, the per-window scalar of every indicator:
- one-pole (i) **AR(1)** = lag-1 autocorrelation of detrended chl in the window;
- one-pole (ii) **variance** = variance of detrended chl in the window;
- one-pole (iii) **DFA-α level** = `dfa_fast`(chl in window) = the locked **τ(t)** (rolling DFA-α);
- candidate **A_cyc(t)** = inter-decile range (P90−P10) of the τ trajectory within the **same**
  trailing 50%-window of τ-samples. (This makes A_cyc a trajectory with a Kendall-τ trend and a +2σ
  band — required by §4(b) lead-time and §4(c) Paul-null, which both reference "A_cyc … Kendall-τ" —
  using the **same locked 50% fraction**, introducing no new parameter.)

This is the **single-window** reading. Because A_cyc is, per §3, "P90−P10 of τ(t)" (a dispersion of
the τ trajectory) while the one-pole indicators are per-window scalars, A_cyc necessarily sits one
level up (a spread of τ over a stretch). The lock's own §4(c) ("A_cyc shows no significant decline …
Kendall-τ p>0.05") requires A_cyc to be a *trajectory*; the only construction that (a) yields an
A_cyc trajectory, (b) uses the locked 50% rule, and (c) adds no DOF is the trailing-50%-of-τ
inter-decile range above. The DFA `scale_min`/`scale_max` are the tested `dfa_fast` defaults
(scale_min=8, scale_max=W//4) — unchanged from the verified estimator.

## C5 — §4 AUC discrimination unit (Peter vs Paul, "same-span")

§4 AUC = "ROC area discriminating manipulated (Peter, transition-approaching windows) vs reference
(Paul, same-span windows)." The repeated discrimination unit is the **rolling window** (per-window
scalar), pooled over the transition-approaching span and matched by **same calendar window** in Paul
("same-span"). For each indicator I pool its per-window scalar values across Peter windows (label 1)
vs Paul windows (label 0) over the identical seasons/calendar span, and compute ROC-AUC (Mann–Whitney
U / n1 n2). For the one-pole indicators the per-window scalar is AR1(t)/Var(t)/τ(t) directly; for
A_cyc it is A_cyc(t) (the trailing τ inter-decile range, C4). AUC is **direction-agnostic** per §3
("Decline in A_cyc … Direction-agnostic"): I report AUC = max(AUC_raw, 1−AUC_raw) so that a metric
which separates the lakes in EITHER direction scores its true discrimination — applied identically to
ALL indicators, so A_cyc gets no special treatment. ("Transition-approaching" = the locked span up to
and incl. 2011; the documented transition completes mid-2010, so 2009–2010 windows are the
approach.)

## C6 — Kendall-τ trend "toward the transition", lead-time, +2σ band (§4)

§3: each one-pole indicator "summarized by **Kendall-τ trend** toward the transition." §4 lead-time:
"days before the documented Peter onset at which the indicator's **trailing Kendall-τ** trend first
reaches **p<0.05** (or crosses a pre-shift **+2σ** band)." Implementation, identical for all
indicators incl. A_cyc:
- **Kendall-τ trend** = Kendall rank correlation of the indicator's per-window trajectory vs window-
  centre time, over the analysis span ordered toward the transition. p from the standard Kendall test
  (scipy `kendalltau`). For the one-pole CSD indicators "warning" = a *rising* trend (one-sided as in
  the field); for A_cyc "warning" = a *declining* trend (§3) — direction-agnostic magnitude reported
  too. The "best one-pole" for each metric = whichever of (i)–(iii) scores highest on that metric.
- **Lead-time** = (onset_day − first window-centre day at which the **trailing** Kendall-τ (computed on
  all windows up to that point) reaches p<0.05 in the warning direction). Reported against BOTH
  anchors of C2. The +2σ band is reported as a cross-check (first crossing of pre-shift mean ± 2 SD).
- **Paul-null** (§4c): the SAME trailing-Kendall-τ on Paul must give p>0.05 (no significant decline)
  and no +2σ crossing.

## C7 — z-score / detrend (§3 rule 3)

§3: "Per-series z-score; linear-detrend." Applied per season per lake to the daily-median chl before
the rolling computation (z-score then remove linear trend), identical for both lakes — exactly the
prior-pilot `_preprocess` convention. AR(1)/variance/DFA are then computed on this standardized,
detrended within-season series.

## C8 — PhysioNet RR extraction (§3, §4 SECONDARY)

§3: "use the native RR-interval sequence (PhysioNet); native cadence read from METADATA." nsr2db (54
records, healthy NSR) and chf2db (29 records, CHF) are **annotation-only** (sig_len=0): RR intervals
are taken from the `.ecg` beat annotations (fs=128 Hz from the header) as successive **normal-to-
normal (NN)** interval differences (beats with symbol 'N' only — standard HRV practice; ectopic
A/V/noise beats excluded). Fantasia is SECONDARY/optional and uses beat annotations ONLY (never the
~307 MB raw ECG); included only if it does not bloat the run. **static-α** = DFA-α over the whole NN
series per record (tested `dfa`); the rolling-amplitude feature = A_cyc (inter-decile range of
rolling DFA-α over the NN series, same construction as Cascade). The §4 SECONDARY test: does
AUC_rolling ≥ AUC_static-α + 0.05 (NSR vs CHF)?

## C9 — Delecroix λ (diagnostic only, §3 / Cowork Decision #2)

λ = −log(AR1)/dt reported for completeness; explicitly CANNOT change the §4 verdict.

---

## ADDENDUM — 2026-06-05 (Step 3 finalization audit; this entry added by Claude Code)

> Three independent adversarial audits (data-integrity lens, metric/estimator lens, and a
> cardinal-sin-hunting lens) were run over `groundtruth_validation.py` + `groundtruth_results.json`.
> **All three returned `confirmed_bugs: []`, `result_trustworthy: true`, `verdict_honest: true`.**
> I (Claude Code) then independently re-ran the pipeline end-to-end and unit-tested the load-bearing
> functions. **No code was changed** — there was no bug to fix and the CARDINAL RULE forbids touching
> any locked §3/§4 parameter. The full-rerun reproduced every headline number bit-for-bit
> (A_cyc AUC 0.6773, AR(1) 0.6513, var 0.5136, τ 0.5413; gate a/b/c all False → PRIMARY_PASS False;
> PhysioNet static-α1-HRV 0.8129, rolling A_cyc 0.6462; verdict FAIL; DFA max|Δα|=4.44e-16).
> This addendum records the verification done and the ONE genuine locked-spec tension surfaced
> (C10), per the Step-3 instruction to log spec-level issues in a dated confound rather than silently
> editing §4.

### Verification performed (no code changed)
- **DFA identity**: `verify_against_pilot()` → `fast_dfa == pilot.dfa`, max|Δα| = 4.44e-16 (< 1e-9). ✓
- **Lead-time detector is causal + direction-symmetric** (unit-tested): on a monotone *rising* series
  `trailing_kendall_first_sig(...,+1)` fires and `(...,−1)` returns None; on a *declining* series the
  reverse. The firing index is identical whether computed on a truncated `v[:k]` prefix or the full
  series (strict `v[:i+1]` causality). ∴ A_cyc's "predicted-declining warning never fires in Peter"
  is a **genuine mechanism failure** (Peter A_cyc rises, τ=+0.495), not a suppressed/under-powered
  detection. ✓
- **Direction-agnostic AUC `max(a,1−a)` is applied identically to all four indicators**; the flip
  actually fires only for **variance** (raw 0.4864 → 0.5136) — i.e. it helps a *one-pole baseline*,
  not the candidate. A_cyc's **raw** AUC is already 0.6773 (> 0.5), so the dir-agnostic transform does
  NOT rescue A_cyc: it separates the lakes in the (mechanistically wrong) direction and still falls
  short of the 0.701 bar. The dir-agnostic framing is, if anything, generous to A_cyc and it still
  fails (a). ✓
- **AUC pooling is balanced/non-degenerate**: 228 Peter windows vs 228 Paul windows. ✓
- **Data are real and correct**: `chl` (chlorophyll-a) column, 5-min sonde cadence, both lakes,
  seasons 2008–2011; per-lake-year daily-median day counts (107/114/113/113) and window days
  (54/57/56/56) reproduce. ✓
- **The FAIL is not an artifact of the trailing A_cyc construction**: at the *more* A_cyc-favorable
  **epoch level** (one P90−P10-of-τ scalar per season), the dir-agnostic A_cyc AUC is **0.8125**
  (n=4 vs 4) — which *would* clear cond-(a)'s 0.701 bar — yet cond-(b) **still fails** because Peter
  epoch A_cyc *rises* (0.811→0.917→1.476→1.270; τ=+0.667, peaking in the 2010 transition year), the
  opposite of the predicted collapse. So even the construction most charitable to A_cyc cannot
  produce a PASS; the FAIL is mechanism-level. The implemented (less-charitable) pooled-per-window
  construction is therefore conservative-against-the-candidate on the AUC gate, NOT pro-candidate. ✓

### C10 — §4 SECONDARY static-α baseline: a genuine locked-text tension (logged, gate evaluated as locked)
**Issue.** §4 SECONDARY pre-registers the static-α sanity/baseline as **"Goldberger's own result"**
(static α separating NSR≈1 / CHF-high). But "static α" can be computed at two scale ranges, and they
diverge on RR series:
- **tested-DFA *default* scales** (scale_min=8, scale_max=N//4 — the locked Pilot-1 estimator
  defaults, designed for ~110-day lake seasons): on the ~10⁵-beat RR series these span far beyond the
  short-term HRV band and **do NOT reproduce Goldberger** — NSR 1.121 vs CHF 1.124, AUC **0.515** (no
  separation). The data are fine; this is a scale-domain property of the default window on very long
  series.
- **canonical short-term HRV α1** (scales 4–16 beats — the configuration Goldberger et al. 2002 *PNAS*
  actually use): NSR 1.267 vs CHF 0.996, AUC **0.813** — **reproduces Goldberger** exactly.

The locked text names the *result* ("Goldberger's own result") but not the *scale range*, so which
"static α" is the §4 baseline is genuinely ambiguous in the lock.

**Resolution (does NOT edit §4; both reported; gate evaluated as locked).** The verdict-relevant
`adds_over_static_alpha` uses the **canonical HRV α1 baseline (AUC 0.813)** because that is the
configuration that *is* "Goldberger's own result" the lock refers to, and it is the scientifically
correct NSR-vs-CHF comparison. Under it, rolling A_cyc (AUC 0.646) does **NOT** add (0.646 < 0.813 +
0.05). **Note the direction of this choice:** the code also computes `adds_over_static_alpha_default`
and it is **True** (0.646 ≥ 0.515 + 0.05) — i.e. choosing the *default-scale* baseline would have let
A_cyc "add." The implementation deliberately picked the baseline that makes the SECONDARY **FAIL**.
This is the **anti-candidate** direction (consistent with an honest FAIL, never a faked PASS). Both
baselines are reported transparently in `groundtruth_results.json` and `discussion.md`.

**Gate impact: none.** PhysioNet is SECONDARY; per §4 it cannot upgrade a Cascade FAIL regardless,
and the Cascade PRIMARY gate already fails robustly on (a) and (b). The SECONDARY also fails under the
proper baseline, so the overall verdict (FAIL) is unchanged under *either* reading of this ambiguity.

### Disposition of the three audits' "deviations" (all dispositioned; zero code changes)
1. **EDI 355.6 → 360.2 substitution (C1):** legitimate; 355.6 genuinely resolves to a zooplankton
   package with no sonde/chl, 360.2 is the unique package matching every §3 term. §3 implements as
   written. Not pro-A_cyc.
2. **A_cyc trailing-trajectory construction (C4):** required by §4(b)/(c) language ("A_cyc … Kendall-τ
   … +2σ"), adds no DOF, and is *conservative* against the candidate (epoch-level reading scores 0.81
   on AUC vs the implemented 0.677). Not pro-A_cyc.
3. **PhysioNet 50% window → fixed-window-count on RR (C8):** a literal 50% window yields ONE window on
   a 10⁵-beat series; the rolling construction *gives A_cyc a trajectory it would not otherwise have*
   (favorable to A_cyc) and is on the SECONDARY channel, which cannot change the verdict. Disclosed.
4. **PhysioNet HRV-α1 baseline (C10 above):** anti-candidate, scientifically correct, both reported.
5. **discussion.md §3.1 wording imprecision** (the audits' one shared nit): the previous draft called
   the pooled-per-window AUC (0.677) "the most A_cyc-favorable construction," but the epoch-level
   dir-agnostic A_cyc AUC is actually **higher (0.8125)**. The old wording *understated* how good A_cyc
   could look under a weaker (n=4-vs-4) framing. **Corrected in the final discussion.md §3.1** (this
   finalization): the pooled construction is now labeled the *implemented/conservative* one, with the
   epoch-level 0.81 stated explicitly and the note that cond-(b) fails under it too. Documentation-only;
   no number and no verdict changes.
