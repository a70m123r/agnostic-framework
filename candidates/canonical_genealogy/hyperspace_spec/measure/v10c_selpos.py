#!/usr/bin/env python3
"""
V10c -- the SELECTOR-POSITION 2x2, the control named by FOUR independent auditors (V10b's codex+Claude,
NF/SV's codex+Claude). It splits the surviving application-independent frame cost (SV D_frame +113/+372/+405)
into ORIENTING (header) vs LATE-INSTRUCTION RESCAN (selector position) -- the one confound the whole frame
component still rides on.

Design (all four cells share a BYTE-IDENTICAL body per seed; application-free; above-floor):
  HEADER:   present ("The text below is a system log.")  vs  absent (a word-count-matched NEUTRAL pad)
  POSITION: selector LEADING (before body)               vs  TRAILING (after body)
  H_LEAD, H_TRAIL, N_LEAD, N_TRAIL.
The task is a pure NEUTRAL-MARKER locate (codex's fix so qwen cannot read the tag as "verify the arithmetic"):
every computation line carries [tag: KEEP|drop], exactly one KEEP (the needle); report its '=>' value. No
predicate application. Finals given.

POSITION main effect = mean(*_TRAIL) - mean(*_LEAD) is PERFECTLY length-matched (same tokens reordered) -> the
cleanest contrast. HEADER main effect = mean(N_*) - mean(H_*) with position held (H/N word-matched within 1).
Reconnect: H_LEAD ~ V10 F2_DEINDEXED (header+leading); N_TRAIL ~ F1_S (no-header+trailing); so
(N_TRAIL - H_LEAD) = HEADER + POSITION + interaction should reproduce SV's D_frame and DECOMPOSE it.
KILL: POSITION swamps & HEADER CI includes 0 -> the frame cost is late-rescan, orienting demotes (DC-39 dies).
     HEADER significant with position held -> orienting survives, sharpened.
"""
import os, json, hashlib, argparse, sys, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import _is_prime, _last_int, paired, MOD
from v10_framestrip import _make, _line0, _filler_line, PROSE, SUBSTRATE_LINES
from providers import solve, estimate_table, MODELS

TIER = "high"
MODEL = "deepseek"
CONDS = ["H_LEAD", "H_TRAIL", "N_LEAD", "N_TRAIL", "Z_LEAD", "Z_TRAIL"]
SIZE = "S"                                                # one size class (above the locate floor at ~24 lines)
HEADER = "The text below is a system log."                # H: 7 words -- the orienting content-frame
NEUTRAL = "Several notes were filed during the cycle."    # N: 7 words -- a neutral sentence (no orienting frame)
#                                                           Z: TRUE-ABSENT -- no first line at all (codex's bridge
#                                                           arm). H vs N vs Z separates header-HELPS from
#                                                           neutral-line-HURTS: Z~H & N higher => neutral hurts;
#                                                           Z~N & H lower => header orients; Z between => both.
SEL = ("Exactly one line is tagged [tag: KEEP]. Report the value shown after '=>' on that line. "
       "Output ONLY that integer.")


def _tline(c, tag):
    return _line0(c) + f"   [tag: {tag}]"


def _body(seed):
    """byte-identical scattered substrate per seed: 6 task lines (needle=KEEP, rest=drop) + prose + tagged
    filler (all drop). Composed ONCE; reused across all 4 cells so only the wrapper (header/position) varies."""
    st = _make(seed)
    chains, needle = st["chains"], st["needle"]
    task_lines = [_tline(c, "KEEP" if c is needle else "drop") for c in chains]
    rng = random.Random(f"V10Csub|{seed}|{SIZE}")
    other = []
    for _ in range(SUBSTRATE_LINES[SIZE]):
        if rng.random() < 0.5:
            other.append(rng.choice(PROSE))
        else:
            other.append(_tline(_filler_line(rng), "drop"))
    total = len(task_lines) + len(other)
    slots = list(range(total)); random.Random(f"V10Cscat|{seed}|{SIZE}").shuffle(slots)
    task_slots = set(slots[:len(task_lines)])
    out, ti, oi = [], 0, 0
    for i in range(total):
        if i in task_slots:
            out.append(task_lines[ti]); ti += 1
        else:
            out.append(other[oi]); oi += 1
    return "\n".join(out), needle["final"], _tline(needle, "KEEP")


