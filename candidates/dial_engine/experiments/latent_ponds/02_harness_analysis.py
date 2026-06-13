"""
P-L4 harness-signature probe — Step 2: full analysis
(a) 24h and 168h spectral line strength per language (FFT + autocorrelation)
(b) Circadian phase offset in UTC per language (peak hour)
(c) Canon-radius: daily cross-correlation matrix (5x5) + time-varying windows
(d) Q6 rung instrument on en.wikipedia: persistence comp-ratio + rho1 identity
    at rungs 1h/6h/24h/168h
All numbers from real fetched data; no fabrication.
"""

import json
import math
import numpy as np
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
RESULTS_DIR = Path(__file__).parent
LANGUAGES = ["en", "ja", "de", "ar", "es"]
START = "2026030100"
END   = "2026060123"


# ── helpers ──────────────────────────────────────────────────────────────────

def load_hourly(lang: str) -> np.ndarray:
    path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    with open(path) as f:
        items = json.load(f)
    return np.array([x["views"] for x in items], dtype=float)


def timestamps(lang: str):
    path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    with open(path) as f:
        items = json.load(f)
    return [x["timestamp"] for x in items]


def autocorr(x: np.ndarray, lag: int) -> float:
    """Pearson autocorrelation at given lag."""
    n = len(x)
    if lag >= n:
        return float("nan")
    x0 = x[:n - lag] - x[:n - lag].mean()
    x1 = x[lag:] - x[lag:].mean()
    denom = np.sqrt(np.sum(x0**2) * np.sum(x1**2))
    if denom == 0:
        return float("nan")
    return float(np.sum(x0 * x1) / denom)


def fft_power_at_freq(x: np.ndarray, period_hours: float) -> float:
    """
    FFT power fraction at the spectral line closest to 1/period_hours.
    Returns (power at that bin) / (total power) — a dimensionless fraction.
    """
    n = len(x)
    # detrend: subtract linear trend to avoid DC-leak
    t = np.arange(n, dtype=float)
    slope = np.polyfit(t, x, 1)
    xd = x - np.polyval(slope, t)
    # Hann window to reduce spectral leakage
    w = np.hanning(n)
    xw = xd * w
    fft_vals = np.fft.rfft(xw)
    power = np.abs(fft_vals)**2
    freqs = np.fft.rfftfreq(n)   # cycles per sample (1 sample = 1 hour)
    target_freq = 1.0 / period_hours
    idx = int(np.argmin(np.abs(freqs - target_freq)))
    # Report the bin power / total power (fraction in that line)
    total = power.sum()
    if total == 0:
        return float("nan")
    return float(power[idx] / total)


def circadian_phase(x: np.ndarray) -> dict:
    """
    Compute the mean hour-of-day (UTC) profile and find the peak hour.
    Also returns the trough hour and the peak/trough ratio.
    x is an hourly series starting at hour 0 of the first day.
    """
    n = len(x)
    # hour_of_day for each sample (index mod 24, offset by the first hour)
    # timestamps start at 2026030100 => hour 0 UTC on day 0
    hours = np.arange(n) % 24
    profile = np.zeros(24)
    counts = np.zeros(24)
    for i in range(n):
        h = int(hours[i])
        profile[h] += x[i]
        counts[h] += 1
    mask = counts > 0
    profile[mask] /= counts[mask]
    peak_hour = int(np.argmax(profile))
    trough_hour = int(np.argmin(profile))
    peak_val = float(profile[peak_hour])
    trough_val = float(profile[trough_hour])
    ratio = peak_val / trough_val if trough_val > 0 else float("nan")
    return {
        "profile": profile.tolist(),
        "peak_hour_utc": peak_hour,
        "trough_hour_utc": trough_hour,
        "peak_over_trough": ratio,
    }


def pearson_r(a: np.ndarray, b: np.ndarray) -> float:
    a0 = a - a.mean()
    b0 = b - b.mean()
    denom = np.sqrt(np.sum(a0**2) * np.sum(b0**2))
    if denom == 0:
        return float("nan")
    return float(np.dot(a0, b0) / denom)


# ── SECTION A: spectral line strengths ───────────────────────────────────────

print("=" * 70)
print("SECTION A — spectral line strength: 24h and 168h per language")
print("=" * 70)

