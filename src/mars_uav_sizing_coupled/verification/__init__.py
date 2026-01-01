"""
Wrapper for mars_uav_sizing.verification.
"""

from mars_uav_sizing.verification import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    runpy.run_module("mars_uav_sizing.verification", run_name="__main__")
