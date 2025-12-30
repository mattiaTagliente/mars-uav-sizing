"""
Comparative Analysis
====================

Implements the comparative analysis from manuscript Section 5.5.
Compares all three configurations to determine the optimal choice.

Reference: 
- Manuscript: sections_en/05_05_comparative-results.md
- Prompt: docs/prompt_04_python_implementation.txt

Updated 2025-12-28: Parameters aligned with sections 2, 3, 4 of manuscript.
"""

import math
from typing import Dict, Any, List
from datetime import datetime

from .rotorcraft_analysis import rotorcraft_feasibility_analysis
from .fixed_wing_analysis import fixed_wing_feasibility_analysis
from .hybrid_vtol_analysis import hybrid_vtol_feasibility


# Default parameters
G_MARS = 3.711          # m/s²
MTOW_BASELINE_KG = 10.0


def run_all_analyses(mtow_kg: float = MTOW_BASELINE_KG) -> Dict[str, Dict[str, Any]]:
    """Run all three configuration analyses with consistent parameters.
    
    Parameters
    ----------
    mtow_kg : float
        MTOW for all configurations in kg
    
    Returns
    -------
    dict
        Dictionary with keys 'rotorcraft', 'fixed_wing', 'hybrid_vtol'
        each containing the full result dictionary from that analysis
    """
    results = {}
    
    # Rotorcraft analysis
    results['rotorcraft'] = rotorcraft_feasibility_analysis(mtow_kg=mtow_kg)
    
    # Fixed-wing analysis
    results['fixed_wing'] = fixed_wing_feasibility_analysis(mtow_kg=mtow_kg)
    
    # Hybrid VTOL analysis
    results['hybrid_vtol'] = hybrid_vtol_feasibility(mtow_kg=mtow_kg)
    
    return results


