# fetch_align.py — S1 drag-synergy DATA seat: parse + align GRACE-FO density x OMNI2 drivers
# Register: exploratory instrument, NO fabrication — every number traces to the cached files below.
# Inputs (already fetched, cached in ./data/):
#   GC_DNS_ACC_2024_{03..07}_v02c.zip  TU Delft thermosphere POD/ACC density (GRACE C = GRACE-FO 1)
#       http://thermosphere.tudelft.nl/data/data/version_02/GRACE-FO_data/   (CC BY 4.0)
#   omni2_2024.dat + omni2_format.txt  SPDF OMNI2 hourly
#       https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/
# Output: data/s1_aligned_hourly.csv + data/s1_provenance.json
#
# Disclosed processing decisions (v0):
#  D1  Density = GRACE-FO accelerometer-derived (col 9) AND the source's running
#      orbit-average (col 10). The ORBIT-AVERAGE channel is the primary variable:
#      one GRACE-FO orbit (~94 min) sweeps both LST sectors and the full altitude
#      range, so orbit-averaging is the v0 normalization for the local-solar-time
#      (diurnal tide) and along-orbit altitude confounds. Point density kept as a
#      secondary column; latitude/LST/altitude hourly means kept as covariates.
#  D2  NO fixed-altitude renormalization applied (no model ratio used — keeps the
#      chain model-free). Hourly mean altitude is a column; the inter-month orbit
#      decay (~few km) and storm-time contraction are left to the MODEL seat as a
#      covariate. DISCLOSED, not solved.
#  D3  GRACE-FO timestamps are GPS time; GPS-UTC = +18 s in 2024. Shifted by -18 s
#      to UTC before hourly binning (negligible vs 1 h bins, applied anyway).
#  D4  Hourly bin = calendar UTC hour [HH:00, HH+1:00). Mean over flag==0 samples
#      only (flag per channel); bins with zero valid samples -> empty cells.
#  D5  OMNI2 F10.7 is a daily value replicated across the 24 hourly records by the
#      source (verified day 132) — taken as-is = the forward-fill the task asks for.
#      F10.7_81d = centered 81-day mean of the daily series, computable for the
#      whole window from omni2_2024.dat alone (window doy 61..213 needs 21..253).
#  D6  Fill-value handling per omni2.text: Kp*10=99, Dst=99999, ap=999, F10.7=999.9
#      -> empty cells, counted in provenance.
#  D7  LST hourly mean is a CIRCULAR mean (24 h wrap). GRACE-FO samples two LST
#      sectors ~12 h apart each orbit, so the point-density LST covariate is
#      bimodal — another reason the orbit-average channel is primary.

import json, zipfile, hashlib, math, csv
from datetime import datetime, timezone
import numpy as np

