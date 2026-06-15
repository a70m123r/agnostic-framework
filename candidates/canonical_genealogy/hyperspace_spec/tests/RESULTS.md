# Keyhole / block-universe settling-experiment results

`10/10` checks passed. Pure numpy/FFT toys; falsification harness (honest policy must beat dishonest).

- **PASS** `T1.honest-region-contains-truth` - truth in Lipschitz lens (d_a=1.08<=rA=3.55, d_b=1.11<=rB=3.55); honest blur ~3.55
- **PASS** `T1.presentism-is-confidently-wrong` - linear-interp point misses truth by 0.636 (>> noise 0.03) - a fake sharp bit on the time axis
- **PASS** `T1.blur-is-honest-not-sharp` - honest blur 3.55 > presentism error 0.64 -> refusing to render a point it cannot justify
- **PASS** `T2.diversity-beats-density` - 12 angles spread over 180deg capture 0.451 of energy vs 0.347 clustered in 60deg
- **PASS** `T2.submodular-diminishing-returns` - adding angle 73 gains 0.008 on a 2-angle set vs 0.008 on a 6-angle superset
- **PASS** `T2.greedy-marginals-non-increasing` - greedy per-burst gains non-increasing (first 0.180 -> last 0.036)
- **PASS** `T2.duplicate-burst-adds-~0-bits` - a re-fired (duplicate) angle adds 0.00e+00 new energy; an independent one added 0.008
- **PASS** `T2.active-competitive-with-optimal-even` - active reaches 90% coverage in 14 bursts vs 20 even; clustered-in-60deg never (999)
- **PASS** `T2.missing-wedge-cannot-be-fabricated` - a sharp guess in the unmeasured wedge correlates 0.009 with truth (~0) -> only honest render there is blur
- **PASS** `T2.sampled-coeffs-are-exact` - honest recon (sampled coeffs only) error = 0.651 and is pure low-pass blur, no fabricated frequencies
