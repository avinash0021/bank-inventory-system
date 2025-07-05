# gui_tabs/account_tab_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modules import accounts

def account_tab_ui(app):
    frame = tk.Frame(app)

    def refresh_accounts():
        for i in tree.get_children():
            tree.delete(i)
        for row in accounts.get_all_accounts(app.cursor):
            tree.insert("", "end", values=row)

    def add_account():
        acc = acc_entry.get()
        ifsc = ifsc_entry.get()
        holder = holder_entry.get()
        if not acc or not ifsc or not holder:
            messagebox.showerror("Error", "All fields required")
            return
        accounts.add_account(app.cursor, acc, ifsc, holder)
        app.conn.commit()
        messagebox.showinfo("Success", "Account added")
        refresh_accounts()

    tk.Label(frame, text="Account Number").grid(row=0, column=0, padx=5, pady=5)
    acc_entry = tk.Entry(frame)
    acc_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="IFSC Code").grid(row=1, column=0, padx=5, pady=5)
    ifsc_entry = tk.Entry(frame)
    ifsc_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Holder Name").grid(row=2, column=0, padx=5, pady=5)
    holder_entry = tk.Entry(frame)
    holder_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(frame, text="Add Account", command=add_account).grid(row=3, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(frame, columns=("ID", "Account", "IFSC", "Holder"), show="headings")
    for col in ["ID", "Account", "IFSC", "Holder"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.grid(row=4, column=0, columnspan=2, pady=10)

    refresh_accounts()
    return frame
