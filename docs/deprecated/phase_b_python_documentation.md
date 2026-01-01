# Phase B: Python Implementation Documentation

## Overview

This document describes the Python analysis modules implemented for the Mars UAV feasibility study. These modules reproduce the equations from manuscript Sections 5.2–5.5 and generate the computed values that will update the manuscript in Phase C.

**Location:** `src/mars_uav_sizing/analysis/`

**Reference:** `docs/prompt_04_python_implementation.txt`

> **⚠️ CORRECTED 2025-12-28:** Parameters updated based on verification:
> - Air density: ρ = 0.0196 kg/m³ (was 0.0209)
> - Oswald efficiency: e = 0.869 for AR=6 (was 0.82)
> - Stall speed: V_stall = 29.2 m/s for W/S=10 N/m² (was 20 m/s)

---

## Module Structure

```
src/mars_uav_sizing/
├── analysis/
│   ├── __init__.py              # Package initialization
│   ├── rotorcraft_analysis.py   # §5.2 Rotorcraft configuration
│   ├── fixed_wing_analysis.py   # §5.3 Fixed-wing configuration
│   ├── hybrid_vtol_analysis.py  # §5.4 Hybrid VTOL (QuadPlane)
│   ├── comparative_analysis.py  # §5.5 Configuration comparison
│   ├── matching_chart.py        # §5.5 Constraint-based sizing
│   └── run_all_analyses.py      # Main runner script
└── data/
    └── baseline_parameters.yaml # Consolidated input parameters
```

---

## Running the Analyses

### Complete Analysis Suite

Run all analyses with a single command:

```bash
cd src
python -m mars_uav_sizing.analysis.run_all_analyses
```

This executes all analysis modules sequentially and produces a comprehensive summary with key values for manuscript update.

### Individual Modules

Each module can be run independently:

```bash
# Rotorcraft analysis (Section 5.2)
python -m mars_uav_sizing.analysis.rotorcraft_analysis

# Fixed-wing analysis (Section 5.3)
python -m mars_uav_sizing.analysis.fixed_wing_analysis

# Hybrid VTOL analysis (Section 5.4)
python -m mars_uav_sizing.analysis.hybrid_vtol_analysis

# Matching chart analysis (Section 5.5)
python -m mars_uav_sizing.analysis.matching_chart

# Comparative analysis (Section 5.5)
python -m mars_uav_sizing.analysis.comparative_analysis
```

### Programmatic Usage

```python
from mars_uav_sizing.analysis import (
    rotorcraft_feasibility_analysis,
    fixed_wing_feasibility_analysis,
    hybrid_vtol_feasibility,
    matching_chart_analysis,
    comparative_summary,
)

# Run with default parameters (MTOW = 10 kg)
rc_results = rotorcraft_feasibility_analysis()
fw_results = fixed_wing_feasibility_analysis()
hv_results = hybrid_vtol_feasibility()
mc_results = matching_chart_analysis()
summary = comparative_summary()

# Run with custom MTOW
results = rotorcraft_feasibility_analysis(mtow_kg=8.0)
```

---

## Input Parameters

All input parameters are consolidated in `data/baseline_parameters.yaml` and sourced from verified manuscript sections.

### Physical Constants (§3.1)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Mars gravity | $g$ | 3.711 | m/s² | NASA Mars Fact Sheet |
| Air density (Arcadia) | $\rho$ | **0.0196** | kg/m³ | Atmospheric model (CORRECTED) |
| Dynamic viscosity | $\mu$ | 1.08×10⁻⁵ | Pa·s | §4.12 |

### Propulsion Efficiencies (§4.5)

| Parameter | Symbol | Value | Range | Source |
|-----------|--------|-------|-------|--------|
| Figure of merit | FM | 0.40 | 0.30–0.50 | Leishman (MAV data) |
| Propeller efficiency | $\eta_\text{prop}$ | 0.55 | 0.45–0.65 | Sadraey 2020 |
| Motor efficiency | $\eta_\text{motor}$ | 0.85 | 0.82–0.90 | Industry typical |
| ESC efficiency | $\eta_\text{ESC}$ | 0.95 | 0.93–0.98 | Industry typical |

**Derived combined efficiencies:**
- $\eta_\text{hover} = FM \times \eta_\text{motor} \times \eta_\text{ESC} = 0.323$
- $\eta_\text{cruise} = \eta_\text{prop} \times \eta_\text{motor} \times \eta_\text{ESC} = 0.444$

