# Agent wiki: toys + spec docs

**Audience:** a future agent that must modify this area without breaking it.
**Scope:** toys/, VIEWER_SPEC.md, PROXY_SPEC.md, candidates/CLAIM_LIFECYCLE.md, graduation path.

---

## What this area is

The `toys/` directory holds two single-file exploratory visualisations that prototype specific
viewer subsystems (time axis, composition bands) in isolation before the logic graduates into
`viewer_v3.html`. The three spec docs (`VIEWER_SPEC.md`, `PROXY_SPEC.md`, `candidates/CLAIM_LIFECYCLE.md`)
are the disclosed contracts that govern what the viewer renders and why. Everything in this
area is **Tier-3 / render-tool** — nothing here is canon, nothing promotes the convergence list.

---

## File map

```
canonical_genealogy/
  toys/
    time_axis_toy.html            standalone toy — adaptive time axis
    composition_spectrograph_toy.html standalone toy — wrapper composition bands
  VIEWER_SPEC.md                  render-model spec v0+v1+v2+v3 addenda (1038 lines)
  PROXY_SPEC.md                   versioned proxy weights for size/solidity/weather channels
  viewer_v3.html                  production viewer (MAY receive surgical additive edits)
  viewer_v0.html / v1 / v2        frozen lineage — DO NOT EDIT

candidates/
  CLAIM_LIFECYCLE.md              claim-lifecycle states, parent/child distinction, dead-children tally
```

---

## time_axis_toy.html

**What it is (3 lines).** Single-file vanilla-JS canvas toy. Renders the framework's uneven
event timeline (decades-sparse, then ~25 days with 90% of events) on an adaptive axis that
blends calendar position with order position. Lets a developer test the time-axis logic before
it graduates into the viewer.

**Key functions (all inside the IIFE):**

| Function | Purpose |
|---|---|
| `decYear(s)` | Parses date strings (`"~1990"`, `"2026-05-17T02:19"`, `"2026"`) to a decimal year (e.g. 2026.374). Handles fuzzy `~` prefix, full ISO timestamps, and bare years. |
| `load(k)` | Loads a dataset (`'framework'` or `'maxwell'`) from the `DATA` map, sorts events by decimal year, computes `T0/T1` (padded range), calls `buildAnchors()`. |
| `buildAnchors()` | Computes the `AN[]` warp table: each event's calendar position blended with its ordinal position by `lam` (the calendar↔order slider). Normalises to `[0,1]`. This is the blend that compresses the sparse decades and expands the dense sprint. |
| `uBase(t)` / `tOfU(u)` | Forward/inverse of the piecewise-linear warp defined by `AN[]`. Used to map a calendar year to a screen fraction and back. |
| `fish(u)` | Furnas 1D fisheye lens centred at `pf` (playhead fraction) with distortion strength `fstr`. Order-preserving; identity at `fstr=0`. Used to magnify the region around the scrub playhead. |
| `fmt(t)` | Formats a decimal year for the readout: hour-level for 2026 sprint events, month+year for 2025+, bare year otherwise. |
| `draw()` | Main render: fold-texture hatching, axis + ticks, event dots + collision-avoided labels, playhead line, fisheye lens bracket, truth strip (unwarped calendar density), readout. |
| `setP(ev)` | Pointer event handler — updates `pf` from clientX, calls `draw()`. |

**DATA contract.**
```js
DATA[key] = [
  [dateString, precise_int, label_string, big_int, note_string],
  ...
]
// precise_int: 1 = git-timestamp, 0 = approximate/undated
// big_int:     1 = major event (larger dot, brighter label), 0 = minor
```
The `framework` dataset contains **real git commit timestamps** for post-2026-05-17 events;
pre-repo events are approximate (`precise=0`, fuzzy halo rendered). The `maxwell` dataset is
historical (all approximate). Event order is preserved — `buildAnchors()` sorts by `t` but
never reorders events in the `EV[]` array relative to their ordinal position.

