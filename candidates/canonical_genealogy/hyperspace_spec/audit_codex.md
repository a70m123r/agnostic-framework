**Verdict**

The docs are not yet lined up. They are a strong architecture metaphor with useful components, but they repeatedly promote analogies into mechanisms. The biggest failure mode is uncalibrated "measured_bits" over a latent, observer-shaped space.

**R-A: COIN Dial**

Coherent only if CONCEAL is renamed and treated as a labelled simulation/restoration mode. It is not "as honest" as EXPOSE just because the ledger is queryable.

The invariant is insufficient unless it includes enforcement outside the viewer: persistent visible badge, signed provenance, measured-vs-generated sidecar, export/API retention, screenshot/watermark policy, and a threat model. "Reversibility" inside the app is not proof once the render is copied, screenshotted, embedded, or cited. Fraud is correctly defined as misrepresenting conceal as expose, but the spec has not shown how that fraud is prevented.

**R-B: 4D CT**

Partly right: dynamic tomography is the better analogy than static latent shape. But basis rotation is not merely a Lipschitz/max-rate issue. It is an alignment, gauge, and identifiability problem.

If the latent basis rotates, coordinates no longer mean the same thing. A pure basis rotation may be no semantic change at all; an unaligned basis rotation can look like drift. A real basis change can also change the measurement operator itself. The fix is: require an explicit inter-slice alignment/transport map, uncertainty over that map, anchor entities, and an invariant metric. Without anchors, the gap slice is underidentified, not just blurry.

**1. Internal Consistency**

- Doc2 still says the honesty spine is unchanged: `rendered_sharpness(x) <= measured_bits(x)`. Doc1 says conceal mode may visually exceed measured bits. This is a direct leftover contradiction.
- "Never render a fake measured bit" conflicts with "try to hide all the fakes." The only coherent version is: never render generated content as measured.
- Bitemporality is muddled. Doc1 says observations change `B_hat`, not the past. Doc2 says probing reshapes the entity's measured extent and global dynamics. Separate posterior update, definition-conditioned view, and real causal attention events.
- Append-only log plus negative retractions plus CALM is inconsistent. The evidence log can be append-only, but derived beliefs/support are non-monotonic.
- Z-set deltas are not idempotent by default. Duplicate `+1` events double count unless event IDs dedupe. That is not a semilattice law.
- "Confidence only goes up" is wrong. Evidence volume can go up; confidence in a claim can go down.
- "Every rendered bit traces to log, therefore fake measured bits are structurally impossible" is false. Traceability catches missing provenance, not bad labels, bad sources, ingestion bugs, or generated content falsely tagged measured.
- Per-axis measured_bits are asserted, not defined. WHAT/HOW/WHY/WHO are correlated; composing them by a chain-rule metaphor is not enough.
- WHOM cannot be only the observer. Recipient, victim, beneficiary, audience, and affected party are content roles in many events.
- Valence = EIG contradicts Doc2's signed valence. EIG is nonnegative and task-relative; valence is utility/priority/sign.
- Section 9 says latent drift is reframed as solved, then the final section says latent-axis drift is still the next design target.
- Minor but important: "`The system never writes B*` ???" has a corrupted marker in a canonical doc.

**2. Over-Claiming**

- "Real machinery, not metaphor" and "almost one-to-one" are not warranted.
- Keyhole retrieval/spreading activation is not a Radon projection unless `P_i` is a known linear measurement operator.
- "`measured_bits` = volume of frequency space the slices fill" ignores noise, conditioning, priors, source dependence, and estimator bias.
- Sample complexity "`m ~ s` projection angles" is too loose. Compressed sensing needs assumptions like sparsity basis, incoherence/randomness, noise bounds, and log factors.
- Conditional MI is not universally submodular. It needs adaptive-submodularity/conditional-independence conditions.
- Cramer-Rao "`error ~ m^-1`" is sloppy. Variance can scale like `1/m`; standard error like `1/sqrt(m)`; inverse problems vary.
- "Gaps blur, never streak" is false as a CT claim. Limited-angle/missing-wedge artifacts are often directional streaks. Lowpass/TV is a prior, not a guaranteed lower bound.
- Kolmogorov structure-function "kink = knowledge" overstates an incomputable theory. MDL is a proxy, not the theorem.
- Derivation entropy does not validate the COIN. It is a retrieval-vs-computation proposal, not a provenance or truth gate.
- Epiplexity is relevant, but not a settled knowledge criterion.
- "Fuzzy region IS argmax-EIG" is false. High uncertainty can be irrelevant, unmeasurable, too costly, or low utility.
- V-Dem reclassification is a useful example of definition-sensitive classification, not a "measured_bits collapse."
- Stigler's law is not a formal cap on WHO-bits.
- "5W1H is near-optimal and exactly what event ontologies converge on" is too strong.

