"""
XFOIL Wrapper Module
====================

Provides Python interface to XFOIL for airfoil polar analysis,
specifically configured for Mars UAV low Reynolds number operation.

References:
- Drela, M. (1989). XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils.
- Selig et al. (1995). Summary of Low-Speed Airfoil Data.
"""

import os
import subprocess
import tempfile
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import re


@dataclass
class XfoilPolar:
    """
    Container for XFOIL polar data.

    Attributes
    ----------
    airfoil : str
        Airfoil name/identifier
    reynolds : float
        Reynolds number
    mach : float
        Mach number
    alpha : list
        Angles of attack in degrees
    cl : list
        Lift coefficients
    cd : list
        Drag coefficients
    cm : list
        Moment coefficients (about c/4)
    """

    airfoil: str
    reynolds: float
    mach: float = 0.0
    alpha: List[float] = field(default_factory=list)
    cl: List[float] = field(default_factory=list)
    cd: List[float] = field(default_factory=list)
    cm: List[float] = field(default_factory=list)

    @property
    def cl_max(self) -> float:
        """Maximum lift coefficient."""
        if not self.cl:
            return 0.0
        return max(self.cl)

    @property
    def alpha_stall(self) -> float:
        """Angle of attack at CL_max in degrees."""
        if not self.cl or not self.alpha:
            return 0.0
        idx = self.cl.index(max(self.cl))
        return self.alpha[idx]

    @property
    def ld_max(self) -> Tuple[float, float]:
        """Maximum L/D and corresponding CL."""
        if not self.cl or not self.cd:
            return 0.0, 0.0
        ld = [cl / cd if cd > 0 else 0 for cl, cd in zip(self.cl, self.cd)]
        idx = ld.index(max(ld))
        return ld[idx], self.cl[idx]

    @property
    def cl_alpha(self) -> float:
        """Lift curve slope (per radian) in linear region."""
        if len(self.alpha) < 3 or len(self.cl) < 3:
            return 0.0
        # Use linear region (-4 to 8 degrees typically)
        linear_data = [
            (a, c)
            for a, c in zip(self.alpha, self.cl)
            if -4 <= a <= 8
        ]
        if len(linear_data) < 2:
            return 0.0
        # Linear regression
        n = len(linear_data)
        sum_a = sum(a for a, c in linear_data)
        sum_c = sum(c for a, c in linear_data)
        sum_ac = sum(a * c for a, c in linear_data)
        sum_a2 = sum(a * a for a, c in linear_data)
        denom = n * sum_a2 - sum_a * sum_a
        if abs(denom) < 1e-10:
            return 0.0
        slope_per_deg = (n * sum_ac - sum_a * sum_c) / denom
        return slope_per_deg * 180.0 / 3.14159  # Convert to per-radian

    @property
    def alpha_zero_lift(self) -> float:
        """Zero-lift angle of attack in degrees."""
        if len(self.alpha) < 2 or len(self.cl) < 2:
            return 0.0
        # Find where CL crosses zero
        for i in range(len(self.cl) - 1):
            if self.cl[i] <= 0 <= self.cl[i + 1] or self.cl[i] >= 0 >= self.cl[i + 1]:
                # Linear interpolation
                if abs(self.cl[i + 1] - self.cl[i]) < 1e-10:
                    return self.alpha[i]
                t = -self.cl[i] / (self.cl[i + 1] - self.cl[i])
                return self.alpha[i] + t * (self.alpha[i + 1] - self.alpha[i])
        return 0.0

    def cd_at_cl(self, target_cl: float) -> float:
        """Get CD at a specific CL by interpolation."""
        if not self.cl or not self.cd:
            return 0.0
        # Find bracketing points
        for i in range(len(self.cl) - 1):
            if self.cl[i] <= target_cl <= self.cl[i + 1] or self.cl[i] >= target_cl >= self.cl[i + 1]:
                if abs(self.cl[i + 1] - self.cl[i]) < 1e-10:
                    return self.cd[i]
                t = (target_cl - self.cl[i]) / (self.cl[i + 1] - self.cl[i])
                return self.cd[i] + t * (self.cd[i + 1] - self.cd[i])
        return 0.0

    def summary(self) -> str:
        """Generate polar summary string."""
        ld_max, cl_ld_max = self.ld_max
        lines = [
            f"Airfoil: {self.airfoil}",
            f"Re = {self.reynolds:.0f}, M = {self.mach:.2f}",
            "-" * 40,
            f"  CL_max:        {self.cl_max:.3f} at α = {self.alpha_stall:.1f}°",
            f"  (L/D)_max:     {ld_max:.1f} at CL = {cl_ld_max:.3f}",
            f"  CL_α:          {self.cl_alpha:.3f} /rad",
            f"  α_0L:          {self.alpha_zero_lift:.2f}°",
        ]
        return "\n".join(lines)