**Controls state:**
```js
var lam   // 0..1, calendar↔order blend
var fstr  // fisheye distortion (0..6)
var opt   // {lens, strip, fold, fuzz} booleans
var pf    // playhead fraction [0,1]
var playing // bool, animation state
var specKey // 'framework' | 'maxwell'
```

---

## composition_spectrograph_toy.html

**What it is (3 lines).** Single-file vanilla-JS canvas toy. Renders the composition of a
wrapper over its development as stacked bands across a warped time axis, showing how parent
contributions and novel synthesis evolve. Carries the `MODELLED shape — not measured shares`
badge on-canvas; disclosure is mandatory and must never be removed.

**Key functions (all inside the IIFE):**

| Function | Purpose |
|---|---|
| `norm(arr)` | Normalises an array so its values sum to 1. Applied to phase share vectors before stacking. |
| `px(i)` | Returns the warped x-fraction for phase index `i`: same `(1-lam)*calendar + lam*order` blend as the time-axis toy. |
| `rgba(hex, a)` | Converts a `#RRGGBB` hex colour + alpha to `rgba(r,g,b,a)` string. |
| `darker(hex)` | Returns a darkened version (40% brightness) of a hex colour; used for pattern strokes over the fill. |
| `patFill(kind, col, x0, y0, w, h, conf)` | Draws a fill-pattern (hatch / cross / dots) inside the bounding rect using `ctx.clip()`. `conf` modulates stripe density when `confDens` is on. |
| `draw()` | Main render: dispatches to either the frozen `conception-DNA` bar or the `expression spectrum`. For expression mode: builds `xs[]` (screen x per phase) + `cum[][]` (cumulative top per band per phase), draws stacked polygonal areas, future-dim past the playhead, phase ticks, demotion markers, playhead, hover guide. |
| `interpShares(frac)` | Interpolates the normalised band shares at a given x-fraction by finding the surrounding phases and linearly blending. Returns `{shares, i, tt, t}`. Used for the hover readout. |
| `drawLegend(bands)` | Writes the legend DOM once per specimen change (keyed by `leg.dataset.k`). Uses `patCss()` to inline CSS background-image for pattern swatches. |
| `patCss(kind, col)` | Returns a CSS `background-image` string for a legend pattern swatch. Note: the `if(kind==='dots')` dead branch at line 179 is unreachable (return already happened) — do not rely on it. |

**DATA contracts.**

Phases (modelled composition):
```js
SPECS[key].phases = [
  { d: decimal_year, label: string, s: [share_0, share_1, ...] }
]
// s[] is the RAW share vector — normalised at draw by norm().
// Sum does not need to equal 1 in the data.
// Phases must be in ascending d order.
```

Bands (parent/component identity):
```js
BANDS[key] = [
  { name: string, col: '#RRGGBB', pat: 'solid'|'hatch'|'cross'|'dots', conf: 0..1 }
]
// Band count must equal phase.s.length for every phase in the specimen.
// conf controls stripe density in confDens mode.
```

Demotions:
```js
SPECS[key].demotions = [
  { d: decimal_year, t: string }  // d must match a phase.d exactly (within 1e-3)
]
```

**Controls state:**
```js
var specKey   // 'framework' | 'maxwell'
var lam       // 0..1, calendar↔order blend
var view      // 1 = expression spectrum (default), 0 = conception DNA (frozen bar)
var pat       // bool, patterns on/off
var confDens  // bool, pattern density = certainty
var demo      // bool, show demotion markers
var playhead  // [0,1] reveal fraction (right of this is dimmed)
var hoverX    // canvas pixel x for hover guide, -1 = none
```

**Mandatory disclosure.** The `MODELLED shape` badge and the honest-framing paragraph in the
HTML must be preserved in any edit. The composition shares are a model of development, not
measured values. Never add a "measured" label or remove the disclosure note.

---

## VIEWER_SPEC.md — structure

The file is a single 1038-line document. It covers:

- **Base spec (lines 1–537):** v0 render model. Sections 0–13: blob channels, size proxy,
  anchor stems, force layout, welds, solidity, friction (D6), LOD, mirage rule, observer
  picker, timeline scrubber, element-channel crosswalk, build order, covered-vs-new table.
  Section 15 (lines 541–614): cross-Claude (Opus) review fold with four build fixes applied to
  `viewer_v0.html` (open-weld detection, `YEAR_RE` decade bug, forcing-target resolution,
  solidity legend relabel).

