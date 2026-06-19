#!/usr/bin/env python3
"""
V11 -- the MEANING / KNOWLEDGE rung (de-amortization). The deepest column of the WRAPPER SPECTRUM and the
first to touch the BUILD clock: every prior rung let the model get the selection concept ("prime") for FREE
from training (amortized). V11 swaps it for a NOVEL in-prompt predicate co-designed to select the EXACT same
needle, and reads -- in reasoning_tokens -- the cost of the model RE-PAYING a concept the frame used to
supply pre-paid. Designed via the white-space design workflow; the build-first winner (Cell A).

The trick: per seed, the needle is BOTH the unique prime AND the unique line whose digit-sum equals a target
S. So "prime" (known) and "digit-sum == S" (novel) pick the IDENTICAL singleton; the answer integer is the
same in every arm; only the SELECTION CONCEPT's amortization changes. LOCUS/SEGMENTATION/FORMAT/TASK-IDENTITY
are all held pristine (a clean contiguous 6-line framed block in every arm) -- ONLY meaning moves.

CONDITIONS (needle byte-identical across all; reuses v10's _line0 compute-free renderer):
  NAMED_BARE    : the V4-V10 floor -- "the ONE whose result is a PRIME number" (prime fully amortized).
  NAMED_DEF     : + a definition block of the KNOWN concept (length-matched to NOVEL). prime still pre-paid.
  RENAMED_PRIME : the SAME primality predicate under a NONCE name ("FLONK iff >=2 and no divisor but 1/itself")
                  -- de-amortizes only the NAME (bind a nonce to a known computation).
  NOVEL_RULE    : a genuinely made-up predicate, no pre-paid concept ("ZILP iff its 3 zero-padded digits sum
                  to S"), selecting the identical needle -- the concept must be HELD + APPLIED in working memory.
  F0_NAMED_DEF  : NAMED_DEF, COMPUTE-FREE -- finals given inline + a PASS/fail verdict per line (no predicate
                  to evaluate; just read the PASS line). The falsifier floor for the known concept.
  F0_NOVEL_RULE : NOVEL_RULE, compute-free -- identical verdict-table format; differs from F0_NAMED_DEF ONLY
                  in the (now-vestigial) definition word. The decisive null-router.

PRIMARY contrasts (paired by seed, correct calls only, @ xhigh):
  (1) HEADLINE de-amortization  e(NOVEL_RULE) - e(NAMED_DEF)   -- cost of an UN-amortized selection concept.
  (2) NAME-only                 e(RENAMED_PRIME) - e(NAMED_DEF) -- retrieve-by-name vs bind-a-nonce.
  (3) DEFINITION-presence       e(NAMED_DEF) - e(NAMED_BARE)    -- carrying a def of a KNOWN concept (~reading).
  (4) THE FALSIFIER             e(F0_NOVEL_RULE) - e(F0_NAMED_DEF) -- compute removed both sides, length matched:
      if the headline SURVIVES here it was definition-READING (confound) -> demote; if it VANISHES while (1)>0,
      the delta is genuine concept-APPLICATION de-amortization (the missing MEANING wrapper).
gpt-5.5 @ xhigh. Synthetic data (authorized). Cite OverThink 2502.02542 (effort), the amortization principle.
"""
import os, json, hashlib, argparse, sys, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import _chain, _is_prime, _line, _last_int, paired, MOD
from v10_framestrip import _line0
from providers import solve, estimate_table, MODELS, CHEAP3

TIER = "high"            # OpenRouter cheap models cap reasoning at 'high'
MODEL = "deepseek"       # set via --model {deepseek|qwen|gemini|gpt5}
TASK_NAMES = ["alpha", "bravo", "cosmo", "delta", "echo", "foxy", "gamma", "hotel", "indi", "juno"]
CONDS = ["NAMED_BARE", "NAMED_DEF", "RENAMED_PRIME", "NOVEL_RULE", "F0_NAMED_DEF", "F0_NOVEL_RULE"]

DEF_PRIME = "Call a number {W} iff it is an integer at least 2 whose only positive divisors are 1 and the number itself."
DEF_NOVEL = "Call a number {W} iff its three zero-padded decimal digits add up to exactly {S}, a fixed chosen target."


def _dsum(v):
    return sum(int(d) for d in f"{v:03d}")