### Battery Parameters (§4.6, §4.11)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Specific energy | $e_\text{spec}$ | 270 | Wh/kg | Solid-state Li-ion |
| Depth of discharge | DoD | 0.80 | — | Cycle life |
| Discharge efficiency | $\eta_\text{batt}$ | 0.95 | — | Industry typical |
| Energy reserve | — | 0.20 | — | Mission profile |

### Mass Fractions (§4.11)

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Battery fraction | $f_\text{batt}$ | 0.35 | Reference UAV data |
| Empty fraction | $f_\text{empty}$ | 0.30 | Reference UAV data |
| Payload fraction | $f_\text{payload}$ | 0.10 | Reference UAV data |
| Propulsion fraction | $f_\text{prop}$ | 0.20 | Dual system |
| Avionics fraction | $f_\text{avionics}$ | 0.05 | Standard |
| **Baseline MTOW** | — | **10.0 kg** | Computed |

### Aerodynamic Parameters (§4.7)

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Aspect ratio | AR | 6 | Mars precedents |
| Oswald efficiency | $e$ | **0.869** | Sadraey correlation (CORRECTED) |
| Zero-lift drag | $C_{D,0}$ | 0.030 | Equivalent friction |
| Max lift coefficient | $C_{L,\text{max}}$ | 1.20 | UIUC Vol. 1 (E387) |
| Rotorcraft L/D | $(L/D)_\text{eff}$ | 4.0 | Leishman |

**Derived values (CORRECTED):**
- Induced drag factor: $K = 1/(\pi \cdot AR \cdot e) = 0.0612$
- Maximum L/D: $(L/D)_\text{max} = 0.5\sqrt{\pi \cdot AR \cdot e / C_{D,0}} = 11.7$
- Optimal $C_L$: $C_L^* = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = 0.70$

### Mission Parameters (§4.12)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Cruise velocity | $V_\text{cruise}$ | 40 | m/s | Mach/Re constraints |
| Stall velocity (W/S=10) | $V_\text{stall}$ | **29.2** | m/s | CORRECTED |
| Hover time | $t_\text{hover}$ | 180 | s | Mission profile |
| Cruise time | $t_\text{cruise}$ | 57 | min | 50 km radius |
| Disk loading | DL | 30 | N/m² | Design choice |

---

## Module Descriptions

### 1. Rotorcraft Analysis (`rotorcraft_analysis.py`)

**Manuscript section:** §5.2 Rotorcraft Configuration

**Key equations implemented:**

| Equation | Reference | Description |
|----------|-----------|-------------|
| $v_i = \sqrt{T/(2\rho A)}$ | @eq:induced-velocity | Induced velocity (momentum theory) |
| $P_\text{ideal} = W^{1.5}/\sqrt{2\rho A}$ | @eq:ideal-power | Ideal hover power |
| $P_\text{hover} = P_\text{ideal}/FM$ | @eq:hover-power | Actual hover power |
| $P_\text{elec} = P_\text{hover}/(\eta_m \eta_\text{ESC})$ | @eq:electric-hover-full | Electrical hover power |
| $P/W = (1/\eta_\text{hover})\sqrt{DL/(2\rho)}$ | @eq:hover-constraint | Hover constraint |
| $P_\text{fwd} = WV/(L/D)_\text{eff}$ | @eq:forward-power-ld | Forward flight power |

**Key functions:**
- `induced_velocity()` — Momentum theory induced velocity
- `ideal_hover_power()` — Theoretical minimum hover power
- `actual_hover_power()` — Hover power with figure of merit
- `electric_hover_power()` — Electrical power from battery
- `hover_power_loading()` — P/W for matching chart
- `forward_flight_power()` — Forward flight mechanical power
- `rotorcraft_feasibility_analysis()` — Complete analysis
- `print_rotorcraft_analysis()` — Formatted output

**Output (CORRECTED):**
```
Hover power: 3178 W
Cruise power: 460 W
Induced velocity: 27.7 m/s
Endurance: 57 min (-5% margin)
Result: FAILS (insufficient margin)
```

---

### 2. Fixed-Wing Analysis (`fixed_wing_analysis.py`)

**Manuscript section:** §5.3 Fixed-Wing Configuration

**Key equations implemented:**

