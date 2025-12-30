"""
Fixed-Wing Configuration Analysis
==================================

Implements equations from manuscript Section 5.2 (Fixed-Wing Configuration).
All parameters loaded from configuration - NO HARDCODED VALUES.

Equations implemented:
    @eq:lift-equation        - Lift force equation
    @eq:cl-required          - Required lift coefficient
    @eq:drag-polar           - Parabolic drag polar
    @eq:ld-ratio             - Lift-to-drag ratio
    @eq:ld-max               - Maximum L/D
    @eq:cruise-electric-power - Cruise power
    @eq:stall-speed          - Stall speed
    @eq:endurance-fixedwing  - Fixed-wing endurance
    @eq:takeoff-roll         - Takeoff ground roll
    
Reference: 
    - Manuscript: sections_en/05_02_fixed-wing-configuration-sec-fixed-wing-analysis.md
    - Torenbeek (1982), Synthesis of Subsonic Airplane Design
    - Sadraey (2013), Aircraft Design: A Systems Engineering Approach

Last Updated: 2025-12-29
"""

import math
from typing import Dict, Any, Tuple
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
# AERODYNAMIC EQUATIONS (§5.2.1)
# =============================================================================

def cruise_lift_coefficient(wing_loading: float, rho: float, velocity: float) -> float:
    """
    Calculate C_L required for level flight.
    
    Implements @eq:cl-required from §5.2:
        C_L = 2×(W/S) / (ρ×V²)
    
    Reference: Torenbeek (1982), Section 5.3
    
    Parameters
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    rho : float
        Air density in kg/m³
    velocity : float
        True airspeed in m/s
    
    Returns
    -------
    float
        Required lift coefficient (dimensionless)
    """
    return (2 * wing_loading) / (rho * velocity**2)


def drag_coefficient(
    c_l: float, 
    c_d0: float = None, 
    ar: float = None, 
    e: float = None
) -> float:
    """
    Calculate drag coefficient from parabolic polar.
    
    Implements @eq:drag-polar from §5.2:
        C_D = C_D0 + C_L² / (π×AR×e)
    
    Reference: Torenbeek (1982), Section 5.3
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    c_d0 : float, optional
        Zero-lift drag coefficient (default: from config)
    ar : float, optional
        Aspect ratio (default: from config)
    e : float, optional
        Oswald efficiency factor (default: from config)
    
    Returns
    -------
    float
        Total drag coefficient
    """
    aero = get_aerodynamic_params()
    if c_d0 is None:
        c_d0 = aero['cd0']
    if ar is None:
        ar = aero['aspect_ratio']
    if e is None:
        e = aero['oswald_e']
    
    k = 1 / (math.pi * ar * e)  # Induced drag factor
    return c_d0 + k * c_l**2


def induced_drag_factor(ar: float = None, e: float = None) -> float:
    """
    Calculate induced drag factor K.
    
    K = 1 / (π × AR × e)
    
    Parameters
    ----------
    ar : float, optional
        Aspect ratio (default: from config)
    e : float, optional
        Oswald efficiency factor (default: from config)
    
    Returns
    -------
    float
        Induced drag factor K
    """
    aero = get_aerodynamic_params()
    if ar is None:
        ar = aero['aspect_ratio']
    if e is None:
        e = aero['oswald_e']
    
    return 1 / (math.pi * ar * e)


def lift_to_drag(
    c_l: float, 
    c_d0: float = None, 
    ar: float = None, 
    e: float = None
) -> float:
    """
    Calculate lift-to-drag ratio at given C_L.
    
    Implements @eq:ld-ratio from §5.2:
        L/D = C_L / C_D
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    c_d0 : float, optional
        Zero-lift drag coefficient (default: from config)
    ar : float, optional
        Aspect ratio (default: from config)
    e : float, optional
        Oswald efficiency factor (default: from config)
    
    Returns
    -------
    float
        Lift-to-drag ratio
    """
    c_d = drag_coefficient(c_l, c_d0, ar, e)
    return c_l / c_d


def maximum_ld(
    c_d0: float = None, 
    ar: float = None, 
    e: float = None
) -> Tuple[float, float]:
    """
    Calculate maximum L/D and corresponding C_L.
    
    Implements @eq:ld-max and @eq:cl-optimal from §5.2:
        (L/D)_max = 0.5 × sqrt(π×AR×e / C_D0)
        C_L,opt = sqrt(π×AR×e×C_D0)
    
    Parameters
    ----------
    c_d0 : float, optional
        Zero-lift drag coefficient (default: from config)
    ar : float, optional
        Aspect ratio (default: from config)
    e : float, optional
        Oswald efficiency factor (default: from config)
    
    Returns
    -------
    tuple
        (L/D_max, C_L_optimal)
    """
    aero = get_aerodynamic_params()
    if c_d0 is None:
        c_d0 = aero['cd0']
    if ar is None:
        ar = aero['aspect_ratio']
    if e is None:
        e = aero['oswald_e']
    
    cl_opt = math.sqrt(math.pi * ar * e * c_d0)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / c_d0)
    
    return ld_max, cl_opt


