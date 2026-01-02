# Reference data and trade-off analysis

## Initial mass estimate {#sec:initial-mass-estimate}

This section establishes the initial MTOW (Maximum Takeoff Weight) estimate using the mass fraction approach, a standard technique in aircraft conceptual design [@roskamAirplaneDesign12005a]<!-- #s:mass-fraction --> [@sadraeyAircraftDesignSystems2013]<!-- #s:mass-fraction -->. The MTOW range established here provides the starting point for constraint analysis in @sec:constraint-analysis.

### Mass fraction methodology

The total aircraft mass decomposes into major component categories:

$$MTOW = m_\text{payload} + m_\text{battery} + m_\text{empty} + m_\text{propulsion} + m_\text{avionics}$$ {#eq:mtow-breakdown}

Each component mass can be expressed as a fraction of MTOW:

$$f_i = \frac{m_i}{MTOW}$$ {#eq:fraction-def}

Since the sum of fractions equals unity:

$$f_\text{payload} + f_\text{battery} + f_\text{empty} + f_\text{propulsion} + f_\text{avionics} = 1$$ {#eq:fraction-sum}

Given the payload mass $m_\text{payload}$ (a mission requirement from @sec:payload-systems), the MTOW can be estimated if the payload fraction is known:

$$MTOW = \frac{m_\text{payload}}{f_\text{payload}}$$ {#eq:mtow-from-payload}

This approach provides a first-order estimate before detailed component selection.

### Reference data analysis

Mass fractions were calculated from a database of nine commercial hybrid VTOL UAVs documented in @sec:commercial-vtol. @tbl:reference-mass-fractions summarizes the results.

: Mass fractions from reference VTOL UAV database {#tbl:reference-mass-fractions}

| Fraction | Symbol | Min | Max | Mean | Median | Sample size |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Battery | $f_\text{batt}$ | 0.36 | 0.40 | 0.38 | 0.38 | 3 |
| Payload | $f_\text{payload}$ | 0.10 | 0.30 | 0.20 | 0.21 | 9 |
| Empty | $f_\text{empty}$ | 0.25 | 0.27 | 0.26 | 0.26 | 2 |
| Propulsion | $f_\text{prop}$ | 0.09 | 0.10 | 0.10 | 0.10 | 2 |

The reference data analysis reveals several patterns. Commercial VTOL UAVs allocate approximately 36-40% of MTOW to batteries, reflecting the energy demands of both hover and cruise flight phases. Payload fraction shows wide variation (10-30%) depending on mission focus: endurance-optimized designs exhibit lower payload fractions (approximately 10%), while heavy-lift designs achieve up to 30%. Limited data exists for empty fraction (only two UAVs with unambiguous empty weight definitions), with observed values of 25-27%; however, Mars-specific factors will increase this significantly. For propulsion fraction, motors-only data is available (9-10%), while complete propulsion systems (motors, ESCs, propellers) are estimated at 12-18%.

### Recommended design values

Based on the reference data analysis and Mars mission requirements, the following mass fractions are adopted for initial sizing:

: Recommended mass fractions for Mars UAV initial sizing {#tbl:design-mass-fractions}

| Fraction | Symbol | Value | Range | Rationale |
|---|:---:|:---:|:---:|---|
| Battery | $f_\text{batt}$ | 0.35 | 0.30-0.40 | High endurance requirement; Mars thermal constraints |
| Payload | $f_\text{payload}$ | 0.10 | 0.08-0.15 | Conservative allocation for camera and radio relay |
| Empty | $f_\text{empty}$ | 0.30 | 0.25-0.35 | Includes thermal management, dust protection, structural margins |
| Propulsion | $f_\text{prop}$ | 0.20 | 0.15-0.25 | Redundant dual propulsion system (lift + cruise) |
| Avionics | $f_\text{avionics}$ | 0.05 | 0.03-0.07 | Standard estimate with Mars-specific sensors |

The propulsion fraction is higher than commercial UAV benchmarks due to the need for redundancy in the dual propulsion system (both lift rotors and cruise propellers), operating without possibility of in-flight repair.

The empty fraction accounts for Mars-specific requirements: thermal insulation and active heating systems for the −80 to +20 °C operating environment, dust ingress protection (equivalent to IP55 or higher), potential radiation-tolerant component selection, and structural margins for thermal cycling fatigue.

### MTOW baseline estimate

Using the payload fraction method from @eq:mtow-from-payload with:

* Payload mass: $m_\text{payload}$ = 1.0 kg
* Payload fraction: $f_\text{payload}$ = 0.10 (from @tbl:design-mass-fractions)

The payload mass estimate of 1.0 kg is derived from a conservative assumption for the combined payload: a compact RGB camera system (approximately 400 g based on the survey in @sec:camera-survey), an enclosed radio module (approximately 170 g based on @sec:radio-survey), redundancy allowance for the radio relay mission, and safety margin for mounting hardware and thermal protection.

$$MTOW = \frac{1.0}{0.10} = 10 \text{ kg}$$

The sensitivity to payload fraction selection:

: Sensitivity of MTOW estimate to payload fraction {#tbl:mtow-sensitivity}

| Payload fraction | MTOW estimate |
|:---:|---:|
| 0.08 | 12.5 kg |
| 0.10 | 10.0 kg |
| 0.15 | 6.7 kg |

A baseline MTOW of 10 kg is adopted for initial sizing. This value will be refined through the constraint analysis in @sec:constraint-analysis, where power requirements, wing loading, and endurance constraints are evaluated simultaneously.

The payload mass of 1.00 kg is a fixed mission constraint derived from the selected camera and radio relay components (@sec:payload-systems). This payload-driven sizing ensures that the mission payload requirement is satisfied by construction. Any configuration that cannot carry 1.00 kg within the 10.00 kg MTOW envelope is infeasible.

### Mass fraction validation

The recommended fractions sum to unity:

$$f_\text{batt} + f_\text{payload} + f_\text{empty} + f_\text{prop} + f_\text{avionics} = 0.35 + 0.10 + 0.30 + 0.20 + 0.05 = 1.00$$

The fractions are self-consistent, with the reduced empty fraction (compared to initial estimates) compensated by increased propulsion allocation for redundancy. This allocation reflects the hybrid VTOL architecture where both lift and cruise propulsion systems must be sized for reliability.

The detailed component weight estimation methodology, using semi-empirical equations adapted for Mars conditions, is presented in @sec:mass-breakdown after the constraint analysis determines the required geometry.
