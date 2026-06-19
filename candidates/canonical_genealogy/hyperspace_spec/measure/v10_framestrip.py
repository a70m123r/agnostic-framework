#!/usr/bin/env python3
"""
V10 -- the GLOBAL-SUBSTRATE / NO-FRAME rung (the FRAME-DISSOLUTION GRADIENT). Pav's "dropped and mixed into
the random global substrate; the outside-the-frame global wrapper that's the environment." Designed via a
3-design adversarial workflow; the winning skeleton (Design 1) + grafts (size curve, anti-V7 flank, byte-
identical splice). Tests the WRAPPER SPECTRUM cell LOCUS x {DETACHED, ABSENT}.

Every prior rung handed the model a clean FRAME ("Below are 6 computations, report the prime one"). The frame
is a pre-digested wrapper: it supplies the INDEX (here they are), the SEGMENTATION (a contiguous block) and
the GOAL (stated up front). V10 dissolves the frame in steps and reads, in reasoning_tokens, the cost of the
model RE-SUPPLYING it -- ORIENTING / locating structure in raw substrate -- while holding the needle's compute
BYTE-IDENTICAL and (for the headline) the length matched.

CONDITIONS (paired by seed; the 6 task-chains -- needle + 5 non-prime distractors -- are spliced byte-identical):
  F3_FRAMED     : canonical header + the 6 chains as a contiguous indexed block (prior-rung baseline; SHORT --
                  reported with a length caveat, never the headline).
  DECOY_FRAMED  : F3 frame but padded with K extra arithmetic-shaped LABELLED lines inside the frame (the
                  anti-V7 firewall: same line-count as F2 but still FRAMED).
  F2_DEINDEXED  : de-pointered header ('somewhere in the following text are some computations') at TOP + the 6
                  chains SCATTERED among K unlabelled shape-matched value-clean filler/prose lines (the same
                  substrate as F1_S). Index removed; task still stated up front.
  F1_S/F1_M/F1_L: NO top header; the 6 chains scattered into a raw substrate (prose + filler) of growing size
                  (~1x/2.5x/5x); the task instruction moved to a single TRAILING line. The size axis is the
                  global-substrate SEARCH-curve signature.
  F0_DEINDEXED  : F2 but every line's final is GIVEN inline ('=> V') -> ZERO chain-compute (compute-free).
  F0_DISSOLVED  : F1_S but every line's final GIVEN inline -> ZERO compute.
THE DECISIVE FALSIFIER: D_frame_compute = e(F1_S)-e(F2) (with compute) vs D_frame_nocompute =
e(F0_DISSOLVED)-e(F0_DEINDEXED) (compute REMOVED, length matched). If the dissolution cost survives WITHOUT
compute, it is ORIENTING; if it vanishes, it was 'harder-to-compute-once-buried' -> the rung is a NULL.
gpt-5.5 @ xhigh (un-clipped). Synthetic data (authorized). Cite NIAH/lost-in-the-middle; V7 reading tax.
"""
import os, json, hashlib, argparse, sys, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import _chain, _is_prime, _line, _last_int, paired, MOD
from providers import solve, estimate_table, MODELS, CHEAP3

TIER = "high"            # OpenRouter cheap models cap reasoning at 'high'
MODEL = "deepseek"       # set via --model {deepseek|qwen|gemini|gpt5}
TASK_NAMES = ["alpha", "bravo", "cosmo", "delta", "echo", "foxy", "gamma", "hotel", "indi", "juno"]
FILL_NAMES = ["node", "cfgx", "bufr", "tmpv", "regq", "acc0", "idxn", "ctrl", "valu", "keyz",
              "ptrx", "segm", "blkk", "roww", "coll", "bitz", "tagg", "refp", "lenq", "mapz",
              "qz1", "qz2", "qz3", "qz4", "qz5", "qz6", "qz7", "qz8", "qz9", "qz0"]
