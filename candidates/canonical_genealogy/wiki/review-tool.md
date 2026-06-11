# Review Tool — Agent Onboarding Wiki

**What it is.** A zero-dependency, inject-on-serve annotation layer for any `.html` file in the `canonical_genealogy/` tree. `review_server.py` (port 8742) rewrites HTML responses on the fly to inject `review_layer.js`; the overlay adds a radial marking-menu, drawing tools, and a permanent-pin registry without touching the viewer source files. Reviews are saved as JSON + PNG pairs under `reviews/`.

> **UPDATE (2026-06-11, post-Stage-1):** this page is the pre-lifecycle scout map and
> is kept as that record. Since then the tool gained: `PATCH /pins/<id>` +
> `DELETE /pins/<id>` (= retire, record kept) with `status` / `history[]` / `give{}` /
> `notes[]` fields on pins (so the "migration script" caveat below is superseded —
> mutate via the server API, never by hand); full-slice composite capture (DOM
> panels/bars via `<foreignObject>`, z-index order, review chrome excluded,
> `window.__review.lastCapture` disclosure); and exact replay against viewer_v3's
> `__getReviewState`/`__applyReviewState` hooks (all six panels incl. the transport
> bar, symmetric float/re-dock). Current contracts: `reviews/README.md`; conveyor:
> `wiki/PIPELINE.md`; law: `wiki/UI_GUIDELINES.md` §7.

---

## File Map

| Path (relative to `canonical_genealogy/`) | Role | Key names |
|---|---|---|
| `review/review_server.py` | Python HTTP server (ThreadingTCPServer, port 8742) | `Handler`, `load_pins()`, `append_pin()`, `do_GET()` (injects script + serves `/pins`), `do_POST()` (writes to `reviews/`) |
| `review/review_layer.js` | Client overlay, IIFE, no deps | `scrapeState()`, `applyState()`, `composite()`, `save()`, `openPermPopup()`, `loadPins()`, `renderPins()`, `placePins()`, `openRadial()`, `hitContext()`, `newAnn()`, `render()`, `openComment()`, `toast()` |
| `reviews/pins.json` | Permanent pin registry (append-only array) | written by `append_pin()` on every `/save` that includes `meta.pin` |
| `reviews/<stamp>-<slug>.review.json` | Full session dump (state + annotations) | written in `do_POST()` |
| `reviews/<stamp>-<slug>.png` | Base64-decoded composite screengrab | written in `do_POST()` alongside the JSON |
| `reviews/.gitignore` | Ignores `*.review.json`, `*.png`, `pins.json` | only `README.md` is tracked |

The server root is `canonical_genealogy/` (`ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))`). All static files are served from there; the overlay script is served at `/review/review_layer.js`.

---

## Data Contracts

### `pins.json` — permanent pin registry

```json
[
  {
    "id":          "20260611-003618-<slug>",   // == basename of .review.json (no extension)
    "page":        "/viewer_v3.html",           // location.pathname at save time
    "x":           604,                         // viewport px at time of save
    "y":           809,
    "nx":          0.3159,                      // normalized [0,1] = x / innerWidth
    "ny":          0.8375,
    "comment":     "...",                       // text of the first/named pin
    "savedAt":     "2026-06-10T23:36:17.914Z", // ISO8601
    "annotations": 9,                           // count of annotation objects in session
    "review":      "<stamp>-<slug>.review.json",// relative to reviews/
    "png":         "<stamp>-<slug>.png"         // relative to reviews/, or null
  }
]
```

**Append-only.** `append_pin()` always reads → appends → writes the whole file under `PINS_LOCK`. Never hand-edit entries; if you must mutate (e.g., to add `status`/`give` fields for the pipeline), do it via a migration script that rewrites the full array atomically.

### `.review.json` — full session

