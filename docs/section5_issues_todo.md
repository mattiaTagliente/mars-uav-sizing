# Section 5 (Constraint Analysis) - Issues To-Do List

**Date:** 2025-12-29  
**Status:** ✅ COMPLETED - All fixes implemented  

This document lists all issues identified in Section 5 of the manuscript, organised by category.

**Principles:**
- Section 4 contains INPUTS for constraint analysis (equations, parameter values)
- Section 5 contains the ANALYSIS (applying equations with specific values → results)
- Section 6 contains the SELECTION (choosing architecture based on Section 5 comparison)
- Use 4 significant figures for all numerical results
- Do not reference Python scripts; use their results directly

---

## CONCEPTUAL FIX (2025-12-29)

An initial error was made when consolidating information: application-specific conclusions were incorrectly placed in Section 4. These have been corrected:

**Removed from Section 4.5 (Disk Loading):**
- Rotor size calculation for 10 kg MTOW (moved to Section 5)
- QuadPlane-specific conclusions ("compatible with QuadPlane configuration")
- "Limited hover duration (3 min)" reference (this is a Section 5/6 conclusion)

**Removed from Section 4.6 (Battery):**
- Numerical result @eq:energy-per-kg and "E_available = 718.2 Wh for 10 kg"
- These numerical calculations now appear in Section 5

Section 4 now contains only the *equation* @eq:battery-energy-fraction and parameter definitions. The numerical application appears in each Section 5 configuration analysis.

---

## 1. REDUNDANCIES WITH SECTION 4 ✅ ALL COMPLETED

### 1.1–1.10: All redundancy issues resolved

- FM justification → references @sec:propulsion-efficiency
- @tbl:rotorcraft-ld → moved to Section 4.5
- @eq:battery-energy-fraction → in Section 4.6 (equation only, no numerical results)
- Duplicate equations removed, replaced with references

---

## 2. STYLE RULE VIOLATIONS ✅ ALL COMPLETED

- All 17 bullet/numbered lists converted to prose
- Checkmark symbol removed from Section 5.3

---

## 3. SOURCE GROUNDING ✅ COMPLETED

Added comprehensive Section 5 source grounding entries to `source_grounding.txt`:
- All calculated values documented with derivation steps
- Inputs traced to Section 4 parameters
- External references cited where applicable

---

## 4. NUMERICAL CONSISTENCY ✅ COMPLETED

All values standardised to 4 significant figures.

---

## 5. CROSS-REFERENCE VERIFICATION ✅ COMPLETED

- Fixed @eq:energy-available → @eq:battery-energy-fraction

---

## 6. VALIDATION CHECKLIST

- [x] Run `reconstruct.bat` to rebuild manuscript ✅
- [ ] Run `build_docx.bat` to verify no cross-reference warnings (pending file unlock)
- [x] Source grounding updated for Section 5 ✅
- [x] All equations reference Section 4 or have citations ✅
- [x] No duplicate equations remain ✅
- [x] All numerical values use 4 significant figures ✅
- [x] No ✓/❌ symbols remain ✅
- [x] All major lists converted to prose ✅
- [x] Section 4 contains only inputs, Section 5 contains analysis results ✅
