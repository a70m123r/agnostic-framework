# NF + SV — cross-model audited: the de-amortization mechanism sharpened; the camera's SPINE confirmed; two components demoted

**Date:** 2026-06-19 | The two next-controls the V10b/V11b auditors named (NF = label vs compute; SV = same-task
application removal), built + locked + run across deepseek/qwen/gemini, then put through **two independent
subscription audits** (codex/GPT external + a Claude 7-skeptic adversarial workflow). Both re-derived every
number from the locked files; both CONVERGE. This is a humbling-but-sharpening cycle: the camera's spine holds,
the de-amortization mechanism is refined, and two "extra" components are demoted to confounded. Demote-not-kill.
Params: [CROSS_MODEL_RUNCARD.md](CROSS_MODEL_RUNCARD.md). Audit docs: session_arc/{codex,claude}_nf_sv_audit.md.

## The instruments
- **NF** (`v_nf_labelcompute.py`, lock `354d7d5e`, 60 seeds): 5 conds isolating LABEL (rule stated PLAIN vs
  coined NONCE) x COMPUTE (trivial last-digit vs hard primality), all selecting the IDENTICAL needle (prime AND
  unique last-digit-{3,7}); finals given so only predicate+label varies. HARD_WORD uses the amortized word 'prime'.
- **SV** (`v_sv_verdict.py`, lock `9093531`, 24 seeds): V10's 6 frame conds, every line pre-tagged
  [verdict: PASS/fail], task = "report the PASS computation's value" -> removes application WITHOUT switching task.
  3-way vs V10 prime / V10b lookup via `compare_3way.py`.

## SURVIVES CLEAN (both audits) -- the camera's spine
1. **The size axis is predicate-EVALUATION volume, NOT reading volume.** (SV-C3, reproduced both.) Under the
   application-free verdict task, rt is FLAT-to-NEGATIVE with 5x more substrate (deepseek -55/-85, qwen -283/-176,
   gemini null) -- the THIRD independent confirmation (after V10b lookup). The "universal reading-volume cost"
   from V10 is dead. (Scope-limit flagged: SV collapses toward the locate floor at L on 2/3 models, but the
   negative slope refutes reading-volume regardless of floor proximity.)
2. **A hard predicate costs more to APPLY than a trivial one.** (NF-C3, reproduced.) HARD_PLAIN-TRIV_PLAIN =
   +144 (deepseek, p<.001), +488 (gemini, p<.001), length-control-robust. qwen = underpowered-leaning-null
   (genuinely null vs a gemini-sized effect; could miss a deepseek-sized +144 ~1/3 of the time; symmetric
   dispersion SD~640, not a tail/accuracy artifact).

## SURVIVES AS DIRECTION / LOWER-BOUND
3. **Application-volume is the dominant reasoning cost.** (SV-C1, direction survives, conservative.)
   D_application = rt(prime)-rt(verdict) at matched cond = +524..+7568 (deepseek), +1480..+11980 (gemini),
   +2572..+10926 (qwen), GROWING with size. Conservative: the prime prompt is ~15% SHORTER yet costs 30-50x more
   rt (not a reading artifact); gemini prime-accuracy survivorship censors the hardest items (understates prime).
   DEMOTE the over-claims: NOT "all p<.001" (deepseek F3 p=.013; qwen F3 sign-reverses), cross-exp is n=14 (V10
   prime ran 14 seeds), and qwen is NOT application-free (it re-verifies the arithmetic behind PASS -> the qwen F3
   anomaly; D_app is a conservative lower bound for qwen).

