# Analisi dei vincoli

## Metodologia del diagramma di matching {#sec:comparative-results}

Questa sezione presenta la metodologia del diagramma di matching (diagramma dei vincoli) per il dimensionamento preliminare dell'aeromobile e la applica per derivare i parametri del punto di progetto per l'UAV marziano. Il diagramma di matching visualizza tutti i vincoli di prestazioni simultaneamente, identificando lo spazio di progetto fattibile come l'intersezione di tutte le regioni accettabili [@roskamAirplaneDesign12005a].

### Riepilogo dei requisiti

Da @sec:user-needs e @sec:derived-requirements, l'UAV marziano deve soddisfare i seguenti requisiti chiave:

: Riepilogo dei requisiti di missione {#tbl:requirements-summary}

| ID | Requisito | Soglia | Motivazione |
|:---|:------------|:----------|:----------|
| OR-1 | Raggio operativo | ≥50 km | Superare la distanza totale di 35 km di Curiosity in un singolo volo |
| OR-4 | Autonomia di crociera | ≥60 min | Andata e ritorno + operazioni di rilevamento (42 min transito + 15 min rilevamento + 3 min hovering) |
| - | Capacità VTOL | Richiesta | Nessuna infrastruttura di pista su Marte |
| - | Capacità di carico | ≥0.5 kg | Payload camera + relè radio |
| N6 | Tolleranza ai guasti singoli | Richiesta | Sistema di missione senza capacità di abort |

### Fondamenti del diagramma di matching

#### Definizione degli assi

Asse orizzontale (Carico alare, $W/S$):

Il carico alare è definito come il peso dell'aeromobile per unità di superficie alare:

$$\frac{W}{S} \quad [\text{N/m}^2 \text{ o Pa}]$$

Un carico alare più alto implica una superficie alare più piccola per un dato peso, risultando in velocità di crociera e stallo più elevate, resistenza ridotta da una minore area bagnata, struttura alare più leggera, e maggiore sensibilità alle raffiche.

Asse verticale (Carico di potenza, $P/W$):

Il carico di potenza è definito come la potenza installata per unità di peso:

$$\frac{P}{W} \quad [\text{W/N o W/kg}]$$

Un carico di potenza più alto implica più potenza installata rispetto al peso, fornendo migliore velocità di salita, maggiore capacità di hovering (per configurazioni VTOL), maggiore capacità di accelerazione, e aumento della massa e del costo del sistema propulsivo.

#### Linee di vincolo

Ogni condizione di volo genera una linea di vincolo sul diagramma di matching. I punti sulla linea rappresentano il minimo $P/W$ (o massimo $W/S$) che soddisfa quel vincolo.

Vincolo di hovering (velivolo a rotore e VTOL ibrido):

Da @eq:hover-constraint in @sec:rotorcraft-analysis:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$

Questo vincolo è indipendente dal carico alare (il carico del disco $DL$ non dipende dalla superficie alare), apparendo come una linea orizzontale sul diagramma di matching. Tutti i punti sopra questa linea soddisfano il requisito di hovering.

Vincolo di crociera (ala fissa e VTOL ibrido):

Da @eq:cruise-electric-power in @sec:fixed-wing-analysis:

$$\left(\frac{P}{W}\right)_\text{crociera} = \frac{V}{(L/D) \times \eta_\text{crociera}}$$

Poiché $L/D$ dipende da $C_L$ (che varia con $W/S$ a velocità fissa), questo vincolo forma una curva con un minimo al carico alare ottimale. A $W/S$ molto basso, l'aeromobile opera ad alto $C_L$ con alta resistenza indotta; a $W/S$ molto alto, l'aeromobile deve volare più veloce, aumentando la potenza parassita. Il minimo si verifica vicino a $(L/D)_\text{max}$.

Vincolo di stallo:

Da @eq:wing-loading-constraint in @sec:fixed-wing-analysis:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

Questo vincolo stabilisce il carico alare massimo ammissibile e appare come una linea verticale sul diagramma di matching. Tutti i punti a sinistra di questa linea soddisfano il requisito di velocità minima.

Vincolo energetico (VTOL ibrido):

Il vincolo energetico da @sec:energy-constraint si manifesta come un confine della regione fattibile che accoppia il carico di potenza alla durata della missione. Un carico di potenza più alto (volo più veloce) generalmente riduce il tempo di missione ma può violare i vincoli energetici se la potenza di hovering è troppo alta.

La regione fattibile è l'intersezione di tutte le regioni accettabili: sopra il vincolo di hovering (per le configurazioni VTOL), sopra la curva del vincolo di crociera, a sinistra del vincolo di stallo, e soddisfacendo il vincolo energetico (verificato separatamente).

Il punto di progetto ottimale minimizza il carico di potenza all'interno della regione fattibile, poiché questo corrisponde a un sistema propulsivo più leggero e più efficiente. Tipicamente, il punto di progetto si trova all'intersezione di due o più vincoli attivi.

### Diagrammi di matching delle configurazioni

Prima di esaminare ogni configurazione individualmente, @fig:ld-comparison attraverso @fig:endurance-comparison presentano le metriche di prestazione chiave per tutte e tre le architetture candidate.

![Confronto dell'efficienza aerodinamica tra le configurazioni. L'L/D equivalente del velivolo a rotore di 4.0 è limitato dall'inefficienza del volo avanzato del rotore, mentre l'ala fissa raggiunge 11.7. Il VTOL ibrido raggiunge 10.5 a causa della penalità di resistenza dei rotori fermi.](figures/ld_comparison_it.png){#fig:ld-comparison width=80%}

![Confronto dei requisiti di potenza. La potenza di hovering (3178 W) è identica per velivolo a rotore e VTOL ibrido. La potenza di crociera varia con l'efficienza aerodinamica: velivolo a rotore 460 W, ala fissa 286 W, VTOL ibrido 318 W.](figures/power_comparison_it.png){#fig:power-comparison width=85%}

![Confronto dell'autonomia rispetto al requisito di 60 minuti (linea tratteggiata). Il velivolo a rotore non soddisfa marginalmente a 57 min. L'ala fissa raggiunge 151 min ma non può soddisfare il requisito VTOL. Il VTOL ibrido raggiunge 81 min con margine adeguato.](figures/endurance_comparison_it.png){#fig:endurance-comparison width=80%}

#### Analisi dei vincoli del velivolo a rotore

Per la configurazione a velivolo a rotore puro, gli assi del diagramma di matching devono essere adattati poiché non c'è ala. Il parametro rilevante è il carico del disco ($DL = T/A$) piuttosto che il carico alare. Il vincolo dominante è la potenza di hovering, che aumenta drammaticamente con il carico del disco nella rarefatta atmosfera marziana.

Lo spazio di progetto del velivolo a rotore è eliminato dalle prestazioni marginali di autonomia. Il bilancio energetico dominato dall'hovering (potenza di hovering 3178 W per 3 min consuma 158.9 Wh) lascia energia insufficiente per la crociera (459.7 W in volo avanzato). La configurazione raggiunge solo 57.27 minuti di autonomia, non soddisfacendo il requisito di 60 minuti con un margine del -4.5%.

#### Analisi dei vincoli dell'ala fissa

Per la configurazione ad ala fissa pura, il diagramma di matching mostra un vincolo di crociera come curva poco profonda con minimo al carico alare ottimale (circa 11.00 N/m² per le condizioni marziane), un vincolo di stallo come linea verticale a $W/S_\text{max}$ = 7.300 N/m² per $V_\text{min}$ = 30.00 m/s e $C_{L,\text{max}}$ = 1.200, e nessun vincolo di hovering (l'ala fissa non può effettuare hovering).

La regione fattibile esiste e offre eccellente efficienza di potenza (286.4 W in crociera a MTOW 10.00 kg). Tuttavia, questa regione è inaccessibile perché l'aeromobile non può decollare senza una pista. La distanza di corsa di decollo di circa 536 m assicura che nessun punto di progetto nella regione fattibile sia raggiungibile operativamente.

#### Analisi dei vincoli del VTOL ibrido

Per la configurazione QuadPlane, il diagramma di matching combina un vincolo di hovering come linea orizzontale a $P/W$ = 85.64 W/N (domina il diagramma), un vincolo di crociera come curva ben al di sotto del vincolo di hovering (potenza di crociera circa 10× inferiore), e un vincolo di stallo come linea verticale al carico alare massimo ammissibile (7.300 N/m²).

Il diagramma di matching per il QuadPlane traccia il carico di potenza $(P/W)$ rispetto al carico alare $(W/S)$.

Vincolo di hovering: Appare come una linea orizzontale, indipendente dal carico alare. La potenza di hovering richiesta dipende dal carico del disco e dalla densità atmosferica, non dalla dimensione dell'ala:

$$(P/W)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint-qp}

Vincolo di crociera: Appare come una curva con minimo al carico alare ottimale. A $W/S$ molto basso, la resistenza indotta è alta (alto $C_L$); a $W/S$ molto alto, l'aeromobile deve volare veloce per generare sufficiente portanza (alta $V$). Il minimo si verifica vicino a $(L/D)_\text{max}$.

Vincolo di stallo: Appare come una linea verticale al carico alare massimo ammissibile:

$$\left(\frac{W}{S}\right)_\text{max} = \frac{1}{2}\rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:stall-constraint}

Vincolo energetico: Si manifesta come un confine della regione fattibile che accoppia il carico di potenza alla durata della missione. Un carico di potenza più alto (volo più veloce) generalmente riduce il tempo di missione ma può violare i vincoli energetici se la potenza di hovering è troppo alta.

La regione fattibile si trova sopra la linea del vincolo di hovering, a sinistra del vincolo di stallo, con il vincolo energetico verificato (margine 29.7%).

Il punto di progetto è dominato dall'hovering. La potenza installata è determinata interamente dai requisiti di hovering; la potenza di crociera è abbondante. Il dimensionamento dell'ala è determinato dalle considerazioni di stallo ed efficienza aerodinamica, indipendente dalla potenza.

![Diagramma di matching (diagramma dei vincoli) per la configurazione VTOL ibrida. Il vincolo di hovering (linea rossa orizzontale) domina, stabilendo il carico di potenza minimo richiesto. Il vincolo di stallo (linea verde verticale) limita il carico alare massimo. Il vincolo di crociera (curva blu) è facilmente soddisfatto sotto la linea di hovering. Il punto di progetto (*) si trova all'intersezione dei vincoli di hovering e stallo.](figures/matching_chart_it.png){#fig:matching-chart width=90%}

### Determinazione del punto di progetto

Dall'analisi del diagramma di matching del VTOL ibrido (@fig:matching-chart), il punto di progetto del QuadPlane è caratterizzato da:

: Parametri del punto di progetto {#tbl:design-point}

| Parametro | Valore | Vincolo |
|:----------|------:|:-----------|
| Carico alare, $W/S$ | 7.300 N/m² | Fissato dal limite di stallo a $V_\text{min}$ = 30.00 m/s |
| Carico di potenza, $P/W$ | 85.64 W/N | Fissato dal requisito di hovering |
| Carico del disco, $DL$ | 30.00 N/m² | Compromesso tra dimensione del rotore e potenza |

Questi valori implicano i seguenti parametri derivati per MTOW = 10.00 kg ($W$ = 37.11 N):

: Parametri di progetto derivati {#tbl:design-parameters}

| Parametro derivato | Valore | Calcolo |
|:------------------|------:|:------------|
| Superficie alare | $S = W/(W/S) = 37.11/7.300$ | 5.083 m² |
| Apertura alare | $b = \sqrt{AR \times S}$ | 5.523 m (con AR = 6) |
| Corda media | $c = S/b$ | 0.9203 m |
| Potenza di hovering installata | $P = (P/W) \times W$ | 3178 W |
| Potenza di crociera installata | - | circa 318.5 W |

Questi valori preliminari saranno raffinati in @sec:design-decisions sulla base della selezione dettagliata dei componenti e dell'analisi dei compromessi. Il diagramma di matching fornisce punti di partenza per il progetto iterativo.

Il confronto delle configurazioni, l'eliminazione delle alternative, e la motivazione della selezione sono presentati in @sec:architecture-selection.
