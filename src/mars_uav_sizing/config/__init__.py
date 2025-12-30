"""
Configuration Module
====================

Provides centralized configuration loading for Mars UAV sizing.
All numerical parameters are loaded from YAML files, organized by manuscript section.

Configuration Files:
    - physical_constants.yaml      # Universal constants (from §3)
    - mars_environment.yaml        # Mars-specific environment (from §3)
    - propulsion_parameters.yaml   # Efficiencies (from §4.5)
    - battery_parameters.yaml      # Energy storage (from §4.6)
    - aerodynamic_parameters.yaml  # Drag polar, CL_max (from §4.7)
    - geometry_parameters.yaml     # Disk loading, AR, etc (from §4.12)
    - mission_parameters.yaml      # Velocities, times (from §4.12)

Usage:
    from mars_uav_sizing.config import load_config, get_param
    
    config = load_config()
    g_mars = get_param('physical.mars.g')
    rho = get_param('environment.arcadia_planitia.density_kg_m3')
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional

# Configuration directory
CONFIG_DIR = Path(__file__).parent

# Cache for loaded configurations
_config_cache: Dict[str, Any] = {}

# List of all configuration files
CONFIG_FILES = {
    'physical': 'physical_constants.yaml',
    'environment': 'mars_environment.yaml',
    'propulsion': 'propulsion_parameters.yaml',
    'battery': 'battery_parameters.yaml',
    'aerodynamic': 'aerodynamic_parameters.yaml',
    'geometry': 'geometry_parameters.yaml',
    'mission': 'mission_parameters.yaml',
}


def _load_yaml(filename: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    filepath = CONFIG_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_config(reload: bool = False) -> Dict[str, Any]:
    """
    Load all configuration files into a unified dictionary.
    
    Parameters
    ----------
    reload : bool
        If True, reload from files even if cached
        
    Returns
    -------
    dict
        Complete configuration dictionary with keys:
        - physical: Physical constants
        - environment: Mars environment
        - propulsion: Propulsion efficiencies
        - battery: Battery parameters
        - aerodynamic: Aerodynamic parameters
        - geometry: Geometry parameters
        - mission: Mission parameters
    """
    global _config_cache
    
    if _config_cache and not reload:
        return _config_cache
    
    # Load all config files
    _config_cache = {}
    for key, filename in CONFIG_FILES.items():
        try:
            _config_cache[key] = _load_yaml(filename)
        except FileNotFoundError:
            print(f"Warning: Config file {filename} not found, skipping...")
            _config_cache[key] = {}
    
    return _config_cache


def get_param(path: str, default: Any = None) -> Any:
    """
    Get a parameter value using dot notation path.
    
    Parameters
    ----------
    path : str
        Dot-separated path to parameter
    default : Any
        Default value if path not found
        
    Returns
    -------
    Any
        Parameter value
        
    Examples
    --------
    >>> get_param('physical.mars.g')
    3.711
    >>> get_param('propulsion.electromechanical.eta_motor')
    0.85
    >>> get_param('mission.mass.mtow_kg')
    10.0
    """
    config = load_config()
    
    keys = path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        if default is not None:
            return default
        raise KeyError(f"Configuration path not found: {path}")


# =============================================================================
# Convenience functions for commonly used parameters
# =============================================================================

def get_mars_gravity() -> float:
    """Get Mars surface gravity (m/s²)."""
    return get_param('physical.mars.g')


def get_density() -> float:
    """Get atmospheric density at Arcadia Planitia (kg/m³)."""
    return get_param('environment.arcadia_planitia.density_kg_m3')


def get_mtow() -> float:
    """Get baseline MTOW (kg)."""
    return get_param('mission.mass.mtow_kg')


def get_propulsion_efficiencies() -> Dict[str, float]:
    """Get all propulsion efficiency values."""
    rotor = get_param('propulsion.rotor')
    elec = get_param('propulsion.electromechanical')
    return {
        'figure_of_merit': rotor['figure_of_merit'],
        'eta_motor': elec['eta_motor'],
        'eta_esc': elec['eta_esc'],
        'eta_prop': elec['eta_prop'],
    }


def get_battery_params() -> Dict[str, float]:
    """Get battery parameters."""
    spec = get_param('battery.specifications')
    util = get_param('battery.utilization')
    return {
        'e_spec_Wh_kg': spec['specific_energy_Wh_kg'],
        'dod': util['depth_of_discharge'],
        'eta_discharge': util['discharge_efficiency'],
    }


def get_aerodynamic_params() -> Dict[str, float]:
    """Get aerodynamic parameters."""
    wing = get_param('aerodynamic.wing')
    polar = get_param('aerodynamic.drag_polar')
    airfoil = get_param('aerodynamic.airfoil')
    rotor = get_param('aerodynamic.rotorcraft')
    return {
        'aspect_ratio': wing['aspect_ratio'],
        'oswald_e': wing['oswald_efficiency'],
        'cd0': polar['cd0'],
        'cl_max': airfoil['cl_max'],
        'ld_eff_rotorcraft': rotor['ld_effective'],
    }


def get_mission_params() -> Dict[str, float]:
    """Get mission parameters."""
    vel = get_param('mission.velocity')
    time = get_param('mission.time')
    energy = get_param('mission.energy')
    mass_frac = get_param('mission.mass_fractions')
    return {
        'v_cruise': vel['v_cruise_m_s'],
        'v_stall': vel['v_stall_m_s'],
        't_hover_s': time['t_hover_s'],
        't_cruise_min': time['t_cruise_min'],
        'energy_reserve': energy['reserve_fraction'],
        'f_batt': mass_frac['f_battery'],
    }


def get_geometry_params() -> Dict[str, float]:
    """Get geometry parameters."""
    rotor = get_param('geometry.rotor')
    wing = get_param('geometry.wing')
    return {
        'disk_loading': rotor['disk_loading_N_m2'],
        'taper_ratio': wing['taper_ratio'],
        'thickness_ratio': wing['thickness_ratio'],
    }


def print_config_summary():
    """Print a summary of all loaded configuration."""
    config = load_config()
    
    print("=" * 70)
    print("MARS UAV CONFIGURATION SUMMARY")
    print("=" * 70)
    
    print("\n[PHYSICAL CONSTANTS]")
    print(f"  Mars gravity:       {get_mars_gravity():.3f} m/s²")
    
    print("\n[ENVIRONMENT - Arcadia Planitia]")
    print(f"  Density:            {get_density():.4f} kg/m³")
    
    print("\n[PROPULSION - §4.5]")
    prop = get_propulsion_efficiencies()
    for k, v in prop.items():
        print(f"  {k}: {v}")
    
    print("\n[BATTERY - §4.6]")
    batt = get_battery_params()
    for k, v in batt.items():
        print(f"  {k}: {v}")
    
    print("\n[AERODYNAMICS - §4.7]")
    aero = get_aerodynamic_params()
    for k, v in aero.items():
        print(f"  {k}: {v}")
    
    print("\n[MISSION - §4.12]")
    mission = get_mission_params()
    for k, v in mission.items():
        print(f"  {k}: {v}")
    print(f"  MTOW: {get_mtow()} kg")
    
    print("\n[GEOMETRY - §4.12]")
    geom = get_geometry_params()
    for k, v in geom.items():
        print(f"  {k}: {v}")
    
    print("=" * 70)


# Print config summary when module loaded directly
if __name__ == "__main__":
    print_config_summary()
