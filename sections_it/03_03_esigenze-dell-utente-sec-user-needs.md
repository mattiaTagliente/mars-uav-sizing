# Analisi della missione

## Esigenze dell'utente {#sec:user-needs}

Questa sezione identifica le esigenze degli stakeholder che guidano la progettazione dell'UAV marziano. Le esigenze dell'utente esprimono quali capacità sono richieste senza specificare valori numerici; i requisiti quantitativi derivati da queste esigenze sono documentati in @sec:derived-requirements. Le esigenze sono organizzate in tre categorie: le esigenze di capacità di missione definiscono gli obiettivi funzionali che l'UAV deve raggiungere, le esigenze di sicurezza operativa riguardano l'affidabilità e la robustezza durante le operazioni di volo, e le esigenze di compatibilità ambientale garantiscono che il sistema possa funzionare entro i vincoli fisici specifici di Marte.

@Tbl:user-needs-summary fornisce una vista consolidata di tutte le esigenze dell'utente organizzate per categoria.

: Riepilogo delle esigenze dell'utente {#tbl:user-needs-summary}

| ID  | Categoria                   | Esigenza                           |
|-----|-----------------------------|------------------------------------|
| N1  | Capacità di missione        | Raggio operativo esteso            |
| N2  | Capacità di missione        | Imaging aereo                      |
| N3  | Capacità di missione        | Ponte radio per comunicazioni      |
| N4  | Capacità di missione        | Decollo e atterraggio verticali    |
| N5  | Capacità di missione        | Autonomia estesa                   |
| N6  | Sicurezza operativa         | Tolleranza al guasto singolo       |
| N7  | Sicurezza operativa         | Tolleranza al vento                |
| N8  | Sicurezza operativa         | Protezione dall'ingresso di polvere|
| N9  | Compatibilità ambientale    | Propulsione elettrica              |
| N10 | Compatibilità ambientale    | Tolleranza alle radiazioni         |
| N11 | Compatibilità ambientale    | Compatibilità termica              |

### Esigenze di capacità di missione

Le esigenze di capacità di missione definiscono ciò che l'UAV deve realizzare per soddisfare i suoi obiettivi scientifici e operativi. Queste esigenze stabiliscono le funzionalità fondamentali richieste per le missioni di ricognizione, rilevamento e ponte radio per comunicazioni.

* N1. Raggio operativo esteso: l'UAV dovrà fornire capacità di rilevamento aereo oltre il raggio pratico dei rover di superficie. Gli attuali rover marziani hanno percorso meno di 50 km in missioni pluriennali, limitando l'area accessibile intorno ai siti di atterraggio. Una piattaforma aerea può rilevare aree più vaste in meno tempo, consentendo la ricognizione di siti che altrimenti richiederebbero anni di viaggio via rover o rimarrebbero inaccessibili.
* N2. Imaging aereo: l'UAV dovrà trasportare un sistema di telecamere capace di acquisire immagini per il rilevamento geologico. Questo supporta l'obiettivo primario di missione di mappatura del terreno, identificazione di siti scientificamente interessanti e fornitura di contesto per le operazioni di superficie.
* N3. Ponte radio per comunicazioni: l'UAV dovrà trasportare un sistema radio capace di estendere il raggio di comunicazione per le operazioni EVA (attività extraveicolare). Le comunicazioni radio di superficie sono limitate da vincoli di linea di vista e oscuramento del terreno; una stazione relay aerea può estendere il raggio operativo sicuro delle attività di superficie con equipaggio.
* N4. Decollo e atterraggio verticali: l'UAV dovrà essere capace di operare senza piste o strisce di atterraggio preparate. La superficie marziana non offre infrastrutture per operazioni aeronautiche convenzionali; tutti i decolli e atterraggi devono avvenire da terreno non preparato nei pressi dell'habitat.
* N5. Autonomia estesa: l'UAV dovrà fornire un tempo di volo sufficiente per completare una missione di andata e ritorno con tempo di rilevamento nella località obiettivo. Voli brevi, come quelli dimostrati da Ingenuity, sono insufficienti per le missioni di ricognizione e ponte radio previste. L'autonomia deve accomodare transito, operazioni di rilevamento e ritorno con margini appropriati.

### Esigenze di sicurezza operativa

Le esigenze di sicurezza operativa riguardano i requisiti di affidabilità e robustezza che garantiscono il successo della missione nonostante l'ambiente operativo ostile e l'impossibilità di intervento in volo.

* N6. Tolleranza al guasto singolo: l'UAV dovrà mantenere un'operazione sicura in seguito a qualsiasi guasto singolo di sistema. La riparazione in volo non è possibile e le opportunità di manutenzione sono limitate. Il progetto deve accomodare guasti dei componenti senza perdita catastrofica del velivolo.
* N7. Tolleranza al vento: l'UAV dovrà operare in sicurezza nelle tipiche condizioni di vento marziane. Marte sperimenta regolari picchi di vento pomeridiani che il velivolo deve sopportare senza perdita di controllo o danni strutturali.
* N8. Protezione dall'ingresso di polvere: l'UAV dovrà essere protetto dalla polvere marziana. La fine regolite (dimensioni delle particelle 1-100 μm) può degradare i cuscinetti meccanici, contaminare le superfici ottiche e ridurre l'efficacia della gestione termica. La protezione dalla polvere è necessaria per un funzionamento affidabile per tutta la durata della missione.

### Esigenze di compatibilità ambientale

Le esigenze di compatibilità ambientale derivano dai vincoli fisici fondamentali di Marte, inclusa la composizione atmosferica, l'ambiente di radiazione e le condizioni termiche. Queste esigenze non possono essere scambiate con le prestazioni; la non conformità comporta il guasto del sistema.

* N9. Propulsione elettrica: l'UAV dovrà utilizzare sistemi di propulsione elettrica. L'atmosfera marziana è priva di ossigeno per la combustione, precludendo i motori a combustione interna convenzionali. I sistemi a batteria elettrica o solari-elettrici sono le uniche opzioni pratiche.
* N10. Tolleranza alle radiazioni: l'elettronica e i materiali dell'UAV dovranno resistere all'ambiente di radiazione superficiale marziano. La combinazione di radiazione cosmica galattica e eventi di particelle solari crea un ambiente di radiazione che l'elettronica commerciale deve tollerare per la durata della missione.
* N11. Compatibilità termica: l'UAV dovrà operare nell'ambiente termico marziano. Le escursioni termiche diurne e le basse temperature ambientali (da -80°C a +20°C) impongono vincoli su materiali, meccanismi e in particolare sulle prestazioni delle batterie.