```json
{
  "meta": {
    "name":        "<slug>",
    "tool":        "review_layer v2",
    "savedAt":     "<ISO8601>",
    "pin":         { "x":..., "y":..., "nx":..., "ny":..., "comment":"..." },
    "png":         "<stamp>-<slug>.png",        // null if capture failed
    "source_page": "/viewer_v3.html"
  },
  "state": {
    "url":         "http://localhost:8742/...",
    "path":        "/viewer_v3.html",
    "title":       "...",
    "ts":          "<ISO8601>",
    "viewport":    { "w":1912, "h":966, "dpr":1 },
    "viewer":      { ... },                     // present ONLY if window.__getReviewState exists
    "inputs":      { "<id|name>": { "value":"...", "type":"..." }, ... },
    "activeControls": ["Maxwell EM", "Play", ...]
  },
  "annotations": [
    {
      "id":      24,                            // local counter, resets each session
      "type":    "arrow|pen|rect|hi|text|pin",
      "color":   "#ff5a3c",
      "t":       1781134284505,                 // Date.now() ms
      "context": {                              // element under cursor at draw time
        "tag":"canvas", "id":"cv", "cls":null, "text":null, "node":null,
        "nx":0.2992, "ny":0.8416               // normalized position
      },
      // shape-specific fields:
      // arrow: x1,y1,x2,y2
      // pen:   pts:[{x,y},...]
      // rect/hi: x,y,w,h
      // text/pin: x,y,text,n(pin only)
    }
  ]
}
```

`png` is stripped from the payload before writing JSON (`payload.pop('png', None)`), then saved separately. The `meta.png` field holds the relative filename or `null`.

### Hook contract — `window.__getReviewState` / `window.__applyReviewState`

`scrapeState()` calls `window.__getReviewState()` if it exists and stores the result at `state.viewer`. `applyState()` calls `window.__applyReviewState(state.viewer)` if it exists. These hooks must be installed on `window` by the viewer (e.g., `viewer_v3.html`) before the overlay boots. Neither hook is currently implemented in `viewer_v3.html` — the slot exists in the overlay but is unwired. When you add them, the function signatures are:

```js
window.__getReviewState = function() { return { /* arbitrary serializable object */ }; };
window.__applyReviewState = function(savedState) { /* restore */ };
```

### Hook contract — `window.__reviewHitTest`

`hitContext()` calls `window.__reviewHitTest(x, y)` if present (returns a `node` descriptor for the annotation context). Optional; not yet implemented in any viewer.

---

## Known Gaps (current limits)

1. **DOM panels/bars missing from PNG.** `composite()` iterates `document.querySelectorAll('canvas')` only — it draws the `<canvas id="cv">` element and then rasterizes the SVG overlay. Fixed `<footer>` (Play/NOW/scrub/sliders), `<header>`, and `.panel` overlays are pure DOM/HTML and are not included in the PNG. The screenshot captures the canvas background + drawn annotations only. Fix: rasterize the full page via `SVG foreignObject` wrapping `document.documentElement`, or use a `html2canvas`-style approach. The gap is documented and disclosed; any fix must be disclosed in the saved review metadata.

2. **Panel positions not captured.** `scrapeState()` does not record draggable `.panel` positions (`left`/`top` CSS), collapsed state (`.collapsed` class), or the footer's position/visibility. The `state.inputs` dict captures only `<input>` and `<select>` values by `id`/`name`. To add panel-layout capture, `window.__getReviewState` must serialize panel positions and collapsed flags; `window.__applyReviewState` must restore them.

3. **Replay is heuristic, not exact.** `applyState()` matches `activeControls[]` entries by `textContent` equality (click the button if it is not already active) and replays `inputs{}` by `id`/`name`. It does not know about render-loop state, scroll position, canvas transforms, or the viewer's internal year/playing/specimen variables. Exact replay requires the `__getReviewState`/`__applyReviewState` hooks.

4. **No pin edit / delete from the permanent popup.** `openPermPopup()` renders the pin's comment, thumbnail, and a "go to frame" button only. There is no in-UI path to update `comment`, delete a pin entry from `pins.json`, or change any pin field after save. Edit/delete requires new server endpoints (`/pin/update`, `/pin/delete`) and corresponding UI in `openPermPopup`.

