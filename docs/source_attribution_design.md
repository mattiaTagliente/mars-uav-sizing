# Source Attribution System Design

**Version**: 1.1  
**Date**: 2026-01-01  
**Status**: Approved for Implementation

## Overview

This document specifies a precision citation system that enables traceability from any claim in the manuscript to the exact location in the primary source. The system replaces the monolithic `source_grounding.txt` file with a distributed, token-efficient architecture.

**Key principle**: No claim text is duplicated in YAML. The locator is the primary link between the manuscript and the sidecar entry.

---

## Architecture

### Components

```
Drone_marte/
├── sections_en/                    # English manuscript sections
│   └── *.md                        # Contains inline locator tags
├── sections_it/                    # Italian manuscript sections  
│   └── *.md                        # Same locator tags as EN
├── sources/                        # Sidecar directory (language-independent)
│   ├── 04_07.sources.yaml          # Section-specific attribution
│   ├── 05_01.sources.yaml
│   ├── 05_02.sources.yaml
│   └── ...
└── Mars_UAV.bib                    # Bibliography (unchanged)
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MANUSCRIPT                                     │
│  "The thrust equation [@leishmanPrinciples2006]<!-- #eq2.14 --> states" │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
              ┌─────────────────────┴────────────────────┐
              │                                          │
              ▼                                          ▼
┌──────────────────────────┐              ┌──────────────────────────────┐
│     Mars_UAV.bib         │              │  sources/05_01.sources.yaml  │
│  (Full bibliographic     │              │                              │
│   metadata)              │              │  leishmanPrinciples2006:     │
│                          │              │    eq2.14:      ← no hash    │
│  @book{leishmanPrinci... │              │      excerpt: "T = 2ρAv_i²"  │
│    author = {...},       │              │      context: "momentum..."  │
│    title = {...},        │              │                              │
│  }                       │              └──────────────────────────────┘
└──────────────────────────┘
```

---

## Inline Locator Tag Specification

### Syntax

```
[@citationKey]<!-- #locator -->
```

- **`[@citationKey]`**: Standard Pandoc citation (linked to Mars_UAV.bib)
- **`<!-- #locator -->`**: HTML comment containing the unique locator ID with hash prefix

### Locator Normalization

| Rule | Description |
|------|-------------|
| **Inline format** | Uses hash prefix: `<!-- #loc -->` |
| **YAML key format** | Omits hash prefix: `loc:` |
| **Case** | Locators are **lowercase** in both inline and YAML |
| **Lookup** | Parsers strip leading `#` when matching inline to YAML |

### Allowed Characters

Locator tokens use only:
- Lowercase letters: `a-z`
- Digits: `0-9`
- Separators: `:` `.` `_` `-`

**Prohibited**:
- Spaces
- Uppercase letters
- The sequence `--` (invalid HTML comment syntax)

### Parser Tolerance

Parsers should accept optional whitespace before the HTML comment:
- `[@key]<!-- #loc -->` ✓ (canonical)
- `[@key] <!-- #loc -->` ✓ (also valid)

### Range Notation

Ranges are expressed with a single dash inside the token:
- `<!-- #p12-15 -->` → pages 12 through 15
- `<!-- #tbl3:r2-5 -->` → table 3, rows 2 through 5

A range refers to a single contiguous location and maps to one YAML entry.

### Rules

1. **Hash prefix** (`#`) is mandatory in inline locators
2. **Locator uniqueness**: Within a given citation key in each sidecar file, each locator must be unique
3. **Same locator = same source location**: If `[@key]<!-- #loc -->` appears in multiple sections, all instances refer to the same source location

### Compound Citations

For citations with multiple sources, split into separate citations with individual tags:

```markdown
Based on experimental data [@seligSummary1995]<!-- #v1:e387 --> and 
theoretical analysis [@torenbeekSynthesis1982]<!-- #ch5:eq5.12 -->.
```

**Not** this (ambiguous):
```markdown
<!-- ❌ WRONG -->
[@seligSummary1995; @torenbeekSynthesis1982]<!-- #??? -->
```

---

## Locator Format by Source Type

All examples use lowercase as required.

### Books and Textbooks

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#ch{n}` | Chapter n | `<!-- #ch10 -->` |
| `#ch{n}:p{m}` | Chapter n, page m | `<!-- #ch10:p584 -->` |
| `#ch{n}:p{m}-{k}` | Chapter n, pages m–k | `<!-- #ch10:p584-590 -->` |
| `#ch{n}:s{x}` | Chapter n, section x | `<!-- #ch5:s3.2 -->` |
| `#eq{x}` | Equation number x | `<!-- #eq2.14 -->` |
| `#fig{n}` | Figure n | `<!-- #fig8.3 -->` |
| `#tbl{n}` | Table n | `<!-- #tbl4.2 -->` |
| `#app{x}:p{m}` | Appendix x, page m | `<!-- #appa:p312 -->` |

