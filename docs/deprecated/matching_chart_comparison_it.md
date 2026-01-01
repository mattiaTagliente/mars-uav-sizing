# Confronto Completo: Matching Charts per Jet Regionale vs. Progetto UAV Marziano

**Documento:** Confronto metodologico e guida all'adattamento  
**Data:** 2025-12-23  
**Script di riferimento:** `C:\Users\matti\OneDrive - Politecnico di Bari\5.5 IELTS\progettazione\Profilo\matchingcharts.m`

---

## 1. Funzione dello Script Originale

### Scopo

Lo script `matchingcharts.m` esegue un **dimensionamento simultaneo basato su vincoli** per un **jet regionale da 100 passeggeri** risolvendo un sistema di 5 equazioni non lineari che accoppiano:

1. **Bilancio dei pesi** (chiusura delle masse)
2. **Vincolo di decollo** (lunghezza pista)
3. **Vincolo di atterraggio** (lunghezza pista)
4. **Vincolo di crociera** (spinta per volo livellato)
5. **Vincolo di autonomia** (equazione di Breguet)

Lo script utilizza `fsolve` di MATLAB con l'algoritmo di Levenberg-Marquardt per trovare il punto di progetto in cui tutti i vincoli sono simultaneamente soddisfatti.

### Caratteristiche Principali

- **Tipo di aeromobile**: Jet regionale convenzionale con turbofan
- **Passeggeri**: 100 (npax = 100)
- **Propulsione**: Motore a getto (basato sulla spinta, combustione di carburante)
- **Configurazione**: Convenzionale (senza VTOL)
- **Ambiente operativo**: Terra (livello del mare + quota di crociera)

---

## 2. Input e Output

### Parametri di Input (Costanti Fisse)

| Categoria | Parametro | Simbolo | Valore | Descrizione |
|-----------|-----------|---------|--------|-------------|
| **Passeggeri** | Numero passeggeri | `npax` | 100 | Carico utile di progetto |
| **Geometria** | Lunghezza fusoliera | `Lfus` | 36,0 m | Lunghezza totale |
| | Raggio fusoliera | `Rfuso` | 1,46 m | Sezione trasversale |
| | Rapporto di rastremazione | `lambda_taper` | 0,4 | Pianta alare |
| | Angolo di freccia | `sweep25_deg` | 25° | Al 25% della corda |
| | Spessore relativo | `tc` | 0,14 | Spessore relativo |
| **Aerodinamica** | $C_{L,max}$ (TO) | `Clmaxto` | 2,3 | Con dispositivi ipersostentatori |
| | Fattore di Oswald | `osw` | 0,93 | Efficienza di campata |
| | Numero di Mach | `M` | 0,7 | Crociera |
| **Prestazioni** | Velocità di crociera | `V` | 221,2 m/s | A Mach 0,7 |
| | Autonomia | `A` | 1852 km | 1000 nm |
| | Lunghezza decollo | `Lto` | 1400 m | Pista |
| | Lunghezza atterraggio | `Lland` | 1250 m | Pista |
| | Decelerazione | `abb` | 1,9 m/s² | Frenata |
| **Atmosfera** | Densità al decollo | `rhoto` | 1,225 kg/m³ | Livello del mare |
| | Densità di crociera | `rho` | 0,6527 kg/m³ | ~6 km di quota |
| | Viscosità cinematica | `nu` | 2,44×10⁻⁵ m²/s | |
| **Propulsione** | Fattore di manetta | `zeta` | 0,685 | Frazione di spinta massima |
| | Correzione di quota | `psi` | 0,5951 | Rapporto pressione/temperatura |
| | SFC base | `cs0` | 0,7/3600 kg/N/s | Consumo specifico |
| **Carichi** | Fattore di carico ultimo | `Nult` | 5,7 (1,5×3,8) | Certificazione CS-25 |

### Variabili di Ottimizzazione (Risolte)

