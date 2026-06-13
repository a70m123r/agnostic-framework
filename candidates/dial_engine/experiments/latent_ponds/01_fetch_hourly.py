"""
P-L4 harness-signature probe — Step 1: fetch hourly per-project pageviews
Languages: en, ja, de, ar, es
Window: 2026-03-01 to 2026-06-01 (hourly)
Cache to disk; respects API etiquette (1 req/sec, no retries on 200).
UA: agnostic-framework-research/0.1 (research instrument)
"""

import json
import time
import urllib.request
import urllib.error
import os
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

UA = "agnostic-framework-research/0.1 (research instrument)"

LANGUAGES = ["en", "ja", "de", "ar", "es"]

# Hourly endpoint: aggregate per project
# https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/{project}/all-access/user/hourly/{start}/{end}
# Date format: YYYYMMDDHH
START = "2026030100"
END   = "2026060123"


def fetch_hourly(lang: str) -> list:
    project = f"{lang}.wikipedia"
    cache_path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    if cache_path.exists():
        print(f"[cache hit] {lang}")
        with open(cache_path) as f:
            return json.load(f)

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate"
        f"/{project}/all-access/user/hourly/{START}/{END}"
    )
    print(f"[fetch] {lang} -> {url}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  HTTP error {e.code}: {e.reason}")
        raise

    items = data.get("items", [])
    with open(cache_path, "w") as f:
        json.dump(items, f)
    print(f"  -> {len(items)} hourly points")
    time.sleep(1.1)   # polite rate
    return items


if __name__ == "__main__":
    results = {}
    for lang in LANGUAGES:
        items = fetch_hourly(lang)
        results[lang] = items
        print(f"  {lang}: {len(items)} points, first={items[0] if items else None}")

    # Quick sanity
    print("\nSanity check:")
    for lang, items in results.items():
        views = [x["views"] for x in items]
        print(f"  {lang}: n={len(views)}, sum={sum(views):,.0f}, "
              f"min={min(views):,}, max={max(views):,}")

    print("\nDone. Data cached.")
