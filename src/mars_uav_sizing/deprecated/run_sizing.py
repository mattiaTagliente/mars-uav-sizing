#!/usr/bin/env python3
"""
Mars UAV Sizing - Main Entry Point
===================================

Runs the complete sizing analysis for Mars UAV configurations:
- Configuration A: 7.5 kg battery-only minimal design
- Configuration B: 24 kg solar-augmented extended endurance

Outputs:
- Constraint diagrams
- Weight breakdowns
- Power budgets
- Performance comparison tables
- Figures for final report

Usage:
    python -m mars_uav_sizing.run_sizing

References:
- Desert et al. (2017). Aerodynamic Design on a Martian Micro Air Vehicle.
- Barbato et al. (2024). Preliminary Design of a Fixed-Wing Drone for Mars.
"""

import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

from .constants import (
    G_MARS,
    RHO_ARCADIA,
    RHO_SURFACE_REF,
    ARCADIA_ELEVATION,
)
from .atmosphere import MarsAtmosphere, AtmosphericState
from .aerodynamics import DragPolar, cruise_power
from .constraints import SizingConstraints, sizing_iteration
from .weights import WeightEstimation, MassBreakdown
from .endurance import (
    EnduranceCalculator,
    PowerBudget,
    hover_power,
    solar_power_available,
    mission_energy_breakdown,
)


@dataclass
class UAVConfiguration:
    """Complete UAV configuration specification."""
    name: str
    mtow: float  # kg
    payload_mass: float  # kg
    wing_span: float  # m
    wing_area: float  # m²
    aspect_ratio: float
    chord: float  # m
    cruise_speed: float  # m/s
    cruise_altitude_km: float  # km (relative to Arcadia)
    n_lift_rotors: int
    rotor_radius: float  # m
    battery_capacity_wh: float
    solar_area: float  # m² (0 for battery-only)
    solar_efficiency: float


@dataclass
class PerformanceResults:
    """Performance analysis results."""
    config: UAVConfiguration
    weight_n: float
    rho: float
    reynolds: float
    mach: float
    cl_cruise: float
    cd_cruise: float
    ld_ratio: float
    cruise_power_w: float
    hover_power_w: float
    total_power_cruise_w: float
    endurance_h: float
    range_km: float
    operational_radius_km: float
    mass_breakdown: MassBreakdown


def analyze_atmosphere(altitude_km: float = ARCADIA_ELEVATION) -> AtmosphericState:
    """Get atmospheric conditions at operating altitude."""
    atm = MarsAtmosphere.arcadia_planitia()
    return atm.get_state(altitude_km)


def calculate_reynolds(
    velocity: float,
    chord: float,
    rho: float,
    mu: float,
) -> float:
    """Calculate Reynolds number."""
    return rho * velocity * chord / mu


