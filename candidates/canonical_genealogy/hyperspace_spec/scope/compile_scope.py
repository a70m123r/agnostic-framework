#!/usr/bin/env python3
"""
Procedural compiler for the FULL-SCOPE substrate (the whole latent-camera arc V1->V6 + the two
octaves + the three-clock equation + the big-map placement). Follows the canonical_genealogy
SUBSTRATE discipline + the COIN: rendered_sharpness <= verified support. render = min(declared,
bucket_cap) -- a card renders only as sharp as its verification state allows; blur (low opacity in
the viewer) is the badge. Demotions are kept as dead-children, not deleted. Stdlib only. Offline.

In: scope_records.jsonl   Out: compiled/scope.compiled.json + inline-injected SCOPE.html + summary.
"""
import json, re, sys, html
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BUCKET_CAP = {"corroborated": 1.00, "pending": 0.60, "conceptual": 0.55, "planned": 0.40, "demoted": 0.30}
COLOR = {"corroborated": "#3fb950", "pending": "#d29922", "conceptual": "#58a6ff",
         "planned": "#8b62d9", "demoted": "#6e7681"}
SECTIONS = [
    ("instrument", "The Instrument"),
    ("spectrum", "The Wrapper Spectrum - the cost of every missing frame"),
    ("stack", "The Model Cost Stack - the BUILD iceberg"),
    ("single", "Octave I - Single Observer (work + span)"),
    ("collective", "Octave II - Collective (+ coordination)"),
    ("clocks", "The Three Clocks (build + maintain + use)"),
    ("map", "The Big Map - where we are"),
]


def _card_html(r, i):
    """Server-render ONE card -- identical structure to the old JS render(), so the page shows full
    content even when scripts don't run. data-i lets the JS enhancer wire the click->detail panel."""
    col = COLOR.get(r.get("bucket", ""), "#8a97ac")
    e = lambda x: html.escape(str(x))
    opacity = max(0.32, float(r.get("render", 0.4)))          # COIN: blur = low opacity
    cls = "card planned" if r.get("bucket") == "planned" else "card"
    dead = ""
    if r.get("demotions"):
        dead = '<div class="dead">' + "".join(
            f'<span class="x">&dagger; {e(d)}</span>' for d in r["demotions"]) + '</div>'
    refs = ""
    if r.get("refs"):
        refs = '<div class="refs">' + "".join(f'<span>{e(x)}</span>' for x in r["refs"]) + '</div>'
    dc = f'<span class="badge">&dagger; {r["dead_children"]} demoted</span>' if r.get("dead_children") else ""
    return (
        f'<div class="{cls}" data-i="{i}" style="opacity:{opacity:.3f}">'
        f'<div class="t"><span class="dot" style="background:{col}"></span>{e(r.get("title",""))}</div>'
        f'<div class="c">{e(r.get("claim",""))}</div>'
        f'<div class="meta"><span class="badge" style="border-color:{col}44;color:{col}">{e(r.get("bucket",""))}</span>'
        f'{dc}<span class="render">render {float(r.get("render",0)):.2f}</span></div>{dead}{refs}</div>')


def _body_html(recs):
    by_sec = {}
    for idx, r in enumerate(recs):
        by_sec.setdefault(r.get("section"), []).append((idx, r))
    out = []
    for key, label in SECTIONS:
        rs = by_sec.get(key, [])
        if not rs:
            continue
        cards = "".join(_card_html(r, idx) for idx, r in rs)
        out.append(f'<div class="section"><h2>{html.escape(label)}</h2><div class="grid">{cards}</div></div>')
    return "".join(out)


def _inject_between(html_text, start, end, payload):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    new, n = pat.subn(lambda m: start + payload + end, html_text, count=1)
    return new, n


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

    # inline-inject into SCOPE.html: (1) the data blob for the JS detail-panel enhancer, AND
    # (2) the SERVER-RENDERED cards + footer, so the page is never blank without JS.
    foot_txt = (f'{compiled["_meta"]["what"]} &middot; compiled {t_obs} &middot; {stats["records"]} records '
                f'&middot; mean render {stats["mean_render"]} &middot; {stats["demotions_total"]} '
                f'demotions (dead children) &middot; {html.escape(json.dumps(stats["by_bucket"]))}')
    tl = HERE / "SCOPE.html"
    if tl.exists():
        doc = tl.read_text(encoding="utf-8")
        data_js = "window.SCOPE = " + json.dumps(compiled, ensure_ascii=False) + ";"
        inline = '<script id="scope-data">' + data_js + '</script>'
        doc, n1 = re.subn(r'<script id="scope-data">.*?</script>', lambda m: inline, doc, count=1, flags=re.DOTALL)
        doc, n2 = _inject_between(doc, "<!--BODY:START-->", "<!--BODY:END-->", _body_html(recs))
        doc, n3 = _inject_between(doc, "<!--FOOT:START-->", "<!--FOOT:END-->", foot_txt)
        if n1 and n2 and n3:
            tl.write_text(doc, encoding="utf-8")
            print("  injected scope data + server-rendered body/footer into SCOPE.html")
        else:
            print(f"  WARN: SCOPE.html injection points missing (data={n1} body={n2} foot={n3})", file=sys.stderr)
    print("=== scope compile ===")
    print(f"  records {stats['records']}  mean render {stats['mean_render']}")
    print(f"  by bucket {stats['by_bucket']}")
    print(f"  demotions (dead children) total {stats['demotions_total']}")
    print(f"  wrote compiled/scope.compiled.json")


if __name__ == "__main__":
    main()
