#!/usr/bin/env python3
"""
Fold the dig strata BACK INTO the seed node's conjecture-fan (Pav: "adding layers to the original seed ... the
substrate node permanently carries its own excavated depth"). Each excavated contributor becomes a depth-tagged
candidate in the WHO conjecture-fan, with elicitation_method provenance (spec sec8.1: a forced-divergence /
under-the-rocks take is provenance, NOT a held best guess) and the layer-depth at which it surfaced. The canonical
surface (L0) renders sharp; deeper strata render progressively blurrier (the geology column = the iceberg).

Reads substrate_dig.json (+ substrate_dig_current.json if present) -> enriched_substrate.json.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

ELICIT = {0: "canonical (spontaneous mode)", 1: "forbid-canonical (under-the-rocks)",
          2: "forbid canonical+L1 (deeper dig)", 3: "forbid canonical+L1+L2 (deepest dig)"}


def enrich(dig_path):
    if not (HERE / dig_path).exists(): return []
    dig = json.loads((HERE / dig_path).read_text(encoding="utf-8"))
    out = []
    for node in dig:
        fan = []
        depth_curve = []
        floor_layer = None
        for L in node["layers"]:
            ents = L.get("entities", L.get("new_entities", []))
            depth_curve.append(len(ents))
            ex = L.get("exhausted_count", 0)
            if ex and floor_layer is None: floor_layer = L["layer"]
            for e in ents:
                fan.append({"reading": e, "surfaced_at_layer": L["layer"],
                            "elicitation": ELICIT.get(L["layer"], f"L{L['layer']}"),
                            # COIN: deeper strata are blurrier -- sharpness decays with dig depth
                            "render_sharpness": round(max(0.05, 1.0 - 0.28 * L["layer"]), 2),
                            "tag": "measured" if L["layer"] == 0 else "conjectured (forced-elicitation)"})
        out.append({
            "artefact": node["artefact"], "title": node["title"],
            "canon_surface": [f["reading"] for f in fan if f["surfaced_at_layer"] == 0][:30],
            "excavated_fan": fan,                       # the seed's WHO conjecture-fan, depth-tagged
            "depth_curve": depth_curve,                 # entities per layer L0..Ln
            "floor_first_exhausted_at_layer": floor_layer,
            "total_strata": len(node["layers"]),
            "fan_size": len(fan),
        })
    return out


def main():
    enriched = enrich("substrate_dig.json") + enrich("substrate_dig_current.json")
    (HERE / "enriched_substrate.json").write_text(json.dumps(enriched, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote enriched_substrate.json: {len(enriched)} seed nodes, each carrying its excavated depth")
    for n in enriched:
        print(f"  {n['artefact']:>3} {n['title'][:30]:<30} fan={n['fan_size']:>4} depth_curve={n['depth_curve']}  floor@L{n['floor_first_exhausted_at_layer']}")


if __name__ == "__main__":
    main()
