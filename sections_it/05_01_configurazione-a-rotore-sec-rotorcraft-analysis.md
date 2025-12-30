# Analisi dei vincoli

## Configurazione a rotore {#sec:rotorcraft-analysis}

Questa sezione valuta se una configurazione a rotore puro (elicottero o multirotore) può soddisfare i requisiti di missione dell'UAV marziano. L'analisi sviluppa il quadro teorico per la potenza di hovering, la potenza in volo avanzato e l'autonomia, culminando in una valutazione di fattibilità rispetto al requisito di autonomia di 60 minuti.

### Analisi della potenza di hovering

#### Fondamenti della teoria della quantità di moto {#sec:momentum-theory}

Le prestazioni del rotore in hovering sono analizzate utilizzando la teoria della quantità di moto di Rankine-Froude, che tratta il rotore come un disco attuatore infinitamente sottile che trasferisce quantità di moto all'aria che lo attraversa [@leishmanPrinciplesHelicopterAerodynamics2006]. Questo modello idealizzato, nonostante la sua semplicità, fornisce intuizioni sulle prestazioni del rotore e sulla relazione tra spinta, potenza e carico del disco.

La teoria della quantità di moto fa le seguenti assunzioni: flusso uniforme e stazionario attraverso il disco del rotore; flusso non viscoso senza rotazione nella scia; condizioni incomprimibili (valide per $M < 0.3$); e flusso unidimensionale attraverso un getto ben definito.

Dal principio di conservazione della quantità di moto del fluido, la spinta del rotore eguaglia la variazione temporale della quantità di moto dell'aria che passa attraverso il disco del rotore. Per un rotore in hovering con velocità indotta $v_i$ al piano del disco, la spinta è [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$T = \dot{m} \cdot w = 2\rho A v_i^2$$ {#eq:thrust-momentum}

