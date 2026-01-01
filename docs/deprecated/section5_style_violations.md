# Section 5: Style Rule Violations

**Date:** 2025-12-30
**Scope:** All files in `sections_en/05_*`

---

## Summary

This document identifies all violations of the style rules documented in `docs/style_rules.txt` found in Section 5 (Constraint Analysis) of the manuscript.

---

## File: `05_00_constraint-analysis-sec-constraint-analysis.md`

**No violations found.** This is a brief section header file with compliant formatting.

---

## File: `05_01_rotorcraft-configuration-sec-rotorcraft-analysis.md`

### 1. Missing Header Cross-Reference Label (Line 1)

**Rule violated:** Cross-reference labels should be applied to section headers for proper navigation.

**Current:**
```markdown
# Constraint analysis
```

**Issue:** The top-level header lacks a cross-reference label `{#sec:...}`.

**Fix:** Add a label or remove if redundant with the parent section.

---

### 2. Wrong Character: Question Mark Instead of Greater-Than Symbol (Line 213)

**Rule violated:** Use Unicode characters directly for common symbols (line 5 of style rules); escape special characters for markdown (line 30).

**Current:**
```markdown
| Cruise endurance | ?60 min | 63.17 min (with 20% reserve) | PASS |
```

**Issue:** The "?" character appears to be a corrupted "≥" symbol.

**Fix:** Replace with `≥60 min`.

---

### 3. Wrong Character: Question Mark Instead of Multiplication (Line 218)

**Rule violated:** Use Unicode characters directly for common symbols.

**Current (multiple occurrences on line 218):**
```markdown
The usable energy is 718.2 Wh ? 0.80 (reserve) = 574.6 Wh.
...
Range: 40.00 m/s ? 61.17 min ? 60 s/min = 146.8 km.
```

**Issue:** The "?" characters should be "×" (multiplication sign).

**Fix:** Replace "?" with "×" in all arithmetic expressions.

---

### 4. Colon After Constraint Statement (Line 220-221)

**Rule violated:** Limit vertical lists to cases strictly necessary for quick reference (line 48).

**Current:**
```markdown
The rotorcraft configuration marginally meets the endurance requirement (63.17 min vs 60 min required), but the margin is limited:

#### Sensitivity analysis
```

**Issue:** The colon suggests a list follows, but instead a new section header appears. This is inconsistent formatting.

**Fix:** Remove the colon or add the intended content as prose.

---

### 5. Missing Tight List Formatting (Lines 222-232)

**Rule violated:** Make ALL lists tight by removing ALL blank lines (line 50).

**Issue:** The prose paragraphs from line 222-232 read like a list but are formatted as separate paragraphs, creating loose spacing. If intended as prose, this is acceptable. If intended as a list, it should use asterisks.

**Recommendation:** Review intent. If these are related points about sensitivity, consider converting to a tight bulleted list or integrating into flowing prose.

---

### 6. Implicit List Without Bullets (Lines 236-246)

**Rule violated:** Always use asterisks (*) for bulleted lists (line 46).

**Current (lines 236-246):**
```markdown
### Rotorcraft configuration conclusion

The pure rotorcraft configuration marginally meets...

The 63.17-minute achievable endurance exceeds...

Any variation in atmospheric density...

Unlike a hybrid VTOL that can glide...

The fundamental limitation is the low equivalent...
```

**Issue:** These read as separate list items but are formatted as paragraphs. This creates visual inconsistency.

**Recommendation:** Either convert to a tight bulleted list or merge into flowing prose paragraphs.

---

## File: `05_02_fixed-wing-configuration-sec-fixed-wing-analysis.md`

### 1. Missing Header Cross-Reference Label (Line 1)

**Rule violated:** Cross-reference labels for navigation.

**Current:**
```markdown
# Constraint analysis
```

**Fix:** Add label or confirm redundancy with parent.

---

### 2. Run-In List Candidates (Lines 236-244)

**Rule violated:** Limit vertical lists; use run-in lists integrated into paragraph flow (line 48).

**Current (lines 234-244):**
```markdown
#### Mars-specific effects on takeoff

On Mars, several factors increase the takeoff distance:

Regarding low density effect on stall speed, the stall speed scales...

Regarding low density effect on acceleration, both thrust...

For the estimated ground roll, using the standard ground roll estimation...
```

