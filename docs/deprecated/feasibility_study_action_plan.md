# Action plan for mission-driven feasibility study (baseline case with honest feasibility checks)

## Purpose and scope

This plan defines the minimum set of actions required to produce a mission-driven and internally consistent feasibility study using the baseline-case methodology (fixed reference MTOW) and to document a deferred, improved methodology as future work.

The target outcome is a manuscript that:

* reports results that are reproducible from the current sizing code
* states feasibility conditions and limitations explicitly (payload and energy constraints included)
* avoids presenting exploratory coupled sizing results as final design results

## Key decisions (record)

* Baseline case is retained for this feasibility study: the comparative analysis is performed at a fixed reference MTOW justified in Section 4.
* Mission constraints are treated as non-negotiable requirements, including payload mass and endurance.
* Energy feasibility is treated as necessary for any configuration labelled feasible, including reserve and non-cruise phases.
* A configuration-specific coupled sizing workflow (improved approach) is deferred to future work and is not required for feasibility-study completion.

## Working definition of “feasible” (necessary and sufficient for this study)

For a configuration to be labelled feasible in the baseline case, all items below must be satisfied simultaneously under the same set of assumptions:

* Payload: the mission payload mass is carried as a fixed mass term in the mass model, and the baseline MTOW allocation remains consistent with the assumed mass fractions in Section 4.
* VTOL: configurations that do not satisfy the VTOL requirement are labelled not feasible regardless of endurance.
* Energy: the mission energy budget including hover, transition allowance, cruise, battery depth of discharge, discharge efficiency, and reserve fraction is satisfied.
* Endurance and range: the computed mission endurance and range satisfy the requirement thresholds.

If a condition is not modelled (for example, packaging volume, thermal margins, controllability, actuator sizing), it must be stated as an unverified item and treated as a limitation, not as satisfied.

## Current state audit (inputs and code authority)

* Manuscript results in Section 5.4 are expressed for a baseline `MTOW = 10.00 kg` and use that MTOW to compute absolute geometry and installed power (`S`, `b`, `P`), see `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md`.
* Uncoupled code path (authoritative for baseline case): `src/mars_uav_sizing/`.
* Coupled code path (exploratory, not yet suitable for baseline-case manuscript numbers): `src/mars_uav_sizing_coupled/` currently solves one coupled state and reuses it across configurations, which is not a mission-fair comparison across architectures.

## Deliverables

* Updated manuscript sections that match the uncoupled code outputs and state feasibility conditions precisely:
  * `sections_en/05_01_rotorcraft-configuration-sec-rotorcraft-analysis.md`
  * `sections_en/05_02_fixed-wing-configuration-sec-fixed-wing-analysis.md`
  * `sections_en/05_03_hybrid-vtol-configuration-sec-hybrid-vtol-analysis.md`
  * `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md`
* Reproducible baseline report generated from `src/mars_uav_sizing/run_analysis.py` and stored under `reports/` with an unambiguous label and UTF-8-safe output.
* A future-work subsection describing the deferred “improved approach” without changing the current feasibility-study scope.

## Action steps (baseline case completion)

### 1. Align definitions, assumptions, and terminology in the manuscript

* Add a short paragraph in `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md` stating explicitly that the matching-chart design point is evaluated at a fixed baseline MTOW (reference case), and that it is not a closed-loop sizing result.
* Add a short paragraph in `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md` stating that the energy constraint is verified by an explicit mission energy budget evaluation at the candidate design point, and is not plotted as a separate constraint line for the fixed disk loading baseline case.
* Add a short paragraph in `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md` stating what is held constant across configurations in the baseline comparison (payload mass, MTOW, battery technology assumptions, reserve policy, mission time allocations).

### 2. Ensure payload constraint is applied and communicated correctly

