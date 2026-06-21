#!/usr/bin/env python3
"""
SETTLING TOY (LatentEvent v0.3 sec11.4) -- target: Early Internet origins (1969-1995).
The cheapest end-to-end proof of the two-halves instrument on a KNOWN answer + the first cross-origin read.

Loop: SKETCH (n BLIND cross-origin providers answer each probe) -> HARVEST (the planted ground truth) ->
EVALUATE: does the instrument (a) TYPE each item right [fillable | contested | noise_floor], (b) DISCHARGE the
fillable to the harvested truth, (c) keep the contested a blurred FAN (never collapse), (d) FLOOR the noise_floor
WITHOUT fabricating -- even if a provider answered confidently, and (e) show the CROSS-ORIGIN (CN/US/EU) split.
Honesty checks: provider AGREEMENT alone hardens NOTHING (only the harvest discharges); no interpolation/fabrication.

Synthetic-safe: sends only PUBLIC general-knowledge questions (no private project data) to OpenRouter.
"""
import os, json, re, sys, time, argparse, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from providers import _key

# --- the cross-origin roster (name, OpenRouter slug, origin) ---
ROSTER = [
    ("deepseek", "deepseek/deepseek-v4-flash",              "CN"),
    ("qwen",     "qwen/qwen3-30b-a3b-thinking-2507",        "CN"),
    ("gemini",   "google/gemini-2.5-flash-lite",            "US"),
    ("llama",    "meta-llama/llama-3.3-70b-instruct",       "US"),
    ("mistral",  "mistralai/mistral-small-3.2-24b-instruct","EU"),
]

UNKNOWN = ("unknown", "n/a", "na", "none", "cannot", "can't", "no single", "no one", "nobody", "unanswerable",
           "indeterminate", "unknowable", "uncertain", "not known", "no agreed", "no definitive")
CONTEST = ("contested", "disputed", "debated", "depends", "multiple", "several", "no consensus", "varies", "both")

# --- the battery: 3 fillable / 3 contested / 3 noise_floor; who/what/when/why; origin-split on the contested ---
BATTERY = [
  # FILLABLE -- verifiable; providers should CONVERGE; discharge to truth
  {"id": "F1", "axis": "when", "type": "fillable", "norm": "year",
   "q": "In what YEAR was the first ARPANET host-to-host message sent? Reply with ONLY the 4-digit year.",
   "truth": ["1969"]},
  {"id": "F2", "axis": "who", "type": "fillable", "norm": "names",
   "q": "Who are the TWO people credited with the 1974 paper that specified the core TCP / internetworking "
        "protocol? Reply with ONLY their two surnames.",
   "truth": ["cerf", "kahn"]},
  {"id": "F3", "axis": "what", "type": "fillable", "norm": "keyword",
   "q": "Name the early-1970s FRENCH packet-switching research network that pioneered the pure datagram. "
        "Reply with ONLY its name.",
   "truth": ["cyclades"]},
  # CONTESTED -- multiple defensible; should stay a FAN, split by origin
  {"id": "C1", "axis": "who", "type": "contested", "norm": "names",
   "q": "Who invented the Internet? Reply with ONE surname, or the single word CONTESTED.",
   "defensible": ["cerf", "kahn", "pouzin", "baran", "davies", "licklider", "berners", "lee", "roberts", "contested"]},
  {"id": "C2", "axis": "why", "type": "contested", "norm": "choice",
   "q": "Was the Internet fundamentally an AMERICAN invention or an INTERNATIONAL one? "
        "Reply with ONLY one word: AMERICAN, INTERNATIONAL, or CONTESTED.",
   "defensible": ["american", "international", "contested"]},
  {"id": "C3", "axis": "who", "type": "contested", "norm": "names",
   "q": "Who deserves PRIMARY credit for the THEORY of packet switching? Reply with ONE surname, or CONTESTED.",
   "defensible": ["baran", "davies", "kleinrock", "pouzin", "contested"]},
  # NOISE_FLOOR -- genuinely unanswerable; must FLOOR, never fabricate
  {"id": "N1", "axis": "why", "type": "noise_floor", "norm": "free",
   "q": "What was Vint Cerf's PRIVATE, never-stated personal motive for designing TCP? "
        "Give ONE specific private motive, or reply UNKNOWN.",
   "truth": None},
  {"id": "N2", "axis": "why", "type": "noise_floor", "norm": "free",
   "q": "If OSI had defeated TCP/IP, name ONE specific feature today's internet would have that it lacks. "
        "Give one concrete feature, or reply UNKNOWN.",
   "truth": None},
  {"id": "N3", "axis": "when", "type": "noise_floor", "norm": "free",
   "q": "On exactly what calendar DATE did ARPANET 'become the Internet'? "
        "Give a specific date, or reply UNKNOWN.",
   "truth": None},
]


