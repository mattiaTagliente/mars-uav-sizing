#!/usr/bin/env python3
"""
Section 4: Initial Design Hypotheses - Calculation Script

This script computes all design parameters for Section 4 of the Mars UAV 
feasibility study. All calculations are based on grounded sources and 
first-principles physics.

References:
- Momentum theory: Prouty (2002), Johnson et al. (2020)
- Mars atmosphere: NASA/GRC Mars Atmosphere Model
- Battery specifications: CGBT SLD1-6S27Ah solid-state Li-Ion
- Aircraft design: Roskam (2004, 2005), Sadraey (2013)
"""

import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class MarsAtmosphere:
    """Mars atmospheric conditions at Arcadia Planitia (-3 km elevation)."""
    density: float = 0.020  # kg/m³
    gravity: float = 3.711  # m/s²
    dynamic_viscosity: float = 1.2e-5  # Pa·s (CO2 at ~220 K)
    speed_of_sound: float = 240  # m/s


@dataclass
class EarthAtmosphere:
    """Earth sea-level atmospheric conditions (ISA)."""
    density: float = 1.225  # kg/m³
    gravity: float = 9.81  # m/s²
    dynamic_viscosity: float = 1.789e-5  # Pa·s
    speed_of_sound: float = 340  # m/s


@dataclass
class BatterySpecs:
    """Solid-state Li-Ion battery specifications.
    
    Source: CGBT SLD1-6S27Ah specifications
    """
    specific_energy: float = 270  # Wh/kg
    depth_of_discharge: float = 0.80  # 80% DoD for optimal cycle life
    discharge_efficiency: float = 0.95  # Round-trip efficiency
    operating_temp_min: float = -20  # °C
    operating_temp_max: float = 60  # °C
    cycle_life: int = 1000  # cycles at 80% DoD


@dataclass
class PropulsionEfficiency:
    """Propulsion system efficiency parameters.
    
    Sources: 
    - Motor efficiency: Industry typical for BLDC motors at peak operation
    - Propeller efficiency: Bertani (2023), scaled for low-Re Mars conditions
    - ESC efficiency: Industry typical for high-quality ESCs
    """
    motor_efficiency: float = 0.85  # η_motor
    esc_efficiency: float = 0.95  # η_ESC
    propeller_efficiency_cruise: float = 0.55  # η_prop at Mars (low Re)
    propeller_efficiency_earth: float = 0.75  # η_prop at Earth (reference)
    figure_of_merit: float = 0.65  # FM for small rotors


# ============================================================================
# SECTION 4.3: MTOW CALCULATION
# ============================================================================

def calculate_mars_weight(mass_kg: float, mars: MarsAtmosphere) -> float:
    """Calculate weight on Mars given mass."""
    return mass_kg * mars.gravity


# ============================================================================
# SECTION 4.4: WING GEOMETRY
# ============================================================================

def calculate_wing_area_ratio(
    v_mars: float, 
    v_earth: float,
    mars: MarsAtmosphere = MarsAtmosphere(),
    earth: EarthAtmosphere = EarthAtmosphere()
) -> float:
    """
    Calculate wing area ratio between Mars and Earth.
    
    From @eq:area-ratio:
    S_Mars/S_Earth = (g_Mars/g_Earth) × (ρ_Earth/ρ_Mars) × (V_Earth/V_Mars)²
    """
    gravity_ratio = mars.gravity / earth.gravity
    density_ratio = earth.density / mars.density
    speed_ratio_squared = (v_earth / v_mars) ** 2
    
    return gravity_ratio * density_ratio * speed_ratio_squared


def calculate_wingspan_from_area_ar(wing_area: float, aspect_ratio: float) -> float:
    """Calculate wingspan from wing area and aspect ratio."""
    return math.sqrt(wing_area * aspect_ratio)


def calculate_mean_chord(wing_area: float, wingspan: float) -> float:
    """Calculate mean aerodynamic chord from wing area and span."""
    return wing_area / wingspan


