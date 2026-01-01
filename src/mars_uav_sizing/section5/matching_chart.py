"""
Matching Chart Analysis
========================

Implements the constraint-based sizing (matching chart) methodology from
manuscript Section 5.4. Generates P/W vs W/S constraint diagram.

The matching chart visualizes all performance constraints simultaneously,
identifying the feasible design space as the intersection of all acceptable
regions.

Equations implemented:
    @eq:hover-constraint-qp  - Hover constraint (horizontal line)
    @eq:stall-constraint     - Stall constraint (vertical line)
    @eq:cruise-constraint    - Cruise constraint (curve)
    
Reference:
    - Manuscript: sections_en/05_04_matching-chart-methodology-sec-comparative-results.md
    - Roskam (2005), Airplane Design Part I, Chapter 3

Last Updated: 2025-12-29
"""

import math
from typing import Dict, Any, Tuple, List
from datetime import datetime
import numpy as np

# Import configuration loader
from ..config import (
    get_mars_gravity,
    get_density,
    get_mtow,
    get_propulsion_efficiencies,
    get_aerodynamic_params,
    get_mission_params,
    get_param,
)

# Import from sibling modules
from .rotorcraft import hover_power_loading, induced_velocity_from_disk_loading
from .fixed_wing import (
    cruise_lift_coefficient, 
    lift_to_drag, 
    cruise_power_loading, 
    stall_wing_loading_limit,
    maximum_ld,
)


# =============================================================================
# CONSTRAINT FUNCTIONS
# =============================================================================

def hover_constraint() -> float:
    """
    Calculate P/W required for hover (horizontal line on chart).
    
    Implements @eq:hover-constraint-qp from §5.4:
        (P/W)_hover = (1/η_hover) × sqrt(DL/(2ρ))
    
    This constraint is INDEPENDENT of W/S.
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    return hover_power_loading()


def stall_constraint() -> float:
    """
    Calculate maximum W/S from stall (vertical line on chart).

    Implements @eq:stall-constraint from §5.4:
        (W/S)_max = 0.5 × ρ × V_min² × C_L,max

    Where V_min = 1.2 × V_stall (safety margin from §4.12).

    Returns
    -------
    float
        Maximum wing loading in N/m²
    """
    rho = get_density()
    v_stall = get_mission_params()['v_stall']
    v_min_factor = get_param('mission.velocity.v_min_factor')
    v_min = v_stall * v_min_factor
    cl_max = get_aerodynamic_params()['cl_max']

    return stall_wing_loading_limit(rho, v_min, cl_max)


def cruise_constraint(wing_loading: float) -> float:
    """
    Calculate P/W required for cruise at given W/S.
    
    Implements @eq:cruise-constraint from §5.4:
        (P/W)_cruise = V / ((L/D)_cruise × η_cruise)
    
    Where (L/D)_cruise depends on C_L at cruise, which depends on W/S.
    
    Parameters
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    rho = get_density()
    v_cruise = get_mission_params()['v_cruise']
    
    # C_L at this wing loading and velocity
    cl = cruise_lift_coefficient(wing_loading, rho, v_cruise)
    
    # L/D at this C_L (with QuadPlane penalty)
    ld_penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    ld_pure = lift_to_drag(cl)
    ld = ld_pure * ld_penalty
    
    return cruise_power_loading(v_cruise, ld)


def cruise_constraint_curve(ws_range: np.ndarray) -> np.ndarray:
    """
    Calculate cruise constraint curve over range of W/S values.
    
    Parameters
    ----------
    ws_range : np.ndarray
        Array of wing loading values in N/m²
    
    Returns
    -------
    np.ndarray
        Array of corresponding P/W values
    """
    return np.array([cruise_constraint(ws) for ws in ws_range])


# =============================================================================
# DESIGN POINT DETERMINATION
# =============================================================================

def find_design_point() -> Dict[str, float]:
    """
    Find the design point from constraint intersections.
    
    For QuadPlane:
    - Hover constraint dominates (horizontal line sets minimum P/W)
    - Stall constraint sets maximum W/S
    - Cruise constraint is easily satisfied (below hover)
    
    Returns
    -------
    dict
        Design point parameters
    """
    # Get constraint values
    pw_hover = hover_constraint()
    ws_stall = stall_constraint()
    
    # Cruise at stall-limited W/S
    pw_cruise_at_stall = cruise_constraint(ws_stall)
    
    # Design point is at maximum feasible W/S (smallest wing)
    # with P/W set by dominant constraint (hover)
    ws_design = ws_stall
    pw_design = max(pw_hover, pw_cruise_at_stall)
    
    # Determine which constraint is active
    if pw_hover > pw_cruise_at_stall:
        active_constraint = 'hover'
    else:
        active_constraint = 'cruise'
    
    return {
        'wing_loading': ws_design,
        'power_loading': pw_design,
        'hover_pw': pw_hover,
        'cruise_pw_at_stall': pw_cruise_at_stall,
        'stall_ws': ws_stall,
        'active_constraint': active_constraint,
    }


