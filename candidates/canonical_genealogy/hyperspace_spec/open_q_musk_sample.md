# Elon Musk - a data-grounded person sample for the zone/lifecycle model

**Status:** READ-ONLY public-data worked example. SPEC-only viewer; no live system perturbed. Every value is badged **[MEASURED]** (multi-source corroborated public record), **[MEASURED-VOLATILE]** (real and sourced but live/market-driven, render with a confidence blur), **[ESTIMATE]** (single-source, self-reported, or my own bit-assignment), or **[SPEC]** (model-level speculation).

**Fresh-scan note (2026-06-14):** The most volatile facts were re-verified this scan. The June 12 2026 SpaceX IPO and Musk's trillionaire status are confirmed by CNBC, Bloomberg, Fox Business, and Fortune. Post-IPO net worth is now reported at **~$1.05-1.1T** (SpaceX stake ~$766B at the $150 open + Tesla ~$280B), which *supersedes* the digest's pre-IPO ~$780B Forbes figure. The Feb 2 2026 SpaceX-xAI all-stock merger ($1.25T combined: SpaceX ~$1.0T + xAI ~$250B) is confirmed by CNBC/CNN/Motley Fool.

---

## 0. The model in one paragraph (what we are testing)

Pav's claim: a real entity can be rendered in the canonical-space viewer as **two fibrations over one shared base poset** - a PHYSICAL nesting tree (places, sites, dwellings) and a LATENT containment tree (person -> companies -> industries -> ideas) - coupled at **seams** (observation/assertion events). The anchor of the latent tree is not a precise point but the **origin seen through its lifecycle**: a person who *called* an idea, blurring outward into a **zone of influence** for organizations. Sharpness is continuous and set by the COIN: `rendered_sharpness(x) <= measured_bits(x)`, with `sigma = 2^(-location_bits)`. Low location-bits = wide blur = a zone. **Blur is the honesty badge.**

This document runs that model against Elon Musk and reports, honestly, where it holds and where it breaks.

---

## 1. PHYSICAL chain - lifecycle from a sharp origin point to multi-site zones

The physical fibration is a **sharpness gradient over time**. `sigma = 2^(-location_bits)`; higher bits = sharper = smaller sigma. I list each beat with an assigned bit-level and the resulting blur character. Bit assignments are **[ESTIMATE]** (my mapping of public locational precision onto a log2 scale); the underlying facts are badged separately.

### 1a. The sharp origin (the lowest-blur beat in the whole lifecycle)

| Beat | Date | location_bits | sigma character | Fact badge |
|---|---|---|---|---|
| **Born, Pretoria, South Africa** | 28 Jun 1971 | ~30 [ESTIMATE] | near-point (a single dated person at a single city, even building-level if the hospital were public) | [MEASURED] birth date/place (Wikipedia) |

This is the canonical lifecycle ORIGIN anchor. A single person at a single dated event - **the COIN permits a near-point render here**, and nothing later in the lifecycle is sharper. This is the empirical confirmation of the steer's "person at origin = sharp point."

### 1b. The migrating point / trajectory (childhood -> emigration -> university)

