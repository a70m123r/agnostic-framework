# Falsifier — the 6-organ reduction, blind-coded against held-out dynamics

**Date:** 2026-06-16 | **Status:** the test codex + gemini asked for, run. 4 INDEPENDENT blind coders classified 15 held-out dynamics (fresh domains, not the 41) into the 6 candidate organs (or NONE-needs-new). Demote-not-kill.

**Overall agreement:** substantial. Fleiss kappa = 0.671 (substantial band, 0.61-0.80); observed agreement P_o = 0.778, chance P_e = 0.324. 10/15 items unanimous, 2/15 three-of-four, 3/15 split. Agreement is genuinely strong on the discriminating organs (h1, h2, h3, h3b, h4, h5, h8, h10, h13, h14 all 4/4) and concentrates its disagreement on exactly the items that triggered new-organ proposals (h6, h7, h9, h11, h12) -- i.e. the disagreement is informative, not noise.

**Needs-new-organ pressure:** 3/15 = 0.20 at the strict threshold (>=2 of 4 coders coded NONE-needs-new-organ: h6, h9, h11). BUT the named-construct signal is stronger than the forced-choice vote: 4 items (h6, h7, h9, h11) had a single coherent new-organ construct named by ALL 4 coders independently, and 2 more (h12, h13) by 2 coders. So the effective needs-new pressure is ~4/15 (0.27) of clearly-missing organs plus 2/15 sub-organ refinements -- materially above a clean-survival threshold (~<=1/15).

## Verdict

PARTIAL (demote-not-kill). The 6-organ reduction does NOT cleanly survive blind held-out coding, but it does not collapse either. (A) SURVIVING organs -- 4 of 6 discriminate cleanly with high blind agreement: CRITICALITY-HYSTERESIS, MOTIVE-DRIVE, BACK-REACTION, REFEREE-INFO-STRUCTURE each won at least one unanimous item (h2/h3/h3b/h4/h5/h13/h14; h1; h8; h10). (B) DEAD organ -- BANDWIDTH-CAPACITY drew exactly 1 of 60 raw votes (only coder 4, on h12, which itself was the most-scattered item) and never won an item: candidate for collinearity/merger or removal; on this 15-item held-out set it is non-discriminating. (C) OVERLOADED organ -- CRITICALITY-HYSTERESIS absorbs 31/60 raw votes and 8/15 majority items, acting as a catch-all that swallows at least three distinct mechanisms coders flagged by name: phase-transition/quorum (h4/h5/h14, legitimate), network-cascade (h3), ragged-landscape (h13), and feedback-oscillation (h7). It is too coarse and is masking missing organs. (D) MISSING organs -- 4 constructs were independently named by all 4 coders (HEAVY-TAIL-DISPERSION, FRAME-BORROW, ABSTRACTION-OVERSHOOT, FEEDBACK-GAIN-OSCILLATION); a recurring blind proposal at 4/4 is the strongest possible evidence of a real gap, and two of these (h9, h11) also won the forced NONE vote. The overall kappa of 0.671 is genuinely substantial, so the SKELETON holds -- but the falsifier succeeds in showing the reduction is under-complete (missing ~3-4 organs) and partly redundant (1 dead, 1 overloaded). Recommendation: retain the 5 discriminating organs, retire/merge BANDWIDTH-CAPACITY pending evidence, split CRITICALITY-HYSTERESIS, and promote HEAVY-TAIL-DISPERSION, FRAME-BORROW, and ABSTRACTION-OVERSHOOT to organ status (FEEDBACK-GAIN-OSCILLATION as a strong candidate, INFO-GAIN-SEARCH/RAGGED-LANDSCAPE as sub-organs to watch). Honest framing: not killed, demoted from '6 organs span the space' to '5 robust organs + a documented 3-4 organ gap; one organ on probation.'

## Recommended (empirically-revised) organ set
- CRITICALITY-HYSTERESIS (survives but flagged OVERLOADED -- recommend splitting off phase-transition vs network-cascade)
- MOTIVE-DRIVE (survives)
- BACK-REACTION (survives)
- REFEREE-INFO-STRUCTURE (survives)
- HEAVY-TAIL-DISPERSION (promote -- new, 4/4 blind proposal)
- FRAME-BORROW (promote -- new, 4/4 blind proposal, won forced NONE vote)
- ABSTRACTION-OVERSHOOT (promote -- new, 4/4 blind proposal, won forced NONE vote)
- FEEDBACK-GAIN-OSCILLATION (candidate -- new, 4/4 named but currently absorbed; distinct from phase transition)

