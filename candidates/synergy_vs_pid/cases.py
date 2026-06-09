"""cases.py -- the 6 controlled ground-truth cases for the synergy-vs-PID test.

Shape (256, 256) float32. Fixed seeds via numpy.random.default_rng:
    A     = default_rng(1).standard_normal
    B     = default_rng(2).standard_normal
    noise = default_rng(3).standard_normal
"*" below is ELEMENTWISE. The SAME A, B (seeds 1, 2) and noise (seed 3) are
reused across every case so the cases differ ONLY in the construction formula.

This is the 5-case frame-lock pilot set (SYN/ADD/ROT/COPY/ALLOY) PLUS XOR, the
canonical PID-synergy archetype, added here because the sharpened bar is a
synergy-gate-vs-plain-PID comparison and XOR is the case where PID synergy MUST
be high (each parent alone ~0 info about M; jointly they determine it).

  SYN   (witnessed PASS):  M = 0.5*A + 0.5*B + 0.5*(A*B) + 0.01*noise
                           genuine nonlinear interaction OUTSIDE the affine span.
  ADD   (witnessed FAIL):  M = 0.5*A + 0.5*B
                           pure additive blend, in the affine span. THE KEY
                           comparison: what does a PROPER PID say here?
  ROT   (witnessed FAIL):  M = cos(pi/5)*A + sin(pi/5)*B
                           still affine (a mixing rotation).
  COPY  (NULL calibrator): M = A + 0.001*noise
                           degenerate single-parent; calibrates the null floor.
  ALLOY (FAIL@r_top):      M = 0.5*A + 0.5*B + 0.1*(A*B)
                           small interaction: fine-scale synergy, coarse-scale
                           additive -> the FRAME-RELATIVITY demo across resolution.
  XOR   (witnessed PASS):  M = sign(A)*sign(B)  (values in {-1, +1})
                           canonical PID-synergy: each parent alone is ~0 info
                           about M, jointly they determine it. CALIBRATES the PID
                           estimator (PID synergy MUST be high here).

build_case(name) -> (A, B, M), all float32, all shape (256, 256).
"""

from __future__ import annotations

import numpy as np

SHAPE = (256, 256)
DTYPE = np.float32

CASE_NAMES = ["SYN", "ADD", "ROT", "COPY", "ALLOY", "XOR"]

# What the WITNESSED gate (non-additivity witness) is expected to call.
PREDICTED = {
    "SYN": "PASS",
    "ADD": "FAIL",          # pure additive blend -- witnessed FAIL is the headline
    "ROT": "FAIL",
    "COPY": "NULL",         # degenerate single parent (upstream parent-count gate)
    "ALLOY": "FAIL@r_top",  # fine-scale synergy, coarse-scale additive (frame-relative)
    "XOR": "PASS",          # canonical PID synergy -> witnessed PASS too
}


def _parents():
    A = np.random.default_rng(1).standard_normal(SHAPE).astype(DTYPE)
    B = np.random.default_rng(2).standard_normal(SHAPE).astype(DTYPE)
    noise = np.random.default_rng(3).standard_normal(SHAPE).astype(DTYPE)
    return A, B, noise


def build_case(name: str):
    """Return (A, B, M) for the named case with the EXACT seeds and formulas."""
    name = name.upper()
    A, B, noise = _parents()

    if name == "SYN":
        M = 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * noise
    elif name == "ADD":
        M = 0.5 * A + 0.5 * B
    elif name == "ROT":
        M = np.cos(np.pi / 5) * A + np.sin(np.pi / 5) * B
    elif name == "COPY":
        M = A + 0.001 * noise
    elif name == "ALLOY":
        M = 0.5 * A + 0.5 * B + 0.1 * (A * B)
    elif name == "XOR":
        # sign(A)*sign(B) as +/-1. np.sign maps the (measure-zero) exact-0 to 0;
        # standard_normal floats are never exactly 0, so M is in {-1,+1}.
        M = np.sign(A) * np.sign(B)
    else:
        raise ValueError(
            f"unknown case {name!r}; expected one of {CASE_NAMES}"
        )

    M = M.astype(DTYPE)
    return A, B, M


if __name__ == "__main__":
    for nm in CASE_NAMES:
        A, B, M = build_case(nm)
        assert A.shape == SHAPE == B.shape == M.shape
        assert A.dtype == B.dtype == M.dtype == DTYPE
        print(f"{nm:6s} predicted={PREDICTED[nm]:10s} "
              f"A[0,0]={A[0,0]:+.5f} B[0,0]={B[0,0]:+.5f} M[0,0]={M[0,0]:+.5f} "
              f"M.std={M.std():.4f}")
