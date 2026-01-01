# Source attribution refinements

## Scope

This document adds small clarifications to the approved system while preserving the current locator format and the section-local sidecar model. The refinements avoid duplicate claim text, keep files small, and make parsing predictable.

## Locator normalization

* The inline locator keeps the hash prefix: `[@key]<!-- #loc -->`.
* The YAML key for the locator omits the hash: `loc:`. This avoids two spellings for the same locator and keeps keys compact.
* Locators are case-insensitive and stored lowercase in YAML. The inline form should also be lowercase for consistency.

## Allowed characters

* Locator tokens use only `a-z`, `0-9`, `:`, `.`, `_`, and `-`.
* Spaces are not allowed in locators.
* The sequence `--` is not allowed inside locators to avoid invalid HTML comment syntax.

## Optional range notation

* Ranges are expressed with a single dash inside the token, for example `p12-15` or `tbl3:r2-5`.
* A range refers to a single contiguous location and still maps to one YAML entry.

## YAML sidecar schema clarifications

* The existing `citationKey -> locator -> fields` structure remains unchanged.
* The `excerpt` and `context` fields remain required.
* The existing `note` field can hold extra disambiguation when a locator label is necessarily short.

## Parser tolerance

* Parsers should accept optional whitespace before the HTML comment: both `[@key]<!-- #loc -->` and `[@key] <!-- #loc -->` are valid.
* Parsers should treat `#loc` and `loc` as equivalent for lookup, after stripping a leading hash.

## Validation checks

* Each `[@key]<!-- #loc -->` in a section must have a matching entry in that section sidecar.
* Locator uniqueness is enforced per citation key within each sidecar file.
* `excerpt` length and `context` length limits are enforced to keep files concise.

## Workflow note

* No claim text is duplicated in YAML. The locator is the primary link between the manuscript and the sidecar entry.

