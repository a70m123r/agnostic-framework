# Canonicalizer falsifier results — the semantic/lossless mismatch

Demonstrates the external pass's THIRD failure mode: verbatim verified-dissolve cannot tell a reworded concept (Paraphrase | Source) from new content (Distinct | Source). `paraphrase_discount` = 1 - cond(P|S)/cond(D|S); ~1 = recognised as redundant, ~0 = surface-bound.


## gzip — mean paraphrase_discount = **0.187**

| concept | cond(P\|S) bits | cond(D\|S) bits | discount |
|---|---|---|---|
| mito | 304.0 | 448.0 | 0.321 |
| boil | 360.0 | 368.0 | 0.022 |
| evo | 328.0 | 432.0 | 0.241 |
| supply | 400.0 | 424.0 | 0.057 |
| gravity | 344.0 | 488.0 | 0.295 |

## bz2 — mean paraphrase_discount = **0.128**

| concept | cond(P\|S) bits | cond(D\|S) bits | discount |
|---|---|---|---|
| mito | 368.0 | 496.0 | 0.258 |
| boil | 432.0 | 424.0 | -0.019 |
| evo | 384.0 | 464.0 | 0.172 |
| supply | 448.0 | 424.0 | -0.057 |
| gravity | 384.0 | 536.0 | 0.284 |

## lzma — mean paraphrase_discount = **0.203**

| concept | cond(P\|S) bits | cond(D\|S) bits | discount |
|---|---|---|---|
| mito | 384.0 | 576.0 | 0.333 |
| boil | 448.0 | 480.0 | 0.067 |
| evo | 384.0 | 576.0 | 0.333 |
| supply | 512.0 | 544.0 | 0.059 |
| gravity | 448.0 | 576.0 | 0.222 |

## verdict

- TRAP threshold = 0.45; surface-bound per coder: {'gzip': True, 'bz2': True, 'lzma': True}
- **classical coders surface-bound = True** — verbatim verified-dissolve rewards surface form, not the concept. This is the demonstrated third failure mode.
- FIX = the canonicalizer (`CANONICALIZER.md`): define `canon(W)` first, then measure `semantic_dissolve` (concept recovered, via the LLM coder cond up to paraphrase/entailment) + `residual_surface_bits` (the leftover wording variance) separately.
- VALIDATION (pending): wire the semantic LLM coder (P1 OpenAI-echo / P2 local) as a 4th provider — it should push `paraphrase_discount` HIGH while the classical coders stay low.
