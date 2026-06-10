# PROXY_SPEC — render-channel proxy weights (viewer_v2)

**Version:** `proxy-v2.0 (2026-06-10)`
**Status:** Tier-3 render tool. NOT canon, NOT a tier promotion, does NOT grow the convergence list (stays 9).
**Why this file exists:** the INSTRUMENT meditation (Q1) asks for a *falsification condition* for each visual channel, and the Opus review flagged that the weights below lived as un-versioned magic numbers inside `computeSolidity`/`computeSize`. This file is the disclosed, version-controlled artifact those questions act on — so "retune or retire the proxy" has something concrete to change. The viewer reads the same numbers from a `PROXY_SPEC` object; **this doc and that object must stay in sync** (change both, bump the version).

> Honest-proxy discipline (v1 standard): every channel here is a **proxy** derived from list-lengths and confidence scores. Only `canon` is partly data-bound (it folds verified-confidence). NONE of these are MDL / `gain_v2` bits. The viewer is an **illustrator of a disclosed-proxy substrate**, not a measuring instrument. Do not present a blob radius, opacity, or glow as a measurement.

---

## Channel: node SIZE (radius)

`radius = clamp(8 + sqrt(size)*4.2, 9, 70)` where `size` is the proxy below.

**Child (the welded theory):**
```
size = childBase(6)
     + |action_spaces_unlocked| * 1.4   (aspace)
     + |harvest.descendants|    * 1.6   (descendant)
     + |weld.sub_welds|         * 0.8   (subweld)
     + surprise_confidence      * 3     (surprise)
```

**Every other role:**
```
size = base[role] + confidence * confGain(3)
base = { parent 4.5, descendant 3.6, cultural 3.0, aspace 2.8,
         relative 2.4, candidate 3.2, default 2.6 }
```

**What it is / is not:** size tracks *how many things a node is connected to in the harvested specimen* (Wikipedia-list cardinality) plus a SOFT confidence term. It does **not** measure the "mass" of an idea. **Falsification target:** an external importance signal (e.g. citation count, downstream-merge count from a held-out corpus) that disagrees with the list-length ordering would force a retune. Until such a check exists, size cannot be "wrong."

## Channel: node SOLIDITY (opacity)

A 4-class proxy `{kernel, canon, artefact, protocol}` combined as:
```
mean      = (kernel + canon + artefact + protocol) / 4
spanBonus = min(canon, max(artefact, protocol))
solidity  = clamp(combine.mean(0.6)*mean + combine.span(0.4)*spanBonus, floor(0.05), 1)
```

Class derivations:
```
kernel  = frame_layer.physical_membership
          (default: child 0.10, other 0.25)
canon   = clamp(0.45*conf + 0.55*inCertainCore(name) + (conf>=0.9 ? 0.15 : 0), 0, 1)
          conf default: child -> child.confidence||0.70 ; other -> 0.60
artefact/protocol = role-keyed constants (child reads harvest/adoption presence)
```

**What it is / is not:** only `canon` folds verified confidence; `kernel`/`artefact`/`protocol` are hand-set role constants. **Falsification target:** a low-certainty *pending* single-source value can still render at high opacity if its role constants are high — so solidity does **not** currently track source-certainty. A calibration check would require opacity to correlate with the substrate `certainty`/`bucket` of the node's own facts. (See INSTRUMENT Q2, DATA Q3.)

## Channel: WEATHER direction (forcing arrows)

Direction is **data-bound** — derived from the real `forcing_events.acted_on[].effect` string, not from the (absent) R20 `direction` field:
```
PULL    = {fund, accelerate, elevate}      -> green, single arrow toward puller
SQUEEZE = {suppress, starve, kill}         -> red, paired inward arrows
REDIRECT= (anything else)                  -> amber, sideways curve
```
Arrows are drawn **only** where a specimen actually carries `forcing_events` (3 of 7 specimens carry none -> no arrows). A small "data-bound" ring marks each event tag so a present arrow is never confused with a schema default.

## Channel: BEDROCK anchor lines (R3)

Bedrock *entries* are a curated L0 set; each entry discloses a `ref` binding to a substrate/specimen id. The faint **anchor lines** from roots to bedrock are drawn by **temporal proximity** (nearest bedrock by `|year - born|`), **NOT attested dependency** — this is disclosed on-canvas and in the legend. Treat the lines as "what was already on the ground when this root appeared," not "this root provably grew from that item."

---

## Change log
- `proxy-v2.0 (2026-06-10)` — extracted the inline magic numbers from `computeSize`/`computeSolidity` into a disclosed spec; documented the falsification target for each channel; recorded the weather direction set and the bedrock-anchor proximity heuristic. Numeric behaviour unchanged from the shipped viewer_v2 (extraction only).
