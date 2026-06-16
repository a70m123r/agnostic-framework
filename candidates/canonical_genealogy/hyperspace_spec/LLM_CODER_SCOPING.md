# LLM-coder for latent measured_bits - scoping (2026-06-15)

**Goal.** Replace the classical coders (gzip / lzma) in the validated unit `measured_bits = min(cost_ub, evidence_lcb)` with an **LLM-as-coder**, so `cost_ub` and the conditional `cond(new | existing)` capture **semantic** content - paraphrase, implication, entailment - which classical compressors miss (they only see *verbatim* overlap). This is what turns the unit from an honest *syntactic* measurement into an honest *semantic* one.

**The codelength is exact and well-defined.** For a pinned LLM `M`:
```
cost_ub(W)        = Sum_t  -log2 P_M(token_t | prefix_<t, frame)   # teacher-forced per-token NLL = arithmetic-coding codelength
cond(W | context) = Sum_t  -log2 P_M(token_t | context, prefix_<t) # same, with the context prepended
```
This is a sound one-sided upper bound on K (a worse model only spends more bits), and it is the *same bit unit* as the classical and physical coders - so it drops into the existing prototype as a 4th "provider."

## Tooling available here (checked)

| tool | status | use for the coder |
|---|---|---|
| transformers / torch | **absent** | local logit access (clean per-token NLL) - would need install |
| llama_cpp (python) | absent | local NLL via llama.cpp |
| openai (SDK) | absent | not required - raw HTTP works |
| tiktoken | absent | (only needed for token accounting) |
| **ollama** | **present** (`D:\Ollama\ollama.exe`) | local GGUF runtime; per-token *input* logprob support is version-dependent / uncertain |
| **OPENAI_API_KEY** | **set** | the readily-available path (below) |
| ANTHROPIC_API_KEY | unset | Anthropic exposes no logprobs regardless |
| numpy | present | stats |

## Feasible paths, ranked

1. **OpenAI Completions API with `echo` + `logprobs`** *(immediately available via the set key).*
   `POST /v1/completions` to a base/instruct model (`babbage-002` / `davinci-002` / `gpt-3.5-turbo-instruct`) with `echo=true, logprobs=1, max_tokens=0` returns the per-token logprobs of the **input** text = exact codelength. Call via raw `urllib`/HTTP (no SDK needed). **Cost:** spends Pav's key per call and **sends the corpus to OpenAI (an external call)** - fine for the *synthetic* test corpus, needs an explicit OK for anything real.
2. **Local `transformers` + a tiny model (gpt2 / distilgpt2)** *(cost-free, offline, repeatable).*
   Exact per-token NLL in a few lines; the cleanest long-term coder. **Needs** `pip install transformers torch` (~GB) + the model (~500 MB) -> feasibility = network for the install.
3. **llama.cpp perplexity / ollama** *(local, uncertain).*
   `llama.cpp`'s perplexity tool computes `Sum -log p` = codelength directly; ollama (present) runs GGUF models but its API's teacher-forced input-logprob support is version-dependent. Riskier; verify before relying on it.

**Recommendation.** Path 2 (local `transformers`+gpt2) for a free, offline, repeatable semantic coder *if* the install works here; otherwise Path 1 (OpenAI echo+logprobs) for an immediate validation on Pav's OK (small spend, synthetic data only).

## The validation it unlocks (the ultimate coder-swap)

Re-run the SAME five falsifiers (A-E in `tests/latent_measure_tests.py`) with the LLM coder added as a 4th provider. Two things the LLM coder should show that the classical coders **cannot**:
- **(i) Semantic redundancy.** A **paraphrase** of a stone (no verbatim overlap) should compress to ~0 conditional bits under the LLM = correctly flagged *deadweight*, where gzip/lzma see it as brand-new content. This is the gap the prototype had to paper over by making "deadweight" verbatim.
- **(ii) Implication / entailment.** A fact logically implied by others should carry low conditional bits. Add a paraphrase-stone and an entailed-stone to the corpus and check the LLM coder discounts them while the classical coders don't.

**Pass condition:** the LLM coder **agrees** with gzip/lzma on the existing verdicts (lie blurred, evidence discriminates, deadweight separates, amnesia-drop lossless) **and additionally** catches paraphrase/entailment redundancy. That would validate the unit as a *semantic* measurement, not just a syntactic one.

## Honest gap

The prototype (`tests/latent_measure_tests.py`, 14/15, coder-robust) validated the **mechanism** - one-sided cost, evidence-discounting, redundancy -> 0, the lie-blur, lossless amnesia-drop - with **classical** coders on a **synthetic** corpus. Until the LLM coder is wired in and the paraphrase/entailment tests pass, the unit is **honest but syntactic**. The LLM coder is the single remaining step to a semantic latent `measured_bits`; the path is clear and the key is present, gated only on the API-spend / external-call OK (Path 1) or a `transformers` install (Path 2).
