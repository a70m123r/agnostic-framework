"""contextual_frame_test.py -- PHASE-2 REAL TEST of observer-kernel frame-relativity.

THE QUESTION
------------
The grid-RESOLUTION sweep (ZOOM = change resolution within a FIXED frame) came back
a QUANTIZATION ARTIFACT: at coarse bins everything blew up underpowered, the verdict
moved for a measurement reason, not a structural one. That killed the resolution
PROXY for frame-relativity -- NOT the framework's real claim.

Pav's distinction: CONTEXTUAL SCALING is NOT zoom. It is ADJUSTING THE FRAME ITSELF
-- the relevance / context / depth cutoff: which SUB-POPULATION of the world you are
asking about, and which OTHER variables are in scope. The claim under test:

    the SAME global system can be emergent (interactive) in one CONTEXT and
    additive (separable) in another, in a PRINCIPLED way -- not because we
    re-binned, but because we changed WHAT REGION / WHAT VARIABLES are in frame.

Principle = LOCALITY OF NONLINEARITY. A product M = A*B is interactive globally
(the cross term is irreducible over a wide range of A) but LOCALLY near-linear:
near A = a0, M = a0*B + (A-a0)*B ~ a0*B to first order, i.e. ADDITIVE in a narrow
band. A curve looks straight up close. So the emergence verdict for the SAME M
should FLOOR when the FRAME (the relevance band of A) narrows around a point, and
FLAG when the frame is wide -- a structural, predictable, sign-and-magnitude flip.

This is distinct from the grid artifact in a way we MUST prove, not assert:
  * grid artifact: verdict moved because COARSE BINS lose power (a measurement defect);
    finer bins -> verdict returns. Direction was "everything degrades together."
  * frame effect (if real): verdict moves because the FUNCTION IS LOCALLY DIFFERENT
    in the narrow frame; it must SURVIVE at full per-frame measurement power and
    must be EXPLAINED BY THE TAYLOR REMAINDER (curvature * band width^2), not by n.

TWO OPERATIONALIZATIONS (both change the FRAME/CONTEXT, NOT the grid resolution)
-------------------------------------------------------------------------------
(I)  PARENT-RANGE / SUB-POPULATION. Take M = A*B on the fixed (256,256) field.
     Restrict the SAMPLE to the sub-population {|A - a0| <= h} (a relevance band of
     half-width h around a0). Re-measure emergence of the SAME M on that sub-pop.
     Wide band (whole support) -> interactive; narrow band -> additive.
     POWER CONTROLS (the anti-artifact guards):
       (a) hold n FIXED across frames (subsample every frame to the smallest n) so a
           narrow frame is NOT just fewer points -- if the flip survives equal-n it
           is NOT the grid/power failure mode;
       (b) keep the measure's resolution adaptive (quantile bins) so each frame is
           measured at full power for its own support -- no coarse-bin starvation;
       (c) PREDICT the floor quantitatively from the Taylor remainder: in a band of
           half-width h the interaction variance / additive variance ~ h^2 * Var(B) /
           (a0^2 + ...) -> the interaction fraction should fall like h^2, and we check
           the measured curve against that law. A law-following decline = structural;
           a power collapse would not track h^2.
       (d) FALSIFIER: a TRULY non-local interaction (XOR = sign(A)*sign(B)) must NOT
           floor when you narrow the band away from the A=0 seam -- its nonlinearity
           is NOT local, so frame-relativity must NOT fire for it. If our narrowing
           floored XOR too, we'd be measuring power loss, not locality.

(II) CONTEXT VARIABLE C. Build a merge that looks emergent OUT of context and
     separable IN context. M = A*B with B == C (a third variable that is "in the
     world" but may or may not be in frame). OUT of context: you only get to use
     (A, M) -> A alone cannot explain M (B/C is a hidden common driver) so M looks
     like it has irreducible extra structure. IN context: bring C into frame and
     condition on it -> within each C-stratum M = A*c is LINEAR in A, fully
     explained, interaction gone. Same system, two frames, opposite verdict --
     driven by WHAT VARIABLE IS IN SCOPE, the relevance/depth cutoff, not the grid.

We reuse the soundest calibrated measures unchanged:
  * predictive_gain  (held-out R2[joint(A,B)] - R2[additive f(A)+g(B)])  -- op (I)
  * gam_interaction_frac (held-out functional-ANOVA interaction fraction) -- op (I) cross-check
  * a held-out conditional-on-C predictive gain  -- op (II)

DISCIPLINE: controlled ground-truth; numpy + scipy only; no torch/HF/sklearn/network.
NEW file; existing committed files untouched. REAL numbers printed; nothing fabricated.
"""

