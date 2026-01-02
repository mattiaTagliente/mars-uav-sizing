# Appendix C: Sizing script documentation

## Package overview

The Mars UAV sizing calculations are implemented in the Python package `mars_uav_sizing`, located in:

```
src/mars_uav_sizing/
```

## Directory structure

```
mars_uav_sizing/
├── config/                    # YAML configuration files
│   ├── physical_constants.yaml
│   ├── mars_environment.yaml
│   ├── propulsion_parameters.yaml
│   ├── battery_parameters.yaml
│   ├── aerodynamic_parameters.yaml
│   ├── geometry_parameters.yaml
│   └── mission_parameters.yaml
├── core/                      # Core physics modules
│   ├── atmosphere.py          # Mars atmospheric model
│   └── utils.py               # Common utilities
├── section3/                  # Mission analysis (§3)
│   └── atmospheric_model.py
├── section4/                  # Reference data (§4)
│   ├── aerodynamic_calculations.py
│   ├── derived_requirements.py
│   └── geometry_calculations.py
├── section5/                  # Constraint analysis (§5)
│   ├── rotorcraft.py
│   ├── fixed_wing.py
│   ├── hybrid_vtol.py
│   ├── matching_chart.py
│   └── comparative.py
├── section6/                  # Design decisions (§6)
│   ├── airfoil_selection.py
│   └── airfoil_plots.py
├── section7/                  # Component selection (§7)
│   ├── component_selection.py
│   └── mass_breakdown.py
├── visualization/             # Plotting functions
│   └── plotting.py
├── verification/              # Manuscript verification
│   └── verify_manuscript.py
└── run_analysis.py            # Main entry point
```

## Usage

### Running all analyses

```bash
cd src
python -m mars_uav_sizing.run_analysis
```

### Running individual section scripts

```bash
# Section 3 - Atmospheric model
python -m mars_uav_sizing.section3.atmospheric_model

# Section 4 - Reference data
python -m mars_uav_sizing.section4.aerodynamic_calculations
python -m mars_uav_sizing.section4.derived_requirements

# Section 5 - Constraint analysis
python -m mars_uav_sizing.section5.rotorcraft
python -m mars_uav_sizing.section5.fixed_wing
python -m mars_uav_sizing.section5.hybrid_vtol
python -m mars_uav_sizing.section5.matching_chart
python -m mars_uav_sizing.section5.comparative
```

### Configuration access

All parameters are loaded from YAML configuration files:

```python
from mars_uav_sizing.config import get_param

# Physical constants
g_mars = get_param('physical.mars.g')  # 3.711 m/s²

# Environment
rho = get_param('environment.arcadia_planitia.density_kg_m3')  # 0.0196

# Mission
v_cruise = get_param('mission.velocity.v_cruise_m_s')  # 40
mtow = get_param('mission.mass.mtow_kg')  # 10
```

## Configuration files

: Configuration file contents {#tbl:config-files}

| File | Content | Section |
|:-----|:--------|:--------|
| `physical_constants.yaml` | Gravity, gas constants, Sutherland params | §3, Appendix A |
| `mars_environment.yaml` | Arcadia Planitia conditions | §3.1 |
| `propulsion_parameters.yaml` | FM, motor/ESC efficiency | §4.5 |
| `battery_parameters.yaml` | Specific energy, DoD | §4.6 |
| `aerodynamic_parameters.yaml` | AR, e, CD0, CL_max | §4.7 |
| `geometry_parameters.yaml` | Disk loading, taper | §4.12 |
| `mission_parameters.yaml` | Velocities, times, mass fractions | §3.2, §4.11, §4.12 |

## Output format

All scripts produce formatted console output with clear section headers, input parameters, calculated values, and feasibility assessments. Example output:

```
================================================================================
QUADPLANE FEASIBILITY ANALYSIS (Section 5.3)
================================================================================
Computed: 2026-01-01 18:00:00
Config:   All values loaded from config/ YAML files

INPUT PARAMETERS (from configuration)
--------------------------------------------------
  MTOW:               10.00 kg
  Mars gravity:       3.711 m/s²
  Weight:             37.11 N
  ...

FEASIBILITY ASSESSMENT
--------------------------------------------------
  Requirement:        60 min endurance
  Achieved:           89.6 min
  Margin:             +49.3%
  Status:             ✓ PASS
================================================================================
```

