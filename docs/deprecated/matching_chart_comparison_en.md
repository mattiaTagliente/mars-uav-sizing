# Comprehensive Comparison: Regional Jet Matching Charts vs. Mars UAV Design

**Document:** Methodology comparison and adaptation guide  
**Date:** 2025-12-23  
**Reference script:** `C:\Users\matti\OneDrive - Politecnico di Bari\5.5 IELTS\progettazione\Profilo\matchingcharts.m`

---

## 1. Function of the Original Script

### Purpose

The `matchingcharts.m` script performs **simultaneous constraint-based sizing** for a **100-passenger regional jet** by solving a system of 5 nonlinear equations that couple:

1. **Weight balance** (mass closure)
2. **Take-off constraint** (runway length)
3. **Landing constraint** (runway length)
4. **Cruise constraint** (thrust for level flight)
5. **Range constraint** (Breguet equation)

The script uses MATLAB's `fsolve` with the Levenberg-Marquardt algorithm to find the design point where all constraints are simultaneously satisfied.

### Key Characteristics

- **Aircraft type**: Conventional turbofan regional jet
- **Passengers**: 100 (npax = 100)
- **Propulsion**: Jet engine (thrust-based, fuel-burning)
- **Configuration**: Conventional (no VTOL)
- **Operating environment**: Earth (sea level + cruise altitude)

---

## 2. Inputs and Outputs

### Input Parameters (Fixed Constants)

| Category | Parameter | Symbol | Value | Description |
|----------|-----------|--------|-------|-------------|
| **Passengers** | Passenger count | `npax` | 100 | Design payload |
| **Geometry** | Fuselage length | `Lfus` | 36.0 m | Total length |
| | Fuselage radius | `Rfuso` | 1.46 m | Cross-section |
| | Taper ratio | `lambda_taper` | 0.4 | Wing planform |
| | Sweep angle | `sweep25_deg` | 25° | At 25% chord |
| | Thickness ratio | `tc` | 0.14 | Relative thickness |
| **Aerodynamics** | $C_{L,max}$ (TO) | `Clmaxto` | 2.3 | With high-lift devices |
| | Oswald factor | `osw` | 0.93 | Span efficiency |
| | Mach number | `M` | 0.7 | Cruise |
| **Performance** | Cruise speed | `V` | 221.2 m/s | At Mach 0.7 |
| | Range | `A` | 1852 km | 1000 nm |
| | Take-off length | `Lto` | 1400 m | Runway |
| | Landing length | `Lland` | 1250 m | Runway |
| | Deceleration | `abb` | 1.9 m/s² | Braking |
| **Atmosphere** | TO density | `rhoto` | 1.225 kg/m³ | Sea level |
| | Cruise density | `rho` | 0.6527 kg/m³ | ~6 km altitude |
| | Kinematic viscosity | `nu` | 2.44×10⁻⁵ m²/s | |
| **Propulsion** | Throttle factor | `zeta` | 0.685 | Full thrust fraction |
| | Altitude correction | `psi` | 0.5951 | Pressure/temp ratio |
| | SFC base | `cs0` | 0.7/3600 kg/N/s | Specific fuel consumption |
| **Loads** | Ultimate load factor | `Nult` | 5.7 (1.5×3.8) | CS-25 certification |

### Optimization Variables (Solved)

| Variable | Symbol | Initial Guess | Description |
|----------|--------|---------------|-------------|
| **Weight** | `W` | 445,000 N | Total weight |
| **Wing loading** | `S_W` | ~5200 N/m² | W/S |
| **Thrust loading** | `T_S` | ~1675 N/m² | T/S |
| **Aspect ratio** | `lam` | 9.17 | Bounded [6, 12] |
| **Fuel fraction** | `k` | 0.35 | Wf/W |

### Outputs (Results)

