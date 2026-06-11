# UI Guidelines — Canonical Genealogy Viewer family

**Status:** LAW for future agent-made UI changes in `candidates/canonical_genealogy/`.
**Authored by:** Fable, 2026-06-11. Distilled from the design language already in use across `viewer_v0..v3`, the two toys (`toys/time_axis_toy.html`, `toys/composition_spectrograph_toy.html`), and the review layer (`review/review_layer.js`).
**Updated:** 2026-06-11, post-Stage-1 — the replay hooks and the managed transport bar (`#barpanel`) have since LANDED in `viewer_v3`, and the pin popup gained the ask/give/status lifecycle; §3/§7 now describe the implemented state and every line citation has been re-pointed against the post-Stage-1 files.
**Scope:** This governs new UI added to *our* surfaces — primarily `viewer_v3.html` (additive surgical edits only) and any new tool/toy/panel built for the review-and-update pipeline. It does **not** authorize edits to ratified files, `viewer_v0/v1/v2` (frozen lineage), Cowork's files, or `candidates/frame_lock_data/`.

> **Read this first if you are about to add or change any pixel.** The honesty conventions in §5 are not style preferences — they are the same proxy-disclosure discipline that governs the framework itself, expressed as UI. Violating them (rendering a fabricated number, presenting a proxy as data) is a correctness bug, not a taste call.

---

## 0. The one-paragraph design brief

A dark, dense, single-screen instrument. Everything lives in one viewport (`overflow:hidden`, flex column: header / stage / footer). The stage is a full-bleed `<canvas>` with floating, draggable, collapsible glass panels over it. Color is **semantic, not decorative** — each hue means a specific thing (a frame kernel, a lifecycle state, a disclosure tag). Type is small Segoe UI with uppercase micro-labels. Numbers are tabular. Every quantity that is not measured says so, in the legend, in the tooltip, or both. The aesthetic is "scientific console," not "consumer app": muted, precise, quietly disclosed.

---

## 1. Color tokens (the dark theme)

All viewers declare the same root palette. Use the CSS variables — **never hardcode a hex that a variable already names.** Source of truth: `viewer_v3.html` lines 5–10.

```css
:root{
  --bg:#0c0f16; --panel:#141a26; --panel2:#1b2333; --ink:#e8edf6; --muted:#8b97ad;
  --line:#28324a; --accent:#7fb3ff; --warn:#d2504a;
  --time:#e0a838; --space:#4a90d2; --knowledge:#46c07a; --meaning:#a06cd5;
  --harvest:#7fd6c0;
}
```

### 1.1 Structural neutrals

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#0c0f16` | App background. The "void." Canvas clears to this; panels float above it at ~0.9 alpha. |
| `--panel` | `#141a26` | Header / footer bars. |
| `--panel2` | `#1b2333` | Buttons, selects (raised controls on a bar). |
| `--ink` | `#e8edf6` | Primary text. |
| `--muted` | `#8b97ad` | Secondary text, micro-labels, panel body default color. |
| `--line` | `#28324a` | All borders / dividers. |

The toys use a parallel (slightly different) neutral set — `--fg:#e8edf6`, `--mut:#8e98ad`, `--hint:#5a6275`, `--brd:#2a3142` (`toys/time_axis_toy.html` line 3). `--hint` (`#5a6275`) is the toys' "third-tier / footnote" gray, dimmer than `--mut`; reach for it on honesty-footnote text. When you build a new standalone toy you may use the toy set; when you touch a viewer, use the viewer set.

### 1.2 Semantic accent colors — **each hue has a fixed meaning**

This is the load-bearing part. Do not repurpose a color; if you need a new meaning, add a new token.

