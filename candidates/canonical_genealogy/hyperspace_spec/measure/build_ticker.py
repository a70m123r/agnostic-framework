#!/usr/bin/env python3
"""Inject the live digestion stream (measurement_run.jsonl) into TICKER.html. Self-contained.
Every needle is a measured value; nothing fabricated (the channel rule)."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
rows = [json.loads(l) for l in (HERE/"measurement_run.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
T = {}
for r in rows:
    t = T.setdefault(r["target"], {"id": r["target"], "kind": r.get("kind",""), "rho": []})
    if "depth" in r:
        T[r["target"]]["rho"].append((r["depth"], r["residue_bits"]))
    if "two_clock_present" in r:
        t["present"] = r["two_clock_present"]; t["amortized"] = r["two_clock_amortized"]
        t["gap"] = r["two_clock_gap"]; t["dissolved"] = r["dissolved_frac"]
targets = []
for t in T.values():
    t["rho"] = [v for _, v in sorted(t["rho"])]
    targets.append(t)
data = {"targets": targets, "n": len(targets)}
p = HERE/"TICKER.html"
html = p.read_text(encoding="utf-8")
inj = '<script id="tk-data">window.TK_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
html2, n = re.subn(r'<script id="tk-data">.*?</script>', lambda m: inj, html, count=1, flags=re.DOTALL)
if not n:
    raise SystemExit("no tk-data block")
p.write_text(html2, encoding="utf-8")
print(f"injected {len(targets)} targets into TICKER.html:", ", ".join(f"{t['id']}({int((t.get('dissolved') or 0)*100)}%)" for t in targets))
