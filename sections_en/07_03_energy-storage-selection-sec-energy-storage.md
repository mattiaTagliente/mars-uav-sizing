# Component selection and verification

## Energy storage selection {#sec:energy-storage}

The energy storage selection follows from the battery survey presented in @sec:energy-data. Selection criteria prioritize specific energy, low-temperature performance, and reliability for Mars conditions.

### Requirements from constraint analysis

The energy requirements are derived from the QuadPlane analysis in @sec:hybrid-vtol-analysis:

: Energy requirements from constraint analysis {#tbl:energy-requirements}

| Parameter | Value | Derivation |
|:----------|------:|:-----------|
| Available battery mass | 3.50 kg | $f_\text{batt}$ × MTOW = 0.35 × 10.00 |
| Required specific energy | ≥ 200 Wh/kg | Mission endurance margin |
| Total battery capacity | ≥ 700 Wh | 3.50 kg × 200 Wh/kg |
| Usable energy (80% DoD, 95% η) | ≥ 532 Wh | 700 × 0.80 × 0.95 |
| Operating temperature | −60 to +20 °C | Mars surface conditions |

### Candidate evaluation

@Tbl:battery-selection presents battery technologies evaluated against mission requirements, based on the survey data from @tbl:reference-battery.

: Battery technology selection trade-off analysis {#tbl:battery-selection}

| Technology | Spec. energy (Wh/kg) | Temp. range (°C) | Cycle life | Rating |
|:-----------|:--------------------:|:----------------:|:----------:|:------:|
| Solid-state Li-ion | 270 | −20 to +60 | 1000 | Selected |
| Semi-solid Li-ion | 180 | −20 to +45 | 500 | Alternative |
| LiPo (high voltage) | 150 | −20 to +45 | 300 | Rejected |
| Standard LiPo | 130-150 | 0 to +40 | 300 | Rejected |

### Selection rationale

**Solid-state lithium-ion batteries** are selected based on:

* **Specific energy**: 270 Wh/kg exceeds the 200 Wh/kg requirement by 35% [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025]<!-- #specs -->
* **Temperature range**: −20 to +60 °C provides baseline cold tolerance [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025]<!-- #specs -->
* **Cycle life**: 1000 cycles at 80% DoD supports long mission campaign
* **Safety**: solid electrolyte reduces thermal runaway risk in Mars habitat

The **semi-solid lithium-ion** technology is retained as an alternative if solid-state availability is limited. At 180 Wh/kg, it still meets mission requirements with reduced margin.

Standard LiPo batteries are rejected due to:

* Lower specific energy (130-150 Wh/kg)
* Narrower operating temperature (typically 0 to +40 °C without preheating)
* Shorter cycle life (approximately 300 cycles)

### Mars thermal considerations

The solid-state battery operating range (−20 to +60 °C) does not fully cover Mars surface temperatures (−60 to +20 °C). The battery thermal management strategy includes:

* Insulated battery compartment to reduce heat loss
* Resistive heating elements activated during cold soak periods
* Pre-flight battery conditioning in the habitat hangar
* Flight operations limited to daytime thermal window

The thermal control system mass is allocated within the avionics/systems mass fraction.

### Selected specification

: Selected battery specifications (solid-state Li-ion) {#tbl:battery-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Chemistry | Solid-state Li-ion | - |
| Reference model | CGBT SLD1-6S27Ah | - |
| Configuration | 6S (22.2V nominal) | - |
| Specific energy | 270 | Wh/kg |
| Battery mass | 3.50 | kg |
| Total capacity | 945 | Wh |
| Usable capacity (80% DoD, 95% η) | 718 | Wh |
| Operating temperature | −20 to +60 | °C |
| Cycle life (80% DoD) | 1000 | cycles |

### Energy budget verification

The selected battery provides 718 Wh of usable energy. From the QuadPlane analysis (@sec:hybrid-vtol-analysis), the mission energy requirement is:

$$E_\text{mission} = E_\text{hover} + E_\text{transition} + E_\text{cruise} = 106.0 + 10.0 + 302.0 = 418.0 \text{ Wh}$$

The energy margin is:

$$\text{Margin} = \frac{E_\text{available} - E_\text{mission}}{E_\text{mission}} = \frac{718 - 418.0}{418.0} = 71.8\%$$

After applying the 20% energy reserve:

$$E_\text{reserved} = 0.20 \times 718 = 143.6 \text{ Wh}$$
$$E_\text{net} = 718 - 143.6 = 574.4 \text{ Wh}$$

The net margin above mission requirement is:

$$\text{Net margin} = \frac{E_\text{net} - E_\text{mission}}{E_\text{mission}} = \frac{574.4 - 418.0}{418.0} = 37.4\%$$

This exceeds the minimum 20% reserve, confirming the battery selection meets mission requirements.

