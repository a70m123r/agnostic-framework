"""
P-L6 — intervention damping — ANALYZE stage.

Reads data/pl6/pl6_dataset.json (real fetched Wikimedia data, cached) and measures:
  E1  paired post-peak decay rate lambda (treated vs matched unprotected storms)
  E2  paired ln R7 (same-weekday excess ratio at +7d; weekly-cycle robust)
  E3  protection-anchored decay (lag-transferred to the matched control)
  E4  DiD trajectory of ln normalized excess, k = 1..21 post-peak
  plus: pre-peak cascade growth rates (ripple->earthquake half), Streisand/rebound
  census, strata by protection level + trigger, sensitivity variants.

All cross-phenomenon numbers dimensionless (ratios, ln-ratios); lambda is per-day
but is only interpreted through the treated/control RATIO (E-units discipline).
Decay model per storm: ln(excess) ~ a - lambda*k  (2 fitted params; comparison
estimator is nonparametric paired). No fabricated values anywhere.
"""
import json, os, datetime as dt, math, csv
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "pl6")
DS   = os.path.join(DATA, "pl6_dataset.json")

DECAY_K   = (1, 14)
GROWTH_K  = (-5, 0)
MIN_DECAY_PTS  = 7
MIN_GROWTH_PTS = 3
CALIPER   = 0.35
G_SCALE   = 0.15
MAX_CTRL  = 3
LNR_CLIP  = math.log(0.001)   # clip ln R at 0.1% of peak excess (disclosed)
RNG       = np.random.default_rng(0)

def iso_add(d, k):
    return (dt.date.fromisoformat(d) + dt.timedelta(days=k)).isoformat()

def excess_fn(rec):
    s, b, p = rec["series"], rec["baseline"], rec["peak_date"]
    def ex(k):
        v = s.get(iso_add(p, k))
        return None if v is None else v - b
    return ex

def ols_slope(ks, ys):
    ks = np.asarray(ks, float); ys = np.asarray(ys, float)
    return float(np.polyfit(ks, ys, 1)[0])

def storm_metrics(rec):
    ex = excess_fn(rec)
    pe = rec["peak_excess"]
    m = {}
    # decay fit k=1..14
    pts = [(k, ex(k)) for k in range(DECAY_K[0], DECAY_K[1] + 1)]
    pts = [(k, v) for k, v in pts if v is not None and v >= max(5.0, 0.01 * pe)]
    if len(pts) >= MIN_DECAY_PTS:
        m["lambda"] = -ols_slope([k for k, _ in pts], [math.log(v) for _, v in pts])
        m["lambda_npts"] = len(pts)
    else:
        m["lambda"] = None
        m["lambda_npts"] = len(pts)
    # same-weekday ratios
    for kk, name in ((7, "R7"), (14, "R14")):
        v = ex(kk)
        if v is None:
            m[name] = None; m[name + "_floor"] = None
        else:
            m[name] = max(v, 0.5) / pe
            m[name + "_floor"] = (v <= 0)
    # growth fit k=-5..0
    gpts = [(k, ex(k)) for k in range(GROWTH_K[0], GROWTH_K[1] + 1)]
    gpts = [(k, v) for k, v in gpts if v is not None and v >= max(5.0, 0.02 * pe)]
    if len(gpts) >= MIN_GROWTH_PTS:
        m["g"] = ols_slope([k for k, _ in gpts], [math.log(v) for _, v in gpts])
        m["g_npts"] = len(gpts)
    else:
        m["g"] = None; m["g_npts"] = len(gpts)
    # tail mass + rebound + empirical half-decay day
    aucv = [max(ex(k), 0.0) for k in range(1, 22) if ex(k) is not None]
    m["auc21"] = (sum(aucv) / pe) if aucv else None
    m["rebound"] = any((ex(k) or 0) > pe for k in range(3, 15))
    m["t_half"] = None
    for k in range(1, 22):
        v = ex(k)
        if v is not None and v <= 0.5 * pe:
            m["t_half"] = k; break
    m["ln_x"] = {}
    for k in range(0, 22):
        v = ex(k)
        m["ln_x"][k] = None if v is None else max(math.log(max(v, 0.5) / pe), LNR_CLIP)
    return m

