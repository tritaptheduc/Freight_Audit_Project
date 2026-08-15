CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_mart_weight_discrepancy` AS
SELECT 
  Invoice_Number,
  BOL_Number,
  Carrier,
  Container_Type,
  WMS_Measured_Weight_KG,
  Billed_Weight_KG,
  Weight_Discrepancy_KG,
  Weight_Discrepancy_Pct,
  CASE 
    WHEN Weight_Discrepancy_Pct > 10 THEN 'Overbilled Weight (>10%)'
    WHEN Weight_Discrepancy_Pct > 0 THEN 'Overbilled Weight (<10%)'
    ELSE 'Correct Billed Weight'
  END AS Audit_Weight_Status
FROM `freight-audit-project.freight_audit_db_2.v_base_freight_audit`
WHERE Is_Duplicate_Invoice = FALSE;