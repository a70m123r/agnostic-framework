# -*- coding: utf-8 -*-
"""Per-moment-coin angle: does the replay/simulate coin flip PER-MOMENT, not per-phenomenon?

Loads probe_data/series.npz (written by harness.py) and asks, within each
phenomenon's own NLL series (its own units, so no cross-unit trap):
  - is the orbit FLAT (every moment cheap under the law = always replayable)?
  - is the flare FLAT-THEN-EXPLOSIVE (quiet sun cheap, onsets enormously dear)?
All cross-phenomenon contrasts are DIMENSIONLESS ratios of within-series stats.
"""
import json, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
z = np.load(HERE / "probe_data" / "series.npz")
o = np.asarray(z["orbit_nll"], float)
f = np.asarray(z["flare_nll"], float)
fr = np.asarray(z["flare_resid"], float)
ft = np.asarray(z["flare_truth"], float)   # log10 flux

def stats(x):
    return dict(
        n=int(x.size),
        mean=float(x.mean()), std=float(x.std()),
        p50=float(np.percentile(x, 50)),
        p99=float(np.percentile(x, 99)),
        max=float(x.max()),
        max_over_mean=float(x.max() / x.mean()),
        p99_over_p50=float(np.percentile(x, 99) / np.percentile(x, 50)),
        cv=float(x.std() / x.mean()),
        z_max=float((x.max() - x.mean()) / x.std()),
        top1pct_bit_share=float(np.sort(x)[-max(1, int(round(0.01 * x.size))):].sum() / x.sum()),
    )

so, sf = stats(o), stats(f)

# ---- flare onsets: NLL > mean + 5*std ------------------------------------
mu, sd = f.mean(), f.std()
thr = mu + 5.0 * sd
onset_idx = np.where(f > thr)[0]

# robustness sibling: MAD-based threshold (spikes inflate std -> mean+5*std is conservative)
med = np.median(f)
mad_sigma = 1.4826 * np.median(np.abs(f - med))
thr_mad = med + 5.0 * mad_sigma
onset_idx_mad = np.where(f > thr_mad)[0]

# group contiguous onsets (gap <= 10 steps = 10 min) into events
def group(idx, gap=10):
    ev = []
    if idx.size:
        start = prev = int(idx[0])
        for i in idx[1:]:
            i = int(i)
            if i - prev <= gap:
                prev = i
            else:
                ev.append((start, prev)); start = prev = i
        ev.append((start, prev))
    return ev

events = group(onset_idx)

quiet_mask = np.ones(f.size, bool); quiet_mask[onset_idx] = False
quiet = f[quiet_mask]

# ---- time tags for onsets (replicate harness parsing exactly) -------------
rows = json.loads((HERE / "probe_data" / "goes_xray_7day.json").read_text(encoding="utf-8"))
long = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
long.sort(key=lambda r: r["time_tag"])
flux_chk = np.clip(np.array([r["flux"] for r in long], float), 1e-9, None)
flux_chk = flux_chk[np.isfinite(flux_chk)]
time_ok = (len(flux_chk) == len(long) == f.size)
tags = [r["time_tag"] for r in long] if time_ok else None

def goes_class(fx):
    return "X" if fx >= 1e-4 else "M" if fx >= 1e-5 else "C" if fx >= 1e-6 else "B/A"

onset_detail = []
for i in onset_idx:
    i = int(i)
    onset_detail.append(dict(
        idx=i,
        time=tags[i] if time_ok else None,
        nll_bits=round(float(f[i]), 2),
        z=round(float((f[i] - mu) / sd), 1),
        dlogflux_dex=round(float(fr[i]), 4),       # +ve = brightening step
        flux_Wm2=float(10.0 ** ft[i]),
        goes_class=goes_class(10.0 ** ft[i]),
        p_solomonoff=float(2.0 ** -float(f[i])),   # p = 2^-bits at this moment
    ))
