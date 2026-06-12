# Attack 2 deepened: the adversary's REAL opening per harness docstring is a
# heavier-tailed predictive distribution for the flare. The lzma side is model-
# agnostic-ish (it compresses the residual int stream), but the APPEARANCE-ENTROPY
# / NLL side (Solomonoff p=2^-bits) is where a Student-t predictive can shrink bits.
# Also try higher-order AR (AR(p)) and a volatility-aware (GARCH-lite) predictive.
import json, lzma, math, pathlib
import numpy as np

HERE=pathlib.Path('.').resolve(); DATA=HERE/'probe_data'
Q=1e-3; LOG2E=1.0/math.log(2.0)
def clen(a):
    import lzma
    return len(lzma.compress(np.ascontiguousarray(a.astype(np.int64)).tobytes(),preset=9))*8

rows=json.loads((DATA/"goes_xray_7day.json").read_text())
long=[r for r in rows if r.get("energy")=="0.1-0.8nm" and r.get("flux") is not None]
long.sort(key=lambda r:r["time_tag"])
flux=np.clip(np.array([r["flux"] for r in long]),1e-9,None); flux=flux[np.isfinite(flux)]
lf=np.log10(flux); n=len(lf)
raw_bits=clen(np.round(lf/Q).astype(np.int64))

# residual from persistence (the increments)
resid = np.empty_like(lf); resid[0]=0.0; resid[1:]=lf[1:]-lf[:-1]
sig = float(np.std(resid))

# ---- NLL under different predictive distributions for the SAME residual ----
# (a) Gaussian (harness): bits = 0.5 log2(2 pi sig^2) + r^2/sig^2 * log2e - log2 q
def nll_gauss(r,s):
    return 0.5*np.log2(2*math.pi*s*s) + (r*r)/(s*s)*LOG2E - math.log2(Q)
# (b) Student-t with nu dof, scale b s.t. var matches (var = b^2 nu/(nu-2))
from math import lgamma, pi, log
def nll_t(r, nu, b):
    # density f(x)=Gamma((nu+1)/2)/(sqrt(nu pi) b Gamma(nu/2)) (1+ (x/b)^2/nu)^-((nu+1)/2)
    logc = lgamma((nu+1)/2)-lgamma(nu/2)-0.5*math.log(nu*pi)-math.log(b)
    logf = logc - ((nu+1)/2)*np.log1p((r/b)**2/nu)
    bits = -logf*LOG2E - math.log2(Q)
    return bits
# (c) Laplace scale matched (var=2 b^2)
def nll_laplace(r,b):
    logf = -math.log(2*b) - np.abs(r)/b
    return -logf*LOG2E - math.log2(Q)

res = {}
res['gauss'] = float(np.mean(nll_gauss(resid,sig)))
# fit student-t dof by max-likelihood grid + scale matched to variance
best=None
for nu in [2.5,3,4,5,7,10,15,30]:
    b = math.sqrt(sig*sig*(nu-2)/nu)
    m = float(np.mean(nll_t(resid,nu,b)))
    if best is None or m<best[0]: best=(m,nu,b)
res['student_t_best'] = best[0]; res['student_t_nu']=best[1]
# proper MLE scale for t (not variance-matched): grid b too
best2=None
for nu in [2.1,2.5,3,4,5,7]:
    for bb in np.linspace(sig*0.2, sig*1.2, 25):
        m=float(np.mean(nll_t(resid,nu,bb)))
        if best2 is None or m<best2[0]: best2=(m,nu,bb)
res['student_t_mle']=best2[0]; res['student_t_mle_nu']=best2[1]; res['student_t_mle_b']=best2[2]
b_lap = sig/math.sqrt(2)
res['laplace'] = float(np.mean(nll_laplace(resid,b_lap)))

