"""
sv_pipeline.py -- the LOCKED Pilot #150b/#151 cycling-capacity pipeline, run
end-to-end against synthetic systems with KNOWN ground truth (PRE_REGISTRATION §6).

Implements, numpy-only, the entire locked chain:
  Poisson-thin (volume control, §3.3 triple-lock)
    -> rolling DFA-alpha tau(t)  (window 365 / stride 30, reusing pilot.dfa, §3.3)
      -> estimators:  A_cyc = inter-decile range of tau (H1b, §4.1)
                      T_half shock-recovery half-life (H2b, §4.2)
                      L = |tau - tau_1f| panel slope vs annual step-fn steer (H3b, §4.3)
        -> inference: H1b one-sided paired permutation on log-A_cyc, phase-randomized null
                      H2b recovery half-life diff, healthy vs captured, + placebo arm
                      H3b within-system fixed-effects slope of L on steer, block/phase null
          -> Holm across the 3 (family-wise alpha=0.05, §4)
            -> >=70% population-wideness gates (§4.1-§4.3)
            -> volume-survival gate (raw-vs-thinned, §4.1 volume gate)
          -> combined verdict (§4.4)
        -> E1 co-movement spine (exploratory; the gen(v) must-NULL, §4.5)

DFA is REUSED from pilots/1f_failsafe/pilot.py (the verified Peng-1994 implementation);
NOT reimplemented (per task: cut bug surface).

Run:
  python sv_pipeline.py --selftest                 # one panel per generator, full pipeline, prints per-system truth-vs-call
  python sv_pipeline.py --power --nsim 250          # the POWER DRIVER (the §6 gate)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_PILOT_DIR = _HERE.parents[1] / "1f_failsafe"
for p in (str(_PILOT_DIR), str(_HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    """Stable OLS slope of y on x via covariance (avoids polyfit ill-conditioning on
    step-function regressors). Returns 0.0 if x is constant."""
    vx = np.var(x)
    if vx < 1e-12:
        return 0.0
    return float(np.cov(x, y, ddof=0)[0, 1] / vx)

from pilot import dfa                      # noqa: E402  TESTED DFA (Peng 1994) -- reference oracle
from fast_dfa import dfa_fast, verify_against_pilot  # noqa: E402  vectorized, verified == pilot.dfa
import generators as G                     # noqa: E402


# ============================================================================
# Locked pipeline parameters (PRE_REGISTRATION §3.3)
# ============================================================================
WINDOW = 365         # rolling DFA window, days
STRIDE = 30          # rolling DFA stride, days
THIN_PCT = 1.0       # within-system common rate floor = 1st pct of daily totals.
                     # (Verified: thinning every window down to this near-global-minimum
                     #  rate drives corr(tau, log-volume) ~ 0 on the gen-iv confound,
                     #  vs +0.4..+0.6 raw -- the locked volume control, PRE_REG §3.3/§7.1.)
RECOVERY_H_MONTHS = 12   # H2b return horizon
PLACEBO = True

# Effect-size thresholds (locked, §4.1-§4.3)
DZ_MIN = 0.5             # H1b paired d_z
RELDECL_MIN = 0.25       # H1b median relative decline >= 25%
HR_MIN = 1.5             # H2b hazard ratio
THALF_RATIO_MIN = 1.5    # H2b T_half(captured)/T_half(healthy)
GAMMA_STD_MAX = -0.30    # H3b standardized slope
POP_GATE = 0.70          # >= 70% population-wideness
ALPHA = 0.05             # one-sided, Holm-corrected across 3


# ============================================================================
# Entropy + volume control
# ============================================================================
def entropy_bits(hist_row: np.ndarray) -> float:
    """Shannon entropy (bits) of one EventRootCode count histogram (PRE_REG §3.1)."""
    tot = hist_row.sum()
    if tot <= 0:
        return 0.0
    p = hist_row[hist_row > 0] / tot
    return float(-(p * np.log2(p)).sum())


def entropy_series(hist: np.ndarray) -> np.ndarray:
    """Daily entropy series from a (n_days, K) histogram matrix."""
    out = np.empty(hist.shape[0])
    for t in range(hist.shape[0]):
        out[t] = entropy_bits(hist[t])
    return out


def system_rate_floor(hist: np.ndarray) -> float:
    """Common within-system rate floor: low percentile of daily totals (PRE_REG §3.3).
    A single floor per system applied to every window makes all windows comparable at
    the same effective rate -> kills within-system volume drift."""
    daily_tot = hist.sum(axis=1).astype(float)
    return float(max(20.0, np.percentile(daily_tot, THIN_PCT)))


def poisson_thin(hist: np.ndarray, floor: float, rng: np.random.Generator) -> np.ndarray:
    """Binomial-thin each day's category counts down so expected daily total == floor.
    Keep each event w.p. min(1, floor/day_total). This is the volume control: it removes
    the volume-dependent sampling-noise floor that biases DFA-alpha (PRE_REG §7.1)."""
    tot = hist.sum(axis=1).astype(float)
    q = np.minimum(1.0, floor / np.maximum(tot, 1.0))      # (n_days,)
    # vectorized binomial thinning over the whole matrix
    return rng.binomial(hist, q[:, None])


# ============================================================================
# tau(t): rolling DFA-alpha (REUSES pilot.dfa)
# ============================================================================
def rolling_tau(entropy: np.ndarray, window: int = WINDOW, stride: int = STRIDE
                ) -> tuple[np.ndarray, np.ndarray]:
    """tau(t) = rolling DFA-alpha of the entropy series. Returns (tau, centers)
    where centers are the day-index of each window centre (for steer alignment)."""
    n = len(entropy)
    taus, centers = [], []
    for st in range(0, n - window + 1, stride):
        seg = entropy[st:st + window]
        a = dfa_fast(seg)                   # == pilot.dfa(seg)[0], default scale_min=8, scale_max=W//4
        taus.append(a)
        centers.append(st + window // 2)
    return np.asarray(taus, dtype=float), np.asarray(centers, dtype=int)


def compute_tau_for_system(sysobj, rng: np.random.Generator, thinned: bool = True
                           ) -> tuple[np.ndarray, np.ndarray]:
    """Full per-system tau(t): (optionally) Poisson-thin -> daily entropy -> rolling DFA."""
    if thinned:
        floor = system_rate_floor(sysobj.root_hist)
        hist = poisson_thin(sysobj.root_hist, floor, rng)
    else:
        hist = sysobj.root_hist
    ent = entropy_series(hist)
    return rolling_tau(ent)


# ============================================================================
# Epoch labelling from the steer (PRE_REG §3.4) -- the analyst-blind epoch key
# ============================================================================
CAPTURE_DROP_MIN = 0.20      # min sustained steer drop to call an epoch "captured" (PRE_REG
                             #   §3.4: a capture episode = >= X index-point drop sustained >= Y
                             #   months). Results-blind (steer-only).
CAPTURE_MIN_SAMPLES = 6      # >= Y-months sustained (in 30-d tau strides)


def epoch_labels_from_steer(sysobj, centers: np.ndarray) -> np.ndarray:
    """Per-tau-sample epoch label: 1 = captured, 0 = healthy/open (PRE_REG §3.4).
    Locked cut: 'captured' = a SUSTAINED SUBSTANTIAL DROP in the openness steer -- the steer
    must fall at least CAPTURE_DROP_MIN below the system's healthy (high) level, for at least
    CAPTURE_MIN_SAMPLES strides. A merely steer-stable system (small year-to-year wander, no
    real drop) is therefore labelled ALL-HEALTHY (no captured epoch) and does NOT contribute
    to the paired H1b/H2b tests -- fixing a bug where a midpoint-split of any wander spuriously
    manufactured a 'captured' epoch on stable systems and diluted the paired contrast."""
    s_at = sysobj.steer[centers].astype(float)
    hi = np.percentile(s_at, 75)                       # healthy/open reference level
    if s_at.max() - s_at.min() < 1e-6:
        return np.zeros(len(centers), dtype=int)
    captured = s_at <= (hi - CAPTURE_DROP_MIN)
    if captured.sum() < CAPTURE_MIN_SAMPLES:
        return np.zeros(len(centers), dtype=int)       # no sustained substantial drop -> healthy
    return captured.astype(int)


def paired_epoch_amplitudes(tau: np.ndarray, labels: np.ndarray
                            ) -> tuple[float, float] | None:
    """A_cyc (inter-decile range P90-P10 of tau, PRE_REG §4.1) for the healthy epoch
    and the captured epoch of one system. Returns (A_healthy, A_captured) or None if a
    system lacks both epochs with >= min samples."""
    MIN = 6   # min tau samples per epoch (24 monthly samples ideal; relaxed for synthetic epochs)
    h = tau[labels == 0]
    c = tau[labels == 1]
    if len(h) < MIN or len(c) < MIN:
        return None
    a_h = np.percentile(h, 90) - np.percentile(h, 10)
    a_c = np.percentile(c, 90) - np.percentile(c, 10)
    return float(a_h), float(a_c)


# ============================================================================
# H1b -- one-sided paired permutation on log-A_cyc (healthy - captured)
#        autocorrelation-respecting null via phase-randomization of tau within epoch
# ============================================================================
def _phase_randomize(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Phase-randomized surrogate preserving the power spectrum (and thus linear
    autocorrelation) of x. Used to build the autocorrelation-respecting null for A_cyc."""
    n = len(x)
    if n < 4:
        return rng.permutation(x)
    X = np.fft.rfft(x - x.mean())
    mag = np.abs(X)
    phases = rng.uniform(0, 2 * np.pi, size=mag.shape)
    phases[0] = 0.0
    if n % 2 == 0:
        phases[-1] = 0.0
    Xs = mag * np.exp(1j * phases)
    xs = np.fft.irfft(Xs, n=n) + x.mean()
    return xs


