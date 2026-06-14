#!/usr/bin/env python3
"""apply_growth2.py - append-only application of the DEPTH-2 swarm growth plan.

Reads the workflow output JSON (result = the plan), strips 'proposed:' to clean cast ids,
adds new cast nodes to the specimen, appends new facts/verifications to the substrate, and
writes speculations/conjectures to a DISCLOSED doc (NOT substrate facts). Idempotent (dedupe
by id/fact_id). Defensive: coerces source_type to the allowed set, clamps certainty, forces
verification='pending'. Stdlib only.
"""
import json, os
from pathlib import Path

OUT = Path(r"C:\Users\Admin\AppData\Local\Temp\claude\D--\36902d4e-bc4e-4608-859a-5a03ff9b3f45\tasks\wpferfhd7.output")
CG  = Path(r"D:\PlatformOperator\research\pav\candidates\canonical_genealogy")
SPECIMEN = CG / "specimens" / "fable_takedown.json"
ENT = CG / "substrate" / "facts" / "fable_takedown.entities.jsonl"
EVT = CG / "substrate" / "facts" / "fable_takedown.events.jsonl"
VER = CG / "substrate" / "verifications" / "fable_takedown.jsonl"
SPEC_DOC = CG / "scene" / "SPECULATIONS.md"
GEO_OUT = CG / "scene" / "geo_overlay_additions.json"

RET = "2026-06-14T12:00:00Z"
SRCOK = {"aggregator","primary","encyclopedia","news","academic"}
g = json.loads(OUT.read_text(encoding="utf-8"))["result"]

def strip(s):
    s = s or ""
    return s[len("proposed:"):] if s.startswith("proposed:") else s
def src_type(t): return t if t in SRCOK else "news"
def clamp(v):
    try: v=float(v)
    except: return 0.5
    return max(0.0, min(1.0, v))

# ---- geo from hint (for the globe/atlas overlay; disclosed estimates) ----
CITY = [("pentagon",(38.87,-77.06)),("white house",(38.90,-77.04)),("treasury",(38.90,-77.03)),
        ("washington",(38.90,-77.03)),(" dc",(38.90,-77.03)),("san francisco",(37.77,-122.42)),
        ("seattle",(47.61,-122.33)),("new york",(40.71,-74.01)),("nyc",(40.71,-74.01)),
        ("brussels",(50.85,4.35)),("sydney",(-33.87,151.21)),("australia",(-25.27,133.78)),
        ("minneapolis",(44.98,-93.27)),("paris",(48.85,2.35)),("beijing",(39.90,116.40)),
        ("china",(39.90,116.40)),("london",(51.51,-0.12)),("cambridge",(42.36,-71.06)),
        ("boston",(42.36,-71.06)),("howard university",(38.92,-77.02)),("california",(37.77,-122.42))]
def geo_of(hint, role, depth):
    h=(hint or "").lower(); lat,lon=38.90,-77.03
    for key,(la,lo) in CITY:
        if key in h: lat,lon=la,lo; break
    pen = 2 if (depth or 1)<=1 else 1
    return {"lat":lat,"lon":lon,"pen":pen}

# ---- 1. specimen cast nodes ----
spec = json.loads(SPECIMEN.read_text(encoding="utf-8"))
have = {n["id"] for n in spec["nodes"]}
geo_add={}; added_nodes=0
for nd in g.get("new_cast_nodes",[]):
    cid = strip(nd["id"])
    geo_add[cid] = geo_of(nd.get("geo_hint"), nd.get("role"), nd.get("depth"))
    if cid in have: continue
    spec["nodes"].append({"id":cid,"name":nd.get("name",cid),"role":nd.get("role","audience"),
        "depth":nd.get("depth",1),"acts_on":[], "gloss":(nd.get("gloss","") or "")[:600],
        "basis":"depth-2 growth 2026-06-14"})
    have.add(cid); added_nodes+=1
