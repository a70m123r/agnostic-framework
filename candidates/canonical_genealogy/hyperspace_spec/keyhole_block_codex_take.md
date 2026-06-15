**Position**

Use the block universe as the target ontology, not as the stored artifact.

The honest stack is:

```text
fixed world/latent block B*     unknown referent
append-only fact log L_tau      observations up to compiler time tau
compiler C(L_tau)               inference engine
compiled view B_hat_tau         posterior estimate, not reality
render R(B_hat_tau, budget)     visible keyhole, capped by measured_bits
```

The system never writes into `B*`. It only appends observations and increases measured_bits about coordinates in `B*`.

**1. Block Universe Substrate**

Eternalism is useful if it means: every event or latent state has coordinates, including past and future-relative positions. It is dangerous if it means: the compiled view is complete.

A fact wrapper should be a measurement, not a fact:

```text
w = {
  target: axis coordinates or fuzzy region,
  measurement_operator: M,
  observed_value: y,
  noise_model: N,
  axes: what/when/where/who/how/why/whom,
  before/after links,
  measured_bits per axis,
  provenance,
  compiler_time tau
}
```

Observation across time is then simple:

```text
y_i = M_i(B*) + noise
B_hat_tau = argmin_B [sum_i loss(M_i(B), y_i) + prior(B)]
```

A new observation in 2026 can sharpen a 1790 latent state of "democracy" without changing 1790. It changes `B_hat_tau`, not `B*`.

The main ontology leak is false determinism: a compiled block looks like the thing itself. Prevent that with two time axes:

```text
event_time t      when the target state/event belongs
compiler_time tau when the system learned/inferred it
```

Every render must answer: "what did the system know as of tau?" No `as_of_tau`, no honesty.

**2. Multi-Keyhole Tomography**

Treat each keyhole burst as a projection of a latent field.

Let:

```text
F(z, t) = latent construct field, e.g. democracy over latent coordinates z and time t
y_i     = observed resonance burst
P_i     = projection/keyhole operator
eta_i   = noise
```

Then:

```text
y_i = P_i F + eta_i
```

Prior art mappings:

```text
Radon transform / CT:              many angular projections reconstruct density
synthetic aperture:                many weak views combine into higher resolution
multi-view 3D reconstruction:      shape from many viewpoints
Gaussian splatting:                uncertain particles with covariance ellipsoids
compressed sensing:                sparse structure recovered from few incoherent views
spreading activation:              concept probe propagates through graph substrate
```

A burst is useful only to the degree it is independent. Ten newspapers copying one wire story are one projection with ten echoes, not ten projections.

Define effective evidence:

```text
N_eff = rank_or_information_dimension({P_i}, weighted by source independence)
```

Fidelity grows like information, not count:

```text
bits_region <= min(
  sum_i independent_bits_i,
  coin_cap_region,
  model_capacity_cap,
  source_provenance_cap
)
```

Resolution improves when projection diversity covers the local frequency band:

```text
resolvable_detail k only if projections contain enough independent energy at k
```

Limited-angle tomography gives streak artifacts. In this system, streak artifacts must render as fuzz or conjecture-stubs. Mechanism:

```text
if posterior variance high along any axis:
  do not collapse to MAP as fact
  render covariance/fuzz
  emit typed stub for missing axis
```

A reconstruction "locks" when additional independent projections no longer move the posterior beyond the declared tolerance:

```text
KL(B_hat_tau+1 || B_hat_tau) < epsilon
and measured_bits >= disclosed_threshold
and no high-impact alternative hypothesis remains within delta evidence
```

**3. Observation, Meaning, Knowledge**

Observation:

```text
a bounded measurement y_i with provenance and measured_bits
```

Meaning:

```text
a compression: multiple observations become explainable by a shorter latent structure
```

Knowledge:

```text
a stable, corroborated compression that survives independent probes
```

Measured-bits framing:

```text
observation_bits = bits delivered by probes
meaning_bits     = compression gain from latent model
knowledge_bits   = corroborated bits after adversarial/independent checks
```

A useful threshold is the Kolmogorov structure-function kink: the point where adding model complexity stops buying meaningful compression. Before the kink, structure is being discovered. After it, the model is probably fitting noise.

Speculative but useful rule:

```text
knowledge if:
  compression_gain > threshold
  independent_corrob_bits > threshold
  prediction_or_retrodiction succeeds out of sample
  alternatives are explicitly weaker
```

Meaning is both discovered and constructed. Discovered because the substrate constrains which compressions work. Constructed because the choice of probe vocabulary, latent axes, and observer purpose changes which structures become visible. That is the participatory back-reaction.

**4. Conjecture-Stubs**

A conjecture-stub is not a weak fact. It is a typed hole.

```text
stub = {
  type: missing_what | missing_how | missing_why | missing_link | missing_actor,
  target_region,
  triggering_fuzz,
  candidate_hypotheses,
  falsifiers,
  required_probe_types,
  current_support_bits,
  status: conjecture | under_test | corroborated | demoted | retired,
  created_by,
  compiler_time
}
```

Lifecycle:

```text
fuzz detected
-> stub created
-> experiment/probe proposed
-> new bursts collected
-> support_bits update
-> corroborate, split, merge, demote, or retire
```

Render rule:

```text
facts: solid, sharpness capped by measured_bits
inferences: translucent, show dependency
stubs: outline/negative space, never same visual grammar as facts
```

A stub must always display its falsifier. If it cannot be falsified, it is not a conjecture-stub. It is a note, metaphor, or prior.

Use stubs for active learning:

```text
choose next probe P_next maximizing expected information gain

P_next = argmax_P E[ H(B_hat) - H(B_hat | y_P) ] / cost(P)
```

Better: maximize expected reduction in decision-relevant uncertainty, not global uncertainty.

**5. Biggest Risk And Settling Experiment**

Biggest risk: the compiled block becomes a prestige visualization of abductive guesses. The viewer may create fake continuity, fake causality, and fake certainty by smoothing sparse observations through an elegant latent space.

Settling experiment:

Build a toy hidden block with known ground truth. Hide it from the compiler. Generate keyhole bursts from limited, biased, copied, and independent projections. Then compare three renderers:

```text
A: naive compiled block, renders MAP estimates sharply
B: COIN-capped block, renders only measured_bits
C: COIN + stubs + active learning
```

Success condition:

```text
C reconstructs true latent shape with fewer probes,
marks limited-angle gaps as fuzz/stubs,
aims new probes into those gaps,
and produces fewer false sharp bits than A or B.
```

If the model cannot beat a normal probabilistic graph plus uncertainty visualization in this controlled case, then "block universe compiled by keyholes" is mostly metaphor. If it does beat it, the machinery is real: append-only measurements, projection geometry, measured-bit rendering, and active conjecture stubs form a working epistemic instrument.