- **v1 addendum (lines 618–795):** eight asks from Pav's test-drive and what was built
  (harvest band, entity lifecycles, depth/context dial, NOW extension, honest math answer,
  global view, rival fade, encompass/absorption + theory DNA). Opus review fold at lines
  761–794: four low-priority cleanups applied.

- **v2 addendum (lines 798–923):** crash fix (sprite cache, DOM-write throttle, de-O(n^2)
  physics), conceived smear, orientation dial + weather, bedrock/L0 layer, draggable panels,
  click detail panel, narration track. Disclosure section + Opus review fold (four fixes).

- **v3 addendum (lines 927–1038):** 8th specimen (agnostic framework self-specimen), claim
  lifecycle render states, reflexive marker. Build/verification section.

**You must read the relevant addendum before modifying the viewer that corresponds to it.**
The spec is the authoritative record; the viewer implements it. If you add a feature to
`viewer_v3.html`, add an entry to the v3 addendum (or a new v3+ addendum block).

---

## PROXY_SPEC.md — versioned proxy weights

**Version:** `proxy-v2.0 (2026-06-10)`

Defines the exact numeric weights for three visual channels:

| Channel | Key function in viewer | Formula |
|---|---|---|
| **size (radius)** | `computeSize()` | `childBase(6) + |action_spaces_unlocked|*1.4 + |harvest.descendants|*1.6 + |weld.sub_welds|*0.8 + surprise_confidence*3`; then `clamp(8 + sqrt(size)*4.2, 9, 70)` |
| **solidity (opacity)** | `computeSolidity()` | 4-class proxy `{kernel, canon, artefact, protocol}`: `0.6*mean + 0.4*spanBonus`, clamped `[0.05, 1]`. Only `canon` is data-bound (`conf` + `inCertainCore`). |
| **weather direction** | `resolveForcingTargets()` | `{fund, accelerate, elevate}` → PULL; `{suppress, starve, kill}` → SQUEEZE; else REDIRECT. |

**Sync rule (load-bearing).** `PROXY_SPEC.md` and the `PROXY_SPEC` object embedded in the
viewer must stay identical. When you change a weight in the viewer, update the spec too and
bump the version string. The spec file exists precisely so "retune or retire the proxy" has a
concrete versioned target.

**Falsification targets (per-channel).**
- **size:** an external importance signal (citation count, downstream-merge count) that
  disagrees with list-length ordering forces a retune.
- **solidity:** opacity correlation with substrate `certainty`/`bucket` would expose the proxy;
  until verified, the `canon` axis is the only data-bound component — kernel/artefact/protocol
  are role constants.
- **weather:** direction is data-bound to `effect` strings; the absent R20 per-target `direction`
  field defaults to the event-level direction until specimens are back-filled.

---

## candidates/CLAIM_LIFECYCLE.md — states, parent/child, dead-children tally

**What it is (3 lines).** Tier-3 working draft formalising Pav's claim-lifecycle reframe:
a claim is demoted/dormant/friction-logged, never killed; a conjecture is a parent wrapper,
its experiment a child; the dead-children tally is the falsification-pressure gauge.

**States and their `SCHEMA_v2.md` bindings:**

| State | Maps onto | Status |
|---|---|---|
| `active` / `open-conjecture` | `child.status: active` / `open-conjecture` | REUSE |
| `demoted` | `child.status_trajectory[]` entry `{state: "demoted — from → to", when, by, continuity}` | REUSE |
| `dormant` | `child.status: dormant`; `weld.dormancy_intervals[]`; `lifecycle.phase_trajectory[]` dormancy phase | REUSE |
| `friction` | D6a `opposes[]` row `{from: experiment, target: claim, a_charge}`; `weld.lag`; `gates[]` | REUSE |
| `revival` | `weld.revival[]` `{when, by, trigger, kind: same|reinterpreted, method_continuity}` | REUSE |
| `friction-logged` | `open-conjecture` + `friction_tally` block | **PROPOSED-not-promoted** |
| `parent_dormant_pending_child` / `why_frame: operational` | `dormancy_intervals[].why_frame` new value | **PROPOSED-not-promoted** |

