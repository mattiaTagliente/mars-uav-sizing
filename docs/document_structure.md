# Mars UAV Feasibility Study - Document Structure
# Last Updated: 2026-01-01 (Manuscript complete: propeller sizing, tail sizing, mass breakdown)

## Overview

This document defines the authoritative structure of the Mars UAV feasibility study manuscript. It reflects the current state after the following key decisions:
- **Airfoil selection**: SD8000 (replaced E387)
- **Baseline MTOW**: 10.00 kg
- **Selected architecture**: QuadPlane (hybrid VTOL with octocopter lift system)

---

## Current Manuscript Structure

```
0. Title, Abstract, Keywords
   - Mars UAV feasibility study abstract
   - Keywords: Mars, UAV, QuadPlane, low Reynolds, SD8000

1. Introduction
   - Project motivation and scope
   - Manuscript organization

2. Design methodology
   2.1 Iterative sizing approach
   2.2 Role of constraint-based sizing

3. Mission analysis
   3.1 Operational environment (Arcadia Planitia, atmosphere model)
   3.2 Mission profile
   3.3 User needs and requirements

4. Reference data and trade-off analysis
   4.1 Payload systems (camera, radio relay)
   4.2 Architecture comparison (rotorcraft, fixed-wing, hybrid VTOL)
   4.3 Mars UAV concepts (Ingenuity, ARES, Mars Science Helicopter)
   4.4 Commercial VTOL benchmarks
   4.5 Propulsion characteristics
   4.6 Energy storage characteristics
   4.7 Aerodynamic analysis and airfoil data
   4.8 Fuselage geometry data
   4.9 Tail configurations
   4.10 Structural materials
   4.11 Initial mass estimate
   4.12 Derived requirements

5. Constraint analysis
   5.1 Rotorcraft configuration
       - Hover power equation
       - Forward flight power
       - Energy budget
       - Feasibility assessment: MARGINAL PASS (+5% margin)
   5.2 Fixed-wing configuration
       - Cruise power equation
       - Stall constraint
       - Takeoff analysis
       - Feasibility assessment: FAIL (no runway)
   5.3 Hybrid VTOL configuration (QuadPlane)
       - Hover constraint (lift rotors)
       - Cruise constraint (wing + cruise propeller)
       - Transition energy analysis
       - Energy budget with 20% reserve
       - Feasibility assessment: PASS (+49% margin)
   5.4 Matching chart methodology and comparative results
       - Matching chart fundamentals
       - Constraint line derivations
       - Configuration-specific charts
       - Baseline design point determination

6. Design decisions
   6.1 Architecture selection
       - Configuration comparison table
       - Elimination rationale (rotorcraft, fixed-wing)
       - QuadPlane selection (with octocopter lift + coaxial cruise)
       - Design point summary
   6.2 Airfoil selection ★ (SD8000)
        - Airfoil comparison (tier-based evaluation of all 7 candidates)
        - Tier 1: E387, SD8000, S7055 (highest efficiency)
        - Tier 2: SD7037B, AG455ct-02r (moderate efficiency)
        - Tier 3: AG12, AG35-r (reflexed, for flying wings)
        - E387 vs SD8000 detailed analysis
        - SD8000 rationale: larger stall margin (4.6°), no LSB transitions
   6.3 Geometry selection
       - Wing geometry (S=2.686 m², b=4.01 m, c=0.669 m, AR=6)
       - Tail configuration (boom-mounted inverted V-tail, 1.144 m², 40° dihedral)
       - Fuselage geometry (L_f=1.20 m, D_f=0.20 m, fineness=6)
       - Total aircraft length (L_total=2.25 m, boom extension 1.05 m)
       - Propeller sizing (lift: 0.36 m, cruise: 0.31 m)
   6.4 Material selection
       - CFRP for primary structure
       - Justification for Mars conditions
   6.5 Mass breakdown
       - Preliminary mass allocation
       - Subsystem weight estimates

7. Component selection and verification
   7.1 Selection methodology
        - Requirements from constraint analysis
        - Mass budget constraints
        - Selection criteria
   7.2 Propulsion system selection
        7.2.1 Lift motors (octocopter configuration)
        7.2.2 Cruise motors (coaxial tractor)
        7.2.3 Lift propellers
        7.2.4 Cruise propellers
   7.3 Payload selection
        7.3.1 Camera selection (mapping payload)
        7.3.2 Radio selection (telecommunication relay payload)
   7.4 Energy storage selection
        - Battery specifications
   7.5 Performance verification
        - Updated calculations with selected components
        - Requirements compliance check

8. Infrastructure requirements
   8.1 Habitat hangar specifications
        - UAV dimensional envelope
        - Hangar zones (storage bay, airlock, external platform)
        - Airlock: 6 × 3 m (matches storage bay width for full wingspan)
        - Dust removal: pressurised air jets (CO₂)
        - Charging infrastructure (1000 W charger)
        - Solar power system
            - Mars solar irradiance analysis
            - Solar cell selection (SolAero IMM-α selected)
            - Panel sizing (2.0 m²)
            - Buffer battery storage (1260 Wh)
   8.2 Operations concept
        - Mission phases and timeline
        - Crew roles
        - Operational tempo
        - Contingency operations
        - Maintenance schedule

9. Conclusions and recommendations
   9.1 Summary of findings
   9.2 Recommendations
   9.3 Future work
       9.3.1 Sizing methodology improvements
           - Configuration-specific coupled closures
           - Component-based mass model
           - Configuration-appropriate constraint diagrams
       9.3.2 Subsystem analyses
           - Avionics system design
           - Thermal management analysis
           - Structural analysis and detailed design

10. References

Appendices:
   A. Physical constants and parameters
   B. Component datasheets
   C. Sizing script documentation
   D. Atmospheric model derivation
```

