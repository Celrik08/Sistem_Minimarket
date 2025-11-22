# Fajar Tambah Produk
from Data_Produk import muat_produk, simpan_produk
from tkinter import messagebox

def tambah_produk(parent, entry_id, entry_nama, entry_harga, entry_stok):

    id_text = entry_id.get().strip()
    nama = entry_nama.get().strip()
    harga_text = entry_harga.get().strip()
    stok_text = entry_stok.get().strip()

    if not nama:
        messagebox.showerror("Error", "Nama produk tidak boleh kosong!", parent=parent)
        return

    if not harga_text.isdigit() or not stok_text.isdigit():
        messagebox.showerror("Error", "Harga dan Stok harus berupa angka!", parent=parent)
        entry_harga.delete(0, "end")
        entry_stok.delete(0, "end")
        entry_harga.focus()
        return

    harga = int(harga_text)
    stok = int(stok_text)

    produk = muat_produk()

    if not id_text:
        new_id = max(produk.keys()) + 1 if produk else 1
    else:
        if not id_text.isdigit():
            messagebox.showerror("Error", "ID harus angka!", parent=parent)
            return
        new_id = int(id_text)
        if new_id in produk:
            messagebox.showerror("Error", "ID produk sudah ada!", parent=parent)
            return

    produk[new_id] = {"nama": nama, "harga": harga, "stok": stok}
    simpan_produk(produk)
    messagebox.showinfo("Sukses", "Produk berhasil ditambahkan.", parent=parent)

    entry_id.delete(0, "end")
    entry_nama.delete(0, "end")
    entry_harga.delete(0, "end")
    entry_stok.delete(0, "end")