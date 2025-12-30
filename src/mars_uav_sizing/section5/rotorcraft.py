"""
Rotorcraft Configuration Analysis
==================================

Implements equations from manuscript Section 5.1 (Rotorcraft Configuration).
All parameters loaded from configuration - NO HARDCODED VALUES.

Equations implemented:
    @eq:induced-velocity     - Momentum theory induced velocity
    @eq:ideal-power          - Ideal hover power
    @eq:hover-power          - Actual hover power with FM
    @eq:electric-hover-full  - Electrical hover power
    @eq:hover-constraint     - Power loading constraint
    @eq:forward-power-ld     - Forward flight power
    @eq:endurance-simple     - Endurance equation
    
Reference: 
    - Manuscript: sections_en/05_01_rotorcraft-configuration-sec-rotorcraft-analysis.md
    - Leishman (2006), Principles of Helicopter Aerodynamics

Last Updated: 2025-12-29
"""

import math
from typing import Dict, Any
from datetime import datetime

# Import configuration loader
from ..config import (
    get_mars_gravity,
    get_density,
    get_mtow,
    get_propulsion_efficiencies,
    get_battery_params,
    get_mission_params,
    get_aerodynamic_params,
    get_param,
)


# =============================================================================
# MOMENTUM THEORY EQUATIONS (§5.1.1)
# =============================================================================

def induced_velocity(thrust_n: float, rho: float, disk_area_m2: float) -> float:
    """
    Calculate induced velocity from momentum theory.
    
    Implements @eq:induced-velocity from §5.1:
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
    """
    return math.sqrt(thrust_n / (2 * rho * disk_area_m2))


def induced_velocity_from_disk_loading(disk_loading: float, rho: float) -> float:
    """
    Calculate induced velocity from disk loading.
    
    Implements @eq:induced-velocity-dl from §5.1:
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
    """
    return math.sqrt(disk_loading / (2 * rho))


def ideal_hover_power(weight_n: float, rho: float, disk_area_m2: float) -> float:
    """
    Calculate ideal (theoretical minimum) hover power.
    
    Implements @eq:ideal-power from §5.1:
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
    figure_of_merit: float = None
) -> float:
    """
    Calculate actual hover power including rotor losses.
    
    Implements @eq:hover-power from §5.1:
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
        Rotor figure of merit (default: from config)
    
    Returns
    -------
    float
        Actual mechanical hover power in Watts
    """
    if figure_of_merit is None:
        figure_of_merit = get_propulsion_efficiencies()['figure_of_merit']
    
    p_ideal = ideal_hover_power(weight_n, rho, disk_area_m2)
    return p_ideal / figure_of_merit


def electric_hover_power(
    weight_n: float = None, 
    rho: float = None, 
    disk_area_m2: float = None,
    figure_of_merit: float = None,
    eta_motor: float = None,
    eta_esc: float = None
) -> float:
    """
    Calculate electrical power from battery for hover.
    
    Implements @eq:electric-hover-full from §5.1:
        P_elec = W^1.5 / (FM × η_motor × η_ESC × sqrt(2ρA))
    
    Parameters
    ----------
    weight_n : float, optional
        Aircraft weight in Newtons (default: from config MTOW)
    rho : float, optional
        Air density in kg/m³ (default: from config)
    disk_area_m2 : float, optional
        Total rotor disk area in m² (default: computed from DL)
    figure_of_merit : float, optional
        Rotor figure of merit (default: from config)
    eta_motor : float, optional
        Motor efficiency (default: from config)
    eta_esc : float, optional
        ESC efficiency (default: from config)
    
    Returns
    -------
    float
        Electrical hover power in Watts
    """
    # Load defaults from config
    g_mars = get_mars_gravity()
    prop = get_propulsion_efficiencies()
    
    if weight_n is None:
        weight_n = get_mtow() * g_mars
    if rho is None:
        rho = get_density()
    if figure_of_merit is None:
        figure_of_merit = prop['figure_of_merit']
    if eta_motor is None:
        eta_motor = prop['eta_motor']
    if eta_esc is None:
        eta_esc = prop['eta_esc']
    if disk_area_m2 is None:
        disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
        disk_area_m2 = weight_n / disk_loading
    
    p_hover = actual_hover_power(weight_n, rho, disk_area_m2, figure_of_merit)
    return p_hover / (eta_motor * eta_esc)


def hover_power_loading(
    disk_loading: float = None, 
    rho: float = None,
    figure_of_merit: float = None,
    eta_motor: float = None,
    eta_esc: float = None
) -> float:
    """
    Calculate P/W ratio for hover constraint on matching chart.
    
    Implements @eq:hover-constraint from §5.1:
        P/W = (1/(FM × η_motor × η_ESC)) × sqrt(DL/(2ρ))
    
    This value is INDEPENDENT of wing loading (W/S).
    Returns a horizontal line on the matching chart.
    
    Parameters
    ----------
    disk_loading : float, optional
        Disk loading in N/m² (default: from config)
    rho : float, optional
        Air density in kg/m³ (default: from config)
    figure_of_merit : float, optional
        Figure of merit (default: from config)
    eta_motor : float, optional
        Motor efficiency (default: from config)
    eta_esc : float, optional
        ESC efficiency (default: from config)
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    prop = get_propulsion_efficiencies()
    
    if disk_loading is None:
        disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    if rho is None:
        rho = get_density()
    if figure_of_merit is None:
        figure_of_merit = prop['figure_of_merit']
    if eta_motor is None:
        eta_motor = prop['eta_motor']
    if eta_esc is None:
        eta_esc = prop['eta_esc']
    
    eta_hover = figure_of_merit * eta_motor * eta_esc
    v_i = induced_velocity_from_disk_loading(disk_loading, rho)
    return v_i / eta_hover


