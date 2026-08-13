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
- **Config backend**: `GITHUB_REPO` (env var, default attuale `QTS-RDS/dashboard` — **da verificare/correggere** con il nome reale del repo GitHub, vedi §5), `MONGO_URL`, `DB_NAME`.

## 4. Brand kit (obbligatorio)

Applicare sempre il brand kit Retelit (`brandkitretelit.md`, se presente nel repo):
- Palette blu monocromatica — **niente colori caldi** (no arancione/giallo/rosso)
- Font Raleway
- Nessuna emoji, nessun gradiente decorativo
- Tono sobrio B2B infrastrutturale
- Border-radius componenti UI: 8–12px
- Numeri grandi con unità inline, formato italiano (punto come separatore migliaia)

Citare la sezione del brand kit pertinente quando informa una scelta di design.

## 5. Cosa serve completare (TODO aperti da questa sessione di setup)

Rinominato in automatico **ENRI → QTS** in tutto il codice (titoli pagina,
namespace JS, chiavi localStorage, log console, commenti, GITHUB_REPO
default), preservando `enrich`/`enriched` (falsi positivi). Restano da
definire con dati reali del progetto QTS:

- [ ] **`GITHUB_REPO`** in `backend/server.py` (riga ~994): attualmente
      `QTS-RDS/dashboard` per continuità con lo schema precedente — va
      sostituito con l'organizzazione/repo GitHub reale del progetto QTS.
- [ ] **Link GitHub Pages** in `hub.html` (es. `https://qts-rds.github.io/dashboard/...`) — stesso discorso.
- [ ] **File sorgente dati**: i riferimenti a file Excel/CSV/QGIS del progetto
      ENRI (`Riepilogo_progettazione.csv`, `Master.csv`, `QGIS.geojson`,
      `Progetto_QTS_GANTT_Cluster_1-2.mpp` — quest'ultimo rinominato
      automaticamente da `Progetto_ENRI_GANTT_Cluster_1-2.mpp` in `gantt.html`,
      ma il file `.mpp` reale è diverso per QTS) vanno sostituiti con i nomi/percorsi
      reali dei file del progetto QTS non appena disponibili.
- [ ] **`DEFAULT_API_BASE`** in `js/api-config.js` / `api-config.js` (placeholder
      `https://qts-dashboard-api.onrender.com`) da aggiornare dopo il deploy Render.
- [ ] Verificare se esiste un `brandkitretelit.md` dedicato o se va riportato dal progetto ENRI.
- [ ] Lotti/cluster: verificare se la struttura lotti (1A/1B/2A/2B) è la stessa o cambia per QTS.

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
  TODO aperti: vedi §5.
