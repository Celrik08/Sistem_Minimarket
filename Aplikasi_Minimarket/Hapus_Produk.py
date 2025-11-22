# Fajar Hapus Data
from Data_Produk import muat_produk, simpan_produk
from tkinter import messagebox

def hapus_produk(parent, entry_id, entry_nama, entry_harga, entry_stok):
    produk = muat_produk()
    id_text = entry_id.get().strip()
    if not id_text or not id_text.isdigit():
        messagebox.showerror("Error", "ID Produk harus diisi, atau bukan angka!", parent=parent)
        return

    idp = int(id_text)
    if idp not in produk:
        messagebox.showerror("Error", "ID produk tidak ditemukan!", parent=parent)
        return

    konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus '{produk[idp]['nama']}'?", parent=parent)
    if konfirmasi:
        del produk[idp]
        simpan_produk(produk)
        messagebox.showinfo("Sukses", "Produk berhasil dihapus.", parent=parent)

        entry_id.delete(0, "end")
        entry_nama.delete(0, "end")
        entry_harga.delete(0, "end")
        entry_stok.delete(0, "end")