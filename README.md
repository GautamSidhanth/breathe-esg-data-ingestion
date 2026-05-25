# Breathe ESG - Data Ingestion Prototype

This repository contains the solution for the Breathe ESG Tech Intern Assignment.

## Live Demo
- **Frontend App**: [https://breathe-esg-data-ingestion.vercel.app](https://breathe-esg-data-ingestion.vercel.app)
- **Backend API**: [https://breathe-esg-api-qxqm.onrender.com/api/sources/](https://breathe-esg-api-qxqm.onrender.com/api/sources/)

## Architecture
- **Backend**: Django REST Framework (SQLite for prototype simplicity)
- **Frontend**: React (Vite, TypeScript, Vanilla CSS)

## Core Deliverables Included
1. **MODEL.md**: Explanation of the normalized database schema, multi-tenancy, and audit traceability.
2. **DECISIONS.md**: Justifications for ambiguous choices (e.g., date formats, ingestion mechanisms).
3. **TRADEOFFS.md**: What was intentionally excluded (complex parsing, RBAC, live emissions calculations).
4. **SOURCES.md**: Research on SAP, Utility, and Travel data, and why the specific formats were chosen.

## Running Locally

### Backend (Django)
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python manage.py makemigrations api`
4. `python manage.py migrate`
5. `python seed.py` (Seeds the database with default Tenant and 3 Data Sources)
6. `python manage.py runserver` (Runs on port 8000)

### Frontend (React)
1. `cd frontend`
2. `npm install`
3. `npm run dev` (Runs on port 5173)

## Deployment Notes

The project is deployment-ready and can be hosted using Render (backend) and Vercel (frontend). Example deployment steps are provided below.

### Option 1: Render (Recommended for Backend)
1. Create a GitHub repository and push this code.
2. Go to [Render](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repo.
4. Set the **Root Directory** to `backend`.
5. Set the **Build Command** to: `pip install -r requirements.txt && python manage.py migrate && python seed.py`
6. Set the **Start Command** to: `gunicorn backend.wsgi:application`
7. Copy the backend deployment URL.

### Option 2: Vercel (Recommended for Frontend)
1. Go to [Vercel](https://vercel.com) and import the same GitHub repository.
2. Set the **Root Directory** to `frontend`.
3. Add an Environment Variable: `VITE_API_URL` and set it to your deployed Render URL (e.g., `https://my-backend.onrender.com/api`).
4. Click Deploy.

### Post-Deployment
1. Make sure to share the GitHub repo with `saurav@breatheesg.com`, `rahul@breatheesg.com`, and `shivang@breatheesg.com`.
2. Reply to the email with the deployed Vercel URL and the repo link.

## Using the App
1. Open the deployed frontend.
2. Under **Ingest Data**, select a data source (e.g., "SAP ERP").
3. Upload a sample CSV file that matches the source format (you can create simple CSVs based on the `SOURCES.md` definitions).
4. The data will normalize and appear in the **Review & Approve Data** table.
5. Click **Approve** or **Reject** to simulate the analyst workflow.

## Future Improvements
- Automated schema detection for unknown CSV formats
- Background ingestion workers (e.g., Celery/SQS) for async processing
- Emission factor engine integration
- PDF/OCR ingestion pipeline
- Role-based access control
- Data lineage dashboard
- Enforcing duplicate upload detection using the `deduplication_key`
