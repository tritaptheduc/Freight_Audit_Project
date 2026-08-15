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
