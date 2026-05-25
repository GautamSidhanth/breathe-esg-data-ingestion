# Tradeoffs

Here are three things I deliberately chose **not** to build in this prototype and why:

### 1. Complex File Parsing (e.g., PDF Scraping or IDoc parsing)
**What I didn't build:** Direct ingestion of PDF utility bills or SAP IDoc XML structures.
**Why:** The assignment emphasizes a "sharp data model and honest tradeoffs," not spending 3 days building a brittle Regex/OCR parser for PDFs. I chose CSV representations as the ingestion layer. In a real-world scenario, you might build a microservice (e.g., using AWS Textract) to convert PDFs to JSON/CSV before hitting this pipeline. For the prototype, standardizing on CSV uploads allows me to focus on the core value proposition: normalization, review, and audit workflows, rather than fighting edge-case parser logic.

### 2. Live Emission Factor Computation Engine
**What I didn't build:** A real-time calculation engine that matches normalized activity data against dynamic emission factor databases (e.g., EPA, DEFRA, Ecoinvent).
**Why:** The prompt explicitly stated, "The hard part of our job isn't computing carbon, it's that every client's data lives somewhere different..." Therefore, I mocked the emission calculation step or assumed normalized volume is sufficient for the analyst's approval. Building a full calculation engine with region-specific factors and unit conversions (e.g., converting liters of diesel to kgCO2e based on the specific fuel blend) is highly complex and distracts from the core requirement: data ingestion and analyst review.

### 3. Role-Based Access Control (RBAC) and Granular Auth
**What I didn't build:** A fully fleshed-out authentication system with multi-tier roles (Data Provider, Analyst, Auditor, Admin).
**Why:** While I designed the data model to handle multi-tenancy (via a `Tenant` model), I did not build the UI/API layers for authentication and role management (e.g., JWTs with scoped permissions). The time limit is best spent demonstrating the workflow (Ingest -> Normalize -> Review -> Approve). In a production app, I would integrate Auth0 or Clerk. For this prototype, I simulate an "Analyst" view without a complex login wall to ensure the core workflow is immediately accessible for evaluation.

### 4. Idempotency / Duplicate Protection
**What I didn't build:** Row-level deduplication blocking in the ingestion pipeline.
**Why:** While I added a `deduplication_key` field to the database to show how it should be done, I did not build the logic to automatically block or overwrite duplicate rows if the same CSV is uploaded twice. In production, I would add checksum/hash-based duplicate detection on uploads and row-level deduplication rules to prevent double-counting emissions.

### 5. Async Processing
**What I didn't build:** Background task queues for large file uploads.
**Why:** The prototype ingests CSVs synchronously during the HTTP request. In production, ingestion and normalization would run asynchronously through a job queue (Celery/RQ/SQS workers) to support large multi-megabyte uploads and retry handling without blocking the client.

### 6. Comprehensive Observability
**What I didn't build:** Detailed telemetry and monitoring around ingestion failures.
**Why:** I return standard HTTP status codes and attach JSON errors to failed rows, but in a real enterprise system, I would also add ingestion metrics and monitoring (failed rows, parser errors, processing latency via Datadog or Prometheus) for operational visibility.
