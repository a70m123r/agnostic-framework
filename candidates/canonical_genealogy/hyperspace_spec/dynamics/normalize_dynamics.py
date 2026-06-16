#!/usr/bin/env python3
"""
Normalize the latent-dynamics FINDINGS (bestiary creatures + adversarial tactics + couplings)
into the canonical_genealogy SUBSTRATE methodology: append-only records with provenance +
certainty + a lifecycle-as-verification state, then a deterministic best-value compile.

Each dynamic becomes a WRAPPER record (its kernel = formal_name + observable; its membrane =
framework_tie + citation; its certainty = confidence; its verification = lifecycle stage).
The COIN holds: render <= confidence, capped by lifecycle support.

Inputs (workflow result files, wrapped JSON):
  bestiary:  w96q9smxd.output          (6+1 families, 41 creatures)
  tactics:   <argv[1]>  (optional)     (the adversarial-tactics-catalogue result)
Outputs (here, in dynamics/):
  dynamics.jsonl                 - append-only normalized records (source of truth)
  compiled/dynamics.compiled.json - best-value compile (by family, lifecycle buckets, stats)
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
TASKS = Path(r"C:\Users\Admin\AppData\Local\Temp\claude\D--\36902d4e-bc4e-4608-859a-5a03ff9b3f45\tasks")
BEST = TASKS / "w96q9smxd.output"
t_obs = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def result_obj(path):
    top = json.loads(Path(path).read_text(encoding="utf-8"))
    for v in [top] + (list(top.values()) if isinstance(top, dict) else []):
        if isinstance(v, dict) and any(k in v for k in ("families","tactic_taxonomy","reduction")):
            return v
    return None

# physical <-> latent by the field the dynamic is grounded in
FIELD_PL = [
    (r"thermo|physics|landauer|energy|statistical mech", 0.15),
    (r"ecolog|evolution|biolog|predator|parasite", 0.35),
    (r"machine learning|ml\b|algorithm|control|streaming|mlops|adversarial-ml|adversarial ml", 0.55),
    (r"game.?theory|econom|mechanism|incentive|signal", 0.66),
    (r"argument|rhetoric|negotiat|debate|dialectic", 0.76),
    (r"cognit|cog-?sci|neuro|psycholog|metacognit|behav", 0.88),
]
def phys_latent(field):
    f = (field or "").lower()
    for pat, v in FIELD_PL:
        if re.search(pat, f): return v
    return 0.6

LIFE_CAP = {"documented": 1.0, "classified": 0.85, "tracked": 0.6, "sighted": 0.4}

def slug(s):
    return re.sub(r"[^a-z0-9]+","-", (s or "").lower()).strip("-")[:50]

records = []
def add(kind, family, d):
    name = d.get("name","")
    conf = float(d.get("confidence", 0.6))
    life = d.get("lifecycle_stage") or d.get("lifecycle") or ("documented" if kind=="creature" else "tracked")
    rec = {
        "id": f"dyn-{slug(family)}-{slug(name)}",
        "type": kind, "family": family, "name": name,
        "what": d.get("what",""),
        "framework_tie": d.get("framework_tie",""),
        "formal_name": d.get("formal_name",""),
        "field": d.get("field",""),
        "citation": d.get("citation",""),
        "observable": d.get("observable",""),
        "ask_give_role": d.get("ask_give_role",""),
        "evolves_borrows": d.get("evolves_borrows",""),
        "creatures_underlain": d.get("creatures_underlain", []),
        "phys_latent": phys_latent(d.get("field","")),
        "lifecycle": life,
        "certainty": conf,
        "source": {"doc": "LATENT_DYNAMICS_BESTIARY.md" if kind=="creature" else "ADVERSARIAL_TACTICS.md"},
        "retrieved_at": t_obs,
    }
    records.append(rec)

# --- creatures from the bestiary ---
best = result_obj(BEST)
if best:
    for fam in best.get("families", []):
        fid = fam.get("family", fam.get("title",""))
        for c in fam.get("creatures", []):
            add("creature", fid, c)

# --- tactics + couplings from WF1 (optional) ---
reduction = None
tac_path = sys.argv[1] if len(sys.argv) > 1 else None
if tac_path and Path(tac_path).exists():
    tac = result_obj(tac_path)
    if tac:
        for t in tac.get("tactic_taxonomy", []):
            add("tactic", "tactic:"+(t.get("side","")), t)
        for c in tac.get("couplings", []):
            add("coupling", "coupling", {**c, "lifecycle_stage": "tracked", "confidence": c.get("confidence", 0.6),
                                         "what": c.get("loop",""), "observable": c.get("observable",""),
                                         "formal_name": c.get("formal_name",""), "citation": c.get("citation","")})
        reduction = tac.get("reduction")

# --- write append-only jsonl ---
(HERE).mkdir(parents=True, exist_ok=True)
(HERE/"dynamics.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records)+"\n", encoding="utf-8")

# --- compile: best-value (here: dedup by id, COIN render = min(certainty, lifecycle cap)) ---
byid = {}
for r in records:
    r2 = dict(r); r2["render"] = round(min(r["certainty"], LIFE_CAP.get(r["lifecycle"], 0.5)), 3)
    byid[r["id"]] = r2   # last wins (append-only newest)
out = sorted(byid.values(), key=lambda r:(r["family"], -r["render"]))

fams, types, lifes = {}, {}, {}
for r in out:
    fams[r["family"]] = fams.get(r["family"],0)+1
    types[r["type"]] = types.get(r["type"],0)+1
    lifes[r["lifecycle"]] = lifes.get(r["lifecycle"],0)+1

compiled = {
    "_meta": {"what":"latent-dynamics substrate (creatures + tactics + couplings) normalized via SUBSTRATE methodology",
              "discipline":"append-only + provenance + certainty + lifecycle-as-verification + COIN render<=support",
              "t_obs": t_obs},
    "stats": {"records": len(out), "by_type": types, "by_family": fams, "by_lifecycle": lifes,
              "reduction": reduction},
    "records": out,
}
(HERE/"compiled").mkdir(exist_ok=True)
(HERE/"compiled"/"dynamics.compiled.json").write_text(json.dumps(compiled, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"normalized {len(out)} dynamics records")
print(f"  by_type: {types}")
print(f"  by_family: {fams}")
print(f"  by_lifecycle: {lifes}")
print(f"  reduction: {'(tactics pending)' if reduction is None else reduction.get('ratio')}")
print(f"  wrote dynamics.jsonl + compiled/dynamics.compiled.json")