| Token / hex | Meaning | Where it lives |
|---|---|---|
| `--accent` `#7fb3ff` (cornflower blue) | **Interactive / selected / focus.** Active toggle fill, `#tip b` headings, detail titles, range thumbs, links. The "you can touch this / this is on" color. | `viewer_v3` 21–25, 28–32 |
| `--time` `#e0a838` (gold) | **Frame kernel: TIME.** Also the year readout color and, in `--both`, the squeeze/pull "both" arrow. | 8, 49, 309 |
| `--space` `#4a90d2` (blue) | **Frame kernel: SPACE.** | 8, 309 |
| `--knowledge` `#46c07a` (green) | **Frame kernel: KNOWLEDGE.** Also the "certain / green band" end of the sharp↔fuzzy gradient. | 8, 309 |
| `--meaning` `#a06cd5` (purple) | **Frame kernel: MEANING.** | 8, 309 |
| `--harvest` `#7fd6c0` (teal) | **Harvest / agnostic-space / cross-substrate layer.** GLOBAL-mode active button; `ASPACE_COL`; the `.pp` provenance key color in detail. Teal = "this is the agnostic / knowledge-harvest layer." | 9, 25, 309+ |
| `--warn` `#d2504a` (coral/red) | **Warning / safety / squeeze-force / demotion.** The `safety` cultural domain, the `--squeeze` forcing arrow, demotion markers. Coral = "pressure, danger, or a claim that lost." | 7, `viewer_v0` 9, `CULT` 316–325 |
| **gold `#f0b75e` / `#9c8763`** | **Bedrock + review pins.** `BEDROCK_COL=#9c8763` (the L0 stratum); permanent review pins are **status-colored** with `open` = gold `#f0b75e` (see `STATUS_COLORS`: acknowledged blue, answered teal, applied green, verified bright-green ring, retired grey). Gold = "bedrock / an open marked anchor." | 326; `review_layer.js` 40–41 |

**Frame-kernel color map** is duplicated as a JS object (`FRAME_COL`, `viewer_v3` line 309) and as CSS vars — keep them identical if you touch either.

