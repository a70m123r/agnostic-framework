# Fact Wrappers, the Excitation Probe, and the Observer (v0.3 conceptual layer)

**Date:** 2026-06-15 | **Status:** Tier-3 design. NOT built. Extends [SPEC.md](SPEC.md), [SCOPE_NESTING_LOD.md](SCOPE_NESTING_LOD.md), and the ratified refinements R1-R4.

This layer answers four things Pav raised, and fixes one category error:
1. **What every fact wrapper carries** - the scaffold axes ("the sphere of a fact").
2. **What an "origin / who-called-it" actually is** - retroactive, definition-relative, a fuzzy spike on an agreed record.
3. **How the instrument observes** - the excitation-emission keyhole probe (shine a concept in, see what pings back). This is the retrieval/observation model, and it is *spreading activation*.
4. **The person mind-sandbox** - a latent interior (inner canon + tribe) for a person-node.
Plus the taxonomy fix: **democracy is not the number 4**, and even some numbers (0) carry a zone.

The honesty spine is unchanged and load-bearing throughout: `rendered_sharpness(x) <= measured_bits(x)`; blur is the badge; never render a fake measured bit. The new content axes simply give the COIN **a separate ledger per axis**.

---

## 1. The fact wrapper: the sphere of a fact

### 1.1 The scaffold (answering "is there a better list?")

Every fact wrapper carries the **six honest axes** - Kipling's six serving-men, = 5W1H + Why:

```
WHAT   the thing/claim/predicate            (semantic content)
WHEN   time                                 (temporal)
WHERE  place / zone                         (spatial -> the zone-of-influence, R1)
WHO    actor(s) / attribution               (agent; for persons -> the mind-sandbox, sec 4)
HOW    mechanism / manner                   (instrument)
WHY    cause / intent / purpose             (the interpretive axis)
```

This is the canonical event scaffold and it is **near-optimal** - it is exactly what semantic-role labeling and event ontologies converge on (core roles agent/patient/source/goal + peripheral location/time/manner/cause; the six event "aspects": temporal, spatial, informational, experiential, structural, causal). It is deliberately simpler than full SRL/AMR; that simplicity is the point - it is the minimal complete set of axes a human or a renderer needs.

**The one principled addition the literature flags is WHOM** - the affected party / recipient / audience. In this architecture **WHOM is not a seventh content axis; it is the OBSERVER** (the glasses, sec 3.4). "Influence FOR whom," "perceived BY whom" - the recipient is the viewing pole, kept in a different stratum on purpose. So the wrapper has **six content axes + one observer axis (WHOM)**.

Two more things every wrapper carries, distinct from the content axes:
- **Link axes** `BEFORE` / `AFTER` - predecessor and successor pointers (Allen-style interval relations). These thread facts into worldlines / beat-chains. Pav: *"should be on every fact wrapper with when it happened before and what happened next."* A special case is `FROM` - "where the attention came from" - a provenance-direction link, not just a source citation.
- **Provenance / COIN metadata** - the existing substrate fields (`source{url,title,type}`, `route`, `certainty`) PLUS, now, **`measured_bits` PER AXIS** (sec 1.3).

### 1.2 The sphere: each axis spawns a latent FIELD and a CLASS

Pav: *"on a sphere of a fact it would form the axis of latent fields and classes."* Take it literally. A fact is a small sphere; the six axes are its poles. **Each pole spawns (a) a latent FIELD - the continuous render of that axis - and (b) a CLASS - the discrete category the axis sorts into.**

| Axis | Latent FIELD (continuous render) | CLASS (discrete sort) |
|------|----------------------------------|-----------------------|
| WHERE | the **zone of influence** (R1 per-channel kernel field) | region / jurisdiction / site-type |
| WHEN | the **lifecycle / diffusion** curve (origin -> spread) | era / stage (Hagerstrand primary/diffusion/condensing/saturation) |
| WHO | actor field; for a person, the **mind-sandbox** (sec 4) | role (founder/amplifier/opponent), tribe |
| WHAT | the semantic content embedding | type / ontology class |
| HOW | mechanism field | method / modality |
| WHY | the **intent/cause field** - structurally the **lowest-bit, blurriest axis** | motive / purpose class |

This is not a new decomposition bolted on - **the six axes ARE the per-channel COIN decomposition** the addendum already uses. R1 (per-channel prior) is "a prior per pole." The aggregation cap, chain-rule COIN, and the dial all apply per axis.

