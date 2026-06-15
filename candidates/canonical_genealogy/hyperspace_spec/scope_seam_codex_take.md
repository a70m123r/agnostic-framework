**Answer**
Use a dial, but not as a free arbitrary edge slider. The primitive should be a measured physical anchor field with COIN location bits. A discrete tag is only a schema/UI shortcut.

For entity `e`:

```text
A_e(x,t) = sum_o w_o * K_space(d(x, x_o) / sigma_o) * K_time(|t - t_o| / tau_o)

sigma_o = 2^(-location_bits_o)
render_bits_o <= location_bits_o
```

`A_e` is the physical anchor: a point when evidence is sharp, a zone when evidence is diffuse, and a multi-modal field when an entity has several sites or audiences. `kappa` can be derived from concentration:

```text
kappa_e(view,t) = information gained by A_e over the visible physical prior
```

So `kappa = 0` means "the physical anchor is present but no more localized than the prior"; `kappa = 1` means "localized to one resolvable physical cell at this scale." The toggle `SPATIAL / MEMBERSHIP / BOTH` is useful only when a renderer or query planner needs to know which operators are legal. It cannot express measured sharpness, so it cannot enforce COIN.

**Zone Of Influence**
Render an organization or movement as a field, not a polygon:

```text
zone_e(x,t) = operations_field + membership_field + attention_field + legal_field
```

Each source layer has its own provenance, weight, time span, and location bits. Headquarters, factories, launch sites, stores, offices, customers, employees, posts, citations, events, and users are different evidence channels. Do not collapse them into one crisp territory.

Rules:

- If the source is a precise address, render a small kernel at that address.
- If the source says "operates in Germany", use a low-bit support field over Germany, not a sharp claim that every border point is equally influenced.
- If the source is sparse, use adaptive bandwidth: `sigma_eff = max(2^(-bits), data_spacing, pixel_scale)`.
- Contours are allowed only as density thresholds, not as ownership boundaries.
- A legal border is a border of the jurisdictional source layer, not automatically a border of influence.

Prior art: kernel density estimation, adaptive KDE, fuzzy set membership from Zadeh, spatial-interaction/gravity models, Huff market-area models, time geography, and spatial diffusion of innovation. Huff-style models are especially relevant when influence depends on attractiveness and distance decay; KDE is better for honest visual density from sparse observations.

**Lifecycle Origin**
There is not one origin. There are at least three physically different origins:

```text
conditions_origin: diffuse causal field before the entity is named
person_origin: sharp-ish person trajectory / birthplace / biographical path
calling_origin: naming, declaration, incorporation, publication, or first assertion event
```

For canonical identity, the naming/calling event is the clean origin because it creates the addressable latent node. For causal explanation, the origin is a field of preconditions. Pav's steer fits: the person who called it is the nucleation event; the wider conditions are the pre-origin field; later adoption turns the point into a spreading zone.

**Elon Musk Test**
For Musk as a person, the physical fiber begins with a birth anchor: Pretoria, South Africa, June 28, 1971. If the source only says Pretoria, render city-scale blur, not a fake hospital-level point. Britannica gives the public timeline: South Africa, Canada, Queen's University, University of Pennsylvania, California, Zip2, X.com/PayPal, SpaceX, Tesla, X, xAI, Neuralink.

In the latent fiber, Musk has roles and edges: person, founder, CEO, investor, engineer/manager, public communicator, political actor, etc. Those edges attach to organizations and ideas.

In the physical fiber, render separate layers:

```text
origin layer: Pretoria birth anchor
trajectory layer: education/business migration over time
company-sites layer: Tesla, SpaceX, xAI, Neuralink, Boring Company sites
attention layer: media/X/public attention field, only where geolocated or honestly global
```

Tesla, for example, has sharp facility anchors such as Austin/Giga Texas, Palo Alto, Fremont, Nevada, Buffalo, Shanghai, Berlin-Brandenburg, Amsterdam, Tilburg, and other offices listed by Tesla. xAI currently lists offices in Palo Alto, Seattle, Memphis, and London. Those are not "Musk's body"; they are organizational influence kernels coupled to Musk through role edges.

**Biggest Risk**
The risk is mistaking a projection of effects for a coordinate. A heatmap of attention may just be population, language, internet access, media geography, or platform distribution wearing an entity label.

The settling experiment: build two time-sliced predictors.

```text
Model A: latent graph only
Model B: latent graph + zone_of_influence field built only from past observations
```

Hold out future geolocated observations: offices, events, customers, citations, adoption, mentions, visits. If Model B improves calibrated out-of-sample log score or spatial error across scales, zone-of-influence is a real coordinate. If not, it is only a projection layer.

Sources checked: [Britannica on Elon Musk](https://www.britannica.com/money/Elon-Musk), [Tesla Elon Musk bio](https://www.tesla.com/elon-musk), [Tesla worldwide offices](https://www.tesla.com/contact), [xAI company page](https://x.ai/company), [KDE](https://en.wikipedia.org/wiki/Kernel_density_estimation), [fuzzy sets](https://en.wikipedia.org/wiki/Fuzzy_set), [Huff model](https://en.wikipedia.org/wiki/Huff_model), [diffusion of innovations](https://en.wikipedia.org/wiki/Diffusion_of_innovations).
