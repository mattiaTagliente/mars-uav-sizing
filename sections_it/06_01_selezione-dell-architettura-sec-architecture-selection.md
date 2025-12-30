# Decisioni progettuali

## Selezione dell'architettura {#sec:architecture-selection}

Questa sezione consolida il confronto delle configurazioni dall'analisi dei vincoli (@sec:constraint-analysis), presenta la motivazione dell'eliminazione delle configurazioni alternative, e documenta l'architettura QuadPlane selezionata con le sue decisioni progettuali.

### Confronto delle configurazioni

#### Riepilogo quantitativo

@tbl:config-comparison sintetizza le analisi delle tre configurazioni candidate—velivolo a rotore (@sec:rotorcraft-analysis), ala fissa (@sec:fixed-wing-analysis), e VTOL ibrido (@sec:hybrid-vtol-analysis).

: Riepilogo del confronto delle configurazioni {#tbl:config-comparison}

| Criterio | Velivolo a rotore | Ala fissa | VTOL ibrido |
|:----------|:----------:|:----------:|:-----------:|
| **Efficienza aerodinamica** | | | |
| L/D o $(L/D)_\text{eff}$ | 4 | 15 | 13 |
| **Requisiti di potenza** | | | |
| P/W hovering (W/kg) | 246 | N.D. | 246 |
| P/W crociera (W/kg) | N.D. | 22.5 | 26 |
| Potenza di crociera (W) | 152$^a$ | 74 | 86 |
| **Capacità di missione** | | | |
| Autonomia (min) | 62 | 191 | 108 |
| Margine di autonomia | +3% | +218% | +80% |
| Raggio (km) | 142 | 459 | 252 |
| Margine di raggio | +42% | +359% | +152% |
| **Operatività** | | | |
| Capacità VTOL | ✓ Sì | ❌ No | ✓ Sì |
| Infrastruttura | Nessuna | circa 6 km pista | Nessuna |
| Capacità di planata | ❌ No | ✓ Sì | ✓ Sì$^b$ |
| **Budget di massa** | | | |
| Frazione propulsiva | circa 15% | circa 8% | circa 25% |
| Penalità di massa | N.D. | N.D. | +20% |
| **Conformità ai requisiti** | | | |
| Soddisfa autonomia | ✓ (appena) | ✓ | ✓ |
| Soddisfa raggio | ✓ | ✓ | ✓ |
| Soddisfa VTOL | ✓ | ❌ | ✓ |
| **RACCOMANDAZIONE** | ⚠️ Non raccomandato | ❌ Non fattibile | ✓ **SELEZIONATO** |

$^a$ Potenza di volo avanzato del velivolo a rotore per velocità di missione equivalente; la potenza di hovering è 812 W.
$^b$ Il QuadPlane può planare in modalità crociera se il motore di crociera si guasta, estendendo il tempo per l'atterraggio VTOL di emergenza.

#### Confronto dell'efficienza aerodinamica

: Confronto dell'efficienza aerodinamica {#tbl:aerodynamic-efficiency-comparison}

| Configurazione | Tipo L/D | Valore | Fonte |
|:--------------|:---------|------:|:-------|
| Velivolo a rotore | $(L/D)_\text{eff}$ | 4 | Analisi potenza volo avanzato (@sec:rotorcraft-analysis) |
| Ala fissa | $(L/D)$ | 15 | Polare di resistenza a $C_L$ ottimale (@sec:fixed-wing-analysis) |
| VTOL ibrido | $(L/D)$ | 13 | Crociera alare con penalità resistenza rotori (@sec:hybrid-vtol-analysis) |

Le configurazioni ad ala fissa e VTOL ibrido condividono un'efficienza di crociera simile perché il QuadPlane utilizza la portanza alare durante la crociera. La riduzione del 13% nell'L/D del QuadPlane (da 15 a 13) tiene conto della resistenza parassita dovuta ai rotori di sollevamento fermi e alla loro struttura di montaggio. Il velivolo a rotore, vincolato dal volo supportato dal rotore per l'intera missione, raggiunge solo $(L/D)_\text{eff} \approx 4$—circa un quarto dell'efficienza dell'ala fissa.

### Eliminazione delle alternative

#### Velivolo a rotore: NON RACCOMANDATO

La configurazione a velivolo a rotore puro è eliminata dalla considerazione per le seguenti ragioni:

* **Margine di sicurezza inadeguato:** Il margine di autonomia del 3% (62 min raggiunti vs 60 min richiesti) è inaccettabile per una missione senza capacità di abort. Qualsiasi deviazione dalle condizioni nominali—degradazione della batteria, variazione della densità atmosferica, inefficienza di navigazione—potrebbe comportare il fallimento della missione.

* **Alta sensibilità ai parametri:** Una riduzione del 10% della densità atmosferica (possibile durante le variazioni stagionali) aumenta i requisiti di potenza di circa il 5%, eliminando interamente il margine di autonomia.

* **Nessuna capacità di planata:** Se un rotore si guasta in volo avanzato, un multirotore non può planare per estendere il tempo per le procedure di emergenza. L'aeromobile precipita immediatamente, senza opzioni di recupero.

* **Nessun percorso di miglioramento:** A differenza delle prestazioni marginali dell'ala fissa che potrebbero essere migliorate con profili più avanzati, la limitazione del velivolo a rotore è fondamentale—$(L/D)_\text{eff} \approx 4$ è una conseguenza fisica del volo supportato dal rotore.

#### Ala fissa: NON FATTIBILE

La configurazione ad ala fissa pura è eliminata dalla considerazione perché **non può soddisfare il requisito VTOL**:

* **Requisito di pista:** La corsa di decollo è calcolata in 5-6 km, richiedendo un'infrastruttura di pista che non esiste su Marte.

* **Nessuna alternativa pratica:** Il lancio con catapulta, il decollo assistito da razzo (RATO) e il lancio con sgancio da pallone richiedono tutti un'infrastruttura sostanziale, materiali di consumo o intervento dell'equipaggio incompatibili con le operazioni autonome dall'habitat.

* **Atterraggio altrettanto problematico:** L'avvicinamento a circa 90 m/s con una corsa di atterraggio misurata in chilometri è incompatibile con terreno non preparato.

Nonostante dimostri un'efficienza aerodinamica superiore ($(L/D) = 15$) e prestazioni teoriche eccezionali (191 min di autonomia, 459 km di raggio), la configurazione ad ala fissa è **operativamente impossibile**.

### Selezione del VTOL ibrido (QuadPlane)

La configurazione VTOL ibrida è selezionata come base per l'UAV marziano perché è **l'unica architettura che soddisfa simultaneamente tutti i requisiti di missione**:

* **Capacità VTOL:** I rotori di sollevamento forniscono decollo e atterraggio verticale senza infrastruttura a terra (✓)

* **Margine di autonomia adeguato:** 108 minuti raggiunti vs 60 minuti richiesti (margine +80%) (✓)

* **Margine di raggio adeguato:** 252 km raggiunti vs 100 km richiesti (margine +152%) (✓)

* **Capacità in modalità degradata:** Se il motore di crociera si guasta, l'aeromobile può planare per estendere il tempo per l'atterraggio VTOL di emergenza, a differenza del velivolo a rotore puro che precipita immediatamente.

* **Fattibilità energetica:** 146 Wh richiesti vs 237 Wh disponibili (margine del 62% sopra il requisito).

La configurazione accetta una penalità di massa di circa il 20-25% dell'MTOW per il sistema di propulsione doppio. Questa penalità è giustificata perché:

1. Abilita la missione (nessuna alternativa per VTOL + crociera efficiente)
2. Fornisce margini di sicurezza sostanziali rispetto al velivolo a rotore
3. Mantiene opzioni di operazione in modalità degradata

### Riepilogo della configurazione

Dall'analisi del diagramma di matching (@sec:comparative-results), il punto di progetto del QuadPlane selezionato è caratterizzato da:

: Riepilogo del punto di progetto del QuadPlane {#tbl:quadplane-design-point}

| Parametro | Valore | Vincolo |
|:----------|------:|:-----------|
| Carico alare, $W/S$ | circa 17 N/m² | Tra limite di stallo e L/D ottimale |
| Carico di potenza, $P/W$ | circa 246 W/kg | Fissato dal requisito di hovering |
| Carico del disco, $DL$ | circa 30 N/m² | Compromesso tra dimensione rotore e potenza |
| MTOW | 3.3 kg | Base da @sec:initial-mass-estimate |
| Superficie alare | circa 0.72 m² | $S = W/(W/S)$ |
| Apertura alare | circa 2.9 m | $b = \sqrt{AR \times S}$ con AR = 12 |

### Motivazione della configurazione QuadPlane

L'architettura QuadPlane è selezionata per l'UAV marziano in base ai requisiti di missione e ai vincoli operativi.

#### Compatibilità con la missione

I doppi obiettivi di missione, mappatura e relè di telecomunicazione, richiedono un tempo di volo esteso su grandi aree. La crociera ad ala fissa fornisce il raggio e l'autonomia necessari, mentre la capacità VTOL consente operazioni da un sito habitat non preparato. L'architettura QuadPlane affronta direttamente entrambi i requisiti.

#### Tolleranza ai guasti

Per un UAV marziano dove la riparazione in volo è impossibile, la tolleranza ai guasti singoli è essenziale. Una configurazione di sollevamento octocopter (otto motori in quattro coppie coassiali) fornisce questa capacità: l'UAV può completare un atterraggio controllato con qualsiasi singolo motore guasto. Ogni coppia coassiale condivide un supporto strutturale, con rotori superiori e inferiori controrotanti per annullare la coppia.

Per estendere la tolleranza ai guasti singoli alla fase di crociera, viene selezionata una configurazione trattrice coassiale controrotante. Due eliche di crociera sono montate coassialmente a prua della fusoliera, azionate da motori indipendenti e rotanti in direzioni opposte. Ogni motore è dimensionato per fornire il 60% della spinta nominale di crociera, assicurando che il guasto di uno dei motori di crociera consenta alla missione di continuare con prestazioni ridotte piuttosto che richiedere un abort immediato. Il margine di spinta totale del 20% tiene conto della resistenza aggiuntiva dovuta all'elica guasta in moto libero.

Questa configurazione coassiale a prua offre diversi vantaggi rispetto alle alternative come i propulsori posteriori o le eliche wing-mounted affiancate [@roskamAirplaneDesign22004]:

* Flusso d'aria pulito: le eliche trattrici operano nell'aria indisturbata davanti alla fusoliera, portando a un'efficienza propulsiva più alta rispetto alle configurazioni a spinta dove l'elica incontra la scia turbolenta dall'intelaiatura. Questo vantaggio di efficienza è ben documentato nella letteratura di progettazione aeronautica, con le eliche a spinta che tipicamente subiscono perdite di efficienza del 2-15% a causa dell'ingestione della scia.
* Annullamento della coppia: le eliche controrotanti annullano la coppia reattiva, eliminando i momenti di imbardata asimmetrici durante la crociera e migliorando la stabilità direzionale. Questo è particolarmente vantaggioso per un veicolo che opera autonomamente senza correzione del pilota.
* Ingombro compatto: una disposizione coassiale concentra entrambe le eliche lungo l'asse della fusoliera, mantenendo un profilo aerodinamico e evitando l'interferenza aerodinamica e la complessità strutturale delle eliche wing-mounted affiancate.

Un compromesso di questa configurazione trattrice è che le camere rivolte in avanti sono ostruite dalle eliche. Per la missione di mappatura, la camera payload primaria è rivolta al nadir (verso il basso), che rimane non ostruita. I sensori di navigazione che richiedono visibilità in avanti possono essere montati sul bordo d'attacco dell'ala o utilizzare orientamenti rivolti all'indietro.

L'architettura propulsiva risultante comprende 10 motori in totale: otto motori di sollevamento in quattro coppie coassiali più due motori di crociera coassiali a prua. Questa configurazione raggiunge la piena tolleranza ai guasti singoli in tutte le fasi di volo senza fare affidamento sulla ridondanza incrociata tra sistemi (cioè, utilizzando i motori di sollevamento per il ritorno in crociera), che limiterebbe gravemente il raggio operativo a causa della minore efficienza del volo avanzato del multirotore.

#### Semplicità operativa

Rispetto ad altri approcci VTOL (tilt-rotor, tilt-wing, tail-sitter), il QuadPlane offre diversi vantaggi. La configurazione non richiede attuatori di inclinazione o componenti a geometria variabile, risultando in meccanismi più semplici con meno modalità di guasto. Hovering e crociera utilizzano sistemi propulsivi separati, disaccoppiando le modalità di volo e semplificando la progettazione del sistema di controllo. L'architettura beneficia di un'ampia heritage commerciale di volo con supporto maturo dell'autopilota, riducendo il rischio di sviluppo. Infine, i componenti sono accessibili e modulari, consentendo una manutenzione più facile. Questi fattori migliorano l'affidabilità nell'ambiente marziano dove la capacità di manutenzione è severamente limitata.

### Selezione della configurazione della coda

Sulla base dell'analisi dei compromessi, viene selezionata una configurazione a V invertita montata su boom. Questa scelta sfrutta i boom strutturali già richiesti per i motori di sollevamento dell'octocopter.

I boom dei motori di sollevamento posteriori si estendono verso poppa per supportare le superfici di coda, eliminando la necessità di una struttura di boom di coda separata e riducendo la massa strutturale complessiva. La configurazione montata su boom fornisce un braccio di momento più lungo di quello che consentirebbe una coda montata sulla fusoliera con la fusoliera compatta selezionata per questo progetto, compensando la ridotta efficacia di controllo ai numeri di Reynolds marziani. La geometria a V invertita inclina le superfici verso l'alto rispetto all'asse della fusoliera, fornendo spazio dalla superficie durante l'atterraggio su terreno irregolare. Inoltre, le superfici della coda a V sono posizionate al di fuori del getto dell'elica di crociera (configurazione trattrice a prua), assicurando un flusso d'aria indisturbato sulle superfici di controllo.

La disposizione a V invertita combina il controllo di beccheggio e imbardata in due superfici con miscelazione in stile ruddervator. Studi CFD sulle configurazioni di impennaggio montato su boom hanno trovato che i design a U invertita su boom fornivano stabilità longitudinale superiore e caratteristiche di stallo per missioni di sorveglianza [@nugrohoPerformanceAnalysisEmpennage2022], e il design a due superfici riduce il conteggio dei pezzi rispetto a una coda convenzionale a tre superfici.

Il dimensionamento delle superfici di coda per le condizioni marziane è affrontato in @sec:geometry-selection, dove i coefficienti di volume di coda e gli effetti del numero di Reynolds sono quantificati.

### Selezione della geometria della fusoliera

I benchmark commerciali mostrano un rapporto lunghezza-apertura alare che varia da 0.28 a 0.63, con una mediana di circa 0.50 (@tbl:reference-fuselage). Tuttavia, la scalatura diretta di questo rapporto alle condizioni marziane produrrebbe una fusoliera impraticabilmente grande: con l'apertura alare di 6 m richiesta per il volo marziano (derivata in @sec:geometry-selection), un rapporto di 0.50 produrrebbe una fusoliera di 3 m, che supera di gran lunga i requisiti di volume interno per un UAV da 12 kg.

Questa discrepanza nasce perché la dimensione della fusoliera è guidata principalmente dai requisiti di volume interno (batterie, payload, avionica), che non scalano con la densità atmosferica, mentre l'apertura alare è guidata dai requisiti di portanza, che scalano significativamente con la rarefatta atmosfera marziana. L'approccio corretto dimensiona la fusoliera sulla base dei requisiti funzionali piuttosto che della scalatura del rapporto.

L'MTOW target di 12 kg richiede alloggiamento per i payload (sistemi camera e radio) più le batterie; questi componenti richiedono circa 4-5 L di volume interno con margini per il routing e la gestione termica. Una lunghezza della fusoliera di 1.5-2.0 m fornisce un volume interno adeguato mantenendo un profilo aerodinamico con rapporto di finezza di 5-7 [@gottenFullConfigurationDrag2021]. Questo risulta in un rapporto lunghezza-apertura alare di circa 0.25-0.30, inferiore ai benchmark commerciali ma coerente con i vincoli di scalatura specifici per Marte.

La lunghezza della fusoliera selezionata fornisce un braccio di momento adeguato per le superfici di coda montate su boom quando combinata con i boom strutturali che si estendono verso poppa, raggiungendo la stabilità longitudinale e direzionale richiesta senza un'area eccessiva delle superfici di coda.

La sezione trasversale della fusoliera e il dimensionamento dettagliato sono affrontati in @sec:geometry-selection.

### Selezione dei materiali

Il polimero rinforzato con fibra di carbonio (CFRP) è selezionato come materiale strutturale primario, coerentemente con l'heritage di Ingenuity e la pratica commerciale.

Il CFRP presenta bassa espansione termica (CTE circa 0.5 ppm/°C), minimizzando le sollecitazioni termiche dal ciclo di temperatura diurno da −80°C a +20°C su Marte. Fornisce il più alto rapporto resistenza-peso tra i materiali strutturali comunemente disponibili, supportando la minimizzazione della massa critica per il volo marziano. L'elicottero Ingenuity ha dimostrato con successo la costruzione in CFRP su Marte, utilizzando tessuti in carbonio a tow distribuito TeXtreme® selezionati per la resistenza alle microfessurazioni da ciclo termico [@latourabOxeonPartOwnedHoldings2025].

Le pelli dell'ala e della fusoliera utilizzeranno una costruzione sandwich con nucleo in schiuma e facce in fibra di carbonio, fornendo alta rigidezza-peso per le superfici aerodinamiche primarie. I boom dei motori di sollevamento e del supporto della coda saranno tubi in fibra di carbonio, avvolti a filamento o pultrusi. Il rinforzo in fibra di vetro sarà utilizzato nei punti di attacco del carrello di atterraggio e sui bordi d'attacco vulnerabili per la tolleranza agli impatti. La gestione termica interna utilizzerà superfici interne placcate in oro o isolamento multistrato per il controllo termico del compartimento elettronica, seguendo la pratica di Ingenuity.

Le implicazioni della selezione dei materiali per la frazione di massa strutturale sono affrontate in @sec:material-selection.

![Concetto proposto di QuadPlane con configurazione di sollevamento octocopter ed eliche di crociera trattrici coassiali.](figures/our_proposal_concept.jpg){#fig:concept-architecture width=70%}
