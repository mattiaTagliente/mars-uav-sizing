"""
Matching Chart Analysis (Coupled)
=================================

Generates the constraint-based matching chart and determines a design point.
Optionally uses a coupled fsolve workflow to solve constraints and energy
simultaneously.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict

import numpy as np

from ..config import (
    get_mars_gravity,
    get_density,
    get_mtow,
    get_propulsion_efficiencies,
    get_aerodynamic_params,
    get_mission_params,
    get_param,
)

from .rotorcraft import hover_power_loading, induced_velocity_from_disk_loading
from .fixed_wing import (
    cruise_lift_coefficient,
    lift_to_drag,
    cruise_power_loading,
    stall_wing_loading_limit,
    maximum_ld,
)


def hover_constraint() -> float:
    return hover_power_loading()


def stall_constraint() -> float:
    rho = get_density()
    v_stall = get_mission_params()["v_stall"]
    v_min_factor = get_param("mission.velocity.v_min_factor")
    v_min = v_stall * v_min_factor
    cl_max = get_aerodynamic_params()["cl_max"]
    return stall_wing_loading_limit(rho, v_min, cl_max)


def cruise_constraint(wing_loading: float) -> float:
    rho = get_density()
    v_cruise = get_mission_params()["v_cruise"]

    cl = cruise_lift_coefficient(wing_loading, rho, v_cruise)
    ld_penalty = get_param("aerodynamic.quadplane.ld_penalty_factor")
    ld_pure = lift_to_drag(cl)
    ld = ld_pure * ld_penalty

    return cruise_power_loading(v_cruise, ld)


def cruise_constraint_curve(ws_range: np.ndarray) -> np.ndarray:
    return np.array([cruise_constraint(ws) for ws in ws_range])


def find_design_point(use_coupled_solver: bool = True) -> Dict[str, Any]:
    if use_coupled_solver:
        from .coupled_solver import get_coupled_solution

        solver = get_coupled_solution()
        sol = solver["solution"]
        wing_loading = sol["wing_loading_n_m2"]
        power_loading = sol["power_loading_w_n"]

        pw_hover = hover_constraint()
        pw_cruise = cruise_constraint(wing_loading)
        active_constraint = "hover" if pw_hover >= pw_cruise else "cruise"

        return {
            "wing_loading": wing_loading,
            "power_loading": power_loading,
            "hover_pw": pw_hover,
            "cruise_pw_at_stall": pw_cruise,
            "stall_ws": stall_constraint(),
            "active_constraint": active_constraint,
            "solver": solver,
        }

    pw_hover = hover_constraint()
    ws_stall = stall_constraint()
    pw_cruise_at_stall = cruise_constraint(ws_stall)

    ws_design = ws_stall
    pw_design = max(pw_hover, pw_cruise_at_stall)
    active_constraint = "hover" if pw_hover > pw_cruise_at_stall else "cruise"

    return {
        "wing_loading": ws_design,
        "power_loading": pw_design,
        "hover_pw": pw_hover,
        "cruise_pw_at_stall": pw_cruise_at_stall,
        "stall_ws": ws_stall,
        "active_constraint": active_constraint,
        "solver": None,
    }


def derive_geometry(design_point: Dict[str, Any] | None = None) -> Dict[str, float]:
    if design_point is None:
        design_point = find_design_point(use_coupled_solver=True)

    g_mars = get_mars_gravity()
    ar = get_aerodynamic_params()["aspect_ratio"]

    mtow_kg = get_mtow()
    solver = design_point.get("solver")
    if solver and "solution" in solver:
        mtow_kg = solver["solution"]["mtow_kg"]

    weight_n = mtow_kg * g_mars
    ws = design_point["wing_loading"]
    pw = design_point["power_loading"]

    wing_area = weight_n / ws
    wingspan = math.sqrt(ar * wing_area)
    chord = wing_area / wingspan

    installed_power = pw * weight_n

    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    disk_area = weight_n / disk_loading

    return {
        "wing_area_m2": wing_area,
        "wingspan_m": wingspan,
        "chord_m": chord,
        "installed_power_w": installed_power,
        "disk_area_m2": disk_area,
    }


def matching_chart_analysis(use_coupled_solver: bool = True) -> Dict[str, Any]:
    g_mars = get_mars_gravity()
    rho = get_density()
    mtow_kg = get_mtow()
    prop = get_propulsion_efficiencies()
    aero = get_aerodynamic_params()
    mission = get_mission_params()
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")

    pw_hover = hover_constraint()
    ws_stall = stall_constraint()

    design_point = find_design_point(use_coupled_solver=use_coupled_solver)
    solver = design_point.get("solver")
    if solver and "solution" in solver:
        mtow_kg = solver["solution"]["mtow_kg"]

    weight_n = mtow_kg * g_mars

    geometry = derive_geometry(design_point)

    ld_max, _ = maximum_ld()
    ld_penalty = get_param("aerodynamic.quadplane.ld_penalty_factor")
    ld_quadplane = ld_max * ld_penalty

    v_i = induced_velocity_from_disk_loading(disk_loading, rho)

    eta_hover = prop["figure_of_merit"] * prop["eta_motor"] * prop["eta_esc"]
    eta_cruise = prop["eta_prop"] * prop["eta_motor"] * prop["eta_esc"]

    ws_range = np.linspace(2.0, 15.0, 50)
    pw_cruise_curve = cruise_constraint_curve(ws_range)
    pw_hover_line = np.full_like(ws_range, pw_hover)

    return {
        "mtow_kg": mtow_kg,
        "weight_n": weight_n,
        "rho_kg_m3": rho,
        "v_cruise_m_s": mission["v_cruise"],
        "disk_loading_n_m2": disk_loading,
        "figure_of_merit": prop["figure_of_merit"],
        "eta_hover": eta_hover,
        "eta_cruise": eta_cruise,
        "ld_max": ld_max,
        "ld_quadplane": ld_quadplane,
        "cl_max": aero["cl_max"],
        "hover_pw": pw_hover,
        "stall_ws": ws_stall,
        "induced_velocity_m_s": v_i,
        "design_point": design_point,
        "geometry": geometry,
        "ws_range": ws_range,
        "pw_cruise_curve": pw_cruise_curve,
        "pw_hover_line": pw_hover_line,
    }


def print_analysis(results: Dict[str, Any] | None = None, use_coupled_solver: bool = True) -> None:
    if results is None:
        results = matching_chart_analysis(use_coupled_solver=use_coupled_solver)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dp = results["design_point"]
    geom = results["geometry"]
    mode_label = "COUPLED" if use_coupled_solver else "UNCOUPLED"

    print("=" * 80)
    print(f"MATCHING CHART ANALYSIS (Section 5.4) - {mode_label}")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print("Config:   All values loaded from config/ YAML files")
    print()

    print("INPUT PARAMETERS")
    print("-" * 50)
    print(f"  MTOW:               {results['mtow_kg']:.2f} kg")
    print(f"  Weight:             {results['weight_n']:.2f} N")
    print(f"  Air density:        {results['rho_kg_m3']:.4f} kg/m^3")
    print(f"  Cruise velocity:    {results['v_cruise_m_s']:.1f} m/s")
    print(f"  Disk loading:       {results['disk_loading_n_m2']:.1f} N/m^2")
    print()

    print("CONSTRAINT VALUES")
    print("-" * 50)
    print(f"  Hover P/W:          {results['hover_pw']:.2f} W/N (horizontal line)")
    print(f"  Stall W/S limit:    {results['stall_ws']:.2f} N/m^2 (vertical line)")
    print()

    print("DESIGN POINT")
    print("-" * 50)
    print(f"  Wing loading:       {dp['wing_loading']:.2f} N/m^2")
    print(f"  Power loading:      {dp['power_loading']:.2f} W/N")
    print(f"  Active constraint:  {dp['active_constraint'].upper()}")
    print()

    solver = dp.get("solver")
    if solver:
        print("COUPLED SOLVER")
        print("-" * 50)
        print(f"  Converged:          {solver['converged']}")
        print(f"  Iterations:         {solver['iterations']}")
        print(f"  Message:            {solver['message']}")
        sol = solver["solution"]
        print(f"  MTOW (solved):      {sol['mtow_kg']:.2f} kg")
        print(f"  Battery mass:       {sol['battery_mass_kg']:.2f} kg")
        print(f"  Battery fraction:   {sol['battery_fraction']:.2f}")
        print()

    print("DERIVED GEOMETRY")
    print("-" * 50)
    print(f"  Wing area:          {geom['wing_area_m2']:.3f} m^2")
    print(f"  Wingspan:           {geom['wingspan_m']:.2f} m")
    print(f"  Mean chord:         {geom['chord_m']:.3f} m")
    print(f"  Installed power:    {geom['installed_power_w']:.0f} W (hover)")
    print(f"  Disk area:          {geom['disk_area_m2']:.3f} m^2")
    print()

    print("SUMMARY")
    print("-" * 50)
    print("  The matching chart shows:")
    print(f"  1. Hover constraint at P/W = {results['hover_pw']:.1f} W/N")
    print(f"  2. Stall constraint limits W/S to {results['stall_ws']:.1f} N/m^2")
    print(
        f"  3. Cruise power at stall: {dp['cruise_pw_at_stall']:.1f} W/N"
    )
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
