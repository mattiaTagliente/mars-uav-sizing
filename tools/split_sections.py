#!/usr/bin/env python3
"""
Split a markdown document into separate files by top-level sections and their level-2 subsections.

- Strips the leading YAML front matter.
- Saves the YAML front matter to a separate file (configurable, default: `sections/front_matter.yaml`).
- The first output file contains the title (from YAML), authors, abstract, and keywords.
- Each level-1 heading (`# Heading`) produces a base file (suffix `_00_...`) with
  content before any `##` subsections, plus additional files for each `##` subsection.
"""

import argparse
import pathlib
import re
import unicodedata
import yaml
from typing import Dict, Iterable, List, Optional, Tuple


def load_config(config_path: pathlib.Path) -> Dict[str, str]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config


def slugify(text: str) -> str:
    """Turn a heading into a filesystem-friendly slug."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_only = ascii_only.lower()
    ascii_only = re.sub(r"[^a-z0-9]+", "-", ascii_only).strip("-")
    return ascii_only or "section"


def parse_yaml_front_matter(lines: List[str]) -> Tuple[Dict[str, str], List[str], List[str]]:
    """
    Remove the initial YAML block if present and return its key-value pairs
    together with the remaining lines and raw YAML block.
    """
    if not lines or lines[0].strip() != "---":
        return {}, lines, []

    yaml_lines: List[str] = []
    raw_block: List[str] = ["---"]
    closing_index = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = idx
            raw_block.append("---")
            break
        yaml_lines.append(line)
        raw_block.append(line.rstrip("\n"))

    if closing_index is None:
        # No closing delimiter; treat as plain text.
        return {}, lines, []

    yaml_data: Dict[str, str] = {}
    for raw_line in yaml_lines:
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        yaml_data[key.strip()] = value.strip().strip('"')

    remaining = lines[closing_index + 1 :]
    return yaml_data, remaining, raw_block


def split_sections(lines: Iterable[str]) -> Tuple[List[str], List[Tuple[str, List[str]]]]:
    """Split content lines into the preface block and a list of level-1 sections."""
    preface: List[str] = []
    sections: List[Tuple[str, List[str]]] = []
    current_heading: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("# "):
            if current_heading is not None:
                sections.append((current_heading, current_lines))
                current_lines = []
            current_heading = line[2:]
            continue

        if current_heading is None:
            preface.append(line)
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections.append((current_heading, current_lines))

    return preface, sections


def split_subsections(lines: Iterable[str]) -> Tuple[List[str], List[Tuple[str, List[str]]]]:
    """
    Split a section's lines into content before the first level-2 heading and a list of
    level-2 subsections (heading, lines).
    """
    base_lines: List[str] = []
    subsections: List[Tuple[str, List[str]]] = []
    current_heading: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_heading is None:
                base_lines = current_lines
            else:
                subsections.append((current_heading, current_lines))
            current_heading = line[3:]
            current_lines = []
            continue

        current_lines.append(line)

    if current_heading is None:
        base_lines = current_lines
    else:
        subsections.append((current_heading, current_lines))

    return base_lines, subsections


def strip_label(heading: str) -> str:
    """
    Strip pandoc-crossref label from a heading.
    
    Example: "Constraint analysis {#sec:constraint-analysis}" -> "Constraint analysis"
    """
    # Match pattern: text followed by optional whitespace and {#label}
    match = re.match(r'^(.*?)\s*\{#[^}]+\}\s*$', heading)
    if match:
        return match.group(1).strip()
    return heading


def write_section_file(
    path: pathlib.Path,
    heading: Optional[str],
    body_lines: List[str],
    parent_heading: Optional[str] = None,
) -> None:
    """Write a section file with optional heading and parent heading.
    
    Note: When writing subsection files, the parent_heading label is stripped
    to avoid duplicate labels across files. The label is preserved only in the
    base section file (_00_).
    """
    parts: List[str] = []
    if parent_heading:
        # Strip label from parent heading to avoid duplicates
        parent_heading_clean = strip_label(parent_heading)
        parts.append(f"# {parent_heading_clean}")
        if heading:
            parts.append("")
            parts.append(f"## {heading}")
    elif heading:
        parts.append(f"# {heading}")
    body = "\n".join(body_lines)
    body = body.lstrip("\n")
    if body:
        if parts:
            parts.append("")
        parts.append(body)
    text = "\n".join(parts)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")



def split_document(source_path: pathlib.Path, output_dir: pathlib.Path, front_matter_filename: str) -> int:
    """Split a single document into sections. Returns the number of files written."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    raw_lines = source_path.read_text(encoding="utf-8").splitlines()
    yaml_meta, content_lines, raw_yaml_block = parse_yaml_front_matter(raw_lines)
    preface_lines, sections = split_sections(content_lines)

    title = yaml_meta.get("title", "").strip()
    authors = yaml_meta.get("author", "").strip()

    preface_with_authors = preface_lines
    if authors:
        preface_with_authors = [f"Authors: {authors}", ""] + preface_lines

    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all section prefixes that will be written (to clean up stale files)
    # Format: set of patterns like "03_01_", "03_02_", etc.
    prefixes_to_write: set = {"00_"}  # Always write title/abstract file
    for idx, (heading, lines) in enumerate(sections, start=1):
        prefixes_to_write.add(f"{idx:02d}_00_")
        base_lines, subsections = split_subsections(lines)
        for sub_idx in range(1, len(subsections) + 1):
            prefixes_to_write.add(f"{idx:02d}_{sub_idx:02d}_")

    # Clean up stale files: for each prefix we're about to write, 
    # delete any existing .md files with that prefix but different slug
    stale_files_removed = 0
    if output_dir.exists():
        for existing_file in output_dir.glob("*.md"):
            # Extract prefix (first two underscore-separated parts, e.g., "03_01_")
            parts = existing_file.stem.split("_", 2)
            if len(parts) >= 2:
                prefix = f"{parts[0]}_{parts[1]}_"
                if prefix in prefixes_to_write:
                    # This prefix will be overwritten - delete the old file
                    existing_file.unlink()
                    stale_files_removed += 1

    if stale_files_removed > 0:
        print(f"  Cleaned up {stale_files_removed} stale section file(s)")

    if raw_yaml_block:
        front_matter_path = output_dir / front_matter_filename
        front_matter_path.write_text("\n".join(raw_yaml_block).rstrip("\n") + "\n", encoding="utf-8")

    first_filename = output_dir / "00_title_abstract_keywords.md"
    write_section_file(first_filename, title or None, preface_with_authors)

    for idx, (heading, lines) in enumerate(sections, start=1):
        slug = slugify(heading)
        base_lines, subsections = split_subsections(lines)

        base_filename = output_dir / f"{idx:02d}_00_{slug}.md"
        write_section_file(base_filename, heading, base_lines)

        for sub_idx, (sub_heading, sub_lines) in enumerate(subsections, start=1):
            sub_slug = slugify(sub_heading)
            sub_filename = output_dir / f"{idx:02d}_{sub_idx:02d}_{sub_slug}.md"
            write_section_file(sub_filename, sub_heading, sub_lines, parent_heading=heading)

    total_files = (1 if raw_yaml_block else 0) + 1 + sum(1 + len(split_subsections(lines)[1]) for _, lines in sections)
    return total_files