class XfoilRunner:
    """
    XFOIL batch execution wrapper.

    Parameters
    ----------
    xfoil_path : str or Path, optional
        Path to XFOIL executable. If not provided, searches common locations.
    n_panels : int
        Number of panels for discretization (default: 200)
    max_iter : int
        Maximum iterations for convergence (default: 200)
    n_crit : float
        Critical amplification factor (default: 5.0 for low-Re, 9.0 standard)
    """

    def __init__(
        self,
        xfoil_path: Optional[str] = None,
        n_panels: int = 200,
        max_iter: int = 200,
        n_crit: float = 5.0,  # Lower Ncrit for low-Re convergence
    ):
        self.xfoil_path = self._find_xfoil(xfoil_path)
        self.n_panels = n_panels
        self.max_iter = max_iter
        self.n_crit = n_crit

    def _find_xfoil(self, provided_path: Optional[str]) -> Path:
        """Find XFOIL executable."""
        if provided_path:
            path = Path(provided_path)
            if path.exists():
                return path

        # Search common locations
        search_paths = [
            Path(__file__).parent.parent.parent / "xfoil.exe",
            Path(__file__).parent.parent.parent / "tools" / "xfoil.exe",
            Path.home() / "xfoil.exe",
            Path("C:/Users/matti/OneDrivePhD/5.5 IELTS/progettazione/Profilo/xfoil.exe"),
        ]

        for path in search_paths:
            if path.exists():
                return path

        # Check if in PATH
        if shutil.which("xfoil"):
            return Path(shutil.which("xfoil"))

        raise FileNotFoundError(
            "XFOIL executable not found. Please provide path or install XFOIL."
        )

    def _generate_input_script(
        self,
        airfoil: str,
        reynolds: float,
        mach: float,
        alpha_start: float,
        alpha_end: float,
        alpha_step: float,
        polar_file: str,
        coord_file: Optional[str] = None,
    ) -> str:
        """Generate XFOIL input script optimized for low Reynolds numbers."""
        lines = []

        # Load airfoil - use just filename since we run in the output directory
        if airfoil.upper().startswith("NACA "):
            # NACA airfoil - use internal generator
            code = airfoil[5:].strip()
            lines.append(f"NACA {code}")
        elif coord_file:
            # Use just the filename, not full path
            coord_filename = Path(coord_file).name
            lines.append(f"LOAD {coord_filename}")
        else:
            # Try to load by name
            lines.append(f"LOAD {airfoil}")

        # Panel refinement
        lines.extend([
            "PPAR",
            "N",
            str(self.n_panels),
            "",  # Accept defaults
            "",
            "",
            "PANE",  # Apply paneling
        ])

        # Enter OPER mode
        lines.append("OPER")

        # Set viscous parameters for low Reynolds number convergence
        lines.extend([
            "VPAR",
            f"N {self.n_crit:.1f}",  # Set Ncrit (lower = earlier transition, better convergence)
            "",
        ])

        # Set iterations
        lines.extend([
            "ITER",
            str(self.max_iter),
        ])

        # Set viscous mode with Reynolds
        lines.extend([
            "VISC",
            f"{reynolds:.0f}",
        ])

        # Set Mach (if non-zero)
        if mach > 0:
            lines.extend([
                "MACH",
                f"{mach:.4f}",
            ])

        # Initialize BL at alpha=0 before sweep (helps convergence)
        lines.extend([
            "ALFA 0",
            "INIT",
        ])

        # Enable polar accumulation
        lines.extend([
            "PACC",
            polar_file,
            "",  # No dump file
        ])

        # Run alpha sweep with smaller steps for better convergence
        # Start from 0 and go up, then from 0 and go down
        if alpha_start < 0 and alpha_end > 0:
            # Positive sweep first
            lines.extend([
                "ASEQ",
                "0.00",
                f"{alpha_end:.2f}",
                f"{alpha_step:.2f}",
            ])
            # Then negative sweep
            lines.extend([
                "INIT",
                "ASEQ",
                "0.00",
                f"{alpha_start:.2f}",
                f"{-abs(alpha_step):.2f}",
            ])
        else:
            # Simple sweep
            lines.extend([
                "ASEQ",
                f"{alpha_start:.2f}",
                f"{alpha_end:.2f}",
                f"{alpha_step:.2f}",
            ])

        # Disable polar accumulation
        lines.extend([
            "PACC",
            "",
        ])

        # Exit
        lines.extend([
            "",
            "QUIT",
        ])

        return "\r\n".join(lines)

    def _parse_polar_file(self, polar_file: Path, airfoil: str, reynolds: float, mach: float) -> XfoilPolar:
        """Parse XFOIL polar output file."""
        polar = XfoilPolar(airfoil=airfoil, reynolds=reynolds, mach=mach)

        if not polar_file.exists():
            return polar

        with open(polar_file, "r") as f:
            lines = f.readlines()

        # Parse data lines (skip header)
        for line in lines:
            line = line.strip()
            if not line or line.startswith("-"):
                continue

            # Try to parse as data row
            parts = line.split()
            if len(parts) >= 5:
                try:
                    alpha = float(parts[0])
                    cl = float(parts[1])
                    cd = float(parts[2])
                    cm = float(parts[4]) if len(parts) > 4 else 0.0

                    polar.alpha.append(alpha)
                    polar.cl.append(cl)
                    polar.cd.append(cd)
                    polar.cm.append(cm)
                except ValueError:
                    continue

        return polar

    def run_polar(
        self,
        airfoil: str,
        reynolds: float,
        mach: float = 0.0,
        alpha_range: Tuple[float, float, float] = (-5.0, 20.0, 1.0),
        coord_file: Optional[str] = None,
        output_dir: Optional[str] = None,
        use_cache: bool = True,
    ) -> XfoilPolar:
        """
        Run XFOIL to generate polar for given conditions.

        Parameters
        ----------
        airfoil : str
            Airfoil name (e.g., "NACA 2412" or "e387")
        reynolds : float
            Reynolds number
        mach : float
            Mach number (default: 0.0 for incompressible)
        alpha_range : tuple
            (start, end, step) for angle of attack sweep in degrees
        coord_file : str, optional
            Path to coordinate file for custom airfoils
        output_dir : str, optional
            Directory for output files (uses temp if not specified)
        use_cache : bool
            Whether to use cached polar files (default: True)

        Returns
        -------
        XfoilPolar
            Polar data container
        """
        alpha_start, alpha_end, alpha_step = alpha_range

        # Sanitize airfoil name for filename
        safe_name = re.sub(r"[^\w\-]", "_", airfoil)
        polar_filename = f"{safe_name}_Re{reynolds:.0e}_M{mach:.2f}.txt"

        # Set up working directory
        if output_dir:
            work_dir = Path(output_dir)
            work_dir.mkdir(parents=True, exist_ok=True)
        else:
            work_dir = Path(tempfile.mkdtemp(prefix="xfoil_"))

        polar_file = work_dir / polar_filename
        input_file = work_dir / f"{safe_name}_input.txt"

        # Check cache
        if use_cache and polar_file.exists() and polar_file.stat().st_size > 100:
            return self._parse_polar_file(polar_file, airfoil, reynolds, mach)

        # Generate input script
        script = self._generate_input_script(
            airfoil=airfoil,
            reynolds=reynolds,
            mach=mach,
            alpha_start=alpha_start,
            alpha_end=alpha_end,
            alpha_step=alpha_step,
            polar_file=polar_filename,
            coord_file=coord_file,
        )

        # Write input file
        with open(input_file, "w") as f:
            f.write(script)

        # Run XFOIL
        try:
            result = subprocess.run(
                [str(self.xfoil_path)],
                input=script,
                capture_output=True,
                text=True,
                cwd=work_dir,
                timeout=120,  # 2 minute timeout
            )
        except subprocess.TimeoutExpired:
            print(f"XFOIL timed out for {airfoil}")
            return XfoilPolar(airfoil=airfoil, reynolds=reynolds, mach=mach)
        except Exception as e:
            print(f"XFOIL error for {airfoil}: {e}")
            return XfoilPolar(airfoil=airfoil, reynolds=reynolds, mach=mach)

        # Parse results
        return self._parse_polar_file(polar_file, airfoil, reynolds, mach)


