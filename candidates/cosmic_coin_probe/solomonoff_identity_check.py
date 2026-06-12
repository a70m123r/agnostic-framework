# -*- coding: utf-8 -*-
"""
Angle: solomonoff-identity.
Test codelength ~= predictive entropy (p = 2^-bits) on the REAL probe data.

For BOTH phenomena:
  (a) empirical entropy of the residual series at the disclosed quantization:
        - plug-in histogram entropy of the quantized symbols (+ Miller-Madow)
        - Gaussian discrete entropy 0.5*log2(2*pi*e*var) - log2(q)
  (b) actual lzma codelength PER SYMBOL of the quantized residual
        (exactly the harness encoding: int64 -> bytes -> lzma preset 9)
Plus controls:
  - coder fixed overhead (lzma container) so small-n orbit isn't penalized
  - SHUFFLE control: lzma on permuted symbols ~ iid/marginal-entropy coder;
    ordered-vs-shuffled gap = temporal structure lzma finds beyond marginal
  - lag-1 autocorrelation, kurtosis (Gaussianity / iid-ness diagnostics)
"""
import json, lzma, math, pathlib
import numpy as np

HERE = pathlib.Path(r"D:/PlatformOperator/research/pav/candidates/cosmic_coin_probe")
npz = np.load(HERE / "probe_data" / "series.npz")
Q_POS_KM, Q_LOGFLUX = 1.0, 1e-3

res_o = npz["orbit_resid"]            # (n_epochs, 3) km
res_f = npz["flare_resid"]            # (n_steps,)  dex increments
nll_o = npz["orbit_nll"]              # bits/step (3 symbols/step)
nll_f = npz["flare_nll"]              # bits/step (1 symbol/step)

def clen_bits(int_array):
    b = np.ascontiguousarray(int_array.astype(np.int64)).tobytes()
    return len(lzma.compress(b, preset=9)) * 8

LZMA_OVERHEAD_BITS = len(lzma.compress(b"", preset=9)) * 8   # container cost

def plug_in_entropy(ints):
    _, cnt = np.unique(ints, return_counts=True)
    n = cnt.sum()
    p = cnt / n
    H = float(-(p * np.log2(p)).sum())
    mm = (len(cnt) - 1) / (2.0 * math.log(2) * n)             # Miller-Madow
    return H, H + mm, int(len(cnt)), int(n)

def gauss_H_bits(var, q):
    return 0.5 * math.log2(2 * math.pi * math.e * max(var, 1e-300)) - math.log2(q)

def lag1(x):
    x = x - x.mean()
    return float(np.dot(x[:-1], x[1:]) / np.dot(x, x))

def kurt(x):
    x = x - x.mean()
    return float(np.mean(x**4) / np.mean(x**2)**2 - 3.0)

def shuffled_bits_per_sym(ints, reps=3):
    rng = np.random.default_rng(0)
    vals = []
    for _ in range(reps):
        vals.append(clen_bits(rng.permutation(ints)) / ints.size)
    return float(np.mean(vals)), float(np.std(vals))

report = {"lzma_container_overhead_bits": LZMA_OVERHEAD_BITS}

# ---------------- ORBIT (3 symbols per step, flattened exactly like harness)
oi = np.round(res_o / Q_POS_KM).astype(np.int64).reshape(-1)
n_o = oi.size
lz_o = clen_bits(oi)
H_hist_o, H_hist_o_mm, K_o, _ = plug_in_entropy(oi)
sig_ax = np.std(res_o, axis=0)
H_gauss_peraxis = float(np.mean([gauss_H_bits(s * s, Q_POS_KM) for s in sig_ax]))
H_gauss_meansig = gauss_H_bits(float(sig_ax.mean())**2, Q_POS_KM)   # harness headline convention
sh_o, sh_o_sd = shuffled_bits_per_sym(oi)
# innovation proxy: per-axis first difference of the residual drift
dres = np.diff(res_o, axis=0)
H_gauss_diff = float(np.mean([gauss_H_bits(np.var(dres[:, k]), Q_POS_KM) for k in range(3)]))
di = np.round(dres / Q_POS_KM).astype(np.int64).reshape(-1)
lz_diff_o = clen_bits(di) / di.size

