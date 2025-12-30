"""
Matching Chart Analysis
========================

Implements constraint-based sizing methodology for the QuadPlane configuration.
Generates the P/W vs W/S matching chart from manuscript Section 5.5.

Reference: 
- Manuscript: sections_en/05_05_comparative-results.md
- Prompt: docs/prompt_04_python_implementation.txt

Updated 2025-12-28: CORRECTED parameters from verification:
- ρ = 0.0196 kg/m³ (was 0.0209)
- e = 0.869 for AR=6 (was 0.82)
- V_stall appropriately calculated from density
"""

import math
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

# Default parameters from baseline_parameters.yaml (updated from §4.12)
# Physical constants
G_MARS = 3.711          # m/s²
RHO_ARCADIA = 0.0196    # kg/m³ (CORRECTED from 0.0209)

# Propulsion efficiencies (from §4.5)
FM_DEFAULT = 0.40       # Figure of merit
ETA_PROP = 0.55         # Propeller efficiency
ETA_MOTOR = 0.85        # Motor efficiency
ETA_ESC = 0.95          # ESC efficiency

# Aerodynamic parameters (from §4.7)
AR_DEFAULT = 6          # Aspect ratio
OSWALD_E = 0.869        # Oswald efficiency factor (CORRECTED: Sadraey correlation for AR=6)
CD0_DEFAULT = 0.030     # Zero-lift drag coefficient
CL_MAX = 1.20           # Maximum lift coefficient

# Mission (from §4.12)
DISK_LOADING_DEFAULT = 30.0  # N/m²
V_CRUISE_DEFAULT = 40.0      # m/s
V_MIN_FACTOR = 1.2           # V_min = 1.2 × V_stall


def hover_constraint(disk_loading: float = DISK_LOADING_DEFAULT,
                     rho: float = RHO_ARCADIA,
                     figure_of_merit: float = FM_DEFAULT,
                     eta_motor: float = ETA_MOTOR,
                     eta_esc: float = ETA_ESC) -> float:
    """Calculate P/W required for hover (horizontal line on chart).
    
    Implements @eq:hover-constraint-qp from §5.5:
        (P/W)_hover = (1/η_hover) × sqrt(DL/(2ρ))
    
    This constraint is INDEPENDENT of W/S.
    
    Parameters
    ----------
    disk_loading : float
        Disk loading in N/m²
    rho : float
        Air density in kg/m³
    figure_of_merit : float
        Rotor figure of merit
    eta_motor : float
        Motor efficiency
    eta_esc : float
        ESC efficiency
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    eta_hover = figure_of_merit * eta_motor * eta_esc
    v_i = math.sqrt(disk_loading / (2 * rho))
    return v_i / eta_hover


def stall_constraint(rho: float = RHO_ARCADIA,
                     v_stall: float = 25.0,
                     c_l_max: float = CL_MAX) -> float:
    """Calculate maximum W/S from stall (vertical line on chart).
    
    Implements @eq:stall-constraint from §5.5 and §4.12:
        (W/S)_max = 0.5 × ρ × V_stall² × C_L,max
    
    The stall constraint determines the maximum allowable wing loading.
    Higher V_stall allows higher W/S, which means smaller wings.
    
    Parameters
    ----------
    rho : float
        Air density in kg/m³ (default 0.0196 CORRECTED)
    v_stall : float
        Stall speed in m/s (default 25 m/s)
    c_l_max : float
        Maximum lift coefficient
    
    Returns
    -------
    float
        Maximum wing loading W/S in N/m²
    
    Examples
    --------
    >>> round(stall_constraint(0.0196, 25.0, 1.20), 1)
    7.4
    >>> round(stall_constraint(0.0196, 29.2, 1.20), 1)
    10.0
    """
    # (W/S)_max = 0.5 × ρ × V_stall² × C_L,max
    ws_max = 0.5 * rho * v_stall**2 * c_l_max
    
    return ws_max


def cruise_constraint(wing_loading: float,
                      v_cruise: float = V_CRUISE_DEFAULT,
                      rho: float = RHO_ARCADIA,
                      ar: float = AR_DEFAULT,
                      e: float = OSWALD_E,
                      c_d0: float = CD0_DEFAULT,
                      eta_prop: float = ETA_PROP,
                      eta_motor: float = ETA_MOTOR,
                      eta_esc: float = ETA_ESC) -> float:
    """Calculate P/W required for cruise at given W/S.
    
    Implements @eq:cruise-constraint from §5.5:
        (P/W)_cruise = V / ((L/D)_cruise × η_cruise)
    
    Where (L/D)_cruise depends on C_L at cruise, which depends on W/S.
    
    Parameters
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    v_cruise : float
        Cruise velocity in m/s
    rho : float
        Air density in kg/m³
    ar : float
        Aspect ratio
    e : float
        Oswald efficiency factor
    c_d0 : float
        Zero-lift drag coefficient
    eta_prop : float
        Propeller efficiency
    eta_motor : float
        Motor efficiency
    eta_esc : float
        ESC efficiency
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    # Calculate C_L required for level flight
    c_l = (2 * wing_loading) / (rho * v_cruise**2)
    
    # Calculate C_D from drag polar
    k = 1 / (math.pi * ar * e)
    c_d = c_d0 + k * c_l**2
    
    # L/D at this condition
    if c_d > 0 and c_l > 0:
        ld = c_l / c_d
    else:
        ld = 1.0  # Prevent division by zero
    
    # P/W = V / (L/D × η_cruise)
    eta_cruise = eta_prop * eta_motor * eta_esc
    pw = v_cruise / (ld * eta_cruise)
    
    return pw


