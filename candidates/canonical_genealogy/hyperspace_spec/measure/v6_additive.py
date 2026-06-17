#!/usr/bin/env python3
"""
V6 — the STERNBERG ADDITIVE-FACTORS test on reasoning tokens (the chronometric inversion).

Sternberg (1969): if two task factors load SEPARATE serial stages, their effects on total time
are ADDITIVE (zero interaction); if they load the SAME stage, they INTERACT. We run the exact
design on reasoning_tokens, with two ORTHOGONAL factors:

  ENCODE (E in {0,3}) -- a ONE-TIME decode load at the start: the starting value s0 is given either
      as a plain integer (E=0) or as a fixed 3-op arithmetic EXPRESSION that must be evaluated to
      s0 (E=3). Same resulting s0 in both arms -> the only difference is the decode stage.
  DEPTH  (D in {4,12}) -- the length of the serial dependent chain applied to s0 (the V5 span knob).

Factorial 2x2 x seeds. PRIMARY = the INTERACTION term
  I = [tok(E=3,D=12) - tok(E=0,D=12)] - [tok(E=3,D=4) - tok(E=0,D=4)]
ADDITIVE (I ~ 0): encode and depth are separable serial stages -> the camera reads compositional
cost as a SUM (the chronometric signature; rediscovery-as-validation made load-bearing).
INTERACTION (I > 0): the decode is re-paid through the chain -> a shared stage / no clean staging.
The interaction is a difference-of-differences, so it CANCELS any main effect of E (incl. its extra
prompt length) and of D -- length-robust BY CONSTRUCTION. sha256 lock binds stimulus + tier.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = 1000
OPS = ["+", "-", "*"]
E_LEVELS = [0, 3]        # encode decode-ops (0 = plain integer, 3 = a 3-op expression)
D_LEVELS = [4, 12]       # serial chain depth (short, long)
TIER_PREREG = "high"


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def gen_cell(E, D, seed):
    """One 2x2 cell. The encode value s0 + the depth chain are shared across E within a (D,seed)."""
    rng = random.Random(f"V6|{D}|{seed}")            # NB: keyed on (D,seed) only -> s0 + chain identical across E
    a, b, c, e = (rng.randint(2, 20) for _ in range(4))
    s0 = ((( a + b) * c) - e) % MOD                  # the decode target
    encode_expr = f"((({a} + {b}) * {c}) - {e}) % {MOD}"
    chain = []
    s = s0
    for _ in range(D):
        op = rng.choice(OPS); k = rng.randint(2, 9)
        s = _apply(s, op, k); chain.append((op, k))
    answer = s
    setup = f"s = {s0}" if E == 0 else f"s = {encode_expr}"
    lines = [setup] + [f"s = (s {op} {k}) % {MOD}" for (op, k) in chain]
    prompt = ("Evaluate these assignments in order. All arithmetic is mod " + str(MOD) +
              ". Reply with ONLY the final integer.\n\n" + "\n".join(lines) + "\n\nFinal value of s?")
    return {"item_id": f"V6-E{E}-D{D}-s{seed}", "encode": E, "depth": D, "seed": seed,
            "s0": s0, "chain": chain, "prompt": prompt, "prompt_words": len(prompt.split()),
            "answer": answer}


def build_grid(seeds):
    return [gen_cell(E, D, s) for s in range(seeds) for E in E_LEVELS for D in D_LEVELS]


def oracle_recompute(item):
    """Independent replay from stored structure (s0 + chain), not the prompt string."""
    s = item["s0"]
    for (op, k) in item["chain"]:
        s = _apply(s, op, k)
    return s


def canonical_labels(items):
    return [{"item_id": it["item_id"], "encode": it["encode"], "depth": it["depth"],
             "seed": it["seed"], "answer": it["answer"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=12):
    import numpy as np
    items = build_grid(seeds)
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} replay-match", "OK" if not bad else f"FAIL {bad[:4]}")
    # design balance + the matched-answer check (E arms share s0+chain+answer within a (D,seed))
    cells = {}
    for it in items:
        cells.setdefault((it["encode"], it["depth"]), []).append(it)
    print("[design] 2x2 cell counts:", {k: len(v) for k, v in sorted(cells.items())})
    # E-arms must share answer within (D,seed); D-arms differ
    mism = []
    for s in range(seeds):
        for D in D_LEVELS:
            a0 = next(it["answer"] for it in items if it["encode"] == 0 and it["depth"] == D and it["seed"] == s)
            a3 = next(it["answer"] for it in items if it["encode"] == 3 and it["depth"] == D and it["seed"] == s)
            if a0 != a3:
                mism.append((s, D, a0, a3))
    print(f"[match] E=0 and E=3 share the answer within (D,seed): {'OK' if not mism else 'FAIL '+str(mism[:3])}")
    # report per-cell median prompt_words (E adds length; the interaction cancels it)
    for k in sorted(cells):
        w = np.median([it["prompt_words"] for it in cells[k]])
        print(f"   cell E={k[0]} D={k[1]:>2}: median prompt_words={w:.0f}")
    print("SELFTEST PASS" if not bad and not mism else "SELFTEST FAIL")


def write_lock(seeds):
    items = build_grid(seeds); labels = canonical_labels(items); digest = lock_digest(labels)
    (HERE / "v6_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v6_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "E_levels": E_LEVELS,
         "D_levels": D_LEVELS, "tier_preregistered": TIER_PREREG,
         "note": "Sternberg additive-factors; primary = interaction(encode x depth) on reasoning_tokens; additive(I~0)=separable serial stages"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v6_labels.jsonl + v6_labels.LOCK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--seeds", type=int, default=12)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    else: print("use --selftest or --lock --seeds N")
