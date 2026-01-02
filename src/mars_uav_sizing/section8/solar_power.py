#!/usr/bin/env python3
"""
Solar Power System Sizing for Mars UAV Charging Infrastructure
================================================================

Calculates solar panel area, buffer battery capacity, and daily energy
balance for the habitat-integrated UAV charging system.

Key design decision: Buffer battery uses the SAME battery technology as
the UAV (solid-state Li-ion, 270 Wh/kg) to simplify logistics, enable
parts commonality, and ensure Mars temperature compatibility.

Reference: Manuscript Section 8.1.4 - Solar Power System
Last Updated: 2026-01-02
"""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from ..config import get_param


@dataclass
class SolarIrradianceParams:
    """Mars solar irradiance parameters."""
    solar_constant_W_m2: float  # At Mars orbit (1.52 AU)
    perihelion_W_m2: float      # Closest approach
    aphelion_W_m2: float        # Farthest point
    surface_clear_W_m2: float   # Clear day at noon (NOT for design)
    design_irradiance_W_m2: float  # Aphelion + dust (for sizing)
    effective_sun_hours: float  # Usable daylight hours per sol
    avg_incidence_factor: float # Cosine losses for fixed-tilt


@dataclass 
class SolarPanelSizing:
    """Solar panel sizing results."""
    cell_efficiency: float      # Decimal (e.g., 0.33)
    surface_irradiance_W_m2: float
    peak_power_W_m2: float      # W/m² at noon
    daily_energy_Wh_m2: float   # Wh/m²/sol
    energy_required_Wh: float   # Per charge cycle
    panel_area_min_m2: float    # Minimum required
    design_margin: float        # For dust/degradation
    panel_area_design_m2: float # With margin
    panel_mass_kg: float        # Total mass


@dataclass
class BufferBatterySizing:
    """Buffer battery sizing results."""
    uav_battery_capacity_Wh: float    # From UAV specs
    energy_per_charge_Wh: float       # At 80% DoD
    charger_efficiency: float         # Decimal
    energy_from_buffer_Wh: float      # Required from buffer
    night_reserve_factor: float       # For overnight charging
    buffer_capacity_Wh: float         # Total capacity
    battery_energy_density_Wh_kg: float  # Same as UAV
    buffer_mass_kg: float             # Total mass
    rationale: str                    # Design decision rationale


@dataclass
class ChargingInfrastructure:
    """Charging infrastructure specifications."""
    uav_battery_capacity_Wh: float
    energy_to_replenish_Wh: float  # 20% to 100%
    target_charge_time_h: float
    charger_power_0_5C_W: float    # At 0.5C rate
    charger_power_1C_W: float       # At 1C rate
    specified_charger_W: float      # Selected value


@dataclass
class SolarSystemSpecs:
    """Complete solar power system specifications."""
    # Solar cells
    cell_technology: str
    cell_efficiency_pct: float
    cell_mass_kg_m2: float
    # Panel
    panel_area_m2: float
    peak_power_W: float
    daily_energy_Wh: float
    panel_mass_kg: float
    # Buffer battery
    buffer_capacity_Wh: float
    buffer_mass_kg: float
    buffer_technology: str
    # Mounting
    mounting: str
    # Daily balance
    excess_energy_Wh: float


def get_solar_irradiance_params() -> SolarIrradianceParams:
    """
    Get Mars solar irradiance parameters from configuration.
    
    Returns
    -------
    SolarIrradianceParams
        Solar irradiance parameters for Mars.
    """
    # Load from config/mars_environment.yaml (under 'environment' key)
    solar_constant = get_param('environment.solar.constant_mars')
    perihelion = get_param('environment.solar.perihelion')
    aphelion = get_param('environment.solar.aphelion')
    surface_clear = get_param('environment.solar.surface_clear_noon')
    design_irradiance = get_param('environment.solar.surface_aphelion_dusty')
    effective_sun_hours = get_param('environment.solar.effective_sun_hours')
    avg_incidence_factor = get_param('environment.solar.avg_incidence_factor')
    
    return SolarIrradianceParams(
        solar_constant_W_m2=solar_constant,
        perihelion_W_m2=perihelion,
        aphelion_W_m2=aphelion,
        surface_clear_W_m2=surface_clear,
        design_irradiance_W_m2=design_irradiance,
        effective_sun_hours=effective_sun_hours,
        avg_incidence_factor=avg_incidence_factor,
    )


