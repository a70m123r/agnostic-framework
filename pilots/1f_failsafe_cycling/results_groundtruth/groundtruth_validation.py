"""
Pilot 2 Step 2 — Ground-truth EWS validation (Cascade + PhysioNet).

Implements the LOCKED pre-registration
  pilots/1f_failsafe_cycling/PILOT_groundtruth_validation_PRE_REGISTRATION.md  (§3 + §4)
EXACTLY. Every interpretive choice is logged in results_groundtruth/confounds_groundtruth.md
(C1..C9). The candidate metric A_cyc is given NO favorable treatment over the one-pole baselines.

DFA: reuses the TESTED estimator. `dfa_fast` (synthetic_validation/fast_dfa.py) is proven numerically
identical to pilots/1f_failsafe/pilot.py dfa() (max |Δα| < 1e-9); used in the rolling hot loop.

Outputs (results_groundtruth/):
  - groundtruth_results.json   (every number from this run)
  - cascade_tau_trajectories.png, cascade_indicator_rocs.png, physionet_dfa.png

Run:  python groundtruth_validation.py
"""
from __future__ import annotations
import csv, json, sys, io
from pathlib import Path
import numpy as np

# ---- reuse the tested DFA (fast vectorization, proven identical) -------------
HERE = Path(__file__).resolve().parent
SV = HERE.parent / "synthetic_validation"
PILOT = HERE.parent.parent / "1f_failsafe"
for p in (str(SV), str(PILOT)):
    if p not in sys.path:
        sys.path.insert(0, p)
from fast_dfa import dfa_fast, verify_against_pilot   # noqa: E402

from scipy.stats import kendalltau, mannwhitneyu      # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ============================================================================
# LOCKED parameters (§3) — none tunable to favor A_cyc
# ============================================================================
WIN_FRAC = 0.50          # §3: rolling window = 50% of usable per-series length (earlywarnings default)
STRIDE = 1               # §3: stride = 1 daily sample
AUC_MARGIN = 0.05        # §4(a): A_cyc AUC must beat best one-pole by >= 0.05
ALPHA = 0.05             # §4: p<0.05 trend significance
DATA = HERE.parent / "data_groundtruth" / "cascade"
SONDE_CSV = DATA / "sonde_360_squeal.csv"            # knb-lter-ntl.360.2 (see C1)
DAILY_374_CSV = DATA / "daily_374.csv"               # companion daily set (sanity only, C1)

# Documented Peter onset anchors (sourced from Carpenter et al. 2011 Science — see C2)
ONSET_DOY_EARLIEST = 193      # first bass addition, 2008 (earliest documented destabilization onset)
ONSET_YEAR_EARLIEST = 2008
TRANSITION_DOY_COMPLETE = 230 # transition complete by day 230 of 2010
TRANSITION_YEAR_COMPLETE = 2010

SEASONS = [2008, 2009, 2010, 2011]   # ice-free seasons up to & incl. 2011 (§3)


# ============================================================================
# generic helpers (identical for every indicator)
# ============================================================================
def zscore_detrend(x: np.ndarray) -> np.ndarray:
    """§3 rule 3: per-series z-score then linear-detrend. Identical for both lakes."""
    x = np.asarray(x, float)
    sd = x.std()
    z = (x - x.mean()) / sd if sd > 0 else x - x.mean()
    t = np.arange(len(z), dtype=float)
    p = np.polyfit(t, z, 1)
    return z - (p[0] * t + p[1])


def ar1(x: np.ndarray) -> float:
    """lag-1 autocorrelation (one-pole indicator i)."""
    x = np.asarray(x, float)
    x = x - x.mean()
    denom = np.sum(x * x)
    if denom <= 0 or len(x) < 3:
        return np.nan
    return float(np.sum(x[:-1] * x[1:]) / denom)


