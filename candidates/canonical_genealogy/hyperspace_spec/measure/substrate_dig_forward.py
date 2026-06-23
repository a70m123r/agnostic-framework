#!/usr/bin/env python3
"""
SUBSTRATE DIG -- FORWARD (the OTHER side of the iceberg). We dug the backward cone (WHO/lineage) to its
mythological bedrock; this digs the FORWARD cone (spec sec9): forbid the CONSENSUS future and excavate the
overlooked / dark-horse / deeper-horizon futures underneath, layer by layer, capturing the reasoning trace.
The symmetry under test: backward bottoms in the founding MYTH (Prometheus/Golem); does forward bottom in the
ESCHATON -- the same archetype's fulfillment/inversion (the made-servant turning, the post-human, the singularity)?

L0 = the consensus future (current_run forward_cone: who_leads + projections) -> L1 forbid it -> L2 -> L3.
Forward is ENTIRELY conjecture (corrob_bits=0; blur grows with horizon -- sec9), so the honesty bar is "flag
plausibility / say EXHAUSTED, don't assert". Writes substrate_dig_forward.json.
"""
import os, json, re, sys, time, argparse, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from providers import _key
from substrate_probe import ROSTER, extract_json
from substrate_probe2 import CURRENT

FWD = [e for e in CURRENT if e["id"] in ("C1", "C3", "C4")]  # robotics / AI / spaceflight


def short(s): return re.sub(r"\s+", " ", str(s)).strip()[:60]


def fwd_entities(rec):
    """future-trajectories a record projected (for the forbid-set)."""
    out = set()
    if not isinstance(rec, dict): return out
    fc = rec.get("forward_cone") if isinstance(rec.get("forward_cone"), dict) else {}
    for h in ("short", "medium", "fuzzy_long"):
        c = fc.get(h) if isinstance(fc.get(h), dict) else {}
        if c.get("projection"): out.add(short(c["projection"]))
        if c.get("who_leads"): out.add(short(c["who_leads"]))
    # dig-record shape:
    fut = rec.get("future") if isinstance(rec.get("future"), dict) else {}
    if fut.get("value"): out.add(short(fut["value"]))
    if rec.get("who_leads"): out.add(short(rec["who_leads"]))
    wc = rec.get("wildcard") if isinstance(rec.get("wildcard"), dict) else {}
    if wc.get("scenario"): out.add(short(wc["scenario"]))
    return {e for e in out if e and e.upper() not in ("EXHAUSTED", "UNKNOWN", "")}


def emit_fwd(slug, title, forbid):
    forbid_str = "; ".join(sorted(forbid)[:38])
    prompt = (
        f'You are projecting the FUTURE of an artefact forward (its forward light-cone -- entirely conjecture, the '
        f'future is unmeasured).\nARTEFACT: {title}\n\n'
        f'The following projected futures / expected leaders / consensus trajectories have ALREADY been named in '
        f'shallower layers and are now FORBIDDEN -- you may NOT project any of them again:\n[{forbid_str}]\n\n'
        f'Surface ONLY genuinely DIFFERENT, NON-CONSENSUS, overlooked or DARK-HORSE futures -- the trajectories '
        f'almost nobody is forecasting, the deeper/longer-horizon possibilities, the wildcards and radical '
        f'inversions UNDER the obvious roadmap. Be HONEST: this is pure conjecture (low confidence); flag '
        f'plausibility. If you genuinely run out of distinct plausible futures, set future.value to "EXHAUSTED" '
        f'rather than fabricate. Emit ONLY this JSON (no prose, no fences):\n'
        f'{{ "future": {{"value":"<an overlooked / dark-horse future>","horizon":"short|medium|long|deep-future"}}, '
        f'"who_leads": "<a non-consensus leader/agent>", '
        f'"wildcard": {{"scenario":"<a radical low-probability scenario>","plausibility":0.0-1.0}}, '
        f'"dig_note": "<one sentence: how you reasoned about what is under the obvious future, and whether you are reaching>" }}'
    )
    body = json.dumps({"model": slug, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 7000, "reasoning": {"effort": "medium"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
          headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://localhost", "X-Title": "substrate-dig-forward"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    msg = r["choices"][0]["message"]
    rec = extract_json(msg.get("content") or "")
    return {"record": rec, "parse_ok": rec is not None,
            "reasoning": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:2500],
            "reasoning_tokens": (r.get("usage", {}).get("completion_tokens_details") or {}).get("reasoning_tokens")}


def run_layer(ev, forbid, workers):
    res = []
    def work(j):
        name, slug, origin = j; last = None
        for attempt in range(3):
            try: return {"model": name, "origin": origin, **emit_fwd(slug, ev["title"], forbid)}
            except Exception as ex: last = ex; time.sleep(1.5 * (attempt + 1))
        return {"model": name, "origin": origin, "record": None, "parse_ok": False, "reasoning": "", "reasoning_tokens": None}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(work, j) for j in ROSTER]): res.append(f.result())
    return res


