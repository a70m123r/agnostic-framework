# P-L5 avalanche census -- ANALYSIS stage. Real cached data only; no synthetic data
# read as data (the only generated numbers are PL random variates inside the
# goodness-of-fit bootstrap, clearly labelled, never stored as measurements).
#
# ============================ PRE-REGISTRATION =================================
# Declared BEFORE any tail fit was run (Notarmuzi 2022 caution: exponent is
# operationalization-sensitive; we fix the operationalization first and then
# report sensitivity to it).
#   temporal resolution : daily (per-article endpoint granularity)
#   baseline b(t)       : trailing BASE_WIN-day median of v, window ending at t-1
#                         (spike cannot contaminate its own baseline)
#   burn-in             : first BASE_WIN days of the series are not testable
#   testability gate    : b(t) >= B_MIN views/day (else day not testable;
#                         excludes newborn-article spikes -- disclosed scoping)
#   excited day         : v(t) >= THRESH * b(t)
#   avalanche           : maximal run of consecutive excited days; GAP=0
#                         (one quiet day terminates the avalanche)
#   censoring           : runs touching the first testable day or the last day
#                         of the window are excluded (size/duration censored)
#   PRIMARY observable  : R = max_t v(t)/b(t) over the run   [dimensionless,
#                         baseline-units -- the E-units law]
#   SECONDARY           : X = sum_t (v(t)/b(t) - 1)  [dimensionless integrated
#                         excess], D = run length in days (count of samples)
#   tail fitting        : Clauset xmin scan (KS-minimizing) + continuous MLE
#                         alpha; lognormal alternative fit on the SAME tail;
#                         Vuong normalized LR test. No power-law claim from a
#                         straight-ish line.
#   PRIMARY pre-registered parameters: THRESH=2.0, BASE_WIN=28, GAP=0, B_MIN=5
#   sensitivity grid    : THRESH in {1.5,2.0,3.0} x BASE_WIN in {14,28,56}
#                         x GAP in {0,1}  (18 combos, all reported)
# ===============================================================================

import json, os, csv, hashlib, datetime
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
DATA, RES = os.path.join(ROOT, "data"), os.path.join(ROOT, "results")
THRESH, BASE_WIN, GAP, B_MIN = 2.0, 28, 0, 5.0
S0 = datetime.date(2025, 6, 1)
S1 = datetime.date(2026, 6, 10)   # 12 months + 10-day completion margin (matches fetch)
NDAYS = (S1 - S0).days + 1
rng = np.random.default_rng(0)

# ----------------------------- data loading -----------------------------------
def load_series(proj, title):
    h = hashlib.sha1(title.encode("utf-8")).hexdigest()[:16]
    p = os.path.join(DATA, f"pa_{proj}_{h}_20250601_20260610.json")
    if not os.path.exists(p): return None
    with open(p, "r", encoding="utf-8") as f:
        obj = json.load(f)
    items = obj.get("items", [])
    if not items: return None
    v = np.zeros(NDAYS)
    for it in items:
        ts = it["timestamp"]  # YYYYMMDD00
        d = datetime.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))
        i = (d - S0).days
        if 0 <= i < NDAYS: v[i] = it["views"]
    return v

TOPK = {"en.wikipedia": 40, "ja.wikipedia": 25}   # must match fetch chooser
EN_JUNK = ("Special:","Wikipedia:","Portal:","Help:","File:","Category:","Template:",
           "Talk:","User:","Draft:","Module:","MediaWiki:","Book:","TimedText:")
JA_JUNK = ("特別:","ヘルプ:","ファイル:","カテゴリ:","テンプレート:","ノート:","利用者:",
           "プロジェクト:","モジュール:") + EN_JUNK

def load_top_first_appearance(proj, top_days):
    """first day the article entered the per-day TOP-K (the selection event) --
    the Okamura-style anchored-on-top reference day for the variance duel."""
    junk = EN_JUNK if proj.startswith("en") else JA_JUNK
    first = {}
    for day in top_days:
        y, m, d = day.split("-")
        p = os.path.join(DATA, f"top_{proj}_{y}{m}{d}.json")
        with open(p, "r", encoding="utf-8") as f:
            obj = json.load(f)
        arts = sorted(obj["items"][0]["articles"], key=lambda a: a["rank"])
        kept = 0
        for a in arts:
            t = a["article"]
            if t in ("Main_Page", "メインページ", "-") or t.startswith(junk): continue
            kept += 1
            if kept > TOPK[proj]: break
            if t not in first: first[t] = day
    return first

