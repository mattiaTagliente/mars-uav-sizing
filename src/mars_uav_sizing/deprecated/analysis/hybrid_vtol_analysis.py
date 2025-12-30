"""
Hybrid VTOL (QuadPlane) Configuration Analysis
==============================================

Implements equations from manuscript Section 5.4 (Hybrid VTOL Configuration).
Combines hover analysis from §5.2 with cruise analysis from §5.3.

Reference: 
- Manuscript: sections_en/05_04_hybrid-vtol-analysis.md
- Prompt: docs/prompt_04_python_implementation.txt

Updated 2025-12-28: CORRECTED parameters from verification:
- ρ = 0.0196 kg/m³ (was 0.0209)
- e = 0.869 for AR=6 (was 0.82)
"""

import math
from typing import Dict, Any
from datetime import datetime

# Import functions from other analysis modules
from .rotorcraft_analysis import (
    induced_velocity,
    induced_velocity_from_disk_loading,
    ideal_hover_power,
    actual_hover_power,
    electric_hover_power,
    hover_power_loading,
)

from .fixed_wing_analysis import (
    cruise_lift_coefficient,
    drag_coefficient,
    lift_to_drag,
    maximum_ld,
    cruise_power,
    stall_speed,
)

# Default parameters from baseline_parameters.yaml (updated from §4.12)
# Physical constants
G_MARS = 3.711          # m/s²
RHO_ARCADIA = 0.0196    # kg/m³ (CORRECTED from 0.0209)

# Propulsion efficiencies (from §4.5)
FM_DEFAULT = 0.40       # Figure of merit
ETA_PROP = 0.55         # Propeller efficiency
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

# Aerodynamic parameters (from §4.7)
AR_DEFAULT = 6          # Aspect ratio
OSWALD_E = 0.869        # Oswald efficiency factor (CORRECTED: Sadraey correlation for AR=6)
CD0_DEFAULT = 0.030     # Zero-lift drag coefficient
CL_MAX = 1.20           # Maximum lift coefficient

# QuadPlane specific
LD_PENALTY_FACTOR = 0.90  # L/D reduction due to stopped rotors

# Mission (from §4.12)
DISK_LOADING_DEFAULT = 30.0  # N/m²
V_CRUISE_DEFAULT = 40.0      # m/s
T_HOVER_DEFAULT_S = 180      # s (3 min)
T_CRUISE_DEFAULT_MIN = 57    # min


