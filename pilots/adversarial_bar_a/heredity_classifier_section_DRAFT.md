# Heredity — operational definition (§H of the Brief-2 pre-registration)

**Status:** DRAFT section, surfaced for Pav's ratification. Tier-3. **NOT locked. NOT the census-run.** No data examined; no SHA/git lock ceremony performed (that happens at census-run if Pav steers P1).

This is the `heredity-bearing-vs-not` operational-definition slot of the eventual `PILOT_outcome_blind_basrate_census_PRE_REGISTRATION.md`, written in the **frame-relative-classifier** form per Pav's 2026-06-11 steer:

> *"it's all of those per frame view and is observer plane dependant so a classifier not a fact, current standing measurement and is agnostic, like a dial or a toggle that you can switch and examine the result of, compare and eval."*

The rest of the pre-reg (sampling frame, niche-presence classifier internals, "first opportunity", estimator choice, substrate list) lives in sibling sections — see §H.10.

---

## H.0 — The reframe (one line)

Heredity is **not a property a substrate has.** It is a **reading a classifier returns under a chosen instrument-setting** — observer-, plane-, and frame-dependent; a *current-standing measurement*; agnostic; provisional to the instrument. The census never asserts "substrate X is hereditary." It records *what the heredity-classifier reads at each locked setting*, and the science is in the **sweep, the comparison, and the co-variation** with the niche-presence reading.

---

## H.1 — The dial: the instrument's settings (the axes you switch)

A single reading is `C(substrate | plane, observer, frame) → ⟨Q, toggle⟩`. Three settable axes:

| Axis | What you're switching | Declared positions (the locked grid) |
|---|---|---|
| **plane** | which medium the lineage lives in | `physical` (pattern in matter) · `latent` (pattern in representation) |
| **observer** | who/what individuates the replicating unit | physical: `molecular-replicator` · `cell` · `organism` · `population` · `institution` — latent: `individual-mind` · `community` · `canon` |
| **frame** | what counts as a "copy event" + a "lineage" | `strict-replicator` (Dawkins copy-with-fidelity) · `broad-reproducer` (any regeneration of form) · `information-channel` (Shannon transmission of state) |

The grid = the full set of {plane × observer × frame} positions the census will sweep. **The grid is pre-declared and locked** (H.6). No position may be added after data.

> **Open design fork for Pav:** your observer schema also carries a *mode* axis — `{neutral · dormant · passive · active · reactive}`. It can be a **4th dial axis** (richer, bigger grid) or held fixed at one mode for v0 (tractable). Flagged, not decided. Defaulted OFF in this draft.

---

## H.2 — The two output modes (dial and toggle)

At each setting the classifier evaluates the three Lewontin clauses — (i) a replicated entity with variation, (ii) differential persistence under selection, (iii) **transmission of that variation across copy events** (the gate) — and returns:

- **Dial (continuous): `Q` ∈ [0,1]** = measured transmission fidelity = the probability that a variant state of the parent is carried into the copy *under this setting's copy-event definition*.
  *(Plain: when the parent differs, how reliably does the child inherit the difference?)*
- **Toggle (binary, derived):** compare Q to the **error threshold `Q_c = 1/a`** (`a` = selective advantage of the master variant under this setting — your own Eigen handle):
  - **`ABOVE-GATE`** if `Q > Q_c` — variation localizes into a lineage; cumulative selection runs.
  - **`BELOW-GATE`** if `Q ≤ Q_c` — variation smears out (error catastrophe); no persistent lineage.
  - **`UNDEFINED`** if clause (i) fails — there is **no individuable replicated entity** under this setting, so transmission has no referent (the analogue of "no q to deceive" at the molecular floor in §C2.2-B).

A reading is the triple `⟨setting, Q, toggle⟩`, e.g. `⟨physical/molecular-replicator/strict-replicator, Q≈0.97, ABOVE-GATE⟩`.

---

## H.3 — Per-plane copy-event definitions (the measurable meat)

**Physical plane.** Copy event = material replication (template-directed polymerization, cell division, manufacture, institutional reproduction). Variation-transmission = a perturbation to the parent *structure* recurs in the daughter structure. `Q` estimated from the per-copy error/retention rate of the substrate's own replication machinery.
*Below-gate / undefined exemplars:* a single star, a hurricane, a Bénard cell — they regenerate order but no individuated unit carries *variation* forward → clause (i)/(iii) fail → `UNDEFINED` or `BELOW-GATE`. (These are the §5.1-R clean negatives, now expressed as classifier readings rather than asserted facts.)

