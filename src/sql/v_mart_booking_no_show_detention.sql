CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_mart_booking_no_show_detention` AS
SELECT 
  Invoice_Number,
  Carrier,
  POL_Origin,
  POD_Destination,
  COUNT(DISTINCT BOL_Number) AS Total_Shipments,
  ROUND(AVG(Actual_Detention_Days), 1) AS Avg_Detention_Days,
  ROUND(SUM(Billed_Detention_USD), 2) AS Total_Detention_Cost_USD
FROM `freight-audit-project.freight_audit_db_2.v_base_freight_audit`
WHERE Is_Duplicate_Invoice = FALSE
GROUP BY Invoice_Number, Carrier, POL_Origin, POD_Destination;