onset_detail.sort(key=lambda d: -d["nll_bits"])

event_detail = []
for (a, b) in events:
    seg = f[a:b + 1]
    pk = a + int(np.argmax(seg))
    event_detail.append(dict(
        start_idx=a, end_idx=b, dur_steps=b - a + 1,
        start_time=tags[a] if time_ok else None,
        peak_nll_bits=round(float(f[pk]), 2),
        peak_flux_Wm2=float(10.0 ** ft[pk]),
        goes_class=goes_class(10.0 ** ft[pk]),
        sign=("brightening" if fr[pk] > 0 else "decay"),
    ))

# ---- orbit: same 5-sigma per-moment rule ----------------------------------
omu, osd = o.mean(), o.std()
orbit_exceed = np.where(o > omu + 5.0 * osd)[0]
# orbit is smooth, not iid -- characterize ramp vs spikes via quarter means
q = np.array_split(o, 4)
orbit_quarter_means = [round(float(s.mean()), 2) for s in q]

out = dict(
    orbit_nll=so,
    flare_nll=sf,
    flare_onsets=dict(
        rule="flare_nll > mean + 5*std",
        threshold_bits=round(float(thr), 2),
        count=int(onset_idx.size),
        frac_of_steps=float(onset_idx.size / f.size),
        events=len(events),
        event_detail=event_detail,
        min_onset_bits=round(float(f[onset_idx].min()), 2) if onset_idx.size else None,
        max_onset_bits=round(float(f[onset_idx].max()), 2) if onset_idx.size else None,
        onset_bits_share_of_total=float(f[onset_idx].sum() / f.sum()) if onset_idx.size else 0.0,
        top12=onset_detail[:12],
        mad_sibling=dict(threshold_bits=round(float(thr_mad), 2), count=int(onset_idx_mad.size),
                         frac_of_steps=float(onset_idx_mad.size / f.size)),
    ),
    flare_quiet=dict(
        n=int(quiet.size),
        frac_of_steps=float(quiet.size / f.size),
        mean=round(float(quiet.mean()), 3),
        p50=round(float(np.percentile(quiet, 50)), 3),
        p99=round(float(np.percentile(quiet, 99)), 3),
        p999=round(float(np.percentile(quiet, 99.9)), 3),
        max=round(float(quiet.max()), 2),
        max_over_mean=round(float(quiet.max() / quiet.mean()), 2),
        p_solomonoff_at_p50=float(2.0 ** -np.percentile(quiet, 50)),
    ),
    orbit_5sigma=dict(rule="orbit_nll > mean + 5*std",
                      threshold_bits=round(float(omu + 5 * osd), 2),
                      count=int(orbit_exceed.size),
                      z_max=round(float((o.max() - omu) / osd), 2),
                      quarter_means_bits=orbit_quarter_means),
    contrast_dimensionless=dict(
        orbit_max_over_mean=round(so["max_over_mean"], 3),
        flare_max_over_mean=round(sf["max_over_mean"], 2),
        ratio_max_over_mean=round(sf["max_over_mean"] / so["max_over_mean"], 1),
        orbit_p99_over_p50=round(so["p99_over_p50"], 3),
        flare_p99_over_p50=round(sf["p99_over_p50"], 3),
        ratio_p99_over_p50=round(sf["p99_over_p50"] / so["p99_over_p50"], 2),
        orbit_cv=round(so["cv"], 4),
        flare_cv=round(sf["cv"], 4),
        ratio_cv=round(sf["cv"] / so["cv"], 1),
        orbit_top1pct_bit_share=round(so["top1pct_bit_share"], 4),
        flare_top1pct_bit_share=round(sf["top1pct_bit_share"], 4),
        onset_max_vs_quiet_p50=round(float(f[onset_idx].max() / np.percentile(quiet, 50)), 1) if onset_idx.size else None,
    ),
)
print(json.dumps(out, indent=2))
