"""
Rotorcraft Configuration Analysis
==================================

Implements equations from manuscript Section 5.2 (Rotorcraft Configuration).
All equations are traced to source_grounding.txt for citations.

Reference: 
- Manuscript: sections_en/05_02_rotorcraft-analysis.md
- Prompt: docs/prompt_04_python_implementation.txt

Updated 2025-12-28: CORRECTED parameters from verification:
- ρ = 0.0196 kg/m³ (was 0.0209)
"""

import math
from typing import Dict, Any
from datetime import datetime

# Default parameters from baseline_parameters.yaml (updated from §4.12)
# Physical constants
G_MARS = 3.711          # m/s²
RHO_ARCADIA = 0.0196    # kg/m³ (CORRECTED from 0.0209)

# Propulsion efficiencies (from §4.5)
FM_DEFAULT = 0.40       # Figure of merit [Leishman, MAV data 0.30-0.50]
ETA_MOTOR = 0.85        # Motor efficiency
ETA_ESC = 0.95          # ESC efficiency

# Battery parameters (from §4.6, §4.11)
E_SPEC_WH_KG = 270      # Wh/kg
DOD = 0.80              # Depth of discharge
ETA_DISCHARGE = 0.95    # Discharge efficiency
RESERVE_FRACTION = 0.20 # Energy reserve

# Mass fractions (from §4.11)
F_BATT = 0.35           # Battery mass fraction
MTOW_BASELINE_KG = 10.0 # Baseline MTOW

# Aerodynamic (from §4.7)
LD_EFF_ROTORCRAFT = 4.0 # Equivalent L/D for rotorcraft forward flight

# Mission (from §4.12)
DISK_LOADING_DEFAULT = 30.0  # N/m²
V_CRUISE_DEFAULT = 40.0      # m/s
T_HOVER_DEFAULT_S = 180      # s


def induced_velocity(thrust_n: float, rho: float, disk_area_m2: float) -> float:
    """Calculate induced velocity from momentum theory.
    
    Implements @eq:induced-velocity from §5.2:
        v_i = sqrt(T / (2ρA))
    
    Reference: Leishman (2006), Eq. 2.15
    
    Parameters
    ----------
    thrust_n : float
        Rotor thrust in Newtons
    rho : float
        Air density in kg/m³
    disk_area_m2 : float
        Total rotor disk area in m²
    
    Returns
    -------
    float
        Induced velocity in m/s
    
    Examples
    --------
    >>> round(induced_velocity(37.11, 0.0209, 1.237), 1)
    26.8
    """
    return math.sqrt(thrust_n / (2 * rho * disk_area_m2))


def induced_velocity_from_disk_loading(disk_loading: float, rho: float) -> float:
    """Calculate induced velocity from disk loading.
    
    Implements @eq:induced-velocity-dl from §5.2:
        v_i = sqrt(DL / (2ρ))
    
    Parameters
    ----------
    disk_loading : float
        Disk loading T/A in N/m²
    rho : float
        Air density in kg/m³
    
    Returns
    -------
    float
        Induced velocity in m/s
    
    Examples
    --------
    >>> round(induced_velocity_from_disk_loading(30.0, 0.0209), 1)
    26.8
    """
    return math.sqrt(disk_loading / (2 * rho))


def ideal_hover_power(weight_n: float, rho: float, disk_area_m2: float) -> float:
    """Calculate ideal (theoretical minimum) hover power.
    
    Implements @eq:ideal-power from §5.2:
        P_ideal = W^1.5 / sqrt(2ρA)
    
    Reference: Leishman (2006), Section 2.3
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    rho : float
        Air density in kg/m³
    disk_area_m2 : float
        Total rotor disk area in m²
    
    Returns
    -------
    float
        Ideal hover power in Watts
    """
    return (weight_n ** 1.5) / math.sqrt(2 * rho * disk_area_m2)


