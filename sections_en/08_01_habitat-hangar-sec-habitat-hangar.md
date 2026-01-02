# Infrastructure requirements

## Habitat hangar {#sec:habitat-hangar}

The UAV requires protected storage and maintenance facilities integrated with the Mars habitat. The hangar design accommodates the QuadPlane configuration specified in @sec:geometry-selection.

### UAV dimensional envelope

The hangar dimensions are driven by the UAV geometry derived in @sec:geometry-selection:

: UAV dimensional envelope for hangar sizing {#tbl:uav-envelope}

| Parameter | Symbol | Value | Source |
|:----------|:------:|------:|:-------|
| Wingspan | $b$ | 4.01 m | @tbl:wing-geometry |
| Fuselage length | $L_f$ | 1.20 m | @tbl:fuselage-geometry |
| Fuselage diameter | $D_f$ | 0.20 m | @tbl:fuselage-geometry |
| Height (with landing gear) | $H$ | 0.50 m | @tbl:fuselage-geometry |
| Boom extension aft | $\Delta L$ | 1.05 m | @tbl:total-length |
| Total aircraft length | $L_\text{total}$ | 2.25 m | @tbl:total-length |
| Lift propeller diameter | $D_p$ | 0.36 m | @sec:propeller-sizing |
| Cruise propeller diameter | $D_{p,c}$ | 0.31 m | @sec:propeller-sizing |

The UAV footprint for storage is 4.01 × 2.25 m (wingspan × total aircraft length). The lift rotors are mounted on wing booms within the wingspan envelope. The boom extension beyond the fuselage supports the V-tail surfaces and provides the required tail moment arm.

### Hangar zones

The hangar comprises three functional zones following standard Mars habitat airlock architecture.

#### Pressurised maintenance bay (storage zone)

The pressurised bay provides a shirtsleeve environment for maintenance and is sized to accommodate the full UAV wingspan plus work area:

: Pressurised bay specifications {#tbl:pressurised-bay}

| Parameter | Value | Notes |
|:----------|------:|:------|
| Interior dimensions | 6 × 5 × 3 m | Full wingspan (4.01 m) + 2 m margin × total length (2.25 m) + work area |
| Atmosphere | Habitat-equivalent | O₂/N₂ at approximately 70 kPa |
| Temperature | +15 to +25 °C | Battery-safe range |
| Lighting | 500 lux | Maintenance operations |

#### Airlock (transition zone)

The airlock enables pressure transitions and dust removal. The width matches the storage bay to accommodate the UAV without wing folding:

: Airlock specifications {#tbl:airlock-specs}

| Parameter | Value | Notes |
|:----------|------:|:------|
| Interior dimensions | 6 × 3 × 2.5 m | 6 m width accommodates full wingspan |
| Cycle time (depressurisation) | 5 min | To Mars ambient |
| Cycle time (repressurisation) | 5 min | To habitat pressure |
| Dust removal | Pressurised air jets | Compressed CO₂ from habitat reserves |

Dust removal is accomplished using pressurised air jets. As described in @sec:introduction, fine Martian regolith accumulates on exposed surfaces and degrades mechanical and optical components. The airlock employs an array of nozzles that direct high-velocity compressed gas (CO₂ from habitat atmospheric processing) across the UAV surfaces, dislodging particles before the vehicle enters the pressurised bay. This system is simpler and more reliable than electrostatic precipitators, requires no consumables beyond the compressed gas (which can be recycled), and has no moving parts exposed to the abrasive Martian dust.

#### External platform (launch/recovery zone)

The external platform provides a clear area for VTOL operations:

: External platform specifications {#tbl:platform-specs}

| Parameter | Value | Notes |
|:----------|------:|:------|
| Platform dimensions | 10 × 10 m | 2.5× wingspan clearance |
| Surface | Stabilised regolith | Dust-suppression coating |
| Landing markers | LED array | Low-power, cold-tolerant |

### Charging infrastructure

The charging system is sized based on the battery specifications from @sec:energy-storage:

The battery parameters are as follows: total battery capacity of 945 Wh, energy to replenish (20% to 100% charge) of 756 Wh, target charge time of 2–3 hours, charger power at 0.5C rate of 472 W, and charger power at 1C rate of 945 W.

A 1000 W charger is specified to allow rapid turnaround with margin.

### Solar power system

The solar power system provides energy for UAV charging independent of habitat power. This section presents the solar irradiance analysis, cell selection, panel sizing, and buffer battery dimensioning.

#### Mars solar irradiance

The solar energy available on Mars differs significantly from Earth due to orbital distance and atmospheric effects [@nasagoddardspaceflightcenterMarsFactSheet2024]<!-- #orbital -->:

: Mars solar irradiance parameters {#tbl:mars-irradiance}

| Parameter | Value | Notes |
|:----------|------:|:------|
| Solar constant at Mars orbit | 589 W/m² | 43% of Earth's 1361 W/m² |
| Perihelion irradiance | 717 W/m² | Closest approach to Sun |
| Aphelion irradiance | 493 W/m² | Farthest from Sun |
| Clear-sky surface irradiance (noon) | 500 W/m² | Atmospheric attenuation included |
| Design irradiance (aphelion + dust) | 350 W/m² | Sizing basis for panel area |
| Effective sunlight hours | 6 h/sol | Usable daylight for power generation |
| Average incidence factor | 0.7 | Cosine losses for fixed-tilt panels |


The panel sizing uses worst-case conditions (aphelion + typical dust loading, 350 W/m²) rather than optimistic clear-sky noon values (500 W/m²). This ensures the system can provide adequate charging throughout the Martian year, including during winter and periods of elevated atmospheric dust.

#### Solar cell selection

Space-grade triple-junction solar cells are evaluated for the habitat-integrated charging system. Three candidate technologies are compared:

: Solar cell technology comparison {#tbl:solar-cell-comparison}

| Technology | Efficiency (BOL) | Mass (mg/cm²) | Heritage |
|:-----------|:----------------:|:-------------:|:---------|
| SolAero IMM-α | 33.0% | 49 | Ingenuity Mars Helicopter |
| Spectrolab XTJ Prime | 30.7% | 50–84 | LEO/GEO satellites |
| Azur Space 3G30C | 30.0% | 86 | MER Spirit/Opportunity |

SolAero IMM-α [@solaerotechnologiesrocketlabSolAeroIMMalphaInverted2024]<!-- #specs -->: This inverted metamorphic multi-junction (IMM) cell achieves the highest efficiency at 33% BOL. At 49 mg/cm² (0.49 kg/m²), it is 42% lighter than conventional space-grade cells. The IMM-α has direct Mars heritage, powering the Ingenuity helicopter's solar panel through over 70 flights.

Spectrolab XTJ Prime [@spectrolabboeingSpectrolabXTJPrime2023]<!-- #specs -->: This triple-junction GaInP/GaAs/Ge cell achieves 30.7% average efficiency (31.9% maximum demonstrated). Mass ranges from 50–84 mg/cm² depending on thickness (80–225 μm). Qualified to AIAA-S111 and AIAA-S112 standards with extensive LEO and GEO flight heritage.

Azur Space 3G30C-Advanced [@azurspacesolarpowerAzurSpace3G30CAdvanced2023]<!-- #specs -->: This 30% efficiency InGaP/GaAs/Ge cell on germanium substrate has a mass of 86 mg/cm² at 150 μm thickness. Qualified to ECSS-E-ST-20-08C with heritage on the Mars Exploration Rovers Spirit and Opportunity.

SolAero IMM-α is selected based on its highest efficiency (33%) which maximises power per unit area, lowest mass per area (49 mg/cm² = 0.49 kg/m²), proven Mars heritage on Ingenuity helicopter, and tuning to the Mars spectrum for optimal performance.

#### Panel sizing

Panel sizing uses the conservative design irradiance (350 W/m², aphelion + typical dust) to ensure year-round operability.

Power output per unit area (at design irradiance):

$$P_\text{design} = \eta_\text{cell} \times I_\text{design} = 0.33 \times 350 = 115.5 \text{ W/m}^2$$

Daily energy yield:

$$E_\text{panel} = P_\text{design} \times t_\text{sun} \times \cos\theta_\text{avg} = 115.5 \times 6 \times 0.7 = 485.1 \text{ Wh/m}^2/\text{sol}$$

Energy requirement per charge cycle:

$$E_\text{charge} = \frac{756 \text{ Wh}}{0.90} = 840 \text{ Wh}$$ (including charger efficiency)

Minimum panel area:

$$A_\text{min} = \frac{E_\text{charge}}{E_\text{panel}} = \frac{840}{485.1} = 1.73 \text{ m}^2$$

Design margin (×1.5 for cell degradation and operational margin):

$$A_\text{design} = 1.73 \times 1.5 = 2.60 \text{ m}^2 \approx 3.0 \text{ m}^2$$

The panel area is rounded up to 3.0 m² to ensure the daily solar energy generation (1455 Wh) comfortably exceeds the buffer capacity requirement.

#### Buffer battery storage

The solar panel generates energy only during daylight hours, while UAV charging may be required at any time (including overnight turnaround or after evening missions). A buffer battery stores the solar energy for on-demand charging.

The buffer battery uses the same solid-state lithium-ion technology as the UAV battery (CGBT SLD1 series, 270 Wh/kg) rather than conventional Li-ion cells (180 Wh/kg). This decision provides logistics simplification (same battery chemistry means shared spares, charging equipment, and handling procedures), proven Mars compatibility (the CGBT solid-state battery was already selected for UAV operations based on its wide temperature range of -20 to +60°C), mass reduction (270 vs 180 Wh/kg reduces buffer mass by 33%), and operational flexibility (UAV battery packs can serve as buffer spares if needed, enabling battery rotation to even out cycle wear).

Buffer battery sizing:

: Buffer battery dimensioning {#tbl:buffer-battery}

| Parameter | Value | Calculation |
|:----------|------:|:------------|
| UAV battery capacity | 945 Wh | @sec:energy-storage |
| Energy per charge cycle | 756 Wh | 80% depth of discharge |
| Charger efficiency | 90% | |
| Energy required from buffer | 840 Wh | 756 / 0.90 |
| Night reserve factor | 1.5 | One overnight charge + margin |
| Buffer battery capacity | 1260 Wh | 840 × 1.5 |
| Buffer battery energy density | 270 Wh/kg | Same as UAV (solid-state Li-ion) |
| Buffer battery mass | 4.67 kg | 1260 / 270 |

The 1260 Wh buffer battery allows one complete UAV charge during nighttime or dust storm conditions when no solar input is available. The factor of 1.5 provides margin for battery degradation and system losses. During extended dust storms (weeks to months), charging falls back to habitat nuclear power.

During a typical sol the buffer charge/discharge cycle operates as follows: during daytime (6 h effective) solar panels generate 1455 Wh (3.0 m² × 485.1 Wh/m²); during buffer charging 1260 Wh is stored in the buffer battery; during UAV charging (2–3 h) 840 Wh is delivered to the UAV battery (756 Wh stored after losses); and excess energy of approximately 195 Wh is returned to the habitat grid.

: Solar power system specifications {#tbl:solar-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Cell technology | SolAero IMM-α | - |
| Cell efficiency | 33 | % |
| Panel area | 3.0 | m² |
| Peak power output | 346 | W |
| Daily energy yield | 1455 | Wh/sol |
| Panel mass | 1.47 | kg |
| Buffer battery capacity | 1260 | Wh |
| Buffer battery mass | 4.67 | kg |
| Buffer battery technology | Solid-state Li-ion (same as UAV) | - |
| Mounting | Habitat roof, fixed tilt | - |

### Summary

The hangar infrastructure enables one complete UAV charge cycle per sol under worst-case (aphelion + dust) conditions. The 3.0 m² solar array with 1260 Wh buffer battery provides energy independence for daily operations. The pressurised air jet system in the airlock removes Martian dust before the UAV enters the maintenance bay. The 6 m airlock width accommodates the full 4.01 m wingspan without requiring wing folding mechanisms. During dust storm conditions, charging falls back to habitat nuclear power or is deferred until conditions improve.

