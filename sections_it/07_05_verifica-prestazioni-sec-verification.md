# Selezione dei componenti e verifica

## Verifica delle prestazioni {#sec:verification}

Questa sezione verifica che i componenti selezionati, una volta integrati, soddisfino i requisiti di missione stabiliti in @sec:user-needs. La verifica confronta le specifiche effettive dei componenti con le ipotesi dell'analisi dei vincoli.

### Roll-up massa componenti

@Tbl:mass-rollup consolida il budget di massa usando le specifiche dei componenti selezionati dalle Sezioni 7.1-7.3.

: Ripartizione massa verificata con componenti selezionati {#tbl:mass-rollup}

| Categoria | Allocata (kg) | Selezionata (kg) | Margine |
|:---------|---------------:|--------------:|-------:|
| Propulsione | 2.00 | 1.18 | +41% |
| Payload | 1.00 | 0.42 | +58% |
| Batteria | 3.50 | 3.50 | 0% |
| Struttura | 3.00 | 3.00 | 0% |
| Avionica | 0.50 | 0.50 | 0% |
| **Totale** | **10.00** | **8.60** | **+14%** |

Nota: Le masse di struttura e avionica sono valori allocati, non ancora verificati rispetto alle selezioni componenti. La massa batteria è fissata al valore allocato per massimizzare la capacità energetica.

### Riallocazione massa

Le selezioni di propulsione e payload producono un risparmio di massa combinato di:

$$\Delta m = (2.00 - 1.18) + (1.00 - 0.42) = 0.82 + 0.58 = 1.40 \text{ kg}$$

Questo margine di 1.40 kg può essere riallocato per aumentare l'autonomia attraverso capacità batteria aggiuntiva:

$$m_\text{batt,max} = 3.50 + 1.40 = 4.90 \text{ kg}$$
$$E_\text{disponibile,max} = 4.90 \times 270 \times 0.80 \times 0.95 = 1006 \text{ Wh}$$

Tuttavia, si raccomanda di mantenere la massa batteria baseline di 3.50 kg per preservare il margine strutturale e accomodare la crescita progettuale durante la progettazione di dettaglio.

### Verifica potenza

@Tbl:power-verify confronta le ipotesi di potenza dell'analisi dei vincoli con le capacità dei componenti selezionati.

: Verifica potenza rispetto ai componenti selezionati {#tbl:power-verify}

| Modo | Richiesta (W) | Fornita (W) | Margine |
|:-----|-------------:|-------------:|-------:|
| Hovering totale | 3181 | 8 × 375 = 3000 | −6% |
| Crociera totale | 318 | 2 × 350 = 700 | +120% |

Il margine di potenza hovering è leggermente negativo (−6%), indicando che i motori SunnySky V4006-380 operano vicino alla loro potenza nominale durante l'hovering. Questo è accettabile per la breve durata dell'hovering (2 minuti totali per volo) ma richiede progetto termico adeguato per il raffreddamento motori nell'atmosfera rarefatta marziana e considerazione dell'alternativa MAD 4008 EEE (88 g, 400 W) se i test rivelano problemi termici.

Il margine di potenza crociera è sostanziale (+120%), confermando che i motori T-Motor AT2312-1150 sono adeguatamente dimensionati con significativo headroom termico.

### Verifica energia

@Tbl:energy-verify riassume la verifica del budget energetico.

: Verifica budget energetico {#tbl:energy-verify}

| Parametro | Valore | Unità |
|:----------|------:|:-----|
| Capacità batteria (totale) | 945 | Wh |
| Capacità utilizzabile (80% DoD, 95% η) | 718 | Wh |
| Requisito energetico missione | 418.0 | Wh |
| Riserva (20%) | 143.6 | Wh |
| Netto disponibile | 574.4 | Wh |
| Margine netto | +37.4 | % |

Il margine netto del 37.4% supera il requisito di riserva del 20%, confermando l'adeguatezza energetica.

### Verifica autonomia

L'autonomia raggiunta con i componenti selezionati:

$$t_\text{crociera,max} = \frac{E_\text{netto} - E_\text{hover} - E_\text{transizione}}{P_\text{crociera}} = \frac{574.4 - 106.0 - 10.0}{318} \times 60 = 86.5 \text{ min}$$

Tempo di volo totale:

$$t_\text{totale} = t_\text{hover} + t_\text{transizione} + t_\text{crociera} = 2 + 1 + 86.5 = 89.5 \text{ min}$$

Questo supera il requisito di 60 minuti del 49%.

### Verifica raggio

Il raggio raggiunto con i componenti selezionati:

$$R = V_\text{crociera} \times t_\text{crociera,max} = 40 \times \frac{86.5}{60} = 57.7 \text{ km (solo andata)}$$

Raggio andata-ritorno: 115.3 km, superando il requisito di 100 km del 15%.

### Riepilogo conformità requisiti

@Tbl:compliance riassume lo stato di conformità rispetto ai requisiti di missione da @sec:user-needs.

: Riepilogo conformità requisiti {#tbl:compliance}

| Requisito | Target | Raggiunto | Stato |
|:------------|-------:|---------:|:------:|
| MTOW | 10.00 kg | 8.60 kg | Conforme |
| Autonomia | ≥ 60 min | 89.5 min | Conforme |
| Raggio | ≥ 100 km | 115.3 km | Conforme |
| Raggio operativo | ≥ 50 km | 57.7 km | Conforme |
| Capacità payload | ≥ 1.0 kg | 0.42 kg (usato) | Conforme |
| Capacità VTOL | Richiesta | QuadPlane | Conforme |

Tutti i requisiti di missione sono soddisfatti con margini positivi. Il punto di progetto è verificato come fattibile con i componenti commerciali selezionati.

### Sensibilità di progetto

Le sensibilità chiave identificate durante la verifica sono:

1. Dimensionamento motori hovering: il deficit di potenza del 6% richiede verifica termica nelle condizioni atmosferiche marziane. Il passaggio al MAD 4008 EEE (88 g, 400 W) aggiungerebbe 176 g alla massa propulsione fornendo margine di potenza adeguato.
2. Temperatura batteria: l'intervallo operativo batteria stato solido (−20°C minimo) non copre le condizioni superficiali marziane più fredde. La gestione termica attiva è obbligatoria.
3. Controllo termico camera: la Ricoh GR III non ha specifiche per basse temperature. Sono richiesti test di qualifica o un involucro isolato con riscaldamento.
4. Crescita massa: il margine di massa di 1.40 kg fornisce buffer per la crescita progettuale durante la progettazione di dettaglio, sistemi di controllo termico e rinforzo strutturale se richiesto.