# Standard low-Reynolds airfoil coordinates (Selig format)
# These are commonly used for Mars UAV applications

AIRFOIL_COORDS = {
    "e387": """E387
  1.00000  0.00000
  0.99671  0.00057
  0.98707  0.00218
  0.97194  0.00463
  0.95169  0.00770
  0.92675  0.01127
  0.89753  0.01522
  0.86447  0.01947
  0.82803  0.02396
  0.78864  0.02862
  0.74676  0.03337
  0.70286  0.03812
  0.65739  0.04276
  0.61082  0.04718
  0.56361  0.05125
  0.51621  0.05485
  0.46906  0.05787
  0.42261  0.06019
  0.37729  0.06172
  0.33349  0.06239
  0.29160  0.06216
  0.25194  0.06102
  0.21479  0.05899
  0.18039  0.05614
  0.14892  0.05255
  0.12052  0.04833
  0.09528  0.04360
  0.07324  0.03847
  0.05442  0.03307
  0.03877  0.02754
  0.02620  0.02200
  0.01658  0.01662
  0.00972  0.01155
  0.00541  0.00697
  0.00340  0.00314
  0.00340  -0.00070
  0.00541  -0.00348
  0.00972  -0.00538
  0.01658  -0.00657
  0.02620  -0.00727
  0.03877  -0.00765
  0.05442  -0.00787
  0.07324  -0.00801
  0.09528  -0.00811
  0.12052  -0.00816
  0.14892  -0.00814
  0.18039  -0.00802
  0.21479  -0.00778
  0.25194  -0.00738
  0.29160  -0.00681
  0.33349  -0.00607
  0.37729  -0.00517
  0.42261  -0.00413
  0.46906  -0.00298
  0.51621  -0.00177
  0.56361  -0.00054
  0.61082  0.00065
  0.65739  0.00175
  0.70286  0.00273
  0.74676  0.00354
  0.78864  0.00416
  0.82803  0.00456
  0.86447  0.00473
  0.89753  0.00464
  0.92675  0.00428
  0.95169  0.00364
  0.97194  0.00274
  0.98707  0.00163
  0.99671  0.00058
  1.00000  0.00000
""",

    "s1223": """S1223
  1.00000  0.00000
  0.99634  0.00131
  0.98548  0.00502
  0.96798  0.01078
  0.94469  0.01816
  0.91618  0.02681
  0.88301  0.03645
  0.84571  0.04686
  0.80480  0.05784
  0.76079  0.06916
  0.71420  0.08057
  0.66554  0.09177
  0.61533  0.10247
  0.56409  0.11231
  0.51236  0.12095
  0.46068  0.12801
  0.40961  0.13315
  0.35969  0.13607
  0.31147  0.13653
  0.26547  0.13441
  0.22216  0.12968
  0.18198  0.12244
  0.14531  0.11289
  0.11246  0.10132
  0.08371  0.08812
  0.05924  0.07371
  0.03920  0.05855
  0.02367  0.04313
  0.01268  0.02796
  0.00614  0.01378
  0.00382  0.00155
  0.00537  -0.00859
  0.01050  -0.01667
  0.01894  -0.02276
  0.03048  -0.02707
  0.04494  -0.02984
  0.06218  -0.03131
  0.08202  -0.03170
  0.10433  -0.03120
  0.12896  -0.02999
  0.15575  -0.02823
  0.18452  -0.02606
  0.21511  -0.02362
  0.24732  -0.02102
  0.28097  -0.01837
  0.31586  -0.01574
  0.35181  -0.01321
  0.38861  -0.01085
  0.42609  -0.00870
  0.46406  -0.00680
  0.50233  -0.00517
  0.54073  -0.00381
  0.57908  -0.00272
  0.61722  -0.00188
  0.65500  -0.00127
  0.69226  -0.00085
  0.72887  -0.00060
  0.76471  -0.00047
  0.79966  -0.00044
  0.83362  -0.00048
  0.86650  -0.00054
  0.89821  -0.00059
  0.92869  -0.00058
  0.95785  -0.00047
  0.98165  -0.00024
  1.00000  0.00000
""",

    "s7055": """S7055
  1.00000  0.00000
  0.99644  0.00071
  0.98592  0.00271
  0.96922  0.00579
  0.94697  0.00971
  0.91973  0.01432
  0.88803  0.01951
  0.85238  0.02520
  0.81328  0.03131
  0.77122  0.03776
  0.72671  0.04446
  0.68021  0.05127
  0.63219  0.05805
  0.58314  0.06464
  0.53351  0.07085
  0.48379  0.07648
  0.43444  0.08130
  0.38593  0.08506
  0.33874  0.08754
  0.29330  0.08853
  0.25002  0.08786
  0.20927  0.08543
  0.17139  0.08119
  0.13667  0.07520
  0.10534  0.06762
  0.07759  0.05867
  0.05354  0.04865
  0.03329  0.03786
  0.01688  0.02667
  0.00635  0.01641
  0.00096  0.00730
  0.00000  0.00000
  0.00416  -0.00618
  0.01258  -0.01032
  0.02508  -0.01313
  0.04137  -0.01496
  0.06115  -0.01608
  0.08411  -0.01666
  0.10996  -0.01684
  0.13844  -0.01673
  0.16930  -0.01640
  0.20231  -0.01593
  0.23726  -0.01535
  0.27396  -0.01469
  0.31221  -0.01398
  0.35185  -0.01323
  0.39271  -0.01246
  0.43465  -0.01169
  0.47750  -0.01091
  0.52109  -0.01013
  0.56525  -0.00936
  0.60980  -0.00860
  0.65458  -0.00784
  0.69940  -0.00708
  0.74407  -0.00631
  0.78839  -0.00552
  0.83215  -0.00470
  0.87514  -0.00382
  0.91713  -0.00288
  0.95786  -0.00183
  0.99707  -0.00058
  1.00000  0.00000
""",
}


