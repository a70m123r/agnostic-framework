# SCOUT — Critical Transitions / Early-Warning-Signals (EWS) field

> **STATUS: SCOUT — findings for Pav/Cowork steer; NOT canon, NOT a promoted candidate.**
> Date: **2026-06-04**. Synthesis of 4 independent web-research scouts (all URLs live-verified June 2026 unless flagged). This document exists to *steer* the cycling-capacity programme, not to be cited as settled. Every load-bearing claim carries a Tier tag (Tier 1 = established/empirical, Tier 2 = candidate, Tier 3 = speculative). Read §1 first — the headline is a discipline-imposing one.

---

## §1 — The novelty verdict (the crux)

**Verdict: SYNTHESIS + a metric-level shift, NOT an invention. The symmetric two-pole idea is largely prior art; the genuinely under-occupied seam is narrow and specific.** This is a valuable finding, not a failure — it tells us exactly what to claim and what to drop.

Decompose the programme's claim into three parts and grade each:

| Sub-claim | Verdict | Closest prior art |
|---|---|---|
| (a) "Failure is **symmetric**: over-correlation (α≫1) **or** whiteness (α≈0.5), both = loss of complexity" | **ALREADY PUBLISHED, near-verbatim, in DFA-α terms** (Tier 1) | Goldberger et al. 2002 PNAS |
| (b) "Health = **intermediate** structure (broadband 1/f, α≈1)" | **TAKEN** (Tier 1) | Goldberger 2002; Vaillancourt & Newell 2002; brain-criticality "distance to criticality" |
| (c) "The diagnostic of failure is **collapse of the temporal cycling AMPLITUDE** — the oscillation between A+ and A- dying over a rolling window, in either direction — NOT a particular α level" | **Could not be found operationalized** (Tier 2) | Conceptual only: Holling adaptive cycle (r↔K); neuro "dynamic repertoire shrinks in disease" |

### The single most important sentence in this report

Goldberger, Amaral, Hausdorff, Ivanov, Peng & Stanley (2002, PNAS), verified verbatim via the open PMC mirror (PMC128562):

> *"the breakdown of fractal physiologic complexity may be associated with excessive order (pathologic periodicity), on the one hand, or uncorrelated randomness, on the other."*

That is the symmetric two-pole claim, on the *same DFA-α axis* the programme uses (healthy α≈1 / 1/f; ordered pole α≈1.3+ e.g. heart failure / Cheyne-Stokes; random pole α≈0.5 e.g. atrial fibrillation). **We do not own "symmetric failure exists." Goldberger 2002 owns it.** Three of four scouts independently converged on this exact paper as the closest prior art. Overclaiming symmetry-novelty is the single biggest reviewer-credibility risk in the whole programme.

### Why the EWS contrast is the *right* contrast but must be drawn carefully (Tier 1)

The canonical EWS / critical-slowing-down (CSD) field (Scheffer 2009; Dakos 2012; Lenton 2012; Dakos 2024 review) is **predominantly one-pole**: it predicts *rising* lag-1 autocorrelation / *rising* variance / *slowing* recovery / *rising* DFA-α toward **one** approaching fold. Critically, the field's own toolbox (early-warning-signals.org) computes **rolling DFA-α with a Kendall-τ trend test — exactly the instrument the programme uses** — and reads a *rising* α as the warning. It never treats α→0.5 whiteness as a co-equal failure, and it never tracks cycling-amplitude collapse.

**BUT** — and this is the honesty guardrail — the EWS field already contains the seeds of two-sidedness, so "EWS only knows one pole" is **too strong** and will get the framing rejected:
- **Critical *speeding up*** (Titus, Gelbaum & Watson 2019, arXiv:1901.08084): some transitions show *falling* autocorrelation / whitening as the opposite pole to CSD. This already *names* both poles.
- **The Hopf case**: AC1 *decreases* / variance is non-monotonic before oscillatory instability.
- **Bidirectional psychopathology EWS** (Olthof / Wichers / Scheffer): EWS precede *both* improvement and deterioration, and indicators are direction-dependent.

So the field knows the canonical signal can *flip sign per transition type* — it just has never unified this into a single "health = cycling capacity" construct.

### What actually survives as a contribution (Tier 2 — the candidate)

Two things, claimed *together*, and nothing more:

1. **A cross-field SYNTHESIS / bridge.** The EWS/critical-transitions literature (Scheffer, Lenton, Dakos, Boers) and the physiology *decomplexification* literature (Goldberger, Lipsitz, Costa, Peng) describe the *same two-pole phenomenon* and **barely cite each other**. Verified: the 2024 Dakos *ESD* review gives DFA a single Table-2 line and **never** cites Goldberger / loss-of-1/f / decomplexification. Unifying them under one cycling-capacity construct is defensible and citable.