PROSE = [
    "The deploy was rolled back after the staging smoke test flagged a latency regression.",
    "Reminder: the quarterly metrics review moves to Thursday; bring the retention deck.",
    "Cache warming now runs nightly; the cold-start tail dropped noticeably last week.",
    "We agreed to defer the schema migration until the read replicas are caught up.",
    "Onboarding copy needs a final pass before the marketing freeze on Friday.",
    "The incident postmortem is in the shared drive; action items are assigned.",
    "Vendor renewal is up next month; finance wants a usage forecast by EOW.",
    "Feature flag rollout is at twenty percent; no error-rate change observed.",
    "The design review surfaced two accessibility gaps in the new table component.",
    "Backups verified green for the third consecutive cycle; alerting unchanged.",
    "Note: the API rate limit was raised for the batch importer during the migration.",
    "Standup moved earlier so the EU team can join before their lunch.",
    "The load test plateaued around the expected ceiling; headroom looks fine.",
    "Docs for the new endpoint are drafted; awaiting a review from the platform team.",
    "We trimmed the dependency tree; the build is about a minute faster now.",
    "The customer escalation was resolved; root cause was a stale config cache.",
]
CONDS = ["F3_FRAMED", "FP_POINTED", "F2_DEINDEXED", "F1_S", "F1_M", "F1_L", "F0_DEINDEXED", "F0_DISSOLVED"]
SUBSTRATE_LINES = {"S": 24, "M": 60, "L": 120}     # non-task lines for the dissolved tiers (size axis)
K_MATCH = SUBSTRATE_LINES["S"]                     # the length-matched set uses S


def _filler_line(rng):
    """A shape-matched inert arithmetic line whose final is NON-prime (so it can't be a second needle)."""
    for _ in range(200):
        c = _chain(rng, rng.choice(FILL_NAMES))
        if not _is_prime(c["final"]):
            return c
    c["final"] = 4
    return c


def _make(seed):
    """6 task chains: exactly ONE prime (needle) + 5 distinct non-prime; all finals distinct. Byte-frozen."""
    rng = random.Random(f"V10|{seed}")
    for _ in range(8000):
        names = rng.sample(TASK_NAMES, 6)
        chains = [_chain(rng, nm) for nm in names]
        if len({c["final"] for c in chains}) != 6:
            continue
        primes = [c for c in chains if _is_prime(c["final"])]
        if len(primes) != 1:
            continue
        needle = primes[0]
        return {"chains": chains, "needle": needle}
    raise RuntimeError(f"no V10 structure for seed {seed}")


def _line0(c):
    """compute-free variant: the chain line with its final GIVEN inline (zero arithmetic on the path)."""
    return _line(c) + f"  =>  {c['final']}"


SELECTOR = ("Report the value of the ONE computation whose final result is a PRIME number. "
            "Output ONLY that integer.")
SELECTOR0 = ("Each line below shows a computation and its final result after '=>'. Report the value of the ONE "
             "whose final result is a PRIME number. Output ONLY that integer.")


def _substrate(rng, n_lines, compute_free=False):
    """n_lines of raw global substrate: a deterministic prose + inert-arithmetic mix (no prime finals).
    When compute_free, the arithmetic FILLER lines ALSO get their final given inline (=>) so F0 is TRULY
    compute-free -- no unevaluated arithmetic anywhere (the codex-audit fix: previously only the 6 task lines
    got '=>', leaving ~11 filler lines computable, so the F0 falsifier wasn't actually compute-free)."""
    out = []
    for i in range(n_lines):
        if rng.random() < 0.5:
            out.append(rng.choice(PROSE))
        else:
            c = _filler_line(rng)
            out.append(_line0(c) if compute_free else _line(c))
    return out