**The `friction_tally` block (PROPOSED):**
```json
{
  "parent": "conjecture id/name",
  "dead_children": [
    { "child": "name", "what_it_operationalized": "...", "killed_by": "...", "when": "...", "identity_break": true }
  ],
  "dead_count": 4,
  "live_children": [...],
  "live_count": 0,
  "best_result_so_far": "...",
  "revisit_trigger": "...",
  "pressure_reading": "none|normal|accumulating|heavy|critical"
}
```

**Pressure bands:** `none` (0 deaths) · `normal` (1 death, ≥1 live) · `accumulating` (2 deaths
or ≥1 death + 0 live) · `heavy` (≥3 deaths, 0 live) · `critical` (≥3 deaths, 0 live, stalled
high-water mark across last 2 children).

**Anti-gaming rules (append-only discipline):**
1. Dead children are **never deleted** from `dead_children[]` — append-only, dated.
2. A reinterpreted revival does **not** reset `dead_count`. Prior dead children remain tallied.
3. "Refine the estimator again" always costs +1 dead child.

**Current canonical case:** `parents-produce-W_C` has dead_count=4+ (children: witnessed-synergy,
functional-ANOVA/quotient, naive BES-4.4, frame-lock protocol specifics), live_count=0 real-corpus,
`gain_v2` pending, pressure_reading=**heavy**. This is the honest standing — not rescued by the
reframe, made legible by it.

---

## DATA CONTRACTS — what an agent must respect

### Append-only / never-modify
- `specimens/*.json` (7 base + agnostic_framework) — **ratified-frozen.** Never edit.
- `overlays/*.overlay.json` — **additive-only.** Never mutate base specimen fields.
- `SCHEMA_v2.md` — **ratified.** Never edit.
- `CLAIM_LIFECYCLE.md §3.1` dead-children entries — **append-only** by design; never delete a row.
- `PROXY_SPEC.md` version history — **append-only changelog.**

### Generated (never hand-edit these, regenerate instead)
- `viewer_v3.html` embedded JSON blocks — the 32 `<script type="application/json">` blocks are
  compiled from source files by `_reembed_agnostic.js` (for the self-specimen blocks) or manually
  extracted at build time. If you change a specimen/overlay/narration/substrate source, re-embed
  the blocks rather than hand-patching the inline JSON. The `<\/` escaping of `</` inside JSON
  strings is required so values cannot prematurely close the `<script>` tag.
- `substrate/compiled/*.compiled.json` — output of `substrate/compile_substrate.py`. Run the
  script; do not hand-edit compiled files.

### Ratified-frozen (do not edit, do not add new viewer versions based on these)
- `viewer_v0.html`, `viewer_v1.html`, `viewer_v2.html` — lineage, untouched.

### Mutable
- `viewer_v3.html` — may receive **surgical additive edits** (state hooks, new panels). After any
  edit: (a) run `node --check` on the extracted app script; (b) verify all 32 JSON blocks still
  parse; (c) verify the embedded `#lint` comment block passes.
- `VIEWER_SPEC.md` — append a new addendum block for any v3+ feature; never rewrite existing sections.
- `PROXY_SPEC.md` — bump version + append changelog entry when weights change.
- `toys/*.html` — freely editable; they are sandboxes with no external dependents.

---

## GOTCHAS

1. **VIEWER_SPEC.md is 1038 lines — never read the whole file in one call.** Use offset+limit or
   grep for the relevant section. The v3 addendum starts at line 927.

2. **viewer_v3.html is ~1.28 MB** — never read it whole. Extract the app script with a tool
   (Python `utf-8` read, or grep for `<script>` boundaries) before editing; then re-embed.
   PowerShell `Get-Content`/`Set-Content` round-trips were found to **double-encode non-ASCII**
   (mojibake on `→ × ▾ ✗ ✔`) — use Python or Bash UTF-8 tooling.