| Variabile | Simbolo | Stima Iniziale | Descrizione |
|-----------|---------|----------------|-------------|
| **Peso** | `W` | 445.000 N | Peso totale |
| **Carico alare** | `S_W` | ~5200 N/m² | W/S |
| **Carico di spinta** | `T_S` | ~1675 N/m² | T/S |
| **Allungamento alare** | `lam` | 9,17 | Vincolato [6, 12] |
| **Frazione di carburante** | `k` | 0,35 | Wf/W |

### Output (Risultati)

| Output | Simbolo | Unità | Descrizione |
|--------|---------|-------|-------------|
| Superficie alare | `S` | m² | S = (W/S) × W |
| Apertura alare | `b` | m | √(S × λ) |
| MAC | `c` | m | Corda media aerodinamica |
| Spinta totale | `T` | N | T = (T/S) × S |
| $C_L$ di crociera | `Cl` | — | Coefficiente di portanza in volo livellato |
| $C_D$ di crociera | `Cd` | — | Dalla polare di resistenza |
| L/D | `Eff` | — | Efficienza aerodinamica |

---

## 3. Le Cinque Equazioni di Vincolo

### Equazione 1: Bilancio dei Pesi

```matlab
equ1 = (Qala + Qfus + Qimp + Qcarr + Qmot + Qfisso + Qf + Qimpianti)*g - W == 0;
```

La somma delle masse dei componenti eguaglia l'MTOW:
$$W = g \cdot (m_{ala} + m_{fus} + m_{coda} + m_{carrello} + m_{motori} + m_{fisso} + m_{carburante} + m_{sistemi})$$

### Equazione 2: Vincolo di Decollo

$$\frac{T}{S} = \left(\frac{W}{S}\right)^2 \cdot \frac{1,75}{g \cdot C_{L,max} \cdot x_{fr} \cdot L_{TO} \cdot \rho_{TO}}$$

### Equazione 3: Vincolo di Atterraggio

$$\frac{W}{S} = \frac{L_{land}}{1,66} \cdot a_{frenata} \cdot \rho \cdot C_{L,max} \cdot (1 - a \cdot k_{carburante})$$

### Equazione 4: Vincolo di Crociera

$$\frac{T}{S} = \frac{1}{\psi \cdot \zeta} \cdot \frac{1}{2} \rho V^2 C_D$$

### Equazione 5: Vincolo di Autonomia (Breguet)

$$R = \frac{V}{c_s} \cdot \frac{L}{D} \cdot \ln\left(\frac{1}{1 - a \cdot k_{carburante}}\right)$$

---

## 4. Confronto con il Progetto UAV Marziano

### 4.1 Disponibilità degli Input

| Categoria Input | Jet Regionale | UAV Marziano | Disponibile? | Note |
|-----------------|---------------|--------------|--------------|------|
| **Carico utile** | 100 pax (~10.000 kg) | 0,5 kg camera | ✅ Diverso | Molto più semplice per UAV |
| **Geometria fusoliera** | Lfus=36m, R=1,46m | ~1,5m di lunghezza | ✅ Diverso | Ordini di grandezza più piccolo |
| **Geometria alare** | λ=6-12, Λ=25°, t/c=0,14 | λ=10-14, Λ=0°, t/c=0,10 | ✅ Adattabile | Alto AR necessario per Marte |
| **$C_{L,max}$** | 2,3 (con flap) | 1,2-1,4 (pulito, basso Re) | ✅ Diverso | Profili basso-Re, senza flap |
| **Velocità di crociera** | 221,2 m/s | 35-40 m/s | ✅ Diverso | Molto più lento |
| **Autonomia** | 1852 km | 10-50 km | ✅ Diverso | Missioni locali |
| **Lunghezza decollo** | 1400 m | N/A (VTOL) | ❌ **Non applicabile** | Nessuna pista su Marte |
| **Lunghezza atterraggio** | 1250 m | N/A (VTOL) | ❌ **Non applicabile** | Nessuna pista su Marte |
| **Atmosfera ρ** | 1,225 / 0,6527 kg/m³ | 0,020 kg/m³ | ✅ Diverso | 60× più rarefatta |
| **Gravità** | 9,81 m/s² | 3,711 m/s² | ✅ Diverso | 38% della Terra |
| **SFC** | 0,7 kg/N/h | N/A (elettrico) | ❌ **Non applicabile** | Batteria, non carburante |

