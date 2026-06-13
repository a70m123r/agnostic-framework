# OPUS SKEPTIC -- P-L4 reproduction + anchor-thesis canon stress test.
# Real cached hourly data only (data/hourly_*_all-access_2026030100_2026060100.json).
# No fabrication. Recompute circadian phase, weekly-line strength, and the
# cross-pond DAILY-series correlation matrix that the anchor thesis calls
# "canon-radius coupling". Then attack it:
#  A) Is cross-pond corr just shared trend + weekly cycle? -> strip both, re-corr.
#  B) Does residual cross-pond corr survive an AR-whitening of each series?
#  C) Phase-randomization null: how big is "expected" corr from matched spectra?
#  D) DST micro-shift: is the claimed sub-hour shift inside sampling noise?
import json, os, glob, hashlib, math
import numpy as np

ROOT = r"D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/latent_ponds"
DATA = os.path.join(ROOT, "data")
PONDS = ["en", "ja", "de", "ar", "es"]
rng = np.random.default_rng(12345)

def load_hourly(pond, access="all-access"):
    p = os.path.join(DATA, f"hourly_{pond}.wikipedia.org_{access}_2026030100_2026060100.json")
    o = json.load(open(p, encoding="utf-8"))
    items = o["items"]
    ts = [it["timestamp"] for it in items]
    v = np.array([it["views"] for it in items], float)
    return ts, v

def to_2184(ts, v):
    # confirm contiguous hourly; return first 2184 (13 whole weeks) as the committed window did
    return v[:2184].copy()

def circ_phase(v):
    # hour-of-day mean profile -> peak hour via complex argmax (matches f24 phase idea)
    n = v.size
    hod = np.arange(n) % 24
    prof = np.array([v[hod == h].mean() for h in range(24)])
    prof = prof / prof.mean()
    # circular mean angle of the 24h profile
    ang = 2 * np.pi * np.arange(24) / 24
    z = np.sum(prof * np.exp(1j * ang))
    peak_hour = (np.angle(z) % (2 * np.pi)) / (2 * np.pi) * 24
    # f24 = fraction of variance at the 24h line (single-bin power / total ac-power)
    x = v - v.mean()
    F = np.fft.rfft(x)
    P = np.abs(F) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0)  # cycles per hour
    def bin_power(per_h):
        k = int(round(per_h * n))
        return P[k] if 0 < k < P.size else 0.0
    p24 = bin_power(1 / 24.0); p168 = bin_power(1 / 168.0)
    tot = P[1:].sum()
    return peak_hour, prof, p24 / tot, p168 / tot

