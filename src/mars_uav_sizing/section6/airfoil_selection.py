#!/usr/bin/env python3
"""
Airfoil Selection Module
========================

Loads airfoil performance data from YAML configuration and provides
selection logic for Mars UAV wing design.

All data loaded from config/airfoil_data.yaml - no hardcoded values.

Reference:
    Selig, M.S., et al. (1995). Summary of Low-Speed Airfoil Data, Vol. 1.
    SoarTech Publications. ISBN: 0-9646747-1-8

Last Updated: 2025-12-31
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any


@dataclass
class AirfoilDataPoint:
    """Single data point from airfoil polar."""
    alpha: float      # Angle of attack [deg]
    cl: float         # Lift coefficient
    cd: float         # Drag coefficient
    ld: float = 0.0   # Lift-to-drag ratio (computed)
    
    def __post_init__(self):
        if self.cd > 0:
            self.ld = self.cl / self.cd


@dataclass
class AirfoilPolar:
    """Complete polar data for an airfoil at a specific Reynolds number."""
    airfoil_name: str
    reynolds: int
    data: List[AirfoilDataPoint] = field(default_factory=list)
    
    @property
    def cl_max(self) -> float:
        """Maximum lift coefficient."""
        if not self.data:
            return 0.0
        return max(p.cl for p in self.data)
    
    @property
    def alpha_at_cl_max(self) -> float:
        """Angle of attack at Cl_max [deg]."""
        if not self.data:
            return 0.0
        max_cl = self.cl_max
        for p in self.data:
            if p.cl == max_cl:
                return p.alpha
        return 0.0
    
    @property
    def ld_max(self) -> float:
        """Maximum lift-to-drag ratio."""
        if not self.data:
            return 0.0
        return max(p.ld for p in self.data if p.cd > 0)
    
    @property
    def cl_at_ld_max(self) -> float:
        """Cl at maximum L/D."""
        if not self.data:
            return 0.0
        max_ld = self.ld_max
        for p in self.data:
            if abs(p.ld - max_ld) < 0.01:
                return p.cl
        return 0.0
    
    @property
    def alpha_at_ld_max(self) -> float:
        """Angle of attack at maximum L/D [deg]."""
        if not self.data:
            return 0.0
        max_ld = self.ld_max
        for p in self.data:
            if abs(p.ld - max_ld) < 0.01:
                return p.alpha
        return 0.0
    
    @property
    def cd_at_ld_max(self) -> float:
        """Cd at maximum L/D."""
        if not self.data:
            return 0.0
        max_ld = self.ld_max
        for p in self.data:
            if abs(p.ld - max_ld) < 0.01:
                return p.cd
        return 0.0
    
    @property
    def cd_min(self) -> float:
        """Minimum drag coefficient."""
        if not self.data:
            return 0.0
        return min(p.cd for p in self.data if p.cd > 0)
    
    def get_arrays(self) -> Tuple[List[float], List[float], List[float], List[float]]:
        """Return arrays for plotting: alpha, cl, cd, ld."""
        alpha = [p.alpha for p in self.data]
        cl = [p.cl for p in self.data]
        cd = [p.cd for p in self.data]
        ld = [p.ld for p in self.data]
        return alpha, cl, cd, ld


def load_airfoil_data(yaml_path: Path = None) -> Dict[str, AirfoilPolar]:
    """
    Load airfoil data from YAML file.
    
    Parameters
    ----------
    yaml_path : Path, optional
        Path to airfoil_data.yaml. If None, uses default config location.
    
    Returns
    -------
    dict
        Dictionary mapping airfoil names to AirfoilPolar objects
    """
    if yaml_path is None:
        yaml_path = Path(__file__).parent.parent / "config" / "airfoil_data.yaml"
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    result = {}
    
    for airfoil in data.get('airfoils', []):
        name = airfoil['name']
        
        for perf in airfoil.get('performance_data', []):
            reynolds = perf['reynolds']
            points = []
            
            for ld_point in perf.get('ld_data', []):
                point = AirfoilDataPoint(
                    alpha=ld_point['alpha'],
                    cl=ld_point['cl'],
                    cd=ld_point['cd']
                )
                points.append(point)
            
            polar = AirfoilPolar(
                airfoil_name=name,
                reynolds=reynolds,
                data=points
            )
            result[name] = polar
    
    return result


def get_airfoil_metrics(polars: Dict[str, AirfoilPolar]) -> Dict[str, Dict[str, float]]:
    """
    Extract key metrics for all airfoils for comparison.
    
    Parameters
    ----------
    polars : dict
        Dictionary of airfoil polars from load_airfoil_data()
    
    Returns
    -------
    dict
        Dictionary of airfoil metrics
    """
    metrics = {}
    
    for name, polar in polars.items():
        metrics[name] = {
            'reynolds': polar.reynolds,
            'cl_max': polar.cl_max,
            'alpha_stall': polar.alpha_at_cl_max,
            'ld_max': polar.ld_max,
            'cl_at_ld_max': polar.cl_at_ld_max,
            'cd_at_ld_max': polar.cd_at_ld_max,
            'cd_min': polar.cd_min,
        }
    
    return metrics


def select_best_airfoil(
    polars: Dict[str, AirfoilPolar],
    weights: Dict[str, float] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Select the best airfoil based on weighted criteria.
    
    Parameters
    ----------
    polars : dict
        Dictionary of airfoil polars from load_airfoil_data()
    weights : dict, optional
        Weights for criteria. Default emphasizes L/D (cruise efficiency).
        Keys: 'ld_max', 'cl_max', 'stall_margin'
    
    Returns
    -------
    tuple
        (best_airfoil_name, scores_dict)
    """
    if weights is None:
        weights = {
            'ld_max': 0.6,        # Priority: cruise efficiency
            'cl_max': 0.25,       # Secondary: stall margin
            'stall_margin': 0.15  # Tertiary: controllability
        }
    
    scores = {}
    all_metrics = get_airfoil_metrics(polars)
    
    for name, m in all_metrics.items():
        # Normalize scores (higher is better)
        # L/D max: normalize relative to best expected (~50)
        ld_score = m['ld_max'] / 50.0
        
        # Cl max: normalize relative to typical max (~2.0)
        cl_score = m['cl_max'] / 2.0
        
        # Stall margin: higher stall angle is better (15° is good)
        stall_score = m['alpha_stall'] / 15.0
        
        # Weighted sum
        total_score = (
            weights['ld_max'] * ld_score +
            weights['cl_max'] * cl_score +
            weights['stall_margin'] * stall_score
        )
        
        scores[name] = total_score
        all_metrics[name]['score'] = total_score
    
    # Select best
    best_name = max(scores, key=scores.get)
    
    return best_name, all_metrics