# --------------------------- avalanche detection -------------------------------
def trailing_median_baseline(v, win):
    b = np.full(v.size, np.nan)
    for t in range(win, v.size):
        b[t] = np.median(v[t - win:t])
    return b

def detect(v, thresh=THRESH, win=BASE_WIN, gap=GAP, bmin=B_MIN):
    """returns list of avalanches: dict(start,end,peakday,R,X,D,censored)"""
    b = trailing_median_baseline(v, win)
    testable = (~np.isnan(b)) & (b >= bmin)
    excited = testable & (v >= thresh * np.maximum(b, 1e-9))
    runs, t = [], 0
    n = v.size
    while t < n:
        if excited[t]:
            s = t; e = t; g = 0; u = t + 1
            while u < n:
                if excited[u]: e = u; g = 0; u += 1
                elif testable[u] and g < gap: g += 1; u += 1
                else: break
            runs.append((s, e)); t = u
        else: t += 1
    first_testable = int(np.argmax(testable)) if testable.any() else None
    out = []
    for s, e in runs:
        seg_v, seg_b = v[s:e+1], b[s:e+1]
        ratio = seg_v / seg_b
        R = float(np.max(ratio))
        X = float(np.sum(np.where(seg_b >= bmin, ratio - 1.0, 0.0)))
        D = int(e - s + 1)
        peak = s + int(np.argmax(ratio))
        cens = (s == first_testable) or (e == n - 1)
        out.append({"start": s, "end": e, "peak": peak, "R": R, "X": X, "D": D, "censored": cens})
    return out, b, testable

# ------------------------------ tail fitting -----------------------------------
def pl_mle(tail, xmin):
    return 1.0 + tail.size / np.sum(np.log(tail / xmin))

def ks_stat_pl(tail, xmin, alpha):
    xs = np.sort(tail); n = xs.size
    cf = 1.0 - (xs / xmin) ** (1.0 - alpha)
    lo = np.arange(0, n) / n; hi = np.arange(1, n + 1) / n
    return float(np.max(np.maximum(np.abs(cf - lo), np.abs(cf - hi))))

def clauset_fit(x, min_tail=50, ncand=120, qmax=0.95):
    xs = np.sort(np.asarray(x, float))
    xs = xs[xs > 0]
    cands = np.unique(np.quantile(xs, np.linspace(0.0, qmax, ncand)))
    best = None
    for xm in cands:
        tail = xs[xs >= xm]
        if tail.size < min_tail: continue
        a = pl_mle(tail, xm)
        ks = ks_stat_pl(tail, xm, a)
        if best is None or ks < best["ks"]:
            best = {"xmin": float(xm), "alpha": float(a), "ks": ks, "ntail": int(tail.size)}
    return best

def lognormal_tail_fit(tail, xmin):
    lx = np.log(tail); lxm = np.log(xmin)
    def nll(p):
        mu, ls = p; s = np.exp(ls)
        if s <= 0 or not np.isfinite(s): return 1e12
        z = (lxm - mu) / s
        logZ = norm.logsf(z)
        if not np.isfinite(logZ): return 1e12
        ll = norm.logpdf((lx - mu) / s) - np.log(s) - lx - logZ
        return -np.sum(ll)
    res = minimize(nll, [np.mean(lx), np.log(np.std(lx) + 1e-9)], method="Nelder-Mead",
                   options={"xatol": 1e-7, "fatol": 1e-7, "maxiter": 8000, "maxfev": 8000})
    mu, s = float(res.x[0]), float(np.exp(res.x[1]))
    return mu, s, float(-res.fun)

def vuong(tail, xmin, alpha, mu, s):
    lx = np.log(tail); lxm = np.log(xmin)
    lpl = np.log(alpha - 1) - np.log(xmin) - alpha * (lx - lxm)
    z0 = (lxm - mu) / s
    lln = norm.logpdf((lx - mu) / s) - np.log(s) - lx - norm.logsf(z0)
    li = lpl - lln
    n = li.size; Rsum = float(np.sum(li)); sd = float(np.std(li, ddof=1))
    if sd == 0: return Rsum, 0.0, 1.0
    z = Rsum / (sd * np.sqrt(n))
    p = float(2 * norm.sf(abs(z)))
    return Rsum, float(z), p

