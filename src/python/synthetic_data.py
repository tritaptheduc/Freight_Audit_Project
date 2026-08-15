import os
import random
from datetime import datetime, timedelta
import pandas as pd

# Thiết lập seed cố định để dữ liệu tái lập chính xác mỗi lần chạy
random.seed(42)

# Tạo thư mục "data" nếu chưa tồn tại
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. TẠO BẢNG: dim_exchange_rates (Biến động Tỷ giá)
# ---------------------------------------------------------
print("⏳ Đang tạo bảng dim_exchange_rates...")
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 7, 1)

exchange_rate_data = []
curr_date = start_date

# Tỷ giá gốc
eur_usd_base = 1.0850
vnd_usd_base = 0.0000405

while curr_date <= end_date:
    date_str = curr_date.strftime("%Y-%m-%d")

    # Giả lập biến động tỷ giá nhẹ hàng ngày (+/- 0.5%)
    eur_rate = round(eur_usd_base * random.uniform(0.995, 1.005), 4)
    vnd_rate = round(vnd_usd_base * random.uniform(0.998, 1.002), 8)

    exchange_rate_data.append(
        {
            "Rate_Date": date_str,
            "From_Currency": "EUR",
            "To_Currency": "USD",
            "Exchange_Rate": eur_rate,
        }
    )
    exchange_rate_data.append(
        {
            "Rate_Date": date_str,
            "From_Currency": "VND",
            "To_Currency": "USD",
            "Exchange_Rate": vnd_rate,
        }
    )

    curr_date += timedelta(days=1)

df_exchange_rates = pd.DataFrame(exchange_rate_data)

# ---------------------------------------------------------
# 2. TẠO BẢNG: dim_contract_rates (Hợp đồng Cước Phức hợp)
# ---------------------------------------------------------
print("⏳ Đang tạo bảng dim_contract_rates...")
carriers = ["Maersk", "CMA CGM", "COSCO", "ONE", "Evergreen", "MSC"]
pol_list = ["VNHPH", "VNSGN", "VNDNG"]
pod_list = ["CNSHA", "DEHAM", "NLRTM", "USLAX"]
container_types = ["20DC", "40HC"]

contract_data = []
contract_id_counter = 1001

for carrier in carriers:
    for pol in pol_list:
        for pod in pod_list:
            for cont in container_types:
                currency = random.choice(["USD", "USD", "USD", "EUR"])
                base_rate = (
                    random.randint(500, 3500)
                    if currency == "USD"
                    else random.randint(450, 3200)
                )

                fuel_type = random.choice(["PERCENTAGE", "FLAT"])
                fuel_rate = (
                    random.choice([0.10, 0.12, 0.15])
                    if fuel_type == "PERCENTAGE"
                    else random.randint(120, 300)
                )

                contract_data.append(
                    {
                        "Contract_ID": f"CTR-{contract_id_counter}",
                        "Carrier": carrier,
                        "POL_Origin": pol,
                        "POD_Destination": pod,
                        "Container_Type": cont,
                        "Currency": currency,
                        "Agreed_Base_Rate": float(base_rate),
                        "Fuel_Surcharge_Type": fuel_type,
                        "Agreed_Fuel_Rate": fuel_rate,
                        "Free_Demurrage_Days": random.choice([5, 7]),
                        "Demurrage_Tier1_Rate": 50.0,  # 5 ngày quá hạn đầu
                        "Demurrage_Tier2_Rate": 100.0,  # Từ ngày quá hạn thứ 6
                        "Free_Detention_Days": random.choice([3, 5]),
                        "Detention_Daily_Rate": 40.0,
                    }
                )
                contract_id_counter += 1

df_contracts = pd.DataFrame(contract_data)

# ---------------------------------------------------------
# 3. TẠO BẢNG: fact_shipments_bol (Thực tế Vận chuyển & WMS)
# ---------------------------------------------------------
print("⏳ Đang tạo bảng fact_shipments_bol...")
num_shipments = 1200
shipment_data = []

