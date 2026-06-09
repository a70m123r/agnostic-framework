"""run_rot.py — MEASURE AGENT for CASE = ROT (called shot: FAIL).

Runs the VALIDATED pipeline (mdl_synergy.py) on the ROT case across the full
band b in [16,12,8,6,4,3]. Also calibrates tau_eff from the COPY null per the
LOCKED lock-before-data rule. Reports Syn_wit and Syn_pid curves (bits) under
the pinned lzma compressor, plus zlib/bz2 sibling error bars at r_top, and the
realized verdicts under BOTH estimators. Nothing is modified in the pipeline.
"""

from __future__ import annotations

import json

import mdl_synergy as mdl
from cases import build_case, PREDICTED

CASE = "ROT"

# --- COPY null floor -> tau_eff (LOCKED rule), exactly as smoke.py does -------
cA, cB, cM = build_case("COPY")
tau_eff, base_delta, sigma = mdl.compute_tau_eff(
    cA, cB, cM, b=mdl.R_TOP, n_boot=200, seed=12345)

# bootstrap sigma siblings on the COPY floor for an error-bar note on the floor
copy_floor_siblings = {}
for c in ("lzma", "zlib", "bz2"):
    bd = mdl.syn_wit(cA, cB, cM, mdl.R_TOP, compressor=c)
    copy_floor_siblings[c] = bd

# --- ROT full-band sweep under pinned lzma -----------------------------------
A, B, M = build_case(CASE)
rows = mdl.band_sweep(A, B, M)  # pinned lzma
passes, per_b = mdl.verdict_from_band(rows, tau_eff)

# --- ROT full-band under sibling compressors (for spread across the band) ----
sib_sweeps = mdl.band_sweep_all_compressors(A, B, M)

# --- assemble curves ----------------------------------------------------------
syn_wit_curve = [{"b": r.b, "syn_wit_bits": r.syn_wit} for r in rows]
syn_pid_curve = [{"b": r.b, "syn_pid_bits": r.syn_pid} for r in rows]

rtop_row = [r for r in rows if r.b == mdl.R_TOP][0]
rfloor_row = [r for r in rows if r.b == mdl.R_FLOOR][0]

syn_wit_at_rtop = rtop_row.syn_wit
syn_pid_at_rtop = rtop_row.syn_pid

# witnessed verdict: PASS iff Syn_wit(b) >= tau_eff for EVERY b
wit_pass = passes
# pid verdict: the naive estimator flags SYNERGY iff Syn_pid > 0 at r_top
pid_flags_synergy_rtop = syn_pid_at_rtop > 0

# sibling spread of Syn_wit at r_top
rtop_siblings = {c: [r for r in sib_sweeps[c] if r.b == mdl.R_TOP][0].syn_wit
                 for c in sib_sweeps}

print("=" * 80)
print(f"MEASURE AGENT — CASE = {CASE}  (called shot: {PREDICTED[CASE]})")
print("pinned compressor = lzma preset 6 ; shape (256,256) float32")
print("band =", mdl.BAND, "; r_floor =", mdl.R_FLOOR, "; r_top =", mdl.R_TOP)
print("=" * 80)

print("\n[COPY null floor -> LOCKED tau_eff rule]")
print(f"  base_delta = Syn_wit(COPY @ r_top={mdl.R_TOP}) [lzma] = {base_delta} bits")
print(f"  bootstrap sigma (n=200, seed=12345)               = {sigma:.6f} bits")
print(f"  tau_eff = base_delta + 3*sigma                     = {tau_eff:.6f} bits")
print(f"  COPY-floor sibling spread (Syn_wit @ r_top): "
      f"lzma={copy_floor_siblings['lzma']} zlib={copy_floor_siblings['zlib']} "
      f"bz2={copy_floor_siblings['bz2']}")

print(f"\n[{CASE} full-band sweep, pinned lzma]")
print(mdl.format_band_table(rows, title=f"  --- {CASE} (predicted {PREDICTED[CASE]}) ---"))

