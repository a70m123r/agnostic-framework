# Census instrument workflow — protocol DRAFT

**Status:** DRAFT, Tier-3, surfaced for Pav+Cowork ratification. **Nothing run/locked; convergence list still 9; no canon or ratified file touched.** This proposes the standard that makes the census instruments (heredity + niche-presence) and their prototype toys **plug into the already-ratified substrate/viewer system instead of forking a parallel one.**

It **does not redefine** `SUBSTRATE_SPEC.md`, `SCHEMA_v2.md`, or `PROXY_SPEC.md` — it *binds the census to them*. Where it adds anything census-specific, it adds it in their idiom.

> Companion files this governs: [heredity_classifier_section_DRAFT.md](heredity_classifier_section_DRAFT.md), [niche_presence_classifier_section_DRAFT.md](niche_presence_classifier_section_DRAFT.md). Standard it binds to: `../../candidates/canonical_genealogy/{SUBSTRATE_SPEC,SCHEMA_v2,PROXY_SPEC,VIEWER_SPEC}.md`.

---

## §0 — The realization (why this is short)

The standard you asked for **mostly already exists**, built for the genealogy specimens:

- **`SUBSTRATE_SPEC.md`** — append-only provenance'd **fact-log** (`facts/*.jsonl`) + a deterministic compiler → `substrate.db` (disposable) → **`compiled/*.json` (committed; what viewers ingest)**. No-fabrication discipline; certainty rubric; verification state machine; disputed-keeps-both.
- **`SCHEMA_v2`** — frame basis `{time, space, knowledge, meaning}`, per-node `frame_layer ∈ {physical, latent, straddle}`, graded membership `[0,1]` (D5), the design law (optional, default-empty).
- **`PROXY_SPEC.md`** — render channels as **versioned, disclosed proxies**, each with a **falsification target**; numbers live in one synced spec object, never inline magic numbers.
- **`VIEWER_SPEC` + `viewer_v*.html`** — the frame viewer: observer picker, physical/latent toggle, depth dial, timeline scrubber.

The census instruments are **the same kind of object the viewer already is** — a reader over the compiled substrate that returns a disclosed-proxy reading. So the protocol is mostly *"bind, don't fork."*

---

## §1 — The one rule (anti-divergence mandate)

**There is ONE substrate standard. The census does not invent a substrate structure.** It reuses `SUBSTRATE_SPEC`'s fact-log + `SCHEMA_v2`'s frame machinery + the compiler pattern + `PROXY_SPEC`'s proxy discipline. This is the rule that prevents Workspace Divergence (the multiple-copies-out-of-sync failure): if the census forks its own substrate shape, the viewer can't render it and the toys can't merge. One shape, one contract.

---

## §2 — Substrate structure (the shared record)

A **census substrate** (a thing being censused — RNA-world, immune system, oral tradition, software ecosystem, hurricane…) is recorded as a specimen conforming to `SCHEMA_v2`'s frame machinery. The instruments' **dial axes are not new structure** — they are a *reading-coordinate over existing SCHEMA_v2 fields*:

| Instrument dial axis (the DRAFTs) | Existing SCHEMA_v2 / substrate field | 
|---|---|
| **plane** (`physical` / `latent`) | `frame_layer.layer` + its graded `physical_membership` / `latent_membership` |
| **frame** (the copy-event lens) | `frame[] ⊆ {time, space, knowledge, meaning}` |
| **observer** (what individuates the unit) | node identity + `actors[].kind` (molecular-replicator … institution; individual-mind … canon) |
| **dial value** (`Q`, `E`) | a graded membership `[0,1]` (D5), recorded as facts |

Every substrate datum the instruments read is a **fact** in `facts/*.jsonl` (SUBSTRATE_SPEC format): real provenance, certainty per rubric, verification status, disputed-keeps-both. The instruments read the **compiled** best-values (`compiled/<substrate>.compiled.json`), exactly as the viewer does.

> **Placement proposal (decide):** census substrates are a *different object type* than theory-merges, so record them in a **parallel substrate instance** — `pilots/adversarial_bar_a/substrate/` using the **same `SUBSTRATE_SPEC` + the same `compile_substrate.py`** — rather than jamming them into `canonical_genealogy/specimens/`. Same standard, separate store.

---

## §3 — Instruments are reader/proxy-channels, not new pipelines

Each instrument is a pure function **`read(compiled_substrate, setting) → reading`**, where a *setting* is a {plane, observer, frame} point (§2). An admissible instrument:

1. **Consumes** `compiled/<substrate>.compiled.json` — the *same committed contract the viewer ingests*. No private input format.
2. **Emits a shared reading envelope** — `⟨substrate, setting, dial_value, toggle, [type], provenance_refs⟩`. Heredity returns `⟨Q, ABOVE|BELOW|UNDEFINED⟩`; niche returns `⟨E, PRESENT|ABSENT|UNDEFINED, sub-primitive⟩`. Same shape so they compare at matched settings and the viewer can render either.
3. **Reads its numbers from a versioned `CENSUS_PROXY_SPEC`** (the `PROXY_SPEC` pattern) — thresholds `Q_c`, `E_c`, estimator weights, effort floor — never inline. Doc and code object stay in sync; bump the version to change behaviour.
4. **Declares a falsification target per channel** (mandatory; the `PROXY_SPEC` / INSTRUMENT-meditation discipline): *what external signal would force this reading to retune or retire.* A channel with no falsification target is **not admissible** — that's the line between a measurement-shaped illustration and a measurement.
5. **Never fabricates.** A reading is a real base fact or a disclosed proxy. Critically: **`ABSENT` requires corroborated detection-effort facts** (§5); "we didn't look hard enough" resolves to `NO-CALL`, never `ABSENT`.