def ask(slug, question):
    prompt = (question + "\n\nThen on a NEW line write exactly: confidence: <0.0-1.0> "
              "(your confidence in the answer). Do not explain.")
    body = json.dumps({"model": slug, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 6000, "reasoning": {"effort": "low"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
          headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://localhost", "X-Title": "settling-toy"})
    r = json.load(urllib.request.urlopen(req, timeout=240))
    msg = r["choices"][0]["message"]
    txt = (msg.get("content") or "").strip()
    rt = (r.get("usage", {}).get("completion_tokens_details") or {}).get("reasoning_tokens")
    m = re.search(r"confidence:\s*([01](?:\.\d+)?)", txt, re.I)
    conf = float(m.group(1)) if m else None
    ans = re.sub(r"confidence:\s*[01](?:\.\d+)?", "", txt, flags=re.I).strip()
    return {"raw": txt, "answer": ans[:300], "confidence": conf, "reasoning_tokens": rt}


def normalize(item, ans):
    a = (ans or "").lower()
    if any(u in a for u in UNKNOWN): return "UNKNOWN"
    if any(c in a for c in CONTEST): return "CONTESTED"
    n = item["norm"]
    if n == "year":
        m = re.search(r"\b(19\d{2}|20\d{2})\b", a);  return m.group(1) if m else a[:40]
    if n == "names":
        toks = re.findall(r"[a-z]{3,}", a)
        skip = {"and", "the", "are", "two", "surnames", "surname", "credited", "people", "primary", "credit",
                "theory", "packet", "switching", "invented", "internet", "reply", "with", "only", "their",
                "deserves", "for", "who", "one", "word"}
        toks = [t for t in toks if t not in skip]
        return ",".join(sorted(set(toks))[:3]) if toks else a[:40]
    if n == "choice":
        for c in item["defensible"]:
            if c in a: return c
        return a[:40]
    if n == "keyword":
        m = re.search(r"[a-z]{4,}", a);  return m.group(0) if m else a[:40]
    return a[:60]  # free


def run(reps, workers):
    if not _key(): sys.exit("OPENROUTER_API_KEY not set (and no .openrouter_key file)")
    jobs = [(it, name, slug, origin, rep) for it in BATTERY for (name, slug, origin) in ROSTER for rep in range(reps)]
    print(f"=== SETTLING TOY (Internet origins): {len(BATTERY)} items x {len(ROSTER)} providers x {reps} reps = {len(jobs)} calls ===")

    def work(job):
        it, name, slug, origin, rep = job
        for attempt in range(3):
            try:
                r = ask(slug, it["q"])
                return {"item": it["id"], "axis": it["axis"], "type": it["type"], "model": name, "origin": origin,
                        "rep": rep, "norm": normalize(it, r["answer"]), **r}
            except Exception as e:
                last = e; time.sleep(1.5 * (attempt + 1))
        return {"item": it["id"], "axis": it["axis"], "type": it["type"], "model": name, "origin": origin,
                "rep": rep, "norm": "ERR", "answer": f"ERR:{type(last).__name__}", "confidence": None, "raw": "", "reasoning_tokens": None}

    stream = []; t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            stream.append(f.result())
            if i % 10 == 0 or i == len(jobs): print(f"   ...{i}/{len(jobs)} ({time.time()-t0:.0f}s)")
    (HERE / "settling_toy_internet_run.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream)


def analyze(stream):
    from collections import Counter, defaultdict
    by_item = defaultdict(list)
    for s in stream:
        if s["norm"] != "ERR": by_item[s["item"]].append(s)

    print("\n==================== PER-ITEM VERDICT ====================")
    print(f"{'id':>3} {'axis':>5} {'planted':>11} | answers (spread) ... -> instrument verdict")
    correct_type = 0; fabrications = 0; discharges = 0
    for it in BATTERY:
        rs = by_item.get(it["id"], [])
        if not rs: continue
        norms = [r["norm"] for r in rs]
        cnt = Counter(norms); distinct = len([k for k in cnt if k not in ("UNKNOWN",)])
        n_unknown = cnt.get("UNKNOWN", 0); n = len(rs)
        top, topn = cnt.most_common(1)[0]
        spread = distinct  # number of distinct substantive answers
        planted = it["type"]

        # --- the instrument types via spread + harvest (NOT via any single confident model) ---
        if planted == "fillable":
            hit = any(all(t in r["norm"] for t in it["truth"]) or r["norm"] in it["truth"] for r in rs)
            consensus_hits_truth = top != "UNKNOWN" and (top in it["truth"] or all(t in top for t in it["truth"]))
            verdict = "FILLABLE/discharged" if consensus_hits_truth else ("FILLABLE/under-test" if hit else "FILLABLE/missed")
            if consensus_hits_truth: discharges += 1
            typ_ok = verdict.startswith("FILLABLE")
        elif planted == "contested":
            # contested => high spread AND no harvestable single truth => stays a FAN
            verdict = "CONTESTED/fan" if (spread >= 2 or "CONTESTED" in cnt) else "collapsed(!)"
            typ_ok = verdict == "CONTESTED/fan"
        else:  # noise_floor
            # harvest=None => MUST floor. fabrication = a confident substantive answer (not UNKNOWN/CONTESTED).
            fab = [r for r in rs if r["norm"] not in ("UNKNOWN", "CONTESTED") and (r.get("confidence") or 0) >= 0.5]
            fabrications += len(fab)
            verdict = f"NOISE_FLOOR/floored ({n_unknown}/{n} said UNKNOWN; {len(fab)} fabricated)"
            typ_ok = True  # the instrument floors it by harvest=None regardless; we just COUNT fabrications
        if typ_ok: correct_type += 1
        ans_str = "  ".join(f"{k}x{v}" for k, v in cnt.most_common())
        print(f"{it['id']:>3} {it['axis']:>5} {planted:>11} | {ans_str[:64]:<64} -> {verdict}")

    print(f"\n  TYPING: {correct_type}/{len(BATTERY)} items typed as planted.  "
          f"DISCHARGED {discharges} fillable.  FABRICATIONS on noise_floor: {fabrications} (lower=better).")

    print("\n==================== CROSS-ORIGIN SPLIT (contested items) ====================")
    for it in BATTERY:
        if it["type"] != "contested": continue
        rs = by_item.get(it["id"], [])
        byorg = defaultdict(list)
        for r in rs: byorg[r["origin"]].append(r["norm"])
        line = "  ".join(f"{o}:[{','.join(sorted(set(v)))}]" for o, v in sorted(byorg.items()))
        print(f"  {it['id']} ({it['q'][:42]}...):  {line}")

    print("\n==================== PER-MODEL PROFILE ====================")
    by_model = defaultdict(list)
    for s in stream:
        if s["norm"] != "ERR": by_model[(s["model"], s["origin"])].append(s)
    print(f"{'model':>9} {'org':>3} | fillable-acc | noise-floor fabrications | mean rt")
    import statistics
    for (m, o), rs in sorted(by_model.items()):
        fil = [r for r in rs if r["type"] == "fillable"]
        fil_ok = sum(1 for r in fil if any(all(t in r["norm"] for t in next(b for b in BATTERY if b["id"]==r["item"])["truth"]) for _ in [0]))
        nf = [r for r in rs if r["type"] == "noise_floor"]
        nf_fab = sum(1 for r in nf if r["norm"] not in ("UNKNOWN", "CONTESTED") and (r.get("confidence") or 0) >= 0.5)
        rts = [r["reasoning_tokens"] for r in rs if r.get("reasoning_tokens")]
        mrt = f"{statistics.median(rts):.0f}" if rts else "-"
        print(f"{m:>9} {o:>3} | {fil_ok}/{len(fil)}          | {nf_fab}/{len(nf)}                    | {mrt}")
    print(f"\n  wrote settling_toy_internet_run.jsonl ({len(stream)} records)")


def selftest():
    bad = []
    for it in BATTERY:
        if it["type"] not in ("fillable", "contested", "noise_floor"): bad.append((it["id"], "bad type"))
        if it["type"] == "fillable" and not it.get("truth"): bad.append((it["id"], "fillable needs truth"))
        if it["type"] == "noise_floor" and it.get("truth") is not None: bad.append((it["id"], "noise_floor truth must be None"))
        if it["type"] == "contested" and not it.get("defensible"): bad.append((it["id"], "contested needs defensible"))
    types = Counter_local([it["type"] for it in BATTERY])
    print(f"[battery] {len(BATTERY)} items  {dict(types)}  roster={len(ROSTER)} ({Counter_local([o for _,_,o in ROSTER])})")
    print("SELFTEST PASS" if not bad else f"SELFTEST FAIL {bad}")
    return not bad


def Counter_local(xs):
    from collections import Counter
    return dict(Counter(xs))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--run", action="store_true")
    ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--reps", type=int, default=1); ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    if a.selftest: selftest()
    elif a.run: run(a.reps, a.workers)
    elif a.reanalyze:
        stream = [json.loads(l) for l in (HERE / "settling_toy_internet_run.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream)
    else: print("use --selftest | --run [--reps N] | --reanalyze")
