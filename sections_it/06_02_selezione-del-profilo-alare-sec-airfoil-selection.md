# Decisioni progettuali

## Selezione del profilo alare {#sec:airfoil-selection}

Questa sezione presenta la logica di selezione del profilo alare per la progettazione dell'ala dell'UAV marziano sulla base dei dati prestazionali riassunti in @sec:aerodynamic-analysis. Il processo di selezione valuta sette profili candidati al numero di Reynolds target di circa 60,000, corrispondente alle condizioni di crociera su Marte.

### Criteri di selezione

La selezione del profilo alare è guidata da tre criteri primari, ponderati in base alla loro importanza per il successo della missione:

1. **Efficienza di crociera (peso 60%)**: Il rapporto portanza-resistenza massimo $(L/D)_\text{max}$ determina direttamente l'autonomia e la durata di crociera. Un $(L/D)_\text{max}$ più elevato riduce la potenza di crociera e prolunga la durata della batteria.

2. **Margine di stallo (peso 25%)**: Il coefficiente di portanza massimo $C_{L,\text{max}}$ determina la velocità minima di volo e fornisce margine contro raffiche o manovre. Un $C_{L,\text{max}}$ più elevato consente un'area alare più piccola o velocità di avvicinamento inferiori.

3. **Angolo di stallo (peso 15%)**: Un angolo di stallo $\alpha_\text{stallo}$ più elevato fornisce un inviluppo operativo più ampio e caratteristiche di stallo più graduali, migliorando la controllabilità nell'atmosfera marziana a bassa densità.

### Confronto prestazionale

I sette profili candidati da @tbl:airfoil-comparison presentano caratteristiche prestazionali distinte al numero di Reynolds target. @fig:airfoil-ld-alpha presenta le curve di efficienza che mostrano come il rapporto portanza-resistenza varia con l'angolo di attacco.

