# Viewer App Architecture

**Audience:** a future agent that must modify viewer_v3.html or its data pipeline without breaking it.

---

## What it is

`viewer_v3.html` is a ~1.23 MB, ~2342-line self-contained single-file browser app that renders the Agnostic Framework's canonical genealogy specimens as animated force-directed graphs. It is a Tier-3 render tool: it illustrates disclosed proxies, it is NOT canon and does NOT promote any specimen or grow the convergence list (stays 9). The file carries all 8 specimen data sets embedded as inline `<script type="application/json">` blocks; the only server requirement is to serve the file at origin (or use review_server.py on :8742 which injects review_layer.js).

---

## File map

| Path | Role |
|------|------|
| `candidates/canonical_genealogy/viewer_v3.html` | The app. NEVER read whole (~1.23 MB). Split reads by line range or regex. The main JS block runs from line 195 (`<script>`) to line 2343 (`</script>`). |
| `candidates/canonical_genealogy/_reembed_agnostic.js` | Node script. Regenerates only the 3 agnostic_framework data blocks (spec / overlay / narration) in viewer_v3.html from the canonical files. Run: `node _reembed_agnostic.js`. Never run for the other 7 specimens. |
| `candidates/canonical_genealogy/specimens/*.json` | 8 canonical specimen JSON files (7 base + agnostic_framework). RATIFIED-FROZEN: never hand-edit once ratified. |
| `candidates/canonical_genealogy/overlays/*.overlay.json` | Per-specimen overlay JSON (entity_lifecycles, rival_fates, claim_fates, harvest_dates, theory_dna, now_extension). Generated/curated; never hand-edit the embedded copy. |
| `candidates/canonical_genealogy/narration/*.narration.json` | Per-specimen narration JSON (segments with from/to/refs). refs must resolve to FACT ids or specimen/overlay keys. |
| `candidates/canonical_genealogy/PROXY_SPEC.md` | Version-controlled proxy weight disclosure. The `PROXY_SPEC` object at viewer_v3 line ~240 and this file MUST stay in sync; bump version on any weight change. |
| `candidates/canonical_genealogy/review/review_server.py` | Flask review server on :8742. Injects review_layer.js. Serves pins registry and session files. |
| `candidates/canonical_genealogy/review/review_layer.js` | Injected review overlay: long-press radial menu, pin creation, state capture. |
| `candidates/canonical_genealogy/reviews/pins.json` | Permanent pin registry (array). PRESERVE: never overwrite or truncate; only append. |
| `candidates/canonical_genealogy/reviews/*.review.json` | Per-session review payloads (state + annotations). |
| `viewer_v0.html`, `viewer_v1.html`, `viewer_v2.html` | Lineage viewers. UNTOUCHED: never edit. |

Key function names inside viewer_v3.html (all within the IIFE at line 195):

