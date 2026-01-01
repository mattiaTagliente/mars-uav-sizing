#!/usr/bin/env python3
"""
Propeller Sizing Module
========================

Implements propeller sizing methodology for the Mars UAV.
Covers both lift propellers (hover) and cruise propellers (forward flight).

The sizing approach uses momentum theory and empirical correlations adapted
for Mars atmospheric conditions. Propeller selection is then verified against
commercial component specifications.

Key equations:
    @eq:prop-diameter-hover   - Lift propeller diameter from disk loading
    @eq:prop-diameter-cruise  - Cruise propeller diameter from thrust
    @eq:tip-speed            - Tip speed constraint for Mars Mach limit
    @eq:advance-ratio        - Advance ratio for cruise propeller

Reference:
    - Manuscript: sections_en/06_03_geometry-selection-sec-geometry-selection.md
    - Leishman (2006), Principles of Helicopter Aerodynamics, Chapter 2
    - Sadraey (2020), Electric Aircraft, Chapter 9

Last Updated: 2026-01-01
"""

import math
from typing import Dict, Any, Tuple
from datetime import datetime

from ..config import (
    get_mars_gravity,
    get_density,
    get_mtow,
    get_param,
    get_propulsion_efficiencies,
    get_mission_params,
)


# =============================================================================
# ATMOSPHERIC CONSTRAINTS
# =============================================================================

def get_speed_of_sound() -> float:
    """
    Get Mars speed of sound from atmospheric model.

    Pre-computed for operating altitude at Arcadia Planitia:
        a = sqrt(gamma × R × T) = 229.7 m/s

    Returns
    -------
    float
        Speed of sound in m/s
    """
    return get_param('environment.arcadia_planitia.speed_of_sound_m_s')


def max_tip_speed(mach_limit: float = 0.7) -> float:
    """
    Calculate maximum tip speed from Mach limit.

    Implements @eq:tip-speed:
        V_tip,max = M_limit × a

    Parameters
    ----------
    mach_limit : float
        Maximum allowable tip Mach number (default 0.7)

    Returns
    -------
    float
        Maximum tip speed in m/s
    """
    a = get_speed_of_sound()
    return mach_limit * a


# =============================================================================
# LIFT PROPELLER SIZING
# =============================================================================

def lift_propeller_sizing() -> Dict[str, Any]:
    """
    Size lift propellers from hover requirements.

    Uses disk loading and motor count to derive per-rotor thrust and diameter.

    Implements @eq:prop-diameter-hover:
        D_prop = sqrt(4 × T_per_rotor / (pi × DL))

    Returns
    -------
    dict
        Lift propeller sizing results
    """
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    weight_n = mtow_kg * g_mars

    # Disk loading
    disk_loading = get_param('geometry.rotor.disk_loading_N_m2')

    # Motor count
    n_lift_motors = get_param('geometry.propulsion_config.lift.n_motors')

    # Total disk area required
    total_disk_area = weight_n / disk_loading

    # Per-rotor values
    thrust_per_rotor = weight_n / n_lift_motors
    disk_area_per_rotor = total_disk_area / n_lift_motors

    # Propeller diameter
    diameter_m = 2 * math.sqrt(disk_area_per_rotor / math.pi)
    diameter_in = diameter_m * 39.37

    # Tip speed check at hover RPM (estimate)
    # Typical hover tip speed: 100-150 m/s for small UAVs
    # RPM = V_tip / (pi × D) × 60
    v_tip_max = max_tip_speed(0.7)
    rpm_max = (v_tip_max / (math.pi * diameter_m)) * 60

    # Conservative operating RPM (70% of max)
    rpm_operating = 0.7 * rpm_max
    v_tip_operating = (rpm_operating / 60) * math.pi * diameter_m
    mach_tip = v_tip_operating / get_speed_of_sound()

    # Selected propeller from config
    prop_model = get_param('propulsion.components.lift.propeller.model')
    prop_diameter_in = get_param('propulsion.components.lift.propeller.diameter_in')

    return {
        'n_motors': n_lift_motors,
        'total_thrust_n': weight_n,
        'thrust_per_rotor_n': thrust_per_rotor,
        'disk_loading_n_m2': disk_loading,
        'total_disk_area_m2': total_disk_area,
        'disk_area_per_rotor_m2': disk_area_per_rotor,
        'diameter_required_m': diameter_m,
        'diameter_required_in': diameter_in,
        'rpm_max_tip_limit': rpm_max,
        'rpm_operating': rpm_operating,
        'v_tip_operating_m_s': v_tip_operating,
        'mach_tip': mach_tip,
        'selected_model': prop_model,
        'selected_diameter_in': prop_diameter_in,
    }


