# Section 4 Style Rule Violations - TODO

**Status: ALL FIXES IMPLEMENTED** (2025-12-29)

This document identified all violations of the style rules (as defined in `docs/style_rules.txt`) found in Section 4 of the manuscript. All issues have now been resolved.

---

## Summary of Violations (Resolved)

| Rule Category | Violation Count | Files Affected | Status |
|:--------------|:---------------:|:---------------|:------:|
| Subscripts/superscripts | 2 | 04_02, 04_04 | ✓ Fixed |
| Lists (should be prose) | 6 | 04_02, 04_03, 04_11, 04_12 | ✓ Fixed |
| Subjective adjectives | 2 | 04_06 | ✓ Fixed |
| Bold/italic misuse | 3 | 04_11, 04_12 | ✓ Fixed |
| Table caption placement | 1 | 04_04 | ✓ Fixed |

---

## Fixes Applied

### 04_02_architecture-comparison-sec-architecture-comparison.md

- [x] **Line 15**: Changed `A~rotor~` to `$A_\text{rotor}$` (LaTeX math mode for subscripts)
- [x] **Lines 51–55**: Converted fuselage-mounted tail configuration bullets to prose paragraphs
- [x] **Lines 59–62**: Converted boom-mounted tail configuration bullets to prose paragraphs

### 04_03_mars-uav-concepts-sec-mars-uav-concepts.md

- [x] **Lines 5–15**: Converted Mars UAV concepts bulleted list to prose paragraphs (Ingenuity, ARES, Mars Science Helicopter, Hybrid VTOL concepts)

### 04_04_commercial-vtol-benchmarks-sec-commercial-vtol.md

- [x] **Lines 7–19**: Moved table caption from after table to before table
- [x] **Table header**: Changed `V~cruise~` to `$V_\text{cruise}$` (LaTeX math mode)

### 04_06_energy-storage-characteristics-sec-energy-data.md

- [x] **Line 5**: Replaced "critical" with "important"
- [x] **Line 21**: Replaced "attractive" with "suitable"

### 04_11_initial-mass-estimate-sec-initial-mass-estimate.md

- [x] **Lines 40–48**: Converted key observations bulleted list to prose paragraph
- [x] **Line 89**: Removed bold from "10 kg"

### 04_12_derived-requirements-sec-derived-requirements.md

- [x] **Lines 71–83**: Converted numbered load factor justification list to prose paragraphs
- [x] **Line 103**: Removed bold from "Note on regulatory status" and integrated into prose

---

## Compliant Files (No Changes Needed)

These files had no style violations:
- 04_00_reference-data-and-trade-off-analysis (header only)
- 04_01_payload-systems ✓
- 04_05_propulsion-characteristics ✓
- 04_07_aerodynamic-analysis-and-airfoil-data ✓
- 04_08_fuselage-geometry ✓
- 04_09_tail-configurations ✓
- 04_10_structural-materials ✓

---

## Notes

1. **Tight lists**: All lists were already tight (no blank lines between items). No violations found.

2. **Cross-references**: All cross-references use the correct format (`@tbl:`, `@eq:`, `@fig:`, `@sec:`). No hard-coded references found.

3. **First-person pronouns**: No instances of "I," "we," or "you" found in Section 4.

4. **Citations**: All citations use implicit format `[@author2024]`. No explicit attribution phrases found.

5. **UTF-8 encoding**: Files use correct encoding with Unicode symbols (°, μ, ×, etc.) rendered correctly.

6. **Asterisks for bullets**: All bulleted lists use asterisks (*), not hyphens.

7. **Bold in tables**: The bold row for "Mars UAV (this study)" in `@tbl:load-factor-comparison` was retained as it serves an identification purpose in a comparative table, which is an acceptable use case.
