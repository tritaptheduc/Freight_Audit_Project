# BUSINESS REQUIREMENTS DOCUMENT (BRD)

## Project Title: Automated Freight Audit & Logistics Cost Optimization System
**Document Version:** 1.0  
**Target Audience:** Supply Chain Leadership, Logistics Managers, Data Engineering, & Business Intelligence Teams

---

## 1. Business Objectives & Scope
The objective of this project is to build an end-to-end analytical framework to audit freight invoices, evaluate carrier SLA compliance, detect billing anomalies, and optimize logistics payload utilization.

### In-Scope:
* Ingestion of raw carrier invoices, shipment execution logs (WMS/BOL), contract rates, and exchange rate tables.
* Data transformation, deduplication, currency standardization (USD), and multi-layer data modeling in Google BigQuery.
* Interactive 4:3 canvas Power BI executive dashboards covering 5 core business analytical dimensions.
* DAX measures for dynamic KPI tracking, discrepancy auditing, and financial recovery estimation.

### Out-of-Scope:
* Real-time GPS tracking of active transit vessels.
* Direct API integration with carrier ERP systems for automatic payment execution.

---

## 2. Stakeholder Requirements & User Stories

### User Story 1: Freight Auditor (Operational Level)
* *As a Freight Auditor,* I want to automatically identify duplicate invoices and weight discrepancies *so that* I can halt invalid payments before disbursements are made.

### User Story 2: Logistics Manager (Tactical Level)
* *As a Logistics Manager,* I want to track carrier SLA violations and storage penalties *so that* I can file claim requests backed by timestamped evidence.

### User Story 3: VP of Supply Chain (Strategic Level)
* *As an Executive,* I want clear visual visibility into container payload efficiency and route-level cost performance *so that* I can optimize shipping contracts and operational budgets.

---

## 3. Detailed Analytical Dimensions (5 Analytical Focus Areas)

### Requirement 1: Invoice Integrity & SLA Claim Audit
* **Business Purpose:** Eliminate duplicate billing and claim reimbursements for carrier-caused SLA delivery delays.
* **Key Metrics:** Total Invoices, Duplicate Invoice Count, Duplicate Billed USD, SLA Claimable USD.
* **Required Data Attributes:** `Invoice_Number`, `BOL_Number`, `SLA_Delay_Days`, `Root_Cause_Delay`, `Is_Duplicate_Invoice`, `Invoice_Audit_Flag`.

### Requirement 2: Weight Discrepancy & Billing Audit
* **Business Purpose:** Prevent carriers from overcharging based on inflated weights compared to WMS measurements.
* **Key Metrics:** Total Billed Weight (KG), Total WMS Weight (KG), Overbilled Weight (KG), Overbilled Percentage (%).
* **Required Data Attributes:** `Container_Type`, `WMS_Measured_Weight_KG`, `Billed_Weight_KG`, `Weight_Discrepancy_KG`, `Audit_Weight_Status`.

### Requirement 3: Demurrage & Detention Charge Audit
* **Business Purpose:** Audit validity of storage penalties assessed during contractual Free Time windows.
* **Key Metrics:** Total Demurrage USD, Total Detention USD, Invalid Storage Fees USD, Invalid Penalty Count.
* **Required Data Attributes:** `Actual_Port_Stay_Days`, `Free_Demurrage_Days`, `Actual_Detention_Days`, `Free_Detention_Days`, `Audit_Storage_Status`.

### Requirement 4: Container Weight Utilization Efficiency
* **Business Purpose:** Measure load factor performance to eliminate wasted space in container shipments.
* **Key Metrics:** Avg Capacity Utilization (%), Underutilized Shipment Count, Underutilized Ratio (%).
* **Required Data Attributes:** `Container_Type`, `WMS_Measured_Weight_KG`, `Max_Payload_Capacity_KG`, `Capacity_Utilization_Pct`, `Utilization_Category`.

### Requirement 5: Carrier & Route Detention Performance
* **Business Purpose:** Monitor turnaround times and turnaround penalty costs by Carrier and Trade Lane (POL -> POD).
* **Key Metrics:** Total Shipments, Weighted Avg Detention Days, Total Detention Cost USD.
* **Required Data Attributes:** `Carrier`, `POL_Origin`, `POD_Destination`, `Total_Shipments`, `Avg_Detention_Days`, `Total_Detention_Cost_USD`.

---

## 4. Non-Functional & Visual Layout Requirements
* **Canvas Format:** Standard 4:3 Ratio Aspect (`1024 x 768 px`).
* **Layout Scaffolding:** Fixed Top Header (Title), Left Sidebar (Global Slicers & Navigation), Top KPI Cards, Middle Analytics Visuals, Bottom Detail Grid.
* **Data Security & Governance:** Row-level data validation via staging views in Google BigQuery; no hardcoded credentials.