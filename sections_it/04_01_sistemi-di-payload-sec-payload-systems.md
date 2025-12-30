# Dati di riferimento e analisi dei compromessi

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
