CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_mart_underutilization` AS
SELECT 
  Invoice_Number,
  BOL_Number,
  Carrier,
  Container_Type,
  WMS_Measured_Weight_KG,
  -- Tải trọng tiêu chuẩn: 20DC (21,700 KG), 40HC (26,500 KG)
  CASE WHEN Container_Type = '20DC' THEN 21700 ELSE 26500 END AS Max_Payload_Capacity_KG,
  WMS_Measured_Weight_KG / (CASE WHEN Container_Type = '20DC' THEN 21700 ELSE 26500 END) AS Capacity_Utilization_Pct,
  CASE 
    WHEN (WMS_Measured_Weight_KG / (CASE WHEN Container_Type = '20DC' THEN 21700 ELSE 26500 END)) < 0.60 
      THEN 'Severe Underutilization (< 60%)'
    ELSE 'Severe Utilization'
  END AS Utilization_Category
FROM `freight-audit-project.freight_audit_db_2.v_base_freight_audit`
WHERE Is_Duplicate_Invoice = FALSE;