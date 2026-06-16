# External pass — codex (GPT-5.5) + gemini, 2026-06-16

Two non-Claude models, run from the CLI on `external_brief.txt` + `ARC_DIGEST.md` + `DIGESTION_DYNAMICS.md`. They **converged** — the standing cross-model A- ([[feedback_cross_model_external_pass]]). Demote-not-kill: nothing is killed; the spec + the method survive with named corrections. Raw: `codex_arc_review.md`, `gemini_arc_review.md`.

## Q1 — the digestion-dynamics harden

**Verdict (both): the framing holds and is the field's convergent direction; cite don't coin; the novelty is a *synthesis*, not new math.**

**Citations — corrected + extended** (codex web-verified every ID):
- Confirmed: KT **2503.13992**; PVI Xu **2002.10689** + Ethayarajh **2110.08420**; epiplexity **2601.03220**; EDL **2601.04728**.
- **Fix: LMIC = arXiv:2309.10668** (Deletang et al.; not an ICLR-proceedings link).
- **Missing load-bearing prior art to add:** test-time-compute/allocation — Snell et al. **2408.03314**, s1 budget-forcing **2501.19393**, overthinking/length-confound **2412.21187** + **2502.07266** + **2604.10739**; verifier/search priors our novelty leans on — AlphaCode **2203.07814**, Tree-of-Thoughts **2305.10601**, self-consistency **2203.11171**, process-supervision/verification **2305.20050**, RoundTripCodeEval **2601.13398**; Hutter prize (compression=AGI) for the framing flank.

**Over-claim flagged:** "residue **==** epiplexity / time-bounded entropy" is too tight — epiplexity is closer to *useful bounded structural content*; the random/unpredictable floor must stay **separate**. This **reinforces §11.2 fix #1** (the aleatoric/epistemic split): relabel as "relates to / per-instance verified epiplexity," floor held out.

**The THIRD failure mode (both, independently) — the semantic/lossless mismatch.** The verified-dissolve gate demands *exact* reconstruction. For anything without a canonical representation (concepts, claims, narratives), bit-for-bit reconstruction **rewards memorizing surface syntax / incidental wording** — you measure the cost of human variance, not the algorithmic complexity of the concept (gemini also: Goodhart/lookup-table risk). **Fix:** define an **equivalence class / canonicalizer** for the target first, then measure **semantic dissolve + residual surface bits** separately. (This is exactly where the semantic LLM-coder from `LLM_CODER_SCOPING.md` earns its place — reconstruct up to entailment/paraphrase equivalence, not verbatim.)

**Novelty — demoted to synthesis/hypothesis.** KT already owns "short program + exact reconstruction"; verifier-guided-TTC-search ≈ execution-based program synthesis (AlphaCode/AlphaGeometry; codex+gemini). The conjugate-trace ≈ Levin search + training-loss/EDL curves repackaged. **The defensible-novel claim is only the *unified observer-indexed trace+residue law* (trace as the conjugate dual of the residue) — flag it a synthesis, not established new math.**

## Q2 — the self-capture method

**Verdict (codex): "trustworthy as a navigable, COIN-capped provenance record; NOT trustworthy as truth unless each arc's specific claims are hash/time/content verified."** (gemini: "innovative high-signal structural log, but not epistemically trustworthy" as-is.)

**Systematic risks to guard (both):**
1. **Narrative-smoothing** — the stitch invents causal connective tissue between coincidental acts (LLMs abhor a vacuum). The narrative is the most-exposed surface.
2. **Anachronism** — verifying a past act against the *final* disk state (`t_obs`) lets a later edit falsely corroborate an earlier `t_event`. The bitemporal split records this but the verify pass doesn't honour it.
3. **Overlap dedup** can merge two distinct acts or split one.
4. **Omission bias** — the verifier only checks what the agents extracted; dropped transcript regions, failed branches, absent artifacts never become "fake bits."
5. **Evidence laundering** — a memory file repeating a claim is corroboration-by-the-same-author, not independent support (several arcs verified against memory notes — count those as testimony, not evidence).
6. **Rubber-stamping / file-existence ≠ claim-content** — `verify.jsonl` is partly content-aware (good — it caught 10 over-claims), but it is still LLM judgment, prone to keyword-match "corroborated."
7. **Runtime / branch / push / model-version / browser-state claims need hashes/logs/screenshots, not prose** (this is exactly why `commit-push` is `unverifiable` and `infra-housekeeping` is flagged).
8. **Self-capture bias** — the same model family extracts, stitches, narrates, AND verifies. The cross-model external pass (this doc) is the only outside check.

**The good sign (both):** the 4452-vs-3073 catch proves the method can falsify itself — but also proves **counts/scopes need machine-checked invariants**, not LLM extraction.

## What changes (the to-dos this pass earns)

- DIGESTION_DYNAMICS §11: fold the citation fixes + the **third failure mode (canonicalizer/semantic-dissolve)** + the **novelty demotion** → done as §11.6.
- The capture: treat memory-only corroboration as **testimony** (cap certainty), add **machine-checked count invariants**, and honour `t_event` (verify as-of-event) before this is called history rather than an index.
- Keep it as what it is: a **COIN-capped navigable provenance record** — which is exactly what it was built to be, and what it honestly renders itself as.