| Equation | Reference | Description |
|----------|-----------|-------------|
| $C_L = 2(W/S)/(\rho V^2)$ | @eq:cl-required | Required lift coefficient |
| $C_D = C_{D,0} + C_L^2/(\pi \cdot AR \cdot e)$ | @eq:drag-polar | Parabolic drag polar |
| $(L/D)_\text{max} = 0.5\sqrt{\pi \cdot AR \cdot e / C_{D,0}}$ | @eq:ld-max | Maximum L/D |
| $C_L^* = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}}$ | @eq:cl-optimal | Optimal lift coefficient |
| $P = WV/(L/D \cdot \eta_\text{cruise})$ | @eq:cruise-electric-power | Cruise power |
| $V_\text{stall} = \sqrt{2(W/S)/(\rho C_{L,\text{max}})}$ | @eq:stall-speed | Stall speed |

**Key functions:**
- `cruise_lift_coefficient()` — C_L for level flight
- `drag_coefficient()` — C_D from drag polar
- `maximum_ld()` — (L/D)_max and C_L*
- `cruise_power()` — Electrical cruise power
- `stall_speed()` — Stall speed from W/S
- `takeoff_ground_roll()` — Takeoff distance
- `fixed_wing_feasibility_analysis()` — Complete analysis
- `print_fixed_wing_analysis()` — Formatted output

**Output (CORRECTED):**
```
(L/D)_max: 11.7
C_L*: 0.70
Cruise power: 286 W
Endurance: 121 min
Takeoff roll: 525 m
Result: FAILS (no VTOL capability)
```

---

### 3. Hybrid VTOL Analysis (`hybrid_vtol_analysis.py`)

**Manuscript section:** §5.4 Hybrid VTOL (QuadPlane) Configuration

**Key equations implemented:**

| Equation | Reference | Description |
|----------|-----------|-------------|
| $P_\text{hover,QP} = P_\text{hover,rotor}$ | @eq:electric-hover-qp | Hover (same as rotorcraft) |
| $P_\text{cruise,QP} = WV/(L/D_\text{QP} \cdot \eta_\text{cruise})$ | @eq:cruise-power-qp | Cruise with L/D penalty |
| $E_\text{req} = E_\text{hover} + E_\text{cruise} + E_\text{reserve}$ | @eq:energy-budget | Energy budget |
| $m_\text{batt} = E_\text{total}/(e_\text{spec} \cdot DoD \cdot \eta)$ | @eq:battery-requirement | Battery mass |
| $E_\text{avail} = f_\text{batt} \cdot MTOW \cdot e_\text{spec} \cdot DoD \cdot \eta$ | @eq:energy-available | Available energy |

**Key functions:**
- `hybrid_hover_power()` — Hover power (from rotorcraft)
- `hybrid_cruise_power()` — Cruise power with L/D penalty
- `energy_budget()` — Mission energy breakdown
- `required_battery_mass()` — Minimum battery for mission
- `available_energy()` — Energy from battery allocation
- `hybrid_vtol_feasibility()` — Complete analysis
- `print_hybrid_vtol_analysis()` — Formatted output

**Output (CORRECTED):**
```
Hover power: 3178 W
Cruise power: 318 W
QuadPlane L/D: 10.5 (90% of pure wing)
Energy margin: 30%
Endurance: 91 min (+52% margin)
Range: 212 km
Result: PASSES (all requirements met)
```

---

### 4. Matching Chart Analysis (`matching_chart.py`)

**Manuscript section:** §5.5 Comparative Results (Matching Chart)

**Key equations implemented:**

| Equation | Reference | Description |
|----------|-----------|-------------|
| $(P/W)_\text{hover} = (1/\eta_\text{hover})\sqrt{DL/(2\rho)}$ | @eq:hover-constraint-qp | Hover constraint (horizontal) |
| $(W/S)_\text{max} = 0.5\rho V_\text{stall}^2 C_{L,\text{max}}$ | @eq:stall-constraint | Stall constraint (vertical) |
| $(P/W)_\text{cruise} = V/(L/D \cdot \eta_\text{cruise})$ | @eq:cruise-constraint | Cruise constraint (curve) |