spec_results = {}
for lang in LANGUAGES:
    x = load_hourly(lang)
    p24  = fft_power_at_freq(x, 24.0)
    p168 = fft_power_at_freq(x, 168.0)
    ac24  = autocorr(x, 24)
    ac168 = autocorr(x, 168)
    spec_results[lang] = {
        "fft_frac_24h":  p24,
        "fft_frac_168h": p168,
        "ac_24h":        ac24,
        "ac_168h":       ac168,
    }
    print(f"  {lang:2s}  FFT@24h={p24:.4f}  FFT@168h={p168:.4f}  "
          f"AC@24h={ac24:.4f}  AC@168h={ac168:.4f}")


# ── SECTION B: circadian phase per language ───────────────────────────────────

print()
print("=" * 70)
print("SECTION B — circadian phase (UTC) per language")
print("=" * 70)

phase_results = {}
for lang in LANGUAGES:
    x = load_hourly(lang)
    cp = circadian_phase(x)
    phase_results[lang] = cp
    print(f"  {lang:2s}  peak_hour_UTC={cp['peak_hour_utc']:02d}:00  "
          f"trough_UTC={cp['trough_hour_utc']:02d}:00  "
          f"peak/trough={cp['peak_over_trough']:.3f}")

# Phase offsets relative to en
en_peak = phase_results["en"]["peak_hour_utc"]
print(f"\n  Phase offsets vs en (peak={en_peak:02d}:00 UTC):")
for lang in LANGUAGES:
    offset = (phase_results[lang]["peak_hour_utc"] - en_peak) % 24
    if offset > 12:
        offset -= 24
    print(f"    {lang:2s}: {'+' if offset >= 0 else ''}{offset:+d}h")


# ── SECTION C: daily cross-correlation matrix ─────────────────────────────────

print()
print("=" * 70)
print("SECTION C — daily cross-correlation matrix (5x5)")
print("=" * 70)

# Aggregate hourly -> daily for correlation (reduces noise, 93 days)
daily = {}
for lang in LANGUAGES:
    x = load_hourly(lang)
    n_days = len(x) // 24
    daily[lang] = np.array([x[i*24:(i+1)*24].sum() for i in range(n_days)], dtype=float)

print(f"  Daily series: {n_days} days per language\n")
print(f"  {'':4s}", end="")
for lang in LANGUAGES:
    print(f"{lang:>8s}", end="")
print()

corr_matrix = {}
for la in LANGUAGES:
    print(f"  {la:4s}", end="")
    corr_matrix[la] = {}
    for lb in LANGUAGES:
        r = pearson_r(daily[la], daily[lb])
        corr_matrix[la][lb] = r
        print(f"{r:8.4f}", end="")
    print()

# Co-movement pairs (r > 0.7, excluding self)
print("\n  Strong co-movement pairs (r > 0.70, off-diagonal):")
for la in LANGUAGES:
    for lb in LANGUAGES:
        if la < lb:
            r = corr_matrix[la][lb]
            if r > 0.70:
                print(f"    {la}-{lb}: r={r:.4f}")

# Weakest pairs
print("\n  Weakest pairs (off-diagonal):")
pairs = [(la, lb, corr_matrix[la][lb]) for la in LANGUAGES for lb in LANGUAGES if la < lb]
pairs.sort(key=lambda t: t[2])
for la, lb, r in pairs[:3]:
    print(f"    {la}-{lb}: r={r:.4f}")

# Rolling 14-day cross-correlation: en vs each other (capturing drift)
print("\n  Rolling 14-day Pearson r (en vs others):")
print(f"  {'window_start_day':20s}", end="")
for lang in LANGUAGES[1:]:
    print(f" {'en-'+lang:>10s}", end="")
print()

window = 14
n_days_d = len(daily["en"])
step = 7
rows_printed = 0
for start_day in range(0, n_days_d - window + 1, step):
    end_day = start_day + window
    print(f"  days {start_day:02d}-{end_day:02d}              ", end="")
    for lang in LANGUAGES[1:]:
        r = pearson_r(daily["en"][start_day:end_day], daily[lang][start_day:end_day])
        print(f"{r:10.4f}", end="")
    print()
    rows_printed += 1


# ── SECTION D: Q6 rung instrument on en.wikipedia ────────────────────────────