## REPRODUCED & STANDING -- the de-amortization MECHANISM, sharpened
4. **Pure nonce-naming is NOT a universal tax; the cost is word-amortization x rule-difficulty.** (NF-C2.)
   Coining a novel name for a TRIVIAL rule does not robustly cost (TRIV_NONCE-TRIV_PLAIN: deepseek +35 small-real,
   qwen null, gemini -306 NEGATIVE). The real warrant is the **difficulty SIGN-FLIP**: the same coin-and-deref
   operation costs +614 (gemini) when wrapping a HARD rule (HARD_NONCE-HARD_WORD) but -306 when wrapping a TRIVIAL
   one. So V11b's RENAMED +162/+263/+241 was NOT content-free label-binding -- it was **losing the amortized WORD
   'prime' and having to carry+APPLY the explicit hard rule**. De-amortization bites only when the un-cached
   concept must then be applied.

## DEMOTED -- dated dead-children (both audits flagged each)
- **DC-38 "WORD shortcut = amortization"** -> **reading-LENGTH confound.** (NF-C1.) HARD_WORD (21 words) is the
  shortest and cheapest HARD cell; HARD_NONCE (41 words) the longest and dearest -- despite being the UN-amortized
  nonce (amortization predicts the opposite). Traces: PLAIN and WORD do the SAME trial-division (WORD sometimes
  MORE), so application is identical; what shrinks is reading the longer rule. reasoning_tokens conflate compute
  with NARRATION LENGTH -> use the trial-division-MARKER count as the amortization endpoint instead.
- **DC-39 "SV rescues frame-ORIENTING"** -> **application-independent frame cost survives, but orienting vs
  late-rescan UNSEPARATED.** (SV-C2.) D_frame (F1_S-F2_DEINDEXED) = +113/+372/+405 (all sig) is real, BUT F1_S
  vs F2_DEINDEXED still crosses {header removed + selector TRAILING} vs {header present + selector LEADING} -- the
  exact V10 confound. SV's clean contribution is on the ORTHOGONAL task axis (application removal); on header/
  position it inherits V10's confound verbatim. V10c still required.
- **DC-40 "SV-C4 answer-format cost"** -> **re-triggered application.** "Report the one PASS value" makes the
  model DISTRUST the tags and re-execute the arithmetic; verdict>lookup conflates search-key + objective changes,
  not a clean answer-format isolate.

## THE CONVERGED NEXT CONTROL (named by BOTH audits -> 4 auditors total)
**Build V10c** -- the compute-free / verdict-task **{HEADER present | absent} x {selector LEADING | TRAILING}**
2x2, byte-identical body, length-matched neutral pad in the header slot, and a **NEUTRAL marker** ([tag: KEEP],
NOT PASS/fail, so qwen cannot read it as "verify the arithmetic"). Report the POSITION main effect (perfectly
length-matched) and the HEADER main effect with position held. This single control gates the ENTIRE frame
component: POSITION swamps + HEADER CI includes 0 -> orienting collapses to late-instruction rescan (DC-39 + V10
orienting demote); HEADER significant with position held -> orienting survives sharpened. Spec: AGY_V10C_BRIEF.txt
(written, unbuilt). Methodological upgrade: pre-register the trial-division-marker count as the amortization
endpoint (reasoning_tokens conflate compute with narration length -- the DC-38 lesson).

## The honest landing
The camera's SPINE is robust and cross-model: the reasoning cost is PREDICATE APPLICATION whose VOLUME scales
with the number of candidates (not bytes read) -- confirmed three times, survivorship-clean. The de-amortization
face is real but specific: losing an amortized WORD costs only when a hard rule must then be applied. The two
"extra" components (a clean word-shortcut, a clean frame-orienting cost) are each one confound away from
canonical -- and ONE control (V10c, neutral-marker) closes both. The audit loop demoted my own over-claims
(NF-C1, SV-C2/C4) before they entered the record -- the instrument working on itself.

## Cost / provenance
NF+SV spectrum ~$1-2 OpenRouter; both audits $0 (Claude workflow = Max sub; codex = ChatGPT sub, `-c
service_tier=fast`). Scope -> +NF/SV records, 40 dead-children (DC-38/39/40).
