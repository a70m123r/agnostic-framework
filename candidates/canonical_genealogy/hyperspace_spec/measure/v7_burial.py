#!/usr/bin/env python3
"""
V7 -- the BURIAL GRADIENT (Pav's "the more you bury the real thing in, the more compute?"). Holds the
real computation FIXED (a depth-6 chain on s -> answer) and varies how much IRRELEVANT clutter is
piled around it, separating two kinds of burial:
  inert(k) : k labelled-distractor lines that are trivial no-ops (w = 0)        -> pure length/reading
  ops(k)   : k labelled-distractor lines that are real arithmetic (w = (a*b)%M) -> COMPUTATIONAL clutter
Both are explicitly tagged "distractor, ignore". Conditions: k0 (no clutter), inert/ops at k in {6,12}.
=> reading-cost          = inert(k) - k0      (labelled clutter you are told to ignore, but must read)
   burial-of-computation = ops(k) - inert(k)  (same #lines, but the clutter is COMPUTATIONAL)
If ops > inert at matched k, the model cannot cleanly skip computational clutter -- burying the needle
in COMPUTATION costs more reasoning than burying it in equal-length TEXT (the V6b 'can't-help-computing'
effect, as clutter). The answer is IDENTICAL across all conditions (core chain fixed per seed). gpt-5.5.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MOD = 1000
OPS = ["+", "-", "*"]
DCORE = 6
CONDS = [("k0", 0, "none"), ("inert6", 6, "inert"), ("ops6", 6, "ops"), ("inert12", 12, "inert"), ("ops12", 12, "ops")]
TIER_PREREG = "high"


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def gen_cell(cond, k, ctype, seed):
    rng = random.Random(f"V7|{seed}")                 # core chain shared across all conditions of a seed
    s0 = rng.randint(10, 99)
    s = s0; core = [f"s = {s0}"]
    for _ in range(DCORE):
        op = rng.choice(OPS); c = rng.randint(2, 9)
        s = _apply(s, op, c); core.append(f"s = (s {op} {c}) % {MOD}")
    answer = s
    crng = random.Random(f"V7clutter|{cond}|{seed}")
    clutter = []
    for i in range(k):
        a, b, op = crng.randint(10, 99), crng.randint(2, 9), crng.choice(OPS)
        if ctype == "inert":   # length-matched DEAD-expression clutter: same expr, value GIVEN -> no compute needed
            val = _apply(a, op, b)
            clutter.append(f"w{i} = ({a} {op} {b}) % {MOD} = {val}    # distractor, already computed, ignore")
        else:                  # LIVE-expression clutter: same expr, must be EVALUATED if not skipped
            clutter.append(f"w{i} = ({a} {op} {b}) % {MOD}    # distractor, ignore")
    body = list(core)
    for cl in clutter:
        body.insert(crng.randint(1, len(body)), cl)    # never before the s=s0 init
    prompt = ("Track ONLY the variable s. Lines that assign to w-variables are distractors -- ignore them. "
              "All arithmetic on s is mod " + str(MOD) + ". Reply with ONLY the final integer.\n\n"
              + "\n".join(body) + "\n\nFinal value of s?")
    return {"item_id": f"V7-{cond}-s{seed}", "cond": cond, "k": k, "ctype": ctype, "seed": seed,
            "s0": s0, "answer": answer, "prompt": prompt, "prompt_words": len(prompt.split()),
            "core_chain": core}


def build_grid(seeds):
    return [gen_cell(c, k, t, s) for s in range(seeds) for (c, k, t) in CONDS]


def oracle_recompute(item):
    # replay ONLY the core s-chain (distractors never touch s)
    s = None
    for line in item["prompt"].splitlines():
        line = line.strip()
        if line.startswith("s = ") and "(" not in line and "%" not in line:
            s = int(line.split("=")[1])
        elif line.startswith("s = (s "):
            inside = line.split("(s", 1)[1].split(")")[0].strip()
            op, c = inside.split(); s = _apply(s, op, int(c))
    return s


def canonical_labels(items):
    return [{"item_id": it["item_id"], "cond": it["cond"], "seed": it["seed"],
             "answer": it["answer"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=16):
    import numpy as np
    items = build_grid(seeds)
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} core-chain replay-match", "OK" if not bad else f"FAIL {bad[:4]}")
    mism = []
    for s in range(seeds):
        ans = {c[0]: next(it["answer"] for it in items if it["cond"] == c[0] and it["seed"] == s) for c in CONDS}
        if len(set(ans.values())) != 1:
            mism.append((s, ans))
    print(f"[match] all conditions share the answer within seed: {'OK' if not mism else 'FAIL '+str(mism[:2])}")
    by = {}
    for it in items:
        by.setdefault(it["cond"], []).append(it)
    for c, k, t in CONDS:
        print(f"   {c:>8} (k={k} {t:>5}): n={len(by[c])} median prompt_words={np.median([it['prompt_words'] for it in by[c]]):.0f}")
    print("SELFTEST PASS" if not bad and not mism else "SELFTEST FAIL")


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v7_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v7_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "conds": [c[0] for c in CONDS],
         "Dcore": DCORE, "tier_preregistered": TIER_PREREG,
         "note": "burial gradient; reading=inert(k)-k0, burial-of-computation=ops(k)-inert(k)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v7_labels.jsonl + v7_labels.LOCK")


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
    lk = json.loads((HERE / "v7_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    tier = lk.get("tier_preregistered", "high")
    print(f"=== V7 burial: {len(items)} items ({len(CONDS)} conds x {lk['seeds']} seeds) @ '{tier}' ===")
    stream = []
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = verify(it["answer"], reply); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({**{k: it[k] for k in ("item_id", "cond", "k", "ctype", "seed", "prompt_words", "answer")},
                       "tier": tier, "reasoning_tokens": rt, "got": a, "correct": ok, "exhausted": ex})
    (HERE / "v7_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n  solved {len(solved)}/{len(stream)}")
    def med(c):
        v = [s["reasoning_tokens"] for s in solved if s["cond"] == c]
        return np.median(v) if v else float('nan')
    print("  median reasoning_tokens by condition:")
    for c, k, t in CONDS:
        print(f"    {c:>8} (k={k:>2} {t:>5}): {med(c):>6.0f}")
    def tok(c, sd):
        v = [s["reasoning_tokens"] for s in solved if s["cond"] == c and s["seed"] == sd]
        return v[0] if v else None
    seeds = sorted({s["seed"] for s in solved})
    print("\n  DECOMPOSITION (paired):")
    for k in (6, 12):
        rd = paired([tok(f"inert{k}", sd) - tok("k0", sd) for sd in seeds if None not in (tok(f"inert{k}",sd), tok("k0",sd))])
        rb = paired([tok(f"ops{k}", sd) - tok(f"inert{k}", sd) for sd in seeds if None not in (tok(f"ops{k}",sd), tok(f"inert{k}",sd))])
        print(f"    k={k:>2}: reading-cost (inert-k0) = {rd[0]:+.1f} [{rd[1][0]:+.0f},{rd[1][1]:+.0f}] p={rd[2]:.3f}  |  burial-of-compute (ops-inert) = {rb[0]:+.1f} [{rb[1][0]:+.0f},{rb[1][1]:+.0f}] p={rb[2]:.3f}")
    # gradient: does ops cost climb with k?
    g = paired([tok("ops12", sd) - tok("ops6", sd) for sd in seeds if None not in (tok("ops12",sd), tok("ops6",sd))])
    print(f"\n  GRADIENT ops12 - ops6 = {g[0]:+.1f} [{g[1][0]:+.0f},{g[1][1]:+.0f}] p={g[2]:.3f}  (does computational burial scale with depth-of-burial?)")
    print(f"  wrote v7_run.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--seeds", type=int, default=16)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    elif a.run: run(a.seeds)
    else: print("use --selftest | --lock --seeds N | --run")
