# Framework Diagrams

Standalone SVG diagrams visualizing the Agnostic Framework's core structure. Each is self-contained — no external dependencies, no font loading, dark-theme matching the framework's site palette.

## Files

| File | Subject |
|------|---------|
| `01_compile_loop.svg` | The compile loop with A⁻ marked as primary discipline |
| `02_observer_architecture.svg` | Concentric layers: action-space → wrapper → harness → canon |
| `03_genotype_phenotype.svg` | Code vs render; what carriers actually transmit |
| `04_four_carrier_convergence.svg` | Aleph + MAMMAL + ANDI + Lippmann instantiating the same shape at four scales |
| `05_framework_overview.svg` | Map of canon primitives grouped into five regions, plus the three-lens callout |

## Design language

- **Background:** `#0a0a0a` (matches framework site)
- **Foreground text:** `#ececec`
- **Muted text:** `#8a8a8a`
- **Canon accent (load-bearing emphasis):** `#4ade80` (framework's canon green)
- **Border:** `#262626` (subtle), `#3a3a3a` (visible)

The canon green is used consistently to mark whatever the diagram identifies as load-bearing — A⁻ in the compile loop, Canon in the observer architecture, Phenotype in the genotype split, the convergence summary in the four-carrier diagram, A⁻ at the center of the overview map.

## Usage

- **Embed in HTML:** `<img src="diagrams/01_compile_loop.svg" alt="The compile loop">` — the SVGs render correctly on any page.
- **Light-context viewing (email, presentations on white slides):** the SVGs have a black background baked in; they read correctly on light surfaces because the dark frame defines its own visual context.
- **Modification:** SVG files are text; edit directly. The palette is uniform across all five — change one, change all.

## Provenance

Drafted 2026-05-18 in collaboration with Claude. The diagrams visualize claims from continuations 04 (observer/action-space), 06–07 (AU matrix), 13 (charge algebra), 14 (genotype/phenotype, slice-viewer), and 15 (A⁻ asymmetry refactor + four-carrier convergence). See `audits/v03.md` for the canon status of each primitive depicted.
