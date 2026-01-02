# Reference data and trade-off analysis

## Architecture comparison {#sec:architecture-comparison}

### Flight architecture

Three architectures are considered for Mars atmospheric flight: rotorcraft, fixed-wing, and hybrid VTOL. Each presents distinct trade-offs between operational flexibility and energy efficiency.

#### Rotorcraft

Pure rotorcraft designs provide vertical take-off and landing without requiring prepared surfaces. NASA's Ingenuity helicopter demonstrated this approach, completing 72 flights on Mars [@tzanetosIngenuityMarsHelicopter2022]<!-- #abs --> [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights -->. However, rotorcraft suffer from poor cruise efficiency. Hover power scales according to momentum theory as [@johnsonMarsScienceHelicopter2020]<!-- #eq:hover -->:

$$P_{hover} = \frac{T^{1.5}}{\sqrt{2\rho A_{rotor}}} \cdot \frac{1}{FM}$$ {#eq:hover-power-arch}

where T is thrust, ρ is atmospheric density, $A_\text{rotor}$ is rotor disk area, and FM is the figure of merit (typically 0.6-0.7 for small rotors [@johnsonMarsScienceHelicopter2020]<!-- #eq:hover -->). The inverse square root dependence on density means that hover power increases by a factor of approximately 7 when moving from Earth sea level (ρ = 1.225 kg/m³) to Mars surface (ρ ≈ 0.020 kg/m³) [@nasaMarsAtmosphereModel2021]<!-- #s:density -->.

For the mission profile considered here, requiring > 50 km operational radius, rotorcraft endurance would be severely limited. Ingenuity's 72 flights totaled only 128.8 minutes of flight time, with typical flights lasting 1-3 minutes [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights -->. Even with larger battery capacity, pure rotorcraft endurance on Mars would likely remain below 15 minutes, insufficient for meaningful survey operations at the required range.

#### Fixed-wing

Conventional fixed-wing aircraft achieve the highest aerodynamic efficiency, with lift-to-drag ratios of 10-20 compared to effective L/D of 3-5 for rotorcraft in forward flight [@proutyHelicopterPerformanceStability2002]<!-- #ch3:ld -->. Cruise power is:

$$P_{cruise} = \frac{W \cdot V}{L/D \cdot \eta}$$ {#eq:cruise-power-arch}

where W is weight, V is cruise speed, and η is propulsive efficiency. The dependence on L/D rather than disk loading makes fixed-wing flight far more energy-efficient for covering distance.

However, fixed-wing aircraft require either runways or launch/recovery systems. Given the absence of prepared surfaces on Mars and the risk of landing damage on unprepared terrain, pure fixed-wing designs are unsuitable for habitat-based operations.

#### Hybrid VTOL (QuadPlane)

Hybrid designs combine dedicated lift rotors for VTOL with a fixed wing for cruise flight. During take-off and landing, lift rotors provide thrust; during cruise, the wing generates lift while cruise propellers provide forward thrust and the lift rotors are stopped or windmilling.

For Mars operations where in-flight repair is impossible, single-fault tolerance is essential. This is achieved through coaxial configurations for both propulsion systems:

* Lift system: Eight motors in four coaxial pairs (octocopter configuration), where each coaxial pair has counter-rotating rotors sharing a structural mount. This allows controlled landing with any single motor failed.
* Cruise system: Two coaxial contra-rotating tractor propellers at the bow, driven by independent motors. Each motor is sized to provide 60% of nominal cruise thrust, allowing mission continuation with reduced performance if either motor fails.

This architecture achieves near-fixed-wing cruise efficiency while retaining VTOL capability. The mass penalty for the dual propulsion system (10 motors total: 8 lift plus 2 cruise) is typically 20-25% of MTOW based on the commercial references in @tbl:reference-vtol and accounting for the redundant cruise motors. This penalty is acceptable given the operational flexibility and fault tolerance gained.

The QuadPlane architecture is widely adopted in the commercial drone industry, with mature flight control systems and proven reliability. All nine reference UAVs in @tbl:reference-vtol employ this configuration.

### Fuselage geometry trade-offs

Fuselage geometry affects drag, stability, and payload integration. The length-to-wingspan ratio ($l/b$) observed in commercial VTOL UAVs ranges from 0.28 to 0.63 (@tbl:reference-fuselage), reflecting different design priorities: parasitic drag, longitudinal stability, payload volume.

The fuselage and miscellaneous components (landing gear, sensor turrets, antennas) contribute substantially to UAV parasitic drag. Analysis of ten fixed-wing surveillance UAVs found that these components account for nearly half of total parasitic drag, leading to equivalent skin friction coefficients significantly higher than for manned aircraft [@gottenFullConfigurationDrag2021]<!-- #s:drag -->.
Longer fuselages (higher $l/b$) provide greater tail moment arm, improving longitudinal stability with smaller tail surfaces. However, this comes at the cost of increased fuselage wetted area and structural mass.
Longer fuselages also provide more internal volume for payload, batteries, and avionics. Flying-wing configurations (very low $l/b$) sacrifice internal volume for reduced parasitic drag.

### Tail configuration trade-offs

The tail configuration affects stability, control authority, drag, and structural complexity. For QuadPlane designs, the presence of lift rotor support booms creates the option to mount tail surfaces on these booms rather than on the fuselage.

#### Fuselage-mounted configurations

Fuselage-mounted tail configurations represent the conventional approach for aircraft design, with tail surfaces attached directly to the aft fuselage. These configurations benefit from simpler structural integration and established design practices, though they may experience aerodynamic interference from the fuselage and wing wake. Three fuselage-mounted configurations are considered.

The conventional tail combines horizontal and vertical stabilizers, providing proven stability and control with relatively simple control linkages. The horizontal and vertical surfaces create interference drag at their intersection, and the tail may be positioned in the wing wake.

The V-tail combines pitch and yaw control in two upward-angled surfaces. It reduces interference drag and lightens structure by eliminating the intersection between horizontal and vertical surfaces, but requires control mixing (ruddervators). The reduced wetted area provides drag reduction compared to conventional configurations [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:comparison -->.

The Y-tail is an inverted V-tail configuration with an additional central vertical fin. The inverted V surfaces provide pitch control and partial yaw authority, while the central fin enhances directional stability and yaw control.

#### Boom-mounted configurations

QuadPlane designs inherently include structural booms for the lift rotors. Extending these booms to support the tail surfaces offers advantages in structural efficiency, moment arm, and wake avoidance. The boom structure required for lift rotors can simultaneously carry tail loads, reducing overall structural mass compared to separate boom and fuselage-mounted arrangements. Boom-mounted tails can achieve greater moment arms than fuselage-mounted configurations, potentially allowing smaller tail surfaces for equivalent stability, and can be positioned outside the wing and fuselage wake, improving tail effectiveness. At Mars Reynolds numbers (Re of approximately 50,000 for tail surfaces), control surface effectiveness is reduced compared to Earth conditions; boom-mounted configurations may provide the increased moment arm necessary to achieve adequate control authority without excessively large tail surfaces. Two specific configurations are considered.

The boom-mounted inverted V consists of two tail surfaces angled upward from the boom endpoints, forming an inverted V when viewed from behind. This configuration provides combined pitch and yaw control while maintaining ground clearance. The booms position the surfaces away from the fuselage wake.

The boom-mounted inverted U features a horizontal stabilizer connecting the two boom endpoints, with vertical stabilizers extending upward from each boom. CFD analysis found this configuration provided the highest critical angle (18° vs 15° for other configurations), good longitudinal stability, and favorable maneuverability for surveillance missions [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:comparison -->. The inverted U boom configuration achieved good flight efficiency while the addition of a ventral fin further improved directional stability.

![Side and rear views of five aircraft tail configurations: (a) fuselage-mounted conventional, (b) fuselage-mounted V-tail, (c) fuselage-mounted Y-tail, (d) boom-mounted inverted V, and (e) boom-mounted inverted U-shaped.](figures/en/tail_configurations.png){#fig:tail-configurations width=90%}

### Structural material trade-offs

Material selection affects structural mass fraction, thermal performance, and reliability. The commercial benchmarks predominantly use carbon fiber composite construction, with variations in manufacturing approach.

Carbon fiber reinforced polymer (CFRP) provides the highest specific strength and stiffness and is used in all high-performance commercial VTOL UAVs. Manufacturing options include wet layup, prepreg/autoclave, and filament winding, with prepreg construction providing the most consistent material properties. Fiberglass reinforced polymer offers lower cost and easier manufacturing than carbon fiber, and is used for secondary structures and damage-tolerant areas such as wing leading edges and fairings. Foam core sandwich construction, with lightweight foam core between fiber skins, is common for wing skins and fairings and provides excellent stiffness-to-weight for large flat surfaces. Kevlar (aramid fiber) provides high impact resistance and is used for areas subject to damage such as landing gear mount points.

The Martian environment imposes additional constraints on material selection. Diurnal temperature variation from −80 °C to +20 °C causes thermal expansion and contraction; carbon fiber composites have low coefficients of thermal expansion (CTE approximately 0.5 ppm/°C for unidirectional CFRP), reducing thermal stress, and the Ingenuity helicopter used TeXtreme spread tow carbon fabrics specifically selected for resistance to microcracking under these thermal cycles [@latourabOxeonPartOwnedHoldings2025]<!-- #s:textreme -->. The near-vacuum conditions (approximately 600 Pa) eliminate convective heat transfer, making radiative properties critical, and internal thermal management may require gold-plated surfaces (as used in Ingenuity) or multi-layer insulation. The Mars surface radiation dose (approximately 76 mGy/year) is orders of magnitude below polymer degradation thresholds, so radiation is not a significant concern for structural materials over a multi-year mission. Some polymer matrix materials may outgas under low pressure, potentially contaminating optical surfaces, so space-qualified resins with low outgassing characteristics are preferred.
