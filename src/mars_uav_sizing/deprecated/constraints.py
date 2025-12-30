"""
Constraint-Based Sizing Module
==============================

Implements power-based matching chart methodology for electric VTOL aircraft,
adapted from thrust-based approach in matchingcharts.m for Mars conditions.

The sizing problem solves a system of constraint equations:
1. Hover power constraint (VTOL capability)
2. Cruise power constraint (level flight)
3. Climb power constraint (rate of climb)
4. Stall speed constraint (wing loading limit)
5. Endurance/range constraint (mission requirement)

References:
- Adapted from matchingcharts.m (Earth jet aircraft sizing)
- Raymer, D. (2018). Aircraft Design: A Conceptual Approach.
- Gundlach, J. (2012). Designing Unmanned Aircraft Systems.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List
import math
import numpy as np
from scipy.optimize import fsolve

from .constants import G_MARS, RHO_ARCADIA
from .aerodynamics import DragPolar, cruise_cl


@dataclass
class DesignPoint:
    """
    Design point from constraint analysis.

    Attributes
    ----------
    wing_loading : float
        Wing loading W/S in N/m²
    power_loading : float
        Power loading P/W in W/N
    weight : float
        Total weight in N
    wing_area : float
        Wing area in m²
    power_required : float
        Total power required in W
    aspect_ratio : float
        Wing aspect ratio
    """

    wing_loading: float  # N/m²
    power_loading: float  # W/N
    weight: float  # N
    wing_area: float  # m²
    power_required: float  # W
    aspect_ratio: float


class SizingConstraints:
    """
    Constraint-based sizing for Mars electric VTOL UAV.

    Parameters
    ----------
    rho : float
        Air density in kg/m³
    polar : DragPolar
        Drag polar model
    eta_prop : float
        Cruise propeller efficiency
    eta_hover : float
        Hover figure of merit
    """

    def __init__(
        self,
        rho: float = RHO_ARCADIA,
        polar: Optional[DragPolar] = None,
        eta_prop: float = 0.65,
        eta_hover: float = 0.6,
    ):
        self.rho = rho
        self.polar = polar if polar else DragPolar(cd0=0.015, aspect_ratio=12.0)
        self.eta_prop = eta_prop
        self.eta_hover = eta_hover  # Figure of merit for VTOL

    def hover_power_loading(
        self,
        wing_loading: float,
        disk_loading: float,
        thrust_margin: float = 1.5,
    ) -> float:
        """
        Calculate power loading required for hover.

        Uses momentum theory: P_hover = T^1.5 / (FM * sqrt(2 * rho * A_disk))

        For VTOL: T = thrust_margin * W

        P/W = (T/W)^1.5 * sqrt(W/S) / (FM * sqrt(2 * rho * (S/DL)))

        Simplified: P/W = thrust_margin^1.5 * sqrt(DL / (2 * rho)) / FM

        Parameters
        ----------
        wing_loading : float
            Wing loading W/S in N/m²
        disk_loading : float
            Rotor disk loading T/A in N/m²
        thrust_margin : float
            Thrust-to-weight ratio for hover (default: 1.5)

        Returns
        -------
        float
            Required P/W in W/N
        """
        # Power required per unit thrust (momentum theory)
        # P = T * sqrt(T / (2 * rho * A))
        # For disk loading DL = T/A:
        # P = T * sqrt(DL / (2 * rho))

        # Power loading (P/W) = (T/W) * sqrt(DL / (2 * rho)) / FM
        p_w = thrust_margin * math.sqrt(disk_loading / (2.0 * self.rho)) / self.eta_hover

        return p_w

    def cruise_power_loading(
        self,
        wing_loading: float,
        velocity: float,
    ) -> float:
        """
        Calculate power loading required for steady level cruise.

        P/W = V * CD / CL / eta_prop
            = V * (CD0 + CL^2/(pi*AR*e)) / CL / eta_prop

        where CL = 2 * (W/S) / (rho * V^2)

        Parameters
        ----------
        wing_loading : float
            Wing loading W/S in N/m²
        velocity : float
            Cruise velocity in m/s

        Returns
        -------
        float
            Required P/W in W/N
        """
        q = 0.5 * self.rho * velocity**2

        # Lift coefficient at cruise
        cl = wing_loading / q

        # Drag coefficient
        cd = self.polar.cd(cl)

        # Power loading
        p_w = velocity * cd / cl / self.eta_prop

        return p_w

    def climb_power_loading(
        self,
        wing_loading: float,
        velocity: float,
        rate_of_climb: float,
    ) -> float:
        """
        Calculate power loading required for steady climb.

        P/W = ROC + V * CD / CL / eta_prop

        Parameters
        ----------
        wing_loading : float
            Wing loading W/S in N/m²
        velocity : float
            Climb velocity in m/s
        rate_of_climb : float
            Rate of climb in m/s

        Returns
        -------
        float
            Required P/W in W/N
        """
        q = 0.5 * self.rho * velocity**2
        cl = wing_loading / q
        cd = self.polar.cd(cl)

        # Excess power for climb + cruise power
        p_w = rate_of_climb + velocity * cd / cl / self.eta_prop

        return p_w

    def stall_constraint(
        self,
        v_stall: float,
        cl_max: float,
    ) -> float:
        """
        Calculate maximum wing loading from stall speed.

        W/S = 0.5 * rho * V_stall^2 * CL_max

        Parameters
        ----------
        v_stall : float
            Maximum allowable stall speed in m/s
        cl_max : float
            Maximum lift coefficient

        Returns
        -------
        float
            Maximum wing loading in N/m²
        """
        return 0.5 * self.rho * v_stall**2 * cl_max

    def gust_load_factor(
        self,
        wing_loading: float,
        velocity: float,
        gust_velocity: float,
        cl_alpha: float = 5.7,  # per radian
    ) -> float:
        """
        Calculate load factor from gust encounter.

        Delta_n = rho * V * w * CL_alpha / (2 * W/S)

        where w is gust velocity.

        Parameters
        ----------
        wing_loading : float
            Wing loading W/S in N/m²
        velocity : float
            Flight velocity in m/s
        gust_velocity : float
            Gust velocity in m/s
        cl_alpha : float
            Lift curve slope in per radian

        Returns
        -------
        float
            Incremental load factor from gust
        """
        return self.rho * velocity * gust_velocity * cl_alpha / (2.0 * wing_loading)

    def endurance_constraint(
        self,
        weight: float,
        wing_area: float,
        battery_energy: float,
        velocity: float,
        reserve_fraction: float = 0.20,
        hover_energy: float = 0.0,
    ) -> float:
        """
        Calculate achievable endurance from battery energy.

        Parameters
        ----------
        weight : float
            Total weight in N
        wing_area : float
            Wing area in m²
        battery_energy : float
            Battery energy in Wh
        velocity : float
            Cruise velocity in m/s
        reserve_fraction : float
            Energy reserve fraction (default: 0.20)
        hover_energy : float
            Energy consumed in hover/transition in Wh

        Returns
        -------
        float
            Endurance in hours
        """
        wing_loading = weight / wing_area
        p_w = self.cruise_power_loading(wing_loading, velocity)
        p_cruise = p_w * weight  # Watts

        # Available energy for cruise
        e_available = battery_energy * (1.0 - reserve_fraction) - hover_energy

        # Endurance in hours
        endurance = e_available / p_cruise

        return endurance

    def generate_constraint_diagram(
        self,
        wing_loading_range: Tuple[float, float] = (5.0, 50.0),
        n_points: int = 100,
        v_cruise: float = 40.0,
        v_stall: float = 30.0,
        cl_max: float = 0.9,
        disk_loading: float = 30.0,
        rate_of_climb: float = 2.0,
        thrust_margin: float = 1.5,
    ) -> dict:
        """
        Generate constraint diagram data.

        Parameters
        ----------
        wing_loading_range : tuple
            Range of wing loadings to evaluate (W/S)_min, (W/S)_max in N/m²
        n_points : int
            Number of points to compute
        v_cruise : float
            Cruise velocity in m/s
        v_stall : float
            Stall speed in m/s
        cl_max : float
            Maximum lift coefficient
        disk_loading : float
            Hover disk loading in N/m²
        rate_of_climb : float
            Required rate of climb in m/s
        thrust_margin : float
            Hover thrust margin

        Returns
        -------
        dict
            Dictionary containing:
            - wing_loading: array of W/S values
            - p_w_hover: hover constraint line
            - p_w_cruise: cruise constraint line
            - p_w_climb: climb constraint line
            - ws_stall: stall constraint (vertical line)
        """
        ws = np.linspace(wing_loading_range[0], wing_loading_range[1], n_points)

        # Compute constraint lines
        p_w_hover = np.array([self.hover_power_loading(w, disk_loading, thrust_margin) for w in ws])
        p_w_cruise = np.array([self.cruise_power_loading(w, v_cruise) for w in ws])
        p_w_climb = np.array([self.climb_power_loading(w, v_cruise * 0.8, rate_of_climb) for w in ws])

        # Stall constraint
        ws_stall = self.stall_constraint(v_stall, cl_max)

        return {
            "wing_loading": ws,
            "p_w_hover": p_w_hover,
            "p_w_cruise": p_w_cruise,
            "p_w_climb": p_w_climb,
            "ws_stall": ws_stall,
        }

    def find_design_point(
        self,
        target_weight: float,
        v_cruise: float = 40.0,
        v_stall: float = 30.0,
        cl_max: float = 0.9,
        disk_loading: float = 30.0,
        thrust_margin: float = 1.5,
    ) -> DesignPoint:
        """
        Find optimal design point satisfying all constraints.

        Selects highest feasible wing loading (smallest wing) that satisfies
        stall and power constraints.

        Parameters
        ----------
        target_weight : float
            Target weight in N
        v_cruise : float
            Cruise velocity in m/s
        v_stall : float
            Stall speed in m/s
        cl_max : float
            Maximum lift coefficient
        disk_loading : float
            Hover disk loading in N/m²
        thrust_margin : float
            Hover thrust margin

        Returns
        -------
        DesignPoint
            Selected design point
        """
        # Maximum wing loading from stall
        ws_max = self.stall_constraint(v_stall, cl_max)

        # Use stall-limited wing loading (conservative)
        ws = ws_max * 0.95  # 5% margin

        # Calculate required power loadings
        p_w_hover = self.hover_power_loading(ws, disk_loading, thrust_margin)
        p_w_cruise = self.cruise_power_loading(ws, v_cruise)

        # Take maximum (most demanding constraint)
        p_w = max(p_w_hover, p_w_cruise)

        # Calculate derived quantities
        wing_area = target_weight / ws
        power_required = p_w * target_weight

        return DesignPoint(
            wing_loading=ws,
            power_loading=p_w,
            weight=target_weight,
            wing_area=wing_area,
            power_required=power_required,
            aspect_ratio=self.polar.aspect_ratio,
        )


def sizing_iteration(
    payload_mass: float,
    battery_energy_density: float = 150.0,  # Wh/kg
    target_endurance: float = 1.0,  # hours
    v_cruise: float = 40.0,  # m/s
    rho: float = RHO_ARCADIA,
    cd0: float = 0.015,
    aspect_ratio: float = 12.0,
    oswald_e: float = 0.85,
    eta_prop: float = 0.65,
    empty_weight_fraction: float = 0.55,
    solar_power: float = 0.0,  # Watts during cruise
    max_iterations: int = 20,
    tolerance: float = 0.01,
) -> dict:
    """
    Iterative sizing to converge on consistent MTOW.

    Parameters
    ----------
    payload_mass : float
        Payload mass in kg
    battery_energy_density : float
        Battery specific energy in Wh/kg
    target_endurance : float
        Target cruise endurance in hours
    v_cruise : float
        Cruise velocity in m/s
    rho : float
        Air density in kg/m³
    cd0 : float
        Zero-lift drag coefficient
    aspect_ratio : float
        Wing aspect ratio
    oswald_e : float
        Oswald efficiency factor
    eta_prop : float
        Propeller efficiency
    empty_weight_fraction : float
        Empty weight fraction (structure/avionics/motors)
    solar_power : float
        Solar power contribution during cruise in Watts
    max_iterations : int
        Maximum iterations
    tolerance : float
        Convergence tolerance (fraction)

    Returns
    -------
    dict
        Sizing results including:
        - mtow_kg: maximum takeoff mass in kg
        - battery_mass_kg: battery mass in kg
        - wing_area_m2: wing area in m²
        - wingspan_m: wingspan in m
        - cruise_power_w: cruise power in W
        - endurance_h: achieved endurance in hours
        - converged: whether iteration converged
    """
    polar = DragPolar(cd0=cd0, aspect_ratio=aspect_ratio, oswald_efficiency=oswald_e)
    constraints = SizingConstraints(rho=rho, polar=polar, eta_prop=eta_prop)

    # Initial guess
    mtow_kg = payload_mass / (1.0 - empty_weight_fraction - 0.35)  # Assume 35% battery

    for iteration in range(max_iterations):
        weight_n = mtow_kg * G_MARS

        # Find design point
        dp = constraints.find_design_point(
            target_weight=weight_n,
            v_cruise=v_cruise,
            v_stall=30.0,
            cl_max=0.9,
        )

        # Cruise power (accounting for solar)
        p_cruise_gross = constraints.cruise_power_loading(dp.wing_loading, v_cruise) * weight_n
        p_cruise_net = max(0.0, p_cruise_gross - solar_power)

        # Required battery energy for target endurance
        # Add 20% reserve + 10% for hover/transition
        e_required = p_cruise_net * target_endurance / 0.70  # Wh

        # Battery mass
        battery_mass = e_required / battery_energy_density

        # New MTOW estimate
        mtow_new = payload_mass / (1.0 - empty_weight_fraction - battery_mass / mtow_kg)

        # Check convergence
        if abs(mtow_new - mtow_kg) / mtow_kg < tolerance:
            mtow_kg = mtow_new
            break

        # Update for next iteration (with damping)
        mtow_kg = 0.5 * mtow_kg + 0.5 * mtow_new

    # Final calculations
    weight_n = mtow_kg * G_MARS
    dp = constraints.find_design_point(target_weight=weight_n, v_cruise=v_cruise)

    wingspan = math.sqrt(dp.wing_area * aspect_ratio)

    return {
        "mtow_kg": mtow_kg,
        "weight_n": weight_n,
        "payload_mass_kg": payload_mass,
        "battery_mass_kg": battery_mass,
        "structure_mass_kg": mtow_kg * empty_weight_fraction,
        "wing_area_m2": dp.wing_area,
        "wingspan_m": wingspan,
        "wing_loading_n_m2": dp.wing_loading,
        "cruise_power_w": p_cruise_gross,
        "net_cruise_power_w": p_cruise_net,
        "endurance_h": target_endurance,
        "aspect_ratio": aspect_ratio,
        "converged": iteration < max_iterations - 1,
        "iterations": iteration + 1,
    }


if __name__ == "__main__":
    print("Constraint-Based Sizing - Validation")
    print("=" * 60)

    # Configuration A: 7.5 kg battery-only
    print("\n--- Configuration A: Battery-Only (7.5 kg target) ---")
    result_a = sizing_iteration(
        payload_mass=0.5,
        battery_energy_density=150.0,
        target_endurance=1.0,
        v_cruise=40.0,
        aspect_ratio=12.0,
        empty_weight_fraction=0.55,
        solar_power=0.0,
    )

    print(f"  MTOW: {result_a['mtow_kg']:.2f} kg")
    print(f"  Battery: {result_a['battery_mass_kg']:.2f} kg")
    print(f"  Wing area: {result_a['wing_area_m2']:.2f} m²")
    print(f"  Wingspan: {result_a['wingspan_m']:.2f} m")
    print(f"  Cruise power: {result_a['cruise_power_w']:.0f} W")
    print(f"  Converged: {result_a['converged']}")

    # Configuration B: 24 kg solar-augmented
    print("\n--- Configuration B: Solar-Augmented (24 kg target) ---")
    result_b = sizing_iteration(
        payload_mass=2.5,
        battery_energy_density=150.0,
        target_endurance=2.0,
        v_cruise=35.0,
        aspect_ratio=6.0,
        empty_weight_fraction=0.50,
        solar_power=400.0,  # 400W solar contribution
    )

    print(f"  MTOW: {result_b['mtow_kg']:.2f} kg")
    print(f"  Battery: {result_b['battery_mass_kg']:.2f} kg")
    print(f"  Wing area: {result_b['wing_area_m2']:.2f} m²")
    print(f"  Wingspan: {result_b['wingspan_m']:.2f} m")
    print(f"  Cruise power (gross): {result_b['cruise_power_w']:.0f} W")
    print(f"  Net power from battery: {result_b['net_cruise_power_w']:.0f} W")
    print(f"  Converged: {result_b['converged']}")
