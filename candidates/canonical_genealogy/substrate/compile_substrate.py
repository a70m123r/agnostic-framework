#!/usr/bin/env python3
"""compile_substrate.py — compile the append-only fact log into best-value exports.

Tier-3 exploratory data-harvest infrastructure for the canonical wrapper-genealogy
specimens. Stdlib only (json, sqlite3, argparse, pathlib, datetime).

Reads:
    facts/*.jsonl          one fact record per line (see SUBSTRATE_SPEC.md §2)
    verifications/*.jsonl  one verification record per line (see SUBSTRATE_SPEC.md §4)

Validates each record against the schema and against base-specimen node ids
(loaded from ../specimens/*.json). An unknown subject_id without a "proposed:"
prefix is FLAGGED, not fatal.

Resolves each (specimen, subject_id, predicate) group to a BEST value by:
    1. verification bucket   corroborated > pending > disputed   (unverifiable ~ pending, flagged)
    2. certainty             higher wins
    3. freshness             newer retrieved_at wins
    4. stable tiebreak       lexicographically smallest fact_id
keeping the FULL history (and all disputed alternatives — never dropped).

Writes:
    substrate.db                         SQLite (tables: facts, verifications, best_values) — NEVER committed
    compiled/<specimen>.compiled.json    best values grouped by subject, with provenance refs (committed)
    compiled/_summary.json               coverage + freshness + certainty + disputes rollup (committed)
and prints a summary to stdout.

NO fabrication: this tool only ever reports what the logs contain. Honest discipline is the
harvesters' job; this tool's job is to never silently overwrite a disputed value.
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SPECIMENS_DIR = (HERE.parent / "specimens").resolve()
FACTS_DIR = HERE / "facts"
VERIF_DIR = HERE / "verifications"
COMPILED_DIR = HERE / "compiled"
DB_PATH = HERE / "substrate.db"

SOURCE_TYPES = {"aggregator", "primary", "encyclopedia", "news", "academic"}
VERIF_STATUSES = {"corroborated", "disputed", "unverifiable"}
# Bucket precedence for best-value selection (higher = preferred).
# unverifiable is given the same trust level as pending but is flagged in output.
BUCKET_RANK = {"corroborated": 3, "pending": 2, "unverifiable": 2, "disputed": 1}

REQUIRED_FACT_FIELDS = (
    "fact_id", "specimen", "subject_id", "predicate", "value",
    "source", "retrieved_at", "certainty", "verification", "agent",
)
REQUIRED_SOURCE_FIELDS = ("url", "title", "type", "published_or_updated")
REQUIRED_VERIF_FIELDS = (
    "fact_id", "status", "second_source", "value_found", "retrieved_at", "verifier",
)


# ---------------------------------------------------------------------------
# Specimen index (for subject_id validation)
# ---------------------------------------------------------------------------
def _walk_collect(node, ids, names):
    """Recursively collect every "id" slug and every node-name string from a specimen."""
    if isinstance(node, dict):
        for key, val in node.items():
            if key == "id" and isinstance(val, str):
                ids.add(val)
            elif key in ("name", "who") and isinstance(val, str):
                names.add(val)
            else:
                _walk_collect(val, ids, names)
    elif isinstance(node, list):
        for item in node:
            _walk_collect(item, ids, names)


def load_specimen_index():
    """Map specimen_id -> {"ids": set(slugs), "names": set(node-name strings), "file": path}."""
    index = {}
    if not SPECIMENS_DIR.is_dir():
        return index
    for path in sorted(SPECIMENS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  WARN: could not read specimen {path.name}: {exc}", file=sys.stderr)
            continue
        spec_id = data.get("specimen_id")
        if not spec_id:
            continue
        ids, names = set(), set()
        _walk_collect(data, ids, names)
        index[spec_id] = {"ids": ids, "names": names, "file": path.name}
    return index


# ---------------------------------------------------------------------------
# JSONL loading
# ---------------------------------------------------------------------------
def load_jsonl(directory):
    """Yield (path, lineno, obj) for every JSON line; collect parse errors."""
    records, errors = [], []
    if not directory.is_dir():
        return records, errors
    for path in sorted(directory.glob("*.jsonl")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue
            try:
                records.append((path.name, lineno, json.loads(line)))
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}:{lineno}: JSON parse error: {exc}")
    return records, errors


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def parse_ts(stamp):
    """Parse an ISO-8601 stamp to an aware datetime; return None if unparseable."""
    if not isinstance(stamp, str) or not stamp:
        return None
    s = stamp.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def validate_fact(obj, specimen_index):
    """Return (errors, flags). Errors are fatal-ish (skip the record); flags are non-fatal."""
    errors, flags = [], []
    fid = obj.get("fact_id", "<no fact_id>")

    for field in REQUIRED_FACT_FIELDS:
        if field not in obj:
            errors.append(f"fact {fid}: missing required field '{field}'")
    if errors:
        return errors, flags

    src = obj.get("source")
    if not isinstance(src, dict):
        errors.append(f"fact {fid}: 'source' must be an object")
    else:
        for field in REQUIRED_SOURCE_FIELDS:
            if field not in src:
                errors.append(f"fact {fid}: source missing '{field}'")
        stype = src.get("type")
        if stype not in SOURCE_TYPES:
            errors.append(f"fact {fid}: source.type '{stype}' not in {sorted(SOURCE_TYPES)}")
        url = src.get("url", "")
        if not (isinstance(url, str) and url.startswith(("http://", "https://"))):
            flags.append(f"fact {fid}: source.url is not an http(s) URL ('{url}') — provenance suspect")

    cert = obj.get("certainty")
    if not isinstance(cert, (int, float)) or not (0.0 <= float(cert) <= 1.0):
        errors.append(f"fact {fid}: certainty '{cert}' must be a number in [0,1]")

    if obj.get("verification") != "pending":
        flags.append(f"fact {fid}: verification should be 'pending' at emit time "
                     f"(got '{obj.get('verification')}'); use a verification record to change status")

    if parse_ts(obj.get("retrieved_at")) is None:
        flags.append(f"fact {fid}: retrieved_at '{obj.get('retrieved_at')}' is not a parseable ISO-8601 stamp")

    # certainty-rubric guard: theory-DNA shares must be capped low.
    if obj.get("predicate") == "contribution_share" and isinstance(cert, (int, float)) and float(cert) > 0.6:
        flags.append(f"fact {fid}: contribution_share certainty {cert} > 0.6 — theory-DNA is an estimate, cap at 0.6")

    # subject_id validation against base specimen (non-fatal flags).
    spec_id = obj.get("specimen")
    subject = obj.get("subject_id", "")
    if spec_id not in specimen_index:
        flags.append(f"fact {fid}: specimen '{spec_id}' not found among ../specimens/*.json")
    elif isinstance(subject, str) and subject.startswith("proposed:"):
        if len(subject) <= len("proposed:"):
            flags.append(f"fact {fid}: 'proposed:' subject_id has empty slug")
    else:
        known = specimen_index[spec_id]
        if subject not in known["ids"] and subject not in known["names"]:
            flags.append(f"fact {fid}: subject_id '{subject}' not a known node id/name in "
                         f"specimen '{spec_id}' (and lacks 'proposed:' prefix) — FLAGGED")
    return errors, flags


def validate_verification(obj):
    errors, flags = [], []
    fid = obj.get("fact_id", "<no fact_id>")
    for field in REQUIRED_VERIF_FIELDS:
        if field not in obj:
            errors.append(f"verification for {fid}: missing required field '{field}'")
    if errors:
        return errors, flags
    if obj.get("status") not in VERIF_STATUSES:
        errors.append(f"verification for {fid}: status '{obj.get('status')}' not in {sorted(VERIF_STATUSES)}")
    ss = obj.get("second_source")
    if not isinstance(ss, dict):
        errors.append(f"verification for {fid}: 'second_source' must be an object")
    elif ss.get("type") not in SOURCE_TYPES:
        flags.append(f"verification for {fid}: second_source.type '{ss.get('type')}' not in {sorted(SOURCE_TYPES)}")
    if parse_ts(obj.get("retrieved_at")) is None:
        flags.append(f"verification for {fid}: retrieved_at not a parseable ISO-8601 stamp")
    return errors, flags


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------
def bucket_for(fact_id, verifs_by_fact):
    """Assign a verification bucket from all verification records targeting a fact."""
    recs = verifs_by_fact.get(fact_id, [])
    if not recs:
        return "pending"
    statuses = {r["status"] for r in recs}
    if "corroborated" in statuses:
        return "corroborated"
    if "disputed" in statuses:
        return "disputed"
    if "unverifiable" in statuses:
        return "unverifiable"
    return "pending"


def sort_key(fact, bucket):
    """Lexicographic best-value key (higher tuple wins under max())."""
    ts = parse_ts(fact.get("retrieved_at"))
    epoch = ts.timestamp() if ts else float("-inf")
    # Negate fact_id by ranking: smaller fact_id should win on tie -> use reverse via a wrapper.
    return (
        BUCKET_RANK.get(bucket, 0),
        float(fact.get("certainty", 0.0)),
        epoch,
        _InvStr(str(fact.get("fact_id", ""))),  # smaller fact_id wins
    )


class _InvStr:
    """Wrap a string so that SMALLER strings compare as GREATER (so max() picks the smallest)."""
    __slots__ = ("s",)

    def __init__(self, s):
        self.s = s

    def __lt__(self, other):
        return self.s > other.s

    def __eq__(self, other):
        return self.s == other.s


def resolve_best(facts, verifs_by_fact):
    """Group facts by (specimen, subject_id, predicate); pick best; collect disputes."""
    groups = {}
    for f in facts:
        key = (f["specimen"], f["subject_id"], f["predicate"])
        groups.setdefault(key, []).append(f)

    best_rows = []
    for key, members in sorted(groups.items()):
        specimen, subject, predicate = key
        ranked = []
        for f in members:
            b = bucket_for(f["fact_id"], verifs_by_fact)
            ranked.append((sort_key(f, b), b, f))
        ranked.sort(key=lambda t: t[0])
        _, best_bucket, best_fact = ranked[-1]

        # Collect disputed alternatives (contradicting values found by verifiers).
        disputed_alternatives = []
        for f in members:
            for v in verifs_by_fact.get(f["fact_id"], []):
                if v["status"] == "disputed":
                    disputed_alternatives.append({
                        "value_found": v.get("value_found"),
                        "fact_id": f["fact_id"],
                        "fact_value": f.get("value"),
                        "second_source": v.get("second_source"),
                        "verifier": v.get("verifier"),
                        "retrieved_at": v.get("retrieved_at"),
                    })

        best_rows.append({
            "specimen": specimen,
            "subject_id": subject,
            "predicate": predicate,
            "value": best_fact.get("value"),
            "when": best_fact.get("when"),
            "best_fact_id": best_fact["fact_id"],
            "bucket": best_bucket,
            "certainty": best_fact.get("certainty"),
            "retrieved_at": best_fact.get("retrieved_at"),
            "source": best_fact.get("source"),
            "agent": best_fact.get("agent"),
            "notes": best_fact.get("notes"),
            "provenance_refs": sorted(f["fact_id"] for f in members),
            "n_facts": len(members),
            "disputed_alternatives": disputed_alternatives,
        })
    return best_rows


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
def build_db(facts, verifs, best_rows):
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE facts (
            fact_id TEXT, specimen TEXT, subject_id TEXT, predicate TEXT,
            value TEXT, when_ TEXT, source_url TEXT, source_title TEXT,
            source_type TEXT, source_pub TEXT, retrieved_at TEXT,
            certainty REAL, verification TEXT, agent TEXT, notes TEXT, raw TEXT
        );
        CREATE TABLE verifications (
            fact_id TEXT, status TEXT, value_found TEXT,
            second_source_url TEXT, second_source_type TEXT,
            retrieved_at TEXT, verifier TEXT, notes TEXT, raw TEXT
        );
        CREATE TABLE best_values (
            specimen TEXT, subject_id TEXT, predicate TEXT, value TEXT, when_ TEXT,
            best_fact_id TEXT, bucket TEXT, certainty REAL, retrieved_at TEXT,
            source_url TEXT, provenance_refs TEXT, n_facts INTEGER,
            n_disputed INTEGER, disputed_alternatives TEXT
        );
        CREATE INDEX idx_facts_group ON facts(specimen, subject_id, predicate);
        CREATE INDEX idx_verif_fact ON verifications(fact_id);
        CREATE INDEX idx_best_group ON best_values(specimen, subject_id, predicate);
    """)
    for f in facts:
        src = f.get("source") or {}
        cur.execute("INSERT INTO facts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            f.get("fact_id"), f.get("specimen"), f.get("subject_id"), f.get("predicate"),
            json.dumps(f.get("value"), ensure_ascii=False), f.get("when"),
            src.get("url"), src.get("title"), src.get("type"), src.get("published_or_updated"),
            f.get("retrieved_at"), f.get("certainty"), f.get("verification"),
            f.get("agent"), f.get("notes"), json.dumps(f, ensure_ascii=False),
        ))
    for v in verifs:
        ss = v.get("second_source") or {}
        cur.execute("INSERT INTO verifications VALUES (?,?,?,?,?,?,?,?,?)", (
            v.get("fact_id"), v.get("status"),
            json.dumps(v.get("value_found"), ensure_ascii=False),
            ss.get("url"), ss.get("type"), v.get("retrieved_at"),
            v.get("verifier"), v.get("notes"), json.dumps(v, ensure_ascii=False),
        ))
    for b in best_rows:
        src = b.get("source") or {}
        cur.execute("INSERT INTO best_values VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            b["specimen"], b["subject_id"], b["predicate"],
            json.dumps(b.get("value"), ensure_ascii=False), b.get("when"),
            b["best_fact_id"], b["bucket"], b.get("certainty"), b.get("retrieved_at"),
            src.get("url"), json.dumps(b["provenance_refs"], ensure_ascii=False),
            b["n_facts"], len(b["disputed_alternatives"]),
            json.dumps(b["disputed_alternatives"], ensure_ascii=False),
        ))
    conn.commit()
    conn.close()


