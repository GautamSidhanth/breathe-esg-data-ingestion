# Decisions & Ambiguities

## 1. What subset of each source did I handle?
- **SAP**: I handled a subset of a Material Document export (CSV). I assume the export contains material names, quantities, and units. I ignored multi-currency cost conversions and internal SAP plant routing codes, focusing purely on volume.
- **Utility Data**: I handled a standard portal CSV export for Electricity (kWh). I ignored Demand charges (kW) and peak/off-peak tiering, as GHG emissions are calculated based on total consumption (kWh), not peak demand.
- **Corporate Travel**: I handled flight data with origin/destination and cabin class. I ignored hotel stays and ground transport for this prototype to focus the normalization logic on one complex travel type (flights require distance calculation).

## 2. Ingestion Mechanism
I chose **File Upload (CSV)** for all three sources in this prototype. 
- **Why?** The prompt states data "lives somewhere different, in a different shape... Utility bills as PDFs or portal scrapes." In reality, analysts often fallback to manual CSV uploads when APIs break or are unavailable. Building 3 different OAuth API integrations (Concur, SAP OData, PG&E) would take weeks. A unified CSV ingestion pipeline with source-specific normalizers (parsers) proves the architecture without getting bogged down in OAuth dances.

## 3. How did I handle Date Parsing?
**Ambiguity:** SAP uses `DD.MM.YYYY`, US utilities use `MM/DD/YYYY`, and APIs use ISO8601.
**Decision:** I built simple date parsers in the backend normalizers that attempt to parse based on the known source type. If a date fails to parse, the row is flagged with a `validation_error` and marked as `PENDING_REVIEW` so the analyst can correct it in the UI.

## 4. What would I ask the PM?
If I had access to the PM, I would ask:
1. "Who owns the mapping tables for SAP materials? If SAP exports 'MAT-991', do we maintain the mapping that says it's Diesel, or does the client upload a mapping file?"
2. "For utility bills, if a bill covers Jan 15 to Feb 14, do we split the emissions across the two calendar months pro-rata, or attribute it to the month the bill was issued?"
3. "Are analysts allowed to edit the normalized quantity directly, or do they only approve/reject rows? If they edit, do we need to calculate the difference for the audit log?"
