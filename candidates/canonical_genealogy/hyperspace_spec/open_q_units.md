# Units: the latent measured_bits, the ladder radix, and the civilisation ceiling

Synthesis for the SPEC-ONLY hyperdimensional canonical-space viewer.

Resolves three open unit questions against the keystone (one logarithm does
three jobs) and the COIN law (`rendered_bits(x) <= measured_bits(x)`; blur is
the honesty badge; never render a fake measured bit).

- **Q1** the canonical UNIT of `measured_bits` on the latent axis
- **Q2** the branching RADIX per axis (depth / path-ID width / LCA cost)
- **Q4** the latent ceiling N (fixed vs open-ended; how to normalise a zoom
  window with no fixed maximum)

Scope of the latent axis: TOTAL CIVILISATION -> a SINGLE WORD. Scope of the
physical axis: UNIVERSE -> PLANCK (~205-206 bits in log2 metres). The two are
fibrations over one shared base poset.

---

## 0. The one constraint all three answers must satisfy

Every unit decision is downstream of a single inequality that must hold at every
node, every frame, on both fibrations:

```
rendered_bits(x | ancestry) <= measured_bits(x | ancestry)
```

For this to be meaningful and ungameable, `measured_bits` must be:

1. **One-sided** -- a true UPPER bound on the content of `x`, so blur can only
   ever be honest (it can over-state cost, never under-state it).
2. **Per-node and conditional** -- defined given the ancestry already
   transmitted, so the chain rule is additive: `anchor_bits + window_bits =
   path_bits`, byte-for-byte.
3. **Computable** under a pinned, disclosed coder.
4. **The same functional on both halves**, so "appearance = 2^-bits = Solomonoff
   p = render-in-log2" stays one coherent unit across the metres ladder and the
   word axis.

These four requirements are what disqualify the seductive-but-unsound candidates
below, and what force the radix and ceiling answers into a specific shape.

---

## Q1 -- The canonical UNIT of latent measured_bits

### 1.1 The unit (one line)

```
measured_bits_latent(x; coder C, fidelity tau)
    = min( prequential_codelength_C(x at tau),  KT_literal_bits(x) )
```

In words: the **prequential (online) next-token codelength**, in bits, that a
single PINNED coder C spends to *losslessly* transmit a reconstruction of
concept `x` at or above fidelity threshold `tau`, computed in one online pass and
**hard-capped by the KoLMogorov-Test back-off** to the entropy-coded literal.

This is the exact latent twin of the settled physical unit (EntropyGS / PCGS /
SPZ "entropy-coded size at a quantization/quality floor"). In both halves
`measured_bits` is the same thing: *the number of bits an honest, lossless,
disclosed coder actually pays to reproduce the thing to a stated fidelity.*

### 1.2 Why prequential codelength, and why it is a SOUND upper bound

A prequential code transmits the data without transmitting the model weights:

```
L_C(x) = sum_i  -log2 p_C(token_i | token_<i, context)
```

Because `L_C(x)` is an *actual lossless code* for `x`, by Kraft/Shannon it is
`>=` the Shannon-optimal codelength of the source and, for the individual object,
`>= K(x) - O(1)`. It can therefore only OVER-state, never under-state, true
content. That one-sidedness is precisely what the COIN needs: `measured_bits` is
a valid ceiling, so `rendered_bits = min(measured_bits, lod_budget(zoom))` can
never claim structure that was not paid for. This is the same NLL machinery the
physical harness already runs -- the strongest no-fake-bit guarantee on offer.

Prequential coding is the right realization (over, e.g., two-part MDL) because it
encodes the data without paying for the weights, converges blockwise on the MDL
objective, and gives tight high-probability Occam bounds
(Prada et al. 2025, arXiv 2505.14635; Shaw et al. Sep 2025).

### 1.3 Why the KT gate is not optional -- soundness is a PROTOCOL, not a number

The upper-bound guarantee holds **only if the reconstruction is actually
checked.** The KoLMogorov Test (KT, ICLR 2025, arXiv 2503.13992) supplies the
gate: emit the shortest program `rho` reproducing `x`, EXECUTE it to verify
`[[rho]] = x` exactly, and if the program errs or exceeds the literal, BACK OFF
to the literal:

```
y = rho        if [[rho]] = x
y = x          otherwise
reported_bits = 1 + ||y||_enc          (rate never exceeds 1.0)
```

KT "does not produce false positives" -- it structurally cannot leak a fake bit.
That literal cap is the latent analogue of Landauer's `>= kT ln2` real-bit floor
on the physical side: no clever coder can fabricate compression it cannot cash
out by actual reconstruction.

**Rule (load-bearing):** any latent `measured_bits` that is *displayed as
structure* must be checkable by reconstruction and capped at the literal.
Caption-based or embedding-based shortcuts (CCDA captions, semantic entropy) that
SKIP reconstruction silently UNDER-count and would leak fake bits. They are
hints, not the unit.

### 1.4 Fidelity tau is part of the unit -- the canonical object is a CURVE

The right latent quantity is not a scalar but the **Kolmogorov structure
function** `h_x(alpha)` / CCDA codelength-vs-fidelity **curve** `measured_bits(tau)`.
Its kink

```
k* = Algorithmic Minimum Sufficient Statistic
```

marks "stop here, beyond is noise" -- this is the COIN's "never render past
measured structure" on the latent axis. **k\* is the latent Planck floor:** the
"single word" stop, the place you must not zoom past. (Epiplexity, Finzi et al.
Jan 2026 arXiv 2601.03220, is *not* adopted as the per-node unit -- it is not a
sound per-item upper bound and is harder to compute -- but it is adopted as the
principled *interpretation* of k\*: halt at the kink rather than coding
incompressible noise.)

### 1.5 The three-layer stack (one law)

| Layer | Role | What it is | Wired to |
|-------|------|-----------|----------|
| **L1 SOUND** | the cap / authority | prequential/online NLL codelength, KT-gated | the committed/displayed `measured_bits` |
| **L2 FAST** | the dial | KARL min-tokens-at-tau, single forward pass | `lod_budget(zoom)` (interactivity) |
| **L3 DISCRETE** | the quantizer | Matryoshka prefix length | integer path-ID nesting-coordinate (one prefix step ~ one octave ~ one bit) |

All three are unified by the structure-function curve and capped by the KT gate.

### 1.6 The disqualification that the digest's own WINNER line got wrong

The prior-art TAKEAWAYS crowned **KARL min-tokens** as the WINNER for the unit.
That contradicts the same section's CAUTION line and must be corrected:

> **KARL is the DIAL, never the CAP.**

KARL (arXiv 2507.07995) is a *learned, unverified* predictor. The paper itself
disclaims minimality guarantees ("no guarantees of true minimality"); it never
executes a reconstruction to check. So its count is an ESTIMATE of complexity,
not an UPPER bound on content. Wiring an estimate into the cap **inverts the
COIN**: if KARL predicts 40 tokens but faithful reconstruction needs 80, the
renderer is licensed to sharpen to 40-tokens'-worth of crispness on content that
is actually 80-tokens deep -- a fake measured bit, silently. KARL cannot pass the
KT execute-verify-or-back-off gate, so it is disqualified as the cap and demoted
to driving `lod_budget(zoom)` only. **L2 proposes; L1 disposes.**

Also rejected as the per-node unit (kept only as global scale-ladder hints):
intrinsic-dimension / effective-rank (measures manifold dimensionality, not
per-item codelength; low-ID manifolds can hold high-K points -- not a sound
per-item upper bound) and semantic entropy (measures answer-distribution
uncertainty, not description length).

### 1.7 Composition with the physical unit (the chain-rule COIN)

Because both units are now the *same functional* -- entropy-coded lossless bits
to reproduce `x` to a disclosed fidelity under a disclosed coder -- they share
one base poset and one chain rule:

```
measured_bits(x | ancestry) = L_C(x | parent-context)
                            = prequential codelength of x given ancestors sent
```

- **Physical:** bits-per-splat given the parent octree node already streamed
  (PCGS/EntropyGS conditioned on coarser LOD).
- **Latent:** conditional next-token NLL of the concept given its parent
  concept's tokens already sent.

