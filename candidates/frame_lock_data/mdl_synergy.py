"""
mdl_synergy.py — first real ΔL-in-bits estimator for the frame-lock protocol.

Implements the two synergy estimators the protocol §1.B / §3 / §7 require, on
CONTROLLED ground-truth weight tensors with KNOWN verdicts. This is the
disciplined first step: validate the metric against known answers (cf. Pilot-2)
BEFORE any real HuggingFace model-merging (an explicit LATER step, not this one).

Pipeline order is LOAD-BEARING: quantize FIRST, then fit (least squares on the
quantized codes), then compress the (re-quantized) residual. Coarse quantization
can therefore annihilate fine nonlinear structure — that is the P3b
child-anchored-ceiling phenomenon we are trying to exhibit.

Two estimators (the comparison IS the scientific point):

  (1) WITNESSED synergy — the P1 non-additivity witness, operationalized:
        Syn_wit(b) = L_b(R_AB)
      bits of M NOT reconstructible from ANY affine combination of (A, B).
      This quotients out linear re-coordinatizations of the (A,B) span, so it
      should be ~floor for any M in the affine span (ADD / ROT / COPY) and > 0
      only for genuinely nonlinear interactions (SYN, and ALLOY at fine b).

  (2) NAIVE synergy — BES Theorem 4.4 / PID form, as literally written in the
      formalization (§1.B):
        Syn_pid(b) = min(L_b(R_A), L_b(R_B)) - L_b(R_AB)
      An additive average M=(A+B)/2 genuinely needs BOTH parents and neither
      alone, so it carries large PID-synergy — i.e. the naive form may MIS-FLAG
      an additive blend as synergistic. Confirming/refuting that separation is
      the finding.

Codelength of a tensor X at resolution b (bits):
    L_b(X) = 8 * len( COMPRESSOR( bbit_int_codes(X).tobytes() ) )
PINNED_COMPRESSOR = lzma (preset 6). zlib(level 9) and bz2 are error-bar siblings.

No torch / HF / network. numpy only.
"""

from __future__ import annotations

import bz2
import lzma
import zlib
from dataclasses import dataclass, field

import numpy as np

# ----------------------------------------------------------------------------
# Pinned compressor configuration
# ----------------------------------------------------------------------------

LZMA_PRESET = 6  # PINNED. The headline / verdict compressor.


def _c_lzma(b: bytes) -> bytes:
    # Pin the FORMAT and FILTERS too, not just the preset, so the byte count is
    # reproducible-to-the-bit across machines (raw stream, no .xz container
    # header/footer, no random check field).
    filt = [{"id": lzma.FILTER_LZMA2, "preset": LZMA_PRESET}]
    return lzma.compress(b, format=lzma.FORMAT_RAW, filters=filt)


def _c_zlib(b: bytes) -> bytes:
    return zlib.compress(b, level=9)


def _c_bz2(b: bytes) -> bytes:
    return bz2.compress(b, compresslevel=9)


COMPRESSORS = {
    "lzma": _c_lzma,   # pinned / headline
    "zlib": _c_zlib,   # sibling
    "bz2": _c_bz2,     # sibling
}
PINNED = "lzma"


# ----------------------------------------------------------------------------
# Quantization
# ----------------------------------------------------------------------------

def quantize(X: np.ndarray, b: int) -> np.ndarray:
    """Uniform b-bit quantization of X over its OWN [min, max] range.

    Returns integer codes in [0, 2**b - 1] with the SAME shape as X.

    A degenerate (constant) tensor maps to all-zeros. The integer dtype is the
    smallest that holds 2**b - 1, so .tobytes() length scales with b — which is
    exactly what makes coarse b cheaper and able to annihilate fine structure.
    """
    if b < 1:
        raise ValueError("b must be >= 1 bit/element")
    X = np.asarray(X, dtype=np.float64)
    xmin = float(X.min())
    xmax = float(X.max())
    levels = (1 << b) - 1  # max integer code
    if xmax <= xmin:
        codes = np.zeros(X.shape, dtype=np.int64)
    else:
        # scale to [0, levels], round to nearest integer code
        norm = (X - xmin) / (xmax - xmin)
        codes = np.rint(norm * levels).astype(np.int64)
        codes = np.clip(codes, 0, levels)
    # smallest unsigned int dtype that holds `levels`
    if levels <= 0xFF:
        dt = np.uint8
    elif levels <= 0xFFFF:
        dt = np.uint16
    elif levels <= 0xFFFFFFFF:
        dt = np.uint32
    else:
        dt = np.uint64
    return codes.astype(dt)