This retro-fits the two instrument DRAFTs onto the existing standard with zero new machinery: their `⟨dial, toggle⟩` readings *are* `PROXY_SPEC`-style channels.

---

## §4 — The toy → instrument merge contract (the thing you asked for)

A **toy is an instrument with narrower scope and/or synthetic data.** It is *mergeable* iff it conforms to three shared interfaces:

1. **Input contract** — it reads the same `compiled/*.json` shape (or a synthetic substrate authored in that shape), not its own embedded data blob.
2. **Output contract** — it emits the same reading envelope (§3.2).
3. **Proxy contract** — its tunable numbers live in (or graduate into) the versioned `CENSUS_PROXY_SPEC`, not inline.

A toy meeting all three **merges by substitution**: swap its synthetic-data guts for the real estimator and the harness is unchanged — the exact graduation path the frame-lock pilot's ground-truth harness was built for (validate logic on known answers → swap in real data). On graduation, the toy's `read()` fn + its proxy numbers move into the instrument + `CENSUS_PROXY_SPEC`; the toy **stays in `toys/` as a lineage artifact** (the `viewer_v0→v1` copy-don't-mutate rule).

> **Honest status of the current toys:** `composition_spectrograph_toy.html` and `time_axis_toy.html` are **standalone with embedded data and inline numbers** ("MODELLED shape — not measured shares"). They are good exploration but **do not meet the merge contract as written** — they hold their own data and tunables. This protocol is the forward standard the *next* toy generation must meet to be merge-able rather than throwaway. (Retrofitting the two existing toys to the contract is optional and low-priority.)

---

## §5 — Provenance / verification / frame-lock (inherited wholesale)

- **Fact-log discipline** is inherited verbatim from `SUBSTRATE_SPEC`: no fabrication; skip rather than guess; proxies/estimates labelled and capped low; **disputed facts keep both values**; append-only; `substrate.db` disposable; `compiled/*.json` is the contract.
- **The detection-effort proxy maps straight onto the verification state machine** (a real gain from reusing the standard): a substrate-setting cell may read **`ABSENT` only if ≥1 `corroborated` detection-effort fact** says we searched adequately and found no nameable beneficiary+cost. `pending` / `unverifiable` effort → **`NO-CALL`**. "We didn't look" can no longer masquerade as "nothing there" — the existing machinery enforces it.
- **Frame-lock binds at the compiled-snapshot layer** (per `frame_lock_protocol §7`): the lock file SHA-records `{dial grid + CENSUS_PROXY_SPEC version + the compiled-substrate snapshot hash + called-shots + scoring rule}`, committed before any reading is examined; git strict-ancestry comes **free** from the append-only log. Recompute-and-match + `git merge-base --is-ancestor` at result-commit.

---

## §6 — The build/run loop (the ordered workflow)

1. **Record** census substrates as facts (`SUBSTRATE_SPEC` format) → `compile_substrate.py` → `compiled/*.json`.
2. **Lock** the dial grid + `CENSUS_PROXY_SPEC` version + falsification targets + per-cell called-shots + the §5.1-R scoring rule (frame-lock, §5).
3. **Validate on toys** — synthetic substrates with known answers, run through the *real* instrument harness (merge contract, §4). The ground-truth leg; catches inverted/backwards logic before real data (frame-lock-pilot pattern).
4. **Run** the instruments over the compiled real substrates → reading envelopes (the sweep).
5. **Score** §5.1-R co-variation at matched settings per the locked rule (PASS / FAIL / INCONCLUSIVE).
6. **Result-commit** with three skeptics + an independent re-run + the lock recompute-and-match.

Every step is an existing discipline; nothing forks.

---

## §7 — Reuse vs add (honesty table)

| Reused as-is (do not re-derive) | Added (census-specific, Tier-3) |
|---|---|
| `SUBSTRATE_SPEC` fact-log + compiler + verification machine | the two reading **instruments** (heredity / niche) as new proxy channels |
| `SCHEMA_v2` frame basis + `frame_layer` + graded membership | the **dial-grid** as a reading-coordinate over those fields (§2) |
| `PROXY_SPEC` versioned-proxy + falsification-target discipline | `CENSUS_PROXY_SPEC` (a new instance of that pattern) |
| the `compiled/*.json` viewer contract | the shared **reading envelope** (§3.2) |
| `frame_lock §7` SHA + git-ancestor lock | lock binds the compiled-snapshot + proxy-version (§5) |
| `viewer_v*` copy-don't-mutate lineage rule | the **toy→instrument merge contract** (§4) |

---

*Provenance: drafted 2026-06-11 by Claude Code at Pav's request — a workflow standard so census instruments + toys bind to the ratified substrate/viewer system rather than forking it. Grounded in a read of `SUBSTRATE_SPEC`, `SCHEMA_v2`, `PROXY_SPEC`, `VIEWER_SPEC`, and the current `substrate/` + `toys/` state. Tier-3, surfaced for ratification. Could graduate to a `canonical_genealogy/`-level standard governing all instruments if Pav wants it to. Nothing run/locked; convergence list still 9.*
