#!/usr/bin/env python3
"""
Section 8: Infrastructure Requirements
=======================================

This module calculates all infrastructure parameters for the Mars UAV
habitat hangar and ground support equipment.

Submodules:
- solar_power: Solar power system sizing for charging infrastructure
- hangar: Hangar zone dimensions and specifications

Reference: Manuscript Section 8 - Infrastructure Requirements
Last Updated: 2026-01-02
"""

from .solar_power import (
    get_solar_irradiance_params,
    get_solar_panel_sizing,
    get_buffer_battery_sizing,
    get_charging_infrastructure,
    get_solar_system_specs,
    print_solar_power_analysis,
)

__all__ = [
    'get_solar_irradiance_params',
    'get_solar_panel_sizing', 
    'get_buffer_battery_sizing',
    'get_charging_infrastructure',
    'get_solar_system_specs',
    'print_solar_power_analysis',
]
