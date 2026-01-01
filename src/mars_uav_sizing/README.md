# Mars UAV Sizing Package

**Version 0.2.0** - Fully restructured with section-based organization.

---

## User Requirements

> *"Your task is now to carefully assess the codebase and restructure it. The problem is that several scripts have been developed in different moments, so we have outdated scripts and updated scripts but with hardcoded values. First of all, identify and delete the outdated and useless scripts. Then, update the scripts still valid by removing ALL the hardcoded values and saving them instead in external .yaml file. You must make sure that the equations and numbers coincide between the manuscripts and the configuration file and the scripts. The idea is to separate the scripts based on sections and functions: we will have scripts for the calculations needed in section 2 and these will be divided logically, then the same for section 3 etc. All the script must provide clear console output and be written in a way that is easy to understand and follow by a human reader."*

### Design Principles

1. **No hardcoded values** - ALL numerical parameters load from YAML config files
2. **Section-based organization** - Scripts organized by manuscript section (§3, §4, §5)
3. **Traceability** - Every equation traces to manuscript and source_grounding.txt
4. **Clear console output** - Human-readable formatted output from all scripts
5. **Consistency** - Config values match manuscript values exactly

---

## Directory Structure

```
src/mars_uav_sizing/
├── config/                           # Configuration files (YAML)
│   ├── __init__.py                   # Config loader with caching
│   ├── physical_constants.yaml       # Universal constants (from §3)
│   ├── mars_environment.yaml         # Mars-specific environment (from §3)
│   ├── propulsion_parameters.yaml    # Efficiencies (from §4.5)
│   ├── battery_parameters.yaml       # Energy storage (from §4.6)
│   ├── aerodynamic_parameters.yaml   # Drag polar, CL_max (from §4.7)
│   ├── geometry_parameters.yaml      # Disk loading, AR, etc (from §4.12)
│   └── mission_parameters.yaml       # Velocities, times (from §4.12)
├── core/                             # Core utilities
│   ├── __init__.py
│   ├── atmosphere.py                 # Mars atmospheric model class
│   └── utils.py                      # Common utility functions
├── section3/                         # Mission Analysis (§3)
│   ├── __init__.py
│   └── atmospheric_model.py          # Atmospheric calculations (§3.1)
├── section4/                         # Reference Data (§4)
│   ├── __init__.py
│   ├── aerodynamic_calculations.py   # Drag polar, L/D (§4.7)
│   ├── derived_requirements.py       # Velocity, wing geometry (§4.12)
│   └── geometry_calculations.py      # Tail, fuselage, rotor sizing (§4)
├── section5/                         # Constraint Analysis (§5)
│   ├── __init__.py
│   ├── rotorcraft.py                 # Rotorcraft analysis (§5.1)
│   ├── fixed_wing.py                 # Fixed-wing analysis (§5.2)
│   ├── hybrid_vtol.py                # Hybrid VTOL analysis (§5.3)
│   ├── matching_chart.py             # Constraint diagram (§5.4)
│   └── comparative.py                # Configuration comparison (§5.4)
├── section6/                         # Design Decisions (§6)
│   ├── __init__.py
│   ├── airfoil_selection.py          # Airfoil comparison and selection (§6.2)
│   └── airfoil_plots.py              # Airfoil visualization (§6.2 figures)
├── section7/                         # Component Selection (§7)
│   ├── __init__.py
│   ├── component_selection.py        # Component trade-off analysis (§7.1-7.4)
│   └── mass_breakdown.py             # Propulsion mass breakdown (§7.2)
├── visualization/                    # Plotting functions
│   ├── __init__.py
│   └── plotting.py                   # Matplotlib-based plots
├── verification/                     # Manuscript verification
│   ├── __init__.py
│   └── verify_manuscript.py          # Check scripts vs manuscript
├── deprecated/                       # Old scripts (reference only)
│   ├── analysis/                     # Old analysis module
│   ├── data/                         # Old baseline_parameters.yaml
│   ├── design_parameters.yaml        # Old consolidated config
│   └── *.py                          # Various superseded scripts
├── __init__.py                       # Package init
├── README.md                         # This file
└── run_analysis.py                   # Main entry point
```

---

## Configuration Files

Each YAML file corresponds to a manuscript section:

| File | Content | Section |
|------|---------|---------|
| `physical_constants.yaml` | Gravity, gas constants, Sutherland params | §3 / Appendix A |
| `mars_environment.yaml` | Arcadia Planitia conditions | §3.1 |
| `propulsion_parameters.yaml` | FM, η_motor, η_esc, η_prop | §4.5 |
| `battery_parameters.yaml` | e_spec, DoD, η_discharge | §4.6 |
| `aerodynamic_parameters.yaml` | AR, e, CD0, CL_max | §4.7 |
| `geometry_parameters.yaml` | Disk loading, taper, t/c | §4.12 |
| `mission_parameters.yaml` | Velocities, times, mass fractions | §3.2, §4.11, §4.12 |

