CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_mart_demurrage_detention` AS
SELECT 
  Invoice_Number,
  BOL_Number,
  Carrier,
  Actual_Port_Stay_Days,
  Free_Demurrage_Days,
  GREATEST(0, Actual_Port_Stay_Days - Free_Demurrage_Days) AS Expected_Excess_Demurrage_Days,
  Billed_Demurrage_USD,
  
  Actual_Detention_Days,
  Free_Detention_Days,
  GREATEST(0, Actual_Detention_Days - Free_Detention_Days) AS Expected_Excess_Detention_Days,
  Billed_Detention_USD,

  CASE 
    WHEN Actual_Port_Stay_Days <= Free_Demurrage_Days AND Billed_Demurrage_USD > 0 
      THEN 'Error: Incorrect Detention assessment during Free Time'
    WHEN Actual_Detention_Days <= Free_Detention_Days AND Billed_Detention_USD > 0 
      THEN 'Error: Incorrect Demurrage assessment during Free Time'
    ELSE 'Normal'
  END AS Audit_Storage_Status
FROM `freight-audit-project.freight_audit_db_2.v_base_freight_audit`
WHERE Is_Duplicate_Invoice = FALSE;