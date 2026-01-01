<!-- 
  CANONICAL SOURCE: This file (AGENTS.md) is the single source of truth.
  SYNCHRONIZED COPIES: GEMINI.md and CLAUDE.md must be identical.
  
  TO UPDATE: Edit only AGENTS.md, then run sync_agent_rules.bat to propagate changes.
  
  DO NOT edit GEMINI.md or CLAUDE.md directly - changes will be overwritten.
-->

# Mars UAV Feasibility Study - Project Instructions

## Project Overview

This project develops a comprehensive feasibility study for a Mars UAV operating from a crewed habitat. The study focuses on a single configuration: a **battery-only QuadPlane design (10 kg MTOW)** optimized for simplicity and reliability.

### Mission Objectives
1. **Mapping**: Aerial reconnaissance and geological survey of the area around the habitat (camera payload)
2. **Telecommunication relay**: Extend communication range for surface operations (radio payload)

### Key Files
- **Main manuscript**: `drone.md` (English), `drone_it.md` (Italian)
- **Document structure**: `docs/document_structure.md` ★ (authoritative reference)
- **Implementation plan**: `docs/mars_UAV_plan.md`
- **Bibliography**: `Mars_UAV.bib` (auto-updated from Zotero)
- **Source attribution**: `sources/*.sources.yaml` (precision citation system)
- **Attribution design**: `docs/source_attribution_design.md` ★
- **Python sizing tools**: `src/mars_uav_sizing/`

---

## Browsing

Do not use browsing automation, it is too slow. Use more efficient tool if you need to search information on the web.

---

## Document Editing Tools

This project is edited with the aid of **markdown_tools**, a reusable toolkit for managing technical documents in Markdown. The toolkit is accessed using the batch script in the root dir:

### Key Scripts
| Script | Purpose |
|--------|---------|
| `split.bat` | Split document into sections for editing |
| `reconstruct.bat` | Reconstruct document from sections (with auto-backup) |
| `build_docx.bat` | Build DOCX output via Pandoc |

### Workflow
1. Edit sections in `sections_en/` (English) or `sections_it/` (Italian)
2. Run `reconstruct.bat` to rebuild the main document
3. Run `build_docx.bat` to generate DOCX output

### Configuration
- `config.yaml`: Project-specific settings
- `docx.defaults.en.yaml` / `docx.defaults.it.yaml`: Pandoc settings per language
- `reference.docx`: Word template for styling

---

## Reference Handling (CRITICAL)

### Universal Data Verification & Attribution Protocol (CRITICAL)
**This protocol MUST be followed for EVERY single piece of information (fact, number, claim, equation, or parameter) entered into the project.**

**The Workflow Loop:**
For every distinct piece of information:

1.  **Verification (Primary Source Rule)**:
    - Do not be satisfied at first by data at face value from secondary sources (e.g., aggregators, review sites, integrators listing sub-components).
    - **Trace to the Source**: You MUST try to find the original, primary source.
        *   *Example*: For a drone's motor efficiency, go to the motor manufacturer's official datasheet.
        *   *Example*: For Mars gravity, search a standard astronomical reference or NASA fact sheet, not a random blog.
    - If a primary source cannot be found, then you can rely on secondary sources (e.g., aggregators, review sites, integrators listing sub-components) if they are authoritative.
    - If no authoritative source is found, then data is **UNVERIFIED** and must NOT be used.

2.  **Search Protocol**:
    - Follow the strict **Reference Search Order** (below) to locate this primary source.

3.  **Registration (Zotero)**:
    - Once the primary source is found, immediately add it to the **Mars_UAV** Zotero collection.
    - **MANDATORY**: You must populate valid metadata (Author, Title, Date, URL).
    - **Verification**: Check `Mars_UAV.bib` to confirm the key exists.

4.  **Attribution (Inline Locator + YAML Sidecar)**:
    - Add an **inline locator tag** after the citation: `[@key]<!-- #loc -->`
    - Add a matching entry in `sources/{section}.sources.yaml`
    - See `docs/source_attribution_design.md` for full specification

**Strict Prohibition**:
- NEVER invent or guess data.
- NEVER use a citation key that is not in `Mars_UAV.bib`.
- NEVER skip the source attribution step.

### Reference Search Order
When a reference is needed, search in this order:

1. **Zotero Mars_UAV collection** (primary)
   - Use the Zotero MCP tools to search: `zotero_search_items`, `zotero_semantic_search`
   - Collection name: `Mars_UAV`

