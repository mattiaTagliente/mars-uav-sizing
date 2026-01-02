# Decisioni progettuali

## Selezione dell'architettura {#sec:architecture-selection}

Questa sezione consolida il confronto delle configurazioni dall'analisi dei vincoli (@sec:constraint-analysis), presenta la motivazione dell'eliminazione delle configurazioni alternative, e documenta l'architettura QuadPlane selezionata con le sue decisioni progettuali.

### Confronto delle configurazioni

#### Riepilogo quantitativo

@tbl:config-comparison sintetizza le analisi delle tre configurazioni candidate, velivolo a rotore (@sec:rotorcraft-analysis), ala fissa (@sec:fixed-wing-analysis), e VTOL ibrido (@sec:hybrid-vtol-analysis).

: Riepilogo del confronto delle configurazioni {#tbl:config-comparison}

| Criterio | Velivolo a rotore | Ala fissa | VTOL ibrido |
|:----------|:----------:|:----------:|:-----------:|
| Efficienza aerodinamica | | | |
| L/D o $(L/D)_	ext{eff}$ | 4.0 | 11.7 | 10.5 |
| Requisiti di potenza | | | |
| P/W hovering (W/N) | 85.7 | N.D. | 85.7 |
| P/W crociera (W/N) | 12.4$^a$ | 7.7 | 8.6 |
| Potenza di crociera (W) | 460$^a$ | 286 | 318 |
| Capacità di missione | | | |
| Autonomia (min) | 63.17 | 120.5 | 89.55 |
| Margine di autonomia | +5.284% | +100.8% | +49.26% |
| Raggio (km) | 146.8 | 289 | 207.7 |
| Margine di raggio | +46.81% | +189% | +107.7% |
| Operatività | | | |
| Capacità VTOL | Sì | No | Sì |
| Infrastruttura | Nessuna | Circa 1 km pista | Nessuna |
| Capacità di planata | No | Sì | Sì$^b$ |
| Budget di massa | | | |
| Frazione propulsiva | circa 15% | circa 8% | circa 25% |
| Penalità di massa | N.D. | N.D. | +17% |
| Conformità ai requisiti | | | |
| Soddisfa autonomia | Sì (marginale) | Sì | Sì |
| Soddisfa raggio | Sì | Sì | Sì |
| Soddisfa VTOL | Sì | No | Sì |
| Raccomandazione | Non raccomandato | Non fattibile | SELEZIONATO |

$^a$ Potenza di volo avanzato del velivolo a rotore per velocità di missione equivalente; la potenza di hovering è 3178 W.
$^b$ Il QuadPlane può planare in modalità crociera se il motore di crociera si guasta, estendendo il tempo per l'atterraggio VTOL di emergenza.

#### Confronto dell'efficienza aerodinamica

: Confronto dell'efficienza aerodinamica {#tbl:aerodynamic-efficiency-comparison}

| Configurazione | Tipo L/D | Valore | Fonte |
|:--------------|:---------|------:|:-------|
| Velivolo a rotore | $(L/D)_\text{eff}$ | 4 | Analisi potenza volo avanzato (@sec:rotorcraft-analysis) |
| Ala fissa | $(L/D)$ | 11.7 | Polare di resistenza a $C_L$ ottimale (@sec:fixed-wing-analysis) |
| VTOL ibrido | $(L/D)$ | 10.5 | Crociera alare con penalità resistenza rotori (@sec:hybrid-vtol-analysis) |

Le configurazioni ad ala fissa e VTOL ibrido condividono un'efficienza di crociera simile perché il QuadPlane utilizza la portanza alare durante la crociera. La riduzione del 10% nell'L/D del QuadPlane (da 11.7 a 10.5) tiene conto della resistenza parassita dovuta ai rotori di sollevamento fermi e alla loro struttura di montaggio. Il velivolo a rotore, vincolato dal volo supportato dal rotore per l'intera missione, raggiunge solo $(L/D)_\text{eff} \approx 4$, circa un terzo dell'efficienza dell'ala fissa.

### Eliminazione delle alternative

#### Velivolo a rotore: NON RACCOMANDATO

La configurazione a velivolo a rotore puro è eliminata dalla considerazione per le seguenti ragioni:

* Margine di autonomia limitato: il margine di autonomia del +5.284% (63.17 min raggiunti vs 60 min richiesti) è insufficiente per una missione senza capacità di abort. Qualsiasi deviazione dalle condizioni nominali, degradazione della batteria, variazione della densità atmosferica, o inefficienza di navigazione potrebbe comportare il fallimento della missione.

* Alta sensibilità ai parametri: una riduzione del 10% della densità atmosferica (possibile durante le variazioni stagionali) aumenta i requisiti di potenza di circa il 5%, eliminando interamente il margine di autonomia.

* Nessuna capacità di planata: se un rotore si guasta in volo avanzato, un multirotore non può planare per estendere il tempo per le procedure di emergenza. L'aeromobile precipita immediatamente, senza opzioni di recupero.

* Nessun percorso di miglioramento: a differenza delle prestazioni marginali dell'ala fissa che potrebbero essere migliorate con profili più avanzati, la limitazione del velivolo a rotore è fondamentale, $(L/D)_\text{eff} \approx 4$ è una conseguenza fisica del volo supportato dal rotore.

#### Ala fissa: NON FATTIBILE

La configurazione ad ala fissa pura è eliminata dalla considerazione perché non può soddisfare il requisito VTOL:

* Requisito di pista: la corsa di decollo è calcolata in circa 1060 m, richiedendo un'infrastruttura di pista che non esiste su Marte.

* Nessuna alternativa pratica: il lancio con catapulta, il decollo assistito da razzo (RATO) e il lancio con sgancio da pallone richiedono tutti un'infrastruttura sostanziale, materiali di consumo o intervento dell'equipaggio incompatibili con le operazioni autonome dall'habitat.

* Atterraggio altrettanto problematico: l'avvicinamento a circa 45.5 m/s con una corsa di atterraggio misurata in centinaia o migliaia di metri è incompatibile con terreno non preparato.

Nonostante dimostri un'efficienza aerodinamica superiore ($(L/D) = 11.7$) e prestazioni teoriche elevate (120.5 min di autonomia, 289 km di raggio), la configurazione ad ala fissa è operativamente impossibile.

### Selezione del VTOL ibrido (QuadPlane)

La configurazione VTOL ibrida è selezionata come base per l'UAV marziano perché è l'unica architettura che soddisfa simultaneamente tutti i requisiti di missione:

* Capacità VTOL: i rotori di sollevamento forniscono decollo e atterraggio verticale senza infrastruttura a terra.

* Margine di autonomia adeguato: 89.55 minuti raggiunti vs 60 minuti richiesti (margine +49.26%).

* Margine di raggio adeguato: 207.7 km raggiunti vs 100 km richiesti (margine +107.7%).

* Capacità in modalità degradata: se il motore di crociera si guasta, l'aeromobile può planare per estendere il tempo per l'atterraggio VTOL di emergenza, a differenza del velivolo a rotore puro che precipita immediatamente.

* Fattibilità energetica: 501.6 Wh richiesti vs 718.2 Wh disponibili (margine del +43.20% sopra il requisito).

La configurazione accetta una penalità di massa di circa il 17% dell'MTOW per il sistema di propulsione doppio. Questa penalità è giustificata perché:

1. Abilita la missione (nessuna alternativa per VTOL + crociera efficiente)
2. Fornisce margini di sicurezza sostanziali rispetto al velivolo a rotore
3. Mantiene opzioni di operazione in modalità degradata

### Riepilogo della configurazione

Dall'analisi del diagramma di matching (@sec:comparative-results), il punto di progetto del QuadPlane selezionato è caratterizzato da:

: Riepilogo del punto di progetto del QuadPlane {#tbl:quadplane-design-point}

| Parametro | Valore | Vincolo |
|:----------|------:|:-----------|
| Carico alare, $W/S$ | 13.82 N/m² | Fissato dal limite di stallo a $V_\text{min}$ = 35.04 m/s |
| Carico di potenza, $P/W$ | 85.71 W/N | Fissato dal requisito di hovering |
| Carico del disco, $DL$ | 30.00 N/m² | Compromesso tra dimensione rotore e potenza |
| MTOW | 10.00 kg | Base da @sec:initial-mass-estimate |
| Superficie alare | 2.686 m² | $S = W/(W/S)$ |
| Apertura alare | 4.01 m | $b = \sqrt{AR \times S}$ con AR = 6 |

### Motivazione della configurazione QuadPlane

L'architettura QuadPlane è selezionata per l'UAV marziano in base ai requisiti di missione e ai vincoli operativi.

#### Compatibilità con la missione

I doppi obiettivi di missione, mappatura e relè di telecomunicazione, richiedono un tempo di volo esteso su grandi aree. La crociera ad ala fissa fornisce il raggio e l'autonomia necessari, mentre la capacità VTOL consente operazioni da un sito habitat non preparato. L'architettura QuadPlane affronta direttamente entrambi i requisiti.

#### Tolleranza ai guasti

Per un UAV marziano dove la riparazione in volo è impossibile, la tolleranza ai guasti singoli è essenziale. Una configurazione di sollevamento octocopter (otto motori in quattro coppie coassiali) fornisce questa capacità: l'UAV può completare un atterraggio controllato con qualsiasi singolo motore guasto. Ogni coppia coassiale condivide un supporto strutturale, con rotori superiori e inferiori controrotanti per annullare la coppia.

Per estendere la tolleranza ai guasti singoli alla fase di crociera, viene selezionata una configurazione traente coassiale controrotante. Due eliche di crociera sono montate coassialmente a prua della fusoliera, azionate da motori indipendenti e rotanti in direzioni opposte. Ogni motore è dimensionato per fornire il 60% della spinta nominale di crociera, assicurando che il guasto di uno dei motori di crociera consenta alla missione di continuare con prestazioni ridotte piuttosto che richiedere un abort immediato. Il margine di spinta totale del 20% tiene conto della resistenza aggiuntiva dovuta all'elica guasta in moto libero.

Questa configurazione coassiale a prua offre diversi vantaggi rispetto alle alternative come i propulsori posteriori o le eliche wing-mounted affiancate [@roskamAirplaneDesign22004]<!-- #s:tractor-pusher -->:

* Flusso d'aria pulito: le eliche traenti operano nell'aria indisturbata davanti alla fusoliera, portando a un'efficienza propulsiva più alta rispetto alle configurazioni a spinta dove l'elica incontra la scia turbolenta dall'intelaiatura. Questo vantaggio di efficienza è ben documentato nella letteratura di progettazione aeronautica, con le eliche a spinta che tipicamente subiscono perdite di efficienza del 2-15% a causa dell'ingestione della scia.
* Annullamento della coppia: le eliche controrotanti annullano la coppia reattiva, eliminando i momenti di imbardata asimmetrici durante la crociera e migliorando la stabilità direzionale. Questo è particolarmente vantaggioso per un veicolo che opera autonomamente senza correzione del pilota.
* Ingombro compatto: una disposizione coassiale concentra entrambe le eliche lungo l'asse della fusoliera, mantenendo un profilo aerodinamico e evitando l'interferenza aerodinamica e la complessità strutturale delle eliche wing-mounted affiancate.

Un compromesso di questa configurazione traente è che le camere rivolte in avanti sono ostruite dalle eliche. Per la missione di mappatura, la camera payload primaria è rivolta al nadir (verso il basso), che rimane non ostruita. I sensori di navigazione che richiedono visibilità in avanti possono essere montati sul bordo d'attacco dell'ala o utilizzare orientamenti rivolti all'indietro.

L'architettura propulsiva risultante comprende 10 motori in totale: otto motori di sollevamento in quattro coppie coassiali più due motori di crociera coassiali a prua. Questa configurazione raggiunge la piena tolleranza ai guasti singoli in tutte le fasi di volo senza fare affidamento sulla ridondanza incrociata tra sistemi (cioè, utilizzando i motori di sollevamento per il ritorno in crociera), che limiterebbe gravemente il raggio operativo a causa della minore efficienza del volo avanzato del multirotore.

#### Semplicità operativa

Rispetto ad altri approcci VTOL (tilt-rotor, tilt-wing, tail-sitter), il QuadPlane offre diversi vantaggi. La configurazione non richiede attuatori di inclinazione o componenti a geometria variabile, risultando in meccanismi più semplici con meno modalità di guasto. Hovering e crociera utilizzano sistemi propulsivi separati, disaccoppiando le modalità di volo e semplificando la progettazione del sistema di controllo. L'architettura beneficia di un'ampia heritage commerciale di volo con supporto maturo dell'autopilota, riducendo il rischio di sviluppo. Infine, i componenti sono accessibili e modulari, consentendo una manutenzione più facile. Questi fattori migliorano l'affidabilità nell'ambiente marziano dove la capacità di manutenzione è severamente limitata.

![Concetto di QuadPlane proposto, con configurazione di sollevamento octocopter ed eliche di crociera traenti coassiali.](figures/shared/our_proposal_concept.jpg){#fig:concept-architecture width=70%}
