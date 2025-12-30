# Dati di riferimento e analisi dei compromessi

## Caratteristiche di accumulo energetico {#sec:energy-data}

La selezione della tecnologia delle batterie è importante per l'autonomia dell'UAV marziano. Questa sezione presenta i dati di riferimento da piattaforme commerciali e deriva i parametri di utilizzo necessari per l'analisi dei vincoli.

### Specifiche batterie di riferimento {#sec:reference-battery-specs}

La capacità e la tecnologia delle batterie variano tra i progetti. Le batterie al litio-ione allo stato solido e semi-solido stanno emergendo per applicazioni ad alta autonomia, offrendo migliore densità energetica e prestazioni a basse temperature.

: Specifiche batterie UAV di riferimento {#tbl:reference-battery}

| UAV | Tipo batteria | Capacità (mAh) | Massa (kg) | Energia spec. (Wh/kg) | Range temp. (°C) | Rif. |
|:----|:-------------|---------------:|----------:|---------------------:|-----------------:|:----:|
| UAVMODEL X2400 | LiPo 6S | 30000 | 2.5 | circa 133 | N.D. | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | Li-ion semi-solido | 44000 | 4.0 | circa 180 | −20 a +45 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| AirMobi V25 | HV LiPo 6S ×2 | 50000 | 5.05 | circa 150 | −20 a +45 | [@gensace/tattuTattu25000mAh228V2024] |
| RTV320 E | Li-ion stato solido ×4 | 108000 | 9.36 | circa 270 | −20 a +60 | [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025] |

Le batterie allo stato solido utilizzate nel RTV320 E raggiungono 270 Wh/kg con range di temperatura esteso, rendendole adatte per applicazioni marziane dove le temperature ambiente raggiungono −80°C.

### Parametri di utilizzo batteria {#sec:battery-utilisation}

L'energia utilizzabile dalla batteria è ridotta dall'efficienza di scarica e dalle limitazioni di profondità di scarica. L'efficienza di scarica tiene conto delle perdite per resistenza interna durante l'assorbimento di corrente:

$$E_\text{utilizzabile} = E_\text{totale} \times DoD \times \eta_\text{batt}$$ {#eq:usable-energy}

dove $E_\text{totale}$ è la capacità nominale della batteria, $DoD$ è la profondità di scarica, e $\eta_\text{batt}$ è l'efficienza di scarica.

Per il dimensionamento dell'aeromobile, l'energia disponibile è convenientemente espressa come funzione dell'MTOW utilizzando la frazione di massa della batteria:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$ {#eq:battery-energy-fraction}

dove $f_\text{batt}$ è la frazione di massa della batteria (da @sec:initial-mass-estimate) e $e_\text{spec}$ è l'energia specifica (Wh/kg). Questa equazione è applicata nell'analisi dei vincoli (@sec:constraint-analysis) per determinare l'energia disponibile per ciascuna configurazione.

Viene adottata una profondità di scarica di $DoD$ = 0.80 per preservare la vita ciclica della batteria. L'efficienza di scarica dipende dal C-rate (corrente di scarica relativa alla capacità). Per le correnti di scarica previste durante il funzionamento dell'UAV marziano (circa 3-5C durante l'hovering, 0.5-1C durante la crociera), le batterie al litio allo stato solido raggiungono efficienze di scarica di 0.93-0.97 [@sadraeyDesignUnmannedAerial2020]. Viene adottato un valore di $\eta_\text{batt}$ = 0.95 come rappresentativo di tassi di scarica moderati.
