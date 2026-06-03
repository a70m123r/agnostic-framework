# Pilot #150b — SEED / DRAFT proposal — within-system texture *cycling* (squeeze ↔ pull), no political binary

> **STATUS: DRAFT SEED — NOT a locked pre-registration, NOT canon, NOT a promoted candidate.**
> Written by the Claude Code session on **2026-06-03**, immediately after Pilot #150's confounded null, capturing Pav's steer:
> *"the authoritative = bad, democracy = good is biased — its cycles of squeeze and pull, steers."*
> This is a hypothesis-**generating** sketch for Cowork to evaluate, refine, and **formally lock before any 150b data is examined**. Because it was written *with knowledge of #150's outcome*, it carries pre-registration-fitting risk and must be re-derived/locked independently (cont 27 §2 discipline). Do not run data against this draft as-is.

---

## §0 Why this exists — what #150 got wrong

Pilot #150 ([results/discussion.md](results/discussion.md)) tested a **static** spectral exponent β per country and asked whether a fixed **political label** (authoritarian vs pluralistic) predicts it. It returned a **confounded null**, and the post-mortem exposed two design flaws Pav named directly:

1. **The β contrast was a volume artifact** — Welch β tracked per-country event volume at r = 0.92 (confounds.md §10); the volume-robust DFA-α showed *no* cross-country difference. The test couldn't separate "authoritarian" from "lightly covered by GDELT."
2. **The authoritarian/pluralistic axis is a biased, static binary** — value-coded, Western/English-media-coded, and frozen for 11 years across systems that visibly shifted (Turkey, Russia, Venezuela mid-window). The pre-registration's own confound §8.1 + the demoted hypothesis **H4** already half-acknowledged this.

