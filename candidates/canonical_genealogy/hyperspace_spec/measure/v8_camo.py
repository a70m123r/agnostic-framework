#!/usr/bin/env python3
"""
V8 -- the CAMOUFLAGE rung (adversarial burial), AUDIT-REVISED. V7 showed labelled distractors are
filtered for free (reading tax, no compute tax). The naive V7b ("report the prime chain" vs "report
chain s") was caught by the design audit as measuring EXECUTION (evaluating the decoys, already known
from V5b), not CAMOUFLAGE. The fix: hold the evaluation requirement FIXED and vary only how
SURFACE-DISTINGUISHABLE the needle is -- the decoy-GAP knob.

4 conditions, m=6 chains x L=4 ops, no "ignore" labels:
  LABEL    : selector "the chain named s"            -> name-match, NO evaluation (the V7 free-filter floor)
  SUM      : selector "the sum of all final values"  -> full evaluation, NO disambiguation
  MAX_WIDE : selector "the largest final value", decoy finals SPREAD -> eval all, EASY disambiguation
  MAX_TIGHT: selector "the largest final value", decoy finals CLUSTERED near the needle -> eval all, HARD
             disambiguation (the needle hides among near-identical noise = camouflage)
PRIMARY estimand: CAMOUFLAGE = reasoning_tokens(MAX_TIGHT) - reasoning_tokens(MAX_WIDE) (execution held
fixed: both evaluate all m chains; only the final disambiguation difficulty differs) + a co-primary
error-rate contrast. Secondary: EXEC = SUM-LABEL, SELECT = MAX_WIDE-SUM. Prediction: CAMOUFLAGE > 0 and
CI excludes 0 -- the compute tax V7 missed appears when the needle is not surface-separable.
Machine-verifiable (generator knows every final + applies the rule). gpt-5.5. Cite Hidden-in-Haystack
(arXiv 2505.18148: smaller needle distinctness -> harder).
"""
import json, hashlib, argparse, sys, random
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MOD = 1000
OPS = ["+", "-", "*"]
M = 6          # chains per item
L = 4          # ops per chain
CONDS = ["LABEL", "SUM", "MAX_WIDE", "MAX_TIGHT"]
TIER_PREREG = "high"
NAMES = [f"x{i}" for i in range(1, 10)] + [f"y{i}" for i in range(1, 10)] + [f"z{i}" for i in range(1, 10)]


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def _chain(rng, name):
    v0 = rng.randint(10, 99); v = v0; ops = []
    for _ in range(L):
        op = rng.choice(OPS); c = rng.randint(2, 9); v = _apply(v, op, c); ops.append((op, c))
    line = f"{name} = {v0}; " + "; ".join(f"{name} = ({name} {op} {c}) % {MOD}" for (op, c) in ops)
    return {"name": name, "final": v, "line": line}


def _pool(rng, n=400):
    names = rng.sample(NAMES, M)              # m distinct names, no signal
    # generate many candidate chains per name slot? simpler: many chains, then pick by final-value pattern
    cands = []
    for _ in range(n):
        nm = rng.choice(names)
        cands.append(_chain(rng, nm))
    return names, cands


def gen_cell(cond, seed):
    rng = random.Random(f"V8|{cond}|{seed}")
    if cond == "LABEL":
        names = rng.sample(NAMES, M - 1)
        chains = [_chain(rng, nm) for nm in names]
        needle = _chain(rng, "s")             # the named needle
        chains.append(needle); truth = needle["final"]
        sel = "Report the final value of the variable named s."
    elif cond == "SUM":
        names = rng.sample(NAMES, M)
        chains = [_chain(rng, nm) for nm in names]
        truth = sum(c["final"] for c in chains)
        sel = "Report the sum of the final values of all the variables."
    else:  # MAX_WIDE / MAX_TIGHT -- per-name candidate pools; place the runner-up tight or wide below the needle
        names = rng.sample(NAMES, M)
        chains = None
        for _ in range(300):
            cand = {nm: [_chain(rng, nm) for _ in range(200)] for nm in names}
            needle = max(cand[names[0]], key=lambda c: c["final"]); Vn = needle["final"]
            picks = [needle]
            below = [c for c in cand[names[1]] if c["final"] < Vn]
            if not below:
                continue
            runner = max(below, key=lambda c: c["final"])             # nearest decoy below the needle
            gap = Vn - runner["final"]
            if cond == "MAX_TIGHT" and gap > 3:                        # runner-up must be within 3 of the needle
                continue
            if cond == "MAX_WIDE" and gap < 40:                        # runner-up clearly below the needle
                continue
            picks.append(runner)
            ok = True
            for nm in names[2:]:                                      # fill the rest, all clearly below the runner
                opts = [c for c in cand[nm] if c["final"] < runner["final"] - 5]
                if not opts:
                    ok = False; break
                picks.append(rng.choice(opts))
            if ok and len({c["final"] for c in picks}) == M:
                chains = picks; truth = Vn; break
        if chains is None:
            raise RuntimeError(f"no {cond} arrangement for seed {seed}")
        sel = "Report the single largest final value among all the variables."
    rng.shuffle(chains)
    sel = sel.ljust(64)   # pad selector text to equalize its length across conditions
    prompt = ("Below are " + str(M) + " short computations (all arithmetic mod " + str(MOD) +
              "). " + sel.strip() + " Output ONLY that integer.\n\n" + "\n".join(c["line"] for c in chains) +
              "\n\nThe integer:")
    return {"item_id": f"V8-{cond}-s{seed}", "cond": cond, "seed": seed,
            "truth": truth, "prompt": prompt, "prompt_words": len(prompt.split()),
            "finals": sorted(c["final"] for c in chains)}


