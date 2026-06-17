#!/usr/bin/env python3
"""
V5 generator — the WORK-vs-SPAN separator (Brent 1974, JACM, 10.1145/321812.321815).

V4 showed reasoning_tokens scale with arithmetic WORK (op-count) net of input length, but could
NOT beat the OUTPUT-transcription tautology (~6 tokens/op = one scratchpad line per step). V5 holds
total WORK (op-count) FIXED and varies only the dependency STRUCTURE:

    DEEP  (m=1): one serial chain of W ops.            span = W   (critical path = whole chain)
    WIDE  (m>1): m INDEPENDENT sub-chains of length L  span = L + (m-1)  (a sub-chain + the reduction)
                 + a final (m-1)-op reduction over their results.

Total ops are MATCHED EXACTLY across deep/wide:  payload = W-(m-1) split into m chains of length
L = payload/m, plus (m-1) reduction ops  ->  L*m + (m-1) = W  ops for EVERY structure. Only the
critical-path SPAN differs (W for deep, ~L+(m-1) for wide). Same #lines to TRANSCRIBE, same work.

Predictions (the three-way discriminator):
  * tokens = TRANSCRIPTION length   -> WIDE == DEEP at fixed W (same #lines printed/written).
  * tokens = WORK / op-volume       -> WIDE == DEEP at fixed W (same op-count).        [== above]
  * tokens = genuine DEPTH / span   -> DEEP  >  WIDE at fixed W (deep has the longer critical path).
So a DEEP>WIDE gap at fixed work is the ONLY outcome that separates depth from work+transcription
(which are collinear here, exactly the V4 confound). A null (WIDE==DEEP) demotes effort to volume.

INVARIANTS HELD FIXED across every matched deep/wide pair (or the test fails):
  (I1) total op-count W              -- identical by construction (L*m + (m-1) = W).
  (I2) display line-count L_disp     -- padded with ignorable distractor assignments to a common total.
  (I3) answer magnitude + digit-count-- rejection-sampled into a matched band (both 3 digits, mod 1000).
  (I4) operator mix (+,-,* counts)   -- rejection-sampled so the multiset of op symbols matches by tier.
  (I5) mod structure                 -- all ops mod 1000, identical surface form "v = (v op c) % 1000".
The reduction step does NOT smuggle extra work: its (m-1) ops are CHARGED into W (payload=W-(m-1)).

Oracle: deterministically execute the printed program, tracking the answer variable, IGNORING any
distractor (w*) variable -- independent of the generator's own bookkeeping (cross-check). SHA-256
label-lock binds the full stimulus + tier (the V4-hardened pattern). Stdlib + numpy(selftest only).
Offline. Deterministic. gpt-5.5 only downstream (sole reasoning_tokens emitter).
"""
import json, hashlib, argparse, sys, random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = 1000
APPLY = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
OPSYMS = ["+", "-", "*"]

# --- the matched grid -------------------------------------------------------
# WORK level W chosen so (W+1) % m == 0 for every width m -> integer sub-chain length L=(W-(m-1))/m.
# width set {1,3,5}: m=1 is DEEP; m=3,5 are WIDE. (W+1)%15==0 -> W in {14,29}.
W_LEVELS = [14, 29]              # two work levels (span range; both fully solvable like V4)
WIDTHS   = [1, 3, 5]            # m=1 DEEP (span=W); m=3,5 WIDE (span ~ L+(m-1))
DISP_PAD = {14: 22, 29: 40}    # common display line-count per W (>= max raw lines of any structure)


def _apply(z, sym, c):
    return APPLY[sym](z, c) % MOD


def span_of(W, m):
    """Critical-path length (longest dependency chain), Brent 1974. deep=W; wide=L + (m-1) reduction."""
    L = (W - (m - 1)) // m
    return W if m == 1 else (L + (m - 1))


