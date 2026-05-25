# Data Model

The core of the application revolves around standardizing disparate data streams into a unified, auditable `ActivityData` table, while preserving the original raw payload for traceability and debugging.

## Core Entities

### 1. Tenant (Multi-Tenancy)
Represents a client company. All data must be isolated by Tenant.
- `id`: UUID (Primary Key)
- `name`: String
- `created_at`: DateTime

### 2. DataSource
Represents a specific integration or manual upload origin (e.g., "SAP Procurement CSV", "PG&E Utility Portal").
- `id`: UUID
- `tenant_id`: UUID (FK)
- `name`: String
- `source_type`: Enum (SAP, UTILITY, TRAVEL)
- `config`: JSON (Stores connection details or mapping rules)

### 3. DataUpload (Source-of-Truth Tracking)
Represents a single ingestion event (a file upload or API pull). Crucial for auditability to know *when* and *how* data arrived.
- `id`: UUID
- `data_source_id`: UUID (FK)
- `uploaded_at`: DateTime
- `status`: Enum (PENDING, PROCESSED, FAILED)
- `raw_file_path`: String (Reference to S3/Blob storage of the original file)
- `uploaded_by`: String (User ID or API key identifier)

### 4. ActivityData (The Normalized Core)
This is where the disparate shapes become uniform. It holds normalized values while keeping a JSON blob of the original row.
- `id`: UUID
- `tenant_id`: UUID (FK)
- `data_upload_id`: UUID (FK) - Traceability to the exact file/event
- `scope`: Enum (SCOPE_1, SCOPE_2, SCOPE_3) - Categorization
- `activity_type`: String (e.g., "Fuel Combustion", "Purchased Electricity", "Business Travel")
- `date_start`: Date
- `date_end`: Date
- `normalized_quantity`: Float - The computed volume in a standard unit
- `normalized_unit`: String (e.g., "kWh", "L", "km")
- `source_row_number`: Integer - Traceability back to the original row in the CSV file
- `deduplication_key`: String - A hash (e.g. SHA-256) of the source ID and raw JSON string to prevent double-counting
- `raw_data`: JSON - The exact JSON representation of the source row (e.g., `{"BUKRS": "1000", "MATNR": "Diesel", ...}`). This is the "source-of-truth" backup.
- `status`: Enum (PENDING_REVIEW, APPROVED, REJECTED)
- `validation_errors`: JSON - Populated during ingestion if a row looks suspicious (e.g., missing dates, unknown unit).

### 5. AuditLog
Tracks every state change to an `ActivityData` record.
- `id`: UUID
- `activity_data_id`: UUID (FK)
- `action`: Enum (CREATED, EDITED, APPROVED, REJECTED)
- `changed_by`: String (Analyst user)
- `timestamp`: DateTime
- `changes`: JSON - (e.g., `{"status": {"old": "PENDING_REVIEW", "new": "APPROVED"}}`)

## Why this model?
1. **Multi-tenancy:** Enforced at the `Tenant` level.
2. **Audit Trail & Source of Truth:** We never mutate `raw_data`. Any changes made by an analyst are logged in `AuditLog`, and the current state is stored in standard columns. We can always trace back to `DataUpload` to see the original file.
3. **Flexibility:** `raw_data` (JSON) handles the fact that SAP has different columns than Concur. The normalization layer's job is simply to extract `date_start`, `date_end`, `quantity`, and `unit` and map them to the strict columns.
