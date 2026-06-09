"""run_copy.py — MEASURE AGENT driver for CASE = COPY.

Runs the REAL validated pipeline (mdl_synergy + cases) on the COPY case across
the full band b in [16,12,8,6,4,3] for BOTH estimators (Syn_wit, Syn_pid),
under all three compressors (lzma pinned, zlib, bz2).

COPY also CALIBRATES the lock-before-data threshold:
    base_delta = Syn_wit(COPY @ r_top=3)         (the realized null floor)
    sigma      = bootstrap sigma of that quantity (n=200, seed=12345)
    tau_eff    = base_delta + 3*sigma             (k=1, knowledge frame)

Then applies the verdict rule (PASS iff Syn_wit(b) >= tau_eff for EVERY b incl
r_top) under both estimators. Called shot for COPY: NULL/degenerate.

Prints JSON-ish machine-readable blocks plus human tables. No fabrication —
every number is computed live.
"""

from __future__ import annotations

import json

import numpy as np

import mdl_synergy as mdl
from cases import PREDICTED, build_case

CASE = "COPY"
A, B, M = build_case(CASE)
N = int(M.size)

print("=" * 80)
print(f"MEASURE AGENT — CASE = {CASE}  (predicted {PREDICTED[CASE]})")
print(f"shape {M.shape} {M.dtype} ; N={N} ; band={mdl.BAND} ; "
      f"r_floor={mdl.R_FLOOR} r_top={mdl.R_TOP}")
print(f"pinned compressor = {mdl.PINNED} (lzma preset {mdl.LZMA_PRESET})")
print("=" * 80)

# Sanity: COPY M should be ~A (degenerate copy of parent A with tiny noise).
print(f"\n[sanity] max|M - A| = {float(np.abs(M - A).max()):.6f} "
      f"(COPY = A + 0.001*noise, so should be ~3.5e-3 scale)")
print(f"[sanity] corr(M, A) = {np.corrcoef(M.ravel(), A.ravel())[0,1]:.8f}")
print(f"[sanity] corr(M, B) = {np.corrcoef(M.ravel(), B.ravel())[0,1]:.8f}")

# ---------------------------------------------------------------------------
# 1. Full band, all compressors, both estimators
# ---------------------------------------------------------------------------
all_sweeps = mdl.band_sweep_all_compressors(A, B, M)  # {comp: [BandRow,...]}

print("\n[1] FULL BAND — pinned lzma  (Syn_wit = L_b(R_AB) ; "
      "Syn_pid = min(L_b R_A, L_b R_B) - L_b R_AB):")
print(mdl.format_band_table(all_sweeps["lzma"]))

# machine-readable curves under pinned lzma
syn_wit_curve = [{"b": r.b, "syn_wit_bits": int(r.syn_wit)} for r in all_sweeps["lzma"]]
syn_pid_curve = [{"b": r.b, "syn_pid_bits": int(r.syn_pid)} for r in all_sweeps["lzma"]]

# ---------------------------------------------------------------------------
# 2. tau_eff calibration from the COPY null floor (this case IS the calibrator)
# ---------------------------------------------------------------------------
tau_eff, base_delta, sigma = mdl.compute_tau_eff(
    A, B, M, b=mdl.R_TOP, n_boot=200, seed=12345, compressor="lzma"
)
print("\n[2] NULL-FLOOR CALIBRATION (COPY @ r_top, k=1, knowledge frame) — LOCKED rule:")
print(f"  base_delta = Syn_wit(COPY @ r_top={mdl.R_TOP})  = {base_delta} bits  (the noise floor)")
print(f"  bootstrap sigma (n=200, seed=12345)            = {sigma:.6f} bits")
print(f"  tau_eff = base_delta + 3*sigma                 = {tau_eff:.6f} bits")

# ---------------------------------------------------------------------------
# 3. Verdict under BOTH estimators (apply tau_eff rule to each curve)
# ---------------------------------------------------------------------------
rows = all_sweeps["lzma"]

# WITNESSED verdict: PASS iff syn_wit(b) >= tau_eff for every b
passes_wit, per_b_wit = mdl.verdict_from_band(rows, tau_eff)
wit_verdict = "PASS" if passes_wit else "FAIL"

# PID verdict: apply the SAME tau_eff rule to the syn_pid curve, honestly.
# (PASS iff syn_pid(b) >= tau_eff for every b.)
per_b_pid = [(r.b, int(r.syn_pid), r.syn_pid >= tau_eff) for r in rows]
passes_pid = all(ok for _, _, ok in per_b_pid)
pid_verdict = "PASS" if passes_pid else "FAIL"