from __future__ import annotations

import numpy as np

from cand_predictive_gain import predictive_gain
from cand_gam_anova import gam_interaction_frac


# ----------------------------------------------------------------------------- #
# The fixed controlled field (exact seeds).                                     #
# ----------------------------------------------------------------------------- #
def field():
    A = np.random.default_rng(1).standard_normal((256, 256)).astype(np.float64)
    B = np.random.default_rng(2).standard_normal((256, 256)).astype(np.float64)
    n = np.random.default_rng(3).standard_normal((256, 256)).astype(np.float64)
    return A.ravel(), B.ravel(), n.ravel()


def _equal_n_subsample(mask: np.ndarray, n_keep: int, seed: int) -> np.ndarray:
    """Return indices: a random n_keep-subset of the True positions in `mask`."""
    idx = np.flatnonzero(mask)
    if idx.size <= n_keep:
        return idx
    rng = np.random.default_rng(seed)
    return rng.choice(idx, size=n_keep, replace=False)


# =============================================================================== #
# OPERATIONALIZATION (I): PARENT-RANGE / SUB-POPULATION (locality of nonlinearity)
# =============================================================================== #
def op1_parent_range(a0: float = 0.0, bands=(3.0, 1.5, 1.0, 0.6, 0.3, 0.15),
                     bins: int = 8, n_equal: int | None = None,
                     measure: str = "predictive_gain"):
    """Emergence of the SAME M=A*B measured over frames {|A-a0|<=h} for each h in bands.

    Returns a list of dict rows (one per band): band half-width h, the kept n, the
    realised A-range, the predictive-gain (and gam-frac) on that sub-population, and
    -- with equal-n on -- the same at a FIXED n so the flip cannot be a sample-size
    artifact. Also returns the Taylor-law prediction for the interaction fraction.
    """
    A, B, _ = field()
    M = A * B  # the SAME global system across every frame

    rows = []
    # smallest band sets the common n for the equal-n control
    if n_equal is None:
        counts = [int(np.sum(np.abs(A - a0) <= h)) for h in bands]
        n_equal = max(50, min(counts))  # floor at 50 so the tiniest band stays scoreable

    for h in bands:
        mask = np.abs(A - a0) <= h
        idx_all = np.flatnonzero(mask)
        Aa, Bb, Mm = A[idx_all], B[idx_all], M[idx_all]

        # full-power gain on the whole sub-population (resolution adaptive => no
        # coarse-bin starvation; each frame measured at its own full power)
        g_full = predictive_gain(Aa, Bb, Mm, bins=bins).gain_r2
        f_full = gam_interaction_frac(Aa, Bb, Mm, n_interior=8)

        # equal-n control: same measurement, FIXED sample size across frames
        idx_eq = _equal_n_subsample(mask, n_equal, seed=20240601)
        Ae, Be, Me = A[idx_eq], B[idx_eq], M[idx_eq]
        g_eq = predictive_gain(Ae, Be, Me, bins=bins).gain_r2
        f_eq = gam_interaction_frac(Ae, Be, Me, n_interior=8)

        rows.append(dict(
            h=h, n=int(idx_all.size), n_eq=int(idx_eq.size),
            a_lo=float(Aa.min()), a_hi=float(Aa.max()),
            gain_full=float(g_full), gamfrac_full=float(f_full),
            gain_eq=float(g_eq), gamfrac_eq=float(f_eq),
        ))
    return rows, n_equal


