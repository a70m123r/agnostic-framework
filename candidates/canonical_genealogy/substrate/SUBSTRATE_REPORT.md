# Compiled Substrate — Build Report

**Generated:** 2026-06-10 (UTC) · compiler: `compile_substrate.py` · build: `python compile_substrate.py` (full build, all 7 specimens) · Python 3.12.9, stdlib only.

> **Revision — 2026-06-10, Opus-audit fold.** This report has been updated after an independent Opus audit. Two concrete fixes landed (qm-relativity provenance failure re-sourced; cross-file `fact_id` collision eliminated for the last two seats), the compiler was hardened, and the build was fully recompiled. The de-leak corrected the headline numbers **downward** (verified% 37.9 → **32.7**, disputes 27 → **22**, flags 129 → **1**). All numbers below reflect the post-audit rebuild. See **§10 — Opus audit fold** for the full diff.

**Status:** Tier-3 exploratory data-harvest infrastructure for the canonical wrapper-genealogy specimens. NOT canon, NOT a tier promotion, does NOT grow the convergence list (convergence stays **9**). Honest discipline: no fabrication; every fact carries a real source URL + retrieval stamp; estimates/proxies are labelled with basis and capped low; disputed facts keep BOTH values.

This report describes what the **append-only fact log** currently contains after the 7-seat harvest + verification pass, exactly as the compiler resolved it. It reports only what the logs hold — nothing here is fabricated or inferred beyond the recorded provenance.

---

## 1. Build result (headline)

| Metric | Value |
|---|---|
| Facts loaded | **1029** |
| Verification records loaded | **303** |
| Best values resolved | **771** `(specimen, subject_id, predicate)` groups |
| Distinct subjects | 396 (273 base-specimen nodes + 123 new `proposed:` nodes) |
| Distinct predicates | 20 |
| **Validation errors (fatal, records skipped)** | **0** |
| Validation flags (non-fatal) | **1** |
| Disputed best values (both values retained) | **22** |
| Specimens with facts | 7 / 7 |
| Compiled exports written | 7 + `_summary.json` |
| `substrate.db` (SQLite, never committed) | 2.24 MB |

**The build is clean: 0 validation errors.** The compiler ran end-to-end, built `substrate.db`, and wrote all 7 `compiled/<specimen>.compiled.json` exports plus `compiled/_summary.json`.

### Compiler hardening — one defect fixed (Opus-audit fold)
The first build carried **128 duplicate-`fact_id` flags** that were *not* benign as originally reported. Two seats (`manhattan` **and** `maxwell`) reused a single `fact_id` namespace across their `entities` and `events` files. Because the compiler keys verifications and disputed-alternatives on the **bare `fact_id`** (`bucket_for`, `resolve_best`), a verification authored against the *entities* twin **leaked** its bucket onto an unrelated *events* twin in a different `(specimen, subject_id, predicate)` group — silently fabricating both corroborations and disputes. This was a real pipeline defect, now fixed:

- **Data fix — disjoint id namespaces.** The 69 `maxwell.events.jsonl` and 63 `manhattan.events.jsonl` `fact_id`s were renumbered to a disjoint `f-<specimen>-e####` namespace (the convention `deep-learning` / `internet` / `keynesian` already used; `darwin-mendel` and `quantum-gravity` were already disjoint by a different prefix). **Only the `fact_id` token changed** on each line — every value, source, certainty and stamp is byte-identical. After renumber there are **0** cross-file duplicate ids.
- **Compiler fix — hazard guard.** `compile_substrate.py` now detects any `fact_id` reused across facts in **different** resolution groups and raises a **fatal `HAZARD` error** (exit 2), so this class of silent leak can never recur. A duplicate id *within* one group (genuine multi-attestation) stays a benign non-fatal flag.

The single remaining flag is honest by design:
- **1 flag — `qm_relativity.jsonl:31` `f-qg-0057` `second_source.type 'None'`.** A genuinely `unverifiable` record (the 1988 Osgood-Hill renaming of the Wheeler-DeWitt equation could not be independently corroborated). Its `second_source` is an honest empty object `{}` — no fabricated source. The flag is the *correct* signal for an unverifiable record and is non-fatal by design.

