"""
cases.py — the 5 controlled ground-truth cases for the frame-lock ΔL pilot.

Shape (256, 256) float32. Fixed seeds via numpy.random.default_rng:
    A     = default_rng(1).standard_normal
    B     = default_rng(2).standard_normal
    noise = default_rng(3).standard_normal
"*" below is ELEMENTWISE.

  SYN   (predict PASS):  M = 0.5*A + 0.5*B + 0.5*(A*B) + 0.01*noise
                         elementwise product = a real nonlinear interaction
                         OUTSIDE the affine span.
  ADD   (predict FAIL):  M = 0.5*A + 0.5*B
                         purely additive, in the affine span.
  ROT   (predict FAIL):  M = cos(pi/5)*A + sin(pi/5)*B
                         still affine (the coupled-plate mixing angle).
  COPY  (predict NULL):  M = A + 0.001*noise
                         degenerate; CALIBRATES the null / noise floor.
  ALLOY (predict FAIL @ r_top, would-pass @ fine r):
                         M = 0.5*A + 0.5*B + 0.1*(A*B)
                         small-amplitude interaction that coarse quantization
                         at the child-anchored ceiling annihilates (P3b).

build_case(name) -> (A, B, M), all float32, all shape (256, 256).
The SAME A, B (seeds 1, 2) and noise (seed 3) are reused across every case so
the cases differ ONLY in the construction formula.
"""

from __future__ import annotations

import numpy as np

SHAPE = (256, 256)
DTYPE = np.float32

CASE_NAMES = ["SYN", "ADD", "ROT", "COPY", "ALLOY"]

PREDICTED = {
    "SYN": "PASS",
    "ADD": "FAIL",
    "ROT": "FAIL",
    "COPY": "NULL",          # calibrates the null floor
    "ALLOY": "FAIL@r_top",   # would-pass at fine r, FAIL at coarse ceiling (P3b)
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
    else:
        raise ValueError(
            f"unknown case {name!r}; expected one of {CASE_NAMES}"
        )

    M = M.astype(DTYPE)
    return A, B, M


if __name__ == "__main__":
    # quick self-check: shapes, dtypes, and that the parents are shared
    for nm in CASE_NAMES:
        A, B, M = build_case(nm)
        assert A.shape == SHAPE == B.shape == M.shape
        assert A.dtype == B.dtype == M.dtype == DTYPE
        print(f"{nm:6s} predicted={PREDICTED[nm]:10s} "
              f"A[0,0]={A[0,0]:+.5f} B[0,0]={B[0,0]:+.5f} M[0,0]={M[0,0]:+.5f} "
              f"M.std={M.std():.4f}")
