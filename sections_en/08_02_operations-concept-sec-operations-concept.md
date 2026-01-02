# Infrastructure requirements

## Operations concept {#sec:operations-concept}

This section defines the operational procedures for UAV missions from the Mars habitat, including mission phases, crew roles, and operational tempo.

### Mission phases

A typical UAV sortie consists of the following phases:

: UAV sortie phases and timeline {#tbl:sortie-phases}

| Phase | Location | Duration | Description |
|:------|:---------|:--------:|:------------|
| 1. Pre-flight preparation | Pressurised bay | 30 min | System checks, flight plan upload |
| 2. Transfer to airlock | Airlock | 10 min | UAV moved to transition zone |
| 3. Airlock depressurisation | Airlock | 5 min | Pressure reduction to Mars ambient |
| 4. Transfer to platform | External | 5 min | UAV positioned on launch pad |
| 5. VTOL takeoff | External | 2 min | Hover, transition, departure |
| 6. Outbound cruise | Airborne | 20-40 min | Transit to survey area |
| 7. Survey operations | Airborne | 20-60 min | Mapping or relay mission |
| 8. Return cruise | Airborne | 20-40 min | Transit to habitat |
| 9. VTOL landing | External | 2 min | Approach, transition, hover |
| 10. Transfer to airlock | Airlock | 5 min | UAV moved to transition zone |
| 11. Airlock repressurisation | Airlock | 5 min | Pressure increase to habitat |
| 12. Post-flight inspection | Pressurised bay | 30 min | Data download, system check |
| 13. Battery charging | Pressurised bay | 2-3 h | Recharge to full capacity |

Total sortie duration: 2.5-4.5 hours (ground phases), 1-2 hours (flight phases).

### Crew roles

UAV operations require minimal crew involvement due to autonomous flight capability:

UAV operator (1 person): Responsible for mission planning, flight monitoring, and data analysis. Operations are conducted from inside the habitat using ground control station.

EVA support (optional): For non-routine maintenance or recovery operations outside the pressurised bay.

### Operational tempo

The operational tempo is constrained by battery charging time and Mars solar day (sol) duration:

: Operational tempo analysis {#tbl:ops-tempo}

| Scenario | Flights/sol | Notes |
|:---------|:-----------:|:------|
| Single UAV | 1-2 | Limited by 2-3 h charging time |
| Two UAVs (alternating) | 3-4 | One flies while other charges |
| Sustained campaign | 1/sol average | Conservative for equipment longevity |

With two flight-ready UAVs, daily operations are feasible with alternating flights and charging cycles. Over a 30-sol mission campaign, approximately 30-60 sorties can be executed.

### Contingency operations

Contingency procedures address foreseeable failure modes: aborted takeoff (UAV remains on platform and crew retrieves via airlock procedure); in-flight emergency (autonomous return-to-base or emergency landing at alternate flat terrain); communication loss (pre-programmed return-to-base after configurable timeout, default 5 min); and landing failure (secondary landing zone designated with EVA recovery if required).

### Maintenance schedule

Scheduled maintenance between sorties:

: Maintenance schedule {#tbl:maintenance}

| Interval | Activity | Duration |
|:---------|:---------|:--------:|
| Each flight | Visual inspection, data download | 30 min |
| Every 5 flights | Propeller condition check, connector inspection | 1 h |
| Every 10 flights | Motor thermal assessment, bearing check | 2 h |
| Every 50 flights | Full system inspection, battery capacity test | 4 h |

