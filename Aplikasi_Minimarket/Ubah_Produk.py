# Fajar Ubah Produk
from Data_Produk import muat_produk, simpan_produk
from tkinter import messagebox

def ubah_produk(parent, entry_id, entry_nama, entry_harga, entry_stok):
    produk = muat_produk()
    id_text = entry_id.get().strip()
    if not id_text or not id_text.isdigit():
        messagebox.showerror("Error", "ID Produk harus diisi!", parent=parent)
        return

    idp = int(id_text)
    if idp not in produk:
        messagebox.showerror("Error", "ID produk tidak ditemukan!", parent=parent)
        return

    data = produk[idp]

    nama_baru = entry_nama.get().strip()
    harga_text = entry_harga.get().strip()
    stok_text = entry_stok.get().strip()

    if (nama_baru == data["nama"] and 
        harga_text == str(data["harga"]) and 
        stok_text == str(data["stok"])):
        messagebox.showinfo("Info", "Tidak ada data yang diubah.", parent=parent)
        return

    if harga_text and not harga_text.isdigit():
        messagebox.showerror("Error", "Harga harus berupa angka!", parent=parent)
        entry_harga.delete(0, "end")
        entry_harga.focus()
        return
    if stok_text and not stok_text.isdigit():
        messagebox.showerror("Error", "Stok harus berupa angka!", parent=parent)
        entry_stok.delete(0, "end")
        entry_stok.focus()
        return

    if nama_baru:
        data["nama"] = nama_baru
    if harga_text:
        data["harga"] = int(harga_text)
    if stok_text:
        data["stok"] = int(stok_text)

    produk[idp] = data
    simpan_produk(produk)
    messagebox.showinfo("Sukses", "Produk berhasil diubah.", parent=parent)