---

## 2. Facts per specimen

| Specimen | Facts | Best values | Subjects | Predicates |
|---|--:|--:|--:|--:|
| darwin-mendel-modern-synthesis | 153 | 107 | 54 | 17 |
| deep-learning | 142 | 95 | 59 | 19 |
| internet | 178 | 134 | 61 | 19 |
| keynesian-economics | 149 | 126 | 63 | 18 |
| manhattan-project | 146 | 107 | 57 | 17 |
| maxwell-electromagnetism | 134 | 92 | 34 | 19 |
| quantum-gravity | 127 | 110 | 69 | 14 |
| **TOTAL** | **1029** | **771** | 396 distinct | 20 distinct |

---

## 3. Verification statistics

### 3.1 Verification records (303 total, append-only, fact-level)

| Status | Records | Share |
|---|--:|--:|
| corroborated | 275 | 90.8% |
| disputed | 23 | 7.6% |
| unverifiable | 5 | 1.7% |

300 distinct `fact_id`s carry at least one verification record. (Audit-fold delta: +1 corroborated and +1 unverifiable from the qm-relativity re-source in §10; +1 re-keyed dispute target, no net change to the disputed count.)

### 3.2 Resolved best values (771 groups, what viewers ingest)

The compiler assigns each best value a **bucket** from all verifications on its member facts (corroborated > pending > disputed; unverifiable ~ pending-trust but flagged).

| Bucket | Best values | Share |
|---|--:|--:|
| **corroborated** | **252** | **32.7%** |
| pending (no verification yet) | 504 | 65.4% |
| disputed | 11 | 1.4% |
| unverifiable | 4 | 0.5% |

**Verified % (corroborated best values / all best values) = 32.7%.** The remaining 65.4% are still `pending` (harvested with provenance, not yet second-sourced).

> **Honest correction (Opus-audit fold).** The first build reported **37.9%** verified / 60.2% pending. That figure was **inflated by the same cross-file `fact_id` leak** that inflated the dispute count: ~40 `maxwell`/`manhattan` *events*-twin best-values inherited a `corroborated` bucket from an entities-twin verification they did not actually share. After the de-leak, those 40 correctly fall back to `pending`. **32.7% is the honest verified ceiling**; 37.9% was an artifact. The drop is concentrated entirely in the two affected seats (see §3.3).

### 3.3 Per-specimen verification + certainty + freshness

| Specimen | best | corrob | pending | disp | unver | verified % | certainty min/mean/max |
|---|--:|--:|--:|--:|--:|--:|---|
| darwin-mendel-modern-synthesis | 107 | 27 | 76 | 4 | 0 | 25.2% | 0.25 / 0.821 / 0.90 |
| deep-learning | 95 | 28 | 64 | 3 | 0 | 29.5% | 0.30 / 0.838 / 0.98 |
| internet | 134 | 39 | 94 | 1 | 0 | 29.1% | 0.40 / 0.814 / 0.95 |
| keynesian-economics | 126 | 42 | 83 | 0 | 1 | 33.3% | 0.35 / 0.820 / 0.95 |
| manhattan-project | 107 | 37 | 69 | 1 | 0 | 34.6% | 0.30 / 0.841 / 0.95 |
| maxwell-electromagnetism | 92 | 37 | 52 | 1 | 2 | 40.2% | 0.30 / 0.835 / 0.95 |
| quantum-gravity | 110 | 42 | 66 | 1 | 1 | 38.2% | 0.40 / 0.816 / 0.95 |

After the de-leak, verified% is **flat across all seats (25–40%)**, not the 62%/54% the first build reported for Maxwell/Manhattan. Maxwell (40.2%) and quantum-gravity (38.2%) now lead narrowly; **Darwin-Mendel is still the least-verified (25.2%)** — the clearest honest target for the next verification pass. The Maxwell/Manhattan drops (62→40, 54→35) are exactly the falsely-corroborated events twins reverting to `pending`.

