"""
Wrapper for mars_uav_sizing.core.atmosphere.
"""

from mars_uav_sizing.core.atmosphere import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    runpy.run_module("mars_uav_sizing.core.atmosphere", run_name="__main__")
