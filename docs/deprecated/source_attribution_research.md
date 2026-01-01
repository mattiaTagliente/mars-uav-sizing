# Research Report: Alternative Approaches for Source Location Tracking

**Date**: 2026-01-01  
**Status**: Research Complete - Refinement in Progress

## Problem Analysis

The current `source_grounding.txt` file holds **3,610 lines** (~166 KB) as a centralized, monolithic document mapping every claim to its source location. This approach has several issues:

1. **Scalability**: File grows linearly with manuscript content
2. **Maintainability**: Difficult to find specific entries, hard to keep synchronized
3. **Fragility**: A single-file approach creates a single point of failure
4. **Locality**: Source attribution is physically distant from the claims it documents
5. **LLM context burden**: Loading the entire file consumes significant context

---

## Design Alternatives

### **Option A: Section-Local YAML Sidecar Files (Distributed)**

**Concept**: Each manuscript section file gets a companion YAML file storing its source attributions.

**Structure**:
```
sections_en/
├── 04_07_aerodynamic-analysis.md
├── 04_07_aerodynamic-analysis.sources.yaml   ← NEW
├── 05_01_rotorcraft-configuration.md
├── 05_01_rotorcraft-configuration.sources.yaml   ← NEW
...
```

**Example `*.sources.yaml`**:
```yaml
# Source attributions for 04_07_aerodynamic-analysis.md
section: "4.7 Aerodynamic analysis"
claims:
  - claim: "Seven low-Reynolds airfoils were evaluated"
    citation_key: "seligSummaryLowSpeedAirfoil1995"
    location: "Vol. 1, E387A.DRG, SD8000.DRG files"
    line_ref: 14  # Optional: approximate line in parent .md

  - claim: "CL_max = 1.22 for E387 at Re = 61,000"
    citation_key: "seligSummaryLowSpeedAirfoil1995"
    location: "Vol. 1, E387A.DRG, tabulated data"
    line_ref: 22

  - claim: "Equivalent skin friction coefficient Cf_eq = 0.0128"
    citation_key: "gottenFullConfigurationDrag2021"
    location: "Section 4 Results, Table 2"
    line_ref: 66
```

**Pros**:
- **Locality**: Attribution data lives next to the content it documents
- **Granularity**: Each section file is small and manageable (~20-50 entries max)
- **Selective loading**: LLM only loads the relevant sidecar when editing a section
- **Version control**: Git diffs show changes at section level
- **Parallel editing**: Multiple sections can be edited without merge conflicts

**Cons**:
- File proliferation (45+ additional files)
- Must keep section files and sidecar files in sync

---

### **Option B: Inline YAML Frontmatter Annotations**

**Concept**: Embed source attribution metadata directly in each markdown section file using YAML frontmatter or end-matter.

**Example**:
```markdown
---
title: "Aerodynamic analysis and airfoil data"
section_ref: sec:aerodynamic-analysis
source_attributions:
  - claim: "Seven low-Reynolds airfoils were evaluated"
    key: seligSummaryLowSpeedAirfoil1995
    location: "Vol. 1"
  - claim: "Cf_eq = 0.0128 for short-range UAVs"
    key: gottenFullConfigurationDrag2021
    location: "Section 4, Table 2"
---

# Reference data and trade-off analysis

## Aerodynamic analysis and airfoil data {#sec:aerodynamic-analysis}

(... markdown content ...)
```

**Pros**:
- **Single file per section**: Attribution and content co-located
- **No file proliferation**
- **Standard YAML format**: Easy to parse programmatically

**Cons**:
- Bloats markdown files (YAML frontmatter can become very long)
- May interfere with Pandoc processing if not handled correctly
- Harder to maintain: editing prose may accidentally break YAML structure
- **Not compatible with the current split/reconstruct workflow**

---

### **Option C: Extended BibTeX `annote` Field (Reference-Centric)**

**Concept**: Store source location details in the BibTeX file itself, using the `annote` field (or a custom `locations` field).

**Example in `Mars_UAV.bib`**:
```bibtex
@book{seligSummaryLowSpeedAirfoil1995,
  author = {Selig, Michael S. and others},
  title = {Summary of Low-Speed Airfoil Data, Vol. 1},
  year = {1995},
  annote = {
    LOCATIONS:
    - E387 CL_max=1.22: Vol.1, E387A.DRG, line 50
    - SD8000 data: Vol.1, SD8000.DRG, full file
    - Test methodology: Chapter 2, pp. 15-28
  }
}
```

**Pros**:
- **Centralized in bibliography**: All attribution for a source in one place
- **Reference manager compatible**: Zotero can edit `annote` fields
- **Natural grouping**: All uses of a source documented together

**Cons**:
- **Reference-centric, not claim-centric**: Harder to answer "where does this claim come from?"
- **Loses connection to manuscript location**: No link back to which section uses each location
- **BibTeX field limits**: Long annote fields can cause formatting issues

---

### **Option D: Citation-Key Indexed JSON Database (Hybrid)**

