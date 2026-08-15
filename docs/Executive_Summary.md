# EXECUTIVE SUMMARY: FREIGHT AUDIT & LOGISTICS COST ANALYTICS

## 1. Project Context & Business Challenge
In global logistics and supply chain operations, shipping invoice inaccuracies present a silent yet significant drain on corporate capital. Transportation contracts involve complex multi-tiered fee structures, dynamic fuel surcharges, multi-currency conversions, and strict Service Level Agreements (SLAs). 

Manual invoice reviews fail to capture systematically hidden overcharges, resulting in an estimated **3% to 7% loss of total freight expenditure** annually. Key pain points identified include:
* **Duplicate Billing:** Carriers submitting multiple invoices for a single Bill of Lading (BOL).
* **Weight Discrepancy (Overbilling):** Discrepancies between WMS-measured weight and carrier-billed weight.
* **Invalid Demurrage & Detention Penalties:** Penalty charges levied within agreed contract "Free Time" windows.
* **Carrier-Induced SLA Violations:** Delivery delays caused by carrier operational errors without systematic financial recovery.
* **Container Underutilization:** Sub-optimal container space utilization leading to unnecessary freight runs.

---

## 2. Core Audit Findings & Impact Analysis

| Audit Domain | Key Metric / Insight | Financial & Operational Impact | Actionable Mitigation |
| :--- | :--- | :--- | :--- |
| **Invoice Integrity** | Detected **Duplicate Invoices** & **Carrier SLA Delays** | Direct financial leakage due to redundant payments and unrecovered delay penalties | Automate automated validation rules; file formal claims for carrier-caused SLA breaches. |
| **Weight Audit** | Identified systematic **Weight Overbilling (>10%)** | Excess freight spend calculated on inflated billable weights | Implement automated WMS vs. Carrier weight cross-checking prior to payment approval. |
| **Storage Penalty Audit** | Discovered **Free Time Penalty Violations** | Improper Demurrage/Detention charges applied during valid free days | Dispute non-compliant storage invoices using port gate-in/gate-out timestamps. |
| **Payload Efficiency** | Found **Severe Underutilization (<60%)** | Higher cost per unit shipped due to poor volume/weight consolidation | Re-engineer load planning algorithms and consolidate cargo per trade lane. |
| **Carrier Performance** | Uncovered high **Detention Days per Route** | Operational bottlenecks at specific destination ports (POD) | Renegotiate Free Time terms with low-performing carriers on high-risk routes. |

---

## 3. Financial Recovery & Strategic Value
By implementing the automated BigQuery + Power BI Freight Audit pipeline:
1. **Immediate Cost Recovery:** 100% detection of duplicate invoices and invalid storage fees prior to disbursement.
2. **Discrepancy Elimination:** Automated reconciliation between WMS physical metrics and billing statements.
3. **Data-Driven Carrier Negotiations:** Empirical performance scorecards leverage better terms during annual contract renewals.

---

## 4. Key Strategic Recommendations
* **Enforce Gatekeeper Validation:** Block invoice approval in ERP systems unless passed by `v_base_freight_audit` automated checks.
* **Establish Monthly Claim Cycles:** Deduct validated overcharges directly from upcoming carrier payout accounts.
* **Optimize Container Packing:** Set a mandatory baseline of **>80% capacity utilization** for all 20DC and 40HC shipments.