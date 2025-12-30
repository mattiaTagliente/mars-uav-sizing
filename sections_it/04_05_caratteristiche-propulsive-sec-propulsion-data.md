# Dati di riferimento e analisi dei compromessi

## Caratteristiche propulsive {#sec:propulsion-data}

Gli UAV di riferimento impiegano prevalentemente una configurazione QuadPlane, combinando quattro rotori di sollevamento verticali con un'elica spingente separata per la crociera. Questa architettura disaccoppia portanza e spinta, consentendo l'ottimizzazione di ciascun sistema propulsivo. La potenza del motore di sollevamento varia significativamente con l'MTOW, spaziando da circa 500 W (es. Sunnysky 4112 sull'X2400 da 8.5 kg) a 6000 W (es. T-Motor V13L sul V13-5 da 26.5 kg). @tbl:reference-propulsion-commercial riassume i dati propulsivi per i benchmark commerciali, incluse le masse dei motori dalle schede tecniche dei produttori.

: Specifiche propulsive UAV VTOL commerciali {#tbl:reference-propulsion-commercial}

| UAV | Motore lift | Potenza (W) | Massa (g) | Elica (in) | Motore crociera | Potenza (W) | Massa (g) | Rif. |
|:----|:-----------|----------:|---------:|----------:|:-------------|----------:|---------:|:----:|
| UAVMODEL X2400 | Sunnysky 4112 485KV | 550 | 153 | 15 | Sunnysky 3525 465KV | 2100 | 259 | [@uavmodelUAVMODELX2400VTOL2024] |
| AirMobi V25 | T-Motor MN505-S KV260 | 2500 | 225 | 16-17 | T-Motor AT4130 KV230 | 2500 | 408 | [@airmobiAirmobiV25Full2024] |
| V13-5 Sentinel | T-Motor V13L KV65 | 6000 | 1680 | N.D. | N.D. | N.D. | N.D. | [@spideruavV135SentinelVTOL2024] |

I concetti di aeromobili marziani presentano architetture propulsive distinte guidate dall'atmosfera rarefatta. @tbl:reference-propulsion-mars riassume i dati disponibili da fonti NASA e accademiche. I dati sulla massa del motore non sono generalmente disponibili per i concetti marziani poiché utilizzano design personalizzati o concettuali piuttosto che componenti commerciali.

: Specifiche propulsive UAV marziani {#tbl:reference-propulsion-mars}

| UAV | Motore lift | Potenza (W) | Elica (in) | Motore crociera | Potenza (W) | Rif. |
|:----|:-----------|----------:|----------:|:-------------|----------:|:----:|
| Ingenuity | 2 × 46-poli BLDC (AeroVironment) | circa 175 ciascuno | 48 | N.D. | N.D. | [@balaramMarsHelicopterTechnology2018] |
| Mars Science Helicopter | 6 × Elettrico (concettuale) | circa 550 ciascuno | 50 | N.D. | N.D. | [@johnsonMarsScienceHelicopter2020] |
| Concetto VTOL ibrido | 6 × Elettrico (concettuale) | circa 750 ciascuno | 20 | Elettrico | circa 635 | [@bertaniPreliminaryDesignFixedwing2023] |

Ingenuity utilizza due motori brushless DC outrunner a 46 poli personalizzati progettati e costruiti da AeroVironment per azionare i suoi rotori coassiali controrotanti a velocità superiori a 2400 RPM [@balaramMarsHelicopterTechnology2018]. La potenza totale di ingresso del sistema di circa 350 W corrisponde a circa 175 W per motore. Sei motori DCX 10S brushed DC Maxon aggiuntivi (7.1 g ciascuno) attivano il meccanismo del piatto oscillante per il controllo del passo delle pale, contribuendo con una potenza trascurabile (circa 1.4 W ciascuno) rispetto al sistema di propulsione principale [@maxongroupMaxonMotorsFly2021].

I dati del Mars Science Helicopter corrispondono alla configurazione esacottero da 31 kg, che richiede circa 3300 W di potenza di hovering distribuiti su sei rotori (circa 550 W ciascuno). Questo design rientra in un aeroshell di 2.5 m di diametro [@johnsonMarsScienceHelicopter2020]. Il concetto VTOL ibrido utilizza sei rotori di sollevamento da 20 pollici richiedendo circa 4500 W di potenza all'albero totale per il volo verticale (circa 750 W ciascuno), con un sistema di propulsione di crociera separato che richiede circa 635 W per il volo in avanti a 92 m/s [@bertaniPreliminaryDesignFixedwing2023].

Queste specifiche contrastano con i riferimenti commerciali in termini di potenza specifica. Ingenuity (1.8 kg) opera con una potenza media di sistema di circa 350 W, ottenendo una potenza specifica di circa 194 W/kg, riflettendo la natura ad alta intensità energetica del volo a rotore nell'atmosfera rarefatta marziana [@tzanetosIngenuityMarsHelicopter2022]. Il concetto Mars Science Helicopter (31 kg) scala questo approccio a una potenza di hovering stimata di circa 3300 W, ottenendo circa 106 W/kg grazie a rotori più grandi e più efficienti [@johnsonMarsScienceHelicopter2020]. ARES (175 kg) richiedeva un sistema a razzo bipropellente (MMH/MON3) piuttosto che propulsione elettrica per raggiungere il suo raggio di 600 km [@braunDesignARESMars2006]. I recenti studi VTOL ibridi per Marte stimano requisiti di potenza di crociera di circa 635 W (circa 32 W/kg), paragonabili alla potenza specifica di crociera di droni terrestri efficienti perché le velocità di volo più elevate su Marte compensano la minore densità atmosferica [@bertaniPreliminaryDesignFixedwing2023].

I dati indicano che mentre i requisiti di potenza di crociera sono simili tra piattaforme marziane e terrestri, la fase di sollevamento nell'atmosfera marziana richiede sistemi ad alta potenza specifica.

### Parametri di efficienza propulsiva {#sec:propulsion-efficiency}

La potenza richiesta sia per il volo hovering che per la crociera deve tenere conto delle perdite nella catena propulsiva. Questi parametri di efficienza impattano direttamente sul consumo energetico e sono input per l'analisi dei vincoli.

#### Figura di merito

La figura di merito quantifica l'efficienza del rotore in hovering, definita come il rapporto tra la potenza indotta ideale (dalla teoria della quantità di moto) e la potenza effettiva:

$$
FM = \frac{P_\text{ideale}}{P_\text{effettiva}} = \frac{T^{3/2}/\sqrt{2 \rho A}}{P_\text{effettiva}}
$$ {#eq:figure-of-merit-def}

Per elicotteri a grandezza naturale ad alti numeri di Reynolds ($Re > 10^6$), $FM$ raggiunge tipicamente 0.75-0.82 [@leishmanPrinciplesHelicopterAerodynamics2006]. Tuttavia, la figura di merito degrada sostanzialmente a bassi numeri di Reynolds a causa dell'aumento della resistenza di profilo. Leishman documenta che i micro velivoli ad ala rotante (MAV) a numeri di Reynolds molto bassi ($Re \sim 10{,}000$-$50{,}000$) raggiungono valori di $FM$ di solo 0.30-0.50 [@leishmanPrinciplesHelicopterAerodynamics2006]. Questa degradazione risulta da coefficienti di resistenza di profilo che aumentano da $C_{d_0} \approx 0.01$ ad alto $Re$ a $C_{d_0} \approx 0.035$ a basso $Re$.

I rotori marziani operano a numeri di Reynolds di $Re \approx 11{,}000$ per Ingenuity e $Re \approx 15{,}000$-$25{,}000$ per i concetti Mars Science Helicopter [@johnsonMarsScienceHelicopter2020], collocandoli nel regime dove avviene una significativa degradazione di $FM$. Basandosi sui dati di Leishman per MAV a basso Reynolds, la $FM$ del rotore marziano è stimata a 0.40, rappresentando la mediana dell'intervallo documentato 0.30-0.50.

#### Efficienza dell'elica

L'efficienza dell'elica di crociera è definita come:

$$
\eta_\text{elica} = \frac{T \times V}{P_\text{albero}}
$$ {#eq:propeller-efficiency}

Eliche ottimizzate ad alti numeri di Reynolds raggiungono $\eta_\text{elica} \approx 0.80$-$0.85$ [@sadraeyDesignUnmannedAerial2020]. Ai numeri di Reynolds previsti per la crociera marziana ($Re \approx 50{,}000$-$100{,}000$), l'efficienza degrada a causa dell'aumento della resistenza di profilo. Sadraey documenta efficienze dell'elica di 0.50-0.65 per piccole eliche UAV operanti in questo regime di Reynolds [@sadraeyDesignUnmannedAerial2020]. L'efficienza dell'elica di crociera marziana è stimata a 0.55 con un intervallo di 0.45-0.65.

#### Efficienza del motore e dell'ESC

I motori brushless DC utilizzati nelle applicazioni UAV raggiungono tipicamente efficienze di picco dell'88-92% [@sadraeyDesignUnmannedAerial2020], con valori dell'85-87% alle impostazioni di potenza di crociera (40-60% della potenza massima). I regolatori di velocità elettronici (ESC) raggiungono un'efficienza del 93-98% a impostazioni di acceleratore moderate o alte [@sadraeyDesignUnmannedAerial2020]. Queste efficienze sono relativamente non influenzate dalle condizioni atmosferiche marziane, sebbene la gestione termica nell'atmosfera rarefatta richieda considerazione.

#### Riepilogo delle efficienze

@tbl:efficiency-parameters riassume i valori di efficienza per l'analisi dei vincoli dell'UAV marziano.

: Parametri di efficienza propulsiva per il dimensionamento dell'UAV marziano {#tbl:efficiency-parameters}

| Parametro | Simbolo | Valore | Intervallo | Fonte |
|:----------|:------:|------:|------:|:-------|
| Figura di merito | $FM$ | 0.40 | 0.30-0.50 | [@leishmanPrinciplesHelicopterAerodynamics2006] |
| Efficienza elica | $\eta_\text{elica}$ | 0.55 | 0.45-0.65 | [@sadraeyDesignUnmannedAerial2020] |
| Efficienza motore | $\eta_\text{motore}$ | 0.85 | 0.82-0.90 | [@sadraeyDesignUnmannedAerial2020] |
| Efficienza ESC | $\eta_\text{ESC}$ | 0.95 | 0.93-0.98 | [@sadraeyDesignUnmannedAerial2020] |

L'efficienza combinata dalla batteria alla potenza di spinta è:

$$\eta_\text{hover} = FM \times \eta_\text{motore} \times \eta_\text{ESC} = 0.4000 \times 0.8500 \times 0.9500 = 0.3230$$ {#eq:hover-efficiency}

$$\eta_\text{crociera} = \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC} = 0.5500 \times 0.8500 \times 0.9500 = 0.4436$$ {#eq:cruise-efficiency}

Queste efficienze combinate indicano che circa il 32% della potenza della batteria è convertita in potenza di spinta utile in hovering, e il 44% in potenza di spinta di crociera. La bassa figura di merito domina la catena di efficienza in hovering, mentre l'efficienza dell'elica limita le prestazioni in crociera.

### Carico del disco {#sec:disk-loading}

Il carico del disco ($DL = T/A$) è il rapporto tra la spinta del rotore e l'area totale del disco del rotore ed è un parametro fondamentale per il dimensionamento degli aeromobili a rotore. Un carico del disco più alto riduce la dimensione del rotore ma aumenta i requisiti di potenza, poiché la velocità indotta e la potenza di hovering scalano con la radice quadrata del carico del disco.

Per la configurazione a rotori coassiali di Ingenuity, il carico del disco può essere calcolato dalle sue specifiche. Con una massa di 1.8 kg (peso 6.68 N su Marte), raggio del rotore di 0.60 m (diametro 1.2 m) e due rotori:

$$DL_\text{Ingenuity} = \frac{W}{2 \pi R^2} = \frac{6.68}{2 \times \pi \times 0.60^2} = \frac{6.68}{2.26} \approx 3.0 \text{ N/m}^2$$ {#eq:dl-ingenuity}

Il concetto esacottero Mars Science Helicopter (31 kg, sei rotori con raggio di 0.64 m) ha un carico del disco più alto [@johnsonMarsScienceHelicopter2020]:

$$DL_\text{MSH} = \frac{W}{6 \pi R^2} = \frac{31 \times 3.711}{6 \times \pi \times 0.64^2} = \frac{115}{7.72} \approx 15 \text{ N/m}^2$$ {#eq:dl-msh}

I multicotteri commerciali terrestri operano tipicamente con carichi del disco di 100-400 N/m² alla densità del livello del mare. Il rapporto del carico del disco richiesto tra Marte e la Terra scala con l'inverso della densità per mantenere una velocità indotta equivalente:

$$\frac{DL_\text{Marte}}{DL_\text{Terra}} = \frac{\rho_\text{Terra}}{\rho_\text{Marte}} = \frac{1.225}{0.0196} \approx 63$$

Questo fattore di scala spiega perché gli aeromobili marziani a rotore richiedono rotori molto più grandi (carico del disco più basso) rispetto a equivalenti terrestri della stessa massa.

Per l'UAV marziano, viene adottato un carico del disco di 30 N/m² come compromesso di progetto tra dimensione del rotore e potenza di hovering. Questo valore è più alto di Ingenuity (2.956 N/m²) e MSH (14.90 N/m²), ma inferiore a quanto lo scalamento equivalente terrestre suggerirebbe, bilanciando i requisiti contrastanti di geometria compatta del rotore e potenza di hovering accettabile nell'atmosfera marziana. Le implicazioni di questa scelta per il dimensionamento del rotore e i requisiti di potenza sono analizzate in @sec:constraint-analysis.

### Rapporto portanza/resistenza equivalente per aeromobili a rotore {#sec:rotorcraft-ld}

Per gli aeromobili a rotore in volo traslato, un rapporto portanza/resistenza equivalente $(L/D)_\text{eff}$ caratterizza l'efficienza propulsiva complessiva. Questo parametro mette in relazione la potenza con il prodotto di peso e velocità:

$$P = \frac{W \times V}{(L/D)_\text{eff}}$$ {#eq:rotorcraft-power}

A differenza degli aeromobili ad ala fissa dove $L/D$ è un parametro puramente aerodinamico, il rapporto $L/D$ equivalente per aeromobili a rotore include l'efficienza propulsiva del rotore e le perdite indotte in volo traslato. @tbl:rotorcraft-ld riassume i valori tipici per diverse configurazioni di aeromobili a rotore.

: Rapporto portanza/resistenza equivalente per configurazioni ad ala rotante [@proutyHelicopterPerformanceStability2002; @leishmanPrinciplesHelicopterAerodynamics2006] {#tbl:rotorcraft-ld}

| Configurazione | $(L/D)_\text{eff}$ | Note |
|:--------------|:------------------:|:------|
| Elicottero convenzionale | 4-6 | Resistenza del mozzo, inefficienza del rotore |
| Compound ottimizzato | 6-8 | L'ala alleggerisce il rotore ad alta velocità |
| Puro multirotore | 3-5 | Nessun beneficio dalla portanza traslazionale |

Viene adottato un valore di $(L/D)_\text{eff}$ = 4.000 per l'analisi della configurazione ad ala rotante dell'UAV marziano, rappresentando una stima conservativa che tiene conto del regime a basso numero di Reynolds e dell'ottimizzazione limitata del rotore a piccola scala. Questo valore è utilizzato solo per il confronto della configurazione puramente ad ala rotante; l'analisi VTOL ibrida utilizza i valori di $L/D$ ad ala fissa per la crociera.
