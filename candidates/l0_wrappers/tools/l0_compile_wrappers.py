#!/usr/bin/env python3
"""l0_compile_wrappers.py — the deferred L0 wrapper-view BUILDER (sweep-1 deliverable).

Tier-3 exploratory instrument tooling for the agnostic framework. STDLIB-ONLY
(json, argparse, pathlib, datetime, difflib) — the same constraint as
``../canonical_genealogy/substrate/compile_substrate.py``. Reads the compiled
substrate and *derives* each L0 wrapper view; the wrapper JSON is a COMPILED VIEW,
never a second source of truth (L0_WRAPPER_SPEC.md §2.9 doctrine #2).

Closes the sweep-1 LIMITS gap (§9): the six ``wrappers/<slug>.json`` files and the
constellation toy's inline data were hand-assembled / hand-transcribed snapshots that
drift on re-harvest. This builder regenerates them from
``compiled/l0-catalog.compiled.json`` so they stay in lockstep with the substrate.

  INPUT : ../canonical_genealogy/substrate/compiled/l0-catalog.compiled.json
          (subjects -> rows of {predicate,value,when,bucket,certainty,best_fact_id,
           source,provenance_refs,disputed_alternatives?})  [--substrate overrides]
  OUTPUT: wrappers/<slug>.json                         (--write)
          ../canonical_genealogy/toys/l0_constellation_toy.html  GENERATED data block (--write)
          group_configs/{...}.json                     (--write)

NAMING DISCREPANCY (resolved, kept): L0_WRAPPER_SPEC.md §1.1 file-map writes
``wrappers/<slug>.wrapper.json`` on ONE line, but every hand-assembled view ships as
``wrappers/<slug>.json`` (no ``.wrapper`` infix), and the template/substrate_binding,
the toy embed comment, and SWEEP_LOG all reference the bare ``<slug>.json`` form. This
builder keeps the EXISTING ``<slug>.json`` naming (the de-facto convention) and the
sweep-1 finalize note; the spec file-map line is corrected to match in the same commit.

DOCTRINE (the source-of-record rule). The compiled substrate is authoritative. Where a
hand file disagrees with the substrate on a fact-backed VALUE, this builder emits the
SUBSTRATE value and ``--check`` flags the hand-assembly error — it never silently adopts
the hand value (§2.9 doctrine #1-2; the finalize-pass "facts first" rule).

WHAT IS FACT-BACKED vs AUTHORED. The builder derives the following DIRECTLY from
substrate facts (these are the drift-comparison surface): names, abstraction
(level / ladder / level_by_scope), the whole membrane partition (kernel /
corroborated_soft / pending / unverifiable / disputed / scars), lifecycle, relations,
specimen_refs. Two field groups are classified by the spec itself as AUTHORED RENDER
ESTIMATES, *not* substrate facts (§2.5 frame weights; §2.8 frame-layer memberships):
the builder derives them from frame-weight / frame-layer facts WHERE those facts exist
in the substrate, and otherwise carries the instrument author's disclosed estimates as
documented compiler constants (``_AUTHORED_FRAMES`` / ``_AUTHORED_FRAME_LAYER``) so the
group renders keep working and the estimates stay disclosed. Toy layout (node positions,
proposed-node display labels, ladder family titles) is likewise display-only config, not
substrate, carried in ``_TOY_LAYOUT``. None of these authored constants are part of the
substrate-drift diff; the fact-backed frame-layer values ARE checked against substrate.

Usage:
  python tools/l0_compile_wrappers.py            # alias for --check
  python tools/l0_compile_wrappers.py --check    # semantic diff vs wrappers/<slug>.json
  python tools/l0_compile_wrappers.py --write     # regen wrappers + toy + group_configs
  python tools/l0_compile_wrappers.py --write --no-toy --no-groups   # wrappers only
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

COMPILER_STAMP = "tools/l0_compile_wrappers.py v1"
SCHEMA_VERSION = "0.1-l0-wrapper"

# ---------------------------------------------------------------------------
# Layout (paths resolved relative to the repo, not the cwd)
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent           # candidates/l0_wrappers/tools
L0_DIR = HERE.parent                              # candidates/l0_wrappers
CANDIDATES = L0_DIR.parent                        # candidates
CG = CANDIDATES / "canonical_genealogy"
DEFAULT_SUBSTRATE = CG / "substrate" / "compiled" / "l0-catalog.compiled.json"
WRAPPERS_DIR = L0_DIR / "wrappers"
GROUPS_DIR = L0_DIR / "group_configs"
TOY = CG / "toys" / "l0_constellation_toy.html"

# The six sweep-1 samples (non-proposed subjects). proposed:* subjects appear in the
# compiled view only as relation targets / inverse-edge sources and get NO wrapper file.
SAMPLE_SLUGS = [
    "smartphone", "iphone-15-pro", "claude",
    "alan-turing", "acetylsalicylic-acid", "turing-enigma-hodges",
]

# Open kind vocabulary (spec §2.0); used to recover `kind` from an instance-of target
# when no explicit `kind` fact exists (e.g. alan-turing).
KIND_VOCAB = {
    "object", "device-model", "ai-model", "person", "compound", "book",
    "idea", "institution", "place", "work", "event",
}

# Predicate names that are lifecycle EVENTS, per kind (spec §2.6). A lifecycle row is
# emitted only when the predicate is in this set AND the fact value is date-like
# (starts with a 3-4 digit year) — naming/descriptive predicates whose value is not a
# bare date are intentionally NOT auto-extracted (a future sweep should emit dedicated
# date facts; doing date-parsing of prose here would invent precision, UI law §5.4).
LIFECYCLE_PREDICATES = {
    "object": ["emerged", "named", "mass_adoption"],
    "device-model": ["announced", "released", "discontinued", "superseded_when"],
    "ai-model": ["claude_first_trained", "announced", "released", "claude2_released",
                 "claude3_family_released", "ios_app_released", "android_app_released"],
    "person": ["born", "died", "active_from", "active_to"],
    "compound": ["first_synthesized", "first_synthesized_pure_stable_form",
                 "first_marketed", "genericized", "mechanism_discovery_year"],
    "book": ["written", "published"],
}
_DATE_LIKE = re.compile(r"^\s*\d{3,4}")

# ---------------------------------------------------------------------------
# AUTHORED RENDER ESTIMATES — spec §2.5 / §2.8 classify these as NOT substrate facts.
# Carried here (disclosed) so group renders keep working. Where the substrate DOES carry
# a structured frame-layer fact, that fact wins and is checked; these are the fallback.
# Sourced from the instrument author's sweep-1 values. NOT part of the substrate-drift diff.
# ---------------------------------------------------------------------------
_AUTHORED_FRAMES = {
    # frame-weight facts exist in the substrate ONLY for turing-enigma-hodges; the other
    # five carry no frames_<channel> facts, so these authored weights are used (disclosed).
    "smartphone": {"time": 0.5, "space": 0.8, "knowledge": 0.4, "meaning": 0.5},
    "iphone-15-pro": {"time": 0.75, "space": 0.6, "knowledge": 0.5, "meaning": 0.45},
    "claude": {"time": 0.6, "space": 0.3, "knowledge": 0.95, "meaning": 0.8},
    "alan-turing": {"time": 0.9, "space": 0.3, "knowledge": 0.95, "meaning": 0.85},
    "acetylsalicylic-acid": {"time": 0.6, "space": 0.8, "knowledge": 0.7, "meaning": 0.5},
}
_AUTHORED_FRAME_LAYER = {
    # Fallback only. iphone-15-pro has NO frame_layer fact; claude's frame_layer fact is a
    # prose string (l0-claude-0017, "latent with physical infrastructure membership"), not
    # a structured membership, so the authored memberships below are used for claude too.
    "iphone-15-pro": {"layer": "straddle", "physical_membership": 0.85, "latent_membership": 0.6},
    "claude": {"layer": "straddle", "physical_membership": 0.2, "latent_membership": 0.95},
}

# ---------------------------------------------------------------------------
# TOY DISPLAY LAYOUT — node positions, proposed-node labels, ladder titles.
# Display-only config; not substrate facts (node coordinates and pretty labels are not
# harvested). Carried so the regenerated toy keeps its hand-tuned layout. The DATA inside
# each node (facts, buckets, certainties, lifecycle, edges) is regenerated from substrate.
# ---------------------------------------------------------------------------
_TOY_LAYOUT = {
    "pos": {
        "smartphone": [0.77, 0.84], "iphone-15-pro": [0.62, 0.66], "claude": [0.50, 0.40],
        "alan-turing": [0.24, 0.28], "acetylsalicylic-acid": [0.86, 0.24],
        "turing-enigma-hodges": [0.12, 0.58],
    },
    "plab": {
        "proposed:apple": "Apple", "proposed:iphone-14-pro": "iPhone 14 Pro",
        "proposed:large-language-model": "large language model", "proposed:anthropic": "Anthropic",
        "proposed:person": "person", "proposed:turing-award": "Turing Award",
        "proposed:andrew-hodges": "Andrew Hodges", "proposed:imitation-game": "The Imitation Game",
        "proposed:breaking-the-code-play": "Breaking the Code", "proposed:biography": "biography",
        "proposed:bayer": "Bayer", "proposed:mobile-device": "mobile device",
        "proposed:device-category": "device category", "proposed:iphone": "iPhone (line)",
        "proposed:bayer-aspirin": "Aspirin (Bayer brand)",
        "proposed:claude-3-opus": "Claude 3 Opus", "proposed:claude-3-sonnet": "Claude 3 Sonnet",
        "proposed:claude-3-haiku": "Claude 3 Haiku", "proposed:claude-3-5-sonnet": "Claude 3.5 Sonnet",
        "proposed:claude-4": "Claude 4", "proposed:claude-fable-5": "Claude Fable 5",
        "proposed:salicylate-class": "salicylate class",
    },
    "ladder_titles": {
        "smartphone": "object", "claude": "ai-model",
        "acetylsalicylic-acid": "compound", "alan-turing": "person",
        "turing-enigma-hodges": "book",
    },
}


# ---------------------------------------------------------------------------
# Helpers over the compiled view
# ---------------------------------------------------------------------------
def load_compiled(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    subs = data.get("subjects", {})
    return data, subs


def is_estimate(row):
    """Estimate/proxy-tagged? The compiled view drops `notes`, so we detect via an
    ESTIMATE:/PROXY: marker in the value when it is a string (the harvest convention)."""
    v = row.get("value")
    if isinstance(v, str) and ("ESTIMATE" in v or "PROXY" in v):
        return True
    return False


def norm_target(slug, catalog):
    """Map a bare/proposed target slug to its wrapper reference form."""
    if slug is None:
        return None
    if slug.startswith("proposed:"):
        return slug
    if slug in catalog:
        return "l0:" + slug
    return "proposed:" + slug


def rel_type_target(row):
    """For a rel:<type>:<target> predicate row, return (type, target_slug)."""
    pred = row["predicate"]
    parts = pred.split(":", 2)              # ['rel', <type>, <rest>]
    rtype = parts[1] if len(parts) >= 2 else pred
    target = None
    val = row.get("value")
    if isinstance(val, dict):
        target = val.get("target")
    if target is None and len(parts) >= 3:
        target = parts[2]
    return rtype, target


def is_rel(row):
    return isinstance(row.get("predicate"), str) and row["predicate"].startswith("rel:")


def build_edge_index(subjects):
    """Every rel:* row across ALL compiled subjects (incl. proposed:* subjects), as
    a list of dicts. Used for outgoing relations AND inverse-ladder reconstruction."""
    edges = []
    for subj, rows in subjects.items():
        for r in rows:
            if not is_rel(r):
                continue
            rtype, target = rel_type_target(r)
            note = r["value"].get("note", "") if isinstance(r.get("value"), dict) else ""
            edges.append({
                "subject": subj, "type": rtype, "target": target,
                "bucket": r.get("bucket"), "certainty": r.get("certainty"),
                "best_fact_id": r.get("best_fact_id"), "note": note,
            })
    return edges


def find_rows(rows, predicate):
    return [r for r in rows if r.get("predicate") == predicate]


def first_value(rows, predicate, default=None):
    hits = find_rows(rows, predicate)
    return hits[0]["value"] if hits else default


# ---------------------------------------------------------------------------
# Section assembly (per the wrapper.template.json key order)
# ---------------------------------------------------------------------------
def derive_kind(rows, edges_out):
    raw = first_value(rows, "kind")
    if isinstance(raw, str) and raw:
        # strip a parenthetical qualifier, e.g. "object (generic)" -> "object"
        return raw.split("(")[0].strip()
    # fall back to an instance-of target that is a kind term (e.g. alan-turing -> person)
    for e in edges_out:
        if e["type"] == "instance-of" and e["target"] in KIND_VOCAB:
            return e["target"]
    return ""


def assemble_names(rows, slug):
    canonical = first_value(rows, "canonical_name", "")
    aka = first_value(rows, "aka", [])
    if isinstance(aka, str):
        aka = [aka]
    refs = []
    cn = find_rows(rows, "canonical_name")
    if cn:
        refs.append(cn[0]["best_fact_id"])
    ak = find_rows(rows, "aka")
    if ak:
        refs.append(ak[0]["best_fact_id"])
    return {"canonical": canonical, "aka": aka, "fact_refs": refs}


def assemble_abstraction(rows, slug, edges_out, edges_all, catalog):
    # level: explicit unscoped abstraction_level fact, else derived from ladder.
    level_fact = find_rows(rows, "abstraction_level")
    scoped = sorted((r for r in rows if r["predicate"].startswith("abstraction_level:")),
                    key=lambda r: r["predicate"])
    level_by_scope = {}
    for r in scoped:
        scope = r["predicate"].split(":", 1)[1]
        level_by_scope[scope] = r["value"]

    # ladder.generalizes_to: explicit generalizes_to fact, else an outgoing
    # subclass-of / instance-of edge target.
    gen = first_value(rows, "generalizes_to")
    if isinstance(gen, str) and gen:
        generalizes_to = gen if gen.startswith(("l0:", "proposed:")) else norm_target(gen, catalog)
    else:
        generalizes_to = None
        for e in edges_out:
            if e["type"] in ("subclass-of", "instance-of") and e["bucket"] != "unverifiable":
                generalizes_to = norm_target(e["target"], catalog)
                break

    # ladder.specializes_to: explicit specializes_to fact list, then inverse edges
    # (any subject X with a pending/corroborated instance-of|subclass-of|brand-of edge
    #  whose target is this slug).
    specializes_to = []
    spec_fact = first_value(rows, "specializes_to")
    if isinstance(spec_fact, list):
        for s in spec_fact:
            ref = s if str(s).startswith(("l0:", "proposed:")) else norm_target(s, catalog)
            if ref not in specializes_to:
                specializes_to.append(ref)
    for e in sorted(edges_all, key=lambda e: e["subject"]):
        if e["target"] == slug and e["type"] in ("instance-of", "subclass-of", "brand-of") \
                and e["bucket"] != "unverifiable":
            ref = norm_target(e["subject"], catalog)
            if ref not in specializes_to:
                specializes_to.append(ref)

    # derived default level if no explicit fact
    if level_fact:
        level = level_fact[0]["value"]
    else:
        has_inst_or_brand = any(e["type"] in ("instance-of", "brand-of")
                                and e["bucket"] != "unverifiable" for e in edges_out)
        if generalizes_to is None and not has_inst_or_brand:
            level = "generic"
        elif has_inst_or_brand:
            level = "instance"
        else:
            level = "class"

    # fact_refs: the level fact(s) + the ladder-edge facts
    refs = []
    for r in level_fact:
        refs.append(r["best_fact_id"])
    for r in scoped:
        refs.append(r["best_fact_id"])
    gfacts = find_rows(rows, "generalizes_to")
    for r in gfacts:
        refs.append(r["best_fact_id"])
    for e in edges_out:
        if e["type"] in ("subclass-of", "instance-of") and e["bucket"] != "unverifiable":
            refs.append(e["best_fact_id"])
            break
    sfacts = find_rows(rows, "specializes_to")
    for r in sfacts:
        refs.append(r["best_fact_id"])
    for e in sorted(edges_all, key=lambda e: e["subject"]):
        if e["target"] == slug and e["type"] in ("instance-of", "subclass-of", "brand-of") \
                and e["bucket"] != "unverifiable":
            refs.append(e["best_fact_id"])
    # de-dup, preserve order
    seen, uref = set(), []
    for r in refs:
        if r and r not in seen:
            seen.add(r)
            uref.append(r)

    return {
        "level": level,
        "ladder": {"generalizes_to": generalizes_to, "specializes_to": specializes_to},
        "level_by_scope": level_by_scope,
        "fact_refs": uref,
    }


def membrane_row(row):
    """Compiled fact row -> wrapper membrane entry (the rendered fields)."""
    return {
        "fact_id": row.get("best_fact_id"),
        "predicate": row.get("predicate"),
        "value": row.get("value"),
        "bucket": row.get("bucket"),
        "certainty": row.get("certainty"),
    }


def assemble_membrane(rows):
    """Partition every compiled row into kernel / membrane buckets (spec §2.3-§2.4).

    Mechanical, from the compiled bucket + certainty + estimate tag. A row is `disputed`
    iff its bucket is `disputed` OR it carries a non-empty `disputed_alternatives` (a
    verifier-recorded contradiction). NB: a hand file may pre-classify a `pending` fact as
    disputed using out-of-band prose (the compiler drops `notes`); the substrate-faithful
    view keeps such a fact in `pending` until a disputed VERIFICATION record lands.
    """
    kernel_facts, corr_soft, pending, unverifiable, disputed, scars = [], [], [], [], [], []
    for r in rows:
        bucket = r.get("bucket")
        cert = r.get("certainty") or 0.0
        est = is_estimate(r)
        has_dispute = bool(r.get("disputed_alternatives"))
        entry = membrane_row(r)
        # Relation (rel:*) facts are surfaced in relations[]. Only RETIRED relation facts
        # (bucket=unverifiable) belong in the membrane — in membrane.unverifiable (spec §2.7;
        # the 7 sweep-1 demoted edges). Pending/corroborated relation facts are NOT also
        # listed in the membrane (no double-listing).
        if is_rel(r):
            if bucket == "unverifiable":
                unverifiable.append(entry)
            continue
        if bucket == "disputed" or has_dispute:
            if r.get("disputed_alternatives"):
                entry["disputed_alternatives"] = r["disputed_alternatives"]
            disputed.append(entry)
        elif bucket == "corroborated":
            if cert >= 0.7 and not est:
                kernel_facts.append({
                    "fact_id": r.get("best_fact_id"),
                    "predicate": r.get("predicate"),
                    "value": r.get("value"),
                    "battle_count": max(0, (r.get("n_facts") or 1) - 1),
                })
            else:
                corr_soft.append(entry)
        elif bucket == "unverifiable":
            unverifiable.append(entry)
        else:  # pending (and anything unknown -> treated as fuzzy frontier)
            pending.append(entry)

    kernel_statement = ""  # populated only when kernel_facts is non-empty (sweep-2+)
    kernel = {"statement": kernel_statement, "facts": kernel_facts}
    membrane = {
        "corroborated_soft": corr_soft,
        "pending": pending,
        "unverifiable": unverifiable,
        "disputed": disputed,
        "scars": scars,
        "open_questions": [],   # candidate edges / gaps are hand-authored prose, not in substrate
    }
    return kernel, membrane


def assemble_frames(rows, slug):
    # frame-weight facts exist only where the harvest emitted frames_<channel>;
    # otherwise carry the disclosed authored estimate (spec §2.5).
    out = {}
    refs = []
    backed = False
    for ch in ("time", "space", "knowledge", "meaning"):
        hit = find_rows(rows, "frames_" + ch)
        if hit:
            out[ch] = hit[0]["value"]
            refs.append(hit[0]["best_fact_id"])
            backed = True
        else:
            out[ch] = None
    if not backed and slug in _AUTHORED_FRAMES:
        out = dict(_AUTHORED_FRAMES[slug])
    note = ("MANDATORY DISCLOSURE: observer-global-kernel relevance weights are AUTHORED "
            "RENDER ESTIMATES in [0,1], not measured quantities and not substrate facts "
            "(spec §2.5). Any toy/viewer rendering them owes an adjacent estimate/proxy "
            "disclosure (UI_GUIDELINES §5).")
    if backed:
        note += " Source: frames_<channel> facts " + ", ".join(refs) + "."
    else:
        note += (" No frames_<channel> facts exist for this subject in the substrate; "
                 "values are the instrument author's disclosed estimate (carried by the "
                 "builder as an authored constant, not a substrate fact).")
    result = {"time": out["time"], "space": out["space"],
              "knowledge": out["knowledge"], "meaning": out["meaning"],
              "_estimate_note": note}
    return result


def assemble_frame_layer(rows, slug):
    # Prefer a structured frame-layer fact; fall back to authored memberships.
    fact = None
    fid = None
    for pred in ("frame_layer", "frame_layer_assessment", "frame_layer_estimate"):
        hit = find_rows(rows, pred)
        if hit and isinstance(hit[0]["value"], dict):
            fact = hit[0]["value"]
            fid = hit[0]["best_fact_id"]
            break
    phys_fact = find_rows(rows, "frame_layer_physical_membership")
    lat_fact = find_rows(rows, "frame_layer_latent_membership")
    refs = []
    if fact is not None:
        layer = fact.get("layer", "straddle")
        phys = fact.get("physical_membership")
        lat = fact.get("latent_membership")
        refs.append(fid)
    elif phys_fact and lat_fact:
        # smartphone encodes membership as two scalar facts; layer not asserted -> straddle.
        phys = phys_fact[0]["value"]
        lat = lat_fact[0]["value"]
        layer = "straddle"
        refs.extend([phys_fact[0]["best_fact_id"], lat_fact[0]["best_fact_id"]])
    elif slug in _AUTHORED_FRAME_LAYER:
        a = _AUTHORED_FRAME_LAYER[slug]
        layer, phys, lat = a["layer"], a["physical_membership"], a["latent_membership"]
    else:
        layer, phys, lat = "straddle", None, None
    note = "authored analytic estimate, not a substrate fact (spec §2.8)."
    if refs:
        note += " Memberships from frame-layer fact(s) " + ", ".join(refs) + "."
    else:
        note += (" No structured frame-layer fact for this subject; values are the "
                 "instrument author's disclosed estimate (builder constant).")
    out = {"layer": layer, "physical_membership": phys, "latent_membership": lat,
           "_estimate_note": note}
    if refs:
        out["fact_refs"] = refs
    return out


def assemble_lifecycle(rows, kind):
    preds = LIFECYCLE_PREDICATES.get(kind, [])
    out = []
    for r in rows:
        if r["predicate"] in preds:
            val = r.get("value")
            when = val if isinstance(val, str) else (r.get("when") or "")
            if isinstance(val, str) and not _DATE_LIKE.match(val):
                continue  # descriptive (non-date) value -> not auto-extracted
            out.append({"event": r["predicate"], "when": when,
                        "fact_refs": [r["best_fact_id"]]})
    # stable order: by when then predicate
    out.sort(key=lambda e: (str(e["when"]), e["event"]))
    return out


def assemble_relations(edges_out, catalog):
    """Outgoing rel:* edges that are NOT unverifiable (those land in membrane.unverifiable).
    Only fact-backed edges belong here (spec §2.7 hard rule)."""
    out = []
    for e in sorted(edges_out, key=lambda e: (e["type"], str(e["target"]))):
        if e["bucket"] == "unverifiable":
            continue
        out.append({
            "type": e["type"],
            "target": norm_target(e["target"], catalog),
            "fact_refs": [e["best_fact_id"]],
            "bucket": e["bucket"],
            "certainty": e["certainty"],
        })
    return out


def assemble_specimen_refs(rows):
    out = []
    for pred in ("specimen_convergence_ref", "specimen_ref"):
        for r in find_rows(rows, pred):
            v = r.get("value")
            if isinstance(v, dict):
                out.append({
                    "specimen": v.get("specimen", ""),
                    "subject_id": v.get("subject_id", ""),
                    "relation": v.get("relation", "implicit-in"),
                    "note": v.get("note", ""),
                    "fact_refs": [r["best_fact_id"]],
                })
    return out


def assemble_wrapper(slug, subjects, catalog, generated):
    rows = subjects[slug]
    edges_all = build_edge_index(subjects)
    edges_out = [e for e in edges_all if e["subject"] == slug]

    kind = derive_kind(rows, edges_out)
    names = assemble_names(rows, slug)
    abstraction = assemble_abstraction(rows, slug, edges_out, edges_all, catalog)
    kernel, membrane = assemble_membrane(rows)
    frames = assemble_frames(rows, slug)
    lifecycle = assemble_lifecycle(rows, kind)
    relations = assemble_relations(edges_out, catalog)
    frame_layer = assemble_frame_layer(rows, slug)
    specimen_refs = assemble_specimen_refs(rows)

    return {
        "_doc": ("L0 wrapper — GENERATED compiled view (do not hand-edit). Built by "
                 + COMPILER_STAMP + " from the compiled substrate. The wrapper JSON is a "
                 "compiled view over substrate facts, never a second source of truth "
                 "(L0_WRAPPER_SPEC.md §2.9). Edit facts/*.jsonl + recompile, then rerun "
                 "this builder. Kernel is empty whenever no fact is corroborated+cert>=0.7."),
        "_status": ("Tier-3 WORKING wrapper view — exploratory, surfaced for Cowork+Pav "
                    "ratification. NOT canon, NOT a tier promotion, convergence list stays 9."),
        "schema_version": SCHEMA_VERSION,
        "wrapper_id": "l0:" + slug,
        "kind": kind,
        "names": names,
        "abstraction": abstraction,
        "kernel": kernel,
        "membrane": membrane,
        "frames": frames,
        "lifecycle": lifecycle,
        "relations": relations,
        "frame_layer": frame_layer,
        "specimen_refs": specimen_refs,
        "substrate_binding": {
            "specimen": "l0-catalog",
            "facts_files": [
                "../canonical_genealogy/substrate/facts/l0_catalog.entities.jsonl",
                "../canonical_genealogy/substrate/facts/l0_catalog.relations.jsonl",
            ],
            "verifications_file": "../canonical_genealogy/substrate/verifications/l0_catalog.jsonl",
            "compiled_from": "../canonical_genealogy/substrate/compiled/l0-catalog.compiled.json",
            "fact_id_namespaces": {
                "entities": "l0-" + slug + "-NNNN",
                "relations": "l0-" + slug + "-rNNNN",
            },
            "generated": generated,
            "compiler": COMPILER_STAMP,
            "hand_assembled": False,
        },
    }


# ---------------------------------------------------------------------------
# Semantic diff (for --check)
# ---------------------------------------------------------------------------
STAMP_KEYS = {"generated", "compiler", "hand_assembled"}
# Render/prose helper keys carried by the hand files that are NOT substrate content
# (the compiled view has no per-fact note, no hardness proxy, no kernel prose digest).
# Dropped from the diff so it surfaces only fact-backed value drift.
HELPER_KEYS = {"note", "hardness_proxy", "statement"}


def normalize(obj):
    """Drop `_`-prefixed prose keys, the 3 stamp keys, and render-helper keys, recursively,
    so the diff sees only substrate content."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and (k.startswith("_") or k in STAMP_KEYS or k in HELPER_KEYS):
                continue
            out[k] = normalize(v)
        return out
    if isinstance(obj, list):
        return [normalize(x) for x in obj]
    return obj