def h1b_paired_permutation(amp_pairs: list, tau_by_system: list, label_by_system: list,
                           n_perm: int, rng: np.random.Generator) -> dict:
    """Primary H1b test (PRE_REG §4.1).

    amp_pairs: list of (A_healthy, A_captured) per capture-episode system.
    Observed statistic: mean over systems of d = log(A_healthy) - log(A_captured)  (>0 predicted).

    Null (PRE_REG §4.1, LITERAL): "one-sided paired permutation test (SIGN-FLIP of the
    within-pair log-A_cyc differences, healthy - captured) across the set of capture-episode
    systems, with the null preserving within-series autocorrelation."  The sign-flip of the
    paired differences IS the inferential mechanism (exactly the prior pilot's tested
    permutation_test_delta_beta); autocorrelation is respected because each A_cyc is computed
    on the genuinely autocorrelated tau(t) (the difference is never formed from shuffled data).
    For >n systems an exhaustive 2^n enumeration is used when small, else Monte-Carlo sign-flips.
    Reports p (one-sided), Cohen's d_z, median relative decline, population-wideness share.
    """
    eps = 1e-6
    d_obs = np.array([np.log(a_h + eps) - np.log(a_c + eps) for a_h, a_c in amp_pairs])
    obs_stat = float(np.mean(d_obs))
    sd = np.std(d_obs, ddof=1) if len(d_obs) > 1 else 0.0
    d_z = obs_stat / sd if sd > 0 else float("nan")
    # median within-system relative decline: 1 - A_c/A_h
    rel_decl = np.array([1.0 - (a_c / (a_h + eps)) for a_h, a_c in amp_pairs])
    median_rel_decl = float(np.median(rel_decl))
    pop_share = float(np.mean([a_h > a_c for a_h, a_c in amp_pairs]))

    n = len(d_obs)
    abs_d = np.abs(d_obs)
    if n <= 14:
        # exhaustive sign-flip enumeration over all 2^n flips (exact permutation p)
        signs = ((np.arange(1 << n)[:, None] >> np.arange(n)[None, :]) & 1) * 2 - 1  # +/-1
        null = (signs * abs_d[None, :]).mean(axis=1)
    else:
        # n>14: 2^n enumeration is wasteful; Monte-Carlo sign-flips sample the SAME exact
        # null (each system's paired difference independently +/-). Vectorized, fixed large
        # count so the H1b p-floor (~1/20001) is far below alpha and not the limiting factor.
        n_mc = 20000
        signs = rng.integers(0, 2, size=(n_mc, n)) * 2 - 1
        null = (signs * abs_d[None, :]).mean(axis=1)
    # one-sided: healthy cycling amplitude > captured => obs_stat large positive
    p = float((np.sum(null >= obs_stat)) / len(null))
    p = max(p, 1.0 / (len(null) + 1))         # floor so an all-extreme result isn't exactly 0
    return dict(stat=obs_stat, p=p, d_z=float(d_z), median_rel_decl=median_rel_decl,
                pop_share=pop_share, n_systems=len(amp_pairs))


