# Dati di riferimento e analisi dei compromessi

## Benchmark VTOL commerciali {#sec:commercial-vtol}

I droni VTOL ibridi commerciali forniscono ulteriori riferimenti di progettazione. Sebbene progettati per condizioni terrestri, questi sistemi dimostrano allocazioni di massa pratiche, proporzioni geometriche e selezioni di componenti che informano le ipotesi iniziali di progetto. La seguente tabella riassume le specifiche di nove VTOL commerciali di tipo QuadPlane nella gamma 8-32 kg MTOW.

: Specifiche UAV VTOL commerciali {#tbl:reference-vtol}

| UAV | MTOW (kg) | Payload (kg) | Apertura (m) | Lunghezza (m) | Autonomia (min) | $V_\text{cruise}$ (m/s) | Rif. |
|:----|----------:|-------------:|---------:|-----------:|----------------:|----------------:|:----:|
| UAVMODEL X2400 | 8.5 | 2.0 | 2.40 | 1.20 | 220 | 16 | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | 10.0 | 3.0 | 2.69 | 0.75 | 272 | 17 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| Elevon X Sierra | 13.5 | 1.5 | 3.00 | 1.58 | 150 | 20 | [@elevonxElevonXSierraVTOL2024] |
| AirMobi V25 | 14.0 | 2.5 | 2.50 | 1.26 | 180 | 20 | [@airmobiAirmobiV25Full2024] |
| JOUAV CW-15 | 14.5 | 3.0 | 3.54 | 2.06 | 180 | 17 | [@jouavJOUAVCW15Multipurpose2024] |
| AirMobi V32 | 23.5 | 5.0 | 3.20 | 1.26 | 195 | 20 | [@airmobiAirmobiV32Full2024] |
| RTV320 E | 24.0 | 2.5 | 3.20 | 2.00 | 180 | 21 | [@uavfordroneRTV320ElectricVTOL2024] |
| V13-5 Sentinel | 26.5 | 7.5 | 3.50 | 1.88 | 160 | 44 | [@spideruavV135SentinelVTOL2024] |
| JOUAV CW-25E | 31.6 | 6.0 | 4.35 | 2.18 | 210 | 20 | [@jouavJOUAVCW25ELong2024] |

Diverse tendenze sono evidenti dai dati di riferimento. Il carico alare aumenta con l'MTOW: gli UAV più piccoli (8-15 kg) hanno aperture alari di 2.4-3.5 m, mentre gli UAV più grandi (24-32 kg) raggiungono 3.2-4.4 m, con carico alare che varia da 15-40 N/m² sulla Terra (corrispondente a 6-15 N/m² con gravità marziana). La frazione di payload varia dal 10-30% dell'MTOW tra i progetti, con payload tipici di 1.5-7.5 kg. Le velocità di crociera si aggirano attorno ai 17-21 m/s, poiché la maggior parte dei progetti ottimizza per l'autonomia piuttosto che per la velocità, eccetto piattaforme di sorveglianza ad alta velocità come il V13-5 Sentinel. L'autonomia supera i 150 minuti per tutti i progetti; la tecnologia delle batterie e la crociera efficiente consentono tempi di missione di 2.5-4.5 ore sulla Terra.
