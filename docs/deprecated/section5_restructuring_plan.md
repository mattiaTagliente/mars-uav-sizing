# Section 5 Restructuring Plan

## Purpose

This document outlines the restructuring needed to ensure:
1. **Structural parallelism** - all three configuration subsections have identical internal structure
2. **Content purity** - Section 5 is analysis only, no comparisons or selection conclusions
3. **Correct placement** - detailed component selection moves to Section 7

## Current Structure Audit

### Section 5.1: Rotorcraft Configuration
```
### Hover power analysis
    #### Momentum theory fundamentals
    #### Figure of merit
    #### Electrical power requirements
    #### Power loading constraint
### Forward flight performance
    #### Power components in forward flight
    #### Equivalent lift-to-drag ratio
    #### Forward flight electrical power
### Endurance analysis
    #### Battery energy model
    #### Rotorcraft endurance equation
    #### Endurance calculation
### Feasibility assessment
    #### Critical analysis of rotorcraft endurance
    #### Comparison with mission requirements
    #### Sensitivity analysis                      # ISSUE: contains comparative comments
### Rotorcraft configuration conclusion
```

### Section 5.2: Fixed-Wing Configuration
```
### Steady level flight fundamentals
    #### Force equilibrium
    #### Lift equation
### Lift-to-drag ratio
    #### L/D from the drag polar
    #### Maximum lift-to-drag ratio
    #### Speed for maximum L/D
### Cruise power analysis
    #### Power required for level flight
    #### Shaft power and propeller efficiency
    #### Electrical power
    #### Power loading formulation
### Stall constraint
    #### Stall speed
    #### Wing loading constraint
### Endurance analysis
    #### Battery energy model
    #### Fixed-wing endurance equation
    #### Endurance calculation
    #### Range calculation
### Takeoff and landing problem
    #### Ground roll analysis
    #### Mars-specific effects on takeoff
    #### Alternative launch methods
    #### Landing problem
### Feasibility assessment
    #### Requirements compliance
### Fixed-wing configuration conclusion
```

### Section 5.3: Hybrid VTOL Configuration
```
### QuadPlane architecture                      # ISSUE: different structure than 5.1, 5.2
    #### Configuration description
    #### Flight phases
### Hover constraint
    #### Reference to rotorcraft analysis
    #### Difference from rotorcraft: hover duration
    #### Hover energy
### Cruise constraint
    #### Reference to fixed-wing analysis
    #### QuadPlane aerodynamic efficiency
    #### Cruise power
    #### Cruise energy
### Transition phase analysis                   # UNIQUE to hybrid
### Energy storage constraint
    #### Total energy requirement
    #### Energy constraint verification
    #### Battery fraction constraint
### Mass penalty analysis                       # ISSUE: contains detailed component table
    #### Dual propulsion mass breakdown         # MOVE to Section 7
    #### Mass penalty calculation
    #### Mass penalty trade-off
### Combined constraint analysis
    #### Constraints summary
### Feasibility conclusion                      # ISSUE: different from "Feasibility assessment"
    #### Energy budget summary
```

## Issues Identified

### 1. Structural Inconsistency
- 5.1 has "Feasibility assessment" with 3 sub-sections
- 5.2 has "Feasibility assessment" with 1 sub-section
- 5.3 has "Feasibility conclusion" (different name!)

### 2. Comparative Content in Analysis Section
- 5.1.4.3 "Sensitivity analysis" contains: "For comparison, the hybrid VTOL configuration..."
- These comparative statements belong in Section 6.1.1 (Configuration comparison)

### 3. Detailed Component Data in Analysis Section
- 5.3.6.1 "Dual propulsion mass breakdown" contains specific T-Motor component masses
- This belongs in Section 7 (Component selection)

### 4. Missing Parallel Sections
- 5.1 has "Forward flight performance" - 5.2 and 5.3 should have equivalent or clearly mapped sections
- 5.3 has "Transition phase analysis" - unique to hybrid, which is acceptable

## Proposed Unified Structure

Each configuration section (5.1, 5.2, 5.3) should follow this template:

```
## [Configuration] configuration {#sec:[config]-analysis}

### Configuration description                   # Brief description of the configuration
    #### Operating principle                    # How it works
    #### Flight phases                          # For hybrid only (brief reference)

### Power analysis                              # Main analytical content
    #### Hover/Cruise power model               # Configuration-specific equations
    #### Electrical power requirements          # With efficiencies
    #### Power loading                          # P/W formulation

### Endurance analysis                          # Energy and time
    #### Energy model                           # Battery energy, consumption
    #### Endurance equation                     # Configuration-specific
    #### Endurance calculation                  # Numerical result

### Constraint summary                          # Unified constraints section
    #### Power constraint                       # P/W requirements
    #### Geometric constraint                   # W/S, stall, ground roll, etc.
    #### Energy constraint                      # Battery sizing

### Feasibility assessment                      # Same name in all sections
    #### Requirements compliance                # Pass/fail for each requirement
    #### Sensitivity to key parameters          # Parameter variations only, NO comparisons
    #### Configuration limitations              # What this config cannot do

### Configuration summary                       # Brief summary, NO selection decision
```