def derive_geometry(design_point: Dict[str, float] = None) -> Dict[str, float]:
    """
    Derive aircraft geometry from design point.
    
    Parameters
    ----------
    design_point : dict, optional
        Design point from find_design_point() (default: compute)
    
    Returns
    -------
    dict
        Derived geometric parameters
    """
    if design_point is None:
        design_point = find_design_point()
    
    g_mars = get_mars_gravity()
    mtow_kg = get_mtow()
    ar = get_aerodynamic_params()['aspect_ratio']
    
    weight_n = mtow_kg * g_mars
    ws = design_point['wing_loading']
    pw = design_point['power_loading']
    
    # Wing geometry
    wing_area = weight_n / ws
    wingspan = math.sqrt(ar * wing_area)
    chord = wing_area / wingspan
    
    # Power requirement
    installed_power = pw * weight_n
    
    # Disk area (from disk loading)
    disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    disk_area = weight_n / disk_loading
    
    return {
        'wing_area_m2': wing_area,
        'wingspan_m': wingspan,
        'chord_m': chord,
        'installed_power_w': installed_power,
        'disk_area_m2': disk_area,
    }


# =============================================================================
# COMPLETE ANALYSIS
# =============================================================================

def matching_chart_analysis() -> Dict[str, Any]:
    """
    Complete matching chart analysis.
    
    Returns all constraint values, design point, and derived geometry.
    
    Returns
    -------
    dict
        Complete matching chart analysis
    """
    # Load parameters
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    prop = get_propulsion_efficiencies()
    aero = get_aerodynamic_params()
    mission = get_mission_params()
    disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    
    weight_n = mtow_kg * g_mars
    
    # Constraint values
    pw_hover = hover_constraint()
    ws_stall = stall_constraint()
    
    # Design point
    design_point = find_design_point()
    
    # Geometry
    geometry = derive_geometry(design_point)
    
    # L/D values
    ld_max, cl_opt = maximum_ld()
    ld_penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    ld_quadplane = ld_max * ld_penalty
    
    # Induced velocity
    v_i = induced_velocity_from_disk_loading(disk_loading, rho)
    
    # Combined efficiencies
    eta_hover = prop['figure_of_merit'] * prop['eta_motor'] * prop['eta_esc']
    eta_cruise = prop['eta_prop'] * prop['eta_motor'] * prop['eta_esc']
    
    # Curve data for plotting
    ws_range = np.linspace(2.0, 15.0, 50)
    pw_cruise_curve = cruise_constraint_curve(ws_range)
    pw_hover_line = np.full_like(ws_range, pw_hover)
    
    return {
        # Input parameters
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'rho_kg_m3': rho,
        'v_cruise_m_s': mission['v_cruise'],
        'disk_loading_n_m2': disk_loading,
        
        # Efficiencies
        'figure_of_merit': prop['figure_of_merit'],
        'eta_hover': eta_hover,
        'eta_cruise': eta_cruise,
        
        # Aerodynamics
        'ld_max': ld_max,
        'ld_quadplane': ld_quadplane,
        'cl_max': aero['cl_max'],
        
        # Constraint values
        'hover_pw': pw_hover,
        'stall_ws': ws_stall,
        'induced_velocity_m_s': v_i,
        
        # Design point
        'design_point': design_point,
        'geometry': geometry,
        
        # Curve data (for plotting)
        'ws_range': ws_range,
        'pw_cruise_curve': pw_cruise_curve,
        'pw_hover_line': pw_hover_line,
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted matching chart analysis results."""
    if results is None:
        results = matching_chart_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dp = results['design_point']
    geom = results['geometry']
    
    print("=" * 80)
    print("MATCHING CHART ANALYSIS (Section 5.4)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()
    
    print("INPUT PARAMETERS")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m³")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print(f"  Disk loading:       {results['disk_loading_n_m2']:.1f} N/m²")
    print()
    
    print("CONSTRAINT VALUES")
    print("-" * 50)
    print(f"  Hover P/W:          {results['hover_pw']:.2f} W/N (horizontal line)")
    print(f"  Stall W/S limit:    {results['stall_ws']:.2f} N/m² (vertical line)")
    print()
    
    print("DESIGN POINT (intersection of constraints)")
    print("-" * 50)
    print(f"  Wing loading:       {dp['wing_loading']:.2f} N/m²")
    print(f"  Power loading:      {dp['power_loading']:.2f} W/N")
    print(f"  Active constraint:  {dp['active_constraint'].upper()}")
    print()
    
    print("DERIVED GEOMETRY")
    print("-" * 50)
    print(f"  Wing area:          {geom['wing_area_m2']:.3f} m²")
    print(f"  Wingspan:           {geom['wingspan_m']:.2f} m")
    print(f"  Mean chord:         {geom['chord_m']:.3f} m")
    print(f"  Installed power:    {geom['installed_power_w']:.0f} W (hover)")
    print(f"  Disk area:          {geom['disk_area_m2']:.3f} m²")
    print()
    
    print("SUMMARY")
    print("-" * 50)
    print("  The matching chart shows that:")
    print(f"  1. Hover constraint dominates at P/W = {results['hover_pw']:.1f} W/N")
    print(f"  2. Stall constraint limits W/S to {results['stall_ws']:.1f} N/m²")
    print(f"  3. Cruise power ({dp['cruise_pw_at_stall']:.1f} W/N) is ~{results['hover_pw']/dp['cruise_pw_at_stall']:.0f}× lower than hover")
    print("  -> Design is HOVER-DOMINATED; cruise power is abundant")
    print()
    
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_analysis()
