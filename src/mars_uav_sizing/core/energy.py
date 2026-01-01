#!/usr/bin/env python3
"""
Shared Energy Accounting Module
================================

Provides unified energy budget calculations for all architecture analyses.
Computes available energy, mission energy, reserve energy, required energy,
and margins using configuration values.

This module centralizes energy calculations to ensure consistency between:
- Section 5.1 Rotorcraft analysis
- Section 5.2 Fixed-wing analysis
- Section 5.3 Hybrid VTOL analysis
- Section 7.4 Performance verification

All parameters are loaded from configuration - NO HARDCODED VALUES.

Last Updated: 2026-01-01
"""

from dataclasses import dataclass
from typing import Dict, Any
from ..config import (
    get_mtow,
    get_battery_params,
    get_mission_params,
    get_param,
)


@dataclass
class EnergyBudget:
    """Complete energy budget breakdown."""
    # Battery capacity
    battery_mass_kg: float
    total_energy_wh: float
    usable_energy_wh: float

    # Mission phases
    hover_energy_wh: float
    transition_energy_wh: float
    cruise_energy_wh: float

    # Totals
    mission_energy_wh: float
    reserve_energy_wh: float
    required_energy_wh: float

    # Margins
    margin_wh: float
    margin_percent: float
    feasible: bool

    # Configuration values (for traceability)
    dod: float
    eta_discharge: float
    reserve_fraction: float


def get_battery_energy() -> Dict[str, float]:
    """
    Calculate available battery energy from configuration.

    Implements @eq:energy-available:
        E_available = m_batt × e_spec × DoD × η_disch

    Returns
    -------
    dict
        Battery energy breakdown
    """
    mtow_kg = get_mtow()
    batt = get_battery_params()
    f_batt = get_mission_params()['f_batt']

    battery_mass_kg = f_batt * mtow_kg
    total_energy_wh = battery_mass_kg * batt['e_spec_Wh_kg']
    usable_energy_wh = total_energy_wh * batt['dod'] * batt['eta_discharge']

    return {
        'battery_mass_kg': battery_mass_kg,
        'total_energy_wh': total_energy_wh,
        'usable_energy_wh': usable_energy_wh,
        'e_spec_Wh_kg': batt['e_spec_Wh_kg'],
        'dod': batt['dod'],
        'eta_discharge': batt['eta_discharge'],
        'f_batt': f_batt,
    }


def compute_reserve_energy(mission_energy_wh: float) -> Dict[str, float]:
    """
    Compute energy reserve from mission energy.

    Implements @eq:energy-reserve:
        E_reserve = E_mission × reserve_fraction
        E_required = E_mission + E_reserve

    Parameters
    ----------
    mission_energy_wh : float
        Total mission energy (hover + transition + cruise)

    Returns
    -------
    dict
        Reserve and required energy
    """
    reserve_fraction = get_param('mission.energy.reserve_fraction')

    reserve_energy_wh = mission_energy_wh * reserve_fraction
    required_energy_wh = mission_energy_wh + reserve_energy_wh

    return {
        'mission_energy_wh': mission_energy_wh,
        'reserve_fraction': reserve_fraction,
        'reserve_energy_wh': reserve_energy_wh,
        'required_energy_wh': required_energy_wh,
    }


def compute_energy_margin(
    available_wh: float,
    required_wh: float,
) -> Dict[str, float]:
    """
    Compute energy margin and feasibility.

    Implements @eq:energy-feasibility:
        margin = E_available - E_required
        feasible = E_available >= E_required

    Parameters
    ----------
    available_wh : float
        Available usable energy from battery
    required_wh : float
        Required energy (mission + reserve)

    Returns
    -------
    dict
        Energy margin analysis
    """
    margin_wh = available_wh - required_wh
    margin_percent = (margin_wh / required_wh) * 100 if required_wh > 0 else 0.0
    feasible = available_wh >= required_wh

    return {
        'available_wh': available_wh,
        'required_wh': required_wh,
        'margin_wh': margin_wh,
        'margin_percent': margin_percent,
        'feasible': feasible,
    }


