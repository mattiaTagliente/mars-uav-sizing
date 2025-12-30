"""
Airfoil Analysis for Mars UAV
=============================

Generates polar data and comparison plots for low Reynolds number airfoils.
Uses both XFOIL calculations (where convergent) and Selig experimental data.

References:
- Selig et al. (1995). Summary of Low-Speed Airfoil Data, Vol. 1
- Drela, M. (1989). XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import json

import matplotlib.pyplot as plt
import numpy as np

from xfoil_wrapper import (
    XfoilRunner,
    XfoilPolar,
    get_airfoil_coord_file,
    get_selig_polar,
    SELIG_DATA,
)


def run_xfoil_analysis(
    airfoils: List[str],
    reynolds_numbers: List[float],
    output_dir: Path,
    timeout_per_run: int = 60,
) -> Dict[str, Dict[float, XfoilPolar]]:
    """
    Run XFOIL analysis for multiple airfoils and Reynolds numbers.

    Parameters
    ----------
    airfoils : list
        List of airfoil names
    reynolds_numbers : list
        List of Reynolds numbers
    output_dir : Path
        Output directory for results
    timeout_per_run : int
        Timeout per XFOIL run in seconds

    Returns
    -------
    dict
        Nested dict: results[airfoil][reynolds] = XfoilPolar
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    runner = XfoilRunner(n_crit=5.0, max_iter=300)
    results = {}

    for airfoil in airfoils:
        results[airfoil] = {}

        # Get coordinate file
        coord_file = None
        if not airfoil.upper().startswith("NACA"):
            coord_file = get_airfoil_coord_file(airfoil, str(output_dir))

        for re_num in reynolds_numbers:
            print(f"  XFOIL: {airfoil} at Re = {re_num:,.0f}...")

            try:
                polar = runner.run_polar(
                    airfoil=airfoil,
                    reynolds=re_num,
                    mach=0.0,
                    alpha_range=(-4.0, 16.0, 0.5),
                    coord_file=coord_file,
                    output_dir=str(output_dir),
                    use_cache=True,
                )

                if polar.cl and len(polar.cl) > 5:
                    results[airfoil][re_num] = polar
                    print(f"    Success: {len(polar.alpha)} points")
                else:
                    print(f"    Failed: insufficient data")

            except Exception as e:
                print(f"    Error: {e}")

    return results


def get_selig_data(
    airfoils: List[str],
    reynolds_numbers: List[float],
) -> Dict[str, Dict[float, XfoilPolar]]:
    """
    Get Selig experimental data for airfoils.

    Parameters
    ----------
    airfoils : list
        List of airfoil names
    reynolds_numbers : list
        List of Reynolds numbers (will find closest available)

    Returns
    -------
    dict
        Nested dict: results[airfoil][reynolds] = XfoilPolar
    """
    results = {}

    for airfoil in airfoils:
        results[airfoil] = {}

        for re_num in reynolds_numbers:
            polar = get_selig_polar(airfoil, re_num)

            if polar:
                results[airfoil][polar.reynolds] = polar
                print(f"  Selig: {airfoil} at Re = {polar.reynolds:,.0f}")

    return results


