# Freight Audit & Logistics Cost Analytics

## 📖 Executive Summary & DMAIC Framework Overview
In global supply chain management, freight invoice inaccuracies—such as duplicate billing, weight overcharges, and unjustified detention fees—account for an estimated **5% to 7% of unnecessary logistics expenditure**.

This repository presents an enterprise-grade **Automated Freight Audit & Analytics System** built using **Google BigQuery and Power BI**. The project adopts the **Six Sigma DMAIC (Define, Measure, Analyze, Improve, Control)** methodology to systematically uncover cost leakage, streamline auditing workflows, and establish continuous data control.

```plaintext
       ┌──────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
       │  DEFINE  │ ──► │ MEASURE │ ──► │ ANALYZE  │ ──► │ IMPROVE  │ ──► │ CONTROL │
       └──────────┘     └─────────┘     └──────────┘     └──────────┘     └─────────┘
        Problem &        Data Pipeline   Audit Marts &   Power BI Dash   Automated
        Objectives       Architecture     Root Cause      Visualizations  Data Rules
```
### 🎯 1. DEFINE Phase
**Problem Statement** <br>
The logistics organization faces financial loss due to unverified carrier invoices. Manual sampling fails to catch duplicate invoices, discrepancies between Warehouse Management System (WMS) weight logs and carrier-billed weights, and improper demurrage/detention penalty assessments during contractual free time.

**Business Objectives** <br>
- Automate 100% Invoice Audit: Eliminate manual sample checks by transforming raw logistics streams into auto-audited data marts.
- Recover Overcharged Capital: Identify invalid billings (duplicate charges, carrier-induced SLA delays, improper storage fees) to submit financial claims.
- Optimize Payload Capacity: Track container load factors to reduce underutilization.

**Target Stakeholders** <br>
- Logistics & Supply Chain Directors: High-level cost transparency, vendor compliance ratings, and total claimable financial recovery.
- Freight Audit & Billing Specialists: Operational granularity down to individual Bill of Lading (BOL) level for invoice dispute processing.

### 📏 2. MEASURE Phase
Data Pipeline Architecture
The solution uses Google BigQuery as a scalable cloud data warehouse to process raw operational logs and contract matrices into structured audit layers.

```plaintext
[Raw Data Ingestion]
  ├── raw_carrier_invoices (Carrier billing streams)
  ├── fact_shipments_bol   (WMS & logistics execution logs)
  ├── dim_contract_rates   (Agreed contract rates & Free Time terms)
  └── dim_exchange_rates   (Currency conversion benchmarks)
         │
         ▼
[BigQuery Staging Layer] -> v_stg_invoices
  └── FX Normalization (to USD) & Multi-attribute Deduplication
         │
         ▼
[BigQuery Core Audit Layer] -> v_base_freight_audit
  └── Relational JOINs across Invoices, BOL execution, and Contracts
         │
         ▼
[BigQuery Data Marts Layer] -> 5 Domain-Specific Views
  ├── v_mart_sla_violation_audit
  ├── v_mart_weight_discrepancy
  ├── v_mart_demurrage_detention
  ├── v_mart_underutilization
  └── v_mart_booking_no_show_detention
         │
         ▼
[Power BI Analytical Presentation Layer]
  └── Star-schema Data Model with custom DAX measures & 4:3 ratio canvases
```
**Core Metrics & Key Performance Indicators (KPIs)**

| Metric Category | Measure Name | Formula / Logic | Business Target |
| :--- | :--- | :--- | :--- |
| **Integrity** | `M_Total_Duplicate_Amount_USD` | $\sum \text{Billed Total USD} \quad \text{where } \text{Is\_Duplicate\_Invoice} = \text{TRUE}$ | $\$0$ (Zero duplicates paid) |
| **Integrity** | `M_Claimable_SLA_Amount_USD` | $\sum \text{Billed Total USD} \quad \text{where } \text{Root\_Cause} = \text{'CARRIER\_ERROR'} \text{ and } \text{SLA\_Delay\_Days} > 0$ | 100% Claim recovery |
| **Weight Audit** | `M_Overbilled_Weight_KG` | $\sum (\text{Billed\_Weight\_KG} - \text{WMS\_Measured\_Weight\_KG})$ | $0 \text{ KG}$ discrepancy |
| **Weight Audit** | `M_Overbilled_Weight_Pct` | $\frac{\text{M\_Overbilled\_Weight\_KG}}{\text{M\_Total\_WMS\_Weight\_KG}} \times 100$ | $< 1\%$ tolerance |
| **Storage Audit** | `M_Invalid_Storage_Fees_USD` | $\sum (\text{Demurrage} + \text{Detention}) \quad \text{assessed within Free Time limits}$ | $\$0$ invalid penalties |
| **Utilization** | `M_Avg_Capacity_Utilization_Pct` | $\text{AVERAGE}\left(\frac{\text{WMS Weight}}{\text{Max Payload Capacity}}\right) \times 100$ | $\ge 85\%$ payload rate |
