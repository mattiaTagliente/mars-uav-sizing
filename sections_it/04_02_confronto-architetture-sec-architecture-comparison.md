# Dati di riferimento e analisi dei compromessi

## Confronto architetture {#sec:architecture-comparison}

### Architettura di volo

Tre architetture sono considerate per il volo atmosferico su Marte: ad ala rotante, ad ala fissa e VTOL ibrido. Ognuna presenta distinti compromessi tra flessibilità operativa ed efficienza energetica.

#### Ala rotante

I progetti puramente ad ala rotante forniscono decollo e atterraggio verticali senza richiedere superfici preparate. L'elicottero Ingenuity della NASA ha dimostrato questo approccio, completando 72 voli su Marte [@tzanetosIngenuityMarsHelicopter2022]<!-- #abs --> [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights -->. Tuttavia, gli aeromobili a rotore soffrono di scarsa efficienza in crociera. La potenza di hovering scala secondo la teoria della quantità di moto come [@johnsonMarsScienceHelicopter2020]<!-- #eq:hover -->:

$$P_{hover} = \frac{T^{1.5}}{\sqrt{2\rho A_{rotor}}} \cdot \frac{1}{FM}$$ {#eq:hover-power-arch}

dove T è la spinta, ρ è la densità atmosferica, $A_\text{rotor}$ è l'area del disco del rotore, e FM è la figura di merito (tipicamente 0.6-0.7 per piccoli rotori [@johnsonMarsScienceHelicopter2020]<!-- #eq:hover -->). La dipendenza inversa dalla radice quadrata della densità significa che la potenza di hovering aumenta di un fattore di circa 7 passando dal livello del mare terrestre (ρ = 1.225 kg/m³) alla superficie di Marte (ρ ≈ 0.020 kg/m³) [@nasaMarsAtmosphereModel2021]<!-- #s:density -->.

Per il profilo di missione qui considerato, che richiede > 50 km di raggio operativo, l'autonomia dell'ala rotante sarebbe severamente limitata. I 72 voli di Ingenuity hanno totalizzato solo 128.8 minuti di tempo di volo, con voli tipici della durata di 1-3 minuti [@nasaIngenuityMarsHelicopter2024]<!-- #s:flights -->. Anche con una maggiore capacità della batteria, l'autonomia di un puro aeromobile a rotore su Marte rimarrebbe probabilmente sotto i 15 minuti, insufficiente per operazioni di rilevamento significative al raggio d'azione richiesto.

#### Ala fissa

Gli aeromobili convenzionali ad ala fissa raggiungono la massima efficienza aerodinamica, con rapporti portanza/resistenza (L/D) di 10-20 confrontati con L/D effettivi di 3-5 per l'ala rotante in volo traslato [@proutyHelicopterPerformanceStability2002]<!-- #ch3:ld -->. La potenza di crociera è:

$$P_{cruise} = \frac{W \cdot V}{L/D \cdot \eta}$$ {#eq:cruise-power-arch}

dove W è il peso, V è la velocità di crociera, e η è l'efficienza propulsiva. La dipendenza da L/D piuttosto che dal carico del disco rende il volo ad ala fissa molto più efficiente dal punto di vista energetico per coprire distanze.

Tuttavia, gli aeromobili ad ala fissa richiedono piste o sistemi di lancio/recupero. Data l'assenza di superfici preparate su Marte e il rischio di danni all'atterraggio su terreno non preparato, i progetti puramente ad ala fissa sono inadatti per operazioni basate sull'habitat.

#### VTOL ibrido (QuadPlane)

I design ibridi combinano rotori di sollevamento dedicati per il VTOL con un'ala fissa per il volo di crociera. Durante il decollo e l'atterraggio, i rotori di sollevamento forniscono spinta; durante la crociera, l'ala genera portanza mentre le eliche di crociera forniscono spinta in avanti e i rotori di sollevamento sono fermi o in autorotazione.

Per le operazioni marziane dove la riparazione in volo è impossibile, la tolleranza a singolo guasto è essenziale. Ciò si ottiene attraverso configurazioni coassiali per entrambi i sistemi propulsivi:

* Sistema di sollevamento: Otto motori in quattro coppie coassiali (configurazione ottacottero), dove ogni coppia coassiale ha rotori controrotanti che condividono un supporto strutturale. Ciò consente un atterraggio controllato con qualsiasi singolo motore guasto.
* Sistema di crociera: Due eliche traenti coassiali controrotanti a prua, azionate da motori indipendenti. Ogni motore è dimensionato per fornire il 60% della spinta di crociera nominale, permettendo la continuazione della missione con prestazioni ridotte se uno dei motori si guasta.

Questa architettura raggiunge un'efficienza di crociera vicina all'ala fissa pur mantenendo la capacità VTOL. La penalità di massa per il sistema di propulsione duale (10 motori totali: 8 di sollevamento più 2 di crociera) è tipicamente il 20-25% dell'MTOW basato sui riferimenti commerciali in @tbl:reference-vtol e tenendo conto dei motori di crociera ridondanti. Questa penalità è accettabile data la flessibilità operativa e la tolleranza ai guasti guadagnate.

L'architettura QuadPlane è ampiamente adottata nell'industria dei droni commerciali, con sistemi di controllo di volo maturi e affidabilità comprovata. Tutti e nove gli UAV di riferimento in @tbl:reference-vtol impiegano questa configurazione.

### Compromessi sulla geometria della fusoliera

La geometria della fusoliera influenza resistenza, stabilità e integrazione del payload. Il rapporto lunghezza-apertura alare ($l/b$) osservato negli UAV VTOL commerciali varia da 0.28 a 0.63 (@tbl:reference-fuselage), riflettendo diverse priorità progettuali: resistenza parassita, stabilità longitudinale, volume del payload.

La fusoliera e i componenti vari (carrello di atterraggio, torrette di sensori, antenne) contribuiscono sostanzialmente alla resistenza parassita degli UAV. L'analisi di dieci UAV da sorveglianza ad ala fissa ha rilevato che questi componenti rappresentano quasi la metà della resistenza parassita totale, portando a coefficienti di attrito equivalenti significativamente più alti rispetto agli aeromobili con equipaggio [@gottenFullConfigurationDrag2021]<!-- #s:drag -->.
Fusoliere più lunghe (maggiore $l/b$) forniscono un braccio di momento maggiore per la coda, migliorando la stabilità longitudinale con superfici di coda più piccole. Tuttavia, questo comporta un aumento dell'area bagnata della fusoliera e della massa strutturale.
Fusoliere più lunghe forniscono inoltre più volume interno per payload, batterie e avionica. Le configurazioni ad ala volante (molto basso $l/b$) sacrificano il volume interno per una ridotta resistenza parassita.

### Compromessi sulla configurazione della coda

La configurazione della coda influenza stabilità, autorità di controllo, resistenza e complessità strutturale. Per i design QuadPlane, la presenza di bracci di supporto dei rotori di sollevamento crea l'opzione di montare le superfici di coda su questi bracci piuttosto che sulla fusoliera.

#### Configurazioni montate sulla fusoliera

Le configurazioni di coda montate sulla fusoliera rappresentano l'approccio convenzionale per la progettazione aeronautica, con le superfici di coda attaccate direttamente alla parte posteriore della fusoliera. Queste configurazioni beneficiano di un'integrazione strutturale più semplice e di pratiche di progettazione consolidate, sebbene possano subire interferenza aerodinamica dalla fusoliera e dalla scia dell'ala. Sono considerate tre configurazioni montate sulla fusoliera.

La coda convenzionale combina stabilizzatori orizzontali e verticali, fornendo stabilità e controllo comprovati con collegamenti di controllo relativamente semplici. Le superfici orizzontali e verticali creano resistenza di interferenza alla loro intersezione, e la coda può essere posizionata nella scia dell'ala.

La V-tail combina il controllo di beccheggio e imbardata in due superfici angolate verso l'alto. Riduce la resistenza di interferenza e alleggerisce la struttura eliminando l'intersezione tra superfici orizzontali e verticali, ma richiede miscelazione dei comandi (ruddervator). La ridotta area bagnata fornisce una riduzione della resistenza rispetto alle configurazioni convenzionali [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:comparison -->.

La Y-tail è una configurazione a V invertita con una pinna verticale centrale aggiuntiva. Le superfici a V invertita forniscono controllo di beccheggio e autorità parziale di imbardata, mentre la pinna centrale migliora la stabilità direzionale e il controllo di imbardata.

#### Configurazioni montate sui bracci

I design QuadPlane includono intrinsecamente bracci strutturali per i rotori di sollevamento. Estendere questi bracci per supportare le superfici di coda offre vantaggi in efficienza strutturale, braccio di momento ed evitamento della scia. La struttura del braccio richiesta per i rotori di sollevamento può contemporaneamente sostenere i carichi della coda, riducendo la massa strutturale complessiva rispetto a bracci separati e coda montata sulla fusoliera. Le code montate sui bracci possono ottenere bracci di momento maggiori rispetto alle configurazioni montate sulla fusoliera, permettendo potenzialmente superfici di coda più piccole per una stabilità equivalente, e possono essere posizionate fuori dalla scia dell'ala e della fusoliera, migliorando l'efficacia della coda. Ai numeri di Reynolds marziani (Re circa 50,000 per le superfici di coda), l'efficacia delle superfici di controllo è ridotta rispetto alle condizioni terrestri; le configurazioni montate sui bracci possono fornire il maggiore braccio di momento necessario per ottenere un'adeguata autorità di controllo senza superfici di coda eccessivamente grandi. Sono considerate due configurazioni specifiche.

La V invertita montata sui bracci consiste in due superfici di coda angolate verso l'alto dalle estremità dei bracci, formando una V invertita vista da dietro. Questa configurazione fornisce controllo combinato di beccheggio e imbardata mantenendo la luce da terra. I bracci posizionano le superfici lontano dalla scia della fusoliera.

La U invertita montata sui bracci presenta uno stabilizzatore orizzontale che collega le due estremità dei bracci, con stabilizzatori verticali che si estendono verso l'alto da ciascun braccio. L'analisi CFD ha rilevato che questa configurazione forniva il più alto angolo critico (18° vs 15° per altre configurazioni), buona stabilità longitudinale e manovrabilità favorevole per missioni di sorveglianza [@nugrohoPerformanceAnalysisEmpennage2022]<!-- #s:comparison -->. La configurazione a U invertita sui bracci ha raggiunto una buona efficienza di volo mentre l'aggiunta di una pinna ventrale ha ulteriormente migliorato la stabilità direzionale.

![Viste laterali e posteriori di cinque configurazioni di coda: (a) convenzionale montata su fusoliera, (b) V-tail montata su fusoliera, (c) Y-tail montata su fusoliera, (d) V invertita montata sui bracci, e (e) U invertita montata sui bracci.](figures/it/configurazioni_coda.jpg){#fig:tail-configurations width=90%}

### Compromessi sui materiali strutturali

La selezione dei materiali influenza la frazione di massa strutturale, le prestazioni termiche e l'affidabilità. I benchmark commerciali utilizzano prevalentemente costruzione in composito di fibra di carbonio, con variazioni nell'approccio di fabbricazione.

Il polimero rinforzato con fibra di carbonio (CFRP) fornisce la massima resistenza e rigidità specifiche ed è utilizzato in tutti gli UAV VTOL commerciali ad alte prestazioni. Le opzioni di fabbricazione includono laminazione a mano, prepreg/autoclave e avvolgimento di filamento, con la costruzione in prepreg che fornisce le proprietà del materiale più consistenti. Il polimero rinforzato con fibra di vetro offre costo inferiore e fabbricazione più facile rispetto alla fibra di carbonio, ed è utilizzato per strutture secondarie e aree tolleranti ai danni come bordi d'attacco alari e carenature. La costruzione sandwich con anima in schiuma, con anima leggera tra pelli in fibra, è comune per rivestimenti alari e carenature e fornisce eccellente rigidità rispetto al peso per grandi superfici piane. Il Kevlar (fibra aramidica) fornisce alta resistenza agli urti ed è utilizzato per aree soggette a danni come punti di attacco del carrello di atterraggio.

L'ambiente marziano impone vincoli aggiuntivi sulla selezione dei materiali. La variazione di temperatura diurna da −80°C a +20°C causa espansione e contrazione termica; i compositi in fibra di carbonio hanno bassi coefficienti di espansione termica (CTE circa 0.5 ppm/°C per CFRP unidirezionale), riducendo lo stress termico, e l'elicottero Ingenuity ha utilizzato tessuti di carbonio TeXtreme spread tow specificamente selezionati per la resistenza alle microfratture sotto questi cicli termici [@latourabOxeonPartOwnedHoldings2025]<!-- #s:textreme -->. Le condizioni quasi-vuoto (circa 600 Pa) eliminano il trasferimento di calore convettivo, rendendo critiche le proprietà radiative, e la gestione termica interna può richiedere superfici placcate in oro (come usato in Ingenuity) o isolamento multistrato. La dose di radiazione superficiale di Marte (circa 76 mGy/anno) è ordini di grandezza inferiore alle soglie di degradazione dei polimeri, quindi la radiazione non è una preoccupazione significativa per i materiali strutturali su una missione pluriennale. Alcuni materiali della matrice polimerica possono subire outgassing a bassa pressione, potenzialmente contaminando le superfici ottiche, quindi sono preferite resine qualificate per lo spazio con basse caratteristiche di outgassing.
