"""
Plotting Functions
==================

Visualization functions for Mars UAV sizing analysis.
All parameters loaded from configuration.

Last Updated: 2025-12-29
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

# Try to import matplotlib, but don't fail if not available
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Plotting functions disabled.")

from ..config import get_param


# =============================================================================
# INTERNATIONALIZATION (i18n)
# =============================================================================

TRANSLATIONS = {
    'en': {
        # Matching chart
        'matching_chart_title': 'Matching Chart - Mars UAV',
        'matching_chart_rotorcraft_title': 'Matching Chart - Rotorcraft',
        'matching_chart_fixed_wing_title': 'Matching Chart - Fixed-Wing',
        'hover_constraint': 'Hover constraint',
        'stall_limit': 'Stall limit',
        'cruise_constraint': 'Cruise constraint',
        'design_point': 'Design point',
        'feasible_region': 'Feasible Region',
        'wing_loading': 'Wing Loading W/S (N/m²)',
        'power_loading': 'Power Loading P/W (W/N)',
        'disk_loading': 'Disk Loading DL (N/m²)',
        
        # Power comparison
        'power_title': 'Power Requirements by Configuration',
        'hover_power': 'Hover Power',
        'cruise_power': 'Cruise Power',
        'power_ylabel': 'Power (W)',
        'configuration': 'Configuration',
        
        # Endurance comparison
        'endurance_title': 'Endurance by Configuration',
        'endurance_ylabel': 'Endurance (min)',
        'requirement': 'Requirement',
        'min_unit': 'min',
        
        # Energy budget
        'energy_budget_title': 'Hybrid VTOL Energy Budget',
        'energy_ylabel': 'Energy (Wh)',
        'hover_label': 'Hover',
        'cruise': 'Cruise',
        'reserve_label': 'Reserve',
        'available': 'Available',
        'required': 'Required',
        'margin': 'Margin',
        
        # L/D comparison
        'ld_title': 'Aerodynamic Efficiency by Configuration',
        'ld_ylabel': 'Lift-to-Drag Ratio (L/D)',
        
        # Configuration names
        'rotorcraft': 'Rotorcraft',
        'fixed_wing': 'Fixed-Wing',
        'fixed_wing_no_vtol': 'Fixed-Wing\n(no VTOL)',
        'hybrid_vtol': 'Hybrid VTOL',
        'rotorcraft_equiv': 'Rotorcraft\n(equivalent)',
        'fixed_wing_pure': 'Fixed-Wing\n(pure)',
        'hybrid_vtol_qp': 'Hybrid VTOL\n(QuadPlane)',
    },
    'it': {
        # Matching chart
        'matching_chart_title': 'Diagramma di Matching - UAV Marte',
        'matching_chart_rotorcraft_title': 'Diagramma di Matching - Rotorcraft',
        'matching_chart_fixed_wing_title': 'Diagramma di Matching - Ala fissa',
        'hover_constraint': 'Vincolo hovering',
        'stall_limit': 'Limite di stallo',
        'cruise_constraint': 'Vincolo crociera',
        'design_point': 'Punto di progetto',
        'feasible_region': 'Regione ammissibile',
        'wing_loading': 'Carico alare W/S (N/m²)',
        'power_loading': 'Carico di potenza P/W (W/N)',
        'disk_loading': 'Carico del disco DL (N/m²)',
        
        # Power comparison
        'power_title': 'Requisiti di potenza per configurazione',
        'hover_power': 'Potenza hovering',
        'cruise_power': 'Potenza crociera',
        'power_ylabel': 'Potenza (W)',
        'configuration': 'Configurazione',
        
        # Endurance comparison
        'endurance_title': 'Autonomia per configurazione',
        'endurance_ylabel': 'Autonomia (min)',
        'requirement': 'Requisito',
        'min_unit': 'min',
        
        # Energy budget
        'energy_budget_title': 'Budget energetico VTOL ibrido',
        'energy_ylabel': 'Energia (Wh)',
        'hover_label': 'Hovering',
        'cruise': 'Crociera',
        'reserve_label': 'Riserva',
        'available': 'Disponibile',
        'required': 'Richiesta',
        'margin': 'Margine',
        
        # L/D comparison
        'ld_title': 'Efficienza aerodinamica per configurazione',
        'ld_ylabel': 'Rapporto portanza/resistenza (L/D)',
        
        # Configuration names
        'rotorcraft': 'Rotorcraft',
        'fixed_wing': 'Ala fissa',
        'fixed_wing_no_vtol': 'Ala fissa\n(no VTOL)',
        'hybrid_vtol': 'VTOL ibrido',
        'rotorcraft_equiv': 'Rotorcraft\n(equivalente)',
        'fixed_wing_pure': 'Ala fissa\n(pura)',
        'hybrid_vtol_qp': 'VTOL ibrido\n(QuadPlane)',
    }
}


def get_text(key: str, lang: str = 'en') -> str:
    """Get translated text for a key."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


