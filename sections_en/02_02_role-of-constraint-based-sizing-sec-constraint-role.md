# Design methodology

## Role of constraint-based sizing {#sec:constraint-role}

The matching chart, or constraint diagram, forms the analytical core of the sizing methodology. This graphical tool, adapted from power-based aircraft sizing methods, visualises the constraints that bound the feasible design space.

### Configuration-specific constraint spaces

Different aircraft configurations require different constraint diagram formulations, reflecting their distinct performance drivers:

* **Rotorcraft configurations** use a constraint diagram with power loading (P/W) on the vertical axis and **disk loading** (DL = T/A) on the horizontal axis. Since rotorcraft have no wing, wing loading is not a meaningful parameter. The hover power constraint dominates, with power loading increasing monotonically with disk loading according to actuator disk theory.

* **Fixed-wing configurations** use power loading (P/W) versus **wing loading** (W/S) axes. The stall constraint appears as a vertical line limiting maximum wing loading, while the cruise constraint appears as a curve with minimum power at optimal wing loading. No hover constraint exists since fixed-wing aircraft cannot hover.

* **Hybrid VTOL configurations** (QuadPlane) combine elements of both: wing loading applies to the cruise phase while disk loading applies to the hover phase. The constraint diagram uses P/W versus W/S axes, with the hover constraint appearing as a horizontal line (independent of wing loading) and the cruise and stall constraints as for fixed-wing.

This configuration-specific approach ensures that each architecture is evaluated in its natural constraint space, enabling meaningful comparison of feasibility margins.

### Hybrid VTOL constraints

For a hybrid VTOL aircraft, which emerges as the most suitable configuration from the trade-off analysis (@sec:architecture-selection), the relevant constraints include:

* Hover constraint: sets minimum power loading based on disk loading and atmospheric density. The thin Mars atmosphere (approximately 0.020 kg/m³ at Arcadia Planitia) demands higher power loading than equivalent Earth operations.
* Cruise constraint: derived from the drag polar, this constraint determines the power required for steady-level flight at the design cruise speed.
* Climb constraint: ensures sufficient excess power for the required rate of climb.
* Stall constraint: sets the maximum wing loading based on the airfoil's maximum lift coefficient at the operating Reynolds number.

The design point is selected within the feasible region bounded by these constraints. For QuadPlane configurations, the hover and cruise constraints are largely decoupled: the lift rotors are sized to satisfy the hover constraint, while the wing and cruise motor are sized to satisfy the cruise and stall constraints. This decoupling simplifies the design space exploration but requires verification that the combined system remains within the MTOW target.

The derived requirements summarized in @tbl:derived-requirements define the starting point for the matching chart analysis. The target MTOW of 10 kg, derived from mass fraction analysis and payload requirements, establishes the weight for constraint evaluation. The assumed battery fraction (35%), specific energy (270 Wh/kg), and propulsion efficiencies feed into the power and endurance calculations. Running the matching chart with these inputs yields the preliminary design point: the specific combination of wing loading and power loading that maximizes endurance while satisfying all constraints. This design point then determines the wing area, span, and motor power requirements that drive component selection.

The iterative nature of this process acknowledges that initial hypotheses are necessarily approximate. As component selection reveals actual masses and efficiencies, the design point may shift. The methodology ensures that such shifts are systematically tracked and that the final design remains traceable to its analytical foundations.
