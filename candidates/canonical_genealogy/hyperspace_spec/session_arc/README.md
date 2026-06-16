# session_arc — the tomographic self-capture (2026-06-16)

The instrument turned on its own history. This folder captures the **2026-06-11 → 06-16 milestone arc** (the work since viewer_v3) as an append-only **substrate** — the *acts* (atomic events) and the *arcs* (storyline threads) — with provenance, a verification pass, and a timeline viewer. Built with the same honest-measurement discipline the milestone itself produced.

## How it was made (the pipeline)

```
session transcripts (.jsonl, 06/11..06/16, since-viewer_v3 floor)
  │  extract a clean narrative spine (drop tool-result noise; keep Pav steers + Soren acts + tool-acts)
  ▼  3,073 events
  │  tile with OVERLAP  (CT-method: 19 tiles, ~34-event overlap seams)
  ▼
  │  CHUNK   — per-tile agent: extract acts (w/ event-ref provenance) + arc-fragments     [workflow, Opus]
  │  STITCH  — dedup the overlaps → 43 canonical arcs + 120 acts + the milestone narrative [workflow, Opus]
  │  VERIFY  — each arc checked against the real files on disk (COIN: render ≤ support)     [workflow, Opus]
  ▼
  acts.jsonl + arcs.jsonl + verify.jsonl   (append-only, bitemporal t_event/t_obs)
  │  compile_arc.py  — best-value resolve + COIN render-cap + fake-bit flags
  ▼
  compiled/arc.compiled.json + arc_data.js → TIMELINE.html
```

Plus a concurrent **fresh literature scan** (5 angles) hardening the digestion-dynamics spec, and a **codex + gemini** external pass on the result.

## Files

| file | what |
|---|---|
| `ARC_DIGEST.md` | **the readable digest** — narrative + 43 arcs in 7 movements + the honesty ledger + the harden synthesis |
| `TIMELINE.html` | **the viewer** — swimlane-per-arc; Pav-steers as bold dots; low-support acts rendered *blurred*; the expose↔conceal COIN dial. Serve via the `genealogy-viewer` launch config, open `/hyperspace_spec/session_arc/TIMELINE.html` |
| `acts.jsonl` | 120 atomic acts (act_id, arc_id, t_event, actor, kind, title, artifacts, provenance.ref, certainty) |
| `arcs.jsonl` | 43 storyline arcs (summary, t_start/end, status, pav_steers, key_artifacts, demotions, certainty) |
| `verify.jsonl` | 43 verification records (verdict, artifacts_present/missing, unsupported_claims = candidate fake bits) |
| `compile_arc.py` | the procedural compiler (stdlib; SUBSTRATE_SPEC discipline + bitemporal + the COIN render-cap) |
| `compiled/arc.compiled.json` | the compiled capture (committed artifact; what the viewer ingests) |
| `arc_data.js` | `window.ARC_DATA = {...}` (the viewer's data include) |
| `milestone_narrative.txt` | the stitched narrative (source for the digest) |
| `fresh_scan.json` | the 5-angle digestion-dynamics prior-art scan |
| `external_brief.txt` · `codex_arc_review.md` · `gemini_arc_review.md` · `EXTERNAL_SYNTHESIS.md` | the external pass |
| `tiles/` | the 19 overlapping transcript tiles (the raw chunk inputs) |
| `_raw_timeline.txt` | the full extracted narrative spine |

## Honesty notes (what this is and is NOT)

- Tier-3 capture, **not canon**. Every arc carries its real artifacts; unsupported claims are flagged, never sharpened (10 over-claim flags surfaced — see the digest's honesty ledger).
- **Verified against final disk state**, so a past act is corroborated by the artifact as it stands *now* (`t_obs`), not as-of-`t_event` — an anachronism caveat (raised by the external pass).
- The **stitch** can smooth coincidental acts into a tidy arc; the narrative is the most-exposed surface and should be read as the stitch's voice, with the verify ledger as the check on top.
- To regenerate: re-run the extractor → workflows → `compile_arc.py`. The logs are the source of truth; everything compiled is derived.