| Function | Purpose |
|----------|---------|
| `gatherYears(spec)` | Collects all year values from a specimen for range calculation |
| `buildModel(key)` | Central model builder: ingests SPECS/OVR/NARR/SUBS for one specimen, produces the node/edge/actor graph and metadata object returned to `M` |
| `computeSize(role, node, spec)` | Proxy: list-length + confidence -> node size scalar |
| `computeSolidity(role, node, spec)` | Proxy: kernel/canon/artefact/protocol span -> solidity scalar in [0,1] |
| `computeNormFrames(nodes)` | Per-specimen [min,max] normalization frames for conf and size |
| `selectSpecimen(key)` | Switches active specimen: calls buildModel, seedPositions, buildLegend, buildDNA, runLint |
| `frame()` | rAF loop: pauses when `document.hidden` (R1 hidden-pause); dispatches to `step(dt)` + `render()` or `stepGlobal(dt)` + `renderGlobal()` |
| `step(dt)` | Physics step: spring forces, separation, edge forces, weather forces, velocity damping |
| `render()` | Canvas render: drawBands, drawFeedbackArcs, drawStems, drawEdges, drawWeather, drawAbsorption, drawNodes, drawActors, drawNowItems, drawWeldFlash, drawBedrock, drawLoopOverlay, drawTimeGuides |
| `drawBands()` | Draws 3 horizontal (or 3 vertical) band regions: HARVEST / LATENT / PHYSICAL with cached gradients |
| `buildBandGrad()` | Builds and caches band gradients; invalidated on resize or orientation change |
| `getSprite(col,r,fuzz,glow)` | Returns memoized offscreen canvas blob sprite; keyed by color+radius+fuzz+glow bucket |
| `drawSprite(x,y,col,r,fuzz,glow,op)` | Draws a cached sprite at (x,y) with opacity |
| `qualityStep(dt)` | EMA frame-time quality ladder: drops to 'low' above 40ms EMA (disables separation + arcs + glow) |
| `seedPositions()` | Initialises node/actor positions and velocities for a newly loaded specimen |
| `refreshMass(force)` | Memoizes node._mass from size+magK; only recomputes when magK changes |
| `visibleNode(n)` | Visibility predicate: depth/layerFilter/year/appearAt gates |
| `visibleActor(a)` | Visibility predicate for actors |
| `targetOpacity(n)` | Target opacity for a node: solidity * observerFactor * dormancyDim * rivalFade * lifeFade * ramp |
| `nodePhase(n)` | Returns 'pre' (conceived smear) or 'formed' |
| `drawLifeMark(n,r)` | v3: renders claim-lifecycle badges: down-chevron (demoted), dashed ring (dormant), friction hatch + dead-children tally pill |
| `updateReflexiveBanner()` | Shows the reflexive Tier-3 self-referential banner only when agnostic_framework is active in single mode |
| `throttledPanels(now)` | ~5 Hz side-panel updates (ratio + narration); NOT per frame |
| `updateRatioMaybe()` | Updates SHARP/FUZZY panel with agnostic-ratio proxy |
| `buildDNA()` | Builds the THEORY DNA bar once per specimen load (static) |
| `currentSegment(narr, yr)` | Finds the narration segment active at year yr |
| `updateNarrationMaybe()` | Updates narration panel; uses refChip to resolve f-refs against FACT index |
| `buildLegend()` | Builds legend HTML; includes claim-lifecycle section when any node has lifeState |
| `buildGlobal()` | Builds all 8 models for GLOBAL swimlane view |
| `enterGlobal()` | Switches mode to 'global' |
| `renderGlobal()` | Renders normalized cross-specimen swimlanes |
| `runLint()` | Linter: (1) all narration f-refs resolve in FACT; (2) all nodes have finite size/solidity in [0,1]; (3) all substrate facts have a source field. Writes badge to DOM, console.warns on failure. Triggered by `#lint` in URL or `window.__lint()`. |
| `lintFrame()` | Per-frame op sanity check (only fires once per specimen per session) |
| `setupPanel(id)` | R4: wires up draggable + collapsible behaviour for a panel; persists position in panelPos{} |
| `selectSpecimen(key)` | Full specimen switch (also resets lint fired state) |
| `boot()` | Entry: resize, setupPanel x5, selectSpecimen(maxwell or ORDER[0]), rAF loop |
| `provenanceHTML(key, node)` | Looks up substrate provenance via findSubject; renders fact rows with source links |
| `findSubject(key, names)` | Searches compiled substrate SUBS[key].subjects for a node by id/name |

---

## Data contracts

### Inline data blocks (lines 162-194 of viewer_v3.html)

Each specimen has 3 or 4 data blocks embedded as `<script type="application/json" id="..." data-key="KEY" data-kind="KIND">`:

- `data-kind` absent or `"spec"` -> SPECS[key]; ORDER.push(key)
- `data-kind="overlay"` -> OVR[key]
- `data-kind="narration"` -> NARR[key]
- `data-kind="substrate"` -> SUBS[key] (SLIM/COMPILED form with short keys; NOT a verbatim copy of the .jsonl)

**These blocks are GENERATED, never hand-edited.** The script `_reembed_agnostic.js` regenerates only the agnostic_framework trio from canonical files. The other specimens were embedded by their own build steps; re-embed them from their canonical source files using the same replaceBlock pattern if they change.

