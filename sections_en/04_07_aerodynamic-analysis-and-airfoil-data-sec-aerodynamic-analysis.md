# Reference data and trade-off analysis

## Aerodynamic analysis and airfoil data {#sec:aerodynamic-analysis}

### Low Reynolds number flight {#sec:low-reynolds}

The combination of low atmospheric density and moderate flight speeds on Mars results in Reynolds numbers far below typical terrestrial aircraft. At low Reynolds numbers (below approximately 100,000), viscous effects dominate aerodynamic performance. Boundary layer transition, laminar separation bubbles, and flow separation behavior differ substantially from high-Reynolds conditions, degrading airfoil performance relative to theoretical predictions.

Very low Reynolds numbers are detrimental to aerodynamic efficiency due to these viscous effects. However, achieving higher Reynolds numbers requires either larger chord (increasing mass and wing surface area) or higher velocity (increasing cruise power, since power scales with $V^3$ once parasite drag dominates). A target Reynolds number of approximately 60,000 is adopted as a compromise: it provides acceptable airfoil performance based on available wind tunnel data while limiting wing chord and cruise velocity to reasonable values.
The specific cruise velocity and chord values that achieve this target are derived in @sec:derived-requirements based on the coupled constraints of Mach number, Reynolds number, and wing geometry.

### Airfoil experimental data {#sec:airfoil-data}

