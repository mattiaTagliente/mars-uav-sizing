# Requisiti infrastrutturali

## Concetto operativo {#sec:operations-concept}

Questa sezione definisce le procedure operative per le missioni UAV dall'habitat marziano, includendo le fasi di missione, i ruoli dell'equipaggio e il ritmo operativo.

### Fasi della missione

Una tipica sortita UAV consiste nelle seguenti fasi:

: Fasi sortita UAV e cronoprogramma {#tbl:sortie-phases}

| Fase | Ubicazione | Durata | Descrizione |
|:------|:---------|:--------:|:------------|
| 1. Preparazione pre-volo | Baia pressurizzata | 30 min | Controlli sistema, upload piano volo |
| 2. Trasferimento ad airlock | Airlock | 10 min | UAV spostato in zona transizione |
| 3. Depressurizzazione airlock | Airlock | 5 min | Riduzione pressione ad ambiente Marte |
| 4. Trasferimento a piattaforma | Esterno | 5 min | UAV posizionato su pad lancio |
| 5. Decollo VTOL | Esterno | 2 min | Hovering, transizione, partenza |
| 6. Crociera andata | In volo | 20-40 min | Transito verso area survey |
| 7. Operazioni survey | In volo | 20-60 min | Missione mapping o relay |
| 8. Crociera ritorno | In volo | 20-40 min | Transito verso habitat |
| 9. Atterraggio VTOL | Esterno | 2 min | Avvicinamento, transizione, hovering |
| 10. Trasferimento ad airlock | Airlock | 5 min | UAV spostato in zona transizione |
| 11. Ripressurizzazione airlock | Airlock | 5 min | Aumento pressione ad habitat |
| 12. Ispezione post-volo | Baia pressurizzata | 30 min | Download dati, controllo sistema |
| 13. Ricarica batteria | Baia pressurizzata | 2-3 h | Ricarica a piena capacità |

Durata totale sortita: 2.5-4.5 ore (fasi a terra), 1-2 ore (fasi di volo).

### Ruoli dell'equipaggio

Le operazioni UAV richiedono coinvolgimento minimo dell'equipaggio grazie alla capacità di volo autonomo:

Operatore UAV (1 persona): Responsabile della pianificazione missione, monitoraggio volo e analisi dati. Le operazioni sono condotte dall'interno dell'habitat usando la stazione di controllo a terra.

Supporto EVA (opzionale): Per manutenzione non di routine o operazioni di recupero fuori dalla baia pressurizzata.

### Ritmo operativo

Il ritmo operativo è vincolato dal tempo di ricarica batteria e dalla durata del giorno solare marziano (sol):

: Analisi ritmo operativo {#tbl:ops-tempo}

| Scenario | Voli/sol | Note |
|:---------|:-----------:|:------|
| Singolo UAV | 1-2 | Limitato da 2-3 h tempo ricarica |
| Due UAV (alternati) | 3-4 | Uno vola mentre l'altro ricarica |
| Campagna sostenuta | 1/sol media | Conservativo per longevità equipaggiamento |

Con due UAV pronti al volo, le operazioni giornaliere sono fattibili con voli alternati e cicli di ricarica. In una campagna missione di 30 sol, si possono eseguire circa 30-60 sortite.

### Operazioni di contingenza

Le procedure di contingenza affrontano i modi di guasto prevedibili: decollo abortito (l'UAV rimane sulla piattaforma e l'equipaggio recupera tramite procedura airlock); emergenza in volo (ritorno autonomo alla base o atterraggio di emergenza su terreno pianeggiante alternativo); perdita comunicazioni (ritorno alla base pre-programmato dopo timeout configurabile, default 5 min); e guasto atterraggio (zona di atterraggio secondaria designata con recupero EVA se richiesto).

### Programma manutenzione

Manutenzione programmata tra le sortite:

: Programma manutenzione {#tbl:maintenance}

| Intervallo | Attività | Durata |
|:---------|:---------|:--------:|
| Ogni volo | Ispezione visiva, download dati | 30 min |
| Ogni 5 voli | Controllo condizione eliche, ispezione connettori | 1 h |
| Ogni 10 voli | Valutazione termica motori, controllo cuscinetti | 2 h |
| Ogni 50 voli | Ispezione completa sistema, test capacità batteria | 4 h |

