# Mission analysis

## User needs {#sec:user-needs}

This section identifies the stakeholder needs that drive the Mars UAV design. User needs express what capabilities are required without specifying numerical values; the quantitative requirements derived from these needs are documented in @sec:derived-requirements. The needs are organized into three categories: mission capability needs define the functional objectives the UAV must achieve, operational safety needs address reliability and robustness during flight operations, and environmental compatibility needs ensure the system can function within Mars-specific physical constraints.

@Tbl:user-needs-summary provides a consolidated view of all user needs organized by category.

: Summary of user needs {#tbl:user-needs-summary}

| ID  | Category                  | Need                         |
|-----|---------------------------|------------------------------|
| N1  | Mission capability        | Extended operational range   |
| N2  | Mission capability        | Aerial imaging               |
| N3  | Mission capability        | Communication relay          |
| N4  | Mission capability        | Vertical takeoff and landing |
| N5  | Mission capability        | Extended endurance           |
| N6  | Operational safety        | Single-fault tolerance       |
| N7  | Operational safety        | Wind tolerance               |
| N8  | Operational safety        | Dust ingress protection      |
| N9  | Environmental compatibility | Electric propulsion        |
| N10 | Environmental compatibility | Radiation tolerance        |
| N11 | Environmental compatibility | Thermal compatibility      |

### Mission capability needs

Mission capability needs define what the UAV must accomplish to fulfill its scientific and operational objectives. These needs establish the core functionality required for reconnaissance, survey, and communication relay missions.

* N1. Extended operational range: the UAV shall provide aerial survey capability beyond the practical range of surface rovers. Current Mars rovers have traversed less than 50 km over multi-year missions, limiting the accessible area around landing sites. An airborne platform can survey larger areas in less time, enabling reconnaissance of sites that would otherwise require years of rover travel or remain inaccessible.
* N2. Aerial imaging: the UAV shall carry a camera system capable of acquiring geological survey imagery. This supports the primary mission objective of mapping terrain, identifying scientifically interesting sites, and providing context for surface operations.
* N3. Communication relay: the UAV shall carry a radio system capable of extending communication range for EVA (extra-vehicular activity) operations. Surface radio communications are limited by line-of-sight constraints and terrain shadowing; an airborne relay station can extend the safe operational range of crewed surface activities.
* N4. Vertical takeoff and landing: the UAV shall be capable of operating without prepared runways or landing strips. The Mars surface offers no infrastructure for conventional aircraft operations; all takeoffs and landings must occur from unprepared terrain near the habitat.
* N5. Extended endurance: the UAV shall provide sufficient flight time to complete an out-and-back mission with survey time at the target location. Brief flights, as demonstrated by Ingenuity, are insufficient for the envisioned reconnaissance and relay missions. The endurance must accommodate transit, survey operations, and return with appropriate margins.

### Operational safety needs

Operational safety needs address the reliability and robustness requirements that ensure mission success despite the hostile operating environment and the impossibility of in-flight intervention.

* N6. Single-fault tolerance: the UAV shall maintain safe operation following any single system failure. In-flight repair is not possible, and maintenance opportunities are limited. The design must accommodate component failures without catastrophic loss of the vehicle.
* N7. Wind tolerance: the UAV shall operate safely in typical Martian wind conditions. Mars experiences regular afternoon wind peaks that the vehicle must withstand without loss of control or structural damage.
* N8. Dust ingress protection: the UAV shall be protected against Martian dust. The fine regolith (particle sizes 1-100 μm) can degrade mechanical bearings, contaminate optical surfaces, and reduce thermal management effectiveness. Dust protection is necessary for reliable operation over the mission lifetime.

### Environmental compatibility needs

Environmental compatibility needs derive from the fundamental physical constraints of Mars, including its atmospheric composition, radiation environment, and thermal conditions. These needs cannot be traded against performance; non-compliance results in system failure.

* N9. Electric propulsion: the UAV shall use electric propulsion systems. The Martian atmosphere lacks oxygen for combustion, precluding conventional internal combustion engines. Battery-electric or solar-electric systems are the only practical options.
* N10. Radiation tolerance: the UAV electronics and materials shall withstand the Mars surface radiation environment. The combination of galactic cosmic radiation and solar particle events creates a radiation environment that commercial electronics must tolerate over the mission duration.
* N11. Thermal compatibility: the UAV shall operate within the Mars thermal environment. Diurnal temperature swings and low ambient temperatures (-80°C to +20°C) impose constraints on materials, mechanisms, and especially battery performance.