Identical arithmetic on two fibrations over one base; one bit = one octave on
both. This is the same fact Hilbert & Lopez (2011) used ("optimally compressed
bits") and the same arithmetic-coding/MDL idea the 2024-26 LLM-compression
papers use, so the keystone's third job (sharpness = 2^-bits = Solomonoff p)
holds verbatim on the latent axis: `appearance = 2^-measured_bits` is literally
the coder's per-concept probability mass.

### 1.8 Caveat carried from the physical work: the latent axis is MORE coder-relative

`K(x)` is defined only up to an additive constant; prequential codelength
inherits the full coder/tokenizer choice. Two coders can disagree by hundreds of
bits on the same concept, and as you zoom, the conditioning prefix grows, so the
same concept's bit-count shifts with context -- `measured_bits` is a property of
`node x decoder x prefix`, not of the node alone. The physical axis does not have
this problem (metres are decoder-free). Mitigations, all disclosed:

- **Pin and disclose the coder** (which LLM, tokenizer, quantization, tau) per
  atlas, exactly as the physical harness pins its coder; freeze the conditioning
  context per atlas.
- **Cross-model re-measurement** (GPT-5.x + Gemini) of any load-bearing latent
  bit-count is the real external A-minus. If two decoders disagree on a node by
  more than the rung size, the node renders at the MAX (blurriest) of the two
  caps -- max preserves the upper-bound guarantee.
- **Peg the conventional zero**: "0 bits = a single word/token" at the fine end;
  let the coarse end re-anchor (see Q4).

---

## Q2 -- The branching RADIX per axis

### 2.1 The decision

| Fibration | Radix | bits/level | Rationale |
|-----------|-------|-----------|-----------|
| **Physical (3D)** | radix-2 per axis = octree (8-way per node) | 3 | metres are decoder-free, sum is exact -> can afford fat rungs |
| **Latent (default)** | radix-2 (binary nesting, 1 prefix step) | 1 | each rung carries ONE auditable conditional bit |
| **Latent (exception)** | base-7 IGEO7/Z7 | 2.807 | ONLY if equal-area hex tiling is a hard requirement |

The decisive reason on both is the **LCA primitive.** With a power-of-2 radix
`r = 2^b`, every level is a fixed `b`-bit field, so:

```
parent(key)            = key >> b
ancestor-at-level k    = key & mask_k
LCA(a, b)              = clz(a XOR b) / b          # single-cycle, branch-free, O(1)
```

The chain-rule COIN query is an ancestry/LCA operation evaluated on *every
visible node every frame*, so LCA cost is the dominant cost term and must stay
O(1). A non-power-of-2 radix (e.g. 7) breaks bit-alignment: descent needs
multiply/divide-by-7 + modulo, and LCA degrades to O(depth) digit-walk. This is
why power-of-2 dominates every production DGGS.

### 2.2 Radix -> bits/level (verified)

```
r = 2  -> 1.0000 bits/level
r = 4  -> 2.0000
r = 7  -> 2.8074   (log2 7)
r = 8  -> 3.0000
```

H3 wastes `3 - 2.8074 = 0.1926` bit/level by spending 3 bits to encode only 7
states; IGEO7/Z7 (AGILE-GISS 6/32/2025, DGGRID) reclaims that with a true
septenary index, AND gives equal-area cells -- but at the cost of divide-by-7
addressing and O(depth) ancestry.

### 2.3 Depth, path-ID width -- and the "618 not 64" correction

The verified physical span:

```
8.8e26 m / 1.616e-35 m  ->  log2 = 205.1  ~  spec's 206
```

**The digest's "~69 rungs at 3 bits = 206 bits" claim conflates two readings and
is wrong.** Three octree bits = ONE isotropic scale octave across three spatial
axes, NOT three scale bits. By the keystone's "one octave = one bit" law:

```
206 isotropic scale octaves  =  206 octree LEVELS
octree path-ID width         =  3 bits/level x 206 levels  =  ~618 bits
```

The "69 rungs" number only appears if you (wrongly) credit each octree level with
3 octaves of scale. **Canonical ruling needed in SUBSTRATE_SPEC:** one octree
level buys ONE octave (consistent with the keystone and the octave-quantized LOD
law). Under that ruling the honest physical key is **~618 bits, not 64 and not
128.** For reference:

```
64-bit  Morton:  21 octree levels  (63 / 3)        -- verified
128-bit Morton:  ~42 octree levels
206 octaves:     206 levels -> 618 path bits
```

Therefore the spec's **"split into 64-bit integer rung + near-origin float" is
MANDATORY, not optional polish** -- no fixed machine word holds the depth.

### 2.4 Path-ID width: self-delimiting, sentinel-terminated

Prefer S2's trick over H3's redundant resolution field. Layout:

```
[root bits][child: b per level] ... [sentinel: 1][zeros]
depth = position of lowest set bit       (level k = (pos - root) / b)
```

Depth is then free -- no separate length field, and LCA stays XOR+CLZ. This is
the sweet spot for the unbounded 206-octave ladder and naturally supports the
open-ended latent ceiling (Q4): a path-ID is a PATH, not a coordinate in a fixed
box, so it inherently has no maximum.

Accepted tradeoff (not a free lunch): variable-length sentinel-terminated keys
are worse for columnar/cache-friendly storage than fixed 64-bit IDs (why S2/H3
stay 64-bit). The viewer pays a storage/cache cost for the unbounded depth the
universe->Planck span demands.

### 2.5 LCA cost (verified word model)

For a key spanning `W` bits = `ceil(W/64)` machine words, LCA = up to
`ceil(W/64)` XOR+CLZ ops: XOR word-by-word from the MSB, stop at the first
differing word, then `CLZ / b` that word.

```
64 bits   -> 1 op
128 bits  -> 2 ops
206 bits  -> 4 ops
618 bits  -> 10 ops
```

All O(1) for fixed `W`. LCA = compare integer rungs by XOR+CLZ first; descend
into the near-origin float ONLY when rungs tie. Re-anchoring (rebasing) at
sub-rung scale uses the fractal deep-zoom reference-orbit + perturbation trick
(re-anchor when `|Z_m + z_n| < |z_n|`).

### 2.6 Why the LATENT radix should be SMALLER (the adversarial correction)

The digest leans toward depth-efficient fat rungs everywhere. **On the latent
fiber this is dangerous for the chain-rule COIN.** The "one prefix step = one
octave = one bit" Matryoshka claim is only *approximately* additive: MRL prefixes
are near-monotone ("later dims can only improve, never rescue"), but the bit GAIN
per prefix step is NOT constant and not guaranteed `<=` the conditional
rate-distortion cost. Summing many latent rungs can therefore DRIFT above the
joint cap by accumulated rounding -- and a fat 7-bit rung carries more
un-audited conditional bits per rung, making the drift WORSE.

> **Pick the SMALLER radix (1 bit/level) on the LATENT axis** precisely so each
> rung carries one auditable conditional bit, accepting deeper trees. Reserve the
> fat radix (3 bits/level octree) for the PHYSICAL fiber, where metres are
> decoder-free and the sum is exact.

This leaves an **undischarged obligation** (open Q below): measure
`L(x | first-k dims) - L(x | first-(k+1) dims)` on a real MRL model and verify it
is `>= 0` and `<= the joint-cap increment` for all k. If it can go negative or
overshoot, the latent fiber needs an explicit per-rung re-floor.

### 2.7 base-7 exception

Take base-7 (IGEO7/Z7) ONLY if equal-area hex tiling is a *hard* latent
requirement. Span in base-7 = `ceil(206 / 2.8074) = 74 levels` (verified). But:
a "word" has no intrinsic metric (no area/volume), so equal-area -- the only
thing base-7 buys -- almost certainly evaporates on the latent side. The
recommendation leans power-of-2 on both fibrations; base-7 is a documented escape
hatch, not the default. [SPEC] If a "word" later acquires a measure (embedding-
space volume / Matryoshka prefix energy), the equal-area case reopens.

### 2.8 Naming hygiene (pin in spec)

"radix-2 per axis" and "radix-8 per node" are the SAME octree code: 3 bits/level,
8-way node branching, 2-way per-axis. Pin one framing in SUBSTRATE_SPEC to avoid
a phantom radix choice.

---

## Q4 -- The latent ceiling N

### 4.1 The resolution: there is NO honest fixed N, and the architecture does not need one

The quantity the COIN measures is ENTROPY (optimally-compressed bits), not raw
volume. Entropy is coder-relative and still growing, so any single pinned N would
be a fake bit. The resolution is to make the latent axis re-anchoring exactly
like the physical cone, and to *prove N is unnecessary for any zoom operation*:

```
rendered_bits(x | ancestry) = min( measured_bits(x | ancestry), lod_budget(zoom) )
```

is ALREADY window-relative -- it never references a global N. Windowing normalises
against the resident subtree, never against a civilisation total.

### 4.2 Two readout modes, one law

**(A) PRIMARY -- relative-to-resident-subtree (no N, ever).**
When you zoom into node R, the bits ABOVE R (its path-ID) become a
losslessly-carried ANCHOR that is NOT rendered; the WINDOW renders only the
subtree below R against the local budget. Normalisation uses

```
B_R = measured_bits(R | parent-of-R)
    = local sum of conditional child bits down to the LOD frontier   (finite, local)
```

Displayed fraction `frac(x) = rendered_bits(x|A) / lod_budget(zoom)`;
"structure remaining below me" gauge = `B_R - lod_budget(zoom)`. None reference a
global N. This is the chain-rule COIN: addressing a single leaf WORD costs the
PATH SUM (toy: civilisation -> era -> field -> work -> paragraph -> sentence ->
word ~ 55 conditional bits), NOT the whole-corpus total. **You never pay the
global ceiling to address one leaf -- you pay the ancestry path.** Re-anchoring
is exact: `anchor_bits + window_bits = full path`, byte-for-byte (identical to
the fractal reference-orbit + perturbation trick and to Patent US 8,972,462's
fixed-field/sliding-window, one bit shift = one octave). Mode A needs only the
integer path-ID ladder (a PATH, inherently no maximum) plus the near-origin
float, and is immune to coder-dependence -- so it is the DEFAULT.

**(B) OPTIONAL -- soft absolute scale-bar (a disclosed running estimate, never a
render input).**
If a user wants an absolute "you are here in all of civilisation" readout:

```
N_soft = (effective human-text stock) x (residual entropy/token under PINNED coder),
         gated by the KT back-off (cap at the entropy-coded literal -> no under-count)
```

Current anchor (disclosed, dated): Epoch AI 2024 effective stock ~ 300T tokens
(90% CI 100T-1000T); at 0.5-2.0 bits/token residual entropy this is
~10^14.2-14.8 bits, i.e. **log2 ~ 47-49** -- robust to within ~+/-2 bits despite
10x stock x 4x coder uncertainty. The scale-bar shows this as a **BLURRED band**
(the honesty badge), widening with the disclosed CI, NEVER as a sharp number. Its
conservative lower bound is the **session running-max**: `max over traversed
subtrees of (anchor_bits + measured_bits resident)` -- a true achieved-so-far
quantity that can only grow.

### 4.3 Why the open-endedness dissolves (the latent twin of "never render a fake bit")

Raw datasphere is open-ended (~149 -> 181 -> 394 ZB, 2024-2028, IDC; ~1 order /
3-4 yrs). But the COIN measures ENTROPY, and synthetic/redundant content
compresses to ~0 `measured_bits`. **Model collapse is the proof:** synthetic
content adds raw bytes but ~0 new entropy. So the open-endedness cannot push the
ceiling up -- the effective ceiling is the ENTROPY ceiling (slowly-growing,
near-saturating per the 2024-26 data wall), not the RAW one (~unbounded). The
keystone's law transfers verbatim: physical = "never render a fake measured bit"
(Landauer: a real bit costs `>= kT ln2`); latent = "never render a
synthetic/redundant bit as if it were measured entropy" (model collapse = the
violation). [Caveat] This rests on the current-regime data-wall reading; if a
genuinely new high-entropy modality (e.g. verified scientific-instrument streams)
is folded into "civilisation", N_soft could resume ~1 order/decade growth.
"Saturating" is a current-regime claim, not a theorem.

