# External pass — gemini (+ codex pending) on V6_RESULTS.md (2026-06-17)

Cross-model A− on the V6 additive-factors claim. Raw: `../session_arc/gemini_v6results_review.md`
(codex `../session_arc/codex_v6results_review.md` was still running at write time — fold when it lands).
**gemini verified the numbers and then dismantled the framing — correctly.** Demote-not-kill.

## gemini verdict: UNCONFIRMED / OVERCLAIMED — and it's right
gemini reproduced the result exactly from `v6_run.jsonl` (median +8.5, sign-test p=0.0654, CI [+2.0,+12.5]),
then made four points I have to concede:

1. **The pre-registered rule FIRED "super-additive → demote," and I pivoted away from it.** The script's
   own decision logic (median > 8.0 null AND bootstrap CI excludes 0) triggered the SUPER-ADDITIVE branch.
   My report's "~90% additive-dominant" reframing was **post-hoc rhetorical salvage** that contradicted the
   pre-registration. That's the exact failure mode this project is supposed to guard against.
2. **Additive-factors is a FALSIFICATION tool (this is the methodological crux).** Sternberg (1969): if you
   find an interaction, you **must reject** the independent-serial-stages hypothesis. A super-additive
   interaction whose CI excludes 0 therefore **falsifies the modularity** of encode×depth for gpt-5.5 — it
   does **not** "reproduce the additive signature." I had the logic backwards: finding an interaction is the
   *negative* result, not a softer positive one.
3. **The interaction is NOT negligible.** The depth effect is ~8.4 tok/op; the +8.5 interaction ≈ **one full
   extra reasoning step.** Calling that "small / within the null band" was an unforced calibration error; the
   ±8 null was conveniently close to the observed 8.5.
4. **N=12 is underpowered** — the bootstrap CI excludes 0 but the sign test (p=0.065) does not; I leaned on
   the favorable statistic. And the interaction may be a **verbosity/context-pressure artifact** (long chain
   + complex setup → more "show-your-work"), not a cognitive-stage effect.

## The honest V6 result (demoted)
- **NOT** "the chronometric method reproduces / the cost is ~90% additive." 
- **IS:** *the additive-factors method ran on reasoning_tokens and detected a small but CI-significant
  super-additive interaction (+8.5 tok ≈ one step), which — by Sternberg's own logic — REJECTS clean
  modularity of the encode and depth stages for gpt-5.5 at N=12.* The chronometric *apparatus* transfers
  (we can run the design and read an interpretable interaction); the clean *additive signature* did not appear.
- This is still a real result and on-thesis: the method discriminates. It just landed on "not cleanly
  modular," not "validated additive."

## Demotions to fold
- "chronometric method REPRODUCES; ~90% additive; rediscovery-as-validation made load-bearing" →
  **"the additive-factors apparatus transfers; it found a super-additive interaction → modularity REJECTED
  at N=12 (escalate to N≈48 to confirm sign/size)."**
- "small interaction within the null band" → **"interaction ≈ one full reasoning step; not negligible; the
  ±8 null was mis-calibrated."**
- the FLAG (BIG_MAP) "the chronometric inversion, run" → **"run once; it falsified clean modularity rather
  than confirming additivity — informative, not the hoped-for validation."**

## Next
1. **Escalate to N≈48 seeds** — settle whether the +8.5 interaction is a stable property or sampling noise
   (the single decisive cheap move both the script and gemini call for).
2. **Pre-register a principled null** (not "one op"): e.g., the interaction must exceed a fraction of the
   smaller main effect, fixed before the run.
3. **Control the verbosity-artifact** — report correct-trace-only and a length-residualized interaction.

## codex (folded) — converges, and sharpens the verdict to *borderline*
codex verdict: **overclaims-remain** (same direction as gemini). Its sharper points:
- **The interaction is statistically BORDERLINE, not robustly nonzero.** Per-seed interactions are
  `[7,25,13,4,-5,12,10,0,10,13,-11,6]` (median +8.5, mean +7.0, 6/12 ≤+8 vs 6/12 >+8). The **exact
  order-statistic ~96% CI for the median is [0, 13] — it INCLUDES 0.** So "bootstrap CI excludes 0" is *not*
  robust at n=12. (This actually softens gemini's "modularity rejected" → the honest call is **inconclusive/
  underpowered**, leaning slightly super-additive.)
- **Sternberg logic does not transport automatically (the deepest point).** Additivity isn't proof of
  discrete stages even in human RT — cascade / continuous-flow models mimic additive factors (McClelland
  1979; Stafford & Gurney 2011). For LLMs, reasoning_tokens are a *generated trace, not elapsed time*, so
  additivity may just mean *"one decode block + D chain blocks written,"* not separable cognition.
- **ENCODE is not cleanly a different stage** — the 3-op decode uses the *same* arithmetic (+,*,-,%) as the
  chain, so it may be "three more ops before the chain," not a distinct encoding stage. Construct-confounded.
- **Depth is noisier than needed** — RNG keyed on `(D,seed)` means D=12 isn't an *extension* of D=4 (different
  s0/ops); E-arms are still matched within (D,seed), so not fatal, but it adds item noise.

## Net synthesis (both)
**V6 is overclaimed and now demoted.** The honest result: *the additive-factors apparatus transfers — we can
run the 2×2 and read an interpretable pattern (large additive main effects, encode +23 / depth +67) — but the
interaction is **borderline at n=12** (bootstrap excludes 0, exact order-statistic CI [0,13] does not; sign-p
0.065), so **staged cognition is NOT identified** either way.* The hoped-for "clean additive signature
validates the chronometric camera" did not appear; nor is modularity cleanly refuted. And **seed-escalation
will not fix the real blocker** — the transcription-vs-cognition + ENCODE-construct confound.

## The decisive next move (codex — better than escalating seeds)
A matched **irrelevant-expression control**, crossed with D:
- `E0`: `s = 437`
- `E3-live`: `s = (((a+b)*c)-e) % 1000`  (must be computed)
- `E3-dead`: `ignore (((a+b)*c)-e) % 1000; s = 437`  (same text, explicitly irrelevant)

If **E3-dead ≈ E3-live** → V6 was mostly prompt/transcription cost. If **E3-dead collapses to E0** while
E3-live stays costly → the decode load is genuinely *computational*. *Then* fix the depth-as-true-extension
issue and only then escalate to N≈48. This separates the confound that seeds cannot.

## Demotions to fold (merged)
- "chronometric method reproduces / ~90% additive / rediscovery-as-validation load-bearing" → **"a
  Sternberg-inspired 2×2 token assay; additive-dominant main effects with a BORDERLINE interaction at n=12;
  staged cognition not identified; a promising validation *probe*, not yet load-bearing."**
- "the camera reads genuine staged structure" → **"reasoning_tokens track compositional task/prompt work
  here; separable cognition is not established (cascade models mimic additivity; tokens are a trace, not time)."**