# =============================================================================
# CRUISE PROPELLER SIZING
# =============================================================================

def cruise_propeller_sizing() -> Dict[str, Any]:
    """
    Size cruise propellers from forward flight requirements.

    Uses cruise power and velocity to derive propeller parameters.

    Implements @eq:prop-diameter-cruise from momentum theory:
        D_cruise >= sqrt(8 × T / (pi × rho × V^2 × eta))

    Returns
    -------
    dict
        Cruise propeller sizing results
    """
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    weight_n = mtow_kg * g_mars

    # Cruise parameters
    v_cruise = get_mission_params()['v_cruise']

    # L/D for cruise thrust estimate
    from ..section5.fixed_wing import maximum_ld
    ld_max, cl_opt = maximum_ld()
    ld_penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    ld_cruise = ld_max * ld_penalty

    # Cruise thrust = D = W / (L/D)
    cruise_thrust_n = weight_n / ld_cruise

    # Motor count
    n_cruise_motors = get_param('geometry.propulsion_config.cruise.n_motors')
    thrust_per_motor = cruise_thrust_n / n_cruise_motors

    # Propeller efficiencies
    eta_prop = get_propulsion_efficiencies()['eta_prop']

    # Minimum diameter from momentum theory (actuator disk)
    # For efficient propellers, want low disk loading
    # T = 0.5 × rho × A × V^2 × eta × CT
    # Typical CT ~ 0.1 for cruise props
    # D_min = sqrt(8 × T / (pi × rho × V^2 × CT))
    ct_typical = 0.10
    d_min_m = math.sqrt(8 * cruise_thrust_n / (math.pi * rho * v_cruise**2 * ct_typical))
    d_min_in = d_min_m * 39.37

    # Selected propeller from config
    prop_model = get_param('propulsion.components.cruise.propeller.model')
    prop_diameter_in = get_param('propulsion.components.cruise.propeller.diameter_in')
    prop_pitch_in = get_param('propulsion.components.cruise.propeller.pitch_in')

    # Advance ratio for selected propeller
    # J = V / (n × D)
    # Estimate RPM from typical cruise operation
    rpm_cruise = 8000  # Typical for high-KV cruise motor
    diameter_m = prop_diameter_in / 39.37
    n_rps = rpm_cruise / 60
    advance_ratio = v_cruise / (n_rps * diameter_m)

    # Tip speed at cruise
    v_tip = (rpm_cruise / 60) * math.pi * diameter_m
    mach_tip = v_tip / get_speed_of_sound()

    return {
        'n_motors': n_cruise_motors,
        'cruise_thrust_n': cruise_thrust_n,
        'thrust_per_motor_n': thrust_per_motor,
        'ld_cruise': ld_cruise,
        'v_cruise_m_s': v_cruise,
        'diameter_min_m': d_min_m,
        'diameter_min_in': d_min_in,
        'selected_model': prop_model,
        'selected_diameter_in': prop_diameter_in,
        'selected_pitch_in': prop_pitch_in,
        'advance_ratio': advance_ratio,
        'rpm_cruise': rpm_cruise,
        'v_tip_m_s': v_tip,
        'mach_tip': mach_tip,
    }


# =============================================================================
# COMPLETE PROPELLER ANALYSIS
# =============================================================================