### 4.2 Requisiti di Output

| Output | Jet Regionale | UAV Marziano | Necessario? |
|--------|---------------|--------------|-------------|
| **Peso totale W** | ✅ Sì | ✅ Sì | ✅ Stesso |
| **Carico alare W/S** | ✅ Sì | ✅ Sì | ✅ Stesso |
| **Carico di spinta T/S** | ✅ Sì | ⚠️ Carico di potenza P/W | ⚠️ Diverso |
| **Frazione di carburante k** | ✅ Sì | ⚠️ Frazione batteria | ⚠️ Diverso |

### 4.3 Trasformazioni delle Variabili

Le seguenti variabili richiedono una trasformazione dalla formulazione del jet regionale alla formulazione dell'UAV elettrico:

| Variabile Jet Regionale | Simbolo | Variabile UAV Marziano | Simbolo | Trasformazione |
|-------------------------|---------|------------------------|---------|----------------|
| Carico di spinta | `T_S` [N/m²] | Carico di potenza | `P_W` [W/N] | P = T × V / η_elica |
| Frazione di carburante | `k` [-] | Frazione batteria | `f_batt` [-] | Nessuna riduzione di massa durante il volo |
| Consumo specifico | `cs` [kg/N/s] | Energia specifica | `e_spec` [Wh/kg] | Basato su energia, non flusso di massa |
| Fattori quota/manetta | `psi, zeta` [-] | Efficienze propulsive | `η_elica, η_motore` [-] | Basato su efficienza |
| Spinta di crociera | `T` [N] | Potenza di crociera | `P_cruise` [W] | P = D × V / η_elica |
| N/A | — | Potenza di hovering | `P_hover` [W] | Dalla teoria del momento |

### 4.4 Mappatura dei Termini di Massa (Termini Q)

Lo script originale usa termini Q per le masse dei componenti. Ecco come si mappano all'UAV marziano:

| Termine Jet Regionale | Descrizione | Equivalente UAV Marziano | Note |
|-----------------------|-------------|--------------------------|------|
| `Qala` | Massa alare | Struttura alare | Formula Sadraey con K_rho adattato |
| `Qfus` | Massa fusoliera | Fusoliera + trave di coda | Scalato a dimensioni minori |
| `Qimp` | Impennaggi (superfici di coda) | Superfici di coda | Formula simile, scala minore |
| `Qcarr` | Carrello di atterraggio | **Carrello/gambe di atterraggio** | L'UAV necessita di gambe per VTOL |
| `Qmot` | Motori a getto | **Motori + ESC + eliche** | Tutti i componenti propulsivi |
| `Qimpianti` | Sistemi/equipaggiamenti | Avionica + gestione termica | ~5-8% di MTOW |
| `Qfisso` | Fisso/carico utile | Carico utile (camera, radio) | 0,5 kg fisso |
| `Qf` | Carburante | **Batteria + montaggio** | Massa fissa durante il volo |
| — | N/A | Bracci motore/supporti | Nuovo termine strutturale se necessario |

**Differenza chiave**: Nel jet regionale, `Qmot` include solo la massa dei motori. Per l'UAV, `Qmot` deve includere:
- Motori di sollevamento (8×)
- Motori di crociera (2×)
- ESC (tutti 10)
- Eliche (10 totali: 8 lift + 2 cruise)
- Cablaggio e connettori

Analogamente, `Qf` (carburante→batteria) deve includere l'hardware di montaggio batteria e i materiali di interfaccia termica.

---

## 5. Modifiche e Adattamenti Necessari

### 5.1 Propulsione di Sollevamento vs. Crociera: Trattamento Separato Richiesto