| Output | Symbol | Unit | Description |
|--------|--------|------|-------------|
| Wing area | `S` | m² | S = (W/S) × W |
| Wingspan | `b` | m | √(S × λ) |
| MAC | `c` | m | Mean aerodynamic chord |
| Total thrust | `T` | N | T = (T/S) × S |
| Cruise $C_L$ | `Cl` | — | Level flight lift coefficient |
| Cruise $C_D$ | `Cd` | — | From drag polar |
| L/D | `Eff` | — | Aerodynamic efficiency |

---

## 3. The Five Constraint Equations

### Equation 1: Weight Balance

```matlab
equ1 = (Qala + Qfus + Qimp + Qcarr + Qmot + Qfisso + Qf + Qimpianti)*g - W == 0;
```

Sum of component masses equals MTOW:
$$W = g \cdot (m_{wing} + m_{fus} + m_{tail} + m_{gear} + m_{engine} + m_{fixed} + m_{fuel} + m_{systems})$$

### Equation 2: Take-off Constraint

$$\frac{T}{S} = \left(\frac{W}{S}\right)^2 \cdot \frac{1.75}{g \cdot C_{L,max} \cdot x_{fr} \cdot L_{TO} \cdot \rho_{TO}}$$

### Equation 3: Landing Constraint

$$\frac{W}{S} = \frac{L_{land}}{1.66} \cdot a_{braking} \cdot \rho \cdot C_{L,max} \cdot (1 - a \cdot k_{fuel})$$

### Equation 4: Cruise Constraint

$$\frac{T}{S} = \frac{1}{\psi \cdot \zeta} \cdot \frac{1}{2} \rho V^2 C_D$$

### Equation 5: Range (Breguet) Constraint

$$R = \frac{V}{c_s} \cdot \frac{L}{D} \cdot \ln\left(\frac{1}{1 - a \cdot k_{fuel}}\right)$$

---

## 4. Comparison with Mars UAV Design

### 4.1 Input Availability

| Input Category | Regional Jet | Mars UAV | Available? | Notes |
|----------------|--------------|----------|------------|-------|
| **Payload** | 100 pax (~10,000 kg) | 0.5 kg camera | ✅ Different | Much simpler for UAV |
| **Fuselage geometry** | Lfus=36m, R=1.46m | ~1.5m length | ✅ Different | Orders of magnitude smaller |
| **Wing geometry** | λ=6-12, Λ=25°, t/c=0.14 | λ=10-14, Λ=0°, t/c=0.10 | ✅ Adaptable | High AR needed for Mars |
| **$C_{L,max}$** | 2.3 (with flaps) | 1.2-1.4 (clean, low Re) | ✅ Different | Low-Re airfoils, no flaps |
| **Cruise speed** | 221.2 m/s | 35-40 m/s | ✅ Different | Much slower |
| **Range** | 1852 km | 10-50 km | ✅ Different | Local missions |
| **TO length** | 1400 m | N/A (VTOL) | ❌ **Not applicable** | No runway on Mars |
| **Landing length** | 1250 m | N/A (VTOL) | ❌ **Not applicable** | No runway on Mars |
| **Atmosphere ρ** | 1.225 / 0.6527 kg/m³ | 0.020 kg/m³ | ✅ Different | 60× thinner |
| **Gravity** | 9.81 m/s² | 3.711 m/s² | ✅ Different | 38% of Earth |
| **SFC** | 0.7 kg/N/h | N/A (electric) | ❌ **Not applicable** | Battery, not fuel |

### 4.2 Output Requirements

| Output | Regional Jet | Mars UAV | Needed? |
|--------|--------------|----------|---------|
| **Total Weight W** | ✅ Yes | ✅ Yes | ✅ Same |
| **Wing Loading W/S** | ✅ Yes | ✅ Yes | ✅ Same |
| **Thrust Loading T/S** | ✅ Yes | ⚠️ Power Loading P/W | ⚠️ Different |
| **Fuel Fraction k** | ✅ Yes | ⚠️ Battery Fraction | ⚠️ Different |

### 4.3 Variable Transformations

The following variables require transformation from the regional jet formulation to the electric UAV formulation:

