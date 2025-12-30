#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Defaults:
    output_file: str
    reference_doc: Optional[str]
    bibliography: Optional[str]
    csl: Optional[str]


def die(msg: str, code: int = 1) -> None:
    print(f"[build_docx] ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config


def parse_defaults_yaml(path: Path) -> Defaults:
    text = path.read_text(encoding="utf-8", errors="replace")

    def pick(key: str) -> Optional[str]:
        m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", text)
        if not m:
            return None
        v = m.group(1).strip()
        # strip simple quotes
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1].strip()
        return v

    # output-file is now optional (can be set via config)
    return Defaults(
        output_file=pick("output-file") or "",
        reference_doc=pick("reference-doc"),
        bibliography=pick("bibliography"),
        csl=pick("csl"),
    )


def choose_input(project_root: Path, cli_input: Optional[str]) -> Path:
    if cli_input:
        p = (project_root / cli_input).resolve()
        if not p.exists():
            die(f"Input file not found: {p}")
        return p

    # deterministic candidates first
    for name in ("relazione_tecnica_reconstructed.md", "relazione_tecnica.md", "paper.md", "manuscript.md"):
        p = project_root / name
        if p.exists():
            return p.resolve()

    # fallback: most recently modified .md excluding common non-manuscripts
    md_files = [
        p for p in project_root.glob("*.md")
        if p.name.lower() not in {"readme.md", "changelog.md", "license.md"}
        and not p.name.startswith("_")
    ]
    if not md_files:
        die("No markdown input found in project root (and no input passed).")

    md_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0].resolve()