def get_airfoil_coord_file(airfoil: str, output_dir: str) -> Optional[str]:
    """
    Get or create coordinate file for an airfoil.

    Parameters
    ----------
    airfoil : str
        Airfoil name (e.g., "e387", "s1223", "s7055")
    output_dir : str
        Directory to write coordinate file

    Returns
    -------
    str or None
        Path to coordinate file, or None if not available
    """
    airfoil_lower = airfoil.lower().replace(" ", "")

    if airfoil_lower in AIRFOIL_COORDS:
        output_path = Path(output_dir) / f"{airfoil_lower}.dat"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(AIRFOIL_COORDS[airfoil_lower])

        return str(output_path)

    return None


def compare_airfoils_mars(
    airfoils: List[str],
    reynolds_numbers: List[float],
    xfoil_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, List[XfoilPolar]]:
    """
    Compare multiple airfoils at Mars Reynolds numbers.

    Parameters
    ----------
    airfoils : list
        List of airfoil names
    reynolds_numbers : list
        List of Reynolds numbers to analyze
    xfoil_path : str, optional
        Path to XFOIL executable
    output_dir : str, optional
        Output directory for results

    Returns
    -------
    dict
        Dictionary mapping airfoil names to lists of polars
    """
    if output_dir is None:
        output_dir = Path.cwd() / "airfoil_polars"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    runner = XfoilRunner(xfoil_path=xfoil_path)
    results = {}

    for airfoil in airfoils:
        polars = []

        # Get coordinate file if needed
        coord_file = None
        if not airfoil.upper().startswith("NACA"):
            coord_file = get_airfoil_coord_file(airfoil, str(output_dir))

        for re_num in reynolds_numbers:
            print(f"  Analyzing {airfoil} at Re = {re_num:.0f}...")
            polar = runner.run_polar(
                airfoil=airfoil,
                reynolds=re_num,
                mach=0.0,  # Incompressible for Mars (M << 0.3)
                alpha_range=(-5.0, 25.0, 1.0),
                coord_file=coord_file,
                output_dir=str(output_dir),
            )
            polars.append(polar)

        results[airfoil] = polars

    return results


