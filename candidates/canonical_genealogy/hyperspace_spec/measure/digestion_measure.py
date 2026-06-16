#!/usr/bin/env python3
"""
The real digestion-measurement run (V1) — the first LIVE stream the Ticker can read.

Reuses the validated P1 coder (OpenAI echo+logprobs, exact codelength = arithmetic-coding bits).
For each target W we measure rho(prior-depth): the residue cond(W | context_d) as we hand the
observer increasingly relevant PRIOR (the digestion / amortization). Contexts give RELATED prior,
never W verbatim (so we measure genuine dissolve, not a lookup — the Goodhart confound the
external pass flagged).

  cost_bits(t)   = -sum logprob(token_t)/ln2        (one echo call, max_tokens=0)
  cond(W|ctx)    = max(0, cost(ctx+W) - cost(ctx))  (the residue under that prior)
  TWO CLOCKS     present = cond(W|cold) ; amortized = cond(W|deep prior) ; gap = present - amortized
  ALEATORIC vs EPISTEMIC: a random string stays flat-high (no prior dissolves it = the floor);
                          a structured fact drops as the right prior is given (epistemic, digestible).

Synthetic, non-sensitive targets only. Spends Pav's OPENAI_API_KEY (authorized 2026-06-16, P1).
"""
import os, json, math, urllib.request, urllib.error, sys, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = os.environ.get("CANON_OPENAI_MODEL", "davinci-002")  # base model: echo+logprobs+max_tokens=0
LN2 = math.log(2)
_memo = {}

def cost_bits(text):
    if text in _memo:
        return _memo[text]
    req = urllib.request.Request(
        "https://api.openai.com/v1/completions",
        data=json.dumps({"model": MODEL, "prompt": text, "max_tokens": 0,
                         "echo": True, "logprobs": 1, "temperature": 0}).encode("utf-8"),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=90) as r:
        resp = json.loads(r.read().decode("utf-8"))
    lp = resp["choices"][0]["logprobs"]["token_logprobs"]
    bits = -sum(x for x in lp if x is not None) / LN2
    _memo[text] = bits
    return bits

def cond(W, ctx):
    if not ctx.strip():                 # cold: empty context costs ~0; avoid the 1-token API error
        return cost_bits(W)
    return max(0.0, cost_bits(ctx + W) - cost_bits(ctx))

# A fixed random string (the aleatoric control) — high-entropy, no prior can dissolve it.
random.seed(7)
RAND = " ".join(random.choice(["qx","vmt","zol","bree","kud","wint","paxu","jorl","theb","gnis","ulf","drav"])
                for _ in range(10))

# targets: (id, kind, W, [contexts depth 0..N], expectation)
# contexts give RELATED prior, never W verbatim.
TARGETS = [
    ("common", "epistemic", " The Earth orbits the Sun once each year.",
     ["", " In astronomy, bodies move under gravity.",
      " In astronomy, planets move around stars under gravity. The Earth is a planet; the Sun is a star."],
     "should DISSOLVE: the right prior makes W highly predictable"),
    ("arithmetic", "epistemic", " Seven times eight equals fifty-six.",
     ["", " Consider basic arithmetic.",
      " Consider basic multiplication tables. We are computing the product of seven and eight."],
     "should DISSOLVE: derivable once the operation is framed"),
    ("specific", "mixed", " The QX-440 pressure valve opens at 3.2 bar.",
     ["", " Industrial pressure valves have set-points.",
      " Industrial pressure valves open near 3 bar. The QX-440 is one such pressure valve."],
     "PARTIAL: the kind dissolves, the exact 3.2 stays (residual specific bits)"),
    ("random", "aleatoric", " " + RAND + ".",
     ["", " Here is a sequence of tokens.",
      " Here is a sequence of unrelated nonsense tokens with no pattern or meaning."],
     "should STAY FLAT-HIGH: no prior dissolves incompressible noise = the aleatoric floor"),
]

def main():
    if not KEY:
        print("OPENAI_API_KEY not set."); sys.exit(2)
    print(f"=== digestion-measurement V1 (echo-codelength, model={MODEL}) ===\n")
    stream = []
    try:
        for tid, kind, W, ctxs, exp in TARGETS:
            row = []
            for depth, ctx in enumerate(ctxs):
                r = cond(W, ctx)
                row.append(r)
                stream.append({"target": tid, "kind": kind, "depth": depth,
                               "context_chars": len(ctx), "residue_bits": round(r, 2)})
            present = row[0]; amortized = row[-1]
            gap = round(present - amortized, 2)
            drop = round(1 - amortized / present, 3) if present > 0 else 0.0
            stream.append({"target": tid, "kind": kind, "two_clock_present": round(present, 2),
                           "two_clock_amortized": round(amortized, 2), "two_clock_gap": gap, "dissolved_frac": drop})
            print(f"[{tid:11s} {kind:9s}] rho(depth)= " + " -> ".join(f"{x:6.1f}" for x in row) +
                  f"   present={present:6.1f} amortized={amortized:6.1f} gap={gap:+6.1f} dissolved={drop:+.2f}")
            print(f"    {exp}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        print(f"HTTPError {e.code}: {body}")
        print("  retry with CANON_OPENAI_MODEL=babbage-002 or gpt-3.5-turbo-instruct"); sys.exit(3)
    except Exception as e:
        print(f"call failed: {type(e).__name__}: {e}"); sys.exit(3)

    (HERE).mkdir(exist_ok=True)
    (HERE/"measurement_run.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in stream) + "\n", encoding="utf-8")
    # the headline test: does the random string resist while structured facts dissolve?
    byid = {t[0]: t[1] for t in TARGETS}
    drops = {s["target"]: s.get("dissolved_frac") for s in stream if "dissolved_frac" in s}
    rand_resists = drops.get("random", 1) < 0.25
    struct_dissolve = all(drops.get(t, 0) > 0.25 for t in ("common", "arithmetic"))
    print(f"\nHEADLINE: random resists (aleatoric floor, dissolved<0.25) = {rand_resists} "
          f"(random dissolved={drops.get('random')}); structured facts dissolve (>0.25) = {struct_dissolve}")
    print(f"  => the aleatoric/epistemic split is {'OBSERVED in real codelength' if rand_resists and struct_dissolve else 'NOT cleanly observed'}")
    print(f"  wrote measurement_run.jsonl ({len(stream)} records)")

if __name__ == "__main__":
    main()