def interdecile(x: np.ndarray) -> float:
    """A_cyc kernel: P90 - P10 (§3)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return np.nan
    return float(np.percentile(x, 90) - np.percentile(x, 10))


def roc_auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """ROC-AUC via Mann-Whitney U / (n1*n2). pos=label1 (Peter), neg=label0 (Paul)."""
    pos = np.asarray(pos, float); neg = np.asarray(neg, float)
    pos = pos[np.isfinite(pos)]; neg = neg[np.isfinite(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    U, _ = mannwhitneyu(pos, neg, alternative="two-sided")
    return float(U / (len(pos) * len(neg)))


def auc_dir_agnostic(pos, neg) -> float:
    """Direction-agnostic AUC (§3 'Direction-agnostic'), applied identically to ALL indicators."""
    a = roc_auc(pos, neg)
    if not np.isfinite(a):
        return np.nan
    return max(a, 1.0 - a)


def kendall_trend(values: np.ndarray, times: np.ndarray):
    """Kendall-tau trend of a per-window trajectory vs time (§3/§4). Returns (tau, p_two_sided)."""
    v = np.asarray(values, float); t = np.asarray(times, float)
    m = np.isfinite(v) & np.isfinite(t)
    if m.sum() < 4:
        return np.nan, np.nan
    tau, p = kendalltau(t[m], v[m])
    return float(tau), float(p)


# ============================================================================
# Cascade — load + daily-median aggregate the high-frequency sonde (§3 cadence rule)
# ============================================================================
def load_sonde_daily_median():
    """Return dict[(lake,year)] -> (doy_array, daily_median_chl_array), sorted by doy.
    Daily median over the 5-min chl readings; 0% within-season missing days (see C3)."""
    bucket = {}   # (lake,year) -> {doy: [chl,...]}
    with open(SONDE_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            lake = row["lake"]; yr = int(row["year"])
            try:
                doy = int(float(row["doy"]))           # integer day-of-year bucket
            except Exception:
                continue
            try:
                chl = float(row["chl"])
            except Exception:
                chl = np.nan
            bucket.setdefault((lake, yr), {}).setdefault(doy, []).append(chl)
    out = {}
    for k, days in bucket.items():
        doys = sorted(days)
        med = []
        for d in doys:
            vals = np.array(days[d], float)
            med.append(np.nanmedian(vals) if not np.all(np.isnan(vals)) else np.nan)
        out[k] = (np.array(doys, int), np.array(med, float))
    return out


# ---- the locked single rolling window over a within-season series (C4) ------
def rolling_window_indicators(z: np.ndarray, doys: np.ndarray):
    """One rolling pass (window = 50% of season length, stride 1) over a standardized,
    detrended within-season daily-median chl series z (aligned to day-of-year `doys`).

    Returns per-window-centre arrays (identical framework for every indicator, C4):
      centres (doy), ar1(t), var(t), tau(t)=rolling DFA-alpha
    """
    n = len(z)
    W = max(8, int(round(WIN_FRAC * n)))      # 50% of usable per-series length
    if W > n:
        W = n
    cen, a1, vv, tt = [], [], [], []
    for st in range(0, n - W + 1, STRIDE):
        seg = z[st:st + W]
        cen.append(int(doys[st + W // 2]))
        a1.append(ar1(seg))
        vv.append(float(np.var(seg)))
        tt.append(dfa_fast(seg))              # == pilot.dfa(seg)[0]; tested estimator
    return (np.array(cen, int), np.array(a1, float),
            np.array(vv, float), np.array(tt, float), W)


def rolling_acyc_from_tau(tau: np.ndarray):
    """A_cyc(t): trailing inter-decile range (P90-P10) of the tau trajectory using the SAME
    locked 50% fraction over the tau samples (C4). Trailing -> a causal trajectory that can
    decline toward the transition and carry a Kendall-tau trend and a +2sigma band (§4)."""
    n = len(tau)
    if n < 4:
        return np.full(n, np.nan)
    w2 = max(3, int(round(WIN_FRAC * n)))
    out = np.full(n, np.nan)
    for i in range(n):
        lo = max(0, i - w2 + 1)
        seg = tau[lo:i + 1]
        if np.isfinite(seg).sum() >= 3:
            out[i] = interdecile(seg)
    return out


def trailing_kendall_first_sig(values, times, warning_sign, alpha=ALPHA, min_pts=5):
    """First time-point (centre) at which the TRAILING Kendall-tau (all points up to it) reaches
    p<alpha in the warning direction. warning_sign=+1 -> rising is the warning (one-pole CSD);
    -1 -> declining is the warning (A_cyc). Returns (centre_doy_or_None, idx_or_None)."""
    v = np.asarray(values, float); t = np.asarray(times, float)
    for i in range(min_pts - 1, len(v)):
        vi, ti = v[:i + 1], t[:i + 1]
        m = np.isfinite(vi) & np.isfinite(ti)
        if m.sum() < min_pts:
            continue
        tau, p = kendalltau(ti[m], vi[m])
        if np.isfinite(p) and p < alpha and np.sign(tau) == warning_sign:
            return float(t[i]), i
    return None, None


def first_2sigma_cross(values, times, warning_sign, n_baseline=None):
    """First crossing of a pre-shift mean +/- 2*SD band, in the warning direction.
    Baseline = first n_baseline points (default: first 50% of the trajectory)."""
    v = np.asarray(values, float); t = np.asarray(times, float)
    fin = np.isfinite(v)
    if fin.sum() < 6:
        return None
    if n_baseline is None:
        n_baseline = max(4, int(0.5 * fin.sum()))
    base = v[fin][:n_baseline]
    mu, sd = np.nanmean(base), np.nanstd(base)
    if sd <= 0:
        return None
    thr = mu + warning_sign * 2 * sd
    for i in range(n_baseline, len(v)):
        if not np.isfinite(v[i]):
            continue
        if (warning_sign > 0 and v[i] > thr) or (warning_sign < 0 and v[i] < thr):
            return float(t[i])
    return None


# absolute "experiment day" so lead-times can be measured across seasons against the onset
def exp_day(year: int, doy: int) -> int:
    """Days since 2008-01-01 (approx; 365-day years) for ordering windows toward the transition
    and computing lead-times in days. Seasons are May-Sept so leap-day drift is immaterial."""
    return (year - 2008) * 365 + doy


def onset_exp_day_earliest():
    return exp_day(ONSET_YEAR_EARLIEST, ONSET_DOY_EARLIEST)


def onset_exp_day_complete():
    return exp_day(TRANSITION_YEAR_COMPLETE, TRANSITION_DOY_COMPLETE)


# ============================================================================
# Cascade analysis (the §4 PRIMARY gate)
# ============================================================================
def analyze_cascade():
    daily = load_sonde_daily_median()
    per_lake = {}     # lake -> dict of pooled per-window arrays + per-season trajectories
    traj_store = {}   # for plotting

    for lake in ("Peter", "Paul"):
        pooled = {"centres_expday": [], "ar1": [], "var": [], "tau": [], "acyc": [],
                  "season": []}
        seasons_out = {}
        for yr in SEASONS:
            key = (lake, yr)
            if key not in daily:
                continue
            doys, chl = daily[key]
            # drop any nan days defensively (C3: there are none within-season)
            good = np.isfinite(chl)
            doys, chl = doys[good], chl[good]
            if len(chl) < 16:
                continue
            z = zscore_detrend(chl)
            cen, a1, vv, tt, W = rolling_window_indicators(z, doys)
            acyc = rolling_acyc_from_tau(tt)
            ed = np.array([exp_day(yr, c) for c in cen], int)
            seasons_out[yr] = dict(centres_doy=cen.tolist(), centres_expday=ed.tolist(),
                                   ar1=a1.tolist(), var=vv.tolist(), tau=tt.tolist(),
                                   acyc=acyc.tolist(), window_days=int(W),
                                   n_days=int(len(chl)))
            pooled["centres_expday"].extend(ed.tolist())
            pooled["ar1"].extend(a1.tolist())
            pooled["var"].extend(vv.tolist())
            pooled["tau"].extend(tt.tolist())
            pooled["acyc"].extend(acyc.tolist())
            pooled["season"].extend([yr] * len(cen))
        for k in pooled:
            pooled[k] = np.array(pooled[k], float if k != "season" else int)
        per_lake[lake] = {"pooled": pooled, "seasons": seasons_out}
        traj_store[lake] = seasons_out

    # ---------- §4 AUC: Peter (transition-approaching) vs Paul (same-span) -----------
    # "same-span": pool over the identical seasons present in both lakes (here all of 2008-2011).
    indicators = ["acyc", "ar1", "var", "tau"]
    auc = {}
    for ind in indicators:
        pos = per_lake["Peter"]["pooled"][ind]
        neg = per_lake["Paul"]["pooled"][ind]
        auc[ind] = auc_dir_agnostic(pos, neg)

    # ---------- §4 Kendall-tau trend "toward the transition" + lead-time ----------
    # Order each lake's windows by experiment-day (toward the 2010 transition / from 2008 onset).
    # warning direction: A_cyc declining (-1); one-pole CSD rising (+1) (§3).
    warn_sign = {"acyc": -1, "ar1": +1, "var": +1, "tau": +1}
    onset_e = onset_exp_day_earliest()
    onset_c = onset_exp_day_complete()

    trend = {}
    for lake in ("Peter", "Paul"):
        pooled = per_lake[lake]["pooled"]
        order = np.argsort(pooled["centres_expday"])
        ed = pooled["centres_expday"][order]
        trend[lake] = {}
        for ind in indicators:
            vals = pooled[ind][order]
            ktau, kp = kendall_trend(vals, ed)
            # trailing first-significant (warning direction)
            tcen, _ = trailing_kendall_first_sig(vals, ed, warn_sign[ind])
            x2 = first_2sigma_cross(vals, ed, warn_sign[ind])
            lead_e = (onset_e - tcen) if tcen is not None else None
            lead_c = (onset_c - tcen) if tcen is not None else None
            lead_e_2s = (onset_e - x2) if x2 is not None else None
            lead_c_2s = (onset_c - x2) if x2 is not None else None
            trend[lake][ind] = dict(
                kendall_tau=ktau, kendall_p=kp,
                first_sig_expday=tcen,
                lead_days_vs_earliest_onset=lead_e,
                lead_days_vs_transition_complete=lead_c,
                first_2sigma_expday=x2,
                lead_days_2sigma_vs_earliest_onset=lead_e_2s,
                lead_days_2sigma_vs_transition_complete=lead_c_2s,
                warning_sign=warn_sign[ind],
            )

    # ---------- Delecroix lambda (diagnostic only, C9) ----------
    lam = {}
    for lake in ("Peter", "Paul"):
        a1m = np.nanmedian(per_lake[lake]["pooled"]["ar1"])
        lam[lake] = float(-np.log(a1m) / 1.0) if (np.isfinite(a1m) and 0 < a1m < 1) else None

    # ---------- §4 PRIMARY GATE evaluation ----------
    onepole = ["ar1", "var", "tau"]
    best_onepole_auc = float(np.nanmax([auc[i] for i in onepole]))
    best_onepole_auc_name = onepole[int(np.nanargmax([auc[i] for i in onepole]))]

    # lead-time vs best one-pole (use the LOCKED earliest-onset anchor for the gate).
    def lead_vs_onset(lake, ind):
        return trend[lake][ind]["lead_days_vs_earliest_onset"]
    peter_lead = {i: lead_vs_onset("Peter", i) for i in indicators}
    onepole_leads = [peter_lead[i] for i in onepole if peter_lead[i] is not None]
    best_onepole_lead = max(onepole_leads) if onepole_leads else None
    acyc_lead = peter_lead["acyc"]

    # (a) AUC margin
    cond_a = (np.isfinite(auc["acyc"]) and np.isfinite(best_onepole_auc)
              and auc["acyc"] >= best_onepole_auc + AUC_MARGIN)
    # (b) lead-time >= best one-pole
    if acyc_lead is None:
        cond_b = False
    elif best_onepole_lead is None:
        cond_b = True   # A_cyc warns; no one-pole warned at all
    else:
        cond_b = acyc_lead >= best_onepole_lead
    # (c) Paul must-NULL for A_cyc: Kendall p>0.05 (declining) AND no +2sigma decline crossing
    paul_acyc = trend["Paul"]["acyc"]
    paul_decline_sig = (np.isfinite(paul_acyc["kendall_p"]) and paul_acyc["kendall_p"] < ALPHA
                        and paul_acyc["kendall_tau"] < 0)
    paul_2sigma_decline = paul_acyc["first_2sigma_expday"] is not None
    cond_c = (not paul_decline_sig) and (not paul_2sigma_decline)

    primary_pass = bool(cond_a and cond_b and cond_c)

    return dict(
        package_used="knb-lter-ntl.360.2 (squealSondesMet_08to11_forOPUS.csv); see confounds C1",
        variable="chl (chlorophyll-a, optical YSI 6025); primary per §3",
        onset_anchors=dict(
            earliest_documented_onset="day 193 of 2008 (first bass addition, Carpenter 2011)",
            transition_complete="day 230 of 2010 (Carpenter 2011)",
            note="lead-time gate uses earliest-onset anchor (locked); both reported (C2)"),
        per_lake_window={lk: {str(y): {"window_days": per_lake[lk]["seasons"][y]["window_days"],
                                       "n_days": per_lake[lk]["seasons"][y]["n_days"],
                                       "n_windows": len(per_lake[lk]["seasons"][y]["tau"])}
                              for y in per_lake[lk]["seasons"]}
                         for lk in ("Peter", "Paul")},
        AUC=auc,
        best_onepole_auc=best_onepole_auc, best_onepole_auc_name=best_onepole_auc_name,
        trend=trend,
        peter_leadtime_vs_earliest_onset=peter_lead,
        best_onepole_lead_days=best_onepole_lead, acyc_lead_days=acyc_lead,
        delecroix_lambda_diagnostic=lam,
        gate=dict(cond_a_auc_margin=bool(cond_a), cond_b_leadtime=bool(cond_b),
                  cond_c_paul_null=bool(cond_c),
                  paul_acyc_kendall_p=paul_acyc["kendall_p"],
                  paul_acyc_kendall_tau=paul_acyc["kendall_tau"],
                  paul_acyc_2sigma_decline=bool(paul_2sigma_decline),
                  PRIMARY_PASS=primary_pass),
        _traj=traj_store,   # popped before json dump (kept for plotting)
    )


# ============================================================================
# PhysioNet (§4 SECONDARY): static-alpha sanity + adds-over-static-alpha
# ============================================================================
def rr_nn_series(rec, db):
    """Normal-to-normal RR interval series (ms) from .ecg beat annotations (C8)."""
    import wfdb
    ann = wfdb.rdann(rec, "ecg", pn_dir=db)
    samp = np.asarray(ann.sample); sym = np.asarray(ann.symbol)
    fs = ann.fs if ann.fs else 128
    isN = sym == "N"
    # NN = consecutive normal beats only
    nn = []
    for i in range(1, len(samp)):
        if isN[i] and isN[i - 1]:
            nn.append((samp[i] - samp[i - 1]) / fs * 1000.0)
    nn = np.array(nn, float)
    # physiologic plausibility filter (standard HRV): 300-2000 ms
    nn = nn[(nn > 300) & (nn < 2000)]
    return nn


def rolling_acyc_rr(nn: np.ndarray, win_frac=WIN_FRAC, n_windows_target=120):
    """Rolling DFA-alpha tau(t) over the NN series, then A_cyc = inter-decile range of tau.
    For long RR series a fixed window-count keeps runtime bounded while honoring the 50% idea:
    window = 50% is impractical on 1e5-beat series (one window), so per C8 we use a rolling DFA
    with a window sized to yield ~n_windows_target samples and stride = window/n; A_cyc is the
    inter-decile range of that tau(t). All DFA reuse the tested estimator. (Identical for NSR/CHF.)

    Returns: static_alpha_default (whole-series, locked tested-DFA defaults),
             static_alpha1_HRV (whole-series, canonical short-term HRV scales 4-16 beats —
                 the configuration that reproduces Goldberger's CHF result; the proper §4
                 SECONDARY sanity baseline, see C8 cross-check),
             a_cyc (inter-decile range of rolling tau(t)), tau_mean.
    """
    n = len(nn)
    if n < 2000:
        return np.nan, np.nan, np.nan, np.nan
    W = max(800, n // 20)
    stride = max(1, (n - W) // n_windows_target)
    taus = []
    for st in range(0, n - W + 1, stride):
        taus.append(dfa_fast(nn[st:st + W]))
    taus = np.array(taus, float)
    static_alpha_default = dfa_fast(nn)                       # locked tested-DFA defaults
    static_alpha1_hrv = dfa_fast(nn, scale_min=4, scale_max=16, num_scales=8)  # canonical HRV a1
    a_cyc = interdecile(taus)
    tau_mean = float(np.nanmean(taus))
    return float(static_alpha_default), float(static_alpha1_hrv), float(a_cyc), tau_mean


def analyze_physionet(max_records=None):
    import wfdb
    out = {}
    for db, label in [("nsr2db", "healthy"), ("chf2db", "CHF")]:
        recs = wfdb.get_record_list(db)
        if max_records:
            recs = recs[:max_records]
        rows = []
        for rec in recs:
            try:
                nn = rr_nn_series(rec, db)
                sad, sa1, ac, tm = rolling_acyc_rr(nn)
                if np.isfinite(sad):
                    rows.append(dict(record=rec, n_nn=int(len(nn)),
                                     static_alpha_default=sad, static_alpha1_hrv=sa1,
                                     a_cyc=ac, tau_mean=tm))
            except Exception as e:
                rows.append(dict(record=rec, error=f"{type(e).__name__}: {str(e)[:60]}"))
        out[db] = dict(label=label, records=rows)

    nsr = [r for r in out["nsr2db"]["records"] if "static_alpha_default" in r]
    chf = [r for r in out["chf2db"]["records"] if "static_alpha_default" in r]
    sad_nsr = np.array([r["static_alpha_default"] for r in nsr], float)
    sad_chf = np.array([r["static_alpha_default"] for r in chf], float)
    sa1_nsr = np.array([r["static_alpha1_hrv"] for r in nsr], float)
    sa1_chf = np.array([r["static_alpha1_hrv"] for r in chf], float)
    ac_nsr = np.array([r["a_cyc"] for r in nsr], float)
    ac_chf = np.array([r["a_cyc"] for r in chf], float)

    auc_static_default = auc_dir_agnostic(sad_chf, sad_nsr)  # locked tested-DFA defaults
    auc_static_hrv = auc_dir_agnostic(sa1_chf, sa1_nsr)      # canonical HRV a1 (Goldberger baseline)
    auc_rolling = auc_dir_agnostic(ac_chf, ac_nsr)           # rolling A_cyc (the test feature)
    # §4 SECONDARY: does rolling A_cyc add over STATIC alpha (+0.05)? The proper static-alpha
    # baseline is the one that reproduces Goldberger's sanity result (canonical HRV a1). Reported
    # against BOTH baselines for transparency; the scientifically valid comparison uses the HRV a1.
    adds_over_static_hrv = bool(np.isfinite(auc_rolling) and np.isfinite(auc_static_hrv)
                                and auc_rolling >= auc_static_hrv + AUC_MARGIN)
    adds_over_static_default = bool(np.isfinite(auc_rolling) and np.isfinite(auc_static_default)
                                    and auc_rolling >= auc_static_default + AUC_MARGIN)

    return dict(
        n_nsr=len(nsr), n_chf=len(chf),
        static_alpha_default_nsr_mean=float(np.nanmean(sad_nsr)),
        static_alpha_default_chf_mean=float(np.nanmean(sad_chf)),
        static_alpha1_hrv_nsr_mean=float(np.nanmean(sa1_nsr)),
        static_alpha1_hrv_chf_mean=float(np.nanmean(sa1_chf)),
        a_cyc_nsr_mean=float(np.nanmean(ac_nsr)), a_cyc_chf_mean=float(np.nanmean(ac_chf)),
        AUC_static_alpha_default=auc_static_default,
        AUC_static_alpha1_hrv=auc_static_hrv,
        AUC_rolling_acyc=auc_rolling,
        adds_over_static_alpha_hrv=adds_over_static_hrv,
        adds_over_static_alpha_default=adds_over_static_default,
        adds_over_static_alpha=adds_over_static_hrv,   # verdict-relevant = proper HRV baseline
        sanity_static_default_separates=bool(np.isfinite(auc_static_default) and auc_static_default >= 0.70),
        sanity_static_hrv_separates=bool(np.isfinite(auc_static_hrv) and auc_static_hrv >= 0.70),
        per_db=out,
    )


# ============================================================================
# Plots
# ============================================================================
def make_plots(cascade, physio, results_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    traj = cascade["_traj"]
    colors = {"Peter": "tab:red", "Paul": "tab:blue"}

    # ---- Cascade figure: trajectories (left) + pooled distributions w/ AUC (right) ----
    fig, axes = plt.subplots(3, 2, figsize=(13, 11))
    # row 0: tau(t); row 1: A_cyc(t); per season, x = experiment day
    for ci, ind in enumerate(["tau", "acyc"]):
        ax = axes[ci][0]
        for lake in ("Peter", "Paul"):
            first = True
            for yr in SEASONS:
                if yr in traj[lake]:
                    s = traj[lake][yr]
                    ax.plot(s["centres_expday"], s[ind], color=colors[lake], alpha=0.85,
                            lw=1.4, label=lake if first else None)
                    first = False
        # onset + transition markers (experiment-day)
        ax.axvline(onset_exp_day_earliest(), color="k", ls=":", lw=1,
                   label="first bass add (day193/2008)")
        ax.axvline(onset_exp_day_complete(), color="gray", ls="--", lw=1,
                   label="transition complete (day230/2010)")
        ttl = "rolling DFA-α  τ(t)" if ind == "tau" else "A_cyc(t)=P90−P10 of τ (trailing 50%)"
        ax.set_title(f"{ttl}  — by season, vs experiment day")
        ax.set_xlabel("experiment day (from 2008-01-01)"); ax.set_ylabel(ind)
        ax.legend(fontsize=7)
    # right col rows 0,1: pooled distributions
    for ci, ind in enumerate(["tau", "acyc"]):
        ax = axes[ci][1]
        for lake in ("Peter", "Paul"):
            vals = []
            for yr in SEASONS:
                if yr in traj[lake]:
                    vals.extend(traj[lake][yr][ind])
            vals = np.array(vals, float); vals = vals[np.isfinite(vals)]
            ax.hist(vals, bins=20, alpha=0.5, color=colors[lake], label=lake, density=True)
        ax.set_title(f"pooled {ind}: Peter vs Paul  (dir-agnostic AUC={cascade['AUC'][ind]:.3f})")
        ax.set_xlabel(ind); ax.legend(fontsize=8)
    # row 2: epoch-level A_cyc per season (the validated Pilot-1 H1b metric) + AUC bar
    axL = axes[2][0]
    for lake in ("Peter", "Paul"):
        ys = [interdecile(np.array(traj[lake][yr]["tau"], float)) if yr in traj[lake] else np.nan
              for yr in SEASONS]
        axL.plot(SEASONS, ys, "o-", color=colors[lake], label=lake)
    axL.axvspan(2009.5, 2010.5, color="gray", alpha=0.15, label="transition (2010)")
    axL.set_title("epoch-level A_cyc (P90−P10 of τ within each season)\nPredicted: DECLINE toward transition. Observed: Peter RISES.")
    axL.set_xlabel("season"); axL.set_ylabel("A_cyc (epoch)"); axL.set_xticks(SEASONS); axL.legend(fontsize=8)
    axR = axes[2][1]
    inds = ["acyc", "ar1", "var", "tau"]
    aucs = [cascade["AUC"][i] for i in inds]
    bars = axR.bar(inds, aucs, color=["tab:purple", "tab:green", "tab:olive", "tab:cyan"])
    axR.axhline(0.5, color="k", ls=":", lw=1, label="chance")
    axR.axhline(cascade["best_onepole_auc"] + AUC_MARGIN, color="r", ls="--", lw=1,
                label=f"best one-pole+0.05 ({cascade['best_onepole_auc']+AUC_MARGIN:.3f})")
    axR.set_ylim(0.4, 0.85); axR.set_title("Cascade discrimination AUC (Peter vs Paul)\nA_cyc must clear the red line — it does NOT")
    axR.set_ylabel("dir-agnostic AUC"); axR.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(results_dir / "cascade_tau_trajectories.png", dpi=110)
    plt.close(fig)

    # ---- PhysioNet figure ----
    nsr = [r for r in physio["per_db"]["nsr2db"]["records"] if "static_alpha1_hrv" in r]
    chf = [r for r in physio["per_db"]["chf2db"]["records"] if "static_alpha1_hrv" in r]
    fig2, ax2 = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, key, ttl in [
        (ax2[0], "static_alpha1_hrv", f"static α1 (HRV 4-16) — Goldberger sanity\nAUC={physio['AUC_static_alpha1_hrv']:.3f}"),
        (ax2[1], "static_alpha_default", f"static α (tested-DFA default scales)\nAUC={physio['AUC_static_alpha_default']:.3f}"),
        (ax2[2], "a_cyc", f"rolling A_cyc (the test feature)\nAUC={physio['AUC_rolling_acyc']:.3f}")]:
        ax.hist([r[key] for r in nsr], bins=14, alpha=0.55, color="tab:blue", label="NSR (healthy)", density=True)
        ax.hist([r[key] for r in chf], bins=14, alpha=0.55, color="tab:red", label="CHF", density=True)
        ax.set_title(ttl); ax.set_xlabel(key); ax.legend(fontsize=8)
    fig2.suptitle(f"PhysioNet NSR (n={physio['n_nsr']}) vs CHF (n={physio['n_chf']}): "
                  f"rolling A_cyc (AUC {physio['AUC_rolling_acyc']:.3f}) does NOT add over static α1 "
                  f"(AUC {physio['AUC_static_alpha1_hrv']:.3f})", fontsize=10)
    fig2.tight_layout()
    fig2.savefig(results_dir / "physionet_dfa.png", dpi=110)
    plt.close(fig2)


# ============================================================================
def main():
    print("=" * 78)
    print("Pilot 2 Step 2 — Ground-truth EWS validation (Cascade + PhysioNet)")
    print("=" * 78)
    print("\n[verify] fast_dfa == tested pilot.dfa ...")
    ok = verify_against_pilot()
    print(f"[verify] DFA estimator identical: {ok}")

    print("\n[Cascade] loading 360.2 sonde, daily-median aggregating, running locked pipeline ...")
    cascade = analyze_cascade()
    print(f"[Cascade] window per season (Peter): {cascade['per_lake_window']['Peter']}")
    print(f"[Cascade] AUC (dir-agnostic): " +
          ", ".join(f"{k}={v:.3f}" for k, v in cascade["AUC"].items()))
    print(f"[Cascade] best one-pole AUC = {cascade['best_onepole_auc']:.3f} "
          f"({cascade['best_onepole_auc_name']})")
    print(f"[Cascade] Peter lead-time vs earliest onset (days): "
          f"{cascade['peter_leadtime_vs_earliest_onset']}")
    g = cascade["gate"]
    print(f"[Cascade] GATE: (a)AUC+0.05={g['cond_a_auc_margin']} "
          f"(b)lead>=best={g['cond_b_leadtime']} (c)Paul-null={g['cond_c_paul_null']} "
          f"=> PRIMARY_PASS={g['PRIMARY_PASS']}")

    print("\n[PhysioNet] nsr2db (healthy) vs chf2db (CHF): static-α + rolling A_cyc ...")
    physio = analyze_physionet()
    print(f"[PhysioNet] static-α DEFAULT(tested-DFA): NSR={physio['static_alpha_default_nsr_mean']:.3f} "
          f"CHF={physio['static_alpha_default_chf_mean']:.3f}  AUC={physio['AUC_static_alpha_default']:.3f} "
          f"(separates={physio['sanity_static_default_separates']})")
    print(f"[PhysioNet] static-α1 HRV(4-16, Goldberger): NSR={physio['static_alpha1_hrv_nsr_mean']:.3f} "
          f"CHF={physio['static_alpha1_hrv_chf_mean']:.3f}  AUC={physio['AUC_static_alpha1_hrv']:.3f} "
          f"(separates={physio['sanity_static_hrv_separates']})")
    print(f"[PhysioNet] rolling A_cyc AUC={physio['AUC_rolling_acyc']:.3f}  "
          f"adds_over_static_HRV(+0.05)={physio['adds_over_static_alpha_hrv']}  "
          f"adds_over_static_default(+0.05)={physio['adds_over_static_alpha_default']}")

    # ---- verdict per LOCKED §4 ----
    primary = cascade["gate"]["PRIMARY_PASS"]
    adds = physio["adds_over_static_alpha"]
    if primary and adds:
        verdict = "PASS"
    elif primary and not adds:
        verdict = "MIXED"
    else:
        verdict = "FAIL"
    print("\n" + "=" * 78)
    print(f"PRELIMINARY VERDICT (locked §4): {verdict}")
    print("=" * 78)

    # ---- write results json ----
    cascade_json = {k: v for k, v in cascade.items() if k != "_traj"}
    results = dict(
        pilot="pilot2_groundtruth_ews_validation",
        run="real-data, end-to-end",
        dfa_estimator_identical_to_tested=ok,
        locked_params=dict(window="50% of usable per-series length", stride=1,
                           auc_margin=AUC_MARGIN, alpha=ALPHA),
        cascade=cascade_json,
        physionet=physio,
        verdict=verdict,
    )
    out = HERE / "groundtruth_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[write] {out}")

    try:
        make_plots(cascade, physio, HERE)
        print(f"[write] {HERE/'cascade_tau_trajectories.png'}")
        print(f"[write] {HERE/'physionet_dfa.png'}")
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f"[plot] skipped: {type(e).__name__}: {e}")

    return results


if __name__ == "__main__":
    main()
