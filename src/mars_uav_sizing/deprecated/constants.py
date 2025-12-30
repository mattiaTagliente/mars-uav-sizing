"""
Physical constants and Mars environment parameters.

References:
- Mars atmospheric data: NASA Mars Fact Sheet
- Viking Lander measurements
- Desert et al. 2017 - Aerodynamic Design on a Martian Micro Air Vehicle
"""

import math

# ============================================================================
# Universal Physical Constants
# ============================================================================

G_EARTH = 9.80665  # m/s², standard gravity on Earth
G_MARS = 3.711     # m/s², gravity on Mars (38% of Earth)

# ============================================================================
# Mars Atmospheric Composition
# ============================================================================

# Molar masses (kg/mol)
M_CO2 = 44.01e-3   # Carbon dioxide
M_N2 = 28.01e-3    # Nitrogen
M_AR = 39.95e-3    # Argon

# Volume fractions
X_CO2 = 0.9532     # 95.32% CO2
X_N2 = 0.027       # 2.7% N2
X_AR = 0.016       # 1.6% Ar

# Mean molar mass of Mars atmosphere
M_MARS = X_CO2 * M_CO2 + X_N2 * M_N2 + X_AR * M_AR  # ~43.34e-3 kg/mol

# Specific gas constant for Mars atmosphere
R_UNIVERSAL = 8.314462  # J/(mol·K)
R_MARS = R_UNIVERSAL / M_MARS  # ~191.8 J/(kg·K)

# Specific heat ratio (gamma) for CO2-dominated atmosphere
GAMMA_MARS = 1.29  # cp/cv for CO2 at ~200K

# ============================================================================
# Mars Reference Atmosphere (Surface at Datum)
# ============================================================================

# Reference values at Mars areoid (0 km datum)
T_SURFACE_REF = 210.0     # K, mean surface temperature
P_SURFACE_REF = 636.0     # Pa, mean surface pressure (~6.36 mbar)
RHO_SURFACE_REF = P_SURFACE_REF / (R_MARS * T_SURFACE_REF)  # ~0.0158 kg/m³

# Scale height
H_SCALE = R_MARS * T_SURFACE_REF / G_MARS  # ~10.8 km

# Temperature lapse rate (varies, but approximately)
LAPSE_RATE = 0.0025  # K/m (about 2.5 K per km in lower atmosphere)

# ============================================================================
# Arcadia Planitia Specific Conditions
# ============================================================================

# Arcadia Planitia is at approximately -3 km below datum
# This results in higher density than average

ARCADIA_ELEVATION = -3.0  # km below datum
ARCADIA_LATITUDE = 47.2   # degrees North

# Seasonal temperature variations at Arcadia Planitia
T_ARCADIA_SUMMER = 220.0  # K, summer daytime
T_ARCADIA_WINTER = 180.0  # K, winter
T_ARCADIA_MEAN = 210.0    # K, annual mean

# Density at Arcadia Planitia (elevated due to low altitude)
# Using exponential atmosphere: rho = rho0 * exp(h/H)
RHO_ARCADIA = RHO_SURFACE_REF * math.exp(-ARCADIA_ELEVATION / H_SCALE)  # ~0.017 kg/m³

# ============================================================================
# Dynamic Viscosity (Sutherland's Law for CO2)
# ============================================================================

# Reference viscosity for CO2
MU_REF = 1.48e-5   # Pa·s at T_ref = 293 K
T_MU_REF = 293.0   # K
C_SUTHERLAND = 240.0  # K, Sutherland constant for CO2

def dynamic_viscosity_co2(T: float) -> float:
    """
    Calculate dynamic viscosity of CO2 using Sutherland's law.

    Parameters
    ----------
    T : float
        Temperature in Kelvin

    Returns
    -------
    float
        Dynamic viscosity in Pa·s
    """
    return MU_REF * (T / T_MU_REF) ** 1.5 * (T_MU_REF + C_SUTHERLAND) / (T + C_SUTHERLAND)

# Approximate viscosity at Mars surface temperature
MU_MARS_SURFACE = dynamic_viscosity_co2(T_SURFACE_REF)  # ~1.13e-5 Pa·s

# ============================================================================
# Speed of Sound
# ============================================================================

def speed_of_sound(T: float) -> float:
    """
    Calculate speed of sound in Mars atmosphere.

    a = sqrt(gamma * R * T)

    Parameters
    ----------
    T : float
        Temperature in Kelvin

    Returns
    -------
    float
        Speed of sound in m/s
    """
    return math.sqrt(GAMMA_MARS * R_MARS * T)

# Speed of sound at reference temperature
A_MARS_REF = speed_of_sound(T_SURFACE_REF)  # ~244 m/s

# ============================================================================
# Solar Irradiance
# ============================================================================

# Solar constant at Mars (average)
SOLAR_CONSTANT_MARS = 589.0  # W/m² at 1.52 AU (43% of Earth's 1361 W/m²)

# Surface irradiance accounting for atmospheric attenuation
SOLAR_SURFACE_CLEAR = 500.0  # W/m² at noon, clear day
SOLAR_SURFACE_DUSTY = 300.0  # W/m² during dusty conditions

# ============================================================================
# Wind Conditions at Arcadia Planitia
# ============================================================================

WIND_MEAN = 10.0           # m/s, average wind speed
WIND_GUST_MAX = 45.0       # m/s, maximum recorded gusts
WIND_DUST_DEVIL = 30.0     # m/s, typical dust devil wind speed

# ============================================================================
# Common Unit Conversions
# ============================================================================

def kg_to_N_mars(mass_kg: float) -> float:
    """Convert mass in kg to weight in Newtons on Mars."""
    return mass_kg * G_MARS

def N_to_kg_mars(weight_N: float) -> float:
    """Convert weight in Newtons to mass in kg on Mars."""
    return weight_N / G_MARS
