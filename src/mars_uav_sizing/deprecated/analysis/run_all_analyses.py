"""
Mars UAV Sizing - Phase B Main Runner
=====================================

Runs all analysis modules and generates comprehensive output.
This is the main entry point for Phase B: Python Implementation.

Reference: docs/prompt_04_python_implementation.txt

Usage:
    python -m mars_uav_sizing.analysis.run_all_analyses
"""

from datetime import datetime

from .rotorcraft_analysis import rotorcraft_feasibility_analysis, print_rotorcraft_analysis
from .fixed_wing_analysis import fixed_wing_feasibility_analysis, print_fixed_wing_analysis
from .hybrid_vtol_analysis import hybrid_vtol_feasibility, print_hybrid_vtol_analysis
from .comparative_analysis import comparative_summary, print_comparative_analysis
from .matching_chart import matching_chart_analysis, print_matching_chart_analysis


def run_all_analyses(mtow_kg: float = 10.0):
    """Run all Phase B analyses with consistent parameters.
    
    Parameters
    ----------
    mtow_kg : float
        Baseline MTOW for all analyses
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("MARS UAV SIZING - PHASE B: PYTHON IMPLEMENTATION")
    print("=" * 80)
    print(f"Run started: {timestamp}")
    print(f"MTOW baseline: {mtow_kg} kg")
    print()
    print("This script runs all analysis modules from manuscript Sections 5.2-5.5")
    print("and generates values that will update the manuscript in Phase C.")
    print("=" * 80)
    print()
    
    # 1. Rotorcraft Analysis (Section 5.2)
    print("\n" + "=" * 80)
    print("SECTION 5.2: ROTORCRAFT CONFIGURATION")
    print("=" * 80)
    rc_results = rotorcraft_feasibility_analysis(mtow_kg=mtow_kg)
    print_rotorcraft_analysis(rc_results)
    
    # 2. Fixed-Wing Analysis (Section 5.3)
    print("\n" + "=" * 80)
    print("SECTION 5.3: FIXED-WING CONFIGURATION")
    print("=" * 80)
    fw_results = fixed_wing_feasibility_analysis(mtow_kg=mtow_kg)
    print_fixed_wing_analysis(fw_results)
    
    # 3. Hybrid VTOL Analysis (Section 5.4)
    print("\n" + "=" * 80)
    print("SECTION 5.4: HYBRID VTOL (QUADPLANE) CONFIGURATION")
    print("=" * 80)
    hv_results = hybrid_vtol_feasibility(mtow_kg=mtow_kg)
    print_hybrid_vtol_analysis(hv_results)
    
    # 4. Matching Chart Analysis (Section 5.5)
    print("\n" + "=" * 80)
    print("SECTION 5.5: MATCHING CHART ANALYSIS")
    print("=" * 80)
    mc_results = matching_chart_analysis(mtow_kg=mtow_kg)
    print_matching_chart_analysis(mc_results)
    
    # 5. Comparative Analysis (Section 5.5)
    print("\n" + "=" * 80)
    print("SECTION 5.5: COMPARATIVE RESULTS")
    print("=" * 80)
    summary = comparative_summary(mtow_kg=mtow_kg)
    print_comparative_analysis(summary)
    
    # Final Summary
    print("\n" + "=" * 80)
    print("PHASE B EXECUTION COMPLETE")
    print("=" * 80)
    print()
    print("KEY COMPUTED VALUES FOR MANUSCRIPT UPDATE (Phase C):")
    print("-" * 60)
    print()
    print("From Rotorcraft Analysis (§5.2):")
    print(f"  Hover power: {rc_results['hover_power_w']:.0f} W")
    print(f"  Cruise power: {rc_results['cruise_power_w']:.0f} W")
    print(f"  Induced velocity: {rc_results['induced_velocity_m_s']:.1f} m/s")
    print(f"  Endurance: {rc_results['endurance_min']:.0f} min (FAILS: {rc_results['margin_percent']:.0f}% margin)")
    print()
    print("From Fixed-Wing Analysis (§5.3):")
    print(f"  (L/D)_max: {fw_results['ld_max']:.1f}")
    print(f"  C_L*: {fw_results['cl_optimal']:.2f}")
    print(f"  Cruise power: {fw_results['cruise_power_w']:.0f} W")
    print(f"  Endurance: {fw_results['endurance_with_reserve_min']:.0f} min")
    print(f"  Takeoff roll: {fw_results['takeoff_roll_m']:.0f} m (FAILS VTOL)")
    print()
    print("From Hybrid VTOL Analysis (§5.4):")
    print(f"  Hover power: {hv_results['hover_power_w']:.0f} W")
    print(f"  Cruise power: {hv_results['cruise_power_w']:.0f} W")
    print(f"  QuadPlane L/D: {hv_results['ld_quadplane']:.1f}")
    print(f"  Energy margin: {hv_results['energy_margin_percent']:.0f}%")
    print(f"  Endurance: {hv_results['endurance_min']:.0f} min ({hv_results['endurance_margin_percent']:.0f}% margin)")
    print(f"  Range: {hv_results['range_km']:.0f} km")
    print(f"  RECOMMENDATION: HYBRID VTOL SELECTED")
    print()
    print("From Matching Chart (§5.5):")
    print(f"  Design W/S: {mc_results['design_ws']:.1f} N/m² (at stall limit)")
    print(f"  Design P/W: {mc_results['design_pw']:.1f} W/N (hover dominates)")
    print(f"  Wing area: {mc_results['wing_area_m2']:.1f} m²")
    print(f"  Wingspan: {mc_results['wingspan_m']:.1f} m")
    print(f"  Installed power: {mc_results['installed_power_w']:.0f} W")
    print()
    print("=" * 80)
    print(">>> Use these values to update manuscript in Phase C.")
    print("=" * 80)
    
    return {
        'rotorcraft': rc_results,
        'fixed_wing': fw_results,
        'hybrid_vtol': hv_results,
        'matching_chart': mc_results,
        'summary': summary,
    }


if __name__ == "__main__":
    run_all_analyses()
