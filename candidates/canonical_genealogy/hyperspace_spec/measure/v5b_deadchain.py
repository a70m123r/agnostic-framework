#!/usr/bin/env python3
"""
V5b -- the DEAD-CHAIN control: extends V6b's compute-vs-transcription test from the ENCODE stage to
the SERIAL/SPAN stage (V5's DEEP>WIDE surcharge). Same serial chain shown in all arms; only whether
it must be EXECUTED differs:
  base : answer given, NO chain text                       (floor)
  dead : answer given, chain shown as ALREADY-APPLIED       (chain TEXT present, not executed)
  live : must apply the chain to get the answer             (chain EXECUTED)
=> chain-text-cost  = dead - base   (carrying the chain text)
   chain-compute-cost = live - dead (running the D serial steps)
If compute-cost >> text-cost AND scales with D, V5's span surcharge is real serial COMPUTATION, not
transcription -- the analog of V6b's encode-axis result, on the depth axis. 3 arms x D{4,12} x seeds.
Within (D,seed) all arms share the same chain + ANSWER. sha256 lock binds stimulus + tier. gpt-5.5.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path
from math import comb
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MOD = 1000
OPS = ["+", "-", "*"]
ARMS = ["base", "dead", "live"]
D_LEVELS = [4, 12]
TIER_PREREG = "high"


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def gen_cell(arm, D, seed):
    rng = random.Random(f"V5b|{D}|{seed}")
    s0 = rng.randint(10, 99)
    chain, s = [], s0
    for _ in range(D):
        op = rng.choice(OPS); k = rng.randint(2, 9)
        s = _apply(s, op, k); chain.append((op, k))
    answer = s
    clines = "\n".join(f"s = (s {op} {k}) % {MOD}" for (op, k) in chain)
    if arm == "base":
        prompt = (f"s = {answer}\n\nReply with ONLY the final integer (the value of s).")
    elif arm == "dead":
        prompt = (f"s starts at {s0}. The operations below have ALREADY been applied to s; the result "
                  f"is s = {answer} (do NOT recompute -- just report it):\n\n{clines}\n\n"
                  f"Reply with ONLY the final integer (the value of s).")
    else:  # live
        prompt = (f"s starts at {s0}. Apply these operations to s in order (all arithmetic mod {MOD}):"
                  f"\n\n{clines}\n\nReply with ONLY the final integer (the final value of s).")
    return {"item_id": f"V5b-{arm}-D{D}-s{seed}", "arm": arm, "depth": D, "seed": seed,
            "s0": s0, "chain": chain, "prompt": prompt, "prompt_words": len(prompt.split()), "answer": answer}


def build_grid(seeds):
    return [gen_cell(arm, D, s) for s in range(seeds) for arm in ARMS for D in D_LEVELS]


def oracle_recompute(item):
    s = item["s0"]
    for (op, k) in item["chain"]:
        s = _apply(s, op, k)
    return s


def canonical_labels(items):
    return [{"item_id": it["item_id"], "arm": it["arm"], "depth": it["depth"], "seed": it["seed"],
             "answer": it["answer"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=16):
    import numpy as np
    items = build_grid(seeds)
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} replay-match", "OK" if not bad else f"FAIL {bad[:4]}")
    mism = []
    for s in range(seeds):
        for D in D_LEVELS:
            ans = {a: next(it["answer"] for it in items if it["arm"] == a and it["depth"] == D and it["seed"] == s) for a in ARMS}
            if len(set(ans.values())) != 1:
                mism.append((s, D, ans))
    print(f"[match] 3 arms share the answer within (D,seed): {'OK' if not mism else 'FAIL '+str(mism[:2])}")
    cells = {}
    for it in items:
        cells.setdefault((it["arm"], it["depth"]), []).append(it)
    print("[design] cell counts:", {f"{k[0]}/D{k[1]}": len(v) for k, v in sorted(cells.items())})
    for k in sorted(cells):
        print(f"   {k[0]:>5} D={k[1]:>2}: median prompt_words={np.median([it['prompt_words'] for it in cells[k]]):.0f}")
    print("SELFTEST PASS" if not bad and not mism else "SELFTEST FAIL")


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v5b_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v5b_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "arms": ARMS, "D_levels": D_LEVELS,
         "tier_preregistered": TIER_PREREG, "note": "dead-chain control; text=dead-base, compute=live-dead"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v5b_labels.jsonl + v5b_labels.LOCK")


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


def run(seeds_tier):
    from digestion_v2 import openai_solve, verify, last_int
    import numpy as np
    lk = json.loads((HERE / "v5b_labels.LOCK").read_text(encoding="utf-8"))
    items = build_grid(lk["seeds"])
    if lock_digest(canonical_labels(items)) != lk["sha256"]:
        sys.exit("LOCK MISMATCH")
    tier = lk.get("tier_preregistered", "high")
    print(f"=== V5b dead-chain: {len(items)} items (3 arms x 2 depths x {lk['seeds']} seeds) @ '{tier}' ===")
    stream = []
    for it in items:
        try:
            reply, rt, dt = openai_solve(it["prompt"], tier); ok = verify(it["answer"], reply); a = last_int(reply); ex = False
        except Exception:
            reply, rt, dt, ok, a, ex = "", None, 100.0, False, None, True
        stream.append({**{k: it[k] for k in ("item_id", "arm", "depth", "seed", "prompt_words", "answer")},
                       "tier": tier, "reasoning_tokens": rt, "got": a, "correct": ok, "exhausted": ex})
    (HERE / "v5b_run.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    solved = [s for s in stream if s["correct"] and s["reasoning_tokens"] is not None]
    print(f"\n  solved {len(solved)}/{len(stream)}")
    def med(a, D):
        v = [s["reasoning_tokens"] for s in solved if s["arm"] == a and s["depth"] == D]
        return np.median(v) if v else float('nan')
    print(f"  cell medians:        D=4     D=12")
    for a in ARMS:
        print(f"    {a:>5}:             {med(a,4):>6.0f}  {med(a,12):>6.0f}")
    def tok(a, D, sd):
        v = [s["reasoning_tokens"] for s in solved if s["arm"] == a and s["depth"] == D and s["seed"] == sd]
        return v[0] if v else None
    seeds = sorted({s["seed"] for s in solved})
    for D in (4, 12):
        text = [tok("dead", D, sd) - tok("base", D, sd) for sd in seeds if None not in (tok("dead",D,sd), tok("base",D,sd))]
        comp = [tok("live", D, sd) - tok("dead", D, sd) for sd in seeds if None not in (tok("live",D,sd), tok("dead",D,sd))]
        rt, rc = paired(text), paired(comp)
        print(f"\n  D={D}:  chain-text-cost (dead-base) = {rt[0]:+.1f} [{rt[1][0]:+.0f},{rt[1][1]:+.0f}] p={rt[2]:.3f}  |  chain-compute-cost (live-dead) = {rc[0]:+.1f} [{rc[1][0]:+.0f},{rc[1][1]:+.0f}] p={rc[2]:.3f}")
    # pooled
    text = [tok("dead", D, sd) - tok("base", D, sd) for sd in seeds for D in (4,12) if None not in (tok("dead",D,sd), tok("base",D,sd))]
    comp = [tok("live", D, sd) - tok("dead", D, sd) for sd in seeds for D in (4,12) if None not in (tok("live",D,sd), tok("dead",D,sd))]
    rt, rc = paired(text), paired(comp)
    print(f"\n  POOLED: chain-text-cost {rt[0]:+.1f}  vs  chain-compute-cost {rc[0]:+.1f}")
    print("  VERDICT:", "SPAN IS COMPUTE (executing the chain >> carrying its text; scales with D)" if rc[0] > rt[0] + 4 else
          ("SPAN IS TEXT/TRANSCRIPTION (carrying the chain ~ executing it)" if rt[0] > rc[0] + 4 else "MIXED"))
    print(f"  wrote v5b_run.jsonl ({len(stream)} records)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--lock", action="store_true")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--seeds", type=int, default=16)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    elif a.run: run(a.seeds)
    else: print("use --selftest | --lock --seeds N | --run")