Seven low-Reynolds airfoils were evaluated using experimental data from the UIUC Low-Speed Airfoil Tests program [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:e387:re61k --> [@williamsonSummaryLowSpeedAirfoil2012]<!-- #v5:ag455ct:re60k -->. The candidates include the Eppler 387 (E387), widely studied for low-Reynolds applications with extensive experimental validation; the SD8000, a low-drag design optimized for minimum profile drag; the S7055, a moderate camber design balancing lift and drag; the AG455ct-02r and AG35-r, thin reflexed airfoils designed for flying wings and tailless aircraft; the SD7037B, a popular general-purpose low-Reynolds airfoil; and the AG12, a low-camber thin airfoil for high-speed applications.

At Reynolds numbers below 100,000, XFOIL boundary layer calculations exhibit convergence difficulties due to laminar separation bubbles and transition phenomena. Wind tunnel data from the UIUC database provides validated performance characteristics at these conditions. Performance data at $Re \approx 60{,}000$ are summarized in @tbl:airfoil-comparison.

: Airfoil performance at Re ≈ 60,000 from UIUC wind tunnel data [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:sd8000:re61k --> [@williamsonSummaryLowSpeedAirfoil2012]<!-- #v5:ag12:re60k --> {#tbl:airfoil-comparison}

| Airfoil | Test Re | $C_{L,\text{max}}$ | $\alpha_\text{stall}$ | $(L/D)_\text{max}$ | $C_L$ at $(L/D)_\text{max}$ | Source |
|:--------|--------:|-------------------:|----------------------:|-------------------:|----------------------------:|:-------|
| E387    |  61,000 |               1.22 |                 10.2° |               46.6 |                        1.20 | Vol. 1 |
| SD8000  |  60,800 |               1.15 |                 11.5° |               45.4 |                        0.94 | Vol. 1 |
| S7055   |  60,700 |               1.23 |                  9.7° |               41.6 |                        1.23 | Vol. 1 |
| AG455ct |  60,157 |               1.06 |                  9.2° |               40.0 |                        0.56 | Vol. 5 |
| SD7037B |  60,500 |               1.22 |                 11.1° |               36.6 |                        0.92 | Vol. 1 |
| AG12    |  59,972 |               1.06 |                 10.3° |               34.6 |                        0.71 | Vol. 5 |
| AG35-r  |  59,904 |               1.04 |                 11.4° |               30.7 |                        0.96 | Vol. 5 |

The AG-series reflexed airfoils (AG455ct-02r, AG35-r) are designed for tailless aircraft with self-stabilizing pitching moment characteristics, which reduces their aerodynamic efficiency compared to conventional cambered airfoils. For sizing purposes, the maximum lift coefficient is taken as $C_{L,\text{max}}$ = 1.15 based on the SD8000 airfoil selected in @sec:airfoil-selection. The SD8000 is chosen for its consistent drag behaviour and larger stall margin compared to the E387, which achieves marginally higher peak efficiency but at an operating point very close to stall.

### Drag polar model

The aircraft drag polar is modeled as:

$$C_D = C_{D,0} + \frac{C_L^2}{π \cdot AR \cdot e}$$ {#eq:drag-polar}

where $C_{D,0}$ is the zero-lift drag coefficient, $AR$ is the wing aspect ratio, and $e$ is the Oswald span efficiency factor [@sadraeyAircraftDesignSystems2013]<!-- #ch5:eq5.x -->.

#### Oswald efficiency factor

The Oswald span efficiency factor accounts for the deviation from ideal elliptical lift distribution and other induced drag sources. For straight (unswept) wings, Sadraey provides the empirical correlation [@sadraeyAircraftDesignSystems2013]<!-- #ch5:oswald -->:

$$e = 1.78 \times (1 - 0.045 \times AR^{0.68}) - 0.64$$ {#eq:oswald-correlation}

This correlation is valid for aspect ratios in the range 6-20. Applying @eq:oswald-correlation for aspect ratios of interest yields the values in @tbl:oswald-values.

: Oswald efficiency factor from Sadraey correlation [@sadraeyAircraftDesignSystems2013]<!-- #ch5:oswald-range --> {#tbl:oswald-values}

| Aspect Ratio | $e$ (calculated) |
|:-------------|:----------------:|
| 5            | 0.90             |
| 6            | 0.87             |
| 7            | 0.84             |

Typical values for the Oswald efficiency factor range from 0.7 to 0.95 [@sadraeyAircraftDesignSystems2013]<!-- #ch5:oswald-range -->. The correlation yields $e$ = 0.87 for the baseline aspect ratio of 6, which falls within the expected range. The higher Oswald efficiency at lower aspect ratios partially compensates for the increased induced drag, improving the trade-off.

#### Zero-lift drag coefficient

The zero-lift drag coefficient is estimated using the equivalent skin friction method [@gottenFullConfigurationDrag2021]<!-- #abs -->:

$$C_{D,0} = C_{f,\text{eq}} \times \frac{S_\text{wet}}{S_\text{ref}}$$ {#eq:cd0-method}

where $C_{f,\text{eq}}$ is an equivalent skin friction coefficient for the aircraft category, $S_\text{wet}$ is the total wetted area, and $S_\text{ref}$ is the wing reference area.

Götten et al. analyzed ten reconnaissance UAVs and found that miscellaneous components such as fixed landing gear and sensor turrets contribute 36-60% of total parasitic drag [@gottenFullConfigurationDrag2021]<!-- #tbl2 -->. Their derived equivalent skin friction coefficient for short-to-medium range UAVs is $C_{f,\text{eq}}$ = 0.0128 [@gottenFullConfigurationDrag2021]<!-- #s4:cfe -->, significantly higher than manned aircraft categories.

For the Mars UAV, several factors suggest a lower $C_{f,\text{eq}}$ is appropriate: no fixed landing gear (VTOL operation from habitat), no external sensor turret (camera integrated in payload bay), clean aerodynamic design with fewer protrusions, and VTOL rotors stowed or feathered during cruise. A value of $C_{f,\text{eq}}$ = 0.0055, corresponding to clean light aircraft, is adopted. With an estimated wetted area ratio of $S_\text{wet}/S_\text{ref} \approx 5.5$ for the QuadPlane configuration (accounting for fuselage, tail booms, and VTOL rotors):

$$C_{D,0} = 0.0055 \times 5.5 = 0.030$$ {#eq:cd0-calculation}

This value is consistent with statistical estimates for clean light aircraft ($C_{D,0}$ = 0.020-0.030) and small UAVs without fixed landing gear.

#### Complete drag polar

With the estimated coefficients, the complete drag polar for $AR$ = 6 is:

$$C_D = 0.03000 + \frac{C_L^2}{\pi \times 6 \times 0.8692} = 0.03000 + 0.06103 \times C_L^2$$ {#eq:drag-polar-ar6}

The induced drag factor is $K = 1/(\pi \cdot AR \cdot e)$ = 0.06103.

Maximum lift-to-drag ratio occurs when induced drag equals parasitic drag:

$$(L/D)_\text{max} = \frac{1}{2}\sqrt{\frac{\pi \cdot AR \cdot e}{C_{D,0}}} = \frac{1}{2}\sqrt{\frac{\pi \times 6 \times 0.8692}{0.03000}} = 11.68$$ {#eq:ld-max-calculated}

The corresponding lift coefficient at maximum L/D is:

$$C_{L}^{*} = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = \sqrt{\pi \times 6 \times 0.8692 \times 0.03000} = 0.7011$$ {#eq:cl-optimum}

The aircraft $(L/D)_\text{max}$ of 11.68 is lower than the 2D airfoil $(L/D)_\text{max}$ of 45.4 for the SD8000. This reduction is expected because the aircraft drag includes fuselage, tail, interference, and three-dimensional induced drag effects not present in 2D airfoil testing. The lower aspect ratio compared to high-efficiency sailplanes results in higher induced drag, which dominates the drag budget at the moderate lift coefficients required for Mars flight.

### Aerodynamic coefficients summary

@tbl:aero-coefficients summarizes the aerodynamic parameters for the constraint analysis.

: Aerodynamic coefficients for Mars UAV constraint analysis {#tbl:aero-coefficients}

| Parameter | Symbol | Value | Source |
|:----------|:------:|:-----:|:-------|
| Maximum lift coefficient | $C_{L,\text{max}}$ | 1.150 | SD8000 (UIUC wind tunnel) |
| Oswald efficiency factor | $e$ | 0.8692 | Sadraey correlation (AR = 6) |
| Zero-lift drag coefficient | $C_{D,0}$ | 0.03000 | Equivalent friction method |
| Aspect ratio | $AR$ | 6 | Design selection |
| Maximum lift-to-drag ratio | $(L/D)_\text{max}$ | 11.68 | Calculated |
| Lift coefficient at $(L/D)_\text{max}$ | $C_L^{*}$ | 0.7011 | Calculated |

These values are used in the constraint analysis (@sec:constraint-analysis) to determine the design space boundaries for power loading and wing loading.