def get_solar_panel_sizing() -> SolarPanelSizing:
    """
    Calculate solar panel area for UAV charging.
    
    Uses SolAero IMM-α cells (33% efficiency, 0.49 kg/m²).
    
    DESIGN PHILOSOPHY: Panel sizing uses WORST-CASE conditions (aphelion + 
    typical dust, 350 W/m²) rather than optimistic clear-sky noon values 
    (500 W/m²). This ensures the system can provide adequate charging 
    throughout the Martian year, including during winter and dusty periods.
    
    Design margin of 1.5× added for cell degradation and operational margin.
    
    Returns
    -------
    SolarPanelSizing
        Solar panel sizing results.
    """
    # Solar cell parameters (SolAero IMM-α selected)
    cell_efficiency = 0.33  # 33% BOL efficiency
    cell_mass_kg_m2 = 0.49  # 49 mg/cm² = 0.49 kg/m²
    
    # Irradiance parameters - use DESIGN (worst-case) value, not clear-sky
    irradiance = get_solar_irradiance_params()
    surface_irradiance = irradiance.design_irradiance_W_m2  # Aphelion + dust
    
    # Peak power per unit area (at design irradiance)
    # P_peak = η_cell × I_design
    peak_power_W_m2 = cell_efficiency * surface_irradiance
    
    # Daily energy yield per unit area
    # E_panel = P_peak × t_sun × cos(θ_avg)
    daily_energy_Wh_m2 = (peak_power_W_m2 * 
                          irradiance.effective_sun_hours * 
                          irradiance.avg_incidence_factor)
    
    # Energy requirement per charge cycle
    # Get UAV battery specs
    batt_capacity = get_uav_battery_capacity_Wh()
    depth_of_discharge = get_param('battery.utilization.depth_of_discharge')
    charger_efficiency = 0.90  # Typical charger efficiency
    
    # Energy to replenish = capacity × DoD
    energy_per_charge = batt_capacity * depth_of_discharge
    
    # Energy required from solar (accounting for charger losses)
    energy_required = energy_per_charge / charger_efficiency
    
    # Minimum panel area
    panel_area_min = energy_required / daily_energy_Wh_m2
    
    # Design margin for cell degradation and operational margin
    # Sizing basis already uses worst-case (aphelion + dust) irradiance
    # 1.5x margin ensures daily generation comfortably exceeds buffer capacity
    design_margin = 1.5
    panel_area_design = panel_area_min * design_margin
    
    # Round UP to practical value (0.5 m² increments)
    import math
    panel_area_design = math.ceil(panel_area_design * 2) / 2
    
    # Panel mass (cells only, mounting structure separate)
    panel_mass = panel_area_design * cell_mass_kg_m2
    
    return SolarPanelSizing(
        cell_efficiency=cell_efficiency,
        surface_irradiance_W_m2=surface_irradiance,
        peak_power_W_m2=peak_power_W_m2,
        daily_energy_Wh_m2=daily_energy_Wh_m2,
        energy_required_Wh=energy_required,
        panel_area_min_m2=panel_area_min,
        design_margin=design_margin,
        panel_area_design_m2=panel_area_design,
        panel_mass_kg=panel_mass,
    )


def get_uav_battery_capacity_Wh() -> float:
    """
    Get UAV battery capacity from config.
    
    Returns
    -------
    float
        UAV battery capacity in Wh.
    """
    # From mission parameters: battery mass = f_battery × MTOW
    mtow = get_param('mission.mass.mtow_kg')
    f_battery = get_param('mission.mass_fractions.f_battery')
    battery_mass = f_battery * mtow
    
    # From battery parameters: specific energy
    specific_energy = get_param('battery.specifications.specific_energy_Wh_kg')
    
    # Total capacity
    capacity_Wh = battery_mass * specific_energy
    
    return capacity_Wh


