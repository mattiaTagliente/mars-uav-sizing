#!/usr/bin/env python3
"""
Mars UAV Sizing - Main Entry Point
====================================

Runs complete constraint analyses and design sizing.
Generates comprehensive outputs for manuscript tables and verification.
All parameters are loaded from config/ YAML files.

Usage:
    python -m mars_uav_sizing.run_analysis
    python -m mars_uav_sizing.run_analysis --section 5
    python -m mars_uav_sizing.run_analysis --section 6
    python -m mars_uav_sizing.run_analysis --section 7
    python -m mars_uav_sizing.run_analysis --all

Sections:
    5 - Constraint Analysis (rotorcraft, fixed-wing, hybrid VTOL, matching chart)
    6 - Design Decisions (airfoil, propeller, tail sizing)
    7 - Component Selection and Mass Breakdown

Last Updated: 2026-01-01
"""

import sys
from datetime import datetime
from pathlib import Path

# Add package to path if running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from mars_uav_sizing.config import load_config, get_param
from mars_uav_sizing.section5 import (
    rotorcraft,
    fixed_wing,
    hybrid_vtol,
    matching_chart,
    comparative,
)
from mars_uav_sizing.section6 import (
    propeller_sizing,
    tail_sizing,
)
from mars_uav_sizing.section7 import (
    component_selection,
    mass_breakdown,
)