## Missing organs the blind coders named (independently)
- HEAVY-TAIL-DISPERSION (h6): outcome dominated by rare over-dispersed events, k<<1, mean carried by tail, top-event ablation collapses cascade, replay-divergent -- named by 4/4 coders. STRONGEST missing-organ signal.
- FRAME-BORROW / BASIS-CHANGE (h9): transient licensed excursion into an adjacent rule-set to reach an in-frame target provably unreachable by in-frame moves, then reabsorbed -- named by 4/4 coders, and 3/4 forced it to NONE. STRONG missing-organ signal.
- ABSTRACTION/GENERALIZATION-OVERSHOOT (h11): non-monotonic U-shaped competence dip from over-applying a newly-induced general rule to its exceptions; systematic rule-shaped errors; recovery to higher plateau -- named by 4/4, 3/4 forced to NONE. STRONG missing-organ signal.
- FEEDBACK-GAIN-OSCILLATION (h7): lag+buffer control-loop amplification producing ringing that grows with distance from the source; control instability, NOT a phase transition -- named by 4/4 but absorbed into CRITICALITY-HYSTERESIS / BACK-REACTION. MODERATE: distinct mechanism currently mis-binned.
- INFO-GAIN-SEARCH (h12): probe placement chosen to maximize bits eliminated per step; log2 candidate-set descent, EIG-optimal partitioning -- named by 2/4; h12 was the most scattered item (4 different codes). MODERATE.
- RAGGED-LANDSCAPE (h13): locally-smooth-but-discontinuity-riddled response surface (activity cliffs) that punishes gradient extrapolation -- named by 2/4 as a sub-organ of CRITICALITY-HYSTERESIS. WEAK/refinement.

## Per-item blind agreement

| item | domain | agreement | majority organ |
|---|---|---|---|
| h1 Affinity Maturation | immune systems | unanimous (4/4) | MOTIVE-DRIVE |
| h2 Liquidity Evaporation | financial markets | unanimous (4/4) | CRITICALITY-HYSTERESIS |
| h3 Trophic Cascade | ecosystems | unanimous (4/4) | CRITICALITY-HYSTERESIS |
| h3b Metastable Jam | traffic / queueing | unanimous (4/4) | CRITICALITY-HYSTERESIS |
| h4 Tipping Cascade | social contagion | unanimous (4/4) | CRITICALITY-HYSTERESIS |
| h5 Crack Coalescence | materials fracture | unanimous (4/4) | CRITICALITY-HYSTERESIS |
| h6 Superspreader Skew | epidemics | 2-2 split (MOTIVE-DRIVE vs NONE-needs-new); all 4 named HEAVY-TAIL as the missing construct | MOTIVE-DRIVE / NONE (tie) |
| h7 Bullwhip Amplification | supply chains | 2-1-1 split (CRITICALITY-HYSTERESIS x2, BACK-REACTION x1, NONE x1); all 4 named FEEDBACK-GAIN-OSCILLATION | CRITICALITY-HYSTERESIS |
| h8 Counterpunch Read | sport | unanimous (4/4) | BACK-REACTION |
| h9 Modal Interchange | music improvisation | 3-of-4 (NONE-needs-new x3, REFEREE-INFO-STRUCTURE x1); all 4 named FRAME-BORROW | NONE-needs-new-organ |
| h10 Burden Shift | law / courtroom | unanimous (4/4) | REFEREE-INFO-STRUCTURE |
| h11 Overregularization Dip | language acquisition | 3-of-4 (NONE-needs-new x3, CRITICALITY-HYSTERESIS x1); all 4 named ABSTRACTION/GENERALIZATION-OVERSHOOT | NONE-needs-new-organ |
| h12 Bisection Collapse | debugging | 2-1-1 split (MOTIVE-DRIVE x2, REFEREE-INFO-STRUCTURE x1, BANDWIDTH-CAPACITY x1); 2 named INFO-GAIN-SEARCH | MOTIVE-DRIVE |
| h13 Lead Optimization Cliff | drug discovery | unanimous (4/4) on CRITICALITY-HYSTERESIS; 2 flagged RAGGED-LANDSCAPE as sub-organ | CRITICALITY-HYSTERESIS |
| h14 Quorum Latch | ecosystems / microbial | unanimous (4/4) | CRITICALITY-HYSTERESIS |

## Organ usage (votes)

