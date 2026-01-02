# Metodologia di progettazione

## Ruolo del dimensionamento basato sui vincoli {#sec:constraint-role}

Il diagramma di vincolo, o matching chart, costituisce il nucleo analitico della metodologia di dimensionamento. Questo strumento grafico, adattato dai metodi di dimensionamento aeronautico basati sulla potenza, visualizza i vincoli che delimitano lo spazio di progettazione ammissibile.

### Spazi di vincolo specifici per configurazione

Diverse configurazioni di aeromobili richiedono formulazioni del diagramma di vincolo differenti, che riflettono i loro diversi fattori prestazionali:

* Configurazioni ad ala rotante utilizzano un diagramma di vincolo con il carico di potenza (P/W) sull'asse verticale e il carico del disco (DL = T/A) sull'asse orizzontale. Poiché i velivoli ad ala rotante non hanno ali, il carico alare non è un parametro significativo. Il vincolo di potenza in hovering domina, con il carico di potenza che aumenta monotonicamente con il carico del disco secondo la teoria del disco attuatore.

* Configurazioni ad ala fissa utilizzano il carico di potenza (P/W) in funzione del carico alare (W/S). Il vincolo di stallo appare come una linea verticale che limita il carico alare massimo, mentre il vincolo di crociera appare come una curva con potenza minima al carico alare ottimale. Non esiste alcun vincolo di hovering poiché gli aeromobili ad ala fissa non possono eseguire il volo stazionario.

* Configurazioni VTOL ibride (QuadPlane) combinano elementi di entrambe: il carico alare si applica alla fase di crociera mentre il carico del disco si applica alla fase di hovering. Il diagramma di vincolo utilizza gli assi P/W rispetto a W/S, con il vincolo di hovering che appare come una linea orizzontale (indipendente dal carico alare) e i vincoli di crociera e stallo come per l'ala fissa.

Questo approccio specifico per configurazione garantisce che ogni architettura sia valutata nel suo spazio di vincolo naturale, consentendo un confronto significativo dei margini di fattibilità.

### Vincoli del VTOL ibrido

Per un aeromobile VTOL ibrido, che emerge come la configurazione più adatta dall'analisi dei trade-off (@sec:architecture-selection), i vincoli rilevanti includono:

* Vincolo di hovering: stabilisce il carico di potenza minimo in base al carico del disco e alla densità atmosferica. L'atmosfera rarefatta di Marte (circa 0.020 kg/m³ ad Arcadia Planitia) richiede carichi di potenza maggiori rispetto a operazioni terrestri equivalenti.
* Vincolo di crociera: derivato dalla polare di resistenza, questo vincolo determina la potenza necessaria per il volo livellato stazionario alla velocità di crociera di progetto.
* Vincolo di salita: garantisce una potenza eccedente sufficiente per la velocità di salita richiesta.
* Vincolo di stallo: stabilisce il carico alare massimo in base al coefficiente di portanza massimo del profilo alare al numero di Reynolds operativo.

Il punto di progetto viene selezionato all'interno della regione ammissibile delimitata da questi vincoli. Per le configurazioni QuadPlane, i vincoli di hovering e crociera sono in gran parte disaccoppiati: i rotori di sollevamento sono dimensionati per soddisfare il vincolo di hovering, mentre l'ala e il motore di crociera sono dimensionati per soddisfare i vincoli di crociera e stallo. Questo disaccoppiamento semplifica l'esplorazione dello spazio di progettazione ma richiede una verifica che il sistema combinato rimanga entro l'obiettivo di MTOW.

I requisiti derivati riassunti in @tbl:derived-requirements definiscono il punto di partenza per l'analisi del matching chart. L'MTOW target di 10 kg, derivato dall'analisi delle frazioni di massa e dai requisiti di payload, stabilisce il peso per la valutazione dei vincoli. La frazione di batteria assunta (35%), l'energia specifica (270 Wh/kg) e le efficienze propulsive alimentano i calcoli di potenza e autonomia. L'esecuzione del matching chart con questi input produce il punto di progetto preliminare: la combinazione specifica di carico alare e carico di potenza che massimizza l'autonomia soddisfacendo tutti i vincoli. Questo punto di progetto determina poi l'area alare, l'apertura e i requisiti di potenza dei motori che guidano la selezione dei componenti.

La natura iterativa di questo processo riconosce che le ipotesi iniziali sono necessariamente approssimate. Man mano che la selezione dei componenti rivela masse ed efficienze effettive, il punto di progetto può spostarsi. La metodologia garantisce che tali spostamenti siano sistematicamente tracciati e che il progetto finale rimanga tracciabile rispetto ai suoi fondamenti analitici.
