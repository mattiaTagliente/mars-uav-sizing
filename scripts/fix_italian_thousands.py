#!/usr/bin/env python3
"""
Convert Italian thousands format to English format in markdown files.
Italian: point for thousands (55.000)
English: comma for thousands (55,000)

This script focuses on Reynolds numbers and similar large integers.
"""

import re
from pathlib import Path
import sys


def process_file(filepath: Path, dry_run: bool = True) -> list[tuple[int, str, str]]:
    """
    Process a single file and convert Italian thousands to English format.
    Returns a list of (line_number, original_line, new_line) tuples for changes.
    """
    changes = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for i, line in enumerate(lines, 1):
        original = line
        
        # Pattern to match Italian thousands separators for specific cases:
        # Numbers like 50.000, 55.000, 60.000, 90.000 (tens of thousands)
        # These are likely Reynolds numbers or similar integer values
        
        # Match patterns: \d{2}\.000 (like 50.000, 55.000) but NOT decimal values
        # Need to ensure we're not matching decimals like 3.711
        
        # Look for patterns where .000 is at word boundary (end of number)
        # This handles cases like "55.000" -> "55,000"
        
        # Pattern: 2-digit number followed by .000 at word boundary
        pattern = r'(\d{2})\.000\b'
        
        def replace_thousands(match):
            return f"{match.group(1)},000"
        
        new_line = re.sub(pattern, replace_thousands, line)
        
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
