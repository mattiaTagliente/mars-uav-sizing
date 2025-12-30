"""
Derived Requirements Calculations
==================================

Implements calculations from manuscript Section 4.12 (Derived Requirements).

Equations:
    @eq:stall-speed        - V_stall = sqrt(2×(W/S)/(ρ×C_L,max))
    @eq:wing-loading-limit - (W/S)_max = 0.5×ρ×V_min²×C_L,max
    @eq:reynolds-cruise    - Re = ρ×V×c/μ
    @eq:reynolds-chord     - c = Re×μ/(ρ×V)
    @eq:wing-area-from-ar  - S = c²×AR
    @eq:mach-cruise        - M = V/a

Reference:
    - Manuscript: sections_en/04_12_derived-requirements.md

Last Updated: 2025-12-29
"""

import math
from datetime import datetime
from typing import Dict, Any

from ..config import get_param


def stall_speed(wing_loading: float = None) -> float:
    """
    Calculate stall speed from wing loading.

    Implements @eq:stall-speed from §4.12:
        V_stall = sqrt(2 × (W/S) / (ρ × C_L,max))

    Parameters
    ----------
    wing_loading : float, optional
        Wing loading in N/m² (default: from Reynolds-based derivation)

    Returns
    -------
    float
        Stall speed in m/s
    """
    if wing_loading is None:
        # Use Reynolds-based wing loading as default
        wing_loading = wing_loading_from_reynolds()

    rho = get_param('environment.arcadia_planitia.density_kg_m3')
    cl_max = get_param('aerodynamic.airfoil.cl_max')

    return math.sqrt(2 * wing_loading / (rho * cl_max))


def minimum_flight_speed(wing_loading: float = None) -> float:
    """
    Calculate minimum flight speed with safety margin.
    
    V_min = factor × V_stall
    
    Parameters
    ----------
    wing_loading : float, optional
        Wing loading in N/m²
        
    Returns
    -------
    float
        Minimum safe flight speed in m/s
    """
    v_stall = stall_speed(wing_loading)
    factor = get_param('mission.velocity.v_min_factor')
    return factor * v_stall


def maximum_wing_loading(v_min: float = None) -> float:
    """
    Calculate maximum allowable wing loading from stall constraint.
    
    Implements @eq:wing-loading-limit from §4.12:
        (W/S)_max = 0.5 × ρ × V_min² × C_L,max
    
    Parameters
    ----------
    v_min : float, optional
        Minimum flight speed (default: from config)
        
    Returns
    -------
    float
        Maximum wing loading in N/m²
    """
    if v_min is None:
        v_stall = get_param('mission.velocity.v_stall_m_s')
        factor = get_param('mission.velocity.v_min_factor')
        v_min = v_stall * factor
    
    rho = get_param('environment.arcadia_planitia.density_kg_m3')
    cl_max = get_param('aerodynamic.airfoil.cl_max')
    
    return 0.5 * rho * v_min**2 * cl_max


def chord_from_reynolds(target_re: float = 60000) -> float:
    """
    Calculate required chord for target Reynolds number.

    Implements @eq:reynolds-chord from §4.12 (derived from @eq:reynolds-definition):
        c = Re × μ / (ρ × V)

    This is the fundamental equation linking Reynolds number target
    to required wing geometry in the Mars atmosphere.

    Parameters
    ----------
    target_re : float
        Target Reynolds number (default: 60,000 for E387 performance)

    Returns
    -------
    float
        Required mean chord in m
    """
    rho = get_param('environment.arcadia_planitia.density_kg_m3')
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    mu = get_param('environment.arcadia_planitia.viscosity_Pa_s')

    return target_re * mu / (rho * v_cruise)


def wing_area_from_reynolds(target_re: float = 60000, aspect_ratio: float = None) -> float:
    """
    Calculate required wing area from Reynolds number target.

    Implements @eq:wing-area-from-ar from §4.12:
        S = c̄² × AR

    where c̄ is derived from @eq:reynolds-chord.

    Parameters
    ----------
    target_re : float
        Target Reynolds number (default: 60,000)
    aspect_ratio : float, optional
        Aspect ratio (default: from config)

    Returns
    -------
    float
        Required wing area in m²
    """
    if aspect_ratio is None:
        aspect_ratio = get_param('aerodynamic.wing.aspect_ratio')

    chord = chord_from_reynolds(target_re)
    return chord**2 * aspect_ratio


