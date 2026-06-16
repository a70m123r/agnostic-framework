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

## 3. Two instruments, not one (corrected 2026-06-16 by the P1 test - demote-not-kill)

The original hope - that one LLM-codelength coder does both the bits AND the equivalence - was **tested and falsified** (`tests/canonicalizer_validate_p1.py`, `CANONICALIZER_P1_RESULTS.md`). Codelength and semantic-equivalence are **different measurements needing different instruments:**

- **`residual_surface_bits` <- CODELENGTH** (the bits instrument). LLM echo+logprobs gives codelength (input logprobs = arithmetic-coding bits). Right tool for the cost/bits side.
- **`canon(W)` / the `~=_canon` relation <- a MEANING instrument** (embedding cosine, or NLI entailment). Codelength FAILS at equivalence: a paraphrase uses different tokens, so prefix-conditioning - even paraphrase-primed - doesn't make it cheap (mean discount -0.10 naive / +0.09 primed on davinci-002, no clean separation), AND the only OpenAI models exposing echo+logprobs are weak base models (instruct models reject `echo`+`logprobs`, HTTP 400). **Embeddings separate paraphrase from distinct cleanly** (sec 4), so the equivalence is an embedding/NLI judgement, not a codelength one.

The lesson: don't ask the bits-coder to also be the meaning-comparator. Both instruments are pinned + disclosed (the relational-bit discipline is unchanged).

---

## 4. Validation result (2026-06-16, P1 OpenAI on the synthetic corpus)

`tests/canonicalizer_validate_p1.py` -> `CANONICALIZER_P1_RESULTS.md`:

| instrument | mean(paraphrase) | mean(distinct) | separation | verdict |
|---|---|---|---|---|
| classical LZ (gzip/bz2/lzma) | discount 0.13-0.20 | - | - | surface-bound (the trap) |
| echo-codelength (davinci-002, primed) | discount +0.09 | - | - | **NOT validated** (codelength is the wrong instrument; base models weak, instruct reject echo) |
| **embedding cosine (text-embedding-3-small)** | **cos 0.684** | **cos 0.062** | **0.622** | **VALIDATED** (clean across all 5 concepts) |

The canon equivalence relation **is real and cleanly detectable** - by a meaning instrument, not a bits instrument. The negative control holds (distinct cosine ~0.06, not collapsed). The honest dead-child: "one LLM-codelength coder does semantic equivalence too." The corrected mechanism: `~=_canon` via embedding cosine (threshold-gated, symmetric, distinct-must-fail) + codelength for `residual_surface_bits`.

**Still to wire into the live unit:** the embedding gate as `~=_canon`; an NLI entailment check for the asymmetric (derivable, not just reworded) case; and the per-instance fold into `measured_bits = min(cost_ub, evidence_lcb)` so the digestion unit measures **concepts**, not surface form. That retires the `LLM_CODER_SCOPING.md` "honest but syntactic" caveat on the equivalence side.

---

## 5. What it changes / where it sits

- Upgrades `measured_bits = min(cost_ub, evidence_lcb)`: `cost_ub` becomes a **semantic** codelength (cond up to `canon`), with `residual_surface_bits` split off and labelled - so the validated static unit keeps its honesty discipline while measuring meaning.
- Closes DIGESTION_DYNAMICS §11.6's third failure mode: the resistance-curve now reads against semantic reconstruction, not verbatim - so "overthinking" that only reworders earns no discount, and a concept a mind truly knows melts even when worded differently.
- The equivalence class is the **WHAT-axis canon** the keyhole/wrapper layer wanted: `canon(W)` is the concept-node; surface forms are its renderings. (Connects [[project_hyperspace_viewer_spec]] WRAPPER/PROBE/OBSERVER.)
- Honest scope limit until validated: the verbatim gate is sound ONLY for already-canonical targets (code, sequences, formal logic); for concepts/claims it is surface-bound (proven) until the LLM-coder canonicalizer is wired and §4 passes.

---

## 6. Open question for Pav

The canonicalizer makes `canon(W)` decoder-relative (the LLM coder defines the equivalence class). Do you want **one pinned canon-coder** as the standard (a single declared "meaning decoder"), or `canon` as **another dial** on the observer-glass (each observer/epoch carries its own equivalence relation - a 1789 mind and a 2026 mind canonicalize differently, which is the definition-drift layer made operational)? The second is more powerful and more honest to the frame-relative thesis, but multiplies the pinned-relational-bit bookkeeping.
