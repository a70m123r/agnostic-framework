# -*- coding: utf-8 -*-
"""Coder-robustness re-measure for the cosmic-coin probe.

Dimensionless cross-phenomenon ranking: compression ratio (raw/resid),
bits-saved fraction ((raw-resid)/raw) under lzma-9 / zlib-9 / bz2-9,
recomputed from series.npz (verification against results.json), plus an
analytic Gaussian entropy floor. INSTRUMENT register: locates the coin
edge, does not declare anything incompressible.
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(r"D:\PlatformOperator\research\pav\candidates\cosmic_coin_probe")
Q_POS_KM = 1.0
Q_LOGFLUX = 1e-3

def clen_bits(int_array, coder):
    b = np.ascontiguousarray(int_array.astype(np.int64)).tobytes()
    if coder == "lzma":
        c = lzma.compress(b, preset=9)
    elif coder == "zlib":
        c = zlib.compress(b, 9)
    elif coder == "bz2":
        c = bz2.compress(b, 9)
    return len(c) * 8

# ---- load harness output + raw series -------------------------------------
results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
npz = np.load(HERE / "probe_data" / "series.npz")
orbit_truth = npz["orbit_truth"]     # (N,3) km
orbit_resid = npz["orbit_resid"]     # (N,3) km
flare_truth = npz["flare_truth"]     # (M,)  log10 flux
flare_resid = npz["flare_resid"]     # (M,)  log10 increments

# ---- 1) recompute coder bits from the arrays (verify results.json) --------
orbit_raw_i = np.round(orbit_truth / Q_POS_KM).astype(np.int64).reshape(-1)
orbit_res_i = np.round(orbit_resid / Q_POS_KM).astype(np.int64).reshape(-1)
flare_raw_i = np.round(flare_truth / Q_LOGFLUX).astype(np.int64)
flare_res_i = np.round(flare_resid / Q_LOGFLUX).astype(np.int64)

MODEL_BITS = {"orbit": 7 * 64, "flare": 64}
recomp, verify_ok = {}, True
for coder in ("lzma", "zlib", "bz2"):
    row = {}
    for name, raw_i, res_i in (("orbit", orbit_raw_i, orbit_res_i),
                               ("flare", flare_raw_i, flare_res_i)):
        raw_b = clen_bits(raw_i, coder)
        res_b = clen_bits(res_i, coder)
        ref = results[name]["mdl"][coder]
        match = (raw_b == ref["raw_bits"] and res_b == ref["resid_bits"])
        verify_ok &= match
        m = MODEL_BITS[name]
        row[name] = dict(
            raw_bits=raw_b, resid_bits=res_b, model_bits=m, matches_results_json=match,
            ratio_no_model=raw_b / res_b,
            ratio_with_model=raw_b / (res_b + m),
            saved_frac_no_model=(raw_b - res_b) / raw_b,
            saved_frac_with_model=(raw_b - res_b - m) / raw_b,
        )
    row["orbit_gt_flare_ratio"] = row["orbit"]["ratio_no_model"] > row["flare"]["ratio_no_model"]
    row["orbit_gt_flare_ratio_with_model"] = row["orbit"]["ratio_with_model"] > row["flare"]["ratio_with_model"]
    row["orbit_gt_flare_frac"] = row["orbit"]["saved_frac_no_model"] > row["flare"]["saved_frac_no_model"]
    row["margin_ratio_of_ratios"] = row["orbit"]["ratio_no_model"] / row["flare"]["ratio_no_model"]
    row["margin_ratio_of_ratios_with_model"] = row["orbit"]["ratio_with_model"] / row["flare"]["ratio_with_model"]
    row["margin_frac_diff"] = row["orbit"]["saved_frac_no_model"] - row["flare"]["saved_frac_no_model"]
    recomp[coder] = row

# ---- 2) analytic Gaussian entropy floor ------------------------------------
def gauss_bits(var, q):
    return 0.5 * math.log2(2 * math.pi * math.e * var) - math.log2(q)

# orbit: per-axis variances, total entropy = sum over 3 axes
ovar_raw = np.var(orbit_truth, axis=0)
ovar_res = np.var(orbit_resid, axis=0)
oH_raw = sum(gauss_bits(v, Q_POS_KM) for v in ovar_raw)
oH_res = sum(gauss_bits(v, Q_POS_KM) for v in ovar_res)
# flare: 1-D
fvar_raw = float(np.var(flare_truth))
fvar_res = float(np.var(flare_resid))
fH_raw = gauss_bits(fvar_raw, Q_LOGFLUX)
fH_res = gauss_bits(fvar_res, Q_LOGFLUX)

# q-invariant per-dim bits saved (the -log2 q cancels in the difference)
o_saved_per_dim = 0.5 * float(np.mean(np.log2(ovar_raw / ovar_res)))
f_saved_per_dim = 0.5 * math.log2(fvar_raw / fvar_res)

gauss = dict(
    orbit=dict(H_raw_bits_step=oH_raw, H_resid_bits_step=oH_res,
               ratio=oH_raw / oH_res, saved_frac=(oH_raw - oH_res) / oH_raw,
               saved_bits_per_dim=o_saved_per_dim,
               sigma_shrink_factor=2 ** o_saved_per_dim),
    flare=dict(H_raw_bits_step=fH_raw, H_resid_bits_step=fH_res,
               ratio=fH_raw / fH_res, saved_frac=(fH_raw - fH_res) / fH_raw,
               saved_bits_per_dim=f_saved_per_dim,
               sigma_shrink_factor=2 ** f_saved_per_dim),
)
gauss["orbit_gt_flare_ratio"] = gauss["orbit"]["ratio"] > gauss["flare"]["ratio"]
gauss["orbit_gt_flare_frac"] = gauss["orbit"]["saved_frac"] > gauss["flare"]["saved_frac"]
gauss["orbit_gt_flare_per_dim"] = o_saved_per_dim > f_saved_per_dim
gauss["margin_frac_diff"] = gauss["orbit"]["saved_frac"] - gauss["flare"]["saved_frac"]
gauss["margin_per_dim_bits"] = o_saved_per_dim - f_saved_per_dim

# the known trap, reproduced for the record (absolute bits/step, incommensurate)
trap = dict(
    orbit_appearance_bits_step=results["orbit"]["appearance_bits_per_step"],
    flare_appearance_bits_step=results["flare"]["appearance_bits_per_step"],
    naive_absolute_gap=results["coin_edge"]["separation_bits"],
)

holds_all = all(recomp[c]["orbit_gt_flare_ratio"] and recomp[c]["orbit_gt_flare_frac"]
                and recomp[c]["orbit_gt_flare_ratio_with_model"]
                for c in ("lzma", "zlib", "bz2"))
holds_all_plus_floor = holds_all and gauss["orbit_gt_flare_ratio"] and \
    gauss["orbit_gt_flare_frac"] and gauss["orbit_gt_flare_per_dim"]

out = dict(verify_recompute_matches_results_json=bool(verify_ok),
           per_coder=recomp, gaussian_floor=gauss, known_trap_reproduced=trap,
           ranking_coder_robust=bool(holds_all),
           ranking_holds_including_floor=bool(holds_all_plus_floor),
           n_orbit=int(orbit_truth.shape[0]), n_flare=int(flare_truth.shape[0]))
print(json.dumps(out, indent=2, default=float))
