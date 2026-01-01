"""
Wrapper for mars_uav_sizing.verification.verify_manuscript.
"""

from mars_uav_sizing.verification.verify_manuscript import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    runpy.run_module("mars_uav_sizing.verification.verify_manuscript", run_name="__main__")