Per una configurazione QuadPlane, i sistemi di propulsione per il sollevamento e la crociera sono **fondamentalmente diversi** e devono essere trattati separatamente:

| Aspetto | Propulsione di Sollevamento | Propulsione di Crociera |
|---------|----------------------------|-------------------------|
| **Funzione** | Decollo/atterraggio verticale | Volo in avanti |
| **Tipo di motore** | Alta coppia, basso KV | Alta efficienza, KV medio |
| **Tempo operativo** | 2-3 minuti per volo | 60-90 minuti per volo |
| **Vincolo di dimensionamento** | Potenza di hovering (teoria del momento) | Resistenza di crociera (L/D) |
| **Numero di unità** | 8 motori (ottocottero) | 2 motori (tractor coassiale) |
| **Tipo di elica** | Passo fisso, piccolo diametro | Variabile/fisso, grande diametro |
| **Carico del disco** | 100-150 N/m² (efficienza) | N/A (dimensionamento basato sulla spinta) |

#### Nuove Variabili per la Propulsione di Sollevamento

| Variabile | Simbolo | Valore Tipico | Fonte |
|-----------|---------|---------------|-------|
| Carico del disco | $DL$ | 100-150 N/m² | Ottimizzazione teoria del momento |
| Numero di rotori di sollevamento | $n_{lift}$ | 8 | Ottocottero per ridondanza |
| Diametro rotore di sollevamento | $D_{lift}$ | 0,22-0,27 m | Da DL e peso |
| Figura di merito | $FM$ | 0,6-0,7 | Efficienza piccoli rotori [@johnsonMarsScienceHelicopter2020] |
| Potenza motore di sollevamento (ciascuno) | $P_{lift}$ | 450-600 W | Da potenza hover / n_lift |
| Massa motore di sollevamento (ciascuno) | $m_{motor,lift}$ | 0,15-0,25 kg | Schede tecniche motori |

#### Nuove Variabili per la Propulsione di Crociera

| Variabile | Simbolo | Valore Tipico | Fonte |
|-----------|---------|---------------|-------|
| Numero di motori di crociera | $n_{cruise}$ | 2 | Ridondanza tractor coassiale |
| Diametro elica di crociera | $D_{cruise}$ | 0,6-0,8 m | Scalato dai riferimenti |
| Efficienza dell'elica | $\eta_{prop}$ | 0,50-0,65 | Condizioni Marte basso Re |
| Potenza motore di crociera (ciascuno) | $P_{cruise}$ | 180-210 W | Dalla resistenza a V_cruise |
| Massa motore di crociera (ciascuno) | $m_{motor,cruise}$ | 0,3-0,5 kg | Schede tecniche motori |

### 5.2 Stime delle Frazioni di Massa con Fonti

Le seguenti frazioni di massa sono derivate dalla letteratura e dai dati di riferimento:

#### Struttura e Cellula

| Componente | Frazione di MTOW | Fonte |
|------------|------------------|-------|
| Struttura alare | 10-15% | Raymer, adattato per UAV [@sadraeyAircraftDesignSystematic2013] |
| Fusoliera + trave di coda | 8-12% | Dati statistici piccoli UAV |
| Bracci motore/supporti | 3-5% | Strutture QuadPlane |
| Carrello di atterraggio (gambe/pattini) | 2-4% | Necessario per operazioni VTOL a terra |
| **Totale struttura** | **23-35%** | Coerente con 28% per eVTOL a decollo verticale [studio NLR] |

*Nota: Per piccoli UAV (MTOW < 50 kg), la frazione di peso a vuoto è tipicamente del 40-60%, di cui la struttura comprende circa la metà. Il carrello di atterraggio è essenziale per le operazioni VTOL e non può essere omesso.*

#### Sistema di Propulsione

