"""diag_floor.py — characterize whether tau_eff (COPY-anchored) separates the
affine-span cases (ADD, ROT) from the genuinely-synergistic ones, and locate
the ALLOY r_top result relative to the ADD affine floor.

This is the honest diagnostic for WHY the ALLOY witnessed verdict came out the
way it did. No fabrication.
"""
from __future__ import annotations
import json
import numpy as np
import mdl_synergy as mdl
from cases import build_case, CASE_NAMES, PREDICTED

cA, cB, cM = build_case("COPY")
tau_eff, base_delta, sigma = mdl.compute_tau_eff(cA, cB, cM, b=mdl.R_TOP,
                                                 n_boot=200, seed=12345)

OUT = {"tau_eff": tau_eff, "base_delta": base_delta, "sigma": sigma}

# COPY degeneracy check: is M essentially A? (range collapse on R_AB)
A, B, M = cA, cB, cM
OUT["copy_M_equals_A_max_abs"] = float(np.max(np.abs(M.astype(np.float64) - A.astype(np.float64))))

# Witnessed verdict (band rule) for EVERY case under the single COPY-anchored tau
per_case = {}
for nm in CASE_NAMES:
    A, B, M = build_case(nm)
    rows = mdl.band_sweep(A, B, M)
    passes, per_b = mdl.verdict_from_band(rows, tau_eff)
    rtop = [r for r in rows if r.b == mdl.R_TOP][0]
    per_case[nm] = {
        "predicted": PREDICTED[nm],
        "wit_verdict_taurule": "PASS" if passes else "FAIL",
        "syn_wit_at_rtop": rtop.syn_wit,
        "syn_wit_at_rtop_over_tau": rtop.syn_wit / tau_eff,
        "syn_wit_curve": [r.syn_wit for r in rows],
        "syn_pid_at_rtop": rtop.syn_pid,
    }
OUT["per_case_taurule"] = per_case

# The KEY contrast: does Syn_wit separate affine-span (ADD/ROT/COPY) from
# nonlinear (SYN/ALLOY) if we anchor the floor at the AFFINE floor (ADD) instead
# of the degenerate COPY? Report ALLOY - ADD and SYN - ADD at each b.
addrows = mdl.band_sweep(*build_case("ADD"))
for src in ("SYN", "ALLOY", "ROT", "COPY"):
    srows = mdl.band_sweep(*build_case(src))
    OUT[f"{src}_minus_ADD_wit"] = [
        {"b": s.b, "delta": s.syn_wit - a.syn_wit} for s, a in zip(srows, addrows)
    ]

# If we (hypothetically) anchored tau on the ADD affine floor + 3 sigma of ADD's
# own bootstrap, would ALLOY then FAIL at r_top? (exploratory, NOT the locked rule)
addA, addB, addM = build_case("ADD")
add_floor = mdl.syn_wit(addA, addB, addM, mdl.R_TOP)
add_sigma = mdl.bootstrap_sigma_syn_wit(addA, addB, addM, mdl.R_TOP, n_boot=200, seed=12345)
alt_tau = add_floor + 3.0 * add_sigma
OUT["EXPLORATORY_add_anchored"] = {
    "add_floor_rtop": add_floor,
    "add_sigma_rtop": add_sigma,
    "alt_tau": alt_tau,
}
for nm in ("SYN", "ALLOY", "ROT"):
    A, B, M = build_case(nm)
    rows = mdl.band_sweep(A, B, M)
    passes_alt = all(r.syn_wit >= alt_tau for r in rows)
    rtop = [r for r in rows if r.b == mdl.R_TOP][0]
    OUT["EXPLORATORY_add_anchored"][nm] = {
        "rtop_syn_wit": rtop.syn_wit,
        "rtop_ge_alt_tau": bool(rtop.syn_wit >= alt_tau),
        "band_all_ge_alt_tau": bool(passes_alt),
    }

print(json.dumps(OUT, indent=2))
