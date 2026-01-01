"""
Coupled Solver for Constraint-Based Sizing
=========================================

Solves a coupled set of sizing constraints using fsolve. The workflow uses
engineering guesses from YAML, with matching-chart style constraints to
initialize and guide the solution.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

from scipy.optimize import fsolve

from ..config import (
    get_param,
    get_initial_guess,
    get_solver_options,
    get_mars_gravity,
    get_density,
    get_propulsion_efficiencies,
    get_battery_params,
    get_mission_params,
    get_aerodynamic_params,
)

from mars_uav_sizing.section5.rotorcraft import hover_power_loading
from mars_uav_sizing.section5.fixed_wing import (
    cruise_lift_coefficient,
    lift_to_drag,
    cruise_power_loading,
    stall_wing_loading_limit,
)


def smooth_max(a: float, b: float, eps: float) -> float:
    return 0.5 * (a + b + math.sqrt((a - b) ** 2 + eps ** 2))


def transition_energy_wh(mtow_kg: float) -> float:
    n_transitions = get_param("mission.time.n_transitions")
    reference_energy_j = get_param("mission.transition.reference_energy_j")
    ref_mtow_kg = get_param("mission.transition.reference_mtow_kg")
    mars_scaling = get_param("mission.transition.mars_scaling_factor")

    if ref_mtow_kg <= 0:
        return 0.0

    mass_ratio = mtow_kg / ref_mtow_kg
    scaled_energy_j = reference_energy_j * mass_ratio * mars_scaling
    total_transition_j = scaled_energy_j * n_transitions
    return total_transition_j / 3600.0


def constraint_values(wing_loading: float) -> Dict[str, float]:
    rho = get_density()
    mission = get_mission_params()
    aero = get_aerodynamic_params()

    cl = cruise_lift_coefficient(wing_loading, rho, mission["v_cruise"])
    ld_pure = lift_to_drag(cl)
    ld_penalty = get_param("aerodynamic.quadplane.ld_penalty_factor")
    ld_qp = ld_pure * ld_penalty
    pw_cruise = cruise_power_loading(mission["v_cruise"], ld_qp)

    pw_hover = hover_power_loading()

    v_min = mission["v_stall"] * get_param("mission.velocity.v_min_factor")
    ws_stall = stall_wing_loading_limit(rho, v_min, aero["cl_max"])

    return {
        "pw_hover": pw_hover,
        "pw_cruise": pw_cruise,
        "ws_stall": ws_stall,
        "ld_qp": ld_qp,
        "cl_cruise": cl,
    }


def power_loading_target(wing_loading: float, constraint_mode: str, eps: float) -> float:
    values = constraint_values(wing_loading)
    pw_hover = values["pw_hover"]
    pw_cruise = values["pw_cruise"]

    if constraint_mode == "hover":
        return pw_hover
    if constraint_mode == "cruise":
        return pw_cruise
    return smooth_max(pw_hover, pw_cruise, eps)


def build_initial_guess() -> List[float]:
    guess = get_initial_guess()

    mtow_kg = float(guess.get("mtow_kg", get_param("mission.mass.mtow_kg")))

    if "wing_loading_n_m2" in guess:
        wing_loading = float(guess["wing_loading_n_m2"])
    else:
        rho = get_density()
        mission = get_mission_params()
        aero = get_aerodynamic_params()
        v_min = mission["v_stall"] * get_param("mission.velocity.v_min_factor")
        wing_loading = stall_wing_loading_limit(rho, v_min, aero["cl_max"])

    if "power_loading_w_n" in guess:
        power_loading = float(guess["power_loading_w_n"])
    else:
        options = get_solver_options()
        mode = options.get("power_constraint", "smooth_max")
        eps = float(options.get("smooth_max_epsilon", 1.0e-3))
        power_loading = power_loading_target(wing_loading, mode, eps)

    if "battery_mass_kg" in guess:
        battery_mass = float(guess["battery_mass_kg"])
    else:
        f_batt = get_param("mission.mass_fractions.f_battery")
        battery_mass = f_batt * mtow_kg

    return [mtow_kg, wing_loading, power_loading, battery_mass]


def residuals(x: List[float]) -> List[float]:
    mtow_kg, wing_loading, power_loading, battery_mass = x

    if mtow_kg <= 0 or wing_loading <= 0 or power_loading <= 0 or battery_mass <= 0:
        return [1.0e6, 1.0e6, 1.0e6, 1.0e6]

    g_mars = get_mars_gravity()
    weight_n = mtow_kg * g_mars

    # Mass balance
    payload_kg = get_param("mission.mass.payload_kg")
    f_empty = get_param("mission.mass_fractions.f_empty")
    f_prop = get_param("mission.mass_fractions.f_propulsion")
    f_av = get_param("mission.mass_fractions.f_avionics")
    eq_mass = mtow_kg * (1.0 - f_empty - f_prop - f_av) - payload_kg - battery_mass

    # Stall constraint (active)
    values = constraint_values(wing_loading)
    eq_stall = wing_loading - values["ws_stall"]

    # Power constraint (active selector)
    options = get_solver_options()
    mode = options.get("power_constraint", "smooth_max")
    eps = float(options.get("smooth_max_epsilon", 1.0e-3))
    pw_target = power_loading_target(wing_loading, mode, eps)
    eq_power = power_loading - pw_target

    # Energy balance
    batt = get_battery_params()
    mission = get_mission_params()

    battery_energy_wh = (
        battery_mass
        * batt["e_spec_Wh_kg"]
        * batt["dod"]
        * batt["eta_discharge"]
    )
    energy_available_wh = battery_energy_wh * (1.0 - mission["energy_reserve"])

    pw_hover = values["pw_hover"]
    pw_cruise = values["pw_cruise"]
    p_hover_w = pw_hover * weight_n
    p_cruise_w = pw_cruise * weight_n

    t_hover_s = get_param("mission.time.t_hover_s")
    t_cruise_min = get_param("mission.time.t_cruise_min")

    e_hover_wh = p_hover_w * (t_hover_s / 3600.0)
    e_cruise_wh = p_cruise_w * (t_cruise_min / 60.0)
    e_transition_wh = transition_energy_wh(mtow_kg)

    mission_energy_wh = e_hover_wh + e_transition_wh + e_cruise_wh
    eq_energy = energy_available_wh - mission_energy_wh

    return [eq_mass, eq_stall, eq_power, eq_energy]


def solve_coupled_design(initial_guess: List[float] | None = None) -> Dict[str, Any]:
    options = get_solver_options()
    max_iter = int(options.get("max_iter", 500))
    tol = float(options.get("tol", 1.0e-9))

    x0 = initial_guess if initial_guess is not None else build_initial_guess()

    solution, info, ier, message = fsolve(
        residuals,
        x0,
        xtol=tol,
        maxfev=max_iter,
        full_output=True,
    )

    mtow_kg, wing_loading, power_loading, battery_mass = solution

    values = constraint_values(wing_loading)
    g_mars = get_mars_gravity()
    weight_n = mtow_kg * g_mars

    batt = get_battery_params()
    mission = get_mission_params()

    battery_energy_wh = (
        battery_mass
        * batt["e_spec_Wh_kg"]
        * batt["dod"]
        * batt["eta_discharge"]
    )
    energy_available_wh = battery_energy_wh * (1.0 - mission["energy_reserve"])

    pw_hover = values["pw_hover"]
    pw_cruise = values["pw_cruise"]

    t_hover_s = get_param("mission.time.t_hover_s")
    t_cruise_min = get_param("mission.time.t_cruise_min")

    e_hover_wh = pw_hover * weight_n * (t_hover_s / 3600.0)
    e_cruise_wh = pw_cruise * weight_n * (t_cruise_min / 60.0)
    e_transition_wh = transition_energy_wh(mtow_kg)
    mission_energy_wh = e_hover_wh + e_transition_wh + e_cruise_wh

    f_payload = get_param("mission.mass.payload_kg") / mtow_kg if mtow_kg > 0 else 0.0
    f_batt = battery_mass / mtow_kg if mtow_kg > 0 else 0.0

    return {
        "converged": ier == 1,
        "message": message,
        "iterations": info.get("nfev"),
        "residuals": info.get("fvec"),
        "solution": {
            "mtow_kg": mtow_kg,
            "weight_n": weight_n,
            "wing_loading_n_m2": wing_loading,
            "power_loading_w_n": power_loading,
            "battery_mass_kg": battery_mass,
            "battery_fraction": f_batt,
            "payload_fraction": f_payload,
        },
        "constraints": {
            "pw_hover": pw_hover,
            "pw_cruise": pw_cruise,
            "ws_stall": values["ws_stall"],
            "ld_qp": values["ld_qp"],
            "cl_cruise": values["cl_cruise"],
        },
        "energy": {
            "battery_energy_wh": battery_energy_wh,
            "energy_available_wh": energy_available_wh,
            "hover_energy_wh": e_hover_wh,
            "transition_energy_wh": e_transition_wh,
            "cruise_energy_wh": e_cruise_wh,
            "mission_energy_wh": mission_energy_wh,
        },
    }


_solution_cache: Dict[str, Any] | None = None


def get_coupled_solution(reload: bool = False) -> Dict[str, Any]:
    global _solution_cache
    if _solution_cache is None or reload:
        _solution_cache = solve_coupled_design()
    return _solution_cache
