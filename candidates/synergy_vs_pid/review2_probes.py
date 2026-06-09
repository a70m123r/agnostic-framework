"""review2_probes.py -- SECOND-PASS reviewer adversarial probes (Fable pass).

NEW file; touches nothing committed. Pure numpy + the two calibrated measures.
Probes:
  P1  Taylor-law claim audit at a0=2: recompute Pearson r of measured gain vs
      (a) the uniform h^2/3 law printed by contextual_frame_test.py and
      (b) the EXACT empirical law rho = Var(A|band) / (E[A|band]^2 + Var(A|band))
      plus per-band measured/law ratios. (The first pass reported r=1.0000.)
  P2  Floor frame-INVARIANCE: SEP=A^2+B^2 and ADD under the same a0=2 band
      narrowing. Separability is closed under sub-population restriction, so the
      floor verdict must NOT flip in any band. If it did, the Phase-2 "flip"
      would be suspect (anything-moves-under-framing artifact).
  P3  Noise confound: M = 0.5A+0.5B+0.5*noise (NO interaction, big irreducible
      noise). gam_interaction_frac counts noise as residual -> expect FALSE-HIGH;
      predictive gain differences it out -> expect ~0. Structural discriminator
      between candidate #1 and #4.
  P4  Correlated parents (model-merge substrate realism; calibration battery is
      all-independent): Bc = r*A + sqrt(1-r^2)*B at r=0.9. SEPc/ADDc must floor,
      INTc must flag, on both measures.
  P5  Variance-only interaction (scope limit of mean-based gates):
      M = A + B + (1+0.9*sign(A)*sign(B))*noise. Conditional MEAN is separable;
      the joint structure lives in the conditional VARIANCE. Expect both
      mean-based measures ~0 (a documented blind spot, not a bug).
"""
from __future__ import annotations

import numpy as np

from cand_predictive_gain import predictive_gain
from cand_gam_anova import gam_interaction_frac


def field():
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float64).ravel()
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float64).ravel()
    n = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float64).ravel()
    return A, B, n


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1])