### 1.3 Per-axis measured_bits (the COIN, six ledgers)

The single most useful consequence: **each axis carries its own `measured_bits`**, so a wrapper is sharp on some poles and blurry on others, honestly.

- **WHERE-bits** -> `sigma_zone = 2^(-where_bits)` (the zone dial, R1/seam doc).
- **WHEN-bits** -> temporal blur (a date known to the year vs the decade).
- **WHO-bits** -> attribution confidence; capped by **Stigler's law** (a contested origin renders blurred even as a "point" - the contest is uncertainty about WHO, not WHERE).
- **WHAT/HOW-bits** -> semantic/mechanism sharpness.
- **WHY-bits** -> almost always the FEWEST. Intent and cause are interpretive; the WHY axis renders **blurriest by construction**, which is correct - we rarely *measure* why, we infer it. The COIN forbids a crisp WHY.

A wrapper's overall sharpness is per-axis, never a single scalar. "We know exactly WHERE and WHEN, roughly WHO, and can only guess WHY" is a normal, honestly-renderable state.

---

## 2. Origin is retroactive and definition-relative ("who called it")

### 2.1 The meaning drifts; the definition is time-indexed

Pav: *"who called it depends on its present definition; as we look back the meaning changes; what democracy was 1000 years ago is not what it is now."* This is **diachronic semantic drift** (Hamilton 2016; semantic-shift survey): an entity's definition is a **time-indexed trajectory** `D(t)` in latent space (broadening / narrowing / amelioration / pejoration). `democracy(t_now) != democracy(t_1000)`.

Consequence: **the entity's identity is the trajectory `D(t)`, not a fixed point.** "Who called it" is *not an absolute fact* - it is the answer **given a chosen definition epoch**, projected backward. Choose `D(2026)` and you get one origin story; choose `D(1789)` and you get another.

### 2.2 The "calling" event is a fuzzy spike on an agreed record

Pav: *"a person who called it - it's a fuzzy spike, an agreed-on record."* So the WHO/WHEN of an origin is:
- **FUZZY** - a spike with width, not a delta (low WHO-bits + WHEN-bits), and
- **INTERSUBJECTIVE** - a *consensus* record, not an objective measurement. The "agreed" badge means its certainty is social-consensus-grade, a distinct provenance class.

And the calling event is **not one fact but a bundle of sub-fields**, all of which Pav enumerated, mapped onto the axes:

| Pav's sub-field | Axis |
|---|---|
| when it became *known* / *used for utility* / *applied* | WHEN (three distinct beats) |
| when it got *attention* / *where the attention came from* | WHEN + WHERE + a `FROM` link |
| what *made* them call it (the trigger) | WHY / BEFORE |
| why they called it; what they *meant* | WHY + WHAT |
| how it was *perceived*, and why | HOW + WHY, **as seen through the observer (WHOM)** |

So an origin is a small cluster of wrappers (became-known, first-used, got-attention, ...), each with its own per-axis bits, threaded by BEFORE/AFTER - **a fuzzy multi-beat spike, not a yolk-point.** (This generalizes the egg-yolk origin of the seam doc to a **multi-yolk** origin field, which is exactly what an authorless idea like democracy needs - see sec 5.)

---

## 3. The excitation-emission keyhole probe (the observation model)

### 3.1 The idea, in Pav's words

*"You can apply democracy's [present] definition to the past and map its instances or core principles in unconnected spaces, places, singular events - the sparks. The lens of our instrument would be like a keyhole: only democracy emitting into the substrate, to see what gets excited and pings back."*

This is the **retrieval/observation primitive** of the whole instrument, and it has a precise name: **spreading activation** (Collins & Loftus 1975), in its 2025 knowledge-graph-RAG form (arXiv 2512.15922). It also reads as **fluorescence excitation-emission**: shine a narrow excitation wavelength in, record what fluoresces back.

### 3.2 The mechanism

