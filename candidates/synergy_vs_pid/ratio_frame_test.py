# Ratio frame-relativity test (2026-06-09).
# Motivated by agnostic_units_hairy_membrane_SKETCH.md §6: the cross-model called the gate's
# frame-relativity a "quantization artifact" -- but it judged the ABSOLUTE grid-codelength.
# A dimensionless RATIO cancels the grid-bits. Does frame-relativity survive as a ratio?
#
# interaction-fraction = Var(interaction)/Var(M), interaction = M minus its best SEPARABLE
# polynomial main-effects fit f(A)+g(B) (deg 3, NO cross terms -> floors any separable incl
# A^2+B^2), on data quantized to b bits, swept across the band. Dimensionless -> grid-bits cancel.
#
# RESULT: at FINE b (>=8) clean, FLAT (frame-stable), bug-fixed (separable -> 0, interaction
# flagged). At COARSE b (<=4) everything blows up incl separable (ADD->0.51, SEP->0.88) =
# underpowered-fit artifact. So frame-relativity does NOT survive as a genuine signal -- flat
# where clean, artifact where it varies. (Cross-model: confirmed artifact; caveat -- this only
# kills the RESOLUTION proxy, not the broader observer-kernel frame-relativity; and residual-
# variance-as-interaction confounds genuine interaction with main-effect model misspecification.)

import numpy as np

A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float64)
B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float64)
n = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float64)

def q(X, b):
    lo, hi = X.min(), X.max()
    step = (hi - lo) / (2 ** b - 1) if hi > lo else 1.0
    return np.round((X - lo) / step) * step + lo

def interaction_varfrac(M, b, deg=3):
    Aq, Bq, Mq = q(A, b).ravel(), q(B, b).ravel(), q(M, b).ravel()
    cols = [np.ones_like(Aq)]
    for k in range(1, deg + 1): cols.append(Aq ** k)
    for k in range(1, deg + 1): cols.append(Bq ** k)
    X = np.column_stack(cols)
    X = (X - X.mean(0)) / (X.std(0) + 1e-12); X[:, 0] = 1.0
    c, _, _, _ = np.linalg.lstsq(X, Mq, rcond=None)
    resid = Mq - X @ c
    v = Mq.var()
    return resid.var() / v if v > 0 else 0.0

cases = {
    "SYN   0.5A+0.5B+0.5*A*B  (large interaction)": 0.5 * A + 0.5 * B + 0.5 * (A * B) + 0.01 * n,
    "ADD   0.5A+0.5B          (separable/affine)":  0.5 * A + 0.5 * B,
    "SEP   A^2+B^2            (separable nonlin)":   A * A + B * B,
    "INT   A*B                (pure interaction)":   A * B,
    "ALLOY 0.5A+0.5B+0.1*A*B  (small interaction)":  0.5 * A + 0.5 * B + 0.1 * (A * B),
}
band = [16, 12, 10, 8, 6, 5, 4, 3, 2]
if __name__ == "__main__":
    print("INTERACTION-FRACTION (dimensionless) across resolution b  [grid-bits cancel]")
    print("case                                          " + " ".join(f"b={b:>2}" for b in band))
    for name, M in cases.items():
        print(f"{name:46s} " + " ".join(f"{interaction_varfrac(M, b):5.3f}" for b in band))
