# reviews/ — saved graph feedback (annotations + page state)

Drop-zone for visual feedback on the viewers/toys. Each review is a screengrab **plus** the
page state behind it, so a comment is replayable in context rather than floating on a flat image.

## How to capture a review
1. Start the review server (serves the viewers with the annotation overlay injected):
   ```
   python candidates/canonical_genealogy/review/review_server.py
   ```
2. Open a page **through it**: `http://localhost:8742/viewer_v3.html`
   (or `viewer_v2.html`, `toys/time_axis_toy.html`, etc.)
   Opening the same page through the plain preview server (8741) stays clean — no overlay.
3. **LONG-PRESS anywhere** (hold ~half a second; a gold progress ring shows the press) →
   a **radial menu** appears around the cursor. Keep holding and release over a segment
   (marking-menu style), or release and click a segment. Right-click also opens it.
   Segments: **comment** (pin + note) · **pen** · **arrow** · **box** · **mark** · **text**
   · **save** · **discard** · **use viewer**. Long-press again any time to switch tool or
   save/discard. (A bottom toolbar mirrors everything; `h` hides the overlay; Esc closes.)
4. **Save** (radial or toolbar) → the whole session (drawings + comments + page state + a
   composite PNG) is written here, and collapses into ONE **permanent gold pin** at your
   first comment-pin's spot:
   - `<timestamp>-<comment-slug>.review.json` — the structured capture (below)
   - `<timestamp>-<comment-slug>.png` — composite screengrab
   - a record in `pins.json` — the permanent pin registry

   If no save-server is listening (page opened via 8741), Save falls back to a browser
   **download** — move the files into this folder.

## Permanent pins (the compare loop)
Pins **persist across sessions and iterations** — every time the page loads through
:8742, its saved pins render. Click a pin → popup with the comment, the **old capture
thumbnail**, and **"go to frame"**, which REPLAYS the saved page state on the CURRENT
build — so you see the updated iteration in the exact frame the feedback was left on,
with the old capture right there for comparison.

### Exact-slice replay (not heuristic)
"Go to frame" now restores the **precise slice** the pin was made on, when the viewer
exposes the replay hooks (`viewer_v3.html` does):

- **`window.__getReviewState()`** captures specimen, year, play state, orient, layer
  filter, observer, depth, mass→force, mirage, every toggle (weather / loop / bedrock /
  narrate), the selected node, **and every draggable panel's position + collapsed /
  floating / hidden state** (legend, ratio, dna, narration, detail, and the transport
  bar) plus scroll position.
- **`window.__applyReviewState(s)`** restores all of it exactly — selecting the specimen,
  driving the same dials/toggles the user used, seeking the year, and replacing each
  panel at its saved position and collapse state.

Viewers without the hooks fall back to the older heuristic (match toggles/chips by label,
replay slider/select values) plus a measured panel-layout snapshot (`state.panelsFallback`:
bounding rects + collapsed flags of each `#id` panel), so the slice is still approximated.

### Ask / give / status lifecycle
Each pin carries the framework's claim-lifecycle shape:

- **ASK** — the reviewer's comment (the request). Editable in the popup (**✎ edit**).
- **GIVE** — the response/change: `{ text, by, commit, at }`. Recorded via **↪ give**
  (which also moves the pin to `applied`), shown in a green block in the popup.
- **STATUS** — `open → acknowledged → answered → applied → verified` (plus `retired`).
  The pin's **color** encodes status (open=gold, acknowledged=blue, answered=teal,
  applied=green, verified=bright-green ring, retired=grey); the popup shows a status
  **chip**, the **history** of transitions, and a **✓ <next>** button to advance.
- **FOLLOW-UPS** — append a note to the pin thread with **+ note**; a small tally badge
  on the pin shows how many.

**Edit / delete:** the popup has **edit** (ask comment), **+ note** (follow-up),
**◉ sub-pin** (threaded annotation session), **↪ give** (response), and **delete**.
Delete is a **retire** — the pin's record stays in `pins.json` (`status:retired`,
`retired:true`) and its `.review.json` / `.png` are kept on disk. **Records are never
destroyed.**

### Threads (follow-ups with annotations)
The follow-up flow: **click the parent pin → its popup → choose:**
- **+ note** — a quick text follow-up appended to the pin's thread, or
- **◉ sub-pin** — a full annotation session attached to the parent: the popup closes,
  you're in pin mode; pin + draw + comment as usual, then **save** — it lands as a
  **sub-pin** (small circle labelled `2.1`, `2.2`, …) with its own capture, state, and
  ask/give lifecycle, threaded under the parent. The parent popup lists the THREAD
  (click any entry to open the sub-pin; sub-pin popups link back to the parent).
  The parent pin's badge counts notes + sub-pins.