def size_configuration_a() -> Tuple[UAVConfiguration, PerformanceResults]:
    """
    Size Configuration A: 7.5 kg battery-only minimal design.

    Key design choices:
    - Minimal mass for feasibility demonstration
    - 8 coaxial lift rotors (octocopter) for redundancy
    - High aspect ratio (AR=12) for efficiency
    - No solar panels (battery-only)
    """
    print("\n" + "=" * 60)
    print("CONFIGURATION A: 7.5 kg Battery-Only Minimal Design")
    print("=" * 60)

    # Design parameters
    mtow = 7.5  # kg
    payload = 0.5  # kg (micro camera only)
    battery_wh = 390  # Wh (Saft MP 176065 xtd)

    # Wing geometry (high AR for efficiency)
    aspect_ratio = 12.0
    wing_area = 4.04  # m² (from constraint analysis)
    wing_span = math.sqrt(aspect_ratio * wing_area)  # 6.96 m
    chord = wing_area / wing_span  # 0.58 m

    # Flight conditions
    cruise_speed = 40.0  # m/s
    cruise_alt_km = ARCADIA_ELEVATION + 0.5  # 500m AGL

    # Rotor configuration (8 coaxial rotors)
    n_rotors = 8
    rotor_radius = 0.30  # m

    config = UAVConfiguration(
        name="Configuration A",
        mtow=mtow,
        payload_mass=payload,
        wing_span=wing_span,
        wing_area=wing_area,
        aspect_ratio=aspect_ratio,
        chord=chord,
        cruise_speed=cruise_speed,
        cruise_altitude_km=cruise_alt_km,
        n_lift_rotors=n_rotors,
        rotor_radius=rotor_radius,
        battery_capacity_wh=battery_wh,
        solar_area=0.0,
        solar_efficiency=0.0,
    )

    # Atmospheric conditions
    atm = MarsAtmosphere.arcadia_planitia()
    state = atm.get_state(cruise_alt_km)
    rho = state.density
    mu = state.viscosity

    # Weight
    weight_n = mtow * G_MARS

    # Aerodynamics
    re = calculate_reynolds(cruise_speed, chord, rho, mu)
    mach = cruise_speed / state.speed_of_sound

    # Drag polar (based on low-Re airfoil data)
    # CD0 ≈ 0.025 for clean configuration
    # e ≈ 0.80 for high AR wing
    cd0 = 0.025
    oswald = 0.80
    polar = DragPolar(cd0=cd0, aspect_ratio=aspect_ratio, oswald_efficiency=oswald)

    # Cruise CL
    cl_cruise = (2.0 * weight_n) / (rho * cruise_speed**2 * wing_area)

    # Cruise CD
    cd_cruise = polar.cd(cl_cruise)

    # L/D
    ld_ratio = cl_cruise / cd_cruise

    # Cruise power (propulsion only)
    eta_prop = 0.70
    p_cruise_prop = cruise_power(
        weight_mars=weight_n,
        rho=rho,
        velocity=cruise_speed,
        wing_area=wing_area,
        polar=polar,
        eta_prop=eta_prop,
    )

    # Hover power
    disk_area = n_rotors * math.pi * rotor_radius**2
    p_hover = hover_power(weight_n, disk_area, rho, figure_of_merit=0.60)

    # Total cruise power (with subsystems)
    power_budget = PowerBudget(
        p_propulsion=p_cruise_prop,
        p_avionics=15.0,
        p_payload=10.0,
        p_thermal=20.0,
        p_comms=8.0,
    )

    # Endurance calculation
    calc = EnduranceCalculator(
        battery_capacity_wh=battery_wh,
        battery_efficiency=0.95,
        reserve_fraction=0.20,
        thermal_penalty=0.10,
    )

    endurance_h, breakdown = calc.endurance_battery_only(
        cruise_power=power_budget.total,
        hover_power=p_hover,
        hover_time_s=120.0,
        transition_power=600.0,
        transition_time_s=60.0,
    )

    # Range and radius
    range_km = calc.range_from_endurance(endurance_h, cruise_speed)
    radius_km = calc.operational_radius(endurance_h, cruise_speed, loiter_fraction=0.10)

    # Weight breakdown
    mass_breakdown = WeightEstimation.configuration_a_breakdown(mtow_target=mtow)

    results = PerformanceResults(
        config=config,
        weight_n=weight_n,
        rho=rho,
        reynolds=re,
        mach=mach,
        cl_cruise=cl_cruise,
        cd_cruise=cd_cruise,
        ld_ratio=ld_ratio,
        cruise_power_w=p_cruise_prop,
        hover_power_w=p_hover,
        total_power_cruise_w=power_budget.total,
        endurance_h=endurance_h,
        range_km=range_km,
        operational_radius_km=radius_km,
        mass_breakdown=mass_breakdown,
    )

    # Print results
    print(f"\nGeometry:")
    print(f"  Wing span:        {wing_span:.2f} m")
    print(f"  Wing area:        {wing_area:.2f} m²")
    print(f"  Aspect ratio:     {aspect_ratio:.1f}")
    print(f"  Chord:            {chord:.2f} m")
    print(f"  Rotor disk area:  {disk_area:.2f} m²")

    print(f"\nFlight Conditions:")
    print(f"  Cruise speed:     {cruise_speed:.0f} m/s")
    print(f"  Air density:      {rho:.5f} kg/m³")
    print(f"  Reynolds number:  {re:.0f} ({re/1000:.1f}k)")
    print(f"  Mach number:      {mach:.3f}")

    print(f"\nAerodynamics:")
    print(f"  CL cruise:        {cl_cruise:.3f}")
    print(f"  CD cruise:        {cd_cruise:.4f}")
    print(f"  L/D:              {ld_ratio:.1f}")

    print(f"\nPower:")
    print(f"  Cruise propulsion:{p_cruise_prop:.0f} W")
    print(f"  Total cruise:     {power_budget.total:.0f} W")
    print(f"  Hover power:      {p_hover:.0f} W")

    print(f"\nPerformance:")
    print(f"  Endurance:        {endurance_h:.2f} h ({endurance_h*60:.0f} min)")
    print(f"  Range:            {range_km:.0f} km")
    print(f"  Op. radius:       {radius_km:.0f} km")

    print(f"\n{mass_breakdown.summary()}")

    return config, results