```
{
  "CRITICALITY-HYSTERESIS_majority_items": 8,
  "CRITICALITY-HYSTERESIS_raw_votes_of_60": 31,
  "MOTIVE-DRIVE_majority_items": 3,
  "MOTIVE-DRIVE_raw_votes_of_60": 8,
  "BACK-REACTION_majority_items": 1,
  "BACK-REACTION_raw_votes_of_60": 5,
  "REFEREE-INFO-STRUCTURE_majority_items": 1,
  "REFEREE-INFO-STRUCTURE_raw_votes_of_60": 6,
  "BANDWIDTH-CAPACITY_majority_items": 0,
  "BANDWIDTH-CAPACITY_raw_votes_of_60": 1,
  "NONE-needs-new-organ_majority_items": 2,
  "NONE-needs-new-organ_raw_votes_of_60": 9
}
```

## The held-out test set (15 dynamics, fresh domains)
- **Affinity Maturation** (immune systems) — The observer doesn't solve at once; it keeps a pool of partial antibody-hypotheses and runs rounds of somatic hypermutation + selection, where each round preferentially amplifies variants that bind the antigen-problem slightly better, so th
- **Liquidity Evaporation** (financial markets) — An observer that was digesting the problem fluidly (many counterparties / cheap moves available) hits a stress threshold where the apparent depth of available moves vanishes non-linearly: everyone's strategy correlates at once, the bid-ask 
- **Trophic Cascade** (ecosystems) — Removing or resolving one keystone sub-problem doesn't just close it; it propagates down a dependency web, releasing or suppressing whole layers of previously-stable sub-problems, so the observer's single targeted edit triggers a chain of c
- **Metastable Jam** (traffic / queueing) — The observer is processing arrivals below nominal capacity, yet a tiny perturbation (one slow step) nucleates a backward-propagating stall: the congestion wave travels upstream against the flow of work, persisting and even growing long afte
- **Tipping Cascade** (social contagion) — The observer holds the problem in suspension while adoption of a candidate framing stays below each local threshold; nothing visibly moves, then a single additional commitment crosses a critical fraction and the framing flips the entire int
- **Crack Coalescence** (materials fracture) — The observer accumulates many independent micro-flaws (small unresolved tensions) that are individually harmless; under sustained load they grow quietly and align, and at a critical density two cracks link, suddenly providing a low-resistan
- **Superspreader Skew** (epidemics) — Progress through the problem is not driven by the average move but by a heavy-tailed minority: most sub-steps transmit almost nothing forward, while a few rare 'superspreader' insights each ignite a disproportionate share of all subsequent 
- **Bullwhip Amplification** (supply chains) — The observer's correction to a small downstream discrepancy gets amplified at each upstream reasoning layer due to lag and safety-buffering, so a minor change in the surface problem induces wild over- and under-shooting oscillations deep in
- **Counterpunch Read** (sport) — The observer deliberately under-commits, baiting the problem to reveal its structure by reacting; it solves not by initiating but by reading the opponent-problem's committed motion and exploiting the opening that commitment necessarily crea
- **Modal Interchange** (music improvisation) — The observer resolves an impasse by borrowing structure from a parallel frame (a different key/mode) — temporarily importing a foreign element that is locally dissonant but creates a new resolution path unavailable within the home frame, th
- **Burden Shift** (law / courtroom) — The observer advances by establishing a presumption that flips who must do the work: once a prima-facie threshold is met, the cost of the problem transfers to the other side, and progress thereafter is measured not by proving the claim but 
- **Overregularization Dip** (language acquisition) — The observer first handles cases by rote and performs well, then discovers a general rule and over-applies it, temporarily getting previously-correct irregular cases wrong (a U-shaped competence dip) before learning where the rule's excepti
- **Bisection Collapse** (debugging) — The observer halves an exponential hypothesis space per probe by testing the midpoint of an ordered fault-region, discarding half regardless of outcome, so uncertainty shrinks geometrically and the solve cost is logarithmic in problem size 
- **Lead Optimization Cliff** (drug discovery) — The observer climbs a smooth structure-activity gradient improving a candidate, then hits an 'activity cliff' where a tiny change in the candidate causes a huge drop in fit — the response surface is locally smooth but riddled with discontin
- **Quorum Latch** (ecosystems / microbial) — Independent sub-solvers each emit a weak signal and stay dormant; none acts alone, but once the aggregate signal concentration crosses a quorum threshold the whole population switches behavior simultaneously and commits to a coordinated sol