def build_grid(seeds):
    return [gen_cell(c, s) for s in range(seeds) for c in CONDS]


def canonical_labels(items):
    return [{"item_id": it["item_id"], "cond": it["cond"], "seed": it["seed"],
             "truth": it["truth"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=16):
    import numpy as np
    items = build_grid(seeds)
    # uniqueness of MAX winner (no ties), LABEL has exactly one 's', truth in-range
    bad = []
    for it in items:
        if it["cond"].startswith("MAX") and it["finals"].count(it["truth"]) != 1:
            bad.append(it["item_id"] + ":max-tie")
        if it["cond"] == "LABEL" and (" s =" not in (" " + it["prompt"].replace("\n", " "))):
            bad.append(it["item_id"] + ":no-s")
    print(f"[integrity] {len(items)-len(bad)}/{len(items)} ok", "OK" if not bad else f"FAIL {bad[:4]}")
    by = {}
    for it in items:
        by.setdefault(it["cond"], []).append(it)
    for c in CONDS:
        ws = [it["prompt_words"] for it in by[c]]
        gaps = [max(it["finals"]) - min(it["finals"]) for it in by[c] if it["cond"].startswith("MAX")]
        gtxt = f" gap~{np.median(gaps):.0f}" if gaps else ""
        print(f"   {c:>9}: n={len(by[c])} median prompt_words={np.median(ws):.0f}{gtxt}")
    print("SELFTEST PASS" if not bad else "SELFTEST FAIL")


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v8_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v8_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": CONDS, "M": M, "L": L,
         "tier_preregistered": TIER_PREREG,
         "note": "camouflage rung; PRIMARY camouflage=MAX_TIGHT-MAX_WIDE (eval fixed, disambiguation varied)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v8_labels.jsonl + v8_labels.LOCK")


def paired(deltas):
    import numpy as np
    d = np.array([x for x in deltas if x is not None], float)
    if len(d) < 4: return None
    rng = np.random.default_rng(7)
    boot = [np.median(rng.choice(d, len(d), replace=True)) for _ in range(4000)]
    ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
    pos = int((d > 0).sum()); neg = int((d < 0).sum()); nz = pos + neg
    p = min(1.0, 2 * sum(comb(nz, i) for i in range(max(pos, neg), nz + 1)) / (2 ** nz)) if nz else 1.0
    return float(np.median(d)), ci, p, pos, neg, len(d)


def run(_):
    from digestion_v2 import openai_solve, verify, last_int
    import numpy as np
    lk = json.loads((HERE / "v8_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    tier = lk.get("tier_preregistered", "high")
    print(f"=== V8 camouflage: {len(items)} items ({len(CONDS)} conds x {lk['seeds']} seeds) @ '{tier}' ===")
    stream = []
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = (last_int(reply) == it["truth"]); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({**{k: it[k] for k in ("item_id", "cond", "seed", "prompt_words", "truth")},
                       "tier": tier, "reasoning_tokens": rt, "got": a, "correct": ok, "exhausted": ex})
    (HERE / "v8_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n  solved {len(solved)}/{len(stream)}  (accuracy by cond: " +
          ", ".join(f"{c}={sum(1 for s in stream if s['cond']==c and s['correct'])}/{sum(1 for s in stream if s['cond']==c)}" for c in CONDS) + ")")
    def med(c):
        v = [s["reasoning_tokens"] for s in solved if s["cond"] == c]
        return np.median(v) if v else float('nan')
    print("  median reasoning_tokens by condition:")
    for c in CONDS:
        print(f"    {c:>9}: {med(c):>6.0f}")
    def tok(c, sd):
        v = [s["reasoning_tokens"] for s in solved if s["cond"] == c and s["seed"] == sd]
        return v[0] if v else None
    seeds = sorted({s["seed"] for s in solved})
    rc = paired([tok("MAX_TIGHT", sd) - tok("MAX_WIDE", sd) for sd in seeds if None not in (tok("MAX_TIGHT", sd), tok("MAX_WIDE", sd))])
    re_ = paired([tok("SUM", sd) - tok("LABEL", sd) for sd in seeds if None not in (tok("SUM", sd), tok("LABEL", sd))])
    rs = paired([tok("MAX_WIDE", sd) - tok("SUM", sd) for sd in seeds if None not in (tok("MAX_WIDE", sd), tok("SUM", sd))])
    print(f"\n  PRIMARY  camouflage (MAX_TIGHT - MAX_WIDE) = {rc[0]:+.1f} [{rc[1][0]:+.0f},{rc[1][1]:+.0f}] p={rc[2]:.3f}  ({rc[3]}+/{rc[4]}-/n={rc[5]})")
    print(f"  secondary execution (SUM - LABEL)          = {re_[0]:+.1f} [{re_[1][0]:+.0f},{re_[1][1]:+.0f}] p={re_[2]:.3f}")
    print(f"  secondary selection (MAX_WIDE - SUM)       = {rs[0]:+.1f} [{rs[1][0]:+.0f},{rs[1][1]:+.0f}] p={rs[2]:.3f}")
    print("\n  VERDICT:", "CAMOUFLAGE BITES (tight>wide; the compute tax V7 missed appears when the needle is not surface-separable)" if rc[0] > 4 and rc[1][0] > 0 else
          ("NO CAMOUFLAGE TAX (tight ~ wide; the model disambiguates near-identical candidates as cheaply as separated ones)" if abs(rc[0]) <= 4 or rc[1][0] <= 0 < rc[1][1] else "MIXED"))
    print(f"  wrote v8_run.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--seeds", type=int, default=16)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    elif a.run: run(a.seeds)
    else: print("use --selftest | --lock --seeds N | --run")