def pl_gof_p(tail, xmin, alpha, ks_emp, B=200, rng=rng):
    """Approximate semi-parametric GOF: synthetic tails from fitted PL with xmin
    FIXED (full Clauset re-scans xmin; this is the disclosed light version)."""
    n = tail.size; cnt = 0
    for _ in range(B):
        u = rng.random(n)
        syn = xmin * (1 - u) ** (-1.0 / (alpha - 1.0))
        a2 = pl_mle(syn, xmin)
        if ks_stat_pl(syn, xmin, a2) >= ks_emp: cnt += 1
    return cnt / B

def bootstrap_alpha(x, B=200, rng=rng):
    xs = np.asarray(x, float); out_a, out_xm = [], []
    for _ in range(B):
        bs = rng.choice(xs, size=xs.size, replace=True)
        f = clauset_fit(bs)
        if f: out_a.append(f["alpha"]); out_xm.append(f["xmin"])
    a = np.array(out_a)
    return {"alpha_ci": [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
            "alpha_boot_median": float(np.median(a)),
            "xmin_boot_iqr": [float(np.percentile(out_xm, 25)), float(np.percentile(out_xm, 75))],
            "B": B}

def full_tail_block(values, label, B_boot=200, B_gof=200):
    f = clauset_fit(values)
    if f is None: return {"label": label, "error": "no admissible xmin"}
    tail = np.sort(np.asarray(values, float)); tail = tail[tail >= f["xmin"]]
    mu, s, llln = lognormal_tail_fit(tail, f["xmin"])
    llpl = float(np.sum(np.log(f["alpha"] - 1) - np.log(f["xmin"])
                        - f["alpha"] * (np.log(tail) - np.log(f["xmin"]))))
    Rsum, z, p = vuong(tail, f["xmin"], f["alpha"], mu, s)
    gof = pl_gof_p(tail, f["xmin"], f["alpha"], f["ks"], B=B_gof)
    boot = bootstrap_alpha(values, B=B_boot)
    if p > 0.1: verdict = "indistinguishable (Vuong p>0.1)"
    elif z > 0: verdict = "power-law favored"
    else: verdict = "lognormal favored"
    return {"label": label, "n_total": int(len(values)), "xmin": f["xmin"],
            "ntail": f["ntail"], "alpha": f["alpha"], "ks": f["ks"],
            "gof_p_xminfixed": gof, "alpha_ci95_bootstrap": boot["alpha_ci"],
            "alpha_boot_median": boot["alpha_boot_median"],
            "xmin_boot_iqr": boot["xmin_boot_iqr"],
            "lognormal_mu": mu, "lognormal_sigma": s,
            "ll_pl": llpl, "ll_ln": llln,
            "vuong_R": Rsum, "vuong_z": z, "vuong_p": p, "verdict": verdict}

def alpha_at_fixed_xmin(values, xmin, min_n=30):
    t = np.asarray(values, float); t = t[t >= xmin]
    if t.size < min_n: return None, int(t.size)
    return float(pl_mle(t, xmin)), int(t.size)

# --------------------------- auxiliary measures --------------------------------
def dow_factors(v):
    """multiplicative day-of-week factors (median-based, robust to spikes)"""
    idx = np.arange(v.size) % 7  # S0 = 2025-06-01 is a Sunday; offset irrelevant
    med_all = np.median(v[v > 0]) if (v > 0).any() else 1.0
    fac = np.ones(7)
    for k in range(7):
        sel = v[idx == k]; sel = sel[sel > 0]
        if sel.size > 5 and med_all > 0: fac[k] = np.median(sel) / med_all
    fac[fac <= 0] = 1.0
    return fac, idx

def weekly_amplitude(v):
    fac, _ = dow_factors(v)
    return float(np.max(fac) / np.min(fac))

def deseasonalize(v):
    fac, idx = dow_factors(v)
    return v / fac[idx]

def hurst_aggvar(v):
    """aggregated-variance Hurst of increments of ln(v+1), DOW-deseasonalized.
    Var(block mean of increments, block m) ~ m^(2H-2)."""
    x = np.log(deseasonalize(v) + 1.0)
    d = np.diff(x)
    if d.size < 120 or np.std(d) == 0: return None
    ms = [1, 2, 4, 7, 14, 28]
    lv, lm = [], []
    for m in ms:
        nb = d.size // m
        if nb < 8: continue
        bm = d[:nb * m].reshape(nb, m).mean(axis=1)
        var = np.var(bm, ddof=1)
        if var <= 0: continue
        lv.append(np.log(var)); lm.append(np.log(m))
    if len(lv) < 4: return None
    slope = np.polyfit(lm, lv, 1)[0]
    return float(1.0 + slope / 2.0)

def burstiness(avs_by_article):
    """pooled inter-avalanche-start intervals, normalized per article by its mean.
    BP = (sig-mu)/(sig+mu)  [Goh-Barabasi]; quantile-ratio q90/q50 (BTI-style per
    Stadlan 2026 motivation; exact BTI formula not reproduced -- our
    operationalization is stated here). Poisson/exponential nulls: BP=0,
    q90/q50 = ln10/ln2 = 3.3219."""
    pooled = []; n_art = 0
    for avs in avs_by_article:
        starts = sorted(a["start"] for a in avs)
        if len(starts) < 3: continue
        iv = np.diff(starts).astype(float)
        if iv.mean() <= 0: continue
        pooled.extend(iv / iv.mean()); n_art += 1
    if len(pooled) < 20: return {"n_articles": n_art, "n_intervals": len(pooled), "note": "too few intervals"}
    p = np.array(pooled)
    mu, sd = p.mean(), p.std(ddof=1)
    bp = (sd - mu) / (sd + mu)
    q50, q90 = np.percentile(p, 50), np.percentile(p, 90)
    return {"n_articles": n_art, "n_intervals": int(p.size),
            "BP": float(bp), "BP_null_poisson": 0.0,
            "q90_q50": float(q90 / q50), "q90_q50_null_exponential": float(np.log(10) / np.log(2)),
            "note": "intervals normalized per-article by mean; small-n per Stadlan caution"}

def variance_duel(series, anchors, tmax=60):
    """Okamura-style: cohort anchored on first top-appearance day; fixed cohort =
    articles with >= tmax days of forward data. Var_i[ln(v(t0+t)/v(t0))] vs t.
    Model L: Var = a + b ln t ; Model P: Var = C t^g. Same y, RSS/AIC compared."""
    rs = []
    for title, (v, t0) in series.items():
        if t0 is None or t0 + tmax >= NDAYS: continue
        v0 = max(v[t0], 1.0)
        traj = np.log(np.maximum(v[t0 + 1:t0 + tmax + 1], 1.0) / v0)
        rs.append(traj)
    if len(rs) < 25: return {"error": "cohort too small", "n_cohort": len(rs)}
    Rm = np.vstack(rs)
    t = np.arange(1, tmax + 1, dtype=float)
    var = Rm.var(axis=0, ddof=1)
    # model L
    AL = np.vstack([np.ones_like(t), np.log(t)]).T
    cL, resL = np.linalg.lstsq(AL, var, rcond=None)[:2]
    rssL = float(resL[0]) if resL.size else float(np.sum((var - AL @ cL) ** 2))
    # model P (nonlinear LSQ on var)
    def rssP_f(p):
        C, g = p
        if C <= 0: return 1e12
        return float(np.sum((var - C * t ** g) ** 2))
    init_g = np.polyfit(np.log(t), np.log(np.maximum(var, 1e-12)), 1)[0]
    init_C = np.exp(np.polyfit(np.log(t), np.log(np.maximum(var, 1e-12)), 1)[1])
    rp = minimize(rssP_f, [init_C, init_g], method="Nelder-Mead",
                  options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 8000})
    rssP = float(rp.fun); C, g = float(rp.x[0]), float(rp.x[1])
    n = t.size
    aicL = n * np.log(rssL / n) + 4; aicP = n * np.log(rssP / n) + 4
    sst = float(np.sum((var - var.mean()) ** 2))
    return {"n_cohort": int(Rm.shape[0]), "tmax": tmax,
            "var_t1": float(var[0]), "var_t7": float(var[6]), "var_t30": float(var[29]),
            "var_t60": float(var[59]),
            "logmodel": {"a": float(cL[0]), "b": float(cL[1]), "rss": rssL,
                         "aic": float(aicL), "r2": 1 - rssL / sst},
            "powermodel": {"C": C, "g": g, "rss": rssP, "aic": float(aicP),
                           "r2": 1 - rssP / sst},
            "delta_aic_log_minus_power": float(aicL - aicP),
            "winner": "log" if aicL < aicP else "power",
            "note": "descriptive fit comparison; Var(t) points are serially correlated (shared cohort), so AIC is heuristic not formal inference; t-range 1-60d sits below Okamura t_c 61-276d (ambiguous-zone caveat)"}