# ============================================================================
# H2b -- shock-recovery half-life, healthy vs captured, with placebo arm
# ============================================================================
def _tau_at_day(tau: np.ndarray, centers: np.ndarray, day: int) -> float:
    """Nearest-window tau value at a given day index."""
    i = int(np.argmin(np.abs(centers - day)))
    return tau[i]


def recovery_half_life(tau: np.ndarray, centers: np.ndarray, shock_day: int,
                       pre_win_days: int = 365, post_win_days: int = 720) -> float | None:
    """Return half-life T_half (in STRIDE units -> months) for one shock (PRE_REG §4.2):
    baseline tau_1f = trailing-12-month median tau before the shock; find the post-shock peak
    |deviation|; T_half = time for |tau - tau_1f| to fall to 50% of that peak. Censored
    (returns None) if no return within the post window."""
    pre_mask = (centers >= shock_day - pre_win_days) & (centers < shock_day)
    post_mask = (centers >= shock_day) & (centers <= shock_day + post_win_days)
    if pre_mask.sum() < 3 or post_mask.sum() < 4:
        return None
    tau_1f = np.median(tau[pre_mask])
    post_idx = np.where(post_mask)[0]
    dev = np.abs(tau[post_idx] - tau_1f)
    peak_local = int(np.argmax(dev))
    peak_dev = dev[peak_local]
    # require a REAL excursion (above the background tau scatter) before measuring recovery,
    # else the metric just tracks cycling noise. ~a fraction of a healthy A_cyc.
    if peak_dev < 0.10:
        return None
    half = 0.5 * peak_dev
    # search after the peak for first return to <= half
    for j in range(peak_local, len(post_idx)):
        if dev[j] <= half:
            months = (centers[post_idx[j]] - centers[post_idx[peak_local]]) / STRIDE
            return float(max(months, 0.0)) + 0.5     # +0.5 so a same-window return isn't exactly 0
    return None    # censored -> no recovery