| Regional Jet Variable | Symbol | Mars UAV Variable | Symbol | Transformation |
|-----------------------|--------|-------------------|--------|----------------|
| Thrust loading | `T_S` [N/m²] | Power loading | `P_W` [W/N] | P = T × V / η_prop |
| Fuel fraction | `k` [-] | Battery fraction | `f_batt` [-] | No mass reduction during flight |
| Specific fuel consumption | `cs` [kg/N/s] | Specific energy | `e_spec` [Wh/kg] | Energy-based, not mass-flow |
| Altitude/throttle factors | `psi, zeta` [-] | Propulsion efficiencies | `η_prop, η_motor` [-] | Efficiency-based |
| Cruise thrust | `T` [N] | Cruise power | `P_cruise` [W] | P = D × V / η_prop |
| N/A | — | Hover power | `P_hover` [W] | From momentum theory |

### 4.4 Mass Term Mapping (Q Terms)

The original script uses Q terms for component masses. Here is how they map to the Mars UAV:

| Regional Jet Term | Description | Mars UAV Equivalent | Notes |
|-------------------|-------------|---------------------|-------|
| `Qala` | Wing mass | Wing structure | Sadraey formula with adjusted K_rho |
| `Qfus` | Fuselage mass | Fuselage + tail boom | Scaled to smaller size |
| `Qimp` | Empennage (tail surfaces) | Tail surfaces | Similar formula, smaller scale |
| `Qcarr` | Landing gear | **Landing gear/legs** | UAV needs landing legs for VTOL |
| `Qmot` | Jet engines | **Motors + ESCs + propellers + Motor arms/mounts** | All propulsion components |
| `Qimpianti` | Systems/equipment | Avionics + thermal management | ~5-8% of MTOW |
| `Qfisso` | Fixed/payload | Payload (camera, radio) | 0.5 kg fixed |
| `Qf` | Fuel | **Battery + mounting** | Fixed mass during flight |

**Key difference**: In the regional jet, `Qmot` only includes engine mass. For the UAV, `Qmot` should include:
- Lift motors (8×)
- Cruise motors (2×)
- ESCs (all 10)
- Propellers (10 total: 8 lift + 2 cruise)
- Wiring and connectors
- Motor arms/mounts

Similarly, `Qf` (fuel→battery) should include battery mounting hardware and thermal interface materials. 

---

## 5. Required Changes and Adaptations

### 5.1 Lift vs. Cruise Propulsion: Separate Treatment Required

For a QuadPlane configuration, the lift and cruise propulsion systems are **fundamentally different** and must be treated separately:

| Aspect | Lift Propulsion | Cruise Propulsion |
|--------|----------------|-------------------|
| **Function** | Vertical takeoff/landing | Forward flight |
| **Motor type** | High-torque, low-KV | High-efficiency, medium-KV |
| **Operating time** | 2-3 minutes per flight | 60-90 minutes per flight |
| **Sizing constraint** | Hover power (momentum theory) | Cruise drag (L/D) |
| **Number of units** | 8 motors (octocopter) | 2 motors (coaxial tractor) |
| **Propeller type** | Fixed-pitch, small diameter | Variable/fixed, large diameter |
| **Disk loading** | 100-150 N/m² (efficiency) | N/A (thrust-based sizing) |

#### New Variables for Lift Propulsion

| Variable | Symbol | Typical Value | Source |
|----------|--------|---------------|--------|
| Disk loading | $DL$ | 100-150 N/m² | Momentum theory optimization |
| Number of lift rotors | $n_{lift}$ | 8 | Octocopter for redundancy |
| Lift rotor diameter | $D_{lift}$ | 0.22-0.27 m | From DL and weight |
| Figure of merit | $FM$ | 0.6-0.7 | Small rotor efficiency [@johnsonMarsScienceHelicopter2020] |
| Lift motor power (each) | $P_{lift}$ | 450-600 W | From hover power / n_lift |
| Lift motor mass (each) | $m_{motor,lift}$ | 0.15-0.25 kg | Motor datasheets |

#### New Variables for Cruise Propulsion

