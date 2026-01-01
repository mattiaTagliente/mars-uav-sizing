"""
Wrapper for mars_uav_sizing.core.
"""

from mars_uav_sizing.core import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    runpy.run_module("mars_uav_sizing.core", run_name="__main__")
