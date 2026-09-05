# AGENT_BRIEF.md — QTS Dashboard

> Memoria persistente di progetto per sessioni Claude successive. Aggiornare
> il **log revisioni** in fondo al file dopo ogni sessione di modifiche,
> con numero sequenziale progressivo (continuare da `rev.1`, non riutilizzare
> numeri già assegnati anche in sessioni parallele).

## 1. Cos'è questo progetto

Dashboard web full-stack per il monitoraggio di un progetto di infrastruttura
in fibra ottica per Retelit S.p.A. — **fork/derivazione del progetto ENRI-RDS**,
riadattato per il progetto **QTS**. Stessa architettura, stesso funzionamento,
stesso brand kit; cambiano i dati sorgente (Excel/CSV di progettazione, file
QGIS/geojson, WBS `.mpp`) e i riferimenti testuali al nome progetto.

- Frontend: vanilla JS + HTML multipagina (nessun framework)
- Backend: FastAPI (Python), `backend/server.py`
- Database: MongoDB + GridFS (upload file)
- Hosting: GitHub Pages (frontend) + Render (backend API)
- Deploy: push automatico su GitHub

## 2. Struttura pagine

| File | Funzione |
|---|---|
| `hub.html` | Portale di navigazione, card con visibilità per ruolo |
| `index.html` | Dashboard principale: KPI, stepper permessi, donut, tabella pratiche |
| `scavi.html` | Avanzamento scavi/cantieri, mappa, log cantiere |
| `mappa.html` | Mappa Leaflet con layer GeoJSON (tratte, SED), filtro per lotto |
| `mappa_impresa_caricamento.html` | Mappa lato impresa esterna: caricamento pratiche, note registro |
| `imprese.html` | Area impresa (accesso credenziali esterne, filtrato per lotto assegnato) |
| `imprese_scavi.html` | Avanzamento scavi lato impresa |
| `gantt.html` | Gantt gerarchico (Lotto → Comune → Pratica → 5 fasi), da `.mpp` |
| `sopralluoghi.html` | Gestione verbali di sopralluogo, export DOCX/PDF |
| `polizze_convenzioni.html` | Tracking polizze e convenzioni, export Excel |
| `milestone.html` | Milestone di progetto |
| `ai_alerts.html` | Alert predittivi (modello proprietario) |
| `admin.html` | Pannello amministrazione: config API, token, note, audit |
| `pm/*.html` | Dashboard PM: panoramica portfolio/progetti, allocazione, integrazioni |
| `js/api-config.js` / `api-config.js` | Helper config API (`window.QTS`), riscrive i fetch verso l'API base configurata |
| `backend/server.py` | API FastAPI, endpoint REST, integrazione GitHub/GridFS |

## 3. Convenzioni tecniche

- **Namespace globale JS**: `window.QTS = { apiBase, isEnabled, ... }`, definito in `js/api-config.js`.
- **Storage locale**:
  - `localStorage['qts_api_base']` — base URL API custom (override)
  - `localStorage['qts_upload_token']` — token upload lato admin
  - `localStorage['_qts_session']` — token sessione (header `x-session-token`)
  - `localStorage['_qts_revalidate_fails']` — contatore fallimenti rivalidazione ruolo
- **Auth**: JWT via header `x-session-token`; endpoint protetti da `_require_staff_session` lato backend.
- **Dati centrali**: `Master.csv` (append-only) come sorgente di verità per pratiche/tratte.
- **Config backend**: `GITHUB_REPO=ENRI-RDS/QTS_DASHBOARD` (confermato,
  impostato via env var Render — il default nel codice resta il vecchio
  placeholder `QTS-RDS/dashboard`, non modificato in `server.py`), `MONGO_URL`,
  `DB_NAME=qts_dashboard`.

## 4. Brand kit (obbligatorio)

Applicare sempre il brand kit Retelit (`brandkitretelit.md`, se presente nel repo):
- Palette blu monocromatica — **niente colori caldi** (no arancione/giallo/rosso)
- Font Raleway
- Nessuna emoji, nessun gradiente decorativo
- Tono sobrio B2B infrastrutturale
- Border-radius componenti UI: 8–12px
- Numeri grandi con unità inline, formato italiano (punto come separatore migliaia)

Citare la sezione del brand kit pertinente quando informa una scelta di design.

## 5. Prossimi step (in ordine)

1. [x] **Deploy Render confermato "Live"** dopo fix `PYTHON_VERSION=3.11.10`
       (rev.5/rev.6) — verificato dai deploy logs (`Deploy live for 6158694:
       Update AGENT_BRIEF.md`).
2. [x] **Distribuire Code.gs come Web App** sul Google Sheet QTS — fatto,
       URL `/exec` ottenuto: `https://script.google.com/macros/s/
       AKfycby_5hYBzumFCVCqIkQ3Qq27Q6_xcoHPBzaK0K59b7uH69cFg1EdG3tIjlSPQl3wCfk0Mg/exec`.
       `Code.gs` scritto da zero (non preesisteva, foglio aveva solo
       `myFunction` vuota): legge sheet "Utenti" (colonne Nome/Codice/Ruolo),
       verifica `secret`+action `login`, ritorna `{ok, nome, ruolo}`.
3. [~] **Inserire su Render** `APPS_SCRIPT_URL` (vedi sopra) e
       `APPS_SCRIPT_SECRET` (stesso valore scritto dentro `Code.gs`,
       generato random, diverso da quello ENRI — NON annotato qui per
       motivi di sicurezza, repo pubblico) — in corso lato utente.
4. [x] **Testare login** da `hub.html` con un nome/codice presente nel
       foglio Utenti QTS — ok, login funzionante end-to-end (rev.9).
5. [x] **Aggiornare `DEFAULT_API_BASE`** in `js/api-config.js` e
       `api-config.js` (root, duplicati) — corretto: URL reale del Web
       Service Render è `https://qts-dashboard.onrender.com` (il
       placeholder precedente `qts-dashboard-api.onrender.com` non
       esisteva → causava `net::ERR_FAILED`/falso positivo CORS in
       console, il vero CORS su `enri-rds.github.io` era già corretto).
6. [x] **Aggiornare link GitHub Pages** in `hub.html` — l'unico link
       assoluto rotto era la card Milestone (puntava al placeholder
       `qts-rds.github.io/dashboard/milestone.html`); convertito in path
       relativo `milestone.html`, coerente con tutte le altre card che già
       usavano path relativi (rev.9).
7. [ ] **Caricare i file dati reali** del progetto QTS (Master.csv,
       QGIS.geojson, Riepilogo_progettazione.csv, SED_classificato.geojson)
       via pannello admin — verificare che le colonne combacino con quanto
       si aspetta il parser lato backend (§ struttura in `_regenerate_derived_files`).
8. [ ] **Gantt**: `.mpp` reale di QTS ancora da fornire — `GANTT_ROWS`/
       `GANTT_DEPS` in `gantt.html` sono ancora quelli ereditati da ENRI,
       vanno ricostruiti da zero una volta ricevuto il file.
9. [ ] Verificare se esiste un `brandkitretelit.md` dedicato o se va
       riportato dal progetto ENRI.
10. [x] Lotti/cluster: struttura lotti QTS è A/B/C (diversa da ENRI 1A/1B/2A/2B).
        Confermato e corretto in rev.17.

## 6. Log revisioni

- **rev.28** — `milestone.html`: rinomina colonne milestone contrattuali
  e fix di due bug segnalati da Andrea.
  - Header tabella "Milestone Imprese": `Invio P.1` → `Submission SED`,
    `Invio P.2` → `Submission Comuni`.
  - Header tabella "Contract Milestone", col-head gruppo: `Scavi` →
    `Attività Civili`.
  - **Bug pill senza sfondo per date 2029+**: `dateClass()` aveva un
    cutoff esplicito a `yr <= 2028` con fallback `dp-none` (nessuno
    sfondo/colore) per qualsiasi data successiva — riportato da Andrea
    su `02/01/2029`. Corretto rimuovendo il limite: `yr > 2027` ricade
    ora su `dp-2028` (navy), coerente con la logica a 3 fasce già usata
    da `colorForDate()` nel Gantt sottostante (mai stata affetta dallo
    stesso bug).
  - **Bug "Gantt Milestone — Imprese vs Contratto non si popola tutto"**:
    causa radice = `T1` (limite destro asse temporale) hardcoded ad
    Apr-2029, con bande anno e griglia trimestri come array statici
    fermi allo stesso anno. Qualsiasi riga con scadenza oltre quella
    soglia veniva clampata (`Math.min(1, ratio)` in `xPos()`) sul bordo
    destro, con barre accatastate/troncate invece che posizionate
    correttamente. Fix: `T1` ora calcolato dinamicamente come la data
    massima trovata in `GANTT_ROWS` (su tutti i campi data: avvio, p50,
    p90, p100, firma, ripensamento, invio, scavi50, completamento) + 1
    trimestre di padding, con minimo storico invariato ad Apr-2029 (se
    non c'è nessuna data oltre quella soglia il comportamento resta
    identico a prima). Bande anno e griglia trimestri/etichette non più
    hardcoded ma generate in loop da `T0` a `T1`, quindi si estendono
    automaticamente qualunque sia l'anno massimo nei dati (2029, 2030,
    ...) senza bisogno di ritoccare il codice ad ogni cambio di
    orizzonte temporale del progetto.
  - JS inline estratto e validato con `node --check` → OK.
