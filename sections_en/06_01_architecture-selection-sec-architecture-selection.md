# Design decisions

## Architecture selection {#sec:architecture-selection}

This section consolidates the configuration comparison from the constraint analysis (@sec:constraint-analysis), presents the elimination rationale for alternative configurations, and documents the selected QuadPlane architecture with its design decisions.

### Configuration comparison

#### Quantitative summary

@tbl:config-comparison synthesises the analyses of the three candidate configurations—rotorcraft (@sec:rotorcraft-analysis), fixed-wing (@sec:fixed-wing-analysis), and hybrid VTOL (@sec:hybrid-vtol-analysis).

| Criterion | Rotorcraft | Fixed-Wing | Hybrid VTOL |
|:----------|:----------:|:----------:|:-----------:|
| **Aerodynamic efficiency** | | | |
| L/D or $(L/D)_\text{eff}$ | 4.0 | 11.7 | 10.5 |
| **Power requirements** | | | |
| Hover P/W (W/N) | 85.7 | — | 85.7 |
| Cruise P/W (W/N) | 12.4$^a$ | 7.7 | 8.6 |
| Cruise power (W) | 460$^a$ | 286 | 318 |
| **Mission capability** | | | |
| Endurance (min) | 57 | 121 | 81 |
| Endurance margin | −4.5% | +101% | +35.7% |
| Range (km) | 130 | 289 | 188 |
| Range margin | +30% | +189% | +88% |
| **Operational** | | | |
| VTOL capable | ✓ Yes | ❌ No | ✓ Yes |
| Infrastructure | None | ~1 km runway | None |
| Glide capability | ❌ No | ✓ Yes | ✓ Yes$^b$ |
| **Mass budget** | | | |
| Propulsion fraction | ~15% | ~8% | ~25% |
| Mass penalty | — | — | +17% |
| **Requirements compliance** | | | |
| Meets endurance | ❌ | ✓ | ✓ |
| Meets range | ✓ | ✓ | ✓ |
| Meets VTOL | ✓ | ❌ | ✓ |
| **RECOMMENDATION** | ❌ ELIMINATED | ❌ Not feasible | ✓ **SELECTED** |