| Beat | Date | location_bits | sigma character | Fact badge |
|---|---|---|---|---|
| Parents divorce; lives with father Errol | 1979 (~age 9) | ~28 [ESTIMATE] | sharp | [MEASURED] |
| Schools: Waterkloof Prep -> Bryanston High -> Pretoria Boys High | ~1977-1988 | ~26 [ESTIMATE] | sharp cluster of named points | [MEASURED] schools; [ESTIMATE] the Blastar ~$500 sale (self-reported) |
| Leaves SA for Canada (Saskatchewan, cousin's farm) | Jun 1989 | ~18 [ESTIMATE] | sharp moving point, **fuzzy farm sub-location** | [MEASURED] emigration; [ESTIMATE] exact farm |
| Queen's University, Kingston ON | 1990-1992 | ~26 [ESTIMATE] | sharp (named campus) | [MEASURED] |
| Transfer to UPenn/Wharton, Philadelphia; BA physics + BS economics | 1992; **degrees awarded 1997** | ~26 site / **but year carries a blur** | sharp place, **temporally blurred** | [MEASURED] place; **[CONTESTED]** year: registrar 1997 vs Musk's stated 1995 |

**COIN flag (do not fake a sharp bit):** the graduation year has *conflicting measured bits* (1995 self-claim vs 1997 registrar). The viewer must render this beat with a **temporal blur / badge**, not a single asserted year. This is a clean real-world instance of "never render a fake measured bit" applied to the *time* axis rather than space.

### 1c. The point -> zone pivot (first organization)

| Beat | Date | location_bits | sigma character | Fact badge |
|---|---|---|---|---|
| Declines Stanford PhD; co-founds **Zip2**, Palo Alto | 1995 | site ~22 / **zone ~7** | **point begins to spread into a zone** | [MEASURED] founding; Zip2 sold to Compaq 1999 ~$307M [MEASURED] |

This is the first beat where the physical anchor stops being a person-point and becomes an **organization with a site and a zone** - the model's predicted transition.

### 1d. The diffuse multi-zone influence-field (the mature career)

Here the physical tree is no longer one anchor but a **set of (site_bits, zone_bits) pairs**. Crucially, site-bits and zone-bits are **independent axes** - the digest found cases where they invert. All coordinates below are **[MEASURED]** from public records; the bit numbers are **[ESTIMATE]**.

| Site | site_bits | zone_bits | Notes |
|---|---|---|---|
| SpaceX **Cape Canaveral SLC-40 / KSC LC-39A**, FL | ~23 (govt-published pad coords) | ~4 (Space Coast + offshore downrange, intentionally diffuse) | sharpest site in the atlas |
| Tesla **Fremont**, CA (45500 Fremont Blvd; 37.4950N,121.9425W) | ~22 | ~6 | full street address + coords |
| Tesla **Giga Berlin**, Gruenheide (Tesla Strasse 1; 52.395N,13.790E) | ~22 | ~6 | **water-use dispute makes the zone a live, contested measurement** |
| SpaceX **Hawthorne**, CA (1 Rocket Road) | ~22 | ~7 | original HQ; now industrial campus only |
| Tesla **Giga Texas / Austin** (global HQ; ~30.22N,97.62W) | ~21 | ~6 | re-anchored HQ (see 1e) |
| Tesla **Giga Shanghai** (Tonghui Rd 168; 30.8703N,121.7689E) | ~21 | ~4 (effectively a *national market* zone) | highest-volume plant |
| SpaceX **Starbase / Boca Chica**, TX (launch pad ~25.997N,97.157W; **incorporated city 2025**) | ~20 (city boundary adds spread) | ~5 | new corporate HQ + Musk's dwelling |
| SpaceX **McGregor**, TX (engine test; ~4,000 acres) | ~18 (large acreage) | ~6 | acreage shaves point-precision |
| xAI **Colossus** (TN/MS borderland) | ~16 | ~5 (litigated power/air/water footprint) | environmental litigation *raises* the zone bit-count |
| **The Boring Company** (Bastrop HQ) | **~16 (fuzzy HQ)** | **~9 (permitted, mapped Vegas Loop)** | **AXIS INVERSION: the zone is better-known than the HQ** |

**Key model finding (holds):** a single sharpness scalar is *insufficient*. The Boring Company's mapped Vegas Loop (zone ~9) is **more precisely known than its own headquarters** (~16... wait - higher bits = sharper, so HQ ~16 is sharper than zone ~9 in absolute terms, but the *surprise* is that a permitted public-works zone is unusually crisp for a zone, ~9 vs the typical ~4-7). The model **needs two bit-axes per entity** (site_bits, zone_bits), confirmed.

### 1e. The re-localized sharp dwelling-point inside a global zone (present edge)

| Beat | Date | location_bits | sigma character | Fact badge |
|---|---|---|---|---|
| Moves to Texas; **~$50k prefab tiny home, Boca Chica/Starbase** (rented from SpaceX) + Boxabl guest house; ~$35M Austin-adjacent property | 2020-2021 | dwelling ~24 [ESTIMATE] / personal-influence zone ~1-2 [ESTIMATE] | **re-sharpened dwelling-point nested inside a now-global influence zone** | [MEASURED] move; **[ESTIMATE]** the $50k and $35M dollar figures (single-source, Fortune/Isaacson) |
| **SpaceX IPO -> world's first trillionaire** | 12 Jun 2026 | n/a (a valuation, not a place) | **[MEASURED-VOLATILE]** - render with confidence blur | $135 IPO, opened $150; net worth ~$1.05-1.1T (SpaceX ~$766B + Tesla ~$280B) [MEASURED-VOLATILE] |

**Model finding (holds, and is striking):** the lifecycle is genuinely **U-shaped in dwelling-sharpness** - a sharp Pretoria origin-point, a long diffuse multi-zone middle, and a *late re-sharpening* to a single tiny home, all while the *influence* zone monotonically widens to planetary scale. The physical anchor and the influence zone **decouple in late life**: dwelling sigma shrinks while influence sigma explodes. This is exactly the steer's "late re-localized sharp dwelling-point nested inside a now-global influence zone," and it is the most elegant single confirmation in the dataset.

---

## 2. LATENT containment chain - person -> companies -> industries -> ideas

The latent fibration. The person is the sharp seam; everything below is a zone. **Origination vs amplification is badged per idea** - this is where the model earns its keep, because it forces an honest attribution that a naive "founder" label hides.

```
PERSON: Elon Musk  [sharp lifecycle-origin point]
   |
   +-- COMPANIES  [each a zone of operation + influence]
   |     |
   |     +-- SpaceX  ("SpaceXAI" after Feb 2026)  -- relatively sharp anchor (Starbase) blurring to a global Starlink/orbital mesh
   |     |     +-- xAI  (absorbed Feb 2026)
   |     |           +-- X / Twitter  (absorbed by xAI Mar 2025)
   |     +-- Tesla  (independent)  -- Austin + Gigafactories + global fleet
   |     +-- Neuralink  (independent)
   |     +-- The Boring Company  (independent)
   |
   +-- INDUSTRIES: aerospace | automotive+energy | social media | neurotech | AI
   |
   +-- IDEAS  [the latent layer]
```

### 2a. The six ideas, badged by origination vs amplification

| # | Idea | Company | Musk's true role | Origination vs Amplification | Badge |
|---|---|---|---|---|---|
| 1 | **Reusable rockets** | SpaceX | Made it economically real; first orbital-class propulsive landing (Falcon 9, Dec 21 2015) | **AMPLIFIER/commercializer** - prior art NASA Shuttle, DC-X | [MEASURED] |
| 2 | **Mars settlement / "multiplanetary"** | SpaceX | Made it SpaceX's raison d'etre; **named** the framing ("Making Humanity a Multi-Planetary Species," New Space, 2016) | **CHAMPION + NAMER** - idea old (von Braun 1948) | [MEASURED] |
| 3 | **EVs at scale** | Tesla | "Secret Master Plan" (2006) top-down strategy | **AMPLIFIER + strategist; legally-settled co-founder** - founded 2003 by Eberhard & Tarpenning | [MEASURED] incl. 2009 lawsuit settlement |
| 4 | **Free-speech platform / "digital town square"** | X | Acquired Twitter ($44B, Oct 2022); rebranded X (2023) | **ACQUIRER + NAMER** - Twitter founded 2006 by others; town-square metaphor predates him | [MEASURED] |
| 5 | **Brain-computer interface ("neural lace")** | Neuralink | Co-founder + primary funder | **CO-FOUNDER, but concept borrowed/NAMED** from Iain M. Banks' Culture novels | [MEASURED] |
| 6 | **Safe AGI** | xAI (founder) | Founded xAI (Mar 2023); the safety framing traces to co-founding OpenAI (2015) | **FOUNDER of the company; amplifier/co-originator of the safety framing** (shared with Bostrom/Yudkowsky/OpenAI cofounders) | [MEASURED]; attribution is the softest (MEDIUM-HIGH) |

**Model finding (holds, and is the sharpest insight of the exercise):** Musk is a **genuine originator of essentially zero of the six headline ideas**. He is the founder-of-company for only Neuralink and xAI, and even those ideas are borrowed (neural lace from fiction; AGI-safety from the broader field). His signature move is **renaming and re-framing** existing ideas ("multiplanetary," "X," "neural lace," "digital town square"). The latent tree's honesty badge - **origination vs amplification** - *changes the picture entirely* versus a flat "Elon Musk's ideas" rendering. This is a strong vindication of insisting the latent layer carry an attribution badge, not just a containment edge.

### 2b. The 2026 middle-layer collapse (a real topology change)

The latent tree's **middle layer collapsed in 2026** [MEASURED]: SpaceX acquired xAI (all-stock, Feb 2 2026), and xAI already contained X (acquired Mar 2025). So **three of the six ideas - Mars, AGI, and free-speech-platform - now nest under ONE physical parent** (SpaceX/"SpaceXAI"), which IPO'd June 12 2026. The strategic thread (orbital data centers fusing Starlink + Grok compute) **physically links the aerospace zone to the AGI zone** - the latent containment and the physical nesting literally converge.

---

## 3. The SEAM - where a physical event becomes a latent claim

The coupling seam is the **observation/assertion event**: the moment a physical happening is asserted into the latent tree (or re-routes its pointers). Catalogued seams in the Musk dataset:

| Seam event | Date | Physical side | Latent side (what gets asserted/re-pointed) | Badge |
|---|---|---|---|---|
| **Birth, Pretoria** | 1971 | a body at a place | the origin anchor of the *entire* latent tree | [MEASURED] |
| **Russian-ICBM price-shock** | 2001 | Musk pricing rockets in Moscow | the *reusability thesis* is born -> seeds SpaceX | [MEASURED] |
| **Falcon 9 first landing** | 21 Dec 2015 | a booster touching down at Cape Canaveral | "reusable rockets are real" becomes an asserted fact, not a claim | [MEASURED] |
| **Twitter acquisition closes** | Oct 2022 | a corporate-control transfer | the "digital town square" idea acquires a physical host | [MEASURED] |
| **xAI acquires X** | Mar 2025 | corporate merger | free-speech-platform pointer re-routes under xAI | [MEASURED] |
| **SpaceX acquires xAI ("SpaceXAI")** | 2 Feb 2026 | corporate merger | **Mars + AGI + free-speech all re-anchor to SpaceX/Starbase** - the single biggest seam | [MEASURED] |
| **SpaceX IPO** | 12 Jun 2026 | shares begin trading (Nasdaq SPCX) | the entire latent edifice gets a *single public price* -> Musk = first trillionaire | [MEASURED-VOLATILE] |
| **Starlink cutoff -> Ukrainian advance** | Feb 2026 | a switch flipped in orbit | infrastructural influence becomes a *measured* geopolitical fact (~400 sq km retaken) | [MEASURED] |

**Model finding (holds):** the seam concept is **non-trivially load-bearing**. The Feb 2026 merger is a textbook seam - a *physical* corporate event that *re-anchored three latent idea-pointers* up to a single physical parent. The viewer cannot represent the 2026 state correctly without modeling the seam as a first-class event that mutates the latent tree's edges. A static two-tree render would be *wrong* about 2026.

**[SPEC] subtlety:** seams are not symmetric. Physical->latent assertion (a landing "proves" reusability) is an *evidence* seam; the merger is a *re-pointing* seam (no new evidence, just topology). The model currently treats both as "the seam." These may be two seam *types* and the viewer might need to distinguish them.

---

## 4. The bit-slice atlas run (conceptual) - three passes

The atlas "slices" the entity at successive bit-budgets and asks what refines. Run conceptually over the Musk dataset.

### PASS-1 - Does ONE budget drive BOTH physical and latent refinement? (shared-budget test)

**Procedure:** spend a single increasing bit-budget and watch what sharpens, on both the physical and latent trees simultaneously.

- Budget ~2-4 bits: physical = "a person in the USA"; latent = "a tech entrepreneur." Both coarse.
- Budget ~7-10 bits: physical = "California + Texas operations"; latent = "rockets + cars + AI." Both refine **roughly in step**.
- Budget ~16-23 bits: physical = exact pad/factory coordinates resolve; latent = individual *ideas* with attribution badges resolve.

**Finding (partial hold, [ESTIMATE]):** a shared budget refines *both* trees, but **not at the same rate**. The physical tree has a **much higher ceiling** (govt pad coords ~23 bits) than the latent tree (idea attribution tops out ~MEDIUM-HIGH confidence, effectively a hard low ceiling because "who really originated AGI-safety" is *irreducibly* fuzzy). So a single scalar budget **drives both but saturates the latent tree early** while the physical tree keeps sharpening. **The trees are coupled at the base poset but have different bit-ceilings.** A naive shared-budget render would over-sharpen the latent tree past its evidence.

### PASS-2 - Physical <-> semantic middle: structured or spaghetti?

**Procedure:** examine the *middle* layers where physical sites meet semantic industries - is the mapping clean (a tree) or tangled (a DAG/spaghetti)?

**Finding (mixed - the model's most honest stress point):**
- **Structured where:** SpaceX -> aerospace -> {rockets, Mars} maps cleanly; Tesla -> automotive/energy -> EVs maps cleanly. Clean fibers.
- **Spaghetti where:** after Feb 2026, **SpaceX (one physical parent) -> {aerospace, AI, social-media} (three industries) -> {Mars, AGI, free-speech} (three ideas)**. One physical node now fans out to three industries. And the *person* attaches to ideas he didn't originate (the AMPLIFIER edges) - so the latent tree has **cross-links that are not containment but attribution**. It is **not a clean tree; it is a DAG with two edge-types** (contains vs originated-vs-amplified).
- **Orbital data centers** are the worst tangle: a *physical* product (data centers in space) that is simultaneously an aerospace artifact AND an AI artifact - **a single node that belongs to two fibers at once.**

**Verdict:** the physical-to-semantic middle is **structured at the leaves, spaghetti at the 2026-merged core.** The model's "two fibrations over one base" is *approximately* true but the base poset is not a tree - it is a poset with diamonds (the merger created a diamond: Musk -> SpaceX -> {xAI, aerospace}; xAI -> X). **The model should be stated as two fibrations over a shared base *poset/DAG*, not a base *tree*** - which, notably, is exactly how the keystone was phrased ("base poset"). So this is a *confirmation of the careful wording* and a *correction of any tree-shaped intuition*.

### PASS-3 - Does any zoomed-out aggregate render CRISPER than measured? (the aggregation cap / COIN-honest)

**Procedure:** zoom out and aggregate; check whether any summary value renders sharper than the measured bits of its constituents. The COIN forbids `rendered_sharpness > measured_bits`.

**Findings (the COIN is genuinely tested here, and mostly holds - with named violations to render as blur):**

1. **Net worth as a crisp scalar = a COIN violation if rendered sharp.** "$1.05T" *looks* like ~40 bits of precision but is a **[MEASURED-VOLATILE]** aggregate of live market caps that moved ~20% intraday on IPO day. **Honest render: a wide confidence blur, not a sharp number.** The aggregate is *less* certain than its appearance. **Aggregation cap engaged - render blurred.**

2. **"World's first trillionaire" as a binary = over-crisp.** It is a thresholded aggregate; on a slightly different market day the bit could flip. Render the *threshold-crossing* with blur, not as a hard fact. (It is currently *true and measured* on 2026-06-12/14, so render it as "true with a volatility halo.")

3. **Combined-entity valuation ($1.25-1.77T across sources).** Sources *disagree* by ~$500B. The honest aggregate is a **band, not a point** - rendering a single number would manufacture bits that no source has. **Aggregation cap engaged.**

4. **"Influence" as an aggregate is the deepest COIN trap.** Reach (impressions/followers ~230-237M, the only 200M+ account) is **[MEASURED]**. But "influence" (changed belief/behavior/price) is an **[ESTIMATE]** that is **sign-dependent per observer**: the *same* broadcast is +favorable to AfD voters (70%) / Reform UK (47%) and -unfavorable to the broad public (US ~53% unfavorable; Germany/Britain 71% unfavorable). **A zoomed-out "Musk influence" scalar would render crisper than measured AND would average away the sign.** This is a *flagrant* aggregation-cap violation if attempted. **Honest render: influence is a field with positive and negative lobes, never a single magnitude.** Plus the channel self-amplifies (~138% view / ~238% RT boost post-July-2024; ~80 engineers; algo open-sourced Jan 2026) - so even *reach* must be discounted to recover *organic* reach.

5. **Where the cap is NOT needed (COIN naturally satisfied):** government pad coordinates and factory street addresses aggregate up to "the SpaceX physical footprint" *without* over-crisping, because each constituent is independently sharp. Physical aggregates behave; **value/influence aggregates do not.**

**PASS-3 verdict:** the aggregation cap is **real and necessary**, and the Musk dataset contains **at least four live aggregates (net worth, trillionaire-binary, combined valuation, influence-scalar) that would each render crisper than measured if not blurred.** This is arguably the strongest empirical support for the COIN in the whole exercise: a real entity *spontaneously generates* over-crisp aggregates, and the honest viewer must blur every one of them.

---

## 5. Honest verdict - where the model holds and where it fails

**Holds:**
- Sharp lifecycle-origin point (Pretoria 1971) - confirmed, sharpest beat in the dataset.
- Continuous sharpness gradient over the lifecycle - confirmed.
- Late re-sharpening of dwelling inside a widening influence zone (the U-shape) - confirmed, elegantly.
- Org location = zone of influence, not a point - confirmed (X ~2 zone-bits is near-pure attention-output).
- Two independent bit-axes (site vs zone) that can invert - confirmed (Boring Company).
- Origination-vs-amplification attribution badge - **essential**; it overturns the naive "Musk's ideas" render.
- Seams as first-class tree-mutating events - confirmed (Feb 2026 merger).
- The aggregation cap / COIN - **strongly** confirmed; real entities spawn over-crisp aggregates.

**Fails / strains:**
- **Base is a DAG with diamonds, not a tree** (PASS-2). The 2026 merger and orbital-data-centers create nodes that live in two fibers at once. The keystone's "base poset" wording survives; any tree-shaped implementation would not.
- **The two trees have different bit-ceilings** (PASS-1). A single shared budget over-sharpens the latent tree, whose attribution is irreducibly fuzzy. The shared-budget assumption needs a per-fiber ceiling.
- **Latent edges are not all containment.** "Amplifier" edges are attribution, not containment - the latent tree mixes two edge semantics. [SPEC] this may need two edge-types.
- **Influence cannot be a scalar at all** (PASS-3 #4). It is observer-relative and sign-bearing. The model's "zone of influence" is correct in *shape* but the viewer must carry *valence-per-observer*, not just *location-bits*. This is a genuine extension the current spec does not name.

---

## 6. SPECULATION (disclosed) [SPEC]

- **[SPEC]** Seams have at least two types: *evidence* seams (a landing proves reusability) and *re-pointing* seams (a merger re-anchors idea-pointers with no new evidence). The viewer may need to color them differently; only evidence seams should raise an idea's measured_bits.
- **[SPEC]** The U-shaped dwelling-sharpness curve (sharp -> diffuse -> sharp) may be a *general* signature of a successful founder lifecycle, not Musk-specific: you start as a point, your influence diffuses as you scale orgs, and once influence is fully delegated to org-zones you can re-collapse your *personal* footprint (the tiny home) because your influence no longer needs your body anywhere in particular. If so, dwelling-sigma and influence-sigma are *anti-correlated* in late lifecycle - a testable cross-entity prediction.
- **[SPEC]** Valence (the +/- sign of influence per observer) might be a *third* coin alongside location-bits and render-sharpness: a "valence-bits" axis where low valence-bits = "we can measure he is salient but not whether he persuades." The negative-lobe/positive-lobe field would then be a *measured* object, not an estimate.
- **[SPEC]** The "naming/re-framing" move (multiplanetary, X, neural lace, town square) might be its own latent operation - a *relabel* edge that copies an existing idea-node under a new name with the original's bits intact. Musk's whole latent tree might be mostly relabel-edges over a small set of borrowed origin-nodes. If quantified, "fraction of an entity's latent tree that is relabel vs originate" could be a portable metric.

---

## 7. QUESTIONS WE SHOULD BE ASKING (register-shift: stepping back from the worked example to the apparatus itself)

*(This section deliberately changes register - from "does the model fit Musk" to "is the apparatus asking the right things at all.")*

- If a *real* entity's base is a DAG with diamonds and not a tree, is "two fibrations over a shared base" still the right primitive - or should the primitive be **one DAG with typed edges** (contains / originated / amplified / relabeled / re-pointed), with "physical" and "latent" as *projections* rather than separate trees? The two-tree framing may be a convenience that the data does not actually support.
- We treated "influence" as the place the model strains. But maybe **the COIN's deepest job is precisely to forbid scalar influence** - i.e. the aggregation cap is not a side-rule, it is *the* rule, and everything else (location-bits, lifecycle) is scaffolding for "do not render a fake bit, *especially* about how much a person matters." Are we under-selling the COIN by treating it as one of three jobs?
- Who is the **observer** in the Musk render? The whole influence layer is observer-relative (favorable to AfD, hostile to the broad public). The current spec has an "observer-global-kernel frame" - does the worked example *force* the observer into the base poset itself, so that the *same* entity has *different* latent trees per observer-frame? (This connects directly to the heredity/frame-relative-classifier memory: the +/- valence is a dial-setting, and frame-lock is what keeps it falsifiable.)
- Is "origination vs amplification" *itself* frame-relative? From a NASA frame, reusable rockets are NASA's idea Musk amplified; from a markets frame, Musk *originated* the *economic* version. The badge we treated as factual may be another dial.
- What would *falsify* the zone/lifecycle model? On Musk it mostly held - which should make us nervous. A model that fits a hand-picked rich-data subject proves little. What entity would *break* it, and should the next run deliberately pick a hostile case (an anonymous collective? a pseudonymous founder with no sharp origin point? an idea with no nameable originator)?

---

## 8. Open sub-questions for Pav

1. **Tree or DAG?** The data says the base is a poset *with diamonds* (the 2026 merger). Do you want the viewer's primitive to stay "two trees over a base," or move to "one typed-edge DAG with physical/latent as projections"? This is the load-bearing architecture choice.
2. **Per-fiber bit-ceilings?** PASS-1 showed the latent tree saturates early (attribution is irreducibly fuzzy) while the physical tree sharpens to ~23 bits. Should the shared budget carry a per-fiber ceiling so we never over-sharpen attribution?
3. **Valence as a third coin?** Influence is sign-bearing and observer-relative. Add a `valence_bits` axis (positive/negative lobes as a measured field), or keep influence purely as a location-blur and handle sign elsewhere?
4. **Two seam types?** Evidence-seams (raise measured_bits) vs re-pointing-seams (mutate topology only). Worth distinguishing in the spec?
5. **Hostile next subject?** Musk was a friendly, data-rich case and the model mostly held. Do you want the next run to target a *deliberately hostile* entity (pseudonymous founder / authorless idea / anonymous collective) to actually try to falsify the model rather than confirm it?
6. **The "relabel" operation** - is renaming/re-framing a first-class latent edge worth measuring (fraction of an entity's tree that is relabel vs originate)? Musk would score very high; it might be a portable signature.

---

## Sources

Core lifecycle/origin: [Elon Musk - Wikipedia](https://en.wikipedia.org/wiki/Elon_Musk); [Elon Musk and South Africa - Wikipedia](https://en.wikipedia.org/wiki/Elon_Musk_and_South_Africa). Physical zones: [SpaceX facilities](https://en.wikipedia.org/wiki/SpaceX_facilities); [Starbase](https://rocketlaunch.org/rocket-launch-sites/starbase-boca-chica); [SLC-40](https://en.wikipedia.org/wiki/Cape_Canaveral_Space_Launch_Complex_40); [Tesla factories](https://en.wikipedia.org/wiki/List_of_Tesla_factories); [Fremont](https://en.wikipedia.org/wiki/Tesla_Fremont_Factory); [Giga Berlin](https://en.wikipedia.org/wiki/Gigafactory_Berlin-Brandenburg); [Giga Shanghai](https://en.wikipedia.org/wiki/Gigafactory_Shanghai). Latent/ideas: [SpaceX-xAI merger - TechCrunch](https://techcrunch.com/2026/02/02/elon-musk-spacex-acquires-xai-data-centers-space-merger/); [Falcon 9 landing - NBC](https://www.nbcnews.com/tech/innovation/spacex-makes-history-successfully-launches-lands-falcon-9-rocket-n483921); [Mars paper - Scientific American](https://www.scientificamerican.com/article/elon-musk-publishes-plans-for-colonizing-mars/); [History of Tesla](https://en.wikipedia.org/wiki/History_of_Tesla,_Inc.); [Neuralink](https://en.wikipedia.org/wiki/Neuralink); [xAI - Contrary Research](https://research.contrary.com/company/xai). Influence/attention: [X followers - IBTimes](https://www.ibtimes.com.au/elon-musk-dominates-2026-ceo-x-followers-list-over-230-million-towering-over-tech-peers-1865188); [algo boost - The Conversation](https://theconversation.com/tech-billionaire-elon-musks-social-media-posts-have-had-a-sudden-boost-since-july-new-research-reveals-242490); [Civiqs favorability](https://civiqs.com/results/favorable_elon_musk); [YouGov Europe](https://yougov.com/en-gb/articles/51395-germans-and-britons-disapprove-of-musks-recent-interventions); [Starlink/Ukraine - Bloomberg](https://www.bloomberg.com/news/articles/2026-05-21/ukraine-retook-territory-after-hobbling-starlink-pentagon-says). Fresh-scan 2026 verification: [Musk trillionaire - CNBC](https://www.cnbc.com/2026/06/12/elon-musk-trillionaire-spacex.html); [SpaceX IPO net worth - Bloomberg](https://www.bloomberg.com/news/articles/2026-06-12/elon-musk-hits-1-trillion-net-worth-as-spacex-ipo-breaks-records); [Fox Business](https://www.foxbusiness.com/markets/spacex-ipo-elon-musk-trillionaire-net-worth); [Fortune - tiny home](https://fortune.com/2026/06/12/where-does-musk-live-spacex-stock-ipo-net-worth-trillionaire-homes-texas/); [xAI-SpaceX $1.25T - CNBC](https://www.cnbc.com/2026/02/03/musk-xai-spacex-biggest-merger-ever.html); [Motley Fool merger](https://www.fool.com/investing/2026/03/31/spacex-absorbed-xai-at-a-combined-125-trillion-val/).
