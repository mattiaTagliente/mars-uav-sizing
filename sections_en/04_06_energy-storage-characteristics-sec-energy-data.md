# Reference data and trade-off analysis

## Energy storage characteristics {#sec:energy-data}

Battery technology selection is important for Mars UAV endurance. This section presents reference data from commercial platforms and derives the utilisation parameters needed for constraint analysis.

### Reference battery specifications {#sec:reference-battery-specs}

Battery capacity and technology vary across designs. Solid-state and semi-solid lithium-ion batteries are emerging for high-endurance applications, offering improved energy density and low-temperature performance.

: Reference UAV battery specifications {#tbl:reference-battery}

| UAV | Battery type | Capacity (mAh) | Mass (kg) | Spec. energy (Wh/kg) | Temp. range (°C) | Ref. |
|:----|:-------------|---------------:|----------:|---------------------:|-----------------:|:----:|
| UAVMODEL X2400 | LiPo 6S | 30000 | 2.5 | approximately 133 | N.A. | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | Semi-solid Li-ion | 44000 | 4.0 | approximately 180 | −20 to +45 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| AirMobi V25 | HV LiPo 6S ×2 | 50000 | 5.05 | approximately 150 | −20 to +45 | [@gensace/tattuTattu25000mAh228V2024] |
| RTV320 E | Solid-state Li-ion ×4 | 108000 | 9.36 | approximately 270 | −20 to +60 | [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025] |

The solid-state batteries used in the RTV320 E achieve 270 Wh/kg with extended temperature range, making them suitable for Mars applications where ambient temperatures reach −80°C.

### Battery utilisation parameters {#sec:battery-utilisation}

The usable energy from the battery is reduced by discharge efficiency and depth of discharge limitations. The discharge efficiency accounts for internal resistance losses during current draw:

$$E_\text{usable} = E_\text{total} \times DoD \times \eta_\text{batt}$$ {#eq:usable-energy}

where $E_\text{total}$ is the nominal battery capacity, $DoD$ is the depth of discharge, and $\eta_\text{batt}$ is the discharge efficiency.

For aircraft sizing, the available energy is conveniently expressed as a function of MTOW using the battery mass fraction:

$$E_\text{available} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$ {#eq:battery-energy-fraction}

where $f_\text{batt}$ is the battery mass fraction (from @sec:initial-mass-estimate) and $e_\text{spec}$ is the specific energy (Wh/kg). This equation is applied in the constraint analysis (@sec:constraint-analysis) to determine the available energy for each configuration.

A depth of discharge of $DoD$ = 0.80 is adopted to preserve battery cycle life. The discharge efficiency depends on the C-rate (discharge current relative to capacity). For the anticipated discharge currents during Mars UAV operation (approximately 3-5C during hover, 0.5-1C during cruise), solid-state lithium batteries achieve discharge efficiencies of 0.93-0.97 [@sadraeyDesignUnmannedAerial2020]. A value of $\eta_\text{batt}$ = 0.95 is adopted as representative of moderate discharge rates.
