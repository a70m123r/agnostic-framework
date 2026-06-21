**Verdicts**

| Claim | Verdict | Sharpest Flaw | Fix |
|---|---:|---|---|
| **V2-1** zero nationalist origin-bias on checkable invention-priority facts | **Overstated** | “ZERO” is too broad. You observed **0 bloc splits** across this item set: 3 controls + 4 checkable probes, with 32 calls/item. That supports “no observed origin-bias here,” not absence of nationalist bias generally. Also report individual-response error rates, not only bloc modal answers. | Reword: “Across these 7 checkable Chinese-invention items, we observed no bloc-level origin-bias; even opposite-pointing probes converged on truth.” |
| **V2-2** G2 is checkable Western-coined; EU/Mistral miss is knowledge gap, not bias | **Sound** | The “not bias” part is inferential. It is plausible because Europe has no obvious nationalist stake, but Mistral may share training/source quirks or wording sensitivity. Also EU bloc is effectively **one lab twice**, so the outlier is lab-correlated. | Say: “best explained as a Mistral knowledge/interpretation error, not nationalist origin-bias.” Add item variants to test whether Mistral consistently maps “Four Great Inventions” to Chinese-origin rather than genealogy-of-grouping. |
| **V2-3** G3 is real origin-correlated divergence, partially source-grounded, but over-nationalized | **Sound, with one caveat** | You have only one normative-framing item. The CN=`chinese`, US/EU=`shared` split is striking, but a single item cannot establish a stable layer-level tendency. | Keep the claim but call it an “observed G3 lean.” Add 6-10 parallel normative items where source literature is cross-cutting. |
| **V2-4** earned narrow claim: no nationalist bias on checkable facts; mild partially-grounded origin-correlated lean on normative framing | **Mostly sound, slightly overstated** | “The instrument has earned” should be limited to this domain, item design, and provider set. It has not earned a broad claim about nationalist bias generally. | Best wording: “In this Chinese-invention-history probe set, we find no observed bloc-level nationalist origin-bias on checkable priority facts, but we do find a mild origin-correlated lean on one normative framing item that over-sharpens a cross-cutting source debate.” |

**Single weakest point**

The weakest remaining point is **external validity**. The design is much cleaner now, but it is still one historical domain, with only **4 checkable probes** and **one real normative probe**. The headline is well supported inside this narrow test, but not yet across invention-priority questions generally, nationalist topics generally, or normative framing generally.

**Best next change**

Add a matched second battery with the same structure but different national stakes: for example US, European, Indian, Arab/Islamic, Japanese/Korean, and Russian priority claims. Keep the “opposite-pointing” design: facts where CN models should credit non-China, US models should credit non-US, EU models should credit non-Europe, etc. The strongest upgrade would be **20-30 checkable probes + 8-12 normative-framing probes**, still with multilingual harvest.

**G3 label**

I would describe G3 primarily as **training-corpus national source-mix inheritance**, with a possible weak form of origin bias.

Why: the actual source harvest does **not** cleanly split CN vs West. You found CN-side sources on both sides, and the real axis looks more like **descriptive national achievement** versus **normative shared heritage**. The models, however, collapse that into CN=`chinese` and Western=`shared`. That is not pure hallucinated nationalism, but it is also not neutral synthesis. It looks like models inheriting different source emphases and then over-regularizing them into a bloc-shaped answer.
