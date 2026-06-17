#!/usr/bin/env python3
"""
V6b -- the IRRELEVANT-EXPRESSION CONTROL (codex's decisive add-on to V6). Separates V6's ENCODE
effect into two parts the bare V6 design confounds:
  text-cost   = E3dead - E0    (the expression TEXT is present but explicitly already-computed)
  compute-cost = E3live - E3dead (the SAME text, but now it must be EVALUATED)
If compute-cost >> text-cost, the decode load is genuinely COMPUTATIONAL (reasoning_tokens track
work, not transcription). If text-cost dominates, V6's encode effect was mostly the longer/expr-laden
PROMPT (transcription/attention) -- demote further. This is the confound seed-escalation cannot fix.

3x2 design: E in {E0, E3dead, E3live} x D in {4,12} x seeds. Within a (D,seed) all three E arms share
the SAME s0 + chain + ANSWER -- only the encode treatment differs. E3dead and E3live carry the SAME
expression text (matched attention/transcription load); only 'must compute' differs. sha256 lock
binds stimulus + tier. Stdlib (numpy selftest only). gpt-5.5.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
MOD = 1000
OPS = ["+", "-", "*"]
E_LEVELS = ["E0", "E3dead", "E3live"]
D_LEVELS = [4, 12]
TIER_PREREG = "high"


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def gen_cell(E, D, seed):
    rng = random.Random(f"V6b|{D}|{seed}")            # shared s0 + chain across the 3 E arms
    a, b, c, e = (rng.randint(2, 20) for _ in range(4))
    s0 = ((( a + b) * c) - e) % MOD
    expr = f"((({a} + {b}) * {c}) - {e}) % {MOD}"
    chain = []
    s = s0
    for _ in range(D):
        op = rng.choice(OPS); k = rng.randint(2, 9)
        s = _apply(s, op, k); chain.append((op, k))
    answer = s
    if E == "E0":
        setup = f"s = {s0}"
    elif E == "E3dead":
        setup = f"s = {s0}   # note: {s0} = {expr}  (already computed for you -- do NOT recompute this expression)"
    else:  # E3live
        setup = f"s = {expr}"
    lines = [setup] + [f"s = (s {op} {k}) % {MOD}" for (op, k) in chain]
    prompt = ("Evaluate these assignments in order. All arithmetic is mod " + str(MOD) +
              ". Reply with ONLY the final integer.\n\n" + "\n".join(lines) + "\n\nFinal value of s?")
    return {"item_id": f"V6b-{E}-D{D}-s{seed}", "encode": E, "depth": D, "seed": seed,
            "s0": s0, "chain": chain, "expr": expr, "prompt": prompt,
            "prompt_words": len(prompt.split()), "answer": answer}


def build_grid(seeds):
    return [gen_cell(E, D, s) for s in range(seeds) for E in E_LEVELS for D in D_LEVELS]


def oracle_recompute(item):
    s = item["s0"]
    for (op, k) in item["chain"]:
        s = _apply(s, op, k)
    return s


def canonical_labels(items):
    return [{"item_id": it["item_id"], "encode": it["encode"], "depth": it["depth"],
             "seed": it["seed"], "answer": it["answer"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=16):
    import numpy as np
    items = build_grid(seeds)
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} replay-match", "OK" if not bad else f"FAIL {bad[:4]}")
    # all 3 E arms share the answer within (D,seed)
    mism = []
    for s in range(seeds):
        for D in D_LEVELS:
            ans = {E: next(it["answer"] for it in items if it["encode"] == E and it["depth"] == D and it["seed"] == s) for E in E_LEVELS}
            if len(set(ans.values())) != 1:
                mism.append((s, D, ans))
    print(f"[match] 3 E arms share the answer within (D,seed): {'OK' if not mism else 'FAIL '+str(mism[:2])}")
    # the expression TEXT must be present in BOTH E3dead and E3live, absent in E0
    txt = []
    for s in range(seeds):
        for D in D_LEVELS:
            byE = {it["encode"]: it for it in items if it["depth"] == D and it["seed"] == s}
            ex = byE["E0"]["expr"]
            ok = (ex in byE["E3dead"]["prompt"]) and (ex in byE["E3live"]["prompt"]) and (ex not in byE["E0"]["prompt"])
            if not ok: txt.append((s, D))
    print(f"[textmatch] expr present in E3dead & E3live, absent in E0: {'OK' if not txt else 'FAIL '+str(txt[:2])}")
    cells = {}
    for it in items:
        cells.setdefault((it["encode"], it["depth"]), []).append(it)
    print("[design] 3x2 cell counts:", {f"{k[0]}/D{k[1]}": len(v) for k, v in sorted(cells.items())})
    for k in sorted(cells):
        w = np.median([it["prompt_words"] for it in cells[k]])
        print(f"   cell {k[0]:>6} D={k[1]:>2}: median prompt_words={w:.0f}")
    print("SELFTEST PASS" if not bad and not mism and not txt else "SELFTEST FAIL")


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v6b_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v6b_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "E_levels": E_LEVELS,
         "D_levels": D_LEVELS, "tier_preregistered": TIER_PREREG,
         "note": "irrelevant-expression control; text-cost=E3dead-E0, compute-cost=E3live-E3dead"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v6b_labels.jsonl + v6b_labels.LOCK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--seeds", type=int, default=16)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    else: print("use --selftest or --lock --seeds N")
