# Manuscript Corrections Plan - Progress Tracker

## Overview
This document tracks the comprehensive corrections requested for sections 1-4 of the Mars UAV manuscript.

## Task Status Legend
- [ ] Not started
- [x] Completed
- [~] In progress

---

## Phase 1: Style Rules Application (Sections 1-4)

### Completed Style Improvements
- [x] Removed uncertainty phrases (±0.05, ±0.1 etc.) throughout
- [x] Converted lists to prose in multiple sections
- [x] Fixed citation format issues (removed "[40, Ch. 10]" style)
- [x] Used proper Unicode characters (−, ×, °, etc.)

---

## Phase 2: Section 2 Restructuring

### Completed
- [x] Fixed forward reference in section 2.1 ("previous section" → @sec:reference-data)
- [x] Updated MTOW from 3.3 kg to 10 kg in section 2.2
- [x] Updated battery fraction from 35% to 40% in section 2.2
- [x] Removed orphan subsection header in 2.2 (content merged into main section)

### Deferred
- [ ] Integrate 5.5.4 content into 2.2 (matching chart methodology is now complete in 5.5)

---

## Phase 3: Section 3 - User Needs

### Already Complete
Section 3.3 was previously restructured per ECSS guidelines. User needs are expressed qualitatively as required; quantitative requirements are in Section 4.12.

---

## Phase 4: Section 4 Corrections - ALL COMPLETE

### 4.1.1 - Camera Systems
- [x] Added camera dimension analysis (verified from sources)
- [x] Rewrote mass range summary in prose form
- [x] Rewrote Mars thermal considerations in prose form
- [x] Updated source_grounding.txt with dimension entries

### 4.1.2 - Radio Systems
- [x] Added radio dimension analysis (verified from sources)
- [x] Fixed temperature error (−40 to −40 °C → proper range)
- [x] Rewrote mass range summary in prose form
- [x] Rewrote Mars environment considerations in prose form
- [x] Updated source_grounding.txt with dimension entries

### 4.2.3.1 - Fuselage-mounted Configurations
- [x] Added prose introduction before list

### 4.2.3 - Structural Materials
- [x] Converted list to prose form

### 4.5 - Propulsion Table
- [x] Added motor masses to propulsion specifications table
- [x] Converted comparison list to prose form

### 4.5.1 - Propulsion Efficiency
- [x] Converted bolded titles to fourth-level subsections
- [x] Fixed FM from 0.50 to 0.40 (range 0.30-0.50 per Leishman)
- [x] Added citations for propeller efficiency (Sadraey 2020)
- [x] Added citations for motor and ESC efficiency (Sadraey 2020)
- [x] Completed efficiency parameters table with references
- [x] Updated combined efficiency calculations (hover ~32%, cruise ~44%)

### 4.7.1 - Reynolds Number
- [x] Removed claim about "wing chord sized to Re=60,000"
- [x] Added justification for 60,000 Re target (viscous effects, power trade-offs)
- [x] Explained Re choice as compromise between aero performance and geometry/power
- [x] Moved numerical calculation to 4.12.5.1

### 4.7.2 - Airfoil Data
- [x] Rewrote airfoil list in prose form
- [x] Added note that design selection deferred to section 6.2

### 4.7.3.2 - Zero-lift Drag
- [x] Rewrote list in prose form

### 4.7 - Drag Polar Updates for AR=6
- [x] Updated Oswald efficiency table (AR 5-7 instead of 10-14)
- [x] Updated e from 0.75 to 0.82 for AR=6
- [x] Updated drag polar equation for AR=6
- [x] Updated (L/D)max from 15.3 to 11.7
- [x] Updated optimal CL from 0.92 to 0.68
- [x] Updated summary table

### 4.11.3-4.11.5 - Mass Fractions (CRITICAL)
- [x] Changed payload fraction: 0.10 (conservative)
- [x] Changed propulsion fraction: 0.20 (redundancy)
- [x] Changed empty weight fraction: 0.30
- [x] Verified sum = 1.0
- [x] Updated paragraph 4.11.5 to reflect changes
- [x] Set payload mass to 1 kg (camera 400g + radio 170g + margin)
- [x] Calculated new target MTOW = 10 kg
- [x] Updated sensitivity table

### 4.12.4.1 - Aspect Ratio
- [x] Changed AR range from 10-14 to 5-7
- [x] Set baseline AR = 6
- [x] Removed unsupported claim about "AR below 10 = unacceptable drag"
- [x] Justified decision with Earth UAV data (4-12) and Mars precedents (5-6)