def compute_full_energy_budget(
    hover_energy_wh: float,
    transition_energy_wh: float,
    cruise_energy_wh: float,
) -> EnergyBudget:
    """
    Compute complete energy budget from phase energies.

    This is the main entry point for energy calculations.

    Parameters
    ----------
    hover_energy_wh : float
        Energy for hover phase(s)
    transition_energy_wh : float
        Energy for transition phase(s)
    cruise_energy_wh : float
        Energy for cruise phase

    Returns
    -------
    EnergyBudget
        Complete energy budget dataclass
    """
    # Battery capacity
    batt = get_battery_energy()

    # Mission energy
    mission_energy_wh = hover_energy_wh + transition_energy_wh + cruise_energy_wh

    # Reserve and required
    reserve = compute_reserve_energy(mission_energy_wh)

    # Margin
    margin = compute_energy_margin(
        batt['usable_energy_wh'],
        reserve['required_energy_wh'],
    )

    return EnergyBudget(
        # Battery
        battery_mass_kg=batt['battery_mass_kg'],
        total_energy_wh=batt['total_energy_wh'],
        usable_energy_wh=batt['usable_energy_wh'],
        # Mission phases
        hover_energy_wh=hover_energy_wh,
        transition_energy_wh=transition_energy_wh,
        cruise_energy_wh=cruise_energy_wh,
        # Totals
        mission_energy_wh=mission_energy_wh,
        reserve_energy_wh=reserve['reserve_energy_wh'],
        required_energy_wh=reserve['required_energy_wh'],
        # Margins
        margin_wh=margin['margin_wh'],
        margin_percent=margin['margin_percent'],
        feasible=margin['feasible'],
        # Config values
        dod=batt['dod'],
        eta_discharge=batt['eta_discharge'],
        reserve_fraction=reserve['reserve_fraction'],
    )


def format_energy_budget(budget: EnergyBudget, label: str = "ENERGY BUDGET") -> str:
    """
    Format energy budget for console output.

    Parameters
    ----------
    budget : EnergyBudget
        Energy budget to format
    label : str
        Section label

    Returns
    -------
    str
        Formatted output string
    """
    reserve_pct = int(budget.reserve_fraction * 100)

    lines = [
        f"{label}",
        "-" * 50,
        f"  Battery mass:       {budget.battery_mass_kg:.2f} kg",
        f"  Total capacity:     {budget.total_energy_wh:.0f} Wh",
        f"  Usable ({budget.dod*100:.0f}% DoD, {budget.eta_discharge*100:.0f}% η): {budget.usable_energy_wh:.0f} Wh",
        "",
        f"  Mission energy:     {budget.mission_energy_wh:.1f} Wh",
    ]

    # Breakdown percentages
    if budget.mission_energy_wh > 0:
        hover_pct = budget.hover_energy_wh / budget.mission_energy_wh * 100
        trans_pct = budget.transition_energy_wh / budget.mission_energy_wh * 100
        cruise_pct = budget.cruise_energy_wh / budget.mission_energy_wh * 100
        lines.extend([
            f"    - Hover:          {budget.hover_energy_wh:.1f} Wh ({hover_pct:.0f}%)",
            f"    - Transition:     {budget.transition_energy_wh:.1f} Wh ({trans_pct:.0f}%)",
            f"    - Cruise:         {budget.cruise_energy_wh:.1f} Wh ({cruise_pct:.0f}%)",
        ])

    lines.extend([
        f"  Reserve ({reserve_pct}%):      {budget.reserve_energy_wh:.1f} Wh",
        f"  Required total:     {budget.required_energy_wh:.1f} Wh",
        f"  Margin:             {budget.margin_wh:.1f} Wh ({budget.margin_percent:+.1f}%)",
    ])

    return "\n".join(lines)


def get_reserve_label() -> str:
    """
    Get reserve fraction label from configuration.

    Returns
    -------
    str
        Formatted label like "20%" or "Reserve (20%)"
    """
    reserve_fraction = get_param('mission.energy.reserve_fraction')
    return f"{int(reserve_fraction * 100)}%"


if __name__ == "__main__":
    # Test with example values
    from ..section5.hybrid_vtol import (
        quadplane_hover_energy,
        quadplane_cruise_energy,
        transition_energy_estimate,
    )

    e_hover = quadplane_hover_energy()
    e_cruise = quadplane_cruise_energy()
    trans = transition_energy_estimate()
    e_trans = trans['total_transition_wh']

    budget = compute_full_energy_budget(e_hover, e_trans, e_cruise)
    print(format_energy_budget(budget, "QUADPLANE ENERGY BUDGET"))
    print()
    print(f"Feasible: {'[PASS]' if budget.feasible else '[FAIL]'}")