def main() -> None:
    # Load configuration
    project_root = pathlib.Path(__file__).resolve().parents[1]
    config_path = project_root / "config.yaml"
    config = load_config(config_path)

    # Check for multilanguage config
    languages = config.get("languages", {})
    front_matter_filename = config.get("front_matter_file", "front_matter.yaml")

    # Build list of available languages for help text
    available_langs = list(languages.keys()) if languages else []
    lang_help = f"Language to process ({', '.join(available_langs)}). Use 'all' for all languages." if available_langs else "Language code (e.g., 'en', 'it')"

    parser = argparse.ArgumentParser(description="Split markdown document into section files.")
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="Path to the source markdown file (overrides config).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Directory where section files are written (overrides config).",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="all",
        help=lang_help,
    )
    parser.add_argument(
        "-c",
        "--config",
        default=str(config_path),
        help="Path to config.yaml file (default: config.yaml in project root).",
    )
    args = parser.parse_args()

    # Determine which languages to process
    if args.source and args.output_dir:
        # Manual mode: specific source and output
        source_path = pathlib.Path(args.source)
        output_dir = pathlib.Path(args.output_dir)
        total_files = split_document(source_path, output_dir, front_matter_filename)
        print(f"Wrote {total_files} files to {output_dir.resolve()}")
    elif languages:
        # Multilanguage mode
        langs_to_process = available_langs if args.lang == "all" else [args.lang]

        for lang in langs_to_process:
            if lang not in languages:
                print(f"Warning: Language '{lang}' not found in config. Skipping.")
                continue

            lang_config = languages[lang]
            source_path = project_root / lang_config.get("main_document", f"{lang}.md")
            output_dir = project_root / lang_config.get("sections_dir", f"sections_{lang}")

            if not source_path.exists():
                print(f"Warning: Source file '{source_path}' not found for language '{lang}'. Skipping.")
                continue

            print(f"[{lang.upper()}] Splitting {source_path.name}...")
            total_files = split_document(source_path, output_dir, front_matter_filename)
            print(f"[{lang.upper()}] Wrote {total_files} files to {output_dir.resolve()}")
    else:
        # Legacy single-language mode (backward compatibility)
        default_source = config.get("main_document", "document.md")
        default_sections_dir = config.get("sections_dir", "sections")

        source_path = pathlib.Path(args.source or default_source)
        output_dir = pathlib.Path(args.output_dir or default_sections_dir)

        total_files = split_document(source_path, output_dir, front_matter_filename)
        print(f"Wrote {total_files} files to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
