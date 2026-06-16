# The Keyhole Block Universe (v0.4 canonical synthesis)

**Date:** 2026-06-15 | **Status:** Tier-3 design. NOT built. Extends [SPEC.md](SPEC.md), [SCOPE_NESTING_LOD.md](SCOPE_NESTING_LOD.md), [WRAPPER_PROBE_OBSERVER.md](WRAPPER_PROBE_OBSERVER.md).

Consolidates a four-workflow Opus batch + a codex/gemini cross-pass on Pav's keyhole/block-universe expansion. Detailed resolved analyses: [K1_block_universe.md](K1_block_universe.md), [K2_tomography.md](K2_tomography.md), [K3_observation_to_knowledge.md](K3_observation_to_knowledge.md), [K4_democracy_keyhole.md](K4_democracy_keyhole.md); external takes: [keyhole_block_codex_take.md](keyhole_block_codex_take.md), [keyhole_block_gemini_take.md](keyhole_block_gemini_take.md); brief: [keyhole_block_brief.txt](keyhole_block_brief.txt).

**Verdict (CORRECTED 2026-06-15 after a codex + gemini audit - see AUDIT CORRECTIONS below).** ~~it is real machinery, not metaphor; Pav's expansion maps almost one-to-one onto current named work~~ - that was **over-claimed.** Honest verdict: this is a **coherent architecture built on named analogies**, not validated machinery. The expansion *resonates* with current work (information-eternalism, crystallizing block universe, DBSP/CALM, Radon/Fourier-slice, algorithmic-statistics structure functions, Bayesian experimental design, truth-maintenance) - but those are **analogy / implementation-inspiration, not one-to-one mechanism**, and the load-bearing quantity `measured_bits` is **undefined for latent constructs**, which gates everything downstream. One physical-axis claim was tested and passed (the tomography toy, [tests/](tests/)); the latent-axis claims are unvalidated. **Read the AUDIT CORRECTIONS section before relying on any section below.**

---

## AUDIT CORRECTIONS (codex + gemini cross-audit, 2026-06-15)

Two independent external audits ([audit_codex.md](audit_codex.md), [audit_gemini.md](audit_gemini.md)) of this doc + [WRAPPER_PROBE_OBSERVER.md](WRAPPER_PROBE_OBSERVER.md) **converged** on one verdict: the spec **repeatedly promotes analogies into mechanisms, on top of an undefined measurement model.** These corrections SUPERSEDE the over-claims in the sections below (demote-not-kill: the original text stays as the dated record; this section governs).

