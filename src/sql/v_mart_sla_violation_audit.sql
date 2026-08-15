CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_mart_sla_violation_audit` AS
SELECT 
  Invoice_Number,
  BOL_Number,
  Carrier,
  SLA_Delay_Days,
  Root_Cause_Delay,
  Is_Duplicate_Invoice,
  Billed_Total_USD,
  CASE 
    WHEN Is_Duplicate_Invoice = TRUE THEN 'Error: Duplicate Invoice'
    WHEN SLA_Delay_Days > 0 AND Root_Cause_Delay = 'CARRIER_ERROR' THEN 'Error: Carrier SLA Violation'
    ELSE 'Normal'
  END AS Invoice_Audit_Flag
FROM `freight-audit-project.freight_audit_db_2.v_base_freight_audit`;