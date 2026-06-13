# OPUS SKEPTIC -- P-L6 STRUCTURAL probe on cached fragments (dataset never built;
# only 22/3861 treated pv series + protlog + tops cached, 0 control screens).
# We do NOT fabricate a damping number. We test the DESIGN's feasibility + the
# endogeneity/selection critiques using what is really on disk:
#   1) reconstruct treated storms whose pv IS cached; measure peak-to-protection LAG
#      (endogeneity timing: does protection land mid-storm = confounded with decay?)
#   2) count how many cached treated series actually QUALIFY as storms (ratio>=5,
#      excess>=2000) -> the real treated-n ceiling
#   3) protection-log selection: what TRIGGERS protection (comment text), and is the
#      protected set systematically the high-amplitude tail? (selection effect)
#   4) feasibility of matched controls: on a treated peak date, how many same-magnitude
#      UNprotected top-1000 articles exist? (can the caliper even be met?)
import json, os, glob, hashlib, datetime as dt, math, re
import numpy as np
import sys
sys.path.insert(0, r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds")
from pl6_fetch import (parse_events, detect_storm, canon, NS_PREFIXES, BLOCK_EXACT,
                       CTRL_BAND, PEAK_LO, PEAK_HI, PV_PRE_D, PV_POST_D)

ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
CACHE = os.path.join(ROOT, "cache", "pl6")

def get_protlog():
    events, page = [], 0
    while True:
        p = os.path.join(CACHE, "protlog_p%03d.json" % page)
        if not os.path.exists(p): break
        obj = json.load(open(p, encoding="utf-8"))
        events.extend(obj.get("query", {}).get("logevents", []))
        if not obj.get("continue", {}).get("lecontinue"): break
        page += 1
    return events

def load_pv_cache():
    # map sha1(canon(title)+d0+d1) -> series ; but we don't know d0/d1 per file.
    # Instead load each pv file and reconstruct its date->views.
    out = {}
    for p in glob.glob(os.path.join(CACHE, "pv_*.json")):
        if p.endswith("pv_avail_probe.json"): continue
        obj = json.load(open(p, encoding="utf-8"))
        items = obj.get("items", [])
        if not items: continue
        title = items[0]["article"]
        series = {}
        for it in items:
            ts = it["timestamp"][:8]
            series["%s-%s-%s" % (ts[:4], ts[4:6], ts[6:8])] = it["views"]
        out[canon(title)] = series
    return out

def main():
    events = get_protlog()
    treated_events, all_logged = parse_events(events)
    print("protlog: %d raw events ; %d unique edit-protected titles ; %d exclusion titles"
          % (len(events), len(treated_events), len(all_logged)))

    # ---- (3) selection: trigger text census on the protection log ----
    reasons = {}
    for ev in events:
        c = (ev.get("comment") or "").lower()
        tag = "other"
        for k in ("vandal", "disrupt", "edit war", "edit-war", "spam", "sock",
                  "blp", "arbitration", "move", "salt", "create", "protection",
                  "high-risk", "template", "persistent"):
            if k in c:
                tag = k; break
        reasons[tag] = reasons.get(tag, 0) + 1
    print("\nprotection-trigger text census (top):")
    for k, v in sorted(reasons.items(), key=lambda x: -x[1])[:12]:
        print("   %-14s %d" % (k, v))

    pv = load_pv_cache()
    print("\ncached treated pv series usable: %d" % len(pv))

    # ---- (1)+(2) reconstruct storms for treated events whose pv IS cached ----
    lags = []; quals = 0; ratios = []; peaks = []
    storm_rows = []
    by_key = {ev["key"]: ev for ev in treated_events}
    for key, series in pv.items():
        ev = by_key.get(key)
        if ev is None:
            # title may differ in canon; try matching by any treated event title
            continue
        det = detect_storm(series, ev["prot_date"], "treated")
        if det.get("peak_date") is None: continue
        pdte = dt.date.fromisoformat(ev["prot_date"])
        peakd = dt.date.fromisoformat(det["peak_date"])
        lag = (pdte - peakd).days
        if det.get("qualifies"):
            quals += 1
            lags.append(lag)
            ratios.append(det["peak_views"] / max(det.get("baseline", 1), 1))
            peaks.append(det["peak_views"])
            storm_rows.append({"key": key, "peak_date": det["peak_date"],
                               "prot_date": ev["prot_date"], "lag": lag,
                               "peak_views": det["peak_views"],
                               "baseline": det.get("baseline"),
                               "ratio": round(det["peak_views"]/max(det.get("baseline",1),1),1)})
    print("\ncached treated that QUALIFY as storms (ratio>=5, excess>=2000): %d" % quals)
    if lags:
        la = np.array(lags)
        print("peak->protection LAG (days): median %.1f  mean %.1f  IQR [%.0f, %.0f]  min %d max %d"
              % (np.median(la), la.mean(), np.percentile(la, 25), np.percentile(la, 75), la.min(), la.max()))
        print("  frac protection lands DURING/AFTER peak (lag>=0): %.2f  (endogenous-to-decay window)"
              % np.mean(la >= 0))
        print("  frac lag in [0,7] (the E3 transferable window): %.2f" % np.mean((la >= 0) & (la <= 7)))
    for r in sorted(storm_rows, key=lambda x: x["lag"]):
        print("   ", r)

    # ---- (4) matched-control feasibility on cached top files ----
    # for each qualifying treated peak date, count unprotected same-magnitude tops
    def load_top(dstr):
        p = os.path.join(CACHE, "top_%s.json" % dstr)
        if not os.path.exists(p): return None
        obj = json.load(open(p, encoding="utf-8"))
        arts = {}
        if obj.get("items"):
            for it in obj["items"][0].get("articles", []):
                arts[it["article"]] = it["views"]
        return arts
    feas = []
    for r in storm_rows:
        tops = load_top(r["peak_date"])
        if tops is None: continue
        pe = r["peak_views"]
        n_band = 0
        for a, v in tops.items():
            if a in BLOCK_EXACT or any(a.startswith(p) for p in NS_PREFIXES): continue
            if a in all_logged: continue   # exclude anything that was itself protected/logged
            if CTRL_BAND[0]*pe <= v <= CTRL_BAND[1]*pe:
                n_band += 1
        feas.append(n_band)
    if feas:
        fa = np.array(feas)
        print("\nmatched-control feasibility: same-day unprotected top-1000 articles within "
              "[%.1f, %.1f]x peak:" % CTRL_BAND)
        print("   per treated storm: median %.0f  min %d  max %d  (n storms checked %d)"
              % (np.median(fa), fa.min(), fa.max(), fa.size))
        print("   frac storms with >=1 candidate: %.2f ; with >=3: %.2f"
              % (np.mean(fa >= 1), np.mean(fa >= 3)))

    out = {"protlog_raw_events": len(events),
           "unique_edit_protected_titles": len(treated_events),
           "exclusion_titles": len(all_logged),
           "trigger_census": reasons,
           "cached_treated_pv_usable": len(pv),
           "cached_treated_qualifying_storms": quals,
           "lag_days": {"median": float(np.median(lags)) if lags else None,
                        "mean": float(np.mean(lags)) if lags else None,
                        "frac_ge0": float(np.mean(np.array(lags) >= 0)) if lags else None,
                        "frac_0to7": float(np.mean((np.array(lags) >= 0) & (np.array(lags) <= 7))) if lags else None,
                        "values": lags},
           "storm_rows": storm_rows,
           "control_feasibility_perstorm": feas,
           "DESIGN_STATUS": "dataset NOT built; 22/3861 treated pv cached, 0 control screens; "
                            "no damping coefficient is computable from cache. This probes design only."}
    json.dump(out, open(os.path.join(ROOT, "results", "skeptic_pl6_probe.json"), "w", encoding="utf-8"),
              indent=1, default=str)
    print("\nwritten results/skeptic_pl6_probe.json")

if __name__ == "__main__":
    main()
