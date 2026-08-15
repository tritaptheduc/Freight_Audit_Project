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
| **Integrity** | `M_Total_Duplicate_Amount_USD` | $\sum \text{Billed Total USD} \quad \text{where } \text{Is Duplicate Invoice} = \text{TRUE}$ | $\$0$ (Zero duplicates paid) |
| **Integrity** | `M_Claimable_SLA_Amount_USD` | $\sum \text{Billed Total USD} \quad \text{where } \text{Root Cause} = \text{'CARRIER ERROR'} \text{ and } \text{SLA Delay Days} > 0$ | 100% Claim recovery |
| **Weight Audit** | `M_Overbilled_Weight_KG` | $\sum (\text{Billed Weight KG} - \text{WMS Measured Weight KG})$ | $0 \text{ KG}$ discrepancy |
| **Weight Audit** | `M_Overbilled_Weight_Pct` | $\frac{\text{M Overbilled Weight KG}}{\text{M Total WMS Weight KG}} \times 100$ | $< 1\%$ tolerance |
| **Storage Audit** | `M_Invalid_Storage_Fees_USD` | $\sum (\text{Demurrage} + \text{Detention}) \quad \text{assessed within Free Time limits}$ | $\$0$ invalid penalties |
| **Utilization** | `M_Avg_Capacity_Utilization_Pct` | $\text{AVERAGE}\left(\frac{\text{WMS Weight}}{\text{Max Payload Capacity}}\right) \times 100$ | $\ge 85\%$ payload rate |

### 🔍 3. ANALYZE Phase
The system partitions analytics into five specialized business dashboards formatted for standard 4:3 canvas layouts.

**1. Invoice Integrity & SLA Claim Audit**
- **Business Purpose**: Detect duplicate invoice submissions and identify carrier-caused delivery SLA violations for claim generation.
- **Key Visuals**: KPI Cards (Duplicate Count, Duplicate USD, Claimable SLA Amount), Column Chart of Billing by Audit Flag, SLA Delay Root Cause Donut Chart, Detailed BOL Dispute Table.
- **Dashboard Preview**:

![Invoice Integrity & SLA Claim Audit](<assets/images/Invoice Integrity & SLA Claim Audit.png>)

**2. Weight Discrepancy & Billing Audit**
- **Business Purpose**: Benchmark carrier billed weight against WMS scale measurements to uncover over-billing.
- **Key Visuals**: Weight Comparison KPIs (Billed vs. WMS), Top Over-billing Carriers Bar Chart, Discrepancy % by Container Type Scatter Plot, Line-item Weight Audit Table.
- **Dashboard Preview**:

![Carrier & Route Detention Performance](<assets/images/Weight Discrepancy & Billing Audit.png>)

**3. Demurrage & Detention Charge Audit**
- **Business Purpose**: Audit carrier demurrage and detention assessments against contractual free-time allowances.
- **Key Visuals**: Storage Penalty KPIs, Actual Port Stay vs. Contractual Free Days Clustered Column Chart, Invalid Penalty Status Distribution, Storage Fee Detail Grid.
- **Dashboard Preview**:

![Carrier & Route Detention Performance](<assets/images/Demurrage & Detention Charge Audit.png>)

**4. Container Weight Utilization Efficiency**
- **Business Purpose**: Identify underutilized container capacity ($<60\%$ payload) to reduce total shipment volume requirements.
- **Key Visuals**: Average Load Factor Gauge Chart, Utilization Breakdown by Container Type (20DC vs 40HC), Underutilized Shipment Ratio Cards, Container Payload Detail Table.
- **Dashboard Preview**:

![Carrier & Route Detention Performance](<assets/images/Container Weight Utilization Efficiency.png>)

**5. Carrier & Route Detention Performance**
- **Business Purpose**: Measure container turnaround times and total detention costs across carriers and shipping corridors (Trade Lanes).
- **Key Visuals**: Trade Lane Heatmap Matrix (POL_Origin $\times$ POD_Destination), Average Detention Days by Carrier, Total Shipment Volume Cards, Route Level Performance Breakdown.
- **Dashboard Preview**:

![Carrier & Route Detention Performance](<assets/images/Carrier & Route Detention Performance.png>)

### 🚀 4. IMPROVE Phase
Based on data mart analysis, the following operational improvements are implemented:

```plaintext
                  ┌──────────────────────────────────────────────┐
                  │          ACTIONABLE IMPROVEMENTS             │
                  └──────────────────────┬───────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│ Automated Claim │             │ Contract Term   │             │ Load Factor     │
│ Generation      │             │ Negotiations    │             │ Consolidation   │
├─────────────────┤             ├─────────────────┤             ├─────────────────┤
│ Export detail   │             │ Leverage carrier│             │ Consolidate LCL │
│ dispute logs    │             │ scorecards using│             │ shipments on    │
│ directly into   │             │ detention & SLA │             │ routes with     │
│ Carrier Claim   │             │ data to extend  │             │ load factors    │
│ templates.      │             │ Free Time.      │             │ under 60%.      │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

### 🛡️ 5. CONTROL Phase
To ensure long-term data integrity and prevent regression, control mechanisms are applied at both warehouse and BI layers.

**Data Warehouse Controls (Google BigQuery)**
- **Ingestion Deduplication Logic**: Uses window functions (`ROW_NUMBER() OVER(PARTITION BY BOL_Number, Billed_Total_Amount`)) in `v_stg_invoices` to flag duplicates upon ingestion.
- **Partition Filter Optimization**: Explicitly handles ingestion-time partitioning filters (_PARTITIONDATE) across staging views to guarantee low-latency query performance and maintain schema stability.

**Power BI Data Model Controls**
- **Star Schema Design**: All 5 data marts connect to a centralized, calculated calendar table (dim_date_table), enforcing date aggregation consistency across all visuals.
- **Isolated DAX Measures Layer**: DAX measures are defined against model views rather than raw tables, enabling dynamic filtering based on user role and date context.

## 🛠️ Repository Structure & Quick Start
### Repository Layout
```plaintext
Freight_Audit_Project/
├── assets/
│   ├── images/                          
│   │   ├── Carrier & Route Detention Performance.png
│   │   ├── Container Weight Utilization Efficiency.png
│   │   ├── Demurrage & Detention Charge Audit.png
│   │   ├── Invoice Integrity & SLA Claim Audit.png
│   │   └── Weight Discrepancy & Billing Audit.png
│   └── architecture_diagram.png        
├── data/
│   ├── raw/                         
│   │   ├── dim_contract_rates.csv
│   │   ├── dim_exchange_rates.csv
│   │   ├── fact_shipments_bol.csv
│   │   └── raw_carrier_invoices.csv
│   └── data-dictionary/
│       └── data-dictionary.xlsx
├── docs/
│   ├── Executive_Summary.md            
│   └── Business_Requirements.md   
├── reports/
│   ├── freight-audit-2-2.pbix
│   └── freight-audit-2-2.pbit 
├── src/
│   ├── dax/
│   │   ├── dim_date_table.dax
│   │   └── measures.dax
│   ├── json/
│   │   └── Logistics_Freight_Audit_Theme.json
│   ├── python/
│   │   └── generate_mock_data.py
│   └── sql/
│       ├── 01_stg/
│       │   └── v_stg_invoices.sql
│       ├── 02_core/
│       │   └── v_base_freight_audit.sql
│       └── 03_marts/
│           ├── v_mart_booking_no_show_detention.sql
│           ├── v_mart_demurrage_detention.sql
│           ├── v_mart_sla_violation_audit.sql
│           ├── v_mart_underutilization.sql
│           └── v_mart_weight_discrepancy.sql
├── .gitignore
├── LICENSE
└── README.md
```

### Installation & Deployment Steps
**1. Clone the Repository:**
```bash
git clone https://github.com/tritaptheduc/Freight_Audit_Project.git
cd Freight_Audit_Project
```

**2. Load Raw Data to Google BigQuery:**
- Create dataset `freight_audit_db_2` inside project `freight-audit-project`.
- Upload the 4 CSV files from the `data/` directory into BigQuery.

**3. Execute SQL Transformations:**

Run the SQL scripts in `src/sql/` in the following sequence:
- `v_stg_invoices.sql`
- `v_base_freight_audit.sql`
- `v_mart_*.sql` (all analytical data marts)

**4. Launch Power BI Dashboard:**
- Open `reports/freight-audit-2-2.pbit` in Power BI Desktop.
- Provide your BigQuery GCP Project ID and Dataset ID when prompted.

Apply the custom theme from src/json/Logistics_Freight_Audit_Theme.json if required.