### Journal Articles / Conference Papers

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#p{n}` | Page n | `<!-- #p4 -->` |
| `#p{n}-{m}` | Pages n–m | `<!-- #p4-7 -->` |
| `#s{n}` | Section n | `<!-- #s3 -->` |
| `#s{n}:p{m}` | Section n, paragraph m | `<!-- #s4:p2 -->` |
| `#fig{n}` | Figure n | `<!-- #fig2a -->` |
| `#tbl{n}` | Table n | `<!-- #tbl1 -->` |
| `#tbl{n}:r{m}` | Table n, row m | `<!-- #tbl3:r5 -->` |
| `#tbl{n}:r{m}-{k}` | Table n, rows m–k | `<!-- #tbl3:r2-5 -->` |
| `#abs` | Abstract | `<!-- #abs -->` |

### Technical Reports (NASA, etc.)

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#p{n}` | Page n | `<!-- #p23 -->` |
| `#s:{name}` | Named section | `<!-- #s:rotor-sizing -->` |
| `#fig{n}` | Figure n | `<!-- #fig12 -->` |

### Webpages

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#sec:{name}` | Named section | `<!-- #sec:specs -->` |
| `#{anchor}` | HTML anchor ID | `<!-- #operating-temperature -->` |
| `#tbl:{name}` | Named table | `<!-- #tbl:dimensions -->` |

### Datasets / Data Files

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#file:{name}` | Specific file | `<!-- #file:e387a.drg -->` |
| `#v{n}:{file}` | Volume n, file | `<!-- #v1:sd8000 -->` |
| `#v{n}:{file}:re{k}` | Volume, file, Re number | `<!-- #v1:e387:re61k -->` |

### Theses / Dissertations

| Pattern | Meaning | Example |
|---------|---------|---------|
| `#ch{n}:s{x}` | Chapter n, section x | `<!-- #ch4:s2.3 -->` |
| `#exec` | Executive summary | `<!-- #exec -->` |
| `#p{n}` | Page n | `<!-- #p87 -->` |

---

## YAML Sidecar Specification

### File Naming

```
sources/{section_number}.sources.yaml
```

Examples:
- `sources/04_07.sources.yaml` (Aerodynamic analysis)
- `sources/05_01.sources.yaml` (Rotorcraft configuration)
- `sources/05_03.sources.yaml` (Hybrid VTOL configuration)

### File Structure

```yaml
# sources/05_01.sources.yaml
# Source attribution data for Section 5.1: Rotorcraft configuration
# Language-independent (shared by EN and IT manuscripts)

# Format:
# citationKey:
#   locator:                        ← no hash prefix in YAML keys
#     excerpt: "Direct quote or formula from source"
#     context: "Brief explanation of what this proves/supports"

leishmanPrinciplesHelicopterAerodynamics2006:
  eq2.14:                           # ← lowercase, no hash
    excerpt: "T = 2ρA v_i (2v_i) = 2ρA v_i²"
    context: "Momentum theory thrust equation for hovering rotor"
  
  eq2.15:
    excerpt: "v_i = √(T / 2ρA)"
    context: "Induced velocity derived from thrust and disk area"
  
  s2.8:
    excerpt: "FM = P_ideal / P_actual"
    context: "Figure of merit definition"
  
  ch5:s4:
    excerpt: "Forward flight power = induced + profile + parasite + climb"
    context: "Power breakdown for rotorcraft in forward flight"

proutyHelicopterPerformanceStability2002:
  ch4:p112:
    excerpt: "Effective L/D for helicopters: 3.5 to 5.0 in cruise"
    context: "Rotorcraft equivalent L/D including propulsive efficiency"

johnsonMarsScienceHelicopter2020:
  p4:
    excerpt: "P = κT√(T/2ρA) + ρA_bV_tip³(1/8)c_d,mean"
    context: "MSH rotor power equation with induced and profile terms"
  
  abs:
    excerpt: "31 kg hexacopter, ~3.3 kW hover power"
    context: "Final MSH design parameters"
```

### Field Definitions

| Field | Required | Description | Limit |
|-------|----------|-------------|-------|
| `excerpt` | **Yes** | Direct quote, formula, or value from source. Must be searchable. | ≤100 chars |
| `context` | **Yes** | What this data point proves or supports in the manuscript. | ≤80 chars |
| `verified` | No | Set to `true` after manual verification. Default: unverified. | — |
| `note` | No | Additional disambiguation when locator label is necessarily short. | — |

