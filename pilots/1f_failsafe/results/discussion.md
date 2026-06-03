# Pilot #150 — Result-commit discussion (GDELT v2, H1 verdict)

**Date:** 2026-06-03 (result-commit). Pre-registration locked 2026-06-02 BEFORE any GDELT data examined ([`candidates/1f_l0_failsafe_signature.md`](../../../candidates/1f_l0_failsafe_signature.md) §4; N=6 amendment [`confounds.md`](../confounds.md) §1).
**Data:** GDELT v2 `gdelt-bq.gdeltv2.events`, queried via BigQuery 2026-06-03 (21.39 GB scanned, 47,610 country-day rows; window 2015-02-18 → 2025-12-31, daily). Methods + reproducibility: [`methods.md`](methods.md).

---

## §1 Verdict: **H1 NOT SUPPORTED** (confounded null)

On the pre-registered **primary signal (event-category-entropy)**, across the N=6 paired comparisons:

| quantity | pre-registered target (H1) | observed |
|---|---|---|
| mean Δβ (auth − plur) | **< −0.10** | **+0.084** (wrong sign) |
| Cohen's d | ≥ 0.5 (magnitude) | +0.380 |
| permutation p (one-sided, Δβ<0) | < 0.05 | **0.792** |
| pairs with β_auth < β_plur − 0.10 | 6/6 | **1/6** |

**H1 predicted authoritarian systems would show *lower* β (less broadband 1/f). The data show the opposite weak tendency (authoritarian β slightly *higher*), and it does not reach significance or the pre-registered effect-size bar.** The pre-registered permutation test fails to reject in the H1 direction (p = 0.79).

Crucially, the cross-country β contrast that does exist is **almost entirely a source-volume artifact, not a political-system signal** (§3). The volume-robust DFA-α estimator shows essentially **no cross-country difference at all** (§3). So the honest characterization is a **confounded null**: H1's predicted direction is absent, and what little Welch-β spread exists tracks media-event volume rather than the authoritarian/pluralistic axis.

**Promotion Bar A ([candidate §8](../../../candidates/1f_l0_failsafe_signature.md)) is NOT satisfied.** It required H1 to land at d ≥ 0.5, p < 0.05 in the predicted direction. It did not.

This is not a clean §4.4 falsifier either (that required Δβ > 0 at d ≥ 0.5 on the primary signal; observed d = 0.38 < 0.5), and the confound makes the *direction* uninterpretable. See §6 for the precise mapping to the pre-registered outcome categories.

---

## §2 The numbers

### Per-country spectral exponent (primary signal: event-category-entropy)

| country | role | Welch β (primary) | DFA α (robustness) | β 95% CI (block-bootstrap) | total events |
|---|---|---|---|---|---|
| CHN | auth | 0.957 | 0.866 | [0.94, 1.61] | 22.3M |
| USA | plur | 1.083 | 0.839 | [0.80, 1.29] | 204.4M |
| RUS | auth | 0.879 | 0.867 | [0.74, 1.49] | 37.0M |
| GBR | plur | 0.890 | 0.843 | [0.55, 1.02] | 34.9M |
| PRK | auth | 0.616 | 0.838 | [0.68, 1.26] | 3.3M |
| DEU | plur | 0.695 | 0.866 | [0.53, 1.38] | 14.4M |
| IRN | auth | 0.683 | 0.873 | [0.67, 1.21] | 11.6M |
| FRA | plur | 0.631 | 0.887 | [0.53, 1.59] | 16.4M |
| TUR | auth | 0.791 | 0.856 | [0.62, 1.72] | 14.9M |
| NLD | plur | 0.382 | 0.827 | [0.25, 1.45] | 3.3M |
| VEN | auth | 0.605 | 0.901 | [0.52, 1.50] | 6.0M |
| CHL | plur | 0.348 | 0.828 | [0.26, 1.42] | 2.4M |

### Per-pair Δβ (auth − plur), primary signal

| pair | Δβ | direction | provenance |
|---|---|---|---|
| CHN − USA | −0.126 | H1 (auth lower) | original N=3 |
| RUS − GBR | −0.011 | ~tie | original N=3 |
| PRK − DEU | −0.079 | H1 (weak) | original N=3 |
| IRN − FRA | +0.052 | anti-H1 | added in N=6 |
| TUR − NLD | +0.409 | anti-H1 (large) | added in N=6 |
| VEN − CHL | +0.257 | anti-H1 (large) | added in N=6 |
| **mean** | **+0.084** | **anti-H1** | |

### All three signals (primary + secondary/exploratory)

| signal | role | mean Δβ | p (one-sided) | Cohen's d | dir | outcome |
|---|---|---|---|---|---|---|
| event-category-entropy | **PRIMARY (H1)** | +0.084 | 0.792 | +0.380 | 1/6 | H1 not supported |
| event_count | secondary (H2) | +0.100 | 0.955 | +0.527 | 0/6 | anti-H1 direction |
| mean_tone | secondary (H3) | +0.148 | 0.955 | +0.937 | 0/6 | anti-H1 direction |

