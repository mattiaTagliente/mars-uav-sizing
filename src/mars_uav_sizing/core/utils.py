"""
Utility Functions
=================

Common utility functions for Mars UAV sizing calculations.

Last Updated: 2025-12-29
"""

import math
from typing import Tuple

from ..config import get_param


def kg_to_weight_mars(mass_kg: float) -> float:
    """
    Convert mass (kg) to weight (N) on Mars.
    
    W = m × g_Mars
    
    Parameters
    ----------
    mass_kg : float
        Mass in kilograms
        
    Returns
    -------
    float
        Weight in Newtons
    """
    g_mars = get_param('physical.mars.g')
    return mass_kg * g_mars


def weight_to_kg_mars(weight_n: float) -> float:
    """
    Convert weight (N) to mass (kg) on Mars.
    
    m = W / g_Mars
    
    Parameters
    ----------
    weight_n : float
        Weight in Newtons
        
    Returns
    -------
    float
        Mass in kilograms
    """
    g_mars = get_param('physical.mars.g')
    return weight_n / g_mars


def wing_geometry(wing_area: float, aspect_ratio: float) -> Tuple[float, float]:
    """
    Calculate wingspan and chord from wing area and aspect ratio.
    
    b = sqrt(AR × S)
    c = S / b
    
    Parameters
    ----------
    wing_area : float
        Wing planform area in m²
    aspect_ratio : float
        Wing aspect ratio AR = b²/S
        
    Returns
    -------
    tuple
        (wingspan in m, mean chord in m)
    """
    wingspan = math.sqrt(aspect_ratio * wing_area)
    chord = wing_area / wingspan
    return wingspan, chord


def disk_area_from_loading(weight_n: float, disk_loading: float = None) -> float:
    """
    Calculate rotor disk area from weight and disk loading.
    
    A = W / DL
    
    Parameters
    ----------
    weight_n : float
        Aircraft weight in Newtons
    disk_loading : float, optional
        Disk loading in N/m² (default: from config)
        
    Returns
    -------
    float
        Total disk area in m²
    """
    if disk_loading is None:
        disk_loading = get_param('geometry.rotor.disk_loading_N_m2')
    return weight_n / disk_loading


def efficiency_hover() -> float:
    """
    Calculate combined hover efficiency.
    
    η_hover = FM × η_motor × η_ESC
    
    Returns
    -------
    float
        Combined hover efficiency (dimensionless)
    """
    fm = get_param('propulsion.rotor.figure_of_merit')
    eta_m = get_param('propulsion.electromechanical.eta_motor')
    eta_e = get_param('propulsion.electromechanical.eta_esc')
    return fm * eta_m * eta_e


def efficiency_cruise() -> float:
    """
    Calculate combined cruise efficiency.
    
    η_cruise = η_prop × η_motor × η_ESC
    
    Returns
    -------
    float
        Combined cruise efficiency (dimensionless)
    """
    eta_p = get_param('propulsion.electromechanical.eta_prop')
    eta_m = get_param('propulsion.electromechanical.eta_motor')
    eta_e = get_param('propulsion.electromechanical.eta_esc')
    return eta_p * eta_m * eta_e


def usable_battery_energy(mtow_kg: float = None) -> float:
    """
    Calculate usable battery energy accounting for DoD and efficiency.
    
    E_usable = f_batt × MTOW × e_spec × DoD × η_batt
    
    Parameters
    ----------
    mtow_kg : float, optional
        Maximum takeoff weight (default: from config)
        
    Returns
    -------
    float
        Usable energy in Wh
    """
    if mtow_kg is None:
        mtow_kg = get_param('mission.mass.mtow_kg')
    
    f_batt = get_param('mission.mass_fractions.f_battery')
    e_spec = get_param('battery.specifications.specific_energy_Wh_kg')
    dod = get_param('battery.utilization.depth_of_discharge')
    eta_batt = get_param('battery.utilization.discharge_efficiency')
    
    return f_batt * mtow_kg * e_spec * dod * eta_batt


def format_value(value: float, unit: str, decimals: int = 2) -> str:
    """
    Format a numerical value with unit for display.
    
    Parameters
    ----------
    value : float
        Numerical value
    unit : str
        Unit string
    decimals : int
        Number of decimal places
        
    Returns
    -------
    str
        Formatted string
    """
    return f"{value:.{decimals}f} {unit}"


def print_parameter_table(title: str, params: dict, width: int = 50):
    """
    Print a formatted table of parameters.
    
    Parameters
    ----------
    title : str
        Table title
    params : dict
        Dictionary of parameter names and values
    width : int
        Table width in characters
    """
    print("-" * width)
    print(f"{title}")
    print("-" * width)
    for name, value in params.items():
        if isinstance(value, float):
            print(f"  {name:<30} {value:>15.4g}")
        else:
            print(f"  {name:<30} {str(value):>15}")
    print("-" * width)
