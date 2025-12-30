# Reference data and trade-off analysis

## Derived requirements {#sec:derived-requirements}

This section translates the qualitative user needs identified in @sec:user-needs into quantitative, verifiable requirements. Each requirement is derived from stakeholder needs through analysis of the operational environment, reference platform performance, and physical constraints. The requirements documented here provide the numerical inputs for constraint analysis (@sec:constraint-analysis).

### Operational requirements {#sec:operational-requirements}

The operational requirements define the mission performance envelope derived from user needs N1 (extended range), N2 (aerial imaging), N5 (extended endurance), and N4 (VTOL capability).

#### Operational radius

The UAV shall achieve an operational radius of at least 50 km. This requirement derives from user need N1 (extended range beyond surface rover capability). The Curiosity rover has traversed approximately 35 km total over more than a decade on the Martian surface [@nasaMarsScienceLaboratory2025]. A 50 km radius enables single-flight survey of areas inaccessible to rovers within practical mission timelines, providing a substantial capability improvement that justifies the UAV development. Verification is demonstrated through endurance flight test covering 100 km round-trip distance.

#### Operational altitude

The UAV shall operate at altitudes between 30 m and 350 m above ground level. The minimum altitude of 30 m derives from terrain clearance needs: rock size-frequency distributions at Mars landing sites indicate that hazardous rocks are typically 0.5 m high or approximately 1 m in diameter [@golombekRockSizeFrequencyDistributions2021], and 30 m provides a safety factor of 60× over the largest common surface obstacles. The maximum altitude of 350 m derives from imaging resolution requirements (user need N2). Geological mapping typically requires ground sample distance (GSD) of 5-10 cm per pixel. For a camera with 2.4 μm pixel pitch and 8.8 mm focal length (typical 1-inch sensor such as the DJI Air 2S [@djiDJIAir2S2021]), the GSD is calculated as:

$$GSD = \frac{H \cdot p}{f}$$ {#eq:gsd}

where $H$ is flight altitude, $p$ is pixel pitch, and $f$ is focal length. Achieving 10 cm GSD requires:

$$H_\text{max} = \frac{GSD \cdot f}{p} = \frac{0.10 \times 8.8 \times 10^{-3}}{2.4 \times 10^{-6}} = 367 \text{ m}$$ {#eq:hmax}

Rounding down to 350 m ensures the 10 cm GSD requirement is met with margin. Verification is demonstrated through flight test with altitude hold and imaging validation.

#### Flight endurance

The UAV shall achieve a total flight time of at least 60 minutes, including hover and cruise phases. This requirement derives from user need N5 (extended endurance) in combination with the operational radius requirement. The mission profile (@sec:mission-parameters) requires 42 minutes transit time (100 km round-trip at 40 m/s), 15 minutes survey operations, and 3 minutes hover phases (takeoff, landing, contingency), totaling 60 minutes. This endurance substantially exceeds the Ingenuity helicopter, which achieved individual flights of up to 169 seconds and cumulative flight time of approximately 129 minutes over 72 flights [@nasaIngenuityMarsHelicopter2024; @tzanetosIngenuityMarsHelicopter2022]. Verification is demonstrated through full mission profile flight test.

### Environmental requirements {#sec:environmental-requirements}

The environmental requirements define the conditions under which the UAV must operate, derived from user needs N7 (wind tolerance), N8 (dust protection), N10 (radiation tolerance), and N11 (thermal compatibility).

#### Wind tolerance

The UAV shall operate safely in sustained winds up to 10 m/s. Wind measurements by the Mars 2020 Perseverance rover at Jezero crater found mean wind speeds of 3.2 ± 2.3 m/s, with afternoon peaks reaching 6.1 ± 2.2 m/s; 99% of measured winds remained below 10 m/s [@viudez-moreirasWindsMars20202022]. The 10 m/s limit accommodates typical Martian conditions with margin. Although dust storm winds can reach 27 m/s [@nasaFactFictionMartian2015], flight operations during such events are deferred rather than designed for. Verification includes wind tunnel testing of control authority and flight simulation with 10 m/s gust profiles.

#### Dust protection

All critical components shall be protected to IP6X standard. Dust protection follows the IP Code defined by IEC 60529 [@internationalelectrotechnicalcommissionDegreesProtectionProvided2013]. IP6X denotes dust-tight enclosures with complete exclusion of particulate matter, necessary given the fine Martian regolith (particle sizes 1-100 μm) that can degrade mechanical bearings and optical surfaces. Verification is through dust ingress testing per IEC 60529 procedures or equivalent.

#### Radiation tolerance

Electronics shall tolerate a total ionizing dose of at least 1 krad(Si). The Mars Science Laboratory RAD instrument measured an average absorbed dose rate of approximately 76 mGy/year (7.6 rad/year, or 0.0076 krad/year) on the Martian surface [@hasslerMarsSurfaceRadiation2014]. Over a two-year mission, the accumulated dose is approximately 0.015 krad. A radiation tolerance requirement of 1 krad(Si) total ionizing dose provides approximately 67× margin and is achievable with commercial off-the-shelf (COTS) electronics, which typically tolerate 5-20 krad without requiring expensive radiation-hardened components [@brunettiCOTSDevicesSpace2024]. Verification is through component-level radiation test data or heritage qualification.

#### Operating temperature range

The UAV shall operate in ambient temperatures from −80 °C to +20 °C. Mars diurnal temperature swings range from approximately −80 °C (night) to +20 °C (midday) depending on season and location. Critical subsystems (particularly batteries and cameras) require thermal management to function within their operational ranges. The requirement applies to the ambient environment; internal subsystem temperatures are managed through insulation and active heating. Verification is through thermal vacuum testing across the temperature range.


### Load factor selection {#sec:load-factor-selection}

The structural weight estimation equations in @sec:mass-breakdown include the ultimate load factor ($n_\text{ult}$) as a key parameter. This subsection documents the load factor selection and its justification.

#### Definitions

The *limit load factor* ($n_\text{limit}$) is the maximum load factor expected in normal operation without permanent deformation. The *ultimate load factor* ($n_\text{ult}$) is the limit load factor multiplied by a factor of safety [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017]:

$$n_\text{ult} = n_\text{limit} \times SF$$ {#eq:n-ult-definition}

where $SF = 1.5$ is the standard aerospace factor of safety [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017, CS 23.2230(a)(2)]. This 1.5 factor accounts for material property variations, manufacturing tolerances, fatigue and damage tolerances, uncertainty in load prediction.
The structure must support limit loads without permanent deformation, and ultimate loads without failure.

#### Load factor selection rationale

For the Mars UAV, a limit load factor of $n_\text{limit} = 2.5$ is adopted, yielding:

$$n_\text{ult} = 2.5 \times 1.5 = 3.75$$

This value represents the lower bound of CS-23 normal category requirements and is justified by four considerations.

First, unmanned operation fundamentally changes the structural design philosophy. Structural failure of a crewed aircraft risks human lives, motivating conservative safety margins. For an unmanned autonomous vehicle, failure consequences are limited to mission loss and equipment damage. Lower structural safety margins are therefore acceptable and industry-standard for unmanned systems.

Second, autonomous flight with limited manoeuvring envelope provides inherent load protection. The flight control system enforces strict manoeuvre limits through software. Unlike piloted aircraft, where rapid or panic manoeuvres can generate unexpected loads, the autopilot restricts bank angle (typically 45-60°) and commanded load factor (typically 2-3 g). This bounded envelope ensures that the design limit load is not exceeded in normal operation.

Third, gust loads are substantially reduced in the Mars atmosphere. Gust-induced load factors scale with atmospheric density. The gust load factor increment can be expressed as:

$$\Delta n_\text{gust} \propto \frac{\rho \cdot U_\text{de} \cdot V \cdot a}{W/S}$$

where $\rho$ is atmospheric density, $U_\text{de}$ is design gust velocity, $V$ is flight speed, and $a$ is lift curve slope. At Mars surface density (approximately 0.020 kg/m³), gust loads are approximately 60 times lower than at Earth sea level for equivalent gust velocities. Even with the higher design gust velocities on Mars (up to 10 m/s, per @sec:user-needs), the gust load contribution remains negligible compared to manoeuvring loads. The manoeuvring load factor therefore dominates the structural design.

Fourth, precedents from Mars rotorcraft support reduced load factors. The NASA Mars Science Helicopter study [@johnsonMarsScienceHelicopter2020] noted that "aerodynamic loads on the blade are small because of the low atmospheric density on Mars," enabling innovative lightweight structural designs. While specific load factors are not published for Ingenuity or MSH, the thin atmosphere fundamentally reduces aerodynamic loading relative to Earth-based designs.

#### Comparison with other aircraft categories

@tbl:load-factor-comparison presents the Mars UAV load factors in context with other aircraft categories.

: Load factor comparison for various aircraft categories {#tbl:load-factor-comparison}

| Aircraft category | $n_\text{limit}$ | SF | $n_\text{ult}$ | Source |
|:---|:---:|:---:|:---:|:---|
| CS-25 transport (high W) | 2.5 | 1.5 | 3.75 | FAR Part 25 |
| CS-25 transport (low W) | 3.8 | 1.5 | 5.7 | FAR Part 25 |
| CS-23 normal (heavy) | 2.5 | 1.5 | 3.75 | CS-23 Amdt 4 §23.337 |
| CS-23 normal (light) | 3.8 | 1.5 | 5.7 | CS-23 Amdt 4 §23.337 |
| CS-23 utility | 4.4 | 1.5 | 6.6 | CS-23 Amdt 4 |
| CS-23 aerobatic | 6.0 | 1.5 | 9.0 | CS-23 Amdt 4 |
| Mars UAV (this study) | 2.5 | 1.5 | 3.75 | This work |

The selected $n_\text{ult} = 3.75$ corresponds to the lower bound of certified normal category aircraft and the value used for heavy transport aircraft. This selection balances structural weight reduction against acceptable safety margins for an unmanned research platform.

Regarding regulatory status, EASA CS-23 and FAA Part 23 are Earth certification standards for manned aircraft. The Mars UAV is not subject to these regulations. CS-23 is used here as a methodology reference to establish consistent, industry-standard load factors, not as a regulatory requirement.

The structural weight impact of the reduced ultimate load factor is quantified in @sec:mass-breakdown, where the weight estimation equations are applied to the sized geometry. The reduced load factor enables approximately 23% wing weight reduction and 10% fuselage weight reduction compared to light aircraft designed to CS-25 standards ($n_\text{ult} = 5.7$).


### Geometry parameter bounds {#sec:geometry-bounds}

This section defines the wing planform geometry parameters used in the constraint analysis and weight estimation. Each parameter involves trade-offs that determine the optimal design space for the Mars UAV.

#### Aspect ratio

The aspect ratio is bounded as:

$$AR \in [5, 7]$$ {#eq:ar-bounds}

Induced drag scales inversely with aspect ratio:

$$C_{D,i} = \frac{C_L^2}{\pi \cdot AR \cdot e}$$ {#eq:induced-drag}

Higher aspect ratio reduces induced drag, while wing weight increases approximately as $AR^{0.6}$ [@sadraeyAircraftDesignSystems2013]. For fixed wing area, higher aspect ratio also reduces mean chord:

$$\bar{c} = \sqrt{\frac{S}{AR}}$$ {#eq:chord-from-ar}

This chord reduction affects Reynolds number, which is constrained by airfoil performance requirements.

The selected range is based on both Earth UAV data and Mars-specific studies. Typical aspect ratios for small UAVs range from 4 to 12 [@sadraeyAircraftDesignSystems2013]. Mars UAV designs in the literature consistently select aspect ratios in the 5 to 6 range. The ARES Mars airplane design used $AR$ = 5.6 [@braunDesignARESMars2006]. Barbato et al. found optimal $AR$ = 5.3 to 6.3 for a 24 kg solar-powered Mars UAV [@barbatoPreliminaryDesignFixedWing2024], demonstrating that optimal aspect ratio increases with lift coefficient and decreases with payload mass.

A baseline aspect ratio of $AR$ = 6 is adopted, representing a compromise between induced drag reduction (favouring higher AR) and structural weight (favouring lower AR). At the target MTOW of 10 kg, this aspect ratio provides adequate lift-to-drag ratio while maintaining reasonable wing chord for Reynolds number requirements and structural depth for load-bearing capacity.


#### Thickness ratio

The wing thickness ratio is bounded by structural and aerodynamic considerations:

$$t/c \in [0.06, 0.11]$$ {#eq:tc-bounds}

This range reflects the thickness characteristics of candidate low-Reynolds airfoils from the UIUC database [@seligSummaryLowSpeedAirfoil1995; @williamsonSummaryLowSpeedAirfoil2012]. The candidate airfoils span thickness ratios from 6.2% (AG12, thin AG-series) through 10.5% (S7055, balanced design). The E387 general-purpose airfoil has $t/c$ = 9.1%, the SD8000 low-drag airfoil has $t/c$ = 8.9%, and the SD7037 general-purpose airfoil has $t/c$ = 9.2%.

Wing structural weight scales approximately as $(t/c)^{-0.3}$ [@sadraeyAircraftDesignSystems2013], favouring thicker airfoils for structural efficiency. A baseline thickness ratio of $t/c$ = 0.09 is adopted for sizing, providing adequate structural depth while remaining compatible with the candidate airfoils. The specific airfoil selection is deferred to @sec:airfoil-selection where aerodynamic performance at the design Reynolds number is evaluated.

#### Taper ratio

The taper ratio is constrained to:

$$\lambda \in [0.4, 0.6]$$ {#eq:taper-bounds}

where $\lambda = c_\text{tip} / c_\text{root}$.

For minimum induced drag, the ideal spanwise lift distribution is elliptical, and for an unswept wing, a taper ratio of approximately $\lambda$ = 0.4 closely approximates this loading distribution [@sadraeyAircraftDesignSystems2013]. Tapered wings also concentrate structural material near the root where bending moments are highest, improving structural efficiency, though lower taper ratios increase tip stall susceptibility. Rectangular wings ($\lambda$ = 1.0) offer the simplest manufacturing; the upper bound of $\lambda$ = 0.6 represents a compromise toward manufacturing simplicity while maintaining near-elliptical loading.

A nominal value of $\lambda$ = 0.5 is adopted for baseline sizing, providing approximately 98% of the theoretical minimum induced drag while offering good stall characteristics and reasonable manufacturing complexity.

#### Sweep angle

The quarter-chord sweep angle is fixed at:

$$\Lambda = 0°$$ {#eq:sweep-selection}

Wing sweep is primarily used to delay compressibility effects at transonic speeds, typically above $M$ = 0.7 [@sadraeyAircraftDesignSystems2013]. The mechanism is that sweep reduces the component of velocity perpendicular to the wing leading edge, effectively reducing the local Mach number.

At the Mars UAV cruise Mach number of approximately $M$ = 0.17, compressibility effects are entirely negligible. Sweep provides no aerodynamic benefit at this speed and introduces penalties including increased structural complexity from bending-torsion coupling, weight penalty from heavier swept-wing structures, reduced lift curve slope requiring higher angles of attack, and degraded stall characteristics as swept wings tend to stall at the tip first, compromising roll control.

An unswept configuration is adopted for the Mars UAV.

#### Geometry parameter summary

@tbl:geometry-summary consolidates the geometry parameters for constraint analysis.

: Wing geometry parameter summary {#tbl:geometry-summary}

| Parameter | Symbol | Range | Baseline | Rationale |
|:----------|:------:|:-----:|:--------:|:----------|
| Aspect ratio | $AR$ | 5-7 | 6 | Mars UAV precedents, L/D vs. structure |
| Thickness ratio | $t/c$ | 0.06-0.11 | 0.09 | Structural depth vs. drag |
| Taper ratio | $\lambda$ | 0.4-0.6 | 0.5 | Near-elliptical loading |
| Sweep angle | $\Lambda$ | N.A. | 0° | Low Mach, no benefit |

### Mission velocity and time parameters {#sec:mission-parameters}

This section derives and justifies the velocity and time parameters required for constraint analysis. Each parameter is traceable to mission requirements (@sec:user-needs) and consistent with atmospheric conditions (@sec:operational-environment).

#### Cruise velocity

Cruise velocity selection must balance multiple constraints: Mach number, Reynolds number, power consumption, and mission time requirements.

Staying well below $M \approx 0.3$ keeps compressibility corrections small, as density changes scale roughly with $M^2$ in subsonic flow. A design Mach band of $M_\infty \approx 0.16$-$0.28$ is targeted, with an initial selection around $M \approx 0.17$. Using the Mars speed of sound at operating altitude ($a$ = 230.8 m/s from @tbl:atmosphere), this corresponds to:

$$V_\text{cruise} = M \times a = 0.17 \times 230.8 \approx 40 \text{ m/s}$$ {#eq:cruise-velocity-value}

This velocity is approximately twice that of typical Earth hybrid VTOL UAVs but represents a necessary compromise: lower velocities would require excessively large wing chords to achieve acceptable Reynolds numbers, while higher velocities would increase power consumption significantly. Cruise power scales strongly with velocity once parasite drag dominates ($P \sim D \times V$, with parasite drag $\sim V^2$, leading to $P \sim V^3$).

The Reynolds number at cruise is:

$$Re = \frac{\rho \cdot V \cdot c}{\mu}$$ {#eq:reynolds-definition}

Using the atmospheric properties at operating altitude from @tbl:atmosphere ($\rho$ = 0.0196 kg/m³, $\mu$ = 1.08 × 10⁻⁵ Pa·s), with $V$ = 40 m/s and targeting $Re$ = 60,000:

$$c = \frac{Re \cdot \mu}{\rho \cdot V} = \frac{60{,}000 \times 1.08 \times 10^{-5}}{0.0196 \times 40} = 0.83 \text{ m}$$

The wing area is related to chord through aspect ratio. For $AR$ = 6 and mean chord $\bar{c}$ = 0.83 m:

$$S = \bar{c}^2 \times AR = 0.83^2 \times 6 = 4.1 \text{ m}^2$$

@tbl:chord-velocity presents the relationship between cruise velocity, chord, and wing area for achieving $Re$ = 60,000 at $AR$ = 6.

: Chord and wing area requirements for Re = 60,000 {#tbl:chord-velocity}

| $V_\text{cruise}$ (m/s) | Required $\bar{c}$ (m) | Required $S$ (m²) at AR = 6 |
|:------------------------|:----------------------:|:------------------------:|
| 35 | 0.95 | 5.4 |
| 38 | 0.87 | 4.5 |
| 40 | 0.83 | 4.1 |

These wing areas are larger than typical for small terrestrial UAVs but reflect the low atmospheric density on Mars. For the target MTOW of 10 kg (Mars weight $W$ = 37.1 N), a wing area of 4.1 m² yields a wing loading of approximately 9 N/m².

A cruise velocity of $V_\text{cruise}$ = 40 m/s is adopted, with a sensitivity range of 35-45 m/s for constraint analysis parametric studies. The 50 km operational radius requires a round-trip distance of 100 km, yielding a transit time of 2500 s (approximately 42 min) at 40 m/s.

#### Minimum velocity

The minimum operating velocity provides a safety margin above the stall speed. Per general aerospace practice, the approach and minimum operating speeds for aircraft are typically 1.2 times the stall speed [@sadraeyAircraftDesignSystems2013]:

$$V_\text{min} \geq 1.2 \times V_\text{stall}$$ {#eq:v-min-constraint}

The stall speed depends on wing loading:

$$V_\text{stall} = \sqrt{\frac{2 \cdot (W/S)}{\rho \cdot C_{L,\text{max}}}}$$ {#eq:stall-speed-prelim}

The 1.2 factor ensures adequate margin for gust upset recovery, control authority at low speed, and transition manoeuvres between cruise and hover modes.

#### Wing loading constraint

Rearranging @eq:stall-speed-prelim for wing loading:

$$\frac{W}{S} = \frac{1}{2} \rho V_\text{stall}^2 C_{L,\text{max}}$$ {#eq:wing-loading-stall}

For a minimum operating speed $V_\text{min}$ with safety margin above stall:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:wing-loading-constraint}

This equation defines the stall constraint on the matching chart. On a chart with P/W on the vertical axis and W/S on the horizontal axis, the stall constraint appears as a vertical line (constant maximum W/S) independent of power loading.

For the preliminary design, using the wing loading derived from cruise velocity analysis ($W/S \approx 9.000$ N/m² from @tbl:chord-velocity), $\rho$ = 0.01960 kg/m³, and $C_{L,\text{max}}$ = 1.200:

$$V_\text{stall} = \sqrt{\frac{2 \times 9.000}{0.01960 \times 1.200}} = \sqrt{765.3} = 27.67 \text{ m/s}$$

$$V_\text{min} \geq 1.200 \times 27.67 = 33.20 \text{ m/s}$$

The cruise velocity of 40.00 m/s provides a comfortable margin above the minimum velocity, indicating that the aircraft will operate at moderate lift coefficients during cruise rather than near stall. This margin allows for manoeuvring and provides safety against gusty conditions.

#### Hover and transition time allocation

For the hybrid VTOL configuration, hover time is limited to vertical takeoff, landing, and contingency operations. Transition phases are accounted separately due to their distinct energy characteristics. The time allocation is summarised in @tbl:hover-allocation.

: Hover and transition time allocation for energy budget {#tbl:hover-allocation}

| Flight phase | Duration (s) | Category | Description |
|:-------------|-------------:|:---------|:------------|
| Takeoff climb | 30 | Hover | Vertical climb to 30 m safe altitude |
| Takeoff hover | 30 | Hover | Station keeping before transition |
| Transition Q2P | 30 | Transition | Quad-to-plane mode change |
| Transition P2Q | 30 | Transition | Plane-to-quad mode change |
| Landing hover | 30 | Hover | Station keeping after transition |
| Landing descent | 30 | Hover | Controlled descent and touchdown |
| **Total hover** | **120** | N.A. | 2 min pure hover |
| **Total transition** | **60** | N.A. | 1 min (2 × 30 s) |

The hover time of 120 s (2 min) and transition time of 60 s (1 min) are used for energy calculations. These durations are engineering estimates based on Earth-based QuadPlane operations scaled for Mars conditions. Reference data from @goetzendorf-grabowskiOptimizationEnergyConsumption2022 indicates total VTOL time of approximately 2 minutes for a 10 kg quad-plane, with vertical takeoff requiring approximately 20 seconds and landing 10-15 seconds. The remaining time accommodates station-keeping hover and transitions. The 30-second transition duration per phase is a conservative estimate; actual transition times depend on the specific transition corridor and control strategy employed [@mathurMultiModeFlightSimulation2025]. For Mars, the allocation accounts for slower climb rates in the thin atmosphere (estimated 1 to 2 m/s for a 10 kg vehicle), extended transition phases due to reduced control authority from lower air density, and contingency for unexpected wind gusts or abort scenarios. For comparison, the Ingenuity helicopter achieved total flight times of 90-170 seconds for pure rotorcraft operations [@nasaIngenuityMarsHelicopter2024], though direct comparison is limited as Ingenuity operates entirely in hover/forward-flight rotorcraft mode rather than transitioning to fixed-wing cruise.

#### Cruise endurance

The cruise endurance requirement is derived from the 50 km operational radius:

$$t_\text{cruise} = t_\text{outbound} + t_\text{survey} + t_\text{return}$$ {#eq:cruise-time}

The components are: outbound transit (50,000 m / 40 m/s = 1250 s = 20.8 min), return transit (20.8 min), and survey/loiter at target (15 min for mapping operations). The total cruise time is:

$$t_\text{cruise} = 20.8 + 20.8 + 15 \approx 57 \text{ min}$$ {#eq:cruise-endurance}

#### Energy reserve

A 20% energy reserve is maintained in addition to the mission profile energy. This reserve accounts for navigation inefficiencies and course corrections, increased power due to atmospheric density variations, extended hover for precision landing, and emergency return capability. The reserve is applied to the total energy budget, not individual flight phases.

#### Mission profile summary

@tbl:mission-profile presents the nominal mission timeline.

: Nominal mission profile {#tbl:mission-profile}

| Phase | Duration | Cumulative | Power mode |
|:------|:--------:|:----------:|:-----------|
| Takeoff hover | 1 min | 1 min | Hover |
| Outbound cruise | 21 min | 22 min | Cruise |
| Survey operations | 15 min | 37 min | Cruise |
| Return cruise | 21 min | 58 min | Cruise |
| Landing hover | 1 min | 59 min | Hover |
| Contingency | 1 min | 60 min | Hover |
| Total flight | 60 min | N.A. | N.A. |

The 60-minute flight time plus 20% energy reserve yields a design endurance requirement of approximately 72 minutes equivalent energy capacity.

### Summary of derived requirements {#sec:requirements-summary}

@tbl:derived-requirements consolidates all numerical inputs required for the constraint analysis, organised by functional category as defined in the sizing methodology. Each parameter is traced to its source: user need (N1-N11), physical analysis, reference data, or design standard.

: Constraint analysis input parameters {#tbl:derived-requirements}

| ID | Parameter | Symbol | Value | Derived from |
|:---|:----------|:------:|:------|:-------------|
| Mission parameters | | | | |
| M1 | Payload mass | $m_\text{payload}$ | 1.0 kg | N2, N3 |
| M2 | Cruise velocity | $V_\text{cruise}$ | 40 m/s | Mach, Re constraints |
| M3 | Minimum velocity | $V_\text{min}$ | 1.2 × $V_\text{stall}$ | Safety margin |
| M4 | Cruise time | $t_\text{cruise}$ | 57 min | N1, N5 |
| M5 | Hover time | $t_\text{hover}$ | 2 min | N4 |
| M5b | Transition time | $t_\text{transition}$ | 1 min | N4 |
| M6 | Energy reserve | N.A. | 20% | Safety margin |
| Geometry parameters | | | | |
| G1 | Aspect ratio | $AR$ | 6 | Mars precedents |
| G2 | Thickness ratio | $t/c$ | 0.09 | Structural/aero trade |
| G3 | Taper ratio | $\lambda$ | 0.5 | Elliptical loading |
| G4 | Sweep angle | $\Lambda$ | 0° | Low Mach |
| Aerodynamic coefficients | | | | |
| A1 | Max lift coefficient | $C_{L,\text{max}}$ | 1.20 | UIUC wind tunnel |
| A2 | Oswald efficiency | $e$ | 0.87 | AR=6 correlation |
| A3 | Zero-lift drag | $C_{D,0}$ | 0.030 | Component buildup |
| Propulsion efficiencies | | | | |
| P1 | Figure of merit | FM | 0.40 | Low-Re rotor data |
| P2 | Propeller efficiency | $\eta_\text{prop}$ | 0.55 | Low-Re analysis |
| P3 | Motor efficiency | $\eta_\text{motor}$ | 0.85 | BLDC typical |
| P4 | ESC efficiency | $\eta_\text{ESC}$ | 0.95 | Industry typical |
| Energy parameters | | | | |
| E1 | Battery specific energy | $e_\text{spec}$ | 270 Wh/kg | Solid-state Li-ion |
| E2 | Depth of discharge | DoD | 0.80 | Cycle life |
| E3 | Discharge efficiency | $\eta_\text{batt}$ | 0.95 | Moderate C-rate |
| Rotor parameters | | | | |
| R1 | Disk loading | DL | 30 N/m² | Trade-off analysis |
| R2 | Rotorcraft $(L/D)_\text{eff}$ | $(L/D)_\text{eff}$ | 4.0 | Helicopter typical |
| Structural parameters | | | | |
| S1 | Limit load factor | $n_\text{limit}$ | 2.5 | N6, CS-23 |
| S2 | Safety factor | SF | 1.5 | CS-23 standard |
| S3 | Ultimate load factor | $n_\text{ult}$ | 3.75 | S1 × S2 |



The operational and environmental requirements from @sec:operational-requirements and @sec:environmental-requirements define the mission performance envelope but are not direct inputs to the constraint analysis. The operational radius requirement (OR-1, ≥ 50 km) determines cruise velocity (M2) and cruise time (M4). The flight endurance requirement (OR-4, ≥ 60 min) constrains the sum of cruise time and hover time (M4, M5). The wind tolerance requirement (ER-1, ≥ 10 m/s) motivates the energy reserve margin (M6) to accommodate headwind conditions.