| Variable | Symbol | Typical Value | Source |
|----------|--------|---------------|--------|
| Number of cruise motors | $n_{cruise}$ | 2 | Coaxial tractor redundancy |
| Cruise propeller diameter | $D_{cruise}$ | 0.6-0.8 m | Scaled from references |
| Propeller efficiency | $\eta_{prop}$ | 0.50-0.65 | Low-Re Mars conditions |
| Cruise motor power (each) | $P_{cruise}$ | 180-210 W | From drag at V_cruise |
| Cruise motor mass (each) | $m_{motor,cruise}$ | 0.3-0.5 kg | Motor datasheets |

### 5.2 Mass Fraction Estimates with Sources

The following mass fractions are derived from literature and reference data:

#### Structure and Airframe

| Component | Fraction of MTOW | Source |
|-----------|------------------|--------|
| Wing structure | 10-15% | Raymer, adapted for UAV [@sadraeyAircraftDesignSystematic2013] |
| Fuselage + tail boom | 8-12% | Small UAV statistical data |
| Motor arms/mounts | 3-5% | QuadPlane structures |
| Landing gear (legs/skids) | 2-4% | Required for VTOL ground operations |
| **Total structure** | **23-35%** | Consistent with 28% for powered-lift eVTOL [NLR study] |

*Note: For small UAVs (MTOW < 50 kg), empty weight fraction of 40-60% is typical, of which structure comprises roughly half. The landing gear is essential for VTOL operations and cannot be omitted.*

#### Propulsion System

| Component | Fraction of MTOW | Source |
|-----------|------------------|--------|
| Lift motors (8×) | 5-8% | From reference UAV data: 9-10% total motors |
| Cruise motors (2×) | 2-4% | From reference UAV data |
| ESCs | 1-2% | Approximately 15-25% of motor mass [@oscarliang_esc] |
| Propellers | 1-2% | Foam-core composite blades ~28g each [@nasa_ingenuity] |
| Wiring/connectors | 0.5-1% | Wire gauge tables: 14-20 AWG, length-dependent |
| **Total propulsion** | **10-15%** | |

*ESC mass estimate: Modern 4-in-1 ESCs weigh 12-15g for small drones; larger discrete ESCs 40-60g each. For 8 lift + 2 cruise motors with 50g average ESC, total ~500g ≈ 4% of 12 kg MTOW. Conservative estimate: 1-2% of MTOW.*

#### Energy Storage

| Component | Fraction of MTOW | Source |
|-----------|------------------|--------|
| Battery pack | 29-40% | Reference UAV data (see sources/reference_drones.yaml) |
| Battery mounting | 1-2% | Vibration isolation, thermal interface |
| **Total energy** | **30-42%** | |

*Reference: Ingenuity battery = 273g / 1800g = 15.2% of MTOW. However, Ingenuity is solar-recharged with minimal endurance. For 60-90 min cruise endurance, higher fractions (30-40%) are necessary.*

#### Avionics and Systems

| Component | Fraction of MTOW | Source |
|-----------|------------------|--------|
| Flight controller + IMU | 0.5-1% | ~50-100g for commercial autopilots |
| GPS/navigation | 0.3-0.5% | ~30-50g |
| Radio/telemetry | 0.5-1% | Including antennas |
| Sensors (additional) | 0.3-0.5% | Temperature, pressure, etc. |
| Thermal management | 1-3% | Heaters for Mars conditions |
| **Total avionics/systems** | **3-6%** | |

*Note: For UAM eVTOL, avionics can be 27-68% of non-structural system weight [TE Connectivity study]. For simpler UAVs, 3-6% of MTOW is reasonable.*

#### Summary Mass Budget (Mapped to Q Terms)

