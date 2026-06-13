# P-L5 smoke test: run the analysis pipeline on the PARTIAL cache while the
# polite crawl fills in (pipeline validation only -- numbers not final).
import json, os, hashlib, importlib.util
ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
spec = importlib.util.spec_from_file_location("an", os.path.join(ROOT, "p_l5_analyze.py"))
an = importlib.util.module_from_spec(spec); spec.loader.exec_module(an)
spec2 = importlib.util.spec_from_file_location("fe", os.path.join(ROOT, "p_l5_fetch.py"))
fe = importlib.util.module_from_spec(spec2)
# do NOT exec fe.main; just reuse its chooser constants by re-deriving here
TOP_DAYS = ["2026-03-01","2026-03-10","2026-03-19","2026-03-28","2026-04-06",
            "2026-04-15","2026-04-24","2026-05-03","2026-05-12","2026-05-21","2026-05-30"]
proj = "en.wikipedia"
agg = {}
for day in TOP_DAYS:
    y, m, d = day.split("-")
    with open(os.path.join(ROOT, "data", f"top_{proj}_{y}{m}{d}.json"), encoding="utf-8") as f:
        obj = json.load(f)
    arts = sorted(obj["items"][0]["articles"], key=lambda a: a["rank"])
    kept = 0
    EN_JUNK = ("Special:","Wikipedia:","Portal:","Help:","File:","Category:","Template:",
               "Talk:","User:","Draft:","Module:","MediaWiki:","Book:","TimedText:")
    for a in arts:
        t = a["article"]
        if t in ("Main_Page","-") or t.startswith(EN_JUNK): continue
        kept += 1
        if kept > 40: break
        rec = agg.setdefault(t, {"days": 0, "best_rank": 10**9, "views": 0})
        rec["days"] += 1; rec["best_rank"] = min(rec["best_rank"], a["rank"]); rec["views"] += a["views"]
ranked = sorted(agg.items(), key=lambda kv: (kv[1]["best_rank"], -kv[1]["days"], -kv[1]["views"]))
chosen = [t for t, _ in ranked[:240]]
have = [t for t in chosen if os.path.exists(os.path.join(ROOT, "data",
        f"pa_{proj}_{hashlib.sha1(t.encode()).hexdigest()[:16]}_20250601_20260610.json"))]
print(f"cached so far: {len(have)}/{len(chosen)}")
if len(have) >= 25:
    manifest = {"projects": {proj: {"chosen": have}}, "top_days": TOP_DAYS}
    out, rows = an.run_project(proj, manifest, TOP_DAYS)
    print(json.dumps({k: out[k] for k in ("n_articles_with_data", "n_avalanches",
          "n_censored_excluded", "weekly_amplitude_median")}, indent=1))
    fr = out["fit_R_primary"]
    print(json.dumps(fr, indent=1)[:900])
else:
    print("not enough cached series yet for a smoke run")
