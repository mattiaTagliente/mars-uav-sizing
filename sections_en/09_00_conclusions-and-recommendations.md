# Conclusions and recommendations {#sec:conclusions}

This feasibility study has assessed the viability of deploying an autonomous UAV from a crewed Mars habitat to support mapping and telecommunication relay missions. The analysis focused on conceptual sizing and component selection, establishing the foundation for subsequent design phases.

## Summary of findings {#sec:summary-findings}

The study evaluated three candidate architectures—rotorcraft, fixed-wing, and hybrid VTOL—through constraint-based sizing analysis. Key findings include:

* The **QuadPlane hybrid architecture** provides an effective compromise between VTOL capability and cruise efficiency, achieving a 49% energy margin over mission requirements
* **Low Reynolds number effects** (Re ≈ 55,000) significantly impact aerodynamic design; the SD8000 airfoil offers consistent low-drag performance with adequate stall margin (4.6°)
* **Hover power dominates motor sizing**; fixed-wing cruise power is substantially lower than hover power, favoring configurations that minimize hover duration
* Current **battery technology** (150 Wh/kg) enables practical mission durations of approximately 90 minutes with 20% reserve
* The pure rotorcraft configuration is **marginally feasible** but offers limited operational margin; the fixed-wing configuration is **not feasible** without runway infrastructure

## Recommendations {#sec:recommendations}

Based on the analysis, the following recommendations are made for the preliminary design phase:

1. **Proceed with QuadPlane architecture**: The octocopter lift system with coaxial cruise propeller configuration offers the best balance of performance, reliability, and operational flexibility
2. **Technology development**: Prioritize improved battery specific energy (>200 Wh/kg) for significant performance gains in future iterations
3. **Airfoil validation**: Wind tunnel testing of the SD8000 airfoil at Mars-representative Reynolds numbers is warranted to confirm the low-speed aerodynamic predictions
4. **Dust mitigation**: Surface contamination effects on rotor and wing performance require investigation, particularly for long-duration surface operations

## Future work {#sec:future-work}

This feasibility study employed a baseline-case methodology with fixed reference MTOW to enable fair comparison across architectures. Several improvements to the sizing methodology and additional subsystem analyses are identified for subsequent design phases.

### Sizing methodology improvements

The current baseline approach uses fixed mass fractions and a reference MTOW. Future iterations should implement:

* **Configuration-specific coupled closures**: Iterative sizing that solves for MTOW and battery mass simultaneously for each architecture, given payload mass, mission segment times, and energy reserve requirements. This would enable optimization rather than feasibility checking
* **Component-based mass model**: Replacing fixed mass fractions with a build-up model for battery, payload, propulsion, and structure subsystems. Payload fraction plausibility should be constrained using the reference drone database
* **Configuration-appropriate constraint diagrams**: Power-to-weight versus disk loading (P/W vs DL) for rotorcraft; power-to-weight versus wing loading (P/W vs W/S) for fixed-wing and hybrid VTOL, with parametric sweeps in disk loading and mission segment times

### Subsystem analyses

Several critical subsystems were identified but deferred to subsequent design phases:

* **Avionics system design**: Selection and integration of the flight controller, inertial measurement unit, altimeter, and air data sensors appropriate for the low-density Mars atmosphere. Definition of the telemetry link architecture between the UAV and habitat
* **Thermal management analysis**: Detailed thermal modeling for the extreme Mars diurnal temperature range (approximately −80 °C to −20 °C). Design of active heating systems for battery and avionics thermal protection during night storage and flight operations
* **Structural analysis and detailed design**: Finite element analysis of the airframe, wing, and boom structure. Vibration analysis for rotor-induced loads. Material qualification for the Mars radiation and thermal environment. **Fuselage length trade-off analysis**: The benchmark-median fuselage ratio (0.50) was adopted without detailed optimization; shorter fuselages reduce structural mass and wetted area while longer fuselages provide more tail moment arm (enabling smaller tail surfaces) and more internal volume margin. Quantitative analysis of these competing effects is needed to identify the optimal configuration

These methodology improvements and subsystem analyses are essential prerequisites for advancing from feasibility to preliminary design review (PDR).

---

The Mars UAV concept is **technically feasible** with current or near-term technology. The QuadPlane configuration meets all primary mission requirements with adequate margin, providing a viable platform for extending the operational reach of crewed Mars surface missions.