for i in range(1, num_shipments + 1):
    bol_num = f"BOL2026{i:05d}"
    matched_contract = df_contracts.sample(1).iloc[0]

    shipment_date = start_date + timedelta(days=random.randint(0, 150))
    transit_days = random.randint(15, 30)
    promised_delivery = shipment_date + timedelta(days=transit_days)

    # 10% đơn bị trễ hẹn SLA do các nguyên nhân khác nhau
    delay_days = 0
    root_cause = "NONE"
    if random.random() < 0.10:
        delay_days = random.randint(1, 5)
        root_cause = random.choice(
            ["CARRIER_ERROR", "CUSTOMS_HOLD", "WEATHER"]
        )

    actual_delivery = promised_delivery + timedelta(days=delay_days)

    # Đo lường trọng lượng Kho WMS (KG)
    wms_weight = round(random.uniform(10000, 26000), 1)

    # Các mốc thời gian luân chuyển vỏ Container & Bãi Cảng
    gate_in_port = shipment_date - timedelta(days=random.randint(1, 3))
    # Số ngày nằm bãi cảng (Demurrage)
    port_stay_days = random.randint(2, 16)
    gate_out_port = gate_in_port + timedelta(days=port_stay_days)

    # Số ngày giữ vỏ container tại kho (Detention)
    detention_stay_days = random.randint(1, 12)
    empty_return = gate_out_port + timedelta(days=detention_stay_days)

    shipment_data.append(
        {
            "BOL_Number": bol_num,
            "Contract_ID": matched_contract["Contract_ID"],
            "Shipment_Date": shipment_date.strftime("%Y-%m-%d"),
            "Promised_SLA_Delivery_Date": promised_delivery.strftime(
                "%Y-%m-%d"
            ),
            "Actual_Delivery_Date": actual_delivery.strftime("%Y-%m-%d"),
            "WMS_Measured_Weight_KG": wms_weight,
            "Gate_In_Port_Date": gate_in_port.strftime("%Y-%m-%d"),
            "Gate_Out_Port_Date": gate_out_port.strftime("%Y-%m-%d"),
            "Empty_Return_Date": empty_return.strftime("%Y-%m-%d"),
            "Root_Cause_Delay": root_cause,
            # Lưu tạm thông tin hợp đồng để dùng cho bước sinh hóa đơn
            "_ctr_ref": matched_contract,
            "_port_stay_days": port_stay_days,
            "_detention_stay_days": detention_stay_days,
        }
    )

df_shipments = pd.DataFrame(shipment_data)

# ---------------------------------------------------------
# 4. TẠO BẢNG: raw_carrier_invoices (Có chèn lỗi nghiệp vụ)
# ---------------------------------------------------------
print("⏳ Đang tạo bảng raw_carrier_invoices...")
invoice_data = []
inv_id_counter = 5001

for idx, row in df_shipments.iterrows():
    inv_num = f"INV-2026-{inv_id_counter}"
    bol_num = row["BOL_Number"]
    ctr = row["_ctr_ref"]
    carrier = ctr["Carrier"]

    # Ngày xuất hóa đơn = Ngày giao hàng + 2 đến 5 ngày
    inv_date = datetime.strptime(
        row["Actual_Delivery_Date"], "%Y-%m-%d"
    ) + timedelta(days=random.randint(2, 5))
    inv_date_str = inv_date.strftime("%Y-%m-%d")

    # Loại tiền tệ hóa đơn (80% đồng nhất với hợp đồng, 20% hãng tàu xuất VND/EUR ngẫu nhiên)
    inv_currency = (
        ctr["Currency"] if random.random() < 0.8 else random.choice(["VND", "USD"])
    )

    # Lấy Tỷ giá để tính cước nếu hóa đơn khác tiền tệ hợp đồng
    fx_rate = 1.0
    if inv_currency != ctr["Currency"]:
        if inv_currency == "VND" and ctr["Currency"] == "USD":
            fx_rate = 24500.0
        elif inv_currency == "USD" and ctr["Currency"] == "EUR":
            fx_rate = 0.92

    # --- TÍNH CƯỚC CHUẨN THEO HỢP ĐỒNG ---
    base_rate = ctr["Agreed_Base_Rate"] * fx_rate

    # Fuel Surcharge
    if ctr["Fuel_Surcharge_Type"] == "PERCENTAGE":
        fuel_surcharge = base_rate * ctr["Agreed_Fuel_Rate"]
    else:
        fuel_surcharge = ctr["Agreed_Fuel_Rate"] * fx_rate

    # Demurrage Lũy tiến
    excess_dem_days = max(0, row["_port_stay_days"] - ctr["Free_Demurrage_Days"])
    if excess_dem_days == 0:
        demurrage_amt = 0.0
    elif excess_dem_days <= 5:
        demurrage_amt = excess_dem_days * ctr["Demurrage_Tier1_Rate"] * fx_rate
    else:
        demurrage_amt = (
            (5 * ctr["Demurrage_Tier1_Rate"])
            + ((excess_dem_days - 5) * ctr["Demurrage_Tier2_Rate"])
        ) * fx_rate

    # Detention
    excess_det_days = max(
        0, row["_detention_stay_days"] - ctr["Free_Detention_Days"]
    )
    detention_amt = excess_det_days * ctr["Detention_Daily_Rate"] * fx_rate

    billed_weight = row["WMS_Measured_Weight_KG"]

    # --- CHÈN LỖI NGHIỆP VỤ ANOMALY INJECTION ---
    rand_val = random.random()

    # Lỗi 1: Base Rate Overcharge (~3% số hóa đơn)
    if rand_val < 0.08:
        base_rate += 150.0 * fx_rate

    # Lỗi 2: Weight Discrepancy - Phóng đại cân nặng trên 10% (~4% số hóa đơn)
    elif rand_val < 0.11:
        billed_weight = round(billed_weight * random.uniform(1.12, 1.25), 1)

    # Lỗi 3: Demurrage Overcharge - Tính phạt dù chưa vượt ngày Free (~3% số hóa đơn)
    elif rand_val < 0.14 and excess_dem_days == 0:
        demurrage_amt = 200.0 * fx_rate

    # Lỗi 4: Detention Overcharge (~3% số hóa đơn)
    elif rand_val < 0.18:
        detention_amt += 120.0 * fx_rate

    # Lỗi 5: Bỏ qua giảm trừ phạt SLA trễ hạn (~2% số hóa đơn)
    # (Đáng lẽ phải giảm cước do giao trễ lỗi Hãng tàu nhưng vẫn đòi full)

    billed_total = round(
        base_rate + fuel_surcharge + demurrage_amt + detention_amt, 2
    )

    invoice_data.append(
        {
            "Invoice_Number": inv_num,
            "BOL_Number": bol_num,
            "Carrier": carrier,
            "Invoice_Date": inv_date_str,
            "Invoice_Currency": inv_currency,
            "Billed_Weight_KG": billed_weight,
            "Billed_Base_Rate": round(base_rate, 2),
            "Billed_Fuel_Surcharge": round(fuel_surcharge, 2),
            "Billed_Demurrage_Amount": round(demurrage_amt, 2),
            "Billed_Detention_Amount": round(detention_amt, 2),
            "Billed_Total_Amount": billed_total,
        }
    )
    inv_id_counter += 1

