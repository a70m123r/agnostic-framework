"""smoke.py — actually run the estimator and print REAL numbers.

Prints both estimators (witnessed P1 vs naive PID) for SYN and ADD at b=16
(r_floor) and b=3 (r_top); calibrates tau_eff from the COPY null per the LOCKED
rule; renders the full band + verdict for all 5 cases under the pinned lzma
compressor; reports normalized bits/element; shows the affine-floor contrast
(the honest diagnostic of where the witness separates and where it does not);
and reports zlib/bz2 sibling error bars at r_top.
"""

from __future__ import annotations

import mdl_synergy as mdl
from cases import CASE_NAMES, PREDICTED, build_case

print("=" * 80)
print("FRAME-LOCK dL PILOT - controlled ground truth, pinned compressor = lzma p6")
print("shape (256,256) float32 ; band =", mdl.BAND,
      "; r_floor =", mdl.R_FLOOR, "r_top =", mdl.R_TOP)
print("estimators: Syn_wit = L_b(R_AB)  |  Syn_pid = min(L_b(R_A),L_b(R_B)) - L_b(R_AB)")
print("residuals coded on M's own b-bit grid (see residual_codelength docstring)")
print("=" * 80)

# --- 1. the two headline cases at r_floor and r_top --------------------------
print("\n[1] Two estimators on SYN and ADD at b=16 (r_floor) and b=3 (r_top):\n")
print(f"  {'case':6s} {'b':>3}  {'Syn_wit (bits)':>15}  {'Syn_pid (bits)':>15}")
for nm in ["SYN", "ADD"]:
    A, B, M = build_case(nm)
    for b in (16, 3):
        sw = mdl.syn_wit(A, B, M, b)
        sp = mdl.syn_pid(A, B, M, b)
        print(f"  {nm:6s} {b:>3}  {sw:>15}  {sp:>15}")

# --- 2. calibrate tau_eff from COPY (the LOCKED lock-before-data rule) --------
cA, cB, cM = build_case("COPY")
tau_eff, base_delta, sigma = mdl.compute_tau_eff(cA, cB, cM, b=mdl.R_TOP,
                                                 n_boot=200, seed=12345)
print("\n[2] Null-floor calibration (COPY case, k=1, knowledge frame) - LOCKED rule:")
print(f"  base_delta = Syn_wit(COPY @ r_top={mdl.R_TOP}) = {base_delta} bits")
print(f"  bootstrap sigma (n=200)                     = {sigma:.3f} bits")
print(f"  tau_eff = base_delta + 3*sigma              = {tau_eff:.3f} bits")

# --- 3. full band + verdict for every case (Syn_wit) -------------------------
print("\n[3] Full band sweep (pinned lzma) + Syn_wit verdict (>= tau_eff for all b):")
sweeps = {}
for nm in CASE_NAMES:
    A, B, M = build_case(nm)
    rows = mdl.band_sweep(A, B, M)
    sweeps[nm] = rows
    passes, per_b = mdl.verdict_from_band(rows, tau_eff)
    print()
    print(mdl.format_band_table(
        rows, title=f"  --- {nm}  (predicted {PREDICTED[nm]}) ---"))
    wit_verdict = "PASS" if passes else "FAIL"
    rtop = [r for r in rows if r.b == mdl.R_TOP][0]
    print(f"     Syn_wit verdict (witnessed, all b >= tau_eff): {wit_verdict}"
          f"   | Syn_pid@r_top = {rtop.syn_pid} bits "
          f"({'>0 => PID flags SYNERGY' if rtop.syn_pid > 0 else '<=0'})")

# --- 4. HONEST diagnostic: contrast against the affine quantization floor -----
print("\n[4] Diagnostic - Syn_wit/element (bits/elem); ADD/ROT mark the affine")
print("    quantization-noise floor. Watch SYN & ALLOY vs that floor down the band:")
print(f"    {'b':>3} " + " ".join(f"{nm:>8}" for nm in CASE_NAMES))
for k, b in enumerate(mdl.BAND):
    row = " ".join(f"{sweeps[nm][k].syn_wit_per_elem:8.4f}" for nm in CASE_NAMES)
    print(f"    {b:>3} {row}")
print("    contrast DeltaWit = Syn_wit(case) - Syn_wit(ADD) [bits], per b:")
print(f"    {'b':>3} " + " ".join(f"{nm:>9}" for nm in CASE_NAMES))
for k, b in enumerate(mdl.BAND):
    floor = sweeps['ADD'][k].syn_wit
    row = " ".join(f"{sweeps[nm][k].syn_wit - floor:9d}" for nm in CASE_NAMES)
    print(f"    {b:>3} {row}")

# --- 5. sibling-compressor error bars at r_top -------------------------------
print("\n[5] Compressor error bars at r_top (Syn_wit bits): lzma(pinned)/zlib/bz2")
print(f"    {'case':6s} {'lzma':>9} {'zlib':>9} {'bz2':>9}")
for nm in CASE_NAMES:
    A, B, M = build_case(nm)
    vals = {c: mdl.syn_wit(A, B, M, mdl.R_TOP, compressor=c)
            for c in ("lzma", "zlib", "bz2")}
    print(f"    {nm:6s} {vals['lzma']:>9} {vals['zlib']:>9} {vals['bz2']:>9}")

print("\n" + "=" * 80)
print("DONE.")
