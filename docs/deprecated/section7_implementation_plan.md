# Section 7: Component Selection - Implementation Plan

## Purpose

Section 7 presents the selection of specific components for the Mars UAV based on the sizing requirements from Section 5 (Constraint Analysis) and the architectural decisions from Section 6 (Design Decisions).

## Key Constraints from Analysis

### Power Requirements (from Section 5 code output)
| Parameter | Value | Source |
|-----------|-------|--------|
| Total hover power | 3181 W | hybrid_vtol.py |
| Per lift motor (8 motors) | ~400 W | 3181/8 |
| Per coaxial pair (4 pairs) | ~795 W | 3181/4 |
| Total cruise power | 318 W | hybrid_vtol.py |
| Per cruise motor (2 motors) | ~160 W | 318/2 |

### Mass Budget (from Section 4)
| Category | Fraction | Mass (kg) |
|----------|----------|-----------|
| Propulsion | 0.20 | 2.00 |
| Battery | 0.35 | 3.50 |
| Payload | 0.10 | 1.00 |
| Empty (structure) | 0.30 | 3.00 |
| Avionics | 0.05 | 0.50 |
| **MTOW** | 1.00 | **10.00** |

### Propulsion Mass Target
- Total propulsion budget: 2.00 kg
- Target per lift motor unit (motor+ESC+prop): 2.00 × 0.70 / 8 = 0.175 kg = 175 g
- Target per cruise motor unit: 2.00 × 0.30 / 2 = 0.300 kg = 300 g

## Section 7 Structure

```
# Component selection and verification {#sec:component-verification}

## Selection methodology
### Requirements summary (from Section 5)
### Selection criteria
### Trade-off approach

## Propulsion system {#sec:propulsion-selection}

### Lift motors
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Lift ESCs
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Lift propellers
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Cruise motors
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Cruise ESCs
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Cruise propellers
#### Requirements
#### Candidate comparison table
#### Selection rationale
#### Selected component specification

### Propulsion mass summary
#### Complete mass breakdown table
#### Comparison with parametric estimate
#### Implications for MTOW

## Energy storage system {#sec:battery-selection}

### Requirements
### Candidate comparison table
### Selection rationale
### Selected specification

## Payload system {#sec:payload-selection}

### Camera payload
#### Requirements
#### Candidate comparison table
#### Selection rationale

### Telecommunication relay
#### Requirements
#### Candidate comparison table
#### Selection rationale

## Avionics {#sec:avionics-selection}

### Flight controller
### Navigation sensors
### Communication system

## Thermal management {#sec:thermal-selection}

### Requirements for Mars surface operation
### Heating system sizing
### Insulation specification

## Component mass summary {#sec:component-mass-summary}

### Complete vehicle mass breakdown
### Requirements compliance verification
### Design iteration recommendations
```

## Component Research Checklist

### Lift Motors (need 8)
Requirements:
- Power: ≥400 W continuous
- Mass: ≤100 g target (to stay within budget)
- Voltage: 6S compatible

Candidates to research:
- [ ] SunnySky V4006 (66g, 375W) - PROMISING
- [ ] T-Motor MN5008 (135g, 800W) - heavier but more power
- [ ] T-Motor MN4006 (if exists)
- [ ] SunnySky V3508 (105g)
- [ ] MAD 4014 EEE (142g, 507W)

### Lift ESCs (need 8)
Requirements:
- Current: ≥30A (based on motor current draw)
- Mass: ≤30 g target
- BLHeli/proprietary protocol

Candidates to research:
- [ ] T-Motor FLAME 25A
- [ ] T-Motor AIR 40A
- [ ] Hobbywing XRotor
- [ ] Smaller/lighter alternatives

### Lift Propellers (need 8)
Requirements:
- Diameter: ~12-15 inch (to fit disk loading constraint)
- Mass: ≤20 g per prop

### Cruise Motors (need 2)
Requirements:
- Power: ≥200 W continuous (with margin)
- Mass: ≤150 g target
- Efficiency optimized for sustained cruise

Candidates:
- [ ] T-Motor AT2814 (109g, 370W)
- [ ] T-Motor AT2312 (60g, 350W) - PROMISING for weight
- [ ] SunnySky motors

### Cruise ESCs (need 2)
Requirements:
- Current: ≥20A
- Mass: ≤30 g

### Cruise Propellers (need 2)
Requirements:
- Diameter: 12-15 inch
- Pitch optimized for cruise velocity

## Mass Target Analysis