df_invoices = pd.DataFrame(invoice_data)

# Lỗi 6: Duplicate Invoices - Hóa đơn trùng (~2% tổng số hóa đơn)
duplicate_samples = df_invoices.sample(n=25, random_state=42).copy()
duplicate_samples["Invoice_Number"] = duplicate_samples["Invoice_Number"].apply(
    lambda x: f"{x}-DUP"
)
duplicate_samples["Invoice_Date"] = pd.to_datetime(
    duplicate_samples["Invoice_Date"]
) + timedelta(days=1)
duplicate_samples["Invoice_Date"] = duplicate_samples[
    "Invoice_Date"
].dt.strftime("%Y-%m-%d")

df_invoices_final = pd.concat(
    [df_invoices, duplicate_samples], ignore_index=True
)

# ---------------------------------------------------------
# 5. LÀM SẠCH VÀ XUẤT CSV VÀO THƯ MỤC "data/"
# ---------------------------------------------------------
# Loại bỏ các cột tạm ẩn
df_shipments_clean = df_shipments.drop(
    columns=["_ctr_ref", "_port_stay_days", "_detention_stay_days"]
)

# Export file CSV
df_exchange_rates.to_csv(
    os.path.join(OUTPUT_DIR, "dim_exchange_rates.csv"), index=False
)
df_contracts.to_csv(
    os.path.join(OUTPUT_DIR, "dim_contract_rates.csv"), index=False
)
df_shipments_clean.to_csv(
    os.path.join(OUTPUT_DIR, "fact_shipments_bol.csv"), index=False
)
df_invoices_final.to_csv(
    os.path.join(OUTPUT_DIR, "raw_carrier_invoices.csv"), index=False
)

print("\n SẢN PHẨM ĐÃ ĐƯỢC TẠO THÀNH CÔNG TRONG THƯ MỤC 'data/':")
print(
    f" 1. dim_exchange_rates.csv  ({len(df_exchange_rates)} dòng) -> Tỷ giá biến động EUR/VND về USD"
)
print(
    f" 2. dim_contract_rates.csv  ({len(df_contracts)} dòng) -> Khung cước & Demurrage/Detention lũy tiến"
)
print(
    f" 3. fact_shipments_bol.csv  ({len(df_shipments_clean)} dòng) -> Vận đơn thực tế & Cân nặng WMS"
)
print(
    f" 4. raw_carrier_invoices.csv ({len(df_invoices_final)} dòng) -> Hóa đơn hãng tàu (Đã chèn 6 loại lỗi)"
)