### 4.4 Pin both ends -- the sharpness normaliser may NOT float (adversarial correction)

The re-anchoring trick that makes unbounded RANGE honest is the SAME trick that,
applied to the SHARPNESS normaliser, would manufacture a fake bit. If the
window's normalisation re-anchors between frames, the same node can render at
different sharpness for the same `measured_bits`, and a viewer cannot tell a true
refine from a re-normalisation. The physical cone is safe because its rebasing is
to a FIXED Planck floor / fixed log2(metre). The latent cone has "0 bits = one
word/token" pegged at the fine end but a FLOATING coarse end. Therefore:

- **Fine end: HARD-pegged.** "0 bits = one token" at the structure-function kink
  k\* (Algorithmic Minimum Sufficient Statistic) -- don't zoom past it; beyond is
  noise. [Caveat] "one token (~16 bits)" not literally "one bit" -- a token is
  not a bit; the fine-end zero is a token, and its exact value is a disclosed
  coder property.
- **Coarse end: may grow, but only by a DATED, DISCLOSED re-measurement, never
  silently per-frame.** RANGE may rebase freely (mode A); the SHARPNESS cap may
  NOT rebase without a dated disclosed re-measurement. Freeze the coarse
  normaliser to a disclosed entropy-ceiling estimate (Hilbert & Lopez optimally-
  compressed bits ~71 bits in 2007 for all-media, OR a fresh pinned-decoder
  re-measurement of a reference corpus), dated and versioned.