```
PROBE P = a concept defined as a weighted region across the six axes,
          time-indexed to a definition epoch:  P = D(t_def)
          (e.g. democracy's core principles: rule-by-the-governed,
           contested/alternating power, ... as a query over WHAT/HOW/WHY)

EXCITE  : seed the substrate DAG with P; compute resonance
          r(P, w) = match(P, w) across the axes' latent fields,
          then SPREAD activation along typed edges (decaying per hop).

EMIT    : excited wrappers PING BACK. Ping intensity of wrapper w:
          emit(w) = r(P, w) * activation(w)         capped by the COIN:
          rendered_ping(w) <= measured_bits(w)
          (a faint, weakly-attested old spark CANNOT render bright)

SPARKS  : the lit set = instances / principle-matches across DISCONNECTED
          space-time - even where the thing was never *called* democracy,
          even with no causal link between them. The sparks are the answer.
```

The substrate stays the agnostic measured medium; the **probe is the active light**; the **pings are the emission**. This **inverts** the keystone's "substrate = light on a sensor": there the world emits and the sensor records; here **the observer emits the concept-light and the substrate fluoresces back.** Both obey the COIN.

### 3.3 Why "keyhole" is the honest word

You see only through the **narrow aperture of the probe**. The substrate is vast; only the resonant subset emits. **Change the probe -> a different constellation of sparks lights up. Change the definition epoch `D(t_def)` -> the same substrate yields a different history.** Project `D(2026)` onto antiquity and you get a *presentist* reading (honest, if badged: "what WE would now recognize as democratic"); project `D(1789)` and Athens lights differently. The keyhole makes the definition-relativity of sec 2 operational and **visible**: the instrument never claims a view-from-nowhere; it shows you what *your chosen concept-light* excites, and says so.

**Honesty rules for the probe:**
- Badge the **definition epoch** `t_def` of every probe (a presentist projection must be labelled).
- The ping obeys the per-axis COIN: an old sparse spark stays dim; you cannot brighten history you did not measure.
- A spark is an **instance match, not a causal claim** - "resonates with the principles" is rendered distinct from "descends from" (a CONTAINS/ORIGINATED edge in the DAG). The instrument lights principle-kin and lineage-kin in different channels.

### 3.4 Frame agnostic, glasses = observer, and the back-reaction

Pav: *"the frame is agnostic, the glasses are the observer, and what we observe through that slice has influence on the global dynamics."*

- **FRAME = agnostic substrate** - the DAG of wrappers + their measured bits. Observer-neutral. The base.
- **GLASSES = the observer** - the probe `P`, the definition epoch `t_def`, the per-observer budget (foveation), the valence sign (R3), and the WHOM axis. The glasses are *the decoder `q`* the philosopher named; "whose accounting are we rendering?" is a glasses setting.
- **BACK-REACTION (load-bearing, [SPEC]):** observing through a slice **influences the global dynamics**. Two reasons: (a) *definitional* - choosing the probe defines what counts as an instance, which reshapes the entity's measured extent (you partly make the thing by how you query it); (b) *causal in a live social substrate* - attention is causal; naming and surfacing instances feeds the concept's own spread. So the instrument is **participatory, not passive**, and that participation must be **badged** - the slice you chose is part of the record, never a neutral window. (This is the agnostic-instrument frame: an exploratory INSTRUMENT, not a confirmatory test; 0.99-not-Boolean; the frame-reversal of solid<->fuzzy is itself an observable.)

---

## 4. The person mind-sandbox (a latent interior)

Pav: *"for a person like Musk we need to create an approximation of his wrapper's mind sandbox based on facts of what he said and what he does - distil a model of his core inner canon and his tribe / inner circle."*

A person-node gains a **latent interior**, on the WHO pole:

```
mind_sandbox(person) = {
  inner_canon : a modelled belief/value/worldview distilled from SAID + DID
                (utterances + actions over the lifecycle; a diachronic D(t)),
  tribe       : the inner-circle graph (who they trust/coordinate-with;
                CONTAINS-member / role edges in the DAG),
}
```

