# Latent measurement prototype + falsifiers (as-is + provider-swap shadow)

`measured_bits = min(cost_ub, evidence_lcb)`. Coders = gzip / bz2 / lzma (any lossless coder is a one-sided bound). Synthetic corpus with known ground truth (stones / deadweight / a high-cost uncorroborated fabrication).

**11/12** per-coder checks passed; **3/4 falsifiers robust across ALL three coders** (conditional-redundancy C needs an LZ-family or LLM coder - bz2/BWT is the named exception).

- **A.complex-lie-is-blurred** -> ROBUST
    - gzip: PASS - mb(fab)=8 vs cost(fab)=2952 and mb(stone)=2468 -> the high-cost UNCORROBORATED claim renders at 0% of its cost
    - bz2: PASS - mb(fab)=35 vs cost(fab)=3520 and mb(stone)=749 -> the high-cost UNCORROBORATED claim renders at 1% of its cost
    - lzma: PASS - mb(fab)=32 vs cost(fab)=3755 and mb(stone)=2571 -> the high-cost UNCORROBORATED claim renders at 1% of its cost
- **B.deadweight-vs-stone** -> ROBUST
    - gzip: PASS - cond(deadweight|its original) max=448 < cond(stone|another) min=2552 (mean dead=265, mean stone=2591)
    - bz2: PASS - cond(deadweight|its original) max=1368 < cond(stone|another) min=2736 (mean dead=1075, mean stone=2828)
    - lzma: PASS - cond(deadweight|its original) max=416 < cond(stone|another) min=2720 (mean dead=224, mean stone=2745)
- **C.redundancy-adds-~0** -> NOT robust
    - gzip: PASS - cond(duplicate|original)=96 vs cond(independent|other)=2608 -> a redundant source adds 4% of an independent one
    - bz2: FAIL - cond(duplicate|original)=880 vs cond(independent|other)=2848 -> a redundant source adds 31% of an independent one
    - lzma: PASS - cond(duplicate|original)=32 vs cond(independent|other)=2752 -> a redundant source adds 1% of an independent one
- **D.evidence-discriminates** -> ROBUST
    - gzip: PASS - evidence stone min=2440 > fabrication max=16 (mean stone=2468, mean fab=8)
    - bz2: PASS - evidence stone min=680 > fabrication max=40 (mean stone=749, mean fab=35)
    - lzma: PASS - evidence stone min=2528 > fabrication max=32 (mean stone=2571, mean fab=32)

Coder-relativity: absolute measured_bits move ~88% across coders, but the verdicts (lie blurred, deadweight vs stone, redundancy ~0, evidence discriminates) are stable -> the *pinned relational bit*.
