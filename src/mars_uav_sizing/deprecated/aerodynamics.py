"""
Aerodynamics Module
===================

Provides aerodynamic analysis functions for Mars UAV design including:
- Drag polar calculations
- Lift-to-drag ratio estimation
- Airfoil data handling and interpolation
- Low Reynolds number corrections

References:
- Sadraey, M.H. (2013). Aircraft Design: A Systems Engineering Approach.
- Roskam, J. (2005). Airplane Design Part I: Preliminary Sizing of Airplanes.
- Desert et al. (2017). Aerodynamic Design on a Martian Micro Air Vehicle.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import math
import numpy as np


@dataclass
class AirfoilData:
    """
    Container for airfoil polar data.

    Attributes
    ----------
    name : str
        Airfoil designation (e.g., "E387", "S1223")
    thickness_ratio : float
        Maximum thickness to chord ratio (t/c)
    alpha : np.ndarray
        Angle of attack array in degrees
    cl : np.ndarray
        Lift coefficient array
    cd : np.ndarray
        Drag coefficient array
    cm : np.ndarray
        Pitching moment coefficient array (about c/4)
    reynolds : float
        Reynolds number at which polar was generated
    """

    name: str
    thickness_ratio: float
    alpha: np.ndarray
    cl: np.ndarray
    cd: np.ndarray
    cm: np.ndarray
    reynolds: float

    @property
    def cl_max(self) -> float:
        """Maximum lift coefficient."""
        return float(np.max(self.cl))

    @property
    def alpha_stall(self) -> float:
        """Angle of attack at maximum lift (stall angle) in degrees."""
        idx = np.argmax(self.cl)
        return float(self.alpha[idx])

    @property
    def cl_alpha(self) -> float:
        """
        Lift curve slope in the linear region (per radian).

        Computed via linear regression in the range -4° to 8°.
        """
        mask = (self.alpha >= -4) & (self.alpha <= 8)
        if np.sum(mask) < 2:
            return 2 * math.pi  # Theoretical thin airfoil value

        alpha_rad = np.deg2rad(self.alpha[mask])
        cl_linear = self.cl[mask]

        # Linear regression: cl = cl_alpha * alpha + cl_0
        coeffs = np.polyfit(alpha_rad, cl_linear, 1)
        return float(coeffs[0])

    @property
    def alpha_zero_lift(self) -> float:
        """Zero-lift angle of attack in degrees."""
        mask = (self.alpha >= -4) & (self.alpha <= 8)
        if np.sum(mask) < 2:
            return 0.0

        # Find where cl crosses zero
        coeffs = np.polyfit(self.alpha[mask], self.cl[mask], 1)
        if abs(coeffs[0]) < 1e-10:
            return 0.0
        return float(-coeffs[1] / coeffs[0])

    @property
    def cd_min(self) -> float:
        """Minimum drag coefficient (zero-lift drag)."""
        return float(np.min(self.cd))

    @property
    def ld_max(self) -> Tuple[float, float]:
        """
        Maximum lift-to-drag ratio and corresponding CL.

        Returns
        -------
        tuple
            (L/D_max, CL_at_max_LD)
        """
        ld = self.cl / self.cd
        idx = np.argmax(ld)
        return float(ld[idx]), float(self.cl[idx])

    def get_cl(self, alpha_deg: float) -> float:
        """Interpolate CL at given angle of attack."""
        return float(np.interp(alpha_deg, self.alpha, self.cl))

    def get_cd(self, alpha_deg: float) -> float:
        """Interpolate CD at given angle of attack."""
        return float(np.interp(alpha_deg, self.alpha, self.cd))

    def get_cd_at_cl(self, cl_target: float) -> float:
        """Interpolate CD at given CL."""
        return float(np.interp(cl_target, self.cl, self.cd))


@dataclass
class DragPolar:
    """
    Aircraft drag polar model.

    The total drag coefficient is modeled as:
        CD = CD0 + CL² / (π * AR * e)

    where:
        CD0 = zero-lift drag coefficient (profile + parasite)
        AR  = aspect ratio
        e   = Oswald efficiency factor

    Parameters
    ----------
    cd0 : float
        Zero-lift drag coefficient
    aspect_ratio : float
        Wing aspect ratio (b²/S)
    oswald_efficiency : float
        Oswald efficiency factor (typically 0.7-0.9)
    """

    cd0: float
    aspect_ratio: float
    oswald_efficiency: float = 0.85

    @property
    def k(self) -> float:
        """Induced drag factor: k = 1 / (π * AR * e)"""
        return 1.0 / (math.pi * self.aspect_ratio * self.oswald_efficiency)

    def cd(self, cl: float) -> float:
        """
        Calculate total drag coefficient at given lift coefficient.

        CD = CD0 + k * CL²

        Parameters
        ----------
        cl : float
            Lift coefficient

        Returns
        -------
        float
            Total drag coefficient
        """
        return self.cd0 + self.k * cl**2

    def cl_for_max_ld(self) -> float:
        """
        Lift coefficient for maximum L/D.

        At (L/D)_max: CL = sqrt(CD0 * π * AR * e)
        """
        return math.sqrt(self.cd0 / self.k)

    def max_ld(self) -> float:
        """
        Maximum lift-to-drag ratio.

        (L/D)_max = 0.5 * sqrt(π * AR * e / CD0)
        """
        cl_opt = self.cl_for_max_ld()
        cd_opt = self.cd(cl_opt)
        return cl_opt / cd_opt

    def ld(self, cl: float) -> float:
        """
        Calculate lift-to-drag ratio at given CL.

        Parameters
        ----------
        cl : float
            Lift coefficient

        Returns
        -------
        float
            Lift-to-drag ratio
        """
        cd = self.cd(cl)
        if cd < 1e-10:
            return 0.0
        return cl / cd

    def cl_for_min_power(self) -> float:
        """
        Lift coefficient for minimum power (maximum endurance for props).

        At P_min: CL = sqrt(3 * CD0 * π * AR * e)
        """
        return math.sqrt(3.0 * self.cd0 / self.k)

    def cl_for_min_drag(self) -> float:
        """
        Lift coefficient for minimum drag (maximum range for jets).

        Same as cl_for_max_ld().
        """
        return self.cl_for_max_ld()


def estimate_cd0_uav(
    s_wing: float,
    s_wet_wing: Optional[float] = None,
    s_wet_fuse: float = 0.5,
    s_wet_tail: float = 0.2,
    s_wet_other: float = 0.1,
    cf_wing: float = 0.008,
    cf_body: float = 0.010,
    form_factor_wing: float = 1.2,
    form_factor_body: float = 1.3,
    interference_factor: float = 1.1,
) -> float:
    """
    Estimate zero-lift drag coefficient for a small UAV.

    Uses component buildup method with wetted area approximations.

    Parameters
    ----------
    s_wing : float
        Wing planform area in m²
    s_wet_wing : float, optional
        Wing wetted area in m² (default: 2 * s_wing)
    s_wet_fuse : float
        Fuselage wetted area as fraction of s_wing (default: 0.5)
    s_wet_tail : float
        Tail surfaces wetted area as fraction of s_wing (default: 0.2)
    s_wet_other : float
        Other wetted areas (booms, motors, etc.) as fraction of s_wing
    cf_wing : float
        Skin friction coefficient for wing
    cf_body : float
        Skin friction coefficient for fuselage/body
    form_factor_wing : float
        Form factor for wing (accounts for thickness)
    form_factor_body : float
        Form factor for fuselage
    interference_factor : float
        Interference drag factor

    Returns
    -------
    float
        Estimated CD0
    """
    if s_wet_wing is None:
        s_wet_wing = 2.0 * s_wing  # Both surfaces

    # Component drag contributions (referenced to wing area)
    cd0_wing = cf_wing * form_factor_wing * (s_wet_wing / s_wing)
    cd0_fuse = cf_body * form_factor_body * s_wet_fuse
    cd0_tail = cf_wing * form_factor_wing * s_wet_tail
    cd0_other = cf_body * s_wet_other

    # Total with interference
    cd0 = (cd0_wing + cd0_fuse + cd0_tail + cd0_other) * interference_factor

    return cd0


def skin_friction_coefficient(
    reynolds: float,
    mach: float = 0.0,
    laminar_fraction: float = 0.0,
) -> float:
    """
    Calculate skin friction coefficient using Schlichting-Prandtl formula.

    For turbulent flow: Cf = 0.455 / (log10(Re))^2.58 * (1 + 0.144*M²)^-0.65
    For laminar flow:   Cf = 1.328 / sqrt(Re)

    Parameters
    ----------
    reynolds : float
        Reynolds number
    mach : float, optional
        Mach number for compressibility correction (default: 0)
    laminar_fraction : float, optional
        Fraction of surface with laminar flow (0-1, default: 0)

    Returns
    -------
    float
        Skin friction coefficient
    """
    if reynolds < 1e3:
        return 0.02  # Very low Re fallback

    # Laminar component
    cf_lam = 1.328 / math.sqrt(reynolds)

    # Turbulent component with compressibility correction
    compressibility = (1.0 + 0.144 * mach**2) ** 0.65
    cf_turb = 0.455 / (math.log10(reynolds) ** 2.58 * compressibility)

    # Weighted average
    cf = laminar_fraction * cf_lam + (1.0 - laminar_fraction) * cf_turb

    return cf


def oswald_efficiency(
    aspect_ratio: float,
    sweep_deg: float = 0.0,
    taper_ratio: float = 0.4,
) -> float:
    """
    Estimate Oswald efficiency factor for a wing.

    Uses empirical correlation from Raymer.

    Parameters
    ----------
    aspect_ratio : float
        Wing aspect ratio
    sweep_deg : float, optional
        Wing sweep angle at quarter chord in degrees (default: 0)
    taper_ratio : float, optional
        Wing taper ratio (default: 0.4)

    Returns
    -------
    float
        Oswald efficiency factor (typically 0.7-0.9)
    """
    # Raymer's empirical correlation for straight wings
    sweep_rad = math.radians(sweep_deg)

    # Base efficiency
    e_base = 1.78 * (1.0 - 0.045 * aspect_ratio**0.68) - 0.64

    # Sweep correction
    e_sweep = e_base * math.cos(sweep_rad) ** 0.15

    # Ensure reasonable bounds
    e = max(0.5, min(0.95, e_sweep))

    return e


def low_reynolds_correction(
    reynolds: float,
    re_ref: float = 1e6,
    n_exponent: float = 0.2,
) -> float:
    """
    Calculate drag correction factor for low Reynolds number.

    At low Re, profile drag increases due to laminar separation bubbles.
    This correction factor multiplies the profile drag.

    Parameters
    ----------
    reynolds : float
        Operating Reynolds number
    re_ref : float, optional
        Reference Reynolds number (default: 1e6)
    n_exponent : float, optional
        Empirical exponent (default: 0.2)

    Returns
    -------
    float
        Drag multiplication factor (≥1)
    """
    if reynolds >= re_ref:
        return 1.0

    # Empirical correction: drag increases at low Re
    factor = (re_ref / reynolds) ** n_exponent

    return factor


def required_wing_area(
    weight_mars: float,
    rho: float,
    v_stall: float,
    cl_max: float,
) -> float:
    """
    Calculate required wing area from stall speed constraint.

    S = 2W / (ρ * V_stall² * CL_max)

    Parameters
    ----------
    weight_mars : float
        Weight on Mars in Newtons
    rho : float
        Air density in kg/m³
    v_stall : float
        Target stall speed in m/s
    cl_max : float
        Maximum lift coefficient

    Returns
    -------
    float
        Required wing area in m²
    """
    return 2.0 * weight_mars / (rho * v_stall**2 * cl_max)


def wing_geometry(
    wing_area: float,
    aspect_ratio: float,
    taper_ratio: float = 0.4,
) -> dict:
    """
    Calculate wing geometry parameters.

    Parameters
    ----------
    wing_area : float
        Wing planform area in m²
    aspect_ratio : float
        Aspect ratio (b²/S)
    taper_ratio : float, optional
        Taper ratio c_tip/c_root (default: 0.4)

    Returns
    -------
    dict
        Dictionary containing:
        - span: wingspan in m
        - chord_root: root chord in m
        - chord_tip: tip chord in m
        - chord_mac: mean aerodynamic chord in m
        - y_mac: spanwise location of MAC in m
    """
    # Wingspan
    span = math.sqrt(wing_area * aspect_ratio)

    # Root chord (from area of trapezoid)
    chord_root = 2.0 * wing_area / (span * (1.0 + taper_ratio))

    # Tip chord
    chord_tip = taper_ratio * chord_root

    # Mean aerodynamic chord
    chord_mac = (2.0 / 3.0) * chord_root * (1.0 + taper_ratio + taper_ratio**2) / (1.0 + taper_ratio)

    # Spanwise location of MAC (from root)
    y_mac = (span / 6.0) * (1.0 + 2.0 * taper_ratio) / (1.0 + taper_ratio)

    return {
        "span": span,
        "chord_root": chord_root,
        "chord_tip": chord_tip,
        "chord_mac": chord_mac,
        "y_mac": y_mac,
    }


def cruise_cl(
    weight_mars: float,
    rho: float,
    velocity: float,
    wing_area: float,
) -> float:
    """
    Calculate lift coefficient required for steady level flight.

    CL = 2W / (ρ * V² * S)

    Parameters
    ----------
    weight_mars : float
        Weight on Mars in Newtons
    rho : float
        Air density in kg/m³
    velocity : float
        Cruise velocity in m/s
    wing_area : float
        Wing area in m²

    Returns
    -------
    float
        Required lift coefficient
    """
    return 2.0 * weight_mars / (rho * velocity**2 * wing_area)


def cruise_drag(
    weight_mars: float,
    rho: float,
    velocity: float,
    wing_area: float,
    polar: DragPolar,
) -> float:
    """
    Calculate drag force in steady level cruise.

    Parameters
    ----------
    weight_mars : float
        Weight on Mars in Newtons
    rho : float
        Air density in kg/m³
    velocity : float
        Cruise velocity in m/s
    wing_area : float
        Wing area in m²
    polar : DragPolar
        Drag polar model

    Returns
    -------
    float
        Drag force in Newtons
    """
    cl = cruise_cl(weight_mars, rho, velocity, wing_area)
    cd = polar.cd(cl)
    q = 0.5 * rho * velocity**2
    return q * wing_area * cd


def cruise_power(
    weight_mars: float,
    rho: float,
    velocity: float,
    wing_area: float,
    polar: DragPolar,
    eta_prop: float = 0.65,
) -> float:
    """
    Calculate power required for steady level cruise.

    P = D * V / η_prop

    Parameters
    ----------
    weight_mars : float
        Weight on Mars in Newtons
    rho : float
        Air density in kg/m³
    velocity : float
        Cruise velocity in m/s
    wing_area : float
        Wing area in m²
    polar : DragPolar
        Drag polar model
    eta_prop : float, optional
        Propeller efficiency (default: 0.65)

    Returns
    -------
    float
        Power required in Watts
    """
    drag = cruise_drag(weight_mars, rho, velocity, wing_area, polar)
    return drag * velocity / eta_prop


if __name__ == "__main__":
    # Example usage and validation
    from .constants import G_MARS, RHO_ARCADIA

    print("Aerodynamics Module - Validation")
    print("=" * 60)

    # Configuration A: 7.5 kg battery-only
    mass_a = 7.5  # kg
    weight_a = mass_a * G_MARS  # 27.8 N
    rho = 0.017  # kg/m³ at Arcadia Planitia
    v_stall = 30.0  # m/s
    cl_max = 0.9

    # Calculate required wing area
    s_wing = required_wing_area(weight_a, rho, v_stall, cl_max)
    print(f"\nConfiguration A (7.5 kg):")
    print(f"  Weight on Mars: {weight_a:.1f} N")
    print(f"  Required wing area: {s_wing:.2f} m²")

    # Calculate wing geometry
    ar = 12.0
    geom = wing_geometry(s_wing, ar)
    print(f"  Wingspan: {geom['span']:.2f} m")
    print(f"  MAC: {geom['chord_mac']:.2f} m")

    # Create drag polar
    cd0 = 0.015  # Low-Re value
    polar = DragPolar(cd0=cd0, aspect_ratio=ar, oswald_efficiency=0.85)

    print(f"\nDrag Polar Analysis:")
    print(f"  CD0: {polar.cd0:.4f}")
    print(f"  AR: {polar.aspect_ratio:.1f}")
    print(f"  e: {polar.oswald_efficiency:.2f}")
    print(f"  k: {polar.k:.4f}")
    print(f"  (L/D)max: {polar.max_ld():.1f}")
    print(f"  CL for (L/D)max: {polar.cl_for_max_ld():.3f}")

    # Cruise analysis
    v_cruise = 40.0  # m/s
    cl_cruise = cruise_cl(weight_a, rho, v_cruise, s_wing)
    cd_cruise = polar.cd(cl_cruise)
    ld_cruise = polar.ld(cl_cruise)
    drag = cruise_drag(weight_a, rho, v_cruise, s_wing, polar)
    power = cruise_power(weight_a, rho, v_cruise, s_wing, polar, eta_prop=0.65)

    print(f"\nCruise Analysis at V={v_cruise} m/s:")
    print(f"  CL: {cl_cruise:.3f}")
    print(f"  CD: {cd_cruise:.5f}")
    print(f"  L/D: {ld_cruise:.1f}")
    print(f"  Drag: {drag:.2f} N")
    print(f"  Power required: {power:.1f} W")
