"""
Fixed-Wing Configuration Analysis (Coupled)
===========================================

Implements equations from manuscript Section 5.2 (Fixed-Wing Configuration).
All parameters loaded from configuration and coupled sizing results.
"""

import math
from typing import Dict, Any, Tuple
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

from mars_uav_sizing.section5.fixed_wing import (
    cruise_lift_coefficient,
    drag_coefficient,
    induced_drag_factor,
    lift_to_drag,
    maximum_ld,
    cruise_power,
    cruise_power_loading,
    stall_speed,
    stall_wing_loading_limit,
    fixed_wing_endurance_seconds,
    takeoff_ground_roll,
)


# =============================================================================
# FEASIBILITY ANALYSIS (Section 5.2)
# =============================================================================

def fixed_wing_feasibility_analysis() -> Dict[str, Any]:
    """
    Complete fixed-wing feasibility analysis with coupled sizing inputs.
    """
    solver = get_coupled_solution()
    solution = solver["solution"]

    g_mars = get_mars_gravity()
    rho = get_density()
    prop = get_propulsion_efficiencies()
    batt = get_battery_params()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    endurance_req = get_param("mission.requirements.endurance_min")

    mtow_kg = solution["mtow_kg"]
    battery_mass_kg = solution["battery_mass_kg"]

    weight_n = mtow_kg * g_mars
    v_cruise = mission["v_cruise"]

    # Aerodynamic calculations
    ld_max, cl_opt = maximum_ld()
    k = induced_drag_factor()

    # Wing loading at stall limit
    v_min = mission["v_stall"] * get_param("mission.velocity.v_min_factor")
    ws_max = stall_wing_loading_limit(rho, v_min, aero["cl_max"])

    # C_L at cruise
    cl_cruise = cruise_lift_coefficient(ws_max, rho, v_cruise)
    ld_cruise = lift_to_drag(cl_cruise)

    # Cruise power
    eta_cruise = prop["eta_prop"] * prop["eta_motor"] * prop["eta_esc"]
    p_cruise = cruise_power(weight_n, v_cruise, ld_max)

    # P/W ratio
    pw_cruise = cruise_power_loading(v_cruise, ld_max)

    # Endurance calculation
    reserve_fraction = mission["energy_reserve"]
    total_energy_wh = battery_mass_kg * batt["e_spec_Wh_kg"]
    usable_energy_wh = total_energy_wh * batt["dod"] * batt["eta_discharge"] * (1 - reserve_fraction)

    endurance_h = usable_energy_wh / p_cruise
    endurance_min = endurance_h * 60
    range_km = v_cruise * endurance_h * 3.6

    # Takeoff analysis (shows why fixed-wing is infeasible)
    takeoff_distance = takeoff_ground_roll(ws_max, rho, aero["cl_max"])
    v_stall = stall_speed(ws_max, rho, aero["cl_max"])

    # Feasibility (VTOL requirement)
    vtol_possible = False
    endurance_passes = endurance_min >= endurance_req

    f_batt_actual = battery_mass_kg / mtow_kg if mtow_kg > 0 else 0.0

    return {
        "solver": solver,
        # Input parameters
        "mtow_kg": mtow_kg,
        "weight_n": weight_n,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        # Aerodynamics
        "aspect_ratio": aero["aspect_ratio"],
        "oswald_e": aero["oswald_e"],
        "cd0": aero["cd0"],
        "cl_max": aero["cl_max"],
        "k_induced": k,
        "ld_max": ld_max,
        "cl_optimal": cl_opt,
        "cl_cruise": cl_cruise,
        "ld_cruise": ld_cruise,
        # Efficiencies
        "eta_prop": prop["eta_prop"],
        "eta_motor": prop["eta_motor"],
        "eta_esc": prop["eta_esc"],
        "eta_cruise": eta_cruise,
        # Stall and wing loading
        "wing_loading_max": ws_max,
        "v_stall": v_stall,
        # Power
        "cruise_power_w": p_cruise,
        "power_loading_w_per_n": pw_cruise,
        # Energy and performance
        "battery_mass_kg": battery_mass_kg,
        "battery_fraction_actual": f_batt_actual,
        "total_energy_wh": total_energy_wh,
        "energy_reserve_fraction": reserve_fraction,
        "usable_energy_wh": usable_energy_wh,
        "endurance_min": endurance_min,
        "range_km": range_km,
        # Takeoff
        "takeoff_distance_m": takeoff_distance,
        # Assessment
        "requirement_min": endurance_req,
        "vtol_possible": vtol_possible,
        "endurance_passes": endurance_passes,
        "feasible": vtol_possible and endurance_passes,
        "fail_reason": "Cannot satisfy VTOL requirement - no runway on Mars",
    }


