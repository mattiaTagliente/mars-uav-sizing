# Conclusioni e raccomandazioni {#sec:conclusions}

Questo studio di fattibilità ha valutato la possibilità di impiegare un UAV autonomo da un habitat marziano con equipaggio per supportare missioni di mappatura e relè di telecomunicazioni. L'analisi si è concentrata sul dimensionamento concettuale e sulla selezione dei componenti, stabilendo le basi per le successive fasi di progettazione.

## Sintesi dei risultati {#sec:summary-findings}

Lo studio ha valutato tre architetture candidate—velivolo a rotore, ad ala fissa e VTOL ibrido—attraverso un'analisi di dimensionamento basata su vincoli. I risultati chiave includono:

* L'**architettura ibrida QuadPlane** fornisce un compromesso efficace tra capacità VTOL e efficienza di crociera, raggiungendo un margine energetico del 49% rispetto ai requisiti di missione
* Gli **effetti a basso numero di Reynolds** (Re ≈ 55,000) impattano significativamente il progetto aerodinamico; il profilo SD8000 offre prestazioni di resistenza consistenti con adeguato margine di stallo (4.6°)
* La **potenza di hovering domina il dimensionamento dei motori**; la potenza di crociera ad ala fissa è sostanzialmente inferiore alla potenza di hovering, favorendo configurazioni che minimizzano la durata dell'hovering
* L'attuale **tecnologia delle batterie** (150 Wh/kg) consente durate di missione pratiche di circa 90 minuti con riserva del 20%
* La configurazione a solo rotore è **marginalmente fattibile** ma offre margine operativo limitato; la configurazione ad ala fissa **non è fattibile** senza infrastruttura di pista

## Raccomandazioni {#sec:recommendations}

Sulla base dell'analisi, si formulano le seguenti raccomandazioni per la fase di progettazione preliminare:

1. **Procedere con l'architettura QuadPlane**: Il sistema di sollevamento a ottorotore con configurazione di elica di crociera coassiale offre il miglior equilibrio tra prestazioni, affidabilità e flessibilità operativa
2. **Sviluppo tecnologico**: Prioritizzare il miglioramento dell'energia specifica delle batterie (>200 Wh/kg) per significativi guadagni prestazionali nelle future iterazioni
3. **Validazione del profilo**: I test in galleria del vento del profilo SD8000 ai numeri di Reynolds rappresentativi di Marte sono giustificati per confermare le previsioni aerodinamiche a bassa velocità
4. **Mitigazione della polvere**: Gli effetti della contaminazione superficiale sulle prestazioni del rotore e dell'ala richiedono indagine, in particolare per operazioni di superficie di lunga durata

## Lavori futuri {#sec:future-work}

Questo studio di fattibilità ha impiegato una metodologia a caso base con MTOW di riferimento fisso per consentire un confronto equo tra le architetture. Diversi miglioramenti alla metodologia di dimensionamento e analisi aggiuntive dei sottosistemi sono identificati per le successive fasi di progettazione.

### Miglioramenti della metodologia di dimensionamento

L'attuale approccio a caso base utilizza frazioni di massa fisse e un MTOW di riferimento. Le future iterazioni dovrebbero implementare:

* **Chiusure accoppiate specifiche per configurazione**: Dimensionamento iterativo che risolve simultaneamente MTOW e massa della batteria per ciascuna architettura, dati massa del carico utile, tempi dei segmenti di missione e requisiti di riserva energetica. Ciò consentirebbe l'ottimizzazione anziché la sola verifica di fattibilità
* **Modello di massa basato sui componenti**: Sostituzione delle frazioni di massa fisse con un modello costruttivo per i sottosistemi batteria, carico utile, propulsione e struttura. La plausibilità della frazione di carico utile dovrebbe essere vincolata utilizzando il database dei droni di riferimento
* **Diagrammi di vincolo appropriati per configurazione**: Rapporto potenza-peso versus carico del disco (P/W vs DL) per velivoli a rotore; rapporto potenza-peso versus carico alare (P/W vs W/S) per ala fissa e VTOL ibrido, con sweep parametrici nel carico del disco e nei tempi dei segmenti di missione

### Analisi dei sottosistemi

Diversi sottosistemi critici sono stati identificati ma rinviati alle successive fasi di progettazione:

* **Progettazione del sistema avionico**: Selezione e integrazione del controllore di volo, unità di misura inerziale, altimetro e sensori di dati aria appropriati per l'atmosfera marziana a bassa densità. Definizione dell'architettura del collegamento telemetrico tra UAV e habitat
* **Analisi della gestione termica**: Modellazione termica dettagliata per l'estremo intervallo di temperatura diurna marziana (circa da −80 °C a −20 °C). Progettazione di sistemi di riscaldamento attivo per la protezione termica di batteria e avionica durante lo stoccaggio notturno e le operazioni di volo
* **Analisi strutturale e progettazione di dettaglio**: Analisi agli elementi finiti della cellula, ala e struttura del boom. Analisi delle vibrazioni per i carichi indotti dal rotore. Qualificazione dei materiali per l'ambiente radiativo e termico marziano

Questi miglioramenti metodologici e analisi dei sottosistemi sono prerequisiti essenziali per avanzare dalla fattibilità alla revisione del progetto preliminare (PDR).

---

Il concetto di UAV marziano è **tecnicamente fattibile** con la tecnologia attuale o a breve termine. La configurazione QuadPlane soddisfa tutti i requisiti di missione primari con margine adeguato, fornendo una piattaforma praticabile per estendere la portata operativa delle missioni di superficie marziane con equipaggio.