def check_matplotlib():
    """Check if matplotlib is available."""
    if not HAS_MATPLOTLIB:
        raise ImportError(
            "matplotlib is required for plotting. "
            "Install with: pip install matplotlib"
        )


def plot_constraint_diagram(
    ws_range: np.ndarray = None,
    pw_hover: float = None,
    pw_cruise: np.ndarray = None,
    ws_stall: float = None,
    design_point: Tuple[float, float] = None,
    title: str = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot the matching chart (constraint diagram).
    
    Shows P/W vs W/S with:
    - Hover constraint (horizontal line)
    - Stall constraint (vertical line)
    - Cruise constraint (curve)
    - Design point
    
    Parameters
    ----------
    ws_range : np.ndarray
        Wing loading values for cruise curve
    pw_hover : float
        Hover power loading (horizontal line)
    pw_cruise : np.ndarray
        Cruise power loading curve
    ws_stall : float
        Stall wing loading limit (vertical line)
    design_point : tuple
        (W/S, P/W) of design point
    title : str
        Plot title (default: translated)
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display the plot
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if title is None:
        title = get_text('matching_chart_title', lang)
    
    # Create default data if not provided
    if ws_range is None:
        ws_range = np.linspace(2, 15, 100)
    
    if pw_hover is None:
        from ..section5 import matching_chart
        pw_hover = matching_chart.hover_constraint()
    
    if pw_cruise is None:
        from ..section5 import matching_chart
        pw_cruise = matching_chart.cruise_constraint_curve(ws_range)
    
    if ws_stall is None:
        from ..section5 import matching_chart
        ws_stall = matching_chart.stall_constraint()
    
    if design_point is None:
        from ..section5 import matching_chart
        dp = matching_chart.find_design_point()
        design_point = (dp['wing_loading'], dp['power_loading'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot constraints with translated labels (no bracketed numerical values)
    ax.axhline(y=pw_hover, color='red', linestyle='-', linewidth=2, 
               label=get_text('hover_constraint', lang))
    
    ax.axvline(x=ws_stall, color='green', linestyle='--', linewidth=2,
               label=get_text('stall_limit', lang))
    
    ax.plot(ws_range, pw_cruise, 'b-', linewidth=2,
            label=get_text('cruise_constraint', lang))
    
    # Shade feasible region
    ws_feasible = ws_range[ws_range <= ws_stall]
    pw_cruise_feasible = pw_cruise[:len(ws_feasible)]
    
    # Fill above hover line (infeasible) - light red
    ax.fill_between(ws_range, pw_hover, 150, alpha=0.1, color='red')
    
    # Fill right of stall (infeasible) - light green
    ax.axvspan(ws_stall, ws_range[-1], alpha=0.1, color='green')
    
    # Mark design point
    ax.scatter(*design_point, s=200, c='black', marker='*', zorder=5,
               label=get_text('design_point', lang))
    
    # Formatting with translated labels
    ax.set_xlabel(get_text('wing_loading', lang), fontsize=12)
    ax.set_ylabel(get_text('power_loading', lang), fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, ws_range[-1] * 1.1)
    ax.set_ylim(0, pw_hover * 1.8)
    
    # Add annotations
    ax.annotate(get_text('feasible_region', lang), 
                xy=(ws_stall/2, pw_hover*1.05),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_rotorcraft_matching_chart(
    title: str = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot matching chart for pure rotorcraft configuration.
    
    For rotorcraft, the only design driver is hover power. The chart shows
    power loading (P/W) vs disk loading (DL), with the constraint curve
    from actuator disk theory.
    
    The relationship is: P/W = (1/η_hover) × sqrt(DL/(2ρ))
    
    Parameters
    ----------
    title : str
        Plot title (default: translated)
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display the plot
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if title is None:
        title = get_text('matching_chart_rotorcraft_title', lang)
    
    # Get atmospheric parameters
    from ..config import get_density, get_propulsion_efficiencies
    rho = get_density()
    prop = get_propulsion_efficiencies()
    
    # Combined hover efficiency
    eta_hover = prop['figure_of_merit'] * prop['eta_motor'] * prop['eta_esc']
    
    # Disk loading range (N/m²)
    dl_range = np.linspace(10, 100, 100)
    
    # Power loading from actuator disk theory: P/W = (1/η) × sqrt(DL/(2ρ))
    pw_hover = (1 / eta_hover) * np.sqrt(dl_range / (2 * rho))
    
    # Get design disk loading from config
    from ..config import get_param
    dl_design = get_param('geometry.rotor.disk_loading_N_m2')
    pw_design = (1 / eta_hover) * np.sqrt(dl_design / (2 * rho))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot hover constraint curve
    ax.plot(dl_range, pw_hover, 'r-', linewidth=2.5,
            label=get_text('hover_constraint', lang))
    
    # Mark design point
    ax.scatter(dl_design, pw_design, s=200, c='black', marker='*', zorder=5,
               label=get_text('design_point', lang))
    
    # Shade infeasible region (below the curve is infeasible - need more power)
    ax.fill_between(dl_range, 0, pw_hover, alpha=0.1, color='red')
    
    # Formatting with translated labels
    ax.set_xlabel(get_text('disk_loading', lang), fontsize=12)
    ax.set_ylabel(get_text('power_loading', lang), fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, dl_range[-1] * 1.1)
    ax.set_ylim(0, max(pw_hover) * 1.2)
    
    # Add annotation
    ax.annotate(get_text('feasible_region', lang), 
                xy=(dl_range[-1] * 0.7, max(pw_hover) * 1.05),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_fixed_wing_matching_chart(
    title: str = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot matching chart for pure fixed-wing configuration.
    
    For fixed-wing aircraft, the constraints are:
    - Cruise constraint: P/W = V / (L/D × η_cruise)
    - Stall constraint: (W/S)_max = 0.5 × ρ × V_min² × C_L,max
    
    Parameters
    ----------
    title : str
        Plot title (default: translated)
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display the plot
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if title is None:
        title = get_text('matching_chart_fixed_wing_title', lang)
    
    # Get parameters from config
    from ..config import get_density, get_mission_params, get_aerodynamic_params, get_param
    from ..section5.fixed_wing import cruise_lift_coefficient, lift_to_drag, cruise_power_loading, stall_wing_loading_limit
    
    rho = get_density()
    mission = get_mission_params()
    aero = get_aerodynamic_params()
    
    v_cruise = mission['v_cruise']
    v_stall = mission['v_stall']
    v_min_factor = get_param('mission.velocity.v_min_factor')
    v_min = v_stall * v_min_factor
    cl_max = aero['cl_max']
    
    # Wing loading range (N/m²)
    ws_range = np.linspace(2, 15, 100)
    
    # Calculate cruise constraint curve (no QuadPlane penalty for pure fixed-wing)
    pw_cruise = []
    for ws in ws_range:
        cl = cruise_lift_coefficient(ws, rho, v_cruise)
        ld = lift_to_drag(cl)  # Pure L/D without penalty
        pw = cruise_power_loading(v_cruise, ld)
        pw_cruise.append(pw)
    pw_cruise = np.array(pw_cruise)
    
    # Stall constraint (vertical line)
    ws_stall = stall_wing_loading_limit(rho, v_min, cl_max)
    
    # Design point: maximum W/S (at stall) with corresponding cruise P/W
    cl_design = cruise_lift_coefficient(ws_stall, rho, v_cruise)
    ld_design = lift_to_drag(cl_design)
    pw_design = cruise_power_loading(v_cruise, ld_design)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot cruise constraint
    ax.plot(ws_range, pw_cruise, 'b-', linewidth=2,
            label=get_text('cruise_constraint', lang))
    
    # Plot stall constraint (vertical line)
    ax.axvline(x=ws_stall, color='green', linestyle='--', linewidth=2,
               label=get_text('stall_limit', lang))
    
    # Shade infeasible region (right of stall)
    ax.axvspan(ws_stall, ws_range[-1], alpha=0.1, color='green')
    
    # Mark design point
    ax.scatter(ws_stall, pw_design, s=200, c='black', marker='*', zorder=5,
               label=get_text('design_point', lang))
    
    # Formatting with translated labels
    ax.set_xlabel(get_text('wing_loading', lang), fontsize=12)
    ax.set_ylabel(get_text('power_loading', lang), fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, ws_range[-1] * 1.1)
    ax.set_ylim(0, max(pw_cruise) * 1.3)
    
    # Add annotation
    ax.annotate(get_text('feasible_region', lang), 
                xy=(ws_stall/2, max(pw_cruise) * 0.9),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_power_comparison(
    results: Dict[str, Dict[str, Any]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot power comparison across configurations.
    
    Bar chart comparing hover and cruise power for each configuration.
    
    Parameters
    ----------
    results : dict
        Results from comparative analysis
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if results is None:
        from ..section5 import comparative
        results = comparative.run_all_analyses()
    
    # Extract data with translated labels
    configs = [
        get_text('rotorcraft', lang), 
        get_text('fixed_wing', lang), 
        get_text('hybrid_vtol', lang)
    ]
    hover_power = [
        results['rotorcraft']['hover_power_w'],
        0,  # Fixed-wing has no hover
        results['hybrid_vtol']['hover_power_w'],
    ]
    cruise_power = [
        results['rotorcraft']['cruise_power_w'],
        results['fixed_wing']['cruise_power_w'],
        results['hybrid_vtol']['cruise_power_w'],
    ]
    
    x = np.arange(len(configs))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width/2, hover_power, width, 
                   label=get_text('hover_power', lang), color='coral')
    bars2 = ax.bar(x + width/2, cruise_power, width, 
                   label=get_text('cruise_power', lang), color='steelblue')
    
    ax.set_xlabel(get_text('configuration', lang), fontsize=12)
    ax.set_ylabel(get_text('power_ylabel', lang), fontsize=12)
    ax.set_title(get_text('power_title', lang), fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(configs)
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis limit with headroom for labels
    max_power = max(max(hover_power), max(cruise_power))
    ax.set_ylim(0, max_power * 1.25)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.0f}',
                       xy=(bar.get_x() + bar.get_width()/2, height),
                       ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                   xy=(bar.get_x() + bar.get_width()/2, height),
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_endurance_comparison(
    results: Dict[str, Dict[str, Any]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot endurance comparison across configurations.
    
    Bar chart with 60-minute requirement line.
    
    Parameters
    ----------
    results : dict
        Results from comparative analysis
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if results is None:
        from ..section5 import comparative
        results = comparative.run_all_analyses()
    
    configs = [
        get_text('rotorcraft', lang), 
        get_text('fixed_wing_no_vtol', lang), 
        get_text('hybrid_vtol', lang)
    ]
    endurance = [
        results['rotorcraft']['endurance_min'],
        results['fixed_wing']['endurance_min'],
        results['hybrid_vtol']['endurance_min'],
    ]
    
    colors = ['salmon', 'salmon', 'lightgreen']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    bars = ax.bar(configs, endurance, color=colors, edgecolor='black')
    
    # Add requirement line
    ax.axhline(y=60, color='red', linestyle='--', linewidth=2, 
               label=f'{get_text("requirement", lang)} (60 min)')
    
    ax.set_ylabel(get_text('endurance_ylabel', lang), fontsize=12)
    ax.set_title(get_text('endurance_title', lang), fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis limit with headroom
    max_endurance = max(endurance)
    ax.set_ylim(0, max_endurance * 1.15)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_energy_budget(
    results: Dict[str, Dict[str, Any]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot energy budget breakdown for hybrid VTOL.
    
    Stacked bar chart showing hover vs cruise vs reserve energy.
    
    Parameters
    ----------
    results : dict
        Results from comparative analysis
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if results is None:
        from ..section5 import comparative
        results = comparative.run_all_analyses()
    
    hyb = results['hybrid_vtol']
    
    # Energy components for hybrid VTOL
    hover_energy = hyb.get('hover_energy_wh', 158.9)
    cruise_energy = hyb.get('cruise_energy_wh', 302.0)
    reserve_energy = hyb.get('reserve_energy_wh', 92.2)
    available_energy = hyb.get('available_energy_wh', 718.2)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create stacked bar for energy budget
    categories = [get_text('required', lang), get_text('available', lang)]
    hover = [hover_energy, 0]
    cruise = [cruise_energy, 0]
    reserve = [reserve_energy, 0]
    available = [0, available_energy]
    
    x = np.arange(len(categories))
    width = 0.5
    
    bars1 = ax.bar(x, hover, width, label=get_text('hover_label', lang), color='coral')
    bars2 = ax.bar(x, cruise, width, bottom=hover, label=get_text('cruise', lang), color='steelblue')
    bars3 = ax.bar(x, reserve, width, bottom=[h+c for h,c in zip(hover, cruise)], 
                   label=get_text('reserve_label', lang), color='gold')
    bars4 = ax.bar(x, available, width, label=get_text('available', lang), color='lightgreen')
    
    ax.set_ylabel(get_text('energy_ylabel', lang), fontsize=12)
    ax.set_title(get_text('energy_budget_title', lang), fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    # Position legend outside the plot area to avoid overlapping bars
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis limit with headroom for labels and legend
    max_energy = max(available_energy, hover_energy + cruise_energy + reserve_energy)
    ax.set_ylim(0, max_energy * 1.25)
    
    # Add value labels
    total_required = hover_energy + cruise_energy + reserve_energy
    ax.annotate(f'{total_required:.0f} Wh',
               xy=(0, total_required),
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.annotate(f'{available_energy:.0f} Wh',
               xy=(1, available_energy),
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add margin annotation
    margin_pct = (available_energy - total_required) / total_required * 100
    ax.annotate(f'{get_text("margin", lang)}: +{margin_pct:.0f}%',
               xy=(0.5, (total_required + available_energy) / 2),
               ha='center', va='center', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_ld_comparison(
    results: Dict[str, Dict[str, Any]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
) -> None:
    """
    Plot lift-to-drag ratio comparison across configurations.
    
    Bar chart comparing L/D values.
    
    Parameters
    ----------
    results : dict
        Results from comparative analysis
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    if results is None:
        from ..section5 import comparative
        results = comparative.run_all_analyses()
    
    configs = [
        get_text('rotorcraft_equiv', lang), 
        get_text('fixed_wing_pure', lang), 
        get_text('hybrid_vtol_qp', lang)
    ]
    ld_values = [
        results['rotorcraft']['ld_effective'],
        results['fixed_wing']['ld_max'],
        results['hybrid_vtol']['ld_quadplane'],
    ]
    
    colors = ['salmon', 'lightgreen', 'steelblue']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    bars = ax.bar(configs, ld_values, color=colors, edgecolor='black')
    
    ax.set_ylabel(get_text('ld_ylabel', lang), fontsize=12)
    ax.set_title(get_text('ld_title', lang), fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis limit with headroom
    max_ld = max(ld_values)
    ax.set_ylim(0, max_ld * 1.15)
    
    # Add value labels
    for bar, ld in zip(bars, ld_values):
        ax.annotate(f'{ld:.1f}',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_all_figures(output_dir: str = "./figures", lang: str = 'en') -> None:
    """
    Generate all standard figures in specified language.
    
    Parameters
    ----------
    output_dir : str
        Directory to save figures
    lang : str
        Language code ('en' or 'it')
    """
    check_matplotlib()
    
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)
    
    # Language suffix for filenames (empty for English, _it for Italian)
    suffix = '' if lang == 'en' else f'_{lang}'
    
    print(f"Generating figures ({lang.upper()})...")
    
    # Constraint diagram - Hybrid VTOL (QuadPlane)
    plot_constraint_diagram(
        save_path=out_path / f"matching_chart{suffix}.png",
        show=False,
        lang=lang
    )
    
    # Constraint diagram - Rotorcraft
    plot_rotorcraft_matching_chart(
        save_path=out_path / f"matching_chart_rotorcraft{suffix}.png",
        show=False,
        lang=lang
    )
    
    # Constraint diagram - Fixed-Wing
    plot_fixed_wing_matching_chart(
        save_path=out_path / f"matching_chart_fixed_wing{suffix}.png",
        show=False,
        lang=lang
    )
    
    # Power comparison
    plot_power_comparison(
        save_path=out_path / f"power_comparison{suffix}.png",
        show=False,
        lang=lang
    )
    
    # Endurance comparison
    plot_endurance_comparison(
        save_path=out_path / f"endurance_comparison{suffix}.png",
        show=False,
        lang=lang
    )
    
    # Energy budget
    plot_energy_budget(
        save_path=out_path / f"energy_budget{suffix}.png",
        show=False,
        lang=lang
    )
    
    # L/D comparison
    plot_ld_comparison(
        save_path=out_path / f"ld_comparison{suffix}.png",
        show=False,
        lang=lang
    )
    
    print(f"All figures ({lang.upper()}) saved to {output_dir}/")


def generate_all_figures_bilingual(output_dir: str = "./figures") -> None:
    """
    Generate all figures in both English and Italian.
    
    Parameters
    ----------
    output_dir : str
        Directory to save figures
    """
    # Generate English versions
    generate_all_figures(output_dir, lang='en')
    
    # Generate Italian versions
    generate_all_figures(output_dir, lang='it')
    
    print(f"\nBilingual figure generation complete!")


if __name__ == "__main__":
    # Generate all figures in both languages when run directly
    generate_all_figures_bilingual()

