# Constraint analysis

## Fixed-wing configuration {#sec:fixed-wing-analysis}

This section evaluates whether a pure fixed-wing (conventional airplane) configuration can satisfy the Mars UAV mission requirements. The analysis develops the theoretical framework for steady level flight, cruise power, and endurance, demonstrating that while fixed-wing achieves higher aerodynamic efficiency, the configuration fails the mission due to the VTOL requirement. A conventional fixed-wing aircraft requires runway infrastructure that does not exist on Mars.

### Steady level flight fundamentals

#### Force equilibrium

In steady, unaccelerated, level flight, two pairs of forces must be in equilibrium [@torenbeekSynthesisSubsonicAirplane1982, Chapter 5]:

$$L = W$$ {#eq:lift-weight-equilibrium}

$$T = D$$ {#eq:thrust-drag-equilibrium}

where $L$ is lift, $W$ is aircraft weight, $T$ is thrust, and $D$ is drag. These fundamental equilibrium conditions form the basis for all performance analysis.

#### Lift equation

The aerodynamic lift force is expressed as [@torenbeekSynthesisSubsonicAirplane1982, Section 5.3]:

$$L = \frac{1}{2} \rho V^2 S C_L$$ {#eq:lift-equation}

where $L$ is lift force (N), $\rho$ is air density (kg/m³), $V$ is true airspeed (m/s), $S$ is wing reference area (m²), and $C_L$ is the lift coefficient (dimensionless).

For level flight where $L = W$, the lift coefficient required to maintain altitude at a given speed is:

$$C_L = \frac{2W}{\rho V^2 S} = \frac{2(W/S)}{\rho V^2}$$ {#eq:cl-required}

This equation reveals a fundamental constraint for Mars flight: the low atmospheric density ($\rho \approx 0.02000$ kg/m³) requires either high airspeed, large wing area, or high lift coefficient to generate sufficient lift.

The total aerodynamic drag is [@torenbeekSynthesisSubsonicAirplane1982, Section 5.3]:

$$D = \frac{1}{2} \rho V^2 S C_D$$ {#eq:drag-equation}

The drag coefficient is modeled using the parabolic drag polar from @eq:drag-polar (per @sec:aerodynamic-analysis):

$$C_D = C_{D,0} + \frac{C_L^2}{\pi \cdot AR \cdot e}$$

where $C_{D,0}$ is the zero-lift drag coefficient, $AR$ is the wing aspect ratio, and $e$ is the Oswald span efficiency factor. The first term represents parasite drag (skin friction, form drag, interference), which is independent of lift. The second term is induced drag, arising from the finite span wing and proportional to $C_L^2$.

Using the values from @tbl:aero-coefficients: $C_{D,0}$ = 0.03000, $e$ = 0.8692, $AR$ = 6.

### Lift-to-drag ratio

#### L/D from the drag polar

The lift-to-drag ratio quantifies aerodynamic efficiency and directly determines cruise performance [@torenbeekSynthesisSubsonicAirplane1982, Section 5.4]:

$$\frac{L}{D} = \frac{C_L}{C_D} = \frac{C_L}{C_{D,0} + C_L^2/(\pi \cdot AR \cdot e)}$$ {#eq:ld-ratio}

#### Maximum lift-to-drag ratio

From @eq:ld-max-calculated and @eq:cl-optimum in @sec:aerodynamic-analysis, the maximum L/D occurs at the optimal lift coefficient where induced drag equals parasite drag:

$$C_L^* = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = 0.7011$$

$$(L/D)_\text{max} = \frac{1}{2}\sqrt{\frac{\pi \cdot AR \cdot e}{C_{D,0}}} = 11.68$$

This maximum L/D of 11.68 represents an improvement over rotorcraft ($(L/D)_\text{eff}$ = 4.000, per @sec:rotorcraft-analysis) by a factor of approximately 3.

#### Speed for maximum L/D

The airspeed at which $(L/D)_\text{max}$ occurs is found by substituting $C_L^*$ into @eq:cl-required:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2(W/S)}{\rho C_L^*}}$$ {#eq:v-ld-max}

For the Mars UAV with estimated $W/S \approx 14.42$ N/m² (from stall constraint at $V_\text{min}$ = 35.04 m/s), $\rho$ = 0.01960 kg/m³, and $C_L^*$ = 0.7011:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2 \times 14.42}{0.01960 \times 0.7011}} = \sqrt{2099} = 45.82 \text{ m/s}$$

This optimal speed is above the design cruise velocity of 40.00 m/s, indicating that the Mars UAV will operate at a lift coefficient higher than $C_L^*$ during cruise (in the induced drag-dominated regime). At 40.00 m/s, the actual L/D remains close to maximum (approximately 11.0 for the pure wing, reduced slightly for the QuadPlane configuration due to stopped rotor drag).

### Cruise power analysis

#### Power required for level flight

The power required to overcome drag in level flight is the product of drag force and velocity [@torenbeekSynthesisSubsonicAirplane1982, Section 5.4]:

$$P_\text{aero} = D \times V$$ {#eq:power-aero}

Since $D = W/(L/D)$ in equilibrium:

$$P_\text{aero} = \frac{W \times V}{L/D}$$ {#eq:power-required}

This is the aerodynamic power that must be delivered to the airstream to maintain level flight.

#### Shaft power and propeller efficiency

The shaft power required from the motor accounts for propeller efficiency [@torenbeekSynthesisSubsonicAirplane1982, Section 5.3.4]:

$$P_\text{shaft} = \frac{P_\text{aero}}{\eta_\text{prop}} = \frac{W \times V}{(L/D) \times \eta_\text{prop}}$$ {#eq:shaft-power}

where $\eta_\text{prop}$ is the propeller efficiency. At low Reynolds numbers on Mars, propeller efficiency is degraded compared to Earth conditions.

#### Electrical power

Including motor and ESC efficiencies, the electrical power drawn from the battery is:

$$P_\text{electric} = \frac{P_\text{shaft}}{\eta_\text{motor} \times \eta_\text{ESC}} = \frac{W \times V}{(L/D) \times \eta_\text{prop} \times \eta_\text{motor} \times \eta_\text{ESC}}$$ {#eq:cruise-electric-power}

The combined propulsive efficiency is given by @eq:cruise-efficiency:

$$\eta_\text{cruise} = \eta_\text{prop} \times \eta_\text{motor} \times \eta_\text{ESC}$$

Using the efficiency values from @tbl:efficiency-parameters ($\eta_\text{prop}$ = 0.5500, $\eta_\text{motor}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), the combined cruise efficiency is $\eta_\text{cruise}$ = 0.4436.

#### Power loading formulation

Expressing the power requirement as power loading (power per unit weight):

$$\frac{P}{W} = \frac{V}{(L/D) \times \eta_\text{cruise}}$$ {#eq:power-loading-cruise}

For cruise at $V$ = 40.00 m/s with $(L/D)$ = 11.68 and $\eta_\text{cruise}$ = 0.4436:

$$\frac{P}{W} = \frac{40.00}{11.68 \times 0.4436} = 7.719 \text{ W/N}$$

Converting to W/kg using Mars gravity ($g_\text{Mars}$ = 3.711 m/s²):

$$\frac{P}{m} = 7.719 \times 3.711 = 28.64 \text{ W/kg}$$ {#eq:cruise-power-loading}

For the baseline MTOW of 10.00 kg (weight $W$ = 37.11 N), the cruise power is:

$$P_\text{cruise} = 7.719 \times 37.11 = 286.4 \text{ W}$$

This is lower than the 3178 W hover power requirement calculated in @sec:rotorcraft-analysis by a factor of 11, showing the power reduction achieved by fixed-wing cruise.

### Stall constraint

#### Stall speed

The minimum flight speed (stall speed) occurs at maximum lift coefficient. From @eq:stall-speed-prelim in @sec:mission-parameters:

$$V_\text{stall} = \sqrt{\frac{2W}{\rho S C_{L,\text{max}}}} = \sqrt{\frac{2(W/S)}{\rho C_{L,\text{max}}}}$$

This equation establishes the relationship between wing loading and stall speed.

#### Wing loading constraint

The stall constraint, expressed as a maximum allowable wing loading, is derived from @eq:wing-loading-constraint in @sec:mission-parameters:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

Using $C_{L,\text{max}}$ = 1.200 (from @tbl:aero-coefficients), $\rho$ = 0.01960 kg/m³, and $V_\text{min}$ = 35.04 m/s (where $V_\text{min}$ = 1.2 × $V_\text{stall}$ per @eq:v-min-constraint, with $V_\text{stall}$ = 29.2 m/s):

$$\frac{W}{S} \leq \frac{1}{2} \times 0.01960 \times 35.04^2 \times 1.200 = 14.42 \text{ N/m}^2$$

This constrains the maximum allowable wing loading. On a matching chart, this appears as a vertical line (constant $W/S$) independent of power loading.

The wing loading constraint on Mars is extremely low compared to Earth aircraft (typical $W/S$ = 1500-5000 N/m² for light aircraft). This is a direct consequence of the thin atmosphere and represents a significant driver of aircraft geometry.

### Endurance analysis

#### Battery energy model

The available energy from the battery uses @eq:battery-energy-fraction from @sec:battery-utilisation:

$$E_\text{available} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Substituting the parameter values from @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) and @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500), the usable energy per unit MTOW is 71.82 Wh/kg. For the baseline MTOW = 10.00 kg, the available energy is $E_\text{available}$ = 718.2 Wh.

#### Fixed-wing endurance equation

For electric fixed-wing aircraft at constant speed, endurance is:

$$t_\text{endurance} = \frac{E_\text{available}}{P_\text{electric}}$$ {#eq:endurance-definition-fw}

Substituting the expressions for available energy and cruise power:

$$t_\text{endurance} = \frac{f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}}{W \times V / ((L/D) \times \eta_\text{cruise})}$$

Since $W = MTOW \times g_\text{Mars}$, the MTOW terms cancel:

$$t_\text{endurance} = \frac{f_\text{batt} \times e_\text{spec} \times DoD \times \eta_\text{batt} \times (L/D) \times \eta_\text{cruise}}{g_\text{Mars} \times V}$$ {#eq:endurance-fixedwing}

This is the endurance equation for fixed-wing configuration. Note that endurance is independent of MTOW for fixed mass fractions—the same result as for rotorcraft (@eq:endurance-simple).

#### Endurance calculation

Using the parameter values from @sec:derived-requirements:

: Parameters for fixed-wing endurance calculation {#tbl:fw-endurance-parameters}

| Parameter | Symbol | Value | Unit |
|:----------|:------:|------:|:-----|
| Battery fraction | $f_\text{batt}$ | 0.3500 | - |
| Specific energy | $e_\text{spec}$ | 270.0 | Wh/kg |
| Depth of discharge | $DoD$ | 0.8000 | - |
| Battery efficiency | $\eta_\text{batt}$ | 0.9500 | - |
| Lift-to-drag ratio | $(L/D)$ | 11.68 | - |
| Cruise efficiency | $\eta_\text{cruise}$ | 0.4436 | - |
| Mars gravity | $g_\text{Mars}$ | 3.711 | m/s² |
| Cruise velocity | $V$ | 40.00 | m/s |

Converting specific energy to J/kg: $e_\text{spec} = 270 \times 3600 = 972{,}000$ J/kg

Substituting into @eq:endurance-fixedwing:

$$t_\text{endurance} = \frac{0.35 \times 972{,}000 \times 0.80 \times 0.95 \times 11.7 \times 0.444}{3.711 \times 40}$$

$$t_\text{endurance} = \frac{1{,}076{,}267}{148.44} = 7{,}251 \text{ s} \approx 121 \text{ min}$$ {#eq:endurance-fw-result}

The fixed-wing configuration achieves approximately 2 hours of endurance, exceeding the 60-minute requirement by 101%.

#### Range calculation

At the cruise velocity of 40 m/s:

$$R = V \times t_\text{endurance} = 40 \times 7{,}251 = 290{,}040 \text{ m} \approx 289 \text{ km}$$

The theoretical range of approximately 289 km far exceeds the 100 km round-trip requirement for the 50 km operational radius.

### Takeoff and landing problem

The fixed-wing configuration demonstrates excellent cruise performance. However, it cannot satisfy the mission requirement for VTOL operations. This section quantifies the takeoff constraint that disqualifies pure fixed-wing from consideration.

#### Ground roll analysis

The takeoff ground roll distance for a conventional takeoff is [@torenbeekSynthesisSubsonicAirplane1982; @sadraeyAircraftDesignSystems2013]:

$$S_\text{TO} = \frac{V_\text{TO}^2}{2 \bar{a}}$$ {#eq:takeoff-roll}

where $V_\text{TO} \approx 1.1 \times V_\text{stall}$ is the liftoff speed and $\bar{a}$ is the average acceleration during the ground roll.

The average acceleration depends on the balance of forces:

$$\bar{a} = \frac{g}{W} \left[ T - D - \mu_r (W - L) \right]_\text{avg}$$ {#eq:takeoff-accel}

where $\mu_r$ is the rolling friction coefficient (typically 0.02-0.05 on hard surfaces).

#### Mars-specific effects on takeoff

On Mars, several factors increase the takeoff distance:

Regarding low density effect on stall speed, the stall speed scales inversely with the square root of density. For the Mars UAV with $W/S$ = 14.42 N/m² (at the stall constraint limit), $C_{L,\text{max}}$ = 1.20, and $\rho$ = 0.0196 kg/m³:

$$V_\text{stall} = \sqrt{\frac{2 \times 14.42}{0.0196 \times 1.20}} = \sqrt{1225} = 35.0 \text{ m/s}$$

$$V_\text{TO} = 1.1 \times 35.0 = 38.5 \text{ m/s}$$

Regarding low density effect on acceleration, both thrust (from propeller) and rolling friction assistance (from lift during roll) are reduced by low density. Thrust available from a propeller scales approximately with density, and the lift that relieves wheel loading is also reduced.

For the estimated ground roll, using the standard ground roll estimation with available thrust and Mars conditions, assuming an average acceleration of approximately $a \approx 0.7$ m/s² (accounting for reduced thrust and gravity):

$$S_\text{TO} = \frac{38.5^2}{2 \times 0.7000} = \frac{1482}{1.400} = 1059 \text{ m}$$ {#eq:takeoff-distance}

The takeoff ground roll of approximately 1060 m is impractical for Mars operations—no prepared runway of this length exists or can reasonably be constructed near a habitat.

Even with wing loading constrained by the stall speed requirement (14.42 N/m² at the design point), the required runway length is prohibitive. The problem is that low atmospheric density requires substantial ground roll distance regardless of wing sizing.

#### Alternative launch methods

Several alternative launch methods exist for fixed-wing aircraft without runways, but none are practical for Mars operations from a habitat.

Catapult or rail launch requires substantial ground infrastructure including the launcher mechanism, guide rails, and energy storage systems, none of which are available in a Mars habitat environment. This approach adds operational complexity and crew workload, as each launch requires setup and recovery of equipment.

Rocket-assisted takeoff (RATO) requires solid rocket boosters that add significant mass and are single-use per flight, requiring multiple sets for repeated operations. This method presents a safety hazard near a crewed habitat, and exhaust products may contaminate science operations.

Balloon-drop launch requires carrying the aircraft to altitude by balloon before releasing it, but no balloon infrastructure exists on Mars. This approach adds complexity to the operations concept, and ascent time combined with positioning constraints limits operational flexibility.

Air-launch from a carrier aircraft is not applicable because no carrier aircraft exists on Mars.

All alternative launch methods fail the operational requirements for repeated, autonomous operations from a Mars habitat without complex infrastructure.

#### Landing problem

Conventional landing presents similar challenges. The approach speed of approximately $V_\text{approach} \approx 1.3 \times V_\text{stall}$ = 45.5 m/s is high. Deceleration is limited by low friction forces, requiring hundreds to thousands of metres of landing roll. A prepared surface is required to avoid obstacles and provide consistent braking. The high approach speed also increases sensitivity to wind disturbances. The landing problem is potentially more constraining than takeoff, as there is less margin for error and no opportunity for a go-around in an emergency without hover capability.

### Feasibility assessment

#### Requirements compliance

@tbl:fw-feasibility compares fixed-wing capability against mission requirements:

: Fixed-wing feasibility assessment {#tbl:fw-feasibility}

| Requirement | Target | Fixed-wing capability | Status |
|:------------|:-------|:----------------------|:------:|
| Cruise endurance | 60-90 min | 120.5 min | PASS |
| Operational radius | 50 km | 144.5 km | PASS |
| VTOL capability | Required | Not possible | FAIL |
| Runway requirement | None | 1060 m ground roll | FAIL |

The fixed-wing configuration exceeds the endurance and range requirements (endurance margin +101% over the 60-minute requirement), showing the effect of high L/D cruise. However, it fails the VTOL requirement, which is non-negotiable for Mars operations without runway infrastructure.

### Fixed-wing configuration conclusion

The pure fixed-wing configuration cannot satisfy the VTOL requirement for Mars UAV operations.

Despite achieving $(L/D)$ = 11.68 and demonstrating theoretical endurance (120.5 min with 20% energy reserve) and range (289 km) that substantially exceed mission requirements, the fixed-wing configuration cannot take off or land without a prepared runway of approximately 1060 m. Such infrastructure does not exist on Mars and cannot reasonably be constructed for repeated UAV operations from a crewed habitat.

The fixed-wing analysis demonstrates three key points. First, aerodynamic efficiency is not the limiting factor for Mars UAV endurance; rather, the infrastructure constraint (VTOL) dominates configuration selection. Second, moderate L/D is achievable with careful airfoil selection at the low Reynolds numbers characteristic of Mars flight, though values are lower than Earth aircraft due to the challenging aerodynamic environment. Third, fixed-wing cruise should be exploited in any feasible configuration to maximise range and endurance.

The feasibility assessment for the fixed-wing configuration is summarised in @tbl:fw-feasibility. The configuration comparison and selection rationale are presented in @sec:architecture-selection.