def _arrange(seed, size, n_task, compute_free=False):
    """deterministic substrate + scatter positions for (seed,size); shared layout across the conds of that
    size; compute_free toggles the '=>' rendering of ALL arithmetic lines (F0 vs the compute conditions)."""
    other = _substrate(random.Random(f"V10sub|{seed}|{size}"), SUBSTRATE_LINES[size], compute_free)
    total = n_task + len(other)
    slots = list(range(total)); random.Random(f"V10scat|{seed}|{size}").shuffle(slots)
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
    compute_free = cond.startswith("F0")
    line_fn = _line0 if compute_free else _line
    task_lines = [line_fn(c) for c in chains]
    sel = SELECTOR0 if compute_free else SELECTOR

    if cond == "F3_FRAMED":
        body = "\n".join(task_lines)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}), listed together.\n{sel}\n\n{body}\n\nThe integer:"
    elif cond == "FP_POINTED":     # index PRESENT: same substrate as F2 but the header points ("here they are")
        other, task_slots, total = _arrange(seed, "S", 6)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"Below are 6 computations (arithmetic mod {MOD}) interleaved with unrelated log lines.\n{sel}\n\n{body}\n\nThe integer:"
    elif cond in ("F2_DEINDEXED", "F0_DEINDEXED"):     # index WEAKENED: no count, framed only as a log
        other, task_slots, total = _arrange(seed, "S", 6, compute_free)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"The text below is a system log.\n{sel}\n\n{body}\n\nThe integer:"
    else:  # F1_S / F1_M / F1_L / F0_DISSOLVED -- no top header; trailing instruction
        size = "S" if cond == "F0_DISSOLVED" else cond.split("_")[1]
        other, task_slots, total = _arrange(seed, size, 6, compute_free)
        body = _compose(task_lines, other, task_slots, total)
        prompt = f"{body}\n\n{sel}\nThe integer:"

    needle_line = line_fn(needle)
    return {"item_id": f"V10-{cond}-s{seed}", "cond": cond, "seed": seed,
            "compute_free": compute_free, "truth": needle["final"],
            "needle_line_hash": hashlib.sha256(needle_line.encode()).hexdigest()[:16],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def _oracle(seed):
    """independent ground truth: the unique prime final among the 6 task chains."""
    st = _make(seed)
    pr = [c["final"] for c in st["chains"] if _is_prime(c["final"])]
    assert len(pr) == 1
    return pr[0]


def canonical_labels(items):
    keys = ("item_id", "cond", "seed", "compute_free", "truth", "needle_line_hash", "prompt")
    return [{k: it[k] for k in keys} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds):
    import numpy as np
    items = build_grid(seeds)
    bad = []
    for s in range(seeds):
        cells = {it["cond"]: it for it in items if it["seed"] == s}
        if len({c["truth"] for c in cells.values()}) != 1: bad.append((s, "truth differs across conds"))
        if cells["F3_FRAMED"]["truth"] != _oracle(s): bad.append((s, "truth != oracle"))
        if not _is_prime(cells["F3_FRAMED"]["truth"]): bad.append((s, "truth not prime"))
        # byte-identical needle within the compute group and within the no-compute group
        comp_hashes = {cells[c]["needle_line_hash"] for c in ("F3_FRAMED", "FP_POINTED", "F2_DEINDEXED", "F1_S", "F1_M", "F1_L")}
        if len(comp_hashes) != 1: bad.append((s, "needle line not byte-identical across compute conds"))
        if cells["F0_DEINDEXED"]["needle_line_hash"] != cells["F0_DISSOLVED"]["needle_line_hash"]: bad.append((s, "F0 needle mismatch"))
        # F0 must be TRULY compute-free: NO arithmetic line (containing '%') may lack a given '=>' final
        for c in ("F0_DEINDEXED", "F0_DISSOLVED"):
            nbad = sum(1 for ln in cells[c]["prompt"].split("\n") if "%" in ln and "=>" not in ln)
            if nbad: bad.append((s, f"{c} has {nbad} compute lines without => (NOT compute-free)"))
        # exactly ONE prime-final line in each condition's body (no filler/decoy second needle)
        for c, it in cells.items():
            n_prime = _count_prime_lines(it["prompt"])
            if n_prime != 1: bad.append((s, f"{c} has {n_prime} prime lines"))
    clean = seeds - len({b[0] for b in bad})
    print(f"[integrity] {clean}/{seeds} seeds clean", "OK" if not bad else f"FAIL {bad[:6]}")
    by = {}
    for it in items: by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        print(f"   {c:>12}: n={len(by[c])}  median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    matched = ["FP_POINTED", "F2_DEINDEXED", "F1_S", "F0_DEINDEXED", "F0_DISSOLVED"]
    mw = [np.median([it["prompt_words"] for it in by[c]]) for c in matched]
    print(f"   length-matched set {matched}: words span {min(mw):.0f}-{max(mw):.0f} (drift {100*(max(mw)-min(mw))/np.mean(mw):.0f}%)")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")
    return not bad


def _count_prime_lines(prompt):
    """count body lines that look like a chain AND whose final integer is prime (the needle-detector)."""
    import re
    n = 0
    for ln in prompt.split("\n"):
        if "=" not in ln or "%" not in ln and "=>" not in ln:
            continue
        if "=>" in ln:                              # compute-free: final after =>
            m = re.search(r"=>\s*(\d+)", ln)
            if m and _is_prime(int(m.group(1))): n += 1
        else:                                       # compute line: replay to get the final
            v = _replay(ln)
            if v is not None and _is_prime(v): n += 1
    return n


def _replay(ln):
    """re-evaluate a rendered chain line 'name = v0; name = (name op c) % MOD; ...' -> final, else None."""
    import re
    m = re.match(r"\s*(\w+) = (\d+);", ln)
    if not m: return None
    v = int(m.group(2))
    for op, c in re.findall(r"\(\w+ ([+\-*]) (\d+)\)", ln):
        v = {"+": v + int(c), "-": v - int(c), "*": v * int(c)}[op] % MOD
    return v


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v10fs_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v10fs_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "substrate_lines": SUBSTRATE_LINES,
         "note": "V10 frame-dissolution gradient; headline D_frame=e(F1_S)-e(F2) length-matched; falsifier F0_DISSOLVED-F0_DEINDEXED (compute-free)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v10fs_labels.jsonl + v10fs_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v10fs_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== V10 frame-strip: {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
    base = lambda it: {k: it[k] for k in ("item_id", "cond", "seed", "compute_free", "prompt_words", "truth")}

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
    (HERE / f"v10fs_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
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

    print("\n  FRAME-DISSOLUTION deltas (per-seed mean over reps; bootstrap CI + exact sign p):")
    delta("FP_POINTED", "F3_FRAMED", "cost of scattering into substrate WITH a pointer (F3 shorter -> length caveat)")
    delta("F2_DEINDEXED", "FP_POINTED", "D_pointer (remove the 'here they are' pointer, LENGTH-MATCHED)")
    delta("F1_S", "F2_DEINDEXED", "D_frame HEADLINE (remove the top-frame entirely, LENGTH-MATCHED)")
    delta("F1_S", "FP_POINTED", "D_total (pointer -> no frame, length-matched)")
    print("  SIZE axis (global-substrate search curve):")
    delta("F1_M", "F1_S", "1x->2.5x substrate")
    delta("F1_L", "F1_M", "2.5x->5x substrate")
    print("  THE FALSIFIER (compute REMOVED, length-matched):")
    delta("F0_DISSOLVED", "F0_DEINDEXED", "D_frame_NOCOMPUTE -- >0 => cost is ORIENTING not harder-compute")
    print("\n  VERDICT logic: D_frame>0 AND D_frame_NOCOMPUTE>0 AND size-slope>0 AND anti-V7>0 => the camera "
          "photographs a real ORIENTING/framing cost (re-supplying the missing wrapper). Any null demotes per kill-criteria.")
    print(f"  wrote v10fs_run.{MODEL}.jsonl ({len(stream)} records)")


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
        stream = [json.loads(l) for l in (HERE / f"v10fs_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
