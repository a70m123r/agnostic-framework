# PIPELINE — the review-and-update conveyor, on one page

Date: 2026-06-11 (written at Stage-1 finalize). Author: Fable.
Discipline: Tier-3; nothing here promotes anything; the convergence list stays 9.
Companions: `PIPELINE_GAP_ANALYSIS.md` (why this shape), `UI_GUIDELINES.md` (the law),
`REVIEW_THROUGH_THE_FRAMEWORK.md` (the lens), `reviews/README.md` (pin contracts),
the five scouted maps (`viewer-app.md`, `data-layer.md`, `substrate.md`,
`review-tool.md`, `toys-specs.md`).

---

## How one review flows end to end

```
 1. PIN            Pav long-presses in the viewer (served via :8742), comments, saves.
    = the ticket   The pin lands in reviews/pins.json at status OPEN with its EXACT
                   SLICE (.review.json: __getReviewState() — specimen, year, dials,
                   toggles, all six panels' position/collapsed/floating/hidden) and a
                   full-slice PNG (canvases + DOM panels/bars; review chrome excluded).

 2. TRIAGE         A wiki-armed agent reads the pin THROUGH THE FRAMEWORK LENS
    = the read     (a pin is a forcing event from the Pav-observer on the
                   viewer-wrapper; ask/give is the A-/A+ fold). It classifies the ask,
                   scopes it against the FROZEN LIST (SCHEMA_v2, 7 base specimens,
                   viewer_v0/v1/v2, frame_lock_data — route around, never through),
                   names the wiki pages + scout requests needed, and emits a patch
                   brief bound to named UI_GUIDELINES sections. Status -> ACKNOWLEDGED.

 3. SCOUTS         Read-heavy agents ingest whatever data the brief needs — citations
    = the fetch    mandatory, substrate appends are the ONLY data path (append-only
                   facts/verifications jsonl; never edit, never hand-write compiled/*).

 4. PATCH          One agent makes SURGICAL ADDITIVE edits under UI_GUIDELINES (the
    = the change   honesty conventions in §5 are correctness law, not taste). Embeds
                   are regenerated only via their named commands (_reembed_agnostic.js;
                   compile_substrate.py). Single-file viewers stay single-file.
                   Status -> ANSWERED when the approach is settled and communicated.

 5. GATE           Verification before any give is recorded (today's gates below;
    = the evidence Stage 2 collapses them into one command). Red gate = no give.

 6. GIVE           The response is recorded ON the pin via PATCH /pins/<id>:
    = the record   give{text, by, commit, at} + status -> APPLIED (appended to
                   history[], dated — the ledger is a dated record, never rewritten;
                   rejected asks are demoted/retired, never deleted).

 7. PAV VERIFIES   Pav clicks the pin -> "go to frame" replays the exact slice on the
    = the close    current build, old PNG alongside. He flips APPLIED -> VERIFIED
                   (or re-opens with a follow-up note). ONLY Pav sets verified;
                   agents cap at applied. This human close is the pipeline's ground
                   truth, by design.
```

Artifact contracts between stations: **pin record** = ticket · **.review.json** =
exact slice · **wiki** = map · **UI_GUIDELINES.md** = law · **gate verdict** =
evidence · **pins ledger (status history)** = dated record. (Stage 3 adds
**MANIFEST.json** = dependency graph.)

## Agent roles and model tiers

| Role | Model | Bound by | Notes |
|---|---|---|---|
| Scout (ingest, wiki refresh) | Claude Sonnet | append-only substrate rules; citations mandatory | cheap, parallel, read-heavy; never edits the viewer |
| Triage (pin -> patch brief) | Claude Fable (Sonnet for purely cosmetic pins) | wiki + framework lens + frozen list | classifies, scopes, routes |
| Patch / synthesis | Claude Fable | UI_GUIDELINES + wiki gotchas (+ manifest, once it exists) | surgical additive edits; runs the gate |
| Skeptic (adversarial review) | Claude Opus | the diff + the pin | escalation on load-bearing changes only |
| External pass | GPT-5.5 + Gemini | load-bearing claims only | the real external A- (workflow agent() is Claude-only) |
| Verifier | **Pav** | the replayed frame | the only role that can set `verified` |

## The verification gates (every patch, before its give)

1. **Syntax** — extract the app script (`/*APP_START*/../*APP_END*/`), `node --check`.
2. **Embedded lint** — `window.__lint()` on the live page returns `[]` (narration refs
   resolve; node sizes/solidity sane; substrate facts carry sources) — run with a
   specimen loaded, never vacuously.
3. **Replay smoke** — `__applyReviewState(slice)` then `__getReviewState()` roundtrip
   equality, including panel float/re-dock symmetry.
4. **Capture sanity** — composite contains the page's panels/bars
   (`__review.lastCapture`), review chrome absent.
5. **Honesty gates** — no proxy rendered as data, estimate/MODELLED tags travel,
   draw-nothing-when-data-absent (UI_GUIDELINES §5). The gate automates AROUND these,
   never through them.
6. **Server health** — :8742 restarted after server edits; `GET /pins` returns the
   registry. (Pins are loopback-only and unauthenticated — keep it that way.)

Today 1–4 run via `node --check` + a headless-Chrome CDP pass (node built-ins, no new
repo dependency); Stage 2 turns them into one scripted PASS/FAIL command with a
screenshot diff against the pin's own PNG.

## Next three stages (from the gap analysis)

- **Stage 1 — Pin lifecycle v1 + exact replay. SHIPPED 2026-06-11.** Bar converted to
  a managed panel (pin #1's ask), hooks landed, full-slice capture, PATCH/DELETE +
  ask/give/status on the server, pin #1 processed by the pipeline itself to `applied`.
  Remaining: a real commit SHA for the give, and Pav's in-frame `verified`.
- **Stage 2 — The gate as one command.** `review/check`: syntax + headless lint +
  replay smoke + thresholded screenshot diff at the pin's slice, PASS/FAIL + artifact
  paths. Exit: red on an injected fault, green on a clean tree. The one new dependency
  (headless harness) lives in `review/` tooling, never inside the instruments.
- **Stage 3 — Manifest + runbooks.** `wiki/MANIFEST.json` (source | generated | frozen
  | ledger, regen commands, gates), `wiki/TRIAGE_RUNBOOK.md`, scout brief template.
  Exit: a cold agent given only a pin id + the wiki produces a correct patch brief.

Horizons after that (dependency-ordered, undated): H1 scout fan-out -> H2 conveyor
orchestration over pin batches (automation still caps at `applied`) -> H3 toys and
future viewers riding the same server/gate.

## Honest limits

Scale = pin throughput on one localhost machine, not platform fantasy. Screenshot diff
is evidence, not proof. foreignObject capture is best-effort and disclosed
(`reviews/README.md`). The framework mapping is a lens — structural where it is
structural (forcing event, dated record), vocabulary where it is vocabulary — and no
qualitative reading is ever rendered as a measured value.