- **rev.27** — `milestone.html`: ottimizzato layout delle due tabelle
  superiori (Milestone Imprese / Contract Milestone) per farle stare
  affiancate senza scroll orizzontale e con altezze uniformi. `.tables-row`
  passato da grid `3fr 2fr` (sbilanciato: a destra la tabella Contract con
  6 colonne aveva meno spazio della Imprese con 7, da cui lo scroll
  segnalato da Andrea) a `1fr 1fr` con `align-items:stretch` (prima
  `start`, causa dell'altezza diversa tra i due box); entrambi i
  `.section-block` figli ora `display:flex;flex-direction:column` e
  `.table-wrap{flex:1}` così le due card si allungano alla stessa altezza
  a prescindere da leggere differenze di contenuto. Colonna "Lotto"
  fissata a `width:44px` (prima non vincolata, veniva sovradimensionata
  dal layout automatico della tabella — causa della larghezza eccessiva
  segnalata). Ridotto padding celle header/body (`14px`→`8px` orizzontale)
  e dimensione/padding dei `.date-pill` per guadagnare spazio orizzontale.
  `node --check` OK (nessuna modifica JS in questa revisione, solo CSS).
- **rev.26** — `milestone.html`: rimosse le colonne "50%"/"90%" (gruppo
  "Attività Civili") dalla tabella "Milestone Imprese", su richiesta di
  Andrea, per dare più spazio orizzontale alla tabella "Contract
  Milestone" accanto (ora scrollabile con 5 colonne dati + Lotto).
  Restano "Avvio" e "100%"; colspan header "Attività Civili" 4→2. I campi
  `p50`/`p90` restano nel modello dati e nel Gantt sotto (marker a rombo
  intermedi sulle barre Imprese) — rimossi solo dalla tabella piatta, non
  dal backend/gantt. `node --check` OK.
- **rev.25** — `milestone.html`/`backend/server.py`: tabella "Contract
  Milestone" ristrutturata da elenco piatto (6 righe, 1 milestone per riga)
  a formato per-lotto (3 righe A/B/C, 1 colonna per milestone), simmetrica
  alla tabella "Milestone Imprese" accanto — su richiesta di Andrea, più
  leggibile a colpo d'occhio per lotto. Colonne: Firma | Fine Ripens. |
  Invio Permessi (gruppo "Contratto", stesse date per tutti i lotti — sono
  milestone contrattuali generali) | 50% Scavi | Completamento (gruppo
  "Scavi", specifiche per lotto). Le milestone 4-5 ("50% completamento
  scavi Lotto A e B" / "Completamento Lotto A e B") applicate a entrambi i
  lotti A e B con la stessa data; la 6 ("Completamento Lotto C") solo su C,
  che non ha una milestone 50% scavi propria nota → "-". Badge "6
  milestone" → "3 lotti" (coerente col badge della tabella Imprese).
  Gantt: righe Contract Milestone ora disegnano una barra firma→
  completamento per lotto con marker a rombo per le 3 tappe intermedie
  (stesso stile visivo delle righe Imprese), non più un singolo pallino
  numerato per milestone. `node --check`/sintassi Python OK.
- **rev.24** — `milestone.html`/`backend/server.py`: aggiornate le
  "Contract Milestone" con i dati contrattuali reali forniti da Andrea (6
  milestone, singola data ciascuna — non più il vecchio schema a step
  50%/70%/100% di completamento, mai popolato con dati reali: solo 2 righe
  fittizie "Permits submission"/"Authorizations received" ereditate dal
  fork). Nuova struttura tabella: N° | Milestone | Data (stile identico
  alla ex tabella "Milestone Progettazione" rimossa in rev.22). Gantt:
  righe `c` (Contract Milestone) ora disegnano un singolo pallino verde
  con numero d'ordine invece della linea tratteggiata + quadratini 50/70%
  + cerchio 100%. `MILESTONE_CONTRACT_ROWS` in `server.py` sostituito con
  le 6 milestone reali (`n`, `milestone`, `data`), badge "9 milestone" →
  "6 milestone" (era comunque disallineato dalle 2 righe reali prima
  presenti — bug preesistente, ora risolto insieme all'aggiornamento
  dati). `node --check`/sintassi Python OK.
- **rev.23** — `milestone.html`: rimossa colonna "Cluster" (tabella
  "Scadenze Lotti · Milestone Imprese", inutile per QTS: lotti A/B/C non
  hanno sotto-cluster come ENRI, era valorizzata a `-` da rev.22) e ogni
  riferimento — `<th>Cluster</th>`, `<td class="cluster-cell">`, `th.ch-base`
  vuoto in eccesso nella riga di raggruppamento, `sub:'cl.'+r.cluster` nel
  builder righe Gantt, sottotitolo pagina ("...per lotto e cluster"→"...per
  lotto"), commento residuo ENRI "padding per Cluster 6/7" sull'asse
  temporale del Gantt (già riferito a lotti/cluster inesistenti in QTS,
  aggiornato a descrizione generica). Backend: campo `cluster` rimosso da
  `MILESTONE_IMPRESE_ROWS` (3 righe A/B/C). `node --check`/sintassi Python
  OK.
- **rev.22** — `milestone.html`: eliminata la tabella statica "Milestone
  Progettazione" (4 righe: Progetto/Invio Permessi 1/Invio Permessi 2/
  Ottenimento, generiche per tutti i lotti). Le 4 date sono state spostate
  come nuove colonne nella tabella "Scadenze Lotti · Milestone Imprese"
  (gruppo "Permitting", ora 4 colonne — Progetto/Invio P.1/Invio P.2/
  Ottenimento — invece di 2 — Invio P./Ottenimento P.), stesse date per
  ogni lotto essendo milestone di progetto complessive, non per-lotto.
  **Bug pre-esistente corretto in questa occasione**: `MILESTONE_IMPRESE_ROWS`
  in `backend/server.py` conteneva ancora dati ENRI (lotti `1A/1B/2A/2B/1-8`,
  12 righe, stesso bug di rev.17 ma mai applicato a questo file/endpoint) —
  sostituiti con i 3 lotti reali QTS (`A/B/C`), badge "12 lotti"→"3 lotti".
  Colonne "Attività Civili" (avvio/50%/90%/100%) impostate a placeholder
  `-` per i 3 lotti: erano dati ENRI inventati, nessun dato reale QTS
  disponibile ancora (vedi §5.7-8) — di conseguenza le barre "Imprese" nel
  Gantt sotto non si disegnano più finché non arrivano dati reali (atteso:
  prima erano fasulle, ora assenti finché non caricati). `cluster` per i
  lotti A/B/C non ha un valore noto (QTS non ha sotto-cluster come ENRI) →
  impostato a `-`, da correggere se emerge un dato reale. `node --check`
  su JS inline e sintassi Python OK.
- **rev.21** — **Bug fix critico**: "Distribuzione Stati" (donut) in
  `index.html` non si renderizzava mai quando nessun lotto aveva ancora
  superato lo stato IN ATTESA/IN REDAZIONE (caso reale QTS: tutti i lotti
  A/B/C al 100% "in attesa"). Causa: in `renderDashboard()`, quando
  `activeLotti` (lotti con avanzamento) è vuoto, la riga per la tabella
  "Dettaglio lotti attivi" faceva `return;` — uscendo dalla funzione
  **prima** della chiamata a `renderDonut(globalStati, grandTotal)` e
  `renderFlussoMese()` in fondo, che quindi non venivano mai eseguite.
  Bug preesistente, identico anche in `ENRI-RDS/index.html` (verificato
  via file caricato dall'utente) — lì non si manifesta solo perché c'è
  sempre almeno un lotto avanzato. Fix: il `return` anticipato è stato
  sostituito con un `if/else` che mostra il messaggio "Nessun lotto
  avanzato" ma lascia proseguire l'esecuzione fino a `renderDonut`/
  `renderFlussoMese`. `node --check` OK.
  **Nota per ENRI**: stesso bug latente presente anche lì
  (`renderDashboard()`, stessa riga `if(!activeLotti.length){...return;}`)
  — da applicare lo stesso fix se/quando capiterà lo stesso scenario dati
  (tutti i lotti fermi a IN ATTESA/IN REDAZIONE).
- **rev.20** — `index.html`: eliminata completamente la funzione/dicitura
  "Lotti Attivi" / "Lotti in Progettazione" — era residuo del vecchio
  schema lotti ENRI (`ORDER_ATTIVI=['1A','1B','2A','2B']`,
  `ORDER_FUTURI=['1'..'8','P']`), mai adattato allo schema QTS (A/B/C),
  per cui non scattava mai (nessun lotto QTS corrisponde a quei codici) —
  ma lasciava comunque codice morto e un ordinamento lotti inefficace.
  Rimosso in due punti:
  - `renderDashboard()`: tolti `ORDER_ATTIVI`/`ORDER_FUTURI`/`ORDER`,
    `lottiAttivi`/`lottiFuturi`/`totAttivi`/`totFuturi`, i separatori
    "⚡ Lotti Attivi"/"Lotti in Progettazione" e le righe riepilogative
    "Totale attivi"/"Totale progettazione" (con relativi `gruppiAttivi`/
    `gruppiFuturi` e handler). Ordinamento lotti ora semplice
    `a.localeCompare(b)`.
  - `apriEditManuale()` (modale dati manuali): stessa coppia
    `ORDER_ATTIVI`/`ORDER_FUTURI` locale, stesso separatore "Lotti in
    Progettazione" e badge ⚡ per `isAttivo`, rimossi allo stesso modo;
    ordinamento lotti anch'esso `localeCompare`.
  Verificato: nessuna occorrenza residua di `ORDER_ATTIVI`/`ORDER_FUTURI`/
  `lottiAttivi`/`lottiFuturi`/`isAttivo` nel file. JS inline estratto e
  validato con `node --check` → OK.
- **rev.19** — Rimosso il tasto/funzione "Siti QTS" da `mappa.html` e
  `mappa_impresa_caricamento.html`: array `SITI`, controllo `SitiControl`,
  pannello (`sitiPanel`/`sitiBtn`), ricerca (`filterSiti`), marker
  (`goToSito`/`_sitoMarker`) — tutto rimosso, nessuna dipendenza esterna
  residua (verificato via grep). In `mappa.html` il tasto "Pratiche" ha
  preso il posto del tasto Siti come primo controllo Leaflet in topright
  (tolto `margin-top:6px` e il commento "sotto Siti"). In
  `mappa_impresa_caricamento.html` non esisteva un tasto "Pratiche"
  equivalente da spostare: lì "Pratiche" è già una tab della sidebar
  (`sbtab-pratiche`), non un controllo mappa flottante — nessuna azione
  necessaria oltre alla rimozione. `node --check` OK su entrambi i file.
- **rev.18** — Colori legenda ufficiali, fix lotti su
  `mappa_impresa_caricamento.html`, rimozione voce "Tracciato QTS" e
  pulizia codice morto in `mappa.html`.
  - Colori lotto allineati alla specifica ufficiale di progetto (Path A
    giallo, Path B viola, Path C blu): `LOTTO_COLORS` reso esplicito
    (`{A:'#E8C61A', B:'#7A3DAA', C:'#2D6CDF'}`) sia in `mappa.html` sia in
    `mappa_impresa_caricamento.html` (non più solo dinamico via palette).
  - `mappa_impresa_caricamento.html`: stesso bug di `LOTTO_ORDER`/
    `LOTTI_ATTIVI`/`LOTTI_AVVIO` hardcoded ENRI già risolto in `mappa.html`
    in rev.17, qui non ancora sistemato — ora corretto con lo stesso
    approccio (`lottoOrder()` dinamico su `lottoStats`, gruppo filtro
    unico, sidebar/ordinamento senza più liste 1-8/1A-2B fisse).
  - `mappa.html`: rimossa la voce di legenda "Tracciato QTS" (colore
    viola #1A7D99) e l'intera sezione della guida "?" che la descriveva
    — corrispondeva a un toggle/pulsante "Solo QTS" mai realmente
    implementato nel codice, puro residuo testuale ereditato da ENRI.
  - `mappa.html`: pulizia codice morto (3088→3037 righe). JS: rimossa
    `applyFilter()` (mai chiamata, commento "mantenuto per compatibilità"
    non corrispondeva al vero). CSS: rimosse classi definite ma mai
    applicate nel markup/JS — `.btn-mobile-hidden`, `.lav-no`,
    `.legend-dot` (la legenda SED usa stili inline), `.popup-stato-bar`
    (+variante mobile), `.search-highlight`, `.btn.secondary` (+hover),
    `.sidebar-close-btn` (+variante mobile), `.topbar-left`, `.logo`
    (+variante mobile), `.btn-back` (+hover+variante mobile — il
    selettore `a.btn-back[href="index.html?direct=1"]` non veniva mai
    matchato: il link reale in pagina usa `class="topbar-back"`),
    `.popup-tag` e varianti `.ok`/`.warn`/`.err`.
  - Verificato con scansione statica su tutto il file (regex classi CSS
    vs markup, funzioni JS vs chiamate) + `node --check` sul JS inline
    estratto → OK. Nota non risolta: `id="drawerToggleBtn"` non è
    referenziato da alcun JS/CSS (il bottone usa `onclick` inline) — id
    verosimilmente superfluo ma innocuo, lasciato per prudenza.

- **rev.17** — Fix bug lotti QTS ereditati da ENRI (residuo del fork, mai
  riadattati ai dati reali). Confermato: lotti QTS sono **A/B/C** (da
  `LOTTO` in `QTS.geojson`, da "Lotto A.xlsx" ecc. in `Master.csv`),
  diversi dai lotti ENRI (1-8, 1A/1B/2A/2B).
  - `mappa.html`: `LOTTO_COLORS`/`LOTTO_ORDER`/`LOTTI_ATTIVI`/`LOTTI_AVVIO`
    erano hardcoded sui lotti ENRI → causavano tratte grigie (fallback
    colore) in modalità "Lotto" e legenda/filtri con lotti inesistenti
    per QTS. Fix: colori e ordine lotto ora **dinamici**, calcolati sui
    dati effettivamente caricati (`assignLottoColors()` + `lottoOrder()`
    su `lottoStats`, palette `LOTTO_PALETTE` a 12 colori assegnati in
    ordine alfabetico/numerico ai lotti presenti). Rimossa la vecchia
    distinzione "lotti attivi vs lotti in avvio" (concetto ENRI non
    applicabile a QTS, ora un solo elenco filtri). Testo guida "?"
    aggiornato di conseguenza (non cita più 1A/1B/2A/2B/1-8).
  - `IMPRESE_PER_LOTTO` (`index.html`, `scavi.html`) e `IMPRESE`
    (`mappa_impresa_caricamento.html`, `polizze_convenzioni.html`):
    contenevano tutte la stessa mappa impresa-per-lotto di ENRI
    (Valtellina/Soleto/Sielte/Telebit/Sertori/Circet sui lotti 1-8/
    1A-2B). Aggiornate su indicazione di Andrea a
    `{A:'Telebit', B:'Telebit', C:'Telebit'}` — Telebit gestisce la
    progettazione di tutti e 3 i lotti QTS.
  - `mappa.html`: JS inline validato con `node --check` dopo le modifiche
    → OK.
  - **TODO aperto, non ancora corretto**: `COMUNI_PER_LOTTO` in
    `index.html` (~riga 2782) ha ancora comuni/lotti ENRI (1,1A,1B,2...8),
    usato come fallback quando `QTS.geojson` non copre un lotto (righe
    ~2865, 3099, 3200, 3222). Nessuna voce per A/B/C. Dati reali dei
    comuni per lotto sono già ricavabili da `QTS.geojson` (es. lotto A →
    Vimercate, Concorezzo, Monza...); da sistemare su richiesta.

- **rev.1** — Setup iniziale repo QTS: rename automatico ENRI→QTS su tutti i
  file (`gantt.html`, `scavi.html`, `mappa_impresa_caricamento.html`,
  `index.html`, `sopralluoghi.html`, `polizze_convenzioni.html`, `mappa.html`,
  `hub.html`, `imprese_scavi.html`, `imprese.html`, `js/api-config.js`,

  `api-config.js`, `milestone.html`, `ai_alerts.html`, `admin.html`,
  `backend/server.py`), via regex `ENRI(?!CH)`/`enri(?!ch)` per preservare
  `enrich`/`enriched`. Verificata coerenza chiavi localStorage/sessione
  (nessuna incoerenza rilevata, tutto già allineato su `_qts_session` /
  `qts_api_base` / `qts_upload_token`). Creato questo file AGENT_BRIEF.md.
- **rev.2** — Confermato repo GitHub reale (`ENRI-RDS/QTS_DASHBOARD`).
  Creato Apps Script/Google Sheet di login dedicato QTS, separato da ENRI
  (nessuna condivisione utenze). Deciso: backend Render separato da ENRI,
  workspace Render dedicato "QTS" (motivo: necessità di permessi granulari
  per membri futuri, non ottenibile con workspace condiviso).
- **rev.3** — Web Service Render "QTS_DASHBOARD" creato (workspace "QTS",
  repo `ENRI-RDS/QTS_DASHBOARD`, root `backend`, start command
  `uvicorn server:app --host 0.0.0.0 --port $PORT`, instance Free). Env var
  inserite: `DB_NAME=qts_dashboard`, `GITHUB_REPO=ENRI-RDS/QTS_DASHBOARD`,
  `GITHUB_BRANCH=main`, `ALLOWED_ORIGINS` (GitHub Pages `enri-rds.github.io`
  + localhost dev), `SESSION_SECRET` (generato random), `GITHUB_TOKEN`
  (fine-grained, resource owner org ENRI, permesso Contents R/W su
  QTS_DASHBOARD).
- **rev.4** — Creato cluster Atlas M0 free dedicato QTS (project Atlas
  separato da ENRI, cluster `qts-cluster`, utente DB `qts_admin`, network
  access 0.0.0.0/0). `MONGO_URL` inserito su Render.
- **rev.5** — Fix build Render fallito: `pydantic-core` non compilava su
  Python 3.14 (default Render, nessuna wheel precompilata per quella
  versione). Aggiunta env var `PYTHON_VERSION=3.11.10` su Render (creato
  anche `backend/runtime.txt` con `python-3.11.10` come alternativa
  equivalente, da caricare su GitHub se si preferisce documentarlo nel repo
  invece che solo in env var). TODO aperti: vedi §5 (prossimi step in
  ordine).
- **rev.6** — Confermato deploy Render "Live" (deploy logs, screenshot
  utente). Confermato via ispezione `backend/server.py`: la separazione
  utenze QTS/ENRI è già architetturalmente in place — login passa da
  `/api/auth/login` → proxy server-to-server verso `APPS_SCRIPT_URL`/
  `APPS_SCRIPT_SECRET` (env var Render, workspace QTS separato da ENRI),
  nessun codice condiviso tra i due backend. Resta da completare
  operativamente: distribuzione Code.gs come Web App sul foglio QTS,
  inserimento env var su Render, test login end-to-end (§5 punti 2-4).
- **rev.7** — Foglio Utenti QTS confermato con stesse 3 colonne di ENRI
  (Nome/Codice/Ruolo), ma script Apps Script associato era vuoto
  (`myFunction` stub). Scritto `Code.gs` da zero (doPost, verifica
  `secret`+`action:"login"`, match nome+codice case-insensitive su
  colonna Nome/Codice, ritorna `{ok, nome, ruolo}` da colonna Ruolo).
  Distribuito come Web App, URL `/exec` ottenuto (vedi §5.2). Secret
  generato random per QTS, diverso da quello ENRI. Prossimo: inserire
  `APPS_SCRIPT_URL`/`APPS_SCRIPT_SECRET` su Render e testare login.
- **rev.8** — Login falliva con "Errore di connessione" / CORS in console.
  Diagnosi: `ALLOWED_ORIGINS` su Render era già corretto
  (`https://enri-rds.github.io,...`, confermato nei log d'avvio), il vero
  bug era `DEFAULT_API_BASE` in `js/api-config.js` + `api-config.js`
  (root) puntato a `qts-dashboard-api.onrender.com`, host mai esistito —
  l'URL reale del Web Service è `https://qts-dashboard.onrender.com`
  (confermato dai log Render: "Available at your primary URL"). Corretto
  in entrambi i file. **Da verificare**: bug noto non richiesto, segnalato
  qui — nei log d'avvio compare `[sync_cantieri] errore lettura master:
  404: Master.csv not found`, coerente con §5.7 (dati reali ancora da
  caricare), non bloccante per il test di login.
- **rev.9** — Login end-to-end funzionante. Causa ultimo blocco (401
  "Foglio Utenti non trovato"): il tab del Google Sheet QTS si chiamava
  `Foglio1` invece di `Utenti` (Code.gs cerca esplicitamente lo sheet
  `Utenti`). Risolto rinominando il tab su Google Sheets, nessuna modifica
  a `Code.gs`/backend necessaria. §5 punto 4 completato.
- **rev.10** — Eliminato `Riepilogo_progettazione.csv` (ridondante:
  derivato 1:1 da QGIS.geojson, come già documentato in rev.7 dello schema
  colonne). File sorgente ridotti a 3: `Master.csv`, `QTS.geojson`
  (rinominato da `QGIS.geojson` — geometria/attributi tratte, keyed by
  TRATTA_ID), `SED_QTS.geojson` (rinominato da `SED_classificato.geojson`).
  Rimosso anche il vecchio layer overlay "Tracciato QTS" in
  `mappa.html`/`mappa_impresa_caricamento.html` (rete di terze parti
  mostrata in ENRI, nome ormai in collisione col progetto stesso — su
  richiesta utente, eliminato interamente: funzioni `loadQTS`,
  `toggleQTS`, `setQTSOnly`, variabili `qtsLayer`/`qtsOutlineLayer`,
  markup toggle in sidebar, CSS `.qts-toggle-row` e affini).
  Backend: `_regenerate_derived_files` ora rigenera solo `QTS.geojson`
  (patch in place delle proprietà di stato calcolate da Master.csv);
  `_sync_cantieri` legge PROVINCIA/COMUNE direttamente da `QTS.geojson`
  invece che da Riepilogo. `scavi.html` (`_loadPermessi`) riscritta per
  leggere `QTS.geojson` (GeoJSON) invece del CSV Riepilogo.
  **Nota aperta**: `QTS.geojson` non ha un campo `CLUSTER` (presente nel
  vecchio QGIS.geojson/Riepilogo ereditato da ENRI) — l'aggregazione per
  cluster in `scavi.html` degrada automaticamente a vuota (nessun errore,
  ma il grafico cluster non mostra dati finché non si introduce un campo
  equivalente nei dati QTS). `index.html` riscritto: `fetchRiepilogoCSV`
  → `fetchQtsGeojson` (fetch+cache di `QTS.geojson`, JSON invece di CSV);
  `loadData()` e `loadCluster()` aggregano LOTTO×STATO/PROVINCIA/COMUNE
  direttamente dalle properties delle feature. Il pannello "Avanzamento
  per Cluster" mostra ora un messaggio informativo ("dato non disponibile
  nei dati QTS") invece del grafico — **occhio**: `prevRilascioCol`
  (Prev. Rilascio, dati Master.csv, indipendente) è annidato nello stesso
  `clusterSection` e resta visibile, verificato non nasconderlo per
  errore. `_emAggiornaClusters()` (usata solo dal flusso "modifica
  manuale"/ripristina CSV) resta invariata: deriva pseudo-cluster da un
  `CLUSTER_MAP` statico lotto→cluster (1A/1B→1, 2A/2B→2, ecc.), non da un
  campo CLUSTER reale — soluzione disponibile ma NON adottata come fonte
  primaria del grafico principale (approssimazione lotto-based, non
  geografica come il vecchio CLUSTER ENRI: deciderlo esplicitamente se
  serve riattivare il grafico).
  Rinominati anche i riferimenti `SED_classificato.geojson` →
  `SED_QTS.geojson` in `index.html`/`scavi.html`/`mappa*.html`.
  Verificato con `py_compile` (backend) e HTML parser + `node --check`
  (tutti i file frontend toccati): nessun errore.
  **Prossimo step**: caricare via pannello admin i 3 file reali
  (`Master.csv`, `QTS.geojson`, `SED_QTS.geojson`) e testare end-to-end.
- **rev.11** — Eliminato il grafico "Avanzamento per Cluster" da
  `index.html` (nessuna fonte dati, come da rev.10) e da `scavi.html`
  (pannello "Permessi per cluster"). **Incidente rilevato e corretto**:
  la rimozione a blocco di `loadCluster()`→`openModalCluster()` in
  `index.html` aveva accidentalmente cancellato anche `fmt()`,
  `parseNum()`, `setLoading()`, `openModal()` (modale dettaglio Lotto),
  `closeModal()`, il gestore Escape globale e `window._modalOpen`/
  `window._modalClose` (focus-trap, usati da TUTTE le modali: Lotto,
  Gruppo, Kpi, Help) — codice non correlato che si trovava fisicamente
  tra le funzioni cluster nel file. Rilevato confrontando l'elenco
  funzioni prima/dopo con lo zip originale caricato dall'utente
  (`/mnt/user-data/uploads/...QTS_DASHBOARD-main__1_.zip`, riestratto in
  `/home/claude/qts_orig/` come riferimento pulito), poi recuperato
  chirurgicamente dall'originale e reinserito. Verificato con diff
  sistematico funzioni/`window.X=`/costanti top-level su TUTTI i file
  toccati in questa sessione (`index.html`, `scavi.html`, `mappa.html`,
  `mappa_impresa_caricamento.html`, `admin.html`, `backend/server.py`):
  uniche assenze residue sono quelle intenzionali (cluster/Riepilogo/
  layer QTS overlay), nessun'altra vittima collaterale. `py_compile`,
  HTML parser e `node --check` tutti OK.
  **Lezione operativa**: quando si rimuove codice per nome/funzione in
  un file HTML/JS di migliaia di righe, non affidarsi a range di righe
  ricavati da un singolo grep — codice non correlato può trovarsi
  frammisto. Preferire `str_replace` con blocco delimitato per intero
  (funzione per funzione) o verificare sempre con un diff funzioni
  prima/dopo (`grep -oP '^(async )?function \w+'`) contro l'originale
  prima di considerare una rimozione conclusa.
  Nel pannello "Avanzamento per Cluster" resta solo il pannello
  "Prev. Rilascio" (Master.csv, indipendente), ora estratto in una card
  a sé stante (`#prevRilascioSection`) con layout responsive via
  `flex-wrap` invece della vecchia logica JS `adjustClusterMobile()`
  (rimossa, non più necessaria).
- **rev.12** — Eliminato anche il pannello "Avanzamento per Cluster" da
  `scavi.html` (card + `_renderClusters()`, `openModalCluster()`/
  `closeModalCluster()`, modale `modalClusterOverlay`, `CLUSTER_PERMESSI`,
  `CLUSTER_COLOR`, `window._CLUSTER_SCAVI`/`clusterScaviMap`). **Stesso
  incidente della rev.11, rilevato subito con lo stesso metodo diff**:
  la rimozione a blocco `_renderClusters()`→`closeModalCluster()` aveva
  inglobato 4 funzioni non correlate interposte nel mezzo — `_renderBars()`
  (barre di avanzamento per lotto), `_renderRadar()` (radar chart),
  `openModalLotto()`/`closeModalLotto()` (modale dettaglio lotto, con
  relativo gestore Escape). Recuperate dall'originale e reinserite (con
  fix: il gestore Escape recuperato chiamava ancora `closeModalCluster()`,
  rimossa la chiamata). Verificato con lo stesso diff sistematico
  funzioni/`window.X=`/costanti prima/dopo: nessuna assenza inattesa.
  Lasciati intenzionalmente INTATTI: la colonna/tag "Cluster" per-lotto
  nella tabella cantieri principale, i quick-filter, il breakdown imprese
  per cluster, il campo `r.cluster`/`LOTTI[].cl` — è una feature diversa
  (tag per-lotto, non un'aggregazione dedicata) che il richiedente non ha
  chiesto di rimuovere; resta funzionante ma mostrerà sempre "?" finché
  QTS.geojson non avrà un campo CLUSTER (nota già presente, invariata).
  `py_compile` n/a (nessun file Python toccato), HTML parser + `node
  --check` OK su `scavi.html`.
  **Lezione operativa aggiornata**: la tecnica del diff funzioni/window/
  const prima-vs-originale (non solo grep sul range da cancellare) è
  ora il controllo standard dopo ogni rimozione a blocco in questi file.
- **rev.13 (in corso)** — Nuova richiesta: rimozione COMPLETA del concetto
  "cluster" (non solo i pannelli dedicati già tolti in rev.11/12, ma
  anche il campo dati, colonne tabella e filtri residui) da tutti i file
  che lo referenziano: `backend/server.py`, `mappa.html`,
  `mappa_impresa_caricamento.html`, `index.html`, `imprese_scavi.html`,
  `ai_alerts.html`, `scavi.html`, `hub.html`, `gantt.html`,
  `milestone.html`. Un file alla volta, `str_replace` mirato.
  **`backend/server.py` — FATTO**: rimosso `cluster` da `CANTIERI_COLS`,
  `_sync_cantieri()` (var locale, dict `geo_by_tratta`, `groups[key]`,
  update/insert cantiere), endpoint `GET /api/cantieri` (parametro query
  + filtro Mongo), `MILESTONE_IMPRESE_ROWS` (campo per-lotto). Lasciate
  INVARIATE le 7 label `"Cluster 1"`..`"Cluster 7"` in
  `MILESTONE_CONTRACT_ROWS` (milestone contrattuali, non tag cluster) —
  su richiesta esplicita di Andrea, che invierà i dati corretti in
  seguito. `py_compile` OK. NB: `cantieri.csv` su GitHub ha ancora la
  colonna `cluster` nell'header finché non viene rigenerato da un push
  successivo (`_push_cantieri_to_github()` userà il nuovo `CANTIERI_COLS`
  al prossimo giro).
  **Aggiornamento**: chiarito che "cluster" non esisterà nel dominio QTS
  (a differenza del vecchio ENRI). Eliminate anche le 7 righe
  `"Cluster 1"`..`"Cluster 7"` da `MILESTONE_CONTRACT_ROWS` (non più
  rinominate/lasciate in sospeso — cancellate). Restano solo
  `"Permits submission"` e `"Authorizations received"`. `backend/server.py`
  ora a **zero occorrenze** di "cluster" (verificato via grep). `py_compile` OK.
  Prossimo file: `milestone.html`.
- **rev.14** — Chiarito con Andrea: "cluster" non esisterà nel dominio QTS
  (concetto ereditato da ENRI, mai avuto senso in QTS.geojson). Eliminate
  anche le 7 righe `"Cluster 1"`..`"Cluster 7"` da `MILESTONE_CONTRACT_ROWS`
  in `server.py` (non più in sospeso — cancellate, non rinominate). Restano
  solo `"Permits submission"` e `"Authorizations received"`. `milestone.html`
  ESCLUSO su richiesta esplicita di Andrea — non toccarlo.
  **`index.html` — FATTO** (23→0 occorrenze):
  - CSS morta `#clusterBodyFlex` (nessun elemento con quell'id nell'HTML,
    residuo del vecchio pannello "Avanzamento per Cluster" già rimosso in
    rev.11) rimossa dalla media query mobile.
  - Colonna "Cluster" rimossa dalla tabella SED: sort key, array `sedCols`,
    cella `<td>` nel render riga, header `<th>`.
  - Export Excel SED (`buildSedExcelRows`/`writeSedExcel`): rimossa colonna
    Cluster da righe, header e `!cols` widths.
  - `CLUSTER_MAP`/campo `cluster` rimossi dal parsing SED da QTS.geojson
    (oggetto `p` → `{fid, tratta, name, tipo, lotto, comune, ...}`).
  - Help modal: sezione "Avanzamento per Cluster" (descriveva un pannello
    già rimosso in rev.11) sostituita con sezione "Prev. Rilascio" che
    descrive il pannello realmente presente. Corretta anche la voce
    "Storico" che citava un filtro per cluster mai esistito nel codice.
  - 6 commenti con riferimenti fantasma a `loadCluster()` (funzione mai
    definita in questo file, solo citata in commenti) e a modali/export
    "Cluster" inesistenti: ripuliti senza toccare logica.
  - Verificato: `grep -ic cluster index.html` → 0. JS inline estratto e
    validato con `node --check` → OK. Div count 410/411 invariato
    rispetto all'originale (pre-esistente, non introdotto da queste modifiche).
  Prossimo file: da concordare con Andrea (restano `mappa.html`,
  `mappa_impresa_caricamento.html`, `imprese_scavi.html`, `ai_alerts.html`,
  `scavi.html`, `hub.html`, `gantt.html`).
- **rev.16** — `mappa.html` — FATTO (54→0 occorrenze). Qui "cluster" era
  una vera e propria **modalità di visualizzazione** a sé stante (non solo
  un tag come nell'export SED di `index.html`), con:
  - Bottone `vbtn-cluster` nella barra "Visualizzazione" (rimosso, restano
    solo Pratiche/Scavi/Lotto).
  - `_CLUSTER_PALETTE` (30 colori) + `getClusterColor()` (rimossi).
  - Ramo `mode === 'cluster'` in `getColorForMode()` (rimosso).
  - `setViewMode()`: `selectedClusters.clear()`, `'cluster'` nell'array
    modalità, ramo `renderFilterCluster()` (tutti rimossi — ora chiama
    sempre `renderFilterLotto()`).
  - Intero blocco filtro cluster eliminato: `selectedClusters` (Set),
    `renderFilterCluster()`, `toggleCluster()`, `applyFilterClusterMulti()`,
    `applyFilterCluster()` (~90 righe).
  - Ramo `else` (cluster) in `updateLegend()` rimosso — restano
    stato/scavi/lotto.
  - `props.CLUSTER` rimosso da `_prepareExportProps()` (export GeoJSON).
  - Campo "Cluster" rimosso dal popup di dettaglio tratta.
  - 3 paragrafi della guida "?" aggiornati (menzionavano Cluster come
    quarta modalità/filtro/campo popup).
  Verificato: nessuna chiamata orfana a funzioni rimosse
  (`applyFilterCluster`, `renderFilterCluster`, `toggleCluster`,
  `getClusterColor`, `selectedClusters`, `vbtn-cluster`, `cbtn-*`) — grep
  a zero risultati. JS inline estratto e validato con `node --check` → OK.
  Prossimo file: da concordare con Andrea (restano
  `mappa_impresa_caricamento.html`, `imprese_scavi.html`, `ai_alerts.html`,
  `scavi.html`, `hub.html`, `gantt.html`).
- **rev.15** — `admin.html`: rimossa l'opzione `dati.csv (in disuso)` dal
  `<select id="target">` del form upload (tab "File correnti"). File già
  escluso lato backend da `_EXCLUDE_FILES = {"dati.csv"}` in `server.py`
  (non più esposto nella lista admin), ma restava selezionabile come target
  di upload nel form — rimosso solo l'`<option>` orfano, nessun altro
  riferimento a `dati.csv` nel file. Non collegato alla rimozione "cluster"
  (task separato su richiesta di Andrea). JS inline validato con
  `node --check` → OK.
- **rev.22** — `index.html`: spostata la sezione "Attraversamenti SED"
  (tabella completa + KPI Ferroviario/Autostradale/Idrico/Inviati/Ottenuti +
  filtri) da sezione full-width separata (sotto `grid-main`, prima di
  "Tutte le Pratiche") a blocco embedded (`#sedEmbedded`) dentro la card
  "Avanzamento per Lotto" (colonna main di `grid-main`), subito dopo
  `#flussoMeseBar`. Motivo: quello spazio restava vuoto perché `.card`
  main-column viene stretchata da CSS grid (`align-items` default
  `stretch`) all'altezza della colonna `.side` (donut + SED quick card),
  più alta — residuo dell'area che occupavano le barre cluster ora rimosse.
  Font/padding ridotti (~20-30%) via nuove regole CSS `#sedEmbedded ...`
  per adattarsi allo spazio più stretto. Nessun id rinominato (`sedBadge`,
  `sedKpiRow`, `sedKpiFerr/Auto/Idrico`, `sedBarInv*/Ott*`, `sedKpiInv/Ott`,
  `sedProgressFill`, `sedBody`, `sedQ`, `sedF*`, tabella/`sedTbody`,
  `sedFootL`, `sedCollapseBtn`, dropdown Excel) — tutte le funzioni JS
  (`renderSed`, `sedSort`, `sedResetFilters`, `sedToggleCollapse`,
  `toggleSedXlsDropdown`, `exportSedXlsx*`) accedono solo via
  `getElementById`, nessuna dipendenza dalla gerarchia DOM rimossa.
  Vecchio blocco `#sedSection` full-width eliminato per intero (era
  duplicato). Verificato: 0 id duplicati nel file, `node --check` su JS
  inline estratto → OK.
  **Nota**: la card "SED — Permessi" nella sidebar (`#sedQuickCard`,
  dentro `.side`) resta invariata e ora è ridondante con la vista
  compatta embedded — da valutare se rimuoverla in una prossima sessione.
- **rev.23** — `index.html`: rimossa la card "SED — Permessi" dalla
  sidebar (`#sedQuickCard`, dentro `.side`), ridondante dopo rev.22
  (stessi dati già mostrati in `#sedEmbedded` sotto le barre lotto).
  Rimosso solo il markup (`sqBadge`, `sqInvPct`, `sqBarInv`, `sqOttPct`,
  `sqBarOtt`, `sqRows`, `sqLottoRows`); le funzioni JS che li popolano
  (righe ~1784-1838, dentro `loadSED()`) restano invariate — sono già
  `if(el)`-guarded su ogni `getElementById`, quindi diventano no-op
  silenziosi senza il markup, nessun errore console. Non ripulite per
  ridurre rischio in questa sessione; da rimuovere in un secondo momento
  se si vuole eliminare anche il codice morto. Verificato: 0 id duplicati,
  `node --check` su JS inline → OK.
- **rev.24** — `index.html`: rimosso il codice morto residuo di rev.23.
  Eliminata l'intera funzione `updateQuickCard()` (~75 righe, popolava
  `sqBadge/sqInvPct/sqBarInv/sqOttPct/sqBarOtt/sqRows/sqLottoRows`, tutti
  id ormai inesistenti dopo la rimozione di `#sedQuickCard`) e il
  monkey-patch `window.renderSed = function(keepPage){ _origRenderSed(keepPage); updateQuickCard(); }`
  che la richiamava ad ogni render — ripristinato l'unico `window.renderSed`
  originale (riga ~1431). Verificato: grep a zero risultati su
  `sq(Badge|InvPct|BarInv|OttPct|BarOtt|Rows|LottoRows)` e su
  `updateQuickCard`/`_origRenderSed`; 0 id duplicati nel file; `node --check`
  su JS inline estratto → OK.
- **rev.25** — `index.html`: revert di rev.22 su richiesta di Andrea dopo
  feedback estetico negativo (mockup fornito, vedi conversazione). La
  sezione SED torna ad essere una card full-width separata (`#sedSection`,
  stesso pattern/margin di `#tabellaSection`: `margin:18px 28px 32px`),
  posizionata subito prima di "Tutte le Pratiche" — **non più embedded**
  dentro la card "Avanzamento per Lotto". Rispetto alla versione
  pre-rev.22: font/padding tornati alle dimensioni standard (non più
  compressi), e aggiunta un'icona per ciascuna delle 5 KPI box
  (Ferroviario: binario, Autostradale: strada/monte, Idrico: goccia,
  Permessi Inviati: paper-plane, Permessi Ottenuti: scudo/check) — SVG
  stroke-based coerenti con lo stile icone già in uso nel file (es. icona
  di ricerca), badge colorato dietro ciascuna icona (`background:
  <colore-categoria>+"22"`, 22×22px, border-radius 6px). Rimossa la CSS
  morta `#sedEmbedded ...` (compattazione font, non più necessaria).
  Nessun id rinominato, stessa logica di rev.22 sul fatto che tutte le
  funzioni JS accedono solo via `getElementById` — nessuna dipendenza
  dalla posizione nel DOM. Verificato: 0 id duplicati, `node --check` su
  JS inline → OK, nessun residuo `sedEmbedded` nel file. Bilanciamento
  tag `<div>` verificato con conteggio regex: diff -1 pre-esistente anche
  nel file originale (falso positivo dovuto a HTML generato via
  concatenazione stringhe in JS, non un difetto introdotto da questa
  modifica).
- **rev.26** — `index.html`: aggiunta sidebar di navigazione verticale
  (`.app-sidebar`, 64px, `position:fixed`, sfondo `var(--retelit-blue)`)
  su richiesta di Andrea, da mockup fornito. 6 icone SVG stroke-based
  (stile Feather, coerenti con le altre icone già in uso nel file):
  Dashboard (griglia 2×2, attiva/evidenziata su sfondo bianco → punta a
  `index.html`, pagina corrente), Mappa (pin → `mappa.html`), Hub/
  Documenti (foglio → `hub.html`), Avanz. Lavori/Cantieri (casetta →
  `scavi.html`), Gantt/Avanzamento Temporale (barre+trend → `gantt.html`),
  Impostazioni/Admin (ingranaggio, path Feather standard verificato →
  `admin.html`). **Mapping icona→pagina è un'assunzione mia** — il
  mockup non specificava le destinazioni, dedotte da: (a) i 3 link già
  presenti nella topbar (Mappa, Avanz. Lavori→scavi.html, Hub), + (b)
  Gantt e Admin come pagine più probabili per le 2 icone rimanenti
  (chart/trending, gear). Da confermare con Andrea. `body` ha ora
  `padding-left:64px` per lasciare spazio alla sidebar fissa; su mobile
  (`@media max-width:768px`) la sidebar si nasconde (`display:none`) e
  il padding torna a 0 — il topbar-right con i link Mappa/Avanz.
  Lavori/Hub resta invariato e NON è stato rimosso (ridondante con la
  sidebar ma lasciato per non rompere nulla, da valutare rimozione).
  Implementata SOLO su `index.html` — se Andrea conferma il design, va
  replicata sulle altre pagine (mappa.html, scavi.html, admin.html,
  gantt.html, hub.html, ecc.) per coerenza UX in tutto il sito: task non
  ancora fatto. Verificato: link puntano a file esistenti nel repo, 0 id
  duplicati, `node --check` su JS inline → OK.
- **rev.27** — `milestone.html`: aggiunta nuova sezione statica
  "Milestone Progettazione" (4 righe, colonne N./Milestone/Descrizione/
  Scadenza, coerente con lo stile `.section-block` già in uso), inserita
  subito dopo il page-header e prima di `.tables-row` (Milestone
  Imprese/Contract Milestone esistenti, invariate). Dati forniti da
  Andrea via screenshot, applicabili a **tutti e 3 i lotti (A/B/C)**:
  01 Progetto (Capitolo 5 consegna documentazione punti 1-2-3) →
  11/09/2026; 02 Invio Permessi 1 (invio verso Provincia/Città
  Metropolitana, ANAS, Autostrade ecc.) → 30/09/2026; 03 Invio Permessi
  2 (invio verso tutti i Comuni interessati) → 16/10/2026; 04
  Ottenimento (tutte le autorizzazioni) → 31/05/2027. Date-pill colorate
  per anno (`dp-2026`/`dp-2027`, classi CSS già esistenti nel file).
  Tabella statica (no JS, no fetch) — se le date cambiano vanno
  aggiornate a mano in questo blocco HTML.
- **rev.28** — Sidebar (`.app-sidebar`, vedi rev.26) propagata a
  `milestone.html`, con l'icona Milestone marcata `active`. Aggiunta
  anche una **settima icona Milestone** in `index.html` (tra Gantt e
  Admin → `milestone.html`, path documento con check), dato che
  mancava dal set di 6 icone di rev.26. `index.html` ha ora 7 link in
  sidebar: Dashboard, Mappa, Hub, Avanz. Lavori, Gantt, Milestone, Admin.
  Verificato: 0 id duplicati, `node --check` su entrambi i file → OK.
  **Ancora da fare**: propagare la sidebar alle restanti pagine
  (mappa.html, hub.html, scavi.html, gantt.html, admin.html, e le altre:
  polizze_convenzioni, sopralluoghi, ai_alerts, imprese, imprese_scavi,
  mappa_impresa_caricamento, cartella `pm/`) — task confermato da
  Andrea ("va bene procedi") ma non ancora eseguito su queste pagine.
- **rev.29** — Colonna Master.csv `ORDINANZA`/`ORDINANZA NECESSARIA`
  rimossa dal file sorgente (nessuna riga TIPO_PERMESSO=ORDINANZA nei dati
  attuali), sostituita da Andrea con nuova colonna `CONCOMITANZA ENRI`
  (SI/vuoto, flag tratta in concomitanza col progetto ENRI). Il codice
  legacy per ORDINANZA (`_TIPO_PREFIX`, `_build_pratica`, `STATO_ORDINANZA`
  ecc.) NON è stato rimosso — resta innocuo (degrada a "NON NECESSARIO"/
  nessun match) ma è dead code in attesa di pulizia se Andrea conferma che
  ORDINANZA non tornerà mai più come TIPO_PERMESSO.
  - `backend/server.py`: `_compute_tratta_summary` calcola nuovo campo
    `CONCOMITANZA_ENRI` per TRATTA_ID (SI se una qualsiasi riga della
    tratta ha `CONCOMITANZA ENRI`=SI) e `LOTTO` (da `Source.Name`).
    `_regenerate_derived_files` ora scrive `CONCOMITANZA_ENRI` su
    QTS.geojson (prima il campo era esplicitamente escluso/statico,
    ereditato da QGIS — ora Master.csv è la fonte di verità).
    Nuovo endpoint `GET /api/admin/concomitanza-enri` (solo staff):
    elenco tratte SI a livello di TRATTA_ID, **indipendente dal numero
    PRATICA**. Aggiunto anche campo `concomitanza_enri` (SI/NO) ai
    risultati di `/api/admin/pratiche-search`.
  - **Bug scoperto durante l'implementazione**: tutte le 23 tratte
    attualmente in concomitanza (su 111 totali, verificato sul
    Master.csv reale caricato da Andrea) hanno ancora `PRATICA` vuoto
    (pratica non numerata) — `pratiche-search` esclude per design le
    righe senza numero pratica, quindi un badge lì sarebbe rimasto
    invisibile con i dati attuali. Per questo è stato aggiunto l'endpoint
    dedicato sopra, che non dipende dal numero pratica.
  - `admin.html` (tab "Dati pratiche"): badge pillola "ENRI" sul codice
    pratica quando `concomitanza_enri`=SI (visibile solo dopo che la
    pratica avrà un numero); ricercabile digitando "enri" nella barra di
    ricerca. Aggiunto blocco `<details>` collassabile sopra la tabella
    ("Concomitanza ENRI: N tratte") che carica da
    `/api/admin/concomitanza-enri` — questo è il punto dove le 23 tratte
    attuali sono effettivamente visibili oggi.
  - `mappa.html`: nuova riga "Concomitanza ENRI: SI" nel popup di
    dettaglio tratta (sezione "Dettaglio stato", accanto a Nulla Osta/
    Ordinanza), da `p.CONCOMITANZA_ENRI` (proprietà GeoJSON rigenerata
    da Master.csv). Non toccato `mappa_impresa_caricamento.html`
    (stessa struttura popup, logica duplicata) — da valutare se
    propagare anche lì, non richiesto esplicitamente da Andrea.
  - Verificato: `node --check` su JS inline di admin.html e mappa.html →
    OK; `_compute_tratta_summary` testata isolatamente sul Master.csv
    reale (111 tratte, 23 concomitanza SI); nessun id duplicato reale
    introdotto (falso positivo grep su `data-testid="dropzone"`, non
    modificato in questa sessione). Non testato end-to-end con
    backend+Mongo in esecuzione (solo unit-test isolato delle funzioni
    pandas) — verificare dopo il deploy che `/api/admin/concomitanza-enri`
    e il popup mappa rispondano coi dati reali.
- **rev.30** — Sincronizzazione cross-progetto con ENRI per le tratte in
  concomitanza: la pratica di autorizzazione per quelle tratte è gestita e
  seguita nel progetto ENRI (Telebit non se ne occupa su QTS), quindi il
  Master.csv di QTS resta fermo su di esse a tempo indefinito — serve lo
  stato reale letto da ENRI. Deciso con Andrea: NON rinumerare i TRATTA_ID
  tra i due progetti (troppo rischioso su sistemi già in produzione con
  storico). **Corrispondenza reale (chiarita da Andrea con un secondo
  Master.csv)**: non è per TRATTA_ID ma per PRATICA — sulle righe con
  CONCOMITANZA ENRI=SI, Andrea valorizza il campo PRATICA con
  `<numero>_<lotto ENRI>` (es. "14_2") invece del numero pratica QTS, per
  indicare a quale pratica ENRI (formato interno "AUT/14/2"/"NO/32/2")
  fa riferimento quella riga. Più tratte QTS possono puntare alla stessa
  pratica ENRI (N:1), e una stessa tratta QTS può avere riferimenti diversi
  per AUTORIZZAZIONE e NULLA OSTA (1:N) — gestito.
  - **QTS `backend/server.py`**: nuova config `ENRI_API_BASE` (default
    `https://enri-dashboard-api.onrender.com`) ed `ENRI_SYNC_TOKEN` (env
    var da impostare su Render QTS, deve combaciare con `QTS_SYNC_TOKEN`
    lato ENRI). Nuovo `_parse_enri_pratica_rif()` (split su "_" del campo
    PRATICA), nuovo `_fetch_enri_pratica_status()` con cache in-process
    5 minuti (`_enri_sync_cache`/`_ENRI_SYNC_TTL`, chiave = JSON delle
    lookup keys) — ENRI è su Render free tier e può essere addormentato,
    oltre a non voler chiamare l'API ad ogni refresh del pannello admin.
    `/api/admin/concomitanza-enri` riscritto: per ogni riga SI estrae
    {ente, tipo_permesso, numero, lotto} dal campo PRATICA, deduplica le
    chiavi di lookup, chiama in batch (POST) l'endpoint ENRI e arricchisce
    ogni tratta con `riferimenti_enri: [{codice, enri_stato}, ...]` (array,
    non singolo valore — vedi N:1/1:N sopra). Righe con PRATICA non ancora
    nel formato atteso restano con `riferimenti_enri: []` ("non ancora
    inserito"), non causano errori.
  - **ENRI `backend/server.py`** (file NON nel repo QTS — Andrea gestisce
    il deploy separatamente su un altro servizio Render, base url
    `https://enri-dashboard-api.onrender.com`): nuovo endpoint
    `POST /api/external/pratica-status` **read-only**, body
    `{"items": [{"ente","tipo_permesso","numero","lotto"}, ...]}`, protetto
    da un token dedicato **`QTS_SYNC_TOKEN`** (env var da creare,
    volutamente separato da `UPLOAD_TOKEN` che ha permessi di scrittura —
    principio del privilegio minimo: se questo token trapela, espone solo
    stato_permesso/date/nota delle pratiche esplicitamente richieste, mai
    l'intero Master.csv né azioni admin). Cerca la pratica con lo stesso
    criterio di identità usato da `/api/admin/pratiche-search` di ENRI
    (ente+tipo_permesso+numero+lotto, lotto derivato da `_lotto_from_source`
    su Source.Name). Il file patchato è stato consegnato ad Andrea come
    `enri_server_patched.py` (diff minimale, solo additivo) da applicare
    manualmente al repo ENRI e deployare — Claude non ha accesso diretto
    al repo/Render di ENRI in questa sessione. **Nota**: una prima versione
    di questo endpoint (keyed per TRATTA_ID, `GET /api/external/tratte-status`)
    era stata consegnata ad Andrea PRIMA di vedere i dati reali — scartata e
    sostituita nella stessa sessione, mai deployata.
  - **admin.html**: pannello "Concomitanza ENRI" (rev.29) esteso con due
    colonne — "Rif. ENRI" (uno o più codici tipo "AUT/14/2", uno per riga
    se la tratta ne ha più di uno) e "Stato ENRI" (verde se OTTENUTO, ambra
    altrimenti, grigio se non trovata/non disponibile/non ancora inserita).
    Banner di avviso (`#enriSyncWarn`) se la chiamata a ENRI fallisce.
  - **⚠️ Inconsistenza nei dati trovata e segnalata ad Andrea, non ancora
    corretta**: il riferimento "17_2" (AUTORIZZAZIONE) compare sia su
    TR_0034 con ente "COMUNE DI PADERNO DUGNANO" sia su TR_0041/TR_0064/
    TR_0065 con ente "PROVINCIA DI MILANO" — stesso codice pratica ENRI,
    due enti diversi nel Master.csv QTS. Probabile refuso su una delle due
    (verificare quale ente ha realmente la pratica AUT/17/2 su ENRI):
    finché non corretto, una delle due lookup fallirà sempre ("pratica non
    trovata su ENRI") perché la ricerca lato ENRI include l'ente nella
    chiave di identità.
  - **Scoperta rilevante durante l'analisi di ENRI**: esiste già in ENRI
    una collection Mongo `concomitanza_col` + endpoint
    `GET /api/concomitanze` / `POST /api/admin/concomitanze/import`, con
    `fonte` default letteralmente `"ENRI-QTS"` — ma è un concetto diverso
    (TRATTA_ID *lato ENRI* che richiedono un tubo aggiuntivo per la
    sovrapposizione fisica con QTS in fase di scavo, non lo stato della
    pratica). Non approfondito oltre — il meccanismo per PRATICA sopra
    risolve comunque il bisogno attuale, non serve più incrociarlo.
  - **Ancora da fare**: (1) Andrea corregge l'inconsistenza ente su "17_2";
    (2) applica `enri_server_patched.py` (versione POST pratica-status,
    non quella precedente) al repo ENRI e deploya; (3) imposta lo stesso
    valore segreto come `QTS_SYNC_TOKEN` (env ENRI) e `ENRI_SYNC_TOKEN`
    (env QTS su Render); (4) verifica end-to-end in produzione (non
    testabile da Claude: richiede i due backend live + Mongo reale).
    mappa.html non ancora esteso con lo stato live ENRI (per ora resta
    solo il flag SI/NO statico da Master.csv, rev.29).
- **rev.31** — Task (2) di rev.30 completato: `enri_server_patched.py`
  (consegnato ad Andrea, non nel repo QTS) integrato nel `server.py` di
  ENRI più recente fornito da Andrea, che nel frattempo aveva già
  l'endpoint `GET /api/cantieri/scavi-timeseries` (assente nella versione
  base su cui era stato costruito il patch) — integrazione fatta a mano,
  nessuna regressione: `QTS_SYNC_TOKEN`, `_check_qts_sync_token()` e
  `POST /api/external/pratica-status` aggiunti senza toccare
  `scavi-timeseries`. Verificato `python3 -m py_compile` OK, nessuna
  route duplicata, `Header`/`Annotated` già importati.
  - **Bug trovato e corretto durante l'integrazione**: il confronto lotto
    in `/api/external/pratica-status` era case-sensitive
    (`work["_lotto"] == lotto`), ma `_lotto_from_source()` normalizza
    sempre in maiuscolo lato ENRI (lotti reali `1A/1B/2A/2B/...`) mentre
    il lotto arriva da QTS come sottostringa grezza del campo PRATICA
    (es. "14_2a" invece di "14_2A") senza normalizzazione — con lotti a
    lettera il lookup avrebbe silenziosamente fallito ("pratica non
    trovata") ad ogni discrepanza di maiuscole/minuscole in quel campo
    Excel. Fix: `lotto = str(it.get("lotto","")).strip().upper()` prima
    del confronto. **Non serve modificare nulla lato QTS** (il campo
    PRATICA resta libero, la normalizzazione ora è tutta sul lato ENRI).
  - Verificata anche la logica lato QTS (`_parse_enri_pratica_rif`,
    `_fetch_enri_pratica_status`, `/api/admin/concomitanza-enri`): le
    chiavi ente/tipo_permesso/numero combaciano col confronto ENRI
    (entrambi upper-case su ente e tipo_permesso), nessuna altra
    incoerenza trovata.
  - File integrato consegnato ad Andrea come `server.py` (da applicare al
    repo ENRI, non in questo repo QTS) — **ancora da fare**: (1) Andrea
    corregge l'inconsistenza ente su "17_2" (rev.30, non ancora fatta);
    (2) deploy del nuovo `server.py` su Render ENRI; (3) imposta
    `QTS_SYNC_TOKEN` (env ENRI) = `ENRI_SYNC_TOKEN` (env QTS, già presente
    lato QTS da rev.30); (4) test end-to-end in produzione.
  - **`index.html` QTS**: nessun riferimento a concomitanza/ENRI trovato
    nel file attuale (la feature vive solo in `admin.html` e `mappa.html`,
    rev.29/30) — chiesto ad Andrea cosa intende aggiornare lì prima di
    intervenire, per non introdurre modifiche non richieste.
- **rev.32** — Chiarimento da Andrea: le pratiche in concomitanza ENRI
  sono gestite da **Sertori**, non da Telebit (Telebit resta il
  contrattista generico per Lotto A/B/C). Corretto in `admin.html`
  (tooltip pannello Concomitanza ENRI) e in 2 commenti/docstring di
  `backend/server.py` (incluso un refuso residuo: il commento citava
  ancora l'endpoint scartato `/api/external/tratte-status` invece di
  `/api/external/pratica-status`).
  - **`index.html`**: aggiunta lettura colonna `CONCOMITANZA ENRI` dal
    Master.csv (stesso `findCol` pattern delle altre colonne), propagata
    come flag booleano `concomEnri` attraverso l'intera pipeline dati
    lato client — `permessiMap` (OR logico sui merge/aggiornamenti riga,
    il flag non deve mai sparire quando arriva una riga più recente senza
    quella colonna valorizzata), `praticheByLotto`/`_praticheDetailPerLotto`
    (OR logico su tutte le tratte della stessa pratica) e
    `_masterByTratta` (per eventuali popup mappa embedded in index.html).
    In `getAllPrats()` — il punto unico da cui derivano tabella, filtri,
    KPI e la card di dettaglio pratica — l'`impresa` mostrata ora è
    `'Sertori'` se `concomEnri` è true, altrimenti il default
    `IMPRESE_PER_LOTTO[lotto]` (Telebit) invariato. Aggiornati anche i
    due path paralleli usati dal modale "colonne" (`_colGetDisplay`/
    `_colGetSort`, filtro e ordinamento colonna Impresa) e la card di
    dettaglio pratica (sezione "Impresa" con icona). **Non toccati**
    i punti che mostrano l'impresa a livello di LOTTO intero (modale
    "Lotto — Dettaglio", grafico a barre per lotto, header gruppo lotto
    nelle tabelle KPI): lì il default Telebit resta corretto, dato che
    un lotto ha sempre anche pratiche non-concomitanti.
  - Verificato `node --check` su tutti e 6 i blocchi `<script>` inline di
    `index.html` → OK.
  - **Nota per Andrea**: questo fix copre solo `index.html`. Chiarito che
    NON è ancora un aggiornamento "live" da ENRI — è comunque il flag
    statico SI/NO letto da Master.csv (come su `mappa.html`, rev.29), solo
    che ora sull'impresa mostrata compare "Sertori" invece di "Telebit".
    L'auto-refresh dello **stato** della pratica letto in tempo reale da
    ENRI (come già avviene in `admin.html` via
    `/api/admin/concomitanza-enri`) NON è stato ancora implementato su
    `index.html`/`mappa.html` — confermato con Andrea: `mappa.html` è
    solo staff-facing, quindi non ci sono vincoli di privilegio a
    riusare lì l'endpoint staff-only. **Ancora da fare, prossima
    sessione**: (1) estendere `mappa.html` per chiamare
    `/api/admin/concomitanza-enri` (o un endpoint equivalente) nel popup
    tratta invece del solo flag statico SI/NO; (2) valutare se
    aggiungere anche su `index.html` uno stato live (richiede decidere
    dove/come mostrarlo, dato che lì il dato è per-pratica aggregato da
    più tratte, non per-tratta come in mappa.html).
- **rev.33** — Nuova richiesta di Andrea: quando ENRI segna OTTENUTO una
  pratica in concomitanza, l'aggiornamento deve essere **scritto/persistito**
  nel Master.csv di QTS (non solo mostrato live in admin.html come da
  rev.30/32) — altrimenti `pratiche-search`, `index.html` e `mappa.html`
  (che leggono solo Master.csv, mai ENRI in tempo reale) resterebbero
  indefinitamente allo stato congelato. Confermato con Andrea: match per
  **codice pratica** (ENTE+TIPO_PERMESSO+PRATICA-parsata), MAI per
  TRATTA_ID.
  - **Nuovo endpoint `POST /api/admin/concomitanza-enri/sync-master`**
    (`backend/server.py`, protetto da `x-upload-token` come le altre
    scritture admin). A differenza di `/api/admin/concomitanza-enri`
    (aggregato per TRATTA_ID), itera **riga per riga** di Master.csv: una
    tratta può avere righe AUTORIZZAZIONE e NULLA OSTA con due pratiche
    ENRI diverse, quindi il match dev'essere per riga, non per tratta.
    Per ogni riga con `CONCOMITANZA ENRI`=SI e PRATICA nel formato
    `<numero>_<lotto>`: lookup batch su ENRI (`_fetch_enri_pratica_status`,
    stesso helper di rev.30), e se il risultato è OTTENUTO e la riga QTS
    non lo è già, scrive `STATO_PERMESSO=OTTENUTO` +
    `DATA_APPROVAZIONE=<da ENRI>` **in-place** (stesso pattern di
    `update_admin_pratica`, `_apply_changes_to_df` con `in_place=True`)
    — non tocca NOTE per non perdere lo storico. Idempotente: nessuna
    scrittura/nessuna nuova versione Master.csv se non ci sono nuove
    approvazioni. `_write_master_csv` già rigenera da sé i derivati e il
    push GitHub (nessuna modifica necessaria lì).
  - **Bug potenziale trovato e corretto in fase di test**: Master.csv ha
    più righe storiche per la stessa tratta+tipo+pratica (una per cambio
    stato nel tempo — confermato sul CSV reale caricato da Andrea: 44
    righe SI collassano a 7 chiavi ENRI uniche ma restano più righe per
    TRATTA_ID). Senza dedup l'endpoint avrebbe accodato N `changes`
    identiche per la stessa tratta (innocuo perché `_apply_changes_to_df`
    risolve comunque sull'ultima riga, ma sporco nella risposta
    `dettaglio`) — aggiunto dedup esplicito su (tratta, ente, tipo,
    pratica) prima di costruire le `changes`.
  - **`admin.html`**: `loadConcomitanzaEnri()` ora, dopo il refresh
    normale (GET, invariato, nessun side-effect), chiama in automatico
    `sync-master` (POST) e se sono state applicate scritture ricarica la
    tabella mostrando un banner verde con il conteggio e il nuovo
    upload_id; se il sync fallisce (es. token upload non impostato in
    questa sessione) fallisce silenziosamente senza rompere la vista.
    Parametro `triggerSync=false` per evitare loop di ricorsione sul
    ricaricamento post-sync. Fix minore: il colore di `#enriSyncWarn` ora
    viene sempre resettato a inizio funzione (prima poteva restare verde
    da un sync riuscito anche quando appariva un vero `enri_error` al
    giro successivo).
  - Validato a mano (senza rete verso ENRI) il parsing/dedup sul
    `Master.csv` reale caricato da Andrea: 155 righe totali, 44 con
    CONCOMITANZA ENRI=SI, 7 chiavi ENRI uniche corrette.
  - **Trigger attuale = quando l'admin apre/aggiorna il tab "Note
    pratiche" di admin.html** (non un webhook/push da ENRI in tempo reale
    — ENRI non ha modo di notificare QTS quando un admin approva una
    pratica, l'architettura resta pull-based come da rev.30). Se Andrea
    vuole un aggiornamento più "immediato" (es. ad ogni upload di
    Master.csv su ENRI, o su un cron), va aggiunta una chiamata
    server-to-server esplicita da ENRI verso questo endpoint — non
    implementato, da valutare se serve davvero dato il costo aggiuntivo
    (ENRI dovrebbe conoscere URL+token di QTS, accoppiamento nella
    direzione opposta a quella attuale).
  - **Ancora da fare**: test end-to-end reale con i due backend live
    (non eseguibile da Claude, richiede Mongo+ENRI raggiungibile); Andrea
    corregge l'inconsistenza ente "17_2" (rev.30, ancora aperta) prima
    che il sync possa scrivere correttamente su quella pratica.
- **rev.34** — Tre richieste di Andrea nella stessa sessione:
  1. **Sync ENRI→QTS esteso a ogni cambio di stato (non solo OTTENUTO)**.
     `_sync_enri_to_master()` (nuova funzione condivisa, estratta dal corpo
     di `sync_concomitanza_enri_to_master`) ora confronta riga per riga
     `STATO_PERMESSO`, `DATA_RICHIESTA`, `DATA_APPROVAZIONE`,
     `DATA_PREVISTA_RILASCIO` con la risposta ENRI e scrive qualunque campo
     diverso (non solo quando ENRI=OTTENUTO), sempre a livello di riga
     Master.csv (match ENTE+TIPO_PERMESSO+PRATICA-parsata, mai TRATTA_ID,
     invariato da rev.33). Un valore ENRI vuoto non sovrascrive mai il dato
     QTS esistente. **NOTE non è mai sovrascritta**: se ENRI restituisce una
     `nota`, viene ACCODATA con tag `[ENRI] ...` solo se quel testo non è
     già presente in coda (idempotente sui poll ripetuti), per non perdere
     lo storico note QTS. Verificati con Andrea i campi esposti da
     `/api/external/pratica-status` lato ENRI (incollato `server.py` ENRI
     aggiornato): `stato_permesso`, `data_richiesta`, `data_approvazione`,
     `data_prevista_rilascio`, `nota`, `trovata` — schema confermato,
     nessuna assunzione.
  2. **Propagazione automatica via polling**, non più solo manuale
     dall'apertura della tab "Note pratiche" di admin.html (che resta
     comunque disponibile, ora chiama `_sync_enri_to_master` condivisa).
     Nuovo task in background avviato allo startup (`_enri_sync_poll_loop`,
     stesso pattern di `_startup_sync_cantieri`): dorme
     `ENRI_SYNC_POLL_SECONDS` (env, default 1800s/30min) e richiama
     `_sync_enri_to_master("sync-enri-auto")`; no-op silenzioso se
     `ENRI_SYNC_TOKEN` non è configurato. Verificato `python3 -m py_compile`
     OK.
  3. **`index.html`**: nei lotti A e C (quelli con pratiche in concomitanza
     ENRI) il chip "Avanzamento per Lotto" ora mostra "Sertori" sotto
     "Telebit", colore distinto (`--accent2`, teal, già nel palette token
     — nessun hex hardcoded nuovo). Derivato dinamicamente da
     `window._praticheDetailPerLotto[lotto].some(p => p.concomEnri)`, non
     hardcoded sui lotti A/C: se in futuro la concomitanza comparisse su un
     altro lotto, "Sertori" comparirebbe lì automaticamente. Non toccato il
     modale "Lotto — Dettaglio" (mostra solo Telebit, invariato da
     rev.32 — un lotto ha sempre anche pratiche non-concomitanti).
     Verificato `node --check` su tutti e 6 gli script inline.
  4. **Sidebar rimossa per il ruolo impresa in `hub.html`**: le tre pagine
     impresa-facing (`imprese.html`, `imprese_scavi.html`,
     `mappa_impresa_caricamento.html`) non avevano mai una sidebar di
     navigazione tra pagine (solo `.app-sidebar` — nav-rail icone verso
     index/scavi/mappa/polizze/sopralluoghi/gantt/milestone/admin — presente
     su `admin.html`/`index.html`/`scavi.html`/`mappa.html`/`hub.html`/ecc.,
     mai su quelle 3): il problema reale era che `hub.html`, pagina di
     ingresso comune a tutti i ruoli, mostrava quella sidebar completa anche
     alle imprese, che però vedono solo le card impresa dopo il login.
     Fix: nello script IIFE che già nascondeva le icone Admin/Gantt per i
     ruoli non abilitati, aggiunto un branch per `ruolo === 'impresa'` che
     nasconde l'intera `.app-sidebar` e azzera `body.padding-left` (recupera
     lo spazio riservato alla sidebar). Le 3 pagine impresa restano
     invariate (già solo topbar). Verificato `node --check` sui 2 script
     inline di `hub.html`.
- **rev.35** — Bug reale trovato da Andrea: le pagine Area Impresa
  filtravano solo per LOTTO, non escludevano le pratiche/tratte con
  CONCOMITANZA ENRI=SI (gestite da Sertori via ENRI, non dall'impresa del
  lotto) — Telebit le avrebbe viste comunque, essendo nello stesso lotto
  A/C. Fix in `backend/server.py`:
  - Nuovo helper `_is_sertori(nome)` (case-insensitive) — le righe/tratte in
    concomitanza restano visibili SOLO a un'impresa il cui nome è
    esattamente "Sertori" (non ancora registrata come account impresa, ma
    l'helper è pronto per quando lo sarà).
  - `/api/imprese/pratiche`: esclude le righe Master.csv con
    `CONCOMITANZA ENRI`=SI per chi non è Sertori.
  - `/api/imprese/master-sed`: esclude le feature GeoJSON con
    `CONCOMITANZA_ENRI`=SI (proprietà già presente via
    `_compute_tratta_summary`) dallo stesso scoping.
  - `/api/imprese/solleciti`: le tratte in concomitanza vengono tolte dal
    set `tratte_impresa` prima della query solleciti.
  - **`/api/imprese/cantieri` (tab Scavi di imprese_scavi.html) NON
    toccato**: i documenti cantiere non hanno un flag concomitanza salvato,
    e Andrea ha confermato che gli scavi non sono ancora assegnati a
    nessuno per queste tratte (fase attuale = solo permessi) — nessuna
    azione richiesta ora, da rivalutare quando gli scavi verranno assegnati.
  - Verificato `python3 -m py_compile` OK.
- **rev.36** — Bug segnalato da Andrea: al primo login come impresa la
  sidebar `.app-sidebar` compariva comunque nell'hub per un istante (spariva
  solo tornando indietro dopo aver aperto un'altra pagina). Causa: l'hide
  (rev.34) girava solo nell'IIFE di parse-time che legge `_qts_role` da
  localStorage — al primissimo login quella chiave non è ancora stata
  scritta (lo è solo dopo la verifica server in `_showHub`), quindi la
  sidebar restava visibile finché non si ricaricava una pagina con il ruolo
  già cache-ato. Fix: stessa logica di hide (nascondi `.app-sidebar`,
  azzera `body.padding-left`) aggiunta anche dentro `_showHub()`, dove
  `ruolo`/`isImpresa` sono già noti dalla risposta server — copre sia il
  primo login sia i successivi. Verificato `node --check` sui 2 script
  inline di `hub.html`.
- **rev.37** — Rimosso il campo "Cluster" dal popup tratta di
  `mappa_impresa_caricamento.html` (richiesta Andrea) — `.popup-grid` è
  auto-flow (`grid-template-columns:1fr 1fr 1fr`), nessun buco lasciato
  dagli altri campi. Verificato `node --check` sui 5 script inline.
  Chiarito con Andrea perché il Master.csv risultava invariato dopo il
  deploy di rev.34: `ENRI_SYNC_TOKEN` non è ancora impostato su Render QTS
  (confermato "No/non so"), quindi sia il trigger manuale che il polling
  fanno no-op silenzioso (`_fetch_enri_pratica_status` ritorna
  `enri_error="ENRI_SYNC_TOKEN non configurato..."`). Da fare lato Andrea:
  stesso valore in QTS_SYNC_TOKEN (Render ENRI) e ENRI_SYNC_TOKEN (Render
  QTS), poi redeploy di entrambi.
- **rev.38** — Bug reale trovato con Andrea: dopo aver corretto l'ente
  "PROVINCIA DI MB"→"PROVINCIA DI MONZA E BRIANZA" su Master.csv QTS (che
  ha risolto il matching, confermato dalla GET /api/admin/concomitanza-enri
  che ora trova le pratiche), il trigger manuale del sync da admin.html
  continuava ad apparire come "non ha fatto nulla" — nessun messaggio,
  nessun errore. Causa reale: **il frontend nascondeva completamente
  l'esito** quando `aggiornate === 0` o la chiamata falliva — il blocco
  `try { if (s.aggiornate > 0) {...} } catch { /* sync silenzioso */ }` in
  `loadConcomitanzaEnri()` non mostrava mai nulla in quei due casi, quindi
  Andrea non aveva modo di distinguere "0 modifiche perché già allineato"
  da "0 modifiche perché il sync sta fallendo silenziosamente" — diagnosi
  bloccata dalla UI stessa, non (necessariamente) dalla logica di sync.
  Fix in `admin.html`: ora il banner `warn` mostra sempre un esito —
  successo (verde), `enri_error` esplicito (giallo), "nessuna modifica,
  N/M pratiche trovate su ENRI già allineate" (grigio), o l'errore
  dell'eccezione (rosso) se la chiamata fallisce del tutto. Backend
  `_sync_enri_to_master()`: aggiunti `pratiche_totali`/`pratiche_trovate`
  alla risposta (anche nel path "nessuna modifica") per dare quel
  conteggio diagnostico anche quando `dettaglio` è vuoto (conteneva solo
  le pratiche con differenze reali, non quelle controllate e già
  allineate — fuorviante come proxy di "quante ne ho controllate").
  **Nessun bug trovato nella logica di matching/scrittura stessa**
  (`_sync_enri_to_master`/`_apply_changes_to_df`): stessa identità
  ente+tipo+pratica della GET che già funziona, stesso `_read_master_csv()`
  con cache invalidata per versione. Prossimo passo per Andrea: rilanciare
  il sync ora che il banner mostra l'esito reale — se dice "enri_error" o
  "0/N trovate" nonostante la GET trovi tutto, è un indizio nuovo da
  seguire; se scrive ma i valori restano diversi da quanto atteso, serve
  vedere `dettaglio` (loggato ma non ancora mostrato in tabella).
  Verificato `python3 -m py_compile` e `node --check` su entrambi i file.
- **rev.39** — Bug reale trovato: pratiche in concomitanza ENRI non si
  aggiornavano su `index.html` nonostante `_sync_enri_to_master` scrivesse
  correttamente la nuova riga su Master.csv (confermato da Andrea via
  Master.csv scaricato: riga `IN FIRMA RDS` presente con `DATA_ULTIMA_
  MODIFICA` valorizzata per tutte le tratte in concomitanza). Causa radice:
  `_processMasterText()` in `index.html` faceva `text.trim().split('\n')`
  PRIMA di interpretare le virgolette — ogni riga scritta da
  `_sync_enri_to_master` ha NOTE con newline letterale incorporato
  (`"SP45\n[ENRI] ..."`, quotato correttamente da `pandas.to_csv`), quindi lo
  split naive spezzava quella riga in due a metà record, azzerando
  tratta/prat/stato sulla riga risultante → scartata silenziosamente da
  `if (!tratta || !prat || !stato) continue`. `permessiMap` restava quindi
  sull'ultima riga valida, cioè `IN REDAZIONE`. Bug sistemico: colpisce
  OGNI riga toccata dal sync ENRI (nota `[ENRI] ...` sempre accodata con
  `\n`), non un caso isolato. Fix: `_processMasterText` ora usa un
  tokenizer CSV quote-aware che spezza record solo su `\n`/separatore FUORI
  da campi quotati (gestisce anche `""` come quote escape); `lines`/
  `splitLine` mantenuti come alias per compatibilità col resto della
  funzione (nessun'altra riga toccata). Verificato in Node contro il
  Master.csv reale di Andrea: 155/155 righe ora parsate correttamente,
  incluse tutte le righe `IN FIRMA RDS` con nota `[ENRI]`.
  **Da verificare**: `gantt.html` (riga ~773) ha lo stesso pattern
  `text.trim().split('\n')` su un CSV diverso (dati Gantt, non Master.csv) —
  non risulta ancora rotto perché quel CSV non ha campi con newline
  incorporato, ma è lo stesso bug potenziale se in futuro un campo note lì
  contenesse `\n`. Non toccato in questa sessione (nessuna nota "a capo" in
  quel CSV a oggi).
- **rev.40** — Verifica richiesta da Andrea: stesso bug di rev.39 controllato
  su `mappa.html`. Risultato:
  - **Layer tracciato principale** (colore tratta, badge "Concomitanza ENRI"
    nel popup tratta): NON affetto — legge `p.STATO_LEGENDA`/
    `p.CONCOMITANZA_ENRI` da `QTS.geojson`, calcolato lato backend da
    `_compute_tratta_summary`/`_regenerate_derived_files` via pandas
    (gestisce correttamente i campi quotati multi-riga).
  - **Popup SED** (attraversamenti, `_buildSedLayer`/`onEachFeature`): AFFETTO
    — stesso bug di rev.39. `_loadSEDInner()` (riga ~2119) faceva
    `csvText.split('\n')` un secondo parsing client-side di Master.csv
    indipendente da quello di `index.html`, con lo stesso problema sulle
    righe con NOTE `[ENRI] ...` a capo. Stesso fix applicato: tokenizer
    CSV quote-aware, stessa logica di `_processMasterText`. Verificato in
    Node contro il Master.csv reale: 155/155 righe parsate, righe
    `IN FIRMA RDS` per pratica `13_2`/`14_2` ora visibili (anche se per
    queste due pratiche specifiche `N_SED` è vuoto in Master.csv, quindi
    non comparirebbero comunque in un popup SED — nessun SED associato,
    non è un problema del parser). Verificata invece pratica `32_2`
    (6 tratte con `N_SED` popolato, es. `SED-002`/`SED-016`): risulta
    ancora `IN REDAZIONE` su tutte — dato reale non ancora sincronizzato da
    ENRI (nessuna riga gemella `IN FIRMA RDS`), non un bug del parser.
    Verificato `node --check` (via estrazione script inline) su tutti gli
    script di `mappa.html`.
- **rev.41** — Richiesta Andrea: allineare `mappa.html` QTS al file
  `mappa.html` di ENRI per tasto Sopralluogo e "Apri con Google" (file ENRI
  fornito come riferimento, non applicato 1:1 all'intero file — solo le due
  feature richieste). Confronto diretto:
  - **Tasto Sopralluogo** (`cantiereHtml`, link a `sopralluoghi.html?lotto=
    ...&cantiere=...&indirizzo=...`): già identico byte-per-byte tra i due
    progetti — nessuna modifica.
  - **Popup SED / "Apri con Google Maps" lì**: già identico — nessuna
    modifica.
  - **Popup tratta principale (`makePopupHtml`), pulsante "Apri in Google
    Maps"**: QTS aveva ancora un blocco a tutta larghezza in fondo al popup
    (versione vecchia, pre-refactor ENRI); ENRI l'ha sostituito con
    un'icona compatta nell'header, accanto al pulsante di chiusura ✕.
    Applicata la stessa struttura a QTS: icona `<a class="popup-close-btn"
    href="${gmapsUrl}">` con pin SVG prima del bottone ✕, rimosso il vecchio
    blocco `<div style="padding:0 16px 12px">...Apri in Google Maps</div>`
    in fondo al popup. Nessun'altra riga della funzione toccata (stessa
    logica dati, solo riposizionamento markup). Verificato `node --check`
    su tutti gli script inline di `mappa.html`.
- **rev.42** — Richiesta Andrea: popup mappa tratta "troppo grosso e
  invasivo" + si apre sopra la tratta selezionata. Portate 2 ottimizzazioni
  già presenti su ENRI (dati QTS-specifici invariati, es. `praticheHtml`
  resta la versione semplice di QTS senza ente/badge concomitanza — quello
  è codice ENRI-specifico, non portato):
  1. **Sezione "Pratiche" fusa nella griglia campi** (`popup-field full`,
     chip in flex-wrap) invece di `.popup-section` separata sotto con
     titolo+bordo — elimina un blocco verticale intero quando la tratta ha
     pratiche associate (caso comune). `hasDetail` nel calcolo margin-bottom
     ora confronta con `cantiereHtml` invece di `pratiche.length` (coerente
     con ENRI, dato che pratiche non è più una sezione a parte).
  2. **`offset: L.point(360, -10)`** su `layer.bindPopup()` (solo desktop,
     `isMobile` resta centrato in basso come prima): il bordo sinistro del
     popup (max-width 640, metà=320+margine) resta sempre a destra del
     punto cliccato, quindi non copre più la tratta selezionata. Su mobile
     nessun offset laterale (schermo stretto, non ha senso spostarlo).
  Verificato `node --check` su tutti gli script inline di `mappa.html`.
- **rev.43** — Richiesta Andrea: nel popup tratta, campo "Cluster" → "Impresa".
  Aggiunta `IMPRESE_PER_LOTTO = {A:Telebit, B:Telebit, C:Telebit}` (stessa
  mappa statica già usata in `index.html`, mancava in `mappa.html` dove
  l'unico `IMPRESE` era un oggetto vuoto — commento originale "QTS non ha
  una mappa lotto→impresa" era ormai superato). Nuova variabile
  `impresaTratta`: `Sertori` se `CONCOMITANZA_ENRI === 'SI'` (stessa
  precedenza usata in `index.html`/`IMPRESE_PER_LOTTO[p.lotto]`), altrimenti
  `IMPRESE_PER_LOTTO[p.LOTTO]`. Sostituito il campo Cluster nella griglia
  popup con questo valore, nessun'altra riga toccata. Verificato
  `node --check` su tutti gli script inline di `mappa.html`.