---

## Key Design Parameters (Current Baseline)

| Parameter | Value | Source |
|-----------|-------|--------|
| MTOW | 10.00 kg | §4.11 Initial mass estimate |
| Weight on Mars | 37.11 N | W = MTOW × g_Mars |
| Cruise velocity | 40.0 m/s | §4.12 Derived requirements |
| Design Reynolds | ~55,000 | §4.7 Aerodynamic analysis |
| Atmospheric density | 0.0196 kg/m³ | §3.1 Operational environment |

### Airfoil Selection ★ (Updated)

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Selected airfoil** | SD8000 | §6.2 Airfoil selection |
| CL_max | 1.15 | UIUC wind tunnel data |
| Thickness ratio (t/c) | 8.9% | - |
| Cd_min | 0.0142 | At Re = 60,000 |
| Stall margin | 4.6° | α_stall - α_design |

**Selection rationale**: SD8000 provides more consistent drag behavior without laminar separation bubble (LSB) transitions, and a larger stall margin compared to E387. This is critical for the unpredictable Mars atmospheric conditions.

### Wing Geometry (Derived from Matching Chart)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Wing loading (W/S) | 13.82 N/m² | Stall constraint at V_min=35.04 m/s |
| Wing area (S) | 2.686 m² | S = W/(W/S) |
| Wingspan (b) | 4.01 m | b = √(AR × S) |
| Mean chord (c) | 0.669 m | c = S/b |
| Aspect ratio (AR) | 6 | Design choice |

### Performance Summary

| Configuration | Endurance | Range | Margin | Status |
|---------------|-----------|-------|--------|--------|
| Rotorcraft | 63.2 min | 147 km | +5.3% | NOT RECOMMENDED |
| Fixed-wing | 120.5 min | 289 km | +101% | NOT FEASIBLE (runway) |
| **QuadPlane** | **89.6 min** | **208 km** | **+49%** | **SELECTED** |

---

## Files Organization

### Manuscript Sections (English)
Location: `sections_en/`

