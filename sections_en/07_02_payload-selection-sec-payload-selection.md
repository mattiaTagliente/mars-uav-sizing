# Component selection and verification

## Payload selection {#sec:payload-selection}

The payload selection follows from the survey of camera and radio systems presented in @sec:payload-systems. Selection criteria prioritize mass efficiency, environmental tolerance for Mars conditions, and mission capability.

### Camera selection {#sec:camera-selection}

#### Requirements

The mapping mission requires a camera capable of high-resolution imaging from cruise altitude (approximately 100 m AGL). Based on the mass budget from @tbl:design-mass-fractions, the total payload allocation is:

$$m_\text{payload} = f_\text{payload} \times MTOW = 0.10 \times 10.00 = 1.00 \text{ kg}$$

Allocating approximately 60% to the camera and 40% to the radio system yields a camera mass target of approximately 600 g.

#### Candidate evaluation

@Tbl:camera-selection presents the camera candidates from @sec:camera-survey, evaluated against mission requirements.

: Camera selection trade-off analysis {#tbl:camera-selection}

| Camera | Mass (g) | Resolution | Temp. range (°C) | Rating |
|:-------|:--------:|:-----------|:----------------:|:------:|
| Ricoh GR III | 227-257 | 24 MP (APS-C) | N.A. | Selected |
| MicaSense RedEdge-MX | 232 | 1.2 MP/band (5 bands) | N.A. | Alternative |
| DJI Zenmuse P1 | 800-1350 | 45 MP (Full frame) | −20 to +50 | Backup |
| Phase One iXM-100 | 630-1170 | 100 MP (Medium format) | −10 to +40 | Rejected |
| DJI Zenmuse H20T | 828 | 640×512 (thermal) | −20 to +50 | Rejected |

Note: N.A. indicates operating temperature not specified by manufacturer.

#### Selection rationale

The **Ricoh GR III** is selected as the primary camera based on:

* **Mass**: 227 g body, 257 g complete with battery [@ricohimagingRicohGRIII2024]<!-- #specs -->, the lightest RGB option
* **Resolution**: 24 MP APS-C sensor provides adequate resolution for mapping
* **Dimensions**: 109.4 × 61.9 × 33.2 mm compact form factor [@ricohimagingRicohGRIII2024]<!-- #specs -->
* **Lens**: Integrated 18.3 mm lens (28 mm equivalent) eliminates interchangeable lens complexity

The **MicaSense RedEdge-MX** is retained as an alternative if multispectral capability is required for geological analysis [@micasenseMicaSenseRedEdgeMXIntegration2020]<!-- #specs -->. At 232 g, it provides five-band imaging (blue, green, red, red-edge, NIR) suitable for mineral identification.

The DJI Zenmuse P1 and Phase One iXM-100 are rejected due to mass exceeding the 600 g target by a factor of two or more. The DJI Zenmuse H20T thermal system is rejected as thermal imaging is not a primary mission requirement.

#### Thermal management requirement

The Ricoh GR III does not specify an operating temperature range, indicating consumer-grade thermal tolerance [@ricohimagingRicohGRIII2024]<!-- #specs -->. Mars surface temperatures range from approximately −60 to +20 °C, requiring active thermal management to maintain the camera within operational limits. The thermal control system mass is allocated within the avionics mass fraction.

#### Selected specification

: Selected camera specifications (Ricoh GR III) {#tbl:camera-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Model | Ricoh GR III | - |
| Mass (body) | 227 | g |
| Mass (with battery, SD card) | 257 | g |
| Sensor | APS-C CMOS | - |
| Resolution | 24.24 | MP |
| Image dimensions | 6000 × 4000 | pixels |
| Lens focal length | 18.3 | mm |
| Lens aperture | f/2.8-f/16 | - |
| Dimensions | 109.4 × 61.9 × 33.2 | mm |

### Radio selection {#sec:radio-selection}

#### Requirements

The telecommunication relay mission requires a radio system capable of extending communication range between surface EVA astronauts and the habitat ground station. Based on the 40% radio allocation from the 1.00 kg payload budget, the radio mass target is approximately 400 g.

Operating requirements include:

* Range: match or exceed the 50 km operational radius
* Temperature: operation at Mars surface temperatures (−60 to +20 °C)
* Power: minimise power consumption for battery endurance

#### Candidate evaluation

@Tbl:radio-selection presents the radio candidates from @sec:radio-survey, evaluated against mission requirements.

: Radio selection trade-off analysis {#tbl:radio-selection}

| Radio | Mass (g) | Range (km) | Temp. range (°C) | Rating |
|:------|:--------:|:----------:|:----------------:|:------:|
| RFD900x | 14.5 | > 40 | −40 to +85 | Selected |
| Microhard pMDDL2450 (enclosed) | 165 | N.A. | −40 to +85 | Alternative |
| Rajant BreadCrumb ES1 | 455 | N.A. | −40 to +60 | Rejected |
| Silvus StreamCaster 4200E+ | 425 | N.A. | −40 to +85 | Rejected |
| Persistent Systems MPU5 | 391-726 | 209 | −40 to +85 | Rejected |

#### Selection rationale

The **RFD900x** is selected as the primary radio based on:

* **Mass**: 14.5 g is the lightest option, well under the 400 g target [@rfdesignRFD900xModemSpecifications2024]<!-- #specs -->
* **Range**: >40 km line-of-sight range meets the 50 km operational radius with antenna optimisation [@rfdesignRFD900xModemSpecifications2024]<!-- #specs -->
* **Temperature**: −40 to +85 °C operating range exceeds Mars surface requirements
* **Power**: 5 W maximum power consumption at 1 W transmit
* **Heritage**: widely used in UAV applications with open-source SiK firmware

The **Microhard pMDDL2450** is retained as an alternative if higher data throughput is required (25 Mbps vs 0.75 Mbps) for potential video relay applications [@microhardPMDDL2450MiniatureMIMO2025]<!-- #specs -->.

The mesh radio systems (Rajant, Silvus, Persistent Systems) are rejected as mesh functionality is not required for a single UAV relay mission. Their mass of 400-700 g would consume the entire radio budget with no advantage for the mission profile.

#### Selected specification

: Selected radio specifications (RFD900x) {#tbl:radio-spec}

| Parameter | Value | Unit |
|:----------|------:|:-----|
| Model | RFD900x | - |
| Mass | 14.5 | g |
| Frequency | 902-928 | MHz |
| Output power | 1 (max 30 dBm) | W |
| Data rate | 64-750 | kbps |
| Range (LOS) | > 40 | km |
| Power consumption | 5 | W |
| Operating temperature | −40 to +85 | °C |
| Dimensions | 30 × 57 × 12.8 | mm |

### Payload mass summary

@Tbl:payload-summary presents the complete payload mass breakdown with selected components.

: Payload mass summary with selected components {#tbl:payload-summary}

| Component | Model | Qty | Unit (g) | Total (kg) |
|:----------|:------|:---:|:--------:|:----------:|
| Camera | Ricoh GR III | 1 | 257 | 0.257 |
| Radio | RFD900x | 1 | 14.5 | 0.015 |
| Radio antenna | Dipole (est.) | 2 | 25 | 0.050 |
| Camera mount | Custom (est.) | 1 | 50 | 0.050 |
| Cabling, connectors | - | 1 | 50 | 0.050 |
| **Total payload** | - | - | - | **0.422** |

The selected components yield a total payload mass of **0.42 kg**, well within the 1.00 kg budget allocated by the payload fraction $f_\text{payload}$ = 0.10.

$$f_\text{payload,actual} = \frac{m_\text{payload}}{MTOW} = \frac{0.422}{10.00} = 0.042 = 4.2\%$$

This represents a **58% reduction** from the allocated budget, providing margin for:

* Additional payload if mission requirements expand
* Thermal management components for Mars operation
* Design iteration flexibility

The payload mass reduction reallocates 0.58 kg to other system categories, potentially increasing battery capacity for extended endurance.

