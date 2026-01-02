# Constraint analysis {#sec:constraint-analysis-hybrid}

## Hybrid VTOL configuration {#sec:hybrid-vtol-analysis}

This section evaluates whether a hybrid VTOL (QuadPlane) configuration can satisfy the Mars UAV mission requirements. The hybrid configuration combines the vertical takeoff and landing capability of rotorcraft with the efficient cruise performance of fixed-wing aircraft. The analysis demonstrates that this is the only configuration that satisfies all three requirements: VTOL capability, cruise endurance, and operational radius.

### QuadPlane architecture

#### Configuration description

The QuadPlane configuration consists of two distinct propulsion systems optimised for their respective flight regimes [@bertaniPreliminaryDesignFixedwing2023]<!-- #exec -->.

The lift system (for hover) comprises four or more electric rotors in a quadcopter or similar layout, sized for hover thrust only (short duration operation), positioned to minimise interference with wing aerodynamics, and inactive during cruise (stopped or folded).

The cruise system (for forward flight) uses a wing for lift generation and coaxial contra-rotating tractor propellers for thrust, sized for efficient cruise at $(L/D)_\text{max}$, and inactive during hover.

This architecture enables decoupled optimisation: each propulsion system operates only in its optimal regime. The lift rotors are sized for hover thrust without compromise for forward flight efficiency, while the wing and cruise propellers are optimised for maximum aerodynamic efficiency without VTOL capability requirements.

This approach contrasts with pure rotorcraft (where rotors must operate efficiently in both hover and forward flight) and tiltrotor concepts (where mechanical complexity is required for thrust vectoring).

#### Flight phases

The nominal mission profile comprises five flight phases, summarised in @tbl:quadplane-phases.