def codelength_bits(codes: np.ndarray, compressor: str = PINNED) -> int:
    """L = 8 * len(COMPRESSOR(codes.tobytes())) in bits."""
    raw = np.ascontiguousarray(codes).tobytes()
    comp = COMPRESSORS[compressor](raw)
    return 8 * len(comp)


def L_b(X: np.ndarray, b: int, compressor: str = PINNED) -> int:
    """Codelength in bits of tensor X at resolution b: quantize then compress.

    Standalone-tensor form: b-bit uniform codes over X's OWN [min,max], exactly
    as the brief specifies L_b(X). For RESIDUALS use residual_codelength()
    instead (see its docstring for why own-range coding is wrong for residuals).
    """
    return codelength_bits(quantize(X, b), compressor=compressor)


def _grid_step(ref: np.ndarray, b: int):
    """LSB step + lo of the b-bit uniform grid over ref's [min,max]."""
    ref = np.asarray(ref, dtype=np.float64)
    lo, hi = float(ref.min()), float(ref.max())
    levels = (1 << b) - 1
    if hi <= lo:
        return None, lo  # degenerate ref -> no scale
    return (hi - lo) / levels, lo


def residual_codelength(R: np.ndarray, ref: np.ndarray, b: int,
                        compressor: str = PINNED) -> int:
    """Codelength in bits of an affine residual R, coded on ref's OWN b-bit grid.

    THE ESTIMATOR SUBTLETY (found empirically; documented in estimator_notes):
    the naive reading "re-quantize R over R's OWN [min,max] then compress" is
    WRONG for a residual. A residual that is essentially zero (e.g. ADD: M is
    exactly affine in A,B, so R_AB is only sub-LSB quantization rounding) gets
    its tiny own-range STRETCHED across the full 2**b code span, turning pure
    rounding hash into a maximum-entropy, INCOMPRESSIBLE tensor -> ~1.05 Mbit at
    b=16. Meanwhile a genuinely structured residual (SYN's 0.5*A*B term) is more
    compressible -> FEWER bits. That inverts the witness (ADD would out-score
    SYN). See diag.py / diag2.py.

    The fix: code R on the SAME grid (same LSB) as the reference signal `ref`
    (here M, the thing whose reconstructability we are measuring). Then
    "residual ~ 0" maps to "~all-zeros -> ~0 bits" and a large structured
    residual maps to real bits, in M's own code units. This is the
    operationalization that makes Syn_wit = bits-of-M-not-affine-reconstructible
    behave as the protocol's P1 witness intends.

    Implementation: codes_i = round((R_i - lo)/step) on ref's [lo,hi] b-bit grid
    (step = ref LSB), shifted to start at 0; compress the integer codes. Codes
    may range WIDER than [0, 2**b-1] when |R| exceeds ref's range (SYN at fine
    b, where the product term blows the residual far past M's span) — that is
    correct: such a residual genuinely costs many bits.
    """
    step, lo = _grid_step(ref, b)
    if step is None:
        # degenerate reference: nothing to code against -> 0 bits
        return 0
    Rf = np.asarray(R, dtype=np.float64)
    codes = np.rint((Rf - lo) / step).astype(np.int64)
    codes = codes - codes.min()  # nonneg, clean dtype, scale-preserving
    return codelength_bits(codes.astype(np.int64), compressor=compressor)


# ----------------------------------------------------------------------------
# Affine reconstruction (least squares on the QUANTIZED codes)
# ----------------------------------------------------------------------------

