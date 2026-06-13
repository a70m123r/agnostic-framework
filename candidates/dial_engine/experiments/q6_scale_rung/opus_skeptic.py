# -*- coding: utf-8 -*-
"""
OPUS SKEPTIC stress-test of the Q6 scale-rung refutation.
Attack 1: NOISE-FLOOR WANDER  -- is flare decay distinguishable from floor noise?
Attack 2: FINE-LAW-BY-CONSTRUCTION -- build a COARSE-SCALE law and re-run.
Attack 3: WINDOW TOO SHORT -- is the coarse end structurally empty?
Attack 4: MEAN-vs-DECIMATE -- does agreement rule out variance-reduction artifact?
All real computation; flare is the committed GOES week; noise/ar1 are seeded synthetic controls.
"""
import json, lzma, zlib, bz2, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
GOES = HERE / "../../../cosmic_coin_probe/probe_data/goes_xray_7day.json"
Q = 1e-3
RUNGS = [1, 2, 5, 10, 30, 60]

def clen_bits(x, coder="lzma"):
    b = np.ascontiguousarray(np.round(x / Q).astype(np.int64)).tobytes()
    c = {"lzma": lambda: lzma.compress(b, preset=9),
         "zlib": lambda: zlib.compress(b, 9),
         "bz2":  lambda: bz2.compress(b, 9)}[coder]()
    return len(c) * 8

