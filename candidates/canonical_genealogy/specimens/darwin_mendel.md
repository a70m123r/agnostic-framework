# Specimen — Darwin + Mendel → the Modern Synthesis

> **The canonical dormancy→resurrection + multi-parent-weld worked example.**
>
> **Status:** Tier-3 WORKING specimen — exploratory data-harvest, surfaced for **Cowork+Pav ratification**. NOT canon, NOT a tier promotion, does **NOT** grow the convergence list (stays **9**). This is a *worked example of the genealogy schema* on a historical-science merger — used to stress-test the schema's variables — **not** a 10th cross-substrate convergence. All confidences are SOFT scores in [0,1]; bits are qualitative only.
>
> **Files:** machine-readable render is `darwin_mendel.json` (this dir); spec is `../SCHEMA.md`; template is `../one_specimen.template.json`.
> **Extends:** `../latent_olympics_data/wrapper_classes_phase1.json` — same organism, deeper zoom (SCHEMA.md §4). Instance-of the parents-produce-W_C pattern the `bes_convergence_9` test instrument scores all convergences against. **Generated:** 2026-06-09. **Overall confidence:** ~0.90 (trunk ~0.95–0.97; pulled down by the well-attested framework-vs-record tensions).

---

## The merge in one paragraph

Across roughly **1918–1950**, Darwinian natural selection (`W_A`) was welded to Mendelian particulate inheritance (`W_B`) into a single mathematical framework — **the Modern Synthesis** (named by Julian Huxley in 1942). The child `W_C` redefined evolution as *"change in allele frequencies within populations,"* scaling micro-evolution (population genetics) up to explain macro-evolution (speciation, paleontological tempo). The case is the **canonical dormancy→resurrection story**: Mendel's 1866 paper was cited only ~3 times in ~34 years, was independently rediscovered in 1900, and was then welded to a *Darwinism that had itself been eclipsed* — two nested dormancies, where resurrecting one (Mendel) supplied the piece that resurrected the other (selection).

```
        cultural_harvest: eugenics (dark child) · scifi (Wells, Stapledon) · genetic algorithms
                              ▲
   descendants:  neutral theory (Kimura'68) · selfish gene (Hamilton/Williams/Dawkins) ·
                 sociobiology · evo-devo · Extended Evolutionary Synthesis (2007+, contesting) · GWAS
                              ▲
        W_A ──weld──►  ┌──────────────────────┐  ◄──weld──  W_B
   Darwinian          │   THE MODERN          │           Mendelian
   natural            │   SYNTHESIS  (W_C)    │           particulate
   selection          │  "evolution = Δ allele│           inheritance
   (no inheritance    │   frequencies"        │           (first arrived as
    mechanism;        └──────────────────────┘            ANTI-Darwinian
    blending-doomed)            │                          mutationism!)
                                │
                 shared sub-object S = POPULATION GENETICS
                 (Hardy-Weinberg 1908; Fisher 1918/30; Haldane; Wright)
                 ── NOT the 1866-paper-meets-1859-book seam the popular story implies ──
                                │
   sub_wrappers: Fisher-1918 bridge · biometry · mutationism · Weismann hard-heredity ·
                 Morgan's chromosomes · Mendel's peas · Malthus
                                │
   people_0 (0): Mendel · Darwin · Wallace · Napp · Naegeli · the ARCHITECTS
                 (Fisher, Haldane, Wright, Dobzhansky, Mayr, Simpson, Stebbins, Huxley)
```

---

## The child — `W_C`