**The reframe (Pav's steer):** the failsafe claim was never really about a *fixed* β. It's about whether a system retains the **capacity to cycle** — to squeeze (tighten/narrow) and pull (loosen/diversify) and **recover toward broadband 1/f after a shock**. Capture/failure is **loss of cycling** — getting stuck clamped (over-correlated) *or* stuck loose (random) — not a low average value. So measure **texture *over time*, within each system**; each system is its own control; no political binary needed.

---

## §1 Draft hypotheses (illustrative — Cowork to finalize + lock)

Let τ(t) be a **volume-robust texture estimate** (rolling DFA-α, or Poisson-thinned-to-constant-rate β — see §3) computed in sliding windows over each country's daily signals.

- **H1b — texture is dynamic (breathing exists).** Within each country, τ(t) varies significantly across windows (variance exceeds a phase-randomized / block-bootstrap null). *Falsifier:* τ(t) is flat (indistinguishable from a constant + noise) for most countries → there is no "cycle" to study and the framing is wrong.

- **H2b — texture co-moves with an INDEPENDENT openness signal.** Within each country, τ(t) correlates with an externally-published, **pre-specified** media-openness time series (candidates: V-Dem `v2mecenefm` government media-censorship, or `v2x_freexp_altinf`; RSF press-freedom index — all annual). Direction: when the external index says *squeeze* (openness↓), τ moves **away** from the 1/f regime; when it says *pull* (openness↑), τ **returns toward** 1/f. *Falsifier:* no within-country association between τ(t) and the openness index beyond a shared-trend / volume null.
  - **This is the fix to the bias critique:** it replaces the value-loaded auth/plur label with "does information-texture track an independently-measured openness signal, *in whichever direction it moves*." No "auth = bad" assumption; squeeze and pull are symmetric.

- **H3b — capture = collapse of cycling.** During sustained capture episodes (defined *only* by the external index, pre-registered), the **amplitude of τ-cycling shrinks** (rolling variance of τ(t) declines) and/or τ drifts one-way and fails to recover. *Falsifier:* cycling amplitude is unchanged or grows during capture.

H2b is the sharpened, properly-controlled successor to #150's demoted **H4**.

---

## §2 What gets measured

- **Signals:** same GDELT v2 daily aggregates as #150 (category_entropy primary; event_count, mean_tone secondary) — already in `data/raw/`, no new ingest needed for a first pass.
- **NEW — external openness index** per country per year (V-Dem and/or RSF), the independent variable for H2b/H3b. Lock the source + exact variable *before* computing τ(t).
- **Texture trajectory:** τ(t) via rolling window (sketch: 730-day window, 30-day step) → ~120 windows/country over 2015–2026.

---

## §3 The one non-negotiable design requirement — kill the volume confound *in the time domain*

#150's killer (β ~ volume, r=0.92) **returns in the time domain**: within a country, event-volume(t) grows over the decade and spikes during crises, so a naive β(t) would track volume(t), not openness. 150b is worthless unless this is handled up front:

1. **Use a volume-robust estimator** — DFA-α(t) (which showed the null/flat behavior in #150, i.e. it is *not* fooled by the volume floor), and/or
2. **Poisson-thin every window to a common event rate** before estimating texture, and/or
3. **Regress volume(t) out** of τ(t) and report residual associations.
4. **Gate:** pre-register that within-country corr(τ(t), volume(t)) must be reported, and that H2b is only accepted on the volume-residualized signal.

---

## §4 Confounds to pre-register (beyond #150's list)

1. **Within-country volume(t)** — primary; see §3.
2. **GDELT pipeline drift over time** (v2.0→v2.1 schema changes are dated) → could create spurious τ(t) *trends* mistaken for cycles. Check against GDELT's update log; detrend or flag.
3. **Global common-mode events** — COVID (2020–2022), major wars hit all countries at once → common-mode τ shifts that aren't country-specific steers. Remove a global/median baseline; report common-mode separately.
4. **Steer-event endogeneity / cherry-picking** — *do not* hand-pick "squeeze events." Use the external index (§2) as the steer signal; lock source + variable + any event dates before touching τ(t).
5. **Window-length sensitivity** — τ(t) resolution depends on window/step; pre-register them and report a sensitivity sweep.
6. **External-index resolution mismatch** — V-Dem/RSF are annual; τ(t) is sub-annual. Pre-register how they're aligned (e.g., step-interpolate index, or aggregate τ to annual for H2b).

---

## §5 Relationship to existing framework + queued work (for Cowork — flagged, not asserted)

- **Squeeze/pull cycling** may map to the framework's **A⁻/A⁺ coupled pattern** (cont 13) and/or **supersede ↔ dormancy** dynamics (cont 20/28). Worth checking whether "loss of cycling = failsafe failure" is already implied by existing canon, or is a genuine extension. *Do not assert the mapping without the usual claim-validity read.*
- **May subsume or redirect Task #151** (RC-Koopman cultural-eigenmode pilot). Pav noted the cycling frame is "what #151 was reaching toward." Koopman/eigenmode methods are *natural* tools for "is there a cyclical mode in τ(t)?" — so #150b and #151 might merge into one well-posed pilot rather than two. Cowork's call.
- Keeps the framework's failsafe claim (cont 26 §3 / Reading 06 §10.3) **alive and testable** without the discredited static-binary operationalization — consistent with the "narrow, don't demote" recommendation in [results/discussion.md](results/discussion.md) §8.

---

## §6 Suggested next steps (Cowork)

1. Decide: standalone #150b, or merge with #151 (Koopman cycling-mode).
2. Pick + lock the external openness index (V-Dem variable vs RSF) **before** any τ(t) is computed.
3. Re-derive H1b/H2b/H3b cleanly (independent of this draft's wording) and **lock the pre-registration**, including the §3 volume-control gate and §4 confounds.
4. First pass can reuse `data/raw/` (no new GDELT ingest) — only the external index needs fetching.
5. Then, and only then, run it.

---

*Provenance: seed authored 2026-06-03 (Claude Code, post-#150-result-commit) from Pav's steer. Not locked, not canon. Successor framing to Pilot #150's confounded null.*
