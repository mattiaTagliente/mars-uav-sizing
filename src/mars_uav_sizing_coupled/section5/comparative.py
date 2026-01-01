"""
Comparative Analysis (Coupled)
==============================

Compares all three configurations using coupled sizing outputs.
"""

from typing import Dict, Any, List
from datetime import datetime

from . import rotorcraft
from . import fixed_wing
from . import hybrid_vtol


def run_all_analyses() -> Dict[str, Dict[str, Any]]:
    return {
        "rotorcraft": rotorcraft.rotorcraft_feasibility_analysis(),
        "fixed_wing": fixed_wing.fixed_wing_feasibility_analysis(),
        "hybrid_vtol": hybrid_vtol.hybrid_vtol_feasibility_analysis(),
    }


def create_comparison_table(results: Dict[str, Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    if results is None:
        results = run_all_analyses()

    rot = results["rotorcraft"]
    fw = results["fixed_wing"]
    hyb = results["hybrid_vtol"]

    return {
        "VTOL Capability": {
            "Rotorcraft": ("Yes", True),
            "Fixed-Wing": ("No", False),
            "Hybrid VTOL": ("Yes", True),
        },
        "Endurance (min)": {
            "Rotorcraft": (f"{rot['endurance_min']:.0f}", rot["feasible"]),
            "Fixed-Wing": (f"{fw['endurance_min']:.0f}", fw["endurance_passes"]),
            "Hybrid VTOL": (f"{hyb['endurance_min']:.0f}", hyb["endurance_passes"]),
        },
        "Range (km)": {
            "Rotorcraft": (f"{rot['range_km']:.0f}", rot["range_km"] >= 100),
            "Fixed-Wing": (f"{fw['range_km']:.0f}", fw["range_km"] >= 100),
            "Hybrid VTOL": (f"{hyb['range_km']:.0f}", hyb["range_km"] >= 100),
        },
        "Cruise Power (W)": {
            "Rotorcraft": (f"{rot['cruise_power_w']:.0f}", None),
            "Fixed-Wing": (f"{fw['cruise_power_w']:.0f}", None),
            "Hybrid VTOL": (f"{hyb['cruise_power_w']:.0f}", None),
        },
        "Hover Power (W)": {
            "Rotorcraft": (f"{rot['hover_power_w']:.0f}", None),
            "Fixed-Wing": ("N/A", None),
            "Hybrid VTOL": (f"{hyb['hover_power_w']:.0f}", None),
        },
        "L/D Cruise": {
            "Rotorcraft": (f"{rot['ld_effective']:.1f}", None),
            "Fixed-Wing": (f"{fw['ld_max']:.1f}", None),
            "Hybrid VTOL": (f"{hyb['ld_quadplane']:.1f}", None),
        },
        "Overall Feasible": {
            "Rotorcraft": ("No" if not rot["feasible"] else "Marginal", rot["feasible"]),
            "Fixed-Wing": ("No", False),
            "Hybrid VTOL": ("Yes", hyb["feasible"]),
        },
    }


def configuration_ranking(results: Dict[str, Dict[str, Any]] = None) -> List[str]:
    if results is None:
        results = run_all_analyses()

    scores = {}
    for name, res in results.items():
        score = 0

        if name != "fixed_wing":
            score += 100

        if "endurance_min" in res:
            score += res["endurance_min"]

        if "range_km" in res:
            score += res["range_km"] / 10

        if "margin_percent" in res and res["margin_percent"] > 0:
            score += res["margin_percent"]

        scores[name] = score

    ranked = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    return ranked


def elimination_rationale(results: Dict[str, Dict[str, Any]] = None) -> Dict[str, str]:
    if results is None:
        results = run_all_analyses()

    rot = results["rotorcraft"]
    fw = results["fixed_wing"]
    hyb = results["hybrid_vtol"]

    rationale = {}

    if rot["feasible"] and rot["margin_percent"] >= 10:
        rationale["rotorcraft"] = f"VIABLE: Meets requirements with {rot['margin_percent']:.0f}% margin."
    elif rot["feasible"]:
        rationale["rotorcraft"] = (
            f"ELIMINATED: Marginally meets endurance ({rot['endurance_min']:.0f} min) with only "
            f"{rot['margin_percent']:.0f}% margin. Insufficient for mission with no abort capability."
        )
    else:
        rationale["rotorcraft"] = (
            f"ELIMINATED: Fails endurance requirement ({rot['endurance_min']:.0f} min vs 60 min). "
            f"Low equivalent L/D ({rot['ld_effective']:.1f}) limits forward flight efficiency."
        )

    rationale["fixed_wing"] = (
        "ELIMINATED: Cannot satisfy VTOL requirement. Despite excellent endurance "
        f"({fw['endurance_min']:.0f} min, +{(fw['endurance_min']/fw['requirement_min']-1)*100:.0f}% margin), "
        f"ground roll of {fw['takeoff_distance_m']:.0f} m requires runway infrastructure."
    )

    if hyb["feasible"]:
        margin = (hyb["endurance_min"] / hyb["requirement_min"] - 1) * 100
        rationale["hybrid_vtol"] = (
            "SELECTED: Satisfies all requirements. VTOL capability with "
            f"{hyb['endurance_min']:.0f} min endurance ({margin:.0f}% margin). "
            "Combines rotorcraft VTOL with fixed-wing cruise efficiency."
        )
    else:
        rationale["hybrid_vtol"] = (
            "ELIMINATED: Fails to meet requirements despite hybrid architecture. "
            f"Endurance: {hyb['endurance_min']:.0f} min."
        )

    return rationale


def comparative_summary() -> Dict[str, Any]:
    results = run_all_analyses()
    comparison = create_comparison_table(results)
    ranking = configuration_ranking(results)
    rationale = elimination_rationale(results)

    return {
        "results": results,
        "comparison": comparison,
        "ranking": ranking,
        "rationale": rationale,
        "selected": ranking[0],
    }


def print_analysis(summary: Dict[str, Any] = None) -> None:
    if summary is None:
        summary = comparative_summary()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("COMPARATIVE CONFIGURATION ANALYSIS (COUPLED)")
    print("=" * 80)
    print(f"Computed: {timestamp}")
    print("Config:   All values loaded from config/ YAML files")
    print()

    print("CONFIGURATION COMPARISON TABLE")
    print("-" * 80)
    print(f"{'Metric':<25} {'Rotorcraft':>15} {'Fixed-Wing':>15} {'Hybrid VTOL':>15}")
    print("-" * 80)

    for metric, values in summary["comparison"].items():
        rot_val, rot_ok = values["Rotorcraft"]
        fw_val, fw_ok = values["Fixed-Wing"]
        hyb_val, hyb_ok = values["Hybrid VTOL"]

        rot_str = f"{rot_val}" + (" [+]" if rot_ok else " [-]" if rot_ok is False else "")
        fw_str = f"{fw_val}" + (" [+]" if fw_ok else " [-]" if fw_ok is False else "")
        hyb_str = f"{hyb_val}" + (" [+]" if hyb_ok else " [-]" if hyb_ok is False else "")

        print(f"{metric:<25} {rot_str:>15} {fw_str:>15} {hyb_str:>15}")

    print("-" * 80)
    print()

    print("CONFIGURATION RANKING")
    print("-" * 50)
    for i, config in enumerate(summary["ranking"], 1):
        print(f"  {i}. {config.replace('_', ' ').title()}")
    print()

    print("ELIMINATION RATIONALE")
    print("-" * 80)
    for config, reason in summary["rationale"].items():
        print(f"\n{config.replace('_', ' ').upper()}:" )
        print(f"  {reason}")
    print()

    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    selected = summary["selected"]
    print(f"Selected configuration: {selected.replace('_', ' ').upper()}")
    print()
    print(summary["rationale"][selected])
    print("=" * 80)


if __name__ == "__main__":
    print_analysis()