**3. Prior-Art Check**

- Grinbaum operational eternalism exists, but it is about higher-order quantum theory and indefinite causality. It supports an analogy, not this viewer's machinery.
- Ellis/Rothman CBU exists, but quantum crystallization is not the same as retroactive, definition-relative social origin.
- Xu/Li derivation entropy exists, but mapping it to "sharp=replay / fuzzy=generate" is speculative.
- DBSP supports incremental view maintenance with deltas. It does not grant idempotent semilattice merge or truth guarantees.
- CALM is correctly named, but misapplied to retractions, latest/confidence, and posterior belief updates.
- Radon/Fourier-slice theorem is correct for known linear tomography, not arbitrary semantic probes.
- Kolmogorov structure function is real prior art, but operational use needs explicit computable proxies and caveats.
- Epiplexity exists and fits bounded observers, but the doc overuses it as a gate.
- Spreading activation is a good retrieval/probe reference, not a tomography reference.
- BED-LLM supports EIG-driven questioning, not "valence is EIG."
- FisherRF supports EIG/Fisher active view selection for radiance fields. ActiveGS supports active scene reconstruction. Opt3DGS is mainly an optimization method, not provenance/active information machinery.

**4. Biggest Hole**

The spec never defines a valid measurement model for latent constructs. Without known measurement operators, noise models, source-dependence models, axis alignment, and calibrated bit units, `measured_bits` is just a badge. Then the COIN cannot be enforced, tomography does not apply, EIG is not meaningful, and conceal/expose cannot be audited.

**5. Minimal Fix List**

1. Split the law into two invariants: EXPOSE render cap and PROVENANCE render invariant. Stop saying conceal obeys the same COIN.
2. Add a conceal threat model: visible badge, signed ledger, measured/generated map, export retention, watermark/metadata policy.
3. Separate append-only evidence from non-monotonic derived belief. Remove CALM claims except for truly monotone event ingestion.
4. Define `measured_bits`: coding scheme, unit scale, estimator, uncertainty interval, dependency model, and per-axis calibration.
5. Replace generic "tomography" with "inverse problem." Use Radon/Fourier only where projections are actually linear and known.
6. Rewrite 4D drift around alignment: per-epoch local frames, transport maps, anchor sets, alignment uncertainty, and unidentifiable gaps.
7. Replace `valence := EIG` with `objective = expected utility / cost`, where EIG is one term.
8. Treat WHOM as both possible content role and observer role; do not collapse them.
9. Downgrade prior-art language from "one-to-one machinery" to "analogy or implementation inspiration."
10. Add ingestion/adversarial failure modes: false sources, copied sources, model-generated text mislabeled measured, and bad provenance.

Sources checked: [Grinbaum](https://arxiv.org/abs/2512.22879), [Ellis/Rothman](https://arxiv.org/abs/0912.0808), [DBSP](https://arxiv.org/abs/2203.16684), [CALM](https://arxiv.org/abs/1901.01930), [FisherRF](https://arxiv.org/abs/2311.17874), [ActiveGS](https://arxiv.org/abs/2412.17769), [BED-LLM](https://arxiv.org/abs/2508.21184), [epiplexity](https://arxiv.org/abs/2601.03220), [dynamic tomography](https://arxiv.org/abs/2204.09935), [diachronic embedding alignment](https://arxiv.org/abs/1605.09096), [C2PA critique](https://arxiv.org/abs/2604.24890).
