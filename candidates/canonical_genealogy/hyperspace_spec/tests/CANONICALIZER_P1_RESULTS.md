# Canonicalizer P1 validation — OpenAI coder (run 2026-06-16, synthetic corpus)

## A. echo-CODELENGTH (model `davinci-002`) — the bits instrument

Input logprobs = codelength; `cond(b|a)=cost(a+b)-cost(a)`. NAIVE prefix vs PRIMED (restate-S).

| concept | naive cond(P\|S) | naive cond(D\|S) | primed cond(P\|S) | primed cond(D\|S) |
|---|---|---|---|---|
| mito | 60.0 | 70.3 | 42.0 | 49.0 |
| boil | 55.1 | 64.4 | 30.8 | 49.2 |
| evo | 69.2 | 56.4 | 45.7 | 41.1 |
| supply | 80.2 | 49.7 | 58.7 | 47.1 |
| gravity | 59.1 | 59.3 | 42.2 | 61.0 |

- naive mean paraphrase_discount = **-0.109** ; primed = **0.093** (classical: gzip 0.187, bz2 0.128, lzma 0.203)
- **NOT validated by codelength** — base models (only ones exposing echo+logprobs) too weak/noisy; instruct models reject `echo`+`logprobs` (400). Codelength is the right tool for the BITS side, not the equivalence side.

## B. EMBEDDINGS cosine (text-embedding-3-small) — the canon/equivalence instrument

| concept | cos(P,S) | cos(D,S) | separation |
|---|---|---|---|
| mito | 0.618 | 0.026 | 0.592 |
| boil | 0.784 | 0.137 | 0.647 |
| evo | 0.713 | 0.026 | 0.687 |
| supply | 0.637 | 0.097 | 0.54 |
| gravity | 0.668 | 0.025 | 0.644 |

- mean cos(paraphrase,S) = **0.684** ; mean cos(distinct,S) = **0.062** ; separation = **0.622**
- **VALIDATED** — the canon equivalence relation IS real and cleanly detectable via embeddings (paraphrase near-S, distinct far). The two-instrument split: codelength for `residual_surface_bits`, embeddings/NLI for `canon(W)`.