if __name__ == "__main__":
    A, B, n = field()
    M_int = A * B

    # ---------------- P1: Taylor-law audit at a0 = 2 ----------------
    print("=" * 88)
    print("P1  Taylor-law audit, a0=2 bands (measured gain vs uniform-law vs EXACT empirical law)")
    print("=" * 88)
    a0 = 2.0
    bands = (3.0, 1.5, 1.0, 0.6, 0.3, 0.15)
    meas, law_unif, law_exact = [], [], []
    print(f"{'h':>5} {'gain_meas':>10} {'rho_unif':>9} {'rho_exact':>10} {'meas/unif':>10} {'meas/exact':>11}")
    for h in bands:
        idx = np.flatnonzero(np.abs(A - a0) <= h)
        g = predictive_gain(A[idx], B[idx], M_int[idx], bins=8).gain_r2
        var_d_unif = h * h / 3.0
        r_unif = var_d_unif / (a0 * a0 + var_d_unif)
        abar = A[idx].mean()
        vA = A[idx].var()
        r_exact = vA / (abar * abar + vA)
        meas.append(g); law_unif.append(r_unif); law_exact.append(r_exact)
        print(f"{h:>5.2f} {g:>10.4f} {r_unif:>9.4f} {r_exact:>10.4f} "
              f"{g / r_unif:>10.3f} {g / r_exact:>11.3f}")
    print(f"  Pearson r (measured, uniform h^2/3 law) = {pearson(meas, law_unif):.6f}")
    print(f"  Pearson r (measured, EXACT empirical law) = {pearson(meas, law_exact):.6f}")
    print(f"  Pearson r on LOG values (exact law)        = "
          f"{pearson(np.log(meas), np.log(law_exact)):.6f}")

    # ---------------- P2: floor frame-invariance under the same framing ----------------
    print()
    print("=" * 88)
    print("P2  Floor frame-INVARIANCE: SEP=A^2+B^2 and ADD under the same a0=2 bands")
    print("    (separable must stay floored in EVERY frame; flip would impeach Phase-2)")
    print("=" * 88)
    M_sep = A * A + B * B
    M_add = 0.5 * A + 0.5 * B
    print(f"{'h':>5} {'n':>7} {'gain_SEP':>10} {'gain_ADD':>10} {'gamfrac_SEP':>12} {'gamfrac_ADD':>12}")
    for h in bands:
        idx = np.flatnonzero(np.abs(A - a0) <= h)
        gs = predictive_gain(A[idx], B[idx], M_sep[idx], bins=8).gain_r2
        ga = predictive_gain(A[idx], B[idx], M_add[idx], bins=8).gain_r2
        fs = gam_interaction_frac(A[idx], B[idx], M_sep[idx], n_interior=8)
        fa = gam_interaction_frac(A[idx], B[idx], M_add[idx], n_interior=8)
        print(f"{h:>5.2f} {idx.size:>7d} {gs:>10.5f} {ga:>10.5f} {fs:>12.5f} {fa:>12.5f}")

    # ---------------- P3: irreducible-noise confound ----------------
    print()
    print("=" * 88)
    print("P3  Noise confound  M = 0.5A+0.5B+0.5*noise  (ZERO interaction, noise share=1/3)")
    print("    gam frac counts noise as 'interaction'; predictive gain must not.")
    print("=" * 88)
    M_noisy = 0.5 * A + 0.5 * B + 0.5 * n
    r = predictive_gain(A, B, M_noisy, bins=8)
    f = gam_interaction_frac(A, B, M_noisy, n_interior=8)
    print(f"  gam_interaction_frac = {f:.4f}   (false-HIGH expected ~0.33)")
    print(f"  predictive gain_R2   = {r.gain_r2:+.5f}  (R2_add={r.r2_add:.4f} R2_joint={r.r2_joint:.4f})")

    # ---------------- P4: correlated parents ----------------
    print()
    print("=" * 88)
    print("P4  Correlated parents r=0.9 (merge-substrate realism): Bc=0.9A+sqrt(0.19)B")
    print("=" * 88)
    rho = 0.9
    Bc = rho * A + np.sqrt(1 - rho * rho) * B
    cases = [
        ("ADDc 0.5A+0.5Bc  (floor)", 0.5 * A + 0.5 * Bc),
        ("SEPc A^2+Bc^2    (floor)", A * A + Bc * Bc),
        ("INTc A*Bc        (flag)",  A * Bc),
    ]
    print(f"  corr(A,Bc) = {pearson(A, Bc):+.4f}")
    print(f"{'case':<28} {'gain_R2':>10} {'R2_add':>8} {'R2_joint':>9} {'gamfrac':>9}")
    for lbl, M in cases:
        r = predictive_gain(A, Bc, M, bins=8)
        f = gam_interaction_frac(A, Bc, M, n_interior=8)
        print(f"  {lbl:<28} {r.gain_r2:>10.5f} {r.r2_add:>8.4f} {r.r2_joint:>9.4f} {f:>9.4f}")
    # decomposition note for INTc: A*Bc = 0.9A^2 + sqrt(0.19)A*B ->
    # separable share Var(0.9A^2)~2*0.81 vs cross share 0.19*Var(AB)~0.19
    v_sep = np.var(rho * A * A)
    v_x = np.var(np.sqrt(1 - rho * rho) * A * B)
    print(f"  (INTc ground truth: separable-part var={v_sep:.3f}, cross-part var={v_x:.3f}, "
          f"cross share={v_x / (v_sep + v_x):.3f} -> a LOW-ish gain is CORRECT here)")

    # ---------------- P5: variance-only interaction ----------------
    print()
    print("=" * 88)
    print("P5  Variance-only interaction  M = A+B+(1+0.9*sign(A)*sign(B))*noise")
    print("    mean-separable, jointly heteroscedastic: mean-based gates expect ~0 (blind spot)")
    print("=" * 88)
    M_var = A + B + (1.0 + 0.9 * np.sign(A) * np.sign(B)) * n
    r = predictive_gain(A, B, M_var, bins=8)
    f = gam_interaction_frac(A, B, M_var, n_interior=8)
    print(f"  predictive gain_R2   = {r.gain_r2:+.5f}  (R2_add={r.r2_add:.4f} R2_joint={r.r2_joint:.4f})")
    print(f"  gam_interaction_frac = {f:.4f}")
    # ground truth: Var(noise term | signs agree)=3.61 vs disagree=0.01 -> strong joint structure
    print("  (ground truth: conditional noise SD is 1.9 when sign(A)=sign(B), 0.1 otherwise --")
    print("   genuine joint structure, invisible to conditional-MEAN measures.)")
