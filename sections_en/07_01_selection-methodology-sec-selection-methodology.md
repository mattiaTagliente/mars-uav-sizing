# Component selection and verification

## Selection methodology {#sec:selection-methodology}

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

| Component category | Quantity | Target mass (kg) | Per-unit target |
|:-------------------|:--------:|----------------:|:----------------|
| Lift motors | 8 | 0.560 | 70 g each |
| Lift ESCs | 8 | 0.160 | 20 g each |
| Lift propellers | 8 | 0.160 | 20 g each |
| Lift mounting | 1 | 0.200 | total |
| Lift subtotal | N.A. | 1.080 | N.A. |
| Cruise motors | 2 | 0.200 | 100 g each |
| Cruise ESCs | 2 | 0.060 | 30 g each |
| Cruise propellers | 2 | 0.040 | 20 g each |
| Cruise subtotal | N.A. | 0.300 | N.A. |
| Wiring, connectors | 1 | 0.320 | margin |
| Total propulsion | N.A. | 1.700 | N.A. |

### Selection criteria

Components are evaluated against the following criteria, in priority order: (1) power adequacy, meeting or exceeding the constraint analysis power requirements; (2) mass compliance, staying within the per-unit mass targets; (3) voltage compatibility with 6S LiPo nominal 22.2V for system commonality; (4) temperature range for operation at Mars surface temperatures down to −60°C; (5) reliability, with preference for proven designs with flight heritage.

