# Decisioni progettuali

## Selezione dei materiali {#sec:material-selection}

Questa sezione presenta la selezione dei materiali e l'approccio alla progettazione strutturale per l'UAV marziano, affrontando i requisiti termici, meccanici e di massa. La selezione si basa sull'analisi dei compromessi in @sec:materials-data.

### Materiale strutturale primario

Il polimero rinforzato con fibra di carbonio (CFRP) è selezionato come materiale strutturale primario, coerentemente con l'heritage di Ingenuity e la pratica commerciale.

Il CFRP presenta bassa espansione termica (CTE circa 0.5 ppm/°C), minimizzando le sollecitazioni termiche dal ciclo di temperatura diurno da −80°C a +20°C su Marte. Fornisce il più alto rapporto resistenza-peso tra i materiali strutturali comunemente disponibili, supportando la minimizzazione della massa critica per il volo marziano. L'elicottero Ingenuity ha dimostrato con successo la costruzione in CFRP su Marte, utilizzando tessuti in carbonio a tow distribuito TeXtreme selezionati per la resistenza alle microfessurazioni da ciclo termico [@latourabOxeonPartOwnedHoldings2025]<!-- #s:textreme -->.

### Materiali per elementi strutturali

: Materiali strutturali per componente {#tbl:material-selection}

| Componente | Materiale | Costruzione | Motivazione |
|:----------|:---------|:-------------|:----------|
| Rivestimenti alari | CFRP | Sandwich con nucleo in schiuma | Alta rigidezza-peso |
| Rivestimenti fusoliera | CFRP | Sandwich con nucleo in schiuma | Alta rigidezza-peso |
| Longherone alare | CFRP | Tubo o trave a I | Percorso carichi flessionali |
| Boom motori di sollevamento | CFRP | Tubo avvolto a filamento | Torsione e flessione |
| Boom supporto coda | CFRP | Tubo pultruso | Bassa massa, alta rigidezza |
| Carrello di atterraggio | GFRP | Laminato | Tolleranza agli impatti |
| Bordi d'attacco | GFRP | Laminato | Resistenza all'erosione |

I rivestimenti dell'ala e della fusoliera utilizzano una costruzione sandwich con nucleo in schiuma e facce in fibra di carbonio, fornendo alta rigidezza-peso per le superfici aerodinamiche primarie. I boom dei motori di sollevamento e del supporto della coda sono tubi in fibra di carbonio, avvolti a filamento o pultrusi. Il rinforzo in fibra di vetro (GFRP) è utilizzato nei punti di attacco del carrello di atterraggio e sui bordi d'attacco vulnerabili per la tolleranza agli impatti.

### Materiali per la gestione termica

La gestione termica interna utilizza superfici interne placcate in oro o isolamento multistrato (MLI) per il controllo termico del compartimento elettronica, seguendo la pratica di Ingenuity. La bassa conducibilità termica del CFRP aiuta l'isolamento termico passivo del vano elettronica dall'ambiente esterno.

### Implicazioni per la frazione di massa

La selezione del CFRP e delle tecniche di costruzione in composito avanzato influenza la frazione di massa strutturale utilizzata nella stima dei pesi (@sec:mass-breakdown). Basandosi sull'heritage di Ingenuity e sui dati degli UAV commerciali:

: Confronto delle proprietà dei materiali {#tbl:material-comparison}

| Parametro | Base alluminio | Composito CFRP | Riduzione |
|:----------|-------------------:|---------------:|----------:|
| Resistenza specifica (MPa·m³/kg) | 110 | 450 | — |
| Frazione di massa strutturale | 0.35–0.40 | 0.25–0.30 | 25–30% |
| Fattore di densità alare, $K_\rho$ | 1.0 | 0.50–0.60 | 40–50% |

Le equazioni di stima dei pesi in @sec:mass-breakdown applicano fattori di densità corretti per CFRP per tenere conto della costruzione in composito. Vengono utilizzate stime conservative data la limitata esperienza di volo per le strutture composite marziane.