2. **Full Zotero library** (secondary)
   - If not found in Mars_UAV, search the entire library
   - Remember you can also rely on the semantic full-text database

3. **Web search** (tertiary)
   - If no suitable reference exists in Zotero, search the web
   - Prefer peer-reviewed sources, NASA technical reports, textbooks

### Bypassing Anti-Bot Protections (Jina Reader)
When a website blocks automated access (returns 403 Forbidden or requires CAPTCHA), use **Jina Reader** as a proxy:
- Prefix the URL with `https://r.jina.ai/`
- Example: `https://r.jina.ai/https://www.example.com/product-page`
- This converts the page to clean, LLM-friendly markdown
- Works for most e-commerce and product specification pages
- **Much faster than browser automation**

### Adding New References
If a newly found source is not already in the Mars_UAV Zotero collection:
1. Add it to the Mars_UAV collection in Zotero
2. The **Better BibTeX plugin** will automatically update `Mars_UAV.bib`
3. The updated .bib file will be available for citations

### Citation Key Verification (CRITICAL)
**NEVER use a citation key without first verifying it exists in `Mars_UAV.bib`.**

Before adding any citation to the manuscript:
1. Read `Mars_UAV.bib` to get the exact citation keys
2. Use the exact key as it appears in the bib file (keys are case-sensitive and format-specific)
3. Do NOT guess or hallucinate citation keys based on author/year patterns

Common errors to avoid:
- Guessing keys like `@author2022Title` when the actual key is `@authorTitleWord2022`
- Using authors not in the bib file (e.g., citing "Lorenz 2022" when no Lorenz entry exists)
- Mixing up similar-sounding references

If a needed reference is not in the bib file, **do not cite it**. Instead:
1. Note that a reference is needed
2. Start the search as prescribed in ### Reference Search Order
3. Add it to Zotero Mars_UAV collection if found
4. Wait for the bib file to update before citing

### Source Attribution System

The project uses a **precision citation system** with inline locator tags and YAML sidecar files. See `docs/source_attribution_design.md` for the complete specification.

**Key Concepts**:
- Each citation gets a **locator tag**: `[@key]<!-- #loc -->`
- Locators map to entries in `sources/{section}.sources.yaml`
- YAML entries contain searchable excerpts for verification

**Inline Locator Syntax**:
```markdown
The thrust equation [@leishmanPrinciples2006]<!-- #eq2.14 --> states...
```

**YAML Sidecar Entry** (in `sources/05_01.sources.yaml`):
```yaml
leishmanPrinciples2006:
  eq2.14:                          # no hash in YAML key
    excerpt: "T = 2*rho*A*v_i^2"
    context: "Momentum theory thrust equation"
```

**Locator Rules**:
- Inline: uses hash prefix `<!-- #loc -->`
- YAML key: no hash, lowercase only
- Allowed chars: `a-z`, `0-9`, `:`, `.`, `_`, `-`
- Ranges: single dash, e.g., `p12-15`

**Locator Formats by Source Type**:
| Type | Examples |
|------|----------|
| Book | `#ch10`, `#ch10:p584`, `#eq2.14`, `#fig8.3` |
| Article | `#p4`, `#s3`, `#fig2a`, `#tbl1`, `#abs` |
| Report | `#p23`, `#s:rotor-sizing`, `#fig12` |
| Webpage | `#sec:specs`, `#operating-temp` |
| Dataset | `#v1:e387:re61k`, `#file:sd8000.drg` |

**YAML Field Requirements**:
| Field | Required | Limit |
|-------|----------|-------|
| `excerpt` | Yes | ≤100 chars |
| `context` | Yes | ≤80 chars |
| `verified` | No | boolean |
| `note` | No | — |

**Legacy**: The old `source_grounding.txt` is deprecated and will be migrated incrementally.
### Managing Zotero Collection

The Zotero MCP has read-only capabilities. To write information to Zotero, use the Zotero Web API with the following account:
- User ID: 10348042
- Read-write Web API key: s8qR5N0A7GSQxZfkW1NAcmjZ
- Mars_UAV collection key: 2BQEVWT7

### Metadata Validation (CRITICAL)

**Before adding any item to Zotero, verify that the 3 vital metadata fields are complete:**

1. **Authors/Creators** - For webpages, use the company/organization name as author
2. **Title** - Clear, descriptive title of the resource
3. **Date** - Publication or last update date (required for BetterBibTeX citation keys)

