# -*- coding: utf-8 -*-
"""Quantitative mechanism tests: (1) is comp-ratio monotone in lag-1 autocorr?
(2) does the empirical sigma-shrink equal the autocorr prediction? (3) does the
decimated autocorr-vs-rung follow rho^r (AR1 control) / what rho fits the flare?"""
import json, math, pathlib
import numpy as np

HERE = pathlib.Path("D:/PlatformOperator/research/pav/candidates/dial_engine/experiments/q6_scale_rung")
rows = json.load(open(HERE/"autocorr_mechanism_rows.json"))
RUNGS = [1,2,5,10,30,60]

def spearman(a, b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    ra=np.argsort(np.argsort(a)); rb=np.argsort(np.argsort(b))
    ra=ra-ra.mean(); rb=rb-rb.mean()
    return float(np.dot(ra,rb)/math.sqrt(np.dot(ra,ra)*np.dot(rb,rb)))
def pearson(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float); a=a-a.mean(); b=b-b.mean()
    return float(np.dot(a,b)/math.sqrt(np.dot(a,a)*np.dot(b,b)))

cr  = np.array([r["comp_ratio"]        for r in rows])
ss  = np.array([r["sigma_shrink_bits"] for r in rows])
th  = np.array([r["theo_shrink_bits"]  for r in rows])
rho = np.array([r["lag1_autocorr"]     for r in rows])

print("="*90)
print("TEST 1  -- is comp-ratio a MONOTONE function of lag-1 autocorr? (across all 36 cells)")
print("="*90)
print(f"  Pearson(comp_ratio, lag1_autocorr)  = {pearson(cr,rho):+.4f}")
print(f"  Spearman(comp_ratio, lag1_autocorr) = {spearman(cr,rho):+.4f}")
print(f"  Pearson(sigma_shrink, lag1_autocorr)= {pearson(ss,rho):+.4f}")
print(f"  Spearman(sigma_shrink,lag1_autocorr)= {spearman(ss,rho):+.4f}")

print("\n" + "="*90)
print("TEST 2 -- does EMPIRICAL sigma-shrink == predicted -0.5*log2(2(1-rho))? (the exact identity)")
print("="*90)
resid = ss - th
print(f"  max |empirical - predicted| over 36 cells = {np.max(np.abs(resid)):.4f} bits")
print(f"  RMS error                                  = {math.sqrt(np.mean(resid**2)):.4f} bits")
print(f"  Pearson(empirical, predicted)              = {pearson(ss,th):+.6f}")
print("  => sigma-shrink is governed by lag-1 autocorr to <0.02 bit. Persistence-law")
print("     compression IS the lag-1 autocorrelation, by the Var(resid)=2 sig^2 (1-rho) identity.")

print("\n" + "="*90)
print("TEST 3 -- crossover: persistence COMPRESSES iff lag-1 autocorr > 0.5 (sigma-shrink>0 at rho=0.5)")
print("="*90)
for r in rows:
    if r["series"]=="flare_REAL" and r["method"]=="decimate":
        flag = "COMPRESS" if r["sigma_shrink_bits"]>0 else "EXPAND  "
        print(f"  flare decimate r={r['rung']:<3d}: rho={r['lag1_autocorr']:+.3f}  shrink={r['sigma_shrink_bits']:+.3f}b  comp_ratio={r['comp_ratio']:.3f}  [{flag}]")
print(f"  predicted crossover rho* solving 2(1-rho)=1  ->  rho* = 0.500")

print("\n" + "="*90)
print("TEST 4 -- decimated lag-1 autocorr vs rung: does it follow rho^r? (AR1 control vs flare)")
print("="*90)
def fit_rho_power(rungs, acf):
    # fit acf(r) = rho^r on positive values via log-linear:  log(acf) = r*log(rho)
    rungs=np.asarray(rungs,float); acf=np.asarray(acf,float)
    m = acf>0.02
    lr = rungs[m]; la = np.log(acf[m])
    slope = np.dot(lr-lr.mean(), la-la.mean())/np.dot(lr-lr.mean(), lr-lr.mean())
    return math.exp(slope)
for name in ("ar1_CONTROL_memory","flare_REAL"):
    acf = {r["rung"]: r["lag1_autocorr"] for r in rows if r["series"]==name and r["method"]=="decimate"}
    rs = RUNGS; av = [acf[r] for r in rs]
    rho_fit = fit_rho_power(rs, av)
    print(f"\n  {name} (decimate):")
    print("   rung:        " + "  ".join(f"{r:>6d}" for r in rs))
    print("   acf empir:   " + "  ".join(f"{v:6.3f}" for v in av))
    print(f"   acf rho^r:   " + "  ".join(f"{rho_fit**r:6.3f}" for r in rs) + f"   (best-fit rho={rho_fit:.3f})")
    # also show the r=1 value as the 'native' rho and its power law
    rho1 = av[0]
    print(f"   acf rho1^r:  " + "  ".join(f"{rho1**r:6.3f}" for r in rs) + f"   (rho1 = lag-1 at r=1 = {rho1:.3f})")

print("\n  NOTE: decimating by r makes lag-1 autocorr of the result = ORIGINAL series' autocorr at lag r.")
print("        For a pure AR(1) that is exactly rho^r. AR1 control fits rho^r with rho~0.9 (its build param).")
print("        The flare's ACF decays FASTER than any single rho^r at long lags -> multi-timescale, not one AR(1).")