### 4.5 Scope toggle (declare, do not hide)

"civilisation" = human-text-only -> N_soft ~ log2 47-49; OR all-media (incl.
video/images) -> ~ log2 71 (Hilbert & Lopez). This single scope choice swings
N_soft by ~1.5 orders of magnitude and MUST be a declared toggle on the
scale-bar, not a hidden assumption. The "civilisation -> word" cone is the
textual-semantic corpus, so log2 ~48 is correct FOR THIS AXIS; label the scope
(text-entropy, not all-media-bytes) so a user expecting the famous H&L 71-bit
number sees why it differs.

### 4.6 Latent <-> physical symmetry (the mirror)

```
PHYSICAL                              LATENT
--------                              ------
HARD Planck floor (log2 metre)   <->  HARD single-word/token floor (k*)
soft Lloyd/horizon ceiling       <->  soft, disclosed, slowly-growing N_soft
  (~10^90 bits ~ log2 299;             (~log2 48 text / ~71 all-media,
   ~10^120 ops ~ log2 399;              never pinned, never fed into rendering)
   life ~10^60 ~ log2 199)
```

N is resolved by being *structurally unnecessary*, with an honest blurred readout
where one is wanted.

---

## SPECULATION (disclosed)

> Register shift: the following are conjectures, not load-bearing claims. Each is
> marked [SPEC].

