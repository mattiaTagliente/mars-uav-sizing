# Decisioni progettuali

## Selezione della geometria {#sec:geometry-selection}

Questa sezione presenta le selezioni dei parametri geometrici per l'UAV marziano, consolidando le decisioni sulla configurazione della coda e della fusoliera con le specifiche della geometria alare.

### Geometria alare

La geometria alare deriva direttamente dai risultati dell'analisi dei vincoli (@sec:comparative-results):

| Parametro | Valore | Fonte |
|:----------|------:|:-------|
| Carico alare, $W/S$ | 13.82 N/m² | Vincolo di stallo a $V_\text{min}$ = 35.04 m/s |
| Superficie alare, $S$ | 2.686 m² | $S = W/(W/S)$ con MTOW di 10 kg |
| Apertura alare, $b$ | 4.01 m | $b = \sqrt{AR \times S}$ con AR = 6 |
| Corda aerodinamica media, $MAC$ | 0.669 m | $MAC = S/b$ |
| Allungamento, $AR$ | 6 | Selezionato dall'analisi dei compromessi |
| Rapporto di rastremazione, $\lambda$ | 0.5 | @sec:derived-requirements |
| Angolo di freccia, $\Lambda$ | 0° | @sec:derived-requirements |

: Parametri della geometria alare {#tbl:wing-geometry}

L'allungamento di 6 rappresenta un compromesso tra efficienza aerodinamica (un AR più alto aumenta L/D) e peso strutturale (un AR più alto aumenta i carichi flessionali dell'ala). La configurazione non rastremata e senza freccia minimizza la complessità di fabbricazione e il rischio di stallo all'estremità a bassi numeri di Reynolds.

### Selezione della configurazione della coda

Sulla base dell'analisi dei compromessi in @sec:tail-data, viene selezionata una configurazione a V invertita montata su boom. Questa scelta sfrutta i boom strutturali già richiesti per i motori di sollevamento dell'octocopter.

I boom dei motori di sollevamento posteriori si estendono verso poppa per supportare le superfici di coda, eliminando la necessità di una struttura di boom di coda separata e riducendo la massa strutturale complessiva. La configurazione montata su boom fornisce un braccio di momento più lungo di quello che consentirebbe una coda montata sulla fusoliera con la fusoliera compatta selezionata per questo progetto, compensando la ridotta efficacia di controllo ai numeri di Reynolds marziani. La geometria a V invertita inclina le superfici verso l'alto rispetto all'asse della fusoliera, fornendo spazio dalla superficie durante l'atterraggio su terreno irregolare. Le superfici della coda a V sono posizionate al di fuori del getto dell'elica di crociera (configurazione trattrice a prua), assicurando un flusso d'aria indisturbato sulle superfici di controllo.

