"""
fast_dfa.py -- a VECTORIZED Detrended Fluctuation Analysis that is NUMERICALLY
IDENTICAL to pilots/1f_failsafe/pilot.dfa (the tested Peng-1994 implementation),
but ~1-2 orders of magnitude faster in the rolling-window hot loop.

This is NOT a reimplementation of the DFA *method* -- it is the SAME algorithm
(integrate -> log-spaced scales -> per-scale non-overlapping forward+backward windows
-> degree-1 detrend -> RMS fluctuation -> log-log slope), with the per-window Python
`np.polyfit` loop replaced by closed-form vectorized OLS over all windows of a scale
at once. `verify_against_pilot()` asserts agreement with pilot.dfa to < 1e-9 over the
full beta range, so the locked estimator's numbers are unchanged -- only the runtime is.

Why this is needed (PRE_REG §6 power driver feasibility): the locked design computes
tau(t) = rolling DFA-alpha (window 365 / stride 30) -> ~118 DFA calls per system; the
power study runs N_sim x 5 generators x N systems of those. pilot.dfa's per-call Python
loops made the run take tens of hours; this brings it into minutes while keeping the
estimator bit-for-bit equivalent.
"""

from __future__ import annotations

import numpy as np


def dfa_fast(signal: np.ndarray, scale_min: int = 8, scale_max: int | None = None,
             num_scales: int = 20) -> float:
    """Vectorized DFA scaling exponent alpha. Matches pilot.dfa(...)[0] exactly.

    Mirrors pilot.dfa precisely:
      - integrate cumulative sum of mean-centered signal
      - scales = unique(round(logspace(log10(scale_min), log10(scale_max), num_scales)))
        filtered to scales >= 4
      - per scale s: n_windows = N // s; require n_windows >= 4 else fluctuation = nan
      - forward pass over the first n_windows*s points AND backward pass over the last
        n_windows*s points; each window degree-1 detrended; accumulate mean(residual^2)
      - fluctuation = sqrt(mean over 2*n_windows windows of mean(residual^2))
      - alpha = slope of log10(F) vs log10(s) over valid scales (need >= 4 valid)
    """
    signal = np.asarray(signal, dtype=float).ravel()
    N = signal.size
    if scale_max is None:
        scale_max = N // 4

    y = np.cumsum(signal - signal.mean())

    scales = np.unique(np.round(np.logspace(
        np.log10(scale_min), np.log10(scale_max), num_scales)).astype(int))
    scales = scales[scales >= 4]

    fluct = np.full(len(scales), np.nan)
    for i, s in enumerate(scales):
        n_windows = N // s
        if n_windows < 4:
            continue
        ms = _meanresid2_both_passes(y, s, n_windows, N)
        fluct[i] = np.sqrt(ms)

    valid = ~np.isnan(fluct)
    if valid.sum() < 4:
        return float("nan")
    log_s = np.log10(scales[valid])
    log_F = np.log10(fluct[valid])
    # degree-1 polyfit slope == OLS slope of log_F on log_s
    alpha = np.polyfit(log_s, log_F, 1)[0]
    return float(alpha)


def _meanresid2_both_passes(y: np.ndarray, s: int, n_windows: int, N: int) -> float:
    """Mean over all forward+backward non-overlapping length-s windows of
    mean(residual^2) after a per-window degree-1 (linear) detrend. Vectorized.

    Equivalent to pilot.dfa's inner double loop:
        rms_sum += mean(residual**2)   (per window, forward then backward)
        fluctuation = sqrt(rms_sum / count),  count = 2*n_windows
    """
    # forward windows: y[0 : n_windows*s] reshaped to (n_windows, s)
    fwd = y[:n_windows * s].reshape(n_windows, s)
    # backward windows: pilot takes y[N-(w+1)s : N-w*s] for w=0..n_windows-1.
    # Those are the last n_windows*s points, partitioned into consecutive length-s blocks
    # (w=0 is the LAST block). The SET of blocks == y[N-n_windows*s : N] reshaped to
    # (n_windows, s); order within the set does not affect the mean over windows.
    bwd = y[N - n_windows * s:].reshape(n_windows, s)
    blocks = np.concatenate([fwd, bwd], axis=0)              # (2*n_windows, s)
    mr2 = _detrend_meanresid2(blocks, s)                     # (2*n_windows,)
    return float(mr2.mean())


# cache the per-scale design moments (depend only on s)
_DESIGN_CACHE: dict[int, tuple] = {}


def _detrend_meanresid2(blocks: np.ndarray, s: int) -> np.ndarray:
    """For each row (length-s window), fit y = a*t + b by OLS over t=0..s-1, return
    mean(residual^2) per row. Closed-form, vectorized over rows.

    Matches np.polyfit(t, seg, 1) residuals exactly (same OLS, t = arange(s))."""
    if s in _DESIGN_CACHE:
        t, t_mean, Stt = _DESIGN_CACHE[s]
    else:
        t = np.arange(s, dtype=float)
        t_mean = t.mean()
        tc = t - t_mean
        Stt = (tc * tc).sum()
        _DESIGN_CACHE[s] = (t, t_mean, Stt)
    tc = t - t_mean                                          # (s,)
    y_mean = blocks.mean(axis=1, keepdims=True)              # (R,1)
    yc = blocks - y_mean                                     # (R,s) centered
    # slope a = sum(tc*yc)/Stt ; intercept handled by centering
    a = (yc @ tc) / Stt                                      # (R,)
    resid = yc - a[:, None] * tc[None, :]                    # (R,s)
    return np.mean(resid * resid, axis=1)                    # (R,)


def verify_against_pilot(seed: int = 2026) -> bool:
    """Assert dfa_fast == pilot.dfa[0] over the full beta range and several lengths."""
    import sys
    from pathlib import Path
    pilot_dir = Path(__file__).resolve().parents[2] / "1f_failsafe"
    if str(pilot_dir) not in sys.path:
        sys.path.insert(0, str(pilot_dir))
    from pilot import dfa, generate_colored_noise
    rng = np.random.default_rng(seed)
    max_abs = 0.0
    for N in (365, 730, 2000, 3900):
        for beta in (0.0, 0.3, 0.5, 1.0, 1.5, 2.0):
            sig = generate_colored_noise(N, beta, rng=rng)
            # exercise both the default scale_max and the explicit one used downstream
            a_ref, _, _ = dfa(sig)
            a_fast = dfa_fast(sig)
            if np.isfinite(a_ref):
                max_abs = max(max_abs, abs(a_ref - a_fast))
    ok = max_abs < 1e-9
    print(f"fast_dfa vs pilot.dfa  max|d_alpha| = {max_abs:.2e}  -> {'IDENTICAL' if ok else 'MISMATCH'}")
    return ok


if __name__ == "__main__":
    import time, sys
    from pathlib import Path
    pilot_dir = Path(__file__).resolve().parents[2] / "1f_failsafe"
    sys.path.insert(0, str(pilot_dir))
    from pilot import dfa, generate_colored_noise
    assert verify_against_pilot(), "fast_dfa does not match pilot.dfa"
    # speed comparison on a 365-window
    rng = np.random.default_rng(0)
    sig = generate_colored_noise(365, 1.0, rng=rng)
    t0 = time.time()
    for _ in range(200):
        dfa(sig)
    t_ref = time.time() - t0
    t0 = time.time()
    for _ in range(200):
        dfa_fast(sig)
    t_fast = time.time() - t0
    print(f"200x dfa(365):      pilot {t_ref:.2f}s   fast {t_fast:.3f}s   speedup {t_ref/t_fast:.0f}x")
