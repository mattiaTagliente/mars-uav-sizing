# Design methodology

## Iterative sizing approach {#sec:iterative-sizing}

The development of this Mars UAV follows an iterative sizing methodology that balances theoretical analysis with practical component constraints. Unlike conventional terrestrial aircraft design, where mature scaling laws and extensive databases exist, Mars aircraft design requires careful integration of limited flight heritage with scaled analysis from reference cases.

The design process proceeds through four distinct phases, with feedback loops enabling refinement at each stage:

1. **Initial hypotheses**: reference VTOL UAV data from commercial platforms and Mars concept designs (@sec:reference-data) provides empirical grounding for initial parameter estimates. Key parameters extracted from the reference designs include weight fractions (propulsion, energy, payload, and, by subtraction, structure and other subsystems), disk loading for VTOL operations, and power-to-weight ratios. These Earth-based values are then scaled for Mars conditions, accounting for the reduced gravity (38% of Earth) and thin atmosphere (approximately 1% of Earth sea-level density).
2. **Preliminary sizing**: with initial hypotheses established, the constraint-based sizing methodology generates a preliminary design point. The matching chart determines the combination of wing loading and power loading that satisfies all flight conditions (hover, cruise, climb, and stall). From this design point, preliminary values for wing area, span, motor power, and mass breakdown are calculated.
3. **Component selection**: the preliminary sizing results guide the selection of actual components from manufacturer datasheets. This phase confronts the idealized sizing model with real-world constraints, as motors are available only in discrete sizes, batteries have specific energy densities, voltage characteristics, and temperature limitations, and propellers must match available motor configurations.
4. **Verification**: the selected components provide updated mass, power, and efficiency values that differ from preliminary estimates. The design is recalculated with these actual values, and compliance with mission requirements is verified. If requirements are not met, the process returns to phase 2 with refined hypotheses.

@fig:sizing-loop illustrates the iterative nature of this process. Each iteration narrows the design space as component-level constraints emerge and requirements are progressively satisfied.

![The iterative sizing loop for Mars UAV design.](figures/sizing_loop.jpg){#fig:sizing-loop}

### Current study scope

This feasibility study represents the **first iteration** of the described four-phase cycle. Phases 1 (initial hypotheses) and 2 (preliminary sizing) are complete: reference data analysis establishes initial parameters (@sec:reference-data), constraint-based sizing determines the design point (@sec:constraint-analysis), and configuration trade-offs identify the hybrid VTOL as the selected architecture (@sec:architecture-selection). Phases 3 (component selection) and 4 (verification) are partially addressed through representative commercial components and analytical verification against mission requirements.

The numerical results presented in @sec:constraint-analysis are evaluated at a **fixed baseline MTOW of 10.00 kg**, derived from mass fraction analysis (@sec:initial-mass-estimate). This baseline case approach enables direct comparison of configuration performance under identical mass and energy constraints. A closed-loop sizing iteration—where MTOW is adjusted to exactly satisfy mission requirements—is deferred to subsequent design phases.

Aspects not modelled in this first iteration include detailed packaging and volume constraints, thermal margin analysis under operational cycles, stability and control verification, and manufacturing and assembly considerations. These are reserved for subsequent iterations as the design matures toward detailed design.