3. **ASCII-only commit messages required.** The viewer source and spec docs use Unicode symbols
   (`→ × ▾ ✗ ✔ ⟲ ⊔ ∈ ∅`). Git commit messages must stay ASCII to avoid hook failures and
   cross-platform encoding issues. Describe the change in plain ASCII; do not paste symbol
   characters into the commit message.

4. **`node --check` gate is mandatory after any viewer edit.** Extract the app script
   (everything between the closing `>` of the last JSON block and the `</script>` tag), write it
   to a temp `.js` file, run `node --check temp.js`. A syntax error here means the embedded
   script is broken. The check must pass **both** standalone and as embedded (the embedded
   version has the JSON blocks above it; a runaway string in the JSON that leaks into the script
   scope will break the embedded check even if standalone passes).

5. **CRLF warnings are normal** on Windows — git may warn about line-ending conversion for the
   `.html` files. The viewer must be saved as **UTF-8 / LF / no BOM**. The v3 build note
   explicitly documents that PowerShell `Set-Content` was abandoned in favour of Python for this
   reason.

6. **Embedded JSON blocks: the `</` escape rule.** Any JSON string value that contains `</`
   (e.g. a URL with a path like `/viewer</...>`) will prematurely close the surrounding
   `<script>` tag and break the HTML parser. The build process escapes `</` as `<\/` throughout
   embedded JSON. If you hand-patch an embedded block, apply the same escape.

7. **Band count must equal share vector length.** In the composition toy, `BANDS[key].length`
   must equal `phases[i].s.length` for all phases of that specimen. A mismatch causes silent
   rendering gaps (extra bands at 0 width, or out-of-bounds share reads).

8. **Proxy weights live in two places.** The numeric constants in `computeSize()` and
   `computeSolidity()` in the viewer AND in `PROXY_SPEC.md` must match exactly. If you change
   one, change both and bump the version.

9. **D6 / rival_coupling / R20 fields are schema-defined but present in zero specimens.** The
   viewer wires these layers but renders them empty by default. Do not fabricate data for them;
   the empty render is correct signal.

10. **`gain_v2` / MDL bits do not exist for any specimen.** The viewer is a disclosed-proxy
    illustrator, not a measuring instrument. Never add a label that presents a blob radius,
    opacity, or glow as a measurement. The honest-proxy badge and disclosure paragraph in the
    composition toy must be preserved.

---

## HOW TO MODIFY SAFELY — checklist

### Editing a toy (`toys/*.html`)
- [ ] Read the specific toy file before editing.
- [ ] Identify the relevant function from the file map above.
- [ ] If adding a new dataset: add to `DATA`/`SPECS`/`BANDS` (as appropriate), ensure band count
      matches share vector lengths, add the `<option>` to the `<select>`.
- [ ] If changing disclosure text: preserve the `MODELLED shape` badge and the honest-framing
      paragraph in the composition toy.
- [ ] No external dependents — no downstream check required.

### Editing viewer_v3.html (surgical additive edits only)
- [ ] Read the specific section you are changing (not the whole file).
- [ ] Extract the app script to a temp file; make your changes there first.
- [ ] Run `node --check temp_script.js` — must pass.
- [ ] Re-embed the script (UTF-8, LF, no BOM; escape any new `</` occurrences in JSON strings).
- [ ] Verify all 32 JSON blocks still parse (`JSON.parse` each block, or run the embedded
      `#lint` check).
- [ ] If you changed proxy weights: update `PROXY_SPEC.md` and bump the version.
- [ ] If you added a feature: append an entry to the v3 addendum in `VIEWER_SPEC.md`.
- [ ] Append a new addendum section (v3+) in `VIEWER_SPEC.md` if warranted.
- [ ] Commit with ASCII-only message.

### Adding a new specimen (to viewer_v3.html)
- [ ] Author the specimen JSON, overlay, narration, substrate following `SCHEMA_v2.md` and the
      existing v2/v3 specimens as templates.
