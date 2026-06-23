I checked the local [recode_scored.json](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/recode_scored.json) and [recode_codebook.json](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/recode_codebook.json). Bottom line: keep the finding, but demote it to “models compress toward canonical textbook genealogies, especially outside Mistral-style exhaustive enumeration.” Do not sell it as clean non-Western bias.

**R1: Overstated**

The omission gap is real in the recode: the 12 non-saturated contested units average `0.422` credit versus uncontested controls at `0.8875`. Taqi al-Din `0/16`, Maya `2/16`, Papin `2/16`, Islamic optics `5/16` are not noise.

Sharp flaw: H_S proves “creditable legitimacy,” not “required omission error.” Some units are precursor/foundation/parallel-lineage rather than direct artefact origin.

Fix: split units into tiers: direct origin, transmission, parallel independent invention, precursor/foundation, named-person. Report the gap within tier.

**R2: Sound, But Not Killer**

The data strongly rejects simple nationalism/home-boosting. China-owned units are not reliably boosted by CN models: `china_tianyuan` CN `.33` vs EU `1.0`; `china_still` CN `.33`, lowest bloc. Papin gets EU `0`.

Sharp flaw: this only kills naive self-favoritism. It does not kill training-corpus canon, English-prompt effects, answer verbosity, or local textbook canon effects. Many “home” civilizations are not represented by model blocs.

Fix: test home-bias with matched owned marginal nodes across actual represented blocs, plus Arabic/Turkish/Indian/African/Spanish-language model or prompt conditions.

**R3: Risky**

The family/verbosity explanation is very plausible. For the 12 contested units: CN mean `.402`, US `.292`, EU `.646`; EU is basically the Mistral pair enumerating precursor-fans.

Sharp flaw: bloc and family are still entangled. “EU” equals Mistral here, so the design cannot fully separate European bloc effects from Mistral answer style.

Fix: normalize by output length and number of named units; add forced-N answer formats; broaden EU/US/CN families; fit model-family and verbosity as covariates.

**R4: Sound As Reframe**

This is the best interpretation. The canonical Arab/Islamic transmitter slot saturates around `.98`, while off-spine nodes collapse, including Western marginal nodes like Papin `.125` and Hero `.4375`. So “non-Western” is too broad; “non-canonical / off textbook spine” fits better.

Sharp flaw: the codebook was built around contested nodes from only 7 artefacts, so “canon-compression” is not yet a general law.

Fix: build a balanced 2x2: Western/non-Western x canonical/non-canonical, matched for artefact relevance and fame, with canonicality measured independently before scoring.

**R5: Sound**

The Onesimus result is decisive for granularity. “West Africa” gets `.625`, but Onesimus as a named person is `0/16`. That means civilization-level credit can survive while person-level attribution vanishes.

Sharp flaw: current scoring mixes civ, tradition, and named-person units.

Fix: publish separate civ-level, tradition-level, and named-person rates. Do not let “Africa” count as Onesimus in person-resolution claims.

**H_S Sufficiency**

H_S partially breaks the harvest-echo confound. It shows that low-credit nodes are not merely invented by a thin EN+ZH harvest. But it does not fully break circularity if the same LLM-style process selected sources, judged legitimacy, and scored semantic credit.

The residual risk is not “pure circularity”; the sources are external. The risk is coder/LLM-mediated circularity: deciding what counts as a required credit-unit and what counts as semantic credit may import the same priors.

**Most Important Check**

Do a non-LLM, blinded double-rescore of the same 240 cached outputs using the frozen codebook and source packets. Hide provider/bloc labels. Require two human coders plus adjudication, report agreement, and rerun the headline means.

Pass condition: the 12 contested mean stays near `.42`, canonical controls stay near `.89`, and load-bearing lows remain low: Taqi al-Din near `0/16`, Maya near `2/16`, Papin near `2/16`, Islamic optics near `5/16`. If that survives, call it a finding. If not, keep it as an audit hypothesis.
