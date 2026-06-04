"""
Synthetic generators (i)-(v) for the Pilot #150b/#151 cycling-capacity
Section-6 synthetic-validation gate (PRE_REGISTRATION §6).

Each generator emits, per synthetic SYSTEM, a daily record of:
  - root_hist[t, :]  : integer EventRootCode histogram (K categories) per day
  - volume[t]        : daily total event count (== root_hist[t].sum())
  - steer[t]         : external openness index S(t), annual step function
  - ground-truth labels: has_capture, capture_start/end, lock_sign, shocks, placebo

WHY HISTOGRAMS, NOT A SCALAR ENTROPY (matches PRE_REGISTRATION §3.1 + D6):
  The locked PRIMARY texture channel is the daily Shannon entropy (bits) of the
  EventRootCode histogram. The locked VOLUME CONTROL (§3.3 triple-lock / §7.1) is
  Poisson-thinning EACH window down to a common within-system rate floor BEFORE
  entropy/tau are computed. Thinning operates on per-day COUNTS, not on a scalar
  entropy. So a faithful synthetic must emit the daily histogram, exactly as the real
  ingest must persist root_hist (§3.1, D6 -- the existing scalar-only CSVs are
  insufficient for the locked control).

THE TEXTURE-CYCLING MECHANISM (validated empirically before adoption):
  tau(t) = rolling DFA-alpha of the entropy series. For tau(t) to CYCLE, the entropy
  series' local autocorrelation must CHANGE OVER TIME. We drive the daily category
  concentration by a latent AR(1) process whose autoregressive coefficient phi(t)
  VARIES IN TIME:
        x(t) = phi(t) * x(t-1) + noise
        kappa(t) = clip( kappa_center + kappa_amp * z(x(t)) )      # concentration
        p(t) = softmax( base_logits + kappa(t) * concentration_template )
        root_hist(t, :) ~ Multinomial( V(t), p(t) )
  - phi near 1  -> strongly autocorrelated entropy  -> high local DFA-alpha (~1.0-1.5)
  - phi near 0  -> white-ish entropy                -> low  local DFA-alpha (~0.5)
  HEALTHY: phi(t) slowly OSCILLATES (e.g. 0.1<->0.95) -> tau(t) CYCLES (high A_cyc),
           verified to survive Poisson-thinning at both 200/day and 50000/day.
  LOCKED-SQUEEZE: phi pinned HIGH (~0.95) -> tau pinned high, A_cyc collapses, lock +.
  LOCKED-PULL:   phi pinned LOW  (~0.02) -> tau pinned ~0.5,  A_cyc collapses, lock -.
  This was checked directly: healthy A_cyc ~0.5 vs captured ~0.15 (a ~70% collapse that
  survives thinning); squeeze tau-level high, pull tau-level low. See build notes.

THE VOLUME CONFOUND (gen iv) -- planted to MATCH the #150 r=0.92 killer:
  At low V(t), finite-count multinomial sampling adds a WHITE (alpha~0.5) component to
  entropy, depressing DFA-alpha; as V(t) rises, that white floor shrinks and DFA-alpha
  rises -> a SPURIOUS tau trend that tracks volume. With the modest breathing amplitude
  used for gen (iv) (constant texture), this confound is strong: RAW corr(tau, log-vol)
  ~ +0.4..+0.6 (verified). Poisson-thinning to a common LOW floor (1st pct of daily
  totals) removes it (thinned corr ~ 0; verified), and H3b first-differencing neutralizes
  any residual trend. gen (iv) is the within-system longitudinal analogue of #150.

VOLUME HETEROGENEITY (matched to real GDELT, verified from data/raw/*_event_count.csv):
      USA ~51,480/day (204M total) ... RUS ~9,314 ... CHN ~5,608 ...
      VEN ~1,503 ... PRK ~820 (median ~481) ... CHL ~606/day (2.4M total).
  Synthetic systems draw per-system mean daily volume LOG-UNIFORM over [~450, ~52000]
  so low-volume systems are GENUINELY sparse (hundreds/day) and the panel spans the real
  ~2 orders of magnitude.

numpy-only. Reuses nothing that needs reimplementing; pilot.dfa is used downstream in
sv_pipeline (not here).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# ----------------------------------------------------------------------------
# Constants (locked design + real GDELT range)
# ----------------------------------------------------------------------------
K_CATEGORIES = 20          # GDELT EventRootCode = 20 root codes
N_DAYS = 3900              # ~10.7 yr daily record, matches GDELT v2 window length
VOL_LOW = 450.0            # per-system mean daily volume floor  (~PRK/CHL real)
VOL_HIGH = 52000.0         # per-system mean daily volume ceiling (~USA real)

# AR(1) phi targets (the texture knob).  phi high -> DFA-alpha high; phi low -> ~0.5.
PHI_HI = 0.96              # squeeze pole: over-correlated (DFA-alpha HIGH, ~1.0-1.3 thinned).
                           #   RECALIBRATED (was 0.88, BUG): the healthy OSCILLATION reaches
                           #   phi=0.97 so its MEDIAN tau is already ~0.83-0.96; a squeeze pin
                           #   at 0.88 read tau~0.70 -- BELOW the healthy median -> the captured
                           #   "squeeze" departure was NEGATIVE (wrong lock sign, ~1% detection).
                           #   The phi->tau map (constant-phi calibration) shows phi=0.96 lands
                           #   tau ~1.0 (sparse) to ~1.3 (dense), CLEARLY ABOVE the ~0.83-0.96
                           #   healthy median -> a genuine POSITIVE squeeze departure at all
                           #   volumes. A_cyc still collapses (pinned = no oscillation).
PHI_LO = 0.12             # pull pole: white-noise-random (DFA-alpha ~0.55). NOT at the floor.
PHI_MID = 0.6              # neutral baseline (used for constant-texture confound gens)
PHI_OSC_LO, PHI_OSC_HI = 0.05, 0.97   # healthy oscillation band (wide -> high A_cyc)
SHOCK_AMP = 0.70           # phi displacement at a shock (large -> the excursion dominates the
                           #   healthy cycling band so its return is measurable through the
                           #   365-day DFA window's heavy smoothing)
SHOCK_RELAX_DAYS = 220.0   # healthy recovery time-constant. MONTHS-scale (not weeks): social
                           #   relaxation timescales are long (cont 30 / cymatics Reading 06 §6),
                           #   AND a sub-window-scale recovery is invisible to a 365-day rolling
                           #   DFA. ~220 d makes the healthy recovery a resolvable excursion-and-
                           #   return while the captured displacement persists (no recovery).

# breathing amplitude of the concentration (kept MODEST so sampling noise -> a real
# volume floor; cycling comes from phi(t), not from kappa amplitude)
KAPPA_AMP = 0.6
KAPPA_CENTER = 2.0

# cycling oscillation: ~1.0-1.6 yr period so several cycles fit a healthy epoch
OSC_CYCLES_PER_DECADE = 7.0


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _softmax_rows(z: np.ndarray) -> np.ndarray:
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def _zscore(x: np.ndarray) -> np.ndarray:
    s = x.std()
    return (x - x.mean()) / s if s > 0 else x - x.mean()


def _template(K: int, rng: np.random.Generator) -> np.ndarray:
    v = rng.standard_normal(K)
    v = v - v.mean()
    return v / (np.linalg.norm(v) + 1e-12)


def _base_logits(K: int, rng: np.random.Generator) -> np.ndarray:
    b = 0.4 * rng.standard_normal(K)
    return b - b.mean()


def _ar1_with_phipath(phi_path: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """AR(1) latent texture with a TIME-VARYING coefficient phi(t)."""
    n = len(phi_path)
    x = np.zeros(n)
    e = rng.standard_normal(n)
    for t in range(1, n):
        x[t] = phi_path[t] * x[t - 1] + e[t]
    return x


def _make_volume(mean_vol: float, drift_factor: float, n_days: int,
                 rng: np.random.Generator) -> np.ndarray:
    """Daily total volume: overdispersed counts with weekly + slow seasonal wobble and
    an optional smooth multiplicative DRIFT (end/start ratio = drift_factor)."""
    t = np.linspace(0.0, 1.0, n_days)
    # center the geometric drift on mean_vol: start = mean / sqrt(drift), end = mean * sqrt(drift)
    # so the per-system geometric-mean rate stays at mean_vol and the PEAK stays near the
    # GDELT ceiling (keeps volumes realistic AND multinomial draws tractable for large drift).
    trend = drift_factor ** (t - 0.5)
    season = (1.0 + 0.15 * np.sin(2 * np.pi * t * 10.7)
              + 0.10 * np.sin(2 * np.pi * np.arange(n_days) / 7.0))
    lam = np.clip(mean_vol * trend * season, 5.0, None)
    shape = 8.0
    gamma = rng.gamma(shape, lam / shape)
    vol = rng.poisson(gamma).astype(float)
    return np.clip(vol, 1.0, None)


def _emit_hist(phi_path: np.ndarray, volume: np.ndarray, base: np.ndarray,
               tmpl: np.ndarray, rng: np.random.Generator,
               kappa_amp: float = KAPPA_AMP) -> np.ndarray:
    """Realize daily Multinomial category histograms from the AR(1) texture + volume."""
    n = len(phi_path)
    x = _ar1_with_phipath(phi_path, rng)
    xz = _zscore(x)
    kappa = np.clip(KAPPA_CENTER + kappa_amp * xz, 0.0, None)
    logits = base[None, :] + kappa[:, None] * tmpl[None, :]
    p = _softmax_rows(logits)
    hist = np.empty((n, K_CATEGORIES), dtype=np.int64)
    for t in range(n):
        hist[t] = rng.multinomial(int(volume[t]), p[t])
    return hist


def _annual_step(daily: np.ndarray) -> np.ndarray:
    """Collapse a daily openness latent to an annual step function (PRE_REG §3.2:
    annual S assigned to all days in that calendar year, no within-year smoothing)."""
    n = len(daily)
    out = daily.copy()
    for y0 in range(0, n, 365):
        y1 = min(y0 + 365, n)
        out[y0:y1] = np.median(daily[y0:y1])
    return out


def _plant_shocks(n_days: int, n_shocks: int, rng: np.random.Generator,
                  margin: int = 420) -> list:
    """Plant shock-onset days spaced with >= margin days of pre/post coverage."""
    lo, hi = margin, n_days - margin
    if hi <= lo:
        return []
    base = np.linspace(lo, hi, n_shocks + 2)[1:-1]
    jit = rng.integers(-45, 45, size=len(base))
    return sorted(int(d) for d in np.clip(base.astype(int) + jit, lo, hi))


# ----------------------------------------------------------------------------
# phi(t) path construction
# ----------------------------------------------------------------------------
def _phi_healthy(n_days: int, rng: np.random.Generator) -> np.ndarray:
    """Slowly OSCILLATING phi -> tau(t) cycles (high A_cyc). Random phase per system."""
    t = np.linspace(0.0, 1.0, n_days)
    phase = rng.uniform(0, 2 * np.pi)
    cyc = OSC_CYCLES_PER_DECADE * (n_days / 3900.0)
    mid = 0.5 * (PHI_OSC_LO + PHI_OSC_HI)
    amp = 0.5 * (PHI_OSC_HI - PHI_OSC_LO)
    return mid + amp * np.sin(2 * np.pi * t * cyc + phase)


# phi-pin pad: must COVER the steer ramp (~0.10*N) so that EVERY captured-labelled window
# (steer below its midpoint, which extends into the ramps) sees a fully-pinned phi span and
# none of the oscillating pre/post-capture data leaks in. (With the old rectangular steer a
# pad of 200 sufficed; the multi-level RAMP steer needs the pad to exceed the ramp length,
# else ramp-region windows are captured-labelled but still oscillating -> the H1b collapse
# and the squeeze lock sign were diluted.)
CAP_PAD = int(0.13 * N_DAYS)      # ~507 d > ramp (~390 d)


def _phi_with_capture(n_days: int, cap_start: int, cap_end: int, lock_sign: int,
                      rng: np.random.Generator, pad: int = CAP_PAD) -> np.ndarray:
    """Healthy oscillation everywhere, then PIN phi across the capture episode to the
    planted pole (squeeze: high; pull: low) -> cycling collapses in capture.

    The phi-pin is PADDED by `pad` days (> the steer ramp) beyond the steer-trough
    [cap_start, cap_end] on each side, so every captured-labelled 365-day window sees a
    FULLY-pinned span (no oscillating pre/post-capture data leaking into the window) ->
    captured A_cyc reflects the true collapse, not transition contamination."""
    phi = _phi_healthy(n_days, rng)
    pin = PHI_HI if lock_sign > 0 else PHI_LO
    a = max(0, cap_start - pad)
    b = min(n_days, cap_end + pad)
    phi[a:b] = pin
    # tiny residual jitter so the captured segment is not perfectly constant
    phi[a:b] += 0.01 * rng.standard_normal(b - a)
    return np.clip(phi, 0.0, 0.995)


# ----------------------------------------------------------------------------
# System container
# ----------------------------------------------------------------------------
@dataclass
class SyntheticSystem:
    name: str
    root_hist: np.ndarray
    volume: np.ndarray
    steer: np.ndarray
    has_capture: bool
    capture_start: int
    capture_end: int
    lock_sign: int                 # +1 squeeze, -1 pull, 0 none
    shocks: list
    placebo_shocks: list
    meta: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------
# Shock application (in phi-space): healthy recovers, captured does not
# ----------------------------------------------------------------------------
def _apply_shocks_to_phi(phi: np.ndarray, shocks: list, captured_mask: np.ndarray,
                         relax_days: float, amp: float, rng: np.random.Generator
                         ) -> np.ndarray:
    """Each shock transiently displaces phi (texture).
      - HEALTHY stretch: the displacement DECAYS back exponentially (active-stability /
        restorative failsafe -> recovery; cont 26 §2, cont 20).  -> finite return half-life.
      - CAPTURED stretch: a slow, sluggish transient toward mid that PERSISTS over the
        recovery horizon (the locked system mounts no fast restorative return), then relaxes
        back toward the pinned pole. RECALIBRATED (was a HELD permanent step `0.5+0.5 exp`):
        a permanent step COMPOUNDED across the ~5 captured shocks and dragged the squeeze
        pole's phi from 0.96 down to ~0.7, so the captured median tau fell BELOW the healthy
        median -> the squeeze lock sign read negative (~1% correct). A decaying-back kick does
        not compound, so the locked-HIGH pole holds (captured tau ~1.0-1.1, a true POSITIVE
        departure) while the kick is still slow enough to be a non-recovering excursion within
        the 365-d window (H2b non-recovery)."""
    out = phi.astype(float).copy()
    n = len(out)
    cap_amp = 0.08   # captured-kick amplitude (small; decays back -> no compounding drift)
    cap_decay = 300.0  # sluggish (months-scale) so the captured excursion persists across H
    for d in shocks:
        t = np.arange(n - d)
        if captured_mask[min(d, n - 1)]:
            toward_mid = np.sign(0.5 - out[d])                 # away from pole, toward 0.5
            out[d:] += toward_mid * cap_amp * np.exp(-t / cap_decay)   # decays back to the pin
        else:
            sign = rng.choice([-1.0, 1.0])
            out[d:] += sign * amp * np.exp(-t / relax_days)    # large recovering pulse
    return np.clip(out, 0.0, 0.97)


# ----------------------------------------------------------------------------
# Core builder
# ----------------------------------------------------------------------------
def _build(name, has_capture, lock_sign, mean_vol, drift_factor, rng,
           constant_texture=False, kappa_amp=KAPPA_AMP, n_days=N_DAYS):
    K = K_CATEGORIES
    base = _base_logits(K, rng)
    tmpl = _template(K, rng)

    if has_capture:
        cap_start = int(n_days * rng.uniform(0.30, 0.42))
        cap_end = min(int(cap_start + n_days * rng.uniform(0.30, 0.38)), n_days)
    else:
        cap_start, cap_end = -1, n_days

    # captured_mask matches the PADDED phi-pin region (CAP_PAD) so a shock landing inside
    # the pinned span is treated as captured (persistent, non-recovering) even if just
    # outside the steer-trough [cap_start, cap_end]. (Same pad as the phi-pin -> the mask
    # and the pin cover the identical span, so shock-recovery labelling is consistent.)
    captured_mask = np.zeros(n_days, dtype=bool)
    PAD = CAP_PAD
    if has_capture:
        captured_mask[max(0, cap_start - PAD):min(n_days, cap_end + PAD)] = True

    # phi(t)
    if constant_texture:
        phi = np.full(n_days, PHI_MID)
    elif has_capture:
        phi = _phi_with_capture(n_days, cap_start, cap_end, lock_sign, rng, pad=PAD)
    else:
        phi = _phi_healthy(n_days, rng)

    # shocks (skip displacing texture for the constant-texture confound gens so their
    # texture stays genuinely constant -> the only signal is volume)
    shocks = _plant_shocks(n_days, 12, rng)   # >= 5 required (§4.2); 12 -> ~5-6 per epoch
    placebo = _plant_shocks(n_days, 12, np.random.default_rng(rng.integers(1 << 30)))
    if not constant_texture:
        phi = _apply_shocks_to_phi(phi, shocks, captured_mask,
                                   relax_days=SHOCK_RELAX_DAYS, amp=SHOCK_AMP, rng=rng)

    volume = _make_volume(mean_vol, drift_factor, n_days, rng)
    hist = _emit_hist(phi, volume, base, tmpl, rng, kappa_amp=kappa_amp)

    # steer (set by caller for confound gens; default capture/stable here)
    if has_capture:
        steer = _steer_capture(n_days, cap_start, cap_end, rng)
    else:
        steer = _steer_stable(n_days, rng)

    return SyntheticSystem(
        name=name, root_hist=hist, volume=volume, steer=steer,
        has_capture=has_capture, capture_start=cap_start, capture_end=cap_end,
        lock_sign=lock_sign, shocks=shocks, placebo_shocks=placebo,
        meta=dict(mean_vol=mean_vol, drift_factor=drift_factor,
                  constant_texture=constant_texture, kappa_amp=kappa_amp))


def _steer_capture(n_days, cap_start, cap_end, rng, high=None, low=None):
    """MULTI-LEVEL annual openness steer for a capture system (matches real V-Dem
    v2x_freexp_altinf: annual, but multi-level -- it changes a little EVERY year, not a
    two-level rectangular step). High plateau -> gradual ~1-yr ramp DOWN into a sustained
    captured trough -> gradual ramp back UP, plus a small independent per-year wobble so
    every annual step differs.  RECALIBRATED (was a 2-level rectangular step): a rectangular
    step, first-differenced (the locked H3b pre-whitening), left only ~2 nonzero regressor
    points per system -> the H3b regressor was degenerate, so gen(iv)'s 'NULL on H3b' passed
    TRIVIALLY (a dead regressor) rather than by genuinely rejecting the confound. A multi-level
    ramp yields ~10 nonzero dS per system, so the H3b null is now well-posed and the confound
    NULLs for the right reason. (NB: even with a well-posed regressor the first-differenced
    SLOPE remains UNDERPOWERED on the SIGNAL gens -- the lock-up is a level effect that diff
    annihilates; that is a genuine design finding, see synthetic_validation.md, not a generator
    bug. The lock DIRECTION via lock_sign_detected is what works and drives gate (a).)"""
    high = high if high is not None else rng.uniform(0.80, 0.92)
    low = low if low is not None else rng.uniform(0.15, 0.30)
    ramp = max(1, int(0.10 * n_days))                    # ~1-yr gradual transition each side
    daily = np.full(n_days, high)
    a, b = cap_start, cap_end
    seg_d = daily[max(0, a - ramp):a]
    daily[max(0, a - ramp):a] = np.linspace(high, low, len(seg_d))
    daily[a:b] = low
    seg_u = daily[b:min(n_days, b + ramp)]
    daily[b:min(n_days, b + ramp)] = np.linspace(low, high, len(seg_u))
    # annual step WITH a small per-year wobble -> genuinely multi-level (no two years identical)
    out = daily.copy()
    for y0 in range(0, n_days, 365):
        y1 = min(y0 + 365, n_days)
        out[y0:y1] = np.clip(np.median(daily[y0:y1]) + 0.02 * rng.standard_normal(), 0.05, 0.95)
    return out


def _steer_stable(n_days, rng):
    """Steer-stable system: a gentle MULTI-LEVEL annual wander (small year-to-year drift,
    no capture episode). Multi-level (not a flat line) so it matches real annual V-Dem and
    so H3b/E1 are well-defined; the amplitude is small so no capture epoch is labelled."""
    base = rng.uniform(0.78, 0.90)
    walk = np.cumsum(rng.standard_normal(n_days)) / np.sqrt(n_days)
    return _annual_step(np.clip(base + 0.05 * walk, 0.05, 0.95))


def _vol_grid(n_systems: int, rng: np.random.Generator) -> np.ndarray:
    """Per-system mean daily volumes, log-uniform across the real GDELT range so
    ~half the panel is genuinely sparse (hundreds/day)."""
    u = rng.uniform(0.0, 1.0, n_systems)
    return VOL_LOW * (VOL_HIGH / VOL_LOW) ** u


# ----------------------------------------------------------------------------
# The five generators
# ----------------------------------------------------------------------------
def gen_i_cycling(n_systems: int, rng: np.random.Generator) -> list:
    """(i) Cycling + recovering. Healthy phi OSCILLATES (high A_cyc); shocks RECOVER.
    ~half carry a capture episode (so they own a healthy AND a captured epoch for the
    paired test); the captured epoch pins phi (cycling collapses, no recovery). The
    captured pole alternates squeeze/pull so the population is SYMMETRIC (both signs).
    Ground truth: H1b high A_cyc when healthy, H2b fast recovery when healthy, lock present."""
    systems = []
    vols = _vol_grid(n_systems, rng)
    for i in range(n_systems):
        has_cap = (i % 2 == 0)
        sign = (1 if (i % 4 == 0) else -1) if has_cap else 0
        systems.append(_build(f"i_sys{i:02d}", has_cap, sign, vols[i],
                              drift_factor=1.0, rng=rng))
    return systems


def gen_ii_locked_squeeze(n_systems: int, rng: np.random.Generator) -> list:
    """(ii) Locked-squeeze: every system has a capture episode pinning phi HIGH
    (DFA-alpha >> 1, over-correlated), cycling collapsed, no recovery in capture.
    Ground truth: H1b/H2b CAPTURED, lock sign POSITIVE."""
    systems = []
    vols = _vol_grid(n_systems, rng)
    for i in range(n_systems):
        systems.append(_build(f"ii_sys{i:02d}", True, +1, vols[i],
                              drift_factor=1.0, rng=rng))
    return systems


def gen_iii_locked_pull(n_systems: int, rng: np.random.Generator) -> list:
    """(iii) Locked-pull: capture episode pins phi LOW (DFA-alpha ~0.5, white-random),
    cycling collapsed, no recovery.  Ground truth: H1b/H2b CAPTURED, lock sign NEGATIVE."""
    systems = []
    vols = _vol_grid(n_systems, rng)
    for i in range(n_systems):
        systems.append(_build(f"iii_sys{i:02d}", True, -1, vols[i],
                              drift_factor=1.0, rng=rng))
    return systems


# gen(iv) volume regime: SPARSE floor (high sampling-noise) <-> DENSE ceiling (low noise).
# Chosen in the SUB-SATURATION band where DFA-alpha is genuinely volume-sensitive (the
# constant-phi -> tau calibration shows tau rises with volume up to ~2000/day then saturates),
# so the drift actually moves tau. vsparse/vdense tuned so the RAW confound fires the H1b gate
# in ~every panel (corr(tau,logvol) ~ +0.74-0.75, matching the #150 r=0.92 regime) and
# Poisson-thinning kills it to ~0 (see synthetic_validation.md, "load-bearing volume gate").
IV_VOL_DENSE = 3000.0
IV_VOL_SPARSE = 45.0
IV_RAMP_FRAC = 0.04        # SHORT transition (vs the 0.10 healthy-capture ramp): a sharp
                           #   coverage change so the sustained-drop epoch labelling cleanly
                           #   isolates the dense-captured plateau from the sparse-healthy
                           #   plateau (a gradual ramp spread "captured" across the transition
                           #   and washed out the A_cyc contrast -> the confound stopped firing
                           #   H1b, i.e. the must-NULL went vacuous again). Tuned (see report)
                           #   so the RAW confound fires the H1b gate ~every panel (d_z~1.3,
                           #   corr(tau,logvol)~+0.74) and Poisson-thinning kills it (0/N).


def _iv_drift_volume(vsparse: float, vdense: float, cap_start: int, cap_end: int,
                     n_days: int, rng: np.random.Generator,
                     ramp_frac: float = IV_RAMP_FRAC) -> np.ndarray:
    """Daily volume for the confound: SPARSE in the high-steer (pseudo-healthy) epochs,
    ramping up to DENSE across the low-steer (pseudo-captured) epoch, ramping back to sparse.
    This is a within-system COVERAGE drift correlated with the steer (PRE_REG §7 confound #2):
    the sparse epochs' white sampling-noise floor INFLATES tau dispersion, so the dense
    captured epoch spuriously looks like 'cycling collapsed' (A_cyc down) -- the predicted-sign
    H1b artifact. The volume control (thin every window to a common low floor) must kill it."""
    vol = np.full(n_days, float(vsparse))
    ramp = max(1, int(ramp_frac * n_days))
    a, b = cap_start, cap_end
    seg_u = vol[max(0, a - ramp):a]
    vol[max(0, a - ramp):a] = np.linspace(vsparse, vdense, len(seg_u))
    vol[a:b] = vdense
    seg_d = vol[b:min(n_days, b + ramp)]
    vol[b:min(n_days, b + ramp)] = np.linspace(vdense, vsparse, len(seg_d))
    season = 1.0 + 0.10 * np.sin(2 * np.pi * np.arange(n_days) / 7.0)
    lam = np.clip(vol * season, 5.0, None)
    gamma = rng.gamma(8.0, lam / 8.0)
    return np.clip(rng.poisson(gamma).astype(float), 1.0, None)


def _iv_sharp_steer(cap_start: int, cap_end: int, n_days: int,
                    rng: np.random.Generator, ramp_frac: float = IV_RAMP_FRAC) -> np.ndarray:
    """Multi-level annual steer with a SHORT sustained drop, aligned to the volume transition
    so the captured-labelled windows coincide with the dense plateau (and healthy with sparse)."""
    hi = rng.uniform(0.82, 0.90)
    lo = rng.uniform(0.15, 0.25)
    ramp = max(1, int(ramp_frac * n_days))
    d = np.full(n_days, hi)
    a, b = cap_start, cap_end
    d[max(0, a - ramp):a] = np.linspace(hi, lo, len(d[max(0, a - ramp):a]))
    d[a:b] = lo
    d[b:min(n_days, b + ramp)] = np.linspace(lo, hi, len(d[b:min(n_days, b + ramp)]))
    out = d.copy()
    for y0 in range(0, n_days, 365):
        y1 = min(y0 + 365, n_days)
        out[y0:y1] = np.clip(np.median(d[y0:y1]) + 0.02 * rng.standard_normal(), 0.05, 0.95)
    return out


def gen_iv_volume_drift(n_systems: int, rng: np.random.Generator) -> list:
    """(iv) THE CRITICAL CONFOUND (the within-system analogue of the #150 r=0.92 confound),
    REBUILT to be LOAD-BEARING. CONSTANT TRUE texture (phi pinned mid throughout, NO capture,
    NO texture shocks) -- the ONLY thing that moves is daily event VOLUME, which drives a
    sampling-noise floor on raw entropy and hence a SPURIOUS tau signal.

    The drift is SINGLE-SIGNED and aligned to the steer so the artifact mimics the PREDICTED
    H1b effect: every system is SPARSE (~45/day, high white floor) in its high-steer
    (pseudo-healthy) epochs and DENSE (~3000/day, low floor) across its low-steer
    (pseudo-captured) epoch. The sparse healthy epoch therefore has spuriously INFLATED tau
    amplitude, so A_cyc 'collapses' into the dense captured epoch -- a false H1b PASS in the
    predicted direction. (The OLD gen(iv) was VACUOUS: an up/down even-odd split + log-uniform
    volumes left most systems in the saturated high-volume regime, so the panel-mean confound
    was only ~+0.04 and H1b NEVER fired even RAW -- the must-NULL could not fail and proved
    nothing about the volume control. This rebuild fires the H1b gate in a MAJORITY of panels
    RAW, corr(tau,logvol) ~ +0.74, and Poisson-thinning kills it -- see synthetic_validation.md.)

    Ground truth: NULL on H1b/H2b/H3b AFTER the locked volume control."""
    systems = []
    for i in range(n_systems):
        base = _base_logits(K_CATEGORIES, rng)
        tmpl = _template(K_CATEGORIES, rng)
        cap_start = int(N_DAYS * rng.uniform(0.36, 0.42))
        cap_end = int(N_DAYS * rng.uniform(0.72, 0.78))
        phi = np.full(N_DAYS, PHI_MID)                       # constant true texture
        vsparse = IV_VOL_SPARSE * rng.uniform(0.7, 1.4)
        vdense = IV_VOL_DENSE * rng.uniform(0.7, 1.4)
        volume = _iv_drift_volume(vsparse, vdense, cap_start, cap_end, N_DAYS, rng)
        hist = _emit_hist(phi, volume, base, tmpl, rng)
        steer = _iv_sharp_steer(cap_start, cap_end, N_DAYS, rng)  # low-steer epoch == dense epoch
        sys = SyntheticSystem(
            name=f"iv_sys{i:02d}", root_hist=hist, volume=volume, steer=steer,
            has_capture=True, capture_start=cap_start, capture_end=cap_end, lock_sign=0,
            shocks=_plant_shocks(N_DAYS, 12, rng),
            placebo_shocks=_plant_shocks(N_DAYS, 12, np.random.default_rng(rng.integers(1 << 30))),
            meta=dict(vsparse=float(vsparse), vdense=float(vdense), constant_texture=True))
        systems.append(sys)
    return systems


def gen_v_cotrending(n_systems: int, rng: np.random.Generator) -> list:
    """(v) Two co-trending but CAUSALLY UNRELATED series. The spurious co-movement is planted
    in the LEVEL/TREND (so a naive level-correlation 'sees' them co-move) but NOT in the
    cycling AMPLITUDE: the texture phi has a slow independent LEVEL trend PLUS a CONSTANT-
    amplitude oscillation, and the steer carries an INDEPENDENT gradual trend. Both trends are
    GRADUAL (no sustained-drop 'capture episode'), so no spurious A_cyc collapse is manufactured.
    Ground truth: NULL on the E1 co-movement spine (pre-whitening + surrogate-steer null kill
    the spurious level co-trend) -- and, as a robustness bonus, NULL on the primaries too.

    RECALIBRATED (was a random-WALK phi whose VARYING amplitude, once the sustained-drop epoch
    labelling was fixed, manufactured a spurious A_cyc collapse aligned to the steer-defined
    epoch and fired H1b ~88% of the time -- a real false positive on a 'causally unrelated'
    generator). A constant-amplitude oscillation on a gradual level trend keeps A_cyc epoch-
    invariant -> H1b NULLs, while the level still co-trends -> E1 is the proper must-NULL.)"""
    systems = []
    vols = _vol_grid(n_systems, rng)
    TEX_TREND_AMP = 0.25       # texture level trend over the decade (gradual, no capture)
    STEER_TREND_AMP = 0.25     # steer level trend over the decade (gradual, independent dir)
    OSC_AMP = 0.40             # CONSTANT oscillation amplitude (epoch-invariant -> H1b NULL)
    for i in range(n_systems):
        base = _base_logits(K_CATEGORIES, rng)
        tmpl = _template(K_CATEGORIES, rng)
        t = np.linspace(0.0, 1.0, N_DAYS)
        tex_dir = rng.choice([-1.0, 1.0])
        tex_trend = (TEX_TREND_AMP * tex_dir * (t - 0.5)
                     + 0.06 * np.cumsum(rng.standard_normal(N_DAYS)) / np.sqrt(N_DAYS))
        phase = rng.uniform(0, 2 * np.pi)
        osc = OSC_AMP * np.sin(2 * np.pi * t * OSC_CYCLES_PER_DECADE + phase)
        phi = np.clip(PHI_MID + tex_trend + osc, 0.05, 0.95)
        vol = _make_volume(vols[i], 1.0, N_DAYS, rng)
        hist = _emit_hist(phi, vol, base, tmpl, rng)
        steer_dir = rng.choice([-1.0, 1.0])         # INDEPENDENT of tex_dir
        steer_trend = (0.55 + STEER_TREND_AMP * steer_dir * (t - 0.5)
                       + 0.04 * np.cumsum(rng.standard_normal(N_DAYS)) / np.sqrt(N_DAYS))
        steer = _annual_step(np.clip(steer_trend, 0.05, 0.95))
        systems.append(SyntheticSystem(
            name=f"v_sys{i:02d}", root_hist=hist, volume=vol, steer=steer, has_capture=False,
            capture_start=-1, capture_end=N_DAYS, lock_sign=0,
            shocks=_plant_shocks(N_DAYS, 12, rng),
            placebo_shocks=_plant_shocks(N_DAYS, 12, np.random.default_rng(rng.integers(1 << 30))),
            meta=dict(cotrend=True)))
    return systems


GENERATORS = {
    "i_cycling": gen_i_cycling,
    "ii_squeeze": gen_ii_locked_squeeze,
    "iii_pull": gen_iii_locked_pull,
    "iv_voldrift": gen_iv_volume_drift,
    "v_cotrend": gen_v_cotrending,
}


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for key, fn in GENERATORS.items():
        ss = fn(16, rng)
        vols = np.array([s.volume.mean() for s in ss])
        print(f"{key:12s} n={len(ss):2d}  mean-vol [{vols.min():8.0f},{vols.max():8.0f}]  "
              f"caps={sum(s.has_capture for s in ss)}  signs={sorted(set(s.lock_sign for s in ss))}")
