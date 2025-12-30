"""
Section 5: Constraint Analysis
==============================

This package implements the constraint analysis calculations from manuscript
Section 5 (Constraint Analysis).

Modules:
    - rotorcraft: Pure rotorcraft (§5.1)
    - fixed_wing: Pure fixed-wing (§5.2) 
    - hybrid_vtol: Hybrid VTOL / QuadPlane (§5.3)
    - matching_chart: Constraint diagram (§5.4)
    - comparative: Configuration comparison (§5.4)

All modules load parameters from config/ YAML files - no hardcoded values.
"""

from . import rotorcraft
from . import fixed_wing
from . import hybrid_vtol
from . import matching_chart
from . import comparative

__all__ = [
    'rotorcraft',
    'fixed_wing', 
    'hybrid_vtol',
    'matching_chart',
    'comparative',
]
