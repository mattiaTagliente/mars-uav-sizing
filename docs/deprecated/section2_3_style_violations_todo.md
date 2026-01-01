# Style Rule Violations - Sections 2 and 3

**Generated**: 2025-12-29  
**Purpose**: Identify all style rule violations in Sections 2 and 3 against `docs/style_rules.txt`

---

## Section 2: Design Methodology

### File: `02_00_design-methodology.md`
**Status**: ✅ No violations detected

---

### File: `02_01_iterative-sizing-approach-sec-iterative-sizing.md`

| Line | Violation | Rule Reference | Current Text | Suggested Fix |
|------|-----------|----------------|--------------|---------------|
| 9 | Bold for emphasis | "Avoid unnecessary bold or italic formatting" | `**Phase 1: Initial hypotheses.**` | Remove bold, use plain text or integrate into prose |
| 11 | Bold for emphasis | Same rule | `**Phase 2: Preliminary sizing.**` | Remove bold |
| 13 | Bold for emphasis | Same rule | `**Phase 3: Component selection.**` | Remove bold |
| 15 | Bold for emphasis | Same rule | `**Phase 4: Verification.**` | Remove bold |

**Note**: The four phases are presented as bold-prefixed paragraphs. This is a borderline case since they function as pseudo-list items, but the style rules explicitly state: "Avoid unnecessary bold or italic formatting. Do not use bold or italic to highlight words, acronyms, or new concepts." Consider converting to either:
- A numbered list with phase names as regular text
- Run-in prose without bold emphasis

---

### File: `02_02_role-of-constraint-based-sizing-sec-constraint-role.md`

| Line | Violation | Rule Reference | Current Text | Suggested Fix |
|------|-----------|----------------|--------------|---------------|
| 9 | Bold for emphasis | "Avoid unnecessary bold or italic formatting" | `* **Hover constraint**:` | Remove bold from list item labels |
| 10 | Bold for emphasis | Same rule | `* **Cruise constraint**:` | Remove bold |
| 11 | Bold for emphasis | Same rule | `* **Climb constraint**:` | Remove bold |
| 12 | Bold for emphasis | Same rule | `* **Stall constraint**:` | Remove bold |

**Note**: While these are technical definitions that may justify a list format, the bold formatting of labels violates style rules. The reference to `@tbl:derived-requirements` on line 16 is valid - Pandoc cross-references are resolved manuscript-wide at build time.

---

## Section 3: Mission Analysis

### File: `03_00_mission-analysis.md`
**Status**: ✅ No violations detected

---

### File: `03_01_operational-environment-sec-operational-environment.md`

| Line | Violation | Rule Reference | Current Text | Suggested Fix |
|------|-----------|----------------|--------------|---------------|
| 45-54 | Table caption position | "Format tables with captions before the table" | Caption on line 54, table on lines 45-52 | Move caption to before line 45 |
| 49 | Significant figures | "Always use 4 significant figures for reporting calculation results" | `0.0196` (3 sig figs) | Change to `0.01960` (4 sig figs) |
| 51 | Scientific notation consistency | Same rule | `1.08 × 10⁻⁵` | Verify this has 3 sig figs; should be `1.080 × 10⁻⁵` |
| 52 | Significant figures | Same rule | `5.17 × 10⁻⁴` | Change to `5.170 × 10⁻⁴` |

**Corrected table format**:
```markdown
: Atmospheric conditions at Arcadia Planitia, 50 m AGL {#tbl:atmosphere}

| Property | Symbol | Value | Units |
|:---------|:------:|------:|:------|
| Temperature | $T$ | 216.6 | K |
| Pressure | $p$ | 800.5 | Pa |
| Density | $\rho$ | 0.01960 | kg/m³ |
| Speed of sound | $a$ | 230.8 | m/s |
| Dynamic viscosity | $\mu$ | 1.080 × 10⁻⁵ | Pa·s |
| Kinematic viscosity | $\nu$ | 5.170 × 10⁻⁴ | m²/s |
```

---

### File: `03_02_mission-profile-sec-mission-profile.md`
**Status**: ✅ No violations detected

---

### File: `03_03_user-needs-sec-user-needs.md`

| Line | Violation | Rule Reference | Current Text | Suggested Fix |
|------|-----------|----------------|--------------|---------------|
| 5 | Italics for emphasis | "Avoid unnecessary bold or italic formatting" | `*what*` | Remove italics, rephrase if needed |
| 9 | Bold for emphasis | Same rule | `**N1. Extended operational range**:` | Remove bold from need identifiers |
| 11 | Bold for emphasis | Same rule | `**N2. Aerial imaging**:` | Remove bold |
| 13 | Bold for emphasis | Same rule | `**N3. Communication relay**:` | Remove bold |
| 15 | Bold for emphasis | Same rule | `**N4. Vertical takeoff and landing**:` | Remove bold |
| 17 | Bold for emphasis | Same rule | `**N5. Extended endurance**:` | Remove bold |
| 21 | Bold for emphasis | Same rule | `**N6. Single-fault tolerance**:` | Remove bold |
| 23 | Bold for emphasis | Same rule | `**N7. Wind tolerance**:` | Remove bold |
| 25 | Bold for emphasis | Same rule | `**N8. Dust ingress protection**:` | Remove bold |
| 29 | Bold for emphasis | Same rule | `**N9. Electric propulsion**:` | Remove bold |
| 31 | Bold for emphasis | Same rule | `**N10. Radiation tolerance**:` | Remove bold |
| 33 | Bold for emphasis | Same rule | `**N11. Thermal compatibility**:` | Remove bold |

**Note**: The user needs are structured as labeled paragraphs under subsection headers. The bold **NX.** identifiers violate the style rule. Options for fixing:
1. Remove bold entirely: `N1. Extended operational range: The UAV shall...`
2. Convert to proper definition list format (if Pandoc supports it)
3. Use subsection headers for each need (may be too granular)

---

## Summary Statistics

| Section | File | Violations |
|---------|------|------------|
| 2 | 02_00_design-methodology.md | 0 |
| 2 | 02_01_iterative-sizing-approach.md | 4 |
| 2 | 02_02_role-of-constraint-based-sizing.md | 4 |
| 3 | 03_00_mission-analysis.md | 0 |
| 3 | 03_01_operational-environment.md | 4 |
| 3 | 03_02_mission-profile.md | 0 |
| 3 | 03_03_user-needs.md | 12 |
| **Total** | | **24** |

---

## Priority Recommendations

### High Priority (Format/Rendering Issues)
1. **Table caption position** in 03_01: Must be fixed for proper Pandoc rendering
2. **Significant figures** in 03_01: Affects numerical consistency

### Medium Priority (Style Consistency)
3. **Bold emphasis removal** across all affected files: 16 instances total
4. **Italics removal** in 03_03: 1 instance

### Low Priority (Structural Consideration)
5. **Vertical list conversion** in 02_02: Consider converting to prose, but acceptable as reference list

---

## Checklist for Implementation

- [x] 02_01: Remove bold from Phase 1-4 labels
- [x] 02_02: Remove bold from constraint list items
- [x] 03_01: Move table caption before table
- [x] 03_01: Update density to 4 significant figures (0.01960)
- [x] 03_01: Update dynamic viscosity to 4 sig figs (1.080 × 10⁻⁵)
- [x] 03_01: Update kinematic viscosity to 4 sig figs (5.170 × 10⁻⁴)
- [x] 03_03: Remove italics from "what"
- [x] 03_03: Remove bold from all 11 user need identifiers (N1-N11)

**All fixes implemented on 2025-12-29.**