| Componente | Frazione di MTOW | Fonte |
|------------|------------------|-------|
| Motori di sollevamento (8×) | 5-8% | Da dati UAV di riferimento: 9-10% motori totali |
| Motori di crociera (2×) | 2-4% | Da dati UAV di riferimento |
| ESC | 1-2% | Circa 15-25% della massa dei motori [@oscarliang_esc] |
| Eliche | 1-2% | Pale in composito con nucleo in schiuma ~28g ciascuna [@nasa_ingenuity] |
| Cablaggio/connettori | 0,5-1% | Tabelle calibro fili: 14-20 AWG, dipendente dalla lunghezza |
| **Totale propulsione** | **10-15%** | |

*Stima massa ESC: ESC 4-in-1 moderni pesano 12-15g per piccoli droni; ESC discreti più grandi 40-60g ciascuno. Per 8 motori lift + 2 cruise con ESC medio 50g, totale ~500g ≈ 4% di 12 kg MTOW. Stima conservativa: 1-2% di MTOW.*

#### Accumulo di Energia

| Componente | Frazione di MTOW | Fonte |
|------------|------------------|-------|
| Pacco batterie | 29-40% | Dati UAV di riferimento (vedi sources/reference_drones.yaml) |
| Montaggio batteria | 1-2% | Isolamento vibrazioni, interfaccia termica |
| **Totale energia** | **30-42%** | |

*Riferimento: Batteria Ingenuity = 273g / 1800g = 15,2% di MTOW. Tuttavia, Ingenuity è ricaricato dal sole con autonomia minima. Per autonomia di crociera di 60-90 min, sono necessarie frazioni più alte (30-40%).*

#### Avionica e Sistemi

| Componente | Frazione di MTOW | Fonte |
|------------|------------------|-------|
| Flight controller + IMU | 0,5-1% | ~50-100g per autopiloti commerciali |
| GPS/navigazione | 0,3-0,5% | ~30-50g |
| Radio/telemetria | 0,5-1% | Incluse antenne |
| Sensori (aggiuntivi) | 0,3-0,5% | Temperatura, pressione, ecc. |
| Gestione termica | 1-3% | Riscaldatori per condizioni marziane |
| **Totale avionica/sistemi** | **3-6%** | |

*Nota: Per eVTOL UAM, l'avionica può essere il 27-68% del peso dei sistemi non strutturali [studio TE Connectivity]. Per UAV più semplici, 3-6% di MTOW è ragionevole.*

#### Riepilogo Budget di Massa (Mappato ai Termini Q)

| Categoria | Termine Q | Frazione di MTOW | Per UAV da 12 kg |
|-----------|-----------|------------------|------------------|
| Struttura alare | Qala | 12% | 1,44 kg |
| Fusoliera + coda | Qfus | 8% | 0,96 kg |
| Superfici di coda | Qimp | 3% | 0,36 kg |
| Carrello di atterraggio | Qcarr | 3% | 0,36 kg |
| Propulsione (motori, ESC, eliche, cablaggio) | Qmot | 12% | 1,44 kg |
| Avionica + termica | Qimpianti | 5% | 0,60 kg |
| Carico utile | Qfisso | 4% | 0,50 kg |
| Batteria + montaggio | Qf | 36% | 4,32 kg |
| **Margine** | — | **17%** | **2,02 kg** |
| **Totale** | — | **100%** | **12,0 kg** |

### 5.3 Sostituzioni Complete delle Equazioni

#### ❌ RIMUOVERE: Vincolo di Pista di Decollo

**Motivo**: L'UAV marziano usa VTOL; non c'è pista.

✅ **SOSTITUIRE CON: Vincolo di Potenza di Hovering**

Dalla teoria del momento:
$$P_{hover} = \frac{W^{3/2}}{FM \cdot \eta_{motor} \cdot \sqrt{2 \rho_{Marte} A_{disco}}}$$

Dove $A_{disco} = n_{lift} \cdot \pi (D_{lift}/2)^2$

#### ❌ RIMUOVERE: Vincolo di Pista di Atterraggio

**Motivo**: Nessun atterraggio su pista.

✅ **SOSTITUIRE CON: Vincolo di Stallo**

