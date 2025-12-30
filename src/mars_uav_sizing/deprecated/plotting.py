"""
Plotting Module
===============

Visualization functions for Mars UAV sizing analysis,
including constraint diagrams, weight breakdowns, and performance charts.
"""

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from .constraints import SizingConstraints
from .weights import MassBreakdown
from .xfoil_wrapper import XfoilPolar


def check_matplotlib():
    """Check if matplotlib is available."""
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for plotting. Install with: pip install matplotlib")


def plot_constraint_diagram(
    constraints: SizingConstraints,
    wing_loading_range: Tuple[float, float] = (5.0, 50.0),
    n_points: int = 100,
    design_point: Optional[Tuple[float, float]] = None,
    title: str = "Matching Chart - Mars UAV",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot constraint diagram (matching chart).

    Parameters
    ----------
    constraints : SizingConstraints
        Sizing constraints object
    wing_loading_range : tuple
        (min, max) wing loading in N/m²
    n_points : int
        Number of points for curves
    design_point : tuple, optional
        (W/S, P/W) design point to highlight
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    ws_min, ws_max = wing_loading_range
    ws_values = [ws_min + (ws_max - ws_min) * i / (n_points - 1) for i in range(n_points)]

    # Calculate constraint curves
    pw_hover = [constraints.hover_power_loading(ws) for ws in ws_values]
    pw_cruise = [constraints.cruise_power_loading(ws) for ws in ws_values]
    pw_climb = [constraints.climb_power_loading(ws) for ws in ws_values]
    ws_stall = constraints.stall_constraint()

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot constraints
    ax.plot(ws_values, pw_hover, 'b-', linewidth=2, label='Hover')
    ax.plot(ws_values, pw_cruise, 'g-', linewidth=2, label='Cruise')
    ax.plot(ws_values, pw_climb, 'r-', linewidth=2, label='Climb')
    ax.axvline(x=ws_stall, color='purple', linestyle='--', linewidth=2, label=f'Stall (W/S = {ws_stall:.1f})')

    # Find feasible region
    pw_min = [max(h, c, cl) for h, c, cl in zip(pw_hover, pw_cruise, pw_climb)]
    ax.fill_between(ws_values, pw_min, max(pw_min) * 1.5, alpha=0.1, color='green', label='Feasible region')

    # Plot design point if provided
    if design_point:
        ws_dp, pw_dp = design_point
        ax.plot(ws_dp, pw_dp, 'ko', markersize=12, markerfacecolor='yellow',
                markeredgewidth=2, label=f'Design point ({ws_dp:.1f}, {pw_dp:.1f})')

    ax.set_xlabel('Wing Loading W/S (N/m²)', fontsize=12)
    ax.set_ylabel('Power Loading P/W (W/N)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(ws_min, ws_max)
    ax.set_ylim(0, max(pw_min) * 1.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_weight_breakdown(
    breakdown: MassBreakdown,
    title: str = "Mass Breakdown",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot pie chart of mass breakdown.

    Parameters
    ----------
    breakdown : MassBreakdown
        Mass breakdown object
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    # Get components and masses
    components = breakdown.components
    labels = list(components.keys())
    sizes = list(components.values())

    # Filter out zero-mass components
    filtered = [(l, s) for l, s in zip(labels, sizes) if s > 0]
    labels, sizes = zip(*filtered) if filtered else ([], [])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Custom colors
    colors = plt.cm.Set3(range(len(labels)))

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f'{pct:.1f}%\n({pct/100*sum(sizes):.2f} kg)',
        colors=colors,
        startangle=90,
        pctdistance=0.75,
    )

    # Enhance text
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)

    ax.set_title(f"{title}\nTotal: {breakdown.total:.2f} kg", fontsize=14)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_power_budget(
    powers: Dict[str, float],
    title: str = "Power Budget",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot horizontal bar chart of power budget.

    Parameters
    ----------
    powers : dict
        Dictionary of power components in Watts
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    # Sort by power consumption
    sorted_items = sorted(powers.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    total = sum(values)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create horizontal bar chart
    y_pos = range(len(labels))
    colors = plt.cm.Blues([0.3 + 0.5 * v / max(values) for v in values])
    bars = ax.barh(y_pos, values, color=colors, edgecolor='navy', linewidth=1)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        pct = 100 * val / total
        ax.text(bar.get_width() + max(values) * 0.02, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f} W ({pct:.1f}%)', va='center', fontsize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel('Power (W)', fontsize=12)
    ax.set_title(f"{title}\nTotal: {total:.1f} W", fontsize=14)
    ax.set_xlim(0, max(values) * 1.4)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_airfoil_comparison(
    polars: Dict[str, List[XfoilPolar]],
    reynolds: float,
    save_path: Optional[str] = None,
) -> None:
    """
    Plot airfoil polar comparison (CL vs CD, CL vs alpha).

    Parameters
    ----------
    polars : dict
        Dictionary mapping airfoil names to lists of polars
    reynolds : float
        Reynolds number to show
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    colors = plt.cm.tab10(range(len(polars)))

    for idx, (airfoil, polar_list) in enumerate(polars.items()):
        # Find polar at requested Reynolds
        polar = None
        for p in polar_list:
            if abs(p.reynolds - reynolds) < reynolds * 0.1:
                polar = p
                break

        if polar is None or not polar.cl:
            continue

        color = colors[idx]

        # CL vs alpha
        axes[0].plot(polar.alpha, polar.cl, '-', color=color, linewidth=2, label=airfoil)

        # CL vs CD (drag polar)
        axes[1].plot(polar.cd, polar.cl, '-', color=color, linewidth=2, label=airfoil)

        # L/D vs CL
        ld = [cl / cd if cd > 0 else 0 for cl, cd in zip(polar.cl, polar.cd)]
        axes[2].plot(polar.cl, ld, '-', color=color, linewidth=2, label=airfoil)

    # Configure axes
    axes[0].set_xlabel('α (deg)', fontsize=12)
    axes[0].set_ylabel('CL', fontsize=12)
    axes[0].set_title('Lift Curve', fontsize=14)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel('CD', fontsize=12)
    axes[1].set_ylabel('CL', fontsize=12)
    axes[1].set_title('Drag Polar', fontsize=14)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    axes[2].set_xlabel('CL', fontsize=12)
    axes[2].set_ylabel('L/D', fontsize=12)
    axes[2].set_title('Lift-to-Drag Ratio', fontsize=14)
    axes[2].legend(fontsize=10)
    axes[2].grid(True, alpha=0.3)

    fig.suptitle(f'Airfoil Comparison at Re = {reynolds:.0f}', fontsize=16)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_endurance_sensitivity(
    battery_wh_range: List[float],
    endurance_values: List[float],
    solar_endurance_values: Optional[List[float]] = None,
    title: str = "Endurance vs Battery Capacity",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot endurance sensitivity to battery capacity.

    Parameters
    ----------
    battery_wh_range : list
        Battery capacities in Wh
    endurance_values : list
        Endurance values in hours (battery only)
    solar_endurance_values : list, optional
        Endurance values with solar augmentation
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(battery_wh_range, endurance_values, 'b-o', linewidth=2,
            markersize=8, label='Battery only')

    if solar_endurance_values:
        ax.plot(battery_wh_range, solar_endurance_values, 'g-s', linewidth=2,
                markersize=8, label='Solar augmented')

    ax.set_xlabel('Battery Capacity (Wh)', fontsize=12)
    ax.set_ylabel('Endurance (hours)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_mission_profile(
    phases: List[Tuple[str, float, float]],  # (name, duration_s, power_w)
    title: str = "Mission Power Profile",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot mission power profile over time.

    Parameters
    ----------
    phases : list
        List of (phase_name, duration_s, power_w) tuples
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    check_matplotlib()

    fig, ax = plt.subplots(figsize=(12, 6))

    # Build time series
    times = [0]
    powers = []
    labels = []

    for name, duration, power in phases:
        times.append(times[-1] + duration / 60.0)  # Convert to minutes
        powers.append(power)
        labels.append(name)

    # Plot step function
    colors = plt.cm.Set2(range(len(phases)))

    for i, (name, duration, power) in enumerate(phases):
        t_start = times[i]
        t_end = times[i + 1]
        ax.fill_between([t_start, t_end], [0, 0], [power, power],
                        color=colors[i], alpha=0.7, label=name)
        ax.plot([t_start, t_end], [power, power], 'k-', linewidth=2)

        # Add label
        ax.text((t_start + t_end) / 2, power / 2, f'{power:.0f} W',
                ha='center', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('Time (minutes)', fontsize=12)
    ax.set_ylabel('Power (W)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, times[-1])
    ax.set_ylim(0, max(powers) * 1.2)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def generate_all_figures(output_dir: str = "./figures") -> None:
    """
    Generate all figures for the Mars UAV report.

    Parameters
    ----------
    output_dir : str
        Directory to save figures
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating figures...")

    # Power budgets
    print("  Power budgets...")
    powers_a = {
        "Propulsion (cruise)": 135,
        "Avionics": 15,
        "Payload (camera)": 10,
        "Thermal management": 20,
        "Communications": 8,
    }
    plot_power_budget(
        powers_a,
        title="Power Budget - Configuration A (cruise)",
        save_path=str(output_path / "power_budget_a.png"),
    )

    powers_b = {
        "Propulsion (cruise)": 421,
        "Avionics": 20,
        "Payload": 25,
        "Thermal management": 30,
        "Communications": 15,
    }
    plot_power_budget(
        powers_b,
        title="Power Budget - Configuration B (cruise)",
        save_path=str(output_path / "power_budget_b.png"),
    )

    print(f"All figures saved to: {output_path}")


if __name__ == "__main__":
    generate_all_figures()
