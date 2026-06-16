# The Canonicalizer — semantic verified-dissolve (spec)

**Date:** 2026-06-16 | **Status:** Tier-3 design. The "one missing piece" the external pass (codex GPT-5.5 + gemini) named for [DIGESTION_DYNAMICS.md](DIGESTION_DYNAMICS.md) (§11.6) and the semantic upgrade of [LLM_CODER_SCOPING.md](LLM_CODER_SCOPING.md). The failure mode it fixes is **demonstrated** (`tests/canonicalizer_tests.py`, run 2026-06-16); the fix itself is **specced, not yet validated** (needs the LLM coder).

---

## 0. The problem (demonstrated, not assumed)

`VERIFIED-DISSOLVE` discounts bits only if a derivation **exactly** (verbatim) reconstructs the target. For a target with **no canonical form** - a concept, a claim, an idea-wrapper (i.e. most latent entities) - exact reconstruction **rewards memorizing surface wording, not the concept.** A mind that has fully dissolved the *concept* still pays full bits for a paraphrase.

**Falsifier result** (`tests/canonicalizer_tests.py`, classical LZ coders on 5 concept-triples Source / Paraphrase / Distinct):

| coder | mean paraphrase_discount = 1 - cond(P\|S)/cond(D\|S) |
|---|---|
| gzip | 0.187 |
| bz2  | 0.128 (NEGATIVE on 2 concepts) |
| lzma | 0.203 |

A semantic coder would score ~0.8+ (it sees the paraphrase as redundant-given-the-source). Classical/verbatim coders score ~0.15 - **surface-bound**: a reworded fact costs about as much as (bz2: *more* than) a completely different fact, because there is no verbatim overlap. The verbatim gate cannot tell "same concept, reworded" from "new content." That gap is the canonicalizer's job.

---

## 1. The fix - split the measurement in two

Define an **equivalence class / canonical form `canon(W)`** for the target FIRST, then measure two separated quantities:

```
measured_bits(W) = semantic_dissolve( canon(W) )   +   residual_surface_bits(W)
                   \___ the CONCEPT (what hardness means) ___/   \___ incidental wording ___/
```

- **`canon(W)`** = the concept stripped of incidental surface form. Defined **operationally** by the semantic coder (no hand-canonicalization): two targets A, B are in the same class iff each is ~free given the other -
  `cond_LLM(A | B) ~ 0  AND  cond_LLM(B | A) ~ 0` (symmetric, both directions, under the pinned LLM coder = paraphrase/entailment equivalence).
- **`semantic_dissolve(canon(W))`** = the conditional codelength of the *concept* given the mind's program, under the LLM coder (`cond` up to the equivalence class). **This is the residue that means hardness** - it is what reasoning dissolves (the slow-digestion target). A paraphrase the mind already knows -> ~0.
- **`residual_surface_bits(W)`** = `cost(W) - cost(canon(W))` = the wording/format variance NOT determined by the concept. **Incidental, aleatoric-flavoured** (ties to §11.2's aleatoric floor) - reported SEPARATELY, never counted as concept hardness.

So digestion measures the **concept** dissolving; the surface bits are a held-out, honestly-labelled side-channel.

---

## 2. The honesty gate lifts from verbatim to semantic (still one-sided)

VERIFIED-DISSOLVE generalizes from "exactly reconstructs W" to **"reconstructs W up to the VERIFIED equivalence class":**

```
semantic_dissolved_bits(W) = (cost - residue)  IF  reconstruct(program) ~=_canon W   (verified equivalence)
                           = 0  (back off to the literal cost)   otherwise
```

The equivalence `~=_canon` is itself **checked**, not asserted (the Goodhart guard, gemini): a claimed equivalence must satisfy **symmetric near-zero conditional both ways** AND must **fail** on a distinct concept (the falsifier's Distinct pairs are the standing negative control). A canonicalizer that maps everything to one class is caught because it would wrongly equate Distinct pairs (their discount must stay LOW). No "everything is equivalent" lookup-table escape.

This keeps the slow regime one-sided: a strong mind cannot fake-dissolve by *rewording* - it must recover the concept's equivalence class, verified.

---

## 3. The coder (why classical can't, LLM can)

Classical coders see only verbatim overlap (proven surface-bound above). The **LLM coder** gives `cond` up to paraphrase/entailment because next-token probability conditions on *meaning*: a paraphrase of the prior context is high-probability -> low codelength. This is the syntactic->semantic upgrade `LLM_CODER_SCOPING.md` scoped. Paths unchanged: **P1** OpenAI Completions echo+logprobs (immediate, small spend + external call), **P2** local transformers+gpt2 (free/offline, ~GB install). The coder is pinned + disclosed (the pinned relational bit), so `canon` is relative to a declared decoder - which is the whole framework's honest standard, not a flaw.

---

## 4. Validation (the pending step - needs the LLM coder)

Re-run `tests/canonicalizer_tests.py` with the LLM coder added as a 4th provider. **Pass conditions:**
1. **Paraphrase recognised:** `paraphrase_discount` goes HIGH (>~0.7) under the LLM coder - it discounts the reworded concept the classical coders couldn't.
2. **Negative control holds:** Distinct pairs stay LOW (`cond_LLM(D|S)` not discounted) - the canonicalizer isn't collapsing everything.
3. **Entailment, not just paraphrase:** add an *entailed* target (a logical consequence of S) - the LLM coder should partially discount it (it's derivable), the classical coders shouldn't.
4. **Surface split is stable:** `residual_surface_bits` for two paraphrases of one concept should be comparable and small relative to `semantic_dissolve` for a genuinely hard concept.

Pass -> the digestion unit measures **concepts**, not surface form, and `measured_bits` is semantic. This also retires the `LLM_CODER_SCOPING.md` "honest but syntactic" caveat.

---

## 5. What it changes / where it sits

- Upgrades `measured_bits = min(cost_ub, evidence_lcb)`: `cost_ub` becomes a **semantic** codelength (cond up to `canon`), with `residual_surface_bits` split off and labelled - so the validated static unit keeps its honesty discipline while measuring meaning.
- Closes DIGESTION_DYNAMICS §11.6's third failure mode: the resistance-curve now reads against semantic reconstruction, not verbatim - so "overthinking" that only reworders earns no discount, and a concept a mind truly knows melts even when worded differently.
- The equivalence class is the **WHAT-axis canon** the keyhole/wrapper layer wanted: `canon(W)` is the concept-node; surface forms are its renderings. (Connects [[project_hyperspace_viewer_spec]] WRAPPER/PROBE/OBSERVER.)
- Honest scope limit until validated: the verbatim gate is sound ONLY for already-canonical targets (code, sequences, formal logic); for concepts/claims it is surface-bound (proven) until the LLM-coder canonicalizer is wired and §4 passes.

---

## 6. Open question for Pav

The canonicalizer makes `canon(W)` decoder-relative (the LLM coder defines the equivalence class). Do you want **one pinned canon-coder** as the standard (a single declared "meaning decoder"), or `canon` as **another dial** on the observer-glass (each observer/epoch carries its own equivalence relation - a 1789 mind and a 2026 mind canonicalize differently, which is the definition-drift layer made operational)? The second is more powerful and more honest to the frame-relative thesis, but multiplies the pinned-relational-bit bookkeeping.
