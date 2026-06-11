# REVISION v1 — the two upstream fixes (scoring statistic + corpus/schema-fit)

**Status:** DRAFT, Tier-3, surfaced for Pav's steer. **Nothing locked/run; convergence list still 9.** Proposes replacements for the two **upstream** blocking faults in `REVIEW_v1.md` (B1 + B3, plus the PM1/PM2/PM3/BS2/BS3/M3/M4/PM4 cluster that hangs off them). **Not yet applied** to the instrument DRAFTs — those stay as the review's referents until these resolutions are ratified. The remaining review items (B2 de-circularization, M1 blinding, M5 estimators, M2 confounds, BS1 budget-K, register edits) are **downstream** and deferred to REVISION v2.

Why these two first: every other scoring critique is downstream of *"what statistic, computed over what corpus"* — both currently undefined. Fix these and the rest become local edits; leave them and the rest float.

---

## FIX 1 — The scoring statistic (replaces heredity §H.7 wholesale)

**The problem (B1 + PM1):** "concordance" was never defined; as implied (raw cell-agreement) it is dominated by the co-UNDEFINED diagonal and a base rate of PRESENT → 1, so it can almost only PASS/INCONCLUSIVE.

**The replacement — a conditional contrast with a permutation null.**

**1.1 Eligible cells.** A cell `(substrate × observer × plane × copy-lens)` is **scorable** iff BOTH instruments are DEFINED there (neither UNDEFINED). Any cell where either reads UNDEFINED is **out-of-scope**: tabulated separately, *cannot move PASS/FAIL*. (Resolves the H.7-vs-N.1 contradiction, M4: co-UNDEFINED is never "concordant agreement.")

**1.2 The statistic.** §5.1-R's co-presence arm predicts niche-presence tracks heredity-ABOVE among scorable cells. Score the **risk contrast**

```
Δ = p_above − p_below
  p_above = P(niche-PRESENT | heredity-ABOVE  & scorable)
  p_below = P(niche-PRESENT | heredity-BELOW  & scorable)
```

The claim predicts `Δ` large-positive (ideally `p_above → 1`, `p_below → 0`). Δ is the named statistic that goes in the lock — *not* raw agreement.

**1.3 Admissibility for the ABSENT side (resolves M4 + PM4 — ABSENT is two categories).**
- **empirical-search-negative** (e.g. a software-ecosystem cell): may read ABSENT only if the exogenous effort-proxy ≥ floor (the N.7.2 rule). Below floor → NO-CALL (drops out of scorable).
- **conceptual-clean-negative** (hurricane / single star / Bénard cell): "no beneficiary even importing a fitness concept" is an a-priori judgment, *not* a corpus search — admissibility is a **pre-registered conceptual-negative criterion**, NOT an effort floor. (Applying the effort floor here would force NO-CALL on exactly the clean negatives §5.1 relies on.) Each negative is logged with its category.