def cruise_constraint_curve(ws_range: np.ndarray,
                            v_cruise: float = V_CRUISE_DEFAULT,
                            rho: float = RHO_ARCADIA,
                            ar: float = AR_DEFAULT,
                            e: float = OSWALD_E,
                            c_d0: float = CD0_DEFAULT,
                            eta_prop: float = ETA_PROP,
                            eta_motor: float = ETA_MOTOR,
                            eta_esc: float = ETA_ESC) -> np.ndarray:
    """Calculate cruise constraint curve over range of W/S values.
    
    Parameters
    ----------
    ws_range : np.ndarray
        Array of wing loading values in N/m²
    v_cruise : float
        Cruise velocity in m/s
    (other parameters)
        Same as cruise_constraint
    
    Returns
    -------
    np.ndarray
        Array of power loading P/W values in W/N
    """
    return np.array([cruise_constraint(ws, v_cruise, rho, ar, e, c_d0, 
                                       eta_prop, eta_motor, eta_esc) 
                     for ws in ws_range])


def minimum_power_point(ar: float = AR_DEFAULT,
                        e: float = OSWALD_E,
                        c_d0: float = CD0_DEFAULT,
                        v_cruise: float = V_CRUISE_DEFAULT,
                        rho: float = RHO_ARCADIA) -> Tuple[float, float]:
    """Find the W/S and C_L that minimizes cruise power.
    
    Minimum cruise power occurs at (L/D)_max.
    Returns the corresponding W/S.
    
    Parameters
    ----------
    ar : float
        Aspect ratio
    e : float
        Oswald efficiency factor
    c_d0 : float
        Zero-lift drag coefficient
    v_cruise : float
        Cruise velocity
    rho : float
        Air density
    
    Returns
    -------
    tuple
        (wing_loading_optimal, ld_max)
    """
    # C_L for maximum L/D
    cl_opt = math.sqrt(math.pi * ar * e * c_d0)
    
    # Maximum L/D
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / c_d0)
    
    # Corresponding W/S
    ws_opt = cl_opt * rho * v_cruise**2 / 2
    
    return ws_opt, ld_max


def find_design_point(hover_pw: float,
                      stall_ws: float,
                      ws_range: np.ndarray,
                      cruise_pw_curve: np.ndarray) -> Tuple[float, float]:
    """Find the design point from constraint intersections.
    
    The design point selection depends on the active constraint:
    - If hover dominates (P/W_hover > P/W_cruise for all feasible W/S):
      Select W/S at stall limit to maximize L/D and minimize wing area
    - If cruise dominates:
      Select W/S at optimal L/D point
    
    The feasible region is: W/S ≤ stall_ws and P/W ≥ max(hover, cruise)
    
    Parameters
    ----------
    hover_pw : float
        Hover power loading (horizontal constraint)
    stall_ws : float
        Stall wing loading (vertical constraint)
    ws_range : np.ndarray
        Array of W/S values
    cruise_pw_curve : np.ndarray
        Cruise power loading at each W/S
    
    Returns
    -------
    tuple
        (design_ws, design_pw)
    """
    # First check if hover dominates at stall limit
    # Find cruise P/W at stall limit
    stall_idx = np.searchsorted(ws_range, stall_ws)
    if stall_idx >= len(cruise_pw_curve):
        stall_idx = len(cruise_pw_curve) - 1
    
    pw_cruise_at_stall = cruise_pw_curve[stall_idx] if stall_idx < len(cruise_pw_curve) else cruise_pw_curve[-1]
    
    # Determine which constraint is active
    if hover_pw >= pw_cruise_at_stall:
        # Hover dominates: select W/S at stall limit
        # This maximizes L/D for cruise while meeting stall constraint
        design_ws = min(stall_ws, ws_range[-1])  # Ensure within range
        design_pw = hover_pw  # Hover sets the required P/W
    else:
        # Cruise dominates at stall limit: need to check where curves intersect
        # Find intersection of hover and cruise curves
        for i, ws in enumerate(ws_range):
            if ws > stall_ws:
                break  # Exceeds stall constraint
            if cruise_pw_curve[i] >= hover_pw:
                # Cruise curve crosses hover at this W/S
                design_ws = ws
                design_pw = cruise_pw_curve[i]
                break
        else:
            # No intersection found, use stall limit
            design_ws = stall_ws
            design_pw = max(hover_pw, pw_cruise_at_stall)
    
    return design_ws, design_pw