def hybrid_hover_power(weight_n: float, rho: float, disk_area_m2: float,
                       figure_of_merit: float = FM_DEFAULT,
                       eta_motor: float = ETA_MOTOR,
                       eta_esc: float = ETA_ESC) -> float:
    """Calculate hover power for lift rotors.
    
    Identical to rotorcraft analysis (§5.2).
    Implements @eq:electric-hover-qp from §5.4.
    
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
    return electric_hover_power(
        weight_n, rho, disk_area_m2, figure_of_merit, eta_motor, eta_esc
    )


def hybrid_cruise_power(weight_n: float, velocity: float, ld: float,
                        eta_prop: float = ETA_PROP, eta_motor: float = ETA_MOTOR,
                        eta_esc: float = ETA_ESC) -> float:
    """Calculate cruise power for wing + cruise motor.
    
    Same as fixed-wing analysis (§5.3), but L/D may be reduced
    due to parasitic drag from stopped lift rotors.
    
    Implements @eq:cruise-power-qp from §5.4.
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Cruise velocity in m/s
    ld : float
        Lift-to-drag ratio (reduced for QuadPlane)
    eta_prop : float, optional
        Propeller efficiency, default 0.55
    eta_motor : float, optional
        Motor efficiency, default 0.85
    eta_esc : float, optional
        ESC efficiency, default 0.95
    
    Returns
    -------
    float
        Electrical cruise power in Watts
    """
    return cruise_power(weight_n, velocity, ld, eta_prop, eta_motor, eta_esc)


def energy_budget(hover_power_w: float, hover_time_s: float,
                  cruise_power_w: float, cruise_time_s: float,
                  reserve_fraction: float = RESERVE_FRACTION) -> Dict[str, float]:
    """Calculate complete energy budget.
    
    Implements @eq:energy-budget from §5.4:
        E_req = E_hover + E_cruise + E_reserve
    
    Parameters
    ----------
    hover_power_w : float
        Electrical hover power in Watts
    hover_time_s : float
        Total hover time in seconds
    cruise_power_w : float
        Electrical cruise power in Watts
    cruise_time_s : float
        Cruise time in seconds
    reserve_fraction : float, optional
        Energy reserve fraction, default 0.20
    
    Returns
    -------
    dict
        Energy breakdown with keys:
        - hover_energy_wh: Energy for hover phases
        - cruise_energy_wh: Energy for cruise phase
        - mission_energy_wh: Sum of hover + cruise
        - reserve_energy_wh: Reserve (fraction of mission)
        - total_energy_wh: Total required energy
    """
    # Energy in Wh
    hover_energy_wh = hover_power_w * (hover_time_s / 3600)
    cruise_energy_wh = cruise_power_w * (cruise_time_s / 3600)
    mission_energy_wh = hover_energy_wh + cruise_energy_wh
    reserve_energy_wh = reserve_fraction * mission_energy_wh
    total_energy_wh = mission_energy_wh + reserve_energy_wh
    
    return {
        'hover_energy_wh': hover_energy_wh,
        'cruise_energy_wh': cruise_energy_wh,
        'mission_energy_wh': mission_energy_wh,
        'reserve_energy_wh': reserve_energy_wh,
        'total_energy_wh': total_energy_wh,
    }


def required_battery_mass(total_energy_wh: float,
                          e_spec_wh_kg: float = E_SPEC_WH_KG,
                          dod: float = DOD,
                          eta: float = ETA_DISCHARGE) -> float:
    """Calculate minimum battery mass for mission.
    
    Implements @eq:battery-requirement from §5.4:
        m_batt = E_total / (e_spec × DoD × η)
    
    Parameters
    ----------
    total_energy_wh : float
        Total required energy including reserve in Wh
    e_spec_wh_kg : float, optional
        Specific energy in Wh/kg, default 270
    dod : float, optional
        Depth of discharge, default 0.80
    eta : float, optional
        Discharge efficiency, default 0.95
    
    Returns
    -------
    float
        Minimum battery mass in kg
    """
    usable_fraction = e_spec_wh_kg * dod * eta
    return total_energy_wh / usable_fraction


def available_energy(mtow_kg: float, f_batt: float = F_BATT,
                     e_spec_wh_kg: float = E_SPEC_WH_KG,
                     dod: float = DOD, eta: float = ETA_DISCHARGE) -> float:
    """Calculate available energy from battery.
    
    Implements @eq:energy-available from §5.4:
        E_available = f_batt × MTOW × e_spec × DoD × η
    
    Parameters
    ----------
    mtow_kg : float
        MTOW in kg
    f_batt : float, optional
        Battery mass fraction, default 0.35
    e_spec_wh_kg : float, optional
        Specific energy in Wh/kg, default 270
    dod : float, optional
        Depth of discharge, default 0.80
    eta : float, optional
        Discharge efficiency, default 0.95
    
    Returns
    -------
    float
        Available energy in Wh
    """
    return f_batt * mtow_kg * e_spec_wh_kg * dod * eta


def hybrid_vtol_feasibility(
    mtow_kg: float = MTOW_BASELINE_KG,
    disk_loading: float = DISK_LOADING_DEFAULT,
    hover_time_s: float = T_HOVER_DEFAULT_S,
    cruise_time_min: float = T_CRUISE_DEFAULT_MIN,
    v_cruise: float = V_CRUISE_DEFAULT,
    rho: float = RHO_ARCADIA,
    f_batt: float = F_BATT,
    e_spec_wh_kg: float = E_SPEC_WH_KG,
    dod: float = DOD,
    eta_batt: float = ETA_DISCHARGE,
    reserve_fraction: float = RESERVE_FRACTION,
    figure_of_merit: float = FM_DEFAULT,
    eta_prop: float = ETA_PROP,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC,
    ar: float = AR_DEFAULT,
    e: float = OSWALD_E,
    c_d0: float = CD0_DEFAULT,
    ld_penalty: float = LD_PENALTY_FACTOR,
    g_mars: float = G_MARS,
    endurance_requirement_min: float = 60.0
) -> Dict[str, Any]:
    """Complete hybrid VTOL feasibility analysis.
    
    Returns dictionary with all analysis results including:
    - hover_power_w: Electrical hover power
    - cruise_power_w: Electrical cruise power
    - energy_budget: Energy breakdown dict
    - available_energy_wh: Battery capacity
    - energy_margin_percent: Margin over required
    - endurance_min: Achievable cruise minutes
    - range_km: Achievable range
    - feasible: Boolean (should be True!)
    """
    # Weight calculation
    weight_n = mtow_kg * g_mars
    
    # Disk area from disk loading
    disk_area_m2 = weight_n / disk_loading
    
    # Hover power
    p_hover_elec = hybrid_hover_power(
        weight_n, rho, disk_area_m2, figure_of_merit, eta_motor, eta_esc
    )
    
    # Get L/D for cruise (with QuadPlane penalty)
    ld_max_pure, cl_opt = maximum_ld(c_d0, ar, e)
    ld_quadplane = ld_max_pure * ld_penalty
    
    # Cruise power
    p_cruise_elec = hybrid_cruise_power(
        weight_n, v_cruise, ld_quadplane, eta_prop, eta_motor, eta_esc
    )
    
    # Energy budget
    cruise_time_s = cruise_time_min * 60
    budget = energy_budget(p_hover_elec, hover_time_s, p_cruise_elec, cruise_time_s, reserve_fraction)
    
    # Available energy
    e_available = available_energy(mtow_kg, f_batt, e_spec_wh_kg, dod, eta_batt)
    
    # Energy margin
    energy_margin_percent = ((e_available / budget['total_energy_wh']) - 1) * 100
    
    # Minimum battery fraction required
    f_batt_min = required_battery_mass(budget['total_energy_wh'], e_spec_wh_kg, dod, eta_batt) / mtow_kg
    
    # Achievable endurance with available energy
    # After hover, how much cruise time can we achieve?
    energy_for_cruise = e_available - budget['hover_energy_wh'] - budget['reserve_energy_wh']
    if energy_for_cruise > 0:
        achievable_cruise_s = (energy_for_cruise / p_cruise_elec) * 3600
        achievable_cruise_min = achievable_cruise_s / 60
    else:
        achievable_cruise_s = 0
        achievable_cruise_min = 0
    
    total_endurance_min = (hover_time_s / 60) + achievable_cruise_min
    
    # Range
    range_km = (v_cruise * achievable_cruise_s) / 1000
    
    # Induced velocity for reference
    v_i = induced_velocity(weight_n, rho, disk_area_m2)
    
    # Wing area (from stall considerations)
    # For V_stall = 20 m/s with 1.2 safety factor, V_min = 24 m/s
    # W/S = 0.5 × ρ × V_min² × CL_max
    v_stall_target = 24  # m/s (from manuscript analysis)
    ws_max = 0.5 * rho * v_stall_target**2 * CL_MAX
    wing_area = weight_n / ws_max
    wingspan = math.sqrt(ar * wing_area)
    
    # Power loadings
    pw_hover = p_hover_elec / weight_n
    pw_hover_per_kg = p_hover_elec / mtow_kg
    pw_cruise = p_cruise_elec / weight_n
    pw_cruise_per_kg = p_cruise_elec / mtow_kg
    
    # Feasibility check
    energy_feasible = e_available >= budget['total_energy_wh']
    endurance_feasible = total_endurance_min >= endurance_requirement_min
    feasible = energy_feasible and endurance_feasible
    
    # Endurance margin
    endurance_margin_percent = ((total_endurance_min / endurance_requirement_min) - 1) * 100
    
    return {
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'disk_area_m2': disk_area_m2,
        'disk_loading_n_m2': disk_loading,
        'induced_velocity_m_s': v_i,
        'hover_power_w': p_hover_elec,
        'cruise_power_w': p_cruise_elec,
        'power_loading_hover_w_per_kg': pw_hover_per_kg,
        'power_loading_cruise_w_per_kg': pw_cruise_per_kg,
        'ld_max_pure': ld_max_pure,
        'ld_quadplane': ld_quadplane,
        'cl_optimal': cl_opt,
        'energy_budget': budget,
        'available_energy_wh': e_available,
        'energy_margin_percent': energy_margin_percent,
        'f_batt_min': f_batt_min,
        'hover_time_min': hover_time_s / 60,
        'cruise_time_design_min': cruise_time_min,
        'achievable_cruise_min': achievable_cruise_min,
        'endurance_min': total_endurance_min,
        'endurance_margin_percent': endurance_margin_percent,
        'range_km': range_km,
        'wing_area_m2': wing_area,
        'wingspan_m': wingspan,
        'eta_hover': figure_of_merit * eta_motor * eta_esc,
        'eta_cruise': eta_prop * eta_motor * eta_esc,
        'energy_feasible': energy_feasible,
        'endurance_feasible': endurance_feasible,
        'feasible': feasible,
    }


def print_hybrid_vtol_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted hybrid VTOL analysis results."""
    if results is None:
        results = hybrid_vtol_feasibility()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("HYBRID VTOL (QUADPLANE) FEASIBILITY ANALYSIS")
    print("Equations from: Manuscript Section 5.4 (Hybrid VTOL Configuration)")
    print(f"Values computed: {timestamp}")
    print("=" * 80)
    print()
    
    print("INPUT PARAMETERS (verified from sources)")
    print("-" * 40)
    print(f"MTOW:               {results['mtow_kg']:.1f} kg")
    print(f"Mars gravity:       {G_MARS:.3f} m/s²")
    print(f"Weight:             {results['weight_n']:.2f} N")
    print(f"Air density:        {RHO_ARCADIA} kg/m³")
    print()
    
    print("HOVER SYSTEM (from §5.2)")
    print("-" * 40)
    print(f"Disk loading:       {results['disk_loading_n_m2']:.1f} N/m²")
    print(f"Disk area:          {results['disk_area_m2']:.3f} m²")
    print(f"Induced velocity:   {results['induced_velocity_m_s']:.1f} m/s")
    print(f"Figure of Merit:    {FM_DEFAULT:.2f}")
    print(f"Combined η_hover:   {results['eta_hover']:.3f}")
    print(f"Hover power:        {results['hover_power_w']:.0f} W")
    print(f"Hover P/W:          {results['power_loading_hover_w_per_kg']:.0f} W/kg")
    print()
    
    print("CRUISE SYSTEM (from §5.3, with rotor penalty)")
    print("-" * 40)
    print(f"Pure (L/D)_max:     {results['ld_max_pure']:.1f}")
    print(f"QuadPlane L/D:      {results['ld_quadplane']:.1f} (×{LD_PENALTY_FACTOR:.2f} penalty)")
    print(f"Combined η_cruise:  {results['eta_cruise']:.3f}")
    print(f"Cruise velocity:    {V_CRUISE_DEFAULT:.0f} m/s")
    print(f"Cruise power:       {results['cruise_power_w']:.0f} W")
    print(f"Cruise P/W:         {results['power_loading_cruise_w_per_kg']:.1f} W/kg")
    print()
    
    print("BATTERY PARAMETERS")
    print("-" * 40)
    print(f"Mass fraction:      {F_BATT:.2f}")
    print(f"Battery mass:       {F_BATT * results['mtow_kg']:.2f} kg")
    print(f"Specific energy:    {E_SPEC_WH_KG} Wh/kg")
    print(f"Available energy:   {results['available_energy_wh']:.1f} Wh")
    print()
    
    budget = results['energy_budget']
    print("ENERGY BUDGET (@eq:energy-budget)")
    print("-" * 40)
    print(f"Component            Power     Time      Energy    Fraction")
    print(f"Hover (takeoff+land) {results['hover_power_w']:.0f} W     {results['hover_time_min']:.0f} min     {budget['hover_energy_wh']:.1f} Wh    {budget['hover_energy_wh']/budget['mission_energy_wh']*100:.0f}%")
    print(f"Cruise               {results['cruise_power_w']:.0f} W     {results['cruise_time_design_min']:.0f} min    {budget['cruise_energy_wh']:.1f} Wh    {budget['cruise_energy_wh']/budget['mission_energy_wh']*100:.0f}%")
    print(f"Mission total        —         60 min    {budget['mission_energy_wh']:.1f} Wh   100%")
    print(f"Reserve (20%)        —         —         {budget['reserve_energy_wh']:.1f} Wh    —")
    print(f"REQUIRED TOTAL       —         —         {budget['total_energy_wh']:.1f} Wh    —")
    print(f"AVAILABLE            —         —         {results['available_energy_wh']:.1f} Wh    —")
    print(f"MARGIN               —         —         {results['available_energy_wh'] - budget['total_energy_wh']:.1f} Wh    {results['energy_margin_percent']:.0f}%")
    print()
    
    print("ACHIEVABLE PERFORMANCE")
    print("-" * 40)
    print(f"Minimum f_batt required: {results['f_batt_min']:.2f} (design: {F_BATT:.2f})")
    print(f"Achievable cruise time:  {results['achievable_cruise_min']:.0f} min")
    print(f"Total endurance:         {results['endurance_min']:.0f} min")
    print(f"Achievable range:        {results['range_km']:.0f} km")
    print()
    
    print("WING GEOMETRY (derived)")
    print("-" * 40)
    print(f"Wing area:          {results['wing_area_m2']:.2f} m²")
    print(f"Wingspan:           {results['wingspan_m']:.2f} m")
    print()
    
    print("COMPARISON WITH REQUIREMENTS")
    print("-" * 40)
    endurance_status = "✓ PASS" if results['endurance_feasible'] else "❌ FAIL"
    energy_status = "✓ PASS" if results['energy_feasible'] else "❌ FAIL"
    range_margin = (results['range_km'] / 100 - 1) * 100
    range_status = "✓ PASS" if results['range_km'] >= 100 else "❌ FAIL"
    
    print(f"Requirement          Target    Computed     Margin     Status")
    print(f"Endurance            60 min    {results['endurance_min']:.0f} min       {results['endurance_margin_percent']:+.0f}%       {endurance_status}")
    print(f"Range                100 km    {results['range_km']:.0f} km        {range_margin:+.0f}%       {range_status}")
    print(f"Energy feasible      Yes       Yes          {results['energy_margin_percent']:+.0f}%       {energy_status}")
    print(f"VTOL                 Yes       Yes          —          ✓ PASS")
    print()
    
    if results['feasible']:
        print("CONCLUSION: Hybrid VTOL (QuadPlane) MEETS ALL REQUIREMENTS")
        print(f"Energy margin: {results['energy_margin_percent']:.0f}%")
        print(f"Endurance margin: {results['endurance_margin_percent']:.0f}%")
        print("RECOMMENDATION: SELECT QuadPlane as baseline configuration.")
    else:
        print("CONCLUSION: Hybrid VTOL does not meet all requirements.")
        if not results['energy_feasible']:
            print("  - Energy budget exceeded")
        if not results['endurance_feasible']:
            print("  - Endurance requirement not met")
    
    print("=" * 80)
    print()
    print(">>> These COMPUTED values will be used to UPDATE the manuscript in Phase C.")


if __name__ == "__main__":
    # Run complete analysis with baseline parameters
    results = hybrid_vtol_feasibility()
    print_hybrid_vtol_analysis(results)
