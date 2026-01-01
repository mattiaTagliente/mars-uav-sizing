# Decisioni progettuali

## Ripartizione della massa {#sec:mass-breakdown}

Questa sezione presenta la metodologia dettagliata di stima del peso dei componenti e la applica alla configurazione QuadPlane selezionata. La metodologia segue Sadraey [@sadraeyDesignUnmannedAerial2020]<!-- #eq2.1 --> [@sadraeyAircraftDesignSystems2013]<!-- #eq10.3 -->, adattata per le condizioni operative dell'UAV marziano e la geometria stabilita nell'analisi dei vincoli (@sec:constraint-analysis).

### Metodologia di stima del peso

#### Decomposizione del peso dell'UAV elettrico

Per gli UAV a batteria elettrica, l'MTOW si decompone in quattro elementi primari [@sadraeyDesignUnmannedAerial2020, Eq. 2.1]<!-- #eq2.1 -->:

$$W_{TO} = W_{PL} + W_A + W_B + W_E$$ {#eq:sadraey-mtow}

dove:

* $W_{PL}$ = peso del payload (sensori di missione, camera, relè radio)
* $W_A$ = peso autopilota e avionica
* $W_B$ = peso batteria
* $W_E$ = peso a vuoto (struttura, propulsione, cablaggio, carrello)

Questo può essere riformulato in termini di frazioni di peso [@sadraeyDesignUnmannedAerial2020, Eq. 2.2b]<!-- #eq2.2b -->:

$$W_{TO} = \frac{W_{PL} + W_A}{1 - \left(\frac{W_B}{W_{TO}}\right) - \left(\frac{W_E}{W_{TO}}\right)}$$ {#eq:mtow-fractions}

Una differenza chiave rispetto agli aeromobili a combustione è che la massa della batteria rimane costante durante tutto il volo, semplificando i calcoli del bilancio energetico ma richiedendo un dimensionamento accurato per soddisfare i requisiti di autonomia.

#### Dimensionamento della massa della batteria

La massa della batteria è determinata dai requisiti energetici della missione [@sadraeyDesignUnmannedAerial2020, Eq. 2.20]<!-- #eq2.20 -->:

$$W_B = \sum_{i=1}^{n} \frac{P_i \cdot t_i \cdot g_\text{Marte}}{E_D}$$ {#eq:battery-sadraey}

dove:

* $P_i$ = potenza richiesta per il segmento di volo $i$ (W)
* $t_i$ = durata del segmento di volo $i$ (h)
* $E_D$ = densità energetica della batteria (Wh/kg)
* $g_\text{Marte}$ = accelerazione gravitazionale marziana (3.711 m/s²)
* $n$ = numero di segmenti di volo

La sommatoria tiene conto dei diversi requisiti di potenza nelle varie fasi di volo (decollo, salita, crociera, attesa, discesa, atterraggio). Per l'UAV marziano, i segmenti di hovering dominano il consumo energetico a causa dell'alta potenza richiesta nella rarefatta atmosfera.

### Stima del peso strutturale

I pesi dei componenti strutturali sono stimati utilizzando correlazioni semi-empiriche da Sadraey [@sadraeyAircraftDesignSystems2013]<!-- #eq10.3 -->, adattate per l'UAV marziano con fattore di carico ultimo ridotto.

#### Peso dell'ala

Il peso dell'ala è stimato da [@sadraeyAircraftDesignSystems2013, Eq. 10.3]<!-- #eq10.3 -->:

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

Il peso della fusoliera è stimato da [@sadraeyAircraftDesignSystems2013, Eq. 10.7]<!-- #eq10.7 -->:

$$W_F = L_f \cdot D_{f_{\max}}^2 \cdot \rho_{\text{mat}} \cdot K_{\rho_f} \cdot n_{\text{ult}}^{0.25} \cdot K_{\text{inlet}} \cdot g$$ {#eq:fuselage-weight}

dove:

* $L_f$ = lunghezza della fusoliera (m)
* $D_{f_{\max}}$ = diametro massimo della fusoliera (m)
* $K_{\rho_f}$ = fattore di densità della fusoliera
* $K_{\text{inlet}} = 1$ per prese d'aria esterne

### Adattamento del fattore di carico

Il fattore di carico ultimo è definito come [@sadraeyAircraftDesignSystems2013, Eq. 10.4]<!-- #eq10.4 -->:

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

Questo rappresenta circa una riduzione del 24% del peso dell'ala.

Da @eq:fuselage-weight, il peso della fusoliera scala come $n_{\text{ult}}^{0.25}$:

$$\frac{W_{F,Marte}}{W_{F,rif}} = \left(\frac{3.75}{5.7}\right)^{0.25} = 0.90$$

Questo rappresenta circa una riduzione del 10% del peso della fusoliera.

#### Riduzione combinata del peso strutturale

Assumendo che ala e fusoliera contribuiscano in egual misura al peso strutturale, la riduzione media è di circa il 16-17%. Per un aeromobile con MTOW di 10.0 kg con una frazione di peso a vuoto di 0.45 (circa 4.5 kg), questo si traduce in circa 0.72-0.77 kg di risparmio di massa strutturale.

Questa riduzione di peso è un fattore abilitante significativo per la fattibilità della missione, poiché può essere riallocata alla capacità della batteria (estendendo l'autonomia) o al payload (migliorando la capacità di missione). Il fattore di carico ridotto è giustificato dall'operazione senza equipaggio, autonoma, e dai carichi di raffica ridotti nella rarefatta atmosfera marziana, come dettagliato in @sec:load-factor-selection.

### Applicazione al progetto QuadPlane

Utilizzando la geometria dall'analisi dei vincoli (@sec:constraint-analysis) e i risultati del diagramma di matching (@sec:comparative-results):

: Parametri di input per la ripartizione della massa {#tbl:mass-breakdown-inputs}

| Parametro | Valore | Fonte |
|:----------|------:|:-------|
| Superficie alare, $S_W$ | 2.686 m² | Analisi dei vincoli |
| Corda media, $MAC$ | 0.669 m | Analisi dei vincoli |
| Apertura alare, $b$ | 4.01 m | Analisi dei vincoli |
| Allungamento, $AR$ | 6 | @sec:derived-requirements |
| Rapporto di spessore, $(t/c)$ | 0.089 | Profilo SD8000 |
| Rapporto di rastremazione, $\lambda$ | 0.5 | @sec:derived-requirements |
| Angolo di freccia, $\Lambda$ | 0° | @sec:derived-requirements |
| Fattore di carico ultimo, $n_{\text{ult}}$ | 3.75 | @sec:derived-requirements |
| Lunghezza fusoliera, $L_f$ | 2.00 m | @sec:geometry-selection |
| Diametro fusoliera, $D_f$ | 0.33 m | @sec:geometry-selection |

### Ripartizione della massa dei componenti

La ripartizione dettagliata della massa per la configurazione QuadPlane selezionata:

: Ripartizione della massa del QuadPlane {#tbl:quadplane-mass-breakdown}

| Componente | Massa (kg) | Frazione | Fonte |
|:----------|----------:|---------:|:-------|
| **Struttura** | 2.32 | 23.2% | |
| Ala | 0.80 | 8.0% | @eq:wing-weight con CFRP |
| Fusoliera | 0.45 | 4.5% | @eq:fuselage-weight con CFRP |
| Impennaggio (coda a V) | 0.35 | 3.5% | Scalatura dall'ala (1.144 m²) |
| Boom (4×) | 0.40 | 4.0% | Analisi strutturale |
| Carrello | 0.32 | 3.2% | 3.2% dell'MTOW |
| **Propulsione** | 1.18 | 11.8% | |
| Motori di sollevamento (8×) | 0.528 | 5.3% | SunnySky V4006-380, 66 g cad. |
| Motori di crociera (2×) | 0.120 | 1.2% | T-Motor AT2312-1150, 60 g cad. |
| ESC (10×) | 0.060 | 0.6% | Hobbywing XRotor Micro 30A, 6 g cad. |
| Eliche (10×) | 0.174 | 1.7% | 8× sollevamento (18 g) + 2× crociera (15 g) |
| Montaggio + cablaggio | 0.300 | 3.0% | Stima ingegneristica |
| **Energia** | 3.50 | 35.0% | |
| Pacco batteria | 3.50 | 35.0% | @sec:energy-data, 945 Wh totali |
| **Payload** | 1.50 | 15.0% | |
| Sistema camera | 0.30 | 3.0% | @sec:payload-systems |
| Relè radio | 0.15 | 1.5% | @sec:payload-systems |
| Margine payload | 1.05 | 10.5% | Tolleranza di crescita |
| **Avionica** | 0.50 | 5.0% | |
| Controllore di volo | 0.10 | 1.0% | Autopilota classe Pixhawk |
| Sensori e cablaggio | 0.40 | 4.0% | GPS, IMU, telemetria |
| **Subtotale** | 9.00 | 90.0% | |
| **Margine di progetto** | 1.00 | 10.0% | Contingenza |
| **MTOW totale** | 10.00 | 100% | — |

### Limitazioni per piccoli UAV

Le equazioni di stima del peso da Sadraey [@sadraeyAircraftDesignSystems2013]<!-- #ch10:limits --> sono state sviluppate principalmente per aeromobili convenzionali con equipaggio e potrebbero non essere direttamente applicabili a piccoli UAV in composito sotto i 50 kg di MTOW. Per affrontare questa limitazione:

1. Validazione delle frazioni di massa: i pesi stimati dei componenti sono verificati rispetto alle frazioni di massa empiriche da @tbl:design-mass-fractions derivate dai benchmark di UAV commerciali.

2. Approccio conservativo: dove esiste incertezza, vengono utilizzate stime di peso conservative (più alte) per mantenere i margini di progetto.

3. Iterazione con dati dei componenti: la stima del peso viene raffinata dopo la selezione dei componenti (@sec:component-verification) utilizzando i dati effettivi del produttore per motori, batterie e avionica.

4. Fattori dei materiali compositi: i fattori di densità ($K_\rho$, $K_{\rho_f}$) sono regolati per riflettere la costruzione in CFRP piuttosto che in alluminio, secondo l'analisi dei compromessi sui materiali in @sec:materials-data.

### Verifica rispetto alle frazioni di massa

Le masse calcolate dei componenti sono verificate rispetto agli obiettivi delle frazioni di massa da @sec:initial-mass-estimate:

: Verifica delle frazioni di massa {#tbl:mass-fraction-verification}

| Categoria | Frazione target | Frazione calcolata | Stato |
|:---------|----------------:|--------------------:|:------:|
| Batteria | 0.35 | 0.35 | CONFORME |
| Payload | 0.15 | 0.15 | CONFORME |
| Struttura | 0.23 | 0.23 | CONFORME |
| Propulsione | 0.20 | 0.12 | INFERIORE (margine disponibile) |
| Avionica | 0.05 | 0.05 | CONFORME |
| Margine di progetto | — | 0.10 | ALLOCATO |
| **Totale** | 1.00 | 1.00 | BILANCIATO |

La frazione di massa della propulsione (11.8%) è significativamente inferiore al budget del 20%, fornendo un margine di 0.82 kg che è stato riallocato alla struttura e alla contingenza di progetto. Questo margine riflette la selezione di combinazioni moderne di motori/ESC leggeri e valida le ipotesi dell'analisi dei vincoli.
