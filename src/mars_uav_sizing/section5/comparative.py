"""
Comparative Analysis
====================

Compares all three configurations (rotorcraft, fixed-wing, hybrid VTOL)
to support architecture selection decision in Section 6.

Provides:
- Side-by-side comparison table
- Configuration ranking
- Elimination rationale for each configuration
- Selection recommendation

Reference:
    - Manuscript: sections_en/05_04_matching-chart-methodology-sec-comparative-results.md
    - Manuscript: sections_en/06_01_architecture-selection-sec-architecture-selection.md

Last Updated: 2025-12-29
"""

from typing import Dict, Any, List
from datetime import datetime

# Import configuration loader
from ..config import get_param

# Import analysis modules
from . import rotorcraft
from . import fixed_wing
from . import hybrid_vtol


# =============================================================================
# RUN ALL ANALYSES
# =============================================================================

def run_all_analyses() -> Dict[str, Dict[str, Any]]:
    """
    Run all three configuration analyses with consistent parameters.
    
    Returns
    -------
    dict
        Dictionary with keys 'rotorcraft', 'fixed_wing', 'hybrid_vtol'
        each containing the full result dictionary from that analysis
    """
    return {
        'rotorcraft': rotorcraft.rotorcraft_feasibility_analysis(),
        'fixed_wing': fixed_wing.fixed_wing_feasibility_analysis(),
        'hybrid_vtol': hybrid_vtol.hybrid_vtol_feasibility_analysis(),
    }


# =============================================================================
# COMPARISON TABLE
# =============================================================================