**Concept**: A single structured JSON file that maps `[section + claim] → [source + location]`, optimized for machine parsing.

**Structure**:
```json
{
  "04_07": {
    "claims": {
      "airfoil_candidates": {
        "text": "Seven low-Reynolds airfoils were evaluated",
        "citations": [
          {
            "key": "seligSummaryLowSpeedAirfoil1995",
            "location": "Vol. 1, Data files",
            "verified": true
          }
        ]
      },
      "oswald_correlation": {
        "text": "e = 1.78 × (1 - 0.045 × AR^0.68) - 0.64",
        "citations": [
          {
            "key": "sadraeyAircraftDesignSystems2013",
            "location": "Chapter 10, Eq. 10.9, p. 584"
          }
        ]
      }
    }
  },
  "05_01": {
    "claims": { ... }
  }
}
```

**Pros**:
- **Structured and queryable**: Easy to programmatically validate
- **Compact**: JSON is more space-efficient than prose
- **Both directions**: Can look up by section OR by citation key

**Cons**:
- **Still centralized**: Same single-file scalability problem
- **Harder to edit**: JSON editing is error-prone compared to YAML
- **Duplication**: Claim text must be kept in sync with manuscript

---

### **Option E: Inline HTML Comments in Markdown (Invisible Annotations)**

**Concept**: Embed source location information as HTML comments directly after citations in the markdown.

**Example**:
```markdown
The Oswald span efficiency factor accounts for the deviation from ideal elliptical 
lift distribution [@sadraeyAircraftDesignSystems2013]. <!-- LOC: Ch.10, Eq.10.9, p.584 -->

...

Wind tunnel data from the UIUC database provides validated performance 
[@seligSummaryLowSpeedAirfoil1995]. <!-- LOC: Vol.1, E387A.DRG file, Re=61k dataset -->
```

**Pros**:
- **Maximum locality**: Attribution is literally next to the citation
- **Zero file proliferation**: Uses existing files
- **Invisible in output**: HTML comments don't appear in rendered documents
- **Easy to add**: Just append after each `[@key]`

**Cons**:
- **Clutters source files**: Many inline comments may reduce readability
- **Fragile**: Easy to accidentally delete during editing
- **Harder to parse programmatically** (but regex is feasible)
- **No schema enforcement**: Ad-hoc format prone to inconsistency

---

## Initial Recommendation: **Hybrid Approach (Options A + E)**

A **two-tier system**:

### Tier 1: Inline Comment Markers (Lightweight, High-Precision Claims)
For **critical numeric values and equations**, use inline HTML comments:
```markdown
$C_{L,\\text{max}}$ = 1.15 [@seligSummaryLowSpeedAirfoil1995] <!-- LOC: SD8000.DRG, Re=60.8k -->
```

### Tier 2: Section-Local YAML Sidecar Files (Comprehensive Documentation)
For **comprehensive attribution tracking**, each section gets a `*.sources.yaml` companion:
```yaml
# 04_07_aerodynamic-analysis.sources.yaml
claims:
  - id: airfoil-table
    summary: "Performance data for 7 airfoils at Re≈60,000"
    citations:
      - key: seligSummaryLowSpeedAirfoil1995
        location: "Vol.1: E387A.DRG, SD8000.DRG, S7055.DRG, SD7037B.DRG"
      - key: williamsonSummaryLowSpeedAirfoil2012
        location: "Vol.5: AG455ct-02r.DRG, AG12.DRG, AG35-r.DRG"
```

### Benefits of Hybrid:
1. **Inline comments** provide immediate, precise source location next to the data point
2. **YAML sidecars** provide structured, queryable, comprehensive documentation
3. **No single gigantic file** to become unmanageable
4. **Selective loading**: When editing Section 4.7, only load `04_07*.sources.yaml`
5. **Both human and LLM friendly**: YAML is readable; JSON can be generated if needed

---

## Summary Comparison

| Approach | Locality | Scalability | Machine-Readable | Editability | Files Added |
|----------|----------|-------------|------------------|-------------|-------------|
| Current (monolithic txt) | ❌ Poor | ❌ Poor | ⚠️ Partial | ✅ Good | 0 |
| A: YAML sidecars | ✅ Good | ✅ Good | ✅ Excellent | ✅ Good | ~45 |
| B: Inline frontmatter | ✅ Excellent | ⚠️ Medium | ✅ Good | ⚠️ Medium | 0 |
| C: BibTeX annote | ⚠️ Ref-centric | ⚠️ Medium | ⚠️ Partial | ✅ Good | 0 |
| D: JSON database | ❌ Centralized | ⚠️ Medium | ✅ Excellent | ⚠️ Medium | 1 |
| E: Inline comments | ✅ Excellent | ✅ Good | ⚠️ Partial | ⚠️ Medium | 0 |
| **A+E Hybrid** | ✅ Excellent | ✅ Good | ✅ Excellent | ✅ Good | ~45 |

---

## Note

This research report represents the initial analysis. A refined approach based on user feedback is documented separately in `source_attribution_design.md`.