def _make(seed):
    """6 chains, all-distinct finals, EXACTLY one prime (needle), AND the needle's digit-sum S is UNIQUE among
    the 6 -> 'prime' and 'digit-sum==S' select the IDENTICAL singleton (the needle)."""
    rng = random.Random(f"V11|{seed}")
    for _ in range(20000):
        names = rng.sample(TASK_NAMES, 6)
        chains = [_chain(rng, nm) for nm in names]
        finals = [c["final"] for c in chains]
        if len(set(finals)) != 6:
            continue
        primes = [c for c in chains if _is_prime(c["final"])]
        if len(primes) != 1:
            continue
        needle = primes[0]
        S = _dsum(needle["final"])
        if sum(1 for f in finals if _dsum(f) == S) != 1:     # needle's digit-sum must be unique
            continue
        return {"chains": chains, "needle": needle, "S": S}
    raise RuntimeError(f"no V11 structure for seed {seed}")


def _selector(W):
    return f"Report the value of the ONE computation whose final result is {W}. Output ONLY that integer."


def _verdict_body(chains, predicate):
    """compute-free body: each line shows the computation, its final (=> V), and a PASS/fail verdict."""
    return "\n".join(_line0(c) + f"   [verdict: {'PASS' if predicate(c['final']) else 'fail'}]" for c in chains)


