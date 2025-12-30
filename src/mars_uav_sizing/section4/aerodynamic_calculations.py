"""
Aerodynamic Calculations
=========================

Implements aerodynamic calculations from manuscript Section 4.7.

Equations:
    @eq:induced-drag-factor  - K = 1/(π×AR×e)
    @eq:drag-polar           - C_D = C_D0 + K×C_L²
    @eq:ld-max               - (L/D)_max = 0.5×sqrt(π×AR×e/C_D0)
    @eq:cl-optimal           - C_L* = sqrt(C_D0×π×AR×e)
    @eq:oswald-sadraey       - e = 1.78×(1-0.045×AR^0.68)-0.64

Reference: 
    - Manuscript: sections_en/04_07_aerodynamic-analysis.md
    - Sadraey (2013), Aircraft Design: A Systems Engineering Approach

Last Updated: 2025-12-29
"""

import math
from datetime import datetime
from typing import Dict, Any, Tuple

from ..config import get_param


def oswald_efficiency_sadraey(aspect_ratio: float) -> float:
    """
    Calculate Oswald span efficiency using Sadraey correlation.
    
    Implements @eq:oswald-sadraey from §4.7:
        e = 1.78 × (1 - 0.045 × AR^0.68) - 0.64
    
    Reference: Sadraey (2013), Section 5.3.2
    
    Parameters
    ----------
    aspect_ratio : float
        Wing aspect ratio
        
    Returns
    -------
    float
        Oswald efficiency factor
    """
    return 1.78 * (1 - 0.045 * aspect_ratio**0.68) - 0.64


def induced_drag_factor(aspect_ratio: float = None, oswald_e: float = None) -> float:
    """
    Calculate induced drag factor K.
    
    Implements @eq:induced-drag-factor from §4.7:
        K = 1 / (π × AR × e)
    
    Parameters
    ----------
    aspect_ratio : float, optional
        Aspect ratio (default: from config)
    oswald_e : float, optional
        Oswald efficiency (default: from config)
        
    Returns
    -------
    float
        Induced drag factor K
    """
    if aspect_ratio is None:
        aspect_ratio = get_param('aerodynamic.wing.aspect_ratio')
    if oswald_e is None:
        oswald_e = get_param('aerodynamic.wing.oswald_efficiency')
    
    return 1 / (math.pi * aspect_ratio * oswald_e)


def drag_coefficient(c_l: float, cd0: float = None, k: float = None) -> float:
    """
    Calculate total drag coefficient from parabolic polar.
    
    Implements @eq:drag-polar from §4.7:
        C_D = C_D0 + K × C_L²
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    cd0 : float, optional
        Zero-lift drag coefficient (default: from config)
    k : float, optional
        Induced drag factor (default: computed from config)
        
    Returns
    -------
    float
        Total drag coefficient
    """
    if cd0 is None:
        cd0 = get_param('aerodynamic.drag_polar.cd0')
    if k is None:
        k = induced_drag_factor()
    
    return cd0 + k * c_l**2


def lift_to_drag(c_l: float, cd0: float = None, k: float = None) -> float:
    """
    Calculate lift-to-drag ratio.
    
    L/D = C_L / C_D
    
    Parameters
    ----------
    c_l : float
        Lift coefficient
    cd0 : float, optional
        Zero-lift drag coefficient
    k : float, optional
        Induced drag factor
        
    Returns
    -------
    float
        Lift-to-drag ratio
    """
    cd = drag_coefficient(c_l, cd0, k)
    if cd == 0:
        return 0
    return c_l / cd


def maximum_ld() -> Tuple[float, float]:
    """
    Calculate maximum L/D and corresponding optimal C_L.
    
    Implements @eq:ld-max and @eq:cl-optimal from §4.7:
        (L/D)_max = 0.5 × sqrt(π × AR × e / C_D0)
        C_L* = sqrt(C_D0 × π × AR × e)
    
    Returns
    -------
    tuple
        (L/D_max, C_L_optimal)
    """
    ar = get_param('aerodynamic.wing.aspect_ratio')
    e = get_param('aerodynamic.wing.oswald_efficiency')
    cd0 = get_param('aerodynamic.drag_polar.cd0')
    
    cl_opt = math.sqrt(cd0 * math.pi * ar * e)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    
    return ld_max, cl_opt


def quadplane_ld() -> float:
    """
    Calculate QuadPlane L/D with rotor drag penalty.
    
    (L/D)_qp = penalty × (L/D)_max
    
    Returns
    -------
    float
        QuadPlane L/D
    """
    ld_max, _ = maximum_ld()
    penalty = get_param('aerodynamic.quadplane.ld_penalty_factor')
    return ld_max * penalty


def drag_polar_analysis() -> Dict[str, float]:
    """
    Complete drag polar analysis.
    
    Returns
    -------
    dict
        All drag polar parameters
    """
    ar = get_param('aerodynamic.wing.aspect_ratio')
    e = get_param('aerodynamic.wing.oswald_efficiency')
    cd0 = get_param('aerodynamic.drag_polar.cd0')
    
    k = induced_drag_factor(ar, e)
    ld_max, cl_opt = maximum_ld()
    ld_qp = quadplane_ld()
    ld_rotor = get_param('aerodynamic.rotorcraft.ld_effective')
    
    # Compute e from Sadraey for verification
    e_sadraey = oswald_efficiency_sadraey(ar)
    
    return {
        'aspect_ratio': ar,
        'oswald_e': e,
        'oswald_e_sadraey': e_sadraey,
        'cd0': cd0,
        'k': k,
        'ld_max': ld_max,
        'cl_optimal': cl_opt,
        'ld_quadplane': ld_qp,
        'ld_rotorcraft': ld_rotor,
    }


def print_analysis():
    """Print formatted aerodynamic analysis."""
    results = drag_polar_analysis()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("AERODYNAMIC CALCULATIONS (Section 4.7)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values from config/aerodynamic_parameters.yaml")
    print()
    
    print("WING PARAMETERS")
    print("-" * 50)
    print(f"  Aspect ratio (AR):   {results['aspect_ratio']}")
    print(f"  Oswald efficiency:   {results['oswald_e']:.4f} (from config)")
    print(f"  Sadraey correlation: {results['oswald_e_sadraey']:.4f} (verification)")
    print()
    
    print("DRAG POLAR (@eq:drag-polar)")
    print("-" * 50)
    print(f"  C_D0:               {results['cd0']:.4f}")
    print(f"  K = 1/(π×AR×e):     {results['k']:.4f}")
    print(f"  C_D = C_D0 + K×C_L²")
    print()
    
    print("LIFT-TO-DRAG RATIO (@eq:ld-max)")
    print("-" * 50)
    print(f"  (L/D)_max:          {results['ld_max']:.2f}")
    print(f"  C_L optimal:        {results['cl_optimal']:.3f}")
    print()
    
    print("CONFIGURATION-SPECIFIC L/D")
    print("-" * 50)
    print(f"  Fixed-wing:         {results['ld_max']:.2f}")
    print(f"  QuadPlane:          {results['ld_quadplane']:.2f} (10% penalty)")
    print(f"  Rotorcraft:         {results['ld_rotorcraft']:.1f} (equivalent)")
    
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
