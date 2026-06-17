#!/usr/bin/env python3
"""
V4 re-analysis — FREE follow-ups on the already-collected v4_run.jsonl (no new API spend),
answering the audit's load-bearing caveats:
  (1) POST-HOC INTEGRITY: do the 180 run records match the regenerated oracle? (compensates
      for the answer-key-only lock by verifying the stimulus deterministically.)
  (2) ROBUSTNESS: does the E->effort partial SURVIVE additionally controlling for ANSWER
      MAGNITUDE + DIGIT COUNT? (tests "effort tracks arithmetic VOLUME/magnitude" vs the knob.)
  (3) RIGHT-TRUNCATION: per-band reasoning_token distribution — does the top band pile up at a
      soft budget ceiling under effort='high'?
"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v4_generator import build_grid
from v4_stats import partial_spearman, bootstrap_ci, perm_pvalue, raw_spearman

recs = [json.loads(l) for l in (HERE / "v4_run.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
grid = {it["item_id"]: it for it in build_grid(12)}

# (1) integrity
mism = [r["target"] for r in recs if r["target"] not in grid or grid[r["target"]]["answer"] != r["expected"]]
print(f"(1) INTEGRITY: {len(recs)-len(mism)}/{len(recs)} run records match the regenerated oracle",
      "OK" if not mism else f"MISMATCH {mism[:5]}")

solved = [r for r in recs if r["correct"] and r["reasoning_tokens"] is not None]
eff = [r["reasoning_tokens"] for r in solved]
E   = [r["effective_ops"] for r in solved]
T   = [r["display_ops"] for r in solved]
W   = [r["prompt_words"] for r in solved]
ans = [abs(r["expected"]) for r in solved]
dig = [len(str(abs(r["expected"]))) for r in solved]
rng = np.random.default_rng(7)

def show(name, controls):
    rho = partial_spearman(eff, E, controls)
    p, _ = perm_pvalue(eff, E, controls, rng, n=3000)
    ci = bootstrap_ci(eff, E, controls, rng, n=1500)
    print(f"   partial(effort, E | {name:38s}) = {rho:+.3f}  CI[{ci[0]:+.3f},{ci[1]:+.3f}]  p={p:.4f}")

print(f"\n(2) ROBUSTNESS  (n_solved={len(solved)}; does the E->effort signal survive volume controls?)")
show("display_ops)  [PRIMARY]", [T])
show("display_ops, prompt_words)", [T, W])
show("display_ops, ANSWER_MAGNITUDE)", [T, ans])
show("display_ops, ANSWER_DIGITS)", [T, dig])
show("display_ops, ANS_MAG, ANS_DIGITS)", [T, ans, dig])
print(f"   raw Spearman(effort, E)={raw_spearman(eff,E):+.3f}  raw Spearman(effort, answer_magnitude)={raw_spearman(eff,ans):+.3f}  raw(effort, display_ops)={raw_spearman(eff,T):+.3f}")
print("   read: if the partial stays high with ANSWER_MAGNITUDE controlled, effort is not merely tracking the numeric size carried; if it collapses, the knob was magnitude.")

print("\n(3) RIGHT-TRUNCATION  (per effective_ops band; pile-up at a common max = budget ceiling, not need)")
for e in sorted(set(E)):
    tk = np.array([eff[i] for i in range(len(eff)) if E[i] == e])
    at_max = int((tk == tk.max()).sum())
    print(f"   E={e:>2}: n={len(tk):>2}  min={tk.min():>3.0f}  med={np.median(tk):>4.0f}  max={tk.max():>4.0f}  std={tk.std():>4.0f}  (#@max={at_max})")