All three signals point the *same* way — **opposite to H1** — but all three are subject to the same source-volume confound (§3), and tone carries the pre-registered cross-language caveat ([candidate §5.5.4](../../../candidates/1f_l0_failsafe_signature.md)).

---

## §3 The decisive confound: per-country event volume

**[Tier 1, empirical]** Across the 12 countries, the entropy-signal Welch β is almost perfectly rank-ordered by event volume:

- **Pearson r(log₁₀ total events, β) = +0.916; Spearman = +0.909.**
- The four lowest-volume countries (CHL 2.4M, PRK 3.3M, NLD 3.3M, VEN 6.0M) hold four of the five lowest β values. The highest-volume country (USA 204M) has the highest β.

**Mechanism:** daily category-entropy is estimated from a finite number of events. Low-volume countries have noisy daily entropy estimates; that sampling noise is approximately white (independent across days), adding a flat high-frequency floor to the power spectrum that *flattens the fitted slope* — i.e. **biases β downward for low-volume countries**. Pre-registered z-score normalization (candidate §5.2.1) removes mean/variance scale differences but **does not remove this spectral-floor effect**, because it is a frequency-domain artifact, not an amplitude one.

**Corroboration from the volume-robust estimator.** DFA integrates the series before measuring fluctuation scaling and is far less sensitive to a white high-frequency floor. The DFA-α estimates are **nearly identical across all 12 countries** (range 0.827–0.901, spread **0.074**), versus the Welch-β spread of **0.735**. The two estimators agree only that there is *some* long-range correlation everywhere (α ≈ 0.85, β ≈ 1) and disagree entirely on cross-country *differences* — exactly the signature of a volume-driven high-frequency artifact contaminating the Welch sub-band fit.

**Implication:** the cross-country Welch-β variation this pilot measured is dominated by media-event volume, not by political system. The operationalization as written cannot separate "authoritarian system" from "low GDELT coverage." This is the central finding of the result-commit.

---

## §4 Per-pair pattern (and why it does not rescue H1)

The N=6 result splits cleanly along provenance: the **original N=3 pairs** (CHN-USA, RUS-GBR, PRK-DEU) all lean weakly H1-direction (Δβ = −0.13, −0.01, −0.08), while the **three pairs added in the N=6 amendment** (IRN-FRA, TUR-NLD, VEN-CHL) all go anti-H1 (+0.05, +0.41, +0.26) and dominate the mean.

This is **entangled with the volume confound**, in both directions, which is why it must not be read as support for H1:
- In TUR-NLD and VEN-CHL, the *pluralistic* member (NLD 3.3M, CHL 2.4M) is very low volume → its β is artifactually depressed → Δβ(auth−plur) is pushed *positive* (anti-H1).
- In PRK-DEU, the *authoritarian* member (PRK 3.3M) is low volume → PRK β depressed → Δβ pushed *negative* (toward H1).

So the sign of each pair's Δβ is partly determined by which side happens to be lower-volume — not by failsafe health. Selecting the three "classic" pairs as if they confirmed direction would be **post-hoc cherry-picking against the locked N=6 protocol** and is explicitly rejected here.

---

## §5 IAAFT surrogate diagnostic (pre-reg §5.4.2)

**[Tier 1, empirical]** For the primary signal, observed β sits **systematically below** the IAAFT surrogate β distribution, and the gap is largest for the low-volume countries:

| country | obs β | surrogate β mean | z |
|---|---|---|---|
| USA (204M) | 1.083 | 1.125 | −1.8 |
| CHN (22M) | 0.957 | 1.196 | −7.3 |
| PRK (3.3M) | 0.616 | 0.961 | −14.2 |
| CHL (2.4M) | 0.348 | 0.916 | −13.9 |

Two honest notes:
1. The a-priori expectation (recorded in code) was that IAAFT — which preserves the global power spectrum — would yield surrogate β ≈ observed β, making it a **degenerate** null for β. **That expectation was wrong.** Because β is fit on a *sub-band* [1/365, 1/10] and these signals are strongly non-Gaussian (spiky, bounded, zero-inflated for sparse countries), IAAFT's amplitude-matching step measurably shifts the sub-band slope.
2. The resulting pattern is itself **further evidence of the volume/distribution artifact**: the surrogate-vs-observed gap scales with sparsity (|z| = 14 for CHL/PRK, ≈ 2 for USA). The β of low-volume countries is the least stable / most distribution-dependent.

This is *not* used to adjust the H1 verdict (the locked permutation test stands as the inference). It is reported per pre-registration and flagged in [`confounds.md`](../confounds.md) §12.

---

## §6 Mapping to the pre-registered outcome categories

Per [candidate §4.4](../../../candidates/1f_l0_failsafe_signature.md) and the HANDOFF verdict table:

- **PASS** (Δβ < −0.10, d ≥ 0.5, p < 0.05): **No.** Observed +0.084, p = 0.79.
- **Clean falsifier** (Δβ > 0 at d ≥ 0.5 on primary): **No.** Direction is anti-H1 but d = 0.38 < 0.5 on the primary signal. (Both *secondary* signals do reach d ≥ 0.5 anti-H1, but they are exploratory and equally volume-confounded.)
- **Strict null** (|Δβ| < 0.05): **No.** |Δβ| = 0.084.
- **Best description:** **confounded null** — the predicted direction is absent; the measured contrast is a volume artifact (r = 0.92); the volume-robust estimator (DFA-α) is flat. H1's operationalization cannot be cleanly evaluated on this dataset as specified.

---

## §7 Tier-tagging of claims (cont 27 §2 discipline)

- **[Tier 1, empirical]** "GDELT v2 event-category-entropy Welch β (2015–2026, [1/365,1/10] band) is 1.08 for USA, 0.96 for CHN, 0.35 for CHL, … ; β correlates with log event volume at r = 0.92; DFA-α is ≈0.85 ± 0.04 for all 12 countries." — direct measurement on this dataset.
- **[Tier 2 candidate, NOT advanced]** "The authoritarian/pluralistic axis maps to L0-failsafe-health via a 1/f spectral signature" (Reading 06 §10.3). This pilot provides **no support** and, after the volume confound, **no clean refutation**. The candidate does **not** advance to Tier 2 algorithmically-demonstrated (Bar A unmet) and is **not** demoted here — see §8.
- **[Tier 3, explicitly NOT claimed]** Nothing about "authoritarian systems are brittle/robust." The data cannot speak to that; the headline contrast is a measurement artifact.

---

## §8 What this means for the framework — surfaced for Cowork/Pav (not actioned here)

Per the HANDOFF guardrails, the result-commit Claude-Code session does **not** demote canon, promote primitives, or amend Reading 06. The following are **recommendations for Cowork's next session**, not changes made here:

1. **Narrow, do not yet demote.** The pilot does not refute Reading 06 §10.3's underlying claim; it shows the *GDELT-entropy operationalization* is confounded by event volume and cannot test the claim as specified. Per [cont 27 §3](../../../continuations/27.md) pruning procedure, the disciplined move is to **narrow** the §10.3 Tier 2 conditional ("not testable via volume-unmatched GDELT country aggregates") rather than demote on one confounded null.
2. **Run the second test before any demotion.** The HANDOFF + candidate §8 Bar B name the **Wikipedia edit-cadence** pilot (matched-topic articles across zh/ru/en/de) as an independent signal source. Edit cadence is far less volume-skewed than GDELT media coverage and would be a cleaner test of the same hypothesis. If it also nulls, *then* consider demotion.
3. **A volume-controlled v2 of this pilot is the obvious fix.** Options: (a) Poisson-thin every country to a common daily event rate before computing entropy; (b) restrict to volume-matched pairs; (c) use DFA-α (volume-robust) as the primary estimator instead of Welch-β; (d) model the white-noise floor explicitly and fit β above it. Any of these would let GDELT actually test H1. **Pre-register the v2 before re-running** (do not retro-fit to this dataset).
4. **The DFA-α null is itself a mild Tier-1 datum:** at the social-media-coverage substrate, daily category-entropy is ≈ pink (α ≈ 0.85) *everywhere*, with no authoritarian/pluralistic separation detectable by the volume-robust estimator. Whatever 1/f structure exists is common to all 12 media ecosystems.

---

## §9 Honest limits

- **N = 6 is small.** Even absent the confound, six paired comparisons is the minimum for the test; this is a screening pilot, not a definitive result. (Candidate §7.)
- **The confound was not anticipated in the pre-registration.** §5.2.1 z-scoring was expected to handle source-volume; it does not handle the spectral-floor mechanism. This is logged in [`confounds.md`](../confounds.md) §10 as a *discovered* confound, not a retro-active pre-registration change.
- **Tone (H3) and event_count (H2) are exploratory** and not corrected for the cross-language tone pipeline or volume; their stronger anti-H1 effect sizes (d = 0.94, 0.53) are **not** elevated above the primary signal's verdict.
- **GDELT source-selection bias** (candidate §7 confound 2) remains: GDELT indexes an English-weighted media subset; "PRK coverage" is what GDELT chose to index, not all DPRK media.
- **Method substitutions** (BigQuery aggregation; block-bootstrap CI in place of `powerlaw.Fit`) are documented in `confounds.md` §9 and §11; none touch the locked H1 permutation test.

---

## §10 One-line summary

> **Pilot #150 result: H1 not supported. On GDELT v2 event-category-entropy (2015–2026, N=6 pairs), authoritarian systems do not show the predicted lower 1/f exponent; the small anti-direction Welch-β contrast (Δβ=+0.08, d=0.38, p=0.79) is a source-volume sampling artifact (β vs log-volume r=0.92), and the volume-robust DFA-α shows no cross-country difference. Bar A unmet. Recommended: narrow Reading 06 §10.3, run the volume-robust Wikipedia replication before any demotion.**
