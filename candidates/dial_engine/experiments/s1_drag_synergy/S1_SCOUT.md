# S1 scout — drag × solar synergy (fresh-lit scan + data feasibility, 2026-06-13)

> Scout for the S1 dial-protocol sweep-1 candidate, run per the standing fresh-literature-scan practice ([[feedback_fresh_literature_scan]]). The scan **changed the design** — exactly its job. NOT the experiment; this de-risks data + pins the freshest SOTA/baselines before the S1 workflow fires.

## The pivot the scan forced
**Old plan:** satellite orbital decay (TLE history) × solar activity. **Problem:** TLE *history* is Space-Track-auth-gated (CelesTrak archives need a Special Data Request; `tl3` pypi / archive.org are partial) — and creating accounts is prohibited.
**New plan (what every 2024-2026 paper actually uses):** **thermospheric neutral density** (the real drag driver, from GRACE/CHAMP/Swarm accelerometers + POD) × **solar + geomagnetic indices**. Cleaner (removes per-satellite ballistic-coefficient noise), auth-free, and it is the field-standard ML-ready data.

## Data path — CONFIRMED auth-free (all curl-tested 2026-06-13)
- **Thermospheric density:** TU Delft `https://thermosphere.tudelft.nl/data/data/` (CHAMP/GRACE/GOCE/Swarm POD density, HTTP 200, live, updated 2026-06-07) · PANGAEA **TND-IGG RL01** (Vielberg et al. 2021, `doi.org/10.1594/PANGAEA.931347`, textfile export works with `-k` for a cert quirk).
- **Solar/geomagnetic indices (NOAA SWPC, same source as the GOES probe):** F10.7 `json/f107_cm_flux.json` · Kp `products/noaa-planetary-k-index.json` · **Dst** `products/kyoto-dst.json` (hourly) · Ap/A-index · **SSN + F10.7 history to 1749** `json/solar-cycle/observed-solar-cycle-indices.json` (the deep history also feeds the Q6 coarse-scale follow-up — the 11-yr cycle is right there).
- **Karman** (`github.com/spaceml-org/karman`, NASA Heliophysics + Trillium): the SOTA open benchmarking package; ingests POD density + F10.7/M10.7/S10.7/Y10.7 + Dst/Ap + SOHO/GOES EUV in ML-ready form. Optional one-stop loader; or pull TU-Delft/PANGAEA + NOAA directly and align (lighter, matches our instrument style).

## Freshest SOTA + baselines to be aware of (the crop, dated)
- **Acciarini et al. 2024** (Space Weather, `2023SW003652`) — Karman; ML LEO density, MAPE 40-60% -> ~20% vs empirical.
- **Pan et al. 2024 / 2025** (Space Weather `2023SW003844`, `2024SW004259`) — interpretable ML density from GRACE/GRACE-FO; ~91/66/56% improvement over NRLMSIS (Swarm-C/CHAMP/GOCE).
- **Survey of operations-ready density models** (PMC12995994, 2025/26) — names the empirical baselines: **NRLMSIS, JB2008, DTM, HASDM**.
- **HASDM density DB** 2000-2019 public since 2020; **extension through mid-2025 expected public early 2026** — worth re-checking at fire time.
- **May 2024 Gannon storm** drag analysis (arXiv `2406.08617`) — a huge recent drag event = a natural frame-dial storm experiment (the drag analogue of our GOES M-flare week).
- **Belbase 2026** (Space Weather `2025SW004757`) — reconstructing historical solar indices (relevant to the deep-history angle).
- **swsc-journal 2026/01** (`swsc250083`) — a new approach to space-weather impact on LEO drag.

## S1 design, reframed (proposed; gated on a nod before firing the workflow)
**The framework's actual question is NOT "predict density" (Karman/NRLMSIS do that) — it is the SYNERGY GATE (gain_v2) on real coupling.** Density has two drivers: solar flux (F10.7/EUV) and geomagnetic activity (Kp/Dst/Ap). The dial-protocol pair: **framed** = thermospheric density at a fixed altitude/satellite; **inferred** = density given the drivers. The synergy reading: does the JOINT law `density | (F10.7, Dst)` compress more than the additive sum of the marginal laws `density | F10.7` + `density | Dst` (held-out bits, model bits counted)? **Frame-dial event:** in a Gannon-class geomagnetic storm the geomag driver dominates; in quiet sun F10.7 dominates — the dominance/synergy should FLIP across the storm frame = a frame-reversal observable (the instrument register's signature). Disclose NRLMSIS/JB2008 as the standard driver models; our instrument reads the *synergy structure*, not prediction accuracy.

**Proposed S1 workflow (Fable):** inline-fetch + align (density + F10.7 + Dst over a window spanning a storm) -> parallel re-measure (the gain_v2 synergy gate under coders + the joint-vs-additive bit accounting; the storm-frame vs quiet-frame split) -> Opus adversary (is the "synergy" just both drivers being collinear? is the joint-compression gain a degrees-of-freedom artifact? in-sample vs held-out) -> synthesis (synergy reading + the storm frame-reversal + dead children + owed). Mirrors the cosmic-coin pattern; honors the gain_v2 misspecification discipline that the external pass sharpened.

## Sources
Thermosphere ML/data: [TU Delft](https://thermosphere.tudelft.nl/), [PANGAEA TND-IGG](https://doi.pangaea.de/10.1594/PANGAEA.931347), [Karman (GitHub)](https://github.com/spaceml-org/karman), [Acciarini 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023SW003652), [Pan 2025](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024SW004259), [Survey PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12995994/), [Gannon storm drag (arXiv)](https://arxiv.org/pdf/2406.08617), [swsc 2026](https://www.swsc-journal.org/articles/swsc/full_html/2026/01/swsc250083/swsc250083.html). TLE-history (abandoned path): [CelesTrak archives](https://celestrak.org/NORAD/archives/).
