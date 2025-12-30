# Dati di riferimento e analisi dei compromessi

## Analisi aerodinamica e dati dei profili alari {#sec:aerodynamic-analysis}

### Volo a basso numero di Reynolds {#sec:low-reynolds}

La combinazione di bassa densità atmosferica e velocità di volo moderate su Marte risulta in numeri di Reynolds molto inferiori ai tipici aeromobili terrestri. A bassi numeri di Reynolds (sotto circa 100.000), gli effetti viscosi dominano le prestazioni aerodinamiche. La transizione dello strato limite, le bolle di separazione laminare e il comportamento della separazione del flusso differiscono sostanzialmente dalle condizioni ad alto Reynolds, degradando le prestazioni del profilo rispetto alle previsioni teoriche.

Numeri di Reynolds molto bassi sono dannosi per l'efficienza aerodinamica a causa di questi effetti viscosi. Tuttavia, raggiungere numeri di Reynolds più elevati richiede o una corda maggiore (aumentando massa e superficie alare) o velocità più elevata (aumentando la potenza di crociera, poiché la potenza scala con $V^3$ quando la resistenza parassita domina). Viene adottato un numero di Reynolds target di circa 60.000 come compromesso: fornisce prestazioni del profilo accettabili basate sui dati sperimentali in galleria del vento disponibili, limitando al contempo la corda alare e la velocità di crociera a valori ragionevoli.
I valori specifici di velocità di crociera e corda che raggiungono questo obiettivo sono derivati in @sec:derived-requirements basandosi sui vincoli accoppiati di numero di Mach, numero di Reynolds e geometria alare.

### Dati sperimentali dei profili {#sec:airfoil-data}

Sono stati valutati sette profili a basso Reynolds utilizzando dati sperimentali dal programma UIUC Low-Speed Airfoil Tests [@seligSummaryLowSpeedAirfoil1995; @williamsonSummaryLowSpeedAirfoil2012]. I candidati includono l'Eppler 387 (E387), ampiamente studiato per applicazioni a basso Reynolds con estesa validazione sperimentale; l'SD8000, un design a bassa resistenza ottimizzato per la minima resistenza di profilo; l'S7055, un design a camber moderato che bilancia portanza e resistenza; l'AG455ct-02r e l'AG35-r, profili sottili con riflessione progettati per ali volanti e aeromobili senza coda; l'SD7037B, un popolare profilo general-purpose a basso Reynolds; e l'AG12, un profilo sottile a basso camber per applicazioni ad alta velocità.

A numeri di Reynolds inferiori a 100.000, i calcoli dello strato limite XFOIL mostrano difficoltà di convergenza dovute alle bolle di separazione laminare e ai fenomeni di transizione. I dati sperimentali in galleria del vento dal database UIUC forniscono caratteristiche prestazionali validate a queste condizioni. I dati prestazionali a $Re \approx 60{,}000$ sono riassunti in @tbl:airfoil-comparison.

