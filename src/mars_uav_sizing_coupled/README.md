# Mars UAV Sizing Package (Coupled Solver)

This package mirrors `mars_uav_sizing` and adds a coupled, solver-based
sizing workflow. It keeps the existing section structure and config inputs
but uses a matching-chart initial guess followed by a coupled `fsolve`.

## Key Differences

- Coupled solver: solves mass balance, stall, power constraint, and energy
  balance simultaneously and drives all Section 5 analyses.
- Matching chart remains available for visualization and initial guesses.
- Solver settings and engineering seeds (from Section 4) are stored in
  `config/solver_parameters.yaml`.
- Any tuning is treated as a subsequent iteration per Section 2 methodology.

## Usage

Run the full analysis:

```bash
cd src
python -m mars_uav_sizing_coupled.run_analysis
```

Run the matching chart with coupled solver:

```bash
python -m mars_uav_sizing_coupled.section5.matching_chart
```

Run the matching chart without the coupled solver:

```bash
python -m mars_uav_sizing_coupled.run_analysis --uncoupled
```

## Configuration

Base parameters are read from `mars_uav_sizing/config/*.yaml`. Solver-specific
parameters are read from `mars_uav_sizing_coupled/config/solver_parameters.yaml`.

The `--uncoupled` flag runs the full uncoupled analysis from
`mars_uav_sizing.run_analysis` (it ignores `--analysis`).

## Notes

- The coupled solver is designed to use engineering guesses as initial
  conditions. Update the YAML file when exploring new design spaces.
- This package does not modify the original `mars_uav_sizing` codebase.
