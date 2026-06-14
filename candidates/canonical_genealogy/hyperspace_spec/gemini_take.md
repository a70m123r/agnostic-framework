Warning: Windows 10 detected. Some UI features like smooth scrolling may be degraded. Windows 11 is recommended for the best experience.
Warning: True color (24-bit) support not detected. Using a terminal with true color enabled will result in a better visual experience.
I have analyzed your spec brief for the Hyperdimensional Canonical-Space Viewer. This is a profound architectural challenge that sits at the intersection of conformal geometry, rendering theory, and topological data analysis. 

Before we finalize a formal `.md` plan document, I want to present the mathematical foundations, address your core questions, and propose **two distinct architectural approaches** for your approval.

### Mathematical & Theoretical Foundations

**A. The 3D ↔ 2D Morph (The Dial)**
*   **The Math:** The morph from a sphere to a plane is elegantly modeled by applying the **Complex Logarithm** to the **Riemann Sphere**. If you project the sphere stereographically onto the complex plane ($Z$), taking the complex log ($W = \ln(Z)$) maps the punctured plane to a cylinder, which unrolls to the **Mercator projection**. Mercator is natively conformal (preserves local angles and shapes).
*   **The Smooth Dial:** In a vertex shader, this is a continuous homotopy. Let $t \in [0,1]$ be the dial. The position $P(t)$ interpolates between spherical coordinates $(r\cos\theta\cos\phi, r\sin\theta, r\cos\theta\sin\phi)$ and cylindrical/planar coordinates $(u, v, 0)$. 
*   **Papers/Implementations:** *Three.js* custom ShaderMaterials handling vertex interpolation; *d3-geo* transitions; mapbox-gl's recent globe-to-Mercator continuous morphs.

**B. The N-Layer Membrane Stack**
*   **The Math/Frameworks:** **Fiber Bundles** and **Sheaf Theory**. The physical domain acts as the "Base Manifold", and the latent dimensions act as "Fibers" attached to every point. Alternatively, **Multiplex Networks** mathematically model inter-layer vs. intra-layer edges.
*   **Representation:** "Above" is rendered as concentric, semi-transparent shells offset by the normal vector. "Within" is accessed via volumetric slicing or hyperbolic magnification (diving into a point expands it into a new sub-manifold).

**C. Overlap = Energy Exchange**
*   **Rendering:** Do not use literal wormholes. Model this as **Participating Media** / Volumetric Light Transport. When latent and physical coordinates align, they emit a coupling flux modeled as an overlapping kernel (e.g., a Dirac delta smoothed by a Gaussian variance). 
*   **Visual:** A glowing, raymarched column of flux perpendicular to the membrane stack.

**D. Substrate-as-Light-on-a-Sensor**
*   **The Math:** The **Rendering Equation** (Kajiya, 1986), inverted for information transport. 
*   **Implementations:** **3D Gaussian Splatting** (Kerbl et al., 2023). Facts are explicitly modeled as 3D Gaussians. 
*   **Solomonoff/MDL:** The covariance matrix (sharpness) of the Gaussian is strictly inversely proportional to the Shannon Entropy (bits of compression) of the fact. High certainty = sharp point; low certainty = diffuse, volumetric fog.

**E. Honest N-Dimensional Projection**
*   **The Math:** You cannot project $N > 3$ dimensions to 3D without distortion (Johnson-Lindenstrauss lemma). The most honest container for hierarchical latent data is **Hyperbolic Space** (e.g., Poincaré disk/half-space), where volume expands exponentially, matching decision trees.
*   **Honesty Risk Mitigation:** Explicit visual badging. If two points are rendered close in 3D but are distant in $N$-D, draw a high-tension "stress line" indicating projection distortion. 

---

### Proposed Buildable Approaches (Decision Required)

To proceed with drafting the final implementation spec, we need to choose the foundational architecture. Which of these aligns better with your constraints?

**Option 1: The Raymarched Unified Shader (Pure WebGL / twgl.js)**
*   **How it works:** A single full-screen HTML canvas running a heavy GLSL fragment shader. The globe, plane, and layers are mathematically evaluated via distance fields (SDFs) and raymarching.
*   **Pros:** Single-file delivery, pure mathematical continuity, handles volumetric light/energy exchange effortlessly.
*   **Cons/Risks:** Extremely high shader complexity; integrating discrete Gaussian Splatting data into a pure SDF raymarcher is computationally expensive.

**Option 2: The Three.js Scene Graph + Custom Materials (Recommended)**
*   **How it works:** Uses Three.js geometries for the base globe and membranes. The 3D-to-2D "Dial" is driven by a custom vertex shader interpolating the vertices. Substrate facts are injected as instanced 3D Gaussians.
*   **Pros:** Robust ecosystem, vastly easier to implement Gaussian Splatting, easier to handle camera controls and discrete DOM UI overlays (badges).
*   **Cons/Risks:** Slightly heavier dependency (Three.js), requires strict management of the rendering order to prevent Z-fighting and alpha-blending (OIT) artifacts between overlapping layers.

**How would you like to proceed?** Once you select an option (or suggest adjustments), I will formally draft the design spec to the `plans/` directory.