# ------------------------------- pipeline --------------------------------------
def run_project(proj, manifest, top_days):
    chosen = manifest["projects"][proj]["chosen"]
    first_app = load_top_first_appearance(proj, top_days)
    series, skipped = {}, 0
    for t in chosen:
        v = load_series(proj, t)
        if v is None or v.sum() == 0: skipped += 1; continue
        d = first_app.get(t)
        t0 = (datetime.date(*map(int, d.split("-"))) - S0).days if d else None
        series[t] = (v, t0)
    # primary detection
    all_avs, avs_by_article, rows = [], [], []
    n_cens, gate_excluded_articles = 0, 0
    weekly_amps, hursts, med_baselines = [], [], []
    for title, (v, t0) in series.items():
        avs, b, testable = detect(v)
        if not testable.any(): gate_excluded_articles += 1; continue
        keep = [a for a in avs if not a["censored"]]
        n_cens += len(avs) - len(keep)
        avs_by_article.append(keep)
        med_baselines.append((title, float(np.nanmedian(b[testable]))))
        weekly_amps.append(weekly_amplitude(v))
        h = hurst_aggvar(v)
        if h is not None: hursts.append(h)
        for a in keep:
            a2 = dict(a); a2["article"] = title
            a2["peak_date"] = (S0 + datetime.timedelta(days=int(a["peak"]))).isoformat()
            all_avs.append(a2); rows.append(a2)
    R = [a["R"] for a in all_avs]; X = [a["X"] for a in all_avs]; D = [a["D"] for a in all_avs]
    Rq = np.percentile(R, [50, 75, 90, 95, 99, 99.5]) if R else []
    # compact empirical CCDF of R (log-spaced, inspectable census curve)
    Rs = np.sort(np.asarray(R, float))
    grid_pts = np.unique(np.geomspace(max(Rs.min(), 2.0), Rs.max(), 40)) if len(R) else []
    ccdf = [[float(g), float(np.mean(Rs >= g))] for g in grid_pts]
    out = {"project": proj, "n_articles_chosen": len(chosen),
           "n_articles_with_data": len(series), "n_articles_skipped_no_data": skipped,
           "n_articles_failed_baseline_gate": gate_excluded_articles,
           "n_avalanches": len(all_avs), "n_censored_excluded": n_cens,
           "weekly_amplitude_median": float(np.median(weekly_amps)),
           "weekly_amplitude_p90": float(np.percentile(weekly_amps, 90)),
           "hurst_aggvar_median": float(np.median(hursts)) if hursts else None,
           "hurst_aggvar_iqr": [float(np.percentile(hursts, 25)), float(np.percentile(hursts, 75))] if hursts else None,
           "hurst_n_articles": len(hursts)}
    out["R_quantiles_50_75_90_95_99_995"] = [float(q) for q in Rq]
    out["R_max"] = float(np.max(R)) if R else None
    out["R_ccdf_loggrid"] = ccdf
    out["fit_R_primary"] = full_tail_block(R, "R = peak/baseline (dimensionless)")
    out["fit_X_secondary"] = full_tail_block(X, "X = integrated excess (dimensionless)")
    out["duration_summary"] = {"D_median": float(np.median(D)), "D_p90": float(np.percentile(D, 90)),
                               "D_max": int(np.max(D)), "frac_D1": float(np.mean(np.array(D) == 1))}
    # stratifications at pooled xmin (primary R)
    xm = out["fit_R_primary"]["xmin"]
    mid = (datetime.date(2025, 12, 13) - S0).days
    Rh1 = [a["R"] for a in all_avs if a["peak"] <= mid]
    Rh2 = [a["R"] for a in all_avs if a["peak"] > mid]
    a1, n1 = alpha_at_fixed_xmin(Rh1, xm); a2_, n2 = alpha_at_fixed_xmin(Rh2, xm)
    out["time_strata"] = {"split_date": "2025-12-13", "H1_n_av": len(Rh1), "H2_n_av": len(Rh2),
                          "H1_alpha_at_pooled_xmin": a1, "H1_ntail": n1,
                          "H2_alpha_at_pooled_xmin": a2_, "H2_ntail": n2,
                          "note": "top-days sampled Mar-May 2026 => H2 oversampled by selection (disclosed)"}
    med_map = dict(med_baselines)
    bl = np.array([med_map[a["article"]] for a in all_avs])
    terc = np.percentile(bl, [33.3, 66.7])
    strata = {}
    for nm, sel in [("low_baseline", bl <= terc[0]),
                    ("mid_baseline", (bl > terc[0]) & (bl <= terc[1])),
                    ("high_baseline", bl > terc[1])]:
        vals = [all_avs[i]["R"] for i in np.where(sel)[0]]
        aa, nn = alpha_at_fixed_xmin(vals, xm)
        strata[nm] = {"n_av": len(vals), "alpha_at_pooled_xmin": aa, "ntail": nn}
    out["baseline_terciles"] = {"tercile_cuts_views_per_day": [float(terc[0]), float(terc[1])],
                                "strata": strata}
    out["burstiness"] = burstiness(avs_by_article)
    out["variance_duel_fixed_cohort"] = variance_duel(series, None, tmax=60)
    # sensitivity grid (counts + Clauset alpha per combo; no bootstrap, cheap)
    grid = []
    for th in (1.5, 2.0, 3.0):
        for bw in (14, 28, 56):
            for gp in (0, 1):
                vals = []
                for title, (v, t0) in series.items():
                    avs, _, tst = detect(v, thresh=th, win=bw, gap=gp)
                    vals += [a["R"] for a in avs if not a["censored"]]
                f = clauset_fit(vals) if len(vals) >= 60 else None
                grid.append({"thresh": th, "base_win": bw, "gap": gp, "n_av": len(vals),
                             "alpha": (f or {}).get("alpha"), "xmin": (f or {}).get("xmin"),
                             "ntail": (f or {}).get("ntail")})
    out["sensitivity_grid"] = grid
    # DOW-deseasonalized detection (confound check)
    vals_ds = []
    for title, (v, t0) in series.items():
        avs, _, _ = detect(deseasonalize(v))
        vals_ds += [a["R"] for a in avs if not a["censored"]]
    f_ds = clauset_fit(vals_ds) if len(vals_ds) >= 60 else None
    out["dow_deseasonalized_check"] = {"n_av": len(vals_ds),
                                       "alpha": (f_ds or {}).get("alpha"),
                                       "xmin": (f_ds or {}).get("xmin")}
    return out, rows

