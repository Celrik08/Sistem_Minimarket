# Meilonie Register User
from Data_User import muat_user, simpan_user

def register_user(nama_user, kata_sandi):
    user = muat_user()
    if any(u.get("username") == nama_user for u in user.values()):
        return None
    new_id = max(user.keys()) + 1 if user else 1
    user[new_id] = {"username": nama_user, "password": kata_sandi, "role": "user"}
    simpan_user(user)
    return {"id": new_id, **user[new_id]}