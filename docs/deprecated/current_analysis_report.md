# Manuscript and code assessment (current state)

## Verification status
* `python -m mars_uav_sizing.verification.verify_manuscript` passes 193/193 checks.
* Hybrid VTOL expected values now include transition-phase terms.

## Updates applied
* Section 3.1 atmosphere table updated to match code outputs: $a$ = 229.7 m/s, $\mu$ = 1.098 × 10⁻⁵ Pa·s, $\nu$ = 5.611 × 10⁻⁴ m²/s, $\rho$ = 0.01957 kg/m³.
* Section 4.12 mission profile now uses 2 min hover + 1 min transition; cruise Mach updated to $M$ ≈ 0.1741 with $a$ = 229.7 m/s.
* Rotorcraft endurance updated to 63.17 min (2 min hover), with revised energy budget, range (146.8 km), and margin (+5.284%).
* Hybrid VTOL summary updated to 89.55 min endurance and 207.7 km range with transition energy included.
* Matching chart and architecture selection summaries updated to reflect new endurance and range values, and energy margin 43.20%.
* `source_grounding.txt` updated for rotorcraft endurance and Mach/speed-of-sound calculations.

## Notes
* Italian sections and `drone_it.md` have been updated to align with the English changes.