**1.4 Power gate (resolves B1's "no FAIL reachable").** The run is **INCONCLUSIVE by rule** unless both falsifier strata are non-empty above a locked minimum:
- `n_above_recordable ≥ N_a` — heredity-ABOVE cells where niche-ABSENT is *recordable* (so "ABOVE ⇒ PRESENT" is genuinely at risk), and
- `n_below_defined ≥ N_b` — heredity-BELOW-and-scorable cells (so "BELOW ⇒ ABSENT" is genuinely at risk).
If the corpus cannot furnish FAIL-capable cells, the census is **not yet runnable** — that is the honest verdict, not PASS.

**1.5 The null (resolves "no reference distribution").** Permutation: shuffle the niche toggles across scorable cells (preserving marginals), recompute Δ, repeat → null band. Report observed Δ as a percentile of the null.

**1.6 Pre-committed decision rule.**
- **PASS** iff Δ ≥ τ_pass (a locked null-percentile, e.g. > 97.5th) AND `p_below ≤ b_max` AND the §1.4 power gate is met AND (M2) Δ survives detrending on a documentation-density / study-volume covariate.
- **FAIL** iff (a) niche-PRESENT in heredity-BELOW-and-scorable cells beyond τ_fail (`p_below` high), or (b) niche-ABSENT in heredity-ABOVE-recordable cells beyond tolerance (Δ ≈ 0 / negative with adequate power) — the genuine falsifiers.
- **INCONCLUSIVE** otherwise (power gate unmet / effort below floor / Δ in the null band).

**1.7 Necessary-not-sufficient (M2).** State in the lock that co-variation is a *necessary* condition; require Δ to survive the covariate detrend; pre-register ≥1 **hard case** (heredity confidently ABOVE where niche-ABSENT would be surprising-but-admissible) so the ABOVE⇒PRESENT arm is at real risk.

**1.8 Lock-file additions.** `lock_brief_2.yaml` gains a `statistic:` block (the Δ formula + the conditioning), `null: {method: permutation, draws, seed-source}`, `power_gate: {N_a, N_b}`, `thresholds: {tau_pass_percentile, tau_fail, b_max}`, `absent_taxonomy: {empirical: effort_floor, conceptual: criterion}`, `covariate: {proxy, detrend_rule}`.

> **FORK 1 (Pav):** I propose the **conditional contrast Δ + permutation null** above. The defensible alternative is a chance-corrected 2×2 association (Cohen's κ / odds-ratio) over scorable cells. I recommend Δ because it isolates the two *directional* falsifiers the claim actually makes (ABOVE⇒PRESENT, BELOW⇒ABSENT), where κ only measures symmetric agreement. Confirm Δ, or steer to κ/OR.

---

## FIX 2 — Corpus + substrate shape (revises WORKFLOW §2; honest walk-back)

**The problem (BS2 + PM2 + B3 + M3 + BS3 + PM3):** a census substrate (hurricane field, RNA-world pool) is **not** a SCHEMA_v2 specimen — that schema's mandatory `child + weld.parents + when` trunk presupposes one merge-event, which a population/medium has none of. The existing 7 compiled substrates are *100% theory-merges* — zero census substrates exist. And the compiled export doesn't carry the structural fields the instruments read. **My WORKFLOW §2 "binds to SCHEMA_v2 frame machinery" overstated the binding** — owning that.

**The resolution — reuse the substrate-AGNOSTIC machinery only; define a native census-substrate record.**

What genuinely binds (keep): the **SUBSTRATE_SPEC fact-log + compiler + verification state machine + certainty rubric** make no assumption about welds/parents/child — they were verified substrate-agnostic. *That* is the real bind-don't-fork win.

What does NOT bind (drop the claim): the **SCHEMA_v2 specimen shape**. Replace "census substrate = a SCHEMA_v2 specimen" with a **native census-substrate record**:

```
census_substrate:
  substrate_id, name
  kind                 # molecular-replicator-pool | immune-system | cultural-tradition |
                       #   software-ecosystem | dissipative-structure[clean-negative] | ...
  plane_membership: { physical∈[0,1], latent∈[0,1] }   # straddle = both > 0  (fixes PM3: straddle is first-class)
  observer_levels[]    # the individuation ladder available here (molecular-replicator…population;
                       #   or individual-mind…community…canon) — the OBSERVER dial ranges over these
  copy_lens[]          # strict-replicator | broad-reproducer | information-channel
                       #   RENAMED from "frame" (fixes BS3 — frees Pav's frame term)
  kernel_frame[]?      # OPTIONAL ⊆ {time,space,knowledge,meaning} — Pav's frame kernels kept as a
                       #   SEPARATE, currently-unswept axis (NOT conflated with copy_lens)
```

- **Readings are measured facts, not membership (M3).** Q and E per cell are stored as first-class facts *with units + named estimator + certainty per the rubric* — NOT as SCHEMA_v2 graded membership, and the PROXY_SPEC "illustrator-not-measurement" disclaimer is **explicitly repudiated** for these channels (the falsification-target discipline is kept; the decoration disclaimer is not).
- **One artifact contract (fixes B3).** Extend `compile_substrate.py` (or a census sibling) so the **compiled census export carries the structural fields** (`plane_membership`, `observer_levels`, `copy_lens`, the dial facts). Then §3.1 (instruments read compiled) and §2 (axes) reference the **same** artifact, and the frame-lock SHA over the compiled snapshot genuinely pins every instrument input.
- **Corpus is a build step, not an assumption (PM2).** The census needs its **own** v0 corpus authored natively as facts — at minimum: one heredity-ABOVE positive per plane (RNA-world pool [physical], a cultural transmission tradition [latent]), one heredity-BELOW empirical case, and the clean negatives (hurricane / single star). The corpus MUST furnish the FAIL-capable cells of §1.4 or v0 is not runnable. The 7 existing theory-merge specimens are **not** census substrates (a theory-merge *could* later be authored as a latent-plane census substrate — separate exercise).

> **FORK 2 (Pav):** I propose the **native census-substrate record** above (reuse fact-log/compiler/verification only; drop SCHEMA_v2-specimen conformance). The alternative is a **ratified SCHEMA_v2 *variant* carve-out** (keep frame machinery, formally waive the weld trunk for census specimens). I recommend native: it's honest (census substrates aren't merge-events), it fixes B3/M3/BS3/PM3 cleanly, and it still reuses the genuinely-agnostic machinery. The cost is exactly the walk-back above — less shared structure with the genealogy viewer (a census-specific viewer would share only the dial-UI idiom, not the specimen schema). Confirm native, or steer to a carve-out.

---

## What these two fixes resolve (map to REVIEW_v1)

| Review item | Resolved here |
|---|---|
| **B1** test can't fail | Fix 1.2/1.4/1.5/1.6 (conditional Δ, power gate, null, FAIL-reachable) |
| **B3** artifact contract | Fix 2 (compiled export carries structural fields; one artifact; hash pins inputs) |
| **PM1** concordance undefined | Fix 1.2 (Δ is the named statistic) |
| **PM2** corpus doesn't exist | Fix 2 (native corpus as a build step; FAIL-capable requirement) |
| **PM3** straddle dropped | Fix 2 (`plane_membership` makes straddle first-class) |
| **PM4** ABSENT one category | Fix 1.3 (empirical vs conceptual negatives, different admissibility) |
| **M3** dial → membership | Fix 2 (stored as measured facts; disclaimer repudiated) |
| **M4** UNDEFINED scoring contradiction | Fix 1.1 (out-of-scope, can't move PASS/FAIL) |
| **BS2** census ≠ SCHEMA_v2 specimen | Fix 2 (native record) |
| **BS3** "frame" collision | Fix 2 (`copy_lens` rename; `kernel_frame` separate) |
| **M2** necessary-not-sufficient | Fix 1.7 (covariate detrend + hard case) — partial; full confound work is REVISION v2 |

## Deferred to REVISION v2 (downstream)
B2 de-circularize the molecular anchor · M1 nameability/blinding protocol · M5 per-mode E + per-plane "a" · M6 instantiable-grid enumeration · BS1 refutation budget K · BS4 Conjecture-B scope + ESTABLISHED-NON-B · M7/BS5 register + missing-caveat edits · "first opportunity" scoping.

---

*Provenance: 2026-06-11, Claude Code, starting the revision per Pav's "b then a" steer. Addresses REVIEW_v1 upstream faults only. Tier-3, surfaced for Pav steer (two forks). Nothing run/locked; convergence list still 9.*
