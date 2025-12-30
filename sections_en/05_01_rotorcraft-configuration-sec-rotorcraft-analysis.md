# Constraint analysis

## Rotorcraft configuration {#sec:rotorcraft-analysis}

This section evaluates whether a pure rotorcraft (helicopter or multicopter) configuration can satisfy the Mars UAV mission requirements. The analysis develops the theoretical framework for hover power, forward flight power, and endurance, culminating in a feasibility assessment against the 60-minute endurance requirement.

### Hover power analysis

#### Momentum theory fundamentals {#sec:momentum-theory}

The rotor performance in hover is analysed using Rankine-Froude momentum theory, which treats the rotor as an infinitely thin actuator disk that imparts momentum to the air passing through it [@leishmanPrinciplesHelicopterAerodynamics2006]. This idealised model, despite its simplicity, provides insight into rotor performance and the relationship between thrust, power, and disk loading.

The momentum theory makes the following assumptions: uniform, steady flow through the rotor disk; inviscid flow with no swirl in the wake; incompressible conditions (valid for $M < 0.3$); and one-dimensional flow through a well-defined slipstream.

From the principle of conservation of fluid momentum, the rotor thrust equals the time rate of change of momentum of the air passing through the rotor disk. For a hovering rotor with induced velocity $v_i$ at the disk plane, the thrust is [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$T = \dot{m} \cdot w = 2\rho A v_i^2$$ {#eq:thrust-momentum}

where $\dot{m} = \rho A v_i$ is the mass flow rate through the disk, $w = 2v_i$ is the wake velocity far downstream (from energy conservation), $\rho$ is the air density, and $A$ is the rotor disk area.

Solving @eq:thrust-momentum for the induced velocity at the rotor disk yields [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$v_i = \sqrt{\frac{T}{2\rho A}}$$ {#eq:induced-velocity}

This fundamental result shows that induced velocity scales with the square root of thrust and inversely with disk area and density. The induced velocity can also be expressed in terms of disk loading ($DL = T/A$):

$$v_i = \sqrt{\frac{DL}{2\rho}}$$ {#eq:induced-velocity-dl}

The ideal power required to hover is the product of thrust and induced velocity [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{ideal} = T \cdot v_i = T \sqrt{\frac{T}{2\rho A}}$$ {#eq:ideal-power-1}

Rearranging:

$$P_\text{ideal} = \frac{T^{3/2}}{\sqrt{2\rho A}}$$ {#eq:ideal-power}

This equation reveals scaling relationships: power scales as $T^{3/2}$, meaning hover power increases more rapidly than thrust; power scales as $\rho^{-1/2}$, so low atmospheric density substantially increases power requirements; and power scales as $A^{-1/2}$, favouring large rotor disk areas.

For hovering flight where thrust equals weight ($T = W$):

$$P_\text{ideal} = \frac{W^{3/2}}{\sqrt{2\rho A}} = W \sqrt{\frac{DL}{2\rho}} = W \sqrt{\frac{W/A}{2\rho}}$$ {#eq:ideal-power-weight}

#### Figure of merit {#sec:figure-of-merit}

The momentum theory result represents an idealised lower bound on hover power. Real rotors experience additional losses from profile drag on the blade sections, non-uniform inflow distribution, tip losses (finite blade effects), and swirl in the wake.

The figure of merit (FM) quantifies the efficiency of a real rotor relative to the ideal momentum theory prediction [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$FM = \frac{P_\text{ideal}}{P_\text{actual}} < 1$$ {#eq:figure-of-merit}

Rearranging to obtain actual hover power:

$$P_\text{hover} = \frac{P_\text{ideal}}{FM} = \frac{T^{3/2}}{FM \cdot \sqrt{2\rho A}}$$ {#eq:hover-power}

The figure of merit adopted for Mars rotorcraft sizing ($FM$ = 0.4000) is documented in @sec:propulsion-efficiency, representing a conservative estimate within the expected range of 0.30-0.50 for low-Reynolds MAV rotor operation.

#### Electrical power requirements

The electrical power drawn from the battery must account for losses in the motor and electronic speed controller (ESC):

$$P_\text{electric,hover} = \frac{P_\text{hover}}{\eta_\text{motor} \cdot \eta_\text{ESC}}$$ {#eq:electric-hover}

Substituting the hover power equation:

$$P_\text{electric,hover} = \frac{W^{3/2}}{FM \cdot \eta_\text{motor} \cdot \eta_\text{ESC} \cdot \sqrt{2\rho A}}$$ {#eq:electric-hover-full}

The combined efficiency chain from battery to rotor thrust is given by @eq:hover-efficiency:

$$\eta_\text{hover} = FM \cdot \eta_\text{motor} \cdot \eta_\text{ESC}$$

Using the efficiency values from @tbl:efficiency-parameters ($FM$ = 0.4000, $\eta_\text{motor}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), the combined hover efficiency is $\eta_\text{hover}$ = 0.3230.

This means only 32% of the electrical energy from the battery produces useful thrust power in hover. The remaining 68% is lost to rotor profile drag, non-ideal inflow effects, motor copper and iron losses, and ESC switching losses.

#### Power loading constraint

The power loading (thrust per unit power) for hover can be expressed by rearranging @eq:hover-power:

$$\frac{P_\text{hover}}{W} = \frac{1}{FM} \cdot \sqrt{\frac{W/A}{2\rho}} = \frac{1}{FM} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-power-loading}

This equation defines the hover constraint on the matching chart. For a given disk loading and atmospheric density, the required power-to-weight ratio is fixed and independent of wing loading. On a matching chart with P/W on the vertical axis and W/S on the horizontal axis, the hover constraint appears as a horizontal line.

Including the electrical efficiency chain:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{FM \cdot \eta_\text{motor} \cdot \eta_\text{ESC}} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint}

### Forward flight performance

#### Power components in forward flight

In forward flight, the total power required by a rotorcraft comprises multiple components [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{total} = P_i + P_0 + P_p + P_c$$ {#eq:forward-power-components}

where $P_i$ is induced power (to generate lift), $P_0$ is profile power (to overcome blade section drag), $P_p$ is parasite power (to overcome fuselage and hub drag), and $P_c$ is climb power (to change gravitational potential energy).

For level cruise flight ($P_c = 0$), the power breakdown follows a characteristic pattern: at low speeds, induced power dominates (similar to hover); as speed increases, induced power decreases (rotor acts more like a wing); and at high speeds, parasite power dominates (scales as $V^3$).

The minimum power speed occurs where the sum of these components reaches a minimum, typically at an advance ratio $\mu = V/(\Omega R) \approx 0.15$-0.25.

#### Equivalent lift-to-drag ratio

For comparison with fixed-wing aircraft, the rotorcraft forward flight efficiency can be expressed as an equivalent lift-to-drag ratio [@leishmanPrinciplesHelicopterAerodynamics2006, Chapter 1]:

$$\left(\frac{L}{D}\right)_\text{eff} = \frac{W \cdot V}{P_\text{total}}$$ {#eq:equivalent-ld}

This parameter represents the overall aerodynamic efficiency of the rotorcraft in forward flight, incorporating all power losses. Rearranging:

$$P_\text{forward} = \frac{W \cdot V}{(L/D)_\text{eff}}$$ {#eq:forward-power-ld}

Typical equivalent L/D values are summarised in @tbl:rotorcraft-ld. The relatively poor aerodynamic efficiency arises from several factors inherent to rotorcraft: the rotor hub and blade attachments create substantial parasite drag; profile drag on the blade sections is unavoidable, even at high speed; the advancing blade experiences compressibility effects at high speed; and the retreating blade may experience stall, limiting forward speed.

For a Mars rotorcraft without a wing, the equivalent L/D is $(L/D)_\text{eff}$ = 4.000, representing the lower end of the helicopter range due to the absence of design optimisation found in Earth helicopters (per @sec:rotorcraft-ld).

#### Forward flight electrical power

Including the electrical efficiency chain, the power from the battery for forward flight is:

$$P_\text{electric,forward} = \frac{W \cdot V}{(L/D)_\text{eff} \cdot \eta_\text{motor} \cdot \eta_\text{ESC}}$$ {#eq:forward-electric-power}

### Endurance analysis

#### Battery energy model

The usable energy from the battery is derived from @eq:battery-energy-fraction in @sec:battery-utilisation:

$$E_\text{available} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Substituting the parameter values from @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) and @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500):

$$\frac{E_\text{available}}{MTOW} = 0.3500 \times 270.0 \times 0.8000 \times 0.9500 = 71.82 \text{ Wh/kg}$$

For the baseline MTOW = 10.00 kg:

$$E_\text{available} = 71.82 \times 10.00 = 718.2 \text{ Wh}$$

#### Rotorcraft endurance equation

For a rotorcraft in forward flight, the endurance is determined by the available energy and power consumption:

$$t_\text{endurance} = \frac{E_\text{available}}{P_\text{electric,forward}}$$ {#eq:endurance-definition}

Substituting the expressions for available energy (@eq:battery-energy-fraction) and forward flight power (@eq:forward-electric-power):

$$t_\text{endurance} = \frac{f_\text{batt} \cdot MTOW \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt}}{W \cdot V / ((L/D)_\text{eff} \cdot \eta_\text{motor} \cdot \eta_\text{ESC})}$$ {#eq:endurance-expanded}

Since $W = MTOW \cdot g_\text{Mars}$, the MTOW terms cancel:

$$t_\text{endurance} = \frac{f_\text{batt} \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt} \cdot (L/D)_\text{eff} \cdot \eta_\text{motor} \cdot \eta_\text{ESC}}{g_\text{Mars} \cdot V}$$ {#eq:endurance-simple}

This result shows that rotorcraft endurance is independent of MTOW (for fixed mass fractions). Endurance depends on battery parameters ($f_\text{batt}$, $e_\text{spec}$, $DoD$, $\eta_\text{batt}$), aerodynamic efficiency ($(L/D)_\text{eff}$), propulsion efficiency ($\eta_\text{motor}$, $\eta_\text{ESC}$), and flight conditions ($g_\text{Mars}$, $V$).

#### Endurance calculation

Using the parameter values from @sec:derived-requirements:

: Parameters for rotorcraft endurance calculation {#tbl:endurance-parameters}

| Parameter | Symbol | Value | Unit |
|:----------|:------:|------:|:-----|
| Battery fraction | $f_\text{batt}$ | 0.3500 | - |
| Specific energy | $e_\text{spec}$ | 270.0 | Wh/kg |
| Depth of discharge | $DoD$ | 0.8000 | - |
| Battery efficiency | $\eta_\text{batt}$ | 0.9500 | - |
| Equivalent L/D | $(L/D)_\text{eff}$ | 4.000 | - |
| Motor efficiency | $\eta_\text{motor}$ | 0.8500 | - |
| ESC efficiency | $\eta_\text{ESC}$ | 0.9500 | - |
| Mars gravity | $g_\text{Mars}$ | 3.711 | m/s² |
| Cruise velocity | $V$ | 40.00 | m/s |

Converting specific energy to J/kg: $e_\text{spec} = 270.0 \times 3600 = 972000$ J/kg

Substituting into @eq:endurance-simple:

$$t_\text{endurance} = \frac{0.3500 \times 972000 \times 0.8000 \times 0.9500 \times 4.000 \times 0.8500 \times 0.9500}{3.711 \times 40.00}$$

$$t_\text{endurance} = \frac{849706}{148.44} = 5723 \text{ s} = 95.39 \text{ min}$$ {#eq:endurance-result}

This calculation represents the theoretical maximum endurance assuming 100% of flight time is spent in efficient forward cruise. The practical endurance is lower due to hover phases and reserve requirements, as analysed in the feasibility assessment below.

### Feasibility assessment

#### Critical analysis of rotorcraft endurance

The 95.39-minute theoretical endurance calculated above exceeds the 60-minute requirement, but several factors reduce the achievable endurance for a pure rotorcraft mission.

A pure rotorcraft cannot use fixed-wing cruise. The $(L/D)_\text{eff}$ = 4.000 applies to helicopter forward flight, which is less efficient than fixed-wing cruise.

The mission profile requires hover for takeoff, landing, and contingency. Using @eq:hover-power and the hover efficiency of 0.3230, hover power consumption exceeds cruise power. For the baseline MTOW = 10.00 kg with disk loading $DL$ = 30.00 N/m² and Mars density $\rho$ = 0.01960 kg/m³, the induced velocity is:

$$v_i = \sqrt{\frac{30.00}{2 \times 0.01960}} = \sqrt{765.3} = 27.68 \text{ m/s}$$

The hover power requirement is:

$$P_\text{hover} = \frac{W \cdot v_i}{FM \cdot \eta_\text{motor} \cdot \eta_\text{ESC}} = \frac{37.11 \times 27.68}{0.4000 \times 0.8500 \times 0.9500} = 3178 \text{ W}$$

This induced velocity is of the same order as the cruise velocity, and the hover power (3178 W) exceeds cruise power (~459.7 W), consuming significant energy during the 3-minute hover phases.

The 20% energy reserve reduces effective endurance.

A fixed-wing aircraft achieves $(L/D) \approx 12$, approximately three times higher than rotorcraft. This difference limits rotorcraft range and endurance.

#### Comparison with mission requirements

@tbl:rotorcraft-feasibility compares the pure rotorcraft capability against mission requirements:

: Rotorcraft feasibility assessment {#tbl:rotorcraft-feasibility}

| Requirement | Target | Rotorcraft capability | Status |
|:------------|:-------|:----------------------|:------:|
| Cruise endurance | ≥60 min | 57 min (with 20% reserve) | FAIL |
| Operational radius | ≥50 km | 65 km (130 km range) | PASS |
| VTOL capability | Required | Yes, inherent | PASS |
| Hover time | 3 min | Unlimited (power limited) | PASS |

The usable energy is 718.2 Wh × 0.80 (reserve) = 574.6 Wh. Hover energy (3 min at 3178 W) consumes 158.9 Wh, leaving 415.7 Wh for forward flight. Forward flight power is $P = WV/(L/D)_\text{eff}/\eta = 37.11 \times 40.00 / (4.000 \times 0.8075) = 459.7$ W. Forward flight time is 415.7 Wh / 459.7 W = 0.904 h = 54.27 min. Total endurance: 57.27 min. Range: 40.00 m/s × 54.27 min × 60 s/min = 130.2 km.

The rotorcraft configuration fails the endurance requirement (57 min vs 60 min required). Even if it marginally met the requirement, the margin would be insufficient:

#### Sensitivity analysis

The 57.27-minute endurance represents a -4.5% margin below the 60-minute requirement, which is unacceptable for a Mars mission.

Once the UAV departs the habitat, it must complete the mission. There is no alternative landing site.

Mars atmospheric density varies with season and dust loading. A 10% reduction in density increases power requirements by approximately 5%, further degrading performance.

Lithium batteries lose capacity over charge cycles and in extreme cold. Capacity degradation further reduces the already insufficient endurance.

If a rotor fails, a multirotor cannot glide to a safe landing.

For comparison, the hybrid VTOL configuration achieves 90 minutes endurance (+50% margin), providing greater operating margin. The configuration analysis and selection rationale are presented in @sec:architecture-selection.

### Rotorcraft configuration conclusion

The pure rotorcraft configuration fails to meet the minimum endurance requirement (57.27 min vs 60 min required), with a -4.5% margin that is unacceptable for mission operations. The configuration presents operational risks.

The 57.27-minute achievable endurance falls short of the 60-minute requirement by 2.73 minutes.

Any variation in atmospheric density, battery capacity, or efficiency values further degrades performance.

Unlike a hybrid VTOL that can glide if the cruise motor fails, a rotorcraft crashes immediately if any rotor fails.

The fundamental limitation is the low equivalent lift-to-drag ratio inherent to rotorcraft in forward flight ($(L/D)_\text{eff} \approx 4$), resulting in forward flight power consumption (460 W) approximately 45% higher than hybrid VTOL cruise (318 W).

The feasibility assessment for the rotorcraft configuration is summarised in @tbl:rotorcraft-feasibility. The configuration comparison and selection rationale are presented in @sec:architecture-selection.
