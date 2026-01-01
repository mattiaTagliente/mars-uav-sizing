# Dati di riferimento e analisi dei compromessi

## Requisiti derivati {#sec:derived-requirements}

Questa sezione traduce le esigenze qualitative dell'utente identificate in @sec:user-needs in requisiti quantitativi e verificabili. Ogni requisito è derivato dalle esigenze degli stakeholder attraverso l'analisi dell'ambiente operativo, delle prestazioni delle piattaforme di riferimento e dei vincoli fisici. I requisiti documentati qui forniscono gli input numerici per l'analisi dei vincoli (@sec:constraint-analysis).

### Requisiti operativi {#sec:operational-requirements}

I requisiti operativi definiscono l'inviluppo di prestazioni della missione derivato dalle esigenze utente N1 (raggio esteso), N2 (imaging aereo), N5 (autonomia estesa) e N4 (capacità VTOL).

#### Raggio operativo

L'UAV dovrà raggiungere un raggio operativo di almeno 50 km. Questo requisito deriva dall'esigenza utente N1 (raggio esteso oltre la capacità dei rover di superficie). Il rover Curiosity ha percorso circa 35 km in totale in oltre un decennio sulla superficie marziana [@nasaMarsScienceLaboratory2025]<!-- #s:distance -->. Un raggio di 50 km consente il rilevamento in un singolo volo di aree inaccessibili ai rover entro tempistiche di missione pratiche, fornendo un miglioramento sostanziale delle capacità che giustifica lo sviluppo dell'UAV. La verifica è dimostrata attraverso test di volo di autonomia che copre 100 km di distanza andata e ritorno.

#### Altitudine operativa

L'UAV dovrà operare ad altitudini tra 30 m e 350 m sopra il livello del suolo. L'altitudine minima di 30 m deriva dalle esigenze di separazione dal terreno: le distribuzioni di frequenza-dimensione delle rocce nei siti di atterraggio marziani indicano che le rocce pericolose sono tipicamente alte 0.5 m o circa 1 m di diametro [@golombekRockSizeFrequencyDistributions2021]<!-- #abs -->, e 30 m fornisce un fattore di sicurezza di 60× rispetto ai più grandi ostacoli superficiali comuni. L'altitudine massima di 350 m deriva dai requisiti di risoluzione dell'imaging (esigenza utente N2). La mappatura geologica richiede tipicamente una distanza di campionamento a terra (GSD) di 5-10 cm per pixel. Per una camera con passo pixel di 2.4 μm e lunghezza focale di 8.8 mm (tipico sensore da 1 pollice come il DJI Air 2S [@djiDJIAir2S2021]<!-- #specs -->), il GSD è calcolato come:

