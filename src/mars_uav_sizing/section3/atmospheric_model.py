"""
Atmospheric Model Calculations
===============================

Implements atmospheric calculations from manuscript Section 3.1.

Equations:
    @eq:barometric-formula  - Pressure vs altitude
    @eq:ideal-gas           - Density from P and T
    @eq:sutherland          - Dynamic viscosity
    @eq:speed-of-sound      - Speed of sound
    @eq:reynolds            - Reynolds number

Reference: 
    - Manuscript: sections_en/03_01_arcadia-planitia.md
    - NASA GRC Mars Atmosphere Model

Last Updated: 2025-12-29
"""

import math
from datetime import datetime
from typing import Dict, Any

from ..config import get_param


def barometric_pressure(altitude_km: float) -> float:
    """
    Calculate atmospheric pressure using polytropic barometric formula.
    
    Implements @eq:pressure from §3.1 (lapse-rate power law):
        P = P_0 × (T(h)/T_0)^(g/(R×L))
    
    This is the polytropic atmosphere model which correctly accounts for
    the temperature lapse rate, unlike the isothermal model which assumes
    constant temperature.
    
    Parameters
    ----------
    altitude_km : float
        Altitude above Mars areoid in km
        
    Returns
    -------
    float
        Pressure in Pa
    """
    P0 = get_param('environment.reference_atmosphere.P_surface')
    g = get_param('physical.mars.g')
    R = get_param('physical.mars_atmosphere_composition.R_specific')
    T0 = get_param('environment.reference_atmosphere.T_surface')
    lapse = get_param('environment.reference_atmosphere.lapse_rate')
    
    # Temperature at altitude (with lapse rate): T(h) = T0 - L×h
    T = T0 - lapse * altitude_km * 1000
    
    # Polytropic barometric formula: P = P0 × (T/T0)^(g/(R×L))
    # Valid for atmosphere with constant lapse rate
    exponent = g / (R * lapse)
    return P0 * (T / T0) ** exponent


def ideal_gas_density(pressure_Pa: float, temperature_K: float) -> float:
    """
    Calculate density from ideal gas law.
    
    Implements @eq:ideal-gas from §3.1:
        ρ = P / (R × T)
    
    Parameters
    ----------
    pressure_Pa : float
        Pressure in Pa
    temperature_K : float
        Temperature in K
        
    Returns
    -------
    float
        Density in kg/m³
    """
    R = get_param('physical.mars_atmosphere_composition.R_specific')
    return pressure_Pa / (R * temperature_K)


def sutherland_viscosity(temperature_K: float) -> float:
    """
    Calculate dynamic viscosity using Sutherland's law.
    
    Implements @eq:sutherland from §3.1:
        μ = μ_ref × (T/T_ref)^1.5 × (T_ref + C) / (T + C)
    
    Parameters
    ----------
    temperature_K : float
        Temperature in K
        
    Returns
    -------
    float
        Dynamic viscosity in Pa·s
    """
    mu_ref = get_param('physical.sutherland.mu_ref')
    T_ref = get_param('physical.sutherland.T_ref')
    C = get_param('physical.sutherland.C')
    
    ratio = (temperature_K / T_ref) ** 1.5
    factor = (T_ref + C) / (temperature_K + C)
    return mu_ref * ratio * factor


def speed_of_sound(temperature_K: float) -> float:
    """
    Calculate speed of sound.
    
    Implements @eq:speed-of-sound from §3.1:
        a = sqrt(γ × R × T)
    
    Parameters
    ----------
    temperature_K : float
        Temperature in K
        
    Returns
    -------
    float
        Speed of sound in m/s
    """
    gamma = get_param('physical.mars_atmosphere_composition.gamma')
    R = get_param('physical.mars_atmosphere_composition.R_specific')
    return math.sqrt(gamma * R * temperature_K)


def reynolds_number(velocity: float, length: float, rho: float, mu: float) -> float:
    """
    Calculate Reynolds number.
    
    Implements @eq:reynolds from §3.1:
        Re = ρ × V × L / μ
    
    Parameters
    ----------
    velocity : float
        Flow velocity in m/s
    length : float
        Characteristic length in m
    rho : float
        Density in kg/m³
    mu : float
        Dynamic viscosity in Pa·s
        
    Returns
    -------
    float
        Reynolds number (dimensionless)
    """
    return rho * velocity * length / mu