- **[SPEC] One shared coder over a joint token stream.** Can the physical and
  latent prequential codelengths be measured by ONE pinned coder over a joint
  stream (splat-tokens + concept-tokens)? If so, the two fibrations become
  *literally one code over one base poset* rather than two analogous codes -- the
  cross-half COIN becomes an IDENTITY, not an analogy. Worth a small joint-stream
  NLL experiment.

- **[SPEC] Matryoshka prefix-doubling IS the octave.** If an embedding's natural
  prefix steps are geometric (64/128/256/512, ratio 2), then radix-2 in log-dim
  is exactly the embedding's own nesting and no separate quantizer is needed --
  the prefix-doubling literally IS the octave. Check against SMEC / MetaEmbed
  prefix schedules.

- **[SPEC] k\* as a measurable latent Planck constant.** If k\* (the AMSS kink)
  is stable across coders for a typical concept, it is a *measurable physical-
  style constant of the latent medium* -- the smallest meaningful semantic
  quantum. If it drifts heavily with coder strength, the "single word" floor is
  coder-relative and must be disclosed per atlas.

- **[SPEC] A word might acquire a metric.** If embedding-space volume or
  Matryoshka prefix energy gives a "word" a genuine measure, the equal-area
  argument for base-7 (IGEO7/Z7) reopens on the latent fiber, and the latent
  radix choice would have to be re-litigated.

- **[SPEC] N_soft blur = CI in 2^-bits.** Map the soft band's blur width directly
  to the disclosed 90% CI in log2-bits (~+/-1.3 bits at the coarse end), so the
  scale-bar's fuzziness IS the honesty badge in the *same units* as the rest of
  the COIN -- aesthetically the cleanest unification, but the perceptual
  CI -> pixels mapping is unverified.

---

## QUESTIONS WE SHOULD BE ASKING

