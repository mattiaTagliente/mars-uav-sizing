#!/usr/bin/env python3
"""
Airfoil Plotting Module
=======================

Generates comparison plots for airfoil selection (Section 6.2).
Supports English and Italian output.

Plots generated:
    - Cl vs alpha (lift curve)
    - Cd vs alpha (drag curve)
    - Cl vs Cd (drag polar)
    - L/D vs alpha (efficiency curve)

All data loaded from config/airfoil_data.yaml - no hardcoded values.

Last Updated: 2025-12-31
"""

from pathlib import Path
from typing import Optional, Dict, List
import numpy as np

from .airfoil_selection import load_airfoil_data, AirfoilPolar

# Try to import matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
TRANSLATIONS = {
    'en': {
        'title_cl_alpha': 'Lift Coefficient vs Angle of Attack',
        'title_cd_alpha': 'Drag Coefficient vs Angle of Attack',
        'title_polar': 'Drag Polar',
        'title_ld_alpha': 'Lift-to-Drag Ratio vs Angle of Attack',
        'xlabel_alpha': 'Angle of Attack α (°)',
        'ylabel_cl': 'Lift Coefficient $C_L$',
        'ylabel_cd': 'Drag Coefficient $C_D$',
        'ylabel_ld': 'Lift-to-Drag Ratio L/D',
        'xlabel_cd': 'Drag Coefficient $C_D$',
        'subtitle': 'Re ≈ 60,000 (UIUC wind tunnel data)',
        'max_marker': 'max',
    },
    'it': {
        'title_cl_alpha': 'Coefficiente di portanza vs angolo di attacco',
        'title_cd_alpha': 'Coefficiente di resistenza vs angolo di attacco',
        'title_polar': 'Polare di resistenza',
        'title_ld_alpha': 'Efficienza aerodinamica vs angolo di attacco',
        'xlabel_alpha': 'Angolo di attacco α (°)',
        'ylabel_cl': 'Coefficiente di portanza $C_L$',
        'ylabel_cd': 'Coefficiente di resistenza $C_D$',
        'ylabel_ld': 'Rapporto portanza/resistenza L/D',
        'xlabel_cd': 'Coefficiente di resistenza $C_D$',
        'subtitle': 'Re ≈ 60.000 (dati galleria del vento UIUC)',
        'max_marker': 'max',
    }
}