It is **a probe source**: you can shine `inner_canon(Musk)` into the substrate (sec 3) and see what resonates - his *predicted* positions, his likely allies/opponents, what he would call a thing. That is genuinely useful (anticipation, the scene's projections).

**Honesty (this is the most fake-bit-prone construct in the whole system, so the badge is loudest):**
- The mind-sandbox is **Stratum-2, modelled, never measured.** It is a *caricature with disclosed uncertainty*, not a readout of a mind. Render it dashed/hazy, always badged `MODELLED INTERIOR`.
- Its bits come only from SAID + DID. The **gap between SAID and DID is itself a measured signal** (an aspiration-vs-action delta) - render the delta, do not average it into one "what he believes."
- It is **observer-relative** (a rival's model of Musk's canon differs from a fan's) - it is a glasses setting, carries valence (R3), and must say *whose* model it is.
- It drifts: `inner_canon = D(t)` - a diachronic trajectory, not a fixed creed.

---

## 5. Taxonomy fix: democracy is not the number 4 (and 0 has a zone)

The earlier framing ("democracy ~ the number 4 ~ `kappa -> 0`, locationless") was a **category error**. The decision Pav already ratified (R1, the per-channel population prior) is what corrects it:

- `kappa` against the **population prior** measures *excess* concentration over where people already are.
- **The number 4**: taught/written wherever people are -> footprint ~ population -> `kappa ~ 0`. Demographically flat, not profound. (As a *formal* object; see below.)
- **Democracy**: wildly non-uniform over population - concentrated in some polities, contested in hybrids, *opposed* in autocracies -> **high `kappa`**, with `+`/`-` **valence lobes** (R3). A load-bearing structure: a high-in-degree DAG hub with subtypes (Athenian/representative/liberal/social/illiberal) as ORIGINATED children, each with its own origin spike and diffusion wave (Huntington's waves = Hagerstrand at civilizational scale), trackable against real measured indices (V-Dem/Polity/Freedom House).

**The honest taxonomy is a spectrum of latent anchoring:**

```
formal-content object        socio-historical structure        concrete entity
(number 4, empty set)         (democracy, capitalism, 0)        (a person, a company)
kappa ~ 0, demographically    rich SIGNED multi-modal zone,     sharp nucleus + tail
flat; RARE (math/logic)       subtypes, lifecycle; the NORM     (Musk = a comet)
```

**And even a number can have a zone.** Pav: *"there are numbers that have cult followings and historical drama - re number 0."* Zero is the proof: as a *formal* object its usage is flat, but as a **socio-historical entity** it has a real origin (India, ~5th-7th c.), resistance (medieval European suspicion), and a diffusion zone - a genuine `kappa > 0` lifecycle. The distinction is **formal-content vs social-instantiation**, and the **probe (sec 3) chooses which one you light**: a formal-content probe of "0" lights flat; a social-instantiation probe of "0" lights its dramatic history. Same substrate, two keyholes.

---

## 6. What this changes in the spec (summary)

- Every **fact wrapper** = six content axes (WHAT/WHEN/WHERE/WHO/HOW/WHY) + the observer axis (WHOM) + BEFORE/AFTER links + per-axis `measured_bits`. The axes ARE the per-channel COIN; WHY is the structurally-blurriest axis; WHO carries the Stigler cap.
- **Origin** is retroactive + definition-relative + a fuzzy multi-beat spike on an *agreed* (intersubjective) record; the entity's identity is its diachronic definition trajectory `D(t)`.
- **Observation** is the excitation-emission keyhole probe (spreading activation): shine a time-indexed concept-light into the agnostic substrate, the resonant wrappers ping back as sparks, the ping obeys the per-axis COIN, and the act of probing **back-reacts** on the global dynamics (participatory instrument, badged).
- **Glasses = observer/decoder** (probe + epoch + budget + valence + WHOM); **frame = agnostic substrate**.
- **Person-nodes** gain a **mind-sandbox** (inner canon + tribe), a Stratum-2 probe-source with the loudest honesty badge and a measured said-vs-did delta.
- **Taxonomy:** the `kappa` spectrum (formal-content / socio-historical / concrete); R1 separates "4" from "democracy"; the probe chooses formal-content vs social-instantiation (zero's two keyholes).

**Prior art grounding:** 5W1H / semantic-role labeling / event ontologies (the scaffold); spreading activation - Collins & Loftus 1975, KG-RAG revival arXiv 2512.15922, creativity-from-text-networks 2026 (the probe); diachronic word embeddings - Hamilton 2016, semantic-shift survey ACL C18-1117 (definition drift `D(t)`); LLM concept-probing 2024-2025 (the mind-sandbox as a distilled model, badged Stratum-2).

**Still open / deferred:** the strength x type coupling unification (R4); the estimator-soundness gap; a HOSTILE falsification subject (an authorless idea like democracy is the natural one - it stress-tests the multi-yolk origin and the no-nucleus zone at once). A cross-model (codex + gemini) external pass on this v0.3 layer is the standing next A-minus.
