# Reference data and trade-off analysis

## Propulsion characteristics {#sec:propulsion-data}

The reference UAVs predominantly employ a QuadPlane configuration, combining four vertical lift rotors with a separate pusher propeller for cruise. This architecture decouples lift and thrust, allowing optimization of each propulsion system. Lift motor power varies significantly with MTOW, ranging from approximately 500 W (e.g., Sunnysky 4112 on the 8.5 kg X2400) to 6000 W (e.g., T-Motor V13L on the 26.5 kg V13-5). @tbl:reference-propulsion-commercial summarizes propulsion data for commercial benchmarks, including motor masses from manufacturer datasheets.

: Commercial VTOL UAV propulsion specifications {#tbl:reference-propulsion-commercial}

| UAV | Lift motor | Power (W) | Mass (g) | Prop (in) | Cruise motor | Power (W) | Mass (g) | Ref. |
|:----|:-----------|----------:|---------:|----------:|:-------------|----------:|---------:|:----:|
| UAVMODEL X2400 | Sunnysky 4112 485KV | 550 | 153 | 15 | Sunnysky 3525 465KV | 2100 | 259 | [@uavmodelUAVMODELX2400VTOL2024] |
| AirMobi V25 | T-Motor MN505-S KV260 | 2500 | 225 | 16-17 | T-Motor AT4130 KV230 | 2500 | 408 | [@airmobiAirmobiV25Full2024] |
| V13-5 Sentinel | T-Motor V13L KV65 | 6000 | 1680 | N.A. | N.A. | N.A. | N.A. | [@spideruavV135SentinelVTOL2024] |

Mars rotorcraft concepts present distinct propulsion architectures driven by the thin atmosphere. @tbl:reference-propulsion-mars summarizes available data from NASA and academic sources. Motor mass data is generally unavailable for Mars concepts as they use custom or conceptual designs rather than commercial off-the-shelf components.

: Mars UAV propulsion specifications {#tbl:reference-propulsion-mars}

| UAV | Lift motor | Power (W) | Prop (in) | Cruise motor | Power (W) | Ref. |
|:----|:-----------|----------:|----------:|:-------------|----------:|:----:|
| Ingenuity | 2 × 46-pole BLDC (AeroVironment) | approximately 175 each | 48 | N.A. | N.A. | [@balaramMarsHelicopterTechnology2018] |
| Mars Science Helicopter | 6 × Electric (conceptual) | approximately 550 each | 50 | N.A. | N.A. | [@johnsonMarsScienceHelicopter2020] |
| Hybrid VTOL concept | 6 × Electric (conceptual) | approximately 750 each | 20 | Electric | approximately 635 | [@bertaniPreliminaryDesignFixedwing2023] |

Ingenuity uses two custom 46-pole brushless DC outrunner motors designed and built by AeroVironment to drive its coaxial counter-rotating rotors at speeds exceeding 2400 RPM [@balaramMarsHelicopterTechnology2018]. The approximately 350 W total system input power corresponds to approximately 175 W per motor. Six additional Maxon DCX 10S brushed DC motors (7.1 g each) actuate the swashplate mechanism for blade pitch control, contributing negligible power (approximately 1.4 W each) compared to the main propulsion system [@maxongroupMaxonMotorsFly2021].

The Mars Science Helicopter data corresponds to the 31 kg hexacopter configuration, which requires approximately 3300 W hover power distributed across six rotors (approximately 550 W each). This design fits within a 2.5 m diameter aeroshell [@johnsonMarsScienceHelicopter2020]. The hybrid VTOL concept uses six 20-inch lift rotors requiring approximately 4500 W total shaft power for vertical flight (approximately 750 W each), with a separate cruise propulsion system requiring approximately 635 W for forward flight at 92 m/s [@bertaniPreliminaryDesignFixedwing2023].

These specifications contrast with the commercial baselines in terms of specific power. Ingenuity (1.8 kg) operates with a mean system power of approximately 350 W, yielding a specific power of approximately 194 W/kg, reflecting the power-intensive nature of rotorcraft flight in the thin Martian atmosphere [@tzanetosIngenuityMarsHelicopter2022]. The Mars Science Helicopter concept (31 kg) scales this approach to an estimated 3300 W hover power, yielding approximately 106 W/kg due to more efficient larger rotors [@johnsonMarsScienceHelicopter2020]. ARES (175 kg) required a bipropellant rocket system (MMH/MON3) rather than electric propulsion to achieve its 600 km range [@braunDesignARESMars2006]. Recent hybrid VTOL studies for Mars estimate cruise power requirements of approximately 635 W (approximately 32 W/kg), comparable to the specific cruise power of efficient Earth drones because the higher flight speeds on Mars compensate for the lower atmospheric density [@bertaniPreliminaryDesignFixedwing2023].

The data indicates that while cruise power requirements are similar between Mars and Earth platforms, the lift phase in the Martian atmosphere demands high specific power systems.

### Propulsion efficiency parameters {#sec:propulsion-efficiency}

The power required for both hover and cruise flight must account for losses in the propulsion chain. These efficiency parameters directly impact energy consumption and are inputs for constraint analysis.

#### Figure of merit

The figure of merit quantifies rotor efficiency in hover, defined as the ratio of ideal induced power (from momentum theory) to actual power:

$$
FM = \frac{P_\text{ideal}}{P_\text{actual}} = \frac{T^{3/2}/\sqrt{2 \rho A}}{P_\text{actual}}
$$ {#eq:figure-of-merit-def}

For full-scale helicopters at high Reynolds numbers ($Re > 10^6$), $FM$ typically reaches 0.75-0.82 [@leishmanPrinciplesHelicopterAerodynamics2006]. However, figure of merit degrades substantially at low Reynolds numbers due to increased profile drag. Leishman documents that rotating-wing micro air vehicles (MAVs) at very low Reynolds numbers ($Re \sim 10{,}000$-$50{,}000$) achieve $FM$ values of only 0.30-0.50 [@leishmanPrinciplesHelicopterAerodynamics2006]. This degradation results from profile drag coefficients increasing from $C_{d_0} \approx 0.01$ at high $Re$ to $C_{d_0} \approx 0.035$ at low $Re$.

Mars rotors operate at Reynolds numbers of $Re \approx 11{,}000$ for Ingenuity and $Re \approx 15{,}000$-$25{,}000$ for the Mars Science Helicopter concepts [@johnsonMarsScienceHelicopter2020], placing them in the regime where significant $FM$ degradation occurs. Based on the Leishman data for low-Reynolds MAVs, Mars rotor $FM$ is estimated at 0.40, representing the median of the documented 0.30-0.50 range.

#### Propeller efficiency

Cruise propeller efficiency is defined as:

$$
\eta_\text{prop} = \frac{T \times V}{P_\text{shaft}}
$$ {#eq:propeller-efficiency}

Optimized propellers at high Reynolds numbers achieve $\eta_\text{prop} \approx 0.80$-$0.85$ [@sadraeyDesignUnmannedAerial2020]. At the Reynolds numbers expected for Mars cruise ($Re \approx 50{,}000$-$100{,}000$), efficiency degrades due to increased profile drag. Sadraey documents propeller efficiencies of 0.50-0.65 for small UAV propellers operating in this Reynolds regime [@sadraeyDesignUnmannedAerial2020]. Mars cruise propeller efficiency is estimated at 0.55 with a range of 0.45-0.65.

#### Motor and ESC efficiency

Brushless DC motors used in UAV applications typically achieve peak efficiencies of 88-92% [@sadraeyDesignUnmannedAerial2020], with values of 85-87% at cruise power settings (40-60% of maximum power). Electronic speed controllers (ESCs) achieve 93-98% efficiency at moderate to high throttle settings [@sadraeyDesignUnmannedAerial2020]. These efficiencies are relatively unaffected by Mars atmospheric conditions, though thermal management in the thin atmosphere requires consideration.

#### Efficiency summary

@tbl:efficiency-parameters summarizes the efficiency values for the Mars UAV constraint analysis.

: Propulsion efficiency parameters for Mars UAV sizing {#tbl:efficiency-parameters}

| Parameter | Symbol | Value | Range | Source |
|:----------|:------:|------:|------:|:-------|
| Figure of merit | $FM$ | 0.40 | 0.30-0.50 | [@leishmanPrinciplesHelicopterAerodynamics2006] |
| Propeller efficiency | $\eta_\text{prop}$ | 0.55 | 0.45-0.65 | [@sadraeyDesignUnmannedAerial2020] |
| Motor efficiency | $\eta_\text{motor}$ | 0.85 | 0.82-0.90 | [@sadraeyDesignUnmannedAerial2020] |
| ESC efficiency | $\eta_\text{ESC}$ | 0.95 | 0.93-0.98 | [@sadraeyDesignUnmannedAerial2020] |

The combined efficiency from battery to thrust power is:

$$\eta_\text{hover} = FM \times \eta_\text{motor} \times \eta_\text{ESC} = 0.4000 \times 0.8500 \times 0.9500 = 0.3230$$ {#eq:hover-efficiency}

$$\eta_\text{cruise} = \eta_\text{prop} \times \eta_\text{motor} \times \eta_\text{ESC} = 0.5500 \times 0.8500 \times 0.9500 = 0.4436$$ {#eq:cruise-efficiency}

These combined efficiencies indicate that approximately 32% of battery power is converted to useful hover thrust power, and 44% to cruise thrust power. The low figure of merit dominates the hover efficiency chain, while propeller efficiency limits cruise performance.

### Disk loading {#sec:disk-loading}

Disk loading ($DL = T/A$) is the ratio of rotor thrust to total rotor disk area and is a fundamental parameter for rotorcraft sizing. Higher disk loading reduces rotor size but increases power requirements, since induced velocity and hover power scale with the square root of disk loading.

For the coaxial rotor configuration of Ingenuity, the disk loading can be calculated from its specifications. With a mass of 1.8 kg (weight 6.68 N on Mars), rotor radius of 0.60 m (1.2 m diameter), and two rotors:

$$DL_\text{Ingenuity} = \frac{W}{2 \pi R^2} = \frac{6.68}{2 \times \pi \times 0.60^2} = \frac{6.68}{2.26} \approx 3.0 \text{ N/m}^2$$ {#eq:dl-ingenuity}

The Mars Science Helicopter hexacopter concept (31 kg, six rotors with 0.64 m radius) has a higher disk loading [@johnsonMarsScienceHelicopter2020]:

$$DL_\text{MSH} = \frac{W}{6 \pi R^2} = \frac{31 \times 3.711}{6 \times \pi \times 0.64^2} = \frac{115}{7.72} \approx 15 \text{ N/m}^2$$ {#eq:dl-msh}

Commercial multicopters on Earth typically operate at disk loadings of 100-400 N/m² at sea level density. The ratio of required disk loading between Mars and Earth scales with the inverse of density to maintain equivalent induced velocity:

$$\frac{DL_\text{Mars}}{DL_\text{Earth}} = \frac{\rho_\text{Earth}}{\rho_\text{Mars}} = \frac{1.225}{0.0196} \approx 63$$

This scaling factor explains why Mars rotorcraft require much larger rotors (lower disk loading) than Earth equivalents of the same mass.

For the Mars UAV, a disk loading of 30 N/m² is adopted as a design compromise between rotor size and hover power. This value is higher than Ingenuity (2.956 N/m²) and MSH (14.90 N/m²), but lower than theoretical Earth-equivalent scaling would suggest, balancing the conflicting requirements of compact rotor geometry and acceptable hover power in the Martian atmosphere. The implications of this choice for rotor sizing and power requirements are analysed in @sec:constraint-analysis.

### Rotorcraft equivalent lift-to-drag ratio {#sec:rotorcraft-ld}

For rotorcraft in forward flight, an equivalent lift-to-drag ratio $(L/D)_\text{eff}$ characterises the overall propulsive efficiency. This parameter relates power to the product of weight and velocity:

$$P = \frac{W \times V}{(L/D)_\text{eff}}$$ {#eq:rotorcraft-power}

Unlike fixed-wing aircraft where $L/D$ is a purely aerodynamic parameter, the rotorcraft equivalent $L/D$ includes rotor propulsive efficiency and induced losses in forward flight. @tbl:rotorcraft-ld summarises typical values for different rotorcraft configurations.

: Equivalent lift-to-drag ratio for rotorcraft configurations [@proutyHelicopterPerformanceStability2002; @leishmanPrinciplesHelicopterAerodynamics2006] {#tbl:rotorcraft-ld}

| Configuration | $(L/D)_\text{eff}$ | Notes |
|:--------------|:------------------:|:------|
| Conventional helicopter | 4-6 | Hub drag, rotor inefficiency |
| Optimised compound | 6-8 | Wing offloads rotor at speed |
| Pure multirotor | 3-5 | No translational lift benefit |

A value of $(L/D)_\text{eff}$ = 4.000 is adopted for the Mars UAV rotorcraft analysis, representing a conservative estimate that accounts for the low Reynolds number regime and limited rotor optimisation at small scale. This value is used only for comparison of the pure rotorcraft configuration; the hybrid VTOL analysis uses fixed-wing $L/D$ values for cruise.