def gen_cell(cond, seed):
    body, truth, needle_line = _body(seed)
    head = {"H": HEADER, "N": NEUTRAL, "Z": None}[cond[0]]
    if cond.endswith("LEAD"):
        prompt = (f"{head}\n{SEL}\n\n{body}\n\nThe integer:" if head is not None
                  else f"{SEL}\n\n{body}\n\nThe integer:")
    else:  # TRAIL
        prompt = (f"{head}\n\n{body}\n\n{SEL}\nThe integer:" if head is not None
                  else f"{body}\n\n{SEL}\nThe integer:")
    return {"item_id": f"V10c-{cond}-s{seed}", "cond": cond, "seed": seed, "truth": truth,
            "body_hash": hashlib.sha256(body.encode()).hexdigest()[:16],
            "needle_line_hash": hashlib.sha256(needle_line.encode()).hexdigest()[:16],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def canonical_labels(items):
    keys = ("item_id", "cond", "seed", "truth", "body_hash", "needle_line_hash", "prompt")
    return [{k: it[k] for k in keys} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds):
    import numpy as np
    items = build_grid(seeds)
    bad = []
    if abs(len(HEADER.split()) - len(NEUTRAL.split())) > 1:
        bad.append((-1, f"HEADER/NEUTRAL word mismatch {len(HEADER.split())} vs {len(NEUTRAL.split())}"))
    for s in range(seeds):
        cells = {it["cond"]: it for it in items if it["seed"] == s}
        if len({c["truth"] for c in cells.values()}) != 1: bad.append((s, "truth differs"))
        if len({c["body_hash"] for c in cells.values()}) != 1: bad.append((s, "body NOT byte-identical across cells"))
        if len({c["needle_line_hash"] for c in cells.values()}) != 1: bad.append((s, "needle line not byte-identical"))
        body_s, _, _ = _body(s)                                  # the shared body -- count KEEP here (not in the selector)
        if body_s.count("[tag: KEEP]") != 1: bad.append((s, f"body has {body_s.count('[tag: KEEP]')} KEEP lines"))
        for c, it in cells.items():
            nbad = sum(1 for ln in it["prompt"].split("\n") if "%" in ln and "=>" not in ln)
            if nbad: bad.append((s, f"{c} has {nbad} compute lines without => (not application-free)"))
        # POSITION must be perfectly length-matched within each header level (H, N, Z)
        for lvl in ("H", "N", "Z"):
            if cells[f"{lvl}_LEAD"]["prompt_words"] != cells[f"{lvl}_TRAIL"]["prompt_words"]:
                bad.append((s, f"{lvl} pos length drift"))
    clean = seeds - len({b[0] for b in bad if b[0] >= 0})
    print(f"[integrity] {clean}/{seeds} seeds clean", "OK" if not bad else f"FAIL {bad[:6]}")
    by = {}
    for it in items: by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        print(f"   {c:>8}: n={len(by[c])}  median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    print(f"   HEADER={len(HEADER.split())}w  NEUTRAL={len(NEUTRAL.split())}w  Z=true-absent (~{len(HEADER.split())}w shorter, <1% of prompt)")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")
    return not bad


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v10c_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v10c_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "note": "V10c selector-position 2x2 (header x position), neutral marker, byte-identical body; POSITION perfectly length-matched"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v10c_labels.jsonl + v10c_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v10c_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== V10c selector-position 2x2: {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
    base = lambda it: {k: it[k] for k in ("item_id", "cond", "seed", "prompt_words", "truth")}

    def work(job):
        it, rep = job
        err = None
        for attempt in range(3):
            try:
                r = solve(it["prompt"], model=MODEL); got = _last_int(r["content"])
                return {**base(it), "model": MODEL, "rep": rep, "got": got,
                        "correct": (got == it["truth"]), "exhausted": False, **r}
            except Exception as e:
                err = e; time.sleep(1.5 * (attempt + 1))
        return {**base(it), "model": MODEL, "rep": rep, "got": None, "correct": False, "exhausted": True,
                "content": "", "finish": f"ERR:{type(err).__name__}", "reasoning_tokens": None,
                "completion_tokens": None, "prompt_tokens": None, "seconds": None}

    stream = []; t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            stream.append(f.result())
            if i % 40 == 0 or i == len(jobs):
                print(f"   ...{i}/{len(jobs)} done ({time.time()-t0:.0f}s)")
    (HERE / f"v10c_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream, seeds, repeats)


def analyze(stream, seeds, repeats):
    import numpy as np
    nex = sum(1 for s in stream if s.get("exhausted"))
    print(f"\n  ({nex}/{len(stream)} exhausted; excluded)")
    print(f"  by condition:   acc(completed)   median / MEAN rt(correct)   median prompt_tokens")
    for c in CONDS:
        done = [s for s in stream if s["cond"] == c and not s.get("exhausted")]
        if not done: continue
        acc = sum(1 for s in done if s["correct"])
        tk = [s["reasoning_tokens"] for s in done if s["correct"] and s["reasoning_tokens"] is not None]
        pt = [s["prompt_tokens"] for s in done if s["prompt_tokens"]]
        md = np.median(tk) if tk else float('nan'); mn = np.mean(tk) if tk else float('nan')
        print(f"    {c:>8}:  {acc}/{len(done)}        {md:.0f} / {mn:.0f}            {np.median(pt) if pt else float('nan'):.0f}")

    sids = sorted({s["seed"] for s in stream})
    def mt(c, sd):
        v = [s["reasoning_tokens"] for s in stream if s["cond"] == c and s["seed"] == sd
             and s["correct"] and s["reasoning_tokens"] is not None]
        return float(np.mean(v)) if v else None

    def comp(fn, why):
        d = []
        for sd in sids:
            vals = {c: mt(c, sd) for c in CONDS}
            if any(v is None for v in vals.values()):
                continue
            d.append(fn(vals))
        r = paired(d)
        print(f"     {why:<46} {r[0]:+8.1f}  CI[{r[1][0]:+.0f},{r[1][1]:+.0f}]  p={r[2]:.3f}  (n={r[5]})" if r else f"     {why}  n/a")

    H = lambda v: (v["H_LEAD"] + v["H_TRAIL"]) / 2
    N = lambda v: (v["N_LEAD"] + v["N_TRAIL"]) / 2
    Z = lambda v: (v["Z_LEAD"] + v["Z_TRAIL"]) / 2
    print("\n  V10c MAIN EFFECTS (per-seed; bootstrap CI + exact sign p):")
    comp(lambda v: (v["H_TRAIL"] + v["N_TRAIL"] + v["Z_TRAIL"]) / 3 - (v["H_LEAD"] + v["N_LEAD"] + v["Z_LEAD"]) / 3,
         "POSITION (trailing-leading) -- LATE-RESCAN [length-matched, over 3 levels]")
    comp(lambda v: N(v) - H(v), "N - H  (neutral sentence vs system-log frame)")
    print("  THE Z BRIDGE (codex's true-absent arm -- separates header-HELPS from neutral-line-HURTS):")
    comp(lambda v: Z(v) - H(v), "Z - H  (true-absent vs frame; ~0 => frame doesn't help vs nothing)")
    comp(lambda v: N(v) - Z(v), "N - Z  (neutral sentence vs true-absent; >0 => the neutral line HURTS)")
    print("  VERDICT: POSITION null on the panel => NOT late-rescan. Then on the 3-way: "
          "Z~H & N>both => neutral-line-HURTS (orienting NOT shown); Z~N & H<both => header ORIENTS; Z between => both.")
    print(f"  wrote v10c_run.{MODEL}.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--seeds", type=int, default=40); ap.add_argument("--repeats", type=int, default=4)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--model", default="deepseek", choices=list(MODELS))
    ap.add_argument("--estimate", action="store_true")
    a = ap.parse_args()
    MODEL = a.model
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    elif a.estimate:
        prompts = [it["prompt"] for it in build_grid(a.seeds)]
        estimate_table(prompts, a.repeats)
    elif a.run:
        from providers import _key
        if not _key(): sys.exit("OPENROUTER_API_KEY not set (and no .openrouter_key file)")
        run(a.seeds, a.repeats, a.workers)
    elif a.reanalyze:
        stream = [json.loads(l) for l in (HERE / f"v10c_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