def get_buffer_battery_sizing() -> BufferBatterySizing:
    """
    Calculate buffer battery capacity for solar energy storage.
    
    DESIGN DECISION: Buffer battery uses the SAME battery technology as
    the UAV (solid-state Li-ion at 270 Wh/kg) rather than generic Li-ion
    (180 Wh/kg). This provides:
    
    1. Logistics simplification: Same battery chemistry means shared
       spares, charging equipment, and handling procedures
    2. Proven Mars compatibility: CGBT solid-state battery already 
       selected for Mars conditions (-20 to +60°C operating range)
    3. Mass reduction: 270 vs 180 Wh/kg reduces buffer mass by 33%
    4. Operational flexibility: UAV battery packs can serve as buffer
       spares if needed
    
    Returns
    -------
    BufferBatterySizing
        Buffer battery sizing results.
    """
    # UAV battery specs
    batt_capacity = get_uav_battery_capacity_Wh()
    depth_of_discharge = get_param('battery.utilization.depth_of_discharge')
    
    # Energy per charge cycle
    energy_per_charge = batt_capacity * depth_of_discharge
    
    # Charger efficiency
    charger_efficiency = 0.90
    
    # Energy required from buffer
    energy_from_buffer = energy_per_charge / charger_efficiency
    
    # Night reserve factor (allows one overnight charge + margin)
    night_reserve_factor = 1.5
    
    # Buffer capacity
    buffer_capacity = energy_from_buffer * night_reserve_factor
    
    # DESIGN DECISION: Use same battery technology as UAV
    # UAV uses solid-state Li-ion at 270 Wh/kg
    battery_energy_density = get_param('battery.specifications.specific_energy_Wh_kg')
    
    # Buffer mass
    buffer_mass = buffer_capacity / battery_energy_density
    
    rationale = (
        "Same battery technology as UAV (solid-state Li-ion, 270 Wh/kg) "
        "selected for logistics simplification, Mars temperature compatibility "
        "(-20 to +60°C), and parts commonality. UAV battery packs can serve "
        "as buffer spares, enabling battery rotation to even out cycle wear."
    )
    
    return BufferBatterySizing(
        uav_battery_capacity_Wh=batt_capacity,
        energy_per_charge_Wh=energy_per_charge,
        charger_efficiency=charger_efficiency,
        energy_from_buffer_Wh=energy_from_buffer,
        night_reserve_factor=night_reserve_factor,
        buffer_capacity_Wh=buffer_capacity,
        battery_energy_density_Wh_kg=battery_energy_density,
        buffer_mass_kg=buffer_mass,
        rationale=rationale,
    )


def get_charging_infrastructure() -> ChargingInfrastructure:
    """
    Calculate charging infrastructure specifications.
    
    Returns
    -------
    ChargingInfrastructure
        Charging infrastructure specifications.
    """
    # UAV battery specs
    batt_capacity = get_uav_battery_capacity_Wh()
    depth_of_discharge = get_param('battery.utilization.depth_of_discharge')
    
    # Energy to replenish (20% to 100%)
    energy_to_replenish = batt_capacity * depth_of_discharge
    
    # Target charge time
    target_charge_time_h = 2.0  # 2-3 hours
    
    # Charger power at different C-rates
    charger_power_0_5C = batt_capacity * 0.5  # 0.5C rate
    charger_power_1C = batt_capacity * 1.0    # 1C rate
    
    # Specified charger (1000W for margin)
    specified_charger = 1000.0
    
    return ChargingInfrastructure(
        uav_battery_capacity_Wh=batt_capacity,
        energy_to_replenish_Wh=energy_to_replenish,
        target_charge_time_h=target_charge_time_h,
        charger_power_0_5C_W=charger_power_0_5C,
        charger_power_1C_W=charger_power_1C,
        specified_charger_W=specified_charger,
    )


