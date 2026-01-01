# Manuscript and Sizing Code Review

## Scope
- Manuscript: `drone.md`
- Code: `src/mars_uav_sizing/` (config, section3, section4, section5, verification)
- Goal: assess completeness and correctness of concepts, equations, and computed results

## Findings

### Critical
- Placeholder sections indicate incomplete manuscript content for key design decisions (airfoil selection, geometry selection, material selection). These sections are explicitly marked as TODO and therefore are not complete. (`drone.md:2306`, `drone.md:2312`, `drone.md:2322`)
- Conflicting baselines and results are present across the manuscript, which makes the calculation results internally inconsistent and not verifiable:
  - Baseline MTOW is 10 kg in sizing sections, but later design decisions use 3.3 kg. (`drone.md:780`, `drone.md:2236`, `drone.md:2434`)
  - Wing area and wing loading are derived as ~4.1 m^2 and ~9 N/m^2 in the Reynolds-number sizing, but later design point summary uses ~0.72 m^2 and ~17 N/m^2. (`drone.md:989-1005`, `drone.md:2234-2238`)
  - Aspect ratio is 6 in derived requirements, but the design point summary uses AR = 12. (`drone.md:1096-1102`, `drone.md:2238`)
  - Hybrid VTOL performance claims (108 min endurance, 252 km range, 146 Wh required / 237 Wh available) do not align with the sizing inputs and code outputs based on 10 kg MTOW and 270 Wh/kg batteries. (`drone.md:2213-2219`)

### Major
- Atmospheric pressure equation mismatch: the manuscript uses a lapse-rate power law, but the code uses an exponential (isothermal-style) formula with local temperature. This is a different equation than the manuscript’s @eq:pressure. (`drone.md:81`, `src/mars_uav_sizing/section3/atmospheric_model.py:56`)
- Sutherland constant mismatch between manuscript and config: manuscript uses S = 222 K, config uses C = 240 K. This changes viscosity and Reynolds number results. (`drone.md:99`, `src/mars_uav_sizing/config/physical_constants.yaml:60`)
- Derived requirements in the manuscript compute chord from Reynolds number (c = 0.83 m) and wing area (S = 4.1 m^2). The code does not implement that derivation and instead uses hardcoded chord and wing-loading defaults, leading to different geometry and Reynolds numbers. (`drone.md:989-1005`, `src/mars_uav_sizing/section3/atmospheric_model.py:209`, `src/mars_uav_sizing/section4/derived_requirements.py:44`, `src/mars_uav_sizing/section4/derived_requirements.py:119`, `src/mars_uav_sizing/section4/derived_requirements.py:166`)
- Fixed-wing endurance calculation: the manuscript’s numeric result implicitly applies the 20% energy reserve (121 min), but the equation shown does not include reserve and the code does not apply reserve in fixed-wing endurance. This yields a higher endurance in code (~151 min) and conflicts with the manuscript. (`drone.md:1581-1587`, `src/mars_uav_sizing/section5/fixed_wing.py:529-533`)
- Stall constraint is inconsistent across manuscript and code:
  - Manuscript derives V_min = 1.2 * V_stall from W/S ~9 N/m^2 (V_stall = 27.67 m/s). (`drone.md:1010-1038`)
  - Manuscript later uses V_stall = 30 m/s and W/S = 7.3 N/m^2 for the matching chart, conflicting with the earlier derivation. (`drone.md:1450`, `drone.md:1522-1530`, `drone.md:2056`)
  - Code uses v_stall directly (no 1.2 factor) in the matching chart, which does not align with the V_min-based constraint definition in Section 4.12. (`src/mars_uav_sizing/section5/matching_chart.py:85`)
- Geometry calculations rely on hardcoded assumptions not present in config or clearly documented in the manuscript (wing loading 10 N/m^2, tail moment arm = 0.6 * fuselage length, V-tail AR = 4.0, 4 rotors). These materially affect tail and rotor sizing while reducing traceability. (`src/mars_uav_sizing/section4/geometry_calculations.py:274-289`, `src/mars_uav_sizing/section4/geometry_calculations.py:117`)

### Minor
- The verification script prints Unicode check marks and fails under the default Windows cp1252 console encoding unless `PYTHONIOENCODING=utf-8` is set, which can block verification runs. (`src/mars_uav_sizing/verification/verify_manuscript.py:33`)

## Verification Notes
- Command executed: `python -m mars_uav_sizing.verification.verify_manuscript` (with `PYTHONIOENCODING=utf-8`).
- Outcome: 10/10 checks passed, but the coverage is limited (a small subset of values only). Several key inconsistencies listed above are not checked by the verifier.

## Conclusion
The manuscript and code are not fully complete or consistent. There are unresolved placeholders, multiple conflicting baselines, mismatched equations/parameters, and untracked hardcoded assumptions that prevent confirming correctness across all concepts, equations, and computed results.
