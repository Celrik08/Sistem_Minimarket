# Search Barang Sabrina
import tkinter as tk
from tkinter import ttk
from Data_Produk import muat_produk

def search_barang_gui(parent, id_barang_var, nama_barang_var, harga_var):
    produk = muat_produk()

    win = tk.Toplevel(parent)
    win.title("Search Barang")
    win.geometry("600x400")

    tk.Label(win, text="Search:").pack(anchor="w", padx=10, pady=5)
    search_var = tk.StringVar()
    entry_search = tk.Entry(win, textvariable=search_var)
    entry_search.pack(fill="x", padx=10)
    entry_search.focus_set()

    tree = ttk.Treeview(win, columns=("id","nama","harga","stok"), show="headings", height=12)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("id","nama","harga","stok"):
        tree.heading(col, text=col.upper())
        tree.column(col, width=120)

    def tampilkan_data(data):
        tree.delete(*tree.get_children())
        for idb, d in data.items():
            tree.insert("", "end", values=(idb, d["nama"], d["harga"], d["stok"]))

    tampilkan_data(produk)

    def filter_data(*args):
        kata = search_var.get().lower()

        data_filter = {
            k: v for k, v in produk.items()
            if kata in str(k).lower() or kata in v["nama"].lower()
        }

        tampilkan_data(data_filter)

    search_var.trace_add("write", filter_data)

    def pilih_barang(event=None):
        current = tree.focus()
        if current:
            vals = tree.item(current, "values")
            id_barang_var.set(vals[0])
            nama_barang_var.set(vals[1])
            harga_var.set(vals[2])
            win.destroy()

            parent.focus()
            try:
                qty_entry = parent.nametowidget("qty_entry")
                qty_entry.focus_set()
            except:
                pass

    tree.bind("<Return>", pilih_barang)
    tree.bind("<Double-1>", pilih_barang)

    def enter_search(event):
        items = tree.get_children()
        if items:
            tree.focus(items[0])
            tree.selection_set(items[0])
            tree.see(items[0])

        pilih_barang()

    entry_search.bind("<Return>", enter_search)

    def pilih_baris(index):
        items = tree.get_children()
        if not items:
            return
        tree.selection_set(items[index])
        tree.focus(items[index])
        tree.see(items[index])

    def panah_bawah(event):
        items = tree.get_children()
        if not items:
            return "break"

        current = tree.focus()
        if current == "":
            pilih_baris(0)
            return "break"

        index = items.index(current)
        if index == len(items) - 1:
            pilih_baris(0)
        else:
            pilih_baris(index + 1)
        return "break"

    def panah_atas(event):
        items = tree.get_children()
        if not items:
            return "break"

        current = tree.focus()
        if current == "":
            pilih_baris(0)
            return "break"

        index = items.index(current)
        if index == 0:
            pilih_baris(len(items) - 1)
        else:
            pilih_baris(index - 1)
        return "break"

    win.bind("<Down>", panah_bawah)
    win.bind("<Up>", panah_atas)