---

## 4. Disputed facts — all 22, both values retained

The compiler **never silently overwrites a disputed value.** Every group below carries both the harvester's best value and the verifier's `value_found`, with both sources. The first build listed **27** disputes; **5 net were removed in the Opus-audit fold** — they were *artifacts* of the cross-file `fact_id` leak (a verifier's dispute about one twin leaking onto an unrelated events-twin group). One genuine dispute (Oppenheimer's clearance date, #14 below) moved to its correct home as part of the same fix. Of the 22 that remain, **16 are genuine value conflicts** (2 of them verifier-side mis-sources, flagged and kept) and **6 are "soft" disputes** where the verifier's leading value matches the best value but the record was filed `disputed` for a precision/source caveat — retained verbatim per honest discipline rather than reclassified.

### 4.1 Genuine value conflicts (different values on both sides)

| # | Specimen / subject / predicate | Best value (source) | Disputed value_found (source · verifier) |
|---|---|---|---|
| 1 | darwin-mendel / Carl von Naegeli / born | `1817-03-26` (Wikipedia) | `1817-03-27` (Britannica · claude-sonnet-4-6-verifier-01) |
| 2 | darwin-mendel / Weismann germ-plasm theory / formulated | `1886` (ASU Embryo Project) | `1885` (ASU Embryo Project · claude-sonnet-4-6-verifier-01) |
| 3 | darwin-mendel / proposed:eclipse-of-darwinism / active_to | `~1930s` (Wikipedia) | `~1920` (Wikipedia · claude-sonnet-4-6-verifier-01) |
| 4 | darwin-mendel / proposed:eugenics-term / gatekeeping_event | US compulsory-sterilization narrative (~60,000+ sterilized) | `~12,000 by 1947; >64,000 total` (Buck v. Bell, Wikipedia · claude-sonnet-4-6-verifier-01) — count discrepancy |
| 5 | deep-learning / act-fukushima / born | `1936-01-01` (Wikidata Q61904879) | `1936-03-16` (Britannica · sonnet-verifier-01) — exact day |
| 6 | deep-learning / act-miti / dissolved | `1992` (Wikipedia FGCS) | `1992 main project / 1994 follow-on` (ACM DL · sonnet-verifier-01) |
| 7 | deep-learning / act-pdp (Rumelhart) / died | `2011-03-13` (correct) | `2023-04-20` (TechCrunch · sonnet-verifier-01) — verifier mis-sourced (Google DeepMind merger date); flagged, kept |
| 8 | deep-learning / act-symbolics / founded | `1980` (correct) | value_found is a mis-filed note about Rumelhart's birthplace (verifier targeted the wrong subject) — flagged, kept |
| 9 | deep-learning / proposed:donald-hebb / born | `1904-07-22` (corroborated) | `July 20, 1904` (McGill TheBrain PDF · sonnet-verifier-01) |
| 10 | deep-learning / sw-cuda / formulated | `2007-02-15` (Wikipedia CUDA) | `Feb 2007 SDK v0.8 / Jun 2007 CUDA 1.0` (arXiv · sonnet-verifier-01) |
| 11 | internet / act-cyclades / dissolved | `1981` (Wikipedia CYCLADES) | `canceled by 1978 (CHM) / shut down 1981 (Wikipedia)` (Computer History Museum · sonnet-verifier-01) |
| 12 | internet / rel-arpanet / dissolved | `1990-02-28` (Internet Society) | `1990 (year confirmed; Feb 28 exact day not independently corroborated)` (Internet Society · sonnet-verifier-01) |
| 13 | keynesian / act-kalecki / died | `1970-04-18` (Wikipedia infobox) | `1970-04-17` (Wikidata Q436745 preferred rank, citing Soviet encyclopedia + Australian Hist. Soc. · sonnet-verifier-01) |
| 14 | manhattan / act-oppenheimer / gatekeeping_event | Security clearance revoked by AEC **27 May 1954** (Gray Board recommendation) | `1954-06-29` (AHF Nuclear Museum · sonnet-verifier-01) — date of the AEC's *formal* revocation, 32 h before expiry. **Re-keyed in the audit-fold** from `f-manhattan-0009` (a mis-key that had leaked onto `act-groves/died`) to its correct events twin `f-manhattan-e0008` |
| 15 | quantum-gravity / Matvei Bronstein / born | `1906-12-02` (Wikipedia N.S.) | `1906-11-19` Julian/O.S.; harvest events-file had `1906-01-15` (Wikidata Q1226083 · sonnet-verifier-qm-relativity-01) — calendar-system conflict |
| 16 | quantum-gravity / proposed:leonard-susskind / born | `1940-06-16` (Wikipedia infobox) | `1940-05-20` (Wikidata Q203243 preferred P569, Stanford LennyFest archive · sonnet-verifier-qm-relativity-01) |

(Items 7 and 8 are verifier-side mis-sources the seats explicitly flagged and **kept** rather than overwrote — honest discipline: the conflict is preserved for a human to adjudicate, the best value remains the historically correct one. Item 14 is a *correctly-placed* historiographic dispute after the re-key.)

### 4.2 Soft disputes (verifier's leading value matches best; filed disputed for a caveat)

| # | Specimen / subject / predicate | Best value | Note on the dispute record |
|---|---|---|---|
| 17 | darwin-mendel / Morgan Drosophila genetics / conceived | `1910` | value_found `1910` — same year; caveat on range ~1910–15 |
| 18 | deep-learning / act-openai / founded | `2015-12-11` | two records, both `2015-12-11` (TechCrunch) — duplicate verification filed disputed |
| 19 | manhattan / act-med / dissolved | `1947-01-01` | value_found `1947-01-01` — same value, AEC-transfer caveat |
| 20 | manhattan / act-osrd / dissolved | `1947-01-20` | value_found `1947-01-20` — same value |
| 21 | maxwell / proposed:cavendish-laboratory / founded | `1874` | value_found `1874` — same value, Maxwell-appointment-year caveat |
| 22 | maxwell / proposed:george-fitzgerald / died | `1901-02-21` | value_found `1901-02-21` — same value; events-file Maxwellians twin gives `1901-02-22` (1-day intra-harvest caveat) |

All 22 are preserved with both values in `compiled/_summary.json → disputes[]` and in each affected `compiled/<specimen>.compiled.json → …disputed_alternatives[]`. The 5 net-removed entries (former #13/#14/#19/#22/#24 — Oersted/conceived, Maxwell/gatekeeping, Conant/born, Oppenheimer/now_refresh, national-labs/consolidated) were leak artifacts and are documented in §10.

---

## 5. Coverage per gap (a)–(g) — filled vs still-missing

The harvest targeted the seven known viewer-v1 gaps. Predicates map to gaps as follows; counts are fact rows.

| Gap | Description | Predicates | Facts | Status |
|---|---|---|--:|---|
| **(a)** | Entity lifecycles (born/died/founded/dissolved/conceived/formulated/named/active_from/active_to) | 9 predicates | **771** | **Filled, dense** — all 7 specimens, every category populated (+1 from the qm re-source in §10) |
| **(b)** | Consolidation dates (action-spaces / cultural-harvest / descendants) | consolidated, unlocked_when, harvested_when | **77** | **Filled** — all 7 specimens; `harvested_when` thin (1) |
| **(c)** | 2024–2026 now-refresh events per lineage | now_refresh_event | **54** | **Filled** — all 7 specimens; 39 of 54 fall in 2023–2026 (17×2024, 12×2025) |
| **(d)** | Rival fates (faded / absorbed / persists / niche, with when) | rival_fate | **31** | **Filled** — all 7 specimens; all four enum values present (faded 10, persists 10, absorbed 5, niche 5, +1 "dissolved") |
| **(e)** | D6 friction (gatekeeping / publication-lag / adoption-lag / propagation / bandwidth) | 5 predicates | **74** | **Filled from zero** — was schema-defined with ZERO specimen data; now all 7 specimens have D6 facts (gatekeeping 24, propagation 20, publication_lag 15, adoption_lag 11, bandwidth 4) |
| **(f)** | Theory-DNA bases (per-parent contribution shares, estimates, certainty ≤ 0.6) | contribution_share | **22** | **Filled, correctly capped** — all 22 at certainty ≤ 0.6, basis in notes; 0 cap violations |
| **(g)** | Anything else an aggregator cleanly provides → new schema field | (none) | **0** | **No residual** — every harvested datum mapped cleanly onto the (a)–(f) vocabulary; no orphan predicate needed |

### Per-specimen gap matrix (fact counts)

| Specimen | a | b | c | d | e | f |
|---|--:|--:|--:|--:|--:|--:|
| darwin-mendel | 126 | 6 | 7 | 2 | 10 | 2 |
| deep-learning | 98 | 10 | 11 | 4 | 14 | 5 |
| internet | 131 | 17 | 11 | 6 | 11 | 2 |
| keynesian | 107 | 18 | 4 | 5 | 9 | 6 |
| manhattan | 113 | 13 | 8 | 4 | 6 | 2 |
| maxwell | 102 | 7 | 5 | 3 | 13 | 4 |
| quantum-gravity | 94 | 6 | 8 | 7 | 11 | 1 |

**Every (specimen × gap a–f) cell is non-empty.** No specimen is missing any gap category.

### What the fleet could NOT find (honest still-missing list)

The aggregators answered the *structure* of every gap, but coverage is uneven and several specific facts stayed thin or unverifiable:

- **Verification depth (the biggest hole):** **65.4%** of best values are still `pending` — harvested with provenance but not yet second-sourced (up from the first build's 60.2% once the leaked false-corroborations were corrected). Darwin-Mendel (25% verified) and the deep-learning/internet seats (~29%) are the weakest. This is a *verification* gap, not a *harvest* gap.
- **Gap (b) `harvested_when`:** only 1 fact across all specimens — cultural-harvest item dates are the thinnest temporal category; most harvest items have no clean aggregator date.
- **Gap (e) `bandwidth_fact`:** only 4 facts (Maxwell, Keynesian ×2, deep-learning) — propagation *bandwidth* is the hardest D6 datum to source cleanly; most friction facts are gatekeeping/lag events instead.
- **Exact-day precision on 19th/early-20th-c. births/deaths:** several disputes (Naegeli 26 vs 27 Mar; Weismann 1885 vs 1886; Hebb Jul 20 vs 22; Susskind May 20 vs Jun 16; Bronstein O.S./N.S.) reflect genuine aggregator disagreement the fleet could not resolve to a single day — both values retained.
- **One genuinely unverifiable claim:** the 1988 Osgood-Hill renaming of the Wheeler-DeWitt equation (`f-qg-0057`) — appears in Rovelli's history paper but no independent second source confirms the conference/date; marked `unverifiable`, not deleted.
- **One provenance failure, re-sourced (Opus-audit fold):** `f-qm-relativity-0025` (QG-phenomenology field "born ~1997") originally cited an arXiv paper that does not attest the value. It was marked `unverifiable` (cited source fails) and **re-sourced** to the primary Amelino-Camelia et al. *Nature* 393:763 (1998) paper plus the founder's own field review — see §10. Old line retained; corrected value carries proper provenance.

---

## 6. Freshness distribution

**Harvest freshness (`retrieved_at`):** all 1029 facts were retrieved on **2026-06-10 (UTC)** — a single-day harvest. Maximally fresh; the original 1028 span 02:23–02:42 UTC, and the single audit-fold re-source fact carries 03:06 UTC. This is the freshness signal the compiler uses as a best-value tie-breaker (newer wins).

**Source freshness (`source.published_or_updated`)** — when the cited page/source was itself last published or updated:

| Era | Facts | Reading |
|---|--:|---|
| 2026 | 869 | Encyclopedia/aggregator pages with a current "last-updated" stamp (Wikipedia/Wikidata live pages) |
| 2024–2025 | 35 | Recently-updated pages and news for the now-refresh (gap c) events |
| 2010–2023 | 70 | News + academic sources, mostly for modern-era lineages (deep-learning, internet) |
| 1931–2008 | 40 | Primary/academic sources (papers, org records) for mid-century events (incl. the 1998 *Nature* QG-phenomenology re-source from §10) |
| 1846–1867 | 3 | Primary historical sources (e.g. Maxwell-era publications) |
| (no date exposed) | 12 | Source exposes no publish/update date; recorded as `""` per spec |

The long tail to 1846 is the **primary/academic** layer (60 primary + 63 academic facts) anchoring old events to contemporaneous sources; the 2026 bulk is the **encyclopedia/aggregator** layer (828 encyclopedia + 68 aggregator) carrying live last-updated stamps.

**Source-type mix (provenance strength):** encyclopedia 828 · aggregator 68 · academic 63 · primary 60 · news 10. Encyclopedia-dominant, as expected for a biographical/lifecycle harvest, with a respectable structured-aggregator + primary spine for the load-bearing dates. (Academic +1 vs the first build: the qm re-source replaced a non-supporting arXiv citation with the primary *Nature* 1998 paper.)

---

## 7. Certainty distribution

Per the §3 rubric (structured-aggregator 0.7–0.9; single encyclopedia 0.5–0.7; single news 0.4–0.6; historiographic estimate ≤ 0.5 / contribution_share ≤ 0.6).

| Band | Facts | Share |
|---|--:|--:|
| > 0.90 (two independent structured sources) | 52 | 5.1% |
| 0.70 – 0.90 (structured-aggregator-attested) | 927 | 90.1% |
| 0.50 – 0.69 (single encyclopedia) | 28 | 2.7% |
| 0.30 – 0.49 (single news / estimate) | 20 | 1.9% |
| < 0.30 (low-confidence estimate) | 2 | 0.2% |

**min 0.20 · mean 0.827 · median 0.85 · max 0.99.** The distribution is healthy: the bulk sits in the aggregator band, estimates are correctly pushed low, and the two <0.30 facts are flagged historiographic estimates. **All 22 `contribution_share` (theory-DNA) facts are ≤ 0.6 — zero cap violations**, satisfying the hard rule that theory-DNA shares are always estimates.

---

## 8. Compiled exports (the committed viewer artifacts)

Written by this build to `substrate/compiled/`:

| Export | Size |
|---|--:|
| `darwin-mendel-modern-synthesis.compiled.json` | 70.5 KB |
| `deep-learning.compiled.json` | 62.8 KB |
| `internet.compiled.json` | 78.6 KB |
| `keynesian-economics.compiled.json` | 76.3 KB |
| `manhattan-project.compiled.json` | 68.3 KB |
| `maxwell-electromagnetism.compiled.json` | 57.4 KB |
| `quantum-gravity.compiled.json` | 72.8 KB |
| `_summary.json` (coverage + freshness + certainty + disputes rollup) | 23.9 KB |

Each `<specimen>.compiled.json` holds best values grouped by subject, with `provenance_refs` (every contributing `fact_id`), bucket, certainty, source, and `disputed_alternatives[]` where present. The manhattan/maxwell/`_summary` files shrank in the audit-fold because the leaked, duplicated `disputed_alternatives[]` blocks were removed. `substrate.db` (2.24 MB SQLite: `facts`, `verifications`, `best_values`) is rebuilt every run and is **never committed** (`.gitignore`).

---

## 9. The scale story (how this grows)

Append-only logs are the source of truth; everything else is derived and disposable.

- **Source of truth — `facts/*.jsonl` + `verifications/*.jsonl`** (git-native, one record per line, append-only). 1029 facts + 303 verifications across 14 fact files + 7 verification files today. Diff-friendly, mergeable, never rewritten. **Re-harvest = append a newer fact** (newer `retrieved_at` wins on ties); **new specimen = new fact files** (no schema change — the compiler discovers specimens by globbing `../specimens/*.json` and `facts/*.jsonl`).
- **Compiled index — `substrate.db`** (SQLite, rebuilt from the logs every run, never committed). 2.24 MB today. Queryable for analysis; disposable.
- **Viewer contract — `compiled/<specimen>.compiled.json` + `_summary.json`** (committed). Stable best-value exports that viewers ingest, regardless of backend.
- **Forward path:** (1) a future `--ingest-overlays` flag folds `../overlays/*.overlay.json` into the same fact stream so overlays and harvest facts resolve through one pipeline; (2) verification depth grows by appending more `verifications/*.jsonl` records — the 65.4% `pending` best values are the obvious next target, lifting verified% without re-harvesting; (3) if SQLite outgrows one file, the identical `facts`/`verifications`/`best_values` schema lifts unchanged to Postgres (swap the DB-API connection; resolution logic is engine-agnostic Python over loaded rows). The committed JSON exports remain the stable viewer contract throughout.

**Convention converged (Opus-audit fold):** all 7 seats now use disjoint `fact_id` namespaces — five via an `e####` events split (`deep-learning`/`internet`/`keynesian`, plus `maxwell`/`manhattan` renumbered in the audit-fold), two by a distinct entities prefix (`darwin-mendel` uses `f-dm-*`, `quantum-gravity` uses `f-qg-*`). There are **0** cross-file duplicate `fact_id`s. The compiler additionally now raises a **fatal `HAZARD` error** on any `fact_id` reused across different resolution groups, so a future seat cannot silently reintroduce the leak. The earlier first-build claim that "six of seven seats renumbered to `e####`, only Manhattan shared" was inaccurate on both counts (only three used `e####`; *two* seats — Manhattan **and** Maxwell — actually collided); corrected here.

---

## 10. Opus audit fold (2026-06-10)

An independent Opus audit sampled 15 facts, fetched 5 cited sources, re-ran the compiler, and full-scanned all records for schema compliance. Its verdict was **ACCEPT WITH FIXES**: schema compliance clean (0 / 1028), compiler deterministic and reproducing every headline number, disputes retaining both values, theory-DNA cap holding, and 4 of 5 fetched sources fully supporting their values. It surfaced **two concrete issues** and several already-disclosed ones. Both concrete issues are now fixed; the build was fully recompiled. No fact was silently deleted — corrections are append-only with retraction records.

### 10.1 Fix 1 — harvest integrity: `f-qm-relativity-0025` provenance failure
**Finding.** The fact "QG-phenomenology field born ~1997" cited `arxiv.org/pdf/1002.0349`, which is **Vasileiou 2009, a Fermi-LAT GRB-090510 Lorentz-violation *measurement*** — it contains zero occurrences of "1997" or "phenomenology" and does **not** attest the value. The value is plausibly true in the literature, but *this source* did not support it: a provenance failure of exactly the kind honest discipline forbids. (It was still `pending`, so no verifier had caught it.)

**Fix (append-only, no deletion).**
1. **Re-sourced** with a new fact `f-qm-relativity-0057` (same `(subject, predicate)` group) citing the **primary seminal paper itself**: Amelino-Camelia, Ellis, Mavromatos, Nanopoulos & Sarkar, *"Potential Sensitivity of Gamma-Ray Burster Observations to Wave Dispersion in Vacuo,"* arXiv:astro-ph/9712103 (submitted 1997-12-07), **Nature 393:763–765 (1998)** — the founding GRB-dispersion proposal. Both sources independently fetched and confirmed.
2. **Corroborated** `f-qm-relativity-0057` with a second independent academic source: Amelino-Camelia's own field review *"Quantum Spacetime Phenomenology,"* Living Reviews in Relativity 16:5 (2013), arXiv:0806.0339.
3. **Retraction record** on the old `f-qm-relativity-0025`: status `unverifiable`, notes stating the cited arXiv:1002.0349 fails to attest the value and pointing to the re-source. The old line is retained in history; the compiler now resolves the group to the corrected, corroborated value.

### 10.2 Fix 2 — pipeline integrity: cross-file `fact_id` collision (the verification leak)
**Finding.** The compiler keys verifications and `disputed_alternatives` on the **bare `fact_id`**. Two seats — **`manhattan` (63 ids)** and **`maxwell` (65 ids)**, not just Manhattan as the first build claimed — reused one `fact_id` namespace across their `entities` and `events` files. 121 of 128 shared ids spanned *different* `(specimen, subject_id, predicate)` groups, so a verification authored against an entities twin **leaked** its bucket onto an unrelated events twin. This inflated **both** the verified% (false corroborations) and the dispute count (false disputes).

**Fix (data + compiler).**
- **Renumbered** the 69 `maxwell.events.jsonl` and 63 `manhattan.events.jsonl` `fact_id`s to a disjoint `f-<specimen>-e####` namespace. Only the `fact_id` token changed per line; every value/source/certainty/stamp is byte-identical. Result: **0** cross-file duplicate ids (down from 128 flags → the now-single honest flag).
- **Re-keyed** exactly one mis-keyed dispute: the verifier's own note named `f-manhattan-0008`'s `act-oppenheimer/gatekeeping_event` twin, but the record was keyed to `f-manhattan-0009` (leaking onto `act-groves/died`). Re-pointed to `f-manhattan-e0008` with a `QC-FIX` note, so the genuine 1954-05-27-vs-06-29 clearance-date dispute lands on Oppenheimer's gatekeeping event (now §4.1 #14) instead of falsely on Groves' death.
- **Hardened** `compile_substrate.py`: a `fact_id` reused across *different* resolution groups is now a **fatal `HAZARD` error** (exit 2). A duplicate within one group stays a benign flag. This class of silent leak can no longer recur.

### 10.3 Net effect on the headline numbers

| Metric | First build | Post-audit | Why |
|---|--:|--:|---|
| Facts | 1028 | **1029** | +1 re-sourced qm fact |
| Verifications | 301 | **303** | +1 corroboration, +1 retraction |
| Validation flags | 129 | **1** | 128 false duplicate-id flags eliminated |
| Validation errors | 0 | **0** | (hazard guard satisfied) |
| **Verified %** | 37.9% | **32.7%** | ~40 leaked false-corroborations reverted to `pending` (honest ceiling) |
| Disputed best values | 27 | **22** | 5 net leak artifacts removed; 1 genuine dispute re-homed |
| Disputed bucket / unverifiable bucket | 10 / 5 | 11 / 4 | de-leak + qm re-source reshuffle |
| Theory-DNA cap | 22 ≤ 0.6 | **22 ≤ 0.6** | unchanged (0 violations; max 0.45) |

### 10.4 Findings the audit confirmed were *already* honestly disclosed (no change needed)
- The duplicate-`fact_id` defect and the verification-attach-to-wrong-twin risk were self-disclosed in the first build's §1 — the audit confirmed "documented, not hidden." (Now fixed outright.)
- The 60.2% → **65.4%** `pending` verification hole is the real coverage ceiling, not a harvest gap.
- `f-qg-0057` (1988 Wheeler-DeWitt renaming) is the single legitimately `unverifiable` claim, with an honest empty `second_source={}` — correctly handled, retained.
- Two §4.1 disputes (#7 `act-pdp/died`, #8 `act-symbolics/founded`) are verifier-side mis-sources kept verbatim per honest discipline; the best value remains historically correct.

**Bottom line.** The one genuine provenance failure is corrected with a primary source; the one pipeline defect is fixed in both data and compiler and guarded against recurrence; the headline verified% is now the *honest* 32.7% rather than the leak-inflated 37.9%. The substrate remains a reproducible, non-fabricated, append-only fact log.

---

*Tier-3 exploratory data-harvest substrate for Cowork+Pav ratification — NOT canon, NOT a tier promotion, does NOT grow the convergence list (convergence stays **9**). Honest discipline: no fabrication; every fact carries real provenance; estimates/proxies labelled with basis and capped low; disputed facts keep both values. Post-audit build of 2026-06-10: 1029 facts, 0 validation errors, 1 (honest) flag, **32.7% verified**, **22 disputes** retained in full.*
