# Markdown Document Management Tools

This is a reusable toolkit for managing and building technical documents written in Markdown. It provides scripts for splitting/joining documents by section, and building professionally formatted DOCX files with proper cross-references, citations, and table formatting.

## File Structure

```
markdown_tools/
├── README.md                           # This file
├── .gitignore                          # Git ignore template
├── config.template.yaml                # Configuration template (rename to config.yaml)
├── docx.defaults.yaml                  # Pandoc configuration for DOCX output
├── reference.docx                      # Word reference document for styling
├── ieee.csl                            # Citation style (IEEE format)
│
├── Batch Scripts (Windows)
├── split.bat                           # Split document into sections
├── reconstruct.bat                     # Reconstruct document from sections (with auto-backup)
└── build_docx.bat                      # Build DOCX output
│
├── Lua Filters (Pandoc)
├── after_table_spacer.lua              # Add spacing after tables
├── bullet_to_word_list_bullet.lua      # Convert markdown bullets to Word bullets
├── equation_block_style.lua            # Apply equation block styling
├── subfig_grid_tblstyle.lua            # Handle subfigure grids
└── table_body_style.lua                # Apply table body styling
│
├── tools/
│   ├── split_sections.py               # Split markdown by sections
│   ├── join_sections.py                # Reconstruct markdown from sections
│   ├── build_docx.py                   # Build DOCX via Pandoc
│   └── docx_autofit_tables.py          # Post-process DOCX for table AutoFit
│
└── docs/
    ├── regole_di_stile.txt             # Italian style guide
    └── style_rules.txt                 # English style guide
```

## Quick Start for New Projects

To use this toolkit in a new writing project:

1. Copy all necessary files to your project:
   ```bash
   cd C:\Users\matti\OneDrivePhD\Dev\MyNewProject

   # Copy core tools and scripts
   cp -r ../markdown_tools/tools .
   cp ../markdown_tools/*.bat .

   # Copy configuration files
   cp ../markdown_tools/config.template.yaml config.yaml
   cp ../markdown_tools/docx.defaults.yaml .
   cp ../markdown_tools/.gitignore .

   # Copy Pandoc assets (for DOCX building)
   cp ../markdown_tools/reference.docx .
   cp ../markdown_tools/*.lua .
   cp ../markdown_tools/ieee.csl .

   # Optional: Copy style guides
   cp -r ../markdown_tools/docs .
   ```

2. Edit `config.yaml` and set `main_document` to your document filename
3. Edit `docx.defaults.yaml` to configure:
   - `bibliography`: Your .bib file(s)
   - `output-file`: Your desired DOCX output name
   - Metadata (tableTitle, figureTitle, etc.) for your language
4. Create your bibliography file (e.g., `references.bib`)
5. Start writing and using the scripts!

## Configuration

The project uses a `config.yaml` file to configure document settings. This makes the scripts reusable across different projects without modifying code.

### config.yaml

```yaml
# Main markdown document filename (required)
main_document: "my_document.md"

# Directory where split sections are stored (optional, default: "sections")
sections_dir: "sections"

# Front matter YAML filename (optional, default: "front_matter.yaml")
front_matter_file: "front_matter.yaml"
```

### docx.defaults.yaml

The `docx.defaults.yaml` file configures Pandoc for DOCX output:

- **reference-doc**: Word template for styles and formatting
- **filters**: Pandoc filters applied in order:
  - `pandoc-crossref`: Cross-references for figures, tables, equations
  - `table_body_style.lua`: Apply table body styling
  - `after_table_spacer.lua`: Add spacing after tables
  - `equation_block_style.lua`: Style equation blocks
  - `subfig_grid_tblstyle.lua`: Handle subfigure layouts
  - `citeproc`: Process citations and bibliography
- **bibliography**: Path to your .bib file(s)
- **csl**: Citation style file (default: ieee.csl)
- **metadata**: Configure cross-reference labels for your language

### Pandoc Assets

- **reference.docx**: Word template defining all styles (headings, body text, tables, captions, etc.)
- **Lua filters**: Custom Pandoc filters for professional formatting
- **ieee.csl**: IEEE citation style (can be replaced with other CSL files)

## Document Management Scripts

### Splitting Documents

The `split_sections.py` script splits your main markdown document into separate files by section:

```bash
# Using default settings from config.yaml
python tools\split_sections.py

# Or specify a different source file
python tools\split_sections.py my_document.md

# Or use a different output directory
python tools\split_sections.py -o my_sections
```

Or use the convenient batch file:

```bash
split.bat
```

The script will:
- Extract YAML front matter to `sections/front_matter.yaml`
- Create separate files for each top-level heading
- Create additional files for level-2 subsections
- Number files for easy sorting (e.g., `01_00_introduction.md`, `01_01_background.md`)

### Reconstructing Documents

The `join_sections.py` script reconstructs your document from the split sections:

```bash
# Using default settings from config.yaml
python tools\join_sections.py

# Or specify custom options
python tools\join_sections.py -s my_sections -o output.md
```

Or use the convenient batch file (which creates automatic backups):

```bash
reconstruct.bat
```

The script will:
- Read the front matter and all section files
- Reconstruct the complete document
- Write to the output file (default: same as main_document in config.yaml)

Note: `reconstruct.bat` automatically creates timestamped backups in the `backups/` folder before overwriting.

## Building DOCX Output

The `build_docx.py` script converts your markdown document to DOCX format using Pandoc:

```bash
python tools\build_docx.py
```

Or use the convenient batch file:

```bash
build_docx.bat
```

This uses settings from `docx.defaults.yaml` and applies table formatting patches.

## Workflow

1. Edit your main document (e.g., `my_document.md`) or split it into sections for easier editing
2. If working with sections:
   - Split the document: `split.bat`
   - Edit individual section files in the `sections/` directory
   - Reconstruct: `reconstruct.bat`
3. Build DOCX: `build_docx.bat`

## Requirements

### Python
- Python 3.11+
- PyYAML: `pip install pyyaml` or `uv add pyyaml`

### Pandoc Toolchain
- **Pandoc** 2.19+ ([download](https://pandoc.org/installing.html))
- **pandoc-crossref** ([download](https://github.com/lierdakil/pandoc-crossref/releases))
  - Must match your Pandoc version
  - Place executable in PATH or same directory as pandoc.exe

### Optional
- Git (for version control)
- A bibliography manager that exports BibTeX (.bib files)

## Features

### Document Splitting and Reconstruction
- Split large documents by sections for easier editing and collaboration
- Automatic backup system prevents data loss
- Preserves YAML front matter and document structure

### Professional DOCX Output
- Cross-references for figures, tables, and equations (via pandoc-crossref)
- Automatic citation and bibliography generation (via citeproc)
- Custom formatting via Lua filters:
  - Proper table styling and spacing
  - Equation block formatting
  - Subfigure grid layouts
  - Markdown to Word bullet conversion
- AutoFit table layout for optimal column widths
- Customizable via reference.docx template

### Configuration-Driven
- All settings in YAML files - no code changes needed
- Reusable across multiple projects
- Language-independent (configure labels for any language)