def calculate_reynolds_number(
    velocity: float, 
    chord: float, 
    mars: MarsAtmosphere = MarsAtmosphere()
) -> float:
    """Calculate Reynolds number for given conditions."""
    return (mars.density * velocity * chord) / mars.dynamic_viscosity


# ============================================================================
# SECTION 4.5: TAIL GEOMETRY
# ============================================================================

def calculate_tail_volume_coefficients(
    vh_baseline: float = 0.36,
    vv_baseline: float = 0.028,
    mars_increase_factor: float = 1.25
) -> Tuple[float, float]:
    """
    Calculate tail volume coefficients with Mars-specific increase.
    
    Baseline values from Roskam (2004) for small aircraft.
    25% increase for reduced control effectiveness at low Reynolds numbers.
    """
    vh_mars = vh_baseline * mars_increase_factor
    vv_mars = vv_baseline * mars_increase_factor
    return vh_mars, vv_mars


def calculate_horizontal_tail_area(
    vh: float,
    wing_area: float,
    mac: float,
    moment_arm: float
) -> float:
    """
    Calculate required horizontal tail area from volume coefficient.
    
    V_H = S_H × l_H / (S × c̄)
    S_H = V_H × S × c̄ / l_H
    """
    return vh * wing_area * mac / moment_arm


def calculate_vertical_tail_area(
    vv: float,
    wing_area: float,
    wingspan: float,
    moment_arm: float
) -> float:
    """
    Calculate required vertical tail area from volume coefficient.
    
    V_V = S_V × l_V / (S × b)
    S_V = V_V × S × b / l_V
    """
    return vv * wing_area * wingspan / moment_arm


def calculate_vtail_geometry(
    sh_required: float,
    sv_required: float,
    dihedral_deg: float = 40.0,
    aspect_ratio: float = 4.0
) -> dict:
    """
    Calculate V-tail geometry from required projected areas.
    
    For inverted V-tail:
    S_H = S_Vtail × cos²(Γ)
    S_V = S_Vtail × sin²(Γ)
    
    Returns dict with all geometric parameters.
    """
    dihedral_rad = math.radians(dihedral_deg)
    cos2_gamma = math.cos(dihedral_rad) ** 2
    sin2_gamma = math.sin(dihedral_rad) ** 2
    
    # Calculate total V-tail area from horizontal requirement
    s_vtail_from_h = sh_required / cos2_gamma
    # Also calculate from vertical requirement for comparison
    s_vtail_from_v = sv_required / sin2_gamma
    
    # Use the larger to satisfy both requirements
    s_vtail_total = max(s_vtail_from_h, s_vtail_from_v)
    s_per_surface = s_vtail_total / 2
    
    # Calculate dimensions
    span_per_surface = math.sqrt(aspect_ratio * s_per_surface)
    chord = s_per_surface / span_per_surface
    
    return {
        's_vtail_total': s_vtail_total,
        's_per_surface': s_per_surface,
        'dihedral_deg': dihedral_deg,
        'span_per_surface': span_per_surface,
        'chord': chord,
        'aspect_ratio': aspect_ratio,
        'actual_sh': s_vtail_total * cos2_gamma,
        'actual_sv': s_vtail_total * sin2_gamma
    }


# ============================================================================
# SECTION 4.6: FUSELAGE GEOMETRY
# ============================================================================

def calculate_fuselage_length_from_ratio(
    wingspan: float,
    length_to_span_ratio: float = 0.50
) -> float:
    """
    Calculate fuselage length from wingspan and ratio.
    
    Based on commercial VTOL UAV benchmarks, median ratio is ~0.50.
    """
    return length_to_span_ratio * wingspan


