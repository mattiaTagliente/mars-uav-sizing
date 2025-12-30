# Analisi dei vincoli

## Configurazione VTOL ibrida {#sec:hybrid-vtol-analysis}

Questa sezione valuta se una configurazione VTOL ibrida (QuadPlane) può soddisfare i requisiti di missione dell'UAV marziano. La configurazione ibrida combina la capacità di decollo e atterraggio verticale del velivolo a rotore con le efficienti prestazioni di crociera dell'aeromobile ad ala fissa. L'analisi dimostra che questa è l'unica configurazione che soddisfa tutti e tre i requisiti: capacità VTOL, autonomia di crociera e raggio operativo.

### Architettura QuadPlane

#### Descrizione della configurazione

La configurazione QuadPlane consiste in due sistemi propulsivi distinti ottimizzati per i rispettivi regimi di volo [@bertaniPreliminaryDesignFixedwing2023].

Il sistema di sollevamento (per l'hovering) comprende quattro o più rotori elettrici in una disposizione quadricottero o simile, dimensionati solo per la spinta di hovering (operazione di breve durata), posizionati per minimizzare l'interferenza con l'aerodinamica dell'ala, e inattivi durante la crociera (fermi o ripiegati).

Il sistema di crociera (per il volo avanzato) utilizza un'ala per la generazione di portanza e una singola elica spintrice o trattrice per la spinta, dimensionato per una crociera efficiente a $(L/D)_\text{max}$, e inattivo durante l'hovering.

Questa architettura consente l'ottimizzazione disaccoppiata: ogni sistema propulsivo opera solo nel suo regime ottimale. I rotori di sollevamento sono dimensionati per la spinta di hovering senza compromessi per l'efficienza in volo avanzato, mentre l'ala e l'elica di crociera sono ottimizzati per la massima efficienza aerodinamica senza requisiti di capacità VTOL.

Questo approccio contrasta con il velivolo a rotore puro (dove i rotori devono operare efficientemente sia in hovering che in volo avanzato) e i concetti a rotore basculante (dove è richiesta complessità meccanica per la vettorizzazione della spinta).

#### Fasi di volo

Il profilo di missione nominale comprende cinque fasi di volo, riassunte in @tbl:quadplane-phases.

: Fasi di volo del QuadPlane {#tbl:quadplane-phases}

| Fase | Sistema propulsivo | Fonte di portanza | Durata |
|:------|:-----------------|:------------|:---------:|
| Decollo | Solo rotori di sollevamento | Spinta dei rotori | circa 60 s |
| Transizione | Entrambi i sistemi | Rotori → Ala | circa 30 s |
| Crociera | Solo motore di crociera | Ala | circa 57 min |
| Transizione | Entrambi i sistemi | Ala → Rotori | circa 30 s |
| Atterraggio | Solo rotori di sollevamento | Spinta dei rotori | circa 60 s |

L'osservazione è che il tempo di hovering è limitato a circa 3 minuti (180 s) della missione totale di 60 minuti. Durante i restanti 57 minuti, l'aeromobile opera come un convenzionale ala fissa con i rotori di sollevamento inattivi. Questo cambia il bilancio energetico rispetto al velivolo a rotore puro.

### Vincolo di hovering

#### Riferimento all'analisi del velivolo a rotore

Le equazioni della potenza di hovering sviluppate in @sec:rotorcraft-analysis si applicano direttamente al sistema di sollevamento del QuadPlane. Da @eq:hover-power, la potenza meccanica di hovering è:

$$P_\text{hover} = \frac{W^{3/2}}{FM \cdot \sqrt{2\rho A}}$$ {#eq:hover-power-qp}

dove $W$ è il peso dell'aeromobile, $FM$ è la figura di merito, $\rho$ è la densità atmosferica, e $A$ è l'area totale del disco del rotore.

Includendo le perdite elettriche, la potenza dalla batteria per l'hovering è:

$$P_\text{elettrica,hover} = \frac{P_\text{hover}}{\eta_\text{motore} \cdot \eta_\text{ESC}} = \frac{W^{3/2}}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC} \cdot \sqrt{2\rho A}}$$ {#eq:electric-hover-qp}

Utilizzando i valori di efficienza da @tbl:efficiency-parameters ($FM$ = 0.4000, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza di hovering combinata è $\eta_\text{hover}$ = 0.4000 × 0.8500 × 0.9500 = 0.3230, identica al caso del velivolo a rotore puro.

#### Differenza dal velivolo a rotore: durata dell'hovering

Il vantaggio principale del QuadPlane rispetto al velivolo a rotore puro è il ridotto tempo di hovering. Un velivolo a rotore puro utilizza l'hovering o il volo avanzato simile all'hovering per l'intera missione (circa 60 min), mentre il QuadPlane effettua hovering solo durante il decollo e l'atterraggio (circa 3 min).

Questa riduzione di 20× del tempo di hovering cambia l'equazione energetica. Anche se l'hovering è ad alta intensità di potenza, limitarlo al 5% della durata della missione rende il costo energetico gestibile.

#### Energia di hovering

L'energia consumata durante le fasi di hovering è:

$$E_\text{hover} = P_\text{elettrica,hover} \times t_\text{hover}$$ {#eq:hover-energy}

dove $t_\text{hover} = 180$ s (3 min) dall'allocazione del tempo di hovering in @sec:mission-parameters.

Utilizzando i parametri di base (MTOW = 10.00 kg, carico del disco $DL$ = 30.00 N/m²):

Da @eq:induced-velocity-dl e @eq:hover-power:

$$v_i = \sqrt{\frac{DL}{2\rho}} = \sqrt{\frac{30.00}{2 \times 0.01960}} = \sqrt{765.3} = 27.68 \text{ m/s}$$

$$P_\text{ideale} = W \times v_i = (10.00 \times 3.711) \times 27.68 = 1027 \text{ W}$$

$$P_\text{elettrica,hover} = P_\text{ideale} / (FM \times \eta_\text{motore} \times \eta_\text{ESC}) = 1027 / 0.3230 = 3178 \text{ W}$$

Convertendo in energia:

$$E_\text{hover} = 3178 \times (180.0/3600) = 158.9 \text{ Wh}$$ {#eq:hover-energy-value}

Questo rappresenta il 22% del budget energetico disponibile, che è gestibile data la breve durata dell'hovering.

### Vincolo di crociera

#### Riferimento all'analisi dell'ala fissa

Le equazioni della potenza di crociera sviluppate in @sec:fixed-wing-analysis si applicano direttamente alla fase di crociera del QuadPlane. Da @eq:cruise-electric-power, la potenza elettrica per la crociera è:

$$P_\text{elettrica,crociera} = \frac{W \times V}{(L/D) \times \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC}}$$ {#eq:cruise-power-qp}

dove $V$ è la velocità di crociera e $(L/D)$ è il rapporto portanza-resistenza.

#### Efficienza aerodinamica del QuadPlane

Durante la crociera, il QuadPlane raggiunge l'efficienza aerodinamica dell'ala fissa perché i rotori di sollevamento sono inattivi. Due approcci progettuali sono possibili: rotori fermi (i rotori rimangono stazionari, contribuendo solo alla resistenza parassita), e rotori ripiegati (le pale del rotore si ripiegano contro i pod dei motori, minimizzando la resistenza).

Per i rotori fermi, la resistenza parassita di quattro pod motore con eliche stazionarie aumenta la resistenza totale di circa il 5-10% [@bertaniPreliminaryDesignFixedwing2023]. Questo riduce il rapporto portanza-resistenza effettivo:

$$(L/D)_\text{QuadPlane} \approx 0.9000 \times (L/D)_\text{puro} = 0.9000 \times 11.68 = 10.51$$ {#eq:ld-quadplane}

Per i rotori ripiegati, la penalità di resistenza è minore (circa 2-5%), producendo $(L/D) \approx 0.9500 \times 11.68 = 11.10$.

Un valore di $(L/D)$ = 10.50 è adottato per l'analisi del QuadPlane, tenendo conto dei rotori fermi e della loro struttura di montaggio.

#### Potenza di crociera

Utilizzando i valori da @sec:derived-requirements:

Utilizzando i valori da @sec:derived-requirements ($V$ = 40.00 m/s, $(L/D)$ = 10.50, $\eta_\text{elica}$ = 0.5500, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza di crociera combinata è: $\eta_\text{crociera} = 0.5500 \times 0.8500 \times 0.9500 = 0.4436$.

Per l'MTOW di base = 10.00 kg (peso $W$ = 37.11 N):

$$P_\text{elettrica,crociera} = \frac{10.0 \times 3.711 \times 40}{10.5 \times 0.444} = \frac{1484}{4.66} = 318 \text{ W}$$ {#eq:cruise-power-value}

Questo è circa 10 volte inferiore alla potenza di hovering (3178 W), mostrando la differenza di potenza tra le modalità di hovering e crociera.

#### Energia di crociera

L'energia consumata durante le fasi di crociera è:

$$E_\text{crociera} = P_\text{elettrica,crociera} \times t_\text{crociera}$$ {#eq:cruise-energy}

dove $t_\text{crociera}$ = 57.00 min (da @tbl:mission-profile, volo totale 60 min meno 3 min hovering).

Convertendo in ore:

$$E_\text{crociera} = 318.5 \times (57.00/60.00) = 302.6 \text{ Wh}$$ {#eq:cruise-energy-value}

### Vincolo di accumulo energetico {#sec:energy-constraint}

Il vincolo di accumulo energetico è specifico per il VTOL ibrido, combinando le fasi di hovering ad alta intensità di potenza con la fase di crociera ad alta intensità di energia. Questo vincolo accoppia il profilo di missione all'allocazione di massa.

#### Requisito energetico totale

La batteria deve fornire energia per tutte le fasi di volo più una riserva energetica:

$$E_\text{richiesta} = E_\text{hover} + E_\text{crociera} + E_\text{riserva}$$ {#eq:energy-required}

La riserva energetica tiene conto di inefficienze di navigazione e correzioni di rotta, variazioni della densità atmosferica rispetto al modello, hovering esteso per atterraggio di precisione o abort, e capacità di ritorno di emergenza.

Una riserva energetica del 20% è adottata come coerente con la pratica aeronautica e l'approccio progettuale in @sec:mission-parameters:

$$E_\text{riserva} = 0.2000 \times (E_\text{hover} + E_\text{crociera})$$ {#eq:energy-reserve}

L'energia totale richiesta è quindi:

$$E_\text{richiesta} = 1.200 \times (E_\text{hover} + E_\text{crociera})$$ {#eq:energy-required-total}

Sostituendo i valori calcolati:

$$E_\text{richiesta} = 1.200 \times (158.9 + 302.6) = 1.200 \times 461.5 = 553.8 \text{ Wh}$$ {#eq:energy-required-value}

L'energia disponibile dalla batteria è determinata da @eq:battery-energy-fraction da @sec:battery-utilisation:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Sostituendo i valori da @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500, MTOW = 10.00 kg, $e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500):

$$E_\text{disponibile} = 0.3500 \times 10.00 \times 270.0 \times 0.8000 \times 0.9500 = 718.2 \text{ Wh}$$ {#eq:energy-available-value-qp}

#### Verifica del vincolo energetico

La missione è fattibile se:

$$E_\text{disponibile} \geq E_\text{richiesta}$$ {#eq:energy-feasibility}

Poiché 718.2 Wh ≥ 553.8 Wh, il vincolo energetico è soddisfatto.

Il margine energetico è:

$$\text{Margine} = \frac{E_\text{disponibile} - E_\text{richiesta}}{E_\text{richiesta}} = \frac{718.2 - 553.8}{553.8} = 29.7\%$$

Questo margine indica che il progetto di base soddisfa il vincolo energetico con adeguata riserva oltre al 20% già incluso. Questo margine può essere utilizzato per raggio di missione esteso (oltre i 50 km), operazioni di contingenza aggiuntive, aumento della massa del payload, o accomodamento della degradazione della batteria.

#### Vincolo della frazione di batteria

La frazione minima di batteria richiesta per la fattibilità della missione può essere derivata riarrangiando @eq:battery-energy-fraction e @eq:energy-required-total:

$$f_\text{batt,min} = \frac{1.20 \times (P_\text{hover} \times t_\text{hover} + P_\text{crociera} \times t_\text{crociera})}{MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}}$$ {#eq:f-batt-min}

Sostituendo i valori:

$$f_\text{batt,min} = \frac{553.8}{10.00 \times 270.0 \times 0.8000 \times 0.9500} = \frac{553.8}{2052} = 0.2699$$ {#eq:f-batt-min-value}

La frazione minima richiesta di batteria è 27.0%, inferiore all'allocazione di base del 35%. Questo conferma la fattibilità e fornisce flessibilità progettuale.

### Analisi della penalità di massa

La configurazione QuadPlane trasporta massa per entrambi i sistemi propulsivi, risultando in una penalità di peso rispetto a un aeromobile ad ala fissa puro.

#### Ripartizione della massa della doppia propulsione

Il sistema di sollevamento comprende motori, ESC, eliche e struttura di montaggio. Per l'aeromobile con MTOW di 10.00 kg, il sistema di sollevamento scala dai dati di riferimento: motori di sollevamento 4 × 0.2500 kg = 1.000 kg, ESC di sollevamento 4 × 0.0600 kg = 0.2400 kg, eliche di sollevamento 4 × 0.0400 kg = 0.1600 kg, e struttura di montaggio circa 0.3000 kg.

$$m_\text{sistema,sollevamento} = 1.000 + 0.2400 + 0.1600 + 0.3000 = 1.700 \text{ kg}$$ {#eq:lift-system-mass}

Il sistema di crociera comprende un singolo motore, ESC ed elica: motore di crociera circa 0.2000 kg, ESC di crociera circa 0.0500 kg, ed elica di crociera circa 0.0500 kg.

$$m_\text{sistema,crociera} = 0.2000 + 0.0500 + 0.0500 = 0.3000 \text{ kg}$$ {#eq:cruise-system-mass}

#### Calcolo della penalità di massa

Un ala fissa pura richiederebbe solo il sistema di crociera. Il QuadPlane aggiunge l'intero sistema di sollevamento come massa aggiuntiva:

$$\Delta m = m_\text{sistema,sollevamento} = 1.700 \text{ kg}$$ {#eq:mass-penalty}

Come frazione dell'MTOW:

$$f_\text{penalità} = \frac{m_\text{sistema,sollevamento}}{MTOW} = \frac{1.700}{10.00} = 0.1700 = 17.00\%$$ {#eq:mass-penalty-fraction}

Questa è una penalità di massa moderata che è accettabile data la capacità VTOL abilitante. Per confronto, i design commerciali QuadPlane mostrano frazioni di massa del sistema di sollevamento simili.

: Scalatura della penalità di massa con MTOW (stimata) {#tbl:mass-penalty-scaling}

| MTOW (kg) | $m_\text{sistema,sollevamento}$ stimata (kg) | $f_\text{penalità}$ |
|:----------|:-------------------------------------:|:------------------:|
| 5.0 | circa 0.9 | 18% |
| 10.0 (UAV marziano) | circa 1.7 | 17% |
| 14.0 (V25) | 1.42 | 10% |

Per l'UAV marziano, una penalità di massa di circa il 17% dell'MTOW è attesa per il sistema di sollevamento.

#### Compromesso della penalità di massa

La penalità di massa della doppia propulsione è accettabile perché abilita la fattibilità della missione. Il compromesso è:

Senza capacità VTOL, la missione è impossibile—non esistono mezzi di decollo o atterraggio su Marte senza infrastruttura di pista.

Con capacità VTOL, la missione diventa possibile con la penalità di massa.

La penalità di massa è il costo abilitante per la missione dell'UAV marziano, che non ha alternative per il decollo e atterraggio verticale da un ambiente abitativo.

### Analisi combinata dei vincoli

#### Riepilogo dei vincoli

Il QuadPlane deve soddisfare tutti i vincoli simultaneamente. @tbl:quadplane-constraints riassume i tipi di vincolo e le loro formulazioni matematiche.

: Riepilogo dei vincoli del QuadPlane {#tbl:quadplane-constraints}

| Vincolo | Formulazione | Tipo |
|:-----------|:------------|:-----|
| Potenza di hovering | $(P/W)_\text{hover} \geq f(DL, FM, \rho)$ | P/W minimo |
| Potenza di crociera | $(P/W)_\text{crociera} \geq f(V, L/D, \eta)$ | P/W minimo |
| Stallo | $W/S \leq f(\rho, V_\text{min}, C_{L,\text{max}})$ | W/S massimo |
| Energia | $E_\text{disponibile} \geq E_\text{richiesta}$ | Vincolo di accoppiamento |

La metodologia del diagramma di matching e l'analisi del diagramma dei vincoli sono presentate in @sec:comparative-results.

### Conclusione di fattibilità

#### Riepilogo del bilancio energetico

@tbl:energy-budget-quadplane presenta la ripartizione energetica completa per la configurazione QuadPlane.

: Riepilogo del bilancio energetico del QuadPlane {#tbl:energy-budget-quadplane}

| Componente | Potenza (W) | Tempo (min) | Energia (Wh) | Frazione |
|:----------|----------:|:----------:|------------:|---------:|
| Hovering (decollo + atterraggio) | 3178 | 3.00 | 158.9 | 34% |
| Crociera (transito + rilevamento) | 318.5 | 57.00 | 302.6 | 66% |
| Totale missione | - | 60.00 | 461.5 | 100% |
| Riserva (20%) | - | - | 92.30 | - |
| Totale richiesto | - | - | 553.8 | - |
| Disponibile | - | - | 718.2 | - |
| Margine | - | - | 164.4 | 29.7% |

![Visualizzazione del bilancio energetico del VTOL ibrido che mostra l'energia richiesta (hovering, crociera, riserva) rispetto all'energia della batteria disponibile. Il margine del 29.7% fornisce un adeguato buffer di sicurezza per le operazioni di missione.](figures/energy_budget_it.png){#fig:energy-budget width=80%}

L'analisi mostra che nonostante l'alto requisito di potenza durante l'hovering (3178 W), la breve durata dell'hovering (3 min) limita l'energia di hovering a solo il 34% del totale della missione. La maggior parte dell'energia è consumata durante la fase di crociera estesa, dove la configurazione ad ala fissa opera a potenza moderata (318 W).

@tbl:quadplane-feasibility confronta la capacità del QuadPlane con i requisiti di missione:

: Valutazione di fattibilità del QuadPlane {#tbl:quadplane-feasibility}

| Requisito | Obiettivo | Capacità QuadPlane | Stato |
|:------------|:-------|:---------------------|:------:|
| Capacità VTOL | Richiesta | Sì (rotori di sollevamento) | CONFORME |
| Autonomia di crociera | ≥60 min | 90.80 min (margine 51.3%) | CONFORME |
| Raggio operativo | ≥50 km | 106.4 km (margine 113%) | CONFORME |
| Tempo di hovering | 3 min | Limitato dalla batteria, non dall'architettura | CONFORME |

La configurazione VTOL ibrida (QuadPlane) soddisfa tutti i requisiti di missione con margine adeguato.

L'intuizione chiave è che limitando l'hovering a circa 3 minuti (5% del tempo di volo) e sfruttando l'aerodinamica dell'ala fissa per i restanti 57 minuti, il QuadPlane raggiunge un bilancio energetico fondamentalmente diverso dal velivolo a rotore puro. Un velivolo a rotore opera tutto il tempo di volo a basso L/D (circa 4.0) con alto consumo di potenza per tutto il tempo (459.7 W in crociera), risultando in autonomia insufficiente (57.27 min). Il QuadPlane, al contrario, opera solo le fasi di hovering (3 min) ad alta potenza (3178 W), mentre la fase di crociera (57 min) opera con L/D dell'ala (circa 10.5) a potenza moderata (318.5 W).

La valutazione di fattibilità per la configurazione QuadPlane è riassunta in @tbl:quadplane-feasibility. Il confronto delle configurazioni con le alternative a velivolo a rotore e ala fissa, la determinazione del punto di progetto, e la motivazione della selezione sono presentate in @sec:architecture-selection.
