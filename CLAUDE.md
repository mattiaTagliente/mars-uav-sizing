# Mars UAV Feasibility Study - Project Instructions

## Project Overview

This project develops a comprehensive feasibility study for a Mars UAV operating from a crewed habitat. The study focuses on a single configuration: a **battery-only minimal design (TBD kg MTOW)** optimized for simplicity and reliability.

### Mission Objectives
1. **Mapping**: Aerial reconnaissance and geological survey of the area around the habitat (camera payload)
2. **Telecommunication relay**: Extend communication range for surface operations (radio payload)

### Key Files
- **Main manuscript**: `drone.md` (English)
- **Implementation plan**: `docs/mars_UAV_plan.md`
- **Bibliography**: `Mars_UAV.bib` (auto-updated from Zotero)
- **Source grounding**: `source_grounding.txt` (maps claims to source locations)
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

4.  **Mapping (Source Grounding)**:
    - Immediately update `source_grounding.txt`.
    - Map the specific datum to the specific source key and location (page/table/URL).

**Strict Prohibition**:
- NEVER invent or guess data.
- NEVER use a citation key that is not in `Mars_UAV.bib`.
- NEVER skip the source grounding step.

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

### Source Grounding File
The file `source_grounding.txt` MUST be kept updated after every modification to references. Its purpose is to map every piece of information in the manuscript to the exact location in the sources.

**Format for source_grounding.txt**:
```
## Section: [Section name]

- "[Claim or data point]"
  Source: [@citationKey]
  Location: Page X / Section Y / URL / Table Z

- "[Another claim]"
  Source: [@citationKey]
  Location: Page X, paragraph Y
```

**Example entries**:
```
## Section: Atmospheric model

- "Mars surface pressure: 610 Pa mean"
  Source: [@nasaMarsAtmosphereModel2021]
  Location: https://www.grc.nasa.gov/www/k-12/airplane/atmosmrm.html

- "CO2 ratio of specific heats gamma = 1.29"
  Source: [@desertAerodynamicDesignMartian2017]
  Location: Page 4, Table 1

## Section: Aerodynamic analysis

- "E387 airfoil CL_max = 1.20 at Re = 60,000"
  Source: [@seligSummaryLowSpeed1995]
  Location: Volume 1, Page 187, Figure 5.42
```
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

## Document Structure (Target)

```
0.(abstract) Executive summary
1. Introduction
2. Mission definition
   2.1 Operational environment: Arcadia Planitia (includes atmosphere model)
   2.2 Mission profile
   2.3 Requirements
3. Configuration trade-offs
   3.1 Reference designs
       3.1.1 Mars UAV concepts (Ingenuity, ARES, Mars Science Helicopter)
       3.1.2 Commercial VTOL benchmarks
           3.1.2.1 Propulsion characteristics
           3.1.2.2 Energy storage characteristics
           3.1.2.3 Fuselage geometry (length/span ratios, fineness)
           3.1.2.4 Tail configurations (fuselage-mounted vs boom-mounted)
           3.1.2.5 Structural materials
   3.2 Architecture comparison
       3.2.1 Flight architecture (rotorcraft, fixed-wing, hybrid VTOL)
       3.2.2 Fuselage geometry trade-offs
       3.2.3 Tail configuration trade-offs (fuselage vs boom-mounted options)
       3.2.4 Structural material trade-offs
   3.3 Architecture selection
       3.3.1 QuadPlane configuration rationale
       3.3.2 Tail configuration selection
       3.3.3 Fuselage geometry selection
       3.3.4 Structural material selection
4. Initial design hypotheses
   4.1 Design methodology
   4.2 Mass and power allocation
   4.3 Target MTOW
   4.4 Wing geometry
   4.5 Tail geometry (sizing for Mars conditions)
   4.6 Fuselage geometry (sizing and payload integration)
   4.7 Propulsion sizing
   4.8 Rotor and propeller sizing
   4.9 Energy storage
   4.10 Payload
   4.11 Structural materials (mass estimation implications)
   4.12 Summary of initial hypotheses
5. Aerodynamic analysis
   5.1 Low-Reynolds regime characteristics
   5.2 Airfoil selection (E387, S1223, S7055 comparison)
   5.3 Drag polar model
6. Preliminary sizing methodology
   6.1 Constraint-based sizing (matching chart)
   6.2 Weight estimation
7. Preliminary design results
   7.1 Design point from matching chart
   7.2 Preliminary mass breakdown
   7.3 Preliminary power budget
   7.4 Estimated endurance and range
8. Component selection
   8.1 Selection criteria and trade-offs
   8.2 Propulsion (lift motors, cruise motors, propellers)
   8.3 Energy storage (batteries)
   8.4 Payload (camera, radio relay)
   8.5 Avionics and thermal control
9. Detailed design verification
    9.1 Updated mass breakdown with selected components
    9.2 Updated power budget
    9.3 Final performance (endurance, range, operational radius)
    9.4 Requirements compliance check
10. Infrastructure requirements
    10.1 Habitat hangar specifications
    10.2 Operations concept
11. Conclusions and recommendations
12. References
Appendices: A. Constants, B. Component datasheets, C. Sizing scripts, D. XFOIL results
```

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

### Airfoil Analysis
- **XFOIL does not converge** at Reynolds ~50,000 due to laminar separation bubbles
- Use **Selig wind tunnel data** from "Summary of Low-Speed Airfoil Data" instead
- Candidates: E387, S1223, S7055

### Key Design Parameters
- Target MTOW: TBD kg
- Cruise speed: TBD m/s
- Reynolds number: ~50,000-55,000
- Operating location: Arcadia Planitia (-3 km elevation)
- Atmospheric density: ~0.020 kg/m³

### Numerical Calculations (CRITICAL)

**Do NOT rely on manual calculations for numerical results.** All numerical values that appear in the manuscript must be generated or verified using Python code in `src/mars_uav_sizing/`.

**Rationale:**
- Manual calculations are error-prone and difficult to verify
- Code ensures consistency when parameters change
- Results can be reproduced and audited
- Unit conversions and physical constants are handled consistently

**Workflow:**
1. Implement the calculation in the appropriate Python module
2. Run the code to generate the numerical result
3. Copy the result to the manuscript with appropriate precision
4. Document the calculation in `source_grounding.txt` with reference to the code module

**Example:**
```python
# In src/mars_uav_sizing/transition.py
def estimate_transition_energy(transition_energy_j: float = 45000, n_transitions: int = 2) -> float:
    """Estimate total transition energy in Wh."""
    J_PER_WH = 3600
    return (transition_energy_j * n_transitions) / J_PER_WH
```

**Never:**
- Perform arithmetic in your head or with a calculator
- Copy-paste numerical results without code verification
- Use approximate values when exact calculations are available

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

