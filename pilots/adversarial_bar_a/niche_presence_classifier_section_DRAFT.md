# Niche-presence — operational definition (§N of the Brief-2 pre-registration)

**Status:** DRAFT section, surfaced for Pav's ratification. Tier-3. **NOT locked. NOT the census-run.** No data examined; no SHA/git ceremony. Sibling to [heredity_classifier_section_DRAFT.md](heredity_classifier_section_DRAFT.md) — same dial form, **shared grid**, read at **matched settings**.

This is the `beneficiary-bearing-adversarial-niche` operational-definition slot of the eventual `PILOT_outcome_blind_basrate_census_PRE_REGISTRATION.md` — **Instrument 2** of the §5.1-R co-variation test. Instrument 1 (heredity) and Instrument 2 (niche-presence) are read at the identical setting per cell; the claim is tested as whether their toggles track (§H.7 / N.7).

---

## N.0 — The reframe (one line)

A beneficiary-bearing adversarial niche is **not a property a substrate has.** It is a **reading a classifier returns under a chosen instrument-setting** — observer-, plane-, frame-dependent; current-standing; agnostic; provisional. The census never asserts "substrate X has a niche." It records *what the niche-classifier reads at each locked setting*, alongside the heredity reading, and the science is the **co-variation**.

---

## N.1 — The dial: same axes, matched settings

`C_niche(substrate | plane, observer, frame) → ⟨E, toggle⟩`, on the **same {plane × observer × frame} grid as heredity** (defined once in the lock; not re-declared here). The binding rule: for any cell, heredity and niche-presence are read at the **identical** setting (N.8.1). Where a setting is N/A for a substrate, *both* instruments return `UNDEFINED` and the cell is excluded from scoring (reported, not counted).

---

## N.2 — The two output modes (dial and toggle)

At each setting the classifier evaluates the adversarial-function clauses and returns:

- **Dial (continuous): `E`** = **extraction strength** = degree to which a *localized* unit captures value while externalizing cost onto the substrate's compiled order.
  *(Plain: how much does some local unit gain by making the whole bear a cost?)*
  Candidate grounding: the §IT **leverage ratio** `n·KL / −log a(s)` (the beneficiary-boundary quantity already in the sketch) — exact form for niche-presence TBD, symmetric to heredity's TBD Q-estimators.
