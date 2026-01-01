#!/usr/bin/env python3
"""
Tail Sizing Module
===================

Implements tail surface sizing methodology for the Mars UAV.
Uses volume coefficient method adapted for low-Reynolds Mars conditions.

The design uses a boom-mounted inverted V-tail configuration.
Tail surfaces are sized using increased volume coefficients (25% margin)
to compensate for reduced control effectiveness at Mars Reynolds numbers.

Key equations:
    @eq:vtail-vh        - Horizontal tail volume coefficient
    @eq:vtail-vv        - Vertical tail volume coefficient
    @eq:vtail-area      - V-tail surface area from combined coefficients
    @eq:vtail-span      - V-tail span from aspect ratio
    @eq:vtail-dihedral  - Dihedral angle for combined function

Reference:
    - Roskam (2004), Airplane Design Part II, Chapter 8
    - Manuscript: sections_en/06_03_geometry-selection-sec-geometry-selection.md

Last Updated: 2026-01-01
"""

import math
from typing import Dict, Any
from datetime import datetime

from ..config import get_param


def get_wing_geometry() -> Dict[str, float]:
    """
    Get wing geometry from matching chart analysis.

    Returns
    -------
    dict
        Wing geometry parameters
    """
    from ..section5.matching_chart import derive_geometry
    geom = derive_geometry()

    return {
        'wing_area_m2': geom['wing_area_m2'],
        'wingspan_m': geom['wingspan_m'],
        'chord_m': geom['chord_m'],
    }


def get_fuselage_geometry() -> Dict[str, float]:
    """
    Get fuselage geometry from configuration.

    Returns
    -------
    dict
        Fuselage geometry parameters
    """
    wingspan = get_wing_geometry()['wingspan_m']

    length_ratio = get_param('design.fuselage.length_to_span_ratio')
    fineness = get_param('design.fuselage.fineness_ratio')

    length_m = length_ratio * wingspan
    diameter_m = length_m / fineness

    return {
        'length_m': length_m,
        'diameter_m': diameter_m,
        'fineness_ratio': fineness,
        'length_to_span_ratio': length_ratio,
    }


def vtail_sizing() -> Dict[str, Any]:
    """
    Size V-tail surfaces using volume coefficient method.

    For an inverted V-tail configuration:
    - Horizontal component provides pitch control
    - Vertical component (from dihedral) provides yaw control
    - Combined surfaces use ruddervator mixing

    Implements @eq:vtail-area:
        S_H = V_H × S × MAC / l_H
        S_V = V_V × S × b / l_V
        S_V-tail = sqrt(S_H^2 + S_V^2) / (2 × cos(Gamma))

    Returns
    -------
    dict
        V-tail sizing results
    """
    # Wing geometry
    wing = get_wing_geometry()
    S_wing = wing['wing_area_m2']
    b_wing = wing['wingspan_m']
    mac = wing['chord_m']

    # Fuselage geometry
    fus = get_fuselage_geometry()
    L_fus = fus['length_m']

    # Tail parameters from configuration
    V_H = get_param('geometry.tail.v_h')
    V_V = get_param('geometry.tail.v_v')
    gamma_deg = get_param('geometry.tail.vtail_dihedral_deg')
    AR_tail = get_param('geometry.tail.vtail_aspect_ratio')
    arm_ratio = get_param('geometry.tail.moment_arm_ratio')

    # Moment arms (from tail to wing AC)
    # Assumed equal for horizontal and vertical
    l_tail = arm_ratio * L_fus

    # Required horizontal tail area
    S_H_required = (V_H * S_wing * mac) / l_tail

    # Required vertical tail area
    S_V_required = (V_V * S_wing * b_wing) / l_tail

    # V-tail dihedral
    gamma_rad = math.radians(gamma_deg)
    cos_gamma = math.cos(gamma_rad)
    sin_gamma = math.sin(gamma_rad)

    # V-tail effective areas
    # S_H_eff = S_Vtail × cos^2(Gamma)
    # S_V_eff = S_Vtail × sin^2(Gamma)
    # Solve for S_Vtail from both constraints, take max
    S_vtail_from_H = S_H_required / (cos_gamma ** 2)
    S_vtail_from_V = S_V_required / (sin_gamma ** 2)
    S_vtail_total = max(S_vtail_from_H, S_vtail_from_V)

    # Per-surface area (2 surfaces)
    S_vtail_per_surface = S_vtail_total / 2

    # V-tail geometry from aspect ratio
    b_vtail = math.sqrt(AR_tail * S_vtail_total)  # Total projected span
    b_vtail_per_surface = b_vtail / 2  # Per surface (from centerline)
    c_vtail = S_vtail_total / b_vtail  # Mean chord

    # Actual effective areas achieved
    S_H_actual = S_vtail_total * (cos_gamma ** 2)
    S_V_actual = S_vtail_total * (sin_gamma ** 2)

    # Verification
    V_H_actual = (S_H_actual * l_tail) / (S_wing * mac)
    V_V_actual = (S_V_actual * l_tail) / (S_wing * b_wing)

    # Check which constraint is active
    if S_vtail_from_H >= S_vtail_from_V:
        active_constraint = 'horizontal (pitch)'
    else:
        active_constraint = 'vertical (yaw)'

    return {
        # Wing reference
        'wing_area_m2': S_wing,
        'wingspan_m': b_wing,
        'mac_m': mac,

        # Fuselage reference
        'fuselage_length_m': L_fus,

        # Configuration
        'moment_arm_m': l_tail,
        'moment_arm_ratio': arm_ratio,
        'dihedral_deg': gamma_deg,
        'aspect_ratio': AR_tail,

        # Volume coefficients (target)
        'V_H_target': V_H,
        'V_V_target': V_V,

        # Required areas
        'S_H_required_m2': S_H_required,
        'S_V_required_m2': S_V_required,

        # V-tail sizing
        'S_vtail_total_m2': S_vtail_total,
        'S_vtail_per_surface_m2': S_vtail_per_surface,
        'b_vtail_m': b_vtail,
        'b_vtail_per_surface_m': b_vtail_per_surface,
        'c_vtail_m': c_vtail,

        # Actual effective areas
        'S_H_actual_m2': S_H_actual,
        'S_V_actual_m2': S_V_actual,

        # Verification
        'V_H_actual': V_H_actual,
        'V_V_actual': V_V_actual,
        'active_constraint': active_constraint,
    }


