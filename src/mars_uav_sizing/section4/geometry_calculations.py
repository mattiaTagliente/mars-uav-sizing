"""
Geometry Calculations
======================

Implements geometry calculations from manuscript Section 4 (tail, fuselage, rotor).

Equations:
    @eq:horizontal-tail-area  - S_H = V_H × S × c / l_H
    @eq:vertical-tail-area    - S_V = V_V × S × b / l_V
    @eq:vtail-projection      - V-tail area decomposition
    @eq:rotor-diameter        - D = sqrt(4×A/π)

Reference: 
    - Manuscript: sections_en/04_05_tail-geometry.md
    - Roskam (2004), Airplane Design Part I-VIII

Last Updated: 2025-12-29
"""

import math
from datetime import datetime
from typing import Dict, Tuple, Any

from ..config import get_param


def tail_volume_coefficients() -> Tuple[float, float]:
    """
    Get tail volume coefficients with Mars-specific increase.
    
    Baseline values from Roskam (2004) for small aircraft.
    25% increase for reduced control effectiveness at low Reynolds numbers.
    
    Returns
    -------
    tuple
        (V_H, V_V) - horizontal and vertical tail volume coefficients
    """
    v_h = get_param('geometry.tail.v_h')
    v_v = get_param('geometry.tail.v_v')
    return v_h, v_v


def horizontal_tail_area(
    wing_area: float,
    mac: float,
    moment_arm: float,
    v_h: float = None
) -> float:
    """
    Calculate required horizontal tail area from volume coefficient.
    
    Implements @eq:horizontal-tail-area:
        V_H = S_H × l_H / (S × c̄)
        S_H = V_H × S × c̄ / l_H
    
    Parameters
    ----------
    wing_area : float
        Wing planform area in m²
    mac : float
        Mean aerodynamic chord in m
    moment_arm : float
        Distance from wing AC to tail AC in m
    v_h : float, optional
        Horizontal tail volume coefficient (default: from config)
        
    Returns
    -------
    float
        Required horizontal tail area in m²
    """
    if v_h is None:
        v_h = get_param('geometry.tail.v_h')
    
    return v_h * wing_area * mac / moment_arm


def vertical_tail_area(
    wing_area: float,
    wingspan: float,
    moment_arm: float,
    v_v: float = None
) -> float:
    """
    Calculate required vertical tail area from volume coefficient.
    
    Implements @eq:vertical-tail-area:
        V_V = S_V × l_V / (S × b)
        S_V = V_V × S × b / l_V
    
    Parameters
    ----------
    wing_area : float
        Wing planform area in m²
    wingspan : float
        Wing span in m
    moment_arm : float
        Distance from wing AC to tail AC in m
    v_v : float, optional
        Vertical tail volume coefficient (default: from config)
        
    Returns
    -------
    float
        Required vertical tail area in m²
    """
    if v_v is None:
        v_v = get_param('geometry.tail.v_v')
    
    return v_v * wing_area * wingspan / moment_arm


def vtail_geometry(
    sh_required: float,
    sv_required: float,
    dihedral_deg: float = None,
    aspect_ratio: float = None
) -> Dict[str, float]:
    """
    Calculate V-tail geometry from required projected areas.

    Implements @eq:vtail-projection:
        S_H = S_Vtail × cos²(Γ)
        S_V = S_Vtail × sin²(Γ)

    Parameters
    ----------
    sh_required : float
        Required horizontal projection area in m²
    sv_required : float
        Required vertical projection area in m²
    dihedral_deg : float, optional
        V-tail dihedral angle in degrees (default: from config)
    aspect_ratio : float, optional
        V-tail aspect ratio (default: from config)

    Returns
    -------
    dict
        V-tail geometry parameters
    """
    if dihedral_deg is None:
        dihedral_deg = get_param('geometry.tail.vtail_dihedral_deg')
    if aspect_ratio is None:
        aspect_ratio = get_param('geometry.tail.vtail_aspect_ratio')
    
    dihedral_rad = math.radians(dihedral_deg)
    cos2_gamma = math.cos(dihedral_rad) ** 2
    sin2_gamma = math.sin(dihedral_rad) ** 2
    
    # Calculate total V-tail area from horizontal requirement
    s_vtail_from_h = sh_required / cos2_gamma
    # Also calculate from vertical requirement
    s_vtail_from_v = sv_required / sin2_gamma
    
    # Use the larger to satisfy both requirements
    s_vtail_total = max(s_vtail_from_h, s_vtail_from_v)
    s_per_surface = s_vtail_total / 2
    
    # Calculate dimensions
    span_per_surface = math.sqrt(aspect_ratio * s_per_surface)
    chord = s_per_surface / span_per_surface
    
    return {
        's_vtail_total': s_vtail_total,
        's_per_surface': s_per_surface,
        'dihedral_deg': dihedral_deg,
        'span_per_surface': span_per_surface,
        'chord': chord,
        'aspect_ratio': aspect_ratio,
        'actual_sh': s_vtail_total * cos2_gamma,
        'actual_sv': s_vtail_total * sin2_gamma,
    }


def fuselage_length(wingspan: float, ratio: float = None) -> float:
    """
    Calculate fuselage length from wingspan and ratio.
    
    Based on commercial VTOL UAV benchmarks, median ratio is ~0.50.
    
    Parameters
    ----------
    wingspan : float
        Wing span in m
    ratio : float, optional
        Length/span ratio (default: from config)
        
    Returns
    -------
    float
        Fuselage length in m
    """
    if ratio is None:
        ratio = get_param('geometry.fuselage.length_to_span_ratio')
    
    return ratio * wingspan


