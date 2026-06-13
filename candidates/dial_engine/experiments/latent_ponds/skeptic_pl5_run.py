# OPUS SKEPTIC -- run P-L5 avalanche census on WHATEVER per-article data actually
# exists on disk (the fetch was interrupted -> only ~23 en series). Build a manifest
# from disk, run the committed detector, and report: how many avalanches the real
# data yields, whether a Clauset fit is even admissible, and the sensitivity of any
# "power-law" verdict. Imports the committed analyzer's functions to stay faithful.
import json, os, glob, hashlib, datetime
import numpy as np
import sys
sys.path.insert(0, r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds")
import p_l5_analyze as A

ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
DATA = os.path.join(ROOT, "data")

# discover which en articles actually have a *_20250601_20260610.json file with data
files = sorted(glob.glob(os.path.join(DATA, "pa_en.wikipedia_*_20250601_20260610.json")))
arts = []
for p in files:
    o = json.load(open(p, encoding="utf-8"))
    it = o.get("items", [])
    if it:
        arts.append(it[0]["article"])
print("en per-article series on disk WITH data:", len(arts))

# build a minimal manifest the analyzer expects
manifest = {"ua": A.__dict__.get("UA", "agnostic-framework-research/0.1"),
            "top_days": A_top_days if (A_top_days := None) else
                        [f"2026-{m:02d}-{d:02d}" for (m, d) in
                         [(3,1),(3,10),(3,19),(3,28),(4,6),(4,15),(4,24),(5,3),(5,12),(5,21),(5,30)]],
            "series_window": ["20250601", "20260610"],
            "endpoints": {"top": "...", "per_article": "..."},
            "projects": {"en.wikipedia": {"chosen": arts}}}

out, rows = A.run_project("en.wikipedia", manifest, manifest["top_days"])

summary = {
    "n_articles_with_data": out["n_articles_with_data"],
    "n_articles_failed_baseline_gate": out["n_articles_failed_baseline_gate"],
    "n_avalanches_total": out["n_avalanches"],
    "n_censored_excluded": out["n_censored_excluded"],
    "R_max": out["R_max"],
    "R_quantiles_50_75_90_95_99_995": out["R_quantiles_50_75_90_95_99_995"],
    "fit_R_primary": out["fit_R_primary"],
    "duration_summary": out["duration_summary"],
    "sensitivity_grid_admissible_cells":
        [g for g in out["sensitivity_grid"] if g.get("alpha") is not None],
    "sensitivity_grid_n_cells_total": len(out["sensitivity_grid"]),
    "sensitivity_grid_n_cells_with_fit":
        sum(1 for g in out["sensitivity_grid"] if g.get("alpha") is not None),
    "burstiness": out["burstiness"],
    "variance_duel": out["variance_duel_fixed_cohort"],
}
print(json.dumps(summary, indent=1, default=str))
with open(os.path.join(ROOT, "results", "skeptic_pl5_real_data.json"), "w", encoding="utf-8") as f:
    json.dump({"note": "P-L5 census on the ONLY per-article data actually fetched "
                       "(fetch interrupted; full design = 240en+120ja, reality = "
                       f"{len(arts)} en).", "summary": summary}, f, indent=1, default=str)
print("\nwritten results/skeptic_pl5_real_data.json")
