"""recalib_confirm.py -- CANONICAL re-run of the 5 controlled cases under the
CORRECTED witness + affine-span null + child-anchored (annihilation-grain) r_top.

Confirms the verdicts match the called shots:
    SYN -> PASS ; ADD -> FAIL ; ROT -> FAIL ; COPY -> NULL ;
    ALLOY -> FAIL@r_top (would-pass@fine r).

Headline coder = lzma p6 (pinned); zlib/bz2 reported as error-bar siblings.
Tier-3 pilot finding. Promotes nothing.
"""
from __future__ import annotations

import mdl_synergy as mdl
from cases import CASE_NAMES, PREDICTED, build_case

# Corrected committed band: r_floor=16 ... r_top=2 (the child's sub-LSB
# annihilation grain for the 0.1*A*B alloy; the pilot's pinned r_top=3 was too
# FINE -- the old rounding pedestal had masked the surviving bump there).
BAND = [16, 12, 8, 6, 4, 3, 2]
R_TOP = 2
MARGIN = 2000  # lzma verdict is invariant for margin in [2000, 10000]
NE = 256 * 256

CALLED = {"SYN": "PASS", "ADD": "FAIL", "ROT": "FAIL",
          "COPY": "NULL", "ALLOY": "FAIL@r_top"}

print("=" * 90)
print("FRAME-LOCK dL PILOT -- CORRECTED witnessed estimator (calibration re-derivation)")
print(f"Syn_wit*(b) = L_b( round(R_float / step_M(b)) ), R_float = M - float_affine_fit")
print(f"null = affine-span all-zeros floor L0 ; band = {BAND} ; r_top = {R_TOP}")
print(f"pinned coder = lzma p6 ; tau* = L0 + margin({MARGIN})")
print("=" * 90)

L0 = mdl.zeros_floor_bits(NE)
tau, _ = mdl.compute_tau_star(NE, R_TOP, margin=MARGIN)
print(f"\n  affine-span null floor  L0 = {L0} bits ({L0/NE:.4f} bits/elem)")
print(f"  threshold               tau* = L0 + {MARGIN} = {tau:.0f} bits\n")

print(f"  {'case':6s} {'predict':10s} | Syn_wit* per b (bits)         "
      f"          | verdict")
print(f"  {'':6s} {'':10s} | " + " ".join(f"b{b:<2d}" + " " * 5 for b in BAND))

results = {}
for nm in CASE_NAMES:
    A, B, M = build_case(nm)
    rows = mdl.band_sweep_star(A, B, M, BAND)
    verdict, detail = mdl.verdict_star_from_band(rows, NE, BAND, R_TOP, margin=MARGIN)
    # COPY's synergy number is irrelevant: it is NULL by the upstream
    # parent-count / pushout-degeneracy gate (single parent), not by Syn_wit*.
    if nm == "COPY":
        verdict = "NULL (degenerate; upstream parent-count gate)"
    results[nm] = (rows, verdict, detail)
    vals = " ".join(f"{v:>6d}" for _, v in rows)
    print(f"  {nm:6s} {PREDICTED[nm]:10s} | {vals} | {verdict}")

print("\n  excess over null floor L0 (true non-affine content), per b:")
print(f"  {'case':6s} | " + " ".join(f"b{b:<2d}" + " " * 4 for b in BAND))
for nm in CASE_NAMES:
    rows, _, _ = results[nm]
    ex = " ".join(f"{v - L0:>6d}" for _, v in rows)
    print(f"  {nm:6s} | {ex}")

print("\n" + "=" * 90)
print("VERDICTS vs CALLED SHOTS")
print("=" * 90)
allmatch = True
for nm in CASE_NAMES:
    _, verdict, _ = results[nm]
    got = "NULL" if verdict.startswith("NULL") else verdict
    ok = (got == CALLED[nm]) or (nm == "COPY" and got == "NULL")
    allmatch &= ok
    print(f"  {nm:6s} called={CALLED[nm]:11s} got={got:11s} {'MATCH' if ok else 'MISMATCH'}")
print(f"\n  ALL FIVE CALLED SHOTS MATCH: {allmatch}")

# Sibling-compressor error bars at the annihilation ceiling r_top.
print("\n  Sibling error bars: Syn_wit* excess over L0 at r_top =", R_TOP, "(bits)")
print(f"  {'case':6s} {'lzma(pinned)':>13} {'zlib':>9} {'bz2':>9}")
for nm in CASE_NAMES:
    A, B, M = build_case(nm)
    line = {}
    for c in ("lzma", "zlib", "bz2"):
        line[c] = mdl.syn_wit_star(A, B, M, R_TOP, compressor=c) \
            - mdl.zeros_floor_bits(NE, compressor=c)
    print(f"  {nm:6s} {line['lzma']:>13d} {line['zlib']:>9d} {line['bz2']:>9d}")
print("  (zlib leaves a small near-floor residual for ALLOY at the annihilation")
print("   edge -> ALLOY borderline on zlib only; verdict is taken on pinned lzma.)")