**Latent plane.** Copy event = **re-rendering across observers**: A externalizes a representation, B internalizes and re-expresses it (your observe→internalize→metaphor channel). Variation-transmission = a deliberate modification by A survives into B's re-rendering and onward. `Q` estimated by a **transmission-chain measurement** — seed a marked variant, pass it through N independent re-renderings, measure how faithfully the variant survives.
**The §3.3-T discriminator *is* this gate:** *latent transposition* (observe → carry forward) = `Q > 0`, lineage present; *harness-convergence* (same optimizer re-invents independently, no carry) = `Q ≈ 0`, `UNDEFINED`/`BELOW-GATE` even though the surface forms match. This is what stops parallel re-invention from being mis-scored as inheritance.

> **Coupling note.** Latent lineages typically ride a physical anchor (the artefact-viroid: latent payload, physical anchor, observer as replication host). The two fidelities are **separable** and are read as **separate cells**, never blended into one.

---

## H.4 — The result-unit is a SWEEP, not a verdict

For each substrate the census fills the whole locked grid → a **heredity profile**: a table of `setting → ⟨Q, toggle⟩` across all positions. A substrate is **not** "hereditary / non-hereditary"; it has a *pattern*. The profile *is* the measurement.

Illustrative profile (NOT locked called-shots — shape only):

| Substrate | physical / molecular-replicator / strict-replicator | latent / community / information-channel | physical / institution / broad-reproducer |
|---|---|---|---|
| RNA-world autocatalytic sets | Q≈0.95 · **ABOVE** | UNDEFINED (no representation) | UNDEFINED |
| Oral epic tradition | UNDEFINED (no molecular replicator) | Q≈0.70 · **ABOVE** | BELOW / UNDEFINED |
| Hurricane field | UNDEFINED | UNDEFINED | UNDEFINED |
| Open-source software ecosystem | UNDEFINED | Q≈0.90 · **ABOVE** (forks carry diffs) | Q≈0.80 · **ABOVE** (orgs reproduce) |

Note the point of the whole reframe: the oral tradition reads **above-gate latently** and **undefined physically** — one bit could never have said that.

---

## H.5 — Called-shots (locked predictions, before any data)

For every `substrate × setting` cell the framework records, **before data examination**, its predicted reading and (where it commits) a predicted `Q` band. These are the falsifiable called-shots (frame-lock-pilot pattern). A cell where the framework declines to predict is logged `NO-CALL` (counts against coverage, never for the claim).

```yaml
- cell:
    substrate: oral_epic_tradition
    setting: latent/community/information-channel
  predicted_toggle: ABOVE
  predicted_Q_band: [0.50, 0.85]
  rationale_tag: "transmission-chain re-rendering carries marked variants; transposition not convergence (§3.3-T)"
```

---

## H.6 — Frame-lock binding (what makes the dial a measurement, not relativism)

The single discipline that keeps "a classifier, not a fact" honest: **the dial is the thing you lock.** Frame-relativity *without* frame-lock is unfalsifiable — you could twiddle settings post-hoc until any substrate reads the way you want. So, per `frame_lock_protocol_DRAFT.md` §7 (demonstrated in `frame_lock_pilot_RESULTS.md`), the lock file records, on its own pre-data commit:

- the full setting grid (H.1)
- the per-plane copy-event definitions + the `Q` and `Q_c` estimators (H.2–H.3)
- every called-shot (H.5)
- the §5.1-R scoring rule + thresholds (H.7)

…then `sha256(lock_brief_2.yaml)` is recorded in this section's header **and** the lock commit message; at result-commit the hash is recomputed-and-matched and `git merge-base --is-ancestor <lock_commit> HEAD` is verified. **Ceremony performed at census-run, not now.**

