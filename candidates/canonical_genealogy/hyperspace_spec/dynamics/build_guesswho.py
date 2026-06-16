#!/usr/bin/env python3
"""Inject the dynamics substrate into GUESS_WHO.html (self-contained). Every tile is a real record;
every question a real field. No invented numbers — the channel rule, enforced."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
recs = json.loads((HERE/"compiled"/"dynamics.compiled.json").read_text(encoding="utf-8"))["records"]
slim = [{
    "id": r["id"], "name": r["name"], "type": r["type"], "family": r["family"],
    "observable": r.get("observable","") or r.get("what",""),
    "render": r.get("render"), "certainty": r.get("certainty"),
    "lifecycle": r.get("lifecycle","tracked"), "phys_latent": r.get("phys_latent",0.6),
    "formal_name": r.get("formal_name",""),
} for r in recs]
data = {"records": slim, "n": len(slim)}
p = HERE/"GUESS_WHO.html"
html = p.read_text(encoding="utf-8")
inj = '<script id="gw-data">window.GW_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
html2, n = re.subn(r'<script id="gw-data">.*?</script>', lambda m: inj, html, count=1, flags=re.DOTALL)
if not n:
    raise SystemExit("no gw-data block")
p.write_text(html2, encoding="utf-8")
print(f"injected {len(slim)} records into GUESS_WHO.html")