### 4.12.4.2 - Thickness Ratio
- [x] Clarified this is t/c selection, not airfoil selection
- [x] Fixed citation style (removed chapter/section references)
- [x] Set baseline t/c = 0.09
- [x] Deferred airfoil selection to section 6.2

### 4.12.4.3 - Taper Ratio
- [x] Rewrote in proper prose form

### 4.12.4.4 - Sweep Angle
- [x] Fixed citation format
- [x] Rewrote in prose form

### 4.12.5.1 - Cruise Velocity
- [x] Removed claim about "Re must match experimental data"
- [x] Started from Mach number justification (M ≈ 0.17, target band 0.16-0.28)
- [x] Explained compressibility considerations (well below M = 0.3)
- [x] Showed Re = 60,000 derivation with c = 0.78 m, V = 40 m/s
- [x] Used AR = 6 for calculations
- [x] Recalculated S = 3.6 m² for AR=6
- [x] Updated chord/velocity table for AR=6

### 4.12.5.2 - Minimum Velocity
- [x] Revised V_min with corrected W/S = 10 N/m²
- [x] Calculated V_stall ≈ 20 m/s, V_min ≈ 24 m/s
- [x] Noted comfortable margin above stall for manoeuvring

### 4.12.5.3 - Hover Time
- [x] Rewrote in prose form

### 4.12.5.4 - Cruise Endurance
- [x] Removed headwind margin
- [x] Set t_cruise = 57 min (per summary table)

### 4.12.5.5 - Energy Reserve
- [x] Converted list to prose form

### 4.12.6 - Summary Table
- [x] Changed "Design practice" to "Safety margin" (M6)
- [x] Updated payload mass: 1.0 kg
- [x] Updated AR: 6
- [x] Updated t/c: 0.09
- [x] Updated FM: 0.40
- [x] Updated Oswald efficiency: 0.82

---

## Phase 5: Section 5+ Cascading Effects (OUT OF SCOPE)

The following files still contain old parameter values and will need updating when sections 5+ are revised:

### Files with old MTOW = 3.3 kg:
- 05_02_rotorcraft-analysis.md (line 203)
- 05_03_fixed-wing-analysis.md (line 155)
- 05_04_hybrid-vtol-analysis.md (lines 86, 139, 195, 285)
- 06_01_architecture-selection.md (line 123)
- 06_05_mass-breakdown.md (line 111)

### Files with old AR = 12:
- 05_03_fixed-wing-analysis.md (line 81)
- 06_01_architecture-selection.md (line 125)

### Already Updated in Section 5:
- [x] 05_05_comparative-results.md - Updated design point tables for MTOW=10 kg, AR=6

---

## Build Status
- Document reconstructed successfully
- No build errors reported

---

## Summary of Key Value Changes Applied

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| MTOW | 3.3 kg | 10 kg | 1 kg payload / 0.10 fraction |
| Payload mass | 0.5 kg | 1.0 kg | Camera + radio + margin |
| Payload fraction | 0.15 | 0.10 | Conservative |
| Propulsion fraction | 0.15 | 0.20 | Redundancy |
| Empty fraction | 0.45 | 0.30 | Revised estimate |
| Battery fraction | 0.25 | 0.35 | High endurance requirement |
| Avionics fraction | — | 0.05 | Standard estimate |
| Aspect ratio | 12 | 6 | Mars UAV precedents |
| Oswald efficiency | 0.75 | 0.82 | For AR=6 |
| Figure of Merit | 0.50 | 0.40 | Leishman 0.30-0.50 range |
| (L/D)max | 15.3 | 11.7 | Recalculated for AR=6 |
| Wing area | 0.72 m² | 2.2 m² | From matching chart |
| Wingspan | 2.9 m | 3.6 m | √(AR × S) |
| Chord | 0.25 m | 0.61 m | S/b |
| V_stall | ~34.6 m/s | ~20 m/s | New W/S |
| V_min | ~41.5 m/s | ~24 m/s | 1.2 × V_stall |
| t_cruise | 65+/75 min | 57 min | No headwind margin |
| η_hover | 0.40 | 0.32 | FM=0.40 |
| Hover power | 812 W | 2460 W | For 10 kg MTOW |
| Cruise power | 90 W | 270 W | For 10 kg MTOW |
