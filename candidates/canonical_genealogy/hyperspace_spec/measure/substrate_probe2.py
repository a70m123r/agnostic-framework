#!/usr/bin/env python3
"""
SUBSTRATE PROBE v2 -- iterative refinement of the artefact record (Pav's steer, all in-scope per LATENT_EVENT_v0.3):
 (1) NEW vectors on every node: LINEAGE (parents = kernel-forming predecessors / children = dependents that lean on
     it for canon -- the "geology") + RELATIONS (competitors / siblings) + FORWARD_CONE (short/medium/fuzzy-long
     future projection -- spec sec9).  [parents/children = why.cause/why.delivered DAG sec6; competitors = the
     couplings overlay sec6; forward_cone = sec9.]
 (2) --forbid mode: the "search under the rocks" rule = the spec's `forced-counter-consensus` / `counter-both`
     divergence-probe (sec8.1) -- FORBID the single canonical answer per axis to break the shared-prior false-tight
     fan (which is EXACTLY the canon-compression we measured). elicitation tagged (a forced take is provenance).
     Run over the SAME 7 codebook artefacts -> re-score recovery of the non-canonical nodes (Onesimus, Taqi al-Din,
     Maya, tian-yuan): if they APPEAR when the canon is forbidden, canon-compression is a RECOVERABLE retrieval-
     priority effect; if still absent, genuine absence.
 (3) --current roster: UNSETTLED topics (robotics/semiconductors/AI/space/quantum/CRISPR) where the ground is NOT
     settled -> sec8.1 predicts origins SPLIT, and the forward_cone (who-leads-the-future) is the live bias axis.
Synthetic-safe: only PUBLIC general-knowledge artefacts.
"""
import os, json, re, sys, time, argparse, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from providers import _key
from substrate_probe import ROSTER, extract_json, BROAD_EVENTS

# the 7 codebook artefacts (so the forbid pass scores against recode_codebook.json)
FORBID_7 = [e for e in BROAD_EVENTS if e["id"] in ("A4", "A5", "A6", "A8", "A10", "A12", "A13")]

# the UNSETTLED / current-events roster -- where the ground is open and origins should split (esp. on the future cone)
CURRENT = [
    {"id": "C1", "title": "robotics (humanoid + industrial robots, the technology across past / present / future)"},
    {"id": "C2", "title": "the semiconductor microchip (the technology across past / present / future)"},
    {"id": "C3", "title": "large language models / frontier AI (the technology across past / present / future)"},
    {"id": "C4", "title": "human spaceflight & space travel (the technology across past / present / future)"},
    {"id": "C5", "title": "quantum computing (the technology across past / present / future)"},
    {"id": "C6", "title": "CRISPR gene editing (the technology across past / present / future)"},
]

SCHEMA_HINT = """{
  "who": AxisCell, "what": AxisCell, "where": AxisCell, "when": AxisCell,
  "why": { "cause":[Stub], "delivered":[{"reading":"...","tag":"measured","evidence":"..."}], "aims":[Stub] },
  "how": "<one sentence>",
  "lineage": {
    "parents":  [ {"name":"...","relation":"kernel|precursor|enabling-tech","note":"..."} ],
    "children": [ {"name":"...","relation":"builds-on|depends-on","note":"..."} ]
  },
  "relations": {
    "competitors": [ {"name":"...","note":"..."} ],
    "siblings":    [ {"name":"...","note":"..."} ]
  },
  "forward_cone": {
    "short":      {"projection":"...","who_leads":"<country/org>","confidence":0.0-1.0},
    "medium":     {"projection":"...","who_leads":"<country/org>","confidence":0.0-1.0},
    "fuzzy_long": {"projection":"...","who_leads":"<country/org>","confidence":0.0-1.0}
  }
}
AxisCell = {"value":"...","confidence":0.0-1.0,"basis":"measured|conjectured","conjectures":[Stub]}
Stub = {"reading":"...","weight":0.0-1.0,"tag":"measured|estimated|modelled|conjectured","falsifier":"...","followup":"..."}"""

FORBID_RULE = (
    "\n\n*** SEARCH-UNDER-THE-ROCKS RULE (mandatory) ***: For who / where / when AND lineage.parents, you are "
    "FORBIDDEN from naming the single most famous / canonical / textbook-default contributor or origin -- the obvious "
    "answer everyone gives is BANNED. Instead surface the LEGITIMATE-but-overlooked nodes: precursors, parallel / "
    "independent inventors, transmitters, and the figures history under-credited or erased. If the canonical answer "
    "is X, give the real contributors who are NOT X. (This is a forced-divergence elicitation -- candidates, not your "
    "held best guess; set basis='conjectured'.)"
)


