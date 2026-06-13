# -*- coding: utf-8 -*-
import json, math, pathlib
import numpy as np
HERE = pathlib.Path("D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/q6_scale_rung")
rows = json.load(open(HERE/"autocorr_mechanism_rows.json"))
def spear(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    ra=np.argsort(np.argsort(a)).astype(float);rb=np.argsort(np.argsort(b)).astype(float)
    ra-=ra.mean();rb-=rb.mean();return float(np.dot(ra,rb)/math.sqrt(np.dot(ra,ra)*np.dot(rb,rb)))
# within the claim-bearing column
fd=[r for r in rows if r["series"]=="flare_REAL" and r["method"]=="decimate"]
cr=[r["comp_ratio"] for r in fd]; rho=[r["lag1_autocorr"] for r in fd]; ss=[r["sigma_shrink_bits"] for r in fd]
print("FLARE-DECIMATE column (claim-bearing):")
print(f"  Spearman(comp_ratio, autocorr) within column = {spear(cr,rho):+.3f}")
print(f"  Spearman(sigma_shrink, autocorr) within column= {spear(ss,rho):+.3f}")
print(f"  comp_ratio span: {cr[0]:.3f} (rho={rho[0]:.3f}) -> {cr[-1]:.3f} (rho={rho[-1]:.3f})")
# why comp_ratio is a looser global readout than sigma-shrink: model floor + small-n coder overhead
print("\nWhy comp_ratio tracks looser than sigma-shrink: model_b=64 floor + lzma marginal entropy.")
for r in fd:
    overhead = 64.0/(r["resid_bits"]+64.0)
    print(f"  r={r['rung']:<3d} n={r['n']:<6d} model-floor share of resid budget = {overhead*100:5.2f}%")
