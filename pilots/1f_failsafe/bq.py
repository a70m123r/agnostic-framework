"""
BigQuery path for Pilot #150 GDELT ingest (alternative to gdelt_ingest.py).

Computes the SAME locked daily aggregates (event_count / mean_tone /
category_entropy per country per SQLDATE) server-side via one GROUP BY query
against the public `gdelt-bq.gdeltv2.events` table, then writes data/raw/ CSVs
in the identical format pilot.py --mode gdelt consumes.

Auth: browser OAuth via pydata-google-auth (BigQuery sandbox; no billing card,
no gcloud install). Credentials are cached after first login.

Subcommands:
  python bq.py auth                 # one-time browser login (caches creds)
  python bq.py list                 # list GCP projects the user can bill to
  python bq.py dryrun --project ID  # estimate bytes scanned (free, no run)
  python bq.py query  --project ID  # run query + write data/raw/ CSVs
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import pydata_google_auth

import gdelt_ingest as gi  # reuse FIPS_TO_LABEL, window constants, entropy

SCOPES = ["https://www.googleapis.com/auth/bigquery"]
HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "data" / "raw"

# FIPS codes in the locked pairing
FIPS = list(gi.FIPS_TO_LABEL.keys())

QUERY = f"""
WITH base AS (
  SELECT SQLDATE AS d,
         ActionGeo_CountryCode AS cc,
         EventRootCode AS root,
         AvgTone AS tone
  FROM `gdelt-bq.gdeltv2.events`
  WHERE SQLDATE BETWEEN {gi.SQLDATE_LO} AND 20251231
    AND ActionGeo_CountryCode IN ({",".join(f"'{c}'" for c in FIPS)})
),
day_agg AS (
  SELECT d, cc, COUNT(*) AS event_count, AVG(tone) AS mean_tone
  FROM base GROUP BY d, cc
),
per_root AS (
  SELECT d, cc, root, COUNT(*) AS n
  FROM base
  WHERE root IS NOT NULL AND root != ''
  GROUP BY d, cc, root
),
roots_tot AS (
  SELECT d, cc, SUM(n) AS tot FROM per_root GROUP BY d, cc
),
ent AS (
  SELECT pr.d, pr.cc,
         -SUM( (pr.n / rt.tot) * (LN(pr.n / rt.tot) / LN(2.0)) ) AS category_entropy
  FROM per_root pr
  JOIN roots_tot rt ON pr.d = rt.d AND pr.cc = rt.cc
  GROUP BY pr.d, pr.cc
)
SELECT da.d AS sqldate, da.cc AS cc,
       da.event_count AS event_count,
       da.mean_tone AS mean_tone,
       e.category_entropy AS category_entropy
FROM day_agg da
LEFT JOIN ent e ON da.d = e.d AND da.cc = e.cc
ORDER BY da.cc, da.d
"""


def get_creds():
    return pydata_google_auth.get_user_credentials(SCOPES)


def make_client(project=None):
    from google.cloud import bigquery
    creds = get_creds()
    return bigquery.Client(project=project or "bigquery-public-data", credentials=creds)


def cmd_auth():
    print("Starting OAuth — a browser window should open. Log in with your Google "
          "account and approve BigQuery access.", flush=True)
    creds = get_creds()
    print("AUTH_OK — credentials cached. refresh_token:",
          bool(getattr(creds, "refresh_token", None)), flush=True)


def cmd_list():
    client = make_client()
    print("GCP projects you can use as the billing/quota project:")
    n = 0
    for pr in client.list_projects():
        print(f"  {pr.project_id}    ({pr.friendly_name})")
        n += 1
    if n == 0:
        print("  (none found — create one at https://console.cloud.google.com → New Project)")


def cmd_dryrun(project):
    from google.cloud import bigquery
    client = make_client(project)
    job = client.query(QUERY, job_config=bigquery.QueryJobConfig(dry_run=True,
                                                                 use_query_cache=False))
    gb = job.total_bytes_processed / 1e9
    print(f"DRY RUN ok. Bytes to scan: {job.total_bytes_processed:,} ({gb:.2f} GB)")
    print(f"Free tier is 1000 GB/month -> this query is "
          f"{'WITHIN free tier ($0)' if gb < 1000 else 'OVER free tier'}.")


def cmd_query(project):
    client = make_client(project)
    print(f"Running query (billing project: {project}) ...", flush=True)
    job = client.query(QUERY)
    rows = list(job.result())
    gb = (job.total_bytes_processed or 0) / 1e9
    print(f"Query done: {len(rows):,} (country,day) rows, scanned {gb:.2f} GB", flush=True)

    ec, mt, ce = {}, {}, {}
    for r in rows:
        label = gi.FIPS_TO_LABEL[r["cc"]]
        ds = str(r["sqldate"])
        ec[(label, ds)] = int(r["event_count"])
        mt[(label, ds)] = float(r["mean_tone"]) if r["mean_tone"] is not None else None
        ce[(label, ds)] = float(r["category_entropy"]) if r["category_entropy"] is not None else None

    # full daily index across the locked window
    lo = date(int(gi.SQLDATE_LO[:4]), int(gi.SQLDATE_LO[4:6]), int(gi.SQLDATE_LO[6:8]))
    hi = date(int(gi.SQLDATE_HI[:4]), int(gi.SQLDATE_HI[4:6]), int(gi.SQLDATE_HI[6:8]))
    all_dates = []
    d = lo
    while d < hi:
        all_dates.append(d.strftime("%Y%m%d"))
        d += timedelta(days=1)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    labels = sorted(set(gi.FIPS_TO_LABEL.values()))
    for label in labels:
        for signal, src, miss in (("event_count", ec, 0),
                                  ("mean_tone", mt, ""),
                                  ("category_entropy", ce, "")):
            rows_out = []
            for ds in all_dates:
                v = src.get((label, ds), miss)
                if v is None:
                    v = ""
                iso = f"{ds[:4]}-{ds[4:6]}-{ds[6:8]}"
                rows_out.append(f"{iso},{v}")
            (RAW_DIR / f"{label}_{signal}.csv").write_text(
                "date,value\n" + "\n".join(rows_out) + "\n", encoding="utf-8")
    print(f"Wrote {len(labels)*3} CSVs to {RAW_DIR} ({len(all_dates)} rows each)", flush=True)

    print("Coverage (days with events / total) + total events:")
    for label in labels:
        ne = sum(1 for ds in all_dates if ec.get((label, ds), 0) > 0)
        tot = sum(ec.get((label, ds), 0) for ds in all_dates)
        print(f"  {label}: {ne}/{len(all_dates)} days, {tot:,} events")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["auth", "list", "dryrun", "query"])
    ap.add_argument("--project", default=None)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if args.cmd == "auth":
        cmd_auth()
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "dryrun":
        if not args.project:
            sys.exit("dryrun needs --project ID (run `python bq.py list` first)")
        cmd_dryrun(args.project)
    elif args.cmd == "query":
        if not args.project:
            sys.exit("query needs --project ID")
        cmd_query(args.project)


if __name__ == "__main__":
    main()
