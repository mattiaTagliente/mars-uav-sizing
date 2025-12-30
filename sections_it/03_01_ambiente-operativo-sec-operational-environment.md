# Analisi della missione

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