**THE LOAD-BEARING HOLE (both audits, #1): `measured_bits` is undefined for latent constructs.** Without a real measurement model - a coding scheme, a unit scale, an estimator, an uncertainty interval, a source-dependency model, and per-axis calibration - `measured_bits` on the WHAT/WHO/WHY axes is **just a badge.** And if it is a badge, the COIN cannot be enforced, the tomography does not apply, EIG is not meaningful, and conceal/expose cannot be audited. **Everything below is contingent on closing this gap.** (The pinned-coder MDL harness covers the physical/text axes; the latent/semantic axes are uncalibrated. Defining the latent measurement model is THE prerequisite, and is now the next work item.)

**Corrections, by theme:**

*Honesty law (R-A) - TWO invariants; conceal is NOT "as honest as expose".*
- The single coherent law is **"never render generated content AS measured"** (a provenance invariant that holds at every dial setting) - which is **weaker** than the EXPOSE cap "never render a fake bit" (`rendered <= measured`, expose pole only). Stop saying conceal obeys the same COIN. [supersedes sec 0 + Doc2's absolute "never render a fake measured bit"]
- The viewer-internal invariant (queryable substrate + disclosed dial + reversible) is **insufficient**: a seamless render is processed as real regardless of a UI badge, and reversibility is meaningless once a frame is screenshotted/exported/cited. CONCEAL needs an **out-of-viewer threat model**: a **non-removable perceptual watermark** on generated bits, a signed provenance ledger, and a measured-vs-generated sidecar that survives export (cf. C2PA). Full-conceal (no watermark) is honest ONLY for a frame **declared entirely fiction**. [PAV DECISION pending: watermark floor vs declared-fiction full-conceal]

*Compiler - separate append-only EVIDENCE from non-monotonic DERIVED BELIEF.*
- "Confidence only goes up / measured_bits is an up-only lattice" is **wrong**: evidence VOLUME is monotone, CONFIDENCE in a claim can go DOWN. CALM order-free convergence applies only to **monotone event ingestion** (append-only evidence with **event-ID dedup** - raw Z-set +1 deltas are NOT idempotent without it); derived credence is **non-monotonic**, ordered by the bitemporal `tau` clock (retractions are not CALM-safe). [supersedes sec 2]
- "Every rendered bit traces to the log => a fake measured bit is structurally impossible" is **false**: traceability catches MISSING provenance, not bad labels, bad/copied sources, ingestion bugs, or generated content mis-tagged measured. Needs an ingestion/adversarial failure-mode list. [supersedes sec 2]

*Tomography - it is an INVERSE PROBLEM; Radon/Fourier-slice only where projections are linear and known.*
- Keyhole/spreading-activation is **not** a Radon projection unless the probe `P_i` is a known linear operator. Radon/Fourier-slice + compressed-sensing apply on the **physical WHERE/WHEN axes** (the only place the passing test exercised them); on WHAT/WHO/WHY use a **discrete graph-coverage** inverse-problem analog, not Fourier. [supersedes sec 3 latent claims]
- Precision: `m ~ s` needs sparsity-basis + incoherence + noise + log factors; conditional MI is submodular only under adaptive-submodularity/conditional-independence; Cramer-Rao is `SE ~ 1/sqrt(m)`; **"gaps blur never streak" is false** - limited-angle artifacts ARE directional streaks, and low-pass/TV is a **prior**, not a guaranteed lower bound. [supersedes sec 3/4]

*Drift (R-B) - an ALIGNMENT / IDENTIFIABILITY problem, not a Lipschitz one.*
- A basis rotation may be no semantic change (pure gauge), an unaligned rotation that merely LOOKS like drift, or a real basis change that alters the measurement operator. The fix needs **anchor entities + an explicit inter-slice transport/alignment map + uncertainty over that map + an invariant metric.** **Without anchors a gap-slice is UNDERIDENTIFIED, not merely blurry**; a paradigm shift where the transport map breaks is a **rendered rift**, not an interpolated blur. [supersedes sec 9 Lipschitz framing; reconciles "reframed as solved" vs "still open": drift within an aligned basis is handled by the 4D stack, basis-change/alignment is the open problem]

*Objective - valence is NOT EIG.*
- The next-burst objective is **expected utility / cost**, of which EIG is **one term**; "the fuzzy region IS argmax-EIG" is false (high uncertainty can be irrelevant, unmeasurable, costly, or low-utility). **Valence (R3) is the signed sentiment field (+/- lobes)** - a different quantity from the unsigned EIG. [supersedes sec 7 "valence := EIG"]

*Scope softenings.*
- **WHOM is BOTH a content role** (recipient/victim/beneficiary/audience) **and the observer role** - do not collapse it to observer-only (corrects WRAPPER_PROBE_OBSERVER sec 1.1). Stigler's law is a **heuristic prior** (widens WHO-blur), not a cap. Covariance-Intersection is for continuous/physical fusion, not discrete semantic DAGs. The structure-function "kink = knowledge" is incomputable (MDL is a proxy); derivation entropy is a retrieve-vs-compute proposal, not a truth gate; epiplexity is relevant but not a settled criterion; "5W1H is near-optimal" is too strong. Bitemporal "across time" must be split into three senses: posterior update vs definition-conditioned view vs real causal attention events.

*What SURVIVES the audit:* the block-as-target + bitemporal clocks; keyhole = spreading activation (as RETRIEVAL, not tomography); the conjecture-stub as a typed falsifiable hole; the constellation correction; and the **physical-axis fidelity law**, which the 10/10 settling tests confirm on a Euclidean toy. The architecture is sound; the over-claims and the undefined latent measurement model are the debt.

**Honest next step:** define the latent measurement model (the load-bearing hole) before hardening anything downstream. -> **RATIFIED + TESTED CLOSURE (2026-06-15; 11/12 falsifier checks pass, coder-robust)** ([latent_measurement_candidates.md](latent_measurement_candidates.md); workflow + codex + gemini converged): `measured_bits(W) = min(cost_ub, evidence_lcb)`, where `cost_ub` = **prequential codelength under a pinned coder** (a sound one-sided upper bound, the *same* unit as physical bits) and `evidence_lcb` = a **dependency-corrected lower bound on independent supporting evidence** (ablation/holdout gain; conditional codelength makes redundant sources add ~0 bits). Four of Pav's six dials collapse to one codelength family (absolute / normalized / kernel-residual / ablation); connectivity + zoo are diagnostics, not bounds; there is no intrinsic latent measure (the *pinned relational bit*). NEXT: prototype it and run the holdout-calibration falsifier.

---

## 0. The COIN is a DIAL: expose <-> conceal (Pav reframe, 2026-06-15)

The COIN was stated as an absolute - "never render a fake measured bit." Pav's correction: that is **one pole of a dial**, not the whole law. The honesty rule has two ends, and the instrument should expose the dial:

- **EXPOSE pole (forensic, the default):** `rendered_sharpness(x) <= measured_bits(x)` everywhere; every unmeasured or generated region is **visibly** blurred or stubbed; the seam is the product; maximal disclosure. The audit ground-truth, and the COIN as previously written. *"Never render a fake pixel."*
- **CONCEAL pole (generative / immersive):** render a **complete, seamless, plausible whole**; generated bits are made visually indistinguishable from measured ones - *"try to hide all the fakes."* The synthesis render (the generate-face of the derivation-entropy gate turned all the way up).

**The invariant that keeps EVERY setting honest** (what makes a concealing render legitimate, not fraud): the **substrate never lies** - provenance + per-axis `measured_bits` + the measured-vs-generated map stay **queryable and unchanged** at every setting; and **the dial position is always disclosed** ("conceal=0.7; 38% of what you see is inferred"). The dial controls only whether the **render reveals or hides the seam**, never what the **ledger** knows.

> Fraud is not "rendering a generated bit." Fraud is **passing a conceal-pole render off as an expose-pole render** - a seamless synthesis presented as measured fact. With the dial disclosed and the ledger intact, a seamless generative render is as honest as a labelled photo-restoration; without it, even one smoothed gap is a lie.

So the COIN generalizes: `rendered_sharpness <= measured_bits` is the **expose pole**; at conceal>0 the render may exceed measured_bits **visually**, but only by an amount that is (a) disclosed by the dial, (b) drawn from the substrate's flagged generated bits, and (c) **reversible** - turn the dial back to expose and the seams reappear, the audit unchanged. **Reversibility is the proof** (exactly as the chart-dial's reversibility proves it does not mutate the substrate). Mid-dial settings are the working modes: the tomography "measured-first, generate-second, flagged" rule (section 4) is a conceal-low setting; a fully immersive worldline render is conceal-high. This makes the honesty law a first-class **render-intent dial** - `h_honesty in [expose, conceal]` - alongside the shape dial (theta) and scale dial (b), always badged, defaulting to expose.

### 0.1 Pav clarification (2026-06-15): the FACT / ANTI-FACT (mirror) separation

Pav resolves the audit's R-A deepfake worry not by watermarking a blended render but by an **ontological separation**:
- **The conceal dial is the CONTRAST + BRIGHTNESS of the CORE (measured) wrappers** - it dims or brightens the *real* fact-core; it does **NOT** inject or blend generated bits into the measured layer. Turning conceal never makes a fake look measured, because it only ever modulates measured wrappers.
- **Fuzzy, conjectures, and probabilities are the OPPOSITE of wrappers** - **anti-facts** in a **mirror universe**, explicitly **pure fiction** in latent space, living in a **separate mirror layer**, never blended into the fact-core.

So the COIN's two faces become **two ontologically separate spaces**: a **FACT space** (measured wrappers; conceal = its contrast/brightness) and a **MIRROR / ANTI-FACT space** (fuzzy + conjecture + probability; explicitly fictional). **This dissolves the deepfake worry by construction:** a generated bit can never render *as* measured because it lives in the visibly-fiction mirror - **the ontological separation IS the in-viewer watermark.** EXPOSE = both layers shown (fact-core + mirror anti-facts as fiction); CONCEAL = dim the mirror and/or adjust the fact-core contrast; full-conceal-of-the-mirror = only the measured fact-core (the most forensic view); full-fiction = the declared-fiction mode (only the mirror). The dial **never blends the two into an undeclared seamless whole** - which is exactly the move the audit feared. (The audit's export threat-model remains a COMPLEMENT: a screenshot/export can lose the layer distinction, so a signed provenance sidecar + a non-removable marker on exported mirror-layer content stay necessary out-of-viewer.)

