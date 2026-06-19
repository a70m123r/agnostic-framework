**Verdict:** the clean rerun really flips F0 positive, but the honest claim is “there is a compute-free residual locating/late-frame cost, strongest in Gemini,” not yet “orienting mechanism proven universally.”

I verified the fixed lock `cb7ecfdd`: the locked labels hash matches, all 448 records/model map cleanly to the fixed labels, and F0 has zero arithmetic lines missing `=>`. The fix is in [v10_framestrip.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10_framestrip.py:107), with the guard at [v10_framestrip.py](D:/PlatformOperator/research/pav/candidates/canonical_genealogy/hyperspace_spec/measure/v10_framestrip.py:207).

Clean F0 falsifier, using the generator’s method: per-seed mean over correct reps, then median delta/sign test:

| model | F0_DISSOLVED - F0_DEINDEXED | sign | p |
|---|---:|---:|---:|
| deepseek | `+149` | 11+/3- | `.057` |
| gemini | `+2303` | 14+/0- | `<.001` |
| qwen | `+376` | 10+/4- | `.180` |

So yes, the headline numbers reproduce. DeepSeek’s flip is real in the current raw data, but inferentially borderline: one decent negative seed remains, n=14 is small, and `.057` is not a clean single-model win. I did not find old raw buggy JSONL here, only old notes citing `-47`, so I would not treat the old magnitude as independently reverified from this cwd.

The F0 arms are body-matched, not literally prompt-length identical: same F0 body, same arithmetic-line counts, same needle hash/truth, exactly one prime-final line in each; but F0_DISSOLVED is fixed `7` words and 2 lines shorter because the top “system log” wrapper is absent. That means the positive F0 effect is not “more lines to read” in dissolved. The remaining confound is different: F0_DISSOLVED puts the selector after the body, so the cost may be late-instruction/rescan plus locating `=>` candidates, not abstract orienting alone.

The reading-volume axis is solid: `F1_M - F1_S` reproduces as deepseek `+2578`, gemini `+4377`, qwen `+3068`, all sign-positive enough to support a universal volume cost. Gemini’s `F1_L` accuracy collapse to `39/56` does bias exact large-size magnitudes under correct-only conditioning, but it does not touch F0; all-call Gemini large-size signs remain positive.

`CROSS_MODEL_RUNCARD.md` is stale: it still says the F0 runs are compromised and a clean rerun is required.

**Most important remaining control:** run an exact-length, selector-position-crossed F0 control: same body/substrate, padded to equal tokens, with top-vs-trailing selector crossed against deindexed-vs-dissolved framing. That separates true missing-frame/orienting cost from late-instruction/rescan cost.
