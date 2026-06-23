#!/usr/bin/env python3
"""
Compile the dig substrate into the L-0+ stratigraphic columns (enriched_substrate.json) -- pulling FULL text
straight from the per-model SOURCE records (not the pre-truncated entity summaries), so nothing clips.

L-3..L-1 = past dig (founding-myth bedrock at L-3) · L0 = seed/bridge · L+1..L+3 = future dig (eschaton at L+3).
items per stratum = the full leading who/future each model surfaced (deduped) + (for run-file strata) the full
conjecture-fan readings. n_items keeps the rich count for the depth curve. stats = the reasoning-token cost.

Sources:
  L0   <- broad_run (A*) / current_run (C*)                       [full who + conjectures + parents]
  L-1  <- forbid_run (A*) / dig_current layer1 records (C*)
  L-2..L-3 <- substrate_dig{,_current}.json layer records        [full leading who]
  L+1..L+3 <- substrate_dig_forward.json layer records           [full future]
"""
import json
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
PAST_LABEL = {0: "canonical present (the bridge / L0)", 1: "overlooked (forbid canonical)",
              2: "deeper past dig", 3: "founding-myth bedrock"}
FWD_LABEL = {1: "dark-horse future (forbid consensus)", 2: "deeper future dig", 3: "eschaton / deep-future bedrock"}


def sharp(depth):
    return round(max(0.05, 1.0 - (0.33 if depth > 0 else 0.28) * abs(depth)), 2)


def jl(name):
    p = HERE / name; out = defaultdict(list)
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                if r.get("parse_ok"): out[r["event"]].append(r)
    return out


def digfile(name):
    p = HERE / name
    return {n["artefact"]: n for n in json.loads(p.read_text(encoding="utf-8"))} if p.exists() else {}


def run_items(records):
    """full who.value + who.conjectures[].reading + lineage.parents[].name from RUN records (rich + untruncated)."""
    out, seen = [], set()
    def add(s):
        s = (s or "").strip()
        if s and s.lower()[:30] not in seen and s.upper() not in ("EXHAUSTED", "UNKNOWN"):
            seen.add(s.lower()[:30]); out.append(s)
    for r in records:
        rec = r.get("record") if isinstance(r.get("record"), dict) else {}
        who = rec.get("who") if isinstance(rec.get("who"), dict) else {}
        add(who.get("value"))
        for c in (who.get("conjectures") or []):
            if isinstance(c, dict): add(c.get("reading"))
        for p in ((rec.get("lineage") or {}).get("parents") or []):
            if isinstance(p, dict): add(p.get("name"))
    return out


def lead_items(records, key):
    """full leading who/future per model from DIG records (untruncated)."""
    out, seen = [], set()
    for r in records:
        s = (r.get(key) or "").strip()
        if s and not s.upper().startswith("EXHAUST") and s.lower()[:30] not in seen:
            seen.add(s.lower()[:30]); out.append(s)
    return out


def tstats(records):
    if not records: return None
    rts = [r["reasoning_tokens"] for r in records if r.get("reasoning_tokens")]
    return {"n_models": len(records), "n_produced": sum(1 for r in records if (r.get("who") or r.get("future") or r.get("parse_ok"))),
            "n_thinking": len(rts), "think_sum": sum(rts), "think_med": (sorted(rts)[len(rts) // 2] if rts else 0),
            "think_max": (max(rts) if rts else 0)}


def main():
    BROAD, CUR, FORBID = jl("substrate_probe_broad_run.jsonl"), jl("substrate_probe_current_run.jsonl"), jl("substrate_probe_forbid_run.jsonl")
    PASTH, PASTC, FWD = digfile("substrate_dig.json"), digfile("substrate_dig_current.json"), digfile("substrate_dig_forward.json")
    past = {**PASTH, **PASTC}
    arts = list(past.keys()) + [a for a in FWD if a not in past]
    out = []
    for a in arts:
        pnode, fnode = past.get(a, {}), FWD.get(a, {})
        title = pnode.get("title") or fnode.get("title") or a
        is_current = a in PASTC
        col = []
        for L in (pnode.get("layers") or []):
            depth = -L["layer"]; recs = L.get("records") or []
            if depth == 0:
                items = run_items((CUR if is_current else BROAD).get(a, []))
            elif depth == -1 and not recs:                       # historical L-1 = the forbid run
                items = run_items(FORBID.get(a, []))
            else:
                items = lead_items(recs, "who") or L.get("entities", L.get("new_entities", []))
            n_full = len(L.get("entities", L.get("new_entities", []))) or len(items)
            col.append({"depth": depth, "side": "seed" if depth == 0 else "past",
                        "stratum": PAST_LABEL.get(L["layer"], f"L-{L['layer']}"), "render_sharpness": sharp(depth),
                        "kind": "measured" if depth == 0 else "conjecture (forced-dig)",
                        "n_items": n_full, "items": items[:40], "exhausted_count": L.get("exhausted_count"),
                        "stats": tstats(recs)})
        for L in (fnode.get("layers") or []):
            if L["layer"] == 0: continue
            recs = L.get("records") or []
            items = lead_items(recs, "future") or L.get("new_futures", [])
            depth = +L["layer"]
            col.append({"depth": depth, "side": "future", "stratum": FWD_LABEL.get(L["layer"], f"L+{L['layer']}"),
                        "render_sharpness": sharp(depth), "kind": "conjecture (corrob_bits=0; the future is unmeasured)",
                        "n_items": len(L.get("new_futures", items)), "items": items[:40],
                        "exhausted_count": L.get("exhausted_count"), "stats": tstats(recs)})
        col.sort(key=lambda c: c["depth"])
        out.append({"artefact": a, "title": title,
                    "bridge_note": "L0 = the measurable present -- the organ through which the genesis-myth becomes the eschaton-myth",
                    "span": [col[0]["depth"], col[-1]["depth"]] if col else [0, 0],
                    "two_sided": any(c["depth"] > 0 for c in col) and any(c["depth"] < 0 for c in col), "column": col})
    (HERE / "enriched_substrate.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote enriched_substrate.json: {len(out)} L-0+ columns (full text from source records)")
    for n in out:
        print(f"  {n['artefact']:>3} {n['title'][:26]:<26} " + "  ".join(f"L{c['depth']:+d}:{len(c['items'])}/{c['n_items']}" for c in n["column"]))


if __name__ == "__main__":
    main()
