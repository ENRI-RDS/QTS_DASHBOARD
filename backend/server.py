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
10. [ ] Lotti/cluster: verificare se la struttura lotti (1A/1B/2A/2B) è la
        stessa o cambia per QTS.

## 6. Log revisioni

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