- **Name:** The Modern Synthesis (neo-Darwinian synthesis / synthetic theory of evolution).
- **Kernel:** Reconcile Darwinian selection with Mendelian inheritance into one calculus; evolution = change in allele/gene frequencies in populations; micro→macro. A flow over generations carrying a conservation law (Hardy-Weinberg) and theorems (Fisher's fundamental theorem). **Confidence 0.95.**
- **Frame:** `time` + `knowledge` + `meaning` (primary) + `space` (allopatric speciation) — a **wide-frame child**, touching all four observer global kernels.
- **Status:** `resurrected` — but genuinely **status-at-a-time** (see schema gap). Trajectory: *resurrected* (1900–37) → *risen* (1937–59) → *hardened/contested* (1959→) → currently **active with a live extension debate** (the EES, 2007+).
- **Utility:**
  - **Unifier:** welds ≥5 warring sub-disciplines (genetics, systematics, paleontology, botany, ecology) under one allele-frequency calculus *and* ends the biometrician-vs-Mendelian war. A unification of unifications.
  - **Compressor:** collapses *descent with modification* + *3:1 segregation* + *continuous biometric variation* into one statement — continuous variation = many small-effect Mendelian loci summing (Fisher 1918). (Bits qualitative only.)
  - **Action-spaces unlocked:** breeder's equation / heritability · adaptive landscape (Wright 1932) · biological species concept (Mayr 1942) · molecular-clock & neutral tests (Kimura 1968) · all of modern quantitative + medical genetics (**GWAS descends from Fisher 1918**) · genetic algorithms (Holland 1975 — the lineage already in the DB under BES).

---

## The weld — parents → child

| | `W_A` | `W_B` |
|---|---|---|
| **Name** | Darwinian evolution by natural selection | Mendelian genetics / particulate inheritance |
| **Kernel** | Descent with modification by selection on heritable variation under Malthusian struggle | Discrete non-blending factors segregating in fixed ratios (3:1); variation *preserved* not averaged |
| **Fatal gap / twist** | **No mechanism of inheritance**; blending assumption → Jenkin 1867 dissolves any new variant; pangenesis (1868) failed | First arrived as **anti-Darwinian mutationism** (Bateson, de Vries) — *opposed* `W_A` before fusing to it |
| **Frame** | time + space + meaning | knowledge + meaning (gains time only once in populations) |
| **Confidence** | 0.98 | 0.97 |

- **Shared sub-object `S`:** **population genetics** (the Hardy-Weinberg allele-frequency distribution, 1908). Darwin's "variation" and Mendel's "factor" are the *same object* only once expressed as gene frequencies — the seam Fisher/Haldane/Wright actually welded. **This is the load-bearing correction: the real `S` sits a layer *up* from the two ancestral theories the popular story names.** (`S` itself was internally fractured — Fisher vs Wright.)
- **Surprise (synergy, conf 0.90):** neither parent alone predicts that the biometricians' *smooth continuous* variation and the Mendelians' *discrete particulate* genes are the **same thing at two grains**. Reachable only from both, via Fisher 1918: many small-effect Mendelian loci sum to continuous, non-blending variation selection can move smoothly. This (i) rescues gradualism from the blending objection that eclipsed it ~50 years, (ii) shows the two warring schools described one phenomenon, (iii) turns evolution into a quantitative science with a conservation law. **Deepest surprise:** it redefined *"evolution"* itself from "descent of forms" to "change in allele frequencies" — a meaning-frame shift neither parent articulated.
- **`bits_note` (qualitative only):** one statement replaces two unreconciled, mutually-contradicting accounts; the joint description is clearly shorter; synergy genuine, not additive. **No bit value computed** — MDL-in-bits needs latent embeddings (a later step).
- **Frame of weld:** `time` + `knowledge` (built in the knowledge-frame as population-genetic theory; lives dynamically in the time-frame) — note this **differs** from `child.frame`.
- **LOD scale:** holds at the field/theory grain. Zoom in and the single weld dissolves into a ~30-year cascade of pairwise welds among ~8 architects (Fisher 1918 → Haldane → Wright → Dobzhansky 1937 → Mayr 1942 → Simpson 1944 → Stebbins 1950).
- **When:** ~1918–1950 — a **process, not an event** (defensible births: Fisher 1918 / the 1930–32 trio / Dobzhansky 1937; *named* Huxley 1942).

### Survived vs dropped

- **Survived:** natural selection (W_A core) · particulate inheritance + segregation (W_B core) · gradualism (rescued, now grounded) · descent with modification · allopatric isolation (Mayr) · hard heredity (Weismann) · **parents persist as procedural-root stubs** ("Mendelian ratios" and "Darwinian selection" remain the named foundations).
- **Dropped:** pangenesis · **blending inheritance** (the doom of pre-weld `W_A`) · Lamarckism · orthogenesis · **saltationist** mutationism (discrete-factor core kept) · Galton/Pearson's ancestral-heredity framework (data kept) · Huxley's "progress." **Contested-dropped-then-revived:** genetic drift (demoted in the 1940s–50s hardening, revived by Kimura 1968 + EES).

### Dormancy & revival (the defining feature)

| # | Dormant object | Interval | Why |
|---|---|---|---|
| 1 | `W_B` — Mendel's 1866 paper | 1866 → 1900 | ~3 citations in ~34 yrs; read as species-hybridization not heredity; Naegeli's hawkweed misdirection; blending orthodoxy; Mendel→abbot duties (**dormancy contested** — Olby) |
| 2 | `W_A`'s **mechanism** (selection) | ~1880s → ~1930s | the "eclipse of Darwinism" (Bowler) — descent accepted, *selection* unpopular vs mutationism/orthogenesis/neo-Lamarckism |

**Revival:** (a) Mendel rediscovered **1900** by de Vries, Correns, Tschermak (contested three-/two-way; trigger = their own ratio-hitting experiments + Morgan's chromosome context); (b) selection revived **1918–1937** (trigger = Fisher's 1918 reconciliation removing the blending objection, then Dobzhansky 1937 translating the math for naturalists). **Two nested dormancies; resurrecting one resurrected the other.**

---

## Roots (down, physical frame)

**Mediating wrapper at depth 0** — *the real proximate parent the 2-slot `parents[]` can't hold:* **population genetics** (Hardy-Weinberg + Fisher's fundamental theorem + Wright's landscape + Haldane's models), conf 0.92.

