#!/usr/bin/env python3
"""build_scene.py - assemble the Fable-takedown SCENE from the compiled substrate + projections.

Reads:
  ../specimens/fable_takedown.json                    cast skeleton (nodes, roles, depth, acts_on graph)
  ../substrate/compiled/fable-takedown.compiled.json  measured facts (value, bucket, certainty, source)
  ../substrate/facts/fable_takedown.*.jsonl           raw facts (for the per-fact route, kept in notes)
  fable_takedown.projections.json                     the 3 short/medium/long guesses (CONJECTURE)

Writes:
  fable_takedown.scene.json                           the scene the viewer/narrator render

The narrator is SUBSTRATE-BOUND: every narration line derives from a specific fact_id and
carries that fact's certainty + route. Projections are narrated separately, marked PROJECTION.
NO fabrication: the narrator only ever speaks what the substrate (or a marked projection) holds.
Broad-strokes v0 - sharpen the fuzzy_regions with targeted scouts (the refine phase).

Stdlib only. Deterministic: stable sort, no clock, no randomness.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECIMEN = HERE.parent / "specimens" / "fable_takedown.json"
COMPILED = HERE.parent / "substrate" / "compiled" / "fable-takedown.compiled.json"
FACTS = [
    HERE.parent / "substrate" / "facts" / "fable_takedown.entities.jsonl",
    HERE.parent / "substrate" / "facts" / "fable_takedown.events.jsonl",
]
PROJECTIONS = HERE / "fable_takedown.projections.json"
OUT = HERE / "fable_takedown.scene.json"

ROUTE_RE = re.compile(r"route=([a-z][a-z\-]*(?:\s*->\s*[a-z][a-z\-]*)?)")
FUZZY_THRESHOLD = 0.70  # facts below this are flagged for the refine phase

# Entailment class (post external-pass): every scene element declares HOW it is known, computed from
# its route. observed = directly reported; attributed = single-outlet/second-hand; inferred = deduced;
# search-status = a disclosed null / open question (not an event fact); seed = user-origin (now-corroborated).
# Projections are tagged 'projection' separately. This stops interpretation from riding for free inside
# a structure that was (over-)labelled 'measured'.
ENTAIL = {"measured-on-plane": "observed", "lateral-testimony": "attributed",
          "inferred-from-below": "inferred", "user-seed-origin": "seed"}

def entailment_of(route, predicate):
    if predicate in ("disclosed_null", "open_question"):
        return "search-status"
    if not route:
        return "unclassified"
    return ENTAIL.get(route.split("->")[0].strip(), "attributed")


def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def load_routes():
    """fact_id -> route string, parsed from each raw fact's notes."""
    routes = {}
    for fp in FACTS:
        for raw in fp.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line:
                continue
            obj = json.loads(line)
            m = ROUTE_RE.search(obj.get("notes", "") or "")
            routes[obj["fact_id"]] = m.group(1).strip() if m else None
    return routes


def beat_sort_key(entry):
    when = entry.get("when") or ""
    return (when[:10], entry.get("best_fact_id", ""))  # day, then emit order (cause before reaction)