DATA = "D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/s1_drag_synergy/data"
W_START = datetime(2024, 3, 1, 0, tzinfo=timezone.utc)
W_END   = datetime(2024, 7, 31, 23, tzinfo=timezone.utc)   # inclusive hour
H0 = int(W_START.timestamp()) // 3600
H1 = int(W_END.timestamp()) // 3600
NH = H1 - H0 + 1
GPS_MINUS_UTC = 18.0  # s, valid 2017->present (no leap second since)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------- GRACE-FO ----------------
months = ["03", "04", "05", "06", "07"]
acc = {}  # hourbin -> accumulators
n_rows = n_flag_dens = n_flag_mean = 0
tsys_seen = set()
for m in months:
    zp = f"{DATA}/GC_DNS_ACC_2024_{m}_v02c.zip"
    z = zipfile.ZipFile(zp)
    name = z.namelist()[0]
    with z.open(name) as f:
        for raw in f:
            line = raw.decode("ascii", "replace")
            if line.startswith("#"):
                continue
            w = line.split()
            if len(w) < 12:
                continue
            n_rows += 1
            tsys_seen.add(w[2])
            # epoch from date+time (GPS), shift to UTC
            d, t = w[0], w[1]
            ep = datetime(int(d[0:4]), int(d[5:7]), int(d[8:10]),
                          int(t[0:2]), int(t[3:5]), tzinfo=timezone.utc).timestamp() \
                 + float(t[6:]) - GPS_MINUS_UTC
            hb = int(ep // 3600)
            if hb < H0 or hb > H1:
                continue
            a = acc.setdefault(hb, [0.0,0,  0.0,0,  0.0,0.0,0.0,0.0, 0])
            # [rho_pt_sum, n_pt, rho_om_sum, n_om, alt_sum, lat_sum, lst_sin, lst_cos, n_all]
            alt = float(w[3]); lat = float(w[5]); lst = float(w[6])
            rho = float(w[8]); rho_om = float(w[9])
            fd = float(w[10]); fm = float(w[11])
            if fd == 0.0:
                a[0] += rho; a[1] += 1
            else:
                n_flag_dens += 1
            if fm == 0.0:
                a[2] += rho_om; a[3] += 1
            else:
                n_flag_mean += 1
            ang = lst / 24.0 * 2.0 * math.pi
            a[4] += alt; a[5] += lat; a[6] += math.sin(ang); a[7] += math.cos(ang); a[8] += 1

# ---------------- OMNI2 ----------------
omni = {}   # hourbin -> (kp10, dst, ap, f107)
f107_daily = {}  # doy -> value
n_fill = {"kp": 0, "dst": 0, "ap": 0, "f107": 0}
with open(f"{DATA}/omni2_2024.dat") as f:
    for line in f:
        w = line.split()
        yr, doy, hr = int(w[0]), int(w[1]), int(w[2])
        ep = datetime(yr, 1, 1, tzinfo=timezone.utc).timestamp() + (doy - 1) * 86400 + hr * 3600
        hb = int(ep // 3600)
        kp10 = int(w[38]); dst = int(w[40]); ap = int(w[49]); f107 = float(w[50])
        if kp10 == 99: kp10 = None; n_fill["kp"] += 1
        if dst == 99999: dst = None; n_fill["dst"] += 1
        if ap == 999: ap = None; n_fill["ap"] += 1
        if f107 == 999.9: f107 = None; n_fill["f107"] += 1
        omni[hb] = (kp10, dst, ap, f107)
        if f107 is not None and doy not in f107_daily:
            f107_daily[doy] = f107

# 81-day centered mean of daily F10.7
f107_81d = {}
for doy in range(1, 367):
    vals = [f107_daily[d] for d in range(doy - 40, doy + 41) if d in f107_daily]
    if len(vals) == 81:
        f107_81d[doy] = sum(vals) / len(vals)

# ---------------- align + write ----------------
rows = []
n_dens_hours = 0
for hb in range(H0, H1 + 1):
    dt = datetime.fromtimestamp(hb * 3600, tz=timezone.utc)
    doy = dt.timetuple().tm_yday
    a = acc.get(hb)
    if a and a[8] > 0:
        rho_pt = a[0] / a[1] if a[1] > 0 else None
        rho_om = a[2] / a[3] if a[3] > 0 else None
        alt = a[4] / a[8]; lat = a[5] / a[8]
        lst = (math.atan2(a[6] / a[8], a[7] / a[8]) / (2 * math.pi) * 24.0) % 24.0
        n_s = a[8]
        if rho_om is not None:
            n_dens_hours += 1
    else:
        rho_pt = rho_om = alt = lat = lst = None; n_s = 0
    kp10, dst, ap, f107 = omni.get(hb, (None, None, None, None))
    f81 = f107_81d.get(doy)
    rows.append([dt.strftime("%Y-%m-%dT%H:00:00Z"), dt.year, doy, dt.hour,
                 rho_om, rho_pt, n_s, alt, lat, lst, f107, f81, dst, kp10, ap])

hdr = ["datetime_utc", "year", "doy", "hour",
       "rho_orbit_kgm3", "rho_point_kgm3", "n_dens_samples",
       "alt_mean_m", "lat_mean_deg", "lst_circmean_h",
       "f107_sfu", "f107_81d_sfu", "dst_nt", "kp10", "ap_nt"]
def fmt(v):
    if v is None: return ""
    if isinstance(v, float): return f"{v:.6g}"
    return str(v)
out_csv = f"{DATA}/s1_aligned_hourly.csv"
with open(out_csv, "w", newline="") as f:
    wcsv = csv.writer(f)
    wcsv.writerow(hdr)
    for r in rows:
        wcsv.writerow([fmt(v) for v in r])

# ---------------- sanity checks (no plots, printed + recorded) ----------------
R = {h: r for h, r in zip(range(H0, H1 + 1), rows)}
dsts = [(r[12], r[0]) for r in rows if r[12] is not None]
dst_min, dst_min_t = min(dsts)
n_dst_lt_400 = sum(1 for d, _ in dsts if d < -400)
n_dst_lt_300 = sum(1 for d, _ in dsts if d < -300)

om_valid = [(r[4], r[0]) for r in rows if r[4] is not None]
rho_max, rho_max_t = max(om_valid)
# quiet baseline: March+April median of orbit-mean density
quiet = sorted(r[4] for r in rows if r[4] is not None and r[0] < "2024-05-01")
quiet_med = quiet[len(quiet) // 2]
spike_ratio = rho_max / quiet_med
# coincidence: |t(rho_max) - t(dst_min)| in hours
t_rho = datetime.strptime(rho_max_t, "%Y-%m-%dT%H:00:00Z")
t_dst = datetime.strptime(dst_min_t, "%Y-%m-%dT%H:00:00Z")
lag_h = (t_rho - t_dst).total_seconds() / 3600

f107s = sorted(r[10] for r in rows if r[10] is not None)
alts = [r[7] for r in rows if r[7] is not None]
n_missing_dens = NH - n_dens_hours
n_f107_gt200_days = len({r[2] for r in rows if r[10] is not None and r[10] > 200})

sanity = {
    "n_hours_grid": NH,
    "n_hours_with_density": n_dens_hours,
    "n_hours_density_missing": n_missing_dens,
    "grace_rows_parsed": n_rows,
    "grace_rows_flagged_point": n_flag_dens,
    "grace_rows_flagged_orbitavg": n_flag_mean,
    "grace_time_systems_seen": sorted(tsys_seen),
    "omni_fill_counts_full2024": n_fill,
    "dst_min_nt": dst_min, "dst_min_time": dst_min_t,
    "n_hours_dst_below_-400": n_dst_lt_400,
    "n_hours_dst_below_-300": n_dst_lt_300,
    "rho_orbit_max_kgm3": rho_max, "rho_orbit_max_time": rho_max_t,
    "quiet_median_rho_orbit_MarApr_kgm3": quiet_med,
    "storm_spike_ratio_max_over_quiet_median": spike_ratio,
    "rho_peak_minus_dst_min_hours": lag_h,
    "f107_min_sfu": f107s[0], "f107_max_sfu": f107s[-1],
    "f107_median_sfu": f107s[len(f107s) // 2],
    "n_days_f107_above_200sfu": n_f107_gt200_days,
    "alt_min_m": min(alts), "alt_max_m": max(alts),
}
for k, v in sanity.items():
    print(f"{k}: {v}")

# ---------------- provenance ----------------
import os
def mtime_utc(p):
    return datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
fetched_grace = {f"GC_DNS_ACC_2024_{m}_v02c.zip": mtime_utc(f"{DATA}/GC_DNS_ACC_2024_{m}_v02c.zip") for m in months}
fetched_omni = {p: mtime_utc(f"{DATA}/{p}") for p in ("omni2_2024.dat", "omni2_format.txt")}

# contiguous missing-density blocks (for the data-notes record)
miss_hb = sorted(hb for hb, r in zip(range(H0, H1 + 1), rows) if r[4] is None)
miss_blocks = []
for hb in miss_hb:
    if miss_blocks and hb == miss_blocks[-1][1] + 1:
        miss_blocks[-1][1] = hb
    else:
        miss_blocks.append([hb, hb])
miss_blocks = [[datetime.fromtimestamp(a * 3600, tz=timezone.utc).strftime("%Y-%m-%dT%H:00Z"),
                datetime.fromtimestamp(b * 3600, tz=timezone.utc).strftime("%Y-%m-%dT%H:00Z")]
               for a, b in miss_blocks]
prov = {
    "experiment": "s1_drag_synergy / DATA seat",
    "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "window_utc": "2024-03-01T00:00Z .. 2024-07-31T23:00Z inclusive, hourly",
    "n_hours_grid": NH,
    "density": {
        "source": "TU Delft thermosphere data portal, version_02 GRACE-FO (GRACE C / GRACE-FO 1), accelerometer-derived neutral density v02c",
        "urls": [f"http://thermosphere.tudelft.nl/data/data/version_02/GRACE-FO_data/GC_DNS_ACC_2024_{m}_v02c.zip" for m in months],
        "license": "CC BY 4.0 (header in each file)",
        "reference": "Siemes et al., J. Space Weather Space Clim. 2023 (CHAMP/GRACE/GRACE-FO v2 density+crosswind datasets); README http://thermosphere.tudelft.nl/data/README.txt",
        "cadence_native": "10 s",
        "units": "kg m^-3",
        "files": {f"GC_DNS_ACC_2024_{m}_v02c.zip": {"sha256": sha256(f"{DATA}/GC_DNS_ACC_2024_{m}_v02c.zip"),
                                                    "fetched_utc": fetched_grace[f"GC_DNS_ACC_2024_{m}_v02c.zip"]} for m in months},
    },
    "drivers": {
        "source": "NASA SPDF OMNI2 hourly (low_res_omni), omni2_2024.dat",
        "urls": ["https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2_2024.dat",
                 "https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2.text"],
        "fields": {"kp10": "word 39 (Kp*10)", "dst_nt": "word 41 (Kyoto Dst, nT)",
                   "ap_nt": "word 50 (ap, nT)", "f107_sfu": "word 51 (F10.7, sfu, daily replicated hourly by source)"},
        "files": {p: {"sha256": sha256(f"{DATA}/{p}"), "fetched_utc": fetched_omni[p]}
                  for p in ("omni2_2024.dat", "omni2_format.txt")},
    },
    "data_notes": [
        f"missing-density blocks (contiguous, UTC): {miss_blocks} — single GRACE-FO gap, far from the storm",
        "F10.7 outlier: 2024-07-30 daily value 412.9 sfu (only day >250 in window) — consistent with radio-burst contamination of the daily measurement; MODEL seat should cap/log-transform or exclude (known F10.7>200 nonlinearity confound)",
        "50 days in window have F10.7 > 200 sfu (solar-max saturation regime — disclosed confound)",
        "hourly mean of POINT density (secondary col) under-cancels LST/altitude within a bin: 1 h = 0.63 orbit; the ORBIT-AVERAGE channel does not have this problem (each 10-s sample of col 10 is already a full-orbit average)",
    ],
    "processing_decisions": [
        "D1 primary density = hourly mean of the source's running ORBIT-AVERAGE density (col 10, flag==0): one ~94-min orbit sweeps both LST sectors + full along-orbit altitude range, so orbit-averaging is the v0 normalization for the LST/diurnal and along-orbit-altitude confounds; point density (col 9) kept as secondary column",
        "D2 NO fixed-altitude renormalization (model-free chain); hourly mean altitude kept as covariate column; secular decay + storm-time orbit contraction left to MODEL seat — disclosed, not solved",
        "D3 GRACE-FO times are GPS; shifted -18 s to UTC before binning (GPS-UTC=18 s, 2017->present)",
        "D4 hourly bin = calendar UTC hour; mean over flag==0 samples per channel; empty bins -> empty cells",
        "D5 OMNI2 F10.7 daily value replicated hourly by the source (verified day 132) = the forward-fill; f107_81d = centered 81-day mean of the daily series (window doy 61..213 fully covered by 2024 file)",
        "D6 OMNI2 fills (Kp*10=99, Dst=99999, ap=999, F10.7=999.9) -> empty cells, counted",
        "D7 hourly LST = circular mean (24 h wrap); bimodal for point density (two LST sectors per orbit) — orbit-average channel is primary partly for this reason",
        "hemispheric stratification NOT done in v0 (known Gannon N/S asymmetry confound — disclosed for MODEL/adversary seats; raw 10-s files cached for re-binning)",
    ],
    "aligned_csv": out_csv.replace("/", "\\"),
    "columns": hdr,
    "sanity": sanity,
}
with open(f"{DATA}/s1_provenance.json", "w") as f:
    json.dump(prov, f, indent=1)
print("\nwrote:", out_csv)
print("wrote:", f"{DATA}/s1_provenance.json")