def actual_hover_power(
    weight_n: float, 
    rho: float, 
    disk_area_m2: float,
    figure_of_merit: float = FM_DEFAULT
) -> float:
    """Calculate actual hover power including rotor losses.
    
    Implements @eq:hover-power from §5.2:
        P_hover = W^1.5 / (FM × sqrt(2ρA))
    
    Reference: Leishman (2006), Section 2.8
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    rho : float
        Air density in kg/m³
    disk_area_m2 : float
        Total rotor disk area in m²
    figure_of_merit : float, optional
        Rotor figure of merit, default 0.40
    
    Returns
    -------
    float
        Actual mechanical hover power in Watts
    """
    p_ideal = ideal_hover_power(weight_n, rho, disk_area_m2)
    return p_ideal / figure_of_merit


def electric_hover_power(
    weight_n: float, 
    rho: float, 
    disk_area_m2: float,
    figure_of_merit: float = FM_DEFAULT,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC
) -> float:
    """Calculate electrical power from battery for hover.
    
    Implements @eq:electric-hover-full from §5.2:
        P_elec = W^1.5 / (FM × η_motor × η_ESC × sqrt(2ρA))
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    rho : float
        Air density in kg/m³
    disk_area_m2 : float
        Total rotor disk area in m²
    figure_of_merit : float, optional
        Rotor figure of merit, default 0.40
    eta_motor : float, optional
        Motor efficiency, default 0.85
    eta_esc : float, optional
        ESC efficiency, default 0.95
    
    Returns
    -------
    float
        Electrical hover power in Watts
    """
    p_hover = actual_hover_power(weight_n, rho, disk_area_m2, figure_of_merit)
    return p_hover / (eta_motor * eta_esc)


