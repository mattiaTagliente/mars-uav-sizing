"""
Mars UAV Sizing Tool (Coupled Solver)
===================================

Parallel package that preserves the original structure while adding a
coupled, solver-based sizing workflow (matching chart initial guess + fsolve).
"""

__version__ = "0.1.0"

from .config import load_config, get_param

from . import config
from . import core
from . import section3
from . import section4
from . import section5
from . import visualization
from . import verification

__all__ = [
    "__version__",
    "load_config",
    "get_param",
    "config",
    "core",
    "section3",
    "section4",
    "section5",
    "visualization",
    "verification",
]
