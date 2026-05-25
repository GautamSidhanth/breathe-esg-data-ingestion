<div align="center">
  <h1>🌱 Breathe ESG — Data Ingestion Pipeline</h1>
  <p><b>Multi-tenant ESG data ingestion and normalization prototype</b></p>
  
  <a href="https://breathe-esg-data-ingestion.vercel.app"><b>Frontend Live Demo</b></a> • 
  <a href="https://breathe-esg-api-qxqm.onrender.com/api/sources/"><b>Backend API Demo</b></a>

  <br><br>

  ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
  ![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
  ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
  ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
  ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

<br>

> **The Problem:** ESG analysts spend hours wrestling with fragmented client data—SAP procurement logs, PG&E utility scrapes, and Concur travel exports. 
> 
> **The Solution:** A unified ingestion pipeline that ingests disparate formats, extracts the carbon-relevant variables, standardizes the metrics, and presents them in a clean, auditable review dashboard.

---

## 🏗 Engineering Philosophy & Deliverables

To evaluate this assignment, please review the specific architectural markdown documents included in this repository. They detail the "why" behind the code:

* 🗄️ [**MODEL.md**](MODEL.md) — Explains the normalized database schema, multi-tenancy design, and the critical decision to store immutable `raw_data` JSON for ultimate audit traceability.
* ⚖️ [**TRADEOFFS.md**](TRADEOFFS.md) — Honest engineering trade-offs regarding why certain features (like async workers, RBAC, and live emission engines) were intentionally scoped out to prioritize a robust ingestion core.
* 🤔 [**DECISIONS.md**](DECISIONS.md) — How system ambiguities (like parsing different regional date formats `DD.MM.YYYY` vs `MM/DD/YYYY`) were handled.
* 🔍 [**SOURCES.md**](SOURCES.md) — Research on SAP, Utility, and Corporate Travel data structures.

---

## ✨ Core Features

* **Source-Specific Normalization:** Upload a raw CSV; the backend dynamically routes it through a parser based on the `DataSource` (SAP, Utility, or Travel).
* **Audit-First Design:** Analysts can trace any normalized row back to its exact `source_row_number` and inspect the original JSON payload.
* **Idempotency Ready:** Every row generates a deterministic SHA-256 `deduplication_key` to prevent double-counting carbon emissions.
* **Graceful Failure Handling:** Malformed rows aren't dropped; they are flagged with `validation_errors` and set to `PENDING_REVIEW` so analysts can manually intervene.

---

## 🚀 Quick Start (Local Development)

### 1. Backend Setup (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python seed.py          # Seeds the DB with a default Tenant and 3 Data Sources
python manage.py runserver 
```
*The API will run on `http://127.0.0.1:8000`*

### 2. Frontend Setup (React/Vite)
Open a new terminal tab:
```bash
cd frontend
npm install
npm run dev
```
*The dashboard will run on `http://localhost:5173`*

---

## 🧪 How to Test the App

1. Open the UI.
2. Select a **Data Source** from the dropdown (e.g., *SAP ERP Procurement*).
3. Click to upload a file and select the corresponding CSV from the `samples/` directory (e.g., `samples/sap_sample.csv`).
4. Watch the table automatically populate with parsed, standardized data assigned to correct Scopes (Scope 1, 2, 3).
5. Simulate the analyst workflow by clicking **Approve** or **Reject** on `PENDING_REVIEW` rows.

---

## 🗺️ Production Roadmap (Future Improvements)

If this prototype were scaled to production, the next immediate phases would be:
- **Async Processing:** Offload CSV parsing to background workers (Celery/SQS) to prevent HTTP timeouts on multi-megabyte uploads.
- **Dynamic Emission Engine:** Connect the normalized `ActivityData` volumes to a live factor database (e.g., EPA, DEFRA) to compute actual `kgCO2e`.
- **Advanced Observability:** Pipe parser exceptions and ingestion latency metrics into Datadog/Prometheus.
- **Role-Based Access Control:** Implement JWT-based auth separating Data Providers (uploaders) from Analysts (reviewers).