def wing_loading_from_reynolds(mtow_kg: float = None, target_re: float = 60000) -> float:
    """
    Calculate wing loading consistent with Reynolds number target.

    Implements the relationship between Re, chord, and wing loading
    from @eq:reynolds-chord and wing geometry:
        W/S = W / S = (m × g) / (c̄² × AR)

    Parameters
    ----------
    mtow_kg : float, optional
        Maximum takeoff weight in kg (default: from config)
    target_re : float
        Target Reynolds number (default: 60,000)

    Returns
    -------
    float
        Wing loading in N/m²
    """
    if mtow_kg is None:
        mtow_kg = get_param('mission.mass.mtow_kg')

    g = get_param('physical.mars.g')
    weight_n = mtow_kg * g

    wing_area = wing_area_from_reynolds(target_re)
    return weight_n / wing_area


def cruise_reynolds(chord: float = None) -> float:
    """
    Calculate Reynolds number at cruise conditions.

    Implements @eq:reynolds-cruise from §4.12:
        Re = ρ × V × c / μ

    Parameters
    ----------
    chord : float, optional
        Wing chord in m (default: from config mean_chord_m)

    Returns
    -------
    float
        Reynolds number
    """
    if chord is None:
        chord = get_param('aerodynamic.wing.mean_chord_m')

    rho = get_param('environment.arcadia_planitia.density_kg_m3')
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    mu = get_param('environment.arcadia_planitia.viscosity_Pa_s')

    return rho * v_cruise * chord / mu


def cruise_mach() -> float:
    """
    Calculate Mach number at cruise.
    
    Implements @eq:mach-cruise from §4.12:
        M = V / a
    
    Returns
    -------
    float
        Mach number
    """
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    a = get_param('environment.arcadia_planitia.speed_of_sound_m_s')
    return v_cruise / a


def wing_area_from_loading(mtow_kg: float = None, wing_loading: float = None) -> float:
    """
    Calculate wing area from MTOW and wing loading.

    S = W / (W/S) = (m × g) / (W/S)

    Parameters
    ----------
    mtow_kg : float, optional
        Maximum takeoff weight in kg (default: from config)
    wing_loading : float, optional
        Wing loading in N/m² (default: from stall constraint)

    Returns
    -------
    float
        Wing area in m²
    """
    if mtow_kg is None:
        mtow_kg = get_param('mission.mass.mtow_kg')
    if wing_loading is None:
        # Default: compute from stall constraint (V_min-based)
        wing_loading = maximum_wing_loading()

    g = get_param('physical.mars.g')
    weight_n = mtow_kg * g

    return weight_n / wing_loading


def wingspan_from_area(wing_area: float, aspect_ratio: float = None) -> float:
    """
    Calculate wingspan from wing area and aspect ratio.
    
    b = sqrt(AR × S)
    
    Parameters
    ----------
    wing_area : float
        Wing area in m²
    aspect_ratio : float, optional
        Aspect ratio (default: from config)
        
    Returns
    -------
    float
        Wingspan in m
    """
    if aspect_ratio is None:
        aspect_ratio = get_param('aerodynamic.wing.aspect_ratio')
    
    return math.sqrt(aspect_ratio * wing_area)


def mean_chord(wing_area: float, wingspan: float) -> float:
    """
    Calculate mean aerodynamic chord.
    
    c = S / b
    
    Parameters
    ----------
    wing_area : float
        Wing area in m²
    wingspan : float
        Wingspan in m
        
    Returns
    -------
    float
        Mean chord in m
    """
    return wing_area / wingspan


