"""
Configuration Module (Coupled Solver)
====================================

Extends the base mars_uav_sizing configuration with solver parameters.
Base parameters are loaded from mars_uav_sizing.config; solver options
are loaded from this package's config/solver_parameters.yaml.
"""

from pathlib import Path
from typing import Any, Dict
import yaml

from mars_uav_sizing import config as base_config

CONFIG_DIR = Path(__file__).parent
SOLVER_FILE = "solver_parameters.yaml"

_config_cache: Dict[str, Any] = {}


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_config(reload: bool = False) -> Dict[str, Any]:
    global _config_cache
    if _config_cache and not reload:
        return _config_cache

    base = base_config.load_config(reload=reload)
    solver_blob = _load_yaml(CONFIG_DIR / SOLVER_FILE)

    _config_cache = dict(base)
    _config_cache["solver"] = solver_blob.get("solver", {})
    return _config_cache


def get_param(path: str, default: Any = None) -> Any:
    config = load_config()
    keys = path.split(".")
    value: Any = config
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        if default is not None:
            return default
        raise KeyError(f"Configuration path not found: {path}")


# Base convenience functions (pass-through)

def get_mars_gravity() -> float:
    return base_config.get_mars_gravity()


def get_density() -> float:
    return base_config.get_density()


def get_mtow() -> float:
    return base_config.get_mtow()


def get_propulsion_efficiencies() -> Dict[str, float]:
    return base_config.get_propulsion_efficiencies()


def get_battery_params() -> Dict[str, float]:
    return base_config.get_battery_params()


def get_aerodynamic_params() -> Dict[str, float]:
    return base_config.get_aerodynamic_params()


def get_mission_params() -> Dict[str, float]:
    return base_config.get_mission_params()


def get_geometry_params() -> Dict[str, float]:
    return base_config.get_geometry_params()


def get_solver_params() -> Dict[str, Any]:
    return get_param("solver", default={})


def get_solver_options() -> Dict[str, Any]:
    return get_param("solver.options", default={})


def get_initial_guess() -> Dict[str, Any]:
    return get_param("solver.initial_guess", default={})


def print_config_summary() -> None:
    base_config.print_config_summary()
    solver = get_solver_params()
    if solver:
        print("\n[SOLVER PARAMETERS]")
        for key, value in solver.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    print_config_summary()
