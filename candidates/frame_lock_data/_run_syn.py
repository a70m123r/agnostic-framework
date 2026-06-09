"""_run_syn.py — MEASURE AGENT driver for CASE = SYN (called-shot: PASS).

Runs the REAL validated pipeline (mdl_synergy + cases) on SYN across the full
band b in [16,12,8,6,4,3] under all three compressors; calibrates tau_eff from
the COPY null floor per the LOCKED rule (base_delta + 3*sigma); applies the
witnessed and PID verdicts. Emits machine-parseable JSON at the end.
"""
from __future__ import annotations

import json
import mdl_synergy as mdl
from cases import build_case, PREDICTED

CASE = "SYN"
A, B, M = build_case(CASE)
print(f"CASE={CASE} predicted={PREDICTED[CASE]}  band={mdl.BAND} r_top={mdl.R_TOP}")
print(f"shapes A{A.shape} B{B.shape} M{M.shape} dtype={M.dtype} n_elem={M.size}")

# --- COPY floor calibration (LOCKED rule, pinned lzma) -----------------------
cA, cB, cM = build_case("COPY")
tau_eff, base_delta, sigma = mdl.compute_tau_eff(cA, cB, cM, b=mdl.R_TOP,
                                                 n_boot=200, seed=12345)
print("\n[COPY floor / LOCKED tau_eff rule, pinned lzma]")
print(f"  base_delta = Syn_wit(COPY @ r_top={mdl.R_TOP}) = {base_delta} bits")
print(f"  bootstrap sigma (n=200, seed=12345)           = {sigma:.6f} bits")
print(f"  tau_eff = base_delta + 3*sigma                = {tau_eff:.6f} bits")

# --- SYN full band, pinned lzma ----------------------------------------------
rows = mdl.band_sweep(A, B, M)  # pinned lzma
print("\n[SYN full band, pinned lzma]")
print(mdl.format_band_table(rows, title=f"  --- {CASE} (predicted {PREDICTED[CASE]}) ---"))
passes, per_b = mdl.verdict_from_band(rows, tau_eff)
print(f"  per-b (b, Syn_wit, >=tau_eff): {per_b}")
print(f"  WITNESSED verdict (all b >= tau_eff): {'PASS' if passes else 'FAIL'}")

# PID verdict: BES-4.4 form. PID 'flags synergy' when Syn_pid>0. We report the
# PID verdict at r_top under the SAME tau_eff gate AND the sign reading.
rtop = [r for r in rows if r.b == mdl.R_TOP][0]
pid_pass_tau = all(r.syn_pid >= tau_eff for r in rows)
print(f"  Syn_pid@r_top = {rtop.syn_pid} bits ; Syn_pid>0 at r_top: {rtop.syn_pid>0}")
print(f"  PID verdict (all b Syn_pid>=tau_eff): {'PASS' if pid_pass_tau else 'FAIL'}")

# --- SYN full band, sibling compressors (error bars) -------------------------
sib = {}
for comp in ("lzma", "zlib", "bz2"):
    sib[comp] = mdl.band_sweep(A, B, M, compressor=comp)
print("\n[SYN error-bar siblings: Syn_wit (bits) by compressor across band]")
print(f"    {'b':>3} {'lzma':>10} {'zlib':>10} {'bz2':>10}")
for k, b in enumerate(mdl.BAND):
    print(f"    {b:>3} {sib['lzma'][k].syn_wit:>10} {sib['zlib'][k].syn_wit:>10} {sib['bz2'][k].syn_wit:>10}")
print("\n[SYN error-bar siblings: Syn_pid (bits) by compressor across band]")
print(f"    {'b':>3} {'lzma':>10} {'zlib':>10} {'bz2':>10}")
for k, b in enumerate(mdl.BAND):
    print(f"    {b:>3} {sib['lzma'][k].syn_pid:>10} {sib['zlib'][k].syn_pid:>10} {sib['bz2'][k].syn_pid:>10}")

# --- machine-parseable JSON --------------------------------------------------
out = {
    "case": CASE,
    "predicted": PREDICTED[CASE],
    "band": mdl.BAND,
    "r_top": mdl.R_TOP,
    "n_elem": int(M.size),
    "tau_eff": tau_eff,
    "base_delta_copy_floor": base_delta,
    "bootstrap_sigma": sigma,
    "syn_wit_curve": [{"b": r.b, "syn_wit_bits": int(r.syn_wit)} for r in rows],
    "syn_pid_curve": [{"b": r.b, "syn_pid_bits": int(r.syn_pid)} for r in rows],
    "syn_wit_at_rtop": int(rtop.syn_wit),
    "syn_pid_at_rtop": int(rtop.syn_pid),
    "witnessed_verdict": "PASS" if passes else "FAIL",
    "pid_verdict_tau": "PASS" if pid_pass_tau else "FAIL",
    "pid_sign_at_rtop_positive": bool(rtop.syn_pid > 0),
    "siblings_syn_wit": {c: [int(sib[c][k].syn_wit) for k in range(len(mdl.BAND))] for c in sib},
    "siblings_syn_pid": {c: [int(sib[c][k].syn_pid) for k in range(len(mdl.BAND))] for c in sib},
}
print("\nJSON_BEGIN")
print(json.dumps(out))
print("JSON_END")
