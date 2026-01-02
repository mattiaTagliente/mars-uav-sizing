# Conclusioni e raccomandazioni

## Lavori futuri {#sec:future-work}

Questo studio di fattibilità ha impiegato una metodologia a caso base con MTOW di riferimento fisso per consentire un confronto equo tra le architetture. Diversi miglioramenti alla metodologia di dimensionamento e analisi aggiuntive dei sottosistemi sono identificati per le successive fasi di progettazione.

### Miglioramenti della metodologia di dimensionamento

L'attuale approccio a caso base utilizza frazioni di massa fisse e un MTOW di riferimento. Le future iterazioni dovrebbero implementare:

* Chiusure accoppiate specifiche per configurazione: dimensionamento iterativo che risolve simultaneamente MTOW e massa della batteria per ciascuna architettura, dati massa del carico utile, tempi dei segmenti di missione e requisiti di riserva energetica. Ciò consentirebbe l'ottimizzazione anziché la sola verifica di fattibilità
* Modello di massa basato sui componenti: sostituzione delle frazioni di massa fisse con un modello costruttivo per i sottosistemi batteria, carico utile, propulsione e struttura. La plausibilità della frazione di carico utile dovrebbe essere vincolata utilizzando il database dei droni di riferimento
* Diagrammi di vincolo appropriati per configurazione: rapporto potenza-peso versus carico del disco (P/W vs DL) per velivoli a rotore; rapporto potenza-peso versus carico alare (P/W vs W/S) per ala fissa e VTOL ibrido, con sweep parametrici nel carico del disco e nei tempi dei segmenti di missione

### Analisi dei sottosistemi

Diversi sottosistemi critici sono stati identificati ma rinviati alle successive fasi di progettazione:

* Progettazione del sistema avionico: selezione e integrazione del controllore di volo, unità di misura inerziale, altimetro e sensori di dati aria appropriati per l'atmosfera marziana a bassa densità. Definizione dell'architettura del collegamento telemetrico tra UAV e habitat
* Analisi della gestione termica: modellazione termica dettagliata per l'estremo intervallo di temperatura diurna marziana (circa da −80 °C a −20 °C). Progettazione di sistemi di riscaldamento attivo per la protezione termica di batteria e avionica durante lo stoccaggio notturno e le operazioni di volo
* Analisi strutturale e progettazione di dettaglio: analisi agli elementi finiti della cellula, ala e struttura del boom. Analisi delle vibrazioni per i carichi indotti dal rotore. Qualificazione dei materiali per l'ambiente radiativo e termico marziano

Questi miglioramenti metodologici e analisi dei sottosistemi sono prerequisiti essenziali per avanzare dalla fattibilità alla revisione del progetto preliminare (PDR).

---

Il concetto di UAV marziano è tecnicamente fattibile con la tecnologia attuale o a breve termine. La configurazione QuadPlane soddisfa tutti i requisiti di missione primari con margine adeguato, fornendo una piattaforma praticabile per estendere la portata operativa delle missioni di superficie marziane con equipaggio.