def rotor_diameter(
    total_thrust: float,
    n_rotors: int,
    disk_loading: float = None
) -> float:
    """
    Calculate individual rotor diameter for target disk loading.
    
    Implements @eq:rotor-diameter:
        DL = T / A_total
        A_per_rotor = (T / n) / DL
        D = √(4 × A / π)
    
    Parameters
    ----------
    total_thrust : float
        Total thrust required in N
    n_rotors : int
        Number of rotors
    disk_loading : float, optional
        Target disk loading in N/m² (default: from config)
        
    Returns
    -------
    float
        Individual rotor diameter in m
    """
    if disk_loading is None:
        disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    
    area_per_rotor = (total_thrust / n_rotors) / disk_loading
    return math.sqrt(4 * area_per_rotor / math.pi)


def total_disk_area(thrust: float, disk_loading: float = None) -> float:
    """
    Calculate total rotor disk area from thrust and disk loading.
    
    A = T / DL
    
    Parameters
    ----------
    thrust : float
        Total thrust in N
    disk_loading : float, optional
        Disk loading in N/m² (default: from config)
        
    Returns
    -------
    float
        Total disk area in m²
    """
    if disk_loading is None:
        disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    
    return thrust / disk_loading


def geometry_analysis() -> Dict[str, Any]:
    """
    Complete geometry analysis for the baseline design.

    Uses stall-constrained wing loading from derived requirements
    and configuration parameters for all geometry constants.

    Returns
    -------
    dict
        All geometry parameters
    """
    g = get_param('physical.mars.g')
    mtow = get_param('mission.mass.mtow_kg')
    weight_n = mtow * g
    ar = get_param('aerodynamic.wing.aspect_ratio')

    # Wing geometry from stall-constrained derived requirements
    from .derived_requirements import (
        maximum_wing_loading,
        wing_area_from_loading,
        wingspan_from_area,
        mean_chord,
    )

    # Use stall constraint to determine wing loading (V_min-based)
    ws = maximum_wing_loading()
    s = wing_area_from_loading(mtow, ws)
    b = wingspan_from_area(s, ar)
    c = mean_chord(s, b)

    # Fuselage length
    l_fus = fuselage_length(b)

    # Tail geometry (moment arm from config ratio)
    moment_arm_ratio = get_param('geometry.tail.moment_arm_ratio')
    moment_arm = moment_arm_ratio * l_fus
    sh = horizontal_tail_area(s, c, moment_arm)
    sv = vertical_tail_area(s, b, moment_arm)
    vtail = vtail_geometry(sh, sv)

    # Rotor configuration from config
    n_rotors = get_param('geometry.rotor.n_rotors')
    d_rotor = rotor_diameter(weight_n, n_rotors)

    return {
        'wing_loading_n_m2': ws,
        'wing_area_m2': s,
        'wingspan_m': b,
        'mean_chord_m': c,
        'fuselage_length_m': l_fus,
        'moment_arm_ratio': moment_arm_ratio,
        'moment_arm_m': moment_arm,
        'sh_required_m2': sh,
        'sv_required_m2': sv,
        'vtail': vtail,
        'n_rotors': n_rotors,
        'rotor_diameter_m': d_rotor,
        'total_disk_area_m2': total_disk_area(weight_n),
    }


def print_analysis():
    """Print formatted geometry analysis."""
    results = geometry_analysis()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("GEOMETRY CALCULATIONS (Section 4)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values from config/ YAML files")
    print()

    print("WING GEOMETRY (from stall constraint)")
    print("-" * 50)
    print(f"  Wing loading:       {results['wing_loading_n_m2']:.2f} N/m2")
    print(f"  Wing area:          {results['wing_area_m2']:.3f} m2")
    print(f"  Wingspan:           {results['wingspan_m']:.2f} m")
    print(f"  Mean chord:         {results['mean_chord_m']:.3f} m")
    print()

    print("FUSELAGE GEOMETRY")
    print("-" * 50)
    print(f"  Fuselage length:    {results['fuselage_length_m']:.2f} m")
    print()

    print("TAIL GEOMETRY")
    print("-" * 50)
    print(f"  Moment arm ratio:   {results['moment_arm_ratio']:.2f} (from config)")
    print(f"  Moment arm:         {results['moment_arm_m']:.2f} m")
    print(f"  S_H required:       {results['sh_required_m2']:.3f} m2")
    print(f"  S_V required:       {results['sv_required_m2']:.3f} m2")
    vtail = results['vtail']
    print(f"  V-tail total area:  {vtail['s_vtail_total']:.3f} m2")
    print(f"  V-tail dihedral:    {vtail['dihedral_deg']:.0f} deg")
    print(f"  V-tail AR:          {vtail['aspect_ratio']:.1f} (from config)")
    print(f"  V-tail span/side:   {vtail['span_per_surface']:.2f} m")
    print(f"  V-tail chord:       {vtail['chord']:.3f} m")
    print()

    print("ROTOR GEOMETRY")
    print("-" * 50)
    print(f"  Number of rotors:   {results['n_rotors']} (from config)")
    print(f"  Rotor diameter:     {results['rotor_diameter_m']:.3f} m ({results['rotor_diameter_m']*39.37:.1f} in)")
    print(f"  Total disk area:    {results['total_disk_area_m2']:.3f} m2")

    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
