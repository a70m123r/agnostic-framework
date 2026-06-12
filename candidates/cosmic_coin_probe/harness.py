# -*- coding: utf-8 -*-
"""
Cosmic-coin probe -- the canonical MDL + appearance-entropy instrument.

Claim under scan (INSTRUMENT register, not pass/fail): for a real phenomenon,
the bits a fair law saves when compressing it = the (in)sharpness of its
appearance. Solomonoff in miniature: p(appearance) = 2^-bits.

Two phenomena at the ends of the coin:
  ORBIT  -- Mars heliocentric position (real, JPL Horizons DE441). The LAW is a
            pure two-body Kepler propagation from the t0 state vector ALONE
            (osculating elements at epoch 0 -> predict all later epochs;
            strictly out-of-sample, no fit). Residual = what two-body misses
            (real perturbations + osculating drift). Expect: tiny residual ->
            few bits -> sharp appearance -> REPLAY face.
  FLARE  -- GOES long-band (0.1-0.8nm) X-ray flux (real, NOAA SWPC). The LAW is
            a fair persistence baseline on log-flux (f_hat(t)=f(t-1)). Residual
            = log-flux increments; tiny in quiet sun, heavy-tailed spikes at
            flare onsets. Expect: poor compression -> many bits at onsets ->
            broad appearance -> SIMULATE face.

DISCLOSED PROXIES (PROXY_SPEC discipline -- these are render/measurement
heuristics with knobs, not laws):
  * coder            : Python lzma preset 9 (pinned). Sibling coders reported by
                       the workflow re-measure phase (zlib/bz2) to test robustness.
  * quantization     : positions 1 km; log10(flux) 1e-3 dex. Same encoding for
                       raw vs residual so the comparison is fair (gain_v2 lesson:
                       compare like-for-like, floor the model).
  * model cost       : Kepler = 6 elements + mu (float64); persistence = 1 number.
                       Negligible vs the series, but COUNTED, never zero.
  * predictive dist  : a single fair common instrument for both -- Gaussian about
                       the model's point prediction with sigma = residual std.
                       (The skeptic phase is invited to give the flare a heavier-
                       tailed predictive dist; the separation should survive.)

NO fabrication. Real fetched data only. This is a scan that LOCATES the coin
edge as an observable; it does not declare a phenomenon "incompressible" (that
stronger claim is handed to the adversary -- a better flare model could close
the gap; the misspecification confound is the same shape as gain_v2's).
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "probe_data"
MU_SUN = 1.32712440018e11  # km^3/s^2  (heliocentric gravitational parameter, IAU)
Q_POS_KM = 1.0             # position quantization (km)
Q_LOGFLUX = 1e-3           # log10-flux quantization (dex)
LOG2E = 1.0 / math.log(2.0)

# --------------------------------------------------------------------------
# coders (pinned lzma primary; zlib/bz2 reported as siblings)
# --------------------------------------------------------------------------
def clen_bits(int_array, coder="lzma"):
    """Codelength in bits of an integer array under a pinned general coder.
    Same dtype/encoding is used for raw and residual so the contrast is fair."""
    b = np.ascontiguousarray(int_array.astype(np.int64)).tobytes()
    if coder == "lzma":
        c = lzma.compress(b, preset=9)
    elif coder == "zlib":
        c = zlib.compress(b, 9)
    elif coder == "bz2":
        c = bz2.compress(b, 9)
    else:
        raise ValueError(coder)
    return len(c) * 8

def gaussian_entropy_bits(sigma, q):
    """Discrete entropy (bits) of a Gaussian source quantized at step q,
    valid for sigma >> q: 0.5*log2(2*pi*e*sigma^2) - log2(q)."""
    sigma = max(float(sigma), 1e-12)
    return 0.5 * math.log2(2 * math.pi * math.e * sigma * sigma) - math.log2(q)

# --------------------------------------------------------------------------
# ORBIT: parse Horizons, two-body propagate from t0 state, residual
# --------------------------------------------------------------------------
def parse_horizons(path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    lines = txt.splitlines()
    try:
        i0 = next(i for i, l in enumerate(lines) if "$$SOE" in l)
        i1 = next(i for i, l in enumerate(lines) if "$$EOE" in l)
    except StopIteration:
        raise RuntimeError("Horizons markers not found")
    jds, R, V = [], [], []
    blk = lines[i0 + 1:i1]
    k = 0
    while k < len(blk):
        head = blk[k]
        if "=" in head and ("A.D." in head or "B.C." in head):
            jd = float(head.split("=")[0].strip())
            xrow = blk[k + 1]; vrow = blk[k + 2]
            def g3(row):
                # rows like " X =-4.38E+07 Y =-2.17E+08 Z =-3.47E+06"
                parts = row.replace("X =", " ").replace("Y =", " ").replace("Z =", " ")
                parts = parts.replace("VX=", " ").replace("VY=", " ").replace("VZ=", " ")
                return [float(t) for t in parts.split()]
            R.append(g3(xrow)); V.append(g3(vrow)); jds.append(jd)
            k += 3
        else:
            k += 1
    return np.array(jds), np.array(R), np.array(V)

def elements_from_rv(r, v, mu):
    R = np.linalg.norm(r); V = np.linalg.norm(v)
    h = np.cross(r, v); H = np.linalg.norm(h)
    n = np.cross([0, 0, 1.0], h); N = np.linalg.norm(n)
    evec = ((V * V - mu / R) * r - np.dot(r, v) * v) / mu
    e = np.linalg.norm(evec)
    energy = V * V / 2 - mu / R
    a = -mu / (2 * energy)
    i = math.acos(np.clip(h[2] / H, -1, 1))
    Om = math.acos(np.clip(n[0] / N, -1, 1));  Om = 2 * math.pi - Om if n[1] < 0 else Om
    om = math.acos(np.clip(np.dot(n, evec) / (N * e), -1, 1));  om = 2 * math.pi - om if evec[2] < 0 else om
    nu = math.acos(np.clip(np.dot(evec, r) / (e * R), -1, 1));  nu = 2 * math.pi - nu if np.dot(r, v) < 0 else nu
    return a, e, i, Om, om, nu

def kepler_E(M, e, tol=1e-12):
    M = (M + math.pi) % (2 * math.pi) - math.pi
    E = M if e < 0.8 else math.pi
    for _ in range(100):
        d = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= d
        if abs(d) < tol:
            break
    return E

def propagate(elem, mu, dt):
    a, e, i, Om, om, nu0 = elem
    E0 = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu0 / 2), math.sqrt(1 + e) * math.cos(nu0 / 2))
    M0 = E0 - e * math.sin(E0)
    nmot = math.sqrt(mu / a ** 3)
    M = M0 + nmot * dt
    E = kepler_E(M, e)
    nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
    r = a * (1 - e * math.cos(E))
    # perifocal -> inertial via 3-1-3 (Om, i, om)
    rp = np.array([r * math.cos(nu), r * math.sin(nu), 0.0])
    cO, sO, ci, si, cw, sw = math.cos(Om), math.sin(Om), math.cos(i), math.sin(i), math.cos(om), math.sin(om)
    Rm = np.array([
        [cO * cw - sO * sw * ci, -cO * sw - sO * cw * ci,  sO * si],
        [sO * cw + cO * sw * ci, -sO * sw + cO * cw * ci, -cO * si],
        [sw * si,                 cw * si,                 ci]])
    return Rm @ rp

def analyze_orbit():
    jd, R, V = parse_horizons(DATA / "mars_horizons_raw.txt")
    secs = (jd - jd[0]) * 86400.0
    elem = elements_from_rv(R[0], V[0], MU_SUN)
    pred = np.array([propagate(elem, MU_SUN, dt) for dt in secs])
    resid = R - pred                        # km, 3-vector per epoch
    rabs = np.linalg.norm(resid, axis=1)
    # MDL via pinned coder: same int64 km encoding for raw vs residual
    raw_i = np.round(R / Q_POS_KM).astype(np.int64).reshape(-1)
    res_i = np.round(resid / Q_POS_KM).astype(np.int64).reshape(-1)
    out = {}
    for coder in ("lzma", "zlib", "bz2"):
        raw_b = clen_bits(raw_i, coder)
        res_b = clen_bits(res_i, coder)
        model_b = 7 * 64  # 6 elements + mu, float64; counted not zero
        out[coder] = dict(raw_bits=raw_b, resid_bits=res_b, model_bits=model_b,
                          comp_ratio=raw_b / (res_b + model_b))
    # analytic appearance-entropy (fair common Gaussian instrument), bits/step
    # v0.2 (2026-06-13, external-pass fix): SUM per-axis entropies, do NOT take the
    # mean of the per-axis sigmas and multiply by 3 (Jensen: log is concave, so the
    # mean-sigma form OVERSTATES the floor). Two sigma-shrink conventions are emitted
    # NAMED; the per-dimension mean-of-log-ratios is primary (each axis's own shrink).
    sig_raw_ax = np.std(R, axis=0)            # per-axis (3,)
    sig_res_ax = np.std(resid, axis=0)        # per-axis (3,)
    H_raw = float(sum(gaussian_entropy_bits(s, Q_POS_KM) for s in sig_raw_ax))   # per-axis SUM
    H_app = float(sum(gaussian_entropy_bits(s, Q_POS_KM) for s in sig_res_ax))
    sigma_shrink = dict(
        per_dim_mean_of_log_ratios=float(np.mean(np.log2(sig_raw_ax / sig_res_ax))),   # PRIMARY
        log_of_ratio_of_mean_sigmas=float(math.log2(sig_raw_ax.mean() / sig_res_ax.mean())),  # Jensen-biased convention
        per_axis_bits=[float(x) for x in np.log2(sig_raw_ax / sig_res_ax)])
    # per-step NLL (bits) under a DEBIASED Gaussian N(pred + mu_res, sig_res^2) --
    # v0.2 fix: the residual carries a non-zero per-axis mean (osculating drift); the
    # v0.1 NLL used uncentered resid^2 against the mean-subtracted sigma (miscentered
    # by ~0.9 bits). Debias the predictor by mu_res, then the quadratic uses (resid-mu).
    mu_res = resid.mean(axis=0)
    sig = sig_res_ax
    cres = resid - mu_res
    nll = 0.5 * np.sum(np.log2(2 * math.pi * sig ** 2) + (cres ** 2) / (sig ** 2) * LOG2E, axis=1) - 3 * math.log2(Q_POS_KM)
    rng = np.random.default_rng(0)
    sample = pred + mu_res + rng.normal(0, sig, size=pred.shape)   # a draw from the debiased predictive
    return dict(
        n=len(jd), span_days=float(jd[-1] - jd[0]),
        elements=dict(a_km=elem[0], e=elem[1], i_deg=math.degrees(elem[2])),
        resid_km=dict(mean=float(rabs.mean()), p50=float(np.percentile(rabs, 50)),
                      p99=float(np.percentile(rabs, 99)), max=float(rabs.max())),
        orbit_radius_km=float(np.linalg.norm(R, axis=1).mean()),
        rel_resid=float(rabs.mean() / np.linalg.norm(R, axis=1).mean()),
        mdl=out,
        appearance_bits_per_step=H_app, raw_bits_per_step=H_raw,
        bits_saved_per_step=H_raw - H_app,
        sigma_shrink_bits_per_dim=sigma_shrink,
        nll_bits=dict(mean=float(nll.mean()), p50=float(np.percentile(nll, 50)),
                      p99=float(np.percentile(nll, 99)), max=float(nll.max())),
        disclosures=["H_raw is an iid-Gaussian marginal proxy (orbit raw is a smooth"
                      " sinusoid; the real coders beat it -- see mdl). sigmas fit in-sample"
                      " on the evaluated residual (calibration bits NOT counted) -- exploratory,"
                      " not confirmatory. Model bits charge only Kepler's 6 elements + mu, NOT the"
                      " law/program (conditional MDL, not algorithmic probability)."],
        _nll_series=nll, _resid=resid, _truth=R, _pred=pred, _sample=sample,
    )

# --------------------------------------------------------------------------
# FLARE: parse GOES long band, persistence baseline on log-flux
# --------------------------------------------------------------------------
def analyze_flare():
    rows = json.loads((DATA / "goes_xray_7day.json").read_text(encoding="utf-8"))
    long = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    long.sort(key=lambda r: r["time_tag"])
    flux = np.array([r["flux"] for r in long], dtype=float)
    flux = np.clip(flux, 1e-9, None)
    flux = flux[np.isfinite(flux)]
    lf = np.log10(flux)                       # work in log-flux (spans orders of mag)
    pred = np.empty_like(lf); pred[0] = lf[0]; pred[1:] = lf[:-1]   # persistence f_hat(t)=f(t-1)
    resid = lf - pred                          # log-flux increments
    raw_i = np.round(lf / Q_LOGFLUX).astype(np.int64)
    res_i = np.round(resid / Q_LOGFLUX).astype(np.int64)
    out = {}
    for coder in ("lzma", "zlib", "bz2"):
        raw_b = clen_bits(raw_i, coder); res_b = clen_bits(res_i, coder)
        out[coder] = dict(raw_bits=raw_b, resid_bits=res_b, model_bits=64,
                          comp_ratio=raw_b / (res_b + 64))
    sig_raw = float(np.std(lf)); sig_res = float(np.std(resid))
    H_raw = gaussian_entropy_bits(sig_raw, Q_LOGFLUX)
    H_app = gaussian_entropy_bits(sig_res, Q_LOGFLUX)
    sigma_shrink = dict(per_dim_mean_of_log_ratios=float(math.log2(sig_raw / sig_res)))
    # v0.2: debias by the (near-zero) increment mean, matching the orbit treatment
    mu_res = float(resid.mean()); cres = resid - mu_res
    nll = 0.5 * (np.log2(2 * math.pi * sig_res ** 2) + (cres ** 2) / (sig_res ** 2) * LOG2E) - math.log2(Q_LOGFLUX)
    rng = np.random.default_rng(0)
    sample = pred + mu_res + rng.normal(0, sig_res, size=pred.shape)
    # flare census (NOAA classes by long-band flux: C>=1e-6, M>=1e-5, X>=1e-4)
    peak = float(flux.max())
    cls = ("X" if peak >= 1e-4 else "M" if peak >= 1e-5 else "C" if peak >= 1e-6 else "B/A")
    return dict(
        n=len(lf), peak_flux=peak, peak_class=cls,
        resid_log_flux_std=sig_res,    # v0.2: renamed from log_flux_std (it is the RESIDUAL std)
        mdl=out,
        appearance_bits_per_step=H_app, raw_bits_per_step=H_raw,
        bits_saved_per_step=H_raw - H_app,
        sigma_shrink_bits_per_dim=sigma_shrink,
        nll_bits=dict(mean=float(nll.mean()), p50=float(np.percentile(nll, 50)),
                      p99=float(np.percentile(nll, 99)), max=float(nll.max())),
        disclosures=["H_raw models the whole autocorrelated, non-stationary log-flux as a"
                      " SINGLE iid Gaussian -- a loose marginal proxy that INFLATES bits-saved"
                      " (a bad model for raw flux flatters the persistence law's gain). Treat"
                      " raw_bits_per_step as an upper-bound reference, not the entropy rate."
                      " sigmas fit in-sample; calibration bits not counted (exploratory)."],
        _nll_series=nll, _resid=resid, _truth=lf, _pred=pred, _sample=sample,
    )

# --------------------------------------------------------------------------
def main():
    orb = analyze_orbit(); fla = analyze_flare()
    # save arrays for the workflow re-measure/adversary phases
    np.savez(HERE / "probe_data" / "series.npz",
             orbit_nll=orb["_nll_series"], orbit_resid=orb["_resid"],
             orbit_truth=orb["_truth"], orbit_pred=orb["_pred"], orbit_sample=orb["_sample"],
             flare_nll=fla["_nll_series"], flare_resid=fla["_resid"],
             flare_truth=fla["_truth"], flare_pred=fla["_pred"], flare_sample=fla["_sample"])
    for d in (orb, fla):
        for k in list(d):
            if k.startswith("_"):
                del d[k]
    results = dict(
        probe="cosmic_coin v0.2", coder_primary="lzma-9",
        v02_corrections="2026-06-13 external-pass fixes: per-axis-SUM entropy (was mean-sigma x3, Jensen); "
                        "DEBIASED NLL (was uncentered against drift mean); sigma-shrink emitted with NAMED "
                        "convention (per_dim_mean_of_log_ratios PRIMARY vs log_of_ratio_of_mean_sigmas); "
                        "disclosures added (flare H_raw iid-proxy inflation; in-sample calibration; conditional MDL). "
                        "The attack_misspec2 orbit-Student-t Q bug is fixed separately (t is NEUTRAL on orbit, 41.10).",
        quant=dict(pos_km=Q_POS_KM, logflux_dex=Q_LOGFLUX),
        orbit=orb, flare=fla,
        coin_edge=dict(
            orbit_comp_ratio=orb["mdl"]["lzma"]["comp_ratio"],
            flare_comp_ratio=fla["mdl"]["lzma"]["comp_ratio"],
            separation_comp=orb["mdl"]["lzma"]["comp_ratio"] / fla["mdl"]["lzma"]["comp_ratio"],
            # PRIMARY cross-phenomenon observable (quant-invariant, dimensionless):
            orbit_sigma_shrink_per_dim=orb["sigma_shrink_bits_per_dim"]["per_dim_mean_of_log_ratios"],
            flare_sigma_shrink_per_dim=fla["sigma_shrink_bits_per_dim"]["per_dim_mean_of_log_ratios"],
            # absolute appearance bits are UNIT-INCOMMENSURATE across phenomena (E-units guard) -- kept only as a within-phenomenon number, NEVER differenced across:
            orbit_appearance_bits=orb["appearance_bits_per_step"],
            flare_appearance_bits=fla["appearance_bits_per_step"],
            _absolute_bits_gap_DO_NOT_USE=fla["appearance_bits_per_step"] - orb["appearance_bits_per_step"],
        ),
    )
    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    # headline
    print("=" * 64)
    print("COSMIC-COIN PROBE -- headline (pinned lzma-9, real data)")
    print("=" * 64)
    o, f = orb["mdl"]["lzma"], fla["mdl"]["lzma"]
    print(f"ORBIT (Mars, {orb['n']}d)  two-body-vs-DE441")
    print(f"   rel.residual      : {orb['rel_resid']:.2e}  (mean {orb['resid_km']['mean']:.0f} km / {orb['orbit_radius_km']:.3e} km)")
    print(f"   lzma comp ratio   : {o['comp_ratio']:.2f}x   (raw {o['raw_bits']} -> resid {o['resid_bits']} bits)")
    print(f"   appearance entropy: {orb['appearance_bits_per_step']:.2f} bits/step   (raw {orb['raw_bits_per_step']:.2f})")
    print(f"   per-step NLL      : mean {orb['nll_bits']['mean']:.2f}  p99 {orb['nll_bits']['p99']:.2f}  max {orb['nll_bits']['max']:.2f} bits")
    print(f"FLARE (GOES long, {fla['n']}m)  persistence baseline   peak {fla['peak_flux']:.2e} W/m2 ({fla['peak_class']}-class)")
    print(f"   lzma comp ratio   : {f['comp_ratio']:.2f}x   (raw {f['raw_bits']} -> resid {f['resid_bits']} bits)")
    print(f"   appearance entropy: {fla['appearance_bits_per_step']:.2f} bits/step   (raw {fla['raw_bits_per_step']:.2f})")
    print(f"   per-step NLL      : mean {fla['nll_bits']['mean']:.2f}  p99 {fla['nll_bits']['p99']:.2f}  max {fla['nll_bits']['max']:.2f} bits")
    print("-" * 64)
    ce = results["coin_edge"]
    print("-" * 64)
    print(f"COIN EDGE (dimensionless)  comp-ratio separation {ce['separation_comp']:.2f}x")
    print(f"   sigma-shrink/dim (PRIMARY, quant-invariant): orbit {ce['orbit_sigma_shrink_per_dim']:.2f} vs flare {ce['flare_sigma_shrink_per_dim']:.2f} bits/dim")
    print(f"   orbit -> {'SHARP/REPLAY' if ce['orbit_comp_ratio']>ce['flare_comp_ratio'] else '??'}  | flare -> {'FUZZY/SIMULATE' if ce['flare_comp_ratio']<ce['orbit_comp_ratio'] else '??'}")
    print(f"   (absolute appearance-bits are unit-incommensurate -- NOT differenced across phenomena; E-units guard)")
    print("results.json + probe_data/series.npz written")

if __name__ == "__main__":
    main()
