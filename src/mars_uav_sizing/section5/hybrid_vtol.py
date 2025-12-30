"""
Hybrid VTOL (QuadPlane) Configuration Analysis
================================================

Implements equations from manuscript Section 5.3 (Hybrid VTOL Configuration).
Combines hover analysis from §5.1 with cruise analysis from §5.2.
All parameters loaded from configuration - NO HARDCODED VALUES.

Key insight: By limiting hover to ~2 minutes (3% of flight time), explicitly
accounting for transition phases (~1 minute), and exploiting fixed-wing
aerodynamics for the remaining 57 minutes, the QuadPlane achieves a
fundamentally different energy budget than rotorcraft.

Equations implemented:
    @eq:hover-power-qp       - Hover power (same as rotorcraft)
    @eq:cruise-power-qp      - Cruise power with L/D penalty
    @eq:transition-energy    - Transition energy (conservative estimate)
    @eq:energy-budget        - Total energy requirement (hover + transition + cruise)
    @eq:energy-available     - Available battery energy
    @eq:energy-feasibility   - Feasibility check

Reference:
    - Manuscript: sections_en/05_03_hybrid-vtol-configuration-sec-hybrid-vtol-analysis.md
    - Bertani et al. (2023), Preliminary Design of a Fixed-Wing Drone for Mars
    - Goetzendorf-Grabowski (ICAS 2022), Transition energy optimization
    - Mathur & Atkins (MDPI 2025), Multi-mode flight simulation

Last Updated: 2025-12-30
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

# Import from sibling modules
from .rotorcraft import electric_hover_power, induced_velocity_from_disk_loading
from .fixed_wing import maximum_ld, cruise_power, stall_wing_loading_limit


# =============================================================================
# QUADPLANE SPECIFIC PARAMETERS
# =============================================================================

def get_quadplane_ld() -> float:
    """
    Get L/D for QuadPlane accounting for rotor drag penalty.
    
    Implements @eq:ld-quadplane from §5.3:
        (L/D)_QuadPlane = penalty_factor × (L/D)_pure
    
    Returns
    -------
    float
        QuadPlane L/D (reduced from pure fixed-wing)
    """
    ld_max, _ = maximum_ld()
    penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    return ld_max * penalty


# =============================================================================
# HOVER ANALYSIS (§5.3.1)
# =============================================================================

def quadplane_hover_power() -> float:
    """
    Calculate QuadPlane hover power.
    
    Identical to rotorcraft hover power analysis.
    Uses lift rotors only during takeoff/landing.
    
    Returns
    -------
    float
        Electrical hover power in Watts
    """
    return electric_hover_power()


def quadplane_hover_energy() -> float:
    """
    Calculate energy consumed during hover phases.
    
    Implements @eq:hover-energy from §5.3:
        E_hover = P_hover × t_hover
    
    Returns
    -------
    float
        Hover energy in Wh
    """
    p_hover = quadplane_hover_power()
    t_hover_s = get_param('mission.time.t_hover_s')
    return p_hover * (t_hover_s / 3600)  # Convert to Wh


# =============================================================================
# CRUISE ANALYSIS (§5.3.2)
# =============================================================================

def quadplane_cruise_power() -> float:
    """
    Calculate QuadPlane cruise power.
    
    Same as fixed-wing but with reduced L/D due to stopped rotor drag.
    
    Implements @eq:cruise-power-qp from §5.3:
        P_cruise = W×V / ((L/D)_qp × η_cruise)
    
    Returns
    -------
    float
        Electrical cruise power in Watts
    """
    g_mars = get_mars_gravity()
    mtow_kg = get_mtow()
    weight_n = mtow_kg * g_mars
    v_cruise = get_mission_params()['v_cruise']
    
    ld_qp = get_quadplane_ld()
    return cruise_power(weight_n, v_cruise, ld_qp)


def quadplane_cruise_energy() -> float:
    """
    Calculate energy consumed during cruise phase.
    
    Implements @eq:cruise-energy from §5.3:
        E_cruise = P_cruise × t_cruise
    
    Returns
    -------
    float
        Cruise energy in Wh
    """
    p_cruise = quadplane_cruise_power()
    t_cruise_min = get_param('mission.time.t_cruise_min')
    return p_cruise * (t_cruise_min / 60)  # Convert to Wh


# =============================================================================
# TRANSITION ANALYSIS (§5.3.2b - Conservative Estimate)
# =============================================================================
# References:
#   [@goetzendorf-grabowskiOptimizationEnergyConsumption2022] - Transition energy optimization
#   [@mathurMultiModeFlightSimulation2025] - Multi-mode flight simulation
#   [@zhaoDevelopmentMultimodeFlight2023] - Transition corridor theory

def transition_energy_estimate() -> Dict[str, float]:
    """
    Estimate energy consumed during transition phases.

    The transition phase from hover to cruise (and back) consumes significant
    energy but is often omitted in preliminary studies. This function provides
    a conservative estimate based on literature data.

    Reference: Goetzendorf-Grabowski (ICAS 2022) measured ~45 kJ per transition
    for a 10 kg quad-plane on Earth. The energy is scaled for Mars conditions.

    Note: During transition, hybrid mode can consume MORE power than pure hover
    at certain airspeeds due to the additional forward thrust requirement while
    lift rotors are still active (Mathur & Atkins 2025).

    Returns
    -------
    dict
        Transition energy analysis with conservative estimates
    """
    # Load transition parameters
    n_transitions = get_param('mission.time.n_transitions')
    reference_energy_j = get_param('mission.transition.reference_energy_j')
    mars_scaling = get_param('mission.transition.mars_scaling_factor')

    # Reference values for scaling
    ref_mtow_kg = get_param('mission.transition.reference_mtow_kg')
    actual_mtow_kg = get_mtow()

    # Convert J to Wh
    J_PER_WH = 3600.0

    # Scale transition energy by mass ratio (conservative linear scaling)
    mass_ratio = actual_mtow_kg / ref_mtow_kg
    scaled_energy_j = reference_energy_j * mass_ratio * mars_scaling

    # Total transition energy
    total_transition_j = scaled_energy_j * n_transitions
    total_transition_wh = total_transition_j / J_PER_WH

    # Per-transition values
    per_transition_j = scaled_energy_j
    per_transition_wh = per_transition_j / J_PER_WH

    return {
        'n_transitions': n_transitions,
        'reference_energy_j': reference_energy_j,
        'mars_scaling_factor': mars_scaling,
        'per_transition_j': per_transition_j,
        'per_transition_wh': per_transition_wh,
        'total_transition_j': total_transition_j,
        'total_transition_wh': total_transition_wh,
    }


def transition_energy_impact(hover_energy_wh: float, mission_energy_wh: float) -> Dict[str, float]:
    """
    Calculate the impact of transition energy on overall energy budget.

    This function quantifies how transition energy affects margins and
    compares it to hover energy (which it is often lumped into).

    Parameters
    ----------
    hover_energy_wh : float
        Pure hover energy (excluding transition)
    mission_energy_wh : float
        Total mission energy (hover + cruise, without transition)

    Returns
    -------
    dict
        Impact analysis
    """
    trans = transition_energy_estimate()
    e_transition = trans['total_transition_wh']

    # Fraction of hover energy
    if hover_energy_wh > 0:
        fraction_of_hover = (e_transition / hover_energy_wh) * 100
    else:
        fraction_of_hover = 0.0

    # Fraction of mission energy
    if mission_energy_wh > 0:
        fraction_of_mission = (e_transition / mission_energy_wh) * 100
    else:
        fraction_of_mission = 0.0

    return {
        'transition_energy_wh': e_transition,
        'fraction_of_hover_percent': fraction_of_hover,
        'fraction_of_mission_percent': fraction_of_mission,
    }


# =============================================================================
# ENERGY BUDGET (§5.3.3)
# =============================================================================

def energy_budget() -> Dict[str, float]:
    """
    Calculate complete energy budget including transition phases.

    Implements @eq:energy-required from §5.3:
        E_required = (E_hover + E_transition + E_cruise) × (1 + reserve)

    Returns
    -------
    dict
        Energy budget breakdown
    """
    e_hover = quadplane_hover_energy()
    e_cruise = quadplane_cruise_energy()
    trans = transition_energy_estimate()
    e_transition = trans['total_transition_wh']
    reserve = get_param('mission.energy.reserve_fraction')

    e_mission = e_hover + e_transition + e_cruise
    e_reserve = e_mission * reserve
    e_required = e_mission + e_reserve

    return {
        'hover_wh': e_hover,
        'transition_wh': e_transition,
        'cruise_wh': e_cruise,
        'mission_wh': e_mission,
        'reserve_wh': e_reserve,
        'required_wh': e_required,
    }


def available_energy() -> float:
    """
    Calculate available energy from battery.
    
    Implements @eq:energy-available from §5.3:
        E_available = f_batt × MTOW × e_spec × DoD × η_batt
    
    Returns
    -------
    float
        Available energy in Wh
    """
    mtow_kg = get_mtow()
    batt = get_battery_params()
    f_batt = get_mission_params()['f_batt']
    
    return (
        f_batt 
        * mtow_kg 
        * batt['e_spec_Wh_kg'] 
        * batt['dod'] 
        * batt['eta_discharge']
    )


def energy_margin() -> Dict[str, float]:
    """
    Calculate energy margin (feasibility check).
    
    Implements @eq:energy-feasibility from §5.3:
        Mission feasible if E_available >= E_required
    
    Returns
    -------
    dict
        Energy margin analysis
    """
    budget = energy_budget()
    e_available = available_energy()
    e_required = budget['required_wh']
    
    margin_wh = e_available - e_required
    margin_percent = (margin_wh / e_required) * 100
    feasible = e_available >= e_required
    
    return {
        'available_wh': e_available,
        'required_wh': e_required,
        'margin_wh': margin_wh,
        'margin_percent': margin_percent,
        'feasible': feasible,
    }


# =============================================================================
# FEASIBILITY ANALYSIS (§5.3.4)
# =============================================================================

def hybrid_vtol_feasibility_analysis() -> Dict[str, Any]:
    """
    Complete hybrid VTOL (QuadPlane) feasibility analysis.
    
    Loads all parameters from configuration and computes:
    - Hover power and energy
    - Cruise power and energy
    - Complete energy budget with reserve
    - Achievable endurance and range
    - Energy margin assessment
    
    Returns
    -------
    dict
        Complete analysis results
    """
    # Load all parameters from config
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    endurance_req = get_param('mission.requirements.endurance_min')
    disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    ld_penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    
    # Derived values
    weight_n = mtow_kg * g_mars
    disk_area_m2 = weight_n / disk_loading
    v_cruise = mission['v_cruise']
    t_hover_s = mission['t_hover_s']
    t_cruise_min = mission['t_cruise_min']
    
    # L/D values
    ld_max, cl_opt = maximum_ld()
    ld_quadplane = ld_max * ld_penalty
    
    # Hover power
    p_hover = electric_hover_power()
    
    # Cruise power
    eta_cruise = prop['eta_prop'] * prop['eta_motor'] * prop['eta_esc']
    p_cruise = cruise_power(weight_n, v_cruise, ld_quadplane)
    
    # Induced velocity
    v_i = induced_velocity_from_disk_loading(disk_loading, rho)
    
    # Combined efficiencies
    eta_hover = prop['figure_of_merit'] * prop['eta_motor'] * prop['eta_esc']
    
    # Energy budget (with transition)
    e_hover = p_hover * (t_hover_s / 3600)
    e_cruise = p_cruise * (t_cruise_min / 60)

    # Transition energy estimate (conservative)
    trans = transition_energy_estimate()
    e_transition = trans['total_transition_wh']

    # Total mission energy includes transition
    e_mission_without_trans = e_hover + e_cruise
    e_mission = e_hover + e_transition + e_cruise
    e_reserve = e_mission * mission['energy_reserve']
    e_required = e_mission + e_reserve

    # Calculate transition impact
    trans_impact = transition_energy_impact(e_hover, e_mission_without_trans)
    
    # Available energy
    battery_mass_kg = mission['f_batt'] * mtow_kg
    total_energy_wh = battery_mass_kg * batt['e_spec_Wh_kg']
    usable_energy_wh = total_energy_wh * batt['dod'] * batt['eta_discharge']
    
    # Energy margin
    margin_wh = usable_energy_wh - e_required
    margin_percent = (margin_wh / e_required) * 100 if e_required > 0 else 0
    
    # Achievable endurance (with current energy)
    # Endurance = t_hover + t_transition + (E_available - E_hover - E_transition - E_reserve) / P_cruise
    t_transition_s = get_param('mission.time.t_transition_s')
    e_for_cruise = usable_energy_wh * (1 - mission['energy_reserve']) - e_hover - e_transition
    if e_for_cruise > 0 and p_cruise > 0:
        cruise_time_min = (e_for_cruise / p_cruise) * 60
    else:
        cruise_time_min = 0

    total_endurance_min = (t_hover_s / 60) + (t_transition_s / 60) + cruise_time_min
    
    # Range
    range_km = (v_cruise * cruise_time_min * 60) / 1000
    operational_radius_km = range_km / 2  # Round trip
    
    # Feasibility assessment
    feasible = usable_energy_wh >= e_required
    endurance_passes = total_endurance_min >= endurance_req
    
    return {
        # Input parameters
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'rho_kg_m3': rho,
        'v_cruise_m_s': v_cruise,
        'disk_loading_n_m2': disk_loading,
        'disk_area_m2': disk_area_m2,
        
        # L/D values
        'ld_max_pure': ld_max,
        'ld_penalty_factor': ld_penalty,
        'ld_quadplane': ld_quadplane,
        
        # Efficiencies
        'figure_of_merit': prop['figure_of_merit'],
        'eta_motor': prop['eta_motor'],
        'eta_esc': prop['eta_esc'],
        'eta_prop': prop['eta_prop'],
        'eta_hover': eta_hover,
        'eta_cruise': eta_cruise,
        
        # Power
        'induced_velocity_m_s': v_i,
        'hover_power_w': p_hover,
        'cruise_power_w': p_cruise,
        
        # Time allocations
        'hover_time_min': t_hover_s / 60,
        'cruise_time_min': cruise_time_min,
        
        # Energy budget (including transition)
        'hover_energy_wh': e_hover,
        'transition_energy_wh': e_transition,
        'cruise_energy_wh': e_cruise,
        'mission_energy_wh': e_mission,
        'mission_energy_without_trans_wh': e_mission_without_trans,
        'reserve_energy_wh': e_reserve,
        'required_energy_wh': e_required,

        # Transition analysis
        'transition_per_phase_j': trans['per_transition_j'],
        'transition_per_phase_wh': trans['per_transition_wh'],
        'n_transitions': trans['n_transitions'],
        'transition_fraction_of_hover': trans_impact['fraction_of_hover_percent'],
        'transition_fraction_of_mission': trans_impact['fraction_of_mission_percent'],
        
        # Battery
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'usable_energy_wh': usable_energy_wh,
        
        # Margin
        'margin_wh': margin_wh,
        'margin_percent': margin_percent,
        
        # Performance
        'endurance_min': total_endurance_min,
        'range_km': range_km,
        'operational_radius_km': operational_radius_km,
        
        # Assessment
        'requirement_min': endurance_req,
        'feasible': feasible and endurance_passes,
        'endurance_passes': endurance_passes,
        'energy_feasible': feasible,
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted hybrid VTOL analysis results."""
    if results is None:
        results = hybrid_vtol_feasibility_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("HYBRID VTOL (QUADPLANE) FEASIBILITY ANALYSIS (Section 5.3)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()
    
    print("INPUT PARAMETERS (from configuration)")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m³")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print(f"  Disk loading:       {results['disk_loading_n_m2']:.1f} N/m²")
    print()
    
    print("AERODYNAMIC EFFICIENCY")
    print("-" * 50)
    print(f"  Pure wing (L/D)max: {results['ld_max_pure']:.2f}")
    print(f"  Penalty factor:     {results['ld_penalty_factor']:.2f} (stopped rotors)")
    print(f"  QuadPlane L/D:      {results['ld_quadplane']:.2f}")
    print()
    
    print("HOVER ANALYSIS (Lift rotors)")
    print("-" * 50)
    print(f"  Induced velocity:   {results['induced_velocity_m_s']:.2f} m/s")
    print(f"  Hover power:        {results['hover_power_w']:.0f} W")
    print(f"  Hover time:         {results['hover_time_min']:.0f} min")
    print(f"  Hover energy:       {results['hover_energy_wh']:.1f} Wh")
    print()
    
    print("CRUISE ANALYSIS (Wing + cruise motor)")
    print("-" * 50)
    print(f"  Cruise power:       {results['cruise_power_w']:.1f} W")
    print(f"  Cruise time:        {results['cruise_time_min']:.1f} min")
    print(f"  Cruise energy:      {results['cruise_energy_wh']:.1f} Wh")
    print()

    print("TRANSITION ANALYSIS (Conservative estimate)")
    print("-" * 50)
    print(f"  Number of transitions:  {results['n_transitions']}")
    print(f"  Energy per transition:  {results['transition_per_phase_wh']:.1f} Wh ({results['transition_per_phase_j']:.0f} J)")
    print(f"  Total transition energy:{results['transition_energy_wh']:.1f} Wh")
    print(f"  Fraction of hover:      {results['transition_fraction_of_hover']:.1f}%")
    print(f"  Fraction of mission:    {results['transition_fraction_of_mission']:.1f}%")
    print("  Note: Transition energy conservatively lumped into budget.")
    print("  Reference: Goetzendorf-Grabowski (ICAS 2022), Mathur & Atkins (2025)")
    print()

    hover_frac = results['hover_energy_wh'] / results['mission_energy_wh'] * 100
    trans_frac = results['transition_energy_wh'] / results['mission_energy_wh'] * 100
    cruise_frac = results['cruise_energy_wh'] / results['mission_energy_wh'] * 100

    print("ENERGY BUDGET (with transition)")
    print("-" * 50)
    print(f"  Mission energy:     {results['mission_energy_wh']:.1f} Wh")
    print(f"    - Hover:          {results['hover_energy_wh']:.1f} Wh ({hover_frac:.0f}%)")
    print(f"    - Transition:     {results['transition_energy_wh']:.1f} Wh ({trans_frac:.0f}%)")
    print(f"    - Cruise:         {results['cruise_energy_wh']:.1f} Wh ({cruise_frac:.0f}%)")
    print(f"  Reserve (20%):      {results['reserve_energy_wh']:.1f} Wh")
    print(f"  Required total:     {results['required_energy_wh']:.1f} Wh")
    print(f"  Available:          {results['usable_energy_wh']:.1f} Wh")
    print(f"  Margin:             {results['margin_wh']:.1f} Wh ({results['margin_percent']:.1f}%)")
    print()
    
    print("PERFORMANCE")
    print("-" * 50)
    print(f"  Total endurance:    {results['endurance_min']:.1f} min")
    print(f"  Range:              {results['range_km']:.0f} km")
    print(f"  Operational radius: {results['operational_radius_km']:.0f} km")
    print()
    
    print("FEASIBILITY ASSESSMENT")
    print("-" * 50)
    vtol_status = "[PASS] (lift rotors)"
    end_status = "[PASS]" if results['endurance_passes'] else "[FAIL]"
    energy_status = "[PASS]" if results['energy_feasible'] else "[FAIL]"
    overall = "[PASS]" if results['feasible'] else "[FAIL]"

    margin = (results['endurance_min'] / results['requirement_min'] - 1) * 100

    print(f"  VTOL capability:    {vtol_status}")
    print(f"  Energy constraint:  {energy_status} ({results['margin_percent']:+.1f}% margin)")
    print(f"  Endurance req:      {results['requirement_min']:.0f} min -> {results['endurance_min']:.0f} min ({margin:+.1f}%) -> {end_status}")
    print(f"  Overall:            {overall}")
    print()
    
    if results['feasible']:
        print("CONCLUSION: Hybrid VTOL (QuadPlane) SATISFIES all requirements.")
        print(f"           Endurance margin of {margin:.0f}% provides adequate safety buffer.")
        print("           VTOL capability enables Mars operations without runway.")
    else:
        print("CONCLUSION: Hybrid VTOL fails one or more requirements.")
    
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_analysis()
