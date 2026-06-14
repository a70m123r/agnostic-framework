#!/usr/bin/env python3
"""apply_growth.py - append-only application of the workflow growth plan to the Fable substrate.

Reads the workflow output JSON (result.growth), transforms each plan fact into the substrate
fact schema (SUBSTRATE_SPEC), and APPENDS to facts/ + verifications/. Never overwrites.
The two deployment verifications were mislabeled f-fbt-n0001 by the synthesis; they are the
fable-vs-mythos deployment split, so they are retargeted to the new fact f-fbt-n0038.

Idempotency: refuses to append a fact_id already present in the target file.
Stdlib only. Run once.
"""
import json
from pathlib import Path

OUT = Path(r"C:\Users\Admin\AppData\Local\Temp\claude\D--\36902d4e-bc4e-4608-859a-5a03ff9b3f45\tasks\wep2em5ut.output")
BASE = Path(r"D:\PlatformOperator\research\pav\candidates\canonical_genealogy\substrate")
ENT = BASE / "facts" / "fable_takedown.entities.jsonl"
EVT = BASE / "facts" / "fable_takedown.events.jsonl"
VER = BASE / "verifications" / "fable_takedown.jsonl"

RETRIEVED = "2026-06-13T14:00:00Z"
AGENT = "fable-growth-scout-01"
VERIFIER = "fable-growth-verifier-01"

g = json.loads(OUT.read_text(encoding="utf-8"))["result"]["growth"]

def efact(f):
    d = {"fact_id": f["fact_id"], "specimen": "fable-takedown", "subject_id": f["subject_id"],
         "predicate": f["predicate"], "value": f["value"]}
    if f.get("when"):
        d["when"] = f["when"]
    d["source"] = {"url": f["source_url"], "title": f["source_title"], "type": f["source_type"],
                   "published_or_updated": f.get("when", "2026-06-13")}
    d["retrieved_at"] = RETRIEVED
    d["certainty"] = f["certainty"]
    d["verification"] = "pending"
    d["agent"] = AGENT
    d["notes"] = "route=" + f["route"] + ". GROWTH (workflow scouts 2026-06-13). " + (f.get("note", "") or "")
    return d

# the new resolved deployment-split fact (hardcoded; resolves the n0027 open question)
N0038 = {
    "fact_id": "f-fbt-n0038", "specimen": "fable-takedown", "subject_id": "ent-mythos5",
    "predicate": "deployment_split",
    "value": "CONFIRMED (resolves open_question n0027): Fable 5 = the PUBLIC release (2026-06-09); Mythos 5 = restricted to Project Glasswing-approved orgs / a small group of cyberdefenders + infrastructure providers, no general access at launch. Materially different deployment histories.",
    "when": "2026-06-09",
    "source": {"url": "https://techcrunch.com/2026/06/09/anthropics-claude-fable-5-is-a-version-of-mythos-the-public-can-access-today/",
               "title": "Anthropic's Claude Fable 5 is a version of Mythos the public can access today - TechCrunch",
               "type": "news", "published_or_updated": "2026-06-09"},
    "retrieved_at": RETRIEVED, "certainty": 0.9, "verification": "pending", "agent": AGENT,
    "notes": "route=measured-on-plane. GROWTH (workflow scouts 2026-06-13). RESOLVES n0027: corroborated by 3 independent sources (Anthropic primary + TechCrunch + 9to5Google)."
}

def vrec(v):
    fid = v["fact_id"]
    # retarget the mislabeled deployment verifications to the real fact n0038
    if fid == "f-fbt-n0001":
        fid = "f-fbt-n0038"
    return {"fact_id": fid, "status": v["status"],
            "second_source": {"url": v["second_source_url"], "title": v["second_source_title"],
                              "type": "news", "published_or_updated": "2026-06-09"},
            "value_found": v["value_found"], "retrieved_at": RETRIEVED, "verifier": VERIFIER,
            "notes": "GROWTH cross-source corroboration. " + (v.get("note", "") or "")}

entity_dicts = [efact(f) for f in g["new_entity_facts"]] + [N0038] + [efact(f) for f in g["open_questions"]]
event_dicts = [efact(f) for f in g["new_event_facts"]]
verif_dicts = [vrec(v) for v in g["new_verifications"]]

def append(path, dicts):
    existing = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    existing.add(json.loads(line).get("fact_id"))
                except Exception:
                    pass
    # for facts, fact_id must be new; for verifications, dupes allowed (multiple verifs per fact)
    is_verif = (path == VER)
    added, skipped = 0, 0
    lines = []
    for d in dicts:
        if (not is_verif) and d["fact_id"] in existing:
            skipped += 1
            continue
        lines.append(json.dumps(d, ensure_ascii=False))
        added += 1
    if lines:
        with path.open("a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    return added, skipped

ea, es = append(ENT, entity_dicts)
va, vs = append(EVT, event_dicts)
ka, ks = append(VER, verif_dicts)
print(f"entities appended: {ea} (skipped existing: {es})")
print(f"events appended:   {va} (skipped existing: {vs})")
print(f"verifications appended: {ka}")
print("new entity fact_ids:", [d["fact_id"] for d in entity_dicts])
print("new event fact_ids: ", [d["fact_id"] for d in event_dicts])
print("verification targets:", [d["fact_id"] for d in verif_dicts])
