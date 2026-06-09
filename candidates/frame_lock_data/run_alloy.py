"""run_alloy.py — MEASURE AGENT driver for CASE = ALLOY.

Runs the REAL validated pipeline (mdl_synergy.py) on ALLOY across the full band
b in [16,12,8,6,4,3], plus the COPY null-floor calibration that LOCKS tau_eff.
Prints machine-readable JSON at the end so nothing is transcribed by hand.

No fabrication: every number below comes from mdl.* on cases.build_case(...).
"""

from __future__ import annotations

import json

import numpy as np

import mdl_synergy as mdl
from cases import build_case, PREDICTED

OUT = {}

# --- 0. sanity: confirm ALLOY construction matches the brief --------------------
A, B, M = build_case("ALLOY")
A64, B64, M64 = A.astype(np.float64), B.astype(np.float64), M.astype(np.float64)
M_expected = (0.5 * A64 + 0.5 * B64 + 0.1 * (A64 * B64)).astype(np.float32).astype(np.float64)
OUT["alloy_construction_max_abs_err_vs_formula"] = float(np.max(np.abs(M64 - M_expected)))
OUT["alloy_predicted_label"] = PREDICTED["ALLOY"]
OUT["shape"] = list(M.shape)
OUT["dtype"] = str(M.dtype)
OUT["n_elem"] = int(M.size)
OUT["band"] = mdl.BAND
OUT["r_floor"] = mdl.R_FLOOR
OUT["r_top"] = mdl.R_TOP
OUT["lzma_preset"] = mdl.LZMA_PRESET

# --- 1. COPY null-floor calibration -> tau_eff (LOCKED rule) --------------------
cA, cB, cM = build_case("COPY")
tau_eff, base_delta, sigma = mdl.compute_tau_eff(cA, cB, cM, b=mdl.R_TOP,
                                                 n_boot=200, seed=12345)
OUT["copy_base_delta_bits"] = base_delta            # Syn_wit(COPY @ r_top)
OUT["copy_bootstrap_sigma_bits"] = sigma
OUT["tau_eff_bits"] = tau_eff
# COPY's own Syn_pid at r_top (for completeness of the null report)
OUT["copy_syn_pid_at_rtop"] = mdl.syn_pid(cA, cB, cM, mdl.R_TOP)

# --- 2. ALLOY full-band sweep under the PINNED lzma compressor ------------------
rows = mdl.band_sweep(A, B, M)   # pinned lzma, most-fine first
alloy_curve = []
for r in rows:
    alloy_curve.append({
        "b": r.b,
        "L_RA": r.L_RA,
        "L_RB": r.L_RB,
        "L_RAB": r.L_RAB,
        "syn_wit_bits": r.syn_wit,           # = L_RAB
        "syn_pid_bits": r.syn_pid,           # = min(L_RA,L_RB) - L_RAB
        "syn_wit_per_elem": r.syn_wit_per_elem,
        "syn_pid_per_elem": r.syn_pid_per_elem,
        "wit_ge_tau": bool(r.syn_wit >= tau_eff),
    })
OUT["alloy_curve_lzma"] = alloy_curve

# values at r_top
rtop_row = [r for r in rows if r.b == mdl.R_TOP][0]
OUT["alloy_syn_wit_at_rtop"] = rtop_row.syn_wit
OUT["alloy_syn_pid_at_rtop"] = rtop_row.syn_pid

# --- 3. verdicts under BOTH estimators -----------------------------------------
# Witnessed verdict: PASS iff Syn_wit(b) >= tau_eff for EVERY b in band incl r_top.
wit_passes, wit_per_b = mdl.verdict_from_band(rows, tau_eff)
OUT["alloy_wit_verdict"] = "PASS" if wit_passes else "FAIL"
OUT["alloy_wit_per_b"] = [{"b": b, "syn_wit": sw, "ge_tau": bool(ok)}
                          for (b, sw, ok) in wit_per_b]

# PID verdict: the naive BES-4.4 reading flags SYNERGY when Syn_pid > 0.
# Apply the same tau_eff band rule to Syn_pid for a like-for-like "verdict",
# AND separately report the raw sign test at r_top (the literal BES-4.4 flag).
pid_band_pass = all(r.syn_pid >= tau_eff for r in rows)
OUT["alloy_pid_verdict_taurule"] = "PASS" if pid_band_pass else "FAIL"
OUT["alloy_pid_sign_flag_at_rtop"] = "SYNERGY(>0)" if rtop_row.syn_pid > 0 else "<=0"
OUT["alloy_pid_per_b"] = [{"b": r.b, "syn_pid": r.syn_pid,
                           "ge_tau": bool(r.syn_pid >= tau_eff),
                           "positive": bool(r.syn_pid > 0)} for r in rows]

# --- 4. sibling-compressor error bars (lzma / zlib / bz2) ------------------------
# Full band under each compressor, so we can quote the spread at r_top AND across band.
sib = {}
for c in ("lzma", "zlib", "bz2"):
    crows = mdl.band_sweep(A, B, M, compressor=c)
    sib[c] = {
        "syn_wit_curve": [{"b": r.b, "syn_wit_bits": r.syn_wit} for r in crows],
        "syn_pid_curve": [{"b": r.b, "syn_pid_bits": r.syn_pid} for r in crows],
        "syn_wit_at_rtop": [r.syn_wit for r in crows if r.b == mdl.R_TOP][0],
        "syn_pid_at_rtop": [r.syn_pid for r in crows if r.b == mdl.R_TOP][0],
    }
OUT["alloy_siblings"] = sib

# spread of Syn_wit at r_top across the three compressors
wit_rtop_vals = [sib[c]["syn_wit_at_rtop"] for c in ("lzma", "zlib", "bz2")]
OUT["alloy_wit_rtop_spread"] = {
    "lzma": sib["lzma"]["syn_wit_at_rtop"],
    "zlib": sib["zlib"]["syn_wit_at_rtop"],
    "bz2": sib["bz2"]["syn_wit_at_rtop"],
    "min": int(min(wit_rtop_vals)),
    "max": int(max(wit_rtop_vals)),
    "range": int(max(wit_rtop_vals) - min(wit_rtop_vals)),
}

# Does the WITNESSED r_top verdict hold under ALL three compressors?
# (tau_eff itself is lzma-pinned; this just checks robustness of the FAIL.)
OUT["alloy_wit_rtop_fail_under_all_siblings"] = all(v < tau_eff for v in wit_rtop_vals)

# --- 5. contrast vs ADD affine floor (honest diagnostic) ------------------------
add_rows = mdl.band_sweep(*build_case("ADD"))
OUT["add_syn_wit_curve"] = [{"b": r.b, "syn_wit_bits": r.syn_wit} for r in add_rows]
OUT["alloy_minus_add_wit"] = [
    {"b": a.b, "delta_wit_bits": a.syn_wit - d.syn_wit}
    for a, d in zip(rows, add_rows)
]

print(json.dumps(OUT, indent=2))
