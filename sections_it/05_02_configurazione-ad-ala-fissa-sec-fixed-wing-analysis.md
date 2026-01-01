# Analisi dei vincoli {#sec:constraint-analysis-fixed-wing}

## Configurazione ad ala fissa {#sec:fixed-wing-analysis}

Questa sezione valuta se una configurazione ad ala fissa pura (aeroplano convenzionale) può soddisfare i requisiti di missione dell'UAV marziano. L'analisi sviluppa il quadro teorico per il volo livellato stazionario, la potenza di crociera e l'autonomia, dimostrando che sebbene l'ala fissa raggiunga un'efficienza aerodinamica superiore, la configurazione non soddisfa la missione a causa del requisito VTOL. Un aeromobile ad ala fissa convenzionale richiede un'infrastruttura di pista che non esiste su Marte.

### Fondamenti del volo livellato stazionario

#### Equilibrio delle forze

Nel volo livellato, stazionario e non accelerato, due coppie di forze devono essere in equilibrio [@torenbeekSynthesisSubsonicAirplane1982, Capitolo 5]<!-- #ch5 -->:

$$L = W$$ {#eq:lift-weight-equilibrium}

$$T = D$$ {#eq:thrust-drag-equilibrium}

dove $L$ è la portanza, $W$ è il peso dell'aeromobile, $T$ è la spinta, e $D$ è la resistenza. Queste condizioni fondamentali di equilibrio costituiscono la base per tutta l'analisi delle prestazioni.

#### Equazione della portanza

La forza di portanza aerodinamica è espressa come [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3]<!-- #ch5:s3 -->:

$$L = \frac{1}{2} \rho V^2 S C_L$$ {#eq:lift-equation}

dove $L$ è la forza di portanza (N), $\rho$ è la densità dell'aria (kg/m³), $V$ è la velocità vera (m/s), $S$ è l'area alare di riferimento (m²), e $C_L$ è il coefficiente di portanza (adimensionale).

Per il volo livellato dove $L = W$, il coefficiente di portanza richiesto per mantenere l'altitudine a una data velocità è:

$$C_L = \frac{2W}{\rho V^2 S} = \frac{2(W/S)}{\rho V^2}$$ {#eq:cl-required}

Questa equazione rivela un vincolo fondamentale per il volo su Marte: la bassa densità atmosferica ($\rho \approx 0.02000$ kg/m³) richiede alta velocità, grande superficie alare, o alto coefficiente di portanza per generare sufficiente portanza.

La resistenza aerodinamica totale è [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3]<!-- #ch5:s3:drag -->:

$$D = \frac{1}{2} \rho V^2 S C_D$$ {#eq:drag-equation}

Il coefficiente di resistenza è modellato utilizzando la polare di resistenza parabolica da @eq:drag-polar (secondo @sec:aerodynamic-analysis):

$$C_D = C_{D,0} + \frac{C_L^2}{\pi \cdot AR \cdot e}$$

dove $C_{D,0}$ è il coefficiente di resistenza a portanza nulla, $AR$ è l'allungamento alare, ed $e$ è il fattore di efficienza di Oswald. Il primo termine rappresenta la resistenza parassita (attrito superficiale, resistenza di forma, interferenza), che è indipendente dalla portanza. Il secondo termine è la resistenza indotta, derivante dall'ala ad apertura finita e proporzionale a $C_L^2$.

Utilizzando i valori da @tbl:aero-coefficients: $C_{D,0}$ = 0.03000, $e$ = 0.8692, $AR$ = 6.

### Rapporto portanza-resistenza

#### L/D dalla polare di resistenza

Il rapporto portanza-resistenza quantifica l'efficienza aerodinamica e determina direttamente le prestazioni di crociera [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.4]<!-- #ch5:s4 -->:

$$\frac{L}{D} = \frac{C_L}{C_D} = \frac{C_L}{C_{D,0} + C_L^2/(\pi \cdot AR \cdot e)}$$ {#eq:ld-ratio}

#### Rapporto portanza-resistenza massimo

Da @eq:ld-max-calculated e @eq:cl-optimum in @sec:aerodynamic-analysis, il massimo L/D si verifica al coefficiente di portanza ottimale dove la resistenza indotta eguaglia la resistenza parassita:

$$C_L^* = \sqrt{\pi \cdot AR \cdot e \cdot C_{D,0}} = 0.7011$$

$$(L/D)_\text{max} = \frac{1}{2}\sqrt{\frac{\pi \cdot AR \cdot e}{C_{D,0}}} = 11.68$$

Questo L/D massimo di 11.68 rappresenta un miglioramento rispetto al velivolo a rotore ($(L/D)_\text{eff}$ = 4.000, secondo @sec:rotorcraft-analysis) di un fattore di circa 3.

#### Velocità per L/D massimo

La velocità alla quale si verifica $(L/D)_\text{max}$ si trova sostituendo $C_L^*$ in @eq:cl-required:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2(W/S)}{\rho C_L^*}}$$ {#eq:v-ld-max}

Per l'UAV marziano con stima $W/S \approx 13.82$ N/m² (dal vincolo di stallo a $V_\text{min}$ = 35.04 m/s), $\rho$ = 0.01960 kg/m³, e $C_L^*$ = 0.7011:

$$V_{(L/D)\text{max}} = \sqrt{\frac{2 \times 13.82}{0.01960 \times 0.7011}} = \sqrt{2012} = 44.86 \text{ m/s}$$

Questa velocità ottimale è superiore alla velocità di crociera di progetto di 40.00 m/s, indicando che l'UAV marziano opererà a un coefficiente di portanza superiore a $C_L^*$ durante la crociera (nel regime dominato dalla resistenza indotta). A 40.00 m/s, l'L/D effettivo rimane vicino al massimo (circa 11.0 per l'ala pura, ridotto leggermente per la configurazione QuadPlane a causa della resistenza dei rotori fermi).

### Analisi della potenza di crociera

#### Potenza richiesta per il volo livellato

La potenza richiesta per vincere la resistenza in volo livellato è il prodotto della forza di resistenza e della velocità [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.4]<!-- #ch5:s4:power -->:

$$P_\text{aero} = D \times V$$ {#eq:power-aero}

Poiché $D = W/(L/D)$ in equilibrio:

$$P_\text{aero} = \frac{W \times V}{L/D}$$ {#eq:power-required}

Questa è la potenza aerodinamica che deve essere fornita al flusso d'aria per mantenere il volo livellato.

#### Potenza all'albero ed efficienza dell'elica

La potenza all'albero richiesta dal motore tiene conto dell'efficienza dell'elica [@torenbeekSynthesisSubsonicAirplane1982, Sezione 5.3.4]<!-- #ch5:s3.4 -->:

$$P_\text{albero} = \frac{P_\text{aero}}{\eta_\text{elica}} = \frac{W \times V}{(L/D) \times \eta_\text{elica}}$$ {#eq:shaft-power}

dove $\eta_\text{elica}$ è l'efficienza dell'elica. A bassi numeri di Reynolds su Marte, l'efficienza dell'elica è degradata rispetto alle condizioni terrestri.

#### Potenza elettrica

Includendo le efficienze del motore e dell'ESC, la potenza elettrica prelevata dalla batteria è:

$$P_\text{elettrica} = \frac{P_\text{albero}}{\eta_\text{motore} \times \eta_\text{ESC}} = \frac{W \times V}{(L/D) \times \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC}}$$ {#eq:cruise-electric-power}

L'efficienza propulsiva combinata è data da @eq:cruise-efficiency:

$$\eta_\text{crociera} = \eta_\text{elica} \times \eta_\text{motore} \times \eta_\text{ESC}$$

Utilizzando i valori di efficienza da @tbl:efficiency-parameters ($\eta_\text{elica}$ = 0.5500, $\eta_\text{motore}$ = 0.8500, $\eta_\text{ESC}$ = 0.9500), l'efficienza di crociera combinata è $\eta_\text{crociera}$ = 0.4436.

#### Formulazione del carico di potenza

Esprimendo il requisito di potenza come carico di potenza (potenza per unità di peso):

$$\frac{P}{W} = \frac{V}{(L/D) \times \eta_\text{crociera}}$$ {#eq:power-loading-cruise}

Per la crociera a $V$ = 40.00 m/s con $(L/D)$ = 11.68 e $\eta_\text{crociera}$ = 0.4436:

$$\frac{P}{W} = \frac{40.00}{11.68 \times 0.4436} = 7.719 \text{ W/N}$$

Convertendo in W/kg utilizzando la gravità marziana ($g_\text{Marte}$ = 3.711 m/s²):

$$\frac{P}{m} = 7.719 \times 3.711 = 28.64 \text{ W/kg}$$ {#eq:cruise-power-loading}

Per l'MTOW di base di 10.00 kg (peso $W$ = 37.11 N), la potenza di crociera è:

$$P_\text{crociera} = 7.719 \times 37.11 = 286.4 \text{ W}$$

Questo è inferiore al requisito di potenza di hovering di 3178 W calcolato in @sec:rotorcraft-analysis di un fattore 11, mostrando la riduzione di potenza ottenuta dalla crociera ad ala fissa.

### Vincolo di stallo

#### Velocità di stallo

La velocità minima di volo (velocità di stallo) si verifica al coefficiente di portanza massimo. Da @eq:stall-speed-prelim in @sec:mission-parameters:

$$V_\text{stallo} = \sqrt{\frac{2W}{\rho S C_{L,\text{max}}}} = \sqrt{\frac{2(W/S)}{\rho C_{L,\text{max}}}}$$

Questa equazione stabilisce la relazione tra carico alare e velocità di stallo.

#### Vincolo di carico alare

Il vincolo di stallo, espresso come carico alare massimo ammissibile, è derivato da @eq:wing-loading-constraint in @sec:mission-parameters:

$$\frac{W}{S} \leq \frac{1}{2} \rho V_\text{min}^2 C_{L,\text{max}}$$

Utilizzando $C_{L,\text{max}}$ = 1.150 (da @tbl:aero-coefficients), $\rho$ = 0.01960 kg/m³, e $V_\text{min}$ = 35.04 m/s (dove $V_\text{min}$ = 1.2 × $V_\text{stallo}$ secondo @eq:v-min-constraint, con $V_\text{stallo}$ = 29.2 m/s):

$$\frac{W}{S} \leq \frac{1}{2} \times 0.01960 \times 35.04^2 \times 1.150 = 13.82 \text{ N/m}^2$$

Questo vincola il carico alare massimo ammissibile. Su un diagramma di matching, questo appare come una linea verticale (W/S costante) indipendente dal carico di potenza.

Il vincolo di carico alare su Marte è estremamente basso rispetto agli aeromobili terrestri (tipico $W/S$ = 1500-5000 N/m² per aeromobili leggeri). Questa è una conseguenza diretta dell'atmosfera rarefatta e rappresenta un driver significativo della geometria dell'aeromobile.

Il diagramma di matching dell'ala fissa è presentato in @fig:matching-chart-fixed-wing in @sec:comparative-results.

### Analisi dell'autonomia

#### Modello dell'energia della batteria

L'energia disponibile dalla batteria utilizza @eq:battery-energy-fraction da @sec:battery-utilisation:

$$E_\text{disponibile} = f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}$$

Sostituendo i valori dei parametri da @tbl:design-mass-fractions ($f_\text{batt}$ = 0.3500) e @sec:energy-data ($e_\text{spec}$ = 270.0 Wh/kg, $DoD$ = 0.8000, $\eta_\text{batt}$ = 0.9500), l'energia utilizzabile per unità di MTOW è 71.82 Wh/kg. Per l'MTOW di base = 10.00 kg, l'energia disponibile è $E_\text{disponibile}$ = 718.2 Wh.

#### Equazione dell'autonomia ad ala fissa

Per aeromobili ad ala fissa elettrici a velocità costante, l'autonomia è:

$$t_\text{autonomia} = \frac{E_\text{disponibile}}{P_\text{elettrica}}$$ {#eq:endurance-definition-fw}

Sostituendo le espressioni per l'energia disponibile e la potenza di crociera:

$$t_\text{autonomia} = \frac{f_\text{batt} \times MTOW \times e_\text{spec} \times DoD \times \eta_\text{batt}}{W \times V / ((L/D) \times \eta_\text{crociera})}$$

Poiché $W = MTOW \times g_\text{Marte}$, i termini MTOW si cancellano:

$$t_\text{autonomia} = \frac{f_\text{batt} \times e_\text{spec} \times DoD \times \eta_\text{batt} \times (L/D) \times \eta_\text{crociera}}{g_\text{Marte} \times V}$$ {#eq:endurance-fixedwing}

Questa è l'equazione dell'autonomia per la configurazione ad ala fissa. Si noti che l'autonomia è indipendente dall'MTOW per frazioni di massa fisse—lo stesso risultato del velivolo a rotore (@eq:endurance-simple).

#### Calcolo dell'autonomia

Utilizzando i valori dei parametri da @sec:derived-requirements:

: Parametri per il calcolo dell'autonomia ad ala fissa {#tbl:fw-endurance-parameters}

| Parametro | Simbolo | Valore | Unità |
|:----------|:------:|------:|:-----|
| Frazione batteria | $f_\text{batt}$ | 0.3500 | - |
| Energia specifica | $e_\text{spec}$ | 270.0 | Wh/kg |
| Profondità di scarica | $DoD$ | 0.8000 | - |
| Efficienza batteria | $\eta_\text{batt}$ | 0.9500 | - |
| Rapporto portanza-resistenza | $(L/D)$ | 11.68 | - |
| Efficienza di crociera | $\eta_\text{crociera}$ | 0.4436 | - |
| Gravità marziana | $g_\text{Marte}$ | 3.711 | m/s² |
| Velocità di crociera | $V$ | 40.00 | m/s |

Convertendo l'energia specifica in J/kg: $e_\text{spec} = 270 \times 3600 = 972{,}000$ J/kg

Sostituendo in @eq:endurance-fixedwing:

$$t_\text{autonomia} = \frac{0.35 \times 972{,}000 \times 0.80 \times 0.95 \times 11.7 \times 0.444}{3.711 \times 40}$$

$$t_\text{autonomia} = \frac{1{,}076{,}267}{148.44} = 7{,}251 \text{ s} \approx 121 \text{ min}$$ {#eq:endurance-fw-result}

La configurazione ad ala fissa raggiunge circa 2 ore di autonomia, superando il requisito di 60 minuti del 101%.

#### Calcolo del raggio

Alla velocità di crociera di 40 m/s:

$$R = V \times t_\text{autonomia} = 40 \times 7{,}251 = 290{,}040 \text{ m} \approx 289 \text{ km}$$

Il raggio teorico di circa 289 km supera ampiamente il requisito di 100 km andata e ritorno per il raggio operativo di 50 km.

### Problema del decollo e atterraggio

La configurazione ad ala fissa dimostra eccellenti prestazioni di crociera. Tuttavia, non può soddisfare il requisito di missione per le operazioni VTOL. Questa sezione quantifica il vincolo di decollo che squalifica l'ala fissa pura dalla considerazione.

#### Analisi della corsa di decollo

La distanza di corsa di decollo per un decollo convenzionale è [@torenbeekSynthesisSubsonicAirplane1982]<!-- #appk --> [@sadraeyAircraftDesignSystems2013]<!-- #ch4:s3.4 -->:

$$S_\text{TO} = \frac{V_\text{TO}^2}{2 \bar{a}}$$ {#eq:takeoff-roll}

dove $V_\text{TO} \approx 1.1 \times V_\text{stallo}$ è la velocità di distacco e $\bar{a}$ è l'accelerazione media durante la corsa di decollo.

L'accelerazione media dipende dal bilanciamento delle forze:

$$\bar{a} = \frac{g}{W} \left[ T - D - \mu_r (W - L) \right]_\text{media}$$ {#eq:takeoff-accel}

dove $\mu_r$ è il coefficiente di attrito di rotolamento (tipicamente 0.02-0.05 su superfici dure).

#### Effetti specifici di Marte sul decollo

Su Marte, diversi fattori aumentano la distanza di decollo:

Riguardo all'effetto della bassa densità sulla velocità di stallo, la velocità di stallo scala inversamente con la radice quadrata della densità. Per l'UAV marziano con $W/S$ = 13.82 N/m² (al limite del vincolo di stallo), $C_{L,\text{max}}$ = 1.15, e $\rho$ = 0.0196 kg/m³:

$$V_\text{stallo} = \sqrt{\frac{2 \times 13.82}{0.0196 \times 1.15}} = \sqrt{1228} = 35.0 \text{ m/s}$$

$$V_\text{TO} = 1.1 \times 35.0 = 38.5 \text{ m/s}$$

Riguardo all'effetto della bassa densità sull'accelerazione, sia la spinta (dall'elica) che l'assistenza dell'attrito di rotolamento (dalla portanza durante la corsa) sono ridotti dalla bassa densità. La spinta disponibile da un'elica scala approssimativamente con la densità, e la portanza che alleggerisce il carico sulle ruote è anch'essa ridotta.

Per la stima della corsa di decollo, utilizzando la stima standard della corsa di decollo con spinta disponibile e condizioni marziane, assumendo un'accelerazione media di circa $a \approx 0.7$ m/s² (tenendo conto della spinta ridotta e della gravità):

$$S_\text{TO} = \frac{38.5^2}{2 \times 0.7000} = \frac{1482}{1.400} = 1059 \text{ m}$$ {#eq:takeoff-distance}

La corsa di decollo di circa 1060 m è impraticabile per le operazioni su Marte—nessuna pista preparata di questa lunghezza esiste o può ragionevolmente essere costruita vicino a un habitat.

Anche con il carico alare vincolato dal requisito di velocità di stallo (13.82 N/m² al punto di progetto), la lunghezza della pista richiesta è proibitiva. Il problema è che la bassa densità atmosferica richiede una distanza di corsa di decollo sostanziale indipendentemente dal dimensionamento dell'ala.

#### Metodi di lancio alternativi

Esistono diversi metodi di lancio alternativi per aeromobili ad ala fissa senza piste, ma nessuno è pratico per le operazioni marziane da un habitat: il lancio con catapulta o rotaia richiede un'infrastruttura di terra sostanziale, inclusi il meccanismo di lancio, le rotaie guida e i sistemi di accumulo di energia, nessuno dei quali è disponibile in un ambiente abitativo marziano; il decollo assistito da razzo (RATO) richiede booster a razzo solido che aggiungono massa significativa e sono monouso per volo, presentando un pericolo per la sicurezza vicino a un habitat con equipaggio; il lancio con sgancio da pallone richiede il trasporto dell'aeromobile in quota tramite pallone prima di rilasciarlo, ma non esiste un'infrastruttura di palloni su Marte; e il lancio aereo da un aeromobile portante non è applicabile perché non esiste un aeromobile portante su Marte. Tutti i metodi di lancio alternativi non soddisfano i requisiti operativi per operazioni ripetute e autonome da un habitat marziano senza un'infrastruttura complessa.

#### Problema dell'atterraggio

L'atterraggio convenzionale presenta sfide simili. La velocità di avvicinamento di circa $V_\text{avvicinamento} \approx 1.3 \times V_\text{stallo}$ = 45.5 m/s è alta. La decelerazione è limitata dalle basse forze di attrito, richiedendo centinaia o migliaia di metri di corsa di atterraggio. È richiesta una superficie preparata per evitare ostacoli e fornire una frenata costante. L'alta velocità di avvicinamento aumenta anche la sensibilità ai disturbi del vento. Il problema dell'atterraggio è potenzialmente più vincolante del decollo, poiché c'è meno margine di errore e nessuna opportunità per una riattaccata in emergenza senza capacità di hovering.

### Valutazione di fattibilità

#### Conformità ai requisiti

@tbl:fw-feasibility confronta la capacità dell'ala fissa con i requisiti di missione:

: Valutazione di fattibilità dell'ala fissa {#tbl:fw-feasibility}

| Requisito | Obiettivo | Capacità ala fissa | Stato |
|:------------|:-------|:----------------------|:------:|
| Autonomia di crociera | 60-90 min | 120.5 min | CONFORME |
| Raggio operativo | 50 km | 144.6 km | CONFORME |
| Capacità VTOL | Richiesta | Non possibile | NON CONFORME |
| Requisito di pista | Nessuno | 1060 m di corsa | NON CONFORME |

La configurazione ad ala fissa supera i requisiti di autonomia e raggio (margine di autonomia +101%), mostrando l'effetto della crociera ad alto L/D. Tuttavia, non soddisfa il requisito VTOL, che è non negoziabile per le operazioni marziane senza infrastruttura di pista.

### Conclusione sulla configurazione ad ala fissa

La configurazione ad ala fissa pura non può soddisfare il requisito VTOL per le operazioni dell'UAV marziano.

Nonostante raggiunga $(L/D)$ = 11.68 e dimostri autonomia teorica (120.5 min con riserva energetica del 20%) e raggio (289 km) che superano sostanzialmente i requisiti di missione, la configurazione ad ala fissa non può decollare o atterrare senza una pista preparata di circa 1060 m. Tale infrastruttura non esiste su Marte e non può essere ragionevolmente costruita per operazioni UAV ripetute da un habitat con equipaggio.

L'analisi dell'ala fissa dimostra tre punti chiave. Primo, l'efficienza aerodinamica non è il fattore limitante per l'autonomia dell'UAV marziano; piuttosto, il vincolo infrastrutturale (VTOL) domina la selezione della configurazione. Secondo, un L/D moderato è raggiungibile con un'attenta selezione del profilo alare ai bassi numeri di Reynolds caratteristici del volo marziano, sebbene i valori siano inferiori rispetto agli aeromobili terrestri a causa del difficile ambiente aerodinamico. Terzo, la crociera ad ala fissa dovrebbe essere sfruttata in qualsiasi configurazione fattibile per massimizzare il raggio e l'autonomia.

La valutazione di fattibilità per la configurazione ad ala fissa è riassunta in @tbl:fw-feasibility. Il confronto delle configurazioni e la motivazione della selezione sono presentate in @sec:architecture-selection.