# =============================================================================
# FORWARD FLIGHT EQUATIONS (§5.1.2)
# =============================================================================

def forward_flight_power(
    weight_n: float, 
    velocity: float,
    ld_effective: float = None
) -> float:
    """
    Calculate rotor mechanical power in forward flight.
    
    Implements @eq:forward-power-ld from §5.1:
        P_fwd = W × V / (L/D)_eff
    
    Reference: Leishman (2006), Chapter 1
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Forward flight velocity in m/s
    ld_effective : float, optional
        Effective lift-to-drag ratio (default: from config)
    
    Returns
    -------
    float
        Mechanical forward flight power in Watts
    """
    if ld_effective is None:
        ld_effective = get_aerodynamic_params()['ld_eff_rotorcraft']
    
    return (weight_n * velocity) / ld_effective


def electric_forward_flight_power(
    weight_n: float = None,
    velocity: float = None,
    ld_effective: float = None,
    eta_motor: float = None,
    eta_esc: float = None
) -> float:
    """
    Calculate electrical power for rotorcraft forward flight.
    
    Implements @eq:forward-electric-power from §5.1:
        P_elec,fwd = W × V / ((L/D)_eff × η_motor × η_ESC)
    
    Parameters
    ----------
    weight_n : float, optional
        Aircraft weight in Newtons (default: from config)
    velocity : float, optional
        Forward flight velocity in m/s (default: from config)
    ld_effective : float, optional
        Effective lift-to-drag ratio (default: from config)
    eta_motor : float, optional
        Motor efficiency (default: from config)
    eta_esc : float, optional
        ESC efficiency (default: from config)
    
    Returns
    -------
    float
        Electrical forward flight power in Watts
    """
    g_mars = get_mars_gravity()
    prop = get_propulsion_efficiencies()
    mission = get_mission_params()
    
    if weight_n is None:
        weight_n = get_mtow() * g_mars
    if velocity is None:
        velocity = mission['v_cruise']
    if ld_effective is None:
        ld_effective = get_aerodynamic_params()['ld_eff_rotorcraft']
    if eta_motor is None:
        eta_motor = prop['eta_motor']
    if eta_esc is None:
        eta_esc = prop['eta_esc']
    
    p_mech = forward_flight_power(weight_n, velocity, ld_effective)
    return p_mech / (eta_motor * eta_esc)


# =============================================================================
# ENDURANCE EQUATIONS (§5.1.3)
# =============================================================================

def rotorcraft_endurance_seconds() -> float:
    """
    Calculate theoretical rotorcraft endurance (MTOW-independent).
    
    Implements @eq:endurance-simple from §5.1:
        t = (f_batt × e_spec × DoD × η_batt × (L/D)_eff × η_motor × η_ESC) / (g × V)
    
    This key result shows that rotorcraft endurance is INDEPENDENT of MTOW
    when mass fractions are fixed.
    
    Returns
    -------
    float
        Endurance in SECONDS
    """
    g_mars = get_mars_gravity()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    
    # Convert Wh/kg to J/kg
    e_spec_j_kg = batt['e_spec_Wh_kg'] * 3600
    
    numerator = (
        mission['f_batt'] 
        * e_spec_j_kg 
        * batt['dod'] 
        * batt['eta_discharge'] 
        * aero['ld_eff_rotorcraft'] 
        * prop['eta_motor'] 
        * prop['eta_esc']
    )
    denominator = g_mars * mission['v_cruise']
    
    return numerator / denominator


