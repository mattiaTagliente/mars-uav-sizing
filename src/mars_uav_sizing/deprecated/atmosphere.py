"""
Mars Atmospheric Model
======================

Provides atmospheric properties (density, temperature, pressure, viscosity, speed of sound)
as a function of altitude above the Mars areoid (datum).

The model is based on exponential atmosphere with temperature lapse rate correction,
validated against Viking Lander measurements and Mars-GRAM data.

References:
- Seiff, A. (1977). Structure of the Atmosphere of Mars in Summer at Mid-Latitudes. JGR.
- Mars-GRAM 2010 (NASA MSFC)
- Desert et al. 2017 - Aerodynamic Design on a Martian Micro Air Vehicle
"""

from dataclasses import dataclass
import math
from typing import Optional

from .constants import (
    G_MARS,
    R_MARS,
    GAMMA_MARS,
    T_SURFACE_REF,
    P_SURFACE_REF,
    RHO_SURFACE_REF,
    H_SCALE,
    LAPSE_RATE,
    MU_REF,
    T_MU_REF,
    C_SUTHERLAND,
    ARCADIA_ELEVATION,
)


@dataclass
class AtmosphericState:
    """
    Container for atmospheric properties at a given altitude.

    Attributes
    ----------
    altitude_km : float
        Altitude above Mars areoid (datum) in km
    temperature : float
        Temperature in Kelvin
    pressure : float
        Pressure in Pascals
    density : float
        Density in kg/m³
    viscosity : float
        Dynamic viscosity in Pa·s
    speed_of_sound : float
        Speed of sound in m/s
    """

    altitude_km: float
    temperature: float  # K
    pressure: float  # Pa
    density: float  # kg/m³
    viscosity: float  # Pa·s
    speed_of_sound: float  # m/s

    @property
    def kinematic_viscosity(self) -> float:
        """Kinematic viscosity in m²/s."""
        return self.viscosity / self.density


class MarsAtmosphere:
    """
    Mars atmospheric model providing properties as a function of altitude.

    The model uses an exponential atmosphere with optional temperature lapse rate.
    Reference conditions are defined at the Mars areoid (0 km datum).

    Parameters
    ----------
    T_surface : float, optional
        Surface temperature in K (default: 210 K)
    P_surface : float, optional
        Surface pressure in Pa (default: 636 Pa)
    use_lapse_rate : bool, optional
        Whether to use temperature lapse rate (default: True)

    Examples
    --------
    >>> atm = MarsAtmosphere()
    >>> state = atm.get_state(altitude_km=-3.0)  # Arcadia Planitia
    >>> print(f"Density: {state.density:.4f} kg/m³")
    Density: 0.0175 kg/m³
    """

    def __init__(
        self,
        T_surface: float = T_SURFACE_REF,
        P_surface: float = P_SURFACE_REF,
        use_lapse_rate: bool = True,
    ):
        self.T_surface = T_surface
        self.P_surface = P_surface
        self.use_lapse_rate = use_lapse_rate

        # Reference density at surface
        self.rho_surface = P_surface / (R_MARS * T_surface)

        # Scale height at reference temperature
        self.H_scale = R_MARS * T_surface / G_MARS

    def temperature(self, altitude_km: float) -> float:
        """
        Calculate temperature at given altitude.

        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km

        Returns
        -------
        float
            Temperature in Kelvin
        """
        altitude_m = altitude_km * 1000.0

        if self.use_lapse_rate:
            # Temperature decreases with altitude in lower atmosphere
            # Lapse rate is approximately 2.5 K/km in lower 40 km
            T = self.T_surface - LAPSE_RATE * altitude_m
            # Ensure temperature doesn't go below ~140 K (mesospheric minimum)
            T = max(T, 140.0)
        else:
            T = self.T_surface

        return T

    def pressure(self, altitude_km: float) -> float:
        """
        Calculate pressure at given altitude using barometric formula.

        For isothermal atmosphere: p = p0 * exp(-h/H)
        For non-isothermal: uses integrated form with lapse rate

        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km

        Returns
        -------
        float
            Pressure in Pascals
        """
        altitude_m = altitude_km * 1000.0

        if self.use_lapse_rate and LAPSE_RATE > 0:
            # Non-isothermal barometric formula
            T = self.temperature(altitude_km)
            exponent = G_MARS / (R_MARS * LAPSE_RATE)
            p = self.P_surface * (T / self.T_surface) ** exponent
        else:
            # Isothermal exponential atmosphere
            p = self.P_surface * math.exp(-altitude_m / self.H_scale)

        return p

    def density(self, altitude_km: float) -> float:
        """
        Calculate density at given altitude using ideal gas law.

        rho = p / (R * T)

        Parameters
        ----------
        altitude_km : float
            Altitude above Mars areoid in km

        Returns
        -------
        float
            Density in kg/m³
        """
        T = self.temperature(altitude_km)
        p = self.pressure(altitude_km)
        return p / (R_MARS * T)

    def viscosity(self, altitude_km: float) -> float:
        """
        Calculate dynamic viscosity using Sutherland's law for CO2.

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
        return MU_REF * (T / T_MU_REF) ** 1.5 * (T_MU_REF + C_SUTHERLAND) / (T + C_SUTHERLAND)

    def speed_of_sound(self, altitude_km: float) -> float:
        """
        Calculate speed of sound at given altitude.

        a = sqrt(gamma * R * T)

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
        return math.sqrt(GAMMA_MARS * R_MARS * T)

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
            temperature=self.temperature(altitude_km),
            pressure=self.pressure(altitude_km),
            density=self.density(altitude_km),
            viscosity=self.viscosity(altitude_km),
            speed_of_sound=self.speed_of_sound(altitude_km),
        )

    def reynolds_number(
        self, velocity: float, length: float, altitude_km: float = ARCADIA_ELEVATION
    ) -> float:
        """
        Calculate Reynolds number at given conditions.

        Re = rho * V * L / mu

        Parameters
        ----------
        velocity : float
            Flow velocity in m/s
        length : float
            Characteristic length (e.g., chord) in m
        altitude_km : float, optional
            Altitude in km (default: Arcadia Planitia elevation)

        Returns
        -------
        float
            Reynolds number (dimensionless)
        """
        rho = self.density(altitude_km)
        mu = self.viscosity(altitude_km)
        return rho * velocity * length / mu

    def mach_number(self, velocity: float, altitude_km: float = ARCADIA_ELEVATION) -> float:
        """
        Calculate Mach number at given conditions.

        M = V / a

        Parameters
        ----------
        velocity : float
            Flow velocity in m/s
        altitude_km : float, optional
            Altitude in km (default: Arcadia Planitia elevation)

        Returns
        -------
        float
            Mach number (dimensionless)
        """
        a = self.speed_of_sound(altitude_km)
        return velocity / a

    @classmethod
    def arcadia_planitia(cls, T_surface: Optional[float] = None) -> "MarsAtmosphere":
        """
        Create atmosphere model configured for Arcadia Planitia conditions.

        Parameters
        ----------
        T_surface : float, optional
            Surface temperature in K. If not specified, uses mean value.

        Returns
        -------
        MarsAtmosphere
            Atmosphere model instance
        """
        T = T_surface if T_surface is not None else 210.0

        # Adjust surface pressure for Arcadia's lower elevation
        # P increases below datum due to thicker atmosphere column
        P_arcadia = P_SURFACE_REF * math.exp(-ARCADIA_ELEVATION * 1000.0 / H_SCALE)

        return cls(T_surface=T, P_surface=P_arcadia)


