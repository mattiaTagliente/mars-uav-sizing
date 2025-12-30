"""
Mars UAV Sizing Tool
=====================

A comprehensive toolkit for preliminary sizing of UAVs designed for Mars 
atmospheric flight. Implements the analysis from manuscript Sections 3-5.

Package Structure:
    - config/       : YAML configuration loading (all parameters)
    - core/         : Core utilities (atmosphere, utils)
    - section3/     : Mission Analysis (§3)
    - section4/     : Reference Data (§4)
    - section5/     : Constraint Analysis (§5)
    - visualization/: Plotting functions
    - verification/ : Manuscript verification

Usage:
    # Run full analysis
    python -m mars_uav_sizing.run_analysis
    
    # Access configuration
    from mars_uav_sizing.config import get_param
    g_mars = get_param('physical.mars.g')
    
    # Run individual analyses
    from mars_uav_sizing.section5 import rotorcraft
    results = rotorcraft.rotorcraft_feasibility_analysis()

Last Updated: 2025-12-29
"""

__version__ = "0.2.0"

# Configuration
from .config import load_config, get_param

# Import modules
from . import config
from . import core
from . import section3
from . import section4
from . import section5
from . import visualization
from . import verification

__all__ = [
    # Version
    "__version__",
    # Configuration
    "load_config",
    "get_param",
    # Modules
    "config",
    "core",
    "section3",
    "section4",
    "section5",
    "visualization",
    "verification",
]