5. **No pin status lifecycle.** `pins.json` has no `status`, `give`, or history fields. There is no ask/give/status structure on pins. The pipeline design calls for `status` (`open` → `acknowledged` → `answered` → `applied` → `verified`) and a `give` object (`text` + `commit_ref`). Adding these requires a schema extension to `pins.json` and new server endpoints.

6. **One session = one pin.** Each `/save` POST produces exactly one entry in `pins.json` representing the whole session. There is no way to have multiple permanent pins from a single save, or to associate a session's annotations with multiple pins.

---

## How to Modify Safely

Checklist for any agent touching this area:

1. **Read the actual file before editing.** The server is ~157 lines; the overlay is ~436 lines. Both are dense. Read them completely before proposing any change.

2. **Server edits require a restart.** The server must be killed (kill the process on port 8742) and relaunched after any change to `review_server.py`. The overlay (`review_layer.js`) is loaded fresh on each page load with `Cache-Control: no-store`, so client-side changes take effect on next page reload without a server restart.

3. **Never edit `viewer_v0`, `viewer_v1`, `viewer_v2`.** These are lineage artifacts. `viewer_v3.html` may receive surgical additive edits (state hooks only). After any edit to `viewer_v3.html`, run `node --check viewer_v3.html` and verify the embedded `#lint` comment passes.

4. **Never edit ratified files.** `SCHEMA_v2.md`, the 7 base specimens under `specimens/`, `candidates/frame_lock_data/` are frozen. Do not touch them.

5. **`pins.json` is append-only in normal operation.** Mutations for schema extension (adding `status`, `give`) must be atomic rewrites of the full array, never partial writes. Use `PINS_LOCK` if doing this from Python. If extending the schema, preserve all existing fields — especially `id`, `page`, `nx`, `ny`, `review`, `png` — as downstream agents index by them.

6. **Commit messages must be ASCII-only.** The repo's git tooling enforces ASCII in commit text. Do not include Unicode symbols, emoji, or non-ASCII characters in commit messages or file names you create.

7. **No new `.md` files unless explicitly requested.** This wiki page is explicitly requested. Do not create additional documentation files as side effects.

8. **`reviews/` artifacts are gitignored.** `*.review.json`, `*.png`, and `pins.json` are all in `reviews/.gitignore`. Do not commit them. If you write a migration script that modifies `pins.json`, run it locally and verify the result — it will not be committed.

9. **The overlay is a self-contained IIFE.** It uses `var` throughout (no `let`/`const`, no modules). Any additions must maintain this compatibility. The guard `if (window.__reviewLayerLoaded) return;` prevents double-injection.

---

## Verification

After any change to this area, verify:

| What changed | How to verify |
|---|---|
| `review_server.py` | Restart server; open `http://localhost:8742/viewer_v3.html`; confirm overlay toolbar appears at bottom; make a drawing, save — confirm `reviews/<stamp>.review.json` and `.png` are written; confirm `pins.json` has a new entry; reload and confirm the gold pin is visible. |
| `review_layer.js` | Hard-reload the page (Ctrl+Shift+R); confirm toolbar renders; long-press for radial; confirm segments appear; save a review; confirm `/save` POST returns `{ok:true}`; confirm pin appears after reload. |
| `viewer_v3.html` | Run `node --check viewer_v3.html` (must exit 0); reload through port 8742 and confirm no console errors; confirm the overlay still injects (INJECT string not in source, so injection fires). |
| Pin schema extension | Write a test JSON to `reviews/pins.json`; load the page; confirm `/pins?page=/viewer_v3.html` returns the new shape; confirm `renderPins()` does not throw on unknown fields. |
| `__getReviewState` / `__applyReviewState` hooks | After adding hooks to viewer_v3: save a review; open the pin popup; click "go to frame"; confirm toast says "frame replayed" and `rep.length > 0`; confirm viewer state visually matches the thumbnail. |

**Port check before restart:** `netstat -ano | findstr :8742` on Windows — kill the PID, then relaunch `python review/review_server.py` from `canonical_genealogy/`.
