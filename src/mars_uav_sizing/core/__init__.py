"""
Core Module
===========

Core utilities and shared functionality for Mars UAV sizing.

Components:
    - config_loader: Configuration loading (re-export from config/)
    - atmosphere: Mars atmospheric model
    - energy: Shared energy accounting helper
    - utils: Common utility functions
"""

# Re-export config loading for convenience
from ..config import load_config, get_param

from . import atmosphere
from . import energy
from . import utils

__all__ = [
    'load_config',
    'get_param',
    'atmosphere',
    'energy',
    'utils',
]