def affine_residual(Mq: np.ndarray, *parents_q: np.ndarray) -> np.ndarray:
    """Least-squares affine fit of Mq from the parent code tensors + intercept.

    Fits  Mq ~ sum_k a_k * Pq_k + c   via numpy.linalg.lstsq on flattened codes,
    and returns the FLOAT residual R = Mq - fit, same shape as Mq.

    Operates on whatever is passed in — pass the QUANTIZED parents/child (the
    quantize-then-fit order). One parent  -> R_A or R_B; two parents -> R_AB.
    """
    Mf = np.asarray(Mq, dtype=np.float64).ravel()
    cols = [np.asarray(p, dtype=np.float64).ravel() for p in parents_q]
    cols.append(np.ones_like(Mf))  # intercept
    design = np.stack(cols, axis=1)  # (N, k+1)
    coef, *_ = np.linalg.lstsq(design, Mf, rcond=None)
    fit = design @ coef
    resid = (Mf - fit).reshape(np.asarray(Mq).shape)
    return resid


# ----------------------------------------------------------------------------
# The two synergy estimators
# ----------------------------------------------------------------------------

def _residual_codelengths(A, B, M, b, compressor=PINNED):
    """Quantize A,B,M at b (quantize FIRST), fit the three affine residuals,
    and return their codelengths coded on M's OWN b-bit grid.

    Returns (L_RA, L_RB, L_RAB) in bits. The residual codelength uses
    residual_codelength(R, ref=Mq, b) — coding each residual on the merged
    child's code grid (same LSB as M), NOT renormalized over the residual's own
    range. See residual_codelength() for why own-range coding inverts the
    witness. Order is strictly quantize -> fit (lstsq on codes) -> compress.
    """
    Aq = quantize(A, b)
    Bq = quantize(B, b)
    Mq = quantize(M, b)
    R_A = affine_residual(Mq, Aq)
    R_B = affine_residual(Mq, Bq)
    R_AB = affine_residual(Mq, Aq, Bq)
    L_RA = residual_codelength(R_A, Mq, b, compressor)
    L_RB = residual_codelength(R_B, Mq, b, compressor)
    L_RAB = residual_codelength(R_AB, Mq, b, compressor)
    return L_RA, L_RB, L_RAB


def syn_wit(A, B, M, b, compressor=PINNED):
    """WITNESSED synergy (P1 witness): Syn_wit(b) = L_b(R_AB) in bits.

    Bits of M not reconstructible from ANY affine combination of (A, B).
    """
    _, _, L_RAB = _residual_codelengths(A, B, M, b, compressor)
    return L_RAB


def syn_pid(A, B, M, b, compressor=PINNED):
    """NAIVE synergy (BES Thm 4.4 / PID form):
        Syn_pid(b) = min(L_b(R_A), L_b(R_B)) - L_b(R_AB)   in bits.
    """
    L_RA, L_RB, L_RAB = _residual_codelengths(A, B, M, b, compressor)
    return min(L_RA, L_RB) - L_RAB


# ----------------------------------------------------------------------------
# Band sweep
# ----------------------------------------------------------------------------

BAND = [16, 12, 8, 6, 4, 3]   # r_floor = 16 (fine) ... r_top = 3 (coarse ceiling)
R_FLOOR = 16
R_TOP = 3


@dataclass
class BandRow:
    b: int
    L_RA: int
    L_RB: int
    L_RAB: int
    syn_wit: int
    syn_pid: int
    n_elem: int
    syn_wit_per_elem: float = field(init=False)
    syn_pid_per_elem: float = field(init=False)

    def __post_init__(self):
        self.syn_wit_per_elem = self.syn_wit / self.n_elem
        self.syn_pid_per_elem = self.syn_pid / self.n_elem


