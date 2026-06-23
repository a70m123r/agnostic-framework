#!/usr/bin/env python3
"""
Fold BOTH digs into the seed as one bidirectional stratigraphic column -- Pav's "L -0+":
  L-3..L-1  = the PAST dig (backward cone: WHO/lineage forbidden-cascade) -> bedrock = the FOUNDING MYTH.
  L0        = the SEED / the bridge (the canonical present -- the organ of the genesis->eschaton movement).
  L+1..L+3  = the FUTURE dig (forward cone: consensus-future forbidden-cascade) -> bedrock = the ESCHATON.
Render asymmetry (spec sec9): the past is mostly-measurable (blurs slower); the future is entirely conjecture
(corrob_bits=0, blurs faster). render_sharpness decays with |depth|, steeper on the + side.

Reads substrate_dig.json (historical past) + substrate_dig_current.json (current past) +
substrate_dig_forward.json (current future) -> enriched_substrate.json (the L-0+ columns).
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

PAST_LABEL = {0: "canonical present (the bridge / L0)", 1: "overlooked (forbid canonical)",
              2: "deeper past dig", 3: "founding-myth bedrock"}
FWD_LABEL = {1: "dark-horse future (forbid consensus)", 2: "deeper future dig", 3: "eschaton / deep-future bedrock"}


def load(name):
    p = HERE / name
    return {n["artefact"]: n for n in json.loads(p.read_text(encoding="utf-8"))} if p.exists() else {}


def sharp(depth):
    # past (depth<=0): rate .28 ; future (depth>0): rate .33 (steeper -- entirely unmeasured)
    rate = 0.33 if depth > 0 else 0.28
    return round(max(0.05, 1.0 - rate * abs(depth)), 2)


def token_stats(records):
    """the digestion cost of this dig layer: how hard the models had to think to surface it."""
    if not records: return None
    rts = [r["reasoning_tokens"] for r in records if r.get("reasoning_tokens")]
    produced = sum(1 for r in records if (r.get("who") or r.get("future") or r.get("parse_ok")))
    return {"n_models": len(records), "n_produced": produced, "n_thinking": len(rts),
            "think_sum": sum(rts), "think_med": (sorted(rts)[len(rts) // 2] if rts else 0),
            "think_max": (max(rts) if rts else 0)}


def main():
    past = {**load("substrate_dig.json"), **load("substrate_dig_current.json")}
    fwd = load("substrate_dig_forward.json")
    arts = list(past.keys())
    for a in fwd:
        if a not in arts: arts.append(a)
    out = []
    for a in arts:
        pnode = past.get(a, {}); fnode = fwd.get(a, {})
        title = pnode.get("title") or fnode.get("title") or a
        column = []
        # PAST side: backward-dig layer L -> depth -L (L0 stays 0 = the seed/bridge)
        for L in (pnode.get("layers") or []):
            items = L.get("entities", L.get("new_entities", []))
            depth = -L["layer"]
            column.append({"depth": depth, "side": "seed" if depth == 0 else "past",
                           "stratum": PAST_LABEL.get(L["layer"], f"L-{L['layer']}"),
                           "render_sharpness": sharp(depth),
                           "kind": "measured" if depth == 0 else "conjecture (forced-dig, elicitation=under-the-rocks)",
                           "n_items": len(items), "items": items[:40],
                           "exhausted_count": L.get("exhausted_count"), "stats": token_stats(L.get("records"))})
        # FUTURE side: forward-dig layer L (1..3) -> depth +L.
        # use the FULL future text from the per-model records (the new_futures list was truncated at extraction).
        for L in (fnode.get("layers") or []):
            if L["layer"] == 0: continue  # the consensus-future == the seed's forward edge
            seen = set(); futs = []
            for r in (L.get("records") or []):
                f = (r.get("future") or "").strip()
                if not f or f.upper().startswith("EXHAUST"): continue
                k = f[:28].lower()
                if k not in seen: seen.add(k); futs.append(f)
            if not futs: futs = L.get("new_futures", [])  # fallback
            depth = +L["layer"]
            column.append({"depth": depth, "side": "future", "stratum": FWD_LABEL.get(L["layer"], f"L+{L['layer']}"),
                           "render_sharpness": sharp(depth),
                           "kind": "conjecture (corrob_bits=0; the future is unmeasured)",
                           "n_items": len(futs), "items": futs[:40],
                           "exhausted_count": L.get("exhausted_count"), "stats": token_stats(L.get("records"))})
        column.sort(key=lambda c: c["depth"])
        out.append({"artefact": a, "title": title,
                    "bridge_note": "L0 = the measurable present -- the organ through which the genesis-myth becomes the eschaton-myth",
                    "span": [column[0]["depth"], column[-1]["depth"]] if column else [0, 0],
                    "two_sided": any(c["depth"] > 0 for c in column) and any(c["depth"] < 0 for c in column),
                    "column": column})
    (HERE / "enriched_substrate.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote enriched_substrate.json: {len(out)} seed nodes (L-0+ columns)")
    for n in out:
        cells = "  ".join(f"L{c['depth']:+d}:{c['n_items']}" for c in n["column"])
        print(f"  {n['artefact']:>3} {n['title'][:26]:<26} [{'two-sided' if n['two_sided'] else 'past-only '}] {cells}")


if __name__ == "__main__":
    main()
