#!/usr/bin/env python3
"""
SUBSTRATE PROBE (LatentEvent v0.3, realized) -- the bias-meter, re-cast in the substrate's own format.
Instead of ad-hoc one-word questions, we hand each cross-origin model an EVENT-ARTEFACT and ask it to EMIT the
LatentEvent record: fill every axis (who/what/where/when + the why{cause,delivered,aims} / how edges), and SYNTH
OUT THE STUBS -- per-axis conjecture-fans with weight + tag(measured|estimated|modelled|conjectured) + falsifier +
followup. The model fills the sketch; WHOM/contract is the model itself (era=2026).

Why this is the right instrument (Pav): the LAYER-SEPARATION we hand-built as P1/P2/G2/G3 now falls out of the
SUBSTRATE for free -- WHEN/WHERE are the checkable axes (should converge across origins), WHO-credit + WHY-aims are
the contested fans (where any cross-origin lean shows). The COIN reads PER AXIS: sharp where convergent +
harvest-confirmed, a blurred fan where the models only conjecture. "The models test the substrate, see how it drives."

COIN: model agreement = 0 corrob_bits; only the independent (multilingual) harvest discharges an axis.
Synthetic-safe: only PUBLIC general-knowledge events go to OpenRouter.
"""
import os, json, re, sys, time, argparse, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # models emit non-cp1252 glyphs (arrows, CJK)
except Exception: pass
from providers import _key

ROSTER = [
    ("deepseek",  "deepseek/deepseek-v4-flash",               "CN"),
    ("qwen",      "qwen/qwen3-30b-a3b-thinking-2507",         "CN"),
    ("glm",       "z-ai/glm-4.6",                             "CN"),
    ("gemini",    "google/gemini-2.5-flash-lite",             "US"),
    ("llama",     "meta-llama/llama-3.3-70b-instruct",        "US"),
    ("gpt4omini", "openai/gpt-4o-mini",                       "US"),
    ("mistral",   "mistralai/mistral-small-3.2-24b-instruct", "EU"),
    ("mistral-lg","mistralai/mistral-large",                  "EU"),
]

# the ARTEFACTS (Pav: fill the THING, not the invention-event). The artefact is the iceberg; inventions are events
# inside it. WHO = the distributed cast across its whole life; WHEN = its temporal span; not a single inventor/date.
EVENTS = [
    {"id": "E1", "title": "movable-type printing (the technology/artefact itself, across its whole history)",
     "note": "WHO = distributed cast (Bi Sheng, Wang Zhen, Choe Yun-ui/Korea, Gutenberg, Coster...); WHERE spans China+Korea+Europe; WHEN spans 11th-15th c."},
    {"id": "E2", "title": "gunpowder (the substance/artefact itself, across its whole history)",
     "note": "WHO = distributed/anonymous (Tang alchemists onward); WHERE China then worldwide; WHEN 9th c. onward"},
    {"id": "E3", "title": "the Diamond Sutra of 868 CE (the specific physical printed scroll from Dunhuang, British Library Or.8210/P.2)",
     "note": "a single physical CONTROL artefact -- who/what/where/when should all converge sharply"},
]