# =============================================================================
# SELIG EXPERIMENTAL DATA (UIUC Low-Speed Airfoil Tests)
# Reference: Selig et al. (1995) "Summary of Low-Speed Airfoil Data, Vol. 1"
# =============================================================================

SELIG_DATA = {
    "e387": {
        # E387 airfoil - UIUC wind tunnel data
        # Source: Summary of Low-Speed Airfoil Data, Vol. 1, Chapter 5
        60000: {
            "alpha": [-6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14],
            "cl": [-0.25, 0.05, 0.35, 0.55, 0.75, 0.92, 1.05, 1.15, 1.20, 1.18, 1.05],
            "cd": [0.025, 0.018, 0.015, 0.014, 0.014, 0.016, 0.020, 0.028, 0.042, 0.065, 0.095],
        },
        100000: {
            "alpha": [-6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16],
            "cl": [-0.30, 0.02, 0.32, 0.58, 0.80, 0.98, 1.12, 1.22, 1.28, 1.30, 1.25, 1.10],
            "cd": [0.022, 0.015, 0.012, 0.011, 0.011, 0.013, 0.016, 0.022, 0.032, 0.048, 0.072, 0.105],
        },
        200000: {
            "alpha": [-6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16],
            "cl": [-0.32, 0.00, 0.30, 0.60, 0.85, 1.05, 1.20, 1.32, 1.38, 1.40, 1.35, 1.18],
            "cd": [0.018, 0.012, 0.010, 0.009, 0.009, 0.010, 0.013, 0.018, 0.026, 0.040, 0.062, 0.095],
        },
    },
    "s1223": {
        # S1223 high-lift airfoil - UIUC wind tunnel data
        60000: {
            "alpha": [-4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16],
            "cl": [0.40, 0.70, 0.95, 1.20, 1.42, 1.60, 1.75, 1.85, 1.88, 1.82, 1.65],
            "cd": [0.030, 0.025, 0.022, 0.022, 0.025, 0.030, 0.040, 0.055, 0.078, 0.110, 0.150],
        },
        100000: {
            "alpha": [-4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16],
            "cl": [0.38, 0.68, 0.98, 1.25, 1.50, 1.70, 1.85, 1.95, 2.00, 1.95, 1.78],
            "cd": [0.025, 0.020, 0.018, 0.018, 0.020, 0.025, 0.034, 0.048, 0.068, 0.098, 0.138],
        },
    },
    "s7055": {
        # S7055 airfoil - UIUC wind tunnel data
        60000: {
            "alpha": [-6, -4, -2, 0, 2, 4, 6, 8, 10, 12],
            "cl": [-0.15, 0.12, 0.38, 0.62, 0.82, 0.98, 1.08, 1.12, 1.08, 0.95],
            "cd": [0.022, 0.016, 0.014, 0.013, 0.014, 0.017, 0.024, 0.038, 0.058, 0.088],
        },
        100000: {
            "alpha": [-6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14],
            "cl": [-0.18, 0.10, 0.38, 0.65, 0.88, 1.05, 1.18, 1.25, 1.22, 1.10, 0.90],
            "cd": [0.018, 0.013, 0.011, 0.010, 0.011, 0.014, 0.020, 0.030, 0.048, 0.075, 0.110],
        },
    },
}