La disposizione a V invertita combina il controllo di beccheggio e imbardata in due superfici con miscelazione in stile ruddervator. Studi CFD sulle configurazioni di impennaggio montato su boom hanno trovato che i design a U invertita su boom fornivano stabilità longitudinale superiore e caratteristiche di stallo per missioni di sorveglianza [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:inverted-u -->, e il design a due superfici riduce il conteggio dei pezzi rispetto a una coda convenzionale a tre superfici.

#### Dimensionamento della coda

Il dimensionamento delle superfici di coda per le condizioni marziane richiede un'attenta considerazione degli effetti del numero di Reynolds. Alla densità atmosferica marziana, le superfici di coda operano a numeri di Reynolds significativamente più bassi degli equivalenti terrestri, riducendo l'efficacia delle superfici di controllo. Seguendo il metodo dei coefficienti di volume [@roskamAirplaneDesign22004]<!-- #s8.1 -->, le aree di coda orizzontale e verticale sono determinate da:

$$\bar{V}_H = \frac{x_H \cdot S_H}{S \cdot \bar{c}}$$ {#eq:vh-coeff}

$$\bar{V}_V = \frac{x_V \cdot S_V}{S \cdot b}$$ {#eq:vv-coeff}

dove $\bar{V}_H$ e $\bar{V}_V$ sono i coefficienti di volume della coda orizzontale e verticale, $x_H$ e $x_V$ sono i bracci di momento, $S$ è la superficie alare, $\bar{c}$ è la corda aerodinamica media e $b$ è l'apertura alare [@roskamAirplaneDesign22004]<!-- #eq8.1-8.2 -->. Risolvendo per le aree di coda:

$$S_H = \frac{\bar{V}_H \cdot S \cdot \bar{c}}{x_H}$$ {#eq:vtail-vh}

$$S_V = \frac{\bar{V}_V \cdot S \cdot b}{x_V}$$ {#eq:vtail-vv}

Per una configurazione butterfly (coda a V), le aree effettive orizzontali e verticali sono proiezioni dell'area planimetrica totale della coda a V sui piani di riferimento [@roskamAirplaneDesign22004]<!-- #eq8.5 -->:

$$S_{H,\text{eff}} = S_{V\text{-tail}} \cos^2 \Gamma, \quad S_{V,\text{eff}} = S_{V\text{-tail}} \sin^2 \Gamma$$ {#eq:vtail-area}

L'angolo diedro butterfly segue da:

$$\Gamma = \arctan\left(\sqrt{\frac{S_V}{S_H}}\right)$$ {#eq:butterfly-angle}

I coefficienti di volume target sono aumentati del 25% rispetto ai valori tipici per compensare la ridotta efficacia di controllo ai numeri di Reynolds marziani, dando $\bar{V}_H$ = 0.45 e $\bar{V}_V$ = 0.035. Con un braccio di momento della coda di $x_H$ = 1.20 m (fornito dall'estensione del boom a poppa della fusoliera), le aree richieste sono:

| Parametro | Valore | Note |
|:----------|------:|:------|
| Diedro della coda a V, $\Gamma$ | 40° | Bilancia autorità di beccheggio/imbardata |
| Area totale coda a V, $S_{V\text{-tail}}$ | 1.144 m² | Vincolata dal beccheggio |
| Apertura coda a V, $b_{V\text{-tail}}$ | 2.14 m | Con AR = 4.0 |
| Corda media coda a V, $c_{V\text{-tail}}$ | 0.535 m | $S/b$ |
| Rapporto area coda/ala | 42.6% | Maggiore che sulla Terra a causa del basso Re |
| Braccio di momento coda, $l_H$ | 1.20 m | Estensione boom a poppa della fusoliera |

: Parametri della geometria della coda a V {#tbl:vtail-geometry}

Il vincolo orizzontale (beccheggio) è attivo, il che significa che la coda è dimensionata principalmente per un'adeguata stabilità di beccheggio. La componente verticale (imbardata) a 40° di diedro supera i requisiti del 51%, fornendo adeguata stabilità e autorità di controllo direzionale per le operazioni con vento trasversale.

### Selezione della geometria della fusoliera

I benchmark commerciali mostrano un rapporto lunghezza-apertura alare che varia da 0.28 a 0.63, con una mediana di circa 0.50 (@tbl:reference-fuselage). La selezione comporta trade-off tra effetti in competizione:

**Fusoliera più corta (rapporto inferiore):**

* Meno massa strutturale della fusoliera
* Meno area bagnata della fusoliera (resistenza parassitica ridotta)
* Richiede estensione del boom per il braccio di momento della coda
* Meno volume interno

**Fusoliera più lunga (rapporto superiore):**

* Maggiore contributo di portanza della fusoliera
* Braccio di momento della coda più lungo senza estensione boom
* Più volume interno per crescita del payload e gestione termica
* Più massa strutturale della fusoliera
* Più area bagnata della fusoliera

**Selezione: 0.30** (limite inferiore dell'intervallo benchmark)

Per l'UAV marziano, la maggior parte del volume interno è occupata dal payload compatto e dai sistemi di accumulo energetico che richiedono solo 4–5 L. Il volume di 170 L fornito dal rapporto 0.50 è eccessivo. Selezionando il limite inferiore dell'intervallo benchmark (0.30) si minimizza la massa strutturale e la resistenza parassitica fornendo al contempo volume adeguato per tutti i sistemi. Il braccio di momento della coda richiesto è invece ottenuto attraverso l'estensione del boom, che è strutturalmente efficiente poiché serve al duplice scopo di supportare sia i rotori di sollevamento che le superfici della coda a V.

Le dimensioni risultanti della fusoliera sono:

$$L_f = 0.30 \times b = 0.30 \times 4.01 = 1.20 \text{ m}$$

Con rapporto di finezza 6 e sezione circolare:

$$D_f = \frac{L_f}{FR} = \frac{1.20}{6} = 0.20 \text{ m}$$

$$V_f = \frac{\pi}{4} D_f^2 \times L_f = \frac{\pi}{4} \times 0.20^2 \times 1.20 = 0.038 \text{ m}^3 = 38 \text{ L}$$

I payload e i sistemi richiedono circa 4–5 L di volume interno, fornendo un margine adeguato per sistemi di gestione termica, passaggio cavi e crescita futura del payload all'interno dei 38 L disponibili.

#### Dimensioni della fusoliera

I seguenti valori sono derivati dal rapporto lunghezza-apertura alare selezionato e dal vincolo di rapporto di finezza:

| Parametro | Simbolo | Valore | Note |
|:----------|:------:|------:|:------|
| Lunghezza fusoliera | $L_f$ | 1.20 m | 0.30 × 4.01 m (limite inferiore benchmark) |
| Diametro massimo | $D_f$ | 0.20 m | $L_f$/6 (rapporto finezza 6) |
| Rapporto di finezza | $L_f/D_f$ | 6 | Profilo a bassa resistenza [@gottenFullConfigurationDrag2021]<!-- #s:fineness --> |
| Rapporto lunghezza-apertura alare | $L_f/b$ | 0.30 | Limite inferiore benchmark (volume minimo necessario) |
| Volume interno | $V_f$ | 38 L | $\pi/4 \times D_f^2 \times L_f$ |
| Altezza (con carrello) | $H$ | 0.50 m | Spazio da terra per eliche |

: Parametri della geometria della fusoliera {#tbl:fuselage-geometry}

La sezione trasversale della fusoliera è approssimativamente circolare per semplificare l'analisi strutturale e la fabbricazione. L'integrazione del payload e la disposizione interna dettagliata sono affrontate in @sec:component-verification.

#### Lunghezza totale dell'aeromobile {#sec:total-aircraft-length}

La configurazione della coda a V montata su boom si estende oltre l'estremità poppiera della fusoliera. La lunghezza totale dell'aeromobile è determinata dalla posizione della coda richiesta per raggiungere il braccio di momento target:

**Posizione dell'ala:**

$$x_\text{ala,LE} = 0.40 \times L_f = 0.40 \times 1.20 = 0.48 \text{ m dal muso}$$

$$x_\text{ala,AC} = x_\text{ala,LE} + 0.25 \times MAC = 0.48 + 0.25 \times 0.669 = 0.65 \text{ m}$$

**Posizione della coda (da CA ala + braccio di momento):**

$$x_\text{coda,AC} = x_\text{ala,AC} + l_H = 0.65 + 1.20 = 1.85 \text{ m dal muso}$$

**Bordo d'uscita coda (CA al 25% corda dal bordo d'attacco):**

$$x_\text{coda,TE} = x_\text{coda,AC} + 0.75 \times c_{V\text{-tail}} = 1.85 + 0.75 \times 0.535 = 2.25 \text{ m}$$

La lunghezza totale dell'aeromobile è quindi **2.25 m**, con i boom di coda che si estendono **1.05 m** oltre l'estremità poppiera della fusoliera. Questa estensione del boom è strutturalmente integrata con i bracci dei motori di sollevamento posteriori, che servono al duplice scopo di supportare i rotori dell'octocopter e le superfici della coda a V.

| Parametro | Simbolo | Valore | Note |
|:----------|:------:|------:|:------|
| Lunghezza fusoliera | $L_f$ | 1.20 m | Vano payload e sistemi |
| Estensione boom a poppa | $\Delta L$ | 1.05 m | Struttura di supporto coda |
| Lunghezza totale aeromobile | $L_\text{totale}$ | 2.25 m | Dal muso al bordo d'uscita coda |

: Ripartizione lunghezza totale aeromobile {#tbl:total-length}

### Dimensionamento delle eliche {#sec:propeller-sizing}

La configurazione QuadPlane richiede due tipi di eliche: eliche di sollevamento per il sistema VTOL octocopter e eliche di crociera per il volo orizzontale. Entrambe sono dimensionate utilizzando la teoria della quantità di moto [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #ch2 --> con vincoli sul numero di Mach per prevenire perdite di comprimibilità alle estremità delle pale.

#### Dimensionamento eliche di sollevamento

Gli otto motori di sollevamento devono generare spinta sufficiente per l'hovering. Dalla teoria della quantità di moto, il carico del disco $DL$ è definito come spinta per unità di area del disco [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #eq2.13 -->:

$$DL = \frac{T}{A} = \frac{T}{\pi D_p^2 / 4}$$ {#eq:disk-loading}

Risolvendo per il diametro dell'elica:

$$D_p = \sqrt{\frac{4T}{\pi \cdot DL}}$$ {#eq:lift-prop-dia}

Con il carico del disco di progetto di 30.0 N/m² da @sec:derived-requirements e requisito di spinta in hovering di MTOW / 8 = 4.64 N per motore:

$$D_p = \sqrt{\frac{4 \times 4.64}{\pi \times 30.0}} = 0.44 \text{ m}$$

Il numero di Mach all'estremità è verificato rispetto alla velocità del suono su Marte (229.7 m/s a 210 K). L'efficienza dell'elica degrada quando il Mach all'estremità supera circa 0.7 a causa degli effetti di comprimibilità [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #s:compressibility -->:

$$M_\text{tip} = \frac{\pi n D_p}{a}$$ {#eq:tip-mach}

dove $n$ è la velocità di rotazione (giri/s) e $a$ è la velocità del suono. Usando un margine del 70% al limite di Mach si ottengono 4850 rpm con diametro di 0.44 m:

$$M_\text{tip} = \frac{\pi \times (4850/60) \times 0.44}{229.7} = 0.49$$

Questo è inferiore al limite di 0.7, quindi non si applica alcun vincolo sulla velocità dell'estremità. Il diametro teorico dal carico del disco è 0.44 m. Il diametro selezionato dell'elica di sollevamento è **0.36 m** (14 pollici), basato sulle dimensioni disponibili e sulla compatibilità con il motore.

#### Dimensionamento eliche di crociera

I due motori di crociera forniscono spinta in avanti durante il volo orizzontale. Dalla teoria del disco attuatore [@leishmanPrinciplesHelicopterAerodynamics2006]<!-- #ch2 -->, la potenza indotta è:

$$P_\text{indotta} = T v_i = \frac{T^{3/2}}{\sqrt{2 \rho A}}$$ {#eq:induced-power}

La spinta di crociera è fissata dal requisito di resistenza aerodinamica, $T = W/(L/D)$. Per la configurazione di base, la spinta totale in crociera è 3.53 N (1.76 N per motore). Il diametro selezionato dell'elica di crociera è **0.31 m** (12 pollici). A 8000 rpm, il numero di Mach all'estremità è 0.56, inferiore al limite di 0.7.

| Parametro | Elica di sollevamento | Elica di crociera |
|:----------|----------------------:|------------------:|
| Diametro | 0.36 m | 0.31 m |
| Quantità | 8 | 2 |
| Numero pale | 2 | 2 |
| Velocità operativa | 4850 rpm | 8000 rpm |
| Numero di Mach estremità | 0.49 | 0.56 |

: Riepilogo geometria eliche {#tbl:propeller-summary}

