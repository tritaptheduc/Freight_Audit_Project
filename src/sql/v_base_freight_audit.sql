CREATE OR REPLACE VIEW `freight-audit-project.freight_audit_db_2.v_base_freight_audit` AS
SELECT 
  inv.Invoice_Number,
  inv.Is_Duplicate_Invoice,
  sb.BOL_Number,
  sb.Shipment_Date,
  sb.Promised_SLA_Delivery_Date,
  sb.Actual_Delivery_Date,
  sb.Root_Cause_Delay,
  DATE_DIFF(sb.Actual_Delivery_Date, sb.Promised_SLA_Delivery_Date, DAY) AS SLA_Delay_Days,
  
  -- Thông tin Hợp đồng
  ctr.Contract_ID,
  ctr.Carrier,
  ctr.POL_Origin,
  ctr.POD_Destination,
  ctr.Container_Type,
  ctr.Agreed_Base_Rate,
  ctr.Free_Demurrage_Days,
  ctr.Free_Detention_Days,

  -- Cân nặng & Tải trọng
  sb.WMS_Measured_Weight_KG,
  inv.Billed_Weight_KG,
  ROUND(inv.Billed_Weight_KG - sb.WMS_Measured_Weight_KG, 2) AS Weight_Discrepancy_KG,
  ROUND((inv.Billed_Weight_KG - sb.WMS_Measured_Weight_KG) / sb.WMS_Measured_Weight_KG * 100, 2) AS Weight_Discrepancy_Pct,

  -- Số ngày lưu bãi & giữ vỏ thực tế
  DATE_DIFF(sb.Gate_Out_Port_Date, sb.Gate_In_Port_Date, DAY) AS Actual_Port_Stay_Days,
  DATE_DIFF(sb.Empty_Return_Date, sb.Gate_Out_Port_Date, DAY) AS Actual_Detention_Days,

  -- Cước phí bị tính trên Hóa đơn (USD)
  inv.Billed_Base_Rate * inv.FX_To_USD_Rate AS Billed_Base_Rate_USD,
  inv.Billed_Demurrage_Amount * inv.FX_To_USD_Rate AS Billed_Demurrage_USD,
  inv.Billed_Detention_Amount * inv.FX_To_USD_Rate AS Billed_Detention_USD,
  inv.Billed_Total_USD

FROM `freight-audit-project.freight_audit_db_2.v_stg_invoices` inv
JOIN `freight-audit-project.freight_audit_db_2.fact_shipments_bol` sb 
  ON inv.BOL_Number = sb.BOL_Number
JOIN `freight-audit-project.freight_audit_db_2.dim_contract_rates` ctr 
  ON sb.Contract_ID = ctr.Contract_ID;