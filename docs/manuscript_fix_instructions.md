# Manuscript Fix Instructions

## Source of truth

All numeric values must come from code outputs. Update or complete the code first, then refresh the manuscript content and tables using the generated outputs. Do not manually type numeric values into the manuscript without tracing them to code output.

## Abstract and baseline

Update the English and Italian abstracts to match the baseline defined in configuration and produced by code outputs. Keep architecture, operating location, environment, Reynolds range, airfoil selection, and feasibility statements consistent with the analysis outputs.

## Energy budget and reserve handling in code

Implement a shared energy accounting helper in the sizing package to compute available energy, mission energy, reserve energy, required energy, and margins using configuration values. Use that helper in rotorcraft, fixed wing, and hybrid VTOL analyses and in any performance verification output. Ensure reserve fraction and depth of discharge always come from configuration and that any printed labels are derived from configuration instead of hard coded text. Provide a single output source for the manuscript energy budget tables and verification narrative.

## Architecture comparison alignment

Compute propulsion fraction, mass penalty, and any other comparison metrics directly from configuration and analysis outputs. Ensure the architecture comparison tables in both languages use those outputs.

## Rotor and motor count clarity

Add explicit motor and rotor count fields in configuration or analysis outputs. Update architecture selection and configuration description text to state total motor count and lift versus cruise split using those outputs.

## Propeller sizing and hangar envelope alignment

Add a new subsection in the geometry selection section for propeller sizing, covering lift propeller sizing and cruise propeller sizing. Implement the corresponding sizing code in the appropriate section module following the existing section-based code organization and configuration-driven inputs. Use the code outputs to populate the UAV dimensional envelope table in the infrastructure section and remove any made-up dimensions.

## Performance verification alignment

Generate performance verification tables and equations from code outputs. Fix range computation by using the code outputs rather than manual arithmetic. Keep verification narrative aligned with the hybrid VTOL analysis outputs.

## Atmosphere and derived requirements alignment

Update all tables and derived values from code outputs, including the atmosphere table and any derived requirement summaries.

## Complete all sections

Complete tail sizing and mass breakdown with calculated values from code outputs. Remove placeholders and pending markers.

## Style rules

Apply `docs/style_rules.txt` across all English and Italian sections.

## Outdated artifacts

Move `sizing_results.txt` to the deprecated folder under the sizing package.

## Rebuild

Run the document reconstruction and docx build scripts, then review the build log.