# =============================================================================
# FEASIBILITY ANALYSIS (§5.1.4)
# =============================================================================

def rotorcraft_feasibility_analysis() -> Dict[str, Any]:
    """
    Complete rotorcraft feasibility analysis.
    
    Loads all parameters from configuration and computes:
    - Hover power (electrical)
    - Forward flight power (electrical)
    - Energy budget with reserve
    - Achievable endurance and range
    - Comparison against 60-minute requirement
    
    Returns
    -------
    dict
        Complete analysis results including:
        - mtow_kg, weight_n: Mass/weight
        - hover_power_w, cruise_power_w: Power values
        - endurance_min, range_km: Performance
        - feasible, margin_percent: Assessment
    """
    # Load all parameters from config
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    endurance_req = get_param('mission.requirements.endurance_min')
    
    # Derived values
    weight_n = mtow_kg * g_mars
    disk_area_m2 = weight_n / disk_loading
    v_cruise = mission['v_cruise']
    hover_time_s = mission['t_hover_s']
    reserve_fraction = mission['energy_reserve']
    f_batt = mission['f_batt']
    
    # Hover power
    p_hover_elec = electric_hover_power(
        weight_n, rho, disk_area_m2,
        prop['figure_of_merit'], prop['eta_motor'], prop['eta_esc']
    )
    
    # Forward flight power
    p_cruise_elec = electric_forward_flight_power(
        weight_n, v_cruise, aero['ld_eff_rotorcraft'],
        prop['eta_motor'], prop['eta_esc']
    )
    
    # Battery energy
    battery_mass_kg = f_batt * mtow_kg
    total_energy_wh = battery_mass_kg * batt['e_spec_Wh_kg']
    usable_energy_wh = total_energy_wh * batt['dod'] * batt['eta_discharge']
    energy_after_reserve = usable_energy_wh * (1 - reserve_fraction)
    
    # Hover energy
    hover_energy_wh = p_hover_elec * (hover_time_s / 3600)
    
    # Remaining for cruise
    cruise_energy_wh = energy_after_reserve - hover_energy_wh
    
    # Cruise time and endurance
    if cruise_energy_wh > 0:
        cruise_time_s = (cruise_energy_wh / p_cruise_elec) * 3600
        cruise_time_min = cruise_time_s / 60
    else:
        cruise_time_s = 0
        cruise_time_min = 0
    
    total_endurance_min = (hover_time_s / 60) + cruise_time_min
    
    # Range
    range_km = (v_cruise * cruise_time_s) / 1000
    
    # Feasibility
    feasible = total_endurance_min >= endurance_req
    margin_percent = ((total_endurance_min / endurance_req) - 1) * 100
    
    # Induced velocity for reference
    v_i = induced_velocity(weight_n, rho, disk_area_m2)
    
    # Combined efficiencies
    eta_hover = prop['figure_of_merit'] * prop['eta_motor'] * prop['eta_esc']
    eta_cruise = prop['eta_motor'] * prop['eta_esc']
    
    return {
        # Input parameters (from config)
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'disk_loading_n_m2': disk_loading,
        'disk_area_m2': disk_area_m2,
        'rho_kg_m3': rho,
        'v_cruise_m_s': v_cruise,
        
        # Propulsion efficiencies
        'figure_of_merit': prop['figure_of_merit'],
        'eta_motor': prop['eta_motor'],
        'eta_esc': prop['eta_esc'],
        'eta_hover': eta_hover,
        'eta_cruise': eta_cruise,
        'ld_effective': aero['ld_eff_rotorcraft'],
        
        # Power calculations
        'induced_velocity_m_s': v_i,
        'hover_power_w': p_hover_elec,
        'cruise_power_w': p_cruise_elec,
        'power_loading_w_per_n': p_hover_elec / weight_n,
        'power_loading_w_per_kg': p_hover_elec / mtow_kg,
        
        # Energy calculations
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'usable_energy_wh': usable_energy_wh,
        'energy_after_reserve_wh': energy_after_reserve,
        'hover_energy_wh': hover_energy_wh,
        'cruise_energy_wh': cruise_energy_wh,
        
        # Performance
        'hover_time_min': hover_time_s / 60,
        'cruise_time_min': cruise_time_min,
        'endurance_min': total_endurance_min,
        'range_km': range_km,
        
        # Assessment
        'requirement_min': endurance_req,
        'feasible': feasible,
        'margin_percent': margin_percent,
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """
    Print formatted rotorcraft analysis results.
    
    Parameters
    ----------
    results : dict, optional
        Results from rotorcraft_feasibility_analysis()
        If None, runs the analysis first
    """
    if results is None:
        results = rotorcraft_feasibility_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("ROTORCRAFT FEASIBILITY ANALYSIS (Section 5.1)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()
    
    print("INPUT PARAMETERS (from configuration)")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Mars gravity:       {get_mars_gravity():.3f} m/s²")
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Disk loading:       {results['disk_loading_n_m2']:.1f} N/m²")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m³")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print()
    
    print("PROPULSION EFFICIENCIES (from §4.5)")
    print("-" * 50)
    print(f"  Figure of Merit:    {results['figure_of_merit']:.2f}")
    print(f"  Motor efficiency:   {results['eta_motor']:.2f}")
    print(f"  ESC efficiency:     {results['eta_esc']:.2f}")
    print(f"  Combined eta_hover: {results['eta_hover']:.4f}")
    print(f"  Equivalent L/D:     {results['ld_effective']:.1f}")
    print()
    
    print("HOVER ANALYSIS (@eq:hover-power)")
    print("-" * 50)
    print(f"  Disk area:          {results['disk_area_m2']:.3f} m²")
    print(f"  Induced velocity:   {results['induced_velocity_m_s']:.2f} m/s")
    print(f"  Electrical power:   {results['hover_power_w']:.0f} W")
    print(f"  Power loading:      {results['power_loading_w_per_kg']:.0f} W/kg")
    print()
    
    print("FORWARD FLIGHT ANALYSIS (@eq:forward-power-ld)")
    print("-" * 50)
    print(f"  Cruise power:       {results['cruise_power_w']:.1f} W")
    print()
    
    print("ENERGY BUDGET")
    print("-" * 50)
    print(f"  Battery mass:       {results['battery_mass_kg']:.2f} kg")
    print(f"  Total capacity:     {results['total_energy_wh']:.1f} Wh")
    print(f"  Usable (after DoD): {results['usable_energy_wh']:.1f} Wh")
    print(f"  After 20% reserve:  {results['energy_after_reserve_wh']:.1f} Wh")
    print(f"  Hover energy:       {results['hover_energy_wh']:.1f} Wh ({results['hover_time_min']:.0f} min)")
    print(f"  Cruise energy:      {results['cruise_energy_wh']:.1f} Wh")
    print()
    
    print("PERFORMANCE")
    print("-" * 50)
    print(f"  Cruise time:        {results['cruise_time_min']:.1f} min")
    print(f"  Total endurance:    {results['endurance_min']:.1f} min")
    print(f"  Range:              {results['range_km']:.0f} km")
    print()
    
    print("FEASIBILITY ASSESSMENT")
    print("-" * 50)
    status = "[PASS]" if results['feasible'] else "[FAIL]"
    print(f"  Requirement:        {results['requirement_min']:.0f} min endurance")
    print(f"  Achieved:           {results['endurance_min']:.1f} min")
    print(f"  Margin:             {results['margin_percent']:+.1f}%")
    print(f"  Status:             {status}")
    print()
    
    if not results['feasible']:
        print("CONCLUSION: Pure rotorcraft configuration FAILS endurance requirement.")
        print(f"           Deficit of {abs(results['margin_percent']):.1f}% is unacceptable for Mars mission.")
    elif results['margin_percent'] < 10:
        print("CONCLUSION: Rotorcraft marginally meets requirement.")
        print(f"           Margin of only {results['margin_percent']:.1f}% is insufficient for Mars operations.")
    else:
        print(f"CONCLUSION: Rotorcraft meets requirement with {results['margin_percent']:.1f}% margin.")
    
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_analysis()
    
    # Also show theoretical endurance
    print()
    print("=" * 80)
    print("THEORETICAL ENDURANCE CHECK (@eq:endurance-simple)")
    print("=" * 80)
    t_endurance_s = rotorcraft_endurance_seconds()
    t_endurance_min = t_endurance_s / 60
    print(f"Theoretical cruise endurance (MTOW-independent): {t_endurance_min:.1f} min")
    print("Note: This assumes 100% forward flight (no hover phases)")
    print("=" * 80)
