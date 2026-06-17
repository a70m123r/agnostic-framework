#!/usr/bin/env python3
"""
V5 WIDE-vs-DEEP, REBUILT to neutralize the transcription/working-set confound (the v5-design
audit superseded the first build: span was collinear with prompt_words/attended-lines/distractors/
live-vars). This design makes DEEP and WIDE a MATCHED PAIR that is identical in everything a
transcription or memory-load account could use, and differs ONLY in critical-path span:

  Both members:  m registers r0..r_{m-1}; m init lines; K=m*k update lines; (m-1) reduction lines.
                 Every update line is "rX = (rY <op> c) % 1000" -> identical word/line count and the
                 SAME multiset of (op, c). Both track m live variables. Same final reduction.
  DEEP wiring:   update i writes r_{i%m}, READS r_{(i-1)%m}  -> ONE serial chain. span = K + (m-1).
  WIDE wiring:   update i writes r_{i%m}, READS r_{i%m}      -> m independent chains. span = k + (m-1).

So within a (m,k,seed) PAIR: prompt_words, display_lines, work_ops, live_vars, op-multiset, and
(by accept/resample) answer-digit-count are EQUAL; only the source-register routing -> only SPAN
differs. The paired contrast tokens(DEEP)-tokens(WIDE) therefore isolates serial depth, free of the
transcription confound BY CONSTRUCTION. The selftest GATE asserts per-pair matching before any spend.
Stdlib only (numpy for selftest stats). Deterministic. sha256 lock binds full stimulus + tier.
"""
import json, hashlib, argparse, sys, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = 1000
OPS = ["+", "-", "*"]
LITE_CELLS = [(4, 4), (2, 6)]      # (m, k): K=16 span-gap 19vs7 ; K=12 span-gap 13vs7
TIER_PREREG = "high"


def _apply(z, op, c):
    return {"+": z + c, "-": z - c, "*": z * c}[op] % MOD


def gen_member(structure, m, k, seeds, ops):
    """Build one member (DEEP or WIDE) from shared seeds + ops. Returns (statements, answer, span)."""
    K = m * k
    reg = list(seeds)                                  # r0..r_{m-1}
    stmts = [f"r{j} = {seeds[j]}" for j in range(m)]
    for i in range(K):
        op, c = ops[i]
        tgt = i % m
        src = tgt if structure == "WIDE" else ((i - 1) % m if i > 0 else (m - 1))
        reg[tgt] = _apply(reg[src], op, c)
        stmts.append(f"r{tgt} = (r{src} {op} {c}) % {MOD}")
    # identical serial reduction into s for BOTH members
    s = reg[0]
    stmts.append("s = r0")
    for j in range(1, m):
        s = (s + reg[j]) % MOD
        stmts.append(f"s = (s + r{j}) % {MOD}")
    span = (K if structure == "DEEP" else k) + (m - 1)
    return stmts, s, span


def _prompt(stmts):
    return ("Execute these assignments in order, tracking every variable. All arithmetic is mod "
            + str(MOD) + ".\n\n" + "\n".join(stmts) +
            "\n\nWhat is the final value of s? Reply with ONLY the final integer.")


def gen_pair(m, k, seed):
    """A matched DEEP/WIDE pair from one seed; resample until answer digit-counts match."""
    for attempt in range(200):
        rng = random.Random(f"WD|{m}|{k}|{seed}|{attempt}")
        seeds = [rng.randint(10, 99) for _ in range(m)]
        ops = [(rng.choice(OPS), rng.randint(2, 9)) for _ in range(m * k)]
        d_st, d_ans, d_span = gen_member("DEEP", m, k, seeds, ops)
        w_st, w_ans, w_span = gen_member("WIDE", m, k, seeds, ops)
        if len(str(d_ans)) == len(str(w_ans)):         # match answer-digit count
            mk = lambda st, ans, span, struct: {
                "item_id": f"WD-{struct}-m{m}k{k}-s{seed}", "structure": struct,
                "m": m, "k": k, "work_ops": m * k + (m - 1), "span": span, "width": m,
                "live_vars": m, "display_lines": len(st), "prompt": _prompt(st),
                "prompt_words": len(_prompt(st).split()), "ans_digits": len(str(ans)),
                "answer": ans, "seed": seed}
            return mk(d_st, d_ans, d_span, "DEEP"), mk(w_st, w_ans, w_span, "WIDE")
    raise RuntimeError(f"no digit-matched pair for m{m}k{k}s{seed}")


def build_lite(seeds, cells=LITE_CELLS):
    items = []
    for (m, k) in cells:
        for s in range(seeds):
            d, w = gen_pair(m, k, s)
            items += [d, w]
    return items


