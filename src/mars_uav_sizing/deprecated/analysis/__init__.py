"""
Mars UAV Sizing - Analysis Package
===================================

Implements equations from manuscript Sections 5.2-5.5 for the
Mars UAV feasibility study.

Modules:
- rotorcraft_analysis: Rotorcraft configuration (§5.2)
- fixed_wing_analysis: Fixed-wing configuration (§5.3)
- hybrid_vtol_analysis: Hybrid VTOL / QuadPlane (§5.4)
- comparative_analysis: Configuration comparison (§5.5)
- matching_chart: Constraint-based sizing methodology (§5.5)

Usage:
    from mars_uav_sizing.analysis import rotorcraft_analysis
    results = rotorcraft_analysis.rotorcraft_feasibility_analysis()
    rotorcraft_analysis.print_rotorcraft_analysis(results)
    
    # Or run all analyses:
    from mars_uav_sizing.analysis import comparative_analysis
    summary = comparative_analysis.comparative_summary()
    comparative_analysis.print_comparative_analysis(summary)

Updated 2025-12-28: Parameters aligned with manuscript sections 2, 3, 4.
"""

# Import modules for convenience
from . import rotorcraft_analysis
from . import fixed_wing_analysis
from . import hybrid_vtol_analysis
from . import comparative_analysis
from . import matching_chart
from . import run_all_analyses

# Key functions for direct access
from .rotorcraft_analysis import (
    induced_velocity,
    ideal_hover_power,
    actual_hover_power,
    electric_hover_power,
    hover_power_loading,
    forward_flight_power,
    electric_forward_flight_power,
    rotorcraft_endurance,
    rotorcraft_feasibility_analysis,
    print_rotorcraft_analysis,
)

from .fixed_wing_analysis import (
    cruise_lift_coefficient,
    drag_coefficient,
    induced_drag_factor,
    lift_to_drag,
    maximum_ld,
    cruise_power,
    cruise_power_loading,
    stall_speed,
    stall_wing_loading_limit,
    fixed_wing_endurance,
    takeoff_ground_roll,
    fixed_wing_feasibility_analysis,
    print_fixed_wing_analysis,
)

from .hybrid_vtol_analysis import (
    hybrid_hover_power,
    hybrid_cruise_power,
    energy_budget,
    required_battery_mass,
    available_energy,
    hybrid_vtol_feasibility,
    print_hybrid_vtol_analysis,
)

from .comparative_analysis import (
    run_all_analyses,
    create_comparison_table,
    configuration_ranking,
    elimination_rationale,
    comparative_summary,
    print_comparative_analysis,
)

from .matching_chart import (
    hover_constraint,
    stall_constraint,
    cruise_constraint,
    cruise_constraint_curve,
    minimum_power_point,
    find_design_point,
    matching_chart_analysis,
    print_matching_chart_analysis,
)

__all__ = [
    # Modules
    'rotorcraft_analysis',
    'fixed_wing_analysis',
    'hybrid_vtol_analysis',
    'comparative_analysis',
    'matching_chart',
    
    # Rotorcraft functions
    'induced_velocity',
    'ideal_hover_power',
    'actual_hover_power',
    'electric_hover_power',
    'hover_power_loading',
    'forward_flight_power',
    'electric_forward_flight_power',
    'rotorcraft_endurance',
    'rotorcraft_feasibility_analysis',
    'print_rotorcraft_analysis',
    
    # Fixed-wing functions
    'cruise_lift_coefficient',
    'drag_coefficient',
    'induced_drag_factor',
    'lift_to_drag',
    'maximum_ld',
    'cruise_power',
    'cruise_power_loading',
    'stall_speed',
    'stall_wing_loading_limit',
    'fixed_wing_endurance',
    'takeoff_ground_roll',
    'fixed_wing_feasibility_analysis',
    'print_fixed_wing_analysis',
    
    # Hybrid VTOL functions
    'hybrid_hover_power',
    'hybrid_cruise_power',
    'energy_budget',
    'required_battery_mass',
    'available_energy',
    'hybrid_vtol_feasibility',
    'print_hybrid_vtol_analysis',
    
    # Comparative analysis functions
    'run_all_analyses',
    'create_comparison_table',
    'configuration_ranking',
    'elimination_rationale',
    'comparative_summary',
    'print_comparative_analysis',
    
    # Matching chart functions
    'hover_constraint',
    'stall_constraint',
    'cruise_constraint',
    'cruise_constraint_curve',
    'minimum_power_point',
    'find_design_point',
    'matching_chart_analysis',
    'print_matching_chart_analysis',
]
