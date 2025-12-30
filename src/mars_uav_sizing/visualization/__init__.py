"""
Visualization Module
====================

Plotting functions for Mars UAV sizing analysis.

Functions:
    - plot_constraint_diagram: Matching chart (P/W vs W/S)
    - plot_weight_breakdown: Mass breakdown pie/bar chart
    - plot_power_budget: Power consumption breakdown
    - plot_mission_profile: Power vs time through mission

Reference: sections_en/05_04_* (§5.4 matching chart)
"""

from . import plotting

__all__ = ['plotting']