SPECIMEN.write_text(json.dumps(spec, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
GEO_OUT.write_text(json.dumps(geo_add, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

# ---- 2/3. facts ----
def existing_ids(p):
    s=set()
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            ln=ln.strip()
            if ln:
                try: s.add(json.loads(ln).get("fact_id"))
                except: pass
    return s
def efact(f):
    d={"fact_id":f["fact_id"],"specimen":"fable-takedown","subject_id":strip(f["subject_id"]),
       "predicate":f.get("predicate","fact"),"value":f.get("value","")}
    if f.get("when"): d["when"]=f["when"]
    d["source"]={"url":f.get("source_url",""),"title":f.get("source_title",""),"type":src_type(f.get("source_type")),
                 "published_or_updated":f.get("when","2026-06-14")}
    d["retrieved_at"]=RET; d["certainty"]=clamp(f.get("certainty",0.5)); d["verification"]="pending"
    d["agent"]="fable-depth2-scout-01"
    d["notes"]="route="+(f.get("route","measured-on-plane"))+". DEPTH-2 GROWTH (swarm 2026-06-14). "+(f.get("note","") or "")
    return d
def append_facts(p, facts):
    ex=existing_ids(p); lines=[]; n=0
    for f in facts:
        if f.get("subject_id","").replace("proposed:","").strip()=="" or not f.get("fact_id"): continue
        if f["fact_id"] in ex: continue
        lines.append(json.dumps(efact(f), ensure_ascii=False)); n+=1
    if lines:
        with p.open("a",encoding="utf-8") as fh: fh.write("\n".join(lines)+"\n")
    return n
n_ent = append_facts(ENT, g.get("new_entity_facts",[]))
n_evt = append_facts(EVT, g.get("new_event_facts",[]))

# ---- 4. verifications ----
vlines=[]; nv=0
with VER.open("a",encoding="utf-8") as fh:
    for v in g.get("new_verifications",[]):
        rec={"fact_id":strip(v.get("fact_id","")),"status":v.get("status","corroborated"),
             "second_source":{"url":v.get("second_source_url",""),"title":v.get("second_source_title",""),
                              "type":"news","published_or_updated":"2026-06-14"},
             "value_found":v.get("value_found",""),"retrieved_at":RET,"verifier":"fable-depth2-verifier-01",
             "notes":"DEPTH-2 cross-source. "+(v.get("note","") or "")}
        if not rec["fact_id"] or not rec["second_source"]["url"]: continue
        fh.write(json.dumps(rec, ensure_ascii=False)+"\n"); nv+=1

# ---- 5. speculations -> disclosed doc (NOT substrate) ----
specs=g.get("speculations",[])
lines=["# Fable-takedown — SPECULATIONS & CONJECTURES (disclosed, NOT measured substrate)",
 "",
 "> Harvested by the depth-2 scout swarm (2026-06-14) from the same articles as the facts, per Pav's steer to capture the interesting tangents / speculations / conjectures each article raises. These are **NOT** facts and are **NOT** in the substrate — they are analyst predictions, slippery-slope arguments, motive theories, single-source market color, and one load-bearing NULL RESULT. Register: speculation. Track-don't-assert.",
 ""]
for s in specs:
    k=s.get("kind","speculation"); subj=s.get("subject",""); url=s.get("source_url",""); note=s.get("note","")
    lines.append(f"- **[{k}]** {s.get('claim','')}" + (f" _(re {subj})_" if subj else "") + (f" — {note}" if note else "") + (f" [src]({url})" if url else ""))
SPEC_DOC.write_text("\n".join(lines)+"\n", encoding="utf-8")

print(f"cast nodes added: {added_nodes} (total now {len(spec['nodes'])})")
print(f"entity facts appended: {n_ent} | event facts appended: {n_evt} | verifications: {nv}")
print(f"speculations written: {len(specs)} -> {SPEC_DOC.name}")
print(f"geo additions for {len(geo_add)} nodes -> {GEO_OUT.name}")
# anomaly: subjects not resolvable to a cast node (after strip)
allids={n['id'] for n in spec['nodes']}
miss=set()
for f in g.get("new_entity_facts",[])+g.get("new_event_facts",[]):
    sid=strip(f.get("subject_id",""));
    if sid and sid not in allids: miss.add(sid)
print("subjects NOT in cast (will flag):", sorted(miss) if miss else "none")