def mach_number(velocity: float, temperature_K: float) -> float:
    """
    Calculate Mach number.
    
    Implements M = V / a from §3.1.
    
    Parameters
    ----------
    velocity : float
        Flow velocity in m/s
    temperature_K : float
        Temperature in K
        
    Returns
    -------
    float
        Mach number (dimensionless)
    """
    a = speed_of_sound(temperature_K)
    return velocity / a


def arcadia_planitia_conditions() -> Dict[str, float]:
    """
    Calculate all atmospheric conditions at Arcadia Planitia operating altitude.
    
    The operating altitude is the surface elevation plus the AGL flight altitude,
    both read from configuration.
    
    Returns
    -------
    dict
        Complete atmospheric state at operating altitude
    """
    # Surface elevation and operating AGL from config
    surface_elevation_km = get_param('environment.arcadia_planitia.elevation_km')
    agl_m = get_param('environment.arcadia_planitia.operating_altitude_agl_m')
    
    # Operating altitude = surface + AGL (convert AGL to km)
    operating_altitude_km = surface_elevation_km + (agl_m / 1000.0)
    
    T0 = get_param('environment.reference_atmosphere.T_surface')
    lapse = get_param('environment.reference_atmosphere.lapse_rate')
    
    # Temperature at operating altitude (below datum, so warmer)
    T = T0 - lapse * operating_altitude_km * 1000
    
    # Pressure
    P = barometric_pressure(operating_altitude_km)
    
    # Density
    rho = ideal_gas_density(P, T)
    
    # Viscosity
    mu = sutherland_viscosity(T)
    
    # Speed of sound
    a = speed_of_sound(T)
    
    # Reynolds number at cruise conditions
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    chord = get_param('aerodynamic.wing.mean_chord_m')
    Re = reynolds_number(v_cruise, chord, rho, mu)
    
    # Mach number
    M = mach_number(v_cruise, T)
    
    return {
        'surface_elevation_km': surface_elevation_km,
        'agl_m': agl_m,
        'operating_altitude_km': operating_altitude_km,
        'temperature_K': T,
        'pressure_Pa': P,
        'density_kg_m3': rho,
        'viscosity_Pa_s': mu,
        'speed_of_sound_m_s': a,
        'kinematic_viscosity_m2_s': mu / rho,
        'reynolds_at_cruise': Re,
        'mach_at_cruise': M,
    }


def print_analysis():
    """Print formatted atmospheric analysis."""
    results = arcadia_planitia_conditions()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("ATMOSPHERIC MODEL CALCULATIONS (Section 3.1)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values from config/ YAML files")
    print()
    
    print("REFERENCE CONDITIONS (Mars datum, h = 0 km)")
    print("-" * 50)
    T0 = get_param('environment.reference_atmosphere.T_surface')
    P0 = get_param('environment.reference_atmosphere.P_surface')
    print(f"  Temperature:    {T0:.1f} K")
    print(f"  Pressure:       {P0:.1f} Pa")
    print()
    
    print(f"ARCADIA PLANITIA CONDITIONS (surface = {results['surface_elevation_km']:.1f} km, AGL = {results['agl_m']:.0f} m)")
    print("-" * 50)
    print(f"  Operating alt:  {results['operating_altitude_km']:.2f} km (absolute)")
    print(f"  Temperature:    {results['temperature_K']:.1f} K")
    print(f"  Pressure:       {results['pressure_Pa']:.1f} Pa")
    print(f"  Density:        {results['density_kg_m3']:.5f} kg/m³")
    print(f"  Viscosity:      {results['viscosity_Pa_s']:.3e} Pa·s")
    print(f"  Kin. viscosity: {results['kinematic_viscosity_m2_s']:.3e} m²/s")
    print(f"  Speed of sound: {results['speed_of_sound_m_s']:.1f} m/s")
    print()
    
    v_cruise = get_param('mission.velocity.v_cruise_m_s')
    chord = get_param('aerodynamic.wing.mean_chord_m')
    print(f"CRUISE CONDITIONS (V = {v_cruise:.0f} m/s, c = {chord:.3f} m)")
    print("-" * 50)
    print(f"  Reynolds number:  {results['reynolds_at_cruise']:.0f}")
    print(f"  Mach number:      {results['mach_at_cruise']:.3f}")
    print()
    
    # Compare with config stored values
    config_rho = get_param('environment.arcadia_planitia.density_kg_m3')
    diff = abs(results['density_kg_m3'] - config_rho) / config_rho * 100
    
    print("VERIFICATION")
    print("-" * 50)
    print(f"  Computed rho:   {results['density_kg_m3']:.5f} kg/m³")
    print(f"  Config rho:     {config_rho} kg/m³")
    print(f"  Difference:     {diff:.2f}%")
    
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
