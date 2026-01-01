#!/usr/bin/env python3
"""
check_sidecar.py - Validate that all locators in manuscripts have matching sidecar entries

This script:
1. Parses all [@key]<!-- #loc --> patterns from manuscript sections
2. Checks that each locator has a corresponding entry in sources/*.sources.yaml
3. Reports missing entries and orphaned sidecar entries

Usage:
    python check_sidecar.py [--fix] [--verbose]
"""

import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict


# Pattern matches: [@citationKey] or [@citationKey, location]<!-- #locator -->
LOCATOR_PATTERN = re.compile(
    r'\[@([a-zA-Z][a-zA-Z0-9_:/-]*)'  # Citation key
    r'(?:[^\]]*)\]'                   # Optional location info (e.g., ", Chapter 5")
    r'\s*'                            # Optional whitespace
    r'<!--\s*#([a-z0-9:._-]+)\s*-->'  # Locator in HTML comment
)


def get_section_number(filename: str) -> str:
    """Extract section number from filename like 05_01_rotorcraft....md -> 05_01"""
    parts = filename.split('_')
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return f"{parts[0]}_{parts[1]}"
    return None


def extract_manuscript_locators(sections_dir: Path) -> Dict[str, Set[Tuple[str, str]]]:
    """
    Extract all locators from manuscript, grouped by section.
    Returns: {section_number: {(citation_key, locator), ...}}
    """
    section_locators = defaultdict(set)
    
    for md_file in sections_dir.glob('*.md'):
        section_num = get_section_number(md_file.name)
        if not section_num:
            continue
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}")
            continue
        
        for match in LOCATOR_PATTERN.finditer(content):
            citation_key = match.group(1)
            locator = match.group(2)
            section_locators[section_num].add((citation_key, locator))
    
    return section_locators


def load_sidecar(sidecar_path: Path) -> Dict[str, Set[str]]:
    """
    Load a sidecar YAML file and return locators grouped by citation key.
    Returns: {citation_key: {locator, ...}}
    """
    sidecar_locators = defaultdict(set)
    
    if not sidecar_path.exists():
        return sidecar_locators
    
    try:
        with open(sidecar_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not parse {sidecar_path}: {e}")
        return sidecar_locators
    
    if not data:
        return sidecar_locators
    
    for citation_key, locators in data.items():
        if isinstance(locators, dict):
            for locator in locators.keys():
                sidecar_locators[citation_key].add(locator)
    
    return sidecar_locators


def validate_section(
    section_num: str,
    manuscript_locators: Set[Tuple[str, str]],
    sources_dir: Path,
    verbose: bool = False
) -> Tuple[List[str], List[str]]:
    """
    Validate locators for a single section.
    Returns: (missing_in_sidecar, orphaned_in_sidecar)
    """
    sidecar_path = sources_dir / f"{section_num}.sources.yaml"
    sidecar_data = load_sidecar(sidecar_path)
    
    missing = []
    orphaned = []
    
    # Check each manuscript locator has a sidecar entry
    for citation_key, locator in manuscript_locators:
        if citation_key not in sidecar_data or locator not in sidecar_data[citation_key]:
            missing.append(f"{citation_key}.{locator}")
    
    # Check for orphaned sidecar entries (not in manuscript)
    manuscript_set = {(k, l) for k, l in manuscript_locators}
    for citation_key, locators in sidecar_data.items():
        for locator in locators:
            if (citation_key, locator) not in manuscript_set:
                orphaned.append(f"{citation_key}.{locator}")
    
    if verbose:
        if not sidecar_path.exists():
            print(f"  Sidecar not found: {sidecar_path.name}")
        else:
            print(f"  Sidecar: {sidecar_path.name}")
            print(f"    Manuscript locators: {len(manuscript_locators)}")
            print(f"    Sidecar entries: {sum(len(v) for v in sidecar_data.values())}")
    
    return missing, orphaned


def main():
    parser = argparse.ArgumentParser(
        description='Validate manuscript locators against sidecar YAML files'
    )
    parser.add_argument(
        '--sections', '-s',
        default='sections_en',
        help='Directory containing manuscript sections (default: sections_en)'
    )
    parser.add_argument(
        '--sources', '-S',
        default='sources',
        help='Directory containing sidecar YAML files (default: sources)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print detailed information for each section'
    )
    
    args = parser.parse_args()
    
    sections_dir = Path(args.sections)
    sources_dir = Path(args.sources)
    
    if not sections_dir.exists():
        print(f"Error: Sections directory not found: {sections_dir}")
        return 1
    
    if not sources_dir.exists():
        print(f"Error: Sources directory not found: {sources_dir}")
        return 1
    
    # Extract all manuscript locators
    print("Scanning manuscript sections...")
    section_locators = extract_manuscript_locators(sections_dir)
    
    total_locators = sum(len(v) for v in section_locators.values())
    print(f"Found {total_locators} locators in {len(section_locators)} sections\n")
    
    # Validate each section
    all_missing = []
    all_orphaned = []
    
    for section_num in sorted(section_locators.keys()):
        locators = section_locators[section_num]
        
        if args.verbose:
            print(f"Section {section_num}:")
        
        missing, orphaned = validate_section(
            section_num, locators, sources_dir, args.verbose
        )
        
        for m in missing:
            all_missing.append((section_num, m))
        for o in orphaned:
            all_orphaned.append((section_num, o))
        
        if args.verbose:
            if missing:
                print(f"    Missing in sidecar: {len(missing)}")
            if orphaned:
                print(f"    Orphaned in sidecar: {len(orphaned)}")
            print()
    
    # Summary
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    if all_missing:
        print(f"\n❌ MISSING IN SIDECAR ({len(all_missing)} entries):")
        print("   These locators are in the manuscript but not in sidecar YAML:")
        for section, locator in all_missing[:20]:  # Limit output
            print(f"   - [{section}] {locator}")
        if len(all_missing) > 20:
            print(f"   ... and {len(all_missing) - 20} more")
    
    if all_orphaned:
        print(f"\n⚠️  ORPHANED IN SIDECAR ({len(all_orphaned)} entries):")
        print("   These sidecar entries have no matching manuscript locator:")
        for section, locator in all_orphaned[:20]:
            print(f"   - [{section}] {locator}")
        if len(all_orphaned) > 20:
            print(f"   ... and {len(all_orphaned) - 20} more")
    
    if not all_missing and not all_orphaned:
        print("\n✅ All locators validated successfully!")
    
    print(f"\nTotal: {total_locators} locators, {len(all_missing)} missing, {len(all_orphaned)} orphaned")
    
    return 1 if all_missing else 0


if __name__ == '__main__':
    exit(main())