def main():
    with open(os.path.join(RES, "fetch_manifest.json"), "r", encoding="utf-8") as f:
        manifest = json.load(f)
    top_days = manifest["top_days"]
    results = {"probe": "P-L5-avalanche-census",
               "run_at_utc": datetime.datetime.now(datetime.UTC).isoformat(),
               "preregistration": {
                   "resolution": "daily", "baseline": f"trailing {BASE_WIN}-day median ending t-1",
                   "testability_gate_views_per_day": B_MIN, "threshold": THRESH, "gap": GAP,
                   "primary_observable": "R = max v/b (dimensionless baseline-units)",
                   "secondary": ["X = sum(v/b - 1)", "D = run length (samples)"],
                   "censoring": "runs touching first testable day or last day excluded",
                   "fitting": "Clauset xmin scan + MLE alpha + KS; lognormal alt on same tail; Vuong LR",
                   "declared_before_fitting": True},
               "provenance": {"manifest": "results/fetch_manifest.json",
                              "ua": manifest["ua"], "top_days": top_days,
                              "series_window": manifest["series_window"],
                              "endpoints": manifest["endpoints"]},
               "projects": {}}
    all_rows = []
    for proj in manifest["projects"]:
        print(f"=== {proj} ===", flush=True)
        out, rows = run_project(proj, manifest, top_days)
        results["projects"][proj] = out
        for r in rows: r["project"] = proj
        all_rows += rows
        print(json.dumps({k: out[k] for k in ("n_avalanches", "fit_R_primary")}, indent=1)[:1200], flush=True)
    with open(os.path.join(RES, "p_l5_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    with open(os.path.join(RES, "p_l5_avalanches.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["project", "article", "start", "end", "peak",
                                          "peak_date", "R", "X", "D", "censored"])
        w.writeheader()
        for r in all_rows: w.writerow(r)
    print("results written")

if __name__ == "__main__":
    main()