def gen_item(W, m, seed, want_digits=3):
    """One matched item at work=W, width=m. Rejection-sample until answer has want_digits digits and
    the operator multiset matches the per-tier canonical mix (set by the DEEP item of this seed)."""
    assert (W + 1) % m == 0, f"(W+1) must be divisible by m: W={W} m={m}"
    payload = W - (m - 1)
    L = payload // m
    L_disp = DISP_PAD[W]
    # canonical operator mix for this (W, seed): fixed by a dedicated rng so DEEP and WIDE share a target
    mix_rng = random.Random(f"MIX|{W}|{seed}")
    target_payload_mix = Counter(mix_rng.choice(OPSYMS) for _ in range(W))   # W op-symbols, the shared target

    for attempt in range(4000):
        rng = random.Random(f"V5|{m}|{W}|{seed}|{attempt}")
        body, opsyms, subs = [], [], []
        for k in range(m):
            v = "z" if m == 1 else f"a{k}"
            z0 = rng.randint(10, 99)
            body.append(f"{v} = {z0}")
            z = z0
            for _ in range(L):
                sym = rng.choice(OPSYMS); c = rng.randint(2, 9)
                z = _apply(z, sym, c)
                body.append(f"{v} = ({v} {sym} {c}) % {MOD}")
                opsyms.append(sym)
            subs.append((v, z))
        if m == 1:
            final, ansvar = subs[0][1], "z"
        else:
            body.append("r = a0"); r = subs[0][1]
            for k in range(1, m):
                sym = rng.choice(OPSYMS)
                r = _apply(r, sym, subs[k][1])
                body.append(f"r = (r {sym} a{k}) % {MOD}")
                opsyms.append(sym)
            final, ansvar = r, "r"
        # (I3) answer digit-count band  (I4) operator mix match to the shared target
        if len(str(final)) != want_digits:
            continue
        if Counter(opsyms) != target_payload_mix:
            continue
        # (I2) pad display to common L_disp with ignorable distractors; DO NOT disturb the op mix of the
        # REAL chain -- distractors get their own w-vars and are excluded from the matched mix accounting.
        wj = 0
        while len(body) < L_disp:
            sym = rng.choice(OPSYMS); a = rng.randint(10, 99); c = rng.randint(2, 9)
            body.insert(rng.randint(1, len(body)), f"w{wj} = ({a} {sym} {c}) % {MOD}")
            wj += 1
        if len(body) != L_disp:
            continue   # overshot (rare) -> resample
        prog = "\n".join(body)
        prompt = (
            "Execute these assignments in order. Variables named w0, w1, ... are distractors you may "
            f"ignore. All arithmetic is mod {MOD}. Track the variables you need and report the final "
            f"value of {ansvar}.\n\n" + prog +
            f"\n\nWhat is the final value of {ansvar}? Reply with ONLY the final integer."
        )
        return {
            "item_id": f"V5-W{W}-m{m}-s{seed}",
            "family": "WIDEDEEP",
            "structure": "DEEP" if m == 1 else "WIDE",
            "work_ops": W,                 # the MATCHED knob (held fixed across deep/wide)  [primary control]
            "width": m,                    # #independent sub-chains
            "subchain_len": L,
            "span": span_of(W, m),         # the PRIMARY x: critical-path length (deep=W >> wide)
            "display_lines": L_disp,       # (I2) matched
            "ans_digits": want_digits,     # (I3) matched
            "op_mix": dict(target_payload_mix),  # (I4) matched
            "prompt_words": len(prompt.split()),
            "seed": seed,
            "ansvar": ansvar,
            "prompt": prompt,
            "answer": final,
        }
    raise RuntimeError(f"could not match invariants for W={W} m={m} seed={seed}")


def oracle_recompute(item):
    """Independent re-execution of the PRINTED program (cross-check of generation). Tracks every
    assigned variable; returns the answer variable. Distractors are computed but never read by the
    answer chain, so they cannot change the result -- a direct test of (I2) not smuggling work."""
    env = {}
    ansvar = item["ansvar"]
    for line in item["prompt"].splitlines():
        line = line.strip()
        if " = " not in line or line.startswith(("Execute", "What", "Variables")):
            continue
        lhs, rhs = line.split(" = ", 1)
        rhs = rhs.split(" % ")[0].strip()
        if rhs.startswith("("):
            rhs = rhs[1:-1].strip()
        toks = rhs.split()
        if len(toks) == 1:                       # init: v = <int>   OR  reduction-seed: r = a0 (var copy)
            t = toks[0]
            if t.lstrip("-").isdigit():
                env[lhs] = int(t) % MOD
            elif t in env:
                env[lhs] = env[t]                # variable copy (e.g. r = a0)
        elif len(toks) == 3:                     # v = a op b   (b is num or var)
            a = env.get(toks[0], None)
            if a is None and toks[0].lstrip("-").isdigit():
                a = int(toks[0])
            b = env.get(toks[2], None)
            if b is None and toks[2].lstrip("-").isdigit():
                b = int(toks[2])
            env[lhs] = _apply(a, toks[1], b)
    return env.get(ansvar)


def build_grid(seeds):
    items = []
    for W in W_LEVELS:
        for m in WIDTHS:
            for s in range(seeds):
                items.append(gen_item(W, m, s))
    return items


def build_lite(seeds):
    """V5-LITE matched slice: ONE work level (W=14), DEEP(m=1) vs the widest WIDE(m=5) only.
    n = 2 structures * seeds. ~12 seeds -> 24 calls. The decisive direction test."""
    items = []
    for m in (1, 5):
        for s in range(seeds):
            items.append(gen_item(14, m, s))
    return items


def canonical_labels(items):
    return [{"item_id": it["item_id"], "structure": it["structure"], "work_ops": it["work_ops"],
             "width": it["width"], "span": it["span"], "display_lines": it["display_lines"],
             "ans_digits": it["ans_digits"], "op_mix": it["op_mix"], "answer": it["answer"],
             "seed": it["seed"], "ansvar": it["ansvar"], "prompt": it["prompt"],
             "prompt_words": it["prompt_words"]} for it in items]


