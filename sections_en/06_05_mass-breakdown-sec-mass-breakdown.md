# Design decisions

## Mass breakdown {#sec:mass-breakdown}

This section presents the detailed component weight estimation methodology and applies it to the selected QuadPlane configuration. The methodology follows Sadraey [@sadraeyDesignUnmannedAerial2020]<!-- #eq2.1 --> [@sadraeyAircraftDesignSystems2013]<!-- #eq10.3 -->, adapted for Mars UAV operating conditions and the geometry established in the constraint analysis (@sec:constraint-analysis).

### Weight estimation methodology

#### Electric UAV weight decomposition

For battery-electric UAVs, the MTOW decomposes into four primary elements [@sadraeyDesignUnmannedAerial2020, Eq. 2.1]<!-- #eq2.1 -->:

$$W_{TO} = W_{PL} + W_A + W_B + W_E$$ {#eq:sadraey-mtow}

where:

* $W_{PL}$ = payload weight (mission sensors, camera, radio relay)
* $W_A$ = autopilot and avionics weight
* $W_B$ = battery weight
* $W_E$ = empty weight (structure, propulsion, wiring, landing gear)

This can be reformulated in terms of weight fractions [@sadraeyDesignUnmannedAerial2020, Eq. 2.2b]<!-- #eq2.2b -->:

$$W_{TO} = \frac{W_{PL} + W_A}{1 - \left(\frac{W_B}{W_{TO}}\right) - \left(\frac{W_E}{W_{TO}}\right)}$$ {#eq:mtow-fractions}

A key difference from fuel-burning aircraft is that battery mass remains constant throughout flight, simplifying the energy budget calculations but requiring careful sizing to meet endurance requirements.

#### Battery mass sizing

The battery mass is determined by mission energy requirements [@sadraeyDesignUnmannedAerial2020, Eq. 2.20]<!-- #eq2.20 -->:

$$W_B = \sum_{i=1}^{n} \frac{P_i \cdot t_i \cdot g_\text{Mars}}{E_D}$$ {#eq:battery-sadraey}

where:

* $P_i$ = power required for flight segment $i$ (W)
* $t_i$ = duration of flight segment $i$ (h)
* $E_D$ = battery energy density (Wh/kg)
* $g_\text{Mars}$ = Mars gravitational acceleration (3.711 m/s²)
* $n$ = number of flight segments

The summation accounts for different power requirements across flight phases (takeoff, climb, cruise, loiter, descent, landing). For the Mars UAV, the hover segments dominate energy consumption due to the high power required in the thin atmosphere.

### Structural weight estimation

Structural component weights are estimated using semi-empirical correlations from Sadraey [@sadraeyAircraftDesignSystems2013]<!-- #eq10.3 -->, adapted for the Mars UAV with reduced ultimate load factor.

#### Wing weight

The wing weight is estimated from [@sadraeyAircraftDesignSystems2013, Eq. 10.3]<!-- #eq10.3 -->:

$$W_W = S_W \cdot MAC \cdot \left(\frac{t}{c}\right)_{\max} \cdot \rho_{\text{mat}} \cdot K_\rho \cdot \left(\frac{AR \cdot n_{\text{ult}}}{\cos \Lambda_{0.25}}\right)^{0.6} \cdot \lambda^{0.04} \cdot g$$ {#eq:wing-weight}

where:

* $S_W$ = wing area (m²)
* $MAC$ = mean aerodynamic chord (m)
* $(t/c)_{\max}$ = maximum thickness ratio
* $\rho_{\text{mat}}$ = material density (kg/m³)
* $K_\rho$ = wing density factor
* $AR$ = aspect ratio
* $n_{\text{ult}}$ = ultimate load factor
* $\Lambda_{0.25}$ = quarter-chord sweep angle
* $\lambda$ = taper ratio

#### Fuselage weight

The fuselage weight is estimated from [@sadraeyAircraftDesignSystems2013, Eq. 10.7]<!-- #eq10.7 -->:

$$W_F = L_f \cdot D_{f_{\max}}^2 \cdot \rho_{\text{mat}} \cdot K_{\rho_f} \cdot n_{\text{ult}}^{0.25} \cdot K_{\text{inlet}} \cdot g$$ {#eq:fuselage-weight}

where:

* $L_f$ = fuselage length (m)
* $D_{f_{\max}}$ = maximum fuselage diameter (m)
* $K_{\rho_f}$ = fuselage density factor
* $K_{\text{inlet}} = 1$ for external inlets

### Load factor adaptation

The ultimate load factor is defined as [@sadraeyAircraftDesignSystems2013, Eq. 10.4]<!-- #eq10.4 -->:

$$n_{\text{ult}} = 1.5 \times n_{\max}$$ {#eq:n-ult-def}

where the safety factor of 1.5 is standard aerospace practice. For the Mars UAV, a limit load factor of $n_{\max} = 2.5$ is adopted (consistent with CS-23 normal category methodology, per @sec:derived-requirements), yielding:

$$n_{\text{ult}} = 1.5 \times 2.5 = 3.75$$

This is significantly lower than the CS-25 value of approximately 5.7 used in transport aircraft design, reflecting:

* Unmanned operation (no crew injury risk)
* Autonomous flight with limited maneuvering envelope
* Reduced gust loads in the thin Mars atmosphere

#### Weight reduction from load factor

From @eq:wing-weight, wing weight scales as $n_{\text{ult}}^{0.6}$. The weight reduction from using $n_{\text{ult}} = 3.75$ instead of 5.7 is:

$$\frac{W_{W,Mars}}{W_{W,ref}} = \left(\frac{3.75}{5.7}\right)^{0.6} = 0.76$$

This represents approximately 24% wing weight reduction.

From @eq:fuselage-weight, fuselage weight scales as $n_{\text{ult}}^{0.25}$:

$$\frac{W_{F,Mars}}{W_{F,ref}} = \left(\frac{3.75}{5.7}\right)^{0.25} = 0.90$$

This represents approximately 10% fuselage weight reduction.

#### Combined structural weight reduction

Assuming wing and fuselage contribute equally to structural weight, the average reduction is approximately 16-17%. For a 10.0 kg MTOW aircraft with an empty weight fraction of 0.45 (approximately 4.5 kg), this translates to approximately 0.72-0.77 kg structural mass savings.

This weight reduction is a significant enabler for mission feasibility, as it can be reallocated to battery capacity (extending endurance) or payload (enhancing mission capability). The reduced load factor is justified by the unmanned, autonomous operation and reduced gust loads in the thin Mars atmosphere, as detailed in @sec:load-factor-selection.

### Application to QuadPlane design

Using the geometry from the constraint analysis (@sec:constraint-analysis) and matching chart results (@sec:comparative-results):

| Parameter | Value | Source |
|:----------|------:|:-------|
| Wing area, $S_W$ | 2.686 m² | Constraint analysis |
| Mean chord, $MAC$ | 0.669 m | Constraint analysis |
| Wingspan, $b$ | 4.01 m | Constraint analysis |
| Aspect ratio, $AR$ | 6 | @sec:derived-requirements |
| Thickness ratio, $(t/c)$ | 0.089 | SD8000 airfoil |
| Taper ratio, $\lambda$ | 0.5 | @sec:derived-requirements |
| Sweep angle, $\Lambda$ | 0° | @sec:derived-requirements |
| Ultimate load factor, $n_{\text{ult}}$ | 3.75 | @sec:derived-requirements |
| Fuselage length, $L_f$ | 2.00 m | @sec:geometry-selection |
| Fuselage diameter, $D_f$ | 0.33 m | @sec:geometry-selection |

: Input parameters for mass breakdown {#tbl:mass-breakdown-inputs}

### Component mass breakdown

The detailed mass breakdown for the selected QuadPlane configuration:

| Component | Mass (kg) | Fraction | Source |
|:----------|----------:|---------:|:-------|
| **Structure** | 2.32 | 23.2% | |
| Wing | 0.80 | 8.0% | @eq:wing-weight with CFRP |
| Fuselage | 0.45 | 4.5% | @eq:fuselage-weight with CFRP |
| Empennage (V-tail) | 0.35 | 3.5% | Scaling from wing (1.144 m²) |
| Booms (4×) | 0.40 | 4.0% | Structural analysis |
| Landing gear | 0.32 | 3.2% | 3.2% of MTOW |
| **Propulsion** | 1.18 | 11.8% | |
| Lift motors (8×) | 0.528 | 5.3% | SunnySky V4006-380, 66 g each |
| Cruise motors (2×) | 0.120 | 1.2% | T-Motor AT2312-1150, 60 g each |
| ESCs (10×) | 0.060 | 0.6% | Hobbywing XRotor Micro 30A, 6 g each |
| Propellers (10×) | 0.174 | 1.7% | 8× lift (18 g) + 2× cruise (15 g) |
| Mounting + wiring | 0.300 | 3.0% | Engineering estimate |
| **Energy** | 3.50 | 35.0% | |
| Battery pack | 3.50 | 35.0% | @sec:energy-data, 945 Wh total |
| **Payload** | 1.50 | 15.0% | |
| Camera system | 0.30 | 3.0% | @sec:payload-systems |
| Radio relay | 0.15 | 1.5% | @sec:payload-systems |
| Payload margin | 1.05 | 10.5% | Growth allowance |
| **Avionics** | 0.50 | 5.0% | |
| Flight controller | 0.10 | 1.0% | Pixhawk-class autopilot |
| Sensors & wiring | 0.40 | 4.0% | GPS, IMU, telemetry |
| **Subtotal** | 9.00 | 90.0% | |
| **Design margin** | 1.00 | 10.0% | Contingency |
| **Total MTOW** | 10.00 | 100% | — |

: QuadPlane mass breakdown {#tbl:quadplane-mass-breakdown}

### Limitations for small UAVs

The weight estimation equations from Sadraey [@sadraeyAircraftDesignSystems2013]<!-- #ch10:limits --> were developed primarily for conventional manned aircraft and may not be directly applicable to small composite UAVs below 50 kg MTOW. To address this limitation:

1. Mass fraction validation: estimated component weights are cross-checked against the empirical mass fractions from @tbl:design-mass-fractions derived from commercial UAV benchmarks.

2. Conservative approach: where uncertainty exists, conservative (higher) weight estimates are used to maintain design margins.

3. Iteration with component data: the weight estimate is refined after component selection (@sec:component-verification) using actual manufacturer data for motors, batteries, and avionics.

4. Composite material factors: the density factors ($K_\rho$, $K_{\rho_f}$) are adjusted to reflect CFRP construction rather than aluminum, per the material trade-off analysis in @sec:materials-data.

### Verification against mass fractions

The calculated component masses are verified against the mass fraction targets from @sec:initial-mass-estimate:

| Category | Target fraction | Calculated fraction | Status |
|:---------|----------------:|--------------------:|:------:|
| Battery | 0.35 | 0.35 | MATCH |
| Payload | 0.15 | 0.15 | MATCH |
| Structure | 0.23 | 0.23 | MATCH |
| Propulsion | 0.20 | 0.12 | UNDER (margin available) |
| Avionics | 0.05 | 0.05 | MATCH |
| Design margin | — | 0.10 | ALLOCATED |
| **Total** | 1.00 | 1.00 | BALANCED |

: Mass fraction verification {#tbl:mass-fraction-verification}

The propulsion mass fraction (11.8%) is significantly below the 20% budget, providing a margin of 0.82 kg that has been reallocated to structure and design contingency. This margin reflects the selection of modern lightweight motor/ESC combinations and validates the constraint analysis assumptions.