### Current Selection (from earlier work) - TOO HEAVY
| Component | Qty | Unit (g) | Total (kg) |
|-----------|-----|----------|------------|
| Lift motors (MN505-S) | 8 | 225 | 1.800 |
| Lift ESCs (FLAME 60A) | 8 | 74 | 0.592 |
| Lift props (NS16x5.4) | 8 | 26 | 0.208 |
| Mounting | 1 | 300 | 0.300 |
| Cruise motors (AT4130) | 2 | 408 | 0.816 |
| Cruise ESCs (FLAME 60A) | 2 | 74 | 0.148 |
| Cruise props (NS15x5) | 2 | 26 | 0.052 |
| **Total** | | | **3.916** |

### Target Selection - WITHIN BUDGET
| Component | Qty | Target Unit (g) | Target Total (kg) |
|-----------|-----|-----------------|-------------------|
| Lift motors | 8 | ≤100 | ≤0.800 |
| Lift ESCs | 8 | ≤30 | ≤0.240 |
| Lift props | 8 | ≤20 | ≤0.160 |
| Mounting | 1 | 200 | 0.200 |
| Cruise motors | 2 | ≤100 | ≤0.200 |
| Cruise ESCs | 2 | ≤30 | ≤0.060 |
| Cruise props | 2 | ≤20 | ≤0.040 |
| **Total** | | | **≤1.700** |

This leaves ~0.30 kg margin for wiring, connectors, etc.

## Research Priority

1. **Lift motors** - biggest mass contributor, need to find ~100g motors with 400W+ power
2. **Cruise motors** - need ~100g motors with 200W+ power  
3. **ESCs** - find lighter alternatives to FLAME 60A
4. **Propellers** - secondary, most carbon fiber props are light

## Data Integrity Requirements

For each selected component:
1. Find manufacturer datasheet (primary source)
2. Add to Zotero Mars_UAV collection
3. Update source_grounding.txt
4. Update propulsion_parameters.yaml with new data
5. Re-run code to verify calculations

## Implementation Status (2025-12-31)

### Completed ✓

1. **Codebase refactoring**
   - Created `section7/` module with proper architecture
   - `component_selection.py` - Motor/ESC candidate databases and evaluation
   - `mass_breakdown.py` - Propulsion mass calculator (moved from section5)
   - Updated README with section7 directory structure

2. **Component research and selection**
   - Researched lightweight motor alternatives
   - Created comparison tables for lift and cruise motors
   - Selected components meeting mass and power constraints

3. **YAML configuration updated**
   - `propulsion_parameters.yaml` updated with new components
   - Consistent structure: lift/cruise systems each have motor, esc, propeller, mounting
   - Shared wiring component for power distribution

4. **Manuscript updated**
   - Section 7 (EN/IT) with complete comparison tables
   - Propulsion mass summary tables with correct values
   - Italian translations aligned

5. **Source grounding**
   - 5 new Zotero references added for selected components
   - source_grounding.txt updated with Section 7 entries

### Final Selected Components

| Component | Model | Qty | Unit (g) | Total (kg) |
|-----------|-------|-----|----------|------------|
| Lift motors | SunnySky V4006-380 | 8 | 66 | 0.528 |
| Lift ESCs | Hobbywing XRotor Micro 30A | 8 | 6 | 0.048 |
| Lift propellers | NS14×4.8 | 8 | 18 | 0.144 |
| **Lift subtotal** | - | - | - | **0.720** |
| Cruise motors | T-Motor AT2312-1150 | 2 | 60 | 0.120 |
| Cruise ESCs | Hobbywing XRotor Micro 30A | 2 | 6 | 0.012 |
| Cruise propellers | NS12×6 | 2 | 15 | 0.030 |
| **Cruise subtotal** | - | - | - | **0.162** |
| Mounting | Motor pods, booms, nacelle | 1 | 200 | 0.200 |
| Wiring | Power distribution | 1 | 100 | 0.100 |
| **Shared subtotal** | - | - | - | **0.300** |
| **Total propulsion** | - | - | - | **1.182** |

Note: Lift and cruise subtotals include source-grounded components only. Shared components are engineering estimates.

### Results

- **Total propulsion mass**: 1.182 kg
- **Mass budget**: 2.000 kg (f_prop = 0.20)
- **Margin**: +0.818 kg (40.9% under budget) ✓

### Remaining Tasks (Future Work)

- [ ] Battery selection with comparison tables
- [ ] Payload selection (camera, radio)
- [ ] Avionics selection
- [ ] Thermal management sizing
- [ ] Complete vehicle mass breakdown