**Pre-submission checklist:**
- [ ] Title is complete and descriptive
- [ ] Author/creator field is populated (use organization name for corporate sources)
- [ ] Date field contains a valid date (YYYY-MM-DD or YYYY format)
- [ ] URL is valid and accessible (for webpages)
- [ ] Appropriate tags are added

**For webpages without visible dates:**
- Check the page footer, "last updated" notices, or metadata
- Use the Wayback Machine to find historical snapshots
- If no date can be found, use the access date with a note in the "Extra" field: `original-date: unknown`

**Example API call with complete metadata:**
```json
{
  "itemType": "webpage",
  "title": "Product Name - Specifications",
  "creators": [{"creatorType": "author", "name": "Company Name"}],
  "date": "2024",
  "url": "https://example.com/product",
  "accessDate": "2025-12-21",
  "websiteTitle": "Company Website",
  "collections": ["2BQEVWT7"]
}
```

### Zotero Web API - Complete Workflow (CRITICAL)

The Zotero MCP server provides **read-only** access. To **add or modify** items, you must use the Zotero Web API directly. **Follow this workflow exactly to avoid errors.**

#### API Credentials
```
User ID:        10348042
API Key:        s8qR5N0A7GSQxZfkW1NAcmjZ
Collection Key: 2BQEVWT7 (Mars_UAV collection)
API Endpoint:   https://api.zotero.org/users/10348042/items
```

#### CRITICAL: Use File-Based Approach (Not Inline JSON)

**Problem**: PowerShell and other shells have escaping issues with special characters commonly found in bibliographic data:
- Parentheses `()` - e.g., "(20 MP)"
- Unicode characters - e.g., "μm", "°C", "²"
- Quotes within strings
- Commas in descriptions

**Solution**: Always write JSON to a temporary file first, then read it in the API call.

#### Step-by-Step Workflow

**Step 1: Create a temporary JSON file**

Write the item data to a file (e.g., `temp_zotero_item.json`):

```json
[{
  "itemType": "webpage",
  "title": "DJI Air 2S - Specifications",
  "creators": [{"creatorType": "author", "name": "DJI"}],
  "date": "2021",
  "url": "https://www.dji.com/air-2s/specs",
  "accessDate": "2025-12-22",
  "websiteTitle": "DJI",
  "abstractNote": "Technical specifications for DJI Air 2S drone featuring 1-inch CMOS sensor with 20 MP, 2.4 micrometer pixel size, 8.8 mm focal length.",
  "collections": ["2BQEVWT7"],
  "tags": [{"tag": "camera"}, {"tag": "sensor"}, {"tag": "UAV"}]
}]
```

**Important notes for JSON structure:**
- The payload MUST be a JSON **array** `[{...}]`, even for a single item
- Use `"name"` for corporate authors (single field), not `"firstName"/"lastName"`
- Avoid special Unicode in `abstractNote` if possible; spell out symbols (e.g., "micrometer" instead of "μm")
- The `collections` array takes collection keys, not names

**Step 2: Execute PowerShell API call**

```powershell
$headers = @{
    "Zotero-API-Key" = "s8qR5N0A7GSQxZfkW1NAcmjZ"
    "Content-Type" = "application/json"
}
$body = Get-Content -Path "temp_zotero_item.json" -Raw
Invoke-RestMethod -Uri "https://api.zotero.org/users/10348042/items" -Method Post -Headers $headers -Body $body
```

**Step 3: Verify success and get item key**

A successful response looks like:
```
successful success       unchanged failed
---------- -------       --------- ------
@{0=}      @{0=ABC12345}
```

The item key (e.g., `ABC12345`) is in the `success` column.

**Step 4: Wait for BetterBibTeX sync**

After adding an item:
1. Wait 3-5 seconds for Zotero to sync
2. Check `Mars_UAV.bib` for the new citation key
3. The key format is typically: `authorTitleWord20XX`

```powershell
Start-Sleep -Seconds 5
Get-Content Mars_UAV.bib | Select-String -Pattern "newAuthorName|newTitleWord" -Context 0,5
```

**Step 5: Clean up**

```powershell
Remove-Item temp_zotero_item.json
```

#### Item Types and Required Fields

| Item Type | Required Fields |
|-----------|-----------------|
| `webpage` | title, url, websiteTitle, accessDate, creators, date |
| `journalArticle` | title, publicationTitle, volume, pages, date, creators, DOI |
| `book` | title, publisher, place, date, creators, ISBN |
| `conferencePaper` | title, conferenceName, date, creators |
| `report` | title, institution, reportNumber, date, creators |