def size_configuration_b() -> Tuple[UAVConfiguration, PerformanceResults]:
    """
    Size Configuration B: 24 kg solar-augmented extended endurance.

    Key design choices:
    - Larger platform for extended operations
    - Solar array (6 m²) on wing upper surface
    - Lower aspect ratio (AR=6) for structural margin
    - 4 large lift rotors for hover
    """
    print("\n" + "=" * 60)
    print("CONFIGURATION B: 24 kg Solar-Augmented Extended Endurance")
    print("=" * 60)

    # Design parameters
    mtow = 24.0  # kg
    payload = 2.5  # kg (camera + spectrometer)
    battery_wh = 300  # Wh (smaller, solar-supplemented)
    solar_area = 6.0  # m²
    solar_eff = 0.30  # Triple-junction GaAs

    # Wing geometry (lower AR for structure, solar accommodation)
    aspect_ratio = 6.0
    wing_area = 7.0  # m²
    wing_span = math.sqrt(aspect_ratio * wing_area)  # 6.48 m
    chord = wing_area / wing_span  # 1.08 m

    # Flight conditions
    cruise_speed = 35.0  # m/s (slower for efficiency)
    cruise_alt_km = ARCADIA_ELEVATION + 0.5

    # Rotor configuration (4 larger rotors)
    n_rotors = 4
    rotor_radius = 0.75  # m

    config = UAVConfiguration(
        name="Configuration B",
        mtow=mtow,
        payload_mass=payload,
        wing_span=wing_span,
        wing_area=wing_area,
        aspect_ratio=aspect_ratio,
        chord=chord,
        cruise_speed=cruise_speed,
        cruise_altitude_km=cruise_alt_km,
        n_lift_rotors=n_rotors,
        rotor_radius=rotor_radius,
        battery_capacity_wh=battery_wh,
        solar_area=solar_area,
        solar_efficiency=solar_eff,
    )

    # Atmospheric conditions
    atm = MarsAtmosphere.arcadia_planitia()
    state = atm.get_state(cruise_alt_km)
    rho = state.density
    mu = state.viscosity

    # Weight
    weight_n = mtow * G_MARS

    # Aerodynamics
    re = calculate_reynolds(cruise_speed, chord, rho, mu)
    mach = cruise_speed / state.speed_of_sound

    # Drag polar
    cd0 = 0.030  # Higher due to solar panel surface
    oswald = 0.75
    polar = DragPolar(cd0=cd0, aspect_ratio=aspect_ratio, oswald_efficiency=oswald)

    # Cruise CL
    cl_cruise = (2.0 * weight_n) / (rho * cruise_speed**2 * wing_area)

    # Cruise CD
    cd_cruise = polar.cd(cl_cruise)

    # L/D
    ld_ratio = cl_cruise / cd_cruise

    # Cruise power
    eta_prop = 0.70
    p_cruise_prop = cruise_power(
        weight_mars=weight_n,
        rho=rho,
        velocity=cruise_speed,
        wing_area=wing_area,
        polar=polar,
        eta_prop=eta_prop,
    )

    # Hover power
    disk_area = n_rotors * math.pi * rotor_radius**2
    p_hover = hover_power(weight_n, disk_area, rho, figure_of_merit=0.60)

    # Solar power
    p_solar = solar_power_available(
        array_area_m2=solar_area,
        cell_efficiency=solar_eff,
        incidence_factor=0.7,
        dust_factor=0.9,
    )

    # Total cruise power
    power_budget = PowerBudget(
        p_propulsion=p_cruise_prop,
        p_avionics=20.0,
        p_payload=25.0,
        p_thermal=30.0,
        p_comms=15.0,
    )

    # Endurance calculation
    calc = EnduranceCalculator(
        battery_capacity_wh=battery_wh,
        battery_efficiency=0.95,
        reserve_fraction=0.15,
        thermal_penalty=0.10,
    )

    endurance_h, breakdown = calc.endurance_solar_augmented(
        cruise_power=power_budget.total,
        solar_power=p_solar,
        hover_power=p_hover,
        hover_time_s=120.0,
        transition_power=800.0,
        transition_time_s=60.0,
        solar_availability=0.80,
    )

    # Range and radius
    range_km = calc.range_from_endurance(endurance_h, cruise_speed)
    radius_km = calc.operational_radius(endurance_h, cruise_speed, loiter_fraction=0.10)

    # Weight breakdown
    mass_breakdown = WeightEstimation.configuration_b_breakdown(mtow_target=mtow)

    results = PerformanceResults(
        config=config,
        weight_n=weight_n,
        rho=rho,
        reynolds=re,
        mach=mach,
        cl_cruise=cl_cruise,
        cd_cruise=cd_cruise,
        ld_ratio=ld_ratio,
        cruise_power_w=p_cruise_prop,
        hover_power_w=p_hover,
        total_power_cruise_w=power_budget.total,
        endurance_h=endurance_h,
        range_km=range_km,
        operational_radius_km=radius_km,
        mass_breakdown=mass_breakdown,
    )

    # Print results
    print(f"\nGeometry:")
    print(f"  Wing span:        {wing_span:.2f} m")
    print(f"  Wing area:        {wing_area:.2f} m²")
    print(f"  Aspect ratio:     {aspect_ratio:.1f}")
    print(f"  Chord:            {chord:.2f} m")
    print(f"  Solar area:       {solar_area:.1f} m²")
    print(f"  Rotor disk area:  {disk_area:.2f} m²")

    print(f"\nFlight Conditions:")
    print(f"  Cruise speed:     {cruise_speed:.0f} m/s")
    print(f"  Air density:      {rho:.5f} kg/m³")
    print(f"  Reynolds number:  {re:.0f} ({re/1000:.1f}k)")
    print(f"  Mach number:      {mach:.3f}")

    print(f"\nAerodynamics:")
    print(f"  CL cruise:        {cl_cruise:.3f}")
    print(f"  CD cruise:        {cd_cruise:.4f}")
    print(f"  L/D:              {ld_ratio:.1f}")

    print(f"\nPower:")
    print(f"  Cruise propulsion:{p_cruise_prop:.0f} W")
    print(f"  Total cruise:     {power_budget.total:.0f} W")
    print(f"  Solar power:      {p_solar:.0f} W")
    print(f"  Net from battery: {power_budget.total - p_solar * 0.8:.0f} W")
    print(f"  Hover power:      {p_hover:.0f} W")

    print(f"\nPerformance:")
    print(f"  Endurance:        {endurance_h:.2f} h ({endurance_h*60:.0f} min)")
    print(f"  Range:            {range_km:.0f} km")
    print(f"  Op. radius:       {radius_km:.0f} km")

    print(f"\n{mass_breakdown.summary()}")

    return config, results