def main():
    spec = load_json(SPECIMEN)
    comp = load_json(COMPILED)
    proj = load_json(PROJECTIONS)
    routes = load_routes()
    subjects = comp["subjects"]

    def route_for(entry):
        return routes.get(entry.get("best_fact_id"))

    # ---- cast: enrich each skeleton node with its compiled facts ----
    cast = []
    roles = {"actor": [], "acted_on": [], "stage": [], "audience": []}
    for node in spec["nodes"]:
        nid = node["id"]
        facts = subjects.get(nid, [])
        role_fact = next((f for f in facts if f["predicate"] == "role"), None)
        cast.append({
            "id": nid,
            "name": node["name"],
            "role": node["role"],
            "depth": node["depth"],
            "acts_on": node.get("acts_on", []),
            "gloss": node.get("gloss"),
            "headline_certainty": role_fact["certainty"] if role_fact else None,
            "headline_bucket": role_fact["bucket"] if role_fact else None,
            "n_facts": len(facts),
            "facts": [{
                "predicate": f["predicate"], "value": f["value"], "when": f.get("when"),
                "certainty": f["certainty"], "bucket": f["bucket"],
                "route": route_for(f), "entailment": entailment_of(route_for(f), f["predicate"]),
                "fact_id": f["best_fact_id"], "source_url": (f.get("source") or {}).get("url"),
            } for f in facts],
        })
        roles.setdefault(node["role"], []).append(nid)

    # ---- the 2-depth acts_on graph ----
    edges = [{"from": n["id"], "to": t} for n in spec["nodes"] for t in n.get("acts_on", [])]

    # ---- beats: the scrubable timeline (any dated fact in the EVENT namespace f-fbt-e*, or a BEAT-prefixed value) ----
    EVENT_RE = re.compile(r"f-fbt-e\d")
    beats = []
    for sid, facts in subjects.items():
        for f in facts:
            v = f.get("value")
            is_beat = (isinstance(v, str) and v.startswith("BEAT")) or EVENT_RE.search(f.get("best_fact_id", ""))
            if is_beat and f.get("when"):
                beats.append({
                    "when": f.get("when"), "subject": sid, "predicate": f["predicate"],
                    "text": f["value"], "certainty": f["certainty"], "bucket": f["bucket"],
                    "route": route_for(f), "entailment": entailment_of(route_for(f), f["predicate"]),
                    "best_fact_id": f["best_fact_id"],
                })
    beats.sort(key=beat_sort_key)

    # ---- fuzzy regions: low-certainty facts = the targets for the refine phase ----
    fuzzy = []
    for sid, facts in subjects.items():
        for f in facts:
            if isinstance(f.get("certainty"), (int, float)) and f["certainty"] < FUZZY_THRESHOLD:
                fuzzy.append({
                    "subject": sid, "predicate": f["predicate"], "certainty": f["certainty"],
                    "fact_id": f["best_fact_id"], "why": "single-source / second-hand / analytical",
                })
    fuzzy.sort(key=lambda x: x["certainty"])

    # ---- the narrator (substrate-bound): ordered lines, each carrying its fact's confidence + route ----
    narration = []
    seq = 0

    def say(kind, text, **meta):
        nonlocal seq
        seq += 1
        narration.append({"seq": seq, "kind": kind, "text": text, **meta})

    say("frame", "A three-day worldline. Claude Fable 5 and Mythos 5 launch on 2026-06-09 and are cut on 2026-06-12 "
        "at 17:21 ET - the first time a leading AI company takes a publicly deployed model offline under US federal "
        "intervention. What follows is told only from what the substrate holds; confidence and route travel with each line.",
        derived_from="f-fbt-e0007", certainty=0.98, route="measured-on-plane")

    for b in beats:
        raw = b["text"]
        text = raw.split(":", 1)[1].strip() if (raw.startswith("BEAT") and ":" in raw) else raw
        say("beat", text, when=b["when"], derived_from=b["best_fact_id"],
            certainty=b["certainty"], bucket=b["bucket"], route=b["route"], entailment=b["entailment"])

    say("frame", "The worldline ends OPEN, not closed: Anthropic says it is working to restore access, with no timeline. "
        "Everything past this point is projection - conjecture, not measurement; no measured bit is rendered forward.",
        derived_from="f-fbt-e0014", certainty=0.97, route="measured-on-plane")

    for p in proj["projections"]:
        say("projection", p["modal_guess"], horizon=p["horizon"], window=p["window"],
            conjecture_child=p["conjecture_child"], likelihood_band=p["likelihood_band"],
            falsifier=p["falsifier"], marked=p["marked"])

    # ---- assemble ----
    scene = {
        "_doc": "Fable-takedown SCENE - v0.2 (post external-pass). An INTERPRETIVE scene built OVER the measured "
                "substrate - NOT 'derived = measured'. The role-typing (actor/acted_on/stage/audience), the depth-cut, "
                "and the acts_on graph are INTERPRETIVE choices; only the underlying facts (value/certainty/route) are "
                "measured. Every cast fact and beat carries an ENTAILMENT class (observed|attributed|inferred|"
                "search-status|seed) computed from its route; projections are 'projection' and live outside the "
                "substrate with quantized falsifiers. The narrator is substrate-bound. Generated by build_scene.py; "
                "edit the substrate facts or projections and re-run. Sharpen fuzzy_regions with targeted scouts.",
        "epistemics": {
            "status": "interpretive scene over a measured substrate (the substrate is the evidence log; the scene STRUCTURE is interpretation)",
            "entailment_legend": {"observed": "directly reported (route measured-on-plane)",
                                  "attributed": "single-outlet / second-hand (route lateral-testimony)",
                                  "inferred": "deduced from absence/indirect (route inferred-from-below)",
                                  "search-status": "a disclosed null / open question - NOT an event fact, only 'not found by timestamp'",
                                  "seed": "user-origin, now independently corroborated (route user-seed-origin)",
                                  "projection": "conjecture, outside the substrate, with a quantized falsifier"},
            "certainty_note": "certainty is a DISCLOSED-SUBJECTIVE confidence per the harvest rubric, NOT a measured probability; cross-source independence is tracked via the verification BUCKET (corroborated/pending), not by inflating the number.",
            "disputed_note": "the 'disputed' bucket counts fact-VALUE contradictions (0 here); the event's RATIONALE is nonetheless contested - recorded as facts (Anthropic disputes; statute undisclosed), not hidden by the 0.",
            "external_pass": "external_pass/SYNTHESIS.md - this scene is v0.2 after codex+gemini demoted the 'derived=measured' over-claim (dead child) to this interpretive-layer framing (sharpened parent)."
        },
        "specimen": "fable-takedown",
        "title": spec["title"],
        "t0": spec["t0"],
        "terminus": spec["terminus"],
        "generated_from": {"compiled": comp.get("generated"), "projections_t0": proj.get("t0")},
        "stats": {
            "cast": len(cast),
            "by_role": {r: len(ids) for r, ids in roles.items()},
            "edges": len(edges),
            "beats": len(beats),
            "corroborated_facts": sum(1 for s in subjects.values() for f in s if f["bucket"] == "corroborated"),
            "fuzzy_regions": len(fuzzy),
            "projections": len(proj["projections"]),
        },
        "cast": cast,
        "graph_2depth": edges,
        "stage": roles.get("stage", []),
        "audience": roles.get("audience", []),
        "beats": beats,
        "projections": proj["projections"],
        "fuzzy_regions": fuzzy,
        "narration": narration,
    }
    OUT.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"scene written: {OUT.name}")
    print(f"  cast={scene['stats']['cast']}  by_role={scene['stats']['by_role']}")
    print(f"  edges={scene['stats']['edges']}  beats={scene['stats']['beats']}  "
          f"corroborated={scene['stats']['corroborated_facts']}  fuzzy={scene['stats']['fuzzy_regions']}  "
          f"projections={scene['stats']['projections']}")
    print(f"  narration lines={len(narration)}")


if __name__ == "__main__":
    main()