def derived_requirements_analysis() -> Dict[str, Any]:
    """
    Complete derived requirements analysis.

    Includes both Reynolds-based geometry derivation (from §4.12 cruise velocity)
    and stall constraint-based wing loading (from §5.2 matching chart).

    Returns
    -------
    dict
        All derived requirements including both derivation approaches
    """
    g = get_param('physical.mars.g')
    mtow_kg = get_param('mission.mass.mtow_kg')
    weight_n = mtow_kg * g
    ar = get_param('aerodynamic.wing.aspect_ratio')

    # Velocity requirements
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    v_min_factor = get_param('mission.velocity.v_min_factor')

    # ==========================================================================
    # REYNOLDS-BASED DERIVATION (from §4.12)
    # Target Re = 60,000 → chord → wing area → wing loading
    # ==========================================================================
    target_re = 60000
    chord_re = chord_from_reynolds(target_re)
    wing_area_re = wing_area_from_reynolds(target_re, ar)
    wingspan_re = wingspan_from_area(wing_area_re, ar)
    ws_re = wing_loading_from_reynolds(mtow_kg, target_re)
    v_stall_re = stall_speed(ws_re)
    v_min_re = v_stall_re * v_min_factor

    # ==========================================================================
    # STALL CONSTRAINT-BASED DERIVATION (from §5.2 matching chart)
    # V_stall (config) → V_min → W/S_max → wing area
    # ==========================================================================
    v_stall_config = get_param('mission.velocity.v_stall_m_s')
    v_min_stall = v_stall_config * v_min_factor
    ws_stall = maximum_wing_loading(v_min_stall)
    wing_area_stall = wing_area_from_loading(mtow_kg, ws_stall)
    wingspan_stall = wingspan_from_area(wing_area_stall, ar)
    chord_stall = mean_chord(wing_area_stall, wingspan_stall)
    re_stall = cruise_reynolds(chord_stall)

    # Mach number (same for both)
    M = cruise_mach()

    return {
        # Mass
        'mtow_kg': mtow_kg,
        'weight_n': weight_n,

        # Velocity
        'v_cruise_m_s': v_cruise,
        'v_min_factor': v_min_factor,

        # Reynolds-based derivation (§4.12)
        'target_reynolds': target_re,
        're_chord_m': chord_re,
        're_wing_area_m2': wing_area_re,
        're_wingspan_m': wingspan_re,
        're_wing_loading': ws_re,
        're_v_stall_m_s': v_stall_re,
        're_v_min_m_s': v_min_re,

        # Stall-based derivation (matching chart)
        'stall_v_stall_m_s': v_stall_config,
        'stall_v_min_m_s': v_min_stall,
        'stall_wing_loading': ws_stall,
        'stall_wing_area_m2': wing_area_stall,
        'stall_wingspan_m': wingspan_stall,
        'stall_chord_m': chord_stall,
        'stall_reynolds': re_stall,

        # Common
        'mach_cruise': M,
        'aspect_ratio': ar,
    }


def print_analysis():
    """Print formatted derived requirements analysis."""
    results = derived_requirements_analysis()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("DERIVED REQUIREMENTS (Section 4.12)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values from config/ YAML files")
    print()

    print("MASS AND WEIGHT")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Weight (Mars):      {results['weight_n']:.2f} N")
    print(f"  Aspect ratio:       {results['aspect_ratio']}")
    print()

    print("VELOCITY REQUIREMENTS")
    print("-" * 50)
    print(f"  V_cruise:           {results['v_cruise_m_s']:.2f} m/s")
    print(f"  V_min factor:       {results['v_min_factor']}")
    print(f"  Mach number:        {results['mach_cruise']:.4f}")
    print()

    print("=" * 80)
    print("DERIVATION APPROACH 1: Reynolds-based (Section 4.12)")
    print("  Target Re = 60,000 -> chord -> wing area -> W/S -> V_stall")
    print("=" * 80)
    print(f"  Target Reynolds:    {results['target_reynolds']:.0f}")
    print(f"  Required chord:     {results['re_chord_m']:.4f} m")
    print(f"  Wing area:          {results['re_wing_area_m2']:.4f} m2")
    print(f"  Wingspan:           {results['re_wingspan_m']:.4f} m")
    print(f"  Wing loading:       {results['re_wing_loading']:.4f} N/m2")
    print(f"  V_stall:            {results['re_v_stall_m_s']:.4f} m/s")
    print(f"  V_min (1.2xV_stall):{results['re_v_min_m_s']:.4f} m/s")
    print()

    print("=" * 80)
    print("DERIVATION APPROACH 2: Stall-constrained (Matching chart)")
    print("  V_stall (config) -> V_min -> W/S_max -> wing area -> chord -> Re")
    print("=" * 80)
    print(f"  V_stall (config):   {results['stall_v_stall_m_s']:.4f} m/s")
    print(f"  V_min (1.2xV_stall):{results['stall_v_min_m_s']:.4f} m/s")
    print(f"  Wing loading max:   {results['stall_wing_loading']:.4f} N/m2")
    print(f"  Wing area:          {results['stall_wing_area_m2']:.4f} m2")
    print(f"  Wingspan:           {results['stall_wingspan_m']:.4f} m")
    print(f"  Mean chord:         {results['stall_chord_m']:.4f} m")
    print(f"  Achieved Reynolds:  {results['stall_reynolds']:.0f}")
    print()

    print("=" * 80)
    print("COMPARISON")
    print("=" * 80)
    re_ws = results['re_wing_loading']
    stall_ws = results['stall_wing_loading']
    print(f"  W/S (Reynolds):     {re_ws:.4f} N/m2")
    print(f"  W/S (Stall):        {stall_ws:.4f} N/m2")
    print(f"  Ratio:              {stall_ws/re_ws:.4f}")
    print()
    print("  Note: The stall-based derivation determines W/S for the matching")
    print("        chart. The Reynolds-based derivation shows the geometry")
    print("        required to achieve Re=60,000 at cruise velocity.")
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
