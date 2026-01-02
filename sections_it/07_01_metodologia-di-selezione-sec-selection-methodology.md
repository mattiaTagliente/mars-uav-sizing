# Selezione dei componenti e verifica

## Metodologia di selezione {#sec:selection-methodology}

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

| Categoria componente | Quantità | Massa target (kg) | Target per unità |
|:-------------------|:--------:|----------------:|:----------------|
| Motori di sollevamento | 8 | 0.560 | 70 g ciascuno |
| ESC di sollevamento | 8 | 0.160 | 20 g ciascuno |
| Eliche di sollevamento | 8 | 0.160 | 20 g ciascuno |
| Montaggio sollevamento | 1 | 0.200 | totale |
| Subtotale sollevamento | N.A. | 1.080 | N.A. |
| Motori di crociera | 2 | 0.200 | 100 g ciascuno |
| ESC di crociera | 2 | 0.060 | 30 g ciascuno |
| Eliche di crociera | 2 | 0.040 | 20 g ciascuno |
| Subtotale crociera | N.A. | 0.300 | N.A. |
| Cablaggio, connettori | 1 | 0.320 | margine |
| Totale propulsione | N.A. | 1.700 | N.A. |

### Criteri di selezione

I componenti sono valutati rispetto ai seguenti criteri, in ordine di priorità: (1) adeguatezza di potenza, soddisfacendo o superando i requisiti di potenza dell'analisi dei vincoli; (2) conformità di massa, rimanendo entro i target di massa per unità; (3) compatibilità di tensione con LiPo 6S nominale 22.2V per uniformità di sistema; (4) intervallo di temperatura per operazione alle temperature della superficie marziana fino a −60°C; (5) affidabilità, con preferenza per design collaudati con heritage di volo.

