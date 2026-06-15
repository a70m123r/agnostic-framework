Here is a direct, first-principles pressure-test of the Keyhole Block Universe concept, grounded in signal processing, information theory, and epistemic logic.

### 1. THE BLOCK UNIVERSE SUBSTRATE
**The Ontology:** A strictly eternalist (static) block universe is a trap if conflated with the map. The universe may be static, but our *epistemic state* is not. To obey the COIN law (no fake bits), the substrate must be **Bitemporal** (Prior art: Datomic, Event Sourcing). 
Every appended fact requires two time axes: `t_event` (when the thing happened/existed in the block) and `t_obs` (when the keyhole measured it). 

**How observation across time works:** 
The block universe itself ($U$) is indexed by `(x, y, z, latent, t_event)`. 
The compiler ($C$) operates over `t_obs`. At `t_obs = T`, the compiled block $B_T$ is the accumulation of all keyhole bursts up to $T$.
When a keyhole fires at $T$ to measure something at `t_event = T - 100`, it does not change the past of $U$; it increases `measured_bits` at $B_T(..., T - 100)$. The blur at that coordinate strictly decreases.

**The Leak (False-Determinism / Presentism):**
The leak occurs in the compiler's *interpolation phase*. If the compiler assumes that because a latent construct was measured as $X$ at $T-10$ and $X$ at $T+10$, it must have been $X$ at $T$, it has committed a presentism leak. It generates "fake bits." In an honest block universe, the unmeasured $T$ coordinate MUST remain blurred, bounded only by the maximum theoretical rate of change of the latent construct (Lipschitz continuity).

### 2. MULTI-KEYHOLE TOMOGRAPHY
**The Math:** This maps directly to **Computed Tomography (CT) via the Radon Transform** and **Fourier Slice Theorem**, expanded to $N$ dimensions.
Let the latent construct be a scalar field $F(\mathbf{x})$. A keyhole burst from angle $\theta$ is a projection $P_\theta = \int F(\mathbf{x}) d\mathbf{x}_\perp$.
By the Fourier Slice Theorem, the 1D Fourier transform of $P_\theta$ gives a 1D slice through the origin of the $N$-dimensional Fourier transform of the construct, $\hat{F}(\mathbf{k})$.

**The Fidelity Law:**
`measured_bits` maps directly to the volume of frequency space $\mathbf{k}$ filled by our keyhole slices. 
Fidelity $R \propto \sum_{i=1}^K \Delta \theta_i$. 
If keyholes are parallel (dependent), they sample the same slice—no new `measured_bits` are gained. Independence means orthogonal slices in frequency space.

**Preventing Artifacts (Honest Fuzz vs. Streaking):**
In standard CT, missing angles cause "streaking" artifacts (hallucinated high-frequency data across the image). Under the COIN law, streaking is a violation (fake bits). 
To solve this, we use **Compressed Sensing (L1-norm Total Variation minimization)** combined with a strict **Bandpass Mask**. 
Where frequency space is unsampled, we enforce an explicit low-pass filter. The missing angles do not streak; they *blur*. The output is a mathematically guaranteed lower-bound of sharpness: `rendered_sharpness = inverse_fourier(sampled_frequencies_only)`. 

### 3. OBSERVATION -> MEANING -> KNOWLEDGE
We define this transition using **Algorithmic Information Theory (Minimum Description Length / MDL)**.

*   **Observation:** The raw keyhole returns $D$ (Data). To store it costs $L(D)$ bits.
*   **Meaning (The Compiler):** The compiler searches for a structure/model $M$ that compresses $D$. Meaning is the extraction of a rule. The cost is now $L(M) + L(D|M)$ (cost of model + cost of exceptions). Meaning is *constructed* (a participatory back-reaction), because multiple compression algorithms can compress the same data differently.
*   **Knowledge (The Kink):** Observation becomes Knowledge at the **Kolmogorov Structure-Function Kink**. As independent keyholes add data $D_1, D_2, D_3...$, the model $M$ remains stable, while $L(D_i|M)$ approaches zero (the model perfectly predicts the new data). 

Knowledge is reached when the `measured_bits` of the *corroborating data* vastly exceed the bit-length of the *model*, proving the model is an invariant feature of the block universe, not an artifact of the keyhole. Knowledge is the lock.

### 4. CONJECTURE-STUBS
A Conjecture-Stub is a structural prior. It is an uncollapsed node in a **Truth-Maintenance System (TMS) / Bayesian Network**.

**Design & Typing:**
A stub $S$ at coordinate $x$ is defined as the tuple: `[bounds, {H1, H2...Hn}, EIG]`
*   **Bounds:** The topological limit of the fuzz (e.g., "Democracy in 1850 was somewhere between Oligarchy and Republic"). 
*   **Hypotheses ($H_n$):** Mutually exclusive, falsifiable latch-points.
*   **Expected Information Gain (EIG):** The calculated reduction in entropy if a specific hypothesis is tested.

**Rendering:**
A stub CANNOT be rendered as a scalar point. It must be rendered using **Interval Arithmetic** or as a bounding box. Visually, it requires a "hollow" or "dithered" geometry. If you zoom in ($v$ increases), a fact yields detail; a stub yields empty space inside its bounds.

**Aiming (Optimal Experimental Design):**
The instrument uses **Active Learning**. It scans the compiled block for stubs, calculates the EIG for each, and aims the next keyhole burst $\theta_{next}$ at the coordinate/angle that maximizes:
`E[ Shannon_Entropy(Block_Current) - Shannon_Entropy(Block_Given_Probe(theta)) ]`
The instrument literally seeks out the most structural fuzz and fires at it.

### 5. THE BIGGEST RISK & THE ONE EXPERIMENT
**The Biggest Risk:** 
**Concept Drift vs. Dimensional Orthogonality.** In physical CT scans, the skull doesn't change meaning while you scan it. In latent space, "democracy" at `t_event=1800` and `t_event=2000` might not be different coordinates in the same dimensional space; the dimensions themselves might have rotated. If the latent axes are not globally orthogonal and invariant across the block universe, the Tomography math fails, and the compiler will hallucinate fake coherence (Procrustean forcing).

**The One Experiment (Latent Tomography of a Drifting Text):**
To prove this is machinery and not a metaphor, build a literal 2D computational toy. 
1.  **The Substrate:** Take a dataset of historical documents defining a highly contested concept (e.g., "Liberty").
2.  **The Keyholes:** Treat vector-database nearest-neighbor searches as "keyholes". Run a burst of searches restricted *only* to documents from 1800-1850, and another from 1950-2000. 
3.  **The Compilation:** Feed these projection vectors into a Radon transform/compressed sensing matrix.
4.  **The Test:** Ask the compiler to render the `t_event=1900` slice. 
5.  **The Verification:** Does the system produce an "Honest Stub"? If it outputs a blurry bounding box of vectors for 1900, which mathematically *contains* the true 1900 vector, and explicitly flags the internal variance as "unmeasured bits" (without linearly interpolating 1850 and 1950 into a fake, sharp 1900 point), the machinery works. 

If it just gives you a sharp, wrong average of 1850 and 1950, your compiler is leaking presentism, the COIN law is broken, and you have a metaphor.