| File | Content |
|------|---------|
| 00_title_abstract_keywords.md | Front matter |
| 01_00_introduction.md | Introduction |
| 02_00_design-methodology.md | Section 2 header |
| 02_01_*.md, 02_02_*.md | Section 2 subsections |
| 03_00_mission-analysis.md | Section 3 header |
| 03_01_*.md - 03_03_*.md | Section 3 subsections |
| 04_00_reference-data-*.md | Section 4 header |
| 04_01_*.md - 04_12_*.md | Section 4 subsections |
| 05_00_constraint-analysis-*.md | Section 5 header |
| 05_01_*.md - 05_04_*.md | Section 5 subsections |
| 06_00_design-decisions-*.md | Section 6 header |
| 06_01_*.md - 06_05_*.md | Section 6 subsections |
| 07_00_component-selection-*.md | Section 7 header |
| 07_01_*.md - 07_05_*.md | Section 7 subsections (methodology, propulsion, payload, energy, verification) |
| 08_00_infrastructure-*.md | Section 8 header |
| 08_01_*.md, 08_02_*.md | Section 8 subsections |
| 09_00_conclusions-*.md | Section 9 header |
| 09_01_*.md - 09_03_*.md | Section 9 subsections (summary, recommendations, future work) |
| 10_00_references.md | Bibliography |
| 11_00_appendix-a-*.md | Appendix A header |
| 11_01_*.md | Appendix A content (physical constants tables) |
| 12_00_appendix-b-*.md | Appendix B header |
| 12_01_*.md - 12_03_*.md | Appendix B subsections (propulsion, payload, energy storage) |
| 13_00_appendix-c-*.md | Appendix C header |
| 13_01_*.md | Appendix C content (package documentation) |
| 14_00_appendix-d-*.md | Appendix D header |
| 14_01_*.md | Appendix D content (model derivation) |
| 15_00_*.md | Example usage |

### Manuscript Sections (Italian)
Location: `sections_it/`
- Parallel structure to English with translated content
- Same numbering scheme

### Configuration Files
Location: `src/mars_uav_sizing/config/`

| File | Content |
|------|---------|
| aerodynamic_parameters.yaml | Wing geometry, drag polar, **airfoil (SD8000)** |
| atmospheric_parameters.yaml | Mars atmosphere model |
| battery_parameters.yaml | Energy storage specs |
| mission_parameters.yaml | Mission requirements |
| propulsion_parameters.yaml | Motor and propeller specs |

---

## Recent Changes (2025-12-31)

### Airfoil Change: E387 → SD8000

**Rationale**: The SD8000 airfoil was selected over the E387 due to:
1. **Larger stall margin**: 4.6° vs 1.3° (3.5× improvement)
2. **Consistent drag behavior**: No LSB collapse transition
3. **Lower Cd_min**: 0.0142 vs 0.0228 at operating Re
4. **Purpose-designed**: SD8000 is optimized for Re = 60,000 regime

**Cascading Changes**:
All values derived from CL_max were updated:
- CL_max: 1.20 → 1.15 (-4.2%)
- Max W/S: 14.42 → 13.82 N/m² (-4.2%)
- Wing area: 2.574 → 2.686 m² (+4.4%)
- Wingspan: 3.93 → 4.01 m (+2.0%)
- Mean chord: 0.655 → 0.669 m (+2.1%)

**Files Modified**:
- sections_en/04_07_*, 04_12_*
- sections_en/05_02_*, 05_04_*
- sections_en/06_01_*, 06_02_*, 06_03_*, 06_05_*
- sections_en/00_*, 09_00_*
- Corresponding Italian files in sections_it/
- src/mars_uav_sizing/config/aerodynamic_parameters.yaml
- source_grounding.txt

---

## Sections Status

| Section | English | Italian | Content Status |
|---------|---------|---------|----------------|
| 0 Abstract | ✅ | ✅ | Complete (SD8000 updated) |
| 1 Introduction | ✅ | ✅ | Complete |
| 2 Methodology | ✅ | ✅ | Complete |
| 3 Mission | ✅ | ✅ | Complete |
| 4 Reference Data | ✅ | ✅ | Complete (SD8000 updated) |
| 5 Constraint Analysis | ✅ | ✅ | Complete (geometry updated) |
| 6 Design Decisions | ✅ | ✅ | Complete (SD8000 selection) |
| 7 Component Selection | ✅ | ✅ | Complete (7.1-7.4 added 2026-01-01) |
| 8 Infrastructure | ✅ | ✅ | Complete (expanded 2026-01-01) |
| 9 Conclusions | ✅ | ✅ | Complete (SD8000 updated) |
| Appendices | ✅ | ✅ | Complete (A-D expanded 2026-01-01) |