def get_text(key: str, lang: str = 'en') -> str:
    """Get translated text."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


# Color palette for airfoils (consistent across all plots)
AIRFOIL_COLORS = {
    'e387': '#1f77b4',      # Blue (selected)
    'sd8000': '#ff7f0e',    # Orange
    's7055': '#2ca02c',     # Green
    'ag455ct-02r': '#d62728',  # Red
    'sd7037b': '#9467bd',   # Purple
    'ag12': '#8c564b',      # Brown
    'ag35-r': '#e377c2',    # Pink
}

# Line styles
AIRFOIL_STYLES = {
    'e387': '-',        # Solid (selected)
    'sd8000': '--',     # Dashed
    's7055': '-.',      # Dash-dot
    'ag455ct-02r': ':',    # Dotted
    'sd7037b': '--',    # Dashed
    'ag12': '-.',       # Dash-dot
    'ag35-r': ':',      # Dotted
}


def _setup_plot_style():
    """Configure matplotlib style for publication-quality figures."""
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'legend.fontsize': 9,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.grid': True,
        'grid.alpha': 0.3,
    })


def plot_cl_alpha(
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
    highlight_airfoil: str = 'e387',
) -> None:
    """
    Plot lift coefficient vs angle of attack for all airfoils.
    
    Parameters
    ----------
    save_path : str, optional
        Path to save figure
    show : bool
        Whether to display the plot
    lang : str
        Language code ('en' or 'it')
    highlight_airfoil : str
        Airfoil to highlight (thicker line, marker at max)
    """
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available")
        return
    
    _setup_plot_style()
    polars = load_airfoil_data()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, polar in polars.items():
        alpha, cl, cd, ld = polar.get_arrays()
        
        linewidth = 2.5 if name == highlight_airfoil else 1.5
        color = AIRFOIL_COLORS.get(name, '#333333')
        style = AIRFOIL_STYLES.get(name, '-')
        
        ax.plot(alpha, cl, style, color=color, linewidth=linewidth,
                label=name.upper())
        
        # Mark Cl_max for highlighted airfoil
        if name == highlight_airfoil:
            idx_max = cl.index(max(cl))
            ax.plot(alpha[idx_max], cl[idx_max], 'o', color=color, markersize=8)
            ax.annotate(f"$C_{{L,{get_text('max_marker', lang)}}}$ = {cl[idx_max]:.2f}",
                       xy=(alpha[idx_max], cl[idx_max]),
                       xytext=(alpha[idx_max] + 2, cl[idx_max] - 0.1),
                       fontsize=9)
    
    ax.set_xlabel(get_text('xlabel_alpha', lang))
    ax.set_ylabel(get_text('ylabel_cl', lang))
    ax.set_title(get_text('title_cl_alpha', lang))
    ax.legend(loc='lower right', ncol=2)
    ax.set_xlim(-6, 14)
    ax.set_ylim(-0.5, 1.4)
    
    # Add subtitle
    ax.text(0.5, -0.12, get_text('subtitle', lang),
            transform=ax.transAxes, ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_cd_alpha(
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
    highlight_airfoil: str = 'e387',
) -> None:
    """
    Plot drag coefficient vs angle of attack for all airfoils.
    """
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available")
        return
    
    _setup_plot_style()
    polars = load_airfoil_data()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, polar in polars.items():
        alpha, cl, cd, ld = polar.get_arrays()
        
        linewidth = 2.5 if name == highlight_airfoil else 1.5
        color = AIRFOIL_COLORS.get(name, '#333333')
        style = AIRFOIL_STYLES.get(name, '-')
        
        ax.plot(alpha, cd, style, color=color, linewidth=linewidth,
                label=name.upper())
        
        # Mark Cd_min for highlighted airfoil
        if name == highlight_airfoil:
            idx_min = cd.index(min(cd))
            ax.plot(alpha[idx_min], cd[idx_min], 'o', color=color, markersize=8)
            ax.annotate(f"$C_{{D,min}}$ = {cd[idx_min]:.4f}",
                       xy=(alpha[idx_min], cd[idx_min]),
                       xytext=(alpha[idx_min] + 2, cd[idx_min] + 0.01),
                       fontsize=9)
    
    ax.set_xlabel(get_text('xlabel_alpha', lang))
    ax.set_ylabel(get_text('ylabel_cd', lang))
    ax.set_title(get_text('title_cd_alpha', lang))
    ax.legend(loc='upper left', ncol=2)
    ax.set_xlim(-6, 14)
    ax.set_ylim(0, 0.08)
    
    ax.text(0.5, -0.12, get_text('subtitle', lang),
            transform=ax.transAxes, ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_drag_polar(
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
    highlight_airfoil: str = 'e387',
) -> None:
    """
    Plot drag polar (Cl vs Cd) for all airfoils.
    """
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available")
        return
    
    _setup_plot_style()
    polars = load_airfoil_data()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, polar in polars.items():
        alpha, cl, cd, ld = polar.get_arrays()
        
        linewidth = 2.5 if name == highlight_airfoil else 1.5
        color = AIRFOIL_COLORS.get(name, '#333333')
        style = AIRFOIL_STYLES.get(name, '-')
        
        ax.plot(cd, cl, style, color=color, linewidth=linewidth,
                label=name.upper())
        
        # Mark (L/D)_max point for highlighted airfoil
        if name == highlight_airfoil:
            idx_max_ld = ld.index(max(ld))
            ax.plot(cd[idx_max_ld], cl[idx_max_ld], 'o', color=color, markersize=8)
            ax.annotate(f"$(L/D)_{{max}}$",
                       xy=(cd[idx_max_ld], cl[idx_max_ld]),
                       xytext=(cd[idx_max_ld] + 0.005, cl[idx_max_ld] - 0.08),
                       fontsize=9)
    
    ax.set_xlabel(get_text('xlabel_cd', lang))
    ax.set_ylabel(get_text('ylabel_cl', lang))
    ax.set_title(get_text('title_polar', lang))
    ax.legend(loc='lower right', ncol=2)
    ax.set_xlim(0, 0.08)
    ax.set_ylim(-0.5, 1.4)
    
    ax.text(0.5, -0.12, get_text('subtitle', lang),
            transform=ax.transAxes, ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_ld_alpha(
    save_path: Optional[str] = None,
    show: bool = True,
    lang: str = 'en',
    highlight_airfoil: str = 'e387',
) -> None:
    """
    Plot lift-to-drag ratio vs angle of attack for all airfoils.
    """
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available")
        return
    
    _setup_plot_style()
    polars = load_airfoil_data()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, polar in polars.items():
        alpha, cl, cd, ld = polar.get_arrays()
        
        # Filter out negative L/D for cleaner plot
        alpha_pos = [a for a, l in zip(alpha, ld) if l > 0]
        ld_pos = [l for l in ld if l > 0]
        
        linewidth = 2.5 if name == highlight_airfoil else 1.5
        color = AIRFOIL_COLORS.get(name, '#333333')
        style = AIRFOIL_STYLES.get(name, '-')
        
        ax.plot(alpha_pos, ld_pos, style, color=color, linewidth=linewidth,
                label=name.upper())
        
        # Mark (L/D)_max for highlighted airfoil
        if name == highlight_airfoil and ld_pos:
            max_ld = max(ld_pos)
            idx_max = ld_pos.index(max_ld)
            ax.plot(alpha_pos[idx_max], ld_pos[idx_max], 'o', color=color, markersize=8)
            ax.annotate(f"$(L/D)_{{max}}$ = {max_ld:.1f}",
                       xy=(alpha_pos[idx_max], ld_pos[idx_max]),
                       xytext=(alpha_pos[idx_max] - 3, ld_pos[idx_max] + 3),
                       fontsize=9)
    
    ax.set_xlabel(get_text('xlabel_alpha', lang))
    ax.set_ylabel(get_text('ylabel_ld', lang))
    ax.set_title(get_text('title_ld_alpha', lang))
    ax.legend(loc='upper right', ncol=2)
    ax.set_xlim(-2, 14)
    ax.set_ylim(0, 55)
    
    ax.text(0.5, -0.12, get_text('subtitle', lang),
            transform=ax.transAxes, ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_all_airfoil_figures(
    output_dir: str = None,
    show: bool = False,
) -> Dict[str, str]:
    """
    Generate all airfoil comparison figures in English and Italian.
    
    Parameters
    ----------
    output_dir : str, optional
        Directory to save figures. If None, uses figures/
    show : bool
        Whether to display plots
    
    Returns
    -------
    dict
        Paths to generated figures
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent.parent / "figures"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    paths = {}
    
    # Generate for both languages
    for lang in ['en', 'it']:
        suffix = f"_{lang}"
        
        # Cl vs alpha
        path = output_dir / f"airfoil_cl_alpha{suffix}.png"
        plot_cl_alpha(save_path=str(path), show=show, lang=lang)
        paths[f'cl_alpha_{lang}'] = str(path)
        
        # Cd vs alpha
        path = output_dir / f"airfoil_cd_alpha{suffix}.png"
        plot_cd_alpha(save_path=str(path), show=show, lang=lang)
        paths[f'cd_alpha_{lang}'] = str(path)
        
        # Drag polar
        path = output_dir / f"airfoil_polar{suffix}.png"
        plot_drag_polar(save_path=str(path), show=show, lang=lang)
        paths[f'polar_{lang}'] = str(path)
        
        # L/D vs alpha
        path = output_dir / f"airfoil_ld_alpha{suffix}.png"
        plot_ld_alpha(save_path=str(path), show=show, lang=lang)
        paths[f'ld_alpha_{lang}'] = str(path)
    
    print(f"\nGenerated {len(paths)} figures in {output_dir}")
    return paths


if __name__ == "__main__":
    print("Generating airfoil comparison figures...")
    paths = generate_all_airfoil_figures(show=False)
    for name, path in paths.items():
        print(f"  {name}: {path}")
