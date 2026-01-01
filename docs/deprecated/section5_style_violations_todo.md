# Section 5 Style Violations — COMPLETED

**Status**: ✅ All fixes implemented on 2025-12-29

This document lists all style rule violations identified in Section 5 (Constraint Analysis) that were corrected. Violations are grouped by category and file.

**Reference**: `docs/style_rules.txt`

---

## 1. Bold/Italic Formatting Violations

**Rule**: "Avoid unnecessary bold or italic formatting. Do not use bold or italic to highlight words, acronyms, or new concepts."

### 05_01_rotorcraft-configuration-sec-rotorcraft-analysis.md

| Line | Current Text | Action |
|-----:|:-------------|:-------|
| 15 | `**Conservation of momentum**:` | Remove bold, use prose lead-in |
| 21 | `**Induced velocity**:` | Remove bold |
| 29 | `**Ideal hover power**:` | Remove bold |
| 43 | `*figure of merit*` | Remove italics |
| 47 | `*figure of merit*` | Remove italics |
| 81 | `**hover constraint**`, `**horizontal line**` | Remove bold |
| 151 | `**rotorcraft endurance is independent of MTOW**` | Remove bold |
| 179 | `**Note**:` | Remove bold, rephrase as regular prose |
| 187 | `**No transition benefit**:` | Remove bold |
| 189 | `**Hover time overhead**:` | Remove bold |
| 199 | `**Reserve requirement**:` | Remove bold |
| 201 | `**Comparison with fixed-wing L/D**:` | Remove bold |
| 216 | `**Energy budget breakdown**:` | Remove bold |
| 218 | `**fails**` | Remove bold |
| 222 | `**-4.5% margin**` | Remove bold |
| 224 | `**No abort capability**:` | Remove bold |
| 226 | `**Environmental uncertainty**:` | Remove bold |
| 228 | `**Battery degradation**:` | Remove bold |
| 230 | `**No glide capability**:` | Remove bold |
| 236 | `**fails**` | Remove bold |
| 238 | `**Insufficient endurance**:` | Remove bold |
| 240 | `**High sensitivity to parameters**:` | Remove bold |
| 242 | `**No degraded-mode capability**:` | Remove bold |

### 05_02_fixed-wing-configuration-sec-fixed-wing-analysis.md

| Line | Current Text | Action |
|-----:|:-------------|:-------|
| 149 | `**vertical line**` | Remove bold |
| 177 | `**key endurance equation**`, `**independent of MTOW**` | Remove bold |
| 204 | `**2 hours**` | Remove bold |
| 236 | `**Low density effect on stall speed**:` | Remove bold |
| 242 | `**Low density effect on acceleration**:` | Remove bold |
| 244 | `**Estimated ground roll**:` | Remove bold |
| 248 | `**536 m**` | Remove bold |
| 250 | `**Note**:` | Remove bold |
| 256 | `**Catapult/rail launch**:` | Remove bold |
| 258 | `**Rocket-assisted takeoff (RATO)**:` | Remove bold |
| 260 | `**Balloon-drop launch**:` | Remove bold |
| 262 | `**Air-launch from carrier aircraft**:` | Remove bold |
| 285 | `**exceeds**`, `**fails**` | Remove bold |

### 05_03_hybrid-vtol-configuration-sec-hybrid-vtol-analysis.md

| Line | Current Text | Action |
|-----:|:-------------|:-------|
| 5 | `**only**` | Remove bold |
| 13 | `**Lift system (for hover)**:` | Remove bold |
| 15 | `**Cruise system (for forward flight)**:` | Remove bold |
| 17 | `**decoupled optimisation**:` | Remove bold |
| 35 | `**3 minutes**` | Remove bold |
| 56 | `**20× reduction in hover time**` | Remove bold |
| 121 | `**10 times lower**` | Remove bold |
| 137 | `**unique constraint for hybrid VTOL**` | Remove bold |
| 191 | `**minimum required battery fraction is 27.0%**` | Remove bold |
| 195 | `**both**` | Remove bold |
| 199 | `**Lift system mass**:` | Remove bold |
| 203 | `**Cruise system mass**:` | Remove bold |
| 217 | `**moderate mass penalty**` | Remove bold |
| 227 | `**17%**` | Remove bold |
| 231 | `**acceptable**` | Remove bold |
| 233 | `**Without VTOL capability**:` | Remove bold |
| 235 | `**With VTOL capability**:` | Remove bold |
| 237 | `**enabling cost**` | Remove bold |
| 287 | `**satisfies all mission requirements with adequate margin**` | Remove bold |

