# Sabrina Beli Produk
import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from Data_Produk import muat_produk
from Data_Transaksi import muat_transaksi, simpan_transaksi
from Riwayat_Penjualan import muat_riwayat, simpan_riwayat
from Search_Barang import search_barang_gui

folder_skrip = os.path.dirname(os.path.abspath(__file__))
Data_Transaksi = os.path.join(folder_skrip, "Data_Base", "Data_Transaksi.json")

def bersihkan_root(root):
    for w in root.winfo_children():
        try:
            w.destroy()
        except:
            pass
    root.config(menu=None)

def generate_id_transaksi():
    riwayat = muat_riwayat()

    if not riwayat:
        return "TRS01"

    existing_ids = list(riwayat.keys())
    max_num = max(int(x.replace("TRS", "")) for x in existing_ids)
    return f"TRS{max_num+1:02d}"

def beli_produk_gui(self, parent):
    self.bersihkan_root()
    parent.withdraw()
    produk = muat_produk()

    window = tk.Toplevel(parent)
    window.title("Form Menu Transaksi")
    window.geometry("900x500")

    ttk.Label(window, text="Transaksi", font=("Arial", 16)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    ttk.Label(window, text="Id Transaksi:").grid(row=0, column=3, sticky="e", padx=5)
    id_transaksi_var = tk.StringVar()
    id_transaksi_var.set(generate_id_transaksi())
    entry_id_transaksi = ttk.Entry(window, textvariable=id_transaksi_var, state="readonly")
    entry_id_transaksi.grid(row=0, column=4, padx=5, pady=5)

    ttk.Label(window, text="Id Barang:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    id_barang_var = tk.StringVar()
    entry_id_barang = ttk.Entry(window, textvariable=id_barang_var)
    entry_id_barang.grid(row=1, column=1, padx=5, pady=5)
    entry_id_barang.bind("<Return>", lambda e: buka_search_barang())

    def buka_search_barang():
        search_barang_gui(window, id_barang_var, nama_barang_var, harga_var)

    def search_barang():
        search_barang_gui(window, id_barang_var, nama_barang_var, harga_var)

    btn_search = ttk.Button(window, text="Search Id Barang", command=search_barang)
    btn_search.grid(row=1, column=2, padx=5, pady=5)

    ttk.Label(window, text="Nama Barang:").grid(row=1, column=3, sticky="e", padx=5, pady=5)
    nama_barang_var = tk.StringVar()
    entry_nama_barang = ttk.Entry(window, textvariable=nama_barang_var, state="readonly")
    entry_nama_barang.grid(row=1, column=4, padx=5, pady=5)

    ttk.Label(window, text="Harga Satuan:").grid(row=1, column=5, sticky="e", padx=5, pady=5)
    harga_var = tk.StringVar()
    entry_harga = ttk.Entry(window, textvariable=harga_var, state="readonly")
    entry_harga.grid(row=1, column=6, padx=5, pady=5)

    ttk.Label(window, text="Qty:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    qty_var = tk.StringVar()
    entry_qty = ttk.Entry(window, textvariable=qty_var, name="qty_entry")
    entry_qty.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="Sub Total:").grid(row=2, column=3, sticky="e", padx=5, pady=5)
    sub_total_var = tk.StringVar()
    entry_sub_total = ttk.Entry(window, textvariable=sub_total_var, state="readonly")
    entry_sub_total.grid(row=2, column=4, padx=5, pady=5)

    entry_sub_total.bind("<Return>", lambda e: tambah_transaksi())

    # 🌟 UBAH KOLOM TREEVIEW "Id JSON" MENJADI "Id Transaksi"
    tree = ttk.Treeview(window,
        columns=("Id Transaksi","Id Barang","Nama","Harga","Qty","Sub Total"),
        show="headings",
        height=10
    )

    for col in ("Id Transaksi","Id Barang","Nama","Harga","Qty","Sub Total"):
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=3, column=0, columnspan=7, padx=10, pady=10)

    ttk.Label(window, text="Total Harga:").grid(row=4, column=5, sticky="e")
    total_harga_var = tk.StringVar()
    entry_total_harga = ttk.Entry(window, textvariable=total_harga_var, state="readonly")
    entry_total_harga.grid(row=4, column=6, padx=5, pady=5)

    def update_barang(*args):
        idb = id_barang_var.get()
        if not idb.isdigit() or idb.strip() == "":
            nama_barang_var.set("")
            harga_var.set("")
            return
        idb = int(idb)
        if idb in produk:
            nama_barang_var.set(produk[idb]["nama"])
            harga_var.set(produk[idb]["harga"])
        else:
            nama_barang_var.set("")
            harga_var.set("")

    id_barang_var.trace_add("write", update_barang)

    def hitung_sub_total(event=None):
        try:
            qty = int(qty_var.get())
            harga = int(harga_var.get())
            sub_total_var.set(qty * harga)
        except:
            sub_total_var.set("")
    
    def enter_qty(event):
        hitung_sub_total()
        entry_sub_total.focus_set()

    entry_qty.bind("<Return>", enter_qty)

    def tambah_transaksi():
        try:
            if entry_id_barang.get()=="" or entry_nama_barang.get()=="" or entry_harga.get()=="" or entry_qty.get()=="" or entry_sub_total.get()=="":
                messagebox.showerror("Error", "Lengkapi data transaksi!")
                return

            id_trx = id_transaksi_var.get()
            idb = int(entry_id_barang.get())
            nama = entry_nama_barang.get()
            harga = int(entry_harga.get())
            qty = int(entry_qty.get())
            subtotal = int(sub_total_var.get())

            if idb in produk:
                if qty > produk[idb]["stok"]:
                    messagebox.showerror("Error", f"Stok barang hanya {produk[idb]['stok']}")
                    entry_qty.focus_set()
                    return
            else:
                messagebox.showerror("Error", "Barang tidak ditemukan!")
                return

            transaksi = muat_transaksi()
            key_json = None

            for k, v in transaksi.items():
                if v["id_transaksi"] == id_trx and v["id_barang"] == idb:
                    key_json = k
                    break

            if key_json:
                transaksi[key_json]["qty"] += qty
                transaksi[key_json]["sub_total"] = transaksi[key_json]["qty"] * harga

                for item in tree.get_children():
                    row = tree.item(item,"values")
                    if int(row[0]) == key_json:
                        qty_baru = transaksi[key_json]["qty"]
                        sub_total_baru = transaksi[key_json]["sub_total"]
                        tree.item(item, values=(key_json, idb, nama, harga, qty_baru, sub_total_baru))
                        break

            else:

                key_json = max(transaksi.keys())+1 if transaksi else 1

                transaksi[key_json] = {
                    "id_transaksi": id_trx,
                    "id_barang": idb,
                    "nama_barang": nama,
                    "harga": harga,
                    "qty": qty,
                    "sub_total": subtotal
                }

                tree.insert("", "end", values=(key_json, idb, nama, harga, qty, subtotal))

            simpan_transaksi(transaksi)

            produk[idb]["stok"] -= qty
            with open(os.path.join(folder_skrip,"Data_Base","Data_Produk.json"),"w") as f:
                json.dump(produk, f, indent=4)

            entry_id_barang.delete(0, tk.END)
            nama_barang_var.set("")
            harga_var.set("")
            qty_var.set("")
            sub_total_var.set("")
            entry_id_barang.focus_set()

            total = sum(int(tree.item(i, "values")[5]) for i in tree.get_children())
            total_harga_var.set(total)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_klik = ttk.Button(window, text="Klik", command=tambah_transaksi)
    btn_klik.grid(row=2, column=6, padx=5, pady=5)

    def simpan_semua():

        if len(tree.get_children()) == 0:
            messagebox.showerror("Error", "Silahkan anda transaksi terlebih dahulu!\nTransaksi tidak bisa diproses.")
            return
        
        if entry_id_barang.get() or entry_nama_barang.get() or entry_harga.get() or entry_qty.get():
            messagebox.showwarning("Peringatan", "Masih melakukan transaksi!")
            return

        total = int(total_harga_var.get()) if total_harga_var.get() else 0
        id_trx = id_transaksi_var.get()

        riwayat = muat_riwayat()

        if id_trx not in riwayat:
            riwayat[id_trx] = {"total_penjualan": total}
        else:
            riwayat[id_trx]["total_penjualan"] = total

        simpan_riwayat(riwayat)

        simpan_transaksi({})

        for i in tree.get_children():
            tree.delete(i)

        total_harga_var.set("")
        entry_sub_total.delete(0, tk.END)

        id_transaksi_var.set(generate_id_transaksi())

        messagebox.showinfo("Sukses", "Transaksi berhasil disimpan!")

    btn_save = ttk.Button(window, text="Save", command=simpan_semua)
    btn_save.grid(row=4, column=4, padx=5, pady=5)

    def kembali_ke_menu_user():
        trx = muat_transaksi()

        if trx:
            messagebox.showwarning(
                "Peringatan",
                "Selesaikan dulu Transaksinya!\nData_Transaksi masih berisi."
            )
            return

        window.destroy()
        parent.deiconify()
        self.tampilkan_menu_user()

    btn_back = ttk.Button(window, text="Back", command=kembali_ke_menu_user)
    btn_back.grid(row=4, column=0, padx=5, pady=10)