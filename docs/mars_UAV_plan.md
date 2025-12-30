# Mars UAV Feasibility Study - Implementation Plan

## Overview

Create a comprehensive Mars UAV feasibility study for a single configuration:
- **Battery-only minimal design** (~7.5 kg MTOW) optimized for simplicity and reliability

**Mission objectives**:
1. **Mapping**: Aerial reconnaissance and geological survey of the area around the habitat (camera payload)
2. **Telecommunication relay**: Extend communication range for surface operations (radio payload)

**Output**: `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\drone.md`

**References**: Collected in `Mars_UAV.bib` (exported from Zotero collection "Mars_UAV")

---

## 1. Document structure (drone.md)

```
1. Executive summary
2. Mission definition and environmental context
   2.1 Operational environment: Arcadia Planitia
   2.2 Mission profile
   2.3 Requirements definition (dual objectives: mapping + telecom relay)
3. Configuration trade-offs
   3.1 Reference Mars UAV designs (existing studies and proposals)
   3.2 Architecture comparison (rotorcraft, fixed-wing, hybrid VTOL)
   3.3 QuadPlane selection rationale
   3.4 Initial design hypotheses (derived from reference cases)
4. Atmospheric model
   4.1 Mars atmosphere equations
   4.2 Density, temperature, pressure profiles
5. Aerodynamic analysis
   5.1 Low-Reynolds regime characteristics
   5.2 Airfoil comparison (E387, S1223, S7055) using Selig wind tunnel data
   5.3 Airfoil selection (E387)
   5.4 Drag polar model and L/D estimation
6. Preliminary sizing methodology
   6.1 Matching chart adaptation for Mars
   6.2 Constraint equations (power-based)
   6.3 Weight estimation methodology
7. Preliminary design results
   7.1 Design point from matching chart
   7.2 Preliminary mass breakdown
   7.3 Preliminary power budget
   7.4 Estimated endurance and range
8. Component selection
   8.1 Selection criteria and trade-offs
   8.2 Propulsion (lift motors, cruise motor, propellers)
   8.3 Energy storage (batteries)
   8.4 Payload (camera, radio relay)
   8.5 Avionics and thermal control
   8.6 Ground infrastructure (solar panels for hangar)
9. Detailed design verification
   9.1 Updated mass breakdown with selected components
   9.2 Updated power budget
   9.3 Final performance (endurance, range, operational radius)
   9.4 Requirements compliance check
10. Infrastructure requirements
    10.1 Habitat hangar specifications
    10.2 Operations concept
11. Conclusions and recommendations
Appendices: A. Constants, B. Component datasheets, C. Script docs
```

---

## 2. Python script structure

