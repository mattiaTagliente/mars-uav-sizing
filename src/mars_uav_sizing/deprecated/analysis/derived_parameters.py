"""
Derived Parameters Calculations for Section 4.12
=================================================

Calculates and verifies the numerical values used in the derived requirements
section of the manuscript. These values are inputs to the constraint analysis.

Reference:
- Manuscript: sections_en/04_12_derived-requirements-sec-derived-requirements.md
"""

import math
from typing import Dict, Any


# Physical constants
G_MARS = 3.711          # m/s² (Mars gravity)
G_EARTH = 9.81          # m/s² (Earth gravity)
RHO_MARS = 0.0196       # kg/m³ (Mars at -3 km elevation)
RHO_EARTH = 1.225       # kg/m³ (Earth sea level)


def calculate_ingenuity_disk_loading() -> Dict[str, float]:
    """
    Calculate Ingenuity helicopter disk loading.
    
    Reference: Tzanetos et al. (2022), Balaram et al. (2018)
    - Mass: 1.8 kg
    - Rotor diameter: 1.2 m (radius 0.60 m)
    - Configuration: Coaxial (2 rotors)
    
    Returns
    -------
    dict
        Disk loading calculation breakdown
    """
    mass_kg = 1.8
    rotor_radius_m = 0.60
    n_rotors = 2  # Coaxial configuration
    
    weight_mars_n = mass_kg * G_MARS
    single_disk_area = math.pi * rotor_radius_m**2
    total_disk_area = n_rotors * single_disk_area
    disk_loading = weight_mars_n / total_disk_area
    
    return {
        'name': 'Ingenuity',
        'mass_kg': mass_kg,
        'weight_mars_n': weight_mars_n,
        'rotor_radius_m': rotor_radius_m,
        'n_rotors': n_rotors,
        'single_disk_area_m2': single_disk_area,
        'total_disk_area_m2': total_disk_area,
        'disk_loading_n_m2': disk_loading,
    }


def calculate_msh_disk_loading() -> Dict[str, float]:
    """
    Calculate Mars Science Helicopter disk loading.
    
    Reference: Johnson et al. (2020), NASA/TM-2020-220485
    - Mass: 31 kg (hexacopter configuration)
    - Rotor radius: 0.64 m
    - Configuration: Hexacopter (6 rotors)
    
    Returns
    -------
    dict
        Disk loading calculation breakdown
    """
    mass_kg = 31.0
    rotor_radius_m = 0.64
    n_rotors = 6  # Hexacopter
    
    weight_mars_n = mass_kg * G_MARS
    single_disk_area = math.pi * rotor_radius_m**2
    total_disk_area = n_rotors * single_disk_area
    disk_loading = weight_mars_n / total_disk_area
    
    return {
        'name': 'Mars Science Helicopter',
        'mass_kg': mass_kg,
        'weight_mars_n': weight_mars_n,
        'rotor_radius_m': rotor_radius_m,
        'n_rotors': n_rotors,
        'single_disk_area_m2': single_disk_area,
        'total_disk_area_m2': total_disk_area,
        'disk_loading_n_m2': disk_loading,
    }


def calculate_mars_uav_rotor_sizing(
    mtow_kg: float = 10.0,
    disk_loading: float = 30.0,
    n_rotors: int = 4
) -> Dict[str, float]:
    """
    Calculate rotor sizing for Mars UAV given disk loading.
    
    Parameters
    ----------
    mtow_kg : float
        MTOW in kg
    disk_loading : float
        Target disk loading in N/m²
    n_rotors : int
        Number of lift rotors
    
    Returns
    -------
    dict
        Rotor sizing results
    """
    weight_mars_n = mtow_kg * G_MARS
    total_disk_area = weight_mars_n / disk_loading
    rotor_area_each = total_disk_area / n_rotors
    rotor_radius = math.sqrt(rotor_area_each / math.pi)
    rotor_diameter = 2 * rotor_radius
    
    return {
        'mtow_kg': mtow_kg,
        'weight_mars_n': weight_mars_n,
        'disk_loading_n_m2': disk_loading,
        'n_rotors': n_rotors,
        'total_disk_area_m2': total_disk_area,
        'rotor_area_each_m2': rotor_area_each,
        'rotor_radius_m': rotor_radius,
        'rotor_diameter_m': rotor_diameter,
        'rotor_diameter_in': rotor_diameter * 39.37,  # inches
    }


