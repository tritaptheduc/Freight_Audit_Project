CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_stg_invoices` AS
WITH invoice_dedup AS (
  SELECT 
    *,
    -- Chuyển Billed_Total_Amount sang NUMERIC trong PARTITION BY để tránh lỗi FLOAT64
    ROW_NUMBER() OVER(
      PARTITION BY BOL_Number, SAFE_CAST(Billed_Total_Amount AS NUMERIC) 
      ORDER BY Invoice_Date ASC
    ) as dup_rank
  FROM `freight-audit-project.freight_audit_db_2.raw_carrier_invoices`
)
SELECT 
  inv.Invoice_Number,
  inv.BOL_Number,
  inv.Carrier,
  inv.Invoice_Date,
  inv.Invoice_Currency,
  inv.Billed_Weight_KG,
  inv.Billed_Base_Rate,
  inv.Billed_Fuel_Surcharge,
  inv.Billed_Demurrage_Amount,
  inv.Billed_Detention_Amount,
  inv.Billed_Total_Amount,
  IF(inv.dup_rank > 1 OR inv.Invoice_Number LIKE '%-DUP', TRUE, FALSE) AS Is_Duplicate_Invoice,
  -- Quy đổi tỷ giá về USD
  COALESCE(fx.Exchange_Rate, 1.0) AS FX_To_USD_Rate,
  ROUND(inv.Billed_Total_Amount * COALESCE(fx.Exchange_Rate, 1.0), 2) AS Billed_Total_USD
FROM invoice_dedup inv
LEFT JOIN `freight-audit-project.freight_audit_db_2.dim_exchange_rates` fx
  ON inv.Invoice_Date = fx.Rate_Date 
 AND inv.Invoice_Currency = fx.From_Currency 
 AND fx.To_Currency = 'USD';