def plot_polar_comparison(
    xfoil_results: Dict[str, Dict[float, XfoilPolar]],
    selig_results: Dict[str, Dict[float, XfoilPolar]],
    target_re: float,
    output_path: Path,
):
    """
    Create comparison plot of airfoil polars.

    Parameters
    ----------
    xfoil_results : dict
        XFOIL results
    selig_results : dict
        Selig experimental results
    target_re : float
        Target Reynolds number for comparison
    output_path : Path
        Output file path for plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    colors = {'e387': 'blue', 's1223': 'red', 's7055': 'green'}

    # Find closest Re for each dataset
    for airfoil in ['e387', 's1223', 's7055']:
        color = colors.get(airfoil, 'black')

        # Selig data (solid lines, filled markers)
        if airfoil in selig_results:
            re_keys = list(selig_results[airfoil].keys())
            if re_keys:
                closest_re = min(re_keys, key=lambda x: abs(x - target_re))
                polar = selig_results[airfoil][closest_re]

                # CL vs alpha
                axes[0, 0].plot(polar.alpha, polar.cl, 'o-', color=color,
                               label=f'{airfoil.upper()} (Selig, Re={closest_re/1000:.0f}k)',
                               markersize=4)

                # CD vs alpha
                axes[0, 1].plot(polar.alpha, polar.cd, 'o-', color=color,
                               markersize=4)

                # CL vs CD (drag polar)
                axes[1, 0].plot(polar.cd, polar.cl, 'o-', color=color,
                               markersize=4)

                # L/D vs alpha
                ld = [cl/cd if cd > 0 else 0 for cl, cd in zip(polar.cl, polar.cd)]
                axes[1, 1].plot(polar.alpha, ld, 'o-', color=color,
                               markersize=4)

        # XFOIL data (dashed lines, open markers)
        if airfoil in xfoil_results:
            re_keys = list(xfoil_results[airfoil].keys())
            if re_keys:
                closest_re = min(re_keys, key=lambda x: abs(x - target_re))
                polar = xfoil_results[airfoil][closest_re]

                if polar.cl:
                    # CL vs alpha
                    axes[0, 0].plot(polar.alpha, polar.cl, 's--', color=color,
                                   label=f'{airfoil.upper()} (XFOIL, Re={closest_re/1000:.0f}k)',
                                   markersize=3, alpha=0.7)

                    # CD vs alpha
                    axes[0, 1].plot(polar.alpha, polar.cd, 's--', color=color,
                                   markersize=3, alpha=0.7)

                    # CL vs CD
                    axes[1, 0].plot(polar.cd, polar.cl, 's--', color=color,
                                   markersize=3, alpha=0.7)

                    # L/D vs alpha
                    ld = [cl/cd if cd > 0 else 0 for cl, cd in zip(polar.cl, polar.cd)]
                    axes[1, 1].plot(polar.alpha, ld, 's--', color=color,
                                   markersize=3, alpha=0.7)

    # Labels and formatting
    axes[0, 0].set_xlabel('Angle of Attack (deg)')
    axes[0, 0].set_ylabel('Lift Coefficient CL')
    axes[0, 0].set_title(f'Lift Curve (Re ~ {target_re/1000:.0f}k)')
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_xlim(-6, 18)

    axes[0, 1].set_xlabel('Angle of Attack (deg)')
    axes[0, 1].set_ylabel('Drag Coefficient CD')
    axes[0, 1].set_title('Drag Curve')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_xlim(-6, 18)

    axes[1, 0].set_xlabel('Drag Coefficient CD')
    axes[1, 0].set_ylabel('Lift Coefficient CL')
    axes[1, 0].set_title('Drag Polar')
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].set_xlabel('Angle of Attack (deg)')
    axes[1, 1].set_ylabel('Lift-to-Drag Ratio L/D')
    axes[1, 1].set_title('Aerodynamic Efficiency')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_xlim(-6, 18)
    axes[1, 1].set_ylim(0, 60)

    plt.suptitle(f'Airfoil Comparison at Re ~ {target_re/1000:.0f},000', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved: {output_path}")


def generate_summary_table(
    selig_results: Dict[str, Dict[float, XfoilPolar]],
    target_re: float,
) -> str:
    """
    Generate markdown table summarizing airfoil performance.

    Parameters
    ----------
    selig_results : dict
        Selig experimental results
    target_re : float
        Target Reynolds number

    Returns
    -------
    str
        Markdown formatted table
    """
    lines = [
        f"| Airfoil | C_L,max | alpha_stall | (L/D)_max | C_L at (L/D)_max |",
        "|:--------|--------:|------------:|----------:|-----------------:|",
    ]

    for airfoil in ['e387', 's1223', 's7055']:
        if airfoil in selig_results:
            re_keys = list(selig_results[airfoil].keys())
            if re_keys:
                closest_re = min(re_keys, key=lambda x: abs(x - target_re))
                polar = selig_results[airfoil][closest_re]

                cl_max = polar.cl_max
                alpha_stall = polar.alpha_stall
                ld_max, cl_at_ld_max = polar.ld_max

                lines.append(
                    f"| {airfoil.upper()}    | {cl_max:.2f}    | {alpha_stall:.0f}°     | {ld_max:.1f}      | {cl_at_ld_max:.2f}             |"
                )

    return "\n".join(lines)


def save_polar_data(
    results: Dict[str, Dict[float, XfoilPolar]],
    output_path: Path,
):
    """Save polar data to JSON for later use."""
    data = {}

    for airfoil, re_dict in results.items():
        data[airfoil] = {}
        for re_num, polar in re_dict.items():
            data[airfoil][str(int(re_num))] = {
                "alpha": polar.alpha,
                "cl": polar.cl,
                "cd": polar.cd,
                "cm": polar.cm,
            }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"  Saved: {output_path}")


def main():
    """Main analysis routine."""
    print("=" * 60)
    print("Mars UAV Airfoil Analysis")
    print("=" * 60)

    # Configuration
    airfoils = ["e387", "s1223", "s7055"]

    # Reynolds numbers for Mars flight
    # Config A: Re ~ 40,000 (small chord, high speed)
    # Config B: Re ~ 80,000 (large chord)
    xfoil_reynolds = [100000, 200000]  # XFOIL works better at higher Re
    selig_reynolds = [60000, 100000]   # Available in Selig database

    # Output directory
    output_dir = Path(__file__).parent.parent.parent / "figures" / "airfoil_polars"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get Selig experimental data (always available)
    print("\n1. Loading Selig experimental data...")
    selig_results = get_selig_data(airfoils, selig_reynolds)

    # Try XFOIL (may not converge at low Re)
    print("\n2. Running XFOIL analysis (higher Re)...")
    xfoil_results = {}
    try:
        xfoil_results = run_xfoil_analysis(
            airfoils, xfoil_reynolds, output_dir, timeout_per_run=60
        )
    except Exception as e:
        print(f"  XFOIL analysis failed: {e}")
        print("  Continuing with Selig data only...")

    # Generate plots
    print("\n3. Generating comparison plots...")

    # Plot at Re ~ 60,000 (Mars Config A conditions)
    plot_polar_comparison(
        xfoil_results, selig_results,
        target_re=60000,
        output_path=output_dir / "airfoil_comparison_Re60k.png"
    )

    # Plot at Re ~ 100,000 (Mars Config B conditions)
    plot_polar_comparison(
        xfoil_results, selig_results,
        target_re=100000,
        output_path=output_dir / "airfoil_comparison_Re100k.png"
    )

    # Save data
    print("\n4. Saving polar data...")
    save_polar_data(selig_results, output_dir / "selig_polars.json")
    if xfoil_results:
        save_polar_data(xfoil_results, output_dir / "xfoil_polars.json")

    # Generate summary table
    print("\n5. Performance summary (Re = 60,000):")
    print("-" * 60)
    table = generate_summary_table(selig_results, 60000)
    print(table)

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