print()
print("=" * 70)
print("SECTION D — Q6 rung instrument on en.wikipedia")
print("  persistence law, comp-ratio, rho1, rho1 identity")
print("  rungs: 1h, 6h, 24h, 168h")
print("=" * 70)

import lzma

def compress_bytes(b: bytes) -> int:
    return len(lzma.compress(b, preset=9))

def series_to_bytes(arr: np.ndarray) -> bytes:
    """Quantize float series to int (log10 * 1000) -> little-endian int32 bytes."""
    # Use log10 of views (positive, > 0 guaranteed for Wikipedia)
    log_arr = np.log10(arr)
    quantized = np.round(log_arr * 1000).astype(np.int32)
    return quantized.tobytes()

def rho1(arr: np.ndarray) -> float:
    return autocorr(arr, 1)

def sigma_shrink_identity(rho: float) -> float:
    """
    From Q6: per-dim sigma-shrink = -0.5 * log2(2*(1-rho1))
    for the first-difference (persistence) law.
    """
    if rho >= 1.0:
        return float("inf")
    val = 2 * (1 - rho)
    if val <= 0:
        return float("inf")
    return -0.5 * math.log2(val)

# Load en hourly
x_en = load_hourly("en")
print(f"\n  en.wikipedia: n={len(x_en)} hourly samples")
print(f"  Model: persistence f_hat(t) = f(t-1) (log10 scale)")
print(f"  Coder: lzma-9 on quantized int32 (log10*1000)")
print(f"  Rho identity: shrink = -0.5*log2(2*(1-rho1))\n")

print(f"  {'rung':>8s} {'n':>6s} {'raw_CR':>8s} {'resid_CR':>8s} "
      f"{'rho1':>8s} {'shrink_id':>10s} {'shrink_comp':>12s}")
print("  " + "-" * 72)

# MODEL BITS: the persistence model itself costs 64 bits (1 float64 = the prior sample value)
MODEL_BITS = 64

rung_hours = [1, 6, 24, 168]
rung_results = {}

for rung in rung_hours:
    # Decimate (every rung-th sample) — same as Q6 committed instrument
    x_dec = x_en[::rung]
    n = len(x_dec)

    # raw bytes and comp
    raw_bytes = series_to_bytes(x_dec)
    raw_bits = 8 * compress_bytes(raw_bytes)

    # residuals: resid[t] = log10(x[t]) - log10(x[t-1])  for t >= 1
    log_dec = np.log10(x_dec)
    resid = np.diff(log_dec)
    resid_bytes = series_to_bytes(np.exp(resid))  # quantize resid similarly
    # Actually quantize residuals directly
    resid_q = np.round(resid * 1000).astype(np.int32)
    resid_bytes2 = resid_q.tobytes()
    resid_bits = 8 * compress_bytes(resid_bytes2) + MODEL_BITS

    comp_raw = raw_bits / (8 * len(raw_bytes))
    comp_resid = resid_bits / (8 * len(raw_bytes))

    rho = rho1(x_dec)
    shrink_identity = sigma_shrink_identity(rho)

    # empirical sigma-shrink: log2(std_raw / std_resid_in_same_units)
    log_arr = np.log10(x_dec)
    std_raw = float(np.std(np.diff(log_arr * 0 + log_arr)))  # std of log series
    # Actually: shrink = log2(sigma_raw / sigma_resid) where sigma measured on log differences
    diff_log = np.diff(log_dec)
    sigma_raw_log = float(np.std(log_dec))
    sigma_resid_log = float(np.std(diff_log))
    shrink_comp_empirical = float(np.log2(sigma_raw_log / sigma_resid_log)) if sigma_resid_log > 0 else float("nan")

    raw_cr = raw_bits / (len(raw_bytes) * 8)
    resid_cr = resid_bits / (len(raw_bytes) * 8)

    rung_results[rung] = {
        "n": n,
        "rho1": rho,
        "raw_CR": raw_cr,
        "resid_CR": resid_cr,
        "shrink_identity": shrink_identity,
        "shrink_empirical": shrink_comp_empirical,
    }

    print(f"  {rung:>6d}h {n:>6d} {raw_cr:>8.4f} {resid_cr:>8.4f} "
          f"{rho:>8.4f} {shrink_identity:>10.4f} {shrink_comp_empirical:>12.4f}")