$$GSD = \frac{H \cdot p}{f}$$ {#eq:gsd}

dove $H$ è l'altitudine di volo, $p$ è il passo pixel, e $f$ è la lunghezza focale. Per ottenere un GSD di 10 cm è richiesto:

$$H_\text{max} = \frac{GSD \cdot f}{p} = \frac{0.10 \times 8.8 \times 10^{-3}}{2.4 \times 10^{-6}} = 367 \text{ m}$$ {#eq:hmax}

Arrotondando a 350 m si assicura che il requisito di GSD di 10 cm sia soddisfatto con margine. La verifica è dimostrata attraverso test di volo con mantenimento di altitudine e validazione dell'imaging.

#### Autonomia di volo

L'UAV dovrà raggiungere un tempo di volo totale di almeno 60 minuti, incluse le fasi di hovering e crociera. Questo requisito deriva dall'esigenza utente N5 (autonomia estesa) in combinazione con il requisito di raggio operativo. Il profilo di missione (@sec:mission-parameters) richiede 42 minuti di tempo di transito (100 km andata e ritorno a 40 m/s), 15 minuti di operazioni di rilevamento, 2 minuti di fasi di hovering (decollo e atterraggio) e 1 minuto di fasi di transizione, per un totale di 60 minuti. Questa autonomia supera l'elicottero Ingenuity, che ha raggiunto voli individuali fino a 169 secondi e tempo di volo cumulativo di circa 129 minuti su 72 voli [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights --> [@tzanetosIngenuityMarsHelicopter2022]<!-- #abs -->. La verifica è dimostrata attraverso test di volo con profilo di missione completo.

### Requisiti ambientali {#sec:environmental-requirements}

I requisiti ambientali definiscono le condizioni in cui l'UAV deve operare, derivati dalle esigenze utente N7 (tolleranza al vento), N8 (protezione dalla polvere), N10 (tolleranza alle radiazioni) e N11 (compatibilità termica).

#### Tolleranza al vento

L'UAV dovrà operare in sicurezza con venti sostenuti fino a 10 m/s. Le misurazioni del vento da parte del rover Mars 2020 Perseverance nel cratere Jezero hanno rilevato velocità medie del vento di 3.2 ± 2.3 m/s, con picchi pomeridiani che raggiungono 6.1 ± 2.2 m/s; il 99% dei venti misurati è rimasto sotto i 10 m/s [@viudez-moreirasWindsMars20202022]<!-- #abs -->. Il limite di 10 m/s accomoda le condizioni marziane tipiche con margine. Sebbene i venti delle tempeste di polvere possano raggiungere 27 m/s [@nasaFactFictionMartian2015]<!-- #s:storms -->, le operazioni di volo durante tali eventi sono rinviate piuttosto che progettate per essere sostenute. La verifica include test in galleria del vento dell'autorità di controllo e simulazione di volo con profili di raffica di 10 m/s.

#### Protezione dalla polvere

Tutti i componenti critici dovranno essere protetti secondo lo standard IP6X. La protezione dalla polvere segue il codice IP definito dalla IEC 60529 [@internationalelectrotechnicalcommissionDegreesProtectionProvided2013]<!-- #s:ip6x -->. IP6X denota involucri a tenuta di polvere con esclusione completa del particolato, necessaria data la fine regolite marziana (dimensioni delle particelle 1-100 μm) che può degradare cuscinetti meccanici e superfici ottiche. La verifica avviene attraverso test di ingresso polvere secondo le procedure IEC 60529 o equivalenti.

#### Tolleranza alle radiazioni

L'elettronica dovrà tollerare una dose totale ionizzante di almeno 1 krad(Si). Lo strumento RAD del Mars Science Laboratory ha misurato un tasso medio di dose assorbita di circa 76 mGy/anno (7.6 rad/anno, o 0.0076 krad/anno) sulla superficie marziana [@hasslerMarsSurfaceRadiation2014]<!-- #abs -->. In una missione biennale, la dose accumulata è circa 0.015 krad. Un requisito di tolleranza alle radiazioni di 1 krad(Si) di dose totale ionizzante fornisce un margine di circa 67× ed è raggiungibile con elettronica commerciale off-the-shelf (COTS), che tipicamente tollera 5-20 krad senza richiedere costosi componenti radiation-hardened [@brunettiCOTSDevicesSpace2024]<!-- #abs -->. La verifica avviene attraverso dati di test di radiazione a livello di componente o qualifica per heritage.

#### Range di temperatura operativa

L'UAV dovrà operare a temperature ambiente da −80 °C a +20 °C. Le escursioni termiche diurne di Marte variano da circa −80 °C (notte) a +20 °C (mezzogiorno) a seconda della stagione e della posizione. I sottosistemi critici (in particolare batterie e camere) richiedono gestione termica per funzionare entro i loro range operativi. Il requisito si applica all'ambiente circostante; le temperature interne dei sottosistemi sono gestite attraverso isolamento e riscaldamento attivo. La verifica avviene attraverso test in vuoto termico attraverso il range di temperatura.


### Selezione del fattore di carico {#sec:load-factor-selection}

Le equazioni di stima del peso strutturale in @sec:mass-breakdown includono il fattore di carico ultimo ($n_\text{ult}$) come parametro chiave. Questa sottosezione documenta la selezione del fattore di carico e la sua giustificazione.

#### Definizioni

Il *fattore di carico limite* ($n_\text{limite}$) è il massimo fattore di carico atteso in operazione normale senza deformazione permanente. Il *fattore di carico ultimo* ($n_\text{ult}$) è il fattore di carico limite moltiplicato per un fattore di sicurezza [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017]<!-- #cs23.2230 -->:

$$n_\text{ult} = n_\text{limite} \times FS$$ {#eq:n-ult-definition}

dove $FS = 1.5$ è il fattore di sicurezza aerospaziale standard [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017, CS 23.2230(a)(2)]<!-- #cs23.2230 -->. Questo fattore 1.5 tiene conto delle variazioni delle proprietà dei materiali, delle tolleranze di fabbricazione, della fatica e delle tolleranze ai danni, e dell'incertezza nella previsione dei carichi.
La struttura deve sopportare i carichi limite senza deformazione permanente, e i carichi ultimi senza cedimento.

#### Motivazione della selezione del fattore di carico

Per l'UAV marziano, viene adottato un fattore di carico limite di $n_\text{limite} = 2.5$, che produce:

$$n_\text{ult} = 2.5 \times 1.5 = 3.75$$

Questo valore rappresenta il limite inferiore dei requisiti della categoria normale CS-23 ed è giustificato da quattro considerazioni.

Primo, l'operazione senza equipaggio cambia fondamentalmente la filosofia di progettazione strutturale. Il cedimento strutturale di un aeromobile con equipaggio mette a rischio vite umane, motivando margini di sicurezza conservativi. Per un veicolo autonomo senza equipaggio, le conseguenze del cedimento sono limitate alla perdita della missione e al danno all'equipaggiamento. Margini di sicurezza strutturale più bassi sono quindi accettabili e standard per i sistemi senza pilota.

Secondo, il volo autonomo con inviluppo di manovra limitato fornisce protezione intrinseca dal carico. Il sistema di controllo di volo impone limiti di manovra rigorosi tramite software. A differenza degli aeromobili pilotati, dove manovre rapide o di panico possono generare carichi inattesi, l'autopilota limita l'angolo di rollio (tipicamente 45-60°) e il fattore di carico comandato (tipicamente 2-3 g). Questo inviluppo limitato assicura che il carico limite di progetto non sia superato in operazione normale.

Terzo, i carichi da raffica sono sostanzialmente ridotti nell'atmosfera marziana. I fattori di carico indotti dalle raffiche scalano con la densità atmosferica. L'incremento del fattore di carico da raffica può essere espresso come:

$$\Delta n_\text{raffica} \propto \frac{\rho \cdot U_\text{de} \cdot V \cdot a}{W/S}$$

dove $\rho$ è la densità atmosferica, $U_\text{de}$ è la velocità di raffica di progetto, $V$ è la velocità di volo, e $a$ è la pendenza della curva di portanza. Alla densità superficiale di Marte (circa 0.020 kg/m³), i carichi da raffica sono circa 60 volte inferiori rispetto al livello del mare terrestre per velocità di raffica equivalenti. Anche con le velocità di raffica di progetto più elevate su Marte (fino a 10 m/s, secondo @sec:user-needs), il contributo del carico da raffica rimane trascurabile rispetto ai carichi di manovra. Il fattore di carico di manovra domina quindi la progettazione strutturale.

Quarto, i precedenti dei velivoli a rotore marziani supportano fattori di carico ridotti. Lo studio NASA Mars Science Helicopter [@johnsonMarsScienceHelicopter2020]<!-- #s:loads --> ha notato che "i carichi aerodinamici sulla pala sono piccoli a causa della bassa densità atmosferica su Marte," consentendo design strutturali leggeri innovativi. Sebbene i fattori di carico specifici non siano pubblicati per Ingenuity o MSH, l'atmosfera rarefatta riduce fondamentalmente il carico aerodinamico rispetto ai design terrestri.

#### Confronto con altre categorie di aeromobili

@tbl:load-factor-comparison presenta i fattori di carico dell'UAV marziano nel contesto di altre categorie di aeromobili.

: Confronto dei fattori di carico per varie categorie di aeromobili {#tbl:load-factor-comparison}

| Categoria aeromobile | $n_\text{limite}$ | FS | $n_\text{ult}$ | Fonte |
|:---|:---:|:---:|:---:|:---|
| CS-25 trasporto (alto W) | 2.5 | 1.5 | 3.75 | FAR Part 25 |
| CS-25 trasporto (basso W) | 3.8 | 1.5 | 5.7 | FAR Part 25 |
| CS-23 normale (pesante) | 2.5 | 1.5 | 3.75 | CS-23 Amdt 4 §23.337 |
| CS-23 normale (leggero) | 3.8 | 1.5 | 5.7 | CS-23 Amdt 4 §23.337 |
| CS-23 utility | 4.4 | 1.5 | 6.6 | CS-23 Amdt 4 |
| CS-23 acrobatico | 6.0 | 1.5 | 9.0 | CS-23 Amdt 4 |
| UAV marziano (questo studio) | 2.5 | 1.5 | 3.75 | Questo lavoro |

Il valore selezionato $n_\text{ult} = 3.75$ corrisponde al limite inferiore degli aeromobili certificati di categoria normale e al valore utilizzato per gli aeromobili da trasporto pesanti. Questa selezione bilancia la riduzione del peso strutturale con margini di sicurezza accettabili per una piattaforma di ricerca senza equipaggio.

Per quanto riguarda lo status regolamentare, EASA CS-23 e FAA Part 23 sono standard di certificazione terrestri per aeromobili con equipaggio. L'UAV marziano non è soggetto a queste normative. CS-23 è utilizzato qui come riferimento metodologico per stabilire fattori di carico consistenti e standard del settore, non come requisito regolamentare.

L'impatto sul peso strutturale del ridotto fattore di carico ultimo è quantificato in @sec:mass-breakdown, dove le equazioni di stima del peso sono applicate alla geometria dimensionata. Il ridotto fattore di carico consente circa il 23% di riduzione del peso dell'ala e il 10% di riduzione del peso della fusoliera rispetto agli aeromobili leggeri progettati secondo gli standard CS-25 ($n_\text{ult} = 5.7$).


### Limiti dei parametri geometrici {#sec:geometry-bounds}

Questa sezione definisce i parametri geometrici della pianta alare utilizzati nell'analisi dei vincoli e nella stima del peso. Ogni parametro comporta compromessi che determinano lo spazio di progetto ottimale per l'UAV marziano.

#### Allungamento

L'allungamento è limitato come:

$$AR \in [5, 7]$$ {#eq:ar-bounds}

La resistenza indotta scala inversamente con l'allungamento:

$$C_{D,i} = \frac{C_L^2}{\pi \cdot AR \cdot e}$$ {#eq:induced-drag}

Un maggiore allungamento riduce la resistenza indotta, mentre il peso dell'ala aumenta approssimativamente come $AR^{0.6}$ [@sadraeyAircraftDesignSystems2013]<!-- #ch10:ar -->. A parità di superficie alare, un maggiore allungamento riduce anche la corda media:

$$\bar{c} = \sqrt{\frac{S}{AR}}$$ {#eq:chord-from-ar}

Questa riduzione della corda influenza il numero di Reynolds, che è vincolato dai requisiti di prestazione del profilo.

L'intervallo selezionato è basato sia sui dati degli UAV terrestri che sugli studi specifici per Marte. Gli allungamenti tipici per piccoli UAV variano da 4 a 12 [@sadraeyAircraftDesignSystems2013]<!-- #ch10:ar -->. I design di UAV marziani in letteratura selezionano consistentemente allungamenti nell'intervallo da 5 a 6. Il design dell'aereo marziano ARES ha utilizzato $AR$ = 5.6 [@braunDesignARESMars2006]<!-- #s:ar -->. Barbato et al. hanno trovato un $AR$ ottimale da 5.3 a 6.3 per un UAV marziano a energia solare da 24 kg [@barbatoPreliminaryDesignFixedWing2024]<!-- #s:ar -->, dimostrando che l'allungamento ottimale aumenta con il coefficiente di portanza e diminuisce con la massa del payload.

Viene adottato un allungamento di base di $AR$ = 6, che rappresenta un compromesso tra riduzione della resistenza indotta (che favorisce AR più alti) e peso strutturale (che favorisce AR più bassi). All'MTOW target di 10 kg, questo allungamento fornisce un adeguato rapporto portanza/resistenza mantenendo una corda alare ragionevole per i requisiti di numero di Reynolds e uno spessore strutturale per la capacità di sopportare i carichi.


#### Rapporto di spessore

Il rapporto di spessore dell'ala è limitato da considerazioni strutturali e aerodinamiche:

$$t/c \in [0.06, 0.11]$$ {#eq:tc-bounds}

Questo intervallo riflette le caratteristiche di spessore dei profili candidati a basso Reynolds dal database UIUC [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:thickness --> [@williamsonSummaryLowSpeedAirfoil2012]<!-- #v5:thickness -->. I profili candidati coprono rapporti di spessore dal 6.2% (AG12, serie AG sottile) fino al 10.5% (S7055, design bilanciato). Il profilo general-purpose E387 ha $t/c$ = 9.1%, il profilo a bassa resistenza SD8000 ha $t/c$ = 8.9%, e il profilo general-purpose SD7037 ha $t/c$ = 9.2%.

Il peso strutturale dell'ala scala approssimativamente come $(t/c)^{-0.3}$ [@sadraeyAircraftDesignSystems2013]<!-- #ch10:tc -->, favorendo profili più spessi per l'efficienza strutturale. Viene adottato un rapporto di spessore di base di $t/c$ = 0.09 per il dimensionamento, fornendo adeguato spessore strutturale pur rimanendo compatibile con i profili candidati. La selezione specifica del profilo è rinviata a @sec:airfoil-selection dove le prestazioni aerodinamiche al numero di Reynolds di progetto sono valutate.

#### Rapporto di rastremazione

Il rapporto di rastremazione è vincolato a:

$$\lambda \in [0.4, 0.6]$$ {#eq:taper-bounds}

dove $\lambda = c_\text{tip} / c_\text{root}$.

Per la minima resistenza indotta, la distribuzione di portanza lungo l'apertura ideale è ellittica, e per un'ala non a freccia, un rapporto di rastremazione di circa $\lambda$ = 0.4 approssima strettamente questa distribuzione di carico [@sadraeyAircraftDesignSystems2013]<!-- #ch5:taper -->. Le ali rastremate concentrano inoltre il materiale strutturale vicino alla radice dove i momenti flettenti sono massimi, migliorando l'efficienza strutturale, sebbene rapporti di rastremazione più bassi aumentino la suscettibilità allo stallo di estremità. Le ali rettangolari ($\lambda$ = 1.0) offrono la fabbricazione più semplice; il limite superiore di $\lambda$ = 0.6 rappresenta un compromesso verso la semplicità di fabbricazione pur mantenendo un carico quasi ellittico.

Viene adottato un valore nominale di $\lambda$ = 0.5 per il dimensionamento di base, fornendo circa il 98% della resistenza indotta minima teorica offrendo al contempo buone caratteristiche di stallo e ragionevole complessità di fabbricazione.

#### Angolo di freccia

L'angolo di freccia al quarto di corda è fissato a:

$$\Lambda = 0°$$ {#eq:sweep-selection}

La freccia alare è principalmente utilizzata per ritardare gli effetti di comprimibilità a velocità transoniche, tipicamente sopra $M$ = 0.7 [@sadraeyAircraftDesignSystems2013]<!-- #ch5:sweep -->. Il meccanismo è che la freccia riduce la componente di velocità perpendicolare al bordo d'attacco dell'ala, riducendo effettivamente il numero di Mach locale.

Al numero di Mach di crociera dell'UAV marziano di circa $M$ = 0.1741, gli effetti di comprimibilità sono del tutto trascurabili. La freccia non fornisce alcun beneficio aerodinamico a questa velocità e introduce penalità tra cui maggiore complessità strutturale dall'accoppiamento flessione-torsione, penalità di peso da strutture ad ala a freccia più pesanti, ridotta pendenza della curva di portanza che richiede angoli di attacco più elevati, e caratteristiche di stallo degradate poiché le ali a freccia tendono a stallare prima all'estremità, compromettendo il controllo di rollio.

Per l'UAV marziano viene adottata una configurazione senza freccia.

#### Riepilogo dei parametri geometrici

@tbl:geometry-summary consolida i parametri geometrici per l'analisi dei vincoli.

: Riepilogo dei parametri geometrici dell'ala {#tbl:geometry-summary}

| Parametro | Simbolo | Intervallo | Base | Motivazione |
|:----------|:------:|:-----:|:--------:|:----------|
| Allungamento | $AR$ | 5-7 | 6 | Precedenti UAV marziani, L/D vs. struttura |
| Rapporto di spessore | $t/c$ | 0.06-0.11 | 0.09 | Spessore strutturale vs. resistenza |
| Rapporto di rastremazione | $\lambda$ | 0.4-0.6 | 0.5 | Carico quasi ellittico |
| Angolo di freccia | $\Lambda$ | N.D. | 0° | Basso Mach, nessun beneficio |

### Parametri di velocità e tempo della missione {#sec:mission-parameters}

Questa sezione deriva e giustifica i parametri di velocità e tempo richiesti per l'analisi dei vincoli. Ogni parametro è tracciabile ai requisiti di missione (@sec:user-needs) e coerente con le condizioni atmosferiche (@sec:operational-environment).

#### Velocità di crociera

La selezione della velocità di crociera deve bilanciare vincoli multipli: numero di Mach, numero di Reynolds, consumo di potenza e requisiti di tempo di missione.

Rimanere ben sotto $M \approx 0.3$ mantiene piccole le correzioni per comprimibilità, poiché le variazioni di densità scalano approssimativamente con $M^2$ nel flusso subsonico. Viene presa come obiettivo una banda di Mach di progetto di $M_\infty \approx 0.16$-$0.28$, con una selezione iniziale intorno a $M \approx 0.1741$. Utilizzando la velocità del suono su Marte all'altitudine operativa ($a$ = 229.7 m/s da @tbl:atmosphere), questo corrisponde a:

$$V_\text{crociera} = M \times a = 0.1741 \times 229.7 \approx 40 \text{ m/s}$$ {#eq:cruise-velocity-value}

Questa velocità è circa il doppio di quella degli UAV VTOL ibridi terrestri tipici ma rappresenta un compromesso necessario: velocità inferiori richiederebbero corde alari eccessivamente grandi per raggiungere numeri di Reynolds accettabili, mentre velocità superiori aumenterebbero significativamente il consumo di potenza. La potenza di crociera scala fortemente con la velocità una volta che la resistenza parassita domina ($P \sim D \times V$, con resistenza parassita $\sim V^2$, portando a $P \sim V^3$).

Il numero di Reynolds in crociera è:

$$Re = \frac{\rho \cdot V \cdot c}{\mu}$$ {#eq:reynolds-definition}

Utilizzando le proprietà atmosferiche all'altitudine operativa da @tbl:atmosphere ($\rho$ = 0.0196 kg/m³, $\mu$ = 1.08 × 10⁻⁵ Pa·s), con $V$ = 40 m/s e puntando a $Re$ = 60,000:

$$c = \frac{Re \cdot \mu}{\rho \cdot V} = \frac{60{,}000 \times 1.08 \times 10^{-5}}{0.0196 \times 40} = 0.83 \text{ m}$$

La superficie alare è legata alla corda attraverso l'allungamento. Per $AR$ = 6 e corda media $\bar{c}$ = 0.83 m:

$$S = \bar{c}^2 \times AR = 0.83^2 \times 6 = 4.1 \text{ m}^2$$

@tbl:chord-velocity presenta la relazione tra velocità di crociera, corda e superficie alare per raggiungere $Re$ = 60,000 con $AR$ = 6.

: Requisiti di corda e superficie alare per Re = 60,000 {#tbl:chord-velocity}

| $V_\text{crociera}$ (m/s) | $\bar{c}$ richiesta (m) | $S$ richiesta (m²) con AR = 6 |
|:------------------------|:----------------------:|:------------------------:|
| 35 | 0.95 | 5.4 |
| 38 | 0.87 | 4.5 |
| 40 | 0.83 | 4.1 |

Queste superfici alari sono più grandi del tipico per piccoli UAV terrestri ma riflettono la bassa densità atmosferica su Marte. Per l'MTOW target di 10 kg (peso marziano $W$ = 37.1 N), una superficie alare di 4.1 m² produce un carico alare di circa 9 N/m².

Viene adottata una velocità di crociera di $V_\text{crociera}$ = 40 m/s, con un intervallo di sensibilità di 35-45 m/s per studi parametrici dell'analisi dei vincoli. Il raggio operativo di 50 km richiede una distanza andata e ritorno di 100 km, producendo un tempo di transito di 2500 s (circa 42 min) a 40 m/s.

#### Velocità minima

La velocità minima operativa fornisce un margine di sicurezza sopra la velocità di stallo. Secondo la pratica aerospaziale generale, le velocità di avvicinamento e minime operative per gli aeromobili sono tipicamente 1.2 volte la velocità di stallo [@sadraeyAircraftDesignSystems2013]<!-- #ch4:vmin -->:

$$V_\text{min} \geq 1.2 \times V_\text{stallo}$$ {#eq:v-min-constraint}

La velocità di stallo dipende dal carico alare:

$$V_\text{stallo} = \sqrt{\frac{2 \cdot (W/S)}{\rho \cdot C_{L,\text{max}}}}$$ {#eq:stall-speed-prelim}

Il fattore 1.2 assicura un margine adeguato per il recupero da disturbi di raffica, l'autorità di controllo a bassa velocità, e le manovre di transizione tra modalità di crociera e hovering.

#### Vincolo sul carico alare

Riarrangiando @eq:stall-speed-prelim per il carico alare:

$$\frac{W}{S} = \frac{1}{2} \rho V_\text{stallo}^2 C_{L,\text{max}}$$ {#eq:wing-loading-stall}

Per una velocità minima operativa $V_\text{min}$ con margine di sicurezza sopra lo stallo:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:wing-loading-constraint}

Questa equazione definisce il vincolo di stallo sul diagramma di matching. Su un diagramma con P/W sull'asse verticale e W/S sull'asse orizzontale, il vincolo di stallo appare come una linea verticale (W/S massimo costante) indipendente dal carico di potenza.

Per il progetto preliminare, utilizzando il carico alare derivato dall'analisi della velocità di crociera ($W/S \approx 9.000$ N/m² da @tbl:chord-velocity), $\rho$ = 0.01960 kg/m³, e $C_{L,\text{max}}$ = 1.150 (profilo SD8000, vedi @sec:airfoil-selection):

$$V_\text{stallo} = \sqrt{\frac{2 \times 9.000}{0.01960 \times 1.150}} = \sqrt{798.6} = 28.26 \text{ m/s}$$

$$V_\text{min} \geq 1.200 \times 28.26 = 33.91 \text{ m/s}$$

La velocità di crociera di 40.00 m/s fornisce un margine confortevole sopra la velocità minima, indicando che l'aeromobile opererà a coefficienti di portanza moderati durante la crociera piuttosto che vicino allo stallo. Questo margine permette manovre e fornisce sicurezza contro condizioni ventose.

#### Allocazione del tempo di hovering

Per la configurazione VTOL ibrida, il tempo di hovering è limitato al decollo e all'atterraggio. Le fasi di transizione sono contabilizzate separatamente. L'allocazione del tempo è riassunta in @tbl:hover-allocation.

: Allocazione del tempo di hovering per il bilancio energetico {#tbl:hover-allocation}

| Fase di volo | Durata (s) | Categoria | Descrizione |
|:-------------|-------------:|:---------|:------------|
| Salita al decollo | 30 | Hovering | Salita verticale a 30 m di altitudine sicura |
| Hovering al decollo | 30 | Hovering | Stazionamento prima della transizione |
| Transizione Q2P | 30 | Transizione | Passaggio da quad a ala fissa |
| Transizione P2Q | 30 | Transizione | Passaggio da ala fissa a quad |
| Hovering all'atterraggio | 30 | Hovering | Stazionamento dopo la transizione |
| Discesa all'atterraggio | 30 | Hovering | Discesa controllata e contatto |
| **Totale hovering** | **120** | N.D. | 2 min di hovering puro |
| **Totale transizione** | **60** | N.D. | 2 × 30 s |

Il tempo totale di hovering di 120 s (2 min) e il tempo totale di transizione di 60 s (1 min) sono utilizzati per i calcoli energetici. Queste durate sono stime ingegneristiche basate su operazioni QuadPlane terrestri scalate alle condizioni marziane. I dati di riferimento di @goetzendorf-grabowskiOptimizationEnergyConsumption2022 indicano un tempo VTOL totale di circa 2 minuti per un quad-plane da 10 kg, con decollo verticale di circa 20 s e atterraggio di 10-15 s. Il tempo restante copre hovering di stazionamento e transizioni. La durata di 30 s per ciascuna transizione è una stima conservativa; la durata effettiva dipende dal corridoio di transizione e dalla strategia di controllo impiegata [@mathurMultiModeFlightSimulation2025]<!-- #s:transition-time -->. Per Marte, l'allocazione tiene conto di tassi di salita più lenti nell'atmosfera rarefatta (stimati 1-2 m/s per un velivolo da 10 kg), fasi di transizione più lunghe dovute alla minore autorità di controllo e contingenza per raffiche di vento inattese o scenari di abort. Per confronto, l'elicottero Ingenuity ha raggiunto tempi di volo totali di 90-170 secondi per operazioni di puro velivolo a rotore [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights -->, sebbene il confronto diretto sia limitato poiché Ingenuity opera interamente in modalità hovering e volo avanzato a rotore piuttosto che transitando in crociera ad ala fissa.

#### Autonomia di crociera

Il requisito di autonomia di crociera è derivato dal raggio operativo di 50 km:

$$t_\text{crociera} = t_\text{andata} + t_\text{rilevamento} + t_\text{ritorno}$$ {#eq:cruise-time}

Le componenti sono: transito di andata (50,000 m / 40 m/s = 1250 s = 20.8 min), transito di ritorno (20.8 min), e rilevamento/loiter all'obiettivo (15 min per operazioni di mappatura). Il tempo totale di crociera è:

$$t_\text{crociera} = 20.8 + 20.8 + 15 \approx 57 \text{ min}$$ {#eq:cruise-endurance}

#### Riserva energetica

Una riserva energetica del 20% è mantenuta in aggiunta all'energia del profilo di missione. Questa riserva tiene conto di inefficienze di navigazione e correzioni di rotta, aumento di potenza dovuto a variazioni di densità atmosferica, hovering esteso per atterraggio di precisione, e capacità di ritorno di emergenza. La riserva è applicata al bilancio energetico totale, non alle singole fasi di volo.

#### Riepilogo del profilo di missione

@tbl:mission-profile presenta la timeline nominale della missione.

: Profilo di missione nominale {#tbl:mission-profile}

| Fase | Durata | Cumulativo | Modo di potenza |
|:------|:--------:|:----------:|:-----------|
| Hovering al decollo | 1 min | 1 min | Hovering |
| Transizione Q2P | 0.5 min | 1.5 min | Transizione |
| Crociera di andata | 21 min | 22.5 min | Crociera |
| Operazioni di rilevamento | 15 min | 37.5 min | Crociera |
| Crociera di ritorno | 21 min | 58.5 min | Crociera |
| Transizione P2Q | 0.5 min | 59 min | Transizione |
| Hovering all'atterraggio | 1 min | 60 min | Hovering |
| Volo totale | 60 min | N.D. | N.D. |

Il tempo di volo di 60 minuti più il 20% di riserva energetica produce un requisito di autonomia di progetto di circa 72 minuti di capacità energetica equivalente.

### Riepilogo dei requisiti derivati {#sec:requirements-summary}

@tbl:derived-requirements consolida tutti gli input numerici richiesti per l'analisi dei vincoli, organizzati per categoria funzionale come definito nella metodologia di dimensionamento. Ogni parametro è tracciato alla sua fonte: esigenza utente (N1-N11), analisi fisica, dati di riferimento, o standard di progetto.

: Parametri di input per l'analisi dei vincoli {#tbl:derived-requirements}

| ID | Parametro | Simbolo | Valore | Derivato da |
|:---|:----------|:------:|:------|:-------------|
| Parametri di missione | | | | |
| M1 | Massa del payload | $m_\text{payload}$ | 1.0 kg | N2, N3 |
| M2 | Velocità di crociera | $V_\text{crociera}$ | 40 m/s | Vincoli Mach, Re |
| M3 | Velocità minima | $V_\text{min}$ | 1.2 × $V_\text{stallo}$ | Margine di sicurezza |
| M4 | Tempo di crociera | $t_\text{crociera}$ | 57 min | N1, N5 |
| M5 | Tempo di hovering | $t_\text{hover}$ | 2 min | N4 |
| M5b | Tempo di transizione | $t_\text{transition}$ | 1 min | N4 |
| M6 | Riserva energetica | N.D. | 20% | Margine di sicurezza |
| Parametri geometrici | | | | |
| G1 | Allungamento | $AR$ | 6 | Precedenti marziani |
| G2 | Rapporto di spessore | $t/c$ | 0.09 | Compromesso struttura/aero |
| G3 | Rapporto di rastremazione | $\lambda$ | 0.5 | Carico ellittico |
| G4 | Angolo di freccia | $\Lambda$ | 0° | Basso Mach |
| Coefficienti aerodinamici | | | | |
| A1 | Coefficiente di portanza max | $C_{L,\text{max}}$ | 1.15 | SD8000 (UIUC) |
| A2 | Efficienza di Oswald | $e$ | 0.87 | Correlazione AR=6 |
| A3 | Resistenza a portanza nulla | $C_{D,0}$ | 0.030 | Buildup componenti |
| Efficienze propulsive | | | | |
| P1 | Figura di merito | FM | 0.40 | Dati rotore basso Re |
| P2 | Efficienza elica | $\eta_\text{elica}$ | 0.55 | Analisi basso Re |
| P3 | Efficienza motore | $\eta_\text{motore}$ | 0.85 | Tipico BLDC |
| P4 | Efficienza ESC | $\eta_\text{ESC}$ | 0.95 | Tipico industriale |
| Parametri energetici | | | | |
| E1 | Energia specifica batteria | $e_\text{spec}$ | 270 Wh/kg | Li-ion stato solido |
| E2 | Profondità di scarica | DoD | 0.80 | Vita ciclica |
| E3 | Efficienza di scarica | $\eta_\text{batt}$ | 0.95 | C-rate moderato |
| Parametri del rotore | | | | |
| R1 | Carico del disco | DL | 30 N/m² | Analisi compromessi |
| R2 | $(L/D)_\text{eff}$ elicottero | $(L/D)_\text{eff}$ | 4.0 | Tipico elicottero |
| Parametri strutturali | | | | |
| S1 | Fattore di carico limite | $n_\text{limite}$ | 2.5 | N6, CS-23 |
| S2 | Fattore di sicurezza | FS | 1.5 | Standard CS-23 |
| S3 | Fattore di carico ultimo | $n_\text{ult}$ | 3.75 | S1 × S2 |



I requisiti operativi e ambientali da @sec:operational-requirements e @sec:environmental-requirements definiscono l'inviluppo di prestazioni della missione ma non sono input diretti per l'analisi dei vincoli. Il requisito di raggio operativo (OR-1, ≥ 50 km) determina la velocità di crociera (M2) e il tempo di crociera (M4). Il requisito di autonomia di volo (OR-4, ≥ 60 min) vincola la somma del tempo di crociera e del tempo di hovering (M4, M5). Il requisito di tolleranza al vento (ER-1, ≥ 10 m/s) motiva il margine di riserva energetica (M6) per accomodare condizioni di vento contrario.
