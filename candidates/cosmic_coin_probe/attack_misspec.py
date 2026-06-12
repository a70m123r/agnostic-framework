# Attack 2: MISSPECIFICATION. Fit fairer flare models (AR(1), moving-average) and
# recompute compression ratio + bits-saved fraction. Does a better model close the
# gap to orbit? Keep the SAME instrument (lzma-9 + same quantization 1e-3 dex).
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path('.').resolve()
DATA = HERE / 'probe_data'
Q_LOGFLUX = 1e-3
LOG2E = 1.0/math.log(2.0)

def clen_bits(int_array, coder="lzma"):
    b = np.ascontiguousarray(int_array.astype(np.int64)).tobytes()
    if coder=="lzma": c=lzma.compress(b,preset=9)
    elif coder=="zlib": c=zlib.compress(b,9)
    elif coder=="bz2": c=bz2.compress(b,9)
    return len(c)*8

# --- load flare log-flux exactly as harness does ---
rows = json.loads((DATA/"goes_xray_7day.json").read_text(encoding="utf-8"))
long = [r for r in rows if r.get("energy")=="0.1-0.8nm" and r.get("flux") is not None]
long.sort(key=lambda r: r["time_tag"])
flux = np.array([r["flux"] for r in long], dtype=float)
flux = np.clip(flux,1e-9,None); flux = flux[np.isfinite(flux)]
lf = np.log10(flux)
n = len(lf)

raw_i = np.round(lf/Q_LOGFLUX).astype(np.int64)
raw_bits = {c: clen_bits(raw_i,c) for c in ("lzma","zlib","bz2")}

def report_model(name, pred, model_bits):
    resid = lf - pred
    res_i = np.round(resid/Q_LOGFLUX).astype(np.int64)
    out = {}
    for c in ("lzma","zlib","bz2"):
        rb = clen_bits(res_i,c)
        out[c] = dict(resid_bits=rb,
                      comp_ratio=raw_bits[c]/(rb+model_bits),
                      comp_ratio_nomodel=raw_bits[c]/rb,
                      saved_frac=(raw_bits[c]-rb)/raw_bits[c])
    sig = float(np.std(resid))
    # gaussian appearance entropy bits/step
    H = 0.5*math.log2(2*math.pi*math.e*sig*sig)-math.log2(Q_LOGFLUX)
    return dict(model=name, sigma=sig, H_app_bits=H, model_bits=model_bits, coders=out,
                resid_std=sig)

results = {}
# Model 0: persistence (baseline, harness)
pred_pers = np.empty_like(lf); pred_pers[0]=lf[0]; pred_pers[1:]=lf[:-1]
results['persistence'] = report_model('persistence', pred_pers, 64)

# Model 1: AR(1) on log-flux  lf[t] = c + phi*lf[t-1] + eps  (fit OLS on whole series)
x = lf[:-1]; y = lf[1:]
phi = np.cov(x,y,bias=True)[0,1]/np.var(x)
c = y.mean() - phi*x.mean()
pred_ar1 = np.empty_like(lf); pred_ar1[0]=lf[0]; pred_ar1[1:] = c + phi*lf[:-1]
results['ar1'] = report_model(f'ar1(phi={phi:.5f},c={c:.4f})', pred_ar1, 3*64)
results['ar1']['phi']=float(phi); results['ar1']['c']=float(c)

# Model 1b: AR(1) on INCREMENTS (mean-revert increments) -- alt fair model
# predict next increment from prev increment
d = np.diff(lf)  # increments, len n-1
xd = d[:-1]; yd = d[1:]
phid = np.cov(xd,yd,bias=True)[0,1]/np.var(xd)
cd = yd.mean()-phid*xd.mean()
pred_incr = np.empty_like(lf); pred_incr[0]=lf[0]; pred_incr[1]=lf[0]
# pred lf[t] = lf[t-1] + (cd+phid*increment[t-1])
for t in range(2,n):
    pred_incr[t] = lf[t-1] + cd + phid*(lf[t-1]-lf[t-2])
results['ar1_on_increments'] = report_model(f'ar1_incr(phi={phid:.4f})', pred_incr, 3*64)

# Model 2: moving-average baselines f_hat(t)=mean(lf[t-k..t-1])
for k in (3,5,10,30):
    pred_ma = np.empty_like(lf)
    for t in range(n):
        lo = max(0,t-k)
        pred_ma[t] = lf[lo:t].mean() if t>0 else lf[0]
    results[f'ma{k}'] = report_model(f'ma{k}', pred_ma, 64)