def get_solar_system_specs() -> SolarSystemSpecs:
    """
    Get complete solar power system specifications.
    
    Returns
    -------
    SolarSystemSpecs
        Complete solar power system specifications.
    """
    panel = get_solar_panel_sizing()
    buffer = get_buffer_battery_sizing()
    
    # Peak power output
    peak_power = panel.panel_area_design_m2 * panel.peak_power_W_m2
    
    # Daily energy yield
    daily_energy = panel.panel_area_design_m2 * panel.daily_energy_Wh_m2
    
    # Excess energy (daily yield - buffer capacity)
    excess_energy = daily_energy - buffer.buffer_capacity_Wh
    
    return SolarSystemSpecs(
        cell_technology="SolAero IMM-α",
        cell_efficiency_pct=panel.cell_efficiency * 100,
        cell_mass_kg_m2=0.49,
        panel_area_m2=panel.panel_area_design_m2,
        peak_power_W=peak_power,
        daily_energy_Wh=daily_energy,
        panel_mass_kg=panel.panel_mass_kg,
        buffer_capacity_Wh=buffer.buffer_capacity_Wh,
        buffer_mass_kg=buffer.buffer_mass_kg,
        buffer_technology="Solid-state Li-ion (same as UAV)",
        mounting="Habitat roof, fixed tilt",
        excess_energy_Wh=excess_energy,
    )