def create_comparison_table(results: Dict[str, Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Create formatted comparison table data.
    
    Parameters
    ----------
    results : dict, optional
        Results from run_all_analyses() (default: compute)
    
    Returns
    -------
    dict
        Comparison data organized by metric
    """
    if results is None:
        results = run_all_analyses()
    
    rot = results['rotorcraft']
    fw = results['fixed_wing']
    hyb = results['hybrid_vtol']
    
    return {
        'VTOL Capability': {
            'Rotorcraft': ('Yes', True),
            'Fixed-Wing': ('No', False),
            'Hybrid VTOL': ('Yes', True),
        },
        'Endurance (min)': {
            'Rotorcraft': (f"{rot['endurance_min']:.0f}", rot['feasible']),
            'Fixed-Wing': (f"{fw['endurance_min']:.0f}", fw['endurance_passes']),
            'Hybrid VTOL': (f"{hyb['endurance_min']:.0f}", hyb['endurance_passes']),
        },
        'Range (km)': {
            'Rotorcraft': (f"{rot['range_km']:.0f}", rot['range_km'] >= 100),
            'Fixed-Wing': (f"{fw['range_km']:.0f}", fw['range_km'] >= 100),
            'Hybrid VTOL': (f"{hyb['range_km']:.0f}", hyb['range_km'] >= 100),
        },
        'Cruise Power (W)': {
            'Rotorcraft': (f"{rot['cruise_power_w']:.0f}", None),
            'Fixed-Wing': (f"{fw['cruise_power_w']:.0f}", None),
            'Hybrid VTOL': (f"{hyb['cruise_power_w']:.0f}", None),
        },
        'Hover Power (W)': {
            'Rotorcraft': (f"{rot['hover_power_w']:.0f}", None),
            'Fixed-Wing': ('N/A', None),
            'Hybrid VTOL': (f"{hyb['hover_power_w']:.0f}", None),
        },
        'L/D Cruise': {
            'Rotorcraft': (f"{rot['ld_effective']:.1f}", None),
            'Fixed-Wing': (f"{fw['ld_max']:.1f}", None),
            'Hybrid VTOL': (f"{hyb['ld_quadplane']:.1f}", None),
        },
        'Overall Feasible': {
            'Rotorcraft': ('No' if not rot['feasible'] else 'Marginal', rot['feasible']),
            'Fixed-Wing': ('No', False),
            'Hybrid VTOL': ('Yes', hyb['feasible']),
        },
    }


# =============================================================================
# RANKING AND SELECTION
# =============================================================================

def configuration_ranking(results: Dict[str, Dict[str, Any]] = None) -> List[str]:
    """
    Rank configurations by overall capability.
    
    Elimination criteria:
    1. Must meet VTOL requirement (eliminates fixed-wing)
    2. Must have adequate endurance margin (>10% preferred)
    
    Parameters
    ----------
    results : dict, optional
        Results from run_all_analyses()
    
    Returns
    -------
    list
        Configuration names in order of preference
    """
    if results is None:
        results = run_all_analyses()
    
    # Score each configuration
    scores = {}
    for name, res in results.items():
        score = 0
        
        # VTOL capability (mandatory)
        if name != 'fixed_wing':
            score += 100
        
        # Endurance (higher is better)
        if 'endurance_min' in res:
            score += res['endurance_min']
        
        # Range (higher is better)
        if 'range_km' in res:
            score += res['range_km'] / 10
        
        # Margin (higher is better)
        if 'margin_percent' in res and res['margin_percent'] > 0:
            score += res['margin_percent']
        
        scores[name] = score
    
    # Sort by score (descending)
    ranked = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    return ranked


def elimination_rationale(results: Dict[str, Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Generate elimination rationale for each configuration.
    
    Parameters
    ----------
    results : dict, optional
        Results from run_all_analyses()
    
    Returns
    -------
    dict
        Rationale strings for each configuration
    """
    if results is None:
        results = run_all_analyses()
    
    rot = results['rotorcraft']
    fw = results['fixed_wing']
    hyb = results['hybrid_vtol']
    
    rationale = {}
    
    # Rotorcraft
    if rot['feasible'] and rot['margin_percent'] >= 10:
        rationale['rotorcraft'] = f"VIABLE: Meets requirements with {rot['margin_percent']:.0f}% margin."
    elif rot['feasible']:
        rationale['rotorcraft'] = (
            f"ELIMINATED: Marginally meets endurance ({rot['endurance_min']:.0f} min) with only "
            f"{rot['margin_percent']:.0f}% margin. Insufficient for mission with no abort capability."
        )
    else:
        rationale['rotorcraft'] = (
            f"ELIMINATED: Fails endurance requirement ({rot['endurance_min']:.0f} min vs 60 min). "
            f"Low equivalent L/D ({rot['ld_effective']:.1f}) limits forward flight efficiency."
        )
    
    # Fixed-wing
    rationale['fixed_wing'] = (
        f"ELIMINATED: Cannot satisfy VTOL requirement. Despite excellent endurance "
        f"({fw['endurance_min']:.0f} min, +{(fw['endurance_min']/fw['requirement_min']-1)*100:.0f}% margin), "
        f"ground roll of {fw['takeoff_distance_m']:.0f} m requires runway infrastructure."
    )
    
    # Hybrid VTOL
    if hyb['feasible']:
        margin = (hyb['endurance_min'] / hyb['requirement_min'] - 1) * 100
        rationale['hybrid_vtol'] = (
            f"SELECTED: Satisfies all requirements. VTOL capability with {hyb['endurance_min']:.0f} min "
            f"endurance ({margin:.0f}% margin). Combines rotorcraft VTOL with fixed-wing cruise efficiency."
        )
    else:
        rationale['hybrid_vtol'] = (
            f"ELIMINATED: Fails to meet requirements despite hybrid architecture. "
            f"Endurance: {hyb['endurance_min']:.0f} min."
        )
    
    return rationale


# =============================================================================
# SUMMARY
# =============================================================================

def comparative_summary() -> Dict[str, Any]:
    """
    Generate complete comparative summary.
    
    Returns
    -------
    dict
        Complete analysis summary
    """
    results = run_all_analyses()
    comparison = create_comparison_table(results)
    ranking = configuration_ranking(results)
    rationale = elimination_rationale(results)
    
    return {
        'results': results,
        'comparison': comparison,
        'ranking': ranking,
        'rationale': rationale,
        'selected': ranking[0],
    }


def print_analysis(summary: Dict[str, Any] = None) -> None:
    """Print formatted comparative analysis."""
    if summary is None:
        summary = comparative_summary()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPARATIVE CONFIGURATION ANALYSIS")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print(f"Config:   All values loaded from config/ YAML files")
    print()
    
    # Comparison table
    print("CONFIGURATION COMPARISON TABLE")
    print("-" * 80)
    print(f"{'Metric':<25} {'Rotorcraft':>15} {'Fixed-Wing':>15} {'Hybrid VTOL':>15}")
    print("-" * 80)
    
    for metric, values in summary['comparison'].items():
        rot_val, rot_ok = values['Rotorcraft']
        fw_val, fw_ok = values['Fixed-Wing']
        hyb_val, hyb_ok = values['Hybrid VTOL']
        
        # Add status indicators
        rot_str = f"{rot_val}" + (" [+]" if rot_ok else " [-]" if rot_ok is False else "")
        fw_str = f"{fw_val}" + (" [+]" if fw_ok else " [-]" if fw_ok is False else "")
        hyb_str = f"{hyb_val}" + (" [+]" if hyb_ok else " [-]" if hyb_ok is False else "")
        
        print(f"{metric:<25} {rot_str:>15} {fw_str:>15} {hyb_str:>15}")
    
    print("-" * 80)
    print()
    
    # Ranking
    print("CONFIGURATION RANKING")
    print("-" * 50)
    for i, config in enumerate(summary['ranking'], 1):
        print(f"  {i}. {config.replace('_', ' ').title()}")
    print()
    
    # Elimination rationale
    print("ELIMINATION RATIONALE")
    print("-" * 80)
    for config, reason in summary['rationale'].items():
        print(f"\n{config.replace('_', ' ').upper()}:")
        print(f"  {reason}")
    print()
    
    # Final recommendation
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    selected = summary['selected']
    print(f"Selected configuration: {selected.replace('_', ' ').upper()}")
    print()
    print(summary['rationale'][selected])
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_analysis()
