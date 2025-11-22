import os
import sys
import tkinter as tk
from tkinter import ttk, Menu
from Data_Produk import muat_produk
from Login_User import login_user
from Register_User import register_user
from Tambah_Produk import tambah_produk
from Ubah_Produk import ubah_produk
from Hapus_Produk import hapus_produk
from Beli_Produk import beli_produk_gui
from Riwayat_Penjualan import muat_riwayat
from tkinter import messagebox
from Tambah_Produk import tambah_produk
from Ubah_Produk import ubah_produk
from Hapus_Produk import hapus_produk
from tkinter import messagebox
from Login_User import login_user

# Fajar buat Class
class Aplikasi:
    def __init__(self, root):
        self.root = root
        root.title("Minimarket One Logic")
        root.geometry("800x500")
        self.user_saat_ini = None
        self.buat_tampilan_login()

    def bersihkan_root(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.config(menu="")

    # Fajar Login
    def buat_tampilan_login(self):
        self.bersihkan_root()
        frm = ttk.Frame(self.root, padding=20)
        frm.pack(expand=True)

        lbl_judul = ttk.Label(frm, text="FormLogin", font=("Arial", 16))
        lbl_judul.grid(row=0, column=0, columnspan=2, pady=(0,10))

        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_username = ttk.Entry(frm)
        self.entry_username.grid(row=1, column=1, pady=5)
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus())

        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_password = ttk.Entry(frm, show="*")
        self.entry_password.grid(row=2, column=1, pady=5)
        self.entry_password.bind("<Return>", lambda e: self.Login())

        self.var_tampilkan = tk.BooleanVar()

        chk = ttk.Checkbutton(
            frm,
            text="Tampilkan Password",
            variable=self.var_tampilkan,
            command=self.toggle_password
        )
        chk.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        btn_login = ttk.Button(frm, text="Login", command=self.Login)
        btn_login.grid(row=4, column=0, pady=15)

        btn_register = ttk.Button(frm, text="Register", command=self.buka_form_register)
        btn_register.grid(row=4, column=1, pady=15)

        btn_register = ttk.Button(frm, text="Logout", command=self.Logout)
        btn_register.grid(row=4, column=2, pady=15)

    
    def toggle_password(self):
        if self.var_tampilkan.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    
    def Login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        user = login_user(username, password)
        if user is None:
            tk.messagebox.showerror("Error", "Username atau password salah!")
            return
        self.user_saat_ini = user
        if user["role"] == "admin":
            self.Menu_Admin()
        else:
            self.tampilkan_menu_user()

    # Register Meilonie
    def buka_form_register(self):
        self.bersihkan_root()

        frm = ttk.Frame(self.root, padding=20)
        frm.pack(expand=True)

        ttk.Label(frm, text="Form Register", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.reg_username = ttk.Entry(frm)
        self.reg_username.grid(row=1, column=1, pady=5)
        self.reg_username.bind("<Return>", lambda e: self.reg_password.focus())

        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.reg_password = ttk.Entry(frm)
        self.reg_password.grid(row=2, column=1, pady=5)
        self.reg_password.bind("<Return>", lambda e: self.proses_register())

        ttk.Button(frm, text="Register", command=self.proses_register).grid(row=3, column=0, pady=15)

        ttk.Button(frm, text="Back", command=self.buat_tampilan_login).grid(row=3, column=1, pady=15)

    def proses_register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()

        if not username or not password:
            tk.messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
            return

        hasil = register_user(username, password)

        if hasil is None:
            tk.messagebox.showerror("Error", "Username sudah digunakan!")
            self.reg_username.delete(0, tk.END)
            return

        tk.messagebox.showinfo("Sukses", "Username dan password telah tersimpan!")

        self.buat_tampilan_login()
    
    def Logout(self): 
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    # Fajar Menu Admin
    def Menu_Admin(self):
        self.bersihkan_root()
        menubar = Menu(self.root)
        menu_data = Menu(menubar, tearoff=0)
        menu_data.add_command(label="Data Produk", command=self.Menu_Data_Produk)
        menubar.add_cascade(label="Produk", menu=menu_data)
        menu_data1 = Menu(menubar, tearoff=0)
        menu_data1.add_command(label="Data Penjualan", command=self.Menu_Laporan_Penjualan)
        menubar.add_cascade(label="Laporan Penjualan", menu=menu_data1)
        menubar.add_command(label="Back", command=self.buat_tampilan_login)
        self.root.config(menu=menubar)

        kontainer = ttk.Frame(self.root, padding=10)
        kontainer.pack(fill="both", expand=True)
        ttk.Label(kontainer, text=f"Welcome Admin: {self.user_saat_ini['username']}", font=("Arial", 12)).pack(pady=5)

        self.tree = ttk.Treeview(kontainer, columns=("ID","Nama","Harga","Stok"), show="headings", height=15)
        for col in ("ID","Nama","Harga","Stok"):
            self.tree.heading(col, text=col)
            if col == "Nama":
                self.tree.column(col, width=300)
            else:
                self.tree.column(col, width=120, anchor="center")
        self.tree.pack(pady=10, fill="x")

        self.refresh_tree()

    # Fajar Menu Data_Produk
    def Menu_Data_Produk(self):
        self.bersihkan_root()

        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Data Produk", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frm, text="ID Produk:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = ttk.Entry(frm)
        self.entry_id.grid(row=1, column=1, pady=5)
        self.entry_id.bind("<Return>", lambda e: self.entry_nama.focus())

        ttk.Label(frm, text="Nama Produk:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_nama = ttk.Entry(frm)
        self.entry_nama.grid(row=2, column=1, pady=5)
        self.entry_nama.bind("<Return>", lambda e: self.entry_harga.focus())

        ttk.Label(frm, text="Harga Produk:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_harga = ttk.Entry(frm)
        self.entry_harga.grid(row=3, column=1, pady=5)
        self.entry_harga.bind("<Return>", lambda e: self.entry_stok.focus())

        ttk.Label(frm, text="Stok Produk:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_stok = ttk.Entry(frm)
        self.entry_stok.grid(row=4, column=1, pady=5)
        self.entry_stok.bind("<Return>", lambda e: self.tambah_produk_gui())


        ttk.Button(frm, text="Tambah", command=self.tambah_produk_gui).grid(row=5, column=0, pady=10)
        ttk.Button(frm, text="Ubah", command=self.ubah_produk_gui).grid(row=5, column=1, pady=10)
        ttk.Button(frm, text="Hapus", command=self.hapus_produk_gui).grid(row=5, column=2, pady=10)
        ttk.Button(frm, text="Back", command=self.Menu_Admin).grid(row=5, column=3, pady=10)

        self.tree_produk = ttk.Treeview(frm, columns=("ID","Nama","Harga","Stok"), show="headings", height=10)
        for col in ("ID","Nama","Harga","Stok"):
            self.tree_produk.heading(col, text=col)
            if col == "Nama":
                self.tree_produk.column(col, width=200)
            else:
                self.tree_produk.column(col, width=100, anchor="center")
        self.tree_produk.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

        self.tree_produk.bind("<<TreeviewSelect>>", self.pilih_produk)

        self.refresh_tree_produk()

    def refresh_tree_produk(self):
        for row in self.tree_produk.get_children():
            self.tree_produk.delete(row)
        produk = muat_produk()
        for idp, data in produk.items():
            self.tree_produk.insert("", "end", values=(idp, data["nama"], data["harga"], data["stok"]))

    def pilih_produk(self, event):
        selected = self.tree_produk.selection()
        if selected:
            values = self.tree_produk.item(selected[0], "values")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, values[0])
            self.entry_nama.delete(0, tk.END)
            self.entry_nama.insert(0, values[1])
            self.entry_harga.delete(0, tk.END)
            self.entry_harga.insert(0, values[2])
            self.entry_stok.delete(0, tk.END)
            self.entry_stok.insert(0, values[3])

    def tambah_produk_gui(self):
        tambah_produk(self.root, self.entry_id, self.entry_nama, self.entry_harga, self.entry_stok)
        self.refresh_tree_produk()

    def ubah_produk_gui(self):
        ubah_produk(self.root, self.entry_id, self.entry_nama, self.entry_harga, self.entry_stok)
        self.refresh_tree_produk()

    def hapus_produk_gui(self):
        hapus_produk(self.root, self.entry_id, self.entry_nama, self.entry_harga, self.entry_stok)
        self.refresh_tree_produk()
    
    # Meilonie Riwayat_Penjualan
    def Menu_Laporan_Penjualan(self):
        self.bersihkan_root()

        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Laporan Penjualan", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(frm, columns=("ID", "Total"), show="headings", height=12)
        tree.column("ID", width=150, anchor="center")
        tree.column("Total", width=200, anchor="center")

        tree.heading("ID", text="ID Transaksi")
        tree.heading("Total", text="Total Penjualan")

        tree.pack(pady=10, fill="x")

        riwayat = muat_riwayat()

        total_semua = 0

        for idp, data in riwayat.items():
            nilai = data["total_penjualan"]
            total_semua += nilai
            tree.insert("", "end", values=(idp, nilai))

        ttk.Label(frm, text="Total Semua Penjualan:").pack(pady=(10, 2))

        self.entry_total_laporan = ttk.Entry(frm, justify="center")
        self.entry_total_laporan.pack(pady=5)

        self.entry_total_laporan.insert(0, str(total_semua))
        self.entry_total_laporan.config(state="readonly")

        ttk.Button(frm, text="Back", command=self.Menu_Admin).pack(pady=10)

    # Sabrina Menu User
    def tampilkan_menu_user(self):
        self.bersihkan_root()
        menubar = Menu(self.root)

        menu_beli = Menu(menubar, tearoff=0)
        menu_beli.add_command(label="Beli", command=lambda: (beli_produk_gui(self, self.root), self.refresh_tree()))
        menubar.add_cascade(label="Beli Produk", menu=menu_beli)

        menubar.add_command(label="Back", command=self.buat_tampilan_login)
        self.root.config(menu=menubar)

        kontainer = ttk.Frame(self.root, padding=10)
        kontainer.pack(fill="both", expand=True)
        ttk.Label(kontainer, text=f"Welcome User: {self.user_saat_ini['username']}", font=("Arial", 12)).pack(pady=5)

        self.tree = ttk.Treeview(kontainer, columns=("ID","Nama","Harga","Stok"), show="headings", height=15)
        for col in ("ID","Nama","Harga","Stok"):
            self.tree.heading(col, text=col)
            if col == "Nama":
                self.tree.column(col, width=300)
            else:
                self.tree.column(col, width=120, anchor="center")
        self.tree.pack(pady=10, fill="x")

        self.refresh_tree()

    def refresh_tree(self):

        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            produk = muat_produk()
            for idp, data in produk.items():
                self.tree.insert("", "end", values=(idp, data["nama"], f"Rp{data['harga']}", data["stok"]))
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikasi(root)
    root.mainloop()