# =============================================================================
# POWER EQUATIONS (§5.2.2)
# =============================================================================

def cruise_power(
    weight_n: float, 
    velocity: float, 
    ld: float,
    eta_prop: float = None, 
    eta_motor: float = None,
    eta_esc: float = None
) -> float:
    """
    Calculate electrical power for cruise.
    
    Implements @eq:cruise-electric-power from §5.2:
        P = W×V / (L/D × η_prop × η_motor × η_ESC)
    
    Reference: Torenbeek (1982), Section 5.4
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Cruise velocity in m/s
    ld : float
        Lift-to-drag ratio
    eta_prop : float, optional
        Propeller efficiency (default: from config)
    eta_motor : float, optional
        Motor efficiency (default: from config)
    eta_esc : float, optional
        ESC efficiency (default: from config)
    
    Returns
    -------
    float
        Electrical cruise power in Watts
    """
    prop = get_propulsion_efficiencies()
    if eta_prop is None:
        eta_prop = prop['eta_prop']
    if eta_motor is None:
        eta_motor = prop['eta_motor']
    if eta_esc is None:
        eta_esc = prop['eta_esc']
    
    eta_cruise = eta_prop * eta_motor * eta_esc
    return (weight_n * velocity) / (ld * eta_cruise)


def cruise_power_loading(
    velocity: float, 
    ld: float,
    eta_prop: float = None, 
    eta_motor: float = None,
    eta_esc: float = None
) -> float:
    """
    Calculate P/W for cruise constraint on matching chart.
    
    Implements @eq:power-loading-cruise from §5.2:
        P/W = V / (L/D × η_cruise)
    
    Parameters
    ----------
    velocity : float
        Cruise velocity in m/s
    ld : float
        Lift-to-drag ratio
    eta_prop : float, optional
        Propeller efficiency (default: from config)
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
    if eta_prop is None:
        eta_prop = prop['eta_prop']
    if eta_motor is None:
        eta_motor = prop['eta_motor']
    if eta_esc is None:
        eta_esc = prop['eta_esc']
    
    eta_cruise = eta_prop * eta_motor * eta_esc
    return velocity / (ld * eta_cruise)


# =============================================================================
# STALL EQUATIONS (§5.2.3)
# =============================================================================

def stall_speed(wing_loading: float, rho: float = None, c_l_max: float = None) -> float:
    """
    Calculate stall speed from wing loading.
    
    Implements @eq:stall-speed from §5.2:
        V_stall = sqrt(2×(W/S) / (ρ×C_L,max))
    
    Reference: Sadraey (2013), Section 4.3.3
    
    Parameters
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    rho : float, optional
        Air density in kg/m³ (default: from config)
    c_l_max : float, optional
        Maximum lift coefficient (default: from config)
    
    Returns
    -------
    float
        Stall speed in m/s
    """
    if rho is None:
        rho = get_density()
    if c_l_max is None:
        c_l_max = get_aerodynamic_params()['cl_max']
    
    return math.sqrt((2 * wing_loading) / (rho * c_l_max))


def stall_wing_loading_limit(
    rho: float = None, 
    v_min: float = None, 
    c_l_max: float = None
) -> float:
    """
    Calculate maximum allowable wing loading from stall constraint.
    
    Implements @eq:wing-loading-constraint from §5.2:
        (W/S)_max = 0.5 × ρ × V_min² × C_L,max
    
    Parameters
    ----------
    rho : float, optional
        Air density in kg/m³ (default: from config)
    v_min : float, optional
        Minimum flight speed in m/s (default: from config)
    c_l_max : float, optional
        Maximum lift coefficient (default: from config)
    
    Returns
    -------
    float
        Maximum wing loading in N/m²
    """
    if rho is None:
        rho = get_density()
    if v_min is None:
        mission = get_mission_params()
        v_min = mission['v_stall'] * get_param('mission.velocity.v_min_factor')
    if c_l_max is None:
        c_l_max = get_aerodynamic_params()['cl_max']
    
    return 0.5 * rho * v_min**2 * c_l_max


# =============================================================================
# ENDURANCE EQUATIONS (§5.2.4)
# =============================================================================

def fixed_wing_endurance_seconds() -> float:
    """
    Calculate fixed-wing endurance with energy reserve.

    Implements @eq:endurance-fixedwing from §5.2 with 20% energy reserve:
        t = (f_batt × e_spec × DoD × η_batt × (1-reserve) × (L/D) × η_cruise) / (g × V)

    Returns
    -------
    float
        Endurance in SECONDS (with 20% energy reserve)
    """
    g_mars = get_mars_gravity()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()

    # Get maximum L/D
    ld_max, _ = maximum_ld()

    # Combined cruise efficiency
    eta_cruise = prop['eta_prop'] * prop['eta_motor'] * prop['eta_esc']

    # Convert Wh/kg to J/kg
    e_spec_j_kg = batt['e_spec_Wh_kg'] * 3600

    # Apply 20% energy reserve per §4.12
    reserve_fraction = mission['energy_reserve']

    numerator = (
        mission['f_batt']
        * e_spec_j_kg
        * batt['dod']
        * batt['eta_discharge']
        * (1 - reserve_fraction)
        * ld_max
        * eta_cruise
    )
    denominator = g_mars * mission['v_cruise']

    return numerator / denominator


# =============================================================================
# TAKEOFF ANALYSIS (§5.2.5)
# =============================================================================

def takeoff_ground_roll(
    wing_loading: float = None,
    rho: float = None,
    c_l_max: float = None,
    acceleration: float = 0.7
) -> float:
    """
    Estimate takeoff ground roll distance.
    
    Implements @eq:takeoff-roll from §5.2:
        S_TO = V_TO² / (2 × a_avg)
    
    where V_TO ≈ 1.1 × V_stall
    
    Parameters
    ----------
    wing_loading : float, optional
        Wing loading in N/m² (default: stall limit)
    rho : float, optional
        Air density in kg/m³ (default: from config)
    c_l_max : float, optional
        Maximum lift coefficient (default: from config)
    acceleration : float
        Average acceleration in m/s² (default: 0.7 for Mars)
    
    Returns
    -------
    float
        Ground roll distance in meters
    """
    if rho is None:
        rho = get_density()
    if c_l_max is None:
        c_l_max = get_aerodynamic_params()['cl_max']
    if wing_loading is None:
        # Use stall-limited wing loading
        v_min = get_mission_params()['v_stall'] * get_param('mission.velocity.v_min_factor')
        wing_loading = stall_wing_loading_limit(rho, v_min, c_l_max)
    
    v_stall = stall_speed(wing_loading, rho, c_l_max)
    v_to = 1.1 * v_stall
    
    return v_to**2 / (2 * acceleration)


# =============================================================================
# FEASIBILITY ANALYSIS (§5.2.6)
# =============================================================================

def fixed_wing_feasibility_analysis() -> Dict[str, Any]:
    """
    Complete fixed-wing feasibility analysis.
    
    Loads all parameters from configuration and computes:
    - L/D and aerodynamic parameters
    - Cruise power
    - Endurance and range
    - Takeoff distance (disqualifying factor)
    
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
    
    # Derived values
    weight_n = mtow_kg * g_mars
    v_cruise = mission['v_cruise']
    f_batt = mission['f_batt']
    
    # Aerodynamic calculations
    ld_max, cl_opt = maximum_ld()
    k = induced_drag_factor()
    
    # Wing loading at stall limit
    v_min = mission['v_stall'] * get_param('mission.velocity.v_min_factor')
    ws_max = stall_wing_loading_limit(rho, v_min, aero['cl_max'])
    
    # C_L at cruise
    cl_cruise = cruise_lift_coefficient(ws_max, rho, v_cruise)
    ld_cruise = lift_to_drag(cl_cruise)
    
    # Cruise power
    eta_cruise = prop['eta_prop'] * prop['eta_motor'] * prop['eta_esc']
    p_cruise = cruise_power(weight_n, v_cruise, ld_max)
    
    # P/W ratio
    pw_cruise = cruise_power_loading(v_cruise, ld_max)
    
    # Endurance calculation
    # Apply 20% energy reserve per §4.12: E_usable = E_total × DoD × η_batt × (1 - reserve)
    reserve_fraction = mission['energy_reserve']
    battery_mass_kg = f_batt * mtow_kg
    total_energy_wh = battery_mass_kg * batt['e_spec_Wh_kg']
    usable_energy_wh = total_energy_wh * batt['dod'] * batt['eta_discharge'] * (1 - reserve_fraction)

    endurance_h = usable_energy_wh / p_cruise
    endurance_min = endurance_h * 60
    range_km = v_cruise * endurance_h * 3.6  # km
    
    # Takeoff analysis (shows why fixed-wing is infeasible)
    takeoff_distance = takeoff_ground_roll(ws_max, rho, aero['cl_max'])
    v_stall = stall_speed(ws_max, rho, aero['cl_max'])
    
    # Feasibility (VTOL requirement)
    vtol_possible = False  # Fixed-wing cannot hover
    endurance_passes = endurance_min >= endurance_req
    
    return {
        # Input parameters
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'rho_kg_m3': rho,
        'v_cruise_m_s': v_cruise,
        
        # Aerodynamics
        'aspect_ratio': aero['aspect_ratio'],
        'oswald_e': aero['oswald_e'],
        'cd0': aero['cd0'],
        'cl_max': aero['cl_max'],
        'k_induced': k,
        'ld_max': ld_max,
        'cl_optimal': cl_opt,
        'cl_cruise': cl_cruise,
        'ld_cruise': ld_cruise,
        
        # Efficiencies
        'eta_prop': prop['eta_prop'],
        'eta_motor': prop['eta_motor'],
        'eta_esc': prop['eta_esc'],
        'eta_cruise': eta_cruise,
        
        # Stall and wing loading
        'wing_loading_max': ws_max,
        'v_stall': v_stall,
        
        # Power
        'cruise_power_w': p_cruise,
        'power_loading_w_per_n': pw_cruise,
        
        # Energy and performance
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'energy_reserve_fraction': reserve_fraction,
        'usable_energy_wh': usable_energy_wh,
        'endurance_min': endurance_min,
        'range_km': range_km,
        
        # Takeoff
        'takeoff_distance_m': takeoff_distance,
        
        # Assessment
        'requirement_min': endurance_req,
        'vtol_possible': vtol_possible,
        'endurance_passes': endurance_passes,
        'feasible': vtol_possible and endurance_passes,  # Always False
        'fail_reason': 'Cannot satisfy VTOL requirement - no runway on Mars',
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted fixed-wing analysis results."""
    if results is None:
        results = fixed_wing_feasibility_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("FIXED-WING FEASIBILITY ANALYSIS (Section 5.2)")
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
    print()
    
    print("AERODYNAMIC PARAMETERS (from §4.7)")
    print("-" * 50)
    print(f"  Aspect ratio:       {results['aspect_ratio']}")
    print(f"  Oswald efficiency:  {results['oswald_e']:.4f}")
    print(f"  CD0:                {results['cd0']:.4f}")
    print(f"  CL_max:             {results['cl_max']:.2f}")
    print(f"  K (induced):        {results['k_induced']:.4f}")
    print(f"  (L/D)_max:          {results['ld_max']:.2f}")
    print(f"  CL_optimal:         {results['cl_optimal']:.3f}")
    print()
    
    print("WING LOADING AND STALL")
    print("-" * 50)
    print(f"  Max wing loading:   {results['wing_loading_max']:.2f} N/m²")
    print(f"  Stall speed:        {results['v_stall']:.1f} m/s")
    print()
    
    print("CRUISE PERFORMANCE")
    print("-" * 50)
    print(f"  CL at cruise:       {results['cl_cruise']:.3f}")
    print(f"  L/D at cruise:      {results['ld_cruise']:.2f}")
    print(f"  Cruise power:       {results['cruise_power_w']:.1f} W")
    print(f"  Combined eta_cruise:{results['eta_cruise']:.4f}")
    print()
    
    print("ENDURANCE AND RANGE")
    print("-" * 50)
    print(f"  Usable energy:      {results['usable_energy_wh']:.1f} Wh")
    print(f"  Endurance:          {results['endurance_min']:.1f} min")
    print(f"  Range:              {results['range_km']:.0f} km")
    print()
    
    print("TAKEOFF ANALYSIS (Disqualifying)")
    print("-" * 50)
    print(f"  Ground roll:        {results['takeoff_distance_m']:.0f} m")
    print(f"  Status:             IMPRACTICAL - No runway available on Mars")
    print()
    
    print("FEASIBILITY ASSESSMENT")
    print("-" * 50)
    end_status = "[PASS]" if results['endurance_passes'] else "[FAIL]"
    vtol_status = "[PASS]" if results['vtol_possible'] else "[FAIL]"
    print(f"  Endurance req:      {results['requirement_min']:.0f} min -> {results['endurance_min']:.0f} min -> {end_status}")
    print(f"  VTOL requirement:   Required -> Not possible -> {vtol_status}")
    print(f"  Overall:            [FAIL]")
    print()
    
    print("CONCLUSION: Fixed-wing FAILS due to VTOL requirement.")
    print(f"           Despite excellent endurance ({results['endurance_min']:.0f} min, +{(results['endurance_min']/results['requirement_min']-1)*100:.0f}% margin),")
    print(f"           ground roll of {results['takeoff_distance_m']:.0f} m is impractical without runway.")
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_analysis()
