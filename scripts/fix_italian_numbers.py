#!/usr/bin/env python3
"""
Convert Italian number format to English format in markdown files.
Italian: comma for decimal (1,234) and point for thousands (1.000)
English: point for decimal (1.234) and comma for thousands (1,000)

This script focuses on the common patterns in the manuscript:
- Decimal numbers like 4,01 → 4.01
- Numbers like 0,5 → 0.5
- Percentages like 23,2% → 23.2%
"""

import re
from pathlib import Path
import sys


def convert_number(match: re.Match) -> str:
    """Convert a matched Italian-format number to English format."""
    num = match.group(0)
    # Replace comma with point for decimal separator
    # Be careful: we're only replacing commas that are decimal separators
    # (i.e., followed by digits, not by space)
    return num.replace(',', '.')


def process_file(filepath: Path, dry_run: bool = True) -> list[tuple[int, str, str]]:
    """
    Process a single file and convert Italian numbers to English format.
    Returns a list of (line_number, original_line, new_line) tuples for changes.
    """
    changes = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for i, line in enumerate(lines, 1):
        original = line
        
        # Pattern to match Italian decimal numbers:
        # - Integer part (one or more digits)
        # - Comma (Italian decimal separator)
        # - Decimal part (one or more digits)
        # BUT avoid matching things like list items "1, 2, 3" or text commas
        # We need comma IMMEDIATELY followed by digit(s) without space
        
        # Match patterns like: 4,01  0,5  2,686  23,2%  -3,5
        # This pattern: number followed by comma followed by digits (no space)
        pattern = r'(\d+),(\d+)'
        
        new_line = re.sub(pattern, r'\1.\2', line)
        
        if new_line != original:
            changes.append((i, original.rstrip(), new_line.rstrip()))
        
        new_lines.append(new_line)
    
    if not dry_run and changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return changes


def main():
    sections_dir = Path(r"c:\Users\matti\OneDrivePhD\Dev\Drone_marte\sections_it")
    
    # First pass: dry run to show what will change
    dry_run = '--apply' not in sys.argv
    
    if dry_run:
        print("=" * 80)
        print("DRY RUN - No changes will be made. Use --apply to make changes.")
        print("=" * 80)
    else:
        print("=" * 80)
        print("APPLYING CHANGES")
        print("=" * 80)
    
    total_changes = 0
    files_changed = 0
    
    for md_file in sorted(sections_dir.glob('*.md')):
        changes = process_file(md_file, dry_run=dry_run)
        if changes:
            files_changed += 1
            print(f"\n📄 {md_file.name}:")
            for line_num, old, new in changes:
                print(f"  Line {line_num}:")
                print(f"    - {old}")
                print(f"    + {new}")
            total_changes += len(changes)
    
    print("\n" + "=" * 80)
    print(f"Summary: {total_changes} changes in {files_changed} files")
    if dry_run:
        print("Run with --apply to make the changes.")
    else:
        print("Changes applied successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
