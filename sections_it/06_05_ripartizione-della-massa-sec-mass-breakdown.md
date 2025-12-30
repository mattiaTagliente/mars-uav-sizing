# Decisioni progettuali

## Ripartizione della massa {#sec:mass-breakdown}

Questa sezione presenta la metodologia dettagliata di stima del peso dei componenti e la applica alla configurazione QuadPlane selezionata. La metodologia segue Sadraey [@sadraeyDesignUnmannedAerial2020; @sadraeyAircraftDesignSystems2013], adattata per le condizioni operative dell'UAV marziano e la geometria stabilita nell'analisi dei vincoli (@sec:constraint-analysis).

### Metodologia di stima del peso

#### Decomposizione del peso dell'UAV elettrico

Per gli UAV a batteria elettrica, l'MTOW si decompone in quattro elementi primari [@sadraeyDesignUnmannedAerial2020, Eq. 2.1]:

$$W_{TO} = W_{PL} + W_A + W_B + W_E$$ {#eq:sadraey-mtow}

dove:

* $W_{PL}$ = peso del payload (sensori di missione, camera, relè radio)
* $W_A$ = peso autopilota e avionica
* $W_B$ = peso batteria
* $W_E$ = peso a vuoto (struttura, propulsione, cablaggio, carrello)

Questo può essere riformulato in termini di frazioni di peso [@sadraeyDesignUnmannedAerial2020, Eq. 2.2b]:

$$W_{TO} = \frac{W_{PL} + W_A}{1 - \left(\frac{W_B}{W_{TO}}\right) - \left(\frac{W_E}{W_{TO}}\right)}$$ {#eq:mtow-fractions}

Una differenza chiave rispetto agli aeromobili a combustione è che la massa della batteria rimane costante durante tutto il volo, semplificando i calcoli del bilancio energetico ma richiedendo un dimensionamento accurato per soddisfare i requisiti di autonomia.

#### Dimensionamento della massa della batteria

La massa della batteria è determinata dai requisiti energetici della missione [@sadraeyDesignUnmannedAerial2020, Eq. 2.20]:

$$W_B = \sum_{i=1}^{n} \frac{P_i \cdot t_i \cdot g_\text{Marte}}{E_D}$$ {#eq:battery-sadraey}

dove:

* $P_i$ = potenza richiesta per il segmento di volo $i$ (W)
* $t_i$ = durata del segmento di volo $i$ (h)
* $E_D$ = densità energetica della batteria (Wh/kg)
* $g_\text{Marte}$ = accelerazione gravitazionale marziana (3.711 m/s²)
* $n$ = numero di segmenti di volo

La sommatoria tiene conto dei diversi requisiti di potenza nelle varie fasi di volo (decollo, salita, crociera, attesa, discesa, atterraggio). Per l'UAV marziano, i segmenti di hovering dominano il consumo energetico a causa dell'alta potenza richiesta nella rarefatta atmosfera.

### Stima del peso strutturale

I pesi dei componenti strutturali sono stimati utilizzando correlazioni semi-empiriche da Sadraey [@sadraeyAircraftDesignSystems2013], adattate per l'UAV marziano con fattore di carico ultimo ridotto.

#### Peso dell'ala

Il peso dell'ala è stimato da [@sadraeyAircraftDesignSystems2013, Eq. 10.3]:

$$W_W = S_W \cdot MAC \cdot \left(\frac{t}{c}\right)_{\max} \cdot \rho_{\text{mat}} \cdot K_\rho \cdot \left(\frac{AR \cdot n_{\text{ult}}}{\cos \Lambda_{0.25}}\right)^{0.6} \cdot \lambda^{0.04} \cdot g$$ {#eq:wing-weight}

dove:

* $S_W$ = superficie alare (m²)
* $MAC$ = corda aerodinamica media (m)
* $(t/c)_{\max}$ = rapporto di spessore massimo
* $\rho_{\text{mat}}$ = densità del materiale (kg/m³)
* $K_\rho$ = fattore di densità alare
* $AR$ = allungamento
* $n_{\text{ult}}$ = fattore di carico ultimo
* $\Lambda_{0.25}$ = angolo di freccia al quarto di corda
* $\lambda$ = rapporto di rastremazione

#### Peso della fusoliera

Il peso della fusoliera è stimato da [@sadraeyAircraftDesignSystems2013, Eq. 10.7]:

$$W_F = L_f \cdot D_{f_{\max}}^2 \cdot \rho_{\text{mat}} \cdot K_{\rho_f} \cdot n_{\text{ult}}^{0.25} \cdot K_{\text{inlet}} \cdot g$$ {#eq:fuselage-weight}

dove:

* $L_f$ = lunghezza della fusoliera (m)
* $D_{f_{\max}}$ = diametro massimo della fusoliera (m)
* $K_{\rho_f}$ = fattore di densità della fusoliera
* $K_{\text{inlet}} = 1$ per prese d'aria esterne

### Adattamento del fattore di carico

Il fattore di carico ultimo è definito come [@sadraeyAircraftDesignSystems2013, Eq. 10.4]:

$$n_{\text{ult}} = 1.5 \times n_{\max}$$ {#eq:n-ult-def}

dove il fattore di sicurezza di 1.5 è la pratica aerospaziale standard. Per l'UAV marziano, viene adottato un fattore di carico limite di $n_{\max} = 2.5$ (coerente con la metodologia della categoria normale CS-23, secondo @sec:derived-requirements), producendo:

$$n_{\text{ult}} = 1.5 \times 2.5 = 3.75$$

Questo è significativamente inferiore al valore CS-25 di circa 5.7 utilizzato nella progettazione degli aeromobili da trasporto, riflettendo:

* Operazione senza equipaggio (nessun rischio di lesioni all'equipaggio)
* Volo autonomo con inviluppo di manovra limitato
* Carichi di raffica ridotti nella rarefatta atmosfera marziana

#### Riduzione del peso dal fattore di carico

Da @eq:wing-weight, il peso dell'ala scala come $n_{\text{ult}}^{0.6}$. La riduzione di peso dall'utilizzo di $n_{\text{ult}} = 3.75$ invece di 5.7 è:

$$\frac{W_{W,Marte}}{W_{W,rif}} = \left(\frac{3.75}{5.7}\right)^{0.6} = 0.76$$

Questo rappresenta circa una **riduzione del 24% del peso dell'ala**.

Da @eq:fuselage-weight, il peso della fusoliera scala come $n_{\text{ult}}^{0.25}$:

$$\frac{W_{F,Marte}}{W_{F,rif}} = \left(\frac{3.75}{5.7}\right)^{0.25} = 0.90$$

Questo rappresenta circa una **riduzione del 10% del peso della fusoliera**.

#### Riduzione combinata del peso strutturale

Assumendo che ala e fusoliera contribuiscano in egual misura al peso strutturale, la riduzione media è di circa il 16-17%. Per un aeromobile con MTOW di 3.3 kg con una frazione di peso a vuoto di 0.45 (circa 1.5 kg), questo si traduce in circa 0.24-0.26 kg di risparmio di massa strutturale.

Questa riduzione di peso è un fattore abilitante significativo per la fattibilità della missione, poiché può essere riallocata alla capacità della batteria (estendendo l'autonomia) o al payload (migliorando la capacità di missione). Il fattore di carico ridotto è giustificato dall'operazione senza equipaggio, autonoma, e dai carichi di raffica ridotti nella rarefatta atmosfera marziana, come dettagliato in @sec:load-factor-selection.

### Applicazione al progetto QuadPlane

Utilizzando la geometria dall'analisi dei vincoli (@sec:constraint-analysis) e i risultati del diagramma di matching (@sec:comparative-results):

: Parametri di input per la ripartizione della massa {#tbl:mass-breakdown-inputs}

| Parametro | Valore | Fonte |
|:----------|------:|:-------|
| Superficie alare, $S_W$ | [DA CALCOLARE] | Analisi dei vincoli |
| Corda media, $MAC$ | [DA CALCOLARE] | Analisi dei vincoli |
| Allungamento, $AR$ | 12 | @sec:derived-requirements |
| Rapporto di spessore, $(t/c)$ | 0.09 | Profilo E387 |
| Rapporto di rastremazione, $\lambda$ | 0.5 | @sec:derived-requirements |
| Angolo di freccia, $\Lambda$ | 0° | @sec:derived-requirements |
| Fattore di carico ultimo, $n_{\text{ult}}$ | 3.75 | @sec:derived-requirements |
| Lunghezza fusoliera, $L_f$ | [DA CALCOLARE] | @sec:geometry-selection |
| Diametro fusoliera, $D_f$ | [DA CALCOLARE] | @sec:geometry-selection |

### Ripartizione della massa dei componenti

La ripartizione dettagliata della massa per la configurazione QuadPlane selezionata:

: Ripartizione della massa del QuadPlane {#tbl:quadplane-mass-breakdown}

| Componente | Massa (kg) | Frazione | Fonte |
|:----------|----------:|---------:|:-------|
| **Struttura** | | | |
| Ala | [DA CALCOLARE] | N.D. | @eq:wing-weight |
| Fusoliera | [DA CALCOLARE] | N.D. | @eq:fuselage-weight |
| Impennaggio | [DA CALCOLARE] | N.D. | Scalatura dall'ala |
| Boom | [DA CALCOLARE] | N.D. | Analisi strutturale |
| Carrello | [DA CALCOLARE] | N.D. | 3-5% dell'MTOW |
| **Propulsione** | | | |
| Motori di sollevamento (×8) | [DA CALCOLARE] | N.D. | Selezione componenti |
| Motori di crociera (×2) | [DA CALCOLARE] | N.D. | Selezione componenti |
| ESC | [DA CALCOLARE] | N.D. | Selezione componenti |
| Eliche | [DA CALCOLARE] | N.D. | Selezione componenti |
| **Energia** | | | |
| Batteria | [DA CALCOLARE] | N.D. | @eq:battery-sadraey |
| **Payload** | | | |
| Sistema camera | circa 0.30 | N.D. | @sec:payload-systems |
| Relè radio | circa 0.15 | N.D. | @sec:payload-systems |
| **Avionica** | | | |
| Controllore di volo | [DA CALCOLARE] | N.D. | Selezione componenti |
| Sensori e cablaggio | [DA CALCOLARE] | N.D. | 3-5% dell'MTOW |
| **MTOW totale** | [DA CALCOLARE] | 100% | N.D. |

### Limitazioni per piccoli UAV

Le equazioni di stima del peso da Sadraey [@sadraeyAircraftDesignSystems2013] sono state sviluppate principalmente per aeromobili convenzionali con equipaggio e potrebbero non essere direttamente applicabili a piccoli UAV in composito sotto i 50 kg di MTOW. Per affrontare questa limitazione:

1. **Validazione delle frazioni di massa**: I pesi stimati dei componenti sono verificati rispetto alle frazioni di massa empiriche da @tbl:design-mass-fractions derivate dai benchmark di UAV commerciali.

2. **Approccio conservativo**: Dove esiste incertezza, vengono utilizzate stime di peso conservative (più alte) per mantenere i margini di progetto.

3. **Iterazione con dati dei componenti**: La stima del peso viene raffinata dopo la selezione dei componenti (@sec:component-verification) utilizzando i dati effettivi del produttore per motori, batterie e avionica.

4. **Fattori dei materiali compositi**: I fattori di densità ($K_\rho$, $K_{\rho_f}$) sono regolati per riflettere la costruzione in CFRP piuttosto che in alluminio, secondo l'analisi dei compromessi sui materiali in @sec:materials-data.

### Verifica rispetto alle frazioni di massa

Le masse calcolate dei componenti sono verificate rispetto agli obiettivi delle frazioni di massa da @sec:initial-mass-estimate:

: Verifica delle frazioni di massa {#tbl:mass-fraction-verification}

| Categoria | Frazione target | Frazione calcolata | Stato |
|:---------|----------------:|--------------------:|:------:|
| Batteria | 0.35 | [DA CALCOLARE] | N.D. |
| Payload | 0.15 | [DA CALCOLARE] | N.D. |
| A vuoto (struttura) | 0.45 | [DA CALCOLARE] | N.D. |
| Propulsione | 0.15 | [DA CALCOLARE] | N.D. |
| Avionica | 0.05 | [DA CALCOLARE] | N.D. |
| **Totale** | 1.15 (con margine) | [DA CALCOLARE] | N.D. |
