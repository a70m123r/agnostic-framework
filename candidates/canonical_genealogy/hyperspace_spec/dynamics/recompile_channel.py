#!/usr/bin/env python3
"""
Procedural PER-CHANNEL recompile of the agnostic substrate (Pav's X*n intuition):
render n wrappers at once -> form CONSTELLATIONS (emergent-W_C clusters) + BRANCHES
(lineage trees), tuned for a channel's consumption. L0 is the source of truth; each
channel is a derived MATERIALIZED VIEW.

THE HONESTY SEAM (aggregation-faithfulness + spread-of-means): the emergent W_C can
never render sharper than its members support --
  render(W_C) <= mean(member render) * (1 - penalty(spread))   [bits_discarded = the spread]
A tight constellation earns a crisp emergent; a loose one stays fuzzy. No fake centroid.

Input:  compiled/dynamics.compiled.json (88 records: creatures + tactics + couplings)
Output: compiled/channel_<name>.json per channel config (constellations + branches + stats)
Stdlib only. Deterministic.
"""
import json, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
recs = json.loads((HERE/"compiled"/"dynamics.compiled.json").read_text(encoding="utf-8"))["records"]

def emergent_render(members):
    """COIN-honest emergent W_C sharpness: mean member render, blurred by disagreement (spread)."""
    rs = [float(m.get("render", m.get("certainty", 0.5)) or 0.5) for m in members]
    if not rs:
        return 0.0, 0.0
    mean = sum(rs) / len(rs)
    spread = statistics.pstdev(rs) if len(rs) > 1 else 0.0
    penalty = min(0.6, 2.0 * spread)            # bits_discarded -> blur (capped 60%)
    return round(max(0.0, mean * (1 - penalty)), 3), round(spread, 3)

def recompile(channel, constellate_by="family", branch_by="creatures_underlain"):
    # --- CONSTELLATIONS: group the n wrappers; surface each cluster's emergent W_C ---
    groups = {}
    for r in recs:
        groups.setdefault(r.get(constellate_by, "?"), []).append(r)
    constellations = []
    for key, members in sorted(groups.items()):
        render, spread = emergent_render(members)
        constellations.append({
            "emergent_W_C": key,                # the canonical center the constellation renders
            "n": len(members),
            "render": render,                   # <= members support (aggregation-faithfulness)
            "spread": spread,                   # disagreement = bits_discarded = the blur
            "honest": "tight->crisp" if spread < 0.08 else ("loose->fuzzy" if spread > 0.18 else "mid"),
            "members": [{"id": m["id"], "name": m["name"], "type": m["type"],
                         "render": m.get("render")} for m in members],
        })
    constellations.sort(key=lambda c: -c["render"])
    # --- BRANCHES: the lineage trees (tactic/organ -> the creatures it generates) ---
    branches = []
    for r in recs:
        leaves = r.get(branch_by) or []
        if leaves:
            branches.append({"root": r["name"], "root_id": r["id"], "root_type": r["type"],
                             "n_leaves": len(leaves), "leaves": leaves})
    branches.sort(key=lambda b: -b["n_leaves"])
    out = {
        "_meta": {"what": f"per-channel recompile of the agnostic dynamics substrate for '{channel}'",
                  "law": "render(W_C) <= members support - bits_discarded; channel = materialized view of L0"},
        "channel": channel, "config": {"constellate_by": constellate_by, "branch_by": branch_by},
        "constellations": constellations, "branches": branches,
        "stats": {"constellations": len(constellations), "branches": len(branches), "records": len(recs)},
    }
    (HERE/"compiled").mkdir(exist_ok=True)
    (HERE/"compiled"/f"channel_{channel}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out

# example channel configs (the running workflow's Guess-Who / Ticker specs add more)
CHANNELS = [("jungle", "family"), ("battlefield", "type")]
for ch, cb in CHANNELS:
    o = recompile(ch, constellate_by=cb)
    print(f"[{ch}] constellate-by={cb}: {o['stats']['constellations']} constellations, {o['stats']['branches']} branches")
    for c in o["constellations"]:
        print(f"    W_C={c['emergent_W_C']:16s} n={c['n']:2d}  render={c['render']:.3f}  spread={c['spread']:.3f}  [{c['honest']}]")
    print()