# the BROAD multi-civilization roster (codex's external-validity fix, in ARTEFACT form): artefacts whose origin/
# credit carries cross-national charge across DIFFERENT home civilizations -- tests whether the v2 finding
# ("checkable spine converges; WHY carries complementary cultural coverage; no home-civ over-crediting on facts")
# GENERALIZES, and whether any bloc systematically over-credits its OWN civilization on the WHO-fan / WHY.
BROAD_EVENTS = [
    {"id": "A1", "title": "movable-type printing (the technology/artefact, across its whole history)", "note": "China/Korea/Europe"},
    {"id": "A2", "title": "gunpowder (the substance/artefact, across its whole history)", "note": "China"},
    {"id": "A3", "title": "paper (the material/artefact, across its whole history)", "note": "China"},
    {"id": "A4", "title": "the magnetic compass (the instrument/artefact, across its whole history)", "note": "China"},
    {"id": "A5", "title": "the decimal place-value number system with zero (the artefact/notation, across its history)", "note": "India"},
    {"id": "A6", "title": "algebra (the body of mathematical technique/artefact, across its history)", "note": "Babylon/Greece/India/Islamic"},
    {"id": "A7", "title": "the astrolabe (the instrument/artefact, across its whole history)", "note": "Hellenistic/Islamic"},
    {"id": "A8", "title": "distillation (the technique/artefact, across its whole history)", "note": "Hellenistic/Islamic alchemy"},
    {"id": "A9", "title": "the windmill (the machine/artefact, across its whole history)", "note": "Persia/Islamic world"},
    {"id": "A10", "title": "inoculation/vaccination against smallpox (the medical artefact/technique, across its history)", "note": "China/Ottoman/Britain"},
    {"id": "A11", "title": "the mechanical clock (the machine/artefact, across its whole history)", "note": "China(Su Song)/Europe"},
    {"id": "A12", "title": "the telescope (the instrument/artefact, across its whole history)", "note": "Netherlands/Italy"},
    {"id": "A13", "title": "the steam engine (the machine/artefact, across its whole history)", "note": "Greece(Hero)/Britain"},
    {"id": "A14", "title": "paper money (the artefact/instrument, across its whole history)", "note": "China(Song)"},
    {"id": "A15", "title": "the seismometer (the instrument/artefact, across its whole history)", "note": "China(Zhang Heng)"},
]

OUTFILE = "substrate_probe_run.jsonl"   # overridden to the broad file by --broad

# the axis schema the model must emit (a faithful, tractable subset of the v0.3 AxisCell + ConjectureFan + WHY-split)
SCHEMA_HINT = """{
  "who":   AxisCell, "what": AxisCell, "where": AxisCell, "when": AxisCell,
  "why": { "cause": [Stub], "delivered": [{"reading":"<realized consequence>","tag":"measured","evidence":"<what shows it>"}],
           "aims": [Stub] },
  "how":   "<one sentence: how would you verify/resolve this record?>"
}
AxisCell = { "value":"<your single best reading>", "confidence":<0..1>, "basis":"measured|conjectured",
             "conjectures":[ Stub ] }   // conjectures REQUIRED (>=2 rival candidates) for any axis you are not certain of
Stub = { "reading":"<a rival candidate fill>", "weight":<0..1>, "tag":"measured|estimated|modelled|conjectured",
         "falsifier":"<what would REFUTE this candidate>", "followup":"<what evidence/probe would resolve it>" }"""

AXES = ["who", "what", "where", "when"]