def print_comparison_table(
    results_a: PerformanceResults,
    results_b: PerformanceResults,
) -> str:
    """Generate comparison table for both configurations."""
    lines = [
        "",
        "=" * 70,
        "CONFIGURATION COMPARISON",
        "=" * 70,
        "",
        f"{'Parameter':<30} {'Config A':>18} {'Config B':>18}",
        "-" * 70,
        f"{'MTOW (kg)':<30} {results_a.config.mtow:>18.1f} {results_b.config.mtow:>18.1f}",
        f"{'Payload (kg)':<30} {results_a.config.payload_mass:>18.1f} {results_b.config.payload_mass:>18.1f}",
        f"{'Wing span (m)':<30} {results_a.config.wing_span:>18.2f} {results_b.config.wing_span:>18.2f}",
        f"{'Wing area (m²)':<30} {results_a.config.wing_area:>18.2f} {results_b.config.wing_area:>18.2f}",
        f"{'Aspect ratio':<30} {results_a.config.aspect_ratio:>18.1f} {results_b.config.aspect_ratio:>18.1f}",
        f"{'Cruise speed (m/s)':<30} {results_a.config.cruise_speed:>18.0f} {results_b.config.cruise_speed:>18.0f}",
        "-" * 70,
        f"{'Reynolds number':<30} {results_a.reynolds:>18,.0f} {results_b.reynolds:>18,.0f}",
        f"{'Mach number':<30} {results_a.mach:>18.3f} {results_b.mach:>18.3f}",
        f"{'CL cruise':<30} {results_a.cl_cruise:>18.3f} {results_b.cl_cruise:>18.3f}",
        f"{'L/D':<30} {results_a.ld_ratio:>18.1f} {results_b.ld_ratio:>18.1f}",
        "-" * 70,
        f"{'Cruise power (W)':<30} {results_a.cruise_power_w:>18.0f} {results_b.cruise_power_w:>18.0f}",
        f"{'Total cruise power (W)':<30} {results_a.total_power_cruise_w:>18.0f} {results_b.total_power_cruise_w:>18.0f}",
        f"{'Hover power (W)':<30} {results_a.hover_power_w:>18.0f} {results_b.hover_power_w:>18.0f}",
        f"{'Battery (Wh)':<30} {results_a.config.battery_capacity_wh:>18.0f} {results_b.config.battery_capacity_wh:>18.0f}",
        f"{'Solar area (m²)':<30} {results_a.config.solar_area:>18.1f} {results_b.config.solar_area:>18.1f}",
        "-" * 70,
        f"{'Endurance (min)':<30} {results_a.endurance_h * 60:>18.0f} {results_b.endurance_h * 60:>18.0f}",
        f"{'Range (km)':<30} {results_a.range_km:>18.0f} {results_b.range_km:>18.0f}",
        f"{'Op. radius (km)':<30} {results_a.operational_radius_km:>18.0f} {results_b.operational_radius_km:>18.0f}",
        "=" * 70,
    ]
    return "\n".join(lines)