# =============================================================================
# OUTPUT
# =============================================================================

def print_analysis(results: Dict[str, Any] = None) -> None:
    if results is None:
        results = fixed_wing_feasibility_analysis()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("FIXED-WING FEASIBILITY ANALYSIS (Section 5.2) - COUPLED")
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
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m^3")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print(f"  Battery mass:       {results['battery_mass_kg']:.2f} kg")
    print(f"  Battery fraction:   {results['battery_fraction_actual']:.2f}")
    print()

    print("AERODYNAMIC PARAMETERS (from Section 4.7)")
    print("-" * 50)
    print(f"  Aspect ratio:       {results['aspect_ratio']}")
    print(f"  Oswald efficiency:  {results['oswald_e']:.4f}")
    print(f"  CD0:                {results['cd0']:.4f}")
    print(f"  CL_max:             {results['cl_max']:.2f}")
    print(f"  K (induced):        {results['k_induced']:.4f}")
    print(f"  (L/D)_max:          {results['ld_max']:.2f}")
    print(f"  CL_optimal:         {results['cl_optimal']:.3f}")
    print()

    print("WING LOADING AND STALL")
    print("-" * 50)
    print(f"  Max wing loading:   {results['wing_loading_max']:.2f} N/m^2")
    print(f"  Stall speed:        {results['v_stall']:.1f} m/s")
    print()

    print("CRUISE PERFORMANCE")
    print("-" * 50)
    print(f"  CL at cruise:       {results['cl_cruise']:.3f}")
    print(f"  L/D at cruise:      {results['ld_cruise']:.2f}")
    print(f"  Cruise power:       {results['cruise_power_w']:.1f} W")
    print(f"  Combined eta_cruise:{results['eta_cruise']:.4f}")
    print()

    print("ENDURANCE AND RANGE")
    print("-" * 50)
    print(f"  Usable energy:      {results['usable_energy_wh']:.1f} Wh")
    print(f"  Endurance:          {results['endurance_min']:.1f} min")
    print(f"  Range:              {results['range_km']:.0f} km")
    print()

    print("TAKEOFF ANALYSIS (Disqualifying)")
    print("-" * 50)
    print(f"  Ground roll:        {results['takeoff_distance_m']:.0f} m")
    print("  Status:             IMPRACTICAL - No runway available on Mars")
    print()

    print("FEASIBILITY ASSESSMENT")
    print("-" * 50)
    end_status = "[PASS]" if results["endurance_passes"] else "[FAIL]"
    vtol_status = "[PASS]" if results["vtol_possible"] else "[FAIL]"
    print(
        f"  Endurance req:      {results['requirement_min']:.0f} min -> "
        f"{results['endurance_min']:.0f} min -> {end_status}"
    )
    print(f"  VTOL requirement:   Required -> Not possible -> {vtol_status}")
    print("  Overall:            [FAIL]")
    print()

    print("CONCLUSION: Fixed-wing FAILS due to VTOL requirement.")
    print(
        f"           Despite excellent endurance ({results['endurance_min']:.0f} min, "
        f"+{(results['endurance_min']/results['requirement_min']-1)*100:.0f}% margin),"
    )
    print(
        f"           ground roll of {results['takeoff_distance_m']:.0f} m is impractical without runway."
    )
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