def calculate_fuselage_wetted_area(
    length: float,
    width: float,
    height: float
) -> float:
    """
    Estimate fuselage wetted area approximating as ellipsoid.
    
    S_wet ≈ π × a × b × [1 + e²/6 + 3e⁴/40 + ...]
    For ellipsoid with semi-axes a, b, c.
    
    Simplified: treat as prolate spheroid.
    """
    # For prolate spheroid with major axis = length/2, minor = (width+height)/4
    a = length / 2  # Semi-major axis
    b = (width + height) / 4  # Average semi-minor axis
    
    # Eccentricity for prolate spheroid
    if a > b:
        e = math.sqrt(1 - (b/a)**2)
        # Surface area formula for prolate spheroid
        s_wet = 2 * math.pi * b**2 * (1 + (a/(b*e)) * math.asin(e))
    else:
        s_wet = 4 * math.pi * a * b  # Sphere approximation
    
    return s_wet


# ============================================================================
# SECTION 4.7: PROPULSION SIZING
# ============================================================================

def calculate_hover_power_ideal(
    thrust: float,
    rotor_area: float,
    density: float
) -> float:
    """
    Calculate ideal hover power from momentum theory.
    
    Canonical form (Prouty 2002, Johnson et al. 2020):
    P_ideal = T^1.5 / √(2ρA)
    
    This is the induced power only, without losses.
    """
    return thrust ** 1.5 / math.sqrt(2 * density * rotor_area)


def calculate_hover_power_actual(
    thrust: float,
    rotor_area: float,
    density: float,
    figure_of_merit: float = 0.65,
    motor_efficiency: float = 0.85,
    esc_efficiency: float = 0.95
) -> float:
    """
    Calculate actual electrical hover power including losses.
    
    P_actual = P_ideal / (FM × η_motor × η_ESC)
    
    The figure of merit (FM) accounts for profile drag and non-ideal effects.
    Typical FM for small rotors: 0.6-0.7 (Johnson et al. 2020)
    """
    p_ideal = calculate_hover_power_ideal(thrust, rotor_area, density)
    return p_ideal / (figure_of_merit * motor_efficiency * esc_efficiency)


def calculate_disk_loading(thrust: float, rotor_area: float) -> float:
    """Calculate disk loading (thrust per rotor disk area)."""
    return thrust / rotor_area


def calculate_rotor_diameter(
    total_thrust: float,
    n_rotors: int,
    target_disk_loading: float
) -> float:
    """
    Calculate individual rotor diameter for target disk loading.
    
    DL = T / A_total
    A_per_rotor = (T / n) / DL
    D = √(4 × A / π)
    """
    area_per_rotor = (total_thrust / n_rotors) / target_disk_loading
    return math.sqrt(4 * area_per_rotor / math.pi)


def calculate_hover_power_per_mass(
    disk_loading: float,
    density: float,
    gravity: float,
    figure_of_merit: float = 0.65,
    motor_efficiency: float = 0.85,
    esc_efficiency: float = 0.95
) -> float:
    """
    Calculate hover power per unit mass.
    
    From momentum theory:
    P/m = g × √(DL / (2ρ)) / (FM × η_motor × η_ESC)
    
    This gives electrical power per kg of aircraft mass.
    """
    # Induced velocity component
    induced_factor = math.sqrt(disk_loading / (2 * density))
    p_per_m_ideal = gravity * induced_factor
    
    return p_per_m_ideal / (figure_of_merit * motor_efficiency * esc_efficiency)


def compare_mars_earth_hover_power(
    mars: MarsAtmosphere = MarsAtmosphere(),
    earth: EarthAtmosphere = EarthAtmosphere(),
    disk_loading: float = 100.0  # N/m²
) -> float:
    """
    Calculate the ratio of Mars to Earth hover power per unit mass.
    
    Returns the factor by which hover power increases from Earth to Mars.
    """
    # Same disk loading on both planets
    
    # Mars: P/m = g_Mars × √(DL / (2ρ_Mars))
    p_mars = mars.gravity * math.sqrt(disk_loading / (2 * mars.density))
    
    # Earth: P/m = g_Earth × √(DL / (2ρ_Earth))
    p_earth = earth.gravity * math.sqrt(disk_loading / (2 * earth.density))
    
    return p_mars / p_earth


# ============================================================================
# SECTION 4.8: CRUISE POWER AND PROPELLER SIZING
# ============================================================================

