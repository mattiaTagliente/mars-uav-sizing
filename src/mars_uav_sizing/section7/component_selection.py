#!/usr/bin/env python3
"""
Component Selection Module
==========================

Implements component trade-off analysis and selection for the Mars UAV.
Generates the comparison tables and selection rationale for Section 7.

All values are loaded from YAML configuration files.

Reference: Manuscript Section 7 - Component Selection and Verification
Last Updated: 2025-12-31
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..config import get_param


@dataclass
class MotorCandidate:
    """Motor candidate for comparison."""
    model: str
    manufacturer: str
    mass_g: float
    power_w: float
    kv: int
    lipo: str
    prop_size: str
    thrust_g: Optional[float] = None
    source_key: Optional[str] = None


@dataclass
class ESCCandidate:
    """ESC candidate for comparison."""
    model: str
    manufacturer: str
    mass_g: float
    continuous_a: int
    burst_a: int
    lipo: str
    has_bec: bool = False
    source_key: Optional[str] = None


# =============================================================================
# MOTOR CANDIDATES DATABASE
# =============================================================================

LIFT_MOTOR_CANDIDATES: List[MotorCandidate] = [
    MotorCandidate(
        model="V4006-380",
        manufacturer="SunnySky",
        mass_g=66,
        power_w=375,
        kv=380,
        lipo="4-6S",
        prop_size="12-15",
        thrust_g=2560,
        source_key="sunnyskySunnySkyV4006Multicopter2024",
    ),
    MotorCandidate(
        model="4008 EEE-380",
        manufacturer="MAD",
        mass_g=88,
        power_w=400,
        kv=380,
        lipo="4-6S",
        prop_size="14-18",
        thrust_g=2700,
        source_key="madcomponentsMAD4008EEE2024",
    ),
    MotorCandidate(
        model="MN5008-400",
        manufacturer="T-Motor",
        mass_g=135,
        power_w=800,
        kv=400,
        lipo="6S",
        prop_size="15-17",
        thrust_g=4200,
        source_key="t-motorTMotorMN5008Antigravity2024",
    ),
    MotorCandidate(
        model="MN505-S-260",
        manufacturer="T-Motor",
        mass_g=225,
        power_w=2500,
        kv=260,
        lipo="12S",
        prop_size="16-17",
        thrust_g=None,
        source_key="t-motorMN505SKV260Brushless2024",
    ),
]

CRUISE_MOTOR_CANDIDATES: List[MotorCandidate] = [
    MotorCandidate(
        model="AT2312-1150",
        manufacturer="T-Motor",
        mass_g=60,
        power_w=350,
        kv=1150,
        lipo="2-4S",
        prop_size="10-12",
        source_key="t-motorTMotorAT2312FixedWing2024",
    ),
    MotorCandidate(
        model="AT2814-1000",
        manufacturer="T-Motor",
        mass_g=109,
        power_w=370,
        kv=1000,
        lipo="2-4S",
        prop_size="11-13",
        source_key=None,
    ),
    MotorCandidate(
        model="AT4130-230",
        manufacturer="T-Motor",
        mass_g=408,
        power_w=2500,
        kv=230,
        lipo="12S",
        prop_size="15-18",
        source_key=None,
    ),
]

ESC_CANDIDATES: List[ESCCandidate] = [
    ESCCandidate(
        model="XRotor Micro 30A",
        manufacturer="Hobbywing",
        mass_g=6,
        continuous_a=30,
        burst_a=40,
        lipo="2-4S",
        has_bec=False,
        source_key="hobbywingHobbywingXRotorMicro2024",
    ),
    ESCCandidate(
        model="F35A",
        manufacturer="T-Motor",
        mass_g=7,
        continuous_a=35,
        burst_a=45,
        lipo="3-6S",
        has_bec=False,
        source_key=None,
    ),
    ESCCandidate(
        model="FLAME 60A 12S",
        manufacturer="T-Motor",
        mass_g=74,
        continuous_a=60,
        burst_a=80,
        lipo="12S",
        has_bec=False,
        source_key="t-motorFLAME60A12S2024",
    ),
]


def get_power_requirements() -> Dict[str, float]:
    """
    Get power requirements from Section 5 analysis.
    
    Returns
    -------
    dict
        Power requirements for lift and cruise motors.
    """
    # Import here to avoid circular dependency
    from ..section5 import hybrid_vtol
    
    hover_power = hybrid_vtol.quadplane_hover_power()
    cruise_power = hybrid_vtol.quadplane_cruise_power()
    
    n_lift = get_param('propulsion.components.lift.motor.quantity')
    n_cruise = get_param('propulsion.components.cruise.motor.quantity')
    
    return {
        'hover_total_w': hover_power,
        'per_lift_motor_w': hover_power / n_lift,
        'cruise_total_w': cruise_power,
        'per_cruise_motor_w': cruise_power / n_cruise,
        'n_lift_motors': n_lift,
        'n_cruise_motors': n_cruise,
    }


def get_mass_budget() -> Dict[str, float]:
    """
    Get mass budget constraints from mission parameters.
    
    Returns
    -------
    dict
        Mass budget allocation for propulsion components.
    """
    mtow = get_param('mission.mass.mtow_kg')
    f_prop = get_param('mission.mass_fractions.f_propulsion')
    
    # Propulsion mass budget
    m_propulsion = f_prop * mtow
    
    # 70:30 split between lift and cruise
    lift_fraction = 0.70
    cruise_fraction = 0.30
    
    m_lift = lift_fraction * m_propulsion
    m_cruise = cruise_fraction * m_propulsion
    
    # Component count
    n_lift_motors = get_param('propulsion.components.lift.motor.quantity')
    n_cruise_motors = get_param('propulsion.components.cruise.motor.quantity')
    
    return {
        'mtow_kg': mtow,
        'f_propulsion': f_prop,
        'm_propulsion_kg': m_propulsion,
        'm_lift_kg': m_lift,
        'm_cruise_kg': m_cruise,
        'target_lift_motor_g': (m_lift * 1000) / n_lift_motors * 0.5,  # 50% for motors
        'target_cruise_motor_g': (m_cruise * 1000) / n_cruise_motors * 0.5,
        'n_lift_motors': n_lift_motors,
        'n_cruise_motors': n_cruise_motors,
    }


def evaluate_motor_candidates(
    candidates: List[MotorCandidate],
    min_power_w: float,
    max_mass_g: float,
) -> List[Dict[str, Any]]:
    """
    Evaluate motor candidates against requirements.
    
    Parameters
    ----------
    candidates : list
        List of MotorCandidate objects.
    min_power_w : float
        Minimum required power (W).
    max_mass_g : float
        Maximum allowed mass (g).
    
    Returns
    -------
    list
        Evaluation results with status for each candidate.
    """
    results = []
    for motor in candidates:
        power_ok = motor.power_w >= min_power_w
        mass_ok = motor.mass_g <= max_mass_g
        
        if power_ok and mass_ok:
            status = "Suitable"
        elif power_ok and not mass_ok:
            status = "Too heavy"
        elif not power_ok and mass_ok:
            status = "Insufficient power"
        else:
            status = "Fails both"
        
        results.append({
            'model': f"{motor.manufacturer} {motor.model}",
            'mass_g': motor.mass_g,
            'power_w': motor.power_w,
            'kv': motor.kv,
            'lipo': motor.lipo,
            'prop_size': motor.prop_size,
            'thrust_g': motor.thrust_g,
            'power_ok': power_ok,
            'mass_ok': mass_ok,
            'status': status,
            'source_key': motor.source_key,
        })
    
    return results


def get_selected_components() -> Dict[str, Any]:
    """
    Get the selected component specifications from configuration.
    
    Returns
    -------
    dict
        Selected component specifications.
    """
    return {
        'lift_motor': {
            'model': get_param('propulsion.components.lift.motor.model'),
            'mass_kg': get_param('propulsion.components.lift.motor.mass_kg'),
            'quantity': get_param('propulsion.components.lift.motor.quantity'),
            'max_power_w': get_param('propulsion.components.lift.motor.max_power_w'),
        },
        'lift_esc': {
            'model': get_param('propulsion.components.lift.esc.model'),
            'mass_kg': get_param('propulsion.components.lift.esc.mass_kg'),
            'quantity': get_param('propulsion.components.lift.esc.quantity'),
        },
        'lift_propeller': {
            'model': get_param('propulsion.components.lift.propeller.model'),
            'mass_kg': get_param('propulsion.components.lift.propeller.mass_kg'),
            'quantity': get_param('propulsion.components.lift.propeller.quantity'),
        },
        'cruise_motor': {
            'model': get_param('propulsion.components.cruise.motor.model'),
            'mass_kg': get_param('propulsion.components.cruise.motor.mass_kg'),
            'quantity': get_param('propulsion.components.cruise.motor.quantity'),
            'max_power_w': get_param('propulsion.components.cruise.motor.max_power_w'),
        },
        'cruise_esc': {
            'model': get_param('propulsion.components.cruise.esc.model'),
            'mass_kg': get_param('propulsion.components.cruise.esc.mass_kg'),
            'quantity': get_param('propulsion.components.cruise.esc.quantity'),
        },
        'cruise_propeller': {
            'model': get_param('propulsion.components.cruise.propeller.model'),
            'mass_kg': get_param('propulsion.components.cruise.propeller.mass_kg'),
            'quantity': get_param('propulsion.components.cruise.propeller.quantity'),
        },
    }


def print_component_selection():
    """Print component selection analysis."""
    print("=" * 70)
    print("COMPONENT SELECTION ANALYSIS (Section 7)")
    print("=" * 70)
    print(f"Computed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Config:   All values loaded from config/ YAML files")
    
    # Power requirements
    power_req = get_power_requirements()
    print("\nPOWER REQUIREMENTS (from Section 5)")
    print("-" * 50)
    print(f"  Total hover power:      {power_req['hover_total_w']:.0f} W")
    print(f"  Per lift motor ({power_req['n_lift_motors']:.0f}):    {power_req['per_lift_motor_w']:.0f} W")
    print(f"  Total cruise power:     {power_req['cruise_total_w']:.0f} W")
    print(f"  Per cruise motor ({power_req['n_cruise_motors']:.0f}):   {power_req['per_cruise_motor_w']:.0f} W")
    
    # Mass budget
    mass_budget = get_mass_budget()
    print("\nMASS BUDGET")
    print("-" * 50)
    print(f"  MTOW:                   {mass_budget['mtow_kg']:.2f} kg")
    print(f"  f_propulsion:           {mass_budget['f_propulsion']:.2f}")
    print(f"  Propulsion budget:      {mass_budget['m_propulsion_kg']:.3f} kg")
    print(f"  Lift system (70%):      {mass_budget['m_lift_kg']:.3f} kg")
    print(f"  Cruise system (30%):    {mass_budget['m_cruise_kg']:.3f} kg")
    
    # Lift motor evaluation
    print("\nLIFT MOTOR CANDIDATES")
    print("-" * 70)
    print(f"{'Model':<25} {'Mass':<8} {'Power':<8} {'KV':<6} {'Status':<15}")
    print("-" * 70)
    
    lift_results = evaluate_motor_candidates(
        LIFT_MOTOR_CANDIDATES,
        min_power_w=power_req['per_lift_motor_w'],
        max_mass_g=100,  # Target
    )
    
    for r in lift_results:
        status_mark = "[OK]" if r['status'] == "Suitable" else "[X]"
        print(f"{r['model']:<25} {r['mass_g']:<8.0f} {r['power_w']:<8.0f} {r['kv']:<6} {status_mark} {r['status']}")
    
    # Cruise motor evaluation
    print("\nCRUISE MOTOR CANDIDATES")
    print("-" * 70)
    print(f"{'Model':<25} {'Mass':<8} {'Power':<8} {'KV':<6} {'Status':<15}")
    print("-" * 70)
    
    cruise_results = evaluate_motor_candidates(
        CRUISE_MOTOR_CANDIDATES,
        min_power_w=power_req['per_cruise_motor_w'],
        max_mass_g=100,  # Target
    )
    
    for r in cruise_results:
        status_mark = "[OK]" if r['status'] == "Suitable" else "[X]"
        print(f"{r['model']:<25} {r['mass_g']:<8.0f} {r['power_w']:<8.0f} {r['kv']:<6} {status_mark} {r['status']}")
    
    # Selected components
    selected = get_selected_components()
    print("\nSELECTED COMPONENTS")
    print("-" * 50)
    print(f"  Lift motor:     {selected['lift_motor']['model']}")
    print(f"  Lift ESC:       {selected['lift_esc']['model']}")
    print(f"  Cruise motor:   {selected['cruise_motor']['model']}")
    print(f"  Cruise ESC:     {selected['cruise_esc']['model']}")
    
    # Get mass breakdown
    from . import mass_breakdown
    breakdown = mass_breakdown.get_propulsion_mass_breakdown()
    
    print("\nPROPULSION MASS SUMMARY")
    print("-" * 50)
    print(f"  Lift system:     {breakdown['lift']['subtotal_kg']:.3f} kg")
    print(f"  Cruise system:   {breakdown['cruise']['subtotal_kg']:.3f} kg")
    print(f"  Total:           {breakdown['total_kg']:.3f} kg")
    print(f"  Budget:          {mass_budget['m_propulsion_kg']:.3f} kg")
    margin = mass_budget['m_propulsion_kg'] - breakdown['total_kg']
    margin_pct = 100 * margin / mass_budget['m_propulsion_kg']
    print(f"  Margin:          {margin:+.3f} kg ({margin_pct:+.1f}%)")
    
    if margin > 0:
        print("\n  [PASS] Mass budget SATISFIED")
    else:
        print("\n  [FAIL] Mass budget EXCEEDED")
    
    print("=" * 70)


if __name__ == "__main__":
    print_component_selection()
