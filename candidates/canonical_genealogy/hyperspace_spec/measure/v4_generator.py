#!/usr/bin/env python3
"""
V4 generator — the FACTORIAL Parametric Difficulty Ladder (codex/gemini fix #1).

The crux the external pass demanded: decouple EFFECTIVE difficulty from DISPLAY length,
so the headline partial-Spearman can ISOLATE effective difficulty instead of just measuring
prompt length (the autoregressive tautology both reviewers flagged as the #1 threat).

Construction (family CHAIN): an item has a TARGET total display-op count T chosen INDEPENDENTLY
of the effective-op count E. We print exactly T assignment statements; E of them form a
SEQUENTIAL dependency chain on the variable z (each uses the previous z), the other (T-E) are
INDEPENDENT distractor assignments to throwaway variables (never used). So:
    effective_ops = E      (the true reasoning depth; must be executed in order)
    display_ops   = T       (the visible surface complexity; SET INDEPENDENTLY of E)
=> corr(E, T) = 0 BY CONSTRUCTION (full factorial E x T), so partial-Spearman(effort, E | T,
   prompt_words) is identifiable: at a FIXED T, E still varies (T=20 is reachable by E=2..10).

The oracle replays the chain (ignoring distractors) deterministically -> a unique bounded
integer answer. Seeds make it reproducible. A SHA-256 LABEL-LOCK freezes every (E, T, answer)
BEFORE any model call (the pre-registration artifact; digestion_v4 refuses to run if the hash
moved). Stdlib + numpy(selftest only). Offline. Deterministic.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = 1000                      # keep z in 0..999 (short to print/extract)
E_BANDS = [2, 4, 6, 8, 10]      # effective_ops (5 bands)
T_LEVELS = [12, 16, 20]         # display_ops target, INDEPENDENT of E (3 levels)
OPS = [("+", lambda z, c: z + c), ("-", lambda z, c: z - c), ("*", lambda z, c: z * c)]


def gen_item(E, T, seed):
    """Deterministic factorial item. E chain-ops + (T-E) distractors, T total statements."""
    assert 0 < E <= T, f"need 0<E<=T, got E={E} T={T}"
    rng = random.Random(f"CHAIN|{E}|{T}|{seed}")
    z0 = rng.randint(10, 99)
    # build the E sequential chain statements (each depends on prior z)
    z = z0
    chain_stmts = [f"z = {z0}"]
    for _ in range(E):
        sym, fn = rng.choice(OPS)
        c = rng.randint(2, 9)
        z = fn(z, c) % MOD
        chain_stmts.append(f"z = (z {sym} {c}) % {MOD}")
    answer = z
    # build (T-E) INDEPENDENT distractor statements (throwaway vars, never used)
    n_distract = T - E
    distract_stmts = []
    for j in range(n_distract):
        sym, fn = rng.choice(OPS)
        a, c = rng.randint(10, 99), rng.randint(2, 9)
        distract_stmts.append(f"w{j} = ({a} {sym} {c}) % {MOD}")
    # interleave: keep chain statements in relative order, drop distractors at random positions
    body = list(chain_stmts)
    for d in distract_stmts:
        body.insert(rng.randint(1, len(body)), d)   # not before the z=z0 init
    prog = "\n".join(body)
    prompt = (
        "Execute these assignments in order. Variables w0, w1, ... are distractors you may ignore. "
        "Track only z. All arithmetic on z is mod " + str(MOD) + ".\n\n"
        + prog +
        "\n\nWhat is the final value of z? Reply with ONLY the final integer."
    )
    return {
        "item_id": f"CHAIN-E{E}-T{T}-s{seed}",
        "family": "CHAIN",
        "effective_ops": E,           # the reasoning-depth knob (primary x)
        "display_ops": T,             # the surface-length control (set independently of E)
        "distractors": n_distract,
        "prompt_words": len(prompt.split()),
        "seed": seed,
        "prompt": prompt,
        "answer": answer,
    }


def oracle_recompute(item):
    """Independently re-derive the answer by parsing the chain statements (selftest cross-check)."""
    z = None
    for line in item["prompt"].splitlines():
        line = line.strip()
        if line.startswith("z = ") and "%" not in line:        # z = <init>
            z = int(line.split("=")[1])
        elif line.startswith("z = (z "):                        # z = (z <op> c) % MOD
            inside = line.split("(z", 1)[1].split(")")[0].strip()
            sym, c = inside.split()
            c = int(c)
            z = {"+": z + c, "-": z - c, "*": z * c}[sym] % MOD
    return z


def build_grid(seeds):
    items = []
    for E in E_BANDS:
        for T in T_LEVELS:
            for s in range(seeds):
                items.append(gen_item(E, T, s))
    return items


def canonical_labels(items):
    """The frozen pre-registration content. Binds the full STIMULUS (prompt) + answer key, so the
    hash cannot pass if the rendered prompt changes (audit fix: the answer-key-only lock did not
    bind the stimulus or the effort tier)."""
    return [{"item_id": it["item_id"], "effective_ops": it["effective_ops"],
             "display_ops": it["display_ops"], "answer": it["answer"], "seed": it["seed"],
             "prompt": it["prompt"], "prompt_words": it["prompt_words"]}
            for it in items]


def lock_digest(labels):
    blob = json.dumps(labels, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def write_lock(seeds):
    items = build_grid(seeds)
    labels = canonical_labels(items)
    digest = lock_digest(labels)
    (HERE / "v4_labels.jsonl").write_text(
        "\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v4_labels.LOCK").write_text(
        json.dumps({"sha256": digest, "n_items": len(labels), "seeds": seeds,
                    "E_bands": E_BANDS, "T_levels": T_LEVELS, "tier_preregistered": "high",
                    "note": "factorial E _|_ T; binds full stimulus+answer; tier locked; primary estimand = partial-Spearman(effort, E | display_ops) on solved items"},
                   indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items  sha256={digest[:16]}...  -> v4_labels.jsonl + v4_labels.LOCK")
    return items, digest


def selftest(seeds=12):
    import numpy as np
    items = build_grid(seeds)
    # 1) oracle correctness: independent recompute must match generation
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} items recompute-match", "OK" if not bad else f"FAIL {bad[:5]}")
    # 2) THE DECOUPLING: corr(effective_ops, display_ops) must be ~0 by construction
    E = np.array([it["effective_ops"] for it in items], float)
    T = np.array([it["display_ops"] for it in items], float)
    W = np.array([it["prompt_words"] for it in items], float)
    cET = float(np.corrcoef(E, T)[0, 1])
    cEW = float(np.corrcoef(E, W)[0, 1])
    cTW = float(np.corrcoef(T, W)[0, 1])
    print(f"[decouple] corr(E, display_ops)={cET:+.3f}  (target ~0; this is the factorial fix)")
    print(f"[decouple] corr(E, prompt_words)={cEW:+.3f}   corr(display_ops, prompt_words)={cTW:+.3f}")
    # 3) identifiability: at each fixed T, E must still vary
    for t in T_LEVELS:
        evals = sorted({it["effective_ops"] for it in items if it["display_ops"] == t})
        print(f"[identify] at display_ops={t}: effective_ops takes {evals}  (need >=3 distinct)")
    # 4) answer sanity
    ans = [it["answer"] for it in items]
    print(f"[answers] range {min(ans)}..{max(ans)}  distinct={len(set(ans))}/{len(ans)}")
    assert not bad, "oracle mismatch"
    assert abs(cET) < 0.05, f"decoupling failed: corr(E,T)={cET}"
    print("SELFTEST PASS" if not bad and abs(cET) < 0.05 else "SELFTEST FAIL")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lock", action="store_true", help="write v4_labels.jsonl + v4_labels.LOCK")
    ap.add_argument("--seeds", type=int, default=12)
    a = ap.parse_args()
    if a.selftest:
        selftest(a.seeds)
    elif a.lock:
        write_lock(a.seeds)
    else:
        print("use --selftest or --lock --seeds N")