def write_compiled_exports(best_rows, generated):
    COMPILED_DIR.mkdir(exist_ok=True)
    by_spec = {}
    for b in best_rows:
        by_spec.setdefault(b["specimen"], []).append(b)
    written = []
    for spec_id, rows in sorted(by_spec.items()):
        by_subject = {}
        for r in rows:
            entry = {
                "predicate": r["predicate"],
                "value": r["value"],
                "when": r["when"],
                "bucket": r["bucket"],
                "certainty": r["certainty"],
                "best_fact_id": r["best_fact_id"],
                "source": r["source"],
                "provenance_refs": r["provenance_refs"],
            }
            if r["disputed_alternatives"]:
                entry["disputed_alternatives"] = r["disputed_alternatives"]
            by_subject.setdefault(r["subject_id"], []).append(entry)
        out = {
            "_doc": "Compiled best-value export — viewer ingestion artifact. Generated by compile_substrate.py. "
                    "Do not edit by hand; edit facts/*.jsonl and recompile.",
            "specimen": spec_id,
            "generated": generated,
            "subjects": dict(sorted(by_subject.items())),
        }
        path = COMPILED_DIR / f"{spec_id}.compiled.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path.name)
    return written


def write_summary(best_rows, facts, verifs, errors, flags, generated):
    COMPILED_DIR.mkdir(exist_ok=True)
    per_spec = {}
    for b in best_rows:
        s = per_spec.setdefault(b["specimen"], {
            "best_values": 0, "subjects": set(), "predicates": set(),
            "buckets": {"corroborated": 0, "pending": 0, "disputed": 0, "unverifiable": 0},
            "certainties": [], "disputes": 0,
        })
        s["best_values"] += 1
        s["subjects"].add(b["subject_id"])
        s["predicates"].add(b["predicate"])
        s["buckets"][b["bucket"]] = s["buckets"].get(b["bucket"], 0) + 1
        if isinstance(b["certainty"], (int, float)):
            s["certainties"].append(float(b["certainty"]))
        s["disputes"] += len(b["disputed_alternatives"])

    fresh = {}
    for f in facts:
        ts = parse_ts(f.get("retrieved_at"))
        if ts is None:
            continue
        rec = fresh.setdefault(f["specimen"], {"oldest": ts, "newest": ts})
        rec["oldest"] = min(rec["oldest"], ts)
        rec["newest"] = max(rec["newest"], ts)

    specimens = {}
    for spec_id, s in sorted(per_spec.items()):
        certs = s["certainties"]
        fr = fresh.get(spec_id)
        specimens[spec_id] = {
            "best_values": s["best_values"],
            "distinct_subjects": len(s["subjects"]),
            "distinct_predicates": len(s["predicates"]),
            "buckets": s["buckets"],
            "certainty_min": round(min(certs), 3) if certs else None,
            "certainty_mean": round(sum(certs) / len(certs), 3) if certs else None,
            "certainty_max": round(max(certs), 3) if certs else None,
            "freshness_oldest": fr["oldest"].isoformat().replace("+00:00", "Z") if fr else None,
            "freshness_newest": fr["newest"].isoformat().replace("+00:00", "Z") if fr else None,
            "disputes": s["disputes"],
        }

    disputed_list = [
        {
            "specimen": b["specimen"], "subject_id": b["subject_id"], "predicate": b["predicate"],
            "best_value": b["value"], "best_fact_id": b["best_fact_id"], "bucket": b["bucket"],
            "disputed_alternatives": b["disputed_alternatives"],
        }
        for b in best_rows if b["disputed_alternatives"]
    ]

    summary = {
        "_doc": "Compiled substrate summary — coverage, freshness, certainty, disputes. "
                "Generated by compile_substrate.py.",
        "generated": generated,
        "totals": {
            "facts": len(facts),
            "verifications": len(verifs),
            "best_values": len(best_rows),
            "specimens_with_facts": len(per_spec),
            "validation_errors": len(errors),
            "validation_flags": len(flags),
            "disputed_best_values": len(disputed_list),
        },
        "per_specimen": specimens,
        "disputes": disputed_list,
        "validation_errors": errors,
        "validation_flags": flags,
    }
    path = COMPILED_DIR / "_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Compile the canonical-genealogy fact substrate.")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any validation flag (not just error) is raised")
    ap.add_argument("--no-db", action="store_true", help="skip writing substrate.db")
    args = ap.parse_args()

    generated = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    specimen_index = load_specimen_index()

    raw_facts, fact_parse_err = load_jsonl(FACTS_DIR)
    raw_verifs, verif_parse_err = load_jsonl(VERIF_DIR)

    errors = list(fact_parse_err) + list(verif_parse_err)
    flags = []

    facts = []
    fact_id_occurrences = {}  # fact_id -> list of (fname, group_tuple)
    for fname, lineno, obj in raw_facts:
        errs, flgs = validate_fact(obj, specimen_index)
        if errs:
            errors.extend(f"{fname}:{lineno}: {e}" for e in errs)
            continue
        flags.extend(f"{fname}:{lineno}: {fl}" for fl in flgs)
        group = (obj["specimen"], obj["subject_id"], obj["predicate"])
        fact_id_occurrences.setdefault(obj["fact_id"], []).append((fname, group))
        facts.append(obj)

    # Duplicate-fact_id hazard detection (Opus-audit hardening).
    # Verifications and disputed_alternatives are keyed on the BARE fact_id
    # (bucket_for / resolve_best). If one fact_id is reused across facts that
    # belong to DIFFERENT (specimen, subject_id, predicate) groups, a single
    # verification record would LEAK onto every group sharing the id — a silent
    # false-corroboration / false-dispute. That is now a fatal ERROR (exit 2):
    # the only safe fix is a disjoint id namespace (renumber one file to e####).
    # A duplicate id WITHIN one group is benign (multiple attestations) and stays
    # a non-fatal flag.
    for fid, occ in sorted(fact_id_occurrences.items()):
        if len(occ) <= 1:
            continue
        files = sorted({f for f, _ in occ})
        groups = {g for _, g in occ}
        if len(groups) > 1:
            errors.append(
                f"HAZARD: fact_id '{fid}' reused across {len(occ)} facts in {files} spanning "
                f"{len(groups)} DIFFERENT (specimen,subject_id,predicate) groups — verifications "
                f"keyed on the bare fact_id would leak across groups. Renumber one file's ids to a "
                f"disjoint namespace (e####)."
            )
        else:
            flags.append(
                f"duplicate fact_id '{fid}' across {files} within the SAME resolution group "
                f"(benign: multiple attestations; keeping all rows)"
            )

    verifs, verifs_by_fact = [], {}
    valid_fact_ids = {f["fact_id"] for f in facts}
    for fname, lineno, obj in raw_verifs:
        errs, flgs = validate_verification(obj)
        if errs:
            errors.extend(f"{fname}:{lineno}: {e}" for e in errs)
            continue
        flags.extend(f"{fname}:{lineno}: {fl}" for fl in flgs)
        if obj["fact_id"] not in valid_fact_ids:
            flags.append(f"{fname}:{lineno}: verification targets unknown fact_id '{obj['fact_id']}'")
        verifs.append(obj)
        verifs_by_fact.setdefault(obj["fact_id"], []).append(obj)

    best_rows = resolve_best(facts, verifs_by_fact)

    if not args.no_db:
        build_db(facts, verifs, best_rows)
    written = write_compiled_exports(best_rows, generated)
    summary = write_summary(best_rows, facts, verifs, errors, flags, generated)

    # ---- stdout report ----
    print("=" * 68)
    print("CANONICAL-GENEALOGY SUBSTRATE — compile report")
    print("=" * 68)
    print(f"generated:            {generated}")
    print(f"specimens indexed:    {len(specimen_index)} (from {SPECIMENS_DIR})")
    print(f"facts loaded:         {len(facts)}")
    print(f"verifications loaded: {len(verifs)}")
    print(f"best values:          {len(best_rows)}")
    print(f"validation errors:    {len(errors)}")
    print(f"validation flags:     {len(flags)}")
    print(f"disputed best values: {summary['totals']['disputed_best_values']}")
    if not args.no_db:
        print(f"db written:           {DB_PATH.name}")
    print(f"exports written:      {', '.join(written) if written else '(none)'}")
    print("-" * 68)
    print("PER-SPECIMEN coverage / freshness / certainty / disputes")
    for spec_id, s in summary["per_specimen"].items():
        print(f"  {spec_id}")
        print(f"    best={s['best_values']}  subjects={s['distinct_subjects']}  "
              f"predicates={s['distinct_predicates']}  disputes={s['disputes']}")
        print(f"    buckets={s['buckets']}")
        print(f"    certainty[min/mean/max]={s['certainty_min']}/{s['certainty_mean']}/{s['certainty_max']}")
        print(f"    freshness[oldest..newest]={s['freshness_oldest']} .. {s['freshness_newest']}")
    if errors:
        print("-" * 68)
        print("VALIDATION ERRORS (records skipped):")
        for e in errors:
            print(f"  ERROR  {e}")
    if flags:
        print("-" * 68)
        print("VALIDATION FLAGS (non-fatal):")
        for fl in flags:
            print(f"  FLAG   {fl}")
    if summary["disputes"]:
        print("-" * 68)
        print("DISPUTES (both values retained):")
        for d in summary["disputes"]:
            print(f"  {d['specimen']} / {d['subject_id']} / {d['predicate']}: "
                  f"best='{d['best_value']}' (bucket={d['bucket']})")
            for alt in d["disputed_alternatives"]:
                print(f"      vs disputed value_found='{alt['value_found']}' "
                      f"(by {alt['verifier']})")
    print("=" * 68)

    if errors:
        return 2
    if args.strict and flags:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
