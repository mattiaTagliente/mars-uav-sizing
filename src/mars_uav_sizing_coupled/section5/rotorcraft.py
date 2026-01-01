"""
Rotorcraft Configuration Analysis (Coupled)
===========================================

Implements equations from manuscript Section 5.1 (Rotorcraft Configuration).
All parameters loaded from configuration and coupled sizing results.
"""

import math
from typing import Dict, Any
from datetime import datetime

from ..config import (
    get_mars_gravity,
    get_density,
    get_propulsion_efficiencies,
    get_battery_params,
    get_mission_params,
    get_aerodynamic_params,
    get_param,
)

from .coupled_solver import get_coupled_solution

from mars_uav_sizing.section5.rotorcraft import (
    induced_velocity,
    induced_velocity_from_disk_loading,
    ideal_hover_power,
    actual_hover_power,
    electric_hover_power,
    hover_power_loading,
    forward_flight_power,
    electric_forward_flight_power,
    rotorcraft_endurance_seconds,
)


# =============================================================================
# FEASIBILITY ANALYSIS (Section 5.1)
# =============================================================================

def rotorcraft_feasibility_analysis() -> Dict[str, Any]:
    """
    Complete rotorcraft feasibility analysis with coupled sizing inputs.
    """
    solver = get_coupled_solution()
    solution = solver["solution"]

    g_mars = get_mars_gravity()
    rho = get_density()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    endurance_req = get_param("mission.requirements.endurance_min")

    mtow_kg = solution["mtow_kg"]
    battery_mass_kg = solution["battery_mass_kg"]

    weight_n = mtow_kg * g_mars
    disk_area_m2 = weight_n / disk_loading
    v_cruise = mission["v_cruise"]
    hover_time_s = mission["t_hover_s"]
    reserve_fraction = mission["energy_reserve"]

    # Hover power
    p_hover_elec = electric_hover_power(
        weight_n,
        rho,
        disk_area_m2,
        prop["figure_of_merit"],
        prop["eta_motor"],
        prop["eta_esc"],
    )

    # Forward flight power
    p_cruise_elec = electric_forward_flight_power(
        weight_n,
        v_cruise,
        aero["ld_eff_rotorcraft"],
        prop["eta_motor"],
        prop["eta_esc"],
    )

    # Battery energy
    total_energy_wh = battery_mass_kg * batt["e_spec_Wh_kg"]
    usable_energy_wh = total_energy_wh * batt["dod"] * batt["eta_discharge"]
    energy_after_reserve = usable_energy_wh * (1 - reserve_fraction)

    # Hover energy
    hover_energy_wh = p_hover_elec * (hover_time_s / 3600)

    # Remaining for cruise
    cruise_energy_wh = energy_after_reserve - hover_energy_wh

    # Cruise time and endurance
    if cruise_energy_wh > 0:
        cruise_time_s = (cruise_energy_wh / p_cruise_elec) * 3600
        cruise_time_min = cruise_time_s / 60
    else:
        cruise_time_s = 0
        cruise_time_min = 0

    total_endurance_min = (hover_time_s / 60) + cruise_time_min

    # Range
    range_km = (v_cruise * cruise_time_s) / 1000

    # Feasibility
    feasible = total_endurance_min >= endurance_req
    margin_percent = ((total_endurance_min / endurance_req) - 1) * 100

    # Induced velocity for reference
    v_i = induced_velocity(weight_n, rho, disk_area_m2)

    # Combined efficiencies
    eta_hover = prop["figure_of_merit"] * prop["eta_motor"] * prop["eta_esc"]
    eta_cruise = prop["eta_motor"] * prop["eta_esc"]

    f_batt_actual = battery_mass_kg / mtow_kg if mtow_kg > 0 else 0.0

    return {
        "solver": solver,
        # Input parameters
        "mtow_kg": mtow_kg,
        "weight_n": weight_n,
        "disk_loading_n_m2": disk_loading,
        "disk_area_m2": disk_area_m2,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        # Propulsion efficiencies
        "figure_of_merit": prop["figure_of_merit"],
        "eta_motor": prop["eta_motor"],
        "eta_esc": prop["eta_esc"],
        "eta_hover": eta_hover,
        "eta_cruise": eta_cruise,
        "ld_effective": aero["ld_eff_rotorcraft"],
        # Power calculations
        "induced_velocity_m_s": v_i,
        "hover_power_w": p_hover_elec,
        "cruise_power_w": p_cruise_elec,
        "power_loading_w_per_n": p_hover_elec / weight_n,
        "power_loading_w_per_kg": p_hover_elec / mtow_kg,
        # Energy calculations
        "battery_mass_kg": battery_mass_kg,
        "battery_fraction_actual": f_batt_actual,
        "total_energy_wh": total_energy_wh,
        "usable_energy_wh": usable_energy_wh,
        "energy_after_reserve_wh": energy_after_reserve,
        "hover_energy_wh": hover_energy_wh,
        "cruise_energy_wh": cruise_energy_wh,
        # Performance
        "hover_time_min": hover_time_s / 60,
        "cruise_time_min": cruise_time_min,
        "endurance_min": total_endurance_min,
        "range_km": range_km,
        # Assessment
        "requirement_min": endurance_req,
        "feasible": feasible,
        "margin_percent": margin_percent,
    }


