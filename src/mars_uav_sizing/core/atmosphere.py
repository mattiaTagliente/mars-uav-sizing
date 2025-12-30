"""
Mars Atmospheric Model
======================

Provides atmospheric properties (density, temperature, pressure, viscosity)
as a function of altitude above the Mars areoid (datum).

All base parameters loaded from config/mars_environment.yaml and 
config/physical_constants.yaml.

Reference:
    - Manuscript: sections_en/03_01_arcadia-planitia.md (§3.1)
    - NASA GRC Mars Atmosphere Model

Last Updated: 2025-12-29
"""

import math
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ..config import get_param


@dataclass
class AtmosphericState:
    """Container for atmospheric properties at a given altitude."""
    altitude_km: float
    temperature_K: float
    pressure_Pa: float
    density_kg_m3: float
    viscosity_Pa_s: float
    speed_of_sound_m_s: float
    
    @property
    def kinematic_viscosity(self) -> float:
        """Kinematic viscosity in m²/s."""
        return self.viscosity_Pa_s / self.density_kg_m3


class MarsAtmosphere:
    """
    Mars atmospheric model.
    
    Uses exponential atmosphere model with parameters from configuration.
    """
    
    def __init__(self):
        """Initialize with parameters from configuration."""
        # Physical constants
        self.R = get_param('physical.mars_atmosphere_composition.R_specific')
        self.gamma = get_param('physical.mars_atmosphere_composition.gamma')
        self.g = get_param('physical.mars.g')
        
        # Reference conditions
        ref = get_param('environment.reference_atmosphere')
        self.T0 = ref['T_surface']
        self.P0 = ref['P_surface']
        self.H = ref['scale_height_km']
        self.lapse_rate = ref['lapse_rate']
        
        # Sutherland's law parameters
        suth = get_param('physical.sutherland')
        self.mu_ref = suth['mu_ref']
        self.T_mu_ref = suth['T_ref']
        self.C_suth = suth['C']
    
    def temperature(self, altitude_km: float) -> float:
        """
        Calculate temperature at given altitude.
        
        Uses linear lapse rate model.
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        float
            Temperature in Kelvin
        """
        # Lapse rate in K/km
        lapse_K_km = self.lapse_rate * 1000
        return self.T0 - lapse_K_km * altitude_km
    
    def pressure(self, altitude_km: float) -> float:
        """
        Calculate pressure using barometric formula.
        
        P = P0 × exp(-g×h / (R×T))
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        float
            Pressure in Pascals
        """
        h_m = altitude_km * 1000
        T = self.temperature(altitude_km)
        exponent = -self.g * h_m / (self.R * T)
        return self.P0 * math.exp(exponent)
    
    def density(self, altitude_km: float) -> float:
        """
        Calculate density using ideal gas law.
        
        ρ = P / (R × T)
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        float
            Density in kg/m³
        """
        P = self.pressure(altitude_km)
        T = self.temperature(altitude_km)
        return P / (self.R * T)
    
    def viscosity(self, altitude_km: float) -> float:
        """
        Calculate dynamic viscosity using Sutherland's law for CO2.
        
        μ = μ_ref × (T/T_ref)^1.5 × (T_ref + C) / (T + C)
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        float
            Dynamic viscosity in Pa·s
        """
        T = self.temperature(altitude_km)
        ratio = (T / self.T_mu_ref) ** 1.5
        factor = (self.T_mu_ref + self.C_suth) / (T + self.C_suth)
        return self.mu_ref * ratio * factor
    
    def speed_of_sound(self, altitude_km: float) -> float:
        """
        Calculate speed of sound.
        
        a = sqrt(γ × R × T)
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        float
            Speed of sound in m/s
        """
        T = self.temperature(altitude_km)
        return math.sqrt(self.gamma * self.R * T)
    
    def get_state(self, altitude_km: float) -> AtmosphericState:
        """
        Get complete atmospheric state at given altitude.
        
        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km
            
        Returns
        -------
        AtmosphericState
            Dataclass containing all atmospheric properties
        """
        return AtmosphericState(
            altitude_km=altitude_km,
            temperature_K=self.temperature(altitude_km),
            pressure_Pa=self.pressure(altitude_km),
            density_kg_m3=self.density(altitude_km),
            viscosity_Pa_s=self.viscosity(altitude_km),
            speed_of_sound_m_s=self.speed_of_sound(altitude_km),
        )
    
    def reynolds_number(
        self, 
        velocity: float, 
        length: float, 
        altitude_km: float = -3.0
    ) -> float:
        """
        Calculate Reynolds number.
        
        Re = ρ × V × L / μ
        
        Parameters
        ----------
        velocity : float
            Flow velocity in m/s
        length : float
            Characteristic length in m
        altitude_km : float
            Altitude in km (default: Arcadia Planitia at -3 km)
            
        Returns
        -------
        float
            Reynolds number (dimensionless)
        """
        rho = self.density(altitude_km)
        mu = self.viscosity(altitude_km)
        return rho * velocity * length / mu
    
    def mach_number(self, velocity: float, altitude_km: float = -3.0) -> float:
        """
        Calculate Mach number.
        
        M = V / a
        
        Parameters
        ----------
        velocity : float
            Flow velocity in m/s
        altitude_km : float
            Altitude in km (default: Arcadia Planitia)
            
        Returns
        -------
        float
            Mach number (dimensionless)
        """
        a = self.speed_of_sound(altitude_km)
        return velocity / a
    
    @classmethod
    def arcadia_planitia(cls) -> 'MarsAtmosphere':
        """
        Create atmosphere model for Arcadia Planitia operations.
        
        Returns
        -------
        MarsAtmosphere
            Configured atmosphere model
        """
        return cls()


