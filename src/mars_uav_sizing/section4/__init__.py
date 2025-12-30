"""
Section 4: Reference Data
==========================

Calculations for manuscript Section 4 (Reference Data).

Modules:
    - derived_requirements: Velocity, Reynolds, wing loading limits (§4.12)
    - aerodynamic_calculations: Drag polar, L/D calculations (§4.7)

Reference: sections_en/04_*.md
"""

from . import derived_requirements
from . import aerodynamic_calculations
from . import geometry_calculations

__all__ = ['derived_requirements', 'aerodynamic_calculations', 'geometry_calculations']
