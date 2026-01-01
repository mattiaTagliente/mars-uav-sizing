# Design decisions

## Geometry selection {#sec:geometry-selection}

This section presents the geometric parameter selections for the Mars UAV, consolidating the tail and fuselage configuration decisions with wing geometry specifications.

### Wing geometry

Wing geometry follows directly from the constraint analysis results (@sec:comparative-results):

| Parameter | Value | Source |
|:----------|------:|:-------|
| Wing loading, $W/S$ | 13.82 N/m² | Stall constraint at $V_\text{min}$ = 35.04 m/s |
| Wing area, $S$ | 2.686 m² | $S = W/(W/S)$ at 10 kg MTOW |
| Wingspan, $b$ | 4.01 m | $b = \sqrt{AR \times S}$ at AR = 6 |
| Mean aerodynamic chord, $MAC$ | 0.669 m | $MAC = S/b$ |
| Aspect ratio, $AR$ | 6 | Selected from trade-off analysis |
| Taper ratio, $\lambda$ | 0.5 | @sec:derived-requirements |
| Sweep angle, $\Lambda$ | 0° | @sec:derived-requirements |

: Wing geometry parameters {#tbl:wing-geometry}

The aspect ratio of 6 represents a compromise between aerodynamic efficiency (higher AR increases L/D) and structural weight (higher AR increases wing bending loads). The untapered, unswept configuration minimises manufacturing complexity and tip stall risk at low Reynolds numbers.

### Tail configuration selection

Based on the trade-off analysis in @sec:tail-data, a boom-mounted inverted V-tail configuration is selected. This choice leverages the structural booms already required for the octocopter lift motors.

The rear lift motor booms extend aft to support the tail surfaces, eliminating the need for a separate tail boom structure and reducing overall structural mass. The boom-mounted configuration provides a longer moment arm than a fuselage-mounted tail would allow with the compact fuselage selected for this design, compensating for the reduced control effectiveness at Mars Reynolds numbers. The inverted V geometry angles the surfaces upward from the fuselage centerline, providing clearance from the surface during landing on uneven terrain. The V-tail surfaces are positioned outside the cruise propeller slipstream (bow-mounted tractor configuration), ensuring undisturbed airflow over the control surfaces.

The inverted V arrangement combines pitch and yaw control in two surfaces with ruddervator-style mixing. CFD studies of boom-mounted empennage configurations found that inverted U boom designs provided superior longitudinal stability and stall characteristics for surveillance missions [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:inverted-u -->, and the two-surface design reduces parts count compared to a three-surface conventional tail.

#### Tail sizing

Tail surface sizing for Mars conditions requires careful consideration of Reynolds number effects. At Mars atmospheric density, the tail surfaces operate at Reynolds numbers significantly lower than Earth equivalents, reducing control surface effectiveness. Following the volume coefficient method [@roskamAirplaneDesign22004]<!-- #s8.1 -->, the horizontal and vertical tail areas are determined from:

$$\bar{V}_H = \frac{x_H \cdot S_H}{S \cdot \bar{c}}$$ {#eq:vh-coeff}

$$\bar{V}_V = \frac{x_V \cdot S_V}{S \cdot b}$$ {#eq:vv-coeff}

where $\bar{V}_H$ and $\bar{V}_V$ are the horizontal and vertical tail volume coefficients, $x_H$ and $x_V$ are the moment arms, $S$ is the wing area, $\bar{c}$ is the mean aerodynamic chord, and $b$ is the wingspan [@roskamAirplaneDesign22004]<!-- #eq8.1-8.2 -->. Solving for tail areas:

$$S_H = \frac{\bar{V}_H \cdot S \cdot \bar{c}}{x_H}$$ {#eq:vtail-vh}

$$S_V = \frac{\bar{V}_V \cdot S \cdot b}{x_V}$$ {#eq:vtail-vv}

For a butterfly (V-tail) configuration, the effective horizontal and vertical areas are projections of the total V-tail planform area onto the reference planes [@roskamAirplaneDesign22004]<!-- #eq8.5 -->:

$$S_{H,\text{eff}} = S_{V\text{-tail}} \cos^2 \Gamma, \quad S_{V,\text{eff}} = S_{V\text{-tail}} \sin^2 \Gamma$$ {#eq:vtail-area}

The butterfly dihedral angle follows from:

$$\Gamma = \arctan\left(\sqrt{\frac{S_V}{S_H}}\right)$$ {#eq:butterfly-angle}

The target volume coefficients are increased by 25% over typical values to compensate for reduced control effectiveness at Mars Reynolds numbers, giving $\bar{V}_H$ = 0.45 and $\bar{V}_V$ = 0.035. With a tail moment arm of $x_H$ = 1.20 m (provided by the boom extension aft of the fuselage), the required areas are:

| Parameter | Value | Notes |
|:----------|------:|:------|
| V-tail dihedral, $\Gamma$ | 40° | Balances pitch/yaw authority |
| V-tail total area, $S_{V\text{-tail}}$ | 1.144 m² | Pitch-constrained |
| V-tail span, $b_{V\text{-tail}}$ | 2.14 m | At AR = 4.0 |
| V-tail mean chord, $c_{V\text{-tail}}$ | 0.535 m | $S/b$ |
| Tail-to-wing area ratio | 42.6% | Higher than Earth due to low Re |
| Tail moment arm, $l_H$ | 1.20 m | Boom extension aft of fuselage |

: V-tail geometry parameters {#tbl:vtail-geometry}

The horizontal (pitch) constraint is active, meaning the tail is sized primarily for adequate pitch stability. The vertical (yaw) component at 40° dihedral exceeds requirements by 51%, providing adequate directional stability and control authority for crosswind operations.

### Fuselage geometry selection

The commercial benchmarks exhibit a length-to-wingspan ratio ranging from 0.28 to 0.63, with a median of approximately 0.50 (@tbl:reference-fuselage). The selection involves trade-offs between competing effects:

**Shorter fuselage (lower ratio):**

* Less fuselage structural mass
* Less fuselage wetted area (reduced parasitic drag)
* Shorter tail moment arm requiring boom extension
* Less internal volume

**Longer fuselage (higher ratio):**

* More fuselage lift contribution
* Longer tail moment arm allowing smaller tail surfaces
* More internal volume for payload growth and thermal management
* More fuselage structural mass
* More fuselage wetted area

**Selection: 0.30** (lower end of benchmark range)

For the Mars UAV, most of the internal volume is occupied by the compact payload and energy storage systems requiring only 4–5 L. The 170 L volume provided by the 0.50 ratio is excessive. Selecting the lower end of the benchmark range (0.30) minimises structural mass and parasitic drag while providing adequate volume for all systems. The required tail moment arm is instead achieved through the boom extension, which is structurally efficient since it serves the dual purpose of supporting both the lift rotors and the V-tail surfaces.

The resulting fuselage dimensions are:

$$L_f = 0.30 \times b = 0.30 \times 4.01 = 1.20 \text{ m}$$

With fineness ratio 6 and circular cross-section:

$$D_f = \frac{L_f}{FR} = \frac{1.20}{6} = 0.20 \text{ m}$$

$$V_f = \frac{\pi}{4} D_f^2 \times L_f = \frac{\pi}{4} \times 0.20^2 \times 1.20 = 0.038 \text{ m}^3 = 38 \text{ L}$$

The payload and systems require approximately 4–5 L of internal volume, providing adequate margin for thermal management systems, cable routing, and future payload growth within the 38 L available.

#### Fuselage dimensions

The following values are derived from the selected length-to-wingspan ratio and fineness ratio constraint:

| Parameter | Symbol | Value | Notes |
|:----------|:------:|------:|:------|
| Fuselage length | $L_f$ | 1.20 m | 0.30 × 4.01 m (lower benchmark) |
| Maximum diameter | $D_f$ | 0.20 m | $L_f$/6 (fineness ratio 6) |
| Fineness ratio | $L_f/D_f$ | 6 | Low-drag profile [@gottenFullConfigurationDrag2021]<!-- #s:fineness --> |
| Length-to-wingspan ratio | $L_f/b$ | 0.30 | Lower benchmark (minimal volume needed) |
| Internal volume | $V_f$ | 38 L | $\pi/4 \times D_f^2 \times L_f$ |
| Height (with landing gear) | $H$ | 0.50 m | Ground clearance for propellers |

: Fuselage geometry parameters {#tbl:fuselage-geometry}

The fuselage cross-section is approximately circular to simplify structural analysis and manufacturing. Payload integration and detailed internal arrangement are addressed in @sec:component-verification.

#### Total aircraft length {#sec:total-aircraft-length}

The boom-mounted V-tail configuration extends beyond the fuselage aft end. The total aircraft length is determined by the tail position required to achieve the target moment arm:

**Wing position:**

$$x_\text{wing,LE} = 0.40 \times L_f = 0.40 \times 1.20 = 0.48 \text{ m from nose}$$

$$x_\text{wing,AC} = x_\text{wing,LE} + 0.25 \times MAC = 0.48 + 0.25 \times 0.669 = 0.65 \text{ m}$$

**Tail position (from wing AC + moment arm):**

$$x_\text{tail,AC} = x_\text{wing,AC} + l_H = 0.65 + 1.20 = 1.85 \text{ m from nose}$$

**Tail trailing edge (AC at 25% chord from LE):**

$$x_\text{tail,TE} = x_\text{tail,AC} + 0.75 \times c_{V\text{-tail}} = 1.85 + 0.75 \times 0.535 = 2.25 \text{ m}$$

The total aircraft length is therefore **2.25 m**, with the tail booms extending **1.05 m** beyond the fuselage aft end. This boom extension is structurally integrated with the rear lift motor arms, which serve the dual purpose of supporting the octocopter rotors and the V-tail surfaces.

| Parameter | Symbol | Value | Notes |
|:----------|:------:|------:|:------|
| Fuselage length | $L_f$ | 1.20 m | Payload bay and systems |
| Boom extension aft | $\Delta L$ | 1.05 m | Tail support structure |
| Total aircraft length | $L_\text{total}$ | 2.25 m | Nose to tail trailing edge |

: Total aircraft length breakdown {#tbl:total-length}

### Propeller sizing {#sec:propeller-sizing}

The QuadPlane configuration requires two propeller types: lift propellers for the octocopter VTOL system and cruise propellers for forward flight. Both are sized using momentum theory [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #ch2 --> with Mach number constraints to prevent compressibility losses at the blade tips.

#### Lift propeller sizing

The eight lift motors must generate sufficient thrust for hover. From momentum theory, disk loading $DL$ is defined as thrust per unit disk area [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #eq2.13 -->:

$$DL = \frac{T}{A} = \frac{T}{\pi D_p^2 / 4}$$ {#eq:disk-loading}

Solving for propeller diameter:

$$D_p = \sqrt{\frac{4T}{\pi \cdot DL}}$$ {#eq:lift-prop-dia}

With the design disk loading of 30.0 N/m² from @sec:derived-requirements and hover thrust requirement of MTOW / 8 = 4.64 N per motor:

$$D_p = \sqrt{\frac{4 \times 4.64}{\pi \times 30.0}} = 0.44 \text{ m}$$

The tip Mach number is verified against the Mars speed of sound (229.7 m/s at 210 K). Propeller efficiency degrades when tip Mach exceeds approximately 0.7 due to compressibility effects [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #s:compressibility -->:

$$M_\text{tip} = \frac{\pi n D_p}{a}$$ {#eq:tip-mach}

where $n$ is the rotational speed (rev/s) and $a$ is the speed of sound. Using a 70% margin to the Mach limit gives 4850 rpm with a 0.44 m diameter:

$$M_\text{tip} = \frac{\pi \times (4850/60) \times 0.44}{229.7} = 0.49$$

This is below the 0.7 limit, so no tip speed constraint applies. The theoretical diameter from disk loading is 0.44 m. The selected lift propeller diameter is **0.36 m** (14 inches), based on available propeller sizes and motor compatibility.

#### Cruise propeller sizing

The two cruise motors provide forward thrust during horizontal flight. From actuator disk theory [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #ch2 -->, the induced power is:

$$P_\text{induced} = T v_i = \frac{T^{3/2}}{\sqrt{2 \rho A}}$$ {#eq:induced-power}

Cruise thrust is set by the aerodynamic drag requirement, $T = W/(L/D)$. For the baseline configuration, the total cruise thrust is 3.53 N (1.76 N per motor). The selected cruise propeller diameter is **0.31 m** (12 inches). At 8000 rpm, the tip Mach is 0.56, below the 0.7 limit.

| Parameter | Lift propeller | Cruise propeller |
|:----------|---------------:|-----------------:|
| Diameter | 0.36 m | 0.31 m |
| Quantity | 8 | 2 |
| Blade count | 2 | 2 |
| Operating speed | 4850 rpm | 8000 rpm |
| Tip Mach number | 0.49 | 0.56 |

: Propeller geometry summary {#tbl:propeller-summary}

