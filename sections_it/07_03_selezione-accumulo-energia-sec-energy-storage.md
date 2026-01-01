# Selezione dei componenti e verifica

## Selezione accumulo energia {#sec:energy-storage}

La selezione dell'accumulo energia segue dalla survey delle batterie presentata in @sec:energy-data. I criteri di selezione danno priorità all'energia specifica, alle prestazioni a bassa temperatura e all'affidabilità per le condizioni marziane.

### Requisiti dall'analisi dei vincoli

I requisiti energetici sono derivati dall'analisi QuadPlane in @sec:hybrid-vtol-analysis:

: Requisiti energetici dall'analisi dei vincoli {#tbl:energy-requirements}

| Parametro | Valore | Derivazione |
|:----------|------:|:-----------|
| Massa batteria disponibile | 3.50 kg | $f_\text{batt}$ × MTOW = 0.35 × 10.00 |
| Energia specifica richiesta | ≥ 200 Wh/kg | Margine autonomia missione |
| Capacità totale batteria | ≥ 700 Wh | 3.50 kg × 200 Wh/kg |
| Energia utilizzabile (80% DoD, 95% η) | ≥ 532 Wh | 700 × 0.80 × 0.95 |
| Temperatura operativa | −60 a +20 °C | Condizioni superficie Marte |

### Valutazione dei candidati

@Tbl:battery-selection presenta le tecnologie batteria valutate rispetto ai requisiti di missione, basate sui dati survey da @tbl:reference-battery.

: Analisi trade-off selezione tecnologia batteria {#tbl:battery-selection}

| Tecnologia | Energia spec. (Wh/kg) | Temp. (°C) | Cicli vita | Valutazione |
|:-----------|:--------------------:|:----------------:|:----------:|:------:|
| Li-ion stato solido | 270 | −20 a +60 | 1000 | Selezionata |
| Li-ion semi-solido | 180 | −20 a +45 | 500 | Alternativa |
| LiPo (alta tensione) | 150 | −20 a +45 | 300 | Respinta |
| LiPo standard | 130-150 | 0 a +40 | 300 | Respinta |

### Motivazione della selezione

Le **batterie litio-ione a stato solido** sono selezionate in base a:

* **Energia specifica**: 270 Wh/kg supera il requisito di 200 Wh/kg del 35% [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025]<!-- #specs -->
* **Intervallo temperatura**: da −20 a +60 °C fornisce tolleranza base al freddo [@cgbtshenzhenchanggongbeitechnology222VUAVSolid2025]<!-- #specs -->
* **Vita ciclica**: 1000 cicli all'80% DoD supporta campagna missione lunga
* **Sicurezza**: elettrolita solido riduce il rischio di thermal runaway nell'habitat marziano

La tecnologia **litio-ione semi-solido** è mantenuta come alternativa se la disponibilità stato solido è limitata. A 180 Wh/kg, soddisfa comunque i requisiti di missione con margine ridotto.

Le batterie LiPo standard sono respinte per:

* Energia specifica inferiore (130-150 Wh/kg)
* Intervallo temperatura operativa ristretto (tipicamente 0 a +40 °C senza preriscaldamento)
* Vita ciclica più breve (circa 300 cicli)

### Considerazioni termiche marziane

L'intervallo operativo batteria stato solido (−20°C minimo) non copre completamente le temperature superficiali marziane (−60 a +20 °C). La strategia di gestione termica batteria include:

* Vano batteria isolato per ridurre la perdita di calore
* Elementi riscaldanti resistivi attivati durante i periodi di cold soak
* Condizionamento batteria pre-volo nell'hangar habitat
* Operazioni di volo limitate alla finestra termica diurna

La massa del sistema di controllo termico è allocata nella frazione di massa avionica/sistemi.

### Specifiche selezionate

: Specifiche batteria selezionata (Li-ion stato solido) {#tbl:battery-spec}

| Parametro | Valore | Unità |
|:----------|------:|:-----|
| Chimica | Li-ion stato solido | - |
| Modello riferimento | CGBT SLD1-6S27Ah | - |
| Configurazione | 6S (22.2V nominale) | - |
| Energia specifica | 270 | Wh/kg |
| Massa batteria | 3.50 | kg |
| Capacità totale | 945 | Wh |
| Capacità utilizzabile (80% DoD, 95% η) | 718 | Wh |
| Temperatura operativa | −20 a +60 | °C |
| Vita ciclica (80% DoD) | 1000 | cicli |

### Verifica budget energetico

La batteria selezionata fornisce 718 Wh di energia utilizzabile. Dall'analisi QuadPlane (@sec:hybrid-vtol-analysis), il requisito energetico di missione è:

$$E_\text{missione} = E_\text{hover} + E_\text{transizione} + E_\text{crociera} = 106.0 + 10.0 + 302.0 = 418.0 \text{ Wh}$$

Il margine energetico è:

$$\text{Margine} = \frac{E_\text{disponibile} - E_\text{missione}}{E_\text{missione}} = \frac{718 - 418.0}{418.0} = 71.8\%$$

Applicando la riserva energetica del 20%:

$$E_\text{riserva} = 0.20 \times 718 = 143.6 \text{ Wh}$$
$$E_\text{netto} = 718 - 143.6 = 574.4 \text{ Wh}$$

Il margine netto sopra il requisito di missione è:

$$\text{Margine netto} = \frac{E_\text{netto} - E_\text{missione}}{E_\text{missione}} = \frac{574.4 - 418.0}{418.0} = 37.4\%$$

Questo supera la riserva minima del 20%, confermando che la selezione batteria soddisfa i requisiti di missione.