def print_analysis(results: Dict[str, Any] = None) -> None:
    """Print formatted tail sizing results."""
    if results is None:
        results = vtail_sizing()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 70)
    print("TAIL SIZING ANALYSIS (Section 6.3)")
    print("=" * 70)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()

    print("WING REFERENCE GEOMETRY")
    print("-" * 50)
    print(f"  Wing area:             {results['wing_area_m2']:.3f} m2")
    print(f"  Wingspan:              {results['wingspan_m']:.2f} m")
    print(f"  Mean chord:            {results['mac_m']:.3f} m")
    print()

    print("FUSELAGE REFERENCE")
    print("-" * 50)
    print(f"  Fuselage length:       {results['fuselage_length_m']:.2f} m")
    print(f"  Tail moment arm:       {results['moment_arm_m']:.2f} m")
    print(f"  Arm/length ratio:      {results['moment_arm_ratio']:.2f}")
    print()

    print("VOLUME COEFFICIENTS")
    print("-" * 50)
    print(f"  V_H (target):          {results['V_H_target']:.3f}")
    print(f"  V_V (target):          {results['V_V_target']:.4f}")
    print(f"  V_H (actual):          {results['V_H_actual']:.3f}")
    print(f"  V_V (actual):          {results['V_V_actual']:.4f}")
    print()

    print("V-TAIL GEOMETRY")
    print("-" * 50)
    print(f"  Dihedral angle:        {results['dihedral_deg']:.0f}°")
    print(f"  Aspect ratio:          {results['aspect_ratio']:.1f}")
    print(f"  Total planform area:   {results['S_vtail_total_m2']:.3f} m2")
    print(f"  Per-surface area:      {results['S_vtail_per_surface_m2']:.3f} m2")
    print(f"  Total span:            {results['b_vtail_m']:.2f} m")
    print(f"  Per-surface semi-span: {results['b_vtail_per_surface_m']:.2f} m")
    print(f"  Mean chord:            {results['c_vtail_m']:.3f} m")
    print()

    print("SIZING SUMMARY")
    print("-" * 50)
    print(f"  Active constraint:     {results['active_constraint']}")
    print(f"  S_H required:          {results['S_H_required_m2']:.3f} m2")
    print(f"  S_V required:          {results['S_V_required_m2']:.3f} m2")
    print(f"  S_H provided:          {results['S_H_actual_m2']:.3f} m2")
    print(f"  S_V provided:          {results['S_V_actual_m2']:.3f} m2")
    print()

    # Tail fraction
    S_ratio = results['S_vtail_total_m2'] / results['wing_area_m2']
    print(f"  S_tail / S_wing:       {S_ratio:.2%}")
    print()

    print("=" * 70)


if __name__ == "__main__":
    print_analysis()