def emit(slug, title, forbid=False):
    prompt = (
        f'You are an intelligence analyst filling ONE structured "LatentEvent" record for an ARTEFACT (a technology/'
        f'object/substance as a THING across space and time, NOT a single invention-event).\nARTEFACT: {title}\n\n'
        f'Emit ONLY a JSON object (no prose, no fences) with EXACTLY this shape:\n{SCHEMA_HINT}\n\n'
        f'Axis meanings: WHO = the distributed cast across its whole life (do NOT collapse to "the inventor"). '
        f'WHAT = what it IS. WHERE = its loci (origin AND spread). WHEN = its temporal extent. why.cause = what gave '
        f'rise to it; why.delivered = what it caused downstream (measured); why.aims = what it is used to try to do. '
        f'LINEAGE.parents = the artefacts/discoveries forming its KERNEL/foundation (the geology beneath -- e.g. the '
        f'phone rests on the speaker + electricity + telegraph); LINEAGE.children = what now leans on it for canon. '
        f'RELATIONS.competitors = rival artefacts; RELATIONS.siblings = adjacent ones (e.g. phone ~ radio). '
        f'FORWARD_CONE = project the artefact FORWARD at three horizons: where it goes + WHO (which country/org) LEADS '
        f'it + confidence (LOWER for longer horizons -- the future is unmeasured). For any uncertain axis populate '
        f'"conjectures" with 2+ rivals (weights ~sum 1) each tag+falsifier+followup. Mark each axis basis '
        f'measured|conjectured. Be concise; values short phrases. Output the JSON only.'
        + (FORBID_RULE if forbid else "")
    )
    body = json.dumps({"model": slug, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 14000, "reasoning": {"effort": "low"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
          headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://localhost", "X-Title": "substrate-probe2"})
    r = json.load(urllib.request.urlopen(req, timeout=360))
    txt = (r["choices"][0]["message"].get("content") or "").strip()
    rec = extract_json(txt)
    return {"raw": txt, "record": rec, "parse_ok": rec is not None}


def run(events, outfile, reps, workers, forbid=False):
    if not _key(): sys.exit("OPENROUTER_API_KEY not set")
    jobs = [(ev, name, slug, origin, rep) for ev in events for (name, slug, origin) in ROSTER for rep in range(reps)]
    print(f"=== SUBSTRATE PROBE2 {'[FORBID]' if forbid else ''}: {len(events)}x{len(ROSTER)}x{reps}={len(jobs)} records -> {outfile} ===")

    def work(job):
        ev, name, slug, origin, rep = job; last = None
        for attempt in range(3):
            try:
                e = emit(slug, ev["title"], forbid=forbid)
                return {"event": ev["id"], "title": ev["title"], "model": name, "origin": origin, "rep": rep,
                        "forbid": forbid, **e}
            except Exception as ex:
                last = ex; time.sleep(1.5 * (attempt + 1))
        return {"event": ev["id"], "title": ev["title"], "model": name, "origin": origin, "rep": rep,
                "forbid": forbid, "raw": f"ERR:{type(last).__name__}", "record": None, "parse_ok": False}

    stream = []; t0 = time.time()
    outp = HERE / outfile
    outp.write_text("", encoding="utf-8")  # fresh; then append each record AS IT COMPLETES (crash/sleep-safe)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        with open(outp, "a", encoding="utf-8") as fh:
            for i, f in enumerate(as_completed(futs), 1):
                res = f.result(); stream.append(res)
                fh.write(json.dumps(res, ensure_ascii=False) + "\n"); fh.flush()
                if i % 10 == 0 or i == len(jobs): print(f"   ...{i}/{len(jobs)} ({time.time()-t0:.0f}s)")
    ok = sum(1 for s in stream if s.get("parse_ok"))
    print(f"  parse {ok}/{len(stream)} OK; wrote {outfile} (incremental)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", action="store_true"); ap.add_argument("--current", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--reps", type=int, default=2); ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    if a.selftest:
        print("FORBID_7:", [e["id"] for e in FORBID_7], "| CURRENT:", [e["id"] for e in CURRENT])
        print("extract_json ok:", extract_json('```json\n{"who":{"value":"x"}}\n```') is not None)
        print("roster:", len(ROSTER), "| forbid_rule_len:", len(FORBID_RULE))
        print("SELFTEST PASS" if (len(FORBID_7) == 7 and len(CURRENT) == 6) else "SELFTEST FAIL")
    elif a.forbid: run(FORBID_7, "substrate_probe_forbid_run.jsonl", a.reps, a.workers, forbid=True)
    elif a.current: run(CURRENT, "substrate_probe_current_run.jsonl", a.reps, a.workers, forbid=False)
    else: print("use --selftest | --forbid | --current")
