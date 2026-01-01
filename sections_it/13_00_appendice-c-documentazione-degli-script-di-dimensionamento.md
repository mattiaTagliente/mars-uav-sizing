# Appendice C: Documentazione degli script di dimensionamento

Questa appendice documenta il codebase Python utilizzato per i calcoli di dimensionamento in questo studio.

## Panoramica del pacchetto

I calcoli di dimensionamento del Mars UAV sono implementati nel pacchetto Python `mars_uav_sizing`, situato in:

```
src/mars_uav_sizing/
```

## Struttura delle directory

```
mars_uav_sizing/
├── config/                    # File di configurazione YAML
│   ├── physical_constants.yaml
│   ├── mars_environment.yaml
│   ├── propulsion_parameters.yaml
│   ├── battery_parameters.yaml
│   ├── aerodynamic_parameters.yaml
│   ├── geometry_parameters.yaml
│   └── mission_parameters.yaml
├── core/                      # Moduli fisici core
│   ├── atmosphere.py          # Modello atmosferico marziano
│   └── utils.py               # Utility comuni
├── section3/                  # Analisi di missione (§3)
│   └── atmospheric_model.py
├── section4/                  # Dati di riferimento (§4)
│   ├── aerodynamic_calculations.py
│   ├── derived_requirements.py
│   └── geometry_calculations.py
├── section5/                  # Analisi dei vincoli (§5)
│   ├── rotorcraft.py
│   ├── fixed_wing.py
│   ├── hybrid_vtol.py
│   ├── matching_chart.py
│   └── comparative.py
├── section6/                  # Decisioni progettuali (§6)
│   ├── airfoil_selection.py
│   └── airfoil_plots.py
├── section7/                  # Selezione componenti (§7)
│   ├── component_selection.py
│   └── mass_breakdown.py
├── visualization/             # Funzioni di plotting
│   └── plotting.py
├── verification/              # Verifica manoscritto
│   └── verify_manuscript.py
└── run_analysis.py            # Entry point principale
```

## Utilizzo

### Eseguire tutte le analisi

```bash
cd src
python -m mars_uav_sizing.run_analysis
```

### Eseguire script di sezione individuali

```bash
# Sezione 3 - Modello atmosferico
python -m mars_uav_sizing.section3.atmospheric_model

# Sezione 4 - Dati di riferimento
python -m mars_uav_sizing.section4.aerodynamic_calculations
python -m mars_uav_sizing.section4.derived_requirements

# Sezione 5 - Analisi dei vincoli
python -m mars_uav_sizing.section5.rotorcraft
python -m mars_uav_sizing.section5.fixed_wing
python -m mars_uav_sizing.section5.hybrid_vtol
python -m mars_uav_sizing.section5.matching_chart
python -m mars_uav_sizing.section5.comparative
```

### Accesso alla configurazione

Tutti i parametri sono caricati dai file di configurazione YAML:

```python
from mars_uav_sizing.config import get_param

# Costanti fisiche
g_mars = get_param('physical.mars.g')  # 3.711 m/s²

# Ambiente
rho = get_param('environment.arcadia_planitia.density_kg_m3')  # 0.0196

# Missione
v_cruise = get_param('mission.velocity.v_cruise_m_s')  # 40
mtow = get_param('mission.mass.mtow_kg')  # 10
```

## File di configurazione

: Contenuti file di configurazione {#tbl:config-files}

| File | Contenuto | Sezione |
|:-----|:--------|:--------|
| `physical_constants.yaml` | Gravità, costanti gas, parametri Sutherland | §3, Appendice A |
| `mars_environment.yaml` | Condizioni Arcadia Planitia | §3.1 |
| `propulsion_parameters.yaml` | FM, efficienza motore/ESC | §4.5 |
| `battery_parameters.yaml` | Energia specifica, DoD | §4.6 |
| `aerodynamic_parameters.yaml` | AR, e, CD0, CL_max | §4.7 |
| `geometry_parameters.yaml` | Carico disco, rastremazione | §4.12 |
| `mission_parameters.yaml` | Velocità, tempi, frazioni di massa | §3.2, §4.11, §4.12 |

## Formato output

Tutti gli script producono output console formattato con intestazioni di sezione chiare, parametri di input, valori calcolati e valutazioni di fattibilità.