def propeller_sizing_analysis() -> Dict[str, Any]:
    """
    Complete propeller sizing analysis for both lift and cruise systems.

    Returns
    -------
    dict
        Complete propeller sizing results
    """
    lift = lift_propeller_sizing()
    cruise = cruise_propeller_sizing()

    # UAV envelope dimensions for hangar
    # Lift propeller span (tip-to-tip across diagonal)
    n_arms = get_param('geometry.propulsion_config.lift.n_arms')
    wingspan = get_param('geometry.wing.taper_ratio')  # Need actual wingspan

    # Get wingspan from matching chart
    from ..section5.matching_chart import derive_geometry
    geom = derive_geometry()
    wingspan_m = geom['wingspan_m']

    # Rotor arm length (approximate as fraction of semi-span)
    arm_length_fraction = 0.4  # Typical for QuadPlane
    arm_length = arm_length_fraction * wingspan_m / 2

    # Lift propeller diameter in meters
    lift_prop_dia_m = lift['selected_diameter_in'] / 39.37

    # Operational envelope
    # Note: Rotors are mounted on wing booms WITHIN the wingspan, not extending beyond
    envelope_width = wingspan_m  # Rotors inside wingspan
    fuselage_length = get_param('design.fuselage.length_m')
    total_aircraft_length = get_param('design.fuselage.total_length_m')
    envelope_length = total_aircraft_length  # Use total length including boom extension

    return {
        'lift': lift,
        'cruise': cruise,
        'envelope': {
            'wingspan_m': wingspan_m,
            'lift_prop_diameter_m': lift_prop_dia_m,
            'cruise_prop_diameter_m': cruise['selected_diameter_in'] / 39.37,
            'envelope_width_m': envelope_width,
            'envelope_length_m': envelope_length,
        },
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted propeller sizing results."""
    if results is None:
        results = propeller_sizing_analysis()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lift = results['lift']
    cruise = results['cruise']
    env = results['envelope']

    print("=" * 70)
    print("PROPELLER SIZING ANALYSIS (Section 6.3)")
    print("=" * 70)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()

    print("LIFT PROPELLER SIZING (Hover)")
    print("-" * 50)
    print(f"  Number of rotors:      {lift['n_motors']}")
    print(f"  Total hover thrust:    {lift['total_thrust_n']:.2f} N")
    print(f"  Thrust per rotor:      {lift['thrust_per_rotor_n']:.2f} N")
    print(f"  Disk loading:          {lift['disk_loading_n_m2']:.1f} N/m2")
    print(f"  Total disk area:       {lift['total_disk_area_m2']:.3f} m2")
    print(f"  Disk area per rotor:   {lift['disk_area_per_rotor_m2']:.4f} m2")
    print(f"  Required diameter:     {lift['diameter_required_m']:.3f} m ({lift['diameter_required_in']:.1f} in)")
    print(f"  Selected propeller:    {lift['selected_model']} ({lift['selected_diameter_in']} in)")
    print(f"  Tip Mach (operating):  {lift['mach_tip']:.3f}")
    print()

    print("CRUISE PROPELLER SIZING (Forward Flight)")
    print("-" * 50)
    print(f"  Number of motors:      {cruise['n_motors']}")
    print(f"  Cruise velocity:       {cruise['v_cruise_m_s']:.1f} m/s")
    print(f"  Cruise L/D:            {cruise['ld_cruise']:.2f}")
    print(f"  Total cruise thrust:   {cruise['cruise_thrust_n']:.2f} N")
    print(f"  Thrust per motor:      {cruise['thrust_per_motor_n']:.2f} N")
    print(f"  Minimum diameter:      {cruise['diameter_min_m']:.3f} m ({cruise['diameter_min_in']:.1f} in)")
    print(f"  Selected propeller:    {cruise['selected_model']} ({cruise['selected_diameter_in']} in)")
    print(f"  Advance ratio J:       {cruise['advance_ratio']:.2f}")
    print(f"  Tip Mach (cruise):     {cruise['mach_tip']:.3f}")
    print()

    print("UAV ENVELOPE (for Hangar Sizing)")
    print("-" * 50)
    print(f"  Wingspan:              {env['wingspan_m']:.2f} m")
    print(f"  Lift prop diameter:    {env['lift_prop_diameter_m']:.3f} m")
    print(f"  Cruise prop diameter:  {env['cruise_prop_diameter_m']:.3f} m")
    print(f"  Envelope width:        {env['envelope_width_m']:.2f} m (with rotors)")
    print(f"  Envelope length:       {env['envelope_length_m']:.2f} m (fuselage)")
    print()

    # Verification
    print("VERIFICATION")
    print("-" * 50)
    lift_ok = lift['selected_diameter_in'] >= lift['diameter_required_in'] * 0.9
    cruise_ok = cruise['selected_diameter_in'] >= cruise['diameter_min_in'] * 0.9
    mach_ok = lift['mach_tip'] < 0.7 and cruise['mach_tip'] < 0.7

    print(f"  Lift prop sizing:      {'[PASS]' if lift_ok else '[WARN]'}")
    print(f"  Cruise prop sizing:    {'[PASS]' if cruise_ok else '[WARN]'}")
    print(f"  Tip Mach limits:       {'[PASS]' if mach_ok else '[FAIL]'}")

    print("=" * 70)


if __name__ == "__main__":
    print_analysis()
