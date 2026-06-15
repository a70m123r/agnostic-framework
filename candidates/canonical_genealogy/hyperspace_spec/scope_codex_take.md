**Core Position**

Use one **bit-addressed hierarchy**, not one global XYZ space. The scalar log/bit axis is canonical; Euclidean vectors are temporary local render coordinates.

**1. Coordinate Math**

Primitive:

```text
Node N:
  physical radius: r_N = 2^s_N meters
  local coord:     u_N in [-1, 1]^3
  parent transform:
    x_parent = c_N + 2^(s_N - s_parent) * R_N * x_N
```

Store `s_N` as bits. Store `c_N` in **parent-local fixed point / dyadic tile coordinates**, not global meters. The address of a point is:

```text
physical_addr = root/path/to/node + local_u + scale_bits
```

Never materialize Planck-to-universe coordinates as one float. To render, find the least common ancestor of camera and target, compose transforms only down that branch, subtract camera position there, then pass camera-relative coordinates to the GPU.

Ranking of primitives:

1. **Hierarchical nested local frames**: the real coordinate system.
2. **Camera-relative / floating origin**: render implementation detail.
3. **Log or reversed-Z depth**: necessary for depth precision, insufficient for world precision.
4. **Arbitrary global floats**: wrong primitive except for offline analysis.

Depth:

```text
z_log = log2(max(z, near) / near) / log2(far / near)
```

Use log depth or reversed-Z inside scale shells. But depth buffers do not fix vertex precision, so the hierarchy is non-negotiable.

**2. LOD As The COIN**

The proposed law is right, with one correction: make it per channel.

```text
rendered_bits_channel(x) =
  min(measured_bits_channel(x), lod_budget(x, camera), compute_budget)
```

Concrete physical LOD budget:

```text
s_N = log2(node_radius_meters)
w   = log2(view_window_radius_meters)
P   = viewport pixels across relevant axis
tau = minimum visible support, about 1 to 2 px

lod_budget(N) = max(0, floor(log2(P / tau) + s_N - w))
```

Perspective equivalent:

```text
lod_budget(N) =
  max(0, floor(log2(focal_px / tau) + log2(r_N / distance_N)))
```

Each zoom octave adds exactly one resolvable bit. A node smaller than a pixel gets budget zero and becomes a dot, label, or summary token.

Chunk rule:

```text
target_lod = min(measured_bits(N), lod_budget(N))
load tile/splat level l where l <= target_lod
refine children only if required_bits(child) <= target_lod
```

For Gaussian splats:

```text
sigma_world = r_N * 2^(-rendered_bits_geom)
sigma_screen >= tau
```

Recent 3DGS work fits this directly: hierarchical Gaussian sets, view-dependent LOD selection, out-of-core streaming, chunk blending, octree/anchor LOD, and continuous zoom hierarchies. The warning is generative zoom: synthesized details can be useful, but under COIN they are **predicted bits**, not measured bits, so they must render with lower confidence or blur until measured.

**3. Nested Domain Tree**

Use membrane nodes like:

```text
MembraneNode {
  id
  phys:   { parent, radius_bits, parent_local_origin, orientation, epoch, bounds }
  latent: { parent_or_parents, code_bits, embedding_frame, summaries_by_budget }
  measured_bits: { position, geometry, appearance, semantic, temporal }
  content: { splat_tiles, mesh_tiles, text_chunks, provenance }
}
```

Do **not** force physical and latent containment into the same tree. They are two coupled trees/DAGs.

Physical containment:

```text
galaxy -> system -> planet -> region -> building -> room -> artefact
```

Latent containment:

```text
civilisation -> institution -> project -> person -> document -> claim -> word
```

These diverge constantly. A person is physically in a room but latently in an org, family, field, project, and civilisation. An artefact may be physically on Earth but semantically inside a theory. So the correct model is:

```text
entity_id E has:
  physical_addr(E, t)
  latent_addr(E, model)
  provenance/measurement links coupling them
```

The exact coupling point is the **observation/assertion event**:

```text
physical event at place/time -> measured signal -> latent claim
```

That is where physical bits become semantic bits.

**4. Collapse Symmetry**

Defensible, but not literally as “1 bit”.

The shared operation is rate-distortion compression:

```text
render_B(X) = argmin_Y D_X(Y)
              subject to code_length(Y) <= B
              and B <= measured_bits(X)
```

For physical space, `D_X` is metric/projection error. For latent space, `D_X` is semantic/task distortion. At very low budget:

```text
universe -> dot / log-radius
civilisation -> word / symbol
Planck view -> number / limit marker
```

So yes: the dial is the thesis if it controls **compression budget** across space and meaning.

But “one word” is not one bit. A word from a 50k vocabulary is about 16 bits before context. A number with precision may carry many bits. The real symmetry is **one-token collapse**, not literal 1-bit collapse.

What would make it false: if semantic refinement is not locally compositional, if users need independent physical and meaning zoom controls, or if semantic importance routinely beats bit-budget ordering.

**5. Biggest Risk And Settling Experiment**

Biggest risk: the logs line up syntactically but not operationally. Physical scale bits, MDL bits, and render sharpness bits may share notation while obeying different distortion laws.

One decisive illustration/experiment:

Build a static “bit-slice atlas” before implementation.

```text
physical: universe -> galaxy -> system -> planet -> city -> person -> artefact
latent:   civilisation -> org -> project -> person -> document -> fact -> word
```

Annotate every node with:

```text
scale_bits
measured_bits
required_bits_to_refine
summary/code length
```

Then sweep one budget `B = 0..N`.

Pass condition: the same `B` explains both physical refinement and semantic refinement without hand tuning. Gaussian sigma halves per bit; text summaries gain one bit-budget step per bit; no crisp feature appears above measured_bits.

Fail condition: the physical and latent sides require separate budgets to feel truthful or useful.

Sources checked: [3D Gaussian Splatting](https://arxiv.org/abs/2308.04079), [LODGE](https://arxiv.org/abs/2505.23158), [A LoD of Gaussians](https://arxiv.org/abs/2507.01110), [StreamLoD-GS](https://arxiv.org/abs/2601.18475), [GaussianZoom](https://arxiv.org/abs/2605.18252), [3D Tiles HLOD/spec](https://github.com/CesiumGS/3d-tiles/blob/main/specification/README.adoc).