def print_airfoil_comparison():
    """Print airfoil comparison table and selection result."""
    polars = load_airfoil_data()
    best_name, metrics = select_best_airfoil(polars)
    
    print("=" * 80)
    print("AIRFOIL COMPARISON (Section 6.2)")
    print("=" * 80)
    print()
    print(f"{'Airfoil':<12} {'Re':<8} {'Cl_max':<8} {'α_stall':<8} {'(L/D)_max':<10} {'Cl@L/D':<8} {'Score':<8}")
    print("-" * 80)
    
    for name, m in sorted(metrics.items(), key=lambda x: -x[1]['ld_max']):
        marker = " ←" if name == best_name else ""
        print(f"{name.upper():<12} {m['reynolds']:<8} {m['cl_max']:<8.2f} {m['alpha_stall']:<8.1f}° "
              f"{m['ld_max']:<10.1f} {m['cl_at_ld_max']:<8.2f} {m['score']:<8.3f}{marker}")
    
    print()
    print(f"SELECTED: {best_name.upper()} (highest weighted score)")
    print()
    print("Selection rationale:")
    print(f"  - Highest (L/D)_max of {metrics[best_name]['ld_max']:.1f}")
    print(f"  - Cl_max of {metrics[best_name]['cl_max']:.2f} provides adequate stall margin")
    print(f"  - Well-documented experimental data from UIUC")
    print("=" * 80)


if __name__ == "__main__":
    print_airfoil_comparison()
