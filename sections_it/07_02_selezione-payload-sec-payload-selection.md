# Selezione dei componenti e verifica

## Selezione del payload {#sec:payload-selection}

La selezione del payload segue dalla survey dei sistemi camera e radio presentata in @sec:payload-systems. I criteri di selezione danno priorità all'efficienza di massa, alla tolleranza ambientale per le condizioni marziane e alla capacità di missione.

### Selezione della camera {#sec:camera-selection}

#### Requisiti

La missione di mappatura richiede una camera capace di imaging ad alta risoluzione dall'altitudine di crociera (circa 100 m AGL). In base al budget di massa da @tbl:design-mass-fractions, l'allocazione totale del payload è:

$$m_\text{payload} = f_\text{payload} \times MTOW = 0.10 \times 10.00 = 1.00 \text{ kg}$$

Allocando circa il 60% alla camera e il 40% al sistema radio si ottiene un target di massa camera di circa 600 g.

#### Valutazione dei candidati

@Tbl:camera-selection presenta i candidati camera da @sec:camera-survey, valutati rispetto ai requisiti di missione.

: Analisi trade-off selezione camera {#tbl:camera-selection}

| Camera | Massa (g) | Risoluzione | Temp. (°C) | Valutazione |
|:-------|:--------:|:-----------|:----------------:|:------:|
| Ricoh GR III | 227-257 | 24 MP (APS-C) | N.D. | Selezionata |
| MicaSense RedEdge-MX | 232 | 1.2 MP/banda (5 bande) | N.D. | Alternativa |
| DJI Zenmuse P1 | 800-1350 | 45 MP (Full frame) | −20 a +50 | Riserva |
| Phase One iXM-100 | 630-1170 | 100 MP (Medio formato) | −10 a +40 | Respinta |
| DJI Zenmuse H20T | 828 | 640×512 (termico) | −20 a +50 | Respinta |

Nota: N.D. indica temperatura operativa non specificata dal produttore.

#### Motivazione della selezione

La **Ricoh GR III** è selezionata come camera primaria in base a:

* **Massa**: 227 g corpo, 257 g completa con batteria [@ricohimagingRicohGRIII2024]<!-- #specs -->, l'opzione RGB più leggera
* **Risoluzione**: sensore APS-C da 24 MP fornisce risoluzione adeguata per la mappatura
* **Dimensioni**: form factor compatto 109.4 × 61.9 × 33.2 mm [@ricohimagingRicohGRIII2024]<!-- #specs -->
* **Obiettivo**: obiettivo integrato da 18.3 mm (equivalente 28 mm) elimina la complessità degli obiettivi intercambiabili

La **MicaSense RedEdge-MX** è mantenuta come alternativa se è richiesta capacità multispettrale per l'analisi geologica [@micasenseMicaSenseRedEdgeMXIntegration2020]<!-- #specs -->. A 232 g, fornisce imaging a cinque bande (blu, verde, rosso, red-edge, NIR) adatto per l'identificazione minerale.

Le DJI Zenmuse P1 e Phase One iXM-100 sono respinte per massa superiore al target di 600 g di un fattore due o più. Il sistema termico DJI Zenmuse H20T è respinto poiché l'imaging termico non è un requisito di missione primario.

#### Requisito di gestione termica

La Ricoh GR III non specifica un intervallo di temperatura operativa, indicando tolleranza termica consumer-grade [@ricohimagingRicohGRIII2024]<!-- #specs -->. Le temperature superficiali marziane variano da circa −60 a +20 °C, richiedendo gestione termica attiva per mantenere la camera entro i limiti operativi. La massa del sistema di controllo termico è allocata nella frazione di massa avionica.

#### Specifiche selezionate

: Specifiche camera selezionata (Ricoh GR III) {#tbl:camera-spec}

| Parametro | Valore | Unità |
|:----------|------:|:-----|
| Modello | Ricoh GR III | - |
| Massa (corpo) | 227 | g |
| Massa (con batteria, SD) | 257 | g |
| Sensore | APS-C CMOS | - |
| Risoluzione | 24.24 | MP |
| Dimensioni immagine | 6000 × 4000 | pixel |
| Lunghezza focale | 18.3 | mm |
| Apertura | f/2.8-f/16 | - |
| Dimensioni | 109.4 × 61.9 × 33.2 | mm |

### Selezione della radio {#sec:radio-selection}

#### Requisiti

La missione di relay telecomunicazioni richiede un sistema radio capace di estendere la portata di comunicazione tra gli astronauti EVA in superficie e la stazione base dell'habitat. In base all'allocazione radio del 40% dal budget payload di 1.00 kg, il target di massa radio è circa 400 g.

I requisiti operativi includono:

* Portata: corrispondere o superare il raggio operativo di 50 km
* Temperatura: operazione alle temperature superficiali marziane (−60 a +20 °C)
* Potenza: minimizzare il consumo energetico per l'autonomia della batteria

#### Valutazione dei candidati

@Tbl:radio-selection presenta i candidati radio da @sec:radio-survey, valutati rispetto ai requisiti di missione.

: Analisi trade-off selezione radio {#tbl:radio-selection}

| Radio | Massa (g) | Portata (km) | Temp. (°C) | Valutazione |
|:------|:--------:|:----------:|:----------------:|:------:|
| RFD900x | 14.5 | > 40 | −40 a +85 | Selezionata |
| Microhard pMDDL2450 (chiuso) | 165 | N.D. | −40 a +85 | Alternativa |
| Rajant BreadCrumb ES1 | 455 | N.D. | −40 a +60 | Respinta |
| Silvus StreamCaster 4200E+ | 425 | N.D. | −40 a +85 | Respinta |
| Persistent Systems MPU5 | 391-726 | 209 | −40 a +85 | Respinta |

#### Motivazione della selezione

La **RFD900x** è selezionata come radio primaria in base a:

* **Massa**: 14.5 g è l'opzione più leggera, ben sotto il target di 400 g [@rfdesignRFD900xModemSpecifications2024]<!-- #specs -->
* **Portata**: >40 km in linea di vista soddisfa il raggio operativo di 50 km con ottimizzazione antenna [@rfdesignRFD900xModemSpecifications2024]<!-- #specs -->
* **Temperatura**: intervallo operativo da −40 a +85 °C supera i requisiti della superficie marziana
* **Potenza**: 5 W di consumo massimo a 1 W di trasmissione
* **Heritage**: ampiamente usata in applicazioni UAV con firmware open-source SiK

La **Microhard pMDDL2450** è mantenuta come alternativa se è richiesto throughput dati maggiore (25 Mbps vs 0.75 Mbps) per potenziali applicazioni di video relay [@microhardPMDDL2450MiniatureMIMO2025]<!-- #specs -->.

I sistemi radio mesh (Rajant, Silvus, Persistent Systems) sono respinti poiché la funzionalità mesh non è richiesta per una missione relay con singolo UAV. La loro massa di 400-700 g consumerebbe l'intero budget radio senza vantaggio per il profilo di missione.

#### Specifiche selezionate

: Specifiche radio selezionata (RFD900x) {#tbl:radio-spec}

| Parametro | Valore | Unità |
|:----------|------:|:-----|
| Modello | RFD900x | - |
| Massa | 14.5 | g |
| Frequenza | 902-928 | MHz |
| Potenza output | 1 (max 30 dBm) | W |
| Data rate | 64-750 | kbps |
| Portata (LOS) | > 40 | km |
| Consumo | 5 | W |
| Temperatura operativa | −40 a +85 | °C |
| Dimensioni | 30 × 57 × 12.8 | mm |

### Riepilogo massa payload

@Tbl:payload-summary presenta la ripartizione completa della massa payload con i componenti selezionati.

: Riepilogo massa payload con componenti selezionati {#tbl:payload-summary}

| Componente | Modello | Qtà | Unità (g) | Totale (kg) |
|:----------|:------|:---:|:--------:|:----------:|
| Camera | Ricoh GR III | 1 | 257 | 0.257 |
| Radio | RFD900x | 1 | 14.5 | 0.015 |
| Antenna radio | Dipolo (stima) | 2 | 25 | 0.050 |
| Supporto camera | Custom (stima) | 1 | 50 | 0.050 |
| Cablaggio, connettori | - | 1 | 50 | 0.050 |
| **Totale payload** | - | - | - | **0.422** |

I componenti selezionati producono una massa payload totale di **0.42 kg**, ben entro il budget di 1.00 kg allocato dalla frazione payload $f_\text{payload}$ = 0.10.

$$f_\text{payload,effettivo} = \frac{m_\text{payload}}{MTOW} = \frac{0.422}{10.00} = 0.042 = 4.2\%$$

Questo rappresenta una **riduzione del 58%** dal budget allocato, fornendo margine per:

* Payload aggiuntivo se i requisiti di missione si espandono
* Componenti di gestione termica per l'operazione marziana
* Flessibilità di iterazione progettuale

La riduzione della massa payload rialloca 0.58 kg ad altre categorie di sistema, potenzialmente aumentando la capacità batteria per autonomia estesa.

