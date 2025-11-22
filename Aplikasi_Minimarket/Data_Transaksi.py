# Sabrina Data Transaksi
import json
import os

folder_skrip = os.path.dirname(os.path.abspath(__file__))
Data_Transaksi = os.path.join(folder_skrip, "Data_Base", "Data_Transaksi.json")

def muat_transaksi():
    if not os.path.exists(Data_Transaksi):
        with open(Data_Transaksi, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(Data_Transaksi, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
        except:
            return {}

def simpan_transaksi(transaksi_dict):
    with open(Data_Transaksi, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in transaksi_dict.items()}, f, indent=4, ensure_ascii=False)