The embed function in `_reembed_agnostic.js` escapes all non-ASCII chars to `\uXXXX` and neutralizes `</` to `<\/`. This is the required style; all embedded JSON must be ASCII-safe and script-close-safe.

### SPECS[key] (specimen JSON) - key fields consumed by buildModel

```
spec.weld.when                   -> weldStart, weldFire (fracYear)
spec.weld.parents / parents_full -> parentNodes (parents_full takes priority)
spec.weld.candidate_children     -> candidate nodes
spec.weld.dormancy_intervals     -> dormancy[] used in dormancyDim()
spec.weld.lifecycle.phase_trajectory -> phases[]
spec.weld.lifecycle.weld_type    -> weldTypes[]
spec.weld.sub_welds              -> subWelds[]
spec.weld.surprise_confidence    -> child glow intensity
spec.weld.S_structure.agreed     -> seamAgreed (seam flash ring color)
spec.roots.sub_wrappers          -> root nodes
spec.roots.people_0              -> fallback actor list if spec.actors is empty
spec.actors[]                    -> actor nodes (preferred source)
spec.harvest.descendants[]       -> descendant nodes
spec.harvest.cultural_harvest[]  -> cultural nodes
spec.child.utility.action_spaces_unlocked[] -> aspace nodes
spec.relatives.edges[]           -> relative/rival nodes
spec.forcing_events[]            -> forcing[] for weather arrows
spec._claim_lifecycle_tally      -> tally badges on nodes (self-specimen agnostic_framework only)
spec.fuzzy_layer.certain_core    -> used in inCertainCore() for solidity canon term
```

### OVR[key] (overlay JSON) - accessors

```
ovl(key).entity_lifecycles[id]  -> node.life (born/died/conceived/formulated/named/dissolved + _note)
ovl(key).rival_fates[id]        -> node.fate (persists/niche/absorbed/faded)
ovl(key).claim_fates[id]        -> node.fate (own-specimen claim lifecycle; takes priority over rival_fates)
ovl(key).harvest_dates[id].emerged / .consolidated -> harvest born dates
ovl(key).theory_dna.parents[id].load_bearing_share  -> loadShare for DNA bar
ovl(key).theory_dna.novel_residue                   -> novel_residue segment in DNA bar
ovl(key).now_extension[]                            -> nowItems[] (diamond glyphs near NOW line)
```

### NARR[key] (narration JSON) - structure

```
{ segments: [{ title, from, to, text, era_kind, refs: ["f-ID", "specimen:field", "overlay:key"] }] }
```
All `f-` refs MUST resolve in `FACT[key]` (built from SUBS[key].subjects). The lint check (1) enforces this. Unresolved refs render as `chip fact miss` (amber) and fire a lint issue.

### SUBS[key] (compiled substrate) - slim format

```
{ subjects: { "subject name": [ { p, v, w, b, c, f, st, sy, su, st2 } , ... ] } }
```
Short keys: `p`=predicate, `v`=value, `w`=when, `b`=bucket, `c`=certainty, `f`=best_fact_id, `st`=source_title, `sy`=source_year, `su`=source_url, `st2`=source_type. `st` MUST be present for every fact (lint check 3).

### Node object shape (post-buildModel)

```js
{
  id, role, name, kernel, frame, frame_layer,
  confidence,          // [0,1]
  born,                // fracYear
  appearAt,            // min(conceived, born) - controls when node fades in
  conceived, formulated, // K1 smear window (null if absent)
  size,                // proxy scalar
  solidity,            // proxy scalar in [0,1]
  layer,               // 'latent' initial
  life,                // from overlay.entity_lifecycles (may be null)
  fate, fateWhen, fateConf, fateTo,  // from overlay.claim_fates / rival_fates
  lifeState,           // 'demoted'|'walkback'|'dormant'|'friction'|'open'|'held'|'revival' (null elsewhere)
  tally,               // dead-children tally object (agnostic_framework only; null elsewhere)
  raw,                 // original JSON node
  // runtime fields (mutable per frame, skip[]-listed in fieldRows):
  x, y, tx, ty, vx, vy, op, absorbT, lobeAngle, _mass, _sx, _sy, appearAt
}
```