- [ ] Do NOT modify the 7 ratified base specimen files or their overlays.
- [ ] Embed as four new `<script type="application/json">` blocks with the correct `id`/`data-key`/`data-kind` pattern matching existing blocks.
- [ ] `</`-escape the JSON; verify all (32+4) blocks parse.
- [ ] Add the specimen key to the `ORDER` array and a label to `LABELS`.
- [ ] `node --check` + lint pass required.

### Modifying PROXY_SPEC.md
- [ ] Change the weights in the viewer AND in the spec.
- [ ] Bump version string (`proxy-vX.Y (YYYY-MM-DD)`).
- [ ] Append a changelog entry at the bottom of the file.

### Modifying CLAIM_LIFECYCLE.md
- [ ] Dead-children entries are append-only. Do not delete or retroactively edit existing rows.
- [ ] PROPOSED states (`friction-logged`, `why_frame: operational`, `friction_tally`) remain
      PROPOSED until ratified by Cowork+Pav; do not fold them into `SCHEMA_v2.md` unilaterally.
- [ ] Pressure readings are qualitative bands — do not add numeric scores.

---

## VERIFICATION — how to prove your change works

### toys
1. Open the file in a browser (static or `file://`). All controls must respond.
2. Drag the canvas scrubber across the full range; verify readout updates.
3. For composition toy: hover across the spectrum; verify the readout shows band percentages
   at each position.
4. Toggle all buttons; verify visual changes match their labels.

### viewer_v3.html
1. `node --check extracted_script.js` must pass.
2. All 32 (or more) `<script type="application/json">` blocks must parse via
   `JSON.parse(block.textContent)` with zero errors.
3. Boot the viewer in a browser (static server or file://). Open all 8 specimen chips; verify
   no console errors.
4. For the self-specimen (chip 8, "Framework (self)"): scrub through the timeline; verify the
   reflexive banner appears; click demoted/friction nodes; verify the lifecycle badge and detail
   panel populate.
5. Global view: enable all lanes; verify the layout renders and the NOW line is visible.
6. If review server is running (`review_server.py` on :8742): verify the pin overlay still
   loads and existing pins render.

### Spec docs (VIEWER_SPEC.md, PROXY_SPEC.md, CLAIM_LIFECYCLE.md)
These are Markdown; no automated lint. Verify:
- Version strings updated (PROXY_SPEC.md).
- Addendum sections are appended, never rewritten.
- PROPOSED states remain flagged PROPOSED.
- Dead-children rows not deleted.

---

## How toys graduate into the viewer

A toy subsystem graduates when:

1. **The subsystem is needed in the viewer** (a Pav steer or a VIEWER_SPEC.md addendum asks
   for it).
2. **The toy's core functions are extractable** without the toy's standalone controls (the
   function boundary is clean — `buildAnchors()`, `uBase()`, `tOfU()`, `fish()` from the time
   axis toy are the canonical example: pure functions over data, no DOM coupling).
3. **The graduation does NOT require editing `viewer_v0/v1/v2.html`** (those are frozen).
4. **The viewer already embeds the required data** (or the data can be added as a new JSON
   block). The time-axis toy's event timestamps are a subset of what the viewer already reads
   from specimen `when` fields.

**Graduation path (time-axis toy):** the blend function (`buildAnchors` / `uBase` / `tOfU`)
and the Furnas fisheye (`fish`) are the atoms. In the viewer they would replace or augment the
current linear `timeX()` coordinate function. The `DATA` object stays in the toy; the viewer
reads dates from specimen fields.

**Graduation path (composition toy):** the `interpShares()` + `patFill()` + stacked-area
rendering pattern is the atom. In the viewer it would replace the flat theory-DNA bar with a
living spectrum tied to the specimen's `phase_trajectory[]` and overlay `theory_dna` fields.
The per-phase share vectors would need to be added to the overlay schema (currently `theory_dna`
is a single-point snapshot, not a phase series).

Neither toy graduation has been built as of 2026-06-11. The toys remain sandboxes.

---

*Tier-3 render tools — not canon, not a promotion. Convergence list stays 9. Authored 2026-06-11.*