dove $\dot{m} = \rho A v_i$ è la portata massica attraverso il disco, $w = 2v_i$ è la velocità della scia a valle (dalla conservazione dell'energia), $\rho$ è la densità dell'aria, e $A$ è l'area del disco del rotore.

Risolvendo @eq:thrust-momentum per la velocità indotta al disco del rotore si ottiene [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$v_i = \sqrt{\frac{T}{2\rho A}}$$ {#eq:induced-velocity}

Questo risultato fondamentale mostra che la velocità indotta scala con la radice quadrata della spinta e inversamente con l'area del disco e la densità. La velocità indotta può anche essere espressa in termini di carico del disco ($DL = T/A$):

$$v_i = \sqrt{\frac{DL}{2\rho}}$$ {#eq:induced-velocity-dl}

La potenza ideale richiesta per l'hovering è il prodotto di spinta e velocità indotta [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{ideale} = T \cdot v_i = T \sqrt{\frac{T}{2\rho A}}$$ {#eq:ideal-power-1}

Riarrangiando:

$$P_\text{ideale} = \frac{T^{3/2}}{\sqrt{2\rho A}}$$ {#eq:ideal-power}

Questa equazione rivela relazioni di scala: la potenza scala come $T^{3/2}$, il che significa che la potenza di hovering aumenta più rapidamente della spinta; la potenza scala come $\rho^{-1/2}$, quindi la bassa densità atmosferica aumenta sostanzialmente i requisiti di potenza; e la potenza scala come $A^{-1/2}$, favorendo grandi aree del disco del rotore.

Per il volo in hovering dove la spinta eguaglia il peso ($T = W$):

$$P_\text{ideale} = \frac{W^{3/2}}{\sqrt{2\rho A}} = W \sqrt{\frac{DL}{2\rho}} = W \sqrt{\frac{W/A}{2\rho}}$$ {#eq:ideal-power-weight}

#### Figura di merito {#sec:figure-of-merit}

Il risultato della teoria della quantità di moto rappresenta un limite inferiore idealizzato sulla potenza di hovering. I rotori reali subiscono perdite aggiuntive dovute alla resistenza di profilo sulle sezioni delle pale, alla distribuzione non uniforme del flusso indotto, alle perdite di estremità (effetti di pala finita) e alla rotazione nella scia.

La figura di merito (FM) quantifica l'efficienza di un rotore reale rispetto alla previsione ideale della teoria della quantità di moto [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$FM = \frac{P_\text{ideale}}{P_\text{reale}} < 1$$ {#eq:figure-of-merit}

Riarrangiando per ottenere la potenza di hovering reale:

$$P_\text{hover} = \frac{P_\text{ideale}}{FM} = \frac{T^{3/2}}{FM \cdot \sqrt{2\rho A}}$$ {#eq:hover-power}

La figura di merito adottata per il dimensionamento dei velivoli a rotore marziani ($FM$ = 0.4000) è documentata in @sec:propulsion-efficiency, rappresentando una stima conservativa nell'intervallo atteso di 0.30-0.50 per l'operazione di rotori MAV a basso Reynolds.

#### Requisiti di potenza elettrica

La potenza elettrica prelevata dalla batteria deve tenere conto delle perdite nel motore e nel regolatore elettronico di velocità (ESC):

$$P_\text{elettrica,hover} = \frac{P_\text{hover}}{\eta_\text{motore} \cdot \eta_\text{ESC}}$$ {#eq:electric-hover}

Sostituendo l'equazione della potenza di hovering:

$$P_\text{elettrica,hover} = \frac{W^{3/2}}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC} \cdot \sqrt{2\rho A}}$$ {#eq:electric-hover-full}

La catena di efficienza combinata dalla batteria alla spinta del rotore è data da @eq:hover-efficiency:

$$\eta_\text{hover} = FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}$$

Utilizzando i valori di efficienza da @tbl:efficiency-parameters ($FM$ = 0.4000, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza combinata di hovering è $\eta_\text{hover}$ = 0.3230.

Questo significa che solo il 32% dell'energia elettrica dalla batteria produce potenza di spinta utile in hovering. Il restante 68% è perso per resistenza di profilo del rotore, effetti di flusso indotto non ideali, perdite nel rame e nel ferro del motore, e perdite di commutazione dell'ESC.

#### Vincolo di carico di potenza

Il carico di potenza (spinta per unità di potenza) per l'hovering può essere espresso riarrangiando @eq:hover-power:

$$\frac{P_\text{hover}}{W} = \frac{1}{FM} \cdot \sqrt{\frac{W/A}{2\rho}} = \frac{1}{FM} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-power-loading}

Questa equazione definisce il vincolo di hovering sul diagramma di matching. Per un dato carico del disco e densità atmosferica, il rapporto potenza-peso richiesto è fisso e indipendente dal carico alare. Su un diagramma di matching con P/W sull'asse verticale e W/S sull'asse orizzontale, il vincolo di hovering appare come una linea orizzontale.

Includendo la catena di efficienza elettrica:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint}

### Prestazioni in volo avanzato

#### Componenti di potenza in volo avanzato

In volo avanzato, la potenza totale richiesta da un velivolo a rotore comprende molteplici componenti [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{totale} = P_i + P_0 + P_p + P_c$$ {#eq:forward-power-components}

dove $P_i$ è la potenza indotta (per generare portanza), $P_0$ è la potenza di profilo (per vincere la resistenza della sezione della pala), $P_p$ è la potenza parassita (per vincere la resistenza della fusoliera e del mozzo), e $P_c$ è la potenza di salita (per cambiare l'energia potenziale gravitazionale).

Per il volo di crociera livellato ($P_c = 0$), la ripartizione della potenza segue uno schema caratteristico: a basse velocità, la potenza indotta domina (simile all'hovering); all'aumentare della velocità, la potenza indotta diminuisce (il rotore agisce più come un'ala); e ad alte velocità, la potenza parassita domina (scala come $V^3$).

La velocità di potenza minima si verifica dove la somma di queste componenti raggiunge un minimo, tipicamente a un rapporto di avanzamento $\mu = V/(\Omega R) \approx 0.15$-0.25.

#### Rapporto portanza-resistenza equivalente

Per il confronto con aeromobili ad ala fissa, l'efficienza del volo avanzato del velivolo a rotore può essere espressa come un rapporto portanza-resistenza equivalente [@leishmanPrinciplesHelicopterAerodynamics2006, Capitolo 1]:

$$\left(\frac{L}{D}\right)_\text{eff} = \frac{W \cdot V}{P_\text{totale}}$$ {#eq:equivalent-ld}

Questo parametro rappresenta l'efficienza aerodinamica complessiva del velivolo a rotore in volo avanzato, incorporando tutte le perdite di potenza. Riarrangiando:

$$P_\text{avanzato} = \frac{W \cdot V}{(L/D)_\text{eff}}$$ {#eq:forward-power-ld}

I valori tipici di L/D equivalente sono riassunti in @tbl:rotorcraft-ld. L'efficienza aerodinamica relativamente scarsa deriva da diversi fattori inerenti ai velivoli a rotore: il mozzo del rotore e gli attacchi delle pale creano una sostanziale resistenza parassita; la resistenza di profilo sulle sezioni delle pale è inevitabile, anche ad alta velocità; la pala avanzante subisce effetti di comprimibilità ad alta velocità; e la pala retrocedente può subire stallo, limitando la velocità di avanzamento.

Per un velivolo a rotore marziano senza ala, l'L/D equivalente è $(L/D)_\text{eff}$ = 4.000, rappresentando l'estremo inferiore della gamma degli elicotteri a causa dell'assenza dell'ottimizzazione progettuale presente negli elicotteri terrestri (secondo @sec:rotorcraft-ld).

#### Potenza elettrica in volo avanzato

Includendo la catena di efficienza elettrica, la potenza dalla batteria per il volo avanzato è:

$$P_\text{elettrica,avanzato} = \frac{W \cdot V}{(L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC}}$$ {#eq:forward-electric-power}

### Analisi dell'autonomia

#### Modello dell'energia della batteria

L'energia utilizzabile dalla batteria è derivata da @eq:battery-energy-fraction in @sec:battery-utilisation:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Sostituendo i valori dei parametri da @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) e @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500):

$$\frac{E_\text{disponibile}}{MTOW} = 0.3500 \times 270.0 \times 0.8000 \times 0.9500 = 71.82 \text{ Wh/kg}$$

Per l'MTOW di base = 10.00 kg:

$$E_\text{disponibile} = 71.82 \times 10.00 = 718.2 \text{ Wh}$$

#### Equazione dell'autonomia del velivolo a rotore

Per un velivolo a rotore in volo avanzato, l'autonomia è determinata dall'energia disponibile e dal consumo di potenza:

$$t_\text{autonomia} = \frac{E_\text{disponibile}}{P_\text{elettrica,avanzato}}$$ {#eq:endurance-definition}

Sostituendo le espressioni per l'energia disponibile (@eq:battery-energy-fraction) e la potenza di volo avanzato (@eq:forward-electric-power):

$$t_\text{autonomia} = \frac{f_\text{batt} \cdot MTOW \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt}}{W \cdot V / ((L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC})}$$ {#eq:endurance-expanded}

Poiché $W = MTOW \cdot g_\text{Marte}$, i termini MTOW si cancellano:

$$t_\text{autonomia} = \frac{f_\text{batt} \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt} \cdot (L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC}}{g_\text{Marte} \cdot V}$$ {#eq:endurance-simple}

Questo risultato mostra che l'autonomia del velivolo a rotore è indipendente dall'MTOW (per frazioni di massa fisse). L'autonomia dipende dai parametri della batteria ($f_\text{batt}$, $e_\text{spec}$, $DoD$, $\eta_\text{batt}$), dall'efficienza aerodinamica ($(L/D)_\text{eff}$), dall'efficienza propulsiva ($\eta_\text{motore}$, $\eta_\text{ESC}$), e dalle condizioni di volo ($g_\text{Marte}$, $V$).

#### Calcolo dell'autonomia

Utilizzando i valori dei parametri da @sec:derived-requirements:

: Parametri per il calcolo dell'autonomia del velivolo a rotore {#tbl:endurance-parameters}

| Parametro | Simbolo | Valore | Unità |
|:----------|:------:|------:|:-----|
| Frazione batteria | $f_\text{batt}$ | 0.3500 | - |
| Energia specifica | $e_\text{spec}$ | 270.0 | Wh/kg |
| Profondità di scarica | $DoD$ | 0.8000 | - |
| Efficienza batteria | $\eta_\text{batt}$ | 0.9500 | - |
| L/D equivalente | $(L/D)_\text{eff}$ | 4.000 | - |
| Efficienza motore | $\eta_\text{motore}$ | 0.8500 | - |
| Efficienza ESC | $\eta_\text{ESC}$ | 0.9500 | - |
| Gravità marziana | $g_\text{Marte}$ | 3.711 | m/s² |
| Velocità di crociera | $V$ | 40.00 | m/s |

Convertendo l'energia specifica in J/kg: $e_\text{spec} = 270.0 \times 3600 = 972000$ J/kg

Sostituendo in @eq:endurance-simple:

$$t_\text{autonomia} = \frac{0.3500 \times 972000 \times 0.8000 \times 0.9500 \times 4.000 \times 0.8500 \times 0.9500}{3.711 \times 40.00}$$

$$t_\text{autonomia} = \frac{849706}{148.44} = 5723 \text{ s} = 95.39 \text{ min}$$ {#eq:endurance-result}

Questo calcolo rappresenta l'autonomia massima teorica assumendo che il 100% del tempo di volo sia trascorso in crociera efficiente in avanzamento. L'autonomia pratica è inferiore a causa delle fasi di hovering e dei requisiti di riserva, come analizzato nella valutazione di fattibilità sottostante.

### Valutazione di fattibilità

#### Analisi critica dell'autonomia del velivolo a rotore

L'autonomia teorica di 95.39 minuti calcolata sopra supera il requisito di 60 minuti, ma diversi fattori riducono l'autonomia raggiungibile per una missione con velivolo a rotore puro.

Un velivolo a rotore puro non può utilizzare la crociera ad ala fissa. L'$(L/D)_\text{eff}$ = 4.000 si applica al volo avanzato dell'elicottero, che è meno efficiente della crociera ad ala fissa.

Il profilo di missione richiede hovering per decollo, atterraggio e contingenza. Utilizzando @eq:hover-power e l'efficienza di hovering di 0.3230, il consumo di potenza in hovering supera la potenza di crociera. Per l'MTOW di base = 10.00 kg con carico del disco $DL$ = 30.00 N/m² e densità marziana $\rho$ = 0.01960 kg/m³, la velocità indotta è:

$$v_i = \sqrt{\frac{30.00}{2 \times 0.01960}} = \sqrt{765.3} = 27.68 \text{ m/s}$$

Il requisito di potenza di hovering è:

$$P_\text{hover} = \frac{W \cdot v_i}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}} = \frac{37.11 \times 27.68}{0.4000 \times 0.8500 \times 0.9500} = 3178 \text{ W}$$

Questa velocità indotta è dello stesso ordine di grandezza della velocità di crociera, e la potenza di hovering (3178 W) supera la potenza di crociera (circa 459.7 W), consumando energia significativa durante le fasi di hovering di 3 minuti.

La riserva energetica del 20% riduce l'autonomia effettiva.

Un aeromobile ad ala fissa raggiunge $(L/D) \approx 12$, circa tre volte superiore al velivolo a rotore. Questa differenza limita il raggio d'azione e l'autonomia del velivolo a rotore.

#### Confronto con i requisiti di missione

@tbl:rotorcraft-feasibility confronta la capacità del velivolo a rotore puro con i requisiti di missione:

: Valutazione di fattibilità del velivolo a rotore {#tbl:rotorcraft-feasibility}

| Requisito | Obiettivo | Capacità velivolo a rotore | Stato |
|:------------|:-------|:----------------------|:------:|
| Autonomia di crociera | ≥60 min | 57 min (con riserva 20%) | NON CONFORME |
| Raggio operativo | ≥50 km | 65 km (130 km raggio) | CONFORME |
| Capacità VTOL | Richiesta | Sì, intrinseca | CONFORME |
| Tempo di hovering | 3 min | Illimitato (limitato dalla potenza) | CONFORME |

L'energia utilizzabile è 718.2 Wh × 0.80 (riserva) = 574.6 Wh. L'energia di hovering (3 min a 3178 W) consuma 158.9 Wh, lasciando 415.7 Wh per il volo avanzato. La potenza di volo avanzato è $P = WV/(L/D)_\text{eff}/\eta = 37.11 \times 40.00 / (4.000 \times 0.8075) = 459.7$ W. Il tempo di volo avanzato è 415.7 Wh / 459.7 W = 0.904 h = 54.27 min. Autonomia totale: 57.27 min. Raggio: 40.00 m/s × 54.27 min × 60 s/min = 130.2 km.

La configurazione a velivolo a rotore non soddisfa il requisito di autonomia (57 min vs 60 min richiesti). Anche se soddisfacesse marginalmente il requisito, il margine sarebbe insufficiente:

#### Analisi di sensibilità

L'autonomia di 57.27 minuti rappresenta un margine del -4.5% al di sotto del requisito di 60 minuti, che è inaccettabile per una missione marziana.

Una volta che l'UAV parte dall'habitat, deve completare la missione. Non esiste un sito di atterraggio alternativo.

La densità atmosferica marziana varia con la stagione e il carico di polvere. Una riduzione del 10% della densità aumenta i requisiti di potenza di circa il 5%, degradando ulteriormente le prestazioni.

Le batterie al litio perdono capacità nel corso dei cicli di carica e nel freddo estremo. La degradazione della capacità riduce ulteriormente l'autonomia già insufficiente.

Se un rotore si guasta, un multirotore non può planare verso un atterraggio sicuro.

Per confronto, la configurazione VTOL ibrida raggiunge 91 minuti di autonomia (+52% di margine), fornendo un maggiore margine operativo. L'analisi della configurazione e la motivazione della selezione sono presentate in @sec:architecture-selection.

### Conclusione sulla configurazione a velivolo a rotore

La configurazione a velivolo a rotore puro non soddisfa il requisito minimo di autonomia (57.27 min vs 60 min richiesti), con un margine del -4.5% che è inaccettabile per le operazioni di missione. La configurazione presenta rischi operativi.

L'autonomia raggiungibile di 57.27 minuti è inferiore al requisito di 60 minuti di 2.73 minuti.

Qualsiasi variazione nella densità atmosferica, nella capacità della batteria o nei valori di efficienza degrada ulteriormente le prestazioni.

A differenza di un VTOL ibrido che può planare se il motore di crociera si guasta, un velivolo a rotore precipita immediatamente se qualsiasi rotore si guasta.

La limitazione fondamentale è il basso rapporto portanza-resistenza equivalente inerente ai velivoli a rotore in volo avanzato ($(L/D)_\text{eff} \approx 4$), che comporta un consumo di potenza in volo avanzato (460 W) circa il 45% superiore alla crociera del VTOL ibrido (318 W).

La valutazione di fattibilità per la configurazione a velivolo a rotore è riassunta in @tbl:rotorcraft-feasibility. Il confronto delle configurazioni e la motivazione della selezione sono presentati in @sec:architecture-selection.