# Model 3: EWMA (exponential), pick alpha by grid to minimize resid var
best=None
for alpha in np.linspace(0.05,0.95,19):
    pe = np.empty_like(lf); pe[0]=lf[0]
    s = lf[0]
    for t in range(1,n):
        pe[t]=s
        s = alpha*lf[t]+(1-alpha)*s
    v = np.var(lf-pe)
    if best is None or v<best[0]: best=(v,alpha,pe.copy())
results[f'ewma(alpha={best[1]:.2f})'] = report_model(f'ewma_a{best[1]:.2f}', best[2], 2*64)

# --- ORBIT reference (from harness results.json) for gap comparison ---
orbit = json.loads((HERE/'results.json').read_text())['orbit']
orbit_ratio_lzma = orbit['mdl']['lzma']['comp_ratio']  # with model bits
orbit_saved_lzma = (orbit['mdl']['lzma']['raw_bits']-orbit['mdl']['lzma']['resid_bits'])/orbit['mdl']['lzma']['raw_bits']

print("="*70)
print("FLARE MISSPECIFICATION ATTACK -- fairer models, same lzma-9 instrument")
print("="*70)
print(f"flare raw bits (lzma/zlib/bz2): {raw_bits}")
print(f"ORBIT ref: lzma comp_ratio={orbit_ratio_lzma:.3f}, saved_frac={orbit_saved_lzma:.3f}")
print("-"*70)
hdr = f"{'model':28s} {'sigma':>8s} {'lzmaCR':>7s} {'lzmaCRnm':>9s} {'savedfr':>8s} {'Happ':>7s}"
print(hdr)
for name,r in results.items():
    cz = r['coders']['lzma']
    print(f"{name:28s} {r['sigma']:8.5f} {cz['comp_ratio']:7.3f} {cz['comp_ratio_nomodel']:9.3f} {cz['saved_frac']:8.4f} {r['H_app_bits']:7.3f}")
print("-"*70)
# best flare model by lzma no-model comp ratio
bestmodel = max(results.items(), key=lambda kv: kv[1]['coders']['lzma']['comp_ratio_nomodel'])
print(f"BEST flare model (lzma no-model CR): {bestmodel[0]} = {bestmodel[1]['coders']['lzma']['comp_ratio_nomodel']:.3f}")
print(f"  vs ORBIT lzma no-model CR = {orbit['mdl']['lzma']['raw_bits']/orbit['mdl']['lzma']['resid_bits']:.3f}")
orbit_cr_nm = orbit['mdl']['lzma']['raw_bits']/orbit['mdl']['lzma']['resid_bits']
print(f"  ratio-of-ratios orbit/best-flare = {orbit_cr_nm/bestmodel[1]['coders']['lzma']['comp_ratio_nomodel']:.3f}")
print(f"  saved-frac gap orbit-bestflare = {orbit_saved_lzma - bestmodel[1]['coders']['lzma']['saved_frac']:.3f}")
print()
# Does ANY flare model reverse (flare CR > orbit CR)?
reversed_any = any(r['coders']['lzma']['comp_ratio_nomodel'] > orbit_cr_nm for r in results.values())
print(f"ANY flare model reverses (flare lzma-CR > orbit {orbit_cr_nm:.2f})? {reversed_any}")

import json as J
print("\nJSON_DUMP_START")
dump = {name: {'sigma':r['sigma'],'H_app':r['H_app_bits'],
               'lzma_CR_nomodel':r['coders']['lzma']['comp_ratio_nomodel'],
               'lzma_CR':r['coders']['lzma']['comp_ratio'],
               'lzma_saved_frac':r['coders']['lzma']['saved_frac'],
               'zlib_CR_nomodel':r['coders']['zlib']['comp_ratio_nomodel'],
               'bz2_CR_nomodel':r['coders']['bz2']['comp_ratio_nomodel']}
        for name,r in results.items()}
dump['_orbit_ref']={'lzma_CR_nomodel':orbit_cr_nm,'lzma_CR':orbit_ratio_lzma,'lzma_saved_frac':orbit_saved_lzma}
dump['_reversed_any']=reversed_any
print(J.dumps(dump,indent=1))
print("JSON_DUMP_END")