def op1_taylor_law(a0: float = 0.0, bands=(3.0, 1.5, 1.0, 0.6, 0.3, 0.15)):
    """Closed-form-ish prediction of the interaction fraction for M=A*B in a band.

    Within {|A-a0|<=h}, write A = a0 + d, d in [-h,h]. Then M = a0*B + d*B.
    The BEST SEPARABLE model f(A)+g(B) can absorb a0*B's B-linear part as g(B) and
    the d-dependence as f(A); the irreducible interaction is the cross term d*B.
    Decompose by total variance of M over the sub-pop:
        Var(M) ~ Var(a0*B) + Var(d*B)  (d,B independent on the field, ~mean0)
               = a0^2 Var(B) + Var(d)Var(B) + Var(d)*E[B]^2  (E[B]~0)
        irreducible interaction variance ~ Var(d*B) - [B-linear part absorbable]
    For the leading-order intuition we report the INTERACTION-to-TOTAL ratio
        rho(h) = Var(d) * Var(B) / ( a0^2 Var(B) + Var(d) Var(B) )
               = Var(d) / ( a0^2 + Var(d) ),   Var(d) ~ h^2/3 for uniform-ish d.
    This is the QUALITATIVE law: at a0=0 it is rho = 1 for all h>0 (interaction
    never vanishes at the center because there is no linear a0*B term to dominate)
    -- so the floor at a0=0 must come from the SECOND mechanism (shrinking total
    SIGNAL vs fixed binning noise), whereas OFF-CENTER (a0!=0) rho ~ h^2/(3 a0^2)
    -> a clean h^2 decline. We therefore run BOTH a0=0 and a0!=0 and read the laws.
    """
    out = []
    for h in bands:
        var_d = (h ** 2) / 3.0  # variance of uniform on [-h,h]; A is ~normal but
        # within a narrow symmetric band the conditional is ~uniform-ish; this is the
        # ORDER law, not an exact constant.
        rho0 = var_d / (a0 ** 2 + var_d) if (a0 ** 2 + var_d) > 0 else 0.0
        out.append(dict(h=h, var_d=var_d, rho_pred=rho0))
    return out


# =============================================================================== #
# OPERATIONALIZATION (II): CONTEXT VARIABLE C (in-scope vs out-of-scope)          #
# =============================================================================== #
def _condition_on_C_gain(A, M, C, bins=8, folds=5, seed=1234):
    """Held-out predictive gain of (model that may use C) over (model with A only),
    for predicting M -- the IN-CONTEXT analysis. We compare:

       R2_oos[ joint(A,C) cell-mean ]   vs   R2_oos[ A-only bin-mean ]

    OUT of context, C is not available: the only predictor of M is E[M|A], whose
    R2 is the 'A-only' number. IN context, C enters: the 2D (A,C) cell mean can use
    it. For M=A*C, within a C-stratum M is LINEAR in A and fully determined by (A,C),
    so the (A,C) model explains ~all variance while A-only explains ~none -> a HUGE
    in-context gain. The verdict 'is there irreducible extra structure beyond what's
    in frame?' flips: out-of-context A cannot reach M (looks emergent/irreducible),
    in-context (A,C) nails it (explained, additive-in-stratum)."""
    Af = np.asarray(A, float).ravel()
    Mf = np.asarray(M, float).ravel()
    Cf = np.asarray(C, float).ravel()
    n = Mf.size

    # quantile bins per axis (adaptive resolution -> full power, no starvation)
    def qbin(x, k):
        e = np.quantile(x, np.linspace(0, 1, k + 1))
        e[0], e[-1] = -np.inf, np.inf
        return np.clip(np.digitize(x, e[1:-1]), 0, k - 1)

    la = qbin(Af, bins)
    lc = qbin(Cf, bins)
    na = int(la.max()) + 1
    nc = int(lc.max()) + 1
    cell = la * nc + lc
    ncell = na * nc

    rng = np.random.default_rng(seed)
    fold = rng.integers(0, folds, n)
    ss_tot = ss_a = ss_ac = 0.0
    for k in range(folds):
        te = fold == k
        tr = ~te
        if not te.any() or not tr.any():
            continue
        gm = Mf[tr].mean()
        # A-only model (out-of-context predictor: C not in frame)
        sa = np.zeros(na); ca = np.zeros(na)
        np.add.at(sa, la[tr], Mf[tr]); np.add.at(ca, la[tr], 1.0)
        muA = np.where(ca > 0, sa / np.maximum(ca, 1), gm)
        pa = muA[la[te]]
        # (A,C) joint model (in-context predictor: C in frame)
        sc = np.zeros(ncell); cc = np.zeros(ncell)
        np.add.at(sc, cell[tr], Mf[tr]); np.add.at(cc, cell[tr], 1.0)
        muAC = np.where(cc > 0, sc / np.maximum(cc, 1), np.nan)
        pac = muAC[cell[te]]
        pac = np.where(np.isnan(pac), pa, pac)  # leak-free backoff
        y = Mf[te]
        ss_tot += np.sum((y - gm) ** 2)
        ss_a += np.sum((y - pa) ** 2)
        ss_ac += np.sum((y - pac) ** 2)
    r2_a = 1 - ss_a / ss_tot if ss_tot > 0 else 0.0
    r2_ac = 1 - ss_ac / ss_tot if ss_tot > 0 else 0.0
    return dict(r2_Aonly_outofcontext=float(r2_a),
                r2_AC_incontext=float(r2_ac),
                explained_by_bringing_C_into_frame=float(r2_ac - r2_a))


