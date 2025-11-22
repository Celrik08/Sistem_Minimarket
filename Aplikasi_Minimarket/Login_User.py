from Data_User import muat_user

def login_user(nama_user, kata_sandi):
    user = muat_user()
    for id_user, data in user.items():
        if data.get("username") == nama_user and data.get("password") == kata_sandi:
            return {"id": id_user, **data}
    return None