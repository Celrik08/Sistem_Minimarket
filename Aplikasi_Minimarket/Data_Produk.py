# Fajar Data_Produk
import json
import os

folder_skrip = os.path.dirname(os.path.abspath(__file__))
Data_Produk = os.path.join(folder_skrip,"Data_Base", "Data_Produk.json")

def muat_produk():
    if not os.path.exists(Data_Produk):
        with open(Data_Produk, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(Data_Produk, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
        except:
            return {}

def simpan_produk(produk_dict):
    with open(Data_Produk, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in produk_dict.items()}, f, indent=4, ensure_ascii=False)