---
title: "Studio di fattibilità di un UAV marziano per l'esplorazione di habitat"
author: "Elena Morelli"
date: 2025
bibliography: drone.bib
reference-section-title: References
---

::: {custom-style="Abstract Title"}
Sommario esecutivo
:::

::: {custom-style="Abstract"}
Questo studio valuta la fattibilità dell'impiego di un veicolo aereo senza pilota (UAV) da un habitat equipaggiato su Marte per estendere il raggio di esplorazione oltre i limiti della mobilità di superficie. Il progetto impiega un'architettura ibrida QuadPlane che combina capacità di decollo e atterraggio verticale (VTOL) con un'efficiente crociera ad ala fissa. È selezionata una configurazione solo batteria con un MTOW target di 12 kg, dando priorità alla semplicità e all'affidabilità per l'impegnativo ambiente marziano. Operando da Arcadia Planitia a un'elevazione di −3 km, la bassa densità atmosferica (0.020 kg/m³) necessita di grandi aree alari e propulsione ad alta efficienza, risultando in numeri di Reynolds di 50,000–90,000 dove la selezione del profilo alare diventa critica. Il profilo E387 fornisce le migliori prestazioni di portanza/resistenza in queste condizioni. Il dimensionamento preliminare indica che il progetto è tecnicamente fattibile con la tecnologia attuale o a breve termine.
:::

# Introduzione

Questo studio valuta la fattibilità di un UAV progettato per supportare le operazioni di un avamposto con equipaggio su Marte, fornendo capacità di ricognizione aerea, rilevamento geologico e relay di comunicazione.

Il volo atmosferico su Marte presenta sfide distinte rispetto all'aviazione terrestre. L'atmosfera marziana ha approssimativamente l'1% della densità a livello del mare della Terra, richiedendo grandi superfici alari e di rotore, velocità di volo più elevate, o una combinazione di entrambe per generare forze aerodinamiche sufficienti. La gravità di Marte (3.711 m/s²), pari al 38% del valore terrestre, riduce la portanza necessaria per sostenere il volo e compensa parzialmente questa penalità di densità. L'assenza di ossigeno atmosferico preclude la propulsione basata sulla combustione; i motori elettrici che azionano rotori o eliche costituiscono l'unico mezzo pratico di volo motorizzato. La mancanza di piste preparate nei siti di esplorazione rende necessaria la capacità di decollo e atterraggio verticale (VTOL). Le tempeste di polvere e il wind shear locale richiedono un sistema di controllo del volo con larghezza di banda e autorità sufficienti per compensare i disturbi atmosferici. La fine regolite marziana si accumula sulle superfici esposte e degrada i componenti meccanici e ottici, richiedendo stoccaggio protetto e sistemi di pulizia attivi come getti di aria compressa in un airlock dell'hangar. Infine, l'atmosfera sottile e l'assenza di un campo magnetico globale espongono la superficie a radiazioni solari e cosmiche galattiche elevate, richiedendo elettronica tollerante alle radiazioni o schermatura appropriata.

I voli di successo dell'elicottero Ingenuity della NASA hanno dimostrato che il volo motorizzato su Marte è realizzabile [@tzanetosIngenuityMarsHelicopter2022]. Tuttavia, l'architettura a rotori di Ingenuity limita raggio e autonomia. Per missioni di esplorazione che richiedono la copertura di decine o centinaia di chilometri, gli aeromobili ad ala fissa offrono efficienza aerodinamica superiore. Questo studio esamina configurazioni VTOL ibride che combinano la flessibilità operativa dei rotori con l'efficienza di crociera degli aeromobili ad ala fissa.

# Metodologia di progettazione

Questa sezione presenta il quadro metodologico per lo studio di fattibilità dell'UAV marziano. L'approccio combina il dimensionamento iterativo con l'analisi basata sui vincoli per esplorare sistematicamente lo spazio di progettazione e identificare configurazioni realizzabili.

## Approccio iterativo di dimensionamento {#sec:iterative-sizing}

Lo sviluppo di questo UAV marziano segue una metodologia di dimensionamento iterativo che bilancia l'analisi teorica con i vincoli pratici dei componenti. A differenza della progettazione convenzionale di aeromobili terrestri, dove esistono leggi di scalamento mature e ampie banche dati, la progettazione di aeromobili marziani richiede un'attenta integrazione dell'eredità di volo limitata con l'analisi scalata da casi di riferimento.

Il processo di progettazione procede attraverso quattro fasi distinte, con cicli di retroazione che consentono il perfezionamento in ogni fase:

1. **Ipotesi iniziali**: i dati di riferimento degli UAV VTOL da piattaforme commerciali e progetti concettuali marziani (@sec:reference-data) forniscono una base empirica per le stime iniziali dei parametri. I parametri chiave estratti dai progetti di riferimento includono le frazioni di massa (propulsione, energia, payload e, per sottrazione, struttura e altri sottosistemi), il carico del disco per le operazioni VTOL e i rapporti potenza-peso. Questi valori terrestri sono poi scalati per le condizioni marziane, tenendo conto della gravità ridotta (38% della Terra) e dell'atmosfera rarefatta (circa l'1% della densità a livello del mare terrestre).
2. **Dimensionamento preliminare**: con le ipotesi iniziali stabilite, la metodologia di dimensionamento basata sui vincoli genera un punto di progetto preliminare. Il diagramma di vincolo (matching chart) determina la combinazione di carico alare e carico di potenza che soddisfa tutte le condizioni di volo (hovering, crociera, salita e stallo). Da questo punto di progetto vengono calcolati i valori preliminari per area alare, apertura, potenza dei motori e ripartizione delle masse.
3. **Selezione dei componenti**: i risultati del dimensionamento preliminare guidano la selezione dei componenti effettivi dalle schede tecniche dei produttori. Questa fase confronta il modello di dimensionamento idealizzato con i vincoli del mondo reale, poiché i motori sono disponibili solo in dimensioni discrete, le batterie hanno densità energetiche specifiche, caratteristiche di tensione e limitazioni di temperatura, e le eliche devono essere compatibili con le configurazioni dei motori disponibili.
4. **Verifica**: i componenti selezionati forniscono valori aggiornati di massa, potenza ed efficienza che differiscono dalle stime preliminari. Il progetto viene ricalcolato con questi valori effettivi e viene verificata la conformità ai requisiti di missione. Se i requisiti non sono soddisfatti, il processo ritorna alla fase 2 con ipotesi perfezionate.

@fig:sizing-loop illustra la natura iterativa di questo processo. Ogni iterazione restringe lo spazio di progettazione man mano che emergono i vincoli a livello di componente e i requisiti vengono progressivamente soddisfatti.