### 05_04_matching-chart-methodology-sec-comparative-results.md

| Line | Current Text | Action |
|-----:|:-------------|:-------|
| 25 | `**Horizontal axis: Wing loading ($W/S$)**` | Remove bold |
| 33 | `**Vertical axis: Power loading ($P/W$)**` | Remove bold |
| 45 | `**Hover constraint**` | Remove bold |
| 53 | `**Cruise constraint**` | Remove bold |
| 51 | `**horizontal line**` | Remove bold |
| 59 | `**curve**` | Remove bold |
| 61 | `**Stall constraint**` | Remove bold |
| 67 | `**vertical line**`, `**maximum allowable wing loading**` | Remove bold |
| 69 | `**Energy constraint**` | Remove bold |
| 72 | `**feasible region boundary**` | Remove bold |
| 82 | `**eliminated**` | Remove bold |
| 89 | `**this region is inaccessible**` | Remove bold |
| 97 | `**horizontal line**` | Remove bold |
| 101 | `**curve**` | Remove bold |
| 103 | `**vertical line**` | Remove bold |
| 107 | `**feasible region boundary**` | Remove bold |
| 111 | `**Key observation:**`, `**hover-dominated**` | Remove bold |

---

## 2. Table Caption Placement

**Rule**: "Format tables using pipe table syntax with captions before the table: `: Caption text {#tbl:label}` followed by a blank line, then header row..."

All table captions are currently placed AFTER the table. Move each caption to BEFORE the table.

### 05_01_rotorcraft-configuration-sec-rotorcraft-analysis.md

| Line | Table ID | Action |
|-----:|:---------|:-------|
| 169 | `{#tbl:endurance-parameters}` | Move caption before table (currently after line 168) |
| 214 | `{#tbl:rotorcraft-feasibility}` | Move caption before table |

### 05_02_fixed-wing-configuration-sec-fixed-wing-analysis.md

| Line | Table ID | Action |
|-----:|:---------|:-------|
| 194 | `{#tbl:fw-endurance-parameters}` | Move caption before table |
| 283 | `{#tbl:fw-feasibility}` | Move caption before table |

### 05_03_hybrid-vtol-configuration-sec-hybrid-vtol-analysis.md

| Line | Table ID | Action |
|-----:|:---------|:-------|
| 33 | `{#tbl:quadplane-phases}` | Move caption before table |
| 225 | `{#tbl:mass-penalty-scaling}` | Move caption before table |
| 252 | `{#tbl:quadplane-constraints}` | Move caption before table |
| 272 | `{#tbl:energy-budget-quadplane}` | Move caption before table |
| 285 | `{#tbl:quadplane-feasibility}` | Move caption before table |

### 05_04_matching-chart-methodology-sec-comparative-results.md

| Line | Table ID | Action |
|-----:|:---------|:-------|
| 19 | `{#tbl:requirements-summary}` | Move caption before table |
| 123 | `{#tbl:design-point}` | Move caption before table |
| 135 | `{#tbl:design-parameters}` | Move caption before table |

---

## 3. Hyperbolic Necessity Terms

**Rule**: "Replace hyperbolic necessity terms with modest alternatives. Avoid 'crucial', 'critical', 'vital', or 'essential'. Use 'important', 'necessary', or 'relevant' instead."

| File | Line | Current | Replacement |
|:-----|-----:|:--------|:------------|
| `05_01_rotorcraft` | 37 | "critical scaling relationships" | "important scaling relationships" |
| `05_03_hybrid-vtol` | 35 | "critical observation" | "important observation" |
| `05_03_hybrid-vtol` | 53 | "critical advantage" | "main advantage" or "primary advantage" |
| `05_04_matching-chart` | 9 | "critical requirements" | "key requirements" or "primary requirements" |

---