def run_xfoil_analysis(output_dir: Path) -> Optional[Dict]:
    """Run XFOIL airfoil analysis if available."""
    try:
        from .xfoil_wrapper import compare_airfoils_mars, print_comparison_table

        print("\n" + "=" * 60)
        print("XFOIL AIRFOIL ANALYSIS")
        print("=" * 60)

        # Mars Reynolds numbers
        reynolds_numbers = [35000, 50000, 75000]
        airfoils = ["e387", "s1223", "s7055", "NACA 0012"]

        print(f"\nAnalyzing airfoils: {airfoils}")
        print(f"Reynolds numbers: {reynolds_numbers}")

        results = compare_airfoils_mars(
            airfoils=airfoils,
            reynolds_numbers=reynolds_numbers,
            output_dir=str(output_dir / "airfoil_polars"),
        )

        print("\n" + print_comparison_table(results))
        return results

    except FileNotFoundError as e:
        print(f"\nXFOIL not available: {e}")
        print("Skipping airfoil analysis. Using literature values.")
        return None
    except Exception as e:
        print(f"\nXFOIL analysis failed: {e}")
        return None


def main():
    """Main entry point for Mars UAV sizing."""
    print("=" * 70)
    print("MARS UAV SIZING ANALYSIS")
    print("=" * 70)
    print("\nThis script performs complete sizing analysis for two Mars UAV")
    print("configurations, comparing battery-only and solar-augmented designs.")

    # Set up output directory
    output_dir = Path(__file__).parent.parent.parent / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Atmospheric conditions summary
    print("\n" + "-" * 60)
    print("OPERATING ENVIRONMENT: Arcadia Planitia")
    print("-" * 60)
    state = analyze_atmosphere()
    print(f"  Elevation:          {ARCADIA_ELEVATION:.1f} km (below datum)")
    print(f"  Temperature:        {state.temperature:.1f} K")
    print(f"  Pressure:           {state.pressure:.1f} Pa ({state.pressure/100:.2f} mbar)")
    print(f"  Density:            {state.density:.5f} kg/m³")
    print(f"  Speed of sound:     {state.speed_of_sound:.1f} m/s")

    # Run XFOIL analysis
    xfoil_results = run_xfoil_analysis(output_dir)

    # Size both configurations
    config_a, results_a = size_configuration_a()
    config_b, results_b = size_configuration_b()

    # Print comparison
    comparison = print_comparison_table(results_a, results_b)
    print(comparison)

    # Generate figures
    try:
        from .plotting import generate_all_figures
        print("\nGenerating figures...")
        generate_all_figures(str(output_dir))
    except ImportError as e:
        print(f"\nPlotting unavailable: {e}")

    # Save results to file
    results_file = output_dir.parent / "sizing_results.txt"
    with open(results_file, "w", encoding="utf-8") as f:
        f.write("Mars UAV Sizing Results\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Generated by: mars_uav_sizing\n\n")

        f.write("CONFIGURATION A: 7.5 kg Battery-Only\n")
        f.write("-" * 40 + "\n")
        f.write(results_a.mass_breakdown.summary() + "\n\n")

        f.write("CONFIGURATION B: 24 kg Solar-Augmented\n")
        f.write("-" * 40 + "\n")
        f.write(results_b.mass_breakdown.summary() + "\n\n")

        f.write(comparison + "\n")

    print(f"\nResults saved to: {results_file}")
    print("\nSizing analysis complete.")


if __name__ == "__main__":
    main()
