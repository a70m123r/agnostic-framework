#!/usr/bin/env python3
"""
NF -- NOVEL_FAMILIAR: separate LABEL-novelty from COMPUTE-difficulty in the de-amortization tax.

The V11b headline (NOVEL_RULE - NAMED_DEF) confounds TWO things at once: the predicate's NAME is a nonce
AND its COMPUTE is uncached. Both audits (Claude lead + codex external) named the SAME wedge: a 2x2 of
  {label:  rule stated PLAIN  vs  wrapped in a coined NONCE name}
  {compute: TRIVIAL cached (last-digit glance)  vs  HARD uncached (primality trial-division)}
all selecting the IDENTICAL needle. The decisive contrast is TRIV_NONCE - TRIV_PLAIN: the cost of
coining+dereferencing a name with ZERO concept-translation (the def IS the trivial rule, nothing to recognize)
-> isolates PURE label-binding from the FLONK->prime translation that contaminated V11b's RENAMED rung (codex/
Claude C2). If naming a trivial rule STILL costs reasoning, label-binding is a real cost independent of compute.

Needle = the unique prime among 6 finals AND the unique final whose last digit is in {3,7}; so primality (HARD)
and last-digit (TRIVIAL) select the SAME integer (isomorphic). All finals are GIVEN inline ('=> v') so chain
arithmetic is constant across cells -- only PREDICATE application + label varies. The word 'prime' is never used
in PLAIN/NONCE (both state primality as a rule); HARD_WORD is a 5th cell using the amortized word, bridging to
V11b's NAMED_DEF.

5 conds (paired by seed; needle line byte-identical; only the SELECTOR changes):
  TRIV_PLAIN : rule stated, trivial compute (last digit 3 or 7)
  TRIV_NONCE : coined ZILP = that trivial rule
  HARD_PLAIN : rule stated, hard compute (divisible only by 1 and itself, >=2)
  HARD_NONCE : coined FLONK = that hard rule
  HARD_WORD  : the amortized word 'PRIME'   (bridge to V11b)
Headline LABEL effects: TRIV_NONCE-TRIV_PLAIN (pure, no translation) and HARD_NONCE-HARD_PLAIN.
COMPUTE effects: HARD_PLAIN-TRIV_PLAIN and HARD_NONCE-TRIV_NONCE. WORD shortcut: HARD_WORD-HARD_PLAIN.
"""
import os, json, hashlib, argparse, sys, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v9b_resistance import _chain, _is_prime, _line, _last_int, paired, MOD
from v10_framestrip import _line0
from providers import solve, estimate_table, MODELS

TIER = "high"
MODEL = "deepseek"
CONDS = ["TRIV_PLAIN", "TRIV_NONCE", "HARD_PLAIN", "HARD_NONCE", "HARD_WORD"]
TASK_NAMES = ["alpha", "bravo", "cosmo", "delta", "echo", "foxy", "gamma", "hotel", "indi", "juno"]

# Word-count-balanced selectors. PLAIN vs NONCE differ ONLY by the naming clause (kept parallel across
# TRIV/HARD so the label-effect interaction controls for the few naming-clause words).
SEL = {
    "TRIV_PLAIN": "Among the six finals, exactly one has a last digit equal to 3 or to 7. "
                  "Report the value of that one computation. Output ONLY that integer.",
    "TRIV_NONCE": "Call a number a ZILP when its last digit equals 3 or 7. Among the six finals, "
                  "exactly one is a ZILP. Report the value of that one computation. Output ONLY that integer.",
    "HARD_PLAIN": "Among the six finals, exactly one is divisible by no integer except 1 and itself (and is "
                  "at least 2). Report the value of that one computation. Output ONLY that integer.",
    "HARD_NONCE": "Call a number a FLONK when it is divisible by no integer except 1 and itself (and is at "
                  "least 2). Among the six finals, exactly one is a FLONK. Report the value of that one computation. "
                  "Output ONLY that integer.",
    "HARD_WORD":  "Among the six finals, exactly one is a PRIME number. "
                  "Report the value of that one computation. Output ONLY that integer.",
}


def _last_digit_match(n):
    return (n % 10) in (3, 7)


def _make(seed):
    """6 chains, all-distinct finals, EXACTLY one prime (needle), needle's last digit in {3,7}, and NO other
    final has last digit in {3,7} -> primality and last-digit select the SAME unique needle (isomorphic)."""
    rng = random.Random(f"NF|{seed}")
    for _ in range(80000):
        names = rng.sample(TASK_NAMES, 6)
        chains = [_chain(rng, nm) for nm in names]
        finals = [c["final"] for c in chains]
        if len(set(finals)) != 6:
            continue
        primes = [c for c in chains if _is_prime(c["final"])]
        if len(primes) != 1:
            continue
        needle = primes[0]
        if not _last_digit_match(needle["final"]):
            continue
        if any(_last_digit_match(c["final"]) for c in chains if c is not needle):
            continue
        return {"chains": chains, "needle": needle}
    raise RuntimeError(f"no NF structure for seed {seed}")


