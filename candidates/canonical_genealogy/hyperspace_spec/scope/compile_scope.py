#!/usr/bin/env python3
"""
Procedural compiler for the FULL-SCOPE substrate (the whole latent-camera arc V1->V6 + the two
octaves + the three-clock equation + the big-map placement). Follows the canonical_genealogy
SUBSTRATE discipline + the COIN: rendered_sharpness <= verified support. render = min(declared,
bucket_cap) -- a card renders only as sharp as its verification state allows; blur (low opacity in
the viewer) is the badge. Demotions are kept as dead-children, not deleted. Stdlib only. Offline.

In: scope_records.jsonl   Out: compiled/scope.compiled.json + inline-injected SCOPE.html + summary.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BUCKET_CAP = {"corroborated": 1.00, "pending": 0.60, "conceptual": 0.55, "planned": 0.40, "demoted": 0.30}
SECTIONS = [
    ("instrument", "The Instrument"),
    ("single", "Octave I - Single Observer (work + span)"),
    ("collective", "Octave II - Collective (+ coordination)"),
    ("clocks", "The Three Clocks (build + maintain + use)"),
    ("map", "The Big Map - where we are"),
]


def main():
    recs = []
    for i, line in enumerate((HERE / "scope_records.jsonl").read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"  WARN line {i}: {e}", file=sys.stderr)
    t_obs = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for r in recs:
        cap = BUCKET_CAP.get(r.get("bucket", "conceptual"), 0.5)
        r["render"] = round(min(float(r.get("declared", 0.6)), cap), 3)
        r["dead_children"] = len(r.get("demotions", []))
    recs.sort(key=lambda r: r.get("order", 999))
    stats = {"records": len(recs),
             "by_bucket": {b: sum(1 for r in recs if r.get("bucket") == b) for b in BUCKET_CAP},
             "demotions_total": sum(r["dead_children"] for r in recs),
             "mean_render": round(sum(r["render"] for r in recs) / max(1, len(recs)), 3)}
    compiled = {"_meta": {"what": "full-scope latent-camera substrate", "t_obs": t_obs,
                          "discipline": "SUBSTRATE + COIN (render<=support); demote-not-kill",
                          "sections": SECTIONS}, "stats": stats, "records": recs}
    (HERE / "compiled").mkdir(exist_ok=True)
    (HERE / "compiled" / "scope.compiled.json").write_text(json.dumps(compiled, indent=2, ensure_ascii=False), encoding="utf-8")

    # inline-inject into SCOPE.html
    data_js = "window.SCOPE = " + json.dumps(compiled, ensure_ascii=False) + ";"
    tl = HERE / "SCOPE.html"
    if tl.exists():
        html = tl.read_text(encoding="utf-8")
        inline = '<script id="scope-data">' + data_js + '</script>'
        html2, n = re.subn(r'<script id="scope-data">.*?</script>', lambda m: inline, html, count=1, flags=re.DOTALL)
        if n:
            tl.write_text(html2, encoding="utf-8")
            print("  injected scope data into SCOPE.html")
        else:
            print("  WARN: SCOPE.html has no <script id=\"scope-data\"> injection point", file=sys.stderr)
    print("=== scope compile ===")
    print(f"  records {stats['records']}  mean render {stats['mean_render']}")
    print(f"  by bucket {stats['by_bucket']}")
    print(f"  demotions (dead children) total {stats['demotions_total']}")
    print(f"  wrote compiled/scope.compiled.json")


if __name__ == "__main__":
    main()
