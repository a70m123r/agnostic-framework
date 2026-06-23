#!/usr/bin/env python3
"""
Compile the dig substrate into the L-0+ stratigraphic columns (enriched_substrate.json), pulling FULL text from
the per-model SOURCE records. Each item carries its PROVENANCE: {reading, model, origin}. Each stratum carries
t_obs (the synthesis time = the source run's file timestamp -- the spec's second timeline).

L-3..L-1 past dig (founding-myth bedrock at L-3) · L0 seed/bridge · L+1..L+3 future dig (eschaton at L+3).
"""
import json, datetime
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
PAST_LABEL = {0: "canonical present (the bridge / L0)", 1: "overlooked (forbid canonical)",
              2: "deeper past dig", 3: "founding-myth bedrock"}
FWD_LABEL = {1: "dark-horse future (forbid consensus)", 2: "deeper future dig", 3: "eschaton / deep-future bedrock"}


def sharp(depth): return round(max(0.05, 1.0 - (0.33 if depth > 0 else 0.28) * abs(depth)), 2)
def mtime(name):
    p = HERE / name
    return datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(sep=" ", timespec="minutes") if p.exists() else None


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
    """full who.value + conjecture readings + parent names from RUN records, each tagged with its model."""
    out, seen = [], set()
    for r in records:
        m, o = r.get("model"), r.get("origin")
        rec = r.get("record") if isinstance(r.get("record"), dict) else {}
        who = rec.get("who") if isinstance(rec.get("who"), dict) else {}
        cands = [who.get("value")] + [c.get("reading") for c in (who.get("conjectures") or []) if isinstance(c, dict)] \
                + [p.get("name") for p in ((rec.get("lineage") or {}).get("parents") or []) if isinstance(p, dict)]
        for s in cands:
            s = (s or "").strip()
            if s and s.upper() not in ("EXHAUSTED", "UNKNOWN") and (s.lower()[:40], m) not in seen:
                seen.add((s.lower()[:40], m)); out.append({"reading": s, "model": m, "origin": o})
    return out


def lead_items(records, key):
    """full leading who/future per model from DIG records; futures also carry the wildcard scenario."""
    out = []
    for r in records:
        m, o = r.get("model"), r.get("origin")
        s = (r.get(key) or "").strip()
        if s and not s.upper().startswith("EXHAUST"):
            out.append({"reading": s, "model": m, "origin": o})
        if key == "future":
            wc = r.get("wildcard")
            if isinstance(wc, dict) and wc.get("scenario"):
                out.append({"reading": "wildcard (p=%s): %s" % (wc.get("plausibility"), wc["scenario"]),
                            "model": m, "origin": o, "wildcard": True})
    return out


def tstats(records):
    if not records: return None
    rts = [r["reasoning_tokens"] for r in records if r.get("reasoning_tokens")]
    return {"n_models": len(records), "n_produced": sum(1 for r in records if (r.get("who") or r.get("future") or r.get("parse_ok"))),
            "n_thinking": len(rts), "think_sum": sum(rts), "think_med": (sorted(rts)[len(rts) // 2] if rts else 0)}


def main():
    BROAD, CUR, FORBID = jl("substrate_probe_broad_run.jsonl"), jl("substrate_probe_current_run.jsonl"), jl("substrate_probe_forbid_run.jsonl")
    PASTH, PASTC, FWD = digfile("substrate_dig.json"), digfile("substrate_dig_current.json"), digfile("substrate_dig_forward.json")
    T = {"broad": mtime("substrate_probe_broad_run.jsonl"), "cur": mtime("substrate_probe_current_run.jsonl"),
         "forbid": mtime("substrate_probe_forbid_run.jsonl"), "digh": mtime("substrate_dig.json"),
         "digc": mtime("substrate_dig_current.json"), "fwd": mtime("substrate_dig_forward.json")}
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
                items = run_items((CUR if is_current else BROAD).get(a, [])); t_obs = T["cur"] if is_current else T["broad"]
            elif depth == -1 and not recs:
                items = run_items(FORBID.get(a, [])); t_obs = T["forbid"]
            else:
                items = lead_items(recs, "who"); t_obs = T["digc"] if is_current else T["digh"]
            n_full = len(L.get("entities", L.get("new_entities", []))) or len(items)
            col.append({"depth": depth, "side": "seed" if depth == 0 else "past",
                        "stratum": PAST_LABEL.get(L["layer"], f"L-{L['layer']}"), "render_sharpness": sharp(depth),
                        "kind": "measured" if depth == 0 else "conjecture (forced-dig)", "t_obs": t_obs,
                        "n_items": n_full, "items": items[:60], "exhausted_count": L.get("exhausted_count"), "stats": tstats(recs)})
        for L in (fnode.get("layers") or []):
            if L["layer"] == 0: continue
            recs = L.get("records") or []
            col.append({"depth": +L["layer"], "side": "future", "stratum": FWD_LABEL.get(L["layer"], f"L+{L['layer']}"),
                        "render_sharpness": sharp(+L["layer"]), "kind": "conjecture (corrob_bits=0; the future is unmeasured)",
                        "t_obs": T["fwd"], "n_items": len(L.get("new_futures", [])), "items": lead_items(recs, "future")[:60],
                        "exhausted_count": L.get("exhausted_count"), "stats": tstats(recs)})
        col.sort(key=lambda c: c["depth"])
        out.append({"artefact": a, "title": title,
                    "bridge_note": "L0 = the measurable present -- the organ through which the genesis-myth becomes the eschaton-myth",
                    "span": [col[0]["depth"], col[-1]["depth"]] if col else [0, 0],
                    "two_sided": any(c["depth"] > 0 for c in col) and any(c["depth"] < 0 for c in col), "column": col})
    (HERE / "enriched_substrate.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote enriched_substrate.json: {len(out)} L-0+ columns (full text + {{model,origin}} provenance + t_obs)")
    for n in out:
        print(f"  {n['artefact']:>3} {n['title'][:24]:<24} " + "  ".join(f"L{c['depth']:+d}:{len(c['items'])}" for c in n["column"]))


if __name__ == "__main__":
    main()
