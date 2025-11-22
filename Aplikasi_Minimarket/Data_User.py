import json
import os

folder_skrip = os.path.dirname(os.path.abspath(__file__))
Data_User = os.path.join(folder_skrip, "Data_Base", "Data_User.json")

def muat_user():
    if not os.path.exists(Data_User):
        with open(Data_User, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(Data_User, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
        except:
            return {}

def simpan_user(user_dict):
    with open(Data_User, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in user_dict.items()}, f, indent=4, ensure_ascii=False)