**Issue:** These paragraphs start with "Regarding..." which creates an implicit list structure. They could be better integrated as a run-in list or with proper bullet points.

**Fix:** Convert to either:
- A proper tight bulleted list with asterisks, or
- A run-in list integrated into the introductory paragraph.

---

### 3. Run-In List Candidates (Lines 254-266)

**Rule violated:** Limit vertical lists; use run-in lists (line 48).

**Current:**
```markdown
#### Alternative launch methods

Several alternative launch methods exist...

Catapult or rail launch requires substantial ground infrastructure...

Rocket-assisted takeoff (RATO) requires solid rocket boosters...

Balloon-drop launch requires carrying the aircraft to altitude...

Air-launch from a carrier aircraft is not applicable...

All alternative launch methods fail the operational requirements...
```

**Issue:** Each launch method is described in a separate paragraph. This could be tightened.

**Fix:** Consider converting to a tight bulleted list or run-in list.

---

### 4. Verbose Prose Structure (Lines 289-297)

**Rule violated:** Limit vertical lists (line 48); maintain concise prose.

**Current:**
```markdown
### Fixed-wing configuration conclusion

The pure fixed-wing configuration cannot satisfy the VTOL requirement...

Despite achieving $(L/D)$ = 11.68 and demonstrating theoretical endurance...

The fixed-wing analysis demonstrates three key points. First, aerodynamic efficiency... Second, moderate L/D is achievable... Third, fixed-wing cruise should be exploited...
```

**Issue:** The "First...Second...Third..." structure could be formatted as a tight list for clarity.

**Recommendation:** Either keep as prose (acceptable) or convert to a proper numbered/bulleted list.

---

## File: `05_03_hybrid-vtol-configuration-sec-hybrid-vtol-analysis.md`

### 1. Missing Header Cross-Reference Label (Line 1)

**Rule violated:** Cross-reference labels.

**Current:**
```markdown
# Constraint analysis
```

**Fix:** Add label or confirm redundancy.

---

### 2. Implicit Lists Without Bullets (Lines 11-17)

**Rule violated:** Always use asterisks for bulleted lists (line 46); limit vertical lists (line 48).

**Current:**
```markdown
The lift system (for hover) comprises four or more electric rotors in a quadcopter or similar layout, sized for hover thrust only (short duration operation), positioned to minimise interference with wing aerodynamics, and inactive during cruise (stopped or folded).

The cruise system (for forward flight) uses a wing for lift generation and a single pusher or tractor propeller for thrust, sized for efficient cruise at $(L/D)_\text{max}$, and inactive during hover.
```

**Issue:** These paragraphs contain internal comma-separated lists that could be formatted as bulleted lists for clarity.

**Recommendation:** Consider converting the internal lists to proper tight bulleted lists, or keep as prose (acceptable as-is).

---

### 3. Run-In List as Paragraphs (Lines 93-101)

**Rule violated:** Limit vertical lists; use run-in lists (line 48).

**Current:**
```markdown
Two design approaches are possible: stopped rotors (rotors remain stationary, contributing only parasitic drag), and folded rotors (rotor blades fold against the motor pods, minimising drag).

For stopped rotors, the parasitic drag of four motor pods...

For folded rotors, the drag penalty is smaller...

A value of $(L/D)$ = 10.50 is adopted...
```

**Issue:** The "For stopped rotors" / "For folded rotors" structure creates implicit list paragraphs.

**Recommendation:** Keep as prose (acceptable) or convert to a tight bulleted list.

---

### 4. Implicit Bulleted Lists as Paragraphs (Lines 169-177)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
#### Limitations of the transition energy model

The transition energy estimate used here is a simplified energy-only model with several acknowledged limitations:

First, the linear mass scaling assumes...

Second, the model does not capture peak transition power...

