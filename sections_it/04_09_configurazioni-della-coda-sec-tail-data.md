# Dati di riferimento e analisi dei compromessi

## Configurazioni della coda {#sec:tail-data}

Gli UAV QuadPlane utilizzano varie configurazioni di impennaggio, che possono essere categorizzate per posizione di montaggio: montate sulla fusoliera o montate sui bracci. I bracci dei rotori di sollevamento presenti nei design QuadPlane creano opportunità per superfici di coda montate sui bracci che possono offrire vantaggi strutturali e aerodinamici.

: Categorie di configurazione della coda per UAV VTOL {#tbl:reference-tail-types}

| Tipo di configurazione | Descrizione | UAV di esempio |
|:-------------------|:------------|:-------------|
| Convenzionale montata sulla fusoliera | Stabilizzatori orizzontale + verticale sulla fusoliera | JOUAV CW-15 [@jouavJOUAVCW15Multipurpose2024]<!-- #tail --> |
| V-tail montata sulla fusoliera | Due superfici in disposizione a V verso l'alto | UAVMODEL X2400 [@uavmodelUAVMODELX2400VTOL2024]<!-- #tail --> |
| Y-tail montata sulla fusoliera | V invertita con pinna verticale centrale | V13-5 Sentinel [@spideruavV135SentinelVTOL2024]<!-- #tail --> |
| V invertita montata sui bracci | V invertita utilizzando i bracci dei motori di sollevamento | JOUAV CW-25E [@jouavJOUAVCW25ELong2024]<!-- #tail --> |
| U invertita montata sui bracci | Impennaggio a U invertita sui bracci | Event 38 E400 [@event38unmannedsystemsEvent38E4002024]<!-- #tail --> |

Una recente analisi CFD delle configurazioni di impennaggio VTOL-Plane ha confrontato le disposizioni U sui bracci, U invertita sui bracci, V-tail invertita sui bracci e semi-V-tail invertita sui bracci [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:comparison -->. Lo studio ha rilevato che la configurazione a U invertita sui bracci forniva caratteristiche di stallo favorevoli ed efficienza di volo per missioni di sorveglianza.

Per le operazioni marziane, la selezione della configurazione della coda deve considerare l'ambiente a basso numero di Reynolds (Re circa 50,000 per le superfici di coda), che influenza l'efficacia delle superfici di controllo. Inoltre, le configurazioni montate sui bracci offrono sinergia strutturale con i bracci di supporto dei motori di sollevamento già richiesti per la capacità VTOL QuadPlane.
