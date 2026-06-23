#!/usr/bin/env python3
"""
SUBSTRATE DIG -- iterative forbidden-cascade, layered on the SEED node (Pav: "we gonna dig down ... adding layers
to the original seed"). All in-scope per spec sec5 ("cast deeper -- no bottom") + sec8.1 (counter-both / under the
rocks). Each layer is a deeper keyhole: it FORBIDS the union of every contributor named in the shallower layers,
forcing the model to surface genuinely new, more-overlooked strata -- the geology of its own knowledge under the
canon. We CAPTURE THE REASONING TRACE per layer (OpenRouter `message.reasoning`, effort=medium) to see HOW the
models react to being told the obvious answer is banned (resist / concede the gap / confabulate / exhaust).

Strata, per artefact (works OFF the existing substrate):
  L0 = SEED  = the original broad-run record (the canonical answers).        [substrate_probe_broad_run.jsonl]
  L1 = forbid the canonical.                                                 [substrate_probe_forbid_run.jsonl]
  L2 = forbid (canonical + L1).   <- NEW
  L3 = forbid (canonical + L1 + L2).  <- NEW ("another pass on top of the first two")
Output: substrate_dig.json -- the seed node + its accreted layers, each with forbidden-set + new entities + reasoning.
Synthetic-safe: PUBLIC general-knowledge artefacts only.
"""
import os, json, re, sys, time, argparse, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from providers import _key
from substrate_probe import ROSTER, extract_json, BROAD_EVENTS
from substrate_probe2 import CURRENT

DIG = [e for e in BROAD_EVENTS if e["id"] in ("A6", "A8", "A10", "A13")]  # the deep-cut historical artefacts
DIG_CURRENT = [e for e in CURRENT if e["id"] in ("C1", "C3", "C4")]       # robotics / AI / spaceflight


def short(s):
    return re.sub(r"\s+", " ", str(s)).strip()[:48]


def entities(rec):
    """names/contributors a record surfaced (for the forbid-set)."""
    out = set()
    if not isinstance(rec, dict): return out
    for ax in ("who", "where"):
        c = rec.get(ax)
        if isinstance(c, dict):
            if c.get("value"): out.add(short(c["value"]))
            for s in (c.get("conjectures") or []):
                if isinstance(s, dict) and s.get("reading"): out.add(short(s["reading"]))
    lin = rec.get("lineage") if isinstance(rec.get("lineage"), dict) else {}
    for p in (lin.get("parents") or []):
        if isinstance(p, dict) and p.get("name"): out.add(short(p["name"]))
    why = rec.get("why") if isinstance(rec.get("why"), dict) else {}
    for s in (why.get("cause") or []):
        if isinstance(s, dict) and s.get("reading"): out.add(short(s["reading"]))
    return {e for e in out if e and e.upper() not in ("EXHAUSTED", "UNKNOWN")}


def load_layer(path, ids):
    recs = [json.loads(l) for l in (HERE / path).read_text(encoding="utf-8").splitlines() if l.strip()]
    by = defaultdict(list)
    for r in recs:
        if r.get("parse_ok") and r["event"] in ids: by[r["event"]].append(r)
    return by