def matching_chart_analysis(mtow_kg: float = 10.0,
                            disk_loading: float = DISK_LOADING_DEFAULT,
                            v_cruise: float = V_CRUISE_DEFAULT,
                            v_stall: float = 25.0,
                            rho: float = RHO_ARCADIA,
                            figure_of_merit: float = FM_DEFAULT,
                            eta_prop: float = ETA_PROP,
                            eta_motor: float = ETA_MOTOR,
                            eta_esc: float = ETA_ESC,
                            ar: float = AR_DEFAULT,
                            e: float = OSWALD_E,
                            c_d0: float = CD0_DEFAULT,
                            c_l_max: float = CL_MAX) -> Dict[str, Any]:
    """Complete matching chart analysis.
    
    Returns all constraint values and design point.
    
    The stall constraint determines maximum allowable W/S:
        (W/S)_max = 0.5 × ρ × V_stall² × C_L,max
    
    For CORRECTED ρ = 0.0196 kg/m³:
    - V_stall = 25 m/s → W/S_max = 7.4 N/m²
    - V_stall = 29.2 m/s → W/S_max = 10 N/m² (from manuscript)
    
    Parameters
    ----------
    mtow_kg : float
        MTOW in kg (for absolute power calculation)
    disk_loading : float
        Disk loading for hover constraint
    v_cruise : float
        Cruise velocity
    v_stall : float
        Stall speed in m/s (default 25 m/s for V_cruise/V_stall ≈ 1.6)
    (other parameters)
        Propulsion and aerodynamic parameters
    
    Returns
    -------
    dict
        Complete matching chart data
    """
    # Calculate constraints
    pw_hover = hover_constraint(disk_loading, rho, figure_of_merit, eta_motor, eta_esc)
    ws_stall = stall_constraint(rho, v_stall, c_l_max)
    
    # Minimum velocity with 1.2 safety factor
    v_min = 1.2 * v_stall
    
    # Generate W/S range for curve plotting
    ws_min = 2.0
    ws_max = 30.0
    ws_range = np.linspace(ws_min, ws_max, 100)
    
    # Calculate cruise curve
    pw_cruise_curve = cruise_constraint_curve(
        ws_range, v_cruise, rho, ar, e, c_d0, eta_prop, eta_motor, eta_esc
    )
    
    # Find minimum power point for cruise
    ws_opt, ld_max = minimum_power_point(ar, e, c_d0, v_cruise, rho)
    pw_at_optimal = cruise_constraint(ws_opt, v_cruise, rho, ar, e, c_d0,
                                      eta_prop, eta_motor, eta_esc)
    
    # Find design point
    design_ws, design_pw = find_design_point(
        pw_hover, ws_stall, ws_range, pw_cruise_curve
    )
    
    # Check which constraint is active at design point
    pw_cruise_at_design = cruise_constraint(design_ws, v_cruise, rho, ar, e, c_d0,
                                            eta_prop, eta_motor, eta_esc)
    
    if pw_hover > pw_cruise_at_design:
        active_constraint = 'hover'
    else:
        active_constraint = 'cruise'
    
    # Calculate corresponding values at design point
    weight_n = mtow_kg * G_MARS
    wing_area = weight_n / design_ws
    installed_power = design_pw * weight_n
    
    # Power comparison
    hover_total_power = pw_hover * weight_n
    cruise_total_power = pw_cruise_at_design * weight_n
    
    return {
        # Constraints
        'pw_hover': pw_hover,
        'ws_stall': ws_stall,
        'ws_optimal': ws_opt,
        'ld_max': ld_max,
        'pw_at_optimal': pw_at_optimal,
        
        # Design point
        'design_ws': design_ws,
        'design_pw': design_pw,
        'active_constraint': active_constraint,
        
        # Curves for plotting
        'ws_range': ws_range,
        'pw_cruise_curve': pw_cruise_curve,
        
        # Absolute values
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'wing_area_m2': wing_area,
        'wingspan_m': math.sqrt(ar * wing_area),
        'mean_chord_m': math.sqrt(wing_area / ar),
        'installed_power_w': installed_power,
        'hover_power_w': hover_total_power,
        'cruise_power_w': cruise_total_power,
        
        # Efficiencies
        'eta_hover': figure_of_merit * eta_motor * eta_esc,
        'eta_cruise': eta_prop * eta_motor * eta_esc,
        
        # Parameters used
        'disk_loading': disk_loading,
        'v_cruise': v_cruise,
        'v_min': v_min,
        'ar': ar,
        'e': e,
        'c_d0': c_d0,
        'c_l_max': c_l_max,
        'rho': rho,
    }


