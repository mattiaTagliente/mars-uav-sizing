# Dati di riferimento e analisi dei compromessi

## Geometria della fusoliera {#sec:fuselage-data}

Le dimensioni della fusoliera influenzano il volume del payload, la resistenza e la stabilità. Il rapporto lunghezza/apertura alare ($l/b$) caratterizza la compattezza della fusoliera, con valori più bassi che indicano fusoliere più corte rispetto all'apertura alare. La seguente tabella riassume la geometria della fusoliera dai benchmark commerciali.

: Geometria della fusoliera degli UAV VTOL commerciali {#tbl:reference-fuselage}

| UAV | Apertura (m) | Lunghezza (m) | $l/b$ | Rif. |
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

Il rapporto lunghezza/apertura alare varia da 0.28 (DeltaQuad Evo, configurazione ad ala volante) a 0.63 (RTV320 E), con una mediana di circa 0.50. Questo rapporto influenza sia la resistenza parassita che la stabilità longitudinale. La stima della resistenza parassita per UAV ad ala fissa richiede particolare attenzione ai contributi della fusoliera e dei componenti vari, che possono rappresentare quasi la metà della resistenza parassita totale [@gottenFullConfigurationDrag2021]<!-- #s:drag -->.