### PROXY_SPEC object (line ~240 in viewer_v3)

Must stay in sync with `PROXY_SPEC.md`. Version format: `"proxy-vX.Y (YYYY-MM-DD)"`. Change both the object and the md file together; bump the version string.

### panelPos{} - panel position memory

`panelPos[id] = {left, top}` - in-session pixel positions for draggable panels. Panels: `legend`, `ratio`, `dna`, `narration`, `detail`. Populated by `setupPanel()`, read back on re-open.

### window.__getReviewState / window.__applyReviewState

These hooks are the contract for review_layer.js exact-replay. **They do not yet exist in viewer_v3 and must be added** (see PAV BUG REPORT item 2). When implemented they must capture: current specimen key, year, orient, layerFilter, observer, depth, magK, mirThresh, playing, and the panelPos of all 5 panels + their collapsed states. `__applyReviewState(s)` must restore all of these, calling `selectSpecimen` if the key differs.

---

## GOTCHAS

1. **Never read viewer_v3.html whole.** At 1.23 MB / 2342 lines it will hang any tool with a size limit. Always read by line range (e.g., PowerShell `$content[194..399]`) or grep for function names.

2. **Never hand-edit embedded JSON blocks.** The `<script type="application/json">` blocks in lines 162-194 are GENERATED. Edit the canonical source files (`specimens/`, `overlays/`, `narration/`) and then run `node _reembed_agnostic.js` to update the agnostic_framework blocks. For other specimens, use the same replaceBlock pattern with their canonical source files.

3. **Embeds must be ASCII-safe and script-close-safe.** The `embedJSON()` function in `_reembed_agnostic.js` escapes non-ASCII to `\uXXXX` and `</` to `<\/`. Any new embed must apply the same transforms. Failing to do so produces garbled text (the viewer currently shows Mojibake-looking chars like `â€"` in comments - these are display artifacts from CRLF+non-ASCII in the raw file but are correctly decoded at runtime).

4. **CRLF warnings are normal.** The file has Windows CRLF line endings. `git diff` or linters may warn. Do not convert to LF; the viewer renders correctly in all browsers regardless.

5. **node --check gate.** After any JS edit, run `node --check candidates/canonical_genealogy/viewer_v3.html` will FAIL (it is HTML not a module). The correct gate is the embedded `#lint` check: load `http://localhost:8742/candidates/canonical_genealogy/viewer_v3.html#lint` and verify the lint badge shows `LINT [key]: PASS` for each specimen you affected.

6. **The lint check has 3 assertions.** (1) All narration `f-`refs resolve in FACT. (2) All rendered nodes have finite size and solidity in [0,1]. (3) All substrate facts have a `st` (source_title) field. A failing lint is a render-faithfulness violation; fix before shipping.

7. **ASCII-only git commit messages.** The repo enforces ASCII-only in commit messages. Avoid en-dashes, curly quotes, or Unicode symbols in commit text.

8. **Ratified files are frozen.** `SCHEMA_v2.md`, the 7 base specimen JSON files, `viewer_v0/v1/v2.html`, and the contents of `candidates/frame_lock_data/` must never be edited. viewer_v3.html MAY receive small surgical additive edits (state hooks, panel features).

9. **The convergence list stays 9.** No edit to viewer_v3.html should add a new specimen or change any data that would imply a tier promotion. The agnostic_framework specimen renders with an explicit reflexive banner disclosing this.

10. **Quality ladder drops features.** When EMA frame time exceeds 40ms, `quality` flips to `'low'`: separation is skipped, arcs are skipped, glow is zeroed. Do not add heavy per-frame operations. If a new feature is expensive, gate it with `if(quality!=='low')`.

11. **spriteCache is keyed by `col|rb|fb|gb` buckets.** Palette is ~30 hex colors; radius quantized to nearest even 2px; fuzz quantized to 1/8; glow quantized to 1/6. Cache is effectively bounded. Do not bypass it by calling `ctx` directly for node rendering.

12. **Panel drag uses pointer capture** (`handle.setPointerCapture`). Do not replace with mouse events; touch devices need pointer capture to track drag outside the element.