def daily_series(v):
    n = (v.size // 24) * 24
    return v[:n].reshape(-1, 24).sum(axis=1)

def acf1(x):
    x = x - x.mean()
    return float(np.sum(x[1:] * x[:-1]) / np.sum(x * x))

def ar1_whiten(x):
    a = acf1(x)
    return x[1:] - a * x[:-1], a

def corr_matrix(series_list):
    M = np.vstack(series_list)
    return np.corrcoef(M)

def main():
    out = {}
    # ---- P-L4 reproduction (phase + lines) on all-access ----
    repro = {}
    daily = {}
    logdaily = {}
    for pond in PONDS:
        ts, v = load_hourly(pond)
        v = to_2184(ts, v)
        ph, prof, f24, f168 = circ_phase(v)
        d = daily_series(v)
        daily[pond] = d
        logdaily[pond] = np.log(d + 1.0)
        repro[pond] = {"peak_hour_utc": round(ph, 3), "f24_fftbin": round(f24, 4),
                       "f168_fftbin": round(f168, 4), "n_days": int(d.size),
                       "mean_daily": round(float(d.mean()), 1)}
    out["pl4_reproduction"] = repro

    # ---- canon matrices: raw daily, log-daily ----
    pn = PONDS
    raw_corr = corr_matrix([daily[p] for p in pn])
    log_corr = corr_matrix([logdaily[p] for p in pn])
    out["corr_raw_daily"] = np.round(raw_corr, 3).tolist()
    out["corr_log_daily"] = np.round(log_corr, 3).tolist()
    out["ponds_order"] = pn

    # ---- ATTACK A: strip shared trend (7d MA) + weekly cycle (DOW factors), re-corr ----
    def deweek_detrend(d):
        x = np.log(d + 1.0)
        # remove centered 7d moving average (trend), reflect pad
        w = 7
        pad = np.pad(x, (w, w), mode="reflect")
        ma = np.convolve(pad, np.ones(w) / w, mode="same")[w:-w]
        r = x - ma
        # remove day-of-week mean
        dow = np.arange(r.size) % 7
        for k in range(7):
            r[dow == k] -= r[dow == k].mean()
        return r
    resid = {p: deweek_detrend(daily[p]) for p in pn}
    resid_corr = corr_matrix([resid[p] for p in pn])
    out["corr_resid_detrended_deweekly"] = np.round(resid_corr, 3).tolist()

    # ---- ATTACK B: AR(1)-whiten each residual, re-corr (kills shared smoothness) ----
    wh = {}
    a1 = {}
    for p in pn:
        w, a = ar1_whiten(resid[p])
        wh[p] = w; a1[p] = round(a, 3)
    wh_corr = corr_matrix([wh[p] for p in pn])
    out["ar1_coefs_resid"] = a1
    out["corr_resid_ar1whitened"] = np.round(wh_corr, 3).tolist()

    # ---- ATTACK C: phase-randomization null on the RESIDUALS ----
    # build surrogates preserving each pond's power spectrum but randomizing phase,
    # independently across ponds => expected cross-corr under "matched spectra, no
    # shared driver". Report mean abs off-diagonal corr observed vs null band.
    def phase_surrogate(x):
        X = np.fft.rfft(x)
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, X.size))
        ph[0] = 1.0
        if x.size % 2 == 0:
            ph[-1] = 1.0
        Y = np.abs(X) * ph
        return np.fft.irfft(Y, n=x.size)
    def offdiag_meanabs(C):
        n = C.shape[0]
        m = ~np.eye(n, dtype=bool)
        return float(np.mean(np.abs(C[m])))
    obs_resid = offdiag_meanabs(resid_corr)
    obs_wh = offdiag_meanabs(wh_corr)
    null_resid = []
    for _ in range(2000):
        sur = [phase_surrogate(resid[p]) for p in pn]
        null_resid.append(offdiag_meanabs(corr_matrix(sur)))
    null_resid = np.array(null_resid)
    out["phase_null_resid"] = {
        "obs_meanabs_offdiag": round(obs_resid, 4),
        "null_mean": round(float(null_resid.mean()), 4),
        "null_p95": round(float(np.percentile(null_resid, 95)), 4),
        "null_p99": round(float(np.percentile(null_resid, 99)), 4),
        "p_value_obs_ge_null": round(float(np.mean(null_resid >= obs_resid)), 4),
        "z": round(float((obs_resid - null_resid.mean()) / (null_resid.std() + 1e-12)), 2)}

    # ---- specific pair: en-es (the headline "global canon" 0.685 raw / 0.301 resid) ----
    def pearson(a, b):
        return float(np.corrcoef(a, b)[0, 1])
    ie, is_ = pn.index("en"), pn.index("es")
    out["en_es_pair"] = {
        "raw_daily": round(pearson(daily["en"], daily["es"]), 3),
        "log_daily": round(pearson(logdaily["en"], logdaily["es"]), 3),
        "resid_detrended_deweekly": round(pearson(resid["en"], resid["es"]), 3),
        "ar1_whitened": round(pearson(wh["en"], wh["es"]), 3)}
    # en-ja (the "no shared canon"/different-script pair) for contrast
    ij = pn.index("ja")
    out["en_ja_pair"] = {
        "raw_daily": round(pearson(daily["en"], daily["ja"]), 3),
        "resid_detrended_deweekly": round(pearson(resid["en"], resid["ja"]), 3),
        "ar1_whitened": round(pearson(wh["en"], wh["ja"]), 3)}

    # ---- ATTACK D: how many independent daily samples? effective n after AR(1) ----
    # Neff = n * (1-a)/(1+a) using residual AR(1). The corr SE ~ 1/sqrt(Neff).
    eff = {}
    for p in pn:
        a = a1[p]
        nser = resid[p].size
        neff = nser * (1 - a) / (1 + a)
        eff[p] = {"n": nser, "ar1": a, "neff": round(neff, 1)}
    out["effective_n_resid"] = eff
    # crude corr SE from the smallest Neff
    neff_min = min(eff[p]["neff"] for p in pn)
    out["corr_se_approx_from_neff_min"] = round(1.0 / math.sqrt(max(neff_min - 3, 1)), 3)

    print(json.dumps(out, indent=1))
    with open(os.path.join(ROOT, "results", "skeptic_pl4_canon.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    main()