$$\left(\frac{W}{S}\right)_{max} = \frac{1}{2} \rho_{Marte} V_{stallo}^2 C_{L,max}$$

#### ❌ RIMUOVERE: Vincolo di Autonomia di Breguet

**Motivo**: Aeromobile elettrico; la massa della batteria non si riduce durante il volo.

✅ **SOSTITUIRE CON: Vincolo di Energia della Batteria**

$$E_{batteria} = m_{batt} \cdot e_{specifica} \cdot \eta_{scarica} \cdot DoD$$
$$E_{richiesta} = (P_{hover} \cdot t_{hover} + P_{crociera} \cdot t_{crociera}) \cdot riserva$$

#### ⚠️ MODIFICARE: Vincolo di Crociera

Da spinta a potenza:
$$\frac{P}{W} = \frac{V_{crociera}}{\eta_{elica}} \cdot \frac{C_D}{C_L}$$

### 5.4 Modifiche al Modello Atmosferico

| Parametro | Jet Regionale | UAV Marziano | Fattore |
|-----------|---------------|--------------|---------|
| Densità superficiale | 1,225 kg/m³ | 0,020 kg/m³ | 1/61 |
| Gravità | 9,81 m/s² | 3,711 m/s² | 0,38 |
| Velocità del suono | 340 m/s | 240 m/s | 0,71 |
| Viscosità cinematica | 1,5×10⁻⁵ m²/s | 5×10⁻⁴ m²/s | 33× |

### 5.5 Nuove Variabili Necessarie (Non presenti nello Script Originale)

Le seguenti variabili sono richieste per l'UAV marziano ma non hanno equivalenti nello script del jet regionale:

| Nuova Variabile | Simbolo | Valore Tipico | Unità | Scopo |
|-----------------|---------|---------------|-------|-------|
| **Carico del disco** | `DL` | 100-150 | N/m² | Dimensionamento rotori hover (trade-off efficienza) |
| **Numero di rotori di sollevamento** | `n_rot` | 8 | — | Configurazione hover (ottocottero) |
| **Diametro rotore di sollevamento** | `D_rot` | 0,22-0,27 | m | Da DL e peso |
| **Figura di merito** | `FM` | 0,60-0,70 | — | Fattore di efficienza rotore |
| **Numero di motori di crociera** | `n_cruise` | 2 | — | Configurazione tractor coassiale |
| **Diametro elica di crociera** | `D_cruise` | 0,6-0,8 | m | Dimensionato per spinta in crociera |
| **Potenza specifica motore lift** | `P/m_lift` | 4000-6000 | W/kg | Livello tecnologico motori |
| **Potenza specifica motore cruise** | `P/m_cruise` | 3000-5000 | W/kg | Livello tecnologico motori |
| **Energia specifica batteria** | `e_spec` | 150-270 | Wh/kg | Livello tecnologico batterie |
| **Profondità di scarica** | `DoD` | 0,80-0,90 | — | Capacità utilizzabile batteria |
| **Tempo di hovering** | `t_hover` | 90-180 | s | Profilo missione: decollo + atterraggio |
| **Tempo di crociera** | `t_cruise` | 3600-5400 | s | Profilo missione: 60-90 min |
| **Efficienza elica (crociera)** | `η_elica` | 0,50-0,65 | — | Condizioni Marte basso Re |
| **Efficienza motore** | `η_motore` | 0,82-0,88 | — | Motore elettrico |
| **Efficienza ESC** | `η_ESC` | 0,95-0,98 | — | Elettronica di potenza |
| **Gravità marziana** | `g_Mars` | 3,711 | m/s² | Costante |
| **Densità marziana (Arcadia)** | `ρ_Mars` | 0,020 | kg/m³ | A -3 km di elevazione |
| **Viscosità dinamica marziana** | `μ_Mars` | 1,0×10⁻⁵ | Pa·s | CO₂ a ~220 K |

---

## 6. Sistema di Vincoli Proposto per l'UAV Marziano

### Nuovo Sistema di Equazioni