def _list_key(elem):
    """Stable identity for an element of a fact-row / relation / lifecycle / specimen list,
    so lists are diffed order-insensitively. None for unkeyable (scalar) elements."""
    if isinstance(elem, dict):
        if "fact_id" in elem:
            return ("fid", elem["fact_id"])
        if "type" in elem and "target" in elem:
            return ("rel", elem["type"], elem["target"])
        if "event" in elem and "when" in elem:
            return ("life", elem["event"], elem["when"])
        if "specimen" in elem and "subject_id" in elem:
            return ("spec", elem["specimen"], elem["subject_id"])
    return None


def diff_tree(hand, comp, path, out):
    if isinstance(hand, dict) and isinstance(comp, dict):
        for k in sorted(set(hand) | set(comp)):
            if k not in hand:
                out.append((path + "/" + k, "<absent>", _short(comp[k])))
            elif k not in comp:
                out.append((path + "/" + k, _short(hand[k]), "<absent>"))
            else:
                diff_tree(hand[k], comp[k], path + "/" + k, out)
    elif isinstance(hand, list) and isinstance(comp, list):
        hk = [_list_key(x) for x in hand]
        ck = [_list_key(x) for x in comp]
        if all(k is not None for k in hk) and all(k is not None for k in ck):
            # keyed (order-insensitive) diff
            hand_map = {k: v for k, v in zip(hk, hand)}
            comp_map = {k: v for k, v in zip(ck, comp)}
            for k in hk:
                if k not in comp_map:
                    out.append((path + " -" + _keystr(k), _short(hand_map[k]), "<removed>"))
            for k in ck:
                if k not in hand_map:
                    out.append((path + " +" + _keystr(k), "<added>", _short(comp_map[k])))
            for k in hk:
                if k in comp_map:
                    diff_tree(hand_map[k], comp_map[k], path + "{" + _keystr(k) + "}", out)
        else:
            # scalar list: compare as multiset (order-insensitive) to cut noise
            if sorted(map(_canon, hand)) != sorted(map(_canon, comp)):
                out.append((path + " (list)", _short(hand), _short(comp)))
    else:
        if hand != comp:
            out.append((path, _short(hand), _short(comp)))


