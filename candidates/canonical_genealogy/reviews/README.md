# reviews/ — saved graph feedback (annotations + page state)

Drop-zone for visual feedback on the viewers/toys. Each review is a screengrab **plus** the
page state behind it, so a comment is replayable in context rather than floating on a flat image.

## How to capture a review
1. Start the review server (serves the viewers with the annotation overlay injected):
   ```
   python candidates/canonical_genealogy/review/review_server.py
   ```
2. Open a page **through it**: `http://localhost:8742/viewer_v3.html`
   (or `viewer_v2.html`, `toys/time_axis_toy.html`, etc.) The bottom toolbar appears.
   Opening the same page through the plain preview server (8741) stays clean — no overlay.
3. Tools: **comment** (numbered pin + note), **pen**, **arrow**, **box**, **mark** (highlight),
   **text** (typed label); colour swatches; undo; clear; hide (`h` key); **save**.
4. **Save** → writes here:
   - `<timestamp>-<name>.review.json` — the structured capture (below)
   - `<timestamp>-<name>.png` — composite screengrab (viewer canvases + your annotations)

   If no save-server is listening (page opened via 8741), Save falls back to a browser
   **download** — move the two files into this folder.

## What's in a `.review.json`
```jsonc
{
  "meta":  { "name": "...", "savedAt": "...", "png": "<file>.png", "source_page": "/viewer_v3.html" },
  "state": {
    "url": "...", "path": "/viewer_v3.html", "title": "...", "viewport": {"w","h","dpr"},
    "viewer": { ... },          // rich state IF the page exposes window.__getReviewState() (future hook)
    "inputs": { "scrub": {"value"}, "lam": {"value"}, ... },   // every slider/select value
    "activeControls": ["Agnostic Framework", "Bedrock", "Narrate", ...]  // which chips/toggles were on
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

**v0 scope / honest limits:** annotation geometry is viewport-pixel (with normalized `nx,ny` for
resize tolerance) — not yet anchored to specific graph nodes (that needs a `window.__reviewHitTest`
hook in the viewer; `context` captures the element under the point as a stand-in). The composite
PNG rasters the viewer **canvases** + your drawings; DOM panels (narration text, legend) aren't in
the raster but their content is captured in `state`. Both are noted upgrades.
