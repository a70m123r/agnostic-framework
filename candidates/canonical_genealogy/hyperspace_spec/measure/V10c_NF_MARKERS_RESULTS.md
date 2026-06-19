# V10c (selector-position 3x2) + the NF marker-count fix — the frame component pinned, the compute endpoint cleaned

**Date:** 2026-06-19 | The capstone controls for the frame + amortization components, with a codex external pass
on V10c (4-cell) that drove a design fix (the true-absent Z arm). Demote-not-kill.

## V10c — does the surviving frame cost come from ORIENTING (missing frame) or late-instruction RESCAN (trailing selector)?
Built as the control FOUR auditors independently named. Application-free neutral-marker locate ([tag: KEEP]),
BYTE-IDENTICAL body per seed, POSITION perfectly length-matched. First run = 2x2 {H present | absent-as-neutral}
x {LEAD | TRAIL}. codex audit (`session_arc/codex_v10c_audit.md`): the rescan story was killed but "absent" was
not TRUE absence (an active neutral sentence) -> can't separate header-HELPS from neutral-line-HURTS. FIX: added
a true-absent **Z** arm (no first line) -> 3x2, 240 items x 4 reps, lock `fc589892`.

### Result 1 (6-cell): ORIENTING is real, and it is header-HELPS not neutral-line-HURTS
| contrast | deepseek | qwen | gemini |
|---|---|---|---|
| N − H (neutral vs frame) | +15.8 (p=.038) | +140.6 (p=.002) | +155.1 (p=.002) |
| **Z − H** (true-absent vs frame) | +5.0 (ns) | **+80.7 (p=.038)** | **+135.5 (p<.001)** |
| **N − Z** (neutral vs true-absent) | +7.4 (ns) | +13.1 (ns) | +42.3 (ns) |

On qwen + gemini (the models with reasoning headroom): **H < Z ≈ N** — the system-log frame is significantly
cheaper than BOTH true-absence and a neutral sentence, and the neutral line costs no more than absence (N≈Z).
=> a genuine MISSING-FRAME ORIENTING cost; codex's "neutral-line-hurts" alternative REFUTED (N≈Z). deepseek is
floored (~110 tok), its 3-way underpowered (effects ~5-16 tok), consistent direction only.

### Result 2: late-RESCAN is NOT cleanly refuted -- a small, run-VARIABLE co-contributor
POSITION (trailing − leading, perfectly length-matched): 4-cell run = NULL on all 3 (deepseek +3.6 p=.64,
qwen −23 p=.88, gemini +42 p=.08); 6-cell run = small-positive-SIG on 2/3 (deepseek **+19.9 p<.001**, gemini
**+82.7 p=.038**, qwen +73 ns). At ~+20–83 tok it sits at the noise floor and flips significance across
independent runs. Honest: a small late-rescan component that is real-ish but UNSTABLE at n=40 -- not zero, not
dominant.

### V10c landing (DC-39 resolved, nuanced)
The application-independent frame cost (SV's +113/+372/+405) = a **robust ORIENTING component** (header-helps,
clean via the Z bridge on qwen+gemini) **+ a small, borderline late-rescan component** (POSITION ~+20–80,
run-variable). The clean "pure orienting, rescan refuted" the 4-cell hinted does NOT survive the larger run; both
mechanisms contribute. DC-39 -> "orienting CONFIRMED (header-helps, not neutral-confusion); a minor unstable
rescan co-contributes; needs n>=100 for a stable position estimate."

## NF marker-count fix (DC-38 revisited) — separating THINKING from NARRATING about thinking
Both audits' #1 methodological note: reasoning_tokens conflate compute with NARRATION LENGTH. Re-scored NF on the
count of trial-division markers in the reasoning TEXT (`nf_markers.py`, no new API calls -- the CoT is saved).

| contrast | deepseek | qwen | gemini |
|---|---|---|---|
| WORD shortcut HARD_WORD−HARD_PLAIN: **markers** | **−2.7 (p<.001)** | **−7.3 (p<.001)** | **−1.2 (p=.001)** |
| same, in reasoning_tokens | −43 | −185 | −318 |
| compute HARD_PLAIN−TRIV_PLAIN: **markers** | +12.5 (p<.001) | **+24.7 (p<.001)** | +0.3 (ns) |
| same, in reasoning_tokens | +144 | +113 (ns) | +488 |

Findings: (1) **DC-38 PARTIALLY UN-DEMOTED** — the cached word 'prime' genuinely cuts trial-division markers on
all 3 (a REAL compute saving), though the token drop is larger than the marker drop -> narration rides on top.
Not "pure narration" (the audit) nor "clean amortization" (my original) -- BOTH. (2) **reasoning_tokens is a
model-DEPENDENT-noisy compute proxy**: qwen DOES far more trial division (markers +24.7) than its tokens showed
(rt +113 ns -- markers rescue a compute effect rt missed); gemini RECALLS primality (markers ~0) yet spends huge
tokens (rt +488) -- its "compute cost" is recall+narration, not division. The three models pay for a hard
predicate in different currencies. (3) NONCE@hard markers ~0 on all 3 -> the V11b RENAMED rt effect was
binding/narration, not compute (confirms that demotion). The SPINE is untouched (the big dissociations only
sharpen under markers); this refines the amortization component + adds a caveat to every fine-grained rt claim.

## Net for the camera
- **Application** (volume, scales with #candidates): dominant. SPINE.
- **Reading-volume**: DEAD (size = predicate-evaluation, 3x confirmed). SPINE.
- **Amortization**: a cached word genuinely cuts compute markers (real) + a narration component; rt is a noisy
  per-model compute proxy -> prefer marker-counts.
- **Frame**: orienting (header-helps, clean) + a small unstable rescan component.
Cost: V10c ~$3 + NF marker re-score $0. Audits $0 (codex). Dead-children -> DC-38 refined, DC-39 resolved.
