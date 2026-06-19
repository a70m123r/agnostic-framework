#!/usr/bin/env python3
"""
V10b -- the IRRELEVANT-TASK / LOOKUP control (the FRAME-DISSOLUTION GRADIENT under zero compute).
This control isolates the cost of distributed computation (calculating on the path) from reading volume
and search/orienting load.

Instead of reporting the value of the computation whose final result is prime, this control asks the model
to locate a specific variable (which is the needle variable) and report its initial value.
The substrate, variables, and structure are 100% identical to V10. Only the instruction changes.
"""
import os, json, hashlib, argparse, sys, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import _chain, _is_prime, _line, _last_int, paired, MOD
from providers import solve, estimate_table, MODELS
from v10_framestrip import TASK_NAMES, FILL_NAMES, PROSE, SUBSTRATE_LINES, _filler_line, _make, _arrange, _compose

TIER = "high"            # OpenRouter cheap models cap reasoning at 'high'
MODEL = "deepseek"       # set via --model {deepseek|qwen|gemini}
CONDS = ["F3_FRAMED", "FP_POINTED", "F2_DEINDEXED", "F1_S", "F1_M", "F1_L"]


def gen_cell(cond, seed):
    st = _make(seed)
    chains, needle = st["chains"], st["needle"]
    target_var = needle["name"]
    task_lines = [_line(c) for c in chains]
    
    sel = (f"Below are several computations. Report the value that variable '{target_var}' is "
           f"initialized to on its first assignment. Output ONLY that integer.")

    if cond == "F3_FRAMED":
        body = "\n".join(task_lines)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}), listed together.\n{sel}\n\n{body}\n\nThe integer:"
    elif cond == "FP_POINTED":
        other, task_slots, total = _arrange(seed, "S", 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}) interleaved with unrelated log lines.\n{sel}\n\n{body}\n\nThe integer:"
    elif cond == "F2_DEINDEXED":
        other, task_slots, total = _arrange(seed, "S", 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"The text below is a system log.\n{sel}\n\n{body}\n\nThe integer:"
    else:  # F1_S / F1_M / F1_L
        size = cond.split("_")[1]
        other, task_slots, total = _arrange(seed, size, 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"{body}\n\n{sel}\nThe integer:"

    return {"item_id": f"V10b-{cond}-s{seed}", "cond": cond, "seed": seed,
            "target_var": target_var, "truth": needle["v0"],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def canonical_labels(items):
    keys = ("item_id", "cond", "seed", "target_var", "truth", "prompt")
    return [{k: it[k] for k in keys} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds):
    import numpy as np
    items = build_grid(seeds)
    bad = []
    for s in range(seeds):
        cells = {it["cond"]: it for it in items if it["seed"] == s}
        if len({c["truth"] for c in cells.values()}) != 1: bad.append((s, "truth (initial value) differs across conds"))
        if len({c["target_var"] for c in cells.values()}) != 1: bad.append((s, "target variable name differs across conds"))
        
        # Verify target variable exists in the prompt
        for c, it in cells.items():
            if f"'{it['target_var']}'" not in it["prompt"]:
                bad.append((s, f"{c} does not name target variable in prompt instruction"))
            if f"{it['target_var']} = {it['truth']};" not in it["prompt"]:
                bad.append((s, f"{c} does not contain target variable initialization in body"))
                
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
    (HERE / "v10b_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v10b_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "note": "V10b irrelevant-task lookup control; isolates compute cost from search/reading volume"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v10b_labels.jsonl + v10b_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v10b_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== V10b irrelevant-task: {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
    base = lambda it: {k: it[k] for k in ("item_id", "cond", "seed", "target_var", "prompt_words", "truth")}

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
    (HERE / f"v10b_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream, seeds, repeats)


def analyze(stream, seeds, repeats):
    import numpy as np
    nex = sum(1 for s in stream if s.get("exhausted"))
    print(f"\n  ({nex}/{len(stream)} exhausted; excluded from accuracy)")
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

    print("\n  V10b LOOKUP deltas (per-seed mean over reps; bootstrap CI + exact sign p):")
    delta("FP_POINTED", "F3_FRAMED", "lookup search tax in substrate WITH pointer (F3 shorter)")
    delta("F2_DEINDEXED", "FP_POINTED", "D_pointer (remove 'here they are' pointer for lookup)")
    delta("F1_S", "F2_DEINDEXED", "D_frame (remove top frame entirely for lookup)")
    delta("F1_S", "FP_POINTED", "D_total (pointer -> no frame for lookup)")
    print("  SIZE axis (search curve under zero compute):")
    delta("F1_M", "F1_S", "1x->2.5x substrate search")
    delta("F1_L", "F1_M", "2.5x->5x substrate search")
    print(f"  wrote v10b_run.{MODEL}.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--seeds", type=int, default=24); ap.add_argument("--repeats", type=int, default=4)
    ap.add_argument("--workers", type=int, default=6)
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
        stream = [json.loads(l) for l in (HERE / f"v10b_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
