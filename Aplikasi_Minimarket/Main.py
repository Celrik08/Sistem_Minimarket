import os
import sys
import tkinter as tk
from tkinter import ttk, Menu
from Data_Produk import muat_produk
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

        btn_register = ttk.Button(frm, text="Register")
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
            messagebox.showinfo("Sukses", "Selamat Datang User")
    
    def Logout(self): 
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    # Fajar Menu Admin
    def Menu_Admin(self):
        self.bersihkan_root()
        menubar = Menu(self.root)
        menu_data = Menu(menubar, tearoff=0)
        menu_data.add_command(label="Data Produk")
        menubar.add_cascade(label="Produk", menu=menu_data)
        menu_data1 = Menu(menubar, tearoff=0)
        menu_data1.add_command(label="Data Penjualan")
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