| Category | Q Term | Fraction of MTOW | For 12 kg UAV |
|----------|--------|------------------|---------------|
| Wing structure | Qala | 12% | 1.44 kg |
| Fuselage + tail | Qfus | 8% | 0.96 kg |
| Tail surfaces | Qimp | 3% | 0.36 kg |
| Landing gear | Qcarr | 3% | 0.36 kg |
| Propulsion (motors, ESCs, props, wiring) | Qmot | 12% | 1.44 kg |
| Avionics + thermal | Qimpianti | 5% | 0.60 kg |
| Payload | Qfisso | 4% | 0.50 kg |
| Battery + mounting | Qf | 36% | 4.32 kg |
| **Margin** | — | **17%** | **2.02 kg** |
| **Total** | — | **100%** | **12.0 kg** |

### 5.3 Complete Equation Replacements

#### ❌ REMOVE: Take-off Runway Constraint

**Reason**: Mars UAV uses VTOL; there is no runway.

✅ **REPLACE WITH: Hover Power Constraint**

From momentum theory:
$$P_{hover} = \frac{W^{3/2}}{FM \cdot \eta_{motor} \cdot \sqrt{2 \rho_{Mars} A_{disk}}}$$

Where $A_{disk} = n_{lift} \cdot \pi (D_{lift}/2)^2$

#### ❌ REMOVE: Landing Runway Constraint

**Reason**: No runway landing.

✅ **REPLACE WITH: Stall Constraint**

$$\left(\frac{W}{S}\right)_{max} = \frac{1}{2} \rho_{Mars} V_{stall}^2 C_{L,max}$$

#### ❌ REMOVE: Breguet Range Constraint

**Reason**: Electric aircraft; battery mass doesn't reduce during flight.

✅ **REPLACE WITH: Battery Energy Constraint**

$$E_{battery} = m_{batt} \cdot e_{specific} \cdot \eta_{discharge} \cdot DoD$$
$$E_{required} = (P_{hover} \cdot t_{hover} + P_{cruise} \cdot t_{cruise}) \cdot reserve$$

#### ⚠️ MODIFY: Cruise Constraint

From thrust to power:
$$\frac{P}{W} = \frac{V_{cruise}}{\eta_{prop}} \cdot \frac{C_D}{C_L}$$

### 5.4 Atmospheric Model Changes

| Parameter | Regional Jet | Mars UAV | Factor |
|-----------|--------------|----------|--------|
| Surface density | 1.225 kg/m³ | 0.020 kg/m³ | 1/61 |
| Gravity | 9.81 m/s² | 3.711 m/s² | 0.38 |
| Speed of sound | 340 m/s | 240 m/s | 0.71 |
| Kinematic viscosity | 1.5×10⁻⁵ m²/s | 5×10⁻⁴ m²/s | 33× |

### 5.5 New Variables Needed (Not in Original Script)

The following variables are required for the Mars UAV but have no equivalent in the regional jet script:

| New Variable | Symbol | Typical Value | Unit | Purpose |
|--------------|--------|---------------|------|----------|
| **Disk loading** | `DL` | 100-150 | N/m² | Hover rotor sizing (efficiency trade-off) |
| **Number of lift rotors** | `n_rot` | 8 | — | Hover configuration (octocopter) |
| **Lift rotor diameter** | `D_rot` | 0.22-0.27 | m | From DL and weight |
| **Figure of merit** | `FM` | 0.60-0.70 | — | Rotor efficiency factor |
| **Number of cruise motors** | `n_cruise` | 2 | — | Coaxial tractor configuration |
| **Cruise propeller diameter** | `D_cruise` | 0.6-0.8 | m | Sized for thrust at cruise |
| **Lift motor specific power** | `P/m_lift` | 4000-6000 | W/kg | Motor technology level |
| **Cruise motor specific power** | `P/m_cruise` | 3000-5000 | W/kg | Motor technology level |
| **Battery specific energy** | `e_spec` | 150-270 | Wh/kg | Battery technology level |
| **Depth of discharge** | `DoD` | 0.80-0.90 | — | Usable battery capacity |
| **Hover time** | `t_hover` | 90-180 | s | Mission profile: takeoff + landing |
| **Cruise time** | `t_cruise` | 3600-5400 | s | Mission profile: 60-90 min |
| **Propeller efficiency (cruise)** | `η_prop` | 0.50-0.65 | — | Low-Re Mars conditions |
| **Motor efficiency** | `η_motor` | 0.82-0.88 | — | Electric motor |
| **ESC efficiency** | `η_ESC` | 0.95-0.98 | — | Power electronics |
| **Mars gravity** | `g_Mars` | 3.711 | m/s² | Constant |
| **Mars density (Arcadia)** | `ρ_Mars` | 0.020 | kg/m³ | At -3 km elevation |
| **Mars dynamic viscosity** | `μ_Mars` | 1.0×10⁻⁵ | Pa·s | CO₂ at ~220 K |