## 4. Subjective/Evaluative Adjectives

**Rule**: "Avoid subjective evaluative adjectives expressing opinion rather than measurable properties."

| File | Line | Current | Suggested Replacement |
|:-----|-----:|:--------|:----------------------|
| `05_01_rotorcraft` | 185 | "appears promising" | "exceeds the requirement" or factual statement |
| `05_01_rotorcraft` | 232 | "substantially safer" | "provides greater margin" (quantify if possible) |
| `05_02_fixed-wing` | 61 | "substantial improvement" | "improvement of X%" or remove |
| `05_02_fixed-wing` | 127 | "substantially lower" | "lower by a factor of X" (already quantified, remove "substantially") |
| `05_03_hybrid-vtol` | 17 | "key advantage" | "advantage" |
| `05_03_hybrid-vtol` | 35 | "fundamentally changes" | "changes" |
| `05_03_hybrid-vtol` | 81 | "substantial portion" | quantify as percentage |
| `05_03_hybrid-vtol` | 121 | "highlighting the efficiency advantage" | rephrase factually |

---

## 5. Citation Format — Location References

**Rule**: "Use implicit citations only, placing citation tags at the end of the logical statement."

Location-specific references (page numbers, equation numbers, section numbers) should be moved to `source_grounding.txt` rather than appearing inline.

| File | Line | Current Citation | Action |
|:-----|-----:|:-----------------|:-------|
| `05_01_rotorcraft` | 15 | `[@leishmanPrinciplesHelicopterAerodynamics2006, Eq. 2.14]` | Remove `, Eq. 2.14`; document in source_grounding.txt |
| `05_01_rotorcraft` | 21 | `[@leishmanPrinciplesHelicopterAerodynamics2006, Eq. 2.15]` | Remove `, Eq. 2.15` |
| `05_01_rotorcraft` | 91 | `[@leishmanPrinciplesHelicopterAerodynamics2006, Section 5.4]` | Remove `, Section 5.4` |
| `05_02_fixed-wing` | 220 | `[@torenbeekSynthesisSubsonicAirplane1982, Appendix K; @sadraeyAircraftDesignSystems2013, Section 4.3.4]` | Remove location refs |

---

## 6. Em-Dash Usage in Tables

**Rule**: "Never use em-dashes. Use commas to separate concepts and phrases, or hyphens (-) to separate letters or words."

Em-dashes (`—`) appear in table cells as placeholders. Replace with appropriate alternatives.

| File | Line | Current | Replacement |
|:-----|-----:|:--------|:------------|
| `05_03_hybrid-vtol` | 266-270 | `—` in table cells | Use `-` or `N/A` or leave blank |
| `05_04_matching-chart` | 15 | `—` in table cell | Use `-` or descriptive text |

---

## 7. Vertical List to Run-In Text

**Rule**: "Limit vertical (bulleted or numbered) lists to cases strictly necessary for quick reference. Otherwise, use run-in lists integrated into paragraph flow."

| File | Line | Current | Action |
|:-----|-----:|:--------|:-------|
| `05_03_hybrid-vtol` | 109-113 | Bullet list with parameter values | Convert to run-in list or prose: "Using values from @sec:derived-requirements ($V$ = 40 m/s, $(L/D)$ = 10.5, $\eta_\text{prop}$ = 0.55, $\eta_\text{motor}$ = 0.85, $\eta_\text{ESC}$ = 0.95)..." |

---

## Implementation Order

Recommended sequence for fixes:

1. **Table captions** — Move all captions before tables (structural change, easy to verify)
2. **Bold/italic removal** — Systematic removal across all files
3. **Hyperbolic terms** — Quick find-replace with modest alternatives
4. **Subjective adjectives** — Review and rephrase
5. **Citation format** — Remove location references, update source_grounding.txt
6. **Em-dashes** — Replace in tables
7. **Bullet list** — Convert to run-in text

---

## Verification

After implementing fixes:

1. Run `reconstruct.bat` to rebuild `drone.md`
2. Run `build_docx.bat` to verify no Pandoc errors
3. Review generated DOCX for formatting correctness
4. Verify all cross-references still resolve

---

*Document created: 2025-12-29*
