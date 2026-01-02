# Design decisions

## Airfoil selection {#sec:airfoil-selection}

This section presents the airfoil selection rationale for the Mars UAV wing design based on the performance data summarized in @sec:aerodynamic-analysis. The selection process evaluates seven candidate airfoils at the target Reynolds number of approximately 60,000, corresponding to Mars cruise conditions.

### Selection criteria

The airfoil selection is driven by three primary criteria, weighted by their importance to mission success:

1. Cruise efficiency (60% weight): Maximum lift-to-drag ratio $(L/D)_\text{max}$ directly determines cruise range and endurance. Higher $(L/D)_\text{max}$ reduces cruise power and extends battery life.

2. Stall margin (25% weight): Maximum lift coefficient $C_{L,\text{max}}$ determines the minimum flight speed and provides margin against gusts or manoeuvres. A higher $C_{L,\text{max}}$ enables smaller wing area or lower approach speeds.

3. Stall angle (15% weight): A higher stall angle $\alpha_\text{stall}$ provides a wider operational envelope and gentler stall characteristics, improving controllability in the low-density Martian atmosphere.

### Performance comparison

The seven candidate airfoils from @tbl:airfoil-comparison exhibit distinct performance characteristics at the target Reynolds number. @fig:airfoil-ld-alpha presents the efficiency curves showing how lift-to-drag ratio varies with angle of attack.