def print_atmosphere_table(
    atm: MarsAtmosphere, altitudes: Optional[list] = None
) -> None:
    """
    Print a table of atmospheric properties at various altitudes.

    Parameters
    ----------
    atm : MarsAtmosphere
        Atmosphere model instance
    altitudes : list, optional
        List of altitudes in km (default: -5 to 20 km)
    """
    if altitudes is None:
        altitudes = [-5, -3, -1, 0, 1, 2, 5, 10, 15, 20]

    print("\nMars Atmosphere Properties")
    print("=" * 80)
    print(
        f"{'Alt (km)':>10} {'T (K)':>10} {'P (Pa)':>12} {'ρ (kg/m³)':>12} "
        f"{'μ (Pa·s)':>12} {'a (m/s)':>10}"
    )
    print("-" * 80)

    for h in altitudes:
        state = atm.get_state(h)
        print(
            f"{state.altitude_km:>10.1f} {state.temperature:>10.1f} "
            f"{state.pressure:>12.2f} {state.density:>12.5f} "
            f"{state.viscosity:>12.2e} {state.speed_of_sound:>10.1f}"
        )


if __name__ == "__main__":
    # Example usage and validation
    print("Mars Atmospheric Model - Validation")
    print("=" * 60)

    # Create standard atmosphere
    atm = MarsAtmosphere()

    # Print properties at Arcadia Planitia
    state = atm.get_state(ARCADIA_ELEVATION)
    print(f"\nArcadia Planitia (elevation: {ARCADIA_ELEVATION} km):")
    print(f"  Temperature:    {state.temperature:.1f} K")
    print(f"  Pressure:       {state.pressure:.1f} Pa ({state.pressure/100:.2f} mbar)")
    print(f"  Density:        {state.density:.5f} kg/m³")
    print(f"  Viscosity:      {state.viscosity:.2e} Pa·s")
    print(f"  Speed of sound: {state.speed_of_sound:.1f} m/s")

    # Calculate Reynolds number for typical Mars UAV
    V_cruise = 40.0  # m/s
    c_chord = 0.58   # m (from Configuration A)
    Re = atm.reynolds_number(V_cruise, c_chord, ARCADIA_ELEVATION)
    Ma = atm.mach_number(V_cruise, ARCADIA_ELEVATION)

    print(f"\nFlight conditions at V={V_cruise} m/s, chord={c_chord} m:")
    print(f"  Reynolds number: {Re:.0f} ({Re/1000:.1f}k)")
    print(f"  Mach number:     {Ma:.3f}")

    # Print atmosphere table
    print_atmosphere_table(atm)