def hover_power_loading(
    disk_loading: float, 
    rho: float,
    figure_of_merit: float = FM_DEFAULT,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC
) -> float:
    """Calculate P/W ratio for hover constraint on matching chart.
    
    Implements @eq:hover-constraint from §5.2:
        P/W = (1/(FM × η_motor × η_ESC)) × sqrt(DL/(2ρ))
    
    This value is INDEPENDENT of wing loading (W/S).
    Returns a horizontal line on the matching chart.
    
    Parameters
    ----------
    disk_loading : float
        Disk loading in N/m²
    rho : float
        Air density in kg/m³
    figure_of_merit : float, optional
        Figure of merit, default 0.40
    eta_motor : float, optional
        Motor efficiency, default 0.85
    eta_esc : float, optional
        ESC efficiency, default 0.95
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    eta_hover = figure_of_merit * eta_motor * eta_esc
    v_i = induced_velocity_from_disk_loading(disk_loading, rho)
    return v_i / eta_hover


def forward_flight_power(
    weight_n: float, 
    velocity: float,
    ld_effective: float = LD_EFF_ROTORCRAFT
) -> float:
    """Calculate rotor mechanical power in forward flight.
    
    Implements @eq:forward-power-ld from §5.2:
        P_fwd = W × V / (L/D)_eff
    
    Reference: Leishman (2006), Chapter 1
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Forward flight velocity in m/s
    ld_effective : float, optional
        Effective lift-to-drag ratio, default 4.0
    
    Returns
    -------
    float
        Mechanical forward flight power in Watts
    """
    return (weight_n * velocity) / ld_effective


def electric_forward_flight_power(
    weight_n: float,
    velocity: float,
    ld_effective: float = LD_EFF_ROTORCRAFT,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC
) -> float:
    """Calculate electrical power for rotorcraft forward flight.
    
    Implements @eq:forward-electric-power from §5.2:
        P_elec,fwd = W × V / ((L/D)_eff × η_motor × η_ESC)
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Forward flight velocity in m/s
    ld_effective : float, optional
        Effective lift-to-drag ratio, default 4.0
    eta_motor : float, optional
        Motor efficiency, default 0.85
    eta_esc : float, optional
        ESC efficiency, default 0.95
    
    Returns
    -------
    float
        Electrical forward flight power in Watts
    """
    p_mech = forward_flight_power(weight_n, velocity, ld_effective)
    return p_mech / (eta_motor * eta_esc)


def rotorcraft_endurance(
    f_batt: float = F_BATT,
    e_spec_j_kg: float = E_SPEC_WH_KG * 3600,  # Convert Wh/kg to J/kg
    dod: float = DOD,
    eta_batt: float = ETA_DISCHARGE,
    ld_eff: float = LD_EFF_ROTORCRAFT,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC,
    g_mars: float = G_MARS,
    v_cruise: float = V_CRUISE_DEFAULT
) -> float:
    """Calculate rotorcraft endurance (MTOW-independent).
    
    Implements @eq:endurance-simple from §5.2:
        t = (f_batt × e_spec × DoD × η_batt × (L/D)_eff × η_motor × η_ESC) / (g × V)
    
    This key result shows that rotorcraft endurance is INDEPENDENT of MTOW
    when mass fractions are fixed.
    
    Parameters
    ----------
    f_batt : float
        Battery mass fraction
    e_spec_j_kg : float
        Specific energy in J/kg (default: 270 Wh/kg = 972,000 J/kg)
    dod : float
        Depth of discharge
    eta_batt : float
        Battery discharge efficiency
    ld_eff : float
        Effective lift-to-drag ratio
    eta_motor : float
        Motor efficiency
    eta_esc : float
        ESC efficiency
    g_mars : float
        Mars gravity in m/s²
    v_cruise : float
        Cruise velocity in m/s
    
    Returns
    -------
    float
        Endurance in SECONDS
    """
    numerator = f_batt * e_spec_j_kg * dod * eta_batt * ld_eff * eta_motor * eta_esc
    denominator = g_mars * v_cruise
    return numerator / denominator


def rotorcraft_feasibility_analysis(
    mtow_kg: float = MTOW_BASELINE_KG,
    disk_loading: float = DISK_LOADING_DEFAULT,
    hover_time_s: float = T_HOVER_DEFAULT_S,
    v_cruise: float = V_CRUISE_DEFAULT,
    rho: float = RHO_ARCADIA,
    f_batt: float = F_BATT,
    e_spec_wh_kg: float = E_SPEC_WH_KG,
    dod: float = DOD,
    eta_batt: float = ETA_DISCHARGE,
    reserve_fraction: float = RESERVE_FRACTION,
    figure_of_merit: float = FM_DEFAULT,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC,
    ld_eff: float = LD_EFF_ROTORCRAFT,
    g_mars: float = G_MARS,
    endurance_requirement_min: float = 60.0
) -> Dict[str, Any]:
    """Complete rotorcraft feasibility analysis.
    
    Returns dictionary with:
    - hover_power_w: Electrical hover power
    - cruise_power_w: Forward flight power
    - usable_energy_wh: Available battery energy
    - hover_energy_wh: Energy for hover phases
    - cruise_energy_wh: Remaining for cruise
    - endurance_min: Achievable endurance
    - range_km: Achievable range
    - feasible: Boolean meeting 60 min requirement
    - margin_percent: Safety margin over requirement
    """
    # Weight calculation
    weight_n = mtow_kg * g_mars
    
    # Disk area from disk loading
    disk_area_m2 = weight_n / disk_loading
    
    # Hover power
    p_hover_elec = electric_hover_power(
        weight_n, rho, disk_area_m2, figure_of_merit, eta_motor, eta_esc
    )
    
    # Forward flight power
    p_cruise_elec = electric_forward_flight_power(
        weight_n, v_cruise, ld_eff, eta_motor, eta_esc
    )
    
    # Battery energy
    battery_mass_kg = f_batt * mtow_kg
    total_energy_wh = battery_mass_kg * e_spec_wh_kg
    usable_energy_wh = total_energy_wh * dod * eta_batt
    
    # After reserve
    energy_after_reserve = usable_energy_wh * (1 - reserve_fraction)
    
    # Hover energy
    hover_energy_wh = p_hover_elec * (hover_time_s / 3600)
    
    # Remaining for cruise
    cruise_energy_wh = energy_after_reserve - hover_energy_wh
    
    # Cruise time and endurance
    if cruise_energy_wh > 0:
        cruise_time_s = (cruise_energy_wh / p_cruise_elec) * 3600  # seconds
        cruise_time_min = cruise_time_s / 60
    else:
        cruise_time_s = 0
        cruise_time_min = 0
    
    total_endurance_min = (hover_time_s / 60) + cruise_time_min
    
    # Range
    range_km = (v_cruise * cruise_time_s) / 1000
    
    # Feasibility
    feasible = total_endurance_min >= endurance_requirement_min
    margin_percent = ((total_endurance_min / endurance_requirement_min) - 1) * 100
    
    # Induced velocity for reference
    v_i = induced_velocity(weight_n, rho, disk_area_m2)
    
    # Power loading
    pw_hover = p_hover_elec / weight_n  # W/N
    pw_hover_per_kg = p_hover_elec / mtow_kg  # W/kg
    
    return {
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'disk_area_m2': disk_area_m2,
        'disk_loading_n_m2': disk_loading,
        'induced_velocity_m_s': v_i,
        'hover_power_w': p_hover_elec,
        'cruise_power_w': p_cruise_elec,
        'power_loading_w_per_n': pw_hover,
        'power_loading_w_per_kg': pw_hover_per_kg,
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'usable_energy_wh': usable_energy_wh,
        'energy_after_reserve_wh': energy_after_reserve,
        'hover_energy_wh': hover_energy_wh,
        'cruise_energy_wh': cruise_energy_wh,
        'hover_time_min': hover_time_s / 60,
        'cruise_time_min': cruise_time_min,
        'endurance_min': total_endurance_min,
        'range_km': range_km,
        'feasible': feasible,
        'margin_percent': margin_percent,
        'eta_hover': figure_of_merit * eta_motor * eta_esc,
        'eta_cruise': eta_motor * eta_esc,
        'ld_effective': ld_eff,
    }


def print_rotorcraft_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted rotorcraft analysis results."""
    if results is None:
        results = rotorcraft_feasibility_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("ROTORCRAFT FEASIBILITY ANALYSIS")
    print("Equations from: Manuscript Section 5.2 (Rotorcraft Configuration)")
    print(f"Values computed: {timestamp}")
    print("=" * 80)
    print()
    
    print("INPUT PARAMETERS (verified from sources)")
    print("-" * 40)
    print(f"MTOW:               {results['mtow_kg']:.1f} kg")
    print(f"Mars gravity:       {G_MARS:.3f} m/s²")
    print(f"Weight:             {results['weight_n']:.2f} N        [COMPUTED: MTOW × g]")
    print(f"Disk loading:       {results['disk_loading_n_m2']:.1f} N/m²")
    print(f"Disk area:          {results['disk_area_m2']:.3f} m²       [COMPUTED: W / DL]")
    print(f"Air density:        {RHO_ARCADIA} kg/m³")
    print()
    
    print("PROPULSION EFFICIENCIES (from §4.5)")
    print("-" * 40)
    print(f"Figure of Merit:    {FM_DEFAULT:.2f}")
    print(f"Motor efficiency:   {ETA_MOTOR:.2f}")
    print(f"ESC efficiency:     {ETA_ESC:.2f}")
    print(f"Combined η_hover:   {results['eta_hover']:.3f}          [COMPUTED: FM × η_m × η_ESC]")
    print()
    
    print("BATTERY PARAMETERS (from §4.6, §4.11)")
    print("-" * 40)
    print(f"Mass fraction:      {F_BATT:.2f}")
    print(f"Battery mass:       {results['battery_mass_kg']:.3f} kg       [COMPUTED]")
    print(f"Specific energy:    {E_SPEC_WH_KG} Wh/kg")
    print(f"Total capacity:     {results['total_energy_wh']:.1f} Wh       [COMPUTED]")
    print(f"Depth of discharge: {DOD:.2f}")
    print(f"Usable energy:      {results['usable_energy_wh']:.1f} Wh       [COMPUTED]")
    print(f"After 20% reserve:  {results['energy_after_reserve_wh']:.1f} Wh       [COMPUTED]")
    print()
    
    print("HOVER ANALYSIS (@eq:induced-velocity through @eq:hover-constraint)")
    print("-" * 40)
    print(f"Induced velocity:   {results['induced_velocity_m_s']:.1f} m/s")
    p_ideal = ideal_hover_power(results['weight_n'], RHO_ARCADIA, results['disk_area_m2'])
    p_actual = actual_hover_power(results['weight_n'], RHO_ARCADIA, results['disk_area_m2'], FM_DEFAULT)
    print(f"Ideal power:        {p_ideal:.0f} W")
    print(f"Actual power:       {p_actual:.0f} W (mechanical)")
    print(f"Electrical power:   {results['hover_power_w']:.0f} W")
    print(f"Power loading:      {results['power_loading_w_per_kg']:.0f} W/kg")
    print()
    
    print("FORWARD FLIGHT ANALYSIS (@eq:forward-power-ld, @eq:forward-electric-power)")
    print("-" * 40)
    print(f"Equivalent L/D:     {results['ld_effective']:.1f}")
    print(f"Cruise velocity:    {V_CRUISE_DEFAULT:.0f} m/s")
    print(f"Cruise power:       {results['cruise_power_w']:.0f} W")
    print()
    
    print("MISSION ENERGY BUDGET")
    print("-" * 40)
    print(f"Hover energy:       {results['hover_energy_wh']:.1f} Wh ({results['hover_time_min']:.0f} min at {results['hover_power_w']:.0f} W)")
    print(f"Cruise energy:      {results['cruise_energy_wh']:.1f} Wh (available for cruise)")
    print(f"Cruise time:        {results['cruise_time_min']:.0f} min")
    print(f"Total endurance:    {results['endurance_min']:.0f} min (hover + cruise)")
    print(f"Range:              {results['range_km']:.0f} km")
    print()
    
    print("COMPARISON WITH REQUIREMENTS")
    print("-" * 40)
    status_endurance = "✓ PASS" if results['feasible'] else "❌ FAIL"
    range_margin = (results['range_km'] / 100 - 1) * 100
    status_range = "✓ PASS" if results['range_km'] >= 100 else "⚠️ MARGINAL" if results['range_km'] >= 80 else "❌ FAIL"
    
    print(f"Requirement          Target    Computed     Margin     Status")
    print(f"Endurance            60 min    {results['endurance_min']:.0f} min       {results['margin_percent']:+.0f}%       {status_endurance}")
    print(f"Range                100 km    {results['range_km']:.0f} km        {range_margin:+.0f}%       {status_range}")
    print(f"VTOL                 Yes       Yes          —          ✓ PASS")
    print()
    
    if results['feasible'] and results['margin_percent'] < 20:
        print(f"CONCLUSION: Rotorcraft numerically meets requirements with only {results['margin_percent']:.0f}% margin.")
        print("WARNING: Margin is dangerously thin for mission with no abort capability.")
        print("RECOMMENDATION: NOT RECOMMENDED due to inadequate safety margin.")
    elif results['feasible']:
        print(f"CONCLUSION: Rotorcraft meets requirements with {results['margin_percent']:.0f}% margin.")
    else:
        print("CONCLUSION: Rotorcraft FAILS to meet endurance requirements.")
    
    print("=" * 80)
    print()
    print(">>> These COMPUTED values will be used to UPDATE the manuscript in Phase C.")


if __name__ == "__main__":
    # Run complete analysis with baseline parameters
    results = rotorcraft_feasibility_analysis()
    print_rotorcraft_analysis(results)
    
    # Also compute theoretical endurance from simplified equation
    print("\n" + "=" * 80)
    print("THEORETICAL ENDURANCE CHECK (@eq:endurance-simple)")
    print("=" * 80)
    t_endurance_s = rotorcraft_endurance()
    t_endurance_min = t_endurance_s / 60
    print(f"Theoretical cruise endurance (MTOW-independent): {t_endurance_min:.1f} min")
    print("Note: This is maximum endurance assuming 100% forward flight (no hover)")
    print("=" * 80)
