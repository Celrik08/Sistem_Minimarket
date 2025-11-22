# Meilonie Riwayat Penjualan
import json
import os

folder_skrip = os.path.dirname(os.path.abspath(__file__))
Data_Riwayat = os.path.join(folder_skrip, "Data_Base", "Riwayat_Penjualan.json")

def muat_riwayat():
    if not os.path.exists(Data_Riwayat):
        with open(Data_Riwayat, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    with open(Data_Riwayat, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def simpan_riwayat(riwayat_dict):
    with open(Data_Riwayat, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in riwayat_dict.items()}, f, indent=4, ensure_ascii=False)