def print_solar_power_analysis():
    """Print complete solar power system analysis for Section 8.1.4."""
    print("=" * 70)
    print("SOLAR POWER SYSTEM ANALYSIS (Section 8.1.4)")
    print("=" * 70)
    print(f"Computed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Config:   All values from config/ YAML files")
    
    # Irradiance parameters
    irrad = get_solar_irradiance_params()
    print("\nMARS SOLAR IRRADIANCE")
    print("-" * 50)
    print(f"  Solar constant at Mars orbit:    {irrad.solar_constant_W_m2:.0f} W/m²")
    print(f"  Perihelion irradiance:           {irrad.perihelion_W_m2:.0f} W/m²")
    print(f"  Aphelion irradiance:             {irrad.aphelion_W_m2:.0f} W/m²")
    print(f"  Clear-sky surface (noon):        {irrad.surface_clear_W_m2:.0f} W/m² (NOT for design)")
    print(f"  Design irradiance (aphelion+dust): {irrad.design_irradiance_W_m2:.0f} W/m² (SIZING BASIS)")
    print(f"  Effective sunlight hours:        {irrad.effective_sun_hours:.0f} h/sol")
    print(f"  Average incidence factor:        {irrad.avg_incidence_factor:.1f}")
    
    # Solar panel sizing
    panel = get_solar_panel_sizing()
    print("\nSOLAR PANEL SIZING (worst-case design)")
    print("-" * 50)
    print(f"  Cell technology:      SolAero IMM-α")
    print(f"  Cell efficiency:      {panel.cell_efficiency*100:.0f}%")
    print(f"  Design irradiance:    {panel.surface_irradiance_W_m2:.0f} W/m² (aphelion + typical dust)")
    print(f"  Peak power output:    P_peak = {panel.cell_efficiency:.2f} × {panel.surface_irradiance_W_m2:.0f} = {panel.peak_power_W_m2:.1f} W/m²")
    print(f"  Daily energy yield:   E_panel = {panel.peak_power_W_m2:.1f} × {irrad.effective_sun_hours:.0f} × {irrad.avg_incidence_factor:.1f} = {panel.daily_energy_Wh_m2:.1f} Wh/m²/sol")
    print(f"  Energy required:      {panel.energy_required_Wh:.0f} Wh (per charge cycle)")
    print(f"  Minimum panel area:   A = {panel.energy_required_Wh:.0f} / {panel.daily_energy_Wh_m2:.1f} = {panel.panel_area_min_m2:.2f} m²")
    print(f"  Design margin:        ×{panel.design_margin:.2f} (degradation only, dust in irradiance)")
    print(f"  Design panel area:    {panel.panel_area_min_m2:.2f} × {panel.design_margin:.2f} = {panel.panel_area_design_m2:.1f} m²")
    print(f"  Panel mass:           {panel.panel_area_design_m2:.1f} × 0.49 = {panel.panel_mass_kg:.2f} kg")
    
    # Buffer battery sizing
    buffer = get_buffer_battery_sizing()
    print("\nBUFFER BATTERY SIZING")
    print("-" * 50)
    print(f"  UAV battery capacity:     {buffer.uav_battery_capacity_Wh:.0f} Wh")
    print(f"  Energy per charge (80%):  {buffer.energy_per_charge_Wh:.0f} Wh")
    print(f"  Charger efficiency:       {buffer.charger_efficiency*100:.0f}%")
    print(f"  Energy from buffer:       {buffer.energy_per_charge_Wh:.0f} / {buffer.charger_efficiency:.2f} = {buffer.energy_from_buffer_Wh:.0f} Wh")
    print(f"  Night reserve factor:     ×{buffer.night_reserve_factor:.1f}")
    print(f"  Buffer capacity:          {buffer.energy_from_buffer_Wh:.0f} × {buffer.night_reserve_factor:.1f} = {buffer.buffer_capacity_Wh:.0f} Wh")
    print(f"  Battery energy density:   {buffer.battery_energy_density_Wh_kg:.0f} Wh/kg")
    print(f"  Buffer mass:              {buffer.buffer_capacity_Wh:.0f} / {buffer.battery_energy_density_Wh_kg:.0f} = {buffer.buffer_mass_kg:.2f} kg")
    
    print("\n  DESIGN DECISION:")
    print(f"  {buffer.rationale}")
    
    # Charging infrastructure
    charging = get_charging_infrastructure()
    print("\nCHARGING INFRASTRUCTURE")
    print("-" * 50)
    print(f"  UAV battery capacity:     {charging.uav_battery_capacity_Wh:.0f} Wh")
    print(f"  Energy to replenish:      {charging.energy_to_replenish_Wh:.0f} Wh (20% to 100%)")
    print(f"  Target charge time:       {charging.target_charge_time_h:.0f}–3 hours")
    print(f"  Charger power @ 0.5C:     {charging.charger_power_0_5C_W:.0f} W")
    print(f"  Charger power @ 1C:       {charging.charger_power_1C_W:.0f} W")
    print(f"  Specified charger:        {charging.specified_charger_W:.0f} W")
    
    # System summary
    specs = get_solar_system_specs()
    print("\nSOLAR SYSTEM SPECIFICATIONS SUMMARY")
    print("-" * 50)
    print(f"  Cell technology:          {specs.cell_technology}")
    print(f"  Cell efficiency:          {specs.cell_efficiency_pct:.0f}%")
    print(f"  Panel area:               {specs.panel_area_m2:.1f} m²")
    print(f"  Peak power output:        {specs.peak_power_W:.0f} W")
    print(f"  Daily energy yield:       {specs.daily_energy_Wh:.0f} Wh/sol")
    print(f"  Panel mass:               {specs.panel_mass_kg:.2f} kg")
    print(f"  Buffer capacity:          {specs.buffer_capacity_Wh:.0f} Wh")
    print(f"  Buffer mass:              {specs.buffer_mass_kg:.2f} kg")
    print(f"  Buffer technology:        {specs.buffer_technology}")
    print(f"  Mounting:                 {specs.mounting}")
    print(f"  Excess energy:            {specs.excess_energy_Wh:.0f} Wh/sol (to habitat grid)")
    
    # Daily balance example
    print("\nDAILY ENERGY BALANCE (typical sol)")
    print("-" * 50)
    print(f"  1. Daytime ({irrad.effective_sun_hours:.0f} h effective):")
    print(f"     Solar generation:      {specs.panel_area_m2:.1f} m² × {panel.daily_energy_Wh_m2:.0f} Wh/m² = {specs.daily_energy_Wh:.0f} Wh")
    print(f"  2. Buffer charging:")
    print(f"     Stored in buffer:      {specs.buffer_capacity_Wh:.0f} Wh")
    print(f"  3. UAV charging (2–3 h):")
    print(f"     Delivered to UAV:      {buffer.energy_from_buffer_Wh:.0f} Wh")
    print(f"     After charger losses:  {buffer.energy_per_charge_Wh:.0f} Wh stored")
    print(f"  4. Excess to habitat:")
    print(f"     {specs.daily_energy_Wh:.0f} - {specs.buffer_capacity_Wh:.0f} = {specs.excess_energy_Wh:.0f} Wh")
    
    print("=" * 70)


if __name__ == "__main__":
    print_solar_power_analysis()
