#!/usr/bin/env python3
"""
Propulsion Mass Breakdown Calculator
=====================================

Calculates propulsion system masses from component data in config files.
Provides values for both Section 5 (parametric estimates) and Section 7
(detailed component breakdown).

All values are loaded from propulsion_parameters.yaml to ensure
data integrity between configuration and manuscript.

Last Updated: 2025-12-31
"""

from typing import Dict, Any
from ..config import get_param


def get_propulsion_mass_breakdown() -> Dict[str, Any]:
    """
    Calculate complete propulsion mass breakdown from component data.
    
    Returns
    -------
    dict
        Detailed mass breakdown with lift, cruise, shared, and totals.
    """
    # Lift system components (source-grounded)
    lift_motor_mass = get_param('propulsion.components.lift.motor.mass_kg')
    lift_motor_qty = get_param('propulsion.components.lift.motor.quantity')
    lift_esc_mass = get_param('propulsion.components.lift.esc.mass_kg')
    lift_esc_qty = get_param('propulsion.components.lift.esc.quantity')
    lift_prop_mass = get_param('propulsion.components.lift.propeller.mass_kg')
    lift_prop_qty = get_param('propulsion.components.lift.propeller.quantity')
    
    # Cruise system components (source-grounded)
    cruise_motor_mass = get_param('propulsion.components.cruise.motor.mass_kg')
    cruise_motor_qty = get_param('propulsion.components.cruise.motor.quantity')
    cruise_esc_mass = get_param('propulsion.components.cruise.esc.mass_kg')
    cruise_esc_qty = get_param('propulsion.components.cruise.esc.quantity')
    cruise_prop_mass = get_param('propulsion.components.cruise.propeller.mass_kg')
    cruise_prop_qty = get_param('propulsion.components.cruise.propeller.quantity')
    
    # Calculate lift system totals
    lift_motors_total = lift_motor_mass * lift_motor_qty
    lift_escs_total = lift_esc_mass * lift_esc_qty
    lift_props_total = lift_prop_mass * lift_prop_qty
    lift_system_total = lift_motors_total + lift_escs_total + lift_props_total
    
    # Calculate cruise system totals
    cruise_motors_total = cruise_motor_mass * cruise_motor_qty
    cruise_escs_total = cruise_esc_mass * cruise_esc_qty
    cruise_props_total = cruise_prop_mass * cruise_prop_qty
    cruise_system_total = cruise_motors_total + cruise_escs_total + cruise_props_total
    
    # Shared components (engineering estimates - not source-grounded)
    try:
        mounting_mass = get_param('propulsion.components.shared.mounting.mass_kg')
        mounting_qty = get_param('propulsion.components.shared.mounting.quantity')
        mounting_total = mounting_mass * mounting_qty
    except KeyError:
        mounting_total = 0.0
    
    try:
        wiring_mass = get_param('propulsion.components.shared.wiring.mass_kg')
        wiring_qty = get_param('propulsion.components.shared.wiring.quantity')
        wiring_total = wiring_mass * wiring_qty
    except KeyError:
        wiring_total = 0.0
    
    shared_total = mounting_total + wiring_total
    
    # Total propulsion mass
    total_propulsion = lift_system_total + cruise_system_total + shared_total
    
    return {
        'lift': {
            'motors': {
                'unit_mass_kg': lift_motor_mass,
                'quantity': lift_motor_qty,
                'total_kg': lift_motors_total,
                'model': get_param('propulsion.components.lift.motor.model'),
            },
            'escs': {
                'unit_mass_kg': lift_esc_mass,
                'quantity': lift_esc_qty,
                'total_kg': lift_escs_total,
                'model': get_param('propulsion.components.lift.esc.model'),
            },
            'propellers': {
                'unit_mass_kg': lift_prop_mass,
                'quantity': lift_prop_qty,
                'total_kg': lift_props_total,
                'model': get_param('propulsion.components.lift.propeller.model'),
            },
            'subtotal_kg': lift_system_total,
        },
        'cruise': {
            'motors': {
                'unit_mass_kg': cruise_motor_mass,
                'quantity': cruise_motor_qty,
                'total_kg': cruise_motors_total,
                'model': get_param('propulsion.components.cruise.motor.model'),
            },
            'escs': {
                'unit_mass_kg': cruise_esc_mass,
                'quantity': cruise_esc_qty,
                'total_kg': cruise_escs_total,
                'model': get_param('propulsion.components.cruise.esc.model'),
            },
            'propellers': {
                'unit_mass_kg': cruise_prop_mass,
                'quantity': cruise_prop_qty,
                'total_kg': cruise_props_total,
                'model': get_param('propulsion.components.cruise.propeller.model'),
            },
            'subtotal_kg': cruise_system_total,
        },
        'shared': {
            'mounting': {
                'total_kg': mounting_total,
            },
            'wiring': {
                'total_kg': wiring_total,
            },
            'subtotal_kg': shared_total,
        },
        'total_kg': total_propulsion,
        'n_lift_motors': lift_motor_qty,
        'n_cruise_motors': cruise_motor_qty,
        'n_total_motors': lift_motor_qty + cruise_motor_qty,
    }


