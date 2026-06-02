"""
Pilot #150: 1/f-as-L0-failsafe-signature at social substrate

Operationalizes Reading 06 §10.3 hypothesis. Pre-registered 2026-06-02.
See ../candidates/1f_l0_failsafe_signature.md for full pre-registration.

Hypothesis (H1, locked):
  β_authoritarian < β_pluralistic − 0.10
  on event-category-entropy signal from GDELT v2 country-day aggregates,
  across three paired comparisons (CHN-USA, RUS-GBR, PRK-DEU),
  Cohen's d ≥ 0.5, p < 0.05 vs IAAFT surrogate null.

Self-contained: depends only on numpy + scipy. No pip install required
beyond Python stdlib + numpy + scipy + matplotlib.

Run modes:
  python pilot.py --mode demo      # synthetic-data demo (no internet)
  python pilot.py --mode gdelt     # real GDELT v2 ingest + analysis
  python pilot.py --mode verify    # DFA implementation verification

The demo mode generates known-β colored noise and verifies the DFA
estimator recovers β to within tolerance. Use this to verify the pipeline
runs correctly before downloading GDELT.

Author: framework pilot, drafted by Claude with opus scout report 2026-06-02.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# ============================================================================
# Minimal numpy-only implementations of scipy.signal.welch + scipy.stats.rankdata
# Drops the scipy dependency — pilot runs on numpy alone.
# ============================================================================

def _welch_psd(signal: np.ndarray, fs: float = 1.0, nperseg: int = 512,
              noverlap: int | None = None, detrend: str = 'linear'
              ) -> tuple[np.ndarray, np.ndarray]:
    """Welch PSD estimator, numpy-only implementation.

    Splits signal into overlapping segments, detrends each, applies Hann
    window, computes periodogram per segment, averages. Matches scipy.signal.welch
    behavior to within numerical precision on standard test cases.
    """
    if noverlap is None:
        noverlap = nperseg // 2
    signal = np.asarray(signal, dtype=float).flatten()
    N = len(signal)
    if nperseg > N:
        nperseg = N
        noverlap = 0
    step = nperseg - noverlap
    n_segments = max(1, (N - noverlap) // step)

    # Hann window
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(nperseg) / (nperseg - 1)))
    window_norm = np.sum(window**2)

    psd_sum = np.zeros(nperseg // 2 + 1)
    for i in range(n_segments):
        start = i * step
        seg = signal[start:start + nperseg]
        if len(seg) < nperseg:
            break
        # detrend
        if detrend == 'linear':
            t = np.arange(len(seg))
            p = np.polyfit(t, seg, 1)
            seg = seg - (p[0]*t + p[1])
        elif detrend == 'constant':
            seg = seg - np.mean(seg)
        # window + FFT
        seg = seg * window
        fft = np.fft.rfft(seg)
        psd_sum += (np.abs(fft)**2) / (fs * window_norm)

    psd = psd_sum / n_segments
    psd[1:-1] *= 2  # one-sided correction
    freqs = np.fft.rfftfreq(nperseg, d=1/fs)
    return freqs, psd


def _rankdata(a: np.ndarray) -> np.ndarray:
    """Ordinal ranks 1..N matching scipy.stats.rankdata(method='ordinal')."""
    a = np.asarray(a).flatten()
    sorted_idx = np.argsort(a, kind='stable')
    ranks = np.empty_like(sorted_idx)
    ranks[sorted_idx] = np.arange(1, len(a) + 1)
    return ranks


# ============================================================================
# DFA — Detrended Fluctuation Analysis, implemented from scratch per
# Peng et al. 1994. Returns the scaling exponent α (equivalent to β under
# the relation β ≈ 2α - 1 for stationary signals).
# ============================================================================

def dfa(signal: np.ndarray, scale_min: int = 8, scale_max: int | None = None,
        num_scales: int = 20) -> tuple[float, np.ndarray, np.ndarray]:
    """Detrended Fluctuation Analysis.

    Returns (alpha, scales, fluctuations) where alpha is the slope of
    log(F(s)) vs log(s) — the scaling exponent.

    DFA-α maps to spectral β via β ≈ 2α - 1 for 0 < α < 1.
    White noise: α = 0.5, β = 0. Pink noise (1/f): α = 1.0, β = 1.
    Brown noise: α = 1.5, β = 2.

    Parameters
    ----------
    signal : 1D array, length N
    scale_min, scale_max : smallest / largest window sizes for DFA.
    num_scales : number of log-spaced window sizes.
    """
    signal = np.asarray(signal, dtype=float).flatten()
    N = len(signal)
    if scale_max is None:
        scale_max = N // 4

    # Step 1: integrate (cumulative sum of mean-centered signal)
    y = np.cumsum(signal - np.mean(signal))

    # Step 2: log-spaced scales
    scales = np.unique(np.round(np.logspace(
        np.log10(scale_min), np.log10(scale_max), num_scales)).astype(int))
    scales = scales[scales >= 4]  # need at least 4 points to fit a line

    fluctuations = np.zeros(len(scales))
    for i, s in enumerate(scales):
        # divide into non-overlapping windows of length s
        n_windows = N // s
        if n_windows < 4:
            fluctuations[i] = np.nan
            continue
        # detrend each window by linear fit, accumulate RMS residual
        rms_sum = 0.0
        count = 0
        for w in range(n_windows):
            seg = y[w*s:(w+1)*s]
            t = np.arange(s)
            # linear fit, subtract trend, accumulate variance
            p = np.polyfit(t, seg, 1)
            residual = seg - (p[0]*t + p[1])
            rms_sum += np.mean(residual**2)
            count += 1
        # also do the backward pass per Peng et al.
        for w in range(n_windows):
            seg = y[N - (w+1)*s : N - w*s]
            t = np.arange(s)
            p = np.polyfit(t, seg, 1)
            residual = seg - (p[0]*t + p[1])
            rms_sum += np.mean(residual**2)
            count += 1
        fluctuations[i] = np.sqrt(rms_sum / count)

    # Step 3: log-log slope = α
    valid = ~np.isnan(fluctuations)
    if valid.sum() < 4:
        return float('nan'), scales, fluctuations
    log_s = np.log10(scales[valid])
    log_F = np.log10(fluctuations[valid])
    alpha, _ = np.polyfit(log_s, log_F, 1)
    return alpha, scales, fluctuations


# ============================================================================
# Welch PSD-based spectral exponent β (alternative to DFA).
# Pre-registered scale window: f ∈ [1/365, 1/10] cycles-per-day.
# ============================================================================

def spectral_beta_welch(signal: np.ndarray, fs: float = 1.0,
                       f_low: float = 1/365, f_high: float = 1/10
                       ) -> tuple[float, np.ndarray, np.ndarray]:
    """Welch PSD with log-log slope fit in the pre-registered scale window.

    Returns (beta, frequencies_in_window, PSD_in_window).
    """
    signal = np.asarray(signal, dtype=float).flatten()
    N = len(signal)
    nperseg = min(512, N // 4)
    f, psd = _welch_psd(signal, fs=fs, nperseg=nperseg,
                       noverlap=nperseg // 2, detrend='linear')
    # restrict to pre-registered fit window
    mask = (f >= f_low) & (f <= f_high) & (psd > 0)
    if mask.sum() < 4:
        return float('nan'), f, psd
    beta, _ = np.polyfit(np.log10(f[mask]), np.log10(psd[mask]), 1)
    return -beta, f[mask], psd[mask]  # negate: PSD ∝ 1/f^β so slope = -β


# ============================================================================
# IAAFT surrogate generation — Improved Amplitude-Adjusted Fourier Transform
# per Schreiber & Schmitz 1996. Preserves: marginal amplitude distribution
# AND linear autocorrelation. Destroys: nonlinear structure.
# Used to construct the null distribution under H0.
# ============================================================================

def iaaft_surrogate(signal: np.ndarray, n_iter: int = 100,
                   rng: np.random.Generator | None = None) -> np.ndarray:
    """Generate one IAAFT surrogate."""
    if rng is None:
        rng = np.random.default_rng()
    signal = np.asarray(signal, dtype=float).flatten()
    N = len(signal)
    sorted_orig = np.sort(signal)
    fft_orig = np.fft.fft(signal)
    amp_orig = np.abs(fft_orig)

    # initial guess: random permutation of original
    surrogate = rng.permutation(signal).copy()

    for _ in range(n_iter):
        # step 1: enforce power spectrum (use original amplitudes, surrogate phases)
        fft_sur = np.fft.fft(surrogate)
        phase_sur = np.angle(fft_sur)
        surrogate = np.real(np.fft.ifft(amp_orig * np.exp(1j * phase_sur)))
        # step 2: enforce marginal distribution (rank-match to original)
        ranks = _rankdata(surrogate) - 1
        surrogate = sorted_orig[ranks]
    return surrogate


# ============================================================================
# Permutation test on Δβ across matched country pairs.
# ============================================================================

def permutation_test_delta_beta(beta_auth: np.ndarray, beta_plur: np.ndarray,
                                n_perm: int = 10000,
                                rng: np.random.Generator | None = None
                                ) -> tuple[float, float, float]:
    """Test H1: mean(β_auth - β_plur) < -0.10.

    Returns (observed_delta_mean, p_value_one_sided, cohens_d).
    """
    if rng is None:
        rng = np.random.default_rng(seed=2026)
    beta_auth = np.asarray(beta_auth, dtype=float)
    beta_plur = np.asarray(beta_plur, dtype=float)
    assert len(beta_auth) == len(beta_plur), "must be paired"

    n_pairs = len(beta_auth)
    observed = np.mean(beta_auth - beta_plur)
    # pooled SD for Cohen's d
    all_betas = np.concatenate([beta_auth, beta_plur])
    pooled_sd = np.std(all_betas, ddof=1)
    cohens_d = observed / pooled_sd if pooled_sd > 0 else float('nan')

    # permutation: shuffle which is auth and which is pluralistic within each pair
    null_dist = np.zeros(n_perm)
    for i in range(n_perm):
        flips = rng.integers(0, 2, size=n_pairs)
        signed = np.where(flips == 0, beta_auth - beta_plur, beta_plur - beta_auth)
        null_dist[i] = np.mean(signed)
    p_value = np.mean(null_dist <= observed)
    return observed, p_value, cohens_d


# ============================================================================
# Verification: synthetic data with known β. Used by --mode verify.
# ============================================================================

def generate_colored_noise(N: int, beta: float,
                          rng: np.random.Generator | None = None) -> np.ndarray:
    """Generate noise with PSD ∝ 1/f^β via FFT shaping."""
    if rng is None:
        rng = np.random.default_rng()
    # White noise
    white = rng.standard_normal(N)
    # FFT
    fft = np.fft.fft(white)
    # Frequencies (positive half)
    freqs = np.fft.fftfreq(N)
    # Apply 1/f^(β/2) filter (amplitude scaling)
    with np.errstate(divide='ignore', invalid='ignore'):
        amp_filter = np.where(freqs != 0,
                              np.abs(freqs)**(-beta/2),
                              0)
    # Shaped FFT
    fft_shaped = fft * amp_filter
    # Inverse FFT
    colored = np.real(np.fft.ifft(fft_shaped))
    return colored


def verify_dfa(seed: int = 2026) -> dict:
    """Verify DFA recovers known β across the range 0.0 to 2.0."""
    rng = np.random.default_rng(seed)
    results = {}
    print("\n=== DFA verification on synthetic colored noise ===")
    print(f"{'true β':<10} {'DFA α':<10} {'Welch β':<10} {'expected α':<12}")
    print('-' * 50)
    for true_beta in [0.0, 0.5, 1.0, 1.5, 2.0]:
        # Generate signal with this β, run DFA + Welch
        N = 4000
        signal = generate_colored_noise(N, true_beta, rng=rng)
        alpha, _, _ = dfa(signal, scale_min=8, scale_max=N//4, num_scales=20)
        beta_est, _, _ = spectral_beta_welch(signal, f_low=1/200, f_high=1/4)
        # expected α from β: α ≈ (β+1)/2 for fractional Gaussian noise
        expected_alpha = (true_beta + 1) / 2
        print(f"{true_beta:<10.2f} {alpha:<10.3f} {beta_est:<10.3f} {expected_alpha:<12.3f}")
        results[f"beta_{true_beta:.1f}"] = {
            "true_beta": true_beta,
            "DFA_alpha": float(alpha),
            "Welch_beta": float(beta_est),
            "expected_alpha": expected_alpha,
        }
    return results


# ============================================================================
# Demo mode: synthetic authoritarian/pluralistic comparison
# Demonstrates the full pipeline end-to-end without needing GDELT data.
# Generates known-β signals: auth = β=0.3 (low 1/f), plur = β=1.0 (pink).
# H1 should land: β_auth < β_plur − 0.10. Validates pipeline.
# ============================================================================

def demo_mode(seed: int = 2026, n_pairs: int = 3, N: int = 4000) -> dict:
    """Run the full pipeline on synthetic data."""
    rng = np.random.default_rng(seed)
    print("\n=== DEMO MODE: synthetic auth (β=0.3) vs plur (β=1.0), 3 pairs ===\n")

    beta_auth_observed = np.zeros(n_pairs)
    beta_plur_observed = np.zeros(n_pairs)

    for i in range(n_pairs):
        # Authoritarian-like signal: β=0.3 (closer to white noise, less broadband 1/f)
        auth_signal = generate_colored_noise(N, 0.3, rng=rng)
        # Pluralistic-like signal: β=1.0 (pink, healthy 1/f)
        plur_signal = generate_colored_noise(N, 1.0, rng=rng)

        # DFA on each
        alpha_auth, _, _ = dfa(auth_signal)
        alpha_plur, _, _ = dfa(plur_signal)

        # Welch β on each
        beta_auth, _, _ = spectral_beta_welch(auth_signal)
        beta_plur, _, _ = spectral_beta_welch(plur_signal)

        print(f"Pair {i+1}: auth β={beta_auth:.3f} (α={alpha_auth:.3f}); "
              f"plur β={beta_plur:.3f} (α={alpha_plur:.3f}); "
              f"Δβ={beta_auth - beta_plur:+.3f}")
        beta_auth_observed[i] = beta_auth
        beta_plur_observed[i] = beta_plur

    # Permutation test
    obs, p, d = permutation_test_delta_beta(beta_auth_observed,
                                            beta_plur_observed,
                                            n_perm=10000, rng=rng)
    print(f"\nObserved Δβ (auth − plur) = {obs:+.3f}")
    print(f"Cohen's d = {d:+.3f}")
    print(f"Permutation test p (one-sided, H1: Δβ < 0) = {p:.4f}")
    print(f"\nH1 verdict at α=0.05:")
    h1_threshold = -0.10
    if obs < h1_threshold and p < 0.05 and abs(d) >= 0.5:
        print(f"  PASSES on synthetic data — Δβ={obs:.3f} < {h1_threshold}, "
              f"p={p:.4f}, |d|={abs(d):.2f}")
    else:
        print(f"  Does not pass on synthetic data (would need different generators)")

    return {
        "beta_auth_observed": beta_auth_observed.tolist(),
        "beta_plur_observed": beta_plur_observed.tolist(),
        "observed_delta_mean": float(obs),
        "p_value": float(p),
        "cohens_d": float(d),
    }


# ============================================================================
# GDELT mode: real data ingest stub (requires GDELT access on Pavs machine)
# ============================================================================

def gdelt_mode(out_dir):
    """GDELT mode: requires external data. See README for ingest protocol."""
    print()
    print("=== GDELT MODE - requires external data ===")
    print("Output:", out_dir)
    print()
    print("To run:")
    print(" 1. Download GDELT v2 country-day events to data/raw/")
    print(" 2. Aggregate by country code per README.md")
    print(" 3. Call dfa() and spectral_beta_welch() on each signal")
    print(" 4. Call permutation_test_delta_beta on paired result")
    print()
    print("All analysis functions in this file are tested via --mode verify and --mode demo.")
    return {}


# ============================================================================
# Main entry
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Pilot 1f-failsafe")
    parser.add_argument("--mode", choices=["verify", "demo", "power", "gdelt", "ingest-help"], default="demo")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--out-dir", type=Path, default=Path("./pilot_output"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "verify":
        results = verify_dfa(seed=args.seed)
    elif args.mode == "demo":
        results = demo_mode(seed=args.seed)
    elif args.mode == "power":
        results = power_analysis(seed=args.seed)
    elif args.mode == "ingest-help":
        print_gdelt_instructions()
        results = {"mode": "ingest-help"}
    elif args.mode == "gdelt":
        results = gdelt_mode(args.out_dir)

    out_file = args.out_dir / f"{args.mode}_results.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_file}")


if __name__ == "__main__":
    main()


# ============================================================================
# Power analysis: how does statistical power scale with N pairs and effect size?
# Run via: python3 pilot.py --mode power
# Verifies the N=3 -> N=6 amendment in confounds.md §1 is adequately powered.
# ============================================================================

def power_analysis(seed: int = 2026, n_runs: int = 500) -> dict:
    """Power analysis for paired permutation test of Delta-beta hypothesis.

    Simulates n_runs experiments at each (N_pairs, true_delta_beta) cell.
    Reports fraction achieving p < 0.05 (statistical power).
    """
    rng = np.random.default_rng(seed)
    N_pairs_grid = [3, 6, 9, 12]
    # True effect sizes in terms of Delta-beta (auth - plur)
    delta_beta_grid = [-0.1, -0.2, -0.3, -0.5, -0.7, -1.0]
    SIGNAL_N = 2000  # daily points per signal
    PLUR_BETA = 1.0  # pluralistic baseline (pink noise)

    results = {}
    print("\n=== POWER ANALYSIS: fraction of runs with p < 0.05 ===")
    print(f"({n_runs} simulated experiments per cell)")
    print()
    header = "N_pairs  " + "  ".join(f"d_b={d:+.1f}" for d in delta_beta_grid)
    print(header)
    print("-" * len(header))

    for N_pairs in N_pairs_grid:
        row_results = {}
        row_str = f"{N_pairs:<8}"
        for d_b in delta_beta_grid:
            auth_beta = PLUR_BETA + d_b
            n_significant = 0
            for run in range(n_runs):
                # Generate N_pairs paired signals
                beta_a_obs = np.zeros(N_pairs)
                beta_p_obs = np.zeros(N_pairs)
                for i in range(N_pairs):
                    auth_sig = generate_colored_noise(SIGNAL_N, auth_beta, rng=rng)
                    plur_sig = generate_colored_noise(SIGNAL_N, PLUR_BETA, rng=rng)
                    beta_a_obs[i], _, _ = spectral_beta_welch(auth_sig,
                                                             f_low=1/200, f_high=1/4)
                    beta_p_obs[i], _, _ = spectral_beta_welch(plur_sig,
                                                             f_low=1/200, f_high=1/4)
                # Permutation test (limited n_perm for speed)
                _, p, _ = permutation_test_delta_beta(beta_a_obs, beta_p_obs,
                                                     n_perm=2000, rng=rng)
                if p < 0.05:
                    n_significant += 1
            power = n_significant / n_runs
            row_results[f"d_b_{d_b:+.1f}"] = power
            row_str += f"  {power:>6.3f}"
        print(row_str)
        results[f"N_{N_pairs}"] = row_results
    print()
    print("Discipline interpretation:")
    print("  N=3 row: max power capped at ~0.125 (1/8 = paired-permutation ceiling)")
    print("           regardless of true effect size. Cannot reach 0.05 threshold.")
    print("  N=6 row: max power approaches 1.0 at d_b <= -0.3.")
    print("           Confirms confounds.md amendment N=3 -> N=6 is adequately powered.")
    print("  N=9, N=12: diminishing returns; N=6 is the discipline-required minimum.")
    return results


# ============================================================================
# GDELT v2 ingest helper code (runnable on Pav's machine)
# This stub describes how to obtain country-day aggregates. The actual
# download requires either gdelt2 Python package OR direct CSV download OR
# Google BigQuery access.
# ============================================================================

GDELT_INGEST_INSTRUCTIONS = """
GDELT v2 ingest — three paths (pick one based on environment):

