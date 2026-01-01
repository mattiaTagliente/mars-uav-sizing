"""
Wrapper for mars_uav_sizing.section3.atmospheric_model.
"""

from mars_uav_sizing.section3.atmospheric_model import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    runpy.run_module("mars_uav_sizing.section3.atmospheric_model", run_name="__main__")