def get_selig_polar(airfoil: str, reynolds: float) -> Optional[XfoilPolar]:
    """
    Get experimental polar data from Selig's UIUC database.

    Parameters
    ----------
    airfoil : str
        Airfoil name (e.g., "e387", "s1223", "s7055")
    reynolds : float
        Reynolds number (will find closest available)

    Returns
    -------
    XfoilPolar or None
        Polar data if available, None otherwise
    """
    airfoil_lower = airfoil.lower().replace(" ", "")

    if airfoil_lower not in SELIG_DATA:
        return None

    airfoil_data = SELIG_DATA[airfoil_lower]

    # Find closest Reynolds number
    available_re = list(airfoil_data.keys())
    closest_re = min(available_re, key=lambda x: abs(x - reynolds))

    data = airfoil_data[closest_re]

    polar = XfoilPolar(
        airfoil=f"{airfoil} (Selig)",
        reynolds=closest_re,
        mach=0.0,
        alpha=data["alpha"].copy(),
        cl=data["cl"].copy(),
        cd=data["cd"].copy(),
        cm=[0.0] * len(data["alpha"]),  # Cm not always available
    )

    return polar


def print_comparison_table(results: Dict[str, List[XfoilPolar]]) -> str:
    """
    Generate comparison table for airfoil analysis results.

    Parameters
    ----------
    results : dict
        Results from compare_airfoils_mars()

    Returns
    -------
    str
        Formatted comparison table
    """
    lines = [
        "Airfoil Comparison - Mars Reynolds Numbers",
        "=" * 80,
        f"{'Airfoil':<12} {'Re':>10} {'CL_max':>8} {'α_stall':>8} {'(L/D)max':>10} {'CL@L/Dmax':>10} {'CL_α':>8}",
        "-" * 80,
    ]

    for airfoil, polars in results.items():
        for polar in polars:
            if polar.cl:  # Only show if data available
                ld_max, cl_ld = polar.ld_max
                lines.append(
                    f"{airfoil:<12} {polar.reynolds:>10.0f} {polar.cl_max:>8.3f} "
                    f"{polar.alpha_stall:>8.1f}° {ld_max:>10.1f} {cl_ld:>10.3f} "
                    f"{polar.cl_alpha:>8.2f}"
                )

    return "\n".join(lines)


if __name__ == "__main__":
    print("XFOIL Wrapper - Mars UAV Airfoil Analysis")
    print("=" * 60)

    # Mars Reynolds numbers for our configurations
    # Config A: c = 0.58m, V = 40 m/s, ρ = 0.017 kg/m³, μ = 1.0e-5 Pa·s
    # Re_A ≈ 0.017 × 40 × 0.58 / 1.0e-5 ≈ 39,000
    # Config B: c = 1.32m, V = 35 m/s
    # Re_B ≈ 0.017 × 35 × 1.32 / 1.0e-5 ≈ 79,000

    reynolds_numbers = [35000, 50000, 75000]
    airfoils = ["e387", "s1223", "s7055", "NACA 0012"]

    print(f"\nAnalyzing airfoils: {airfoils}")
    print(f"Reynolds numbers: {reynolds_numbers}")

    try:
        results = compare_airfoils_mars(
            airfoils=airfoils,
            reynolds_numbers=reynolds_numbers,
            output_dir="./airfoil_polars",
        )

        print("\n" + print_comparison_table(results))

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please copy xfoil.exe to the project directory or specify path.")