def coarsen(x, r, method):
    if r == 1:
        return x.copy()
    n = (len(x) // r) * r
    xx = x[:n]
    if method == "mean":
        return xx.reshape(-1, r).mean(axis=1)
    elif method == "decimate":
        return xx[::r]
    raise ValueError(method)

def load_flare():
    rows = json.loads(pathlib.Path(GOES).read_text(encoding="utf-8"))
    longb = [r for r in rows if r.get("energy") == "0.1-0.8nm" and r.get("flux") is not None]
    longb.sort(key=lambda r: r["time_tag"])
    flux = np.clip(np.array([r["flux"] for r in longb], float), 1e-9, None)
    return np.log10(flux[np.isfinite(flux)])

def persistence_comp(x, coder="lzma"):
    pred = np.empty_like(x); pred[0] = x[0]; pred[1:] = x[:-1]
    resid = x - pred
    rb = clen_bits(x, coder); sb = clen_bits(resid, coder)
    return rb / (sb + 64)

flare = load_flare()
n = len(flare)
print(f"flare loaded: n={n}, std={flare.std():.4f}, span_min={n} (=={n/60/24:.2f} days)")

# ======================================================================
# ATTACK 1: NOISE-FLOOR WANDER
# Build a LARGE ensemble of iid-noise controls (many seeds) and measure the
# full distribution of the persistence comp-ratio at EACH rung under decimate.
# Then ask: at each rung, is the flare's comp-ratio inside or outside that
# null band? In particular at coarse rungs is the flare distinguishable from
# the structureless floor, or has everything collapsed into the noise cloud?
# ======================================================================
print("\n" + "="*70)
print("ATTACK 1: NOISE-FLOOR WANDER (null ensemble, 200 seeds)")
print("="*70)
NSEED = 200
floor = {r: [] for r in RUNGS}
for s in range(NSEED):
    rng = np.random.default_rng(1000 + s)
    z = rng.normal(0, flare.std(), size=n)
    for r in RUNGS:
        xr = coarsen(z, r, "decimate")
        floor[r].append(persistence_comp(xr))
flare_dec = {r: persistence_comp(coarsen(flare, r, "decimate")) for r in RUNGS}
print(f"{'rung':>5} {'flare':>7} {'null_mean':>9} {'null_sd':>7} {'null_p2.5':>9} {'null_p97.5':>10} {'flare_z':>8} {'flare>p97.5':>11}")
attack1_rows = {}
for r in RUNGS:
    arr = np.array(floor[r])
    mu, sd = arr.mean(), arr.std()
    lo, hi = np.percentile(arr, 2.5), np.percentile(arr, 97.5)
    z = (flare_dec[r] - mu) / sd
    above = flare_dec[r] > hi
    attack1_rows[r] = dict(flare=flare_dec[r], null_mean=mu, null_sd=sd, lo=lo, hi=hi, z=z, above=bool(above))
    print(f"{r:>5} {flare_dec[r]:>7.3f} {mu:>9.3f} {sd:>7.3f} {lo:>9.3f} {hi:>10.3f} {z:>8.2f} {str(bool(above)):>11}")

# Also: is the DECAY itself (rung1 - rungK) distinguishable from the spread of
# decay you'd get inside the null ensemble? i.e. take each null realization,
# compute its own rung1-rungK, and see if flare's decay exceeds the null decay spread.
print("\n  Within-null DECAY spread vs flare decay (rung1 - rungK):")
for r in [10, 30, 60]:
    null_decay = np.array(floor[1]) - np.array(floor[r])
    flare_decay = flare_dec[1] - flare_dec[r]
    print(f"   rung1-rung{r:<2}: flare={flare_decay:+.3f}  null_decay_mean={null_decay.mean():+.3f} sd={null_decay.std():.3f}  p97.5={np.percentile(null_decay,97.5):+.3f}  flare_exceeds_null_p97.5={flare_decay>np.percentile(null_decay,97.5)}")

# KEY skeptic question: how many rungs is the flare ABOVE the null floor?
n_above = sum(attack1_rows[r]['above'] for r in RUNGS)
print(f"\n  => flare above null-p97.5 at {n_above}/{len(RUNGS)} rungs. Rungs where flare is INSIDE the noise cloud (indistinguishable from floor):", [r for r in RUNGS if not attack1_rows[r]['above']])

# ======================================================================
# ATTACK 2: FINE-LAW-BY-CONSTRUCTION  -- build COARSE-SCALE laws.
# Persistence f(t)=f(t-1) is a 1-step law; its edge is fine-scale by definition.
# Fair test of "coarse=more-lawful": use a law that can ONLY see coarse structure.
#   (a) LAG-r persistence: predict f(t) from f(t-r) where r = the rung (scale-matched).
#   (b) WINDOW-MEAN law: predict f(t) by the local mean over the last W coarse steps
#       (a slow trend law). Residual = deviation from slow trend.
#   (c) DETREND-then-compress: does a coarse polynomial/rolling trend carry bits?
# For each, compute comp-ratio vs rung and ask: does ANY coarse law make the
# flare MORE compressible as you coarsen (restoring coarse=more-lawful)?
# ======================================================================
print("\n" + "="*70)
print("ATTACK 2: FINE-LAW-BY-CONSTRUCTION (build coarse-scale laws)")
print("="*70)

def lagr_comp(x, lag, coder="lzma"):
    if len(x) <= lag: return None
    pred = x.copy()
    pred[lag:] = x[:-lag]
    resid = x[lag:] - pred[lag:]
    rb = clen_bits(x[lag:], coder); sb = clen_bits(resid, coder)
    return rb / (sb + 64)

def winmean_comp(x, W, coder="lzma"):
    # predict x[t] by trailing mean of the W samples ending at t-1; residual = x - trend.
    if len(x) <= W: return None
    cs = np.concatenate([[0.0], np.cumsum(x)])           # cs[i] = sum(x[:i])
    # trailing mean over x[t-W : t] for t = W .. len(x)-1
    trend = (cs[W:len(x)] - cs[0:len(x)-W]) / W           # length len(x)-W, aligned to t = W..len(x)-1
    target = x[W:len(x)]                                  # same length
    resid = target - trend
    rb = clen_bits(target, coder); sb = clen_bits(resid, coder)
    return rb / (sb + 64)

# (a) scale-matched lag-r persistence on the ORIGINAL 1-min series (no coarsening):
# this asks "is there lawful structure at scale r minutes" directly, the honest
# coarse-scale analogue. Compare to lag-1.
print("\n (a) LAG-r persistence on the raw 1-min flare (predict f(t) from f(t-lag)):")
print(f"     lag(min): " + "  ".join(f"{r:>6}" for r in [1,2,5,10,30,60,120,240,720,1440]))
line_f = [];
for lag in [1,2,5,10,30,60,120,240,720,1440]:
    line_f.append(lagr_comp(flare, lag))
print("     flare   : " + "  ".join(f"{v:6.3f}" if v else "   nan" for v in line_f))
# null comparison
rngn = np.random.default_rng(7)
z = rngn.normal(0, flare.std(), size=n)
line_n = [lagr_comp(z, lag) for lag in [1,2,5,10,30,60,120,240,720,1440]]
print("     noise   : " + "  ".join(f"{v:6.3f}" if v else "   nan" for v in line_n))

# (b) WINDOW-MEAN (slow-trend) law on raw 1-min flare with growing window:
print("\n (b) WINDOW-MEAN slow-trend law on raw 1-min flare (residual = x - trailing W-mean):")
print(f"     W(min) : " + "  ".join(f"{w:>6}" for w in [5,10,30,60,120,240,720]))
line_fb = [winmean_comp(flare, w) for w in [5,10,30,60,120,240,720]]
print("     flare  : " + "  ".join(f"{v:6.3f}" if v else "   nan" for v in line_fb))
line_nb = [winmean_comp(z, w) for w in [5,10,30,60,120,240,720]]
print("     noise  : " + "  ".join(f"{v:6.3f}" if v else "   nan" for v in line_nb))

# (c) Does a coarse trend itself carry compressible bits? Compare raw_bits of the
# coarsened series (the "coarse view") to its persistence-resid AND to an iid
# surrogate with the SAME marginal (phase-randomized). If the coarse view is more
# compressible than a same-marginal iid surrogate, there's residual coarse structure.
print("\n (c) Coarse-view structure: is the decimated flare more compressible than a")
print("     same-marginal SHUFFLE (destroys all time structure, keeps histogram)?")
print(f"     {'rung':>5} {'raw_bits/n':>11} {'shuffled_bits/n':>15} {'ratio_shuf/raw':>15}")
attack2c = {}
for r in RUNGS:
    xr = coarsen(flare, r, "decimate")
    raw = clen_bits(xr)
    sh_ratios = []
    for sd in range(30):
        rr = np.random.default_rng(500+sd)
        xs = xr.copy(); rr.shuffle(xs)
        sh_ratios.append(clen_bits(xs))
    shuf = np.mean(sh_ratios)
    attack2c[r] = shuf/raw
    print(f"     {r:>5} {raw/len(xr):>11.3f} {shuf/len(xr):>15.3f} {shuf/raw:>15.3f}")
print("     (ratio>1 => time-ordered coarse view compresses better than its own shuffle => coarse structure present)")

# ======================================================================
# ATTACK 3: WINDOW TOO SHORT  -- is the coarse end structurally empty by sampling?
# At rung 60 (hourly) n=167 ~ 7 days. There is <1 cycle of the 27-day rotation.
# Test: (i) how many independent coarse samples remain? (ii) construct a TOY series
# that HAS strong coarse-scale structure (a slow sinusoid at multi-hour period +
# fine noise) and run the SAME instrument: does the persistence law detect the
# coarse structure, or is it invisible to this law+window even when present?
# If a KNOWN coarse signal is also invisible, the refutation is uninformative about
# coarse-scale laws (window/law-blind), strengthening the "circular" critique.
# ======================================================================
print("\n" + "="*70)
print("ATTACK 3: WINDOW TOO SHORT (can persistence-law even SEE coarse structure?)")
print("="*70)
t = np.arange(n)
# Toy A: slow sinusoid (period 2 days) + fine iid noise. Coarse-lawful, fine-fuzzy.
rngt = np.random.default_rng(11)
period_min = 2*24*60
slow = 1.5*flare.std()*np.sin(2*np.pi*t/period_min)
fine_noise = rngt.normal(0, flare.std(), size=n)
toyA = slow + fine_noise
# Toy B: slow sinusoid ONLY (pure coarse law, no fine noise)
toyB = slow + 0.01*flare.std()*rngt.normal(0,1,size=n)
print("\n  persistence-law comp-ratio (decimate) on toy coarse-structured series:")
print(f"  {'rung':>5} {'toyA(slow+noise)':>17} {'toyB(slow only)':>16} {'flare':>7} {'noise':>7}")
for r in RUNGS:
    a = persistence_comp(coarsen(toyA, r, "decimate"))
    b = persistence_comp(coarsen(toyB, r, "decimate"))
    fl = flare_dec[r]
    nz = attack1_rows[r]['null_mean']
    print(f"  {r:>5} {a:>17.3f} {b:>16.3f} {fl:>7.3f} {nz:>7.3f}")
print("  => If toyA (which HAS coarse structure) ALSO decays toward the noise floor like the")
print("     flare, then persistence+7day is BLIND to coarse laws -> refuting coarse-lawful with it is uninformative.")
print("     If toyB (pure slow) STAYS compressible at coarse rungs, the instrument CAN see coarse structure when present.")

# How many independent coarse samples & decorrelation time?
def acf_lag1(x):
    x = x - x.mean()
    return np.sum(x[1:]*x[:-1])/np.sum(x*x)
print(f"\n  flare decorrelation: lag1 acf at rung60 = {acf_lag1(coarsen(flare,60,'decimate')):.3f}; n_eff at rung60 ~= {167}")
# integrated autocorr time on raw series:
xf = flare - flare.mean()
ac = np.correlate(xf, xf, 'full')[n-1:]/np.sum(xf*xf)
tau = 1 + 2*np.sum(ac[1:np.argmax(ac<0.05) if np.any(ac<0.05) else 200])
print(f"  integrated autocorr time tau ~= {tau:.0f} min => independent samples in 7day ~= {n/max(tau,1):.0f}")

# ======================================================================
# ATTACK 4: MEAN-vs-DECIMATE  -- does agreement rule out variance-reduction?
# The variance-reduction confound: mean-aggregation lowers sigma_raw, which can
# only RAISE comp-ratio if anything. They claim decimate (no averaging) ALSO
# decays, so the decay is not a smoothing artifact. But the skeptic angle:
# could BOTH be confounded by something OTHER than averaging? Two real probes:
#  (4a) The variance-reduction artifact would INFLATE the coarse comp-ratio for
#       MEAN (spurious lawfulness). Check: is the noise floor itself higher under
#       mean than decimate at coarse rungs? If yes, mean is contaminated; only
#       decimate is clean -- does the decimate refutation stand alone?
#  (4b) DECIMATION confound of its own: decimating an autocorrelated series both
#       (i) reduces n and (ii) keeps marginal variance ~same but lowers lag-1 rho.
#       Is the decimate "decay" actually just the n-shrinkage shrinking the
#       compressible signal below the fixed 64-bit model floor + header overhead?
#       Control: re-run decimate but PAD each coarse series back to a fixed large n
#       by tiling, removing the n-shrinkage, and/or report comp-ratio WITHOUT the
#       +64 model term and WITHOUT lzma headers (use sigma-shrink, coder-free).
# ======================================================================
print("\n" + "="*70)
print("ATTACK 4: MEAN-vs-DECIMATE (does agreement clear the variance-reduction artifact?)")
print("="*70)

# 4a: noise floor under mean vs decimate (ensemble)
floor_mean = {r: [] for r in RUNGS}
for s in range(NSEED):
    rng = np.random.default_rng(1000 + s)
    z2 = rng.normal(0, flare.std(), size=n)
    for r in RUNGS:
        floor_mean[r].append(persistence_comp(coarsen(z2, r, "mean")))
print("\n (4a) iid-noise FLOOR: mean vs decimate (ensemble mean +/- sd):")
print(f"  {'rung':>5} {'floor_decimate':>15} {'floor_mean':>12}")
for r in RUNGS:
    md = np.mean(floor[r]); sdd = np.std(floor[r])
    mm = np.mean(floor_mean[r]); smm = np.std(floor_mean[r])
    print(f"  {r:>5} {md:>9.3f}+/-{sdd:<4.3f} {mm:>7.3f}+/-{smm:<4.3f}")
print("  => If floor_mean RISES with rung while floor_decimate stays flat, mean is contaminated by")
print("     variance-reduction; decimate is the clean channel and must carry the refutation alone.")

# 4b: n-shrinkage confound. Coder-free sigma-shrink (no headers, no model floor).
# Var(resid of persistence) = 2 sigma^2 (1-rho1). sigma-shrink = -0.5 log2(2(1-rho1)).
# This is n-INDEPENDENT in expectation. Recompute it for flare/noise at each rung.
def sigma_shrink(x):
    pred = np.empty_like(x); pred[0]=x[0]; pred[1:]=x[:-1]
    resid = x-pred
    sr, sd = x.std(), resid.std()
    return math.log2(sr/sd) if sd>0 else float('nan')
print("\n (4b) Coder-free sigma-shrink (NO lzma header, NO +64 model floor; n-independent in expectation):")
print(f"  {'rung':>5} {'flare_dec':>10} {'flare_mean':>11} {'noise_dec':>10} {'theory_iid':>11}")
for r in RUNGS:
    fd = sigma_shrink(coarsen(flare,r,"decimate"))
    fm = sigma_shrink(coarsen(flare,r,"mean"))
    nd = sigma_shrink(coarsen(np.random.default_rng(3).normal(0,flare.std(),n),r,"decimate"))
    print(f"  {r:>5} {fd:>10.3f} {fm:>11.3f} {nd:>10.3f} {-0.5:>11.3f}")
print("  => sigma-shrink removes BOTH the n-shrinkage/header confound and the model floor.")
print("     If flare sigma-shrink STILL decays to ~0 under decimate, the decay is real memory-loss,")
print("     not an n-shrinkage compression artifact.")

# 4b-control: pad-back-to-fixed-n by tiling the decimated series, recompute comp-ratio.
print("\n (4b-pad) Decimate then TILE back to n>=10000 (removes n-shrinkage from coder overhead):")
print(f"  {'rung':>5} {'comp_ratio_padded':>18} {'comp_ratio_raw':>15}")
for r in RUNGS:
    xr = coarsen(flare, r, "decimate")
    reps = int(np.ceil(10000/len(xr)))
    xt = np.tile(xr, reps)[:max(10000,len(xr))]
    print(f"  {r:>5} {persistence_comp(xt):>18.3f} {flare_dec[r]:>15.3f}")
print("  (tiling injects artificial periodicity; read only whether the DIRECTION of decay persists)")

print("\nDONE.")