Create `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\src\mars_uav_sizing\`:

| Module | Purpose |
|--------|---------|
| `atmosphere.py` | Mars atmospheric model (rho, T, p, a, mu vs altitude) |
| `aerodynamics.py` | Drag polar, L/D, Reynolds/Mach calculations |
| `airfoil_data.py` | Selig wind tunnel data for low-Re airfoils |
| `constraints.py` | Matching chart equations adapted for electric VTOL |
| `weights.py` | Weight estimation (Sadraey method adapted) |
| `endurance.py` | Battery energy and endurance calculations |
| `plotting.py` | Constraint diagrams, weight breakdowns |
| `run_sizing.py` | Main entry point |

---

## 3. Key calculations

### 3.1 Cruise power
Calculate using drag polar:
```
CL = 2W / (rho * V^2 * S)
CD = CD0 + CL^2 / (pi * AR * e)
P_cruise = 0.5 * rho * V^3 * S * CD / eta_prop
```
Add detailed power breakdown: P_propulsion + P_avionics + P_comms + P_payload + P_thermal

### 3.2 Aspect ratio trade-off
Parametric study AR = 5 to 14, evaluate:
- Structural weight penalty (Sadraey equation)
- Net L/D including structure
- Optimal AR for max endurance

### 3.3 Motor configuration
Adopt coaxial octocopter (8 lift motors) for single-motor failure tolerance.

---

## 4. Airfoil analysis

### XFOIL limitations
XFOIL does not converge reliably at Reynolds numbers around 50,000 due to laminar separation bubbles and transition phenomena. Attempts to use XFOIL for this analysis were unsuccessful.

### Data source: Selig wind tunnel data
Airfoil performance data is taken from the UIUC Low-Speed Airfoil Tests:
- **Reference**: Selig et al., "Summary of Low-Speed Airfoil Data" (Volumes 1-4)
- **Test conditions**: Re = 60,000 to 500,000, validated wind tunnel measurements
- **Advantage**: Experimental data captures real separation bubble behavior that XFOIL cannot model at low Re

**Candidates**: E387, S1223, S7055

**Mars Reynolds number** (c=0.58m, V=40m/s): Re ≈ 50,000–55,000

**Key metrics from Selig data**: CL_max, α_stall, (L/D)_max, CL at (L/D)_max

---

## 5. Design methodology (iterative process)

### Phase 1: Reference case study (Chapter 3)
Collect existing Mars UAV designs and proposals to derive initial hypotheses:
- **MTOW magnitude**: typical range for similar missions
- **Weight fractions**: structure, propulsion, energy, payload, avionics
- **Propeller sizing**: disk area, disk loading for VTOL in thin atmosphere
- **Wing parameters**: aspect ratio, wing loading ranges
- **Power requirements**: hover vs cruise power ratios

**Reference cases to collect**:
- NASA Ingenuity and follow-on concepts (Mars Helicopter, Mars Science Helicopter)
- Academic Mars UAV studies (e.g., Desert et al., Barbato et al.)
- VTOL/QuadPlane designs for low-density environments

### Phase 2: Preliminary sizing (Chapter 6-7)
Run matching chart with initial guesses → obtain preliminary design point:
- Wing area, span, aspect ratio
- Required power (hover, cruise)
- Preliminary mass breakdown by subsystem
- Estimated endurance and range

### Phase 3: Component selection (Chapter 8)
Use preliminary sizing results to select actual components from datasheets:

| Category | Components to select |
|----------|---------------------|
| Propulsion | Lift motors (×8), cruise motor, propellers |
| Energy | Batteries (flight), solar panels (hangar recharge) |
| Payload | Camera (mapping), radio transceiver (telecom relay) |
| Avionics | Flight computer, sensors, navigation |
| Thermal | Heaters, insulation |

### Phase 4: Verification (Chapter 9)
Recalculate with selected component data:
- Update mass breakdown with actual component masses
- Update power budget with actual efficiencies
- Verify requirements compliance (range, endurance, payload)

---

## 6. Source files

### Input files to read/adapt:
- `C:\Users\matti\OneDrivePhD\5.5 IELTS\progettazione\Profilo\matchingcharts.m` - sizing equations
- `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\intermediate\feasibility_b_v3.md` - minimal design analysis (basis for single configuration)
- `C:\Users\matti\OneDrivePhD\Dev\markdown_tools\docs\style_rules.txt` - formatting rules
- Selig et al. "Summary of Low-Speed Airfoil Data" - airfoil performance data

### Output files to create:
- `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\drone.md` - final report
- `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\src\mars_uav_sizing\*.py` - sizing scripts
- `C:\Users\matti\OneDrivePhD\Dev\Drone_marte\figures\*.png` - generated figures

---

## 7. References

References have been collected and exported to `Mars_UAV.bib` from the Zotero collection "Mars_UAV".

**Key references include**:
- Mars atmosphere and environment
- Low-Reynolds number aerodynamics
- Selig et al. "Summary of Low-Speed Airfoil Data" (experimental data at low Re)
- Mars rotorcraft and UAV design studies (Ingenuity, prior feasibility studies)
- Aircraft design methods (Sadraey, Roskam, Torenbeek)
- Electric propulsion and battery technology

The bibliography file is automatically linked in the manuscript front matter.

---

## 8. Implementation sequence

### Phase 1: Foundation
1. **Setup**: Create Python package structure with uv
2. **Atmosphere module**: Implement Mars atmospheric model
3. **Aerodynamics module**: Drag polar and L/D functions (using Selig data)
4. **Sizing engine**: Constraints, weights, endurance modules

### Phase 2: Reference study and initial hypotheses
5. **Literature review**: Collect reference Mars UAV designs from Zotero
6. **Extract parameters**: Tabulate MTOW, weight fractions, disk loading, etc.
7. **Formulate hypotheses**: Define initial guesses for matching chart

### Phase 3: Preliminary sizing
8. **Run matching chart**: Obtain preliminary design point
9. **Preliminary analysis**: Mass breakdown, power budget, endurance estimate

### Phase 4: Component selection and verification
10. **Collect datasheets**: Motors, batteries, cameras, radios, solar panels
11. **Select components**: Choose best-fit components based on preliminary sizing
12. **Final calculations**: Update design with actual component data
13. **Verification**: Check requirements compliance

### Phase 5: Documentation
14. **Write drone.md**: Document complete design process and results
15. **Cross-check**: Validate against literature and requirements

---

## 9. Style compliance checklist

- [ ] UTF-8 encoding
- [ ] Sentence case headings
- [ ] Asterisks (*) for bullet lists, tight (no blank lines)
- [ ] Cross-references: @fig:, @tbl:, @eq:
- [ ] Implicit citations only: [@author2024]
- [ ] Third-person objective voice
- [ ] No subjective adjectives (crucial, innovative, etc.)
- [ ] LaTeX for complex math, Unicode for simple symbols

### Content checklist
- [ ] Dual mission objectives clearly stated in requirements section
- [ ] Radio payload included in mass breakdown and power budget
- [ ] Reference UAV table with sources in Chapter 3
- [ ] Initial hypotheses clearly derived from reference cases
- [ ] Preliminary sizing results before component selection
- [ ] Component selection justified by preliminary sizing data
- [ ] Final verification shows requirements compliance