### Validation Checks

1. Each `[@key]<!-- #loc -->` in a section **must** have a matching entry in that section's sidecar
2. Locator uniqueness is enforced per citation key within each sidecar file
3. `excerpt` length (≤100 chars) and `context` length (≤80 chars) limits are enforced

---

## Workflow

### Adding a New Citation

1. **Find the source** using Zotero MCP or web search
2. **Add to Zotero** Mars_UAV collection (if not already present)
3. **Verify citation key** exists in `Mars_UAV.bib`
4. **Insert citation** in manuscript with locator tag (lowercase, hash prefix):
   ```markdown
   The value is 0.87 for AR=6 [@sadraeyAircraftDesign2013]<!-- #ch10:eq10.9 -->
   ```
5. **Add entry** to appropriate sidecar file (lowercase, no hash):
   ```yaml
   sadraeyAircraftDesign2013:
     ch10:eq10.9:
       excerpt: "e = 1.78(1 - 0.045×AR^0.68) - 0.64"
       context: "Oswald efficiency correlation for straight wings"
   ```

### Verifying an Existing Citation

1. **Locate the citation** in manuscript: `[@key]<!-- #loc -->`
2. **Look up** `key` → `loc` in `sources/{section}.sources.yaml`
3. **Search source** using excerpt via Zotero semantic search
4. **Compare** source content with manuscript claim
5. **Mark verified** if accurate:
   ```yaml
   ch10:eq10.9:
     excerpt: "..."
     context: "..."
     verified: true
   ```

### Handling Italian Translation

Since locator tags are language-independent:
- Both `sections_en/*.md` and `sections_it/*.md` use **identical** locator tags
- **One shared sidecar folder** (`sources/`) serves both languages
- Italian sections reference the same `[@key]<!-- #loc -->` patterns

---

## Migration from source_grounding.txt

### Strategy

1. Parse existing `source_grounding.txt` by section headers
2. For each entry, create:
   - Locator tag for manuscript (if not already present)
   - YAML entry in sidecar file
3. Gradually deprecate `source_grounding.txt`

### Mapping Example

**Before** (in source_grounding.txt):
```
- "E387 CL_max = 1.22 at Re = 61,000"
  Source: [@seligSummaryLowSpeedAirfoil1995]
  Location: Vol. 1, E387A.DRG, tabulated data at Re = 61,000
```

**After**:

In manuscript:
```markdown
| E387 | 61,000 | 1.22 | ... | Vol. 1 |
```
→ At table caption:
```markdown
[@seligSummaryLowSpeedAirfoil1995]<!-- #v1:e387:re61k -->
```

In `sources/04_07.sources.yaml`:
```yaml
seligSummaryLowSpeedAirfoil1995:
  v1:e387:re61k:
    excerpt: "CL_max=1.22, alpha_stall=10.2, ld_max=46.6"
    context: "E387 performance at Re=61,000 from wind tunnel"
```

---

## Validation Tools (Future)

Possible Python scripts for automated validation:

1. **parse_locators.py**: Extract all `[@key]<!-- #loc -->` patterns from manuscripts
2. **check_sidecar.py**: Verify every locator has a YAML entry
3. **verify_excerpts.py**: Use Zotero semantic search to validate excerpts match sources
4. **report_missing.py**: List citations without locator tags

---

## Examples

### Full Section Example

**In** `sections_en/05_02_fixed-wing-configuration.md`:
```markdown
In steady, unaccelerated, level flight, two pairs of forces must be 
in equilibrium [@torenbeekSynthesisSubsonicAirplane1982]<!-- #ch5 -->:

$$L = W$$ {#eq:lift-weight}
$$T = D$$ {#eq:thrust-drag}

The aerodynamic lift force is expressed as 
[@torenbeekSynthesisSubsonicAirplane1982]<!-- #ch5:s3:eq5.8 -->:

$$L = \frac{1}{2} \rho V^2 S C_L$$ {#eq:lift-equation}
```

**In** `sources/05_02.sources.yaml`:
```yaml
torenbeekSynthesisSubsonicAirplane1982:
  ch5:
    excerpt: "L = W, T = D in steady level flight"
    context: "Force equilibrium conditions for cruise"
  
  ch5:s3:eq5.8:
    excerpt: "L = 0.5*rho*V^2*S*C_L"
    context: "Standard lift equation definition"
```

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-01 | 1.0 | Initial specification |
| 2026-01-01 | 1.1 | Integrated refinements: locator normalization (hash in inline, no hash in YAML), case normalization (lowercase), allowed characters, range notation, parser tolerance, validation checks, character limits |
