# Reference data and trade-off analysis

## Commercial VTOL benchmarks {#sec:commercial-vtol}

Commercial hybrid VTOL drones provide additional design references. Although designed for Earth conditions, these systems demonstrate practical mass allocations, geometric proportions, and component selections that inform initial design hypotheses. The following table summarizes specifications from nine commercial QuadPlane-type VTOLs in the 8-32 kg MTOW range.

: Commercial VTOL UAV specifications {#tbl:reference-vtol}

| UAV | MTOW (kg) | Payload (kg) | Span (m) | Length (m) | Endurance (min) | $V_\text{cruise}$ (m/s) | Ref. |
|:----|----------:|-------------:|---------:|-----------:|----------------:|----------------:|:----:|
| UAVMODEL X2400 | 8.5 | 2.0 | 2.40 | 1.20 | 220 | 16 | [@uavmodelUAVMODELX2400VTOL2024]<!-- #specs --> |
| DeltaQuad Evo | 10.0 | 3.0 | 2.69 | 0.75 | 272 | 17 | [@deltaquadDeltaQuadEvoEnterprise2024]<!-- #specs --> |
| Elevon X Sierra | 13.5 | 1.5 | 3.00 | 1.58 | 150 | 20 | [@elevonxElevonXSierraVTOL2024]<!-- #specs --> |
| AirMobi V25 | 14.0 | 2.5 | 2.50 | 1.26 | 180 | 20 | [@airmobiAirmobiV25Full2024]<!-- #specs --> |
| JOUAV CW-15 | 14.5 | 3.0 | 3.54 | 2.06 | 180 | 17 | [@jouavJOUAVCW15Multipurpose2024]<!-- #specs --> |
| AirMobi V32 | 23.5 | 5.0 | 3.20 | 1.26 | 195 | 20 | [@airmobiAirmobiV32Full2024]<!-- #specs --> |
| RTV320 E | 24.0 | 2.5 | 3.20 | 2.00 | 180 | 21 | [@uavfordroneRTV320ElectricVTOL2024]<!-- #specs --> |
| V13-5 Sentinel | 26.5 | 7.5 | 3.50 | 1.88 | 160 | 44 | [@spideruavV135SentinelVTOL2024]<!-- #specs --> |
| JOUAV CW-25E | 31.6 | 6.0 | 4.35 | 2.18 | 210 | 20 | [@jouavJOUAVCW25ELong2024]<!-- #specs --> |

Several trends are evident from the reference data. Wing loading increases with MTOW: smaller UAVs (8-15 kg) have wingspans of 2.4-3.5 m, while larger UAVs (24-32 kg) reach 3.2-4.4 m, with wing loading ranging from 15-40 N/m² on Earth (corresponding to 6-15 N/m² under Mars gravity). Payload fraction ranges from 10-30% of MTOW across the designs, with typical payloads of 1.5-7.5 kg. Cruise speeds cluster around 17-21 m/s, as most designs optimize for endurance rather than speed, except high-speed surveillance platforms like the V13-5 Sentinel. Endurance exceeds 150 minutes for all designs; battery technology and efficient cruise enable mission times of 2.5-4.5 hours on Earth.
