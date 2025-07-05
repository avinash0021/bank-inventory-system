import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import ImageTk, Image
import sqlite3
import hashlib
import os
import csv
from datetime import datetime
from modules import assets, customers, sales, accounts, transactions
from gui_tabs import asset_tab_ui, customer_tab_ui, sales_tab_ui, account_tab_ui, transaction_tab_ui

DB_PATH = os.path.join("db", "bank_inventory_final.db")
BG_IMAGE = os.path.join("assets", "login_bg.png")

class BankInventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Inventory System")
        self.geometry("1024x720")
        self.resizable(False, False)

        os.makedirs("db", exist_ok=True)
        os.makedirs("exports", exist_ok=True)
        os.makedirs("pdfs", exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.bg_image = ImageTk.PhotoImage(Image.open(BG_IMAGE))
        self.canvas = tk.Canvas(self, width=1024, height=720, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.current_user = None
        self.create_login_screen()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            value REAL NOT NULL,
            low_stock_threshold INTEGER DEFAULT 5
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            asset_id INTEGER,
            quantity INTEGER NOT NULL,
            amount REAL,
            sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(asset_id) REFERENCES assets(id)
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            ifsc_code TEXT NOT NULL,
            holder_name TEXT NOT NULL
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            amount REAL,
            type TEXT CHECK(type IN ('credit', 'debit')),
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )""")
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_widgets()
        self.canvas = tk.Canvas(self, width=1024, height=720, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Shift login form below the heading
        y_offset = 360

        self.username_entry = tk.Entry(self, font=("Arial", 13), fg="grey")
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", lambda e: self._focus_in(self.username_entry, "Username"))
        self.username_entry.bind("<FocusOut>", lambda e: self._focus_out(self.username_entry, "Username"))
        self.canvas.create_window(400, y_offset, anchor="nw", window=self.username_entry, width=230)

        self.password_entry = tk.Entry(self, font=("Arial", 13), show="", fg="grey")
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", lambda e: self._focus_in_pass())
        self.password_entry.bind("<FocusOut>", lambda e: self._focus_out_pass())
        self.canvas.create_window(400, y_offset + 50, anchor="nw", window=self.password_entry, width=230)

        self.show_pass = tk.IntVar()
        show_cb = tk.Checkbutton(self, text="Show Password", variable=self.show_pass, command=self.toggle_password)
        self.canvas.create_window(400, y_offset + 80, anchor="nw", window=show_cb)

        login_btn = tk.Button(self, text="Login", command=self.login)
        register_btn = tk.Button(self, text="Register", command=self.register_screen)
        forgot_btn = tk.Button(self, text="Forgot Password", command=self.forgot_screen)

        self.canvas.create_window(400, y_offset + 120, anchor="nw", window=login_btn, width=100)
        self.canvas.create_window(530, y_offset + 120, anchor="nw", window=register_btn, width=100)
        self.canvas.create_window(460, y_offset + 160, anchor="nw", window=forgot_btn, width=120)

    def _focus_in(self, entry, text):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg="black")

    def _focus_out(self, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg="grey")

    def _focus_in_pass(self):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="black", show="*" if not self.show_pass.get() else "")

    def _focus_out_pass(self):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="grey", show="")

    def toggle_password(self):
        if self.show_pass.get():
            if self.password_entry.get() != "Password":
                self.password_entry.config(show="")
        else:
            if self.password_entry.get() != "Password":
                self.password_entry.config(show="*")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in ["", "Username"] or password in ["", "Password"]:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return

        hashed = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        result = self.cursor.fetchone()

        if result:
            self.current_user = result
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.create_main_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def register_screen(self):
        def perform_register():
            u = username_entry.get()
            p = password_entry.get()
            r = role_var.get()
            if not u or not p:
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                    (u, self.hash_password(p), r))
                self.conn.commit()
                messagebox.showinfo("Success", "User registered!")
                self.create_login_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")

        self.clear_widgets()
        tk.Label(self, text="Register New User", font=("Arial", 16)).pack(pady=10)
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)
        role_var = tk.StringVar(value="staff")
        ttk.Combobox(self, textvariable=role_var, values=["admin", "staff"]).pack(pady=5)
        tk.Button(self, text="Register", command=perform_register).pack(pady=10)
        tk.Button(self, text="Back", command=self.create_login_screen).pack()

    def forgot_screen(self):
        def reset_password():
            u = username_entry.get()
            new_p = password_entry.get()
            self.cursor.execute("SELECT * FROM users WHERE username=?", (u,))
            if self.cursor.fetchone():
                self.cursor.execute("UPDATE users SET password=? WHERE username=?", (self.hash_password(new_p), u))
                self.conn.commit()
                messagebox.showinfo("Success", "Password reset")
                self.create_login_screen()
            else:
                messagebox.showerror("Error", "Username not found")

        self.clear_widgets()
        tk.Label(self, text="Reset Password", font=("Arial", 16)).pack(pady=10)
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)
        tk.Button(self, text="Reset", command=reset_password).pack(pady=10)
        tk.Button(self, text="Back", command=self.create_login_screen).pack()

    def create_main_dashboard(self):
        self.clear_widgets()
        tk.Label(self, text=f"Welcome {self.current_user[1]} ({self.current_user[3]})", font=("Arial", 16)).pack(pady=5)

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        asset_tab = asset_tab_ui(self)
        customer_tab = customer_tab_ui(self)
        sales_tab = sales_tab_ui(self)
        account_tab = account_tab_ui(self)
        transaction_tab = transaction_tab_ui(self)

        tab_control.add(asset_tab, text="Assets")
        tab_control.add(customer_tab, text="Customers")
        tab_control.add(sales_tab, text="Sales")
        tab_control.add(account_tab, text="Accounts")
        tab_control.add(transaction_tab, text="Transactions")

if __name__ == "__main__":
    app = BankInventoryApp()
    app.mainloop()