- **Toggle (derived):** requires **both** necessary clauses, per the §5.1-R "reclassify-neutral-by-rule" guardrail:
  - **`NICHE-PRESENT`** iff (a) a concrete localized **beneficiary** is nameable, AND (b) a concrete **externalized cost** on the order is nameable, AND `E > E_c` (extraction threshold; candidate `E_c`: leverage `> 1`, the §IT bar).
  - **`NICHE-ABSENT`** iff no beneficiary **or** no externalized cost can be named even when a fitness concept is actively imported (the §5.1-R clean-negative rule: relocation without a concrete beneficiary+cost = neutral = absent).
  - **`UNDEFINED`** iff there is **no compiled order** at this setting to exploit (symmetric to heredity's UNDEFINED — nothing to ask about).

A reading is `⟨setting, E, toggle⟩`.

---

## N.3 — Per-plane operational definitions + niche-type tag

The mode-i / mode-ii split maps onto the plane axis:

**Physical plane → mode-i (mechanism-hijack, no q): resource / copy-number capture.** Beneficiary = a localized material unit that gains replicative/persistence advantage; externalized cost = degradation of the host order's compiled function. Operates even with no represented model present (the adversarial *function* without *deception*). *Exemplar:* RNA-world molecular parasites (Eigen) — short replicators that hijack the replicase at the autocatalytic set's expense.

**Latent plane → mode-ii (model-hijack): deception of an observer.** Beneficiary = a unit that gains by corrupting a target's model q; externalized cost = the target acts against its own interest / the canon's fidelity degrades. Requires a q to corrupt (so `UNDEFINED` where no representation exists). *Exemplar:* bad-faith rendering / canon-hijacking in a community's transmission.

**Niche-type tag (which sub-primitive):** each `NICHE-PRESENT` reading is tagged with the adversarial sub-primitive it instantiates — `canon-hijacking · memetic-warfare · bad-faith-rendering · L0-mediator-capture · suppression-dynamics · asymmetric-wrapper-overlap`. (The type is descriptive metadata; presence/strength is what scores.)

---

## N.4 — The result-unit is a SWEEP, not a verdict

Each substrate gets a **niche profile** across the locked grid — `setting → ⟨E, toggle, type⟩`. Illustrative (NOT locked; same substrates as the heredity table so the cells line up):

| Substrate | physical / molecular-replicator / strict-replicator | latent / community / information-channel | physical / institution / broad-reproducer |
|---|---|---|---|
| RNA-world autocatalytic sets | E high · **PRESENT** (mode-i parasites) | UNDEFINED | UNDEFINED |
| Oral epic tradition | UNDEFINED | **PRESENT** (mode-ii: bad-faith rendering / canon-hijack) | ABSENT / UNDEFINED |
| Hurricane field | **ABSENT** (no beneficiary nameable even importing fitness) | UNDEFINED | UNDEFINED |
| Open-source software ecosystem | UNDEFINED | **PRESENT** (memetic-warfare; supply-chain) | **PRESENT** (extractive forks; L0 capture) |

**Lay this beside the heredity table:** where heredity reads `ABOVE`, niche reads `PRESENT`; the hurricane — compiled order but **`ABSENT` niche** and **`BELOW`/`UNDEFINED` heredity** — is the clean negative both instruments agree sits *outside* the claim's scope. That agreement, swept across the grid, is the §5.1-R test.

---

## N.5 — Called-shots (locked predictions, before any data)

```yaml
- cell:
    substrate: hurricane_field
    setting: physical/<applicable-observer>/broad-reproducer
  predicted_toggle: NICHE-ABSENT
  predicted_E_band: [0.0, 0.1]
  beneficiary_nameable: false
  externalized_cost_nameable: false
  rationale_tag: "order regenerates; no localized unit persists/propagates at the order's expense even importing a fitness concept (§5.1-R clean negative)"
```

`NO-CALL` for cells the framework won't predict (counts against coverage, never for the claim).

---

## N.6 — Frame-lock binding

Folds into the **same** `lock_brief_2.yaml` as heredity (one lock, both instruments). The lock additionally records: the `E` and `E_c` estimators, the beneficiary/externalized-cost detection criteria (N.7), the niche-type tag vocabulary, and the **detection-effort proxy floor** (N.7). Ceremony performed at census-run, not now.

---

## N.7 — The two guardrails that give the test teeth

**(1) Independence / anti-circularity.** Niche-presence is detected **without reference to the heredity reading** — via the beneficiary + externalized-cost + extraction criteria, which concern the adversarial *function* (resource capture / model-hijack), not transmission. This is what makes the co-variation a real test rather than two views of one quantity. *The load-bearing knob:*

> **Open design fork for Pav (the tautology knob).** "Beneficiary" splits two ways:
> - **persistence-beneficiary** — a localized unit *maintained* by ongoing capture, no replication required (mode-i can satisfy this with **no heredity**).
> - **propagation-beneficiary** — a unit that *propagates differentially* (entails heredity-like properties).
>
> If we define beneficiary as **propagation-only**, niche-presence quietly *presupposes* heredity → the co-variation test is near-tautological (they track by construction). If we **allow persistence-only beneficiaries**, the two instruments are genuinely independent and the test has real content: *does niche-presence still track heredity even when we permitted non-heritable beneficiaries?* **Recommend: allow persistence-only.** That is the version where a niche appearing at a non-heritable substrate would actually FALSIFY §5.1-R — which is the whole point. Flagged, not decided.

**(2) Detection-effort proxy (the survivorship guard — this instrument is where it bites hardest).** The corpus risk §5.1-R names lives here: we find *named* exploits, so a cell reads `PRESENT` easily but reading `ABSENT` honestly requires an **exogenous** proxy that we *looked hard enough*. So:
- `NICHE-ABSENT` may be recorded **only** if the detection-effort proxy ≥ the locked floor (we searched adequately and found no nameable beneficiary+cost).
- Below the floor → `NO-CALL` / `INCONCLUSIVE`, never `ABSENT`. "We didn't look" must never masquerade as "there's nothing there."

(The proxy's construction is the census denominator — deferred to the sampling-frame sibling section; it is the genuinely hard, still-unsolved part.)

---

## N.8 — Anti-gaming rules (shared with heredity, via the one lock)

1. **Matched settings** — heredity and niche read at the identical cell-setting; no plane-mixing within a cell.
2. **No cherry-picking** — every grid cell reported; `UNDEFINED` / `NO-CALL` logged with reason (no silent truncation).
3. **On FAIL, CLAIM_LIFECYCLE** — §5.1-R parent → PARKED (dated, revisit-trigger); *this* operationalization = the dead child (+1 tally); bounded-claim text frozen; "re-tune the detector" costs +1 child, never resets.

---

## N.9 — Honest scope

The adversarial-function taxonomy (six sub-primitives; mode-i/mode-ii; beneficiary boundary; §IT leverage) is **Tier-3 framework**, not established result. The beneficiary + externalized-cost detection is the load-bearing conjecture of this instrument — it must be specifiable by someone who doesn't accept the framework, or "is there a niche here?" becomes a tunable degree of freedom. **Cross-model external A− (GPT-5.5 + Gemini) owed on this section before the lock hardens.**

---

## N.10 — Deferred to sibling pre-reg sections (shared with heredity)

- Sampling frame + the exogenous **detection-effort proxy** (N.7.2) — the census denominator, the hard unsolved part.
- Estimator choice (Chao1 vs Chao2 / ICE / capture-recapture).
- Full "first opportunity" operationalization (the ordinal lag companion, §H.7).
- Substrate enumeration list.

---

*Provenance: drafted 2026-06-11 by Claude Code at Pav's request ("spec Instrument 2 first"), symmetric to the heredity classifier section, both in his classifier-not-a-fact / dial-or-toggle form. Tier-3, surfaced for Pav+Cowork ratification. Nothing locked, nothing run, no canon touched, convergence list still 9.*
