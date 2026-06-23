#!/usr/bin/env python3
"""
Compile the substrate_probe records into VIEWER DATA (the camera values), honestly per the COIN:
per artefact, per axis -> cross-origin AGREEMENT -> SHARPNESS (sharp where models converge + mark measured;
blurred fan where they diverge/conjecture). Plus: the conjecture-fans (with falsifiers/followups), the WHY
complementary-coverage by bloc, and a parsed WHEN worldline (t_event). Writes viewer_data.js (const SUBSTRATE=...).

Usage: python build_viewer_data.py [run_jsonl]   (default substrate_probe_run.jsonl; pass the broad file to rebuild)
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict, Counter

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE / "substrate_probe_run.jsonl")
AXES = ["who", "what", "where", "when"]
STOP = set("the a an of and or to in on for with by as is are was were that this its it their his her "
           "system using individual reusable characters type printing artefact technology substance object "
           "across whole history paper into onto press inked arranged reproduce text China".lower().split())


def cell(rec, axis):
    if not isinstance(rec, dict): return None
    c = rec.get(axis)
    if isinstance(c, dict): return c
    if c: return {"value": c}
    return None


def keyset(s):
    return frozenset(t for t in re.findall(r"[a-z0-9]+", (s or "").lower()) if t not in STOP and len(t) > 1)


def agreement(values):
    """largest Jaccard>=0.34 cluster size / N -> [0,1]. honest, simple cross-origin convergence metric."""
    ks = [keyset(v) for v in values if v]
    if not ks: return 0.0, None
    best_n, best_rep = 0, None
    for i, a in enumerate(ks):
        cluster = [values[j] for j, b in enumerate(ks)
                   if (len(a & b) / len(a | b) if (a | b) else 0) >= 0.34]
        if len(cluster) > best_n:
            best_n, best_rep = len(cluster), Counter(cluster).most_common(1)[0][0]
    return best_n / len(ks), best_rep


def years_in(text):
    ys = [int(y) for y in re.findall(r"\b(\d{3,4})\b", text or "") if 200 <= int(y) <= 2026]
    for m in re.finditer(r"(\d{1,2})(?:st|nd|rd|th)\s*c", (text or "").lower()):
        ys.append(int(m.group(1)) * 100 - 50)
    return ys


def build():
    recs = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = [r for r in recs if r.get("parse_ok")]
    by_ev = defaultdict(list)
    for r in ok: by_ev[r["event"]].append(r)

    artefacts = []
    for ev, rows in by_ev.items():
        title = rows[0].get("title", ev)
        node = {"id": ev, "title": title, "n": len(rows),
                "whom": sorted({r["model"] for r in rows}), "axes": {}, "all_years": []}
        for axis in AXES:
            vals, bloc_vals, measured, fan = [], defaultdict(list), 0, []
            for r in rows:
                c = cell(r["record"], axis)
                if not c: continue
                v = str(c.get("value", "")).strip()
                if v:
                    vals.append(v); bloc_vals[r["origin"]].append(v)
                if c.get("basis") == "measured": measured += 1
                for s in (c.get("conjectures") or []):
                    if isinstance(s, dict) and s.get("reading"):
                        fan.append({"reading": str(s.get("reading"))[:120], "weight": s.get("weight"),
                                    "tag": s.get("tag"), "bloc": r["origin"],
                                    "falsifier": str(s.get("falsifier", ""))[:160],
                                    "followup": str(s.get("followup", ""))[:160]})
                if axis == "when": node["all_years"] += years_in(v)
            agr, lead = agreement(vals)
            # dedupe fan by reading, keep highest weight
            seen = {}
            for f in fan:
                k = keyset(f["reading"])
                if k and (k not in seen or (f.get("weight") or 0) > (seen[k].get("weight") or 0)): seen[k] = f
            node["axes"][axis] = {
                "leading": lead, "agreement": round(agr, 3),
                "sharpness": round(agr * (0.4 + 0.6 * (measured / max(1, len(rows)))), 3),  # converge AND claim-measured
                "measured_frac": round(measured / max(1, len(rows)), 3),
                "perBloc": {b: [x for x, _ in Counter(v).most_common(3)] for b, v in bloc_vals.items()},
                "fan": sorted(seen.values(), key=lambda f: -(f.get("weight") or 0))[:6],
            }
        # WHY: delivered (measured edges) + aims by bloc (the complementary-coverage fan)
        delivered, aims_bloc = [], defaultdict(list)
        for r in rows:
            why = r["record"].get("why") if isinstance(r["record"].get("why"), dict) else {}
            for d in (why.get("delivered") or []):
                if isinstance(d, dict) and d.get("reading"): delivered.append(str(d["reading"])[:90])
            for a in (why.get("aims") or []):
                if isinstance(a, dict) and a.get("reading"): aims_bloc[r["origin"]].append(str(a["reading"])[:90])
        # complementarity: fraction of distinct aim-keys that appear in only ONE bloc
        aim_keys = defaultdict(set)
        for b, lst in aims_bloc.items():
            for a in lst: aim_keys[b] |= {tuple(sorted(keyset(a)))} if keyset(a) else set()
        allk = Counter()
        for b, ks in aim_keys.items():
            for k in ks: allk[k] += 1
        uniq = sum(1 for k, c in allk.items() if c == 1)
        node["why"] = {"delivered": [d for d, _ in Counter(delivered).most_common(5)],
                       "aims_by_bloc": {b: [a for a, _ in Counter(v).most_common(4)] for b, v in aims_bloc.items()},
                       "complementarity": round(uniq / max(1, len(allk)), 3)}
        ys = node.pop("all_years")
        node["when_span"] = {"start": min(ys) if ys else None, "end": max(ys) if ys else None,
                             "markers": sorted(set(ys))}
        artefacts.append(node)

    artefacts.sort(key=lambda a: a["id"])

    # merge the GROUNDED verdicts (the semantic grounding workflow) if present -> the real camera output
    gpath = HERE / "grounded_full.json"
    if gpath.exists():
        g = {v["id"]: v for v in json.loads(gpath.read_text(encoding="utf-8"))}
        for a in artefacts:
            gv = g.get(a["id"])
            if not gv: continue
            a["grounded"] = {
                "crediting": gv.get("home_civ_crediting", {}).get("verdict"),
                "crediting_detail": (gv.get("home_civ_crediting", {}).get("detail") or "")[:480],
                "spine_converges": gv.get("checkable_spine_converges"),
                "why_complementary": gv.get("why_complementary"),
                "ground_truth": (gv.get("ground_truth_origin") or "").replace("</ground_truth_origin>", "").replace("</invoke>", "").strip()[:340],
                "sharp_axes": gv.get("sharp_axes", []), "blurred_axes": gv.get("blurred_axes", []),
            }

    out = {"source": SRC.name, "n_records": len(recs), "n_parsed": len(ok), "artefacts": artefacts,
           "grounded": gpath.exists(),
           "blocs": {"CN": "#e0564b", "US": "#4b8fe0", "EU": "#56c08a"}}
    (HERE / "viewer_data.js").write_text("const SUBSTRATE = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n",
                                         encoding="utf-8")
    print(f"wrote viewer_data.js: {len(artefacts)} artefacts from {len(ok)}/{len(recs)} parsed records ({SRC.name})")
    for a in artefacts:
        sd = "  ".join(f"{ax}:{a['axes'][ax]['sharpness']:.2f}" for ax in AXES)
        print(f"  {a['id']:>3} {a['title'][:34]:<34} | {sd} | WHY-compl={a['why']['complementarity']:.2f} span={a['when_span']['start']}-{a['when_span']['end']}")


if __name__ == "__main__":
    build()