* Confirm that the baseline case uses `mission.mass.payload_kg = 1.0` and `mission.mass.mtow_kg = 10.0` with consistent mass fractions in `src/mars_uav_sizing/config/mission_parameters.yaml`.
* Add a “payload feasibility” statement in Section 4 or Section 5 clarifying that the payload mass is a fixed mission constraint and is included in the mass allocation.
* Ensure that any discussion of “optimising MTOW” is confined to future work unless a configuration-specific closure is implemented and validated.

### 3. Make energy accounting consistent across configurations (honest feasibility)

* Confirm that all three configurations apply the same reserve policy (`mission.energy.reserve_fraction`) and battery utilisation (`dod`, `eta_discharge`) when computing endurance.
* Confirm that rotorcraft and hybrid VTOL include explicit hover energy for `t_hover_s`.
* For hybrid VTOL, ensure that transition energy is either modelled (with clear assumptions) or explicitly bounded, and that the manuscript states which approach is used.
* Update any manuscript numbers to 4 significant figures and ensure consistency with the current code outputs.

### 4. Correct report generation for reproducibility and manuscript integration

* Generate a single “baseline case” report from `src/mars_uav_sizing/run_analysis.py` and save it under `reports/` with a stable naming scheme (date-time and mode).
* Ensure report headers match the actual mode (avoid “COUPLED” headers when running uncoupled code paths).
* Ensure report output is UTF-8 clean and does not contain non-standard glyphs that impede manuscript copy-paste.

### 5. Reconcile figures and tables with code outputs

* Regenerate the matching chart figure used in `sections_en/05_04_matching-chart-methodology-sec-comparative-results.md` and ensure it corresponds to the baseline assumptions (fixed MTOW and fixed disk loading) and to the numbers reported in `@tbl:design-point` and `@tbl:design-parameters`.
* Confirm that any comparative figures (`@fig:ld-comparison`, `@fig:endurance-comparison`) are generated from the same baseline configuration and are not mixing coupled and uncoupled results.

### 6. Verification loop (required before manuscript rebuild)

* Run manuscript verification checks using `src/mars_uav_sizing/verification/verify_manuscript.py` and reconcile any mismatches by updating either:
  * the manuscript text and tables, if the code is authoritative for the stated assumptions
  * the YAML configuration, if the manuscript states a different assumption
* Rebuild the manuscript using `reconstruct.bat` and confirm that cross-references, equations, and figures render correctly in `build_docx.bat`.

## Deferred future work (improved approach, not required for this study)

This subsection is intended to be added to conclusions or future work, without changing the baseline-case results.

* Implement configuration-specific coupled closures:
  * rotorcraft closure: solve for MTOW and battery mass given payload mass, disk loading, hover time, cruise time, and energy reserve
  * fixed-wing closure: solve for MTOW and battery mass given payload mass, chosen `W/S`, cruise speed policy, and energy reserve
  * hybrid VTOL closure: solve for MTOW and battery mass given payload mass, `DL`, `W/S`, mission segment times, transition energy model, and energy reserve
* Replace fixed mass fractions with a minimal component-based mass model for at least battery, payload, propulsion, and structure, and add a plausibility constraint on payload fraction using the reference drone database.
* Produce configuration-appropriate constraint diagrams:
  * rotorcraft: `P/W` vs `DL`
  * fixed-wing: `P/W` vs `W/S` with relevant constraints
  * hybrid VTOL: `P/W` vs `W/S` plus parametric sweeps in `DL` and mission times
* Report results as minimum feasible MTOW (or maximum margin) subject to all mission constraints, and clearly separate design variables from requirements.

## Acceptance criteria (baseline case)

* A reader can reproduce all Section 5 numeric results by running `src/mars_uav_sizing/run_analysis.py` with the committed YAML inputs.
* Any feasible label is backed by an explicit payload statement, an energy budget check (including reserve), and the endurance requirement check.
* The manuscript does not mix coupled and uncoupled results in the same baseline-case tables or claims.

