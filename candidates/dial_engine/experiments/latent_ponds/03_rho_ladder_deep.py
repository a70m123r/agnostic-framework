"""
Deep rho ladder for en.wikipedia:
- hourly rho at lags 1,2,3,...,24,48,72,168,336 hours
- explains the 6h anomaly (does rho really collapse at 6h spacing?)
- daily series rho ladder
- also: hourly profile plots (numerical, no matplotlib)
"""

import json
import numpy as np
import math
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
START = "2026030100"
END   = "2026060123"


def load_hourly(lang: str) -> np.ndarray:
    path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    with open(path) as f:
        items = json.load(f)
    return np.array([x["views"] for x in items], dtype=float)


def autocorr(x: np.ndarray, lag: int) -> float:
    n = len(x)
    if lag >= n:
        return float("nan")
    x0 = x[:n - lag] - x[:n - lag].mean()
    x1 = x[lag:] - x[lag:].mean()
    denom = np.sqrt(np.sum(x0**2) * np.sum(x1**2))
    if denom == 0:
        return float("nan")
    return float(np.sum(x0 * x1) / denom)


def sigma_shrink_identity(rho: float) -> float:
    if rho >= 1.0:
        return float("inf")
    val = 2 * (1 - rho)
    if val <= 0:
        return float("inf")
    return -0.5 * math.log2(val)


x_en = load_hourly("en")
print(f"en.wikipedia hourly series: n={len(x_en)}")
print()

# ── full rho ladder hourly lags 1..36, then key large lags ────────────────
print("Rho ladder: hourly lags 1-36 + key large lags")
print(f"{'lag_h':>8s} {'rho':>10s} {'shrink':>10s}  interpretation")
key_lags = list(range(1, 37)) + [48, 72, 96, 120, 144, 168, 192, 216, 240, 336]
for lag in key_lags:
    rho = autocorr(x_en, lag)
    if math.isnan(rho):
        print(f"{lag:>8d} {'NaN':>10s}")
        continue
    sid = sigma_shrink_identity(rho)
    note = ""
    if lag == 24:  note = " <- circadian"
    elif lag == 168: note = " <- weekly"
    elif lag == 6: note = " <- 6h (check!)"
    print(f"{lag:>8d} {rho:>10.4f} {sid:>10.4f} {note}")

# ── Explain why 6h decimated rho is 0.024 ────────────────────────────────
print()
print("Explanation of 6h decimated series rho1:")
print("  Decimated 6h: take every 6th sample from hourly series")
print("  This is equivalent to autocorr at lag=6 of the original series.")
lag6_rho = autocorr(x_en, 6)
print(f"  autocorr(hourly, lag=6) = {lag6_rho:.4f}")
print()
print("  Why does this happen? The 24h circadian cycle creates:")
print("  a trough at lag 6h (quarter-period = anti-phase).")
print("  The 24h period means:")
for lag in [6, 12, 18, 24]:
    rho = autocorr(x_en, lag)
    frac = lag / 24.0
    print(f"    lag={lag:3d}h ({frac:.2f} x 24h cycle) -> rho={rho:.4f}")

# ── 24h mean profile for all 5 languages (numerical bar chart) ────────────
print()
print("=" * 70)
print("Hourly profile (24h mean) — all languages")
print("Normalized: each hour divided by mean. Shows shape, not scale.")
print()

LANGUAGES = ["en", "ja", "de", "ar", "es"]
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

    print(f"  {lang}  (peak={np.argmax(profile):02d}:00 UTC, "
          f"trough={np.argmin(profile):02d}:00 UTC, "
          f"peak/mean={norm[np.argmax(profile)]:.3f})")
    # ASCII sparkline
    bar_chars = " ▁▂▃▄▅▆▇█"
    min_v, max_v = norm.min(), norm.max()
    line = ""
    for v in norm:
        idx = int((v - min_v) / (max_v - min_v) * 8)
        line += bar_chars[idx]
    print(f"  h:  " + "".join(f"{h:2d}" for h in range(24)))
    print(f"  v:  {line}")
    print(f"  vals: " + " ".join(f"{v:.2f}" for v in norm))
    print()

# ── rho at 24h lag for all 5 languages ────────────────────────────────────
print()
print("Autocorrelation at 24h and 168h for all languages:")
print(f"  {'lang':>4s} {'rho@24h':>10s} {'shrink@24h':>12s} "
      f"{'rho@168h':>10s} {'shrink@168h':>12s}")
for lang in LANGUAGES:
    x = load_hourly(lang)
    r24  = autocorr(x, 24)
    r168 = autocorr(x, 168)
    s24  = sigma_shrink_identity(r24)
    s168 = sigma_shrink_identity(r168)
    print(f"  {lang:>4s} {r24:>10.4f} {s24:>12.4f} {r168:>10.4f} {s168:>12.4f}")

# ── Weekly rho rhythm in the autocorrelation ladder ───────────────────────
print()
print("Weekly rhythm in rho: lags multiples of 24h, 1-7 days")
print("Shows whether the weekly pattern dominates or the 24h cycle")
print(f"  {'lang':>4s}", end="")
for d in range(1, 8):
    print(f"  rho@{d}d", end="")
print()
for lang in LANGUAGES:
    x = load_hourly(lang)
    print(f"  {lang:>4s}", end="")
    for d in range(1, 8):
        r = autocorr(x, d * 24)
        print(f"  {r:6.4f}", end="")
    print()
