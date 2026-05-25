# Sources Research and Assumptions

## 1. SAP, Fuel and Procurement Data

### Format Choice: Flat File CSV Export (from SAP ALV Grid)
**Research & Justification**: 
SAP ERP and SAP S/4HANA expose data in various ways (IDocs, BAPIs, OData). However, many enterprise companies still rely on simple end-user exports (like ALV Grid exports) for sustainability teams, especially for legacy systems without IT-managed integrations. 
I chose a CSV flat-file export because it represents a common "low maturity" data source that analysts deal with daily. 

**What I Learned**:
- Typical SAP export columns use technical German acronyms: `BUKRS` (Company Code), `WERKS` (Plant), `MATNR` (Material Number), `MENGE` (Quantity), `MEINS` (Base Unit of Measure), and `AEDAT` (Changed On/Date).
- SAP units (`MEINS`) are often internal (e.g., `L` for Liters, `KG` for Kilograms, `ST` for Pieces), which requires normalization to standard GHG units.
- Material Numbers (`MATNR`) require lookup tables to know if a material is "Diesel Fuel" or "Office Paper."

**Sample Data Profile**:
- Columns: `Company_Code`, `Plant`, `Material`, `Quantity`, `Unit`, `Date`, `Total_Cost`
- Sample Row: `1000, 1010, Diesel, 500, L, 2026-05-15, 750.00`
- **Breakage in real deployment**: Missing lookup tables for `Material` codes. Changes to SAP layout variants could reorder columns or rename headers, breaking fixed-index or strict-header parsers.

## 2. Utility Data, Electricity

### Format Choice: CSV Portal Export
**Research & Justification**:
While Green Button XML is the standard for utilities, many commercial property facilities managers log into a utility portal (e.g., PG&E) and download a billing CSV summary.

**What I Learned**:
- Billing cycles do not align with calendar months (e.g., Feb 12 - Mar 14).
- Data often contains both "Demand" (kW) and "Usage" (kWh), and carbon footprints typically depend on Usage.
- A single export often aggregates multiple meters.

**Sample Data Profile**:
- Columns: `Account_Number`, `Meter_ID`, `Start_Date`, `End_Date`, `Usage`, `Usage_Unit`, `Cost`
- Sample Row: `ACC-991, M-1029, 2026-04-12, 2026-05-11, 45000, kWh, 4100.50`
- **Breakage in real deployment**: Overlapping billing periods across exports, missing meter-to-facility mapping (making it impossible to assign electricity to a specific Scope 2 location), or estimated reads being later corrected in subsequent bills.

## 3. Corporate Travel (Navan/TripActions)

### Format Choice: API/Report Export (CSV)
**Research & Justification**:
Platforms like Navan (TripActions) or Concur provide robust reporting. Since analysts often export these reports manually before integration is built, I chose a CSV format mirroring a typical travel segment report.

**What I Learned**:
- Travel data is highly segmented. A single trip might have 4 flight segments, each with different origin/destination airport codes.
- Distance is sometimes provided, but often only IATA codes are available (requiring a Great Circle distance calculator for GHG protocols).
- Cabin class (Economy, Business) is crucial because emission factors vary significantly by seating density.

**Sample Data Profile**:
- Columns: `Employee_ID`, `Booking_ID`, `Segment_Type`, `Origin`, `Destination`, `Cabin_Class`, `Distance_km`, `Date`
- Sample Row: `EMP-001, BKG-881, Flight, SFO, JFK, Economy, 4156, 2026-05-10`
- **Breakage in real deployment**: Invalid IATA codes, missing cabin class for train/ground transport, or canceled bookings appearing in the export without being filtered out (causing over-reporting of emissions).
