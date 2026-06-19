#!/usr/bin/env python3
"""
SV -- the SAME-TASK, application-free VERDICT control (codex's named next control for the V10/V10b half).

V10b's lookup demoted V10's "reading-volume" claim, but both audits flagged the confound (C6): V10's compute-free
F0 still APPLIED primality ("which final is prime?"), while V10b's lookup REMOVED application by switching the
TASK entirely (report a named variable's init value) -- a different objective, search key, and answer target.
So V10-F0 vs V10b is not a clean subtraction.

SV removes predicate application WITHOUT switching the task: every computation line is pre-tagged with its
[verdict: PASS/fail] (exactly one PASS = the unique prime), and the task stays "report the value of the ONE
computation whose verdict is PASS" -- same answer target (a computation's final value), same "which special
computation" framing as the V10 prime task, minus the primality work. The size axis (S/M/L filler, all tagged
'fail') supplies calibrated above-floor scanning load (fixes the C4 floor critique).

Conds mirror V10/V10b EXACTLY (F3_FRAMED, FP_POINTED, F2_DEINDEXED, F1_S, F1_M, F1_L) so the 3-way is matched:
  V10  prime  = apply predicate         (rt = APPLICATION + locate + read)
  V10b lookup = different task           (rt = locate-by-name + read)        <- changes the task
  SV   verdict = same task, no apply     (rt = locate-by-PASS + read)        <- clean application removal
D_application = rt(V10 prime) - rt(SV verdict) at matched cond = the cost of APPLYING primality, task held fixed.
If SV's frame/size deltas are ~0 -> the V10 frame/size cost needed application. If they survive -> an
application-independent orienting/scan cost exists. Compute-free; finals + verdicts both given.
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
CONDS = ["F3_FRAMED", "FP_POINTED", "F2_DEINDEXED", "F1_S", "F1_M", "F1_L"]

SEL = ("Each computation line ends with its final result after '=>' and a [verdict] tag. Exactly one verdict "
       "is PASS. Report the value of the ONE computation whose verdict is PASS. Output ONLY that integer.")


def _vline(c, verdict):
    return _line0(c) + f"   [verdict: {verdict}]"


def _sub(seed, size):
    """deterministic prose + verdict-tagged filler (all 'fail'; filler finals are non-prime by construction)."""
    rng = random.Random(f"SVsub|{seed}|{size}")
    out = []
    for _ in range(SUBSTRATE_LINES[size]):
        if rng.random() < 0.5:
            out.append(rng.choice(PROSE))
        else:
            out.append(_vline(_filler_line(rng), "fail"))
    return out


def _arrange(seed, size, n_task):
    other = _sub(seed, size)
    total = n_task + len(other)
    slots = list(range(total)); random.Random(f"SVscat|{seed}|{size}").shuffle(slots)
    return other, set(slots[:n_task]), total


def _compose(task_lines, other, task_slots, total):
    out, ti, oi = [], 0, 0
    for i in range(total):
        if i in task_slots:
            out.append(task_lines[ti]); ti += 1
        else:
            out.append(other[oi]); oi += 1
    return "\n".join(out)


def gen_cell(cond, seed):
    st = _make(seed)
    chains, needle = st["chains"], st["needle"]
    task_lines = [_vline(c, "PASS" if c is needle else "fail") for c in chains]

    if cond == "F3_FRAMED":
        body = "\n".join(task_lines)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}), listed together.\n{SEL}\n\n{body}\n\nThe integer:"
    elif cond == "FP_POINTED":
        other, task_slots, total = _arrange(seed, "S", 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}) interleaved with unrelated log lines.\n{SEL}\n\n{body}\n\nThe integer:"
    elif cond == "F2_DEINDEXED":
        other, task_slots, total = _arrange(seed, "S", 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"The text below is a system log.\n{SEL}\n\n{body}\n\nThe integer:"
    else:  # F1_S / F1_M / F1_L -- no top header; trailing instruction
        size = cond.split("_")[1]
        other, task_slots, total = _arrange(seed, size, 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"{body}\n\n{SEL}\nThe integer:"

    needle_line = _vline(needle, "PASS")
    return {"item_id": f"SV-{cond}-s{seed}", "cond": cond, "seed": seed,
            "truth": needle["final"], "needle_line_hash": hashlib.sha256(needle_line.encode()).hexdigest()[:16],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def _oracle(seed):
    st = _make(seed)
    pr = [c["final"] for c in st["chains"] if _is_prime(c["final"])]
    assert len(pr) == 1
    return pr[0]


def canonical_labels(items):
    keys = ("item_id", "cond", "seed", "truth", "needle_line_hash", "prompt")
    return [{k: it[k] for k in keys} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds):
    import numpy as np
    items = build_grid(seeds)
    bad = []
    for s in range(seeds):
        cells = {it["cond"]: it for it in items if it["seed"] == s}
        if len({c["truth"] for c in cells.values()}) != 1: bad.append((s, "truth differs"))
        if cells["F3_FRAMED"]["truth"] != _oracle(s): bad.append((s, "truth != oracle"))
        if not _is_prime(cells["F3_FRAMED"]["truth"]): bad.append((s, "truth not prime"))
        if len({cells[c]["needle_line_hash"] for c in CONDS}) != 1: bad.append((s, "needle line not byte-identical"))
        for c, it in cells.items():
            if it["prompt"].count("[verdict: PASS]") != 1: bad.append((s, f"{c} not exactly one PASS"))
            nbad = sum(1 for ln in it["prompt"].split("\n") if "%" in ln and "=>" not in ln)
            if nbad: bad.append((s, f"{c} has {nbad} compute lines without => (not application-free)"))
    clean = seeds - len({b[0] for b in bad})
    print(f"[integrity] {clean}/{seeds} seeds clean", "OK" if not bad else f"FAIL {bad[:6]}")
    by = {}
    for it in items: by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        print(f"   {c:>12}: n={len(by[c])}  median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")
    return not bad


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v_sv_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v_sv_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "note": "SV same-task application-free verdict control; D_application = V10 prime - SV verdict (task held fixed)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v_sv_labels.jsonl + v_sv_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v_sv_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== SV verdict (application-free, same task): {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
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
    (HERE / f"v_sv_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
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
        print(f"    {c:>12}:  {acc}/{len(done)}        {md:.0f} / {mn:.0f}            {np.median(pt) if pt else float('nan'):.0f}")

    sids = sorted({s["seed"] for s in stream})
    def mt(c, sd):
        v = [s["reasoning_tokens"] for s in stream if s["cond"] == c and s["seed"] == sd
             and s["correct"] and s["reasoning_tokens"] is not None]
        return float(np.mean(v)) if v else None
    def delta(a, b, why):
        d = [mt(a, sd) - mt(b, sd) for sd in sids if None not in (mt(a, sd), mt(b, sd))]
        r = paired(d)
        print(f"     {a:>12} - {b:<12} {r[0]:+8.1f}  CI[{r[1][0]:+.0f},{r[1][1]:+.0f}]  p={r[2]:.3f}  (n={r[5]})   {why}" if r else f"     {a}-{b}  n/a   {why}")

    print("\n  SV deltas -- does frame/size cost SURVIVE with application removed (same task)?")
    delta("F1_S", "F2_DEINDEXED", "D_frame (remove top frame), application-free, same task")
    delta("F2_DEINDEXED", "FP_POINTED", "D_pointer, application-free")
    print("  SIZE axis (above-floor scan curve, application removed):")
    delta("F1_M", "F1_S", "1x->2.5x substrate (verdict-scan)")
    delta("F1_L", "F1_M", "2.5x->5x substrate (verdict-scan)")
    print("  (cross-experiment D_application = V10 prime - SV verdict at matched cond -> run compare_3way.py)")
    print(f"  wrote v_sv_run.{MODEL}.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--seeds", type=int, default=24); ap.add_argument("--repeats", type=int, default=4)
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
        stream = [json.loads(l) for l in (HERE / f"v_sv_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