---

## 1. The block is the TARGET, not the artifact (and it is bitemporal)

Both externals insisted, and the workflow confirmed: there is the **real block `B*`** (the fixed, unknown referent) and our **estimate `B_hat_tau`** (the posterior). **The system never writes `B*`** — a keyhole only appends an observation and raises `measured_bits` about a coordinate in `B*`. "Imprint the shape into the block" means imprint into our *estimate*.

Published cover (fresh): **Grinbaum's operational eternalism** (arXiv 2512.22879, Dec 2025) - "eternalism applied to INFORMATION rather than geometry," observers secondary, their operational choices crystallize facts = our FRAME-primary / GLASSES-secondary split. **Ellis-Rothman's Crystallizing Block Universe** - the past crystallizes via state-reduction, delayed-choice actualizes the past = our retroactive, definition-relative origin; we adopt it **plus two upgrades**: crystallize along LATENT axes too, and leave **fuzzy + conjecture-stub** where derivation fails instead of freezing.

**Bitemporal substrate (mandatory):** every wrapper carries two clocks -

```
t_event   when the target state/event belongs in the block
t_obs     when a keyhole measured/inferred it (= compiler_time tau)
```

A 2026 burst measuring a 1790 latent state **decreases the blur at `B_hat(...,1790)` without changing 1790** - it changes the estimate, not the past. Render law: **every view must answer "what did the system know as of `tau`?"** No `as_of_tau`, no honesty (prior art: Datomic, event-sourcing). This is the formal meaning of "observation across time."

