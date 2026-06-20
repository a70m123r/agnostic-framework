# V10c (selector-position 3x2) + the NF marker-count fix — the frame component pinned, the compute endpoint cleaned

**Date:** 2026-06-19 | The capstone controls for the frame + amortization components, with a codex external pass
on V10c (4-cell) that drove a design fix (the true-absent Z arm). Demote-not-kill.

## V10c — does the surviving frame cost come from ORIENTING (missing frame) or late-instruction RESCAN (trailing selector)?
Built as the control FOUR auditors independently named. Application-free neutral-marker locate ([tag: KEEP]),
BYTE-IDENTICAL body per seed, POSITION perfectly length-matched. First run = 2x2 {H present | absent-as-neutral}
x {LEAD | TRAIL}. codex audit (`session_arc/codex_v10c_audit.md`): the rescan story was killed but "absent" was
not TRUE absence (an active neutral sentence) -> can't separate header-HELPS from neutral-line-HURTS. FIX: added
a true-absent **Z** arm (no first line) -> 3x2, 240 items x 4 reps, lock `fc589892`.

### Result 1 (STABILIZED at n=100, lock 68c45104): ORIENTING is real on ALL 3 -- header-HELPS not neutral-HURTS
| contrast | deepseek | qwen | gemini |
|---|---|---|---|
| N − H (neutral vs frame) | +8.2 (p=.007) | +126.9 (p<.001) | +120.2 (p<.001) |
| **Z − H** (true-absent vs frame) | **+9.9 (p=.007)** | **+145.2 (p<.001)** | **+118.0 (p<.001)** |
| **N − Z** (neutral vs true-absent) | +1.2 (ns) | +16.8 (ns) | +13.5 (ns) |

On ALL THREE models (n=100 firmed up deepseek, which was floored at n=40): **H < Z ≈ N** — the system-log frame
is significantly cheaper than BOTH true-absence (Z) and a neutral sentence (N), and the neutral line costs no
more than absence (N≈Z, null all 3). => a genuine MISSING-FRAME ORIENTING cost, cross-model; codex's
"neutral-line-hurts" alternative REFUTED on all 3 (N≈Z).

### Result 2 (n=100): late-RESCAN resolves from "run-variable" to MODEL-DEPENDENT
POSITION (trailing − leading, perfectly length-matched): deepseek **+17.4 (p<.001, small)**, gemini
**+93.4 (p<.001, moderate)**, qwen +5.5 (**null**, p=.62). The n=40 run-variance (null in the 4-cell, sig in the
6-cell) resolves at n=100 into a clean MODEL-DEPENDENT pattern: a real late-rescan cost on gemini (moderate) and
deepseek (small), ABSENT on qwen. Not null-on-all, not sig-on-all -- it genuinely differs by model.

### V10c landing (DC-39 resolved, n=100)
The application-independent frame cost (SV's +113/+372/+405) = a **robust cross-model ORIENTING component**
(header-helps, clean via the Z bridge: H < Z ≈ N on all 3) **+ a MODEL-DEPENDENT late-rescan component**
(POSITION: gemini +93 / deepseek +17 / qwen null). Both mechanisms contribute; orienting is the robust one,
rescan is real-but-model-specific. DC-39 -> "orienting CONFIRMED cross-model (header-helps, not neutral-confusion);
late-rescan is a real model-dependent co-contributor (gemini/deepseek yes, qwen no). Stabilized at n=100."

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
