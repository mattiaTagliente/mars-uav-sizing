# Appendice D: Derivazione del modello atmosferico

## Panoramica del modello

Il modello atmosferico calcola densità, pressione, temperatura e viscosità dinamica in funzione dell'altitudine per il sito operativo di Arcadia Planitia.

## Profilo di temperatura

La temperatura varia linearmente con l'altitudine secondo il modello politropico:

$$T(h) = T_0 - L \cdot h$$ {#eq:temp-altitude}

dove:

* $T_0$ = 210 K (temperatura di riferimento al datum)
* $L$ = 0.00222 K/m (gradiente termico)
* $h$ = altitudine sopra il datum (m)

All'altitudine operativa di −3000 m (Arcadia Planitia):

$$T(-3000) = 210 - 0.00222 \times (-3000) = 210 + 6.66 = 216.66 \text{ K}$$

## Profilo di pressione

La pressione segue la relazione politropica derivata dall'equilibrio idrostatico:

$$p(h) = p_0 \left( \frac{T(h)}{T_0} \right)^{\frac{g}{L \cdot R_{CO_2}}}$$ {#eq:pressure-altitude}

dove:

* $p_0$ = 610 Pa (pressione di riferimento al datum)
* $g$ = 3.711 m/s² (gravità superficiale marziana)
* $R_{CO_2}$ = 188.92 J/(kg·K) (costante specifica dei gas per CO₂)

L'esponente vale:

$$n = \frac{g}{L \cdot R_{CO_2}} = \frac{3.711}{0.00222 \times 188.92} = 8.85$$

All'altitudine operativa:

$$p(-3000) = 610 \times \left( \frac{216.66}{210} \right)^{8.85} = 610 \times 1.327 = 809.5 \text{ Pa}$$

## Calcolo della densità

La densità è calcolata dalla legge dei gas ideali:

$$\rho = \frac{p}{R_{CO_2} \cdot T}$$ {#eq:density-ideal-gas}

Alle condizioni operative:

$$\rho = \frac{809.5}{188.92 \times 216.66} = 0.0198 \text{ kg/m}^3$$

## Viscosità dinamica

La viscosità dinamica è calcolata usando la formula di Sutherland:

$$\mu = \mu_\text{ref} \left( \frac{T}{T_\text{ref}} \right)^{1.5} \frac{T_\text{ref} + S}{T + S}$$ {#eq:sutherland}

dove:

* $\mu_\text{ref}$ = 1.48 × 10⁻⁵ Pa·s (viscosità di riferimento a 293 K)
* $T_\text{ref}$ = 293 K (temperatura di riferimento)
* $S$ = 240 K (costante di Sutherland per CO₂)

Alla temperatura operativa:

$$\mu = 1.48 \times 10^{-5} \times \left( \frac{216.66}{293} \right)^{1.5} \times \frac{293 + 240}{216.66 + 240} = 1.00 \times 10^{-5} \text{ Pa·s}$$

## Riepilogo condizioni operative

: Proprietà atmosferiche Arcadia Planitia a elevazione −3000 m {#tbl:atm-summary}

| Proprietà | Simbolo | Valore | Unità |
|:---------|:------:|------:|:-----|
| Altitudine | $h$ | −3000 | m |
| Temperatura | $T$ | 216.66 | K |
| Pressione | $p$ | 809.5 | Pa |
| Densità | $\rho$ | 0.0198 | kg/m³ |
| Viscosità dinamica | $\mu$ | 1.00 × 10⁻⁵ | Pa·s |
| Velocità del suono | $a$ | 231.2 | m/s |

## Implementazione

Il modello atmosferico è implementato nel modulo Python `mars_uav_sizing/core/atmosphere.py`. Le funzioni chiave includono:

* `MarsAtmosphere.temperature(h)` - Restituisce temperatura all'altitudine
* `MarsAtmosphere.pressure(h)` - Restituisce pressione all'altitudine
* `MarsAtmosphere.density(h)` - Restituisce densità all'altitudine
* `MarsAtmosphere.viscosity(h)` - Restituisce viscosità dinamica all'altitudine

