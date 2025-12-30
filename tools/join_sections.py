#!/usr/bin/env python3
"""
Reassemble a markdown document from split section files.

- Reads front matter from a separate YAML file (configurable, default: `sections/front_matter.yaml`).
- Rebuilds each level-1 section once, combining its base content and level-2 subsections.
- Strips helper lines (added during splitting) such as duplicate H1s and the injected authors line.
"""

import argparse
import pathlib
import re
import yaml
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


def load_config(config_path: pathlib.Path) -> Dict[str, str]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config


def read_front_matter(path: pathlib.Path) -> str:
    """Return front matter text, ensuring it is wrapped in YAML delimiters."""
    text = path.read_text(encoding="utf-8").strip("\n")
    if not text.startswith("---"):
        text = "---\n" + text
    if not text.endswith("---"):
        text = text + "\n---"
    return text


def strip_leading_blank_lines(lines: List[str]) -> List[str]:
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return lines[idx:]


def parse_section_filename(path: pathlib.Path) -> Tuple[int, Optional[int]]:
    """
    Parse section and subsection indices from a filename of the form:
    NN_XX_slug.md (XX optional). Returns (section, part) where part can be None.
    """
    match = re.match(r"^(?P<section>\d{2})_(?P<rest>.+)\.md$", path.name)
    if not match:
        raise ValueError(f"Unexpected section filename: {path.name}")
    section = int(match.group("section"))
    rest = match.group("rest")
    part_match = re.match(r"^(?P<part>\d{2})_.*", rest)
    part = int(part_match.group("part")) if part_match else None
    return section, part


def extract_preface(lines: List[str]) -> str:
    """
    For section 00: drop the injected title H1 and authors line; return the remaining text.
    """
    lines = lines[:]
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    lines = strip_leading_blank_lines(lines)
    filtered = [
        ln for ln in lines 
        if not ln.strip().lower().startswith("authors:") 
        and not ln.strip().lower().startswith("autori:")
    ]
    filtered = strip_leading_blank_lines(filtered)
    return "\n".join(filtered).strip("\n")


def extract_base_section(lines: List[str]) -> Tuple[str, str]:
    """
    From a base section file, return (heading_line, body) where heading_line keeps the
    original H1 line (including any spacing).
    """
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Base section missing H1 heading.")
    heading_line = lines[0]
    body_lines = strip_leading_blank_lines(lines[1:])
    body = "\n".join(body_lines).strip("\n")
    return heading_line, body


def extract_subsection(lines: List[str]) -> str:
    """
    From a subsection file, drop the parent H1 and return text starting from the H2.
    """
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines) and lines[idx].startswith("# "):
        idx += 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
    if idx >= len(lines) or not lines[idx].startswith("## "):
        raise ValueError("Subsection file missing expected H2 heading.")
    subsection = "\n".join(lines[idx:]).strip("\n")
    return subsection


def join_sections(md_files: List[pathlib.Path]) -> str:
    """
    Rebuild the manuscript body from section files while removing helper headings.
    """
    grouped: Dict[int, Dict[Optional[int], pathlib.Path]] = defaultdict(dict)
    for path in md_files:
        section, part = parse_section_filename(path)
        grouped[section][part] = path

    blocks: List[str] = []

    # Section 00 (preface)
    if 0 in grouped:
        preface_parts = grouped[0]
        for part in sorted(preface_parts.keys(), key=lambda x: -1 if x is None else x):
            lines = preface_parts[part].read_text(encoding="utf-8").splitlines()
            preface = extract_preface(lines)
            if preface:
                blocks.append(preface)

    # Other sections
    for section in sorted(k for k in grouped.keys() if k != 0):
        parts = grouped[section]
        if 0 not in parts:
            raise ValueError(f"Missing base file for section {section:02d}")
        base_lines = parts[0].read_text(encoding="utf-8").splitlines()
        heading_line, base_body = extract_base_section(base_lines)

        section_chunks: List[str] = [heading_line]
        if base_body:
            section_chunks.append(base_body)

        for part in sorted(k for k in parts.keys() if k):
            sub_lines = parts[part].read_text(encoding="utf-8").splitlines()
            subsection_text = extract_subsection(sub_lines)
            section_chunks.append(subsection_text)

        blocks.append("\n\n".join(section_chunks).strip("\n"))

    return "\n\n".join(blocks).strip("\n")


def reconstruct_document(sections_dir: pathlib.Path, output_path: pathlib.Path, front_matter_filename: str) -> None:
    """Reconstruct a single document from its sections."""
    if not sections_dir.exists():
        raise FileNotFoundError(f"Sections directory not found: {sections_dir}")

    front_path = sections_dir / front_matter_filename
    if not front_path.exists():
        raise FileNotFoundError(f"Front matter file not found: {front_path}")

    md_files = sorted(p for p in sections_dir.glob("*.md") if p.is_file())
    if not md_files:
        raise FileNotFoundError(f"No markdown section files found in {sections_dir}")

    front_text = read_front_matter(front_path).strip("\n")
    body_text = join_sections(md_files)

    full_text = front_text + "\n\n" + body_text
    output_path.write_text(full_text, encoding="utf-8")


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

    parser = argparse.ArgumentParser(description="Recreate the full manuscript from split sections.")
    parser.add_argument(
        "-s",
        "--sections-dir",
        default=None,
        help="Directory containing split section files (overrides config).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output manuscript file (overrides config).",
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
    if args.sections_dir and args.output:
        # Manual mode: specific sections dir and output
        sections_dir = pathlib.Path(args.sections_dir)
        output_path = pathlib.Path(args.output)
        reconstruct_document(sections_dir, output_path, front_matter_filename)
        print(f"Wrote manuscript to {output_path.resolve()}")
    elif languages:
        # Multilanguage mode
        langs_to_process = available_langs if args.lang == "all" else [args.lang]

        for lang in langs_to_process:
            if lang not in languages:
                print(f"Warning: Language '{lang}' not found in config. Skipping.")
                continue

            lang_config = languages[lang]
            sections_dir = project_root / lang_config.get("sections_dir", f"sections_{lang}")
            output_path = project_root / lang_config.get("main_document", f"{lang}.md")

            if not sections_dir.exists():
                print(f"Warning: Sections directory '{sections_dir}' not found for language '{lang}'. Skipping.")
                continue

            print(f"[{lang.upper()}] Reconstructing {output_path.name}...")
            reconstruct_document(sections_dir, output_path, front_matter_filename)
            print(f"[{lang.upper()}] Wrote manuscript to {output_path.resolve()}")
    else:
        # Legacy single-language mode (backward compatibility)
        default_output = config.get("main_document", "document.md")
        default_sections_dir = config.get("sections_dir", "sections")

        sections_dir = pathlib.Path(args.sections_dir or default_sections_dir)
        output_path = pathlib.Path(args.output or default_output)

        reconstruct_document(sections_dir, output_path, front_matter_filename)
        print(f"Wrote manuscript to {output_path.resolve()}")


if __name__ == "__main__":
    main()