def print_matching_chart_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted matching chart analysis results."""
    if results is None:
        results = matching_chart_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("MATCHING CHART ANALYSIS (QuadPlane)")
    print("Constraint-based sizing from Manuscript Section 5.5")
    print(f"Values computed: {timestamp}")
    print("=" * 80)
    print()
    
    print("INPUT PARAMETERS")
    print("-" * 40)
    print(f"MTOW:               {results['mtow_kg']:.1f} kg")
    print(f"Weight:             {results['weight_n']:.2f} N")
    print(f"Air density:        {results['rho']} kg/m³")
    print(f"Cruise velocity:    {results['v_cruise']:.0f} m/s")
    print(f"Min velocity:       {results['v_min']:.0f} m/s")
    print(f"Disk loading:       {results['disk_loading']:.0f} N/m²")
    print(f"Aspect ratio:       {results['ar']}")
    print()
    
    print("AERODYNAMIC PARAMETERS")
    print("-" * 40)
    print(f"Oswald e:           {results['e']:.2f}")
    print(f"C_D0:               {results['c_d0']:.3f}")
    print(f"C_L,max:            {results['c_l_max']:.2f}")
    print(f"(L/D)_max:          {results['ld_max']:.1f}")
    print()
    
    print("CONSTRAINT ANALYSIS")
    print("-" * 40)
    print(f"Hover constraint:   P/W = {results['pw_hover']:.1f} W/N (horizontal line)")
    print(f"Stall constraint:   W/S = {results['ws_stall']:.1f} N/m² (vertical line)")
    print(f"Optimal cruise W/S: {results['ws_optimal']:.1f} N/m² (minimum cruise power)")
    print(f"Cruise P/W at opt:  {results['pw_at_optimal']:.1f} W/N")
    print()
    
    print("DESIGN POINT")
    print("-" * 40)
    print(f"Design W/S:         {results['design_ws']:.1f} N/m²")
    print(f"Design P/W:         {results['design_pw']:.1f} W/N")
    print(f"Active constraint:  {results['active_constraint'].upper()}")
    print()
    
    print("DERIVED GEOMETRY")
    print("-" * 40)
    print(f"Wing area:          {results['wing_area_m2']:.2f} m²")
    print(f"Wingspan:           {results['wingspan_m']:.2f} m")
    print(f"Mean chord:         {results['mean_chord_m']:.2f} m")
    print()
    
    print("POWER REQUIREMENTS")
    print("-" * 40)
    print(f"Installed power:    {results['installed_power_w']:.0f} W")
    print(f"Hover power:        {results['hover_power_w']:.0f} W")
    print(f"Cruise power:       {results['cruise_power_w']:.0f} W")
    print(f"Power ratio:        {results['hover_power_w']/results['cruise_power_w']:.1f}× (hover/cruise)")
    print()
    
    print("MATCHING CHART INTERPRETATION")
    print("-" * 40)
    if results['active_constraint'] == 'hover':
        print("Hover power requirement DOMINATES sizing.")
        print("The aircraft is sized by lift rotor capability, not cruise efficiency.")
        print("Wing loading is set by stall constraint for maximum efficiency within")
        print("the feasible region.")
    else:
        print("Cruise power requirement DOMINATES sizing.")
        print("The aircraft is sized by cruise efficiency requirements.")
    print()
    
    print("=" * 80)
    print()
    print(">>> These COMPUTED values will be used to UPDATE the manuscript in Phase C.")


if __name__ == "__main__":
    # Run matching chart analysis
    results = matching_chart_analysis()
    print_matching_chart_analysis(results)