: QuadPlane flight phases {#tbl:quadplane-phases}

| Phase | Propulsion system | Lift source | Duration |
|:------|:-----------------|:------------|:---------|
| Takeoff | Lift rotors only | Rotor thrust | 60 s |
| Transition (Q2P) | Both systems | Rotors → Wing | 30 s |
| Cruise | Cruise motor only | Wing | 57 min |
| Transition (P2Q) | Both systems | Wing → Rotors | 30 s |
| Landing | Lift rotors only | Rotor thrust | 60 s |

The observation is that hover time is limited to approximately 2 minutes (120 s) of the total 60-minute mission, with an additional 1 minute allocated for transitions (two 30-second transitions). During the remaining 57 minutes, the aircraft operates as a conventional fixed-wing with the lift rotors inactive. This changes the energy budget compared to pure rotorcraft.

### Hover constraint

#### Reference to rotorcraft analysis

The hover power equations developed in @sec:rotorcraft-analysis apply directly to the QuadPlane lift system. From @eq:hover-power, the mechanical hover power is:

$$P_\text{hover} = \frac{W^{3/2}}{FM \cdot \sqrt{2\rho A}}$$ {#eq:hover-power-qp}

where $W$ is aircraft weight, $FM$ is figure of merit, $\rho$ is atmospheric density, and $A$ is the total rotor disk area.

Including electrical losses, the battery power for hover is:

$$P_\text{electric,hover} = \frac{P_\text{hover}}{\eta_\text{motor} \cdot \eta_\text{ESC}} = \frac{W^{3/2}}{FM \cdot \eta_\text{motor} \cdot \eta_\text{ESC} \cdot \sqrt{2\rho A}}$$ {#eq:electric-hover-qp}

Using the efficiency values from @tbl:efficiency-parameters ($FM$ = 0.4000, $\eta_\text{motor}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), the combined hover efficiency is $\eta_\text{hover}$ = 0.4000 × 0.8500 × 0.9500 = 0.3230, identical to the pure rotorcraft case.

#### Difference from rotorcraft: hover duration

The main advantage of the QuadPlane over pure rotorcraft is the reduced hover time. A pure rotorcraft uses hover or hover-like forward flight for the entire mission (approximately 60 min), while the QuadPlane hovers only during takeoff and landing (approximately 2 min).

This 30× reduction in hover time changes the energy equation. Even though hover is power-intensive, limiting it to approximately 3% of the mission duration makes the energy cost manageable.

#### Hover energy

The energy consumed during hover phases is:

$$E_\text{hover} = P_\text{electric,hover} \times t_\text{hover}$$ {#eq:hover-energy}

where $t_\text{hover} = 120$ s (2 min) from the hover time allocation in @sec:mission-parameters.

Using the baseline parameters (MTOW = 10.00 kg, disk loading $DL$ = 30.00 N/m²):

From @eq:induced-velocity-dl and @eq:hover-power:

$$v_i = \sqrt{\frac{DL}{2\rho}} = \sqrt{\frac{30.00}{2 \times 0.01960}} = \sqrt{765.3} = 27.68 \text{ m/s}$$

$$P_\text{ideal} = W \times v_i = (10.00 \times 3.711) \times 27.68 = 1027 \text{ W}$$

$$P_\text{electric,hover} = P_\text{ideal} / (FM \times \eta_\text{motor} \times \eta_\text{ESC}) = 1027 / 0.3230 = 3178 \text{ W}$$

Converting to energy:

$$E_\text{hover} = 3178 \times (120.0/3600) = 106.0 \text{ Wh}$$ {#eq:hover-energy-value}

This represents 15% of the available energy budget, which is manageable given the short hover duration.

### Cruise constraint

#### Reference to fixed-wing analysis

The cruise power equations developed in @sec:fixed-wing-analysis apply directly to the QuadPlane cruise phase. From @eq:cruise-electric-power, the electrical power for cruise is:

$$P_\text{electric,cruise} = \frac{W \times V}{(L/D) \times \eta_\text{prop} \times \eta_\text{motor} \times \eta_\text{ESC}}$$ {#eq:cruise-power-qp}

where $V$ is cruise velocity and $(L/D)$ is the lift-to-drag ratio.

#### QuadPlane aerodynamic efficiency

During cruise, the QuadPlane achieves fixed-wing aerodynamic efficiency because the lift rotors are inactive. Two design approaches are possible: stopped rotors (rotors remain stationary, contributing only parasitic drag), and folded rotors (rotor blades fold against the motor pods, minimising drag).

For stopped rotors, the parasitic drag of four motor pods with stationary propellers increases total drag by approximately 5-10% [@bertaniPreliminaryDesignFixedwing2023]<!-- #s:drag-penalty -->. This reduces the effective lift-to-drag ratio:

$$(L/D)_\text{QuadPlane} \approx 0.9000 \times (L/D)_\text{pure} = 0.9000 \times 11.68 = 10.51$$ {#eq:ld-quadplane}

For folded rotors, the drag penalty is smaller (approximately 2-5%), yielding $(L/D) \approx 0.9500 \times 11.68 = 11.10$.

A value of $(L/D)$ = 10.50 is adopted for the QuadPlane analysis, accounting for stopped rotors and their mounting hardware.

#### Cruise power

Using the values from @sec:derived-requirements ($V$ = 40.00 m/s, $(L/D)$ = 10.50, $\eta_\text{prop}$ = 0.5500, $\eta_\text{motor}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), the combined cruise efficiency is: $\eta_\text{cruise} = 0.5500 \times 0.8500 \times 0.9500 = 0.4436$.

For the baseline MTOW = 10.00 kg (weight $W$ = 37.11 N):

$$P_\text{electric,cruise} = \frac{10.0 \times 3.711 \times 40}{10.5 \times 0.444} = \frac{1484}{4.66} = 318.5 \text{ W}$$ {#eq:cruise-power-value}

This is approximately 10 times lower than the hover power (3178 W), showing the power difference between hover and cruise modes.

#### Cruise energy

The energy consumed during cruise phases is:

$$E_\text{cruise} = P_\text{electric,cruise} \times t_\text{cruise}$$ {#eq:cruise-energy}

where $t_\text{cruise}$ = 57.00 min (from @tbl:mission-profile, total flight 60 min minus 2 min hover minus 1 min transition).

Converting to hours:

$$E_\text{cruise} = 318.5 \times (57.00/60.00) = 302.6 \text{ Wh}$$ {#eq:cruise-energy-value}

### Transition phase analysis {#sec:transition-analysis}

#### Transition phase significance

The transition from hover to cruise (and back) represents a distinct flight phase that is often omitted in preliminary feasibility studies. Recent literature emphasises that "the phase which consumes a big amount of electric energy is the transition from the vertical to the horizontal flight" [@goetzendorf-grabowskiOptimizationEnergyConsumption2022]<!-- #s:transition -->. Wind tunnel testing has revealed that simplified transition models significantly underestimate actual energy needs by not accounting for propeller drag effects in the airflow.

A counter-intuitive finding from multi-mode flight simulation is that hybrid mode (during transition) can consume higher power than pure hover mode at certain airspeeds, because of the additional forward thrust required to maintain desired pitch angle while lift rotors remain active [@mathurMultiModeFlightSimulation2025]<!-- #s:hybrid-paradox -->. This phenomenon—termed the "hybrid mode power paradox"—means transition energy cannot be estimated by simple interpolation between hover and cruise power levels.

For the Mars UAV, transition dynamics are further complicated by the thin atmosphere and different gravity, affecting both aerodynamic forces and propulsion efficiency during the acceleration/deceleration phases.

#### Conservative transition energy estimate

Given the complexity of transition modelling and the limited applicability of Earth-based measurements to Mars conditions, a conservative approach is adopted: transition energy is explicitly estimated and added to the energy budget rather than being ignored or absorbed into hover time.

Reference data from @goetzendorf-grabowskiOptimizationEnergyConsumption2022<!-- #tbl:energy --> shows transition energy of approximately 45 kJ per transition for the PW Chimera, a 25 kg quad-plane tested under Earth conditions (baseline scenario without optimisation). Optimised transition trajectories achieved approximately 37 kJ per transition, representing a 20-42% reduction through trajectory shaping.

For the 10 kg Mars UAV, the reference energy is scaled linearly with mass:

$$E_\text{trans,10kg} = E_\text{trans,25kg} \times \frac{m_\text{UAV}}{m_\text{ref}} = 45 \times \frac{10}{25} = 18 \text{ kJ}$$ {#eq:transition-scaling}

Linear mass scaling is a first-order approximation based on the observation that transition energy is dominated by kinetic energy changes ($\tfrac{1}{2}mv^2$) and work against gravity ($mgh$), both proportional to mass. This scaling is conservative: the reference vehicle's higher wing loading (25 kg / 1.2 m² = 20.8 kg/m²) compared to the Mars UAV's lower wing loading (10 kg / 0.91 m² ≈ 11 kg/m²) suggests slower transition speeds may be achievable, potentially reducing energy below the linear scaling estimate.

For the Mars UAV mission with two transitions (Q2P after takeoff and P2Q before landing):

$$E_\text{transition} = n_\text{transitions} \times E_\text{per\_transition}$$ {#eq:transition-energy}

$$E_\text{transition} = 2 \times \frac{18{,}000 \text{ J}}{3600 \text{ J/Wh}} = 10.0 \text{ Wh}$$ {#eq:transition-energy-value}

This represents approximately 9% of the pure hover energy (106 Wh) or 2.4% of the total mission energy. While modest in absolute terms, explicitly accounting for this energy provides a more accurate budget and maintains design margins.

#### Literature context

The approach of omitting transition energy is common in preliminary design. A NASA simulation study explicitly stated that "the power required and energy consumption during the transition between the flight phases have been ignored in this study" [@kulkarniSimulationStudiesUrban2022]<!-- #s:simplification -->. However, for a Mars UAV where energy margins directly determine mission success, explicit modelling is preferred even if simplified.

Transition corridor theory from tilt-rotor VTOL analysis establishes that feasible transitions occur within a bounded region of the velocity-tilt angle space, constrained by stall limits at low speeds and available power at high speeds [@zhaoDevelopmentMultimodeFlight2023]<!-- #s:corridor -->. For a QuadPlane, the transition corridor is simpler since the tilt mechanism is replaced by a power transfer between propulsion systems, but the lift balance constraints remain relevant.

Pattern flight simulations show that quad-mode operations (climb/descent) consume nearly 50% of total mission energy despite being a small fraction of flight time [@mathurMultiModeFlightSimulation2025]<!-- #s:quad-mode -->. This supports the finding that vertical flight phases dominate the energy budget even when duration is limited.

#### Limitations of the transition energy model

The transition energy estimate used here is a simplified energy-only model with several acknowledged limitations:

1. The linear mass scaling assumes transition energy scales proportionally with vehicle mass. This is a first-order approximation; actual scaling may be non-linear due to Reynolds number effects on rotor and wing performance, and different power-to-weight ratios between the reference vehicle and the Mars UAV.
2. The model does not capture peak transition power. During transition, instantaneous power demand may exceed steady hover power due to the simultaneous operation of lift rotors (providing residual lift) and forward thrust (for acceleration). The "hybrid mode power paradox" identified by @mathurMultiModeFlightSimulation2025<!-- #s:hybrid-paradox --> shows that at certain airspeeds, hybrid mode power exceeds pure hover power. This peak power constraint is not evaluated; the analysis assumes the propulsion system sized for hover can accommodate transition power demands.
3. The model does not address power-limited feasibility in the transition corridor sense. Transition corridor theory [@zhaoDevelopmentMultimodeFlight2023]<!-- #s:corridor --> establishes that feasible transitions must remain within a bounded region of velocity-pitch space, constrained by stall limits and available power. The current analysis verifies energy sufficiency but does not verify that a feasible transition trajectory exists within the power envelope.

These limitations are acceptable for a preliminary feasibility assessment, where the objective is to screen configurations and establish that adequate energy margins exist. Detailed transition trajectory analysis and power verification would be required in subsequent design phases.

### Energy storage constraint {#sec:energy-constraint}

The energy storage constraint is specific to hybrid VTOL, combining the power-intensive hover phases with the energy-intensive cruise phase. This constraint couples the mission profile to the mass allocation.

#### Total energy requirement

The battery must provide energy for all flight phases—including the transition phases now explicitly modelled—plus an energy reserve:

$$E_\text{required} = E_\text{hover} + E_\text{transition} + E_\text{cruise} + E_\text{reserve}$$ {#eq:energy-required}

The energy reserve accounts for navigation inefficiencies and course corrections, atmospheric density variations from the model, extended hover for precision landing or abort, and emergency return capability.

A 20% energy reserve is adopted as consistent with aviation practice and the design approach in @sec:mission-parameters:

$$E_\text{reserve} = 0.2000 \times (E_\text{hover} + E_\text{transition} + E_\text{cruise})$$ {#eq:energy-reserve}

The total required energy is therefore:

$$E_\text{required} = 1.200 \times (E_\text{hover} + E_\text{transition} + E_\text{cruise})$$ {#eq:energy-required-total}

Substituting the calculated values from hover analysis (@eq:hover-energy-value: 106 Wh for 2 min pure hover), transition estimate (@eq:transition-energy-value: 10 Wh), and cruise analysis (@eq:cruise-energy-value: 302 Wh):

$$E_\text{required} = 1.200 \times (106.0 + 10.0 + 302.0) = 1.200 \times 418.0 = 501.6 \text{ Wh}$$ {#eq:energy-required-value}

The available energy from the battery is determined by @eq:battery-energy-fraction from @sec:battery-utilisation:

$$E_\text{available} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Substituting the values from @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500, MTOW = 10.00 kg, $e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500):

$$E_\text{available} = 0.3500 \times 10.00 \times 270.0 \times 0.8000 \times 0.9500 = 718.2 \text{ Wh}$$ {#eq:energy-available-value-qp}

#### Energy constraint verification

The mission is feasible if:

$$E_\text{available} \geq E_\text{required}$$ {#eq:energy-feasibility}

Since 718.2 Wh ≥ 501.6 Wh, the energy constraint is satisfied.

The energy margin is:

$$\text{Margin} = \frac{E_\text{available} - E_\text{required}}{E_\text{required}} = \frac{718.2 - 501.6}{501.6} = 43.2\%$$

This margin indicates that the baseline design satisfies the energy constraint with adequate reserve beyond the 20% already included. This margin can be used for extended mission range (beyond 50 km radius), additional contingency operations, increased payload mass, or accommodation of battery degradation.

#### Battery fraction constraint

The minimum battery fraction required for mission feasibility can be derived by rearranging @eq:battery-energy-fraction and @eq:energy-required-total:

$$f_\text{batt,min} = \frac{1.20 \times (E_\text{hover} + E_\text{transition} + E_\text{cruise})}{MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}}$$ {#eq:f-batt-min}

Substituting values:

$$f_\text{batt,min} = \frac{501.6}{10.00 \times 270.0 \times 0.8000 \times 0.9500} = \frac{501.6}{2052} = 0.2445$$ {#eq:f-batt-min-value}

The minimum required battery fraction is 24.4%, below the baseline allocation of 35%. This confirms feasibility and provides design flexibility.

### Mass penalty analysis

The QuadPlane configuration carries mass for both propulsion systems, resulting in a weight penalty compared to a pure fixed-wing aircraft.

#### Propulsion mass estimate

The dual propulsion system mass can be estimated using the propulsion mass fraction $f_\text{prop}$ from @tbl:design-mass-fractions:

$$m_\text{propulsion} = f_\text{prop} \times MTOW = 0.2000 \times 10.00 = 2.000 \text{ kg}$$ {#eq:propulsion-mass-estimate}

For QuadPlane configurations, the propulsion mass is divided between lift and cruise systems. Analysis of commercial reference data (@tbl:reference-vtol) suggests that the lift system accounts for approximately 60-70% of propulsion mass, while the cruise system accounts for approximately 30-40%.

Using a 70:30 split (appropriate for the octocopter lift configuration with 8 motors):

$$m_\text{lift,system} = 0.70 \times 2.000 = 1.400 \text{ kg}$$ {#eq:lift-system-estimate}

$$m_\text{cruise,system} = 0.30 \times 2.000 = 0.600 \text{ kg}$$ {#eq:cruise-system-estimate}

#### Mass penalty calculation

A pure fixed-wing would require only the cruise system. The QuadPlane adds the lift system as additional mass:

$$\Delta m = m_\text{lift,system} \approx 1.4 \text{ kg}$$ {#eq:mass-penalty}

As a fraction of MTOW:

$$f_\text{penalty} = \frac{m_\text{lift,system}}{MTOW} = \frac{1.4}{10.00} = 0.14 = 14\%$$ {#eq:mass-penalty-fraction}

This is consistent with the 15-25% propulsion mass penalty observed in commercial QuadPlane designs. The specific component selection and detailed mass breakdown are presented in @sec:propulsion-selection.

#### Mass penalty trade-off

The dual propulsion mass penalty is acceptable because it enables mission feasibility:

* Without VTOL capability, the mission is impossible, as there is no means of takeoff or landing on Mars without runway infrastructure.
* With VTOL capability, the mission becomes possible with the mass penalty.

The mass penalty is the enabling cost for the Mars UAV mission, which has no alternative for vertical takeoff and landing from a habitat environment.

### Combined constraint analysis

#### Constraints summary

The QuadPlane must satisfy all constraints simultaneously. @tbl:quadplane-constraints summarises the constraint types and their mathematical formulations.

: QuadPlane constraint summary {#tbl:quadplane-constraints}

| Constraint | Formulation | Type |
|:-----------|:------------|:-----|
| Hover power | $(P/W)_\text{hover} \geq f(DL, FM, \rho)$ | Minimum P/W |
| Cruise power | $(P/W)_\text{cruise} \geq f(V, L/D, \eta)$ | Minimum P/W |
| Stall | $W/S \leq f(\rho, V_\text{min}, C_{L,\text{max}})$ | Maximum W/S |
| Energy | $E_\text{available} \geq E_\text{required}$ | Coupling constraint |

The matching chart methodology and constraint diagram analysis are presented in @sec:comparative-results.

### Feasibility assessment

#### Energy budget summary

@tbl:energy-budget-quadplane presents the complete energy breakdown for the QuadPlane configuration.

: QuadPlane energy budget summary {#tbl:energy-budget-quadplane}

| Component | Power (W) | Time (min) | Energy (Wh) | Fraction |
|:----------|----------:|:----------:|------------:|---------:|
| Hover (takeoff + landing) | 3178 | 2.00 | 106.0 | 25% |
| Transition (2 × 30 s) | - | 1.00 | 10.0 | 2.4% |
| Cruise (transit + survey) | 318 | 57.00 | 302.0 | 72% |
| Mission total | - | 60.00 | 418.0 | 100% |
| Reserve (20%) | - | - | 83.6 | - |
| Required total | - | - | 501.6 | - |
| Available | - | - | 718.2 | - |
| Margin | - | - | 216.6 | 43.2% |

![Hybrid VTOL energy budget visualisation showing required energy (hover, transition, cruise, reserve) versus available battery energy. The 43% margin provides adequate safety buffer for mission operations.](figures/energy_budget.png){#fig:energy-budget width=80%}

The analysis shows that despite the high power requirement during hover (3178 W), the short hover duration (2 min) limits hover energy to only 25% of the mission total. The transition phases (2 × 30 s) add a modest 2.4% energy overhead, explicitly accounted for based on literature data scaled from the 25 kg PW Chimera to 10 kg. The majority of energy (72%) is consumed during the extended cruise phase, where the fixed-wing configuration operates at moderate power (318 W).

@tbl:quadplane-feasibility compares the QuadPlane capability against mission requirements:

: QuadPlane feasibility assessment {#tbl:quadplane-feasibility}

| Requirement | Target | QuadPlane capability | Status |
|:------------|:-------|:---------------------|:------:|
| VTOL capability | Required | Yes | PASS |
| Cruise endurance | >60 min | 89.55 min | PASS |
| Operational radius | ≥50 km | 104 km | PASS |
| Hover time | 2 min | Limited by battery | PASS |

Note: Cruise endurance includes 20% energy reserve. Endurance margin is 49.26% above requirement; operational radius margin is 108% above requirement. VTOL capability is provided by the lift rotor system.

The hybrid VTOL (QuadPlane) configuration satisfies all mission requirements with adequate margin.

The key insight is that by limiting hover to approximately 2 minutes (3% of flight time) and accounting explicitly for transition phases (1 minute), the QuadPlane exploits fixed-wing aerodynamics for the remaining 57 minutes. The hover phases (2 min) consume high power (3178 W), while the cruise phase (57 min) operates at wing-borne L/D (approximately 10.5) with moderate power (318 W).

The feasibility assessment for the QuadPlane configuration is summarised in @tbl:quadplane-feasibility. The configuration comparison with rotorcraft and fixed-wing alternatives, design point determination, and selection rationale are presented in @sec:architecture-selection.
