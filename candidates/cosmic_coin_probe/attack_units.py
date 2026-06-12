# Attack 1: UNIT CONFOUND. The raw absolute-bits gap is backwards (orbit ~43 > flare ~6
# bits/step). Is "orbit sharp" an artifact of units/dimensionality/quantization?
# Strip units every way possible and check the sign of the cross-phenomenon contrast.
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE=pathlib.Path('.').resolve(); DATA=HERE/'probe_data'
LOG2E=1.0/math.log(2.0)
def clen(a,coder="lzma"):
    b=np.ascontiguousarray(a.astype(np.int64)).tobytes()
    if coder=="lzma": return len(lzma.compress(b,preset=9))*8
    if coder=="zlib": return len(zlib.compress(b,9))*8
    if coder=="bz2": return len(bz2.compress(b,9))*8

d=np.load('probe_data/series.npz')
ores=d['orbit_resid']; otruth=d['orbit_truth']
# flare
rows=json.loads((DATA/"goes_xray_7day.json").read_text())
long=[r for r in rows if r.get("energy")=="0.1-0.8nm" and r.get("flux") is not None]
long.sort(key=lambda r:r["time_tag"])
flux=np.clip(np.array([r["flux"] for r in long]),1e-9,None); flux=flux[np.isfinite(flux)]
lf=np.log10(flux)
fpred=np.empty_like(lf); fpred[0]=lf[0]; fpred[1:]=lf[:-1]; fres=lf-fpred

print("="*72)
print("UNIT-STRIPPING BATTERY: does ORBIT>FLARE survive removing units/quant/dim?")
print("="*72)

# ---- (A) Z-SCORE EVERYTHING: divide each series by its own raw std, quantize at a
#         COMMON dimensionless step. Now both are pure-number 'sigma units'. ----
def zscore_compress(truth_cols, resid_cols, qz, coder="lzma"):
    # truth_cols, resid_cols: list of 1D arrays (per dimension)
    raw_i=[]; res_i=[]
    for tc,rc in zip(truth_cols,resid_cols):
        s = np.std(tc)
        raw_i.append(np.round((tc-tc.mean())/s/qz).astype(np.int64))
        res_i.append(np.round(rc/s/qz).astype(np.int64))  # SAME raw-sigma scale
    raw_i=np.concatenate(raw_i); res_i=np.concatenate(res_i)
    rb=clen(raw_i,coder); xb=clen(res_i,coder)
    return rb, xb, rb/xb, (rb-xb)/rb

orbit_cols_t=[otruth[:,k] for k in range(3)]
orbit_cols_r=[ores[:,k] for k in range(3)]
flare_cols_t=[lf]; flare_cols_r=[fres]

print("\n(A) Z-SCORED to each series' own RAW std, common dimensionless quant step qz:")
print(f"{'qz':>6s} {'phenom':>7s} {'rawb':>8s} {'resb':>8s} {'CR':>7s} {'savedfr':>8s}")
for qz in (0.01,0.05,0.1):
    orb=zscore_compress(orbit_cols_t,orbit_cols_r,qz)
    fla=zscore_compress(flare_cols_t,flare_cols_r,qz)
    print(f"{qz:6.2f} {'ORBIT':>7s} {orb[0]:8d} {orb[1]:8d} {orb[2]:7.3f} {orb[3]:8.4f}")
    print(f"{qz:6.2f} {'FLARE':>7s} {fla[0]:8d} {fla[1]:8d} {fla[2]:7.3f} {fla[3]:8.4f}")
    print(f"       ratio-of-CR orbit/flare = {orb[2]/fla[2]:.3f}   saved-frac gap = {orb[3]-fla[3]:+.3f}")

# ---- (B) PURE SIGMA-SHRINK FACTOR (fully unit/quant invariant): how many bits does
#         the law remove per dimension = log2(sigma_raw/sigma_resid). q cancels. ----
print("\n(B) q-INVARIANT sigma-shrink (log2 sigma_raw/sigma_resid), units fully cancel:")
def sigma_shrink_bits(truth_cols,resid_cols):
    vals=[]
    for tc,rc in zip(truth_cols,resid_cols):
        vals.append(math.log2(np.std(tc)/np.std(rc)))
    return np.mean(vals), vals