13. **FACT_EXTRA patch block** (lines ~240-260). Darwin-Mendel has 3 narration refs that were not in the compiled substrate export. They are patched in at runtime via `FACT_EXTRA`. If more such refs appear for other specimens, add them here with `if(!idx[fid])` guard. Do not silently drop the refs or change the narration file to remove them.

14. **weldOpen vs weldFire logic.** Rivals do NOT fade when `M.weldOpen` is true. The weld flash, absorption animation, and seam ring only fire for closed welds. Any new feature touching weld-time behavior must check `M.weldOpen`.

---

## How to modify safely (checklist)

1. **Identify the line range** you need to edit. Use PowerShell `$content[N..M]` with 50-100 line windows. Never read the whole file.
2. **Edit with Edit tool** (exact old_string/new_string). Keep edits small and surgical (additive where possible).
3. **After JS edits**: open the file in browser at `http://localhost:8742/candidates/canonical_genealogy/viewer_v3.html#lint`. Verify lint badge shows PASS for the affected specimen(s).
4. **After data-block changes** (specimen/overlay/narration): run `node _reembed_agnostic.js` if the changed file is agnostic_framework. For other specimens use the replaceBlock pattern manually or write a peer script. Then reload and lint-check.
5. **After adding a new panel or collapsible element**: call `setupPanel('your-panel-id')` in `boot()` (line ~2232).
6. **After changing PROXY_SPEC weights**: update both the `PROXY_SPEC` object in viewer_v3.html AND `candidates/canonical_genealogy/PROXY_SPEC.md`; bump the version string in both places.
7. **Commit message**: ASCII only. No en-dashes, curly quotes, Unicode glyphs.
8. **Do not touch** viewer_v0/v1/v2.html, SCHEMA_v2.md, the 7 base specimens, or anything in `candidates/frame_lock_data/`.

---

## Verification (how to prove your change works)

| Check | How |
|-------|-----|
| JS syntax | Load the page; no console errors on boot |
| Lint PASS | Load `?#lint`, verify `LINT [key]: PASS` for all specimens you touched (cycle via specimen picker) |
| Narration refs | Open a specimen, scrub through time, watch narration panel — no `miss`-class chips (amber/red border) |
| Panel drag | Drag a panel header; verify it moves and persists position on re-open |
| Panel collapse | Click the chevron; body collapses and chevron flips from down to right triangle |
| Quality ladder | If you added a new draw operation, throttle the browser to 2x slowdown (DevTools Performance), verify the viewer stays above ~15fps and quality badge shows 'low' only under genuine load |
| Substrate provenance | Click a node; verify detail panel shows provenance rows with source links (not "No matching subject") |
| Embed regeneration | Run `node _reembed_agnostic.js`; no error output; reload browser; agnostic_framework specimen loads without parse errors |
| Review server (if editing server) | Kill the listener on :8742, relaunch `review_server.py`, verify pins load on the page |
| ASCII commit | `git log --oneline -1` — no non-ASCII characters visible |

---

## GENERATED-EMBED contract (_reembed_agnostic.js)

The script replaces the content of exactly 3 `<script>` blocks in viewer_v3.html by matching their `id=` attribute:
- `spec-agnostic_framework` <- `specimens/agnostic_framework.json`
- `ovr-agnostic_framework` <- `overlays/agnostic_framework.overlay.json`
- `narr-agnostic_framework` <- `narration/agnostic_framework.narration.json`

It does NOT touch: substrate blocks, any other specimen block, the app script block, or any HTML/CSS. It is idempotent. The replaceBlock function finds `id="BLOCK_ID"` in the raw HTML string, locates the closing `>` of that tag and the next `</script>`, and splices the new JSON between them.

Substrate embeds are a SLIM/COMPILED form with short keys — NOT the raw `.jsonl`. They are produced by a separate substrate compiler (not included in this directory). Do not re-embed substrate from the raw `.jsonl` files directly; the slim format is what the FACT index builder and provenanceHTML expect.

All 8 specimens have peer embed scripts following the same pattern. For non-agnostic specimens, write a peer `_reembed_[key].js` if canonical source files are updated.