def lambda_window(rec, k0, k1):
    ex = excess_fn(rec); pe = rec["peak_excess"]
    pts = [(k, ex(k)) for k in range(k0, k1 + 1)]
    pts = [(k, v) for k, v in pts if v is not None and v >= max(5.0, 0.01 * pe)]
    if len(pts) < MIN_DECAY_PTS:
        return None
    return -ols_slope([k for k, _ in pts], [math.log(v) for _, v in pts])

def boot_ci(vals, B=4000, stat=np.mean):
    vals = np.asarray(vals, float)
    if len(vals) == 0:
        return None, (None, None)
    idx = RNG.integers(0, len(vals), size=(B, len(vals)))
    s = stat(vals[idx], axis=1)
    return float(stat(vals)), (float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5)))

def signflip_p(vals, B=20000):
    vals = np.asarray(vals, float)
    if len(vals) == 0:
        return None
    obs = abs(vals.mean())
    flips = RNG.choice([-1.0, 1.0], size=(B, len(vals)))
    null = np.abs((flips * vals).mean(axis=1))
    return float((null >= obs).mean())

def q(vals, pcts=(10, 25, 50, 75, 90)):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return {("p%d" % p): round(float(np.percentile(vals, p)), 4) for p in pcts}

def main():
    with open(DS, "r", encoding="utf-8") as f:
        ds = json.load(f)
    treated  = [t for t in ds["treated"] if t["qualifies"]]
    controls = ds["controls"]
    print("qualifying treated storms: %d" % len(treated))

    for t in treated:
        t["m"] = storm_metrics(t)
        t["lag"] = (dt.date.fromisoformat(t["prot_date"]) - dt.date.fromisoformat(t["peak_date"])).days
    cq = [c for c in controls if c["qualifies"]]
    for c in cq:
        c["m"] = storm_metrics(c)
    clean = [c for c in cq if not c["prot_event_near_window"] and not c["currently_edit_protected"]]
    flagged = [c for c in cq if c not in clean and not c["prot_event_near_window"]]
    print("qualifying controls: %d (clean %d, flagged-standing-protection %d)" % (len(cq), len(clean), len(flagged)))

    def match(treated_list, pool, caliper=CALIPER, max_ctrl=MAX_CTRL):
        pairs = []
        for t in treated_list:
            if t["m"]["lambda"] is None:
                continue
            lt = math.log10(t["peak_excess"])
            cands = []
            for c in pool:
                if c["m"]["lambda"] is None:
                    continue
                dmag = abs(math.log10(c["peak_excess"]) - lt)
                if dmag > caliper:
                    continue
                if t["m"]["g"] is not None and c["m"]["g"] is not None:
                    dg = abs(c["m"]["g"] - t["m"]["g"]) / G_SCALE
                else:
                    dg = 1.0
                cands.append((dmag / caliper + dg, c))
            if not cands:
                continue
            cands.sort(key=lambda x: x[0])
            pairs.append((t, [c for _, c in cands[:max_ctrl]]))
        return pairs

    pairs = match(treated, clean)
    print("matched treated: %d / %d (caliper %.2f, <=%d controls)" % (len(pairs), len(treated), CALIPER, MAX_CTRL))

    # ---------- paired endpoints ----------
    def paired(pairs, fld, transform=None):
        out = []
        for t, cs in pairs:
            tv = t["m"][fld]
            cvs = [c["m"][fld] for c in cs if c["m"][fld] is not None]
            if tv is None or not cvs:
                continue
            if transform:
                tv = transform(tv); cvs = [transform(v) for v in cvs]
            out.append(tv - float(np.mean(cvs)))
        return out

    d_lambda = paired(pairs, "lambda")
    d_lnR7   = paired(pairs, "R7", transform=lambda v: max(math.log(v), LNR_CLIP))
    d_lnR14  = paired(pairs, "R14", transform=lambda v: max(math.log(v), LNR_CLIP))
    d_lnauc  = paired(pairs, "auc21", transform=lambda v: math.log(max(v, 1e-3)))

    lam_t = [t["m"]["lambda"] for t, _ in pairs]
    lam_c = [float(np.mean([c["m"]["lambda"] for c in cs])) for _, cs in pairs]
    ratio_pairs = [a / b for a, b in zip(lam_t, lam_c) if b and b > 0 and a is not None]

    mean_dl, ci_dl = boot_ci(d_lambda); p_dl = signflip_p(d_lambda)
    med_dl, ci_med_dl = boot_ci(d_lambda, stat=lambda x, axis=None: np.median(x, axis=axis))
    mean_dr7, ci_dr7 = boot_ci(d_lnR7); p_dr7 = signflip_p(d_lnR7)
    mean_dr14, ci_dr14 = boot_ci(d_lnR14); p_dr14 = signflip_p(d_lnR14)
    mean_dauc, ci_dauc = boot_ci(d_lnauc); p_dauc = signflip_p(d_lnauc)
    med_ratio, ci_ratio = boot_ci(ratio_pairs, stat=lambda x, axis=None: np.median(x, axis=axis))

    # E3: protection-anchored, lag-transferred (0 <= lag <= 7)
    d_lam_prot = []
    for t, cs in pairs:
        if not (0 <= t["lag"] <= 7):
            continue
        k0, k1 = t["lag"] + 1, t["lag"] + 14
        lt = lambda_window(t, k0, k1)
        lcs = [lambda_window(c, k0, k1) for c in cs]
        lcs = [v for v in lcs if v is not None]
        if lt is None or not lcs:
            continue
        d_lam_prot.append(lt - float(np.mean(lcs)))
    mean_dlp, ci_dlp = boot_ci(d_lam_prot); p_dlp = signflip_p(d_lam_prot)

    # E4: DiD trajectory
    did = {}
    for k in range(1, 22):
        dk = []
        for t, cs in pairs:
            tv = t["m"]["ln_x"].get(k)
            cvs = [c["m"]["ln_x"].get(k) for c in cs]
            cvs = [v for v in cvs if v is not None]
            if tv is None or not cvs:
                continue
            dk.append(tv - float(np.mean(cvs)))
        if dk:
            mn, ci = boot_ci(dk, B=2000)
            did[k] = {"mean": round(mn, 4), "ci": [round(ci[0], 4), round(ci[1], 4)], "n": len(dk)}

    # growth (ripple->earthquake half)
    g_t  = [t["m"]["g"] for t, _ in pairs if t["m"]["g"] is not None]
    g_c  = [c["m"]["g"] for _, cs in pairs for c in cs if c["m"]["g"] is not None]
    g_all_t = [t["m"]["g"] for t in treated if t["m"]["g"] is not None]
    dg_match = [abs(t["m"]["g"] - float(np.mean([c["m"]["g"] for c in cs if c["m"]["g"] is not None])))
                for t, cs in pairs if t["m"]["g"] is not None and any(c["m"]["g"] is not None for c in cs)]

    # rebound / Streisand census
    reb_t = sum(1 for t, _ in pairs if t["m"]["rebound"])
    reb_c = sum(1 for _, cs in pairs for c in cs if c["m"]["rebound"])
    n_c_all = sum(len(cs) for _, cs in pairs)
    pos_dl = sum(1 for d in d_lambda if d < 0)   # treated decays SLOWER than control

    # strata
    strata = {}
    for t, cs in pairs:
        tv = t["m"]["lambda"]
        cv = float(np.mean([c["m"]["lambda"] for c in cs]))
        for key in ("level:" + str(t.get("level")), "trigger:" + str(t.get("trigger"))):
            s = strata.setdefault(key, {"n": 0, "d": [], "lam_t": [], "lam_c": []})
            s["n"] += 1; s["d"].append(tv - cv); s["lam_t"].append(tv); s["lam_c"].append(cv)
    strata_out = {}
    for k, s in sorted(strata.items()):
        strata_out[k] = {"n": s["n"],
                         "median_lambda_t": round(float(np.median(s["lam_t"])), 4),
                         "median_lambda_c": round(float(np.median(s["lam_c"])), 4),
                         "mean_paired_delta": round(float(np.mean(s["d"])), 4)}

    # lag distribution (endogeneity reading)
    lags = [t["lag"] for t, _ in pairs]

    # unmatched treated (mostly small storms below top-1000 floor)
    matched_keys = {t["key"] for t, _ in pairs}
    unmatched = [t for t in treated if t["key"] not in matched_keys and t["m"]["lambda"] is not None]

    # sensitivity variants
    sens = {}
    def variant(name, pairs_v):
        dv = paired(pairs_v, "lambda")
        if dv:
            mn, ci = boot_ci(dv, B=2000)
            sens[name] = {"n": len(dv), "mean_d_lambda": round(mn, 4),
                          "ci": [round(ci[0], 4), round(ci[1], 4)], "p_signflip": signflip_p(dv, B=5000)}
        else:
            sens[name] = {"n": 0}
    variant("caliper_0.25", match(treated, clean, caliper=0.25))
    variant("nearest_1_control", match(treated, clean, max_ctrl=1))
    variant("include_flagged_controls", match(treated, clean + flagged))
    pairs_lag = [(t, cs) for t, cs in pairs if 0 <= t["lag"] <= 7]
    variant("lag_0_to_7_only", pairs_lag)
    # k=1..10 decay window
    d10 = []
    for t, cs in pairs:
        lt = lambda_window(t, 1, 10)
        lcs = [v for v in (lambda_window(c, 1, 10) for c in cs) if v is not None]
        if lt is not None and lcs:
            d10.append(lt - float(np.mean(lcs)))
    if d10:
        mn, ci = boot_ci(d10, B=2000)
        sens["decay_window_k1_10"] = {"n": len(d10), "mean_d_lambda": round(mn, 4),
                                      "ci": [round(ci[0], 4), round(ci[1], 4)],
                                      "p_signflip": signflip_p(d10, B=5000)}

    results = {
        "probe": "P-L6-intervention-damping",
        "n": {"treated_qualifying": len(treated), "matched_pairs": len(pairs),
              "controls_clean": len(clean), "controls_flagged": len(flagged),
              "controls_used": n_c_all, "unmatched_treated": len(unmatched)},
        "E1_lambda_per_day": {
            "treated_median": round(float(np.median(lam_t)), 4) if lam_t else None,
            "treated_IQR": q(lam_t, (25, 50, 75)),
            "control_median": round(float(np.median(lam_c)), 4) if lam_c else None,
            "control_IQR": q(lam_c, (25, 50, 75)),
            "paired_mean_delta": round(mean_dl, 4) if mean_dl is not None else None,
            "paired_mean_delta_ci95": [round(x, 4) for x in ci_dl] if ci_dl[0] is not None else None,
            "paired_median_delta": round(med_dl, 4) if med_dl is not None else None,
            "paired_median_delta_ci95": [round(x, 4) for x in ci_med_dl] if ci_med_dl[0] is not None else None,
            "p_signflip": p_dl,
            "paired_ratio_median": round(med_ratio, 4) if med_ratio is not None else None,
            "paired_ratio_median_ci95": [round(x, 4) for x in ci_ratio] if ci_ratio[0] is not None else None,
            "frac_treated_slower": round(pos_dl / len(d_lambda), 4) if d_lambda else None,
            "delta_distribution": q(d_lambda)},
        "E2_same_weekday_ratios": {
            "R7_treated_median": q([t["m"]["R7"] for t, _ in pairs], (50,)),
            "R7_control_median": q([c["m"]["R7"] for _, cs in pairs for c in cs], (50,)),
            "paired_mean_d_lnR7": round(mean_dr7, 4) if mean_dr7 is not None else None,
            "ci95": [round(x, 4) for x in ci_dr7] if ci_dr7[0] is not None else None,
            "p_signflip": p_dr7,
            "paired_mean_d_lnR14": round(mean_dr14, 4) if mean_dr14 is not None else None,
            "ci95_R14": [round(x, 4) for x in ci_dr14] if ci_dr14[0] is not None else None,
            "p_signflip_R14": p_dr14},
        "E3_protection_anchored": {
            "n": len(d_lam_prot),
            "paired_mean_delta_lambda": round(mean_dlp, 4) if mean_dlp is not None else None,
            "ci95": [round(x, 4) for x in ci_dlp] if ci_dlp and ci_dlp[0] is not None else None,
            "p_signflip": p_dlp},
        "E4_did_ln_excess": did,
        "tail_mass_auc21": {
            "paired_mean_d_ln_auc21": round(mean_dauc, 4) if mean_dauc is not None else None,
            "ci95": [round(x, 4) for x in ci_dauc] if ci_dauc[0] is not None else None,
            "p_signflip": p_dauc},
        "growth_ripple_to_earthquake": {
            "g_treated_matched": q(g_t),
            "g_controls_matched": q(g_c),
            "g_all_treated": q(g_all_t),
            "doubling_time_days_treated_median": round(math.log(2) / float(np.median(g_t)), 3) if g_t and np.median(g_t) > 0 else None,
            "match_quality_mean_abs_dg": round(float(np.mean(dg_match)), 4) if dg_match else None},
        "streisand_rebound": {
            "treated_rebound_frac": round(reb_t / len(pairs), 4) if pairs else None,
            "control_rebound_frac": round(reb_c / n_c_all, 4) if n_c_all else None,
            "treated_rebound_n": reb_t, "treated_n": len(pairs)},
        "lag_peak_to_protection_days": q(lags) if lags else None,
        "lag_counts": {str(L): lags.count(L) for L in sorted(set(lags))} if lags else None,
        "strata": strata_out,
        "unmatched_treated_median_lambda": round(float(np.median([t["m"]["lambda"] for t in unmatched])), 4) if unmatched else None,
        "sensitivity": sens,
        "model_accounting": {"decay_model_params_per_storm": 2,
                             "comparison": "nonparametric paired (sign-flip permutation + bootstrap)",
                             "ln_ratio_clip": "ln R clipped at ln(0.001), disclosed"},
    }

    out = os.path.join(BASE, "pl6_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print("results written: %s" % out)

    # matched pairs CSV
    csvp = os.path.join(DATA, "pl6_matched_pairs.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["treated", "peak_date", "peak_views", "baseline", "level", "trigger", "lag_d",
                    "lambda_t", "R7_t", "g_t", "controls", "lambda_c_mean", "R7_c_mean", "d_lambda"])
        for t, cs in pairs:
            lc = float(np.mean([c["m"]["lambda"] for c in cs]))
            r7c = [c["m"]["R7"] for c in cs if c["m"]["R7"] is not None]
            w.writerow([t["key"], t["peak_date"], t["peak_views"], t["baseline"], t["level"],
                        t["trigger"], t["lag"],
                        round(t["m"]["lambda"], 4), round(t["m"]["R7"], 4) if t["m"]["R7"] else None,
                        round(t["m"]["g"], 4) if t["m"]["g"] is not None else None,
                        ";".join(c["key"] for c in cs), round(lc, 4),
                        round(float(np.mean(r7c)), 4) if r7c else None,
                        round(t["m"]["lambda"] - lc, 4)])
    print("pairs csv: %s" % csvp)

    # console digest
    print("\n--- P-L6 digest ---")
    print("median lambda treated %.3f /d vs matched control %.3f /d ; paired mean delta %+.3f [%.3f, %.3f] p=%.4f"
          % (np.median(lam_t), np.median(lam_c), mean_dl, ci_dl[0], ci_dl[1], p_dl))
    print("paired ratio (t/c) median %.3f [%.3f, %.3f]" % (med_ratio, ci_ratio[0], ci_ratio[1]))
    print("d lnR7 %+0.3f [%.3f, %.3f] p=%.4f ; d lnR14 %+0.3f p=%.4f"
          % (mean_dr7, ci_dr7[0], ci_dr7[1], p_dr7, mean_dr14, p_dr14))
    if mean_dlp is not None:
        print("protection-anchored paired delta lambda %+0.3f [%.3f, %.3f] p=%.4f (n=%d)"
              % (mean_dlp, ci_dlp[0], ci_dlp[1], p_dlp, len(d_lam_prot)))
    print("DiD ln-excess at k=7: %s ; k=14: %s" % (did.get(7), did.get(14)))
    print("growth g treated median %.3f /d (doubling %.2f d)"
          % (np.median(g_t), math.log(2) / np.median(g_t)) if g_t and np.median(g_t) > 0 else "growth: n/a")
    print("rebound: treated %d/%d vs controls %d/%d"
          % (reb_t, len(pairs), reb_c, n_c_all))
    print("strata: %s" % json.dumps(strata_out))
    print("sensitivity: %s" % json.dumps(sens))

if __name__ == "__main__":
    main()