```yaml
# lock_brief_2.yaml  — SCHEMA ONLY (instantiated + hashed at census-run, not in this draft)
lock_version: 1
sha256_self: "<computed at lock time; recorded in header + commit msg>"
grid:
  planes: [physical, latent]
  observers:
    physical: [molecular-replicator, cell, organism, population, institution]
    latent:   [individual-mind, community, canon]
  frames: [strict-replicator, broad-reproducer, information-channel]
  observer_mode_axis: off          # H.1 fork; flip on only if Pav wants the 4th axis
estimators:
  Q_physical: "per-copy retention rate of the substrate's replication machinery; method TBD"
  Q_latent:   "transmission-chain fidelity over N independent re-renderings; method TBD"
  Q_c:        "1/a; a = selective advantage of master variant under setting; method TBD"
called_shots: [ ... see H.5 ... ]
scoring:
  tau_pass: <to set by Pav/Cowork>
  tau_fail: <to set>
  effort_proxy_floor: <to set>
  first_opportunity_lag_tolerance: <to set>
discipline:
  matched_settings_required: true
  report_all_cells: true
  on_fail: "CLAIM_LIFECYCLE: parent PARKED; this operationalization = dead child; +1 tally; claim text frozen"
```

---

## H.7 — How §5.1-R is scored against the sweep

The bounded claim — *every substrate above the heredity gate grows a beneficiary-bearing adversarial niche, essentially at the first opportunity* — is tested as **co-variation of two swept instruments read at matched settings**:

- **Instrument 1** — the heredity toggle (this section).
- **Instrument 2** — the niche-presence classifier (sibling section), read at the **same setting**.

Pre-committed scoring (thresholds are placeholders for Pav/Cowork):
- **PASS** if, across the locked grid, `ABOVE-GATE ⇒ niche-present` and `BELOW-GATE/UNDEFINED ⇒ niche-absent` hold at ≥ `τ_pass` concordance, *after* effort-detrending (exogenous detection proxy ≥ floor in every counted cell).
- **FAIL** if the two instruments decouple beyond `τ_fail` (niches read present below-gate, or absent above-gate, past tolerance).
- **INCONCLUSIVE** if detection effort is too uneven (proxy below floor) to read a cell — reported, never silently dropped.

**"At the first opportunity"** enters as the **ordinal companion**: along any ordered observer/rung axis, the claim predicts niche-present appears at the *same* rung the toggle first flips `ABOVE`, not k rungs later (lag = 0 within tolerance). Full operationalization deferred to the sibling section.

---

## H.8 — Anti-gaming rules (baked into the lock)

1. **Matched settings.** Heredity and niche-presence for a given cell are read at the *identical* setting — no reading heredity in `latent/community` and niche in `physical/organism` for the same cell.
2. **No cherry-picking.** Every grid cell is reported; dropped/`UNDEFINED` cells are logged with reason (no silent truncation — the "covered everything" illusion is the failure mode this prevents).
3. **On FAIL, CLAIM_LIFECYCLE discipline.** Parent (§5.1-R conjecture) → PARKED, dated, with revisit-trigger. *This* operationalization (this grid + these proxies + these `Q`-estimators) = the dead child, retired with reason, **+1** to the §5.1-R dead-children tally. The bounded-claim text stays frozen; "re-tune the estimator" costs +1 child, never resets the count.

---

## H.9 — Honest scope

The physical-plane half rests on established machinery (Lewontin units-of-selection; Dawkins replicator; Eigen error-threshold / quasispecies). The **latent-plane transfer** — that the *same* gate structure and the `Q / Q_c` math carry to re-rendering-across-observers — is **Tier-3 framework conjecture**, not settled. The classifier is built so this is *testable* (latent `Q` is a measurable transmission-chain quantity), not assumed. **Cross-model external A− (GPT-5.5 + Gemini) owed on this section before the lock hardens.**

---

## H.10 — Deferred to sibling pre-reg sections (scope honesty)

- Sampling frame + the **exogenous detection proxy** — the census denominator, the genuinely hard part.
- The **niche-presence classifier's** own internals (Instrument 2).
- **Estimator choice** — Chao1 vs Chao2 / ICE / capture-recapture; likely incidence/recapture given heterogeneous detection effort across domains (see prior analysis).
- Full **"first opportunity"** operationalization.
- The **substrate enumeration** list.

---

*Provenance: drafted 2026-06-11 by Claude Code at Pav's request, reframing the §5.1-R heredity gate per his classifier-not-a-fact / dial-or-toggle steer. Tier-3, surfaced for Pav+Cowork ratification. Nothing locked, nothing run, no canon touched, convergence list still 9.*
