# Requisiti infrastrutturali

## Hangar dell'habitat {#sec:habitat-hangar}

L'UAV richiede strutture di stoccaggio e manutenzione protette integrate con l'habitat marziano. Il progetto dell'hangar tiene conto della configurazione QuadPlane specificata in @sec:geometry-selection. La @fig:hangar-schematic illustra l'architettura dell'hangar a tre zone.

![Schema della struttura hangar UAV che mostra la baia di stoccaggio pressurizzata, la zona di transizione dell'airlock e la piattaforma esterna di lancio](figures/hangar_schematic.png){#fig:hangar-schematic}

### Ingombro dimensionale dell'UAV

Le dimensioni dell'hangar sono determinate dalla geometria dell'UAV derivata in @sec:geometry-selection:

: Ingombro dimensionale UAV per il dimensionamento hangar {#tbl:uav-envelope}

| Parametro | Simbolo | Valore | Fonte |
|:----------|:-------:|-------:|:------|
| Apertura alare | $b$ | 4.01 m | @tbl:wing-geometry |
| Lunghezza fusoliera | $L_f$ | 1.20 m | @tbl:fuselage-geometry |
| Diametro fusoliera | $D_f$ | 0.20 m | @tbl:fuselage-geometry |
| Altezza (con carrello) | $H$ | 0.50 m | @tbl:fuselage-geometry |
| Estensione trave poppiera | $\Delta L$ | 1.05 m | @tbl:total-length |
| Lunghezza totale aeromobile | $L_\text{totale}$ | 2.25 m | @tbl:total-length |
| Diametro elica di sollevamento | $D_p$ | 0.36 m | @sec:propeller-sizing |
| Diametro elica di crociera | $D_{p,c}$ | 0.31 m | @sec:propeller-sizing |

L'ingombro UAV per lo stoccaggio è **4.01 × 2.25 m** (apertura alare × lunghezza totale). I rotori di sollevamento sono montati su bracci alari all'interno dell'apertura alare. L'estensione della trave oltre la fusoliera sostiene le superfici del V-tail e fornisce il braccio del momento richiesto.

### Zone dell'hangar

L'hangar comprende tre zone funzionali secondo l'architettura standard degli airlock degli habitat marziani.

#### Baia di manutenzione pressurizzata (zona di stoccaggio)

La baia pressurizzata fornisce un ambiente in maniche di camicia per la manutenzione ed è dimensionata per ospitare l'intera apertura alare dell'UAV più l'area di lavoro:

: Specifiche baia pressurizzata {#tbl:pressurised-bay}

| Parametro | Valore | Note |
|:----------|-------:|:-----|
| Dimensioni interne | 6 × 5 × 3 m | Apertura alare completa (4.01 m) + 2 m margine × lunghezza totale (2.25 m) + area lavoro |
| Atmosfera | Equivalente habitat | O₂/N₂ a circa 70 kPa |
| Temperatura | +15 a +25 °C | Intervallo sicuro per batterie |
| Illuminazione | 500 lux | Operazioni di manutenzione |

#### Airlock (zona di transizione)

L'airlock consente le transizioni di pressione e la rimozione della polvere. La larghezza corrisponde alla baia di stoccaggio per ospitare l'UAV senza piegatura delle ali:

: Specifiche airlock {#tbl:airlock-specs}

| Parametro | Valore | Note |
|:----------|-------:|:-----|
| Dimensioni interne | 6 × 3 × 2.5 m | 6 m di larghezza ospita l'apertura alare completa |
| Tempo ciclo (depressurizzazione) | 5 min | Alla pressione ambiente marziana |
| Tempo ciclo (ripressurizzazione) | 5 min | Alla pressione dell'habitat |
| Rimozione polvere | Getti d'aria pressurizzata | CO₂ compressa dalle riserve dell'habitat |

La rimozione della polvere è effettuata tramite getti d'aria pressurizzata. Come descritto in @sec:introduction, la fine regolite marziana si accumula sulle superfici esposte e degrada i componenti meccanici e ottici. L'airlock impiega una serie di ugelli che dirigono gas compresso ad alta velocità (CO₂ dal trattamento atmosferico dell'habitat) sulle superfici dell'UAV, rimuovendo le particelle prima che il veicolo entri nella baia pressurizzata. Questo sistema è più semplice e affidabile dei precipitatori elettrostatici, non richiede consumabili oltre al gas compresso (che può essere riciclato) e non ha parti mobili esposte alla polvere marziana abrasiva.

#### Piattaforma esterna (zona di lancio/recupero)

La piattaforma esterna fornisce un'area libera per le operazioni VTOL:

: Specifiche piattaforma esterna {#tbl:platform-specs}

| Parametro | Valore | Note |
|:----------|-------:|:-----|
| Dimensioni piattaforma | 10 × 10 m | 2.5× la distanza dell'apertura alare |
| Superficie | Regolite stabilizzata | Rivestimento antipolvere |
| Marcatori atterraggio | Array LED | Basso consumo, tolleranti al freddo |

### Infrastruttura di ricarica

Il sistema di ricarica è dimensionato sulla base delle specifiche della batteria da @sec:energy-storage:

**Parametri batteria:**

* Capacità totale batteria: 945 Wh
* Energia da ripristinare (da 20% a 100% di carica): 756 Wh
* Tempo di ricarica obiettivo: 2–3 ore
* Potenza caricatore a rate 0.5C: 472 W
* Potenza caricatore a rate 1C: 945 W

È specificato un **caricatore da 1000 W** per consentire un rapido turnaround con margine.

### Sistema di alimentazione solare

Il sistema di alimentazione solare fornisce energia per la ricarica dell'UAV indipendentemente dall'alimentazione dell'habitat. Questa sezione presenta l'analisi dell'irraggiamento solare, la selezione delle celle, il dimensionamento dei pannelli e il dimensionamento della batteria tampone.

#### Irraggiamento solare su Marte

L'energia solare disponibile su Marte differisce significativamente dalla Terra a causa della distanza orbitale e degli effetti atmosferici:

: Parametri di irraggiamento solare marziano {#tbl:mars-irradiance}

| Parametro | Valore | Note |
|:----------|-------:|:-----|
| Costante solare all'orbita di Marte | 589 W/m² | 43% dei 1361 W/m² terrestri |
| Irraggiamento al perielio | 717 W/m² | Massimo avvicinamento al Sole |
| Irraggiamento all'afelio | 493 W/m² | Massima distanza dal Sole |
| Irraggiamento superficiale cielo sereno (mezzogiorno) | 500 W/m² | Attenuazione atmosferica inclusa |
| Ore di luce efficaci | 6 h/sol | Luce diurna utilizzabile per generazione |
| Fattore di incidenza medio | 0.7 | Perdite per coseno per pannelli a inclinazione fissa |

L'atmosfera marziana, sebbene sottile (circa 1% della pressione terrestre), attenua la radiazione solare attraverso l'assorbimento da parte del CO₂ e la diffusione da parte della polvere sospesa. In Arcadia Planitia alla latitudine operativa, l'irraggiamento medio annuale è circa 130 W/m². Tuttavia, per il dimensionamento dei pannelli, il progetto utilizza l'irraggiamento a mezzogiorno con cielo sereno di 500 W/m² come valore di picco, ridotto dal fattore di incidenza medio per i calcoli dell'energia giornaliera.

#### Selezione delle celle solari

Celle solari spaziali a tripla giunzione sono valutate per il sistema di ricarica integrato nell'habitat. Vengono confrontate tre tecnologie candidate:

: Confronto tecnologie celle solari {#tbl:solar-cell-comparison}

| Tecnologia | Efficienza (BOL) | Massa (mg/cm²) | Heritage |
|:-----------|:----------------:|:--------------:|:---------|
| SolAero IMM-α | 33.0% | 49 | Elicottero Marziano Ingenuity |
| Spectrolab XTJ Prime | 30.7% | 50–84 | Satelliti LEO/GEO |
| Azur Space 3G30C | 30.0% | 86 | MER Spirit/Opportunity |

**SolAero IMM-α** [@solaerotechnologiesrocketlabSolAeroIMMalphaInverted2024]<!-- #specs -->: Questa cella multi-giunzione metamorfica invertita (IMM) raggiunge la massima efficienza al 33% BOL. A 49 mg/cm² (0.49 kg/m²), è il 42% più leggera delle celle spaziali convenzionali. L'IMM-α ha heritage diretto su Marte, alimentando il pannello solare dell'elicottero Ingenuity attraverso oltre 70 voli.

**Spectrolab XTJ Prime** [@spectrolabboeingSpectrolabXTJPrime2023]<!-- #specs -->: Questa cella a tripla giunzione GaInP/GaAs/Ge raggiunge un'efficienza media del 30.7% (31.9% massimo dimostrato). La massa varia da 50–84 mg/cm² a seconda dello spessore (80–225 μm). Qualificata secondo gli standard AIAA-S111 e AIAA-S112 con ampio heritage di volo LEO e GEO.

**Azur Space 3G30C-Advanced** [@azurspacesolarpowerAzurSpace3G30CAdvanced2023]<!-- #specs -->: Questa cella InGaP/GaAs/Ge con efficienza del 30% su substrato di germanio ha una massa di 86 mg/cm² a 150 μm di spessore. Qualificata secondo ECSS-E-ST-20-08C con heritage sui Mars Exploration Rovers Spirit e Opportunity.

**Selezione: SolAero IMM-α** è selezionata sulla base di:

* Massima efficienza (33%) massimizza la potenza per unità di area
* Minima massa per area (49 mg/cm² = 0.49 kg/m²)
* Heritage marziano comprovato sull'elicottero Ingenuity
* Ottimizzata per lo spettro marziano per prestazioni ottimali

#### Dimensionamento dei pannelli

**Potenza in uscita per unità di area:**

$$P_\text{picco} = \eta_\text{cella} \times I_\text{superficie} = 0.33 \times 500 = 165 \text{ W/m}^2$$

**Resa energetica giornaliera:**

$$E_\text{pannello} = P_\text{picco} \times t_\text{sole} \times \cos\theta_\text{medio} = 165 \times 6 \times 0.7 = 693 \text{ Wh/m}^2/\text{sol}$$

**Fabbisogno energetico per ciclo di ricarica:**

$$E_\text{ricarica} = \frac{756 \text{ Wh}}{0.90} = 840 \text{ Wh}$$ (inclusa l'efficienza del caricatore)

**Area pannello richiesta:**

$$A_\text{pannello} = \frac{E_\text{ricarica}}{E_\text{pannello}} = \frac{840}{693} = 1.21 \text{ m}^2$$

**Margine di progetto (×1.5 per polvere e degradazione):**

$$A_\text{progetto} = 1.21 \times 1.5 = 1.82 \text{ m}^2 \approx 2.0 \text{ m}^2$$

#### Accumulo con batteria tampone

Il pannello solare genera energia solo durante le ore diurne, mentre la ricarica dell'UAV può essere richiesta in qualsiasi momento (incluso il turnaround notturno o dopo missioni serali). Una batteria tampone immagazzina l'energia solare per la ricarica su richiesta.

**Dimensionamento batteria tampone:**

: Dimensionamento batteria tampone {#tbl:buffer-battery}

| Parametro | Valore | Calcolo |
|:----------|-------:|:--------|
| Capacità batteria UAV | 945 Wh | @sec:energy-storage |
| Energia per ciclo di ricarica | 756 Wh | 80% profondità di scarica |
| Efficienza caricatore | 90% | |
| Energia richiesta dal tampone | 840 Wh | 756 / 0.90 |
| Fattore riserva notturna | 1.5 | Una ricarica notturna + margine |
| Capacità batteria tampone | 1260 Wh | 840 × 1.5 |
| Massa batteria tampone (180 Wh/kg) | 7.0 kg | Celle Li-ion |

La batteria tampone da 1260 Wh consente una ricarica completa dell'UAV durante la notte o in condizioni di tempesta di polvere quando non è disponibile input solare. Il fattore di 1.5 fornisce margine per il degrado della batteria e le perdite di sistema. Durante tempeste di polvere prolungate (settimane o mesi), la ricarica ricade sull'alimentazione nucleare dell'habitat.

**Ciclo di carica/scarica del tampone:**

Durante un tipico sol:

1. **Giorno (6 h efficaci)**: I pannelli solari generano 1386 Wh (2.0 m² × 693 Wh/m²)
2. **Ricarica tampone**: 1260 Wh immagazzinati nella batteria tampone
3. **Ricarica UAV (2–3 h)**: 840 Wh forniti alla batteria UAV (756 Wh immagazzinati dopo le perdite)
4. **Energia in eccesso**: Circa 126 Wh restituiti alla rete dell'habitat

: Specifiche sistema di alimentazione solare {#tbl:solar-spec}

| Parametro | Valore | Unità |
|:----------|-------:|:------|
| Tecnologia celle | SolAero IMM-α | - |
| Efficienza celle | 33 | % |
| Area pannello | 2.0 | m² |
| Potenza di picco | 330 | W |
| Resa energetica giornaliera | 1386 | Wh/sol |
| Massa pannello | 1.0 | kg |
| Capacità batteria tampone | 1260 | Wh |
| Massa batteria tampone | 7.0 | kg |
| Montaggio | Tetto habitat, inclinazione fissa | - |

### Riepilogo

L'infrastruttura dell'hangar consente un ciclo di ricarica completo dell'UAV per sol in condizioni di cielo sereno. L'array solare da 2.0 m² con batteria tampone da 1260 Wh fornisce indipendenza energetica per le operazioni quotidiane. Il sistema di getti d'aria pressurizzata nell'airlock rimuove la polvere marziana prima che l'UAV entri nella baia di manutenzione. La larghezza dell'airlock di 6 m ospita l'intera apertura alare di 4.01 m senza richiedere meccanismi di piegatura delle ali. Durante le condizioni di tempesta di polvere, la ricarica ricade sull'alimentazione nucleare dell'habitat o viene differita fino al miglioramento delle condizioni.