> Register shift: these are meta-level / framing questions about the unit
> programme itself, not tasks with known answers. They are the questions whose
> answers would most change the design.

- **Is "appearance = 2^-bits" a claim about the WORLD or about the CODER?** On
  the physical axis metres are coder-free, so 2^-bits is (near) a world-property.
  On the latent axis it is irreducibly a coder-property. Are we building a viewer
  of *civilisation*, or a viewer of *one coder's model of civilisation*? The
  honest answer may be the latter -- and if so, the pinned coder is not a nuisance
  parameter but the SUBJECT of the latent half.

- **What is the latent equivalent of a measurement?** The physical half has a
  clean notion: light on a sensor, entropy-constrained quantization. The latent
  half's "measurement" is a reconstruction-and-verify under a coder. Is there a
  coder-independent latent measurement at all, or is the latent axis
  *constitutively* second-order (a measurement OF a model)? This decides whether
  cross-model agreement is a calibration detail or the whole game.

- **Does the chain rule actually hold, or only nearly?** The entire
  anchor+window=path additivity rests on conditional codelength being exactly
  additive across ancestry. Shared-ancestor double-counting, prefix
  non-monotonicity, and re-anchoring residuals all threaten it. We should ask not
  "is it additive?" but "what is the MEASURED additivity defect, in bits, on a
  real corpus, and is it below one rung?" If it is not, the COIN is approximate on
  the latent fiber and we should say so in bits.

- **Is k\* a floor or a horizon?** We treat the structure-function kink as a hard
  fine-end floor ("0 bits = one word"). But epiplexity suggests the floor moves
  with the *learner's* compute budget. Should the latent Planck floor be a fixed
  constant or a disclosed function of coder compute -- i.e. is the "smallest
  meaningful word" itself scale-relative?

- **What breaks first under cross-model disagreement?** If GPT-5.x and Gemini
  disagree by more than a rung on load-bearing nodes, do we (a) render the MAX
  (conservative blur), (b) average, or (c) treat divergence itself as a rendered
  signal (show the disagreement as texture)? Option (c) would make coder-relativity
  *visible* rather than hidden -- arguably the most honest move, and unexplored.

- **Are we measuring the right thing by measuring codelength at all?** Epiplexity
  warns that plain codelength counts incompressible-but-useless noise as "bits."
  k\* is our current answer (stop at the kink). But should the unit be
  *structural* content from the start (epiplexity-style), accepting it is not a
  sound per-item upper bound, or stay with sound-but-noise-counting codelength and
  rely on k\* to mark the cutoff? This is a genuine values choice between soundness
  and meaningfulness.

---

## Open sub-questions for Pav

1. **One-line ruling for SUBSTRATE_SPEC:** does one octree level buy ONE scale
   octave (-> ~618-bit physical path-ID) or THREE (-> ~206)? This sets the
   path-ID width at 3x and reconciles-or-refutes the digest's "69 rungs". I take
   1 octave/level as canonical (keystone-consistent); needs your sign-off.

2. **How is latent fidelity tau operationalized for a single word** so
   `measured_bits(tau)` is comparable across nodes -- round-trip reconstruction +
   embedding similarity, downstream-task accuracy, or a judge LLM? Must be pinned
   before any latent bit-count is load-bearing.

3. **Scope toggle default:** is "civilisation" human-text-only (log2 ~48) or
   all-media (log2 ~71)? This is the single biggest swing in any absolute readout.

4. **Which pinned coder(s)** for the canonical atlas, and is the conservative
   cross-model rule "render the MAX of GPT-5.x and Gemini" acceptable, or do you
   want disagreement shown as visible texture (the unexplored option c above)?

5. **Discharge the latent additivity obligation:** approve an empirical
   prefix-length-vs-NLL sweep on a real MRL model to confirm one prefix step
   `~` one bit (`>= 0` and `<= joint-cap increment` for all k). If it fails, the
   latent fiber needs an explicit per-rung re-floor.

6. **Coarse-end normaliser version:** pin and DATE the frozen latent
   sharpness-ceiling -- Hilbert & Lopez 2007 (~71 bits) or a fresh pinned-decoder
   re-measurement -- and decide the re-measurement cadence (it may only grow by
   dated disclosure, never silently).