orbit = dict(
    n_symbols=n_o,
    lzma_total_bits=lz_o,
    matches_results_json=bool(lz_o == 11488),
    lzma_bits_per_symbol=lz_o / n_o,
    lzma_bits_per_symbol_net=(lz_o - LZMA_OVERHEAD_BITS) / n_o,
    hist_entropy_bits_per_symbol=H_hist_o,
    hist_entropy_miller_madow=H_hist_o_mm,
    hist_support=K_o, frac_unique=K_o / n_o, log2_n_cap=math.log2(n_o),
    gauss_entropy_bits_per_symbol_peraxis=H_gauss_peraxis,
    gauss_entropy_bits_per_symbol_meansigma=H_gauss_meansig,
    nll_mean_bits_per_symbol=float(nll_o.mean()) / 3.0,
    shuffled_lzma_bits_per_symbol=sh_o, shuffled_sd=sh_o_sd,
    gap_lzma_minus_hist=lz_o / n_o - H_hist_o,
    gap_lzma_minus_gauss=lz_o / n_o - H_gauss_peraxis,
    gap_shuffled_minus_gauss=sh_o - H_gauss_peraxis,
    innovation_gauss_entropy_bits_per_symbol=H_gauss_diff,
    innovation_lzma_bits_per_symbol=lz_diff_o,
    lag1_autocorr_per_axis=[lag1(res_o[:, k]) for k in range(3)],
    sigma_per_axis_km=[float(s) for s in sig_ax],
)

# ---------------- FLARE (1 symbol per step)
fi = np.round(res_f / Q_LOGFLUX).astype(np.int64)
n_f = fi.size
lz_f = clen_bits(fi)
H_hist_f, H_hist_f_mm, K_f, _ = plug_in_entropy(fi)
H_gauss_f = gauss_H_bits(float(np.var(res_f)), Q_LOGFLUX)
sh_f, sh_f_sd = shuffled_bits_per_sym(fi)

flare = dict(
    n_symbols=n_f,
    lzma_total_bits=lz_f,
    matches_results_json=bool(lz_f == 57088),
    lzma_bits_per_symbol=lz_f / n_f,
    lzma_bits_per_symbol_net=(lz_f - LZMA_OVERHEAD_BITS) / n_f,
    hist_entropy_bits_per_symbol=H_hist_f,
    hist_entropy_miller_madow=H_hist_f_mm,
    hist_support=K_f, frac_unique=K_f / n_f, log2_n_cap=math.log2(n_f),
    gauss_entropy_bits_per_symbol=H_gauss_f,
    nll_mean_bits_per_symbol=float(nll_f.mean()),
    shuffled_lzma_bits_per_symbol=sh_f, shuffled_sd=sh_f_sd,
    gap_lzma_minus_hist=lz_f / n_f - H_hist_f,
    gap_lzma_minus_gauss=lz_f / n_f - H_gauss_f,
    gap_shuffled_minus_gauss=sh_f - H_gauss_f,
    lag1_autocorr=lag1(res_f),
    excess_kurtosis=kurt(res_f),
    sigma_dex=float(np.std(res_f)),
)

# ---------------- dimensionless cross-phenomenon view (the de-trapped compare)
raw_o_bits, raw_f_bits = 28288, 72576       # from results.json, same coder
cross = dict(
    orbit_lzma_saved_fraction=1.0 - lz_o / raw_o_bits,
    flare_lzma_saved_fraction=1.0 - lz_f / raw_f_bits,
    orbit_entropy_saved_fraction=1.0 - 43.30012280024418 / 85.23517071791309,
    flare_entropy_saved_fraction=1.0 - 6.171764495568608 / 9.673529180998328,
    orbit_comp_ratio_resid_only=raw_o_bits / lz_o,
    flare_comp_ratio_resid_only=raw_f_bits / lz_f,
)

report.update(orbit=orbit, flare=flare, cross=cross)
print(json.dumps(report, indent=2))