![Il ciclo iterativo di dimensionamento per la progettazione di UAV marziani.](figures/sizing_loop.jpg){#fig:sizing-loop}

## Ruolo del dimensionamento basato sui vincoli {#sec:constraint-role}

Il diagramma di vincolo, o matching chart, costituisce il nucleo analitico della metodologia di dimensionamento. Questo strumento grafico, adattato dai metodi di dimensionamento aeronautico basati sulla potenza, traccia il carico di potenza (P/W) in funzione del carico alare (W/S) per ciascun vincolo di volo.

Per un aeromobile VTOL ibrido, che emerge come la configurazione più adatta dall'analisi dei trade-off (@sec:architecture-selection), i vincoli rilevanti includono:

* Vincolo di hovering: stabilisce il carico di potenza minimo in base al carico del disco e alla densità atmosferica. L'atmosfera rarefatta di Marte (circa 0.020 kg/m³ ad Arcadia Planitia) richiede carichi di potenza maggiori rispetto a operazioni terrestri equivalenti.
* Vincolo di crociera: derivato dalla polare di resistenza, questo vincolo determina la potenza necessaria per il volo livellato stazionario alla velocità di crociera di progetto.
* Vincolo di salita: garantisce una potenza eccedente sufficiente per la velocità di salita richiesta.
* Vincolo di stallo: stabilisce il carico alare massimo in base al coefficiente di portanza massimo del profilo alare al numero di Reynolds operativo.

Il punto di progetto viene selezionato all'interno della regione ammissibile delimitata da questi vincoli. Per le configurazioni QuadPlane, i vincoli di hovering e crociera sono in gran parte disaccoppiati: i rotori di sollevamento sono dimensionati per soddisfare il vincolo di hovering, mentre l'ala e il motore di crociera sono dimensionati per soddisfare i vincoli di crociera e stallo. Questo disaccoppiamento semplifica l'esplorazione dello spazio di progettazione ma richiede una verifica che il sistema combinato rimanga entro l'obiettivo di MTOW.

I requisiti derivati riassunti in @tbl:derived-requirements definiscono il punto di partenza per l'analisi del matching chart. L'MTOW target di 10 kg, derivato dall'analisi delle frazioni di massa e dai requisiti di payload, stabilisce il peso per la valutazione dei vincoli. La frazione di batteria assunta (35%), l'energia specifica (270 Wh/kg) e le efficienze propulsive alimentano i calcoli di potenza e autonomia. L'esecuzione del matching chart con questi input produce il punto di progetto preliminare: la combinazione specifica di carico alare e carico di potenza che massimizza l'autonomia soddisfacendo tutti i vincoli. Questo punto di progetto determina poi l'area alare, l'apertura e i requisiti di potenza dei motori che guidano la selezione dei componenti.

La natura iterativa di questo processo riconosce che le ipotesi iniziali sono necessariamente approssimate. Man mano che la selezione dei componenti rivela masse ed efficienze effettive, il punto di progetto può spostarsi. La metodologia garantisce che tali spostamenti siano sistematicamente tracciati e che il progetto finale rimanga tracciabile rispetto ai suoi fondamenti analitici.

# Analisi della missione

Questa sezione definisce il contesto della missione, includendo l'ambiente operativo ad Arcadia Planitia, il profilo di volo necessario per raggiungere gli obiettivi di missione e le esigenze dell'utente che guidano il progetto.

## Ambiente operativo {#sec:operational-environment}

Arcadia Planitia è selezionata come località operativa di riferimento. Questa regione offre diversi vantaggi per l'esplorazione iniziale di Marte: la sua bassa elevazione (−3 km rispetto al datum) fornisce maggiore densità atmosferica, il terreno relativamente pianeggiante è adatto alla costruzione di habitat, i depositi di ghiaccio d'acqua sotterraneo presentano interesse scientifico, e la latitudine moderata (47°11'24"N) bilancia l'illuminazione solare con la stabilità del ghiaccio.

Il volo atmosferico su Marte avviene in condizioni diverse dalla Terra [@desertAerodynamicDesignMartian2017]. La sottile atmosfera di CO₂ presenta pressioni superficiali intorno a 610 Pa medi, con significativa variazione a seconda dell'elevazione e della stagione. Le temperature superficiali hanno una media di circa 210 K con notevoli escursioni diurne. Alle basse elevazioni favorevoli al volo, la densità atmosferica rimane approssimativamente due ordini di grandezza inferiore rispetto al livello del mare terrestre, risultando in aerodinamica a basso numero di Reynolds e ridotta generazione di portanza.

![L'area di Arcadia Planitia nel contesto geografico marziano [@esaArcadiaPlanitiaContext2025].](figures/Arcadia_Planitia_in_context_pillars.png){#fig:arcadia-context width=50%}

### Equazioni dell'atmosfera marziana

L'atmosfera marziana è modellata utilizzando la formula barometrica con una composizione del 95.3% di CO₂ [@nasaMarsAtmosphereModel2021]. Le seguenti equazioni descrivono le proprietà atmosferiche in funzione dell'altitudine geometrica $h$ (in metri sopra il datum di riferimento):

$$T(h) = T_0 - L \cdot h$$ {#eq:temperature}

dove $T_0$ = 210 K è la temperatura di riferimento e $L$ = 0.00222 K/m è il gradiente termico verticale.

$$p(h) = p_0 \left(\frac{T(h)}{T_0}\right)^{g/(R_{CO2} \cdot L)}$$ {#eq:pressure}

dove $p_0$ = 610 Pa è la pressione media di superficie, $g$ = 3.711 m/s² è l'accelerazione di gravità superficiale di Marte, e $R_{CO_2}$ = 188.92 J/(kg·K) è la costante specifica del gas per CO₂.

La densità segue dalla legge dei gas ideali:

$$ρ(h) = \frac{p(h)}{R_{CO_2} \cdot T(h)}$$ {#eq:density}

La velocità del suono è:

$$a(h) = \sqrt{γ \cdot R_{CO_2} \cdot T(h)}$$ {#eq:speed-of-sound}

dove γ = 1.29 per CO₂.

La viscosità dinamica $\mu$ è approssimata usando la legge di Sutherland:

$$\mu(h) = \mu_\text{ref} \left(\frac{T(h)}{T_\text{ref}}\right)^{1.5} \frac{T_\text{ref} + S}{T(h) + S}$$ {#eq:dynamic-viscosity}

dove $\mu_\text{ref}$ = 1.48 × 10⁻⁵ Pa·s è la viscosità dinamica di riferimento a $T_\text{ref}$ = 293 K, e $S$ = 222 K è la costante di Sutherland per CO₂. La viscosità cinematica $\nu$ è quindi ottenuta da:

$$\nu(h) = \frac{\mu(h)}{\rho(h)}$$ {#eq:kinematic-viscosity}

### Condizioni ad Arcadia Planitia

All'altitudine operativa di 50 m sopra Arcadia Planitia (elevazione datum −3 km, quindi −2.95 km assoluti):

: Condizioni atmosferiche ad Arcadia Planitia, 50 m AGL {#tbl:atmosphere}

| Proprietà | Simbolo | Valore | Unità |
|:----------|:-------:|-------:|:------|
| Temperatura | $T$ | 216.6 | K |
| Pressione | $p$ | 800.5 | Pa |
| Densità | $\rho$ | 0.01960 | kg/m³ |
| Velocità del suono | $a$ | 230.8 | m/s |
| Viscosità dinamica | $\mu$ | 1.080 × 10⁻⁵ | Pa·s |
| Viscosità cinematica | $\nu$ | 5.170 × 10⁻⁴ | m²/s |

## Profilo di missione {#sec:mission-profile}

Il raggio di missione è definito come la distanza massima che l'UAV può percorrere in uscita mantenendo energia sufficiente per tornare con una riserva del 20%. Questo tiene conto di errori di navigazione, effetti del vento e manovre di contingenza.

È stato progettato un profilo di missione di riferimento composto da sette fasi. L'UAV esegue un decollo verticale utilizzando i rotori di sollevamento per salire all'altitudine di crociera, poi transita al volo ad ala fissa accelerando fino a che le ali generano portanza sufficiente. Durante la crociera in uscita, l'aeromobile vola in modalità ala fissa verso l'area obiettivo alla velocità di crociera. All'arrivo, il velivolo entra in una fase di loiter o rilevamento con i sistemi di payload attivi per la copertura dell'area. La fase di crociera di ritorno replica la tratta in uscita, con volo ad ala fissa di ritorno all'habitat. Infine, l'aeromobile decelera e transita nuovamente alla modalità di volo verticale prima di completare un atterraggio verticale sulla piazzola designata.

## Esigenze dell'utente {#sec:user-needs}

Questa sezione identifica le esigenze degli stakeholder che guidano la progettazione dell'UAV marziano. Le esigenze dell'utente esprimono quali capacità sono richieste senza specificare valori numerici; i requisiti quantitativi derivati da queste esigenze sono documentati in @sec:derived-requirements. Le esigenze sono organizzate in tre categorie: le esigenze di capacità di missione definiscono gli obiettivi funzionali che l'UAV deve raggiungere, le esigenze di sicurezza operativa riguardano l'affidabilità e la robustezza durante le operazioni di volo, e le esigenze di compatibilità ambientale garantiscono che il sistema possa funzionare entro i vincoli fisici specifici di Marte.

@Tbl:user-needs-summary fornisce una vista consolidata di tutte le esigenze dell'utente organizzate per categoria.

: Riepilogo delle esigenze dell'utente {#tbl:user-needs-summary}

| ID  | Categoria                   | Esigenza                           |
|-----|-----------------------------|------------------------------------|
| N1  | Capacità di missione        | Raggio operativo esteso            |
| N2  | Capacità di missione        | Imaging aereo                      |
| N3  | Capacità di missione        | Ponte radio per comunicazioni      |
| N4  | Capacità di missione        | Decollo e atterraggio verticali    |
| N5  | Capacità di missione        | Autonomia estesa                   |
| N6  | Sicurezza operativa         | Tolleranza al guasto singolo       |
| N7  | Sicurezza operativa         | Tolleranza al vento                |
| N8  | Sicurezza operativa         | Protezione dall'ingresso di polvere|
| N9  | Compatibilità ambientale    | Propulsione elettrica              |
| N10 | Compatibilità ambientale    | Tolleranza alle radiazioni         |
| N11 | Compatibilità ambientale    | Compatibilità termica              |

### Esigenze di capacità di missione

Le esigenze di capacità di missione definiscono ciò che l'UAV deve realizzare per soddisfare i suoi obiettivi scientifici e operativi. Queste esigenze stabiliscono le funzionalità fondamentali richieste per le missioni di ricognizione, rilevamento e ponte radio per comunicazioni.

* N1. Raggio operativo esteso: l'UAV dovrà fornire capacità di rilevamento aereo oltre il raggio pratico dei rover di superficie. Gli attuali rover marziani hanno percorso meno di 50 km in missioni pluriennali, limitando l'area accessibile intorno ai siti di atterraggio. Una piattaforma aerea può rilevare aree più vaste in meno tempo, consentendo la ricognizione di siti che altrimenti richiederebbero anni di viaggio via rover o rimarrebbero inaccessibili.
* N2. Imaging aereo: l'UAV dovrà trasportare un sistema di telecamere capace di acquisire immagini per il rilevamento geologico. Questo supporta l'obiettivo primario di missione di mappatura del terreno, identificazione di siti scientificamente interessanti e fornitura di contesto per le operazioni di superficie.
* N3. Ponte radio per comunicazioni: l'UAV dovrà trasportare un sistema radio capace di estendere il raggio di comunicazione per le operazioni EVA (attività extraveicolare). Le comunicazioni radio di superficie sono limitate da vincoli di linea di vista e oscuramento del terreno; una stazione relay aerea può estendere il raggio operativo sicuro delle attività di superficie con equipaggio.
* N4. Decollo e atterraggio verticali: l'UAV dovrà essere capace di operare senza piste o strisce di atterraggio preparate. La superficie marziana non offre infrastrutture per operazioni aeronautiche convenzionali; tutti i decolli e atterraggi devono avvenire da terreno non preparato nei pressi dell'habitat.
* N5. Autonomia estesa: l'UAV dovrà fornire un tempo di volo sufficiente per completare una missione di andata e ritorno con tempo di rilevamento nella località obiettivo. Voli brevi, come quelli dimostrati da Ingenuity, sono insufficienti per le missioni di ricognizione e ponte radio previste. L'autonomia deve accomodare transito, operazioni di rilevamento e ritorno con margini appropriati.

### Esigenze di sicurezza operativa

Le esigenze di sicurezza operativa riguardano i requisiti di affidabilità e robustezza che garantiscono il successo della missione nonostante l'ambiente operativo ostile e l'impossibilità di intervento in volo.

* N6. Tolleranza al guasto singolo: l'UAV dovrà mantenere un'operazione sicura in seguito a qualsiasi guasto singolo di sistema. La riparazione in volo non è possibile e le opportunità di manutenzione sono limitate. Il progetto deve accomodare guasti dei componenti senza perdita catastrofica del velivolo.
* N7. Tolleranza al vento: l'UAV dovrà operare in sicurezza nelle tipiche condizioni di vento marziane. Marte sperimenta regolari picchi di vento pomeridiani che il velivolo deve sopportare senza perdita di controllo o danni strutturali.
* N8. Protezione dall'ingresso di polvere: l'UAV dovrà essere protetto dalla polvere marziana. La fine regolite (dimensioni delle particelle 1-100 μm) può degradare i cuscinetti meccanici, contaminare le superfici ottiche e ridurre l'efficacia della gestione termica. La protezione dalla polvere è necessaria per un funzionamento affidabile per tutta la durata della missione.

### Esigenze di compatibilità ambientale

Le esigenze di compatibilità ambientale derivano dai vincoli fisici fondamentali di Marte, inclusa la composizione atmosferica, l'ambiente di radiazione e le condizioni termiche. Queste esigenze non possono essere scambiate con le prestazioni; la non conformità comporta il guasto del sistema.

* N9. Propulsione elettrica: l'UAV dovrà utilizzare sistemi di propulsione elettrica. L'atmosfera marziana è priva di ossigeno per la combustione, precludendo i motori a combustione interna convenzionali. I sistemi a batteria elettrica o solari-elettrici sono le uniche opzioni pratiche.
* N10. Tolleranza alle radiazioni: l'elettronica e i materiali dell'UAV dovranno resistere all'ambiente di radiazione superficiale marziano. La combinazione di radiazione cosmica galattica e eventi di particelle solari crea un ambiente di radiazione che l'elettronica commerciale deve tollerare per la durata della missione.
* N11. Compatibilità termica: l'UAV dovrà operare nell'ambiente termico marziano. Le escursioni termiche diurne e le basse temperature ambientali (da -80°C a +20°C) impongono vincoli su materiali, meccanismi e in particolare sulle prestazioni delle batterie.

# Dati di riferimento e analisi dei compromessi {#sec:reference-data}

Questa sezione raccoglie dati di riferimento da concetti esistenti di UAV marziani, piattaforme VTOL commerciali e studi di caratterizzazione dei sottosistemi. I dati informano i compromessi architettonici e forniscono la base empirica per le stime iniziali di massa e i requisiti derivati.

## Sistemi di payload {#sec:payload-systems}

Gli obiettivi di missione dell'UAV marziano, mappatura e ponte radio per telecomunicazioni, richiedono sistemi di payload capaci di operare nell'ambiente marziano rispettando stringenti vincoli di massa e potenza. Questa sezione esamina i sistemi di telecamere esistenti adatti alla ricognizione aerea per stabilire intervalli di massa realistici e informare l'allocazione del payload nella stima di peso iniziale.

### Panoramica dei sistemi di telecamera {#sec:camera-survey}

La selezione del payload camera comporta compromessi tra risoluzione, dimensione del sensore, massa e tolleranza ambientale. @Tbl:camera-survey riassume le specifiche per sistemi rappresentativi in tre categorie: telecamere RGB per mappatura, sensori multispettrali e termocamere.

: Specifiche dei sistemi camera da schede tecniche dei produttori {#tbl:camera-survey}

| Modello | Tipo | Sensore | Risoluzione | Massa (g) | Range temp. (°C) | Fonte |
|---------|------|---------|-------------|----------|------------------|--------|
| DJI Zenmuse P1 | RGB | Full frame | 45 MP | 800-1350 | −20 a +50 | [@djiDJIZenmuseP12024] |
| Ricoh GR III | RGB | APS-C | 24 MP | 227-257 | N.D. | [@ricohimagingRicohGRIII2024] |
| Phase One iXM-100 | RGB | Medio formato | 100 MP | 630-1170 | −10 a +40 | [@phaseonePhaseOneIXM1002024] |
| MicaSense RedEdge-MX | Multispettrale | Custom (5 bande) | 1.2 MP/banda | 232 | N.D. | [@micasenseMicaSenseRedEdgeMXIntegration2020] |
| DJI Zenmuse H20T | Termico + RGB | Multiplo | 640×512 (termico) | 828 | −20 a +50 | [@djiDJIZenmuseH20T2024] |

I valori di massa rappresentano configurazioni dal solo corpo alla configurazione completa. La DJI Zenmuse P1 varia da 800 g (corpo) a 1350 g con l'obiettivo DL 35mm [@djiDJIZenmuseP12024]. La Ricoh GR III raggiunge 257 g includendo batteria e storage [@ricohimagingRicohGRIII2024]. Il corpo della Phase One iXM-100 pesa 630 g, aumentando a 1170 g con l'obiettivo RSM 35mm [@phaseonePhaseOneIXM1002024].

#### Telecamere RGB per mappatura

I sensori full-frame forniscono qualità d'immagine superiore per applicazioni fotogrammetriche. La DJI Zenmuse P1 offre una risoluzione di 45 MP con passo pixel di 4.4 μm, ottenendo una distanza di campionamento a terra di 0.76 cm a 100 m di altitudine con l'obiettivo 35mm [@djiDJIZenmuseP12024]. Il consumo di potenza è circa 20 W. Il range di temperatura operativa da −20 a +50°C copre la porzione più calda delle condizioni superficiali marziane.

Le telecamere compatte offrono vantaggi in termini di massa. La Ricoh GR III fornisce imaging APS-C da 24 MP in un corpo da 227 g con obiettivo integrato da 18.3 mm [@ricohimagingRicohGRIII2024]. Tuttavia, il produttore non specifica limiti di temperatura operativa, indicando una tolleranza termica di grado consumer inadeguata per le condizioni marziane senza gestione termica.

La Phase One iXM-100 rappresenta la fascia alta dei sistemi di mappatura aerea con sensore medio formato (44×33 mm) da 100 MP [@phaseonePhaseOneIXM1002024]. Con consumo massimo di 16 W e massa del corpo di 630 g, ottiene un passo pixel di 3.76 μm. La classificazione IP53 fornisce protezione dalla polvere rilevante per le operazioni marziane, sebbene il range operativo da −10 a +40°C richieda controllo termico.

#### Telecamere multispettrali

La MicaSense RedEdge-MX fornisce imaging multispettrale a cinque bande (blu, verde, rosso, red-edge, infrarosso vicino) per analisi scientifica [@micasenseMicaSenseRedEdgeMXIntegration2020]. A 232 g completa con il sensore DLS 2 per la luce, rappresenta un'opzione leggera per applicazioni di rilevamento geologico. Ogni banda fornisce 1.2 MP (1280×960 pixel) con otturatore globale e profondità di output a 12 bit. La distanza di campionamento a terra è 8 cm/pixel a 120 m di altitudine.

#### Termocamere

La DJI Zenmuse H20T integra telecamere termiche, zoom e grandangolari con telemetro laser in un singolo payload da 828 g [@djiDJIZenmuseH20T2024]. Il microbolometro VOx non raffreddato fornisce una risoluzione termica di 640×512 con differenza di temperatura equivalente al rumore di 50 mK. L'intervallo di misurazione della temperatura va da −40 a +150°C (alto guadagno) o da −40 a +550°C (basso guadagno), adatto per la mappatura termica geologica.

#### Riepilogo di massa e dimensioni

Sulla base dei sistemi esaminati, le caratteristiche del payload camera sono le seguenti. Le telecamere RGB vanno da 227 g (solo corpo, Ricoh GR III) a 1350 g (con obiettivo, DJI Zenmuse P1). I sensori multispettrali come la MicaSense RedEdge-MX pesano circa 232 g. I sistemi termici/ibridi come la DJI Zenmuse H20T pesano circa 828 g.

Le dimensioni delle telecamere variano con il formato del sensore e la configurazione dell'obiettivo. La Ricoh GR III misura 109.4 × 61.9 × 33.2 mm (solo corpo) [@ricohimagingRicohGRIII2024]. La DJI Zenmuse P1 misura 198 × 166 × 129 mm [@djiDJIZenmuseP12024]. La MicaSense RedEdge-MX misura 87 × 59 × 45.4 mm [@micasenseMicaSenseRedEdgeMXIntegration2020].

Per scopi di dimensionamento iniziale, una telecamera RGB compatta (250-400 g) rappresenta l'allocazione di payload di base.

#### Considerazioni sull'ambiente termico marziano

Tutte le telecamere esaminate richiedono gestione termica per le operazioni marziane. Le temperature superficiali di Marte variano da circa −60 a +20°C, superando i limiti operativi inferiori della maggior parte delle telecamere commerciali. I sistemi DJI e Phase One con specifiche per basse temperature (−20°C e −10°C rispettivamente) forniscono la migliore tolleranza termica di base, sebbene siano necessari sistemi di riscaldamento supplementari durante le condizioni fredde. Le telecamere senza intervalli di temperatura specificati richiedono test di qualifica o si assume necessitino di controllo termico attivo.

Considerazioni aggiuntive per i sistemi camera marziani includono: la bassa pressione atmosferica (circa 600 Pa) che influisce sulla dissipazione termica e richiede test di qualifica; la tolleranza sconosciuta all'ambiente di radiazione per componenti commerciali; e i budget di potenza che devono tenere conto del riscaldamento per il controllo termico della camera oltre all'operazione della camera stessa.

### Sistemi radio relay {#sec:radio-survey}

La missione di ponte radio per telecomunicazioni richiede un sistema radio capace di estendere il raggio di comunicazione tra gli astronauti EVA in superficie e la stazione base dell'habitat. Per le operazioni marziane, le bande di frequenza specifiche differirebbero dall'uso terrestre a causa di differenze regolamentari e di propagazione, ma le specifiche di massa e potenza dei sistemi commerciali rimangono valide per la stima di fattibilità. Questa sezione esamina i sistemi radio esistenti adatti ad applicazioni UAV relay in due categorie: sistemi radio mesh e collegamenti dati punto-punto.

#### Sistemi radio mesh

Le radio mesh forniscono capacità di rete auto-formante e auto-rigenerante, sebbene questa funzionalità non sia strettamente richiesta per una missione relay con singolo UAV. @Tbl:radio-mesh riassume le specifiche per sistemi radio mesh rappresentativi.

: Specifiche dei sistemi radio mesh da schede tecniche dei produttori {#tbl:radio-mesh}

| Modello | Produttore | Massa (g) | Range freq. | Potenza (W) | Range temp. (°C) | Fonte |
|---------|------------|----------|-------------|-----------|------------------|--------|
| StreamCaster 4200E+ | Silvus Technologies | 425 | 300 MHz-6 GHz | 5-48 | −40 a +85 | [@silvustechnologiesStreamCaster4200SC42002025] |
| MPU5 | Persistent Systems | 391-726 | Bande multiple | N.D. | −40 a +85 | [@persistentsystemsMPU5TechnicalSpecifications2025] |
| BreadCrumb ES1 | Rajant Corporation | 455 | 2.4/5 GHz | 2.8-15 | −40 a +60 | [@rajantcorporationBreadCrumbES1Specifications2025] |

Il Silvus StreamCaster 4200E+ fornisce capacità mesh MIMO 2×2 a banda larga in un pacchetto da 425 g con classificazione IP68 e sommergibilità fino a 20 m [@silvustechnologiesStreamCaster4200SC42002025]. Il consumo di potenza varia da 5 W a 1 W di potenza di trasmissione a 48 W alla massima potenza di trasmissione di 10 W. Il range di temperatura operativa da −40 a +85°C supera i requisiti superficiali marziani.

Il Persistent Systems MPU5 integra un processore quad-core da 1 GHz con 2 GB di RAM per la gestione autonoma della rete [@persistentsystemsMPU5TechnicalSpecifications2025]. A 391 g (solo chassis) o 726 g con batteria, fornisce un raggio in linea di vista fino a 209 km tra i nodi. Le certificazioni MIL-STD-810G e MIL-STD-461F indicano una robusta tolleranza ambientale.

Il Rajant BreadCrumb ES1 offre funzionamento dual-band (2.4 GHz e 5 GHz) con capacità di rete auto-formante InstaMesh in un'unità da 455 g [@rajantcorporationBreadCrumbES1Specifications2025]. Il consumo di potenza è 2.8 W in idle e 15 W di picco. Il range di temperatura da −40 a +60°C copre le condizioni superficiali diurne marziane.

#### Collegamenti dati punto-punto

Per applicazioni relay con singolo UAV, i collegamenti punto-punto leggeri forniscono una superiore efficienza di massa. @Tbl:radio-p2p riassume le specifiche per sistemi rappresentativi.

: Specifiche dei collegamenti dati punto-punto da schede tecniche dei produttori {#tbl:radio-p2p}

| Modello | Produttore | Massa (g) | Banda freq. | Data rate | Raggio (km) | Potenza (W) | Fonte |
|---------|------------|----------|------------|-----------|------------|-----------|--------|
| RFD900x | RFDesign | 14.5 | 900 MHz | 0.064-0.75 Mbps | > 40 | 5 | [@rfdesignRFD900xModemSpecifications2024] |
| pMDDL2450 (OEM) | Microhard | 7 | 2.4 GHz | 12-25 Mbps | N.D. | N.D. | [@microhardPMDDL2450MiniatureMIMO2025] |
| pMDDL2450 (custodia) | Microhard | 165 | 2.4 GHz | 12-25 Mbps | N.D. | N.D. | [@microhardPMDDL2450MiniatureMIMO2025] |

Il RFD900x è un modem di telemetria ultraleggero da 14.5 g, ampiamente utilizzato nella comunità UAV con firmware open-source SiK [@rfdesignRFD900xModemSpecifications2024]. Fornisce un raggio in linea di vista di oltre 40 km con 1 W di potenza di trasmissione a 900 MHz. Il data rate va da 64 kbps di default a 750 kbps massimo, sufficiente per collegamenti di telemetria e comando. Il range di temperatura operativa da −40 a +85°C si estende oltre i requisiti superficiali marziani.

Il Microhard pMDDL2450 offre maggiore larghezza di banda (throughput di 25 Mbps) per applicazioni video relay in un fattore di forma estremamente compatto [@microhardPMDDL2450MiniatureMIMO2025]. Il modulo OEM pesa solo 7 g, mentre la versione con custodia e connettori pesa 165 g. La configurazione MIMO 2×2 fornisce una migliore affidabilità del collegamento attraverso la diversità spaziale.

#### Riepilogo di massa e dimensioni

Sulla base dei sistemi esaminati, le caratteristiche del payload radio sono le seguenti. Le radio mesh vanno da 391 g (solo chassis) a 726 g con batteria integrata. I collegamenti punto-punto vanno da 7 g (modulo OEM) a 165 g (versione con custodia).

Le dimensioni per il Microhard pMDDL2450 sono: modulo OEM 27 × 33 × 4 mm, versione con custodia 77 × 55 × 28 mm [@microhardPMDDL2450MiniatureMIMO2025].

Per scopi di dimensionamento iniziale, un collegamento punto-punto leggero (15-170 g) rappresenta l'allocazione di payload radio di base. La piena capacità mesh aggiungerebbe circa 400-500 g se fosse richiesto il coordinamento multi-asset.

#### Considerazioni sull'ambiente marziano

Tutti i sistemi radio esaminati superano il tipico range di temperatura superficiale marziana di circa −60 a +20°C ai limiti inferiori, con specifiche che vanno da −40 a +60°C (Rajant) a −40 a +85°C (Silvus, Persistent, RFDesign). Considerazioni aggiuntive per le operazioni marziane includono: la bassa pressione atmosferica (circa 600 Pa) che influisce sulla dissipazione termica, con le radio che potrebbero richiedere strategie di raffreddamento modificate o declassamento; la tolleranza sconosciuta all'ambiente di radiazione per componenti commerciali che richiede test di qualifica o alternative rad-hard; l'allocazione delle frequenze per la comunicazione superficiale marziana che differisce dalle bande regolamentari terrestri richiedendo modifiche al front-end radio; e i budget di potenza che devono tenere conto del controllo termico della radio oltre alla potenza di trasmissione.

## Confronto architetture {#sec:architecture-comparison}

### Architettura di volo

Tre architetture sono considerate per il volo atmosferico su Marte: ad ala rotante, ad ala fissa e VTOL ibrido. Ognuna presenta distinti compromessi tra flessibilità operativa ed efficienza energetica.

#### Ala rotante

I progetti puramente ad ala rotante forniscono decollo e atterraggio verticali senza richiedere superfici preparate. L'elicottero Ingenuity della NASA ha dimostrato questo approccio, completando 72 voli su Marte [@tzanetosIngenuityMarsHelicopter2022; @nasaIngenuityMarsHelicopter2024]. Tuttavia, gli aeromobili a rotore soffrono di scarsa efficienza in crociera. La potenza di hovering scala secondo la teoria della quantità di moto come [@johnsonMarsScienceHelicopter2020]:

$$P_{hover} = \frac{T^{1.5}}{\sqrt{2\rho A_{rotor}}} \cdot \frac{1}{FM}$$ {#eq:hover-power-arch}

dove T è la spinta, ρ è la densità atmosferica, $A_\text{rotor}$ è l'area del disco del rotore, e FM è la figura di merito (tipicamente 0.6-0.7 per piccoli rotori [@johnsonMarsScienceHelicopter2020]). La dipendenza inversa dalla radice quadrata della densità significa che la potenza di hovering aumenta di un fattore di circa 7 passando dal livello del mare terrestre (ρ = 1.225 kg/m³) alla superficie di Marte (ρ ≈ 0.020 kg/m³) [@nasaMarsAtmosphereModel2021].

Per il profilo di missione qui considerato, che richiede > 50 km di raggio operativo, l'autonomia dell'ala rotante sarebbe severamente limitata. I 72 voli di Ingenuity hanno totalizzato solo 128.8 minuti di tempo di volo, con voli tipici della durata di 1-3 minuti [@nasaIngenuityMarsHelicopter2024]. Anche con una maggiore capacità della batteria, l'autonomia di un puro aeromobile a rotore su Marte rimarrebbe probabilmente sotto i 15 minuti, insufficiente per operazioni di rilevamento significative al raggio d'azione richiesto.

#### Ala fissa

Gli aeromobili convenzionali ad ala fissa raggiungono la massima efficienza aerodinamica, con rapporti portanza/resistenza (L/D) di 10-20 confrontati con L/D effettivi di 3-5 per l'ala rotante in volo traslato [@proutyHelicopterPerformanceStability2002]. La potenza di crociera è:

$$P_{cruise} = \frac{W \cdot V}{L/D \cdot \eta}$$ {#eq:cruise-power-arch}

dove W è il peso, V è la velocità di crociera, e η è l'efficienza propulsiva. La dipendenza da L/D piuttosto che dal carico del disco rende il volo ad ala fissa molto più efficiente dal punto di vista energetico per coprire distanze.

Tuttavia, gli aeromobili ad ala fissa richiedono piste o sistemi di lancio/recupero. Data l'assenza di superfici preparate su Marte e il rischio di danni all'atterraggio su terreno non preparato, i progetti puramente ad ala fissa sono inadatti per operazioni basate sull'habitat.

#### VTOL ibrido (QuadPlane)

I design ibridi combinano rotori di sollevamento dedicati per il VTOL con un'ala fissa per il volo di crociera. Durante il decollo e l'atterraggio, i rotori di sollevamento forniscono spinta; durante la crociera, l'ala genera portanza mentre un'elica di crociera (traente o spingente) fornisce spinta in avanti e i rotori di sollevamento sono fermi o in autorotazione.

Questa architettura raggiunge un'efficienza di crociera vicina all'ala fissa pur mantenendo la capacità VTOL. La penalità di massa per il sistema di sollevamento (motori, ESC, rotori) è tipicamente il 15-25% dell'MTOW basato sui riferimenti commerciali in @tbl:reference-vtol. Questa penalità è accettabile data la flessibilità operativa guadagnata.

L'architettura QuadPlane è ampiamente adottata nell'industria dei droni commerciali, con sistemi di controllo di volo maturi e affidabilità comprovata. Tutti e nove gli UAV di riferimento in @tbl:reference-vtol impiegano questa configurazione.

### Compromessi sulla geometria della fusoliera

La geometria della fusoliera influenza resistenza, stabilità e integrazione del payload. Il rapporto lunghezza-apertura alare ($l/b$) osservato negli UAV VTOL commerciali varia da 0.28 a 0.63 (@tbl:reference-fuselage), riflettendo diverse priorità progettuali: resistenza parassita, stabilità longitudinale, volume del payload.

La fusoliera e i componenti vari (carrello di atterraggio, torrette di sensori, antenne) contribuiscono sostanzialmente alla resistenza parassita degli UAV. L'analisi di dieci UAV da sorveglianza ad ala fissa ha rilevato che questi componenti rappresentano quasi la metà della resistenza parassita totale, portando a coefficienti di attrito equivalenti significativamente più alti rispetto agli aeromobili con equipaggio [@gottenFullConfigurationDrag2021].
Fusoliere più lunghe (maggiore $l/b$) forniscono un braccio di momento maggiore per la coda, migliorando la stabilità longitudinale con superfici di coda più piccole. Tuttavia, questo comporta un aumento dell'area bagnata della fusoliera e della massa strutturale.
Fusoliere più lunghe forniscono inoltre più volume interno per payload, batterie e avionica. Le configurazioni ad ala volante (molto basso $l/b$) sacrificano il volume interno per una ridotta resistenza parassita.

### Compromessi sulla configurazione della coda

La configurazione della coda influenza stabilità, autorità di controllo, resistenza e complessità strutturale. Per i design QuadPlane, la presenza di bracci di supporto dei rotori di sollevamento crea l'opzione di montare le superfici di coda su questi bracci piuttosto che sulla fusoliera.

#### Configurazioni montate sulla fusoliera

Le configurazioni di coda montate sulla fusoliera rappresentano l'approccio convenzionale per la progettazione aeronautica, con le superfici di coda attaccate direttamente alla parte posteriore della fusoliera. Queste configurazioni beneficiano di un'integrazione strutturale più semplice e di pratiche di progettazione consolidate, sebbene possano subire interferenza aerodinamica dalla fusoliera e dalla scia dell'ala. Sono considerate tre configurazioni montate sulla fusoliera.

La coda convenzionale combina stabilizzatori orizzontali e verticali, fornendo stabilità e controllo comprovati con collegamenti di controllo relativamente semplici. Le superfici orizzontali e verticali creano resistenza di interferenza alla loro intersezione, e la coda può essere posizionata nella scia dell'ala.

La V-tail combina il controllo di beccheggio e imbardata in due superfici angolate verso l'alto. Riduce la resistenza di interferenza e alleggerisce la struttura eliminando l'intersezione tra superfici orizzontali e verticali, ma richiede miscelazione dei comandi (ruddervator). La ridotta area bagnata fornisce una riduzione della resistenza rispetto alle configurazioni convenzionali [@nugrohoPerformanceAnalysisEmpennage2022].

La Y-tail è una configurazione a V invertita con una pinna verticale centrale aggiuntiva. Le superfici a V invertita forniscono controllo di beccheggio e autorità parziale di imbardata, mentre la pinna centrale migliora la stabilità direzionale e il controllo di imbardata.

#### Configurazioni montate sui bracci

I design QuadPlane includono intrinsecamente bracci strutturali per i rotori di sollevamento. Estendere questi bracci per supportare le superfici di coda offre vantaggi in efficienza strutturale, braccio di momento ed evitamento della scia. La struttura del braccio richiesta per i rotori di sollevamento può contemporaneamente sostenere i carichi della coda, riducendo la massa strutturale complessiva rispetto a bracci separati e coda montata sulla fusoliera. Le code montate sui bracci possono ottenere bracci di momento maggiori rispetto alle configurazioni montate sulla fusoliera, permettendo potenzialmente superfici di coda più piccole per una stabilità equivalente, e possono essere posizionate fuori dalla scia dell'ala e della fusoliera, migliorando l'efficacia della coda. Ai numeri di Reynolds marziani (Re ~50,000 per le superfici di coda), l'efficacia delle superfici di controllo è ridotta rispetto alle condizioni terrestri; le configurazioni montate sui bracci possono fornire il maggiore braccio di momento necessario per ottenere un'adeguata autorità di controllo senza superfici di coda eccessivamente grandi. Sono considerate due configurazioni specifiche.

La V invertita montata sui bracci consiste in due superfici di coda angolate verso l'alto dalle estremità dei bracci, formando una V invertita vista da dietro. Questa configurazione fornisce controllo combinato di beccheggio e imbardata mantenendo la luce da terra. I bracci posizionano le superfici lontano dalla scia della fusoliera.

La U invertita montata sui bracci presenta uno stabilizzatore orizzontale che collega le due estremità dei bracci, con stabilizzatori verticali che si estendono verso l'alto da ciascun braccio. L'analisi CFD ha rilevato che questa configurazione forniva il più alto angolo critico (18° vs 15° per altre configurazioni), buona stabilità longitudinale e manovrabilità favorevole per missioni di sorveglianza [@nugrohoPerformanceAnalysisEmpennage2022]. La configurazione a U invertita sui bracci ha raggiunto una buona efficienza di volo mentre l'aggiunta di una pinna ventrale ha ulteriormente migliorato la stabilità direzionale.

![Viste laterali e posteriori di cinque configurazioni di coda: (a) convenzionale montata su fusoliera, (b) V-tail montata su fusoliera, (c) Y-tail montata su fusoliera, (d) V invertita montata sui bracci, e (e) U invertita montata sui bracci.](figures/tail_configurations.png){#fig:tail-configurations width=90%}

### Compromessi sui materiali strutturali

La selezione dei materiali influenza la frazione di massa strutturale, le prestazioni termiche e l'affidabilità. I benchmark commerciali utilizzano prevalentemente costruzione in composito di fibra di carbonio, con variazioni nell'approccio di fabbricazione.

Il polimero rinforzato con fibra di carbonio (CFRP) fornisce la massima resistenza e rigidità specifiche ed è utilizzato in tutti gli UAV VTOL commerciali ad alte prestazioni. Le opzioni di fabbricazione includono laminazione a mano, prepreg/autoclave e avvolgimento di filamento, con la costruzione in prepreg che fornisce le proprietà del materiale più consistenti. Il polimero rinforzato con fibra di vetro offre costo inferiore e fabbricazione più facile rispetto alla fibra di carbonio, ed è utilizzato per strutture secondarie e aree tolleranti ai danni come bordi d'attacco alari e carenature. La costruzione sandwich con anima in schiuma, con anima leggera tra pelli in fibra, è comune per rivestimenti alari e carenature e fornisce eccellente rigidità rispetto al peso per grandi superfici piane. Il Kevlar (fibra aramidica) fornisce alta resistenza agli urti ed è utilizzato per aree soggette a danni come punti di attacco del carrello di atterraggio.

L'ambiente marziano impone vincoli aggiuntivi sulla selezione dei materiali. La variazione di temperatura diurna da −80°C a +20°C causa espansione e contrazione termica; i compositi in fibra di carbonio hanno bassi coefficienti di espansione termica (CTE circa 0.5 ppm/°C per CFRP unidirezionale), riducendo lo stress termico, e l'elicottero Ingenuity ha utilizzato tessuti di carbonio TeXtreme spread tow specificamente selezionati per la resistenza alle microfratture sotto questi cicli termici [@latourabOxeonPartOwnedHoldings2025]. Le condizioni quasi-vuoto (circa 600 Pa) eliminano il trasferimento di calore convettivo, rendendo critiche le proprietà radiative, e la gestione termica interna può richiedere superfici placcate in oro (come usato in Ingenuity) o isolamento multistrato. La dose di radiazione superficiale di Marte (circa 76 mGy/anno) è ordini di grandezza inferiore alle soglie di degradazione dei polimeri, quindi la radiazione non è una preoccupazione significativa per i materiali strutturali su una missione pluriennale. Alcuni materiali della matrice polimerica possono subire outgassing a bassa pressione, potenzialmente contaminando le superfici ottiche, quindi sono preferite resine qualificate per lo spazio con basse caratteristiche di outgassing.

## Concetti di UAV marziani {#sec:mars-uav-concepts}

Diversi concetti di UAV marziani sono stati proposti o dimostrati, fornendo dati di riferimento per le ipotesi iniziali di progetto.

NASA Ingenuity è un aeromobile a rotore da 1.8 kg che ha dimostrato il volo autonomo propulso su Marte, completando 72 voli con tempo di volo cumulativo di circa 129 minuti [@tzanetosIngenuityMarsHelicopter2022; @nasaIngenuityMarsHelicopter2024]. Ingenuity ha convalidato tecnologie tra cui la navigazione autonoma, le prestazioni del rotore nell'atmosfera rarefatta e la sopravvivenza termica durante le notti marziane.

![NASA Ingenuity Mars Helicopter sulla superficie marziana [@nasaIngenuityMarsHelicopter2024].](figures/ingenuity.jpg){#fig:ingenuity width=50%}

ARES era un aereo ad ala fissa da 175 kg proposto con propulsione a razzo, progettato per missioni di rilevamento regionale coprendo oltre 600 km a 1-2 km di altitudine [@braunDesignARESMars2006]. ARES è stato finalista nel programma Mars Scout della NASA ma non è stato selezionato per il volo.

I concetti Mars Science Helicopter sono esacotteri proposti da 20-30 kg come successori di Ingenuity per operazioni a raggio esteso, dimostrando la tendenza verso aeromobili a rotore più grandi con maggiore capacità di carico utile [@johnsonMarsScienceHelicopter2020].

Recenti indagini su concetti VTOL ibridi per Marte includono architetture VTOL ad ala fissa con un progetto preliminare che affronta le sfide aerodinamiche e propulsive della fase di transizione [@bertaniPreliminaryDesignFixedwing2023], e un concetto di drone a energia solare con apertura alare e allungamento ottimizzati tramite uno strumento di dimensionamento multidisciplinare [@barbatoPreliminaryDesignFixedWing2024].

Questi progetti di riferimento informano le frazioni di massa, i valori di carico del disco e le aspettative prestazionali. Ingenuity fornisce la convalida che il volo propulso su Marte è realizzabile; ARES dimostra che le architetture ad ala fissa sono state considerate valide per missioni su scala regionale; i concetti Mars Science Helicopter mostrano il percorso verso maggiore capacità oltre la dimostrazione tecnologica; e gli studi VTOL ibridi offrono metodologie specifiche di dimensionamento aerodinamico per architetture che combinano crociera efficiente con flessibilità verticale.

## Benchmark VTOL commerciali {#sec:commercial-vtol}

I droni VTOL ibridi commerciali forniscono ulteriori riferimenti di progettazione. Sebbene progettati per condizioni terrestri, questi sistemi dimostrano allocazioni di massa pratiche, proporzioni geometriche e selezioni di componenti che informano le ipotesi iniziali di progetto. La seguente tabella riassume le specifiche di nove VTOL commerciali di tipo QuadPlane nella gamma 8-32 kg MTOW.

: Specifiche UAV VTOL commerciali {#tbl:reference-vtol}

| UAV | MTOW (kg) | Payload (kg) | Apertura (m) | Lunghezza (m) | Autonomia (min) | $V_\text{cruise}$ (m/s) | Rif. |
|:----|----------:|-------------:|---------:|-----------:|----------------:|----------------:|:----:|
| UAVMODEL X2400 | 8.5 | 2.0 | 2.40 | 1.20 | 220 | 16 | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | 10.0 | 3.0 | 2.69 | 0.75 | 272 | 17 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| Elevon X Sierra | 13.5 | 1.5 | 3.00 | 1.58 | 150 | 20 | [@elevonxElevonXSierraVTOL2024] |
| AirMobi V25 | 14.0 | 2.5 | 2.50 | 1.26 | 180 | 20 | [@airmobiAirmobiV25Full2024] |
| JOUAV CW-15 | 14.5 | 3.0 | 3.54 | 2.06 | 180 | 17 | [@jouavJOUAVCW15Multipurpose2024] |
| AirMobi V32 | 23.5 | 5.0 | 3.20 | 1.26 | 195 | 20 | [@airmobiAirmobiV32Full2024] |
| RTV320 E | 24.0 | 2.5 | 3.20 | 2.00 | 180 | 21 | [@uavfordroneRTV320ElectricVTOL2024] |
| V13-5 Sentinel | 26.5 | 7.5 | 3.50 | 1.88 | 160 | 44 | [@spideruavV135SentinelVTOL2024] |
| JOUAV CW-25E | 31.6 | 6.0 | 4.35 | 2.18 | 210 | 20 | [@jouavJOUAVCW25ELong2024] |

Diverse tendenze sono evidenti dai dati di riferimento. Il carico alare aumenta con l'MTOW: gli UAV più piccoli (8-15 kg) hanno aperture alari di 2.4-3.5 m, mentre gli UAV più grandi (24-32 kg) raggiungono 3.2-4.4 m, con carico alare che varia da 15-40 N/m² sulla Terra (corrispondente a 6-15 N/m² con gravità marziana). La frazione di payload varia dal 10-30% dell'MTOW tra i progetti, con payload tipici di 1.5-7.5 kg. Le velocità di crociera si aggirano attorno ai 17-21 m/s, poiché la maggior parte dei progetti ottimizza per l'autonomia piuttosto che per la velocità, eccetto piattaforme di sorveglianza ad alta velocità come il V13-5 Sentinel. L'autonomia supera i 150 minuti per tutti i progetti; la tecnologia delle batterie e la crociera efficiente consentono tempi di missione di 2.5-4.5 ore sulla Terra.

## Caratteristiche propulsive {#sec:propulsion-data}

Gli UAV di riferimento impiegano prevalentemente una configurazione QuadPlane, combinando quattro rotori di sollevamento verticali con un'elica spingente separata per la crociera. Questa architettura disaccoppia portanza e spinta, consentendo l'ottimizzazione di ciascun sistema propulsivo. La potenza del motore di sollevamento varia significativamente con l'MTOW, spaziando da circa 500 W (es. Sunnysky 4112 sull'X2400 da 8.5 kg) a 6000 W (es. T-Motor V13L sul V13-5 da 26.5 kg). @tbl:reference-propulsion-commercial riassume i dati propulsivi per i benchmark commerciali, incluse le masse dei motori dalle schede tecniche dei produttori.

: Specifiche propulsive UAV VTOL commerciali {#tbl:reference-propulsion-commercial}

| UAV | Motore lift | Potenza (W) | Massa (g) | Elica (in) | Motore crociera | Potenza (W) | Massa (g) | Rif. |
|:----|:-----------|----------:|---------:|----------:|:-------------|----------:|---------:|:----:|
| UAVMODEL X2400 | Sunnysky 4112 485KV | 550 | 153 | 15 | Sunnysky 3525 465KV | 2100 | 259 | [@uavmodelUAVMODELX2400VTOL2024] |
| AirMobi V25 | T-Motor MN505-S KV260 | 2500 | 225 | 16-17 | T-Motor AT4130 KV230 | 2500 | 408 | [@airmobiAirmobiV25Full2024] |
| V13-5 Sentinel | T-Motor V13L KV65 | 6000 | 1680 | N.D. | N.D. | N.D. | N.D. | [@spideruavV135SentinelVTOL2024] |

I concetti di aeromobili marziani presentano architetture propulsive distinte guidate dall'atmosfera rarefatta. @tbl:reference-propulsion-mars riassume i dati disponibili da fonti NASA e accademiche. I dati sulla massa del motore non sono generalmente disponibili per i concetti marziani poiché utilizzano design personalizzati o concettuali piuttosto che componenti commerciali.

: Specifiche propulsive UAV marziani {#tbl:reference-propulsion-mars}

| UAV | Motore lift | Potenza (W) | Elica (in) | Motore crociera | Potenza (W) | Rif. |
|:----|:-----------|----------:|----------:|:-------------|----------:|:----:|
| Ingenuity | 2 × 46-poli BLDC (AeroVironment) | circa 175 ciascuno | 48 | N.D. | N.D. | [@balaramMarsHelicopterTechnology2018] |
| Mars Science Helicopter | 6 × Elettrico (concettuale) | circa 550 ciascuno | 50 | N.D. | N.D. | [@johnsonMarsScienceHelicopter2020] |
| Concetto VTOL ibrido | 6 × Elettrico (concettuale) | circa 750 ciascuno | 20 | Elettrico | circa 635 | [@bertaniPreliminaryDesignFixedwing2023] |

Ingenuity utilizza due motori brushless DC outrunner a 46 poli personalizzati progettati e costruiti da AeroVironment per azionare i suoi rotori coassiali controrotanti a velocità superiori a 2400 RPM [@balaramMarsHelicopterTechnology2018]. La potenza totale di ingresso del sistema di circa 350 W corrisponde a circa 175 W per motore. Sei motori DCX 10S brushed DC Maxon aggiuntivi (7.1 g ciascuno) attivano il meccanismo del piatto oscillante per il controllo del passo delle pale, contribuendo con una potenza trascurabile (circa 1.4 W ciascuno) rispetto al sistema di propulsione principale [@maxongroupMaxonMotorsFly2021].

I dati del Mars Science Helicopter corrispondono alla configurazione esacottero da 31 kg, che richiede circa 3300 W di potenza di hovering distribuiti su sei rotori (circa 550 W ciascuno). Questo design rientra in un aeroshell di 2.5 m di diametro [@johnsonMarsScienceHelicopter2020]. Il concetto VTOL ibrido utilizza sei rotori di sollevamento da 20 pollici richiedendo circa 4500 W di potenza all'albero totale per il volo verticale (circa 750 W ciascuno), con un sistema di propulsione di crociera separato che richiede circa 635 W per il volo in avanti a 92 m/s [@bertaniPreliminaryDesignFixedwing2023].

Queste specifiche contrastano con i riferimenti commerciali in termini di potenza specifica. Ingenuity (1.8 kg) opera con una potenza media di sistema di circa 350 W, ottenendo una potenza specifica di circa 194 W/kg, riflettendo la natura ad alta intensità energetica del volo a rotore nell'atmosfera rarefatta marziana [@tzanetosIngenuityMarsHelicopter2022]. Il concetto Mars Science Helicopter (31 kg) scala questo approccio a una potenza di hovering stimata di circa 3300 W, ottenendo circa 106 W/kg grazie a rotori più grandi e più efficienti [@johnsonMarsScienceHelicopter2020]. ARES (175 kg) richiedeva un sistema a razzo bipropellente (MMH/MON3) piuttosto che propulsione elettrica per raggiungere il suo raggio di 600 km [@braunDesignARESMars2006]. I recenti studi VTOL ibridi per Marte stimano requisiti di potenza di crociera di circa 635 W (circa 32 W/kg), paragonabili alla potenza specifica di crociera di droni terrestri efficienti perché le velocità di volo più elevate su Marte compensano la minore densità atmosferica [@bertaniPreliminaryDesignFixedwing2023].

I dati indicano che mentre i requisiti di potenza di crociera sono simili tra piattaforme marziane e terrestri, la fase di sollevamento nell'atmosfera marziana richiede sistemi ad alta potenza specifica.

### Parametri di efficienza propulsiva {#sec:propulsion-efficiency}

La potenza richiesta sia per il volo hovering che per la crociera deve tenere conto delle perdite nella catena propulsiva. Questi parametri di efficienza impattano direttamente sul consumo energetico e sono input per l'analisi dei vincoli.

#### Figura di merito

La figura di merito quantifica l'efficienza del rotore in hovering, definita come il rapporto tra la potenza indotta ideale (dalla teoria della quantità di moto) e la potenza effettiva:

$$
FM = \frac{P_\text{ideale}}{P_\text{effettiva}} = \frac{T^{3/2}/\sqrt{2 \rho A}}{P_\text{effettiva}}
$$ {#eq:figure-of-merit-def}

Per elicotteri a grandezza naturale ad alti numeri di Reynolds ($Re > 10^6$), $FM$ raggiunge tipicamente 0.75-0.82 [@leishmanPrinciplesHelicopterAerodynamics2006]. Tuttavia, la figura di merito degrada sostanzialmente a bassi numeri di Reynolds a causa dell'aumento della resistenza di profilo. Leishman documenta che i micro velivoli ad ala rotante (MAV) a numeri di Reynolds molto bassi ($Re \sim 10{,}000$-$50{,}000$) raggiungono valori di $FM$ di solo 0.30-0.50 [@leishmanPrinciplesHelicopterAerodynamics2006]. Questa degradazione risulta da coefficienti di resistenza di profilo che aumentano da $C_{d_0} \approx 0.01$ ad alto $Re$ a $C_{d_0} \approx 0.035$ a basso $Re$.

I rotori marziani operano a numeri di Reynolds di $Re \approx 11{,}000$ per Ingenuity e $Re \approx 15{,}000$-$25{,}000$ per i concetti Mars Science Helicopter [@johnsonMarsScienceHelicopter2020], collocandoli nel regime dove avviene una significativa degradazione di $FM$. Basandosi sui dati di Leishman per MAV a basso Reynolds, la $FM$ del rotore marziano è stimata a 0.40, rappresentando la mediana dell'intervallo documentato 0.30-0.50.

#### Efficienza dell'elica

L'efficienza dell'elica di crociera è definita come:

$$
\eta_\text{elica} = \frac{T \times V}{P_\text{albero}}
$$ {#eq:propeller-efficiency}

Eliche ottimizzate ad alti numeri di Reynolds raggiungono $\eta_\text{elica} \approx 0.80$-$0.85$ [@sadraeyDesignUnmannedAerial2020]. Ai numeri di Reynolds previsti per la crociera marziana ($Re \approx 50{,}000$-$100{,}000$), l'efficienza degrada a causa dell'aumento della resistenza di profilo. Sadraey documenta efficienze dell'elica di 0.50-0.65 per piccole eliche UAV operanti in questo regime di Reynolds [@sadraeyDesignUnmannedAerial2020]. L'efficienza dell'elica di crociera marziana è stimata a 0.55 con un intervallo di 0.45-0.65.

#### Efficienza del motore e dell'ESC

I motori brushless DC utilizzati nelle applicazioni UAV raggiungono tipicamente efficienze di picco dell'88-92% [@sadraeyDesignUnmannedAerial2020], con valori dell'85-87% alle impostazioni di potenza di crociera (40-60% della potenza massima). I regolatori di velocità elettronici (ESC) raggiungono un'efficienza del 93-98% a impostazioni di acceleratore moderate o alte [@sadraeyDesignUnmannedAerial2020]. Queste efficienze sono relativamente non influenzate dalle condizioni atmosferiche marziane, sebbene la gestione termica nell'atmosfera rarefatta richieda considerazione.

#### Riepilogo delle efficienze

@tbl:efficiency-parameters riassume i valori di efficienza per l'analisi dei vincoli dell'UAV marziano.

: Parametri di efficienza propulsiva per il dimensionamento dell'UAV marziano {#tbl:efficiency-parameters}

| Parametro | Simbolo | Valore | Intervallo | Fonte |
|:----------|:------:|------:|------:|:-------|
| Figura di merito | $FM$ | 0.40 | 0.30-0.50 | [@leishmanPrinciplesHelicopterAerodynamics2006] |
| Efficienza elica | $\eta_\text{elica}$ | 0.55 | 0.45-0.65 | [@sadraeyDesignUnmannedAerial2020] |
| Efficienza motore | $\eta_\text{motore}$ | 0.85 | 0.82-0.90 | [@sadraeyDesignUnmannedAerial2020] |
| Efficienza ESC | $\eta_\text{ESC}$ | 0.95 | 0.93-0.98 | [@sadraeyDesignUnmannedAerial2020] |

L'efficienza combinata dalla batteria alla potenza di spinta è:

$$\eta_\text{hover} = FM \times \eta_\text{motore} \times \eta_\text{ESC} = 0.4000 \times 0.8500 \times 0.9500 = 0.3230$$ {#eq:hover-efficiency}

$$\eta_\text{crociera} = \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC} = 0.5500 \times 0.8500 \times 0.9500 = 0.4436$$ {#eq:cruise-efficiency}

Queste efficienze combinate indicano che circa il 32% della potenza della batteria è convertita in potenza di spinta utile in hovering, e il 44% in potenza di spinta di crociera. La bassa figura di merito domina la catena di efficienza in hovering, mentre l'efficienza dell'elica limita le prestazioni in crociera.

### Carico del disco {#sec:disk-loading}

Il carico del disco ($DL = T/A$) è il rapporto tra la spinta del rotore e l'area totale del disco del rotore ed è un parametro fondamentale per il dimensionamento degli aeromobili a rotore. Un carico del disco più alto riduce la dimensione del rotore ma aumenta i requisiti di potenza, poiché la velocità indotta e la potenza di hovering scalano con la radice quadrata del carico del disco.

Per la configurazione a rotori coassiali di Ingenuity, il carico del disco può essere calcolato dalle sue specifiche. Con una massa di 1.8 kg (peso 6.68 N su Marte), raggio del rotore di 0.60 m (diametro 1.2 m) e due rotori:

$$DL_\text{Ingenuity} = \frac{W}{2 \pi R^2} = \frac{6.68}{2 \times \pi \times 0.60^2} = \frac{6.68}{2.26} \approx 3.0 \text{ N/m}^2$$ {#eq:dl-ingenuity}

Il concetto esacottero Mars Science Helicopter (31 kg, sei rotori con raggio di 0.64 m) ha un carico del disco più alto [@johnsonMarsScienceHelicopter2020]:

$$DL_\text{MSH} = \frac{W}{6 \pi R^2} = \frac{31 \times 3.711}{6 \times \pi \times 0.64^2} = \frac{115}{7.72} \approx 15 \text{ N/m}^2$$ {#eq:dl-msh}

I multicotteri commerciali terrestri operano tipicamente con carichi del disco di 100-400 N/m² alla densità del livello del mare. Il rapporto del carico del disco richiesto tra Marte e la Terra scala con l'inverso della densità per mantenere una velocità indotta equivalente:

$$\frac{DL_\text{Marte}}{DL_\text{Terra}} = \frac{\rho_\text{Terra}}{\rho_\text{Marte}} = \frac{1.225}{0.0196} \approx 63$$

Questo fattore di scala spiega perché gli aeromobili marziani a rotore richiedono rotori molto più grandi (carico del disco più basso) rispetto a equivalenti terrestri della stessa massa.

Per l'UAV marziano, viene adottato un carico del disco di 30 N/m² come compromesso di progetto tra dimensione del rotore e potenza di hovering. Questo valore è più alto di Ingenuity (2.956 N/m²) e MSH (14.90 N/m²), ma inferiore a quanto lo scalamento equivalente terrestre suggerirebbe, bilanciando i requisiti contrastanti di geometria compatta del rotore e potenza di hovering accettabile nell'atmosfera marziana. Le implicazioni di questa scelta per il dimensionamento del rotore e i requisiti di potenza sono analizzate in @sec:constraint-analysis.

### Rapporto portanza/resistenza equivalente per aeromobili a rotore {#sec:rotorcraft-ld}

Per gli aeromobili a rotore in volo traslato, un rapporto portanza/resistenza equivalente $(L/D)_\text{eff}$ caratterizza l'efficienza propulsiva complessiva. Questo parametro mette in relazione la potenza con il prodotto di peso e velocità:

$$P = \frac{W \times V}{(L/D)_\text{eff}}$$ {#eq:rotorcraft-power}

A differenza degli aeromobili ad ala fissa dove $L/D$ è un parametro puramente aerodinamico, il rapporto $L/D$ equivalente per aeromobili a rotore include l'efficienza propulsiva del rotore e le perdite indotte in volo traslato. @tbl:rotorcraft-ld riassume i valori tipici per diverse configurazioni di aeromobili a rotore.

: Rapporto portanza/resistenza equivalente per configurazioni ad ala rotante [@proutyHelicopterPerformanceStability2002; @leishmanPrinciplesHelicopterAerodynamics2006] {#tbl:rotorcraft-ld}

| Configurazione | $(L/D)_\text{eff}$ | Note |
|:--------------|:------------------:|:------|
| Elicottero convenzionale | 4-6 | Resistenza del mozzo, inefficienza del rotore |
| Compound ottimizzato | 6-8 | L'ala alleggerisce il rotore ad alta velocità |
| Puro multirotore | 3-5 | Nessun beneficio dalla portanza traslazionale |

Viene adottato un valore di $(L/D)_\text{eff}$ = 4.000 per l'analisi della configurazione ad ala rotante dell'UAV marziano, rappresentando una stima conservativa che tiene conto del regime a basso numero di Reynolds e dell'ottimizzazione limitata del rotore a piccola scala. Questo valore è utilizzato solo per il confronto della configurazione puramente ad ala rotante; l'analisi VTOL ibrida utilizza i valori di $L/D$ ad ala fissa per la crociera.

## Caratteristiche di accumulo energetico {#sec:energy-data}

La selezione della tecnologia delle batterie è importante per l'autonomia dell'UAV marziano. Questa sezione presenta i dati di riferimento da piattaforme commerciali e deriva i parametri di utilizzo necessari per l'analisi dei vincoli.

### Specifiche batterie di riferimento {#sec:reference-battery-specs}

La capacità e la tecnologia delle batterie variano tra i progetti. Le batterie al litio-ione allo stato solido e semi-solido stanno emergendo per applicazioni ad alta autonomia, offrendo migliore densità energetica e prestazioni a basse temperature.

: Specifiche batterie UAV di riferimento {#tbl:reference-battery}

| UAV | Tipo batteria | Capacità (mAh) | Massa (kg) | Energia spec. (Wh/kg) | Range temp. (°C) | Rif. |
|:----|:-------------|---------------:|----------:|---------------------:|-----------------:|:----:|
| UAVMODEL X2400 | LiPo 6S | 30000 | 2.5 | circa 133 | N.D. | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | Li-ion semi-solido | 44000 | 4.0 | circa 180 | −20 a +45 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| AirMobi V25 | HV LiPo 6S ×2 | 50000 | 5.05 | circa 150 | −20 a +45 | [@gensace/tattuTattu25000mAh228V2024] |
| RTV320 E | Li-ion stato solido ×4 | 108000 | 9.36 | circa 270 | −20 a +60 | [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025] |

Le batterie allo stato solido utilizzate nel RTV320 E raggiungono 270 Wh/kg con range di temperatura esteso, rendendole adatte per applicazioni marziane dove le temperature ambiente raggiungono −80°C.

### Parametri di utilizzo batteria {#sec:battery-utilisation}

L'energia utilizzabile dalla batteria è ridotta dall'efficienza di scarica e dalle limitazioni di profondità di scarica. L'efficienza di scarica tiene conto delle perdite per resistenza interna durante l'assorbimento di corrente:

$$E_\text{utilizzabile} = E_\text{totale} \times DoD \times \eta_\text{batt}$$ {#eq:usable-energy}

dove $E_\text{totale}$ è la capacità nominale della batteria, $DoD$ è la profondità di scarica, e $\eta_\text{batt}$ è l'efficienza di scarica.

Per il dimensionamento dell'aeromobile, l'energia disponibile è convenientemente espressa come funzione dell'MTOW utilizzando la frazione di massa della batteria:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$ {#eq:battery-energy-fraction}

dove $f_\text{batt}$ è la frazione di massa della batteria (da @sec:initial-mass-estimate) e $e_\text{spec}$ è l'energia specifica (Wh/kg). Questa equazione è applicata nell'analisi dei vincoli (@sec:constraint-analysis) per determinare l'energia disponibile per ciascuna configurazione.

Viene adottata una profondità di scarica di $DoD$ = 0.80 per preservare la vita ciclica della batteria. L'efficienza di scarica dipende dal C-rate (corrente di scarica relativa alla capacità). Per le correnti di scarica previste durante il funzionamento dell'UAV marziano (circa 3-5C durante l'hovering, 0.5-1C durante la crociera), le batterie al litio allo stato solido raggiungono efficienze di scarica di 0.93-0.97 [@sadraeyDesignUnmannedAerial2020]. Viene adottato un valore di $\eta_\text{batt}$ = 0.95 come rappresentativo di tassi di scarica moderati.

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

## Geometria della fusoliera {#sec:fuselage-data}

Le dimensioni della fusoliera influenzano il volume del payload, la resistenza e la stabilità. Il rapporto lunghezza/apertura alare ($l/b$) caratterizza la compattezza della fusoliera, con valori più bassi che indicano fusoliere più corte rispetto all'apertura alare. La seguente tabella riassume la geometria della fusoliera dai benchmark commerciali.

: Geometria della fusoliera degli UAV VTOL commerciali {#tbl:reference-fuselage}

| UAV | Apertura (m) | Lunghezza (m) | $l/b$ | Rif. |
|:----|-------------:|-----------:|------:|:----:|
| UAVMODEL X2400 | 2.40 | 1.20 | 0.50 | [@uavmodelUAVMODELX2400VTOL2024] |
| DeltaQuad Evo | 2.69 | 0.75 | 0.28 | [@deltaquadDeltaQuadEvoEnterprise2024] |
| Elevon X Sierra | 3.00 | 1.58 | 0.53 | [@elevonxElevonXSierraVTOL2024] |
| AirMobi V25 | 2.50 | 1.26 | 0.50 | [@airmobiAirmobiV25Full2024] |
| JOUAV CW-15 | 3.54 | 2.06 | 0.58 | [@jouavJOUAVCW15Multipurpose2024] |
| AirMobi V32 | 3.20 | 1.26 | 0.39 | [@airmobiAirmobiV32Full2024] |
| RTV320 E | 3.20 | 2.00 | 0.63 | [@uavfordroneRTV320ElectricVTOL2024] |
| V13-5 Sentinel | 3.50 | 1.88 | 0.54 | [@spideruavV135SentinelVTOL2024] |
| JOUAV CW-25E | 4.35 | 2.18 | 0.50 | [@jouavJOUAVCW25ELong2024] |

Il rapporto lunghezza/apertura alare varia da 0.28 (DeltaQuad Evo, configurazione ad ala volante) a 0.63 (RTV320 E), con una mediana di circa 0.50. Questo rapporto influenza sia la resistenza parassita che la stabilità longitudinale. La stima della resistenza parassita per UAV ad ala fissa richiede particolare attenzione ai contributi della fusoliera e dei componenti vari, che possono rappresentare quasi la metà della resistenza parassita totale [@gottenFullConfigurationDrag2021].

## Configurazioni della coda {#sec:tail-data}

Gli UAV QuadPlane utilizzano varie configurazioni di impennaggio, che possono essere categorizzate per posizione di montaggio: montate sulla fusoliera o montate sui bracci. I bracci dei rotori di sollevamento presenti nei design QuadPlane creano opportunità per superfici di coda montate sui bracci che possono offrire vantaggi strutturali e aerodinamici.

: Categorie di configurazione della coda per UAV VTOL {#tbl:reference-tail-types}

| Tipo di configurazione | Descrizione | UAV di esempio |
|:-------------------|:------------|:-------------|
| Convenzionale montata sulla fusoliera | Stabilizzatori orizzontale + verticale sulla fusoliera | JOUAV CW-15 [@jouavJOUAVCW15Multipurpose2024] |
| V-tail montata sulla fusoliera | Due superfici in disposizione a V verso l'alto | UAVMODEL X2400 [@uavmodelUAVMODELX2400VTOL2024] |
| Y-tail montata sulla fusoliera | V invertita con pinna verticale centrale | V13-5 Sentinel [@spideruavV135SentinelVTOL2024] |
| V invertita montata sui bracci | V invertita utilizzando i bracci dei motori di sollevamento | JOUAV CW-25E [@jouavJOUAVCW25ELong2024] |
| U invertita montata sui bracci | Impennaggio a U invertita sui bracci | Event 38 E400 [@event38unmannedsystemsEvent38E4002024] |

Una recente analisi CFD delle configurazioni di impennaggio VTOL-Plane ha confrontato le disposizioni U sui bracci, U invertita sui bracci, V-tail invertita sui bracci e semi-V-tail invertita sui bracci [@nugrohoPerformanceAnalysisEmpennage2022]. Lo studio ha rilevato che la configurazione a U invertita sui bracci forniva caratteristiche di stallo favorevoli ed efficienza di volo per missioni di sorveglianza.

Per le operazioni marziane, la selezione della configurazione della coda deve considerare l'ambiente a basso numero di Reynolds (Re circa 50.000 per le superfici di coda), che influenza l'efficacia delle superfici di controllo. Inoltre, le configurazioni montate sui bracci offrono sinergia strutturale con i bracci di supporto dei motori di sollevamento già richiesti per la capacità VTOL QuadPlane.

## Materiali strutturali {#sec:materials-data}

Gli UAV VTOL commerciali utilizzano prevalentemente materiali compositi per la struttura primaria, con la fibra di carbonio che fornisce il miglior rapporto resistenza/peso. La seguente tabella riassume i dati disponibili sui materiali dalle specifiche dei produttori.

: Materiali strutturali degli UAV VTOL commerciali {#tbl:reference-materials}

| UAV | Materiali primari | Note |
|:----|:------------------|:------|
| AirMobi V25 | Fibra di carbonio, fibra di vetro, Kevlar, PVC | Design modulare, assemblaggio senza attrezzi |
| AirMobi V32 | Fibra di carbonio, fibra di vetro, Kevlar, PVC | Costruzione simile al V25 |
| V13-5 Sentinel | Fibra di carbonio, fibra di vetro, Kevlar | Configurazione per carichi pesanti |
| Elevon X Sierra | Compositi prepreg in fibra di carbonio | Stampi lavorati CNC, scafo monoscocca |
| DeltaQuad Evo | Composito (non specificato) | Costruzione ad ala volante |

L'elicottero marziano Ingenuity ha impiegato compositi avanzati in fibra di carbonio per le pale del rotore e la struttura, utilizzando tessuti di carbonio spread tow TeXtreme per peso ultraleggero e resistenza alle microfratture sotto i cicli termici marziani [@latourabOxeonPartOwnedHoldings2025]. Anche le gambe di atterraggio e la protezione della fusoliera hanno utilizzato compositi rinforzati con fibra di carbonio, con superfici interne rivestite in oro per la gestione termica.

Per le applicazioni marziane, la selezione dei materiali deve affrontare i cicli termici da −80°C a +20°C della variazione diurna, la bassa pressione atmosferica che elimina il trasferimento di calore convettivo, e l'esposizione alle radiazioni (circa 76 mGy/anno dose superficiale), il tutto minimizzando la massa e mantenendo l'integrità strutturale.

## Stima di massa iniziale {#sec:initial-mass-estimate}

Questa sezione stabilisce la stima iniziale dell'MTOW (Maximum Takeoff Weight) utilizzando l'approccio delle frazioni di massa, una tecnica standard nella progettazione concettuale di aeromobili [@roskamAirplaneDesign12005a; @sadraeyAircraftDesignSystems2013]. L'intervallo di MTOW stabilito qui fornisce il punto di partenza per l'analisi dei vincoli in @sec:constraint-analysis.

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

La frazione di propulsione è più alta rispetto ai benchmark degli UAV commerciali a causa della necessità di ridondanza nel sistema di propulsione duale (sia rotori di sollevamento che elica di crociera), operando senza possibilità di riparazione in volo.

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
| 0.08 (molto conservativa) | 12.5 kg |
| 0.10 (base) | 10.0 kg |
| 0.15 (ottimistica) | 6.7 kg |

Viene adottato un MTOW di base di 10 kg per il dimensionamento iniziale. Questo valore sarà affinato attraverso l'analisi dei vincoli in @sec:constraint-analysis, dove i requisiti di potenza, il carico alare e i vincoli di autonomia sono valutati simultaneamente.

### Validazione delle frazioni di massa

Le frazioni raccomandate sommano a uno:

$$f_\text{batt} + f_\text{payload} + f_\text{vuoto} + f_\text{prop} + f_\text{avionica} = 0.35 + 0.10 + 0.30 + 0.20 + 0.05 = 1.00$$

Le frazioni sono auto-consistenti, con la ridotta frazione a vuoto (rispetto alle stime iniziali) compensata dall'aumentata allocazione propulsiva per la ridondanza. Questa allocazione riflette l'architettura VTOL ibrida dove entrambi i sistemi di propulsione di sollevamento e crociera devono essere dimensionati per l'affidabilità.

La metodologia dettagliata di stima del peso dei componenti, utilizzando equazioni semi-empiriche adattate per le condizioni marziane, è presentata in @sec:mass-breakdown dopo che l'analisi dei vincoli ha determinato la geometria richiesta.

## Requisiti derivati {#sec:derived-requirements}

Questa sezione traduce le esigenze qualitative dell'utente identificate in @sec:user-needs in requisiti quantitativi e verificabili. Ogni requisito è derivato dalle esigenze degli stakeholder attraverso l'analisi dell'ambiente operativo, delle prestazioni delle piattaforme di riferimento e dei vincoli fisici. I requisiti documentati qui forniscono gli input numerici per l'analisi dei vincoli (@sec:constraint-analysis).

### Requisiti operativi {#sec:operational-requirements}

I requisiti operativi definiscono l'inviluppo di prestazioni della missione derivato dalle esigenze utente N1 (raggio esteso), N2 (imaging aereo), N5 (autonomia estesa) e N4 (capacità VTOL).

#### Raggio operativo

L'UAV dovrà raggiungere un raggio operativo di almeno 50 km. Questo requisito deriva dall'esigenza utente N1 (raggio esteso oltre la capacità dei rover di superficie). Il rover Curiosity ha percorso circa 35 km in totale in oltre un decennio sulla superficie marziana [@nasaMarsScienceLaboratory2025]. Un raggio di 50 km consente il rilevamento in un singolo volo di aree inaccessibili ai rover entro tempistiche di missione pratiche, fornendo un miglioramento sostanziale delle capacità che giustifica lo sviluppo dell'UAV. La verifica è dimostrata attraverso test di volo di autonomia che copre 100 km di distanza andata e ritorno.

#### Altitudine operativa

L'UAV dovrà operare ad altitudini tra 30 m e 350 m sopra il livello del suolo. L'altitudine minima di 30 m deriva dalle esigenze di separazione dal terreno: le distribuzioni di frequenza-dimensione delle rocce nei siti di atterraggio marziani indicano che le rocce pericolose sono tipicamente alte 0.5 m o circa 1 m di diametro [@golombekRockSizeFrequencyDistributions2021], e 30 m fornisce un fattore di sicurezza di 60× rispetto ai più grandi ostacoli superficiali comuni. L'altitudine massima di 350 m deriva dai requisiti di risoluzione dell'imaging (esigenza utente N2). La mappatura geologica richiede tipicamente una distanza di campionamento a terra (GSD) di 5-10 cm per pixel. Per una camera con passo pixel di 2.4 μm e lunghezza focale di 8.8 mm (tipico sensore da 1 pollice come il DJI Air 2S [@djiDJIAir2S2021]), il GSD è calcolato come:

$$GSD = \frac{H \cdot p}{f}$$ {#eq:gsd}

dove $H$ è l'altitudine di volo, $p$ è il passo pixel, e $f$ è la lunghezza focale. Per ottenere un GSD di 10 cm è richiesto:

$$H_\text{max} = \frac{GSD \cdot f}{p} = \frac{0.10 \times 8.8 \times 10^{-3}}{2.4 \times 10^{-6}} = 367 \text{ m}$$ {#eq:hmax}

Arrotondando a 350 m si assicura che il requisito di GSD di 10 cm sia soddisfatto con margine. La verifica è dimostrata attraverso test di volo con mantenimento di altitudine e validazione dell'imaging.

#### Autonomia di volo

L'UAV dovrà raggiungere un tempo di volo totale di almeno 60 minuti, incluse le fasi di hovering e crociera. Questo requisito deriva dall'esigenza utente N5 (autonomia estesa) in combinazione con il requisito di raggio operativo. Il profilo di missione (@sec:mission-parameters) richiede 42 minuti di tempo di transito (100 km andata e ritorno a 40 m/s), 15 minuti di operazioni di rilevamento, e 3 minuti di fasi di hovering (decollo, atterraggio, contingenza), per un totale di 60 minuti. Questa autonomia supera sostanzialmente l'elicottero Ingenuity, che ha raggiunto voli individuali fino a 169 secondi e tempo di volo cumulativo di circa 129 minuti su 72 voli [@nasaIngenuityMarsHelicopter2024; @tzanetosIngenuityMarsHelicopter2022]. La verifica è dimostrata attraverso test di volo con profilo di missione completo.

### Requisiti ambientali {#sec:environmental-requirements}

I requisiti ambientali definiscono le condizioni in cui l'UAV deve operare, derivati dalle esigenze utente N7 (tolleranza al vento), N8 (protezione dalla polvere), N10 (tolleranza alle radiazioni) e N11 (compatibilità termica).

#### Tolleranza al vento

L'UAV dovrà operare in sicurezza con venti sostenuti fino a 10 m/s. Le misurazioni del vento da parte del rover Mars 2020 Perseverance nel cratere Jezero hanno rilevato velocità medie del vento di 3.2 ± 2.3 m/s, con picchi pomeridiani che raggiungono 6.1 ± 2.2 m/s; il 99% dei venti misurati è rimasto sotto i 10 m/s [@viudez-moreirasWindsMars20202022]. Il limite di 10 m/s accomoda le condizioni marziane tipiche con margine. Sebbene i venti delle tempeste di polvere possano raggiungere 27 m/s [@nasaFactFictionMartian2015], le operazioni di volo durante tali eventi sono rinviate piuttosto che progettate per essere sostenute. La verifica include test in galleria del vento dell'autorità di controllo e simulazione di volo con profili di raffica di 10 m/s.

#### Protezione dalla polvere

Tutti i componenti critici dovranno essere protetti secondo lo standard IP6X. La protezione dalla polvere segue il codice IP definito dalla IEC 60529 [@internationalelectrotechnicalcommissionDegreesProtectionProvided2013]. IP6X denota involucri a tenuta di polvere con esclusione completa del particolato, necessaria data la fine regolite marziana (dimensioni delle particelle 1-100 μm) che può degradare cuscinetti meccanici e superfici ottiche. La verifica avviene attraverso test di ingresso polvere secondo le procedure IEC 60529 o equivalenti.

#### Tolleranza alle radiazioni

L'elettronica dovrà tollerare una dose totale ionizzante di almeno 1 krad(Si). Lo strumento RAD del Mars Science Laboratory ha misurato un tasso medio di dose assorbita di circa 76 mGy/anno (7.6 rad/anno, o 0.0076 krad/anno) sulla superficie marziana [@hasslerMarsSurfaceRadiation2014]. In una missione biennale, la dose accumulata è circa 0.015 krad. Un requisito di tolleranza alle radiazioni di 1 krad(Si) di dose totale ionizzante fornisce un margine di circa 67× ed è raggiungibile con elettronica commerciale off-the-shelf (COTS), che tipicamente tollera 5-20 krad senza richiedere costosi componenti radiation-hardened [@brunettiCOTSDevicesSpace2024]. La verifica avviene attraverso dati di test di radiazione a livello di componente o qualifica per heritage.

#### Range di temperatura operativa

L'UAV dovrà operare a temperature ambiente da −80 °C a +20 °C. Le escursioni termiche diurne di Marte variano da circa −80 °C (notte) a +20 °C (mezzogiorno) a seconda della stagione e della posizione. I sottosistemi critici (in particolare batterie e camere) richiedono gestione termica per funzionare entro i loro range operativi. Il requisito si applica all'ambiente circostante; le temperature interne dei sottosistemi sono gestite attraverso isolamento e riscaldamento attivo. La verifica avviene attraverso test in vuoto termico attraverso il range di temperatura.


### Selezione del fattore di carico {#sec:load-factor-selection}

Le equazioni di stima del peso strutturale in @sec:mass-breakdown includono il fattore di carico ultimo ($n_\text{ult}$) come parametro chiave. Questa sottosezione documenta la selezione del fattore di carico e la sua giustificazione.

#### Definizioni

Il *fattore di carico limite* ($n_\text{limite}$) è il massimo fattore di carico atteso in operazione normale senza deformazione permanente. Il *fattore di carico ultimo* ($n_\text{ult}$) è il fattore di carico limite moltiplicato per un fattore di sicurezza [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017]:

$$n_\text{ult} = n_\text{limite} \times FS$$ {#eq:n-ult-definition}

dove $FS = 1.5$ è il fattore di sicurezza aerospaziale standard [@europeanunionaviationsafetyagencyCertificationSpecificationsNormalCategory2017, CS 23.2230(a)(2)]. Questo fattore 1.5 tiene conto delle variazioni delle proprietà dei materiali, delle tolleranze di fabbricazione, della fatica e delle tolleranze ai danni, e dell'incertezza nella previsione dei carichi.
La struttura deve sopportare i carichi limite senza deformazione permanente, e i carichi ultimi senza cedimento.

#### Motivazione della selezione del fattore di carico

Per l'UAV marziano, viene adottato un fattore di carico limite di $n_\text{limite} = 2.5$, che produce:

$$n_\text{ult} = 2.5 \times 1.5 = 3.75$$

Questo valore rappresenta il limite inferiore dei requisiti della categoria normale CS-23 ed è giustificato da quattro considerazioni.

Primo, l'operazione senza equipaggio cambia fondamentalmente la filosofia di progettazione strutturale. Il cedimento strutturale di un aeromobile con equipaggio mette a rischio vite umane, motivando margini di sicurezza conservativi. Per un veicolo autonomo senza equipaggio, le conseguenze del cedimento sono limitate alla perdita della missione e al danno all'equipaggiamento. Margini di sicurezza strutturale più bassi sono quindi accettabili e standard per i sistemi senza pilota.

Secondo, il volo autonomo con inviluppo di manovra limitato fornisce protezione intrinseca dal carico. Il sistema di controllo di volo impone limiti di manovra rigorosi tramite software. A differenza degli aeromobili pilotati, dove manovre rapide o di panico possono generare carichi inattesi, l'autopilota limita l'angolo di rollio (tipicamente 45-60°) e il fattore di carico comandato (tipicamente 2-3 g). Questo inviluppo limitato assicura che il carico limite di progetto non sia superato in operazione normale.

Terzo, i carichi da raffica sono sostanzialmente ridotti nell'atmosfera marziana. I fattori di carico indotti dalle raffiche scalano con la densità atmosferica. L'incremento del fattore di carico da raffica può essere espresso come:

$$\Delta n_\text{raffica} \propto \frac{\rho \cdot U_\text{de} \cdot V \cdot a}{W/S}$$

dove $\rho$ è la densità atmosferica, $U_\text{de}$ è la velocità di raffica di progetto, $V$ è la velocità di volo, e $a$ è la pendenza della curva di portanza. Alla densità superficiale di Marte (circa 0.020 kg/m³), i carichi da raffica sono circa 60 volte inferiori rispetto al livello del mare terrestre per velocità di raffica equivalenti. Anche con le velocità di raffica di progetto più elevate su Marte (fino a 10 m/s, secondo @sec:user-needs), il contributo del carico da raffica rimane trascurabile rispetto ai carichi di manovra. Il fattore di carico di manovra domina quindi la progettazione strutturale.

Quarto, i precedenti dei velivoli a rotore marziani supportano fattori di carico ridotti. Lo studio NASA Mars Science Helicopter [@johnsonMarsScienceHelicopter2020] ha notato che "i carichi aerodinamici sulla pala sono piccoli a causa della bassa densità atmosferica su Marte," consentendo design strutturali leggeri innovativi. Sebbene i fattori di carico specifici non siano pubblicati per Ingenuity o MSH, l'atmosfera rarefatta riduce fondamentalmente il carico aerodinamico rispetto ai design terrestri.

#### Confronto con altre categorie di aeromobili

@tbl:load-factor-comparison presenta i fattori di carico dell'UAV marziano nel contesto di altre categorie di aeromobili.

: Confronto dei fattori di carico per varie categorie di aeromobili {#tbl:load-factor-comparison}

| Categoria aeromobile | $n_\text{limite}$ | FS | $n_\text{ult}$ | Fonte |
|:---|:---:|:---:|:---:|:---|
| CS-25 trasporto (alto W) | 2.5 | 1.5 | 3.75 | FAR Part 25 |
| CS-25 trasporto (basso W) | 3.8 | 1.5 | 5.7 | FAR Part 25 |
| CS-23 normale (pesante) | 2.5 | 1.5 | 3.75 | CS-23 Amdt 4 §23.337 |
| CS-23 normale (leggero) | 3.8 | 1.5 | 5.7 | CS-23 Amdt 4 §23.337 |
| CS-23 utility | 4.4 | 1.5 | 6.6 | CS-23 Amdt 4 |
| CS-23 acrobatico | 6.0 | 1.5 | 9.0 | CS-23 Amdt 4 |
| UAV marziano (questo studio) | 2.5 | 1.5 | 3.75 | Questo lavoro |

Il valore selezionato $n_\text{ult} = 3.75$ corrisponde al limite inferiore degli aeromobili certificati di categoria normale e al valore utilizzato per gli aeromobili da trasporto pesanti. Questa selezione bilancia la riduzione del peso strutturale con margini di sicurezza accettabili per una piattaforma di ricerca senza equipaggio.

Per quanto riguarda lo status regolamentare, EASA CS-23 e FAA Part 23 sono standard di certificazione terrestri per aeromobili con equipaggio. L'UAV marziano non è soggetto a queste normative. CS-23 è utilizzato qui come riferimento metodologico per stabilire fattori di carico consistenti e standard del settore, non come requisito regolamentare.

L'impatto sul peso strutturale del ridotto fattore di carico ultimo è quantificato in @sec:mass-breakdown, dove le equazioni di stima del peso sono applicate alla geometria dimensionata. Il ridotto fattore di carico consente circa il 23% di riduzione del peso dell'ala e il 10% di riduzione del peso della fusoliera rispetto agli aeromobili leggeri progettati secondo gli standard CS-25 ($n_\text{ult} = 5.7$).


### Limiti dei parametri geometrici {#sec:geometry-bounds}

Questa sezione definisce i parametri geometrici della pianta alare utilizzati nell'analisi dei vincoli e nella stima del peso. Ogni parametro comporta compromessi che determinano lo spazio di progetto ottimale per l'UAV marziano.

#### Allungamento

L'allungamento è limitato come:

$$AR \in [5, 7]$$ {#eq:ar-bounds}

La resistenza indotta scala inversamente con l'allungamento:

$$C_{D,i} = \frac{C_L^2}{\pi \cdot AR \cdot e}$$ {#eq:induced-drag}

Un maggiore allungamento riduce la resistenza indotta, mentre il peso dell'ala aumenta approssimativamente come $AR^{0.6}$ [@sadraeyAircraftDesignSystems2013]. A parità di superficie alare, un maggiore allungamento riduce anche la corda media:

$$\bar{c} = \sqrt{\frac{S}{AR}}$$ {#eq:chord-from-ar}

Questa riduzione della corda influenza il numero di Reynolds, che è vincolato dai requisiti di prestazione del profilo.

L'intervallo selezionato è basato sia sui dati degli UAV terrestri che sugli studi specifici per Marte. Gli allungamenti tipici per piccoli UAV variano da 4 a 12 [@sadraeyAircraftDesignSystems2013]. I design di UAV marziani in letteratura selezionano consistentemente allungamenti nell'intervallo da 5 a 6. Il design dell'aereo marziano ARES ha utilizzato $AR$ = 5.6 [@braunDesignARESMars2006]. Barbato et al. hanno trovato un $AR$ ottimale da 5.3 a 6.3 per un UAV marziano a energia solare da 24 kg [@barbatoPreliminaryDesignFixedWing2024], dimostrando che l'allungamento ottimale aumenta con il coefficiente di portanza e diminuisce con la massa del payload.

Viene adottato un allungamento di base di $AR$ = 6, che rappresenta un compromesso tra riduzione della resistenza indotta (che favorisce AR più alti) e peso strutturale (che favorisce AR più bassi). All'MTOW target di 10 kg, questo allungamento fornisce un adeguato rapporto portanza/resistenza mantenendo una corda alare ragionevole per i requisiti di numero di Reynolds e uno spessore strutturale per la capacità di sopportare i carichi.


#### Rapporto di spessore

Il rapporto di spessore dell'ala è limitato da considerazioni strutturali e aerodinamiche:

$$t/c \in [0.06, 0.11]$$ {#eq:tc-bounds}

Questo intervallo riflette le caratteristiche di spessore dei profili candidati a basso Reynolds dal database UIUC [@seligSummaryLowSpeedAirfoil1995; @williamsonSummaryLowSpeedAirfoil2012]. I profili candidati coprono rapporti di spessore dal 6.2% (AG12, serie AG sottile) fino al 10.5% (S7055, design bilanciato). Il profilo general-purpose E387 ha $t/c$ = 9.1%, il profilo a bassa resistenza SD8000 ha $t/c$ = 8.9%, e il profilo general-purpose SD7037 ha $t/c$ = 9.2%.

Il peso strutturale dell'ala scala approssimativamente come $(t/c)^{-0.3}$ [@sadraeyAircraftDesignSystems2013], favorendo profili più spessi per l'efficienza strutturale. Viene adottato un rapporto di spessore di base di $t/c$ = 0.09 per il dimensionamento, fornendo adeguato spessore strutturale pur rimanendo compatibile con i profili candidati. La selezione specifica del profilo è rinviata a @sec:airfoil-selection dove le prestazioni aerodinamiche al numero di Reynolds di progetto sono valutate.

#### Rapporto di rastremazione

Il rapporto di rastremazione è vincolato a:

$$\lambda \in [0.4, 0.6]$$ {#eq:taper-bounds}

dove $\lambda = c_\text{tip} / c_\text{root}$.

Per la minima resistenza indotta, la distribuzione di portanza lungo l'apertura ideale è ellittica, e per un'ala non a freccia, un rapporto di rastremazione di circa $\lambda$ = 0.4 approssima strettamente questa distribuzione di carico [@sadraeyAircraftDesignSystems2013]. Le ali rastremate concentrano inoltre il materiale strutturale vicino alla radice dove i momenti flettenti sono massimi, migliorando l'efficienza strutturale, sebbene rapporti di rastremazione più bassi aumentino la suscettibilità allo stallo di estremità. Le ali rettangolari ($\lambda$ = 1.0) offrono la fabbricazione più semplice; il limite superiore di $\lambda$ = 0.6 rappresenta un compromesso verso la semplicità di fabbricazione pur mantenendo un carico quasi ellittico.

Viene adottato un valore nominale di $\lambda$ = 0.5 per il dimensionamento di base, fornendo circa il 98% della resistenza indotta minima teorica offrendo al contempo buone caratteristiche di stallo e ragionevole complessità di fabbricazione.

#### Angolo di freccia

L'angolo di freccia al quarto di corda è fissato a:

$$\Lambda = 0°$$ {#eq:sweep-selection}

La freccia alare è principalmente utilizzata per ritardare gli effetti di comprimibilità a velocità transoniche, tipicamente sopra $M$ = 0.7 [@sadraeyAircraftDesignSystems2013]. Il meccanismo è che la freccia riduce la componente di velocità perpendicolare al bordo d'attacco dell'ala, riducendo effettivamente il numero di Mach locale.

Al numero di Mach di crociera dell'UAV marziano di circa $M$ = 0.17, gli effetti di comprimibilità sono del tutto trascurabili. La freccia non fornisce alcun beneficio aerodinamico a questa velocità e introduce penalità tra cui maggiore complessità strutturale dall'accoppiamento flessione-torsione, penalità di peso da strutture ad ala a freccia più pesanti, ridotta pendenza della curva di portanza che richiede angoli di attacco più elevati, e caratteristiche di stallo degradate poiché le ali a freccia tendono a stallare prima all'estremità, compromettendo il controllo di rollio.

Per l'UAV marziano viene adottata una configurazione senza freccia.

#### Riepilogo dei parametri geometrici

@tbl:geometry-summary consolida i parametri geometrici per l'analisi dei vincoli.

: Riepilogo dei parametri geometrici dell'ala {#tbl:geometry-summary}

| Parametro | Simbolo | Intervallo | Base | Motivazione |
|:----------|:------:|:-----:|:--------:|:----------|
| Allungamento | $AR$ | 5-7 | 6 | Precedenti UAV marziani, L/D vs. struttura |
| Rapporto di spessore | $t/c$ | 0.06-0.11 | 0.09 | Spessore strutturale vs. resistenza |
| Rapporto di rastremazione | $\lambda$ | 0.4-0.6 | 0.5 | Carico quasi ellittico |
| Angolo di freccia | $\Lambda$ | N.D. | 0° | Basso Mach, nessun beneficio |

### Parametri di velocità e tempo della missione {#sec:mission-parameters}

Questa sezione deriva e giustifica i parametri di velocità e tempo richiesti per l'analisi dei vincoli. Ogni parametro è tracciabile ai requisiti di missione (@sec:user-needs) e coerente con le condizioni atmosferiche (@sec:operational-environment).

#### Velocità di crociera

La selezione della velocità di crociera deve bilanciare vincoli multipli: numero di Mach, numero di Reynolds, consumo di potenza e requisiti di tempo di missione.

Rimanere ben sotto $M \approx 0.3$ mantiene piccole le correzioni per comprimibilità, poiché le variazioni di densità scalano approssimativamente con $M^2$ nel flusso subsonico. Viene presa come obiettivo una banda di Mach di progetto di $M_\infty \approx 0.16$-$0.28$, con una selezione iniziale intorno a $M \approx 0.17$. Utilizzando la velocità del suono su Marte all'altitudine operativa ($a$ = 230.8 m/s da @tbl:atmosphere), questo corrisponde a:

$$V_\text{crociera} = M \times a = 0.17 \times 230.8 \approx 40 \text{ m/s}$$ {#eq:cruise-velocity-value}

Questa velocità è circa il doppio di quella degli UAV VTOL ibridi terrestri tipici ma rappresenta un compromesso necessario: velocità inferiori richiederebbero corde alari eccessivamente grandi per raggiungere numeri di Reynolds accettabili, mentre velocità superiori aumenterebbero significativamente il consumo di potenza. La potenza di crociera scala fortemente con la velocità una volta che la resistenza parassita domina ($P \sim D \times V$, con resistenza parassita $\sim V^2$, portando a $P \sim V^3$).

Il numero di Reynolds in crociera è:

$$Re = \frac{\rho \cdot V \cdot c}{\mu}$$ {#eq:reynolds-definition}

Utilizzando le proprietà atmosferiche all'altitudine operativa da @tbl:atmosphere ($\rho$ = 0.0196 kg/m³, $\mu$ = 1.08 × 10⁻⁵ Pa·s), con $V$ = 40 m/s e puntando a $Re$ = 60.000:

$$c = \frac{Re \cdot \mu}{\rho \cdot V} = \frac{60{,}000 \times 1.08 \times 10^{-5}}{0.0196 \times 40} = 0.83 \text{ m}$$

La superficie alare è legata alla corda attraverso l'allungamento. Per $AR$ = 6 e corda media $\bar{c}$ = 0.83 m:

$$S = \bar{c}^2 \times AR = 0.83^2 \times 6 = 4.1 \text{ m}^2$$

@tbl:chord-velocity presenta la relazione tra velocità di crociera, corda e superficie alare per raggiungere $Re$ = 60.000 con $AR$ = 6.

: Requisiti di corda e superficie alare per Re = 60.000 {#tbl:chord-velocity}

| $V_\text{crociera}$ (m/s) | $\bar{c}$ richiesta (m) | $S$ richiesta (m²) con AR = 6 |
|:------------------------|:----------------------:|:------------------------:|
| 35 | 0.95 | 5.4 |
| 38 | 0.87 | 4.5 |
| 40 | 0.83 | 4.1 |

Queste superfici alari sono più grandi del tipico per piccoli UAV terrestri ma riflettono la bassa densità atmosferica su Marte. Per l'MTOW target di 10 kg (peso marziano $W$ = 37.1 N), una superficie alare di 4.1 m² produce un carico alare di circa 9 N/m².

Viene adottata una velocità di crociera di $V_\text{crociera}$ = 40 m/s, con un intervallo di sensibilità di 35-45 m/s per studi parametrici dell'analisi dei vincoli. Il raggio operativo di 50 km richiede una distanza andata e ritorno di 100 km, producendo un tempo di transito di 2500 s (circa 42 min) a 40 m/s.

#### Velocità minima

La velocità minima operativa fornisce un margine di sicurezza sopra la velocità di stallo. Secondo la pratica aerospaziale generale, le velocità di avvicinamento e minime operative per gli aeromobili sono tipicamente 1.2 volte la velocità di stallo [@sadraeyAircraftDesignSystems2013]:

$$V_\text{min} \geq 1.2 \times V_\text{stallo}$$ {#eq:v-min-constraint}

La velocità di stallo dipende dal carico alare:

$$V_\text{stallo} = \sqrt{\frac{2 \cdot (W/S)}{\rho \cdot C_{L,\text{max}}}}$$ {#eq:stall-speed-prelim}

Il fattore 1.2 assicura un margine adeguato per il recupero da disturbi di raffica, l'autorità di controllo a bassa velocità, e le manovre di transizione tra modalità di crociera e hovering.

#### Vincolo sul carico alare

Riarrangiando @eq:stall-speed-prelim per il carico alare:

$$\frac{W}{S} = \frac{1}{2} \rho V_\text{stallo}^2 C_{L,\text{max}}$$ {#eq:wing-loading-stall}

Per una velocità minima operativa $V_\text{min}$ con margine di sicurezza sopra lo stallo:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:wing-loading-constraint}

Questa equazione definisce il vincolo di stallo sul diagramma di matching. Su un diagramma con P/W sull'asse verticale e W/S sull'asse orizzontale, il vincolo di stallo appare come una linea verticale (W/S massimo costante) indipendente dal carico di potenza.

Per il progetto preliminare, utilizzando il carico alare derivato dall'analisi della velocità di crociera ($W/S \approx 9.000$ N/m² da @tbl:chord-velocity), $\rho$ = 0.01960 kg/m³, e $C_{L,\text{max}}$ = 1.200:

$$V_\text{stallo} = \sqrt{\frac{2 \times 9.000}{0.01960 \times 1.200}} = \sqrt{765.3} = 27.67 \text{ m/s}$$

$$V_\text{min} \geq 1.200 \times 27.67 = 33.20 \text{ m/s}$$

La velocità di crociera di 40.00 m/s fornisce un margine confortevole sopra la velocità minima, indicando che l'aeromobile opererà a coefficienti di portanza moderati durante la crociera piuttosto che vicino allo stallo. Questo margine permette manovre e fornisce sicurezza contro condizioni ventose.

#### Allocazione del tempo di hovering

Per la configurazione VTOL ibrida, il tempo di hovering è limitato al decollo verticale, all'atterraggio e alle operazioni di contingenza. L'allocazione del tempo è riassunta in @tbl:hover-allocation.

: Allocazione del tempo di hovering per il bilancio energetico {#tbl:hover-allocation}

| Fase di volo | Durata (s) | Descrizione |
|:-------------|-------------:|:------------|
| Salita al decollo | 30 | Salita verticale a 30 m di altitudine sicura |
| Transizione al decollo | 30 | Transizione da hovering a volo avanzato |
| Transizione all'atterraggio | 30 | Transizione da volo avanzato a hovering |
| Discesa all'atterraggio | 30 | Discesa controllata e contatto |
| Riserva di contingenza | 60 | Abort, evitamento ostacoli, atterraggio di precisione |
| Totale hovering | 180 | N.D. |

Il tempo totale di hovering di 180 s (3 min) è utilizzato per i calcoli energetici. Questa allocazione è conservativa rispetto alle operazioni VTOL terrestri, tenendo conto di tassi di salita più lenti nell'atmosfera rarefatta (stimati 1-2 m/s), fasi di transizione estese a causa della minore autorità di controllo, e contingenza per raffiche di vento inattese o scenari di abort. Per confronto, l'elicottero Ingenuity ha raggiunto tempi di volo totali di 90-170 secondi per operazioni di puro velivolo a rotore [@nasaIngenuityMarsHelicopter2024], sebbene il confronto diretto sia limitato poiché Ingenuity opera interamente in modalità hovering/volo avanzato a rotore piuttosto che transitando in crociera ad ala fissa.

#### Autonomia di crociera

Il requisito di autonomia di crociera è derivato dal raggio operativo di 50 km:

$$t_\text{crociera} = t_\text{andata} + t_\text{rilevamento} + t_\text{ritorno}$$ {#eq:cruise-time}

Le componenti sono: transito di andata (50.000 m / 40 m/s = 1250 s = 20.8 min), transito di ritorno (20.8 min), e rilevamento/loiter all'obiettivo (15 min per operazioni di mappatura). Il tempo totale di crociera è:

$$t_\text{crociera} = 20.8 + 20.8 + 15 \approx 57 \text{ min}$$ {#eq:cruise-endurance}

#### Riserva energetica

Una riserva energetica del 20% è mantenuta in aggiunta all'energia del profilo di missione. Questa riserva tiene conto di inefficienze di navigazione e correzioni di rotta, aumento di potenza dovuto a variazioni di densità atmosferica, hovering esteso per atterraggio di precisione, e capacità di ritorno di emergenza. La riserva è applicata al bilancio energetico totale, non alle singole fasi di volo.

#### Riepilogo del profilo di missione

@tbl:mission-profile presenta la timeline nominale della missione.

: Profilo di missione nominale {#tbl:mission-profile}

| Fase | Durata | Cumulativo | Modo di potenza |
|:------|:--------:|:----------:|:-----------|
| Hovering al decollo | 1 min | 1 min | Hovering |
| Crociera di andata | 21 min | 22 min | Crociera |
| Operazioni di rilevamento | 15 min | 37 min | Crociera |
| Crociera di ritorno | 21 min | 58 min | Crociera |
| Hovering all'atterraggio | 1 min | 59 min | Hovering |
| Contingenza | 1 min | 60 min | Hovering |
| Volo totale | 60 min | N.D. | N.D. |

Il tempo di volo di 60 minuti più il 20% di riserva energetica produce un requisito di autonomia di progetto di circa 72 minuti di capacità energetica equivalente.

### Riepilogo dei requisiti derivati {#sec:requirements-summary}

@tbl:derived-requirements consolida tutti gli input numerici richiesti per l'analisi dei vincoli, organizzati per categoria funzionale come definito nella metodologia di dimensionamento. Ogni parametro è tracciato alla sua fonte: esigenza utente (N1-N11), analisi fisica, dati di riferimento, o standard di progetto.

: Parametri di input per l'analisi dei vincoli {#tbl:derived-requirements}

| ID | Parametro | Simbolo | Valore | Derivato da |
|:---|:----------|:------:|:------|:-------------|
| Parametri di missione | | | | |
| M1 | Massa del payload | $m_\text{payload}$ | 1.0 kg | N2, N3 |
| M2 | Velocità di crociera | $V_\text{crociera}$ | 40 m/s | Vincoli Mach, Re |
| M3 | Velocità minima | $V_\text{min}$ | 1.2 × $V_\text{stallo}$ | Margine di sicurezza |
| M4 | Tempo di crociera | $t_\text{crociera}$ | 57 min | N1, N5 |
| M5 | Tempo di hovering | $t_\text{hover}$ | 3 min | N4 |
| M6 | Riserva energetica | N.D. | 20% | Margine di sicurezza |
| Parametri geometrici | | | | |
| G1 | Allungamento | $AR$ | 6 | Precedenti marziani |
| G2 | Rapporto di spessore | $t/c$ | 0.09 | Compromesso struttura/aero |
| G3 | Rapporto di rastremazione | $\lambda$ | 0.5 | Carico ellittico |
| G4 | Angolo di freccia | $\Lambda$ | 0° | Basso Mach |
| Coefficienti aerodinamici | | | | |
| A1 | Coefficiente di portanza max | $C_{L,\text{max}}$ | 1.20 | Galleria del vento UIUC |
| A2 | Efficienza di Oswald | $e$ | 0.87 | Correlazione AR=6 |
| A3 | Resistenza a portanza nulla | $C_{D,0}$ | 0.030 | Buildup componenti |
| Efficienze propulsive | | | | |
| P1 | Figura di merito | FM | 0.40 | Dati rotore basso Re |
| P2 | Efficienza elica | $\eta_\text{elica}$ | 0.55 | Analisi basso Re |
| P3 | Efficienza motore | $\eta_\text{motore}$ | 0.85 | Tipico BLDC |
| P4 | Efficienza ESC | $\eta_\text{ESC}$ | 0.95 | Tipico industriale |
| Parametri energetici | | | | |
| E1 | Energia specifica batteria | $e_\text{spec}$ | 270 Wh/kg | Li-ion stato solido |
| E2 | Profondità di scarica | DoD | 0.80 | Vita ciclica |
| E3 | Efficienza di scarica | $\eta_\text{batt}$ | 0.95 | C-rate moderato |
| Parametri del rotore | | | | |
| R1 | Carico del disco | DL | 30 N/m² | Analisi compromessi |
| R2 | $(L/D)_\text{eff}$ elicottero | $(L/D)_\text{eff}$ | 4.0 | Tipico elicottero |
| Parametri strutturali | | | | |
| S1 | Fattore di carico limite | $n_\text{limite}$ | 2.5 | N6, CS-23 |
| S2 | Fattore di sicurezza | FS | 1.5 | Standard CS-23 |
| S3 | Fattore di carico ultimo | $n_\text{ult}$ | 3.75 | S1 × S2 |



I requisiti operativi e ambientali da @sec:operational-requirements e @sec:environmental-requirements definiscono l'inviluppo di prestazioni della missione ma non sono input diretti per l'analisi dei vincoli. Il requisito di raggio operativo (OR-1, ≥ 50 km) determina la velocità di crociera (M2) e il tempo di crociera (M4). Il requisito di autonomia di volo (OR-4, ≥ 60 min) vincola la somma del tempo di crociera e del tempo di hovering (M4, M5). Il requisito di tolleranza al vento (ER-1, ≥ 10 m/s) motiva il margine di riserva energetica (M6) per accomodare condizioni di vento contrario.

# Analisi dei vincoli {#sec:constraint-analysis}

Questa sezione applica il dimensionamento basato sui vincoli a tre architetture candidate: velivolo a rotore, ala fissa e VTOL ibrido. Ogni configurazione è analizzata utilizzando gli input derivati in @sec:derived-requirements, e i risultati sono confrontati per informare la selezione dell'architettura.

## Configurazione a rotore {#sec:rotorcraft-analysis}

Questa sezione valuta se una configurazione a rotore puro (elicottero o multirotore) può soddisfare i requisiti di missione dell'UAV marziano. L'analisi sviluppa il quadro teorico per la potenza di hovering, la potenza in volo avanzato e l'autonomia, culminando in una valutazione di fattibilità rispetto al requisito di autonomia di 60 minuti.

### Analisi della potenza di hovering

#### Fondamenti della teoria della quantità di moto {#sec:momentum-theory}

Le prestazioni del rotore in hovering sono analizzate utilizzando la teoria della quantità di moto di Rankine-Froude, che tratta il rotore come un disco attuatore infinitamente sottile che trasferisce quantità di moto all'aria che lo attraversa [@leishmanPrinciplesHelicopterAerodynamics2006]. Questo modello idealizzato, nonostante la sua semplicità, fornisce intuizioni sulle prestazioni del rotore e sulla relazione tra spinta, potenza e carico del disco.

La teoria della quantità di moto fa le seguenti assunzioni: flusso uniforme e stazionario attraverso il disco del rotore; flusso non viscoso senza rotazione nella scia; condizioni incomprimibili (valide per $M < 0.3$); e flusso unidimensionale attraverso un getto ben definito.

Dal principio di conservazione della quantità di moto del fluido, la spinta del rotore eguaglia la variazione temporale della quantità di moto dell'aria che passa attraverso il disco del rotore. Per un rotore in hovering con velocità indotta $v_i$ al piano del disco, la spinta è [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$T = \dot{m} \cdot w = 2\rho A v_i^2$$ {#eq:thrust-momentum}

dove $\dot{m} = \rho A v_i$ è la portata massica attraverso il disco, $w = 2v_i$ è la velocità della scia a valle (dalla conservazione dell'energia), $\rho$ è la densità dell'aria, e $A$ è l'area del disco del rotore.

Risolvendo @eq:thrust-momentum per la velocità indotta al disco del rotore si ottiene [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$v_i = \sqrt{\frac{T}{2\rho A}}$$ {#eq:induced-velocity}

Questo risultato fondamentale mostra che la velocità indotta scala con la radice quadrata della spinta e inversamente con l'area del disco e la densità. La velocità indotta può anche essere espressa in termini di carico del disco ($DL = T/A$):

$$v_i = \sqrt{\frac{DL}{2\rho}}$$ {#eq:induced-velocity-dl}

La potenza ideale richiesta per l'hovering è il prodotto di spinta e velocità indotta [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{ideale} = T \cdot v_i = T \sqrt{\frac{T}{2\rho A}}$$ {#eq:ideal-power-1}

Riarrangiando:

$$P_\text{ideale} = \frac{T^{3/2}}{\sqrt{2\rho A}}$$ {#eq:ideal-power}

Questa equazione rivela relazioni di scala: la potenza scala come $T^{3/2}$, il che significa che la potenza di hovering aumenta più rapidamente della spinta; la potenza scala come $\rho^{-1/2}$, quindi la bassa densità atmosferica aumenta sostanzialmente i requisiti di potenza; e la potenza scala come $A^{-1/2}$, favorendo grandi aree del disco del rotore.

Per il volo in hovering dove la spinta eguaglia il peso ($T = W$):

$$P_\text{ideale} = \frac{W^{3/2}}{\sqrt{2\rho A}} = W \sqrt{\frac{DL}{2\rho}} = W \sqrt{\frac{W/A}{2\rho}}$$ {#eq:ideal-power-weight}

#### Figura di merito {#sec:figure-of-merit}

Il risultato della teoria della quantità di moto rappresenta un limite inferiore idealizzato sulla potenza di hovering. I rotori reali subiscono perdite aggiuntive dovute alla resistenza di profilo sulle sezioni delle pale, alla distribuzione non uniforme del flusso indotto, alle perdite di estremità (effetti di pala finita) e alla rotazione nella scia.

La figura di merito (FM) quantifica l'efficienza di un rotore reale rispetto alla previsione ideale della teoria della quantità di moto [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$FM = \frac{P_\text{ideale}}{P_\text{reale}} < 1$$ {#eq:figure-of-merit}

Riarrangiando per ottenere la potenza di hovering reale:

$$P_\text{hover} = \frac{P_\text{ideale}}{FM} = \frac{T^{3/2}}{FM \cdot \sqrt{2\rho A}}$$ {#eq:hover-power}

La figura di merito adottata per il dimensionamento dei velivoli a rotore marziani ($FM$ = 0.4000) è documentata in @sec:propulsion-efficiency, rappresentando una stima conservativa nell'intervallo atteso di 0.30-0.50 per l'operazione di rotori MAV a basso Reynolds.

#### Requisiti di potenza elettrica

La potenza elettrica prelevata dalla batteria deve tenere conto delle perdite nel motore e nel regolatore elettronico di velocità (ESC):

$$P_\text{elettrica,hover} = \frac{P_\text{hover}}{\eta_\text{motore} \cdot \eta_\text{ESC}}$$ {#eq:electric-hover}

Sostituendo l'equazione della potenza di hovering:

$$P_\text{elettrica,hover} = \frac{W^{3/2}}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC} \cdot \sqrt{2\rho A}}$$ {#eq:electric-hover-full}

La catena di efficienza combinata dalla batteria alla spinta del rotore è data da @eq:hover-efficiency:

$$\eta_\text{hover} = FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}$$

Utilizzando i valori di efficienza da @tbl:efficiency-parameters ($FM$ = 0.4000, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza combinata di hovering è $\eta_\text{hover}$ = 0.3230.

Questo significa che solo il 32% dell'energia elettrica dalla batteria produce potenza di spinta utile in hovering. Il restante 68% è perso per resistenza di profilo del rotore, effetti di flusso indotto non ideali, perdite nel rame e nel ferro del motore, e perdite di commutazione dell'ESC.

#### Vincolo di carico di potenza

Il carico di potenza (spinta per unità di potenza) per l'hovering può essere espresso riarrangiando @eq:hover-power:

$$\frac{P_\text{hover}}{W} = \frac{1}{FM} \cdot \sqrt{\frac{W/A}{2\rho}} = \frac{1}{FM} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-power-loading}

Questa equazione definisce il vincolo di hovering sul diagramma di matching. Per un dato carico del disco e densità atmosferica, il rapporto potenza-peso richiesto è fisso e indipendente dal carico alare. Su un diagramma di matching con P/W sull'asse verticale e W/S sull'asse orizzontale, il vincolo di hovering appare come una linea orizzontale.

Includendo la catena di efficienza elettrica:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}} \cdot \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint}

### Prestazioni in volo avanzato

#### Componenti di potenza in volo avanzato

In volo avanzato, la potenza totale richiesta da un velivolo a rotore comprende molteplici componenti [@leishmanPrinciplesHelicopterAerodynamics2006]:

$$P_\text{totale} = P_i + P_0 + P_p + P_c$$ {#eq:forward-power-components}

dove $P_i$ è la potenza indotta (per generare portanza), $P_0$ è la potenza di profilo (per vincere la resistenza della sezione della pala), $P_p$ è la potenza parassita (per vincere la resistenza della fusoliera e del mozzo), e $P_c$ è la potenza di salita (per cambiare l'energia potenziale gravitazionale).

Per il volo di crociera livellato ($P_c = 0$), la ripartizione della potenza segue uno schema caratteristico: a basse velocità, la potenza indotta domina (simile all'hovering); all'aumentare della velocità, la potenza indotta diminuisce (il rotore agisce più come un'ala); e ad alte velocità, la potenza parassita domina (scala come $V^3$).

La velocità di potenza minima si verifica dove la somma di queste componenti raggiunge un minimo, tipicamente a un rapporto di avanzamento $\mu = V/(\Omega R) \approx 0.15$-0.25.

#### Rapporto portanza-resistenza equivalente

Per il confronto con aeromobili ad ala fissa, l'efficienza del volo avanzato del velivolo a rotore può essere espressa come un rapporto portanza-resistenza equivalente [@leishmanPrinciplesHelicopterAerodynamics2006, Capitolo 1]:

$$\left(\frac{L}{D}\right)_\text{eff} = \frac{W \cdot V}{P_\text{totale}}$$ {#eq:equivalent-ld}

Questo parametro rappresenta l'efficienza aerodinamica complessiva del velivolo a rotore in volo avanzato, incorporando tutte le perdite di potenza. Riarrangiando:

$$P_\text{avanzato} = \frac{W \cdot V}{(L/D)_\text{eff}}$$ {#eq:forward-power-ld}

I valori tipici di L/D equivalente sono riassunti in @tbl:rotorcraft-ld. L'efficienza aerodinamica relativamente scarsa deriva da diversi fattori inerenti ai velivoli a rotore: il mozzo del rotore e gli attacchi delle pale creano una sostanziale resistenza parassita; la resistenza di profilo sulle sezioni delle pale è inevitabile, anche ad alta velocità; la pala avanzante subisce effetti di comprimibilità ad alta velocità; e la pala retrocedente può subire stallo, limitando la velocità di avanzamento.

Per un velivolo a rotore marziano senza ala, l'L/D equivalente è $(L/D)_\text{eff}$ = 4.000, rappresentando l'estremo inferiore della gamma degli elicotteri a causa dell'assenza dell'ottimizzazione progettuale presente negli elicotteri terrestri (secondo @sec:rotorcraft-ld).

#### Potenza elettrica in volo avanzato

Includendo la catena di efficienza elettrica, la potenza dalla batteria per il volo avanzato è:

$$P_\text{elettrica,avanzato} = \frac{W \cdot V}{(L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC}}$$ {#eq:forward-electric-power}

### Analisi dell'autonomia

#### Modello dell'energia della batteria

L'energia utilizzabile dalla batteria è derivata da @eq:battery-energy-fraction in @sec:battery-utilisation:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Sostituendo i valori dei parametri da @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) e @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500):

$$\frac{E_\text{disponibile}}{MTOW} = 0.3500 \times 270.0 \times 0.8000 \times 0.9500 = 71.82 \text{ Wh/kg}$$

Per l'MTOW di base = 10.00 kg:

$$E_\text{disponibile} = 71.82 \times 10.00 = 718.2 \text{ Wh}$$

#### Equazione dell'autonomia del velivolo a rotore

Per un velivolo a rotore in volo avanzato, l'autonomia è determinata dall'energia disponibile e dal consumo di potenza:

$$t_\text{autonomia} = \frac{E_\text{disponibile}}{P_\text{elettrica,avanzato}}$$ {#eq:endurance-definition}

Sostituendo le espressioni per l'energia disponibile (@eq:battery-energy-fraction) e la potenza di volo avanzato (@eq:forward-electric-power):

$$t_\text{autonomia} = \frac{f_\text{batt} \cdot MTOW \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt}}{W \cdot V / ((L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC})}$$ {#eq:endurance-expanded}

Poiché $W = MTOW \cdot g_\text{Marte}$, i termini MTOW si cancellano:

$$t_\text{autonomia} = \frac{f_\text{batt} \cdot e_\text{spec} \cdot DoD \cdot \eta_\text{batt} \cdot (L/D)_\text{eff} \cdot \eta_\text{motore} \cdot \eta_\text{ESC}}{g_\text{Marte} \cdot V}$$ {#eq:endurance-simple}

Questo risultato mostra che l'autonomia del velivolo a rotore è indipendente dall'MTOW (per frazioni di massa fisse). L'autonomia dipende dai parametri della batteria ($f_\text{batt}$, $e_\text{spec}$, $DoD$, $\eta_\text{batt}$), dall'efficienza aerodinamica ($(L/D)_\text{eff}$), dall'efficienza propulsiva ($\eta_\text{motore}$, $\eta_\text{ESC}$), e dalle condizioni di volo ($g_\text{Marte}$, $V$).

#### Calcolo dell'autonomia

Utilizzando i valori dei parametri da @sec:derived-requirements:

: Parametri per il calcolo dell'autonomia del velivolo a rotore {#tbl:endurance-parameters}

| Parametro | Simbolo | Valore | Unità |
|:----------|:------:|------:|:-----|
| Frazione batteria | $f_\text{batt}$ | 0.3500 | - |
| Energia specifica | $e_\text{spec}$ | 270.0 | Wh/kg |
| Profondità di scarica | $DoD$ | 0.8000 | - |
| Efficienza batteria | $\eta_\text{batt}$ | 0.9500 | - |
| L/D equivalente | $(L/D)_\text{eff}$ | 4.000 | - |
| Efficienza motore | $\eta_\text{motore}$ | 0.8500 | - |
| Efficienza ESC | $\eta_\text{ESC}$ | 0.9500 | - |
| Gravità marziana | $g_\text{Marte}$ | 3.711 | m/s² |
| Velocità di crociera | $V$ | 40.00 | m/s |

Convertendo l'energia specifica in J/kg: $e_\text{spec} = 270.0 \times 3600 = 972000$ J/kg

Sostituendo in @eq:endurance-simple:

$$t_\text{autonomia} = \frac{0.3500 \times 972000 \times 0.8000 \times 0.9500 \times 4.000 \times 0.8500 \times 0.9500}{3.711 \times 40.00}$$

$$t_\text{autonomia} = \frac{849706}{148.44} = 5723 \text{ s} = 95.39 \text{ min}$$ {#eq:endurance-result}

Questo calcolo rappresenta l'autonomia massima teorica assumendo che il 100% del tempo di volo sia trascorso in crociera efficiente in avanzamento. L'autonomia pratica è inferiore a causa delle fasi di hovering e dei requisiti di riserva, come analizzato nella valutazione di fattibilità sottostante.

### Valutazione di fattibilità

#### Analisi critica dell'autonomia del velivolo a rotore

L'autonomia teorica di 95.39 minuti calcolata sopra supera il requisito di 60 minuti, ma diversi fattori riducono l'autonomia raggiungibile per una missione con velivolo a rotore puro.

Un velivolo a rotore puro non può utilizzare la crociera ad ala fissa. L'$(L/D)_\text{eff}$ = 4.000 si applica al volo avanzato dell'elicottero, che è meno efficiente della crociera ad ala fissa.

Il profilo di missione richiede hovering per decollo, atterraggio e contingenza. Utilizzando @eq:hover-power e l'efficienza di hovering di 0.3230, il consumo di potenza in hovering supera la potenza di crociera. Per l'MTOW di base = 10.00 kg con carico del disco $DL$ = 30.00 N/m² e densità marziana $\rho$ = 0.01960 kg/m³, la velocità indotta è:

$$v_i = \sqrt{\frac{30.00}{2 \times 0.01960}} = \sqrt{765.3} = 27.68 \text{ m/s}$$

Il requisito di potenza di hovering è:

$$P_\text{hover} = \frac{W \cdot v_i}{FM \cdot \eta_\text{motore} \cdot \eta_\text{ESC}} = \frac{37.11 \times 27.68}{0.4000 \times 0.8500 \times 0.9500} = 3178 \text{ W}$$

Questa velocità indotta è dello stesso ordine di grandezza della velocità di crociera, e la potenza di hovering (3178 W) supera la potenza di crociera (circa 459.7 W), consumando energia significativa durante le fasi di hovering di 3 minuti.

La riserva energetica del 20% riduce l'autonomia effettiva.

Un aeromobile ad ala fissa raggiunge $(L/D) \approx 12$, circa tre volte superiore al velivolo a rotore. Questa differenza limita il raggio d'azione e l'autonomia del velivolo a rotore.

#### Confronto con i requisiti di missione

@tbl:rotorcraft-feasibility confronta la capacità del velivolo a rotore puro con i requisiti di missione:

: Valutazione di fattibilità del velivolo a rotore {#tbl:rotorcraft-feasibility}

| Requisito | Obiettivo | Capacità velivolo a rotore | Stato |
|:------------|:-------|:----------------------|:------:|
| Autonomia di crociera | ≥60 min | 57 min (con riserva 20%) | NON CONFORME |
| Raggio operativo | ≥50 km | 65 km (130 km raggio) | CONFORME |
| Capacità VTOL | Richiesta | Sì, intrinseca | CONFORME |
| Tempo di hovering | 3 min | Illimitato (limitato dalla potenza) | CONFORME |

L'energia utilizzabile è 718.2 Wh × 0.80 (riserva) = 574.6 Wh. L'energia di hovering (3 min a 3178 W) consuma 158.9 Wh, lasciando 415.7 Wh per il volo avanzato. La potenza di volo avanzato è $P = WV/(L/D)_\text{eff}/\eta = 37.11 \times 40.00 / (4.000 \times 0.8075) = 459.7$ W. Il tempo di volo avanzato è 415.7 Wh / 459.7 W = 0.904 h = 54.27 min. Autonomia totale: 57.27 min. Raggio: 40.00 m/s × 54.27 min × 60 s/min = 130.2 km.

La configurazione a velivolo a rotore non soddisfa il requisito di autonomia (57 min vs 60 min richiesti). Anche se soddisfacesse marginalmente il requisito, il margine sarebbe insufficiente:

#### Analisi di sensibilità

L'autonomia di 57.27 minuti rappresenta un margine del -4.5% al di sotto del requisito di 60 minuti, che è inaccettabile per una missione marziana.

Una volta che l'UAV parte dall'habitat, deve completare la missione. Non esiste un sito di atterraggio alternativo.

La densità atmosferica marziana varia con la stagione e il carico di polvere. Una riduzione del 10% della densità aumenta i requisiti di potenza di circa il 5%, degradando ulteriormente le prestazioni.

Le batterie al litio perdono capacità nel corso dei cicli di carica e nel freddo estremo. La degradazione della capacità riduce ulteriormente l'autonomia già insufficiente.

Se un rotore si guasta, un multirotore non può planare verso un atterraggio sicuro.

Per confronto, la configurazione VTOL ibrida raggiunge 91 minuti di autonomia (+52% di margine), fornendo un maggiore margine operativo. L'analisi della configurazione e la motivazione della selezione sono presentate in @sec:architecture-selection.

### Conclusione sulla configurazione a velivolo a rotore

La configurazione a velivolo a rotore puro non soddisfa il requisito minimo di autonomia (57.27 min vs 60 min richiesti), con un margine del -4.5% che è inaccettabile per le operazioni di missione. La configurazione presenta rischi operativi.

L'autonomia raggiungibile di 57.27 minuti è inferiore al requisito di 60 minuti di 2.73 minuti.

Qualsiasi variazione nella densità atmosferica, nella capacità della batteria o nei valori di efficienza degrada ulteriormente le prestazioni.

A differenza di un VTOL ibrido che può planare se il motore di crociera si guasta, un velivolo a rotore precipita immediatamente se qualsiasi rotore si guasta.

La limitazione fondamentale è il basso rapporto portanza-resistenza equivalente inerente ai velivoli a rotore in volo avanzato ($(L/D)_\text{eff} \approx 4$), che comporta un consumo di potenza in volo avanzato (460 W) circa il 45% superiore alla crociera del VTOL ibrido (318 W).

La valutazione di fattibilità per la configurazione a velivolo a rotore è riassunta in @tbl:rotorcraft-feasibility. Il confronto delle configurazioni e la motivazione della selezione sono presentati in @sec:architecture-selection.

## Configurazione ad ala fissa {#sec:fixed-wing-analysis}

Questa sezione valuta se una configurazione ad ala fissa pura (aeroplano convenzionale) può soddisfare i requisiti di missione dell'UAV marziano. L'analisi sviluppa il quadro teorico per il volo livellato stazionario, la potenza di crociera e l'autonomia, dimostrando che sebbene l'ala fissa raggiunga un'efficienza aerodinamica superiore, la configurazione non soddisfa la missione a causa del requisito VTOL. Un aeromobile ad ala fissa convenzionale richiede un'infrastruttura di pista che non esiste su Marte.

### Fondamenti del volo livellato stazionario

#### Equilibrio delle forze

Nel volo livellato, stazionario e non accelerato, due coppie di forze devono essere in equilibrio [@torenbeekSynthesisSubsonicAirplane1982, Capitolo 5]:

$$L = W$$ {#eq:lift-weight-equilibrium}

$$T = D$$ {#eq:thrust-drag-equilibrium}

dove $L$ è la portanza, $W$ è il peso dell'aeromobile, $T$ è la spinta, e $D$ è la resistenza. Queste condizioni fondamentali di equilibrio costituiscono la base per tutta l'analisi delle prestazioni.

#### Equazione della portanza

La forza di portanza aerodinamica è espressa come [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3]:

$$L = \frac{1}{2} \rho V^2 S C_L$$ {#eq:lift-equation}

dove $L$ è la forza di portanza (N), $\rho$ è la densità dell'aria (kg/m³), $V$ è la velocità vera (m/s), $S$ è l'area alare di riferimento (m²), e $C_L$ è il coefficiente di portanza (adimensionale).

Per il volo livellato dove $L = W$, il coefficiente di portanza richiesto per mantenere l'altitudine a una data velocità è:

$$C_L = \frac{2W}{\rho V^2 S} = \frac{2(W/S)}{\rho V^2}$$ {#eq:cl-required}

Questa equazione rivela un vincolo fondamentale per il volo su Marte: la bassa densità atmosferica ($\rho \approx 0.02000$ kg/m³) richiede alta velocità, grande superficie alare, o alto coefficiente di portanza per generare sufficiente portanza.

La resistenza aerodinamica totale è [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3]:

$$D = \frac{1}{2} \rho V^2 S C_D$$ {#eq:drag-equation}

Il coefficiente di resistenza è modellato utilizzando la polare di resistenza parabolica da @eq:drag-polar (secondo @sec:aerodynamic-analysis):

$$C_D = C_{D,0} + \frac{C_L^2}{\pi \cdot AR \cdot e}$$

dove $C_{D,0}$ è il coefficiente di resistenza a portanza nulla, $AR$ è l'allungamento alare, ed $e$ è il fattore di efficienza di Oswald. Il primo termine rappresenta la resistenza parassita (attrito superficiale, resistenza di forma, interferenza), che è indipendente dalla portanza. Il secondo termine è la resistenza indotta, derivante dall'ala ad apertura finita e proporzionale a $C_L^2$.

Utilizzando i valori da @tbl:aero-coefficients: $C_{D,0}$ = 0.03000, $e$ = 0.8692, $AR$ = 6.

### Rapporto portanza-resistenza

#### L/D dalla polare di resistenza

Il rapporto portanza-resistenza quantifica l'efficienza aerodinamica e determina direttamente le prestazioni di crociera [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.4]:

$$\frac{L}{D} = \frac{C_L}{C_D} = \frac{C_L}{C_{D,0} + C_L^2/(\pi \cdot AR \cdot e)}$$ {#eq:ld-ratio}

#### Rapporto portanza-resistenza massimo

Da @eq:ld-max-calculated e @eq:cl-optimum in @sec:aerodynamic-analysis, il massimo L/D si verifica al coefficiente di portanza ottimale dove la resistenza indotta eguaglia la resistenza parassita:

$$C_L^* = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = 0.7011$$

$$(L/D)_\text{max} = \frac{1}{2}\sqrt{\frac{\pi \cdot AR \cdot e}{C_{D,0}}} = 11.68$$

Questo L/D massimo di 11.68 rappresenta un miglioramento rispetto al velivolo a rotore ($(L/D)_\text{eff}$ = 4.000, secondo @sec:rotorcraft-analysis) di un fattore di circa 3.

#### Velocità per L/D massimo

La velocità alla quale si verifica $(L/D)_\text{max}$ si trova sostituendo $C_L^*$ in @eq:cl-required:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2(W/S)}{\rho C_L^*}}$$ {#eq:v-ld-max}

Per l'UAV marziano con stima $W/S \approx 7.300$ N/m² (dal vincolo di stallo), $\rho$ = 0.01960 kg/m³, e $C_L^*$ = 0.7011:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2 \times 7.300}{0.01960 \times 0.7011}} = \sqrt{1063} = 32.61 \text{ m/s}$$

Questa velocità ottimale è inferiore alla velocità di crociera di progetto di 40.00 m/s, indicando che l'UAV marziano opererà a un coefficiente di portanza inferiore a $C_L^*$ durante la crociera. A 40.00 m/s, l'L/D effettivo rimane alto (circa 10.50 per l'ala pura, ridotto leggermente per la configurazione QuadPlane).

### Analisi della potenza di crociera

#### Potenza richiesta per il volo livellato

La potenza richiesta per vincere la resistenza in volo livellato è il prodotto della forza di resistenza e della velocità [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.4]:

$$P_\text{aero} = D \times V$$ {#eq:power-aero}

Poiché $D = W/(L/D)$ in equilibrio:

$$P_\text{aero} = \frac{W \times V}{L/D}$$ {#eq:power-required}

Questa è la potenza aerodinamica che deve essere fornita al flusso d'aria per mantenere il volo livellato.

#### Potenza all'albero ed efficienza dell'elica

La potenza all'albero richiesta dal motore tiene conto dell'efficienza dell'elica [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3.4]:

$$P_\text{albero} = \frac{P_\text{aero}}{\eta_\text{elica}} = \frac{W \times V}{(L/D) \times \eta_\text{elica}}$$ {#eq:shaft-power}

dove $\eta_\text{elica}$ è l'efficienza dell'elica. A bassi numeri di Reynolds su Marte, l'efficienza dell'elica è degradata rispetto alle condizioni terrestri.

#### Potenza elettrica

Includendo le efficienze del motore e dell'ESC, la potenza elettrica prelevata dalla batteria è:

$$P_\text{elettrica} = \frac{P_\text{albero}}{\eta_\text{motore} \times \eta_\text{ESC}} = \frac{W \times V}{(L/D) \times \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC}}$$ {#eq:cruise-electric-power}

L'efficienza propulsiva combinata è data da @eq:cruise-efficiency:

$$\eta_\text{crociera} = \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC}$$

Utilizzando i valori di efficienza da @tbl:efficiency-parameters ($\eta_\text{elica}$ = 0.5500, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza di crociera combinata è $\eta_\text{crociera}$ = 0.4436.

#### Formulazione del carico di potenza

Esprimendo il requisito di potenza come carico di potenza (potenza per unità di peso):

$$\frac{P}{W} = \frac{V}{(L/D) \times \eta_\text{crociera}}$$ {#eq:power-loading-cruise}

Per la crociera a $V$ = 40.00 m/s con $(L/D)$ = 11.68 e $\eta_\text{crociera}$ = 0.4436:

$$\frac{P}{W} = \frac{40.00}{11.68 \times 0.4436} = 7.719 \text{ W/N}$$

Convertendo in W/kg utilizzando la gravità marziana ($g_\text{Marte}$ = 3.711 m/s²):

$$\frac{P}{m} = 7.719 \times 3.711 = 28.64 \text{ W/kg}$$ {#eq:cruise-power-loading}

Per l'MTOW di base di 10.00 kg (peso $W$ = 37.11 N), la potenza di crociera è:

$$P_\text{crociera} = 7.719 \times 37.11 = 286.4 \text{ W}$$

Questo è inferiore al requisito di potenza di hovering di 3178 W calcolato in @sec:rotorcraft-analysis di un fattore 11, mostrando la riduzione di potenza ottenuta dalla crociera ad ala fissa.

### Vincolo di stallo

#### Velocità di stallo

La velocità minima di volo (velocità di stallo) si verifica al coefficiente di portanza massimo. Da @eq:stall-speed-prelim in @sec:mission-parameters:

$$V_\text{stallo} = \sqrt{\frac{2W}{\rho S C_{L,\text{max}}}} = \sqrt{\frac{2(W/S)}{\rho C_{L,\text{max}}}}$$

Questa equazione stabilisce la relazione tra carico alare e velocità di stallo.

#### Vincolo di carico alare

Il vincolo di stallo, espresso come carico alare massimo ammissibile, è derivato da @eq:wing-loading-constraint in @sec:mission-parameters:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

Utilizzando $C_{L,\text{max}}$ = 1.200 (da @tbl:aero-coefficients), $\rho$ = 0.01960 kg/m³, e una velocità di stallo target di $V_\text{stallo}$ = 30.00 m/s:

$$\frac{W}{S} \leq \frac{1}{2} \times 0.01960 \times 30.00^2 \times 1.200 = 10.58 \text{ N/m}^2$$

Questo vincola il carico alare massimo ammissibile. Su un diagramma di matching, questo appare come una linea verticale (W/S costante) indipendente dal carico di potenza.

Il vincolo di carico alare su Marte è estremamente basso rispetto agli aeromobili terrestri (tipico $W/S$ = 1500-5000 N/m² per aeromobili leggeri). Questa è una conseguenza diretta dell'atmosfera rarefatta e rappresenta un driver significativo della geometria dell'aeromobile.

### Analisi dell'autonomia

#### Modello dell'energia della batteria

L'energia disponibile dalla batteria utilizza @eq:battery-energy-fraction da @sec:battery-utilisation:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Sostituendo i valori dei parametri da @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) e @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500), l'energia utilizzabile per unità di MTOW è 71.82 Wh/kg. Per l'MTOW di base = 10.00 kg, l'energia disponibile è $E_\text{disponibile}$ = 718.2 Wh.

#### Equazione dell'autonomia ad ala fissa

Per aeromobili ad ala fissa elettrici a velocità costante, l'autonomia è:

$$t_\text{autonomia} = \frac{E_\text{disponibile}}{P_\text{elettrica}}$$ {#eq:endurance-definition-fw}

Sostituendo le espressioni per l'energia disponibile e la potenza di crociera:

$$t_\text{autonomia} = \frac{f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}}{W \times V / ((L/D) \times \eta_\text{crociera})}$$

Poiché $W = MTOW \times g_\text{Marte}$, i termini MTOW si cancellano:

$$t_\text{autonomia} = \frac{f_\text{batt} \times e_\text{spec} \times DoD \times \eta_\text{batt} \times (L/D) \times \eta_\text{crociera}}{g_\text{Marte} \times V}$$ {#eq:endurance-fixedwing}

Questa è l'equazione dell'autonomia per la configurazione ad ala fissa. Si noti che l'autonomia è indipendente dall'MTOW per frazioni di massa fisse—lo stesso risultato del velivolo a rotore (@eq:endurance-simple).

#### Calcolo dell'autonomia

Utilizzando i valori dei parametri da @sec:derived-requirements:

: Parametri per il calcolo dell'autonomia ad ala fissa {#tbl:fw-endurance-parameters}

| Parametro | Simbolo | Valore | Unità |
|:----------|:------:|------:|:-----|
| Frazione batteria | $f_\text{batt}$ | 0.3500 | - |
| Energia specifica | $e_\text{spec}$ | 270.0 | Wh/kg |
| Profondità di scarica | $DoD$ | 0.8000 | - |
| Efficienza batteria | $\eta_\text{batt}$ | 0.9500 | - |
| Rapporto portanza-resistenza | $(L/D)$ | 11.68 | - |
| Efficienza di crociera | $\eta_\text{crociera}$ | 0.4436 | - |
| Gravità marziana | $g_\text{Marte}$ | 3.711 | m/s² |
| Velocità di crociera | $V$ | 40.00 | m/s |

Convertendo l'energia specifica in J/kg: $e_\text{spec} = 270 \times 3600 = 972{,}000$ J/kg

Sostituendo in @eq:endurance-fixedwing:

$$t_\text{autonomia} = \frac{0.35 \times 972{,}000 \times 0.80 \times 0.95 \times 11.7 \times 0.444}{3.711 \times 40}$$

$$t_\text{autonomia} = \frac{1{,}076{,}267}{148.44} = 7{,}251 \text{ s} \approx 121 \text{ min}$$ {#eq:endurance-fw-result}

La configurazione ad ala fissa raggiunge circa 2 ore di autonomia, superando il requisito di 60 minuti del 101%.

#### Calcolo del raggio

Alla velocità di crociera di 40 m/s:

$$R = V \times t_\text{autonomia} = 40 \times 7{,}251 = 290{,}040 \text{ m} \approx 289 \text{ km}$$

Il raggio teorico di circa 289 km supera ampiamente il requisito di 100 km andata e ritorno per il raggio operativo di 50 km.

### Problema del decollo e atterraggio

La configurazione ad ala fissa dimostra eccellenti prestazioni di crociera. Tuttavia, non può soddisfare il requisito di missione per le operazioni VTOL. Questa sezione quantifica il vincolo di decollo che squalifica l'ala fissa pura dalla considerazione.

#### Analisi della corsa di decollo

La distanza di corsa di decollo per un decollo convenzionale è [@torenbeekSynthesisSubsonicAirplane1982; @sadraeyAircraftDesignSystems2013]:

$$S_\text{TO} = \frac{V_\text{TO}^2}{2 \bar{a}}$$ {#eq:takeoff-roll}

dove $V_\text{TO} \approx 1.1 \times V_\text{stallo}$ è la velocità di distacco e $\bar{a}$ è l'accelerazione media durante la corsa di decollo.

L'accelerazione media dipende dal bilanciamento delle forze:

$$\bar{a} = \frac{g}{W} \left[ T - D - \mu_r (W - L) \right]_\text{media}$$ {#eq:takeoff-accel}

dove $\mu_r$ è il coefficiente di attrito di rotolamento (tipicamente 0.02-0.05 su superfici dure).

#### Effetti specifici di Marte sul decollo

Su Marte, diversi fattori aumentano la distanza di decollo:

Riguardo all'effetto della bassa densità sulla velocità di stallo, la velocità di stallo scala inversamente con la radice quadrata della densità. Per l'UAV marziano con $W/S = 7.3$ N/m² (al limite del vincolo di stallo), $C_{L,\text{max}} = 1.20$, e $\rho = 0.0196$ kg/m³:

$$V_\text{stallo} = \sqrt{\frac{2 \times 7.3}{0.0196 \times 1.20}} = \sqrt{619} = 24.9 \text{ m/s}$$

$$V_\text{TO} = 1.1 \times 24.9 = 27.4 \text{ m/s}$$

Riguardo all'effetto della bassa densità sull'accelerazione, sia la spinta (dall'elica) che l'assistenza dell'attrito di rotolamento (dalla portanza durante la corsa) sono ridotti dalla bassa densità. La spinta disponibile da un'elica scala approssimativamente con la densità, e la portanza che solleva il carico sulle ruote è anch'essa ridotta.

Per la stima della corsa di decollo, utilizzando la stima standard della corsa di decollo con la spinta disponibile e le condizioni marziane, assumendo un'accelerazione media di circa $a \approx 0.7$ m/s² (tenendo conto della riduzione di spinta e gravità):

$$S_\text{TO} = \frac{27.40^2}{2 \times 0.7000} = \frac{750.8}{1.400} = 536.3 \text{ m}$$ {#eq:takeoff-distance}

La corsa di decollo di circa 536 m è impraticabile per le operazioni su Marte—non esiste una pista preparata di questa lunghezza né può essere ragionevolmente costruita vicino a un habitat.

Anche con il basso carico alare vincolato dalla velocità di stallo (7.3 N/m²), la lunghezza della pista richiesta è proibitiva. Il problema è che la bassa densità atmosferica richiede una distanza di corsa di decollo sostanziale indipendentemente dal dimensionamento dell'ala.

#### Metodi di lancio alternativi

Esistono diversi metodi di lancio alternativi per aeromobili ad ala fissa senza piste, ma nessuno è pratico per le operazioni marziane da un habitat.

Il lancio con catapulta o rotaia richiede un'infrastruttura di terra sostanziale, inclusi il meccanismo di lancio, le rotaie guida e i sistemi di accumulo di energia, nessuno dei quali è disponibile in un ambiente abitativo marziano. Questo approccio aggiunge complessità operativa e carico di lavoro per l'equipaggio, poiché ogni lancio richiede l'installazione e il recupero dell'equipaggiamento.

Il decollo assistito da razzo (RATO) richiede booster a razzo solido che aggiungono massa significativa e sono monouso per volo, richiedendo set multipli per operazioni ripetute. Questo metodo presenta un pericolo per la sicurezza vicino a un habitat con equipaggio, e i prodotti di scarico possono contaminare le operazioni scientifiche.

Il lancio con sgancio da pallone richiede il trasporto dell'aeromobile in quota tramite pallone prima di rilasciarlo, ma non esiste un'infrastruttura di palloni su Marte. Questo approccio aggiunge complessità al concetto operativo, e il tempo di ascesa combinato con i vincoli di posizionamento limita la flessibilità operativa.

Il lancio aereo da un aeromobile portante non è applicabile perché non esiste un aeromobile portante su Marte.

Tutti i metodi di lancio alternativi non soddisfano i requisiti operativi per operazioni ripetute e autonome da un habitat marziano senza un'infrastruttura complessa.

#### Problema dell'atterraggio

L'atterraggio convenzionale presenta sfide simili. La velocità di avvicinamento di circa $V_\text{avvicinamento} \approx 1.3 \times V_\text{stallo} = 40.00$ m/s è alta. La decelerazione è limitata dalle basse forze di attrito, richiedendo centinaia o migliaia di metri di corsa di atterraggio. È richiesta una superficie preparata per evitare ostacoli e fornire una frenata costante. L'alta velocità di avvicinamento aumenta anche la sensibilità ai disturbi del vento. Il problema dell'atterraggio è potenzialmente più vincolante del decollo, poiché c'è meno margine di errore e nessuna opportunità per una riattaccata in emergenza senza capacità di hovering.

### Valutazione di fattibilità

#### Conformità ai requisiti

@tbl:fw-feasibility confronta la capacità dell'ala fissa con i requisiti di missione:

: Valutazione di fattibilità dell'ala fissa {#tbl:fw-feasibility}

| Requisito | Obiettivo | Capacità ala fissa | Stato |
|:------------|:-------|:----------------------|:------:|
| Autonomia di crociera | 60-90 min | 120.9 min | CONFORME |
| Raggio operativo | 50 km | 145.1 km | CONFORME |
| Capacità VTOL | Richiesta | Non possibile | NON CONFORME |
| Requisito di pista | Nessuno | 536 m di corsa | NON CONFORME |

La configurazione ad ala fissa supera i requisiti di autonomia e raggio (margine di autonomia +101%), mostrando l'effetto della crociera ad alto L/D. Tuttavia, non soddisfa il requisito VTOL, che è non negoziabile per le operazioni marziane senza infrastruttura di pista.

### Conclusione sulla configurazione ad ala fissa

La configurazione ad ala fissa pura non può soddisfare il requisito VTOL per le operazioni dell'UAV marziano.

Nonostante raggiunga $(L/D)$ = 11.68 e dimostri autonomia teorica (120.9 min) e raggio (290.3 km) che superano sostanzialmente i requisiti di missione, la configurazione ad ala fissa non può decollare o atterrare senza una pista preparata di circa 536 m. Tale infrastruttura non esiste su Marte e non può essere ragionevolmente costruita per operazioni UAV ripetute da un habitat con equipaggio.

L'analisi dell'ala fissa dimostra tre punti chiave. Primo, l'efficienza aerodinamica non è il fattore limitante per l'autonomia dell'UAV marziano; piuttosto, il vincolo infrastrutturale (VTOL) domina la selezione della configurazione. Secondo, un L/D moderato è raggiungibile con un'attenta selezione del profilo alare ai bassi numeri di Reynolds caratteristici del volo marziano, sebbene i valori siano inferiori rispetto agli aeromobili terrestri a causa del difficile ambiente aerodinamico. Terzo, la crociera ad ala fissa dovrebbe essere sfruttata in qualsiasi configurazione fattibile per massimizzare il raggio e l'autonomia.

La valutazione di fattibilità per la configurazione ad ala fissa è riassunta in @tbl:fw-feasibility. Il confronto delle configurazioni e la motivazione della selezione sono presentate in @sec:architecture-selection.

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

## Metodologia del diagramma di matching {#sec:comparative-results}

Questa sezione presenta la metodologia del diagramma di matching (diagramma dei vincoli) per il dimensionamento preliminare dell'aeromobile e la applica per derivare i parametri del punto di progetto per l'UAV marziano. Il diagramma di matching visualizza tutti i vincoli di prestazioni simultaneamente, identificando lo spazio di progetto fattibile come l'intersezione di tutte le regioni accettabili [@roskamAirplaneDesign12005a].

### Riepilogo dei requisiti

Da @sec:user-needs e @sec:derived-requirements, l'UAV marziano deve soddisfare i seguenti requisiti chiave:

: Riepilogo dei requisiti di missione {#tbl:requirements-summary}

| ID | Requisito | Soglia | Motivazione |
|:---|:------------|:----------|:----------|
| OR-1 | Raggio operativo | ≥50 km | Superare la distanza totale di 35 km di Curiosity in un singolo volo |
| OR-4 | Autonomia di crociera | ≥60 min | Andata e ritorno + operazioni di rilevamento (42 min transito + 15 min rilevamento + 3 min hovering) |
| - | Capacità VTOL | Richiesta | Nessuna infrastruttura di pista su Marte |
| - | Capacità di carico | ≥0.5 kg | Payload camera + relè radio |
| N6 | Tolleranza ai guasti singoli | Richiesta | Sistema di missione senza capacità di abort |

### Fondamenti del diagramma di matching

#### Definizione degli assi

Asse orizzontale (Carico alare, $W/S$):

Il carico alare è definito come il peso dell'aeromobile per unità di superficie alare:

$$\frac{W}{S} \quad [\text{N/m}^2 \text{ o Pa}]$$

Un carico alare più alto implica una superficie alare più piccola per un dato peso, risultando in velocità di crociera e stallo più elevate, resistenza ridotta da una minore area bagnata, struttura alare più leggera, e maggiore sensibilità alle raffiche.

Asse verticale (Carico di potenza, $P/W$):

Il carico di potenza è definito come la potenza installata per unità di peso:

$$\frac{P}{W} \quad [\text{W/N o W/kg}]$$

Un carico di potenza più alto implica più potenza installata rispetto al peso, fornendo migliore velocità di salita, maggiore capacità di hovering (per configurazioni VTOL), maggiore capacità di accelerazione, e aumento della massa e del costo del sistema propulsivo.

#### Linee di vincolo

Ogni condizione di volo genera una linea di vincolo sul diagramma di matching. I punti sulla linea rappresentano il minimo $P/W$ (o massimo $W/S$) che soddisfa quel vincolo.

Vincolo di hovering (velivolo a rotore e VTOL ibrido):

Da @eq:hover-constraint in @sec:rotorcraft-analysis:

$$\left(\frac{P}{W}\right)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$

Questo vincolo è indipendente dal carico alare (il carico del disco $DL$ non dipende dalla superficie alare), apparendo come una linea orizzontale sul diagramma di matching. Tutti i punti sopra questa linea soddisfano il requisito di hovering.

Vincolo di crociera (ala fissa e VTOL ibrido):

Da @eq:cruise-electric-power in @sec:fixed-wing-analysis:

$$\left(\frac{P}{W}\right)_\text{crociera} = \frac{V}{(L/D) \times \eta_\text{crociera}}$$

Poiché $L/D$ dipende da $C_L$ (che varia con $W/S$ a velocità fissa), questo vincolo forma una curva con un minimo al carico alare ottimale. A $W/S$ molto basso, l'aeromobile opera ad alto $C_L$ con alta resistenza indotta; a $W/S$ molto alto, l'aeromobile deve volare più veloce, aumentando la potenza parassita. Il minimo si verifica vicino a $(L/D)_\text{max}$.

Vincolo di stallo:

Da @eq:wing-loading-constraint in @sec:fixed-wing-analysis:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

Questo vincolo stabilisce il carico alare massimo ammissibile e appare come una linea verticale sul diagramma di matching. Tutti i punti a sinistra di questa linea soddisfano il requisito di velocità minima.

Vincolo energetico (VTOL ibrido):

Il vincolo energetico da @sec:energy-constraint si manifesta come un confine della regione fattibile che accoppia il carico di potenza alla durata della missione. Un carico di potenza più alto (volo più veloce) generalmente riduce il tempo di missione ma può violare i vincoli energetici se la potenza di hovering è troppo alta.

La regione fattibile è l'intersezione di tutte le regioni accettabili: sopra il vincolo di hovering (per le configurazioni VTOL), sopra la curva del vincolo di crociera, a sinistra del vincolo di stallo, e soddisfacendo il vincolo energetico (verificato separatamente).

Il punto di progetto ottimale minimizza il carico di potenza all'interno della regione fattibile, poiché questo corrisponde a un sistema propulsivo più leggero e più efficiente. Tipicamente, il punto di progetto si trova all'intersezione di due o più vincoli attivi.

### Diagrammi di matching delle configurazioni

Prima di esaminare ogni configurazione individualmente, @fig:ld-comparison attraverso @fig:endurance-comparison presentano le metriche di prestazione chiave per tutte e tre le architetture candidate.

![Confronto dell'efficienza aerodinamica tra le configurazioni. L'L/D equivalente del velivolo a rotore di 4.0 è limitato dall'inefficienza del volo avanzato del rotore, mentre l'ala fissa raggiunge 11.7. Il VTOL ibrido raggiunge 10.5 a causa della penalità di resistenza dei rotori fermi.](figures/ld_comparison_it.png){#fig:ld-comparison width=80%}

![Confronto dei requisiti di potenza. La potenza di hovering (3178 W) è identica per velivolo a rotore e VTOL ibrido. La potenza di crociera varia con l'efficienza aerodinamica: velivolo a rotore 460 W, ala fissa 286 W, VTOL ibrido 318 W.](figures/power_comparison_it.png){#fig:power-comparison width=85%}

![Confronto dell'autonomia rispetto al requisito di 60 minuti (linea tratteggiata). Il velivolo a rotore non soddisfa marginalmente a 57 min. L'ala fissa raggiunge 151 min ma non può soddisfare il requisito VTOL. Il VTOL ibrido raggiunge 81 min con margine adeguato.](figures/endurance_comparison_it.png){#fig:endurance-comparison width=80%}

#### Analisi dei vincoli del velivolo a rotore

Per la configurazione a velivolo a rotore puro, gli assi del diagramma di matching devono essere adattati poiché non c'è ala. Il parametro rilevante è il carico del disco ($DL = T/A$) piuttosto che il carico alare. Il vincolo dominante è la potenza di hovering, che aumenta drammaticamente con il carico del disco nella rarefatta atmosfera marziana.

Lo spazio di progetto del velivolo a rotore è eliminato dalle prestazioni marginali di autonomia. Il bilancio energetico dominato dall'hovering (potenza di hovering 3178 W per 3 min consuma 158.9 Wh) lascia energia insufficiente per la crociera (459.7 W in volo avanzato). La configurazione raggiunge solo 57.27 minuti di autonomia, non soddisfacendo il requisito di 60 minuti con un margine del -4.5%.

#### Analisi dei vincoli dell'ala fissa

Per la configurazione ad ala fissa pura, il diagramma di matching mostra un vincolo di crociera come curva poco profonda con minimo al carico alare ottimale (circa 11.00 N/m² per le condizioni marziane), un vincolo di stallo come linea verticale a $W/S_\text{max}$ = 7.300 N/m² per $V_\text{min}$ = 30.00 m/s e $C_{L,\text{max}}$ = 1.200, e nessun vincolo di hovering (l'ala fissa non può effettuare hovering).

La regione fattibile esiste e offre eccellente efficienza di potenza (286.4 W in crociera a MTOW 10.00 kg). Tuttavia, questa regione è inaccessibile perché l'aeromobile non può decollare senza una pista. La distanza di corsa di decollo di circa 536 m assicura che nessun punto di progetto nella regione fattibile sia raggiungibile operativamente.

#### Analisi dei vincoli del VTOL ibrido

Per la configurazione QuadPlane, il diagramma di matching combina un vincolo di hovering come linea orizzontale a $P/W$ = 85.64 W/N (domina il diagramma), un vincolo di crociera come curva ben al di sotto del vincolo di hovering (potenza di crociera circa 10× inferiore), e un vincolo di stallo come linea verticale al carico alare massimo ammissibile (7.300 N/m²).

Il diagramma di matching per il QuadPlane traccia il carico di potenza $(P/W)$ rispetto al carico alare $(W/S)$.

Vincolo di hovering: Appare come una linea orizzontale, indipendente dal carico alare. La potenza di hovering richiesta dipende dal carico del disco e dalla densità atmosferica, non dalla dimensione dell'ala:

$$(P/W)_\text{hover} = \frac{1}{\eta_\text{hover}} \sqrt{\frac{DL}{2\rho}}$$ {#eq:hover-constraint-qp}

Vincolo di crociera: Appare come una curva con minimo al carico alare ottimale. A $W/S$ molto basso, la resistenza indotta è alta (alto $C_L$); a $W/S$ molto alto, l'aeromobile deve volare veloce per generare sufficiente portanza (alta $V$). Il minimo si verifica vicino a $(L/D)_\text{max}$.

Vincolo di stallo: Appare come una linea verticale al carico alare massimo ammissibile:

$$\left(\frac{W}{S}\right)_\text{max} = \frac{1}{2}\rho V_\text{min}^2 C_{L,\text{max}}$$ {#eq:stall-constraint}

Vincolo energetico: Si manifesta come un confine della regione fattibile che accoppia il carico di potenza alla durata della missione. Un carico di potenza più alto (volo più veloce) generalmente riduce il tempo di missione ma può violare i vincoli energetici se la potenza di hovering è troppo alta.

La regione fattibile si trova sopra la linea del vincolo di hovering, a sinistra del vincolo di stallo, con il vincolo energetico verificato (margine 29.7%).

Il punto di progetto è dominato dall'hovering. La potenza installata è determinata interamente dai requisiti di hovering; la potenza di crociera è abbondante. Il dimensionamento dell'ala è determinato dalle considerazioni di stallo ed efficienza aerodinamica, indipendente dalla potenza.

![Diagramma di matching (diagramma dei vincoli) per la configurazione VTOL ibrida. Il vincolo di hovering (linea rossa orizzontale) domina, stabilendo il carico di potenza minimo richiesto. Il vincolo di stallo (linea verde verticale) limita il carico alare massimo. Il vincolo di crociera (curva blu) è facilmente soddisfatto sotto la linea di hovering. Il punto di progetto (*) si trova all'intersezione dei vincoli di hovering e stallo.](figures/matching_chart_it.png){#fig:matching-chart width=90%}

### Determinazione del punto di progetto

Dall'analisi del diagramma di matching del VTOL ibrido (@fig:matching-chart), il punto di progetto del QuadPlane è caratterizzato da:

: Parametri del punto di progetto {#tbl:design-point}

| Parametro | Valore | Vincolo |
|:----------|------:|:-----------|
| Carico alare, $W/S$ | 7.300 N/m² | Fissato dal limite di stallo a $V_\text{min}$ = 30.00 m/s |
| Carico di potenza, $P/W$ | 85.64 W/N | Fissato dal requisito di hovering |
| Carico del disco, $DL$ | 30.00 N/m² | Compromesso tra dimensione del rotore e potenza |

Questi valori implicano i seguenti parametri derivati per MTOW = 10.00 kg ($W$ = 37.11 N):

: Parametri di progetto derivati {#tbl:design-parameters}

| Parametro derivato | Valore | Calcolo |
|:------------------|------:|:------------|
| Superficie alare | $S = W/(W/S) = 37.11/7.300$ | 5.083 m² |
| Apertura alare | $b = \sqrt{AR \times S}$ | 5.523 m (con AR = 6) |
| Corda media | $c = S/b$ | 0.9203 m |
| Potenza di hovering installata | $P = (P/W) \times W$ | 3178 W |
| Potenza di crociera installata | - | circa 318.5 W |

Questi valori preliminari saranno raffinati in @sec:design-decisions sulla base della selezione dettagliata dei componenti e dell'analisi dei compromessi. Il diagramma di matching fornisce punti di partenza per il progetto iterativo.

Il confronto delle configurazioni, l'eliminazione delle alternative, e la motivazione della selezione sono presentati in @sec:architecture-selection.

# Decisioni progettuali {#sec:design-decisions}

Questa sezione presenta le selezioni progettuali basate sull'analisi dei compromessi (@sec:reference-data) e sui risultati dei vincoli (@sec:constraint-analysis). Ogni decisione è giustificata dall'analisi condotta e tracciabile a requisiti specifici o obiettivi prestazionali.

## Selezione dell'architettura {#sec:architecture-selection}

Questa sezione consolida il confronto delle configurazioni dall'analisi dei vincoli (@sec:constraint-analysis), presenta la motivazione dell'eliminazione delle configurazioni alternative, e documenta l'architettura QuadPlane selezionata con le sue decisioni progettuali.

### Confronto delle configurazioni

#### Riepilogo quantitativo

@tbl:config-comparison sintetizza le analisi delle tre configurazioni candidate—velivolo a rotore (@sec:rotorcraft-analysis), ala fissa (@sec:fixed-wing-analysis), e VTOL ibrido (@sec:hybrid-vtol-analysis).

: Riepilogo del confronto delle configurazioni {#tbl:config-comparison}

| Criterio | Velivolo a rotore | Ala fissa | VTOL ibrido |
|:----------|:----------:|:----------:|:-----------:|
| **Efficienza aerodinamica** | | | |
| L/D o $(L/D)_\text{eff}$ | 4 | 15 | 13 |
| **Requisiti di potenza** | | | |
| P/W hovering (W/kg) | 246 | N.D. | 246 |
| P/W crociera (W/kg) | N.D. | 22.5 | 26 |
| Potenza di crociera (W) | 152$^a$ | 74 | 86 |
| **Capacità di missione** | | | |
| Autonomia (min) | 62 | 191 | 108 |
| Margine di autonomia | +3% | +218% | +80% |
| Raggio (km) | 142 | 459 | 252 |
| Margine di raggio | +42% | +359% | +152% |
| **Operatività** | | | |
| Capacità VTOL | ✓ Sì | ❌ No | ✓ Sì |
| Infrastruttura | Nessuna | circa 6 km pista | Nessuna |
| Capacità di planata | ❌ No | ✓ Sì | ✓ Sì$^b$ |
| **Budget di massa** | | | |
| Frazione propulsiva | circa 15% | circa 8% | circa 25% |
| Penalità di massa | N.D. | N.D. | +20% |
| **Conformità ai requisiti** | | | |
| Soddisfa autonomia | ✓ (appena) | ✓ | ✓ |
| Soddisfa raggio | ✓ | ✓ | ✓ |
| Soddisfa VTOL | ✓ | ❌ | ✓ |
| **RACCOMANDAZIONE** | ⚠️ Non raccomandato | ❌ Non fattibile | ✓ **SELEZIONATO** |

$^a$ Potenza di volo avanzato del velivolo a rotore per velocità di missione equivalente; la potenza di hovering è 812 W.
$^b$ Il QuadPlane può planare in modalità crociera se il motore di crociera si guasta, estendendo il tempo per l'atterraggio VTOL di emergenza.

#### Confronto dell'efficienza aerodinamica

: Confronto dell'efficienza aerodinamica {#tbl:aerodynamic-efficiency-comparison}

| Configurazione | Tipo L/D | Valore | Fonte |
|:--------------|:---------|------:|:-------|
| Velivolo a rotore | $(L/D)_\text{eff}$ | 4 | Analisi potenza volo avanzato (@sec:rotorcraft-analysis) |
| Ala fissa | $(L/D)$ | 15 | Polare di resistenza a $C_L$ ottimale (@sec:fixed-wing-analysis) |
| VTOL ibrido | $(L/D)$ | 13 | Crociera alare con penalità resistenza rotori (@sec:hybrid-vtol-analysis) |

Le configurazioni ad ala fissa e VTOL ibrido condividono un'efficienza di crociera simile perché il QuadPlane utilizza la portanza alare durante la crociera. La riduzione del 13% nell'L/D del QuadPlane (da 15 a 13) tiene conto della resistenza parassita dovuta ai rotori di sollevamento fermi e alla loro struttura di montaggio. Il velivolo a rotore, vincolato dal volo supportato dal rotore per l'intera missione, raggiunge solo $(L/D)_\text{eff} \approx 4$—circa un quarto dell'efficienza dell'ala fissa.

### Eliminazione delle alternative

#### Velivolo a rotore: NON RACCOMANDATO

La configurazione a velivolo a rotore puro è eliminata dalla considerazione per le seguenti ragioni:

* **Margine di sicurezza inadeguato:** Il margine di autonomia del 3% (62 min raggiunti vs 60 min richiesti) è inaccettabile per una missione senza capacità di abort. Qualsiasi deviazione dalle condizioni nominali—degradazione della batteria, variazione della densità atmosferica, inefficienza di navigazione—potrebbe comportare il fallimento della missione.

* **Alta sensibilità ai parametri:** Una riduzione del 10% della densità atmosferica (possibile durante le variazioni stagionali) aumenta i requisiti di potenza di circa il 5%, eliminando interamente il margine di autonomia.

* **Nessuna capacità di planata:** Se un rotore si guasta in volo avanzato, un multirotore non può planare per estendere il tempo per le procedure di emergenza. L'aeromobile precipita immediatamente, senza opzioni di recupero.

* **Nessun percorso di miglioramento:** A differenza delle prestazioni marginali dell'ala fissa che potrebbero essere migliorate con profili più avanzati, la limitazione del velivolo a rotore è fondamentale—$(L/D)_\text{eff} \approx 4$ è una conseguenza fisica del volo supportato dal rotore.

#### Ala fissa: NON FATTIBILE

La configurazione ad ala fissa pura è eliminata dalla considerazione perché **non può soddisfare il requisito VTOL**:

* **Requisito di pista:** La corsa di decollo è calcolata in 5-6 km, richiedendo un'infrastruttura di pista che non esiste su Marte.

* **Nessuna alternativa pratica:** Il lancio con catapulta, il decollo assistito da razzo (RATO) e il lancio con sgancio da pallone richiedono tutti un'infrastruttura sostanziale, materiali di consumo o intervento dell'equipaggio incompatibili con le operazioni autonome dall'habitat.

* **Atterraggio altrettanto problematico:** L'avvicinamento a circa 90 m/s con una corsa di atterraggio misurata in chilometri è incompatibile con terreno non preparato.

Nonostante dimostri un'efficienza aerodinamica superiore ($(L/D) = 15$) e prestazioni teoriche eccezionali (191 min di autonomia, 459 km di raggio), la configurazione ad ala fissa è **operativamente impossibile**.

### Selezione del VTOL ibrido (QuadPlane)

La configurazione VTOL ibrida è selezionata come base per l'UAV marziano perché è **l'unica architettura che soddisfa simultaneamente tutti i requisiti di missione**:

* **Capacità VTOL:** I rotori di sollevamento forniscono decollo e atterraggio verticale senza infrastruttura a terra (✓)

* **Margine di autonomia adeguato:** 108 minuti raggiunti vs 60 minuti richiesti (margine +80%) (✓)

* **Margine di raggio adeguato:** 252 km raggiunti vs 100 km richiesti (margine +152%) (✓)

* **Capacità in modalità degradata:** Se il motore di crociera si guasta, l'aeromobile può planare per estendere il tempo per l'atterraggio VTOL di emergenza, a differenza del velivolo a rotore puro che precipita immediatamente.

* **Fattibilità energetica:** 146 Wh richiesti vs 237 Wh disponibili (margine del 62% sopra il requisito).

La configurazione accetta una penalità di massa di circa il 20-25% dell'MTOW per il sistema di propulsione doppio. Questa penalità è giustificata perché:

1. Abilita la missione (nessuna alternativa per VTOL + crociera efficiente)
2. Fornisce margini di sicurezza sostanziali rispetto al velivolo a rotore
3. Mantiene opzioni di operazione in modalità degradata

### Riepilogo della configurazione

Dall'analisi del diagramma di matching (@sec:comparative-results), il punto di progetto del QuadPlane selezionato è caratterizzato da:

: Riepilogo del punto di progetto del QuadPlane {#tbl:quadplane-design-point}

| Parametro | Valore | Vincolo |
|:----------|------:|:-----------|
| Carico alare, $W/S$ | circa 17 N/m² | Tra limite di stallo e L/D ottimale |
| Carico di potenza, $P/W$ | circa 246 W/kg | Fissato dal requisito di hovering |
| Carico del disco, $DL$ | circa 30 N/m² | Compromesso tra dimensione rotore e potenza |
| MTOW | 3.3 kg | Base da @sec:initial-mass-estimate |
| Superficie alare | circa 0.72 m² | $S = W/(W/S)$ |
| Apertura alare | circa 2.9 m | $b = \sqrt{AR \times S}$ con AR = 12 |

### Motivazione della configurazione QuadPlane

L'architettura QuadPlane è selezionata per l'UAV marziano in base ai requisiti di missione e ai vincoli operativi.

#### Compatibilità con la missione

I doppi obiettivi di missione, mappatura e relè di telecomunicazione, richiedono un tempo di volo esteso su grandi aree. La crociera ad ala fissa fornisce il raggio e l'autonomia necessari, mentre la capacità VTOL consente operazioni da un sito habitat non preparato. L'architettura QuadPlane affronta direttamente entrambi i requisiti.

#### Tolleranza ai guasti

Per un UAV marziano dove la riparazione in volo è impossibile, la tolleranza ai guasti singoli è essenziale. Una configurazione di sollevamento octocopter (otto motori in quattro coppie coassiali) fornisce questa capacità: l'UAV può completare un atterraggio controllato con qualsiasi singolo motore guasto. Ogni coppia coassiale condivide un supporto strutturale, con rotori superiori e inferiori controrotanti per annullare la coppia.

Per estendere la tolleranza ai guasti singoli alla fase di crociera, viene selezionata una configurazione trattrice coassiale controrotante. Due eliche di crociera sono montate coassialmente a prua della fusoliera, azionate da motori indipendenti e rotanti in direzioni opposte. Ogni motore è dimensionato per fornire il 60% della spinta nominale di crociera, assicurando che il guasto di uno dei motori di crociera consenta alla missione di continuare con prestazioni ridotte piuttosto che richiedere un abort immediato. Il margine di spinta totale del 20% tiene conto della resistenza aggiuntiva dovuta all'elica guasta in moto libero.

Questa configurazione coassiale a prua offre diversi vantaggi rispetto alle alternative come i propulsori posteriori o le eliche wing-mounted affiancate [@roskamAirplaneDesign22004]:

* Flusso d'aria pulito: le eliche trattrici operano nell'aria indisturbata davanti alla fusoliera, portando a un'efficienza propulsiva più alta rispetto alle configurazioni a spinta dove l'elica incontra la scia turbolenta dall'intelaiatura. Questo vantaggio di efficienza è ben documentato nella letteratura di progettazione aeronautica, con le eliche a spinta che tipicamente subiscono perdite di efficienza del 2-15% a causa dell'ingestione della scia.
* Annullamento della coppia: le eliche controrotanti annullano la coppia reattiva, eliminando i momenti di imbardata asimmetrici durante la crociera e migliorando la stabilità direzionale. Questo è particolarmente vantaggioso per un veicolo che opera autonomamente senza correzione del pilota.
* Ingombro compatto: una disposizione coassiale concentra entrambe le eliche lungo l'asse della fusoliera, mantenendo un profilo aerodinamico e evitando l'interferenza aerodinamica e la complessità strutturale delle eliche wing-mounted affiancate.

Un compromesso di questa configurazione trattrice è che le camere rivolte in avanti sono ostruite dalle eliche. Per la missione di mappatura, la camera payload primaria è rivolta al nadir (verso il basso), che rimane non ostruita. I sensori di navigazione che richiedono visibilità in avanti possono essere montati sul bordo d'attacco dell'ala o utilizzare orientamenti rivolti all'indietro.

L'architettura propulsiva risultante comprende 10 motori in totale: otto motori di sollevamento in quattro coppie coassiali più due motori di crociera coassiali a prua. Questa configurazione raggiunge la piena tolleranza ai guasti singoli in tutte le fasi di volo senza fare affidamento sulla ridondanza incrociata tra sistemi (cioè, utilizzando i motori di sollevamento per il ritorno in crociera), che limiterebbe gravemente il raggio operativo a causa della minore efficienza del volo avanzato del multirotore.

#### Semplicità operativa

Rispetto ad altri approcci VTOL (tilt-rotor, tilt-wing, tail-sitter), il QuadPlane offre diversi vantaggi. La configurazione non richiede attuatori di inclinazione o componenti a geometria variabile, risultando in meccanismi più semplici con meno modalità di guasto. Hovering e crociera utilizzano sistemi propulsivi separati, disaccoppiando le modalità di volo e semplificando la progettazione del sistema di controllo. L'architettura beneficia di un'ampia heritage commerciale di volo con supporto maturo dell'autopilota, riducendo il rischio di sviluppo. Infine, i componenti sono accessibili e modulari, consentendo una manutenzione più facile. Questi fattori migliorano l'affidabilità nell'ambiente marziano dove la capacità di manutenzione è severamente limitata.

### Selezione della configurazione della coda

Sulla base dell'analisi dei compromessi, viene selezionata una configurazione a V invertita montata su boom. Questa scelta sfrutta i boom strutturali già richiesti per i motori di sollevamento dell'octocopter.

I boom dei motori di sollevamento posteriori si estendono verso poppa per supportare le superfici di coda, eliminando la necessità di una struttura di boom di coda separata e riducendo la massa strutturale complessiva. La configurazione montata su boom fornisce un braccio di momento più lungo di quello che consentirebbe una coda montata sulla fusoliera con la fusoliera compatta selezionata per questo progetto, compensando la ridotta efficacia di controllo ai numeri di Reynolds marziani. La geometria a V invertita inclina le superfici verso l'alto rispetto all'asse della fusoliera, fornendo spazio dalla superficie durante l'atterraggio su terreno irregolare. Inoltre, le superfici della coda a V sono posizionate al di fuori del getto dell'elica di crociera (configurazione trattrice a prua), assicurando un flusso d'aria indisturbato sulle superfici di controllo.

La disposizione a V invertita combina il controllo di beccheggio e imbardata in due superfici con miscelazione in stile ruddervator. Studi CFD sulle configurazioni di impennaggio montato su boom hanno trovato che i design a U invertita su boom fornivano stabilità longitudinale superiore e caratteristiche di stallo per missioni di sorveglianza [@nugrohoPerformanceAnalysisEmpennage2022], e il design a due superfici riduce il conteggio dei pezzi rispetto a una coda convenzionale a tre superfici.

Il dimensionamento delle superfici di coda per le condizioni marziane è affrontato in @sec:geometry-selection, dove i coefficienti di volume di coda e gli effetti del numero di Reynolds sono quantificati.

### Selezione della geometria della fusoliera

I benchmark commerciali mostrano un rapporto lunghezza-apertura alare che varia da 0.28 a 0.63, con una mediana di circa 0.50 (@tbl:reference-fuselage). Tuttavia, la scalatura diretta di questo rapporto alle condizioni marziane produrrebbe una fusoliera impraticabilmente grande: con l'apertura alare di 6 m richiesta per il volo marziano (derivata in @sec:geometry-selection), un rapporto di 0.50 produrrebbe una fusoliera di 3 m, che supera di gran lunga i requisiti di volume interno per un UAV da 12 kg.

Questa discrepanza nasce perché la dimensione della fusoliera è guidata principalmente dai requisiti di volume interno (batterie, payload, avionica), che non scalano con la densità atmosferica, mentre l'apertura alare è guidata dai requisiti di portanza, che scalano significativamente con la rarefatta atmosfera marziana. L'approccio corretto dimensiona la fusoliera sulla base dei requisiti funzionali piuttosto che della scalatura del rapporto.

L'MTOW target di 12 kg richiede alloggiamento per i payload (sistemi camera e radio) più le batterie; questi componenti richiedono circa 4-5 L di volume interno con margini per il routing e la gestione termica. Una lunghezza della fusoliera di 1.5-2.0 m fornisce un volume interno adeguato mantenendo un profilo aerodinamico con rapporto di finezza di 5-7 [@gottenFullConfigurationDrag2021]. Questo risulta in un rapporto lunghezza-apertura alare di circa 0.25-0.30, inferiore ai benchmark commerciali ma coerente con i vincoli di scalatura specifici per Marte.

La lunghezza della fusoliera selezionata fornisce un braccio di momento adeguato per le superfici di coda montate su boom quando combinata con i boom strutturali che si estendono verso poppa, raggiungendo la stabilità longitudinale e direzionale richiesta senza un'area eccessiva delle superfici di coda.

La sezione trasversale della fusoliera e il dimensionamento dettagliato sono affrontati in @sec:geometry-selection.

### Selezione dei materiali

Il polimero rinforzato con fibra di carbonio (CFRP) è selezionato come materiale strutturale primario, coerentemente con l'heritage di Ingenuity e la pratica commerciale.

Il CFRP presenta bassa espansione termica (CTE circa 0.5 ppm/°C), minimizzando le sollecitazioni termiche dal ciclo di temperatura diurno da −80°C a +20°C su Marte. Fornisce il più alto rapporto resistenza-peso tra i materiali strutturali comunemente disponibili, supportando la minimizzazione della massa critica per il volo marziano. L'elicottero Ingenuity ha dimostrato con successo la costruzione in CFRP su Marte, utilizzando tessuti in carbonio a tow distribuito TeXtreme® selezionati per la resistenza alle microfessurazioni da ciclo termico [@latourabOxeonPartOwnedHoldings2025].

Le pelli dell'ala e della fusoliera utilizzeranno una costruzione sandwich con nucleo in schiuma e facce in fibra di carbonio, fornendo alta rigidezza-peso per le superfici aerodinamiche primarie. I boom dei motori di sollevamento e del supporto della coda saranno tubi in fibra di carbonio, avvolti a filamento o pultrusi. Il rinforzo in fibra di vetro sarà utilizzato nei punti di attacco del carrello di atterraggio e sui bordi d'attacco vulnerabili per la tolleranza agli impatti. La gestione termica interna utilizzerà superfici interne placcate in oro o isolamento multistrato per il controllo termico del compartimento elettronica, seguendo la pratica di Ingenuity.

Le implicazioni della selezione dei materiali per la frazione di massa strutturale sono affrontate in @sec:material-selection.

![Concetto proposto di QuadPlane con configurazione di sollevamento octocopter ed eliche di crociera trattrici coassiali.](figures/our_proposal_concept.jpg){#fig:concept-architecture width=70%}

## Selezione del profilo alare {#sec:airfoil-selection}

<!-- PLACEHOLDER: Logica di selezione da estrarre dall'analisi -->

Sulla base dei dati sulle prestazioni del profilo alare in @sec:aerodynamic-analysis, questa sezione presenta la motivazione della selezione del profilo alare per il progetto dell'ala dell'UAV marziano.

## Selezione della geometria {#sec:geometry-selection}

Questa sezione presenta il dimensionamento geometrico dettagliato per la configurazione QuadPlane selezionata, derivando i parametri alari, della fusoliera e dell'impennaggio dai risultati dell'analisi dei vincoli.

(Contenuto in corso di lavorazione...)

## Selezione dei materiali {#sec:material-selection}

Questa sezione presenta la selezione dettagliata dei materiali per la configurazione QuadPlane, basata sull'analisi dei compromessi in @sec:materials-data e sull'heritage di Ingenuity.

(Contenuto in corso di lavorazione...)

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

# Selezione dei componenti e verifica {#sec:component-verification}

Questa sezione presenta la selezione dei componenti specifici basata sui risultati del dimensionamento, seguita dalla verifica che il progetto assemblato soddisfi tutti i requisiti. La ripartizione della massa e il bilancio di potenza sono aggiornati con i dati effettivi dei componenti.

# Requisiti infrastrutturali

Questa sezione definisce l'infrastruttura di terra richiesta per supportare le operazioni dell'UAV dall'habitat con equipaggio, incluse le specifiche dell'hangar e il concetto operativo.

## Hangar dell'habitat {#sec:habitat-hangar}

(Contenuto in corso di lavorazione...)

## Concetto operativo {#sec:operations-concept}

(Contenuto in corso di lavorazione...)

# Conclusioni e raccomandazioni

*[Questa sezione riassumerà i risultati dello studio di fattibilità e fornirà raccomandazioni. Contenuto da aggiornare una volta finalizzato il progetto.]*

Risultati chiave:

* L'architettura ibrida QuadPlane fornisce un compromesso efficace tra capacità VTOL e efficienza di crociera
* Gli effetti a basso numero di Reynolds impattano significativamente il progetto aerodinamico; il profilo E387 offre buone prestazioni a Re = 50,000-90,000
* La potenza di hovering domina il dimensionamento dei motori; la potenza di crociera ad ala fissa è sostanzialmente inferiore alla potenza di hovering
* L'attuale tecnologia delle batterie (150 Wh/kg) consente durate di missione pratiche

Raccomandazioni:

1. **Sviluppo tecnologico**: Prioritizzare il miglioramento dell'energia specifica delle batterie (>200 Wh/kg) per significativi guadagni prestazionali
2. **Validazione dei profili**: I test in galleria del vento dei profili selezionati ai numeri di Reynolds rappresentativi di Marte sono giustificati
3. **Progetto termico**: È richiesta un'analisi termica dettagliata per l'estremo intervallo di temperatura diurna marziana
4. **Mitigazione della polvere**: Gli effetti della contaminazione superficiale sulle prestazioni del rotore richiedono indagine

Il concetto di UAV marziano è tecnicamente fattibile con la tecnologia attuale o a breve termine.

# Riferimenti

# Appendice A: Costanti fisiche e parametri

(Contenuto in corso di lavorazione...)

# Appendice B: Schede tecniche dei componenti

(Contenuto in corso di lavorazione...)

# Appendice C: Documentazione degli script di dimensionamento

(Contenuto in corso di lavorazione...)

# Appendice D: Derivazione del modello atmosferico

(Contenuto in corso di lavorazione...)

# Esempio di utilizzo

(Contenuto in corso di lavorazione...)