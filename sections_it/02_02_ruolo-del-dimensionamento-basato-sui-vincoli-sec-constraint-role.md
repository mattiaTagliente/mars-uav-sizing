# Metodologia di progettazione

## Ruolo del dimensionamento basato sui vincoli {#sec:constraint-role}

Il diagramma di vincolo, o matching chart, costituisce il nucleo analitico della metodologia di dimensionamento. Questo strumento grafico, adattato dai metodi di dimensionamento aeronautico basati sulla potenza, traccia il carico di potenza (P/W) in funzione del carico alare (W/S) per ciascun vincolo di volo.

Per un aeromobile VTOL ibrido, che emerge come la configurazione più adatta dall'analisi dei trade-off (@sec:architecture-selection), i vincoli rilevanti includono:

* Vincolo di hovering: stabilisce il carico di potenza minimo in base al carico del disco e alla densità atmosferica. L'atmosfera rarefatta di Marte (circa 0.020 kg/m³ ad Arcadia Planitia) richiede carichi di potenza maggiori rispetto a operazioni terrestri equivalenti.
* Vincolo di crociera: derivato dalla polare di resistenza, questo vincolo determina la potenza necessaria per il volo livellato stazionario alla velocità di crociera di progetto.
* Vincolo di salita: garantisce una potenza eccedente sufficiente per la velocità di salita richiesta.
* Vincolo di stallo: stabilisce il carico alare massimo in base al coefficiente di portanza massimo del profilo alare al numero di Reynolds operativo.

Il punto di progetto viene selezionato all'interno della regione ammissibile delimitata da questi vincoli. Per le configurazioni QuadPlane, i vincoli di hovering e crociera sono in gran parte disaccoppiati: i rotori di sollevamento sono dimensionati per soddisfare il vincolo di hovering, mentre l'ala e il motore di crociera sono dimensionati per soddisfare i vincoli di crociera e stallo. Questo disaccoppiamento semplifica l'esplorazione dello spazio di progettazione ma richiede una verifica che il sistema combinato rimanga entro l'obiettivo di MTOW.

I requisiti derivati riassunti in @tbl:derived-requirements definiscono il punto di partenza per l'analisi del matching chart. L'MTOW target di 10 kg, derivato dall'analisi delle frazioni di massa e dai requisiti di payload, stabilisce il peso per la valutazione dei vincoli. La frazione di batteria assunta (35%), l'energia specifica (270 Wh/kg) e le efficienze propulsive alimentano i calcoli di potenza e autonomia. L'esecuzione del matching chart con questi input produce il punto di progetto preliminare: la combinazione specifica di carico alare e carico di potenza che massimizza l'autonomia soddisfacendo tutti i vincoli. Questo punto di progetto determina poi l'area alare, l'apertura e i requisiti di potenza dei motori che guidano la selezione dei componenti.

La natura iterativa di questo processo riconosce che le ipotesi iniziali sono necessariamente approssimate. Man mano che la selezione dei componenti rivela masse ed efficienze effettive, il punto di progetto può spostarsi. La metodologia garantisce che tali spostamenti siano sistematicamente tracciati e che il progetto finale rimanga tracciabile rispetto ai suoi fondamenti analitici.
