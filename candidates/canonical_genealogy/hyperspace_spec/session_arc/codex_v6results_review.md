## Verdict
**overclaims-remain** — the additive-dominant token pattern is real; the “Sternberg reproduces / validates staged cognition” framing is too strong.

## Residual Issues

1. **Statistical verdict is edge-case, not clean reproduction.**  
   Per-seed interactions are `[7, 25, 13, 4, -5, 12, 10, 0, 10, 13, -11, 6]`: median `+8.5`, mean `+7.0`, sign test `p=0.065` with one zero. Since the preregistered null band is `±8`, the result is only `0.5` token outside the band, and exactly `6/12` seeds are `<= +8` while `6/12` are `> +8`. The bootstrap CI excluding zero is not enough to override that. An exact order-statistic CI for the median at about 96% coverage is `[0, 13]`, so “CI excludes 0” is not robust at `n=12`.

2. **“~90% additive” is descriptively OK, inferentially soft.**  
   Main effects are large: encode about `+23 tok`, depth about `+67 tok`. The interaction is small relative to their sum, but not small relative to the encode effect or the preregistered one-op null band. Honest wording: **“large additive main effects with a small positive interaction at the null-band boundary.”**

3. **Sternberg logic does not transport automatically.**  
   Sternberg’s additive-factors method depends on selective influence over serial processing stages, not merely additive totals ([Sternberg 1969](https://doi.org/10.1016/0001-6918(69)90055-9)). Even in human RT, additivity is not sufficient proof of discrete stages; cascade and continuous-flow accounts can mimic additive factors ([McClelland 1979](https://doi.org/10.1037/0033-295X.86.4.287)), and worked modeling examples make the same point ([Stafford & Gurney 2011](https://doi.org/10.3389/fpsyg.2011.00287)). For LLMs, reasoning tokens are a generated hidden trace, not elapsed time. Additivity may mean “the model writes one decode block plus D chain blocks,” not “separable cognitive stages.”

4. **ENCODE is not cleanly different-stage.**  
   The `E=3` condition is another arithmetic expression using the same operations as the chain: `+`, `*`, `-`, `% 1000`. It may be “three more arithmetic ops before the chain,” not a distinct encoding stage. The prompt balancing is good: `E=3` adds a constant `+8` prompt words across depths. But constant prompt length does not solve the construct problem: syntax complexity, hidden scratchpad policy, and same arithmetic execution remain confounded.

5. **Depth is noisier than it needs to be.**  
   In `v6_additive.py`, RNG is keyed by `(D, seed)`, so `D=12` is not an extension of the `D=4` chain for the same seed; it uses a different `s0` and different operations. That is not fatal, because E arms are matched within `(D, seed)`, but it adds item noise to the interaction estimate.

## Demotions

- Demote **“the additive-factors method reproduces on reasoning_tokens”** to:  
  **“A Sternberg-inspired 2x2 token-count assay shows additive-dominant costs on one model/tier/factor-pair.”**

- Demote **“the camera reads genuine staged structure”** to:  
  **“reasoning_tokens track compositional prompt/task work here; staged cognition is not identified.”**

- Demote **“small super-additive residual is a finding”** to:  
  **“suggestive positive interaction at the preregistered boundary; needs replication and controls.”**

- Demote **“rediscovery-as-validation made load-bearing”** to:  
  **“promising validation probe, not yet load-bearing.”**

## Next Move

Do **not** just escalate seeds first. More seeds will refine the `+8.5` estimate but will not resolve the transcription-vs-cognition confound.

Cheapest decisive add-on: run a matched **irrelevant-expression control**.

- `E0`: `s = 437`
- `E3-live`: `s = (((a + b) * c) - e) % 1000`
- `E3-dead`: same expression text present, but explicitly irrelevant, e.g. `ignore (((a + b) * c) - e) % 1000; s = 437`

Cross that with `D=4/12`. If `E3-dead` costs like `E3-live`, V6 is mostly prompt/transcript cost. If `E3-dead` collapses to `E0` while `E3-live` remains costly, the decode load is more plausibly computational.

Then run the stronger same-stage-vs-different-stage contrast, with `D=12` generated as a true extension of `D=4`, and only then escalate to `24-48` seeds.