**Key functions:**
- `hover_constraint()` — P/W for hover (horizontal line)
- `stall_constraint()` — Max W/S from stall (vertical line)
- `cruise_constraint()` — P/W for cruise at given W/S
- `cruise_constraint_curve()` — Cruise P/W over W/S range
- `minimum_power_point()` — W/S at (L/D)_max
- `find_design_point()` — Optimal design point
- `matching_chart_analysis()` — Complete analysis
- `print_matching_chart_analysis()` — Formatted output

**Output (CORRECTED):**
```
Hover constraint: P/W = 85.6 W/N (horizontal)
Stall constraint: W/S = 7.3 N/m² (vertical)
Optimal cruise: W/S = 11.0 N/m²
Design point: W/S = 7.3 N/m², P/W = 85.6 W/N
Active constraint: HOVER (dominates)
Wing area: 5.0 m²
Wingspan: 5.5 m
Installed power: 3178 W
```

---

### 5. Comparative Analysis (`comparative_analysis.py`)

**Manuscript section:** §5.5 Comparative Results

**Key functions:**
- `run_all_analyses()` — Execute all three configurations
- `create_comparison_table()` — Format comparison data
- `configuration_ranking()` — Rank by capability
- `elimination_rationale()` — Explain eliminations
- `comparative_summary()` — Complete comparison
- `print_comparative_analysis()` — Formatted output

**Output (CORRECTED):**
```
Configuration Comparison:
                    Rotorcraft   Fixed-Wing   Hybrid VTOL
L/D (effective)          4.0         11.7          10.5
Hover power (W)         3178          N/A          3178
Cruise power (W)         460          286           318
Endurance (min)           57          121            91
Range (km)               130          289           212
Endurance margin (%)      -5         +101           +52
VTOL capable             Yes           No           Yes
Feasible                  No           No           Yes

Recommendation: HYBRID VTOL
```

---

## Key Results Summary

### Computed Values for Manuscript Update (Phase C) — CORRECTED

| Parameter | Rotorcraft | Fixed-Wing | Hybrid VTOL | Unit |
|-----------|------------|------------|-------------|------|
| Hover power | 3178 | N/A | 3178 | W |
| Cruise power | 460 | 286 | 318 | W |
| Effective L/D | 4.0 | 11.7 | 10.5 | — |
| Endurance | 57 | 121 | 91 | min |
| Endurance margin | -5 | +101 | +52 | % |
| Range | 130 | 289 | 212 | km |
| VTOL capable | Yes | No | Yes | — |
| **Feasible** | **No** | **No** | **Yes** | — |

### Design Point (from Matching Chart) — CORRECTED

| Parameter | Value | Unit |
|-----------|-------|------|
| Design wing loading | 7.3 | N/m² |
| Design power loading | 85.6 | W/N |
| Wing area | 5.0 | m² |
| Wingspan | 5.5 | m |
| Mean chord | 0.92 | m |
| Installed power | 3178 | W |
| Active constraint | Hover | — |

### Recommendation

**Selected configuration: Hybrid VTOL (QuadPlane)**

Rationale:
1. **VTOL requirement met** — Fixed-wing eliminated (525 m takeoff roll impractical)
2. **Adequate endurance margin** — Rotorcraft eliminated (-5% margin too thin)
3. **Substantial safety margins** — Energy margin 30%, endurance margin 52%
4. **Achievable range** — 212 km (112% above requirement)

---

## Equation Traceability

All implemented equations are traced to manuscript sections via docstrings:

```python
def induced_velocity(thrust_n: float, rho: float, disk_area_m2: float) -> float:
    """Calculate induced velocity from momentum theory.
    
    Implements @eq:induced-velocity from §5.2:
        v_i = sqrt(T / (2ρA))
    
    Reference: Leishman (2006), Eq. 2.15
    ...
    """
```

Each function includes:
- **Equation reference** — Manuscript equation number
- **Section reference** — Manuscript section
- **Source reference** — Original literature source
- **Parameter descriptions** — Units and meanings
- **Return value** — Units and meaning

---

## Dependencies

- Python 3.11+
- NumPy (for arrays in matching chart)
- Standard library only (math, typing, datetime)

No external packages required beyond NumPy.

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-28 | 1.0 | Initial Phase B implementation |
| 2025-12-28 | 1.1 | CORRECTED: ρ=0.0196, e=0.869, V_stall recalculated |

---

## Next Steps (Phase C)

1. Update manuscript placeholders with computed values
2. Generate matching chart figure from `matching_chart.py` data
3. Verify all numerical results match code output
4. Update source_grounding.txt with code references