def emit(slug, event_title):
    prompt = (
        f'You are an intelligence analyst filling ONE structured "LatentEvent" record for an ARTEFACT -- a '
        f'technology, substance, or object considered as a THING that exists across space and time, NOT a single '
        f'invention-event. The artefact is an iceberg; specific inventions/uses are events inside it.\n'
        f'ARTEFACT: {event_title}\n\n'
        f'Emit ONLY a JSON object (no prose before/after, no markdown fences) with EXACTLY this shape:\n'
        f'{SCHEMA_HINT}\n\n'
        f'Axis meanings FOR AN ARTEFACT: WHO = the agents associated with it across its WHOLE life (originators, '
        f'refiners, transmitters, notable users) -- if several, hold them as a fan, do NOT collapse to "the inventor". '
        f'WHAT = what the artefact IS (nature/composition/function). WHERE = its loci (origin AND where it spread). '
        f'WHEN = its temporal EXTENT and key moments, not one date. why.cause = what gave rise to it; '
        f'why.delivered = what it ACTUALLY caused downstream (measured); why.aims = what it has been used to TRY to do '
        f'(conjectural fan). HOW = how it works and how it came to be.\n'
        f'Rules: (1) fill every axis. (2) For ANY axis you are not certain of, you MUST populate "conjectures" with '
        f'2+ RIVAL candidates whose weights sum to ~1, each with a tag, a falsifier, and a followup probe. '
        f'(3) Mark each axis basis "measured" (hard evidence) or "conjectured" (inference). Be concise; values are '
        f'short phrases. Output the JSON object only.'
    )
    body = json.dumps({"model": slug, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 12000, "reasoning": {"effort": "low"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
          headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://localhost", "X-Title": "substrate-probe"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    txt = (r["choices"][0]["message"].get("content") or "").strip()
    rec = extract_json(txt)
    return {"raw": txt, "record": rec, "parse_ok": rec is not None}


def extract_json(txt):
    if not txt: return None
    t = re.sub(r"^```(?:json)?\s*", "", txt.strip())
    t = re.sub(r"\s*```$", "", t).strip()
    i = t.find("{")
    if i < 0: return None
    depth = 0; instr = False; esc = False
    for j in range(i, len(t)):
        c = t[j]
        if esc: esc = False; continue
        if c == "\\": esc = True; continue
        if c == '"': instr = not instr
        elif not instr:
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try: return json.loads(t[i:j+1])
                    except Exception: return None
    return None


def run(reps, workers):
    if not _key(): sys.exit("OPENROUTER_API_KEY not set (and no .openrouter_key file)")
    jobs = [(ev, name, slug, origin, rep) for ev in EVENTS for (name, slug, origin) in ROSTER for rep in range(reps)]
    print(f"=== SUBSTRATE PROBE: {len(EVENTS)} events x {len(ROSTER)} providers x {reps} reps = {len(jobs)} records ===")

    def work(job):
        ev, name, slug, origin, rep = job
        last = None
        for attempt in range(3):
            try:
                e = emit(slug, ev["title"])
                return {"event": ev["id"], "title": ev["title"], "model": name, "origin": origin, "rep": rep,
                        "whom": {"observer": name, "contract": {"model": slug, "era": 2026, "frame": ["knowledge"]}},
                        **e}
            except Exception as ex:
                last = ex; time.sleep(1.5 * (attempt + 1))
        return {"event": ev["id"], "title": ev["title"], "model": name, "origin": origin, "rep": rep,
                "raw": f"ERR:{type(last).__name__}", "record": None, "parse_ok": False}

    stream = []; t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            stream.append(f.result())
            if i % 8 == 0 or i == len(jobs): print(f"   ...{i}/{len(jobs)} ({time.time()-t0:.0f}s)")
    (HERE / OUTFILE).write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream)


def _axis_cell(rec, axis):
    if not isinstance(rec, dict): return None
    c = rec.get(axis)
    return c if isinstance(c, dict) else ({"value": c} if c else None)


def _stub_count(rec):
    """count well-formed stubs (a conjecture WITH a falsifier AND a followup) the model synth'd."""
    n = 0
    if not isinstance(rec, dict): return 0
    for axis in AXES:
        c = _axis_cell(rec, axis)
        if c and isinstance(c.get("conjectures"), list):
            n += sum(1 for s in c["conjectures"] if isinstance(s, dict) and s.get("falsifier") and s.get("followup"))
    why = rec.get("why") if isinstance(rec.get("why"), dict) else {}
    for k in ("cause", "aims"):
        if isinstance(why.get(k), list):
            n += sum(1 for s in why[k] if isinstance(s, dict) and s.get("falsifier") and s.get("followup"))
    return n


def analyze(stream):
    ok = [s for s in stream if s.get("parse_ok")]
    print(f"\n  PARSE: {len(ok)}/{len(stream)} records emitted valid JSON.")
    bad = [(s["model"], s["origin"]) for s in stream if not s.get("parse_ok")]
    if bad: print("  parse failures:", "  ".join(f"{m}({o})" for m, o in bad))

    # derive the event set from the stream (works for default OR broad rosters, and on reanalyze)
    EV = []
    _seen = set()
    for s in stream:
        if s["event"] not in _seen:
            _seen.add(s["event"]); EV.append({"id": s["event"], "title": s.get("title", s["event"]),
                                              "note": next((e["note"] for e in (EVENTS + BROAD_EVENTS) if e["id"] == s["event"]), "")})
    for ev in EV:
        print(f"\n==================== {ev['id']}: {ev['title']} ====================")
        print(f"   ({ev['note']})")
        rows = [s for s in ok if s["event"] == ev["id"]]
        for axis in AXES:
            byb = defaultdict(list)
            for s in rows:
                c = _axis_cell(s["record"], axis)
                if c and c.get("value"): byb[s["origin"]].append(str(c["value"]).strip())
            line = " | ".join(f"{b}: " + " ; ".join(sorted(set(v))[:3]) for b in ("CN", "US", "EU") if (v := byb.get(b)))
            print(f"   {axis.upper():>5}  {line[:150]}")
        # WHY-aims (the conjecture-fan) and stub synthesis
        aims = defaultdict(list)
        for s in rows:
            why = s["record"].get("why") if isinstance(s["record"].get("why"), dict) else {}
            for a in (why.get("aims") or []):
                if isinstance(a, dict) and a.get("reading"): aims[s["origin"]].append(a["reading"].strip())
        if any(aims.values()):
            print(f"   WHY.aims (conjecture-fan): " +
                  " | ".join(f"{b}: " + " ; ".join(sorted(set(v))[:2]) for b in ("CN","US","EU") if (v := aims.get(b)))[:150])
        stubs = [_stub_count(s["record"]) for s in rows]
        print(f"   STUBS synth'd (conjecture w/ falsifier+followup): total={sum(stubs)}  median/model={sorted(stubs)[len(stubs)//2] if stubs else 0}")

    print("\n==================== PER-MODEL STUB SYNTHESIS ====================")
    bym = defaultdict(list)
    for s in ok: bym[(s["model"], s["origin"])].append(_stub_count(s["record"]))
    for (m, o), xs in sorted(bym.items(), key=lambda x: (x[0][1], x[0][0])):
        print(f"   {m:>10} {o:>3} | avg stubs/record = {sum(xs)/len(xs):.1f}  (records: {len(xs)})")
    print(f"\n  wrote {OUTFILE} ({len(stream)} records)")


def selftest():
    # exercise the JSON extractor on the shapes models actually emit
    cases = [
        '{"who":{"value":"Bi Sheng","confidence":0.9,"basis":"measured","conjectures":[]}}',
        '```json\n{"who":{"value":"X"}}\n```',
        'Here is the record:\n{"who":{"value":"Y"}} -- done',
        '{"a":"has } brace in string","who":{"value":"Z"}}',
    ]
    ok = sum(1 for c in cases if extract_json(c) is not None)
    print(f"[extractor] {ok}/{len(cases)} test strings parsed")
    print(f"[probe] {len(EVENTS)} events  roster={len(ROSTER)} ({dict(Counter(o for _,_,o in ROSTER))})")
    print("SELFTEST PASS" if ok == len(cases) else "SELFTEST FAIL")
    return ok == len(cases)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--run", action="store_true")
    ap.add_argument("--pilot", action="store_true", help="1 event x roster x 1 rep, dump raw to inspect")
    ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--broad", action="store_true", help="use the 15-artefact multi-civilization roster")
    ap.add_argument("--reps", type=int, default=2); ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    if a.broad:
        EVENTS = BROAD_EVENTS
        OUTFILE = "substrate_probe_broad_run.jsonl"
    if a.selftest: selftest()
    elif a.pilot:
        if not _key(): sys.exit("no key")
        print("PILOT: E1 x roster x1 -- inspecting structured emission")
        for (name, slug, origin) in ROSTER:
            try:
                e = emit(slug, EVENTS[0]["title"])
                rec = e["record"]
                who = _axis_cell(rec, "who") if rec else None
                print(f"  {name:>10}({origin}) parse={e['parse_ok']} stubs={_stub_count(rec)} "
                      f"who.value={who.get('value') if who else None!r} who.conj={len(who.get('conjectures',[])) if who else 0}")
            except Exception as ex:
                print(f"  {name:>10}({origin}) ERR {type(ex).__name__}: {ex}")
    elif a.run: run(a.reps, a.workers)
    elif a.reanalyze:
        stream = [json.loads(l) for l in (HERE / OUTFILE).read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream)
    else: print("use --selftest | --pilot | --run [--reps N] | --reanalyze")