def run(cmd: list[str], cwd: Path) -> None:
    print("[build_docx] " + " ".join(cmd))
    cp = subprocess.run(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if cp.stdout:
        # Ensure users see all tool output even when the window closes after exit.
        print(cp.stdout, end="" if cp.stdout.endswith("\n") else "\n")

    if cp.returncode != 0:
        die(f"Command failed with exit code {cp.returncode}: {' '.join(cmd)}", cp.returncode)


def build_single_document(
    project_root: Path,
    input_path: Path,
    defaults_path: Path,
    output_file: Path,
    bibliography: Optional[str],
    pandoc: str,
    python_exe: str,
    patcher: Path,
    keep_raw: bool,
) -> bool:
    """Build a single DOCX document. Returns True on success."""
    defaults = parse_defaults_yaml(defaults_path)

    final_docx = output_file.resolve()
    raw_docx = final_docx.with_suffix(".raw.docx")

    # Optional sanity checks
    if defaults.reference_doc:
        ref = project_root / defaults.reference_doc
        if not ref.exists():
            print(f"[build_docx] ERROR: reference-doc not found: {ref}")
            return False
    if defaults.csl:
        csl = project_root / defaults.csl
        if not csl.exists():
            print(f"[build_docx] ERROR: csl not found: {csl}")
            return False

    # Build pandoc command
    cmd = [pandoc, str(input_path), "-d", str(defaults_path), "-o", str(raw_docx)]

    # Add bibliography if specified (from config, overrides defaults)
    if bibliography:
        bib_path = project_root / bibliography
        if not bib_path.exists():
            print(f"[build_docx] ERROR: bibliography not found: {bib_path}")
            return False
        cmd.extend(["--bibliography", str(bib_path)])

    # 1) pandoc -> raw docx
    run(cmd, cwd=project_root)

    # 2) patch -> final docx
    run([python_exe, str(patcher), str(raw_docx), str(final_docx)], cwd=project_root)

    if not keep_raw:
        try:
            raw_docx.unlink(missing_ok=True)
        except Exception:
            pass

    print(f"[build_docx] OK: {final_docx}")
    return True


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config.yaml"
    config = load_config(config_path)

    # Check for multilanguage config
    languages = config.get("languages", {})
    available_langs = list(languages.keys()) if languages else []
    lang_help = f"Language to build ({', '.join(available_langs)}). Use 'all' for all languages." if available_langs else "Language code (e.g., 'en', 'it')"

    ap = argparse.ArgumentParser(description="Build DOCX via pandoc defaults + AutoFit patch.")
    ap.add_argument("input", nargs="?", help="Markdown input path (relative to project root).")
    ap.add_argument("-d", "--defaults", default=None, help="Pandoc defaults YAML (overrides config).")
    ap.add_argument("-o", "--output", default=None, help="Output DOCX file (overrides config).")
    ap.add_argument("-l", "--lang", default="all", help=lang_help)
    ap.add_argument("--pandoc", default=None, help="Pandoc executable (default: autodetect).")
    ap.add_argument("--python", dest="python_exe", default=None, help="Python executable (default: current).")
    ap.add_argument("--keep-raw", action="store_true", help="Keep intermediate .raw.docx.")
    args = ap.parse_args()

    pandoc = args.pandoc or shutil.which("pandoc")
    if not pandoc:
        die("pandoc not found on PATH.")

    python_exe = args.python_exe or sys.executable
    patcher = (project_root / "tools" / "docx_autofit_tables.py").resolve()
    if not patcher.exists():
        die(f"Patcher not found: {patcher}")

    # Shared bibliography from config
    shared_bibliography = config.get("bibliography")

    # Determine mode
    if args.input and args.defaults:
        # Manual mode: specific input and defaults
        input_path = (project_root / args.input).resolve()
        if not input_path.exists():
            die(f"Input file not found: {input_path}")

        defaults_path = (project_root / args.defaults).resolve()
        if not defaults_path.exists():
            die(f"Defaults file not found: {defaults_path}")

        defaults = parse_defaults_yaml(defaults_path)
        output_file = project_root / (args.output or defaults.output_file or "output.docx")

        build_single_document(
            project_root, input_path, defaults_path, output_file,
            shared_bibliography, pandoc, python_exe, patcher, args.keep_raw
        )
    elif languages:
        # Multilanguage mode
        langs_to_process = available_langs if args.lang == "all" else [args.lang]
        success_count = 0

        for lang in langs_to_process:
            if lang not in languages:
                print(f"Warning: Language '{lang}' not found in config. Skipping.")
                continue

            lang_config = languages[lang]
            input_path = project_root / lang_config.get("main_document", f"{lang}.md")
            defaults_path = project_root / lang_config.get("docx_defaults", f"docx.defaults.{lang}.yaml")
            output_file = project_root / lang_config.get("output_file", f"{lang}.docx")

            if not input_path.exists():
                print(f"[{lang.upper()}] Warning: Input file '{input_path}' not found. Skipping.")
                continue

            if not defaults_path.exists():
                print(f"[{lang.upper()}] Warning: Defaults file '{defaults_path}' not found. Skipping.")
                continue

            print(f"\n[{lang.upper()}] Building {output_file.name} from {input_path.name}...")
            if build_single_document(
                project_root, input_path, defaults_path, output_file,
                shared_bibliography, pandoc, python_exe, patcher, args.keep_raw
            ):
                success_count += 1

        print(f"\n[build_docx] Completed: {success_count}/{len(langs_to_process)} documents built.")
    else:
        # Legacy single-language mode (backward compatibility)
        defaults_file = args.defaults or "docx.defaults.yaml"
        defaults_path = (project_root / defaults_file).resolve()
        if not defaults_path.exists():
            die(f"Defaults file not found: {defaults_path}")

        defaults = parse_defaults_yaml(defaults_path)
        input_path = choose_input(project_root, args.input)
        output_file = project_root / (args.output or defaults.output_file or "output.docx")

        build_single_document(
            project_root, input_path, defaults_path, output_file,
            shared_bibliography, pandoc, python_exe, patcher, args.keep_raw
        )


if __name__ == "__main__":
    main()
