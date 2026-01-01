# Section 6 restructure plan

## Goals
* Make section 6 a complete decision log tied to constraint analysis outputs and trade-off data
* Remove mixed content in section 6.1 by relocating tail, fuselage, and material rationale to the correct subsections
* Replace placeholders with finalized values from the constraint calculations and sizing scripts
* Ensure cross-references, citations, and source grounding are consistent

## Target structure for section 6
* 6.0 Design decisions, short bridge from constraint analysis to selections
* 6.1 Architecture selection, configuration comparison, elimination rationale, final QuadPlane selection, design point summary
* 6.2 Airfoil selection, rationale and performance values from low-Re data
* 6.3 Geometry selection, wing sizing from design point, tail sizing, fuselage dimensions and payload volume
* 6.4 Material selection, structural material choice and thermal considerations
* 6.5 Mass breakdown, computed component masses and mass fraction verification

## Content moves from section 6.1
* Move Tail configuration selection to `sections_en/06_03_geometry-selection-sec-geometry-selection.md`
* Move Fuselage geometry selection to `sections_en/06_03_geometry-selection-sec-geometry-selection.md`
* Move Material selection to `sections_en/06_04_material-selection-sec-material-selection.md`
* Keep architecture comparison, elimination rationale, QuadPlane selection, and configuration summary in `sections_en/06_01_architecture-selection-sec-architecture-selection.md`
* Keep the concept figure in 6.1 unless it is needed to illustrate geometry, otherwise move it to 6.3

## Code and figures (recommended)
* Add `src/mars_uav_sizing/section6/` with `__init__.py` and section scripts that expose `*_analysis()` and `print_analysis()` functions, following sections 4 and 5 conventions and using config-only inputs.
* Proposed scripts:
  * `architecture_selection.py` to assemble the final configuration summary table using outputs from `section5.matching_chart` and `section5.comparative`.
  * `airfoil_selection.py` to tabulate candidate airfoil metrics from a config-backed dataset, no XFOIL, and return the selection rationale values used in 6.2.
  * `geometry_selection.py` to collect final geometry from `section4.geometry_calculations` and `section5.matching_chart`, formatted for 6.3 tables.
  * `mass_breakdown.py` to implement Sadraey mass equations and mass fraction checks for 6.5, using new config keys for material density factors and load factor.
  * Optional `figures.py` to generate section 6 figures using `visualization.plotting` helpers.
* Add missing config entries needed by section 6 calculations, preferably as a new YAML in `src/mars_uav_sizing/config/` (e.g., material density factors, structural coefficients, tail mass fraction assumptions).
* Recommended new figure: a mass breakdown chart for 6.5. If included, add a plot helper in `src/mars_uav_sizing/visualization/plotting.py` and call it from `section6/figures.py`.

## Action plan
1. Clean up section 6.1 and relocate content, keep only architecture level discussion and design point recap with references to @sec:comparative-results.
2. Fill section 6.2 with airfoil selection logic using data from `sections_en/04_07_aerodynamic-analysis-and-airfoil-data-sec-aerodynamic-analysis.md` and finalize chosen airfoil with values and citations.
3. Populate section 6.3 with wing geometry derived from @tbl:design-point and @tbl:design-parameters, then append tail and fuselage content moved from 6.1 and update to match constraint outputs.
4. Populate section 6.4 with moved material text and align with trade-off evidence from `sections_en/04_10_structural-materials-sec-materials-data.md`.
5. Implement section 6 calculation scripts in `src/mars_uav_sizing/section6/` and add any missing config parameters required for mass breakdown and geometry summary tables.
6. If a new mass breakdown figure is approved, add plotting support in `src/mars_uav_sizing/visualization/plotting.py`, then generate the figure through `section6/figures.py` into `figures/`.
7. Complete section 6.5 by replacing placeholders with computed values from the section 6 scripts, then update mass fraction verification.
8. Run a consistency pass, remove garbled symbols, enforce 4 significant figures for numbers, verify cross-references, and update `source_grounding.txt` for any new or revised data claims.
9. Reconstruct the manuscript and spot check section 6 in `drone.md`, then optionally build the docx for layout verification.