#### Common Pitfalls to Avoid

1. **DO NOT** use inline JSON in PowerShell commands - special characters will break parsing
2. **DO NOT** forget the outer array brackets `[...]` around the item
3. **DO NOT** use `firstName`/`lastName` for organizations - use single `name` field
4. **DO NOT** include Unicode symbols in abstractNote - spell them out
5. **DO NOT** cite the new key until you verify it exists in `Mars_UAV.bib`

#### Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `UnexpectedToken` | Special chars in inline JSON | Use file-based approach |
| `400 Bad Request` | Invalid JSON structure | Validate JSON, check array brackets |
| `403 Forbidden` | Wrong API key | Verify API key is correct |
| Key not in .bib | BetterBibTeX not synced | Wait longer, check Zotero is running |
| Wrong citation key format | Missing date field | Ensure date is populated |

#### Adding an Existing Item to Mars_UAV Collection

Sometimes a reference already exists in the Zotero library but is not in the Mars_UAV collection. To add it:

**Step 1: Find the item key**

Use Zotero MCP to search and get the item key:
```
mcp_zotero_zotero_search_items(query="author title keywords")
```
The response includes `Item Key: XXXXXXXX`.

**Step 2: Get current item version**

```powershell
$headers = @{ "Zotero-API-Key" = "s8qR5N0A7GSQxZfkW1NAcmjZ" }
Invoke-RestMethod -Uri "https://api.zotero.org/users/10348042/items/XXXXXXXX" -Method Get -Headers $headers
```

Note the `version` number from the response (e.g., `version: 17184`).

**Step 3: Create PATCH JSON file**

Write to `temp_patch_item.json`:
```json
{
  "collections": ["2BQEVWT7"]
}
```

**Step 4: PATCH the item**

```powershell
$headers = @{
    "Zotero-API-Key" = "s8qR5N0A7GSQxZfkW1NAcmjZ"
    "Content-Type" = "application/json"
    "If-Unmodified-Since-Version" = "17184"  # Use version from Step 2
}
$body = Get-Content -Path "temp_patch_item.json" -Raw
Invoke-RestMethod -Uri "https://api.zotero.org/users/10348042/items/XXXXXXXX" -Method Patch -Headers $headers -Body $body
```

**Step 5: Verify and clean up**

```powershell
Start-Sleep -Seconds 5
Get-Content Mars_UAV.bib | Select-String -Pattern "citationKey" -Context 0,3
Remove-Item temp_patch_item.json
```

**Important notes:**
- The `If-Unmodified-Since-Version` header is required for PATCH requests
- Use the exact version number from the GET response
- The `collections` array in the PATCH body **replaces** existing collections; if you want to **add** to existing collections, include all collection keys
- A successful PATCH returns no output (empty response with 204 status)

---

## Document Structure

**See `docs/document_structure.md` for the authoritative, up-to-date document structure.**

The document structure file contains:
- Current manuscript organization (sections and subsections)
- Key design parameters with current values
- Section completion status
- Cross-reference labels
- Recent changes log

---

## Design Methodology

The design follows an iterative process:

### Phase 1: Reference Case Study
- Collect existing Mars UAV designs from literature
- Extract parameters: MTOW, weight fractions, disk loading, wing parameters
- Formulate initial hypotheses for matching chart

### Phase 2: Preliminary Sizing
- Run matching chart with initial guesses
- Obtain: wing area, span, power requirements, mass breakdown

### Phase 3: Component Selection
- Use preliminary sizing to select actual components from datasheets
- Categories: propulsion, energy, payload, avionics, thermal

### Phase 4: Verification
- Recalculate with selected component data
- Verify requirements compliance

---

## Technical Notes

### Airfoil Selection (Updated 2025-12-31)
- **Selected airfoil**: SD8000 (replaced E387)
- **Selection rationale**: Larger stall margin (4.6° vs 1.3°), consistent drag behavior without LSB transitions
- **Key parameters**: CL_max = 1.15, t/c = 8.9%, Cd_min = 0.0142
- **XFOIL does not converge** at Reynolds ~50,000 due to laminar separation bubbles
- Use **Selig wind tunnel data** from "Summary of Low-Speed Airfoil Data" instead