# Also note where syn_pid > 0 (the BES-4.4 "flags synergy" sign), regardless of tau.
pid_positive_any = any(r.syn_pid > 0 for r in rows)

print("\n[3] VERDICTS under tau_eff rule (>= tau_eff for ALL b incl r_top):")
print(f"  {'b':>3}  {'Syn_wit':>9}  {'wit>=tau':>9}  {'Syn_pid':>9}  {'pid>=tau':>9}")
for (b, sw, okw), (_, sp, okp) in zip(per_b_wit, per_b_pid):
    print(f"  {b:>3}  {sw:>9}  {str(okw):>9}  {sp:>9}  {str(okp):>9}")
print(f"  -> WITNESSED verdict (Syn_wit): {wit_verdict}")
print(f"  -> PID verdict (Syn_pid vs same tau): {pid_verdict}  "
      f"(any Syn_pid>0 down band: {pid_positive_any})")

rtop_row = [r for r in rows if r.b == mdl.R_TOP][0]
syn_wit_at_rtop = int(rtop_row.syn_wit)
syn_pid_at_rtop = int(rtop_row.syn_pid)

# ---------------------------------------------------------------------------
# 4. Error bars across compressors (full band, both estimators)
# ---------------------------------------------------------------------------
print("\n[4] COMPRESSOR ERROR BARS — Syn_wit (bits) across lzma/zlib/bz2, full band:")
print(f"    {'b':>3}  {'lzma':>9}  {'zlib':>9}  {'bz2':>9}  {'min':>9}  {'max':>9}  {'spread':>7}")
wit_spread_by_b = {}
for k, b in enumerate(mdl.BAND):
    vals = {c: all_sweeps[c][k].syn_wit for c in ("lzma", "zlib", "bz2")}
    lo, hi = min(vals.values()), max(vals.values())
    wit_spread_by_b[b] = (lo, hi, hi - lo)
    print(f"    {b:>3}  {vals['lzma']:>9}  {vals['zlib']:>9}  {vals['bz2']:>9}  "
          f"{lo:>9}  {hi:>9}  {hi-lo:>7}")

print("\n    Syn_pid (bits) across lzma/zlib/bz2, full band:")
print(f"    {'b':>3}  {'lzma':>9}  {'zlib':>9}  {'bz2':>9}  {'min':>9}  {'max':>9}  {'spread':>7}")
for k, b in enumerate(mdl.BAND):
    vals = {c: all_sweeps[c][k].syn_pid for c in ("lzma", "zlib", "bz2")}
    lo, hi = min(vals.values()), max(vals.values())
    print(f"    {b:>3}  {vals['lzma']:>9}  {vals['zlib']:>9}  {vals['bz2']:>9}  "
          f"{lo:>9}  {hi:>9}  {hi-lo:>7}")

# error bar at r_top specifically (the verdict resolution)
rtop_idx = mdl.BAND.index(mdl.R_TOP)
wit_rtop_vals = {c: all_sweeps[c][rtop_idx].syn_wit for c in ("lzma", "zlib", "bz2")}
pid_rtop_vals = {c: all_sweeps[c][rtop_idx].syn_pid for c in ("lzma", "zlib", "bz2")}

# ---------------------------------------------------------------------------
# 5. Machine-readable summary block for the structured output
# ---------------------------------------------------------------------------
summary = {
    "case": CASE,
    "predicted": PREDICTED[CASE],
    "ran": True,
    "N": N,
    "band": mdl.BAND,
    "r_top": mdl.R_TOP,
    "syn_wit_curve": syn_wit_curve,
    "syn_pid_curve": syn_pid_curve,
    "syn_wit_at_rtop": syn_wit_at_rtop,
    "syn_pid_at_rtop": syn_pid_at_rtop,
    "tau_eff": tau_eff,
    "base_delta_nullfloor": int(base_delta),
    "bootstrap_sigma": sigma,
    "wit_verdict": wit_verdict,
    "pid_verdict": pid_verdict,
    "pid_positive_any_b": bool(pid_positive_any),
    "wit_rtop_compressor_vals": wit_rtop_vals,
    "pid_rtop_compressor_vals": pid_rtop_vals,
    "wit_spread_by_b": {str(k): v for k, v in wit_spread_by_b.items()},
}
print("\n[5] MACHINE-READABLE SUMMARY (JSON):")
print(json.dumps(summary, indent=2))
print("\nDONE.")