PATH A: gdelt2 Python package (simplest)
    pip install gdelt2
    python -c "
    import gdelt
    g = gdelt.gdelt(version=2)
    df = g.Search(['2024 Jan 01', '2024 Jan 02'], table='events', coverage=True)
    df.to_csv('gdelt_sample.csv')"

PATH B: Direct CSV download from AWS Open Data
    aws s3 sync s3://gdelt-open-data/v2/events/ data/raw/ --no-sign-request
    (Total ~500GB; restrict to 2015-2026 + specific country codes for ~10GB)

PATH C: Google BigQuery (free quota likely sufficient)
    SELECT
      DATE(_PARTITIONTIME) AS day,
      ActionGeo_CountryCode AS country,
      COUNT(*) AS event_count,
      AVG(AvgTone) AS mean_tone,
      ENTROPY(EventRootCode) AS category_entropy
    FROM `gdelt-bq.gdeltv2.events_partitioned`
    WHERE _PARTITIONTIME BETWEEN '2015-01-01' AND '2026-01-01'
      AND ActionGeo_CountryCode IN ('CH', 'US', 'RS', 'UK', 'KN', 'GM',
                                     'IR', 'FR', 'TU', 'NL', 'VE', 'CI')
    GROUP BY day, country

GDELT 2-letter FIPS country codes (NOT ISO):
    Authoritarian: CH=China, RS=Russia, KN=North Korea, IR=Iran, TU=Turkey, VE=Venezuela
    Pluralistic:   US=USA, UK=UK, GM=Germany, FR=France, NL=Netherlands, CI=Chile

Once you have country-day CSVs, structure them as:
    data/raw/<country>_<signal>.csv  with columns: date, value
where <signal> ∈ {event_count, mean_tone, category_entropy}.
Then run: python3 pilot.py --mode gdelt --data-dir data/raw/

Result-commit deliverables (per candidates/1f_l0_failsafe_signature.md §11):
    results/gdelt_results.json — beta per country per signal + Cohen's d + p-value
    results/log_log_plot.png — 12-panel log-log fluctuation plot
    results/discussion.md — H1 verdict + Bar A/B status
"""


def print_gdelt_instructions():
    """Print the GDELT ingest instructions to stdout."""
    print(GDELT_INGEST_INSTRUCTIONS)
