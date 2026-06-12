# DIAL PROTOCOL — SWEEP LOG (append-only)

> Dated record per sweep, per `DIAL_PROTOCOL_SPEC.md` §3.7. Never edit a prior section.

---

## Sweep 0 — 2026-06-12 (retro-encode of the cosmic-coin probe)

**Seat:** `dial-sweep-00-retro-encode` (Fable, main loop). **No new measurement** — sweep 0 encodes the cosmic-coin probe's actually-measured grid (`../cosmic_coin_probe/`: harness + 3 re-measure agents + Opus adversary, all real JPL/NOAA data) as the first 18 trial records in `runs/dial-sweep-00.jsonl`, exercising the record format end-to-end. Every number traces to `results.json` / `FINDINGS.md` / the adversary scripts; family-level results where the probe retained only ranges (MA family, sub-window bands) are encoded as range-records, disclosed in-line.

**Pairs covered:** (mars-heliocentric-position, position-from-t0-state) and (goes18-xray-long, next-minute log-flux), plus the per-moment mixture `inferred` for both.

**Decomposition (probe §5 adversary table, re-read as protocol output):**
- **Engine band:** coder ladder ratio-of-CR 1.33–2.03× (never inverts); predictive family moves flare saved-frac 0.213→0.454 and deflates onset magnitudes ~26× (599→22.8 bits). Margin = render band ~1.17×–2.8×.
- **Frame observables:** window sub-splits (orbit 1.92–2.72, flare 1.09–1.23), channel swap (long 1.27 vs short 1.02), onset-removal (1.21 — killed the quieter-reads-sharp conjecture).
- **Interaction flags:** Student-t helps flare / hurts orbit (tail weight is structure of the framed thing) — `dial-mars-0004` × `dial-goes-0008`.
- **Dial-jumps:** none. Persistence holds as flare kernel candidate; `ar1-on-increments` (1.30 vs 1.27) flagged within-band, held for an out-of-sample re-trial before any jump.
- **Dead children inherited:** 6 (FINDINGS §7), encoded where they were trial-shaped (`dial-goes-0004/0005/0006`, the onset-magnitude demotion in 0008/0012 notes).

**NOT done (gated):** `tools/compile_dials.py` (the deterministic compiler), the viewer dial panel, the conjecture-engine seat — all await a Pav/Cowork nod on the spec. Opus skeptic pass on the SPEC itself + the GPT-5.5/Gemini external pass: owed.

**Proposed for sweep 1 (apply after a nod):**
- First live sweep: the S1 coupling pair (framed: LEO satellite orbit residuals × solar indices; inferred: does the joint compress better than the parts — the synergy gate on real sky data).
- Or the Q6 scale-rung sweep: same GOES flux at 1-min / 10-min / daily / monthly rungs — hardness-vs-rung as the first measured frame-relativity curve.
- Candidate registry seeding: regime-switching (HMM quiet/onset), ARFIMA, and a symmetric best-fair-predictive search for BOTH phenomena.

---