### Accessing Configuration

```python
from mars_uav_sizing.config import get_param

# Physical constants
g_mars = get_param('physical.mars.g')  # 3.711 m/s²

# Environment
rho = get_param('environment.arcadia_planitia.density_kg_m3')  # 0.0196

# Propulsion (§4.5)
fm = get_param('propulsion.rotor.figure_of_merit')  # 0.40
eta_m = get_param('propulsion.electromechanical.eta_motor')  # 0.85

# Battery (§4.6)
e_spec = get_param('battery.specifications.specific_energy_Wh_kg')  # 270

# Aerodynamics (§4.7)
ar = get_param('aerodynamic.wing.aspect_ratio')  # 6
cd0 = get_param('aerodynamic.drag_polar.cd0')  # 0.030

# Geometry (§4.12)
dl = get_param('geometry.rotor.disk_loading_N_m2')  # 30

# Mission (§4.12)
v_cruise = get_param('mission.velocity.v_cruise_m_s')  # 40
mtow = get_param('mission.mass.mtow_kg')  # 10
```

---

## Usage

### Run All Analyses
```bash
cd src
python -m mars_uav_sizing.run_analysis
```

### Run Individual Section Scripts
```bash
# Section 3 - Atmospheric Model
python -m mars_uav_sizing.section3.atmospheric_model

# Section 4 - Reference Data
python -m mars_uav_sizing.section4.aerodynamic_calculations
python -m mars_uav_sizing.section4.derived_requirements
python -m mars_uav_sizing.section4.geometry_calculations

# Section 5 - Constraint Analysis
python -m mars_uav_sizing.section5.rotorcraft
python -m mars_uav_sizing.section5.fixed_wing
python -m mars_uav_sizing.section5.hybrid_vtol
python -m mars_uav_sizing.section5.matching_chart
python -m mars_uav_sizing.section5.comparative

# Verification
python -m mars_uav_sizing.verification.verify_manuscript
```

### From Python API
```python
from mars_uav_sizing.section5 import rotorcraft, comparative

# Run single analysis
results = rotorcraft.rotorcraft_feasibility_analysis()
rotorcraft.print_analysis(results)

# Run comparative analysis
summary = comparative.comparative_summary()
print(f"Selected: {summary['selected']}")
```

---

## Script Output Format

All scripts produce formatted console output:

```
================================================================================
ROTORCRAFT FEASIBILITY ANALYSIS (Section 5.1)
================================================================================
Computed: 2025-12-29 16:00:00
Config:   All values loaded from config/ YAML files

INPUT PARAMETERS (from configuration)
--------------------------------------------------
  MTOW:               10.00 kg
  Mars gravity:       3.711 m/s²
  Weight:             37.11 N
  ...

HOVER ANALYSIS (@eq:hover-power)
--------------------------------------------------
  Disk area:          1.237 m²
  Induced velocity:   27.64 m/s
  Electrical power:   3178 W
  ...

FEASIBILITY ASSESSMENT
--------------------------------------------------
  Requirement:        60 min endurance
  Achieved:           57.3 min
  Margin:             -4.5%
  Status:             ✗ FAIL

================================================================================
```

---

## Traceability

### Equation References
Every calculated value traces to a manuscript equation:
```python
def hover_power(...):
    """
    Implements @eq:hover-power from §5.1:
        P_hover = W^1.5 / (FM × sqrt(2ρA))
    
    Reference: Leishman (2006), Section 2.8
    """
```

### Source Grounding
All primary sources are documented in `source_grounding.txt`.

---

## Verification

Run verification to check script values against manuscript:

```bash
python -m mars_uav_sizing.verification.verify_manuscript
```

---

## Deprecated Files

The `deprecated/` folder contains old implementations that have been superseded:

| File | Reason |
|------|--------|
| `atmosphere.py` | Replaced by `core/atmosphere.py` |
| `plotting.py` | Replaced by `visualization/plotting.py` |
| `aerodynamics.py` | Replaced by `section4/aerodynamic_calculations.py` |
| `constraints.py` | Replaced by `section5/matching_chart.py` |
| `endurance.py` | Replaced by `section5/` modules |
| `weights.py` | Replaced by `section5/` modules |
| `constants.py` | Replaced by `config/` YAML files |
| `run_sizing.py` | Replaced by `run_analysis.py` |
| `section4_calculations.py` | Replaced by `section4/geometry_calculations.py` |
| `verify_manuscript_calculations.py` | Replaced by `verification/verify_manuscript.py` |
| `xfoil.exe`, `xfoil_wrapper.py` | XFOIL doesn't work at Mars Re numbers |
| `airfoil_analysis.py` | Duplicate of draft version |
| `analysis/` | Old analysis module, replaced by `section5/` |
| `data/baseline_parameters.yaml` | Replaced by `config/` YAML files |

These are kept for reference but **should not be used**.