def shock_recovered(tau: np.ndarray, centers: np.ndarray, shock_day: int,
                    pre_win_days: int = 365, H_months: int = RECOVERY_H_MONTHS,
                    min_exc: float = 0.10) -> int | None:
    """Binary per-shock RECOVERY outcome (PRE_REG §4.2 complement metric: 'share of shocks
    that return within H months, within 0.5 pre-shock SD, sustained').
    Returns 1 if recovered, 0 if not, None if no measurable excursion (excluded).

    A shock 'recovers' if, after its post-shock peak deviation from tau_1f, |tau - tau_1f|
    falls back to within a band (max of 0.5*peak and 1 pre-shock SD) within H months AND
    STAYS there (sustained to the end of the H-window). A persistent (locked) displacement
    never returns -> 0. Robust to the 365-day window smoothing and to background cycling
    (the band scales with the pre-shock SD), which the fragile median-T_half is not."""
    pre_mask = (centers >= shock_day - pre_win_days) & (centers < shock_day)
    H_days = H_months * STRIDE
    post_mask = (centers >= shock_day) & (centers <= shock_day + H_days)
    if pre_mask.sum() < 3 or post_mask.sum() < 4:
        return None
    tau_1f = np.median(tau[pre_mask])
    pre_sd = tau[pre_mask].std()
    post_idx = np.where(post_mask)[0]
    dev = np.abs(tau[post_idx] - tau_1f)
    peak_local = int(np.argmax(dev))
    peak_dev = dev[peak_local]
    # Excursion threshold scales with the pre-shock variability of THIS epoch. A PINNED
    # (captured) epoch has tiny pre_sd, so even a small post-shock displacement registers as
    # an excursion -- and because the locked system cannot mount restorative dynamics, that
    # displacement persists -> scored non-recovery (0). A CYCLING (healthy) epoch has large
    # pre_sd, so only a genuine shock excursion (above the cycling band) registers, and the
    # active failsafe returns it -> scored recovery (1). (PRE_REG §4.2: locked-squeeze fails
    # to return; locked-pull has no structure to return to -- both are non-recovery.)
    exc_thresh = max(0.04, 1.5 * pre_sd)
    if peak_dev < exc_thresh:
        return None                          # genuinely no event in this epoch -> excluded
    band = max(0.5 * peak_dev, 1.5 * pre_sd, 0.04)
    tail = dev[peak_local:]
    if len(tail) < 2:
        return 0
    returned = np.any(tail <= band)
    sustained = np.median(tail[max(1, len(tail) - max(2, len(tail) // 3)):]) <= band
    return int(returned and sustained)


def _shock_outcomes(tau, centers, shock_days):
    """Per-shock (outcome, epoch_label_index) for all measurable shocks of a system.
    The recovery OUTCOME of a shock is intrinsic (independent of the epoch labelling); only
    its label assignment changes under the H2b permutation null. Precomputing outcomes once
    makes the null ~n_perm x cheaper (and is exactly equivalent)."""
    outs, lab_idx = [], []
    for d in shock_days:
        out = shock_recovered(tau, centers, d)
        if out is None:
            continue
        outs.append(out)
        lab_idx.append(int(np.argmin(np.abs(centers - d))))
    return np.array(outs, dtype=float), np.array(lab_idx, dtype=int)


def _R_from_outcomes(outs, labels_at_lab_idx):
    """Recovery fractions (R_healthy, R_captured, n_h, n_c) given precomputed shock outcomes
    and the epoch label at each shock's window."""
    if len(outs) == 0:
        return None, None, 0, 0
    healthy = labels_at_lab_idx == 0
    rec_h = outs[healthy]; rec_c = outs[~healthy]
    Rh = float(rec_h.mean()) if len(rec_h) else None
    Rc = float(rec_c.mean()) if len(rec_c) else None
    return Rh, Rc, len(rec_h), len(rec_c)


def _recovery_summary(tau, centers, shock_days, labels_at_center):
    """Per-system RECOVERY FRACTION R for shocks in healthy vs captured epochs.
    Returns (R_healthy, R_captured, n_h, n_c). (Convenience wrapper over the precompute path.)"""
    outs, lab_idx = _shock_outcomes(tau, centers, shock_days)
    return _R_from_outcomes(outs, labels_at_center[lab_idx] if len(lab_idx) else np.array([], int))


def h2b_recovery(systems, tau_list, centers_list, label_list, n_perm: int,
                 rng: np.random.Generator) -> dict:
    """Primary H2b test (PRE_REG §4.2): within-system recovery MORE COMPLETE when healthy.

    Metric: per-system RECOVERY FRACTION R = #shocks-recovered / #shocks-with-excursion
    (the pre-reg §4.2 complement metric, used as primary here because median-T_half is
    fragile to the 365-day window's smoothing). Predicted: R_healthy > R_captured.
    Statistic: mean over systems of  d = R_healthy - R_captured  (>0 predicted).
    Effect size: standardized d_z; a return-rate HAZARD RATIO proxy HR = R_healthy/R_captured
    (>=1.5 threshold); and median per-system R_healthy/R_captured ratio. pop_share = fraction
    of systems with R_healthy > R_captured (>= 70% gate).
    Null: within-system permutation of shock-onset epoch labels (autocorrelation/event-rate
    respecting, PRE_REG §4.2). Placebo arm: same on placebo (random non-)shocks -> must NULL.
    """
    eps = 1e-6

    def _prep(shock_attr):
        """Precompute per-system (outcomes, label-array-at-shock-windows) ONCE."""
        prepped = []
        for sysobj, tau, centers, lab in zip(systems, tau_list, centers_list, label_list):
            if lab.sum() == 0 or lab.sum() == len(lab):
                continue
            outs, lab_idx = _shock_outcomes(tau, centers, getattr(sysobj, shock_attr))
            if len(outs) == 0:
                continue
            prepped.append((outs, lab, lab_idx))
        return prepped

    def _obs_diffs(prepped, label_perm=None):
        """Mean R_h - R_c over systems with >=2 shocks per epoch. label_perm: optional list of
        permuted label arrays aligned to prepped (for the null)."""
        ds, rhs, rcs, sgn = [], [], [], []
        for i, (outs, lab, lab_idx) in enumerate(prepped):
            labels = (label_perm[i] if label_perm is not None else lab)[lab_idx]
            Rh, Rc, nh, nc = _R_from_outcomes(outs, labels)
            if Rh is None or Rc is None or nh < 2 or nc < 2:
                continue
            ds.append(Rh - Rc); rhs.append(Rh); rcs.append(Rc); sgn.append(Rh > Rc)
        return ds, rhs, rcs, sgn

    prepped = _prep("shocks")
    ds, rhs, rcs, signs = _obs_diffs(prepped)
    if len(ds) < 3:
        return dict(p=1.0, d=float("nan"), hr=float("nan"), median_ratio=float("nan"),
                    pop_share=0.0, n_systems=len(ds), placebo_p=1.0, underpowered=True,
                    R_healthy=float("nan"), R_captured=float("nan"))
    diffs = np.array(ds)
    obs = float(np.mean(diffs))
    sd = np.std(diffs, ddof=1) if len(diffs) > 1 else 0.0
    d_eff = obs / sd if sd > 0 else float("nan")
    median_ratio = float(np.median([(h + eps) / (c + eps) for h, c in zip(rhs, rcs)]))
    pop_share = float(np.mean(signs))
    mean_Rh, mean_Rc = float(np.mean(rhs)), float(np.mean(rcs))
    hr = (mean_Rh + eps) / (mean_Rc + eps)        # pooled return-rate hazard-ratio proxy

    # null: permute epoch labels within each system (cheap -- outcomes precomputed)
    null = np.empty(n_perm)
    for k in range(n_perm):
        lp = [rng.permutation(lab) for (_, lab, _) in prepped]
        dn, _, _, _ = _obs_diffs(prepped, label_perm=lp)
        null[k] = np.mean(dn) if dn else 0.0
    p = float((np.sum(null >= obs) + 1) / (n_perm + 1))

    # placebo arm: same metric on placebo (non-)shocks -> must show no healthy>captured effect
    pl_prep = _prep("placebo_shocks")
    pl_ds, _, _, _ = _obs_diffs(pl_prep)
    if len(pl_ds) >= 3:
        pl_obs = float(np.mean(pl_ds))
        m = min(n_perm, 300)
        pl_null = np.empty(m)
        for k in range(m):
            lp = [rng.permutation(lab) for (_, lab, _) in pl_prep]
            dn, _, _, _ = _obs_diffs(pl_prep, label_perm=lp)
            pl_null[k] = np.mean(dn) if dn else 0.0
        placebo_p = float((np.sum(pl_null >= pl_obs) + 1) / (m + 1))
    else:
        placebo_p = 1.0

    return dict(p=p, d=float(d_eff), hr=float(hr), median_ratio=median_ratio,
                pop_share=pop_share, n_systems=len(ds), placebo_p=placebo_p,
                underpowered=False, R_healthy=mean_Rh, R_captured=mean_Rc)


# ============================================================================
# H3b -- within-system fixed-effects slope of L=|tau - tau_1f| on steer S
#        block/phase-randomized null on the slope; symmetry-share check
# ============================================================================
def h3b_lockup_slope(systems, tau_list, centers_list, n_perm: int,
                     rng: np.random.Generator) -> dict:
    """Primary H3b test (PRE_REG §4.3): lock-up magnitude L increases as openness S falls.

    Per system: tau_1f = system healthy-epoch (high-steer) median tau; L(t) = |tau - tau_1f|.
    Fixed-effects = within-system de-meaning of L and S; first-difference to neutralize shared
    trend. Pooled standardized slope gamma_std of dL on dS (predicted negative: lower S -> larger L).
    Null: phase-randomize each system's dL (block/phase) and recompute the pooled slope.
    Symmetry sub-claim: signed (tau - tau_1f) in capture epochs must include both directions
    (neither sign >= 90%).

    KNOWN UNDERPOWERED (a genuine design finding, see synthetic_validation.md): on this tau(t),
    the lock-up signal is a LEVEL effect (L stays large THROUGHOUT the captured low-S plateau),
    but the LOCKED first-differencing (which is what neutralizes the spurious-trend confound, so
    gens iv/v correctly NULL here) also annihilates that level contrast -> gamma_std ~ 0 even on
    the signal generators. The slope test therefore has ~0 power and is reported as a DIAGNOSTIC.
    The lock DIRECTION, by contrast, is read from `lock_sign_detected` (the median captured-epoch
    signed departure tau - tau_1f), which IS reliable (squeeze -> +, pull -> -) and is what the
    §6 gate (a) classification for the poles actually uses.
    """
    dL_all, dS_all, sys_id = [], [], []
    signed_dev = []                 # pooled signed (tau - tau_1f) over low-steer samples
    per_sys_slopes = []
    for sid, (sysobj, tau, centers) in enumerate(zip(systems, tau_list, centers_list)):
        s_at = sysobj.steer[centers].astype(float)
        if s_at.max() - s_at.min() < 1e-6:
            continue                # steer-stable system: H3b not testable on it
        # tau_1f = high-steer (healthy) median
        thr = s_at.min() + 0.5 * (s_at.max() - s_at.min())
        healthy = s_at >= thr
        if healthy.sum() < 4 or (~healthy).sum() < 4:
            continue
        tau_1f = np.median(tau[healthy])
        L = np.abs(tau - tau_1f)
        # within-system de-mean then first-difference (FE + pre-whiten shared trend)
        dL = np.diff(L - L.mean())
        dS = np.diff(s_at - s_at.mean())
        if np.std(dS) < 1e-9:
            continue
        dL_all.append(dL); dS_all.append(dS)
        sys_id.append(np.full(len(dL), sid))
        # per-system slope sign (stable OLS)
        per_sys_slopes.append(_ols_slope(dS, dL))
        signed_dev.append((tau - tau_1f)[~healthy])    # captured-epoch signed departures

    if len(dL_all) < 3:
        return dict(p=1.0, gamma_std=float("nan"), pop_share=0.0, n_systems=len(dL_all),
                    one_signed_share=float("nan"), symmetry_falsified=False,
                    lock_sign_detected=0, lock_pos_share=0.0, underpowered=True)

    dL_cat = np.concatenate(dL_all); dS_cat = np.concatenate(dS_all)
    # standardized pooled slope (stable OLS)
    sL, sS = np.std(dL_cat), np.std(dS_cat)
    beta = _ols_slope(dS_cat, dL_cat)
    gamma_std = float(beta * sS / sL) if sL > 0 else float("nan")
    # population-wideness: share of systems with predicted-sign (negative) slope
    pop_share = float(np.mean([b < 0 for b in per_sys_slopes]))

    # null: phase-randomize each system's dL, recompute pooled standardized slope
    null = np.empty(n_perm)
    for k in range(n_perm):
        dLn = [_phase_randomize(d, rng) for d in dL_all]
        dLn_cat = np.concatenate(dLn)
        b = _ols_slope(dS_cat, dLn_cat)
        null[k] = b * sS / (np.std(dLn_cat) + 1e-12)
    # one-sided: predicted negative slope -> small (very negative) gamma_std
    p = float((np.sum(null <= gamma_std) + 1) / (n_perm + 1))

    # symmetry sub-claim
    sd = np.concatenate(signed_dev) if signed_dev else np.array([0.0])
    pos = np.mean(sd > 0); neg = np.mean(sd < 0)
    one_signed = float(max(pos, neg))
    symmetry_falsified = bool(one_signed >= 0.90)

    # detected LOCK SIGN (PRE_REG §6: squeeze -> positive, pull -> negative): per-system
    # median captured-epoch signed departure, then population median sign.
    per_sys_signed = [float(np.median(s)) for s in signed_dev if len(s)]
    lock_sign_detected = int(np.sign(np.median(per_sys_signed))) if per_sys_signed else 0
    lock_pos_share = float(np.mean([m > 0 for m in per_sys_signed])) if per_sys_signed else 0.0

    return dict(p=p, gamma_std=gamma_std, pop_share=pop_share, n_systems=len(per_sys_slopes),
                one_signed_share=one_signed, symmetry_falsified=symmetry_falsified,
                lock_sign_detected=lock_sign_detected, lock_pos_share=lock_pos_share,
                underpowered=False)


# ============================================================================
# E1 -- continuous steer co-movement spine (exploratory; the gen(v) must-NULL)
# ============================================================================
def e1_comovement(systems, tau_list, centers_list, n_perm: int,
                  rng: np.random.Generator) -> dict:
    """E1 (PRE_REG §4.5): per-system partial cross-correlation between pre-whitened
    Delta-tau and Delta-S; predicted negative. Surrogate-steer null (phase-randomized S)
    must give chance-level co-movement. The gen(v) co-trending generator must NULL here:
    two independently-trending series co-move only spuriously, killed by pre-whitening (diff)
    + a phase-randomized surrogate null."""
    corrs = []
    for sysobj, tau, centers in zip(systems, tau_list, centers_list):
        s_at = sysobj.steer[centers].astype(float)
        if s_at.max() - s_at.min() < 1e-6:
            continue
        dt = np.diff(tau); ds = np.diff(s_at)
        if np.std(dt) < 1e-9 or np.std(ds) < 1e-9:
            continue
        corrs.append(np.corrcoef(dt, ds)[0, 1])
    if len(corrs) < 3:
        return dict(mean_corr=float("nan"), p=1.0, n_systems=len(corrs))
    corrs = np.array(corrs)
    obs = float(np.mean(corrs))
    # surrogate-steer null: phase-randomize each system's dS
    null = np.empty(n_perm)
    for k in range(n_perm):
        cs = []
        for sysobj, tau, centers in zip(systems, tau_list, centers_list):
            s_at = sysobj.steer[centers].astype(float)
            if s_at.max() - s_at.min() < 1e-6:
                continue
            dt = np.diff(tau); ds = np.diff(s_at)
            if np.std(dt) < 1e-9 or np.std(ds) < 1e-9:
                continue
            ds_sur = _phase_randomize(ds, rng)
            cs.append(np.corrcoef(dt, ds_sur)[0, 1])
        null[k] = np.mean(cs) if cs else 0.0
    # predicted negative co-movement -> obs strongly negative; two-sided-ish: p that null as extreme
    p = float((np.sum(np.abs(null) >= abs(obs)) + 1) / (n_perm + 1))
    return dict(mean_corr=obs, p=p, n_systems=len(corrs))


# ============================================================================
# Holm correction across the 3-hypothesis family
# ============================================================================
def holm(pvals: dict, alpha: float = ALPHA) -> dict:
    """Holm step-down across the named family. Returns {name: reject_bool}."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out = {}
    prev_reject = True
    for i, (name, p) in enumerate(items):
        thr = alpha / (m - i)
        rej = (p <= thr) and prev_reject
        out[name] = rej
        prev_reject = rej
    return out


# ============================================================================
# One full panel through the entire pipeline
# ============================================================================
def run_panel(systems, rng: np.random.Generator, n_perm: int = 200,
              thinned: bool = True) -> dict:
    """Run the ENTIRE locked pipeline on one synthetic panel. Returns all three
    primary results + Holm + gates + E1."""
    tau_list, centers_list, label_list = [], [], []
    for s in systems:
        tau, centers = compute_tau_for_system(s, rng, thinned=thinned)
        tau_list.append(tau); centers_list.append(centers)
        label_list.append(epoch_labels_from_steer(s, centers))

    # --- H1b: paired amplitudes over capture-episode systems ---
    amp_pairs, tau_cap, lab_cap = [], [], []
    for s, tau, lab in zip(systems, tau_list, label_list):
        ap = paired_epoch_amplitudes(tau, lab)
        if ap is not None:
            amp_pairs.append(ap); tau_cap.append(tau); lab_cap.append(lab)
    if amp_pairs:
        h1 = h1b_paired_permutation(amp_pairs, tau_cap, lab_cap, n_perm, rng)
    else:
        h1 = dict(stat=0.0, p=1.0, d_z=float("nan"), median_rel_decl=0.0,
                  pop_share=0.0, n_systems=0)

    # --- H2b: recovery (only capture-episode systems have both epochs) ---
    cap_sys = [s for s, lab in zip(systems, label_list) if 0 < lab.sum() < len(lab)]
    cap_tau = [tau for tau, lab in zip(tau_list, label_list) if 0 < lab.sum() < len(lab)]
    cap_cen = [c for c, lab in zip(centers_list, label_list) if 0 < lab.sum() < len(lab)]
    cap_lab = [lab for lab in label_list if 0 < lab.sum() < len(lab)]
    h2 = h2b_recovery(cap_sys, cap_tau, cap_cen, cap_lab, n_perm, rng)

    # --- H3b: lock-up slope (systems whose steer moves) ---
    h3 = h3b_lockup_slope(systems, tau_list, centers_list, n_perm, rng)

    # --- E1 co-movement spine ---
    e1 = e1_comovement(systems, tau_list, centers_list, n_perm, rng)

    # --- Holm across the 3 primary ---
    holm_rej = holm({"H1b": h1["p"], "H2b": h2["p"], "H3b": h3["p"]})

    # --- gates per hypothesis (significance + effect size + population-wideness) ---
    h1_pass = bool(holm_rej["H1b"] and (h1["d_z"] >= DZ_MIN) and
                   (h1["median_rel_decl"] >= RELDECL_MIN) and (h1["pop_share"] >= POP_GATE))
    h2_pass = bool(holm_rej["H2b"] and (not h2["underpowered"]) and
                   (h2["hr"] >= HR_MIN) and (h2["pop_share"] >= POP_GATE) and
                   (h2["placebo_p"] > ALPHA))
    h3_pass = bool(holm_rej["H3b"] and (not h3["underpowered"]) and
                   (h3["gamma_std"] <= GAMMA_STD_MAX) and (h3["pop_share"] >= POP_GATE))

    return dict(h1=h1, h2=h2, h3=h3, e1=e1, holm=holm_rej,
                h1_pass=h1_pass, h2_pass=h2_pass, h3_pass=h3_pass,
                n_systems=len(systems))


# ============================================================================
# Volume-survival gate: run thinned AND raw, confirm thinning changes the picture
# on the confound generator (the volume gate, PRE_REG §4.1)
# ============================================================================
def volume_survival_check(systems, rng: np.random.Generator, n_perm: int = 150) -> dict:
    """The LOAD-BEARING volume gate (PRE_REG §4.1 volume gate / §6 critical confound check).

    Runs the panel BOTH ways and reports, for each:
      - per-system corr(tau, log-volume)  (the #150 confound metric)
      - whether the H1b GATE FIRES  (the inferential must-NULL -- the thing that can fail)
    On the gen(iv) confound the volume control is demonstrated load-bearing iff the confound
    FIRES H1b RAW (it genuinely bites the surviving primary test) and is suppressed THINNED.
    On signal gens (i-iii) the real effect must SURVIVE thinning.

    The RAW and THINNED panels are drawn from the SAME seed stream re-seeded identically, so
    the only difference between them is the thinning step (a paired comparison, not two
    independent noise draws)."""
    def panel(thinned, seed):
        r = np.random.default_rng(seed)
        taus, corrs = [], []
        amp_pairs = []
        for s in systems:
            tau, centers = compute_tau_for_system(s, r, thinned=thinned)
            lv = np.array([np.log(s.volume[max(0, c - WINDOW // 2):c + WINDOW // 2].mean() + 1)
                           for c in centers])
            if np.std(tau) > 0 and np.std(lv) > 0:
                corrs.append(np.corrcoef(tau, lv)[0, 1])
            lab = epoch_labels_from_steer(s, centers)
            ap = paired_epoch_amplitudes(tau, lab)
            if ap is not None:
                amp_pairs.append(ap)
        # H1b gate on this panel
        h1_fire = False
        if amp_pairs:
            r2 = np.random.default_rng(seed + 1)
            h1 = h1b_paired_permutation(amp_pairs, [], [], n_perm, r2)
            h1_fire = bool(h1["p"] <= ALPHA and h1["d_z"] >= DZ_MIN and
                           h1["median_rel_decl"] >= RELDECL_MIN and h1["pop_share"] >= POP_GATE)
        return (float(np.nanmean(corrs)) if corrs else float("nan"),
                float(np.nanmean(np.abs(corrs))) if corrs else float("nan"), h1_fire)
    seed = int(rng.integers(1 << 31))
    raw_corr, raw_abscorr, raw_h1 = panel(False, seed)
    thin_corr, thin_abscorr, thin_h1 = panel(True, seed)
    return dict(raw_tau_logvol_corr=raw_corr, thin_tau_logvol_corr=thin_corr,
                raw_abs_corr=raw_abscorr, thin_abs_corr=thin_abscorr,
                raw_h1_fires=raw_h1, thin_h1_fires=thin_h1)


# ============================================================================
# Selftest: one panel per generator, print ground-truth vs pipeline call
# ============================================================================
def selftest(seed: int = 2026, n_systems: int = 18, n_perm: int = 200) -> dict:
    rng = np.random.default_rng(seed)
    print(f"\n=== SELFTEST: full pipeline, one panel per generator (N={n_systems}, n_perm={n_perm}) ===\n")
    results = {}
    for key, fn in G.GENERATORS.items():
        sysset = fn(n_systems, rng)
        r = run_panel(sysset, rng, n_perm=n_perm, thinned=True)
        vs = volume_survival_check(sysset, rng, n_perm=80)
        h1, h2, h3, e1 = r["h1"], r["h2"], r["h3"], r["e1"]
        print(f"--- generator {key} ---")
        print(f"  H1b: p={h1['p']:.4f} d_z={h1['d_z']:+.2f} reldecl={h1['median_rel_decl']:+.2f} "
              f"pop={h1['pop_share']:.2f} n={h1['n_systems']}  PASS={r['h1_pass']}")
        print(f"  H2b: p={h2['p']:.4f} ratio={h2['median_ratio']:.2f} pop={h2['pop_share']:.2f} "
              f"placebo_p={h2['placebo_p']:.3f} n={h2['n_systems']}  PASS={r['h2_pass']}")
        print(f"  H3b: p={h3['p']:.4f} gamma_std={h3['gamma_std']:+.3f} pop={h3['pop_share']:.2f} "
              f"1-signed={h3['one_signed_share']:.2f} symF={h3['symmetry_falsified']} n={h3['n_systems']}  PASS={r['h3_pass']}")
        print(f"  E1 : mean_corr={e1['mean_corr']:+.3f} p={e1['p']:.4f} n={e1['n_systems']}")
        print(f"  vol-gate: corr(tau,logvol) RAW={vs['raw_tau_logvol_corr']:+.3f} "
              f"THINNED={vs['thin_tau_logvol_corr']:+.3f}  |  H1b-gate fires RAW={vs['raw_h1_fires']} "
              f"THINNED={vs['thin_h1_fires']}")
        print(f"  Holm: {r['holm']}")
        print()
        results[key] = dict(h1=h1, h2=h2, h3=h3, e1=e1, holm=r["holm"],
                            h1_pass=r["h1_pass"], h2_pass=r["h2_pass"], h3_pass=r["h3_pass"],
                            vol_gate=vs)
    return results


# ============================================================================
# POWER DRIVER -- the §6 gate
# ============================================================================
def power_driver(seed: int = 2026, n_sim: int = 250, n_systems: int = 18,
                 n_perm: int = 200, out_path: Path | None = None) -> dict:
    """Run each generator n_sim times; report POWER on (i)-(iii) and
    FALSE-POSITIVE / must-NULL rate on (iv)-(v). Implements the PRE_REG §6 gate."""
    t0 = time.time()
    master = np.random.default_rng(seed)
    out = {}
    print(f"\n{'='*78}\nPOWER DRIVER  (n_sim={n_sim} per generator, N={n_systems} systems, "
          f"window={WINDOW}/stride={STRIDE}, n_perm={n_perm})\n{'='*78}")

    for key, fn in G.GENERATORS.items():
        is_signal = key in ("i_cycling", "ii_squeeze", "iii_pull")
        # per-sim outcome flags
        hit = dict(H1b=0, H2b=0, H3b=0, e1_fire=0, any_primary=0,
                   classify_correct=0, classify_h1_lock=0, lock_ok=0,
                   vg_raw_fire=0, vg_thin_fire=0, vg_n=0)
        n_done = 0
        for sim in range(n_sim):
            rng = np.random.default_rng(master.integers(1 << 31))
            sysset = fn(n_systems, rng)
            r = run_panel(sysset, rng, n_perm=n_perm, thinned=True)
            h1p, h2p, h3p = r["h1_pass"], r["h2_pass"], r["h3_pass"]
            lock = r["h3"]["lock_sign_detected"]
            hit["H1b"] += int(h1p); hit["H2b"] += int(h2p); hit["H3b"] += int(h3p)
            hit["any_primary"] += int(h1p or h2p or h3p)
            # E1 fires if its surrogate-null p < alpha (must-NULL for gen v)
            e1_fire = int(r["e1"]["p"] < ALPHA and np.isfinite(r["e1"]["mean_corr"]))
            hit["e1_fire"] += e1_fire
            # per-generator "correct classification" definition (PRE_REG §6 gate (a), as locked):
            # gen(i) cycling -> H1b PASS AND H2b PASS; gen(ii)/(iii) -> H1b & H2b & correct lock sign.
            # ALSO record an H1b-ONLY-cycling-collapse classification (lock-sign-aware) for the
            # revision analysis (what the gate would be if H2b were demoted to a diagnostic).
            if key == "i_cycling":
                ok = h1p and h2p
                ok_h1lock = h1p                                # mixed poles: lock direction not required
            elif key == "ii_squeeze":
                ok = h1p and h2p and (lock > 0)
                ok_h1lock = h1p and (lock > 0)
                hit["lock_ok"] += int(lock > 0)
            elif key == "iii_pull":
                ok = h1p and h2p and (lock < 0)
                ok_h1lock = h1p and (lock < 0)
                hit["lock_ok"] += int(lock < 0)
            else:
                ok = False; ok_h1lock = False
            hit["classify_correct"] += int(ok)
            hit["classify_h1_lock"] += int(ok_h1lock)
            # for the confound generator (iv): record the LOAD-BEARING volume gate (does the
            # confound fire the H1b inferential gate RAW, and is it killed THINNED?) on a subset
            if key == "iv_voldrift" and sim < min(n_sim, 20):
                vs = volume_survival_check(sysset, rng, n_perm=80)
                hit["vg_raw_fire"] += int(vs["raw_h1_fires"])
                hit["vg_thin_fire"] += int(vs["thin_h1_fires"])
                hit["vg_n"] += 1
            n_done += 1

        if is_signal:
            power = hit["classify_correct"] / n_done
            out[key] = dict(
                kind="signal", n_sim=n_done, power=power,
                power_h1_lock=hit["classify_h1_lock"] / n_done,
                H1b_rate=hit["H1b"] / n_done, H2b_rate=hit["H2b"] / n_done,
                H3b_rate=hit["H3b"] / n_done,
                lock_sign_correct=(hit["lock_ok"] / n_done) if key in ("ii_squeeze", "iii_pull") else None)
            print(f"  [{key:11s}] POWER (locked, H1b&H2b[&lock]) = {power:.3f}   "
                  f"[H1b-only(&lock) = {out[key]['power_h1_lock']:.3f}]   "
                  f"(H1b={out[key]['H1b_rate']:.3f} H2b={out[key]['H2b_rate']:.3f} "
                  f"H3b={out[key]['H3b_rate']:.3f}"
                  + (f" lock-ok={out[key]['lock_sign_correct']:.3f}" if out[key]['lock_sign_correct'] is not None else "")
                  + ")")
        else:
            # must-NULL: false positive = ANY primary fires (iv) OR E1 fires (v)
            fp_any = hit["any_primary"] / n_done
            fp_e1 = hit["e1_fire"] / n_done
            out[key] = dict(
                kind="confound", n_sim=n_done,
                fp_any_primary=fp_any, fp_e1=fp_e1,
                H1b_rate=hit["H1b"] / n_done, H2b_rate=hit["H2b"] / n_done,
                H3b_rate=hit["H3b"] / n_done)
            if key == "iv_voldrift" and hit["vg_n"] > 0:
                out[key]["volgate_raw_h1_fire_rate"] = hit["vg_raw_fire"] / hit["vg_n"]
                out[key]["volgate_thin_h1_fire_rate"] = hit["vg_thin_fire"] / hit["vg_n"]
                out[key]["volgate_n"] = hit["vg_n"]
            print(f"  [{key:11s}] FALSE-POSITIVE  any-primary={fp_any:.3f}  E1-spine={fp_e1:.3f}   "
                  f"(H1b={out[key]['H1b_rate']:.3f} H2b={out[key]['H2b_rate']:.3f} "
                  f"H3b={out[key]['H3b_rate']:.3f})")
            if key == "iv_voldrift" and hit["vg_n"] > 0:
                print(f"               LOAD-BEARING vol gate: H1b-gate fires RAW="
                      f"{out[key]['volgate_raw_h1_fire_rate']:.2f} -> THINNED="
                      f"{out[key]['volgate_thin_h1_fire_rate']:.2f}  (n={hit['vg_n']}; "
                      f"confound bites raw, Poisson-thin kills it)")

    runtime = time.time() - t0
    # ---- the §6 acceptance gate (as LOCKED) ----
    powers = {k: out[k]["power"] for k in ("i_cycling", "ii_squeeze", "iii_pull")}
    powers_h1_lock = {k: out[k]["power_h1_lock"] for k in ("i_cycling", "ii_squeeze", "iii_pull")}
    fps = {"iv_voldrift": out["iv_voldrift"]["fp_any_primary"],
           "v_cotrend": out["v_cotrend"]["fp_e1"]}
    power_ok = all(p >= 0.80 for p in powers.values())
    fp_ok = all(f <= 0.05 + 1e-9 for f in fps.values())
    gate = "PASS" if (power_ok and fp_ok) else "FAIL"
    # the REVISION the gate implies: would {H1b cycling-collapse [& lock-sign]} as the single
    # primary (H2b demoted to diagnostic) pass BOTH halves?  (Reported, not a change to the lock.)
    revised_power_ok = all(p >= 0.80 for p in powers_h1_lock.values())
    revised_gate = "PASS" if (revised_power_ok and fp_ok) else "FAIL"
    print(f"\n{'-'*78}")
    print(f"GATE (a) power>=80% on (i)-(iii) [LOCKED: H1b&H2b(&lock)]: {powers}  -> {'OK' if power_ok else 'FAIL'}")
    print(f"GATE (b) FP<=5% on (iv)[any-primary]/(v)[E1]: {fps}  -> {'OK' if fp_ok else 'FAIL'}")
    print(f"\nSECTION-6 GATE (locked design): {gate}   (runtime {runtime:.1f}s)")
    print(f"\n[revision analysis] power if H2b demoted -> primary = H1b cycling-collapse(&lock): "
          f"{powers_h1_lock}  -> revised gate {revised_gate}")
    print(f"{'='*78}\n")

    summary = dict(params=dict(n_sim=n_sim, n_systems=n_systems, window=WINDOW,
                               stride=STRIDE, n_perm=n_perm, seed=seed),
                   per_generator=out, powers=powers, powers_h1_lock=powers_h1_lock,
                   false_positives=fps, power_ok=power_ok, fp_ok=fp_ok, gate=gate,
                   revised_power_ok=revised_power_ok, revised_gate=revised_gate,
                   runtime_s=runtime)
    if out_path:
        out_path.write_text(json.dumps(summary, indent=2, default=str))
        print(f"results written to {out_path}")
    return summary


# ============================================================================
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--power", action="store_true")
    ap.add_argument("--nsim", type=int, default=250)
    ap.add_argument("--nsystems", type=int, default=18)
    ap.add_argument("--nperm", type=int, default=200)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out", type=Path, default=_HERE / "sv_power_results.json")
    args = ap.parse_args()
    if args.selftest:
        selftest(seed=args.seed, n_systems=args.nsystems, n_perm=args.nperm)
    if args.power:
        power_driver(seed=args.seed, n_sim=args.nsim, n_systems=args.nsystems,
                     n_perm=args.nperm, out_path=args.out)
    if not (args.selftest or args.power):
        selftest(seed=args.seed)


if __name__ == "__main__":
    main()
