"""
Section 7: Component Selection and Verification
================================================

This package implements the component selection calculations from manuscript
Section 7 (Component Selection and Verification).

Modules:
    - component_selection: Component trade-off and selection (§7.1-7.4)
    - mass_breakdown: Propulsion mass breakdown calculator (§7.2)
    - verification: Requirements compliance check (§7.5)

All modules load parameters from config/ YAML files - no hardcoded values.
"""

from . import component_selection
from . import mass_breakdown

__all__ = [
    'component_selection',
    'mass_breakdown',
]