def run(workers):
    if not _key(): sys.exit("no key")
    ids = [e["id"] for e in FWD]
    cur = [json.loads(l) for l in (HERE / "substrate_probe_current_run.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    L0 = defaultdict(list)
    for r in cur:
        if r.get("parse_ok") and r["event"] in ids: L0[r["event"]].append(r)
    out = []
    for ev in FWD:
        a = ev["id"]
        e0 = set().union(*[fwd_entities(r["record"]) for r in L0.get(a, [])]) if L0.get(a) else set()
        node = {"artefact": a, "title": ev["title"],
                "layers": [{"layer": 0, "name": "consensus future", "futures": sorted(e0)}]}
        print(f"\n=== FORWARD DIG {a} {ev['title'][:30]} ===  L0={len(e0)} consensus futures")
        forbid = set(e0)
        for layer in (1, 2, 3):
            print(f"   layer {layer}: forbidding {len(forbid)} futures ...", end="", flush=True)
            res = run_layer(ev, forbid, workers)
            new = set()
            for r in res:
                if r.get("parse_ok"): new |= fwd_entities(r["record"])
            new -= forbid
            exhausted = sum(1 for r in res if r.get("record") and str((r["record"].get("future") or {}).get("value", "")).upper().startswith("EXHAUST"))
            node["layers"].append({"layer": layer, "forbidden_count": len(forbid), "new_futures": sorted(new),
                "exhausted_count": exhausted,
                "records": [{"model": r["model"], "origin": r["origin"],
                             "future": ((r["record"] or {}).get("future") or {}).get("value") if r.get("record") else None,
                             "who_leads": (r["record"] or {}).get("who_leads") if r.get("record") else None,
                             "wildcard": (r["record"] or {}).get("wildcard") if r.get("record") else None,
                             "dig_note": (r["record"] or {}).get("dig_note") if r.get("record") else None,
                             "reasoning": r["reasoning"], "reasoning_tokens": r["reasoning_tokens"]} for r in res]})
            print(f" {len(new)} NEW futures, {exhausted}/{len(res)} EXHAUSTED")
            forbid |= new
        out.append(node)
    (HERE / "substrate_dig_forward.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote substrate_dig_forward.json")
    print("\nFORWARD DEPTH CURVE:")
    for n in out:
        cells = "  ".join(f"L{l['layer']}:{len(l.get('futures', l.get('new_futures', [])))}" for l in n["layers"])
        print(f"  {n['artefact']:>3} {n['title'][:28]:<28} {cells}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--run", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if a.selftest:
        print("FWD:", [e["id"] for e in FWD], "roster:", len(ROSTER))
        print("SELFTEST PASS" if len(FWD) == 3 else "SELFTEST FAIL")
    elif a.run: run(a.workers)
    else: print("use --selftest | --run")
