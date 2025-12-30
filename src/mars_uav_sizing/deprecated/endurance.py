"""
Endurance and Energy Module
===========================

Provides energy budget analysis and endurance calculations for Mars UAV,
including:
- Battery-only endurance
- Solar-augmented endurance
- Power budget breakdown
- Thermal considerations

References:
- Desert et al. (2017). Aerodynamic Design on a Martian Micro Air Vehicle.
- Barbato et al. (2024). Preliminary Design of a Fixed-Wing Drone for Mars.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import math

from .constants import G_MARS, SOLAR_SURFACE_CLEAR, SOLAR_SURFACE_DUSTY


@dataclass
class PowerBudget:
    """
    Power budget for UAV operations.

    Attributes
    ----------
    p_propulsion : float
        Propulsion power in W
    p_avionics : float
        Avionics power in W
    p_payload : float
        Payload power in W
    p_thermal : float
        Thermal management power in W
    p_comms : float
        Communications power in W
    """

    p_propulsion: float
    p_avionics: float = 15.0
    p_payload: float = 10.0
    p_thermal: float = 20.0
    p_comms: float = 8.0

    @property
    def total(self) -> float:
        """Total power consumption in W."""
        return self.p_propulsion + self.p_avionics + self.p_payload + self.p_thermal + self.p_comms

    def summary(self) -> str:
        """Generate power budget summary."""
        lines = [
            "Power Budget",
            "-" * 40,
            f"  Propulsion:    {self.p_propulsion:8.1f} W ({100*self.p_propulsion/self.total:5.1f}%)",
            f"  Avionics:      {self.p_avionics:8.1f} W ({100*self.p_avionics/self.total:5.1f}%)",
            f"  Payload:       {self.p_payload:8.1f} W ({100*self.p_payload/self.total:5.1f}%)",
            f"  Thermal:       {self.p_thermal:8.1f} W ({100*self.p_thermal/self.total:5.1f}%)",
            f"  Communications:{self.p_comms:8.1f} W ({100*self.p_comms/self.total:5.1f}%)",
            "-" * 40,
            f"  Total:         {self.total:8.1f} W",
        ]
        return "\n".join(lines)


@dataclass
class MissionPhase:
    """
    Single mission phase energy consumption.

    Attributes
    ----------
    name : str
        Phase name
    duration_s : float
        Duration in seconds
    power_w : float
        Average power in Watts
    """

    name: str
    duration_s: float
    power_w: float

    @property
    def energy_wh(self) -> float:
        """Energy consumed in Wh."""
        return self.power_w * self.duration_s / 3600.0


class EnduranceCalculator:
    """
    Endurance and energy calculations for Mars UAV.

    Parameters
    ----------
    battery_capacity_wh : float
        Battery capacity in Wh
    battery_efficiency : float
        Battery discharge efficiency (default: 0.95)
    reserve_fraction : float
        Energy reserve fraction (default: 0.20)
    thermal_penalty : float
        Energy allocated to thermal management (fraction, default: 0.10)
    """

    def __init__(
        self,
        battery_capacity_wh: float,
        battery_efficiency: float = 0.95,
        reserve_fraction: float = 0.20,
        thermal_penalty: float = 0.10,
    ):
        self.battery_capacity = battery_capacity_wh
        self.battery_efficiency = battery_efficiency
        self.reserve_fraction = reserve_fraction
        self.thermal_penalty = thermal_penalty

    @property
    def usable_energy(self) -> float:
        """Usable energy in Wh after reserves and thermal."""
        return self.battery_capacity * self.battery_efficiency * (
            1.0 - self.reserve_fraction - self.thermal_penalty
        )

    def endurance_battery_only(
        self,
        cruise_power: float,
        hover_power: float,
        hover_time_s: float = 120.0,
        transition_power: float = 600.0,
        transition_time_s: float = 60.0,
    ) -> Tuple[float, dict]:
        """
        Calculate endurance for battery-only configuration.

        Parameters
        ----------
        cruise_power : float
            Cruise propulsion power in W
        hover_power : float
            Hover power in W
        hover_time_s : float
            Total hover time (takeoff + landing) in seconds
        transition_power : float
            Transition phase power in W
        transition_time_s : float
            Total transition time in seconds

        Returns
        -------
        tuple
            (endurance_hours, energy_breakdown_dict)
        """
        # Energy for hover phases
        e_hover = hover_power * hover_time_s / 3600.0

        # Energy for transitions
        e_transition = transition_power * transition_time_s / 3600.0

        # Available for cruise
        e_cruise_available = self.usable_energy - e_hover - e_transition

        # Endurance
        if cruise_power > 0:
            endurance_h = e_cruise_available / cruise_power
        else:
            endurance_h = 0.0

        breakdown = {
            "battery_capacity_wh": self.battery_capacity,
            "usable_energy_wh": self.usable_energy,
            "hover_energy_wh": e_hover,
            "transition_energy_wh": e_transition,
            "cruise_energy_wh": e_cruise_available,
            "cruise_power_w": cruise_power,
            "endurance_h": max(0, endurance_h),
        }

        return max(0, endurance_h), breakdown

    def endurance_solar_augmented(
        self,
        cruise_power: float,
        solar_power: float,
        hover_power: float,
        hover_time_s: float = 120.0,
        transition_power: float = 600.0,
        transition_time_s: float = 60.0,
        solar_availability: float = 0.8,
    ) -> Tuple[float, dict]:
        """
        Calculate endurance with solar augmentation.

        Parameters
        ----------
        cruise_power : float
            Cruise propulsion power in W
        solar_power : float
            Peak solar power generation in W
        hover_power : float
            Hover power in W
        hover_time_s : float
            Total hover time in seconds
        transition_power : float
            Transition phase power in W
        transition_time_s : float
            Total transition time in seconds
        solar_availability : float
            Fraction of cruise time with good solar (default: 0.8)

        Returns
        -------
        tuple
            (endurance_hours, energy_breakdown_dict)
        """
        # Energy for hover phases (no solar benefit during hover)
        e_hover = hover_power * hover_time_s / 3600.0

        # Energy for transitions
        e_transition = transition_power * transition_time_s / 3600.0

        # Net cruise power (solar reduces battery draw)
        effective_solar = solar_power * solar_availability
        net_cruise_power = max(0, cruise_power - effective_solar)

        # Available for cruise
        e_cruise_available = self.usable_energy - e_hover - e_transition

        # Endurance
        if net_cruise_power > 0:
            endurance_h = e_cruise_available / net_cruise_power
        else:
            # Solar exceeds cruise requirement - effectively unlimited by power
            # Limited by daylight (~6 hours on Mars)
            endurance_h = 6.0  # Cap at reasonable daylight duration

        breakdown = {
            "battery_capacity_wh": self.battery_capacity,
            "usable_energy_wh": self.usable_energy,
            "hover_energy_wh": e_hover,
            "transition_energy_wh": e_transition,
            "cruise_energy_wh": e_cruise_available,
            "gross_cruise_power_w": cruise_power,
            "solar_power_w": solar_power,
            "effective_solar_w": effective_solar,
            "net_cruise_power_w": net_cruise_power,
            "endurance_h": endurance_h,
        }

        return endurance_h, breakdown

    def range_from_endurance(
        self,
        endurance_h: float,
        cruise_speed_m_s: float,
    ) -> float:
        """
        Calculate range from endurance and cruise speed.

        Parameters
        ----------
        endurance_h : float
            Endurance in hours
        cruise_speed_m_s : float
            Cruise speed in m/s

        Returns
        -------
        float
            Range in km
        """
        return endurance_h * cruise_speed_m_s * 3.6  # Convert to km

    def operational_radius(
        self,
        endurance_h: float,
        cruise_speed_m_s: float,
        loiter_fraction: float = 0.1,
    ) -> float:
        """
        Calculate operational radius accounting for return flight.

        Parameters
        ----------
        endurance_h : float
            Total endurance in hours
        cruise_speed_m_s : float
            Cruise speed in m/s
        loiter_fraction : float
            Fraction of time allocated to loiter/mapping (default: 0.1)

        Returns
        -------
        float
            Operational radius in km
        """
        # Available for transit (out + back)
        transit_time = endurance_h * (1.0 - loiter_fraction)
        one_way_time = transit_time / 2.0

        return one_way_time * cruise_speed_m_s * 3.6  # km


def hover_power(
    weight_n: float,
    disk_area_m2: float,
    rho: float,
    figure_of_merit: float = 0.6,
) -> float:
    """
    Calculate hover power using momentum theory.

    P = T * sqrt(T / (2 * rho * A)) / FM

    For hover: T = W

    Parameters
    ----------
    weight_n : float
        Weight on Mars in N
    disk_area_m2 : float
        Total rotor disk area in m²
    rho : float
        Air density in kg/m³
    figure_of_merit : float
        Rotor figure of merit (default: 0.6)

    Returns
    -------
    float
        Hover power in W
    """
    thrust = weight_n
    induced_velocity = math.sqrt(thrust / (2.0 * rho * disk_area_m2))
    ideal_power = thrust * induced_velocity
    return ideal_power / figure_of_merit


def solar_power_available(
    array_area_m2: float,
    cell_efficiency: float = 0.30,
    irradiance_w_m2: float = SOLAR_SURFACE_CLEAR,
    incidence_factor: float = 0.7,
    dust_factor: float = 0.9,
) -> float:
    """
    Calculate available solar power.

    Parameters
    ----------
    array_area_m2 : float
        Solar array area in m²
    cell_efficiency : float
        Solar cell efficiency (default: 0.30 for triple-junction)
    irradiance_w_m2 : float
        Solar irradiance at surface in W/m²
    incidence_factor : float
        Average cosine factor for sun angle (default: 0.7)
    dust_factor : float
        Transmission factor due to dust (default: 0.9)

    Returns
    -------
    float
        Available solar power in W
    """
    return array_area_m2 * cell_efficiency * irradiance_w_m2 * incidence_factor * dust_factor


def mission_energy_breakdown(
    weight_n: float,
    rho: float,
    cruise_power: float,
    disk_area_m2: float,
    takeoff_hover_s: float = 60.0,
    landing_hover_s: float = 60.0,
    transition_time_s: float = 30.0,
    cruise_time_s: float = 3600.0,
) -> dict:
    """
    Calculate energy breakdown for complete mission.

    Parameters
    ----------
    weight_n : float
        Weight on Mars in N
    rho : float
        Air density in kg/m³
    cruise_power : float
        Cruise power in W
    disk_area_m2 : float
        Total rotor disk area in m²
    takeoff_hover_s : float
        Takeoff hover duration in seconds
    landing_hover_s : float
        Landing hover duration in seconds
    transition_time_s : float
        Transition phase duration (each way) in seconds
    cruise_time_s : float
        Cruise duration in seconds

    Returns
    -------
    dict
        Mission energy breakdown
    """
    # Hover power
    p_hover = hover_power(weight_n, disk_area_m2, rho)

    # Transition power (average of hover and cruise)
    p_transition = (p_hover + cruise_power) / 2.0

    # Phase energies
    phases = [
        MissionPhase("Takeoff hover", takeoff_hover_s, p_hover),
        MissionPhase("Climb transition", transition_time_s, p_transition),
        MissionPhase("Cruise (outbound)", cruise_time_s / 2, cruise_power),
        MissionPhase("Cruise (return)", cruise_time_s / 2, cruise_power),
        MissionPhase("Descent transition", transition_time_s, p_transition),
        MissionPhase("Landing hover", landing_hover_s, p_hover),
    ]

    total_energy = sum(p.energy_wh for p in phases)
    total_time = sum(p.duration_s for p in phases)

    return {
        "phases": phases,
        "total_energy_wh": total_energy,
        "total_time_s": total_time,
        "hover_power_w": p_hover,
        "cruise_power_w": cruise_power,
        "transition_power_w": p_transition,
    }


if __name__ == "__main__":
    from .constants import RHO_ARCADIA

    print("Endurance Calculator - Validation")
    print("=" * 60)

    # Configuration A: 7.5 kg battery-only
    print("\n--- Configuration A (7.5 kg battery-only) ---")

    mass_a = 7.5
    weight_a = mass_a * G_MARS  # 27.8 N
    battery_wh_a = 390  # Wh
    cruise_power_a = 200  # W

    # Hover power estimate (8 rotors, 0.3m radius each)
    disk_area_a = 8 * math.pi * 0.30**2  # 8 × 0.28 m² = 2.26 m²
    p_hover_a = hover_power(weight_a, disk_area_a, RHO_ARCADIA)

    calc_a = EnduranceCalculator(
        battery_capacity_wh=battery_wh_a,
        reserve_fraction=0.20,
        thermal_penalty=0.10,
    )

    endurance_a, breakdown_a = calc_a.endurance_battery_only(
        cruise_power=cruise_power_a,
        hover_power=p_hover_a,
        hover_time_s=120,
        transition_time_s=60,
    )

    range_a = calc_a.range_from_endurance(endurance_a, 40.0)
    radius_a = calc_a.operational_radius(endurance_a, 40.0)

    print(f"  Weight on Mars: {weight_a:.1f} N")
    print(f"  Battery: {battery_wh_a} Wh")
    print(f"  Hover power: {p_hover_a:.0f} W")
    print(f"  Cruise power: {cruise_power_a} W")
    print(f"  Endurance: {endurance_a:.2f} hours ({endurance_a*60:.0f} min)")
    print(f"  Range: {range_a:.0f} km")
    print(f"  Operational radius: {radius_a:.0f} km")

    # Configuration B: 24 kg solar-augmented
    print("\n--- Configuration B (24 kg solar-augmented) ---")

    mass_b = 24.0
    weight_b = mass_b * G_MARS  # 89 N
    battery_wh_b = 300  # Wh
    cruise_power_b = 500  # W (higher for larger aircraft)

    # Hover power estimate (4 larger rotors)
    disk_area_b = 4 * math.pi * 0.75**2  # 4 × 1.77 m² = 7.07 m²
    p_hover_b = hover_power(weight_b, disk_area_b, RHO_ARCADIA)

    # Solar power
    solar_area = 6.0  # m²
    p_solar = solar_power_available(solar_area, cell_efficiency=0.30)

    calc_b = EnduranceCalculator(
        battery_capacity_wh=battery_wh_b,
        reserve_fraction=0.15,
        thermal_penalty=0.10,
    )

    endurance_b, breakdown_b = calc_b.endurance_solar_augmented(
        cruise_power=cruise_power_b,
        solar_power=p_solar,
        hover_power=p_hover_b,
        hover_time_s=120,
        transition_time_s=60,
    )

    range_b = calc_b.range_from_endurance(endurance_b, 35.0)
    radius_b = calc_b.operational_radius(endurance_b, 35.0)

    print(f"  Weight on Mars: {weight_b:.1f} N")
    print(f"  Battery: {battery_wh_b} Wh")
    print(f"  Solar array: {solar_area} m² → {p_solar:.0f} W")
    print(f"  Hover power: {p_hover_b:.0f} W")
    print(f"  Gross cruise power: {cruise_power_b} W")
    print(f"  Net cruise power: {breakdown_b['net_cruise_power_w']:.0f} W")
    print(f"  Endurance: {endurance_b:.2f} hours ({endurance_b*60:.0f} min)")
    print(f"  Range: {range_b:.0f} km")
    print(f"  Operational radius: {radius_b:.0f} km")