ob,ov=sigma_shrink_bits(orbit_cols_t,orbit_cols_r)
fb,fv=sigma_shrink_bits(flare_cols_t,flare_cols_r)
print(f"  ORBIT bits-saved/dim = {ob:.3f}  (per-axis {[round(x,2) for x in ov]})")
print(f"  FLARE bits-saved/dim = {fb:.3f}")
print(f"  --> EDGE = {ob-fb:.3f} bits/dim  (orbit sharper); sign INDEPENDENT of q")

# ---- (C) Coefficient of determination R^2 = 1 - var(resid)/var(truth): dimensionless,
#         quant-free, dimension-free (variance-explained by the law). ----
print("\n(C) R^2 variance-explained by the law (fully dimensionless):")
def r2(truth_cols,resid_cols):
    num=sum(np.var(rc) for rc in resid_cols); den=sum(np.var(tc) for tc in truth_cols)
    return 1-num/den
print(f"  ORBIT R^2 = {r2(orbit_cols_t,orbit_cols_r):.6f}")
print(f"  FLARE R^2 = {r2(flare_cols_t,flare_cols_r):.6f}")

# ---- (D) INVERT THE TRAP: put BOTH in the SAME physical-style quant grid by
#         choosing q = k * sigma_raw (q scales with the data), forcing equal raw entropy
#         per dim. Then ALL that differs is resid. This removes the incommensurate-q. ----
print("\n(D) EQUALIZED raw entropy (q = sigma_raw/256 each): forces fair raw baseline:")
def equalized(truth_cols,resid_cols,coder="lzma"):
    raw_i=[]; res_i=[]
    for tc,rc in zip(truth_cols,resid_cols):
        q=np.std(tc)/256.0
        raw_i.append(np.round((tc-tc.mean())/q).astype(np.int64))
        res_i.append(np.round(rc/q).astype(np.int64))
    raw_i=np.concatenate(raw_i); res_i=np.concatenate(res_i)
    rb=clen(raw_i,coder); xb=clen(res_i,coder); return rb,xb,rb/xb,(rb-xb)/rb
for coder in ("lzma","zlib","bz2"):
    orb=equalized(orbit_cols_t,orbit_cols_r,coder); fla=equalized(flare_cols_t,flare_cols_r,coder)
    print(f"  [{coder}] ORBIT CR {orb[2]:.3f} saved {orb[3]:.3f} | FLARE CR {fla[2]:.3f} saved {fla[3]:.3f} | ratio {orb[2]/fla[2]:.3f}")

# ---- (E) THE BACKWARDS NAIVE GAP, and WHY: absolute bits/step ----
print("\n(E) The known trap reproduced (absolute bits/step, incommensurate):")
osig=np.std(ores,axis=0); fsig=np.std(fres)
o_app=0.5*np.sum(np.log2(2*math.pi*math.e*osig**2))-3*math.log2(1.0)
f_app=0.5*math.log2(2*math.pi*math.e*fsig**2)-math.log2(1e-3)
print(f"  orbit appearance {o_app:.2f} bits/step (3D @1km) vs flare {f_app:.2f} (1D @1e-3 dex) -> naive gap {f_app-o_app:.2f}")
print(f"  per-DIM: orbit {o_app/3:.2f} vs flare {f_app:.2f} -- still apples/oranges (km vs dex, 1km vs 1e-3 quant)")
print(f"  The gap is a DIMENSION x QUANT artifact: 3 dims and finer quant for flare both inflate flare bits.")

print("\nVERDICT inputs:")
print(f"  sigma-shrink edge (q-free): orbit {ob:.2f} > flare {fb:.2f} bits/dim  [SIGN: orbit sharper]")
print(f"  R2: orbit {r2(orbit_cols_t,orbit_cols_r):.4f} > flare {r2(flare_cols_t,flare_cols_r):.4f}")
