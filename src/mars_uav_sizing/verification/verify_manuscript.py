"""
Manuscript Verification
=======================

Comprehensive verification of all computed values against expected results
derived from configuration and explicit formulas.

Last Updated: 2025-12-29
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np

from ..config import get_param
from ..section3 import atmospheric_model
from ..section4 import aerodynamic_calculations, derived_requirements, geometry_calculations
from ..section5 import rotorcraft, fixed_wing, hybrid_vtol, matching_chart


DEFAULT_TOLERANCE_PCT = 0.5
ARRAY_TOLERANCE_PCT = 0.5


@dataclass
class VerificationResult:
    """Result of a single verification check."""

    name: str
    expected: Any
    computed: Any
    unit: str
    passed: bool
    error_pct: float | None
    section: str
    note: str = ""

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        error_text = "n/a" if self.error_pct is None else f"{self.error_pct:.2f}%"
        note_text = f" ({self.note})" if self.note else ""
        return (
            f"{status} {self.name}: expected={self.expected}, "
            f"computed={self._format_computed()} {self.unit} "
            f"(error={error_text}){note_text}"
        )

    def _format_computed(self) -> str:
        if self.computed is None:
            return "None"
        if isinstance(self.computed, float):
            return f"{self.computed:.6g}"
        return str(self.computed)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_array(value: Any) -> bool:
    return isinstance(value, np.ndarray)


def _unit_from_key(key: str) -> str:
    suffix_map = [
        ("_kg_m3", "kg/m^3"),
        ("_n_m2", "N/m^2"),
        ("_w_per_n", "W/N"),
        ("_w_per_kg", "W/kg"),
        ("_pa_s", "Pa*s"),
        ("_m_s", "m/s"),
        ("_m2", "m^2"),
        ("_m3", "m^3"),
        ("_km", "km"),
        ("_min", "min"),
        ("_wh", "Wh"),
        ("_kg", "kg"),
        ("_n", "N"),
        ("_N", "N"),
        ("_s", "s"),
        ("_w", "W"),
    ]
    for suffix, unit in suffix_map:
        if key.endswith(suffix):
            return unit
    return ""


def _check_value(
    name: str,
    expected: float,
    computed: float,
    unit: str,
    section: str,
    tolerance_pct: float = DEFAULT_TOLERANCE_PCT,
) -> VerificationResult:
    if expected == 0:
        error_pct = abs(computed) * 100
    else:
        error_pct = abs(computed - expected) / abs(expected) * 100
    passed = error_pct <= tolerance_pct
    return VerificationResult(
        name=name,
        expected=expected,
        computed=computed,
        unit=unit,
        passed=passed,
        error_pct=error_pct,
        section=section,
    )


def _check_bool(
    name: str,
    expected: bool,
    computed: bool,
    section: str,
) -> VerificationResult:
    passed = expected is computed
    return VerificationResult(
        name=name,
        expected=expected,
        computed=computed,
        unit="",
        passed=passed,
        error_pct=None,
        section=section,
    )


def _check_array(
    name: str,
    expected: np.ndarray,
    computed: np.ndarray,
    section: str,
    tolerance_pct: float = ARRAY_TOLERANCE_PCT,
) -> VerificationResult:
    expected = np.asarray(expected)
    computed = np.asarray(computed)
    if expected.shape != computed.shape:
        return VerificationResult(
            name=name,
            expected=f"shape={expected.shape}",
            computed=f"shape={computed.shape}",
            unit="",
            passed=False,
            error_pct=None,
            section=section,
            note="shape mismatch",
        )
    denom = np.where(np.abs(expected) > 0, np.abs(expected), 1.0)
    error_pct = float(np.max(np.abs(computed - expected) / denom) * 100)
    passed = error_pct <= tolerance_pct
    return VerificationResult(
        name=name,
        expected=f"array(shape={expected.shape})",
        computed=f"array(shape={computed.shape})",
        unit="",
        passed=passed,
        error_pct=error_pct,
        section=section,
        note="array max error",
    )


def _compare_dict(
    section: str,
    expected: Dict[str, Any],
    computed: Dict[str, Any],
    prefix: str = "",
) -> List[VerificationResult]:
    results: List[VerificationResult] = []

    for key, expected_value in expected.items():
        name = f"{prefix}{key}"
        if key not in computed:
            results.append(
                VerificationResult(
                    name=name,
                    expected=expected_value,
                    computed=None,
                    unit=_unit_from_key(key),
                    passed=False,
                    error_pct=None,
                    section=section,
                    note="missing computed value",
                )
            )
            continue

        computed_value = computed[key]
        if isinstance(expected_value, dict):
            if not isinstance(computed_value, dict):
                results.append(
                    VerificationResult(
                        name=name,
                        expected="dict",
                        computed=type(computed_value).__name__,
                        unit="",
                        passed=False,
                        error_pct=None,
                        section=section,
                        note="type mismatch",
                    )
                )
            else:
                results.extend(
                    _compare_dict(
                        section,
                        expected_value,
                        computed_value,
                        prefix=f"{name}.",
                    )
                )
            continue

        if isinstance(expected_value, bool):
            results.append(_check_bool(name, expected_value, computed_value, section))
            continue

        if _is_array(expected_value):
            results.append(_check_array(name, expected_value, computed_value, section))
            continue

        if _is_number(expected_value):
            unit = _unit_from_key(key)
            results.append(
                _check_value(name, expected_value, computed_value, unit, section)
            )
            continue

        if expected_value != computed_value:
            results.append(
                VerificationResult(
                    name=name,
                    expected=expected_value,
                    computed=computed_value,
                    unit="",
                    passed=False,
                    error_pct=None,
                    section=section,
                    note="value mismatch",
                )
            )

    # Ensure all numeric computed values are covered
    for key, computed_value in computed.items():
        if key in expected:
            continue
        if _is_number(computed_value) or _is_array(computed_value) or isinstance(
            computed_value, bool
        ):
            name = f"{prefix}{key}"
            results.append(
                VerificationResult(
                    name=name,
                    expected="(expected value missing)",
                    computed=computed_value,
                    unit=_unit_from_key(key),
                    passed=False,
                    error_pct=None,
                    section=section,
                    note="unchecked numeric value",
                )
            )

    return results


def _expected_arcadia_conditions() -> Dict[str, float]:
    surface_elevation_km = get_param("environment.arcadia_planitia.elevation_km")
    agl_m = get_param("environment.arcadia_planitia.operating_altitude_agl_m")
    operating_altitude_km = surface_elevation_km + (agl_m / 1000.0)

    T0 = get_param("environment.reference_atmosphere.T_surface")
    P0 = get_param("environment.reference_atmosphere.P_surface")
    lapse = get_param("environment.reference_atmosphere.lapse_rate")
    g = get_param("physical.mars.g")
    R = get_param("physical.mars_atmosphere_composition.R_specific")
    gamma = get_param("physical.mars_atmosphere_composition.gamma")
    mu_ref = get_param("physical.sutherland.mu_ref")
    T_ref = get_param("physical.sutherland.T_ref")
    C = get_param("physical.sutherland.C")

    T = T0 - lapse * operating_altitude_km * 1000
    exponent = g / (R * lapse)
    P = P0 * (T / T0) ** exponent
    rho = P / (R * T)
    mu = mu_ref * (T / T_ref) ** 1.5 * (T_ref + C) / (T + C)
    a = math.sqrt(gamma * R * T)

    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    chord = get_param("aerodynamic.wing.mean_chord_m")
    Re = rho * v_cruise * chord / mu
    M = v_cruise / a

    return {
        "surface_elevation_km": surface_elevation_km,
        "agl_m": agl_m,
        "operating_altitude_km": operating_altitude_km,
        "temperature_K": T,
        "pressure_Pa": P,
        "density_kg_m3": rho,
        "viscosity_Pa_s": mu,
        "speed_of_sound_m_s": a,
        "kinematic_viscosity_m2_s": mu / rho,
        "reynolds_at_cruise": Re,
        "mach_at_cruise": M,
    }


def _expected_aero() -> Dict[str, float]:
    ar = get_param("aerodynamic.wing.aspect_ratio")
    e = get_param("aerodynamic.wing.oswald_efficiency")
    cd0 = get_param("aerodynamic.drag_polar.cd0")
    k = 1 / (math.pi * ar * e)
    cl_opt = math.sqrt(cd0 * math.pi * ar * e)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    e_sadraey = 1.78 * (1 - 0.045 * ar ** 0.68) - 0.64
    ld_qp = ld_max * get_param("aerodynamic.quadplane.ld_penalty_factor")
    ld_rotor = get_param("aerodynamic.rotorcraft.ld_effective")
    return {
        "aspect_ratio": ar,
        "oswald_e": e,
        "oswald_e_sadraey": e_sadraey,
        "cd0": cd0,
        "k": k,
        "ld_max": ld_max,
        "cl_optimal": cl_opt,
        "ld_quadplane": ld_qp,
        "ld_rotorcraft": ld_rotor,
    }


def _expected_derived_requirements() -> Dict[str, float]:
    g = get_param("physical.mars.g")
    mtow_kg = get_param("mission.mass.mtow_kg")
    weight_n = mtow_kg * g
    ar = get_param("aerodynamic.wing.aspect_ratio")
    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    v_min_factor = get_param("mission.velocity.v_min_factor")

    target_re = 60000
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    mu = get_param("environment.arcadia_planitia.viscosity_Pa_s")
    chord_re = target_re * mu / (rho * v_cruise)
    wing_area_re = chord_re**2 * ar
    wingspan_re = math.sqrt(ar * wing_area_re)
    ws_re = weight_n / wing_area_re
    cl_max = get_param("aerodynamic.airfoil.cl_max")
    v_stall_re = math.sqrt(2 * ws_re / (rho * cl_max))
    v_min_re = v_stall_re * v_min_factor

    v_stall_config = get_param("mission.velocity.v_stall_m_s")
    v_min_stall = v_stall_config * v_min_factor
    ws_stall = 0.5 * rho * v_min_stall**2 * cl_max
    wing_area_stall = weight_n / ws_stall
    wingspan_stall = math.sqrt(ar * wing_area_stall)
    chord_stall = wing_area_stall / wingspan_stall
    re_stall = rho * v_cruise * chord_stall / mu

    a = get_param("environment.arcadia_planitia.speed_of_sound_m_s")
    M = v_cruise / a

    return {
        "mtow_kg": mtow_kg,
        "weight_n": weight_n,
        "v_cruise_m_s": v_cruise,
        "v_min_factor": v_min_factor,
        "target_reynolds": target_re,
        "re_chord_m": chord_re,
        "re_wing_area_m2": wing_area_re,
        "re_wingspan_m": wingspan_re,
        "re_wing_loading": ws_re,
        "re_v_stall_m_s": v_stall_re,
        "re_v_min_m_s": v_min_re,
        "stall_v_stall_m_s": v_stall_config,
        "stall_v_min_m_s": v_min_stall,
        "stall_wing_loading": ws_stall,
        "stall_wing_area_m2": wing_area_stall,
        "stall_wingspan_m": wingspan_stall,
        "stall_chord_m": chord_stall,
        "stall_reynolds": re_stall,
        "mach_cruise": M,
        "aspect_ratio": ar,
    }


def _expected_geometry() -> Dict[str, Any]:
    g = get_param("physical.mars.g")
    mtow = get_param("mission.mass.mtow_kg")
    weight_n = mtow * g
    ar = get_param("aerodynamic.wing.aspect_ratio")

    v_stall = get_param("mission.velocity.v_stall_m_s")
    v_min_factor = get_param("mission.velocity.v_min_factor")
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    cl_max = get_param("aerodynamic.airfoil.cl_max")
    v_min = v_stall * v_min_factor
    ws = 0.5 * rho * v_min**2 * cl_max

    wing_area = weight_n / ws
    wingspan = math.sqrt(ar * wing_area)
    chord = wing_area / wingspan

    fuselage_ratio = get_param("geometry.fuselage.length_to_span_ratio")
    fuselage_len = fuselage_ratio * wingspan
    moment_arm_ratio = get_param("geometry.tail.moment_arm_ratio")
    moment_arm = moment_arm_ratio * fuselage_len

    v_h = get_param("geometry.tail.v_h")
    v_v = get_param("geometry.tail.v_v")
    sh = v_h * wing_area * chord / moment_arm
    sv = v_v * wing_area * wingspan / moment_arm

    dihedral_deg = get_param("geometry.tail.vtail_dihedral_deg")
    vtail_ar = get_param("geometry.tail.vtail_aspect_ratio")
    dihedral_rad = math.radians(dihedral_deg)
    cos2_gamma = math.cos(dihedral_rad) ** 2
    sin2_gamma = math.sin(dihedral_rad) ** 2
    s_vtail_from_h = sh / cos2_gamma
    s_vtail_from_v = sv / sin2_gamma
    s_vtail_total = max(s_vtail_from_h, s_vtail_from_v)
    s_per_surface = s_vtail_total / 2
    span_per_surface = math.sqrt(vtail_ar * s_per_surface)
    vtail_chord = s_per_surface / span_per_surface

    n_rotors = get_param("geometry.rotor.n_rotors")
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    area_per_rotor = (weight_n / n_rotors) / disk_loading
    rotor_diam = math.sqrt(4 * area_per_rotor / math.pi)
    total_disk = weight_n / disk_loading

    return {
        "wing_loading_n_m2": ws,
        "wing_area_m2": wing_area,
        "wingspan_m": wingspan,
        "mean_chord_m": chord,
        "fuselage_length_m": fuselage_len,
        "moment_arm_ratio": moment_arm_ratio,
        "moment_arm_m": moment_arm,
        "sh_required_m2": sh,
        "sv_required_m2": sv,
        "vtail": {
            "s_vtail_total": s_vtail_total,
            "s_per_surface": s_per_surface,
            "dihedral_deg": dihedral_deg,
            "span_per_surface": span_per_surface,
            "chord": vtail_chord,
            "aspect_ratio": vtail_ar,
            "actual_sh": s_vtail_total * cos2_gamma,
            "actual_sv": s_vtail_total * sin2_gamma,
        },
        "n_rotors": n_rotors,
        "rotor_diameter_m": rotor_diam,
        "total_disk_area_m2": total_disk,
    }


def _expected_rotorcraft() -> Dict[str, Any]:
    g = get_param("physical.mars.g")
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    mtow = get_param("mission.mass.mtow_kg")
    weight_n = mtow * g
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    disk_area = weight_n / disk_loading
    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    t_hover_s = get_param("mission.time.t_hover_s")
    reserve = get_param("mission.energy.reserve_fraction")
    f_batt = get_param("mission.mass_fractions.f_battery")
    e_spec = get_param("battery.specifications.specific_energy_Wh_kg")
    dod = get_param("battery.utilization.depth_of_discharge")
    eta_dis = get_param("battery.utilization.discharge_efficiency")
    fm = get_param("propulsion.rotor.figure_of_merit")
    eta_m = get_param("propulsion.electromechanical.eta_motor")
    eta_e = get_param("propulsion.electromechanical.eta_esc")
    ld_eff = get_param("aerodynamic.rotorcraft.ld_effective")
    endurance_req = get_param("mission.requirements.endurance_min")

    v_i = math.sqrt(weight_n / (2 * rho * disk_area))
    p_ideal = (weight_n**1.5) / math.sqrt(2 * rho * disk_area)
    p_hover = p_ideal / fm
    p_hover_elec = p_hover / (eta_m * eta_e)
    p_fwd_mech = (weight_n * v_cruise) / ld_eff
    p_fwd_elec = p_fwd_mech / (eta_m * eta_e)

    battery_mass = f_batt * mtow
    total_energy = battery_mass * e_spec
    usable_energy = total_energy * dod * eta_dis
    energy_after_reserve = usable_energy * (1 - reserve)
    hover_energy = p_hover_elec * (t_hover_s / 3600)
    cruise_energy = energy_after_reserve - hover_energy

    if cruise_energy > 0:
        cruise_time_s = (cruise_energy / p_fwd_elec) * 3600
        cruise_time_min = cruise_time_s / 60
    else:
        cruise_time_s = 0.0
        cruise_time_min = 0.0

    endurance_min = (t_hover_s / 60) + cruise_time_min
    range_km = (v_cruise * cruise_time_s) / 1000

    feasible = endurance_min >= endurance_req
    margin_pct = ((endurance_min / endurance_req) - 1) * 100

    eta_hover = fm * eta_m * eta_e
    eta_cruise = eta_m * eta_e

    return {
        "mtow_kg": mtow,
        "weight_n": weight_n,
        "disk_loading_n_m2": disk_loading,
        "disk_area_m2": disk_area,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        "figure_of_merit": fm,
        "eta_motor": eta_m,
        "eta_esc": eta_e,
        "eta_hover": eta_hover,
        "eta_cruise": eta_cruise,
        "ld_effective": ld_eff,
        "induced_velocity_m_s": v_i,
        "hover_power_w": p_hover_elec,
        "cruise_power_w": p_fwd_elec,
        "power_loading_w_per_n": p_hover_elec / weight_n,
        "power_loading_w_per_kg": p_hover_elec / mtow,
        "battery_mass_kg": battery_mass,
        "total_energy_wh": total_energy,
        "usable_energy_wh": usable_energy,
        "energy_after_reserve_wh": energy_after_reserve,
        "hover_energy_wh": hover_energy,
        "cruise_energy_wh": cruise_energy,
        "hover_time_min": t_hover_s / 60,
        "cruise_time_min": cruise_time_min,
        "endurance_min": endurance_min,
        "range_km": range_km,
        "requirement_min": endurance_req,
        "feasible": feasible,
        "margin_percent": margin_pct,
    }


def _expected_fixed_wing() -> Dict[str, Any]:
    g = get_param("physical.mars.g")
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    mtow = get_param("mission.mass.mtow_kg")
    weight_n = mtow * g
    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    v_stall = get_param("mission.velocity.v_stall_m_s")
    v_min_factor = get_param("mission.velocity.v_min_factor")
    f_batt = get_param("mission.mass_fractions.f_battery")
    e_spec = get_param("battery.specifications.specific_energy_Wh_kg")
    dod = get_param("battery.utilization.depth_of_discharge")
    eta_dis = get_param("battery.utilization.discharge_efficiency")
    endurance_req = get_param("mission.requirements.endurance_min")

    ar = get_param("aerodynamic.wing.aspect_ratio")
    e = get_param("aerodynamic.wing.oswald_efficiency")
    cd0 = get_param("aerodynamic.drag_polar.cd0")
    cl_max = get_param("aerodynamic.airfoil.cl_max")

    k = 1 / (math.pi * ar * e)
    cl_opt = math.sqrt(math.pi * ar * e * cd0)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)

    v_min = v_stall * v_min_factor
    ws_max = 0.5 * rho * v_min**2 * cl_max
    cl_cruise = (2 * ws_max) / (rho * v_cruise**2)
    cd_cruise = cd0 + k * cl_cruise**2
    ld_cruise = cl_cruise / cd_cruise

    eta_prop = get_param("propulsion.electromechanical.eta_prop")
    eta_motor = get_param("propulsion.electromechanical.eta_motor")
    eta_esc = get_param("propulsion.electromechanical.eta_esc")
    eta_cruise = eta_prop * eta_motor * eta_esc

    p_cruise = (weight_n * v_cruise) / (ld_max * eta_cruise)
    pw_cruise = v_cruise / (ld_max * eta_cruise)

    reserve = get_param("mission.energy.reserve_fraction")
    battery_mass = f_batt * mtow
    total_energy = battery_mass * e_spec
    usable_energy = total_energy * dod * eta_dis * (1 - reserve)
    endurance_h = usable_energy / p_cruise
    endurance_min = endurance_h * 60
    range_km = v_cruise * endurance_h * 3.6

    v_stall_calc = math.sqrt((2 * ws_max) / (rho * cl_max))
    v_to = 1.1 * v_stall_calc
    takeoff_distance = v_to**2 / (2 * 0.7)

    vtol_possible = False
    endurance_passes = endurance_min >= endurance_req

    return {
        "mtow_kg": mtow,
        "weight_n": weight_n,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        "aspect_ratio": ar,
        "oswald_e": e,
        "cd0": cd0,
        "cl_max": cl_max,
        "k_induced": k,
        "ld_max": ld_max,
        "cl_optimal": cl_opt,
        "cl_cruise": cl_cruise,
        "ld_cruise": ld_cruise,
        "eta_prop": eta_prop,
        "eta_motor": eta_motor,
        "eta_esc": eta_esc,
        "eta_cruise": eta_cruise,
        "wing_loading_max": ws_max,
        "v_stall": v_stall_calc,
        "cruise_power_w": p_cruise,
        "power_loading_w_per_n": pw_cruise,
        "battery_mass_kg": battery_mass,
        "total_energy_wh": total_energy,
        "usable_energy_wh": usable_energy,
        "endurance_min": endurance_min,
        "range_km": range_km,
        "takeoff_distance_m": takeoff_distance,
        "requirement_min": endurance_req,
        "energy_reserve_fraction": reserve,
        "vtol_possible": vtol_possible,
        "endurance_passes": endurance_passes,
        "feasible": vtol_possible and endurance_passes,
        "fail_reason": "Cannot satisfy VTOL requirement - no runway on Mars",
    }


def _expected_hybrid_vtol() -> Dict[str, Any]:
    g = get_param("physical.mars.g")
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    mtow = get_param("mission.mass.mtow_kg")
    weight_n = mtow * g
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    disk_area = weight_n / disk_loading
    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    t_hover_s = get_param("mission.time.t_hover_s")
    t_cruise_min = get_param("mission.time.t_cruise_min")
    t_transition_s = get_param("mission.time.t_transition_s")
    n_transitions = get_param("mission.time.n_transitions")
    reserve = get_param("mission.energy.reserve_fraction")
    f_batt = get_param("mission.mass_fractions.f_battery")
    e_spec = get_param("battery.specifications.specific_energy_Wh_kg")
    dod = get_param("battery.utilization.depth_of_discharge")
    eta_dis = get_param("battery.utilization.discharge_efficiency")
    endurance_req = get_param("mission.requirements.endurance_min")

    fm = get_param("propulsion.rotor.figure_of_merit")
    eta_m = get_param("propulsion.electromechanical.eta_motor")
    eta_e = get_param("propulsion.electromechanical.eta_esc")
    eta_p = get_param("propulsion.electromechanical.eta_prop")

    ar = get_param("aerodynamic.wing.aspect_ratio")
    e = get_param("aerodynamic.wing.oswald_efficiency")
    cd0 = get_param("aerodynamic.drag_polar.cd0")
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    ld_penalty = get_param("aerodynamic.quadplane.ld_penalty_factor")
    ld_qp = ld_max * ld_penalty

    v_i = math.sqrt(disk_loading / (2 * rho))
    p_ideal = (weight_n**1.5) / math.sqrt(2 * rho * disk_area)
    p_hover = p_ideal / fm
    p_hover_elec = p_hover / (eta_m * eta_e)

    eta_cruise = eta_p * eta_m * eta_e
    p_cruise = (weight_n * v_cruise) / (ld_qp * eta_cruise)

    reference_energy_j = get_param("mission.transition.reference_energy_j")
    mars_scaling = get_param("mission.transition.mars_scaling_factor")
    ref_mtow_kg = get_param("mission.transition.reference_mtow_kg")
    mass_ratio = mtow / ref_mtow_kg
    per_transition_j = reference_energy_j * mass_ratio * mars_scaling
    per_transition_wh = per_transition_j / 3600.0
    total_transition_wh = per_transition_wh * n_transitions

    e_hover = p_hover_elec * (t_hover_s / 3600)
    e_cruise = p_cruise * (t_cruise_min / 60)
    e_mission_without_trans = e_hover + e_cruise
    e_mission = e_mission_without_trans + total_transition_wh
    e_reserve = e_mission * reserve
    e_required = e_mission + e_reserve

    battery_mass = f_batt * mtow
    total_energy = battery_mass * e_spec
    usable_energy = total_energy * dod * eta_dis

    margin_wh = usable_energy - e_required
    margin_pct = (margin_wh / e_required) * 100 if e_required > 0 else 0.0

    e_for_cruise = usable_energy * (1 - reserve) - e_hover - total_transition_wh
    if e_for_cruise > 0 and p_cruise > 0:
        cruise_time_min = (e_for_cruise / p_cruise) * 60
    else:
        cruise_time_min = 0.0
    endurance_min = (t_hover_s / 60) + (t_transition_s / 60) + cruise_time_min

    range_km = (v_cruise * cruise_time_min * 60) / 1000
    operational_radius_km = range_km / 2

    if e_hover > 0:
        fraction_of_hover = (total_transition_wh / e_hover) * 100
    else:
        fraction_of_hover = 0.0

    if e_mission_without_trans > 0:
        fraction_of_mission = (total_transition_wh / e_mission_without_trans) * 100
    else:
        fraction_of_mission = 0.0

    energy_feasible = usable_energy >= e_required
    endurance_passes = endurance_min >= endurance_req

    return {
        "mtow_kg": mtow,
        "weight_n": weight_n,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        "disk_loading_n_m2": disk_loading,
        "disk_area_m2": disk_area,
        "ld_max_pure": ld_max,
        "ld_penalty_factor": ld_penalty,
        "ld_quadplane": ld_qp,
        "figure_of_merit": fm,
        "eta_motor": eta_m,
        "eta_esc": eta_e,
        "eta_prop": eta_p,
        "eta_hover": fm * eta_m * eta_e,
        "eta_cruise": eta_cruise,
        "induced_velocity_m_s": v_i,
        "hover_power_w": p_hover_elec,
        "cruise_power_w": p_cruise,
        "hover_time_min": t_hover_s / 60,
        "cruise_time_min": cruise_time_min,
        "hover_energy_wh": e_hover,
        "transition_energy_wh": total_transition_wh,
        "cruise_energy_wh": e_cruise,
        "mission_energy_wh": e_mission,
        "mission_energy_without_trans_wh": e_mission_without_trans,
        "reserve_energy_wh": e_reserve,
        "required_energy_wh": e_required,
        "transition_per_phase_j": per_transition_j,
        "transition_per_phase_wh": per_transition_wh,
        "n_transitions": n_transitions,
        "transition_fraction_of_hover": fraction_of_hover,
        "transition_fraction_of_mission": fraction_of_mission,
        "battery_mass_kg": battery_mass,
        "total_energy_wh": total_energy,
        "usable_energy_wh": usable_energy,
        "margin_wh": margin_wh,
        "margin_percent": margin_pct,
        "endurance_min": endurance_min,
        "range_km": range_km,
        "operational_radius_km": operational_radius_km,
        "requirement_min": endurance_req,
        "feasible": energy_feasible and endurance_passes,
        "endurance_passes": endurance_passes,
        "energy_feasible": energy_feasible,
    }


def _expected_matching_chart() -> Dict[str, Any]:
    g = get_param("physical.mars.g")
    rho = get_param("environment.arcadia_planitia.density_kg_m3")
    mtow = get_param("mission.mass.mtow_kg")
    weight_n = mtow * g
    v_cruise = get_param("mission.velocity.v_cruise_m_s")
    disk_loading = get_param("geometry.rotor.disk_loading_N_m2")
    fm = get_param("propulsion.rotor.figure_of_merit")
    eta_m = get_param("propulsion.electromechanical.eta_motor")
    eta_e = get_param("propulsion.electromechanical.eta_esc")
    eta_p = get_param("propulsion.electromechanical.eta_prop")
    eta_hover = fm * eta_m * eta_e
    eta_cruise = eta_p * eta_m * eta_e
    ld_penalty = get_param("aerodynamic.quadplane.ld_penalty_factor")

    ar = get_param("aerodynamic.wing.aspect_ratio")
    e = get_param("aerodynamic.wing.oswald_efficiency")
    cd0 = get_param("aerodynamic.drag_polar.cd0")
    cl_max = get_param("aerodynamic.airfoil.cl_max")
    v_stall = get_param("mission.velocity.v_stall_m_s")
    v_min_factor = get_param("mission.velocity.v_min_factor")
    v_min = v_stall * v_min_factor

    k = 1 / (math.pi * ar * e)
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    ld_quad = ld_max * ld_penalty

    v_i = math.sqrt(disk_loading / (2 * rho))
    pw_hover = v_i / eta_hover
    ws_stall = 0.5 * rho * v_min**2 * cl_max

    def cruise_constraint(ws: float) -> float:
        cl = (2 * ws) / (rho * v_cruise**2)
        ld_pure = cl / (cd0 + k * cl**2)
        ld = ld_pure * ld_penalty
        return v_cruise / (ld * eta_cruise)

    pw_cruise_at_stall = cruise_constraint(ws_stall)
    pw_design = max(pw_hover, pw_cruise_at_stall)
    active = "hover" if pw_hover > pw_cruise_at_stall else "cruise"

    wing_area = weight_n / ws_stall
    wingspan = math.sqrt(ar * wing_area)
    chord = wing_area / wingspan
    installed_power = pw_design * weight_n
    disk_area = weight_n / disk_loading

    ws_range = np.linspace(2.0, 15.0, 50)
    pw_cruise_curve = np.array([cruise_constraint(ws) for ws in ws_range])
    pw_hover_line = np.full_like(ws_range, pw_hover)

    return {
        "mtow_kg": mtow,
        "weight_n": weight_n,
        "rho_kg_m3": rho,
        "v_cruise_m_s": v_cruise,
        "disk_loading_n_m2": disk_loading,
        "figure_of_merit": fm,
        "eta_hover": eta_hover,
        "eta_cruise": eta_cruise,
        "ld_max": ld_max,
        "ld_quadplane": ld_quad,
        "cl_max": cl_max,
        "hover_pw": pw_hover,
        "stall_ws": ws_stall,
        "induced_velocity_m_s": v_i,
        "design_point": {
            "wing_loading": ws_stall,
            "power_loading": pw_design,
            "hover_pw": pw_hover,
            "cruise_pw_at_stall": pw_cruise_at_stall,
            "stall_ws": ws_stall,
            "active_constraint": active,
        },
        "geometry": {
            "wing_area_m2": wing_area,
            "wingspan_m": wingspan,
            "chord_m": chord,
            "installed_power_w": installed_power,
            "disk_area_m2": disk_area,
        },
        "ws_range": ws_range,
        "pw_cruise_curve": pw_cruise_curve,
        "pw_hover_line": pw_hover_line,
    }


def verify_section3() -> List[VerificationResult]:
    results = []
    computed = atmospheric_model.arcadia_planitia_conditions()
    expected = _expected_arcadia_conditions()
    results.extend(_compare_dict("§3.1", expected, computed))
    return results


def verify_section4() -> List[VerificationResult]:
    results = []

    computed_aero = aerodynamic_calculations.drag_polar_analysis()
    expected_aero = _expected_aero()
    results.extend(_compare_dict("§4.7", expected_aero, computed_aero))

    computed_req = derived_requirements.derived_requirements_analysis()
    expected_req = _expected_derived_requirements()
    results.extend(_compare_dict("§4.12", expected_req, computed_req))

    computed_geom = geometry_calculations.geometry_analysis()
    expected_geom = _expected_geometry()
    results.extend(_compare_dict("§4 (Geometry)", expected_geom, computed_geom))

    return results


def verify_section5() -> List[VerificationResult]:
    results = []

    computed_rot = rotorcraft.rotorcraft_feasibility_analysis()
    expected_rot = _expected_rotorcraft()
    results.extend(_compare_dict("§5.1", expected_rot, computed_rot))

    computed_fw = fixed_wing.fixed_wing_feasibility_analysis()
    expected_fw = _expected_fixed_wing()
    results.extend(_compare_dict("§5.2", expected_fw, computed_fw))

    computed_hyb = hybrid_vtol.hybrid_vtol_feasibility_analysis()
    expected_hyb = _expected_hybrid_vtol()
    results.extend(_compare_dict("§5.3", expected_hyb, computed_hyb))

    computed_match = matching_chart.matching_chart_analysis()
    expected_match = _expected_matching_chart()
    results.extend(_compare_dict("§5.4", expected_match, computed_match))

    return results


def verify_all() -> Tuple[List[VerificationResult], int, int]:
    all_results: List[VerificationResult] = []
    all_results.extend(verify_section3())
    all_results.extend(verify_section4())
    all_results.extend(verify_section5())

    passed = sum(1 for r in all_results if r.passed)
    failed = len(all_results) - passed
    return all_results, passed, failed


def print_verification_report() -> bool:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 80)
    print("MANUSCRIPT VERIFICATION REPORT")
    print("=" * 80)
    print(f"Generated: {timestamp}")
    print()

    all_results, passed, failed = verify_all()

    sections: Dict[str, List[VerificationResult]] = {}
    for r in all_results:
        sections.setdefault(r.section, []).append(r)

    for section, results in sorted(sections.items()):
        print(f"\n{section}")
        print("-" * 50)
        for r in results:
            print(f"  {r}")

    print()
    print("=" * 80)
    print(f"SUMMARY: {passed}/{passed + failed} tests passed")
    if failed > 0:
        print(f"\nFAILURES: {failed} discrepancies found - review values")
    else:
        print("\nPASS: All calculations match expected values")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = print_verification_report()
    raise SystemExit(0 if success else 1)