Third, the model does not address power-limited feasibility...
```

**Issue:** "First...Second...Third..." reads as an ordered list but is formatted as paragraphs.

**Fix:** Convert to a numbered list or tight bulleted list:
```markdown
* First, the linear mass scaling assumes...
* Second, the model does not capture peak transition power...
* Third, the model does not address power-limited feasibility...
```

---

### 5. Implicit Bulleted Lists (Lines 187-191)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
The energy reserve accounts for navigation inefficiencies and course corrections, atmospheric density variations from the model, extended hover for precision landing or abort, and emergency return capability.
```

**Issue:** This run-in list is comma-separated within the paragraph.

**Status:** This is **acceptable** per the style rule that prefers run-in lists over vertical lists. No action needed.

---

### 6. Implicit Bulleted Paragraphs (Lines 241-249)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
#### Dual propulsion mass breakdown

The lift system comprises motors, ESCs, propellers, and mounting structure. For the 10.00 kg MTOW aircraft, the lift system scales from reference data: lift motors 4 × 0.2500 kg = 1.000 kg, lift ESCs 4 × 0.0600 kg = 0.2400 kg, lift propellers 4 × 0.0400 kg = 0.1600 kg, and mounting structure ~0.3000 kg.

...

The cruise system comprises a single motor, ESC, and propeller: cruise motor ~0.2000 kg, cruise ESC ~0.0500 kg, and cruise propeller ~0.0500 kg.
```

**Issue:** The component breakdowns could be formatted as bulleted lists for clarity.

**Recommendation:** Consider converting to bulleted lists or keep as prose (acceptable as-is).

---

### 7. Implicit Numbered Paragraphs (Lines 273-281)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
#### Mass penalty trade-off

The dual propulsion mass penalty is acceptable because it enables mission feasibility. The trade-off is:

Without VTOL capability, the mission is impossible—no means of takeoff or landing on Mars without runway infrastructure.

With VTOL capability, the mission becomes possible with the mass penalty.

The mass penalty is the enabling cost for the Mars UAV mission...
```

**Issue:** "The trade-off is:" suggests a list follows, but items are formatted as paragraphs.

**Fix:** Convert to a tight bulleted list:
```markdown
The trade-off is:

* Without VTOL capability, the mission is impossible—no means of takeoff or landing on Mars without runway infrastructure.
* With VTOL capability, the mission becomes possible with the mass penalty.
```

---

### 8. Em-Dash Usage (Line 277)

**Rule violated:** Never use em-dashes; use commas or hyphens (line 38).

**Current:**
```markdown
Without VTOL capability, the mission is impossible—no means of takeoff or landing on Mars without runway infrastructure.
```

**Fix:** Replace em-dash with comma or rephrase:
```markdown
Without VTOL capability, the mission is impossible, as there is no means of takeoff or landing on Mars without runway infrastructure.
```

---

### 9. Inconsistent Significant Figures (Various Lines)

**Rule violated:** Always use 4 significant figures for reporting calculation results (line 11).

**Examples:**
- Line 113: `= 318 W` → should be `= 318.0 W` or `= 318.5 W` (4 sig figs)
- Line 127: `= 302.6 Wh` → acceptable (4 sig figs)
- Line 201: `= 501.6 Wh` → acceptable (4 sig figs)
- Line 310: `= 106.0` → acceptable (4 sig figs)
- Line 312: `= 302.0` → acceptable (4 sig figs)

**Fix:** Ensure all numerical results have 4 significant figures.

---

## File: `05_04_matching-chart-methodology-sec-comparative-results.md`

### 1. Missing Header Cross-Reference Label (Line 1)

**Rule violated:** Cross-reference labels.

**Current:**
```markdown
# Constraint analysis
```

**Fix:** Add label or confirm redundancy.

---

### 2. Wrong Character: Question Mark Instead of Greater-Than Symbol (Line 16)

**Rule violated:** Use Unicode characters directly for common symbols.

**Current:**
```markdown
| OR-4 | Cruise endurance | ?60 min | Round trip + survey operations (42 min transit + 15 min survey + 2 min hover + 1 min transition) |
```

**Issue:** The "?" character should be "≥".

**Fix:** Replace with `≥60 min`.

---

### 3. Implicit Heading List (Lines 25-39)

**Rule violated:** Limit vertical lists (line 48).