def calculate_cruise_power(
    weight: float,
    velocity: float,
    lift_to_drag: float,
    propeller_efficiency: float = 0.55,
    motor_efficiency: float = 0.85,
    esc_efficiency: float = 0.95
) -> float:
    """
    Calculate cruise power.
    
    P_cruise = (W × V) / (L/D × η_prop × η_motor × η_ESC)
    """
    total_efficiency = propeller_efficiency * motor_efficiency * esc_efficiency
    return (weight * velocity) / (lift_to_drag * total_efficiency)


def calculate_cruise_thrust(weight: float, lift_to_drag: float) -> float:
    """Calculate required cruise thrust from L/D ratio."""
    return weight / lift_to_drag


# ============================================================================
# SECTION 4.9: ENERGY STORAGE
# ============================================================================

def calculate_battery_energy(
    battery_mass: float,
    specific_energy: float = 270,  # Wh/kg
    depth_of_discharge: float = 0.80,
    discharge_efficiency: float = 0.95
) -> float:
    """
    Calculate usable battery energy.
    
    E_usable = m_batt × e_spec × DoD × η_discharge
    """
    return battery_mass * specific_energy * depth_of_discharge * discharge_efficiency


def calculate_battery_mass_for_mission(
    hover_power: float,
    cruise_power: float,
    hover_time_s: float,
    cruise_time_s: float,
    reserve_factor: float = 1.20,  # 20% reserve
    specific_energy: float = 270,  # Wh/kg
    depth_of_discharge: float = 0.80,
    discharge_efficiency: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate required battery mass for mission profile.
    
    Returns (battery_mass_kg, total_energy_Wh)
    """
    # Convert times to hours
    hover_time_h = hover_time_s / 3600
    cruise_time_h = cruise_time_s / 3600
    
    # Energy required
    e_hover = hover_power * hover_time_h
    e_cruise = cruise_power * cruise_time_h
    e_total = (e_hover + e_cruise) * reserve_factor
    
    # Battery mass
    usable_fraction = depth_of_discharge * discharge_efficiency
    battery_mass = e_total / (specific_energy * usable_fraction)
    
    return battery_mass, e_total


# ============================================================================
# SECTION 4.11: STRUCTURAL MASS
# ============================================================================

def calculate_wing_mass(
    wing_area: float,
    surface_density: float = 1.0  # kg/m² - to be refined
) -> float:
    """Estimate wing structural mass from surface density."""
    return wing_area * surface_density


# ============================================================================
# MAIN CALCULATION ROUTINE
# ============================================================================

def run_section4_calculations():
    """Execute all Section 4 calculations and print results."""
    
    print("=" * 80)
    print("SECTION 4: INITIAL DESIGN HYPOTHESES - CALCULATIONS")
    print("=" * 80)
    
    # Initialize conditions
    mars = MarsAtmosphere()
    earth = EarthAtmosphere()
    battery = BatterySpecs()
    efficiency = PropulsionEfficiency()
    
    # ========================================================================
    # 4.3 TARGET MTOW
    # ========================================================================
    print("\n## 4.3 Target MTOW")
    print("-" * 40)
    
    mtow_kg = 12.0  # Based on scaling from median of references
    weight_mars = calculate_mars_weight(mtow_kg, mars)
    
    print(f"Target MTOW: {mtow_kg:.1f} kg")
    print(f"Mars weight: {weight_mars:.2f} N")
    
    # ========================================================================
    # 4.4 WING GEOMETRY
    # ========================================================================
    print("\n## 4.4 Wing Geometry")
    print("-" * 40)
    
    # Reference data
    v_earth_cruise = 18.0  # m/s (typical commercial UAV)
    v_mars_cruise = 38.0   # m/s (approximately 2× Earth)
    s_earth_baseline = 0.6  # m² (typical for 12 kg Earth UAV)
    aspect_ratio = 12.0
    
    # Wing area ratio calculation
    area_ratio = calculate_wing_area_ratio(v_mars_cruise, v_earth_cruise, mars, earth)
    
    print(f"Earth cruise speed: {v_earth_cruise:.1f} m/s")
    print(f"Mars cruise speed: {v_mars_cruise:.1f} m/s")
    print(f"Gravity ratio (g_Mars/g_Earth): {mars.gravity/earth.gravity:.3f}")
    print(f"Density ratio (ρ_Earth/ρ_Mars): {earth.density/mars.density:.1f}")
    print(f"Speed ratio (V_Earth/V_Mars): {v_earth_cruise/v_mars_cruise:.3f}")
    print(f"Wing area ratio S_Mars/S_Earth: {area_ratio:.2f}")
    
    # Mars wing parameters
    s_mars = s_earth_baseline * area_ratio
    b_mars = calculate_wingspan_from_area_ar(s_mars, aspect_ratio)
    mac = calculate_mean_chord(s_mars, b_mars)
    
    print(f"\nMars wing area: {s_mars:.2f} m²")
    print(f"Mars wingspan: {b_mars:.2f} m")
    print(f"Mean aerodynamic chord: {mac:.2f} m")
    print(f"Aspect ratio: {aspect_ratio:.1f}")
    
    # Reynolds number at wing
    re_wing = calculate_reynolds_number(v_mars_cruise, mac, mars)
    print(f"Reynolds number at wing (cruise): {re_wing:.0f}")
    
    # ========================================================================
    # 4.5 TAIL GEOMETRY
    # ========================================================================
    print("\n## 4.5 Tail Geometry")
    print("-" * 40)
    
    # Tail volume coefficients with Mars increase
    vh, vv = calculate_tail_volume_coefficients(0.36, 0.028, 1.25)
    moment_arm = 2.0  # m (boom-mounted tail)
    
    print(f"Horizontal tail volume coefficient V_H: {vh:.3f}")
    print(f"Vertical tail volume coefficient V_V: {vv:.4f}")
    print(f"Moment arm: {moment_arm:.1f} m")
    
    # Required projected areas
    sh_required = calculate_horizontal_tail_area(vh, s_mars, mac, moment_arm)
    sv_required = calculate_vertical_tail_area(vv, s_mars, b_mars, moment_arm)
    
    print(f"\nRequired horizontal projection S_H: {sh_required:.3f} m²")
    print(f"Required vertical projection S_V: {sv_required:.3f} m²")
    
    # V-tail geometry
    vtail = calculate_vtail_geometry(sh_required, sv_required, 40.0, 4.0)
    
    print(f"\nV-tail total area: {vtail['s_vtail_total']:.3f} m²")
    print(f"Area per surface: {vtail['s_per_surface']:.3f} m²")
    print(f"Dihedral angle: {vtail['dihedral_deg']:.0f}°")
    print(f"Span per surface: {vtail['span_per_surface']:.2f} m")
    print(f"Chord: {vtail['chord']:.2f} m")
    print(f"Actual S_H: {vtail['actual_sh']:.3f} m²")
    print(f"Actual S_V: {vtail['actual_sv']:.3f} m²")
    
    # Tail Reynolds number
    re_tail = calculate_reynolds_number(v_mars_cruise, vtail['chord'], mars)
    print(f"Reynolds number at tail: {re_tail:.0f}")
    
    # ========================================================================
    # 4.6 FUSELAGE GEOMETRY
    # ========================================================================
    print("\n## 4.6 Fuselage Geometry")
    print("-" * 40)
    
    length_span_ratio = 0.50  # From Section 3.3.3 decision
    fuselage_length = calculate_fuselage_length_from_ratio(b_mars, length_span_ratio)
    fuselage_width = 0.30  # m (scaled proportionally)
    fuselage_height = 0.24  # m
    fineness_ratio = fuselage_length / max(fuselage_width, fuselage_height)
    
    print(f"Length/span ratio: {length_span_ratio:.2f}")
    print(f"Fuselage length: {fuselage_length:.2f} m")
    print(f"Fuselage width: {fuselage_width:.2f} m")
    print(f"Fuselage height: {fuselage_height:.2f} m")
    print(f"Fineness ratio: {fineness_ratio:.1f}")
    
    s_wet_fus = calculate_fuselage_wetted_area(fuselage_length, fuselage_width, fuselage_height)
    print(f"Estimated wetted area: {s_wet_fus:.2f} m²")
    
    # ========================================================================
    # 4.7 PROPULSION SIZING
    # ========================================================================
    print("\n## 4.7 Propulsion Sizing")
    print("-" * 40)
    
    # Compare Mars vs Earth hover power
    disk_loading_target = 100.0  # N/m²
    power_ratio = compare_mars_earth_hover_power(mars, earth, disk_loading_target)
    
    print(f"Target disk loading: {disk_loading_target:.0f} N/m²")
    print(f"Mars/Earth hover power ratio: {power_ratio:.2f}×")
    
    # Hover power calculation
    n_lift_rotors = 8
    total_rotor_area = weight_mars / disk_loading_target
    rotor_diameter = calculate_rotor_diameter(weight_mars, n_lift_rotors, disk_loading_target)
    
    print(f"\nNumber of lift rotors: {n_lift_rotors}")
    print(f"Total rotor disk area: {total_rotor_area:.3f} m²")
    print(f"Individual rotor diameter: {rotor_diameter:.3f} m ({rotor_diameter*1000:.0f} mm, {rotor_diameter*39.37:.1f} in)")
    
    # Power calculations
    p_hover_ideal = calculate_hover_power_ideal(weight_mars, total_rotor_area, mars.density)
    p_hover_actual = calculate_hover_power_actual(
        weight_mars, total_rotor_area, mars.density,
        efficiency.figure_of_merit, efficiency.motor_efficiency, efficiency.esc_efficiency
    )
    
    print(f"\nIdeal hover power (momentum theory): {p_hover_ideal:.0f} W")
    print(f"Actual electrical hover power: {p_hover_actual:.0f} W")
    print(f"Hover power per unit mass: {p_hover_actual/mtow_kg:.0f} W/kg")
    print(f"Power per lift motor: {p_hover_actual/n_lift_rotors:.0f} W")
    
    # ========================================================================
    # 4.8 CRUISE POWER
    # ========================================================================
    print("\n## 4.8 Cruise Power")
    print("-" * 40)
    
    lift_to_drag = 15.0  # Target L/D from aerodynamic analysis
    cruise_thrust = calculate_cruise_thrust(weight_mars, lift_to_drag)
    cruise_power = calculate_cruise_power(
        weight_mars, v_mars_cruise, lift_to_drag,
        efficiency.propeller_efficiency_cruise,
        efficiency.motor_efficiency,
        efficiency.esc_efficiency
    )
    
    print(f"Target L/D ratio: {lift_to_drag:.1f}")
    print(f"Cruise thrust required: {cruise_thrust:.2f} N")
    print(f"Cruise power (electrical): {cruise_power:.0f} W")
    print(f"Cruise power per unit mass: {cruise_power/mtow_kg:.1f} W/kg")
    
    n_cruise_motors = 2
    print(f"\nCruise motors: {n_cruise_motors}")
    print(f"Power per cruise motor: {cruise_power/n_cruise_motors:.0f} W")
    
    # Hover to cruise power ratio
    print(f"\nHover/cruise power ratio: {p_hover_actual/cruise_power:.1f}×")
    
    # ========================================================================
    # 4.9 ENERGY STORAGE
    # ========================================================================
    print("\n## 4.9 Energy Storage")
    print("-" * 40)
    
    print(f"Battery technology: Solid-state Li-Ion")
    print(f"Specific energy: {battery.specific_energy:.0f} Wh/kg")
    print(f"Depth of discharge (DoD): {battery.depth_of_discharge*100:.0f}%")
    print(f"Discharge efficiency: {battery.discharge_efficiency*100:.0f}%")
    
    # Mission profile
    hover_time_s = 180  # 3 minutes total (takeoff + landing)
    cruise_time_s = 3600  # 60 minutes
    
    battery_mass, total_energy = calculate_battery_mass_for_mission(
        p_hover_actual, cruise_power, hover_time_s, cruise_time_s,
        reserve_factor=1.20,
        specific_energy=battery.specific_energy,
        depth_of_discharge=battery.depth_of_discharge,
        discharge_efficiency=battery.discharge_efficiency
    )
    
    print(f"\nMission profile:")
    print(f"  Hover time: {hover_time_s:.0f} s ({hover_time_s/60:.1f} min)")
    print(f"  Cruise time: {cruise_time_s:.0f} s ({cruise_time_s/60:.0f} min)")
    print(f"  Reserve: 20%")
    
    print(f"\nEnergy required (with reserve): {total_energy:.0f} Wh")
    print(f"Calculated battery mass: {battery_mass:.2f} kg")
    print(f"Battery fraction: {battery_mass/mtow_kg*100:.1f}%")
    
    # Cross-check with stored energy
    battery_fraction_target = 0.35
    battery_mass_target = mtow_kg * battery_fraction_target
    usable_energy = calculate_battery_energy(
        battery_mass_target,
        battery.specific_energy,
        battery.depth_of_discharge,
        battery.discharge_efficiency
    )
    
    print(f"\nAlternative (35% battery fraction):")
    print(f"  Battery mass: {battery_mass_target:.2f} kg")
    print(f"  Usable energy: {usable_energy:.0f} Wh")
    
    # Endurance calculation
    endurance_cruise_only = usable_energy / cruise_power  # hours
    print(f"  Cruise-only endurance: {endurance_cruise_only*60:.0f} min")
    
    # ========================================================================
    # SUMMARY TABLE
    # ========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY OF CALCULATED PARAMETERS")
    print("=" * 80)
    
    summary = {
        "MTOW": f"{mtow_kg:.0f} kg",
        "Mars weight": f"{weight_mars:.1f} N",
        "Wing area": f"{s_mars:.2f} m²",
        "Wingspan": f"{b_mars:.2f} m",
        "Aspect ratio": f"{aspect_ratio:.0f}",
        "MAC": f"{mac:.3f} m",
        "Cruise speed": f"{v_mars_cruise:.0f} m/s",
        "Wing Reynolds number": f"{re_wing:.0f}",
        "V-tail total area": f"{vtail['s_vtail_total']:.2f} m²",
        "V-tail dihedral": f"{vtail['dihedral_deg']:.0f}°",
        "Tail moment arm": f"{moment_arm:.1f} m",
        "Fuselage length": f"{fuselage_length:.2f} m",
        "Lift rotor diameter": f"{rotor_diameter:.3f} m ({rotor_diameter*39.37:.1f} in)",
        "Disk loading": f"{disk_loading_target:.0f} N/m²",
        "Hover power (electrical)": f"{p_hover_actual:.0f} W",
        "Cruise power (electrical)": f"{cruise_power:.0f} W",
        "Battery mass (calculated)": f"{battery_mass:.2f} kg ({battery_mass/mtow_kg*100:.1f}%)",
        "Battery specific energy": f"{battery.specific_energy:.0f} Wh/kg",
    }
    
    for param, value in summary.items():
        print(f"  {param:30s}: {value}")
    
    return {
        'mtow_kg': mtow_kg,
        'weight_mars': weight_mars,
        's_mars': s_mars,
        'b_mars': b_mars,
        'mac': mac,
        'aspect_ratio': aspect_ratio,
        'v_cruise': v_mars_cruise,
        're_wing': re_wing,
        'vtail': vtail,
        'moment_arm': moment_arm,
        'fuselage_length': fuselage_length,
        'rotor_diameter': rotor_diameter,
        'disk_loading': disk_loading_target,
        'p_hover': p_hover_actual,
        'p_cruise': cruise_power,
        'battery_mass': battery_mass,
        'battery_fraction': battery_mass / mtow_kg,
        'area_ratio': area_ratio,
    }


if __name__ == "__main__":
    results = run_section4_calculations()
