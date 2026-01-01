#!/usr/bin/env python3
"""
Mars UAV Sizing (Coupled) - Main Entry Point
============================================

Runs Section 5 constraint analyses and the coupled matching chart solver.
All parameters are loaded from config/ YAML files.
"""

import sys
from datetime import datetime
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from mars_uav_sizing_coupled.config import get_param
from mars_uav_sizing_coupled.section5 import (
    rotorcraft,
    fixed_wing,
    hybrid_vtol,
    matching_chart,
    comparative,
)


def print_header() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print("=" * 80)
    print("MARS UAV FEASIBILITY STUDY (COUPLED)")
    print("Section 5: Constraint Analysis")
    print("=" * 80)
    print()
    print(f"  Analysis run: {timestamp}")
    print("  Configuration: All parameters from config/ YAML files")
    print(f"  Baseline MTOW: {get_param('mission.mass.mtow_kg')} kg")
    print()


def run_all_analyses(verbose: bool = True, use_coupled_solver: bool = True) -> dict:
    print_header()

    results = {}

    print("\n" + "-" * 80)
    print(" 1/5  ROTORCRAFT ANALYSIS (Section 5.1)")
    print("-" * 80 + "\n")
    results["rotorcraft"] = rotorcraft.rotorcraft_feasibility_analysis()
    if verbose:
        rotorcraft.print_analysis(results["rotorcraft"])
    else:
        status = "PASS" if results["rotorcraft"]["feasible"] else "FAIL"
        print(f"  Endurance: {results['rotorcraft']['endurance_min']:.0f} min - {status}")

    print("\n" + "-" * 80)
    print(" 2/5  FIXED-WING ANALYSIS (Section 5.2)")
    print("-" * 80 + "\n")
    results["fixed_wing"] = fixed_wing.fixed_wing_feasibility_analysis()
    if verbose:
        fixed_wing.print_analysis(results["fixed_wing"])
    else:
        status = "PASS" if results["fixed_wing"]["endurance_passes"] else "FAIL"
        print(f"  Endurance: {results['fixed_wing']['endurance_min']:.0f} min - {status}")

    print("\n" + "-" * 80)
    print(" 3/5  HYBRID VTOL ANALYSIS (Section 5.3)")
    print("-" * 80 + "\n")
    results["hybrid_vtol"] = hybrid_vtol.hybrid_vtol_feasibility_analysis()
    if verbose:
        hybrid_vtol.print_analysis(results["hybrid_vtol"])
    else:
        status = "PASS" if results["hybrid_vtol"]["feasible"] else "FAIL"
        print(f"  Endurance: {results['hybrid_vtol']['endurance_min']:.0f} min - {status}")

    print("\n" + "-" * 80)
    print(" 4/5  MATCHING CHART ANALYSIS (Section 5.4)")
    print("-" * 80 + "\n")
    results["matching_chart"] = matching_chart.matching_chart_analysis(
        use_coupled_solver=use_coupled_solver
    )
    if verbose:
        matching_chart.print_analysis(results["matching_chart"], use_coupled_solver)
    else:
        dp = results["matching_chart"]["design_point"]
        print(
            f"  Design point: W/S = {dp['wing_loading']:.1f} N/m^2, "
            f"P/W = {dp['power_loading']:.1f} W/N"
        )

    print("\n" + "-" * 80)
    print(" 5/5  COMPARATIVE ANALYSIS")
    print("-" * 80 + "\n")
    results["comparative"] = comparative.comparative_summary()
    if verbose:
        comparative.print_analysis(results["comparative"])
    else:
        print(f"  Selected: {results['comparative']['selected'].replace('_', ' ').upper()}")

    print("\n" + "-" * 80)
    print("ANALYSIS COMPLETE")
    print("-" * 80)
    print()

    for config in ["rotorcraft", "fixed_wing", "hybrid_vtol"]:
        if config in results and "feasible" in results[config]:
            status = "FEASIBLE" if results[config]["feasible"] else "NOT FEASIBLE"
            name = config.replace("_", " ").title()
            print(f"  {name:20} {status}")

    print()
    print(f"  Selected configuration: {results['comparative']['selected'].replace('_', ' ').upper()}")
    print()

    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Mars UAV Section 5 Constraint Analysis (Coupled)"
    )
    parser.add_argument(
        "--brief",
        "-b",
        action="store_true",
        help="Show brief output only",
    )
    parser.add_argument(
        "--analysis",
        "-a",
        choices=["rotorcraft", "fixed_wing", "hybrid_vtol", "matching_chart", "comparative", "all"],
        default="all",
        help="Run specific analysis only",
    )
    parser.add_argument(
        "--uncoupled",
        action="store_true",
        help="Run full uncoupled analysis from mars_uav_sizing (ignores --analysis)",
    )

    args = parser.parse_args()
    verbose = not args.brief
    use_coupled_solver = not args.uncoupled

    if args.uncoupled:
        from mars_uav_sizing.run_analysis import run_all_analyses as run_uncoupled

        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

        print_header()
        print("  Mode: UNCOUPLED (delegated to mars_uav_sizing.run_analysis)")
        print()
        run_uncoupled(verbose=verbose)
        return

    if args.analysis == "all":
        run_all_analyses(verbose=verbose, use_coupled_solver=use_coupled_solver)
    elif args.analysis == "rotorcraft":
        rotorcraft.print_analysis()
    elif args.analysis == "fixed_wing":
        fixed_wing.print_analysis()
    elif args.analysis == "hybrid_vtol":
        hybrid_vtol.print_analysis()
    elif args.analysis == "matching_chart":
        matching_chart.print_analysis(use_coupled_solver=use_coupled_solver)
    elif args.analysis == "comparative":
        comparative.print_analysis()


if __name__ == "__main__":
    main()
