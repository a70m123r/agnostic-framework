**(1) Digestion Dynamics**

Citation map: directionally right, not complete, and a few identities are too strong.

- Correct anchors: KT / exact reconstruction: The KoLMogorov Test [arXiv:2503.13992](https://arxiv.org/abs/2503.13992); LMIC: [arXiv:2309.10668](https://arxiv.org/abs/2309.10668); PVI: Xu [arXiv:2002.10689](https://arxiv.org/abs/2002.10689), Ethayarajh [arXiv:2110.08420](https://arxiv.org/abs/2110.08420); epiplexity: [arXiv:2601.03220](https://arxiv.org/abs/2601.03220); EDL: [arXiv:2601.04728](https://arxiv.org/abs/2601.04728).
- Over-claim: “residue == epiplexity / time-bounded entropy” is too loose. Epiplexity is closer to useful bounded structural content; random/unpredictable floor must stay separate.
- Missing load-bearing line: test-time search/allocation literature: Snell et al. [arXiv:2408.03314](https://arxiv.org/abs/2408.03314), `s1` budget forcing [arXiv:2501.19393](https://arxiv.org/abs/2501.19393), overthinking/length confounds [arXiv:2412.21187](https://arxiv.org/abs/2412.21187), [arXiv:2502.07266](https://arxiv.org/abs/2502.07266), [arXiv:2604.10739](https://arxiv.org/abs/2604.10739). Also cite verifier/search priors: AlphaCode [arXiv:2203.07814](https://arxiv.org/abs/2203.07814), Tree-of-Thoughts [arXiv:2305.10601](https://arxiv.org/abs/2305.10601), self-consistency [arXiv:2203.11171](https://arxiv.org/abs/2203.11171), process verification [arXiv:2305.20050](https://arxiv.org/abs/2305.20050), RTCE [arXiv:2601.13398](https://arxiv.org/abs/2601.13398).
- The two fixes are necessary, not sufficient. Third failure mode: **semantic/lossless mismatch**. Exact reconstruction measures surface form unless the target has a canonical representation. For concepts, claims, narratives, etc., bit-for-bit reconstruction rewards memorizing syntax and incidental wording. Fix: define equivalence class/canonicalizer first, then measure semantic dissolve plus residual surface bits.
- Novelty: modest. KT already owns “short program + exact reconstruction.” Verifier-guided TTC search is close to program synthesis/search. The likely novel part is the **unified observer-indexed trace+residue law**, but call it a synthesis/hypothesis, not established new math.

**(2) Self-Capture**

Soundness: good as a provenance-bearing index; not sound as canonical history without per-claim audit.

Systematic risks:

- Stitch can invent causal connective tissue.
- Overlap dedup can merge distinct acts or split one act.
- Verification against final disk state creates anachronism: `t_obs` can falsely corroborate `t_event`.
- Artifact existence is insufficient; your `verify.jsonl` is partly content-aware, which is good, but still LLM/manual judgment.
- Omission bias: dropped transcript regions, failed branches, tool noise, and absent artifacts never become “fake bits.”
- Evidence laundering: memory files may repeat the claim rather than independently support it.
- Runtime claims, branch/push claims, model-version claims, and browser-state claims need hashes/logs/screenshots, not prose.
- Self-capture bias: same system family extracts, stitches, narrates, verifies.

The 4452 vs 3073 catch is a good sign: the method can falsify itself. But it also proves counts/scopes need machine-checked invariants.

One-line verdict: **trustworthy as a navigable, COIN-capped provenance record; not trustworthy as truth unless each arc’s specific claims are hash/time/content verified.**