![Rapporto portanza-resistenza vs angolo di attacco per i profili candidati a Re ≈ 60,000. Mentre l'E387 raggiunge la massima efficienza di picco di (L/D)_max = 46.6, questo avviene molto vicino allo stallo. L'SD8000 raggiunge (L/D)_max = 45.4 con un margine maggiore rispetto allo stallo.](figures/airfoil_ld_alpha_it.png){#fig:airfoil-ld-alpha}

### Confronto dei profili

I sette profili candidati da @tbl:airfoil-comparison sono valutati rispetto ai tre criteri di selezione. Sulla base del punteggio ponderato, i profili si separano in tre livelli:

Il primo livello comprende l'E387, l'SD8000 e l'S7055, che raggiungono la massima efficienza di crociera con $(L/D)_\text{max}$ superiore a 41. L'E387 è in testa con $(L/D)_\text{max}$ = 46.6, seguito dall'SD8000 a 45.4 e dall'S7055 a 41.6. Questi tre profili forniscono anche coefficienti di portanza massima adeguati ($C_{L,\text{max}}$ = 1.15 a 1.23) per il carico alare previsto.

Il secondo livello include l'SD7037B e l'AG455ct-02r. L'SD7037B raggiunge un'efficienza moderata ($(L/D)_\text{max}$ = 36.6) con buone caratteristiche di stallo ($\alpha_\text{stallo}$ = 11.1°), ma la sua maggiore resistenza alle condizioni di crociera ne riduce la competitività. L'AG455ct-02r, progettato per velivoli senza coda, ha un coefficiente di portanza massimo inferiore ($C_{L,\text{max}}$ = 1.06) e opera a valori di $C_L$ inferiori, rendendolo meno adatto al carico alare richiesto dalle operazioni dell'UAV marziano.

Il terzo livello è costituito dall'AG12 e dall'AG35-r, entrambi profili a riflessione progettati per ali volanti. Le loro caratteristiche di momento di beccheggio autostabilizzante vengono a scapito dell'efficienza aerodinamica, con valori di $(L/D)_\text{max}$ di 34.6 e 30.7. Questi profili non sono adatti alla configurazione convenzionale con impennaggio adottata per questo progetto.

L'S7055 è escluso dalla considerazione finale nonostante il suo elevato $C_{L,\text{max}}$ = 1.23 perché va in stallo a $\alpha_\text{stallo}$ = 9.7°, il più basso di tutti i candidati. Questo stallo precoce non fornisce un margine sufficiente per un'operatività sicura nell'atmosfera marziana. I rimanenti candidati del primo livello, E387 e SD8000, sono confrontati in dettaglio.

L'analisi iniziale basata solo sui criteri ponderati favorirebbe l'E387 per il suo $(L/D)_\text{max}$ = 46.6 più elevato. Tuttavia, l'esame dei dati polari rivela una criticità operativa: l'efficienza di picco dell'E387 si verifica a α = 8.8°, solo 1.3° dal suo angolo di stallo di 10.2°. Questo margine ristretto solleva preoccupazioni per l'operatività pratica.

Inoltre, l'E387 presenta una riduzione anomala della resistenza a α ≈ 9° ($C_d$ = 0.0257) rispetto agli angoli adiacenti ($C_d$ = 0.0377 a α = 7° e $C_d$ = 0.0393 a α = 10.2°). Questo comportamento è attribuito al collasso della bolla di separazione laminare (LSB), un fenomeno ben documentato per questo profilo a bassi numeri di Reynolds [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:lsb -->. Sebbene fisicamente reale, questo punto operativo è sensibile e inaffidabile per la progettazione.

@tbl:e387-sd8000-comparison presenta un confronto dettagliato dei due candidati principali.

: Confronto tra i profili E387 e SD8000 a Re ≈ 60,000 {#tbl:e387-sd8000-comparison}

| Parametro | E387 | SD8000 | Vantaggio |
|:----------|-----:|-------:|:----------|
| Resistenza minima $C_{D,\text{min}}$ | 0.0228 | 0.0142 | SD8000 (38% inferiore) |
| Efficienza massima $(L/D)_\text{max}$ | 46.6 | 45.4 | E387 (3% superiore) |
| Portanza massima $C_{L,\text{max}}$ | 1.22 | 1.15 | E387 (6% superiore) |
| Angolo a $(L/D)_\text{max}$ | 8.8° | 7.0° | — |
| Angolo di stallo | 10.2° | 11.5° | SD8000 |
| Margine allo stallo | 1.3° | 4.6° | SD8000 (3.5× maggiore) |

L'SD8000 offre caratteristiche di resistenza superiori nell'intero intervallo operativo. Ai tipici coefficienti di portanza di crociera (0.7 < $C_L$ < 0.9), l'SD8000 raggiunge un L/D significativamente più alto dell'E387 grazie alla sua minore resistenza di profilo.

@fig:airfoil-polar presenta la polare di resistenza che mostra la relazione tra i coefficienti di portanza e resistenza. La resistenza costantemente inferiore dell'SD8000 è evidente nell'intervallo $C_L$ utilizzabile.

![Polare di resistenza per i profili candidati a Re ≈ 60,000. L'SD8000 presenta una resistenza costantemente inferiore all'E387 nell'intervallo operativo.](figures/airfoil_polar_it.png){#fig:airfoil-polar}

Le curve di portanza in @fig:airfoil-cl-alpha mostrano le caratteristiche di stallo di ciascun profilo. L'angolo di stallo più tardivo dell'SD8000 (11.5° vs 10.2°) fornisce un margine aggiuntivo per un'operatività sicura.

![Coefficiente di portanza vs angolo di attacco per i profili candidati a Re ≈ 60,000.](figures/airfoil_cl_alpha_it.png){#fig:airfoil-cl-alpha}

### Motivazione della selezione

Sulla base dell'analisi comparativa, il **Selig/Donovan SD8000** è selezionato per la progettazione dell'ala dell'UAV marziano. Mentre l'E387 raggiunge un'efficienza di picco marginalmente superiore, l'SD8000 offre vantaggi critici per un'operatività affidabile su Marte:

* **Minore resistenza nell'intervallo operativo**: $C_{D,\text{min}}$ = 0.0142, 38% inferiore all'E387
* **Maggiore margine di stallo**: 4.6° di margine tra il miglior L/D e lo stallo, rispetto a solo 1.3° per l'E387
* **Comportamento di resistenza coerente**: Nessuna transizione anomala o sensibilità alla dinamica delle LSB
* **Prestazioni robuste**: L/D più elevato alle condizioni di crociera pratiche ($C_L$ = 0.7–0.9)
* **Progettato per basso numero di Reynolds**: L'SD8000 è stato specificamente progettato da Selig e Donovan per applicazioni a basso Re, con prestazioni documentate in UAV e applicazioni simili [@seligSummaryLowSpeedAirfoil1995]<!-- #v1:sd8000 -->
* **Stallo tardivo**: Stallo a α = 11.5° fornisce un ampio inviluppo operativo

Il vantaggio di efficienza di picco del 3% dell'E387 è compensato dal rischio operativo di mirare a un angolo di attacco entro 1.3° dallo stallo. Per una missione su Marte senza opportunità di recupero, la selezione più conservativa dell'SD8000 fornisce un margine di sicurezza appropriato.

### Implicazioni progettuali

Il profilo SD8000 selezionato stabilisce i seguenti valori di progetto per l'analisi dei vincoli:

* Coefficiente di portanza massimo: $C_{L,\text{max}}$ = 1.15 (da dati galleria del vento UIUC)
* $(L/D)_\text{max}$ del profilo = 45.4 a $C_L$ = 0.94
* Rapporto di spessore: $t/c$ = 0.089 (8.9%)
* Coefficiente di resistenza minimo: $C_{D,\text{min}}$ = 0.0142

Questi valori sono utilizzati in @sec:aerodynamic-analysis per il modello della polare di resistenza e nell'analisi dei vincoli (@sec:hybrid-vtol-analysis) per i calcoli della velocità di stallo.

