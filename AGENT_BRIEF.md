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
4. [ ] **Testare login** da `hub.html` con un nome/codice presente nel
       foglio Utenti QTS.
5. [ ] **Aggiornare `DEFAULT_API_BASE`** in `js/api-config.js` e
       `api-config.js` (root, sono duplicati) con l'URL reale del Web
       Service Render (es. `https://qts-dashboard-xyz.onrender.com`).
6. [ ] **Aggiornare link GitHub Pages** in `hub.html` (placeholder
       `https://qts-rds.github.io/dashboard/...`) con l'URL Pages reale
       una volta pubblicato il frontend.
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