def calculate_density_scaling() -> Dict[str, float]:
    """
    Calculate Mars/Earth density scaling for disk loading.
    
    To maintain equivalent induced velocity on Mars,
    disk loading must scale inversely with density.
    
    Returns
    -------
    dict
        Scaling factors
    """
    density_ratio = RHO_EARTH / RHO_MARS
    
    return {
        'rho_earth_kg_m3': RHO_EARTH,
        'rho_mars_kg_m3': RHO_MARS,
        'density_ratio': density_ratio,
        'disk_loading_scale_factor': density_ratio,
    }


def calculate_combined_efficiencies() -> Dict[str, float]:
    """
    Calculate combined propulsion chain efficiencies.
    
    Returns
    -------
    dict
        Individual and combined efficiencies
    """
    # Individual efficiencies (from §4.5)
    fm = 0.40           # Figure of merit
    eta_prop = 0.55     # Propeller efficiency
    eta_motor = 0.85    # Motor efficiency
    eta_esc = 0.95      # ESC efficiency
    eta_batt = 0.95     # Battery discharge efficiency
    
    # Combined efficiencies
    eta_hover = fm * eta_motor * eta_esc
    eta_cruise = eta_prop * eta_motor * eta_esc
    
    return {
        'fm': fm,
        'eta_prop': eta_prop,
        'eta_motor': eta_motor,
        'eta_esc': eta_esc,
        'eta_batt': eta_batt,
        'eta_hover': eta_hover,
        'eta_cruise': eta_cruise,
    }


def calculate_aerodynamic_derived() -> Dict[str, float]:
    """
    Calculate derived aerodynamic parameters.
    
    These are computed from the base parameters in §4.7.
    
    Returns
    -------
    dict
        Derived aerodynamic values
    """
    # Base parameters (from §4.7)
    ar = 6              # Aspect ratio
    e = 0.869           # Oswald efficiency (Sadraey correlation for AR=6)
    cd0 = 0.030         # Zero-lift drag coefficient
    
    # Derived parameters
    k = 1 / (math.pi * ar * e)  # Induced drag factor
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)  # Maximum L/D
    cl_star = math.sqrt(math.pi * ar * e * cd0)  # Optimal C_L
    
    # QuadPlane L/D (with 10% penalty for stopped rotors)
    ld_penalty = 0.90
    ld_quadplane = ld_max * ld_penalty
    
    # Rotorcraft equivalent L/D (from Leishman, Prouty)
    ld_eff_rotorcraft = 4.0
    
    return {
        'ar': ar,
        'e': e,
        'cd0': cd0,
        'k': k,
        'ld_max': ld_max,
        'cl_star': cl_star,
        'ld_penalty': ld_penalty,
        'ld_quadplane': ld_quadplane,
        'ld_eff_rotorcraft': ld_eff_rotorcraft,
    }