def _canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def _keystr(k):
    return ":".join(str(x) for x in k[1:]) if isinstance(k, tuple) else str(k)


def _short(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= 90 else s[:87] + "..."


def check(subjects, catalog, generated):
    total = 0
    print("=" * 72)
    print("L0 WRAPPER BUILDER — --check (compiled substrate vs wrappers/<slug>.json)")
    print("Doctrine: substrate is source of record; a hand/substrate value mismatch is a")
    print("hand-assembly error (builder emits the substrate value; never adopts the hand).")
    print("=" * 72)
    for slug in SAMPLE_SLUGS:
        comp = assemble_wrapper(slug, subjects, catalog, generated)
        path = WRAPPERS_DIR / (slug + ".json")
        if not path.exists():
            print("  %-24s  (no hand file — would be created by --write)" % slug)
            continue
        hand = json.loads(path.read_text(encoding="utf-8"))
        diffs = []
        diff_tree(normalize(hand), normalize(comp), "", diffs)
        total += len(diffs)
        if diffs:
            print("\n  %s  — %d content diff(s):" % (slug, len(diffs)))
            for p, h, c in diffs:
                print("      %s" % p)
                print("          hand     : %s" % h)
                print("          compiled : %s" % c)
        else:
            print("\n  %s  — clean (0 content diffs)" % slug)
    print("\n" + "-" * 72)
    print("TOTAL content diffs: %d" % total)
    print("-" * 72)
    return total


# ---------------------------------------------------------------------------
# Write wrappers
# ---------------------------------------------------------------------------
def write_wrappers(subjects, catalog, generated):
    WRAPPERS_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for slug in SAMPLE_SLUGS:
        w = assemble_wrapper(slug, subjects, catalog, generated)
        path = WRAPPERS_DIR / (slug + ".json")
        path.write_text(json.dumps(w, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path.name)
    return written


# ---------------------------------------------------------------------------
# Toy data-block regeneration
# ---------------------------------------------------------------------------
def snippet(value, limit=80):
    """Deterministic short display string for a substrate value (toy value-snippet)."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        s = value
    elif isinstance(value, list):
        s = " / ".join(snippet(x, limit) for x in value)
    elif isinstance(value, dict):
        if "target" in value:
            s = str(value["target"])
        else:
            s = "; ".join("%s: %s" % (k, value[k]) for k in value)
    else:
        s = str(value)
    s = s.replace("\n", " ").strip()
    return s if len(s) <= limit else s[:limit - 3] + "..."


def src_note(row):
    """Short source/estimate note for the toy fact tuple ([6])."""
    if is_estimate(row):
        return "ESTIMATE/PROXY: authored render estimate; hardness capped <=0.5"
    src = row.get("source") or {}
    title = src.get("title") or ""
    stype = src.get("type") or ""
    note = title
    if isinstance(row.get("value"), dict) and row["value"].get("note"):
        note = row["value"]["note"]
    note = note.replace("\n", " ").strip()
    if len(note) > 80:
        note = note[:77] + "..."
    return note


def build_toy_data(subjects, catalog):
    """Build the W / EDGES / CANDS / PLAB / LADDERS arrays from the compiled view."""
    pos = _TOY_LAYOUT["pos"]
    plab = _TOY_LAYOUT["plab"]
    titles = _TOY_LAYOUT["ladder_titles"]
    edges_all = build_edge_index(subjects)

    # ---- W (nodes) ----
    W = []
    for slug in SAMPLE_SLUGS:
        rows = subjects[slug]
        edges_out = [e for e in edges_all if e["subject"] == slug]
        kind = derive_kind(rows, edges_out)
        abstraction = assemble_abstraction(rows, slug, edges_out, edges_all, catalog)
        frames = assemble_frames(rows, slug)
        fl = assemble_frame_layer(rows, slug)
        life = [[lc["event"], lc["when"], ""] for lc in assemble_lifecycle(rows, kind)]
        ladder = {
            "up": abstraction["ladder"]["generalizes_to"],
            "downs": abstraction["ladder"]["specializes_to"],
        }
        if abstraction["level_by_scope"]:
            ladder["scope"] = abstraction["level_by_scope"]
        facts = []
        for r in rows:
            bucket = r.get("bucket")
            override = "disputed" if (bucket == "disputed" or r.get("disputed_alternatives")) else ""
            facts.append([
                r.get("best_fact_id"), r.get("predicate"), snippet(r.get("value")),
                bucket, r.get("certainty"), override, src_note(r),
            ])
        node = {
            "id": slug,
            "label": first_value(rows, "canonical_name", slug),
            "kind": kind,
            "level": abstraction["level"],
            "pos": pos.get(slug, [0.5, 0.5]),
            "fr": {"time": frames["time"], "space": frames["space"],
                   "knowledge": frames["knowledge"], "meaning": frames["meaning"]},
            "layer": {"n": fl["layer"], "phys": fl["physical_membership"],
                      "lat": fl["latent_membership"]},
            "ladder": ladder,
            "life": life,
            "facts": facts,
        }
        W.append(node)

    # ---- EDGES (solid, fact-backed, non-unverifiable outgoing edges) ----
    EDGES = []
    for e in edges_all:
        if e["subject"] not in catalog:
            continue  # solid edges originate from the six catalog samples
        if e["bucket"] == "unverifiable":
            continue
        EDGES.append({
            "f": e["subject"],
            "t": norm_target(e["target"], catalog).split("l0:")[-1]
                 if norm_target(e["target"], catalog).startswith("l0:")
                 else norm_target(e["target"], catalog),
            "ty": e["type"],
            "c": e["certainty"],
            "refs": [e["best_fact_id"]],
            "src": e["note"][:120] if e["note"] else "",
            "cat": (e["target"] in catalog),
        })

    # ---- CANDS (retired/unverifiable edges as ghosts — the '(inverse)' set) ----
    CANDS = []
    for e in edges_all:
        if e["bucket"] != "unverifiable":
            continue
        tgt = norm_target(e["target"], catalog)
        tgt = tgt[3:] if tgt.startswith("l0:") else tgt
        CANDS.append({
            "f": e["subject"], "t": tgt, "ty": e["type"] + " (retired/inverse)",
            "src": "RETIRED sweep-1 (unverifiable): reversed-direction or multi-hop "
                   "candidate; the correctly-directed counterpart is the solid edge. "
                   + (e["note"][:80] if e["note"] else ""),
        })

    # ---- PLAB (display labels for proposed: nodes that actually appear) ----
    appearing = set()
    for e in EDGES:
        if str(e["t"]).startswith("proposed:"):
            appearing.add(e["t"])
    for c in CANDS:
        if str(c["t"]).startswith("proposed:"):
            appearing.add(c["t"])
    for node in W:
        up = node["ladder"]["up"]
        if isinstance(up, str) and up.startswith("proposed:"):
            appearing.add(up)
        for d in node["ladder"]["downs"]:
            if isinstance(d, str) and d.startswith("proposed:"):
                appearing.add(d)
    PLAB = {k: plab.get(k, k.split("proposed:")[-1].replace("-", " ")) for k in sorted(appearing)}

    # ---- LADDERS (one family per catalog sample that roots/sits on a ladder) ----
    # Build each family from substrate ladder edges: walk generalizes_to upward and
    # collect specializes_to downward; title is display config.
    LADDERS = []
    ladder_keys = ["smartphone", "claude", "acetylsalicylic-acid", "alan-turing", "turing-enigma-hodges"]
    label_for = {}
    for node in W:
        label_for[node["id"]] = node["label"]
    for k in ladder_keys:
        node = next(n for n in W if n["id"] == k)
        rungs = []
        up = node["ladder"]["up"]
        if isinstance(up, str):
            slug_up = up[3:] if up.startswith("l0:") else up
            lab = label_for.get(slug_up, plab.get(up, slug_up.split("proposed:")[-1].replace("-", " ")))
            lv = "class" if k == "turing-enigma-hodges" else "generic"
            rungs.append({"lab": lab, "lv": lv, "node": slug_up})
        rungs.append({"lab": node["label"], "lv": node["level"], "node": k})
        for d in node["ladder"]["downs"]:
            slug_d = d[3:] if d.startswith("l0:") else d
            lab = label_for.get(slug_d, plab.get(d, slug_d.split("proposed:")[-1].replace("-", " ")))
            rungs.append({"lab": lab, "lv": "instance", "node": slug_d})
        fam = {"key": k, "title": titles.get(k, node["kind"]), "rungs": rungs}
        if node["ladder"].get("scope"):
            fam["scoped"] = True
        LADDERS.append(fam)

    return W, EDGES, CANDS, PLAB, LADDERS


def _jsval(obj):
    """JSON for inline <script> embedding: escape non-ASCII to \\uXXXX and neutralize </
    (mirrors _reembed_agnostic.js). Produces valid JS literals (quoted keys are fine)."""
    s = json.dumps(obj, ensure_ascii=True)
    s = s.replace("</", "<\\/")
    return s


TOY_BEGIN = "/* GENERATED L0 DATA (do not hand-edit — l0_compile_wrappers.py) */"
TOY_END = "/* END GENERATED L0 DATA */"


def splice_toy(subjects, catalog):
    W, EDGES, CANDS, PLAB, LADDERS = build_toy_data(subjects, catalog)
    block = []
    block.append(TOY_BEGIN)
    block.append("/* W / EDGES / CANDS / PLAB / LADDERS are regenerated from the compiled")
    block.append("   substrate (compiled/l0-catalog.compiled.json) by l0_compile_wrappers.py.")
    block.append("   Per-fact membrane segments (bucket, certainty, predicate, value-snippet,")
    block.append("   fact_id, source note), the solid fact-backed EDGES, retired/inverse edges")
    block.append("   (CANDS), ladder links, frame weights and lifecycle events all come from the")
    block.append("   substrate. Node positions / proposed-node labels / ladder titles are")
    block.append("   display-only layout config (not substrate). Re-run the builder to refresh. */")
    block.append("var W=" + _jsval(W) + ";")
    block.append("/* fact-backed solid edges (natural direction; unverifiable/retired edges are NOT here) */")
    block.append("var EDGES=" + _jsval(EDGES) + ";")
    block.append("/* retired/inverse edges (bucket=unverifiable) — ghosts only, never solid */")
    block.append("var CANDS=" + _jsval(CANDS) + ";")
    block.append("/* display labels for proposed: frontier nodes */")
    block.append("var PLAB=" + _jsval(PLAB) + ";")
    block.append("/* ladder families (top = generic, bottom = specific) */")
    block.append("var LADDERS=" + _jsval(LADDERS) + ";")
    block.append(TOY_END)
    new_block = "\n".join(block)

    html = TOY.read_text(encoding="utf-8")

    if TOY_BEGIN in html and TOY_END in html:
        pre = html[:html.index(TOY_BEGIN)]
        post = html[html.index(TOY_END) + len(TOY_END):]
        html2 = pre + new_block + post
    else:
        # First splice: replace the original hand data region (from the embedded-data
        # comment through the end of the LADDERS array) with the generated block.
        m_start = re.search(r"/\* -+ embedded data:", html)
        if not m_start:
            m_start = re.search(r"\nvar W\s*=\s*\[", html)
            start = m_start.start() + 1
        else:
            start = m_start.start()
        m_end = re.search(r"/\* -+ proxy \+ helpers -+ \*/", html)
        if not m_end:
            raise SystemExit("toy splice: could not locate end-of-data anchor ('proxy + helpers')")
        end = m_end.start()
        html2 = html[:start] + new_block + "\n\n" + html[end:]

    TOY.write_text(html2, encoding="utf-8")
    return len(W), len(EDGES), len(CANDS), len(LADDERS)


def extract_toy_script():
    """Extract the FIRST <script> body to %TEMP% for `node --check` (never load the whole
    html into the model context; operate on the file directly)."""
    html = TOY.read_text(encoding="utf-8")
    i = html.find("<script>")
    j = html.find("</script>", i)
    body = html[i + len("<script>"):j]
    import tempfile
    out = Path(tempfile.gettempdir()) / "l0_toy_extracted.js"
    out.write_text(body, encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Group configs (spec §4)
# ---------------------------------------------------------------------------
def write_group_configs():
    GROUPS_DIR.mkdir(parents=True, exist_ok=True)
    configs = {
        "grp-six-sample-constellation": {
            "_doc": ("GENERATED by " + COMPILER_STAMP + ". Saved group-frame render config "
                     "(spec §4). The full interconnection web of the six sweep-1 samples + the "
                     "proposed: frontier as depth-1 ghosts. Display/observer config, not substrate."),
            "config_id": "grp-six-sample-constellation",
            "title": "Six-sample constellation — the full L0 web",
            "wrappers": ["l0:" + s for s in SAMPLE_SLUGS],
            "observer": {"kernel": ["time", "space", "knowledge", "meaning"],
                         "frame_layer": "straddle", "scope": "global"},
            "lod": {"depth": 1, "membrane_detail": "kernel+membrane", "abstraction_dial": {}},
            "layout": "constellation",
            "edges": "all",
            "options": {"frontier": True, "candidate_edges": False},
            "provenance_chips": True,
        },
        "grp-turing-lineage-timeline": {
            "_doc": ("GENERATED by " + COMPILER_STAMP + ". Saved group-frame render config "
                     "(spec §4). One lineage spine person -> book -> ai-model -> device on a "
                     "shared time axis (~1912 to now). Display/observer config, not substrate."),
            "config_id": "grp-turing-lineage-timeline",
            "title": "Turing lineage timeline",
            "wrappers": ["l0:alan-turing", "l0:turing-enigma-hodges", "l0:claude", "l0:iphone-15-pro"],
            "observer": {"kernel": ["time", "knowledge", "meaning"],
                         "frame_layer": "straddle", "scope": "global"},
            "lod": {"depth": 0, "membrane_detail": "kernel+membrane", "abstraction_dial": {}},
            "layout": "timeline",
            "edges": "fact-backed-only",
            "options": {"lam": 0.45, "fisheye": False},
            "provenance_chips": True,
        },
        "grp-two-ladders": {
            "_doc": ("GENERATED by " + COMPILER_STAMP + ". Saved group-frame render config "
                     "(spec §4). The contextual-scale abstraction dial in TWO kinds at once, with "
                     "the genericide scope toggle (global / US / DE-CA) live. Not substrate."),
            "config_id": "grp-two-ladders",
            "title": "Two ladders — the contextual-scale dial across kinds",
            "wrappers": ["l0:smartphone", "l0:iphone-15-pro", "l0:acetylsalicylic-acid"],
            "observer": {"kernel": ["space", "knowledge"],
                         "frame_layer": "straddle", "scope": "global"},
            "lod": {"depth": 0, "membrane_detail": "kernel+membrane",
                    "abstraction_dial": {"smartphone": "generic",
                                         "iphone-15-pro": "instance",
                                         "acetylsalicylic-acid": "generic"}},
            "layout": "abstraction-ladder",
            "edges": ["instance-of", "subclass-of", "brand-of"],
            "options": {"scope_toggle": ["global", "us", "de"]},
            "provenance_chips": True,
        },
    }
    written = []
    for cid, cfg in configs.items():
        path = GROUPS_DIR / (cid + ".json")
        path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path.name)
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Compile L0 wrapper views from the substrate.")
    ap.add_argument("--check", action="store_true",
                    help="semantic diff of compiled output vs wrappers/<slug>.json (default)")
    ap.add_argument("--write", action="store_true",
                    help="regenerate wrappers + toy data block + group_configs")
    ap.add_argument("--substrate", default=str(DEFAULT_SUBSTRATE),
                    help="path to l0-catalog.compiled.json (default: repo-relative)")
    ap.add_argument("--no-toy", action="store_true", help="with --write, skip the toy splice")
    ap.add_argument("--no-groups", action="store_true", help="with --write, skip group_configs")
    args = ap.parse_args()

    generated = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    _, subjects = load_compiled(args.substrate)
    catalog = set(SAMPLE_SLUGS)

    missing = [s for s in SAMPLE_SLUGS if s not in subjects]
    if missing:
        print("ERROR: compiled view is missing sample subject(s): %s" % ", ".join(missing),
              file=sys.stderr)
        return 2

    if args.write:
        written = write_wrappers(subjects, catalog, generated)
        print("wrote %d wrapper view(s): %s" % (len(written), ", ".join(written)))
        if not args.no_toy:
            nW, nE, nC, nL = splice_toy(subjects, catalog)
            print("spliced toy GENERATED data block: W=%d EDGES=%d CANDS=%d LADDERS=%d"
                  % (nW, nE, nC, nL))
        if not args.no_groups:
            gw = write_group_configs()
            print("emitted %d group config(s): %s" % (len(gw), ", ".join(gw)))
        return 0

    # default: --check
    total = check(subjects, catalog, generated)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
