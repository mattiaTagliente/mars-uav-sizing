#!/usr/bin/env python3
"""
parse_locators.py - Extract all [@key]<!-- #loc --> patterns from manuscript sections

This script parses manuscript markdown files and extracts all citation-locator pairs,
reporting them in a structured format for validation.

Usage:
    python parse_locators.py [sections_dir]
    
Output:
    JSON list of extracted locators with file, line, key, and locator info
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


# Pattern matches: [@citationKey] or [@citationKey, location]<!-- #locator -->
# Also handles optional space before comment: [@key] <!-- #loc -->
LOCATOR_PATTERN = re.compile(
    r'\[@([a-zA-Z][a-zA-Z0-9_:/-]*)'  # Citation key
    r'(?:[^\]]*)\]'                   # Optional location info (e.g., ", Chapter 5")
    r'\s*'                            # Optional whitespace
    r'<!--\s*#([a-z0-9:._-]+)\s*-->'  # Locator in HTML comment
)


def extract_locators_from_file(filepath: Path) -> List[Dict[str, Any]]:
    """Extract all locator patterns from a single markdown file."""
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return results
    
    for line_num, line in enumerate(lines, start=1):
        for match in LOCATOR_PATTERN.finditer(line):
            citation_key = match.group(1)
            locator = match.group(2)
            
            results.append({
                'file': str(filepath),
                'line': line_num,
                'citation_key': citation_key,
                'locator': locator,
                'composite_key': f"{citation_key}.{locator}"
            })
    
    return results


def extract_all_locators(sections_dir: Path) -> List[Dict[str, Any]]:
    """Extract locators from all markdown files in a directory."""
    all_results = []
    
    md_files = sorted(sections_dir.glob('*.md'))
    
    for md_file in md_files:
        file_results = extract_locators_from_file(md_file)
        all_results.extend(file_results)
    
    return all_results


def main():
    parser = argparse.ArgumentParser(
        description='Extract citation locator patterns from manuscript sections'
    )
    parser.add_argument(
        'sections_dir',
        nargs='?',
        default='sections_en',
        help='Directory containing markdown section files (default: sections_en)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output JSON file (default: print to stdout)'
    )
    parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Print summary statistics instead of full output'
    )
    
    args = parser.parse_args()
    
    sections_dir = Path(args.sections_dir)
    if not sections_dir.exists():
        print(f"Error: Directory not found: {sections_dir}")
        return 1
    
    results = extract_all_locators(sections_dir)
    
    if args.summary:
        # Print summary
        print(f"Total locators found: {len(results)}")
        
        # Count by file
        by_file = {}
        for r in results:
            fname = Path(r['file']).name
            by_file[fname] = by_file.get(fname, 0) + 1
        
        print("\nBy file:")
        for fname, count in sorted(by_file.items()):
            print(f"  {fname}: {count}")
        
        # Count by citation key
        by_key = {}
        for r in results:
            key = r['citation_key']
            by_key[key] = by_key.get(key, 0) + 1
        
        print("\nBy citation key (top 10):")
        for key, count in sorted(by_key.items(), key=lambda x: -x[1])[:10]:
            print(f"  {key}: {count}")
    else:
        # Output full results
        output = json.dumps(results, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Wrote {len(results)} locators to {args.output}")
        else:
            print(output)
    
    return 0


if __name__ == '__main__':
    exit(main())
