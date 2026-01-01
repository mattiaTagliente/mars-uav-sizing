# Mission analysis

## Operational environment {#sec:operational-environment}

Arcadia Planitia is selected as the reference operating location. This region offers several advantages for early Mars exploration: its low elevation (−3 km relative to datum) provides higher atmospheric density, the relatively flat terrain is suitable for habitat construction, subsurface water ice deposits present scientific interest, and the moderate latitude (47°11'24"N) balances solar illumination with ice stability.

Mars atmospheric flight occurs under conditions different from Earth [@desertAerodynamicDesignMartian2017]<!-- #s:mars-atmosphere -->. The thin CO₂ atmosphere exhibits surface pressures around 610 Pa mean, with significant variation depending on elevation and season. Surface temperatures average around 210 K with substantial diurnal swings. At the low elevations favorable for flight, atmospheric density remains approximately two orders of magnitude lower than Earth sea level, resulting in low Reynolds number aerodynamics and reduced lift generation. 

![The area of Arcadia Planitia in the Mars geographical context [@esaArcadiaPlanitiaContext2025]<!-- #fig:arcadia -->.](figures/Arcadia_Planitia_in_context_pillars.png){#fig:arcadia-context width=50%}

### Mars atmosphere equations

The Mars atmosphere is modeled using the barometric formula with a composition of 95.3% CO₂ [@nasaMarsAtmosphereModel2021]<!-- #s:composition -->. The following equations describe atmospheric properties as functions of geometric altitude $h$ (in meters above the reference datum):

$$T(h) = T_0 - L \cdot h$$ {#eq:temperature}

where $T_0$ = 210 K is the reference temperature and $L$ = 0.00222 K/m is the lapse rate.

$$p(h) = p_0 \left(\frac{T(h)}{T_0}\right)^{g/(R_{CO2} \cdot L)}$$ {#eq:pressure}

where $p_0$ = 610 Pa is the mean surface pressure, $g$ = 3.711 m/s² is Mars surface gravity, and $R_{CO_2}$ = 188.92 J/(kg·K) is the specific gas constant for CO₂.

The density follows from the ideal gas law:

$$ρ(h) = \frac{p(h)}{R_{CO_2} \cdot T(h)}$$ {#eq:density}

The speed of sound is:

$$a(h) = \sqrt{γ \cdot R_{CO_2} \cdot T(h)}$$ {#eq:speed-of-sound}

where γ = 1.29 for CO₂.

Dynamic viscosity $\mu$ is approximated using Sutherland's law:

$$\mu(h) = \mu_\text{ref} \left(\frac{T(h)}{T_\text{ref}}\right)^{1.5} \frac{T_\text{ref} + S}{T(h) + S}$$ {#eq:dynamic-viscosity}

where $\mu_\text{ref}$ = 1.48 × 10⁻⁵ Pa·s is the reference dynamic viscosity at $T_\text{ref}$ = 293 K, and $S$ = 222 K is the Sutherland constant for CO₂. Kinematic viscosity $\nu$ is then obtained from:

$$\nu(h) = \frac{\mu(h)}{\rho(h)}$$ {#eq:kinematic-viscosity}

### Arcadia Planitia conditions

At the operating altitude of 50 m above Arcadia Planitia (−3 km datum elevation, so −2.95 km absolute):

: Atmospheric conditions at Arcadia Planitia, 50 m AGL {#tbl:atmosphere}

| Property | Symbol | Value | Units |
|:---------|:------:|------:|:------|
| Temperature | $T$ | 216.6 | K |
| Pressure | $p$ | 800.5 | Pa |
| Density | $\rho$ | 0.01960 | kg/m³ |
| Speed of sound | $a$ | 229.7 | m/s |
| Dynamic viscosity | $\mu$ | 1.080 × 10⁻⁵ | Pa·s |
| Kinematic viscosity | $\nu$ | 5.170 × 10⁻⁴ | m²/s |