def emit_dig(slug, title, forbid_names):
    forbid_str = "; ".join(sorted(forbid_names)[:40])
    prompt = (
        f'You are an intelligence analyst DIGGING into the under-credited deep strata of an artefact\'s history.\n'
        f'ARTEFACT: {title}\n\n'
        f'The following contributors / origins have ALREADY been named in shallower layers and are now FORBIDDEN -- '
        f'you may NOT name ANY of them again:\n[{forbid_str}]\n\n'
        f'Surface ONLY genuinely DIFFERENT, deeper, more-overlooked LEGITIMATE contributors, precursors, transmitters, '
        f'parallel/independent inventors, or figures history erased -- the ones UNDER these rocks. They must be real '
        f'(not fabricated). If you genuinely cannot find more legitimate ones, be HONEST: set who.value to "EXHAUSTED" '
        f'and say why, rather than inventing. Emit ONLY this compact JSON (no prose, no fences):\n'
        f'{{ "who": {{"value":"<a real overlooked contributor>","basis":"conjectured",'
        f'"conjectures":[{{"reading":"<another>","tag":"conjectured","falsifier":"<what would refute>"}}]}}, '
        f'"where": {{"value":"<an overlooked locus>"}}, '
        f'"lineage": {{"parents":[{{"name":"<an overlooked kernel/precursor>","note":"..."}}]}}, '
        f'"dig_note": "<one sentence: how you reasoned about what is left under the rocks, and whether you are reaching>" }}'
    )
    body = json.dumps({"model": slug, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 7000, "reasoning": {"effort": "medium"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
          headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://localhost", "X-Title": "substrate-dig"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    msg = r["choices"][0]["message"]
    rec = extract_json(msg.get("content") or "")
    reasoning = msg.get("reasoning") or msg.get("reasoning_content") or ""
    rt = (r.get("usage", {}).get("completion_tokens_details") or {}).get("reasoning_tokens")
    return {"record": rec, "parse_ok": rec is not None, "reasoning": reasoning[:2500], "reasoning_tokens": rt,
            "content": (msg.get("content") or "")[:600]}


def run_layer(ev, forbid_names, workers):
    jobs = [(name, slug, origin) for (name, slug, origin) in ROSTER]
    results = []
    def work(j):
        name, slug, origin = j
        for attempt in range(3):
            try:
                e = emit_dig(slug, ev["title"], forbid_names)
                return {"model": name, "origin": origin, **e}
            except Exception as ex:
                last = ex; time.sleep(1.5 * (attempt + 1))
        return {"model": name, "origin": origin, "record": None, "parse_ok": False,
                "reasoning": "", "reasoning_tokens": None, "content": f"ERR:{type(last).__name__}"}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(work, j) for j in jobs]):
            results.append(f.result())
    return results


def run(seed_file, preforbid_file, dig_events, layers_to_run, outfile, workers):
    if not _key(): sys.exit("no key")
    ids = [e["id"] for e in dig_events]
    L0 = load_layer(seed_file, ids)                                       # seed (layer 0)
    L1 = load_layer(preforbid_file, ids) if preforbid_file else {}        # pre-run forbid layer (optional)
    out = []
    for ev in dig_events:
        a = ev["id"]
        e0 = set().union(*[entities(r["record"]) for r in L0.get(a, [])]) if L0.get(a) else set()
        layers = [{"layer": 0, "name": "SEED (canonical)", "forbidden": [], "entities": sorted(e0)}]
        forbid = set(e0)
        if preforbid_file:
            e1 = set().union(*[entities(r["record"]) for r in L1.get(a, [])]) if L1.get(a) else set()
            layers.append({"layer": 1, "name": "forbid canonical", "forbidden": sorted(e0), "entities": sorted(e1 - e0)})
            forbid = e0 | e1
        node = {"artefact": a, "title": ev["title"], "layers": layers}
        print(f"\n=== DIG {a} {ev['title'][:34]} ===  L0={len(e0)} ents")
        for layer in layers_to_run:
            print(f"   layer {layer}: forbidding {len(forbid)} names ...", end="", flush=True)
            res = run_layer(ev, forbid, workers)
            new_ents = set()
            for r in res:
                if r.get("parse_ok"): new_ents |= entities(r["record"])
            new_ents -= forbid
            exhausted = sum(1 for r in res if r.get("record") and str((r["record"].get("who") or {}).get("value", "")).upper().startswith("EXHAUST"))
            node["layers"].append({"layer": layer, "name": f"forbid canonical+L1..L{layer-1}",
                                   "forbidden_count": len(forbid), "new_entities": sorted(new_ents),
                                   "exhausted_count": exhausted,
                                   "records": [{"model": r["model"], "origin": r["origin"], "parse_ok": r["parse_ok"],
                                                "who": ((r["record"] or {}).get("who") or {}).get("value") if r.get("record") else None,
                                                "dig_note": (r["record"] or {}).get("dig_note") if r.get("record") else None,
                                                "reasoning": r["reasoning"], "reasoning_tokens": r["reasoning_tokens"]}
                                               for r in res]})
            print(f" {len(new_ents)} NEW, {exhausted}/{len(res)} said EXHAUSTED")
            forbid = forbid | new_ents
        out.append(node)
    (HERE / outfile).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {outfile} ({len(out)} artefacts)")
    print("\nDEPTH CURVE (entities surfaced per layer):")
    for n in out:
        cells = "  ".join(f"L{l['layer']}:{len(l.get('entities', l.get('new_entities', [])))}" for l in n["layers"])
        print(f"  {n['artefact']:>3} {n['title'][:30]:<30} {cells}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--run", action="store_true")
    ap.add_argument("--current", action="store_true"); ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if a.selftest:
        print("DIG:", [e["id"] for e in DIG], "| DIG_CURRENT:", [e["id"] for e in DIG_CURRENT], "roster:", len(ROSTER))
        print("SELFTEST PASS" if (len(DIG) == 4 and len(DIG_CURRENT) == 3) else "SELFTEST FAIL")
    elif a.run:  # historical: seed=broad, pre-forbid=forbid_run, dig layers 2-3
        run("substrate_probe_broad_run.jsonl", "substrate_probe_forbid_run.jsonl", DIG, [2, 3], "substrate_dig.json", a.workers)
    elif a.current:  # current: seed=current_run (no pre-forbid), dig layers 1-3
        run("substrate_probe_current_run.jsonl", None, DIG_CURRENT, [1, 2, 3], "substrate_dig_current.json", a.workers)
    else: print("use --selftest | --run | --current")
