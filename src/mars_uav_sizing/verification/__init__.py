"""
Verification Module
===================

Script verification functions to ensure calculations match manuscript values.

Functions:
    - verify_all: Run all verification tests
    - verify_section3: Verify atmospheric calculations
    - verify_section4: Verify reference data calculations
    - verify_section5: Verify constraint analysis results

Last Updated: 2025-12-29
"""

from . import verify_manuscript

__all__ = ['verify_manuscript']
