# -*- coding: utf-8 -*-
"""
P-L4 HARNESS-SIGNATURE probe -- data fetch (latent_ponds).

Fetches REAL Wikimedia pageview aggregates (no fabrication; every byte cached to disk
with endpoint + params in the filename). Read-only probe of a live system.

Endpoints (verified live, per program brief):
  https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/{project}/{access}/user/hourly/{YYYYMMDDHH}/{YYYYMMDDHH}
  https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{project}/all-access/{yyyy}/{mm}/{dd}

User-Agent: agnostic-framework-research/0.1 (research instrument)   [program law]
Etiquette: ~1 req/s, retry with backoff, cache-first (re-runs hit disk only).

What is fetched and why:
  MAIN window 2026030100..2026060100 (92 days), 5 ponds (en/ja/de/ar/es wikipedia):
    - all-access  : primary series for spectral lines, phase, canon-radius, Q6 rungs
    - desktop     : P-L4 design change (Piccardi&West 2025) -- work-harness channel
    - mobile-web  : P-L4 design change -- body-clock-harness channel
  TREND windows (same calendar span Mar01..Jun01) 2019/2021/2023/2025, en+ja all-access:
    - P-L4 design change (Crokidakis 2026 alternative): multi-year circadian-amplitude
      trend -- monotone shrink would favor gradual-degradation over stable harness line.
agent=user throughout (filters spider/automated -- McGrady-2025 bot confound mitigation
at the endpoint level; residual unflagged bots disclosed as caveat).
"""
import json, pathlib, time, sys
import requests

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "agnostic-framework-research/0.1 (research instrument)"}
BASE = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/"
        "{proj}/{access}/user/hourly/{s}/{e}")

PROJECTS = ["en.wikipedia.org", "ja.wikipedia.org", "de.wikipedia.org",
            "ar.wikipedia.org", "es.wikipedia.org"]
MAIN = ("2026030100", "2026060100")
ACCESS_MAIN = ["all-access", "desktop", "mobile-web"]
TREND_YEARS = ["2019", "2021", "2023", "2025"]
TREND_PROJECTS = ["en.wikipedia.org", "ja.wikipedia.org"]


def fetch(url, cache_name):
    f = DATA / cache_name
    if f.exists():
        print("cache  ", cache_name)
        return json.loads(f.read_text(encoding="utf-8"))
    last = None
    for attempt in range(8):
        try:
            r = requests.get(url, headers=UA, timeout=90)
        except Exception as ex:
            last = str(ex); time.sleep(10 * (attempt + 1)); continue
        if r.status_code == 200:
            j = r.json()
            f.write_text(json.dumps(j), encoding="utf-8")
            n = len(j.get("items", []))
            print("fetched", cache_name, n, "items", flush=True)
            time.sleep(12.0)         # etiquette: this endpoint throttles hard
            return j
        last = f"HTTP {r.status_code}: {r.text[:120]}"
        print("retry  ", cache_name, last, flush=True)
        time.sleep(25 * (attempt + 1))
    raise RuntimeError(f"FAILED {url} :: {last}")


def fetch_hourly(proj, access, s, e):
    url = BASE.format(proj=proj, access=access, s=s, e=e)
    return fetch(url, f"hourly_{proj}_{access}_{s}_{e}.json")


def main():
    total = 0
    for proj in PROJECTS:
        for access in ACCESS_MAIN:
            j = fetch_hourly(proj, access, *MAIN)
            total += len(j.get("items", []))
    for proj in TREND_PROJECTS:
        for y in TREND_YEARS:
            j = fetch_hourly(proj, "all-access", f"{y}030100", f"{y}060100")
            total += len(j.get("items", []))
    print("TOTAL hourly items fetched/cached:", total)


if __name__ == "__main__":
    main()