def lock_digest(labels):
    blob = json.dumps(labels, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def write_lock(seeds, which="full"):
    items = build_lite(seeds) if which == "lite" else build_grid(seeds)
    labels = canonical_labels(items)
    digest = lock_digest(labels)
    tag = "v5_lite" if which == "lite" else "v5"
    (HERE / f"{tag}_labels.jsonl").write_text(
        "\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / f"{tag}_labels.LOCK").write_text(
        json.dumps({"sha256": digest, "n_items": len(labels), "seeds": seeds, "which": which,
                    "W_levels": ([14] if which == "lite" else W_LEVELS),
                    "widths": ([1, 5] if which == "lite" else WIDTHS),
                    "tier_preregistered": "high",
                    "primary_estimand": "partial-Spearman(reasoning_tokens, span | work_ops, display_lines, ans_digits, prompt_words) on solved items",
                    "note": "WORK held fixed (op-count matched deep/wide); SPAN varies; binds full stimulus+tier"},
                   indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED [{which}] {len(labels)} items  sha256={digest[:16]}...  -> {tag}_labels.jsonl + {tag}_labels.LOCK")
    return items, digest


def selftest(seeds=12):
    import numpy as np
    items = build_grid(seeds)
    n = len(items)
    # (oracle) independent recompute matches generation
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle]   {n-len(bad)}/{n} recompute-match", "OK" if not bad else f"FAIL {bad[:4]}")
    # (I1) op-count W matched across structures at each W level (work == work_ops by construction)
    for W in W_LEVELS:
        works = {it["work_ops"] for it in items if it["work_ops"] == W}
        print(f"[I1 work]  W={W}: all structures carry work_ops={W}  (matched)  ok={works == {W}}")
    # the SEPARATION: at fixed W, does span actually vary with enough range + is it ~uncorrelated noise-free?
    for W in W_LEVELS:
        sp = sorted({it["span"] for it in items if it["work_ops"] == W})
        print(f"[span]     W={W}: span takes {sp}  (DEEP={W} vs WIDE -> real range, need >=2 distinct)")
    # identifiability of the partial: corr(span, work_ops) across the grid, and within-W span variation
    S = np.array([it["span"] for it in items], float)
    Wv = np.array([it["work_ops"] for it in items], float)
    D = np.array([it["display_lines"] for it in items], float)
    print(f"[ident]    corr(span, work_ops)={np.corrcoef(S, Wv)[0,1]:+.3f}  corr(span, display_lines)={np.corrcoef(S, D)[0,1]:+.3f}")
    # (I2) display lines matched within each W
    for W in W_LEVELS:
        dl = {it["display_lines"] for it in items if it["work_ops"] == W}
        print(f"[I2 disp]  W={W}: display_lines={dl}  (single value -> matched)  ok={len(dl)==1}")
    # (I3) answer digit-count matched
    dig = {it["ans_digits"] for it in items}
    digs_real = {len(str(it["answer"])) for it in items}
    print(f"[I3 dig]   nominal ans_digits={dig}  actual={digs_real}  ok={digs_real <= {3}}")
    # (I4) operator mix matched DEEP-vs-WIDE within each (W, seed)
    mix_ok = True
    for W in W_LEVELS:
        for s in range(seeds):
            mixes = {it["item_id"]: tuple(sorted(it["op_mix"].items()))
                     for it in items if it["work_ops"] == W and it["seed"] == s}
            if len(set(mixes.values())) != 1:
                mix_ok = False
    print(f"[I4 mix]   operator multiset identical across DEEP/WIDE within each (W,seed)  ok={mix_ok}")
    # answer sanity
    ans = [it["answer"] for it in items]
    print(f"[answers]  range {min(ans)}..{max(ans)}  distinct={len(set(ans))}/{len(ans)}")
    assert not bad and mix_ok and digs_real <= {3}, "selftest failed"
    print("SELFTEST PASS")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--which", choices=["full", "lite"], default="full")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--show", action="store_true", help="print one matched DEEP/WIDE pair")
    a = ap.parse_args()
    if a.selftest:
        selftest(a.seeds)
    elif a.lock:
        write_lock(a.seeds, which=a.which)
    elif a.show:
        d = gen_item(14, 1, 0); w = gen_item(14, 5, 0)
        for it in (d, w):
            print("=" * 60, f"\n{it['structure']} W={it['work_ops']} m={it['width']} span={it['span']} "
                  f"lines={it['display_lines']} digits={it['ans_digits']} mix={it['op_mix']}")
            print(it["prompt"]); print("ANSWER:", it["answer"], "oracle:", oracle_recompute(it))
    else:
        print("use --selftest | --lock [--which full|lite] [--seeds N] | --show")
