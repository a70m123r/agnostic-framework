"""
Generate the 12-panel log-log fluctuation (Welch PSD) plot for Pilot #150.

Layout: 6 rows (one per pre-registered pair) x 2 columns
(left = authoritarian, right = open pluralistic). Each panel shows the Welch
power spectral density of the PRIMARY signal (category_entropy) on log-log axes,
the pre-registered fit window f in [1/365, 1/10] cycles/day shaded, and the
fitted slope line whose negative slope is the spectral exponent beta.

H1 (β_authoritarian < β_pluralistic − 0.10) reads off the figure as: left-column
slopes flatter (smaller β, closer to white noise) than right-column slopes.

Reads:  data/raw/<label>_category_entropy.csv  +  results/gdelt_results.json
Writes: results/log_log_plot.png
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pilot

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "raw"
RESULTS = HERE / "results"
SIGNAL = "category_entropy"
F_LOW, F_HIGH = 1 / 365, 1 / 10


def panel(ax, label, beta_record):
    _, raw = pilot._load_raw_signal(RAW, label, SIGNAL)
    z, gap = pilot._preprocess(raw)
    f, psd = pilot._welch_psd(z, fs=1.0, nperseg=min(512, len(z) // 4),
                              noverlap=min(512, len(z) // 4) // 2, detrend="linear")
    m = (f > 0) & (psd > 0)
    f, psd = f[m], psd[m]
    ax.loglog(f, psd, ".", ms=2.0, color="0.65", alpha=0.55, zorder=1)

    # pre-registered fit window
    ax.axvspan(F_LOW, F_HIGH, color="#cfe3ff", alpha=0.45, zorder=0)
    win = (f >= F_LOW) & (f <= F_HIGH)
    beta = beta_record["welch_beta"]
    if win.sum() >= 4:
        # fit line: log10(psd) = -beta*log10(f) + c  ->  recover c from window
        c = np.mean(np.log10(psd[win]) + beta * np.log10(f[win]))
        ff = np.array([F_LOW, F_HIGH])
        ax.loglog(ff, 10 ** (-beta * np.log10(ff) + c), "-", color="#c1121f",
                  lw=2.0, zorder=3)

    miss = gap["frac_missing"] * 100
    miss_txt = f"  (miss {miss:.0f}%)" if miss > 0.5 else ""
    ax.set_title(f"{label}   β={beta:+.2f}{miss_txt}", fontsize=9)
    ax.tick_params(labelsize=7)
    ax.grid(True, which="both", ls=":", lw=0.4, alpha=0.5)


def main():
    res = json.load(open(RESULTS / "gdelt_results.json", encoding="utf-8"))
    per = res["per_country"][SIGNAL]
    prim = res["results_by_signal"][SIGNAL]

    fig, axes = plt.subplots(6, 2, figsize=(9, 15), sharex=True)
    for row, (auth, plur) in enumerate(pilot.GDELT_PAIRS):
        panel(axes[row, 0], auth, per[auth])
        panel(axes[row, 1], plur, per[plur])
    axes[0, 0].set_title(f"AUTHORITARIAN\n{axes[0,0].get_title()}", fontsize=9)
    axes[0, 1].set_title(f"OPEN PLURALISTIC\n{axes[0,1].get_title()}", fontsize=9)
    for ax in axes[-1, :]:
        ax.set_xlabel("frequency (cycles/day)", fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel("PSD", fontsize=8)

    verdict = prim["verdict"]
    fig.suptitle(
        f"Pilot #150 — Welch PSD of GDELT v2 event-category-entropy (2015–2026)\n"
        f"H1: β_auth < β_plur − 0.10   |   Δβ={prim['observed_delta_mean']:+.3f}, "
        f"d={prim['cohens_d']:+.3f}, p={prim['p_value']:.4f}   →   {verdict}",
        fontsize=11, y=0.997)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "log_log_plot.png"
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
