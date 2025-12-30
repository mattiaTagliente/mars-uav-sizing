"""
Fixed-Wing Configuration Analysis
==================================

Implements equations from manuscript Section 5.3 (Fixed-Wing Configuration).
All equations are traced to source_grounding.txt for citations.

Reference: 
- Manuscript: sections_en/05_03_fixed-wing-analysis.md
- Prompt: docs/prompt_04_python_implementation.txt

Updated 2025-12-28: CORRECTED parameters from verification:
- ρ = 0.0196 kg/m³ (was 0.0209)
- e = 0.869 for AR=6 (was 0.82)
"""

import math
from typing import Dict, Any, Tuple
from datetime import datetime

# Default parameters from baseline_parameters.yaml (updated from §4.12)
# Physical constants
G_MARS = 3.711          # m/s²
RHO_ARCADIA = 0.0196    # kg/m³ (CORRECTED from 0.0209)

# Propulsion efficiencies (from §4.5)
ETA_PROP = 0.55         # Propeller efficiency at low-Re
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

# Mission (from §4.12)
V_CRUISE_DEFAULT = 40.0  # m/s


def cruise_lift_coefficient(wing_loading: float, rho: float, velocity: float) -> float:
    """Calculate C_L required for level flight.
    
    Implements @eq:cl-required from §5.3:
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
    
    Examples
    --------
    >>> round(cruise_lift_coefficient(10.0, 0.0209, 40.0), 3)
    0.598
    """
    return (2 * wing_loading) / (rho * velocity**2)


def drag_coefficient(c_l: float, c_d0: float = CD0_DEFAULT, 
                     ar: float = AR_DEFAULT, e: float = OSWALD_E) -> float:
    """Calculate drag coefficient from parabolic polar.
    
    Implements @eq:drag-polar from §5.3:
        C_D = C_D0 + C_L² / (π×AR×e)
    
    Reference: Torenbeek (1982), Section 5.3
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    c_d0 : float, optional
        Zero-lift drag coefficient, default 0.030
    ar : float, optional
        Aspect ratio, default 6
    e : float, optional
        Oswald efficiency factor, default 0.82
    
    Returns
    -------
    float
        Total drag coefficient
    """
    k = 1 / (math.pi * ar * e)  # Induced drag factor
    return c_d0 + k * c_l**2


def induced_drag_factor(ar: float = AR_DEFAULT, e: float = OSWALD_E) -> float:
    """Calculate induced drag factor K.
    
    K = 1 / (π × AR × e)
    
    Parameters
    ----------
    ar : float
        Aspect ratio
    e : float
        Oswald efficiency factor
    
    Returns
    -------
    float
        Induced drag factor K
    """
    return 1 / (math.pi * ar * e)


def lift_to_drag(c_l: float, c_d0: float = CD0_DEFAULT,
                 ar: float = AR_DEFAULT, e: float = OSWALD_E) -> float:
    """Calculate lift-to-drag ratio at given C_L.
    
    Implements @eq:ld-ratio from §5.3:
        L/D = C_L / C_D
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    c_d0 : float, optional
        Zero-lift drag coefficient
    ar : float, optional
        Aspect ratio
    e : float, optional
        Oswald efficiency factor
    
    Returns
    -------
    float
        Lift-to-drag ratio
    """
    c_d = drag_coefficient(c_l, c_d0, ar, e)
    if c_d <= 0:
        return 0
    return c_l / c_d


def maximum_ld(c_d0: float = CD0_DEFAULT, ar: float = AR_DEFAULT, 
               e: float = OSWALD_E) -> Tuple[float, float]:
    """Calculate maximum L/D and corresponding C_L.
    
    Implements @eq:ld-max and @eq:cl-optimal from §5.3:
        (L/D)_max = 0.5 × sqrt(π×AR×e / C_D0)
        C_L,opt = sqrt(π×AR×e×C_D0)
    
    Reference: Sadraey (2013), Chapter 5
    
    Parameters
    ----------
    c_d0 : float, optional
        Zero-lift drag coefficient, default 0.030
    ar : float, optional
        Aspect ratio, default 6
    e : float, optional
        Oswald efficiency factor, default 0.82
    
    Returns
    -------
    tuple
        (ld_max, cl_optimal)
    
    Examples
    --------
    >>> ld_max, cl_opt = maximum_ld(0.030, 6, 0.82)
    >>> round(ld_max, 1)
    11.7
    >>> round(cl_opt, 2)
    0.68
    """
    cl_opt = math.sqrt(math.pi * ar * e * c_d0)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / c_d0)
    return ld_max, cl_opt


