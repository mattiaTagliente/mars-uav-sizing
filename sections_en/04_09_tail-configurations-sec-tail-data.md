# Reference data and trade-off analysis

## Tail configurations {#sec:tail-data}

QuadPlane UAVs use various empennage configurations, which can be categorized by mounting location: fuselage-mounted or boom-mounted. The lift rotor booms present in QuadPlane designs create opportunities for boom-mounted tail surfaces that may offer structural and aerodynamic advantages.

: Tail configuration categories for VTOL UAVs {#tbl:reference-tail-types}

| Configuration type | Description | Example UAVs |
|:-------------------|:------------|:-------------|
| Fuselage-mounted conventional | Horizontal + vertical stabilizers on fuselage | JOUAV CW-15 [@jouavJOUAVCW15Multipurpose2024] |
| Fuselage-mounted V-tail | Two surfaces in upward V arrangement | UAVMODEL X2400 [@uavmodelUAVMODELX2400VTOL2024] |
| Fuselage-mounted Y-tail | Inverted V with central vertical fin | V13-5 Sentinel [@spideruavV135SentinelVTOL2024] |
| Boom-mounted inverted V | Inverted V using lift motor booms | JOUAV CW-25E [@jouavJOUAVCW25ELong2024] |
| Boom-mounted inverted U | Inverted U empennage on booms | Event 38 E400 [@event38unmannedsystemsEvent38E4002024] |

Recent CFD analysis of VTOL-Plane empennage configurations compared U boom, inverted U boom, inverted V-tail boom, and semi-inverted V-tail boom arrangements [@nugrohoPerformanceAnalysisEmpennage2022]. The study found that the inverted U boom configuration provided favorable stall characteristics and flight efficiency for surveillance missions.

For Mars operations, tail configuration selection must consider the low Reynolds number environment (Re approximately 50,000 for tail surfaces), which affects control surface effectiveness. Additionally, boom-mounted configurations offer structural synergy with the lift motor support booms already required for QuadPlane VTOL capability.