def gen_cell(cond, seed):
    st = _make(seed)
    chains, needle, S = st["chains"], st["needle"], st["S"]
    rng = random.Random(f"V11ord|{seed}")
    order = list(chains); rng.shuffle(order)         # one shared display order per seed
    head = f"Below are 6 computations (arithmetic mod {MOD}), listed together."

    if cond == "NAMED_BARE":
        body = "\n".join(_line(c) for c in order)
        prompt = f"{head}\nReport the value of the ONE computation whose final result is a PRIME number. Output ONLY that integer.\n\n{body}\n\nThe integer:"
    elif cond == "NAMED_DEF":
        body = "\n".join(_line(c) for c in order)
        prompt = f"{head}\n{DEF_PRIME.format(W='PRIME')}\n{_selector('PRIME')}\n\n{body}\n\nThe integer:"
    elif cond == "RENAMED_PRIME":
        body = "\n".join(_line(c) for c in order)
        prompt = f"{head}\n{DEF_PRIME.format(W='FLONK')}\n{_selector('FLONK')}\n\n{body}\n\nThe integer:"
    elif cond == "NOVEL_RULE":
        body = "\n".join(_line(c) for c in order)
        prompt = f"{head}\n{DEF_NOVEL.format(W='ZILP', S=S)}\n{_selector('ZILP')}\n\n{body}\n\nThe integer:"
    elif cond == "F0_NAMED_DEF":
        body = _verdict_body(order, _is_prime)
        prompt = (f"{head}\n{DEF_PRIME.format(W='PRIME')}\nEach line shows a computation, its final result after "
                  f"'=>', and a verdict. Report the value of the ONE whose verdict is PASS. Output ONLY that integer.\n\n{body}\n\nThe integer:")
    else:  # F0_NOVEL_RULE
        body = _verdict_body(order, lambda v: _dsum(v) == S)
        prompt = (f"{head}\n{DEF_NOVEL.format(W='ZILP', S=S)}\nEach line shows a computation, its final result after "
                  f"'=>', and a verdict. Report the value of the ONE whose verdict is PASS. Output ONLY that integer.\n\n{body}\n\nThe integer:")

    compute_free = cond.startswith("F0")
    needle_line = (_line0(needle) if compute_free else _line(needle))
    return {"item_id": f"V11-{cond}-s{seed}", "cond": cond, "seed": seed, "compute_free": compute_free,
            "truth": needle["final"], "S": S,
            "needle_line_hash": hashlib.sha256(needle_line.encode()).hexdigest()[:16],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def _oracle(seed):
    st = _make(seed)
    primes = [c["final"] for c in st["chains"] if _is_prime(c["final"])]
    dsing = [c["final"] for c in st["chains"] if _dsum(c["final"]) == st["S"]]
    assert len(primes) == 1 and dsing == primes, "isomorphism broken"
    return primes[0]


def canonical_labels(items):
    keys = ("item_id", "cond", "seed", "compute_free", "truth", "S", "needle_line_hash", "prompt")
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
        if cells["NAMED_BARE"]["truth"] != _oracle(s): bad.append((s, "truth != oracle (isomorphism)"))
        comp = {cells[c]["needle_line_hash"] for c in ("NAMED_BARE", "NAMED_DEF", "RENAMED_PRIME", "NOVEL_RULE")}
        if len(comp) != 1: bad.append((s, "needle not byte-identical across compute arms"))
        if cells["F0_NAMED_DEF"]["needle_line_hash"] != cells["F0_NOVEL_RULE"]["needle_line_hash"]: bad.append((s, "F0 needle mismatch"))
        # exactly one PASS line in each F0 body, and it is the needle (same in both F0 arms)
        for c in ("F0_NAMED_DEF", "F0_NOVEL_RULE"):
            if cells[c]["prompt"].count("[verdict: PASS]") != 1: bad.append((s, f"{c} not exactly one PASS"))
        # def-block word counts matched across the three defined arms
        dw = [len(DEF_PRIME.format(W='PRIME').split()), len(DEF_PRIME.format(W='FLONK').split()),
              len(DEF_NOVEL.format(W='ZILP', S=cells['NOVEL_RULE']['S']).split())]
        if max(dw) - min(dw) > 3: bad.append((s, f"def word drift {dw}"))
    clean = seeds - len({b[0] for b in bad})
    print(f"[integrity] {clean}/{seeds} seeds clean", "OK" if not bad else f"FAIL {bad[:6]}")
    by = {}
    for it in items: by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        print(f"   {c:>13}: n={len(by[c])}  median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    defined = ["NAMED_DEF", "RENAMED_PRIME", "NOVEL_RULE"]
    dw = [np.median([it["prompt_words"] for it in by[c]]) for c in defined]
    print(f"   defined arms {defined}: words {min(dw):.0f}-{max(dw):.0f} (drift {100*(max(dw)-min(dw))/np.mean(dw):.0f}%)")
    f0 = [np.median([it["prompt_words"] for it in by[c]]) for c in ("F0_NAMED_DEF", "F0_NOVEL_RULE")]
    print(f"   F0 falsifier pair: words {f0[0]:.0f} / {f0[1]:.0f}")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")
    return not bad


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v11_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v11_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "note": "V11 de-amortization; headline e(NOVEL_RULE)-e(NAMED_DEF); falsifier e(F0_NOVEL)-e(F0_NAMED) (compute-free)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v11_labels.jsonl + v11_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v11_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== V11 de-amortize: {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
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
    (HERE / f"v11_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    analyze(stream, seeds, repeats)


def analyze(stream, seeds, repeats):
    import numpy as np
    nex = sum(1 for s in stream if s.get("exhausted"))
    print(f"\n  ({nex}/{len(stream)} exhausted; excluded)")
    print(f"  by condition:   acc(completed)   median / MEAN rt(correct)")
    for c in CONDS:
        done = [s for s in stream if s["cond"] == c and not s.get("exhausted")]
        if not done: continue
        acc = sum(1 for s in done if s["correct"])
        tk = [s["reasoning_tokens"] for s in done if s["correct"] and s["reasoning_tokens"] is not None]
        md = np.median(tk) if tk else float('nan'); mn = np.mean(tk) if tk else float('nan')
        print(f"    {c:>13}:  {acc}/{len(done)}        {md:.0f} / {mn:.0f}")

    sids = sorted({s["seed"] for s in stream})
    def mt(c, sd):
        v = [s["reasoning_tokens"] for s in stream if s["cond"] == c and s["seed"] == sd
             and s["correct"] and s["reasoning_tokens"] is not None]
        return float(np.mean(v)) if v else None
    def delta(a, b, why):
        d = [mt(a, sd) - mt(b, sd) for sd in sids if None not in (mt(a, sd), mt(b, sd))]
        r = paired(d)
        print(f"     {a:>13} - {b:<13} {r[0]:+8.1f}  CI[{r[1][0]:+.0f},{r[1][1]:+.0f}]  p={r[2]:.3f}  (n={r[5]})   {why}" if r else f"     {a}-{b}  n/a   {why}")

    print("\n  DE-AMORTIZATION deltas (per-seed mean over reps; bootstrap CI + exact sign p):")
    delta("NAMED_DEF", "NAMED_BARE", "(3) carrying a def of a KNOWN concept (~reading tax)")
    delta("RENAMED_PRIME", "NAMED_DEF", "(2) NAME-only de-amortization (nonce binding)")
    delta("NOVEL_RULE", "NAMED_DEF", "(1) HEADLINE -- un-amortized selection concept (BUILD-clock re-pay)")
    print("  THE FALSIFIER (compute removed both sides, length-matched):")
    delta("F0_NOVEL_RULE", "F0_NAMED_DEF", "vanishes (CI~0) => headline was concept-APPLICATION not def-reading")
    print("\n  VERDICT logic: (1)>0 AND falsifier~0 AND gradient NAMED<=RENAMED<NOVEL => the camera reads a real "
          "MEANING-wrapper de-amortization (the cost of NOT having the concept pre-paid). Nulls demote per kill-criteria.")
    print(f"  wrote v11_run.{MODEL}.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--seeds", type=int, default=28); ap.add_argument("--repeats", type=int, default=4)
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
        stream = [json.loads(l) for l in (HERE / f"v11_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
