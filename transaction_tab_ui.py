# gui_tabs/transaction_tab_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modules import transactions

def transaction_tab_ui(app):
    frame = tk.Frame(app)

    def refresh_txns():
        for i in tree.get_children():
            tree.delete(i)
        for row in transactions.get_all_transactions(app.cursor):
            tree.insert("", "end", values=row)

    def add_txn():
        try:
            account_id = int(account_entry.get())
            amount = float(amount_entry.get())
            txn_type = txn_type_var.get()
            if txn_type not in ["credit", "debit"]:
                raise ValueError("Invalid type")
            transactions.add_transaction(app.cursor, account_id, amount, txn_type)
            app.conn.commit()
            messagebox.showinfo("Success", "Transaction added")
            refresh_txns()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Form
    tk.Label(frame, text="Account ID").grid(row=0, column=0, padx=5, pady=5)
    account_entry = tk.Entry(frame)
    account_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Amount").grid(row=1, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Type").grid(row=2, column=0, padx=5, pady=5)
    txn_type_var = tk.StringVar()
    ttk.Combobox(frame, textvariable=txn_type_var, values=["credit", "debit"]).grid(row=2, column=1, padx=5, pady=5)

    tk.Button(frame, text="Add Transaction", command=add_txn).grid(row=3, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(frame, columns=("ID", "AccountID", "Amount", "Type", "Date"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=4, column=0, columnspan=2, pady=10)

    refresh_txns()
    return frame