### Special Considerations:
- Hybrid VTOL may have additional "Transition phase analysis" subsection
- Fixed-wing has "Takeoff and landing problem" (VTOL constraint) - critical for its infeasibility
- Rotorcraft has "Forward flight performance" - equivalent to cruise analysis

## Content Relocation

### To Remove from Section 5:
1. **All comparative statements** (e.g., "For comparison, the hybrid VTOL...")
   → Move to Section 6.1.1 (Configuration comparison)

2. **Selection conclusions** (e.g., "QuadPlane is the only recommended...")
   → Move to Section 6.1.3 (Selection of hybrid VTOL)

3. **Detailed component masses** (specific T-Motor part numbers, weights)
   → Move to Section 7 (Component selection)

### To Keep in Section 5:
1. Configuration descriptions
2. Constraint equations and analysis
3. Endurance calculations
4. Feasibility pass/fail assessments (objective, not comparative)
5. Parameter sensitivity (how does endurance change with mass fraction, L/D, etc.)

## Mass Penalty in Section 5.3

Replace the detailed component table with a parametric estimate:

**Current** (in 5.3):
```
| Lift motors | 4 | 0.2250 | 0.9000 | [@t-motorMN505SKV260Brushless2024] |
| Lift ESCs   | 4 | 0.0740 | 0.2960 | ...
```

**Proposed** (in 5.3):
```
The mass penalty for the dual propulsion system can be estimated using the 
propulsion mass fraction fₚᵣₒₚ = 0.20 from @tbl:design-mass-fractions:

  m_propulsion = f_prop × MTOW = 0.20 × 10.00 = 2.00 kg

For QuadPlane configurations, this is divided between lift and cruise systems.
Commercial reference data (@tbl:reference-vtol) suggests approximately:
- Lift system: 60-70% of propulsion mass
- Cruise system: 30-40% of propulsion mass

Using a 2:1 ratio (conservative for octocopter configuration):
  m_lift = 0.67 × 2.00 = 1.33 kg
  m_cruise = 0.33 × 2.00 = 0.67 kg

Detailed component selection is presented in @sec:component-selection.
```

## Action Items

1. [ ] Create unified subsection structure for 5.1, 5.2, 5.3
2. [x] Remove all comparative statements from Section 5 → move to Section 6.1.1
3. [x] Remove specific component table from Section 5.3 → move to Section 7
4. [x] Replace with parametric mass estimate in Section 5.3
5. [ ] Rename sections for consistency (all use "Feasibility assessment")
6. [ ] Add missing "Sensitivity to key parameters" subsections where absent
7. [x] Remove selection conclusions from Section 5
8. [x] Update Italian versions to match

## Verification

After restructuring:
- [ ] Each of 5.1, 5.2, 5.3 has same subsection names
- [x] No comparative statements in Section 5
- [x] No selection conclusions in Section 5
- [x] No specific component data in Section 5
- [ ] All tables reference code-generated values, not hardcoded numbers
- [x] Italian version matches English structure

## Progress Notes (2025-12-31)

### Completed:
- Removed comparative statements from Section 5.1 (EN/IT):
  - Removed "For comparison, the hybrid VTOL configuration..." from sensitivity analysis
  - Removed "Unlike a hybrid VTOL that can glide..." from conclusion
  - Removed "45% higher than hybrid VTOL cruise" comparison
- Removed comparative statements from Section 5.3 (EN/IT):
  - Removed "This achieves a fundamentally different energy budget than pure rotorcraft..."
  - Removed detailed rotorcraft comparison from conclusion
- Replaced detailed component table in Section 5.3 with parametric estimate using mass fractions
- Created mass_breakdown.py module in codebase for propulsion mass calculations
- Updated propulsion_parameters.yaml with correct component quantities (8 lift, 2 cruise)

### Remaining:
- [ ] Structural parallelism: ensure 5.1, 5.2, 5.3 have matching section headings
- [ ] Rename "Feasibility conclusion" in 5.3 to "Feasibility assessment"
- [ ] Verify all numerical values in Section 5 match code output
- [ ] Move detailed component table to Section 7 (Component Selection)