def get_parametric_mass_estimate() -> Dict[str, Any]:
    """
    Get parametric mass estimate for Section 5 feasibility analysis.
    
    Uses mass fractions rather than specific components.
    This is appropriate for the constraint analysis phase.
    
    Returns
    -------
    dict
        Parametric mass estimates based on mass fractions.
    """
    mtow = get_param('mission.mass.mtow_kg')
    f_prop = get_param('mission.mass_fractions.f_propulsion')
    
    # Total propulsion mass from mass fraction
    m_propulsion = f_prop * mtow
    
    # Estimated split between lift and cruise (based on reference data)
    # Octocopter lift system is heavier than quadcopter
    lift_fraction = 0.70  # 70% for lift system
    cruise_fraction = 0.30  # 30% for cruise system
    
    m_lift = lift_fraction * m_propulsion
    m_cruise = cruise_fraction * m_propulsion
    
    return {
        'mtow_kg': mtow,
        'f_propulsion': f_prop,
        'm_propulsion_kg': m_propulsion,
        'lift_fraction': lift_fraction,
        'cruise_fraction': cruise_fraction,
        'm_lift_kg': m_lift,
        'm_cruise_kg': m_cruise,
    }


def print_mass_breakdown():
    """Print propulsion mass breakdown for verification."""
    breakdown = get_propulsion_mass_breakdown()
    parametric = get_parametric_mass_estimate()
    
    print("=" * 70)
    print("PROPULSION MASS BREAKDOWN (Section 7)")
    print("=" * 70)
    
    print("\nLIFT SYSTEM (Octocopter - 4 coaxial pairs)")
    print("-" * 50)
    lift = breakdown['lift']
    print(f"  Motors:     {lift['motors']['quantity']:2d} × {lift['motors']['unit_mass_kg']:.4f} kg = {lift['motors']['total_kg']:.4f} kg")
    print(f"  ESCs:       {lift['escs']['quantity']:2d} × {lift['escs']['unit_mass_kg']:.4f} kg = {lift['escs']['total_kg']:.4f} kg")
    print(f"  Propellers: {lift['propellers']['quantity']:2d} × {lift['propellers']['unit_mass_kg']:.4f} kg = {lift['propellers']['total_kg']:.4f} kg")
    print(f"  Subtotal:   {lift['subtotal_kg']:.4f} kg")
    
    print("\nCRUISE SYSTEM (Coaxial tractor)")
    print("-" * 50)
    cruise = breakdown['cruise']
    print(f"  Motors:     {cruise['motors']['quantity']:2d} × {cruise['motors']['unit_mass_kg']:.4f} kg = {cruise['motors']['total_kg']:.4f} kg")
    print(f"  ESCs:       {cruise['escs']['quantity']:2d} × {cruise['escs']['unit_mass_kg']:.4f} kg = {cruise['escs']['total_kg']:.4f} kg")
    print(f"  Propellers: {cruise['propellers']['quantity']:2d} × {cruise['propellers']['unit_mass_kg']:.4f} kg = {cruise['propellers']['total_kg']:.4f} kg")
    print(f"  Subtotal:   {cruise['subtotal_kg']:.4f} kg")
    
    print("\nSHARED (Engineering estimates)")
    print("-" * 50)
    shared = breakdown['shared']
    print(f"  Mounting:   {shared['mounting']['total_kg']:.4f} kg")
    print(f"  Wiring:     {shared['wiring']['total_kg']:.4f} kg")
    print(f"  Subtotal:   {shared['subtotal_kg']:.4f} kg")
    
    print("\nTOTAL PROPULSION")
    print("-" * 50)
    print(f"  Total motors: {breakdown['n_total_motors']} ({breakdown['n_lift_motors']} lift + {breakdown['n_cruise_motors']} cruise)")
    print(f"  Lift system:   {lift['subtotal_kg']:.4f} kg")
    print(f"  Cruise system: {cruise['subtotal_kg']:.4f} kg")
    print(f"  Shared:        {shared['subtotal_kg']:.4f} kg")
    print(f"  Total mass:    {breakdown['total_kg']:.4f} kg")
    
    print("\nPARAMETRIC COMPARISON")
    print("-" * 50)
    print(f"  MTOW:                {parametric['mtow_kg']:.2f} kg")
    print(f"  f_propulsion:        {parametric['f_propulsion']:.2f}")
    print(f"  Parametric estimate: {parametric['m_propulsion_kg']:.4f} kg")
    print(f"  Actual (detailed):   {breakdown['total_kg']:.4f} kg")
    
    diff = breakdown['total_kg'] - parametric['m_propulsion_kg']
    diff_pct = 100 * diff / parametric['m_propulsion_kg']
    print(f"  Difference:          {diff:+.4f} kg ({diff_pct:+.1f}%)")
    
    if diff < 0:
        print(f"\n  [PASS] Mass budget SATISFIED with {-diff:.3f} kg margin")
    else:
        print(f"\n  [FAIL] Mass budget EXCEEDED by {diff:.3f} kg")
        print("      Consider lighter components or revised MTOW.")


if __name__ == "__main__":
    print_mass_breakdown()
