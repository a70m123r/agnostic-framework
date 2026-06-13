"""
Hourly profile (24h mean) + weekly rho table — ASCII safe, no unicode bars.
"""

import json
import numpy as np
import math
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
START = "2026030100"
END   = "2026060123"
LANGUAGES = ["en", "ja", "de", "ar", "es"]

def load_hourly(lang):
    path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    with open(path) as f:
        items = json.load(f)
    return np.array([x["views"] for x in items], dtype=float)

def autocorr(x, lag):
    n = len(x)
    if lag >= n:
        return float("nan")
    x0 = x[:n-lag] - x[:n-lag].mean()
    x1 = x[lag:] - x[lag:].mean()
    denom = np.sqrt(np.sum(x0**2)*np.sum(x1**2))
    if denom == 0:
        return float("nan")
    return float(np.sum(x0*x1)/denom)

def sigma_shrink_identity(rho):
    if rho >= 1.0: return float("inf")
    val = 2*(1-rho)
    if val <= 0: return float("inf")
    return -0.5*math.log2(val)

# hourly profiles
print("Hourly profile (24h mean, normalized to mean=1.0):")
print()
profiles = {}
for lang in LANGUAGES:
    x = load_hourly(lang)
    n = len(x)
    profile = np.zeros(24)
    counts = np.zeros(24)
    for i in range(n):
        h = i % 24
        profile[h] += x[i]
        counts[h] += 1
    mask = counts > 0
    profile[mask] /= counts[mask]
    norm = profile / profile.mean()
    profiles[lang] = norm
    peak_h = int(np.argmax(profile))
    trough_h = int(np.argmin(profile))
    print(f"  {lang}  peak={peak_h:02d}h UTC  trough={trough_h:02d}h UTC  "
          f"pk/mean={norm[peak_h]:.3f}  pk/trough={norm[peak_h]/norm[trough_h]:.3f}")
    # ASCII bar: . = below mean, | = near mean, # = above mean
    bar = ""
    for v in norm:
        if v < 0.7: bar += "."
        elif v < 0.9: bar += "_"
        elif v < 1.1: bar += "-"
        elif v < 1.3: bar += "+"
        else: bar += "#"
    print(f"  h00..23: {bar}  (.=low _=below -=mean +=above #=high)")
    print(f"  vals: " + " ".join(f"{v:.3f}" for v in norm))
    print()

# Weekly rho table
print()
print("Weekly rho table (lags multiples of 24h, 1-7 days):")
print(f"  {'lang':>4s}", end="")
for d in range(1, 8):
    print(f"   d{d:1d}   ", end="")
print()
for lang in LANGUAGES:
    x = load_hourly(lang)
    print(f"  {lang:>4s}", end="")
    for d in range(1, 8):
        r = autocorr(x, d*24)
        print(f"  {r:+.4f}", end="")
    print()

# shrink_identity at day-lags
print()
print("sigma_shrink_identity at day-lags (bits) -- en only:")
print(f"  {'lag':>6s} {'rho':>8s} {'shrink':>8s}")
for lag in [24, 48, 72, 96, 120, 144, 168]:
    x = load_hourly("en")
    r = autocorr(x, lag)
    s = sigma_shrink_identity(r)
    print(f"  {lag:>4d}h  {r:>8.4f}  {s:>8.4f}")

# Circadian amplitude shrinkage over time (3-month trend)
print()
print("Circadian amplitude trend: monthly mean rho@24h for en")
x_en = load_hourly("en")
n = len(x_en)
# 3 roughly equal months: Mar (31d=744h), Apr (30d=720h), May+partial (remainder)
bounds = [(0, 744), (744, 1464), (1464, n)]
labels = ["Mar", "Apr", "May-Jun"]
for (s,e), lab in zip(bounds, labels):
    chunk = x_en[s:e]
    if len(chunk) < 48:
        continue
    r = autocorr(chunk, 24)
    # circadian amplitude from FFT
    from numpy.fft import rfft, rfftfreq
    t = np.arange(len(chunk), dtype=float)
    slope = np.polyfit(t, chunk, 1)
    xd = chunk - np.polyval(slope, t)
    w = np.hanning(len(chunk))
    xw = xd * w
    fft_vals = rfft(xw)
    power = np.abs(fft_vals)**2
    freqs = rfftfreq(len(chunk))
    target_freq = 1.0/24.0
    idx = int(np.argmin(np.abs(freqs - target_freq)))
    frac_24h = float(power[idx]/power.sum())
    print(f"  {lab}: n={len(chunk)}h  rho@24h={r:.4f}  FFT_24h_frac={frac_24h:.4f}")