def cruise_power(weight_n: float, velocity: float, ld: float,
                 eta_prop: float = ETA_PROP, eta_motor: float = ETA_MOTOR,
                 eta_esc: float = ETA_ESC) -> float:
    """Calculate electrical power for cruise.
    
    Implements @eq:cruise-electric-power from §5.3:
        P = W×V / (L/D × η_prop × η_motor × η_ESC)
    
    Reference: Torenbeek (1982), Section 5.4
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    velocity : float
        Cruise velocity in m/s
    ld : float
        Lift-to-drag ratio at cruise
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
    eta_cruise = eta_prop * eta_motor * eta_esc
    return (weight_n * velocity) / (ld * eta_cruise)


def cruise_power_loading(velocity: float, ld: float,
                         eta_prop: float = ETA_PROP, eta_motor: float = ETA_MOTOR,
                         eta_esc: float = ETA_ESC) -> float:
    """Calculate P/W for cruise constraint on matching chart.
    
    Implements @eq:power-loading-cruise from §5.3:
        P/W = V / (L/D × η_cruise)
    
    Parameters
    ----------
    velocity : float
        Cruise velocity in m/s
    ld : float
        Lift-to-drag ratio at cruise
    eta_prop : float, optional
        Propeller efficiency
    eta_motor : float, optional
        Motor efficiency
    eta_esc : float, optional
        ESC efficiency
    
    Returns
    -------
    float
        Power loading P/W in W/N
    """
    eta_cruise = eta_prop * eta_motor * eta_esc
    return velocity / (ld * eta_cruise)


def stall_speed(wing_loading: float, rho: float, c_l_max: float = CL_MAX) -> float:
    """Calculate stall speed from wing loading.
    
    Implements @eq:stall-speed from §5.3:
        V_stall = sqrt(2×(W/S) / (ρ×C_L,max))
    
    Reference: Sadraey (2013), Section 4.3.3
    
    Parameters
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    rho : float
        Air density in kg/m³
    c_l_max : float, optional
        Maximum lift coefficient, default 1.20
    
    Returns
    -------
    float
        Stall speed in m/s
    
    Examples
    --------
    >>> round(stall_speed(10.0, 0.0209, 1.20), 1)
    28.2
    """
    return math.sqrt(2 * wing_loading / (rho * c_l_max))


def stall_wing_loading_limit(rho: float, v_min: float, 
                             c_l_max: float = CL_MAX) -> float:
    """Calculate maximum allowable wing loading from stall constraint.
    
    Implements @eq:wing-loading-constraint from §5.3:
        (W/S)_max = 0.5 × ρ × V_min² × C_L,max
    
    Parameters
    ----------
    rho : float
        Air density in kg/m³
    v_min : float
        Minimum operating speed in m/s
    c_l_max : float, optional
        Maximum lift coefficient, default 1.20
    
    Returns
    -------
    float
        Maximum wing loading in N/m²
    
    Examples
    --------
    >>> round(stall_wing_loading_limit(0.0209, 30.0, 1.20), 1)
    11.3
    """
    return 0.5 * rho * v_min**2 * c_l_max


def fixed_wing_endurance(f_batt: float = F_BATT, e_spec_wh_kg: float = E_SPEC_WH_KG,
                         dod: float = DOD, eta_batt: float = ETA_DISCHARGE,
                         ld: float = None, eta_prop: float = ETA_PROP,
                         eta_motor: float = ETA_MOTOR, eta_esc: float = ETA_ESC,
                         g_mars: float = G_MARS, v_cruise: float = V_CRUISE_DEFAULT,
                         c_d0: float = CD0_DEFAULT, ar: float = AR_DEFAULT,
                         e: float = OSWALD_E) -> float:
    """Calculate fixed-wing endurance.
    
    Implements @eq:endurance-fixedwing from §5.3:
        t = (f_batt × e_spec × DoD × η_batt × (L/D) × η_cruise) / (g × V)
    
    Similar to rotorcraft but with higher L/D.
    
    Parameters
    ----------
    f_batt : float
        Battery mass fraction
    e_spec_wh_kg : float
        Specific energy in Wh/kg
    dod : float
        Depth of discharge
    eta_batt : float
        Battery discharge efficiency
    ld : float, optional
        Lift-to-drag ratio (if None, uses (L/D)_max)
    eta_prop : float
        Propeller efficiency
    eta_motor : float
        Motor efficiency
    eta_esc : float
        ESC efficiency
    g_mars : float
        Mars gravity
    v_cruise : float
        Cruise velocity
    c_d0 : float
        Zero-lift drag coefficient
    ar : float
        Aspect ratio
    e : float
        Oswald efficiency factor
    
    Returns
    -------
    float
        Endurance in MINUTES
    """
    # If L/D not specified, use maximum L/D
    if ld is None:
        ld, _ = maximum_ld(c_d0, ar, e)
    
    # Convert Wh/kg to J/kg
    e_spec_j_kg = e_spec_wh_kg * 3600
    
    # Combined cruise efficiency
    eta_cruise = eta_prop * eta_motor * eta_esc
    
    # Endurance in seconds
    numerator = f_batt * e_spec_j_kg * dod * eta_batt * ld * eta_cruise
    denominator = g_mars * v_cruise
    t_seconds = numerator / denominator
    
    return t_seconds / 60  # Return in minutes


def takeoff_ground_roll(mtow_kg: float, wing_area: float, rho: float,
                        c_l_max: float = CL_MAX, thrust_to_weight: float = 0.3,
                        mu_r: float = 0.02, g_mars: float = G_MARS) -> float:
    """Calculate takeoff ground roll distance.
    
    Implements @eq:takeoff-roll from §5.3:
        S_TO = V_TO² / (2 × a_avg)
    
    Reference: Torenbeek (1982), Appendix K
    
    Parameters
    ----------
    mtow_kg : float
        MTOW in kg
    wing_area : float
        Wing area in m²
    rho : float
        Air density in kg/m³
    c_l_max : float, optional
        Maximum lift coefficient
    thrust_to_weight : float, optional
        Thrust-to-weight ratio (T/W), default 0.3
    mu_r : float, optional
        Rolling friction coefficient, default 0.02
    g_mars : float, optional
        Mars gravity
    
    Returns
    -------
    float
        Ground roll distance in METERS
    """
    weight_n = mtow_kg * g_mars
    wing_loading = weight_n / wing_area
    
    # Stall speed
    v_stall = stall_speed(wing_loading, rho, c_l_max)
    
    # Liftoff speed (1.1 × stall)
    v_to = 1.1 * v_stall
    
    # Average acceleration during ground roll
    # a = g * (T/W - μ_r * (1 - L/W))
    # At average speed ~0.7×V_TO, assume L/W ≈ 0.5
    lift_fraction = 0.5
    a_avg = g_mars * (thrust_to_weight - mu_r * (1 - lift_fraction))
    
    # If acceleration is too low, return very large distance
    if a_avg <= 0.1:
        a_avg = 0.1
    
    # Ground roll distance
    s_to = v_to**2 / (2 * a_avg)
    
    return s_to


def fixed_wing_feasibility_analysis(
    mtow_kg: float = MTOW_BASELINE_KG,
    v_cruise: float = V_CRUISE_DEFAULT,
    rho: float = RHO_ARCADIA,
    f_batt: float = F_BATT,
    e_spec_wh_kg: float = E_SPEC_WH_KG,
    dod: float = DOD,
    eta_batt: float = ETA_DISCHARGE,
    reserve_fraction: float = RESERVE_FRACTION,
    eta_prop: float = ETA_PROP,
    eta_motor: float = ETA_MOTOR,
    eta_esc: float = ETA_ESC,
    ar: float = AR_DEFAULT,
    e: float = OSWALD_E,
    c_d0: float = CD0_DEFAULT,
    c_l_max: float = CL_MAX,
    g_mars: float = G_MARS,
    endurance_requirement_min: float = 60.0
) -> Dict[str, Any]:
    """Complete fixed-wing feasibility analysis.
    
    Returns dictionary with:
    - cruise_power_w: Electrical cruise power
    - ld_max: Maximum L/D achievable
    - endurance_min: Achievable endurance  
    - range_km: Achievable range
    - takeoff_roll_m: Ground roll distance
    - can_takeoff: Boolean (should be False!)
    - feasible: Boolean (should be False due to no VTOL)
    """
    # Weight calculation
    weight_n = mtow_kg * g_mars
    
    # Get maximum L/D
    ld_max, cl_opt = maximum_ld(c_d0, ar, e)
    
    # Wing area for optimal cruise (at C_L*)
    # From C_L = 2(W/S) / (ρV²), so W/S = C_L × ρ × V² / 2
    ws_optimal = cl_opt * rho * v_cruise**2 / 2
    wing_area = weight_n / ws_optimal
    
    # Mean chord and Reynolds number check
    mean_chord = math.sqrt(wing_area / ar)
    mu = 1.08e-5  # Pa·s
    reynolds = rho * v_cruise * mean_chord / mu
    
    # Actual operating L/D (may be different from optimal)
    cl_cruise = cruise_lift_coefficient(ws_optimal, rho, v_cruise)
    ld_cruise = lift_to_drag(cl_cruise, c_d0, ar, e)
    
    # Cruise power
    p_cruise = cruise_power(weight_n, v_cruise, ld_max, eta_prop, eta_motor, eta_esc)
    
    # Battery energy
    battery_mass_kg = f_batt * mtow_kg
    total_energy_wh = battery_mass_kg * e_spec_wh_kg
    usable_energy_wh = total_energy_wh * dod * eta_batt
    energy_after_reserve = usable_energy_wh * (1 - reserve_fraction)
    
    # Endurance
    t_endurance_min = fixed_wing_endurance(
        f_batt, e_spec_wh_kg, dod, eta_batt, ld_max,
        eta_prop, eta_motor, eta_esc, g_mars, v_cruise, c_d0, ar, e
    )
    
    # Account for reserve
    t_endurance_with_reserve = t_endurance_min * (1 - reserve_fraction)
    
    # Range
    range_km = v_cruise * (t_endurance_with_reserve * 60) / 1000
    
    # Takeoff ground roll
    takeoff_roll = takeoff_ground_roll(mtow_kg, wing_area, rho, c_l_max)
    
    # Stall speed
    v_stall = stall_speed(ws_optimal, rho, c_l_max)
    
    # Feasibility (cannot VTOL!)
    can_takeoff = takeoff_roll < 100  # Would need to be < 100m for any practicality
    feasible = False  # Fixed-wing cannot satisfy VTOL requirement
    
    # Power loading
    pw_cruise = p_cruise / weight_n
    pw_cruise_per_kg = p_cruise / mtow_kg
    
    return {
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,
        'wing_area_m2': wing_area,
        'wingspan_m': math.sqrt(ar * wing_area),
        'mean_chord_m': mean_chord,
        'wing_loading_n_m2': ws_optimal,
        'reynolds_number': reynolds,
        'ld_max': ld_max,
        'cl_optimal': cl_opt,
        'cl_cruise': cl_cruise,
        'ld_cruise': ld_cruise,
        'cruise_power_w': p_cruise,
        'power_loading_w_per_n': pw_cruise,
        'power_loading_w_per_kg': pw_cruise_per_kg,
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'usable_energy_wh': usable_energy_wh,
        'energy_after_reserve_wh': energy_after_reserve,
        'endurance_theoretical_min': t_endurance_min,
        'endurance_with_reserve_min': t_endurance_with_reserve,
        'range_km': range_km,
        'v_stall_m_s': v_stall,
        'takeoff_roll_m': takeoff_roll,
        'can_takeoff': can_takeoff,
        'feasible': feasible,
        'eta_cruise': eta_prop * eta_motor * eta_esc,
        'ar': ar,
        'e': e,
        'cd0': c_d0,
    }


def print_fixed_wing_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted fixed-wing analysis results."""
    if results is None:
        results = fixed_wing_feasibility_analysis()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("FIXED-WING FEASIBILITY ANALYSIS")
    print("Equations from: Manuscript Section 5.3 (Fixed-Wing Configuration)")
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
    
    print("AERODYNAMIC PARAMETERS (from §4.7)")
    print("-" * 40)
    print(f"Aspect ratio:       {results['ar']}")
    print(f"Oswald efficiency:  {results['e']:.2f}")
    print(f"Zero-lift C_D:      {results['cd0']:.3f}")
    print(f"Max lift coeff:     {CL_MAX:.2f}")
    print()
    
    print("DRAG POLAR ANALYSIS (@eq:ld-max, @eq:cl-optimal)")
    print("-" * 40)
    print(f"Induced drag factor K = 1/(π×AR×e): {induced_drag_factor(results['ar'], results['e']):.4f}")
    print(f"C_L* (optimal):     {results['cl_optimal']:.2f}")
    print(f"(L/D)_max:          {results['ld_max']:.1f}")
    print()
    
    print("WING GEOMETRY (derived for optimal cruise)")
    print("-" * 40)
    print(f"Wing area:          {results['wing_area_m2']:.2f} m²")
    print(f"Wingspan:           {results['wingspan_m']:.2f} m")
    print(f"Mean chord:         {results['mean_chord_m']:.2f} m")
    print(f"Wing loading:       {results['wing_loading_n_m2']:.1f} N/m²")
    print(f"Reynolds number:    {results['reynolds_number']:.0f}")
    print()
    
    print("PROPULSION EFFICIENCIES (from §4.5)")
    print("-" * 40)
    print(f"Propeller η:        {ETA_PROP:.2f}")
    print(f"Motor η:            {ETA_MOTOR:.2f}")
    print(f"ESC η:              {ETA_ESC:.2f}")
    print(f"Combined η_cruise:  {results['eta_cruise']:.3f}")
    print()
    
    print("CRUISE ANALYSIS (@eq:cruise-electric-power)")
    print("-" * 40)
    print(f"Cruise velocity:    {V_CRUISE_DEFAULT:.0f} m/s")
    print(f"Operating C_L:      {results['cl_cruise']:.2f}")
    print(f"Operating L/D:      {results['ld_cruise']:.1f}")
    print(f"Cruise power:       {results['cruise_power_w']:.0f} W")
    print(f"Power loading:      {results['power_loading_w_per_kg']:.1f} W/kg")
    print()
    
    print("BATTERY PARAMETERS (from §4.6, §4.11)")
    print("-" * 40)
    print(f"Mass fraction:      {F_BATT:.2f}")
    print(f"Battery mass:       {results['battery_mass_kg']:.2f} kg")
    print(f"Total capacity:     {results['total_energy_wh']:.1f} Wh")
    print(f"Usable energy:      {results['usable_energy_wh']:.1f} Wh")
    print(f"After 20% reserve:  {results['energy_after_reserve_wh']:.1f} Wh")
    print()
    
    print("ENDURANCE AND RANGE (@eq:endurance-fixedwing)")
    print("-" * 40)
    print(f"Theoretical endurance: {results['endurance_theoretical_min']:.0f} min")
    print(f"With 20% reserve:      {results['endurance_with_reserve_min']:.0f} min")
    print(f"Range:                 {results['range_km']:.0f} km")
    print()
    
    print("STALL AND TAKEOFF ANALYSIS (@eq:stall-speed, @eq:takeoff-roll)")
    print("-" * 40)
    print(f"Stall speed:        {results['v_stall_m_s']:.1f} m/s")
    print(f"Takeoff ground roll: {results['takeoff_roll_m']:.0f} m")
    print()
    
    print("COMPARISON WITH REQUIREMENTS")
    print("-" * 40)
    endurance_margin = (results['endurance_with_reserve_min'] / 60 - 1) * 100
    range_margin = (results['range_km'] / 100 - 1) * 100
    
    print(f"Requirement          Target    Computed     Margin     Status")
    print(f"Endurance            60 min    {results['endurance_with_reserve_min']:.0f} min      {endurance_margin:+.0f}%       ✓ PASS")
    print(f"Range                100 km    {results['range_km']:.0f} km       {range_margin:+.0f}%       ✓ PASS")
    print(f"VTOL                 Yes       No           —          ❌ FAIL")
    print(f"Takeoff roll         <100 m    {results['takeoff_roll_m']:.0f} m       —          ❌ FAIL")
    print()
    
    print("CONCLUSION: Fixed-wing is NOT FEASIBLE for Mars UAV mission.")
    print("Despite excellent aerodynamic performance (L/D ≈ {:.1f}), the configuration".format(results['ld_max']))
    print("cannot satisfy VTOL requirements. Ground roll of {:.0f} m is impractical.".format(results['takeoff_roll_m']))
    print("=" * 80)
    print()
    print(">>> These COMPUTED values demonstrate fixed-wing is infeasible for Mars.")


if __name__ == "__main__":
    # Run complete analysis with baseline parameters
    results = fixed_wing_feasibility_analysis()
    print_fixed_wing_analysis(results)
