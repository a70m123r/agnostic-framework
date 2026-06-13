# P-L5 avalanche census -- FETCH stage (real data only; cached to disk)
# Program register: exploratory instrument, read-only, no fabrication.
# Endpoints (verified-live family, Wikimedia REST v1):
#   top:         /metrics/pageviews/top/{project}/all-access/{yyyy}/{mm}/{dd}
#   per-article: /metrics/pageviews/per-article/{project}/all-access/user/{article}/daily/{YYYYMMDD}/{YYYYMMDD}
# UA: agnostic-framework-research/0.1 (research instrument)
#
# Sampling design (declared before fetching):
#   - top-lists: 11 days spanning 3 months (2026-03-01 .. 2026-05-30, every ~9 days), en + ja
#   - union ranked by (days_appeared desc, best_rank asc, total_top_views desc)
#   - cap: en 300 articles, ja 150 articles (budget)
#   - per-article daily window: 2025-06-01 .. 2026-05-31 (12 months)
#   - junk filter: namespace-prefixed titles, Main_Page/メインページ, "-"
# Known selection property (disclosed): articles enter the census by reaching the
# top-100 of >=1 sampled day => census is CONDITIONAL on reaching top-of-pond;
# small-spike end is selection-truncated; tail end is what we fit.

import json, time, hashlib, os, sys, urllib.request, urllib.parse, datetime

BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews"
UA = "agnostic-framework-research/0.1 (research instrument)"
ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
DATA = os.path.join(ROOT, "data")
SLEEP = 0.18  # modest rate (per-article endpoint rate-limits anonymous bursts)

TOP_DAYS = ["2026-03-01","2026-03-10","2026-03-19","2026-03-28","2026-04-06",
            "2026-04-15","2026-04-24","2026-05-03","2026-05-12","2026-05-21","2026-05-30"]
SERIES_START, SERIES_END = "20250601", "20260610"  # 12 months + 10-day completion
# margin so late-May avalanches complete instead of hitting the right-censor rule
# (window extension declared before analysis; one request per article regardless)
CAPS = {"en.wikipedia": 240, "ja.wikipedia": 120}
# union rule (declared): per sampled day take the top-K ranked articles AFTER the
# junk filter (K_en=40, K_ja=25) -- "reached top-of-pond that day". This keeps the
# one-day spike carriers; a days-appeared ranking over the full top-1000 would
# select only perennial heads and systematically drop the avalanche carriers.
TOPK = {"en.wikipedia": 40, "ja.wikipedia": 25}

EN_JUNK_PREFIX = ("Special:","Wikipedia:","Portal:","Help:","File:","Category:","Template:",
                  "Talk:","User:","Draft:","Module:","MediaWiki:","Book:","TimedText:",
                  "User_talk:","Wikipedia_talk:","Template_talk:","Category_talk:","File_talk:")
JA_JUNK_PREFIX = ("特別:","Wikipedia:","Portal:","Help:","ヘルプ:","ファイル:","カテゴリ:","Category:",
                  "Template:","テンプレート:","ノート:","利用者:","プロジェクト:","モジュール:","MediaWiki:")
EXACT_JUNK = {"Main_Page","メインページ","-","Search","Pornhub.com"}  # Pornhub.com kept? it IS an article; remove from junk
EXACT_JUNK = {"Main_Page","メインページ","-"}

def fetch(url, cache_key):
    p = os.path.join(DATA, cache_key)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last, hard_fail = None, 0
    for attempt in range(60):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                obj = json.loads(r.read().decode("utf-8"))
            with open(p, "w", encoding="utf-8") as f:
                json.dump(obj, f)
            time.sleep(SLEEP)
            return obj
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 404:           # article has no views rows in window
                obj = {"items": [], "_http": 404}
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(obj, f)
                time.sleep(SLEEP)
                return obj
            if e.code == 429:           # expected-normal: token bucket; honor Retry-After
                ra = e.headers.get("Retry-After")
                time.sleep(min(float(ra) + 1.0 if ra and ra.isdigit() else 30.0, 90.0))
                continue
            hard_fail += 1
            if hard_fail >= 6: break
            time.sleep(2.0 * hard_fail)
        except Exception as e:
            last = repr(e); hard_fail += 1
            if hard_fail >= 6: break
            time.sleep(2.0 * hard_fail)
    raise RuntimeError(f"fetch failed after retries ({last}): {url}")

def is_junk(title, proj):
    if title in EXACT_JUNK: return True
    pref = EN_JUNK_PREFIX if proj.startswith("en") else (JA_JUNK_PREFIX + EN_JUNK_PREFIX)
    return title.startswith(pref)

def main():
    os.makedirs(DATA, exist_ok=True)
    manifest = {"fetched_at_utc": datetime.datetime.now(datetime.UTC).isoformat(),
                "ua": UA, "top_days": TOP_DAYS,
                "series_window": [SERIES_START, SERIES_END],
                "endpoints": {"top": BASE + "/top/{project}/all-access/{y}/{m}/{d}",
                              "per_article": BASE + "/per-article/{project}/all-access/user/{article}/daily/{s}/{e}"},
                "projects": {}}
    for proj, cap in CAPS.items():
        agg = {}   # title -> dict(days, best_rank, views_sum) over per-day top-K survivors
        for day in TOP_DAYS:
            y, m, d = day.split("-")
            url = f"{BASE}/top/{proj}/all-access/{y}/{m}/{d}"
            key = f"top_{proj}_{y}{m}{d}.json"
            obj = fetch(url, key)
            arts = sorted(obj["items"][0]["articles"], key=lambda a: a["rank"])
            kept = 0
            for a in arts:
                t = a["article"]
                if is_junk(t, proj): continue
                kept += 1
                if kept > TOPK[proj]: break
                rec = agg.setdefault(t, {"days": 0, "best_rank": 10**9, "views": 0})
                rec["days"] += 1
                rec["best_rank"] = min(rec["best_rank"], a["rank"])
                rec["views"] += a["views"]
        ranked = sorted(agg.items(), key=lambda kv: (kv[1]["best_rank"], -kv[1]["days"], -kv[1]["views"]))
        chosen = [t for t, _ in ranked[:cap]]
        print(f"{proj}: union after filter = {len(agg)}, chosen = {len(chosen)}", flush=True)
        ok, n404 = 0, 0
        for i, t in enumerate(chosen):
            enc = urllib.parse.quote(t, safe="")
            url = f"{BASE}/per-article/{proj}/all-access/user/{enc}/daily/{SERIES_START}/{SERIES_END}"
            h = hashlib.sha1(t.encode("utf-8")).hexdigest()[:16]
            key = f"pa_{proj}_{h}_{SERIES_START}_{SERIES_END}.json"
            obj = fetch(url, key)
            if obj.get("_http") == 404: n404 += 1
            else: ok += 1
            if (i + 1) % 10 == 0:
                print(f"  {proj} {i+1}/{len(chosen)} fetched ({time.strftime('%H:%M:%S')})", flush=True)
        manifest["projects"][proj] = {
            "union_size_after_filter": len(agg), "chosen": chosen,
            "chosen_n": len(chosen), "series_ok": ok, "series_404": n404,
            "agg_meta": {t: agg[t] for t in chosen}}
    with open(os.path.join(ROOT, "results", "fetch_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("manifest written")

if __name__ == "__main__":
    main()