**Depth-1 sub-wrappers:** Fisher 1918 bridge (0.95) · biometry / ancestral heredity (Galton/Pearson, 0.85) · mutationism (de Vries/Bateson, 0.85) · Weismann germ-plasm (0.85) · Morgan's Drosophila chromosomes (0.85) · Mendel's pea experiments (0.95) · Malthusian pressure (0.90).

**People (ground kernel "(0)"):**
- **Mendel side:** Gregor Mendel (Brno Augustinian friar, b.1822; originator, the dormant root) · Abbot Napp (patron) · Doppler / Ettingshausen / Unger (Vienna teachers — methodological roots, conf 0.70) · **Carl von Naegeli** (the *transmitter-who-failed-to-transmit* — a causal node in the dormancy).
- **Darwin side:** Charles Darwin (b.1809; originator) · Wallace (co-originator, 1858) · Erasmus Darwin / Lyell / Malthus + the *Beagle* voyage (ancestral sub-wrappers).
- **The architects (the REAL proximate people-0):** Fisher, Haldane, Wright (the maths trio — Fisher & Wright *disagreed*) · Dobzhansky, Mayr, Simpson, Stebbins, Huxley, Ford (the naturalist synthesizers). A transatlantic UK + US + émigré-European network.

---

## Harvest (up, latent + cultural)

**Descendant theories:** neutral theory (Kimura 1968 — re-opened the drift question; counter-child) · gene-centred view / kin selection (Hamilton 1964, Williams 1966, Dawkins 1976) · sociobiology (Wilson 1975) · evo-devo (rival-child) · **Extended Evolutionary Synthesis** (2007+ — the *contesting* child keeping `W_C` "active") · quantitative genetics → **GWAS** (direct from Fisher 1918).

**Cultural spill:** **eugenics** (Galton coined it 1883 from Darwin; Fisher's 1930 book had eugenic chapters; weaponized by the Nazi state + sterilization programs — the dark child) · **sci-fi** (Wells' Eloi/Morlocks, Stapledon's future-human evolution) · **art/thought** (Social Darwinism, Spencer's "survival of the fittest") · **tech** (genetic algorithms, Holland 1975 — the cross-link back into the convergence DB).