def oracle_recompute(item):
    """Independent parse-replay of the printed program (cross-check vs generation). Handles all four
    statement forms: 'rJ = <int>' (init), 'rX = (rY op c) % MOD' (update), 's = r0' (copy),
    's = (s + rJ) % MOD' (reduce)."""
    env = {}
    for line in item["prompt"].splitlines():
        line = line.strip()
        if "=" not in line or not (line.startswith("r") or line.startswith("s")):
            continue
        tgt, rhs = line.split("=", 1); tgt, rhs = tgt.strip(), rhs.strip()
        if "(" in rhs:                                              # (a op b) % MOD
            a, op, b = rhs.split("(", 1)[1].split(")", 1)[0].strip().split()
            av = env[a] if a in env else int(a)
            bv = env[b] if b in env else int(b)
            env[tgt] = {"+": av + bv, "-": av - bv, "*": av * bv}[op] % MOD
        else:                                                       # int literal or a var copy
            env[tgt] = env[rhs] if rhs in env else int(rhs)
    return env.get("s")


def canonical_labels(items):
    return [{"item_id": it["item_id"], "structure": it["structure"], "m": it["m"], "k": it["k"],
             "span": it["span"], "work_ops": it["work_ops"], "answer": it["answer"],
             "seed": it["seed"], "prompt": it["prompt"]} for it in items]


def lock_digest(labels):
    return hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def selftest(seeds=8):
    import numpy as np
    items = build_lite(seeds)
    pairs = {}
    for it in items:
        pairs.setdefault((it["m"], it["k"], it["seed"]), {})[it["structure"]] = it
    # 1) oracle correctness
    bad = [it["item_id"] for it in items if oracle_recompute(it) != it["answer"]]
    print(f"[oracle] {len(items)-len(bad)}/{len(items)} parse-replay match", "OK" if not bad else f"FAIL {bad[:4]}")
    # 2) PER-PAIR MATCH GATE — everything equal except span
    fields = ["prompt_words", "display_lines", "work_ops", "live_vars", "ans_digits"]
    mism = []
    span_gaps = []
    for key, pr in pairs.items():
        if "DEEP" not in pr or "WIDE" not in pr:
            mism.append((key, "incomplete")); continue
        d, w = pr["DEEP"], pr["WIDE"]
        for f in fields:
            if d[f] != w[f]:
                mism.append((key, f"{f}: {d[f]}!={w[f]}"))
        if d["span"] <= w["span"]:
            mism.append((key, f"span not deep>wide: {d['span']}<={w['span']}"))
        span_gaps.append((d["span"], w["span"]))
    print(f"[pair-match] {len(pairs)-len(set(k for k,_ in mism))}/{len(pairs)} pairs match on {fields} (span differs)",
          "OK" if not mism else f"FAIL {mism[:4]}")
    # 3) decoupling: across the pooled set, does span correlate with the transcription/memory covariates?
    def corr(a, b):
        a, b = np.array(a, float), np.array(b, float)
        if a.std() == 0 or b.std() == 0: return 0.0
        return float(np.corrcoef(a, b)[0, 1])
    span = [it["span"] for it in items]
    for f in ["prompt_words", "display_lines", "live_vars", "ans_digits"]:
        print(f"[decouple] corr(span, {f:13s}) = {corr(span, [it[f] for it in items]):+.3f}  (want ~0)")
    print(f"[decouple] corr(span, work_ops)    = {corr(span, [it['work_ops'] for it in items]):+.3f}  (work is CONTROLLED, not decoupled; the paired test holds it equal)")
    print(f"[span] gaps (deep,wide): {sorted(set(span_gaps))}")
    ok = (not bad) and (not mism)
    # the load-bearing decoupling check: within every pair, words/lines/vars are EQUAL, so
    # corr(span, words) across pooled data comes only from the cross-cell K change, which the
    # paired primary cancels. Report the WITHIN-PAIR confound = 0 by the pair-match gate.
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return ok


def write_lock(seeds):
    items = build_lite(seeds)
    labels = canonical_labels(items)
    digest = lock_digest(labels)
    (HERE / "v5wd_labels.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in labels) + "\n", encoding="utf-8")
    (HERE / "v5wd_labels.LOCK").write_text(json.dumps(
        {"sha256": digest, "n_items": len(labels), "seeds": seeds, "cells": LITE_CELLS,
         "tier_preregistered": TIER_PREREG,
         "note": "matched DEEP/WIDE pairs; per-pair words/lines/vars/work/digits equal, only span differs; primary = paired median(tokens DEEP-WIDE)"},
        indent=2) + "\n", encoding="utf-8")
    print(f"LOCKED {len(labels)} items sha256={digest[:16]}... -> v5wd_labels.jsonl + v5wd_labels.LOCK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--seeds", type=int, default=8)
    a = ap.parse_args()
    if a.selftest: selftest(a.seeds)
    elif a.lock: write_lock(a.seeds)
    else: print("use --selftest or --lock --seeds N")
