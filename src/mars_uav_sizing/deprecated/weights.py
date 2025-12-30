"""
Weight Estimation Module
========================

Provides weight estimation methods for Mars UAV components using:
- Statistical methods (Sadraey, Roskam, Torenbeek)
- Component buildup
- Mars-specific adaptations

References:
- Sadraey, M.H. (2013). Aircraft Design: A Systems Engineering Approach.
- Roskam, J. (2005). Airplane Design Part I: Preliminary Sizing of Airplanes.
- Adapted from matchingcharts.m wing mass equation (Sadraey Eq. 10.3)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import math

from .constants import G_EARTH, G_MARS


@dataclass
class ComponentMass:
    """
    Individual component mass specification.

    Attributes
    ----------
    name : str
        Component name
    mass_kg : float
        Mass in kg
    category : str
        Category (payload, propulsion, structure, avionics, energy)
    part_number : str, optional
        Part number or specification
    notes : str, optional
        Additional notes
    """

    name: str
    mass_kg: float
    category: str
    part_number: str = ""
    notes: str = ""


@dataclass
class MassBreakdown:
    """
    Complete mass breakdown for UAV.

    Attributes
    ----------
    components : list
        List of ComponentMass objects
    """

    components: List[ComponentMass] = field(default_factory=list)

    def add(self, component: ComponentMass) -> None:
        """Add a component to the breakdown."""
        self.components.append(component)

    @property
    def total_mass(self) -> float:
        """Total mass in kg."""
        return sum(c.mass_kg for c in self.components)

    @property
    def weight_mars(self) -> float:
        """Total weight on Mars in N."""
        return self.total_mass * G_MARS

    @property
    def weight_earth(self) -> float:
        """Total weight on Earth in N."""
        return self.total_mass * G_EARTH

    def by_category(self) -> Dict[str, float]:
        """Get mass by category."""
        categories = {}
        for c in self.components:
            if c.category not in categories:
                categories[c.category] = 0.0
            categories[c.category] += c.mass_kg
        return categories

    def summary(self) -> str:
        """Generate summary string."""
        lines = ["Mass Breakdown", "=" * 50]

        by_cat = self.by_category()
        for cat, mass in sorted(by_cat.items()):
            lines.append(f"{cat:20s}: {mass:8.3f} kg ({100*mass/self.total_mass:5.1f}%)")

        lines.append("-" * 50)
        lines.append(f"{'Total':20s}: {self.total_mass:8.3f} kg")
        lines.append(f"{'Weight (Mars)':20s}: {self.weight_mars:8.2f} N")

        return "\n".join(lines)


class WeightEstimation:
    """
    Weight estimation methods for Mars UAV.

    Provides both statistical and component-buildup approaches.
    """

    @staticmethod
    def wing_mass_sadraey(
        wing_area: float,
        chord_mac: float,
        thickness_ratio: float,
        aspect_ratio: float,
        n_ultimate: float = 3.8,
        sweep_deg: float = 0.0,
        taper_ratio: float = 0.4,
        rho_material: float = 1600.0,  # Carbon composite
        k_rho: float = 0.0025,  # Factor for UAV-class aircraft
    ) -> float:
        """
        Estimate wing mass using Sadraey's method (Eq. 10.3).

        Adapted from matchingcharts.m:
        Q_ala = S * c_mac * t/c * rho_mat * K_rho *
                ((AR * N_ult)/cos(sweep))^0.6 * taper^0.04

        Parameters
        ----------
        wing_area : float
            Wing planform area in m²
        chord_mac : float
            Mean aerodynamic chord in m
        thickness_ratio : float
            Maximum thickness to chord ratio (t/c)
        aspect_ratio : float
            Wing aspect ratio
        n_ultimate : float
            Ultimate load factor (default: 3.8 for UAV)
        sweep_deg : float
            Wing sweep at quarter chord in degrees
        taper_ratio : float
            Wing taper ratio (c_tip/c_root)
        rho_material : float
            Material density in kg/m³ (default: 1600 for CFRP)
        k_rho : float
            Empirical density factor (default: 0.0025 for small UAV)

        Returns
        -------
        float
            Estimated wing mass in kg
        """
        sweep_rad = math.radians(sweep_deg)
        cos_sweep = max(0.1, math.cos(sweep_rad))

        mass = (
            wing_area
            * chord_mac
            * thickness_ratio
            * rho_material
            * k_rho
            * ((aspect_ratio * n_ultimate) / cos_sweep) ** 0.6
            * taper_ratio**0.04
        )

        return mass

    @staticmethod
    def fuselage_mass_fraction(
        mtow_kg: float,
        fuselage_length: float,
        n_ultimate: float = 3.8,
    ) -> float:
        """
        Estimate fuselage mass using simple correlation.

        Adapted from matchingcharts.m:
        Q_fus = (1/1000) * N_ult * W * L_fus

        For Mars UAV, use lighter scaling (composite construction).

        Parameters
        ----------
        mtow_kg : float
            Maximum takeoff mass in kg
        fuselage_length : float
            Fuselage length in m
        n_ultimate : float
            Ultimate load factor

        Returns
        -------
        float
            Estimated fuselage mass in kg
        """
        # Simplified correlation for UAV-class vehicles
        return 0.0005 * n_ultimate * mtow_kg * fuselage_length

    @staticmethod
    def tail_mass_fraction(wing_mass: float, tail_volume_ratio: float = 0.15) -> float:
        """
        Estimate tail surfaces mass as fraction of wing mass.

        Parameters
        ----------
        wing_mass : float
            Wing mass in kg
        tail_volume_ratio : float
            Combined horizontal + vertical tail area / wing area

        Returns
        -------
        float
            Estimated tail mass in kg
        """
        return wing_mass * tail_volume_ratio

    @staticmethod
    def propulsion_mass_vtol(
        n_lift_motors: int,
        motor_mass: float,
        esc_mass: float,
        prop_mass: float,
        cruise_motor_mass: float = 0.3,
        cruise_esc_mass: float = 0.05,
        cruise_prop_mass: float = 0.1,
    ) -> float:
        """
        Estimate total VTOL propulsion system mass.

        Parameters
        ----------
        n_lift_motors : int
            Number of lift motors (e.g., 8 for octocopter)
        motor_mass : float
            Mass per lift motor in kg
        esc_mass : float
            Mass per ESC in kg
        prop_mass : float
            Mass per propeller in kg
        cruise_motor_mass : float
            Cruise motor mass in kg
        cruise_esc_mass : float
            Cruise ESC mass in kg
        cruise_prop_mass : float
            Cruise propeller mass in kg

        Returns
        -------
        float
            Total propulsion mass in kg
        """
        lift_system = n_lift_motors * (motor_mass + esc_mass + prop_mass)
        cruise_system = cruise_motor_mass + cruise_esc_mass + cruise_prop_mass

        return lift_system + cruise_system

    @staticmethod
    def battery_mass(
        energy_required_wh: float,
        specific_energy_wh_kg: float = 150.0,
        packaging_factor: float = 0.9,
    ) -> float:
        """
        Calculate battery mass from energy requirement.

        Parameters
        ----------
        energy_required_wh : float
            Required energy in Wh
        specific_energy_wh_kg : float
            Battery specific energy in Wh/kg (default: 150 for Li-ion)
        packaging_factor : float
            Cell-to-pack efficiency (default: 0.9)

        Returns
        -------
        float
            Battery mass in kg
        """
        return energy_required_wh / (specific_energy_wh_kg * packaging_factor)

    @staticmethod
    def solar_array_mass(
        array_area_m2: float,
        specific_mass_kg_m2: float = 0.5,
    ) -> float:
        """
        Calculate solar array mass.

        Parameters
        ----------
        array_area_m2 : float
            Solar array area in m²
        specific_mass_kg_m2 : float
            Specific mass in kg/m² (default: 0.5 for flexible thin-film)

        Returns
        -------
        float
            Solar array mass in kg
        """
        return array_area_m2 * specific_mass_kg_m2

    @staticmethod
    def avionics_mass(
        flight_computer: float = 0.05,
        imu: float = 0.02,
        gps: float = 0.02,
        radio: float = 0.05,
        wiring: float = 0.1,
    ) -> float:
        """
        Calculate avionics mass from component estimates.

        Parameters
        ----------
        flight_computer : float
            Flight computer mass in kg
        imu : float
            IMU mass in kg
        gps : float
            GPS receiver mass in kg
        radio : float
            Radio/telemetry mass in kg
        wiring : float
            Wiring harness mass in kg

        Returns
        -------
        float
            Total avionics mass in kg
        """
        return flight_computer + imu + gps + radio + wiring

    @classmethod
    def configuration_a_breakdown(cls, mtow_target: float = 7.5) -> MassBreakdown:
        """
        Generate mass breakdown for Configuration A (battery-only minimal).

        Based on feasibility_b_v3.md specifications.

        Parameters
        ----------
        mtow_target : float
            Target MTOW in kg

        Returns
        -------
        MassBreakdown
            Complete mass breakdown
        """
        breakdown = MassBreakdown()

        # Payload
        breakdown.add(ComponentMass(
            name="Optical gimbal (M2D Micro)",
            mass_kg=0.159,
            category="payload",
            part_number="M2D-MICRO",
            notes="Thermal/optical gimbal, <9W",
        ))
        breakdown.add(ComponentMass(
            name="UHF Transceiver",
            mass_kg=0.200,
            category="payload",
            part_number="EnduroSat UHF II",
            notes="400-438 MHz, 8W TX",
        ))
        breakdown.add(ComponentMass(
            name="Payload wiring/mounts",
            mass_kg=0.141,
            category="payload",
        ))

        # Propulsion - Lift (8x coaxial)
        for i in range(8):
            breakdown.add(ComponentMass(
                name=f"Lift motor #{i+1}",
                mass_kg=0.287,
                category="propulsion",
                part_number="T-Motor U8 II Pro 100KV",
            ))
        for i in range(8):
            breakdown.add(ComponentMass(
                name=f"Lift ESC #{i+1}",
                mass_kg=0.050,
                category="propulsion",
                part_number="T-Motor FLAME 60A",
            ))
        for i in range(8):
            breakdown.add(ComponentMass(
                name=f"Lift propeller #{i+1}",
                mass_kg=0.080,
                category="propulsion",
                notes="20-22 inch diameter",
            ))

        # Propulsion - Cruise
        breakdown.add(ComponentMass(
            name="Cruise motor",
            mass_kg=0.300,
            category="propulsion",
            part_number="Maxon EC-4pole 30 200W",
            notes="Space heritage, -100°C rated",
        ))
        breakdown.add(ComponentMass(
            name="Cruise ESC",
            mass_kg=0.030,
            category="propulsion",
        ))
        breakdown.add(ComponentMass(
            name="Cruise propeller",
            mass_kg=0.100,
            category="propulsion",
            notes="Multi-blade scimitar design",
        ))

        # Energy
        breakdown.add(ComponentMass(
            name="Battery pack",
            mass_kg=2.6,
            category="energy",
            part_number="Saft MP 176065 xtd",
            notes="Li-ion, 150 Wh/kg, 390 Wh total",
        ))

        # Avionics
        breakdown.add(ComponentMass(
            name="Flight controller",
            mass_kg=0.037,
            category="avionics",
            part_number="Pixhawk 4 Mini",
        ))
        breakdown.add(ComponentMass(
            name="IMU/sensors",
            mass_kg=0.020,
            category="avionics",
        ))
        breakdown.add(ComponentMass(
            name="Wiring harness",
            mass_kg=0.150,
            category="avionics",
        ))

        # Calculate remaining for structure
        current_total = breakdown.total_mass
        structure_mass = mtow_target - current_total

        breakdown.add(ComponentMass(
            name="Airframe structure",
            mass_kg=max(0.1, structure_mass - 0.3),
            category="structure",
            notes="CFRP construction, folding wing",
        ))
        breakdown.add(ComponentMass(
            name="Landing gear",
            mass_kg=0.15,
            category="structure",
        ))
        breakdown.add(ComponentMass(
            name="Margin",
            mass_kg=0.15,
            category="structure",
        ))

        return breakdown

    @classmethod
    def configuration_b_breakdown(cls, mtow_target: float = 24.0) -> MassBreakdown:
        """
        Generate mass breakdown for Configuration B (solar-augmented).

        Based on feasibility_a_v3.md specifications.

        Parameters
        ----------
        mtow_target : float
            Target MTOW in kg

        Returns
        -------
        MassBreakdown
            Complete mass breakdown
        """
        breakdown = MassBreakdown()

        # Payload (enhanced)
        breakdown.add(ComponentMass(
            name="High-res camera system",
            mass_kg=0.500,
            category="payload",
            notes="5MP sensor + gimbal",
        ))
        breakdown.add(ComponentMass(
            name="Communication system",
            mass_kg=0.300,
            category="payload",
            notes="UHF + high-speed downlink",
        ))
        breakdown.add(ComponentMass(
            name="Scientific instruments",
            mass_kg=1.0,
            category="payload",
            notes="Spectrometer, additional sensors",
        ))
        breakdown.add(ComponentMass(
            name="Payload structure/wiring",
            mass_kg=0.7,
            category="payload",
        ))

        # Propulsion - Lift (4x quad)
        for i in range(4):
            breakdown.add(ComponentMass(
                name=f"Lift motor #{i+1}",
                mass_kg=0.400,
                category="propulsion",
                part_number="T-Motor U15 series",
                notes="High torque for large props",
            ))
        for i in range(4):
            breakdown.add(ComponentMass(
                name=f"Lift ESC #{i+1}",
                mass_kg=0.080,
                category="propulsion",
            ))
        for i in range(4):
            breakdown.add(ComponentMass(
                name=f"Lift propeller #{i+1}",
                mass_kg=0.150,
                category="propulsion",
                notes="1.5m diameter props",
            ))

        # Propulsion - Cruise (dual for redundancy)
        for i in range(2):
            breakdown.add(ComponentMass(
                name=f"Cruise motor #{i+1}",
                mass_kg=0.350,
                category="propulsion",
            ))
            breakdown.add(ComponentMass(
                name=f"Cruise propeller #{i+1}",
                mass_kg=0.120,
                category="propulsion",
            ))

        # Energy
        breakdown.add(ComponentMass(
            name="Battery pack",
            mass_kg=2.0,
            category="energy",
            part_number="Saft Li-Ion",
            notes="300 Wh total",
        ))
        breakdown.add(ComponentMass(
            name="Solar array",
            mass_kg=3.0,
            category="energy",
            notes="~6 m² at 0.5 kg/m², 30% efficiency",
        ))
        breakdown.add(ComponentMass(
            name="MPPT controller",
            mass_kg=0.100,
            category="energy",
        ))

        # Avionics
        breakdown.add(ComponentMass(
            name="Flight computer",
            mass_kg=0.100,
            category="avionics",
            notes="Radiation-hardened",
        ))
        breakdown.add(ComponentMass(
            name="Sensors/IMU",
            mass_kg=0.050,
            category="avionics",
        ))
        breakdown.add(ComponentMass(
            name="Wiring harness",
            mass_kg=0.300,
            category="avionics",
        ))

        # Calculate structure
        current_total = breakdown.total_mass
        structure_mass = mtow_target - current_total

        breakdown.add(ComponentMass(
            name="Wing structure",
            mass_kg=structure_mass * 0.50,
            category="structure",
            notes="7 m² wing area, folding mechanism",
        ))
        breakdown.add(ComponentMass(
            name="Fuselage/boom structure",
            mass_kg=structure_mass * 0.30,
            category="structure",
        ))
        breakdown.add(ComponentMass(
            name="Tail surfaces",
            mass_kg=structure_mass * 0.10,
            category="structure",
        ))
        breakdown.add(ComponentMass(
            name="Landing gear",
            mass_kg=structure_mass * 0.05,
            category="structure",
        ))
        breakdown.add(ComponentMass(
            name="Margin",
            mass_kg=structure_mass * 0.05,
            category="structure",
        ))

        return breakdown


if __name__ == "__main__":
    print("Weight Estimation - Validation")
    print("=" * 60)

    # Configuration A
    print("\n--- Configuration A (7.5 kg battery-only) ---")
    breakdown_a = WeightEstimation.configuration_a_breakdown(7.5)
    print(breakdown_a.summary())

    # Configuration B
    print("\n--- Configuration B (24 kg solar-augmented) ---")
    breakdown_b = WeightEstimation.configuration_b_breakdown(24.0)
    print(breakdown_b.summary())

    # Wing mass estimate
    print("\n--- Wing Mass Estimation (Sadraey method) ---")
    wing_mass = WeightEstimation.wing_mass_sadraey(
        wing_area=4.04,
        chord_mac=0.58,
        thickness_ratio=0.12,
        aspect_ratio=12.0,
        n_ultimate=3.8,
        sweep_deg=0.0,
        taper_ratio=0.4,
        rho_material=1600.0,  # CFRP
        k_rho=0.0025,
    )
    print(f"  Wing area: 4.04 m²")
    print(f"  Aspect ratio: 12")
    print(f"  Estimated wing mass: {wing_mass:.2f} kg")