print(f"\n[{CASE} Syn_wit vs tau_eff, per b]")
for (b, sw, ok) in per_b:
    print(f"  b={b:>3}  Syn_wit={sw:>9}  >= tau_eff({tau_eff:.1f})? {ok}")

print(f"\n[{CASE} headline numbers]")
print(f"  Syn_wit @ r_floor(16) = {rfloor_row.syn_wit} bits   "
      f"Syn_wit @ r_top(3) = {syn_wit_at_rtop} bits")
print(f"  Syn_pid @ r_floor(16) = {rfloor_row.syn_pid} bits   "
      f"Syn_pid @ r_top(3) = {syn_pid_at_rtop} bits")

print(f"\n[{CASE} sibling-compressor full band: Syn_wit bits (lzma/zlib/bz2)]")
print(f"  {'b':>3}  {'lzma':>9}  {'zlib':>9}  {'bz2':>9}")
for k, b in enumerate(mdl.BAND):
    print(f"  {b:>3}  "
          f"{sib_sweeps['lzma'][k].syn_wit:>9}  "
          f"{sib_sweeps['zlib'][k].syn_wit:>9}  "
          f"{sib_sweeps['bz2'][k].syn_wit:>9}")

print(f"\n[{CASE} sibling-compressor full band: Syn_pid bits (lzma/zlib/bz2)]")
print(f"  {'b':>3}  {'lzma':>9}  {'zlib':>9}  {'bz2':>9}")
for k, b in enumerate(mdl.BAND):
    print(f"  {b:>3}  "
          f"{sib_sweeps['lzma'][k].syn_pid:>9}  "
          f"{sib_sweeps['zlib'][k].syn_pid:>9}  "
          f"{sib_sweeps['bz2'][k].syn_pid:>9}")

print("\n[REALIZED VERDICTS]")
print(f"  WITNESSED (Syn_wit >= tau_eff for ALL b incl r_top): "
      f"{'PASS' if wit_pass else 'FAIL'}")
print(f"  NAIVE PID (Syn_pid @ r_top > 0 => flags synergy): "
      f"Syn_pid@r_top = {syn_pid_at_rtop} -> "
      f"{'PASS(flags SYNERGY)' if pid_flags_synergy_rtop else 'FAIL(no synergy)'}")
print(f"  Called shot for {CASE}: {PREDICTED[CASE]}")
print(f"  Witnessed matches called shot (FAIL)? "
      f"{(not wit_pass)}")

# machine-readable dump for the structured handoff
out = {
    "case": CASE,
    "predicted": PREDICTED[CASE],
    "band": mdl.BAND,
    "r_floor": mdl.R_FLOOR,
    "r_top": mdl.R_TOP,
    "tau_eff": tau_eff,
    "base_delta_copy_floor": base_delta,
    "bootstrap_sigma": sigma,
    "copy_floor_siblings": copy_floor_siblings,
    "syn_wit_curve": syn_wit_curve,
    "syn_pid_curve": syn_pid_curve,
    "syn_wit_at_rtop": syn_wit_at_rtop,
    "syn_pid_at_rtop": syn_pid_at_rtop,
    "rtop_siblings_wit": rtop_siblings,
    "sibling_full_band_wit": {
        c: [{"b": r.b, "syn_wit_bits": r.syn_wit} for r in sib_sweeps[c]]
        for c in sib_sweeps
    },
    "sibling_full_band_pid": {
        c: [{"b": r.b, "syn_pid_bits": r.syn_pid} for r in sib_sweeps[c]]
        for c in sib_sweeps
    },
    "wit_pass": wit_pass,
    "pid_flags_synergy_rtop": pid_flags_synergy_rtop,
    "wit_matches_called_shot_FAIL": (not wit_pass),
}
print("\n[JSON]")
print(json.dumps(out, indent=2))