**Other secondary palettes already in use** (cite, reuse, don't reinvent): `KIND_COL` (actor/entity kinds — individual/lab/journal/company/government, lines 311–315) and `CULT` (cultural-harvest domains — art `#e07ab5`, sci-fi `#a06cd5`, tech `#46c07a`, prizes `#e0a838`, safety `#d2504a`, lines 316–325). Reuse these maps for anything coloring actors or cultural nodes.

### 1.3 Review layer's own accent (interaction blue)

The review layer deliberately uses a **distinct interaction blue** so its chrome reads as "meta / on top of the artifact," not part of it: active tool fill `#16324a`, border `#2f6a9a`, text `#cfe6ff` (`review_layer.js` 80–97, 301–307). Permanent pins are **status-colored** (`STATUS_COLORS`, line 40: open gold `#f0b75e`, acknowledged `#3cc8ff`, answered `#39d3c0`, applied `#5dffa0`, verified `#bfffd0` + ring, retired grey) on `#1a1206` ink. Annotation stroke palette: `['#ff5a3c','#ffd23c','#3cc8ff','#5dffa0','#ff7ad9','#ffffff']` (line 17). Keep review-layer chrome in this blue/gold family; keep viewer content in the semantic palette above. The separation is intentional and should be preserved — and it is now load-bearing in capture too: review chrome is **excluded** from the composite PNG (it is meta, never the subject).

---

## 2. Typography

One family, one scale. Source: `viewer_v3` 12–13 and throughout.

- **Family:** `"Segoe UI", system-ui, sans-serif`. Base `font:13px/1.45`. (Toys: `14px/1.5`.) Never introduce a second typeface.
- **Size ladder actually in use:**
  - `14px/600` — `h1` page title.
  - `13px` — body / detail kernel text / textarea.
  - `12.5px/600` — detail title (`.dTitle`).
  - `11.5px` — buttons, tooltips, sub-labels, narration body.
  - `11px` — `header .sub`, detail frame-meta.
  - `10.5px` — panel body default, micro-labels, legend rows.
  - `10px` — `.note`, detail headers, frame rows.
  - `9.5px` — DNA legend keys.
  - `9px` — chips, radial sub-labels.
- **Weights:** 400 default, 600 for titles/active/emphasis, 700 only for pin numerals and the strongest emphasis. No 300/100.
- **Uppercase micro-label pattern:** section labels are `text-transform:uppercase; letter-spacing:.5px; font-size:10.5px; color:var(--muted)` (`.grp .lbl`, line 20; panel `.ptitle`; detail `.dHdr`). Use this for every group/section header on a bar or panel.
- **Numbers:** any numeric readout that updates live uses `font-variant-numeric:tabular-nums` so digits don't jitter (`#yr`, line 49). Apply to every counter/clock/percentage you add.
- **Letter-spacing:** titles `.2px–.3px`; uppercase labels `.5px`. Body text: none.

---

## 3. Panel anatomy (the floating glass panel)

The signature component. Defined once as `.panel` chrome (`viewer_v3` 56–65) and reused for `#legend`, `#ratio`, `#dna`, `#narration`, `#detail` — and, since Stage 1 (pin #1's ask), the **transport bar `#barpanel`** (CSS 34–47, markup 164–175, `setupPanel('barpanel', true)` in `boot()`, line 2435). **Every new floating overlay MUST use this anatomy** so it is draggable + collapsible like the rest.

```
.panel                      → position:absolute; rgba(12,16,24,.9) glass; 1px var(--line);
                              border-radius:8px; box-shadow:0 4px 18px rgba(0,0,0,.45); z-index:6
  .phead                    → the drag handle. cursor:move; touch-action:none; user-select:none;
                              flex row, bottom border, rgba(27,35,51,.6) header tint
     .ptitle                → uppercase 10.5px/600 #cdd6e8 title, flex:1
     .pchev  ▾ (&#9662;)    → collapse chevron (toggles .collapsed → hides .pbody)
     .pclose ✕ (&#10005;)   → close button (only on dismissible panels e.g. #detail)
  .pbody                    → padding:8px 10px; max-height:46vh; overflow:auto
.panel.collapsed .pbody     → display:none   (collapsed = header-only)
```

Rules:
- **Drag handle is the header (`.phead`), never the body.** `cursor:move` + `touch-action:none` are required (touch-action lets pointer-drag work on touch/pen).
- **Collapse via chevron** flips a `.collapsed` class that hides `.pbody`. Header stays visible. Hover state on chevron/close: `color:var(--ink); background:rgba(127,179,255,.15)` (accent at 15%).
- **Panel glass** is `rgba(12,16,24,.9)` (≈`--bg` at 0.9). Tooltips are darker/denser: `rgba(10,14,22,.97)`. Keep panels translucent, tooltips near-opaque.
- **Default positions** are corner-anchored and collision-light: legend top-right, ratio top-left, dna left below ratio, narration bottom-center, detail bottom-right (`viewer_v3` 66–84). New panels should claim an unused corner/edge and set a sensible `max-width`/`max-height` (panels cap at `46vh`; detail/narration override to `60vh`/`30vh`).
- **z-index bands** (respect them): canvas tooltip `#tip` z-8; panels z-6; header/footer bars sit in normal flow above the stage. Review-layer chrome lives far above everything (z 2147482000+). Never park a viewer panel above z-10.
- **Docked-bar variant** (`#barpanel`, the pattern for any bar that must stay a bar until the user moves it): `.phead.barhead` grip strip + `.pbody.barbody` inline control row; it lives in **normal flow** (footer) by default and only adopts `.floating` (absolute, z-6, re-parented into `#stage`) on the **first drag**, so nothing changes visually until the user acts. `setupPanel(id, /*undock*/true)` remembers the dock home so a replayed docked snapshot **re-docks** it exactly (`viewer_v3` 34–47, 2271–2314, re-dock branch 2416–2423).

### 3.1 Legend & disclosure notes inside panels

- Legend rows: `.lrow` (flex, gap 6, 2px margin) with a swatch `.sw` (11px circle) or `.sq` (11px square, radius 2) — **circle = node/entity, square = stratum/band/region.** (`viewer_v3` 94–96.)
- **Disclosure note** is `.note` (`#8b97ad`, 10px) and its dimmer variant `.note.dim` (`opacity:.78`). Every panel that shows a derived/proxy quantity ends with one of these explaining what the number is and is not (see §5). Example rendered live: the sharp/fuzzy panel appends *"frame-relative ratio (per-specimen [min,max] norm); NOT MDL/gain_v2 bits — none exist for these specimens"* (`viewer_v3` 1827).
- **Estimate tags** ride in the panel title or as a chip: e.g. the DNA panel title is literally `THEORY DNA · estimate, not bits` (line 151), and the toys carry a `.badge` "MODELLED shape — not measured shares" right next to the H1 (`composition_spectrograph_toy.html` 23, 26).

### 3.2 Chips

Small inline tags: `.chip` (9px, 1px `--line` border, `rgba(27,35,51,.5)`, `cursor:help`). Semantic variants already defined (`viewer_v3` 81–84): `.chip.fact` (blue, real fact ref) with `.miss` modifier (red-ish, dimmed — a referenced fact that's missing), `.chip.spec` (green, from specimen), `.chip.ovr` (amber, from overlay). Reuse these classes for any provenance/source tagging; `cursor:help` + a `title` is the standard "hover for the source" affordance.

---

## 4. Interaction patterns

| Pattern | How it works | Where |
|---|---|---|
| **Timeline scrub** | `#barpanel` (the managed transport-bar panel, docked by default) holds `<input type=range #scrub>` (flex:1, step .25) driving `year`; `▶ Play` animates it; `NOW` jumps to 2026-06. Range thumbs use `accent-color:var(--accent)`. Year readout `#yr` in `--time` gold, tabular. | `viewer_v3` 164–175 |
| **Hover tooltip** | Single reused `#tip` div, `pointer-events:none`, `display:none` until hover, positioned at cursor, `max-width:360px`. Bold term in `--accent`, secondary `.k` line in `--muted`. One tooltip element, repositioned — don't spawn per-node nodes. | 28–32 |
| **Click → detail panel** | Clicking a node opens the `#detail` panel (the only panel with a `.pclose`). It's a normal `.panel`, just toggled `display`. | 158–162 |
| **Long-press → radial marking menu** | Review layer: hold 450ms with <6px movement → progress ring fills → radial menu of tools around the cursor; release over a wedge (marking-menu) or click a wedge. Right-click also opens it. Esc / outside-click closes. | `review_layer.js` 102–227 |
| **Pin popup (ask/give/status)** | Click a status-colored pin → popup with the status chip, the ASK (editable), the GIVE block (text + by + commit), status history, follow-up notes, the saved thumbnail, "↦ go to frame" (exact replay), a `✓ <next-status>` advance button, and edit / +note / ↪give / delete(retire) actions. Popup is `#10141d` card, `#2f6a9a` border. | `review_layer.js` 352–432 |
| **Toggle buttons** | `button.tog` (and `.pick`, `.preset`): `--panel2` bg, `--line` border; `:hover` → accent border; `.on` → accent fill with dark ink `#07101f` and weight 600. GLOBAL toggle's `.on` uses `--harvest` teal instead (special-cased). | 21–25 |
| **Toast** | Transient confirmation, bottom-center, review blue, auto-fades after 3.6s. | `review_layer.js` 630 |

General interaction laws:
- **One reused element** for tooltips/popups/toasts — create-and-reposition, don't accumulate DOM.
- **Hover affordance = `cursor:help` + `title`** for anything explanatory; `cursor:move` for drag handles; `cursor:pointer` for actions; `cursor:ew-resize`/`crosshair` on scrubable/drawable canvases (toys).
- **Keyboard:** `Esc` closes transient UI (radial, in-progress annotation); `h` toggles annotation visibility; Ctrl/Cmd+Enter commits a comment (`review_layer.js` 100, 318).

---

## 5. HONESTY conventions — UI LAW

These are non-negotiable. They are the framework's proxy-disclosure discipline rendered as interface. An agent that breaks one has introduced a defect.

1. **Every proxy is labelled in-legend.** Any rendered size, solidity, ratio, share, or thickness that is a heuristic (not a measured quantity) must be disclosed in the panel/legend that shows it. The canonical phrasings are already in the code — match their voice:
   - *"solidity = proxy span {kernel,canon,artefact,protocol}; only canon is data-bound. size = list-length+confidence proxy … sharp/fuzzy = agnostic frame-ratio, NOT MDL bits. theory-DNA shares = estimates."* (`viewer_v3` 1917)
   - *"load-bearing shares = disclosed historiographic ESTIMATES (conceptually gain_v2 synergy) — NOT measured bits."* (line 1848)
2. **"estimate" / "MODELLED" tags travel with the value.** If a number is hand-set or modelled, the word `estimate` (or `MODELLED`, `proxy`, `not bits`) appears adjacent — in the panel title (`THEORY DNA · estimate, not bits`), in a badge (`MODELLED shape — not measured shares`), or appended to the hover string (`· DNA share 42% (estimate)`, line 2131). Never show a derived percentage naked.
3. **"NOT measured bits" tooltips.** Where a quantity *looks like* it could be an information-theoretic measurement (bits / MDL / gain_v2) but is not, the tooltip/note must say so explicitly. No measured `gain_v2`/MDL bits exist for these specimens; saying otherwise is fabrication (lines 446, 1827, 1848, 1917).
4. **Data-absent = draw NOTHING. Never default.** If a value is missing, render nothing for it — no zero bar, no placeholder number, no invented default that could be misread as data. Panels hide themselves when their data is absent (`if(!M.dna){ document.getElementById('dna').style.display='none'; return; }`, line 1832). The toys say "Gärdenfors stays a thin dotted sliver because it is an *unwelded* parent — a known gap" rather than faking a share. Mirror this: absence is shown as absence (hidden panel, dotted/ghost sliver with a note), never as a fabricated value.
5. **Proximity / heuristic relationships are flagged as such.** Derived edges say what they are: bedrock root-links are *"NEAREST-BY-DATE proxy, NOT attested dependency"* (lines 1690, 1916–1917); attract/repel edges are *"role-proxy."* If you draw a connection the data doesn't directly attest, label the inference.
6. **Tier / not-canon framing stays visible.** The header sub-label carries the standing (`v3 — Tier-3 render tool (not canon)`, line 105). Don't remove or soften provenance/tier disclosure when restyling.

> Rule of thumb: **if a viewer reader could mistake a rendered quantity for a measurement, you owe them a disclosure in the nearest legend/tooltip.** When unsure whether something counts as a proxy, treat it as one and disclose.

---

## 6. Canvas conventions

The stage is a single `<canvas id="cv">` driving a `requestAnimationFrame` loop. Follow the existing performance hygiene (`viewer_v3`, R1 perf pass):

- **DPR cap at 1.5.** `DPR = Math.min(1.5, window.devicePixelRatio||1)` then `ctx.setTransform(DPR,0,0,DPR,0,0)` (lines 872, 877). Don't render at full retina DPR — it's a hot path. Re-apply the transform after any `canvas.width/height` reset (lines 1266, 1947).
- **Sprite cache for repeated blobs.** Node glyphs are pre-rendered to an offscreen canvas keyed by `color/radius/fuzz/glow` and blitted (`spriteCache`, lines 841–860). Any repeated soft/glowing shape should be cached, not re-drawn with gradients per frame.
- **Pause when backgrounded.** `if(document.hidden){ frame._last=null; return; }` in the frame loop; resume on `visibilitychange` (lines 1245, 1262). Any new animation loop must do the same — never burn CPU on a hidden tab.
- **Throttle panel/DOM updates.** Canvas runs at rAF; DOM-side panels update at ~5 Hz behind a signature check (`throttledPanels`, 200ms; `updateRatioMaybe` skips when the `year|layer|depth|observer` signature is unchanged, lines 1807–1816). Don't reflow DOM every frame.
- **Reuse cached rgba/hex parsing.** `hexRGB` and `rgba()` are memoized with bounded caches (lines 330–348). Use them instead of building rgba strings inline in the draw loop.
- **Blobs are gaussian splats, not wavelets** — and the legend says so (line 1827). If you change the rendering primitive, update the disclosure.
- **Hit-testing** goes through `window.__reviewHitTest(x,y)` when present so the review layer can name what a pin sits on (`review_layer.js` 273). The viewer-side hook is **still absent** — adding it is the standing path to node-anchored (rather than viewport-anchored) pins.

---

## 7. Review-state replay hooks (contract for "go to the exact slice") — IMPLEMENTED

The review layer captures and replays viewer state through two global hooks, which **viewer_v3 now exposes** (landed with Stage 1, closing the Pav ask):

```js
window.__getReviewState = function(){ ... }    // viewer_v3 line 2373. Returns {v, specimen, mode,
                                                // year, playing, orient, layerFilter, observer,
                                                // depth, magK, mirThresh, toggles{weather,loop,
                                                // bedrock,narrate}, selected, panels{}, scroll}
window.__applyReviewState = function(state){ ... }  // line 2387. Restores all of it by driving
                                                     // the SAME controls (clicks only on delta)
```

Contract rules, now load-bearing:
- **`panels{}` covers all six managed panels** (`legend`, `ratio`, `dna`, `narration`, `detail`, `barpanel`) with each panel's `left/top/collapsed/floating/hidden` (`PANEL_IDS`, line 2361).
- **Restore is symmetric.** `floating:true` floats the panel into `#stage`; `floating:false` onto a currently-floated panel **re-docks** it (removes `.floating`, re-parents to the remembered dock home, clears inline position — lines 2416–2423). A docked snapshot replayed onto any layout restores the dock exactly; verified by headless roundtrip (snapshot → float+collapse → replay snapshot → state equality).
- **Apply drives the real controls** — `selectSpecimen`/`enterGlobal`, button clicks only when the target differs, `syncScrub` for the year — so UI and internal state cannot diverge.
- Keep the hooks **additive and side-effect-free on load**; `__getReviewState` must stay read-only.

The layer's fallback for hookless viewers remains: scraping `input/select` values, re-clicking `/(on|active|selected)/` buttons, plus a measured `panelsFallback` layout snapshot (`review_layer.js` 467–512).

**Capture is full-slice now:** `composite()` draws canvases, then the page's DOM panels/bars (`footer, header, .panel, [data-review-capture]`) via same-origin SVG `<foreignObject>` with ~40 computed styles inlined (including `accent-color`, so sliders keep the viewer accent), drawn in **computed z-index order** (stable by document order), then the annotation SVG on top (`review_layer.js` 518–594). Review chrome is **excluded** — it is meta and must never occlude the subject. Best-effort is disclosed in `reviews/README.md`; `window.__review.lastCapture` lists what was rastered so gaps are inspectable.

---

## 8. Do / Do-Not for agents adding UI

**DO**
- Use the CSS variables (§1) and the existing semantic color meanings. Add a *new* token if you need a *new* meaning.
- Build every floating overlay as a `.panel` with `.phead` drag-handle + `.pchev` collapse (§3). Free drag/collapse for nothing.
- Keep the type scale and the uppercase-micro-label pattern (§2). Tabular numerals on every live counter.
- Disclose every proxy/estimate in the nearest legend/tooltip, in the established voice (§5). When in doubt, disclose.
- Draw nothing for absent data; hide the panel or show a labelled ghost/gap (§5.4).
- Respect canvas hygiene: DPR≤1.5, sprite cache, pause-when-hidden, throttle DOM (§6).
- Reuse single tooltip/popup/toast elements; reposition rather than accumulate.
- Make `viewer_v3` changes **additive and surgical**; run `node --check` and pass the embedded `#lint` after every edit.
- Keep review-layer chrome in its blue/gold "meta" palette, distinct from viewer content (§1.3).

**DO NOT**
- Hardcode a hex that a variable names; repurpose a semantic color (e.g. teal for a non-harvest thing, gold for a non-bedrock/non-pin thing); or introduce a second typeface.
- Render a fabricated, defaulted, or zero-filled value where data is missing. **No fake measured numbers — ever.** No "bits"/MDL/gain_v2 label on a quantity that isn't one.
- Show a derived percentage/size/share without an adjacent `estimate`/`proxy`/`NOT measured` disclosure.
- Put a draggable affordance on a panel body, or a panel above z-10 (collides with `#tip` z-8 and review chrome).
- Add a per-frame DOM reflow, render at full retina DPR, or run an animation loop while `document.hidden`.
- Edit ratified files, the 7 base specimens, Cowork's files, `candidates/frame_lock_data/`, or `viewer_v0/v1/v2` (frozen lineage). `viewer_v3` is the only viewer that takes edits, and only additive ones.
- Soften or remove tier/not-canon/provenance disclosure when restyling.

---

## 9. Where each pattern lives (citation index)

Re-pointed 2026-06-11 post-Stage-1 (the build inserted the barpanel CSS/markup and the replay hooks, shifting everything after line 33).

| Pattern | File · lines |
|---|---|
| Color tokens (`:root`) | `viewer_v3.html` 5–10; identical in `viewer_v1` 5–9; toy set in `toys/time_axis_toy.html` 3 |
| Frame-kernel JS color map | `viewer_v3.html` 309 (`FRAME_COL`) |
| Actor-kind / cultural-domain palettes | `viewer_v3.html` 311–325 (`KIND_COL`, `CULT`) |
| Bedrock gold + status-colored pins | `viewer_v3.html` 326 (`BEDROCK_COL`); `review/review_layer.js` 40–41 (`STATUS_COLORS`) |
| Panel chrome (drag/collapse) | `viewer_v3.html` 56–65; instances 66–84; docked-bar variant `#barpanel` 34–47 (CSS), 164–175 (markup) |
| Legend swatches / notes / chips | `viewer_v3.html` 81–84, 94–96 |
| Estimate tag (panel title / badge) | `viewer_v3.html` 151; `toys/composition_spectrograph_toy.html` 23, 26 |
| Tooltip (`#tip`) | `viewer_v3.html` 28–32 |
| Timeline scrub / play / NOW (transport bar) | `viewer_v3.html` 164–175 |
| Toggle buttons | `viewer_v3.html` 21–25 |
| Honesty disclosures (rendered) | `viewer_v3.html` 446, 1690, 1827, 1848, 1916–1917, 2131 |
| Data-absent → hide panel | `viewer_v3.html` 1832 |
| Canvas perf (DPR/sprite/pause/throttle) | `viewer_v3.html` 330–348, 841–877, 1245–1266, 1807–1816 |
| Panel system (drag/collapse/dock-home memory) | `viewer_v3.html` 2267–2314 (`setupPanel`) |
| Replay hooks incl. re-dock branch | `viewer_v3.html` 2361–2430 (`PANEL_IDS` 2361, get 2373, apply 2387, re-dock 2416–2423); wired in `boot()` 2432–2435 |
| Long-press radial menu | `review/review_layer.js` 102–227 |
| Pin popup (ask/give/status) + lifecycle calls | `review/review_layer.js` 332–465 (`patchPin`/`deletePin` 332–345, `openPermPopup` 352–432, inline editors 435–465) |
| State scrape/replay + hook calls | `review/review_layer.js` 467–512 (hooks called at 486, 495; `panelsFallback` 471) |
| Full-slice capture (foreignObject, z-ordered) | `review/review_layer.js` 518–594 (`CAPTURE_SEL` 526, `captureDOM` 558, `composite` 577) |
| Toast | `review/review_layer.js` 630 |

---

*This file is law for agent-made UI in the genealogy viewer pipeline. If a future change needs to break a rule here, the rule gets updated first (with the reason), then the code — same discipline as the framework's claim lifecycle.*
