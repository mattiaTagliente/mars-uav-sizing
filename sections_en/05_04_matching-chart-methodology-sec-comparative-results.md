# Constraint analysis {#sec:constraint-analysis-matching}

## Matching chart methodology {#sec:comparative-results}

This section presents the matching chart (constraint diagram) methodology for aircraft preliminary sizing and applies it to derive the design point parameters for the Mars UAV. The matching chart visualises all performance constraints simultaneously, identifying the feasible design space as the intersection of all acceptable regions [@roskamAirplaneDesign12005a]<!-- #s:constraint -->.

### Requirements summary

From @sec:user-needs and @sec:derived-requirements, the Mars UAV must satisfy the following key requirements:

: Mission requirements summary {#tbl:requirements-summary}

| ID | Requirement | Threshold | Rationale |
|:---|:------------|:----------|:----------|
| OR-1 | Operational radius | ≥50 km | Exceed Curiosity's 35 km total distance in single flight |
| OR-4 | Cruise endurance | ≥60 min | Round trip + survey operations (42 min transit + 15 min survey + 2 min hover + 1 min transition) |
| - | VTOL capability | Required | No runway infrastructure on Mars |
| - | Payload capacity | ≥0.5 kg | Camera + radio relay payload |
| N6 | Single-fault tolerance | Required | Mission system with no abort capability |

### Matching chart fundamentals

#### Axes definition

Horizontal axis (Wing loading, $W/S$):

Wing loading is defined as aircraft weight per unit wing area:

$$\frac{W}{S} \quad [\text{N/m}^2 \text{ or Pa}]$$

Higher wing loading implies smaller wing area for a given weight, resulting in higher cruise and stall speeds, reduced drag from smaller wetted area, lighter wing structure, and increased sensitivity to gusts.

Vertical axis (Power loading, $P/W$):

Power loading is defined as installed power per unit weight:

$$\frac{P}{W} \quad [\text{W/N or W/kg}]$$

Higher power loading implies more installed power relative to weight, providing improved climb rate, greater hover capability (for VTOL configurations), greater acceleration capability, and increased propulsion system mass and cost.

#### Constraint lines

Each flight condition generates a constraint line on the matching chart. Points on the line represent the minimum $P/W$ (or maximum $W/S$) that satisfies that constraint.

Hover constraint (rotorcraft and hybrid VTOL):

From @eq:hover-constraint in @sec:rotorcraft-analysis:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$

This constraint is independent of wing loading (the disk loading $DL$ does not depend on wing area), appearing as a horizontal line on the matching chart. All points above this line satisfy the hover requirement.

Cruise constraint (fixed-wing and hybrid VTOL):

From @eq:cruise-electric-power in @sec:fixed-wing-analysis:

$$\left(\frac{P}{W}\right)_\text{cruise} = \frac{V}{(L/D) \times \eta_\text{cruise}}$$

Since $L/D$ depends on $C_L$ (which varies with $W/S$ at fixed velocity), this constraint forms a curve with a minimum at the optimal wing loading. At very low $W/S$, the aircraft operates at high $C_L$ with high induced drag; at very high $W/S$, the aircraft must fly faster, increasing parasite power. The minimum occurs near $(L/D)_\text{max}$.

Stall constraint:

From @eq:wing-loading-constraint in @sec:fixed-wing-analysis:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

This constraint sets the maximum allowable wing loading and appears as a vertical line on the matching chart. All points to the left of this line satisfy the minimum speed requirement.

Energy constraint (hybrid VTOL):

The energy constraint from @sec:energy-constraint manifests as a feasible region boundary that couples power loading to mission duration. Higher power loading (faster flight) generally reduces mission time but may violate energy constraints if hover power is too high.

The feasible region is the intersection of all acceptable regions: above the hover constraint (for VTOL configurations), above the cruise constraint curve, left of the stall constraint, and satisfying the energy constraint (verified separately).

The optimal design point minimises power loading within the feasible region, as this corresponds to a lighter and more efficient propulsion system. Typically, the design point lies at the intersection of two or more active constraints.

### Baseline case definition {#sec:baseline-case}

The constraint analysis in this section is performed for a fixed baseline MTOW of 10.00 kg, derived from the payload-driven mass allocation in @sec:initial-mass-estimate. The matching chart identifies feasible design space regions and constraint interactions; absolute geometry and power values are conditional on the assumed MTOW.

@tbl:baseline-parameters summarises the parameters held constant across configurations to ensure fair comparison.

: Baseline case parameters {#tbl:baseline-parameters}

| Parameter | Value | Notes |
|:----------|------:|:------|
| Payload mass | 1.00 kg | Camera + radio relay |
| MTOW | 10.00 kg | Baseline value |
| Battery mass fraction | 35% | 3.50 kg battery mass |
| Battery technology | 270 Wh/kg | Solid-state Li-ion |
| Depth of discharge | 80% | - |
| Energy reserve | 20% | - |
| Hover time allocation | 2 min | Takeoff + landing |
| Transition time allocation | 1 min | Two 30 s transitions |

The energy constraint is verified by explicit mission energy budget evaluation at the candidate design point, rather than plotted as a separate constraint line. This approach is appropriate for the fixed disk loading baseline case where energy feasibility depends on mission segment durations rather than wing loading.

### Configuration matching charts

Before examining each configuration individually, @fig:ld-comparison through @fig:endurance-comparison present the key performance metrics for all three candidate architectures.

![Aerodynamic efficiency comparison across configurations. The rotorcraft equivalent L/D of 4.0 is limited by rotor forward flight inefficiency, while fixed-wing achieves 11.7. The hybrid VTOL achieves 10.5 due to stopped rotor drag penalty.](figures/en/ld_comparison.png){#fig:ld-comparison width=80%}

![Power requirements comparison. Hover power (3178 W) is identical for rotorcraft and hybrid VTOL. Cruise power varies with aerodynamic efficiency: rotorcraft 460 W, fixed-wing 286 W, hybrid VTOL 318 W.](figures/en/power_comparison.png){#fig:power-comparison width=85%}

![Endurance comparison against the 60-minute requirement (dashed line). Rotorcraft marginally meets the requirement at 63.17 min. Fixed-wing achieves 120.5 min (with 20% energy reserve) but cannot satisfy VTOL requirement. Hybrid VTOL achieves 89.55 min with adequate margin.](figures/en/endurance_comparison.png){#fig:endurance-comparison width=80%}

#### Rotorcraft constraint analysis

For the pure rotorcraft configuration, the matching chart axes must be adapted since there is no wing. The relevant parameter is disk loading ($DL = T/A$) rather than wing loading. The dominant constraint is hover power, which increases dramatically with disk loading in the thin Mars atmosphere.

The rotorcraft design space is limited by the small endurance margin. The hover-dominated energy budget (3178 W hover power for 2 min consumes 106.0 Wh) leaves 468.5 Wh for cruise (459.7 W forward flight). The configuration achieves 63.17 minutes endurance, a +5.284% margin above the 60-minute requirement.

![Matching chart for the rotorcraft configuration. Power loading increases with disk loading according to actuator disk theory. The curve represents the hover constraint from @eq:hover-constraint. The design point (*) corresponds to the selected disk loading of 30 N/m².](figures/en/matching_chart_rotorcraft.png){#fig:matching-chart-rotorcraft width=85%}

#### Fixed-wing constraint analysis

For the pure fixed-wing configuration, the matching chart shows a cruise constraint as a shallow curve with minimum at optimal wing loading (approximately 11.00 N/m² for Mars conditions), a stall constraint as a vertical line at $W/S_\text{max}$ = 13.82 N/m² for $V_\text{min}$ = 35.04 m/s (where $V_\text{min}$ = 1.2 × $V_\text{stall}$ per @eq:v-min-constraint) and $C_{L,\text{max}}$ = 1.150, and no hover constraint (the fixed-wing cannot hover).

The feasible region exists and offers excellent power efficiency (286.4 W cruise at 10.00 kg MTOW). However, this region is inaccessible because the aircraft cannot take off without a runway. The ground roll distance of approximately 1060 m ensures that no design point in the feasible region is operationally achievable.

![Matching chart for the fixed-wing configuration. The cruise constraint curve (blue) shows minimum power loading decreasing toward optimal wing loading. The stall constraint (green vertical line) limits maximum wing loading. The design point (*) lies at the intersection of the cruise curve and stall constraint. Note the absence of a hover constraint, as fixed-wing aircraft cannot hover.](figures/en/matching_chart_fixed_wing.png){#fig:matching-chart-fixed-wing width=85%}

#### Hybrid VTOL constraint analysis

For the QuadPlane configuration, the matching chart combines a hover constraint as a horizontal line at $P/W$ = 85.71 W/N (dominates the chart), a cruise constraint as a curve well below hover constraint (cruise power approximately 10× lower), and a stall constraint as a vertical line at maximum allowable wing loading (13.82 N/m²).

The matching chart for the QuadPlane plots power loading $(P/W)$ against wing loading $(W/S)$.

Hover constraint: Appears as a horizontal line, independent of wing loading. The required hover power depends on disk loading and atmospheric density, not wing size:

$$(P/W)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint-qp}

Cruise constraint: Appears as a curve with minimum at optimal wing loading. At very low $W/S$, induced drag is high (high $C_L$); at very high $W/S$, the aircraft must fly fast to generate sufficient lift (high $V$). The minimum occurs near $(L/D)_\text{max}$.

Stall constraint: Appears as a vertical line at maximum allowable wing loading:

$$\left(\frac{W}{S}\right)_\text{max} = \frac{1}{2}\rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:stall-constraint}

Energy constraint: Manifests as a feasible region boundary that couples power loading to mission duration. Higher power loading (faster flight) generally reduces mission time but may violate energy constraints if hover power is too high.

The feasible region lies above the hover constraint line, left of the stall constraint, with the energy constraint verified (43.20% margin).

The baseline design point is hover-dominated. The installed power is set entirely by hover requirements; cruise power is abundant. The wing sizing is determined by stall and aerodynamic efficiency considerations, independent of power.

![Matching chart (constraint diagram) for the hybrid VTOL configuration. The hover constraint (horizontal red line) dominates, setting the minimum required power loading. The stall constraint (vertical green line) limits maximum wing loading. The cruise constraint (blue curve) is easily satisfied below the hover line. The design point (*) lies at the intersection of hover and stall constraints.](figures/en/matching_chart.png){#fig:matching-chart width=90%}

### Baseline design point determination

From the hybrid VTOL matching chart analysis (@fig:matching-chart), the QuadPlane baseline design point is characterised by:

: Baseline design point parameters {#tbl:design-point}

| Parameter | Value | Constraint |
|:----------|------:|:-----------|
| Wing loading, $W/S$ | 13.82 N/m² | Set by stall limit at $V_\text{min}$ = 35.04 m/s |
| Power loading, $P/W$ | 85.71 W/N | Set by hover requirement |
| Disk loading, $DL$ | 30.00 N/m² | Compromise between rotor size and power |

These values imply the following derived parameters for MTOW = 10.00 kg ($W$ = 37.11 N):

: Baseline design parameters {#tbl:design-parameters}

| Derived Parameter | Value | Calculation |
|:------------------|------:|:------------|
| Wing area | $S = W/(W/S) = 37.11/13.82$ | 2.686 m² |
| Wingspan | $b = \sqrt{AR \times S}$ | 4.01 m |
| Mean chord | $c = S/b$ | 0.669 m |
| Installed hover power | $P = (P/W) \times W$ | 3181 W |
| Installed cruise power | - | 318 W |

These preliminary values will be refined in @sec:design-decisions based on detailed component selection and trade-off analysis. The matching chart provides starting points for iterative design.

The configuration comparison, elimination of alternatives, and selection rationale are presented in @sec:architecture-selection.
