# Reference data and trade-off analysis

## Fuselage geometry {#sec:fuselage-data}

Fuselage dimensions affect payload volume, drag, and stability. The length-to-wingspan ratio ($l/b$) characterizes fuselage compactness, with lower values indicating shorter fuselages relative to wingspan. The following table summarizes fuselage geometry from the commercial benchmarks.

: Commercial VTOL UAV fuselage geometry {#tbl:reference-fuselage}

| UAV | Wingspan (m) | Length (m) | $l/b$ | Ref. |
|:----|-------------:|-----------:|------:|:----:|
| UAVMODEL X2400 | 2.40 | 1.20 | 0.50 | [@uavmodelUAVMODELX2400VTOL2024]<!-- #geom --> |
| DeltaQuad Evo | 2.69 | 0.75 | 0.28 | [@deltaquadDeltaQuadEvoEnterprise2024]<!-- #geom --> |
| Elevon X Sierra | 3.00 | 1.58 | 0.53 | [@elevonxElevonXSierraVTOL2024]<!-- #geom --> |
| AirMobi V25 | 2.50 | 1.26 | 0.50 | [@airmobiAirmobiV25Full2024]<!-- #geom --> |
| JOUAV CW-15 | 3.54 | 2.06 | 0.58 | [@jouavJOUAVCW15Multipurpose2024]<!-- #geom --> |
| AirMobi V32 | 3.20 | 1.26 | 0.39 | [@airmobiAirmobiV32Full2024]<!-- #geom --> |
| RTV320 E | 3.20 | 2.00 | 0.63 | [@uavfordroneRTV320ElectricVTOL2024]<!-- #geom --> |
| V13-5 Sentinel | 3.50 | 1.88 | 0.54 | [@spideruavV135SentinelVTOL2024]<!-- #geom --> |
| JOUAV CW-25E | 4.35 | 2.18 | 0.50 | [@jouavJOUAVCW25ELong2024]<!-- #geom --> |

The length-to-wingspan ratio ranges from 0.28 (DeltaQuad Evo, flying wing configuration) to 0.63 (RTV320 E), with a median of approximately 0.50. This ratio influences both parasitic drag and longitudinal stability. Parasitic drag estimation for fixed-wing UAVs requires careful attention to fuselage and miscellaneous component contributions, which can account for nearly half of total parasitic drag [@gottenFullConfigurationDrag2021]<!-- #s:drag -->.