2. **A diagnostic shift: from static LEVEL to cycling AMPLITUDE.** Every prior thread diagnoses a *static level* — distance of the exponent/complexity/criticality from its healthy value at a point in time (and the physiology work is largely *cross-sectional*: healthy-vs-diseased populations). **None** diagnose failure as the *collapse, over a rolling window, of the amplitude of α's oscillation between regimes.* "Health = capacity to keep moving between exploration and consolidation; failure = that movement flatlining in either direction" is a second-order (dynamics-of-the-dynamics) statement that the scouts could not find operationalized as a rolling-DFA-α cycling-amplitude statistic.

### The honest one-paragraph framing the programme should adopt

> *We do not claim symmetric two-pole failure is new — Goldberger et al. 2002 states it verbatim on the DFA-α axis, and Vaillancourt & Newell 2002 argue complexity change is bidirectional. We do not claim health-as-intermediate-complexity is new. Our contribution is (1) to BRIDGE two disjoint literatures — generic EWS/CSD and physiology decomplexification — that describe the same phenomenon without citing each other, and (2) to shift the diagnostic from the static LEVEL of the exponent (what all prior art measures) to the COLLAPSE OF THE CYCLING AMPLITUDE over a rolling window. We must explicitly distinguish this from relabelled CSD: our metric is the amplitude of cycling, not a pole level.*

### Confidence caveats on the verdict (Tier 2)

- Search was **focused, not exhaustive.** Someone may have operationalized "cycling-amplitude collapse" under other keywords: *time-varying Hurst/α variance*, *metastability-index decline*, "complexity of complexity," *dynamic-repertoire shrinkage*. A targeted follow-up scout on **rolling-DFA-α variability (level vs amplitude) as a clinical marker** would harden — or puncture — claim (c). This is the highest-value de-risking move before any preprint.
- The **brain-criticality "distance to criticality"** biomarker literature is moving fast (2024 bioRxiv) and is the likeliest place a *temporal-instability-of-criticality* idea could already be emerging. Worth a dedicated scout.

---

## §2 — Ground-truth datasets to validate the measure on (ranked)

The disciplined move: **validate the instrument where the answer is known** before claiming anything on social streams. Ranked by how cleanly they give a *labelled positive-vs-negative* (transition vs no-transition) structure, with a bias toward cases where one-pole CSD is *documented to fail* (those are the differentiating tests).

### Tier-1 anchors (open data, known ground truth)