### Key Design Parameters (Current Baseline)
- Baseline MTOW: 10.00 kg
- Wing loading: 13.82 N/m²
- Wing area: 2.686 m²
- Wingspan: 4.01 m
- Cruise speed: 40.0 m/s
- Reynolds number: ~55,000
- Operating location: Arcadia Planitia (-3 km elevation)
- Atmospheric density: 0.0196 kg/m³

---

## Style Guidelines

obey to C:\Users\matti\OneDrivePhD\Dev\Drone_marte\docs\style_rules.txt. Here is a summary:
- UTF-8 encoding for all files
- Sentence case headings
- Asterisks (*) for bullet lists, tight (no blank lines between items)
- Cross-references: `@fig:`, `@tbl:`, `@eq:`
- Implicit citations only: `[@author2024]`
- Third-person objective voice
- No subjective adjectives (crucial, innovative, etc.)
- LaTeX for complex math, Unicode for simple symbols (×, ², °, etc.)
- **Subscripts/superscripts in running text**: Use LaTeX inline math syntax (`$T_\text{ref}$`, `$C_L$`) instead of plain underscore (`T_ref`, `C_L`) for proper Word rendering

---

## Python Environment

- Python 3.11
- Package manager: uv (preferred over pip)
- Package location: `src/mars_uav_sizing/`
- Modern /src layout structure

### Key Modules
| Module | Purpose |
|--------|---------|
| `atmosphere.py` | Mars atmospheric model |
| `aerodynamics.py` | Drag polar, L/D calculations |
| `airfoil_data.py` | Selig wind tunnel data |
| `constraints.py` | Matching chart equations |
| `weights.py` | Weight estimation |
| `endurance.py` | Battery energy calculations |
| `plotting.py` | Visualization |
| `run_sizing.py` | Main entry point |

---

## Structured Data Formats

### Preferred Format: YAML over CSV

When storing tabular or structured data (e.g., drone specifications, component databases), **prefer YAML over CSV**. CSV is prone to errors when manipulated by LLMs due to:
- Column misalignment from inconsistent delimiter handling
- Escaping issues with commas in values
- No schema enforcement or data type hints
- Difficult to read/edit for complex nested data

**YAML advantages:**
- Human-readable and LLM-friendly
- Self-documenting with comments
- Supports nested structures naturally
- Each record is self-contained (no column alignment issues)
- Built-in support for lists, dictionaries, and mixed types
- Easy to parse programmatically (Python `yaml.safe_load()`)

### Example: Drone Specifications in YAML

Instead of `Tab_droni_completed.csv`, use `reference_drones.yaml`:

```yaml
# Reference UAV Database for Mars UAV Feasibility Study
# Source grounding: see source_grounding.txt for attribution

reference_drones:
  - name: AirMobi V25
    source_url: https://www.airmobi.com/product/airmobi-v25-full-electric-vtol-drone/
    source_key: "@airmobiAirmobiV25Full2024"
    
    # Mass properties
    mass:
      empty_kg: 3.45
      mtow_kg: 14
      payload_max_kg: 2.5
    
    # Geometry
    geometry:
      wingspan_m: 2.5
      fuselage_length_m: 1.26
      n_rotors: 5
    
    # Performance
    performance:
      v_max_ms: 34
      v_cruise_ms: 20
      endurance_min: 180  # at 2kg payload
      range_km: 140
    
    # Propulsion
    propulsion:
      lift_motor:
        model: MN505-S KV260
        manufacturer: T-Motor
        power_w: 2500
        weight_kg: 0.225
      cruise_motor:
        model: AT4130 KV230
        manufacturer: T-Motor
        power_w: 2500
        weight_kg: 0.408
      propeller_lift_in: "16-17"
      propeller_cruise_in: "15-18"
    
    # Battery
    battery:
      technology: HV LiPo
      manufacturer: Tattu
      model: 6S 25000mAh HV
      count: 2
      total_mass_kg: 5.05
      total_capacity_mah: 50000
      operating_temp_c: "-20 to 45"
      source_key: "@gensace/tattuTattu25000mAh228V2024"

  - name: RTV320 E
    source_url: https://www.uavfordrone.com/product/...
    # ... (similar structure)
```

### Conversion Script

To convert existing CSV to YAML, use:
```python
import csv
import yaml

def csv_to_yaml(csv_path, yaml_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        drones = [dict(row) for row in reader]
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump({'reference_drones': drones}, f, 
                  default_flow_style=False, allow_unicode=True)
```