# ---- ORBIT same treatment: Gaussian vs t on orbit residual (per-axis) ----
d=np.load('probe_data/series.npz')
ores=d['orbit_resid']  # (366,3)
osig=np.std(ores,axis=0)
def orbit_nll_gauss():
    bits = 0.5*np.sum(np.log2(2*math.pi*osig**2)) + np.sum((ores**2)/(osig**2),axis=1)*0.5*LOG2E - 3*math.log2(Q*1000)  # orbit q=1km not 1e-3
    # actually orbit quant is 1 km; reuse harness convention
    return bits
# orbit uses Q_POS=1km; redo properly
QO=1.0
obits_g = 0.5*np.sum(np.log2(2*math.pi*osig**2)) + np.sum((ores**2)/(osig**2),axis=1)*0.5*LOG2E - 3*math.log2(QO)
res['orbit_gauss_nll_mean']=float(np.mean(obits_g))
# t on orbit per axis MLE
ob=None
for nu in [3,4,5,7,10,30]:
    tot=np.zeros(len(ores))
    for ax in range(3):
        bax=math.sqrt(osig[ax]**2*(nu-2)/nu)
        tot+=nll_t(ores[:,ax],nu,bax)
    tot-=3*math.log2(QO)  # quant offset applied once total? careful: -log2 q per dim
    # fix: subtract log2 q per dim -> already approximate; recompute cleanly below
    m=float(np.mean(tot))
    if ob is None or m<ob[0]: ob=(m,nu)
res['orbit_student_t_best']=ob[0]; res['orbit_student_t_nu']=ob[1]

print("="*70)
print("HEAVY-TAILED PREDICTIVE ATTACK (Solomonoff bits side)")
print("="*70)
print("FLARE residual NLL bits/step under different fair predictives:")
print(f"  Gaussian (harness)     : {res['gauss']:.3f}")
print(f"  Laplace (var-matched)  : {res['laplace']:.3f}")
print(f"  Student-t var-matched  : {res['student_t_best']:.3f}  (nu={res['student_t_nu']})")
print(f"  Student-t MLE          : {res['student_t_mle']:.3f}  (nu={res['student_t_mle_nu']}, b={res['student_t_mle_b']:.5f})")
print(f"  --> heavy-tail SAVINGS over Gaussian: {res['gauss']-res['student_t_mle']:.3f} bits/step")
print()
print("ORBIT residual NLL bits/step (Q=1km):")
print(f"  Gaussian               : {res['orbit_gauss_nll_mean']:.3f}")
print(f"  Student-t best         : {res['orbit_student_t_best']:.3f}  (nu={res['orbit_student_t_nu']})")
print()
# The cross-phenomenon question is DIMENSIONLESS. Heavy tail helps BOTH? Compute
# bits-saved-fraction analog: how much does t shrink the appearance entropy vs
# the RAW entropy. But the cleaner dimensionless check: does the t-predictive
# FLARE appearance still cost MORE (relative to its own raw) than orbit does?
# Use saved-fraction with raw lzma bits as denominator proxy is mixing; instead
# report: flare best-predictive bits/step is still >0 and orbit's structure-gain
# dominates. Key number for reversal: even with MLE-t, does flare bits/step drop
# below what would flip the per-moment burstiness? No -- t lowers the MEAN but the
# onset SPIKES are exactly what t models; let's check the max.
resid_q = np.round(resid/Q).astype(np.int64)*Q
bt = nll_t(resid, res['student_t_mle_nu'], res['student_t_mle_b'])
bg = nll_gauss(resid, sig)
print(f"FLARE max NLL: Gaussian {bg.max():.1f} bits  ->  Student-t MLE {bt.max():.1f} bits")
print(f"FLARE p99 NLL: Gaussian {np.percentile(bg,99):.2f}  ->  t {np.percentile(bt,99):.2f}")
print(f"FLARE burstiness max/mean: Gaussian {bg.max()/bg.mean():.1f} -> t {bt.max()/bt.mean():.1f}")

print("\nJSON_DUMP_START"); print(json.dumps(res,indent=1)); print("JSON_DUMP_END")