def print_header():
    """Print analysis header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print()
    print("+" + "=" * 78 + "+")
    print("|" + " MARS UAV FEASIBILITY STUDY (BASELINE CASE) ".center(78) + "|")
    print("|" + " Section 5: Constraint Analysis ".center(78) + "|")
    print("|" + " Mode: UNCOUPLED - Fixed MTOW baseline ".center(78) + "|")
    print("+" + "=" * 78 + "+")
    print()
    print(f"  Analysis run: {timestamp}")
    print(f"  Configuration: All parameters from config/ YAML files")
    print(f"  Baseline MTOW: {get_param('mission.mass.mtow_kg')} kg")
    print()


def run_section5_analyses(verbose: bool = True) -> dict:
    """
    Run Section 5 constraint analyses.

    Parameters
    ----------
    verbose : bool
        If True, print detailed output for each analysis

    Returns
    -------
    dict
        Section 5 analysis results
    """
    results = {}

    # 1. Rotorcraft Analysis
    print("\n" + "-" * 80)
    print(" 5.1  ROTORCRAFT ANALYSIS")
    print("-" * 80 + "\n")
    results['rotorcraft'] = rotorcraft.rotorcraft_feasibility_analysis()
    if verbose:
        rotorcraft.print_analysis(results['rotorcraft'])
    else:
        status = "[PASS]" if results['rotorcraft']['feasible'] else "[FAIL]"
        print(f"  Endurance: {results['rotorcraft']['endurance_min']:.0f} min -> {status}")

    # 2. Fixed-Wing Analysis
    print("\n" + "-" * 80)
    print(" 5.2  FIXED-WING ANALYSIS")
    print("-" * 80 + "\n")
    results['fixed_wing'] = fixed_wing.fixed_wing_feasibility_analysis()
    if verbose:
        fixed_wing.print_analysis(results['fixed_wing'])
    else:
        status = "[PASS]" if results['fixed_wing']['feasible'] else "[FAIL]"
        print(f"  Endurance: {results['fixed_wing']['endurance_min']:.0f} min (no VTOL) -> {status}")

    # 3. Hybrid VTOL Analysis
    print("\n" + "-" * 80)
    print(" 5.3  HYBRID VTOL ANALYSIS")
    print("-" * 80 + "\n")
    results['hybrid_vtol'] = hybrid_vtol.hybrid_vtol_feasibility_analysis()
    if verbose:
        hybrid_vtol.print_analysis(results['hybrid_vtol'])
    else:
        status = "[PASS]" if results['hybrid_vtol']['feasible'] else "[FAIL]"
        print(f"  Endurance: {results['hybrid_vtol']['endurance_min']:.0f} min -> {status}")

    # 4. Matching Chart Analysis
    print("\n" + "-" * 80)
    print(" 5.4  MATCHING CHART ANALYSIS")
    print("-" * 80 + "\n")
    results['matching_chart'] = matching_chart.matching_chart_analysis()
    if verbose:
        matching_chart.print_analysis(results['matching_chart'])
    else:
        dp = results['matching_chart']['design_point']
        print(f"  Design point: W/S = {dp['wing_loading']:.1f} N/m2, P/W = {dp['power_loading']:.1f} W/N")

    # 5. Comparative Analysis
    print("\n" + "-" * 80)
    print(" 5.5  COMPARATIVE ANALYSIS")
    print("-" * 80 + "\n")
    results['comparative'] = comparative.comparative_summary()
    if verbose:
        comparative.print_analysis(results['comparative'])
    else:
        print(f"  Selected: {results['comparative']['selected'].replace('_', ' ').upper()}")

    return results


def run_section6_analyses(verbose: bool = True) -> dict:
    """
    Run Section 6 design decision analyses.

    Parameters
    ----------
    verbose : bool
        If True, print detailed output for each analysis

    Returns
    -------
    dict
        Section 6 analysis results
    """
    results = {}

    # 1. Propeller Sizing
    print("\n" + "-" * 80)
    print(" 6.3a  PROPELLER SIZING")
    print("-" * 80 + "\n")
    results['propeller'] = propeller_sizing.propeller_sizing_analysis()
    if verbose:
        propeller_sizing.print_analysis(results['propeller'])
    else:
        lift = results['propeller']['lift']
        cruise = results['propeller']['cruise']
        print(f"  Lift props:  {lift['n_motors']}x {lift['selected_diameter_in']}\" ({lift['selected_model']})")
        print(f"  Cruise prop: {cruise['n_motors']}x {cruise['selected_diameter_in']}\" ({cruise['selected_model']})")

    # 2. Tail Sizing
    print("\n" + "-" * 80)
    print(" 6.3b  TAIL SIZING")
    print("-" * 80 + "\n")
    results['tail'] = tail_sizing.vtail_sizing()
    if verbose:
        tail_sizing.print_analysis(results['tail'])
    else:
        print(f"  V-tail area:    {results['tail']['S_vtail_total_m2']:.3f} m2")
        print(f"  V-tail span:    {results['tail']['b_vtail_m']:.2f} m")
        print(f"  Dihedral:       {results['tail']['dihedral_deg']:.0f} deg")

    return results


def run_section7_analyses(verbose: bool = True) -> dict:
    """
    Run Section 7 component selection and mass breakdown analyses.

    Parameters
    ----------
    verbose : bool
        If True, print detailed output for each analysis

    Returns
    -------
    dict
        Section 7 analysis results
    """
    results = {}

    # 1. Component Selection
    print("\n" + "-" * 80)
    print(" 7.1  COMPONENT SELECTION")
    print("-" * 80 + "\n")
    if verbose:
        component_selection.print_component_selection()
    else:
        selected = component_selection.get_selected_components()
        print(f"  Lift motor:   {selected['lift_motor']['model']}")
        print(f"  Cruise motor: {selected['cruise_motor']['model']}")
    results['components'] = component_selection.get_selected_components()

    # 2. Mass Breakdown
    print("\n" + "-" * 80)
    print(" 7.2  MASS BREAKDOWN")
    print("-" * 80 + "\n")
    results['mass'] = mass_breakdown.get_propulsion_mass_breakdown()
    if verbose:
        mass_breakdown.print_mass_breakdown()
    else:
        total = results['mass']['total_kg']
        print(f"  Total propulsion mass: {total:.3f} kg")

    return results


def run_all_analyses(verbose: bool = True):
    """
    Run complete analysis across all sections.

    Parameters
    ----------
    verbose : bool
        If True, print detailed output for each analysis

    Returns
    -------
    dict
        Complete analysis results
    """
    print_header()

    results = {}

    # Section 5: Constraint Analysis
    print("\n" + "=" * 80)
    print(" SECTION 5: CONSTRAINT ANALYSIS")
    print("=" * 80)
    results['section5'] = run_section5_analyses(verbose)

    # Section 6: Design Decisions
    print("\n" + "=" * 80)
    print(" SECTION 6: DESIGN DECISIONS")
    print("=" * 80)
    results['section6'] = run_section6_analyses(verbose)

    # Section 7: Component Selection
    print("\n" + "=" * 80)
    print(" SECTION 7: COMPONENT SELECTION AND VERIFICATION")
    print("=" * 80)
    results['section7'] = run_section7_analyses(verbose)

    # Summary
    print("\n" + "=" * 80)
    print(" ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    # Section 5 summary
    print("  Section 5 - Configuration Results:")
    sec5 = results['section5']
    for config in ['rotorcraft', 'fixed_wing', 'hybrid_vtol']:
        if config in sec5 and 'feasible' in sec5[config]:
            status = "[FEASIBLE]" if sec5[config]['feasible'] else "[NOT FEASIBLE]"
            name = config.replace('_', ' ').title()
            print(f"    {name:20} {status}")
    print(f"    -> Selected: {sec5['comparative']['selected'].replace('_', ' ').upper()}")
    print()

    # Section 6 summary
    print("  Section 6 - Geometry:")
    sec6 = results['section6']
    dp = sec5['matching_chart']['design_point']
    geom = sec5['matching_chart']['geometry']
    print(f"    Wing area:     {geom['wing_area_m2']:.3f} m2")
    print(f"    Wingspan:      {geom['wingspan_m']:.2f} m")
    print(f"    V-tail area:   {sec6['tail']['S_vtail_total_m2']:.3f} m2")
    print()

    # Section 7 summary
    print("  Section 7 - Mass Budget:")
    sec7 = results['section7']
    mtow = get_param('mission.mass.mtow_kg')
    prop_mass = sec7['mass']['total_kg']
    f_prop = get_param('mission.mass_fractions.f_propulsion')
    prop_budget = f_prop * mtow
    margin = prop_budget - prop_mass
    print(f"    MTOW:             {mtow:.2f} kg")
    print(f"    Propulsion mass:  {prop_mass:.3f} kg (budget: {prop_budget:.2f} kg)")
    print(f"    Margin:           {margin:+.3f} kg")
    print()

    return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Mars UAV Sizing Analysis"
    )
    parser.add_argument(
        '--brief', '-b',
        action='store_true',
        help='Show brief output only'
    )
    parser.add_argument(
        '--section', '-s',
        choices=['5', '6', '7', 'all'],
        default='all',
        help='Run specific section only (5=constraint, 6=design, 7=component)'
    )
    parser.add_argument(
        '--analysis', '-a',
        choices=['rotorcraft', 'fixed_wing', 'hybrid_vtol', 'matching_chart',
                 'comparative', 'propeller', 'tail', 'mass'],
        default=None,
        help='Run specific analysis only'
    )

    args = parser.parse_args()

    verbose = not args.brief

    # Run specific analysis if requested
    if args.analysis:
        if args.analysis == 'rotorcraft':
            rotorcraft.print_analysis()
        elif args.analysis == 'fixed_wing':
            fixed_wing.print_analysis()
        elif args.analysis == 'hybrid_vtol':
            hybrid_vtol.print_analysis()
        elif args.analysis == 'matching_chart':
            matching_chart.print_analysis()
        elif args.analysis == 'comparative':
            comparative.print_analysis()
        elif args.analysis == 'propeller':
            propeller_sizing.print_analysis()
        elif args.analysis == 'tail':
            tail_sizing.print_analysis()
        elif args.analysis == 'mass':
            mass_breakdown.print_mass_breakdown()
        return

    # Run section or all
    if args.section == 'all':
        run_all_analyses(verbose=verbose)
    elif args.section == '5':
        print_header()
        run_section5_analyses(verbose=verbose)
    elif args.section == '6':
        print_header()
        run_section6_analyses(verbose=verbose)
    elif args.section == '7':
        print_header()
        run_section7_analyses(verbose=verbose)


if __name__ == "__main__":
    main()