# =============================================================================
# OUTPUT
# =============================================================================

def print_analysis(results: Dict[str, Any] = None) -> None:
    if results is None:
        results = rotorcraft_feasibility_analysis()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("ROTORCRAFT FEASIBILITY ANALYSIS (Section 5.1) - COUPLED")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print("Config:   All values loaded from config/ YAML files")
    print()

    solver = results.get("solver")
    if solver:
        print("COUPLED SOLVER")
        print("-" * 50)
        print(f"  Converged:          {solver['converged']}")
        print(f"  Iterations:         {solver['iterations']}")
        print(f"  Message:            {solver['message']}")
        print()

    print("INPUT PARAMETERS (from configuration)")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Mars gravity:       {get_mars_gravity():.3f} m/s^2")
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Disk loading:       {results['disk_loading_n_m2']:.1f} N/m^2")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m^3")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print(f"  Battery mass:       {results['battery_mass_kg']:.2f} kg")
    print(f"  Battery fraction:   {results['battery_fraction_actual']:.2f}")
    print()

    print("PROPULSION EFFICIENCIES (from Section 4.5)")
    print("-" * 50)
    print(f"  Figure of Merit:    {results['figure_of_merit']:.2f}")
    print(f"  Motor efficiency:   {results['eta_motor']:.2f}")
    print(f"  ESC efficiency:     {results['eta_esc']:.2f}")
    print(f"  Combined eta_hover: {results['eta_hover']:.4f}")
    print(f"  Equivalent L/D:     {results['ld_effective']:.1f}")
    print()

    print("HOVER ANALYSIS (@eq:hover-power)")
    print("-" * 50)
    print(f"  Disk area:          {results['disk_area_m2']:.3f} m^2")
    print(f"  Induced velocity:   {results['induced_velocity_m_s']:.2f} m/s")
    print(f"  Electrical power:   {results['hover_power_w']:.0f} W")
    print(f"  Power loading:      {results['power_loading_w_per_kg']:.0f} W/kg")
    print()

    print("FORWARD FLIGHT ANALYSIS (@eq:forward-power-ld)")
    print("-" * 50)
    print(f"  Cruise power:       {results['cruise_power_w']:.1f} W")
    print()

    print("ENERGY BUDGET")
    print("-" * 50)
    print(f"  Total capacity:     {results['total_energy_wh']:.1f} Wh")
    print(f"  Usable (after DoD): {results['usable_energy_wh']:.1f} Wh")
    print(f"  After reserve:      {results['energy_after_reserve_wh']:.1f} Wh")
    print(f"  Hover energy:       {results['hover_energy_wh']:.1f} Wh ({results['hover_time_min']:.0f} min)")
    print(f"  Cruise energy:      {results['cruise_energy_wh']:.1f} Wh")
    print()

    print("PERFORMANCE")
    print("-" * 50)
    print(f"  Cruise time:        {results['cruise_time_min']:.1f} min")
    print(f"  Total endurance:    {results['endurance_min']:.1f} min")
    print(f"  Range:              {results['range_km']:.0f} km")
    print()

    print("FEASIBILITY ASSESSMENT")
    print("-" * 50)
    status = "[PASS]" if results["feasible"] else "[FAIL]"
    print(f"  Requirement:        {results['requirement_min']:.0f} min endurance")
    print(f"  Achieved:           {results['endurance_min']:.1f} min")
    print(f"  Margin:             {results['margin_percent']:+.1f}%")
    print(f"  Status:             {status}")
    print()

    if not results["feasible"]:
        print("CONCLUSION: Pure rotorcraft configuration FAILS endurance requirement.")
        print(f"           Deficit of {abs(results['margin_percent']):.1f}% is unacceptable for Mars mission.")
    elif results["margin_percent"] < 10:
        print("CONCLUSION: Rotorcraft marginally meets requirement.")
        print(f"           Margin of only {results['margin_percent']:.1f}% is insufficient for Mars operations.")
    else:
        print(f"CONCLUSION: Rotorcraft meets requirement with {results['margin_percent']:.1f}% margin.")

    print("=" * 80)


if __name__ == "__main__":
    print_analysis()

    print()
    print("=" * 80)
    print("THEORETICAL ENDURANCE CHECK (@eq:endurance-simple)")
    print("=" * 80)
    t_endurance_s = rotorcraft_endurance_seconds()
    t_endurance_min = t_endurance_s / 60
    print(f"Theoretical cruise endurance (MTOW-independent): {t_endurance_min:.1f} min")
    print("Note: This assumes 100% forward flight (no hover phases)")
    print("=" * 80)