**Incognite**: W (peso), S (superficie alare), P_lift (potenza hover), P_cruise (potenza crociera), m_batt (massa batteria), λ (allungamento alare)

```
Equazione 1: Vincolo potenza di hovering (dalla teoria del momento)
Equazione 2: Vincolo potenza di crociera (dalla polare di resistenza)  
Equazione 3: Vincolo di stallo (carico alare massimo)
Equazione 4: Vincolo di energia (capacità batteria vs. energia missione)
Equazione 5: Bilancio delle masse (somma masse componenti = MTOW)
```

---

## 7. Riepilogo degli Adattamenti Necessari

### Da Cambiare (Differenze Fondamentali)

| Aspetto | Da | A | Motivo |
|---------|-----|---|--------|
| **Vincolo di decollo** | Lunghezza pista | Potenza di hovering | VTOL |
| **Vincolo di atterraggio** | Lunghezza pista | Velocità di stallo | VTOL + crociera ad ala fissa |
| **Equazione di autonomia** | Carburante Breguet | Energia batteria | Propulsione elettrica |
| **Spinta → Potenza** | T/S [N/m²] | P/W [W/N] | L'elettrico usa potenza |
| **Modello propulsivo** | SFC, bypass ratio | η_motore, η_elica | Basato su efficienza |
| **Frazione carburante** | Diminuisce durante il volo | Massa batteria fissa | Nessun cambiamento di massa |

### Adattabili (Stesso Concetto, Valori Diversi)

| Aspetto | Jet Regionale | UAV Marziano |
|---------|---------------|--------------|
| **Bilancio dei pesi** | Somma componenti | Somma componenti (componenti diversi) |
| **Vincolo di crociera** | Spinta = Resistenza | Potenza = Resistenza × V / η |
| **Polare di resistenza** | CD0 + kCL² | CD0 + kCL² (valori diversi) |
| **Solutore di ottimizzazione** | fsolve, Levenberg-Marquardt | Stesso approccio funziona |

### Nuove Aggiunte Richieste

| Nuovo Elemento | Scopo |
|----------------|-------|
| **Vincolo di hovering** | Dimensionare rotori di sollevamento |
| **Dimensionamento separato lift/cruise** | Configurazione QuadPlane |
| **Carico del disco** | Trade-off efficienza rotore |
| **Modello energia batteria** | Sostituire consumo carburante |
| **Modello atmosfera Marte** | ρ, g, μ |

---

## 8. Conclusioni

Lo script originale `matchingcharts.m` per jet regionale fornisce un **eccellente modello metodologico** ma richiede **adattamenti sostanziali** per l'UAV marziano:

1. **2 dei 5 vincoli devono essere completamente sostituiti** (decollo → hovering, atterraggio → stallo)
2. **1 vincolo deve essere fondamentalmente modificato** (Breguet → energia batteria)
3. **2 vincoli possono essere adattati** (crociera, bilancio masse)
4. **Propulsione di sollevamento e crociera devono essere trattate separatamente** per la configurazione QuadPlane
5. **Tutti i valori dei parametri** devono essere aggiornati per le condizioni marziane
6. **Le frazioni di massa** richiedono fonti specifiche (fornite sopra)

L'approccio del solutore iterativo e il concetto di soddisfacimento simultaneo dei vincoli rimangono validi. L'adattamento è abbastanza significativo da richiedere la scrittura di un **nuovo script specifico per Marte**, ispirato all'originale.

---

## Riferimenti

- Johnson, W. et al. (2020). "Mars Science Helicopter Conceptual Design." NASA/TM-2020-220485.
- Sadraey, M.H. (2013). "Aircraft Design: A Systems Engineering Approach." Wiley.
- Raymer, D.P. (2018). "Aircraft Design: A Conceptual Approach." AIAA Education Series.
- Barbato, G. et al. (2024). "Preliminary Design of a Fixed-Wing Drone for Mars Exploration." ICAS 2024.
- NASA Ingenuity Mars Helicopter fact sheet. mars.nasa.gov/technology/helicopter.