---

## 2. The compiler: a monotone, order-free, audit-complete merge

The fact-log compiles into the block as a **stream of deltas** (DBSP/Feldera, VLDB'23): each wrapper is a Z-set delta (+1 assert / -1 retract), the block is their integral, recompile = differentiate->reapply. Its **chain-rule theorem** proves compile-per-axis-then-compose is **bit-identical** to from-scratch - exactly our per-channel COIN composition. Corrections are negative-weight wrappers, so **the log stays append-only**.

**The compile is a join-semilattice MERGE** (CALM theorem): associative + commutative + **idempotent**, so keyhole bursts fire in **any temporal order and still converge with no coordination** (the tomographic multi-exposure model), and recompile-twice = same-block (`recheck=0`, raised to a law). The hazard CALM names: anything that *retracts* or picks "latest-wins" is non-monotonic and breaks order-free convergence. **The fix is load-bearing:**

> Encode `measured_bits` / confidence as a lattice that only goes **UP**. A fuzzy stub is the lattice **bottom**; conjectures can only sharpen it, never un-sharpen. "Meaning -> knowledge as the block compiles" becomes a **monotone climb up a lattice**, and the COIN (never render a fake measured bit) becomes an **invariant**, not a hope.

The block is a **materialized view over the event-sourced log** - derived, ephemeral, fully rebuildable by replay - so **every rendered bit must trace to a log event; a fake measured bit is structurally impossible to introduce undetected** (+ snapshots + compaction for bounded replay; content-hash memoization for incremental recompute). The retrieve-vs-generate gate itself has a name now: **derivation entropy** (Xu-Li 2511.19156), a thermodynamic phase transition = the COIN's sharp=replay / fuzzy=generate.

The existing `compile_substrate.py` is ~80% of this compiler.

---

## 3. Multi-keyhole tomography and the fidelity law

Each keyhole-burst is a **projection** of the latent construct field: `y_i = P_i F + noise`. Reconstructing `F` from many bursts (across concept-angles AND time) is **computed tomography** (Radon transform / Fourier-slice theorem): a burst's 1-D Fourier transform is **a slice through the construct's N-D Fourier transform**, so **`measured_bits` = the volume of frequency space the slices fill.** Views don't *average* - they **intersect**, each one a constraint collapsing the ambiguity volume (3DGS view-consistency / burst super-resolution / synthetic aperture / compressed sensing, four framings of one mechanism).

**The fidelity law (rigorous):**

- **Sample complexity:** to reconstruct a construct of sparsity/description-length `s` you need on the order of `s` independent projection angles (`m >~ s`). Fidelity scales with the bursts needed to cover the construct's description-length - never fewer.
- **The accrual is MARGINAL information, not count:** `delta I(burst | already_observed)` = conditional mutual information, which is **submodular** (diminishing returns is a theorem). An independent concept-angle adds a large positive delta; **a redundant re-fire adds ~0 automatically.** Crediting redundant bursts additively *fabricates* measured_bits = a COIN violation.
- **Diversity beats density:** wide coverage from many *distinct* concept-angles sharpens far more than repeated similar probes (a few well-spread independent angles >> many redundant ones). Score each burst by the **new** bits it contributes (a coverage / condition-number over concept-angles and time-points), not by tally.
- **Independence = unpredictability:** a burst is informative exactly when its outcome is **unpredictable from the current block** (maximum-entropy sampling). "Corroborated > pending" must mean corroborated **by an independent route**; same-route repeats are *pending*, not corroborated. When two bursts may share an upstream source, fuse with **Covariance-Intersection** (consistent for any correlation), never sum - naive independence-assuming fusion is provably overconfident. (This is the formal version of codex's "ten newspapers copying one wire story are one projection with ten echoes.")
- **Two regimes + a hard floor:** fidelity climbs as a power law in #independent-bursts (Cramer-Rao, `error ~ m^-1`), then **saturates past a knee** (extra views only suppress noise). Below an **error floor** set by the measurement operator + noise, **no amount of data or generation improves fidelity** - the floor is the formal statement of "never render a fake measured bit." The reconstruction **locks** when `KL(B_hat_{tau+1} || B_hat_tau) < epsilon`, `measured_bits >= threshold`, and no high-impact alternative remains within `delta`.

Reference architecture that already implements this: **FisherRF -> ActiveGS / Opt3DGS** (each view = a burst, the accumulated Fisher matrix = the block's information content, per-pixel Fisher = a measured_bits/blur map, views scored conditioned on the accumulated matrix so well-covered regions score ~0).

---

## 4. Honest fuzz: the missing wedge, generate-second, and a runtime audit

- **The missing wedge = where to stub.** Unprobed directions produce **direction-specific blur** (streaking/elongation along exactly the angles never probed; sampled directions stay sharp). This is the geometric source of the block's fuzzy regions, and it tells you precisely **where to attach conjecture-stubs.** Formal triggers for "this region provably cannot be sharpened yet": Tuy's data-sufficiency condition, the RIP/incoherence, viewing-angle diversity.
- **Gaps blur, never streak.** Enforce a **bandpass mask + compressed-sensing (L1/total-variation)** so unsampled frequency space is low-passed: `rendered_sharpness = inverse_fourier(sampled frequencies only)` - a mathematically guaranteed *lower* bound.
- **Measured-first, generate-second, flagged.** A generative/diffusion prior *can* fill the missing wedge (the COIN's generate-mode = our conjecture-stub), but **prior-synthesized regions render bits that were never measured**, so they must carry **lower measured_bits / weaker entailment** than directly-probed regions, or the reconstruction lies. Enforce data-consistency on measured bits; let the prior fill only the gaps; flag the fill.
- **The confabulation audit (a runtime COIN check, not just a render cap).** Under-exposed blocks **co-adapt** - they overfit the views they have and fabricate "floaters" in unobserved gaps that look perfect on the observed views but collapse elsewhere. The **observed-vs-novel-view gap** (a held-out-view discrepancy) is a direct, measurable signal that a region is confabulating -> demote it to fuzzy/stub. Hold out keyhole-bursts and check.

---

## 5. Observation -> meaning -> knowledge: three gates

A region becomes knowledge only past **all three** gates (and the gates are **per-axis** - WHAT/WHEN/WHERE/WHO/HOW/WHY each have their own):

1. **Structure gate** - the Kolmogorov **structure-function kink** (the Algorithmic Minimal Sufficient Statistic): "stop here, this is structure." Below it = still extracting meaning; at it = knowledge; **past it = irreducible noise -> render fuzzy.** The computable proxy is the **pinned-coder MDL harness already built** (shortest two-part code). The per-channel honesty test is **Excess Description Length**: a derived WHAT/HOW is real only if it costs *fewer* bits than the noise it explains; cross that and it is overfit = a fake measured bit.
2. **Corroboration gate** - credence crossing a posted level, and only when **independent** keyhole streams pushed it over (corroboration != confirmation; no finite evidence closes a stub to certainty - Popper + Jaynes - which is exactly *demote-not-kill, 0.99-not-Boolean*).
3. **Epiplexity gate** (arXiv 2601.03220, 2026) - for a bounded observer compiling in bursts, knowledge requires structure that is **computationally reachable within the current budget.**

Naming the layers in bits: `observation_bits` (delivered by probes) -> `meaning_bits` (compression gain from a model: `L(M)+L(D|M)`, and meaning is **both discovered and constructed** = the participatory back-reaction) -> `knowledge_bits` (corroborated after adversarial/independent checks). **Knowledge is the lock.** And per DIKW critique (Fricke): the ladder is *not* one-pass bottom-up - a meaning structure must pre-exist for an observation to register, so **knowledge flows back and reshapes how new data is read** (the keyhole only excites what the compiled block can resonate with).

---

## 6. Conjecture-stubs: typed falsifiable holes

A conjecture-stub is **not a weak fact - it is a typed hole**:

```
stub = {
  fuzz_type:   missing_what | missing_how | missing_why | missing_link | missing_actor,
  fail_reason: noise_floor (provably no more bits) | compute_bound (more bits exist, out of reach),
  target_region, triggering_fuzz,
  candidate_hypotheses (mutually exclusive, falsifiable latch-points),
  falsifiers (REQUIRED - no falsifier => it is a note/prior, not a stub),
  required_probe_types,
  current_support_bits,
  EIG (expected information gain if resolved),
  status: conjecture | under_test | corroborated | demoted | retired,
  created_by, t_obs
}
```

Two failure-reasons matter because they are different falsifiable holes: a **noise-floor stub** says "stop probing, there is nothing more here"; a **compute-bound stub** says "more structure exists, aim a probe/compute here." **Render in a different visual grammar from facts** - outline / dithered / interval bounding-box, never a scalar point; **zoom a fact and you get detail, zoom a stub and you get empty space inside its bounds.** Lifecycle is the standing claim-lifecycle (conjecture=parent fn, experiment=child fn, dead-children tally); a stub **must always display its falsifier**, and a demoted claim is a logged dead child, never silently resurfacing.

---

## 7. The unification: a stub's VALENCE *is* its Expected Information Gain

The third coin (valence, R3) and the keyhole-aiming objective turn out to be **the same quantity**. The next burst should fire at the fuzzy region of **maximum EIG** - and that is formally exact: "the fuzzy region IS argmax-EIG." So:

```
valence(stub) := EIG(stub) = E[ H(B_hat) - H(B_hat | y_probe) ]
next_burst    := argmax over stubs of valence / cost     (aim at the most-disagreeing region)
```

Active-learning discipline (so the aiming stays honest): aim at the **observer's question** (prediction-oriented EIG / EPIG = the FRAME-vs-GLASSES split), optimize the **whole burst** not greedily (a contrastive lower bound = the COIN's never-claim-more law), and use a **Wasserstein/MMD** information measure (IPM-BOED, ratio-free) so the selector cannot pretend it measured tail bits. Cheap deployable burst-selector: gradient-embedding magnitude (fuzziness) + k-means++ over directions (diversity) so a burst fires at *many distinct* fuzzy spots, not the same one. **Observation -> meaning -> knowledge = probe (keyhole) -> posterior update (EIG realized) -> entropy drop on the targeted axis -> residual fuzz spawns the next typed stub.** The loop closes.

---

## 8. The constellation correction (from the democracy run)

The democracy keyhole (K4) returned a structural correction that **generalizes to any contested construct**: a latent construct is **not one fuzzy blob - it is a CONSTELLATION of partially-overlapping sub-principle regions**, each lit independently by different sparks, often with a **near-empty intersection**. Democracy's axes: sortition / majority-vote / consensus / rotation+term-limits / commoner-office / women's-power-recall - and **no single spark fills all of them.** The construct's "shape" is this **principle-vector**, so **the single-blob render is itself a measurement artifact to correct.** Render the axes and their (often empty) intersection, not one zone.

This is the live scholarly consensus, not a reframing (Stasavage; Fargher-Blanton; "democracy with adjectives," Collier-Levitsky 1997, 550+ subtypes; the "essentially contested concept," Gallie 1956). The data even behaved as the machinery predicts: V-Dem's 2026 reclassification of the US (liberal -> electoral) is a **live per-axis measured_bits collapse** (the liberal/WHAT layer going fuzzy while the electoral/WHO layer stays sharp) - subtype membership is a definition-relative classification, not a fixed fact. Measurement modality sets the bits (textual/epigraphic sharp; oral-transcribed mid; pure-archaeology institution-measured/procedure-conjecture). Multi-yolk origins are real in the wild (the Peacemaker, the Gadaa originators, Tlaxcallan with no named founder -> fuzzy multi-yolk spikes, not points).

---

## 9. The construct genuinely changes - reconstruct it as a 4D volume (Pav reframe, 2026-06-15)

**The earlier "latent-axis-drift risk" was framed backwards.** Pav: a CT scan *does* change meaning when you scan it over time - and that is not a failure, it is the **nature of the object**. *"We capture slices and derive the volume by stacking them and inferring the gaps."* A latent construct like democracy genuinely drifts (`D(t)`), so its reconstruction is a **4D (time-stacked) volume**, not a static 3D shape we wrongly assumed invariant. The prior art is literal: **4D-CT / dynamic / time-resolved tomography** (medicine scans a *beating heart* by gating and stacking time-slices). So drift is the **time axis of the reconstruction**, not Procrustean noise to suppress.

**What survives as the real residual rule (the COIN on the time axis):** the only dishonest move is **inferring a gap-slice more sharply than the bracketing measured slices justify.** Between two measured time-slices, the inferred middle (the 1900 slice between 1850 and 1950 measurements) must render as a **stub/interval bounded by the construct's maximum rate of change (a Lipschitz bound)** - a blurry region that *contains* the truth - never a sharp interpolated point (presentism). This is "stack the slices, infer the gaps" with the gaps as flagged lower-bit fills (section 4); drift is the signal, over-confident gap-inference is the fault, and it is the same COIN read along `t_event`. (Handling: per-epoch local frames stacked along `t_event`, inter-slice motion *measured* where two slices share entities and *stubbed* where they do not; never assume a single global invariant basis, but never treat the change as failure - it is the 4D content.) Falsifier #1 below tests exactly this.

**Three pre-registered falsifiers:**
1. **Drifting-concept latent tomography** (gemini, runnable today): take historical texts for a contested concept ("Liberty"); keyholes = vector-DB nearest-neighbor searches restricted to time-windows (1800-1850, 1950-2000); reconstruct and render the **1900 slice**. **Honest** = a blurry bounding box that *contains* the true 1900 vector and flags the internal variance as unmeasured. **Broken** = a sharp, wrong *average* of 1850 and 1950 (presentism leak -> metaphor, COIN violated).
2. **Toy hidden-block** (codex): a known ground-truth block hidden from the compiler; generate limited/biased/copied/independent bursts; compare three renderers - A naive-MAP-sharp, B COIN-capped, C COIN+stubs+active-learning. The machinery is real iff **C reconstructs the true shape with fewer probes, marks limited-angle gaps as fuzz/stubs, aims new probes into those gaps, and produces fewer false sharp bits** than A or B.
3. **Derivation-entropy** (K1): if minimizing derivation entropy predicts the *same* crystallization order as a plain entropy-arrow account, the COIN gate adds no observable beyond the arrow of time - the instrument must show a render decision the entropy arrow alone does not.

---

## 10. What this changes in the canonical spec

- **Wrapper-as-measurement, bitemporal:** every wrapper carries a measurement-operator + noise-model, two clocks (`t_event`, `t_obs`), the six axes + WHOM + BEFORE/AFTER, and **per-axis `measured_bits` as an up-only lattice**. (Upgrades the v0.3 wrapper.)
- **Compiler:** DBSP-delta + CALM-merge (monotone/idempotent/order-free), materialized-view-over-log (every bit traces to an event), derivation-entropy as the retrieve/generate gate. `compile_substrate.py` is ~80% there.
- **Fidelity law:** measured_bits accrue as conditional MI (submodular); diversity>density; corroborated = independent-route; Covariance-Intersection for shared sources; two-regime curve with a hard error floor; lock condition.
- **Honest fuzz:** missing-wedge -> stub placement; bandpass/CS so gaps blur not streak; measured-first/generate-second/flagged; the held-out-view confabulation audit as a runtime COIN check.
- **Epistemic ladder:** three per-axis gates (structure-kink / corroboration / epiplexity); the existing MDL harness is the structure proxy; EDL per-channel test.
- **Conjecture-stub:** the typed hole above (noise-floor vs compute-bound), mandatory falsifier, distinct render grammar, claim-lifecycle + dead-children tally.
- **Valence = EIG:** the third coin doubles as the next-best-burst objective; the instrument self-aims at the highest-valence stub.
- **Constellation render:** a contested construct = a principle-vector of sub-axes, not a blob; the single-blob render is an artifact.

**Open / next:** the latent-axis-drift problem (section 9) is the next design target; the three settling experiments are runnable without building the full viewer; a cross-model A- on this v0.4 synthesis is the standing next check. Nothing here is built or committed.