def print_all_calculations():
    """Print all derived parameter calculations."""
    print("=" * 80)
    print("DERIVED PARAMETERS CALCULATIONS (Section 4.12)")
    print("=" * 80)
    print()
    
    # Ingenuity disk loading
    print("INGENUITY DISK LOADING (@eq:dl-ingenuity)")
    print("-" * 40)
    ing = calculate_ingenuity_disk_loading()
    print(f"Mass:               {ing['mass_kg']:.1f} kg")
    print(f"Weight (Mars):      {ing['weight_mars_n']:.2f} N")
    print(f"Rotor radius:       {ing['rotor_radius_m']:.2f} m")
    print(f"Number of rotors:   {ing['n_rotors']}")
    print(f"Single disk area:   {ing['single_disk_area_m2']:.3f} m²")
    print(f"Total disk area:    {ing['total_disk_area_m2']:.2f} m²")
    print(f"Disk loading:       {ing['disk_loading_n_m2']:.1f} N/m²")
    print()
    
    # MSH disk loading
    print("MARS SCIENCE HELICOPTER DISK LOADING (@eq:dl-msh)")
    print("-" * 40)
    msh = calculate_msh_disk_loading()
    print(f"Mass:               {msh['mass_kg']:.1f} kg")
    print(f"Weight (Mars):      {msh['weight_mars_n']:.1f} N")
    print(f"Rotor radius:       {msh['rotor_radius_m']:.2f} m")
    print(f"Number of rotors:   {msh['n_rotors']}")
    print(f"Single disk area:   {msh['single_disk_area_m2']:.3f} m²")
    print(f"Total disk area:    {msh['total_disk_area_m2']:.2f} m²")
    print(f"Disk loading:       {msh['disk_loading_n_m2']:.1f} N/m²")
    print()
    
    # Density scaling
    print("DENSITY SCALING FACTOR")
    print("-" * 40)
    scale = calculate_density_scaling()
    print(f"ρ_Earth:            {scale['rho_earth_kg_m3']:.3f} kg/m³")
    print(f"ρ_Mars:             {scale['rho_mars_kg_m3']:.4f} kg/m³")
    print(f"Density ratio:      {scale['density_ratio']:.0f}")
    print()
    
    # Mars UAV rotor sizing
    print("MARS UAV ROTOR SIZING (DL = 30 N/m²)")
    print("-" * 40)
    uav = calculate_mars_uav_rotor_sizing()
    print(f"MTOW:               {uav['mtow_kg']:.1f} kg")
    print(f"Weight (Mars):      {uav['weight_mars_n']:.1f} N")
    print(f"Disk loading:       {uav['disk_loading_n_m2']:.0f} N/m²")
    print(f"Number of rotors:   {uav['n_rotors']}")
    print(f"Total disk area:    {uav['total_disk_area_m2']:.2f} m²")
    print(f"Rotor radius each:  {uav['rotor_radius_m']:.2f} m")
    print(f"Rotor diameter:     {uav['rotor_diameter_m']:.2f} m ({uav['rotor_diameter_in']:.0f} in)")
    print()
    
    # Combined efficiencies
    print("COMBINED PROPULSION EFFICIENCIES")
    print("-" * 40)
    eff = calculate_combined_efficiencies()
    print(f"Figure of merit:    {eff['fm']:.2f}")
    print(f"Propeller η:        {eff['eta_prop']:.2f}")
    print(f"Motor η:            {eff['eta_motor']:.2f}")
    print(f"ESC η:              {eff['eta_esc']:.2f}")
    print(f"Battery η:          {eff['eta_batt']:.2f}")
    print(f"Combined η_hover:   {eff['eta_hover']:.3f}  [FM × η_motor × η_ESC]")
    print(f"Combined η_cruise:  {eff['eta_cruise']:.3f}  [η_prop × η_motor × η_ESC]")
    print()
    
    # Aerodynamic derived
    print("DERIVED AERODYNAMIC PARAMETERS")
    print("-" * 40)
    aero = calculate_aerodynamic_derived()
    print(f"Aspect ratio:       {aero['ar']}")
    print(f"Oswald e:           {aero['e']:.3f}")
    print(f"C_D0:               {aero['cd0']:.3f}")
    print(f"K (induced factor): {aero['k']:.4f}")
    print(f"(L/D)_max:          {aero['ld_max']:.1f}")
    print(f"C_L* (optimal):     {aero['cl_star']:.2f}")
    print(f"QuadPlane L/D:      {aero['ld_quadplane']:.1f}  [90% of (L/D)_max]")
    print(f"Rotorcraft (L/D)_eff: {aero['ld_eff_rotorcraft']:.1f}")
    print()
    
    print("=" * 80)
    print("VALUES FOR MANUSCRIPT UPDATE:")
    print("=" * 80)
    print()
    print("Disk loading calculations:")
    print(f"  Ingenuity:  {ing['disk_loading_n_m2']:.1f} N/m² (manuscript states ~3.0)")
    print(f"  MSH:        {msh['disk_loading_n_m2']:.1f} N/m² (manuscript states ~15)")
    print(f"  Scale:      {scale['density_ratio']:.0f}× (manuscript states ~63)")
    print()
    print("Mars UAV rotor sizing at DL = 30 N/m²:")
    print(f"  Total disk area:  {uav['total_disk_area_m2']:.2f} m² (manuscript states ~1.24)")
    print(f"  Rotor radius:     {uav['rotor_radius_m']:.2f} m (manuscript states ~0.31)")
    print()
    

if __name__ == "__main__":
    print_all_calculations()
