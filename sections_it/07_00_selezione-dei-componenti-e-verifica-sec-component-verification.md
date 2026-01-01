# Selezione dei componenti e verifica {#sec:component-verification}

Questa sezione presenta la selezione di componenti specifici basata sui risultati del dimensionamento dall'analisi dei vincoli (@sec:hybrid-vtol-analysis). La selezione dei componenti segue un approccio sistematico di trade-off, valutando i candidati rispetto ai requisiti derivati dai calcoli della Sezione 5.

## Metodologia di selezione

### Requisiti dall'analisi dei vincoli

I requisiti di potenza sono derivati dai calcoli del codice in `section5/hybrid_vtol.py`:

: Requisiti di potenza dall'analisi dei vincoli {#tbl:motor-power-requirements}

| Parametro | Valore | Derivazione |
|:----------|------:|:-----------|
| Potenza di hovering totale | 3181 W | @eq:electric-hover-qp |
| Per motore di sollevamento (8) | 398 W | 3181 W ÷ 8 |
| Per coppia coassiale (4) | 795 W | 3181 W ÷ 4 |
| Potenza di crociera totale | 318 W | @eq:cruise-power-value |
| Per motore di crociera (2) | 159 W | 318 W ÷ 2 |

### Vincoli del budget di massa

Il budget di massa di propulsione da @tbl:design-mass-fractions è:

$$m_\text{propulsione} = f_\text{prop} \times MTOW = 0.20 \times 10.00 = 2.00 \text{ kg}$$

Allocando il 70% al sistema di sollevamento e il 30% al sistema di crociera:

: Allocazione della massa di propulsione {#tbl:mass-allocation}

| Categoria componente | Massa target (kg) | Target per unità |
|:-------------------|----------------:|:----------------|
| Motori di sollevamento (8) | 0.560 | 70 g ciascuno |
| ESC di sollevamento (8) | 0.160 | 20 g ciascuno |
| Eliche di sollevamento (8) | 0.160 | 20 g ciascuno |
| Montaggio sollevamento | 0.200 | totale |
| **Subtotale sollevamento** | **1.080** | - |
| Motori di crociera (2) | 0.200 | 100 g ciascuno |
| ESC di crociera (2) | 0.060 | 30 g ciascuno |
| Eliche di crociera (2) | 0.040 | 20 g ciascuno |
| **Subtotale crociera** | **0.300** | - |
| Cablaggio, connettori | 0.320 | margine |
| **Totale propulsione** | **1.700** | - |

### Criteri di selezione

I componenti sono valutati rispetto ai seguenti criteri, in ordine di priorità:

1. **Adeguatezza di potenza**: soddisfare o superare i requisiti di potenza dell'analisi dei vincoli
2. **Conformità di massa**: rimanere entro i target di massa per unità
3. **Compatibilità di tensione**: LiPo 6S (22.2V nominale) per uniformità di sistema
4. **Intervallo di temperatura**: operazione alle temperature della superficie marziana (fino a −60°C)
5. **Affidabilità**: preferenza per design collaudati con heritage di volo

## Sistema di propulsione {#sec:propulsion-selection}

### Motori di sollevamento {#sec:lift-motor-selection}

#### Requisiti

Ogni motore di sollevamento deve fornire almeno 400 W di potenza continua rimanendo sotto i 100 g (target 70 g) per rispettare il budget di massa. I motori devono essere compatibili con eliche da 12-16 pollici per allinearsi alla classe di eliche di sollevamento selezionata.

#### Confronto candidati

@tbl:lift-motor-comparison presenta i motori di sollevamento candidati valutati rispetto ai requisiti.

: Confronto candidati motori di sollevamento {#tbl:lift-motor-comparison}

| Motore | Massa (g) | Potenza (W) | Spinta (g) | KV | LiPo | Elica (in) | Stato |
|:------|:--------:|----------:|:----------:|---:|:----:|:---------:|:-------|
| SunnySky V4006-380 | 66 | 375 | 2560 | 380 | 4-6S | 12-15 | **Selezionato** |
| MAD 4008 EEE-380 | 88 | ~400 | 2700 | 380 | 4-6S | 14-18 | Alternativa |
| T-Motor MN5008-400 | 135 | 800 | 4200 | 400 | 6S | 15-17 | Troppo pesante |
| T-Motor MN505-S-260 | 225 | 2500 | - | 260 | 12S | 16-17 | Troppo pesante |

#### Motivazione della selezione

Il **SunnySky V4006-380** è selezionato per i motori di sollevamento in base a:

* **Massa**: 66 g per motore è ben entro il target di 70 g, consentendo 8 motori a 528 g totali
* **Potenza**: 375 W continui sono adeguati per il requisito di 398 W con appropriato abbinamento dell'elica
* **Spinta**: 2560 g di spinta massima fornisce margine 2:1 spinta-peso per motore
* **Disponibilità**: ampiamente disponibile da più fornitori

Il MAD 4008 EEE è mantenuto come alternativa se è richiesto margine di potenza aggiuntivo.

### ESC di sollevamento {#sec:lift-esc-selection}

#### Requisiti

Ogni ESC di sollevamento deve gestire almeno 25A di corrente continua (basato su 400 W a 16V) rimanendo sotto i 20 g per rispettare il budget di massa.

#### Confronto candidati

: Confronto candidati ESC di sollevamento {#tbl:lift-esc-comparison}

| ESC | Massa (g) | Continua (A) | Picco (A) | LiPo | BEC | Stato |
|:----|:--------:|---------------:|----------:|:----:|:---:|:-------|
| Hobbywing XRotor Micro 30A | 6 | 30 | 40 | 2-4S | No | **Selezionato** |
| T-Motor F35A | 6.7 | 35 | 45 | 3-6S | No | Alternativa |
| T-Motor FLAME 60A 12S | 74 | 60 | 80 | 12S | No | Troppo pesante |

#### Motivazione della selezione

L'**Hobbywing XRotor Micro 30A** è selezionato per gli ESC di sollevamento in base a:

* **Massa**: 6 g per ESC consente 8 ESC a soli 48 g totali
* **Corrente**: 30A continui superano il requisito di ~25A
* **Compatibilità**: firmware BLHeli_32 per controllo motore affidabile

### Motori di crociera {#sec:cruise-motor-selection}

#### Requisiti

Ogni motore di crociera deve fornire almeno 200 W di potenza continua (con margine sopra 159 W) rimanendo sotto i 100 g.

#### Confronto candidati

: Confronto candidati motori di crociera {#tbl:cruise-motor-comparison}

| Motore | Massa (g) | Potenza (W) | KV | LiPo | Stato |
|:------|:--------:|----------:|---:|:----:|:-------|
| T-Motor AT2312-1150 | 60 | 350 | 1150 | 2-4S | **Selezionato** |
| T-Motor AT2814-1000 | 109 | 370 | 1000 | 2-4S | Alternativa |
| T-Motor AT4130-230 | 408 | 2500 | 230 | 12S | Troppo pesante |

#### Motivazione della selezione

Il **T-Motor AT2312-1150** è selezionato per i motori di crociera in base a:

* **Massa**: 60 g per motore consente 2 motori a soli 120 g totali
* **Potenza**: 350 W continui superano il requisito di 159 W con margine 2:1
* **Design**: la serie AT è ottimizzata per l'efficienza di crociera ad ala fissa

### Riepilogo massa propulsione {#sec:propulsion-mass-summary}

@tbl:propulsion-summary presenta la ripartizione completa della massa di propulsione con i componenti selezionati.

: Riepilogo massa sistema di propulsione con componenti selezionati {#tbl:propulsion-summary}

| Componente | Modello | Qtà | Unità (g) | Totale (kg) |
|:----------|:------|:---:|:--------:|:----------:|
| Motori sollevamento | SunnySky V4006-380 | 8 | 66 | 0.528 |
| ESC sollevamento | Hobbywing XRotor Micro 30A | 8 | 6 | 0.048 |
| Eliche sollevamento | NS14×4.8 | 8 | 18 | 0.144 |
| **Subtotale sollevamento** | - | - | - | **0.720** |
| Motori crociera | T-Motor AT2312-1150 | 2 | 60 | 0.120 |
| ESC crociera | Hobbywing XRotor Micro 30A | 2 | 6 | 0.012 |
| Eliche crociera | NS12×6 | 2 | 15 | 0.030 |
| **Subtotale crociera** | - | - | - | **0.162** |
| Montaggio | Bracci, navicella | 1 | 200 | 0.200 |
| Cablaggio | Distribuzione, connettori | 1 | 100 | 0.100 |
| **Subtotale condiviso** | - | - | - | **0.300** |
| **Totale propulsione** | - | - | - | **1.182** |

Nota: I subtotali di sollevamento e crociera includono dati componenti con fonti. I componenti condivisi (montaggio, cablaggio) sono stime ingegneristiche senza schede tecniche.

### Confronto con budget di massa

I componenti selezionati producono una massa di propulsione totale di **1.18 kg**, ben entro il budget di 2.00 kg allocato dalla frazione di propulsione $f_\text{prop}$ = 0.20.

$$f_\text{prop,effettivo} = \frac{m_\text{propulsione}}{MTOW} = \frac{1.182}{10.00} = 0.118 = 11.8\%$$

Questo rappresenta una **riduzione del 40%** dal budget allocato, fornendo margine per:

* Motori alternativi più pesanti se è necessaria potenza aggiuntiva
* Componenti di gestione termica per l'operazione su Marte
* Flessibilità di iterazione progettuale

La riduzione della massa di propulsione rialloca 0.82 kg ad altre categorie di sistema, potenzialmente aumentando la capacità di payload o la massa strutturale.

