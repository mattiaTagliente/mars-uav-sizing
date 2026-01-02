# Appendix D: Atmospheric model derivation

## Model overview

The atmospheric model calculates density, pressure, temperature, and dynamic viscosity as functions of altitude for the Arcadia Planitia operating site.

## Temperature profile

The temperature varies linearly with altitude according to the polytropic model:

$$T(h) = T_0 - L \cdot h$$ {#eq:temp-altitude}

where:

* $T_0$ = 210 K (reference temperature at datum)
* $L$ = 0.00222 K/m (temperature lapse rate)
* $h$ = altitude above datum (m)

At the operating altitude of −3000 m (Arcadia Planitia):

$$T(-3000) = 210 - 0.00222 \times (-3000) = 210 + 6.66 = 216.66 \text{ K}$$

## Pressure profile

The pressure follows the polytropic relation derived from hydrostatic equilibrium:

$$p(h) = p_0 \left( \frac{T(h)}{T_0} \right)^{\frac{g}{L \cdot R_{CO_2}}}$$ {#eq:pressure-altitude}

where:

* $p_0$ = 610 Pa (reference pressure at datum)
* $g$ = 3.711 m/s² (Mars surface gravity)
* $R_{CO_2}$ = 188.92 J/(kg·K) (specific gas constant for CO₂)

The exponent evaluates to:

$$n = \frac{g}{L \cdot R_{CO_2}} = \frac{3.711}{0.00222 \times 188.92} = 8.85$$

At the operating altitude:

$$p(-3000) = 610 \times \left( \frac{216.66}{210} \right)^{8.85} = 610 \times 1.327 = 809.5 \text{ Pa}$$

## Density calculation

Density is calculated from the ideal gas law:

$$\rho = \frac{p}{R_{CO_2} \cdot T}$$ {#eq:density-ideal-gas}

At the operating conditions:

$$\rho = \frac{809.5}{188.92 \times 216.66} = 0.0198 \text{ kg/m}^3$$

## Dynamic viscosity

Dynamic viscosity is calculated using Sutherland's formula:

$$\mu = \mu_\text{ref} \left( \frac{T}{T_\text{ref}} \right)^{1.5} \frac{T_\text{ref} + S}{T + S}$$ {#eq:sutherland}

where:

* $\mu_\text{ref}$ = 1.48 × 10⁻⁵ Pa·s (reference viscosity at 293 K)
* $T_\text{ref}$ = 293 K (reference temperature)
* $S$ = 240 K (Sutherland constant for CO₂)

At the operating temperature:

$$\mu = 1.48 \times 10^{-5} \times \left( \frac{216.66}{293} \right)^{1.5} \times \frac{293 + 240}{216.66 + 240} = 1.00 \times 10^{-5} \text{ Pa·s}$$

## Summary of operating conditions

: Arcadia Planitia atmospheric properties at −3000 m elevation {#tbl:atm-summary}

| Property | Symbol | Value | Unit |
|:---------|:------:|------:|:-----|
| Altitude | $h$ | −3000 | m |
| Temperature | $T$ | 216.66 | K |
| Pressure | $p$ | 809.5 | Pa |
| Density | $\rho$ | 0.0198 | kg/m³ |
| Dynamic viscosity | $\mu$ | 1.00 × 10⁻⁵ | Pa·s |
| Speed of sound | $a$ | 231.2 | m/s |

## Implementation

The atmospheric model is implemented in the Python module `mars_uav_sizing/core/atmosphere.py`. Key functions include:

* `MarsAtmosphere.temperature(h)` - Returns temperature at altitude
* `MarsAtmosphere.pressure(h)` - Returns pressure at altitude
* `MarsAtmosphere.density(h)` - Returns density at altitude
* `MarsAtmosphere.viscosity(h)` - Returns dynamic viscosity at altitude