: Configuration comparison summary {#tbl:config-comparison}

$^a$ Rotorcraft forward flight power at 40 m/s cruise; hover power is 3178 W.
$^b$ QuadPlane can glide in cruise mode if cruise motor fails, extending time for emergency VTOL landing.

#### Aerodynamic efficiency comparison

| Configuration | L/D type | Value | Source |
|:--------------|:---------|------:|:-------|
| Rotorcraft | $(L/D)_\text{eff}$ | 4.0 | Forward flight power analysis (@sec:rotorcraft-analysis) |
| Fixed-wing | $(L/D)$ | 11.7 | Drag polar at optimal $C_L$ (@sec:fixed-wing-analysis) |
| Hybrid VTOL | $(L/D)$ | 10.5 | Wing-borne cruise with rotor drag penalty (@sec:hybrid-vtol-analysis) |

: Aerodynamic efficiency comparison {#tbl:aerodynamic-efficiency-comparison}

Fixed-wing and hybrid VTOL configurations share similar cruise efficiency because the QuadPlane uses wing lift during cruise. The 10% reduction in QuadPlane L/D (from 11.7 to 10.5) accounts for parasitic drag from the stopped lift rotors and their mounting hardware. Rotorcraft, constrained by rotor-borne flight throughout the mission, achieves only $(L/D)_\text{eff} \approx 4$—approximately one-third of fixed-wing efficiency.

#### Power requirements comparison

| Configuration | Hover P/W (W/N) | Cruise P/W (W/N) | Notes |
|:--------------|:---------------:|:----------------:|:------|
| Rotorcraft | 85.7 | 12.4 | Forward flight at $(L/D)_\text{eff} \approx 4$ |
| Fixed-wing | N/A | 7.7 | No hover capability |
| Hybrid VTOL | 85.7 | 8.6 | Decoupled systems; hover rare, cruise dominant |

: Power loading comparison {#tbl:power-requirements}

For the hybrid VTOL, hover consumes 3178 W (85.7 W/N), but cruise requires only 318 W (8.6 W/N)—approximately ten times lower. This disparity fundamentally changes the energy equation when hover time is minimised.

### Elimination of alternatives

#### Rotorcraft: ELIMINATED

The pure rotorcraft configuration is eliminated from consideration for the following reasons:

* **Fails endurance requirement:** The configuration achieves only 57 min endurance vs 60 min required (−4.5% margin), failing the fundamental mission requirement. Any deviation from nominal conditions—battery degradation, atmospheric density variation, navigation inefficiency—would further degrade performance.

* **High parameter sensitivity:** A 10% reduction in atmospheric density (possible during seasonal variations) increases power requirements by approximately 5%, eliminating the endurance margin entirely.

* **No glide capability:** If a rotor fails in forward flight, a multirotor cannot glide to extend time for emergency procedures. The aircraft crashes immediately, with no recovery options.

* **No improvement path:** Unlike marginal fixed-wing performance that could be enhanced with more advanced airfoils, the rotorcraft limitation is fundamental—$(L/D)_\text{eff} \approx 4$ is a physical consequence of rotor-borne flight.

#### Fixed-wing: NOT FEASIBLE

The pure fixed-wing configuration is eliminated from consideration because it **cannot meet the VTOL requirement**:

* **Runway requirement:** Takeoff ground roll is calculated at approximately 1060 m, requiring runway infrastructure that does not exist on Mars.

* **No practical alternatives:** Catapult launch, rocket-assisted takeoff (RATO), and balloon-drop launch all require substantial infrastructure, consumables, or crew intervention incompatible with autonomous habitat operations.

* **Landing equally problematic:** Approach at ~45 m/s with landing roll measured in hundreds of metres is incompatible with unprepared terrain.

Despite demonstrating good aerodynamic efficiency ($(L/D) = 11.7$) and strong theoretical performance (121 min endurance with 20% reserve, 289 km range), the fixed-wing configuration is **operationally impossible**.

### Selection of hybrid VTOL (QuadPlane)

The hybrid VTOL configuration is selected as the Mars UAV baseline because it is the **only architecture that satisfies all mission requirements simultaneously**:

* **VTOL capability:** Lift rotors provide vertical takeoff and landing without ground infrastructure (✓)

* **Adequate endurance margin:** 90 minutes achieved vs 60 minutes required (+50% margin) (✓)

* **Adequate range margin:** 208 km achieved vs 100 km required (+108% margin) (✓)

* **Degraded-mode capability:** If the cruise motor fails, the aircraft can glide to extend time for emergency VTOL landing, unlike pure rotorcraft which crashes immediately.

* **Energy feasibility:** Required 502 Wh vs available 718 Wh (+43% margin above requirement).

The configuration accepts a mass penalty of approximately 17% of MTOW for the dual propulsion system. This penalty is justified because:

1. It enables the mission (no alternative for VTOL + efficient cruise)
2. It provides substantial safety margins versus rotorcraft
3. It maintains degraded-mode operation options

### Configuration summary

From the matching chart analysis (@sec:comparative-results), the selected QuadPlane design point is characterised by:

| Parameter | Value | Constraint |
|:----------|------:|:-----------|
| Wing loading, $W/S$ | 14.42 N/m² | Set by stall limit at $V_\text{min}$ = 35.04 m/s |
| Power loading, $P/W$ | 85.71 W/N | Set by hover requirement |
| Disk loading, $DL$ | 30.00 N/m² | Compromise between rotor size and power |
| MTOW | 10.00 kg | Baseline from @sec:initial-mass-estimate |
| Wing area | 2.574 m² | $S = W/(W/S)$ |
| Wingspan | 3.93 m | $b = \sqrt{AR \times S}$ at AR = 6 |

: QuadPlane design point summary {#tbl:quadplane-design-point}

### QuadPlane configuration rationale

The QuadPlane architecture is selected for the Mars UAV based on mission requirements and operational constraints.

#### Mission compatibility

The dual mission objectives, mapping and telecommunication relay, require extended flight time over large areas. Fixed-wing cruise provides the necessary range and endurance, while VTOL capability enables operations from an unprepared habitat site. The QuadPlane architecture directly addresses both requirements.

#### Fault tolerance

For a Mars UAV where in-flight repair is impossible, single-fault tolerance is essential. An octocopter lift configuration (eight motors in four coaxial pairs) provides this capability: the UAV can complete a controlled landing with any single motor failed. Each coaxial pair shares a structural mount, with upper and lower rotors counter-rotating to cancel torque.

To extend single-fault tolerance to the cruise phase, a coaxial contra-rotating tractor configuration is selected. Two cruise propellers are mounted coaxially at the bow of the fuselage, driven by independent motors and rotating in opposite directions. Each motor is sized to provide 60% of the nominal cruise thrust, ensuring that failure of either cruise motor allows the mission to continue with reduced performance rather than requiring immediate abort. The 20% total thrust margin accounts for the additional drag from the windmilling failed propeller.

This bow-mounted coaxial configuration offers several advantages over alternatives such as aft-mounted pushers or wing-mounted side-by-side propellers [@roskamAirplaneDesign22004]:

* Clean airflow: tractor propellers operate in undisturbed air ahead of the fuselage, leading to higher propulsive efficiency compared to pusher configurations where the propeller encounters turbulent wake from the airframe. This efficiency advantage is well-documented in aircraft design literature, with pusher propellers typically experiencing 2–15% efficiency losses due to wake ingestion.
* Torque cancellation: contra-rotating propellers cancel reactive torque, eliminating asymmetric yaw moments during cruise and improving directional stability. This is particularly beneficial for a vehicle operating autonomously without pilot correction.
* Compact footprint: a coaxial arrangement concentrates both propellers along the fuselage axis, maintaining a streamlined profile and avoiding the aerodynamic interference and structural complexity of side-by-side wing-mounted propellers.

A trade-off of this tractor configuration is that forward-looking cameras are obstructed by the propellers. For the mapping mission, the primary payload camera is nadir-looking (downward-facing), which remains unobstructed. Navigation sensors requiring forward visibility can be mounted on the wing leading edge or use aft-facing orientations.

The resulting propulsion architecture comprises 10 motors total: eight lift motors in four coaxial pairs plus two coaxial cruise motors at the bow. This configuration achieves full single-fault tolerance across all flight phases without relying on cross-system redundancy (i.e., using lift motors for cruise return), which would severely limit operational radius due to the lower efficiency of multicopter forward flight.

#### Operational simplicity

Compared to other VTOL approaches (tilt-rotor, tilt-wing, tail-sitter), the QuadPlane offers several advantages. The configuration requires no tilting actuators or variable-geometry components, resulting in simpler mechanisms with fewer failure modes. Hover and cruise use separate propulsion systems, decoupling the flight modes and simplifying control system design. The architecture benefits from extensive commercial flight heritage with mature autopilot support, reducing development risk. Finally, components are accessible and modular, enabling easier maintenance. These factors improve reliability in the Mars environment where maintenance capability is severely constrained.

### Tail configuration selection

Based on the trade-off analysis, a boom-mounted inverted V-tail configuration is selected. This choice leverages the structural booms already required for the octocopter lift motors.

The rear lift motor booms extend aft to support the tail surfaces, eliminating the need for a separate tail boom structure and reducing overall structural mass. The boom-mounted configuration provides a longer moment arm than a fuselage-mounted tail would allow with the compact fuselage selected for this design, compensating for the reduced control effectiveness at Mars Reynolds numbers. The inverted V geometry angles the surfaces upward from the fuselage centerline, providing clearance from the surface during landing on uneven terrain. Additionally, the V-tail surfaces are positioned outside the cruise propeller slipstream (bow-mounted tractor configuration), ensuring undisturbed airflow over the control surfaces.

The inverted V arrangement combines pitch and yaw control in two surfaces with ruddervator-style mixing. CFD studies of boom-mounted empennage configurations found that inverted U boom designs provided superior longitudinal stability and stall characteristics for surveillance missions [@nugrohoPerformanceAnalysisEmpennage2022], and the two-surface design reduces parts count compared to a three-surface conventional tail.

Tail surface sizing for Mars conditions is addressed in @sec:geometry-selection, where tail volume coefficients and Reynolds number effects are quantified.

### Fuselage geometry selection

The commercial benchmarks exhibit a length-to-wingspan ratio ranging from 0.28 to 0.63, with a median of approximately 0.50 (@tbl:reference-fuselage). However, direct scaling of this ratio to Mars conditions would yield an impractically large fuselage: with the 3.93 m wingspan required for Mars flight (derived in @sec:geometry-selection), a 0.50 ratio would produce a 2 m fuselage, far exceeding the internal volume requirements for a 10 kg UAV.

This discrepancy arises because fuselage size is driven primarily by internal volume requirements (batteries, payload, avionics), which do not scale with atmospheric density, while wingspan is driven by lift requirements, which scale significantly with the thin Mars atmosphere. The correct approach sizes the fuselage based on functional requirements rather than ratio scaling.

The 10 kg target MTOW requires accommodation payloads (camera and radio systems) plus batteries; these components require approximately 4–5 L of internal volume with margins for routing and thermal management. A fuselage length of 1.5–2.0 m provides adequate internal volume while maintaining a streamlined profile with fineness ratio of 5–7 [@gottenFullConfigurationDrag2021]. This results in a length-to-wingspan ratio of approximately 0.25–0.30, lower than commercial benchmarks but consistent with the Mars-specific scaling constraints.

The selected fuselage length provides adequate moment arm for the boom-mounted tail surfaces when combined with the structural booms extending aft, achieving the required longitudinal and directional stability without excessive tail surface area.

Fuselage cross-section and detailed dimensioning are addressed in @sec:geometry-selection.

### Material selection

Carbon fiber reinforced polymer (CFRP) is selected as the primary structural material, consistent with Ingenuity heritage and commercial practice.

CFRP exhibits low thermal expansion (CTE ~0.5 ppm/°C), minimizing thermal stress from the −80°C to +20°C diurnal temperature cycle on Mars. It provides the highest strength-to-weight ratio of commonly available structural materials, supporting the mass minimization critical for Mars flight. The Ingenuity helicopter successfully demonstrated CFRP construction on Mars, using TeXtreme® spread tow carbon fabrics selected for resistance to thermal cycling microcracking [@latourabOxeonPartOwnedHoldings2025].

Wing and fuselage skins will use foam-core sandwich construction with carbon fiber face sheets, providing high stiffness-to-weight for primary aerodynamic surfaces. The lift motor and tail support booms will be carbon fiber tubes, either filament-wound or pultruded. Fiberglass reinforcement will be used at landing gear attachment points and vulnerable leading edges for impact tolerance. Internal thermal management will employ gold-plated interior surfaces or multi-layer insulation for electronics compartment thermal control, following Ingenuity practice.

Material selection implications for structural mass fraction are addressed in @sec:material-selection.

![Proposed QuadPlane concept with octocopter lift configuration and coaxial tractor cruise propellers.](figures/our_proposal_concept.jpg){#fig:concept-architecture width=70%}
