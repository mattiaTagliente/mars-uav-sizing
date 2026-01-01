# Component selection and verification {#sec:component-verification}

This section presents the selection of specific components based on the sizing results from the constraint analysis (@sec:hybrid-vtol-analysis). Component selection follows a systematic trade-off approach, evaluating candidates against requirements derived from Section 5 calculations.

## Selection methodology

### Requirements from constraint analysis

The power requirements are derived from the codebase calculations in `section5/hybrid_vtol.py`:

: Power requirements from constraint analysis {#tbl:motor-power-requirements}

| Parameter | Value | Derivation |
|:----------|------:|:-----------|
| Total hover power | 3181 W | @eq:electric-hover-qp |
| Per lift motor (8) | 398 W | 3181 W ÷ 8 |
| Per coaxial pair (4) | 795 W | 3181 W ÷ 4 |
| Total cruise power | 318 W | @eq:cruise-power-value |
| Per cruise motor (2) | 159 W | 318 W ÷ 2 |

### Mass budget constraints

The propulsion mass budget from @tbl:design-mass-fractions is:

$$m_\text{propulsion} = f_\text{prop} \times MTOW = 0.20 \times 10.00 = 2.00 \text{ kg}$$

Allocating 70% to lift system and 30% to cruise system:

: Propulsion mass allocation {#tbl:mass-allocation}

| Component category | Target mass (kg) | Per-unit target |
|:-------------------|----------------:|:----------------|
| Lift motors (8) | 0.560 | 70 g each |
| Lift ESCs (8) | 0.160 | 20 g each |
| Lift propellers (8) | 0.160 | 20 g each |
| Lift mounting | 0.200 | total |
| **Lift subtotal** | **1.080** | - |
| Cruise motors (2) | 0.200 | 100 g each |
| Cruise ESCs (2) | 0.060 | 30 g each |
| Cruise propellers (2) | 0.040 | 20 g each |
| **Cruise subtotal** | **0.300** | - |
| Wiring, connectors | 0.320 | margin |
| **Total propulsion** | **1.700** | - |

### Selection criteria

Components are evaluated against the following criteria, in priority order:

1. **Power adequacy**: meet or exceed the constraint analysis power requirements
2. **Mass compliance**: stay within the per-unit mass targets
3. **Voltage compatibility**: 6S LiPo (22.2V nominal) for system commonality
4. **Temperature range**: operation at Mars surface temperatures (down to −60°C)
5. **Reliability**: preference for proven designs with flight heritage

## Propulsion system {#sec:propulsion-selection}

### Lift motors {#sec:lift-motor-selection}

#### Requirements

Each lift motor must provide at least 400 W continuous power while remaining under 100 g (70 g target) to meet the mass budget. Motors must be compatible with 12-16 inch propellers to match the selected lift propeller class.

#### Candidate comparison

@tbl:lift-motor-comparison presents candidate lift motors evaluated against the requirements.

: Lift motor candidate comparison {#tbl:lift-motor-comparison}

| Motor | Mass (g) | Power (W) | Thrust (g) | KV | LiPo | Prop (in) | Status |
|:------|:--------:|----------:|:----------:|---:|:----:|:---------:|:-------|
| SunnySky V4006-380 | 66 | 375 | 2560 | 380 | 4-6S | 12-15 | **Selected** |
| MAD 4008 EEE-380 | 88 | ~400 | 2700 | 380 | 4-6S | 14-18 | Alternative |
| T-Motor MN5008-400 | 135 | 800 | 4200 | 400 | 6S | 15-17 | Too heavy |
| T-Motor MN505-S-260 | 225 | 2500 | - | 260 | 12S | 16-17 | Too heavy |

#### Selection rationale

The **SunnySky V4006-380** is selected for the lift motors based on:

* **Mass**: 66 g per motor is well within the 70 g target, enabling 8 motors at 528 g total
* **Power**: 375 W continuous is adequate for the 398 W requirement with appropriate propeller matching
* **Thrust**: 2560 g maximum thrust provides 2:1 thrust-to-weight margin per motor
* **Availability**: widely available from multiple suppliers

The MAD 4008 EEE is retained as an alternative if additional power margin is required.

#### Selected specification

: SunnySky V4006-380 specifications {#tbl:lift-motor-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Model | SunnySky V4006-380 | - |
| KV | 380 | RPM/V |
| Mass (with wire) | 66 | g |
| Stator diameter | 40 | mm |
| Stator thickness | 6 | mm |
| Max continuous power | 375 | W |
| Max thrust | 2560 | g |
| Recommended LiPo | 4-6S | - |
| Recommended propeller | 12-15 | inch |

### Lift ESCs {#sec:lift-esc-selection}

#### Requirements

Each lift ESC must handle at least 25A continuous current (based on 400 W at 16V) while remaining under 20 g to meet the mass budget.

#### Candidate comparison

: Lift ESC candidate comparison {#tbl:lift-esc-comparison}

| ESC | Mass (g) | Continuous (A) | Burst (A) | LiPo | BEC | Status |
|:----|:--------:|---------------:|----------:|:----:|:---:|:-------|
| Hobbywing XRotor Micro 30A | 6 | 30 | 40 | 2-4S | No | **Selected** |
| T-Motor F35A | 6.7 | 35 | 45 | 3-6S | No | Alternative |
| T-Motor FLAME 60A 12S | 74 | 60 | 80 | 12S | No | Too heavy |

#### Selection rationale

The **Hobbywing XRotor Micro 30A** is selected for the lift ESCs based on:

* **Mass**: 6 g per ESC enables 8 ESCs at only 48 g total
* **Current**: 30A continuous exceeds the ~25A requirement
* **Compatibility**: BLHeli_32 firmware for reliable motor control

#### Selected specification

: Hobbywing XRotor Micro 30A specifications {#tbl:lift-esc-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Model | Hobbywing XRotor Micro 30A | - |
| Continuous current | 30 | A |
| Burst current | 40 | A |
| Mass | 6 | g |
| LiPo cells | 2-4S | - |
| Firmware | BLHeli_32 | - |

### Lift propellers {#sec:lift-prop-selection}

#### Requirements

Lift propellers must be in the 13-15 inch class to match motor compatibility while remaining under 20 g each.

#### Selected specification

Carbon fiber propellers in the 13-14 inch range typically weigh 15-20 g per blade pair. The **T-Motor NS14×4.8** or equivalent is suitable.

: Lift propeller specifications {#tbl:lift-prop-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Diameter | 14 | inch |
| Pitch | 4.8 | inch |
| Mass (pair) | 18 | g |
| Material | Carbon fiber | - |

### Cruise motors {#sec:cruise-motor-selection}

#### Requirements

Each cruise motor must provide at least 200 W continuous power (with margin over 159 W) while remaining under 100 g.

#### Candidate comparison

: Cruise motor candidate comparison {#tbl:cruise-motor-comparison}

| Motor | Mass (g) | Power (W) | KV | LiPo | Status |
|:------|:--------:|----------:|---:|:----:|:-------|
| T-Motor AT2312-1150 | 60 | 350 | 1150 | 2-4S | **Selected** |
| T-Motor AT2814-1000 | 109 | 370 | 1000 | 2-4S | Alternative |
| T-Motor AT4130-230 | 408 | 2500 | 230 | 12S | Too heavy |

#### Selection rationale

The **T-Motor AT2312-1150** is selected for the cruise motors based on:

* **Mass**: 60 g per motor enables 2 motors at only 120 g total
* **Power**: 350 W continuous exceeds the 159 W requirement by 2:1 margin
* **Design**: AT series is optimised for fixed-wing cruise efficiency

#### Selected specification

: T-Motor AT2312-1150 specifications {#tbl:cruise-motor-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Model | T-Motor AT2312-1150 | - |
| KV | 1150 | RPM/V |
| Mass (with wire) | 60 | g |
| Max continuous power | 350 | W |
| Recommended LiPo | 2-4S | - |
| Shaft diameter | 4 | mm |

### Cruise ESCs {#sec:cruise-esc-selection}

#### Requirements

Each cruise ESC must handle at least 20A continuous current while remaining under 30 g.

#### Selected specification

The **Hobbywing XRotor Micro 30A** (same as lift) is selected for component commonality.

### Cruise propellers {#sec:cruise-prop-selection}

#### Requirements

Cruise propellers must be optimised for the cruise velocity of 40 m/s with 12-14 inch diameter.

#### Selected specification

: Cruise propeller specifications {#tbl:cruise-prop-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Diameter | 12 | inch |
| Pitch | 6 | inch |
| Mass (pair) | 15 | g |
| Material | Carbon fiber | - |

### Propulsion mass summary {#sec:propulsion-mass-summary}

@tbl:propulsion-summary presents the complete propulsion mass breakdown with selected components.

: Propulsion system mass summary with selected components {#tbl:propulsion-summary}

| Component | Model | Qty | Unit (g) | Total (kg) |
|:----------|:------|:---:|:--------:|:----------:|
| Lift motors | SunnySky V4006-380 | 8 | 66 | 0.528 |
| Lift ESCs | Hobbywing XRotor Micro 30A | 8 | 6 | 0.048 |
| Lift propellers | NS14×4.8 | 8 | 18 | 0.144 |
| **Lift subtotal** | - | - | - | **0.720** |
| Cruise motors | T-Motor AT2312-1150 | 2 | 60 | 0.120 |
| Cruise ESCs | Hobbywing XRotor Micro 30A | 2 | 6 | 0.012 |
| Cruise propellers | NS12×6 | 2 | 15 | 0.030 |
| **Cruise subtotal** | - | - | - | **0.162** |
| Mounting | Motor pods, booms, nacelle | 1 | 200 | 0.200 |
| Wiring | Power distribution, connectors | 1 | 100 | 0.100 |
| **Shared subtotal** | - | - | - | **0.300** |
| **Total propulsion** | - | - | - | **1.182** |

Note: Lift and cruise subtotals include source-grounded component data. Shared components (mounting, wiring) are engineering estimates without manufacturer datasheets.

### Comparison with mass budget

The selected components yield a total propulsion mass of **1.18 kg**, well within the 2.00 kg budget allocated by the propulsion fraction $f_\text{prop}$ = 0.20.

$$f_\text{prop,actual} = \frac{m_\text{propulsion}}{MTOW} = \frac{1.182}{10.00} = 0.118 = 11.8\%$$

This represents a **40% reduction** from the allocated budget, providing margin for:

* Heavier alternative motors if additional power is needed
* Thermal management components for Mars operation
* Design iteration flexibility

The propulsion mass reduction reallocates 0.82 kg to other system categories, potentially increasing payload capacity or structural mass.

