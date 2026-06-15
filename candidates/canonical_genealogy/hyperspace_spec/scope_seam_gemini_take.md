1. RESOLVE: TOGGLE VS. DIAL
PAV’s steer is correct: the coupling is a DIAL, not a toggle. But we must be precise about what the dial *is* mechanically. 

If we use a 2-bit toggle (Spatial, Latent, Both), we force a false ontological binary on entities that exist on a spectrum. An idea ("Democracy") has 0 spatial bits. A person ("Bob") has 40 spatial bits. An organization ("Red Cross") has ~15 spatial bits (a dispersed but bounded set of coordinates).

The DIAL is not a standalone arbitrary coefficient \kappa. The dial *is literally the measured spatial precision* (the COIN law). 
Mathematically, the dial is the Spatial Negentropy (information gain) of the entity's physical anchor. 

Let H_max be the spatial entropy of a uniform distribution over the Earth's surface. 
Let H(E) be the spatial entropy of entity E's measured location data.
Dial value D = 1 - (H(E) / H_max)

- When D = 1 (Max dial): A sharp physical point (e.g., a specific person at a specific GPS coordinate). \sigma approaches 0. Bits are maxed.
- When D = 0 (Zero dial): A purely latent concept with zero physical bounding (e.g., the number "4"). \sigma approaches \infinity. Blur is total.
- When 0 < D < 1: A ZONE OF INFLUENCE.

By making the Dial equal to the measured spatial bits, the COIN law automatically enforces the render: you only get a sharp physical location if you have the bits to prove it.

2. FORMALISING "ZONE OF INFLUENCE"
How do we render an organization or movement without drawing fake crisp boundaries? 

Prior Art: 
- Kernel Density Estimation (KDE)
- Hagerstrand's Spatial Diffusion of Innovation (Information Fields)
- Huff Gravity Model (Spatial interaction / catchment probabilities)

Mechanism:
A latent entity does not have a single (x, y) coordinate. It has a spatial Probability Density Function (PDF). 
PDF(x) = \sum [ w_i * K(x - x_i, \sigma_i) ]
where x_i are the known anchor points (headquarters, active members, origin events), w_i is the weight of that anchor, and K is a spatial kernel.

Under the COIN law: \sigma_i is strictly bounded by 2^(-location_bits_of_anchor_i). 

Render Execution:
DO NOT draw polygons or isolines (contour lines). Isolines imply a hard boundary threshold that doesn't exist in the data.
DO use Monte Carlo Stippling (Pointillism). 
To render the Zone of Influence, sample N points from the entity's PDF and render them as semi-transparent dots at the physical scale layer. 
- High spatial bits = dense, tight cluster of dots (looks solid).
- Low spatial bits = sparse, wide haze of dots. 
This is mathematically honest. The blur *is* the uncertainty/influence gradient.

3. THE LIFECYCLE ORIGIN
The physical anchor migrates and diffuses over time. We must separate the ASSERTION (the event) from the ANTECEDENTS (the conditions).

"Calling it" (Naming/Founding) is the Origin Event. It is a spacetime coordinate with high precision. 
Event E = {Latent_ID, Actor_ID, x_0, t_0}.
At t = t_0, the entity's spatial footprint is exactly the footprint of the Actor (the person who called it). \sigma is tiny.

As t > t_0, the entity begins its Lifecycle. The footprint diffuses. 
Spatial Diffusion Equation: \partial P / \partial t = D * \nabla^2 P + Source - Sink
The "Zone of Influence" grows. The physical anchor splits from a single point (the originator) into a multi-modal distribution (the followers/org structures). 
The true origin of an idea is the Assertion Event. The "conditions that produced them" are LATENT ancestors in the meaning-tree, not spatial origins. The assertion event is the spark that jumps from the latent fiber to the physical fiber.

4. WORKED TEST ENTITY: ELON MUSK
Let's trace Elon Musk across the two fibers over time (t).

Latent Fiber: Node [ID: EM_01]. Connected to nodes: [EVs], [Spaceflight], [Mars], [Twitter/X].
Physical Fiber Lifecycle:

- Phase 1: Origin (1971). 
Data: Birth in Pretoria, South Africa. 
Render: A single, incredibly sharp point (high location bits). Dial D ~ 0.9.

- Phase 2: Spread / Zip2 & PayPal (1990s).
Data: Moving between Palo Alto and specific office buildings.
Render: The sharp point migrates to California. A tiny "Zone of Influence" haze begins to form around Silicon Valley (his immediate network/capital reach).

- Phase 3: Bifurcation / SpaceX & Tesla (2010s).
Data: Hawthorne (SpaceX HQ), Fremont (Tesla HQ), Boca Chica.
Render: The "Meat" coordinate (where his physical body is tracked via private jet) is a sharp, rapidly moving point. The "Zone of Influence" (his companies) is a stationary, multi-modal Gaussian mixture. Three tight, bright hazes over California and Texas.

- Phase 4: Attention-Output Field / Twitter (2022+).
Data: Ownership of X, global cultural impact.
Render: The latent-to-physical dial for his "influence" drops in spatial precision but expands in mass. A massive, low-opacity continental stipple-cloud covers North America and Europe, representing the digital attention-output field. The physical body remains a single sharp point.

He renders as a comet: a sharp, high-bit physical nucleus (the man) dragging a massive, low-bit, multi-modal probabilistic tail (the zones of influence).

5. THE BIGGEST RISK & THE SETTLING EXPERIMENT
The Risk: Conflating "Cause" (Intrinsic location) with "Effect" (Projected influence).
If an organization is defined purely by its Zone of Influence, the base topology becomes recursively unstable. If Hacker X in Siberia writes a virus that only destroys computers in Wall Street, what is the footprint of the virus? If you map it to Wall Street, you are mapping *symptoms*, not the entity itself. The spatial anchor becomes a projection of effects, ruining the integrity of the physical fiber.

The Settling Experiment: "The Broadcaster vs. The Audience Test"
Take an entity that has a microscopic physical origin but a massive, instantaneous physical effect. 
Example: The Satoshi Nakamoto Bitcoin Whitepaper release, or the broadcast of the Moon Landing.

Task the viewer to render the entity.
If the engine merges the Broadcaster (origin) and the Audience (influence) into a single mathematical centroid (e.g., putting the "location" of the Moon Landing broadcast in the middle of the Atlantic Ocean because it averages the US and Europe), the math is broken.

Success criteria: The engine MUST maintain a bipartite physical state. 
1. The Core Anchor: The server/person (high precision, low spread).
2. The Field of Effect: The audience/users (low precision, high spread, defined by interaction logs).
If "Zone of Influence" is treated as a secondary metric (a field generated BY the anchor, mapped via the network) rather than replacing the anchor itself, the risk is mitigated. The dial governs the rendering of the field, while the exact integer path-ID preserves the core anchor.