def create_comparison_table(results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Create formatted comparison table.
    
    Implements content of @tbl:configuration-comparison from §5.5.
    
    Parameters
    ----------
    results : dict
        Results from run_all_analyses()
    
    Returns
    -------
    dict
        Comparison data organized by metric
    """
    rc = results['rotorcraft']
    fw = results['fixed_wing']
    hv = results['hybrid_vtol']
    
    comparison = {
        'mtow_kg': {
            'rotorcraft': rc['mtow_kg'],
            'fixed_wing': fw['mtow_kg'],
            'hybrid_vtol': hv['mtow_kg'],
        },
        'ld_effective': {
            'rotorcraft': rc['ld_effective'],
            'fixed_wing': fw['ld_max'],
            'hybrid_vtol': hv['ld_quadplane'],
            'unit': '—',
        },
        'hover_power_w': {
            'rotorcraft': rc['hover_power_w'],
            'fixed_wing': 0,  # N/A
            'hybrid_vtol': hv['hover_power_w'],
            'unit': 'W',
        },
        'cruise_power_w': {
            'rotorcraft': rc['cruise_power_w'],
            'fixed_wing': fw['cruise_power_w'],
            'hybrid_vtol': hv['cruise_power_w'],
            'unit': 'W',
        },
        'endurance_min': {
            'rotorcraft': rc['endurance_min'],
            'fixed_wing': fw['endurance_with_reserve_min'],
            'hybrid_vtol': hv['endurance_min'],
            'unit': 'min',
        },
        'range_km': {
            'rotorcraft': rc['range_km'],
            'fixed_wing': fw['range_km'],
            'hybrid_vtol': hv['range_km'],
            'unit': 'km',
        },
        'endurance_margin_percent': {
            'rotorcraft': rc['margin_percent'],
            'fixed_wing': (fw['endurance_with_reserve_min'] / 60 - 1) * 100,
            'hybrid_vtol': hv['endurance_margin_percent'],
            'unit': '%',
        },
        'vtol_capable': {
            'rotorcraft': True,
            'fixed_wing': False,
            'hybrid_vtol': True,
        },
        'feasible': {
            'rotorcraft': rc['feasible'],
            'fixed_wing': fw['feasible'],
            'hybrid_vtol': hv['feasible'],
        },
    }
    
    return comparison


def configuration_ranking(comparison: Dict[str, Dict[str, Any]]) -> List[str]:
    """Rank configurations by overall capability.
    
    Elimination criteria (from §5.5):
    1. Must meet VTOL requirement (eliminates fixed-wing)
    2. Must have adequate endurance margin (>10% preferred)
    3. Preference for higher energy margin
    
    Parameters
    ----------
    comparison : dict
        Comparison data from create_comparison_table()
    
    Returns
    -------
    list
        Configuration names in order of preference
    """
    ranking = []
    
    # Check feasibility
    configs = ['rotorcraft', 'fixed_wing', 'hybrid_vtol']
    
    for config in configs:
        score = 0
        
        # VTOL requirement is critical
        if comparison['vtol_capable'][config]:
            score += 100
        
        # Endurance margin
        score += comparison['endurance_margin_percent'][config]
        
        # Range capability
        score += comparison['range_km'][config] / 10
        
        # L/D efficiency
        score += comparison['ld_effective'][config] * 2
        
        # Overall feasibility
        if comparison['feasible'][config]:
            score += 50
        
        ranking.append((config, score))
    
    # Sort by score descending
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    return [config for config, score in ranking]


def elimination_rationale(results: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """Generate elimination rationale for each configuration.
    
    Content for §5.5 elimination discussion.
    
    Parameters
    ----------
    results : dict
        Results from run_all_analyses()
    
    Returns
    -------
    dict
        Rationale strings for each configuration
    """
    rc = results['rotorcraft']
    fw = results['fixed_wing']
    hv = results['hybrid_vtol']
    
    rationale = {}
    
    # Rotorcraft rationale
    if rc['margin_percent'] < 20:
        rationale['rotorcraft'] = (
            f"ELIMINATED: Insufficient margin ({rc['margin_percent']:.0f}%). "
            f"Low equivalent L/D ({rc['ld_effective']:.1f}) limits endurance. "
            f"No abort capability if mission extends."
        )
    elif not rc['feasible']:
        rationale['rotorcraft'] = (
            f"ELIMINATED: Does not meet 60 min endurance requirement. "
            f"Achieved only {rc['endurance_min']:.0f} min."
        )
    else:
        rationale['rotorcraft'] = (
            f"Technically feasible with {rc['margin_percent']:.0f}% margin, "
            f"but margin is thin for mission-critical application."
        )
    
    # Fixed-wing rationale
    rationale['fixed_wing'] = (
        f"ELIMINATED: Cannot meet VTOL requirement. "
        f"Takeoff roll of {fw['takeoff_roll_m']:.0f} m is impractical. "
        f"Despite excellent L/D ({fw['ld_max']:.1f}) and endurance ({fw['endurance_with_reserve_min']:.0f} min)."
    )
    
    # Hybrid VTOL rationale
    if hv['feasible']:
        rationale['hybrid_vtol'] = (
            f"SELECTED: Meets all requirements. "
            f"VTOL + cruise efficiency (L/D = {hv['ld_quadplane']:.1f}). "
            f"Endurance margin {hv['endurance_margin_percent']:.0f}%. "
            f"Energy margin {hv['energy_margin_percent']:.0f}%."
        )
    else:
        rationale['hybrid_vtol'] = (
            f"Does not meet requirements with current parameters. "
            f"Energy margin: {hv['energy_margin_percent']:.0f}%."
        )
    
    return rationale


def comparative_summary(mtow_kg: float = MTOW_BASELINE_KG) -> Dict[str, Any]:
    """Generate complete comparative summary.
    
    Main entry point for comparative analysis.
    Produces all data for §5.5.
    
    Parameters
    ----------
    mtow_kg : float
        MTOW for analysis
    
    Returns
    -------
    dict
        Complete analysis summary
    """
    # Run all analyses
    results = run_all_analyses(mtow_kg)
    
    # Create comparison
    comparison = create_comparison_table(results)
    
    # Rank configurations
    ranking = configuration_ranking(comparison)
    
    # Get rationales
    rationales = elimination_rationale(results)
    
    # Determine recommendation
    if results['hybrid_vtol']['feasible']:
        recommendation = 'hybrid_vtol'
    elif results['rotorcraft']['feasible'] and results['rotorcraft']['margin_percent'] >= 20:
        recommendation = 'rotorcraft'
    else:
        recommendation = None
    
    return {
        'mtow_kg': mtow_kg,
        'results': results,
        'comparison': comparison,
        'ranking': ranking,
        'rationales': rationales,
        'recommendation': recommendation,
    }


def print_comparative_analysis(summary: Dict[str, Any] = None) -> None:
    """Print formatted comparative analysis."""
    if summary is None:
        summary = comparative_summary()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPARATIVE CONFIGURATION ANALYSIS")
    print("From: Manuscript Section 5.5 (Comparative Results)")
    print(f"Values computed: {timestamp}")
    print("=" * 80)
    print()
    
    print(f"Analysis parameters:")
    print(f"  MTOW: {summary['mtow_kg']:.1f} kg")
    print(f"  Mars gravity: {G_MARS:.3f} m/s²")
    print()
    
    comp = summary['comparison']
    
    print("CONFIGURATION COMPARISON TABLE (@tbl:configuration-comparison)")
    print("=" * 80)
    print(f"{'Parameter':<25} {'Rotorcraft':>15} {'Fixed-Wing':>15} {'Hybrid VTOL':>15}")
    print("-" * 80)
    print(f"{'L/D (effective)':<25} {comp['ld_effective']['rotorcraft']:>15.1f} {comp['ld_effective']['fixed_wing']:>15.1f} {comp['ld_effective']['hybrid_vtol']:>15.1f}")
    print(f"{'Hover power (W)':<25} {comp['hover_power_w']['rotorcraft']:>15.0f} {'N/A':>15} {comp['hover_power_w']['hybrid_vtol']:>15.0f}")
    print(f"{'Cruise power (W)':<25} {comp['cruise_power_w']['rotorcraft']:>15.0f} {comp['cruise_power_w']['fixed_wing']:>15.0f} {comp['cruise_power_w']['hybrid_vtol']:>15.0f}")
    print(f"{'Endurance (min)':<25} {comp['endurance_min']['rotorcraft']:>15.0f} {comp['endurance_min']['fixed_wing']:>15.0f} {comp['endurance_min']['hybrid_vtol']:>15.0f}")
    print(f"{'Range (km)':<25} {comp['range_km']['rotorcraft']:>15.0f} {comp['range_km']['fixed_wing']:>15.0f} {comp['range_km']['hybrid_vtol']:>15.0f}")
    print(f"{'Endurance margin (%)':<25} {comp['endurance_margin_percent']['rotorcraft']:>15.0f} {comp['endurance_margin_percent']['fixed_wing']:>15.0f} {comp['endurance_margin_percent']['hybrid_vtol']:>15.0f}")
    print(f"{'VTOL capable':<25} {'Yes':>15} {'No':>15} {'Yes':>15}")
    print(f"{'Feasible':<25} {'Yes' if comp['feasible']['rotorcraft'] else 'No':>15} {'No':>15} {'Yes' if comp['feasible']['hybrid_vtol'] else 'No':>15}")
    print("-" * 80)
    print()
    
    print("ELIMINATION ANALYSIS")
    print("-" * 40)
    for config in ['rotorcraft', 'fixed_wing', 'hybrid_vtol']:
        name = config.replace('_', ' ').title()
        print(f"\n{name}:")
        print(f"  {summary['rationales'][config]}")
    print()
    
    print("RANKING (by overall capability)")
    print("-" * 40)
    for i, config in enumerate(summary['ranking'], 1):
        name = config.replace('_', ' ').title()
        print(f"  {i}. {name}")
    print()
    
    print("RECOMMENDATION")
    print("-" * 40)
    if summary['recommendation']:
        rec_name = summary['recommendation'].replace('_', ' ').upper()
        hv = summary['results']['hybrid_vtol']
        print(f"  SELECTED CONFIGURATION: {rec_name}")
        print(f"  - Energy margin: {hv['energy_margin_percent']:.0f}%")
        print(f"  - Endurance margin: {hv['endurance_margin_percent']:.0f}%")
        print(f"  - Achievable range: {hv['range_km']:.0f} km")
        print(f"  - VTOL capable: Yes")
    else:
        print("  No configuration meets all requirements with adequate margins.")
    
    print("=" * 80)
    print()
    print(">>> These COMPUTED values will be used to UPDATE the manuscript in Phase C.")


if __name__ == "__main__":
    # Run comparative analysis
    summary = comparative_summary()
    print_comparative_analysis(summary)