![Lift-to-drag ratio vs angle of attack for candidate airfoils at Re ≈ 60,000. While the E387 achieves the highest peak efficiency of (L/D)_max = 46.6, this occurs very close to stall. The SD8000 achieves (L/D)_max = 45.4 with a larger margin to stall.](figures/airfoil_ld_alpha_en.png){#fig:airfoil-ld-alpha}

### Airfoil comparison

The seven candidate airfoils from @tbl:airfoil-comparison are evaluated against the three selection criteria. Based on weighted scoring, the airfoils separate into three tiers:

The first tier comprises the E387, SD8000, and S7055, which achieve the highest cruise efficiency with $(L/D)_\text{max}$ exceeding 41. The E387 leads with $(L/D)_\text{max}$ = 46.6, followed by the SD8000 at 45.4 and the S7055 at 41.6. These three airfoils also provide adequate maximum lift coefficients ($C_{L,\text{max}}$ = 1.15 to 1.23) for the expected wing loading.

The second tier includes the SD7037B and AG455ct-02r. The SD7037B achieves moderate efficiency ($(L/D)_\text{max}$ = 36.6) with good stall characteristics ($\alpha_\text{stall}$ = 11.1°), but its higher drag at cruise conditions reduces its competitiveness. The AG455ct-02r, designed for tailless aircraft, has a lower maximum lift coefficient ($C_{L,\text{max}}$ = 1.06) and operates at lower $C_L$ values, making it less suitable for the wing loading required by Mars UAV operations.

The third tier consists of the AG12 and AG35-r, both reflexed airfoils designed for flying wings. Their self-stabilizing pitching moment characteristics come at the expense of aerodynamic efficiency, with $(L/D)_\text{max}$ values of 34.6 and 30.7. These airfoils are not suited to the conventional tailed configuration adopted for this design.

The S7055 is excluded from final consideration despite its high $C_{L,\text{max}}$ = 1.23 because it stalls at $\alpha_\text{stall}$ = 9.7°, the lowest of all candidates. This early stall provides insufficient margin for safe operation in the Martian atmosphere. The remaining first-tier candidates, E387 and SD8000, are compared in detail.

Initial analysis based on weighted criteria alone would favour the E387 for its highest $(L/D)_\text{max}$ = 46.6. However, examination of the polar data reveals an operational concern: the E387's peak efficiency occurs at α = 8.8°, only 1.3° from its stall angle of 10.2°. This narrow margin raises concerns for practical operation.

Furthermore, the E387 exhibits an anomalous drag reduction at α ≈ 9° ($C_d$ = 0.0257) compared to adjacent angles ($C_d$ = 0.0377 at α = 7° and $C_d$ = 0.0393 at α = 10.2°). This behaviour is attributed to laminar separation bubble (LSB) collapse, a well-documented phenomenon for this airfoil at low Reynolds numbers [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:lsb -->. While physically real, this operating point is sensitive and unreliable for design.

@tbl:e387-sd8000-comparison presents a detailed comparison of the two leading candidates.

: Comparison of E387 and SD8000 airfoils at Re ≈ 60,000 {#tbl:e387-sd8000-comparison}

| Parameter | E387 | SD8000 | Advantage |
|:----------|-----:|-------:|:----------|
| Minimum drag $C_{D,\text{min}}$ | 0.0228 | 0.0142 | SD8000 (38% lower) |
| Maximum efficiency $(L/D)_\text{max}$ | 46.6 | 45.4 | E387 (3% higher) |
| Maximum lift $C_{L,\text{max}}$ | 1.22 | 1.15 | E387 (6% higher) |
| Angle at $(L/D)_\text{max}$ | 8.8° | 7.0° | N/A |
| Stall angle | 10.2° | 11.5° | SD8000 |
| Margin to stall | 1.3° | 4.6° | SD8000 (3.5× larger) |

The SD8000 offers superior drag characteristics across the entire operating range. At typical cruise lift coefficients (0.7 < $C_L$ < 0.9), the SD8000 achieves significantly higher L/D than the E387 due to its lower profile drag.

@fig:airfoil-polar presents the drag polar showing the relationship between lift and drag coefficients. The SD8000's consistently lower drag is evident across the usable $C_L$ range.

![Drag polar for candidate airfoils at Re ≈ 60,000. The SD8000 exhibits consistently lower drag than the E387 across the operating range.](figures/airfoil_polar_en.png){#fig:airfoil-polar}

The lift curves in @fig:airfoil-cl-alpha show the stall characteristics of each airfoil. The SD8000's later stall angle (11.5° vs 10.2°) provides additional margin for safe operation.

![Lift coefficient vs angle of attack for candidate airfoils at Re ≈ 60,000.](figures/airfoil_cl_alpha_en.png){#fig:airfoil-cl-alpha}

### Selection rationale

Based on the comparative analysis, the Selig/Donovan SD8000 is selected for the Mars UAV wing design. While the E387 achieves marginally higher peak efficiency, the SD8000 offers important advantages for reliable Mars operation:

* Lower drag across operating range: $C_{D,\text{min}}$ = 0.0142, 38% lower than E387
* Larger stall margin: 4.6° margin between best L/D and stall, compared to only 1.3° for E387
* Consistent drag behaviour: no anomalous transitions or sensitivity to LSB dynamics
* Robust performance: higher L/D at practical cruise conditions ($C_L$ = 0.7–0.9)
* Designed for low Reynolds number: the SD8000 was specifically designed by Selig and Donovan for low-Re applications, with documented performance in UAV and similar applications [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:sd8000 -->
* Late stall: stall at α = 11.5° provides a wide operational envelope

The E387's peak efficiency advantage of 3% is offset by the operational risk of targeting an angle of attack within 1.3° of stall. For a Mars mission with no opportunity for recovery, the more conservative SD8000 selection provides appropriate safety margin.

### Design implications

The selected SD8000 airfoil establishes the following design values for the constraint analysis:

* Maximum lift coefficient: $C_{L,\text{max}}$ = 1.15 (from UIUC wind tunnel data)
* Airfoil $(L/D)_\text{max}$ = 45.4 at $C_L$ = 0.94
* Thickness ratio: $t/c$ = 0.089 (8.9%)
* Minimum drag coefficient: $C_{D,\text{min}}$ = 0.0142

These values are used in @sec:aerodynamic-analysis for the drag polar model and in the constraint analysis (@sec:hybrid-vtol-analysis) for stall speed calculations.

