Bottom line: the Claude-side audit is directionally right, but A needs demotion. This run did **not** demonstrate origin-bias detection. It mostly demonstrated common-prior collapse, item-definition sensitivity, and one bad/noisy refusal item.

**A. Verdict: overstated**

What survives: C3 is a real fan, not fringe. The “Four Great Inventions” are conventionally Chinese-origin inventions, but the grouping also has a Western/Needham genealogy and is used as a cultural-national frame; open summaries cite scholarship questioning the category/emphasis and tracing its Western construction. See the “Four Great Inventions” analysis trail: Chinese inventions and East-West interaction are both in play, and the category’s Western/commonplace genealogy plus later appropriation is explicitly described.

Sharpest flaw: A conflates **origin credit** with **heritage/framing**. If the question means “where did these four technologies originate?”, “Chinese” is the dominant correct answer. If it means “is the Four Great Inventions frame itself a nationalist/constructed/global-diffusion frame?”, “shared/constructed” is live.

Fix: split C3 into three scored items: factual origin, genealogy of the “Four Great Inventions” category, and normative heritage framing.

**B. Verdict: sound**

Sharpest flaw in the meter claim: the run has no basis yet for bloc-level inference. The only stable divergence is Gemini on C1; Qwen is intra-model scatter, not a CN-bloc signal. With 5 providers and 3 reps each, provider personality and sampling variance dominate origin.

Fix: add more providers per bloc, more reps, and a pre-registered multilingual harvest including Chinese institutional and scholarly sources. Then model origin as one factor after provider-level variance.

**C. Verdict: sound**

F1/F2/F3/C2 are good negative controls: they did not manufacture an origin split. F2 and F3 are conventional enough that convergence is expected: Cai Lun is the standard papermaking figure, with caveats about earlier paper; Bi Sheng is the standard movable-type figure. C2 also largely discharges to China under “earliest firearm/gun” definitions.

Sharpest flaw: “flat” only means “no split observed,” not “the instrument is trustworthy.” Agreement still buys zero corroboration. Also C2 should be definition-locked: fire lance, hand cannon, firearm, modern gun.

Fix: keep these as calibration items, but label them as negative controls, not positive validation.

**D. Verdict: sound, with risky examples**

Core is right: do not refire on questions with no harvestable substrate. Taiwan/COVID-style broad prompts become model opinion polling unless reduced to checkable subclaims.

Sharpest flaw: Senkaku/Diaoyu and Kashmir can also degrade into sovereignty/framing polling unless constrained.

Fix: use bounded tasks: “what names do Japanese/Chinese/UN maps use?”, “render labels under source X/Y,” “which entity administers location Z on date D?” Avoid “who is right?”

**What This Run Measured**

The single most important measured signal is **shared default-prior dominance, not origin bias**. Numerically: 0/3 contested items split by origin bloc, 0/3 fillable split. C3 went 15/15 “Chinese” despite a live framing fan. N2 went 15/15 non-refusal, which is either a refusal failure or a badly planted noise item because many readers will interpret it as “what did Gutenberg contribute?”

**Best Next Change**

Pre-register a multilingual, de-duplicated independent harvest and scoring rubric before the next run. Include Chinese institutional/scholarly sources, Western sources, and relevant third-region sources. Then split ambiguous prompts into factual substrate and framing layer.

**Primary Read-Out**

“Shared-prior collapse vs origin-split” is the right diagnostic contrast, but not the whole primary read-out. Better primary metric:

`fact accuracy + fan preservation + noise refusal + origin-bloc variance`

Origin-split should be secondary unless the item has already passed harvest quality and definition clarity.