def gen_cell(cond, seed):
    st = _make(seed)
    chains, needle = st["chains"], st["needle"]
    rng = random.Random(f"NFord|{seed}")
    order = list(chains); rng.shuffle(order)
    body = "\n".join(_line0(c) for c in order)        # every line shows '=> final' (chain compute removed)
    head = f"Below are 6 computations (arithmetic mod {MOD}); each line shows its final result after '=>'."
    prompt = f"{head}\n{SEL[cond]}\n\n{body}\n\nThe integer:"
    needle_line = _line0(needle)
    return {"item_id": f"NF-{cond}-s{seed}", "cond": cond, "seed": seed,
            "truth": needle["final"], "needle_line_hash": hashlib.sha256(needle_line.encode()).hexdigest()[:16],
            "prompt": prompt, "prompt_words": len(prompt.split())}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def _oracle(seed):
    st = _make(seed)
    pr = [c["final"] for c in st["chains"] if _is_prime(c["final"])]
    ld = [c["final"] for c in st["chains"] if _last_digit_match(c["final"])]
    assert len(pr) == 1 and ld == pr, "isomorphism broken (prime != unique last-digit-{3,7})"
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
        if len({c["truth"] for c in cells.values()}) != 1: bad.append((s, "truth differs across conds"))
        if cells["HARD_WORD"]["truth"] != _oracle(s): bad.append((s, "truth != oracle / isomorphism broken"))
        if not _is_prime(cells["HARD_WORD"]["truth"]): bad.append((s, "truth not prime"))
        if not _last_digit_match(cells["HARD_WORD"]["truth"]): bad.append((s, "truth last digit not in {3,7}"))
        if len({cells[c]["needle_line_hash"] for c in CONDS}) != 1: bad.append((s, "needle line not byte-identical"))
    clean = seeds - len({b[0] for b in bad})
    print(f"[integrity] {clean}/{seeds} seeds clean", "OK" if not bad else f"FAIL {bad[:6]}")
    by = {}
    for it in items: by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        print(f"   {c:>11}: n={len(by[c])}  median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    # label clauses add a few words; report the PLAIN/NONCE drift so it is disclosed not hidden
    sw = {c: int(np.median([it['prompt_words'] for it in by[c]])) for c in CONDS}
    print(f"   label drift: TRIV_NONCE-TRIV_PLAIN={sw['TRIV_NONCE']-sw['TRIV_PLAIN']:+d} words, "
          f"HARD_NONCE-HARD_PLAIN={sw['HARD_NONCE']-sw['HARD_PLAIN']:+d} words (naming clause; controlled by interaction)")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")
    return not bad


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v_nf_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v_nf_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "tier": TIER,
         "note": "NF label x compute 2x2 (+WORD bridge); headline TRIV_NONCE-TRIV_PLAIN = pure label-binding, no translation"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v_nf_labels.jsonl + v_nf_labels.LOCK")


def run(seeds, repeats, workers):
    import numpy as np
    lk = json.loads((HERE / "v_nf_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    use = [it for it in items if it["seed"] < seeds]
    jobs = [(it, rep) for it in use for rep in range(repeats)]
    print(f"=== NF label/compute: {len(use)} items x {repeats} reps = {len(jobs)} calls on '{MODEL}' ({workers} workers) ===")
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
            if i % 50 == 0 or i == len(jobs):
                print(f"   ...{i}/{len(jobs)} done ({time.time()-t0:.0f}s)")
    (HERE / f"v_nf_run.{MODEL}.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
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
        print(f"    {c:>11}:  {acc}/{len(done)}        {md:.0f} / {mn:.0f}")

    sids = sorted({s["seed"] for s in stream})
    def mt(c, sd):
        v = [s["reasoning_tokens"] for s in stream if s["cond"] == c and s["seed"] == sd
             and s["correct"] and s["reasoning_tokens"] is not None]
        return float(np.mean(v)) if v else None
    def delta(a, b, why):
        d = [mt(a, sd) - mt(b, sd) for sd in sids if None not in (mt(a, sd), mt(b, sd))]
        r = paired(d)
        print(f"     {a:>11} - {b:<11} {r[0]:+8.1f}  CI[{r[1][0]:+.0f},{r[1][1]:+.0f}]  p={r[2]:.3f}  (n={r[5]})   {why}" if r else f"     {a}-{b}  n/a   {why}")

    print("\n  LABEL effect (coining a name; the decisive wedge):")
    delta("TRIV_NONCE", "TRIV_PLAIN", "PURE label-binding @ trivial compute (NO translation -> cleanest)")
    delta("HARD_NONCE", "HARD_PLAIN", "label-binding @ hard compute (includes any concept-recognition)")
    print("  COMPUTE effect (hard vs trivial predicate):")
    delta("HARD_PLAIN", "TRIV_PLAIN", "compute @ plain label")
    delta("HARD_NONCE", "TRIV_NONCE", "compute @ coined label")
    print("  WORD shortcut (bridge to V11b NAMED_DEF):")
    delta("HARD_PLAIN", "HARD_WORD", "stating the rule vs the amortized word 'prime' (>0 => word saves)")
    print(f"  wrote v_nf_run.{MODEL}.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--seeds", type=int, default=60); ap.add_argument("--repeats", type=int, default=3)
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
        stream = [json.loads(l) for l in (HERE / f"v_nf_run.{MODEL}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        analyze(stream, a.seeds, a.repeats)
    else: print("use --selftest --seeds N | --lock --seeds N | --estimate --seeds N | --run --model M --seeds N | --reanalyze --model M")