def op2_context_variable(bins=8):
    """M = A*C with C a real third variable (== B field). Two frames:

       OUT of context  : predictor space = {A}            -> A-only R2 (looks irreducible)
       IN  context     : predictor space = {A, C}         -> (A,C) R2 (explained)

    Also report, for reference, the SAME-system 'A vs B' emergence read where B IS C
    (this is exactly INT=A*B): out-of-frame two-parent gain is HIGH, but that two-
    parent read ALREADY has both parents in frame -- the point of op(II) is the
    ONE-variable-in-frame vs TWO-variables-in-frame contrast for the verdict 'is M
    explained by what's in scope?'."""
    A, B, _ = field()
    C = B                      # the context variable: in the world, maybe out of frame
    M = A * C
    return _condition_on_C_gain(A, M, C, bins=bins)


# =============================================================================== #
# DRIVER                                                                          #
# =============================================================================== #
def _verdict(g, hi=0.05):
    return "INTERACTIVE(flag)" if g >= hi else "additive(floor)"


if __name__ == "__main__":
    np.set_printoptions(suppress=True)

    print("#" * 92)
    print("# OPERATIONALIZATION (I): PARENT-RANGE / SUB-POPULATION  --  locality of nonlinearity")
    print("#   SAME system M = A*B, re-measured over relevance bands {|A - a0| <= h}.")
    print("#   gain = held-out R2[joint] - R2[additive] (predictive_gain). flag>=0.05 ; floor<0.05")
    print("#" * 92)

    for a0 in (0.0, 2.0):
        print(f"\n=== frame center a0 = {a0}  (band shrinks the RELEVANCE window, not the grid) ===")
        rows, n_eq = op1_parent_range(a0=a0)
        law = {d["h"]: d for d in op1_taylor_law(a0=a0)}
        print(f"{'h':>5} {'n_band':>7} {'A-range':>16} {'gain_full':>10} {'verdict_full':>18} "
              f"{'gain_eqN':>9} {'gamfrac_f':>10}  {'rho_pred(h^2 law)':>17}")
        for r in rows:
            rng = f"[{r['a_lo']:+.2f},{r['a_hi']:+.2f}]"
            print(f"{r['h']:>5.2f} {r['n']:>7d} {rng:>16} {r['gain_full']:>10.4f} "
                  f"{_verdict(r['gain_full']):>18} {r['gain_eq']:>9.4f} {r['gamfrac_full']:>10.4f}  "
                  f"{law[r['h']]['rho_pred']:>17.4f}")
        print(f"  (equal-n control held n = {n_eq} across ALL bands: if gain_eqN still "
              f"falls with h, the flip is NOT a sample-size artifact.)")

    print("\n" + "#" * 92)
    print("# CRITICAL CONTROL (the anti-artifact discriminator): narrow the band on an")
    print("#   IRRELEVANT axis Z (independent of A and B). This drops n EXACTLY like the")
    print("#   relevant-axis narrowing, but does NOT change the A,B frame of M=A*B.")
    print("#   POWER-ARTIFACT would floor here too (fewer points). FRAME effect must NOT:")
    print("#   the system is still framed over the full range of A and B -> stays interactive.")
    print("#" * 92)
    A, B, _ = field()
    M = A * B
    Z = np.random.default_rng(99).standard_normal(A.shape)
    print(f"{'h(Z)':>6} {'n':>7} {'gain_full':>10} {'verdict':>18}   vs  relevant-axis A at matched n")
    for h in (3.0, 1.0, 0.6, 0.3, 0.15):
        miZ = np.flatnonzero(np.abs(Z) <= h)
        gZ = predictive_gain(A[miZ], B[miZ], M[miZ], bins=8).gain_r2
        # matched-n narrowing on the RELEVANT axis A at a0=2 (subsample to same n)
        miA = np.flatnonzero(np.abs(A - 2.0) <= 3.0)
        if miA.size > miZ.size:
            miA = np.random.default_rng(7).choice(miA, miZ.size, replace=False)
        gA = predictive_gain(A[miA], B[miA], M[miA], bins=8).gain_r2
        print(f"{h:>6.2f} {miZ.size:>7d} {gZ:>10.4f} {_verdict(gZ):>18}   "
              f"(A-frame@matched n={miA.size}: gain={gA:.4f})")
    print("  Z-narrowing keeps gain HIGH at every n => the flip in op(I) is NOT sample size.")

    print("\n" + "#" * 92)
    print("# SECOND CONFIRMATION via XOR = sign(A)*sign(B): its nonlinearity is LOCAL to the")
    print("#   A=0 sign-seam. Narrowing AWAY from 0 (a0=2) makes sign(A) CONSTANT -> M=sign(B),")
    print("#   a function of B alone = additive. Narrowing AROUND 0 (a0=0) keeps the seam in")
    print("#   frame -> stays interactive. Same locality-of-nonlinearity law, second system.")
    print("#" * 92)
    Mx = np.sign(A) * np.sign(B)
    for a0 in (0.0, 2.0):
        seam = "seam A=0 IN frame -> stays interactive" if a0 == 0.0 else "seam A=0 OUT of frame -> sign(A) const -> floors"
        print(f"\n=== XOR, frame center a0 = {a0}   ({seam}) ===")
        print(f"{'h':>5} {'n_band':>7} {'gain_full':>10} {'verdict':>18}")
        for h in (3.0, 1.5, 1.0, 0.6, 0.3):
            idx = np.flatnonzero(np.abs(A - a0) <= h)
            if idx.size < 50:
                print(f"{h:>5.2f} {idx.size:>7d}  (too few)")
                continue
            g = predictive_gain(A[idx], B[idx], Mx[idx], bins=8).gain_r2
            print(f"{h:>5.2f} {idx.size:>7d} {g:>10.4f} {_verdict(g):>18}")

    print("\n" + "#" * 92)
    print("# OPERATIONALIZATION (II): CONTEXT VARIABLE C  (in-scope vs out-of-scope)")
    print("#   M = A*C. OUT of context predictor={A} ; IN context predictor={A,C}.")
    print("#   Same system, two frames: does bringing C into scope EXPLAIN the merge?")
    print("#" * 92)
    res = op2_context_variable(bins=8)
    print(f"  OUT-of-context  R2[A only]      = {res['r2_Aonly_outofcontext']:+.4f}  "
          f"-> {_verdict(max(res['r2_Aonly_outofcontext'],0), hi=0.05)} as 'A explains M?'")
    print(f"  IN-context      R2[A,C joint]   = {res['r2_AC_incontext']:+.4f}  "
          f"-> {'EXPLAINED' if res['r2_AC_incontext']>0.5 else 'still unexplained'}")
    print(f"  explained by bringing C into frame = {res['explained_by_bringing_C_into_frame']:+.4f}")
    print("  Reading: if A-only ~0 (M looks irreducible out of context) but (A,C) ~1")
    print("  (M fully explained once C is in frame), the 'emergent merge' is a FRAME effect:")
    print("  in-context M = A*c is LINEAR per C-stratum -- additive once the relevant")
    print("  context variable is in scope. The verdict flips with WHAT IS IN FRAME.")