## Relatives (wide)

Cousin **symbiogenesis** (DB convergence #3 — a *clean* two-parent biology weld, contrasting this *messy* multi-parent one) · cousin **model merging / BES** (DB #6/#9 — the population-genetics recombination math is a *named ancestor of BES*) · rival **Lamarckism** (the defeated alternative) · influence **Mendel-Fisher controversy** (Fisher, a *parent* of `W_C`, accusing Mendel, an *ancestor* of `W_C`, of data "too good to be true" — a parent auditing an ancestor).

---

## Certain core vs frontier (the fuzzy-LOD split)

### ✅ Certain core (the trunk, conf ≈ 0.90–0.97)

1. The merge happened — selection reconciled with Mendelism across ~1918–1950, named by Huxley 1942. *(~0.95–0.97)*
2. Fisher 1918 reconciled continuous variation with discrete loci (many small-effect loci). *(~0.95)*
3. Mendel cited ~3× in ~34 yrs; rediscovered 1900 by de Vries/Correns/Tschermak — **the fact** (not the interpretation). *(~0.90–0.95)*
4. Darwin lacked an inheritance mechanism; blending (Jenkin 1867) was a real fatal objection the weld removed. *(~0.95)*
5. Evolution redefined as "change in allele frequencies." *(~0.95)*
6. Hardy-Weinberg (1908) as the conservation law. *(~0.95)*
7. The architect roster (Fisher/Haldane/Wright/Dobzhansky/Mayr/Simpson/Stebbins/Huxley). *(~0.92)*
8. The EES (2007+) as a live contesting descendant. *(~0.90)*

### 🌫 Frontier (low-confidence / conjectural / schema-stress — the cultivation zone)

1. **Literal Darwin-Mendel dyad as THE two parents** *(~0.55)* — the proximate parent is population genetics; Darwin & Mendel are the *deep roots*. (= discrepancy #1, highest-value.)
2. **Clean-dormancy narrative** *(~0.50)* — "misunderstood genius ignored then rediscovered intact"; Olby/Brannigan contest it (he did species-hybridization). The *fact* of ~3 citations stays high; the *story* is frontier.
3. **Tschermak as a true co-equal rediscoverer** *(~0.50)* — may not have grasped segregation; the "three rediscoverers" trope may reduce to ~two.
4. **`S` as a single coherent object** *(~0.70)* — the Fisher-Wright rift fractured the seam.
5. **The child as a single fixed object** *(~0.70)* — pluralist-1937 vs hardened-1959 differ (Gould/Provine).
6. **A single birth-date** *(<0.60 any single date; the 1918–1950 range ~0.95)*.
7. **Vienna-teacher methodological roots** *(~0.70)* — Ettingshausen's combinatorics → Mendel's ratio-counting is plausible but not firmly attested.
8. **Schema-stress (frontier of the *model*, not the record):** multi-parent reality, status-trajectory, revived-as-reinterpreted, fractured-`S`, antagonism-then-fusion, weld-as-process all strain the schema's fields.

---

## Discrepancies carried into the record (the real-record frontier — SIGNAL)

| # | Type | What | Confidence impact |
|---|---|---|---|
| 1 | **framework-vs-record-tension** ⭐ | The clean two-parent weld is wrong: the real weld is **multi-parent** (Fisher/Haldane/Wright + Dobzhansky/Mayr/Simpson/Stebbins/Huxley) and the true `S` is **population genetics**, not "1866 paper meets 1859 book." Darwin & Mendel are the two *deep roots*, not the two proximate parents. | Dyad-as-parents → **0.55**; population-genetics-as-`S` → **0.90** |
| 2 | **dormancy-contested** | The "35 years of neglect" is disputed: Olby 1979/Brannigan — Mendel did *species-hybridization*, the "long neglect" framing traces only to Glass 1953; *and* this revisionism is itself contested back (Oxford Genetics 2023; John Innes). A three-pole literature. | Fact of low citation **0.90**; clean-neglect *narrative* **0.50** |
| 3 | **priority-dispute** | de Vries published 1900 **without citing Mendel**, added it only after Correns objected; Tschermak's grasp of segregation is doubted. The revival trigger was itself a contested 3-/2-way event. | de Vries/Correns **0.95**; Tschermak co-equal **0.50** |
| 4 | **contested-genealogy** | **Fisher vs Wright** (1929–62): mass-selection (drift negligible) vs shifting-balance (drift important). `S` (population genetics) contained an **unresolved internal rift** — the seam is fractured, non-unitary. | `S`-as-single-object **0.70**; the rift itself **0.95** |
| 5 | **whig-vs-revisionist** | **Hardening of the synthesis** (Gould/Provine): pluralist 1930s → rigid pan-selectionism by 1959. `W_C` at t=1937 ≠ `W_C` at t=1959 — the child is **time-indexed**. | Child-as-fixed-object **0.70** |
| 6 | **date/attribution-conflict** | No single "start": Fisher 1918 vs the 1930–32 trio vs Dobzhansky 1937; *named* 1942. | No single date **>0.60**; the 1918–1950 range **0.95** |
| 7 | **framework-vs-record-tension** | **Antagonism-then-fusion:** Mendelism arrived as an *anti*-Darwinian weapon (~1900–1915, the biometrician-Mendelian war) **before** Fisher 1918 welded the parents. Neither was dormant — they were *fighting*. | Antagonism phase **0.90**; flags a missing variable (no confidence drop) |

---

## Schema fields that were hard to fill (the missing variables)

These are the deliverable's most valuable output — the places this specimen *breaks* the schema, each grounded in a discrepancy above:

1. **2-slot `parents[]` cannot hold this weld** (= discrepancy #1). Real structure = **two ancestral roots** (Darwin, Mendel) + a **mediating parent that did the welding** (population genetics / Fisher-Haldane-Wright) + **~5 empirical synthesizers**. Needs an explicit **`mediating_wrapper` / `weld_was_built_by`** slot distinct from `parents`, and an **N-parent mode**. (Ratifies SCHEMA.md §5 gap #6 with strong evidence.) *Worked around* by recording extra parents in `roots.people_0` + `roots.sub_wrappers` and as discrepancies — but it visibly strains the model.
2. **`status` is a single enum but the child is status-at-a-time** (= discrepancy #5). pluralist-1937 / hardened-1959 / contested-2007 are different states of the *same* `W_C`. Needs a **status *trajectory*** field.
3. **`dormancy_intervals` assumes the dormant object is the same object that revives** (= discrepancy #2). Mendel's revived object may have been **re-framed** (species-hybridization → heredity). Needs a flag: **`revived-as-same` vs `revived-as-reinterpreted`** — a revival can be a *re-weld into a new role*, not a wake-up.
4. **`shared_sub_object_S` is treated as one coherent string** (= discrepancy #4). Here `S` was **internally fractured** (Fisher-Wright). Needs `S` to be allowed **non-unitary / itself contested**.
5. **No "parent initially OPPOSED the other parent" marker** (= discrepancy #7). `survived`/`dropped` exist, but no **antagonism-then-fusion lifecycle** on the weld. Suggests a **pre-weld-relationship** variable (`antagonism | independence | complementarity`).
6. **`when` is one field but the weld is a ~30-year process** (= discrepancy #6). A weld may need a **duration/interval**, not a date.
7. **Sourcing caveat:** Provine's monograph and Olby's revisionism were accessed via **search-engine summaries, not full primary text**; the framework-vs-record and contested-dormancy claims are well-attested but held at ~0.9, not 1.0. **No bit-values fabricated** (`bits_note` kept qualitative per SCHEMA.md §3).

---

*Tier-3 exploratory data-harvest. Surfaced for Cowork+Pav ratification — refines the variables; does not compile canon, promote anything, or grow the convergence list (stays 9). Every load-bearing claim traces to `sources[]` in `darwin_mendel.json`; trunk facts web-verified 2026-06-09.*
