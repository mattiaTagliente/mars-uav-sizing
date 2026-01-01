# Dati di riferimento e analisi dei compromessi

## Stima di massa iniziale {#sec:initial-mass-estimate}

Questa sezione stabilisce la stima iniziale dell'MTOW (Maximum Takeoff Weight) utilizzando l'approccio delle frazioni di massa, una tecnica standard nella progettazione concettuale di aeromobili [@roskamAirplaneDesign12005a]<!-- #s:mass-fraction --> [@sadraeyAircraftDesignSystems2013]<!-- #s:mass-fraction -->. L'intervallo di MTOW stabilito qui fornisce il punto di partenza per l'analisi dei vincoli in @sec:constraint-analysis.

### Metodologia delle frazioni di massa

La massa totale dell'aeromobile si scompone in categorie di componenti principali:

$$MTOW = m_\text{payload} + m_\text{batteria} + m_\text{vuoto} + m_\text{propulsione} + m_\text{avionica}$$ {#eq:mtow-breakdown}

La massa di ogni componente può essere espressa come frazione dell'MTOW:

$$f_i = \frac{m_i}{MTOW}$$ {#eq:fraction-def}

Poiché la somma delle frazioni è uguale a uno:

$$f_\text{payload} + f_\text{batteria} + f_\text{vuoto} + f_\text{propulsione} + f_\text{avionica} = 1$$ {#eq:fraction-sum}

Data la massa del payload $m_\text{payload}$ (un requisito di missione da @sec:payload-systems), l'MTOW può essere stimato se la frazione di payload è nota:

$$MTOW = \frac{m_\text{payload}}{f_\text{payload}}$$ {#eq:mtow-from-payload}

Questo approccio fornisce una stima di primo ordine prima della selezione dettagliata dei componenti.

### Analisi dei dati di riferimento

Le frazioni di massa sono state calcolate da un database di nove UAV VTOL ibridi commerciali documentati in @sec:commercial-vtol. @tbl:reference-mass-fractions riassume i risultati.

: Frazioni di massa dal database UAV VTOL di riferimento {#tbl:reference-mass-fractions}

| Frazione | Simbolo | Min | Max | Media | Mediana | Campione |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Batteria | $f_\text{batt}$ | 0.36 | 0.40 | 0.38 | 0.38 | 3 |
| Payload | $f_\text{payload}$ | 0.10 | 0.30 | 0.20 | 0.21 | 9 |
| Vuoto | $f_\text{vuoto}$ | 0.25 | 0.27 | 0.26 | 0.26 | 2 |
| Propulsione | $f_\text{prop}$ | 0.09 | 0.10 | 0.10 | 0.10 | 2 |

L'analisi dei dati di riferimento rivela diversi pattern. Gli UAV VTOL commerciali allocano circa il 36-40% dell'MTOW alle batterie, riflettendo le esigenze energetiche di entrambe le fasi di hovering e crociera. La frazione di payload mostra ampia variazione (10-30%) a seconda del focus della missione: i design ottimizzati per l'autonomia mostrano frazioni di payload più basse (circa 10%), mentre i design per carichi pesanti raggiungono fino al 30%. Esistono dati limitati per la frazione a vuoto (solo due UAV con definizioni non ambigue del peso a vuoto), con valori osservati del 25-27%; tuttavia, i fattori specifici per Marte aumenteranno significativamente questo valore. Per la frazione di propulsione, sono disponibili solo i dati dei motori (9-10%), mentre i sistemi propulsivi completi (motori, ESC, eliche) sono stimati al 12-18%.

### Valori di progetto raccomandati

Basandosi sull'analisi dei dati di riferimento e sui requisiti della missione marziana, vengono adottate le seguenti frazioni di massa per il dimensionamento iniziale:

: Frazioni di massa raccomandate per il dimensionamento iniziale dell'UAV marziano {#tbl:design-mass-fractions}

| Frazione | Simbolo | Valore | Intervallo | Motivazione |
|---|:---:|:---:|:---:|---|
| Batteria | $f_\text{batt}$ | 0.35 | 0.30-0.40 | Requisito di alta autonomia; vincoli termici marziani |
| Payload | $f_\text{payload}$ | 0.10 | 0.08-0.15 | Allocazione conservativa per camera e radio relay |
| Vuoto | $f_\text{vuoto}$ | 0.30 | 0.25-0.35 | Include gestione termica, protezione dalla polvere, margini strutturali |
| Propulsione | $f_\text{prop}$ | 0.20 | 0.15-0.25 | Sistema di propulsione duale ridondante (sollevamento + crociera) |
| Avionica | $f_\text{avionica}$ | 0.05 | 0.03-0.07 | Stima standard con sensori specifici per Marte |

La frazione di propulsione è più alta rispetto ai benchmark degli UAV commerciali a causa della necessità di ridondanza nel sistema di propulsione duale (sia rotori di sollevamento che eliche di crociera), operando senza possibilità di riparazione in volo.

La frazione a vuoto tiene conto dei requisiti specifici per Marte: sistemi di isolamento termico e riscaldamento attivo per l'ambiente operativo da −80 a +20 °C, protezione dall'ingresso di polvere (equivalente a IP55 o superiore), potenziale selezione di componenti tolleranti alle radiazioni, e margini strutturali per la fatica da cicli termici.

### Stima di base dell'MTOW

Utilizzando il metodo della frazione di payload da @eq:mtow-from-payload con:

* Massa del payload: $m_\text{payload}$ = 1.0 kg
* Frazione di payload: $f_\text{payload}$ = 0.10 (da @tbl:design-mass-fractions)

La stima della massa del payload di 1.0 kg è derivata da un'ipotesi conservativa per il payload combinato: un sistema camera RGB compatto (circa 400 g basato sull'indagine in @sec:camera-survey), un modulo radio racchiuso (circa 170 g basato su @sec:radio-survey), margine di ridondanza per la missione radio relay, e margine di sicurezza per hardware di montaggio e protezione termica.

$$MTOW = \frac{1.0}{0.10} = 10 \text{ kg}$$

La sensibilità alla selezione della frazione di payload:

: Sensibilità della stima MTOW alla frazione di payload {#tbl:mtow-sensitivity}

| Frazione di payload | Stima MTOW |
|:---:|---:|
| 0.08 | 12.5 kg |
| 0.10 | 10.0 kg |
| 0.15 | 6.7 kg |

Viene adottato un MTOW di base di 10 kg per il dimensionamento iniziale. Questo valore sarà affinato attraverso l'analisi dei vincoli in @sec:constraint-analysis, dove i requisiti di potenza, il carico alare e i vincoli di autonomia sono valutati simultaneamente.

La massa del payload di 1.00 kg è un **vincolo di missione fisso** derivato dai componenti selezionati per camera e relè radio (@sec:payload-systems). Questo dimensionamento basato sul payload garantisce che il requisito di payload della missione sia soddisfatto per costruzione. Qualsiasi configurazione che non possa trasportare 1.00 kg entro l'involucro MTOW di 10.00 kg è non fattibile.

### Validazione delle frazioni di massa

Le frazioni raccomandate sommano a uno:

$$f_\text{batt} + f_\text{payload} + f_\text{vuoto} + f_\text{prop} + f_\text{avionica} = 0.35 + 0.10 + 0.30 + 0.20 + 0.05 = 1.00$$

Le frazioni sono auto-consistenti, con la ridotta frazione a vuoto (rispetto alle stime iniziali) compensata dall'aumentata allocazione propulsiva per la ridondanza. Questa allocazione riflette l'architettura VTOL ibrida dove entrambi i sistemi di propulsione di sollevamento e crociera devono essere dimensionati per l'affidabilità.

La metodologia dettagliata di stima del peso dei componenti, utilizzando equazioni semi-empiriche adattate per le condizioni marziane, è presentata in @sec:mass-breakdown dopo che l'analisi dei vincoli ha determinato la geometria richiesta.