### Popup behavior (fixed after first field test)
The pin popup is never cropped — it measures itself, clamps fully on-screen (and re-fits
as the thumbnail loads), scrolls internally when taller than the viewport, and **drags by
its header**. While a comment editor has unsaved text the popup refuses to be silently
replaced (a toast warns instead) — a draft can no longer vanish mid-typing. The radial
menu renders **above** the popup.

Server endpoints: `PATCH /pins/<id>` (comment / status / give / add_note / retired) and
`DELETE /pins/<id>` (retire). Existing pins with no status field load as `open`.

## What's in a `.review.json`
```jsonc
{
  "meta":  { "name": "...", "savedAt": "...", "png": "<file>.png", "source_page": "/viewer_v3.html" },
  "state": {
    "url": "...", "path": "/viewer_v3.html", "title": "...", "viewport": {"w","h","dpr"},
    "scroll": {"x","y"},
    "viewer": {                 // EXACT state when the page exposes window.__getReviewState()
      "specimen","mode","year","playing","orient","layerFilter","observer",
      "depth","magK","mirThresh","toggles":{"weather","loop","bedrock","narrate"},
      "selected", "panels": { "<id>": {"left","top","collapsed","floating","hidden"} }
    },
    "panelsFallback": { "<id>": {"left","top","w","h","collapsed","hidden"} },  // measured rects (hookless fallback)
    "inputs": { "scrub": {"value"}, "mag": {"value"}, ... },   // every slider/select value
    "activeControls": ["Maxwell EM", "Bedrock", "Narrate", ...]  // which chips/toggles were on
  },
  "annotations": [
    { "id", "type": "pin|pen|arrow|rect|hi|text", "color", "t",
      "x","y" | "pts" | "x1,y1,x2,y2" | "w,h",   // geometry, in viewport px
      "text": "the comment / label",
      "context": { "tag","id","cls","text", "node": <viewer node id if __reviewHitTest exists>,
                   "nx","ny" }   // what sat under the anchor + normalized position (resize-tolerant)
    }
  ]
}
```

## How these get processed
Tell me "process the latest review" (or name one). I read the `.json` here, reconstruct the
context from `state` (which specimen / year / view / toggles you were on), walk each annotation
in order with its `text` and `context`, and turn them into a worklist of changes. The `.png` is
my visual reference; the structured `state`+`context` is what makes each note actionable without
guessing what you were looking at.

## Full-slice capture (DOM panels + bars in the PNG)
The composite PNG now includes the page's **DOM panels and bars**, not just the canvases.
After drawing the graph canvases, the layer rasterizes every panel/bar — anything matching
`footer, header, .panel, [data-review-capture]` — using the standard same-origin
**SVG `<foreignObject>`** trick (clone the element, inline its computed styles, draw it at its
bounding rect), then lays your annotations on top. So a comment left on the bottom
transport bar (or the legend / narration / DNA panels) now appears in the screenshot.
**The capture is what you see** (changed after field test 2, where the panel under review was
the review toolbar itself): the toolbar and permanent pin markers ARE captured at their true
stacking position, so the review UI is itself reviewable. Only **transient overlays** (the pin
popup, the radial menu) stay excluded — they'd occlude half the frame. To keep chrome out of a
shot, press **`h`** (hide — now hides the toolbar too) before saving via the long-press radial,
then `h` again.

**Best-effort + disclosed:** `<foreignObject>` rasterization is same-origin and tainted-canvas
safe, but **cross-origin images and some webfonts may degrade** (a webfont not yet loaded can
fall back to a system face; a cross-origin `<img>` may be skipped). Within the DOM layer,
elements are drawn in **computed z-index order** (stable — equal z keeps document order); panels
in different CSS stacking contexts can in rare overlap cases stack slightly differently than on
screen. The graph canvases and your drawings are always exact; the DOM chrome is a faithful
best-effort. After each capture, `window.__review.lastCapture` lists exactly which elements were
rastered, so a capture gap is inspectable rather than silent. To force-include any extra element,
add the `data-review-capture` attribute to it.

**Honest limits:** annotation geometry is viewport-pixel (with normalized `nx,ny` for resize
tolerance) — not yet anchored to specific graph nodes OR to UI elements (that needs a
`window.__reviewHitTest` hook in the viewer, still absent; `context` captures the element under
the point as a stand-in). This applies to panels too: a pin left on the transport bar stays at
the viewport spot where it was made — if the bar is later dragged elsewhere, the pin does not
follow it (replaying the pin's frame restores the layout it was commented on, which is the
honest workaround until hit-test anchoring exists).

**Server posture:** the review server is **unauthenticated** and must stay bound to
`127.0.0.1` (it is — `ThreadingTCPServer(('127.0.0.1', PORT))`). Any local page could call
`PATCH`/`DELETE /pins/<id>`; that is accepted for this single-reviewer localhost tool. Do not
bind it to a public interface.
