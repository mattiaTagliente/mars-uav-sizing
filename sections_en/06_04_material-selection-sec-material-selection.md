# Design decisions

## Material selection {#sec:material-selection}

This section presents the material selection rationale and structural design approach for the Mars UAV, addressing thermal, mechanical, and mass requirements. The selection builds on the trade-off analysis in @sec:materials-data.

### Primary structural material

Carbon fiber reinforced polymer (CFRP) is selected as the primary structural material, consistent with Ingenuity heritage and commercial practice.

CFRP exhibits low thermal expansion (CTE approximately 0.5 ppm/°C), minimising thermal stress from the −80°C to +20°C diurnal temperature cycle on Mars. It provides the highest strength-to-weight ratio of commonly available structural materials, supporting the mass minimisation critical for Mars flight. The Ingenuity helicopter successfully demonstrated CFRP construction on Mars, using TeXtreme spread tow carbon fabrics selected for resistance to thermal cycling microcracking [@latourabOxeonPartOwnedHoldings2025]<!-- #s:textreme -->.

### Structural element materials

| Component | Material | Construction | Rationale |
|:----------|:---------|:-------------|:----------|
| Wing skins | CFRP | Foam-core sandwich | High stiffness-to-weight |
| Fuselage skins | CFRP | Foam-core sandwich | High stiffness-to-weight |
| Wing spar | CFRP | Tube or I-beam | Bending load path |
| Lift motor booms | CFRP | Filament-wound tube | Torsion and bending |
| Tail support booms | CFRP | Pultruded tube | Low mass, high stiffness |
| Landing gear | GFRP | Laminate | Impact tolerance |
| Leading edges | GFRP | Laminate | Erosion resistance |

: Structural materials by component {#tbl:material-selection}

Wing and fuselage skins use foam-core sandwich construction with carbon fiber face sheets, providing high stiffness-to-weight for primary aerodynamic surfaces. The lift motor and tail support booms are carbon fiber tubes, either filament-wound or pultruded. Fiberglass reinforcement (GFRP) is used at landing gear attachment points and vulnerable leading edges for impact tolerance.

### Thermal management materials

Internal thermal management employs gold-plated interior surfaces or multi-layer insulation (MLI) for electronics compartment thermal control, following Ingenuity practice. The low thermal conductivity of CFRP aids passive thermal isolation of the electronics bay from the external environment.

### Mass fraction implications

The selection of CFRP and advanced composite construction techniques affects the structural mass fraction used in weight estimation (@sec:mass-breakdown). Based on Ingenuity heritage and commercial UAV data:

| Parameter | Aluminium baseline | CFRP composite | Reduction |
|:----------|-------------------:|---------------:|----------:|
| Specific strength (MPa·m³/kg) | 110 | 450 | N/A |
| Structural mass fraction | 0.35–0.40 | 0.25–0.30 | 25–30% |
| Wing density factor, $K_\rho$ | 1.0 | 0.50–0.60 | 40–50% |

: Material properties comparison {#tbl:material-comparison}

The weight estimation equations in @sec:mass-breakdown apply CFRP-adjusted density factors to account for the composite construction. Conservative estimates are used given the limited flight heritage data for Mars composite structures.