# Rho1 identity check (like Q6's RMS check)
print("\n  Identity check (rho1 -> shrink_id vs empirical shrink):")
errors = []
for rung in rung_hours:
    r = rung_results[rung]
    err = abs(r["shrink_identity"] - r["shrink_empirical"])
    errors.append(err)
    print(f"    rung={rung:3d}h  identity={r['shrink_identity']:.4f}  "
          f"empirical={r['shrink_empirical']:.4f}  |diff|={err:.4f}")
print(f"  RMS identity error: {math.sqrt(sum(e**2 for e in errors)/len(errors)):.4f} bits")

# Dial placement: compare to Q6 committed flare rho1 values
print("\n  Dial placement (rho1): en.wikipedia vs Q6 committed flare")
print(f"  {'rung_proxy':>14s} {'en.wiki':>10s} {'flare_Q6':>10s}")
# Q6 rho1 at 1min/2min/5min/10min/30min/60min: 0.996/0.986/0.946/0.885/0.734/0.484
# For comparison map: 1h wiki ~ 60-min flare; 6h~360min; 24h~1440min; 168h~10080min
flare_ref = {1: 0.484, 6: None, 24: None, 168: None}  # only 60-min has direct data
# We can extrapolate using the fitted multi-timescale decay from Q6
# The Q6 paper notes rho at 60min=0.484; at longer lags it doesn't decay to 0 (slow trend)
# Let's just report wiki values and note the comparison
for rung in rung_hours:
    rho = rung_results[rung]["rho1"]
    flare_note = f"{flare_ref[rung]}" if flare_ref[rung] is not None else "n/a (beyond Q6 window)"
    print(f"  {rung:3d}h ({rung*60:5d} min)  rho1={rho:.4f}  flare_60min={flare_note}")

print("\n  Note: Q6 flare rho1 at rung 1min=0.996, 60min=0.484 (the edge=0 crossover)")
print("  Wikipedia en at 1h rung is the 'coarse' entry point of the wiki series.")


# ── SECTION E: weekly autocorr at longer lags ────────────────────────────────

print()
print("=" * 70)
print("SECTION E — autocorrelation ladder (en) at 24h/48h/72h/96h/120h/144h/168h")
print("  = tidal calendar imprint, days 1-7")
print("=" * 70)

x_en = load_hourly("en")
lags_h = [24, 48, 72, 96, 120, 144, 168]
print(f"\n  {'lag_h':>8s} {'lag_days':>10s} {'rho':>10s} {'shrink_id':>12s}")
for lag in lags_h:
    rho = autocorr(x_en, lag)
    sid  = sigma_shrink_identity(rho) if rho < 1 else float("inf")
    print(f"  {lag:>8d} {lag//24:>10d}d  {rho:>10.4f} {sid:>12.4f}")


# ── SECTION F: rho1 at 1h rung for all 5 languages ────────────────────────────

print()
print("=" * 70)
print("SECTION F — rho1 at 1h rung + spectral amplitudes, all 5 languages")
print("=" * 70)

print(f"\n  {'lang':>4s} {'rho1@1h':>10s} {'shrink_id':>10s} {'FFT@24h%':>10s} {'FFT@168h%':>11s} {'AC@24h':>8s} {'AC@168h':>9s}")
for lang in LANGUAGES:
    x = load_hourly(lang)
    r1 = rho1(x)
    sid = sigma_shrink_identity(r1)
    p24 = spec_results[lang]["fft_frac_24h"] * 100
    p168 = spec_results[lang]["fft_frac_168h"] * 100
    ac24 = spec_results[lang]["ac_24h"]
    ac168 = spec_results[lang]["ac_168h"]
    print(f"  {lang:>4s} {r1:>10.4f} {sid:>10.4f} {p24:>9.4f}% {p168:>10.4f}% {ac24:>8.4f} {ac168:>9.4f}")


# ── Save results ───────────────────────────────────────────────────────────────

results = {
    "spectral": spec_results,
    "phase": {lang: {k: v for k, v in phase_results[lang].items() if k != "profile"}
              for lang in LANGUAGES},
    "corr_matrix": corr_matrix,
    "rung_instrument": rung_results,
}

out_path = RESULTS_DIR / "results.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n\nResults saved to {out_path}")
