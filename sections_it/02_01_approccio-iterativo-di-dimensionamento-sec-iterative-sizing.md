# Metodologia di progettazione

## Approccio iterativo di dimensionamento {#sec:iterative-sizing}

Lo sviluppo di questo UAV marziano segue una metodologia di dimensionamento iterativo che bilancia l'analisi teorica con i vincoli pratici dei componenti. A differenza della progettazione convenzionale di aeromobili terrestri, dove esistono leggi di scalamento mature e ampie banche dati, la progettazione di aeromobili marziani richiede un'attenta integrazione dell'eredità di volo limitata con l'analisi scalata da casi di riferimento.

Il processo di progettazione procede attraverso quattro fasi distinte, con cicli di retroazione che consentono il perfezionamento in ogni fase:

1. **Ipotesi iniziali**: i dati di riferimento degli UAV VTOL da piattaforme commerciali e progetti concettuali marziani (@sec:reference-data) forniscono una base empirica per le stime iniziali dei parametri. I parametri chiave estratti dai progetti di riferimento includono le frazioni di massa (propulsione, energia, payload e, per sottrazione, struttura e altri sottosistemi), il carico del disco per le operazioni VTOL e i rapporti potenza-peso. Questi valori terrestri sono poi scalati per le condizioni marziane, tenendo conto della gravità ridotta (38% della Terra) e dell'atmosfera rarefatta (circa l'1% della densità a livello del mare terrestre).
2. **Dimensionamento preliminare**: con le ipotesi iniziali stabilite, la metodologia di dimensionamento basata sui vincoli genera un punto di progetto preliminare. Il diagramma di vincolo (matching chart) determina la combinazione di carico alare e carico di potenza che soddisfa tutte le condizioni di volo (hovering, crociera, salita e stallo). Da questo punto di progetto vengono calcolati i valori preliminari per area alare, apertura, potenza dei motori e ripartizione delle masse.
3. **Selezione dei componenti**: i risultati del dimensionamento preliminare guidano la selezione dei componenti effettivi dalle schede tecniche dei produttori. Questa fase confronta il modello di dimensionamento idealizzato con i vincoli del mondo reale, poiché i motori sono disponibili solo in dimensioni discrete, le batterie hanno densità energetiche specifiche, caratteristiche di tensione e limitazioni di temperatura, e le eliche devono essere compatibili con le configurazioni dei motori disponibili.
4. **Verifica**: i componenti selezionati forniscono valori aggiornati di massa, potenza ed efficienza che differiscono dalle stime preliminari. Il progetto viene ricalcolato con questi valori effettivi e viene verificata la conformità ai requisiti di missione. Se i requisiti non sono soddisfatti, il processo ritorna alla fase 2 con ipotesi perfezionate.

@fig:sizing-loop illustra la natura iterativa di questo processo. Ogni iterazione restringe lo spazio di progettazione man mano che emergono i vincoli a livello di componente e i requisiti vengono progressivamente soddisfatti.

![Il ciclo iterativo di dimensionamento per la progettazione di UAV marziani.](figures/sizing_loop.jpg){#fig:sizing-loop}