---

## 6. Proposed Mars UAV Constraint System

### New System of Equations

**Unknowns**: W (weight), S (wing area), P_lift (hover power), P_cruise (cruise power), m_batt (battery mass), λ (aspect ratio)

```
Equation 1: Hover power constraint (from momentum theory)
Equation 2: Cruise power constraint (from drag polar)  
Equation 3: Stall constraint (maximum wing loading)
Equation 4: Energy constraint (battery capacity vs. mission energy)
Equation 5: Mass balance (component masses sum to MTOW)
```

---

## 7. Summary of Required Adaptations

### Must Change (Fundamental Differences)

| Aspect | From | To | Reason |
|--------|------|-----|--------|
| **Take-off constraint** | Runway length | Hover power | VTOL |
| **Landing constraint** | Runway length | Stall speed | VTOL + fixed-wing cruise |
| **Range equation** | Breguet fuel | Battery energy | Electric propulsion |
| **Thrust → Power** | T/S [N/m²] | P/W [W/N] | Electric uses power |
| **Propulsion model** | SFC, bypass ratio | η_motor, η_prop | Efficiency-based |
| **Fuel fraction** | Diminishes with flight | Fixed battery mass | No mass change |

### Can Adapt (Same Concept, Different Values)

| Aspect | Regional Jet | Mars UAV |
|--------|--------------|----------|
| **Weight balance** | Component sum | Component sum (different components) |
| **Cruise constraint** | Thrust = Drag | Power = Drag × V / η |
| **Drag polar** | CD0 + kCL² | CD0 + kCL² (different values) |
| **Optimization solver** | fsolve, Levenberg-Marquardt | Same approach works |

### New Additions Required

| New Element | Purpose |
|-------------|---------|
| **Hover constraint** | Size lift rotors |
| **Separate lift/cruise sizing** | QuadPlane configuration |
| **Disk loading** | Rotor efficiency trade-off |
| **Battery energy model** | Replace fuel burn |
| **Mars atmosphere model** | ρ, g, μ |

---

## 8. Conclusion

The original regional jet `matchingcharts.m` script provides an **excellent methodological template** but requires **substantial adaptation** for the Mars UAV:

1. **2 of 5 constraints must be completely replaced** (take-off → hover, landing → stall)
2. **1 constraint must be fundamentally changed** (Breguet → battery energy)
3. **2 constraints can be adapted** (cruise, mass balance)
4. **Lift and cruise propulsion must be treated separately** for QuadPlane configuration
5. **All parameter values** must be updated for Mars conditions
6. **Mass fractions** require specific sources (provided above)

The iterative solver approach and the concept of simultaneous constraint satisfaction remain valid. The adaptation is significant enough that a **new Mars-specific script** should be written, inspired by the original.

---

## References

- Johnson, W. et al. (2020). "Mars Science Helicopter Conceptual Design." NASA/TM-2020-220485.
- Sadraey, M.H. (2013). "Aircraft Design: A Systems Engineering Approach." Wiley.
- Raymer, D.P. (2018). "Aircraft Design: A Conceptual Approach." AIAA Education Series.
- Barbato, G. et al. (2024). "Preliminary Design of a Fixed-Wing Drone for Mars Exploration." ICAS 2024.
- NASA Ingenuity Mars Helicopter fact sheet. mars.nasa.gov/technology/helicopter.
