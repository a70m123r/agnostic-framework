#!/usr/bin/env python3
"""
Procedural compiler for the SESSION-ARC substrate (the 2026-06-11..06-16 milestone capture).

Follows the SUBSTRATE_SPEC discipline (append-only logs -> deterministic best-value compile,
provenance on every record, certainty rubric, verify state-machine) adapted to capture the
WORK ITSELF rather than world-facts, plus two v0.4 ideas:

  * BITEMPORAL: every act carries t_event (when it happened in the session) and t_obs (this compile).
  * THE COIN (render invariant): rendered_sharpness(x) <= measured/verified support(x).
    An arc/act renders only as sharp as the artifacts on disk actually back it.
    Unverified or unsupported -> blurred. Blur IS the badge. No fake bit.

Inputs  (append-only JSONL, one record per line, in this dir):
  acts.jsonl    - atomic events (Pav steers, decisions, artifacts, tests, commits, demotions)
  arcs.jsonl    - the storyline threads that connect the acts
  verify.jsonl  - per-arc verification vs the real files on disk (the COIN check)

Outputs:
  compiled/arc.compiled.json  - committed best-value capture (arcs + acts + render fields + stats)
  arc_data.js                 - window.ARC_DATA = {...}  (loaded by TIMELINE.html, no server/CORS)
  stdout summary              - coverage, verdict distribution, fake-bit flags

Stdlib only. Offline. Deterministic.
"""
import json, argparse, sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
SPEC_DIR = HERE.parent  # hyperspace_spec/

def load_jsonl(p):
    out = []
    if not p.exists():
        return out
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"  WARN {p.name}:{i} bad json ({e}); skipped", file=sys.stderr)
    return out