Legend: ✅ Complete | ⚠️ Partial/Placeholder | ❌ Not started

---

## Build Process

1. **Edit sections**: Modify files in `sections_en/` or `sections_it/`
2. **Reconstruct**: Run `reconstruct.bat` to merge sections into `drone.md` / `drone_it.md`
3. **Build DOCX**: Run `build_docx.bat` to generate Word documents
4. **Verify**: Check `build_docx.log` for errors/warnings

---

## Codebase Structure

Location: `src/mars_uav_sizing/`

```
mars_uav_sizing/
├── __init__.py
├── config/                 # YAML configuration files
│   ├── aerodynamic_parameters.yaml  ★ (SD8000 airfoil)
│   ├── atmospheric_parameters.yaml
│   ├── battery_parameters.yaml
│   ├── mission_parameters.yaml
│   └── propulsion_parameters.yaml
├── core/                   # Core physics modules
│   ├── atmosphere.py
│   ├── aerodynamics.py
│   ├── airfoil_data.py
│   └── energy.py           # Shared energy accounting helper
├── section4/               # Section 4 calculations
│   ├── derived_requirements.py
│   └── initial_mass.py
├── section5/               # Section 5 constraint analysis
│   ├── rotorcraft.py
│   ├── fixed_wing.py
│   ├── hybrid_vtol.py
│   ├── matching_chart.py
│   └── comparative.py
├── section6/               # Section 6 design decisions
│   ├── airfoil_selection.py
│   ├── airfoil_plots.py
│   ├── propeller_sizing.py  # Lift and cruise propeller sizing
│   └── tail_sizing.py       # V-tail geometry sizing
├── section7/               # Section 7 component verification
│   ├── component_selection.py  # Motor and ESC selection
│   └── mass_breakdown.py       # Detailed mass accounting
├── visualization/          # Plotting modules
│   └── figures.py
└── run_analysis.py         # Main entry point
```

---

## Cross-Reference Labels

Key labels used for cross-references in the manuscript:

### Sections
- `@sec:introduction`
- `@sec:iterative-sizing`, `@sec:constraint-role`
- `@sec:operational-environment`, `@sec:mission-profile`, `@sec:user-needs`
- `@sec:constraint-analysis`, `@sec:rotorcraft-analysis`, `@sec:fixed-wing-analysis`
- `@sec:hybrid-vtol-analysis`, `@sec:comparative-results`
- `@sec:design-decisions`, `@sec:architecture-selection`, `@sec:airfoil-selection`
- `@sec:geometry-selection`, `@sec:propeller-sizing`, `@sec:material-selection`, `@sec:mass-breakdown`
- `@sec:component-verification`, `@sec:selection-methodology`, `@sec:propulsion-selection`, `@sec:payload-selection`
- `@sec:habitat-hangar`, `@sec:operations-concept`
- `@sec:conclusions`, `@sec:summary-findings`, `@sec:recommendations`, `@sec:future-work`

### Key Tables
- `@tbl:requirements-summary`
- `@tbl:aero-coefficients`
- `@tbl:airfoil-comparison`
- `@tbl:quadplane-design-point`
- `@tbl:wing-geometry`, `@tbl:vtail-geometry`, `@tbl:fuselage-geometry`, `@tbl:propeller-summary`
- `@tbl:design-point`, `@tbl:design-parameters`
- `@tbl:quadplane-mass-breakdown`, `@tbl:mass-fraction-verification`
- `@tbl:uav-envelope`, `@tbl:pressurised-bay`, `@tbl:airlock-specs`, `@tbl:platform-specs`
- `@tbl:mars-irradiance`, `@tbl:solar-cell-comparison`, `@tbl:buffer-battery`, `@tbl:solar-spec`

### Key Figures
- `@fig:matching-chart`
- `@fig:ld-comparison`
- `@fig:power-comparison`
- `@fig:endurance-comparison`
- `@fig:energy-budget`
- `@fig:hangar-schematic`

### Key Equations
- `@eq:hover-power`
- `@eq:cruise-power`
- `@eq:stall-constraint`
- `@eq:v-min-constraint`
- `@eq:wing-loading-constraint`
