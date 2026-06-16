#!/usr/bin/env python3
"""
Canonicalizer falsifier — demonstrates the THIRD failure mode the external pass
(codex GPT-5.5 + gemini, 2026-06-16) named for digestion-dynamics: the SEMANTIC/LOSSLESS
MISMATCH.

VERIFIED-DISSOLVE charges bits for EXACT (verbatim) reconstruction. For a target with no
canonical form (a concept, a claim), exact reconstruction rewards memorizing surface
wording, not the underlying concept. A mind that has fully dissolved the CONCEPT still
pays full bits for a paraphrase.

This test proves it with the same classical coders as latent_measure_tests.py, on a corpus
of (Source S, Paraphrase P = same concept reworded, Distinct D = different concept):

  cond(P|S) = bits to state the paraphrase GIVEN the source  (a semantic coder -> ~0)
  cond(D|S) = bits to state a distinct concept GIVEN the source

  paraphrase_discount = 1 - cond(P|S)/cond(D|S)   in [0,1]
     ~1  = the coder recognises P as redundant-given-S (it dissolved the concept)
     ~0  = the coder sees P as new content (it only saw surface form = the TRAP)

PREDICTION: classical (verbatim/LZ) coders show a SMALL discount = they cannot separate
"same concept reworded" from "new content" -> the verbatim gate is surface-bound. That gap
is exactly what the canonicalizer (semantic LLM coder, cond up to paraphrase/entailment
equivalence) is for. The LLM-coder provider is stubbed here; wiring it (P1/P2 in
LLM_CODER_SCOPING.md) is the validation: it should push the paraphrase_discount HIGH while
the classical coders stay low.

Stdlib only. Offline. Deterministic.
"""
import zlib, bz2, lzma
from pathlib import Path

PROVIDERS = {
    "gzip": lambda b: zlib.compress(b, 9),
    "bz2":  lambda b: bz2.compress(b, 9),
    "lzma": lambda b: lzma.compress(b, preset=9 | lzma.PRESET_EXTREME),
}
def C(prov, s):  return len(PROVIDERS[prov](s.encode("utf-8"))) * 8.0
def cond(prov, b, a):  return max(0.0, C(prov, a + b) - C(prov, a))   # NCD-style cond codelength

# (concept_id, Source, Paraphrase[same concept, reworded], Distinct[different concept, ~similar length])
CORPUS = [
    ("mito",
     "The mitochondrion is the powerhouse of the cell, producing ATP through respiration.",
     "Cells generate most of their ATP energy inside mitochondria via cellular respiration.",
     "The French Revolution began in 1789 when crowds in Paris stormed the Bastille fortress."),
    ("boil",
     "At sea-level atmospheric pressure, pure water boils at one hundred degrees Celsius.",
     "Water reaches its boiling point of 100 C when the pressure equals one atmosphere.",
     "A regular hexagon has six equal sides and six interior angles of one hundred twenty."),
    ("evo",
     "Natural selection favours heritable traits that raise an organism's reproductive success.",
     "Traits that are inherited and improve breeding success get favoured by natural selection.",
     "The speed of light in a vacuum is roughly three hundred thousand kilometres per second."),
    ("supply",
     "When demand rises and supply is fixed, the market-clearing price of a good goes up.",
     "A good's price climbs if buyers want more of it while the available quantity stays fixed.",
     "Chlorophyll absorbs red and blue light and reflects green, which is why leaves look green."),
    ("gravity",
     "Two masses attract with a force proportional to their product over the squared distance.",
     "The gravitational pull between two bodies grows with their masses and falls with distance squared.",
     "In 1969 Apollo 11 landed and Neil Armstrong became the first person to walk on the Moon."),
]

def paraphrase_discount(prov):
    """mean over concepts of 1 - cond(P|S)/cond(D|S); high = coder sees the paraphrase as redundant."""
    disc = []
    rows = []
    for cid, S, P, D in CORPUS:
        cps = cond(prov, P, S)
        cds = cond(prov, D, S)
        d = 1.0 - (cps / cds) if cds > 0 else 0.0
        disc.append(d)
        rows.append((cid, round(cps, 1), round(cds, 1), round(d, 3)))
    return sum(disc) / len(disc), rows

def main():
    print("=== canonicalizer falsifier: the semantic/lossless mismatch ===\n")
    results = {}
    lines = ["# Canonicalizer falsifier results — the semantic/lossless mismatch\n",
             "Demonstrates the external pass's THIRD failure mode: verbatim verified-dissolve cannot tell "
             "a reworded concept (Paraphrase | Source) from new content (Distinct | Source). "
             "`paraphrase_discount` = 1 - cond(P|S)/cond(D|S); ~1 = recognised as redundant, ~0 = surface-bound.\n"]
    for prov in PROVIDERS:
        mean_d, rows = paraphrase_discount(prov)
        results[prov] = mean_d
        print(f"[{prov}] mean paraphrase_discount = {mean_d:.3f}")
        lines.append(f"\n## {prov} — mean paraphrase_discount = **{mean_d:.3f}**\n")
        lines.append("| concept | cond(P\\|S) bits | cond(D\\|S) bits | discount |")
        lines.append("|---|---|---|---|")
        for cid, cps, cds, d in rows:
            lines.append(f"| {cid} | {cps} | {cds} | {d} |")
        for cid, cps, cds, d in rows:
            print(f"    {cid:8s} cond(P|S)={cps:7.1f}  cond(D|S)={cds:7.1f}  discount={d:+.3f}")

    # THE FALSIFIER: classical (verbatim) coders must show only a SMALL discount.
    # A semantic coder would push this high; the gap is the canonicalizer's job.
    TRAP = 0.45   # if classical coders discounted paraphrases like a semantic coder, this would be high (~0.8+)
    surface_bound = {p: d < TRAP for p, d in results.items()}
    all_surface_bound = all(surface_bound.values())
    print(f"\nsurface-bound (discount < {TRAP}) per coder: {surface_bound}")
    print(f"\nVERDICT: classical coders are surface-bound = {all_surface_bound}")
    print("  -> the verbatim verified-dissolve gate rewards surface form, not the concept.")
    print("  -> FIX (canonicalizer): define canon(W) first; measure semantic_dissolve + residual_surface_bits.")
    print("  -> the semantic LLM coder (P1/P2, LLM_CODER_SCOPING.md) should push paraphrase_discount HIGH.")

    lines.append(f"\n## verdict\n")
    lines.append(f"- TRAP threshold = {TRAP}; surface-bound per coder: {surface_bound}")
    lines.append(f"- **classical coders surface-bound = {all_surface_bound}** — verbatim verified-dissolve "
                 "rewards surface form, not the concept. This is the demonstrated third failure mode.")
    lines.append("- FIX = the canonicalizer (`CANONICALIZER.md`): define `canon(W)` first, then measure "
                 "`semantic_dissolve` (concept recovered, via the LLM coder cond up to paraphrase/entailment) "
                 "+ `residual_surface_bits` (the leftover wording variance) separately.")
    lines.append("- VALIDATION (pending): wire the semantic LLM coder (P1 OpenAI-echo / P2 local) as a 4th "
                 "provider — it should push `paraphrase_discount` HIGH while the classical coders stay low.")
    (Path(__file__).resolve().parent / "CANONICALIZER_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # exit 0 when the trap is demonstrated (classical coders surface-bound, as predicted)
    import sys
    sys.exit(0 if all_surface_bound else 1)

if __name__ == "__main__":
    main()