def band_sweep(A, B, M, band=BAND, compressor=PINNED):
    """Compute both estimators across the whole resolution band.

    Returns a list of BandRow (one per b), most-fine first.
    Normalized bits/element are included (n_elem = M.size).
    """
    n = int(np.asarray(M).size)
    rows = []
    for b in band:
        L_RA, L_RB, L_RAB = _residual_codelengths(A, B, M, b, compressor)
        rows.append(
            BandRow(
                b=b,
                L_RA=L_RA,
                L_RB=L_RB,
                L_RAB=L_RAB,
                syn_wit=L_RAB,
                syn_pid=min(L_RA, L_RB) - L_RAB,
                n_elem=n,
            )
        )
    return rows


def band_sweep_all_compressors(A, B, M, band=BAND):
    """{compressor_name: [BandRow, ...]} for lzma (pinned) + zlib + bz2 siblings."""
    return {name: band_sweep(A, B, M, band=band, compressor=name)
            for name in COMPRESSORS}


# ----------------------------------------------------------------------------
# Null-floor calibration + threshold (lock-before-data rule)
# ----------------------------------------------------------------------------

def bootstrap_sigma_syn_wit(A, B, M, b, n_boot=200, seed=12345, compressor=PINNED):
    """Bootstrap sigma of Syn_wit(b) by resampling elements WITH replacement.

    Resamples the (A,B,M) triples elementwise (paired) so the affine fit and the
    residual codelength are recomputed on each bootstrap draw. Returns the
    standard deviation of Syn_wit across draws, in bits.

    NOTE: resampling reorders/duplicates elements, which changes the compressor's
    achievable codelength somewhat; this is an honest, slightly conservative
    proxy for the sampling sigma of the bits-quantity at this tensor size.
    """
    rng = np.random.default_rng(seed)
    Af = np.asarray(A, dtype=np.float64).ravel()
    Bf = np.asarray(B, dtype=np.float64).ravel()
    Mf = np.asarray(M, dtype=np.float64).ravel()
    n = Af.size
    vals = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        vals[i] = syn_wit(Af[idx], Bf[idx], Mf[idx], b, compressor)
    return float(np.std(vals, ddof=1))


def compute_tau_eff(copy_A, copy_B, copy_M, b=R_TOP, n_boot=200, seed=12345,
                    compressor=PINNED):
    """tau_eff = base_delta + 3*sigma, the lock-before-data threshold.

    base_delta = Syn_wit on the COPY null case at r_top (the realized null floor).
    sigma      = bootstrap sigma of that same quantity.
    k = 1 (single frame, knowledge) => no log2(k) term beyond the 3-sigma band.

    Returns (tau_eff, base_delta, sigma).
    """
    base_delta = syn_wit(copy_A, copy_B, copy_M, b, compressor)
    sigma = bootstrap_sigma_syn_wit(copy_A, copy_B, copy_M, b,
                                    n_boot=n_boot, seed=seed, compressor=compressor)
    tau_eff = base_delta + 3.0 * sigma
    return tau_eff, base_delta, sigma


def verdict_from_band(rows, tau_eff):
    """A case PASSES iff Syn_wit(b) >= tau_eff for EVERY b in the band (incl r_top).

    Returns (passes: bool, per_b: list[(b, syn_wit, bool)]).
    """
    per_b = [(r.b, r.syn_wit, r.syn_wit >= tau_eff) for r in rows]
    passes = all(ok for _, _, ok in per_b)
    return passes, per_b


# ----------------------------------------------------------------------------
# Pretty-print helper
# ----------------------------------------------------------------------------

def format_band_table(rows, title=""):
    lines = []
    if title:
        lines.append(title)
    lines.append(
        f"  {'b':>3}  {'L_RA':>8}  {'L_RB':>8}  {'L_RAB':>8}  "
        f"{'Syn_wit':>9}  {'Syn_pid':>9}  {'wit/elem':>9}  {'pid/elem':>9}"
    )
    for r in rows:
        lines.append(
            f"  {r.b:>3}  {r.L_RA:>8}  {r.L_RB:>8}  {r.L_RAB:>8}  "
            f"{r.syn_wit:>9}  {r.syn_pid:>9}  "
            f"{r.syn_wit_per_elem:>9.4f}  {r.syn_pid_per_elem:>9.4f}"
        )
    return "\n".join(lines)
