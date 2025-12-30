# Reference data and trade-off analysis

## Payload systems {#sec:payload-systems}

The Mars UAV mission objectives, mapping and telecommunication relay, require payload systems capable of operating in the Martian environment while meeting stringent mass and power constraints. This section surveys existing camera systems suitable for aerial reconnaissance to establish realistic mass ranges and inform payload allocation in the initial weight estimate.

### Camera systems survey {#sec:camera-survey}

Camera payload selection involves trade-offs among resolution, sensor size, mass, and environmental tolerance. @Tbl:camera-survey summarizes specifications for representative systems across three categories: RGB mapping cameras, multispectral sensors, and thermal imagers.

: Camera systems specifications from manufacturer datasheets {#tbl:camera-survey}

| Model | Type | Sensor | Resolution | Mass (g) | Temp. range (°C) | Source |
|-------|------|--------|------------|----------|------------------|--------|
| DJI Zenmuse P1 | RGB | Full frame | 45 MP | 800-1350 | −20 to +50 | [@djiDJIZenmuseP12024] |
| Ricoh GR III | RGB | APS-C | 24 MP | 227-257 | N.A. | [@ricohimagingRicohGRIII2024] |
| Phase One iXM-100 | RGB | Medium format | 100 MP | 630-1170 | −10 to +40 | [@phaseonePhaseOneIXM1002024] |
| MicaSense RedEdge-MX | Multispectral | Custom (5 bands) | 1.2 MP/band | 232 | N.A. | [@micasenseMicaSenseRedEdgeMXIntegration2020] |
| DJI Zenmuse H20T | Thermal + RGB | Multiple | 640×512 (thermal) | 828 | −20 to +50 | [@djiDJIZenmuseH20T2024] |

Mass values represent body-only to complete system configurations. The DJI Zenmuse P1 ranges from 800 g (body) to 1350 g with the DL 35mm lens [@djiDJIZenmuseP12024]. The Ricoh GR III achieves 257 g including battery and storage [@ricohimagingRicohGRIII2024]. The Phase One iXM-100 body weighs 630 g, increasing to 1170 g with the RSM 35mm lens [@phaseonePhaseOneIXM1002024].

#### RGB mapping cameras

Full-frame sensors provide superior image quality for photogrammetry applications. The DJI Zenmuse P1 offers 45 MP resolution with 4.4 μm pixel pitch, achieving ground sample distance of 0.76 cm at 100 m altitude with the 35mm lens [@djiDJIZenmuseP12024]. Power consumption is approximately 20 W. The operating temperature range of −20 to +50 °C covers the warmer portion of Mars surface conditions.

Compact cameras offer mass advantages. The Ricoh GR III provides 24 MP APS-C imaging in a 227 g body with integrated 18.3 mm lens [@ricohimagingRicohGRIII2024]. However, the manufacturer does not specify operating temperature limits, indicating consumer-grade thermal tolerance inadequate for Mars conditions without thermal management.

The Phase One iXM-100 represents the high end of aerial mapping systems with 100 MP medium format (44×33 mm) sensor [@phaseonePhaseOneIXM1002024]. At 16 W maximum power consumption and 630 g body mass, it achieves 3.76 μm pixel pitch. The IP53 rating provides dust protection relevant to Mars operations, though the −10 to +40 °C operating range requires thermal control.

#### Multispectral cameras

The MicaSense RedEdge-MX provides five-band multispectral imaging (blue, green, red, red-edge, near-infrared) for scientific analysis [@micasenseMicaSenseRedEdgeMXIntegration2020]. At 232 g complete with the DLS 2 light sensor, it represents a lightweight option for geological survey applications. Each band provides 1.2 MP (1280×960 pixels) with global shutter and 12-bit output depth. Ground sample distance is 8 cm/pixel at 120 m altitude.

#### Thermal cameras

The DJI Zenmuse H20T integrates thermal, zoom, and wide-angle cameras with laser rangefinder in a single 828 g payload [@djiDJIZenmuseH20T2024]. The uncooled VOx microbolometer provides 640×512 thermal resolution with 50 mK noise-equivalent temperature difference. Temperature measurement ranges from −40 to +150 °C (high gain) or −40 to +550 °C (low gain), suitable for geological thermal mapping.

#### Mass and dimension summary

Based on the surveyed systems, camera payload characteristics are as follows. RGB cameras range from 227 g (body only, Ricoh GR III) to 1350 g (with lens, DJI Zenmuse P1). Multispectral sensors such as the MicaSense RedEdge-MX weigh approximately 232 g. Thermal/hybrid systems like the DJI Zenmuse H20T weigh approximately 828 g.

Camera dimensions vary with sensor format and lens configuration. The Ricoh GR III measures 109.4 × 61.9 × 33.2 mm (body only) [@ricohimagingRicohGRIII2024]. The DJI Zenmuse P1 measures 198 × 166 × 129 mm [@djiDJIZenmuseP12024]. The MicaSense RedEdge-MX measures 87 × 59 × 45.4 mm [@micasenseMicaSenseRedEdgeMXIntegration2020].

For initial sizing purposes, a compact RGB camera (250–400 g) represents the baseline payload allocation.

#### Mars thermal environment considerations

All surveyed cameras require thermal management for Mars operations. Mars surface temperatures range from approximately −60 to +20 °C, exceeding the lower operating limits of most commercial cameras. The DJI and Phase One systems with specified cold-weather ratings (−20 °C and −10 °C respectively) provide the best baseline thermal tolerance, though supplementary heating systems will be necessary during cold conditions. Cameras without specified temperature ranges require qualification testing or are assumed to need active thermal control.

Additional considerations for Mars camera systems include low atmospheric pressure (approximately 600 Pa) affecting thermal dissipation and requiring qualification testing, unknown radiation environment tolerance for commercial off-the-shelf components, and power budgets that must account for camera thermal control heating in addition to camera operation.

### Radio relay systems {#sec:radio-survey}

The telecommunication relay mission requires a radio system capable of extending communication range between surface EVA astronauts and the habitat ground station. For Mars operations, the specific frequency bands would differ from Earth usage due to regulatory and propagation differences, but mass and power specifications from commercial systems remain valid for feasibility estimation. This section surveys existing radio systems suitable for UAV relay applications across two categories: mesh radio systems and point-to-point data links.

#### Mesh radio systems

Mesh radios provide self-forming, self-healing network capability, though this functionality is not strictly required for a single UAV relay mission. @Tbl:radio-mesh summarizes specifications for representative mesh radio systems.

: Mesh radio system specifications from manufacturer datasheets {#tbl:radio-mesh}

| Model | Manufacturer | Mass (g) | Freq. range | Power (W) | Temp. range (°C) | Source |
|-------|--------------|----------|-------------|-----------|------------------|--------|
| StreamCaster 4200E+ | Silvus Technologies | 425 | 300 MHz-6 GHz | 5-48 | −40 to +85 | [@silvustechnologiesStreamCaster4200SC42002025] |
| MPU5 | Persistent Systems | 391-726 | Multiple bands | N.A. | −40 to +85 | [@persistentsystemsMPU5TechnicalSpecifications2025] |
| BreadCrumb ES1 | Rajant Corporation | 455 | 2.4/5 GHz | 2.8-15 | −40 to +60 | [@rajantcorporationBreadCrumbES1Specifications2025] |

The Silvus StreamCaster 4200E+ provides wideband 2×2 MIMO mesh capability in a 425 g package with IP68 rating and submersibility to 20 m [@silvustechnologiesStreamCaster4200SC42002025]. Power consumption ranges from 5 W at 1 W transmit power to 48 W at maximum 10 W transmit. The −40 to +85 °C operating temperature range exceeds Mars surface requirements.

The Persistent Systems MPU5 integrates a 1 GHz quad-core processor with 2 GB RAM for autonomous network management [@persistentsystemsMPU5TechnicalSpecifications2025]. At 391 g (chassis only) or 726 g with battery, it provides line-of-sight range up to 209 km between nodes. The MIL-STD-810G and MIL-STD-461F certifications indicate robust environmental tolerance.

The Rajant BreadCrumb ES1 offers dual-band operation (2.4 GHz and 5 GHz) with InstaMesh self-forming network capability in a 455 g unit [@rajantcorporationBreadCrumbES1Specifications2025]. Power consumption is 2.8 W idle to 15 W peak. The −40 to +60 °C temperature range covers Mars daytime surface conditions.

#### Point-to-point data links

For single UAV relay applications, lightweight point-to-point links provide superior mass efficiency. @Tbl:radio-p2p summarizes specifications for representative systems.

: Point-to-point data link specifications from manufacturer datasheets {#tbl:radio-p2p}

| Model | Manufacturer | Mass (g) | Freq. band | Data rate | Range (km) | Power (W) | Source |
|-------|--------------|----------|------------|-----------|------------|-----------|--------|
| RFD900x | RFDesign | 14.5 | 900 MHz | 0.064-0.75 Mbps | > 40 | 5 | [@rfdesignRFD900xModemSpecifications2024] |
| pMDDL2450 (OEM) | Microhard | 7 | 2.4 GHz | 12-25 Mbps | N.A. | N.A. | [@microhardPMDDL2450MiniatureMIMO2025] |
| pMDDL2450 (enclosed) | Microhard | 165 | 2.4 GHz | 12-25 Mbps | N.A. | N.A. | [@microhardPMDDL2450MiniatureMIMO2025] |

The RFD900x is an ultra-lightweight telemetry modem at 14.5 g, widely used in the UAV community with open-source SiK firmware [@rfdesignRFD900xModemSpecifications2024]. It provides > 40 km line-of-sight range with 1 W transmit power at 900 MHz. Data rate ranges from 64 kbps default to 750 kbps maximum, sufficient for telemetry and command links. The −40 to +85 °C operating temperature range extends beyond Mars surface requirements.

The Microhard pMDDL2450 offers higher bandwidth (25 Mbps throughput) for video relay applications in an extremely compact form factor [@microhardPMDDL2450MiniatureMIMO2025]. The OEM module weighs only 7 g, while the enclosed version with connectors weighs 165 g. The 2×2 MIMO configuration provides improved link reliability through spatial diversity.

#### Mass and dimension summary

Based on the surveyed systems, radio payload characteristics are as follows. Mesh radios range from 391 g (chassis only) to 726 g with integrated battery. Point-to-point links range from 7 g (OEM module) to 165 g (enclosed version).

Dimensions for the Microhard pMDDL2450 are: OEM module 27 × 33 × 4 mm, enclosed version 77 × 55 × 28 mm [@microhardPMDDL2450MiniatureMIMO2025].

For initial sizing purposes, a lightweight point-to-point link (15–170 g) represents the baseline radio payload allocation. Full mesh capability would add approximately 400–500 g if multi-asset coordination is required.

#### Mars environment considerations

All surveyed radio systems exceed the typical Mars surface temperature range of approximately −60 to +20 °C at the lower bounds, with specifications ranging from −40 to +60 °C (Rajant) to −40 to +85 °C (Silvus, Persistent, RFDesign). Additional considerations for Mars operations include low atmospheric pressure (approximately 600 Pa) affecting thermal dissipation with radios potentially requiring modified cooling strategies or derating, unknown radiation environment tolerance for commercial off-the-shelf components requiring qualification testing or radiation-hardened alternatives, frequency allocation for Mars surface communication differing from Earth regulatory bands requiring radio front-end modifications, and power budgets that must account for radio thermal control in addition to transmission power.