: Prestazioni dei profili a Re ≈ 60.000 da dati sperimentali UIUC [@seligSummaryLowSpeedAirfoil1995; @williamsonSummaryLowSpeedAirfoil2012] {#tbl:airfoil-comparison}

| Profilo | Re test | $C_{L,\text{max}}$ | $\alpha_\text{stallo}$ | $(L/D)_\text{max}$ | $C_L$ a $(L/D)_\text{max}$ | Fonte |
|:--------|--------:|-------------------:|----------------------:|-------------------:|----------------------------:|:-------|
| E387    |  61.000 |               1.22 |                 10.2° |               46.6 |                        1.20 | Vol. 1 |
| SD8000  |  60.800 |               1.15 |                 11.5° |               45.4 |                        0.94 | Vol. 1 |
| S7055   |  60.700 |               1.23 |                  9.7° |               41.6 |                        1.23 | Vol. 1 |
| AG455ct |  60.157 |               1.06 |                  9.2° |               40.0 |                        0.56 | Vol. 5 |
| SD7037B |  60.500 |               1.22 |                 11.1° |               36.6 |                        0.92 | Vol. 1 |
| AG12    |  59.972 |               1.06 |                 10.3° |               34.6 |                        0.71 | Vol. 5 |
| AG35-r  |  59.904 |               1.04 |                 11.4° |               30.7 |                        0.96 | Vol. 5 |

I profili della serie AG con riflessione (AG455ct-02r, AG35-r) sono progettati per aeromobili senza coda con caratteristiche di momento picchiante auto-stabilizzanti, il che riduce la loro efficienza aerodinamica rispetto ai profili convenzionali con camber. Per scopi di dimensionamento, il coefficiente di portanza massimo è assunto come $C_{L,\text{max}}$ = 1.2 basandosi sui dati sperimentali, rappresentando prestazioni tipiche per i profili candidati. La selezione specifica del profilo, basata sul compromesso tra L/D massimo, coefficiente di portanza a massima efficienza e altre caratteristiche, è presentata in @sec:airfoil-selection.

### Modello della polare di resistenza

La polare di resistenza dell'aeromobile è modellata come:

$$C_D = C_{D,0} + \frac{C_L^2}{\pi \cdot AR \cdot e}$$ {#eq:drag-polar}

dove $C_{D,0}$ è il coefficiente di resistenza a portanza nulla, $AR$ è l'allungamento alare, e $e$ è il fattore di efficienza di Oswald [@sadraeyAircraftDesignSystems2013].

#### Fattore di efficienza di Oswald

Il fattore di efficienza di Oswald tiene conto della deviazione dalla distribuzione di portanza ellittica ideale e da altre sorgenti di resistenza indotta. Per ali dritte (non a freccia), Sadraey fornisce la correlazione empirica [@sadraeyAircraftDesignSystems2013]:

$$e = 1.78 \times (1 - 0.045 \times AR^{0.68}) - 0.64$$ {#eq:oswald-correlation}

Questa correlazione è valida per allungamenti nell'intervallo 6-20. Applicando @eq:oswald-correlation per gli allungamenti di interesse si ottengono i valori in @tbl:oswald-values.

: Fattore di efficienza di Oswald dalla correlazione di Sadraey [@sadraeyAircraftDesignSystems2013] {#tbl:oswald-values}

| Allungamento | $e$ (calcolato) |
|:-------------|:----------------:|
| 5            | 0.90             |
| 6            | 0.87             |
| 7            | 0.84             |

I valori tipici del fattore di efficienza di Oswald variano da 0.7 a 0.95 [@sadraeyAircraftDesignSystems2013]. La correlazione fornisce $e$ = 0.87 per l'allungamento di base di 6, che rientra nell'intervallo atteso. La maggiore efficienza di Oswald ad allungamenti inferiori compensa parzialmente l'aumento della resistenza indotta, migliorando il compromesso.

#### Coefficiente di resistenza a portanza nulla

Il coefficiente di resistenza a portanza nulla è stimato utilizzando il metodo dell'attrito pellicolare equivalente [@gottenFullConfigurationDrag2021]:

$$C_{D,0} = C_{f,\text{eq}} \times \frac{S_\text{wet}}{S_\text{ref}}$$ {#eq:cd0-method}

dove $C_{f,\text{eq}}$ è un coefficiente di attrito equivalente per la categoria di aeromobile, $S_\text{wet}$ è l'area bagnata totale, e $S_\text{ref}$ è l'area alare di riferimento.

Götten et al. hanno analizzato dieci UAV da ricognizione e hanno trovato che componenti vari come carrello fisso e torrette sensori contribuiscono al 36-60% della resistenza parassita totale [@gottenFullConfigurationDrag2021]. Il loro coefficiente di attrito equivalente derivato per UAV a corto-medio raggio è $C_{f,\text{eq}}$ = 0.0128, significativamente più alto delle categorie di aeromobili con equipaggio.

Per l'UAV marziano, diversi fattori suggeriscono che un $C_{f,\text{eq}}$ più basso sia appropriato: nessun carrello fisso (operazioni VTOL dall'habitat), nessuna torretta sensori esterna (camera integrata nel vano payload), design aerodinamico pulito con meno protuberanze, e rotori VTOL fermi o in bandiera durante la crociera. Viene adottato un valore di $C_{f,\text{eq}}$ = 0.0055, corrispondente ad aeromobili leggeri puliti. Con un rapporto area bagnata stimato di $S_\text{wet}/S_\text{ref} \approx 5.5$ per la configurazione QuadPlane (considerando fusoliera, bracci della coda e rotori VTOL):

$$C_{D,0} = 0.0055 \times 5.5 = 0.030$$ {#eq:cd0-calculation}

Questo valore è coerente con le stime statistiche per aeromobili leggeri puliti ($C_{D,0}$ = 0.020-0.030) e piccoli UAV senza carrello fisso.

#### Polare di resistenza completa

Con i coefficienti stimati, la polare di resistenza completa per $AR$ = 6 è:

$$C_D = 0.03000 + \frac{C_L^2}{\pi \times 6 \times 0.8692} = 0.03000 + 0.06103 \times C_L^2$$ {#eq:drag-polar-ar6}

Il fattore di resistenza indotta è $K = 1/(\pi \cdot AR \cdot e)$ = 0.06103.

Il rapporto portanza/resistenza massimo si verifica quando la resistenza indotta eguaglia la resistenza parassita:

$$(L/D)_\text{max} = \frac{1}{2}\sqrt{\frac{\pi \cdot AR \cdot e}{C_{D,0}}} = \frac{1}{2}\sqrt{\frac{\pi \times 6 \times 0.8692}{0.03000}} = 11.68$$ {#eq:ld-max-calculated}

Il coefficiente di portanza corrispondente al L/D massimo è:

$$C_{L}^{*} = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = \sqrt{\pi \times 6 \times 0.8692 \times 0.03000} = 0.7011$$ {#eq:cl-optimum}

Il $(L/D)_\text{max}$ dell'aeromobile di 11.68 è inferiore al $(L/D)_\text{max}$ 2D del profilo di 46.60 per l'E387. Questa riduzione è attesa perché la resistenza dell'aeromobile include effetti di fusoliera, coda, interferenza e resistenza indotta tridimensionale non presenti nei test 2D del profilo. Il minor allungamento rispetto agli alianti ad alta efficienza risulta in una maggiore resistenza indotta, che domina il bilancio di resistenza ai coefficienti di portanza moderati richiesti per il volo marziano.

### Riepilogo dei coefficienti aerodinamici

@tbl:aero-coefficients riassume i parametri aerodinamici per l'analisi dei vincoli.

: Coefficienti aerodinamici per l'analisi dei vincoli dell'UAV marziano {#tbl:aero-coefficients}

| Parametro | Simbolo | Valore | Fonte |
|:----------|:------:|:-----:|:-------|
| Coefficiente di portanza massimo | $C_{L,\text{max}}$ | 1.200 | Galleria del vento UIUC |
| Fattore di efficienza di Oswald | $e$ | 0.8692 | Correlazione Sadraey (AR = 6) |
| Coefficiente di resistenza a portanza nulla | $C_{D,0}$ | 0.03000 | Metodo attrito equivalente |
| Allungamento | $AR$ | 6 | Selezione di progetto |
| Rapporto portanza/resistenza massimo | $(L/D)_\text{max}$ | 11.68 | Calcolato |
| Coefficiente di portanza a $(L/D)_\text{max}$ | $C_L^{*}$ | 0.7011 | Calcolato |

Questi valori sono utilizzati nell'analisi dei vincoli (@sec:constraint-analysis) per determinare i limiti dello spazio di progetto per carico di potenza e carico alare.
