"""
Section 6: Design Decisions
============================

This package implements the design decision analysis from manuscript
Section 6 (Design Decisions).

Modules:
    - airfoil_selection: Airfoil comparison and selection (§6.2)
    - airfoil_plots: Visualization of airfoil performance (§6.2)
    - propeller_sizing: Propeller sizing for lift and cruise (§6.3)
    - tail_sizing: Tail surface sizing (§6.3)

All modules load parameters from config/ YAML files - no hardcoded values.
"""

from . import airfoil_selection
from . import airfoil_plots
from . import propeller_sizing
from . import tail_sizing

__all__ = [
    'airfoil_selection',
    'airfoil_plots',
    'propeller_sizing',
    'tail_sizing',
]