def get_arcadia_conditions() -> AtmosphericState:
    """
    Get atmospheric conditions at Arcadia Planitia (-3 km elevation).
    
    Convenience function for the primary operating location.
    
    Returns
    -------
    AtmosphericState
        Atmospheric properties at Arcadia Planitia
    """
    atm = MarsAtmosphere()
    elevation = get_param('environment.arcadia_planitia.elevation_km')
    return atm.get_state(elevation)


def print_atmosphere_table(altitudes: list = None):
    """Print atmospheric properties at various altitudes."""
    if altitudes is None:
        altitudes = [-5, -3, 0, 5, 10, 15, 20]
    
    atm = MarsAtmosphere()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("MARS ATMOSPHERIC MODEL (Section 3.1)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   Parameters from config/physical_constants.yaml")
    print(f"          and config/mars_environment.yaml")
    print()
    
    print(f"{'Alt (km)':>10} {'T (K)':>10} {'P (Pa)':>10} {'ρ (kg/m³)':>12} {'μ (Pa·s)':>12} {'a (m/s)':>10}")
    print("-" * 80)
    
    for h in altitudes:
        state = atm.get_state(h)
        print(f"{h:>10.1f} {state.temperature_K:>10.1f} {state.pressure_Pa:>10.1f} "
              f"{state.density_kg_m3:>12.4f} {state.viscosity_Pa_s:>12.2e} {state.speed_of_sound_m_s:>10.1f}")
    
    print("-" * 80)
    
    # Highlight Arcadia Planitia
    arcadia = get_arcadia_conditions()
    print(f"\nARCADIA PLANITIA (operating location, h = {arcadia.altitude_km} km):")
    print(f"  Temperature:    {arcadia.temperature_K:.1f} K")
    print(f"  Pressure:       {arcadia.pressure_Pa:.1f} Pa")
    print(f"  Density:        {arcadia.density_kg_m3:.4f} kg/m³")
    print(f"  Viscosity:      {arcadia.viscosity_Pa_s:.2e} Pa·s")
    print(f"  Speed of sound: {arcadia.speed_of_sound_m_s:.1f} m/s")
    
    # Compare with config values
    config_rho = get_param('environment.arcadia_planitia.density_kg_m3')
    print(f"\n  Config density: {config_rho} kg/m³")
    print(f"  Difference:     {abs(arcadia.density_kg_m3 - config_rho):.6f} kg/m³")
    
    print("=" * 80)


if __name__ == "__main__":
    print_atmosphere_table()
