# Metodologia di progettazione

## Approccio iterativo di dimensionamento {#sec:iterative-sizing}

Lo sviluppo di questo UAV marziano segue una metodologia di dimensionamento iterativo che bilancia l'analisi teorica con i vincoli pratici dei componenti. A differenza della progettazione convenzionale di aeromobili terrestri, dove esistono leggi di scalamento mature e ampie banche dati, la progettazione di aeromobili marziani richiede un'integrazione della limitata eredità di volo con l'analisi scalata da casi di riferimento.

Il processo di progettazione procede attraverso quattro fasi distinte, con cicli di retroazione che consentono il perfezionamento in ogni fase:

1. Ipotesi iniziali: i dati di riferimento degli UAV VTOL da piattaforme commerciali e progetti concettuali marziani (@sec:reference-data) forniscono una base empirica per le stime iniziali dei parametri. I parametri chiave estratti dai progetti di riferimento includono le frazioni di massa (propulsione, energia, payload e, per sottrazione, struttura e altri sottosistemi), il carico del disco per le operazioni VTOL e i rapporti potenza-peso. Questi valori terrestri sono poi scalati per le condizioni marziane, tenendo conto della gravità ridotta (38% della Terra) e dell'atmosfera rarefatta (circa l'1% della densità a livello del mare terrestre).
2. Dimensionamento preliminare: con le ipotesi iniziali stabilite, la metodologia di dimensionamento basata sui vincoli genera un punto di progetto preliminare. Il diagramma di vincolo (matching chart) determina la combinazione di carico alare e carico di potenza che soddisfa tutte le condizioni di volo (hovering, crociera, salita e stallo). Da questo punto di progetto vengono calcolati i valori preliminari per area alare, apertura, potenza dei motori e ripartizione delle masse.
3. Selezione dei componenti: i risultati del dimensionamento preliminare guidano la selezione dei componenti effettivi dalle schede tecniche dei produttori. Questa fase confronta il modello di dimensionamento idealizzato con i vincoli del mondo reale, poiché i motori sono disponibili solo in dimensioni discrete, le batterie hanno densità energetiche specifiche, caratteristiche di tensione e limitazioni di temperatura, e le eliche devono essere compatibili con le configurazioni dei motori disponibili.
4. Verifica: i componenti selezionati forniscono valori aggiornati di massa, potenza ed efficienza che differiscono dalle stime preliminari. Il progetto viene ricalcolato con questi valori effettivi e viene verificata la conformità ai requisiti di missione. Se i requisiti non sono soddisfatti, il processo ritorna alla fase 2 con ipotesi perfezionate.

@fig:sizing-loop illustra la natura iterativa di questo processo. Ogni iterazione restringe lo spazio di progettazione man mano che emergono i vincoli a livello di componente e i requisiti vengono progressivamente soddisfatti.

![Il ciclo iterativo di dimensionamento per la progettazione di UAV marziani.](figures/sizing_loop_it.jpg){#fig:sizing-loop}

### Ambito dello studio attuale

Questo studio di fattibilità rappresenta la prima iterazione del ciclo a quattro fasi descritto. Le fasi 1 (ipotesi iniziali) e 2 (dimensionamento preliminare) sono riportate come segue: l'analisi dei dati di riferimento stabilisce i parametri iniziali (@sec:reference-data), il dimensionamento basato sui vincoli determina il punto di progetto (@sec:constraint-analysis) e i trade-off tra configurazioni identificano il VTOL ibrido come architettura selezionata (@sec:architecture-selection). Le fasi 3 (selezione dei componenti) e 4 (verifica) sono affrontate attraverso l'analisi di componenti commerciali rappresentativi e la verifica analitica rispetto ai requisiti di missione.

I risultati numerici presentati in @sec:constraint-analysis sono valutati a un MTOW di riferimento fisso di 10.00 kg, derivato dall'analisi delle frazioni di massa (@sec:initial-mass-estimate). Questo approccio consente il confronto diretto delle prestazioni delle configurazioni sotto vincoli di massa ed energia identici. Un'iterazione di dimensionamento a ciclo chiuso, dove l'MTOW viene aggiustato per soddisfare esattamente i requisiti di missione, è rinviata alle fasi di progettazione successive.

Aspetti non modellati in questa prima iterazione includono vincoli dettagliati di packaging e volume, analisi dei margini termici durante i cicli operativi, verifica di stabilità e controllo e considerazioni di fabbricazione e assemblaggio. Questi sono riservati alle iterazioni successive man mano che il progetto matura verso la progettazione di dettaglio.