# verify bucket -> trust ceiling on render sharpness (the COIN cap by support state)
BUCKET_CAP = {"corroborated": 1.00, "pending": 0.60, "unverifiable": 0.45, "disputed": 0.30}
BUCKET_RANK = {"corroborated": 3, "pending": 2, "unverifiable": 1, "disputed": 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any fake-bit flag is raised")
    args = ap.parse_args()

    acts = load_jsonl(HERE / "acts.jsonl")
    arcs = load_jsonl(HERE / "arcs.jsonl")
    verifs = load_jsonl(HERE / "verify.jsonl")
    t_obs = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if False else "COMPILE_TIME"
    # NOTE: Date.now is fine in plain python (this is not the workflow sandbox); use real UTC:
    t_obs = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # index verifications by arc_id; resolve bucket per state-machine (corroborated>pending>unverifiable>disputed for cap,
    # but disputed must dominate as a flag). Keep all; pick the strongest verdict for the bucket, retain disputes.
    vbyarc = {}
    for v in verifs:
        vbyarc.setdefault(v.get("arc_id"), []).append(v)

    def resolve_verify(arc_id):
        vs = vbyarc.get(arc_id, [])
        if not vs:
            return {"verdict": "pending", "certainty": None, "artifacts_present": [], "artifacts_missing": [],
                    "unsupported_claims": [], "records": 0}
        # any corroborated -> corroborated; else any disputed -> disputed; else unverifiable
        verdicts = [v.get("verdict", "pending") for v in vs]
        if "corroborated" in verdicts:
            bucket = "corroborated"
        elif "disputed" in verdicts:
            bucket = "disputed"
        elif "unverifiable" in verdicts:
            bucket = "unverifiable"
        else:
            bucket = "pending"
        cert = max((v.get("certainty") or 0.0) for v in vs)
        present = sorted({a for v in vs for a in v.get("artifacts_present", [])})
        missing = sorted({a for v in vs for a in v.get("artifacts_missing", [])})
        unsup = sorted({c for v in vs for c in v.get("unsupported_claims", [])})
        return {"verdict": bucket, "certainty": cert, "artifacts_present": present,
                "artifacts_missing": missing, "unsupported_claims": unsup, "records": len(vs)}

    fake_bit_flags = []
    out_arcs = []
    present_global = set()
    for arc in sorted(arcs, key=lambda a: (a.get("t_start") or "z", a.get("arc_id") or "")):
        aid = arc.get("arc_id")
        vr = resolve_verify(aid)
        present_global.update(vr["artifacts_present"])
        declared = float(arc.get("certainty", 0.75))
        cap = BUCKET_CAP[vr["verdict"]]
        vcert = vr["certainty"] if vr["certainty"] is not None else cap
        # THE COIN: render no sharper than the support
        render = round(min(declared, cap, vcert), 3)
        if vr["unsupported_claims"]:
            fake_bit_flags.append({"arc_id": aid, "unsupported": vr["unsupported_claims"]})
        out_arcs.append({
            **arc,
            "verify": vr,
            "bucket": vr["verdict"],
            "render": render,                    # honest sharpness in [0,1] for the viewer
        })

    # render per act: capped by its own arc's render, blurred if it names an artifact the arc could not confirm
    arc_render = {a["arc_id"]: a["render"] for a in out_arcs}
    arc_present = {a["arc_id"]: set(a["verify"]["artifacts_present"]) for a in out_arcs}
    arc_missing = {a["arc_id"]: set(a["verify"]["artifacts_missing"]) for a in out_arcs}
    out_acts = []
    for act in acts:
        aid = act.get("arc_id")
        base = float(act.get("certainty", 0.7))
        cap = arc_render.get(aid, 0.6)
        blurred = False
        for art in act.get("artifacts", []):
            if art in arc_missing.get(aid, set()):
                blurred = True
        render = round(min(base, cap) * (0.5 if blurred else 1.0), 3)
        out_acts.append({**act, "t_obs": t_obs, "render": render, "blurred": blurred})

    out_acts.sort(key=lambda a: (a.get("t_event") or "z", a.get("act_id") or ""))

    # stats
    buckets = {}
    for a in out_arcs:
        buckets[a["bucket"]] = buckets.get(a["bucket"], 0) + 1
    kinds = {}
    for a in out_acts:
        kinds[a.get("kind", "?")] = kinds.get(a.get("kind", "?"), 0) + 1
    t_events = [a["t_event"] for a in out_acts if a.get("t_event")]
    window = {"start": min(t_events) if t_events else None, "end": max(t_events) if t_events else None}

    narrative = ""
    npath = HERE / "milestone_narrative.txt"
    if npath.exists():
        narrative = npath.read_text(encoding="utf-8")

    compiled = {
        "_meta": {
            "what": "session-arc capture: the 2026-06-11..06-16 milestone work, compiled as substrate",
            "discipline": "SUBSTRATE_SPEC (append-only+provenance+certainty+verify) + bitemporal + COIN (render<=support)",
            "t_obs": t_obs, "window": window,
            "honesty": "render in [0,1] = honest sharpness; blur is the badge; unsupported claims flagged as candidate fake bits",
        },
        "stats": {
            "arcs": len(out_arcs), "acts": len(out_acts),
            "buckets": buckets, "kinds": kinds,
            "fake_bit_flags": len(fake_bit_flags),
            "artifacts_verified": len(present_global),
        },
        "arcs": out_arcs,
        "acts": out_acts,
        "fake_bit_flags": fake_bit_flags,
        "milestone_narrative": narrative,
    }

    (HERE / "compiled").mkdir(exist_ok=True)
    (HERE / "compiled" / "arc.compiled.json").write_text(
        json.dumps(compiled, indent=2, ensure_ascii=False), encoding="utf-8")
    data_js = "window.ARC_DATA = " + json.dumps(compiled, ensure_ascii=False) + ";"
    (HERE / "arc_data.js").write_text(data_js + "\n", encoding="utf-8")

    # inject the data INLINE into TIMELINE.html so the viewer is fully self-contained
    # (works on double-click / file:// / any preview panel - no external arc_data.js fetch needed)
    import re
    tl = HERE / "TIMELINE.html"
    if tl.exists():
        html = tl.read_text(encoding="utf-8")
        inline = '<script id="arc-data">' + data_js + '</script>'
        html2, n = re.subn(r'<script id="arc-data">.*?</script>', lambda m: inline, html, count=1, flags=re.DOTALL)
        if n:
            tl.write_text(html2, encoding="utf-8")
        else:
            print("  WARN: TIMELINE.html has no <script id=\"arc-data\"> block to inject into")

    print("=== session-arc compile ===")
    print(f"  arcs: {len(out_arcs)}  acts: {len(out_acts)}")
    print(f"  window: {window['start']} .. {window['end']}")
    print(f"  verify buckets: {buckets}")
    print(f"  act kinds: {kinds}")
    print(f"  artifacts verified present: {len(present_global)}")
    print(f"  fake-bit flags (unsupported claims): {len(fake_bit_flags)}")
    for fb in fake_bit_flags:
        print(f"     [{fb['arc_id']}] {fb['unsupported']}")
    print(f"  wrote compiled/arc.compiled.json + arc_data.js")
    if args.strict and fake_bit_flags:
        sys.exit(1)

if __name__ == "__main__":
    main()
