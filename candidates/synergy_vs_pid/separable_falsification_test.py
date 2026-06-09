# Separable-nonlinearity falsification test for the witnessed (affine-residual) synergy gate.
# Proposed by Gemini in the 2026-06-09 cross-model pass: "the gate erroneously flags
# independent non-linear transformations as synergistic emergence even when no interaction
# between parents occurs" -> test M = A^2 + B^2.
#
# Replicates the affine-residual core of witnessed_synergy.py (M minus best least-squares
# affine fit aA+bB+c, residual coded on M's b-bit grid, lzma codelength, excess over the
# all-zeros floor). The qualitative result is independent of compressor/quantization detail:
# A^2 is fundamentally outside the affine span of A, so a separable nonlinear sum f(A)+g(B)
# leaves a large residual under an AFFINE quotient.
#
# RESULT (b=16, seeds A=rng(1), B=rng(2)):
#   ADD  0.5A+0.5B            (affine, no interaction)            excess =        0   correctly floored
#   SYN  0.5A+0.5B+0.5*A*B    (genuine A*B interaction)           excess =  981,024   flagged
#   INT  A*B                  (pure interaction)                  excess = 1,009,536  flagged
#   SEP  A^2 + B^2            (separable nonlinear, NO interaction) excess = 1,040,352 FLAGGED (higher than INT!)
#   SEP3 A^3 + B^3            (separable nonlinear, NO interaction) excess =  866,944  FLAGGED
#
# VERDICT: bug CONFIRMED. The affine-residual gate measures NON-AFFINITY, which conflates a
# genuine joint A*B interaction with each parent transformed nonlinearly and then added (no
# interaction at all). The fix: quotient out the best SEPARABLE additive model f(A)+g(B)
# (arbitrary, possibly nonlinear f,g) -- i.e. measure the functional-ANOVA INTERACTION term
# h(A,B) -- which floors A^2+B^2 by construction. "Additive blend" must mean SEPARABLE, not
# merely AFFINE.

import numpy as np, lzma

A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float32)
B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float32)

def affine_resid(M):
    X = np.column_stack([A.ravel(), B.ravel(), np.ones(A.size)])
    c, _, _, _ = np.linalg.lstsq(X, M.ravel(), rcond=None)
    return M - (X @ c).reshape(M.shape)

def clen(ints):
    return 8 * len(lzma.compress(np.ascontiguousarray(ints).astype('<i4').tobytes(), preset=6))

def excess(M, b=16):
    R = affine_resid(M)
    step = (M.max() - M.min()) / (2 ** b - 1)
    codes = np.round(R / step).astype(np.int64)
    return clen(codes) - clen(np.zeros_like(codes))

if __name__ == "__main__":
    cases = {
        "ADD  0.5A+0.5B            (affine, no interaction)": 0.5 * A + 0.5 * B,
        "SYN  0.5A+0.5B+0.5*A*B    (genuine A*B interaction)": 0.5 * A + 0.5 * B + 0.5 * (A * B),
        "INT  A*B                  (pure interaction)": A * B,
        "SEP  A^2 + B^2            (separable, NO interaction)": A * A + B * B,
        "SEP3 A^3 + B^3            (separable, NO interaction)": A ** 3 + B ** 3,
    }
    print("witnessed-gate excess over floor (bits), affine-residual @ b=16:")
    for k, M in cases.items():
        print(f"  {k:52s} excess = {excess(M):>10d}")