**#1 — Cascade Project whole-lake experiment (Peter / Paul Lakes, NTL-LTER).** ★ Best single anchor.
- URL: <https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-ntl.355.6> (PASTA API: <https://pasta.lternet.edu/package/eml/knb-lter-ntl/355>)
- **Ground truth:** Carpenter et al. 2011 *Science* 332:1079. Peter Lake was *deliberately destabilized* (added piscivorous bass → trophic-cascade regime shift); adjacent **Paul Lake was an unmanipulated reference that did NOT transition.** A dated positive **and** a matched negative control in one experiment. Published EWS (rising variance, rising AR(1), spectral reddening) appeared >1 yr before the shift completed. High-frequency sonde data (DO, pH, chl-a, phycocyanin, temp; every 5 min, summers 2008–2015) → rolling DFA-α is feasible. *Note: textbook one-pole; the reference lake is your null.*
- **Access:** OPEN CSV via EDI portal + PASTA REST API.

**#2 — PhysioNet labelled physiology pairs.** ★ Best for the *symmetric two-pole* test specifically (this is Goldberger's own home turf — replicate, then extend).
- Root: <https://physionet.org/>
- **nsr2db** (healthy, α≈1 broadband): <https://physionet.org/content/nsr2db/1.0.0/> — 54 long-term normal-sinus-rhythm ECG records.
- **chf2db** (CHF, structure loss / over-correlation pole): <https://physionet.org/content/chf2db/1.0.0/> — 29 records, NYHA I–III.
- **Fantasia** (healthy young vs elderly — benign covariate that shifts α *level*): <https://physionet.org/content/fantasia/1.0.0/> — 20+20 rigorously screened, 120 min ECG+resp @250 Hz.
- **Ground truth:** clinical/age labels. Healthy = α≈1; CHF drifts toward over-correlation; AF toward α≈0.5 fragmentation → a *natural two-pole test bed*. Fantasia is the caution that α-*level* moves with a benign covariate (supports "failure is amplitude-collapse, not a level").
- **Access:** OPEN, no credentialing. `aws s3 sync --no-sign-request s3://physionet-open/<db>/1.0.0/ DEST` or `wget -r`.

**#3 — Lake Veluwe / Lake Erhai eutrophication ("flickering").** ★ Best *differentiating* case — one-pole CSD documented to *disagree with itself*.
- URL: <https://www.nature.com/articles/nature11655> (open via <https://pubmed.ncbi.nlm.nih.gov/23160492/>)
- **Ground truth:** Wang, Dakos, Scheffer et al. 2012 *Nature* 492:419. Before a dated transition to the turbid eutrophic state, **variance rose but skewness AND autocorrelation DECLINED** — the canonical one-pole indicators disagreed and AR(1) moved the *wrong* way. **This is direct empirical evidence that single-pole CSD is not the whole story** — the cleanest real-world case where a two-pole/amplitude diagnostic could *outperform*.
- **Access:** Paper open; raw series in the Nature SI + author request; reconstructed series in follow-up methods papers.

### Tier-1 supporting datasets (dated within-subject transitions / negative controls)

| Dataset | URL | Ground truth | Why |
|---|---|---|---|
| **Depression ESM (Kossakowski/Wichers)** | data: <https://osf.io/j4fg8> · paper: <https://openpsychologydata.metajnl.com/articles/10.5334/jopd.29/> | N=1, 239 days, ~10×/day ESM; **double-blind venlafaxine taper** provoked a dated depressive transition (van de Leemput 2014 PNAS) | Human dated transition; tests cycling-collapse against a *known onset date*. Reports *directional asymmetry* (neg-affect indicators before worsening, pos before improvement) |
| **CHB-MIT Scalp EEG** | <https://physionet.org/content/chbmit/1.0.0/> | ~916 h, **per-second seizure onset/offset annotations** (198 seizures) | Continuous, long, timestamped → rolling-window DFA-α; test over-correlation pole as seizure approaches (preictal) |
| **Sudden Cardiac Death Holter (sddb)** | <https://physionet.org/content/sddb/1.0.0/> | 23 Holter ECGs with **recorded terminal arrhythmia** (dated catastrophic collapse) | Does cycling-amplitude collapse precede a real time-stamped physiological collapse — and toward which pole (VF fragmentation vs over-regularization)? |
| **Bonn EEG epilepsy (Andrzejak 2001)** | mirror: <https://www.ujet.cl/wp-content/uploads/2019/05/datasets-bonn-university.html> (canonical host frequently down) | 5 labelled sets healthy / interictal / ictal | Static DFA-α contrasts (segments too short for rolling windows) |
| **Stock-crash indices (DJIA/S&P/NASDAQ/DAX/FTSE)** | paper: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4711996/>; daily closes free via FRED/Stooq/Yahoo | Diks, Hommes & Wang 2019: **NO critical slowing down** before 1929/1987/2000/2008, yet rising variance + low-freq power flagged them | Second *differentiating* case where AR(1) fails but a structure/amplitude signal succeeds |

### Tier-1 benchmark/comparator data

| Dataset | URL | Use |
|---|---|---|
| **`earlywarnings` R toolbox + bundled series** | <https://www.early-warning-signals.org/> · <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0041010> | Simulated fold/transcritical/**Hopf** series with KNOWN tips + reference AR1/variance/DFA outputs. Benchmark cycling-collapse head-to-head; **show it fires where CSD points the wrong way (Hopf / oscillation death)** |
| **Dakos 2008 paleoclimate proxies (8 dated abrupt shifts)** | <https://www.pnas.org/doi/10.1073/pnas.0802430105> · proxies on NOAA Paleo / PANGAEA | Canonical *one-pole "their best case"* benchmark |
| **HadISST SST (AMOC EWS source)** | <https://www.metoffice.gov.uk/hadobs/hadisst/> | Boers 2021 computed restoring-rate λ on sliding windows here; also where the **volume/coverage confound** was contested — stress-tests both the recovery-rate fix *and* the sampling-confound control |

---

## §3 — Pre-registration-ready operationalization (the next pilot)

**Goal:** test whether **symmetric loss-of-cycling beats one-pole CSD as an early-warning signal**, on a named ground-truth dataset, with a pre-committed falsifier. This is the experiment that converts the §1 "candidate" into either a Tier-1 result or a dead branch.

> **Pre-registration discipline import (Tier 1):** Boettiger & Hastings 2012 (*J. R. Soc. Interface* 9:2527, <https://pmc.ncbi.nlm.nih.gov/articles/PMC3427498/>) — evaluate with **ROC/AUC** (sensitivity vs false-alarm), and beware the **prosecutor's fallacy** (conditioning only on systems known to transition inflates apparent skill). Therefore: **negative controls are mandatory.**

### Primary pre-registration (Cascade paired-lake — the clean positive+control)

- **Data:** EDI `knb-lter-ntl.355.6`. **Peter Lake** = manipulated (KNOWN dated transition). **Paul Lake** = reference (KNOWN no-transition). Same variables, same seasons, same instrument.
- **Indicators (computed identically, rolling window):**
  1. **Ours:** rolling DFA-α → a **cycling-amplitude** statistic (e.g. rolling SD / peak-to-trough envelope of α over a trailing window; symmetric — penalizes flattening toward *either* pole).
  2. **Incumbent one-pole baseline:** lag-1 AR(1) trend (Kendall-τ), variance trend, *rising* DFA-α trend — via the `earlywarnings` R package (fork it; don't reimplement the baseline).
- **Pre-committed primary hypothesis:** the cycling-amplitude metric **declines significantly in Peter before the documented shift date AND stays flat in Paul**, with **AUC (Peter-vs-Paul discrimination) ≥ that of the best one-pole indicator**.
- **FALSIFIER (pre-committed, the whole point):** *If the cycling-amplitude metric does NOT beat (≥, within a pre-set margin) the best single one-pole indicator on lead time and AUC across the lake pair — OR if it fires in the Paul (control) lake — the "amplitude beats level" claim (§1 claim c) is rejected, and the contribution collapses to the synthesis-bridge alone (§1 claim 1).* The programme must state this downgrade explicitly rather than salvage.
- **Secondary, the differentiating test (where the headline lives):** run the *same* metric on (i) the `earlywarnings` **Hopf / oscillation-death** simulated series and (ii) **Lake Veluwe** (Wang 2012) and (iii) a basket of **stock crashes** (Diks 2019). **Pre-committed secondary hypothesis:** cycling-amplitude collapse fires on these while AR(1) does **not** (these are the documented one-pole failures). If it fires where AR(1) is *known* to fail, that is the strongest "we refine EWS" evidence available.

### Why this is the right first pilot (not PhysioNet first)

PhysioNet replicates Goldberger's *static* two-pole separation (expected to succeed, but proves only what's already known). Cascade is the one dataset with a **built-in negative control and a dated transition**, so it isolates the *novel* claim (amplitude-of-cycling as EWS) with the rigor Boettiger-Hastings demand. Run PhysioNet *second*, as the symmetric-pole confirmation: show (i) the two static poles separate classes (replicating Goldberger), THEN (ii) that a rolling cycling-amplitude statistic adds discriminative/early-warning power *over* static α. If (ii) fails on PhysioNet too, the novelty is *only* the bridge — and the framing must say so.

---

## §4 — Method-transfer: fixing the H2b recovery-rate gap and the coupling gap

The synthetic validation established that **recovery-rate-after-shock was NOT measurable on a 365-day rolling window** and a **continuous coupling-to-driver slope was underpowered.** The EWS field has direct, recent, climate-validated fixes for both. (Tier 1 — multiple converging primary sources.)

### H2b — recovery rate on a short window: the field already solved this

The key realization: **"recovery rate" is itself a canonical EWS metric — the programme is not inventing a metric, it just chose the wrong *estimator* (a long rolling window).** Two right estimators:

1. **The AR(1) → λ link (short-segment restoring rate).** For a fold/Langevin system under white noise, AC(τ)=exp(−λτ), so the linearized restoring rate is recovered analytically as **λ = −log(AR1)/dt** from a *single* lag-1 coefficient — **no year-long window required**, just a short high-resolution segment. (Boulton/Lenton/Boers tradition; Boers 2021 *Nat. Clim. Change*, <https://www.nature.com/articles/s41558-021-01097-4>.) ⚠ Note the **known critique**: the Boers λ-trend can ride the observational-coverage/volume trend — *the same volume/sampling confound the synthetic gate already validated as controllable.* Strong talking point: we handle the confound they were criticized on.

2. **THE decisive fix — "Monitoring resilience in bursts"** (Delecroix, van Nes, Scheffer & van de Leemput 2024, *PNAS*; <https://www.pnas.org/doi/10.1073/pnas.2407148121>, full text <https://pmc.ncbi.nlm.nih.gov/articles/PMC11295040/>). Instead of one long window, take **multiple short high-resolution "bursts,"** compute lag-1 AC + variance *within* each burst, then test the trend *across* bursts with **Theil-Sen regression + a sieve-bootstrap** significance test. With the *same total sample budget*, bursts **beat** the moving-window estimator (especially for autocorrelation) and **explicitly target systems "hard to measure continuously"** — i.e. exactly the 365-day-window failure mode.

**What NOT to use (pre-committed):** van Kan, Jegminat & Donges 2021 (arXiv:2112.03260, <https://arxiv.org/abs/2112.03260>) estimates basin stability from observed perturbations but needs **O(100–1000) perturbation-recovery events** and long series, and degrades near the bifurcation. Cite only as the approach *not* to use for a short window.

> **H2b action:** redefine recovery as the **burst-local AR1→λ restoring rate**; replace the single rolling window with a **burst design + Theil-Sen / sieve-bootstrap**. External corroboration that single-pole CSD/recovery metrics are *underpowered on behavioural data* (so a different diagnostic is warranted): Smit et al. 2025 (*Clin. Psych. Sci.*, <https://journals.sagepub.com/doi/10.1177/21677026241305136>) — depression-recurrence EWS had ~84% specificity but only **~33% sensitivity.** This echoes the programme's own honest negative finding.

### The coupling gap — directed-causality estimators beat a naive continuous slope

Three concrete, recent, climate-validated options (pick by whether the steer coupling is linear or nonlinear):

| Method | Source | When to use |
|---|---|---|
| **PCMCI+ causal discovery** (tigramite) | Hoegner & Boers et al. 2025, *ERL* 20:074026 — <https://iopscience.iop.org/article/10.1088/1748-9326/addb62> (arXiv <https://arxiv.org/abs/2501.14374>) | **Best steer-link template.** Recovered a directed driver→system link with 2–4 month lags from **only ~40 yrs of monthly data** — directed causality with significance on a *modest record* where a naive slope is underpowered. Use for directed *lagged* links with significance on short records |
| **Causal Network Markers (CNM-GC / CNM-TE)** | Bian et al. 2025, *Adv. Sci.* — <https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202415732> (open: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12622457/>) | Twin EWS markers capturing **directional** influence; CNM-GC (Granger, linear) / **CNM-TE (transfer entropy, nonlinear)**. Use CNM-TE if steer coupling is nonlinear |
| **Closed-form Jacobian reconstruction** | Barter, Brett & Gross 2020/21, *Proc. R. Soc. A* 477 — <https://royalsocietypublishing.org/doi/10.1098/rspa.2020.0742> (arXiv <https://arxiv.org/pdf/1910.09698>) | Reads the **off-diagonal coupling coefficient + leading eigenvalue** directly from noise responses, rather than via a regression slope |

> **Coupling action:** replace the continuous coupling-slope with **PCMCI+** (linear/lagged, short-record) or **CNM-TE** (nonlinear). Reference programmatic bridge: Scheffer et al. 2018 *PNAS* (<https://www.pnas.org/doi/10.1073/pnas.1810630115>) articulates the recovery-rate ideal *and its data demands* — explaining *why* the rolling-window version was underpowered.

---

## §5 — Outreach targets (people / groups)

Tier 1 = direct authors of the methods/datasets above; natural reviewers and collaborators.

**Critical-transitions / EWS canon**
- **Vasilis Dakos** (CNRS / ISEM, Montpellier) — lead of both EWS *methods* papers + the 2024 review; maintainer-lineage of the `earlywarnings` R package. **Most likely reviewer.** <https://www.vasilisdakos.info/>
- **Marten Scheffer / Egbert van Nes / Ingrid van de Leemput** (Wageningen) — EWS canon + the **bursts** method (the H2b fix) + `generic_ews`/`spatial_ews` tools. Right audience for "symmetric two-pole loss-of-cycling." Route via corresponding-author emails on the 2024 PNAS bursts paper.
- **Tim Lenton + Chris Boulton / Paul Ritchie / Mark Williamson** (Global Systems Institute / **AdvanTip**, Exeter) — run the **DFA-rolling-window EWS pipeline the programme refines**; ARIA-funded early-warning programme. Ideal for the "we refine your one-pole DFA-EWS into a symmetric amplitude-collapse metric" pitch. <https://sites.exeter.ac.uk/advantip/meet-the-team/>
- **Niklas Boers** (TU Munich + PIK) — owner of the **restoring-rate λ** EWS *and* the **PCMCI+ causal-coupling** work → the right contact for *both* gap-fixes; also the natural person to discuss the shared volume/coverage confound. <https://www.pik-potsdam.de/members/boers>

**Physiology / decomplexification (to ground the symmetric claim empirically)**
- **Ary Goldberger, C.-K. Peng, Madalena Costa** (Beth Israel Deaconess / Harvard; PhysioNet lineage) — own the symmetric two-pole DFA complexity-loss framing on real physiological data.
- **Plamen Ivanov** (Boston U, "network physiology") — to co-locate "loss of cycling" in network-physiology language.

**Social-substrate / event-stream adjacents** (see §6)
- **Dan Braha** (NECSI / UMass Dartmouth) — civil-unrest phase transitions on event data; *most natural co-author or critic* for the GDELT application.
- **Thomas Bury** (McGill) — deep-learning EWS, incl. a 2025 paper that already touches "sociology."
- **James R. Watson** (Oregon State / The Prediction Lab) — the critical-*speeding-up* (two-pole) author.
- **Merlijn Olthof / Marieke Wichers** — bidirectional / transdiagnostic EWS in psychopathology.

> **Framing guardrail for ALL outreach (Tier 1 risk):** lead with **"amplitude-of-cycling collapse,"** explicitly distinguish from level-based CSD, and acknowledge that EWS are known to be **direction-dependent / CSD acts only along the dominant eigenvector** — so reviewers don't dismiss it as relabelled critical slowing down.

---

## §6 — How this maps to the framework

Grounded in the programme's own internal docs (`operator_os_v0_2/readings/claude_branch_audit_v0_2_5_5pro.md`):

- **Cont 13** treats **A⁺/A⁻ as symmetric latent dimensions with charge algebra** — "*symmetry exists in the field, asymmetry exists in the compiler*" (A⁺ generates, A⁻ viability-checks; only A⁺ structures surviving A⁻ become canon).
- The **viability band** is the framework's "*do not freeze / do not explode*" kernel (mapped to Wolfram's four computational classes — substrate must be *run*, not solved).

### The mapping (with Tier tags)

| Framework element | EWS/physiology correlate | Tier |
|---|---|---|
| **A⁺ (variety generation / exploration)** ↔ **A⁻ (pruning / consolidation)** | Holling adaptive cycle **r ↔ K**; exploration↔consolidation | **Tier 2** (conceptual prior art exists — Panarchy/Holling — but not via rolling DFA-α) |
| **Cont-13 symmetry of A⁺/A⁻** | Goldberger 2002 symmetric two-pole α ("excessive order…or uncorrelated randomness") | **Tier 1** — the symmetry is *established*, not speculative. This is reassuring for internal consistency but means the programme cannot claim it as novel |
| **Viability band ("don't freeze / don't explode")** | Healthy 1/f / α≈1 *between* over-correlation (α≫1, "freeze") and whiteness (α≈0.5, "explode/fragment") | **Tier 1** for the band's existence (Goldberger; brain-criticality "distance to criticality"); **Tier 2** that the band is the *right* health construct for *this* substrate |
| **Cycling pre-registration** (the programme's #172 blind workflow; cycling-amplitude-collapse as the diagnostic) | **No prior art found operationalized** — this is the candidate | **Tier 2** — the genuine open seam; must survive the §3 falsifier to graduate |
| **Synthetic-validation results** (recovery-rate not measurable on 365 d; coupling-slope underpowered) | Resolved by bursts (Delecroix 2024) + PCMCI+/CNM-TE (§4); independently corroborated by Smit 2025 low-sensitivity finding | **Tier 1** (the fixes are established methods) |

### The asymmetry the framework already encodes — and what it predicts

Cont-13's "*symmetry in the field, asymmetry in the compiler*" is a **non-trivial prediction** that the EWS field has *not* made: the *failure* (loss of cycling) is symmetric (either pole), but the *process* (A⁺ generate → A⁻ check) is directional. This is the programme's most defensible conceptual asset — it is the bridge claim (§1.1) restated in the framework's native language, and it predicts that a *symmetric* amplitude metric should dominate the *asymmetric* one-pole CSD indicators precisely on the cases where CSD is known to fail (Hopf, Lake Veluwe, stock crashes — §3 secondary). **This is testable and is the falsifiable core.**

### Has the social-substrate application been scooped? (Tier 1/2)

**Partially, on a narrower basis than the framework's full claim — but the specific combination is unoccupied.**
- **CSD on discourse/sentiment is ~13 years old but shallow:** MITRE 2012, "Early Warning Signals of Tipping-Points in Blog Posts" (<https://www.mitre.org/sites/default/files/pdf/12_4711.pdf>) ran CSD on blog *sentiment* before two protest tipping-points. One-pole, two hand-picked cases, no DFA, no cycling. *(Author attribution unverified — PDF returned HTTP 403; existence/method/date confirmed via MITRE pub page + snippets.)*
- **Closest event-stream work = Braha 2024**, "Phase transitions of civil unrest across countries and time" (*npj Complexity*; <https://www.nature.com/articles/s44260-024-00001-3>, arXiv:2306.08698). Models unrest in 170 countries as **recurrent low↔high phase shifts** via HMM, explicitly invokes **SOC, 1/f noise, "oscillating patterns of political instability"** — the single biggest overlap with "capacity to cycle." **CRUCIAL GAP (verified via local pdftotext, overriding a misleading WebFetch summary):** Braha **does NOT compute EWS empirically** — he *explicitly defers* "is there a discernible increase in autocorrelation or variance as society approaches a phase transition" to **future work needing day-scale data**; uses HMM not DFA; one-directional; no cycling-amplitude collapse. **The programme picks up exactly where Braha stopped.**
- **The broader GDELT-unrest field is essentially empty of EWS:** the SBP-BRiMS 2025 review of 48 studies (<https://sbp-brims.org/2025/papers/working-papers/2025_SBP-BRiMS_paper_12.pdf>) contains **NO** critical-slowing-down, **NO** DFA/spectral exponent, **NO** regime-cycling-capacity — in its methods *or* its 8 stated research gaps. Nearest cousin: relative-entropy / correlation-breakdown precursors to the Arab Spring ("Gao et al.", ref [27] — *re-verify before citing*).
- **NET:** "EWS on discourse" is taken; "EWS on GDELT-style streams" is sparsely taken (info-theoretic anomalies, ML classifiers, HMM phase models). But **rolling DFA-α measuring the capacity to cycle, with cycling-amplitude collapse as a symmetric two-pole failure diagnostic on event streams, appears UNOCCUPIED.** The differentiation rests on **(a) cycling-amplitude collapse + (b) DFA-α on event streams + (c) the cont-13 symmetry framing applied to GDELT** — *not* on "failure is two-directional" (prior art: critical speeding up; bidirectional psychopathology EWS).
- **Substrate data already in hand (Tier 1):** GDELT v2 country-day 2015–2026 is ingested (programme task #1). Ground-truth/validation partners: ACLED (<https://acleddata.com/>), ICEWS (<https://dataverse.harvard.edu/dataverse/icews>).
- **Anticipated objection (Tier 2):** in social systems, adaptive/anticipatory agents can trigger *self-fulfilling* transitions, so CSD assumptions may not hold cleanly (the "smart-agent" critique from financial-EWS, Diks 2019). Argue *why* a cycling-*capacity* measure is more robust to this than approach-to-bifurcation CSD.

---

## §7 — Sources (all URLs collected)

**Symmetric two-pole / decomplexification prior art**
- Goldberger et al. 2002, *PNAS* — <https://pmc.ncbi.nlm.nih.gov/articles/PMC128562/> *(symmetric-claim quote verified verbatim; pnas.org DOI 403'd)*
- Lipsitz & Goldberger 1992, *JAMA* — <https://pubmed.ncbi.nlm.nih.gov/1482430/>
- Vaillancourt & Newell 2002, *Neurobiol. Aging* — <https://pubmed.ncbi.nlm.nih.gov/11755010/>
- Costa, Goldberger & Peng 2005, *Phys. Rev. E* (MSE) — <https://link.aps.org/doi/10.1103/PhysRevE.71.021906>
- Iyengar/Peng/Goldberger/Lipsitz 1996, *Am. J. Physiol.* (Fantasia basis) — <https://arxiv.org/pdf/0712.1380>
- Hesse & Gross 2014, *Front. Syst. Neurosci.* (brain criticality / distance-to-criticality) — <https://pmc.ncbi.nlm.nih.gov/articles/PMC4171833/>

**EWS / critical-transitions canon (one-pole baseline)**
- Scheffer et al. 2009, *Nature* — <https://www.nature.com/articles/nature08227>
- Dakos et al. 2012, *PLoS ONE* (methods + toolbox) — <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0041010> · <https://pmc.ncbi.nlm.nih.gov/articles/PMC3398887/>
- Lenton, Livina, Dakos, van Nes & Scheffer 2012, *Phil. Trans. R. Soc. A* — <https://pmc.ncbi.nlm.nih.gov/articles/PMC3261433/>
- Dakos et al. 2024, *Earth System Dynamics* (review; DFA = 1 line, no Goldberger) — <https://esd.copernicus.org/articles/15/1117/2024/>
- Scheffer, Carpenter, Dakos & van Nes 2015, *Annu. Rev. Ecol. Evol. Syst.* — <https://research.wur.nl/en/publications/generic-indicators-of-ecological-resilience-inferring-the-chance->
- Dakos 2008 paleoclimate, *PNAS* — <https://www.pnas.org/doi/10.1073/pnas.0802430105>
- Early Warning Signals Toolbox (rolling DFA-α + Kendall-τ) — <https://www.early-warning-signals.org/> · DFA page <https://www.early-warning-signals.org/?page_id=113>

**Two-pole / direction-dependent EWS (the honesty caveats)**
- Titus, Gelbaum & Watson 2019, "Critical speeding up", arXiv:1901.08084 — <https://arxiv.org/abs/1901.08084>
- Smit et al. 2025, *Clin. Psych. Sci.* (low-sensitivity depression EWS) — <https://journals.sagepub.com/doi/10.1177/21677026241305136>
- van de Leemput et al. 2014, *PNAS* (depression onset/termination; directional) — <https://www.pnas.org/doi/10.1073/pnas.1312114110>

**Ground-truth datasets**
- Cascade / Peter-Paul Lakes (EDI) — <https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-ntl.355.6> · API <https://pasta.lternet.edu/package/eml/knb-lter-ntl/355> · Carpenter 2011 *Science* <https://www.caryinstitute.org/sites/default/files/public/reprints/Carpenter_et_al_2011_Science.pdf>
- PhysioNet — <https://physionet.org/> · nsr2db <https://physionet.org/content/nsr2db/1.0.0/> · chf2db <https://physionet.org/content/chf2db/1.0.0/> · fantasia <https://physionet.org/content/fantasia/1.0.0/> · chbmit <https://physionet.org/content/chbmit/1.0.0/> · sddb <https://physionet.org/content/sddb/1.0.0/>
- Lake Veluwe flickering — Wang et al. 2012 *Nature* <https://www.nature.com/articles/nature11655> · <https://pubmed.ncbi.nlm.nih.gov/23160492/>
- Depression ESM — data <https://osf.io/j4fg8> · paper <https://openpsychologydata.metajnl.com/articles/10.5334/jopd.29/>
- Bonn EEG (mirror) — <https://www.ujet.cl/wp-content/uploads/2019/05/datasets-bonn-university.html>
- Stock crashes / no-CSD — Diks, Hommes & Wang 2019 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4711996/>
- HadISST — <https://www.metoffice.gov.uk/hadobs/hadisst/> · ERA5 — <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means>

**Method-transfer (H2b recovery + coupling)**
- Delecroix et al. 2024, "Monitoring resilience in bursts", *PNAS* — <https://www.pnas.org/doi/10.1073/pnas.2407148121> · <https://pmc.ncbi.nlm.nih.gov/articles/PMC11295040/>
- Boers 2021, AMOC EWS, *Nat. Clim. Change* — <https://www.nature.com/articles/s41558-021-01097-4>
- van Kan, Jegminat & Donges 2021 (what NOT to use), arXiv:2112.03260 — <https://arxiv.org/abs/2112.03260>
- Hoegner & Boers et al. 2025, PCMCI+ AMOC→Amazon, *ERL* — <https://iopscience.iop.org/article/10.1088/1748-9326/addb62> · <https://arxiv.org/abs/2501.14374>
- Bian et al. 2025, Causal Network Markers, *Adv. Sci.* — <https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202415732> · <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12622457/>
- Barter, Brett & Gross 2020/21, Jacobian reconstruction, *Proc. R. Soc. A* — <https://royalsocietypublishing.org/doi/10.1098/rspa.2020.0742> · <https://arxiv.org/pdf/1910.09698>
- Scheffer et al. 2018, "Quantifying resilience of humans…", *PNAS* — <https://www.pnas.org/doi/10.1073/pnas.1810630115>

**Evaluation rigor**
- Boettiger & Hastings 2012, limits/ROC + prosecutor's fallacy, *J. R. Soc. Interface* — <https://pmc.ncbi.nlm.nih.gov/articles/PMC3427498/>

**Social-substrate / event-stream**
- Braha 2024, *npj Complexity* — <https://www.nature.com/articles/s44260-024-00001-3> · arXiv <https://arxiv.org/abs/2306.08698>
- SBP-BRiMS 2025 GDELT review (48 studies) — <https://sbp-brims.org/2025/papers/working-papers/2025_SBP-BRiMS_paper_12.pdf>
- MITRE 2012 blog-posts CSD *(author unverified, 403)* — <https://www.mitre.org/sites/default/files/pdf/12_4711.pdf>
- Bury et al. 2021, deep-learning EWS, *PNAS* — <https://www.pnas.org/doi/10.1073/pnas.2106140118>
- Bury 2025, surrogate-trained ML EWS, *Comm. Physics* — <https://www.nature.com/articles/s42005-025-02172-4>
- GDELT — <https://www.gdeltproject.org/> · ACLED — <https://acleddata.com/> · ICEWS — <https://dataverse.harvard.edu/dataverse/icews>
- Info-theoretic GDELT precursor ("Gao et al.", *re-verify*) — <https://www.researchgate.net/publication/326255306_Predicting_Social_Unrest_Using_GDELT>

**Conceptual framing**
- Holling adaptive cycle / Panarchy — <https://www.resalliance.org/adaptive-cycle>

**Adjacent live threads to watch (loss-of-oscillation EWS)** — Tier 3, cite to show awareness: "Echoes Before Collapse: Deep Learning Detection of Flickering" (arXiv:2509.04683); EWS-for-oscillatory-instability / desynchronization (arXiv:2003.11595).

---

### Provenance & honesty notes
- Web access was confirmed working by all four scouts in June 2026; the great majority of URLs were live-fetched or returned by live search.
- **Verified-verbatim:** the Goldberger 2002 symmetric-claim sentence (via open PMC mirror PMC128562) — *not* recalled from memory.
- **Flagged-unverified:** MITRE 2012 author attribution (PDF 403); the "Gao et al." GDELT info-theoretic precursor (surfaced via review reference list, primary PDF not fetched). Re-verify both before any citation.
- **WebFetch correction on record:** WebFetch's summary of Braha 2024 falsely reported "no EWS/cycling content" because the PDF used compressed streams; a *local pdftotext* extraction overrides that — Braha *does* discuss recurrent phases, SOC, 1/f, oscillating instability, and explicitly defers empirical AC/variance EWS to future work.
- This is a **scout for steer, not a canon document.** Carry as a speculative scout, not as promoted candidate. The §3 falsifier is the gate that would graduate claim (c) from Tier 2.