**Current:**
```markdown
Horizontal axis (Wing loading, $W/S$):

Wing loading is defined as...

Higher wing loading implies smaller wing area for a given weight, resulting in higher cruise and stall speeds, reduced drag from smaller wetted area, lighter wing structure, and increased sensitivity to gusts.

Vertical axis (Power loading, $P/W$):

Power loading is defined as...
```

**Issue:** The structure uses paragraph-level headings followed by prose. This is acceptable, but the comma-separated list inside the prose could be formatted as a bulleted list.

**Status:** Acceptable as prose with run-in lists.

---

### 4. Implicit Bulleted Structure (Lines 45-72)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
Hover constraint (rotorcraft and hybrid VTOL):

From @eq:hover-constraint...

Cruise constraint (fixed-wing and hybrid VTOL):

From @eq:cruise-electric-power...

Stall constraint:

From @eq:wing-loading-constraint...

Energy constraint (hybrid VTOL):

The energy constraint from...
```

**Issue:** Each constraint is formatted as a paragraph with bold-like header text. This could be a bulleted list.

**Status:** Acceptable as prose with sub-headers. No action required.

---

### 5. Implicit Bulleted Structure (Lines 117-122)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
For the pure fixed-wing configuration, the matching chart shows a cruise constraint as a shallow curve with minimum at optimal wing loading (approximately 11.00 N/m² for Mars conditions), a stall constraint as a vertical line at $W/S_\text{max}$ = 14.42 N/m² for $V_\text{min}$ = 35.04 m/s (where $V_\text{min}$ = 1.2 × $V_\text{stall}$ per @eq:v-min-constraint) and $C_{L,\text{max}}$ = 1.200, and no hover constraint (the fixed-wing cannot hover).
```

**Issue:** Long sentence with comma-separated list items.

**Recommendation:** Consider reformatting as a bulleted list for readability.

---

### 6. Implicit Bulleted Structure (Lines 126)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
For the QuadPlane configuration, the matching chart combines a hover constraint as a horizontal line at $P/W$ = 85.71 W/N (dominates the chart), a cruise constraint as a curve well below hover constraint (cruise power approximately 10× lower), and a stall constraint as a vertical line at maximum allowable wing loading (14.42 N/m²).
```

**Issue:** Long sentence with comma-separated list items.

**Recommendation:** Consider reformatting as a bulleted list for readability.

---

### 7. Implicit Bulleted Paragraphs (Lines 130-140)

**Rule violated:** Use asterisks for bulleted lists (line 46).

**Current:**
```markdown
Hover constraint: Appears as a horizontal line...

Cruise constraint: Appears as a curve with minimum at optimal wing loading...

Stall constraint: Appears as a vertical line at maximum allowable wing loading:

Energy constraint: Manifests as a feasible region boundary...
```

**Issue:** These are formatted as headings followed by descriptions but could be a bulleted list.

**Status:** Acceptable as prose with inline headers. No action required, but consider consistency with other sections.

---

## Summary of Required Fixes

| File | Issue | Priority |
|:-----|:------|:--------:|
| 05_01 | Wrong character "?" → "≥" (line 213) | HIGH |
| 05_01 | Wrong characters "?" → "×" (line 218) | HIGH |
| 05_01 | Colon without following list (line 220) | LOW |
| 05_03 | Em-dash usage (line 277) | MEDIUM |
| 05_03 | Inconsistent significant figures (line 113) | LOW |
| 05_03 | List formatted as paragraphs (lines 169-177, 273-281) | MEDIUM |
| 05_04 | Wrong character "?" → "≥" (line 16) | HIGH |

**HIGH priority:** Corrupted Unicode characters that affect document readability.
**MEDIUM priority:** Style rule violations that affect consistency.
**LOW priority:** Minor formatting improvements.

---

## Recommended Actions

1. **Fix corrupted Unicode characters** in lines 213, 218 of `05_01` and line 16 of `05_04`.
2. **Replace em-dashes** with commas in `05_03` line 277.
3. **Convert implicit lists** to proper tight bulleted lists where appropriate.
4. **Verify 4 significant figures** in all numerical results.
5. **Run `reconstruct.bat`** after fixes to rebuild the manuscript.
6. **Run `build_docx.bat`** to verify Word output renders correctly.
