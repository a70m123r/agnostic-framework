#!/usr/bin/env python3
"""Build the self-contained BITEMPORAL_3D.html from the compiled session-arc capture.
Wrappers (acts) sit at t_event on the base; each rises a thread to its render height at t_obs
(the data hitting the sensor) — the bitemporal block sharpening. X=time, Y=physical<->latent, Z=dial.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
comp = json.loads((HERE/"compiled"/"arc.compiled.json").read_text(encoding="utf-8"))
acts = comp["acts"]; arcs = comp["arcs"]

# physical <-> latent placement by act kind (0=physical/concrete .. 1=latent/conceptual)
PL = {"test":0.30,"commit":0.35,"artifact":0.40,"fix":0.42,"run":0.40,"tool":0.45,
      "demote":0.55,"external":0.60,"say":0.68,"decision":0.72,"concept":0.80,"steer":0.82}

def parse(s):
    if not s: return None
    s = s.strip().replace("Z","+00:00")
    dt = None
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", s)
        dt = datetime.fromisoformat(m.group(1)+"+00:00") if m else None
    if dt is not None and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

tevs = [parse(a.get("t_event")) for a in acts]
tobss = [parse(a.get("t_obs")) for a in acts]
allt = [t for t in tevs+tobss if t]
tmin = min(allt); tmax = max(allt)
span = max(1.0, (tmax-tmin).total_seconds()/86400.0)
days = lambda t: (t-tmin).total_seconds()/86400.0 if t else 0.0

arc_ids = [a["arc_id"] for a in sorted(arcs, key=lambda x:(x.get("t_start") or "z"))]
arc_idx = {aid:i for i,aid in enumerate(arc_ids)}
nA = max(1, len(arc_ids)-1)

entities=[]
for a, te, to in zip(acts, tevs, tobss):
    k = a.get("kind","say")
    entities.append({
        "label": a.get("title","")[:80],
        "kind": k, "actor": a.get("actor","SOREN"), "arc_id": a.get("arc_id",""),
        "t_event": round(days(te),4), "t_obs": round(days(to),4),
        "t_event_iso": (a.get("t_event","") or "")[:19].replace("T"," "),
        "t_obs_iso": (a.get("t_obs","") or "")[:19].replace("T"," "),
        "phys_latent": PL.get(k,0.65),
        "render": a.get("render",0.5),
        "certainty": a.get("certainty"),
        "arc_norm": round(arc_idx.get(a.get("arc_id"),0)/nA,4),
        "blurred": bool(a.get("blurred")),
    })

# daily ticks
ticks=[]
import math
d0 = datetime(tmin.year,tmin.month,tmin.day,tzinfo=timezone.utc)
t = d0
while t <= tmax:
    dd = days(t)
    if dd>=-0.01:
        ticks.append({"t":round(dd,3),"label":t.strftime("%m-%d")})
    t = t.fromordinal(t.toordinal()+1).replace(tzinfo=timezone.utc)

t_obs_set = sorted({e["t_obs_iso"] for e in entities})
data = {
    "entities": entities, "arcs": [{"arc_id":a["arc_id"],"title":a.get("title","")} for a in arcs],
    "t_min": 0.0, "t_max": round(span,4),
    "t_min_iso": tmin.strftime("%Y-%m-%d"), "t_max_iso": tmax.strftime("%Y-%m-%d"),
    "t_obs_iso": (t_obs_set[0] if len(t_obs_set)==1 else f"{len(t_obs_set)} epochs"),
    "ticks": ticks,
    "stats": {"n": len(entities)},
}

html_path = HERE/"BITEMPORAL_3D.html"
html = html_path.read_text(encoding="utf-8")
inj = '<script id="bt-data">window.BITEMPORAL_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
html2, n = re.subn(r'<script id="bt-data">.*?</script>', lambda m: inj, html, count=1, flags=re.DOTALL)
if not n:
    print("ERROR: no <script id=\"bt-data\"> block found"); sys.exit(1)
html_path.write_text(html2, encoding="utf-8")
print(f"injected {len(entities)} wrappers into BITEMPORAL_3D.html")
print(f"  time span: {tmin.strftime('%Y-%m-%d %H:%M')} -> {tmax.strftime('%Y-%m-%d %H:%M')} ({span:.2f} days)")
print(f"  t_obs epochs: {t_obs_set}")
print(f"  ticks: {[t['label'] for t in ticks]}")
