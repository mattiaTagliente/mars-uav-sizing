#!/usr/bin/env python3
"""
Mars UAV Sizing - Main Entry Point
====================================

Runs all Section 5 constraint analyses and generates a comprehensive report.
All parameters are loaded from config/ YAML files.

Usage:
    python -m mars_uav_sizing.run_analysis
    
    # Or run individual analyses:
    python -m mars_uav_sizing.section5.rotorcraft
    python -m mars_uav_sizing.section5.fixed_wing
    python -m mars_uav_sizing.section5.hybrid_vtol
    python -m mars_uav_sizing.section5.matching_chart
    python -m mars_uav_sizing.section5.comparative

Last Updated: 2025-12-29
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


def print_header():
    """Print analysis header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " MARS UAV FEASIBILITY STUDY ".center(78) + "║")
    print("║" + " Section 5: Constraint Analysis ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"  Analysis run: {timestamp}")
    print(f"  Configuration: All parameters from config/ YAML files")
    print(f"  Baseline MTOW: {get_param('mission.mass.mtow_kg')} kg")
    print()


def run_all_analyses(verbose: bool = True):
    """
    Run complete Section 5 analysis.
    
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
    
    # 1. Rotorcraft Analysis
    print("\n" + "━" * 80)
    print(" 1/5  ROTORCRAFT ANALYSIS (§5.1)")
    print("━" * 80 + "\n")
    results['rotorcraft'] = rotorcraft.rotorcraft_feasibility_analysis()
    if verbose:
        rotorcraft.print_analysis(results['rotorcraft'])
    else:
        status = "✓ PASS" if results['rotorcraft']['feasible'] else "✗ FAIL"
        print(f"  Endurance: {results['rotorcraft']['endurance_min']:.0f} min → {status}")
    
    # 2. Fixed-Wing Analysis
    print("\n" + "━" * 80)
    print(" 2/5  FIXED-WING ANALYSIS (§5.2)")
    print("━" * 80 + "\n")
    results['fixed_wing'] = fixed_wing.fixed_wing_feasibility_analysis()
    if verbose:
        fixed_wing.print_analysis(results['fixed_wing'])
    else:
        status = "✓ PASS" if results['fixed_wing']['feasible'] else "✗ FAIL"
        print(f"  Endurance: {results['fixed_wing']['endurance_min']:.0f} min (no VTOL) → {status}")
    
    # 3. Hybrid VTOL Analysis
    print("\n" + "━" * 80)
    print(" 3/5  HYBRID VTOL ANALYSIS (§5.3)")
    print("━" * 80 + "\n")
    results['hybrid_vtol'] = hybrid_vtol.hybrid_vtol_feasibility_analysis()
    if verbose:
        hybrid_vtol.print_analysis(results['hybrid_vtol'])
    else:
        status = "✓ PASS" if results['hybrid_vtol']['feasible'] else "✗ FAIL"
        print(f"  Endurance: {results['hybrid_vtol']['endurance_min']:.0f} min → {status}")
    
    # 4. Matching Chart Analysis
    print("\n" + "━" * 80)
    print(" 4/5  MATCHING CHART ANALYSIS (§5.4)")
    print("━" * 80 + "\n")
    results['matching_chart'] = matching_chart.matching_chart_analysis()
    if verbose:
        matching_chart.print_analysis(results['matching_chart'])
    else:
        dp = results['matching_chart']['design_point']
        print(f"  Design point: W/S = {dp['wing_loading']:.1f} N/m², P/W = {dp['power_loading']:.1f} W/N")
    
    # 5. Comparative Analysis
    print("\n" + "━" * 80)
    print(" 5/5  COMPARATIVE ANALYSIS")
    print("━" * 80 + "\n")
    results['comparative'] = comparative.comparative_summary()
    if verbose:
        comparative.print_analysis(results['comparative'])
    else:
        print(f"  Selected: {results['comparative']['selected'].replace('_', ' ').upper()}")
    
    # Summary
    print("\n" + "━" * 80)
    print(" ANALYSIS COMPLETE")
    print("━" * 80)
    print()
    print("  Configuration Results:")
    for config in ['rotorcraft', 'fixed_wing', 'hybrid_vtol']:
        if config in results and 'feasible' in results[config]:
            status = "✓ FEASIBLE" if results[config]['feasible'] else "✗ NOT FEASIBLE"
            name = config.replace('_', ' ').title()
            print(f"    {name:20} {status}")
    
    print()
    print(f"  → Selected configuration: {results['comparative']['selected'].replace('_', ' ').upper()}")
    print()
    
    return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Mars UAV Section 5 Constraint Analysis"
    )
    parser.add_argument(
        '--brief', '-b',
        action='store_true',
        help='Show brief output only'
    )
    parser.add_argument(
        '--analysis', '-a',
        choices=['rotorcraft', 'fixed_wing', 'hybrid_vtol', 'matching_chart', 'comparative', 'all'],
        default='all',
        help='Run specific analysis only'
    )
    
    args = parser.parse_args()
    
    verbose = not args.brief
    
    if args.analysis == 'all':
        run_all_analyses(verbose=verbose)
    elif args.analysis == 'rotorcraft':
        rotorcraft.print_analysis()
    elif args.analysis == 'fixed_wing':
        fixed_wing.print_analysis()
    elif args.analysis == 'hybrid_vtol':
        hybrid_vtol.print_analysis()
    elif args.analysis == 'matching_chart':
        matching_chart.print_analysis()
    elif args.analysis == 'comparative':
        comparative.print_analysis()


if __name__ == "__main__":
    main()
